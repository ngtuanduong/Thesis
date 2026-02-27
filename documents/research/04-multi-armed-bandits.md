# Multi-Armed Bandits for Education: State of the Art (2024-2026)

MAB algorithms address: **"Should we recommend what the student needs (exploit) or explore new topics?"**

---

## 1. Hierarchical MAB for Intelligent Tutoring — August 2024

**Paper:** "Hierarchical MAB for ITS" — August 2024

**What it is:** Open-source hierarchical MAB that operates at two levels:
1. **Level 1:** Select which **concept** to tutor (arrays, trees, graphs, DP)
2. **Level 2:** Select the appropriate **difficulty** within that concept (easy/medium/hard)

Uses Bayesian Knowledge Tracing for mastery estimation and incorporates memory decay.

**Why it's better:** Unlike flat MAB approaches, it handles the real structure of educational content. The difficulty-adaptive version significantly outperforms the difficulty-agnostic version. Evaluated with simulated groups of 500 students.

**Application to our system:** Directly applicable.
- Level 1: Choose concept to practice
- Level 2: Choose difficulty within that concept
- Balances exploring new concepts vs reinforcing weak ones
- Within a concept, explores whether student is ready for harder problems

**Implementation:** Full open-source code at https://github.com/b-castleman/hierarchical-mab-tutoring

**References:**
- arXiv: https://arxiv.org/abs/2408.07208
- OpenReview: https://openreview.net/forum?id=ag2m818qUm

---

## 2. MAB with Abandonment (MAB-A) — NeurIPS 2024

**Paper:** NeurIPS 2024

**What it is:** MAB model that accounts for **user abandonment** — users leave the platform if recommendations are too boring or too hard. ULCB and KL-ULCB algorithms increase exploration when engaged, decrease when disengaged.

**Why it's better:** Traditional MAB optimizes for learning but ignores engagement. If a student gets frustrated or bored, they stop using the platform entirely. MAB-A explicitly models this.

**Application to our system:** Monitor whether students complete or abandon recommended problems:
- Student abandoning → shift toward comfort zone (exploitation)
- Student completing → increase exploration of new/harder topics

**References:**
- NeurIPS 2024: https://neurips.cc/virtual/2024/poster/98312
- JMLR: https://jmlr.org/papers/v25/22-1251.html
