# Thesis Complete Outline

**Title:** Adaptive Learning Platform for University Programming Courses
*Hệ thống hỗ trợ học tập thích ứng cho môn lập trình tại đại học*

**Author:** Nguyen Tuan Duong
**Advisor:** Bui Quoc Khanh
**Institution:** Hanoi University, Faculty of Information Technology

---

## Overall Structure

| Chapter | Title | Target Word Count | Pages (est.) |
|---------|-------|-------------------|--------------|
| — | Abstract | 300–500 | 1 |
| — | Acknowledgments | 200–300 | 1 |
| — | Table of Contents | — | 2 |
| — | List of Figures / Tables / Abbreviations | — | 2 |
| 1 | Introduction | 3,000–4,000 | 8–10 |
| 2 | Literature Review & Theoretical Foundation | 8,000–12,000 | 20–30 |
| 3 | System Design & Architecture | 6,000–8,000 | 15–20 |
| 4 | Implementation | 5,000–7,000 | 12–18 |
| 5 | Evaluation & Experiments | 5,000–7,000 | 12–18 |
| 6 | Conclusion & Future Work | 2,000–3,000 | 5–8 |
| — | References | — | 4–6 |
| — | Appendices | — | 10–20 |
| **Total** | | **29,000–42,000** | **~80–130** |

---

## Abstract (300–500 words)

**Content:**
- Problem: Programming courses have high dropout and low engagement; one-size-fits-all instruction fails diverse learners
- Solution: Multi-layer adaptive learning platform integrating Knowledge Tracing, Elo-based difficulty calibration, Hierarchical Multi-Armed Bandits, FSRS spaced repetition, and LLM-powered feedback
- Method: Design and implementation of 5-layer adaptive engine on a web platform with sandboxed code execution
- Results: [To be written after evaluation] — report learning gain, engagement metrics, and recommendation accuracy
- Contribution: First integrated system combining KT + Elo + MAB + FSRS for programming education

**Writing guidance:** Write this LAST, after all chapters are complete. Summarize each chapter in 1–2 sentences.

---

## Chapter 1: Introduction (3,000–4,000 words)

### 1.1 Problem Statement (600–800 words)
**Content:**
- Programming education challenges at Vietnamese universities
- High failure/dropout rates in introductory programming courses (cite statistics)
- Heterogeneous student backgrounds — some have prior experience, others start from zero
- Limitations of traditional lecture-based instruction for skill acquisition
- The gap between knowing syntax and solving problems (computational thinking)

**Key arguments:**
- Programming is a skill that requires deliberate practice, not passive learning
- Current university courses cannot provide individualized practice pathways
- Students who fall behind have no mechanism to catch up at their own pace

**Evidence needed:**
- National/international statistics on CS dropout rates
- Studies on programming education challenges (Robins et al., 2003; Luxton-Reilly et al., 2018)

### 1.2 Motivation (400–600 words)
**Content:**
- Why adaptive learning is the right approach for programming education
- Success stories from adaptive platforms in other domains (mathematics: ALEKS, Khan Academy)
- The unique properties of programming that make it amenable to adaptive learning:
  - Clear measurable outcomes (code compiles/passes tests)
  - Hierarchical skill structure (arrays → sorting → dynamic programming)
  - Rich behavioral signals from code submissions (time, attempts, errors)
- Gap in existing platforms for Vietnamese university context

**Key arguments:**
- Programming is uniquely suited to adaptive learning because outcomes are objectively measurable
- No existing platform combines all necessary adaptive components for programming specifically

### 1.3 Research Objectives (300–400 words)
**Content:**
1. Design a multi-layer adaptive learning architecture for programming courses
2. Implement knowledge tracing to model student mastery of programming concepts
3. Implement difficulty calibration using Elo ratings for both students and problems
4. Implement intelligent problem selection using Multi-Armed Bandits
5. Implement spaced repetition scheduling for long-term retention
6. Evaluate the system's effectiveness through controlled experiments

**Format:** Numbered list of specific, measurable objectives

### 1.4 Research Questions (200–300 words)
**Content:**
- **RQ1 (Primary):** How accurately can the multi-layer adaptive system model student knowledge and predict performance? *(Combines knowledge state modeling via BKT and difficulty calibration via Elo — both measure prediction accuracy via AUC-ROC, and together they validate the learner model foundation)*
- **RQ2:** Does Hierarchical MAB problem selection improve learning outcomes compared to content-based filtering?
- **RQ3:** Does spaced repetition scheduling improve long-term retention of programming concepts?
- **RQ4:** How do students perceive the usability and usefulness of the adaptive platform?

**Note:** RQ1 is the primary research question that validates the system's learner modeling capability (BKT prediction accuracy + Elo prediction accuracy). RQ2–RQ3 are secondary quantitative questions. RQ4 is the qualitative question. This consolidation from 5 to 4 RQs ensures each RQ can be answered with sufficient evidence within the available sample size and evaluation period.

### 1.5 Scope and Limitations (300–400 words)
**Content:**
- **In scope:** Python programming, university students, web-based platform, 5 adaptive layers
- **Out of scope:** Multi-language support beyond Python, mobile app, real-time collaborative features, integration with university LMS
- **Limitations:** Single university, limited sample size, short evaluation period (1 semester max)
- Language: Vietnamese-speaking students, English interface

### 1.6 Thesis Structure (200–300 words)
**Content:** Brief overview of each chapter (1–2 sentences each). Standard "roadmap" section.

### 1.7 Contributions (400–600 words)
**Content:**
- List 3–4 specific contributions
- For each: what it is, why it's new, and where in the thesis it's developed

**Key contributions to claim:**
1. **Integrated multi-layer adaptive architecture** — first system combining KT + Elo + MAB + FSRS in a unified pipeline for programming education *(STRONG — verified by literature gap analysis)*
2. **Prerequisite-constrained Hierarchical MAB** — problem selection that respects knowledge graph prerequisites, with BKT mastery as the gating criterion *(MODERATE — novel combination)*
3. **FSRS for programming skill retention** — first application of FSRS algorithm to programming concept review scheduling, with novel rating mapping from submission outcomes *(STRONG — clearly novel application domain)*
4. **Open-source platform** — complete, deployable system for Vietnamese university context *(MODERATE — practical contribution)*

**Note:** Dynamic K-Value Elo for programming is NOT claimed as a separate contribution — it is a necessary component of the integrated architecture (Contribution 1) but not novel enough to stand alone. See 08-BRAINSTORM-NOVEL-CONTRIBUTIONS.md for detailed analysis.

---

## Chapter 2: Literature Review & Theoretical Foundation (8,000–12,000 words)

### 2.1 Adaptive Learning Systems (1,500–2,000 words)

#### 2.1.1 Definition and Taxonomy (500–700 words)
**Content:**
- Definition of adaptive learning (Brusilovsky, 2001; Paramythis & Loidl-Reisinger, 2004)
- Taxonomy: macro-adaptive (course level) vs micro-adaptive (task level)
- Components of an adaptive system: learner model, content model, adaptation engine
- Types of adaptation: content selection, sequencing, presentation, feedback

#### 2.1.2 History and Evolution (400–600 words)
**Content:**
- Intelligent Tutoring Systems (1970s–1990s): LISP Tutor, Cognitive Tutors
- Web-based adaptive systems (2000s): AEH (Adaptive Educational Hypermedia)
- Modern platforms (2010s–present): ALEKS, Khan Academy, Duolingo
- The shift from rule-based to data-driven adaptation

#### 2.1.3 Adaptive Learning for Programming (500–700 words)
**Content:**
- Specific challenges of programming education (Robins et al., 2003)
- Existing adaptive programming platforms: CodeWorkout, Problets, PCRS
- Why programming is different: code as artifact, debugging as skill, multiple solution paths
- Gap analysis: what current platforms miss

### 2.2 Knowledge Tracing (2,000–2,500 words)

#### 2.2.1 Bayesian Knowledge Tracing — BKT (500–700 words)
**Content:**
- Original formulation (Corbett & Anderson, 1994)
- Four parameters: P(L₀), P(T), P(G), P(S)
- Hidden Markov Model interpretation
- Strengths: interpretable, well-studied
- Limitations: binary skill states, no forgetting, assumes skill independence

#### 2.2.2 Deep Knowledge Tracing — DKT (400–600 words)
**Content:**
- Original DKT (Piech et al., 2015) — LSTM-based
- Improvements: DKT+ (regularization), DKVMN (memory-augmented)
- Input encoding: one-hot skill × correctness
- Advantages over BKT: captures complex dependencies, no manual feature engineering

#### 2.2.3 State-of-the-Art: DKT2, UKT, srcML-DKT (600–800 words)
**Content:**
- **DKT2** (Doan & Sahebi, ECML-PKDD 2025): xLSTM backbone + IRT integration, SOTA on 5 benchmarks
- **UKT** (AAAI 2025): Uncertainty-aware KT, probability distributions instead of point estimates
- **srcML-DKT** (EDM 2025): Code-specific KT, uses source code features from submitted programs
- Comparison table: BKT vs DKT vs DKT2 vs srcML-DKT

**Writing guidance:** Present a clear evolution narrative — each method addresses limitations of the previous one. End with justification for choosing BKT (simplicity, interpretability) as baseline with optional DKT2 upgrade path.

#### 2.2.4 Knowledge Tracing for Programming (300–400 words)
**Content:**
- Special considerations: code submissions contain rich signals beyond binary correctness
- Features extractable from code: time spent, number of attempts, error types, code similarity
- Why BKT is a good starting point for programming (clear skill decomposition by concept)

### 2.3 Spaced Repetition (1,000–1,500 words)

#### 2.3.1 The Forgetting Curve and Memory Models (300–400 words)
**Content:**
- Ebbinghaus forgetting curve (1885)
- Spacing effect: distributed practice > massed practice
- Desirable difficulties theory (Bjork & Bjork, 2011)

#### 2.3.2 SM-2 and Traditional Algorithms (300–400 words)
**Content:**
- SuperMemo SM-2 algorithm (Wozniak, 1990)
- Leitner system
- Limitations: fixed parameters, no individual adaptation

#### 2.3.3 FSRS — Free Spaced Repetition Scheduler (400–600 words)
**Content:**
- FSRS formulation (Ye, 2023): three memory states (D, S, R)
- D = Difficulty, S = Stability (half-life), R = Retrievability (probability of recall)
- Mathematical model: R(t) = (1 + t/(9·S))^(-1)
- Parameter optimization via user review history
- 20–30% fewer reviews than SM-2 (empirically validated)
- Now integrated into Anki 23.10+

#### 2.3.4 Spaced Repetition for Programming Skills (200–300 words)
**Content:**
- Novel application: treating programming concepts as "flashcards"
- Difference: reviewing a concept = solving a problem, not recalling a fact
- Proposed adaptation: FSRS rating mapped from submission outcome (ACCEPTED on first try = "Easy", multiple attempts = "Hard", etc.)

### 2.4 Multi-Armed Bandits in Education (1,000–1,500 words)

#### 2.4.1 MAB Problem Formulation (300–400 words)
**Content:**
- Classic MAB: exploration vs exploitation tradeoff
- Thompson Sampling, UCB algorithms
- Why MAB is natural for educational recommendation: each problem is an "arm," reward is learning gain

#### 2.4.2 Hierarchical MAB for Problem Selection (400–600 words)
**Content:**
- Two-level hierarchy: Level 1 selects concept, Level 2 selects difficulty within concept
- Reward function: learning gain = Δ(knowledge state) after attempting problem
- Thompson Sampling with Beta priors
- Reference: Hierarchical MAB framework for adaptive learning

#### 2.4.3 MAB with Abandonment and Disengagement (200–300 words)
**Content:**
- NeurIPS 2024 paper: accounting for user abandonment in MAB
- Modified reward: includes negative signal when student gives up
- Relevance: programming exercises have high abandonment rates for too-hard problems

### 2.5 Elo Rating and Item Response Theory (1,000–1,500 words)

#### 2.5.1 Classical Elo Rating (300–400 words)
**Content:**
- Original Elo system (Elo, 1978) for chess
- Expected score formula: E(A) = 1 / (1 + 10^((R_B - R_A)/400))
- Update rule: R'_A = R_A + K(S_A - E_A)
- Application to education: student = player, problem = opponent

#### 2.5.2 Item Response Theory Connection (300–400 words)
**Content:**
- Rasch model / 1PL IRT as Elo equivalent
- P(correct) = σ(θ_student - β_problem)
- Connection: Elo converges to IRT estimates asymptotically
- Why Elo is preferred for online settings: incremental updates, no batch refit needed

#### 2.5.3 Dynamic K-Value Elo (400–500 words)
**Content:**
- Springer 2025: K-factor adapts based on learning trend
- Increasing trend → lower K (stable, small updates)
- Decreasing trend → higher K (struggling, needs faster adjustment)
- Mathematical formulation with trend detection
- Advantage over fixed K: faster convergence for struggling students, stability for strong students

#### 2.5.4 Zone of Proximal Development (200–300 words)
**Content:**
- Vygotsky's ZPD theory
- Operationalization: recommend problems where student Elo + 100 ≤ problem Elo ≤ student Elo + 300
- Evidence from Elo-based programming education (ACM TOCE)

### 2.6 Knowledge Graphs and GNNs (800–1,200 words)

#### 2.6.1 Knowledge Graphs for Programming Concepts (300–400 words)
**Content:**
- Concept prerequisite graphs: variables → arrays → sorting → dynamic programming
- ACE methodology for automatic KG construction
- Manual vs automated approaches for university courses

#### 2.6.2 GNN-Based Recommendations (300–400 words)
**Content:**
- Tripartite graph: students–resources–knowledge points
- GNN for learning resource recommendation (NDCG@10 = 0.93)
- Graph Attention Networks for learning path generation

#### 2.6.3 Application in This Thesis (200–300 words)
**Content:**
- How Knowledge Graph feeds into MAB (constrains concept selection to unlocked prerequisites)
- How KG provides structure for BKT (defines skill hierarchy)

### 2.7 Large Language Models in Education (800–1,200 words)

#### 2.7.1 LLMs as Tutoring Agents (300–400 words)
**Content:**
- ChatGPT/GPT-4 for programming tutoring
- PyTutor: Socratic questioning approach
- Risks: hallucination, giving answers directly, inconsistent pedagogy

#### 2.7.2 RAG-Enhanced Educational Systems (300–400 words)
**Content:**
- KG + RAG + LLM hybrid (ScienceDirect 2025): combines structured knowledge with generative AI
- Results: hybrid approach outperforms both adaptive-only and GenAI-only
- Multimodal KG + RAG (Frontiers 2026)

#### 2.7.3 LLM Integration in This Thesis (200–300 words)
**Content:**
- Proposed Layer 5: LLM generates contextual hints based on student's code, knowledge state, and concept prerequisites
- RAG retrieves relevant concepts from KG to ground LLM responses
- This is a "nice to have" layer — the core thesis stands without it

### 2.8 Summary and Research Gaps (500–800 words)
**Content:**
- Summary table: what each reviewed technique addresses
- Gap identification: no existing system integrates all 5 layers
- Commercial platforms comparison (LeetCode, HackerRank, Codeforces) — none use KT+Elo+MAB+FSRS
- Position this thesis: filling the integration gap

---

## Chapter 3: System Design & Architecture (6,000–8,000 words)

### 3.1 Requirements Analysis (800–1,000 words)

#### 3.1.1 Functional Requirements (400–500 words)
**Content:**
- FR1: User authentication and role management (student, instructor, admin)
- FR2: Problem management with test cases and tagging
- FR3: Sandboxed code execution with multiple language support
- FR4: Knowledge tracing — track mastery probability per concept per student
- FR5: Difficulty calibration — maintain Elo ratings for students and problems
- FR6: Adaptive problem selection — recommend problems matching student's ZPD
- FR7: Review scheduling — schedule concept reviews using spaced repetition
- FR8: Progress dashboard with skill visualization
- FR9: Hint generation using LLM (optional)

#### 3.1.2 Non-Functional Requirements (200–300 words)
**Content:**
- NFR1: Code execution within 5 seconds
- NFR2: Recommendation generation within 500ms
- NFR3: Support 100+ concurrent users
- NFR4: Secure sandboxed execution (no network, memory limits)
- NFR5: Extensible architecture for adding new algorithms

#### 3.1.3 Use Case Diagrams (200–300 words)
**Content:**
- Student use cases: browse problems, submit code, view recommendations, track progress, review scheduled concepts
- Instructor use cases: create problems, manage courses, view class analytics
- System use cases: compute KT, update Elo, select problems, schedule reviews

### 3.2 Current System Analysis (800–1,000 words)

#### 3.2.1 Existing Architecture (400–500 words)
**Content:**
- Three-tier: React frontend + NestJS API + PostgreSQL (with pgvector)
- AI service: FastAPI with Sentence Transformers
- Code execution: Docker sandbox
- Current recommendation: content-based filtering with cosine similarity

#### 3.2.2 Weaknesses of Current Approach (400–500 words)
**Content:**
- No learner model (no knowledge tracing)
- Static difficulty labels (EASY/MEDIUM/HARD) not personalized
- Cosine similarity recommends similar problems, not optimal ones
- No exploration-exploitation balance
- No temporal modeling (forgetting)
- No prerequisite awareness

### 3.3 Proposed 5-Layer Architecture (2,000–2,500 words)

#### 3.3.1 Architecture Overview (400–500 words)
**Content:**
- Layer diagram (text-based)
- Each layer's responsibility
- How layers communicate (data flow)
- Design principles: modularity, each layer can be upgraded independently

```
┌─────────────────────────────────────────────┐
│  Layer 5: LLM Feedback (RAG + KG + LLM)    │
├─────────────────────────────────────────────┤
│  Layer 4: Review Scheduler (FSRS)           │
├─────────────────────────────────────────────┤
│  Layer 3: Problem Selector (Hierarchical MAB)│
├─────────────────────────────────────────────┤
│  Layer 2: Difficulty Calibrator (Dynamic Elo)│
├─────────────────────────────────────────────┤
│  Layer 1: Knowledge Tracer (BKT / DKT2)    │
├─────────────────────────────────────────────┤
│  Foundation: Knowledge Graph                 │
└─────────────────────────────────────────────┘
```

#### 3.3.2 Layer 1: Knowledge Tracing (400–500 words)
**Content:**
- BKT implementation details
- Input: submission events (student, concept, correct/incorrect)
- Output: P(mastery) per concept per student
- State transition diagram
- Parameters: P(L₀), P(T), P(G), P(S) — initialized from research defaults, tuned per concept
- Update trigger: after each submission

#### 3.3.3 Layer 2: Difficulty Calibration (400–500 words)
**Content:**
- Dual Elo system: every student has an Elo, every problem has an Elo
- Dynamic K-value based on trend detection
- Expected score calculation
- Rating update after each submission
- Initial ratings: Student = 1200, Problem mapped from tags (EASY=1000, MEDIUM=1400, HARD=1800)

#### 3.3.4 Layer 3: Problem Selection (400–500 words)
**Content:**
- Hierarchical MAB: Level 1 = concept selection, Level 2 = problem selection within concept
- Thompson Sampling with Beta(α, β) priors
- Reward function: combines correctness, time efficiency, learning gain
- Prerequisite constraint: only select concepts whose prerequisites are mastered (P(mastery) > 0.8)
- ZPD constraint: only select problems in student's Elo range (+100 to +300)

#### 3.3.5 Layer 4: Review Scheduling (300–400 words)
**Content:**
- FSRS integration for each (student, concept) pair
- Three memory states: Difficulty, Stability, Retrievability
- Review trigger: when Retrievability drops below 0.9
- Rating mapping: ACCEPTED first try → 4 (Easy), ACCEPTED with help → 3 (Good), ACCEPTED after many attempts → 2 (Hard), WRONG → 1 (Again)
- Interplay with MAB: MAB checks FSRS queue before exploring new concepts

#### 3.3.6 Layer 5: LLM Feedback (200–300 words)
**Content:**
- Optional layer for hint generation
- RAG retrieves concept prerequisites and common mistakes from KG
- LLM generates Socratic hints (not direct answers)
- Activated when student has ≥3 failed attempts on a problem

### 3.4 Data Flow Design (1,000–1,500 words)

#### 3.4.1 Recommendation Flow (400–500 words)
**Content:**
- Step-by-step: request → KT query → FSRS check → MAB decision → Elo filter → return problems
- Sequence diagram (text-based)

#### 3.4.2 Submission Processing Flow (400–500 words)
**Content:**
- Step-by-step: submit → execute → evaluate → update KT → update Elo → update FSRS → update MAB → update dashboard
- All updates are asynchronous after execution result

#### 3.4.3 Cold Start Handling (200–300 words)
**Content:**
- New student: initial BKT parameters, default Elo (1200), recommend easiest prerequisite-free concepts
- New problem: initial Elo from difficulty tag, no BKT data until first submission

### 3.5 Database Schema Design (800–1,000 words)

#### 3.5.1 New Tables (500–700 words)
**Content:**
- `knowledge_state`: (student_id, concept_id, p_mastery, p_L0, p_T, p_G, p_S, updated_at)
- `elo_rating`: (entity_id, entity_type [STUDENT|PROBLEM], rating, k_value, trend, n_attempts, updated_at)
- `mab_state`: (student_id, concept_id, alpha, beta, level, updated_at)
- `fsrs_card`: (student_id, concept_id, difficulty, stability, retrievability, due_date, last_review, reps, updated_at)
- `knowledge_graph_edge`: (from_concept_id, to_concept_id, relation_type [PREREQUISITE|RELATED])
- `concept`: (id, name, description, topic_group)
- `problem_concept`: (problem_id, concept_id) — maps problems to KG concepts

#### 3.5.2 Schema Migration Strategy (200–300 words)
**Content:**
- Backward compatible: new tables only, no modification to existing tables
- Data migration: map existing tags to concepts
- Prisma migration approach

### 3.6 API Design (800–1,000 words)

#### 3.6.1 New API Endpoints (500–700 words)
**Content:**
- `GET /api/recommend/adaptive/:userId` — full adaptive recommendation
- `GET /api/knowledge-state/:userId` — current mastery per concept
- `GET /api/elo/:userId` — student's Elo and history
- `GET /api/review-queue/:userId` — FSRS due reviews
- `POST /api/knowledge-graph/edges` — manage KG (instructor)
- `GET /api/analytics/class/:courseId` — class-level analytics (instructor)

#### 3.6.2 Modification to Existing Endpoints (200–300 words)
**Content:**
- `POST /api/submissions` — add post-submission hooks to update all layers
- `GET /api/dashboard` — add adaptive metrics (mastery, Elo, review queue)

---

## Chapter 4: Implementation (5,000–7,000 words)

### 4.1 Technology Stack (500–700 words)
**Content:**
- Justify each technology choice:
  - React + TypeScript + Ant Design for frontend
  - NestJS + Prisma for backend API
  - FastAPI + Python for AI service (BKT, Elo, MAB, FSRS)
  - PostgreSQL + pgvector for persistence
  - Docker for sandboxed code execution
  - Redis for caching and MAB state

### 4.2 Knowledge Graph Construction (600–800 words)
**Content:**
- Manual curation for university Python course
- Concept taxonomy: variables → data types → control flow → functions → OOP → data structures → algorithms
- Prerequisite relationships
- Mapping existing problems to concepts
- Future: ACE methodology for automated KG construction

### 4.3 Layer 1 Implementation: Knowledge Tracing (800–1,000 words)

#### 4.3.1 BKT Implementation (500–700 words)
**Content:**
- Python implementation using pyBKT or custom
- Parameter initialization strategy
- Update algorithm with code walkthrough
- Per-concept parameter fitting

#### 4.3.2 Integration with Submission Pipeline (200–300 words)
**Content:**
- Event-driven: submission result → message queue → BKT update
- Async processing to avoid latency impact

### 4.4 Layer 2 Implementation: Elo System (800–1,000 words)

#### 4.4.1 Dual Elo Implementation (500–700 words)
**Content:**
- Student Elo initialization and update
- Problem Elo initialization from difficulty tag and calibration from submissions
- Dynamic K-value calculation with trend detection
- Code walkthrough of rating update

#### 4.4.2 ZPD Filtering (200–300 words)
**Content:**
- Query: find problems where |student_elo - problem_elo| is in [100, 300]
- Edge cases: very high or very low rated students

### 4.5 Layer 3 Implementation: Hierarchical MAB (600–800 words)
**Content:**
- Thompson Sampling implementation
- Two-level hierarchy: concept → difficulty
- Reward calculation from submission outcomes
- Prerequisite filtering using KG
- Exploration bonus for new concepts

### 4.6 Layer 4 Implementation: FSRS (600–800 words)
**Content:**
- FSRS-5 algorithm implementation (or ts-fsrs library)
- Card creation on first encounter with concept
- Rating mapping from submission outcomes
- Review queue management
- Integration with MAB: review takes priority over exploration

### 4.7 Layer 5 Implementation: LLM Feedback (400–600 words)
**Content:**
- Optional implementation
- RAG pipeline: student error → retrieve concept from KG → generate hint
- Prompt engineering for Socratic questioning
- Rate limiting and cost management

### 4.8 Frontend Implementation (600–800 words)
**Content:**
- Dashboard enhancements: mastery radar chart, Elo history graph, review queue
- Problem page: adaptive difficulty indicator, hint button
- Progress page: concept mastery tree, predicted review schedule

### 4.9 Deployment (400–500 words)
**Content:**
- Docker Compose orchestration
- Environment configuration
- Monitoring and logging

---

## Chapter 5: Evaluation & Experiments (5,000–7,000 words)

### 5.1 Research Methodology (500–700 words)
**Content:**
- Mixed methods: quantitative (system metrics) + qualitative (surveys, interviews)
- Experiment design: pre-test / post-test with control group
- Ethical considerations: informed consent, data anonymization

### 5.2 Experiment Design (1,000–1,500 words)

#### 5.2.1 Participants (300–400 words)
**Content:**
- Target: 40–60 students from Hanoi University programming courses
- Random assignment to experimental (adaptive) and control (non-adaptive) groups
- Pre-test to establish baseline knowledge

#### 5.2.2 Protocol (400–600 words)
**Content:**
- Week 1: Pre-test, system training
- Weeks 2–5: Students use system (experimental: adaptive, control: random/manual selection)
- Week 6: Post-test, surveys, interviews
- Data collection throughout: all submissions, recommendations, click patterns

#### 5.2.3 Variables (200–300 words)
**Content:**
- Independent: treatment group (adaptive vs non-adaptive)
- Dependent: learning gain, engagement, satisfaction, recommendation accuracy

### 5.3 Evaluation Metrics (1,000–1,500 words)

#### 5.3.1 Learning Effectiveness Metrics (400–500 words)
**Content:**
- Normalized Learning Gain: NLG = (post - pre) / (max - pre)
- Problem-solving accuracy over time
- Concept mastery progression (BKT P(mastery) trajectories)
- Time to mastery per concept

#### 5.3.2 Recommendation Quality Metrics (300–400 words)
**Content:**
- Acceptance rate: % of recommended problems attempted
- Completion rate: % of attempted recommendations solved
- AUC of BKT predictions (does KT accurately predict correctness?)
- Elo prediction accuracy

#### 5.3.3 Engagement Metrics (200–300 words)
**Content:**
- Session frequency and duration
- Problems attempted per session
- Voluntary return rate
- Dropout/abandonment rate

#### 5.3.4 Usability Metrics (200–300 words)
**Content:**
- System Usability Scale (SUS) score
- Technology Acceptance Model (TAM): Perceived Usefulness, Perceived Ease of Use
- Net Promoter Score (NPS)

### 5.4 Results (1,500–2,000 words)
**Content:** [To be written after experiments]
- Descriptive statistics for each metric
- Comparison between groups (t-test or Mann-Whitney U)
- Effect sizes (Cohen's d)
- Learning curves visualization
- BKT accuracy evaluation
- Elo convergence analysis
- Survey results summary

### 5.5 Discussion (800–1,000 words)
**Content:** [To be written after experiments]
- Interpretation of results in context of research questions
- Comparison with related work results
- Threats to validity (internal, external, construct)
- Unexpected findings

---

## Chapter 6: Conclusion & Future Work (2,000–3,000 words)

### 6.1 Summary of Contributions (600–800 words)
**Content:**
- Restate each contribution with evidence from evaluation
- Connect back to research objectives and questions
- What was achieved vs what was planned

### 6.2 Key Findings (400–600 words)
**Content:**
- Most impactful result from each layer
- Which layer contributed most to learning improvement
- Practical insights for deploying adaptive systems

### 6.3 Limitations (400–500 words)
**Content:**
- Sample size and generalizability
- Short evaluation period
- Single language (Python) and single university
- Cold start problem for new users and new problems
- Computational cost of running 5 layers

### 6.4 Future Work (400–600 words)
**Content:**
- Multi-language support (Java, C++, JavaScript)
- Integration with university LMS (Moodle)
- Advanced KT: upgrade from BKT to DKT2
- Automated Knowledge Graph construction using LLM
- Mobile application
- Longitudinal study (full academic year)
- Open-source release and community

### 6.5 Closing Remarks (200–300 words)
**Content:**
- Vision for adaptive programming education
- Broader impact on Vietnamese CS education
- Call to action for educators and researchers

---

## Appendices

### Appendix A: Survey Instruments
- SUS questionnaire (10 items)
- TAM questionnaire (12 items)
- Post-experiment interview guide (5–8 questions)

### Appendix B: Knowledge Graph
- Complete concept map for Python programming course
- Prerequisite relationship table

### Appendix C: Algorithm Parameters
- BKT default parameters per concept
- Elo initial ratings
- FSRS default parameters
- MAB hyperparameters

### Appendix D: Sample Screenshots
- Dashboard, problem page, recommendation list, progress visualization

### Appendix E: Source Code
- Key algorithm implementations (not full codebase)
- Deployment configuration

### Appendix F: Ethics Approval
- Informed consent form
- Data handling protocol

---

## Writing Timeline Suggestion

| Phase | Chapters | Target Date | Notes |
|-------|----------|-------------|-------|
| 1 | Ch 2 (Literature Review) | March 2026 | Can write now — all research done |
| 2 | Ch 3 (System Design) | March 2026 | Can write now — design complete |
| 3 | Implementation (Layers 1–3) | April 2026 | Core adaptive engine |
| 4 | Ch 4 (Implementation) | April 2026 | Write alongside implementation |
| 5 | Implementation (Layers 4–5) | May 2026 | FSRS + LLM |
| 6 | Run experiments | May–June 2026 | Requires deployed system |
| 7 | Ch 5 (Evaluation) | June 2026 | Write after experiments |
| 8 | Ch 1 + Ch 6 | June 2026 | Write last (needs full picture) |
| 9 | Abstract + Polish | July 2026 | Final revision |
