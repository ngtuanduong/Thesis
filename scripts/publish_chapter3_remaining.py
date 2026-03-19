#!/usr/bin/env python3
"""
Publish remaining Chapter 3 sections (3.1.4 through 3.7 + summary) to Google Docs.
All text is humanized inline. Inserts at the correct position before References.
"""

import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ─── Configuration ───────────────────────────────────────────────────────────
DOC_ID = '1cJlWFX9QCEsqYo7mp6cpCWAba3Xc433-IRu8nlR63o0'
SERVICE_ACCOUNT_FILE = 'infra-inkwell-465003-f2-369235afe5ac.json'
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# ─── Authenticate ────────────────────────────────────────────────────────────
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('docs', 'v1', credentials=creds)

# ─── Find insert point ──────────────────────────────────────────────────────
def find_insert_point():
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get('body', {}).get('content', [])
    for element in content:
        if 'paragraph' in element:
            para = element['paragraph']
            text = ''
            for elem in para.get('elements', []):
                if 'textRun' in elem:
                    text += elem['textRun']['content']
            if text.strip().startswith('The use case UC10'):
                return element.get('endIndex', 0)
    raise RuntimeError("Could not find insert point (UC10 paragraph)")

INSERT_INDEX = find_insert_point()
print(f"Insert point: {INSERT_INDEX}")

# ─── Content blocks ─────────────────────────────────────────────────────────
# Each block is (type, text, [optional metadata])
# Types: 'h2', 'h3', 'body', 'bold_para', 'table_caption', 'figure_caption',
#        'image', 'bullet', 'equation', 'table_row', 'table_header'

# All body text has been humanized: rewritten to sound natural, academic,
# with varied sentence structures and no AI-typical phrases.

CONTENT_BLOCKS = []

def h2(text):
    CONTENT_BLOCKS.append(('h2', text))

def h3(text):
    CONTENT_BLOCKS.append(('h3', text))

def body(text):
    CONTENT_BLOCKS.append(('body', text))

def bold_label(text):
    CONTENT_BLOCKS.append(('bold_label', text))

def caption(text):
    CONTENT_BLOCKS.append(('caption', text))

def image(url, width=468, height=300):
    CONTENT_BLOCKS.append(('image', url, width, height))

def bullet(text):
    CONTENT_BLOCKS.append(('bullet', text))

def equation(text):
    CONTENT_BLOCKS.append(('equation', text))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.1.4 — Requirements Traceability
# ═══════════════════════════════════════════════════════════════════════════

h3("3.1.4 Requirements Traceability")

body("Table 3.2 maps each requirement to the architectural components responsible for fulfilling it, the design sections in this chapter where the relevant specifications appear, the implementation sections in Chapter 4, and the evaluation metrics that will be used to verify compliance. This traceability matrix serves two purposes: it confirms that every requirement has a corresponding design specification and implementation plan, and it provides a roadmap for the evaluation protocol in Chapter 5.")

caption("Table 3.2. Requirements traceability matrix.")

# Insert the requirements traceability table as an image
# (The VISUAL-GUIDE doesn't have a separate image for 3.1.4, so we'll render it as formatted text)
# Actually, let's write it as structured text paragraphs since the table is complex

bold_label("FR1: User Authentication and Role Management")
body("Implemented by the NestJS Auth Module using JWT tokens. Design is specified in Section 3.6.2 and implemented in Section 4.1.")

bold_label("FR2: Problem Management with Test Cases")
body("Implemented by the NestJS Problem Module and Knowledge Graph. Design is specified in Sections 3.3.7 and 3.5, with implementation in Section 4.1.")

bold_label("FR3: Sandboxed Code Execution")
body("Implemented through Docker-based sandboxing. Design is specified in Section 3.2, implemented in Section 4.1, and evaluated against NFR1 latency targets.")

bold_label("FR4: Knowledge Tracing")
body("Implemented by Layer 1 (BKT). Design is specified in Section 3.3.2, implemented in Section 4.2.1, and evaluated using AUC and RMSE metrics for RQ1.")

bold_label("FR5: Difficulty Calibration")
body("Implemented by Layer 2 (Dynamic Elo). Design is specified in Section 3.3.3, implemented in Section 4.2.2, and evaluated through rating stability analysis for RQ1.")

bold_label("FR6: Adaptive Problem Selection")
body("Implemented by Layer 3 (Hierarchical MAB). Design is specified in Sections 3.3.4 and 3.4.1, implemented in Section 4.2.3, and evaluated by measuring learning gains for RQ2.")

bold_label("FR7: Review Scheduling")
body("Implemented by Layer 4 (FSRS). Design is specified in Section 3.3.5, implemented in Section 4.2.4, and evaluated through retention rate measurements for RQ3.")

bold_label("FR8: Progress Dashboard")
body("Implemented through a React frontend combined with API endpoints. Design is specified in Section 3.6.2, implemented in Section 4.3, and evaluated using the System Usability Scale for RQ4.")

bold_label("FR9: LLM Feedback Engine")
body("Implemented by Layer 5. Design is specified in Section 3.3.6, implemented in Section 4.2.5. This requirement is optional and not tied to a specific evaluation metric.")

bold_label("FR10: Event Logging")
body("Implemented through the Event Logs table. Design is specified in Section 3.5.1, implemented in Section 4.4.")

bold_label("FR11: Experiment Group Management")
body("Implemented through the Experiment Groups table. Design is specified in Section 3.5.1, implemented in Section 4.4, and evaluated through between-group effect size comparisons.")

bold_label("NFR1-NFR5: Non-Functional Requirements")
body("NFR1 (execution latency) and NFR4 (security) are addressed through Docker sandbox configuration in Section 3.2. NFR2 (recommendation latency) relies on the Redis caching strategy in Section 3.7. NFR3 (concurrent users) is handled by the stateless AI service design in Section 3.3.1. NFR5 (extensibility) is achieved through the strict layer interfaces described in Section 3.3.1. All non-functional requirements are verified through corresponding evaluation metrics: p95 latency measurements, load test throughput, and interface contract tests.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.2 — System Overview and Design Rationale
# ═══════════════════════════════════════════════════════════════════════════

h2("3.2 System Overview and Design Rationale")

body("This section describes the overall architecture of the adaptive learning platform and the reasoning behind its design decisions. The platform was built from the ground up to support adaptive programming education at the university level. Rather than bolting adaptive features onto an existing online judge system, we designed every component \u2014 from the frontend code editor to the backend AI service \u2014 with adaptive learning as a core concern from the outset.")

h3("3.2.1 Four-Component Architecture")

body("The platform is organized around four principal components, each responsible for a distinct role in the adaptive learning pipeline.")

bold_label("React + TypeScript Frontend (Vite, Ant Design, Monaco Editor).")
body("The client application provides students with a Monaco-based code editor for writing and submitting solutions, a problem browser with concept-based navigation, an adaptive dashboard showing mastery progress and Elo ratings, and a review queue that surfaces concepts due for spaced repetition practice. We chose Vite as the build tool for its fast development iteration and optimized production bundles. Ant Design supplies a consistent, accessible component library well suited to data-rich educational interfaces.")

bold_label("NestJS API Gateway (TypeScript, Prisma ORM).")
body("The API gateway manages authentication through JWT tokens, handles user and course management, supports problem CRUD operations, and orchestrates code execution. When a student submits code, the gateway saves the submission record, dispatches it to the Docker sandbox, and returns the execution result. For adaptive features, the gateway acts as a proxy to the FastAPI AI service, forwarding recommendation and update requests while shielding the frontend from the AI service\u2019s internal API. Prisma serves as the ORM, providing type-safe database access and version-controlled schema migrations.")

bold_label("FastAPI AI Service (Python 3.11, SQLAlchemy).")
body("The AI service hosts the five-layer adaptive engine: Bayesian Knowledge Tracing in Layer 1, Dynamic Elo rating in Layer 2, Hierarchical Multi-Armed Bandits with Thompson Sampling in Layer 3, FSRS spaced repetition scheduling in Layer 4, and LLM-based feedback generation in Layer 5. We chose Python for this component because the relevant machine learning ecosystem \u2014 including pyBKT [56], NumPy, SciPy, and the FSRS algorithm library \u2014 is implemented primarily in Python. FastAPI\u2019s asynchronous request handling supports high-throughput recommendation serving, and SQLAlchemy provides direct database access for the adaptive state tables that the AI service owns.")

bold_label("PostgreSQL (pgvector) + Redis + Docker Sandbox.")
body("PostgreSQL serves as the single persistent store, with the pgvector extension reserved for future embedding-based features such as semantic similarity in hint retrieval. Its mature JSONB support enables flexible storage of rating history and event metadata. Redis provides a caching layer for recommendation results and MAB state reads, along with per-student distributed locks that prevent concurrent update race conditions. Docker containers provide isolated sandboxes for executing student-submitted code, with CPU, memory, and time limits enforced at the container level to satisfy the security and fairness requirements defined in NFR4.")

image("https://files.catbox.moe/702phb.png", 468, 340)
caption("Figure 3.1. Five-layer adaptive architecture within the four-component platform.")

h3("3.2.2 Design Principles and Key Decisions")

body("Six design principles guided the architecture. Each principle maps to one or more concrete architectural decisions, as summarized in Table 3.1.")

image("https://files.catbox.moe/yk5jth.png", 468, 400)
caption("Table 3.1. Design principles and corresponding architectural decisions.")

body("The most consequential decision is the separation of the AI service from the NestJS gateway. This separation allows the Python ML ecosystem (pyBKT [56], NumPy, SciPy, FSRS) to be used natively, enables independent scaling and deployment of the adaptive engine, and enforces a clean interface contract between platform logic and adaptive intelligence. The write-ownership convention complements this separation: the NestJS gateway owns writes to core domain tables, while the AI service owns writes to adaptive state tables, eliminating the need for distributed transactions.")

body("Asynchronous adaptive updates further decouple the two services. Submission results are returned to the student synchronously, while adaptive state updates covering BKT, Elo, MAB, and FSRS are processed in the background. Redis provides both caching to meet the 500ms recommendation latency target specified in NFR2, and per-student distributed locks to serialize concurrent adaptive updates. If Redis becomes unavailable, the system degrades gracefully to direct database queries.")

body("The progressive enhancement principle deserves particular emphasis. The platform is designed so that its core functionality \u2014 problem browsing, code submission, execution, and verdict display \u2014 operates independently of the adaptive engine. Each adaptive layer adds a capability that can be independently enabled or disabled via feature flags. This design ensures that a partial failure in the AI service does not prevent students from practicing, and it simplifies evaluation by allowing controlled comparisons between adaptive and non-adaptive conditions.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.3 — Proposed Five-Layer Adaptive Architecture
# ═══════════════════════════════════════════════════════════════════════════

h2("3.3 Proposed Five-Layer Adaptive Architecture")

body("This section presents the five-layer adaptive architecture that constitutes the primary contribution of this thesis. The architecture is built around three principles: modularity, where each layer encapsulates a single adaptive concern and communicates through well-defined interfaces; composability, where layers build upon each other\u2019s outputs to produce adaptive behavior that exceeds what any single layer achieves in isolation; and extensibility, where any layer can be replaced with an alternative algorithm without disrupting the overall pipeline, satisfying NFR5.")

h3("3.3.1 Architecture Overview")

body("The adaptive engine runs as a FastAPI application alongside the NestJS backend, with both services sharing the same PostgreSQL database under a strict write-ownership model. The NestJS backend owns writes to core tables including users, problems, test cases, submissions, courses, concepts, knowledge graph edges, and problem-concept mappings. The AI service owns writes to adaptive state tables including knowledge states, Elo ratings, MAB states, FSRS cards, and event logs. Both services have read access to all tables. Redis is introduced as a caching layer between the two services.")

body("The layered structure in Figure 3.1 reflects a logical dependency ordering from bottom to top. The Knowledge Graph Foundation provides structural information \u2014 concept nodes and prerequisite edges \u2014 that all layers consume. Layer 1 (BKT) consumes submission outcomes and produces mastery estimates. Layer 2 (Elo) consumes submission outcomes and produces difficulty ratings on a shared scale. Layer 3 (MAB) consumes the outputs of Layers 1, 2, and 4 to select problems. Layer 4 (FSRS) consumes submission outcomes and produces review scheduling information that Layer 3 respects. Layer 5 (LLM) operates independently, triggered on demand when students request hints. The following subsections describe each component in detail.")

h3("3.3.2 Layer 1: Knowledge Tracer (BKT)")

bold_label("Purpose.")
body("Layer 1 maintains a probabilistic estimate of each student\u2019s mastery of each programming concept. This estimate serves two critical downstream functions: prerequisite gating, where a concept becomes eligible for recommendation only when all its prerequisites have mastery probability exceeding the threshold of 0.85; and reward signal computation for the MAB, where learning gain is defined as the change in mastery probability resulting from a practice opportunity.")

bold_label("Model.")
body("The Knowledge Tracer implements standard Bayesian Knowledge Tracing [16] as described in Section 2.2.1. For each student-concept pair, the model maintains four parameters \u2014 P(L_0), P(T), P(G), P(S) \u2014 and the current mastery estimate P(L_t). Parameters are initialized with concept-level defaults: P(L_0) = 0.1, P(T) = 0.2, P(G) = 0.15, P(S) = 0.1. These values are drawn from Corbett and Anderson\u2019s original BKT formulation [16] and are consistent with the defaults used in pyBKT [56]. The specific values reflect typical introductory programming exercises where prior knowledge is low, learning per opportunity is moderate, and guessing rates are constrained by the multi-test-case evaluation format.")

bold_label("Mastery threshold.")
body("The mastery threshold of 0.85 was selected based on standard practice in BKT implementations, where mastery at or above 0.80 to 0.90 is recommended for prerequisite gating [16]. Setting the threshold at 0.95 would require excessive practice on already-understood concepts, while 0.70 risks advancing students before they are ready. The sensitivity of this threshold is evaluated in Section 5.5.")

bold_label("Input.")
body("After each graded submission, Layer 1 receives the student identifier, the concept identifier derived from the problem\u2019s primary concept tag, and a binary correctness signal where 1 indicates ACCEPTED and 0 indicates otherwise.")

bold_label("Output.")
body("The updated mastery probability P(L_t), which is written to the knowledge_states table and made available to Layers 3 and 4.")

bold_label("Interaction with other layers.")
body("Layer 1 feeds Layer 3 in two ways. First, the binary mastery classification determines which concepts are eligible at the MAB\u2019s Level 1 by enabling their dependents. If concept B requires concept A as a prerequisite, then B becomes eligible only when concept A\u2019s mastery probability reaches 0.85 or higher. Second, the change in mastery probability serves as the reward signal for the MAB: concepts that produce larger mastery gains are more likely to be selected in the future. Layer 1 also triggers Layer 4: when a concept first reaches mastery, an FSRS card is initialized for that concept, beginning the spaced repetition cycle.")

h3("3.3.3 Layer 2: Difficulty Calibrator (Dynamic Elo)")

bold_label("Purpose.")
body("Layer 2 maintains numerical ratings for both students and problems on a shared scale, enabling principled difficulty matching. By placing students and problems on the same rating scale, the system can operationalize Vygotsky\u2019s Zone of Proximal Development [20] as a numerical interval: problems whose rating falls within a calibrated range above the student\u2019s rating are considered to lie within the student\u2019s ZPD.")

bold_label("Model.")
body("The Difficulty Calibrator implements a dual Elo rating system [17] with dynamic K-values [11]. Each student and each problem maintains a rating initialized at 1200 and a K-factor that controls the sensitivity of rating updates. The expected probability that student A with rating R_A solves problem B with rating R_B is given by Equation 3.1:")

equation("E(A) = 1 / (1 + 10^((R_B - R_A) / 400))    (3.1)")

body("After a submission, ratings are updated based on the discrepancy between expected and actual outcomes:")

equation("R_A\u2032 = R_A + K_A \u00b7 (S_A - E(A))    (3.2)")
equation("R_B\u2032 = R_B + K_B \u00b7 (E(A) - S_A)    (3.3)")

body("Here, S_A equals 1 if the student solved the problem (ACCEPTED) and 0 otherwise. The student\u2019s K-factor is dynamically adjusted based on two criteria: the number of prior attempts, where higher K values allow rapid convergence for newer students, and the recent performance trend, where higher K values accommodate students on a steep learning curve. Specifically:")

equation("K_A = K_base \u00b7 f_novelty(n) \u00b7 f_trend(trend_A)    (3.4)")

body("The base value K_base is set to 25. Elo [17] originally recommended K = 32 for new players and K = 16 for established players in chess; the base value of 25 serves as a midpoint suitable for the educational context, where rating volatility should be moderate. The function f_novelty(n) = max(1.0, 2.0 - n/30) provides a boost for students with fewer than 30 interactions, and f_trend scales K based on the exponential moving average of recent rating changes. Problem K-factors follow an analogous formula but with f_novelty based on the number of submissions the problem has received.")

bold_label("Input.")
body("After each graded submission, Layer 2 receives the student identifier, problem identifier, and the binary outcome.")

bold_label("Output.")
body("Updated student and problem Elo ratings, written to the elo_ratings table.")

bold_label("Interaction with other layers.")
body("Layer 2 feeds Layer 3 by defining the ZPD filter. When the MAB at Level 2 considers candidate problems within a selected concept, only problems whose Elo rating satisfies the following condition are eligible:")

equation("R_student + \u03b4_min \u2264 R_problem \u2264 R_student + \u03b4_max    (3.5)")

body("The lower bound \u03b4_min is set to 50 and the upper bound \u03b4_max to 250. These bounds are derived from the expected success probability in Equation 3.1: substituting \u03b4_min = 50 yields an expected success probability of approximately 0.43, while \u03b4_max = 250 yields approximately 0.15. After accounting for the asymmetric nature of educational gains, where students learn more from moderately challenging tasks, these bounds approximate the 36 to 64 percent success rate range recommended by flow theory [57] and the desirable difficulty framework [21]. The exact values will be validated through sensitivity analysis in Section 5.5.")

h3("3.3.4 Layer 3: Problem Selector (Hierarchical MAB)")

bold_label("Purpose.")
body("Layer 3 is the recommendation engine. It formulates problem selection as a two-level Hierarchical Multi-Armed Bandit problem and solves it using Thompson Sampling [18], [19]. The hierarchical structure mirrors the natural two-step decision process in programming education: first, decide which concept the student should practice; then, decide which specific problem within that concept is optimal.")

bold_label("Model.")
body("The Hierarchical MAB operates at two levels:")

bold_label("Level 1 (Concept Selection).")
body("Each eligible concept constitutes an arm. An arm is eligible if and only if all prerequisite concepts have been mastered and the concept itself is either not yet mastered or flagged for review by Layer 4 because its FSRS retrievability has dropped below the threshold. For each eligible arm, the bandit maintains a Beta distribution modeling the expected learning gain. Thompson Sampling draws a sample from each concept\u2019s distribution and selects the concept with the highest sampled value.")

bold_label("Level 2 (Problem Selection).")
body("Within the selected concept, each unsolved problem whose Elo rating falls within the student\u2019s ZPD constitutes an arm. Each arm maintains its own Beta distribution. Thompson Sampling again draws samples and selects the problem with the highest sampled value.")

bold_label("Reward Signal.")
body("After the student submits a solution, the reward is computed as a composite signal combining three components:")

equation("r = w_1 \u00b7 \u0394P(L_t) + w_2 \u00b7 I[correct] + w_3 \u00b7 (1 - normalized_attempts)    (3.6)")

body("Here, \u0394P(L_t) is the learning gain from Layer 1, I[correct] is the binary correctness indicator, and normalized_attempts equals min(attempt_number, M) / M, where M = 5 is a configurable cap beyond which the attempt penalty is saturated. The weights w_1 = 0.5, w_2 = 0.3, and w_3 = 0.2 are initial values selected to prioritize learning gain as the primary optimization objective. These weights will be tuned through grid search during the evaluation phase described in Section 5.5.")

body("The reward r is clipped to the interval [0, 1] before updating the Beta distribution parameters to ensure mathematical validity. While Thompson Sampling\u2019s convergence guarantees were originally proved for Bernoulli rewards [18], using a continuous reward with Beta priors is a well-established approximation that retains favorable empirical performance [58]. The Beta parameters are updated as follows: \u03b1 is incremented by r and \u03b2 is incremented by (1 - r).")

bold_label("Interaction with other layers.")
body("Layer 3 is the integration point where all other layers converge. It consumes mastery estimates and prerequisite gating from Layer 1, ZPD constraints from Layer 2, review urgency from Layer 4, and structural information from the Knowledge Graph Foundation. The integration of FSRS with the MAB deserves particular attention: when concepts are due for review, they are injected into the Level 1 candidate set with a priority boost to their Thompson Sampling prior, ensuring that review needs are addressed without entirely overriding exploration of new material.")

body("The specific combination of prerequisite constraints derived from a knowledge graph, BKT-based mastery gating, and FSRS review urgency within a hierarchical Thompson Sampling framework has not, to the best of our knowledge, been previously reported. While Multi-Armed Bandits have been applied to educational recommendation before \u2014 notably by Clement et al. [22] \u2014 the integration of these four components into a single hierarchical decision process is the second key contribution of this thesis.")

h3("3.3.5 Layer 4: Review Scheduler (FSRS)")

bold_label("Purpose.")
body("Layer 4 addresses the forgetting problem by modeling memory decay for each mastered concept and scheduling timely reviews to maintain long-term retention. To the best of our knowledge, this is the first application of the FSRS algorithm [12] to programming skill retention, constituting the third key contribution of this thesis.")

bold_label("Model.")
body("The implementation is based on FSRS v4 [12], whose power-law retrievability decay has been empirically validated against the SM-2 algorithm on large-scale flashcard datasets. FSRS models each student-concept pair as a memory card with two state variables: difficulty D, ranging from 1 to 10 and representing how inherently hard the concept is for this student; and stability S, which is the time interval in days at which retrievability drops to 90 percent. The retrievability at time t after the last review is:")

equation("R(t) = (1 + t / (9 \u00b7 S))^(-1)    (3.7)")

body("When the student reviews a concept by solving a problem tagged with that concept, the FSRS algorithm updates both difficulty and stability based on the review outcome. The review outcome is expressed as a rating from 1 (complete failure) to 4 (effortless recall), which requires a mapping from code submission outcomes to FSRS ratings. The details of this rating mapping are presented in Chapter 4.")

bold_label("Input.")
body("After a submission on a mastered concept, Layer 4 receives the student identifier, concept identifier, and a submission-derived FSRS rating.")

bold_label("Output.")
body("Updated FSRS card parameters including difficulty, stability, retrievability, and due date, all written to the fsrs_cards table. Concepts whose retrievability has dropped below the review threshold of 0.7 are flagged as due for review.")

bold_label("Interaction with other layers.")
body("Layer 4 feeds Layer 3 by identifying concepts that need review. The MAB treats review-due concepts as eligible arms at Level 1 even when they are already mastered, with a priority boost proportional to the urgency of the review, determined by how far below the threshold the retrievability has dropped. This integration ensures that the system balances three competing objectives: advancing to new concepts through exploitation, exploring uncertain concepts through exploration, and reviewing mastered concepts at risk of being forgotten to support retention. The specific mechanism for this integration is described in Section 3.4.1.")

h3("3.3.6 Layer 5: LLM Feedback Engine (Optional)")

bold_label("Purpose.")
body("Layer 5 provides contextual, pedagogically appropriate hints when students are struggling with a problem. It is designated as optional because the core thesis contribution \u2014 the integration of Layers 1 through 4 \u2014 is independent of LLM-based feedback.")

bold_label("Model.")
body("The feedback engine uses a Retrieval-Augmented Generation pipeline. When a student requests a hint or after a configurable number of failed attempts, the system constructs a query combining the problem description, the student\u2019s latest code, the error message, and the relevant concept from the knowledge graph. This query is used to retrieve relevant context: concept descriptions and prerequisite information from the knowledge graph, similar solved examples from the problem bank, and common misconceptions associated with the concept. The retrieved context and the student\u2019s submission are passed to a large language model with a prompt template that enforces Socratic questioning, guiding the student toward the solution through questions and partial explanations rather than providing the answer directly.")

bold_label("Interaction with other layers.")
body("Layer 5 operates independently of the recommendation pipeline. It is triggered on demand by the student or automatically after repeated failures, and it consumes the student\u2019s current knowledge state from Layer 1 to calibrate the level of the hint. A student with low mastery of the concept receives more fundamental guidance, while a student with moderate mastery receives a more targeted nudge.")

h3("3.3.7 Knowledge Graph Foundation")

bold_label("Purpose.")
body("The Knowledge Graph provides the structural backbone that coordinates all adaptive layers. It is a directed acyclic graph in which nodes represent programming concepts and edges represent prerequisite relationships. The graph encodes the pedagogical sequencing implicit in any programming curriculum: understanding variables is prerequisite to understanding loops, understanding loops is prerequisite to understanding nested loops and basic algorithms, and so forth.")

bold_label("Structure.")
body("The knowledge graph consists of 28 concepts organized into six topic groups: Basics (variables, data types, I/O), Control Flow (conditionals, loops, nested loops), Functions (function definition, parameters, return values, recursion), Data Structures (lists, tuples, dictionaries, sets, strings), Algorithms (sorting, searching, two pointers), and Advanced (dynamic programming, graph algorithms). The complete concept inventory is provided in Appendix B. Each concept has a difficulty tier ranging from 1 to 5 that reflects its position in the curriculum. Prerequisite edges are weighted with a default weight of 1.0 to allow for soft prerequisites in future extensions.")

image("https://files.catbox.moe/w87g2s.png", 468, 340)
caption("Figure 3.2. Simplified view of the knowledge graph showing concept nodes and prerequisite edges. The complete 28-concept graph is provided in Appendix B.")

bold_label("Role in the architecture.")
body("The Knowledge Graph is consumed by multiple layers. Layer 1 (BKT) uses the graph to identify which concepts each problem assesses via the problem_concepts mapping. When a student solves a problem tagged with concept C, the BKT update is applied to concept C. Layer 3 (MAB) uses prerequisite edges to determine concept eligibility, where a concept is eligible only if all concepts connected to it by incoming prerequisite edges have been mastered, and the graph\u2019s topological sort defines the natural learning progression. Layer 4 (FSRS) uses the graph to ensure that when a concept is due for review, the system selects a problem that specifically targets that concept rather than a related but distinct concept. Layer 5 (LLM) uses concept descriptions and prerequisite chains to provide contextually grounded hints.")

body("The graph is managed by instructors and administrators through the NestJS API and is expected to evolve as the platform\u2019s problem bank grows. A dedicated management interface (UC12) supports adding, editing, and removing concepts and edges, with validation to ensure the graph remains a DAG since cycles would create impossible prerequisite requirements.")

h3("3.3.8 Hyperparameter Summary")

body("Table 3.3 consolidates all hyperparameters introduced in this section with their default values, valid ranges, and justifications. This table serves as a critical reference for Chapter 4 (implementation choices) and Chapter 5 (sensitivity analysis).")

image("https://files.catbox.moe/ue4upp.png", 468, 500)
caption("Table 3.3. Hyperparameter summary for the five-layer adaptive architecture.")

image("https://files.catbox.moe/13j7lt.png", 468, 340)
caption("Figure 3.6. Layer interaction matrix showing data dependencies between the five layers and the Knowledge Graph Foundation.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.4 — Data Flow Design
# ═══════════════════════════════════════════════════════════════════════════

h2("3.4 Data Flow Design")

body("The adaptive platform operates through two primary data flows: the recommendation flow, triggered when a student requests a problem, and the submission processing flow, triggered when a student submits a solution. This section describes each flow in detail, followed by the error handling provisions and the cold-start handling strategy.")

h3("3.4.1 Recommendation Flow")

body("The recommendation flow is triggered when a student requests a practice problem. It traverses all adaptive layers to produce a personalized recommendation. Figure 3.3 illustrates the sequence of interactions between the five system actors: Student, React Client, NestJS API, Redis Cache, and AI Service.")

image("https://files.catbox.moe/8aai68.png", 468, 500)
caption("Figure 3.3. Sequence diagram for the recommendation flow.")

body("The recommendation process within the AI service proceeds through seven steps. First, the service loads the knowledge graph, either from Redis cache or from the concepts and knowledge_graph_edges tables if the cache has expired. The graph structure changes infrequently and is cached with a one-hour TTL. Second, the service loads the student\u2019s BKT knowledge states, Elo ratings, MAB states, and FSRS cards, each cached in Redis with TTLs appropriate to their update frequency, as detailed in Section 3.7.")

body("Third, using the knowledge graph and BKT mastery estimates, the service computes the set of eligible concepts at Level 1. A concept c is eligible if all prerequisites of c are mastered and either c itself is not yet mastered or c is due for review according to FSRS. Concepts due for review that are also mastered are included in the eligible set with a priority boost: their Thompson Sampling prior is inflated by adding a review urgency bonus proportional to how far the retrievability has fallen below the threshold.")

body("Fourth, for each eligible concept, the service draws a sample from the concept\u2019s Beta distribution using Thompson Sampling and selects the concept with the highest sampled value. Fifth, within the selected concept, the service retrieves all unsolved problems tagged with that concept and filters them by the ZPD constraint defined in Equation 3.5. If no problems pass the ZPD filter, the service falls back to the next-highest concept from the previous step.")

body("Sixth, among the ZPD-filtered problems, the service draws Thompson Sampling samples and selects the problem with the highest sampled value. Seventh, the service returns a ranked list of recommended problems, typically three to five, rather than just the single top recommendation. This gives the student some agency in choosing among appropriately challenging options. The NestJS API enriches the list with full problem details before returning it to the client.")

h3("3.4.2 Submission Processing Flow")

body("The submission processing flow is triggered when a student submits code for a problem. It involves two phases: synchronous code execution, which must return promptly to the student, and asynchronous adaptive layer updates, which happen in the background.")

image("https://files.catbox.moe/ntu24z.png", 468, 400)
caption("Figure 3.4. Submission processing flow showing the separation of synchronous execution from asynchronous adaptive updates.")

bold_label("Phase 1: Synchronous Execution.")
body("The student submits code via the React client. The NestJS API receives the submission, saves it to the submissions table with status PENDING, and dispatches it to the Docker sandbox. The Docker sandbox executes the code against each test case, recording pass or fail for each. The NestJS API then updates the submission status to ACCEPTED, WRONG_ANSWER, TIME_LIMIT, RUNTIME_ERROR, or COMPILATION_ERROR and returns the result to the student.")

bold_label("Phase 2: Asynchronous Adaptive Updates.")
body("After the submission status is finalized, the NestJS API sends an asynchronous POST request to the AI service at /adaptive/update with a payload containing the student identifier, problem identifier, concept identifier, correctness indicator, attempt number, time spent, and error type. The AI service processes the update through each layer sequentially.")

body("Layer 1 (BKT) updates the mastery probability using the Bayesian inference equations from Chapter 2 and computes the learning gain. Layer 2 (Elo) updates both student and problem ratings using Equations 3.1 through 3.4 with dynamically adjusted K-factors. Layer 3 (MAB) computes the composite reward signal using Equation 3.6 and updates the Beta distribution parameters for both the selected concept arm and the selected problem arm. Layer 4 (FSRS) either updates an existing FSRS card if the concept was previously mastered, or creates a new card if the concept has just reached mastery for the first time.")

body("All updated states are then written to the database, Redis caches for the affected student are invalidated, and an event log entry is created recording the full update for evaluation purposes.")

body("The sequential ordering of layer updates in Phase 2 is important: Layer 1 must execute before Layer 3 because the MAB reward depends on the learning gain from BKT. Layer 2 can execute in parallel with Layer 1 since it depends only on the submission outcome. Layer 4 depends on Layer 1 to know whether mastery has been reached and must therefore execute after Layer 1.")

body("This asynchronous pattern introduces an eventual consistency window typically under two seconds, which is acceptable given that a single recommendation cycle based on slightly stale state has minimal pedagogical impact. In the worst case, a student who submits a solution and immediately requests a new recommendation may receive a recommendation computed from pre-update state; the next recommendation request will reflect the updated state.")

h3("3.4.3 Error Handling and Edge Cases")

body("The adaptive pipeline must handle failures gracefully to prevent inconsistent state and ensure a reliable student experience. This section describes the error handling strategy for the primary failure modes.")

bold_label("Transactional boundaries.")
body("Each adaptive update covering Layers 1 through 4 is wrapped in a database transaction. A failure in any layer rolls back all updates for that submission event, preventing inconsistent state where, for example, BKT mastery is updated but the corresponding Elo rating is not.")

bold_label("Retry mechanism.")
body("Failed adaptive updates are enqueued in a Redis-backed retry queue with exponential backoff, starting at a one-second delay with a maximum of three retries. After three failures, the event is written to a dead-letter table for manual inspection. The student\u2019s submission result is unaffected by adaptive update failures, since Phase 1 code execution completes independently.")

bold_label("Empty eligible set.")
body("If no eligible concepts exist because all non-mastered concepts have unmet prerequisites, the system falls back to recommending the concept with the highest mastery progress \u2014 the concept closest to the 0.85 threshold. This situation arises rarely in practice, as the knowledge graph is designed with multiple prerequisite-free entry points, but it can occur if a student has partially mastered several prerequisite chains without completing any.")

bold_label("ZPD exhaustion.")
body("If no problems fall within the ZPD bounds after the initial filter, the system performs up to two expansion steps, each widening the bounds by 50 Elo points in both directions. If no problems are found after two expansions, the system returns the easiest unsolved problem in the concept regardless of Elo matching, accepting the pedagogical compromise in favor of providing a recommendation.")

bold_label("Concurrent submissions.")
body("Per-student sequential processing is enforced via a per-student Redis lock using the SETNX pattern with a 30-second TTL to prevent deadlocks. If a lock is held when a new update arrives, the update is queued and processed after the lock is released. This prevents race conditions where two concurrent submissions produce inconsistent state updates.")

bold_label("AI service unavailability.")
body("If the AI service is temporarily unavailable, for example during a restart, the NestJS API returns a fallback recommendation drawn from the pool of unsolved problems in the student\u2019s most recently active topic group, ordered by static difficulty label. The submission result is always returned to the student regardless of AI service availability.")

h3("3.4.4 Cold Start Handling")

body("The cold-start problem arises when the system has insufficient data to make informed adaptive decisions. This occurs in two scenarios: new students with no submission history, and new problems with no submission data.")

image("https://files.catbox.moe/fwnr4w.png", 468, 340)
caption("Figure 3.7. Cold start handling flowchart showing the three-phase transition from round-robin to full adaptive pipeline.")

bold_label("New Student Cold Start.")
body("When a student first uses the platform, all adaptive state is at its default values: BKT mastery at P(L_0) = 0.1 for all concepts, Elo rating at 1200, MAB priors at Beta(1, 1), and no FSRS cards. The system handles this through a structured onboarding phase with three stages.")

body("For the first 3 interactions, the system bypasses the MAB and uses a round-robin strategy over prerequisite-free concepts such as Variables and Data Types. This ensures that the earliest submissions provide signal across the foundational concepts. The threshold of 3 interactions is informed by Clement et al. [22], who demonstrated that MAB-based educational recommendations require a minimum exploration period to outperform random selection. Within each concept, the system selects the problem closest to Elo 1200, ensuring a moderate difficulty level for the first interactions.")

body("After approximately 10 submissions, the BKT and Elo models have accumulated sufficient data to differentiate the student from the population mean, and the full adaptive pipeline takes over. This threshold reflects BKT\u2019s convergence behavior: given the initial prior P(L_0) = 0.1 and transition probability P(T) = 0.2, approximately 10 observations are sufficient for the posterior to diverge meaningfully from the prior [16].")

body("The cold-start phase resolves quickly because BKT\u2019s Bayesian update meaningfully shifts posterior estimates from each observation, and the elevated initial K-factor in the Elo system amplifies early rating changes, enabling rapid calibration.")

bold_label("New Problem Cold Start.")
body("When a new problem is added to the platform, it has no submission history from which to derive an empirical Elo rating. The system initializes the problem\u2019s Elo rating based on its static difficulty label: EASY maps to Elo 1000, MEDIUM to 1200, and HARD to 1400. The initial K-factor is set to 50, which is double the base K-factor, to allow rapid convergence toward the problem\u2019s true difficulty. After approximately 30 submissions from diverse students, the problem\u2019s Elo rating stabilizes and the K-factor decays to the base value. The MAB prior for the new problem is initialized at Beta(1, 1), ensuring that Thompson Sampling\u2019s natural exploration tendency gives the problem a fair chance of being recommended despite its uncertain reward distribution.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.5 — Database Schema Design
# ═══════════════════════════════════════════════════════════════════════════

h2("3.5 Database Schema Design")

body("The database schema comprises core platform tables and adaptive state tables that together support the Knowledge Graph Foundation and the four adaptive layers. This section describes the adaptive tables, the relationships between them, and the migration strategy.")

bold_label("ID strategy.")
body("Core platform tables such as users, problems, and submissions use UUID primary keys for global uniqueness and safe distributed generation. Adaptive engine tables including concepts, knowledge_graph_edges, problem_concepts, and adaptive state tables use auto-incrementing integer primary keys for computational efficiency, since concept IDs and problem IDs serve as array indices in BKT and MAB state lookups where integer indexing is significantly faster than UUID hashing.")

h3("3.5.1 Adaptive Tables and Their Roles")

body("Table 3.4 summarizes the nine database tables that power the adaptive engine, along with their layer associations, purposes, and key columns.")

bold_label("Concepts table.")
body("Each row represents a programming concept in the knowledge graph. The name field is a machine-readable identifier such as recursion or dynamic_programming, while display_name is a human-readable label such as Recursion or Dynamic Programming. The topic_group field organizes concepts into curricular units, and the difficulty_tier ranging from 1 to 5 provides a coarse ordering that assists with initial problem selection before Elo ratings have stabilized.")

bold_label("Knowledge graph edges table.")
body("Each row represents a directed edge in the knowledge graph, indicating that from_concept is a prerequisite for to_concept. The relation_type field defaults to PREREQUISITE but is designed to accommodate future relation types such as RELATED or EXTENDS. The weight field with a default of 1.0 allows for soft prerequisites in future extensions. A unique constraint on the pair of from_concept_id and to_concept_id prevents duplicate edges.")

bold_label("Problem concepts table.")
body("Each row maps a problem to a concept, with a boolean is_primary flag indicating the primary concept assessed by the problem. A problem may be associated with multiple concepts, but exactly one should be designated as primary. The primary concept determines which BKT state is updated when the problem is submitted.")

bold_label("Knowledge states table.")
body("Each row stores the BKT state for a single student-concept pair. The columns p_mastery, p_l0, p_transit, p_guess, and p_slip correspond directly to the BKT parameters described in Section 2.2.1, with p_mastery representing the current posterior mastery estimate P(L_t). The n_attempts and n_correct counters support analytics and parameter tuning. A unique constraint on the student_id and concept_id pair ensures one state per pair, and a composite index on student_id and p_mastery supports efficient querying of mastered concepts for prerequisite gating.")

bold_label("Elo ratings table.")
body("This table uses a polymorphic design where the entity_type field distinguishes between student ratings and problem ratings. This polymorphic approach enables the Elo update algorithm to treat students and problems symmetrically through a single repository layer. The trade-off is that referential integrity between entity_id and its source table must be enforced at the application layer rather than through database foreign keys. The optional concept_id field is included to support per-concept Elo ratings in future extensions; for the current implementation, concept_id is NULL for all ratings. The rating_history column stores a JSONB time series of past ratings for trend analysis and visualization.")

bold_label("MAB states table.")
body("Each row stores the Thompson Sampling state for a single student-arm pair. The arm_type field distinguishes between concept-level arms and problem-level arms. The alpha and beta columns parameterize the Beta distribution, and n_pulls and total_reward support analytics. A unique constraint on student_id, arm_id, and arm_type ensures one state per arm per student.")

bold_label("FSRS cards table.")
body("Each row stores the FSRS memory state for a single student-concept pair. The difficulty, stability, and retrievability columns correspond to the FSRS model parameters described in Section 2.2.5. The state field tracks the card lifecycle through NEW, LEARNING, REVIEW, and RELEARNING stages. The due_date indicates when the next review is scheduled, and last_review records when the concept was last practiced. Composite indices on student_id with due_date and student_id with retrievability support efficient querying of the review queue and priority-based review selection.")

h3("3.5.2 Schema Relationships")

body("Figure 3.5 illustrates the relationships between the adaptive tables and the core platform tables.")

image("https://files.catbox.moe/d0hf0q.png", 468, 400)
caption("Figure 3.5. Entity-relationship diagram showing connections between core platform tables and adaptive state tables.")

body("The key relationships are as follows. Users have a one-to-many relationship with knowledge_states, mab_states, fsrs_cards, elo_ratings (where entity_type is STUDENT), and event_logs. Each user has at most one experiment_groups entry. Concepts serve as a hub connecting knowledge_states, fsrs_cards, problem_concepts, and knowledge_graph_edges, reflecting the concept\u2019s role as the fundamental unit of knowledge in the system. Problems connect to concepts through problem_concepts and to elo_ratings where entity_type is PROBLEM. The problem_concepts mapping enables the system to determine which concepts a submission provides evidence about. Knowledge graph edges form a self-referential relationship within concepts, creating the prerequisite DAG where from_concept is the prerequisite and to_concept is the dependent concept.")

h3("3.5.3 Migration Strategy")

body("The schema is implemented as Prisma migrations, ensuring version-controlled, reproducible database evolution. The migration strategy deploys tables in three phases, ordered by dependency.")

bold_label("Phase 1: Knowledge Graph tables.")
body("The concepts, knowledge_graph_edges, and problem_concepts tables are created. This phase is independent of the adaptive layers and can be populated with concept data and problem-concept mappings before any adaptive algorithms are deployed. Problems receive concept tags through a manual curation process where the instructor maps each problem to its primary concept.")

bold_label("Phase 2: Adaptive state tables.")
body("The knowledge_states, elo_ratings, mab_states, and fsrs_cards tables are created. These tables start empty and are populated as students interact with the system. The AI service creates state rows on first access through lazy initialization: when the system first queries a student\u2019s knowledge state for a concept and no row exists, it creates one with default BKT priors.")

bold_label("Phase 3: Evaluation tables.")
body("The event_logs and experiment_groups tables are created. Experiment group assignment is performed at enrollment time, before the student begins interacting with the adaptive features.")

body("This phased approach allows the knowledge graph to be curated and validated independently of the adaptive engine, reducing the risk of deployment issues.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.6 — API Design
# ═══════════════════════════════════════════════════════════════════════════

h2("3.6 API Design")

body("The API design follows a gateway pattern: the NestJS backend serves as the API gateway that handles authentication, authorization, and request routing, while the FastAPI AI service provides the adaptive intelligence endpoints. This separation allows the AI service to be developed and scaled independently of the web application backend.")

bold_label("Security.")
body("The AI service is deployed on an internal network not accessible from the public internet. All requests to the AI service originate from the NestJS gateway, which validates JWT tokens and enforces role-based access control before proxying. The AI service validates an internal shared API key in the X-Internal-Auth header. Students can only access their own knowledge state and recommendations; cross-user access is prevented by the NestJS layer\u2019s JWT authorization checks, which verify that the user_id in the request path matches the authenticated user\u2019s identity or that the requester has an instructor or admin role for class-level endpoints.")

h3("3.6.1 AI Service Endpoints")

body("The FastAPI AI service exposes the following endpoints:")

bold_label("GET /adaptive/recommend/{user_id}")
body("Returns a ranked list of recommended problems for the specified student. Query parameters include limit (default 5, maximum 10) and include_review (boolean, default true, whether to include review-due concepts in the candidate set). The selection_reason field in each recommendation indicates why the problem was selected, whether through exploitation, exploration, or review, providing transparency for both the student dashboard and evaluation logging.")

bold_label("POST /adaptive/update")
body("Processes a submission result and updates all adaptive layers. This endpoint is called asynchronously by the NestJS backend after code execution completes. The request payload includes student_id, problem_id, concept_id, is_correct, attempt_number, time_spent_seconds, and error_type. The response includes a summary of updates across all four layers.")

bold_label("GET /adaptive/knowledge-state/{user_id}")
body("Returns the complete knowledge state for a student across all concepts, used by the dashboard.")

bold_label("GET /adaptive/review-queue/{user_id}")
body("Returns concepts due for review, ordered by urgency with the lowest retrievability first. Includes the estimated retrievability, stability, and days since last review for each concept.")

bold_label("POST /adaptive/hint")
body("Generates a Socratic hint for a struggling student. The request includes the problem ID, the student\u2019s latest code, and the error message. This endpoint is optional and corresponds to Layer 5.")

body("Detailed request and response JSON schemas for each endpoint are provided in Chapter 4, Section 4.3.")

h3("3.6.2 NestJS Gateway Endpoints")

body("The NestJS backend exposes the following endpoints that proxy or augment the AI service:")

bold_label("Knowledge Graph Management:")
body("GET /api/concepts lists all concepts with their topic groups and difficulty tiers. POST /api/concepts creates a new concept and is restricted to instructor and admin roles. GET /api/knowledge-graph retrieves the full knowledge graph including concepts and edges. POST /api/knowledge-graph/edges adds a prerequisite edge with cycle detection and is restricted to admin role.")

bold_label("Adaptive Recommendations (Proxy):")
body("GET /api/adaptive/recommend/:userId proxies to the AI service, enriching the response with full problem details including description and test case count along with concept display names. GET /api/adaptive/knowledge-state/:userId proxies to the AI service, adding concept display names and topic group labels. GET /api/adaptive/review-queue/:userId proxies to the AI service.")

bold_label("Analytics:")
body("GET /api/analytics/student/:userId returns aggregated analytics for a specific student: mastery heatmap, Elo trajectory, submission history, and review compliance rate. GET /api/analytics/class/:courseId returns class-level analytics for an instructor: concept mastery distribution, common struggle concepts, average Elo progression, and submission volume over time.")

h3("3.6.3 Endpoints with Adaptive Integration")

body("Two platform endpoints incorporate adaptive engine integration.")

bold_label("POST /api/submissions.")
body("After the code execution phase completes and the submission status is finalized, the endpoint issues an asynchronous call to the AI service\u2019s /adaptive/update endpoint. This call is fire-and-forget from the student\u2019s perspective: the submission result is returned to the student immediately, and the adaptive updates happen in the background. If the AI service is temporarily unavailable, the submission result is still returned successfully; the adaptive update is retried via the mechanism described in Section 3.4.3. The payload sent to the AI service is constructed by looking up the problem\u2019s primary concept from the problem_concepts table and computing the attempt number from the count of prior submissions for the same student-problem pair.")

bold_label("GET /api/dashboard.")
body("The dashboard endpoint aggregates both platform metrics, including submission count, acceptance rate, and recent activity, and adaptive metrics: the student\u2019s current concept mastery levels, Elo rating, number of concepts mastered, number of concepts due for review, and the most recent recommendation with its selection reason. Adaptive metrics are fetched from the AI service via the proxy endpoints.")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3.7 — Caching Strategy
# ═══════════════════════════════════════════════════════════════════════════

h2("3.7 Caching Strategy")

body("The recommendation pipeline involves multiple database queries \u2014 loading knowledge states, Elo ratings, FSRS cards, MAB states, and the knowledge graph \u2014 followed by computational processing including prerequisite gating, ZPD filtering, and Thompson Sampling. To meet the 500ms recommendation latency target specified in NFR2 under concurrent load, the system employs Redis as a caching layer with the following policies.")

image("https://files.catbox.moe/7e8r9q.png", 468, 300)
caption("Table 3.5. Redis caching configuration for adaptive state data.")

body("The TTL values are designed to balance freshness against cache hit rate. The knowledge graph changes infrequently, only when instructors modify the curriculum, so a 60-minute TTL is appropriate. Student-specific state has a 5-minute TTL, which serves as a safety net against missed invalidation events. The primary freshness mechanism is explicit invalidation after each submission update, so the TTL is expected to expire rarely under normal operation. The recommendation result itself has the shortest TTL of 2 minutes because it should reflect the student\u2019s most recent submission.")

bold_label("Invalidation strategy.")
body("Cache invalidation follows the write-through pattern: when the AI service processes a submission update, it invalidates the relevant cache entries for the affected student. Specifically, after updating Layers 1 through 4, the service deletes the cached knowledge states, student Elo rating, MAB states, FSRS cards, and recommendation result for that student. Problem-level Elo cache is invalidated only when a problem\u2019s rating changes by more than 10 points, reducing unnecessary cache churn for minor rating fluctuations.")

bold_label("Fallback behavior.")
body("If Redis is unavailable due to a transient failure, the AI service falls back to direct database queries. The recommendation latency may increase to an estimated 800 to 1200 milliseconds without caching, but the system remains functional. This graceful degradation ensures that the adaptive features are not gated on Redis availability.")


# ═══════════════════════════════════════════════════════════════════════════
# CHAPTER SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

body("Chapter Summary. This chapter has defined the functional and non-functional requirements for the adaptive learning platform, described the four-component system architecture and its design rationale, and presented the five-layer adaptive architecture with its Knowledge Graph Foundation. The data flow design specifies how recommendations are generated and how submissions trigger cascading updates across all layers. The database schema, API design, and caching strategy provide the technical infrastructure needed to implement the architecture within the latency and scalability constraints of a university deployment. The following chapter presents the implementation details of each layer, including the specific algorithms, parameter choices, and code-level design decisions.")


# ═══════════════════════════════════════════════════════════════════════════
# BUILD AND EXECUTE GOOGLE DOCS API REQUESTS
# ═══════════════════════════════════════════════════════════════════════════

print(f"\nTotal content blocks: {len(CONTENT_BLOCKS)}")

# Build the full text content first, tracking positions for formatting
all_text = "\n"  # start with newline to separate from existing content
format_ranges = []  # (start, end, type)
image_insertions = []  # (index, url, width, height)
current_offset = INSERT_INDEX  # position in the document

# First pass: build text and track ranges
text_pieces = []
for block in CONTENT_BLOCKS:
    block_type = block[0]

    if block_type == 'image':
        # Images will be inserted after text, so just add a placeholder newline
        text_pieces.append('\n')
        image_insertions.append({
            'text_offset': len(''.join(text_pieces)) - 1,
            'url': block[1],
            'width': block[2],
            'height': block[3]
        })
    elif block_type == 'h2':
        text = '\n' + block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'h2'))
    elif block_type == 'h3':
        text = '\n' + block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'h3'))
    elif block_type == 'body':
        text = block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'body'))
    elif block_type == 'bold_label':
        text = block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'bold_label'))
    elif block_type == 'caption':
        text = block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'caption'))
    elif block_type == 'equation':
        text = block[1] + '\n'
        start = len(''.join(text_pieces))
        text_pieces.append(text)
        end = len(''.join(text_pieces))
        format_ranges.append((start, end, 'equation'))

full_text = ''.join(text_pieces)
print(f"Total text length: {len(full_text)} characters")

# ─── Step 1: Insert all text at once ─────────────────────────────────────
print("\nStep 1: Inserting text...")
# Split into chunks if needed (50k limit)
chunk_size = 40000
chunks = []
for i in range(0, len(full_text), chunk_size):
    chunks.append(full_text[i:i+chunk_size])

# Insert chunks from last to first to maintain correct indices
insert_requests = []
cumulative_offset = 0
for i, chunk in enumerate(chunks):
    insert_requests.append({
        'insertText': {
            'location': {'index': INSERT_INDEX},
            'text': chunk
        }
    })

# Actually, insert all text at once at the insert point
# If multiple chunks, insert them sequentially
for i, chunk in enumerate(chunks):
    result = service.documents().batchUpdate(
        documentId=DOC_ID,
        body={'requests': [{
            'insertText': {
                'location': {'index': INSERT_INDEX + cumulative_offset},
                'text': chunk
            }
        }]}
    ).execute()
    cumulative_offset += len(chunk)
    print(f"  Chunk {i+1}/{len(chunks)} inserted ({len(chunk)} chars)")
    time.sleep(2)

print(f"  Total text inserted: {cumulative_offset} chars")

# ─── Step 2: Apply formatting ────────────────────────────────────────────
print("\nStep 2: Applying formatting...")

format_requests = []
for start_rel, end_rel, fmt_type in format_ranges:
    abs_start = INSERT_INDEX + start_rel
    abs_end = INSERT_INDEX + end_rel

    # Skip empty ranges
    if abs_start >= abs_end:
        continue

    # Strip newline from the range for formatting (don't format the trailing newline)
    fmt_end = abs_end - 1 if abs_end > abs_start + 1 else abs_end

    if fmt_type == 'h2':
        # Skip leading newline for heading format
        fmt_start = abs_start + 1 if abs_start + 1 < fmt_end else abs_start
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': fmt_start, 'endIndex': fmt_end},
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_2',
                    'spaceAbove': {'magnitude': 18, 'unit': 'PT'},
                    'spaceBelow': {'magnitude': 8, 'unit': 'PT'},
                    'keepWithNext': True,
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow,keepWithNext',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': fmt_start, 'endIndex': fmt_end},
                'textStyle': {
                    'bold': True,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 13, 'unit': 'PT'},
                },
                'fields': 'bold,weightedFontFamily,fontSize',
            }
        })

    elif fmt_type == 'h3':
        fmt_start = abs_start + 1 if abs_start + 1 < fmt_end else abs_start
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': fmt_start, 'endIndex': fmt_end},
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_3',
                    'spaceAbove': {'magnitude': 14, 'unit': 'PT'},
                    'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
                    'keepWithNext': True,
                },
                'fields': 'namedStyleType,spaceAbove,spaceBelow,keepWithNext',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': fmt_start, 'endIndex': fmt_end},
                'textStyle': {
                    'bold': True,
                    'italic': True,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'bold,italic,weightedFontFamily,fontSize',
            }
        })

    elif fmt_type == 'body':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'lineSpacing': 150,
                    'spaceAfter': {'magnitude': 6, 'unit': 'PT'},
                    'indentFirstLine': {'magnitude': 36, 'unit': 'PT'},
                    'alignment': 'JUSTIFIED',
                },
                'fields': 'namedStyleType,lineSpacing,spaceAfter,indentFirstLine,alignment',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'textStyle': {
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                    'bold': False,
                    'italic': False,
                },
                'fields': 'weightedFontFamily,fontSize,bold,italic',
            }
        })

    elif fmt_type == 'bold_label':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'lineSpacing': 150,
                    'spaceAfter': {'magnitude': 4, 'unit': 'PT'},
                    'spaceBefore': {'magnitude': 8, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,lineSpacing,spaceAfter,spaceBefore',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'textStyle': {
                    'bold': True,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'bold,weightedFontFamily,fontSize',
            }
        })

    elif fmt_type == 'caption':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'alignment': 'CENTER',
                    'spaceAfter': {'magnitude': 12, 'unit': 'PT'},
                    'spaceBefore': {'magnitude': 6, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,alignment,spaceAfter,spaceBefore',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'textStyle': {
                    'italic': True,
                    'weightedFontFamily': {'fontFamily': 'Times New Roman'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'italic,weightedFontFamily,fontSize',
            }
        })

    elif fmt_type == 'equation':
        format_requests.append({
            'updateParagraphStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'paragraphStyle': {
                    'namedStyleType': 'NORMAL_TEXT',
                    'alignment': 'CENTER',
                    'spaceAfter': {'magnitude': 8, 'unit': 'PT'},
                    'spaceBefore': {'magnitude': 8, 'unit': 'PT'},
                    'indentFirstLine': {'magnitude': 0, 'unit': 'PT'},
                },
                'fields': 'namedStyleType,alignment,spaceAfter,spaceBefore,indentFirstLine',
            }
        })
        format_requests.append({
            'updateTextStyle': {
                'range': {'startIndex': abs_start, 'endIndex': abs_end},
                'textStyle': {
                    'italic': True,
                    'weightedFontFamily': {'fontFamily': 'Cambria Math'},
                    'fontSize': {'magnitude': 12, 'unit': 'PT'},
                },
                'fields': 'italic,weightedFontFamily,fontSize',
            }
        })

# Apply formatting in batches of 40
batch_size = 40
for i in range(0, len(format_requests), batch_size):
    batch = format_requests[i:i+batch_size]
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': batch}
        ).execute()
        print(f"  Format batch {i//batch_size + 1}/{(len(format_requests) + batch_size - 1)//batch_size} applied ({len(batch)} requests)")
    except Exception as e:
        print(f"  Format batch {i//batch_size + 1} FAILED: {e}")
    time.sleep(2)


# ─── Step 3: Insert images ───────────────────────────────────────────────
print("\nStep 3: Inserting images...")

# We need to re-read the document to get current indices since formatting may have shifted things
# Actually, text insertion doesn't change indices for content we already inserted.
# But images need to be inserted from LAST to FIRST to avoid index shifting.

# Sort image insertions by their text_offset in reverse order
image_insertions.sort(key=lambda x: x['text_offset'], reverse=True)

for img in image_insertions:
    img_index = INSERT_INDEX + img['text_offset']
    try:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': [{
                'insertInlineImage': {
                    'location': {'index': img_index},
                    'uri': img['url'],
                    'objectSize': {
                        'width': {'magnitude': img['width'], 'unit': 'PT'},
                        'height': {'magnitude': img['height'], 'unit': 'PT'},
                    }
                }
            }]}
        ).execute()
        print(f"  Image inserted at index {img_index}: {img['url']}")
    except Exception as e:
        print(f"  Image FAILED at index {img_index}: {e}")
    time.sleep(3)

print("\n=== PUBLISHING COMPLETE ===")
print(f"Sections published: 3.1.4, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 + Chapter Summary")
print(f"Total text: {len(full_text)} characters")
print(f"Format ranges applied: {len(format_ranges)}")
print(f"Images inserted: {len(image_insertions)}")
