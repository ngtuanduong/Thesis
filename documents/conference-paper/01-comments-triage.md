# Advisor Comments Triage — Conference Paper

**Source doc:** `1B72mF57eyHFaCgTI-zVvZ01RWOuJInFemI-dVl_qxvA` (review doc)
**Pulled:** 2026-04-21
**Advisor:** Bui Quoc Khanh
**Total unresolved:** 21
**Note:** All comments are anchorless (no quoted text) — triage based on comment content.

**Labels:**
- **CONF-CRITICAL** — must apply in the conference paper
- **CONF-NICE** — nice to have in the paper if space permits
- **THESIS-ONLY** — addresses the full thesis, not the conference paper
- **IGNORE** — not actionable or duplicate already consolidated

---

## CONF-CRITICAL (13 actionable items)

| # | Label | Section it affects | Required action |
|---|---|---|---|
| 2 | CRITICAL | §3 Methodology (control group) | Fix logic: control group holds constant *the platform interface and problem environment while varying the recommendation logic*, NOT "holds constant the effect of the four-layer adaptive engine". |
| 4 | CRITICAL | §4 Results/Discussion (eval framing) | Preserve the core evaluation message from Chapter 5 — the evaluation *is a pre-registered pilot protocol*, not a completed study. Use this framing verbatim. |
| 5 | CRITICAL | §4.1 Results | Highlight implementation evidence (deployed system, code metrics, Docker sandbox) — this proves "not just conceptual design". |
| 6 | CRITICAL | §3 MAB layer | Add one sentence: *"The reward weights (0.5, 0.3, 0.2) are a heuristic weighting combining learning gain, difficulty match, and efficiency; they are not learned from empirical data."* |
| 7 | CRITICAL | §3 Elo layer | Add one sentence: *"K = 25 is a heuristic midpoint chosen for moderate volatility in educational settings, not a tuned optimum."* Committees always ask about hyperparameters. |
| 8 | CRITICAL | §3 BKT layer (mastery threshold) | Add one sentence: *"The mastery threshold θ_m = 0.85 is a design choice informed by the ITS literature, not empirically optimized on this dataset."* Preempts "why 0.85 not 0.8 or 0.9?" |
| 9 | CRITICAL | §3 Methodology (emphasis) | Technical chapters 3–4 are the paper's strength — give Methodology the most page-space (~2.25 pages as budgeted). |
| 10+11+12 | CRITICAL | §2 Related Work structure | Cut literature review depth 20–30%. Keep only the parts that justify design decisions. End each subsection with a "Relevance to this work" closing (1–2 sentences) explaining how that literature informs a concrete thesis choice. |
| 14 | CRITICAL | Abstract + §5 Conclusion | Add: *"Contribution 1 (the integrated adaptive platform) is implemented and demonstrated technically; Contribution 2 (the evaluation protocol) is specified but not yet empirically executed."* Explicit artifact-vs-plan distinction. |
| 16 | CRITICAL | All sections | Tense consistency. System is implemented/deployed → use present or past tense consistently; avoid mixing future tense. |
| 17 | CRITICAL | §3 + §4 (RQ framing) | Refocus RQ1 on **predictive validity** (BKT/Elo AUC). Relegate acceptance rate and convergence speed to *supporting indicators*. |
| 18 | CRITICAL | §1 Introduction + §5 Conclusion | Add defensive sentence: *"This paper should be read as an implementation paper with a pilot evaluation protocol, not as a completed classroom study."* |
| 19 | CRITICAL | §2 Related Work | Factual fix: Duolingo = language learning, not programming. Rewrite as: *"Duolingo demonstrates the scalability of adaptive techniques in language learning, which suggests potential transfer to programming education."* |

---

## CONF-NICE (3 items — apply if space permits)

| # | Label | Section | Note |
|---|---|---|---|
| 1 | NICE | §5 Conclusion | A one-sentence takeaway suitable for the conference's closing slide — can double as the paper's final sentence. |
| 3 | NICE | Q&A prep only | A specific sentence worth quoting verbatim during Q&A — useful to *keep in the paper* so it is visible to reviewers. |
| 15 | NICE | §5 Conclusion | "Nhấn mạnh cái này ở hội thảo" — context-less, but timestamped right before #14 and #18, likely means "emphasize the artifact-vs-plan distinction". Already covered by #14. |

---

## THESIS-ONLY (3 items — defer to full thesis session)

| # | Label | Note |
|---|---|---|
| 13 | THESIS | Check Figure 1.4 alignment with new contribution — Figure 1.4 is thesis-only; conference paper will not include the thesis-structure roadmap figure. |
| 20 | THESIS | "Figure 1.1 đâu" — thesis Figure 1.1 (research-gap Venn) missing/misplaced in thesis doc. Not in conference paper. |
| 21 | THESIS | "3.1.3 đâu" — thesis section 3.1.3 missing/misplaced. Not in conference paper. |

---

## Synthesis — Cross-cutting directives for the paper

From the CRITICAL set, five directives emerge that must shape **every** section:

1. **Artifact vs plan distinction is THE central rhetorical move.** Comments #4, #5, #14, #18 all point to the same thing: the paper must claim "implementation is done, evaluation is pre-registered and pending" — not overclaim results.

2. **Every hyperparameter / threshold gets a rationale sentence.** Comments #6, #7, #8. Defensive writing preempts committee questions.

3. **Literature review is terse and must end each block with "relevance to this work".** Comment #10 (triplicated at #11, #12 — advisor clearly wants this emphasized).

4. **RQ1 is about predictive validity only.** Comment #17. Acceptance rate and convergence speed → supporting indicators.

5. **Fact-check Duolingo and any other cross-domain examples.** Comment #19.

---

## Items NOT in advisor comments but flagged by us (context-derived)

- Section 4 "Results" should present **system metrics** (not learning outcomes), per the design-paper framing agreed in plan.
- Title + abstract need Vietnamese + English per thể lệ.
- References capped at 15 entries, APA 7.
