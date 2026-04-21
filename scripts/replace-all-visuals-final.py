"""
Upload all 32 hi-res PNGs to freeimage.host and replace ALL matching images in Google Doc.
Uses 3 matching strategies: catbox URL, iili.io URL, and caption-based.
"""
import importlib.util
import io
import json
import os
import re
import sys
import time
import base64

import requests as http_requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
service = m.get_docs_service()
DOC_ID = m.DOC_ID

PNG_DIR = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/png"
GUIDE_PATH = "C:/Users/duong/WebstormProjects/Thesis/documents/thesis-chapters/visuals/VISUAL-GUIDE.md"
FREEIMAGE_KEY = "6d207e02198a847aa98d0a2a901485a5"

# Caption text -> PNG filename mapping (comprehensive)
CAPTION_TO_PNG = {
    "Table 1.1": "ch1-platform-comparison-table",
    "Figure 1.1": "ch1-research-gap-diagram",
    "Figure 1.2": "ch1-closed-loop-workflow",
    "Figure 1.3": "ch1-five-layer-architecture-overview",
    "Figure 1.4": "ch1-thesis-structure-roadmap",
    "Figure 2.1": "ch2-literature-landscape-map",
    "Table 2.1": "ch2-kt-evolution-timeline",
    "Table 2.2": "ch2-detailed-comparison-table",
    "Table 2.3": "ch2-technique-complementarity-table",
    "Figure 2.2": "ch2-spaced-repetition-evolution",
    "Figure 3.1": "ch3-system-architecture-diagram",
    "Table 3.1": "ch3-functional-requirements-table",
    "Table 3.2": "ch3-requirements-traceability-table",
    "Figure 3.2": "ch3-knowledge-graph-diagram",
    "Table 3.3": "ch3-hyperparameter-summary-table",
    "Figure 3.3": "ch3-recommendation-sequence-diagram",
    "Figure 3.4": "ch3-submission-processing-flow",
    "Figure 3.5": "ch3-database-schema-erd",
    "Figure 3.6": "ch3-layer-interaction-matrix",
    "Figure 3.7": "ch3-cold-start-flowchart",
    "Table 3.5": "ch3-caching-strategy-table",
    "Table 4.1": "ch4-tech-stack-table",
    "Table 4.2": "ch4-bkt-params-table",
    "Figure 4.1": "ch4-adaptive-engine-sequence",
    "Figure 4.2": "ch4-bkt-state-transition",
    "Figure 4.3": "ch4-mab-decision-flow",
    "Figure 4.4": "ch4-fsrs-card-lifecycle",
    "Figure 4.5": "ch4-fsrs-retrievability-curve",
    "Table 5.1": "ch5-research-questions-table",
    "Figure 5.1": "ch5-experiment-timeline",
    "Table 5.2": "ch5-group-comparison-table",
    "Table 5.3": "ch5-evaluation-metrics-table",
}


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def upload_png(png_path):
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
                url = resp.json().get("image", {}).get("url", "")
                if url:
                    return url
        except Exception as e:
            print(f"    upload attempt {attempt+1}: {e}")
        time.sleep(3)
    return None


# ══ STEP 1: Upload all PNGs ══
print("=== STEP 1: Upload PNGs ===")
png_files = sorted(f for f in os.listdir(PNG_DIR) if f.endswith(".png") and f.startswith("ch"))
upload_map = {}

for fname in png_files:
    png_path = os.path.join(PNG_DIR, fname)
    from PIL import Image
    img = Image.open(png_path)
    w, h = img.size

    url = upload_png(png_path)
    key = fname.replace(".png", "")
    upload_map[key] = {"url": url, "w": w, "h": h, "file": fname}
    status = "OK" if url else "FAIL"
    print(f"  {fname:50s} {w}x{h}  {status}")
    time.sleep(1)

# Save map
with open(os.path.join(PNG_DIR, "final_upload_map.json"), "w") as f:
    json.dump(upload_map, f, indent=2)

uploaded = sum(1 for v in upload_map.values() if v.get("url"))
print(f"\nUploaded: {uploaded}/{len(png_files)}\n")

# ══ STEP 2: Find all large images in doc + their nearby captions ══
print("=== STEP 2: Match doc images to PNGs ===")
doc = get_doc()
inline_objs = doc.get("inlineObjects", {})

# Build list of all paragraphs for caption lookup
all_paras = []
for elem in doc["body"]["content"]:
    if "paragraph" in elem:
        text = ""
        for el in elem["paragraph"].get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        all_paras.append({
            "start": elem.get("startIndex", 0),
            "end": elem.get("endIndex", 0),
            "text": text.strip(),
        })

# Find large images
doc_images = []
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
        props = inline_objs[obj_id]["inlineObjectProperties"]["embeddedObject"]
        uri = props.get("imageProperties", {}).get("sourceUri", "")
        w = props.get("size", {}).get("width", {}).get("magnitude", 0)
        h = props.get("size", {}).get("height", {}).get("magnitude", 0)

        if w < 200:  # Skip equations
            continue

        # Find nearest caption (search ±5 paragraphs)
        caption = ""
        for p in all_paras:
            if abs(p["start"] - si) > 3000:
                continue
            cap_match = re.match(r"^(Table|Figure) (\d+\.\d+)", p["text"])
            if cap_match:
                caption = f"{cap_match.group(1)} {cap_match.group(2)}"
                break

        doc_images.append({
            "obj_id": obj_id,
            "para_start": si,
            "para_end": ei,
            "uri": uri,
            "w_pt": w,
            "h_pt": h,
            "caption": caption,
        })

print(f"Found {len(doc_images)} large images in doc")

# Match each doc image to a PNG
matches = []
matched_pngs = set()

for di in doc_images:
    png_key = None

    # Strategy A: Caption-based matching
    if di["caption"] in CAPTION_TO_PNG:
        png_key = CAPTION_TO_PNG[di["caption"]]

    if png_key and png_key in upload_map and upload_map[png_key].get("url") and png_key not in matched_pngs:
        matches.append({"doc_img": di, "png_key": png_key})
        matched_pngs.add(png_key)
        print(f"  MATCH [{di['para_start']:6d}] {di['caption']:12s} -> {png_key}")
    else:
        print(f"  SKIP  [{di['para_start']:6d}] caption={di['caption'] or 'none':12s} uri={di['uri'][-15:]}")

print(f"\n{len(matches)} matches ready\n")

# ══ STEP 3: Replace (bottom-to-top) ══
print("=== STEP 3: Replace images ===")
matches.sort(key=lambda m: m["doc_img"]["para_start"], reverse=True)

replaced = 0
for match in matches:
    di = match["doc_img"]
    pk = match["png_key"]
    um = upload_map[pk]

    # Re-read doc
    doc = get_doc()
    inline_objs = doc.get("inlineObjects", {})

    # Find image paragraph by obj_id
    found = None
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        for el in elem["paragraph"].get("elements", []):
            if "inlineObjectElement" in el:
                if el["inlineObjectElement"].get("inlineObjectId") == di["obj_id"]:
                    found = elem
                    break
        if found:
            break

    if not found:
        print(f"  NOT FOUND: {pk}")
        continue

    si = found["startIndex"]
    ei = found["endIndex"]

    # Calculate display size
    aspect = um["h"] / um["w"]
    display_w = min(di["w_pt"], 460)  # Cap at 460pt
    display_h = display_w * aspect

    reqs = [
        {"deleteContentRange": {"range": {"startIndex": si, "endIndex": ei - 1}}},
        {"insertInlineImage": {
            "location": {"index": si},
            "uri": um["url"],
            "objectSize": {
                "width": {"magnitude": display_w, "unit": "PT"},
                "height": {"magnitude": display_h, "unit": "PT"},
            },
        }},
        {"updateParagraphStyle": {
            "range": {"startIndex": si, "endIndex": si + 1},
            "paragraphStyle": {
                "alignment": "CENTER",
                "spaceAbove": {"magnitude": 18, "unit": "PT"},
                "spaceBelow": {"magnitude": 6, "unit": "PT"},
            },
            "fields": "alignment,spaceAbove,spaceBelow",
        }},
    ]

    try:
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
        replaced += 1
        print(f"  REPLACED [{si}] {pk:45s} {display_w:.0f}x{display_h:.0f}pt")
    except Exception as e:
        print(f"  ERROR [{si}] {pk}: {e}")

    time.sleep(2)

print(f"\n=== DONE: {replaced}/{len(matches)} replaced ===")
