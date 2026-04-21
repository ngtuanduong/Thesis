"""
gdoc-write-appendix: Insert full Appendix content into thesis Google Doc,
replacing the "[To be added]" placeholder under the APPENDIX heading.

Parses appendix.md into structured blocks (headings, body, code, tables)
and inserts them with HANU formatting using a single advancing cursor.
"""
import importlib.util
import io
import os
import re
import sys
import time
import warnings
from collections import Counter

warnings.filterwarnings("ignore")
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


def batch_update(requests):
    if not requests:
        return None
    return service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()


def parse_bold(text):
    """Parse **bold** markers, return (clean_text, [(start, end), ...])"""
    ranges = []
    clean = ""
    last_end = 0
    for match in re.finditer(r'\*\*(.+?)\*\*', text):
        clean += text[last_end:match.start()]
        bs = len(clean)
        clean += match.group(1)
        be = len(clean)
        ranges.append((bs, be))
        last_end = match.end()
    clean += text[last_end:]
    return clean, ranges


def parse_italic(text):
    """Parse *italic* markers (single asterisk), return (clean_text, [(start, end), ...])"""
    ranges = []
    clean = ""
    last_end = 0
    for match in re.finditer(r'(?<!\*)\*([^*]+?)\*(?!\*)', text):
        clean += text[last_end:match.start()]
        s = len(clean)
        clean += match.group(1)
        e = len(clean)
        ranges.append((s, e))
        last_end = match.end()
    clean += text[last_end:]
    return clean, ranges


def clean_md_text(text):
    """Clean markdown artifacts from text."""
    text = text.replace("&emsp;", "\t")
    text = text.replace("\\ldots", "\u2026")
    text = text.replace("\\to", "\u2192")
    # Remove $ math delimiters but keep content
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    text = text.replace("---", "\u2014")
    # Clean backtick code markers
    # Leave them as is for now - they mark inline code
    return text


def parse_markdown_table(lines):
    """Parse markdown table lines into rows of cells. Skip separator row."""
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        rows.append(cells)
    return rows


# =============================================================================
# Parse appendix.md
# =============================================================================

md_path = r"c:\Users\duong\WebstormProjects\Thesis\documents\thesis-chapters\appendix.md"
with open(md_path, "r", encoding="utf-8") as f:
    md_lines = f.read().split("\n")


def parse_md_to_blocks(lines):
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Heading 3
        if line.startswith("### "):
            blocks.append(("heading3", line[4:].strip()))
            i += 1
            continue

        # Heading 2
        if line.startswith("## "):
            blocks.append(("heading2", line[3:].strip()))
            i += 1
            continue

        # Heading 1
        if re.match(r'^# ', line):
            blocks.append(("heading1", line[2:].strip()))
            i += 1
            continue

        # Code block
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            blocks.append(("code", "\n".join(code_lines)))
            continue

        # Horizontal rule
        if line.strip() == "---":
            i += 1
            continue

        # Table
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            rows = parse_markdown_table(table_lines)
            if rows:
                blocks.append(("table", rows))
            continue

        # Empty line
        if line.strip() == "":
            i += 1
            continue

        # Body paragraph
        para_lines = []
        while i < len(lines):
            l = lines[i]
            if (l.strip() == "" or l.startswith("#") or
                l.strip().startswith("```") or l.strip().startswith("|") or
                l.strip() == "---"):
                break
            para_lines.append(l)
            i += 1
        if para_lines:
            blocks.append(("body", " ".join(para_lines)))

    return blocks


all_blocks = parse_md_to_blocks(md_lines)
print(f"Parsed {len(all_blocks)} blocks")
for t, c in sorted(Counter(b[0] for b in all_blocks).items()):
    print(f"  {t}: {c}")


# =============================================================================
# Find insertion point
# =============================================================================

doc = get_doc()
insert_at = None
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
    if style == "HEADING_1" and text.strip() == "APPENDIX":
        insert_at = elem["endIndex"]
        break

if insert_at is None:
    print("ERROR: Could not find APPENDIX heading")
    sys.exit(1)

# Check if there's an empty paragraph right after and delete it
for elem in doc["body"]["content"]:
    if elem.get("startIndex", 0) == insert_at:
        if "paragraph" in elem:
            ptext = ""
            for el in elem["paragraph"].get("elements", []):
                if "textRun" in el:
                    ptext += el["textRun"]["content"]
            if ptext.strip() == "" or ptext.strip() == "[To be added]":
                # Delete this empty/placeholder paragraph content
                if elem["endIndex"] - elem["startIndex"] > 1:
                    batch_update([{
                        "deleteContentRange": {
                            "range": {
                                "startIndex": elem["startIndex"],
                                "endIndex": elem["endIndex"] - 1
                            }
                        }
                    }])
                    doc = get_doc()
                    # Re-find insertion point
                    for e2 in doc["body"]["content"]:
                        if "paragraph" in e2:
                            p2 = e2["paragraph"]
                            t2 = ""
                            for el in p2.get("elements", []):
                                if "textRun" in el:
                                    t2 += el["textRun"]["content"]
                            s2 = p2.get("paragraphStyle", {}).get("namedStyleType", "")
                            if s2 == "HEADING_1" and t2.strip() == "APPENDIX":
                                insert_at = e2["endIndex"]
                                break
        break

print(f"Insertion point: {insert_at}")


# =============================================================================
# Insert all blocks sequentially with a single advancing cursor
# =============================================================================

# Strategy for each block type:
# - text blocks (heading, body, code): insert text at cursor, then format, advance cursor
# - table blocks: insert table at cursor, fill cells, format, advance cursor
#
# We process blocks in small batches to manage API calls.
# For each batch: insert text -> format text -> insert tables

def process_text_batch(blocks_with_indices, cursor):
    """Insert a batch of text blocks. Returns new cursor position.
    blocks_with_indices: list of (block_type, block_content)
    """
    if not blocks_with_indices:
        return cursor

    # Build combined text
    full_text = ""
    para_info = []  # (type, offset_start, offset_end, bold_ranges, italic_ranges, original_text)

    for btype, btext in blocks_with_indices:
        if btype == "code":
            start_off = len(full_text)
            full_text += btext + "\n"
            end_off = len(full_text)
            para_info.append(("code", start_off, end_off, [], [], btext))
        else:
            cleaned = clean_md_text(btext)
            # Parse bold first
            cleaned, bolds = parse_bold(cleaned)
            # Parse italic
            cleaned, italics = parse_italic(cleaned)

            start_off = len(full_text)
            full_text += cleaned + "\n"
            end_off = len(full_text)
            para_info.append((btype, start_off, end_off, bolds, italics, cleaned))

    # Insert text
    batch_update([{
        "insertText": {
            "location": {"index": cursor},
            "text": full_text
        }
    }])

    # Format each paragraph
    fmt = []
    for ptype, s_off, e_off, bolds, italics, clean in para_info:
        abs_s = cursor + s_off
        abs_e = cursor + e_off

        if ptype == "heading1":
            fmt.append({"updateParagraphStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_1", "alignment": "CENTER",
                    "spaceAbove": {"magnitude": 32, "unit": "PT"},
                    "spaceBelow": {"magnitude": 32, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e - 1},
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 16, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }})

        elif ptype == "heading2":
            fmt.append({"updateParagraphStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_2", "alignment": "JUSTIFIED",
                    "spaceAbove": {"magnitude": 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e - 1},
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 14, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }})

        elif ptype == "heading3":
            fmt.append({"updateParagraphStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e},
                "paragraphStyle": {
                    "namedStyleType": "HEADING_3", "alignment": "JUSTIFIED",
                    "spaceAbove": {"magnitude": 6, "unit": "PT"},
                    "spaceBelow": {"magnitude": 6, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"
            }})
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e - 1},
                "textStyle": {
                    "bold": True,
                    "fontSize": {"magnitude": 13, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }})

        elif ptype == "code":
            # Code: Courier New 10pt, left-aligned, single spacing
            code_lines = clean.split("\n")
            line_start = abs_s
            for cl in code_lines:
                line_end = line_start + len(cl) + 1
                fmt.append({"updateParagraphStyle": {
                    "range": {"startIndex": line_start, "endIndex": min(line_end, abs_e)},
                    "paragraphStyle": {
                        "namedStyleType": "NORMAL_TEXT", "alignment": "START",
                        "lineSpacing": 100,
                        "spaceAbove": {"magnitude": 0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 0, "unit": "PT"},
                    },
                    "fields": "namedStyleType,alignment,lineSpacing,spaceAbove,spaceBelow"
                }})
                line_start = line_end
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e - 1},
                "textStyle": {
                    "bold": False,
                    "fontSize": {"magnitude": 10, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Courier New"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }})

        else:
            # body text
            fmt.append({"updateParagraphStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e},
                "paragraphStyle": {
                    "namedStyleType": "NORMAL_TEXT", "alignment": "JUSTIFIED",
                    "lineSpacing": 150,
                    "spaceAbove": {"magnitude": 0, "unit": "PT"},
                    "spaceBelow": {"magnitude": 0, "unit": "PT"},
                },
                "fields": "namedStyleType,alignment,lineSpacing,spaceAbove,spaceBelow"
            }})
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s, "endIndex": abs_e - 1},
                "textStyle": {
                    "bold": False,
                    "fontSize": {"magnitude": 13, "unit": "PT"},
                    "weightedFontFamily": {"fontFamily": "Times New Roman"}
                },
                "fields": "bold,fontSize,weightedFontFamily"
            }})

        # Apply bold ranges
        for bs, be in bolds:
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s + bs, "endIndex": abs_s + be},
                "textStyle": {"bold": True},
                "fields": "bold"
            }})

        # Apply italic ranges
        for si, ei in italics:
            fmt.append({"updateTextStyle": {
                "range": {"startIndex": abs_s + si, "endIndex": abs_s + ei},
                "textStyle": {"italic": True},
                "fields": "italic"
            }})

    if fmt:
        batch_update(fmt)

    return cursor + len(full_text)


def insert_table_at(cursor, rows):
    """Insert a markdown table as a native Google Docs table at cursor.
    Returns new cursor position (after the table).
    """
    num_rows = len(rows)
    num_cols = len(rows[0]) if rows else 0
    if num_rows == 0 or num_cols == 0:
        return cursor

    # Insert table
    batch_update([{
        "insertTable": {
            "rows": num_rows,
            "columns": num_cols,
            "location": {"index": cursor}
        }
    }])

    # Re-read doc to find the table
    doc = get_doc()
    table_elem = None
    for elem in doc["body"]["content"]:
        if "table" in elem and elem.get("startIndex", 0) >= cursor:
            table_elem = elem
            break

    if not table_elem:
        print(f"  WARNING: Could not find inserted table near {cursor}")
        return cursor + 10  # rough estimate

    table = table_elem["table"]

    # Fill cells (in reverse order to avoid index shifting)
    fill_requests = []
    for row_i in range(num_rows - 1, -1, -1):
        if row_i >= len(table.get("tableRows", [])):
            continue
        tr = table["tableRows"][row_i]
        for col_i in range(num_cols - 1, -1, -1):
            if col_i >= len(tr.get("tableCells", [])):
                continue
            cell = tr["tableCells"][col_i]
            cell_content = cell.get("content", [])
            if not cell_content:
                continue
            cell_start = cell_content[0]["startIndex"]

            cell_text = rows[row_i][col_i] if col_i < len(rows[row_i]) else ""
            cell_text = clean_md_text(cell_text)
            cell_clean, _ = parse_bold(cell_text)
            cell_clean, _ = parse_italic(cell_clean)

            if cell_clean:
                fill_requests.append({
                    "insertText": {
                        "location": {"index": cell_start},
                        "text": cell_clean
                    }
                })

    if fill_requests:
        batch_update(fill_requests)

    # Re-read for formatting
    doc = get_doc()
    table_elem = None
    for elem in doc["body"]["content"]:
        if "table" in elem and elem.get("startIndex", 0) >= cursor:
            table_elem = elem
            break

    if table_elem:
        table = table_elem["table"]
        fmt = []

        for row_i, tr in enumerate(table.get("tableRows", [])):
            for col_i, cell in enumerate(tr.get("tableCells", [])):
                for para in cell.get("content", []):
                    if "paragraph" not in para:
                        continue
                    ps = para["startIndex"]
                    pe = para["endIndex"]

                    fmt.append({"updateParagraphStyle": {
                        "range": {"startIndex": ps, "endIndex": pe},
                        "paragraphStyle": {
                            "namedStyleType": "NORMAL_TEXT",
                            "lineSpacing": 100,
                            "spaceAbove": {"magnitude": 1, "unit": "PT"},
                            "spaceBelow": {"magnitude": 1, "unit": "PT"},
                        },
                        "fields": "namedStyleType,lineSpacing,spaceAbove,spaceBelow"
                    }})

                    if pe - 1 > ps:
                        ts = {"fontSize": {"magnitude": 10, "unit": "PT"},
                              "weightedFontFamily": {"fontFamily": "Times New Roman"}}
                        fields = "fontSize,weightedFontFamily"
                        if row_i == 0:
                            ts["bold"] = True
                            fields += ",bold"

                        fmt.append({"updateTextStyle": {
                            "range": {"startIndex": ps, "endIndex": pe - 1},
                            "textStyle": ts,
                            "fields": fields
                        }})

        if fmt:
            batch_update(fmt)

        # Get table end index
        doc = get_doc()
        for elem in doc["body"]["content"]:
            if "table" in elem and elem.get("startIndex", 0) >= cursor:
                return elem["endIndex"]

    return cursor + 10


# =============================================================================
# Main: process all blocks sequentially
# =============================================================================

print(f"\nStarting insertion at index {insert_at}")
print("=" * 60)

cursor = insert_at
text_batch = []  # accumulate text blocks, flush when we hit a table
total_tables = 0
total_text_blocks = 0
section_tracker = []

for i, (btype, bcontent) in enumerate(all_blocks):
    if btype == "table":
        # Flush any pending text blocks first
        if text_batch:
            cursor = process_text_batch(text_batch, cursor)
            total_text_blocks += len(text_batch)
            text_batch = []

        # Insert table
        rows = bcontent
        print(f"  Block {i}: TABLE {len(rows)}x{len(rows[0]) if rows else 0}")
        cursor = insert_table_at(cursor, rows)
        total_tables += 1
        time.sleep(0.3)
    else:
        text_batch.append((btype, bcontent))

        # Track section names
        if btype in ("heading1", "heading2"):
            section_tracker.append(bcontent)
            print(f"  Block {i}: {btype.upper()} - {bcontent[:60]}")

        # Flush every ~30 text blocks to avoid too-large batches
        if len(text_batch) >= 30:
            cursor = process_text_batch(text_batch, cursor)
            total_text_blocks += len(text_batch)
            text_batch = []
            time.sleep(0.3)

# Flush remaining text blocks
if text_batch:
    cursor = process_text_batch(text_batch, cursor)
    total_text_blocks += len(text_batch)

print(f"\nInserted {total_text_blocks} text blocks, {total_tables} tables")
print(f"Cursor advanced from {insert_at} to {cursor} ({cursor - insert_at} chars)")


# =============================================================================
# Verification
# =============================================================================

print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

doc = get_doc()
found = False
p_count = 0
t_count = 0
h_count = 0

for elem in doc["body"]["content"]:
    if "paragraph" in elem:
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")

        if style == "HEADING_1" and text.strip() == "APPENDIX":
            found = True
            continue

        if found:
            # Stop if we hit a non-appendix heading1
            if style == "HEADING_1" and not any(kw in text.upper() for kw in
                ["APPENDIX", "EVALUATION", "KNOWLEDGE", "APPENDICES"]):
                break
            p_count += 1
            if "HEADING" in style:
                h_count += 1
                print(f"  [{style:12s}] {text.strip()[:80]}")

    elif "table" in elem and found:
        t_count += 1
        rows = len(elem["table"].get("tableRows", []))
        cols = len(elem["table"]["tableRows"][0].get("tableCells", [])) if rows else 0
        print(f"  [TABLE       ] {rows}x{cols}")

print(f"\nSummary:")
print(f"  Sections: {section_tracker}")
print(f"  Headings found: {h_count}")
print(f"  Paragraphs: {p_count}")
print(f"  Tables: {t_count}")
print(f"\nDone!")
