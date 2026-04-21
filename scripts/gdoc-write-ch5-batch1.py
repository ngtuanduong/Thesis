"""
gdoc-write-ch5-batch1: apply Batch 1 revision (T1, T2, T4, T5) to the thesis Google Doc.

This is a one-shot script. It is idempotent at the level of exact-string replaceAllText:
running twice will no-op on any replacement whose target string has already been removed.

Tasks:
  T1 - rename Ch.5 heading + update 1.8 chapter-5 description paragraph
  T2 - replace Ch.5 opening paragraph with two framing paragraphs
  T4 - Layer-5 disabled + confounded-comparison paragraph in §5.2.1 area
  T5 - retone five metric targets in §5.3
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


# =============================================================================
# Target strings
# =============================================================================

# -------- T1 --------
T1_OLD_HEADING = "CHAPTER 5: EVALUATION AND EXPERIMENTS"
# Final heading preserves ALL-CAPS style used for Chapter headings in this doc.
T1_NEW_HEADING = "CHAPTER 5: PILOT EVALUATION DESIGN AND PRELIMINARY PROTOCOL"

# The 1.8 short paragraph about Chapter 5 (near-match; plan referenced a
# different wording that is not present in this doc).
T1_OLD_18 = (
    "Chapter 5 turns to the evaluation methodology and experimental results, "
    "examining whether the implementation presented here delivers on the learning "
    "gains that the theoretical design anticipates."
)
T1_NEW_18 = (
    "Chapter 5: Pilot Evaluation Design and Preliminary Protocol describes the "
    "evaluation methodology and the pilot experimental design that will be used to "
    "assess the platform, including participant recruitment, ethical considerations, "
    "evaluation metrics (Normalized Learning Gain, recommendation accuracy, "
    "engagement, usability), and the statistical analysis plan. Because the "
    "intervention has not been executed at the time of writing, this chapter is "
    "framed as a protocol and preliminary plan rather than a report of completed "
    "results. A planned within-system ablation using feature-flag-based layer "
    "disabling is also described."
)

# -------- T2 --------
# The entire current opening paragraph of Chapter 5 (starts "Chapter 4 of this thesis...").
# We replace it with the two framing paragraphs verbatim, joined with a newline so they
# become two paragraphs in the Google Doc.
T2_OLD_OPENING = (
    "Chapter 4 of this thesis has already seen the five-layer architecture of the "
    "adaptive system implemented as working software, discussing the implementation "
    "of the different layers of the adaptive architecture, the knowledge graph, the "
    "frontend, and the deployment configuration of the system. Feature flags are "
    "integrated into the AI service, allowing the different layers of the adaptive "
    "architecture to be enabled or disabled, and this has been seen to be of "
    "critical importance in this chapter of the thesis. The current chapter, on the "
    "other hand, moves from the construction of the adaptive architecture to the "
    "evaluation of the research, discussing the research methodology, the research "
    "questions, and the evaluation metrics that will be used to evaluate whether "
    "the adaptive architecture does indeed deliver the improved learning that the "
    "underlying theory would suggest. Four research questions are the basis of the "
    "evaluation, as was introduced in Section 1.4 of the thesis, although these "
    "were reduced from five to four during the evaluation planning phase of the "
    "research. The four research questions are as follows: RQ1: Does the "
    "multilayer adaptive architecture accurately model the knowledge of the "
    "students and predict the performance of the students? RQ2: Does the "
    "Hierarchical MAB problem selection strategy improve the performance of the "
    "students as compared to the content-based filtering strategy? RQ3: Does the "
    "FSRS strategy improve the long-term retention of the students on the "
    "different programming concepts? RQ4: Do the students find the adaptive "
    "architecture useful and easy to use? The evaluation draws on a mixed-methods "
    "approach, bringing together quantitative system metrics with qualitative "
    "survey and interview data to address these questions from complementary "
    "angles."
)
T2_NEW_OPENING_P1 = (
    "At the time of writing, the adaptive learning platform has been designed, "
    "implemented, and deployed in a functional form, as documented in Chapters 3 "
    "and 4. However, the full classroom intervention described in this chapter "
    "has not yet been executed. This chapter therefore presents the pilot "
    "evaluation protocol that will be used to assess the platform, together with "
    "the associated instruments, metrics, and statistical analysis plan, rather "
    "than a report of completed experimental results. The chapter is written in "
    "the future or conditional tense where appropriate to reflect this status."
)
T2_NEW_OPENING_P2 = (
    "Four research questions guide the evaluation, as introduced in Section 1.4. "
    "RQ1 concerns the predictive validity of the learner model (BKT and Elo). "
    "RQ2 concerns whether the adaptive recommendation pipeline, taken as a whole, "
    "yields different learning outcomes than a content-based baseline. RQ3 "
    "concerns short-term retention under FSRS-scheduled reviews. RQ4 concerns "
    "students' perception of usability and usefulness. A mixed-methods approach "
    "is adopted, combining system logs, pre-test / post-test scores, and "
    "standardized questionnaires (SUS, TAM) with semi-structured interviews. "
    "Because the experimental condition enables Layers 1-4 of the adaptive "
    "pipeline simultaneously (Layer 5, the LLM hint feature, is disabled for the "
    "pilot to avoid confounding and to keep hint-quality questions out of scope), "
    "the pilot is not designed to isolate the causal contribution of any "
    "individual layer; this limitation is discussed explicitly in Section 5.5 "
    "(Threats to Validity)."
)
# Two paragraphs are represented by joining with "\n" (Docs treats newline as paragraph break).
T2_NEW_OPENING = T2_NEW_OPENING_P1 + "\n" + T2_NEW_OPENING_P2

# -------- T4 --------
# The current "Experimental group (E) ... Control group (C) ..." paragraph.
T4_OLD_GROUPS = (
    "- **Experimental group (E):** The complete adaptive platform, with all five "
    "layers enabled. This means that all five components are active: Bayesian "
    "Knowledge Tracing (Layer 1), Dynamic Elo difficulty calibration (Layer 2), "
    "Hierarchical MAB problem selection (Layer 3), FSRS spaced repetition "
    "scheduling (Layer 4), and LLM-based Socratic hints (Layer 5). - **Control "
    "group (C):** The same platform interface, but with all the adaptive layers "
    "disabled. The problem recommendations are instead provided by the legacy "
    "content-based filtering system, which relies on cosine similarity between "
    "sentence-transformer embeddings. The students in this group will be given "
    "the same set of problems, will use the same code execution environment, and "
    "will have access to the same basic statistics dashboard, but without any "
    "knowledge tracing, Elo-based difficulty matching, spaced repetition "
    "scheduling, or adaptive hints."
)
T4_NEW_GROUPS = (
    "The experimental group receives the full adaptive pipeline comprising "
    "Layers 1-4: Bayesian Knowledge Tracing, the Dynamic K-Value Elo rating "
    "system, Hierarchical Multi-Armed Bandit recommendation with Thompson "
    "Sampling, and FSRS-scheduled reviews. Layer 5 (LLM-generated Socratic "
    "hints) is deliberately disabled (ENABLE_LLM_HINTS=false) for this pilot, so "
    "that hint-quality, hallucination, and cost concerns are kept out of scope. "
    "The control group receives content-based filtering over sentence-transformer "
    "embeddings with no adaptive components."
)

# "This design holds constant..." sentence update + inserted paragraph.
T4_OLD_HOLDS = (
    "This design holds constant the effect of the five-layer adaptive engine "
    "while varying for other potential influences such as platform newness, "
    "problem content, or practicing with the online system itself. Both groups "
    "use the same interface; the only difference is the algorithm that operates "
    "behind the interface."
)
T4_INSERTED_PARA = (
    "Because the experimental condition enables Layers 1-4 simultaneously, the "
    "design does not permit attributing any observed outcome to a single layer in "
    "isolation. In particular, a positive effect on RQ2 cannot be cleanly "
    "separated from the effect of FSRS-scheduled reviews, and vice versa for "
    "RQ3. The pilot is therefore positioned as a first assessment of the "
    "integrated platform as a whole; finer-grained layer-level ablations are "
    "identified as future work. This limitation is revisited in Section 5.5."
)
T4_NEW_HOLDS = (
    "This design holds constant the effect of the four-layer adaptive engine "
    "(Layers 1-4) while varying for other potential influences such as platform "
    "newness, problem content, or practicing with the online system itself. Both "
    "groups use the same interface; the only difference is the algorithm that "
    "operates behind the interface."
    "\n"
    + T4_INSERTED_PARA
)

# Also clean up a related sentence in §5.2.3 Independent variable paragraph:
# "the experimental group E receives the full five-layer pipeline" → "Layers 1-4"
T4_OLD_INDVAR = "the experimental group E receives the full five-layer pipeline"
T4_NEW_INDVAR = "the experimental group E receives the full Layers 1-4 pipeline"

# -------- T5 --------
T5_PAIRS = [
    (
        "Target: 70--85% for the experimental group, compared to an expected "
        "40--60% for the control group.",
        "Planned acceptance threshold: 70--85% for the experimental group and "
        "40--60% for the control group; these are pre-registered targets rather "
        "than observed values.",
    ),
    (
        "The target range should be between 60--80%.",
        "The planned target range is 60--80%.",
    ),
    (
        "The target is $\\text{AUC} \\geq 0.65$, as supported by the moderate "
        "predictive power of BKT as documented in the literature [13].",
        "The pre-registered target is $\\text{AUC} \\geq 0.65$, in line with the "
        "moderate predictive power reported for BKT in the literature [13].",
    ),
    (
        "The target is $\\text{AUC} \\geq 0.65$, consistent with Pelanek's "
        "findings on Elo-based prediction in educational systems [38].",
        "The pre-registered target is $\\text{AUC} \\geq 0.65$, consistent with "
        "Pelanek's findings on Elo-based prediction in educational systems [38].",
    ),
    (
        "The goal for this research is to obtain a minimum average SUS of at "
        "least 70 for the experimental group.",
        "The pre-registered goal is a mean SUS of at least 70 for the "
        "experimental group; the observed value will be reported post hoc.",
    ),
]


# =============================================================================
# Helpers
# =============================================================================

def replace_all_requests(pairs):
    """Build replaceAllText requests for a list of (old, new) string pairs."""
    return [
        {
            "replaceAllText": {
                "containsText": {"text": old, "matchCase": True},
                "replaceText": new,
            }
        }
        for old, new in pairs
    ]


def run_batch(requests, label):
    if not requests:
        print(f"[{label}] no requests to send")
        return None
    resp = service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()
    replies = resp.get("replies", [])
    for req, rep in zip(requests, replies):
        kind = next(iter(req))
        if kind == "replaceAllText":
            n = rep.get("replaceAllText", {}).get("occurrencesChanged", 0)
            snippet = req["replaceAllText"]["containsText"]["text"][:60]
            print(f"  [{label}] replaceAllText occ={n}  old~='{snippet}...'")
        else:
            print(f"  [{label}] {kind}: {rep}")
    return resp


def verify_contains(substrings, label):
    """Re-read the whole doc and check which substrings are present."""
    doc = service.documents().get(documentId=DOC_ID).execute()
    full_text = []
    for elem in doc["body"]["content"]:
        if "paragraph" in elem:
            for el in elem["paragraph"].get("elements", []):
                if "textRun" in el:
                    full_text.append(el["textRun"]["content"])
    text = "".join(full_text)
    for s in substrings:
        present = s in text
        marker = "OK " if present else "MISS"
        print(f"  [{label} verify] {marker}  '{s[:70]}...'")


# =============================================================================
# Execute
# =============================================================================

print("=== T1: heading rename + §1.8 paragraph ===")
t1_reqs = replace_all_requests([
    (T1_OLD_HEADING, T1_NEW_HEADING),
    (T1_OLD_18, T1_NEW_18),
])
run_batch(t1_reqs, "T1")

print("\n=== T2: Ch.5 opening framing paragraphs ===")
# We can use replaceAllText here too: the old opener is a single-paragraph
# run, and the new content is two paragraphs joined by "\n". Google Docs
# interprets embedded newlines in replaceText as paragraph breaks while
# inheriting the paragraph style of the replaced paragraph.
t2_reqs = replace_all_requests([
    (T2_OLD_OPENING, T2_NEW_OPENING),
])
run_batch(t2_reqs, "T2")

print("\n=== T4: Layer 5 disabled + confounded-comparison paragraph ===")
t4_reqs = replace_all_requests([
    (T4_OLD_GROUPS, T4_NEW_GROUPS),
    (T4_OLD_HOLDS, T4_NEW_HOLDS),
    (T4_OLD_INDVAR, T4_NEW_INDVAR),
])
run_batch(t4_reqs, "T4")

print("\n=== T5: retone metric targets ===")
t5_reqs = replace_all_requests(T5_PAIRS)
run_batch(t5_reqs, "T5")

print("\n=== Verification ===")
verify_contains(
    [
        T1_NEW_HEADING,
        "Chapter 5: Pilot Evaluation Design and Preliminary Protocol describes",
        T2_NEW_OPENING_P1[:80],
        T2_NEW_OPENING_P2[:80],
        "Layer 5 (LLM-generated Socratic hints) is deliberately disabled",
        "four-layer adaptive engine (Layers 1-4)",
        "Because the experimental condition enables Layers 1-4 simultaneously",
        "Planned acceptance threshold: 70--85%",
        "The planned target range is 60--80%",
        "The pre-registered target is $\\text{AUC} \\geq 0.65$, in line with the",
        "The pre-registered target is $\\text{AUC} \\geq 0.65$, consistent with Pelanek",
        "The pre-registered goal is a mean SUS of at least 70",
    ],
    label="BATCH1",
)

print("\nDONE.")
