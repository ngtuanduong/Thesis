# Undergraduate Thesis Voice Guide

**Purpose.** Rewrite academic prose in the voice of a final-year (4th-year)
undergraduate student who built a working system, knows it well, and can
explain it clearly. Keep technical accuracy. Lose the professorial tone.

This guide is the source of truth for every rewrite in
`documents/fixed-final-thesis-paper/`. Apply it consistently.

---

## 1. Voice positioning

| Trait | Yes | No |
|---|---|---|
| Confidence | "I built X. It works because Y." | "It is humbly proposed that X may potentially work." |
| Sentence length | 12–22 words on average | 35+ words with 4 subordinate clauses |
| Vocabulary | Precise technical terms when needed; plain English otherwise | Latinate jargon stack (e.g., "instantiate the methodology") |
| Posture | Engineer explaining the build | Professor surveying the literature |
| Hedging | One hedge per claim, max | Stacked hedges ("might possibly perhaps suggest that") |
| Authority | "Studies show…", "I observed…", "BKT cannot model X" | "It would not be unreasonable to suppose…" |

The student knows the system, so writes about it directly. The student is also
honest about what is built vs. what is planned (per Comment #14 + #18).

---

## 2. Concrete rules

### 2.1 Sentence length
- **Target average: 18 words.** **Hard cap: 30 words.**
- If a sentence has 3+ commas or 2+ subordinate clauses, split it.
- One idea per sentence. Don't bundle a definition + a justification + a
  contrast into one breath.

### 2.2 Active voice (default), passive (when natural)
- "I designed the knowledge graph" > "The knowledge graph was designed"
- BUT: "BKT was introduced by Corbett and Anderson in 1995" — passive is
  fine when the agent is named or doesn't matter.
- Use "this thesis" or "the platform" as subjects when "I" feels off.

### 2.3 Prefer English to Latin
- "i.e." → "that is"
- "e.g." → "for example"
- "et al." → keep (it's standard in citations)
- "vs." → "versus" or rewrite
- "viz." → just delete it
- "cf." → "see" or "compare with"

### 2.4 Cut deadweight phrases
| Cut | Replacement |
|---|---|
| It is well-known that X | "X" or "Studies show X [N]" |
| It should be noted that X | "X" |
| It is worth mentioning that X | "X" |
| In order to | "To" |
| Due to the fact that | "Because" |
| A large number of | "Many" |
| At this point in time | "Now" / "Today" |
| In the event that | "If" |
| Has the ability to | "Can" |
| Make a decision | "Decide" |
| The vast majority of | "Most" |

### 2.5 Connectives
- Prefer: "Also,", "But,", "So,", "Then,", "Here,", "However,"
- Avoid (overused academic): "Moreover,", "Furthermore,", "Indeed,", "Notably,", "Henceforth,"
- Don't start a paragraph with "Furthermore." Start with the actual point.

### 2.6 Topic sentences
- First sentence of each paragraph **states the point**. Not a setup.
- Reader should understand the paragraph from the first line alone.

**Bad:**
> The literature on knowledge tracing has evolved significantly over the past
> three decades, with various approaches being proposed and refined to address
> the challenges of modeling student knowledge states accurately.

**Good:**
> Knowledge tracing models predict whether a student has learned a concept.
> The two main approaches are BKT (probabilistic) and DKT (neural).

### 2.7 Citations
- Keep `[N]` numbered citation style (already used in this thesis).
- Don't restate the cited claim; cite once and move on.
- For decisions justified by literature, say "I chose X because [N] showed Y" —
  not "It has been demonstrated by various authors that [1], [2], [3]…"

### 2.8 Tense — be consistent (per Comment #16)
The system **is implemented and deployed**. Use:
- **Past simple** for what was built/done: "I designed the layer", "I trained the model".
- **Present simple** for what the system currently does: "The MAB selects a problem", "BKT updates mastery".
- **Past for the pilot evaluation, future for unrun work, BUT**:
  - The pilot is **specified, not yet run**. So: "The pilot will compare X and Y"
    is correct. Don't write "the pilot showed" — it didn't yet.
- **Don't mix in one paragraph.** If a paragraph is about the system, present.
  If about the build, past. If about the pilot, future (or "is designed to").

### 2.9 "Relevance to this thesis" closing (per Comment #10 reply)
Every literature review subsection (in Ch2) ends with **one short paragraph
labeled "Relevance to this thesis"**. Format:

> **Relevance to this thesis.** I chose <approach> because <one reason
> grounded in the discussion above>. <One sentence on what it does in the
> system> .

This is what the advisor said is "phần có giá trị nhất của literature review".

### 2.10 Justify hyperparameters as design choices (per Comments #6, #7, #8)
For every hyperparameter, add **one sentence** explaining:
- It is a heuristic / design choice / informed by literature.
- It is **not** empirically optimized on this dataset.
- Sensitivity will be evaluated in the pilot (where applicable).

Example:
> The base K-factor is set to K_base = 25, a heuristic midpoint chosen for
> moderate rating volatility in education. It was not tuned on this dataset.
> Sensitivity to K will be tested in the pilot (Section 5.4).

---

## 3. Length-cutting rules

When a sentence/paragraph can be cut without losing meaning, cut it.
Specifically:

### 3.1 Definitional restatement
If a term was just defined, don't redefine. The second mention of "Bayesian
Knowledge Tracing (BKT)" is just "BKT".

### 3.2 Background that doesn't drive a decision
Per advisor: "bỏ bớt benchmark chi tiết không phục vụ trực tiếp cho quyết
định thiết kế". If a paragraph reviews benchmark numbers but doesn't lead
to a decision in this thesis, **delete it**.

### 3.3 Three-example lists
"X has been used in domains such as A, B, C, D, E, F, and G [refs]." → cut
to 2 most relevant: "X has been used in domains such as A and B [refs]."

### 3.4 Mirror sentences
"X is important because Y. As such, the importance of X is reflected in Y."
→ keep one.

### 3.5 Procedural narration
"In this section, we will discuss A, then B, then C, before concluding with D."
→ cut entirely. The headings show structure.

### 3.6 Phrase-level cuts
| 30+ words | <20 words |
|---|---|
| "The learning gain component, which carries a weight of 0.5 within the overall reward function and measures the change in BKT mastery before and after the attempt, captures the primary optimization objective." | "Learning gain (weight 0.5) measures the BKT mastery change before and after the attempt. It is the main optimization signal." |

---

## 4. Before / after exemplars (apply to actual chapters)

### 4.1 Chapter 1 paragraph (current vs. target)

**Original (66 words, professor voice):**
> Adaptive learning, the ability to tailor the content, pace, and methodology
> of the instruction to the unique characteristics of the learner or the
> performance of the learner, has shown considerable promise with respect to
> effectiveness across a variety of different educational domains [6], [7].
> The idea behind adaptive learning is the fundamental premise that the
> effectiveness of the learning can be significantly enhanced by matching the
> content of the instruction to the state of knowledge of the learner or the
> ability of the learner.

**Target (38 words, undergrad voice):**
> Adaptive learning adapts content, pace, and method to each student's
> current knowledge. Studies across many domains show it works [6], [7].
> The core idea is simple: students learn faster when material matches what
> they already know.

**Cut: 42% length. Same point, no loss.**

### 4.2 Chapter 2 paragraph (literature review)

**Original (54 words):**
> It is well-established in the literature [16] that Bayesian Knowledge
> Tracing represents a probabilistic framework wherein student knowledge is
> modeled as a hidden state that evolves over time, with the model parameters
> being learned from observation sequences in a manner that has been shown to
> be both interpretable and effective.

**Target (24 words):**
> Bayesian Knowledge Tracing (BKT) [16] models student knowledge as a hidden
> probability that grows with practice. It is interpretable and well-tested.

**Plus the closing per §2.9:**
> **Relevance to this thesis.** I chose BKT over DKT because the platform
> needs interpretable mastery values to drive the recommendation layer
> (Section 3.3.4). DKT's higher predictive accuracy [32] is not worth the
> opacity for this use case.

### 4.3 Hyperparameter justification (per §2.10)

**Original:**
> The mastery threshold of 0.85 was selected based on standard practice in
> BKT implementations, where mastery at or above 0.80 to 0.90 is recommended
> for prerequisite gating [16]. Setting the threshold at 0.95 would require
> excessive practice on already-understood concepts, while 0.70 risks
> advancing students prematurely.

**Target (advisor-aligned per Comment #8):**
> The mastery threshold is 0.85, the midpoint of the 0.80–0.90 range
> recommended in [16]. This is a design choice from the literature, not
> empirically optimized on this dataset; the pilot will test sensitivity in
> the 0.80–0.90 band (Section 5.4).

---

## 5. Things to **never** do

- **Don't translate sentence-by-sentence.** Read the paragraph, write the
  point, then write a clean version. Translating sentence-by-sentence keeps
  the original sentence rhythm.
- **Don't introduce new claims.** If the original paragraph cites [N] for a
  claim, the new version cites [N] for the same claim. No new facts.
- **Don't drop figures or tables silently.** If a figure is referenced in
  the text, the figure must appear in the rewrite (with the same number,
  e.g., Figure 1.3). If a figure is unused, mark it for review.
- **Don't drop citations.** Every `[N]` in the original maps to a `[N]` in
  the rewrite. Reference numbering stays the same.
- **Don't change figure numbering.** "Figure 3.1" stays "Figure 3.1".
  Even if the rewrite drops Section 3.1.4, Figure 3.5 keeps its number.
  (Why: keeps lists of figures stable; saves cross-reference work.)

---

## 6. Quick checklist before submitting a rewritten section

- [ ] Every sentence ≤ 30 words?
- [ ] Average sentence ≤ 22 words?
- [ ] No "It is well-known/worth-noting/should-be-noted that"?
- [ ] No "Furthermore" / "Moreover" / "Indeed" at sentence start?
- [ ] Topic sentence first in every paragraph?
- [ ] If lit review subsection: ends with **Relevance to this thesis** paragraph?
- [ ] If hyperparameter mentioned: design-choice + not-tuned-here disclaimer?
- [ ] Tense consistent (system = present, build = past, pilot = future)?
- [ ] All citations preserved?
- [ ] All figures/tables referenced and numbered consistently?
- [ ] Word count meets per-chapter target (see PLAN.md)?
