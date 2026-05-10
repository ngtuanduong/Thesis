# CHAPTER 6. CONCLUSION

## 6.1. Summary of Work

This thesis should be read as an implementation thesis with a pilot evaluation protocol, not as a completed classroom evaluation. I designed and built an adaptive learning platform for university programming courses, and I specified — but did not run — a pilot study to evaluate it. Chapter 1 set out the problem: high failure rates and heterogeneous backgrounds in introductory programming, which one-size-fits-all instruction cannot fix at scale [1], [2]. Chapter 2 surveyed the techniques that address it — Bayesian Knowledge Tracing, Elo-based difficulty calibration, multi-armed bandits, spaced repetition, and knowledge graphs — and confirmed that no existing platform integrates all of them for programming. Chapter 3 specified a five-layer adaptive engine over a hand-curated knowledge graph of ~30 Python concepts, and a four-component deployment architecture. Chapter 4 turned that design into a working full-stack system: React frontend, NestJS gateway, FastAPI adaptive service, PostgreSQL, Redis, and a Docker code sandbox. The platform runs end to end. Chapter 5 specified the pilot protocol: a between-subjects, pre-/post-test design with 40–60 students, four-week intervention plus two-week retention, sixteen metrics across four research questions, pre-registered effect-size thresholds, and a full statistical plan.

## 6.2. Contributions Revisited

**Contribution 1 — An integrated adaptive platform for programming courses (Chapters 3–4).** I designed and built a closed-loop platform that combines Bayesian Knowledge Tracing, Dynamic K-Value Elo, prerequisite-constrained Hierarchical MAB with Thompson Sampling, and FSRS, unified by a curated knowledge graph. The integration is the engineering contribution: BKT mastery gates MAB exploration, Elo ratings constrain selection to the student's Zone of Proximal Development [20], and FSRS reviews can interrupt the MAB. The platform is implementation evidence, not a paper design. The system runs end to end. It is deployed with Docker Compose [Chapter 4 §4.2], every adaptive layer in §3.3 has running code that talks to the database and serves an HTTP endpoint, the React frontend renders against live adaptive state, and feature flags allow control-group fallback for the pilot. This is the strongest claim the thesis makes.

**Contribution 2 — A pilot evaluation protocol (Chapter 5).** I specified a pre-registered, between-subjects pilot for Hanoi University undergraduates: recruitment and consent, instruments (custom pre-/post-test, SUS, TAM, semi-structured interviews), quantitative metrics with predetermined thresholds, and a statistical plan that includes a small-sample contingency. The protocol evaluates Layers 1–4 as a whole, not individual layers. It is a design ready for execution.

The two contributions sit in different states. Contribution 1 is realised in software. Contribution 2 is realised as a study design awaiting empirical execution.

## 6.3. Limitations

Several limits constrain the claims this thesis can make.

**No in-the-wild evaluation yet.** The pilot is specified, not run. The four research questions remain open. Effectiveness claims rest on theoretical alignment with prior literature, not on data from the target population.

**Layer 5 not evaluated.** The LLM Socratic hint module is built but disabled in the pilot to avoid confounding the evaluation of Layers 1–4. It is exploratory engineering, not a contribution. Hint quality, cost, and hallucination risk are unmeasured.

**Hyperparameters are heuristic, not learned.** The mastery threshold (0.85), the Elo K-base (25), the MAB reward weights, and the FSRS rating mapping are design choices grounded in the literature, not values fitted to this dataset. The pilot includes a sensitivity analysis plan in §5.4.2, but no per-student fitting yet.

**Knowledge graph is hand-curated.** The ~30-concept graph in Appendix B is an introductory Python curriculum. Extending the platform to broader programming curricula would need substantial graph expansion and re-validation.

## 6.4. Future Work

Future work follows the limitations and is ordered by priority.

**Run the pilot.** The most pressing next step is to execute the protocol in Chapter 5. Recruiting 40–60 students, running the four-week intervention, and analysing the resulting submission, recommendation, and survey data will turn Contribution 2 from a specified study into reported results. This unlocks the rest of the list.

**Evaluate Layer 5 standalone.** A separate controlled study should measure the LLM hint module on three axes: cost per session, hallucination rate, and time-to-solution change against a no-hints baseline. Only with these numbers does Layer 5 earn the right to ship in the main pipeline.

**Upgrade BKT to DKT2 once data accumulates.** Chapter 2 §2.2.2 explained why I chose BKT over DKT for the first deployment: interpretability and small-data robustness. Once the pilot produces enough submission sequences, swapping in DKT2 [Chapter 2 §2.2.2] becomes practical and is expected to lift predictive AUC.

**Expand the knowledge graph.** Adding Java and C++ tracks, plus deeper algorithm and data-structure subgraphs, will test the generality of the five-layer architecture across languages and course levels.

**Per-student parameter learning.** The default BKT parameters are the same for every student. Fitting per-skill parameters with EM, once per-skill response counts are sufficient, should improve predictive validity and reduce reliance on heuristic defaults.

**Multi-institution deployment.** Deploying across several Vietnamese universities — and eventually across institutions in different educational contexts — would enable larger-scale evaluation, cross-institution comparison, and stress-tests of the platform's operational assumptions under varied curricula and student populations.
