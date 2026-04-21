"""
Re-export all thesis visuals from HTML sources at 2x resolution using Playwright,
upload to freeimage.host, and replace in Google Doc.
"""
import asyncio
import base64
import importlib.util
import io
import json
import os
import re
import sys
import time

import requests as http_requests
from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Google Docs auth
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
gdoc_service = m.get_docs_service()
DOC_ID = m.DOC_ID

HTML_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/html"
PNG_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png"
FREEIMAGE_KEY = "6d207e02198a847aa98d0a2a901485a5"

# Map HTML file -> expected catbox URL in the doc (from VISUAL-GUIDE.md)
# We'll match by filename pattern instead


async def export_all_html_to_png():
    """Export all HTML visuals to high-res PNGs using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900},
            device_scale_factor=2,  # 2x DPI = 2800px effective width
        )
        page = await context.new_page()

        html_files = sorted(f for f in os.listdir(HTML_DIR) if f.endswith(".html"))
        results = []

        for fname in html_files:
            html_path = os.path.join(HTML_DIR, fname)
            png_name = fname.replace(".html", ".png")
            png_path = os.path.join(PNG_DIR, png_name)

            url = f"file:///{html_path.replace(os.sep, '/')}"
            try:
                await page.goto(url, wait_until="networkidle", timeout=10000)
                await page.wait_for_timeout(500)
                await page.screenshot(path=png_path, full_page=True, type="png")

                from PIL import Image
                img = Image.open(png_path)
                w, h = img.size
                print(f"  {fname:55s} -> {w}x{h}px")
                results.append({"html": fname, "png": png_name, "png_path": png_path, "w": w, "h": h})
            except Exception as e:
                print(f"  {fname:55s} -> ERROR: {e}")

        await browser.close()
        return results


def upload_to_freeimage(png_path):
    """Upload PNG to freeimage.host and return URL."""
    for attempt in range(3):
        try:
            with open(png_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
            resp = http_requests.post(
                "https://freeimage.host/api/1/upload",
                data={"key": FREEIMAGE_KEY, "source": img_b64, "format": "json"},
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                url = data.get("image", {}).get("url", "")
                if url:
                    return url
            print(f"    Upload attempt {attempt + 1}: {resp.status_code}")
        except Exception as e:
            print(f"    Upload attempt {attempt + 1}: {e}")
        time.sleep(3)
    return None


def get_doc():
    return gdoc_service.documents().get(documentId=DOC_ID).execute()


def find_images_in_doc(doc):
    """Find all inline images with their catbox URLs and doc positions."""
    images = []
    inline_objs = doc.get("inlineObjects", {})

    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        si = elem.get("startIndex", 0)
        ei = elem.get("endIndex", 0)

        for el in para.get("elements", []):
            if "inlineObjectElement" not in el:
                continue
            obj_id = el["inlineObjectElement"].get("inlineObjectId", "")
            if obj_id not in inline_objs:
                continue

            props = inline_objs[obj_id].get("inlineObjectProperties", {}).get("embeddedObject", {})
            uri = props.get("imageProperties", {}).get("sourceUri", "")
            w = props.get("size", {}).get("width", {}).get("magnitude", 0)
            h = props.get("size", {}).get("height", {}).get("magnitude", 0)

            # Only catbox images (our figures/tables)
            if "catbox.moe" in uri and w > 200:
                images.append({
                    "obj_id": obj_id,
                    "para_start": si,
                    "para_end": ei,
                    "uri": uri,
                    "w_pt": w,
                    "h_pt": h,
                    "el_start": el.get("startIndex", si),
                    "el_end": el.get("endIndex", ei),
                })

    return images


def match_visual_to_doc_image(visual_name, doc_images, visual_guide):
    """Match a visual filename to its doc image using VISUAL-GUIDE.md catbox URLs."""
    # Try matching by catbox URL from VISUAL-GUIDE
    for url_entry in visual_guide:
        if visual_name in url_entry.get("html", ""):
            target_url = url_entry.get("catbox_url", "")
            for di in doc_images:
                if target_url and target_url in di["uri"]:
                    return di
    return None


# ══════════════════════════════════════════════
# STEP 1: Re-export all HTMLs at 2x DPI
# ══════════════════════════════════════════════
print("=== STEP 1: Re-export HTMLs at 2x DPI ===")
visuals = asyncio.run(export_all_html_to_png())
print(f"Exported {len(visuals)} visuals\n")

# ══════════════════════════════════════════════
# STEP 2: Upload to freeimage.host
# ══════════════════════════════════════════════
print("=== STEP 2: Upload to freeimage.host ===")
for v in visuals:
    url = upload_to_freeimage(v["png_path"])
    v["new_url"] = url
    if url:
        print(f"  {v['png'][:45]:45s} -> {url}")
    else:
        print(f"  {v['png'][:45]:45s} -> FAILED")
    time.sleep(1)

# Save mapping
with open(os.path.join(PNG_DIR, "hires_upload_map.json"), "w") as f:
    json.dump(visuals, f, indent=2)
print(f"\nUploaded {sum(1 for v in visuals if v.get('new_url'))} / {len(visuals)}\n")

# ══════════════════════════════════════════════
# STEP 3: Read VISUAL-GUIDE.md for catbox URL mapping
# ══════════════════════════════════════════════
print("=== STEP 3: Match visuals to doc images ===")
guide_path = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/VISUAL-GUIDE.md"
with open(guide_path, "r", encoding="utf-8") as f:
    guide_content = f.read()

# Parse catbox URLs from VISUAL-GUIDE
visual_guide = []
current_html = ""
for line in guide_content.split("\n"):
    # Match HTML filename
    html_match = re.search(r"(ch\d+-[a-z0-9-]+\.html)", line)
    if html_match:
        current_html = html_match.group(1)
    # Match catbox URL
    url_match = re.search(r"(https://files\.catbox\.moe/\w+\.png)", line)
    if url_match and current_html:
        visual_guide.append({"html": current_html, "catbox_url": url_match.group(1)})

print(f"Found {len(visual_guide)} visual->catbox mappings in VISUAL-GUIDE.md")

doc = get_doc()
doc_images = find_images_in_doc(doc)
print(f"Found {len(doc_images)} catbox figure images in doc")

# Match each visual to its doc image
matches = []
for v in visuals:
    if not v.get("new_url"):
        continue
    html_name = v["html"]
    doc_img = match_visual_to_doc_image(html_name, doc_images, visual_guide)
    if doc_img:
        matches.append({"visual": v, "doc_img": doc_img})
        print(f"  MATCH: {html_name[:40]:40s} -> doc[{doc_img['para_start']}] ({doc_img['uri'][-12:]})")
    else:
        print(f"  NO MATCH: {html_name}")

print(f"\n{len(matches)} matches ready for replacement\n")

# ══════════════════════════════════════════════
# STEP 4: Replace images in doc (bottom-first)
# ══════════════════════════════════════════════
print("=== STEP 4: Replace images in doc ===")
matches.sort(key=lambda m: m["doc_img"]["para_start"], reverse=True)

for match in matches:
    v = match["visual"]
    di = match["doc_img"]

    # Re-read doc for fresh indices
    doc = get_doc()

    # Find the image paragraph again by obj_id
    found_para = None
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        for el in elem["paragraph"].get("elements", []):
            if "inlineObjectElement" in el:
                if el["inlineObjectElement"].get("inlineObjectId") == di["obj_id"]:
                    found_para = elem
                    break
        if found_para:
            break

    if not found_para:
        print(f"  SKIP (not found): {v['png']}")
        continue

    si = found_para["startIndex"]
    ei = found_para["endIndex"]

    # Calculate display size: keep same width as before, adjust height by new aspect ratio
    new_aspect = v["h"] / v["w"]
    display_w = di["w_pt"]  # Keep same display width
    display_h = display_w * new_aspect

    reqs = [
        # Delete old image (the inline object element, not the whole paragraph)
        {"deleteContentRange": {"range": {"startIndex": si, "endIndex": ei - 1}}},
        # Insert new higher-res image
        {"insertInlineImage": {
            "location": {"index": si},
            "uri": v["new_url"],
            "objectSize": {
                "width": {"magnitude": display_w, "unit": "PT"},
                "height": {"magnitude": display_h, "unit": "PT"},
            },
        }},
        # Re-center
        {"updateParagraphStyle": {
            "range": {"startIndex": si, "endIndex": si + 1},
            "paragraphStyle": {"alignment": "CENTER"},
            "fields": "alignment",
        }},
    ]

    try:
        gdoc_service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
        print(f"  REPLACED [{si}] {v['png'][:40]:40s} {display_w:.0f}x{display_h:.0f}pt")
    except Exception as e:
        print(f"  ERROR [{si}] {v['png'][:40]}: {e}")

    time.sleep(2)

print(f"\nDone. {len(matches)} images replaced with high-res versions.")
