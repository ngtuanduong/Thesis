"""
gdoc-map-comments-to-chapters: map each comment's quoted text to its location in
the thesis chapter .md files.

Reads:   documents/thesis-chapters/review/thesis-comments-raw.jsonl
Scans:   documents/thesis-chapters/*.md  (excludes subdirs: processed/, visuals/, review/)
Writes:  documents/thesis-chapters/review/thesis-comments-mapping.md

Classification per comment:
    - UNIQUE:         quoted text found in exactly one chapter/line
    - MULTIPLE:       quoted text matches in 2+ places (needs manual disambiguation)
    - NOT_FOUND:      quoted text exists but no match (likely rewritten/humanized)
    - ANCHORLESS:     comment has no quoted text (image/table/unanchored)
    - TOO_SHORT:      quoted text < 10 chars; likely to false-match

Usage:
    python scripts/gdoc-map-comments-to-chapters.py
    python scripts/gdoc-map-comments-to-chapters.py --min-quote-len 15
"""
import argparse
import io
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CHAPTERS_DIR = PROJECT_ROOT / "documents" / "thesis-chapters"
REVIEW_DIR = CHAPTERS_DIR / "review"

EXCLUDE_SUBDIRS = {"processed", "visuals", "review"}

WS_RE = re.compile(r"\s+")


def normalize(text):
    """Collapse whitespace, NFKC-fold unicode, strip, lowercase for matching."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace(" ", " ")  # non-breaking space
    text = text.replace("​", "")   # zero-width space
    text = WS_RE.sub(" ", text).strip()
    return text.lower()


def load_chapter_files():
    """Return list of (path, lines, normalized_full_text, per_line_offsets)."""
    out = []
    for md in sorted(CHAPTERS_DIR.glob("*.md")):
        if md.parent != CHAPTERS_DIR:
            continue
        if md.parent.name in EXCLUDE_SUBDIRS:
            continue
        raw = md.read_text(encoding="utf-8")
        lines = raw.splitlines()
        # Build a single normalized blob AND track, for each char in the blob,
        # which line it came from (so we can report a line number per match).
        blob_parts = []
        char_to_line = []  # index into blob -> line number (1-based)
        for i, line in enumerate(lines, start=1):
            norm_line = normalize(line)
            if not norm_line:
                # still need a separator so words from adjacent lines don't fuse
                if blob_parts and not blob_parts[-1].endswith(" "):
                    blob_parts.append(" ")
                    char_to_line.append(i)
                continue
            if blob_parts and not blob_parts[-1].endswith(" "):
                blob_parts.append(" ")
                char_to_line.append(i)
            blob_parts.append(norm_line)
            char_to_line.extend([i] * len(norm_line))
        blob = "".join(blob_parts)
        out.append({
            "path": md,
            "lines": lines,
            "blob": blob,
            "char_to_line": char_to_line,
        })
    return out


def find_matches(needle, chapter):
    """Return list of line numbers in chapter where needle appears (normalized)."""
    blob = chapter["blob"]
    if not needle or not blob:
        return []
    hits = []
    start = 0
    while True:
        idx = blob.find(needle, start)
        if idx == -1:
            break
        # Map blob index -> line number
        if idx < len(chapter["char_to_line"]):
            line_no = chapter["char_to_line"][idx]
        else:
            line_no = len(chapter["lines"])
        hits.append(line_no)
        start = idx + max(1, len(needle))
    return hits


def context_line(chapter, line_no):
    if 1 <= line_no <= len(chapter["lines"]):
        return chapter["lines"][line_no - 1].strip()
    return ""


def shorten(text, n=120):
    text = text.replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jsonl",
        default=str(REVIEW_DIR / "thesis-comments-raw.jsonl"),
        help="Input JSONL file (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default=str(REVIEW_DIR / "thesis-comments-mapping.md"),
        help="Output mapping markdown (default: %(default)s)",
    )
    parser.add_argument(
        "--min-quote-len",
        type=int,
        default=10,
        help="Minimum normalized quote length for reliable matching (default: 10)",
    )
    args = parser.parse_args()

    jsonl_path = Path(args.jsonl)
    if not jsonl_path.exists():
        print(f"ERROR: {jsonl_path} not found. Run gdoc-read-comments.py first.", file=sys.stderr)
        sys.exit(1)

    comments = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            comments.append(json.loads(line))

    chapters = load_chapter_files()
    if not chapters:
        print(f"ERROR: no chapter .md files found under {CHAPTERS_DIR}", file=sys.stderr)
        sys.exit(1)

    # Bucket: chapter_path -> list of mapping entries
    by_chapter = {}
    unmapped = []   # NOT_FOUND
    anchorless = [] # no quoted text
    too_short = []  # quote < min-quote-len
    multiple = []   # matched in 2+ places

    for i, c in enumerate(comments, 1):
        author = (c.get("author") or {}).get("displayName") or "unknown"
        created = c.get("createdTime", "")
        content = (c.get("content") or "").strip()
        cid = c.get("id", "")
        quoted_raw = ((c.get("quotedFileContent") or {}).get("value") or "").strip()
        quoted_norm = normalize(quoted_raw)

        entry = {
            "idx": i,
            "id": cid,
            "author": author,
            "created": created,
            "content": content,
            "quoted_raw": quoted_raw,
            "quoted_norm": quoted_norm,
        }

        if not quoted_raw:
            anchorless.append(entry)
            continue

        if len(quoted_norm) < args.min_quote_len:
            too_short.append(entry)
            continue

        # Search every chapter for the normalized needle
        all_hits = []  # list of (chapter, line_no)
        for ch in chapters:
            for ln in find_matches(quoted_norm, ch):
                all_hits.append((ch, ln))

        if not all_hits:
            unmapped.append(entry)
            continue

        if len(all_hits) == 1:
            ch, ln = all_hits[0]
            by_chapter.setdefault(ch["path"], []).append({
                **entry,
                "line": ln,
                "context": context_line(ch, ln),
                "kind": "UNIQUE",
            })
        else:
            multiple.append({**entry, "hits": all_hits})

    # Render
    lines = []
    lines.append("# Comment → Chapter Mapping")
    lines.append("")
    lines.append(f"- **Total comments processed:** {len(comments)}")
    lines.append(f"- **Unique matches:** {sum(len(v) for v in by_chapter.values())}")
    lines.append(f"- **Multiple matches:** {len(multiple)}")
    lines.append(f"- **Not found:** {len(unmapped)}")
    lines.append(f"- **Anchorless (image/table):** {len(anchorless)}")
    lines.append(f"- **Too-short quote (<{args.min_quote_len} chars):** {len(too_short)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for chapter_path in sorted(by_chapter.keys()):
        rel = chapter_path.relative_to(PROJECT_ROOT)
        entries = sorted(by_chapter[chapter_path], key=lambda e: e["line"])
        lines.append(f"## {rel.as_posix()}  ({len(entries)} comment{'s' if len(entries) != 1 else ''})")
        lines.append("")
        for e in entries:
            lines.append(f"### Comment #{e['idx']} — {e['author']} — {e['created']}")
            lines.append(f"- **Match:** line {e['line']} (unique)")
            lines.append(f"- **Quoted:** {shorten(e['quoted_raw'], 160)}")
            if e["context"]:
                lines.append(f"- **Context:** `{shorten(e['context'], 160)}`")
            lines.append(f"- **Comment:** {shorten(e['content'], 400)}")
            lines.append(f"- **Comment ID:** `{e['id']}`")
            lines.append("")
        lines.append("")

    if multiple:
        lines.append("## MULTIPLE MATCHES (manual disambiguation needed)")
        lines.append("")
        for e in multiple:
            lines.append(f"### Comment #{e['idx']} — {e['author']} — {e['created']}")
            lines.append(f"- **Quoted:** {shorten(e['quoted_raw'], 160)}")
            lines.append(f"- **Comment:** {shorten(e['content'], 400)}")
            lines.append(f"- **Hits ({len(e['hits'])}):**")
            for ch, ln in e["hits"]:
                rel = ch["path"].relative_to(PROJECT_ROOT)
                ctx = shorten(context_line(ch, ln), 120)
                lines.append(f"  - `{rel.as_posix()}:{ln}` — {ctx}")
            lines.append("")
        lines.append("")

    if unmapped:
        lines.append(f"## NOT FOUND ({len(unmapped)})")
        lines.append("")
        lines.append("Possible reasons: chapter was rewritten/humanized after the comment was made, "
                     "or the quoted text contains characters that differ after normalization.")
        lines.append("")
        for e in unmapped:
            lines.append(f"### Comment #{e['idx']} — {e['author']} — {e['created']}")
            lines.append(f"- **Quoted:** {shorten(e['quoted_raw'], 160)}")
            lines.append(f"- **Comment:** {shorten(e['content'], 400)}")
            lines.append(f"- **Comment ID:** `{e['id']}`")
            lines.append("")
        lines.append("")

    if too_short:
        lines.append(f"## TOO-SHORT QUOTE ({len(too_short)})")
        lines.append("")
        lines.append(f"Quoted text is shorter than {args.min_quote_len} chars — auto-match skipped "
                     "to avoid false positives. Please review manually.")
        lines.append("")
        for e in too_short:
            lines.append(f"### Comment #{e['idx']} — {e['author']} — {e['created']}")
            lines.append(f"- **Quoted:** {shorten(e['quoted_raw'], 160)}")
            lines.append(f"- **Comment:** {shorten(e['content'], 400)}")
            lines.append("")
        lines.append("")

    if anchorless:
        lines.append(f"## ANCHORLESS ({len(anchorless)})")
        lines.append("")
        lines.append("Comments with no quoted text — likely attached to an image, table, "
                     "or placed without a selection. Check the GDoc directly.")
        lines.append("")
        for e in anchorless:
            lines.append(f"### Comment #{e['idx']} — {e['author']} — {e['created']}")
            lines.append(f"- **Comment:** {shorten(e['content'], 400)}")
            lines.append(f"- **Comment ID:** `{e['id']}`")
            lines.append("")
        lines.append("")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    mapped = sum(len(v) for v in by_chapter.values())
    print(f"Processed {len(comments)} comments")
    print(f"  Unique matches:   {mapped}")
    print(f"  Multiple matches: {len(multiple)}")
    print(f"  Not found:        {len(unmapped)}")
    print(f"  Anchorless:       {len(anchorless)}")
    print(f"  Too short:        {len(too_short)}")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
