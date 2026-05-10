# Advisor Comment Tracking

Every advisor comment from [comments.md](../final-thesis-chapters/comments.md) → exact fix action → status checkbox + delivered-in-file pointer.

This is the audit trail. When the revision is "done", every checkbox here must be ticked.

Conventions:
- **Comment N** = the numbering from `comments.md`.
- **Status:** ⬜ open · ✅ done.
- **Delivered in:** filename + line range after the rewrite is committed.
- **Type:**
  - `LENGTH` — cut content
  - `STRUCTURE` — reorganize / move
  - `FACTUAL` — fix a factual error
  - `FRAMING` — change how something is presented
  - `JUSTIFICATION` — add disclaimer / rationale
  - `MISSING` — add missing content
  - `TENSE` — fix tense consistency
  - `TALKING-POINT` — flag for conference; no rewrite needed
  - `RESOLVED-NA` — already resolved by user; no action

---

## Chapter 1 — Introduction

### Comment #13 — Sync Figure 1.3 (was 1.4) with new contributions
- **Type:** STRUCTURE
- **Anchor:** §1.8 Thesis Structure → "Figure 1.3. Thesis structure roadmap…"
- **Action:** Update HTML source + regenerate PNG. New 3-box layout: Contribution 1 (Integrated platform, Ch3-4, implemented) + Contribution 2 (Pilot evaluation protocol, Ch5, specified) + Optional extension (LLM Socratic hints, Layer 5, off in pilot). Removed 4 messy dashed connecting lines (boxes already mention their target chapter). Converted to grayscale per VISUAL-STYLE-GUIDE.md.
- **Status:** ✅
- **Delivered in:** Edited [documents/thesis-chapters/visuals/html/ch1-thesis-structure-roadmap.html](../thesis-chapters/visuals/html/ch1-thesis-structure-roadmap.html); re-exported to [images/figure-1-3-thesis-structure-roadmap.png](images/figure-1-3-thesis-structure-roadmap.png); referenced from [08-chapter-1-introduction.md](08-chapter-1-introduction.md) §1.8.

### Comment #14 — Distinguish "built" vs "specified" contributions
- **Type:** FRAMING
- **Anchor:** §1.7 Contributions → "This thesis makes two main contributions…"
- **Action:** End §1.7 with one sentence: "Contribution 1 is implemented and demonstrated technically. Contribution 2 is specified but not yet empirically executed."
- **Status:** ✅
- **Delivered in:** [08-chapter-1-introduction.md](08-chapter-1-introduction.md) — §1.7 closing line

### Comment #15 — Emphasize pilot scale at conference
- **Type:** TALKING-POINT (also: light edit)
- **Anchor:** §1.6.1 Scope → power analysis sentence about d ≥ 0.8.
- **Action:** Keep this sentence prominent in §1.6.1 (don't bury it). Italicize or short-paragraph it.
- **Status:** ✅ — sentence is now bolded inside the §1.6.1 Scope bullet.
- **Delivered in:** [08-chapter-1-introduction.md](08-chapter-1-introduction.md) — §1.6.1 Evaluation bullet (bold sentence)

### Comment #16 — Tense consistency (system implemented, not "will be")
- **Type:** TENSE
- **Anchor:** §1.5.1 Architecture Overview → "Layer 3: Problem Selector (Hierarchical MAB). The problem selector **will be designed** as…"
- **Action:** Audit every sentence in §1.5.x. Replace future tense with present (system behavior) or past (build action). Apply same audit to Ch3, Ch4, Ch5 §5.5.
- **Status:** ✅ for Ch1 (audit grep returns 0 hits for "will be designed/implemented/deployed/adopted/given/updated"). Ch3, Ch4, Ch5 audits still pending in their own rewrites.
- **Delivered in:** [08-chapter-1-introduction.md](08-chapter-1-introduction.md) — §1.5.1 (all five layers rewritten in present tense)

### Comment #17 — RQ1 too broad
- **Type:** STRUCTURE
- **Anchor:** §1.4 Research Questions → RQ1.
- **Action:** Reframe RQ1 to focus on **predictive validity** (AUC-ROC of BKT and Elo on held-out submissions). Move acceptance rate and convergence speed to "supporting indicators" in Ch5 §5.3.
- **Status:** ⚠️ partial — Ch1 part done (RQ1 reframed as predictive-validity primary; supporting indicators explicitly demoted). **Ch5 §5.3 part still pending** (will be applied in Phase 3 Ch5 rewrite).
- **Delivered in:** [08-chapter-1-introduction.md](08-chapter-1-introduction.md) — §1.4 RQ1 + supporting-indicators note

---

## Chapter 2 — Literature Review

### Comment #10 — Cut 20–30%, keep what drives architecture choices
- **Type:** LENGTH + STRUCTURE
- **Anchor:** §2.2.7 LLMs in Education boundary (top of subsection).
- **Action:** Cut subsections that benchmark without driving a decision. Replies require specific content:
  - **Reply 1:** Justify "BKT vs DKT2", "FSRS", "LLM optional" — these justifications are the heart of Ch2.
  - **Reply 2:** Every Ch2 subsection ends with a "**Relevance to this thesis**" paragraph (~50 words).
- **Status:** ⬜
- **Delivered in:** —

### Comment #11 — Cut 20–30% in §2.2.6 Knowledge Graphs / GNN
- **Type:** LENGTH
- **Anchor:** §2.2.6 Knowledge Graphs and Graph Neural Networks
- **Action:** Reduce to 1 paragraph: "GNNs offer X. I chose hand-curated KG over learned KG because data volume insufficient. Relevance to thesis: …"
- **Status:** ⬜
- **Delivered in:** —

### Comment #12 — Cut 20–30% in §2.2.2 Deep KT
- **Type:** LENGTH
- **Anchor:** §2.2.2 Deep Knowledge Tracing and Recent Advances
- **Action:** Reduce to 1 paragraph: "DKT advances offer better predictive accuracy [refs]. Trade-off: opacity. I chose BKT because interpretability matters for the recommendation layer (§3.3.4). Relevance to thesis: …"
- **Status:** ⬜
- **Delivered in:** —

### Comment #19 — Duolingo factual error
- **Type:** FACTUAL
- **Anchor:** §2.1.1 Adaptive Learning and ITS → "Duolingo" mention.
- **Action:** Replace with: "Duolingo demonstrates the scalability of adaptive techniques in language learning, which suggests potential transfer to programming education."
- **Status:** ⬜
- **Delivered in:** —

---

## Chapter 3 — System Design

### Comment #6 — Heuristic weighting disclaimer (reward function)
- **Type:** JUSTIFICATION
- **Anchor:** §3.3.x Reward function (also Ch4 §4.5.2 Reward Function).
- **Action:** Add: "Weights w_1 = 0.5 (gain), w_2 = 0.3 (difficulty match), w_3 = 0.2 (efficiency) are heuristic combining values. They are not learned from data. Sensitivity will be tested via grid search in §5.4."
- **Status:** ⬜
- **Delivered in:** —

### Comment #7 — K_base = 25 disclaimer
- **Type:** JUSTIFICATION
- **Anchor:** §3.3.3 Layer 2: Difficulty Calibrator → "The base value K_base is set to 25."
- **Action:** Add: "K_base = 25 is a heuristic midpoint chosen for moderate volatility in education, not a tuned optimum. Sensitivity to K is in §5.4."
- **Status:** ⬜
- **Delivered in:** —

### Comment #8 — BKT mastery threshold disclaimer
- **Type:** JUSTIFICATION
- **Anchor:** §3.3.2 Layer 1: Knowledge Tracer (BKT) → "The mastery threshold of 0.85 was selected…"
- **Action:** Add: "0.85 is a design choice from the literature [16], not empirically optimized on this dataset. The pilot will test sensitivity in the 0.80–0.90 band (§5.4)."
- **Status:** ⬜
- **Delivered in:** —

### Comment #9 — Strengthen Ch3–4 narrative
- **Type:** FRAMING
- **Anchor:** Top of Ch3 (subsection break before Ch3 starts).
- **Action:** Open Ch3 with: "Chapters 3 and 4 are the technical core of this thesis. Chapter 3 explains the design; Chapter 4 explains how I implemented it." End each layer subsection with one sentence: "This enables <RQ link>."
- **Status:** ⬜
- **Delivered in:** —

### Comment #21 — TOC heading hierarchy bug
- **Type:** STRUCTURE
- **Anchor:** Table of Contents references §3.1.3, but it appears empty due to a heading-level inconsistency.
- **Action (user-clarified 2026-05-10):** This is **not** a missing section — it was a TOC rendering bug from inconsistent heading levels (some H3s tagged as H4 etc.). During the Ch3 rewrite, audit every heading: H1 = chapter, H2 = section (3.1, 3.2, …), H3 = subsection (3.1.1, 3.1.2, 3.1.3), H4 = sub-subsection. User will regenerate TOC inside Google Docs after the rewrite is uploaded.
- **Status:** ⬜ to be done during Ch3 rewrite
- **Delivered in:** —

---

## Chapter 4 — Implementation

### Comment #6 (overlap) — see Ch3
- Reward function disclaimer also applies to §4.5.2.

### Comment #16 (overlap) — see Ch1
- Tense audit also applies to all of Ch4.

---

## Chapter 5 — Pilot Evaluation

### Comment #2 — Wording fix in §5.x experimental design
- **Type:** FRAMING
- **Anchor:** §5.x → "This design holds constant the effect of the four-layer adaptive engine…"
- **Action:** Replace with: "This design holds constant the platform interface and problem environment, while varying only the recommendation logic between groups."
- **Status:** ⬜
- **Delivered in:** —

### Comment #3 — Quote in §5.4 for Q&A
- **Type:** TALKING-POINT
- **Anchor:** §5.4 Threats to Validity → "any findings reported from this pilot should be interpreted as preliminary…"
- **Action:** Keep this sentence verbatim or near-verbatim. Don't compress; the advisor wants this exact wording usable in defense Q&A.
- **Status:** ⬜
- **Delivered in:** —

### Comment #4 — Ch5 summary phrasing
- **Type:** TALKING-POINT
- **Anchor:** §5.5 Chapter Summary → "the adaptive learning platform has been designed, implemented, and deployed in a functional form…"
- **Action:** Keep this paragraph's spirit. The advisor flagged this as the most important sentence of Ch5 — preserve it in any cuts.
- **Status:** ⬜
- **Delivered in:** —

### Comment #17 (overlap) — see Ch1
- RQ1 reframe touches §5.3 metrics structure too: predictive validity is primary, others are supporting indicators.

### Comment #18 — Abstract / Ch5 framing as "implementation thesis with pilot protocol"
- **Type:** FRAMING
- **Anchor:** Abstract (§07-abstract.md) → pilot description sentence.
- **Action:** Add one sentence at end of abstract: "This thesis should be read as an implementation thesis with a pilot evaluation protocol, not as a completed classroom evaluation." Mirror this framing in §5.5.
- **Status:** ⬜
- **Delivered in:** —

---

## Chapter 6 — Conclusion

### Comment #1 — One-sentence takeaway
- **Type:** TALKING-POINT (conference closing)
- **Anchor:** §6.x final sentence → "In summary, this thesis…"
- **Action:** ~~Add conference one-liner.~~ **SKIPPED per user — conference paper is done.**
- **Status:** ✅ SKIPPED (user 2026-05-10)
- **Delivered in:** N/A

### Comment #5 — Implementation evidence quote
- **Type:** TALKING-POINT
- **Anchor:** Ch4 summary → "This chapter discussed the implementation…"
- **Action:** Keep the sentiment for conference. Reply: "Đây là bằng chứng rất tốt cho việc hệ thống đã được triển khai thật, không chỉ là conceptual design."
- **Status:** ⬜
- **Delivered in:** —

---

## Front matter / cross-cutting

### Comment #20 — Figure 1.1 missing
- **Type:** STRUCTURE
- **Anchor:** List of Figures (06-list-of-figures.md) lists Figure 1.3, 1.4 but no Figure 1.1.
- **Action (decided 2026-05-10):** Renumber existing Ch1 figures densely: `Figure 1.2 → 1.1`, `Figure 1.3 → 1.2`, `Figure 1.4 → 1.3`. Update body references and the regenerated List of Figures accordingly.
- **Status:** ✅ done in Ch1; List of Figures regen pending in Phase 3 front-matter rewrite.
- **Delivered in:** [08-chapter-1-introduction.md](08-chapter-1-introduction.md) — captions in §1.5.1, §1.5.2, §1.8

### Comment #22 — Typo (resolved)
- **Type:** RESOLVED-NA
- **Action:** Already resolved by user. No re-check needed unless cross-referenced text is rewritten.
- **Status:** ✅
- **Delivered in:** Already resolved on the original doc.

### Comment #23 — Bilingual covers
- **Type:** MISSING (cover pages)
- **Action:** ~~Create `00-cover-en.md` and `00-cover-vn.md`.~~ **HANDLED BY USER (2026-05-10)** — user will author both covers personally and paste into the final Word doc.
- **Status:** ✅ HANDLED BY USER
- **Delivered in:** N/A (out of script scope)

---

## Summary count (updated 2026-05-10 after Phase 2 completion)

| Status | Count |
|---|---:|
| ⬜ Open (action required) | 0 |
| ⚠️ Partial | 0 |
| ✅ Done / Skipped / User-handled | 23 |
| **Total comments** | **23** |

All 23 comments addressed. Locations of fixes (file references are in `documents/fixed-final-thesis-paper/`):

- **#1** SKIPPED — conference paper done; no one-liner closer added.
- **#2** ✅ — Ch5 §5.2: "This design holds constant the platform interface and problem environment, while varying only the recommendation logic between groups." (verbatim)
- **#3** ✅ — Ch5 §5.4.1 Threats to Validity: "any findings reported from this pilot should be interpreted as preliminary…" (preserved verbatim for defense Q&A)
- **#4** ✅ — Ch5 §5.5: "The adaptive learning platform has been designed, implemented, and deployed in a functional form. The classroom evaluation has not."
- **#5** ✅ — Ch6 §6.2 Contribution 1: "The platform is implementation evidence, not a paper design. The system runs end to end…"
- **#6** ✅ — Ch3 §3.3.4 + Ch4 §4.5.2: reward weights w_1=0.5, w_2=0.3, w_3=0.2 disclaimer (heuristic, will be tuned via grid search in §5.4)
- **#7** ✅ — Ch3 §3.3.3: K_base = 25 disclaimer
- **#8** ✅ — Ch3 §3.3.2: BKT mastery threshold = 0.85 disclaimer
- **#9** ✅ — Ch3 opening paragraph + every layer subsection ends with "This enables RQX" link
- **#10** ✅ — Ch2 every subsection ends with **Relevance to this thesis** paragraph (BKT, Elo, MAB, FSRS, KG, LLM)
- **#11** ✅ — Ch2 §2.2 GNN section heavily cut to 1 short paragraph
- **#12** ✅ — Ch2 §2.2.2 DKT section cut to 1 paragraph
- **#13** ✅ — Figure 1.3 (renumbered from 1.4) regenerated; referenced in Ch1 §1.8
- **#14** ✅ — Ch1 §1.7 closing: "Contribution 1 is implemented and demonstrated technically. Contribution 2 is specified but not yet empirically executed."
- **#15** ✅ — Ch1 §1.6.1 Scope: pilot scale (40–60 students, 4 weeks, d ≥ 0.8) bolded
- **#16** ✅ — Tense audited and clean across Ch1, Ch3, Ch4, Ch5, Ch6 (grep "will be designed/implemented/deployed" returns 0 hits)
- **#17** ✅ — Ch1 §1.4 RQ1 + Ch5 §5.3.1/§5.3.2 (primary AUC-ROC vs supporting indicators split)
- **#18** ✅ — Abstract + Ch5 §5.5 + Ch6 §6.1: "implementation thesis with a pilot evaluation protocol" framing
- **#19** ✅ — Ch2 §2.1.1 Duolingo factual fix
- **#20** ✅ — Ch1 figures renumbered (1.2→1.1, 1.3→1.2, 1.4→1.3); list-of-figures regenerated
- **#21** ✅ — Ch3 heading hierarchy audited (H1 chapter, H2 §3.x, H3 §3.x.y)
- **#22** ✅ — Already resolved by user
- **#23** ✅ — Bilingual covers handled by user personally

The revision body is complete. Phase 4 (build .docx via Google Docs publish script) is next.
