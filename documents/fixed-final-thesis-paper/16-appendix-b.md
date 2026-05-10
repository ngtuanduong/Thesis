# APPENDIX B. KNOWLEDGE GRAPH SPECIFICATION

## B.1 Overview

The knowledge graph contains 34 programming concepts and 52 directed prerequisite edges. I curated the taxonomy from Hanoi University's introductory Python curriculum and grouped concepts into five difficulty tiers (T1 Foundations through T5 Expert) and seven topic groups. The graph is the foundation of the adaptive engine. Layer 1 (BKT) uses the problem-to-concept mapping; Layer 3 (MAB) uses prerequisite edges for gating; Layer 4 (FSRS) uses the graph to schedule the right concept for review. Figure 3.2 in Chapter 3 shows a 10-concept slice of the graph for visual readability. The data lives in `server/prisma/seed-adaptive.ts` and seeds the `concepts` and `knowledge_graph_edges` tables. The full 34-concept listing and all 52 edges are in the companion file (see B.6).

## B.2 Tier Definitions

*Table B.1. Difficulty tiers.*

| Tier | Label | Count | Description |
| --- | --- | --- | --- |
| T1 | Foundations | 7 | Variables, types, operators, I/O, strings, conditionals, loops. The first weeks of any introductory course. |
| T2 | Core Skills | 8 | Functions, parameters, return values, lists, tuples, dictionaries, nested loops, basic searching. |
| T3 | Intermediate | 8 | Scope, recursion, sets, stacks, queues, classes, sorting, sliding window. |
| T4 | Advanced Application | 6 | Inheritance, encapsulation, polymorphism, two pointers, greedy, divide and conquer. |
| T5 | Expert | 5 | Dynamic programming, graphs, trees, backtracking, bit manipulation. |

The 7 + 8 + 8 + 6 + 5 split sums to 34. Tiers also drive Elo seeding: T1 problems start at 1000, T3 at 1200, T5 at 1400.

## B.3 Topic Groups

Concepts are tagged with a `topicGroup` field for grouping in the recommendation UI and review queue. The seven groups are: `basics` (T1 fundamentals), `control_flow` (conditionals, loops, nested loops), `functions` (definition, parameters, return values, scope, recursion), `data_structures` (lists, tuples, dictionaries, sets, stacks, queues), `oop` (classes, inheritance, encapsulation, polymorphism), `algorithms` (searching, sorting, sliding window, two pointers, greedy, divide and conquer), and `advanced` (DP, graphs, trees, backtracking, bit manipulation).

## B.4 Sample Concepts

The 10 concepts below match the Figure 3.2 slice in Chapter 3.

*Table B.2. Sample concepts (10 of 34) spanning all five tiers.*

| Name | Display Name | Topic Group | Tier | Description |
| --- | --- | --- | --- | --- |
| variables | Variables and Assignment | basics | 1 | Variable declaration, assignment, naming. |
| conditionals | Conditional Statements | control_flow | 1 | if / elif / else and boolean logic. |
| loops | Loops | control_flow | 1 | for and while loops, break, continue. |
| functions | Functions | functions | 2 | Function definition, calling, docstrings. |
| lists | Lists | data_structures | 2 | Indexing, slicing, comprehensions. |
| recursion | Recursion | functions | 3 | Base cases, recursive thinking. |
| sorting | Sorting Algorithms | algorithms | 3 | Bubble, insertion, merge, quicksort. |
| two_pointers | Two Pointers Technique | algorithms | 4 | Opposite and same-direction patterns. |
| dynamic_programming | Dynamic Programming | advanced | 5 | Memoization, tabulation, optimal substructure. |
| trees | Trees | advanced | 5 | Binary trees, BST, traversals. |

## B.5 Edge Types

Every edge currently uses one relation type, `PREREQUISITE`, with a default weight of 1.0. An edge `u → v` means concept `u` must be mastered before the recommender unlocks concept `v` (the threshold is mastery probability ≥ 0.85, see Section 3.3.5). The relation column and weight column are reserved for future relation types such as `RELATED_TO` (lateral suggestions) and `EXTENDS` (deeper variants), which are noted as future work and not used in the pilot.

## B.6 Companion File

The full 34-concept inventory and all 52 prerequisite edges, plus edge statistics (root, leaves, longest path), are in [appendix-b-companion-full-kg.md](appendix-b-companion-full-kg.md). The companion file lives outside the main paper page count.
