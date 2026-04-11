# Chapter 1: Introduction

## 1.1 Problem Statement

Programming has become a foundational competency in higher education worldwide, with enrollment in introductory computer science courses growing steadily over the past two decades. Yet despite this growth in demand, programming education continues to face a persistent and well-documented crisis: high failure and dropout rates that far exceed those of most other undergraduate disciplines. A comprehensive systematic literature review by Luxton-Reilly et al. [1] found that failure rates in introductory programming courses average between 30% and 40% globally, a figure that has remained remarkably stable over several decades of pedagogical experimentation. Robins et al. [2], in their seminal review of learning and teaching programming, identified the heterogeneity of student backgrounds as one of the central challenges --- some students arrive with years of self-taught coding experience, while others encounter their first line of code on the first day of class.

This heterogeneity creates a fundamental tension in traditional lecture-based instruction. In a typical university programming class of 50 to 100 students, the instructor must deliver content at a single pace and a single difficulty level. Students who already possess foundational skills --- variables, control flow, basic data structures --- find themselves disengaged while waiting for peers to catch up. Conversely, students who lack prior exposure fall progressively further behind, unable to bridge the gap between knowing syntax and developing the computational thinking required to solve problems independently. Programming, unlike many academic subjects, is fundamentally a *skill* that demands deliberate, individualized practice [3]. Passive consumption of lectures, no matter how well designed, cannot substitute for the iterative cycle of writing code, encountering errors, debugging, and refining solutions.

The problem is compounded by the resource constraints that instructors face. Providing personalized feedback on student code --- identifying misconceptions, suggesting targeted practice problems, and monitoring individual progress across multiple programming concepts --- requires time and effort that scale linearly with class size. In large sections, meaningful individualized instruction becomes practically impossible. Grading coding assignments is itself time-consuming, and delayed feedback diminishes its pedagogical value, as students have often moved on to new topics by the time they receive comments on prior work.

Within the Vietnamese university context specifically, these challenges are no less pressing. Programming courses at Vietnamese institutions face the same diversity of student preparation, the same limitations of one-size-fits-all instruction, and additional constraints including limited access to advanced educational technology platforms and a scarcity of adaptive learning tools designed for local curricula [4]. A worldwide systematic review by Watson and Li [5] confirmed a mean failure rate of 32.3% across 161 courses in 15 countries, underscoring that this is not merely a local phenomenon but a global challenge that Vietnamese institutions share. The gap between the growing demand for software engineering graduates and the effectiveness of current programming pedagogy represents both an educational and an economic concern.

In summary, the core problem this thesis addresses is the mismatch between the individualized, practice-intensive nature of programming skill acquisition and the uniform, resource-constrained reality of university instruction. Students need personalized learning paths, appropriately challenging practice problems, timely feedback, and systematic review of previously learned concepts --- yet current educational practices and platforms provide none of these at scale.

## 1.2 Motivation

### 1.2.1 The Promise of Adaptive Learning

Adaptive learning --- the practice of adjusting instructional content, pace, and methodology based on individual learner characteristics and performance --- has demonstrated significant effectiveness across multiple educational domains [6], [7]. The fundamental premise is that learning is optimized when instruction matches the learner's current knowledge state, cognitive ability, and learning trajectory.

Research spanning several decades has validated this premise. Early Intelligent Tutoring Systems such as the Cognitive Tutor series demonstrated 50--100% improvements in problem-solving skills [3], [8], while modern platforms like ALEKS [9] and Duolingo [10] have shown that machine learning-driven adaptation can operate effectively at scale. A detailed review of these systems and their evolution is provided in Chapter 2.

These success stories motivate the application of adaptive learning to programming education, a domain with properties that make it particularly amenable to data-driven personalization.

### 1.2.2 Why Programming is Uniquely Suited to Adaptive Learning

Programming education possesses several characteristics that distinguish it from other domains and make it an ideal candidate for adaptive learning systems:

**Objectively measurable outcomes.** Unlike essay-based subjects or open-ended creative tasks, programming exercises produce artifacts --- code --- that can be automatically evaluated against test cases, providing at minimum a binary correctness signal and often more granular feedback such as the proportion of tests passed. This measurability provides a clean foundation for knowledge modeling.

**Rich behavioral signals.** Beyond binary correctness, each code submission contains a wealth of information: the number of attempts before success, the time elapsed between attempts, the types of errors encountered (syntax, runtime, logic), the structural complexity of the submitted code, and its similarity to known optimal solutions. These signals are far richer than those available in multiple-choice assessments.

**Hierarchical skill structure.** Programming concepts form a natural prerequisite hierarchy: understanding variables is prerequisite to understanding arrays, which is prerequisite to understanding sorting algorithms, which in turn supports dynamic programming. This structure can be explicitly modeled as a knowledge graph and used to sequence learning.

**Multiple solution paths.** Most programming problems admit multiple correct solutions of varying sophistication (brute force versus optimized approaches), providing opportunities for differentiated assessment based on the approach a student takes.

These properties mean that an adaptive system for programming can leverage unusually rich data to model student knowledge with high fidelity, recommend problems at precisely calibrated difficulty levels, and provide targeted feedback --- capabilities that are difficult or impossible to achieve through manual instruction alone.

### 1.2.3 The Gap in Existing Platforms

Despite the strong case for adaptive learning in programming, existing online coding platforms fail to deliver comprehensive adaptation. Platforms such as LeetCode, HackerRank, and Codeforces have achieved remarkable scale with millions of users, but their pedagogical architecture remains fundamentally static:

- **LeetCode** and **HackerRank** classify problems into fixed difficulty tiers that do not adapt to individual users, with no probabilistic knowledge model or prerequisite awareness.
- **Codeforces** and **CodeSignal** employ Elo-based rating systems, but primarily for competitive ranking or assessment rather than pedagogical recommendation integrated with knowledge tracing or retention scheduling.

A systematic comparison reveals that no existing platform --- academic or commercial --- integrates all the components that learning science indicates are necessary for effective personalized instruction: modeling *what* the student knows (knowledge tracing), calibrating *how hard* each problem is for each individual (difficulty calibration), selecting *which* problem to recommend next to maximize learning (intelligent selection), scheduling *when* to review previously learned concepts to prevent forgetting (spaced repetition), and providing *contextual help* when the student is stuck (feedback generation) [see Table 1.1]. The table includes both programming-focused platforms (LeetCode through CodeSignal) and adaptive learning platforms from other domains (Duolingo through Knewton Alta); the research gap this thesis targets lies precisely at their intersection --- bringing the adaptive sophistication of the latter category into the programming education domain.

**Table 1.1.** Comparison of adaptive capabilities across existing platforms and this thesis.

| Platform       | Knowledge Tracing | Difficulty Calibration | Intelligent Selection | Spaced Repetition | LLM Feedback | Knowledge Graph |
|----------------|:-----------------:|:---------------------:|:--------------------:|:-----------------:|:------------:|:---------------:|
| LeetCode       | No                | No                    | No                   | No                | Partial      | No              |
| HackerRank     | No                | No                    | No                   | No                | No           | No              |
| Codeforces     | No                | Elo (ranking only)    | No                   | No                | No           | No              |
| CodeSignal     | No                | Elo-IRT               | No                   | No                | No           | No              |
| Duolingo       | HLR-based         | Implicit              | Implicit             | FSRS              | No           | No              |
| Khan Academy   | Mastery-based     | Mastery-based         | Implicit             | No                | Khanmigo     | No              |
| ALEKS          | Knowledge Spaces  | Implicit              | Adaptive             | No                | No           | Partial         |
| Carnegie MATHia| BKT-based         | Implicit              | Model-tracing        | No                | No           | No              |
| Knewton Alta   | IRT-based         | IRT                   | Adaptive             | No                | No           | Partial         |
| **This Thesis**\* | **BKT**        | **Dynamic Elo**       | **Hierarchical MAB** | **FSRS**          | **RAG+LLM**  | **Yes**         |

\* *This row represents a proposed system, not yet deployed and validated at scale. All other rows represent production systems.*

The platforms in Table 1.1 were selected based on two criteria: (1) commercial platforms with over one million active users that are widely used for programming practice or adaptive learning, and (2) well-known academic systems from the Intelligent Tutoring Systems and Adaptive Learning literature. The comparison focuses specifically on whether each platform integrates the six adaptive components identified above.

Academic research, similarly, has tended to study these adaptive components in isolation. Knowledge tracing papers evaluate prediction accuracy but do not build recommendation systems around their models. Multi-Armed Bandit papers for education assume fixed difficulty models rather than adaptive ones. The FSRS algorithm was developed for flashcard-based memorization (vocabulary, facts) and has not yet been applied to programming skill retention. Each body of work addresses one aspect of the problem but leaves the integration challenge unresolved.

This thesis aims to address this integration gap by proposing and evaluating a unified adaptive platform that combines all five components into a coherent, closed-loop system.

## 1.3 Research Objectives

The primary aim of this thesis is to design, implement, and evaluate an adaptive learning platform for university programming courses that integrates multiple complementary adaptive techniques into a unified, closed-loop system. The specific objectives are as follows:

**Objective 1: Design a multi-layer adaptive learning architecture for programming courses.**
Propose a modular, five-layer architecture in which each layer addresses a distinct aspect of adaptive instruction: knowledge tracing (Layer 1), difficulty calibration (Layer 2), intelligent problem selection (Layer 3), spaced repetition scheduling (Layer 4), and LLM-powered feedback generation (Layer 5). The architecture must define clear data flows between layers, allowing each to operate independently while contributing to a coherent adaptive pipeline.

**Objective 2: Implement knowledge tracing to model student mastery of programming concepts.**
Implement Bayesian Knowledge Tracing (BKT) to estimate the probability of mastery for each student across each programming concept, using submission outcomes as the primary observation signal. The knowledge tracer provides the foundation for prerequisite-aware recommendations.

**Objective 3: Implement difficulty calibration using Elo ratings for both students and problems.**
Implement a dual Elo rating system with dynamic K-values that continuously calibrates the difficulty of each programming problem relative to each student's ability. Leverage the well-documented relationship between the Elo system and Item Response Theory (IRT) to provide principled difficulty matching grounded in psychometric theory [11].

**Objective 4: Implement intelligent problem selection using Hierarchical Multi-Armed Bandits.**
Implement a two-level Hierarchical Multi-Armed Bandit (H-MAB) algorithm using Thompson Sampling that first selects a concept to study (Level 1) and then selects a specific problem within that concept (Level 2). The selection process must respect knowledge graph prerequisites (concepts are only eligible if all prerequisites are mastered) and Elo-based Zone of Proximal Development (ZPD) constraints (problems must be appropriately challenging for the individual student).

**Objective 5: Implement spaced repetition scheduling for long-term retention of programming concepts.**
Apply the Free Spaced Repetition Scheduler (FSRS) algorithm [12] to programming concept review scheduling --- a novel application domain for FSRS. Design a mapping from code submission outcomes to FSRS review ratings, and integrate the review scheduler with the MAB-based recommendation pipeline so that concepts due for review are prioritized alongside exploration of new material.

**Objective 6: Evaluate the system's effectiveness through a controlled experiment.**
Conduct a between-subjects experiment with pre-test and post-test design, comparing the adaptive platform (experimental group) against the same platform with adaptive features disabled (control group). Evaluate learning effectiveness, recommendation quality, student engagement, and usability.

## 1.4 Research Questions

This thesis addresses four research questions, one primary and three secondary. For comparative questions (RQ2, RQ3), corresponding hypotheses are stated and will be tested at the alpha = 0.05 significance level.

**RQ1 (Primary): How accurately can the multi-layer adaptive system model student knowledge and predict performance?**
This question evaluates the foundational capability of the system's learner model. It is assessed through the prediction accuracy (AUC-ROC) of both the BKT knowledge tracer and the Elo difficulty calibrator, as well as the acceptance rate of recommendations per difficulty band and the convergence speed of Elo ratings. Following established thresholds in educational data mining [11], an AUC-ROC exceeding 0.70 is considered acceptable predictive performance. If the system cannot accurately model what students know and predict how they will perform, the downstream recommendation and scheduling layers cannot function effectively.

**RQ2: Does Hierarchical MAB problem selection improve learning outcomes compared to content-based filtering?**
This question tests the core adaptive recommendation mechanism. It compares the experimental group (H-MAB with BKT prerequisite gating and Elo ZPD filtering) against the control group (content-based filtering using cosine similarity of embedding vectors). The primary metric is Normalized Learning Gain (NLG), supplemented by the problems-to-mastery ratio (how efficiently students achieve concept mastery).
- *H2 (Alternative):* Students in the H-MAB group will achieve significantly higher Normalized Learning Gain than students in the content-based filtering group.
- *H2₀ (Null):* There is no significant difference in Normalized Learning Gain between the two groups.

**RQ3: Does spaced repetition scheduling improve long-term retention of programming concepts?**
This question evaluates the application of FSRS to programming education. It is assessed through a retention test administered two weeks after the intervention period ends, comparing concept recall rates between the experimental group (FSRS-scheduled reviews) and the control group (no scheduled reviews).
- *H3 (Alternative):* Students who receive FSRS-scheduled reviews will demonstrate significantly higher retention scores on the two-week follow-up test than students without scheduled reviews.
- *H3₀ (Null):* There is no significant difference in retention scores between the two groups.

**RQ4: How do students perceive the usability and usefulness of the adaptive platform?**
This qualitative question captures the student experience through the System Usability Scale (SUS) [13], the Technology Acceptance Model (TAM) constructs of Perceived Usefulness and Perceived Ease of Use [14], and semi-structured interviews analyzed using thematic analysis [15].

## 1.5 Proposed Solution

This thesis proposes an Adaptive Learning Platform for University Programming Courses built on a five-layer adaptive engine, unified through a knowledge graph of programming concepts. The system operates as a closed-loop: student interactions produce data that updates the learner model, which in turn influences subsequent recommendations, creating a continuously evolving personalized learning experience.

### 1.5.1 Architecture Overview

The platform extends an existing three-tier web application (React frontend, NestJS API, PostgreSQL database) with a Python-based adaptive engine (FastAPI) comprising five layers:

**Foundation: Knowledge Graph.** A manually curated directed graph of programming concepts (e.g., variables, loops, functions, recursion, dynamic programming) connected by prerequisite edges. Each problem in the database is mapped to one or more concepts. The knowledge graph provides the structural backbone that constrains and coordinates all adaptive layers.

**Layer 1: Knowledge Tracer (Bayesian Knowledge Tracing).** For each (student, concept) pair, BKT maintains a probabilistic estimate of mastery using a Hidden Markov Model [16]. After each submission, the mastery probability is updated via Bayesian inference, enabling prerequisite-gated progression through the knowledge graph.

**Layer 2: Difficulty Calibrator (Dynamic K-Value Elo).** A dual Elo rating system assigns numerical ratings to both students and problems, with ratings updated after each submission based on the match between expected and actual outcomes [17]. This thesis proposes a dynamic K-factor mechanism that adapts based on the student's recent learning trend, drawing on the principles of adaptive Elo systems in educational contexts [11]. This ensures that ratings converge efficiently for all students regardless of their learning phase.

**Layer 3: Problem Selector (Hierarchical Multi-Armed Bandit).** The recommendation engine formulates problem selection as a Hierarchical MAB problem solved via Thompson Sampling [18], [19]. At Level 1, the system selects a concept to study from among those whose prerequisites are met. At Level 2, it selects a specific problem within that concept whose Elo rating falls within the student's Zone of Proximal Development [20], aligning with the desirable difficulty framework [21]. The MAB naturally balances exploitation (practicing concepts with high learning gain) and exploration (trying new concepts to discover strengths and weaknesses).

**Layer 4: Review Scheduler (FSRS).** The Free Spaced Repetition Scheduler tracks memory states per (student, concept) pair, modeling the decay of retrievability over time according to a power-law forgetting curve [12]. When retrievability drops below a threshold, the concept is flagged for review, and the MAB layer prioritizes it in the next recommendation cycle. A key design element is the mapping of code submission outcomes to FSRS review ratings, bridging the gap between FSRS's flashcard-oriented design and the richer signal space of programming exercises. The specific mapping is detailed in Chapter 4.

**Layer 5: LLM Feedback Engine (Optional).** When a student struggles with a problem, a Retrieval-Augmented Generation (RAG) pipeline retrieves relevant context from the knowledge graph and prompts a large language model to generate Socratic hints that guide the student toward the solution without revealing it directly. This layer is supplementary; the core thesis contribution stands on Layers 1 through 4.

The specific parameters, thresholds, and algorithmic details for each layer are presented in Chapter 4.

### 1.5.2 Closed-Loop Workflow

The system operates through a continuous feedback cycle:

1. The student requests a recommendation. The adaptive engine queries the BKT knowledge state, FSRS review queue, and Elo ratings, then runs the Hierarchical MAB to select an optimal problem.
2. The student submits code. The solution is executed in a Docker-based sandbox against test cases.
3. The submission result triggers asynchronous updates to all layers: BKT updates concept mastery, Elo updates student and problem ratings, MAB updates the reward distribution for the selected arm, and FSRS updates the memory state and schedules the next review.
4. The updated learner model influences the next recommendation, completing the loop.

This closed-loop design ensures that the learning experience evolves continuously with the student's progress, maintaining optimal challenge levels and preventing the stagnation that occurs when recommendations are based on static profiles.

## 1.6 Scope and Limitations

### 1.6.1 Scope

This thesis encompasses the following:

- **Subject domain:** Python programming, covering approximately 30 concepts from basic (variables, data types, I/O) through intermediate (functions, recursion, data structures) to advanced (dynamic programming, graph algorithms).
- **Target population:** Undergraduate students at Hanoi University enrolled in programming courses.
- **Platform type:** Web-based application accessible via modern browsers.
- **Adaptive components:** All five layers described in Section 1.5, with Layer 5 (LLM feedback) designated as optional.
- **Evaluation:** A controlled pilot experiment with 40--60 participants over a 4-week intervention period, with a follow-up retention test at Week 8. A formal power analysis (detailed in Chapter 5) indicates that this sample size is sufficient to detect large effect sizes (Cohen's d >= 0.8) at alpha = 0.05 with 80% power; the study is therefore framed as a preliminary assessment rather than a definitive large-scale validation.
- **Ethical considerations:** The experimental protocol will be submitted for review to Hanoi University's academic oversight body. All participants will provide informed consent, participation will be voluntary with no impact on course grades, and student data will be anonymized.

### 1.6.2 Limitations

The following are explicitly outside the scope of this thesis:

- **Multi-language support.** The platform supports Python only. Extension to Java, C++, or JavaScript is left for future work.
- **Mobile application.** The system is designed as a web application; a dedicated mobile application is not included.
- **Real-time collaboration.** Peer programming, collaborative problem-solving, and social features are not implemented.
- **LMS integration.** Integration with institutional learning management systems (e.g., Moodle) is not addressed.
- **Large-scale deployment.** The evaluation is conducted at a single university with a limited sample size (40--60 participants). With approximately 20--30 participants per group, the study is powered to detect only large effect sizes. Generalizability to other institutions and larger populations requires further study with larger samples.
- **Longitudinal evaluation.** The intervention period is limited to four weeks. While this is sufficient for preliminary assessment, a full-semester or full-year study would provide stronger evidence for long-term effects.
- **Cold start limitations.** New students with no submission history receive generic beginner-level recommendations until sufficient interaction data accumulates (approximately 10 submissions).

## 1.7 Contributions

This thesis makes the following contributions to the fields of educational technology and computer science education:

### Research Contributions

**Contribution 1: Integrated multi-layer adaptive architecture (Chapters 3--4).**
To the best of our knowledge, based on a review of the literature (detailed in Chapter 2), no existing system integrates Bayesian Knowledge Tracing, Dynamic K-Value Elo, Hierarchical Multi-Armed Bandits, and FSRS spaced repetition into a unified adaptive pipeline specifically designed for programming education. The architecture defines explicit data flows between layers --- BKT mastery feeds prerequisite gating in the MAB, Elo ratings constrain problem selection to the Zone of Proximal Development, FSRS review urgency interrupts MAB exploration, and the knowledge graph provides structural coherence across all layers. This integration produces emergent adaptive behavior that no single technique achieves alone. The novelty claim is supported by the systematic comparison in Table 1.1 and an extended literature review in Chapter 2, covering databases including Scopus, IEEE Xplore, ACM Digital Library, and Google Scholar.

**Contribution 2: Prerequisite-constrained Hierarchical MAB for problem selection (Chapter 4).**
The thesis proposes a combination of Hierarchical Thompson Sampling with BKT-based prerequisite gating, where a concept is eligible for recommendation only when all its prerequisite concepts have reached a mastery threshold. The reward function --- combining BKT learning gain, difficulty appropriateness, and time efficiency --- is specifically designed for programming exercises. To the best of our knowledge, this integration of knowledge graph constraints with MAB exploration-exploitation optimization has not been previously reported in the literature.

**Contribution 3: FSRS for programming skill retention (Chapter 4).**
To the best of our knowledge, this thesis is the first to apply the FSRS algorithm to programming concept review scheduling. The key innovation lies in the rating mapping that translates programming submission outcomes into FSRS review ratings: a construct that bridges the flashcard-oriented design of FSRS with the richer, multi-dimensional signal space of code submissions. This contribution opens a new application domain for spaced repetition research.

### Practical Contribution

**Contribution 4: Open-source adaptive learning platform (Chapters 3--5).**
The thesis delivers a complete, deployable system --- React frontend, NestJS API backend, FastAPI adaptive engine, PostgreSQL database, Docker-based code execution sandbox --- designed for the Vietnamese university context and released as open-source software. Unlike most adaptive learning research that produces papers but not usable systems, this contribution provides a practical tool that other researchers and institutions can deploy, extend, and build upon.

## 1.8 Thesis Structure

The remainder of this thesis is organized as follows:

**Chapter 2: Literature Review and Theoretical Foundations** surveys the research landscape across six thematic areas: adaptive learning systems, knowledge tracing (from BKT to state-of-the-art Deep Knowledge Tracing), spaced repetition (from Ebbinghaus to FSRS), Multi-Armed Bandits in education, Elo rating systems and Item Response Theory, and knowledge graphs with graph neural networks. The chapter concludes with a gap analysis that positions this thesis within the existing literature.

**Chapter 3: System Requirements and Analysis** defines the functional and non-functional requirements of the platform, presents user personas and use case diagrams, describes the system workflow and data model, and details the proposed five-layer architecture including the knowledge graph foundation, data flow diagrams, database schema design, and API specifications.

**Chapter 4: Design and Implementation** provides the detailed algorithmic design and implementation of each adaptive layer: BKT knowledge tracing with multi-concept extension, Dynamic K-Value Elo with ZPD filtering, Hierarchical MAB with Thompson Sampling, FSRS with the programming-specific rating mapping, and the optional LLM feedback engine. The chapter also covers the technology stack, frontend implementation, and deployment configuration.

**Chapter 5: Experimentation and Evaluation** describes the experimental design (between-subjects, pre-test/post-test with control group), participant recruitment and ethical considerations, evaluation metrics (Normalized Learning Gain, recommendation accuracy, engagement, usability), statistical analysis plan, and results. An ablation study using feature-flag-based layer disabling and interaction log replay provides evidence for each layer's marginal contribution.

**Chapter 6: Conclusion** summarizes the key findings, discusses limitations and practical implications, outlines directions for future research (including multi-language support, DKT2 upgrade, automated knowledge graph construction, and longitudinal evaluation), and offers closing remarks on the broader potential of adaptive learning in programming education.

---

## References

[1]    A. Luxton-Reilly et al., "Introductory programming: A systematic literature review," in *Proc. ITiCSE Companion*, 2018, pp. 55--106, doi: https://doi.org/10.1145/3293881.3295779.

[2]    A. Robins, J. Rountree, and N. Rountree, "Learning and teaching programming: A review and discussion," *Computer Science Education*, vol. 13, no. 2, pp. 137--172, 2003, doi: https://doi.org/10.1076/csed.13.2.137.14200.

[3]    J. R. Anderson, C. F. Boyle, and B. J. Reiser, "Intelligent tutoring systems," *Science*, vol. 228, no. 4698, pp. 456--462, 1985, doi: https://doi.org/10.1126/science.228.4698.456.

[4]    T. T. Nguyen, H. Q. Le, and T. H. Pham, "Challenges and solutions for teaching programming in Vietnamese universities," *Journal of Science, Hanoi National University of Education*, vol. 67, no. 4, pp. 120--132, 2022. (in Vietnamese)

[5]    C. Watson and F. W. B. Li, "Failure rates in introductory programming revisited," in *Proc. ITiCSE*, 2014, pp. 39--44, doi: https://doi.org/10.1145/2591708.2591749.

[6]    P. Brusilovsky, "Adaptive hypermedia," *User Modeling and User-Adapted Interaction*, vol. 11, no. 1--2, pp. 87--110, 2001, doi: https://doi.org/10.1023/A:1011143116306.

[7]    A. Paramythis and S. Loidl-Reisinger, "Adaptive learning environments and e-learning standards," *Electronic Journal of e-Learning*, vol. 2, no. 1, pp. 181--194, 2004.

[8]    S. Ritter, J. R. Anderson, K. R. Koedinger, and A. Corbett, "Cognitive Tutor: Applied research in mathematics education," *Psychonomic Bulletin & Review*, vol. 14, no. 2, pp. 249--255, 2007, doi: https://doi.org/10.3758/BF03194060.

[9]    J.-P. Doignon and J.-C. Falmagne, *Knowledge Spaces*. Berlin: Springer-Verlag, 1999, doi: https://doi.org/10.1007/978-3-642-58625-5.

[10]   B. Settles and B. Meeder, "A trainable spaced repetition model for language learning," in *Proc. ACL*, 2016, pp. 1848--1858, doi: https://doi.org/10.18653/v1/P16-1174.

[11]   R. Pelanek, "Applications of the Elo rating system in adaptive educational systems," *Computers & Education*, vol. 98, pp. 169--179, 2016, doi: https://doi.org/10.1016/j.compedu.2016.03.015.

[12]   J. Ye, "A stochastic shortest path algorithm for optimizing spaced repetition scheduling," in *Proc. SIGKDD*, 2023, doi: https://doi.org/10.1145/3580305.3599922.

[13]   J. Brooke, "SUS: A 'quick and dirty' usability scale," in *Usability Evaluation in Industry*, P. W. Jordan et al., Eds. London: Taylor & Francis, 1996, pp. 189--194.

[14]   F. D. Davis, "Perceived usefulness, perceived ease of use, and user acceptance of information technology," *MIS Quarterly*, vol. 13, no. 3, pp. 319--340, 1989, doi: https://doi.org/10.2307/249008.

[15]   V. Braun and V. Clarke, "Using thematic analysis in psychology," *Qualitative Research in Psychology*, vol. 3, no. 2, pp. 77--101, 2006, doi: https://doi.org/10.1191/1478088706qp063oa.

[16]   A. T. Corbett and J. R. Anderson, "Knowledge tracing: Modeling the acquisition of procedural knowledge," *User Modeling and User-Adapted Interaction*, vol. 4, no. 4, pp. 253--278, 1994, doi: https://doi.org/10.1007/BF01099821.

[17]   A. E. Elo, *The Rating of Chessplayers, Past and Present*. New York: Arco, 1978.

[18]   W. R. Thompson, "On the likelihood that one unknown probability exceeds another in view of the evidence of two samples," *Biometrika*, vol. 25, no. 3--4, pp. 285--294, 1933, doi: https://doi.org/10.2307/2332286.

[19]   D. Russo, B. Van Roy, A. Kazerouni, I. Osband, and Z. Wen, "A tutorial on Thompson Sampling," *Foundations and Trends in Machine Learning*, vol. 11, no. 1, pp. 1--96, 2018, doi: https://doi.org/10.1561/2200000070.

[20]   L. S. Vygotsky, *Mind in Society: The Development of Higher Psychological Processes*. Cambridge, MA: Harvard University Press, 1978.

[21]   R. A. Bjork and E. L. Bjork, "Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning," in *Psychology and the Real World*, M. A. Gernsbacher et al., Eds. New York: Worth, 2011, pp. 56--64.
