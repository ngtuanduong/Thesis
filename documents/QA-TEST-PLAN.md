# QA & Test Plan — AdaptLearn Platform

> Ke hoach kiem thu toan dien cho he thong AdaptLearn.
> Bao gom: ma tran test, Backend unit test (Jest), E2E test (Playwright), Integration test, Non-functional test, va huong dan chay.

---

## 1. Tong quan test coverage

### 1.1 Ma tran kiem thu theo tang

| Tang | Framework | So luong test | So file | Coverage |
|------|-----------|---------------|---------|----------|
| **Backend Unit** | Jest + @nestjs/testing | 146 test cases | 18 suites | Tat ca 14 modules + guards + filters + middleware + utils |
| **AI Service Unit** | Pytest | 5 modules | 5 files | BKT, Elo, MAB, FSRS, Integration |
| **Frontend E2E** | Playwright | ~65 test cases | 8 suites | Auth, Student, Instructor, Admin, Security, Error, Performance, Functional |
| **Integration** | Jest | 5 test cases | 1 suite | Submission pipeline end-to-end |
| **Tong cong** | | **~220+ tests** | **32 files** | |

### 1.2 Ma tran kiem thu theo feature

| Feature | Unit Test | E2E Test | Integration | Manual QA |
|---------|-----------|----------|-------------|-----------|
| **Dang nhap / Dang ky** | ✅ auth.service.spec | ✅ auth.spec.ts | | |
| **Dang ky tai khoan** | ✅ auth.service.spec | ✅ auth.spec.ts | | |
| **Dang xuat** | | ✅ auth.spec.ts | | |
| **Phien lam viec (session)** | | ✅ auth.spec.ts | | |
| **Danh sach bai tap** | ✅ problems.service.spec | ✅ student-flow.spec | | |
| **Loc/Tim kiem bai tap** | | ✅ student-flow.spec | | |
| **Giai bai (code editor)** | ✅ submissions.service.spec | ✅ student-flow.spec | ✅ pipeline | Can Docker |
| **Code Execution (Docker)** | ✅ code-execution.service.spec | | ✅ pipeline | Can Docker daemon |
| **Starter Code Generation** | ✅ starter-code.util.spec | | | |
| **Knowledge Map** | ✅ concepts.service.spec | ✅ student-flow.spec | | |
| **Review Queue (FSRS)** | | ✅ student-flow.spec | | |
| **Profile & Skills** | ✅ skills.service.spec | ✅ student-flow.spec | | |
| **SUS Survey** | | ✅ student-flow.spec | | |
| **Instructor Dashboard** | ✅ instructor.service.spec | ✅ instructor-flow.spec | | |
| **Quan ly bai tap (CRUD)** | ✅ problems.service.spec | ✅ instructor-flow.spec | | |
| **Admin Dashboard** | ✅ admin.service.spec | ✅ admin-flow.spec | | |
| **Quan ly user/groups** | ✅ admin.service.spec | ✅ admin-flow.spec | | |
| **Experiment A/B Testing** | ✅ admin.service.spec | ✅ admin-flow.spec | | |
| **Export Events** | ✅ admin.service.spec | | | |
| **RBAC (phan quyen)** | ✅ roles.guard.spec | ✅ admin-flow.spec + security.spec | | |
| **Adaptive Recommendations** | ✅ adaptive.service.spec + recommendations.service.spec | | | Can AI service |
| **AI Hint Generation** | ✅ ai.service.spec | | | Can AI service |
| **AI Service Integration** | ✅ ai.service.spec | | | |
| **User Management** | ✅ users.service.spec | | | |
| **Course Management** | ✅ courses.service.spec | | | |
| **BKT Knowledge Tracing** | ✅ test_bkt.py | | | |
| **Elo Rating** | ✅ test_elo.py | | | |
| **MAB Selection** | ✅ test_mab.py | | | |
| **FSRS Scheduling** | ✅ test_fsrs.py | | | |
| **Full Adaptive Pipeline** | ✅ test_integration.py | | | |
| **Error Handling (Filter)** | ✅ http-exception.filter.spec | ✅ error-handling.spec | | |
| **Logging Middleware** | ✅ logging.middleware.spec | | | |
| **Security (Route Protection)** | ✅ roles.guard.spec | ✅ security.spec.ts | | |
| **Performance** | | ✅ performance.spec.ts | | |
| **Swagger API Docs** | | | | Manual: GET /api/docs |

---

## 2. Backend Unit Tests (Jest)

### 2.1 auth.service.spec.ts — Authentication (5 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Register: create user with hashed password | bcrypt hash, JWT token tra ve |
| 2 | Register: throw ConflictException | Email da ton tai |
| 3 | Login: return token on valid credentials | bcrypt compare, JWT sign |
| 4 | Login: throw UnauthorizedException | Sai mat khau |
| 5 | Login: throw UnauthorizedException | User khong ton tai |

### 2.2 problems.service.spec.ts — Problem CRUD (11 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Create: basic problem with embedding | Prisma create, AI embed called |
| 2 | FindAll: no courseId filter | Return all, only public test cases |
| 3 | FindAll: with courseId filter | Filter by courseId |
| 4 | FindById: found | Return with all test cases |
| 5 | FindById: not found | NotFoundException |
| 6 | Update: basic update | Prisma update |
| 7 | Remove: delete problem | Prisma delete |
| 8 | Create: auto-generate starterCode | TestCases → starterCode |
| 9 | Create: don't overwrite explicit starterCode | Giu nguyen user starterCode |
| 10 | Create: handle embedding failure | Fire-and-forget, khong throw |
| 11 | Update: replace testCases + regenerate starterCode | deleteMany + create pattern |

### 2.3 starter-code.util.spec.ts — Starter Code Generation (12 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Empty test cases → DEFAULT_STARTER_CODE | Fallback |
| 2 | Null/undefined → DEFAULT_STARTER_CODE | Edge case |
| 3 | Dict input → named params | `def solution(nums, target):` |
| 4 | Dict with string values | Param type inference |
| 5 | Single key dict | `def solution(nums):` |
| 6 | Flat list → *data | `def solution(*data):` |
| 7 | Nested list → *items | `def solution(*items):` |
| 8 | Empty list | `Any each` type hint |
| 9 | List of strings | `str each` type hint |
| 10 | Scalar int | `def solution(n):` |
| 11 | Scalar float | `def solution(n): float` |
| 12 | Non-JSON string | `def solution(s):` |

### 2.4 submissions.service.spec.ts — Submissions (7 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Create: PENDING status | Prisma create with PENDING |
| 2 | FindById: found | Return submission |
| 3 | FindById: not found | NotFoundException |
| 4 | FindByUser: ordered by date | Include problem metadata |
| 5 | FindByProblem: filter by user | Correct where clause |
| 6 | Create: triggers async execution | executeSubmission called |
| 7 | Execute: RUNTIME_ERROR on no test cases | Status transition |

### 2.5 code-execution.service.spec.ts — Docker Code Sandbox (11 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Docker unavailable → descriptive error | Error message |
| 2 | API version mismatch → specific error | Error detection |
| 3 | Build image when not exists | docker build called |
| 4 | Skip build when image exists | Only 2 exec calls |
| 5 | Unsupported language → RUNTIME_ERROR | Only Python |
| 6 | All tests pass → ACCEPTED | Status + output |
| 7 | Failing test → WRONG_ANSWER | Expected vs Got |
| 8 | Timeout → TIME_LIMIT | error.killed detection |
| 9 | Stderr → RUNTIME_ERROR | Error message extraction |
| 10 | Docker throw → RUNTIME_ERROR | Stderr from exception |
| 11 | Stop at first failure | Not run remaining tests |

### 2.6 submission-pipeline.integration.spec.ts — Pipeline Integration (5 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | ACCEPTED pipeline | PENDING→RUNNING→ACCEPTED + adaptive update |
| 2 | WRONG_ANSWER pipeline | isCorrect=false + adaptive update |
| 3 | RUNTIME_ERROR pipeline | Adaptive NOT called |
| 4 | TIME_LIMIT pipeline | Adaptive NOT called |
| 5 | Execution error | Catch error → RUNTIME_ERROR |

### 2.7 users.service.spec.ts — User Management (5 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Create: success | User created |
| 2 | Create: ConflictException | Email da ton tai |
| 3 | FindByEmail: found / null | Return user or null |
| 4 | FindById: found / NotFoundException | Return or throw |
| 5 | FindAll: sanitized fields | Select chi truong can thiet |

### 2.8 courses.service.spec.ts — Course Management (5 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Create with instructor ID | Prisma create |
| 2 | FindAll with instructor | Include instructor info |
| 3 | FindById: found | Include problems |
| 4 | FindById: NotFoundException | Course khong ton tai |
| 5 | Enroll: success + duplicate | Create enrollment, P2002 error |

### 2.9 skills.service.spec.ts — Skill Profile (4 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | GetByUser: sorted by score | OrderBy desc |
| 2 | GetByUser: empty array | No skills |
| 3 | Upsert: create/update | Prisma upsert |
| 4 | ComputeProfile: delegate + error propagation | AiService call |

### 2.10 recommendations.service.spec.ts — Recommendations (4 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | AI service → mapped results | Transform response |
| 2 | AI down → fallback (unsolved problems) | Exclude solved |
| 3 | Default limit = 10 | Parameter default |
| 4 | Empty fallback | All problems solved |

### 2.11 admin.service.spec.ts — Admin Operations (10 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | GetStats: aggregation | All counts |
| 2 | GetUsers: with submission counts | Include _count + experimentGroup |
| 3 | AssignGroup: AI service delegation | POST to AI |
| 4 | AssignGroup: local fallback | Prisma upsert |
| 5 | GetExperimentStats: AI service | Return stats |
| 6 | GetExperimentStats: local fallback | groupBy |
| 7 | ExportEvents: AI delegation | With event filter |
| 8 | ExportEvents: without filter | No event param |
| 9 | ExportEvents: local fallback with filter | EventLog query |
| 10 | ExportEvents: local fallback no filter | Empty where |

### 2.12 instructor.service.spec.ts — Instructor Features (7 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | GetDashboard: full stats | enrolled, submissions, mastery, struggling |
| 2 | GetDashboard: empty course | All zeros, empty arrays |
| 3 | GetDashboard: identify struggling students | Avg mastery < 0.5 |
| 4 | GetStudents: enriched list | submissions, mastery, elo |
| 5 | GetStudents: no data | Zero defaults, null elo |
| 6 | GetProblemsManage: acceptance rate | accepted/total calculation |
| 7 | GetProblemsManage: zero submissions | Rate = 0 |

### 2.13 ai.service.spec.ts — AI Service Client (13 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Headers: Content-Type + X-Service-Key | Correct headers |
| 2 | EmbedProblem: POST /embed/problem | Snake_case mapping |
| 3 | GetRecommendations: GET with limit | URL construction |
| 4 | UpdateAdaptiveLayers: POST snake_case | camelCase → snake_case |
| 5 | GenerateHint: POST /hints/generate | Payload mapping |
| 6 | GetKnowledgeState: GET | URL construction |
| 7 | GetReviewQueue: GET | URL construction |
| 8 | LogEvent: POST /evaluation/log | Session ID mapping |
| 9 | ExportEvents: with filter | Query string encoding |
| 10 | ExportEvents: without filter | No query string |
| 11 | Error: 500 response | Throw with status + body |
| 12 | Error: 404 response | Throw with status |
| 13 | AssignGroup + GetEloHistory | POST + GET |

### 2.14 roles.guard.spec.ts — RBAC Guard (5 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | No @Roles decorator → allow | Default access |
| 2 | Role matches → allow | Single role check |
| 3 | Role mismatch → deny | Access denied |
| 4 | Multiple roles (any match) → allow | OR logic |
| 5 | Multiple roles (none match) → deny | Deny all |

### 2.15 http-exception.filter.spec.ts — Error Filter (4 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Correct JSON shape | statusCode, message, timestamp |
| 2 | String exception | Direct string message |
| 3 | Object exception | Extract .message field |
| 4 | Valid ISO timestamp | Date format |

### 2.16 logging.middleware.spec.ts — HTTP Logger (6 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Calls next() | Middleware chain |
| 2 | Registers finish listener | res.on('finish') |
| 3 | Log request details | method, URL, status |
| 4 | Warn for status >= 400 | logger.warn called |
| 5 | Warn for 500 errors | Server error logging |
| 6 | Duration in ms | Timing measurement |

---

## 3. E2E Test Suites (Playwright)

### 3.1 auth.spec.ts — Authentication (9 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Display login form | Form hien thi dung (email, password, button) |
| 2 | Switch to register tab | Tab register hien thi truong name |
| 3 | Validation errors on empty submit | 2 error messages |
| 4 | Login with valid credentials | Redirect to dashboard |
| 5 | Error on invalid credentials | Stay on /login |
| 6 | Redirect unauthenticated to login | /problems → /login |
| 7 | **Register new account** | Unique email → redirect dashboard |
| 8 | **Logout and redirect** | Click logout → /login |
| 9 | **Session persistence after reload** | Reload → van o dashboard |

### 3.2 student-flow.spec.ts — Student Core Flow (16 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Dashboard | Stats cards render | "Problems Solved", "Total Submissions" |
| 2 | Dashboard | Onboarding modal | Modal welcome cho user moi |
| 3 | Problems | Problem list renders | Table co data, rows hien thi |
| 4 | Problems | Filter by difficulty | Loc EASY → chi con tag EASY |
| 5 | Problems | Search by title | Tim "Swap Two" → ket qua |
| 6 | Problem Solving | Code editor visible | CodeMirror `.cm-editor` render |
| 7 | Problem Solving | Submit button present | Button "Submit" hien thi |
| 8 | Knowledge Map | Page renders | Text "knowledge" hien thi |
| 9 | **Knowledge Map** | **Graph nodes render** | `.react-flow__node` count > 0 |
| 10 | **Knowledge Map** | **Graph edges render** | `.react-flow__edge` count > 0 |
| 11 | Review Queue | Page loads | Text "review" hien thi |
| 12 | **Review Queue** | **Items or empty state** | Cards hoac empty message |
| 13 | Profile | User info correct | Ten, email hien thi dung |
| 14 | **Profile** | **Skill refresh** | Button refresh, page van functional |
| 15 | Survey | 10 questions displayed | 10 cards |
| 16 | **Survey** | **Enable submit after answering all** | Radio buttons → button enabled |

### 3.3 instructor-flow.spec.ts — Instructor Flow (10 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Dashboard | Instructor menu visible | Menu "Instructor" |
| 2 | Dashboard | Navigate to instructor page | URL /instructor |
| 3 | Dashboard | Course selector and stats | Select hien thi |
| 4 | Problem Mgmt | Navigate to management | URL /instructor/problems |
| 5 | Problem Mgmt | Table with actions | Edit, Delete buttons |
| 6 | Problem Mgmt | Create modal opens | Modal "Create Problem" |
| 7 | **Problem Mgmt** | **Create a new problem** | Fill form, save, verify in table |
| 8 | **Problem Mgmt** | **Edit existing problem** | Open modal, verify pre-filled data |
| 9 | **Problem Mgmt** | **Delete confirmation** | Popover/modal confirm hien thi |

### 3.4 admin-flow.spec.ts — Admin Flow + RBAC (12 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Admin | Admin menu visible | Menu "Admin" |
| 2 | Admin | Navigate to admin page | URL /admin |
| 3 | Admin | Platform stats | Stat cards hien thi |
| 4 | Admin | User management table | Table voi users |
| 5 | **Admin Ops** | **Experiment statistics** | Experiment/group text visible |
| 6 | **Admin Ops** | **Group assignment controls** | Select dropdowns in table |
| 7 | **Admin Ops** | **Assign group to user** | Select option, verify update |
| 8 | RBAC | Student KHONG thay admin | Phan quyen |
| 9 | RBAC | Instructor KHONG thay admin | Phan quyen |
| 10 | RBAC | Admin thay ALL | Phan quyen |

### 3.5 security.spec.ts — Security & Access Control (6 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Route Protection | Student → /admin redirect | Khong o trang /admin |
| 2 | Route Protection | Student → /instructor redirect | Khong o trang /instructor |
| 3 | Route Protection | Instructor → /admin redirect | Khong o trang /admin |
| 4 | Auth Protection | Unauthenticated API → 401 | HTTP 401 status |
| 5 | Auth Protection | Malformed token → /login | Redirect login |
| 6 | Auth Protection | Empty token → /login | Redirect login |

### 3.6 error-handling.spec.ts — Error Handling (3 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | API 500 → graceful (no white screen) | Body text > 10 chars |
| 2 | Network timeout → layout visible | Sidebar van hien thi |
| 3 | Page reload → no white screen | Content hien thi |

### 3.7 performance.spec.ts — Page Load Performance (4 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Dashboard load < 5s | Sidebar visible within 5s |
| 2 | Problems list load < 5s | Table visible within 5s |
| 3 | Problem detail + CodeMirror < 8s | Editor visible within 8s |
| 4 | Knowledge Map render < 8s | ReactFlow visible within 8s |

### 3.8 functional.spec.ts — Functional Tests (11 tests, can Docker)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Code Submit | Correct code → ACCEPTED | Type code → Submit → "ACCEPTED" hien thi |
| 2 | Code Submit | Wrong code → WRONG_ANSWER | Code sai → "WRONG ANSWER" + Expected/Got |
| 3 | Code Submit | Infinite loop → TIME_LIMIT | `while True` → "TIME LIMIT" sau ~5s |
| 4 | Code Submit | Syntax error → RUNTIME_ERROR | `1/0` → "RUNTIME ERROR" |
| 5 | Knowledge Map | Mastery nodes render | Nodes co data tu adaptive layers |
| 6 | Instructor CRUD | Create problem | Fill form → save → hien thi trong table |
| 7 | Instructor CRUD | Edit problem | Open modal → pre-filled data → verify |
| 8 | Instructor CRUD | Delete confirmation | Popover confirm hien thi |
| 9 | Admin | Assign experiment group | Select dropdown → chon group |
| 10 | AI Hints | Request hint | "Get Hint" → hint text hoac error fallback |
| 11 | History | Submission history tab | Tab "Submissions" → table hien thi |

---

## 4. Huong dan chay test

### 4.1 Prerequisites

**Backend + Database phai dang chay**:
```bash
# Terminal 1: Start database
docker compose -f docker/docker-compose.yml up postgres redis -d

# Terminal 2: Start backend
cd server && npm run start:dev

# Terminal 3: Start frontend
cd client && npm run dev
```

**Seed data phai co**:
```bash
cd server && npx ts-node prisma/seed.ts
```

### 4.2 Chay Backend Unit Tests

```bash
cd server
npm test                    # Chay tat ca 146 tests (18 suites)
npm run test:cov           # Chay voi coverage report
npx jest src/submissions/  # Chay 1 folder cu the
npx jest --testPathPattern="code-execution"  # Chay 1 file cu the
```

### 4.3 Chay E2E Tests

```bash
# Chay tat ca (headless)
npm run test:e2e

# Chay voi Playwright UI (interactive)
npm run test:e2e:ui

# Chay voi browser hien thi (debug)
npm run test:e2e:headed

# Chay 1 file cu the
npx playwright test e2e/auth.spec.ts
npx playwright test e2e/security.spec.ts

# Chay 1 test cu the
npx playwright test -g "should login with valid credentials"
```

### 4.4 Chay AI Service Tests

```bash
cd ai-service
python -m pytest tests/ -v              # Verbose output
python -m pytest tests/test_bkt.py -v   # Chi chay BKT tests
```

### 4.5 Chay tat ca

```bash
npm run test:all       # Backend unit + E2E
```

### 4.6 Xem test report

```bash
npx playwright show-report  # HTML report voi screenshots, traces, timing
```

---

## 5. Manual QA Checklist

### 5.1 Smoke Test (truoc moi lan demo — 15 buoc)

- [ ] Truy cap http://localhost:5173 → trang Login hien thi
- [ ] Dang nhap `student1@example.com` / `password123` → Dashboard hien thi
- [ ] Navigate Problems → danh sach bai tap hien thi (30+ bai)
- [ ] Click 1 bai → Code editor hien thi
- [ ] Navigate Knowledge Map → graph render voi nodes va edges
- [ ] Navigate Review Queue → trang hien thi (items hoac empty state)
- [ ] Navigate Profile → thong tin dung (ten, email, role)
- [ ] Navigate Survey → 10 cau hoi hien thi
- [ ] Dang nhap `instructor@example.com` → thay Instructor menu
- [ ] Navigate Instructor Dashboard → stats hien thi
- [ ] Navigate Manage Problems → table voi Edit/Delete
- [ ] Dang nhap `admin@example.com` → thay Admin menu
- [ ] Navigate Admin Dashboard → stat cards + user table + experiment section
- [ ] Swagger: http://localhost:3000/api/docs → API docs hien thi
- [ ] Reload bat ky trang → khong bi white screen

### 5.2 Functional Test (khi co Docker)

> **DA TU DONG HOA:** Tat ca items duoi day da duoc cover trong `e2e/functional.spec.ts`.
> Chay: `npx playwright test e2e/functional.spec.ts --headed`

- [x] Submit code dung → status ACCEPTED ← `functional.spec.ts` test 1
- [x] Submit code sai → status WRONG_ANSWER ← `functional.spec.ts` test 2
- [x] Submit vong lap vo han → status TIME_LIMIT ← `functional.spec.ts` test 3
- [x] Submit syntax error → status RUNTIME_ERROR ← `functional.spec.ts` test 4
- [x] Sau ACCEPTED → Knowledge Map co mastery nodes ← `functional.spec.ts` test 5
- [x] Instructor tao bai moi ← `functional.spec.ts` test 6
- [x] Instructor sua bai (verify pre-fill) ← `functional.spec.ts` test 7
- [x] Instructor xoa bai (confirm dialog) ← `functional.spec.ts` test 8
- [x] Admin assign experiment group ← `functional.spec.ts` test 9
- [x] AI hint request → hint hoac fallback ← `functional.spec.ts` test 10
- [x] Submission history tab ← `functional.spec.ts` test 11

### 5.3 Edge Case Test

- [ ] Dang nhap sai 5 lan → rate limiter block (429 status)
- [ ] Tat AI service → Dashboard van hien thi (graceful degradation)
- [ ] Tat AI service → Submit code van hoat dong (adaptive update fail silently)
- [ ] Reload trang bat ky → khong bi white screen (Error Boundary)
- [ ] Mo 2 tab → dang nhap 1 tab, tab kia tu cap nhat
- [ ] Mobile (375px width) → layout khong bi vo, drawer navigation

### 5.4 Cross-Browser Testing

- [ ] Chrome (phien ban moi nhat) — tat ca chuc nang hoat dong
- [ ] Firefox (phien ban moi nhat) — tat ca chuc nang hoat dong
- [ ] Edge (phien ban moi nhat) — tat ca chuc nang hoat dong

### 5.5 Responsive Layout Verification

- [ ] Mobile (375px) → Drawer navigation, single-column, tab-based problem detail
- [ ] Tablet (768px) → Balanced layout, collapsible sidebar
- [ ] Desktop (1440px) → Full sidebar, multi-column grids, splitter layout

### 5.6 AI Service Degradation

- [ ] Tat AI service → Dashboard: recommendations section empty/fallback
- [ ] Tat AI service → Knowledge Map: van render (data tu local DB)
- [ ] Tat AI service → Review Queue: empty state message
- [ ] Tat AI service → Submit code: van execute, adaptive update fail silently
- [ ] Tat AI service → Admin assign group: fallback to local upsert
- [ ] Tat AI service → Hints: error message hien thi

---

## 6. Known Limitations

| Van de | Muc do | Ghi chu |
|--------|--------|---------|
| Code execution can Docker daemon | Blocker cho full E2E | E2E test submit code bi skip neu Docker khong chay |
| AI service can chay cho adaptive | Medium | Recommendations/Knowledge State tra empty neu AI tat |
| Frontend unit tests chua co | Low | E2E da cover UI dang ke, backend unit da cover logic |
| Khong co load test | Low | 60 user thesis khong can load test |

---

## 7. Test trong CI/CD (tuong lai)

```yaml
# .github/workflows/test.yml (reference)
name: Tests
on: [push, pull_request]
jobs:
  backend-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd server && npm ci && npm test

  ai-service-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd ai-service && pip install -r requirements.txt && pytest

  e2e:
    runs-on: ubuntu-latest
    services:
      postgres: ...
      redis: ...
    steps:
      - uses: actions/checkout@v4
      - run: cd server && npm ci && npm run start:dev &
      - run: cd client && npm ci && npm run dev &
      - run: npx playwright install chromium
      - run: npx playwright test
```

---

## 8. Cau truc file test

```
server/src/
├── auth/
│   └── auth.service.spec.ts                    (5 tests)
├── problems/
│   ├── problems.service.spec.ts                (11 tests)
│   └── starter-code.util.spec.ts               (12 tests)
├── submissions/
│   ├── submissions.service.spec.ts             (7 tests)
│   ├── code-execution.service.spec.ts          (11 tests)
│   └── submission-pipeline.integration.spec.ts (5 tests)
├── concepts/
│   └── concepts.service.spec.ts                (existing)
├── adaptive/
│   └── adaptive.service.spec.ts                (existing)
├── users/
│   └── users.service.spec.ts                   (5 tests)
├── courses/
│   └── courses.service.spec.ts                 (5 tests)
├── skills/
│   └── skills.service.spec.ts                  (4 tests)
├── recommendations/
│   └── recommendations.service.spec.ts         (4 tests)
├── admin/
│   └── admin.service.spec.ts                   (10 tests)
├── instructor/
│   └── instructor.service.spec.ts              (7 tests)
├── ai/
│   └── ai.service.spec.ts                      (13 tests)
└── common/
    ├── guards/
    │   └── roles.guard.spec.ts                 (5 tests)
    ├── filters/
    │   └── http-exception.filter.spec.ts       (4 tests)
    └── middleware/
        └── logging.middleware.spec.ts           (6 tests)

e2e/
├── helpers.ts                                  (shared utilities)
├── auth.spec.ts                                (9 tests)
├── student-flow.spec.ts                        (16 tests)
├── instructor-flow.spec.ts                     (10 tests)
├── admin-flow.spec.ts                          (12 tests)
├── security.spec.ts                            (6 tests)
├── error-handling.spec.ts                      (3 tests)
├── performance.spec.ts                         (4 tests)
└── functional.spec.ts                          (11 tests, can Docker)

ai-service/tests/
├── test_bkt.py
├── test_elo.py
├── test_mab.py
├── test_fsrs.py
└── test_integration.py
```

---

*In document nay kem theo khi bao ve. Chay Smoke Test (muc 5.1) truoc buoi bao ve 30 phut.*
