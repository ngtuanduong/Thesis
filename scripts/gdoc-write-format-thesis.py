"""
gdoc-write-format-thesis: Apply Decision 612/QD-DHHN formatting to the thesis doc.

Applies:
  - Page margins (top 3cm, bottom 3cm, left 3.5cm, right 2cm)
  - Named style updates for NORMAL_TEXT, HEADING_1..4
  - Clears conflicting inline overrides on heading/body paragraphs

Usage:
    python scripts/gdoc-write-format-thesis.py
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

# ── Conversion helpers ──────────────────────────────────────────
def cm_to_pt(cm):
    return round(cm * 28.3465, 2)

# Margins in PT
MARGIN_TOP = cm_to_pt(3)      # 85.04
MARGIN_BOTTOM = cm_to_pt(3)   # 85.04
MARGIN_LEFT = cm_to_pt(3.5)   # 99.21
MARGIN_RIGHT = cm_to_pt(2)    # 56.69

# ── Build requests ──────────────────────────────────────────────
requests = []

# ── A. Page margins ─────────────────────────────────────────────
requests.append({
    "updateDocumentStyle": {
        "documentStyle": {
            "marginTop":    {"magnitude": MARGIN_TOP,    "unit": "PT"},
            "marginBottom": {"magnitude": MARGIN_BOTTOM, "unit": "PT"},
            "marginLeft":   {"magnitude": MARGIN_LEFT,   "unit": "PT"},
            "marginRight":  {"magnitude": MARGIN_RIGHT,  "unit": "PT"},
        },
        "fields": "marginTop,marginBottom,marginLeft,marginRight",
    }
})

# ── B-F. Named style definitions ───────────────────────────────
# This globally redefines every paragraph tagged with that style.
named_style_updates = []

# NORMAL_TEXT: Times New Roman 13pt, justified, line spacing 1.5, no extra spacing
named_style_updates.append({
    "namedStyleType": "NORMAL_TEXT",
    "textStyle": {
        "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        "fontSize": {"magnitude": 13, "unit": "PT"},
        "bold": False,
        "italic": False,
    },
    "paragraphStyle": {
        "alignment": "JUSTIFIED",
        "lineSpacing": 150,       # percentage (1.5 = 150)
        "spaceAbove": {"magnitude": 0, "unit": "PT"},
        "spaceBelow": {"magnitude": 0, "unit": "PT"},
    },
})

# HEADING_1: Chapter titles — TNR 16pt BOLD, CENTER, spacing 32/32, 1.5
named_style_updates.append({
    "namedStyleType": "HEADING_1",
    "textStyle": {
        "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        "fontSize": {"magnitude": 16, "unit": "PT"},
        "bold": True,
        "italic": False,
    },
    "paragraphStyle": {
        "alignment": "CENTER",
        "lineSpacing": 150,
        "spaceAbove": {"magnitude": 32, "unit": "PT"},
        "spaceBelow": {"magnitude": 32, "unit": "PT"},
    },
})

# HEADING_2: Section — TNR 14pt BOLD, JUSTIFIED, spacing 6/6, 1.5
named_style_updates.append({
    "namedStyleType": "HEADING_2",
    "textStyle": {
        "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        "fontSize": {"magnitude": 14, "unit": "PT"},
        "bold": True,
        "italic": False,
    },
    "paragraphStyle": {
        "alignment": "JUSTIFIED",
        "lineSpacing": 150,
        "spaceAbove": {"magnitude": 6, "unit": "PT"},
        "spaceBelow": {"magnitude": 6, "unit": "PT"},
    },
})

# HEADING_3: Subsection — TNR 13pt NOT bold, JUSTIFIED, spacing 6/6, 1.5
named_style_updates.append({
    "namedStyleType": "HEADING_3",
    "textStyle": {
        "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        "fontSize": {"magnitude": 13, "unit": "PT"},
        "bold": False,
        "italic": False,
    },
    "paragraphStyle": {
        "alignment": "JUSTIFIED",
        "lineSpacing": 150,
        "spaceAbove": {"magnitude": 6, "unit": "PT"},
        "spaceBelow": {"magnitude": 6, "unit": "PT"},
    },
})

# HEADING_4: Sub-subsection — TNR 13pt ITALIC not bold, JUSTIFIED, 6/6, 1.5
named_style_updates.append({
    "namedStyleType": "HEADING_4",
    "textStyle": {
        "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        "fontSize": {"magnitude": 13, "unit": "PT"},
        "bold": False,
        "italic": True,
    },
    "paragraphStyle": {
        "alignment": "JUSTIFIED",
        "lineSpacing": 150,
        "spaceAbove": {"magnitude": 6, "unit": "PT"},
        "spaceBelow": {"magnitude": 6, "unit": "PT"},
    },
})

for ns in named_style_updates:
    requests.append({
        "updateNamedStyle": {
            "namedStyle": ns,
            "fields": (
                "named_style_type,"
                "text_style.weighted_font_family,"
                "text_style.font_size,"
                "text_style.bold,"
                "text_style.italic,"
                "paragraph_style.alignment,"
                "paragraph_style.line_spacing,"
                "paragraph_style.space_above,"
                "paragraph_style.space_below"
            ),
        }
    })

# ── Clear inline overrides on heading paragraphs ────────────────
# After updating named styles, paragraphs with inline overrides
# (e.g. fontSize set directly on the paragraph) will still show
# the OLD inline value. We need to clear those overrides so the
# named style takes effect.

doc = m.get_document(service, DOC_ID)

heading_styles = {"HEADING_1", "HEADING_2", "HEADING_3", "HEADING_4"}

for elem in doc["body"]["content"]:
    if "paragraph" not in elem:
        continue
    para = elem["paragraph"]
    ps = para.get("paragraphStyle", {})
    nst = ps.get("namedStyleType", "NORMAL_TEXT")

    start = elem["startIndex"]
    end = elem["endIndex"]

    if nst in heading_styles:
        # Clear paragraph-level inline overrides (alignment, spacing, lineSpacing)
        # that conflict with the named style definition
        has_inline_ps = any(
            k in ps for k in ["alignment", "lineSpacing", "spaceAbove", "spaceBelow"]
            if k != "namedStyleType"
        )
        if has_inline_ps:
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {
                        # Set to the named style's values to override any inline
                    },
                    "fields": "alignment,lineSpacing,spaceAbove,spaceBelow",
                }
            })

        # Clear text-level inline overrides (fontSize, fontFamily, bold, italic)
        for el in para.get("elements", []):
            tr = el.get("textRun")
            if not tr:
                continue
            ts = tr.get("textStyle", {})
            has_inline_ts = any(
                k in ts for k in ["fontSize", "weightedFontFamily", "bold", "italic"]
            )
            if has_inline_ts:
                requests.append({
                    "updateTextStyle": {
                        "range": {
                            "startIndex": el["startIndex"],
                            "endIndex": el["endIndex"],
                        },
                        "textStyle": {},
                        "fields": "fontSize,weightedFontFamily,bold,italic",
                    }
                })

    elif nst == "NORMAL_TEXT":
        # For body text, clear inline font/size overrides so named style applies
        # But preserve intentional formatting (e.g., bold for emphasis within text,
        # cover page formatting). Only clear fontSize and fontFamily overrides.
        for el in para.get("elements", []):
            tr = el.get("textRun")
            if not tr:
                continue
            ts = tr.get("textStyle", {})
            # Clear fontSize if it's not 13pt (the target), and fontFamily if not TNR
            font_size = ts.get("fontSize", {}).get("magnitude")
            font_family = ts.get("weightedFontFamily", {}).get("fontFamily")

            fields_to_clear = []
            if font_size is not None and font_size != 13:
                fields_to_clear.append("fontSize")
            if font_family is not None and font_family != "Times New Roman":
                fields_to_clear.append("weightedFontFamily")

            if fields_to_clear:
                requests.append({
                    "updateTextStyle": {
                        "range": {
                            "startIndex": el["startIndex"],
                            "endIndex": el["endIndex"],
                        },
                        "textStyle": {},
                        "fields": ",".join(fields_to_clear),
                    }
                })

# ── Execute ─────────────────────────────────────────────────────
print(f"Sending {len(requests)} requests to Google Docs API...")
result = service.documents().batchUpdate(
    documentId=DOC_ID,
    body={"requests": requests},
).execute()
print(f"Done. {len(result.get('replies', []))} replies received.")
print("Formatting applied successfully.")
