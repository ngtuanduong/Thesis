# Graph Neural Networks & Knowledge Graphs: State of the Art (2024-2026)

GNN/KG approaches address: **"How are programming concepts related, and how do we use that structure?"**

---

## 1. GNN-based Educational Resource Recommendation — 2025

**What it is:** Uses GNN to model the tripartite relationship between students, learning resources, and knowledge points. Achieves NDCG@10 of 0.93 in standard scenarios and 0.88 in knowledge gap scenarios.

**Why it's better:** Traditional systems treat items independently. GNN models structural relationships (prerequisites, similarity) between concepts and between students. This structural awareness leads to better recommendations.

**Application to our system:** Build a knowledge graph:
- Nodes = programming concepts + problems + students
- Edges = prerequisite relations, concept-problem associations, student-problem interactions
- GNN propagates information through this graph to fill knowledge gaps

**References:**
- Liu, 2025: https://journals.sagepub.com/doi/10.1177/14727978251374326
- GNN Recommendation Survey: https://dl.acm.org/doi/10.1145/3694784

---

## 2. Graph Attention + Deep Reinforcement Learning for Learning Paths — 2025

**What it is:** Combines Graph Attention Networks (GAT) with Actor-Critic RL to generate personalized learning paths. GAT assigns importance weights to concept connections, RL learns optimal sequencing.

**Why it's better:** Student scores improved by **5.8 and 12.8 points**, accuracy improved by **5.3%** vs previous deep learning models. Graph attention dynamically weighs which prerequisites matter most for each individual student.

**Application to our system:** Model programming curriculum as a directed graph. RL agent navigates it, deciding optimal concept sequence per student. E.g., Student A benefits from "hash maps" before "two pointers," while Student B is ready for "graphs" directly.

**References:**
- Gu, 2025: https://journals.sagepub.com/doi/10.1177/14727978241313260
- KG+DRL: https://www.nature.com/articles/s41598-025-17918-x

---

## 3. Prerequisite-Enhanced Category-Aware GNN — 2024

**What it is:** GNN model that learns prerequisite relations between concepts and uses them for recommendation. Uses both category info and prerequisite structures.

**Application to our system:** Directly model "arrays before hash maps" and "recursion before tree traversals." GNN uses prerequisite edges to avoid recommending problems the student isn't ready for.

**References:**
- ACM TKDD: https://dl.acm.org/doi/10.1145/3643644

---

## 4. AI-Assisted Educational Knowledge Graph Construction (ACE) — 2024

**What it is:** Methodology for automatically constructing Educational Knowledge Graphs with prerequisite relations using AI.

**Application to our system:** Automatically generate the programming concept knowledge graph from textbooks, syllabi, or problem descriptions — instead of manual curation.

**References:**
- JEDM: https://jedm.educationaldatamining.org/index.php/JEDM/article/view/737
