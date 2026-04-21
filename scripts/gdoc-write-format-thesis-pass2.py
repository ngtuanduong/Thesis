"""
gdoc-write-format-thesis-pass2: Fix heading level assignments.

- Promote Chapter 1/2/3 headings from HEADING_2 to HEADING_1
- Demote LaTeX equation HEADING_2 paragraphs to NORMAL_TEXT
- Demote reference entry "[1]..." from HEADING_2 to NORMAL_TEXT
- Remove empty HEADING_1 paragraph (clear its style to NORMAL_TEXT)

Usage:
    python scripts/gdoc-write-format-thesis-pass2.py
"""
import importlib.util
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID
doc = m.get_document(service, DOC_ID)

requests = []

# Indices of chapter title HEADING_2 paragraphs to promote to HEADING_1
promote_to_h1 = []
# Indices of equation/reference HEADING_2 to demote to NORMAL_TEXT
demote_to_normal = []
# Empty HEADING_1 to clear
clear_empty_h1 = []

for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    ps = para.get("paragraphStyle", {})
    nst = ps.get("namedStyleType", "NORMAL_TEXT")
    start = elem["startIndex"]
    end = elem["endIndex"]

    text = ""
    for el in para.get("elements", []):
        if "textRun" in el:
            text += el["textRun"]["content"]
    t = text.strip()

    if nst == "HEADING_2":
        # Chapter titles that should be HEADING_1
        if t.lower().startswith("chapter ") and ":" in t:
            promote_to_h1.append((start, end, t))
        # LaTeX equations incorrectly styled as headings
        elif any(kw in t for kw in ["\\frac", "\\text{", "\\tag", "\\min", "\\sigma", "\\hat"]):
            demote_to_normal.append((start, end, t[:60]))
        # Reference entry
        elif t.startswith("[1]"):
            demote_to_normal.append((start, end, t[:60]))

    elif nst == "HEADING_1" and not t:
        clear_empty_h1.append((start, end))

# Promote chapter titles to HEADING_1
for start, end, t in promote_to_h1:
    print(f"Promoting to HEADING_1: {t[:60]}")
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": "HEADING_1"},
            "fields": "namedStyleType",
        }
    })

# Demote equations/references to NORMAL_TEXT
for start, end, t in demote_to_normal:
    print(f"Demoting to NORMAL_TEXT: {t[:60]}")
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType",
        }
    })

# Clear empty HEADING_1
for start, end in clear_empty_h1:
    print(f"Clearing empty HEADING_1 at [{start}-{end}]")
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType",
        }
    })

if requests:
    print(f"\nSending {len(requests)} requests...")
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests},
    ).execute()
    print(f"Done. {len(result.get('replies', []))} replies.")
else:
    print("No changes needed.")
