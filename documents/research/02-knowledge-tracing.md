# Knowledge Tracing: State of the Art (2024-2026)

Knowledge Tracing (KT) is the backbone of any adaptive learning system. It answers: **"What does the student know right now?"**

---

## 1. DKT2 (xLSTM-based Deep Knowledge Tracing) — January 2025

**Paper:** "From Deep Knowledge Tracing to DKT2" — ECML-PKDD 2025

**What it is:** Next-generation knowledge tracing that replaces LSTM with xLSTM (Extended LSTM). Uses the Rasch model for input embeddings and Item Response Theory (IRT) for interpretable output decomposition, splitting learned knowledge into "familiar" and "unfamiliar" components.

**Why it's better:** Consistently outperforms 18 baseline models (including DKT, AKT, SAINT, SAKT) across three large-scale datasets in one-step, multi-step, and varying-history-length predictions.

**Key innovation:** xLSTM introduces:
- sLSTM: exponential activation for better storage decisions
- mLSTM: matrix memory for increased storage capacity with full parallelization

**Application to our system:** Track which programming concepts (loops, recursion, DP, etc.) a student has mastered. The IRT-based output decomposes mastery into "concepts the student is comfortable with" vs "concepts they struggle with."

**Implementation:** Open-source at https://github.com/zyy-2001/DKT2

**References:**
- arXiv: https://arxiv.org/abs/2501.14256
- ECML-PKDD 2025: https://link.springer.com/chapter/10.1007/978-3-032-06109-6_14

---

## 2. srcML-DKT (Code-Specific Knowledge Tracing) — EDM 2025

**Paper:** "srcML-DKT" — Educational Data Mining 2025

**What it is:** Extension of Code-DKT using srcML-based code representations instead of AST-based. Specifically designed for programming education, extracting features directly from student-submitted code — including code that fails to compile.

**Why it's better:** Code-DKT relied on ASTs, which only work for parsable code. In introductory programming, many submissions are unparsable. srcML represents even uncompilable code in XML format. Tested on N=610 students.

**Application to our system:** Directly applicable — trace knowledge by analyzing the actual code students write, not just right/wrong answers. Can identify specific syntactic and semantic patterns to understand what concepts students struggle with.

**References:**
- EDM 2025: https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.short-papers.83/index.html
- PDF: https://learninganalytics.upenn.edu/ryanbaker/EDM2025-srcml-DKT-proceedings-v01.pdf

---

## 3. UKT (Uncertainty-aware Knowledge Tracing) — AAAI 2025

**Paper:** "UKT" — AAAI 2025

**What it is:** Represents student knowledge states as **probability distributions** rather than point estimates. Uses Wasserstein self-attention for learning state transitions and uncertainty-aware contrastive learning.

**Why it's better:** Traditional KT gives a single confidence score. UKT captures uncertainty — "70% confident with HIGH uncertainty" is very different from "70% confident with LOW uncertainty." This directly impacts recommendation quality:
- High uncertainty → recommend **diagnostic** problems to determine true mastery
- Low uncertainty + high mastery → advance to harder topics
- Low uncertainty + low mastery → targeted practice

**Application to our system:** Use uncertainty to decide between diagnostic vs advancement problems. When we're not sure if a student knows "graphs", give them a diagnostic graph problem first.

**References:**
- arXiv: https://arxiv.org/abs/2501.05415
- AAAI 2025: https://ojs.aaai.org/index.php/AAAI/article/view/35007

---

## 4. LefoKT (Learning and Forgetting Knowledge Tracing) — 2025

**What it is:** Decouples forgetting patterns from problem relevance via "relative forgetting attention." Specifically designed to model diverse forgetting behaviors in ever-growing interaction sequences.

**Why it's better:** Previous attention-based KT models conflated "which problems are related" with "how quickly knowledge decays." LefoKT separates these, giving better length extrapolation — critical for tracking learning over a full semester.

**Application to our system:** Combine with spaced repetition. If a student learned binary search 3 weeks ago but hasn't practiced, LefoKT can estimate how much they've forgotten.

**References:**
- pyKT: https://pykt.org/lefokt

---

## 5. HCGKT (Hierarchical Contrastive Graph Knowledge Tracing) — 2025

**What it is:** Integrates hierarchical graph filtering attention with adversarial contrastive learning and GCN to model educational data relationships.

**Why it's better:** Captures hierarchical relationships between knowledge concepts natively through graph structure (e.g., "loops" → "recursion" → "dynamic programming").

**Application to our system:** Model the prerequisite graph of programming concepts, then use HCGKT to trace knowledge while respecting the hierarchical nature of programming knowledge.

**References:**
- Springer: https://link.springer.com/chapter/10.1007/978-3-031-98420-4_20

---

## Implementation Toolkits

| Toolkit | URL | Description |
|---------|-----|-------------|
| pyKT | https://github.com/pykt-team/pykt-toolkit | PyTorch, 10+ DLKT models, standardized preprocessing |
| pyBKT | https://github.com/CAHLR/pyBKT | Bayesian KT, scikit-learn API, C++ acceleration |
