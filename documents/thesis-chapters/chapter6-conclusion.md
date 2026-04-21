# Chapter 6. Conclusion

This chapter summarizes the work presented in this thesis, articulates the contributions made, acknowledges limitations, and outlines directions for future research.

## 6.1. Summary of Work

This thesis addressed the problem of providing personalized programming instruction at scale in Vietnamese university settings. The work proceeded through five stages, each corresponding to a preceding chapter.

Chapter 1 established the motivation for adaptive learning in programming education, identified the research gap---that no existing platform integrates knowledge tracing, difficulty calibration, intelligent problem selection, and spaced repetition within a single system---and formulated four research questions concerning prediction accuracy, recommendation effectiveness, long-term retention, and perceived usability.

Chapter 2 surveyed the theoretical foundations and related work across six areas: Bayesian Knowledge Tracing, Elo-based difficulty calibration, multi-armed bandit recommendation, spaced repetition scheduling, knowledge graphs for prerequisite modeling, and large language model feedback generation. The review identified that while each technique has been validated independently, their integration into a unified adaptive loop for programming education remains unexplored.

Chapter 3 presented the system design, specifying a five-layer adaptive architecture (Knowledge Tracer, Difficulty Calibrator, Problem Selector, Review Scheduler, and an optional LLM Feedback Engine) coordinated through a knowledge graph of approximately 30 Python programming concepts and 45 prerequisite edges. The chapter detailed the four-component deployment architecture (React frontend, NestJS gateway, FastAPI AI service, and PostgreSQL with Redis and Docker sandbox), the database schema, API contracts, caching strategy, and data flow sequences.

Chapter 4 described the implementation of each adaptive layer, including the construction of the knowledge graph, the parameter initialization and update logic for BKT and dynamic Elo, the hierarchical multi-armed bandit with Thompson Sampling, the FSRS integration with a submission-to-rating mapping, and the RAG-based hint generation pipeline. The chapter also documented frontend implementation decisions, the Docker-based code execution sandbox, and deployment configuration.

Chapter 5 specified a pilot evaluation protocol: a between-subjects mixed-methods design with pre-test and post-test, targeting 40 to 60 undergraduate students over a four-week intervention period followed by a two-week retention phase. The chapter defined 16 metrics across four research questions, established pre-registered statistical thresholds, described the planned analysis procedures, and discussed threats to validity.

In summary, this thesis designed, implemented, and deployed a working adaptive learning platform, and specified a rigorous evaluation protocol for future empirical validation.

## 6.2. Contributions

This thesis makes two primary contributions.

**Contribution 1: An integrated adaptive learning platform for programming education (Chapters 3--4).** The platform combines Bayesian Knowledge Tracing, dynamic Elo rating, hierarchical multi-armed bandits with Thompson Sampling, and the Free Spaced Repetition Scheduler into a single closed-loop system. These four layers operate through a shared knowledge graph that encodes prerequisite relationships among programming concepts, enabling prerequisite-gated recommendations and mastery-aware review scheduling. The integration is the central contribution: while each algorithm has been studied in isolation, their composition---where BKT mastery estimates gate MAB arm availability, Elo ratings constrain the candidate set to the learner's zone of proximal development, and FSRS schedules review of previously mastered concepts---represents a configuration not previously reported in the literature for programming education. The platform is a working, deployable web application rather than a theoretical framework, implemented with open-source technologies suitable for adoption at Vietnamese universities.

**Contribution 2: A pilot evaluation protocol (Chapter 5).** The thesis specifies a pre-registered mixed-methods evaluation design with clearly defined independent and dependent variables, 16 quantitative and qualitative metrics mapped to four research questions, predetermined effect-size thresholds, and a structured analysis plan including both frequentist and Bayesian statistical tests. The protocol addresses internal and external validity threats and provides a replicable template for evaluating adaptive learning systems in similar institutional contexts.

**Optional extension: LLM-based Socratic hints (Layer 5).** The platform includes a retrieval-augmented generation pipeline that produces Socratic-style hints grounded in the knowledge graph and relevant code context. This layer was implemented as a proof-of-concept but deliberately excluded from the pilot evaluation protocol to avoid confounding the assessment of the core adaptive layers (Layers 1--4).

## 6.3. Limitations

Several limitations constrain the claims that can be drawn from this work.

**Absence of empirical results.** The pilot evaluation protocol has been specified but not yet executed. Consequently, the research questions remain unanswered, and the effectiveness of the adaptive layers is supported only by theoretical arguments and alignment with prior literature rather than by experimental evidence from the target population.

**Single-site sample.** The planned evaluation targets students at a single Vietnamese university, which limits generalizability to other institutions, curricula, or cultural contexts. Even if executed, the sample size of 40 to 60 participants constrains statistical power and the detection of small effect sizes.

**Confounded treatment condition.** The experimental design enables all four adaptive layers simultaneously in the treatment group. This bundled intervention means that, should positive effects be observed, it will not be possible to attribute them to any individual layer. Isolating the contribution of each component would require a factorial or ablation design with substantially larger sample sizes.

**Short intervention window.** A four-week active period with two-week retention follow-up may be insufficient to observe the full benefits of spaced repetition scheduling, which is designed to operate over months or years. Long-term retention effects may therefore be underestimated.

**Metric-model coupling.** Several evaluation metrics (e.g., mastery probability, predicted performance) are derived from the same models being evaluated. While this is mitigated by the inclusion of external measures such as pre/post-test scores and the SUS questionnaire, the coupling introduces a risk of circular validation for model-internal metrics.

**Knowledge graph scope.** The current knowledge graph covers approximately 30 Python programming concepts. This scope is sufficient for introductory courses but may not capture the full complexity of intermediate or advanced programming curricula.

## 6.4. Future Work

Future research directions proceed from immediate next steps to longer-term goals.

**Immediate: Execute the pilot evaluation.** The most pressing next step is to recruit participants and conduct the four-week intervention as specified in Chapter 5. Collecting pre-test, post-test, interaction log, and survey data will provide the first empirical evidence regarding the platform's effectiveness and allow the research questions to be answered.

**Short-term: Ablation studies.** Following the initial pilot, a factorial experiment that systematically enables and disables individual layers (e.g., BKT only, BKT + Elo, BKT + Elo + MAB, full system) would clarify the marginal contribution of each component. Such a study would require a larger participant pool, potentially across multiple course sections or semesters.

**Short-term: Validate LLM-based hints.** A separate controlled study could assess whether the Socratic hint generation pipeline (Layer 5) improves debugging skills and reduces time-to-solution without promoting over-reliance on generated assistance.

**Medium-term: Automated knowledge graph construction.** The current knowledge graph was manually constructed by domain experts. Natural language processing techniques applied to course materials, textbooks, and problem statements could partially automate the extraction of concepts and prerequisite relationships, reducing the effort required to extend the platform to new programming languages or courses.

**Medium-term: Multi-course scaling.** Extending the platform beyond introductory Python to additional languages (Java, C++) and course levels (data structures, algorithms) would test the generality of the five-layer architecture and the transferability of the adaptive algorithms.

**Medium-term: Instructor analytics dashboard.** Providing instructors with aggregated views of class-level mastery distributions, common misconceptions, and at-risk students would complement the student-facing adaptive features and support data-informed pedagogical decisions.

**Long-term: Cross-institutional deployment.** Deploying the platform across multiple Vietnamese universities would enable larger-scale evaluation, cross-institutional comparison, and investigation of how institutional context moderates adaptive learning effectiveness.

**Long-term: LMS integration.** Integration with established learning management systems such as Moodle or Canvas via LTI (Learning Tools Interoperability) would lower adoption barriers and enable the adaptive engine to operate within existing institutional infrastructure.

**Long-term: Longitudinal retention studies.** Multi-semester tracking of student performance would provide stronger evidence for the FSRS scheduling layer's contribution to durable skill retention, addressing one of the limitations of the short intervention window in the current protocol.

## 6.5. Closing Remarks

Programming education occupies a position of growing importance in higher education, yet the fundamental challenge of matching instruction to individual learner needs at scale remains inadequately addressed by existing platforms and pedagogical practices. This thesis proposes one approach to that challenge: an adaptive learning platform that draws on established techniques from educational data mining, psychometrics, and information retrieval, integrating them into a coherent system designed for practical deployment in Vietnamese university programming courses. The decision to combine multiple well-studied algorithms---rather than pursuing a single technique in isolation---reflects a conviction that effective personalization requires multiple complementary mechanisms operating in concert: modeling what the learner knows, calibrating what is appropriately challenging, selecting what to practice next, and scheduling when to revisit prior material.

The work presented here represents a starting point rather than a conclusion. The platform exists as a functional artifact, and the evaluation protocol provides a path toward empirical validation. Whether the proposed integration of knowledge tracing, difficulty calibration, intelligent recommendation, and spaced repetition produces measurable improvements in learning outcomes is a question that future data collection will answer. This thesis contributes the architectural design, the working implementation, and the methodological framework necessary to pursue that answer. If the adaptive approach proves effective, it may offer a scalable means of providing the individualized practice and feedback that programming learners require---without demanding proportional increases in instructor effort. Ultimately, the goal is not to replace human instruction but to augment it: to ensure that each student receives practice at the right level, at the right time, on the right concept---at a scale that no single instructor could achieve alone.
