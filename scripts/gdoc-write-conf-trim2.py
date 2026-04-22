"""
gdoc-write-conf-trim2: Second-pass trim of §2 Related Work to hit the
450-480 word target specified in the plan (Priority 5). The first trim pass
(scripts/gdoc-write-conf-content.py) cut ~100 words but the measured total
still sits at ~572 body words. This pass applies additional cuts to §2.1,
§2.2, §2.4, §2.5 using the exact current sentences as find-text selectors.

Usage:
    GDOC_KEY_FILE=... GDOC_DOC_ID=... python3 scripts/gdoc-write-conf-trim2.py
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


REPLACEMENTS = [
    # §2.1 — tighten the "Relevance" line; drop redundant "cold-start populations of a
    # few hundred learners" framing and "raw point accuracy" tail.
    (
        "Relevance to this work: BKT is chosen as Layer 1 because the platform must operate with cold-start populations of a few hundred learners, and because the mastery estimate is consumed downstream by a bandit that benefits from calibrated uncertainty rather than raw point accuracy.",
        "Relevance to this work: BKT is chosen as Layer 1 because it is data-efficient on cold-start cohorts of a few hundred learners and exposes a calibrated mastery estimate to the bandit downstream.",
        "it is data-efficient on cold-start cohorts",
    ),

    # §2.2 — drop the "both of which argue that optimal learning occurs when task
    # difficulty modestly exceeds current ability" tail; the principle names are
    # enough for a conference audience.
    (
        "Pelánek (2016) formalized Elo-style rating for adaptive educational systems, showing that dual student–item ratings converge within roughly twenty attempts per learner and stabilize faster than Item Response Theory alternatives in small cohorts, and operationalizes the Zone of Proximal Development (Vygotsky, 1978) and the desirable-difficulties principle (Bjork & Bjork, 2011), both of which argue that optimal learning occurs when task difficulty modestly exceeds current ability.",
        "Pelánek (2016) formalized Elo-style rating for adaptive educational systems, showing that dual student–item ratings converge within roughly twenty attempts per learner, and operationalizes the Zone of Proximal Development (Vygotsky, 1978) and the desirable-difficulties principle (Bjork & Bjork, 2011).",
        "operationalizes the Zone of Proximal Development (Vygotsky, 1978) and the desirable-difficulties principle (Bjork & Bjork, 2011).",
    ),

    # §2.3 — shorten the Relevance sentence; "both levels constrained by the
    # knowledge graph and the ZPD filter" is slightly redundant with §3.5.
    (
        "Relevance to this work: Layer 3 uses a two-level hierarchical Thompson-sampling bandit in which the outer level selects the next concept to practise and the inner level selects a specific problem within that concept, with both levels constrained by the knowledge graph and the ZPD filter.",
        "Relevance to this work: Layer 3 adopts a two-level hierarchical Thompson-sampling bandit in which the outer level selects the next concept and the inner level selects a problem within it; Section 3.5 describes the prerequisite and ZPD constraints that shape this choice.",
        "adopts a two-level hierarchical Thompson-sampling bandit in which the outer level selects the next concept",
    ),

    # §2.4 — two cuts:
    #  (a) collapse the "while programming is a procedural skill…" clause
    #  (b) drop "— an application that the surveyed literature has not previously
    #      reported" (duplicated later at §3.6's softened "among the first reported").
    (
        "The existing FSRS literature evaluates on vocabulary and factual-recall tasks, while programming is a procedural skill whose decay dynamics are less well understood. Layer 4 of the proposed platform applies FSRS to programming skill retention — an application that the surveyed literature has not previously reported; Section 3.6 describes the submission-to-rating mapping this application requires.",
        "FSRS has been evaluated mainly on vocabulary and factual-recall tasks, whereas programming is a procedural skill whose decay dynamics are less well understood. Layer 4 applies FSRS to programming skill retention, and Section 3.6 describes the submission-to-rating mapping this application requires.",
        "Layer 4 applies FSRS to programming skill retention, and Section 3.6 describes the submission-to-rating mapping",
    ),

    # §2.5 — cut the "Relevance to this work:" closing line; the last sentence
    # already signals intent + forward reference to Table 1 and the remainder.
    (
        "Research prototypes have examined individual adaptive components in programming education, but the literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph. Relevance to this work: this gap is the paper's core motivation; Table 1 summarizes the four techniques and their complementary roles, and the remainder of the paper describes the integrated architecture that fills the gap.",
        "Research prototypes have examined individual adaptive components in programming education, but the literature surveyed in this paper does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph. This gap is the paper's core motivation, and Table 1 summarizes the four techniques' complementary roles.",
        "This gap is the paper's core motivation, and Table 1 summarizes the four techniques' complementary roles.",
    ),
]


def main():
    requests = [{
        "replaceAllText": {
            "containsText": {"text": f, "matchCase": True},
            "replaceText": r,
        }
    } for f, r, _c in REPLACEMENTS]
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={"requests": requests},
    ).execute()
    zero = []
    for i, reply in enumerate(result.get("replies", [])):
        occ = reply.get("replaceAllText", {}).get("occurrencesChanged", 0)
        print(f"[{i}] occurrencesChanged={occ} find={REPLACEMENTS[i][0][:70]!r}...")
        if occ == 0:
            zero.append(i)
    if zero:
        print(f"WARNING: {len(zero)} requests missed. Indices: {zero}")

    # canary verification
    doc = mod.get_document(service=service, doc_id=DOC_ID)
    joined = "\n".join(text for _s, _e, text, _st in mod.iter_paragraphs(doc))
    missing = [c for _f, _r, c in REPLACEMENTS if c not in joined]
    if missing:
        print(f"FAIL: missing canaries: {missing}")
    else:
        print(f"OK: all {len(REPLACEMENTS)} canaries present.")


if __name__ == "__main__":
    main()
