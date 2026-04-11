# Thesis Documentation Suite — Master Index

**Thesis:** Adaptive Learning Platform for University Programming Courses
**Author:** Nguyen Tuan Duong
**Advisor:** Bui Quoc Khanh
**Institution:** Hanoi University, Faculty of Information Technology
**Date:** February 2026

---

## Document Index

| # | Document | Description |
|---|----------|-------------|
| 01 | [Thesis Complete Outline](./01-THESIS-COMPLETE-OUTLINE.md) | Full chapter-by-chapter thesis structure with writing guidance, word count targets, and key arguments per section |
| 02 | [Literature Review](./02-LITERATURE-REVIEW.md) | Comprehensive thematic literature review covering adaptive learning, knowledge tracing, spaced repetition, MAB, Elo/IRT, GNNs, and LLMs in education |
| 03 | [System Architecture](./03-SYSTEM-ARCHITECTURE.md) | Complete technical architecture: current system analysis, proposed 5-layer design, data flows, database schema, API design |
| 04 | [Algorithm Design](./04-ALGORITHM-DESIGN.md) | Deep mathematical and algorithmic treatment of each layer: BKT/DKT2, Dynamic Elo, Hierarchical MAB, FSRS, Knowledge Graphs |
| 05 | [Implementation Plan](./05-IMPLEMENTATION-PLAN.md) | Step-by-step implementation roadmap with phases, dependencies, file changes, technology choices, and risk assessment |
| 06 | [Implementation Tracker](./06-IMPLEMENTATION-TRACKER.md) | Living checklist of every feature/component with status tracking, current system audit, and test criteria |
| 07 | [Evaluation Plan](./07-EVALUATION-PLAN.md) | Experiment design: research questions, metrics, protocol (pre/post-test, control groups), statistical analysis, survey instruments |
| 08 | [Brainstorm Novel Contributions](./08-BRAINSTORM-NOVEL-CONTRIBUTIONS.md) | Novelty analysis: what makes this thesis unique, comparison with commercial platforms, publication potential |
| 09 | [References](./09-REFERENCES.md) | Complete bibliography organized by topic with all cited works |

---

## How to Use These Documents

1. **Start with 01** to understand the overall thesis structure and what goes where
2. **Use 02** as the foundation for writing Chapter 2 (Literature Review) of the thesis
3. **Use 03 and 04** together when writing Chapter 3 (System Design) — architecture first, then algorithms
4. **Follow 05** during implementation — it provides the execution order
5. **Update 06** continuously as you build — it tracks what's done vs what remains
6. **Use 07** to design and run experiments for Chapter 4 (Evaluation)
7. **Reference 08** when writing the Introduction and Conclusion — it clarifies your contributions
8. **Cite from 09** — all references are pre-formatted in IEEE style

## Cross-Reference Map

```
01 Outline ─────────► Guides structure of ALL other documents
02 Literature ──────► Feeds into 03 (justifies architecture choices)
                    ► Feeds into 04 (grounds algorithm selection)
                    ► Feeds into 08 (identifies gaps = contributions)
03 Architecture ────► Feeds into 04 (algorithms implement the layers)
                    ► Feeds into 05 (implementation follows architecture)
04 Algorithms ──────► Feeds into 05 (implementation realizes algorithms)
                    ► Feeds into 07 (evaluation measures algorithm performance)
05 Plan ────────────► Feeds into 06 (tracker follows the plan)
06 Tracker ─────────► Living document updated during development
07 Evaluation ──────► Independent; references 04 for metrics
08 Contributions ───► Synthesis of 02 + 03 + 04
09 References ──────► Cited throughout all documents
```
