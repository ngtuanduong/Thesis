# Brainstorm: Novel Contributions

**Thesis:** Adaptive Learning Platform for University Programming Courses

---

## 1. What Makes This Thesis Unique

### 1.1 The Integration Gap

The fundamental novelty of this thesis is **not** any single algorithm — each algorithm (BKT, Elo, MAB, FSRS) exists in published literature. The novelty is the **integration of all five into a unified adaptive pipeline for programming education.**

No existing system — academic or commercial — does this:

```
Existing systems:          This thesis:

BKT alone ──── Academic      BKT ─────┐
Elo alone ──── Codeforces    Elo ─────┤
MAB alone ──── Academic      MAB ─────┼──► Integrated Pipeline
FSRS alone ─── Anki          FSRS ────┤      for Programming
LLM alone ──── ChatGPT       LLM ─────┘
```

The integration creates emergent value:
- BKT **feeds** MAB (mastery determines which concepts to explore)
- Elo **constrains** MAB (ZPD limits problem selection)
- FSRS **interrupts** MAB (review queue takes priority over exploration)
- LLM is **grounded** by KG + BKT (hints are personalized to knowledge state)

No individual technique achieves this on its own.

### 1.2 Why This Matters

In the literature, each technique is typically evaluated in isolation:
- "We applied BKT and achieved AUC=0.7" (but no recommendation system)
- "We used Elo for programming exercises" (but no knowledge tracing)
- "We used MAB for problem selection" (but assumed fixed difficulty)

The real educational challenge requires **all components working together**. A student needs:
1. A model of what they know (BKT)
2. Problems at the right difficulty (Elo)
3. The right concept at the right time (MAB)
4. Review before they forget (FSRS)
5. Help when they're stuck (LLM)

This thesis is the first to build and evaluate the complete pipeline.

---

## 2. Comparison with Existing Platforms

### 2.1 LeetCode

| Aspect | LeetCode | This Thesis |
|--------|----------|-------------|
| Problem selection | Manual (user browses by topic/difficulty) | Adaptive (MAB selects optimal problem) |
| Difficulty | Static labels (Easy/Medium/Hard) | Dynamic Elo calibrated from submissions |
| Knowledge model | None | BKT per concept |
| Spaced repetition | None | FSRS schedules reviews |
| Hints | LLM hints (paid feature) | RAG+LLM grounded in knowledge state |
| Target audience | Self-directed competitive programmers | University students in courses |

**LeetCode's gap:** No adaptation. Students must self-assess their level and choose problems. There is no mechanism to prevent a student from attempting DP problems before mastering recursion.

### 2.2 HackerRank

| Aspect | HackerRank | This Thesis |
|--------|------------|-------------|
| Problem selection | Curated tracks or manual | Adaptive pipeline |
| Difficulty | Static badges | Dynamic Elo |
| Knowledge model | Skill badges (binary: attempted/not) | BKT (probabilistic mastery) |
| Review | None | FSRS |
| Assessment | Fixed skill tests | BKT + Elo combined prediction |

**HackerRank's gap:** Skill assessment is binary (you either solved the problem or didn't). No probabilistic knowledge model, no difficulty calibration, no spaced repetition.

### 2.3 Codeforces

| Aspect | Codeforces | This Thesis |
|--------|------------|-------------|
| Elo system | Yes (for competitive rating) | Yes (for learning optimization) |
| Purpose of Elo | Ranking/matchmaking | ZPD-based problem selection |
| Knowledge model | None | BKT |
| Problem recommendation | Tag-based browsing | MAB + Elo + BKT combined |
| Review | None | FSRS |

**Codeforces' gap:** Uses Elo for competition ranking, not for pedagogical recommendation. No knowledge tracing, no concept prerequisites, no spaced repetition. Designed for competitive programmers, not learners.

### 2.4 Duolingo (Cross-Domain Comparison)

| Aspect | Duolingo | This Thesis |
|--------|----------|-------------|
| Domain | Language learning | Programming |
| Spaced repetition | Yes (now uses FSRS) | Yes (FSRS) |
| Knowledge model | Implicit (in model) | Explicit (BKT) |
| Difficulty calibration | Adaptive | Elo-based |
| Problem selection | Internal algorithm | Hierarchical MAB |
| Unique to us | — | Code execution, rich submission signals |

**Duolingo's relevance:** Closest existing platform in terms of adaptive sophistication, but for a completely different domain. Programming has unique properties (code artifacts, compilation errors, multiple solution paths) that Duolingo's language-learning algorithms don't address.

### 2.5 ALEKS (Cross-Domain Comparison)

| Aspect | ALEKS | This Thesis |
|--------|-------|-------------|
| Domain | Mathematics | Programming |
| Knowledge model | Knowledge Spaces Theory | BKT (more granular) |
| Difficulty | Assessment-based | Elo (continuous) |
| Problem selection | Next in knowledge space | MAB (optimized for learning gain) |
| Review | Yes (periodic reassessment) | FSRS (scheduled per concept) |

**ALEKS's relevance:** Most academically rigorous adaptive platform, but uses Knowledge Spaces Theory which requires complete prerequisite graphs and binary mastery assessments. BKT + Elo provides a more nuanced model.

---

## 3. Novel Contribution Candidates

### Contribution 1: Integrated Multi-Layer Adaptive Architecture

**Claim:** First system to integrate Knowledge Tracing + Elo Difficulty Calibration + Hierarchical MAB + FSRS Spaced Repetition into a single adaptive pipeline for programming education.

**Novelty argument:**
- No published system combines all 5 components
- The architecture specifies exactly how layers communicate (data flow, constraints)
- The modular design allows each layer to be independently upgraded
- Evaluated as an end-to-end system, not individual components

**Strength of claim:** STRONG. Easy to verify by literature search — no such system exists.

### Contribution 2: Dynamic K-Value Elo for Programming Exercises

**Claim:** Application of trend-aware dynamic K-value Elo to calibrate programming exercise difficulty.

**Novelty argument:**
- Dynamic K-value Elo exists in the literature (Springer 2025) but for general education
- Elo for programming exists (ACM TOCE) but with fixed K
- Combining dynamic K with programming-specific features is new
- The dual Elo system (student + problem ratings) with programming-specific initialization is a modest extension

**Strength of claim:** WEAK. This is essentially applying an existing technique to a new domain without fundamental modification. The dynamic K-value mechanism is unchanged from the Springer 2025 formulation; only the domain (programming exercises instead of general education) is new. **Do not oversell this contribution.** Instead, position it as a necessary engineering component of the integrated architecture, not as a standalone research contribution.

**Marketing strategy:** Fold this into Contribution 1 (the integration) rather than claiming it as a separate novel contribution. The Elo component's value comes from its role in the pipeline (feeding ZPD constraints to MAB), not from the algorithm itself.

### Contribution 3: Prerequisite-Constrained Hierarchical MAB

**Claim:** Hierarchical MAB for problem selection that respects knowledge graph prerequisites, where concept eligibility is gated by BKT mastery states.

**Novelty argument:**
- Hierarchical MAB for education exists in literature
- Knowledge graph prerequisites for learning exist in literature
- Using BKT mastery as the gate criterion for MAB concept selection is new
- The specific reward function combining learning gain + difficulty match + efficiency is new

**Strength of claim:** MODERATE. Novel combination of known techniques.

### Contribution 4: FSRS for Programming Skill Retention

**Claim:** First application of the FSRS (Free Spaced Repetition Scheduler) algorithm to programming concept review scheduling.

**Novelty argument:**
- FSRS is designed for flashcard-based learning (vocabulary, facts)
- No published work applies FSRS to programming skills
- The key innovation: "reviewing a concept" = solving a problem from that concept (not recalling a fact)
- The rating mapping from submission outcomes to FSRS ratings (1–4) is entirely new

**Strength of claim:** STRONG. Clearly novel application domain for FSRS.

### Contribution 5: Open-Source Adaptive Platform

**Claim:** Open-source, deployable adaptive learning platform for programming education, designed for Vietnamese university context.

**Novelty argument:**
- Most adaptive education research produces papers, not deployable systems
- The system is designed for real classroom use, not just experimentation
- Vietnamese university context: curriculum-aligned, appropriate for local teaching practices
- Full stack: frontend + backend + AI service + code execution sandbox

**Strength of claim:** MODERATE. Open-source educational platforms exist, but few with this level of adaptive sophistication.

---

## 4. Why the Multi-Layer Integration is New

### 4.1 Literature Evidence

Searching for systems that combine these techniques:

| Paper/System | BKT | Elo | MAB | FSRS | LLM | Year |
|--------------|:---:|:---:|:---:|:----:|:---:|:----:|
| Corbett & Anderson | ✓ | ✗ | ✗ | ✗ | ✗ | 1994 |
| Pelánek (Elo for education) | ✗ | ✓ | ✗ | ✗ | ✗ | 2016 |
| Clement et al. (MAB for education) | ✗ | ✗ | ✓ | ✗ | ✗ | 2015 |
| Ye (FSRS) | ✗ | ✗ | ✗ | ✓ | ✗ | 2023 |
| PyTutor (LLM ITS) | ✗ | ✗ | ✗ | ✗ | ✓ | 2024 |
| Chen et al. (KG+RAG+LLM) | ✗ | ✗ | ✗ | ✗ | ✓ | 2025 |
| DKT2 | ✓ | ~IRT | ✗ | ✗ | ✗ | 2025 |
| **This thesis** | **✓** | **✓** | **✓** | **✓** | **✓** | **2026** |

**No published work combines all five.** The closest are:
- Systems with BKT + IRT (similar to Elo), but no MAB, FSRS, or LLM
- Systems with MAB + difficulty model, but no KT or spaced repetition

### 4.2 Why Nobody Has Done This Before

1. **Complexity:** Building 5 integrated systems is significantly more work than building 1
2. **Evaluation challenge:** Hard to attribute learning gains to specific layers (need ablation studies)
3. **Data requirements:** Each layer needs interaction data; together they need more data
4. **Disciplinary boundaries:** BKT comes from education, MAB from statistics, FSRS from memory science, LLM from NLP — integration requires cross-disciplinary knowledge
5. **Engineering effort:** Production-quality implementation of all 5 layers is a substantial software project
6. **Uncertain marginal benefit:** It is not yet empirically established that combining all 5 layers produces significantly better outcomes than simpler 2–3 layer systems. Researchers may reasonably ask: "Does adding FSRS on top of BKT+Elo+MAB justify the added complexity?" The answer is an empirical question that this thesis aims to address through ablation analysis.

This thesis bridges these gaps by being both a research contribution and a software engineering project.

### 4.3 Justifying Each Layer's Marginal Benefit

Anticipated reviewer question: *"Does each additional layer provide sufficient marginal benefit to justify its complexity?"*

**Prepared response:**

| Layer Added | What It Enables | What Breaks Without It | Marginal Complexity |
|-------------|----------------|----------------------|-------------------|
| BKT (Layer 1) | Prerequisite gating, mastery estimation | MAB recommends advanced concepts to beginners; no concept mastery tracking | Low (O(1) HMM update) |
| Elo (Layer 2) | ZPD difficulty matching | MAB recommends too-easy or too-hard problems; no calibration | Low (simple arithmetic) |
| MAB (Layer 3) | Exploration-exploitation balance | System always exploits known-good concepts; never discovers new strengths | Low (Beta sampling) |
| FSRS (Layer 4) | Forgetting prevention | Mastered concepts decay without review; long-term retention degraded | Medium (FSRS state machine) |
| LLM (Layer 5) | Natural language hints | Student stuck with no help; higher abandonment | High (API cost, prompt engineering) |

**Key argument:** Layers 1–3 are **foundational** — removing any one fundamentally breaks the recommendation quality. Layer 4 addresses a **distinct learning science concern** (forgetting) not addressed by Layers 1–3. Layer 5 is **supplementary** and the thesis stands without it.

**Empirical validation plan:** The within-system ablation study (see 07-EVALUATION-PLAN.md §9) will provide evidence for each layer's contribution by replaying interaction logs with layers disabled.

---

## 5. Publication Potential

### 5.1 Target Venues

| Venue | Type | Fit | Contribution to Highlight |
|-------|------|-----|---------------------------|
| **EDM** (Educational Data Mining) | Conference | Excellent | Multi-layer adaptive architecture + BKT/Elo evaluation |
| **LAK** (Learning Analytics & Knowledge) | Conference | Excellent | Learning analytics pipeline + evaluation results |
| **AIED** (AI in Education) | Conference | Good | LLM integration + knowledge graph |
| **ACM TOCE** (Transactions on Computing Education) | Journal | Good | Programming-specific adaptive system |
| **UMAP** (User Modeling, Adaptation, Personalization) | Conference | Good | Multi-layer user modeling |
| **IEEE TLT** (Transactions on Learning Technologies) | Journal | Good | Full system + evaluation |

### 5.2 Paper Ideas

**Paper 1 (Systems paper):**
*"An Integrated Multi-Layer Adaptive Engine for Programming Education: Combining Knowledge Tracing, Elo Calibration, Multi-Armed Bandits, and Spaced Repetition"*
- Target: EDM or LAK
- Focus: Architecture, data flow, layer interactions
- Results: End-to-end evaluation (NLG, prediction accuracy, engagement)

**Paper 2 (Application paper):**
*"Applying FSRS Spaced Repetition to Programming Skill Retention"*
- Target: AIED or L@S
- Focus: FSRS adaptation for programming, rating mapping, retention experiment
- Results: Retention test comparison, FSRS scheduling accuracy

**Paper 3 (Evaluation paper):**
*"Does Multi-Layer Adaptation Outperform Single-Layer? An Ablation Study in Programming Education"*
- Target: EDM or LAK
- Focus: Ablation results showing each layer's marginal contribution
- Requires: Ablation study (see Evaluation Plan §9)

### 5.3 What Reviewers Will Ask

**Likely reviewer questions and how to address them:**

1. *"How do you know the improvement isn't just from having more problems?"*
   → Control group has access to the same problems; only the selection mechanism differs.

2. *"Isn't this just engineering? Where's the research contribution?"*
   → The integration itself is the contribution — plus novel applications (FSRS for programming, dynamic K for code exercises). Evaluation demonstrates that integration > individual components.

3. *"How do you handle the cold start problem?"*
   → Defined cold start strategy with sensible defaults (§3.3.3 of Architecture). Elo and BKT converge within ~20 interactions.

4. *"What about scalability? Can this handle 10,000 students?"*
   → Each layer is O(1) per update. The pipeline is inherently per-student. Redis caching handles repeated reads. Full load testing results would strengthen the paper.

5. *"Why BKT instead of DKT2?"*
   → BKT is interpretable (prerequisite checking requires explicit mastery probabilities), lower data requirements, and provides a strong baseline. DKT2 is discussed as future work.

---

## 6. Differentiation Summary

**In one paragraph:**

This thesis presents the first integrated adaptive learning platform for programming education that combines Bayesian Knowledge Tracing for concept mastery modeling, Dynamic K-Value Elo for difficulty calibration, Hierarchical Multi-Armed Bandits for intelligent problem selection, FSRS for spaced repetition scheduling, and LLM-powered Socratic hints — all unified through a knowledge graph of programming concepts. Unlike existing platforms (LeetCode, HackerRank, Codeforces) that offer no adaptation or single-technique adaptation, our system orchestrates five complementary layers where each compensates for the others' limitations: BKT tells us what the student knows, Elo tells us how hard each problem is for them, MAB optimally explores the concept space, FSRS prevents forgetting, and LLM provides grounded pedagogical feedback. Evaluated through a controlled experiment with university students, we demonstrate that the integrated approach produces significantly higher learning gains than content-based filtering alone.
