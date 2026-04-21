"""
gdoc-write-ch1-batch5: Batch 5 corrective pass.
  PART A: delete redundancy paragraphs D2, D5 (D1, D3 flagged — would break references)
  PART B: retone marketing phrases M1, M3, M6, M7 (M2 folded into M1, M4 into M7, M5 NONE FOUND)
  PART C: F1 References heading, F2 stray R, F3 placeholder scan, F4 §1.8 confirmation

Executed as a single batchUpdate. Deletions are computed from paragraph indices
obtained via a fresh fetch; replacements use replaceAllText for anchor-based edits.
"""
import sys, io, importlib.util, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth", "c:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py"
)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

service = mod.get_docs_service()
doc = mod.get_document(service)
paras = list(mod.iter_paragraphs(doc))

# Locate paragraphs fresh (by anchor prefix) for deletions
def find_para(prefix):
    for s, e, t, style in paras:
        if t.startswith(prefix):
            return s, e, t
    return None

# D2 anchor
d2 = find_para("With regards to the Vietnamese university setting in particular")
# D5 anchor
d5 = find_para("In summary, the fundamental concern that this thesis seeks to resolve")

print(f"D2 found: s={d2[0]} e={d2[1]}" if d2 else "D2 NOT FOUND")
print(f"D5 found: s={d5[0]} e={d5[1]}" if d5 else "D5 NOT FOUND")

# Include following \n paragraph in each deletion to keep spacing clean
def extend_with_blank(s, e):
    for ps, pe, t, style in paras:
        if ps == e and t == "\n":
            return s, pe
    return s, e

d2r = extend_with_blank(*d2[:2]) if d2 else None
d5r = extend_with_blank(*d5[:2]) if d5 else None
print("D2 range:", d2r)
print("D5 range:", d5r)

# Build batchUpdate requests. Deletions MUST be in descending startIndex order.
requests = []

# ---- PART B text replacements (applied first; do not affect D2/D5 indices
# because PART B targets live either earlier or later but deleteContentRange is
# evaluated in the order given, so we send deletions FIRST (by descending index)
# and replacements AFTER — but replaceAllText is anchor-based and is robust to
# prior deletions. We'll send deletions first, replacements second.) ----

# Deletions (descending)
del_ranges = []
if d5r:
    del_ranges.append(("D5", d5r))
if d2r:
    del_ranges.append(("D2", d2r))
del_ranges.sort(key=lambda x: -x[1][0])
for tag, (s, e) in del_ranges:
    requests.append({"deleteContentRange": {"range": {"startIndex": s, "endIndex": e}}})
    print(f"Queued delete {tag}: {s}..{e}")

# ---- M1/M2 — para 278: "To the best of the author's knowledge, this thesis
#       represents the first application of FSRS to programming concept review
#       scheduling" → softened
# (note: curly apostrophe in doc)
requests.append({"replaceAllText": {
    "containsText": {"text": "To the best of the author\u2019s knowledge, this thesis represents the first application of FSRS to programming concept review scheduling.", "matchCase": True},
    "replaceText": "Within the scope of the literature surveyed in Chapter 2, this appears to be among the first applications of FSRS to programming concept review scheduling."
}})

# ---- M1 — para 171: "the novel submission-to-rating mapping for FSRS" → drop "novel"
requests.append({"replaceAllText": {
    "containsText": {"text": "the novel submission-to-rating mapping for FSRS", "matchCase": True},
    "replaceText": "the submission-to-rating mapping for FSRS"
}})

# ---- M1 — para 317: "requires a novel mapping from code submission" → drop "novel"
requests.append({"replaceAllText": {
    "containsText": {"text": "requires a novel mapping from code submission outcomes to FSRS review ratings", "matchCase": True},
    "replaceText": "requires a mapping from code submission outcomes to FSRS review ratings"
}})

# ---- M3 — para 278: "This mapping bridges the gap between FSRS\u2019s flashcard-oriented design"
requests.append({"replaceAllText": {
    "containsText": {"text": "This mapping bridges the gap between FSRS\u2019s flashcard-oriented design and the richer signal space of programming exercises.", "matchCase": True},
    "replaceText": "This mapping connects FSRS\u2019s flashcard-oriented design and the richer signal space of programming exercises."
}})

# ---- M3 — heading para 319: "2.4.3 How This Thesis Fills the Gap" → rename
requests.append({"replaceAllText": {
    "containsText": {"text": "2.4.3 How This Thesis Fills the Gap", "matchCase": True},
    "replaceText": "2.4.3 How This Thesis Addresses the Integration Question"
}})

# ---- M6 — para 146 Scope Evaluation bullet rewrite
old_146 = ("Evaluation: A controlled pilot experiment design involving 40-60 participants over a 4-week period, "
           "with a follow-up retention test at Week 8. A formal power analysis (as described in Chapter 5) confirms "
           "that this sample size is adequate for detecting large effects (Cohen\u2019s d >= 0.8) at alpha = 0.05 with "
           "80% power, and the experiment is conceptualized as a preliminary evaluation rather than large-scale validation.")
# NB: actual doc uses straight apostrophe in "Cohen's d >= 0.8"; double-check via earlier dump
old_146_v2 = ("Evaluation: A controlled pilot experiment design involving 40-60 participants over a 4-week period, "
              "with a follow-up retention test at Week 8. A formal power analysis (as described in Chapter 5) confirms "
              "that this sample size is adequate for detecting large effects (Cohen's d >= 0.8) at alpha = 0.05 with "
              "80% power, and the experiment is conceptualized as a preliminary evaluation rather than large-scale validation.")
new_146 = ("Evaluation: A pilot evaluation protocol is specified for a between-subjects study with 40-60 participants, "
           "a four-week intervention, and a two-week retention follow-up. A power analysis (Chapter 5) indicates that "
           "the nominal sample size can only detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power. "
           "Execution of the intervention and reporting of results are beyond the scope of this thesis; the study is "
           "presented as a preliminary design rather than a completed evaluation.")
requests.append({"replaceAllText": {
    "containsText": {"text": old_146_v2, "matchCase": True},
    "replaceText": new_146
}})

# ---- M7 — para 83 Table 1.1 row/footnote rewrite
old_83 = "This thesis proposes a unified adaptive platform that incorporates all the components of the adaptive system."
new_83 = ("This row describes the platform proposed in this thesis. At the time of writing it has been implemented "
          "but not yet evaluated in a classroom pilot. All other rows describe production systems.")
requests.append({"replaceAllText": {
    "containsText": {"text": old_83, "matchCase": True},
    "replaceText": new_83
}})

# ---- F1 — References heading. Replace malformed "eference:\x0b" with "References\n"
# (the \x0b converts to a real paragraph break, separating the heading from the
# bibliography entries — which was the original formatting intent).
requests.append({"replaceAllText": {
    "containsText": {"text": "eference:\x0b", "matchCase": True},
    "replaceText": "References\n"
}})

# ---- F2 — stray R before **Contingency for smaller samples**
requests.append({"replaceAllText": {
    "containsText": {"text": "R**Contingency for smaller samples.**", "matchCase": True},
    "replaceText": "**Contingency for smaller samples.**"
}})

print(f"\nTotal requests: {len(requests)}")
for i, r in enumerate(requests):
    key = list(r.keys())[0]
    if key == "deleteContentRange":
        print(f"  {i}. deleteContentRange {r[key]['range']}")
    else:
        t = r[key]['containsText']['text'][:70].replace('\n','\\n').replace('\x0b','\\v')
        print(f"  {i}. replaceAllText  {t!r}")

# Execute
result = service.documents().batchUpdate(
    documentId=mod.DOC_ID,
    body={"requests": requests},
).execute()

# Report per-request result
replies = result.get("replies", [])
for i, (req, rep) in enumerate(zip(requests, replies)):
    key = list(req.keys())[0]
    if key == "replaceAllText":
        n = rep.get("replaceAllText", {}).get("occurrencesChanged", 0)
        t = req[key]['containsText']['text'][:60].replace('\n','\\n').replace('\x0b','\\v')
        print(f"  [{i}] replaceAllText: {n} occurrence(s) — {t!r}")
    else:
        print(f"  [{i}] {key}: done")

print("\nBatch 5 main edits applied.")
