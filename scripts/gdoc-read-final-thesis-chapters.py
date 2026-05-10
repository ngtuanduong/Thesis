"""
gdoc-read-final-thesis-chapters: pull the final thesis Google Doc, split it into
one folder per Heading 1, and download all inline images locally.

Output layout (per H1 section):
    documents/final-thesis-chapters/
        _index.md                                  (manifest)
        00-front-matter/
            00-front-matter.md
            image/image-1.png, image-2.png, ...
        08-chapter-1-introduction/
            08-chapter-1-introduction.md
            image/...
        ...

Markdown image refs are rewritten to `![](image/image-N.png)` so each chapter
folder is fully self-contained.

Usage:
    python scripts/gdoc-read-final-thesis-chapters.py
    python scripts/gdoc-read-final-thesis-chapters.py --doc-id <FILE_ID>
    python scripts/gdoc-read-final-thesis-chapters.py --output-dir <PATH>
    python scripts/gdoc-read-final-thesis-chapters.py --no-images
    python scripts/gdoc-read-final-thesis-chapters.py --dry-run

Prerequisite: doc must be shared with the service account
(service-account@infra-inkwell-465003-f2.iam.gserviceaccount.com) as Viewer.
"""
import argparse
import importlib.util
import io
import re
import sys
import unicodedata
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "documents" / "final-thesis-chapters"
DEFAULT_DOC_ID = "1B72mF57eyHFaCgTI-zVvZ01RWOuJInFemI-dVl_qxvA"
PLACEHOLDER_RE = re.compile(r"!\[image\]\(inline-object-([^)]+)\)")

HEADING_PREFIX = {
    "TITLE": "# ",
    "SUBTITLE": "## ",
    "HEADING_1": "# ",
    "HEADING_2": "## ",
    "HEADING_3": "### ",
    "HEADING_4": "#### ",
    "HEADING_5": "##### ",
    "HEADING_6": "###### ",
}


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def slugify(text, max_len=50):
    """ASCII slug from Vietnamese text. Strips diacritics, lowercases, dashes."""
    if not text:
        return "untitled"
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in nfkd if not unicodedata.combining(c))
    ascii_only = ascii_only.replace("đ", "d").replace("Đ", "D")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_only).strip("-").lower()
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "untitled"


def render_text_run(text_run):
    """Apply textStyle (bold/italic) to the run's content. Underline -> plain."""
    content = text_run.get("content", "")
    if not content:
        return ""
    style = text_run.get("textStyle", {}) or {}
    has_link = bool((style.get("link") or {}).get("url"))
    bold = style.get("bold")
    italic = style.get("italic")

    stripped = content.rstrip("\n\r\t ")
    trailing = content[len(stripped):]
    if not stripped:
        return content

    rendered = stripped.replace("\\", "\\\\")
    if bold and italic:
        rendered = f"***{rendered}***"
    elif bold:
        rendered = f"**{rendered}**"
    elif italic:
        rendered = f"*{rendered}*"

    if has_link:
        url = style["link"]["url"]
        rendered = f"[{rendered}]({url})"

    return rendered + trailing


def render_paragraph(paragraph, lists, counters, stats):
    """Return markdown string for a paragraph (one logical line)."""
    style = paragraph.get("paragraphStyle", {}) or {}
    named = style.get("namedStyleType", "NORMAL_TEXT")
    prefix = HEADING_PREFIX.get(named, "")

    parts = []
    for el in paragraph.get("elements", []):
        if "textRun" in el:
            parts.append(render_text_run(el["textRun"]))
        elif "inlineObjectElement" in el:
            obj_id = el["inlineObjectElement"].get("inlineObjectId", "?")
            parts.append(f"![image](inline-object-{obj_id})")
            stats["images"] += 1
        elif "footnoteReference" in el:
            ref_id = el["footnoteReference"].get("footnoteId", "?")
            parts.append(f"[^{ref_id}]")
        elif "horizontalRule" in el:
            parts.append("\n---\n")
        elif "equation" in el:
            parts.append("<!-- unsupported: equation -->")
        elif "autoText" in el:
            parts.append("<!-- unsupported: autoText -->")
        elif "pageBreak" in el:
            parts.append("\n\n<!-- page break -->\n")
        elif "columnBreak" in el:
            parts.append("\n\n<!-- column break -->\n")
        elif "richLink" in el:
            rich = el["richLink"].get("richLinkProperties", {})
            title = rich.get("title", "link")
            url = rich.get("uri", "")
            parts.append(f"[{title}]({url})")
        else:
            kind = next(iter(el.keys() - {"startIndex", "endIndex"}), "?")
            parts.append(f"<!-- unsupported: {kind} -->")

    text = "".join(parts).rstrip("\n")

    bullet = paragraph.get("bullet")
    if bullet:
        list_id = bullet.get("listId")
        nesting = bullet.get("nestingLevel", 0)
        glyph = "-"
        if list_id and lists:
            list_props = (lists.get(list_id) or {}).get("listProperties", {}) or {}
            nesting_levels = list_props.get("nestingLevels") or []
            if nesting < len(nesting_levels):
                glyph_type = nesting_levels[nesting].get("glyphType", "")
                if glyph_type and glyph_type != "GLYPH_TYPE_UNSPECIFIED":
                    key = (list_id, nesting)
                    counters[key] = counters.get(key, 0) + 1
                    glyph = f"{counters[key]}."
        indent = "    " * nesting
        return f"{indent}{glyph} {text}".rstrip()

    if prefix:
        return f"{prefix}{text.strip()}"
    return text


def is_h1(paragraph):
    style = paragraph.get("paragraphStyle", {}) or {}
    return style.get("namedStyleType") == "HEADING_1"


def heading_text(paragraph):
    parts = []
    for el in paragraph.get("elements", []):
        if "textRun" in el:
            parts.append(el["textRun"].get("content", ""))
    return "".join(parts).strip()


def cell_text(cell, lists, counters, stats):
    """Render a single table cell as a single-line markdown string (pipes escaped)."""
    parts = []
    for elem in cell.get("content", []):
        if "paragraph" in elem:
            md = render_paragraph(elem["paragraph"], lists, counters, stats)
            if md.strip():
                parts.append(md.strip())
        elif "table" in elem:
            parts.append("<nested-table>")
    text = " ".join(parts)
    return text.replace("|", "\\|").replace("\n", " ")


def render_table(table, lists, counters, stats):
    """Render a Google Docs table as markdown. 1x1 tables become their inline content
    (Google Docs often wraps single images/blocks in a 1x1 table for layout)."""
    rows = table.get("tableRows", []) or []
    if not rows:
        return ""
    n_rows = len(rows)
    n_cols = max((len(r.get("tableCells", []) or []) for r in rows), default=0)

    if n_rows == 1 and n_cols == 1:
        cell = rows[0]["tableCells"][0]
        out = []
        for elem in cell.get("content", []):
            if "paragraph" in elem:
                md = render_paragraph(elem["paragraph"], lists, counters, stats)
                out.append(md)
        return "\n\n".join(s for s in out if s is not None)

    grid = []
    for r in rows:
        row_cells = []
        for c in (r.get("tableCells", []) or []):
            row_cells.append(cell_text(c, lists, counters, stats))
        while len(row_cells) < n_cols:
            row_cells.append("")
        grid.append(row_cells)

    lines = []
    header = grid[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * n_cols) + " |")
    for row in grid[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def walk_doc(doc, stats):
    """Yield ('h1', title, paragraph_md, start_index) or ('para', md, start_index)
    or ('table', md, start_index) in document order."""
    lists = doc.get("lists", {}) or {}
    counters = {}
    for elem in doc["body"]["content"]:
        s = elem.get("startIndex", 0)
        if "paragraph" in elem:
            p = elem["paragraph"]
            md = render_paragraph(p, lists, counters, stats)
            if is_h1(p):
                yield ("h1", heading_text(p), md, s)
            else:
                yield ("para", md, s)
        elif "table" in elem:
            t = elem["table"]
            rows = t.get("rows", 0) or len(t.get("tableRows", []) or [])
            cols = t.get("columns", 0)
            stats["tables"] += 1
            md = render_table(t, lists, counters, stats)
            if rows > 1 or cols > 1:
                print(
                    f"INFO: rendered {rows}x{cols} table at index {s} as markdown table",
                    file=sys.stderr,
                )
            yield ("table", md, s)
        elif "sectionBreak" in elem:
            yield ("para", "<!-- section break -->", s)
        elif "tableOfContents" in elem:
            yield ("para", "<!-- table of contents -->", s)


def collect_chapters(events):
    """Group flat events into front-matter + chapters keyed by H1 order."""
    front_lines = []
    chapters = []
    current = None
    first_index = {}

    for event in events:
        kind = event[0]
        if kind == "h1":
            _, title, md, idx = event
            if current is not None:
                chapters.append(current)
            current = {
                "title": title,
                "lines": [md],
                "start_index": idx,
                "end_index": idx,
            }
            first_index.setdefault("h1_count", 0)
            first_index["h1_count"] += 1
        else:
            md = event[1]
            idx = event[-1]
            if current is None:
                front_lines.append(md)
            else:
                current["lines"].append(md)
                current["end_index"] = idx
    if current is not None:
        chapters.append(current)
    return front_lines, chapters


def join_lines(lines):
    """Join lines with proper paragraph spacing (blank line between non-empty lines)."""
    # Drop runs of empty lines down to a single blank
    out = []
    prev_blank = True
    for ln in lines:
        ln = ln.rstrip()
        if ln == "":
            if not prev_blank:
                out.append("")
                prev_blank = True
            continue
        out.append(ln)
        out.append("")
        prev_blank = True
    text = "\n".join(out).strip() + "\n"
    return text


EXT_FROM_CT = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/gif": "gif",
    "image/webp": "webp",
    "image/svg+xml": "svg",
    "image/bmp": "bmp",
    "image/tiff": "tiff",
}


CAPTION_RE = re.compile(
    r"^[\s\*_]*(Figure|Table|Hình|Bảng)\s*(\d+(?:[.\-]\d+)?)\s*[\.\:]?\s*(.+?)[\s\*_\.]*$",
    re.IGNORECASE,
)


def detect_caption(lines, image_line_idx):
    """Look for a 'Figure 1.3. ...' caption near the image. Check the first
    non-blank line AFTER the image first (most common position), then the
    first non-blank line BEFORE. Returns (kind, number, title) or (None,)*3."""
    def search(idx_range):
        for j in idx_range:
            line = lines[j].strip()
            if not line:
                continue
            # Only inspect the first non-blank line; if it's not a caption, give up
            m = CAPTION_RE.match(line)
            if m:
                kind = m.group(1).lower()
                kind = {"hình": "figure", "bảng": "table"}.get(kind, kind)
                return kind, m.group(2).replace(".", "-"), m.group(3).strip()
            return None, None, None
        return None, None, None

    after = search(range(image_line_idx + 1, min(image_line_idx + 4, len(lines))))
    if after[0]:
        return after
    return search(range(image_line_idx - 1, max(image_line_idx - 4, -1), -1))


HEADING_LINE_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SECTION_NUM_RE = re.compile(r"^(\d+(?:\.\d+){1,3})\.?\s*(.*)$")


def alt_text_for(oid, inline_objects):
    obj = inline_objects.get(oid) or {}
    embedded = (obj.get("inlineObjectProperties") or {}).get("embeddedObject") or {}
    return (embedded.get("title") or embedded.get("description") or "").strip()


def find_nearest_heading(lines, image_line_idx, prefer_levels=(4, 3, 2, 1)):
    """Walk backwards to find the nearest markdown heading. Returns the
    heading text (without #s)."""
    for j in range(image_line_idx - 1, -1, -1):
        m = HEADING_LINE_RE.match(lines[j].strip())
        if m and len(m.group(1)) in prefer_levels:
            return m.group(2).strip()
    return None


def looks_like_equation(lines, image_line_idx):
    """Heuristic: does the line before the image end with ':' (introducing a
    formula) or contain math-y markers ('Here,', 'where', 'Equation', 'computed',
    LaTeX-style backslashes)?"""
    for j in range(image_line_idx - 1, -1, -1):
        line = lines[j].strip()
        if not line:
            continue
        if line.endswith(":"):
            return True
        lower = line.lower()
        if any(k in lower for k in ("equation ", "formula", "where ", "here,", "compute")):
            return True
        return False
    return False


def section_slug_from_heading(heading, max_len=40):
    """Convert '3.3.2. Elo Rating Layer Continuous Difficulty Calibration' to
    a short slug like 'sec-3-3-2-elo-rating-layer'."""
    m = SECTION_NUM_RE.match(heading)
    if m:
        num = m.group(1).replace(".", "-")
        rest = m.group(2)
        rest_slug = slugify(rest, max_len=max_len - len(num) - 5)
        if rest_slug and rest_slug != "untitled":
            return f"sec-{num}-{rest_slug}"
        return f"sec-{num}"
    return slugify(heading, max_len=max_len)


def make_image_filename(
    kind, number, title, alt, fallback_idx, ext, used_names,
    lines, line_idx, section_counters,
):
    """Build a stable filename. Priority:
        1. Figure/Table caption
        2. Alt text
        3. Nearest sub-heading slug + per-section counter (eq- prefix if
           the surrounding text looks like an inline equation)
        4. image-NN fallback
    """
    if kind and title:
        base = f"{kind}-{number}-{slugify(title, max_len=60)}"
    elif alt:
        base = f"image-{fallback_idx:02d}-{slugify(alt, max_len=60)}"
    else:
        heading = find_nearest_heading(lines, line_idx)
        if heading:
            section = section_slug_from_heading(heading)
            section_counters[section] = section_counters.get(section, 0) + 1
            n = section_counters[section]
            prefix = "eq" if looks_like_equation(lines, line_idx) else "img"
            base = f"{section}-{prefix}-{n}"
        else:
            base = f"image-{fallback_idx:02d}"

    fname = f"{base}.{ext}"
    if fname in used_names:
        suffix = 2
        while f"{base}-{suffix}.{ext}" in used_names:
            suffix += 1
        fname = f"{base}-{suffix}.{ext}"
    used_names.add(fname)
    return fname


def download_chapter_images(body_md, image_dir, inline_objects, session, dry_run):
    """Find image placeholders, generate caption-based filenames, download, and
    return rewritten markdown."""
    lines = body_md.split("\n")

    # Walk lines in order, build [(line_idx, oid), ...] preserving order of FIRST appearance
    seen_set = set()
    refs = []
    for i, line in enumerate(lines):
        for m in PLACEHOLDER_RE.finditer(line):
            oid = m.group(1)
            if oid not in seen_set:
                refs.append((i, oid))
                seen_set.add(oid)

    if not refs:
        return body_md, 0, 0

    obj_to_filename = {}
    used_names = set()
    section_counters = {}
    downloaded = 0
    failed = 0

    if not dry_run:
        image_dir.mkdir(parents=True, exist_ok=True)

    for i, (line_idx, oid) in enumerate(refs, 1):
        kind, number, title = detect_caption(lines, line_idx)
        alt = alt_text_for(oid, inline_objects)

        obj = inline_objects.get(oid) or {}
        embedded = (obj.get("inlineObjectProperties") or {}).get("embeddedObject") or {}
        img_props = embedded.get("imageProperties") or {}
        content_uri = img_props.get("contentUri")

        if dry_run or session is None:
            ext = "png"
            fname = make_image_filename(
                kind, number, title, alt, i, ext, used_names,
                lines, line_idx, section_counters,
            )
            if image_dir.exists():
                base = fname.rsplit(".", 1)[0]
                existing = list(image_dir.glob(f"{base}.*"))
                if existing:
                    used_names.discard(fname)
                    fname = existing[0].name
                    used_names.add(fname)
            obj_to_filename[oid] = fname
            continue

        if not content_uri:
            ext = "png"
            fname = make_image_filename(
                kind, number, title, alt, i, ext, used_names,
                lines, line_idx, section_counters,
            )
            obj_to_filename[oid] = fname.replace(f".{ext}", ".MISSING")
            failed += 1
            print(f"    WARN: no contentUri for {oid}", file=sys.stderr)
            continue

        try:
            r = session.get(content_uri)
            r.raise_for_status()
            ct = (r.headers.get("content-type") or "").split(";")[0].strip().lower()
            ext = EXT_FROM_CT.get(ct, "png")
            fname = make_image_filename(
                kind, number, title, alt, i, ext, used_names,
                lines, line_idx, section_counters,
            )
            (image_dir / fname).write_bytes(r.content)
            obj_to_filename[oid] = fname
            downloaded += 1
        except Exception as e:
            ext = "png"
            fname = make_image_filename(
                kind, number, title, alt, i, ext, used_names,
                lines, line_idx, section_counters,
            )
            obj_to_filename[oid] = fname.replace(f".{ext}", ".MISSING")
            failed += 1
            print(f"    WARN: failed to download {oid}: {e}", file=sys.stderr)

    def repl(m):
        oid = m.group(1)
        fname = obj_to_filename.get(oid, f"unknown-{oid}")
        return f"![](image/{fname})"

    return PLACEHOLDER_RE.sub(repl, body_md), downloaded, failed


def write_chapter_folder(out_dir, basename, lines, inline_objects, session, dry_run):
    """Create <out_dir>/<basename>/<basename>.md plus image/ subfolder."""
    folder = out_dir / basename
    md_path = folder / f"{basename}.md"
    body = join_lines(lines)
    body, n_dl, n_fail = download_chapter_images(
        body, folder / "image", inline_objects, session, dry_run
    )
    if dry_run:
        print(f"  [dry-run] would write {md_path}  ({len(lines)} lines, "
              f"{n_dl + n_fail} image refs)")
    else:
        folder.mkdir(parents=True, exist_ok=True)
        md_path.write_text(body, encoding="utf-8")
        img_summary = f", {n_dl} images" if n_dl else ""
        if n_fail:
            img_summary += f", {n_fail} failed"
        print(f"  wrote {basename}/  ({len(lines)} lines{img_summary})")
    return md_path.relative_to(out_dir).as_posix()


def write_chapter(out_dir, idx, chapter, inline_objects, session, dry_run):
    title = chapter["title"] or ""
    slug = slugify(title)
    if not title.strip() or slug == "untitled":
        slug = "untitled-section"
    basename = f"{idx:02d}-{slug}"
    return write_chapter_folder(
        out_dir, basename, chapter["lines"], inline_objects, session, dry_run
    )


def write_front_matter(out_dir, lines, inline_objects, session, dry_run):
    if not any(ln.strip() for ln in lines):
        return None
    return write_chapter_folder(
        out_dir, "00-front-matter", lines, inline_objects, session, dry_run
    )


def write_index(out_dir, manifest, doc_id, stats, dry_run):
    lines = [
        "# Chapter Index",
        "",
        f"- **Source doc:** `{doc_id}`",
        f"- **H1 chapters extracted:** {len([m for m in manifest if m['kind'] == 'chapter'])}",
        f"- **Inline images:** {stats['images']}  (downloaded into each chapter's `image/` subfolder)",
        f"- **Tables rendered:** {stats['tables']}  (1x1 tables flattened, multi-cell tables as markdown tables)",
        "",
        "| File | H1 title | Doc index range |",
        "| --- | --- | --- |",
    ]
    for m in manifest:
        title = (m["title"] or "").replace("|", "\\|")
        # m["file"] is e.g. "08-chapter-1-introduction/08-chapter-1-introduction.md"
        rel = m["file"]
        lines.append(
            f"| [{rel}]({rel}) | {title} | "
            f"{m.get('start_index', '-')} – {m.get('end_index', '-')} |"
        )
    body = "\n".join(lines) + "\n"
    if dry_run:
        print(f"  [dry-run] would write {out_dir / '_index.md'}")
    else:
        (out_dir / "_index.md").write_text(body, encoding="utf-8")
        print(f"  wrote _index.md")


def make_authorized_session(auth_module):
    creds = service_account.Credentials.from_service_account_file(
        auth_module.KEY_FILE, scopes=auth_module.SCOPES
    )
    return AuthorizedSession(creds)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="Skip image download — placeholders left as ![](image/image-N.png) but no bytes fetched",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    auth = load_auth()
    print(f"Fetching doc {args.doc_id} ...")
    doc = auth.get_document(doc_id=args.doc_id)
    title = doc.get("title", "(untitled)")
    print(f"  title: {title}")

    inline_objects = doc.get("inlineObjects", {}) or {}
    session = None
    if not args.no_images and not args.dry_run:
        session = make_authorized_session(auth)

    stats = {"images": 0, "tables": 0}
    events = list(walk_doc(doc, stats))
    front_lines, chapters = collect_chapters(events)
    print(f"  found {len(chapters)} H1 chapters, "
          f"{stats['images']} inline images, {stats['tables']} tables, "
          f"{len(inline_objects)} unique inline objects in doc")

    manifest = []

    front_file = write_front_matter(out_dir, front_lines, inline_objects, session, args.dry_run)
    if front_file:
        manifest.append({
            "kind": "front",
            "file": front_file,
            "title": "(front matter — before first H1)",
            "start_index": 0,
            "end_index": chapters[0]["start_index"] - 1 if chapters else "-",
        })

    for i, ch in enumerate(chapters, 1):
        fname = write_chapter(out_dir, i, ch, inline_objects, session, args.dry_run)
        manifest.append({
            "kind": "chapter",
            "file": fname,
            "title": ch["title"],
            "start_index": ch["start_index"],
            "end_index": ch["end_index"],
        })

    write_index(out_dir, manifest, args.doc_id, stats, args.dry_run)

    print("done.")


if __name__ == "__main__":
    main()
