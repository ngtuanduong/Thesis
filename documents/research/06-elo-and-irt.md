# Elo Rating & Item Response Theory: State of the Art (2024-2026)

Elo/IRT addresses: **"How do we calibrate student skill AND problem difficulty simultaneously?"**

---

## 1. Dynamic K-Value Elo Rating — December 2025

**Paper:** Springer, December 2025

**What it is:** Novel modification to Elo that dynamically adjusts the K sensitivity parameter based on observed trends. When rating changes show consistent upward/downward trends (student learning or struggling), K increases. Otherwise, K decreases for stability.

**Why it's better:** Traditional fixed-K Elo forces a trade-off:
- Large K → tracks fast learning but volatile
- Small K → stable but slow to respond

Dynamic K adapts to individual learning pace. Validated on Math Garden platform.

**Application to our system:** Rate both students AND problems using Elo. As a student rapidly improves in "graph algorithms," dynamic K detects the upward trend, increases sensitivity, and quickly matches them with harder graph problems. When progress stabilizes, K decreases for accurate steady-state rating.

**References:**
- Springer: https://link.springer.com/article/10.1007/s11257-025-09439-z

---

## 2. Elo Rating for Programming Exercises — Proven

**Paper:** ACM TOCE

**What it is:** Applying Elo to simultaneously estimate learner skill and problem difficulty. Each interaction updates both ratings.

**Why it's better:** Computationally cheap, simple, works with small sample sizes (unlike IRT which needs large calibration datasets), naturally handles skill changes over time. Tested on 76 tasks, 299 users, 50,055 attempts, 300,000+ unit tests.

**Application to our system:** Directly applicable. Each attempt updates both ratings. Recommend problems whose difficulty is slightly above student's skill rating (Zone of Proximal Development).

**References:**
- ACM TOCE: https://dl.acm.org/doi/10.1145/3511886

---

## 3. Multidimensional Elo — EDM 2025

**What it is:** Tracks concept-specific student proficiency and question difficulty using multivariate Elo. Outperforms logistic regression with improved cold-start performance.

**Application to our system:** Instead of one Elo per student, maintain separate ratings per concept (arrays, trees, DP, etc.). Enables targeted recommendations.

**References:**
- EDM 2025: https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.long-papers.99/index.html

---

## 4. Platform Rating Systems in Practice

| Platform | System | Details |
|----------|--------|---------|
| Codeforces | Generalized Elo (multiplayer) | Rates students + problems simultaneously |
| CodeChef/DMOJ | Elo-MMR (Bayesian) | Incentive-compatible, linear-time, robust |
| Math Garden | Dynamic K-value Elo | Real-time with response time integration |

**Elo-MMR Implementation:** https://github.com/EbTech/Elo-MMR

---

## Zone of Proximal Development (ZPD)

ZPD defines three zones:
- **Can do alone:** Too easy, limited learning
- **ZPD (sweet spot):** Can solve with some scaffolding — maximum learning
- **Cannot do even with help:** Too hard, frustrating, no learning

**Operationalizing ZPD:** Using Elo ratings, ZPD = problems whose difficulty is +100 to +300 Elo points above the student's current skill. Dynamic K-value Elo is particularly suited because it adapts to learning pace.

**References:**
- Springer: https://link.springer.com/chapter/10.1007/3-540-47987-2_75
- NWEA 2025: https://www.nwea.org/blog/2025/the-zone-of-proximal-development-zpd-the-power-of-just-right/
