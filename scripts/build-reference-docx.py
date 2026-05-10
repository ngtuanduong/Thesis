"""
build-reference-docx: generate Decision 612/QD-DHHN reference template for pandoc.

Output: documents/fixed-final-thesis-paper/reference.docx

The output file is a docx whose only purpose is to carry style definitions that
pandoc will copy into the final thesis docx via `pandoc --reference-doc=...`.
Body content is empty; only styles + page setup matter.

Specs — verbatim from HD-the-thuc-trinh-bay-KLTN.txt §2.2.1 (Decision 612/QD-DHHN):

  Body (Normal)  TNR 13 pt, regular, justified, line 1.5
                 (no compression/expansion of letter spacing)

  Heading 1      TNR 16 pt bold UPPERCASE, centered,
                 32 pt before / 32 pt after, line 1.5
                 — chapter titles ("CHAPTER 1. INTRODUCTION")

  Heading 2      TNR 14 pt bold (lowercase), justified both sides,
                 6 pt before / 6 pt after, line 1.5
                 — sections "1.1. ..."

  Heading 3      TNR 13 pt regular (NOT bold), justified both sides,
                 6 pt before / 6 pt after, line 1.5
                 — subsections "1.1.1. ..."

  Heading 4      TNR 13 pt italic (NOT bold), justified both sides,
                 6 pt before / 6 pt after, line 1.5
                 — sub-subsections "1.1.1.1. ..."

  Footnote       TNR 10 pt (§2.2.2)

  Block Quote    indent 5 spaces from left, line 1.5 (§3.1.2)
                 — long quotations of 40+ words

  Caption        TNR 12 pt italic centered (common practice; spec silent)

  Page           A4 (210x297 mm), margins T 3 / B 3 / L 3.5 / R 2 cm
                 Page number bottom-center, Arabic from Chapter 1.
                 Front matter (Declaration → Abstract) uses lowercase
                 Roman (i, ii, iii) — set up by user in Word via two
                 section breaks (cannot be expressed in pandoc reference doc).

Usage:
    python scripts/build-reference-docx.py
"""
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "documents" / "fixed-final-thesis-paper" / "reference.docx"

FONT = "Times New Roman"


def force_font(rpr_element, name=FONT):
    """Force ascii/hAnsi/eastAsia/cs font slots — python-docx only sets ascii."""
    rfonts = rpr_element.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr_element.append(rfonts)
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{attr}"), name)


def force_black(rpr_element):
    """Override any inherited theme/blue color with explicit black.

    Built-in Word "Heading 1/2/3/4" styles default to a blue accent color
    (e.g. #2E74B5). The thesis must be black per Decision 612, so we strip
    any inherited <w:color> and pin it to #000000.
    """
    for old in rpr_element.findall(qn("w:color")):
        rpr_element.remove(old)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "000000")
    color.set(qn("w:themeColor"), "")  # break theme link
    rpr_element.append(color)


def add_paragraph_shading(ppr_element, fill="F5F5F5"):
    """Add <w:shd w:fill="..."/> to a paragraph properties element."""
    for old in ppr_element.findall(qn("w:shd")):
        ppr_element.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    ppr_element.append(shd)


def add_paragraph_border(ppr_element, sides=("top", "left", "bottom", "right"),
                         sz="4", color="000000", space="6"):
    """Add <w:pBdr> with selected edges. sz in eighths-of-pt (4 = 0.5pt)."""
    for old in ppr_element.findall(qn("w:pBdr")):
        ppr_element.remove(old)
    bdr = OxmlElement("w:pBdr")
    for side in sides:
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), sz)
        b.set(qn("w:space"), space)
        b.set(qn("w:color"), color)
        bdr.append(b)
    ppr_element.append(bdr)


def set_font(style, size_pt, bold=False, italic=False):
    f = style.font
    f.name = FONT
    rpr = style.element.get_or_add_rPr()
    force_font(rpr)
    force_black(rpr)
    f.size = Pt(size_pt)
    f.bold = bold
    f.italic = italic


def set_paragraph(style, alignment, line_spacing, space_before, space_after,
                  first_line_indent=None, left_indent=None,
                  page_break_before=False, keep_with_next=False):
    p = style.paragraph_format
    p.alignment = alignment
    if line_spacing is not None:
        p.line_spacing = line_spacing
        p.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if first_line_indent is not None:
        p.first_line_indent = first_line_indent
    if left_indent is not None:
        p.left_indent = left_indent
    p.page_break_before = page_break_before
    p.keep_with_next = keep_with_next


def configure_styles(doc):
    """Set styles per Decision 612/QD-DHHN §2.2.1."""
    styles = doc.styles
    existing = {st.name for st in styles}

    # Normal — body text  (TNR 13pt, justified, 1.5 line, indent 1.27cm)
    s = styles["Normal"]
    set_font(s, 13)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.5, space_before=0, space_after=0,
                  first_line_indent=Cm(1.27))

    # Heading 1 — Chapter title  (TNR 16pt bold UPPERCASE center 32/32 1.5)
    s = styles["Heading 1"]
    s.base_style = styles["Normal"]
    set_font(s, 16, bold=True)
    # caps property
    rpr = s.element.get_or_add_rPr()
    caps = OxmlElement("w:caps")
    caps.set(qn("w:val"), "true")
    rpr.append(caps)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.CENTER,
                  line_spacing=1.5, space_before=32, space_after=32,
                  first_line_indent=Cm(0),
                  page_break_before=True, keep_with_next=True)

    # Heading 2 — Section "1.1."  (TNR 14pt bold justified 6/6 1.5)
    s = styles["Heading 2"]
    s.base_style = styles["Normal"]
    set_font(s, 14, bold=True)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.5, space_before=6, space_after=6,
                  first_line_indent=Cm(0), keep_with_next=True)

    # Heading 3 — Subsection "1.1.1."  (TNR 13pt PLAIN justified 6/6 1.5)
    s = styles["Heading 3"]
    s.base_style = styles["Normal"]
    set_font(s, 13, bold=False)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.5, space_before=6, space_after=6,
                  first_line_indent=Cm(0), keep_with_next=True)

    # Heading 4 — Sub-subsection "1.1.1.1."  (TNR 13pt italic-only justified 6/6 1.5)
    s = styles["Heading 4"]
    s.base_style = styles["Normal"]
    set_font(s, 13, bold=False, italic=True)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.5, space_before=6, space_after=6,
                  first_line_indent=Cm(0), keep_with_next=True)

    # Caption — figure / table captions  (12pt italic centered)
    if "Caption" not in existing:
        styles.add_style("Caption", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Caption"]
    s.base_style = styles["Normal"]
    set_font(s, 12, italic=True)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.CENTER,
                  line_spacing=1.15, space_before=6, space_after=6,
                  first_line_indent=Cm(0))

    # Image Caption — used by pandoc for `![caption](image)` figures
    if "Image Caption" not in existing:
        styles.add_style("Image Caption", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Image Caption"]
    s.base_style = styles["Caption"]
    set_font(s, 12, italic=True)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.CENTER,
                  line_spacing=1.15, space_before=6, space_after=6,
                  first_line_indent=Cm(0))

    # Footnote Text — TNR 10pt (§2.2.2)
    if "Footnote Text" not in existing:
        styles.add_style("Footnote Text", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Footnote Text"]
    s.base_style = styles["Normal"]
    set_font(s, 10)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.0, space_before=0, space_after=0,
                  first_line_indent=Cm(0))

    # Footnote Reference — superscript number, TNR 10pt
    if "Footnote Reference" not in existing:
        styles.add_style("Footnote Reference", WD_STYLE_TYPE.CHARACTER)
    s = styles["Footnote Reference"]
    f = s.font
    f.name = FONT
    f.size = Pt(10)
    f.superscript = True
    rpr = s.element.get_or_add_rPr()
    force_font(rpr)

    # Block Quote — long quotations 40+ words, indent 5 chars from left (§3.1.2)
    # 5 spaces ≈ 1.27 cm at 13pt TNR
    if "Block Quote" not in existing:
        styles.add_style("Block Quote", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Block Quote"]
    s.base_style = styles["Normal"]
    set_font(s, 13)
    set_paragraph(s, WD_ALIGN_PARAGRAPH.JUSTIFY,
                  line_spacing=1.5, space_before=6, space_after=6,
                  first_line_indent=Cm(0), left_indent=Cm(1.27))


CODE_FONT = "Consolas"


def _set_code_font(rpr_element, size_pt):
    """Set Consolas across all 4 font slots + black + size."""
    rfonts = rpr_element.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr_element.append(rfonts)
    for attr in ("ascii", "hAnsi", "eastAsia", "cs"):
        rfonts.set(qn(f"w:{attr}"), CODE_FONT)
    for old in rpr_element.findall(qn("w:sz")):
        rpr_element.remove(old)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size_pt * 2)))  # half-points
    rpr_element.append(sz)
    force_black(rpr_element)


def configure_code_styles(doc):
    """Add Source Code (paragraph) + Verbatim Char (character) styles.

    Source Code (Consolas 10pt, left, line 1.0, gray shading #F5F5F5):
      - Frame borders are NOT applied here. They are added per-paragraph in
        the merge_code_block_borders post-process so a multi-line block looks
        like one continuous box (top on first line, bottom on last, sides on
        every line, NO horizontal line between code lines).
      - Shading IS applied here so every line carries the gray background
        consistently.

    Verbatim Char (Consolas 11pt, no shading):
      - Used for inline `code` spans inline with prose.
      - 11pt is a slight visual reduction from body 13pt so monospace doesn't
        bloat the line height.
    """
    styles = doc.styles
    existing = {st.name for st in styles}

    # ── Source Code (paragraph) ─────────────────────────────────────────────
    if "Source Code" not in existing:
        styles.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Source Code"]
    # Don't base on Normal — we want a clean slate (no first-line indent,
    # no justified alignment inheritance).
    rpr = s.element.get_or_add_rPr()
    _set_code_font(rpr, 10)
    # Strip any inherited bold / italic so code is plain
    for tag in ("b", "i", "caps"):
        for old in rpr.findall(qn(f"w:{tag}")):
            rpr.remove(old)
    # Paragraph properties
    p = s.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.line_spacing = 1.0
    p.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.first_line_indent = Cm(0)
    p.left_indent = Cm(0)
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.keep_with_next = True
    # Shading on every line; borders added per-line in post-process
    ppr = s.element.get_or_add_pPr()
    add_paragraph_shading(ppr, fill="F5F5F5")
    # Suppress automatic hyphenation and explicit "wrap to next line" indents
    # by setting a contextualSpacing flag (so adjacent Source Code paragraphs
    # don't get extra space between them).
    cs = OxmlElement("w:contextualSpacing")
    cs.set(qn("w:val"), "true")
    ppr.append(cs)

    # ── Verbatim Char (character) ───────────────────────────────────────────
    if "Verbatim Char" not in existing:
        styles.add_style("Verbatim Char", WD_STYLE_TYPE.CHARACTER)
    s = styles["Verbatim Char"]
    rpr = s.element.get_or_add_rPr()
    _set_code_font(rpr, 11)
    # No shading on character style (must work mid-sentence)


def _table_borders_xml(sz="4", color="000000"):
    """Build a <w:tblBorders> element with full single-line borders.

    sz is in eighths of a point: sz=4 → 0.5pt (Word default thin border).
    """
    tbl_borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), sz)
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), color)
        tbl_borders.append(b)
    return tbl_borders


def configure_table_styles(doc):
    """Define table styles so pandoc-generated tables render with visible borders.

    Pandoc's docx writer applies styleId "Table" to every table by default. The
    built-in "Table Normal" carries no borders, so without an override every cell
    would be borderless. We add a "Table" style here that:
      - sets full single 0.5pt black borders on outer + inner cell edges
      - inherits font from Normal (TNR 13pt)
      - leaves cell margins at Word defaults
    Keep "Table Grid" untouched so users can fall back to Word's built-in if
    they manually re-style any specific table.
    """
    styles = doc.styles
    existing = {st.name for st in styles}

    # Add or reuse "Table" style. python-docx auto-attaches it to TableNormal
    # via the underlying XML; we don't need to set base_style explicitly
    # (and "Table Normal" isn't always exposed by friendly name).
    if "Table" not in existing:
        styles.add_style("Table", WD_STYLE_TYPE.TABLE)
    s = styles["Table"]

    # python-docx exposes limited table-style API; drop into the XML to add
    # tblPr → tblBorders.
    style_el = s.element
    # Clear any pre-existing tblPr to keep our definition authoritative
    for old in style_el.findall(qn("w:tblPr")):
        style_el.remove(old)
    tbl_pr = OxmlElement("w:tblPr")

    # Width = 100% of text area (5000 fiftieths-of-a-percent = 100%).
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), "5000")
    tbl_w.set(qn("w:type"), "pct")
    tbl_pr.append(tbl_w)

    tbl_pr.append(_table_borders_xml())

    # Layout = autofit so columns redistribute within the 100% table width.
    tbl_layout = OxmlElement("w:tblLayout")
    tbl_layout.set(qn("w:type"), "autofit")
    tbl_pr.append(tbl_layout)

    # Reasonable cell margins so text doesn't kiss the borders.
    tbl_cell_mar = OxmlElement("w:tblCellMar")
    for edge, twips in (("top", "60"), ("left", "100"), ("bottom", "60"), ("right", "100")):
        m = OxmlElement(f"w:{edge}")
        m.set(qn("w:w"), twips)
        m.set(qn("w:type"), "dxa")
        tbl_cell_mar.append(m)
    tbl_pr.append(tbl_cell_mar)
    style_el.append(tbl_pr)

    # Paragraph defaults for cells: TNR 13pt, single line spacing, no first-line
    # indent (overrides Normal's 1.27cm body indent which looks ugly in cells).
    for old in style_el.findall(qn("w:pPr")):
        style_el.remove(old)
    p_pr = OxmlElement("w:pPr")
    spacing = OxmlElement("w:spacing")
    spacing.set(qn("w:before"), "60")
    spacing.set(qn("w:after"), "60")
    spacing.set(qn("w:line"), "276")  # 1.15× line
    spacing.set(qn("w:lineRule"), "auto")
    p_pr.append(spacing)
    ind = OxmlElement("w:ind")
    ind.set(qn("w:firstLine"), "0")
    p_pr.append(ind)
    style_el.append(p_pr)

    for old in style_el.findall(qn("w:rPr")):
        style_el.remove(old)
    r_pr = OxmlElement("w:rPr")
    force_font(r_pr)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "26")  # 13pt
    r_pr.append(sz)
    force_black(r_pr)
    style_el.append(r_pr)


def configure_page(doc):
    """A4 with Decision 612 margins (T3 / B3 / L3.5 / R2 cm)."""
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(3.5)
    section.right_margin = Cm(2.0)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)


def add_centered_page_number_footer(doc):
    """Insert a centered PAGE field into the primary footer of section 1.

    Note: front matter (Declaration → Abstract) needs lowercase Roman numerals
    and body needs Arabic restarting at Chapter 1. That two-zone setup requires
    section breaks pandoc cannot generate from markdown — user configures it
    in Word via Layout → Breaks → Section Break (Next Page) and Insert →
    Page Number → Format Page Numbers per section. See PLAN.md §7.4.
    """
    section = doc.sections[0]
    footer = section.footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    force_font(rpr)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "26")  # 13pt = 26 half-points
    rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    run.append(t)
    fld.append(run)
    para._p.append(fld)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    configure_page(doc)
    configure_styles(doc)
    configure_table_styles(doc)
    configure_code_styles(doc)
    add_centered_page_number_footer(doc)
    doc.save(OUT)
    print(f"[OK] reference.docx written: {OUT}")
    print(f"     size: {OUT.stat().st_size:,} bytes")
    print()
    print("Styles applied (Decision 612/QD-DHHN):")
    print("  Normal       TNR 13pt regular black, justified, 1.5 line, indent 1.27cm")
    print("  Heading 1    TNR 16pt bold UPPERCASE BLACK, center, 32/32, page break")
    print("  Heading 2    TNR 14pt bold BLACK,         justify, 6/6")
    print("  Heading 3    TNR 13pt plain BLACK,        justify, 6/6")
    print("  Heading 4    TNR 13pt italic-only BLACK,  justify, 6/6")
    print("  Caption      TNR 12pt italic black, center")
    print("  Footnote     TNR 10pt black")
    print("  Block Quote  TNR 13pt indent 1.27cm")
    print("  Table        TNR 13pt, full 0.5pt black borders, 100% page width, autofit")
    print("  Source Code  Consolas 10pt left, line 1.0, gray #F5F5F5 shading (borders added in post-process)")
    print("  Verbatim Char Consolas 11pt black (inline `code`)")


if __name__ == "__main__":
    main()
