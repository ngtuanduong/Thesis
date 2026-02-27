# Proposed Architecture: Multi-Layer Adaptive Recommendation System

## The Problem with Current System

The current system uses basic **content-based filtering with cosine similarity** — the same technique used for product recommendations ("users who bought X also bought Y"). It has zero pedagogical intelligence: no knowledge tracing, no difficulty calibration, no forgetting model, no prerequisite awareness.

## Proposed: 5-Layer Adaptive Architecture

Each layer addresses a different pedagogical need. The combination is novel and publishable.

```
+------------------------------------------------------------------+
|  Layer 5: LLM Feedback (Optional Enhancement)                    |
|  KG + RAG + LLM for hints, explanations, code feedback           |
+------------------------------------------------------------------+
|  Layer 4: Review Scheduling (FSRS)                                |
|  When should the student review a previously learned concept?     |
+------------------------------------------------------------------+
|  Layer 3: Problem Selection (Hierarchical MAB)                    |
|  Which concept + which difficulty to recommend next?              |
+------------------------------------------------------------------+
|  Layer 2: Difficulty Calibration (Dynamic K-Value Elo)            |
|  How skilled is the student? How hard is each problem?            |
+------------------------------------------------------------------+
|  Layer 1: Knowledge Tracing (BKT or DKT2)                        |
|  What does the student know right now per concept?                |
+------------------------------------------------------------------+
|  Foundation: Knowledge Graph of Programming Concepts              |
|  Prerequisite relationships between concepts                      |
+------------------------------------------------------------------+
```

---

## Layer 1: Knowledge Tracing — "What does the student know?"

**Technique:** Bayesian Knowledge Tracing (BKT) via pyBKT, or DKT2 for more novelty

**What it does:**
- Tracks per-concept mastery probability (e.g., P(knows arrays) = 0.85, P(knows DP) = 0.30)
- Updates after every submission (correct/incorrect)
- Models learning rate per concept per student

**Why better than current:**
- Current: binary (solved or not), weighted only by difficulty
- Proposed: probabilistic mastery estimate per concept, updated continuously

**Implementation:** pyBKT (simple, interpretable) or DKT2 (state-of-the-art, more complex)

---

## Layer 2: Difficulty Calibration — "How hard is each problem for this student?"

**Technique:** Dynamic K-Value Elo Rating

**What it does:**
- Maintains Elo rating per student per concept dimension (Multidimensional Elo)
- Maintains Elo rating per problem
- K-value adapts: increases when student is rapidly learning, decreases when stable
- Directly operationalizes Zone of Proximal Development: recommend problems +100 to +300 Elo above student

**Why better than current:**
- Current: no difficulty model at all, just EASY/MEDIUM/HARD labels
- Proposed: continuous, personalized difficulty estimation that adapts to learning speed

---

## Layer 3: Problem Selection — "Which problem should we show next?"

**Technique:** Hierarchical Multi-Armed Bandit

**What it does:**
- Level 1 (concept arm): Selects which concept to practice, balancing:
  - Concepts with low mastery (exploitation)
  - New concepts the student hasn't tried (exploration)
  - Prerequisite ordering from knowledge graph
- Level 2 (difficulty arm): Within the chosen concept, selects difficulty:
  - Uses Elo-based ZPD targeting
  - Considers mastery trend (improving → harder, struggling → easier)

**Why better than current:**
- Current: cosine similarity returns "most similar" problems (echo chamber effect)
- Proposed: intelligent exploration-exploitation with prerequisite awareness

---

## Layer 4: Review Scheduling — "When should the student review?"

**Technique:** FSRS (Free Spaced Repetition Scheduler)

**What it does:**
- After mastering a concept, schedules review problems at optimal intervals
- Models per-student, per-concept forgetting curves
- Integrates with Layer 3: MAB arm selection considers both "new learning" and "review needed"

**Why better than current:**
- Current: no review mechanism at all. Once solved, a concept is "done forever"
- Proposed: scientifically-optimal review scheduling, 20-30% more efficient than SM-2

---

## Layer 5: LLM Feedback (Enhancement)

**Technique:** Knowledge Graph + RAG + LLM

**What it does:**
- When student is stuck, provides scaffolded hints (not direct answers)
- Analyzes submitted code to identify specific misconceptions
- Generates personalized explanations based on student's history
- Hint specificity adapts: vague hints first, more specific if still stuck

**Why better than current:**
- Current: no hint or feedback system
- Proposed: proven to achieve highest correct submission rate (hybrid > adaptive-only > GenAI-only)

---

## Foundation: Knowledge Graph

**What it includes:**
- Programming concepts as nodes (arrays, hash-maps, trees, graphs, DP, etc.)
- Prerequisite edges (directed): "arrays" → "hash-maps" → "two-sum patterns"
- Similarity edges (undirected): "BFS" ~ "DFS", "merge sort" ~ "quick sort"
- Problems linked to concepts they test

**How it's built:**
- Initial manual curation from problem tags
- Enhanced via LLM-based automatic prerequisite extraction (ACE methodology)
- Can be refined over time from student performance data

---

## Data Flow: Complete Recommendation Cycle

```
1. Student requests a recommendation
   |
2. Layer 1 (KT): Compute current mastery per concept
   |-- P(arrays) = 0.92, P(recursion) = 0.75, P(DP) = 0.20, P(graphs) = 0.10
   |
3. Layer 4 (FSRS): Check if any concept needs review
   |-- "recursion" was last practiced 14 days ago, review due
   |
4. Layer 3 (MAB): Decide: review recursion OR learn something new?
   |-- If review: select recursion concept
   |-- If new: explore between DP (low mastery) and graphs (untried)
   |
5. Layer 2 (Elo): Select problem at right difficulty
   |-- Student's recursion Elo: 1350
   |-- Find problem with difficulty Elo: 1400-1600 (ZPD range)
   |
6. Return recommended problem
   |
7. Student submits solution
   |
8. Update all layers:
   |-- Layer 1: Update P(concept) based on success/failure
   |-- Layer 2: Update student Elo and problem Elo
   |-- Layer 4: Update FSRS memory model for this concept
   |-- Layer 3: Update MAB reward signals
```

---

## Novel Thesis Contributions

1. **Multi-layer integration:** No existing system combines KT + Elo + MAB + FSRS in a unified architecture
2. **Dynamic K-value Elo for programming:** First application of dynamic K to competitive programming domain
3. **Hierarchical MAB with prerequisite constraints:** MAB arms constrained by knowledge graph prerequisites
4. **FSRS for programming concept retention:** First application of FSRS to programming skill retention (vs flashcards)
5. **Hybrid adaptive + LLM feedback:** Combining algorithmic recommendations with LLM-generated scaffolded hints

---

## Implementation Priority

| Priority | Layer | Technique | Difficulty | Impact |
|----------|-------|-----------|------------|--------|
| 1 (must) | Layer 2 | Elo Rating | Low | High — enables ZPD |
| 2 (must) | Layer 1 | BKT (pyBKT) | Low-Medium | High — enables mastery tracking |
| 3 (must) | Layer 3 | Hierarchical MAB | Medium | High — core recommendation logic |
| 4 (should) | Foundation | Knowledge Graph | Medium | Medium — enables prerequisites |
| 5 (should) | Layer 4 | FSRS | Low | Medium — enables review scheduling |
| 6 (nice) | Layer 5 | LLM + RAG | High | Medium — enhancement, not core |

---

## Open-Source Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| pyBKT | https://github.com/CAHLR/pyBKT | Bayesian Knowledge Tracing |
| DKT2 | https://github.com/zyy-2001/DKT2 | Deep Knowledge Tracing |
| pyKT | https://github.com/pykt-team/pykt-toolkit | KT model toolkit |
| Hierarchical MAB | https://github.com/b-castleman/hierarchical-mab-tutoring | MAB recommendation |
| FSRS | https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler | Spaced repetition |
| Elo-MMR | https://github.com/EbTech/Elo-MMR | Rating system |
