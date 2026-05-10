"""
gdoc-locate-comments: figure out which chapter/section each Drive API comment
belongs to by exporting the doc as DOCX and parsing the embedded comment anchors.

Why this script exists:
    The Drive Comments API returns `anchor: "kix.cmtNN"` — an opaque internal
    Google Docs ID. The public API does NOT expose where in the doc that anchor
    points to. DOCX export, however, embeds comment markers inline in
    word/document.xml so we can read positions directly.

Workflow:
    1. Drive API: export doc as DOCX (in-memory)
    2. Parse word/document.xml to find paragraphs + comment markers in order
    3. Parse word/comments.xml to get DOCX comment text + author
    4. Match DOCX comments <-> Drive API comments (read from
       documents/final-thesis-chapters/thesis-comments-raw.jsonl) by content
    5. Map each comment's paragraph index to its containing H1 chapter, using
       the same NN-slug folder convention as gdoc-read-final-thesis-chapters.py
    6. Regenerate comments.md with `**Located in:**` and `**Anchored text:**`
       fields appended to each comment.

Usage:
    python scripts/gdoc-locate-comments.py
    python scripts/gdoc-locate-comments.py --doc-id <FILE_ID>
    python scripts/gdoc-locate-comments.py --output-dir <PATH>
    python scripts/gdoc-locate-comments.py --debug-docx /tmp/thesis.docx

Prerequisite: doc shared with the service account as Viewer, and
thesis-comments-raw.jsonl already exists (run gdoc-read-comments.py first).
"""
import argparse
import importlib.util
import io
import json
import re
import sys
import unicodedata
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from googleapiclient.http import MediaIoBaseDownload

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_DOC_ID = "1B72mF57eyHFaCgTI-zVvZ01RWOuJInFemI-dVl_qxvA"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "documents" / "final-thesis-chapters"

DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def export_docx(drive, doc_id):
    request = drive.files().export_media(fileId=doc_id, mimeType=DOCX_MIME)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buf.getvalue()


def parse_docx_comments(docx_bytes):
    """Returns dict[docx_id] = {'author', 'date', 'text'}."""
    z = zipfile.ZipFile(io.BytesIO(docx_bytes))
    if "word/comments.xml" not in z.namelist():
        return {}
    root = ET.fromstring(z.read("word/comments.xml"))
    out = {}
    for c in root.findall("w:comment", NS):
        cid = c.get(f"{W_NS}id")
        author = c.get(f"{W_NS}author") or ""
        date = c.get(f"{W_NS}date") or ""
        texts = [t.text or "" for t in c.iter(f"{W_NS}t")]
        out[cid] = {"author": author, "date": date, "text": "".join(texts)}
    return out


def parse_docx_body(docx_bytes):
    """Walk paragraphs in document order. Each paragraph dict has:
        kind: 'title' | 'h1' | 'h2' | ... | 'normal'
        text: full paragraph text
        events: ordered list of ('range_start' | 'range_end' | 'ref', docx_id)
    """
    z = zipfile.ZipFile(io.BytesIO(docx_bytes))
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    paragraphs = []
    for p in body.findall("w:p", NS):
        # Detect paragraph style
        style = ""
        pPr = p.find("w:pPr", NS)
        if pPr is not None:
            pStyle = pPr.find("w:pStyle", NS)
            if pStyle is not None:
                style = pStyle.get(f"{W_NS}val", "")
        kind = "normal"
        if style.lower() == "title":
            kind = "title"
        else:
            m = re.match(r"^[Hh]eading\s*(\d)$", style)
            if m:
                kind = f"h{m.group(1)}"

        texts = []
        events = []
        for elem in p.iter():
            tag = elem.tag.replace(W_NS, "")
            if tag == "t":
                texts.append(elem.text or "")
            elif tag == "commentRangeStart":
                events.append(("range_start", elem.get(f"{W_NS}id")))
            elif tag == "commentRangeEnd":
                events.append(("range_end", elem.get(f"{W_NS}id")))
            elif tag == "commentReference":
                events.append(("ref", elem.get(f"{W_NS}id")))
        paragraphs.append({"kind": kind, "text": "".join(texts), "events": events})
    return paragraphs


def slugify(text, max_len=50):
    if not text:
        return "untitled-section"
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_only = ascii_only.replace("đ", "d").replace("Đ", "D")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "untitled-section"


def build_h1_index(paragraphs):
    """Returns list of (paragraph_index, folder_basename, h1_title) for each H1
    in document order. Matches the convention used in
    gdoc-read-final-thesis-chapters.py: NN-slug where NN is 1-indexed H1 order."""
    out = []
    n = 0
    for i, p in enumerate(paragraphs):
        if p["kind"] == "h1":
            n += 1
            out.append((i, f"{n:02d}-{slugify(p['text'])}", p["text"].strip()))
    return out


def chapter_for_paragraph(para_idx, h1_index):
    """Return (folder, title) of the H1 that contains the given paragraph."""
    chosen = ("00-front-matter", "(front matter — before first H1)")
    for h_idx, folder, title in h1_index:
        if h_idx <= para_idx:
            chosen = (folder, title)
        else:
            break
    return chosen


def nearest_subheading(para_idx, paragraphs, max_levels=("h2", "h3", "h4")):
    """Walk backwards from para_idx to find the closest heading at h2/h3/h4."""
    for j in range(para_idx, -1, -1):
        if paragraphs[j]["kind"] in max_levels:
            return paragraphs[j]["kind"], paragraphs[j]["text"].strip()
    return None, None


def locate_comments_in_body(paragraphs, h1_index):
    """For every DOCX comment id encountered in the body, record where it lives."""
    open_ranges = {}  # cid -> {'start': para_idx, 'chunks': []}
    located = {}     # cid -> {'chapter_folder', 'chapter_title', 'sub_kind',
                     #          'sub_title', 'anchored_text', 'paragraph_text', 'para_idx'}

    def finalize(cid, start_idx, chunks, end_para_text):
        folder, title = chapter_for_paragraph(start_idx, h1_index)
        sub_kind, sub_title = nearest_subheading(start_idx, paragraphs)
        anchored = " ".join(c.strip() for c in chunks if c.strip())[:300]
        if not anchored:
            anchored = end_para_text.strip()[:300]
        located[cid] = {
            "chapter_folder": folder,
            "chapter_title": title,
            "sub_kind": sub_kind,
            "sub_title": sub_title,
            "anchored_text": anchored,
            "paragraph_text": paragraphs[start_idx]["text"].strip()[:300],
            "para_idx": start_idx,
        }

    for i, p in enumerate(paragraphs):
        # Process events in order
        for event_kind, cid in p["events"]:
            if event_kind == "range_start":
                open_ranges[cid] = {"start": i, "chunks": []}
            elif event_kind == "range_end":
                state = open_ranges.pop(cid, None)
                if state is not None:
                    state["chunks"].append(p["text"])
                    finalize(cid, state["start"], state["chunks"], p["text"])
                else:
                    # range_end without matching start: still record at this para
                    if cid not in located:
                        finalize(cid, i, [], p["text"])
            elif event_kind == "ref":
                if cid not in located:
                    finalize(cid, i, [], p["text"])

        # If any range is open and this paragraph contributes text, accumulate
        for cid, state in open_ranges.items():
            if state["start"] != i and p["text"]:
                state["chunks"].append(p["text"])

    # Any still-open ranges
    for cid, state in open_ranges.items():
        if cid not in located:
            finalize(cid, state["start"], state["chunks"], "")

    return located


def normalize(text):
    """Lowercase + strip HTML + normalize unicode + collapse whitespace + drop
    most punctuation. For fuzzy matching DOCX <-> Drive comment text."""
    s = re.sub(r"<[^>]+>", "", text or "")
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def match_drive_to_docx(drive_comments, docx_comments):
    """Returns (drive_id -> docx_id, list of unmatched drive_ids)."""
    # Pre-index DOCX by normalized prefix
    by_prefix = {}
    for did, dc in docx_comments.items():
        key = normalize(dc["text"])[:60]
        by_prefix.setdefault(key, []).append(did)

    out = {}
    used = set()
    unmatched = []

    for c in drive_comments:
        norm = normalize(c.get("content", ""))[:60]
        candidates = by_prefix.get(norm, [])
        # Filter unused
        free = [d for d in candidates if d not in used]
        if free:
            out[c["id"]] = free[0]
            used.add(free[0])
            continue

        # Fuzzy fallback: find DOCX whose normalized content starts with the same first 30 chars
        norm30 = norm[:30]
        if norm30:
            for did, dc in docx_comments.items():
                if did in used:
                    continue
                if normalize(dc["text"]).startswith(norm30):
                    out[c["id"]] = did
                    used.add(did)
                    break
            if c["id"] in out:
                continue

        unmatched.append(c["id"])

    return out, unmatched


def render_md(drive_comments, docx_comments, drive_to_docx, located, doc_id):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    matched = sum(1 for c in drive_comments if c["id"] in drive_to_docx)
    with_loc = sum(
        1 for c in drive_comments
        if c["id"] in drive_to_docx and drive_to_docx[c["id"]] in located
    )
    resolved_n = sum(1 for c in drive_comments if c.get("resolved"))
    open_n = len(drive_comments) - resolved_n
    lines = [
        "# Thesis Comments Report",
        "",
        f"- **Doc ID:** `{doc_id}`",
        f"- **Pulled at (UTC):** {now}",
        f"- **Total comments:** {len(drive_comments)}  "
        f"(open: {open_n}, resolved: {resolved_n})",
        f"- **Located in a chapter:** {with_loc} / {len(drive_comments)}  "
        f"(unlocated are typically resolved comments — DOCX export drops their anchors)",
        "",
        "> Location info is derived by exporting the Google Doc as DOCX and reading"
        " the inline comment anchor markers. Each comment's containing chapter"
        " (and the nearest sub-heading) is shown alongside the actual paragraph"
        " text the advisor was looking at.",
        "",
        "---",
        "",
    ]
    for i, c in enumerate(drive_comments, 1):
        author = (c.get("author") or {}).get("displayName") or "unknown"
        email = (c.get("author") or {}).get("emailAddress") or ""
        created = c.get("createdTime", "")
        modified = c.get("modifiedTime", "")
        resolved = c.get("resolved", False)
        content = (c.get("content") or "").strip()
        replies = c.get("replies") or []
        cid = c.get("id", "")
        status = "RESOLVED" if resolved else "OPEN"

        header = f"## Comment #{i} — {author}"
        if email:
            header += f" ({email})"
        header += f" — {status}"
        lines.append(header)
        lines.append("")
        lines.append(f"- **Comment ID:** `{cid}`")
        lines.append(f"- **Created:** {created}")
        if modified and modified != created:
            lines.append(f"- **Modified:** {modified}")

        docx_id = drive_to_docx.get(cid)
        loc = located.get(docx_id) if docx_id is not None else None
        if loc:
            chapter_md = f"{loc['chapter_folder']}/{loc['chapter_folder']}.md"
            lines.append(f"- **Located in:** [{chapter_md}]({chapter_md}) — {loc['chapter_title']}")
            if loc.get("sub_title"):
                lines.append(f"- **Nearest sub-heading:** ({loc['sub_kind'].upper()}) {loc['sub_title']}")
        elif resolved:
            lines.append(
                "- **Located in:** _(resolved comment — Google Docs DOCX export"
                " strips inline anchors for resolved comments, so position is"
                " not recoverable. Locate manually if still relevant.)_"
            )
        else:
            lines.append(
                "- **Located in:** _(could not match — possibly an orphaned anchor"
                " or content was edited after the DOCX export was last refreshed)_"
            )
        lines.append("")

        if loc and loc["anchored_text"]:
            lines.append("**Anchored text (what the comment is pointing to):**")
            lines.append("")
            for qline in loc["anchored_text"].splitlines() or [""]:
                lines.append(f"> {qline}")
            lines.append("")
        elif loc and loc["paragraph_text"]:
            lines.append("**Paragraph at anchor (no text selection — comment was placed without selection):**")
            lines.append("")
            for qline in loc["paragraph_text"].splitlines() or [""]:
                lines.append(f"> {qline}")
            lines.append("")

        lines.append("**Comment:**")
        lines.append("")
        lines.append(content if content else "_(empty)_")
        lines.append("")

        if replies:
            lines.append(f"**Replies ({len(replies)}):**")
            lines.append("")
            for r in replies:
                r_author = (r.get("author") or {}).get("displayName") or "unknown"
                r_created = r.get("createdTime", "")
                r_content = (r.get("content") or "").strip() or "_(empty)_"
                lines.append(f"- **{r_author}** ({r_created}):")
                for rline in r_content.splitlines():
                    lines.append(f"  > {rline}")
            lines.append("")

        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--jsonl",
        default=None,
        help="Path to thesis-comments-raw.jsonl (default: <output-dir>/thesis-comments-raw.jsonl)",
    )
    parser.add_argument(
        "--debug-docx",
        default=None,
        help="Optional: dump the exported DOCX to this path for inspection",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    jsonl_path = Path(args.jsonl) if args.jsonl else (out_dir / "thesis-comments-raw.jsonl")
    if not jsonl_path.exists():
        print(f"ERROR: Drive comments JSONL not found at {jsonl_path}.\n"
              "Run scripts/gdoc-read-comments.py first.", file=sys.stderr)
        sys.exit(2)

    drive_comments = []
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                drive_comments.append(json.loads(line))
    print(f"Loaded {len(drive_comments)} Drive comments from {jsonl_path.name}")

    auth = load_auth()
    drive = auth.get_drive_service()

    print(f"Exporting doc {args.doc_id} as DOCX ...")
    docx_bytes = export_docx(drive, args.doc_id)
    print(f"  DOCX size: {len(docx_bytes):,} bytes")
    if args.debug_docx:
        Path(args.debug_docx).write_bytes(docx_bytes)
        print(f"  saved DOCX to {args.debug_docx}")

    docx_comments = parse_docx_comments(docx_bytes)
    print(f"  DOCX comments parsed: {len(docx_comments)}")

    paragraphs = parse_docx_body(docx_bytes)
    print(f"  DOCX paragraphs: {len(paragraphs)}")
    h1_index = build_h1_index(paragraphs)
    print(f"  H1 chapters in DOCX: {len(h1_index)}")

    located = locate_comments_in_body(paragraphs, h1_index)
    print(f"  comments with body anchor: {len(located)}")

    drive_to_docx, unmatched = match_drive_to_docx(drive_comments, docx_comments)
    print(f"  matched Drive->DOCX: {len(drive_to_docx)}, unmatched: {len(unmatched)}")
    if unmatched:
        for cid in unmatched:
            print(f"    UNMATCHED: {cid}", file=sys.stderr)

    md = render_md(drive_comments, docx_comments, drive_to_docx, located, args.doc_id)
    out_path = out_dir / "comments.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
