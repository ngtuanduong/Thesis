"""
gdoc-write-conf-format: Apply formatting-only revisions (Priority 3) to the
conference-paper Google Doc. Run after gdoc-write-conf-content.py.

Actions:
  1. Italicise math variables throughout the body: θ_m, θ_p, K (K-factor), δ,
     w₁, w₂, w₃, and the "n = 40-60" occurrence. Uses Unicode subscripts for
     θ_m and θ_p (θₘ / θₚ) so the rendered doc shows real subscripts instead
     of underscore notation.
  2. Promote numbered section/subsection headings to HEADING_2 / HEADING_3
     paragraph styles so toc depth is consistent.
  3. Caption unification:
     - Replace "Source: authors' own synthesis." with "Source: authors' own work."
     - For every "Figure N." and "Table N." caption anchor, set that prefix to
       bold and ensure the rest of the line uses the default (non-italic,
       non-bold) body style except for the "Source:" tail which stays regular.

All locate-by-text operations use the post-Priority-0..6 doc body as the
authoritative source.

Usage:
    GDOC_KEY_FILE=/Users/avada/Downloads/infra-inkwell-465003-f2-369235afe5ac.json \
    GDOC_DOC_ID=1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs \
    python3 scripts/gdoc-write-conf-format.py
"""
import io
import os
import sys
import importlib.util

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth", os.path.join(HERE, "gdoc-util-auth.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

service = mod.get_docs_service()
DOC_ID = os.environ.get("GDOC_DOC_ID") or mod.DOC_ID


def fetch_doc():
    return service.documents().get(documentId=DOC_ID).execute()


def iter_text_with_index(doc):
    """Yield (startIndex, text) for each paragraph text, along with the raw body list."""
    out = []
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        runs = []
        for el in para.get("elements", []):
            if "textRun" in el:
                tr = el["textRun"]
                text += tr["content"]
                runs.append((el["startIndex"], el["endIndex"], tr["content"], tr.get("textStyle", {})))
        out.append({
            "startIndex": elem["startIndex"],
            "endIndex": elem["endIndex"],
            "text": text,
            "runs": runs,
            "style": para.get("paragraphStyle", {}),
        })
    return out


def find_all_offsets(paragraphs, needle):
    """Yield absolute (startIndex, endIndex) for every occurrence of `needle` in the body."""
    for p in paragraphs:
        text = p["text"]
        base = p["startIndex"]
        start_in_para = 0
        while True:
            idx = text.find(needle, start_in_para)
            if idx < 0:
                break
            # Map idx in paragraph text to absolute doc index by walking runs
            remaining = idx
            abs_start = None
            for rs, re_, rt, _ts in p["runs"]:
                if remaining < len(rt):
                    abs_start = rs + remaining
                    break
                remaining -= len(rt)
            if abs_start is None:
                break
            yield abs_start, abs_start + len(needle)
            start_in_para = idx + len(needle)


# ------------------------------------------------------------------
# Helpers to build requests
# ------------------------------------------------------------------

def italicize_request(start, end):
    return {
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "textStyle": {"italic": True},
            "fields": "italic",
        }
    }


def bold_request(start, end):
    return {
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "textStyle": {"bold": True},
            "fields": "bold",
        }
    }


def unbold_unitalic_request(start, end):
    return {
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "textStyle": {"bold": False, "italic": False},
            "fields": "bold,italic",
        }
    }


def set_heading_request(start, end, level):
    return {
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": f"HEADING_{level}"},
            "fields": "namedStyleType",
        }
    }


def replace_text_request(find, repl):
    return {
        "replaceAllText": {
            "containsText": {"text": find, "matchCase": True},
            "replaceText": repl,
        }
    }


# ------------------------------------------------------------------
# 1a. Replace "θ_m" and "θ_p" underscore forms with real Unicode subscripts θₘ / θₚ
#     Using Unicode: ₘ (U+2098), ₚ (U+209A).
#     Also swap the subscript numerals on w₁..w₃ (they are already Unicode subscripts
#     in the source) by keeping them as-is; italicising the base letter "w" is done
#     via a separate pass.
# ------------------------------------------------------------------

SUBSCRIPT_REPLACEMENTS = [
    ("θ_m", "θₘ"),
    ("θ_p", "θₚ"),
]

# ------------------------------------------------------------------
# 1b. Italicise math variables by per-occurrence updateTextStyle over the
#     exact byte range for that letter.
#
# Targets (per plan Priority 3A):
#   - θ in every θₘ / θₚ occurrence (italicise the theta character)
#   - K in "K = 25" (no longer in body; kept for safety if the pilot calibration
#     text reintroduces it), "K-factor", "K_max", "K_min"
#   - δ in "δ ∈ [50, 250]"
#   - w in "w₁ = 0.5", "w₂ = 0.3", "w₃ = 0.2"
#   - n in "n = 40–60"
# We italicise only the one letter per match, not the surrounding text.
# ------------------------------------------------------------------

ITALIC_LETTER_CONTEXTS = [
    # (full_match_needle_in_body, letter_character, offset_of_letter_in_needle)
    # θₘ
    ("θₘ", "θ", 0),
    # θₚ
    ("θₚ", "θ", 0),
    # "K-factor"
    ("K-factor", "K", 0),
    # "K_max"
    ("K_max", "K", 0),
    # "K_min"
    ("K_min", "K", 0),
    # "K = 25" not guaranteed in body after rewrite — skip.
    # δ in "δ ∈"
    ("δ ∈", "δ", 0),
    # w subscripts in reward weights
    ("w₁", "w", 0),
    ("w₂", "w", 0),
    ("w₃", "w", 0),
    # n in "n = 40–60"
    ("n = 40", "n", 0),
]


# ------------------------------------------------------------------
# 2. Promote section headings
#     Numbered "N." at top level -> HEADING_2
#     Numbered "N.M." at subsection level -> HEADING_3
#     "References" left as NORMAL_TEXT? The plan asks for same level per depth —
#     References is the same depth as "1. Introduction" etc., so promote to HEADING_2
#     for consistency.
# ------------------------------------------------------------------

HEADING_TEXTS = [
    # top-level section titles (Heading 2)
    ("1. Introduction", 2),
    ("2. Related Work and Theoretical Background", 2),
    ("3. Methodology", 2),
    ("4. Implemented Artifact and Design Discussion", 2),
    ("5. Conclusion", 2),
    ("References", 2),
    # subsection titles (Heading 3)
    ("2.1. Knowledge tracing", 3),
    ("2.2. Difficulty calibration and the Zone of Proximal Development", 3),
    ("2.3. Multi-Armed Bandits in education", 3),
    ("2.4. Spaced repetition and FSRS", 3),
    ("2.5. Programming platforms and the integration gap", 3),
    ("3.1. System overview and closed-loop architecture", 3),
    ("3.2. Knowledge graph foundation", 3),
    ("3.3. Layer 1 — Bayesian Knowledge Tracing", 3),
    ("3.4. Layer 2 — Dynamic Elo rating", 3),
    ("3.5. Layer 3 — Hierarchical MAB with Thompson Sampling", 3),
    ("3.6. Layer 4 — FSRS and the submission-to-rating mapping", 3),
    ("3.7. Layer 5 — Optional LLM feedback", 3),
    ("3.8. Pre-registered pilot evaluation protocol", 3),
    ("4.1. Implemented Artifact", 3),
    ("4.2. Discussion", 3),
]


# ------------------------------------------------------------------
# 3. Caption unification
#   (a) Text replacement: "Source: authors' own synthesis." -> "Source: authors' own work."
#   (b) Bold the "Figure N." / "Table N." prefix, clear italic from the rest of the caption.
#       Captions currently render as italic across the whole line (Figure/Table 1-3).
#       Target final style per plan: bold label, normal body, no italic.
# ------------------------------------------------------------------

CAPTION_PREFIXES = [
    "Figure 1.",
    "Figure 2.",
    "Figure 3.",
    "Table 1.",
]


def main():
    print("--- Step A: Unicode subscript replacement (θ_m -> θₘ, θ_p -> θₚ) ---")
    requests_a = [replace_text_request(f, r) for f, r in SUBSCRIPT_REPLACEMENTS]
    result_a = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests_a},
    ).execute()
    for i, reply in enumerate(result_a.get("replies", [])):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        print(f"  [{i}] {SUBSCRIPT_REPLACEMENTS[i][0]!r} -> {SUBSCRIPT_REPLACEMENTS[i][1]!r}: {occ} occurrences")

    print("\n--- Step B: 'authors\\' own synthesis' -> 'authors\\' own work' ---")
    result_b = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": [replace_text_request(
            "Source: authors' own synthesis.",
            "Source: authors' own work.",
        )]},
    ).execute()
    for reply in result_b.get("replies", []):
        print(f"  synthesis -> work: {reply.get('replaceAllText', {}).get('occurrencesChanged', 0)} occurrences")

    # Re-fetch to get exact indices for per-range styling
    print("\n--- Step C: Italicise math variables (per-occurrence byte-range updateTextStyle) ---")
    doc = fetch_doc()
    paragraphs = iter_text_with_index(doc)

    italic_requests = []
    italic_summary = []
    for needle, letter, off in ITALIC_LETTER_CONTEXTS:
        # locate every occurrence of `needle` in the body text and map to absolute range
        ranges = list(find_all_offsets(paragraphs, needle))
        for abs_start, _abs_end in ranges:
            letter_start = abs_start + off
            letter_end = letter_start + len(letter)
            italic_requests.append(italicize_request(letter_start, letter_end))
        italic_summary.append((needle, letter, len(ranges)))

    if italic_requests:
        result_c = service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": italic_requests},
        ).execute()
        print(f"  sent {len(italic_requests)} updateTextStyle requests; replies: {len(result_c.get('replies', []))}")
    for needle, letter, count in italic_summary:
        print(f"  italicised '{letter}' in {count} occurrences of {needle!r}")

    # Step D: Promote headings
    print("\n--- Step D: Promote numbered headings to HEADING_2 / HEADING_3 ---")
    doc = fetch_doc()
    paragraphs = iter_text_with_index(doc)

    heading_requests = []
    for h_text, level in HEADING_TEXTS:
        match = None
        for p in paragraphs:
            txt = p["text"].rstrip("\n")
            if txt.strip() == h_text:
                match = p
                break
        if match is None:
            print(f"  WARN: heading not found: {h_text!r}")
            continue
        heading_requests.append(
            set_heading_request(match["startIndex"], match["endIndex"], level)
        )
        # also ensure the text itself is NOT bold/italic (heading styles carry that)
        # but only for the text range, not the trailing newline
        text_start = match["startIndex"]
        text_end = match["endIndex"] - 1  # minus the trailing \n
        # reset bold/italic to inherit from paragraph style
        heading_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": text_start, "endIndex": text_end},
                "textStyle": {"bold": False, "italic": False},
                "fields": "bold,italic",
            }
        })
    if heading_requests:
        result_d = service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": heading_requests},
        ).execute()
        print(f"  sent {len(heading_requests)} heading-promotion requests")

    # Step E: Caption prefix bold + de-italicise rest
    print("\n--- Step E: Caption prefix bold + de-italicise caption body ---")
    doc = fetch_doc()
    paragraphs = iter_text_with_index(doc)

    caption_requests = []
    for p in paragraphs:
        txt = p["text"].rstrip("\n")
        matched_prefix = None
        for prefix in CAPTION_PREFIXES:
            if txt.startswith(prefix):
                matched_prefix = prefix
                break
        if not matched_prefix:
            continue
        # Clear italic across the whole caption paragraph (text portion only)
        text_start = p["startIndex"]
        text_end = p["endIndex"] - 1
        caption_requests.append({
            "updateTextStyle": {
                "range": {"startIndex": text_start, "endIndex": text_end},
                "textStyle": {"bold": False, "italic": False},
                "fields": "bold,italic",
            }
        })
        # Bold the "Figure N." / "Table N." prefix
        prefix_start = p["startIndex"]
        prefix_end = p["startIndex"] + len(matched_prefix)
        caption_requests.append(bold_request(prefix_start, prefix_end))
        print(f"  caption: prefix={matched_prefix!r}  range {prefix_start}..{prefix_end}  line={txt!r}")
    if caption_requests:
        result_e = service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": caption_requests},
        ).execute()
        print(f"  sent {len(caption_requests)} caption-styling requests")

    print("\nFormatting pass complete. Re-run gdoc-find-conf-anchors.py to inspect.")


if __name__ == "__main__":
    main()
