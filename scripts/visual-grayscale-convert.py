"""
visual-grayscale-convert: bulk convert thesis visuals from saturated colors to grayscale.

Reads HTML files in documents/thesis-chapters/visuals/html/, replaces saturated
hex colors with grayscale equivalents per
documents/fixed-final-thesis-paper/VISUAL-STYLE-GUIDE.md (the authoritative
palette).

Backs up originals to documents/thesis-chapters/visuals/html.backup-pre-grayscale/
on first run (don't overwrite an existing backup file). Pass --no-backup to skip.

Usage:
    python scripts/visual-grayscale-convert.py --dry-run
    python scripts/visual-grayscale-convert.py
    python scripts/visual-grayscale-convert.py --only ch1-thesis-structure-roadmap.html
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
HTML_DIR = PROJECT_ROOT / "documents" / "thesis-chapters" / "visuals" / "html"
BACKUP_DIR = PROJECT_ROOT / "documents" / "thesis-chapters" / "visuals" / "html.backup-pre-grayscale"

# Saturated hex -> grayscale hex.
# Strategy: collapse all chapter/layer color coding to a uniform gray palette.
# Distinction comes from labels and layout, not hue (per VISUAL-STYLE-GUIDE.md §3).
COLOR_MAP = {
    # --- Light fills ---
    "#e3f2fd": "#f5f5f5",   # light blue
    "#bbdefb": "#ebebeb",
    "#90caf9": "#e0e0e0",
    "#fce4ec": "#f5f5f5",   # light pink
    "#f8bbd0": "#ebebeb",
    "#f48fb1": "#e0e0e0",
    "#e8eaf6": "#f5f5f5",   # light deep purple/blue
    "#c5cae9": "#ebebeb",
    "#9fa8da": "#e0e0e0",
    "#fff3e0": "#f5f5f5",   # light orange
    "#ffe0b2": "#ebebeb",
    "#ffcc80": "#e0e0e0",
    "#f3e5f5": "#f5f5f5",   # light purple
    "#e1bee7": "#ebebeb",
    "#ce93d8": "#e0e0e0",
    "#e8f5e9": "#f5f5f5",   # light green
    "#c8e6c9": "#ebebeb",
    "#a5d6a7": "#e0e0e0",
    "#e0f2f1": "#f5f5f5",   # light teal
    "#b2dfdb": "#ebebeb",
    "#80cbc4": "#e0e0e0",
    "#ffebee": "#f5f5f5",   # very light red
    "#ffcdd2": "#ebebeb",

    # --- Dark accents (borders, accent text, glyphs) ---
    "#1565c0": "#222",      # blue (BKT/Ch1)
    "#1a56db": "#222",
    "#4285f4": "#222",
    "#0d47a1": "#222",
    "#283593": "#222",      # deep purple/blue (Ch3 layer)
    "#1a237e": "#222",
    "#3f51b5": "#222",
    "#5c6bc0": "#222",
    "#880e4f": "#222",      # pink (Elo/Ch2)
    "#c2185b": "#222",
    "#ad1457": "#222",
    "#d81b60": "#222",
    "#e91e63": "#222",
    "#e65100": "#222",      # orange (MAB/Ch3 charts)
    "#f57c00": "#222",
    "#fb8c00": "#222",
    "#ef6c00": "#222",
    "#ff9800": "#222",
    "#ff6f00": "#222",
    "#ea4335": "#222",      # red (warnings)
    "#c5221f": "#222",
    "#d32f2f": "#222",
    "#b71c1c": "#222",
    "#f44336": "#222",
    "#6a1b9a": "#222",      # purple (FSRS/Ch4)
    "#7b1fa2": "#222",
    "#4a148c": "#222",
    "#9c27b0": "#222",
    "#8e24aa": "#222",
    "#2e7d32": "#222",      # green (KG/highlights/Ch5)
    "#1b5e20": "#222",
    "#388e3c": "#222",
    "#43a047": "#222",
    "#4caf50": "#222",
    "#66bb6a": "#222",
    "#00695c": "#222",      # teal (data structures topic)
    "#004d40": "#222",
    "#00796b": "#222",
    "#00897b": "#222",
    "#009688": "#222",
    "#006064": "#222",      # very dark teal
    "#00838f": "#222",
    "#0277bd": "#222",      # blue variants
    "#0288d1": "#222",
    "#039be5": "#222",
    "#117722": "#222",      # green
    "#2196f3": "#222",      # blue
    "#42a5f5": "#222",
    "#221155": "#222",      # dark indigo
    "#3949ab": "#222",      # indigo
    "#3d5afe": "#222",
    "#4a90d9": "#222",      # blue
    "#560027": "#222",      # dark maroon
    "#994455": "#222",      # muted maroon
    "#994466": "#222",
    "#995522": "#222",      # muted brown
    "#bf360c": "#222",      # dark orange
    "#dd6611": "#222",
    "#c62828": "#222",      # red
    "#ef5350": "#222",      # light red
    "#f57f17": "#222",      # orange
    "#f9a825": "#222",      # amber
    "#ffb74d": "#222",      # light orange
    "#ffa726": "#222",
    "#ffc107": "#222",
    "#ffd54f": "#222",
    # Light fills missed in initial map
    "#aaccff": "#e0e0e0",   # light blue
    "#cce5ff": "#ebebeb",
    "#ddeeff": "#f5f5f5",
    "#fff8e1": "#f5f5f5",   # light amber
    "#ffecb3": "#ebebeb",
    "#ffe082": "#e0e0e0",
    "#fff9c4": "#f5f5f5",   # light yellow
}

HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")


def expand_short(hex_str):
    """Expand 3-digit hex (#abc) to 6-digit (#aabbcc). Lowercase normalize."""
    s = hex_str.lower()
    if len(s) == 4:
        s = "#" + s[1] * 2 + s[2] * 2 + s[3] * 2
    return s


def convert(content):
    """Apply COLOR_MAP. Returns (new_content, dict[old_hex] -> count)."""
    counts = {}

    def replace(match):
        full = match.group(0)
        normalized = expand_short(full)
        if normalized in COLOR_MAP:
            new = COLOR_MAP[normalized]
            counts[normalized] = counts.get(normalized, 0) + 1
            return new
        return full

    return HEX_RE.sub(replace, content), counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing files.",
    )
    parser.add_argument(
        "--only",
        default=None,
        metavar="FILENAME",
        help="Convert only one file (filename in html/, e.g., ch1-thesis-structure-roadmap.html).",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backups (default: copies originals to html.backup-pre-grayscale/ on first run).",
    )
    args = parser.parse_args()

    if not HTML_DIR.exists():
        print(f"ERROR: {HTML_DIR} does not exist", file=sys.stderr)
        sys.exit(2)

    if args.only:
        files = [HTML_DIR / args.only]
        if not files[0].exists():
            print(f"ERROR: {files[0]} does not exist", file=sys.stderr)
            sys.exit(2)
    else:
        files = sorted(HTML_DIR.glob("*.html"))

    if not args.dry_run and not args.no_backup:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    total_replacements = 0
    files_changed = 0
    unmapped_colors = {}

    for fpath in files:
        content = fpath.read_text(encoding="utf-8")
        new_content, counts = convert(content)

        # Track any saturated hex codes that didn't match the map (for visibility)
        for m in HEX_RE.finditer(content):
            normalized = expand_short(m.group(0))
            if normalized in COLOR_MAP:
                continue
            # heuristic: a color is "saturated" if max-min RGB channel > 30
            try:
                r, g, b = int(normalized[1:3], 16), int(normalized[3:5], 16), int(normalized[5:7], 16)
                if max(r, g, b) - min(r, g, b) > 30:
                    unmapped_colors.setdefault(normalized, []).append(fpath.name)
            except ValueError:
                pass

        if not counts:
            continue

        n_in_file = sum(counts.values())
        total_replacements += n_in_file
        files_changed += 1

        if args.dry_run:
            print(f"[dry-run] {fpath.name}  ({n_in_file} replacements)")
            for old, count in sorted(counts.items()):
                new = COLOR_MAP[old]
                print(f"  {old} -> {new}  x{count}")
        else:
            if not args.no_backup:
                backup_path = BACKUP_DIR / fpath.name
                if not backup_path.exists():
                    shutil.copy2(fpath, backup_path)
            fpath.write_text(new_content, encoding="utf-8")
            print(f"  {fpath.name}  ({n_in_file} replacements)")

    print()
    print(f"Summary: {files_changed} file(s) {'would change' if args.dry_run else 'changed'}, "
          f"{total_replacements} hex color replacements.")

    if unmapped_colors:
        print()
        print(f"WARNING: {len(unmapped_colors)} saturated hex(es) were NOT in COLOR_MAP. "
              f"Add them to the map and re-run if they should be grayscaled:")
        for hex_color, files_with in sorted(unmapped_colors.items()):
            sample_files = ", ".join(sorted(set(files_with))[:3])
            extra = "" if len(set(files_with)) <= 3 else f" (+{len(set(files_with)) - 3} more)"
            print(f"  {hex_color}  in: {sample_files}{extra}")

    if args.dry_run:
        print("(dry-run mode — no files written)")


if __name__ == "__main__":
    main()
