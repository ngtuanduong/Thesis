# Implementation Tracker — Living Checklist

**Thesis:** Adaptive Learning Platform for University Programming Courses
**Last Updated:** 2026-02-27

---

## Status Legend

| Symbol | Status | Meaning |
|--------|--------|---------|
| ⬜ | NOT STARTED | Work has not begun |
| 🔲 | IN PROGRESS | Currently being worked on |
| ✅ | DONE | Completed and tested |
| ❌ | BLOCKED | Cannot proceed, dependency unmet |
| ⏭️ | SKIPPED | Deliberately deferred |

---

## Current System State Audit

### What's Already Built (✅)

| Component | Status | Notes |
|-----------|--------|-------|
| React frontend (Vite + TypeScript + Ant Design) | ✅ DONE | Login, Dashboard, Problems, ProblemDetail, Profile pages |
| NestJS backend (Prisma ORM) | ✅ DONE | Auth, Users, Problems, Submissions, Courses modules |
| PostgreSQL + pgvector | ✅ DONE | Running in Docker, pgvector extension enabled |
| FastAPI AI service | ✅ DONE | Embedding, basic recommendations, skill profiling |
| Docker sandbox code execution | ✅ DONE | Python execution with 256MB memory, 5s timeout, no network |
| JWT authentication | ✅ DONE | Register, login, role-based guards |
| Problem CRUD | ✅ DONE | Create/read with test cases, difficulty tags |
| Submission system | ✅ DONE | Submit → execute → evaluate → store result |
| Content-based recommendations | ✅ DONE | Sentence transformer + pgvector cosine similarity |
| Skill profiling | ✅ DONE | Difficulty-weighted tag scores, embedding per skill |
| Docker Compose orchestration | ✅ DONE | postgres, redis, backend, ai-service, prisma-migrate |
| Seed data | ✅ DONE | 5 problems (Two Sum, Palindrome, etc.) |

### What Needs to Change (🔲 → ✅)

| Component | Current State | Target State |
|-----------|--------------|-------------|
| Recommendation engine | Content-based (cosine similarity) | 5-layer adaptive (BKT+Elo+MAB+FSRS+LLM) |
| Skill model | Tag-based embedding scores | BKT per-concept mastery probabilities |
| Difficulty system | Static labels (EASY/MEDIUM/HARD) | Dynamic Elo ratings calibrated from submissions |
| Problem selection | Most similar to profile | Hierarchical MAB with ZPD constraints |
| Forgetting model | None | FSRS spaced repetition per concept |
| Concept structure | Flat tags | Knowledge Graph with prerequisites |
| Hint system | None | LLM + RAG Socratic hints |
| Dashboard | Basic stats + old recommendations | Adaptive metrics + mastery visualization |
| Redis | Provisioned but unused | Active caching for adaptive states |

---

## Phase 0: Foundation — Knowledge Graph & Schema

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 0.1 | Design concept taxonomy (~30 concepts) | ⬜ | Covers all Python course topics |
| 0.2 | Define prerequisite edges (~40-50 edges) | ⬜ | DAG (no cycles), covers dependencies |
| 0.3 | Map existing 5 problems to concepts | ⬜ | Each problem has 1 primary + 0-2 secondary concepts |
| 0.4 | Add Prisma schema: Concept model | ⬜ | `npx prisma migrate dev` succeeds |
| 0.5 | Add Prisma schema: KnowledgeGraphEdge model | ⬜ | Migration succeeds |
| 0.6 | Add Prisma schema: ProblemConcept model | ⬜ | Migration succeeds |
| 0.7 | Add Prisma schema: KnowledgeState model | ⬜ | Migration succeeds |
| 0.8 | Add Prisma schema: EloRating model | ⬜ | Migration succeeds |
| 0.9 | Add Prisma schema: MabState model | ⬜ | Migration succeeds |
| 0.10 | Add Prisma schema: FsrsCard model | ⬜ | Migration succeeds |
| 0.11 | Write seed script: concepts + edges | ⬜ | Seed runs without errors, data in DB |
| 0.12 | Write seed script: problem-concept mappings | ⬜ | All problems have at least 1 concept |
| 0.13 | Create NestJS Concepts module (CRUD) | ⬜ | GET/POST/PUT endpoints work |
| 0.14 | Create NestJS KG endpoints | ⬜ | GET graph, POST/DELETE edges work |
| 0.15 | Add SQLAlchemy models in AI service | ⬜ | Models match Prisma schema |
| 0.16 | Verify DB schema alignment | ⬜ | Prisma and SQLAlchemy agree on all columns |

---

## Phase 1: Layer 1 — BKT Knowledge Tracing

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 1.1 | Implement BKT update function | ⬜ | Unit test: correct math for P(L) updates |
| 1.2 | Implement BKT predict function | ⬜ | Unit test: P(correct) = P(L)(1-P(S)) + (1-P(L))P(G) |
| 1.3 | Implement multi-concept update logic | ⬜ | Primary concept: full update. Secondary: attenuated |
| 1.4 | Implement knowledge state initialization | ⬜ | New student gets default params per concept tier |
| 1.5 | Create FastAPI /kt/update endpoint | ⬜ | POST returns updated P(mastery) |
| 1.6 | Create FastAPI /kt/state endpoint | ⬜ | GET returns all concept masteries for student |
| 1.7 | Create FastAPI /kt/predict endpoint | ⬜ | GET returns P(correct) for specific problem |
| 1.8 | Write unit tests for BKT math | ⬜ | 10+ test cases covering edge cases |
| 1.9 | Integration test: submission → BKT update | ⬜ | End-to-end data flow works |

---

## Phase 2: Layer 2 — Dynamic K-Value Elo

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 2.1 | Implement standard Elo update | ⬜ | Unit test: rating changes match formula |
| 2.2 | Implement dynamic K-value calculation | ⬜ | K decreases when improving, increases when struggling |
| 2.3 | Implement dual update (student + problem) | ⬜ | Both ratings move in opposite directions |
| 2.4 | Implement problem Elo initialization | ⬜ | EASY=1000, MEDIUM=1400, HARD=1800 |
| 2.5 | Implement ZPD filtering | ⬜ | Returns problems in [R+100, R+300] range |
| 2.6 | Implement ZPD fallback (expand range) | ⬜ | Widens range if no problems found |
| 2.7 | Implement rating history storage | ⬜ | JSONB array appended on each update |
| 2.8 | Create FastAPI /elo endpoints | ⬜ | Update, query student/problem, ZPD |
| 2.9 | Write unit tests for Elo math | ⬜ | 10+ test cases |
| 2.10 | Initialize Elo for all existing problems | ⬜ | Seed script sets initial ratings |

---

## Phase 3: Layer 3 — Hierarchical MAB

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 3.1 | Implement Thompson Sampling (Beta dist) | ⬜ | Arms selected proportional to expected reward |
| 3.2 | Implement concept-level selection (Level 1) | ⬜ | Eligible concepts filtered by prerequisites |
| 3.3 | Implement problem-level selection (Level 2) | ⬜ | Problems filtered by ZPD |
| 3.4 | Implement prerequisite constraint logic | ⬜ | Locked concepts never selected |
| 3.5 | Implement reward function | ⬜ | Reward combines learning gain + difficulty match + efficiency |
| 3.6 | Implement review priority logic | ⬜ | FSRS due reviews selected before new concepts |
| 3.7 | Implement MAB state update | ⬜ | Alpha/beta updated proportionally to reward |
| 3.8 | Create FastAPI /mab endpoints | ⬜ | Select, update, state query |
| 3.9 | Write unit tests | ⬜ | Exploration vs exploitation behavior verified |

---

## Phase 4: Layer 4 — FSRS Spaced Repetition

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 4.1 | Implement (or integrate) FSRS-5 algorithm | ⬜ | Stability and difficulty update correctly |
| 4.2 | Implement retrievability decay calculation | ⬜ | R follows power-law: (1 + t/(9S))^(-1) |
| 4.3 | Implement submission-to-rating mapping | ⬜ | Rating 1-4 correctly assigned based on outcome |
| 4.4 | Implement card creation on first encounter | ⬜ | Card created when student first attempts concept |
| 4.5 | Implement review queue management | ⬜ | Due items (R<0.9) returned sorted by urgency |
| 4.6 | Implement due date scheduling | ⬜ | Next review at t=S days (when R=0.9) |
| 4.7 | Create FastAPI /fsrs endpoints | ⬜ | Review, queue, card query |
| 4.8 | Write unit tests | ⬜ | Stability increases on success, decreases on failure |

---

## Phase 5: Integration — Pipeline Orchestration

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 5.1 | Create adaptive_engine.py (orchestrator) | ⬜ | Single function calls all layers in order |
| 5.2 | Create /adaptive/recommend endpoint | ⬜ | Returns recommendations with reasons and metadata |
| 5.3 | Create /adaptive/update endpoint | ⬜ | Accepts submission result, updates all layers |
| 5.4 | Create /adaptive/knowledge-state endpoint | ⬜ | Returns complete student state for dashboard |
| 5.5 | Create /adaptive/review-queue endpoint | ⬜ | Returns due + upcoming reviews |
| 5.6 | Wire NestJS submission hook | ⬜ | POST /submissions triggers AI service update |
| 5.7 | Create NestJS adaptive module | ⬜ | Proxies to AI service adaptive endpoints |
| 5.8 | Implement cold start handling | ⬜ | New student gets beginner recommendations |
| 5.9 | Add Redis caching | ⬜ | Knowledge state cached 5min, KG cached 1hr |
| 5.10 | Performance test: < 500ms recommendation | ⬜ | Measure latency end-to-end |
| 5.11 | End-to-end integration test | ⬜ | Submit → update → recommend cycle works |

---

## Phase 6: Frontend Updates

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 6.1 | Create useAdaptive.ts query hooks | ⬜ | TanStack Query hooks for all adaptive endpoints |
| 6.2 | Update Dashboard: Elo card | ⬜ | Shows student Elo with trend indicator |
| 6.3 | Update Dashboard: mastery progress | ⬜ | Shows X/Y concepts mastered |
| 6.4 | Update Dashboard: review queue badge | ⬜ | Shows count of due reviews |
| 6.5 | Create AdaptiveRecommendations page | ⬜ | Lists recommendations with reasons |
| 6.6 | Create ReviewQueue page | ⬜ | Lists due reviews with "Start Review" action |
| 6.7 | Create KnowledgeGraph visualization | ⬜ | Interactive concept tree with mastery colors |
| 6.8 | Create EloChart component | ⬜ | Line chart of Elo history |
| 6.9 | Create MasteryRadar component | ⬜ | Radar chart of concept mastery levels |
| 6.10 | Update ProblemDetail: difficulty indicator | ⬜ | Shows Elo match and expected success |
| 6.11 | Add routes for new pages | ⬜ | React Router routes registered |
| 6.12 | Responsive design check | ⬜ | All new components render on mobile |

---

## Phase 7: Layer 5 — LLM Feedback (Optional)

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 7.1 | Implement hint generation service | ⬜ | Returns Socratic question, not answer |
| 7.2 | Build RAG context retrieval | ⬜ | Retrieves relevant KG context |
| 7.3 | Engineer prompt templates | ⬜ | Hints are pedagogically sound |
| 7.4 | Add rate limiting | ⬜ | Max 3 hints/problem, 10/day |
| 7.5 | Create FastAPI /hint endpoint | ⬜ | Returns hint within 5 seconds |
| 7.6 | Create HintPanel component | ⬜ | Expandable panel in ProblemDetail |
| 7.7 | Integration test | ⬜ | End-to-end: click hint → get response |

---

## Phase 8: Evaluation

| # | Task | Status | Test Criteria |
|---|------|--------|--------------|
| 8.1 | Deploy to accessible server | ⬜ | System accessible from university network |
| 8.2 | Create pre-test questions | ⬜ | 15-20 Python problems covering all concept tiers |
| 8.3 | Create post-test questions | ⬜ | Parallel form to pre-test (same difficulty, different problems) |
| 8.4 | Prepare SUS questionnaire | ⬜ | 10-item standard SUS |
| 8.5 | Prepare TAM questionnaire | ⬜ | Perceived Usefulness + Ease of Use |
| 8.6 | Recruit 40-60 participants | ⬜ | From Hanoi University programming courses |
| 8.7 | Random assignment to groups | ⬜ | Experimental (adaptive) vs Control (non-adaptive) |
| 8.8 | Administer pre-test | ⬜ | Baseline scores recorded |
| 8.9 | Run 4-week intervention | ⬜ | Both groups use system for 4 weeks |
| 8.10 | Administer post-test + surveys | ⬜ | Post scores + SUS + TAM recorded |
| 8.11 | Collect system logs | ⬜ | All submissions, recommendations, clicks exported |
| 8.12 | Statistical analysis | ⬜ | NLG, t-tests, effect sizes computed |
| 8.13 | Write Chapter 5 (Evaluation) | ⬜ | Draft complete |

---

## Progress Summary

| Phase | Total Tasks | Done | In Progress | Not Started | % Complete |
|-------|------------|------|-------------|-------------|------------|
| Phase 0: Foundation | 16 | 0 | 0 | 16 | 0% |
| Phase 1: BKT | 9 | 0 | 0 | 9 | 0% |
| Phase 2: Elo | 10 | 0 | 0 | 10 | 0% |
| Phase 3: MAB | 9 | 0 | 0 | 9 | 0% |
| Phase 4: FSRS | 8 | 0 | 0 | 8 | 0% |
| Phase 5: Integration | 11 | 0 | 0 | 11 | 0% |
| Phase 6: Frontend | 12 | 0 | 0 | 12 | 0% |
| Phase 7: LLM (Optional) | 7 | 0 | 0 | 7 | 0% |
| Phase 8: Evaluation | 13 | 0 | 0 | 13 | 0% |
| **TOTAL** | **95** | **0** | **0** | **95** | **0%** |

**Existing system (pre-adaptive): ~15 components ✅ DONE**
**Adaptive upgrade: 95 tasks ⬜ NOT STARTED**
