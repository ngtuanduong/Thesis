"""
Render all thesis LaTeX display equations to PNG via CodeCogs,
upload to Catbox, and insert as inline images into the Google Doc.

Pipeline: markdown → extract $$ blocks → CodeCogs PNG → Catbox URL → GDoc insertInlineImage
"""
import importlib.util
import io
import json
import os
import re
import sys
import time
import urllib.parse

import requests
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Google Docs auth ──
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID

CHAPTERS_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters"
TMP_DIR = "C:/tmp/equations"
MAP_FILE = "C:/Users/duong/WebstormProjects/Thesis/scripts/equation-map.json"

os.makedirs(TMP_DIR, exist_ok=True)

# ── Step 1: Extract display equations from markdown ──
MD_FILES = [
    ("chapter3-system-design.md", 3),
    ("chapter4-implementation.md", 4),
    ("chapter5-evaluation.md", 5),
]

equations = []
for fname, ch in MD_FILES:
    path = os.path.join(CHAPTERS_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Match $$...$$  (single-line display equations)
    for match in re.finditer(r'\$\$(.+?)\$\$', content):
        latex = match.group(1).strip()
        # Extract tag number if present
        tag_match = re.search(r'\\tag\{([^}]+)\}', latex)
        if tag_match:
            eq_id = f"eq{tag_match.group(1)}"
        else:
            # Generate ID from chapter + order
            eq_id = f"eq{ch}_notag_{len([e for e in equations if e['chapter'] == ch])}"
        equations.append({
            "id": eq_id,
            "latex": latex,
            "chapter": ch,
        })

print(f"Extracted {len(equations)} display equations:")
for eq in equations:
    print(f"  {eq['id']}: {eq['latex'][:60]}...")

# ── Step 2: Render to PNG via CodeCogs ──
DPI = 200

for eq in equations:
    latex = eq["latex"]
    encoded = urllib.parse.quote(latex)
    url = r"https://latex.codecogs.com/png.image?" + f"\\dpi{{{DPI}}}\\bg{{white}}" + encoded

    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        print(f"  ERROR rendering {eq['id']}: HTTP {resp.status_code}")
        eq["png_path"] = None
        continue

    png_path = os.path.join(TMP_DIR, f"{eq['id'].replace('.', '_')}.png")
    with open(png_path, "wb") as f:
        f.write(resp.content)

    # Get image dimensions
    img = Image.open(png_path)
    eq["png_path"] = png_path
    eq["width_px"] = img.width
    eq["height_px"] = img.height
    print(f"  {eq['id']}: {img.width}x{img.height}px -> {png_path}")

    time.sleep(1)  # Rate limit

# ── Step 3: Upload to Catbox ──
for eq in equations:
    if not eq.get("png_path"):
        continue

    with open(eq["png_path"], "rb") as f:
        resp = requests.post(
            "https://catbox.moe/user/api.php",
            files={"fileToUpload": (os.path.basename(eq["png_path"]), f, "image/png")},
            data={"reqtype": "fileupload"},
            timeout=30,
        )

    if resp.status_code == 200 and resp.text.startswith("https://"):
        eq["catbox_url"] = resp.text.strip()
        print(f"  {eq['id']}: {eq['catbox_url']}")
    else:
        print(f"  ERROR uploading {eq['id']}: {resp.status_code} {resp.text[:100]}")
        eq["catbox_url"] = None

    time.sleep(1)

# Save map for debugging / reuse
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(equations, f, indent=2, ensure_ascii=False)
print(f"\nEquation map saved to {MAP_FILE}")

# ── Step 4: Find equation paragraphs in Google Doc and replace ──
doc = service.documents().get(documentId=DOC_ID).execute()

def iter_paragraphs(doc):
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style

# Build search patterns: for each equation, derive a text fragment
# that would appear in the Google Doc (LaTeX rendered as plain text)
def make_search_fragments(eq):
    """Generate text fragments to search for in the doc.
    The doc may show LaTeX as-is or partially rendered."""
    latex = eq["latex"]
    fragments = []

    # Try the tag number as primary identifier
    tag_match = re.search(r'\\tag\{([^}]+)\}', latex)
    if tag_match:
        tag_num = tag_match.group(1)
        # Various ways the tag might appear
        fragments.append(f"\\tag{{{tag_num}}}")
        fragments.append(f"(tag{{{tag_num}}})")
        fragments.append(f"({tag_num})")

    # Also try key distinctive parts of the formula
    # Remove \tag{...} and extract the core expression
    core = re.sub(r'\\tag\{[^}]+\}', '', latex).strip()
    # Take first 30 chars as a fragment
    if len(core) > 10:
        fragments.append(core[:30])

    return fragments

# Collect all doc paragraphs that look like equations
eq_paragraphs = []
for start, end, text, style in iter_paragraphs(doc):
    stripped = text.strip()
    if not stripped:
        continue
    # Check for LaTeX markers
    has_latex = any(marker in stripped for marker in [
        '\\frac', '\\tag', '\\text{', '\\cdot', '\\Delta',
        '\\mathbb', '\\left', '\\leq', '\\geq', '\\min',
        '\\sigma', '\\hat', '= \\frac',
        'E(A) =', "R_A'", "R_B'", "K_A =", "K_{",
        'NLG =', 'PTM =', 'TFM(', 'AUC-ROC',
        'R(t)', "S' = S", "S' = w",
    ])
    if has_latex and len(stripped) < 500:  # Equations are typically short
        eq_paragraphs.append({
            "start": start,
            "end": end,
            "text": stripped,
        })

print(f"\nFound {len(eq_paragraphs)} equation-like paragraphs in the doc:")
for p in eq_paragraphs:
    print(f"  [{p['start']},{p['end']}): {p['text'][:80]}...")

# Match doc paragraphs to our equation list
def match_equation(doc_para, equations):
    """Find which equation from our list matches this doc paragraph."""
    doc_text = doc_para["text"]
    for eq in equations:
        if not eq.get("catbox_url"):
            continue
        fragments = make_search_fragments(eq)
        for frag in fragments:
            if frag in doc_text:
                return eq
        # Fuzzy: check if key parts of the equation appear
        latex = eq["latex"]
        # Remove LaTeX commands and check if the "skeleton" matches
        skeleton = re.sub(r'\\[a-zA-Z]+', '', latex)
        skeleton = skeleton.replace('{', '').replace('}', '')[:20]
        if len(skeleton) > 5 and skeleton in doc_text:
            return eq
    return None

# Match and prepare replacements
replacements = []
used_eqs = set()
for p in eq_paragraphs:
    eq = match_equation(p, equations)
    if eq and eq["id"] not in used_eqs:
        replacements.append({
            "para": p,
            "eq": eq,
        })
        used_eqs.add(eq["id"])
        print(f"  MATCH: [{p['start']}] '{p['text'][:50]}...' -> {eq['id']}")
    else:
        print(f"  NO MATCH: [{p['start']}] '{p['text'][:50]}...'")

print(f"\n{len(replacements)} equations matched for replacement.")

# Process replacements in REVERSE order (highest index first)
replacements.sort(key=lambda r: r["para"]["start"], reverse=True)

# Target width for equations in the doc: ~400pt (about 70% of text width)
TARGET_WIDTH_PT = 380
MAX_HEIGHT_PT = 60

for rep in replacements:
    para = rep["para"]
    eq = rep["eq"]

    # Calculate proportional dimensions
    aspect = eq["height_px"] / eq["width_px"]
    width_pt = min(TARGET_WIDTH_PT, eq["width_px"] * 72 / DPI)  # Convert px to pt at DPI
    height_pt = width_pt * aspect
    if height_pt > MAX_HEIGHT_PT:
        height_pt = MAX_HEIGHT_PT
        width_pt = height_pt / aspect

    requests_batch = [
        # Delete the text content (keep the paragraph structure)
        {
            "deleteContentRange": {
                "range": {
                    "startIndex": para["start"],
                    "endIndex": para["end"] - 1,  # Keep trailing newline
                }
            }
        },
        # Insert inline image at the same position
        {
            "insertInlineImage": {
                "location": {"index": para["start"]},
                "uri": eq["catbox_url"],
                "objectSize": {
                    "width": {"magnitude": width_pt, "unit": "PT"},
                    "height": {"magnitude": height_pt, "unit": "PT"},
                },
            }
        },
        # Center the paragraph
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": para["start"],
                    "endIndex": para["start"] + 1,
                },
                "paragraphStyle": {
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 8, "unit": "PT"},
                    "spaceBelow": {"magnitude": 8, "unit": "PT"},
                },
                "fields": "alignment,spaceAbove,spaceBelow",
            }
        },
    ]

    try:
        result = service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": requests_batch}
        ).execute()
        print(f"  INSERTED {eq['id']} at index {para['start']} ({width_pt:.0f}x{height_pt:.0f}pt)")
    except Exception as e:
        print(f"  ERROR inserting {eq['id']}: {e}")

    # Re-read doc after each insertion to get fresh indices
    doc = service.documents().get(documentId=DOC_ID).execute()
    time.sleep(2)

# ── Step 5: Final count ──
print(f"\nDone. {len(replacements)} equations replaced with images.")
print("Unmatched equations (may need manual check):")
for eq in equations:
    if eq["id"] not in used_eqs:
        print(f"  {eq['id']}: {eq['latex'][:60]}...")
