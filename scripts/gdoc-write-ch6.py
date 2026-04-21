"""
gdoc-write-ch6: Insert Chapter 6 Conclusion into thesis doc before REFERENCES heading.
Applies HANU thesis formatting: HEADING_1, HEADING_2, body text TNR 13pt justified.
"""
import sys, os, re, warnings
warnings.filterwarnings("ignore")

scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)
# Also handle importlib pattern for hyphenated filename
import importlib.util
_spec = importlib.util.spec_from_file_location("gdoc_util_auth", os.path.join(scripts_dir, "gdoc-util-auth.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
sys.modules["gdoc_util_auth"] = _mod
from gdoc_util_auth import get_docs_service, get_document, iter_paragraphs, DOC_ID

# ---------- 1. Find REFERENCES heading ----------
service = get_docs_service()
doc = get_document(service)

ref_index = None
for start, end, text, style in iter_paragraphs(doc):
    if style == "HEADING_1" and "REFERENCES" in text.upper():
        ref_index = start
        break

if ref_index is None:
    print("ERROR: Could not find REFERENCES heading")
    sys.exit(1)

print(f"Found REFERENCES at index {ref_index}")

# ---------- 2. Parse chapter6 content ----------
chapter_title = "CHAPTER 6. CONCLUSION"

sections = [
    ("heading2", "6.1. Summary of Work"),
    ("heading2", "6.2. Contributions"),
    ("heading2", "6.3. Limitations"),
    ("heading2", "6.4. Future Work"),
    ("heading2", "6.5. Closing Remarks"),
]

md_path = r"c:\Users\duong\WebstormProjects\Thesis\documents\thesis-chapters\chapter6-conclusion.md"
with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Parse into blocks: (type, text)
# type: "chapter_title", "heading2", "body"
blocks = []

lines = md_content.split("\n")
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("# ") and i == 0:
        # skip md chapter title, we use our own
        i += 1
        continue
    elif line.startswith("## "):
        heading_text = line[3:].strip()
        blocks.append(("heading2", heading_text))
        i += 1
        continue
    elif line.strip() == "":
        i += 1
        continue
    else:
        # body paragraph - collect until empty line or heading
        para_lines = []
        while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith("#"):
            para_lines.append(lines[i])
            i += 1
        para_text = " ".join(para_lines)
        # Convert --- to em-dash
        para_text = para_text.replace("---", "\u2014")
        blocks.append(("body", para_text))
        continue

# ---------- 3. Build insert requests ----------
# We insert at ref_index. All inserts shift indices, so we insert in reverse
# or calculate offsets. Easier: insert all text first, then format.

# Strategy: insert all text at ref_index as a single batch,
# then apply formatting in a second batch.

# Build the full text to insert, tracking ranges for formatting
# We'll insert a page break first, then the content.

# Collect (type, text, bold_ranges) for each block
# bold_ranges: list of (start_in_text, end_in_text) for bold spans

def parse_bold(text):
    """Parse **bold** markers, return (clean_text, [(start, end), ...])"""
    ranges = []
    clean = ""
    pattern = re.compile(r'\*\*(.+?)\*\*')
    last_end = 0
    for m in pattern.finditer(text):
        clean += text[last_end:m.start()]
        bold_start = len(clean)
        clean += m.group(1)
        bold_end = len(clean)
        ranges.append((bold_start, bold_end))
        last_end = m.end()
    clean += text[last_end:]
    return clean, ranges


# Build ordered content: chapter_title, then blocks
content_items = []  # (type, clean_text, bold_ranges)

# Chapter title
content_items.append(("chapter_title", chapter_title, []))

# Body and headings from blocks
for btype, btext in blocks:
    clean, bolds = parse_bold(btext)
    content_items.append((btype, clean, bolds))

# Now build the text string and track absolute positions relative to ref_index
# Insert format: page_break + \n + chapter_title\n + body\n + heading\n + ...
# Each paragraph ends with \n

# We'll build requests list
requests = []

# Insert page break at ref_index
requests.append({
    "insertPageBreak": {
        "location": {"index": ref_index}
    }
})

# After page break insertion, text shifts. The page break inserts 2 chars (break + newline)
# Actually insertPageBreak inserts a paragraph with break. Let's use insertText approach instead.
# Better approach: insert all text first with newlines, then format.

# Actually let's do it properly:
# 1) Insert page break
# 2) Insert text paragraphs
# 3) Apply paragraph styles
# 4) Apply text formatting (bold, font)

# The page break creates a new paragraph. After inserting it at ref_index,
# the break occupies indices ref_index to ref_index+2 (break char + newline).
# Then we insert our text starting at ref_index + 2.

# Let's just build all text first, then insert, then format.
# We insert in one go to avoid index shifting complexities.

# Build full text string
full_text = ""
paragraph_ranges = []  # (type, start_offset, end_offset) relative to insertion point

for item_type, text, bolds in content_items:
    start = len(full_text)
    full_text += text + "\n"
    end = len(full_text)
    paragraph_ranges.append((item_type, start, end, bolds))

# Now: insert page break at ref_index, then insert full_text after the break.
# Page break inserts a paragraph break + page break special char.
# To simplify, let's do sequential requests:

# Step 1: Insert the full text at ref_index
# Step 2: Insert page break at ref_index (this pushes text forward)
# Wait, order matters. Let's think about this differently.

# If we insert text first at ref_index, text goes before REFERENCES. Good.
# Then if we insert page break at ref_index, it goes before our chapter text. Good.
# But batch requests execute in order, so:

# Request 1: insert text at ref_index -> our chapter text is at [ref_index, ref_index + len(full_text))
# Request 2: insert page break at ref_index -> pushes chapter text forward by 2

# Actually the API executes requests in order and indices shift.
# Let's insert page break first (at ref_index), then text after it.

# After page break insertion at ref_index:
# - Page break creates a paragraph: occupies ref_index to ref_index + 2 (one for break element, one for newline)
# Actually, insertPageBreak at index X inserts a page break character. The resulting content is:
# The paragraph gets a page break element. It inserts 1 character (the break) but may also create a newline.
# Let's just test with inserting text first approach using insertText for everything including a page break character.

# Simpler approach: use insertText for \f (form feed) which doesn't work in Docs.
# The correct way: use insertPageBreak request, then insertText for the rest.

# Let me use a clean two-batch approach:
# Batch 1: structural inserts (page break + text)
# Batch 2: formatting

# For Batch 1, we need to know exact indices after each operation.
# Google Docs batchUpdate processes requests sequentially, each shifting indices.

# Strategy: Insert everything in REVERSE order at ref_index.
# Last paragraph first, chapter title last, page break very last.
# This way each insert goes to ref_index and doesn't affect previously inserted content.

# Actually simpler: insert all text at ref_index in one insertText call,
# then insert page break at ref_index to push it all forward.

requests_batch1 = []

# First: insert all text at ref_index
requests_batch1.append({
    "insertText": {
        "location": {"index": ref_index},
        "text": full_text
    }
})

# Second: insert page break at ref_index (pushes text after it)
requests_batch1.append({
    "insertPageBreak": {
        "location": {"index": ref_index}
    }
})

# Execute batch 1
print(f"Inserting {len(full_text)} chars of chapter 6 text + page break...")
result = service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": requests_batch1}
).execute()
print(f"Batch 1 done. {len(result.get('replies', []))} replies.")

# Now figure out where our text actually is.
# After insertText at ref_index: text is at [ref_index, ref_index + len(full_text))
# After insertPageBreak at ref_index: page break is at ref_index,
# and our text shifts forward. Page break inserts 2 characters (break + implicit newline for the paragraph).
# So our text starts at ref_index + 2.

# Actually let's just re-read the doc to get exact positions.
doc = get_document(service)

# Find our chapter title
ch6_start = None
ch6_ranges = []  # (type, startIndex, endIndex, bold_ranges_absolute)

for start, end, text, style in iter_paragraphs(doc):
    if chapter_title in text and ch6_start is None:
        ch6_start = start
        break

if ch6_start is None:
    print("ERROR: Could not find inserted chapter title")
    sys.exit(1)

print(f"Chapter 6 title found at index {ch6_start}")

# Now collect all paragraphs from ch6_start until we hit REFERENCES
paragraphs = []
found_ch6 = False
for start, end, text, style in iter_paragraphs(doc):
    if start >= ch6_start:
        if "REFERENCES" in text and style == "HEADING_1" and found_ch6:
            break
        found_ch6 = True
        paragraphs.append((start, end, text, style))

print(f"Found {len(paragraphs)} paragraphs in chapter 6 section")

# ---------- 4. Apply formatting ----------
requests_batch2 = []

# Map paragraph text to type
def get_para_type(text):
    text = text.strip()
    if text == chapter_title:
        return "chapter_title"
    for _, heading in sections:
        if text == heading:
            return "heading2"
    return "body"

for start, end, text, style in paragraphs:
    ptype = get_para_type(text.strip())

    if ptype == "chapter_title":
        # HEADING_1, centered, TNR 16pt bold, 32pt spacing
        requests_batch2.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_1",
                    "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 32, "unit": "PT"},
                    "spaceBelow": {"magnitude": 32, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }
        })
        requests_batch2.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 16, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }
        })
    elif ptype == "heading2":
        # HEADING_2, justified, TNR 14pt bold, 6pt spacing
        requests_batch2.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_2",
                    "alignment": "START",
                    "spaceAbove": {"magnitude": 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }
        })
        requests_batch2.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 14, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }
        })
    else:
        # NORMAL_TEXT, justified, TNR 13pt, 1.5 line spacing
        requests_batch2.append({
            "updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT",
                    "alignment": "JUSTIFIED",
                    "lineSpacing": 150,
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 0, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,lineSpacing,spaceAbove,spaceBelow"
            }
        })
        requests_batch2.append({
            "updateTextStyle": {
                "range": {"startIndex": start, "endIndex": end - 1},
                "textStyle": {
                    "bold": False,
                    "fontSize": {"magnitude": 13, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }
        })

# ---------- 5. Apply bold for **text** markers ----------
# We need to find bold ranges in the actual document text
# Re-parse original content_items and match against inserted paragraphs

# Match paragraphs to content_items by text content
for start, end, text, style in paragraphs:
    # Find matching content_item
    for item_type, item_text, bold_ranges in content_items:
        if item_text.strip() == text.strip() and bold_ranges:
            # Apply bold to each range
            for bstart, bend in bold_ranges:
                abs_start = start + bstart
                abs_end = start + bend
                requests_batch2.append({
                    "updateTextStyle": {
                        "range": {"startIndex": abs_start, "endIndex": abs_end},
                        "textStyle": {"bold": True},
                        "fields": "bold"
                    }
                })
            break

if requests_batch2:
    print(f"Applying {len(requests_batch2)} formatting requests...")
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests_batch2}
    ).execute()
    print(f"Batch 2 done. {len(result.get('replies', []))} replies.")

# ---------- 6. Verify ----------
doc = get_document(service)
print("\n--- Verification ---")
found_ch6 = False
count = 0
for start, end, text, style in iter_paragraphs(doc):
    if chapter_title in text:
        found_ch6 = True
    if found_ch6:
        print(f"  [{style:15s}] {text[:80].strip()}")
        count += 1
        if count > 25 or ("REFERENCES" in text and style == "HEADING_1"):
            break

print("\nDone! Chapter 6 inserted successfully before REFERENCES.")
