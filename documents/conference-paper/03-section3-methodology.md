# 3. Methodology

## 3.1. System overview and closed-loop architecture

The platform is organized as a four-component full-stack web application: a React 18 frontend, a NestJS 10 API gateway, a FastAPI adaptive engine written in Python 3.11, and a PostgreSQL 16 database with a Redis 7 cache. A Docker-based sandbox executes submitted code under strict resource limits (256 MB memory, five-second CPU timeout, unprivileged user, no network). Inside the adaptive engine sits a five-layer adaptive stack, shown in Figure 1. Each code submission triggers an asynchronous event that updates Layers 1–4 in parallel, after which the bandit re-ranks the candidate pool for the next recommendation. This closed-loop behaviour is the central architectural property of the platform: the learner model is never stale.

[FIGURE_1_HERE]  *Figure 1. Five-layer adaptive architecture. Source: authors' own work.*

## 3.2. Knowledge graph foundation

All five layers share a single learning artefact: a knowledge graph of 28 programming concepts connected by approximately 45 prerequisite edges, grouped into five difficulty tiers and seven topic clusters (control flow, functions, data structures, recursion, and so on). Every problem in the bank is tagged with one primary concept and zero or more secondary concepts. The graph is authored manually; automated construction from curriculum documents is left as future work. The graph provides the substrate on which BKT estimates are maintained, prerequisite gating is enforced, and FSRS review schedules are aligned.

## 3.3. Layer 1 — Bayesian Knowledge Tracing

Layer 1 maintains a per-learner, per-concept mastery posterior using the four-parameter BKT formulation of Corbett and Anderson (1995). Default parameters are tiered by problem difficulty, with easier concepts initialized to higher P(L₀) and P(T) and more challenging concepts initialized to lower priors. A concept is considered mastered when its posterior mastery exceeds the threshold θ_m = 0.85. The mastery threshold θ_m = 0.85 is a design choice informed by the intelligent-tutoring-systems literature, not an optimum obtained by empirical tuning on this dataset; the follow-up pilot will treat it as a calibration target.

## 3.4. Layer 2 — Dynamic Elo rating

Layer 2 maintains dual Elo ratings: every learner has a rating initialized at 1200, and every problem has a rating initialized at 1000, 1200, or 1400 for Easy, Medium, and Hard tiers respectively, with values clamped to [400, 2800]. A dynamic K-factor in [10, 40] adjusts update magnitude based on recent trend: learners with rapidly changing ratings receive larger updates while stable learners receive smaller ones. The base value K = 25 is a heuristic midpoint chosen for moderate volatility in educational settings, not a tuned optimum. A ZPD filter restricts the candidate pool to problems whose rating differs from the learner's current rating by δ ∈ [50, 250] rating points; this operationalizes the desirable-difficulties principle in a form directly usable by Layer 3.

## 3.5. Layer 3 — Hierarchical MAB with Thompson Sampling

Layer 3 uses a two-level Thompson-sampling bandit. The outer arm selects the next concept to practise; the inner arm selects a specific problem within that concept. Arm eligibility at the outer level is gated by a prerequisite constraint derived from the knowledge graph: a concept becomes eligible only when every one of its prerequisite concepts has reached the mastery threshold θ_m. At the inner level, the ZPD filter from Section 3.4 removes out-of-range problems. The reward function combines three components into a scalar in [0, 1]: expected BKT learning gain with weight w₁ = 0.5, correctness signal w₂ = 0.3, and solve-time efficiency w₃ = 0.2. These weights are a heuristic weighting combining learning gain, difficulty match, and efficiency; they are not learned from empirical data, and re-estimating them from the pilot traces is explicitly listed as future work.

## 3.6. Layer 4 — FSRS and the submission-to-rating mapping

Layer 4 maintains an FSRS-5 state (19 parameters, defaults from Ye et al., 2022) per learner–concept pair, scheduling reviews when retrievability drops below 0.9. The technical novelty at this layer is the mapping from a code submission outcome to an FSRS rating. FSRS was designed for flashcard recall and expects one of four discrete ratings: Again, Hard, Good, Easy. Programming submissions offer a richer signal space: correctness on hidden tests, number of attempts, and time spent. We map this signal space to FSRS ratings through a decision rule that combines correctness (all tests passed vs partial vs failed), attempt count (first-try vs retries), and time relative to the learner's median on problems of the same difficulty tier. To the best of our knowledge, this is the first reported application of FSRS to programming skill retention.

## 3.7. Layer 5 — Optional LLM feedback

Layer 5 provides Socratic-style hints via a retrieval-augmented generation pipeline grounded in the learner's current BKT state (Wang et al., 2023). The layer is designed as a feature-flagged capability that is disabled by default during evaluation to prevent confounding the effect of Layers 1–4.

## 3.8. Pre-registered pilot evaluation protocol

A between-subjects, pre-test/post-test design with a control group is pre-registered. The experimental group uses the four-layer adaptive engine — Layers 1–4 (BKT, Elo, Hierarchical MAB, FSRS); Layer 5 LLM hints are feature-flagged off in the pilot so that the measured treatment effect is attributable to the core adaptive layers and not confounded by generative-AI assistance. The control group uses the identical platform with the adaptive layers replaced by legacy content-based filtering. The control group is constructed to hold constant the platform interface and problem environment while varying only the recommendation logic. The protocol targets n = 40–60 Hanoi University undergraduates across four weeks of intervention with a Week 8 retention follow-up, and IRB review has been completed. Figure 2 summarizes the eight-week timeline. The primary research question (RQ1) concerns predictive validity: whether BKT and Elo mastery estimates predict post-intervention item correctness with AUC ≥ 0.70. Acceptance rate and convergence speed are treated as supporting indicators for RQ1 rather than primary outcomes.

[FIGURE_2_HERE]  *Figure 2. Eight-week pilot evaluation timeline. Source: authors' own work.*
