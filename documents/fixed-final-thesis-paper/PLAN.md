# Final Thesis Revision — Master Plan

**Status:** PROPOSED — awaiting user sign-off on per-chapter cut targets.
**Owner:** Nguyễn Tuấn Dương · advisor: ThS. Bùi Quốc Khánh.
**Created:** 2026-05-10.
**Source:** [documents/final-thesis-chapters/](../final-thesis-chapters/) (English body, 19 sections, 38,569 words ≈ 142 dense pages, 54 images, 18 tables).
**Target:** [documents/fixed-final-thesis-paper/](.) (English body + bilingual covers, ≈ 18,900 words ≈ 70 pages).

---

## 1. Why this revision exists

Three drivers:

1. **Length.** Current paper is ~180 printed pages (with figures and formatting); target is 70. Halve the body word count.
2. **Advisor feedback.** 21 located + 2 resolved comments from ThS. Bùi Quốc Khánh, ranging from factual fixes (Duolingo isn't programming, Figure 1.1 missing) to structural rewrites (RQ1 too broad, lit review needs "relevance" closings, system tense is inconsistent).
3. **Voice.** Current draft reads like a journal paper. The defense audience expects an undergraduate's voice — confident on the build, honest about what's pilot vs. validated, plain-English where jargon isn't needed. Voice rules are in [UNDERGRAD-VOICE-GUIDE.md](UNDERGRAD-VOICE-GUIDE.md).

Final deliverable: a `.docx` Word file produced by concatenating the revised markdown files and converting them with pandoc against a Decision 612/QD-DHHN reference template. No Google Doc step in the build path; covers are added by the user directly in Word after the build.

---

## 2. Constraints (user-confirmed)

| Constraint | Value | Source |
|---|---|---|
| Body language | English (keep as-is) | User Q1 |
| Cover pages | Bilingual: English + Vietnamese | Comment #23 + User Q1 |
| Review pace | Pilot Chapter 1 → user reviews → auto for Ch2–Ch6 | User Q2 |
| Appendices | Cut to ~30% of current (Appendix A: 1,000 w · Appendix B: 700 w) | User Q3 |
| Build pipeline | Concatenate markdown → pandoc → `.docx` (Decision 612 reference template); covers added in Word | User Q4 (revised 2026-05-10) |
| Reuse style | A persistent voice guide — applied by every rewrite | User intent |

---

## 3. Discovery (baseline measurements)

### 3.1 Current word counts

| Section | Now | Target | Cut | Pages (target) |
|---|---:|---:|---:|---:|
| 00 Front matter | 103 | 103 | 0% | <1 |
| 01 Declaration | 135 | 150 | — | <1 |
| 02 Acknowledgement | 79 | 80 | — | <1 |
| 03 TOC | 13 | (auto) | — | 1–2 |
| 04 Abbreviations | 75 | 80 | — | <1 |
| 05 List of tables | 104 | 80 | 23% | <1 |
| 06 List of figures | 261 | 200 | 23% | 1 |
| 07 Abstract | 297 | 250 | 16% | 1 |
| **08 Ch1 Introduction** | 3,903 | **1,700** | **56%** | **6** |
| **09 Ch2 Lit review** | 7,113 | **3,000** | **58%** | **11** |
| **10 Ch3 System design** | 7,432 | **4,000** | **46%** | **14** |
| **11 Ch4 Implementation** | 5,743 | **3,200** | **44%** | **11** |
| **12 Ch5 Pilot evaluation** | 4,430 | **2,000** | **55%** | **7** |
| 14 Ch6 Conclusion | 1,582 | 1,000 | 37% | 3 |
| 15 References | 1,351 | 1,351 | 0% | 5 |
| 18 Appendix A | 3,426 | 1,000 | 71% | 3 |
| 19 Appendix B | 2,522 | 700 | 72% | 2 |
| **TOTAL** | **38,569** | **18,907** | **51%** | **~70** |

Bold rows = primary cuts. Front matter and references stay roughly intact.

### 3.2 Comment classification (full mapping in [COMMENT-ACTIONS.md](COMMENT-ACTIONS.md))

| Theme | Count | Comments |
|---|---:|---|
| Length cuts (-20–30% per advisor) | 3 | #10, #11, #12 |
| Tense fixing (system = present/past consistent) | 1 | #16 |
| Lit-review "relevance to thesis" closings | 1 | #10 (reply) |
| Justify choices (BKT vs DKT, FSRS, LLM optional) | 1 | #10 (reply) |
| Hyperparameter "design choice" disclaimers | 3 | #6, #7, #8 |
| Reframe RQ1 (predictive validity is primary) | 1 | #17 |
| Implementation thesis framing | 2 | #18, #14 |
| Factual fix (Duolingo) | 1 | #19 |
| Missing items | 3 | #20 (Fig 1.1), #21 (§3.1.3), #22 (typo, resolved) |
| Bilingual cover | 1 | #23 (resolved) |
| Strengthen Ch3–4 narrative | 1 | #9 |
| Conference talking-points (no rewrite needed) | 6 | #1, #2, #3, #4, #5, #15 |
| Sync Figure 1.4 with new contributions | 1 | #13 |

---

## 4. Phased plan

### Phase 0 · Discovery & sign-off **← we are here**
- [x] Voice guide written: [UNDERGRAD-VOICE-GUIDE.md](UNDERGRAD-VOICE-GUIDE.md)
- [x] Master plan: this file
- [ ] Comment-action mapping: [COMMENT-ACTIONS.md](COMMENT-ACTIONS.md) (next)
- [ ] **User reviews voice guide + per-chapter targets, signs off.**

### Phase 1 · Pilot rewrite of Chapter 1
- Rewrite [08-chapter-1-introduction.md](../final-thesis-chapters/08-chapter-1-introduction/08-chapter-1-introduction.md) using the voice guide.
- Address all 5 comments anchored in Ch1: #13 (Figure 1.4 sync), #14 (Contribution 1 vs 2 distinction), #15 (pilot scale emphasis), #16 (tense consistency in §1.5.1), #17 (RQ1 reframe).
- Output: [01-chapter-1-introduction.md](.) (target 1,700 words).
- **User reviews** voice + cuts.
- If approved → proceed to Phase 2. If not → iterate.

### Phase 2 · Auto-rewrite Ch2–Ch6 + front matter + appendices
Rewrite each section in order, applying the voice guide. Per-chapter specs in §5 below.

Order:
1. Front matter (cover pages EN + VN, declaration, ack, abbreviations, lists, abstract)
2. Ch2 Literature review — biggest cut (-58%); add "Relevance to this thesis" closings
3. Ch3 System design — moderate cut (-46%); fix §3.1.3, hyperparameter disclaimers, strengthen narrative
4. Ch4 Implementation — moderate cut (-44%); fix reward function disclaimer, tense
5. Ch5 Pilot evaluation — moderate cut (-55%); reframe RQ1 supporting indicators
6. Ch6 Conclusion — light cut (-37%); align with new contributions
7. Appendix A — heavy cut (-71%); keep summary tables, drop full Q&A
8. Appendix B — heavy cut (-72%); keep concept list, drop full graph spec
9. References — verify, no rewrite

### Phase 3 · Cross-chapter consistency
- Regenerate TOC (manual, since pandoc/Docs auto-builds it on the live doc)
- Update List of Figures + List of Tables to reflect new figure/table set
- Verify every `[N]` citation appears in References, no orphans
- Verify figure numbering is dense (no gaps)
- Add missing Figure 1.1 (per Comment #20) — confirm it exists in the source images or mark as TODO

### Phase 4 · Build the Word file
1. Concatenate the 16 ordered markdown files (front matter → chapters → references → condensed appendices) into a single working file with explicit page breaks between sections.
2. Run pandoc against `reference.docx` (Decision 612/QD-DHHN style template) to produce `Adaptive-Learning-Platform-Final.docx`.
3. User opens the docx in Word and adds: English cover page, Vietnamese cover page (per Comment #23), and any spacing/page-break tweaks.
4. User refreshes TOC, List of Tables, List of Figures inside Word.
5. Save as the submission file. Detailed steps and command in §7.

### Phase 5 · Final check & delivery
- Word count check: actual ≤ 19,500 (a 3% buffer over target).
- Page count check: visual page count of the docx ≤ 75 (5-page buffer).
- Comment satisfaction check: every advisor comment has a corresponding edit (cross-reference COMMENT-ACTIONS.md).
- Final PDF preview from the docx.

---

## 5. Per-chapter rewrite specs

These specs are applied during Phase 1 (Ch1) and Phase 2 (rest). Each spec lists: target word count, what to keep, what to cut, what to merge, comments to address.

### 5.1 Chapter 1 — Introduction (3,903 → 1,700 words, -56%)

**Keep (rewrite to undergrad voice):**
- §1.1 Problem statement — core failure rate / heterogeneity argument. Compress 2 paragraphs into 1.
- §1.2.1 Promise of adaptive learning — 1 paragraph max.
- §1.2.2 Why programming is uniquely suited — 1 paragraph (cut from 4).
- §1.2.3 Gap in existing platforms — keep table reference (Table 1.1), drop the multi-paragraph platform-by-platform breakdown (table covers it).
- §1.4 Research questions — keep RQ1, RQ2; **reframe RQ1 per Comment #17** (predictive validity primary; acceptance / convergence become "supporting indicators in Chapter 5").
- §1.5 Solution overview — keep architecture sketch (Figure 1.3); **fix tense per Comment #16** (system is implemented, not "will be designed").
- §1.6.1 Scope — **emphasize pilot scale per Comment #15** (40-60 students, 4 weeks, can detect d ≥ 0.8 only).
- §1.7 Contributions — **add Comment #14 closing**: "Contribution 1 is implemented and demonstrated technically; Contribution 2 is specified but not yet empirically executed."
- §1.8 Thesis structure — keep Figure 1.4; **verify Figure 1.4 is consistent with new contributions per Comment #13**.

**Cut entirely:**
- Most of §1.2 expansion (already covered by table 1.1)
- §1.5 sub-paragraph that re-describes layers in detail (Chapter 3 covers this)
- "In this thesis, the following will be presented…" procedural narration

**Renumber figures (per Comment #20, decided 2026-05-10):**
- `Figure 1.2 → Figure 1.1` (Closed-loop adaptive workflow)
- `Figure 1.3 → Figure 1.2` (Five-layer adaptive engine architecture)
- `Figure 1.4 → Figure 1.3` (Thesis structure roadmap)
- Update body in-text references and List of Figures accordingly. No new figure needs to be created.

**Comments addressed:** #13, #14, #15, #16, #17, #20.

---

### 5.2 Chapter 2 — Literature Review (7,113 → 3,000 words, -58%)

**Keep:**
- §2.1 Background (adaptive learning history): 1 paragraph + 1 paragraph for ITS.
- §2.2 Knowledge tracing (BKT, DKT) — keep as the foundation for Ch3.
- §2.3 Difficulty / IRT — keep as foundation for Elo layer.
- §2.4 Spaced repetition (FSRS) — keep, justify FSRS choice.
- §2.5 MAB — keep, justify Thompson Sampling.
- §2.6 LLM in education — short, justify LLM as **optional layer**.
- §2.7 Synthesis & gap → Section 1.3 in this thesis.

**Cut hard:**
- All "this approach has been benchmarked on EdNet 2.0…" detail unless it drives a decision (per Comment #10).
- Entire timeline / history paragraphs (1990s ITS era). Compress to 2 sentences.
- Section 2.2.6 (Knowledge Graphs / GNN) — heavy cut per Comment #11. Keep ONLY the part justifying our hand-curated KG over a learned one.
- Section 2.2.2 (Deep KT advances) — heavy cut per Comment #12. 1 paragraph is enough.

**Add (per Comment #10 reply, the most important advisor instruction):**
- Every subsection ends with a **"Relevance to this thesis"** paragraph (~50 words):
  - 2.2 BKT: "I chose BKT because <interpretability for layer 3>; DKT was rejected because <opacity>."
  - 2.3 IRT/Elo: "I chose dynamic Elo because <continuous calibration without item-fitting>; full IRT was rejected because <too few responses per item>."
  - 2.4 FSRS: "I chose FSRS because <state-of-the-art retention modeling, open algorithm>; SM-2 was rejected because <less accurate>."
  - 2.5 MAB: "I chose Thompson Sampling because <handles exploration/exploitation cleanly with priors from BKT>."
  - 2.6 LLM: "LLM is optional because <feedback quality varies, expensive>; not a core layer."

**Fix:** Comment #19 — Duolingo factual error.

**Comments addressed:** #10, #11, #12, #19.

---

### 5.3 Chapter 3 — System Design (7,432 → 4,000 words, -46%)

This is the technical strength per Comment #9. Cut less, but cleaner.

**Keep (more aggressive than other chapters because thầy said make it stand out):**
- §3.1 Requirements — keep functional + non-functional + traceability matrix (Table 3.2).
- §3.2 Architecture overview (Figure 3.1) — keep, polish.
- §3.3 Five-layer engine — keep all 5 layers, but each tighter.
- §3.4 Data model & knowledge graph — keep, with Figure 3.2.
- §3.5 Sequence diagrams (Figure 3.3, 3.4) — keep both.

**Cut:**
- Long descriptions of "how Elo works in chess" — 2 sentences max, then go to the variant.
- Repetition between §3.2 and §3.3 (architecture is described twice).
- Layer interaction matrix (Figure 3.6) — keep figure, drop the prose that re-narrates it.

**Add (per Comments #6, #7, #8):**
- **§3.3.2 BKT** — add: "The mastery threshold is 0.85, the midpoint of the 0.80–0.90 range recommended in [16]. This is a design choice from the literature, not optimized on this dataset."
- **§3.3.3 Elo** — add: "K_base = 25 is a heuristic midpoint chosen for moderate volatility in education, not a tuned optimum. Sensitivity to K is in §5.4."

**Heading hierarchy audit (per Comment #21, decided 2026-05-10):**
- Comment #21 was a TOC rendering bug, NOT a missing section. During the rewrite, audit every Ch3 heading: H1 = chapter, H2 = section (3.1, 3.2, …), H3 = subsection (3.1.1, 3.1.2, 3.1.3), H4 = sub-subsection. Ensure every numbered subsection has the right level so Google Docs auto-TOC renders correctly.

**Strengthen narrative (per Comment #9):**
- Open §3 with: "Chapter 3 presents the system that I designed and built. This is the technical heart of the thesis." — declare the chapter's importance up front.
- End each layer subsection with one sentence of "what this enables" (links layer to RQ).

**Comments addressed:** #6, #7, #8, #9, #21.

---

### 5.4 Chapter 4 — Implementation (5,743 → 3,200 words, -44%)

Same posture as Ch3: technical strength, cut redundancy not depth.

**Keep:**
- §4.1 Tech stack table (Table 4.1).
- §4.2 BKT impl (parameters table 4.2).
- §4.3 Elo impl (dual-rating, K-factor formulas).
- §4.4 MAB impl (hierarchical structure).
- §4.5 FSRS impl (card lifecycle, retrievability curve).
- §4.6 LLM feedback layer (mark explicitly OPTIONAL).
- §4.7 Frontend + deployment (1 paragraph each, link to figures).

**Cut:**
- Code snippets that just illustrate library calls — leave 1–2 illustrative ones.
- "We chose React because…" — covered in tech stack table.
- Re-derivation of Elo from chess — already covered in Ch3.

**Add (per Comment #6):**
- **§4.5.2 Reward function** — add: "Weights w_1=0.5 (gain), w_2=0.3 (difficulty match), w_3=0.2 (efficiency) are heuristic; they were not learned from data. They will be tuned by grid search in Section 5.4."

**Tense (per Comment #16):**
- "I designed", "I implemented", "the system uses" — past for build, present for current behavior. Audit every paragraph.

**Comments addressed:** #6, #16.

---

### 5.5 Chapter 5 — Pilot Evaluation Design (4,430 → 2,000 words, -55%)

**Keep:**
- §5.1 RQ table — but rewrite RQ1 per Comment #17.
- §5.2 Experimental design (between-subjects, control/experimental, sample size).
- §5.3 Metrics — primary metrics only, push secondary metrics to a single short paragraph.
- §5.4 Threats to validity — keep most; this is the most-cited section per the conference talking points.
- §5.5 Chapter summary — keep the "implementation thesis with pilot protocol" framing per Comment #18.

**Cut:**
- Long preamble explaining what an RCT is.
- Detailed power analysis derivation — keep the result table.
- §5.3 metric definitions: keep one-sentence definition per metric, not the half-page each.

**Reframe (per Comment #17):**
- RQ1: "How accurately does the learner model predict student performance?" — primary metric is **AUC-ROC of BKT and Elo predictions on held-out submissions**.
- Move acceptance rate, convergence speed, etc. to a "**Supporting indicators**" sub-paragraph at the bottom of §5.3.

**Tense (per Comment #4 / #16):** Pilot is **specified, not yet run**. Use future tense for pilot ("the study will recruit"); past tense only for what was done (designed, implemented).

**Comments addressed:** #2, #3, #4, #17, #18.

---

### 5.6 Chapter 6 — Conclusion (1,582 → 1,000 words, -37%)

**Keep:**
- §6.1 Summary of work — 1 paragraph: what was built, what was specified.
- §6.2 Contributions revisited — match Ch1's distinction (built vs. specified).
- §6.3 Limitations — honest list (no in-the-wild evaluation; small pilot sample; English-only platform).
- §6.4 Future work — short list, prioritized.

**Cut:**
- Long restatement of Chapter 1.
- "In conclusion, this thesis…" closing paragraph that adds no info.

**Add the closing line per Comment #1:**
- "If you remember one sentence from this thesis: <one-line takeaway>." — TODO with user (the takeaway should match the conference one-liner).

**Comments addressed:** #1.

---

### 5.7 Front matter (rewrite — covers handled by user)

| File | Current | Action |
|---|---|---|
| Cover EN + VN | (none — Comment #23) | **Out of scope — user authors both covers personally** |
| Declaration | 135 w | Rewrite to undergrad voice |
| Acknowledgement | 79 w | Light edit |
| TOC | (auto) | User regenerates inside Google Docs after upload |
| Abbreviations | 75 w | Verify all abbreviations actually appear in body |
| List of tables | 104 w | Regen after rewrite |
| List of figures | 261 w | Regen after rewrite using **renumbered Ch1 figures** (1.2→1.1, 1.3→1.2, 1.4→1.3 per Comment #20) |
| Abstract | 297 w | Add Comment #18's "implementation thesis with pilot protocol" framing |

---

### 5.8 Appendices (heavy cuts)

**Appendix A: Evaluation Instruments** (3,426 → 1,000 words):
- Keep: Sample test items (3 of each type), grading rubric summary, demographic survey questions list (not full text).
- Cut: Full 20-question pre-test, full 20-question post-test (move to a separate "Appendix A — Companion" markdown file outside the page count, link from main appendix).

**Appendix B: Knowledge Graph Specification** (2,522 → 700 words):
- Keep: Concept count summary, tier definitions, sample of 10 concepts (not all 53).
- Cut: Full 53-row table (move to companion markdown).

Companion files (don't count toward 70 pages):
- [appendix-a-companion-full-instruments.md](appendix-a-companion-full-instruments.md)
- [appendix-b-companion-full-kg.md](appendix-b-companion-full-kg.md)

---

## 6. Output structure

```
documents/fixed-final-thesis-paper/
├── PLAN.md                                  ← this file
├── UNDERGRAD-VOICE-GUIDE.md                 ← style guide
├── COMMENT-ACTIONS.md                       ← per-comment fix log
├── 00-cover-en.md                           ← English cover
├── 00-cover-vn.md                           ← Vietnamese cover (new, per #23)
├── 01-declaration.md
├── 02-acknowledgement.md
├── 03-toc.md                                ← marker only; auto-built in Google Docs
├── 04-abbreviations.md
├── 05-list-of-tables.md
├── 06-list-of-figures.md
├── 06b-list-of-listings.md           ← new (2026-05-10), List of Listings
├── 07-abstract.md
├── 08-chapter-1-introduction.md
├── 09-chapter-2-literature-review.md
├── 10-chapter-3-system-design.md
├── 11-chapter-4-implementation.md
├── 12-chapter-5-pilot-evaluation.md
├── 13-chapter-6-conclusion.md
├── 14-references.md
├── 15-appendix-a.md                         ← condensed
├── 16-appendix-b.md                         ← condensed
├── appendix-a-companion-full-instruments.md ← outside page count
├── appendix-b-companion-full-kg.md          ← outside page count
└── images/                                  ← copied from original (figures used in revised body only)
```

**Naming conventions:**
- Markdown files: `NN-<slug>.md` matching the existing convention so existing scripts can pick them up.
- Images: flat `images/` folder at root. Copy from source `documents/final-thesis-chapters/<chapter>/image/` and rename:
  - Drop the truncated suffix (e.g., `figure-1-2-closed-loop-...-knowledge-s.png` → `figure-1-1-closed-loop-adaptive-workflow.png`)
  - Apply Ch1 figure renumbering per Comment #20 (1.2→1.1, 1.3→1.2, 1.4→1.3)
  - Image filenames stay unique by chapter prefix (figure-1-N, figure-2-N, ..., table-N-M, sec-X-Y-...)
- Markdown image refs use **plural** `![](images/<file>.png)`, NOT singular `image/`. (The source convention was per-chapter `image/` subfolder; the target uses a single flat `images/` folder shared across chapters.)

**Visual style — grayscale required.** Every image in `images/` must follow [VISUAL-STYLE-GUIDE.md](VISUAL-STYLE-GUIDE.md): grayscale palette only (no saturated hues), distinguish categories by stroke pattern + weight + label rather than color. Bulk converter: [scripts/visual-grayscale-convert.py](../../scripts/visual-grayscale-convert.py). Re-exporter: [scripts/reexport-visuals-v2.py](../../scripts/reexport-visuals-v2.py) with `--output-dir images/`.

---

## 7. Build pipeline (Phase 4)

**Approach (decided 2026-05-10):** Pandoc → DOCX, no Google Docs intermediate. User Q4 was revised after seeing that the conference paper pipeline (`gdoc-write-conference-paper-docx.py`) already proved markdown → DOCX preserves headings, tables, italics, and inline images cleanly. Skipping Google Docs removes a brittle round-trip and the Docs-API styling pass.

Inputs: 16 ordered markdown files in this folder + 33 PNGs in [images/](images/) + a Decision 612/QD-DHHN reference template.
Output: `Adaptive-Learning-Platform-Final.docx` ready for Word polish.

### 7.1 One-time setup

**Pandoc (≥ 3.x):**
```powershell
winget install --id JohnMacFarlane.Pandoc -e
pandoc --version   # confirm ≥ 3.0
```

**Reference template — `reference.docx`:**
Create once at `documents/fixed-final-thesis-paper/reference.docx` carrying the Decision 612/QD-DHHN style set. Two ways to seed it:

- **From scratch:** `pandoc -o reference.docx --print-default-data-file reference.docx`, then open in Word and edit each style.
- **From existing styled doc:** copy the current main thesis doc (already styled) to `reference.docx`, delete its body content, keep style definitions.

Required style values — **verbatim from [HD-the-thuc-trinh-bay-KLTN.txt](../../HD-the-thuc-trinh-bay-KLTN.txt) §2.2.1** (Decision 612/QD-DHHN). Any deviation is a spec violation.

| Style | Font | Size | Weight | Alignment | Spacing | Notes |
|---|---|---:|---|---|---|---|
| Normal (body) | Times New Roman | 13 pt | regular | Justified | 1.5 line; first-line indent 1.27 cm; no letter-spacing compression | |
| Heading 1 (chapter) | Times New Roman | 16 pt | **bold UPPERCASE** | Centered | 32 pt before / 32 pt after | Page break before; "CHAPTER 1. INTRODUCTION" form |
| Heading 2 (1.1.) | Times New Roman | 14 pt | bold | **Justified both sides** | **6 pt before / 6 pt after** | |
| Heading 3 (1.1.1.) | Times New Roman | 13 pt | **regular (NOT bold)** | **Justified both sides** | 6 pt before / 6 pt after | Spec §2.2.1 Cấp 3 omits "in đậm" |
| Heading 4 (1.1.1.1.) | Times New Roman | 13 pt | **italic only (NOT bold)** | **Justified both sides** | 6 pt before / 6 pt after | Spec §2.2.1 Cấp 4 only says "in nghiêng" |
| Caption | Times New Roman | 12 pt | italic | Centered | 6 pt before / 6 pt after | Common practice; spec silent |
| Footnote Text | Times New Roman | 10 pt | regular | Justified | single line | Spec §2.2.2 |
| Block Quote | Times New Roman | 13 pt | regular | Justified, **left indent 1.27 cm** | 1.5 line | For 40+ word direct quotations (spec §3.1.2) |
| Source Code | **Consolas** (fallback Courier New) | 10 pt | regular | Left | line 1.0; 0/0 in-block; 6/0 first-line; 0/6 last-line | Frame added in post-process; gray #F5F5F5 shading; LaTeX `listings` analog (§10) |
| Verbatim Char | **Consolas** | 11 pt | regular | inline | — | Inline `` `code` `` spans (§10) |
| Page setup | — | — | — | — | — | A4 (210×297 mm), margins T 3 cm / B 3 cm / L 3.5 cm / R 2 cm; page number bottom-center |

### 7.2 File order for concatenation

The build script joins these files **in this order**, inserting `\newpage` (or pandoc raw `\pagebreak`) between each:

| # | File | Section in docx |
|---:|---|---|
| 1 | 01-declaration-of-authorship.md | Front matter |
| 2 | 02-acknowledgement.md | Front matter |
| 3 | _(TOC marker — pandoc fills via `--toc`)_ | Front matter |
| 4 | 04-abbreviations.md | Front matter |
| 5 | 05-list-of-tables.md | Front matter |
| 6 | 06-list-of-figures.md | Front matter |
| 6b | 06b-list-of-listings.md | Front matter (new — added 2026-05-10) |
| 7 | 07-abstract.md | Front matter |
| 8 | 08-chapter-1-introduction.md | Body |
| 9 | 09-chapter-2-literature-review.md | Body |
| 10 | 10-chapter-3-system-design.md | Body |
| 11 | 11-chapter-4-implementation.md | Body |
| 12 | 12-chapter-5-pilot-evaluation.md | Body |
| 13 | 13-chapter-6-conclusion.md | Body |
| 14 | 14-references.md | Back matter |
| 15 | 15-appendix-a.md | Back matter (condensed) |
| 16 | 16-appendix-b.md | Back matter (condensed) |

**Excluded from the docx** (kept as supplementary markdown only):
- `appendix-a-companion-full-instruments.md`
- `appendix-b-companion-full-kg.md`
- `00-cover-en.md` / `00-cover-vn.md` — covers are NOT in the markdown set; user authors them in Word after build (per Constraint §2).

### 7.3 Build script

Create `scripts/build-fixed-thesis-docx.py`. Pseudocode:

```python
# scripts/build-fixed-thesis-docx.py
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "documents" / "fixed-final-thesis-paper"
OUT  = SRC / "Adaptive-Learning-Platform-Final.docx"
REF  = SRC / "reference.docx"

ORDER = [
    "01-declaration-of-authorship.md",
    "02-acknowledgement.md",
    "04-abbreviations.md",
    "05-list-of-tables.md",
    "06-list-of-figures.md",
    "06b-list-of-listings.md",
    "07-abstract.md",
    "08-chapter-1-introduction.md",
    "09-chapter-2-literature-review.md",
    "10-chapter-3-system-design.md",
    "11-chapter-4-implementation.md",
    "12-chapter-5-pilot-evaluation.md",
    "13-chapter-6-conclusion.md",
    "14-references.md",
    "15-appendix-a.md",
    "16-appendix-b.md",
]

# 1. Concatenate with explicit page breaks between files
combined = SRC / "_combined.md"
with combined.open("w", encoding="utf-8") as f:
    for i, name in enumerate(ORDER):
        if i > 0:
            f.write("\n\n\\newpage\n\n")
        f.write((SRC / name).read_text(encoding="utf-8"))
        f.write("\n")

# 2. Run pandoc
subprocess.run([
    "pandoc", str(combined),
    "--from",  "markdown+pipe_tables+yaml_metadata_block+raw_tex+implicit_figures",
    "--to",    "docx",
    "--reference-doc", str(REF),
    "--resource-path", str(SRC),
    "--toc", "--toc-depth=3",
    "--number-sections",
    "--output", str(OUT),
], check=True)

print(f"✔ wrote {OUT}")
print(f"  word count (rough): run `pandoc {combined} --to plain | wc -w`")
```

Usage: `python scripts/build-fixed-thesis-docx.py`. Idempotent — overwrites `_combined.md` and the docx each run.

### 7.4 Manual polish in Word (after build)

These steps cannot be done by pandoc + reference.docx; the user performs them in Word once after the build.

1. **Add covers** (Decision 612 §2.1 + Comment #23 + HD spec mẫu 1 & 2):
   - **Trang bìa chính** (outer cover, Vietnamese): per HD spec at end of guideline — "BỘ GIÁO DỤC VÀ ĐÀO TẠO" (TNR 13), "TRƯỜNG ĐẠI HỌC HÀ NỘI" (TNR 13 bold), Hanoi University logo 2.5×2.5 cm, "KHÓA LUẬN TỐT NGHIỆP" (TNR 15 bold), VN title (TNR 16 bold), EN title (TNR 16 bold), supervisor / student / ID / specialization / faculty / "Hà Nội, 20.." (all TNR 14 bold lowercase).
   - **Trang bìa phụ** (inner cover, English): same layout in English — "MINISTRY OF EDUCATION AND TRAINING", "HANOI UNIVERSITY", EN title only, Supervisor/Student/Student ID/Specialization/Faculty/"Hanoi, 20..".
   - Both covers must NOT have page numbers. Use a section break (next page) after the inner cover.
2. **Set up two-zone page numbering** (Decision 612 §2.2.1, line 60):
   - **Front matter** (Declaration → Abstract): lowercase Roman `i, ii, iii, …`, bottom-center.
   - **Body** (Chapter 1 onwards through Appendices): Arabic `1, 2, 3, …`, bottom-center, **restart at 1 from Chapter 1**.
   - In Word: Layout → Breaks → Section Break (Next Page) at end of Abstract; in body footer Insert → Page Number → Format Page Numbers → "Start at 1"; in front-matter footer Format Page Numbers → "i, ii, iii".
3. **Insert Word-native Table of Contents**:
   - Delete pandoc's auto-TOC if present.
   - Position cursor between Acknowledgement and Abbreviations (per spec order: Declaration → Acknowledgement → **TABLE OF CONTENT** → Abbreviations → ...).
   - References → Table of Contents → Custom Table of Contents → 3 levels.
   - Right-click → Update Field whenever headings change.
4. **Update fields**: List of Tables, List of Figures → right-click → Update Field → Update entire table.
5. **Caption styles**: scan figure/table captions; if pandoc output left them as Normal, select and apply `Caption` style. Captions must read "Figure 1.1: …" / "Table 1.1: …" centered, italic, 12pt.
6. **Orphans/widows**: scan H1 page breaks — every chapter must start on its own page.
7. **References hanging indent**: select all references → Home → Paragraph → Special: Hanging by 1.27 cm.
8. **Append "Bản giải trình chỉnh sửa Khóa luận tốt nghiệp"** (HD spec line 28 — required as last document item):
   - Form provided by Faculty after defense; user fills based on advisor / committee feedback.
   - Inserted as final section after Appendix B with its own H1 title.
   - Not part of body word count.
9. **Verify Vietnamese diacritics** on the outer cover render correctly.

### 7.5 Verification

| Check | Command / Action | Pass criterion |
|---|---|---|
| **Decision 612 — page setup** | Layout → Margins → Custom | A4, T 3 / B 3 / L 3.5 / R 2 cm |
| **Decision 612 — body** | Click in body → Home | TNR 13 pt, justified, line 1.5 |
| **Decision 612 — H1** | Click chapter title → Home | TNR 16 pt bold, UPPERCASE, centered, page break before |
| **Decision 612 — H2** | Click "1.1" heading → Home | TNR 14 pt bold, justified, 6/6 |
| **Decision 612 — H3** | Click "1.1.1" heading → Home | TNR 13 pt **regular** (NOT bold), justified, 6/6 |
| **Decision 612 — H4** | Click "1.1.1.1" heading → Home | TNR 13 pt italic only (NOT bold), justified, 6/6 |
| **Decision 612 — page numbering** | Visual scan | Front matter: i, ii, iii (Roman lowercase); Body Ch1+: 1, 2, 3 (Arabic, restart) |
| **Decision 612 — footnote** | Click any footnote (if present) | TNR 10 pt |
| **Decision 612 — block quote** | Find any 40+ word direct quote | Indented 1.27 cm from left margin |
| **Tables — full page width** | Click any pipe-table in front matter / appendix | Spans margin-to-margin (15.5 cm); borders visible on all cells |
| **Tables — image PNG width** | Click any `table-*.png` figure | Width = 15.5 cm; aspect ratio preserved |
| **Heading colors** | Click any H1/H2/H3/H4 → Home → Font color | Black (Automatic), no blue accent |
| **Code blocks — font** | Click any code line in Ch4 → Home | Consolas 10 pt, all black, left-aligned |
| **Code blocks — frame** | Visual scan of all 9 listings | Single 0.5 pt black border on all 4 sides; gray #F5F5F5 fill; one continuous frame per block (no horizontal lines between code lines) |
| **Code blocks — indentation** | Inspect a multi-line block (e.g. Listing 1 BKT update) | 4-space Python indent visible on every nested line |
| **Code blocks — captions** | Above each block | "*Listing N. Title.*" italic, 12 pt; nine captions Listing 1–Listing 9 |
| **Inline code** | Find any `` `backticked` `` span in Ch3/Ch4/Ch5 | Consolas 11 pt black; no shading; baseline aligned with prose |
| **Decision 612 — doc structure** | Word Navigation pane order | Cover → Cover phụ → Declaration → Acknowledgement → TOC → Abbreviations → List of Tables → List of Figures → **List of Listings** → Abstract → Ch1–6 → References → Appendix → Bản giải trình |
| **List of Listings** | Front matter, after List of Figures | Table with 9 rows (Listing 1–9), each with title + page; user fills page numbers in Word |
| Body word count | `pandoc _combined.md --to plain \| wc -w` | ≤ 19,500 |
| Page count | Word status bar (after covers added) | ≤ 75 (excluding covers + Bản giải trình) |
| Comment satisfaction | Cross-read [COMMENT-ACTIONS.md](COMMENT-ACTIONS.md) | Every advisor comment has ✅ |
| All images embedded | After build: open .docx → check 33 images | 33 figures + tables-as-images |
| Heading hierarchy | Word Navigation pane (View → Navigation Pane) | H1 = chapters, H2/H3/H4 nest correctly (Comment #21) |
| Tense consistency | grep `will be` in body files (only Ch5 pilot allowed) | No false positives in Ch3/Ch4 (Comment #16) |
| Voice checklist | UNDERGRAD-VOICE-GUIDE.md §6 | Pass for every chapter |
| Final PDF preview | Word → File → Export → PDF | Visual scan, no glitches |

### 7.6 Fallback if pandoc styling drifts

Tried in this order:

1. **Adjust `reference.docx`** — most style fixes belong here, then re-run §7.3.
2. **Post-process with python-docx** — narrow fixes only (e.g., force margin overrides). Add to the build script as a final step.
3. **Last resort — Google Doc styling pass:** upload the docx to Google Drive as a Google Doc, run [scripts/gdoc-write-format-thesis.py](../../scripts/) against it, then File → Download → Microsoft Word (.docx). Only do this if §7.6 (1)+(2) cannot match Decision 612.

### 7.7 Versioning

Save successive builds as `Adaptive-Learning-Platform-Final-v{1,2,3}.docx`. The script overwrites the unversioned file on every run; once a version is approved, the user copies it to `…-vN.docx`. Final submission file: `…-vFINAL.docx`.

---

## 8. Acceptance criteria

The revision is **done** when:

1. Total body word count ≤ 19,500. ✅ Hard target.
2. Word doc visual page count ≤ 75 (with images, headers, etc.). ✅ Hard target.
3. Every advisor comment in [COMMENT-ACTIONS.md](COMMENT-ACTIONS.md) has its action box checked off, with the file + line where it was applied. ✅ Hard target.
4. Voice checklist (UNDERGRAD-VOICE-GUIDE.md §6) passes for all body chapters. ✅ Hard target.
5. Tense audit clean (system = present/past consistent, pilot = future). ✅ Hard target.
6. References list intact and consistent. ✅ Hard target.
7. Bilingual cover present. ✅ Hard target.
8. Final `.docx` opens cleanly in Word with no formatting glitches. ✅ Hard target.

---

## 8.1 Cross-chapter framing rule for Layer 5 (decided 2026-05-10)

User decision: **Layer 5 (LLM Socratic hints) is NOT a contribution.** It is exploratory engineering work, mentioned where relevant but never tracked as a thesis contribution.

Apply consistently in Phase 3:

| Where | How to frame Layer 5 |
|---|---|
| Ch1 §1.5.1 Architecture | "Layer 5: LLM Feedback (exploratory). Built to test feasibility; disabled in the pilot. Not part of the thesis's evaluated contribution." |
| Ch1 §1.7 Contributions | A trailing standalone paragraph after the 2 contributions: "A Layer 5 module was also built as exploratory work… disabled in the pilot to avoid confounding the evaluation of Layers 1–4. It is not a primary contribution." |
| Ch3 System design | List Layer 5 in the architecture overview, but mark "exploratory" and skip detailed design rationale. |
| Ch4 Implementation | Devote one short subsection (e.g., §4.6 LLM feedback layer) showing it was built. State explicitly: not contribution, exploratory. |
| Ch5 §5.2 Experimental design | One sentence: "Layer 5 is disabled in the pilot to avoid confounding RAG hint quality with the core adaptive logic." |
| Ch6 §6.4 Future work | "Evaluate Layer 5 (LLM hints) standalone — cost / hallucination / hint quality." |
| Figure 1.3 | **Already removed** from contribution boxes. Show only Contribution 1 and Contribution 2. |

Forbidden words for Layer 5: "optional contribution", "contribution 3", "main contribution". Use: "exploratory", "exploratory addition", "auxiliary module", "future work direction".

## 9. Risks & mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Voice transformation feels uneven across chapters | Med | Pilot Ch1 → user review → adjust voice guide before auto phase. Apply checklist to every chapter. |
| Cuts remove something the advisor wanted kept | Low | All comments mapped to actions in COMMENT-ACTIONS.md; nothing the advisor flagged "keep" is cut. |
| Section 3.1.3 (missing per Comment #21) — user must specify what it is | High | Listed as TODO; user will provide before Phase 2 ships Ch3. |
| Figure 1.1 missing (per Comment #20) — must locate or create | Med | Search image folder first; if absent, generate or annotate as TODO. |
| Word count overshoot during rewrite | Med | Each chapter is rewritten with explicit target; if over, second pass to cut. |
| Pandoc styling drift from Decision 612 | Low | Tune `reference.docx` first; python-docx post-process for narrow fixes; Google Docs styling pass as last-resort fallback (§7.6). |
| Pandoc image path resolution fails | Low | Build script passes `--resource-path` to the fixed-final-thesis-paper folder; markdown refs use relative `images/<file>.png`. Verify with `unzip -l` check in §7.5. |
| Markdown tables render as plain text | Low | Build script enables `pipe_tables` extension; pre-flight grep for any HTML `<table>` blocks (those need conversion to pipe-table form). |
| Vietnamese diacritics in cover render badly in Word | Low | Use Times New Roman (UTF-8 friendly); verify in Word before delivery. |

---

## 10. Code listing format (Phase 4.5 — decided 2026-05-10)

**Status:** APPROVED 2026-05-10 — implementation in progress.

### 10.1 Inventory

| Where | Count | Type |
|---|---:|---|
| [11-chapter-4-implementation.md](11-chapter-4-implementation.md) | 9 | fenced ```python``` (3–13 lines each) |
| Ch3, Ch4, Ch5 body | 55 | inline `` `code` `` spans |
| Ch1, Ch2, Ch6, front matter, appendices in build set | 0 | — |

Companion files (`appendix-a-companion-full-instruments.md` etc.) are out of scope; they are not in the docx build per §6.

### 10.2 Why pandoc default renders code wrong

Without a `Source Code` paragraph style and a `Verbatim Char` character style in the reference.docx, pandoc falls back to inheriting from `Normal`. That means:

- Code text comes out as Times New Roman 13 pt **justified** — the body style.
- Justified alignment expands inter-word spaces, which destroys code indentation.
- Tabs and runs of spaces collapse, so `for x in y:\n    print(x)` loses its 4-space indent.
- No frame, no shading — code blocks are visually indistinguishable from prose.

This is the "render sai" the user reported.

### 10.3 Style spec (LaTeX `listings` analog)

**Source Code** (paragraph style — applied by pandoc to each line of a fenced block):

| Property | Value | LaTeX `lstset` analog |
|---|---|---|
| Font family | Consolas (fallback Courier New) | `basicstyle=\ttfamily` |
| Font size | 10 pt | `basicstyle=\small` |
| Color | #000000 (auto/black) | mono color |
| Alignment | Left (NOT justified) | — |
| Line spacing | 1.0 (single) | — |
| First-line indent | 0 | — |
| Space before / after | 0 pt within block; 6 pt outer (set on first/last line only) | — |
| Border | single 0.5 pt #000000, top + left + right + bottom | `frame=single` |
| Internal padding (border distance) | 6 pt all sides | — |
| Background shading | #F5F5F5 light gray | `backgroundcolor=\color{gray!10}` |
| White-space preservation | yes (`<w:t xml:space="preserve">`) | always on in `listings` |
| Keep with next | yes (avoid breaking block across pages where possible) | — |

**Verbatim Char** (character style — applied by pandoc to inline `` `code` `` spans):

| Property | Value |
|---|---|
| Font family | Consolas (fallback Courier New) |
| Font size | 11 pt (slightly smaller than 13 pt body so it visually shrinks back without disrupting line height) |
| Color | #000000 |
| Background | none (must work mid-sentence; shading would break paragraph flow) |

### 10.4 Caption convention (proposed)

Each code block gets an italic caption ABOVE it, mirroring the figure/table caption convention. Format: `*Listing N. Brief description.*` — flat numbering across the whole thesis (decided 2026-05-10), NOT chapter-coupled. Same convention `\begin{lstlisting}[caption=...]` would auto-number across the document.

**9 captions for Chapter 4 (signed off 2026-05-10):**

| # | Block location | Function(s) | Caption |
|---:|---|---|---|
| 1 | [11-chapter-4-implementation.md:47–58](11-chapter-4-implementation.md#L47) | `bkt_update` | *Listing 1. BKT posterior update.* |
| 2 | [11-chapter-4-implementation.md:74–82](11-chapter-4-implementation.md#L74) | `expected_score`, `update_elo` | *Listing 2. Elo expected score and rating update.* |
| 3 | [11-chapter-4-implementation.md:88–99](11-chapter-4-implementation.md#L88) | `compute_dynamic_k` | *Listing 3. Dynamic K-factor for student ratings.* |
| 4 | [11-chapter-4-implementation.md:105–108](11-chapter-4-implementation.md#L105) | `compute_problem_k` | *Listing 4. Square-root K-factor decay for problem ratings.* |
| 5 | [11-chapter-4-implementation.md:122–127](11-chapter-4-implementation.md#L122) | `thompson_select` | *Listing 5. Thompson Sampling arm selection.* |
| 6 | [11-chapter-4-implementation.md:139–149](11-chapter-4-implementation.md#L139) | `compute_reward` | *Listing 6. MAB reward function (gain + difficulty match + efficiency).* |
| 7 | [11-chapter-4-implementation.md:166–175](11-chapter-4-implementation.md#L166) | `update` (MAB) | *Listing 7. Beta posterior update for MAB arms.* |
| 8 | [11-chapter-4-implementation.md:185–188](11-chapter-4-implementation.md#L185) | `retrievability` | *Listing 8. FSRS retrievability decay.* |
| 9 | [11-chapter-4-implementation.md:212–220](11-chapter-4-implementation.md#L212) | `submission_to_fsrs_rating` | *Listing 9. Submission-to-FSRS-rating mapping.* |

Decision 612 §I doesn't require a "List of Listings" — only List of Tables and List of Figures. **User explicitly requested LoL on 2026-05-10**, so [06b-list-of-listings.md](06b-list-of-listings.md) is now in the build (positioned after List of Figures, before Abstract).

### 10.5 Build pipeline changes

**A. [scripts/build-reference-docx.py](../../scripts/build-reference-docx.py)** — add two styles:

```python
# Source Code (paragraph) — Consolas 10pt, framed, shaded, single line
def configure_code_styles(doc):
    styles = doc.styles
    if "Source Code" not in [s.name for s in styles]:
        styles.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
    s = styles["Source Code"]
    s.base_style = styles["Normal"]
    f = s.font
    f.name = "Consolas"
    f.size = Pt(10)
    rpr = s.element.get_or_add_rPr()
    force_font(rpr, "Consolas")
    force_black(rpr)
    p = s.paragraph_format
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.line_spacing = 1.0
    p.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.first_line_indent = Cm(0)
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    p.keep_with_next = True
    # Border (top/bottom/left/right) + shading via XML
    ppr = s.element.get_or_add_pPr()
    add_paragraph_border(ppr, sz="4", color="000000")
    add_paragraph_shading(ppr, fill="F5F5F5")

# Verbatim Char (character) — Consolas 11pt, no shading
def configure_verbatim_char(doc):
    ...
```

The border is encoded as `<w:pBdr>` with all four edges; shading as `<w:shd w:fill="F5F5F5"/>`. Helpers `add_paragraph_border()` and `add_paragraph_shading()` are new.

**B. [scripts/build-fixed-thesis-docx.py](../../scripts/build-fixed-thesis-docx.py)** — pandoc args + post-process:

- Add `--no-highlight` to disable Pygments-style coloring (keeps code uncolored, all black, consistent with the grayscale-only rule from VISUAL-STYLE-GUIDE.md).
- Add `merge_code_block_borders()` post-process. Without merging, each line of a fenced block gets its own complete frame (top+bottom on every line) — looks like a stack of single-row boxes. The pass walks `Source Code` paragraphs and sets per-position borders:
  - First line: top + left + right (no bottom)
  - Middle lines: left + right only
  - Last line: bottom + left + right
- Plus a `space_before=6pt` on first line and `space_after=6pt` on last line of each block, restoring outer breathing room.

**C. [11-chapter-4-implementation.md](11-chapter-4-implementation.md)** — insert italic caption ABOVE each ```python``` fence per §11.4 table.

### 10.6 Acceptance criteria

The code-listing format is **done** when:

1. All 9 Ch4 blocks render as monospace Consolas 10pt, framed (single 0.5pt black border, gray #F5F5F5 fill), no syntax color. ✅ Hard target.
2. Indentation is preserved (4-space Python indent visible). ✅ Hard target.
3. Each block has an italic *Listing N.* caption above it (flat numbering, Listing 1–9). ✅ Hard target.
4. Each block stays on a single page where length permits (≤ ~25 lines). ✅ Soft target (longer blocks can break).
5. Inline `` `code` `` spans render Consolas 11pt, plain (no shading). ✅ Hard target.
6. No code block exceeds page width (15.5 cm). Long lines either wrap or are pre-shortened in markdown. ✅ Hard target.

### 10.7 Task checklist

- [x] User signs off on 9 listing captions (§10.4 table) — flat numbering Listing 1–9, decided 2026-05-10.
- [x] Add `Source Code` + `Verbatim Char` styles to `build-reference-docx.py` with `add_paragraph_border()` and `add_paragraph_shading()` helpers.
- [x] Regenerate `reference.docx` and verify the 2 new styles via the XML inspector.
- [x] Add `--no-highlight` to pandoc args in `build-fixed-thesis-docx.py`.
- [x] Add `merge_code_block_borders()` post-process pass in `build-fixed-thesis-docx.py`.
- [x] Insert 9 italic captions in `11-chapter-4-implementation.md`.
- [x] Pre-flight: scan Ch4 blocks for lines > 85 chars (no lines exceed 80 chars; safe).
- [x] Add `Source Code` and `Verbatim Char` rows to PLAN.md §7.1 spec table.
- [x] Add 5 verification rows to PLAN.md §7.5 (font, frame, indentation, captions, inline code).
- [ ] Run full build, open in Word, confirm acceptance criteria 1–6.

---

## 11. Blockers — all resolved (2026-05-10)

| # | Blocker | Resolution |
|---|---|---|
| 1 | Per-chapter targets sign-off | ✅ Approved. Posture: "real system thesis built by an undergrad", emphasize Ch3 + Ch4 |
| 2 | §3.1.3 missing — what topic? | ✅ Not missing. TOC heading-level bug. Action shifted to heading hierarchy audit during Ch3 rewrite |
| 3 | Direct-rewrite vs draft stage | ✅ Direct rewrite into markdown files; user reviews markdown |
| 4 | Conference one-liner (Comment #1) | ✅ Skipped — conference paper is done |

Plus user-handled out of scope: bilingual covers (Comment #23).

**Status:** ready to execute. Starting Ch1 pilot.
