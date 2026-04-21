"""
Fix code blocks in thesis Google Doc using single-cell tables with syntax highlighting.
Phase 1: Delete broken code-block images (iili.io source URLs)
Phase 2: Insert code blocks as 1x1 tables with Pygments syntax colors
"""
import importlib.util
import io
import json
import re
import sys
import time

from pygments import lex
from pygments.lexers import PythonLexer, SqlLexer
from pygments.styles import get_style_by_name

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID

with open("C:/tmp/equations/code_blocks.json", "r", encoding="utf-8") as f:
    CODE_BLOCKS = json.load(f)

STYLE = get_style_by_name("friendly")
LEXERS = {"python": PythonLexer(), "sql": SqlLexer()}

# ── Anchor texts: the sentence PRECEDING each code block in the doc ──
# These are used to find where to insert the table
ANCHORS = [
    # Block 1: concepts SQL
    {"search": "The concepts table stores each concept", "block_idx": 0},
    # Block 2: knowledge_graph_edges SQL
    {"search": "These edges live in the knowledge_graph_edges table", "block_idx": 1},
    # Block 3: problem_concepts SQL
    {"search": "is_primary BOOLEAN column distinguishes", "block_idx": 2},
    # Block 4: bkt_update
    {"search": "Below is the core update function", "block_idx": 3},
    # Block 5: BKTService.update
    {"search": "BKTService.update method retrieves all", "block_idx": 4},
    # Block 6: ELO constants + expected_score
    {"search": "Student ratings are initially set at 1200", "block_idx": 5},
    # Block 7: compute_dynamic_k
    {"search": "innovation of this system is its dynamic K-factor", "block_idx": 6},
    # Block 8: compute_problem_k
    {"search": "problem K-factors work differently", "block_idx": 7},
    # Block 9: get_zpd_problems
    {"search": "ZPD range is", "block_idx": 8},
    # Block 10: thompson_select
    {"search": "Thompson Sampling is a Bayesian method", "block_idx": 9},
    # Block 11: compute_reward
    {"search": "three parts to the reward signal", "block_idx": 10},
    # Block 12: MAB update
    {"search": "update method feeds the computed reward", "block_idx": 11},
    # Block 13: W = [FSRS weights]
    {"search": "nineteen optimizable weights", "block_idx": 12},
    # Block 14: submission_to_fsrs_rating
    {"search": "mapping from programming submission outcomes", "block_idx": 13},
]


def get_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def find_paragraph_by_text(doc, search_text, min_index=140000):
    """Find a paragraph containing search_text, return its endIndex."""
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        si = elem["startIndex"]
        if si < min_index:
            continue
        text = ""
        for el in elem["paragraph"].get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        if search_text.lower() in text.lower():
            return elem["endIndex"]
    return None


def find_code_image_after(doc, after_index):
    """Find the next inline image paragraph after a given index (within 2000 chars)."""
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        si = elem["startIndex"]
        if si < after_index or si > after_index + 2000:
            continue
        for el in elem["paragraph"].get("elements", []):
            if "inlineObjectElement" in el:
                obj_id = el["inlineObjectElement"].get("inlineObjectId", "")
                # Check if it's a code block image (iili.io)
                inline_objs = doc.get("inlineObjects", {})
                if obj_id in inline_objs:
                    props = inline_objs[obj_id].get("inlineObjectProperties", {}).get("embeddedObject", {})
                    uri = props.get("imageProperties", {}).get("sourceUri", "")
                    if "iili.io" in uri:
                        return elem["startIndex"], elem["endIndex"]
    return None, None


def find_table_start_after_insert(doc, insert_index):
    """After inserting a table, find its startIndex and the inner cell paragraph index."""
    for elem in doc["body"]["content"]:
        if "table" not in elem:
            continue
        si = elem["startIndex"]
        # Table should be near the insert index
        if abs(si - insert_index) > 100:
            continue
        table = elem["table"]
        # Navigate: table → tableRows[0] → tableCells[0] → content[0] → paragraph
        row = table["tableRows"][0]
        cell = row["tableCells"][0]
        cell_content = cell["content"][0]
        if "paragraph" in cell_content:
            cell_para_start = cell_content["startIndex"]
            cell_para_end = cell_content["endIndex"]
            return si, cell_para_start, cell_para_end
    return None, None, None


def build_syntax_highlight_requests(code, lang, text_start_index):
    """Build updateTextStyle requests for Pygments syntax highlighting."""
    lexer = LEXERS.get(lang, PythonLexer())
    tokens = list(lex(code, lexer))
    requests = []
    offset = text_start_index

    for ttype, value in tokens:
        if not value:
            continue
        token_start = offset
        token_end = offset + len(value)

        style_def = STYLE.style_for_token(ttype)
        color_hex = style_def.get("color")
        is_bold = style_def.get("bold", False)
        is_italic = style_def.get("italic", False)

        style_updates = {}
        fields = []

        if color_hex:
            r = int(color_hex[:2], 16) / 255.0
            g = int(color_hex[2:4], 16) / 255.0
            b = int(color_hex[4:6], 16) / 255.0
            style_updates["foregroundColor"] = {
                "color": {"rgbColor": {"red": r, "green": g, "blue": b}}
            }
            fields.append("foregroundColor")

        if is_bold:
            style_updates["bold"] = True
            fields.append("bold")

        if is_italic:
            style_updates["italic"] = True
            fields.append("italic")

        if fields:
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": token_start, "endIndex": token_end},
                    "textStyle": style_updates,
                    "fields": ",".join(fields),
                }
            })

        offset = token_end

    return requests


def add_line_numbers(code):
    """Add line numbers to code."""
    lines = code.split("\n")
    width = len(str(len(lines)))
    numbered = []
    for i, line in enumerate(lines, 1):
        numbered.append(f"{i:>{width}} | {line}")
    return "\n".join(numbered)


# ══════════════════════════════════════════════
# PHASE 1: Delete broken code-block images
# ══════════════════════════════════════════════
print("=== PHASE 1: Deleting broken code-block images ===")

doc = get_doc()

# Find all iili.io image paragraphs
code_img_paras = []
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    for el in elem["paragraph"].get("elements", []):
        if "inlineObjectElement" in el:
            obj_id = el["inlineObjectElement"].get("inlineObjectId", "")
            inline_objs = doc.get("inlineObjects", {})
            if obj_id in inline_objs:
                props = inline_objs[obj_id].get("inlineObjectProperties", {}).get("embeddedObject", {})
                uri = props.get("imageProperties", {}).get("sourceUri", "")
                if "iili.io" in uri:
                    code_img_paras.append({
                        "start": elem["startIndex"],
                        "end": elem["endIndex"],
                        "uri": uri,
                    })

print(f"  Found {len(code_img_paras)} code-block images to delete")

# Delete in reverse order
code_img_paras.sort(key=lambda p: p["start"], reverse=True)
for img_para in code_img_paras:
    reqs = [{"deleteContentRange": {"range": {"startIndex": img_para["start"], "endIndex": img_para["end"] - 1}}}]
    try:
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
        print(f"  Deleted image at [{img_para['start']}]")
    except Exception as e:
        print(f"  Error deleting [{img_para['start']}]: {e}")
    time.sleep(0.5)

print("  Phase 1 complete.\n")

# ══════════════════════════════════════════════
# PHASE 2: Insert code blocks as tables
# ══════════════════════════════════════════════
print("=== PHASE 2: Inserting code blocks as tables ===")

for anchor in ANCHORS:
    block = CODE_BLOCKS[anchor["block_idx"]]
    code = block["code"]
    lang = block["lang"]
    code_with_numbers = add_line_numbers(code)

    print(f"\n--- Block {anchor['block_idx']+1}: {block['first_line'][:50]} ---")

    # Step 1: Find anchor paragraph
    doc = get_doc()
    anchor_end = find_paragraph_by_text(doc, anchor["search"])
    if anchor_end is None:
        print(f"  ANCHOR NOT FOUND: '{anchor['search'][:40]}...'")
        continue
    print(f"  Anchor found, inserting table after index {anchor_end}")

    # Step 2: Check if there's already a broken image to skip over
    # (some images might not have been deleted if they were between anchor and next heading)

    # Step 3: Insert 1x1 table
    insert_idx = anchor_end  # Insert right after the anchor paragraph
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{"insertTable": {"rows": 1, "columns": 1, "location": {"index": insert_idx}}}]},
        ).execute()
        print(f"  Table inserted at {insert_idx}")
    except Exception as e:
        print(f"  ERROR inserting table: {e}")
        continue
    time.sleep(1)

    # Step 4: Re-read doc and find the table cell paragraph
    doc = get_doc()
    table_start, cell_para_start, cell_para_end = find_table_start_after_insert(doc, insert_idx)
    if table_start is None:
        print(f"  ERROR: Could not find inserted table near {insert_idx}")
        continue
    print(f"  Table at {table_start}, cell paragraph at [{cell_para_start}, {cell_para_end})")

    # Step 5: Insert code text into the cell
    # The cell paragraph has a trailing \n already, insert before it
    reqs = [{"insertText": {"location": {"index": cell_para_start}, "text": code_with_numbers}}]
    try:
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
        print(f"  Code text inserted ({len(code_with_numbers)} chars)")
    except Exception as e:
        print(f"  ERROR inserting text: {e}")
        continue
    time.sleep(0.5)

    # Step 6: Format text + cell + syntax highlighting
    text_end = cell_para_start + len(code_with_numbers)

    format_reqs = [
        # Text style: Courier New 10pt
        {
            "updateTextStyle": {
                "range": {"startIndex": cell_para_start, "endIndex": text_end},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Courier New"},
                    "fontSize": {"magnitude": 10, "unit": "PT"},
                    "bold": False,
                    "italic": False,
                },
                "fields": "weightedFontFamily,fontSize,bold,italic",
            }
        },
        # Paragraph style: tight line spacing, left-aligned
        {
            "updateParagraphStyle": {
                "range": {"startIndex": cell_para_start, "endIndex": text_end},
                "paragraphStyle": {
                    "lineSpacing": 115,
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 0, "unit": "PT"},
                    "alignment": "START",
                    "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                    "indentStart": {"magnitude": 0, "unit": "PT"},
                },
                "fields": "lineSpacing,spaceAbove,spaceBelow,alignment,indentFirstLine,indentStart",
            }
        },
        # Cell style: light gray background + padding
        {
            "updateTableCellStyle": {
                "tableCellStyle": {
                    "backgroundColor": {
                        "color": {"rgbColor": {"red": 0.96, "green": 0.96, "blue": 0.96}}
                    },
                    "paddingTop": {"magnitude": 8, "unit": "PT"},
                    "paddingBottom": {"magnitude": 8, "unit": "PT"},
                    "paddingLeft": {"magnitude": 10, "unit": "PT"},
                    "paddingRight": {"magnitude": 10, "unit": "PT"},
                },
                "tableStartLocation": {"index": table_start},
                "fields": "backgroundColor,paddingTop,paddingBottom,paddingLeft,paddingRight",
            }
        },
    ]

    # Add syntax highlighting
    # Need to map highlighting to the numbered code text
    # Line numbers are not part of the code, so highlight only the code portion
    # For simplicity, apply colors to the full text including line numbers
    # (line numbers will just stay default color which is fine)
    highlight_reqs = build_syntax_highlight_requests(code_with_numbers, lang, cell_para_start)
    format_reqs.extend(highlight_reqs)

    # Batch in chunks of 100
    for i in range(0, len(format_reqs), 100):
        batch = format_reqs[i:i + 100]
        try:
            service.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch}).execute()
        except Exception as e:
            print(f"  ERROR formatting batch {i//100}: {e}")
            break
        time.sleep(0.5)

    print(f"  Formatted: Courier New 10pt + gray bg + {len(highlight_reqs)} syntax colors")
    time.sleep(1)

print("\n=== DONE ===")
print(f"Processed {len(ANCHORS)} code blocks.")
