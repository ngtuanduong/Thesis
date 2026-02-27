# Implementation Plan — Step-by-Step Roadmap

**Thesis:** Adaptive Learning Platform for University Programming Courses

---

## Implementation Phases Overview

```
Phase 0: Foundation ──────── Knowledge Graph + DB schema + concept mapping
Phase 1: Layer 1 ─────────── BKT Knowledge Tracing
Phase 2: Layer 2 ─────────── Dynamic K-Value Elo
Phase 3: Layer 3 ─────────── Hierarchical MAB
Phase 4: Layer 4 ─────────── FSRS Spaced Repetition
Phase 5: Integration ─────── Pipeline orchestration + submission hooks
Phase 6: Frontend ─────────── Dashboard, recommendations UI, review queue
Phase 7: Layer 5 (Optional)── LLM Feedback Engine
Phase 8: Evaluation ──────── Experiment setup, data collection, analysis
```

**Dependencies:**
```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3 ──► Phase 5 ──► Phase 6 ──► Phase 8
                                        ▲
             Phase 4 ───────────────────┘
                                                   Phase 7 (independent, optional)
```

---

## Phase 0: Foundation — Knowledge Graph & Schema (Week 1)

### Objectives
- Define the concept taxonomy for Python programming course
- Create database schema for all adaptive layers
- Map existing problems to concepts
- Set up the prerequisite graph

### Files to Create

| File | Purpose |
|------|---------|
| `server/prisma/schema.prisma` | ADD: Concept, KnowledgeGraphEdge, ProblemConcept, KnowledgeState, EloRating, MabState, FsrsCard models |
| `server/prisma/migrations/xxx_adaptive_layers/` | Migration for new tables |
| `server/prisma/seed-concepts.ts` | Seed script: concepts + prerequisites + problem-concept mappings |
| `server/src/concepts/concepts.module.ts` | NestJS module for concept CRUD |
| `server/src/concepts/concepts.controller.ts` | REST endpoints for concepts + KG management |
| `server/src/concepts/concepts.service.ts` | Business logic for concepts |
| `ai-service/models/concept.py` | SQLAlchemy model for concept table |
| `ai-service/models/knowledge_state.py` | SQLAlchemy model for BKT state |
| `ai-service/models/elo_rating.py` | SQLAlchemy model for Elo |
| `ai-service/models/mab_state.py` | SQLAlchemy model for MAB |
| `ai-service/models/fsrs_card.py` | SQLAlchemy model for FSRS |

### Files to Modify

| File | Change |
|------|--------|
| `server/prisma/schema.prisma` | Add 7 new models (see 03-SYSTEM-ARCHITECTURE.md §4) |
| `ai-service/models/__init__.py` | Export new models |
| `docker/docker-compose.yml` | No changes needed (same DB) |

### Tasks

- [ ] Design concept taxonomy (30 concepts for Python course)
- [ ] Define prerequisite edges (40–50 edges)
- [ ] Map each existing problem to 1–3 concepts (primary + secondary)
- [ ] Write Prisma schema additions
- [ ] Run migration
- [ ] Write and run seed script
- [ ] Create concept CRUD module in NestJS
- [ ] Add SQLAlchemy models in AI service
- [ ] Verify: all tables created, seed data loaded, models aligned

### Technology Choices
- **Prisma** for NestJS-side schema management and migrations
- **SQLAlchemy** for AI service reads (same DB, no inter-service API needed for data access)
- Concept taxonomy: manually curated based on university Python curriculum

### Risks
| Risk | Mitigation |
|------|------------|
| Concept taxonomy too coarse/fine | Start with ~30 concepts; can split/merge later |
| Problem-concept mapping ambiguity | Use "primary concept" designation; secondary concepts are optional |

---

## Phase 1: Layer 1 — BKT Knowledge Tracing (Week 2)

### Objectives
- Implement BKT update algorithm
- Initialize knowledge state for all (student, concept) pairs
- Create API endpoint for knowledge state queries
- Test BKT predictions against historical submission data

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/bkt_service.py` | Core BKT implementation: update, predict, initialize |
| `ai-service/routers/knowledge_tracing.py` | FastAPI endpoints for KT |
| `ai-service/tests/test_bkt.py` | Unit tests for BKT math |

### Files to Modify

| File | Change |
|------|--------|
| `ai-service/main.py` | Register new router |
| `ai-service/requirements.txt` | Add pyBKT (optional, for parameter fitting) |

### Algorithm Implementation
See [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §1 for complete pseudocode.

### Key decisions
- Start with **custom BKT implementation** (not pyBKT) for full control
- Use pyBKT only for offline parameter fitting when data accumulates
- Default parameters by concept difficulty tier (basic/intermediate/advanced)
- Multi-concept update: primary concept gets full update, secondary concepts get attenuated update

### API Endpoints
```
POST /kt/update          — Update BKT after submission
GET  /kt/state/{user_id} — Get all knowledge states for user
GET  /kt/predict/{user_id}/{problem_id} — Predict P(correct) for a problem
```

### Test Criteria
- [ ] BKT update produces valid probabilities (0 ≤ P(mastery) ≤ 1)
- [ ] Correct responses increase mastery, incorrect responses may decrease it
- [ ] Mastery converges to ~1.0 after many consecutive correct responses
- [ ] Mastery converges to ~P(G) after many consecutive incorrect responses
- [ ] Multi-concept update correctly weights primary vs secondary

### Risks
| Risk | Mitigation |
|------|------------|
| BKT parameters poorly calibrated | Use conservative defaults; refit after data collection |
| Single-concept assumption too simplistic | Multi-concept extension handles this |

---

## Phase 2: Layer 2 — Dynamic K-Value Elo (Week 2–3)

### Objectives
- Implement dual Elo system (student + problem ratings)
- Implement dynamic K-value based on learning trend
- Initialize problem Elo from difficulty tags
- Create ZPD filtering function
- Create API endpoints for Elo queries

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/elo_service.py` | Elo update, dynamic K, ZPD filtering |
| `ai-service/routers/elo.py` | FastAPI endpoints for Elo |
| `ai-service/tests/test_elo.py` | Unit tests for Elo calculations |

### Files to Modify

| File | Change |
|------|--------|
| `ai-service/main.py` | Register new router |

### Key Decisions
- **Global Elo** for students initially (one rating per student)
- Per-concept Elo as future enhancement (multidimensional)
- Problem Elo initialized from difficulty tag: EASY=1000, MEDIUM=1400, HARD=1800
- Student Elo initialized at 1200
- K-factor range: K_min=10, K_max=40
- Trend window: 10 most recent submissions

### API Endpoints
```
POST /elo/update          — Update Elo after submission
GET  /elo/student/{id}    — Get student Elo + history
GET  /elo/problem/{id}    — Get problem Elo + stats
GET  /elo/zpd/{user_id}   — Get problems in ZPD
```

### Test Criteria
- [ ] Student rating increases on unexpected correct (low expected → correct)
- [ ] Student rating decreases on unexpected incorrect (high expected → incorrect)
- [ ] Problem rating moves opposite to student rating
- [ ] Dynamic K: improving student gets lower K, struggling student gets higher K
- [ ] ZPD filter returns problems in [R+100, R+300] range
- [ ] ZPD fallback works when no problems in range
- [ ] Ratings clamped to [400, 2800]

---

## Phase 3: Layer 3 — Hierarchical MAB (Week 3)

### Objectives
- Implement Thompson Sampling with Beta priors
- Implement 2-level hierarchy: concept selection → problem selection
- Integrate prerequisite constraints from Knowledge Graph
- Integrate ZPD filtering from Elo
- Define and implement reward function

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/mab_service.py` | MAB: Thompson Sampling, hierarchical selection, reward computation |
| `ai-service/routers/mab.py` | FastAPI endpoints for MAB |
| `ai-service/tests/test_mab.py` | Unit tests for MAB |

### Key Decisions
- Thompson Sampling (not UCB) — no tuning parameter, naturally Bayesian
- Beta(1, 1) uniform prior — maximum initial exploration
- Continuous rewards [0, 1] via fractional alpha/beta updates
- Prerequisite constraint: only concepts with all prereqs P(mastery) ≥ 0.85
- Review priority: due FSRS reviews take precedence (allocated first)

### API Endpoints
```
POST /mab/select          — Select next problem (full pipeline)
POST /mab/update          — Update MAB after observing reward
GET  /mab/state/{user_id} — Get MAB state for debugging/visualization
```

### Test Criteria
- [ ] With no data, arms are selected roughly uniformly (exploration)
- [ ] Arms with higher rewards are selected more frequently over time (exploitation)
- [ ] Locked concepts (unmet prerequisites) are never selected
- [ ] ZPD filtering correctly constrains problem selection
- [ ] Review concepts are prioritized over new concepts when due

---

## Phase 4: Layer 4 — FSRS Spaced Repetition (Week 3–4)

### Objectives
- Implement FSRS-5 algorithm (or integrate `py-fsrs` library)
- Map submission outcomes to FSRS ratings
- Create review queue management
- Create API endpoints

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/fsrs_service.py` | FSRS: review processing, scheduling, queue management |
| `ai-service/routers/fsrs.py` | FastAPI endpoints for FSRS |
| `ai-service/tests/test_fsrs.py` | Unit tests for FSRS |

### Files to Modify

| File | Change |
|------|--------|
| `ai-service/requirements.txt` | Add `py-fsrs` (or implement from scratch) |

### Key Decisions
- **Use `py-fsrs` library** if it provides sufficient control; otherwise implement from [04-ALGORITHM-DESIGN.md](./04-ALGORITHM-DESIGN.md) §4
- Card created on **first encounter** with a concept (first submission to any problem in that concept)
- Rating mapping from submission outcomes (see §4.5 of Algorithm Design)
- Default FSRS-5 parameters; can be optimized per-student later when data accumulates

### API Endpoints
```
POST /fsrs/review         — Process a review event
GET  /fsrs/queue/{user_id} — Get review queue (due + upcoming)
GET  /fsrs/card/{user_id}/{concept_id} — Get specific card state
```

### Test Criteria
- [ ] New card initializes correctly on first review
- [ ] Stability increases after successful review (rating 2–4)
- [ ] Stability decreases (resets) after failed review (rating 1)
- [ ] Retrievability decays over time following power-law curve
- [ ] Review queue returns concepts where R < 0.9
- [ ] Due date calculation is correct (scheduled at t where R = 0.9)
- [ ] Rating mapping from submission outcomes is correct

---

## Phase 5: Integration — Pipeline Orchestration (Week 4–5)

### Objectives
- Create the unified `/adaptive/recommend` endpoint
- Create the unified `/adaptive/update` endpoint (all layers)
- Wire submission hook in NestJS to call AI service
- Handle cold start scenarios
- Add Redis caching

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/adaptive_engine.py` | Orchestrates all layers for recommendation and update |
| `ai-service/routers/adaptive.py` | Unified adaptive endpoints |

### Files to Modify

| File | Change |
|------|--------|
| `server/src/submissions/submissions.service.ts` | Add post-submission hook to call adaptive update |
| `server/src/adaptive/adaptive.module.ts` | New NestJS module proxying to AI service |
| `server/src/adaptive/adaptive.controller.ts` | New endpoints |
| `server/src/adaptive/adaptive.service.ts` | Service calling AI service |
| `ai-service/main.py` | Register adaptive router |

### Integration Flow
```
1. Student submits code
2. NestJS executes code in sandbox
3. NestJS determines result (ACCEPTED/WRONG_ANSWER/...)
4. NestJS calls AI service: POST /adaptive/update
5. AI service updates BKT → Elo → MAB → FSRS (sequentially)
6. AI service returns updated states
7. NestJS stores/caches result
8. Client polls and receives updated recommendation data
```

### Test Criteria
- [ ] End-to-end: submit code → all layers updated → recommendations change
- [ ] Cold start: new student gets beginner recommendations
- [ ] Performance: recommendation generation < 500ms
- [ ] Caching: subsequent requests within TTL use cache

---

## Phase 6: Frontend Updates (Week 5–6)

### Objectives
- Update Dashboard with adaptive metrics
- Create adaptive recommendation component
- Create review queue page
- Create knowledge state visualization (concept mastery tree/radar)
- Create Elo history chart

### Files to Create

| File | Purpose |
|------|---------|
| `client/src/pages/AdaptiveRecommendations.tsx` | Full adaptive recommendation page |
| `client/src/pages/ReviewQueue.tsx` | FSRS review queue page |
| `client/src/components/KnowledgeGraph.tsx` | Interactive concept mastery tree |
| `client/src/components/EloChart.tsx` | Elo rating history chart |
| `client/src/components/MasteryRadar.tsx` | Radar chart of concept mastery |
| `client/src/api/queries/useAdaptive.ts` | TanStack Query hooks for adaptive APIs |

### Files to Modify

| File | Change |
|------|--------|
| `client/src/pages/Dashboard.tsx` | Add adaptive metrics section |
| `client/src/pages/ProblemDetail.tsx` | Add hint button, difficulty indicator |
| `client/src/routes/index.tsx` | Add new routes |

### UI Components

**Dashboard additions:**
- Student Elo rating card with trend arrow
- Mastery progress bar (X/Y concepts mastered)
- Review queue badge (N concepts due)
- Next recommended problem card

**Recommendation page:**
- List of recommended problems with reason labels (REVIEW / NEW / PRACTICE)
- Difficulty match indicator (color-coded: green=good match, yellow=stretch, red=too hard)
- Expected success probability

**Knowledge visualization:**
- Interactive concept tree (nodes colored by mastery: red → yellow → green)
- Prerequisite edges shown
- Locked vs unlocked indicators

**Review queue:**
- List of concepts due for review with urgency indicators
- One-click "Start Review" → navigates to recommended problem for that concept

---

## Phase 7: Layer 5 — LLM Feedback (Optional, Week 6–7)

### Objectives
- Implement RAG pipeline for hint generation
- Build prompt templates
- Add rate limiting
- Create hint UI component

### Files to Create

| File | Purpose |
|------|---------|
| `ai-service/services/llm_service.py` | LLM integration: RAG + prompt engineering + hint generation |
| `ai-service/routers/hints.py` | FastAPI endpoint for hints |
| `client/src/components/HintPanel.tsx` | Hint UI (expandable panel in ProblemDetail) |

### Files to Modify

| File | Change |
|------|--------|
| `ai-service/requirements.txt` | Add openai or anthropic SDK |
| `ai-service/.env` | Add LLM API key |
| `client/src/pages/ProblemDetail.tsx` | Integrate HintPanel |

### Technology Choice
- **LLM:** OpenAI GPT-4o-mini (cost-effective) or Claude Haiku
- **RAG:** Simple retrieval from KG (no vector DB needed — concepts are structured data)
- No LangChain dependency — simple API call with prompt template is sufficient

### Risks
| Risk | Mitigation |
|------|------------|
| LLM gives direct answers | Prompt engineering + output validation |
| API costs | Rate limiting, use cheapest adequate model |
| Latency | Async hint generation, show "thinking..." spinner |

---

## Phase 8: Evaluation (Week 7–10)

### Objectives
- Deploy system for user testing
- Recruit participants
- Run pre-test / intervention / post-test protocol
- Collect and analyze data
- Write evaluation chapter

### Tasks
- [ ] Deploy system to accessible server
- [ ] Create pre-test and post-test (15–20 programming questions)
- [ ] Prepare SUS and TAM questionnaires
- [ ] Recruit 40–60 students
- [ ] Random assignment to experimental (adaptive) and control (non-adaptive) groups
- [ ] Run 4-week intervention
- [ ] Collect all system logs (submissions, recommendations, clicks)
- [ ] Administer post-test and surveys
- [ ] Analyze data (see [07-EVALUATION-PLAN.md](./07-EVALUATION-PLAN.md))

See [07-EVALUATION-PLAN.md](./07-EVALUATION-PLAN.md) for detailed experiment design.

---

## Technology Decisions Summary

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| BKT implementation | Custom Python | pyBKT library | Full control, simple math, pyBKT for later parameter fitting only |
| Elo implementation | Custom Python | Glicko-2, TrueSkill | Elo is simpler, well-understood, sufficient for our needs |
| MAB algorithm | Thompson Sampling | UCB1, LinUCB, ε-greedy | No tuning parameters, naturally Bayesian, proven in education |
| FSRS implementation | py-fsrs library | Custom, SM-2 | Well-tested, matches Anki's production implementation |
| LLM provider | OpenAI GPT-4o-mini | Claude Haiku, local LLaMA | Cost-effective, good at Socratic questioning, widely available |
| KG construction | Manual curation | ACE automated, LLM extraction | Most reliable for thesis scope; automated is future work |
| Inter-service communication | Shared DB (SQLAlchemy reads Prisma-managed DB) | REST API between services, message queue | Lowest latency, simplest architecture |
| Caching | Redis | In-memory, no cache | Already provisioned in Docker Compose, standard choice |
| Frontend charting | Ant Design Charts / ECharts | Recharts, D3 | Matches existing Ant Design UI, good radar/line chart support |

---

## Timeline Summary

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Phase 0: Foundation | KG + DB schema + concept seed data |
| 2 | Phase 1 + 2: BKT + Elo | Knowledge tracing + difficulty calibration working |
| 3 | Phase 3 + 4: MAB + FSRS | Problem selection + review scheduling working |
| 4–5 | Phase 5: Integration | End-to-end adaptive pipeline working |
| 5–6 | Phase 6: Frontend | Updated UI with all adaptive features |
| 6–7 | Phase 7: LLM (optional) | Hint generation working |
| 7–10 | Phase 8: Evaluation | Experiments completed, data analyzed |

**Total: ~10 weeks** (March → May 2026)

---

## Rollback Strategy

Each phase is independently deployable. If a layer proves problematic:

1. **Disable at MAB level:** MAB can operate without any layer by falling back to random selection
2. **Feature flags:** Each layer can be toggled on/off via environment variable
3. **Database:** New tables are additive; dropping them doesn't affect existing functionality
4. **API:** New endpoints are separate from existing ones; old endpoints continue working

```python
# Feature flags in AI service
ENABLE_BKT = os.getenv('ENABLE_BKT', 'true') == 'true'
ENABLE_ELO = os.getenv('ENABLE_ELO', 'true') == 'true'
ENABLE_MAB = os.getenv('ENABLE_MAB', 'true') == 'true'
ENABLE_FSRS = os.getenv('ENABLE_FSRS', 'true') == 'true'
ENABLE_LLM = os.getenv('ENABLE_LLM', 'false') == 'false'
```
