"""
Generate LIST OF TABLES and LIST OF FIGURES in the thesis Google Doc.
Replace placeholder text with actual caption lists.
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


def extract_captions(doc):
    """Extract Table and Figure captions from the doc body.
    Only include actual captions (short, title-like), not description sentences."""
    tables = []
    figures = []

    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        text = ""
        for el in elem["paragraph"].get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        stripped = text.strip()

        # Table captions: "Table X.Y. Title text" (not "Table X.Y. describes..." or "Table X.Y. maps...")
        t_match = re.match(r"^(Table \d+\.\d+)[.:]\s+(.+)", stripped)
        if t_match:
            label = t_match.group(1)
            caption = t_match.group(2).rstrip(".")
            # Filter out description sentences (start with lowercase verb)
            first_word = caption.split()[0].lower() if caption.split() else ""
            if first_word in ("presents", "maps", "consolidates", "summarizes",
                              "extends", "gives", "shows", "describes", "lists",
                              "compares", "illustrates", "provides", "contains"):
                continue
            tables.append({"label": label, "caption": caption})

        # Figure captions: "Figure X.Y. Title text"
        f_match = re.match(r"^(Figure \d+\.\d+)[.:]\s+(.+)", stripped)
        if f_match:
            label = f_match.group(1)
            caption = f_match.group(2).rstrip(".")
            first_word = caption.split()[0].lower() if caption.split() else ""
            if first_word in ("presents", "maps", "consolidates", "summarizes",
                              "extends", "gives", "shows", "describes", "lists",
                              "compares", "illustrates", "provides", "contains"):
                continue
            figures.append({"label": label, "caption": caption})

    return tables, figures


def sort_by_number(items):
    """Sort by chapter.number numerically."""
    def key(item):
        parts = item["label"].split()[-1].split(".")
        return (int(parts[0]), int(parts[1]))
    return sorted(items, key=key)


doc = get_doc()
tables, figures = extract_captions(doc)

# Deduplicate by label (keep first occurrence)
seen_t = set()
unique_tables = []
for t in tables:
    if t["label"] not in seen_t:
        seen_t.add(t["label"])
        unique_tables.append(t)

seen_f = set()
unique_figures = []
for f in figures:
    if f["label"] not in seen_f:
        seen_f.add(f["label"])
        unique_figures.append(f)

unique_tables = sort_by_number(unique_tables)
unique_figures = sort_by_number(unique_figures)

print("=== LIST OF TABLES ===")
for t in unique_tables:
    print(f"  {t['label']}. {t['caption'][:70]}")

print(f"\n=== LIST OF FIGURES ===")
for f in unique_figures:
    print(f"  {f['label']}. {f['caption'][:70]}")

# Build the text to insert
tables_text = "\n".join(f"{t['label']}. {t['caption']}" for t in unique_tables)
figures_text = "\n".join(f"{f['label']}. {f['caption']}" for f in unique_figures)

print(f"\n{len(unique_tables)} tables, {len(unique_figures)} figures")

# Find and replace placeholder text
# LIST OF TABLES placeholder: "[To be generated]" after "LIST OF TABLES" heading
# LIST OF FIGURES placeholder: "[To be generated]" after "LIST OF FIGURES" heading

doc = get_doc()

# Find the two placeholder paragraphs
lot_placeholder = None  # List of Tables
lof_placeholder = None  # List of Figures
in_lot = False
in_lof = False

for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    si = elem.get("startIndex", 0)
    ei = elem.get("endIndex", 0)
    text = ""
    for el in elem["paragraph"].get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    stripped = text.strip()

    if stripped == "LIST OF TABLES":
        in_lot = True
        in_lof = False
        continue
    if stripped == "LIST OF FIGURES":
        in_lof = True
        in_lot = False
        continue

    if in_lot and "[To be generated]" in stripped:
        lot_placeholder = {"start": si, "end": ei}
        in_lot = False
    if in_lof and "[To be generated]" in stripped:
        lof_placeholder = {"start": si, "end": ei}
        in_lof = False

print(f"\nLOT placeholder: {lot_placeholder}")
print(f"LOF placeholder: {lof_placeholder}")

if not lot_placeholder or not lof_placeholder:
    print("ERROR: Could not find placeholder text")
    sys.exit(1)

# Replace LOF first (higher index) then LOT
# LOF
reqs = [
    {"deleteContentRange": {"range": {"startIndex": lof_placeholder["start"], "endIndex": lof_placeholder["end"] - 1}}},
    {"insertText": {"location": {"index": lof_placeholder["start"]}, "text": figures_text + "\n"}},
]
service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
print("LIST OF FIGURES content inserted.")
time.sleep(1)

# Re-read doc for fresh indices
doc = get_doc()
# Re-find LOT placeholder
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    si = elem.get("startIndex", 0)
    ei = elem.get("endIndex", 0)
    text = ""
    for el in elem["paragraph"].get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    if "[To be generated]" in text.strip():
        lot_placeholder = {"start": si, "end": ei}
        break

# LOT
reqs = [
    {"deleteContentRange": {"range": {"startIndex": lot_placeholder["start"], "endIndex": lot_placeholder["end"] - 1}}},
    {"insertText": {"location": {"index": lot_placeholder["start"]}, "text": tables_text + "\n"}},
]
service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()
print("LIST OF TABLES content inserted.")
time.sleep(1)

# Format both lists: TNR 13pt, justified, line spacing 150%
doc = get_doc()

# Find the text ranges for both lists
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    text = ""
    for el in elem["paragraph"].get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    stripped = text.strip()
    if stripped == "LIST OF TABLES":
        lot_heading_end = elem["endIndex"]
    if stripped == "LIST OF FIGURES":
        lof_heading_end = elem["endIndex"]
    if stripped == "ABBREVIATIONS":
        abbr_heading_start = elem.get("startIndex", 0)

# The lists span from after heading to before next heading
# LOT: from lot_heading_end to LOF heading
# LOF: from lof_heading_end to ABSTRACT heading

# Apply formatting to both list areas
# Find exact ranges by looking for Table/Figure entries
format_reqs = []
for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    si = elem.get("startIndex", 0)
    ei = elem.get("endIndex", 0)
    text = ""
    for el in elem["paragraph"].get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    stripped = text.strip()
    if re.match(r"^(Table|Figure) \d+\.\d+\.", stripped):
        format_reqs.append({
            "updateParagraphStyle": {
                "range": {"startIndex": si, "endIndex": ei},
                "paragraphStyle": {
                    "lineSpacing": 150,
                    "spaceAbove": {"magnitude": 3, "unit": "PT"},
                    "spaceBelow": {"magnitude": 3, "unit": "PT"},
                    "alignment": "START",
                    "indentStart": {"magnitude": 0, "unit": "PT"},
                    "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                },
                "fields": "lineSpacing,spaceAbove,spaceBelow,alignment,indentStart,indentFirstLine",
            }
        })
        format_reqs.append({
            "updateTextStyle": {
                "range": {"startIndex": si, "endIndex": ei - 1},
                "textStyle": {
                    "weightedFontFamily": {"fontFamily": "Times New Roman"},
                    "fontSize": {"magnitude": 13, "unit": "PT"},
                    "bold": False,
                    "italic": False,
                },
                "fields": "weightedFontFamily,fontSize,bold,italic",
            }
        })

if format_reqs:
    for i in range(0, len(format_reqs), 50):
        batch = format_reqs[i:i + 50]
        service.documents().batchUpdate(documentId=DOC_ID, body={"requests": batch}).execute()
    print(f"Formatted {len(format_reqs) // 2} list entries.")

print("\nDone!")
