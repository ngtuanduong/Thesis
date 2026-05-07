# 2. Related Work and Theoretical Background

This section reviews the four adaptive techniques that the proposed platform integrates and situates our work with respect to prior programming-education systems. Each subsection closes with the specific design implication that the literature carries for this paper.

## 2.1. Knowledge tracing

Bayesian Knowledge Tracing (Corbett & Anderson, 1995) models mastery of a skill as a two-state hidden Markov process with four parameters: prior knowledge P(L₀), transition P(T), guess P(G), and slip P(S). BKT is interpretable, data-efficient, and remains the reference baseline in modern intelligent tutoring systems (Ma et al., 2014). Deep Knowledge Tracing (Piech et al., 2015) and subsequent neural variants improve raw predictive accuracy but require orders of magnitude more interaction data and sacrifice the interpretability that instructors need to trust the mastery estimate. **Relevance to this work:** BKT is chosen as Layer 1 because this platform must operate with cold-start populations of a few hundred learners, and because the mastery estimate is consumed downstream by a bandit that benefits from calibrated uncertainty rather than raw point accuracy.

## 2.2. Difficulty calibration and the Zone of Proximal Development

Pelánek (2016) formalized Elo-style rating for adaptive educational systems, showing that dual student–item ratings converge within roughly twenty attempts per learner and stabilize faster than Item Response Theory alternatives in small cohorts. The framework operationalizes Vygotsky's (1978) Zone of Proximal Development (ZPD) and Bjork and Bjork's (2011) desirable-difficulties principle, both of which argue that optimal learning occurs when task difficulty modestly exceeds current ability. **Relevance to this work:** Layer 2 adopts dual Elo ratings as the difficulty-calibration mechanism, and the Elo deltas are used to filter the candidate pool to the learner's ZPD before the bandit selects.

## 2.3. Multi-Armed Bandits in education

Thompson Sampling (Chapelle & Li, 2011) is the de facto choice for exploration–exploitation problems with small effective sample sizes, as is typical in one-semester classroom deployments. Rollinson and Brunskill (2015) demonstrated that bandit policies can outperform fixed curricula when combined with a learner model; Segal et al. (2018) extended this to structured action spaces using hierarchical bandits. **Relevance to this work:** Layer 3 uses a two-level hierarchical Thompson-sampling bandit in which the outer level selects the next concept to practise and the inner level selects a specific problem within that concept, with both levels constrained by the knowledge graph and the ZPD filter.

## 2.4. Spaced repetition and FSRS

The spacing effect — that distributed practice produces better long-term retention than massed practice — is among the most robust findings in cognitive psychology (Cepeda et al., 2006). Algorithmic schedulers have evolved from heuristic SM-2 to machine-learned models (Settles & Meeder, 2016) and, most recently, to the Free Spaced Repetition Scheduler (Ye et al., 2022), which formulates the scheduling problem as a stochastic shortest-path and reports 20–30% fewer reviews than SM-2 for the same retention target. Crucially, the existing FSRS literature evaluates on vocabulary and factual-recall tasks; programming is a procedural skill whose decay dynamics are less well understood. **Relevance to this work:** Layer 4 applies FSRS to programming skill retention, which, to the best of our knowledge, has not been reported previously; Section 3.6 describes the novel submission-to-rating mapping this application requires.

## 2.5. Programming platforms and the integration gap

Commercial platforms such as LeetCode, HackerRank, and Codeforces provide large problem libraries but rely on static difficulty tags and static taxonomies; none of them closes the loop from learner outcome back to problem selection. Research prototypes have examined individual adaptive components in programming education, but the literature does not report a system that simultaneously integrates knowledge tracing, dynamic difficulty calibration, bandit-based selection, and spaced repetition under a shared knowledge graph. **Relevance to this work:** this gap is the paper's core motivation; Table 1 summarizes the four techniques and their complementary roles, and the remainder of the paper describes the integrated architecture that fills the gap.

[TABLE_1_HERE]  *Table 1. Complementary roles of the four integrated adaptive techniques. Source: authors' own synthesis.*
