"""
gdoc-write-replace-all-images: Upload 32 hi-res PNGs to freeimage.host,
then replace corresponding low-res images in the thesis Google Doc.

Usage: python gdoc-write-replace-all-images.py
"""
import warnings
warnings.filterwarnings("ignore")

import os, sys, json, time, base64, glob, re, importlib, requests
from pathlib import Path

# ── Auth via importlib ──────────────────────────────────────────────
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    r"C:\Users\duong\WebstormProjects\Thesis\scripts\gdoc-util-auth.py",
)
auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auth)

DOC_ID = auth.DOC_ID
service = auth.get_docs_service()

PNG_DIR = r"C:\Users\duong\WebstormProjects\Thesis\documents\thesis-chapters\visuals\png"
VISUAL_GUIDE = r"C:\Users\duong\WebstormProjects\Thesis\documents\thesis-chapters\visuals\VISUAL-GUIDE.md"
UPLOAD_MAP_PATH = os.path.join(PNG_DIR, "hires_upload_map_freeimage.json")

FREEIMAGE_API = "https://freeimage.host/api/1/upload"
FREEIMAGE_KEY = "6d207e02198a847aa98d0a2a901485a5"

# ── STEP 1: Upload all PNGs to freeimage.host ──────────────────────
def upload_to_freeimage(png_path, retries=3, delay=5):
    """Upload a PNG to freeimage.host, return the image URL."""
    with open(png_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    for attempt in range(retries):
        try:
            resp = requests.post(
                FREEIMAGE_API,
                data={"key": FREEIMAGE_KEY, "source": b64, "format": "json"},
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status_code") == 200:
                    url = data["image"]["url"]
                    print(f"  OK: {url}")
                    return url
                else:
                    print(f"  API error: {data.get('status_txt', 'unknown')}")
            else:
                print(f"  HTTP {resp.status_code}")
        except Exception as e:
            print(f"  Exception: {e}")

        if attempt < retries - 1:
            print(f"  Retrying in {delay}s... (attempt {attempt+2}/{retries})")
            time.sleep(delay)

    return None


def step1_upload_all():
    """Upload all PNGs, return and save mapping."""
    # Load existing map if any
    upload_map = {}
    if os.path.exists(UPLOAD_MAP_PATH):
        with open(UPLOAD_MAP_PATH, "r") as f:
            upload_map = json.load(f)
        print(f"Loaded existing map with {len(upload_map)} entries")

    png_files = sorted(glob.glob(os.path.join(PNG_DIR, "*.png")))
    # Exclude test files
    png_files = [p for p in png_files if "test_" not in os.path.basename(p)]

    print(f"\n=== STEP 1: Uploading {len(png_files)} PNGs to freeimage.host ===\n")

    for i, png_path in enumerate(png_files):
        name = os.path.basename(png_path)
        if name in upload_map and upload_map[name].get("freeimage_url"):
            print(f"[{i+1}/{len(png_files)}] SKIP (already uploaded): {name}")
            continue

        print(f"[{i+1}/{len(png_files)}] Uploading: {name}")
        url = upload_to_freeimage(png_path)

        if url:
            upload_map[name] = upload_map.get(name, {})
            upload_map[name]["freeimage_url"] = url
            upload_map[name]["png_path"] = png_path
            # Save after each upload
            with open(UPLOAD_MAP_PATH, "w") as f:
                json.dump(upload_map, f, indent=2)
        else:
            print(f"  FAILED to upload {name}")

        # Rate limit
        time.sleep(1)

    print(f"\nUpload complete. {sum(1 for v in upload_map.values() if v.get('freeimage_url'))} successful.")
    return upload_map


# ── STEP 2: Build catbox/iili URL -> PNG name mapping ──────────────
def parse_visual_guide():
    """Parse VISUAL-GUIDE.md to build mapping: catbox_url -> png_name."""
    url_to_png = {}
    with open(VISUAL_GUIDE, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all entries with Catbox URL and PNG Export
    # Pattern: look for PNG Export line followed by Catbox URL line
    blocks = content.split("### Visual")
    for block in blocks:
        png_match = re.search(r'\*\*PNG Export:\*\*\s*`png/([^`]+)`', block)
        catbox_match = re.search(r'\*\*Catbox URL:\*\*\s*(https?://\S+)', block)

        if png_match and catbox_match:
            png_name = png_match.group(1)
            catbox_url = catbox_match.group(1).strip()
            url_to_png[catbox_url] = png_name

    print(f"\nParsed VISUAL-GUIDE: {len(url_to_png)} catbox URL -> PNG mappings")
    return url_to_png


# ── Load previous iili.io map for matching already-replaced images ──
def load_iili_map():
    """Load old iili.io upload map to match already-replaced images."""
    old_map_path = os.path.join(PNG_DIR, "hires_upload_map.json")
    iili_to_png = {}
    if os.path.exists(old_map_path):
        with open(old_map_path, "r") as f:
            old_data = json.load(f)
        for entry in old_data:
            if isinstance(entry, dict) and entry.get("new_url") and entry.get("png"):
                iili_to_png[entry["new_url"]] = entry["png"]
    print(f"Loaded iili.io map: {len(iili_to_png)} entries")
    return iili_to_png


# ── STEP 3: Find and replace images in the doc ─────────────────────
def get_inline_images(doc):
    """Extract all inline images from the document with their positions and sizes."""
    images = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        for el in para.get("elements", []):
            if "inlineObjectElement" in el:
                obj_id = el["inlineObjectElement"]["inlineObjectId"]
                start_idx = el["startIndex"]
                end_idx = el["endIndex"]

                # Get image properties from inlineObjects
                inline_obj = doc.get("inlineObjects", {}).get(obj_id, {})
                props = inline_obj.get("inlineObjectProperties", {})
                embedded = props.get("embeddedObject", {})

                source_url = embedded.get("imageProperties", {}).get("sourceUri", "")
                # Also check contentUri
                content_uri = embedded.get("imageProperties", {}).get("contentUri", "")

                # Get size
                size = embedded.get("size", {})
                w_mag = size.get("width", {}).get("magnitude", 0)
                w_unit = size.get("width", {}).get("unit", "PT")
                h_mag = size.get("height", {}).get("magnitude", 0)
                h_unit = size.get("height", {}).get("unit", "PT")

                # Get paragraph start/end for the containing paragraph
                para_start = elem["startIndex"]
                para_end = elem["endIndex"]

                images.append({
                    "obj_id": obj_id,
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                    "para_start": para_start,
                    "para_end": para_end,
                    "source_url": source_url or content_uri,
                    "content_uri": content_uri,
                    "w_pt": w_mag,
                    "h_pt": h_mag,
                    "w_unit": w_unit,
                    "h_unit": h_unit,
                })
    return images


def get_png_dimensions(png_path):
    """Read PNG dimensions from the file header."""
    with open(png_path, "rb") as f:
        f.read(16)  # Skip signature + IHDR chunk type
        width = int.from_bytes(f.read(4), "big")
        height = int.from_bytes(f.read(4), "big")
    return width, height


def replace_image(service, doc_id, image_info, new_url, png_path):
    """Replace an inline image: delete old, insert new with correct sizing."""
    start_idx = image_info["start_idx"]
    end_idx = image_info["end_idx"]
    old_w_pt = image_info["w_pt"]
    old_h_pt = image_info["h_pt"]

    # Get new image aspect ratio from PNG
    png_w, png_h = get_png_dimensions(png_path)
    aspect = png_h / png_w if png_w > 0 else 1.0

    # Keep same width, calculate new height from aspect ratio
    new_w_pt = old_w_pt
    new_h_pt = new_w_pt * aspect

    requests_body = [
        # 1. Delete old image
        {
            "deleteContentRange": {
                "range": {
                    "startIndex": start_idx,
                    "endIndex": end_idx,
                }
            }
        },
        # 2. Insert new image at the same position
        {
            "insertInlineImage": {
                "uri": new_url,
                "location": {
                    "index": start_idx,
                },
                "objectSize": {
                    "width": {"magnitude": new_w_pt, "unit": "PT"},
                    "height": {"magnitude": new_h_pt, "unit": "PT"},
                },
            }
        },
        # 3. Center the paragraph and set spacing
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": start_idx,
                    "endIndex": start_idx + 1,
                },
                "paragraphStyle": {
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 18, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "alignment,spaceAbove,spaceBelow",
            }
        },
    ]

    result = service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": requests_body},
    ).execute()

    return result


def step3_replace_images(upload_map, url_to_png, iili_to_png):
    """Find all inline images in the doc and replace matches."""
    print("\n=== STEP 3: Replacing images in the document ===\n")

    # Build reverse map: png_name -> freeimage_url
    png_to_freeimage = {}
    for png_name, data in upload_map.items():
        if data.get("freeimage_url"):
            png_to_freeimage[png_name] = data["freeimage_url"]

    # Read the document
    doc = auth.get_document(service, DOC_ID)
    images = get_inline_images(doc)
    print(f"Found {len(images)} inline images in the document")

    # Match images to PNGs
    matches = []
    for img in images:
        # Skip small images (equations, icons)
        if img["w_pt"] <= 200:
            continue

        source = img["source_url"]
        png_name = None

        # Try matching catbox URL
        if "catbox.moe" in source:
            png_name = url_to_png.get(source)
            if not png_name:
                # Try without trailing whitespace
                for url, name in url_to_png.items():
                    if url.strip() == source.strip():
                        png_name = name
                        break

        # Try matching iili.io URL (from previous batch)
        if not png_name and "iili.io" in source:
            png_name = iili_to_png.get(source)
            if not png_name:
                for url, name in iili_to_png.items():
                    if url.strip() == source.strip():
                        png_name = name
                        break

        # Try matching freeimage.host URL (already replaced in previous run of this script)
        if not png_name and "freeimage.host" in source:
            # Already has a freeimage URL -- skip
            print(f"  Already freeimage: idx={img['start_idx']} w={img['w_pt']:.0f}pt url={source[:60]}...")
            continue

        if png_name and png_name in png_to_freeimage:
            png_path = os.path.join(PNG_DIR, png_name)
            if os.path.exists(png_path):
                matches.append({
                    "image": img,
                    "png_name": png_name,
                    "png_path": png_path,
                    "freeimage_url": png_to_freeimage[png_name],
                })
            else:
                print(f"  PNG not found: {png_name}")
        elif png_name:
            print(f"  No freeimage URL for: {png_name}")
        else:
            print(f"  UNMATCHED image: idx={img['start_idx']} w={img['w_pt']:.0f}pt url={source[:80]}...")

    print(f"\nMatched {len(matches)} images for replacement")

    # Sort bottom-to-top (highest index first) to preserve indices
    matches.sort(key=lambda m: m["image"]["start_idx"], reverse=True)

    replaced = 0
    failed = 0

    for i, match in enumerate(matches):
        img = match["image"]
        png_name = match["png_name"]
        freeimage_url = match["freeimage_url"]
        png_path = match["png_path"]

        print(f"\n[{i+1}/{len(matches)}] Replacing: {png_name}")
        print(f"  Old URL: {img['source_url'][:60]}...")
        print(f"  New URL: {freeimage_url}")
        print(f"  Position: idx={img['start_idx']}, size={img['w_pt']:.0f}x{img['h_pt']:.0f}pt")

        try:
            replace_image(service, DOC_ID, img, freeimage_url, png_path)
            replaced += 1
            print(f"  SUCCESS")
        except Exception as e:
            failed += 1
            print(f"  FAILED: {e}")

        # Sleep between replacements
        time.sleep(2)

        # Re-read the document to get updated indices
        if i < len(matches) - 1:
            doc = auth.get_document(service, DOC_ID)
            images = get_inline_images(doc)

            # Re-match the next image (update indices)
            for j in range(i+1, len(matches)):
                next_match = matches[j]
                next_source = next_match["image"]["source_url"]
                # Find the image with matching source URL
                found = False
                for updated_img in images:
                    if updated_img["w_pt"] <= 200:
                        continue
                    if updated_img["source_url"] == next_source:
                        matches[j]["image"] = updated_img
                        found = True
                        break
                if not found:
                    # Try content URI
                    for updated_img in images:
                        if updated_img["w_pt"] <= 200:
                            continue
                        if updated_img["content_uri"] == next_source or updated_img["source_url"] == next_source:
                            matches[j]["image"] = updated_img
                            found = True
                            break
                if not found:
                    print(f"  WARNING: Could not re-find image for {matches[j]['png_name']} after re-read")

    return replaced, failed, len(matches)


# ── STEP 4: Verify ─────────────────────────────────────────────────
def step4_verify():
    """Count remaining old vs new images."""
    print("\n=== STEP 4: Verification ===\n")

    doc = auth.get_document(service, DOC_ID)
    images = get_inline_images(doc)

    catbox = 0
    iili = 0
    freeimage = 0
    other = 0
    small_skipped = 0

    for img in images:
        if img["w_pt"] <= 200:
            small_skipped += 1
            continue
        src = img["source_url"]
        if "catbox.moe" in src:
            catbox += 1
            print(f"  CATBOX remaining: idx={img['start_idx']} w={img['w_pt']:.0f}pt {src[:60]}")
        elif "iili.io" in src:
            iili += 1
            print(f"  IILI.IO remaining: idx={img['start_idx']} w={img['w_pt']:.0f}pt {src[:60]}")
        elif "freeimage" in src or "iili" in src:
            freeimage += 1
        else:
            other += 1
            print(f"  OTHER: idx={img['start_idx']} w={img['w_pt']:.0f}pt {src[:60]}")

    print(f"\n--- Image Count Summary ---")
    print(f"  Freeimage.host (new):  {freeimage}")
    print(f"  Catbox.moe (old):      {catbox}")
    print(f"  iili.io (prev batch):  {iili}")
    print(f"  Other:                 {other}")
    print(f"  Small (skipped):       {small_skipped}")
    print(f"  Total large images:    {catbox + iili + freeimage + other}")

    return catbox, iili, freeimage


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Step 1: Upload
    upload_map = step1_upload_all()

    # Step 2: Build URL mappings
    url_to_png = parse_visual_guide()
    iili_to_png = load_iili_map()

    # Step 3: Replace
    replaced, failed, total = step3_replace_images(upload_map, url_to_png, iili_to_png)

    print(f"\n=== REPLACEMENT SUMMARY ===")
    print(f"  Total matched: {total}")
    print(f"  Replaced:      {replaced}")
    print(f"  Failed:        {failed}")

    # Step 4: Verify
    step4_verify()
