# Chapter 3: System Requirements and Architecture

Chapter 2 identified three critical gaps in the literature: the absence of an integrated multi-layer adaptive architecture for programming education, the lack of spaced repetition applied to procedural programming skills, and the insufficient adaptive sophistication of existing platforms. This chapter translates those findings into concrete system requirements and a detailed architectural design that addresses all three gaps.

Section 3.1 defines the functional and non-functional requirements derived from the research objectives stated in Chapter 1 and the theoretical principles surveyed in Chapter 2. Section 3.2 describes the overall system architecture and the design principles that guided its construction. Section 3.3 presents the five-layer adaptive architecture that forms the core contribution of this thesis, describing each layer's role, inputs, outputs, and interactions. Section 3.4 details the data flows for the two primary operations: recommendation generation and submission processing. Section 3.5 specifies the database schema that supports the adaptive layers. Section 3.6 defines the API design for both the AI service and the NestJS gateway. Finally, Section 3.7 describes the caching strategy that ensures acceptable response times under concurrent load.

## 3.1 Requirements Analysis

The requirements for the adaptive learning platform are derived from three sources: the six research objectives defined in Section 1.3, the theoretical principles established in Chapter 2, and practical constraints of the university deployment context. This section formalizes these requirements into functional requirements (what the system must do), non-functional requirements (how well the system must perform), and use cases (how actors interact with the system).

### 3.1.1 Functional Requirements

The functional requirements are organized into three categories: core platform capabilities that the system must provide, adaptive capabilities that constitute the novel contributions, and analytics capabilities that support evaluation.

**Core Platform Capabilities.**

**FR1: User authentication and role management.** The system shall support three roles --- student, instructor, and administrator --- each with distinct permissions. Students can submit code and receive recommendations. Instructors can create and manage problems, test cases, courses, and view class-level analytics. Administrators can manage all entities including the knowledge graph. Authentication shall use JSON Web Tokens (JWT) with role-based access control.

**FR2: Problem management with test cases and concept tagging.** The system shall allow instructors to create programming problems with descriptions, starter code templates, and associated test cases. Each problem shall be tagged with one or more concepts from the knowledge graph, with one concept designated as the primary concept. Problems shall carry a static difficulty label (EASY, MEDIUM, HARD) for initial Elo calibration, though the dynamic Elo rating supersedes this label after sufficient submissions.

**FR3: Sandboxed code execution.** The system shall execute student-submitted code in a Docker-based sandbox environment, evaluating correctness against test cases and returning results within a bounded time. The sandbox shall enforce strict isolation: no network access, memory limits, and CPU time limits to prevent both accidental infinite loops and deliberate resource abuse.

**Adaptive Capabilities.**

**FR4: Knowledge tracing.** The system shall maintain a probabilistic mastery estimate $P(L_t)$ for each (student, concept) pair using Bayesian Knowledge Tracing [16]. After each graded submission, the mastery probability shall be updated via Bayesian inference. Concepts with $P(L_t) \geq 0.85$ shall be classified as mastered for the purpose of prerequisite gating.

**FR5: Difficulty calibration.** The system shall maintain Elo ratings for both students and problems [17], updating ratings after each submission based on the discrepancy between expected and actual outcomes. The K-factor shall be dynamically adjusted based on the student's recent performance trend and the number of prior interactions, following the adaptive K-value approach described by Pelanek [11].

**FR6: Adaptive problem selection.** The system shall recommend problems using a Hierarchical Multi-Armed Bandit with Thompson Sampling [18], [19]. At Level 1, the bandit selects a concept from among those whose prerequisites are satisfied (prerequisite gating). At Level 2, the bandit selects a specific problem within that concept whose Elo rating falls within the student's Zone of Proximal Development [20]. The recommendation pipeline shall also integrate FSRS review urgency, prioritizing concepts whose retrievability has dropped below a threshold.

**FR7: Review scheduling.** The system shall track memory states per (student, concept) pair using the FSRS algorithm [12]. When a concept's estimated retrievability drops below a configurable threshold (default 0.7), it shall be flagged for review. Reviewing a concept means solving a new problem tagged with that concept, not simply displaying a definition --- preserving the retrieval practice effect [21].

**FR8: Progress dashboard with skill visualization.** The system shall provide students with a visual dashboard displaying mastery probabilities across concepts, Elo rating trajectory, upcoming review schedule, and submission history. Instructors shall have access to class-level aggregate views showing concept mastery distributions and common struggle points.

**FR9: Hint generation (optional).** When a student has made multiple unsuccessful attempts on a problem, the system shall optionally generate Socratic hints using a Retrieval-Augmented Generation pipeline that incorporates the knowledge graph and problem context. This requirement is designated as optional; the core thesis contribution is independent of its implementation.

**Analytics Capabilities.**

**FR10: Event logging for evaluation.** The system shall log all educationally significant events --- submissions, recommendations served, recommendations accepted or skipped, review completions, hint requests --- with timestamps and session identifiers. This data supports the experimental evaluation described in Chapter 5.

**FR11: Experiment group management.** The system shall support assignment of students to experiment groups (adaptive vs. control) to facilitate between-subjects evaluation. Students in the control group shall receive content-based filtering recommendations; students in the adaptive group shall receive the full five-layer pipeline.

### 3.1.2 Non-Functional Requirements

**NFR1: Code execution latency.** Submitted code shall be executed and results returned within 5 seconds for typical problems, measured from submission receipt to result availability. This constraint bounds the Docker sandbox timeout and influences the choice of execution strategy (pre-warmed containers vs. cold start).

**NFR2: Recommendation latency.** The adaptive recommendation pipeline --- from receipt of the recommendation request to delivery of the ranked problem list --- shall complete within 500 milliseconds. This target necessitates the caching strategy described in Section 3.7, since the full pipeline involves loading knowledge states, Elo ratings, FSRS cards, and knowledge graph structure, followed by running the Hierarchical MAB sampling algorithm.

**NFR3: Concurrent user support.** The system shall support at least 100 concurrent active users without degradation of response times beyond the thresholds specified in NFR1 and NFR2. This target reflects the expected class size for the pilot evaluation (40--60 students) with a safety margin for instructor activity and concurrent sessions. The AI service is designed as a stateless FastAPI application that can be horizontally scaled to support larger deployments. For the purposes of this thesis, the 100-user target is sufficient for the pilot evaluation.

**NFR4: Execution security.** The Docker sandbox shall enforce strict isolation. Containers shall have no network access, shall be limited to 256 MB of memory and 5 seconds of CPU time, and shall run as unprivileged users. The sandbox configuration shall prevent fork bombs, filesystem escape, and inter-container communication.

**NFR5: Architectural extensibility.** The adaptive engine shall be designed such that individual layers can be replaced or upgraded independently. For example, replacing BKT with DKT2 [35] in Layer 1 shall require changes only to the knowledge tracing module, without affecting the Elo, MAB, or FSRS layers. This modularity is achieved through strict interface contracts between layers.

### 3.1.3 Use Case Diagram

The system involves three primary actors --- Student, Instructor, and Administrator --- interacting with two subsystems: the core platform and the adaptive engine. The following diagram summarizes the key use cases.

```
+------------------------------------------------------------------+
|                    Adaptive Learning Platform                     |
|                                                                  |
|  +--------------------+       +-----------------------------+    |
|  |   Core Platform    |       |     Adaptive Engine         |    |
|  |                    |       |                             |    |
|  |  UC1: Register/    |       |  UC6: Get Adaptive          |    |
|  |       Login        |       |       Recommendation        |    |
|  |  UC2: Browse       |       |  UC7: View Knowledge        |    |
|  |       Problems     |       |       State Dashboard       |    |
|  |  UC3: Submit Code  |------>|  UC8: Get Review Queue      |    |
|  |  UC4: View Results |       |  UC9: Request Hint          |    |
|  |  UC5: Enroll in    |       |  UC10: Process Submission   |    |
|  |       Course       |       |        (async update)       |    |
|  +--------------------+       +-----------------------------+    |
|                                                                  |
|  +--------------------+       +-----------------------------+    |
|  |   Management       |       |     Analytics               |    |
|  |                    |       |                             |    |
|  |  UC11: Manage      |       |  UC14: View Student         |    |
|  |        Problems    |       |        Progress             |    |
|  |  UC12: Manage      |       |  UC15: View Class           |    |
|  |        Knowledge   |       |        Analytics            |    |
|  |        Graph       |       |  UC16: Export Experiment    |    |
|  |  UC13: Manage      |       |        Data                 |    |
|  |        Courses     |       |                             |    |
|  +--------------------+       +-----------------------------+    |
+------------------------------------------------------------------+

Actors:
  Student ----> UC1, UC2, UC3, UC4, UC5, UC6, UC7, UC8, UC9
  Instructor -> UC1, UC2, UC11, UC12, UC13, UC14, UC15
  Admin ------> UC1, UC11, UC12, UC13, UC15, UC16
```

**UC6 (Get Adaptive Recommendation)** is the central use case that distinguishes this platform from a conventional online judge. The student requests a recommendation, which triggers the full adaptive pipeline: the knowledge tracer provides mastery estimates, the difficulty calibrator provides Elo ratings, the review scheduler flags overdue concepts, and the problem selector synthesizes these inputs into a ranked list of problems tailored to the student's current state. This use case depends on UC3 (Submit Code) having been executed at least once to provide behavioral data, though a cold-start fallback handles new students with no submission history (detailed in Section 3.4.3).

**UC10 (Process Submission)** is triggered asynchronously after every code submission (UC3). It is not directly initiated by the student but is essential to the adaptive loop: submission results flow through all four adaptive layers, updating the student's knowledge state, Elo ratings, MAB reward distributions, and FSRS memory parameters. Without this asynchronous processing, the adaptive engine would operate on stale data.

### 3.1.4 Requirements Traceability

Table 3.2 traces each requirement to the architectural components that implement it, the sections in this chapter where the design is specified, the implementation sections in Chapter 4, and the evaluation metrics used to verify it.

**Table 3.2.** Requirements traceability matrix.

| Requirement | Architectural Component | Ch. 3 Section | Ch. 4 Section | Evaluation Metric |
|-------------|------------------------|---------------|---------------|-------------------|
| FR1 | NestJS Auth Module, JWT | 3.6.2 | 4.1 | — |
| FR2 | NestJS Problem Module, KG | 3.3.7, 3.5 | 4.1 | — |
| FR3 | Docker Sandbox | 3.2 | 4.1 | NFR1 (latency) |
| FR4 | Layer 1: BKT | 3.3.2 | 4.2.1 | AUC, RMSE (RQ1) |
| FR5 | Layer 2: Dynamic Elo | 3.3.3 | 4.2.2 | Rating stability (RQ1) |
| FR6 | Layer 3: Hierarchical MAB | 3.3.4, 3.4.1 | 4.2.3 | Learning gain (RQ2) |
| FR7 | Layer 4: FSRS | 3.3.5 | 4.2.4 | Retention rate (RQ3) |
| FR8 | Dashboard (React + API) | 3.6.2 | 4.3 | SUS score (RQ4) |
| FR9 | Layer 5: LLM Feedback | 3.3.6 | 4.2.5 | — (optional) |
| FR10 | Event Logs table | 3.5.1 | 4.4 | — |
| FR11 | Experiment Groups table | 3.5.1 | 4.4 | Between-group effect size |
| NFR1 | Docker resource limits | 3.2 | 4.1 | p95 execution time |
| NFR2 | Redis caching, pipeline | 3.7 | 4.5 | p95 recommendation latency |
| NFR3 | Stateless AI service | 3.3.1 | 4.5 | Load test throughput |
| NFR4 | Sandbox isolation config | 3.2 | 4.1 | Security audit checklist |
| NFR5 | Layer interfaces | 3.3.1 | 4.2 | Interface contract tests |

## 3.2 System Overview and Design Rationale

This section describes the overall architecture of the adaptive learning platform and the design principles that guided its construction. The platform is a purpose-built system designed from the ground up to support adaptive programming education at the university level. Rather than retrofitting adaptive capabilities onto a generic online judge, the architecture was conceived as an integrated whole in which every component --- from the frontend code editor to the backend AI service --- is designed with adaptive learning as a first-class concern.

### 3.2.1 Four-Component Architecture

The platform comprises four principal components, each selected to fulfill a specific role in the adaptive learning pipeline.

**React + TypeScript Frontend (Vite, Ant Design, Monaco Editor).** The client application provides the student-facing interface: a Monaco-based code editor for writing and submitting solutions, a problem browser with concept-based navigation, an adaptive dashboard displaying mastery progress and Elo ratings, and a review queue surfacing concepts due for spaced repetition practice. Vite is used as the build tool for fast development iteration and optimized production bundles. Ant Design provides a consistent, accessible component library suited to data-rich educational interfaces.

**NestJS API Gateway (TypeScript, Prisma ORM).** The API gateway handles authentication (JWT-based), user and course management, problem CRUD operations, and code execution orchestration. When a student submits code, the gateway saves the submission, dispatches it to the Docker sandbox, and returns the execution result. For adaptive features, the gateway acts as a proxy to the FastAPI AI service, forwarding recommendation and update requests while shielding the frontend from the AI service's internal API. Prisma serves as the ORM, providing type-safe database access and version-controlled schema migrations.

**FastAPI AI Service (Python 3.11, SQLAlchemy).** The AI service hosts the five-layer adaptive engine: Bayesian Knowledge Tracing (Layer 1), Dynamic Elo rating (Layer 2), Hierarchical Multi-Armed Bandits with Thompson Sampling (Layer 3), FSRS spaced repetition scheduling (Layer 4), and LLM-based feedback generation (Layer 5). Python was selected for this component because the machine learning ecosystem --- including pyBKT [56], NumPy, SciPy, and the FSRS algorithm library --- is implemented primarily in Python. FastAPI's asynchronous request handling supports high-throughput recommendation serving, and SQLAlchemy provides direct database access for the adaptive state tables that the AI service owns.

**PostgreSQL (pgvector) + Redis + Docker Sandbox.** PostgreSQL serves as the sole persistent store, with the pgvector extension reserved for future embedding-based features (e.g., semantic similarity in hint retrieval). Its mature JSONB support enables flexible storage of rating history and event metadata. Redis provides a caching layer for recommendation results and MAB state reads, as well as per-student distributed locks that prevent concurrent update races. Docker containers provide isolated sandboxes for executing student-submitted code, with CPU, memory, and time limits enforced at the container level to satisfy security and fairness requirements (NFR4).

### 3.2.2 Design Principles and Key Decisions

Six design principles guided the architecture. Each principle maps to one or more concrete architectural decisions, as summarized in Table 3.1.

The most consequential decision is the **separation of the AI service** from the NestJS gateway. This separation allows the Python ML ecosystem (pyBKT [56], NumPy, SciPy, FSRS) to be used natively, enables independent scaling and deployment of the adaptive engine, and enforces a clean interface contract between platform logic and adaptive intelligence. The **write-ownership convention** complements this separation: the NestJS gateway owns writes to core domain tables, while the AI service owns writes to adaptive state tables, eliminating the need for distributed transactions. **Asynchronous adaptive updates** further decouple the two services: submission results are returned to the student synchronously, while adaptive state updates (BKT, Elo, MAB, FSRS) are processed in the background. Redis provides both **caching** (to meet the 500ms recommendation latency target, NFR2) and **per-student distributed locks** (to serialize concurrent adaptive updates). If Redis is unavailable, the system degrades gracefully to direct database queries.

**Table 3.1.** Design principles and corresponding architectural decisions.

| Design Principle | Rationale | Architectural Decision |
|-----------------|-----------|----------------------|
| Separation of concerns | Adaptive intelligence involves different expertise, tooling, and release cadence than platform logic | Dedicated FastAPI AI service for adaptive layers; NestJS gateway for platform operations |
| Write ownership | Concurrent writes to shared tables from multiple services risk data corruption without distributed transactions | Each table is written by exactly one service; both services read all tables |
| Asynchronous adaptive updates | Adaptive computation (BKT inference, Elo update, MAB sampling) should not block the student's submission response | Submission result returned synchronously; adaptive pipeline triggered asynchronously |
| Caching and concurrency safety | Recommendation latency must remain below 500ms (NFR2); concurrent submissions for the same student must not corrupt state | Redis caches adaptive state reads; Redis distributed locks serialize per-student updates |
| Progressive enhancement | The platform should remain functional as a standard online judge even if adaptive features are disabled or degraded | Each adaptive layer is independently enable-able; the submission pipeline does not depend on AI service availability |
| Security by isolation | Arbitrary student code must not compromise the host system or other students' data | Docker sandbox with disabled networking, resource caps, and ephemeral containers |

The progressive enhancement principle deserves additional emphasis. The platform is designed so that its core functionality --- problem browsing, code submission, execution, and verdict display --- operates independently of the adaptive engine. Each adaptive layer adds a capability (mastery tracking, difficulty calibration, intelligent selection, review scheduling, hint generation) that can be independently enabled or disabled via feature flags. This design ensures that a partial failure in the AI service does not prevent students from practicing, and it simplifies evaluation by allowing controlled comparisons between adaptive and non-adaptive conditions.

## 3.3 Proposed Five-Layer Adaptive Architecture

This section presents the five-layer adaptive architecture that constitutes the primary contribution of this thesis. The architecture is designed around three principles: *modularity*, where each layer encapsulates a single adaptive concern and communicates through well-defined interfaces; *composability*, where layers build upon each other's outputs to produce adaptive behavior that exceeds what any single layer achieves in isolation; and *extensibility*, where any layer can be replaced with an alternative algorithm without disrupting the overall pipeline (NFR5).

### 3.3.1 Architecture Overview

The adaptive engine operates as a service within the platform's four-component architecture described in Section 3.2. It runs as a FastAPI application alongside the NestJS backend, with both services sharing the same PostgreSQL database under a strict write-ownership model: the NestJS backend owns writes to core tables (users, problems, test cases, submissions, courses, concepts, knowledge graph edges, problem-concept mappings), while the AI service owns writes to adaptive state tables (knowledge states, Elo ratings, MAB states, FSRS cards, event logs). Both services have read access to all tables. Redis is introduced as a caching layer between the two services.

```
+----------------------------------------------------------------------+
|                         Client (React + TypeScript)                   |
|  +-------------+  +-----------+  +-----------+  +----------------+   |
|  | Code Editor |  | Dashboard |  | Problems  |  | Review Queue   |   |
+------+---+------+--+-----+-----+--+-----+-----+--+-------+--------+-+
       |   |              |              |                  |
       |   +--------------+--------------+------------------+
       |                  | REST API (HTTPS)
+------v------------------v--------------------------------------------+
|                     NestJS API Gateway                               |
|  +----------+  +----------+  +---------+  +----------+  +--------+  |
|  |   Auth   |  | Problems |  | Submit  |  | Adaptive |  |Analytics| |
|  |  Module  |  |  Module  |  | Module  |  |  Proxy   |  | Module | |
+--+-----+----+--+----+-----+--+---+-----+--+----+-----+--+---+----+-+
         |             |            |              |            |
         +-----+-------+-----+-----+-------+------+-----+-----+
               |              |             |            |
         +-----v--------------v------+------v------------v-----+
         |        PostgreSQL         |         Redis           |
         |  (pgvector extension)     |   (Caching Layer)       |
         +-----+-----^--------------+------^---+---^-----------+
               |     |                     |   |   |
   +-----------v-----+-----+-----------+---+---v---+-----------+
   |              FastAPI AI Service (Python)                   |
   |                                                           |
   |  +-----------------------------------------------------+ |
   |  | Layer 5: LLM Feedback Engine (RAG + KG + LLM)       | |
   |  |   [Optional — Socratic hint generation]              | |
   |  +-----------------------------------------------------+ |
   |  | Layer 4: Review Scheduler (FSRS)                     | |
   |  |   [Memory modeling, review scheduling]               | |
   |  +-----------------------------------------------------+ |
   |  | Layer 3: Problem Selector (Hierarchical MAB)         | |
   |  |   [Thompson Sampling, concept + problem selection]   | |
   |  +-----------------------------------------------------+ |
   |  | Layer 2: Difficulty Calibrator (Dynamic K-Value Elo) | |
   |  |   [Student + problem rating, ZPD filtering]          | |
   |  +-----------------------------------------------------+ |
   |  | Layer 1: Knowledge Tracer (BKT)                      | |
   |  |   [Per-concept mastery estimation]                   | |
   |  +-----------------------------------------------------+ |
   |  |          Knowledge Graph Foundation                  | |
   |  |   [Concept DAG, prerequisite edges, topology]        | |
   |  +-----------------------------------------------------+ |
   +-----------+-----------------------------------------------+
               |
   +-----------v-----------+
   |   Docker Sandbox      |
   |   (Code Execution)    |
   +-----------------------+
```

[Figure 3.1: Five-layer adaptive architecture within the four-component platform.]

The layered structure in Figure 3.1 reflects a logical dependency ordering from bottom to top. The Knowledge Graph Foundation provides structural information (concept nodes, prerequisite edges) that all layers consume. Layer 1 (BKT) consumes submission outcomes and produces mastery estimates. Layer 2 (Elo) consumes submission outcomes and produces difficulty ratings on a shared scale. Layer 3 (MAB) consumes the outputs of Layers 1, 2, and 4 to select problems. Layer 4 (FSRS) consumes submission outcomes and produces review scheduling information that Layer 3 respects. Layer 5 (LLM) operates independently, triggered on demand when students request hints. The following subsections describe each component in detail.

### 3.3.2 Layer 1: Knowledge Tracer (BKT)

**Purpose.** Layer 1 maintains a probabilistic estimate of each student's mastery of each programming concept. This estimate serves two critical downstream functions: (1) prerequisite gating, where a concept becomes eligible for recommendation only when all its prerequisites have mastery probability exceeding the mastery threshold $\theta_m = 0.85$; and (2) reward signal computation for the MAB, where learning gain is defined as the change in mastery probability resulting from a practice opportunity.

**Model.** The Knowledge Tracer implements standard Bayesian Knowledge Tracing [16] as described in Section 2.2.1. For each (student, concept) pair, the model maintains four parameters --- $P(L_0)$, $P(T)$, $P(G)$, $P(S)$ --- and the current mastery estimate $P(L_t)$. Parameters are initialized with concept-level defaults: $P(L_0) = 0.1$, $P(T) = 0.2$, $P(G) = 0.15$, $P(S) = 0.1$. These values are drawn from Corbett and Anderson's original BKT formulation [16] and are consistent with the defaults used in pyBKT [56], the standard open-source BKT implementation. The specific values reflect typical introductory programming exercises where prior knowledge is low, learning per opportunity is moderate, and guessing rates are constrained by the multi-test-case evaluation format.

**Mastery threshold.** The mastery threshold $\theta_m = 0.85$ was selected based on standard practice in BKT implementations, where mastery at or above 0.80--0.90 is recommended for prerequisite gating [16]. A threshold of 0.95 would require excessive practice on already-understood concepts, while 0.70 risks advancing students prematurely. The sensitivity of this threshold will be evaluated in Section 5.5.

**Input.** After each graded submission, Layer 1 receives the student identifier, the concept identifier (derived from the problem's primary concept tag), and a binary correctness signal (1 if ACCEPTED, 0 otherwise).

**Output.** The updated mastery probability $P(L_t)$, which is written to the `knowledge_states` table and made available to Layers 3 and 4.

**Interaction with other layers.** Layer 1 feeds Layer 3 in two ways. First, the binary mastery classification ($P(L_t) \geq 0.85$ = mastered) determines which concepts are eligible at the MAB's Level 1 by enabling their dependents. If concept B requires concept A as a prerequisite, then B becomes eligible only when $P(L_t^A) \geq 0.85$. Second, the change in mastery probability $\Delta P(L_t) = P(L_t) - P(L_{t-1})$ serves as the reward signal for the MAB: concepts that produce larger mastery gains are more likely to be selected in the future. Layer 1 also triggers Layer 4: when a concept first reaches mastery ($P(L_t) \geq 0.85$), an FSRS card is initialized for that concept, beginning the spaced repetition cycle.

### 3.3.3 Layer 2: Difficulty Calibrator (Dynamic Elo)

**Purpose.** Layer 2 maintains numerical ratings for both students and problems on a shared scale, enabling principled difficulty matching. By placing students and problems on the same rating scale, the system can operationalize Vygotsky's Zone of Proximal Development [20] as a numerical interval: problems whose rating falls within a calibrated range above the student's rating are considered to be within the student's ZPD.

**Model.** The Difficulty Calibrator implements a dual Elo rating system [17] with dynamic K-values [11]. Each student and each problem maintains a rating (initialized at 1200) and a K-factor that controls the sensitivity of rating updates. The expected probability that student $A$ with rating $R_A$ solves problem $B$ with rating $R_B$ is:

$$E(A) = \frac{1}{1 + 10^{(R_B - R_A) / 400}} \tag{3.1}$$

After a submission, ratings are updated based on the discrepancy between expected and actual outcomes:

$$R_A' = R_A + K_A \cdot (S_A - E(A)) \tag{3.2}$$
$$R_B' = R_B + K_B \cdot (E(A) - S_A) \tag{3.3}$$

where $S_A = 1$ if the student solved the problem (ACCEPTED) and $S_A = 0$ otherwise. The student's K-factor is dynamically adjusted based on two criteria: the number of prior attempts (higher K for newer students to allow rapid convergence) and the recent performance trend (higher K for students on a steep learning curve, lower K for stable performers). Specifically:

$$K_A = K_{\text{base}} \cdot f_{\text{novelty}}(n) \cdot f_{\text{trend}}(\text{trend}_A) \tag{3.4}$$

where $K_{\text{base}} = 25$. Elo [17] originally recommended K = 32 for new players and K = 16 for established players in chess; the base value of 25 is chosen as a midpoint suitable for the educational context, where rating volatility should be moderate. The function $f_{\text{novelty}}(n) = \max(1.0, 2.0 - n/30)$ provides a boost for students with fewer than 30 interactions, and $f_{\text{trend}}$ scales K based on the exponential moving average of recent rating changes. Problem K-factors follow an analogous formula but with $f_{\text{novelty}}$ based on the number of submissions the problem has received.

**Input.** After each graded submission, Layer 2 receives the student identifier, problem identifier, and the binary outcome.

**Output.** Updated student and problem Elo ratings, written to the `elo_ratings` table.

**Interaction with other layers.** Layer 2 feeds Layer 3 by defining the ZPD filter. When the MAB at Level 2 considers candidate problems within a selected concept, only problems whose Elo rating satisfies the following condition are eligible:

$$R_{\text{student}} + \delta_{\min} \leq R_{\text{problem}} \leq R_{\text{student}} + \delta_{\max} \tag{3.5}$$

where $\delta_{\min} = 50$ and $\delta_{\max} = 250$ are hyperparameters. These bounds are derived from the expected success probability in Equation 3.1: substituting $\delta_{\min} = 50$ yields $E(A) \approx 0.43$, while $\delta_{\max} = 250$ yields $E(A) \approx 0.15$. After accounting for the asymmetric nature of educational gains (students learn more from moderately challenging tasks), these bounds approximate the 36--64% success rate range recommended by flow theory [57] and the "desirable difficulty" framework [21]. The exact values will be validated through sensitivity analysis in Section 5.5.

### 3.3.4 Layer 3: Problem Selector (Hierarchical MAB)

**Purpose.** Layer 3 is the recommendation engine. It formulates problem selection as a two-level Hierarchical Multi-Armed Bandit (H-MAB) problem and solves it using Thompson Sampling [18], [19]. The hierarchical structure reflects the natural two-step decision process in programming education: first, decide *which concept* the student should practice; then, decide *which specific problem* within that concept is optimal.

**Model.** The H-MAB operates at two levels:

*Level 1 (Concept Selection).* Each eligible concept constitutes an arm. An arm is eligible if and only if: (a) all prerequisite concepts have been mastered ($P(L_t) \geq 0.85$ for each prerequisite, checked against Layer 1), and (b) the concept itself is not yet mastered ($P(L_t) < 0.85$) OR the concept is flagged for review by Layer 4 (FSRS retrievability below threshold). For each eligible arm, the bandit maintains a Beta distribution $\text{Beta}(\alpha_c, \beta_c)$ modeling the expected learning gain. Thompson Sampling draws a sample $\theta_c \sim \text{Beta}(\alpha_c, \beta_c)$ for each eligible concept and selects the concept with the highest sampled value.

*Level 2 (Problem Selection).* Within the selected concept, each unsolved problem whose Elo rating falls within the student's ZPD (Equation 3.5) constitutes an arm. Each arm maintains a Beta distribution $\text{Beta}(\alpha_p, \beta_p)$. Thompson Sampling again draws samples and selects the problem with the highest sampled value.

**Reward Signal.** After the student submits a solution, the reward is computed as a composite signal:

$$r = w_1 \cdot \Delta P(L_t) + w_2 \cdot \mathbb{1}[\text{correct}] + w_3 \cdot (1 - \text{normalized\_attempts}) \tag{3.6}$$

where $\Delta P(L_t)$ is the learning gain from Layer 1, $\mathbb{1}[\text{correct}]$ is the binary correctness indicator, and $\text{normalized\_attempts} = \min(\text{attempt\_number}, M) / M$, where $M = 5$ is a configurable cap beyond which the attempt penalty is saturated. The weights $w_1 = 0.5$, $w_2 = 0.3$, $w_3 = 0.2$ are initial values selected to prioritize learning gain as the primary optimization objective. These weights will be tuned via grid search during the evaluation phase described in Section 5.5.

The reward $r$ is clipped to the interval $[0, 1]$ before updating the Beta distribution parameters to ensure mathematical validity. While Thompson Sampling's convergence guarantees were originally proved for Bernoulli rewards [18], using a continuous reward $r \in [0, 1]$ with Beta priors is a well-established approximation that retains favorable empirical performance [58]. The Beta parameters are updated: $\alpha \leftarrow \alpha + r$ and $\beta \leftarrow \beta + (1 - r)$.

**Interaction with other layers.** Layer 3 is the integration point where all other layers converge. It consumes: mastery estimates and prerequisite gating from Layer 1 (BKT), ZPD constraints from Layer 2 (Elo), review urgency from Layer 4 (FSRS), and structural information from the Knowledge Graph Foundation. The integration of FSRS with the MAB deserves particular attention: when concepts are due for review, they are injected into the Level 1 candidate set with a priority boost to their Thompson Sampling prior, ensuring that review needs are addressed without entirely overriding exploration of new material.

The specific combination of prerequisite constraints derived from a knowledge graph, BKT-based mastery gating, and FSRS review urgency within a hierarchical Thompson Sampling framework has not, to the best of our knowledge, been previously reported. While Multi-Armed Bandits have been applied to educational recommendation before --- notably by Clement et al. [22] --- the integration of these four components into a single hierarchical decision process is the second key contribution of this thesis.

### 3.3.5 Layer 4: Review Scheduler (FSRS)

**Purpose.** Layer 4 addresses the forgetting problem (W4) by modeling memory decay for each mastered concept and scheduling timely reviews to maintain long-term retention. To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis.

**Model.** The implementation is based on FSRS v4 [12], whose power-law retrievability decay has been empirically validated against the SM-2 algorithm on large-scale flashcard datasets. FSRS models each (student, concept) pair as a memory card with two state variables: *difficulty* $D \in [1, 10]$ (how inherently hard the concept is for this student) and *stability* $S$ (the time interval, in days, at which retrievability drops to 90%). The retrievability at time $t$ after the last review is:

$$R(t) = \left(1 + \frac{t}{9 \cdot S}\right)^{-1} \tag{3.7}$$

The rating mapping described in this chapter represents the primary adaptation of FSRS to the programming domain. When the student reviews a concept (by solving a problem tagged with that concept), the FSRS algorithm updates both difficulty and stability based on the review outcome. The review outcome is expressed as a rating from 1 (complete failure) to 4 (effortless recall), which requires a mapping from code submission outcomes to FSRS ratings --- a mapping detailed in Chapter 4.

**Input.** After a submission on a mastered concept, Layer 4 receives the student identifier, concept identifier, and a submission-derived FSRS rating.

**Output.** Updated FSRS card parameters (difficulty, stability, retrievability, due date), written to the `fsrs_cards` table. Concepts whose retrievability has dropped below the review threshold $\theta_r = 0.7$ are flagged as due for review.

**Interaction with other layers.** Layer 4 feeds Layer 3 by identifying concepts that need review. The MAB treats review-due concepts as eligible arms at Level 1 even if they are already mastered ($P(L_t) \geq 0.85$), with a priority boost proportional to the urgency of the review (how far below $\theta_r$ the retrievability has dropped). This integration ensures that the system balances three competing objectives: advancing to new concepts (exploitation), exploring uncertain concepts (exploration), and reviewing mastered concepts at risk of being forgotten (retention). The specific mechanism for this integration is described in Section 3.4.1.

### 3.3.6 Layer 5: LLM Feedback Engine (Optional)

**Purpose.** Layer 5 provides contextual, pedagogically appropriate hints when students are struggling with a problem. It is designated as optional because the core thesis contribution --- the integration of Layers 1 through 4 --- is independent of LLM-based feedback.

**Model.** The feedback engine uses a Retrieval-Augmented Generation (RAG) pipeline:

1. When a student requests a hint (or after a configurable number of failed attempts), the system constructs a query combining the problem description, the student's latest code, the error message, and the relevant concept from the knowledge graph.
2. The query is used to retrieve relevant context: concept descriptions and prerequisite information from the knowledge graph, similar solved examples from the problem bank, and common misconceptions associated with the concept.
3. The retrieved context and the student's submission are passed to a large language model with a prompt template that enforces Socratic questioning --- guiding the student toward the solution through questions and partial explanations rather than providing the answer directly.

**Interaction with other layers.** Layer 5 operates independently of the recommendation pipeline. It is triggered on demand by the student or automatically after repeated failures, and it consumes the student's current knowledge state (from Layer 1) to calibrate the level of the hint. For example, a student with low mastery of the concept receives more fundamental guidance, while a student with moderate mastery receives a more targeted nudge.

### 3.3.7 Knowledge Graph Foundation

**Purpose.** The Knowledge Graph provides the structural backbone that coordinates all adaptive layers. It is a directed acyclic graph (DAG) in which nodes represent programming concepts and edges represent prerequisite relationships. The graph encodes the pedagogical sequencing that is implicit in any programming curriculum: understanding variables is prerequisite to understanding loops, understanding loops is prerequisite to understanding nested loops and basic algorithms, and so forth.

**Structure.** The knowledge graph consists of 28 concepts organized into six topic groups: Basics (variables, data types, I/O), Control Flow (conditionals, loops, nested loops), Functions (function definition, parameters, return values, recursion), Data Structures (lists, tuples, dictionaries, sets, strings), Algorithms (sorting, searching, two pointers), and Advanced (dynamic programming, graph algorithms). The complete concept inventory is provided in Appendix B. Each concept has a difficulty tier (1--5) that reflects its position in the curriculum. Prerequisite edges are weighted (default weight 1.0) to allow for soft prerequisites in future extensions. Each concept has at least one problem mapped to it, a requirement enforced by the knowledge graph validation rules that prevent a concept from being included in the recommendation pipeline unless it has at least one associated problem.

```
Basics                Control Flow          Functions
+----------+         +----------+          +----------+
| Variables|-------->|  Condi-  |--------->| Function |
|  & Types |         | tionals  |          |   Def    |
+----------+         +----+-----+          +----+-----+
                          |                     |
                     +----v-----+          +----v-----+
                     |  Loops   |--------->| Recursion|
                     +----+-----+          +----+-----+
                          |                     |
                     +----v-----+          +----v-----+
                     |  Nested  |          |    DP    |
                     |  Loops   |          +----------+
                     +----------+

Data Structures              Algorithms
+----------+                +----------+
|  Lists   |--------------->| Sorting  |
+----------+                +----------+
|  Dicts   |--------------->| Searching|
+----------+                +----------+
```

[Figure 3.2: Simplified view of the knowledge graph showing concept nodes and prerequisite edges. The complete 28-concept graph is provided in Appendix B.]

**Role in the architecture.** The Knowledge Graph is consumed by multiple layers:

- **Layer 1 (BKT):** Uses the graph to identify which concepts each problem assesses (via the `problem_concepts` mapping). When a student solves a problem tagged with concept C, the BKT update is applied to concept C.
- **Layer 3 (MAB):** Uses prerequisite edges to determine concept eligibility. A concept is eligible only if all concepts connected to it by incoming prerequisite edges have been mastered. The graph's topological sort defines the natural learning progression.
- **Layer 4 (FSRS):** Uses the graph to ensure that when a concept is due for review, the system selects a problem that specifically targets that concept rather than a related but distinct concept.
- **Layer 5 (LLM):** Uses concept descriptions and prerequisite chains to provide contextually grounded hints.

The graph is managed by instructors and administrators through the NestJS API and is expected to evolve as the platform's problem bank grows. A dedicated management interface (UC12) supports adding, editing, and removing concepts and edges, with validation to ensure the graph remains a DAG (cycles would create impossible prerequisite requirements).

### 3.3.8 Hyperparameter Summary

Table 3.3 consolidates all hyperparameters introduced in this section with their default values, valid ranges, and justifications.

**Table 3.3.** Hyperparameter summary for the five-layer adaptive architecture.

| Parameter | Symbol | Default | Valid Range | Source / Justification | Layer |
|-----------|--------|---------|-------------|----------------------|-------|
| Mastery threshold | $\theta_m$ | 0.85 | [0.80, 0.95] | Corbett & Anderson [16]; standard BKT mastery range | L1 |
| Initial prior knowledge | $P(L_0)$ | 0.1 | [0.01, 0.30] | Corbett & Anderson [16]; pyBKT defaults [56] | L1 |
| Transition probability | $P(T)$ | 0.2 | [0.05, 0.40] | Corbett & Anderson [16]; pyBKT defaults [56] | L1 |
| Guess probability | $P(G)$ | 0.15 | [0.05, 0.30] | Corbett & Anderson [16]; multi-test-case constraint | L1 |
| Slip probability | $P(S)$ | 0.1 | [0.01, 0.20] | Corbett & Anderson [16]; pyBKT defaults [56] | L1 |
| Base K-factor | $K_{\text{base}}$ | 25 | [16, 40] | Elo [17]; midpoint of K=32 (new) and K=16 (established) | L2 |
| ZPD lower bound | $\delta_{\min}$ | 50 | [0, 150] | Eq. 3.1 yields P(correct) $\approx$ 0.43; flow theory [57] | L2 |
| ZPD upper bound | $\delta_{\max}$ | 250 | [150, 400] | Eq. 3.1 yields P(correct) $\approx$ 0.15; desirable difficulty [21] | L2 |
| Student initial Elo | — | 1200 | — | Standard Elo center [17] | L2 |
| Problem initial Elo | — | 1000/1200/1400 | — | Mapped from EASY/MEDIUM/HARD labels | L2 |
| Learning gain weight | $w_1$ | 0.5 | [0.3, 0.7] | Prioritizes mastery improvement; tuned in Sec. 5.5 | L3 |
| Correctness weight | $w_2$ | 0.3 | [0.1, 0.5] | Secondary signal; tuned in Sec. 5.5 | L3 |
| Efficiency weight | $w_3$ | 0.2 | [0.1, 0.4] | Penalizes excessive attempts; tuned in Sec. 5.5 | L3 |
| Max attempts cap | $M$ | 5 | [3, 10] | Attempt penalty saturation point | L3 |
| MAB initial prior | $\alpha_0, \beta_0$ | 1.0, 1.0 | — | Uniform Beta(1,1); standard uninformative prior | L3 |
| Review threshold | $\theta_r$ | 0.7 | [0.5, 0.9] | FSRS default target retrievability [12] | L4 |
| FSRS initial difficulty | $D_0$ | 5.0 | [1, 10] | FSRS midpoint default [12] | L4 |
| FSRS initial stability | $S_0$ | 1.0 day | [0.5, 3.0] | Conservative initial interval | L4 |
| Cold-start round-robin | — | 3 interactions | [2, 5] | Minimum for BKT differentiation; Clement et al. [22] | — |
| Full pipeline threshold | — | 10 submissions | [5, 15] | BKT convergence from prior + ~10 observations [16] | — |

## 3.4 Data Flow Design

The adaptive platform operates through two primary data flows: the recommendation flow (student requests a problem) and the submission processing flow (student submits a solution). This section describes each flow in detail, followed by the cold-start handling strategy and error handling provisions.

### 3.4.1 Recommendation Flow

The recommendation flow is triggered when a student requests a practice problem. It traverses all adaptive layers to produce a personalized recommendation. The following sequence diagram illustrates the flow.

```
Student        React Client       NestJS API        Redis Cache       AI Service (FastAPI)
   |                |                  |                  |                   |
   |  Click "Get    |                  |                  |                   |
   |  Recommendation"|                 |                  |                   |
   |--------------->|                  |                  |                   |
   |                | GET /adaptive/   |                  |                   |
   |                | recommend/:uid   |                  |                   |
   |                |----------------->|                  |                   |
   |                |                  | Check cache      |                   |
   |                |                  |----------------->|                   |
   |                |                  |   Cache miss     |                   |
   |                |                  |<-----------------|                   |
   |                |                  |                  |                   |
   |                |                  | GET /adaptive/   |                   |
   |                |                  | recommend/:uid   |                   |
   |                |                  |---------------------------------->  |
   |                |                  |                  |                   |
   |                |                  |                  |  1. Load KG       |
   |                |                  |                  |  2. Load BKT      |
   |                |                  |                  |     states        |
   |                |                  |                  |  3. Load Elo      |
   |                |                  |                  |     ratings       |
   |                |                  |                  |  4. Load FSRS     |
   |                |                  |                  |     cards         |
   |                |                  |                  |  5. Compute       |
   |                |                  |                  |     eligible      |
   |                |                  |                  |     concepts      |
   |                |                  |                  |  6. Check FSRS    |
   |                |                  |                  |     review queue  |
   |                |                  |                  |  7. Run Level-1   |
   |                |                  |                  |     Thompson      |
   |                |                  |                  |     Sampling      |
   |                |                  |                  |  8. Filter ZPD    |
   |                |                  |                  |  9. Run Level-2   |
   |                |                  |                  |     Thompson      |
   |                |                  |                  |     Sampling      |
   |                |                  |                  |                   |
   |                |                  |  Ranked problem list               |
   |                |                  |<----------------------------------|
   |                |                  |                  |                   |
   |                |                  | Cache result     |                   |
   |                |                  |----------------->|                   |
   |                |                  |                  |                   |
   |                |                  | Enrich with      |                   |
   |                |                  | problem details, |                   |
   |                |                  | concept context  |                   |
   |                |                  |                  |                   |
   |                | Recommendation   |                  |                   |
   |                | response         |                  |                   |
   |                |<-----------------|                  |                   |
   |  Display       |                  |                  |                   |
   |  recommendation|                  |                  |                   |
   |<---------------|                  |                  |                   |
```

[Figure 3.3: Sequence diagram for the recommendation flow.]

The recommendation process within the AI service proceeds through the following steps:

**Step 1: Load knowledge graph.** The service loads the concept DAG, either from Redis cache (if available and not expired) or from the `concepts` and `knowledge_graph_edges` tables. The graph structure changes infrequently and is cached with a 1-hour TTL.

**Step 2: Load student state.** The service loads the student's BKT knowledge states (from `knowledge_states`), Elo ratings (from `elo_ratings`), MAB states (from `mab_states`), and FSRS cards (from `fsrs_cards`). Each of these is cached in Redis with TTLs appropriate to their update frequency (detailed in Section 3.7).

**Step 3: Determine eligible concepts.** Using the knowledge graph and BKT mastery estimates, the service computes the set of eligible concepts at Level 1. A concept $c$ is eligible if:
- All prerequisites of $c$ are mastered: $\forall c' \in \text{prereq}(c): P(L_t^{c'}) \geq 0.85$
- AND either: (a) $c$ is not yet mastered: $P(L_t^c) < 0.85$, or (b) $c$ is due for review: $R_c(t) < 0.7$ (from FSRS)

Concepts due for review that are also mastered are included in the eligible set with a priority boost: their Thompson Sampling prior is inflated by adding a review urgency bonus to $\alpha$, proportional to how far the retrievability has fallen below the threshold.

**Step 4: Level 1 Thompson Sampling.** For each eligible concept, the service draws a sample $\theta_c \sim \text{Beta}(\alpha_c, \beta_c)$ from the concept's reward distribution. The concept with the highest sampled value is selected.

**Step 5: ZPD filtering.** Within the selected concept, the service retrieves all unsolved problems tagged with that concept and filters them by the ZPD constraint (Equation 3.5). If no problems pass the ZPD filter (because the student has outgrown all available problems in that concept, or all are too difficult), the service falls back to the next-highest concept from Step 4.

**Step 6: Level 2 Thompson Sampling.** Among the ZPD-filtered problems, the service draws a sample $\theta_p \sim \text{Beta}(\alpha_p, \beta_p)$ for each and selects the problem with the highest sampled value.

**Step 7: Return ranked list.** The service returns a ranked list of recommended problems (typically 3--5), not just the single top recommendation. This gives the student some agency in choosing among appropriately challenging options. The NestJS API enriches the list with full problem details (title, description, concept name, estimated success probability) before returning it to the client.

### 3.4.2 Submission Processing Flow

The submission processing flow is triggered when a student submits code for a problem. It involves two phases: synchronous code execution (which must return promptly to the student) and asynchronous adaptive layer updates (which happen in the background).

**Phase 1: Synchronous Execution.**

1. The student submits code via the React client.
2. The NestJS API receives the submission, saves it to the `submissions` table with status PENDING, and dispatches it to the Docker sandbox.
3. The Docker sandbox executes the code against each test case, recording pass/fail for each.
4. The NestJS API updates the submission status (ACCEPTED, WRONG_ANSWER, TIME_LIMIT, RUNTIME_ERROR, or COMPILATION_ERROR) and returns the result to the student.

**Phase 2: Asynchronous Adaptive Updates.**

5. After the submission status is finalized, the NestJS API sends an asynchronous POST request to the AI service at `/adaptive/update` with a payload containing:
   - `student_id`: the submitting student's identifier
   - `problem_id`: the problem identifier
   - `concept_id`: the primary concept of the problem (from `problem_concepts`)
   - `is_correct`: boolean indicating whether the submission was ACCEPTED
   - `attempt_number`: the ordinal number of this submission for this (student, problem) pair
   - `time_spent`: elapsed time since the student first viewed the problem (if available)
   - `error_type`: the specific error category (for non-ACCEPTED submissions)

6. The AI service processes the update through each layer sequentially:

   a. **Layer 1 (BKT) update:** The mastery probability $P(L_t)$ is updated using Equations 2.1--2.3 from Chapter 2. The learning gain $\Delta P(L_t)$ is computed.

   b. **Layer 2 (Elo) update:** Student and problem Elo ratings are updated using Equations 3.1--3.4. The K-factors are adjusted based on the student's trend and the number of prior interactions.

   c. **Layer 3 (MAB) update:** The reward signal is computed using Equation 3.6. The Beta distribution parameters for both the selected concept arm and the selected problem arm are updated: $\alpha \leftarrow \alpha + r$ and $\beta \leftarrow \beta + (1 - r)$.

   d. **Layer 4 (FSRS) update:** If the concept has been previously mastered and has an FSRS card, the card is updated with the submission-derived rating. If the concept has just reached mastery for the first time ($P(L_t) \geq 0.85$ and previously $P(L_{t-1}) < 0.85$), a new FSRS card is created.

7. All updated states are written to the database. Redis caches for the affected student are invalidated.

8. An event log entry is created recording the full update for evaluation purposes.

The sequential ordering of layer updates in Phase 2 is important: Layer 1 must execute before Layer 3 because the MAB reward depends on the learning gain from BKT. Layer 2 can execute in parallel with Layer 1 since it depends only on the submission outcome. Layer 4 depends on Layer 1 (to know whether mastery has been reached) and must therefore execute after Layer 1.

This asynchronous pattern introduces an eventual consistency window typically under two seconds, which is acceptable given that a single recommendation cycle based on slightly stale state has minimal pedagogical impact. In the worst case, a student who submits a solution and immediately requests a new recommendation may receive a recommendation computed from pre-update state; the next recommendation request will reflect the updated state.

### 3.4.3 Error Handling and Edge Cases

The adaptive pipeline must handle failures gracefully to prevent inconsistent state and ensure a reliable student experience. This section describes the error handling strategy for the primary failure modes.

**Transactional boundaries.** Each adaptive update (Phases 1--4 in Section 3.4.2) is wrapped in a database transaction. A failure in any phase rolls back all updates for that submission event, preventing inconsistent state where, for example, BKT mastery is updated but the corresponding Elo rating is not.

**Retry mechanism.** Failed adaptive updates are enqueued in a Redis-backed retry queue with exponential backoff (initial delay 1 second, maximum 3 retries). After 3 failures, the event is written to a dead-letter table for manual inspection. The student's submission result is unaffected by adaptive update failures, since Phase 1 (code execution) completes independently.

**Empty eligible set.** If no eligible concepts exist because all non-mastered concepts have unmet prerequisites, the system falls back to recommending the concept with the highest mastery progress (the concept closest to the $\theta_m = 0.85$ threshold). This situation arises rarely in practice, as the knowledge graph is designed with multiple prerequisite-free entry points, but it can occur if a student has partially mastered several prerequisite chains without completing any.

**ZPD exhaustion.** If no problems fall within the ZPD bounds (Equation 3.5) after the initial filter, the system performs up to two expansion steps, each widening the bounds by 50 Elo points in both directions. If no problems are found after two expansions, the system returns the easiest unsolved problem in the concept regardless of Elo matching, accepting the pedagogical compromise in favor of providing a recommendation.

**Concurrent submissions.** Per-student sequential processing is enforced via a per-student Redis lock (SETNX pattern with a 30-second TTL to prevent deadlocks). If a lock is held when a new update arrives, the update is queued and processed after the lock is released. This prevents race conditions where two concurrent submissions produce inconsistent state updates.

**AI service unavailability.** If the AI service is temporarily unavailable (e.g., during a restart), the NestJS API returns a fallback recommendation drawn from the pool of unsolved problems in the student's most recently active topic group, ordered by static difficulty label. The submission result is always returned to the student regardless of AI service availability.

### 3.4.4 Cold Start Handling

The cold-start problem arises when the system has insufficient data to make informed adaptive decisions. This occurs in two scenarios: new students with no submission history, and new problems with no submission data.

**New Student Cold Start.** When a student first uses the platform, all adaptive state is at its default values: BKT mastery at $P(L_0) = 0.1$ for all concepts, Elo rating at 1200 (the population mean), MAB priors at $\text{Beta}(1, 1)$ (uniform), and no FSRS cards. The system handles this through a structured onboarding phase:

1. For the first 3 interactions, the system bypasses the MAB and uses a round-robin strategy over prerequisite-free concepts (those with no incoming edges in the knowledge graph, such as "Variables" and "Data Types"). This ensures that the earliest submissions provide signal across the foundational concepts. The threshold of 3 interactions is informed by Clement et al. [22], who demonstrated that MAB-based educational recommendations require a minimum exploration period to outperform random selection.
2. Within each concept, the system selects the problem closest to Elo 1200 (the student's initial rating), ensuring a moderate difficulty level for the first interactions.
3. After approximately 10 submissions, the BKT and Elo models have sufficient data to differentiate the student from the population mean, and the full adaptive pipeline takes over. This threshold reflects BKT's convergence behavior: given the initial prior $P(L_0) = 0.1$ and transition probability $P(T) = 0.2$, approximately 10 observations are sufficient for the posterior to diverge meaningfully from the prior [16].

The cold-start phase resolves quickly because BKT's Bayesian update meaningfully shifts posterior estimates from each observation, and the elevated initial K-factor in the Elo system amplifies early rating changes, enabling rapid calibration.

**New Problem Cold Start.** When a new problem is added to the platform, it has no submission history from which to derive an empirical Elo rating. The system initializes the problem's Elo rating based on its static difficulty label: EASY maps to Elo 1000, MEDIUM to 1200, and HARD to 1400. The initial K-factor is set to 50 (double the base K-factor) to allow rapid convergence toward the problem's true difficulty. After approximately 30 submissions from diverse students, the problem's Elo rating stabilizes and the K-factor decays to the base value. The MAB prior for the new problem is initialized at $\text{Beta}(1, 1)$, ensuring that Thompson Sampling's natural exploration tendency gives the problem a fair chance of being recommended despite its uncertain reward distribution.

## 3.5 Database Schema Design

The database schema comprises core platform tables and adaptive state tables that together support the Knowledge Graph Foundation and the four adaptive layers. This section describes the adaptive tables, the relationships between tables, and the migration strategy.

**ID strategy.** Core platform tables (users, problems, submissions) use UUID primary keys for global uniqueness and safe distributed generation. Adaptive engine tables (concepts, knowledge_graph_edges, problem_concepts, and adaptive state tables) use auto-incrementing integer primary keys for computational efficiency, since concept IDs and problem IDs serve as array indices in BKT and MAB state lookups where integer indexing is significantly faster than UUID hashing.

### 3.5.1 Adaptive Tables and Their Roles

**Table 3.4.** Database tables for the adaptive learning engine.

| Table | Layer | Purpose | Key Columns |
|-------|-------|---------|-------------|
| `concepts` | Foundation | Knowledge graph nodes | id, name, display_name, topic_group, difficulty_tier |
| `knowledge_graph_edges` | Foundation | Prerequisite edges | from_concept_id, to_concept_id, relation_type, weight |
| `problem_concepts` | Foundation | Problem-to-concept mapping | problem_id, concept_id, is_primary |
| `knowledge_states` | Layer 1 | BKT mastery per (student, concept) | student_id, concept_id, p_mastery, p_l0, p_transit, p_guess, p_slip |
| `elo_ratings` | Layer 2 | Elo ratings for students and problems | entity_id, entity_type, concept_id, rating, k_value, trend |
| `mab_states` | Layer 3 | MAB arm distributions | student_id, arm_id, arm_type, alpha, beta |
| `fsrs_cards` | Layer 4 | FSRS memory states | student_id, concept_id, difficulty, stability, retrievability, due_date |
| `event_logs` | Evaluation | Interaction event log | user_id, event, data (JSON), session_id |
| `experiment_groups` | Evaluation | A/B test group assignment | user_id, group_name |

**Concepts table.** Each row represents a programming concept in the knowledge graph. The `name` field is a machine-readable identifier (e.g., "recursion", "dynamic_programming"), while `display_name` is a human-readable label (e.g., "Recursion", "Dynamic Programming"). The `topic_group` field organizes concepts into curricular units (e.g., "Control Flow", "Data Structures"). The `difficulty_tier` (1--5) provides a coarse ordering that assists with initial problem selection before Elo ratings have stabilized.

**Knowledge graph edges table.** Each row represents a directed edge in the knowledge graph, indicating that `from_concept` is a prerequisite for `to_concept`. The `relation_type` field defaults to "PREREQUISITE" but is designed to accommodate future relation types (e.g., "RELATED", "EXTENDS") if the knowledge graph is enriched. The `weight` field (default 1.0) allows for soft prerequisites in future extensions. A unique constraint on `(from_concept_id, to_concept_id)` prevents duplicate edges.

**Problem concepts table.** Each row maps a problem to a concept, with a boolean `is_primary` flag indicating the primary concept assessed by the problem. A problem may be associated with multiple concepts (e.g., a problem that requires both loops and lists), but exactly one should be designated as primary. The primary concept determines which BKT state is updated when the problem is submitted.

**Knowledge states table.** Each row stores the BKT state for a single (student, concept) pair. The columns `p_mastery`, `p_l0`, `p_transit`, `p_guess`, and `p_slip` correspond directly to the BKT parameters described in Section 2.2.1, with `p_mastery` representing the current posterior mastery estimate $P(L_t)$. The `n_attempts` and `n_correct` counters support analytics and parameter tuning. A unique constraint on `(student_id, concept_id)` ensures one state per pair, and a composite index on `(student_id, p_mastery)` supports efficient querying of mastered concepts for prerequisite gating.

**Elo ratings table.** This table uses a polymorphic design: the `entity_type` field distinguishes between student ratings (`entity_type = 'STUDENT'`) and problem ratings (`entity_type = 'PROBLEM'`). This polymorphic design enables the Elo update algorithm to treat students and problems symmetrically through a single repository layer. The trade-off is that referential integrity between `entity_id` and its source table must be enforced at the application layer rather than through database foreign keys. An alternative design with separate `student_elo_ratings` and `problem_elo_ratings` tables would provide stronger referential integrity; however, it would duplicate the update logic and complicate the rating comparison queries used by the ZPD filter. The polymorphic approach is preferred for this prototype, with a migration path to separate tables documented as future work. The optional `concept_id` field is included to support per-concept Elo ratings in future extensions; for the current implementation, `concept_id` is NULL for all ratings (global Elo only), and the column is included to avoid a future schema migration. The `rating_history` column (JSONB) stores a time series of past ratings for trend analysis and visualization. A unique constraint on `(entity_id, entity_type, concept_id)` ensures one rating per entity per concept.

**MAB states table.** Each row stores the Thompson Sampling state for a single (student, arm) pair. The `arm_type` field distinguishes between concept-level arms (`arm_type = 'CONCEPT'`) and problem-level arms (`arm_type = 'PROBLEM'`). The `arm_id` field stores the concept ID or problem ID as a string. The `alpha` and `beta` columns parameterize the Beta distribution, and `n_pulls` and `total_reward` support analytics. A unique constraint on `(student_id, arm_id, arm_type)` ensures one state per arm per student.

**FSRS cards table.** Each row stores the FSRS memory state for a single (student, concept) pair. The `difficulty` (1--10), `stability` (days), and `retrievability` (0--1) columns correspond to the FSRS model parameters described in Section 2.2.5. The `state` field tracks the card lifecycle (NEW, LEARNING, REVIEW, RELEARNING). The `due_date` indicates when the next review is scheduled, and `last_review` records when the concept was last practiced. A composite index on `(student_id, due_date)` supports efficient querying of the review queue, and a composite index on `(student_id, retrievability)` supports priority-based review selection.

### 3.5.2 Schema Relationships

The following diagram illustrates the relationships between the adaptive tables and the core platform tables.

```
+----------+       +------------------+       +----------+
|  users   |       |   enrollments    |       | courses  |
| (id,     |<------| (userId,         |------>| (id,     |
|  email,  |       |  courseId)        |       |  title)  |
|  role)   |       +------------------+       +----+-----+
+----+-----+                                       |
     |                                             |
     |  1:N    +------------------+                |
     |-------->| knowledge_states |           +----v-----+
     |         | (student_id,     |           | problems |
     |         |  concept_id,     |           | (id,     |
     |         |  p_mastery, ...) |           |  title,  |
     |         +--------+---------+           |  diff,   |
     |                  |                     |  tags)   |
     |  1:N    +--------v---------+           +----+-----+
     |-------->|   mab_states     |                |
     |         | (student_id,     |           +----v-----------+
     |         |  arm_id,         |           | problem_concepts|
     |         |  alpha, beta)    |           | (problem_id,    |
     |         +------------------+           |  concept_id,    |
     |                                        |  is_primary)    |
     |  1:N    +------------------+           +--------+--------+
     |-------->|   fsrs_cards     |                    |
     |         | (student_id,     |           +--------v--------+
     |         |  concept_id,     |           |    concepts     |
     |         |  stability, ...) |           | (id, name,      |
     |         +------------------+           |  display_name,  |
     |                                        |  topic_group,   |
     |  1:N    +------------------+           |  difficulty_    |
     |-------->|   elo_ratings    |           |  tier)          |
     |         | (entity_id,      |           +--------+--------+
     |         |  entity_type,    |                    |
     |         |  rating, ...)    |           +--------v--------+
     |         +------------------+           | knowledge_graph |
     |                                        | _edges          |
     |  1:N    +------------------+           | (from_concept,  |
     |-------->|   event_logs     |           |  to_concept,    |
     |         | (user_id,        |           |  relation_type) |
     |         |  event, data)    |           +-----------------+
     |         +------------------+
     |
     |  1:1    +--------------------+
     +-------->| experiment_groups  |
               | (user_id,          |
               |  group_name)       |
               +--------------------+
```

[Figure 3.4: Entity-relationship diagram showing connections between core platform tables (left, top) and adaptive state tables.]

The key relationships are:

- **Users** have a one-to-many relationship with `knowledge_states`, `mab_states`, `fsrs_cards`, `elo_ratings` (where entity_type = 'STUDENT'), and `event_logs`. Each user has at most one `experiment_groups` entry.
- **Concepts** serve as a hub connecting `knowledge_states`, `fsrs_cards`, `problem_concepts`, and `knowledge_graph_edges`. This central position reflects the concept's role as the fundamental unit of knowledge in the system.
- **Problems** connect to `concepts` through `problem_concepts` and to `elo_ratings` (where entity_type = 'PROBLEM'). The `problem_concepts` mapping enables the system to determine which concept(s) a submission provides evidence about.
- **Knowledge graph edges** form a self-referential relationship within `concepts`, creating the prerequisite DAG. The `from_concept` is the prerequisite and `to_concept` is the dependent concept.

### 3.5.3 Migration Strategy

The schema is implemented as Prisma migrations, ensuring version-controlled, reproducible database evolution. The migration strategy deploys tables in three phases, ordered by dependency:

**Phase 1: Knowledge Graph tables.** The `concepts`, `knowledge_graph_edges`, and `problem_concepts` tables are created. This phase is independent of the adaptive layers and can be populated with concept data and problem-concept mappings before any adaptive algorithms are deployed. Problems receive concept tags through a manual curation process where the instructor maps each problem to its primary concept.

**Phase 2: Adaptive state tables.** The `knowledge_states`, `elo_ratings`, `mab_states`, and `fsrs_cards` tables are created. These tables start empty and are populated as students interact with the system. The AI service creates state rows on first access (lazy initialization): when the system first queries a student's knowledge state for a concept and no row exists, it creates one with default BKT priors.

**Phase 3: Evaluation tables.** The `event_logs` and `experiment_groups` tables are created. Experiment group assignment is performed at enrollment time, before the student begins interacting with the adaptive features.

This phased approach allows the knowledge graph to be curated and validated independently of the adaptive engine, reducing the risk of deployment issues.

## 3.6 API Design

The API design follows a gateway pattern: the NestJS backend serves as the API gateway that handles authentication, authorization, and request routing, while the FastAPI AI service provides the adaptive intelligence endpoints. This separation allows the AI service to be developed and scaled independently of the web application backend.

**Security.** The AI service is deployed on an internal network not accessible from the public internet. All requests to the AI service originate from the NestJS gateway, which validates JWT tokens and enforces role-based access control before proxying. The AI service validates an internal shared API key in the `X-Internal-Auth` header. Students can only access their own knowledge state and recommendations; cross-user access is prevented by the NestJS layer's JWT authorization checks, which verify that the `user_id` in the request path matches the authenticated user's identity (or that the requester has an instructor/admin role for class-level endpoints).

### 3.6.1 AI Service Endpoints

The FastAPI AI service exposes the following endpoints:

**GET /adaptive/recommend/{user_id}** — Returns a ranked list of recommended problems for the specified student. Query parameters include `limit` (default 5, maximum 10) and `include_review` (boolean, default true, whether to include review-due concepts in the candidate set). The `selection_reason` field in each recommendation indicates why the problem was selected ("exploitation", "exploration", or "review"), providing transparency for both the student dashboard and evaluation logging.

**POST /adaptive/update** — Processes a submission result and updates all adaptive layers. This endpoint is called asynchronously by the NestJS backend after code execution completes. The request payload includes `student_id`, `problem_id`, `concept_id`, `is_correct`, `attempt_number`, `time_spent_seconds`, and `error_type`. The response includes a summary of updates across all four layers.

**GET /adaptive/knowledge-state/{user_id}** — Returns the complete knowledge state for a student across all concepts, used by the dashboard.

**GET /adaptive/review-queue/{user_id}** — Returns concepts due for review, ordered by urgency (lowest retrievability first). Includes the estimated retrievability, stability, and days since last review for each concept.

**POST /adaptive/hint** — Generates a Socratic hint for a struggling student. Request includes the problem ID, the student's latest code, and the error message. This endpoint is optional (Layer 5).

Detailed request and response JSON schemas for each endpoint are provided in Chapter 4, Section 4.3.

### 3.6.2 NestJS Gateway Endpoints

The NestJS backend exposes the following endpoints that proxy or augment the AI service:

**Knowledge Graph Management:**
- `GET /api/concepts` — List all concepts with their topic groups and difficulty tiers.
- `POST /api/concepts` — Create a new concept (instructor/admin only).
- `GET /api/knowledge-graph` — Retrieve the full knowledge graph (concepts + edges).
- `POST /api/knowledge-graph/edges` — Add a prerequisite edge (admin only), with cycle detection.

**Adaptive Recommendations (Proxy):**
- `GET /api/adaptive/recommend/:userId` — Proxies to the AI service, enriching the response with full problem details (description, test case count) and concept display names.
- `GET /api/adaptive/knowledge-state/:userId` — Proxies to the AI service, adding concept display names and topic group labels.
- `GET /api/adaptive/review-queue/:userId` — Proxies to the AI service.

**Analytics:**
- `GET /api/analytics/student/:userId` — Aggregated analytics for a specific student: mastery heatmap, Elo trajectory, submission history, review compliance rate.
- `GET /api/analytics/class/:courseId` — Class-level analytics for an instructor: concept mastery distribution, common struggle concepts, average Elo progression, submission volume over time.

### 3.6.3 Endpoints with Adaptive Integration

Two platform endpoints incorporate adaptive engine integration:

**POST /api/submissions.** After the code execution phase completes and the submission status is finalized, the endpoint issues an asynchronous call to the AI service's `/adaptive/update` endpoint. This call is fire-and-forget from the student's perspective: the submission result is returned to the student immediately, and the adaptive updates happen in the background. If the AI service is temporarily unavailable, the submission result is still returned successfully; the adaptive update is retried via the mechanism described in Section 3.4.3. The payload sent to the AI service is constructed by looking up the problem's primary concept from the `problem_concepts` table and computing the attempt number from the count of prior submissions for the same (student, problem) pair.

**GET /api/dashboard.** The dashboard endpoint aggregates both platform metrics (submission count, acceptance rate, recent activity) and adaptive metrics: the student's current concept mastery levels, Elo rating, number of concepts mastered, number of concepts due for review, and the most recent recommendation with its selection reason. Adaptive metrics are fetched from the AI service via the proxy endpoints.

## 3.7 Caching Strategy

The recommendation pipeline involves multiple database queries (loading knowledge states, Elo ratings, FSRS cards, MAB states, and the knowledge graph) followed by computational processing (prerequisite gating, ZPD filtering, Thompson Sampling). To meet the 500ms recommendation latency target (NFR2) under concurrent load, the system employs Redis as a caching layer with the following policies.

**Table 3.5.** Redis caching configuration for adaptive state data.

| Cache Key Pattern | Data | TTL | Invalidation Trigger |
|-------------------|------|-----|---------------------|
| `kg:structure` | Full knowledge graph (concepts + edges) | 60 min | Knowledge graph modification (edge/concept add/delete) |
| `ks:{student_id}` | All knowledge states for a student | 5 min | Any submission by that student |
| `elo:student:{student_id}` | Student Elo rating | 5 min | Any submission by that student |
| `elo:problems:{concept_id}` | Problem Elo ratings within a concept | 10 min | Any submission on a problem in that concept |
| `fsrs:{student_id}` | All FSRS cards for a student | 5 min | Any submission by that student on a mastered concept |
| `mab:{student_id}` | All MAB states for a student | 5 min | Any submission by that student |
| `rec:{student_id}` | Cached recommendation result | 2 min | Any submission by that student |

The TTL values are designed to balance freshness against cache hit rate. The knowledge graph changes infrequently (only when instructors modify the curriculum), so a 60-minute TTL is appropriate. Student-specific state has a 5-minute TTL, which serves as a safety net against missed invalidation events. The primary freshness mechanism is explicit invalidation after each submission update (described below), so the TTL is expected to expire rarely under normal operation. The recommendation result itself has the shortest TTL (2 minutes) because it should reflect the student's most recent submission.

**Invalidation strategy.** Cache invalidation follows the write-through pattern: when the AI service processes a submission update (Section 3.4.2, Phase 2), it invalidates the relevant cache entries for the affected student. Specifically, after updating Layer 1 through Layer 4, the service deletes the `ks:{student_id}`, `elo:student:{student_id}`, `mab:{student_id}`, `fsrs:{student_id}`, and `rec:{student_id}` keys. Problem-level Elo cache (`elo:problems:{concept_id}`) is invalidated only when a problem's rating changes by more than 10 points, reducing unnecessary cache churn for minor rating fluctuations.

**Fallback behavior.** If Redis is unavailable (e.g., due to a transient failure), the AI service falls back to direct database queries. The recommendation latency may increase (estimated 800--1200ms without caching), but the system remains functional. This graceful degradation ensures that the adaptive features are not gated on Redis availability.

---

**Chapter Summary.** This chapter has defined the functional and non-functional requirements for the adaptive learning platform, described the four-component system architecture and its design rationale, and presented the five-layer adaptive architecture with its Knowledge Graph Foundation. The data flow design specifies how recommendations are generated and how submissions trigger cascading updates across all layers. The database schema, API design, and caching strategy provide the technical infrastructure needed to implement the architecture within the latency and scalability constraints of a university deployment. The following chapter presents the implementation details of each layer, including the specific algorithms, parameter choices, and code-level design decisions.

---

## References (New references introduced in Chapter 3)

References [3], [6], [11], [12], [16], [17], [18], [19], [20], [21], [22], [26], [29], [35] were introduced in Chapters 1 and 2 and are reused in this chapter. The following new references are introduced in Chapter 3:

[56] A. Badrinath, F. Wang, and Z. A. Pardos, "pyBKT: An Accessible Python Library of Bayesian Knowledge Tracing Models," in *Proc. 14th International Conference on Educational Data Mining (EDM)*, 2021, pp. 468–474. [Online]. Available: https://arxiv.org/abs/2105.00385

[57] M. Csikszentmihalyi, *Flow: The Psychology of Optimal Experience*. New York: Harper & Row, 1990. ISBN: 978-0-06-016253-5.

[58] S. Agrawal and N. Goyal, "Further Optimal Regret Bounds for Thompson Sampling," in *Proc. 16th International Conference on Artificial Intelligence and Statistics (AISTATS)*, PMLR, vol. 31, pp. 99–107, 2013. [Online]. Available: https://proceedings.mlr.press/v31/agrawal13a.html
