"""
Fix inline math in the thesis Google Doc.

For each $...$ delimited inline math block:
1. Parse the LaTeX content
2. Convert to formatted Google Docs text:
   - Strip $ delimiters
   - Replace LaTeX commands with Unicode equivalents
   - Apply subscript/superscript formatting via API
   - Apply italic + Cambria Math font to math content
3. Delete old text and insert formatted replacement

Run in phases to be safe.
"""
import importlib.util
import io
import json
import os
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

# ── LaTeX to Unicode mapping ──
LATEX_SYMBOLS = {
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠",
    r"\neg": "¬", r"\times": "×", r"\cdot": "·",
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ",
    r"\delta": "δ", r"\Delta": "Δ", r"\sigma": "σ",
    r"\theta": "θ", r"\lambda": "λ", r"\mu": "μ",
    r"\pi": "π", r"\phi": "φ", r"\psi": "ψ",
    r"\omega": "ω", r"\Omega": "Ω",
    r"\infty": "∞", r"\in": "∈", r"\notin": "∉",
    r"\subset": "⊂", r"\cup": "∪", r"\cap": "∩",
    r"\rightarrow": "→", r"\leftarrow": "←",
    r"\Rightarrow": "⇒", r"\Leftarrow": "⇐",
    r"\pm": "±", r"\approx": "≈", r"\sim": "∼",
    r"\hat": "̂",  # combining circumflex
    r"\bar": "̄",  # combining macron
}


def latex_to_segments(latex_str):
    """Convert a LaTeX inline math string to a list of text segments
    with formatting hints.

    Each segment: {"text": str, "sub": bool, "sup": bool, "roman": bool}
    """
    s = latex_str.strip()

    # Replace \text{...} with roman (non-italic) segments
    # We'll handle these specially
    segments = []

    # First pass: replace LaTeX symbols with Unicode
    for cmd, uni in LATEX_SYMBOLS.items():
        s = s.replace(cmd, uni)

    # Remove remaining \mathbb{1} → 𝟙
    s = s.replace(r"\mathbb{1}", "𝟙")

    # Remove \left and \right (just sizing hints)
    s = s.replace(r"\left", "").replace(r"\right", "")

    # Process \text{...} → mark as roman
    parts = []
    pos = 0
    for m in re.finditer(r'\\text\{([^}]+)\}', s):
        if m.start() > pos:
            parts.append({"text": s[pos:m.start()], "roman": False})
        parts.append({"text": m.group(1), "roman": True})
        pos = m.end()
    if pos < len(s):
        parts.append({"text": s[pos:], "roman": False})

    if not parts:
        parts = [{"text": s, "roman": False}]

    # Second pass: expand subscripts and superscripts within each part
    final_segments = []
    for part in parts:
        text = part["text"]
        roman = part["roman"]
        # Process _{...} and ^{...}
        i = 0
        while i < len(text):
            if i < len(text) - 1 and text[i] == '_' and text[i+1] == '{':
                # Find matching }
                j = text.find('}', i+2)
                if j == -1:
                    # No closing brace — treat rest as subscript
                    final_segments.append({
                        "text": text[i+2:],
                        "sub": True, "sup": False, "roman": roman
                    })
                    i = len(text)
                else:
                    final_segments.append({
                        "text": text[i+2:j],
                        "sub": True, "sup": False, "roman": roman
                    })
                    i = j + 1
            elif i < len(text) - 1 and text[i] == '^' and text[i+1] == '{':
                j = text.find('}', i+2)
                if j == -1:
                    final_segments.append({
                        "text": text[i+2:],
                        "sub": False, "sup": True, "roman": roman
                    })
                    i = len(text)
                else:
                    final_segments.append({
                        "text": text[i+2:j],
                        "sub": False, "sup": True, "roman": roman
                    })
                    i = j + 1
            elif text[i] == '_' and i + 1 < len(text) and text[i+1] not in '{':
                # Single char subscript: _x
                final_segments.append({
                    "text": text[i+1],
                    "sub": True, "sup": False, "roman": roman
                })
                i += 2
            elif text[i] == '^' and i + 1 < len(text) and text[i+1] not in '{':
                # Single char superscript
                final_segments.append({
                    "text": text[i+1],
                    "sub": False, "sup": True, "roman": roman
                })
                i += 2
            else:
                # Regular character - accumulate
                start = i
                while i < len(text) and text[i] not in '_^':
                    i += 1
                if i > start:
                    final_segments.append({
                        "text": text[start:i],
                        "sub": False, "sup": False, "roman": roman
                    })

    # Clean up: remove empty segments, strip remaining backslashes from unknown commands
    cleaned = []
    for seg in final_segments:
        t = seg["text"]
        # Remove unknown \commands but keep the argument
        t = re.sub(r'\\[a-zA-Z]+', '', t)
        # Remove stray braces
        t = t.replace('{', '').replace('}', '')
        if t:
            seg["text"] = t
            cleaned.append(seg)

    return cleaned


def find_dollar_math_in_doc(doc):
    """Find all $...$ inline math spans with their exact character indices."""
    matches = []

    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        # Check for inline objects (images) — skip paragraphs that are equation images
        has_image = any("inlineObjectElement" in el for el in para.get("elements", []))
        if has_image:
            continue

        for el in para.get("elements", []):
            if "textRun" not in el:
                continue
            text = el["textRun"]["content"]
            si = el["startIndex"]

            # Find $...$ patterns (non-greedy, single-line)
            for m in re.finditer(r'\$([^$]+)\$', text):
                abs_start = si + m.start()   # index of first $
                abs_end = si + m.end()       # index after last $
                latex = m.group(1)
                matches.append({
                    "start": abs_start,
                    "end": abs_end,
                    "latex": latex,
                    "full_match": m.group(0),
                })

    return matches


def apply_inline_math_fix(service, doc_id, match):
    """Replace a single $...$ span with formatted text."""
    segments = latex_to_segments(match["latex"])
    plain_text = "".join(seg["text"] for seg in segments)

    if not plain_text.strip():
        return False

    # Build requests: delete old text, insert new, apply formatting
    requests = []

    # Delete the $...$ text
    requests.append({
        "deleteContentRange": {
            "range": {
                "startIndex": match["start"],
                "endIndex": match["end"],
            }
        }
    })

    # Insert plain text (without $ delimiters)
    requests.append({
        "insertText": {
            "location": {"index": match["start"]},
            "text": plain_text,
        }
    })

    # Apply formatting to each segment
    offset = match["start"]
    for seg in segments:
        seg_start = offset
        seg_end = offset + len(seg["text"])

        style = {
            "weightedFontFamily": {"fontFamily": "Cambria Math"},
            "italic": not seg["roman"],  # Math vars are italic, \text{} is roman
        }
        fields = "weightedFontFamily,italic"

        if seg["sub"]:
            style["baselineOffset"] = "SUBSCRIPT"
            style["fontSize"] = {"magnitude": 10, "unit": "PT"}
            fields += ",baselineOffset,fontSize"
        elif seg["sup"]:
            style["baselineOffset"] = "SUPERSCRIPT"
            style["fontSize"] = {"magnitude": 10, "unit": "PT"}
            fields += ",baselineOffset,fontSize"
        else:
            style["baselineOffset"] = "NONE"
            fields += ",baselineOffset"

        requests.append({
            "updateTextStyle": {
                "range": {"startIndex": seg_start, "endIndex": seg_end},
                "textStyle": style,
                "fields": fields,
            }
        })

        offset = seg_end

    try:
        service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


# ── Main execution ──
if __name__ == "__main__":
    doc = service.documents().get(documentId=DOC_ID).execute()

    matches = find_dollar_math_in_doc(doc)
    print(f"Found {len(matches)} inline $...$ math spans")

    # Sort by position descending (process from end to start to preserve indices)
    matches.sort(key=lambda m: m["start"], reverse=True)

    success = 0
    fail = 0
    for i, match in enumerate(matches):
        # Preview
        segments = latex_to_segments(match["latex"])
        plain = "".join(seg["text"] for seg in segments)
        print(f"[{i+1}/{len(matches)}] [{match['start']}] ${match['latex'][:50]}$ -> {plain[:50]}")

        ok = apply_inline_math_fix(service, DOC_ID, match)
        if ok:
            success += 1
        else:
            fail += 1

        # Re-read doc every 10 operations to keep indices fresh
        # (processing in reverse order, so earlier indices should be stable)
        if (i + 1) % 10 == 0:
            print(f"  ... re-reading doc (progress: {success} ok, {fail} fail)")
            time.sleep(1)

        time.sleep(0.5)  # Rate limit

    print(f"\nDone: {success} fixed, {fail} failed out of {len(matches)} total")
