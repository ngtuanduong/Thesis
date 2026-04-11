# System Architecture — Complete Technical Design

**Thesis:** Adaptive Learning Platform for University Programming Courses

---

## 1. Current System Analysis

### 1.1 Existing Architecture

The current system is a three-tier web application with a supplementary AI microservice:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   React Client   │────▶│   NestJS API     │────▶│   PostgreSQL     │
│   (Vite + TS)    │     │   (Prisma ORM)   │     │   (pgvector)     │
└──────────────────┘     └────────┬─────────┘     └──────────────────┘
                                  │
                         ┌────────▼─────────┐     ┌──────────────────┐
                         │   FastAPI AI     │     │   Docker Sandbox │
                         │   (Python)       │     │   (Code Exec)    │
                         └──────────────────┘     └──────────────────┘
```

**Technology stack:**
| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | React + TypeScript + Ant Design | React 18, Vite |
| Backend API | NestJS + Prisma | NestJS 10, Prisma 6 |
| AI Service | FastAPI + Sentence Transformers | Python 3.11 |
| Database | PostgreSQL + pgvector | PG 16 |
| Code Execution | Docker sandbox | Python only |
| Cache | Redis | 7 (provisioned, unused) |

### 1.2 Current Data Model

```
User (id, email, password, name, role)
  ├── Enrollment (userId, courseId)
  ├── Submission (userId, problemId, code, language, status, output, runtime, memory)
  └── SkillEmbedding (userId, skillName, embedding[384], score)

Course (id, title, description, instructorId)
  └── Problem (id, title, description, difficulty, tags[], courseId?)
        ├── TestCase (id, problemId, input, expected, isHidden)
        ├── Submission (linked above)
        └── ProblemEmbedding (problemId, embedding[384])
```

### 1.3 Current Recommendation Algorithm

The existing algorithm is **content-based filtering** using sentence transformer embeddings:

```python
# Step 1: Compute user profile
for each ACCEPTED submission:
    weight = {EASY: 1.0, MEDIUM: 2.0, HARD: 3.0}[difficulty]
    skill_scores[tag] += weight
normalize(skill_scores)  # divide by max

# Step 2: Embed each skill
for tag, score in skill_scores:
    embedding = sentence_transformer.encode(tag)
    store(userId, tag, embedding, score)

# Step 3: Recommend
user_profile = AVG(all skill embeddings)
recommendations = pgvector_cosine_search(user_profile, problem_embeddings, top_k=N)
filter out already solved problems
```

### 1.4 Critical Weaknesses

| # | Weakness | Impact | Proposed Solution |
|---|----------|--------|-------------------|
| W1 | No knowledge tracing | Cannot estimate what student knows/doesn't know | Layer 1: BKT |
| W2 | Static difficulty labels | EASY/MEDIUM/HARD don't reflect true difficulty for each student | Layer 2: Dynamic Elo |
| W3 | Similarity ≠ Optimality | Recommends similar problems, not the best learning opportunity | Layer 3: Hierarchical MAB |
| W4 | No forgetting model | Assumes skills once learned are permanent | Layer 4: FSRS |
| W5 | No exploration | Always exploits similarity, never explores new concepts | Layer 3: MAB exploration |
| W6 | No prerequisites | May recommend DP before student knows recursion | Foundation: Knowledge Graph |
| W7 | Binary outcomes only | Only uses ACCEPTED/not, ignores attempts, time, errors | Multi-signal input to all layers |
| W8 | No hints/feedback | Student stuck on hard problem has no guidance | Layer 5: LLM + RAG |

---

## 2. Proposed 5-Layer Architecture

### 2.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (React)                           │
│  Dashboard │ Problems │ Recommendations │ Review Queue │ Profile│
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────────────┐
│                     NestJS API Gateway                          │
│  Auth │ Problems │ Submissions │ Recommendations │ Analytics    │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                   ADAPTIVE ENGINE (FastAPI)                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Layer 5: LLM Feedback Engine                              │ │
│  │  KG + RAG + LLM → Socratic hints (optional)               │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Layer 4: Review Scheduler (FSRS)                          │ │
│  │  Tracks (student, concept) memory states → due reviews     │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Layer 3: Problem Selector (Hierarchical MAB)              │ │
│  │  Thompson Sampling: concept selection → problem selection  │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Layer 2: Difficulty Calibrator (Dynamic K-Value Elo)      │ │
│  │  Dual ratings: student Elo + problem Elo → ZPD filtering  │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Layer 1: Knowledge Tracer (BKT)                           │ │
│  │  P(mastery) per concept per student → prerequisite gates   │ │
│  ├────────────────────────────────────────────────────────────┤ │
│  │  Foundation: Knowledge Graph                                │ │
│  │  Concept nodes + prerequisite edges + problem mappings     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  PostgreSQL  │ │    Redis     │ │Docker Sandbox│
    │  (pgvector)  │ │  (caching)  │ │ (code exec)  │
    └──────────────┘ └──────────────┘ └──────────────┘
```

### 2.2 Design Principles

1. **Modularity:** Each layer is an independent module. Any layer can be upgraded (BKT → DKT2) without changing others.
2. **Incremental adoption:** The system works with fewer layers. Layer 5 is optional. Layers can be enabled/disabled.
3. **Data separation:** Each layer maintains its own state tables. No layer directly modifies another's state.
4. **Event-driven updates:** Submission results trigger asynchronous updates to all layers.
5. **Backward compatibility:** New tables are added; existing tables and APIs are not modified (only extended).

### 2.3 Layer Specifications

#### Layer 1: Knowledge Tracer (BKT)

**Responsibility:** Estimate P(mastery) for each (student, concept) pair.

**Input:** Submission event (student_id, concept_id, is_correct)

**Output:** Updated P(mastery) for the concept

**State:** `knowledge_state` table

**Algorithm:** Bayesian Knowledge Tracing (see [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §1)

**Parameters per concept:**
| Parameter | Initial Value | Tuning |
|-----------|--------------|--------|
| P(L₀) | 0.1 | Fit from data per concept |
| P(T) | 0.2 | Fit from data per concept |
| P(G) | 0.15 | Fixed (programming has low guess rate) |
| P(S) | 0.1 | Fixed |

**Mastery threshold:** P(mastery) ≥ 0.85 → concept considered "mastered"

**Interactions with other layers:**
- Feeds Layer 3 (MAB): mastery scores determine which concepts are unlocked
- Feeds Layer 4 (FSRS): mastery regression detected → trigger review

#### Layer 2: Difficulty Calibrator (Dynamic Elo)

**Responsibility:** Maintain accurate difficulty ratings for students and problems.

**Input:** Submission event (student_id, problem_id, is_correct)

**Output:** Updated Elo ratings for both student and problem

**State:** `elo_rating` table

**Algorithm:** Elo with Dynamic K-Value (see [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §2)

**Initial ratings:**
| Entity | Initial Elo | Rationale |
|--------|------------|-----------|
| New student | 1200 | Average starting point |
| EASY problem | 1000 | Below average student |
| MEDIUM problem | 1400 | Above average student |
| HARD problem | 1800 | Expert level |

**Interactions with other layers:**
- Feeds Layer 3 (MAB): ZPD constraint filters problems by Elo range
- Independent from Layer 1 (complementary: BKT = mastery, Elo = ability level)

#### Layer 3: Problem Selector (Hierarchical MAB)

**Responsibility:** Select the optimal problem for a student to attempt next.

**Input:** Student's knowledge state (from L1), Elo rating (from L2), FSRS review queue (from L4), KG

**Output:** A single recommended problem

**State:** `mab_state` table (Beta distribution parameters per arm)

**Algorithm:** Hierarchical Thompson Sampling (see [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §3)

**Decision flow:**
```
1. Check FSRS review queue
   → If any concept has Retrievability < 0.9, prioritize review

2. Get eligible concepts from KG
   → Filter: all prerequisites have P(mastery) ≥ 0.85

3. Level 1 MAB: Select concept
   → Thompson Sampling over eligible concepts

4. Get eligible problems for selected concept
   → Filter: problem Elo in student's ZPD [+100, +300]
   → Filter: not recently attempted (last 24h)

5. Level 2 MAB: Select problem
   → Thompson Sampling over eligible problems

6. Return selected problem
```

#### Layer 4: Review Scheduler (FSRS)

**Responsibility:** Schedule concept reviews to prevent forgetting.

**Input:** Submission events (for rating updates), time (for retrievability decay)

**Output:** Review queue with due dates per concept

**State:** `fsrs_card` table

**Algorithm:** FSRS-5 (see [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §4)

**Rating mapping:**
| Submission Outcome | FSRS Rating | Description |
|--------------------|-------------|-------------|
| ACCEPTED, 1st attempt, < 2min | 4 (Easy) | Effortless recall |
| ACCEPTED, 1st attempt, ≥ 2min | 3 (Good) | Moderate effort |
| ACCEPTED, 2–3 attempts | 2 (Hard) | Significant effort |
| WRONG_ANSWER / gave up | 1 (Again) | Failed recall |

**Interactions with other layers:**
- Feeds Layer 3 (MAB): review queue takes priority over exploration
- Fed by Layer 1 (BKT): mastery regression triggers review scheduling

#### Layer 5: LLM Feedback Engine (Optional)

**Responsibility:** Generate contextual Socratic hints for struggling students.

**Input:** Student's code, error message, knowledge state, relevant KG context

**Output:** A pedagogical hint (not the answer)

**Trigger:** Student has ≥ 3 failed attempts on current problem

**Algorithm:** RAG + LLM (see [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §5)

**This layer is optional and supplementary.**

---

## 3. Data Flow Diagrams

### 3.1 Recommendation Flow

```
Student requests recommendation
         │
         ▼
┌─────────────────────────┐
│  NestJS: GET /recommend │
│  /adaptive/:userId      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  AI Service: /recommend │
│  1. Load knowledge_state│──── P(mastery) per concept
│  2. Load elo_rating     │──── Student Elo
│  3. Load fsrs_cards     │──── Review queue
│  4. Load KG             │──── Prerequisite graph
│  5. Run MAB algorithm   │──── Select concept + problem
│  6. Return problem list │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  NestJS: Enrich response│
│  - Problem details      │
│  - Difficulty estimate   │
│  - Concept context      │
│  - Why recommended       │
└────────────┬────────────┘
             │
             ▼
        Client displays
        recommendation
```

### 3.2 Submission Processing Flow

```
Student submits code
         │
         ▼
┌─────────────────────────┐
│  NestJS: POST /submit   │
│  1. Save submission      │
│     (status: PENDING)    │
│  2. Execute in Docker    │
│     sandbox              │
│  3. Evaluate results     │
│  4. Update submission    │
│     (status: ACCEPTED/   │
│      WRONG_ANSWER/...)   │
└────────────┬────────────┘
             │
             ▼ (async, after status determined)
┌─────────────────────────────────────────────┐
│  AI Service: POST /update-layers            │
│                                              │
│  Input: {student_id, problem_id, concept_id, │
│          is_correct, attempt_number,          │
│          time_spent, error_type}              │
│                                              │
│  ┌─────────────────────────────────────────┐│
│  │  1. Update BKT (Layer 1)                ││
│  │     P(mastery) for concept              ││
│  ├─────────────────────────────────────────┤│
│  │  2. Update Elo (Layer 2)                ││
│  │     Student Elo + Problem Elo           ││
│  ├─────────────────────────────────────────┤│
│  │  3. Update MAB (Layer 3)                ││
│  │     Reward for (concept, problem) arm   ││
│  ├─────────────────────────────────────────┤│
│  │  4. Update FSRS (Layer 4)               ││
│  │     Rate review + schedule next review  ││
│  └─────────────────────────────────────────┘│
│                                              │
│  Return: updated states for dashboard        │
└─────────────────────────────────────────────┘
```

### 3.3 Cold Start Handling

Cold start is a **critical UX issue** that significantly affects first impressions. With only 5 seed problems in the current system, the cold start experience is particularly important to design well.

#### 3.3.1 New Student Cold Start

```
New Student (no submissions):
  ├── BKT: All concepts P(L₀) = 0.1 (low initial mastery)
  ├── Elo: Rating = 1200 (average)
  ├── MAB: All arms Beta(1, 1) (uniform prior = maximum exploration)
  ├── FSRS: No cards yet (created on first encounter)
  └── Recommendation: Prerequisite-free concepts, EASY problems
      (e.g., variables, basic I/O, simple arithmetic)
```

**Cold start resolution strategy:**
1. **First 3 interactions:** Recommend from prerequisite-free concepts only (Level 1: variables, data_types, operators, io, strings). Use round-robin across these concepts to gather initial signal for each.
2. **Interactions 4–10:** BKT has enough signal to differentiate mastery across basic concepts. Elo begins converging (high K = 40 for fast initial calibration). MAB starts exploiting concepts with higher learning gain.
3. **After 10 interactions:** Cold start effectively resolved. BKT mastery estimates are informative, Elo has narrowed to ±100 range, MAB has meaningful Beta parameters.

**Adaptive onboarding quiz (optional enhancement):** Present 5 diagnostic questions covering different difficulty tiers before the first recommendation. This immediately provides BKT and Elo signals, reducing cold start to near-zero interactions.

#### 3.3.2 New Problem Cold Start

```
New Problem (no submissions against it):
  ├── Elo: Mapped from difficulty tag (EASY=1000, MEDIUM=1400, HARD=1800)
  ├── MAB: Beta(1, 1) for all students (will be explored)
  └── Calibration: Elo updates rapidly (high K) for first ~30 submissions
```

**Problem Elo convergence:** With K_problem = 40/√(n_attempts), the problem's Elo converges within ~30 submissions. For the first 10 submissions, the problem is essentially in "calibration mode" — its Elo may swing widely but stabilizes quickly.

#### 3.3.3 Problem Content Gap — Expansion Plan

**Current state:** 5 seed problems (Two Sum, Palindrome, etc.) — far too few for meaningful adaptive recommendation or evaluation.

**Minimum viable problem set for evaluation:** 30–50 problems covering ~30 concepts (at least 1 problem per concept, ideally 2–3 per concept for ZPD variation).

**Problem creation strategy (added to Phase 0):**
1. Source 15–20 problems from university course assignments and exams (with instructor permission)
2. Create 10–15 original problems targeting gaps in concept coverage
3. Adapt 5–10 problems from open competitive programming archives (e.g., Codeforces Div 2 A/B problems, simplified for course level)
4. Each problem must have: title, description, 5+ test cases (2 visible, 3+ hidden), concept tags (1 primary + 0–2 secondary), difficulty tag
5. Validate by having 2–3 students pilot-test before deployment

**Target timeline:** Problem set expansion completed by end of Phase 0 (Week 1), before any adaptive layer development begins.

---

## 4. Database Schema Design

### 4.1 New Tables

#### `concept` — Knowledge Graph Nodes

```sql
CREATE TABLE concept (
  id          SERIAL PRIMARY KEY,
  name        VARCHAR(100) UNIQUE NOT NULL,   -- e.g., "arrays", "recursion", "dp"
  display_name VARCHAR(200) NOT NULL,          -- e.g., "Arrays and Lists"
  description TEXT,
  topic_group VARCHAR(100),                    -- e.g., "data_structures", "algorithms"
  difficulty_tier INTEGER DEFAULT 1,           -- 1=basic, 2=intermediate, 3=advanced
  created_at  TIMESTAMP DEFAULT NOW(),
  updated_at  TIMESTAMP DEFAULT NOW()
);
```

#### `knowledge_graph_edge` — Prerequisite Relationships

```sql
CREATE TABLE knowledge_graph_edge (
  id              SERIAL PRIMARY KEY,
  from_concept_id INTEGER REFERENCES concept(id) ON DELETE CASCADE,
  to_concept_id   INTEGER REFERENCES concept(id) ON DELETE CASCADE,
  relation_type   VARCHAR(20) DEFAULT 'PREREQUISITE',  -- PREREQUISITE | RELATED
  weight          FLOAT DEFAULT 1.0,                    -- strength of relationship
  UNIQUE(from_concept_id, to_concept_id)
);
-- from_concept_id is prerequisite OF to_concept_id
-- e.g., "loops" → "sorting" means loops is a prerequisite for sorting
```

#### `problem_concept` — Problem-to-Concept Mapping

```sql
CREATE TABLE problem_concept (
  id          SERIAL PRIMARY KEY,
  problem_id  INTEGER REFERENCES problem(id) ON DELETE CASCADE,
  concept_id  INTEGER REFERENCES concept(id) ON DELETE CASCADE,
  is_primary  BOOLEAN DEFAULT FALSE,  -- primary concept for this problem
  UNIQUE(problem_id, concept_id)
);
```

#### `knowledge_state` — BKT State (Layer 1)

```sql
CREATE TABLE knowledge_state (
  id          SERIAL PRIMARY KEY,
  student_id  INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
  concept_id  INTEGER REFERENCES concept(id) ON DELETE CASCADE,
  p_mastery   FLOAT NOT NULL DEFAULT 0.1,    -- P(L_t), current mastery probability
  p_l0        FLOAT NOT NULL DEFAULT 0.1,    -- P(L₀), prior knowledge
  p_transit   FLOAT NOT NULL DEFAULT 0.2,    -- P(T), learning rate
  p_guess     FLOAT NOT NULL DEFAULT 0.15,   -- P(G), guess rate
  p_slip      FLOAT NOT NULL DEFAULT 0.1,    -- P(S), slip rate
  n_attempts  INTEGER DEFAULT 0,
  n_correct   INTEGER DEFAULT 0,
  updated_at  TIMESTAMP DEFAULT NOW(),
  UNIQUE(student_id, concept_id)
);

CREATE INDEX idx_ks_student ON knowledge_state(student_id);
CREATE INDEX idx_ks_mastery ON knowledge_state(student_id, p_mastery);
```

#### `elo_rating` — Elo Ratings (Layer 2)

```sql
CREATE TABLE elo_rating (
  id            SERIAL PRIMARY KEY,
  entity_id     INTEGER NOT NULL,
  entity_type   VARCHAR(10) NOT NULL,  -- 'STUDENT' | 'PROBLEM'
  concept_id    INTEGER REFERENCES concept(id),  -- NULL for global Elo, set for per-concept Elo
  rating        FLOAT NOT NULL DEFAULT 1200.0,
  k_value       FLOAT NOT NULL DEFAULT 25.0,
  trend         FLOAT NOT NULL DEFAULT 0.0,      -- recent performance trend
  n_attempts    INTEGER DEFAULT 0,
  rating_history JSONB DEFAULT '[]',              -- [{timestamp, rating, opponent_rating, outcome}]
  updated_at    TIMESTAMP DEFAULT NOW(),
  UNIQUE(entity_id, entity_type, concept_id)
);

CREATE INDEX idx_elo_entity ON elo_rating(entity_id, entity_type);
CREATE INDEX idx_elo_rating ON elo_rating(rating) WHERE entity_type = 'PROBLEM';
```

#### `mab_state` — Multi-Armed Bandit State (Layer 3)

```sql
CREATE TABLE mab_state (
  id          SERIAL PRIMARY KEY,
  student_id  INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
  arm_id      INTEGER NOT NULL,       -- concept_id (L1) or problem_id (L2)
  arm_type    VARCHAR(10) NOT NULL,   -- 'CONCEPT' | 'PROBLEM'
  alpha       FLOAT NOT NULL DEFAULT 1.0,   -- Beta distribution: successes + 1
  beta        FLOAT NOT NULL DEFAULT 1.0,   -- Beta distribution: failures + 1
  n_pulls     INTEGER DEFAULT 0,
  total_reward FLOAT DEFAULT 0.0,
  updated_at  TIMESTAMP DEFAULT NOW(),
  UNIQUE(student_id, arm_id, arm_type)
);

CREATE INDEX idx_mab_student ON mab_state(student_id, arm_type);
```

#### `fsrs_card` — Spaced Repetition Cards (Layer 4)

```sql
CREATE TABLE fsrs_card (
  id              SERIAL PRIMARY KEY,
  student_id      INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
  concept_id      INTEGER REFERENCES concept(id) ON DELETE CASCADE,
  difficulty      FLOAT NOT NULL DEFAULT 5.0,    -- D: 1-10 scale
  stability       FLOAT NOT NULL DEFAULT 1.0,    -- S: days until R=0.9
  retrievability  FLOAT NOT NULL DEFAULT 1.0,    -- R: current recall probability
  state           VARCHAR(15) DEFAULT 'NEW',     -- NEW | LEARNING | REVIEW | RELEARNING
  due_date        TIMESTAMP NOT NULL DEFAULT NOW(),
  last_review     TIMESTAMP,
  reps            INTEGER DEFAULT 0,
  lapses          INTEGER DEFAULT 0,             -- number of times forgotten (rating=1)
  updated_at      TIMESTAMP DEFAULT NOW(),
  UNIQUE(student_id, concept_id)
);

CREATE INDEX idx_fsrs_due ON fsrs_card(student_id, due_date);
CREATE INDEX idx_fsrs_retrievability ON fsrs_card(student_id, retrievability);
```

### 4.2 Schema Relationships (Complete)

```
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
         ┌─────────────────┼──────────────────────┐
         │                 │                       │
         ▼                 ▼                       ▼
  ┌──────────────┐  ┌──────────────┐    ┌──────────────────┐
  │ knowledge_   │  │  elo_rating  │    │    mab_state     │
  │ state        │  │ (STUDENT)    │    │                  │
  └──────┬───────┘  └──────────────┘    └──────────────────┘
         │                                        │
         ▼                                        ▼
  ┌──────────────┐                       ┌──────────────┐
  │   concept    │◀──────────────────────│ fsrs_card    │
  └──────┬───────┘                       └──────────────┘
         │
    ┌────┼────┐
    ▼         ▼
┌────────┐ ┌──────────────────┐
│  KG    │ │ problem_concept  │
│ edges  │ │                  │
└────────┘ └───────┬──────────┘
                   ▼
            ┌──────────────┐
            │   Problem    │
            └──────┬───────┘
                   │
                   ▼
            ┌──────────────┐
            │  elo_rating  │
            │ (PROBLEM)    │
            └──────────────┘
```

### 4.3 Prisma Schema Additions

```prisma
model Concept {
  id            Int       @id @default(autoincrement())
  name          String    @unique @db.VarChar(100)
  displayName   String    @map("display_name") @db.VarChar(200)
  description   String?   @db.Text
  topicGroup    String?   @map("topic_group") @db.VarChar(100)
  difficultyTier Int      @default(1) @map("difficulty_tier")
  createdAt     DateTime  @default(now()) @map("created_at")
  updatedAt     DateTime  @updatedAt @map("updated_at")

  // Relations
  knowledgeStates   KnowledgeState[]
  problemConcepts   ProblemConcept[]
  fsrsCards         FsrsCard[]
  prerequisiteFor   KnowledgeGraphEdge[] @relation("prerequisiteFor")
  hasPrerequisites  KnowledgeGraphEdge[] @relation("hasPrerequisites")

  @@map("concept")
}

model KnowledgeGraphEdge {
  id             Int     @id @default(autoincrement())
  fromConceptId  Int     @map("from_concept_id")
  toConceptId    Int     @map("to_concept_id")
  relationType   String  @default("PREREQUISITE") @map("relation_type") @db.VarChar(20)
  weight         Float   @default(1.0)

  fromConcept    Concept @relation("prerequisiteFor", fields: [fromConceptId], references: [id], onDelete: Cascade)
  toConcept      Concept @relation("hasPrerequisites", fields: [toConceptId], references: [id], onDelete: Cascade)

  @@unique([fromConceptId, toConceptId])
  @@map("knowledge_graph_edge")
}

model ProblemConcept {
  id         Int     @id @default(autoincrement())
  problemId  Int     @map("problem_id")
  conceptId  Int     @map("concept_id")
  isPrimary  Boolean @default(false) @map("is_primary")

  problem    Problem @relation(fields: [problemId], references: [id], onDelete: Cascade)
  concept    Concept @relation(fields: [conceptId], references: [id], onDelete: Cascade)

  @@unique([problemId, conceptId])
  @@map("problem_concept")
}

model KnowledgeState {
  id         Int      @id @default(autoincrement())
  studentId  Int      @map("student_id")
  conceptId  Int      @map("concept_id")
  pMastery   Float    @default(0.1) @map("p_mastery")
  pL0        Float    @default(0.1) @map("p_l0")
  pTransit   Float    @default(0.2) @map("p_transit")
  pGuess     Float    @default(0.15) @map("p_guess")
  pSlip      Float    @default(0.1) @map("p_slip")
  nAttempts  Int      @default(0) @map("n_attempts")
  nCorrect   Int      @default(0) @map("n_correct")
  updatedAt  DateTime @updatedAt @map("updated_at")

  student    User    @relation(fields: [studentId], references: [id], onDelete: Cascade)
  concept    Concept @relation(fields: [conceptId], references: [id], onDelete: Cascade)

  @@unique([studentId, conceptId])
  @@map("knowledge_state")
}

model EloRating {
  id            Int      @id @default(autoincrement())
  entityId      Int      @map("entity_id")
  entityType    String   @map("entity_type") @db.VarChar(10)
  conceptId     Int?     @map("concept_id")
  rating        Float    @default(1200.0)
  kValue        Float    @default(25.0) @map("k_value")
  trend         Float    @default(0.0)
  nAttempts     Int      @default(0) @map("n_attempts")
  ratingHistory Json     @default("[]") @map("rating_history")
  updatedAt     DateTime @updatedAt @map("updated_at")

  @@unique([entityId, entityType, conceptId])
  @@map("elo_rating")
}

model MabState {
  id          Int      @id @default(autoincrement())
  studentId   Int      @map("student_id")
  armId       Int      @map("arm_id")
  armType     String   @map("arm_type") @db.VarChar(10)
  alpha       Float    @default(1.0)
  beta        Float    @default(1.0)
  nPulls      Int      @default(0) @map("n_pulls")
  totalReward Float    @default(0.0) @map("total_reward")
  updatedAt   DateTime @updatedAt @map("updated_at")

  student     User     @relation(fields: [studentId], references: [id], onDelete: Cascade)

  @@unique([studentId, armId, armType])
  @@map("mab_state")
}

model FsrsCard {
  id              Int      @id @default(autoincrement())
  studentId       Int      @map("student_id")
  conceptId       Int      @map("concept_id")
  difficulty      Float    @default(5.0)
  stability       Float    @default(1.0)
  retrievability  Float    @default(1.0)
  state           String   @default("NEW") @db.VarChar(15)
  dueDate         DateTime @default(now()) @map("due_date")
  lastReview      DateTime? @map("last_review")
  reps            Int      @default(0)
  lapses          Int      @default(0)
  updatedAt       DateTime @updatedAt @map("updated_at")

  student         User    @relation(fields: [studentId], references: [id], onDelete: Cascade)
  concept         Concept @relation(fields: [conceptId], references: [id], onDelete: Cascade)

  @@unique([studentId, conceptId])
  @@map("fsrs_card")
}
```

---

## 5. API Design

### 5.1 New AI Service Endpoints

#### GET `/adaptive/recommend/{user_id}`
Full adaptive recommendation using all 5 layers.

**Query params:** `limit` (default 5), `include_review` (default true)

**Response:**
```json
{
  "recommendations": [
    {
      "problem_id": 42,
      "concept": "sorting",
      "reason": "REVIEW",           // REVIEW | NEW_CONCEPT | PRACTICE
      "difficulty_match": 0.85,      // how well Elo matches ZPD (0-1)
      "expected_success": 0.65,      // Elo-based prediction
      "mastery_before": 0.72,        // current BKT mastery of concept
      "retrievability": 0.82         // FSRS retrievability (if review)
    }
  ],
  "knowledge_summary": {
    "mastered_concepts": 8,
    "in_progress_concepts": 3,
    "locked_concepts": 5,
    "student_elo": 1350,
    "due_reviews": 2
  }
}
```

#### POST `/adaptive/update`
Update all layers after a submission.

**Request:**
```json
{
  "student_id": 1,
  "problem_id": 42,
  "concept_id": 7,
  "is_correct": true,
  "attempt_number": 2,
  "time_spent_seconds": 180,
  "error_type": null
}
```

**Response:**
```json
{
  "bkt_update": {
    "concept": "sorting",
    "p_mastery_before": 0.72,
    "p_mastery_after": 0.81
  },
  "elo_update": {
    "student_elo_before": 1340,
    "student_elo_after": 1355,
    "problem_elo_before": 1420,
    "problem_elo_after": 1412
  },
  "mab_update": {
    "concept_reward": 0.09,
    "problem_reward": 0.09
  },
  "fsrs_update": {
    "rating": 2,
    "next_review": "2026-03-05T00:00:00Z",
    "stability": 3.5
  }
}
```

#### GET `/adaptive/knowledge-state/{user_id}`
Complete knowledge state visualization data.

**Response:**
```json
{
  "concepts": [
    {
      "id": 1,
      "name": "variables",
      "display_name": "Variables and Assignment",
      "p_mastery": 0.95,
      "elo": 1450,
      "status": "MASTERED",           // MASTERED | IN_PROGRESS | LOCKED | NOT_STARTED
      "fsrs_state": "REVIEW",
      "next_review": "2026-03-01",
      "prerequisites_met": true,
      "problems_attempted": 5,
      "problems_solved": 4
    }
  ],
  "knowledge_graph": {
    "nodes": [...],
    "edges": [...]
  }
}
```

#### GET `/adaptive/review-queue/{user_id}`
FSRS review queue — concepts due for review.

**Response:**
```json
{
  "due_now": [
    {
      "concept_id": 3,
      "concept_name": "loops",
      "retrievability": 0.78,
      "days_overdue": 2,
      "suggested_problem_id": 15
    }
  ],
  "upcoming": [
    {
      "concept_id": 5,
      "concept_name": "functions",
      "due_date": "2026-03-03",
      "retrievability": 0.88
    }
  ]
}
```

#### POST `/adaptive/hint`
Generate LLM-powered Socratic hint (Layer 5, optional).

**Request:**
```json
{
  "student_id": 1,
  "problem_id": 42,
  "student_code": "def solution(nums):\n    ...",
  "error_message": "Wrong Answer on test case 3",
  "attempt_number": 3
}
```

**Response:**
```json
{
  "hint": "I see you're iterating through the array once. What would happen if you needed to compare elements that aren't adjacent? Think about what data structure could help you check if a complement exists...",
  "hint_type": "SOCRATIC_QUESTION",
  "related_concept": "hash_maps",
  "concept_mastery": 0.35
}
```

### 5.2 New NestJS Endpoints

```
GET    /api/adaptive/recommend/:userId      → proxy to AI service
GET    /api/adaptive/knowledge-state/:userId → proxy to AI service
GET    /api/adaptive/review-queue/:userId    → proxy to AI service
POST   /api/adaptive/hint                    → proxy to AI service

GET    /api/concepts                         → list all concepts
GET    /api/concepts/:id                     → concept details with KG
POST   /api/concepts                         → create concept (instructor)
PUT    /api/concepts/:id                     → update concept (instructor)

GET    /api/knowledge-graph                  → full KG (nodes + edges)
POST   /api/knowledge-graph/edges            → add prerequisite (instructor)
DELETE /api/knowledge-graph/edges/:id        → remove prerequisite (instructor)

GET    /api/analytics/student/:userId        → student analytics (Elo history, mastery progress)
GET    /api/analytics/class/:courseId         → class-level analytics (instructor)
GET    /api/analytics/problem/:problemId     → problem analytics (submission stats, Elo convergence)
```

### 5.3 Modifications to Existing Endpoints

**POST `/api/submissions`** — Add post-submission hook:
```typescript
// After code execution completes:
if (result.status === 'ACCEPTED' || result.status === 'WRONG_ANSWER') {
  await this.aiService.updateAdaptiveLayers({
    studentId: submission.userId,
    problemId: submission.problemId,
    isCorrect: result.status === 'ACCEPTED',
    attemptNumber: await this.getAttemptCount(submission.userId, submission.problemId),
    timeSpent: computeTimeSpent(submission),
    errorType: result.errorType ?? null,
  });
}
```

**GET `/api/dashboard`** — Add adaptive metrics:
```json
{
  "existing_stats": { ... },
  "adaptive": {
    "student_elo": 1350,
    "elo_trend": "IMPROVING",
    "concepts_mastered": 8,
    "concepts_total": 16,
    "due_reviews": 2,
    "recommended_next": { ... }
  }
}
```

---

## 6. Technology Decisions

### 6.1 Where to Implement Each Layer

| Layer | Service | Rationale |
|-------|---------|-----------|
| BKT (Layer 1) | AI Service (Python) | pyBKT library, NumPy/SciPy for parameter fitting |
| Elo (Layer 2) | AI Service (Python) | Simple math, collocate with BKT for efficiency |
| MAB (Layer 3) | AI Service (Python) | NumPy for Beta sampling, needs BKT + Elo data |
| FSRS (Layer 4) | AI Service (Python) | FSRS Python library (py-fsrs) available |
| LLM (Layer 5) | AI Service (Python) | LangChain/RAG tools in Python ecosystem |
| KG Management | NestJS + Prisma | CRUD operations, instructor-facing |
| KG Queries | AI Service reads from same DB | Needs KG for MAB constraints |

### 6.2 Communication Pattern

```
Client ──REST──▶ NestJS ──REST──▶ AI Service ──SQL──▶ PostgreSQL
                    │                                       ▲
                    └──────────Prisma ORM───────────────────┘
```

Both NestJS (via Prisma) and AI Service (via SQLAlchemy) access the same PostgreSQL database. This avoids API calls between services for data reads and keeps latency low.

**Write Responsibility Convention (Critical):**

To prevent race conditions and schema drift from dual-writer access, strict write ownership is enforced:

| Table(s) | Write Owner | Read By | Rationale |
|-----------|------------|---------|-----------|
| `user`, `problem`, `test_case`, `submission`, `enrollment`, `course` | **NestJS (Prisma)** | Both | Core domain entities managed by API |
| `concept`, `knowledge_graph_edge`, `problem_concept` | **NestJS (Prisma)** | Both | KG management is an instructor-facing CRUD operation |
| `knowledge_state`, `elo_rating`, `mab_state`, `fsrs_card` | **AI Service (SQLAlchemy)** | Both | Adaptive state is computed by AI algorithms |

**Rules:**
1. NestJS **never** writes to adaptive tables (`knowledge_state`, `elo_rating`, `mab_state`, `fsrs_card`)
2. AI Service **never** writes to core domain tables (`user`, `problem`, `submission`)
3. Both services may **read** from any table
4. Schema migrations are always managed by Prisma; SQLAlchemy models must stay aligned manually (verified in Phase 0, task 0.16)
5. If a future requirement needs cross-service writes (e.g., AI service creating a concept), route through NestJS API instead of direct DB write

### 6.3 Caching Strategy (Redis)

Redis is already provisioned but unused. Introduce caching for:

| Data | TTL | Rationale |
|------|-----|-----------|
| Knowledge state per student | 5 min | Frequently read for recommendations |
| Knowledge graph structure | 1 hour | Rarely changes |
| Problem Elo ratings | 10 min | Updates only on submissions |
| Recommendation results | 2 min | Avoid recomputing for rapid page loads |

**Invalidation strategy:**

| Event | Keys Invalidated | Reason |
|-------|-----------------|--------|
| Student submits code | `knowledge_state:{student_id}`, `recommendations:{student_id}` | Mastery and recommendations changed |
| Problem Elo update (from any submission) | `problem_elo:{problem_id}` | Problem difficulty changed |
| Instructor adds/removes KG edge | `knowledge_graph` (global), `recommendations:*` (all students) | Prerequisite structure changed |
| Instructor adds/modifies problem | `recommendations:*` (all students) | New problem available for recommendation |

**Implementation:**
```python
# Redis invalidation in AI service after submission processing
async def invalidate_after_submission(student_id: int, problem_id: int):
    await redis.delete(f"knowledge_state:{student_id}")
    await redis.delete(f"recommendations:{student_id}")
    await redis.delete(f"problem_elo:{problem_id}")

# Redis invalidation in NestJS after KG modification
async invalidateKnowledgeGraph(): Promise<void> {
    await this.redis.del("knowledge_graph");
    // Use pattern-based deletion for all student recommendations
    const keys = await this.redis.keys("recommendations:*");
    if (keys.length > 0) await this.redis.del(...keys);
}
```

**Stale cache risk mitigation:**
- Recommendation cache TTL is 2 minutes — even without explicit invalidation, stale recommendations are short-lived
- Knowledge state cache is invalidated on every submission — the most critical path
- KG cache (1 hour TTL) is only stale if an instructor modifies the KG while students are using the system — rare and low-impact
