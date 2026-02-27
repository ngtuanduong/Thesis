# Spaced Repetition: State of the Art (2024-2026)

Spaced repetition addresses: **"When should the student review a concept they've already learned?"**

---

## 1. FSRS (Free Spaced Repetition Scheduler) — The Modern Standard

**What it is:** Open-source, ML-based spaced repetition algorithm. Models memory with three variables:
- **Difficulty:** How hard is this concept for the student?
- **Stability:** How long until recall probability drops significantly?
- **Retrievability:** What is the current probability of recall?

**Why it's better:** Achieves **20-30% fewer reviews** for the same retention level compared to SM-2 (the algorithm used by Anki for decades). Now built into Anki (since v23.10) and RemNote. Unlike SM-2's fixed intervals, FSRS learns individual memory patterns.

**Application to our system:** After a student solves a problem involving "two pointers," FSRS predicts when they'll start forgetting and schedules a review problem at the optimal time. Prevents the common pattern: learn → move on → forget completely.

**Implementation:**
- Python package: `pip install fsrs`
- GitHub: https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler
- Wiki: https://github.com/open-spaced-repetition/fsrs4anki/wiki

---

## 2. LECTOR (LLM-Enhanced Concept-based Test-Oriented Repetition) — August 2025

**Paper:** "LECTOR" — August 2025

**What it is:** Combines LLMs with spaced repetition. Uses In-Context Learning (ICL) to assess semantic similarity between concepts, identifying "confusable" items that should be reinforced together.

**Why it's better:** Achieves **90.2% success rate** vs 88.4% for the best baseline (SSP-MMC) across 100 simulated learners over 100 days. Key innovation: addresses **semantic confusion** — similar concepts that learners mix up.

**Application to our system:** Programming has many confusable concepts:
- BFS vs DFS
- Stack vs Queue operations
- Merge Sort vs Quick Sort
- Iterative vs Recursive approaches

LECTOR identifies when a student confuses similar algorithms and schedules targeted practice that forces discrimination between them.

**References:**
- arXiv: https://arxiv.org/abs/2508.03275
- OpenReview: https://openreview.net/forum?id=wprP6MbBYd
