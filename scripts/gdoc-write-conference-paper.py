"""
gdoc-write-conference-paper: publish the assembled conference paper to a Google Doc
with HTKH GV-SV 2025 formatting rules.

Source:     documents/conference-paper/paper-final.md
Target doc: env GDOC_CONF_DOC_ID (default: 1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs)

Usage:
    python scripts/gdoc-write-conference-paper.py
    python scripts/gdoc-write-conference-paper.py --doc-id <ID>
    python scripts/gdoc-write-conference-paper.py --dry-run   # parse + print plan, no API calls

Formatting (from Thể Lệ HTKH GV-SV 2025):
    Page:   A4 (210 × 297 mm); margins top 2.5cm, bottom 2.5cm, left 3cm, right 3cm.
    Body:   Times New Roman 13pt; first line indent 0.85cm; space before 6pt, after 0pt;
            line spacing approx "Exactly 17pt" (approximated as 131% at 13pt).
    Title:  Tahoma 15pt, bold, center.
    Authors: Arial 10pt, bold + italic, center.
    Abstract: Arial 10pt, italic.
    Captions: Arial 10pt, italic, center.

The "Exactly 17pt" line-spacing requirement is approximated because the Docs API exposes
line spacing as a percentage of font size; a manual 10-second fix in the Docs UI
(Format → Line & paragraph spacing → Custom spacing → Exactly 17pt) is recommended if
the reviewer flags it.
"""
import argparse
import importlib.util
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_SOURCE = PROJECT_ROOT / "documents" / "conference-paper" / "paper-final.md"
DEFAULT_DOC_ID = "1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs"

# Catbox URLs from VISUAL-GUIDE.md (inventory step).
FIGURE_URLS = {
    "1": "https://lh3.googleusercontent.com/d/12WThyTAlnGaMIBYRjyxK_QPOgaqQfhSh",  # Platform Architecture (enlarged fonts + 2x capture)
    "2": "https://lh3.googleusercontent.com/d/1yMY_mLMrLnGoz87rFDU0Am30bR2ZjfZ_",  # Experiment Timeline (1572×595, enlarged fonts + 2x capture)
    "3": "https://files.catbox.moe/vq16l2.png",   # Submission Pipeline
}
TABLE_URLS = {
    # Table 1 (Technique Complementarity) tight-cropped 810×284 — hosted on user's personal
    # Google Drive (catbox had a CDN propagation bug for fresh uploads on 2026-04-22).
    # lh3.googleusercontent.com/d/<FILE_ID> is the canonical direct-image URL for Drive files
    # shared "Anyone with link".
    "1": "https://lh3.googleusercontent.com/d/1FCdCor_aHfZYl-bAQgr8dppMy4kzH9Qi",
}

# Page/style constants
PT_PER_CM = 28.3464566929

def cm_to_pt(cm):
    return round(cm * PT_PER_CM, 2)

MARGIN_TOP = cm_to_pt(2.5)
MARGIN_BOTTOM = cm_to_pt(2.5)
MARGIN_LEFT = cm_to_pt(3.0)
MARGIN_RIGHT = cm_to_pt(3.0)
PAGE_W = cm_to_pt(21.0)
PAGE_H = cm_to_pt(29.7)

FIRST_LINE_INDENT = cm_to_pt(0.85)
BODY_FONT = "Times New Roman"
BODY_SIZE = 13
TITLE_FONT = "Tahoma"
TITLE_SIZE = 15
AUTHOR_FONT = "Arial"
AUTHOR_SIZE = 10
ABSTRACT_FONT = "Arial"
ABSTRACT_SIZE = 10
CAPTION_FONT = "Arial"
CAPTION_SIZE = 10
LINE_SPACING_PCT = 131  # approximates Exactly 17pt at 13pt body

# Image display size — use near-full content width (15cm = 21cm page - 3cm×2 margins)
FIGURE_WIDTH_PT = cm_to_pt(15.0)
TABLE_WIDTH_PT = cm_to_pt(15.0)


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ───────────────────────────── Block model ─────────────────────────────

class Block:
    """A content block with text + role label. Role determines styling."""
    __slots__ = ("role", "text", "start", "end", "meta")

    def __init__(self, role, text, meta=None):
        self.role = role        # e.g. "title_vi", "authors", "abstract_vi", "body", "h1", "caption", "figure_marker"
        self.text = text        # text content (no trailing newline; newline appended on insertion)
        self.start = None       # start index (inclusive) after insertion
        self.end = None         # end index (exclusive) after insertion
        self.meta = meta or {}

    def __repr__(self):
        return f"Block({self.role!r}, {self.text[:40]!r}...)"


def extract_tagged(text, tag):
    m = re.search(rf"<!-- {tag}_BEGIN -->(.*?)<!-- {tag}_END -->", text, re.S)
    return m.group(1).strip() if m else ""


def strip_md_bold_labels(text):
    """Remove leading **Label:** markdown in abstract/keywords text."""
    return re.sub(r"^\*\*([^*]+?)\*\*:\s*", r"\1: ", text).strip()


def parse_paper(md_text):
    """Parse the assembled paper-final.md into an ordered list of Blocks."""
    blocks = []

    # Front matter
    title_vi = extract_tagged(md_text, "TITLE_VI")
    title_en = extract_tagged(md_text, "TITLE_EN")
    authors = extract_tagged(md_text, "AUTHORS")
    abs_vi = strip_md_bold_labels(extract_tagged(md_text, "ABSTRACT_VI"))
    abs_en = strip_md_bold_labels(extract_tagged(md_text, "ABSTRACT_EN"))
    kw_vi = strip_md_bold_labels(extract_tagged(md_text, "KEYWORDS_VI"))
    kw_en = strip_md_bold_labels(extract_tagged(md_text, "KEYWORDS_EN"))

    blocks.append(Block("title_vi", title_vi))
    blocks.append(Block("title_en", title_en))
    # author block is multi-line; split so lines remain distinct paragraphs.
    for line in authors.splitlines():
        line = line.strip()
        if line:
            blocks.append(Block("authors", line))
    blocks.append(Block("abstract_vi", abs_vi))
    blocks.append(Block("keywords_vi", kw_vi))
    blocks.append(Block("abstract_en", abs_en))
    blocks.append(Block("keywords_en", kw_en))

    # Body sections 1..5 and References
    # Everything after the last KEYWORDS_EN_END is body + refs
    after_front = md_text.split("<!-- KEYWORDS_EN_END -->", 1)[-1]

    # Walk line by line, classifying
    lines = after_front.splitlines()
    pending_para = []  # lines being accumulated for a body paragraph

    def flush_para():
        if pending_para:
            text = " ".join(s.strip() for s in pending_para).strip()
            if text:
                blocks.append(Block("body", text))
            pending_para.clear()

    for raw in lines:
        ln = raw.rstrip()
        if not ln.strip():
            flush_para()
            continue
        # Figure / Table placeholders + their captions are on the same line.
        m_fig = re.match(r"\[FIGURE_(\d+)_HERE\]\s*\*?([^*]*)\*?\s*$", ln)
        if m_fig:
            flush_para()
            blocks.append(Block("figure_marker", "", meta={"num": m_fig.group(1), "kind": "figure"}))
            cap = m_fig.group(2).strip()
            if cap:
                blocks.append(Block("caption", cap))
            continue
        m_tbl = re.match(r"\[TABLE_(\d+)_HERE\]\s*\*?([^*]*)\*?\s*$", ln)
        if m_tbl:
            flush_para()
            blocks.append(Block("figure_marker", "", meta={"num": m_tbl.group(1), "kind": "table"}))
            cap = m_tbl.group(2).strip()
            if cap:
                blocks.append(Block("caption", cap))
            continue
        # Headings
        m_h1 = re.match(r"^#\s+(.+)$", ln)
        if m_h1:
            flush_para()
            heading_text = m_h1.group(1).strip()
            role = "refs_heading" if heading_text.lower() == "references" else "h1"
            blocks.append(Block(role, heading_text))
            continue
        m_h2 = re.match(r"^##\s+(.+)$", ln)
        if m_h2:
            flush_para()
            blocks.append(Block("h2", m_h2.group(1).strip()))
            continue
        # Numbered reference list (only inside References section)
        m_ref = re.match(r"^\d+\.\s+(.+)$", ln)
        if m_ref and blocks and any(b.role == "refs_heading" for b in blocks):
            flush_para()
            blocks.append(Block("reference", m_ref.group(0).strip()))
            continue
        # Default: accumulate into current paragraph
        # Preserve markdown bold (**...**) as plain text here; stripped on insertion.
        pending_para.append(ln)

    flush_para()
    return blocks


# ───────────────────────────── Insertion ─────────────────────────────

def strip_markdown_inline(s):
    """Strip markdown bold/italic markers for insertion as plain text. Inline markers
    (**...**, *...*) are removed entirely; styling is applied via runtime style rules."""
    s = re.sub(r"\*\*([^*]+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\1", s)
    return s


def build_insertions(blocks):
    """Compute insertText requests AND record [start, end) for each block.

    The doc starts empty so we begin at index 1 (GDocs reserves index 0).
    Each paragraph is terminated by "\n" — the trailing "\n" counts in the range.
    """
    requests = []
    cursor = 1
    for b in blocks:
        if b.role == "figure_marker":
            # Placeholder text that we'll later replace with insertInlineImage.
            # Using a unique token so we can find & replace precisely.
            token = f"⁣[[{b.meta['kind'].upper()}_{b.meta['num']}_IMG]]⁣"
            payload = token + "\n"
            b.start = cursor
            b.end = cursor + len(payload)
            b.meta["token"] = token
            requests.append({"insertText": {"location": {"index": cursor}, "text": payload}})
            cursor = b.end
            continue
        text = strip_markdown_inline(b.text)
        payload = text + "\n"
        b.start = cursor
        b.end = cursor + len(payload)
        requests.append({"insertText": {"location": {"index": cursor}, "text": payload}})
        cursor = b.end
    return requests, cursor


# ───────────────────────────── Styling ─────────────────────────────

def style_requests_for(blocks):
    """For each block, emit updateTextStyle + updateParagraphStyle requests based on role."""
    reqs = []
    for b in blocks:
        if b.start is None:
            continue
        rng = {"startIndex": b.start, "endIndex": b.end}

        if b.role == "title_vi" or b.role == "title_en":
            reqs.append(text_style(rng, TITLE_FONT, TITLE_SIZE, bold=True))
            reqs.append(para_style(rng, align="CENTER", first_indent=0, space_above=12, space_below=6, line_pct=LINE_SPACING_PCT))
        elif b.role == "authors":
            reqs.append(text_style(rng, AUTHOR_FONT, AUTHOR_SIZE, bold=True, italic=True))
            reqs.append(para_style(rng, align="CENTER", first_indent=0, space_above=0, space_below=0, line_pct=LINE_SPACING_PCT))
        elif b.role in ("abstract_vi", "abstract_en"):
            reqs.append(text_style(rng, ABSTRACT_FONT, ABSTRACT_SIZE, italic=True))
            reqs.append(para_style(rng, align="JUSTIFIED", first_indent=FIRST_LINE_INDENT, space_above=6, space_below=0, line_pct=LINE_SPACING_PCT))
            # Make the **Tóm tắt:** / **Abstract:** prefix bold.
            label_pattern = re.compile(r"^(Tóm tắt|Abstract):\s*", re.M)
            payload = strip_markdown_inline(b.text)
            mm = label_pattern.match(payload)
            if mm:
                lbl_start = b.start
                lbl_end = b.start + len(mm.group(0))
                reqs.append(text_style({"startIndex": lbl_start, "endIndex": lbl_end}, ABSTRACT_FONT, ABSTRACT_SIZE, bold=True, italic=True))
        elif b.role in ("keywords_vi", "keywords_en"):
            reqs.append(text_style(rng, ABSTRACT_FONT, ABSTRACT_SIZE, italic=True))
            reqs.append(para_style(rng, align="JUSTIFIED", first_indent=FIRST_LINE_INDENT, space_above=0, space_below=6, line_pct=LINE_SPACING_PCT))
            label_pattern = re.compile(r"^(Từ khoá|Keywords):\s*", re.M)
            payload = strip_markdown_inline(b.text)
            mm = label_pattern.match(payload)
            if mm:
                lbl_start = b.start
                lbl_end = b.start + len(mm.group(0))
                reqs.append(text_style({"startIndex": lbl_start, "endIndex": lbl_end}, ABSTRACT_FONT, ABSTRACT_SIZE, bold=True, italic=True))
        elif b.role in ("h1", "refs_heading"):
            reqs.append(text_style(rng, BODY_FONT, 14, bold=True))
            reqs.append(para_style(rng, align="START", first_indent=0, space_above=12, space_below=4, line_pct=LINE_SPACING_PCT))
        elif b.role == "h2":
            reqs.append(text_style(rng, BODY_FONT, 13, bold=True, italic=True))
            reqs.append(para_style(rng, align="START", first_indent=0, space_above=8, space_below=2, line_pct=LINE_SPACING_PCT))
        elif b.role == "body":
            reqs.append(text_style(rng, BODY_FONT, BODY_SIZE))
            reqs.append(para_style(rng, align="JUSTIFIED", first_indent=FIRST_LINE_INDENT, space_above=6, space_below=0, line_pct=LINE_SPACING_PCT))
        elif b.role == "reference":
            reqs.append(text_style(rng, BODY_FONT, BODY_SIZE))
            reqs.append(para_style(rng, align="JUSTIFIED", first_indent=0, space_above=4, space_below=0, line_pct=LINE_SPACING_PCT,
                                    indent_hanging=cm_to_pt(1.0)))
        elif b.role == "caption":
            reqs.append(text_style(rng, CAPTION_FONT, CAPTION_SIZE, italic=True))
            reqs.append(para_style(rng, align="CENTER", first_indent=0, space_above=2, space_below=6, line_pct=LINE_SPACING_PCT))
        elif b.role == "figure_marker":
            # placeholder paragraph styling — will be image after replacement.
            reqs.append(para_style(rng, align="CENTER", first_indent=0, space_above=12, space_below=2, line_pct=LINE_SPACING_PCT))
    return reqs


def text_style(rng, font, size, bold=False, italic=False):
    fields = ["weightedFontFamily", "fontSize", "bold", "italic"]
    return {
        "updateTextStyle": {
            "range": rng,
            "textStyle": {
                "weightedFontFamily": {"fontFamily": font, "weight": 400},
                "fontSize": {"magnitude": size, "unit": "PT"},
                "bold": bold,
                "italic": italic,
            },
            "fields": ",".join(fields),
        }
    }


def para_style(rng, align="START", first_indent=0, space_above=0, space_below=0, line_pct=LINE_SPACING_PCT, indent_hanging=None):
    para = {
        "alignment": align,
        "indentFirstLine": {"magnitude": first_indent, "unit": "PT"},
        "spaceAbove": {"magnitude": space_above, "unit": "PT"},
        "spaceBelow": {"magnitude": space_below, "unit": "PT"},
        "lineSpacing": line_pct,
        "indentStart": {"magnitude": 0, "unit": "PT"},
    }
    fields = ["alignment", "indentFirstLine", "spaceAbove", "spaceBelow", "lineSpacing", "indentStart"]
    if indent_hanging is not None:
        para["indentStart"] = {"magnitude": indent_hanging, "unit": "PT"}
        para["indentFirstLine"] = {"magnitude": -indent_hanging + first_indent, "unit": "PT"}
    return {
        "updateParagraphStyle": {
            "range": rng,
            "paragraphStyle": para,
            "fields": ",".join(fields),
        }
    }


# ───────────────────────────── Clear + Page setup ─────────────────────

def get_end_index(docs_service, doc_id):
    doc = docs_service.documents().get(documentId=doc_id).execute()
    content = doc["body"]["content"]
    end = content[-1]["endIndex"] if content else 1
    return end


def clear_and_setup_requests():
    """Returns the initial batch: set page style. (Clear is done in a separate first call
    so the index state is deterministic before other inserts.)"""
    return [{
        "updateDocumentStyle": {
            "documentStyle": {
                "marginTop": {"magnitude": MARGIN_TOP, "unit": "PT"},
                "marginBottom": {"magnitude": MARGIN_BOTTOM, "unit": "PT"},
                "marginLeft": {"magnitude": MARGIN_LEFT, "unit": "PT"},
                "marginRight": {"magnitude": MARGIN_RIGHT, "unit": "PT"},
                "pageSize": {
                    "width": {"magnitude": PAGE_W, "unit": "PT"},
                    "height": {"magnitude": PAGE_H, "unit": "PT"},
                },
            },
            "fields": "marginTop,marginBottom,marginLeft,marginRight,pageSize",
        }
    }]


# ───────────────────────────── Main ─────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    ap.add_argument("--dry-run", action="store_true", help="Parse + print plan, no API calls.")
    args = ap.parse_args()

    md = Path(args.source).read_text(encoding="utf-8")
    blocks = parse_paper(md)

    print(f"Parsed {len(blocks)} blocks:")
    role_counts = {}
    for b in blocks:
        role_counts[b.role] = role_counts.get(b.role, 0) + 1
    for r, n in sorted(role_counts.items()):
        print(f"  {r}: {n}")

    if args.dry_run:
        print("\n[DRY RUN] First 8 blocks:")
        for b in blocks[:8]:
            print(f"  {b.role:<15} | {b.text[:80]}")
        return

    auth = load_auth()
    docs = auth.get_docs_service()

    # STEP 1: clear doc content.
    end = get_end_index(docs, args.doc_id)
    print(f"\nCurrent doc endIndex: {end}")
    if end > 2:
        print("Clearing existing content...")
        docs.documents().batchUpdate(
            documentId=args.doc_id,
            body={"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1}}}]},
        ).execute()

    # STEP 2: set page style.
    docs.documents().batchUpdate(
        documentId=args.doc_id,
        body={"requests": clear_and_setup_requests()},
    ).execute()
    print("Page style set.")

    # STEP 3: insert all text (forward order — each insertText's location.index is
    # computed assuming all prior requests in the same batchUpdate have already been applied,
    # which is exactly how the Docs API processes a single batch sequentially).
    insert_reqs, final_cursor = build_insertions(blocks)
    # Chunk to stay under API request limits (API cap ~1000/request, we use 200).
    CHUNK_INS = 200
    for i in range(0, len(insert_reqs), CHUNK_INS):
        docs.documents().batchUpdate(
            documentId=args.doc_id,
            body={"requests": insert_reqs[i:i + CHUNK_INS]},
        ).execute()
    print(f"Inserted {len(insert_reqs)} text chunks, final cursor {final_cursor}.")

    # STEP 4: apply styles (forward order: ranges already computed relative to cumulative inserts).
    style_reqs = style_requests_for(blocks)
    # Chunk to stay under API request limits.
    CHUNK = 200
    for i in range(0, len(style_reqs), CHUNK):
        docs.documents().batchUpdate(
            documentId=args.doc_id,
            body={"requests": style_reqs[i:i + CHUNK]},
        ).execute()
    print(f"Applied {len(style_reqs)} style requests.")

    # STEP 5: replace figure markers with inline images.
    fig_replacements = 0
    for b in blocks:
        if b.role != "figure_marker":
            continue
        token = b.meta["token"]
        num = b.meta["num"]
        kind = b.meta["kind"]
        if kind == "figure":
            url = FIGURE_URLS.get(num)
            width = FIGURE_WIDTH_PT
        else:
            url = TABLE_URLS.get(num)
            width = TABLE_WIDTH_PT
        if not url:
            print(f"  WARN: no URL for {kind} {num}")
            continue
        # Re-query to find the current index of the token (since earlier style ops may have left stale ranges).
        doc_now = docs.documents().get(documentId=args.doc_id).execute()
        idx = _find_first_index_of_text(doc_now, token)
        if idx is None:
            print(f"  WARN: token for {kind} {num} not found in doc")
            continue
        reqs = [
            {"deleteContentRange": {"range": {"startIndex": idx, "endIndex": idx + len(token)}}},
            {"insertInlineImage": {
                "location": {"index": idx},
                "uri": url,
                "objectSize": {"width": {"magnitude": width, "unit": "PT"}},
            }},
        ]
        docs.documents().batchUpdate(documentId=args.doc_id, body={"requests": reqs}).execute()
        fig_replacements += 1
    print(f"Replaced {fig_replacements} figure/table markers with inline images.")

    print("\n=== DONE ===")
    print(f"Open https://docs.google.com/document/d/{args.doc_id}/edit to verify.")
    print("NOTE: Line spacing is approximated at 131% of 13pt ≈ 17.03pt. If the reviewer wants exactly 17pt,")
    print("      Format → Line & paragraph spacing → Custom spacing → Exactly 17pt (10-second manual fix).")


def _find_first_index_of_text(doc, token):
    """Scan the doc body for the first occurrence of `token` and return its start index."""
    for elem in doc["body"]["content"]:
        para = elem.get("paragraph")
        if not para:
            continue
        for el in para.get("elements", []):
            tr = el.get("textRun")
            if not tr:
                continue
            content = tr.get("content", "")
            if token in content:
                return el["startIndex"] + content.find(token)
    return None


if __name__ == "__main__":
    main()
