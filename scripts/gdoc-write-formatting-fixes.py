"""
gdoc-write-formatting-fixes.py
Applies formatting fixes to the thesis Google Doc:
1. Promote "References" from HEADING_2 to HEADING_1 + uppercase
2. Renumber 5.5 -> 5.4 (heading + cross-refs)
3. Promote Ch.1/Ch.2 x.y headings from HEADING_3 to HEADING_2
4. Verify Ch.5 unnumbered subsections
"""
import sys, re, json, importlib.util
spec = importlib.util.spec_from_file_location("gdoc_util_auth", r"c:\Users\duong\WebstormProjects\Thesis\scripts\gdoc-util-auth.py")
gdoc_util_auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gdoc_util_auth)
get_docs_service = gdoc_util_auth.get_docs_service
DOC_ID = gdoc_util_auth.DOC_ID

service = get_docs_service()

def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()

def batch_update(requests):
    if not requests:
        return
    return service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()

# ============ STEP 1: Read document structure ============
print("Reading document...")
doc = get_doc()

paragraphs = []
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    paragraphs.append({
        "startIndex": elem["startIndex"],
        "endIndex": elem["endIndex"],
        "text": text.strip(),
        "rawText": text,
        "style": style,
    })

# ============ FIX 1: Promote "References" to HEADING_1 ============
print("\n===== FIX 1: Promote References to HEADING_1 =====")
references_para = None
for p in paragraphs:
    if p["text"] == "References" and p["style"] == "HEADING_2":
        references_para = p
        break

if references_para:
    print(f"  Found 'References' at index {references_para['startIndex']}, style={references_para['style']}")
    # Change style to HEADING_1 and text to REFERENCES
    requests_fix1 = [
        {
            "updateParagraphStyle": {
                "range": {
                    "startIndex": references_para["startIndex"],
                    "endIndex": references_para["endIndex"],
                },
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType",
            }
        },
        {
            "deleteContentRange": {
                "range": {
                    "startIndex": references_para["startIndex"],
                    "endIndex": references_para["endIndex"] - 1,  # keep the newline
                }
            }
        },
        {
            "insertText": {
                "location": {"index": references_para["startIndex"]},
                "text": "REFERENCES",
            }
        },
    ]
    batch_update(requests_fix1)
    print("  DONE: References -> REFERENCES (HEADING_1)")
else:
    print("  WARNING: Could not find 'References' as HEADING_2")

# ============ FIX 2: Renumber 5.5 -> 5.4 ============
print("\n===== FIX 2: Renumber 5.5 -> 5.4 =====")
# Use replaceAllText for each replacement
replacements = [
    ("5.5 Threats to Validity", "5.4. Threats to Validity"),
    ("Section 5.5 (Threats to Validity)", "Section 5.4 (Threats to Validity)"),
    ("Section 5.5", "Section 5.4"),
]

for old_text, new_text in replacements:
    req = {
        "replaceAllText": {
            "containsText": {"text": old_text, "matchCase": True},
            "replaceText": new_text,
        }
    }
    result = batch_update([req])
    count = 0
    if result and "replies" in result:
        for r in result["replies"]:
            if "replaceAllText" in r:
                count = r["replaceAllText"].get("occurrencesChanged", 0)
    print(f"  '{old_text}' -> '{new_text}': {count} occurrence(s)")

# ============ FIX 3: Promote Ch.1/Ch.2 x.y headings from HEADING_3 to HEADING_2 ============
print("\n===== FIX 3: Promote Ch.1/Ch.2 section headings =====")
# Re-read document after previous changes
doc = get_doc()
paragraphs = []
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    paragraphs.append({
        "startIndex": elem["startIndex"],
        "endIndex": elem["endIndex"],
        "text": text.strip(),
        "rawText": text,
        "style": style,
    })

# Pattern: starts with 1.x. or 2.x. (but NOT 1.x.y or 2.x.y)
pattern = re.compile(r"^([12]\.\d+\.)\s")
promoted = []
requests_fix3 = []

for p in paragraphs:
    if p["style"] != "HEADING_3":
        continue
    m = pattern.match(p["text"])
    if m:
        # Make sure it's x.y. not x.y.z (no additional dot-number)
        prefix = m.group(1)
        # Check that after the prefix + space, there's no more digit.dot pattern
        # Actually the regex already ensures it starts with X.Y. so just check prefix has exactly one dot between digits
        parts = prefix.rstrip(".").split(".")
        if len(parts) == 2:  # e.g. ["1", "2"] - this is x.y level
            requests_fix3.append({
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": p["startIndex"],
                        "endIndex": p["endIndex"],
                    },
                    "paragraphStyle": {"namedStyleType": "HEADING_2"},
                    "fields": "namedStyleType",
                }
            })
            promoted.append(p["text"][:60])

if requests_fix3:
    batch_update(requests_fix3)

print(f"  Promoted {len(promoted)} headings from HEADING_3 to HEADING_2:")
for h in promoted:
    print(f"    - {h}")

# ============ FIX 4: Verify Ch.5 unnumbered subsections ============
print("\n===== FIX 4: Verify Ch.5 unnumbered subsections =====")
ch5_unnumbered = [
    "Experimental Design Overview",
    "Research Questions and Measurements",
    "Ethical Considerations",
    "Group Comparison Analysis Plan",
]

# Re-read doc for verification
doc = get_doc()
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    stripped = text.strip()
    if stripped in ch5_unnumbered:
        print(f"  '{stripped}' -> style={style} (expected HEADING_3)")
        if style != "HEADING_3":
            print(f"    WARNING: unexpected style!")

# ============ FINAL VERIFICATION ============
print("\n===== FINAL VERIFICATION =====")
doc = get_doc()
# Check References is HEADING_1
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    stripped = text.strip()
    if stripped == "REFERENCES":
        print(f"  Fix 1 VERIFIED: 'REFERENCES' is {style}")
        break

# Check 5.4 heading exists
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    if "5.4." in text and "Threats" in text:
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        print(f"  Fix 2 VERIFIED: '{text.strip()[:50]}' exists as {style}")
        break

print("\n===== All fixes DONE =====")
