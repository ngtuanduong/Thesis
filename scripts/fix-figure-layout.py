"""
Fix figure/table layout in the thesis Google Doc.
1. Separate mixed text+image paragraphs (split caption from image)
2. Apply correct spacing and centering to all figure/table image paragraphs
3. Format captions: italic, centered, TNR 12pt
"""
import importlib.util
import io
import re
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID

MIN_IMG_WIDTH = 200  # Only fix large images (figures/tables), not equations


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def get_image_size(doc, obj_id):
    inline_objs = doc.get("inlineObjects", {})
    if obj_id not in inline_objs:
        return 0, 0
    props = inline_objs[obj_id].get("inlineObjectProperties", {}).get("embeddedObject", {})
    w = props.get("size", {}).get("width", {}).get("magnitude", 0)
    h = props.get("size", {}).get("height", {}).get("magnitude", 0)
    return w, h


def analyze_image_paragraphs(doc):
    """Find all paragraphs with large inline images and their issues."""
    results = []
    all_paras = [e for e in doc["body"]["content"] if "paragraph" in e]

    for i, elem in enumerate(all_paras):
        para = elem["paragraph"]
        si = elem.get("startIndex", 0)
        ei = elem.get("endIndex", 0)

        img_obj_id = None
        text_parts = []
        img_index = None

        for el_idx, el in enumerate(para.get("elements", [])):
            if "inlineObjectElement" in el:
                img_obj_id = el["inlineObjectElement"].get("inlineObjectId", "")
                img_index = el.get("startIndex", si)
            if "textRun" in el:
                t = el["textRun"]["content"]
                if t.strip():
                    text_parts.append({
                        "start": el["startIndex"],
                        "end": el["endIndex"],
                        "text": t.strip(),
                    })

        if not img_obj_id:
            continue

        w, h = get_image_size(doc, img_obj_id)
        if w < MIN_IMG_WIDTH:
            continue  # Skip equations

        ps = para.get("paragraphStyle", {})
        alignment = ps.get("alignment", "START")
        space_above = ps.get("spaceAbove", {}).get("magnitude", 0)
        space_below = ps.get("spaceBelow", {}).get("magnitude", 0)

        # Check next paragraph for caption
        caption_para = None
        if i + 1 < len(all_paras):
            next_p = all_paras[i + 1]
            next_text = ""
            for el in next_p["paragraph"].get("elements", []):
                if "textRun" in el:
                    next_text += el["textRun"]["content"]
            if re.match(r"^(Table|Figure) \d+\.\d+", next_text.strip()):
                caption_para = {
                    "start": next_p.get("startIndex", 0),
                    "end": next_p.get("endIndex", 0),
                    "text": next_text.strip(),
                }

        results.append({
            "para_start": si,
            "para_end": ei,
            "img_obj_id": img_obj_id,
            "img_index": img_index,
            "img_w": w,
            "img_h": h,
            "has_mixed_text": bool(text_parts),
            "text_parts": text_parts,
            "alignment": alignment,
            "space_above": space_above,
            "space_below": space_below,
            "caption_para": caption_para,
        })

    return results


# ══════════════════════════════════════════════
# PHASE 1: Fix spacing and centering for ALL figure/table images
# ══════════════════════════════════════════════
print("=== PHASE 1: Fix spacing and centering ===")
doc = get_doc()
images = analyze_image_paragraphs(doc)
print(f"Found {len(images)} figure/table images")

# Batch all spacing/centering fixes
spacing_reqs = []
for img in images:
    # Fix image paragraph: centered, proper spacing
    spacing_reqs.append({
        "updateParagraphStyle": {
            "range": {"startIndex": img["para_start"], "endIndex": img["para_end"]},
            "paragraphStyle": {
                "alignment": "CENTER",
                "spaceAbove": {"magnitude": 18, "unit": "PT"},
                "spaceBelow": {"magnitude": 6, "unit": "PT"},
                "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                "indentStart": {"magnitude": 0, "unit": "PT"},
            },
            "fields": "alignment,spaceAbove,spaceBelow,indentFirstLine,indentStart",
        }
    })

    # Fix caption paragraph if exists
    if img["caption_para"]:
        cp = img["caption_para"]
        spacing_reqs.append({
            "updateParagraphStyle": {
                "range": {"startIndex": cp["start"], "endIndex": cp["end"]},
                "paragraphStyle": {
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 3, "unit": "PT"},
                    "spaceBelow": {"magnitude": 12, "unit": "PT"},
                },
                "fields": "alignment,spaceAbove,spaceBelow",
            }
        })
        # Caption text style: italic, TNR 12pt
        spacing_reqs.append({
            "updateTextStyle": {
                "range": {"startIndex": cp["start"], "endIndex": cp["end"] - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Times New Roman"},
                    "fontSize": {"magnitude": 12, "unit": "PT"},
                    "italic": True,
                },
                "fields": "weightedFontFamily,fontSize,italic",
            }
        })

if spacing_reqs:
    for i in range(0, len(spacing_reqs), 50):
        batch = spacing_reqs[i:i + 50]
        try:
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch}).execute()
            print(f"  Batch {i // 50 + 1}: {len(batch)} requests OK")
        except Exception as e:
            print(f"  Batch {i // 50 + 1} ERROR: {e}")
        time.sleep(0.5)

print(f"  Applied spacing/centering to {len(images)} image paragraphs")

# ══════════════════════════════════════════════
# PHASE 2: Split mixed text+image paragraphs
# ══════════════════════════════════════════════
print("\n=== PHASE 2: Split mixed text+image paragraphs ===")

# Re-read doc and find mixed paragraphs
doc = get_doc()
images = analyze_image_paragraphs(doc)
mixed = [img for img in images if img["has_mixed_text"]]
print(f"Found {len(mixed)} paragraphs with mixed text+image")

# Process in REVERSE order (bottom first)
mixed.sort(key=lambda x: x["para_start"], reverse=True)

for img in mixed:
    # Strategy: The text in these paragraphs is the caption (e.g., "Figure 1.3. Title...")
    # We need to:
    # 1. Delete the text from the paragraph (keep only the image + newline)
    # 2. Insert a new paragraph after with the caption text
    # 3. Format the new caption paragraph

    caption_text = " ".join(tp["text"] for tp in img["text_parts"])
    print(f"  Splitting [{img['para_start']}]: \"{caption_text[:50]}...\"")

    # Find the text ranges to delete (everything that's not the image)
    # Delete text parts in reverse order within the paragraph
    text_parts_sorted = sorted(img["text_parts"], key=lambda tp: tp["start"], reverse=True)

    reqs = []
    for tp in text_parts_sorted:
        # Only delete if there's actual content range
        if tp["end"] > tp["start"]:
            reqs.append({
                "deleteContentRange": {
                    "range": {"startIndex": tp["start"], "endIndex": tp["end"]}
                }
            })

    if reqs:
        try:
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
        except Exception as e:
            print(f"    ERROR deleting text: {e}")
            continue
        time.sleep(0.5)

    # Re-read doc to get fresh index for the image paragraph end
    doc = get_doc()

    # Find the image paragraph again (it should now contain only the image)
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        si = elem.get("startIndex", 0)
        for el in elem["paragraph"].get("elements", []):
            if "inlineObjectElement" in el:
                oid = el["inlineObjectElement"].get("inlineObjectId", "")
                if oid == img["img_obj_id"]:
                    # Insert caption text after this paragraph
                    insert_idx = elem.get("endIndex", 0)
                    caption_reqs = [
                        {"insertText": {
                            "location": {"index": insert_idx - 1},
                            "text": "\n" + caption_text,
                        }},
                    ]
                    try:
                        service.documents().batchUpdate(
                            documentId=DOC_ID, body={"requests": caption_reqs}
                        ).execute()
                    except Exception as e:
                        print(f"    ERROR inserting caption: {e}")
                        break

                    time.sleep(0.5)

                    # Format the new caption paragraph
                    doc = get_doc()
                    # Find the caption text we just inserted
                    for elem2 in doc["body"]["content"]:
                        if "paragraph" not in elem2:
                            continue
                        t = ""
                        for el2 in elem2["paragraph"].get("elements", []):
                            if "textRun" in el2:
                                t += el2["textRun"]["content"]
                        if caption_text[:30] in t:
                            fmt_reqs = [
                                {"updateParagraphStyle": {
                                    "range": {"startIndex": elem2["startIndex"], "endIndex": elem2["endIndex"]},
                                    "paragraphStyle": {
                                        "alignment": "CENTER",
                                        "spaceAbove": {"magnitude": 3, "unit": "PT"},
                                        "spaceBelow": {"magnitude": 12, "unit": "PT"},
                                    },
                                    "fields": "alignment,spaceAbove,spaceBelow",
                                }},
                                {"updateTextStyle": {
                                    "range": {"startIndex": elem2["startIndex"], "endIndex": elem2["endIndex"] - 1},
                                    "textStyle": {
                                        "weightedFontFamily": {"fontFamily": "Times New Roman"},
                                        "fontSize": {"magnitude": 12, "unit": "PT"},
                                        "italic": True,
                                    },
                                    "fields": "weightedFontFamily,fontSize,italic",
                                }},
                            ]
                            service.documents().batchUpdate(
                                documentId=DOC_ID, body={"requests": fmt_reqs}
                            ).execute()
                            print(f"    Caption separated and formatted: \"{caption_text[:40]}...\"")
                            break
                    break
        else:
            continue
        break

    time.sleep(1)

# ══════════════════════════════════════════════
# PHASE 3: Final verification count
# ══════════════════════════════════════════════
print("\n=== PHASE 3: Verify ===")
doc = get_doc()
images = analyze_image_paragraphs(doc)

ok_count = 0
issue_count = 0
for img in images:
    issues = []
    if img["has_mixed_text"]:
        issues.append("STILL_MIXED")
    if img["alignment"] != "CENTER":
        issues.append("NOT_CENTERED")
    if img["space_above"] < 10:
        issues.append(f"LOW_ABOVE({img['space_above']})")

    if issues:
        issue_count += 1
        print(f"  ISSUE [{img['para_start']}] {img['img_w']:.0f}x{img['img_h']:.0f}pt: {', '.join(issues)}")
    else:
        ok_count += 1

print(f"\nResult: {ok_count} OK, {issue_count} issues remaining")
print("Done.")
