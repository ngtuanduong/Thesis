"""
gdoc-write-ch1-batch3: apply Batch 3 — rewrite Sections 1.3, 1.4, 1.7 of the
thesis doc.

Execution order: bottom-to-top (T7 -> T8 -> T9), each as a separate
batchUpdate so we re-fetch anchors between steps. This keeps index math
simple because edits below do not shift indices above.

For each section we:
  1. deleteContentRange(body_start, next_heading_start) — this also deletes
     the trailing newline of the last body paragraph, which in Docs merges
     the now-empty paragraph slot into the next heading paragraph's slot.
     After delete, the section heading remains intact and an immediately
     empty paragraph position opens at body_start.
     (Actually: paragraphs are delimited by '\n'. Deleting [body_start,
     next_heading_start) removes all body paragraphs incl. their trailing
     newlines. The section heading paragraph at heading_start is untouched
     and ends at body_start-1 with its own '\n'. The next heading paragraph
     (1.4/1.5/1.8) originally starts at next_heading_start; after delete it
     starts at body_start.)
  2. insertText(body_start, new_body_text) where new_body_text ends with '\n'
     so the next heading starts cleanly.
  3. updateParagraphStyle(NORMAL_TEXT) on the newly inserted range.
  4. updateTextStyle(bold=False, italic=False) defensively to clear any
     inherited styling from the surrounding text.
  5. updateTextStyle(bold=True) on each bold lead-in label.
"""
import importlib.util, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

spec = importlib.util.spec_from_file_location(
    "gdoc_util_auth",
    "C:/Users/duong/WebstormProjects/Thesis/scripts/gdoc-util-auth.py",
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

service = m.get_docs_service()
DOC_ID = m.DOC_ID


def fetch_paras():
    doc = service.documents().get(documentId=DOC_ID).execute()
    return doc, list(m.iter_paragraphs(doc))


def find_heading(paras, needle):
    """Return (startIndex, endIndex) of first paragraph whose trimmed text == needle and style is HEADING_*."""
    for s, e, t, st in paras:
        if st.startswith("HEADING") and t.strip() == needle:
            return s, e
    return None, None


def apply_section_rewrite(section_label, heading_text, next_heading_text, paras_block, intro_text=None):
    """
    paras_block: list of (bold_label_or_None, body_text) tuples, in order.
                 If bold_label_or_None is None, the paragraph has no bold lead-in.
                 Otherwise body_text begins with that label followed by the rest.
    intro_text: optional plain intro paragraph placed before paras_block.

    Bullet paragraphs are encoded by passing body_text with a leading '\t'
    followed by the bullet text; we then attach a createParagraphBullets
    request for that paragraph range.

    Here we use a simpler convention: each entry in paras_block is a dict
    with keys: 'label' (str or None), 'text' (str, full paragraph text
    including the label if any), 'bullet' (bool).
    """
    print(f"\n=== {section_label}: rewriting body ===")
    doc, paras = fetch_paras()

    # Find heading and next heading
    hdr_s, hdr_e = find_heading(paras, heading_text)
    nxt_s, _ = find_heading(paras, next_heading_text)
    if hdr_s is None:
        print(f"  FAIL: heading '{heading_text}' not found")
        return False, None
    if nxt_s is None:
        print(f"  FAIL: next heading '{next_heading_text}' not found")
        return False, None

    body_start = hdr_e  # heading paragraph end = body start
    body_end = nxt_s    # next heading start
    print(f"  heading at [{hdr_s},{hdr_e}); body range [{body_start},{body_end}); next heading at {nxt_s}")

    # Build new text.
    parts = []
    if intro_text:
        parts.append({"text": intro_text, "bullet": False, "label": None})
    for blk in paras_block:
        parts.append(blk)

    # Concatenate with '\n' separators; append final '\n' so next heading stays separate.
    full_text = ""
    # Record per-paragraph offset ranges for styling.
    offsets = []
    for p in parts:
        start_off = len(full_text)
        full_text += p["text"]
        end_off = len(full_text)
        offsets.append((start_off, end_off, p))
        full_text += "\n"
    # full_text now ends with '\n'. That's what we want.

    new_len = len(full_text)
    print(f"  new body length = {new_len} chars, {len(parts)} paragraphs")

    requests = []
    # 1) delete old body
    requests.append({
        "deleteContentRange": {
            "range": {"startIndex": body_start, "endIndex": body_end}
        }
    })
    # 2) insert new body
    requests.append({
        "insertText": {
            "location": {"index": body_start},
            "text": full_text,
        }
    })
    # 3) NORMAL_TEXT paragraph style on inserted range
    requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": body_start, "endIndex": body_start + new_len},
            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
            "fields": "namedStyleType",
        }
    })
    # 4) clear bold/italic defensively
    requests.append({
        "updateTextStyle": {
            "range": {"startIndex": body_start, "endIndex": body_start + new_len},
            "textStyle": {"bold": False, "italic": False},
            "fields": "bold,italic",
        }
    })
    # 5) bold the labels
    for (so, eo, p) in offsets:
        if p.get("label"):
            lbl = p["label"]
            lbl_s = body_start + so
            lbl_e = body_start + so + len(lbl)
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": lbl_s, "endIndex": lbl_e},
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            })
    # 6) bullets: apply createParagraphBullets per contiguous bullet run
    # Find runs of consecutive bullet paragraphs and make one range per run.
    i = 0
    while i < len(offsets):
        if offsets[i][2].get("bullet"):
            j = i
            while j + 1 < len(offsets) and offsets[j + 1][2].get("bullet"):
                j += 1
            run_s = body_start + offsets[i][0]
            run_e = body_start + offsets[j][1] + 1  # include trailing \n
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": run_s, "endIndex": run_e},
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                }
            })
            i = j + 1
        else:
            i += 1

    resp = service.documents().batchUpdate(
        documentId=DOC_ID, body={"requests": requests}
    ).execute()
    print(f"  applied {len(requests)} requests, got {len(resp.get('replies', []))} replies")
    return True, new_len


# =============================================================================
# T7 content — Section 1.7
# =============================================================================

T7_BLOCKS = [
    {
        "label": None,
        "text": "This thesis makes two main contributions, together with one optional extension.",
        "bullet": False,
    },
    {
        "label": "Contribution 1: An integrated adaptive learning platform for programming courses (Chapters 3-4).",
        "text": (
            "Contribution 1: An integrated adaptive learning platform for programming courses (Chapters 3-4). "
            "The thesis proposes and implements a closed-loop adaptive platform that combines Bayesian Knowledge "
            "Tracing, a Dynamic K-Value Elo rating system, a prerequisite-constrained Hierarchical Multi-Armed "
            "Bandit with Thompson Sampling, and the Free Spaced Repetition Scheduler, unified through a curated "
            "knowledge graph of approximately 30 programming concepts. The integration is the central engineering "
            "contribution: each layer exposes well-defined inputs and outputs to the others, so that BKT mastery "
            "gates MAB exploration, Elo ratings constrain problem selection to the Zone of Proximal Development, "
            "and FSRS review urgency can interrupt the MAB when due reviews exist. The system is released as a "
            "working, deployable full-stack application (React, NestJS, FastAPI, PostgreSQL, Docker sandbox), "
            "designed for the Vietnamese university context."
        ),
        "bullet": False,
    },
    {
        "label": "Contribution 2: A pilot evaluation protocol for the integrated platform (Chapter 5).",
        "text": (
            "Contribution 2: A pilot evaluation protocol for the integrated platform (Chapter 5). The thesis "
            "specifies a between-subjects, pre-test / post-test pilot study design for evaluating the platform "
            "with undergraduate students at Hanoi University, including the recruitment and consent procedure, "
            "the instruments (custom pre-/post-test, SUS, TAM, semi-structured interviews), the full set of "
            "quantitative metrics (Normalized Learning Gain, BKT and Elo prediction AUC, acceptance and "
            "completion rates, engagement indicators), and a statistical analysis plan with pre-registered "
            "thresholds, power assumptions, and an explicit fallback for smaller samples. Because the "
            "experimental condition enables Layers 1-4 simultaneously (with Layer 5 disabled for the pilot), "
            "the protocol is scoped as a whole-system pilot rather than a layer-level ablation."
        ),
        "bullet": False,
    },
    {
        "label": "Optional extension: LLM-based Socratic hints (Layer 5).",
        "text": (
            "Optional extension: LLM-based Socratic hints (Layer 5). A Retrieval-Augmented Generation module "
            "that issues Socratic hints grounded in the student's current knowledge state is implemented as "
            "Layer 5 but is disabled in the pilot evaluation. Because it raises additional questions of cost, "
            "hallucination, and hint quality that are out of scope for this pilot, it is positioned as an "
            "optional extension to the platform and as a direction for future work rather than as a primary "
            "contribution."
        ),
        "bullet": False,
    },
]


# =============================================================================
# T8 content — Section 1.4
# =============================================================================

T8_INTRO = (
    "This thesis addresses four research questions. For the comparative questions (RQ2, RQ3) corresponding "
    "hypotheses are stated and are tested at the alpha = 0.05 significance level. Because the experimental "
    "condition in the pilot enables Layers 1-4 simultaneously (see Chapter 5), RQ2 and RQ3 should be read as "
    "questions about the integrated platform as a whole rather than about any single layer in isolation."
)

T8_BLOCKS = [
    {
        "label": "RQ1: How accurately does the learner model embedded in the platform predict student performance?",
        "text": (
            "RQ1: How accurately does the learner model embedded in the platform predict student performance? "
            "This question evaluates the foundational capability of the learner model. It is assessed by the "
            "AUC-ROC of BKT and Elo predictions on held-out submissions, the recommendation acceptance rate "
            "per difficulty band, and the convergence speed of Elo ratings. Following established thresholds "
            "in educational data mining [11], an AUC-ROC of at least 0.65-0.70 is taken as the pre-registered "
            "target for acceptable predictive performance."
        ),
        "bullet": False,
    },
    {
        "label": "RQ2: Does the integrated adaptive pipeline (BKT + Elo + Hierarchical MAB + FSRS) lead to different learning outcomes than a content-based filtering baseline?",
        "text": (
            "RQ2: Does the integrated adaptive pipeline (BKT + Elo + Hierarchical MAB + FSRS) lead to different "
            "learning outcomes than a content-based filtering baseline? This question compares the experimental "
            "group, which receives the full Layers 1-4 pipeline, against the control group, which receives only "
            "content-based filtering over sentence-transformer embeddings. The primary metric is Normalized "
            "Learning Gain; the Problems-to-Mastery ratio is a supporting indicator of efficiency. Because "
            "several adaptive components are active at the same time in the experimental condition, RQ2 does "
            "not attempt to isolate the individual contribution of the Hierarchical MAB."
        ),
        "bullet": False,
    },
    {
        "label": None,
        "text": (
            "H2 (alternative): Students in the adaptive group will show higher Normalized Learning Gain than "
            "students in the content-based filtering group."
        ),
        "bullet": True,
    },
    {
        "label": None,
        "text": "H2_0 (null): There is no difference in Normalized Learning Gain between the two groups.",
        "bullet": True,
    },
    {
        "label": "RQ3: Does the platform with FSRS-scheduled reviews yield different short-term retention outcomes than the same platform without scheduled reviews?",
        "text": (
            "RQ3: Does the platform with FSRS-scheduled reviews yield different short-term retention outcomes "
            "than the same platform without scheduled reviews? This question is assessed through a retention "
            "test administered two weeks after the end of the intervention. As with RQ2, the experimental "
            "condition bundles FSRS with the rest of the adaptive pipeline, so an observed difference cannot "
            "be attributed to FSRS alone."
        ),
        "bullet": False,
    },
    {
        "label": None,
        "text": (
            "H3 (alternative): Students in the adaptive group will show higher retention scores on the two-week "
            "follow-up test than students in the control group."
        ),
        "bullet": True,
    },
    {
        "label": None,
        "text": "H3_0 (null): There is no difference in retention scores between the two groups.",
        "bullet": True,
    },
    {
        "label": "RQ4: How do students perceive the usability and usefulness of the adaptive platform?",
        "text": (
            "RQ4: How do students perceive the usability and usefulness of the adaptive platform? This question "
            "captures the student experience through the System Usability Scale (SUS) [13], the Technology "
            "Acceptance Model constructs of Perceived Usefulness and Perceived Ease of Use [14], and "
            "semi-structured interviews analysed by thematic analysis [15]."
        ),
        "bullet": False,
    },
]


# =============================================================================
# T9 content — Section 1.3
# =============================================================================

T9_INTRO = (
    "The aim of this thesis is to design and implement an integrated adaptive learning platform for "
    "undergraduate programming courses, and to specify a pilot evaluation protocol for it. The specific "
    "objectives are as follows."
)

T9_BLOCKS = [
    {
        "label": "Objective 1: Design a multi-layer adaptive learning architecture.",
        "text": (
            "Objective 1: Design a multi-layer adaptive learning architecture. Propose a modular architecture "
            "in which each layer addresses a distinct aspect of adaptive instruction - knowledge tracing "
            "(Layer 1), difficulty calibration (Layer 2), problem selection (Layer 3), and review scheduling "
            "(Layer 4) - together with an optional LLM hint layer (Layer 5). The architecture defines explicit "
            "data flows between layers so that each can operate independently while contributing to a coherent "
            "pipeline."
        ),
        "bullet": False,
    },
    {
        "label": "Objective 2: Implement the learner model (BKT + Dynamic Elo).",
        "text": (
            "Objective 2: Implement the learner model (BKT + Dynamic Elo). Implement Bayesian Knowledge Tracing "
            "for per-(student, concept) mastery estimation and a dual Elo rating system with a dynamic K-factor "
            "for continuous difficulty calibration, taking submission outcomes as the primary observation "
            "signal. Use the Elo / Item Response Theory link [11] to ground difficulty matching in psychometric "
            "theory."
        ),
        "bullet": False,
    },
    {
        "label": "Objective 3: Implement the recommendation and review pipeline (H-MAB + FSRS).",
        "text": (
            "Objective 3: Implement the recommendation and review pipeline (H-MAB + FSRS). Implement a "
            "two-level Hierarchical Multi-Armed Bandit with Thompson Sampling that selects a concept and then "
            "a specific problem, subject to knowledge-graph prerequisite gating and Elo-based Zone of Proximal "
            "Development filtering. Integrate the Free Spaced Repetition Scheduler [12] so that due reviews "
            "interact with the MAB's next recommendation. Define a rating mapping from code submission outcomes "
            "to FSRS review ratings."
        ),
        "bullet": False,
    },
    {
        "label": "Objective 4: Deliver a deployable full-stack platform.",
        "text": (
            "Objective 4: Deliver a deployable full-stack platform. Integrate the adaptive engine with a React "
            "frontend, a NestJS API, a FastAPI adaptive service, a PostgreSQL database, and a Docker-based code "
            "execution sandbox into a working web application usable by undergraduate students."
        ),
        "bullet": False,
    },
    {
        "label": "Objective 5: Specify and pre-register a pilot evaluation protocol.",
        "text": (
            "Objective 5: Specify and pre-register a pilot evaluation protocol. Design a between-subjects, "
            "pre-test / post-test pilot study with a control group to assess learning effectiveness, "
            "recommendation quality, engagement, and usability, including instruments, metrics, statistical "
            "plan, and ethical procedures. Execution of the intervention and reporting of results are "
            "explicitly scoped as future work beyond this thesis."
        ),
        "bullet": False,
    },
]


# =============================================================================
# Apply bottom-to-top: T7 first (highest index), then T8, then T9.
# =============================================================================

status = {}

# T7
ok, _ = apply_section_rewrite(
    "T7 Section 1.7 Contributions",
    heading_text="1.7 Contributions",
    next_heading_text="1.8 Thesis Structure",
    paras_block=T7_BLOCKS,
    intro_text=None,  # T7_BLOCKS[0] is the non-bold opener already
)
status["T7"] = "APPLIED" if ok else "FAILED"

# T8
ok, _ = apply_section_rewrite(
    "T8 Section 1.4 Research Questions",
    heading_text="1.4 Research Questions",
    next_heading_text="1.5 Proposed Solution",
    paras_block=T8_BLOCKS,
    intro_text=T8_INTRO,
)
status["T8"] = "APPLIED" if ok else "FAILED"

# T9
ok, _ = apply_section_rewrite(
    "T9 Section 1.3 Research Objectives",
    heading_text="1.3 Research Objectives",
    next_heading_text="1.4 Research Questions",
    paras_block=T9_BLOCKS,
    intro_text=T9_INTRO,
)
status["T9"] = "APPLIED" if ok else "FAILED"


# =============================================================================
# Verification
# =============================================================================
print("\n=== Verification ===")
doc = service.documents().get(documentId=DOC_ID).execute()
full_text = []
for elem in doc["body"]["content"]:
    if "paragraph" in elem:
        for el in elem["paragraph"].get("elements", []):
            if "textRun" in el:
                full_text.append(el["textRun"]["content"])
full = "".join(full_text)

checks = [
    ("T9 intro", "The aim of this thesis is to design and implement an integrated adaptive learning platform"),
    ("T9 Obj 1 label", "Objective 1: Design a multi-layer adaptive learning architecture."),
    ("T9 Obj 5 label", "Objective 5: Specify and pre-register a pilot evaluation protocol."),
    ("T9 OLD gone", "The main objective of this thesis is to design, implement, and evaluate an adaptive learning system"),
    ("T8 intro", "This thesis addresses four research questions."),
    ("T8 RQ1", "How accurately does the learner model embedded in the platform predict student performance?"),
    ("T8 RQ2", "Does the integrated adaptive pipeline (BKT + Elo + Hierarchical MAB + FSRS)"),
    ("T8 H2", "H2 (alternative): Students in the adaptive group will show higher Normalized Learning Gain"),
    ("T8 H3_0", "H3_0 (null): There is no difference in retention scores"),
    ("T8 RQ4", "How do students perceive the usability and usefulness of the adaptive platform?"),
    ("T8 OLD gone", "RQ1 (Primary): How accurately can the multi-layer adaptive system model the knowledge"),
    ("T7 opener", "This thesis makes two main contributions, together with one optional extension."),
    ("T7 C1", "Contribution 1: An integrated adaptive learning platform for programming courses (Chapters 3-4)."),
    ("T7 C2", "Contribution 2: A pilot evaluation protocol for the integrated platform (Chapter 5)."),
    ("T7 ext", "Optional extension: LLM-based Socratic hints (Layer 5)."),
    ("T7 OLD gone", "Contribution 3: FSRS for Programming Skill Retention"),
    ("T7 OLD gone 2", "Contribution 4: Open-source adaptive learning platform"),
]
for label, needle in checks:
    present = needle in full
    if "OLD gone" in label:
        ok = not present
        tag = "OK " if ok else "FAIL (old text still present)"
    else:
        ok = present
        tag = "OK " if ok else "MISS"
    print(f"  [{label:22}] {tag}")

print("\n=== STATUS ===")
for k, v in status.items():
    print(f"  {k}: {v}")

if all(v == "APPLIED" for v in status.values()):
    print("\nBatch 3 DONE")
else:
    print("\nBatch 3 PARTIAL")
