"""
Render all code blocks from thesis markdown as PNG images (Pygments),
upload to Catbox, find matching paragraphs in Google Doc, and replace.
"""
import importlib.util
import io
import json
import os
import re
import sys
import time

import requests as http_requests
from PIL import Image
from pygments import highlight
from pygments.lexers import PythonLexer, SqlLexer, TextLexer
from pygments.formatters import ImageFormatter

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

TMP_DIR = "C:/tmp/equations"
os.makedirs(TMP_DIR, exist_ok=True)

# ── Load code blocks ──
with open(f"{TMP_DIR}/code_blocks.json", "r", encoding="utf-8") as f:
    blocks = json.load(f)

LEXERS = {
    "python": PythonLexer(),
    "sql": SqlLexer(),
    "text": TextLexer(),
}

FORMATTER = ImageFormatter(
    font_name="Consolas",
    font_size=26,
    line_numbers=True,
    line_number_bg="#f8f8f8",
    line_number_fg="#999999",
    line_number_separator=True,
    style="friendly",
    image_pad=16,
    line_pad=4,
)

# ── Step 1: Render all blocks to PNG ──
print("=== RENDERING ===")
for i, block in enumerate(blocks):
    lexer = LEXERS.get(block["lang"], TextLexer())
    img_data = highlight(block["code"], lexer, FORMATTER)
    png_path = os.path.join(TMP_DIR, f"code_block_{i+1}.png")
    with open(png_path, "wb") as f:
        f.write(img_data)
    img = Image.open(png_path)
    block["png_path"] = png_path
    block["width_px"] = img.width
    block["height_px"] = img.height
    print(f"  [{i+1}] {img.width}x{img.height}px | {block['first_line'][:60]}")

# ── Step 2: Upload to Catbox ──
print("\n=== UPLOADING (freeimage.host) ===")
import base64

FREEIMAGE_KEY = "6d207e02198a847aa98d0a2a901485a5"

for i, block in enumerate(blocks):
    success = False
    for attempt in range(3):
        try:
            with open(block["png_path"], "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            resp = http_requests.post(
                "https://freeimage.host/api/1/upload",
                data={"key": FREEIMAGE_KEY, "source": img_b64, "format": "json"},
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                url = data.get("image", {}).get("url", "")
                if url:
                    block["image_url"] = url
                    print(f"  [{i+1}] {url}")
                    success = True
                    break
            print(f"  [{i+1}] attempt {attempt+1}: {resp.status_code}")
        except Exception as e:
            print(f"  [{i+1}] attempt {attempt+1} error: {e}")
        time.sleep(3)
    if not success:
        print(f"  [{i+1}] UPLOAD FAILED")
        block["image_url"] = None
    time.sleep(1)

# Save updated map
with open(f"{TMP_DIR}/code_blocks.json", "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=2, ensure_ascii=False)

# ── Step 3: Find and replace in Google Doc ──
print("\n=== REPLACING IN DOC ===")


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def get_paragraphs(doc):
    """Return list of (startIndex, endIndex, text, has_bg, has_img)."""
    result = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        has_img = False
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
            if "inlineObjectElement" in el:
                has_img = True
        shading = para.get("paragraphStyle", {}).get("shading", {})
        has_bg = bool(shading.get("backgroundColor"))
        result.append({
            "start": elem["startIndex"],
            "end": elem["endIndex"],
            "text": text.rstrip("\n"),
            "has_bg": has_bg,
            "has_img": has_img,
        })
    return result


def normalize(s):
    """Normalize whitespace for fuzzy matching."""
    return re.sub(r"\s+", " ", s.strip())


def find_code_block_range(doc_paras, block):
    """Find the start/end indices of a code block in the doc.
    Restrict search to Chapter 4 area (index > 140000)."""
    code_lines = block["code"].split("\n")
    first_norm = normalize(code_lines[0])
    last_norm = normalize(code_lines[-1])

    # Find paragraph matching first line — require strong match
    start_idx = None
    start_para_idx = None
    for pi, p in enumerate(doc_paras):
        # Only search in Chapter 4 area
        if p["start"] < 140000:
            continue
        if p["has_img"]:
            continue
        p_norm = normalize(p["text"])
        # Require first 25+ chars to match exactly
        match_len = min(25, len(first_norm))
        if match_len < 5:
            continue
        if first_norm[:match_len] == p_norm[:match_len]:
            start_idx = p["start"]
            start_para_idx = pi
            break

    if start_idx is None:
        return None, None

    # Scan forward from start to find last line
    end_idx = None
    for pi in range(start_para_idx, min(start_para_idx + len(code_lines) + 5, len(doc_paras))):
        p = doc_paras[pi]
        p_norm = normalize(p["text"])
        match_len = min(20, len(last_norm))
        if match_len >= 5 and last_norm[:match_len] == p_norm[:match_len]:
            end_idx = p["end"]
            break

    # If last line not found, estimate from line count
    if end_idx is None:
        est_end = min(start_para_idx + len(code_lines) + 2, len(doc_paras) - 1)
        end_idx = doc_paras[est_end]["end"]

    # Extend start backwards to include preceding non-BG line if it's the SQL opening bracket
    if start_para_idx > 0:
        prev = doc_paras[start_para_idx - 1]
        prev_stripped = prev["text"].strip()
        if prev_stripped.endswith("(") and len(prev_stripped) < 50:
            start_idx = prev["start"]

    # Extend end forward to include closing ")" bracket
    for pi in range(start_para_idx, min(start_para_idx + len(code_lines) + 5, len(doc_paras))):
        p = doc_paras[pi]
        if p["text"].strip() == ")":
            end_idx = p["end"]
            break

    return start_idx, end_idx


# Process blocks in reverse order (bottom to top) to preserve indices
blocks_with_urls = [b for b in blocks if b.get("image_url")]
print(f"Processing {len(blocks_with_urls)} blocks with Catbox URLs")

# First pass: find all ranges
doc = get_doc()
doc_paras = get_paragraphs(doc)

for block in blocks_with_urls:
    start, end = find_code_block_range(doc_paras, block)
    block["doc_start"] = start
    block["doc_end"] = end
    if start is not None and end is not None and start > 100:
        print(f"  FOUND [{start}-{end}]: {block['first_line'][:60]}")
    else:
        print(f"  NOT FOUND: {block['first_line'][:60]}")
        block["doc_start"] = None
        block["doc_end"] = None

# Sort by doc_start descending (process bottom-first)
replaceable = [b for b in blocks_with_urls if b.get("doc_start") and b.get("doc_end")]
replaceable.sort(key=lambda b: b["doc_start"], reverse=True)

print(f"\n{len(replaceable)} blocks to replace (bottom-first):")

for block in replaceable:
    # Re-read doc for fresh indices
    doc = get_doc()
    doc_paras = get_paragraphs(doc)

    # Re-find the range (indices may have shifted)
    start, end = find_code_block_range(doc_paras, block)
    if not start or not end:
        print(f"  SKIP (lost): {block['first_line'][:50]}")
        continue

    # Calculate image size: fit to page width (~470pt usable), maintain aspect
    aspect = block["height_px"] / block["width_px"]
    width_pt = min(460, block["width_px"] * 72 / 144)  # 144 DPI equivalent
    height_pt = width_pt * aspect

    reqs = [
        # Delete the code text range
        {
            "deleteContentRange": {
                "range": {"startIndex": start, "endIndex": end - 1}
            }
        },
        # Insert the image
        {
            "insertInlineImage": {
                "location": {"index": start},
                "uri": block["image_url"],
                "objectSize": {
                    "width": {"magnitude": width_pt, "unit": "PT"},
                    "height": {"magnitude": height_pt, "unit": "PT"},
                },
            }
        },
        # Center the paragraph + add spacing
        {
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": start + 1},
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
        service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": reqs}
        ).execute()
        print(f"  REPLACED [{start}] {width_pt:.0f}x{height_pt:.0f}pt | {block['first_line'][:50]}")
    except Exception as e:
        print(f"  ERROR [{start}]: {e}")

    time.sleep(2)

print(f"\nDone. {len(replaceable)} code blocks replaced with images.")
