# Thesis Revision Plan — Advisor Feedback of 14 Apr 2026

**Target document:** https://docs.google.com/document/d/1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA/edit
**Source files:** `documents/thesis-chapters/{abstract, chapter1-introduction, chapter2-literature-review, chapter3-system-design, chapter4-implementation, chapter5-evaluation}.md` and the consolidated `Adaptive-Learning-Platform-for-University-Programming-Courses.txt`.
**Guiding principle:** Chapter 5 contains **no real experimental data** as of 2026-04-14. All forward-looking claims must be reframed as *plan / pilot design* rather than completed results. The thesis's core positioning changes from "four contributions" to "two main contributions (platform + pilot evaluation design) with LLM as optional extension."

**User decisions (2026-04-14):**
1. No pilot data will be reported. Chapter 5 is fully reframed as design + protocol only; do NOT invent preliminary results or seed-data figures.
2. Layer 5 (LLM hints) is excluded from the experimental condition. In §5.2.1 the experimental group runs with `ENABLE_LLM_HINTS=false`. Layer 5 is described only as an optional extension in the architecture.
3. Concept count is standardised globally as **"approximately 30 programming concepts"**. Any occurrence of "28 concepts" / "30 topics" / similar variants is replaced with "approximately 30 programming concepts".
4. **T10 (Declaration / Acknowledgements) is SKIPPED.** The user will write these two sections manually. Do NOT edit lines currently containing "Declaration of Originality (Pending)" / "Acknowledgements (Pending)" — leave them exactly as-is for the user.

Tasks below are ordered by the advisor's stated priority: (i) Chapter 5, (ii) Abstract + Introduction, (iii) RQs / Objectives / Contributions, (iv) Language cleanup, (v) Redundancy trimming, (vi) Threats to Validity, (vii) Formatting fixes.

---

## T1 — Rename Chapter 5 to reflect pilot / plan status

- **Location:** Chapter 5 heading (currently "Chapter 5: Evaluation and Experiments"). Also update the Table of Contents entry and the Chapter 6 / Ch. 1.8 cross-reference to this chapter name.
- **Type:** RENAME_SECTION
- **BEFORE:** `Chapter 5: Evaluation and Experiments`
- **AFTER:** `Chapter 5: Pilot Evaluation Design and Preliminary Protocol`
- **Also update Section 1.8 sentence:**
  - BEFORE: `**Chapter 5: Experimentation and Evaluation** describes the experimental design ... and results. An ablation study ... provides evidence for each layer's marginal contribution.`
  - AFTER: `**Chapter 5: Pilot Evaluation Design and Preliminary Protocol** describes the evaluation methodology and the pilot experimental design that will be used to assess the platform, including participant recruitment, ethical considerations, evaluation metrics (Normalized Learning Gain, recommendation accuracy, engagement, usability), and the statistical analysis plan. Because the intervention has not been executed at the time of writing, this chapter is framed as a protocol and preliminary plan rather than a report of completed results. A planned within-system ablation using feature-flag-based layer disabling is also described.`
- **Rationale:** Feedback points 1, 4, 10.
- **Dependencies:** None.

---

## T2 — Add framing paragraph at the top of Chapter 5 clarifying "no results yet"

- **Location:** Insert directly after the new chapter title (T1) and before Section 5.1.
- **Type:** INSERT
- **BEFORE:** (current opening paragraph of Chapter 5, beginning "Chapter 4 of this thesis has already seen ...")
- **AFTER (replace the current opening paragraph entirely):**
  > At the time of writing, the adaptive learning platform has been designed, implemented, and deployed in a functional form, as documented in Chapters 3 and 4. However, the full classroom intervention described in this chapter has not yet been executed. This chapter therefore presents the *pilot evaluation protocol* that will be used to assess the platform, together with the associated instruments, metrics, and statistical analysis plan, rather than a report of completed experimental results. The chapter is written in the future or conditional tense where appropriate to reflect this status.
  >
  > Four research questions guide the evaluation, as introduced in Section 1.4. RQ1 concerns the predictive validity of the learner model (BKT and Elo). RQ2 concerns whether the adaptive recommendation pipeline, taken as a whole, yields different learning outcomes than a content-based baseline. RQ3 concerns long-term retention under FSRS-scheduled reviews. RQ4 concerns students' perception of usability and usefulness. A mixed-methods approach is adopted, combining system logs, pre-test / post-test scores, and standardized questionnaires (SUS, TAM) with semi-structured interviews. Because the experimental condition enables the full five-layer pipeline simultaneously, the pilot is not designed to isolate the causal contribution of any individual layer; this limitation is discussed explicitly in Section 5.5 (Threats to Validity).
- **Rationale:** Feedback points 1, 3, 4, 9, 10.
- **Dependencies:** T1.

---

## T3 — Add a new "5.5 Threats to Validity" subsection

- **Location:** Insert as a new subsection at the end of Chapter 5, after the "Group Comparison Analysis Plan" block at the current end of Section 5.3, and before any Chapter 6 begins.
- **Type:** INSERT
- **BEFORE:** (no existing text — new subsection)
- **AFTER (full text to paste):**
  > ### 5.5 Threats to Validity
  >
  > Several characteristics of the proposed pilot limit the strength of the conclusions that can be drawn from it. They are stated explicitly so that readers can calibrate the weight given to any future results.
  >
  > **Small and single-site sample.** Recruitment is confined to a single cohort at Hanoi University, with a target of 40--60 participants and a fallback plan for as few as 20--30. With approximately 20--30 students per condition in the nominal case, the study is only powered to detect large effect sizes (Cohen's $d \geq 0.8$). Generalization to other institutions, curricula, or student populations is therefore not supported by the data that this pilot can produce.
  >
  > **Short intervention window.** The four-week intervention, together with a two-week gap before the retention test, is short relative to the full forgetting curves that the FSRS algorithm is designed to exploit. Results on RQ3 should therefore be read as suggestive of short-term retention differences rather than as a validation of long-term spaced repetition benefits in programming.
  >
  > **Confounded treatment condition.** The experimental group receives the full five-layer adaptive pipeline simultaneously (BKT, Dynamic Elo, Hierarchical MAB, FSRS, and optional LLM hints), while the control group receives none of these components. Any observed difference between the two groups therefore cannot be attributed to any single layer --- for example, a positive effect on RQ2 cannot be cleanly separated from the effect of FSRS review scheduling or of the LLM hint feature, and vice versa. Within-system analyses based on feature-flag replay may offer partial triangulation, but they rely on the same set of interaction logs and cannot replicate a true ablation experiment.
  >
  > **Metric-model coupling.** Several of the reported metrics, notably BKT prediction AUC and Elo convergence speed, are computed using the same model that also drives the platform's recommendations. A favourable value on these metrics demonstrates internal consistency of the model but does not, on its own, constitute independent evidence of learning effectiveness.
  >
  > **Self-selection, novelty, and attention effects.** Participation is voluntary, and the experimental interface is more feature-rich than the control interface. Observed differences may partly reflect novelty, increased perceived attention, or self-selection of more motivated students into the study rather than the adaptive mechanisms themselves.
  >
  > **Assessment instrument.** The pre-test and post-test are parallel-form instruments constructed for this study and have not been independently validated. Their reliability and concurrent validity will be reported post hoc, but this remains a limitation of the pilot.
  >
  > Taken together, these threats mean that any findings reported from this pilot should be interpreted as *preliminary evidence* about the feasibility and perceived value of the integrated platform, not as a definitive comparative evaluation of the individual adaptive techniques.
- **Rationale:** Feedback point 9 (and reinforces 1, 3, 4).
- **Dependencies:** T1, T2.

---

## T4 — Add explicit disclaimer within Section 5.1 ("confounded comparison")

- **Location:** Section 5.1, inside the "Experimental Design Overview" block, immediately after the paragraph beginning "This design holds constant the effect of the five-layer adaptive engine..."
- **Type:** INSERT
- **BEFORE:** `This design holds constant the effect of the five-layer adaptive engine while varying for other potential influences such as platform newness, problem content, or practicing with the online system itself. Both groups use the same interface; the only difference is the algorithm that operates behind the interface.`
- **AFTER (insert new paragraph directly after the above):**
  > Because the experimental condition enables all adaptive layers simultaneously, the design does not permit attributing any observed outcome to a single layer in isolation. In particular, a positive effect on RQ2 (H-MAB vs. content-based filtering) cannot be cleanly separated from the effect of FSRS-scheduled reviews or of the optional LLM hint feature, as all three are active for the experimental group and inactive for the control group. The pilot is therefore positioned as a first assessment of the integrated platform as a whole; finer-grained layer-level ablations are identified as future work. This limitation is revisited in Section 5.5.
- **Rationale:** Feedback points 3, 9.
- **Dependencies:** T3 (for the forward reference to Section 5.5).

---

## T5 — Remove results-tense language from Section 5.3 metric targets

- **Location:** Section 5.3 throughout (Acceptance Rate, Completion Rate, BKT AUC, Elo AUC, SUS, TAM bullets).
- **Type:** RETONE (selective find-and-replace)
- **Find / Replace pairs inside Section 5.3:**
  1. `Target: 70--85% for the experimental group, compared to an expected 40--60% for the control group.` -> `Planned acceptance threshold: 70--85% for the experimental group and 40--60% for the control group; these are pre-registered targets rather than observed values.`
  2. `The target range should be between 60--80%.` -> `The planned target range is 60--80%.`
  3. `The target is $\text{AUC} \geq 0.65$, as supported by the moderate predictive power of BKT as documented in the literature [13].` -> `The pre-registered target is $\text{AUC} \geq 0.65$, in line with the moderate predictive power reported for BKT in the literature [13].`
  4. `The target is $\text{AUC} \geq 0.65$, consistent with Pelanek's findings on Elo-based prediction in educational systems [38].` -> `The pre-registered target is $\text{AUC} \geq 0.65$, consistent with Pelanek's findings on Elo-based prediction in educational systems [38].`
  5. `The goal for this research is to obtain a minimum average SUS of at least 70 for the experimental group.` -> `The pre-registered goal is a mean SUS of at least 70 for the experimental group; the observed value will be reported post hoc.`
- **Rationale:** Feedback points 1, 4.
- **Dependencies:** T1, T2.

---

## T6 — Rewrite the Abstract

- **Location:** `abstract.md` (Section: English Abstract). Replace the entire abstract body (paragraphs between the "# Abstract / ## English Abstract" header and the `**Keywords:**` line). Remove the trailing italic "*Note: This abstract will be finalized...*" paragraph entirely.
- **Type:** REPLACE
- **BEFORE (quote of opening line for anchor):** `Programming education at universities worldwide faces a persistent challenge: high failure rates averaging 30--40% in introductory courses, driven by the fundamental mismatch between the individualized, practice-intensive nature of programming skill acquisition and the uniform, resource-constrained reality of large-class instruction.`
- **AFTER (full new abstract ~250 words):**
  > Programming education in large university courses faces a long-standing tension between the individualized, practice-intensive nature of programming skill acquisition and the uniform, resource-constrained reality of classroom instruction, with introductory failure rates reported at around 30--40% worldwide. Existing online coding platforms such as LeetCode, HackerRank, and Codeforces offer extensive problem repositories but use static difficulty tiers and do not adapt a learning path to the individual student. Prior academic work on adaptive learning for programming has typically addressed one component --- knowledge tracing, difficulty calibration, problem recommendation, or spaced repetition --- in isolation.
  >
  > This thesis proposes and implements an Adaptive Learning Platform for University Programming Courses that combines several of these components into a single closed-loop system. The platform is built around a manually curated knowledge graph of approximately 30 Python programming concepts and five adaptive layers: Bayesian Knowledge Tracing for per-concept mastery estimation, a Dynamic K-Value Elo rating system for difficulty calibration, a Hierarchical Multi-Armed Bandit with Thompson Sampling for problem selection, the Free Spaced Repetition Scheduler (FSRS) for review scheduling, and an optional Retrieval-Augmented LLM hint module. The system is delivered as a working full-stack application (React, NestJS, FastAPI, PostgreSQL, Docker-based code sandbox).
  >
  > The platform is accompanied by a pilot evaluation protocol describing a between-subjects, pre-test / post-test study with 40--60 undergraduate students at Hanoi University over a four-week intervention and a two-week retention follow-up, using Normalized Learning Gain, model prediction accuracy, engagement metrics, SUS, and TAM. At the time of writing, the intervention has not been executed and no experimental outcomes are reported. The thesis's primary contributions are therefore (i) the integrated platform and (ii) the pilot evaluation design. Layer 5 (LLM hints) is presented as an optional extension.
- **Rationale:** Feedback points 1, 2, 4, 7, 10.
- **Dependencies:** T1 (so the abstract matches the new Chapter 5 framing).

---

## T7 — Collapse contributions to 2 main + LLM as optional

- **Location:** Chapter 1, Section 1.7 "Contributions". Replace the block from the heading "### Research Contributions" through the end of Section 1.7 (before "## 1.8 Thesis Structure").
- **Type:** REPLACE
- **BEFORE (quote of opening anchor):** `This thesis makes the following contributions to the fields of educational technology and computer science education:`
- **AFTER (full replacement for Section 1.7 body):**
  > This thesis makes two main contributions, together with one optional extension.
  >
  > **Contribution 1: An integrated adaptive learning platform for programming courses (Chapters 3--4).**
  > The thesis proposes and implements a closed-loop adaptive platform that combines Bayesian Knowledge Tracing, a Dynamic K-Value Elo rating system, a prerequisite-constrained Hierarchical Multi-Armed Bandit with Thompson Sampling, and the Free Spaced Repetition Scheduler, unified through a curated knowledge graph of programming concepts. The integration is the central engineering contribution: each layer exposes well-defined inputs and outputs to the others, so that BKT mastery gates MAB exploration, Elo ratings constrain problem selection to the Zone of Proximal Development, and FSRS review urgency can interrupt the MAB when due reviews exist. The system is released as a working, deployable full-stack application (React, NestJS, FastAPI, PostgreSQL, Docker sandbox), designed for the Vietnamese university context.
  >
  > **Contribution 2: A pilot evaluation protocol for the integrated platform (Chapter 5).**
  > The thesis specifies a between-subjects, pre-test / post-test pilot study design for evaluating the platform with undergraduate students at Hanoi University, including the recruitment and consent procedure, the instruments (custom pre-/post-test, SUS, TAM, semi-structured interviews), the full set of quantitative metrics (Normalized Learning Gain, BKT and Elo prediction AUC, acceptance and completion rates, engagement indicators), and a statistical analysis plan with pre-registered thresholds, power assumptions, and an explicit fallback for smaller samples. Because the experimental condition enables all adaptive layers simultaneously, the protocol is deliberately scoped as a whole-system pilot rather than a layer-level ablation.
  >
  > **Optional extension: LLM-based Socratic hints (Layer 5).**
  > A Retrieval-Augmented Generation module that issues Socratic hints grounded in the student's current knowledge state is implemented as Layer 5. Because it raises additional questions of cost, hallucination, and hint quality that are out of scope for this pilot, it is positioned as an optional extension to the platform and as a direction for future work rather than as a primary contribution.
- **Rationale:** Feedback points 2, 3, 4, 7.
- **Dependencies:** T1 (Chapter 5 framing), T6 (Abstract framing).

---

## T8 — Down-tone / restructure the Research Questions (Section 1.4)

- **Location:** Chapter 1, Section 1.4 "Research Questions". Replace the full block from the heading through the RQ4 paragraph.
- **Type:** REPLACE
- **BEFORE (anchor):** `This thesis addresses four research questions, one primary and three secondary.`
- **AFTER (full replacement):**
  > This thesis addresses four research questions. For the comparative questions (RQ2, RQ3) corresponding hypotheses are stated and are tested at the $\alpha = 0.05$ significance level. Because the experimental condition in the pilot enables all adaptive layers simultaneously (see Chapter 5), RQ2 and RQ3 should be read as questions about the *integrated platform as a whole* rather than about any single layer in isolation.
  >
  > **RQ1: How accurately does the learner model embedded in the platform predict student performance?**
  > This question evaluates the foundational capability of the learner model. It is assessed by the AUC-ROC of BKT and Elo predictions on held-out submissions, the recommendation acceptance rate per difficulty band, and the convergence speed of Elo ratings. Following established thresholds in educational data mining [11], an AUC-ROC of at least 0.65--0.70 is taken as the pre-registered target for acceptable predictive performance.
  >
  > **RQ2: Does the integrated adaptive pipeline (BKT + Elo + Hierarchical MAB + FSRS) lead to different learning outcomes than a content-based filtering baseline?**
  > This question compares the experimental group, which receives the full five-layer pipeline, against the control group, which receives only content-based filtering over sentence-transformer embeddings. The primary metric is Normalized Learning Gain; the Problems-to-Mastery ratio is a supporting indicator of efficiency. Because several adaptive components are active at the same time in the experimental condition, RQ2 does not attempt to isolate the individual contribution of the Hierarchical MAB.
  > - *H2 (alternative):* Students in the adaptive group will show higher Normalized Learning Gain than students in the content-based filtering group.
  > - *H2$_0$ (null):* There is no difference in Normalized Learning Gain between the two groups.
  >
  > **RQ3: Does the platform with FSRS-scheduled reviews yield different short-term retention outcomes than the same platform without scheduled reviews?**
  > This question is assessed through a retention test administered two weeks after the end of the intervention. As with RQ2, the experimental condition bundles FSRS with the rest of the adaptive pipeline, so an observed difference cannot be attributed to FSRS alone.
  > - *H3 (alternative):* Students in the adaptive group will show higher retention scores on the two-week follow-up test than students in the control group.
  > - *H3$_0$ (null):* There is no difference in retention scores between the two groups.
  >
  > **RQ4: How do students perceive the usability and usefulness of the adaptive platform?**
  > This question captures the student experience through the System Usability Scale (SUS) [13], the Technology Acceptance Model constructs of Perceived Usefulness and Perceived Ease of Use [14], and semi-structured interviews analysed by thematic analysis [15].
- **Rationale:** Feedback points 3, 4, 10.
- **Dependencies:** T1, T2, T4.

---

## T9 — Down-tone / restructure Research Objectives (Section 1.3)

- **Location:** Chapter 1, Section 1.3 "Research Objectives". Replace Objectives 1--6.
- **Type:** REPLACE
- **BEFORE (anchor):** `The primary aim of this thesis is to design, implement, and evaluate an adaptive learning platform for university programming courses that integrates multiple complementary adaptive techniques into a unified, closed-loop system.`
- **AFTER (full replacement):**
  > The aim of this thesis is to design and implement an integrated adaptive learning platform for undergraduate programming courses, and to specify a pilot evaluation protocol for it. The specific objectives are as follows.
  >
  > **Objective 1: Design a multi-layer adaptive learning architecture.**
  > Propose a modular architecture in which each layer addresses a distinct aspect of adaptive instruction --- knowledge tracing (Layer 1), difficulty calibration (Layer 2), problem selection (Layer 3), and review scheduling (Layer 4) --- together with an optional LLM hint layer (Layer 5). The architecture defines explicit data flows between layers so that each can operate independently while contributing to a coherent pipeline.
  >
  > **Objective 2: Implement the learner model (BKT + Dynamic Elo).**
  > Implement Bayesian Knowledge Tracing for per-(student, concept) mastery estimation and a dual Elo rating system with a dynamic K-factor for continuous difficulty calibration, taking submission outcomes as the primary observation signal. Use the Elo / Item Response Theory link [11] to ground difficulty matching in psychometric theory.
  >
  > **Objective 3: Implement the recommendation and review pipeline (H-MAB + FSRS).**
  > Implement a two-level Hierarchical Multi-Armed Bandit with Thompson Sampling that selects a concept and then a specific problem, subject to knowledge-graph prerequisite gating and Elo-based Zone of Proximal Development filtering. Integrate the Free Spaced Repetition Scheduler [12] so that due reviews interact with the MAB's next recommendation. Define a rating mapping from code submission outcomes to FSRS review ratings.
  >
  > **Objective 4: Deliver a deployable full-stack platform.**
  > Integrate the adaptive engine with a React frontend, a NestJS API, a FastAPI adaptive service, a PostgreSQL database, and a Docker-based code execution sandbox into a working web application usable by undergraduate students.
  >
  > **Objective 5: Specify and pre-register a pilot evaluation protocol.**
  > Design a between-subjects, pre-test / post-test pilot study with a control group to assess learning effectiveness, recommendation quality, engagement, and usability, including instruments, metrics, statistical plan, and ethical procedures. Execution of the intervention and reporting of results are explicitly scoped as future work beyond this thesis.
- **Rationale:** Feedback points 2, 3, 4, 7, 10.
- **Dependencies:** T7, T8.

---

## T10 — Replace "Pending" boilerplate blocks

- **Location:** Front matter of the consolidated PDF / Google Doc, lines currently reading:
  - `Declaration of Originality (Pending)`
  - `Acknowledgements (Pending)`
- **Type:** REPLACE
- **BEFORE:**
  > Declaration of Originality (Pending)
  >
  > Acknowledgements (Pending)
- **AFTER (use plain neutral boilerplate):**
  > **Declaration of Originality**
  >
  > I, Nguyen Tuan Duong, declare that this thesis titled "Adaptive Learning Platform for University Programming Courses" and the work presented in it are my own. Where material from other sources has been used, it has been clearly attributed and referenced. No portion of this work has been submitted for any other degree or qualification at this or any other institution.
  >
  > Hanoi, 2026
  > Nguyen Tuan Duong
  >
  > **Acknowledgements**
  >
  > I would like to thank my advisor, Bui Quoc Khanh, for his guidance and patient feedback throughout the development of this thesis. I am also grateful to the Faculty of Information Technology at Hanoi University for providing the academic environment in which this work was carried out, and to the classmates and friends who contributed comments, testing time, and moral support during the project.
- **Rationale:** Feedback point 8.
- **Dependencies:** None.

---

## T11 — Global find-and-replace for "marketing academic" language

- **Location:** Whole thesis (all chapters + abstract + consolidated .txt).
- **Type:** REPLACE (global, case-sensitive unless noted).
- **Pairs (apply in order; only replace when the phrase appears in prose, not in section headings or bibliographic titles):**

  | # | Before | After |
  |---|--------|-------|
  | 1 | `first integrated multi-layer adaptive architecture combining BKT, Elo, MAB, and FSRS for programming education` | `integrated multi-layer adaptive architecture that combines BKT, Elo, MAB, and FSRS for programming education` |
  | 2 | `the first integrated` | `an integrated` |
  | 3 | `fully unified` | `integrated` |
  | 4 | `a novel contribution` | `a contribution of this thesis` |
  | 5 | `novel contribution` | `contribution of this thesis` |
  | 6 | `addresses the gap` | `addresses this integration question` |
  | 7 | `addresses this integration gap` | `addresses this integration question` |
  | 8 | `To the best of our knowledge, this thesis is the first to apply the FSRS algorithm to programming concept review scheduling.` | `Within the scope of the programming education literature surveyed in Chapter 2, this thesis appears to be among the first to apply the FSRS algorithm to programming concept review scheduling.` |
  | 9 | `To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis.` | `Within the scope of the literature surveyed in Chapter 2, this appears to be among the first applications of the FSRS algorithm [12] to programming skill retention, and is described here as a secondary contribution of the thesis.` |
  | 10 | `produces emergent adaptive behavior that no single technique achieves alone` | `exhibits adaptive behaviour that combines signals from multiple techniques` |
  | 11 | `will demonstrate significantly higher` | `will show higher` |
  | 12 | `comprehensive whole-system demonstration of the adaptive system` | `whole-system description of the adaptive platform` |

- **Rationale:** Feedback points 4, 7.
- **Dependencies:** T6--T9 (run global replace after the larger rewrites so the new text is included).

---

## T12 — Cut redundant paragraphs in Chapter 1 (Introduction)

Each entry below is a DELETE (remove the paragraph in full) or MERGE (delete the paragraph, rely on the remaining text). The goal is approximately 15--20% reduction of repetitive "programming is hard / classes are large / platforms are static" content.

- **D1 — DELETE** paragraph in Section 1.1 beginning:
  > "This heterogeneity creates a fundamental tension in traditional lecture-based instruction."
  **Reason:** The following paragraph ("The problem is compounded by the resource constraints...") already covers the same large-class / one-size-fits-all point.

- **D2 — DELETE** paragraph in Section 1.1 beginning:
  > "Within the Vietnamese university context specifically, these challenges are no less pressing."
  **Reason:** The Vietnamese context is re-stated in Section 1.6.1 (Scope) and in Chapter 2. One mention is sufficient.

- **D3 — DELETE** Section 1.2.1 paragraph beginning:
  > "Research spanning several decades has validated this premise."
  **Reason:** Covered in much more depth in Chapter 2; the introductory paragraph that follows ("These success stories motivate...") already carries the argument.

- **D4 — DELETE** Section 1.2.3 paragraph beginning:
  > "Academic research, similarly, has tended to study these adaptive components in isolation."
  **Reason:** Repeats the "components in isolation" claim already made in the abstract and in the paragraph immediately preceding Table 1.1.

- **D5 — DELETE** closing "In summary" paragraph of Section 1.1 beginning:
  > "In summary, the core problem this thesis addresses is the mismatch..."
  **Reason:** Straight restatement of the section. Section 1.2 opens the same argument; the summary is redundant.

- **Rationale:** Feedback points 5, 6.
- **Dependencies:** None.

---

## T13 — Cut redundant paragraphs in Chapter 2 (Literature Review)

- **D6 — DELETE** any paragraph in Chapter 2 that re-opens the "programming courses have high failure rates around 30--40%" framing more than once. Specifically, trim the recurrence in Section 2.1.x (the introductory subsection on CS education challenges) to a single paragraph.
- **D7 — DELETE** repetitive sentences in Chapter 2 subsections that re-argue "existing platforms (LeetCode, HackerRank, Codeforces) use static difficulty." This claim should appear once in Section 2.3 (Related Work / Related Technologies) and nowhere else in the chapter; excise the duplicates in Section 2.1 and Section 2.4.
- **D8 — DELETE** the "In summary" / "In conclusion" wrap-up paragraphs at the end of each subsection in 2.1 where the following subsection already repeats the same synthesis. Keep only the final "Research Gap" synthesis paragraph in Section 2.4.
- **Rationale:** Feedback points 5, 6.
- **Dependencies:** None.
- **Note for executing agent:** Because these deletions depend on the current line numbering in the Google Doc, the agent should use quoted anchor phrases (e.g. "failure rates in introductory programming courses average between 30% and 40%") and delete the *duplicate* occurrence, keeping the first. If the agent is uncertain which instance is redundant, mark for manual review rather than delete.

---

## T14 — Fix Table 1.1 footnote to remove "first integrated" bolding

- **Location:** Chapter 1, Table 1.1 "This Thesis" row and the asterisked footnote immediately below it.
- **Type:** RETONE
- **BEFORE:** `\* *This row represents a proposed system, not yet deployed and validated at scale. All other rows represent production systems.*`
- **AFTER:** `\* *This row describes the platform proposed in this thesis. At the time of writing it has been implemented but not yet evaluated in a classroom pilot. All other rows describe production systems.*`
- **Rationale:** Feedback points 1, 4.
- **Dependencies:** T11.

---

## T15 — Retone Chapter 3 sentence claiming "first application of FSRS"

- **Location:** `chapter3-system-design.md` Section 3.3.x Layer 4 purpose paragraph (and the mirrored paragraph in the consolidated .txt).
- **Type:** RETONE (covered by T11 rule #9 but called out explicitly for the agent to verify both occurrences).
- **BEFORE:** `To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis.`
- **AFTER:** `Within the scope of the literature surveyed in Chapter 2, this appears to be among the first applications of the FSRS algorithm [12] to programming skill retention, and is described here as a secondary contribution of the thesis.`
- **Rationale:** Feedback points 4, 7.
- **Dependencies:** T11.

---

## T16 — Retone Chapter 1 Table 1.1 intro sentence about "research gap this thesis targets"

- **Location:** Chapter 1, Section 1.2.3, sentence ending `the research gap this thesis targets lies precisely at their intersection`.
- **Type:** RETONE
- **BEFORE:** `the research gap this thesis targets lies precisely at their intersection --- bringing the adaptive sophistication of the latter category into the programming education domain.`
- **AFTER:** `the question this thesis investigates sits at their intersection: how to bring the adaptive mechanisms of the latter category into the programming education domain of the former.`
- **Rationale:** Feedback point 4 ("addresses the gap" softening).
- **Dependencies:** T11.

---

## T17 — Replace "results-tense" phrasing in Section 1.6.1 (Scope) bullet on evaluation

- **Location:** Chapter 1, Section 1.6.1 "Scope", the bullet beginning `- **Evaluation:** A controlled pilot experiment...`.
- **Type:** RETONE
- **BEFORE:** `- **Evaluation:** A controlled pilot experiment with 40--60 participants over a 4-week intervention period, with a follow-up retention test at Week 8. A formal power analysis (detailed in Chapter 5) indicates that this sample size is sufficient to detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power; the study is therefore framed as a preliminary assessment rather than a definitive large-scale validation.`
- **AFTER:** `- **Evaluation:** A pilot evaluation protocol is specified for a between-subjects study with 40--60 participants, a four-week intervention, and a two-week retention follow-up. A power analysis (Chapter 5) indicates that the nominal sample size can only detect large effect sizes (Cohen's $d \geq 0.8$) at $\alpha = 0.05$ with 80% power. Execution of the intervention and reporting of results are beyond the scope of this thesis; the study is presented as a preliminary design rather than a completed evaluation.`
- **Rationale:** Feedback points 1, 4, 10.
- **Dependencies:** T1.

---

## T18 — Renumber / caption / tense audit pass

- **Location:** Whole document, applied after T1--T17.
- **Type:** RETONE (editorial pass, no new content)
- **Instructions to executing agent:**
  1. Regenerate the Table of Contents so that the renamed Chapter 5 (T1) is reflected.
  2. Verify that every Figure and Table referenced in the text (by number) exists in the document with a caption, and vice versa. Flag orphans.
  3. Convert Chapter 5 verbs describing the experiment from present/past tense ("students are randomly assigned", "participants completed") to a consistent future/conditional tense ("participants will be randomly assigned", "participants will complete"). Leave instrument descriptions (e.g., "the SUS is a 10-item questionnaire") in present tense, since those describe the instrument itself, not the study's execution.
  4. Check that all references [1]--[58] are present in the final bibliography.
  5. Remove any remaining occurrences of the literal string `Pending`, `[TO BE COMPLETED]`, `[VERIFY: ...]`, or `[CITE: ...]`; for `[CITE: ...]` placeholders where no citation has been supplied, convert to a footnote asking for manual resolution before submission.
- **Rationale:** Feedback point 8.
- **Dependencies:** All prior tasks.

---

## Summary of redundant paragraphs flagged for deletion (quick reference)

- Ch.1 §1.1: "This heterogeneity creates a fundamental tension..."
- Ch.1 §1.1: "Within the Vietnamese university context specifically..."
- Ch.1 §1.1: "In summary, the core problem this thesis addresses..."
- Ch.1 §1.2.1: "Research spanning several decades has validated this premise."
- Ch.1 §1.2.3: "Academic research, similarly, has tended to study these adaptive components in isolation."
- Ch.2 §2.1: duplicate recurrences of the "30--40% failure rate" opening.
- Ch.2 §2.1 and §2.4: duplicate statements of "LeetCode/HackerRank/Codeforces are static."
- Ch.2 §2.1.x end-of-subsection "In summary" paragraphs (keep only the final synthesis in §2.4).

---

## Find-and-replace table (consolidated)

(See T11 for the canonical list; this table is what the executing agent should run across the whole Google Doc.)

| # | Before | After |
|---|--------|-------|
| 1 | first integrated multi-layer adaptive architecture combining BKT, Elo, MAB, and FSRS for programming education | integrated multi-layer adaptive architecture that combines BKT, Elo, MAB, and FSRS for programming education |
| 2 | the first integrated | an integrated |
| 3 | fully unified | integrated |
| 4 | a novel contribution | a contribution of this thesis |
| 5 | novel contribution | contribution of this thesis |
| 6 | addresses the gap | addresses this integration question |
| 7 | addresses this integration gap | addresses this integration question |
| 8 | To the best of our knowledge, this thesis is the first to apply the FSRS algorithm to programming concept review scheduling. | Within the scope of the programming education literature surveyed in Chapter 2, this thesis appears to be among the first to apply the FSRS algorithm to programming concept review scheduling. |
| 9 | To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis. | Within the scope of the literature surveyed in Chapter 2, this appears to be among the first applications of the FSRS algorithm [12] to programming skill retention, and is described here as a secondary contribution of the thesis. |
| 10 | produces emergent adaptive behavior that no single technique achieves alone | exhibits adaptive behaviour that combines signals from multiple techniques |
| 11 | will demonstrate significantly higher | will show higher |
| 12 | comprehensive whole-system demonstration of the adaptive system | whole-system description of the adaptive platform |

---

## Execution order for the downstream agent

1. T1, T2, T4, T5 — Chapter 5 framing and metric retone.
2. T3 — Threats to Validity section.
3. T6 — Abstract rewrite.
4. T7, T8, T9 — Introduction / RQs / Objectives / Contributions.
5. T11 (global find-and-replace), T14, T15, T16, T17 — language cleanup.
6. T12, T13 — redundancy deletions.
7. T10 — Declaration / Acknowledgements boilerplate.
8. T18 — formatting / numbering audit pass.

Each task should be committed as an atomic change so that a reviewer can diff them against the advisor's feedback points.
