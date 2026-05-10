"""
build-fixed-thesis-docx: produce the final thesis .docx via pandoc.

Pipeline:
  1. Concatenate the 15 ordered markdown files in documents/fixed-final-thesis-paper/
     with explicit \\newpage separators into _combined.md
  2. Run pandoc with --reference-doc=reference.docx (Decision 612/QD-DHHN styles)
  3. Output: Adaptive-Learning-Platform-Final.docx in the same folder

Pre-requisites:
  - pandoc installed (>= 3.x). Install on Windows:
      winget install --id JohnMacFarlane.Pandoc -e
  - reference.docx exists. Generate via:
      python scripts/build-reference-docx.py

Usage:
    python scripts/build-fixed-thesis-docx.py
    python scripts/build-fixed-thesis-docx.py --keep-combined   # keep _combined.md after build
    python scripts/build-fixed-thesis-docx.py --output FOO.docx
    python scripts/build-fixed-thesis-docx.py --no-toc          # skip pandoc-generated TOC
    python scripts/build-fixed-thesis-docx.py --dry-run         # only emit _combined.md
"""
import argparse
import glob
import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "documents" / "fixed-final-thesis-paper"
DEFAULT_OUT = SRC / "Adaptive-Learning-Platform-Final.docx"
COMBINED = SRC / "_combined.md"
REF = SRC / "reference.docx"

# Order matches PLAN.md §7.2. Cover EN/VN added by user in Word; companion
# appendix files excluded (supplementary only).
ORDER = [
    "01-declaration-of-authorship.md",
    "02-acknowledgement.md",
    "04-abbreviations.md",
    "05-list-of-tables.md",
    "06-list-of-figures.md",
    "06b-list-of-listings.md",
    "07-abstract.md",
    "08-chapter-1-introduction.md",
    "09-chapter-2-literature-review.md",
    "10-chapter-3-system-design.md",
    "11-chapter-4-implementation.md",
    "12-chapter-5-pilot-evaluation.md",
    "13-chapter-6-conclusion.md",
    "14-references.md",
    "15-appendix-a.md",
    "16-appendix-b.md",
]


def fail(msg, code=1):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(code)


def check_inputs():
    missing = [n for n in ORDER if not (SRC / n).exists()]
    if missing:
        fail("Missing source markdown:\n  - " + "\n  - ".join(missing))
    if not REF.exists():
        fail(f"Missing {REF.name}. Generate it first:\n"
             f"  python scripts/build-reference-docx.py")


def find_pandoc():
    """Locate pandoc.exe across PATH and standard Windows install locations.

    winget often installs pandoc into per-user folders that the running shell
    has not picked up yet (PATH refresh requires a new shell). Search common
    locations directly so the build works without restarting the terminal.
    """
    p = shutil.which("pandoc")
    if p:
        return p

    candidates = []
    local = os.environ.get("LOCALAPPDATA", "")
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    if local:
        candidates += [
            Path(local) / "Pandoc" / "pandoc.exe",
            Path(local) / "Microsoft" / "WinGet" / "Links" / "pandoc.exe",
        ]
        # winget package folder pattern:
        # %LOCALAPPDATA%\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_*\pandoc-*\pandoc.exe
        for hit in glob.glob(str(Path(local) / "Microsoft" / "WinGet" / "Packages"
                                  / "JohnMacFarlane.Pandoc*" / "pandoc-*" / "pandoc.exe")):
            candidates.append(Path(hit))
    candidates += [
        Path(pf) / "Pandoc" / "pandoc.exe",
        Path(pf86) / "Pandoc" / "pandoc.exe",
        Path(r"C:\ProgramData\chocolatey\bin\pandoc.exe"),
    ]
    for c in candidates:
        if c.is_file():
            return str(c)
    return None


def check_pandoc():
    p = find_pandoc()
    if not p:
        fail("pandoc not found on PATH or in standard install locations.\n"
             "Install:\n"
             "  winget install --id JohnMacFarlane.Pandoc -e\n"
             "Then OPEN A NEW TERMINAL (PATH refresh) and re-run this script.")
    out = subprocess.run([p, "--version"], capture_output=True, text=True).stdout
    first_line = out.splitlines()[0] if out else "(unknown)"
    print(f"[INFO] {first_line}  (at {p})")
    return p


def concatenate(keep_yaml_meta=False):
    """Join all chapters with explicit page breaks. Strip per-file BOMs."""
    parts = []
    if keep_yaml_meta:
        parts.append("---\n"
                     "title: Adaptive Learning Platform for University Programming Courses\n"
                     "author: Nguyễn Tuấn Dương\n"
                     "lang: en\n"
                     "---\n\n")
    for i, name in enumerate(ORDER):
        text = (SRC / name).read_text(encoding="utf-8")
        if text.startswith("﻿"):
            text = text.lstrip("﻿")
        if i > 0:
            parts.append("\n\n\\newpage\n\n")
        parts.append(text.rstrip() + "\n")
    COMBINED.write_text("".join(parts), encoding="utf-8")
    word_count = sum(len(p.split()) for p in parts)
    print(f"[OK] wrote {COMBINED.relative_to(ROOT)}  ({word_count:,} approx words)")


def run_pandoc(pandoc_exe: str, out_path: Path, with_toc: bool):
    cmd = [
        pandoc_exe, str(COMBINED),
        "--from", "markdown+pipe_tables+yaml_metadata_block+raw_tex+implicit_figures+smart",
        "--to", "docx",
        "--reference-doc", str(REF),
        "--resource-path", str(SRC),
        # No syntax highlighting — Decision 612 grayscale rule, plus the docx
        # frame already distinguishes code from prose (PLAN.md §10.5).
        "--no-highlight",
        "--output", str(out_path),
    ]
    if with_toc:
        cmd += ["--toc", "--toc-depth=3"]
    print(f"[INFO] pandoc → {out_path.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout, end="")
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        fail(f"pandoc exited {res.returncode}")
    if res.stderr.strip():
        print("[WARN] pandoc stderr:")
        print(res.stderr)


def merge_code_block_borders(docx_path: Path):
    """Group consecutive Source Code paragraphs into single bordered blocks.

    Pandoc emits each line of a fenced ```code``` as a separate paragraph styled
    "Source Code". The reference.docx Source Code style carries shading but no
    borders (intentionally — see configure_code_styles in build-reference-docx).
    Without this pass, a multi-line block has no frame at all. With it:
      - first line of a run: top + left + right borders, plus 6pt space-before
      - middle lines: left + right only
      - last line: bottom + left + right, plus 6pt space-after

    The result reads as one continuous bordered region (LaTeX `frame=single`
    equivalent), matching PLAN.md §10.3.
    """
    try:
        from docx import Document
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Pt
    except ImportError:
        print("[WARN] python-docx missing; skipping code block border pass")
        return

    doc = Document(docx_path)

    # Collect indices of paragraphs whose style is Source Code (or aliases)
    paragraphs = doc.paragraphs
    is_code = []
    for p in paragraphs:
        sn = (p.style.name or "").lower()
        is_code.append(sn in ("source code", "sourcecode"))

    # Group consecutive runs of code paragraphs
    runs = []
    i = 0
    while i < len(is_code):
        if is_code[i]:
            j = i
            while j < len(is_code) and is_code[j]:
                j += 1
            runs.append((i, j - 1))
            i = j
        else:
            i += 1

    def set_border(pPr, sides, sz="4", color="000000", space="6"):
        for old in pPr.findall(qn("w:pBdr")):
            pPr.remove(old)
        bdr = OxmlElement("w:pBdr")
        for side in sides:
            b = OxmlElement(f"w:{side}")
            b.set(qn("w:val"), "single")
            b.set(qn("w:sz"), sz)
            b.set(qn("w:space"), space)
            b.set(qn("w:color"), color)
            bdr.append(b)
        pPr.append(bdr)

    for start, end in runs:
        for k in range(start, end + 1):
            p = paragraphs[k]
            pPr = p._p.get_or_add_pPr()
            if start == end:
                # Single-line block — full frame
                set_border(pPr, ("top", "left", "bottom", "right"))
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(6)
            elif k == start:
                set_border(pPr, ("top", "left", "right"))
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(0)
            elif k == end:
                set_border(pPr, ("left", "bottom", "right"))
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(6)
            else:
                set_border(pPr, ("left", "right"))
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)

    doc.save(docx_path)
    n_lines = sum(end - start + 1 for start, end in runs)
    print(f"[OK] post-process: {len(runs)} code blocks ({n_lines} lines) framed")


def widen_tables_and_images(docx_path: Path):
    """Force every table to 100% page width and every image-table PNG to text-area width.

    Why this is needed:
      - Pandoc emits per-table `<w:tblW w:w="0" w:type="auto">` which overrides
        the 5000-pct width set in the reference.docx Table style. We strip that
        override and pin every table to 100% of the text area.
      - Image-tables (PNG, filename pattern `table-*.png`) are inserted at their
        native pixel-DPI width. We resize them to exactly the text area width
        (15.5 cm with Decision 612 margins) preserving aspect ratio.
      - Other figures (`figure-*.png`) are NOT touched — they keep their
        natural size unless they exceed text width, in which case we shrink to fit.

    Decision 612 margins: A4 21 cm minus left 3.5 cm minus right 2 cm = 15.5 cm.
    """
    try:
        from docx import Document
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
        from docx.shared import Cm, Emu
    except ImportError:
        print("[WARN] python-docx missing; skipping table/image width pass")
        return

    TEXT_WIDTH = Cm(15.5)
    NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    doc = Document(docx_path)

    # ── 1. Tables: set tblW=5000 pct, layout=autofit, strip per-cell widths
    n_tables = 0
    for table in doc.tables:
        tbl = table._tbl
        tbl_pr = tbl.find(qn("w:tblPr"))
        if tbl_pr is None:
            tbl_pr = OxmlElement("w:tblPr")
            tbl.insert(0, tbl_pr)

        # Replace tblW
        for old in tbl_pr.findall(qn("w:tblW")):
            tbl_pr.remove(old)
        tbl_w = OxmlElement("w:tblW")
        tbl_w.set(qn("w:w"), "5000")
        tbl_w.set(qn("w:type"), "pct")
        tbl_pr.append(tbl_w)

        # Replace tblLayout
        for old in tbl_pr.findall(qn("w:tblLayout")):
            tbl_pr.remove(old)
        layout = OxmlElement("w:tblLayout")
        layout.set(qn("w:type"), "autofit")
        tbl_pr.append(layout)

        # Strip <w:tblGrid>/<w:gridCol> widths so columns redistribute
        for grid in tbl.findall(qn("w:tblGrid")):
            for col in grid.findall(qn("w:gridCol")):
                # Remove explicit width — Word will infer from content
                if qn("w:w") in col.attrib:
                    del col.attrib[qn("w:w")]

        # Set every cell width to type=auto so they don't fight tblW
        for row in tbl.findall(qn("w:tr")):
            for cell in row.findall(qn("w:tc")):
                cell_pr = cell.find(qn("w:tcPr"))
                if cell_pr is None:
                    continue
                for tcw in cell_pr.findall(qn("w:tcW")):
                    tcw.set(qn("w:w"), "0")
                    tcw.set(qn("w:type"), "auto")
        n_tables += 1

    # ── 2. Inline images: resize per filename heuristic
    n_table_imgs = 0
    n_other_imgs = 0
    for shape in doc.inline_shapes:
        # Get filename via blip relationship
        try:
            blip = shape._inline.graphic.graphicData.pic.blipFill.blip
            r_id = blip.embed
            rel = doc.part.related_parts[r_id]
            filename = (rel.partname.split("/")[-1] or "").lower()
        except Exception:
            filename = ""

        cur_w = shape.width
        cur_h = shape.height
        if not cur_w or not cur_h:
            continue
        ratio = cur_h / cur_w

        if filename.startswith("table-"):
            # Force to text-area width
            shape.width = TEXT_WIDTH
            shape.height = Emu(int(int(TEXT_WIDTH) * ratio))
            n_table_imgs += 1
        else:
            # Other images: shrink only if too wide
            if cur_w > TEXT_WIDTH:
                shape.width = TEXT_WIDTH
                shape.height = Emu(int(int(TEXT_WIDTH) * ratio))
            n_other_imgs += 1

    doc.save(docx_path)
    print(f"[OK] post-process: {n_tables} tables widened to 100%, "
          f"{n_table_imgs} table-PNGs scaled to 15.5cm, "
          f"{n_other_imgs} other images checked")


def report(out_path: Path):
    if not out_path.exists():
        fail(f"output not produced: {out_path}")
    size_kb = out_path.stat().st_size / 1024
    print()
    print(f"[OK] {out_path}")
    print(f"     size: {size_kb:,.1f} KB")
    print()
    print("Next steps (PLAN.md §7.4):")
    print("  1. Open the .docx in Word.")
    print("  2. Add EN cover page at top, VN cover page after (Comment #23).")
    print("  3. Right-click TOC / List of Tables / List of Figures → Update Field.")
    print("  4. Verify caption styles, page breaks, hanging indent on References.")
    print("  5. Word-count check (≤ 19,500) in Review → Word Count.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUT,
                    help="output docx path (default: %(default)s)")
    ap.add_argument("--keep-combined", action="store_true",
                    help="keep _combined.md after build (otherwise deleted)")
    ap.add_argument("--no-toc", action="store_true",
                    help="skip pandoc-generated TOC")
    ap.add_argument("--dry-run", action="store_true",
                    help="only emit _combined.md, do not run pandoc")
    args = ap.parse_args()

    check_inputs()
    concatenate()

    if args.dry_run:
        print("[INFO] --dry-run: skipping pandoc")
        return

    pandoc_exe = check_pandoc()
    run_pandoc(pandoc_exe, args.output, with_toc=not args.no_toc)
    merge_code_block_borders(args.output)
    widen_tables_and_images(args.output)
    report(args.output)

    if not args.keep_combined:
        COMBINED.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
