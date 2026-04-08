# QA & Test Plan — AdaptLearn Platform

> Ke hoach kiem thu toan dien cho he thong AdaptLearn.
> Bao gom: ma tran test, E2E test voi Playwright, unit test, va huong dan chay.

---

## 1. Tong quan test coverage

### 1.1 Ma tran kiem thu theo tang

| Tang | Framework | So luong test | Coverage |
|------|-----------|---------------|----------|
| **Backend Unit** | Jest + @nestjs/testing | 36 test cases / 5 suites | Auth, Problems, Submissions, Concepts, Adaptive |
| **AI Service Unit** | Pytest | 5 modules (BKT, Elo, MAB, FSRS, Integration) | Tat ca thuat toan adaptive |
| **Frontend E2E** | Playwright | 30+ test cases / 4 suites | Auth, Student flow, Instructor, Admin |
| **Frontend Unit** | (chua implement) | — | — |

### 1.2 Ma tran kiem thu theo feature

| Feature | Unit Test | E2E Test | Manual QA |
|---------|-----------|----------|-----------|
| Dang nhap / Dang ky | ✅ auth.service.spec | ✅ auth.spec.ts | |
| Danh sach bai tap | ✅ problems.service.spec | ✅ student-flow.spec | |
| Loc/Tim kiem bai tap | | ✅ student-flow.spec | |
| Giai bai (code editor) | ✅ submissions.service.spec | ✅ student-flow.spec | Can test Docker |
| Knowledge Map | | ✅ student-flow.spec | |
| Review Queue (FSRS) | | ✅ student-flow.spec | |
| Profile & Skills | | ✅ student-flow.spec | |
| Instructor Dashboard | | ✅ instructor-flow.spec | |
| Quan ly bai tap (CRUD) | ✅ problems.service.spec | ✅ instructor-flow.spec | |
| Admin Dashboard | | ✅ admin-flow.spec | |
| Quan ly user/groups | | ✅ admin-flow.spec | |
| RBAC (phan quyen) | | ✅ admin-flow.spec | |
| SUS Survey | | ✅ student-flow.spec | |
| Adaptive Recommendations | ✅ adaptive.service.spec | | Can AI service |
| BKT Knowledge Tracing | ✅ test_bkt.py | | |
| Elo Rating | ✅ test_elo.py | | |
| MAB Selection | ✅ test_mab.py | | |
| FSRS Scheduling | ✅ test_fsrs.py | | |
| Full Adaptive Pipeline | ✅ test_integration.py | | |
| Swagger API Docs | | | Manual: GET /api/docs |
| Error Boundary | | | Tat AI service → reload page |

---

## 2. E2E Test Suites (Playwright)

### 2.1 auth.spec.ts — Authentication (6 tests)

| # | Test | Kiem tra |
|---|------|---------|
| 1 | Display login form | Form hien thi dung (email, password, button) |
| 2 | Switch to register tab | Tab register hien thi them truong name |
| 3 | Validation errors on empty submit | 2 error messages hien thi |
| 4 | Login with valid credentials | Dang nhap thanh cong → redirect / |
| 5 | Error on invalid credentials | Hien thi thong bao loi |
| 6 | Redirect unauthenticated to login | Truy cap /problems → redirect /login |

### 2.2 student-flow.spec.ts — Student Core Flow (12 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Dashboard | Stats cards render | "Problems Solved", "Total Submissions" hien thi |
| 2 | Dashboard | Onboarding modal | Modal welcome hien thi cho user moi |
| 3 | Problems | Problem list renders | Table co data, rows hien thi |
| 4 | Problems | Filter by difficulty | Loc EASY → chi con tag EASY |
| 5 | Problems | Search by title | Tim "Sum" → chi hien 1 row |
| 6 | Problem Solving | Code editor visible | CodeMirror `.cm-editor` render |
| 7 | Problem Solving | Submit button present | Button "Submit" hien thi |
| 8 | Knowledge Map | Graph renders | ReactFlow `.react-flow` hien thi |
| 9 | Review Queue | Page loads | Chuyen trang thanh cong |
| 10 | Profile | User info correct | Ten, email, role hien thi dung |
| 11 | Survey | 10 questions displayed | 10 card hien thi |
| 12 | Survey | Submit disabled until complete | Button disabled khi chua tra loi het |

### 2.3 instructor-flow.spec.ts — Instructor Flow (7 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Dashboard | Instructor menu visible | Menu "Instructor", "Manage Problems" hien thi |
| 2 | Dashboard | Navigate to instructor page | URL /instructor, title hien thi |
| 3 | Dashboard | Course selector and stats | Select va "Enrolled Students" hien thi |
| 4 | Problem Mgmt | Navigate to management page | URL /instructor/problems |
| 5 | Problem Mgmt | Table with actions | Edit, Delete buttons hien thi |
| 6 | Problem Mgmt | Create modal opens | Modal "Create Problem" voi form fields |
| 7 | Problem Mgmt | Edit modal pre-fills data | Modal "Edit Problem", title khong rong |

### 2.4 admin-flow.spec.ts — Admin Flow + RBAC (9 tests)

| # | Test Group | Test | Kiem tra |
|---|------------|------|---------|
| 1 | Admin | Admin menu visible | Menu "Admin" hien thi |
| 2 | Admin | Navigate to admin page | URL /admin, title |
| 3 | Admin | Platform stats | 5 stat cards hien thi |
| 4 | Admin | User management table | Table voi seed users |
| 5 | Admin | Search users | Tim "Alice" → chi hien Alice |
| 6 | Admin | Experiment overview | Card hien thi |
| 7 | Admin | Group assignment controls | Select dropdown hien thi |
| 8 | RBAC | Student KHONG thay admin/instructor menu | Kiem tra phan quyen |
| 9 | RBAC | Instructor thay instructor, KHONG thay admin | Kiem tra phan quyen |

---

## 3. Huong dan chay test

### 3.1 Prerequisites

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

### 3.2 Chay E2E tests

```bash
# Chay tat ca (headless)
npm run test:e2e

# Chay voi Playwright UI (interactive)
npm run test:e2e:ui

# Chay voi browser hien thi (debug)
npm run test:e2e:headed

# Chay 1 file cu the
npx playwright test e2e/auth.spec.ts

# Chay 1 test cu the
npx playwright test -g "should login with valid credentials"
```

### 3.3 Chay Backend Unit Tests

```bash
cd server
npm test            # chay test
npm run test:cov    # chay test voi coverage report
```

### 3.4 Chay AI Service Tests

```bash
cd ai-service
python -m pytest tests/ -v              # verbose output
python -m pytest tests/test_bkt.py -v   # chi chay BKT tests
```

### 3.5 Xem test report

Sau khi chay Playwright:
```bash
npx playwright show-report
```
→ Mo browser hien thi report HTML voi screenshots, traces, timing.

---

## 4. Manual QA Checklist

### 4.1 Smoke Test (truoc moi lan demo)

- [ ] Truy cap http://localhost:5173 → trang Login hien thi
- [ ] Dang nhap `student1@example.com` / `password123` → Dashboard hien thi
- [ ] Navigate Problems → danh sach bai tap hien thi (30+ bai)
- [ ] Click 1 bai → Code editor hien thi
- [ ] Navigate Knowledge Map → graph render voi nodes
- [ ] Navigate Review Queue → trang hien thi
- [ ] Navigate Profile → thong tin dung
- [ ] Dang nhap `instructor@example.com` → thay Instructor menu
- [ ] Navigate Instructor Dashboard → stats hien thi
- [ ] Navigate Manage Problems → table voi Edit/Delete
- [ ] Dang nhap `admin@example.com` → thay Admin menu
- [ ] Navigate Admin Dashboard → 5 stat cards + user table
- [ ] Swagger: http://localhost:3000/api/docs → API docs hien thi

### 4.2 Functional Test (khi co Docker)

- [ ] Submit code dung → status ACCEPTED, hien thi "All test cases passed"
- [ ] Submit code sai → status WRONG_ANSWER, hien thi expected vs got
- [ ] Submit vong lap vo han → status TIME_LIMIT sau 5s
- [ ] Submit syntax error → status RUNTIME_ERROR voi error message
- [ ] Sau ACCEPTED → Knowledge Map cap nhat mastery (reload trang)
- [ ] Instructor tao bai moi → hien thi trong danh sach
- [ ] Instructor sua bai → thong tin cap nhat
- [ ] Instructor xoa bai → bien mat khoi danh sach
- [ ] Admin assign experiment group → tag hien thi

### 4.3 Edge Case Test

- [ ] Dang nhap sai 5 lan → rate limiter block (429 status)
- [ ] Tat AI service → Dashboard van hien thi (graceful degradation)
- [ ] Tat AI service → Submit code van hoat dong (chi adaptive update fail silently)
- [ ] Reload trang bat ky → khong bi white screen (Error Boundary)
- [ ] Mo 2 tab → dang nhap 1 tab, tab kia tu cap nhat
- [ ] Mobile (375px width) → layout khong bi vo

---

## 5. Known Limitations

| Van de | Muc do | Ghi chu |
|--------|--------|---------|
| Code execution can Docker daemon | Blocker cho full E2E | E2E test submit code bi skip neu Docker khong chay |
| AI service can chay cho adaptive tests | Medium | Recommendations/Knowledge State tra empty neu AI service tat |
| Frontend unit tests chua co | Low | E2E da cover UI, backend unit da cover logic |
| Khong co load test | Low | 60 user thesis khong can load test |

---

## 6. Test trong CI/CD (tuong lai)

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

*In document nay kem theo khi bao ve. Chay Smoke Test (muc 4.1) truoc buoi bao ve 30 phut.*
