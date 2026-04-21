"""
Convert raw Markdown **bold** markers to actual Google Docs bold formatting.
For each **text** occurrence:
1. Find the exact character indices of the ** delimiters
2. Delete the ** markers (4 chars total)
3. Apply bold=True to the enclosed text
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


def find_bold_markers(doc):
    """Find all **text** patterns with exact character indices."""
    markers = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        # Build text with absolute indices
        for el in para.get("elements", []):
            if "textRun" not in el:
                continue
            text = el["textRun"]["content"]
            el_start = el["startIndex"]

            for m_match in re.finditer(r"\*\*([^*]+)\*\*", text):
                abs_start = el_start + m_match.start()  # index of first *
                abs_end = el_start + m_match.end()      # index after last *
                inner_text = m_match.group(1)
                markers.append({
                    "abs_start": abs_start,
                    "abs_end": abs_end,
                    "inner_text": inner_text,
                    "full_match": m_match.group(0),
                })

    return markers


def fix_one_marker(marker):
    """Fix a single **text** marker: remove ** and apply bold."""
    # Strategy: use replaceAllText to remove the ** markers,
    # then apply bold to the text content.
    # But replaceAllText is imprecise for repeated text.
    # Instead, use deleteContentRange + updateTextStyle with exact indices.

    start = marker["abs_start"]
    end = marker["abs_end"]
    inner = marker["inner_text"]

    # Step 1: Delete the closing ** (2 chars at end-2 to end)
    # Step 2: Delete the opening ** (2 chars at start to start+2)
    # Step 3: Apply bold to the inner text (now at start to start+len(inner))
    # Process closing first (higher index) to avoid shifting
    reqs = [
        # Delete closing **
        {"deleteContentRange": {"range": {"startIndex": end - 2, "endIndex": end}}},
        # Delete opening **
        {"deleteContentRange": {"range": {"startIndex": start, "endIndex": start + 2}}},
        # Apply bold to inner text (after deleting 2 chars from front, text starts at 'start')
        {"updateTextStyle": {
            "range": {"startIndex": start, "endIndex": start + len(inner)},
            "textStyle": {"bold": True},
            "fields": "bold",
        }},
    ]

    service.documents().batchUpdate(documentId=DOC_ID, body={"requests": reqs}).execute()


# Main
doc = get_doc()
markers = find_bold_markers(doc)
print(f"Found {len(markers)} **bold** markers")

# Process ONE at a time, re-reading doc each time (indices shift after each edit)
fixed = 0
for i in range(len(markers)):
    doc = get_doc()
    current_markers = find_bold_markers(doc)
    if not current_markers:
        break

    # Always fix the LAST one (highest index) to avoid shifting earlier indices
    marker = current_markers[-1]
    try:
        fix_one_marker(marker)
        fixed += 1
        print(f"  [{fixed}] Fixed: **{marker['inner_text'][:50]}**")
    except Exception as e:
        print(f"  ERROR: {e} — skipping **{marker['inner_text'][:30]}**")
        # Try next one
        if len(current_markers) > 1:
            marker = current_markers[-2]
            try:
                fix_one_marker(marker)
                fixed += 1
                print(f"  [{fixed}] Fixed (retry): **{marker['inner_text'][:50]}**")
            except Exception as e2:
                print(f"  SKIP: {e2}")

    time.sleep(0.3)

print(f"\nDone: {fixed} markers converted to bold formatting.")

# Verify
doc = get_doc()
remaining = find_bold_markers(doc)
if remaining:
    print(f"WARNING: {len(remaining)} markers still remain:")
    for r in remaining[:5]:
        print(f"  **{r['inner_text'][:50]}**")
else:
    print("All markers converted successfully.")
