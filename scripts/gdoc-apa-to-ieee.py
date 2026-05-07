"""
gdoc-apa-to-ieee: convert APA in-text citations to IEEE numeric [N] and replace
the alphabetical APA References list with an IEEE list ordered by first citation.

Target doc: 1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs
Override with env GDOC_DOC_ID or --doc-id.

Pipeline (autonomous, no confirmation prompts):
  Step 1 -- 17 replaceAllText requests for in-text citations. Specific (combos,
           narrative-style) before general (parenthetical). After the batch,
           any replacement that returned 0 occurrencesChanged is retried once
           with the NFD form of 'Pelánek' for the two Pelánek rules; all zero
           counts are reported.
  Step 2 -- Fetch doc structure, locate the "References" HEADING_2 paragraph
           (fallback: paragraph whose text is exactly "References\n"). Delete
           from first char after the heading to body-end minus 1 (preserve
           terminal sentinel), then insertText the IEEE-ordered block.
           After insert, apply NORMAL_TEXT + deleteParagraphBullets across the
           inserted range to suppress any inherited list numbering.
  Step 3 -- Read doc back; verify [1] present in body before References,
           (2016) absent from body, and [14] B. Settles ends the References.

Usage:
    python scripts/gdoc-apa-to-ieee.py
    python scripts/gdoc-apa-to-ieee.py --doc-id 1b21...
    python scripts/gdoc-apa-to-ieee.py --dry-run   # prints plan, does not write
"""
import argparse
import importlib.util
import io
import json
import sys
import unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOC_ID = "1b21l8G9SXiXSYP_2k9Up3ic11OK08yus557vb8gsPhs"

# ---------------------------------------------------------------------------
# Step 1 rules: ordered -- specific before general. Matters because
# "Pelánek (2016)" must be replaced BEFORE any "(2016)"-only rule, and
# "(Chapelle & Li, 2011; Rollinson & Brunskill, 2015)" combo before
# "(Chapelle & Li, 2011)" alone.
# ---------------------------------------------------------------------------
RULES = [
    ("(Chapelle & Li, 2011; Rollinson & Brunskill, 2015)", "[4], [5]"),
    ("Luxton-Reilly et al. (2018)", "Luxton-Reilly et al. [1]"),
    ("Corbett and Anderson (1995)", "Corbett and Anderson [2]"),
    ("(Corbett & Anderson, 1995)", "[2]"),
    ("Pelánek (2016)", "Pelánek [3]"),
    ("(Pelánek, 2016)", "[3]"),
    ("(Chapelle & Li, 2011)", "[4]"),
    ("Ye et al. (2022)", "Ye et al. [6]"),
    ("(Ye et al., 2022)", "[6]"),
    ("Ma et al. (2014)", "Ma et al. [7]"),
    ("(Ma et al., 2014)", "[7]"),
    ("(Piech et al., 2015)", "[8]"),
    ("(Vygotsky, 1978)", "[9]"),
    ("(Bjork & Bjork, 2011)", "[10]"),
    ("Segal et al. (2018)", "Segal et al. [11]"),
    ("(Cepeda et al., 2006)", "[12]"),
    ("(Wang et al., 2023)", "[13]"),
]

# Step 2 IEEE references block, first-citation order.
IEEE_REFS = """[1] A. Luxton-Reilly, Simon, I. Albluwi, B. A. Becker, M. Giannakos, A. N. Kumar, L. Ott, J. Paterson, M. J. Scott, J. Sheard, and C. Szabo, "Introductory programming: A systematic literature review," in Proc. 2018 ITiCSE Conf. Working Group Reports, New York, NY, USA: ACM, 2018, pp. 55–106, doi: 10.1145/3293881.3295779.
[2] A. T. Corbett and J. R. Anderson, "Knowledge tracing: Modeling the acquisition of procedural knowledge," User Modeling and User-Adapted Interaction, vol. 4, no. 4, pp. 253–278, 1995, doi: 10.1007/BF01099821.
[3] R. Pelánek, "Applications of the Elo rating system in adaptive educational systems," Computers & Education, vol. 98, pp. 169–179, Jul. 2016, doi: 10.1016/j.compedu.2016.03.017.
[4] O. Chapelle and L. Li, "An empirical evaluation of Thompson sampling," in Advances in Neural Information Processing Systems, vol. 24, Red Hook, NY, USA: Curran Associates, 2011, pp. 2249–2257.
[5] J. Rollinson and E. Brunskill, "From predictive models to instructional policies," in Proc. 8th Int. Conf. Educational Data Mining (EDM), International Educational Data Mining Society, 2015, pp. 179–186.
[6] J. Ye, J. Su, and Y. Cao, "A stochastic shortest path algorithm for optimizing spaced repetition scheduling," in Proc. 28th ACM SIGKDD Conf. Knowledge Discovery and Data Mining, New York, NY, USA: ACM, 2022, pp. 4381–4390, doi: 10.1145/3534678.3539081.
[7] W. Ma, O. O. Adesope, J. C. Nesbit, and Q. Liu, "Intelligent tutoring systems and learning outcomes: A meta-analysis," Journal of Educational Psychology, vol. 106, no. 4, pp. 901–918, 2014, doi: 10.1037/a0037123.
[8] C. Piech, J. Bassen, J. Huang, S. Ganguli, M. Sahami, L. Guibas, and J. Sohl-Dickstein, "Deep knowledge tracing," in Advances in Neural Information Processing Systems, vol. 28, Red Hook, NY, USA: Curran Associates, 2015, pp. 505–513.
[9] L. S. Vygotsky, Mind in Society: The Development of Higher Psychological Processes. Cambridge, MA, USA: Harvard University Press, 1978.
[10] R. A. Bjork and E. L. Bjork, "Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning," in Psychology and the Real World: Essays Illustrating Fundamental Contributions to Society, M. A. Gernsbacher, R. W. Pew, L. M. Hough, and J. R. Pomerantz, Eds. New York, NY, USA: Worth Publishers, 2011, pp. 56–64.
[11] A. Segal, Y. Gal, E. Kamar, E. Horvitz, and G. Miller, "Optimizing interventions via offline policy evaluation: Studies in citizen science," in Proc. AAAI Conf. Artificial Intelligence, vol. 32, no. 1, Palo Alto, CA, USA: AAAI Press, 2018, pp. 3893–3900, doi: 10.1609/aaai.v32i1.11852.
[12] N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted, and D. Rohrer, "Distributed practice in verbal recall tasks: A review and quantitative synthesis," Psychological Bulletin, vol. 132, no. 3, pp. 354–380, 2006, doi: 10.1037/0033-2909.132.3.354.
[13] R. E. Wang, Q. Wirawarn, N. Goodman, and D. Demszky, "SocraticLM: Exploring Socratic questioning strategies in language models," in Findings of the Association for Computational Linguistics: EMNLP 2023, Stroudsburg, PA, USA: ACL, 2023, pp. 3070–3084.
[14] B. Settles and B. Meeder, "A trainable spaced repetition model for language learning," in Proc. 54th Annu. Meeting of the Association for Computational Linguistics, Stroudsburg, PA, USA: ACL, 2016, pp. 1848–1858, doi: 10.18653/v1/P16-1174."""


def load_auth():
    spec = importlib.util.spec_from_file_location(
        "gdoc_util_auth", str(SCRIPT_DIR / "gdoc-util-auth.py")
    )
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def iter_paragraphs(doc):
    """Yield (startIndex, endIndex, text, namedStyleType) per paragraph."""
    for elem in doc["body"]["content"]:
        para = elem.get("paragraph")
        if not para:
            continue
        text = "".join(
            el.get("textRun", {}).get("content", "")
            for el in para.get("elements", [])
        )
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style


def find_references_anchor(doc):
    """Return (startIndex, endIndex, text) of the References heading paragraph.
    Primary match: HEADING_2 style AND text startswith 'References'.
    Fallback: any paragraph whose text is exactly 'References\n'.
    """
    primary = None
    fallback = None
    for s, e, text, style in iter_paragraphs(doc):
        stripped = text.strip()
        if stripped == "References":
            if style.startswith("HEADING") and primary is None:
                primary = (s, e, text)
            if fallback is None:
                fallback = (s, e, text)
    return primary or fallback


def body_end_index(doc):
    content = doc["body"]["content"]
    return content[-1]["endIndex"] if content else 1


def step1_replacements(docs, doc_id, dry_run):
    """Run the 17 ordered replacements. Return list of (rule_idx, find, replace, occurrencesChanged)."""
    results = []
    for i, (find, replace) in enumerate(RULES, start=1):
        req = {
            "replaceAllText": {
                "containsText": {"text": find, "matchCase": True},
                "replaceText": replace,
            }
        }
        if dry_run:
            print(f"  [dry] rule {i:>2}: {find!r} -> {replace!r}")
            results.append((i, find, replace, None))
            continue
        resp = docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": [req]}
        ).execute()
        occ = resp["replies"][0].get("replaceAllText", {}).get("occurrencesChanged", 0)
        results.append((i, find, replace, occ))
        print(f"  rule {i:>2}: occurrencesChanged={occ}  {find!r} -> {replace!r}")

    # Retry Pelánek rules with NFD form if NFC returned 0.
    if not dry_run:
        for i, (find, replace) in enumerate(RULES, start=1):
            if "Pel" not in find:
                continue
            orig_occ = results[i - 1][3]
            if orig_occ and orig_occ > 0:
                continue
            nfd = unicodedata.normalize("NFD", find)
            if nfd == find:
                continue  # already NFD; nothing to try
            print(f"  rule {i} returned 0; retrying with NFD form {nfd!r}")
            resp = docs.documents().batchUpdate(
                documentId=doc_id,
                body={
                    "requests": [
                        {
                            "replaceAllText": {
                                "containsText": {"text": nfd, "matchCase": True},
                                "replaceText": replace,
                            }
                        }
                    ]
                },
            ).execute()
            retry_occ = (
                resp["replies"][0].get("replaceAllText", {}).get("occurrencesChanged", 0)
            )
            results[i - 1] = (i, nfd, replace, retry_occ)
            print(f"  rule {i:>2} (NFD retry): occurrencesChanged={retry_occ}")
    return results


def step2_replace_references(docs, doc_id, dry_run):
    """Delete content under 'References' heading and insert IEEE-ordered block."""
    doc = docs.documents().get(documentId=doc_id).execute()
    anchor = find_references_anchor(doc)
    if anchor is None:
        raise RuntimeError("Could not locate a 'References' heading or line in the doc.")
    ref_start, ref_end, ref_text = anchor
    body_end = body_end_index(doc)
    # Delete range: from first char AFTER the 'References\n' paragraph to body_end - 1.
    # The final char at body_end - 1 is the document sentinel newline that must not be deleted.
    delete_start = ref_end
    delete_end = body_end - 1
    print(f"  References anchor: [{ref_start}, {ref_end}) text={ref_text.strip()!r}")
    print(f"  Body endIndex: {body_end}")
    print(f"  Delete range: [{delete_start}, {delete_end})")

    if delete_end <= delete_start:
        print("  (nothing to delete under References; body already ends at heading)")
        delete_needed = False
    else:
        delete_needed = True

    # Insert text: starts with \n so the first line "[1] ..." lives in a new paragraph
    # rather than sticking onto the 'References' heading line -- the insert location is
    # at delete_start == ref_end, which is immediately AFTER the heading's \n, so a
    # leading \n would create an empty paragraph. We actually want NO leading newline
    # because ref_end sits at the index of the next paragraph's first character.
    # Example: if References paragraph is [27233, 27244) then ref_end=27244 is the
    # position of the first char of the paragraph AFTER references. Inserting at 27244
    # puts the insert at the start of a new paragraph. Good.
    insert_text = IEEE_REFS

    if dry_run:
        print(f"  [dry] would delete [{delete_start},{delete_end}) and insert {len(insert_text)} chars at {delete_start}")
        return delete_start, len(insert_text)

    requests = []
    if delete_needed:
        requests.append(
            {"deleteContentRange": {"range": {"startIndex": delete_start, "endIndex": delete_end}}}
        )
    requests.append(
        {"insertText": {"location": {"index": delete_start}, "text": insert_text}}
    )

    docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
    print(f"  Deleted and inserted IEEE block ({len(insert_text)} chars) at index {delete_start}.")

    # After the insert, apply NORMAL_TEXT paragraph style + deleteParagraphBullets over the
    # newly inserted range so we do not inherit list numbering or a non-body style from the
    # paragraph at the insertion point.
    inserted_range = {
        "startIndex": delete_start,
        "endIndex": delete_start + len(insert_text),
    }
    style_requests = [
        {
            "updateParagraphStyle": {
                "range": inserted_range,
                "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                "fields": "namedStyleType",
            }
        },
        {"deleteParagraphBullets": {"range": inserted_range}},
    ]
    docs.documents().batchUpdate(
        documentId=doc_id, body={"requests": style_requests}
    ).execute()
    print(f"  Applied NORMAL_TEXT + deleteParagraphBullets to inserted range {inserted_range}.")
    return delete_start, len(insert_text)


def step3_verify(docs, doc_id):
    doc = docs.documents().get(documentId=doc_id).execute()
    # Reconstruct body as paragraphs with text.
    paras = list(iter_paragraphs(doc))

    # Find References anchor index (in paragraphs list).
    ref_idx = None
    for idx, (s, e, text, style) in enumerate(paras):
        if text.strip() == "References":
            ref_idx = idx
            break

    body_text_pre_refs = "".join(p[2] for p in paras[:ref_idx]) if ref_idx is not None else ""
    body_text_post_refs = "".join(p[2] for p in paras[ref_idx + 1:]) if ref_idx is not None else ""

    # Count [1] occurrences in pre-refs body (so we exclude the reference entry [1] itself).
    count_bracket1_body = body_text_pre_refs.count("[1]")
    # Count generic (2016) in pre-refs body -- every APA year-paren pattern should be gone.
    count_2016_body = body_text_pre_refs.count("(2016)")

    # Find the last non-empty entry in the post-refs section and check for [14] B. Settles.
    post_entries = [ln for ln in body_text_post_refs.split("\n") if ln.strip()]
    last_entry = post_entries[-1] if post_entries else ""
    has_settles_14 = last_entry.startswith("[14] B. Settles")

    # Before/after snippet from Introduction (paragraph containing Luxton-Reilly).
    intro_snippet = ""
    for s, e, text, style in paras:
        if "Luxton-Reilly" in text:
            intro_snippet = text.strip()
            break

    return {
        "pre_refs_paragraphs": ref_idx,
        "count_[1]_in_body": count_bracket1_body,
        "count_(2016)_in_body": count_2016_body,
        "last_refs_entry": last_entry,
        "last_entry_is_settles_14": has_settles_14,
        "intro_luxton_snippet": intro_snippet,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--doc-id", default=DEFAULT_DOC_ID)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print(f"Target doc: {args.doc_id}")
    if args.dry_run:
        print("[DRY RUN] no write will be sent.")

    auth = load_auth()
    docs = auth.get_docs_service()

    print("\n--- Step 1: in-text APA -> IEEE numeric ---")
    step1 = step1_replacements(docs, args.doc_id, args.dry_run)
    zero_rules = [(i, f) for (i, f, _, occ) in step1 if occ == 0]
    if zero_rules:
        print(f"  WARN: {len(zero_rules)} rules returned 0 occurrences:")
        for i, f in zero_rules:
            print(f"    rule {i}: {f!r}")
    else:
        print("  All 17 rules changed >=1 occurrence.")

    print("\n--- Step 2: replace References section with IEEE-ordered list ---")
    step2_replace_references(docs, args.doc_id, args.dry_run)

    if args.dry_run:
        print("\n[DRY RUN] skipping verification.")
        return

    print("\n--- Step 3: verify ---")
    v = step3_verify(docs, args.doc_id)
    print(json.dumps(v, ensure_ascii=False, indent=2))

    # Summary block.
    print("\n=== SUMMARY ===")
    print(f"  Step 1 totals: {sum((occ or 0) for *_ , occ in step1)} occurrencesChanged across 17 rules")
    for i, find, replace, occ in step1:
        print(f"    rule {i:>2}: {occ}  {find} -> {replace}")
    print(f"  Step 3 checks:")
    print(f"    [1] in body (pre-refs): {v['count_[1]_in_body']} (expected >= 1)")
    print(f"    (2016) in body (pre-refs): {v['count_(2016)_in_body']} (expected 0)")
    print(f"    last refs entry startswith '[14] B. Settles': {v['last_entry_is_settles_14']}")
    print(f"\n  Intro snippet:\n    {v['intro_luxton_snippet'][:400]}")
    print(f"\nOpen https://docs.google.com/document/d/{args.doc_id}/edit to confirm.")


if __name__ == "__main__":
    main()
