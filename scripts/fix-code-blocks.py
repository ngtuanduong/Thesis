"""
Format code blocks in the thesis Google Doc.
Apply: Consolas 11pt, light gray background, left-aligned, 6pt spacing.
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


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def is_code_line(text):
    s = text.rstrip()
    if not s:
        return False
    if re.match(r'^\s*(name\s+VARCHAR|display_name|topic_group|from_concept_id|to_concept_id|relation_type|problem_id|concept_id|UNIQUE|PRIMARY|CREATE|ALTER|INT |VARCHAR|TEXT |BOOLEAN|UUID |SERIAL|id\s+SERIAL|difficulty_tier)', s):
        return True
    if re.match(r'^\s*(def |class |import |from .+ import |if |elif |else:|for |while |return |try:|except |with |raise |assert |yield |async |await )', s):
        return True
    if re.match(r'^    ', text) and len(s) < 200:
        return True
    if re.match(r'^\s*[a-z_][a-z_0-9]*\s*[=]\s*', s) and len(s) < 200 and any(c in s for c in ['(', ')', '[', ']', '.', '"', "'"]):
        return True
    if re.match(r'^\s*(self\.|await |state\.|params\.|session\.)', s):
        return True
    if re.match(r'^\s*#', s):
        return True
    return False


doc = get_doc()

# Collect paragraphs
paras = []
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
    si = elem["startIndex"]
    ei = elem["endIndex"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    paras.append({"start": si, "end": ei, "text": text.rstrip("\n"), "style": style, "has_img": has_img})

# Group consecutive code lines into blocks (2+ lines required)
code_blocks = []
current_block = None
for p in paras:
    if p["style"] != "NORMAL_TEXT" or p["has_img"]:
        if current_block:
            code_blocks.append(current_block)
            current_block = None
        continue
    if is_code_line(p["text"]):
        if current_block is None:
            current_block = {"lines": [p]}
        else:
            current_block["lines"].append(p)
    else:
        if current_block:
            code_blocks.append(current_block)
            current_block = None

if current_block:
    code_blocks.append(current_block)

code_blocks = [b for b in code_blocks if len(b["lines"]) >= 2]

print(f"Found {len(code_blocks)} code blocks, {sum(len(b['lines']) for b in code_blocks)} lines total")

# Apply formatting to each block in one batch
# Light gray background: RGB(242, 242, 242) = #F2F2F2
BG_COLOR = {"color": {"rgbColor": {"red": 0.949, "green": 0.949, "blue": 0.949}}}

requests = []
for block in code_blocks:
    block_start = block["lines"][0]["start"]
    block_end = block["lines"][-1]["end"]

    # Text style: Consolas 11pt, not italic, not bold
    requests.append({
        "updateTextStyle": {
            "range": {"startIndex": block_start, "endIndex": block_end - 1},
            "textStyle": {
                "weightedFontFamily": {"fontFamily": "Consolas"},
                "fontSize": {"magnitude": 11, "unit": "PT"},
                "bold": False,
                "italic": False,
                "baselineOffset": "NONE",
            },
            "fields": "weightedFontFamily,fontSize,bold,italic,baselineOffset",
        }
    })

    # Paragraph style for each line: left-aligned, tight spacing, background
    for line in block["lines"]:
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": line["start"], "endIndex": line["end"]},
                "paragraphStyle": {
                    "alignment": "START",
                    "lineSpacing": 115,  # Tighter than 150% body text
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 0, "unit": "PT"},
                    "shading": {"backgroundColor": BG_COLOR},
                    "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                    "indentStart": {"magnitude": 18, "unit": "PT"},  # Small left indent
                },
                "fields": "alignment,lineSpacing,spaceAbove,spaceBelow,shading,indentFirstLine,indentStart",
            }
        })

    print(f"  Block [{block_start}-{block_end}]: {len(block['lines'])} lines - {block['lines'][0]['text'][:60]}...")

# Add spacing above first line and below last line of each block
for block in code_blocks:
    first = block["lines"][0]
    last = block["lines"][-1]
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": first["start"], "endIndex": first["end"]},
            "paragraphStyle": {
                "spaceAbove": {"magnitude": 6, "unit": "PT"},
            },
            "fields": "spaceAbove",
        }
    })
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": last["start"], "endIndex": last["end"]},
            "paragraphStyle": {
                "spaceBelow": {"magnitude": 6, "unit": "PT"},
            },
            "fields": "spaceBelow",
        }
    })

print(f"\nApplying {len(requests)} formatting requests...")

# Split into batches of 50 to avoid API limits
BATCH_SIZE = 50
for i in range(0, len(requests), BATCH_SIZE):
    batch = requests[i:i + BATCH_SIZE]
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID, body={"requests": batch}
        ).execute()
        print(f"  Batch {i // BATCH_SIZE + 1}: {len(batch)} requests OK")
    except Exception as e:
        print(f"  Batch {i // BATCH_SIZE + 1}: ERROR - {e}")
    time.sleep(1)

print("\nDone. Code blocks formatted with Consolas 11pt + gray background.")
