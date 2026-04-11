# Architecture & Design Decisions — AdaptLearn Platform

> Document phuc vu bao ve khoa luan: Giai thich cac quyet dinh thiet ke, design pattern, lua chon cong nghe
> trong toan bo he thong.

---

## 1. Tong quan kien truc he thong

### 1.1 Kien truc tong the: Microservice-Lite (3-Service Monorepo)

```
                    ┌──────────────┐
                    │   Browser    │
                    └──────┬───────┘
                           │ HTTP
                    ┌──────▼───────┐
                    │   React SPA  │  ← Port 5173 (dev) / Static build (prod)
                    │  (client/)   │
                    └──────┬───────┘
                           │ REST API /api/*
                    ┌──────▼───────┐
                    │   NestJS     │  ← Port 3000
                    │  (server/)   │  API Gateway + Business Logic
                    └──────┬───────┘
                           │ Internal HTTP (X-Service-Key)
                    ┌──────▼───────┐
                    │   FastAPI    │  ← Port 8000
                    │(ai-service/) │  Adaptive Learning Engine
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼───┐ ┌─────▼─────┐
        │PostgreSQL  │ │ Redis │ │  Docker   │
        │ + pgVector │ │ Cache │ │  Sandbox  │
        └───────────┘ └───────┘ └───────────┘
```

**Tai sao 3 service thay vi monolith?**

| Tieu chi | Monolith | 3-Service |
|----------|----------|-----------|
| AI algorithms (Python) + API (TypeScript) | Khong the chung runtime | Moi service dung ngon ngu toi uu |
| Scale doc lap | Khong | FastAPI co the scale rieng khi nhieu user |
| Failure isolation | 1 loi crash toan bo | AI service loi → NestJS van phuc vu static content |
| Development | 1 team lam tat ca | Frontend/Backend/AI phat trien song song |
| Deployment | Toan bo hoac khong | Deploy tung service doc lap |

**Tai sao khong dung full microservice (Kubernetes, message queue)?**

Day la du an khoa luan cua 1 sinh vien, khong phai production enterprise. 3 service la muc "vua du":
- Du tach biet de demo kien truc tot
- Khong qua phuc tap de 1 nguoi quan ly
- Docker Compose du de orchestrate (khong can Kubernetes)
- HTTP synchronous du nhanh cho 50-60 user thi nghiem

---

## 2. Design Patterns su dung

### 2.1 Backend (NestJS)

#### **a) Modular Architecture (NestJS Modules)**
- **Pattern**: Moi feature la 1 module doc lap (auth, problems, submissions, adaptive, admin, instructor)
- **File**: `server/src/app.module.ts` — import 14 modules
- **Tai sao**: NestJS khong ep buoc module, nhung module giup:
  - Encapsulate controller + service + provider trong 1 don vi
  - Dependency Injection chi hoat dong trong scope module (tranh circular dependency)
  - De test: mock toan bo module khi test

#### **b) Dependency Injection (Constructor Injection)**
- **Pattern**: Tat ca service duoc inject qua constructor, quan ly boi NestJS IoC Container
- **Vi du**: `SubmissionsService` inject `PrismaService`, `CodeExecutionService`, `AdaptiveService`
- **Tai sao**:
  - **Testability**: Mock dependency de viet unit test (36 test cases hien tai)
  - **Loose coupling**: Service khong biet implementation cu the cua dependency
  - **Lifecycle management**: NestJS tu dong tao va huy instance

#### **c) Service Layer Pattern**
- **Pattern**: Controller chi xu ly HTTP (routing, validation) → delegate sang Service xu ly business logic
- **Vi du**: `ProblemsController.create()` → goi `ProblemsService.create()` → goi `PrismaService` + `AiService`
- **Tai sao**:
  - Controller khong chua logic → de doc, de test
  - Service co the tai su dung tu nhieu controller
  - Tuan theo Single Responsibility Principle (SRP)

#### **d) Guard Pattern (RBAC Authorization)**
- **Files**: `common/guards/roles.guard.ts`, `common/decorators/roles.decorator.ts`
- **Cach hoat dong**:
  1. `@Roles(Role.INSTRUCTOR, Role.ADMIN)` — set metadata tren endpoint
  2. `RolesGuard` — doc metadata qua `Reflector`, so sanh voi `user.role` tu JWT
  3. Tra ve `true` (cho phep) hoac throw `ForbiddenException`
- **Tai sao Guard thay vi middleware**:
  - Guard co access vao NestJS execution context (biet role nao can)
  - Middleware khong co metadata reflection
  - Tuan theo Decorator Pattern — khai bao role ngay tren endpoint

#### **e) DTO + Validation Pipe Pattern**
- **Files**: `*/dto/*.ts` — moi DTO dung `class-validator` decorators
- **Applied**: Global `ValidationPipe` trong `main.ts`
- **Cach hoat dong**: Request body → `class-transformer` tao instance → `class-validator` validate → reject hoac pass
- **Tai sao**:
  - **Whitelist mode**: Tu dong strip cac field khong khai bao (chong injection)
  - **Type safety**: DTO la TypeScript class, IDE auto-complete
  - **Swagger integration**: `@ApiProperty` tren DTO → tu dong generate API docs

#### **f) Proxy/Client Pattern (AI Service Communication)**
- **File**: `server/src/ai/ai.service.ts`
- **Cach hoat dong**:
  - Private `request<T>(method, path, body)` — xu ly HTTP, headers, error
  - Public methods (`updateAdaptiveLayers()`, `generateHint()`, ...) — typed interface
  - Tu dong convert camelCase (TypeScript) ↔ snake_case (Python)
- **Tai sao**:
  - **Single point of change**: Doi AI service URL → chi sua 1 cho
  - **Type safety**: Caller khong can biet HTTP detail
  - **Error isolation**: Try/catch trong moi method, tra ve fallback khi AI service down

#### **g) Fire-and-Forget Pattern (Async Execution)**
- **File**: `submissions/submissions.service.ts`
- **Flow**:
  ```
  1. Create submission (status: PENDING) → return to client
  2. Background: Execute code in Docker sandbox
  3. Background: Update submission status (ACCEPTED/WRONG_ANSWER/...)
  4. Background: Trigger adaptive layer updates
  ```
- **Tai sao**: Execution trong Docker mat 1-5 giay. Neu block → UX xau. Fire-and-forget + frontend polling la pattern chuan cho judge system.

#### **h) Docker Sandbox Pattern (Code Execution)**
- **File**: `submissions/code-execution.service.ts`
- **Resource limits**:
  - Memory: 256MB (`--memory=256m`)
  - CPU: 0.5 cores (`--cpus=0.5`)
  - Network: Disabled (`--network=none`)
  - Timeout: 5 giay
  - Code encoded base64 (chong shell injection)
- **Tai sao Docker thay vi chay truc tiep**: 
  - **Bao mat**: User code co the chay `os.system("rm -rf /")` → Docker cach ly hoan toan
  - **Resource control**: Khong the dung het RAM/CPU cua server
  - **Reproducibility**: Moi submission chay trong moi truong giong nhau

---

### 2.2 Frontend (React)

#### **a) Component Hierarchy: Pages → Layouts → Components**
- **Pages** (`pages/`): Route-level components (Dashboard, Problems, ProblemDetail, ...)
- **Layouts** (`layouts/`): Shared wrappers (DashboardLayout voi sidebar, AuthLayout)
- **Components** (`components/`): Reusable UI (ErrorBoundary, HintPanel, OnboardingModal)
- **Tai sao**:
  - Page = 1 URL = 1 component → de navigate va debug
  - Layout = shared chrome (sidebar, header) → DRY
  - Component = tai su dung across pages

#### **b) Server State Management: TanStack React Query**
- **Tai sao React Query thay vi Redux/Zustand?**

| Tieu chi | Redux | React Query |
|----------|-------|-------------|
| Server state (API data) | Manual fetch + store | Tu dong cache + refetch |
| Loading/Error states | Manual tracking | Built-in `isLoading`, `isError` |
| Cache invalidation | Manual dispatch | `invalidateQueries()` tu dong |
| Boilerplate | Action + Reducer + Selector | 1 hook |
| Realtime sync | Khong co | `refetchInterval`, `staleTime` |

- **Cach dung**: Moi domain co 1 file query hooks: `useAuth.ts`, `useProblems.ts`, `useAdaptive.ts`, ...
- **Mutation pattern**: `useMutation()` + `onSuccess: invalidateQueries()` de cap nhat cache sau write

#### **c) API Layer: Axios Instance + Interceptors**
- **File**: `api/axios.ts`
- **Request interceptor**: Tu dong gan `Authorization: Bearer <token>` tu localStorage
- **Response interceptor**: 401 → xoa token → redirect `/login`
- **Tai sao Axios thay vi fetch**: Interceptors, automatic JSON, cancel tokens, retry lib

#### **d) Route Guards (Conditional Rendering)**
- **File**: `routes/index.tsx`
- **Cach hoat dong**: `useMe()` query check auth → `isAuthenticated ? <DashboardLayout /> : <Navigate to="/login" />`
- **Tai sao**: Khong can extra library (react-router v6 du manh). Server-side guard (JWT) la tuyen phong thu chinh, client-side chi la UX.

#### **e) Code Splitting (React.lazy)**
- **Cach hoat dong**: `const KnowledgeMap = lazy(() => import('../pages/KnowledgeMap'))`
- **Ket qua**: Build tao 10+ chunk files thay vi 1 bundle lon
- **Tai sao**: KnowledgeMap (~232KB) va ProblemDetail (~497KB) chi load khi user navigate toi → First Load nhanh hon

#### **f) Error Boundary Pattern**
- **File**: `components/ErrorBoundary.tsx`
- **Tai sao**: React 18 khong co built-in error handling cho async errors. ErrorBoundary catch render errors → hien thi fallback UI thay vi white screen.

---

### 2.3 AI Service (FastAPI/Python)

#### **a) Orchestrator/Mediator Pattern (AdaptiveEngine)**
- **File**: `ai-service/app/services/adaptive_engine.py`
- **Vai tro**: Diem duy nhat dieu phoi 4 layer (BKT, Elo, MAB, FSRS)
- **Cach hoat dong**:
  ```python
  class AdaptiveEngine:
      def __init__(self):
          self.bkt = BKTService()
          self.elo = EloService()
          self.mab = MABService()
          self.fsrs = FSRSService()
      
      async def process_submission(self, session, data):
          # Layer 1 → Layer 2 → Layer 3 → Layer 4 (sequential)
          bkt_result = await self.bkt.update(session, ...) if settings.enable_bkt else {}
          elo_result = await self.elo.update(session, ...) if settings.enable_elo else {}
          # ... MAB, FSRS tuong tu
  ```
- **Tai sao Orchestrator**:
  - 4 layer phu thuoc lan nhau (MAB can BKT mastery, Elo can problem rating)
  - Orchestrator dam bao thu tu dung
  - Feature flags de tat/bat tung layer (phuc vu A/B testing)
  - 1 layer loi → cac layer khac van chay (graceful degradation)

#### **b) Strategy Pattern (Algorithm Services)**
- Moi layer la 1 service doc lap voi interface nhat quan:
  - `update(session, student_id, ...)` — cap nhat sau submission
  - `get_state(session, student_id)` — lay trang thai hien tai
  - `predict(session, student_id, ...)` — du doan ket qua
- **Tai sao**: Moi algorithm co the thay the ma khong anh huong layer khac. Vi du: doi BKT sang Deep Knowledge Tracing chi can thay `BKTService`.

#### **c) Factory Pattern (State Management)**
- Moi service co `get_or_create_state()` / `get_or_create_rating()` / `get_or_create_card()`
- **Tai sao**: Student moi chua co state → tu dong tao voi default params thay vi throw error

#### **d) Multi-TTL Caching Strategy (Redis)**
- **File**: `ai-service/app/services/cache_service.py`
- **TTL khac nhau theo data volatility**:
  - Knowledge state: 5 phut (thay doi moi submission)
  - Recommendations: 2 phut (phu thuoc vao BKT + Elo + MAB)
  - Knowledge graph: 1 gio (prerequisite it thay doi)
- **Tai sao Redis thay vi in-memory cache**: Multi-process share cache; persist qua restart

#### **e) Feature Flag Pattern**
- **File**: `ai-service/app/config.py` — Pydantic BaseSettings
- **Tai sao**: 
  - **A/B testing**: Control group tat het 4 layer → chi content-based recommendation
  - **Gradual rollout**: Bat tung layer mot khi validate
  - **Debugging**: Tat 1 layer de isolate loi

#### **f) RAG Pattern (LLM Hint Generation)**
- **File**: `ai-service/app/services/llm_service.py`
- **Retrieval**: Lay context tu knowledge graph (concepts, prerequisites, mastery)
- **Augmentation**: Ghep context + student code + error message vao prompt
- **Generation**: GPT-4o-mini sinh hint theo Socratic method
- **Tai sao RAG thay vi goi LLM truc tiep**: LLM khong biet knowledge graph cua he thong. RAG cung cap context → hint chinh xac hon, lien quan den concept dang hoc.

---

## 3. Lua chon cong nghe va ly do

### 3.1 Frontend: React 18 + TypeScript + Ant Design + Vite

| Cong nghe | Tai sao chon | Thay the da xem xet |
|-----------|-------------|---------------------|
| **React 18** | Ecosystem lon nhat, hiring pool rong, hooks pattern manh | Vue 3, Svelte |
| **TypeScript** | Type safety ngay compilation, IDE support tot, bat loi som | JavaScript (qua nhieu runtime error) |
| **Ant Design 5** | Component library day du cho enterprise app (Table, Form, Chart), co san theme system | Material UI (it component), Chakra UI (thieu table phuc tap) |
| **Vite** | Build nhanh hon Webpack 10-20x (HMR < 100ms), zero config | Webpack (cham), CRA (deprecated) |
| **React Query** | Server state management tot nhat, tu dong cache/refetch | Redux (qua nhieu boilerplate cho server state) |
| **ReactFlow** | Graph visualization library tot nhat cho React, support dagre layout | D3.js (qua low-level), vis.js (khong React-native) |
| **CodeMirror** | Code editor tieu chuan (VS Code dung), ho tro Python syntax | Monaco (nang hon, 1MB+) |

### 3.2 Backend: NestJS 10 + Prisma ORM + JWT

| Cong nghe | Tai sao chon | Thay the da xem xet |
|-----------|-------------|---------------------|
| **NestJS 10** | TypeScript-native, dependency injection, modular, Swagger tich hop | Express (thieu structure), Fastify (thieu DI ecosystem) |
| **Prisma 5** | Type-safe query, auto-generate types tu schema, migration system | TypeORM (typing kem hon), Sequelize (JavaScript era) |
| **Passport + JWT** | Chuan industry cho API auth, stateless (khong can session storage) | Session-based (can Redis session store, phuc tap hon) |
| **Docker (sandbox)** | Isolation hoan toan cho user code, resource limits, network disable | VM (qua nang), subprocess (khong an toan) |

### 3.3 AI Service: FastAPI + SQLAlchemy + sentence-transformers

| Cong nghe | Tai sao chon | Thay the da xem xet |
|-----------|-------------|---------------------|
| **FastAPI** | Async Python tot nhat, auto OpenAPI docs, Pydantic validation | Flask (sync, cham hon), Django REST (qua nang) |
| **Python** | Thu vien ML/AI phong phu (numpy, scipy, torch), algorithm de implement | Node.js (thieu ML ecosystem) |
| **SQLAlchemy 2.0** | Async support, mature ORM, flexible query builder | Raw SQL (kho maintain), Tortoise ORM (it ecosystem) |
| **sentence-transformers** | Pre-trained embedding model, 384-dim output, chay local (khong can API) | OpenAI embeddings (ton tien, phu thuoc API) |
| **Redis 7** | In-memory cache nhanh nhat, TTL support, pub/sub | Memcached (it feature hon) |
| **pgVector** | PostgreSQL extension cho vector similarity search, khong can separate vector DB | Pinecone (ton tien), Milvus (phuc tap deploy) |

### 3.4 Database: PostgreSQL 16

**Tai sao PostgreSQL thay vi MySQL/MongoDB?**
- **pgVector extension**: Vector similarity search cho embeddings — khong can them 1 database rieng
- **JSON/JSONB columns**: Luu rating_history, event data — linh hoat nhu NoSQL
- **Advanced indexing**: GiST index cho vector, B-tree cho filter, GIN cho JSON
- **ACID compliance**: Adaptive state can consistency (BKT + Elo + MAB + FSRS update cung 1 transaction)
- **Mature ecosystem**: Prisma + SQLAlchemy deu ho tro tot nhat

---

## 4. Cau truc database va indexing strategy

### 4.1 Entity Relationship

```
User (1) ──────── (N) Submission
  │                        │
  │ (N)               (1)  │
  ├── Enrollment ────── Course ──── (N) Problem
  │                                      │
  │ (N)                             (N)  │
  ├── KnowledgeState ──────── Concept ───┘ (via ProblemConcept)
  ├── EloRating                  │
  ├── MabState              KnowledgeGraphEdge
  ├── FsrsCard
  ├── EventLog
  └── ExperimentGroup
```

### 4.2 Indexing Strategy

| Table | Index | Tai sao |
|-------|-------|---------|
| `submissions` | `(userId, problemId)` | Tim submission cua user cho 1 problem (kiem tra da solve chua) |
| `submissions` | `(problemId, status)` | Tinh acceptance rate cho instructor dashboard |
| `submissions` | `(userId, createdAt)` | Recent submissions, dashboard stats |
| `knowledge_states` | `(studentId, pMastery)` | Sort concepts theo mastery level |
| `elo_ratings` | `(entityId, entityType)` | Tim rating cua student hoac problem |
| `fsrs_cards` | `(studentId, dueDate)` | Review queue: tim cards sap den han |
| `event_logs` | `(userId, event)` | Filter events theo user va loai |
| `event_logs` | `(createdAt)` | Export events theo thoi gian |
| `problems` | `(courseId)` | Filter problems theo course |

---

## 5. Cross-cutting concerns

### 5.1 Authentication & Authorization Flow

```
Client                    NestJS                     Database
  │                         │                           │
  │ POST /auth/login        │                           │
  │ {email, password} ──────►│                           │
  │                         │ bcrypt.compare() ─────────►│
  │                         │◄──────── User record ──────│
  │                         │ jwt.sign({sub, role})      │
  │◄─── {token} ────────────│                           │
  │                         │                           │
  │ GET /problems           │                           │
  │ Authorization: Bearer ──►│                           │
  │                         │ JwtStrategy.validate()     │
  │                         │ RolesGuard.canActivate()   │
  │                         │ → check @Roles metadata    │
  │◄─── data ───────────────│                           │
```

### 5.2 Error Handling Strategy

| Layer | Strategy | Vi du |
|-------|----------|-------|
| Frontend | ErrorBoundary + React Query retry | Component crash → fallback UI, API fail → retry 1 lan |
| NestJS Controller | HttpException | NotFoundException, ConflictException |
| NestJS → AI Service | Try/catch + fallback response | AI service down → return `{recommendations: []}` |
| AI Service layers | Graceful degradation | BKT fail → van chay Elo, MAB, FSRS |
| AI Service → Redis | Silent fallback | Redis down → query truc tiep DB |
| AI Service → LLM | Rate limit + timeout + fallback | OpenAI fail → return `{hint: null}` |

### 5.3 Rate Limiting

- **Global**: 100 requests/60 giay (ThrottlerModule)
- **LLM hints**: 30 requests/60 giay/user (sliding window trong Python)
- **Tai sao**: Chong abuse, bao ve AI service va OpenAI API quota

---

## 6. Cau hoi thuong gap tu hoi dong va cau tra loi

### Q: "Tai sao lai tach AI service thanh Python rieng thay vi viet chung voi NestJS?"
**A**: Cac thuat toan BKT, Elo, MAB, FSRS su dung numpy, scipy va math-intensive computation. Python co ecosystem ML/AI tot nhat. NestJS tot cho API gateway nhung khong phai ngon ngu toi uu cho tinh toan so hoc. Tach thanh 2 service con cho phep scale doc lap — khi nhieu user, AI service co the scale horizontal ma khong anh huong API.

### Q: "Tai sao dung PostgreSQL ma khong dung MongoDB?"
**A**: He thong can ca relational data (User → Enrollment → Course) va vector similarity search (problem embeddings). PostgreSQL voi pgVector extension dap ung ca 2 yeu cau trong 1 database duy nhat, giam complexity. Ngoai ra, adaptive state (BKT, Elo) can ACID consistency — NoSQL khong dam bao dieu nay.

### Q: "He thong xu ly bao nhieu user dong thoi?"
**A**: Thiet ke cho 50-60 user thi nghiem. NestJS xu ly HTTP concurrently (event loop), FastAPI xu ly async (uvicorn workers). Redis cache giam tai DB. Docker sandbox co the chay nhieu container song song. Bottleneck chinh la Docker execution (5s/submission) — co the scale bang queue system (BullMQ) neu can.

### Q: "Lam sao dam bao code cua sinh vien khong pha he thong?"
**A**: Docker sandbox chay voi: network disabled (khong truy cap internet), memory limit 256MB, CPU limit 0.5 core, timeout 5 giay, code truyen qua base64 (chong shell injection). Container bi huy ngay sau khi chay xong.

### Q: "Tai sao dung Thompson Sampling cho MAB thay vi UCB?"
**A**: Thompson Sampling co Bayesian interpretation tu nhien — phu hop voi BKT (cung la Bayesian). UCB deterministic, khong co exploration randomness tot cho learning context. Thompson Sampling cung hoi tu nhanh hon trong thuc nghiem voi so luong arm lon (34 concepts × nhieu problems).

### Q: "Feature flags dung de lam gi?"
**A**: Phuc vu A/B testing trong thi nghiem. Nhom control tat het 4 layer → chi nhan recommendation dua tren content-based filtering. Nhom experimental bat 4 layer → nhan adaptive recommendation. So sanh 2 nhom tra loi 4 research questions cua khoa luan.

### Q: "Tai sao FSRS ma khong dung SM-2 (Anki algorithm)?"
**A**: FSRS-5 la thuat toan the he moi hon SM-2, su dung power-law decay thay vi exponential, co 19 learned parameters tu data thuc te cua 10,000+ nguoi dung Anki. FSRS chuan hon trong viec du doan kha nang nho (retrievability). Day la ung dung dau tien cua FSRS cho programming skill retention.

### Q: "Tai sao Ant Design ma khong dung Material UI?"
**A**: Ant Design co component Table va Form phuc tap hon Material UI — phu hop cho dashboard data-heavy cua he thong nay. Ant Design cung co san TreeSelect, Steps, Progress, Statistic — cac component can thiet cho knowledge graph visualization va adaptive dashboard ma khong can viet tu dau.

### Q: "He thong co scale duoc khong? Docker execution co la bottleneck?"
**A**: Phan tich cu the:

**Hien tai (du cho thesis)**:
- 40-60 user thi nghiem → toi da 5-10 submission dong thoi
- Moi submission: `docker run` voi 256MB RAM, 0.5 CPU, 5s timeout
- 10 container dong thoi = 2.5GB RAM, 5 CPU cores → server 8GB chay thoai mai
- Fire-and-forget pattern: user khong bi block, frontend polling status

**Tai sao khong la van de cho thesis evaluation**:
- NestJS async: `create()` return ngay voi PENDING, Docker chay background
- Frontend polling: `refetchInterval: 1000ms` cho den khi terminal status
- Concurrent Docker containers chay song song tren host (khong sequential)

**Neu scale len 1000+ user** (ngoai scope thesis nhung da thiet ke san):
```
Hien tai:  API → fire-and-forget → docker run (truc tiep tren server)
Scale:     API → push to BullMQ/Redis Queue → return jobId
                        ↓
           Worker Pool (N workers, nhieu may) → docker run → update DB
```

**Kien truc da chuan bi san cho viec nay**:
1. `executeSubmission()` da tach rieng khoi `create()` → de chuyen thanh queue consumer
2. Status da la state machine (PENDING → RUNNING → ACCEPTED) → frontend khong can thay doi
3. Chi can them BullMQ adapter, khong can rewrite business logic

**Con so cu the**:
| Scale | Concurrent | RAM can | CPU can | Kha thi? |
|-------|-----------|---------|---------|----------|
| 50 user (thesis) | 5-10 | 2.5 GB | 5 cores | ✅ Server don |
| 200 user | 20-30 | 7.5 GB | 15 cores | ✅ Server 16GB |
| 1000 user | 100+ | 25 GB | 50 cores | ❌ Can queue + worker pool |

**Tom lai**: Bottleneck la thuc, nhung chi xuat hien o scale > 200 concurrent users. Cho thesis evaluation (50-60 user, khong submit cung luc), kien truc hien tai hoan toan du. Khi can scale, chi can them message queue layer ma khong can thay doi code execution logic.

---

## 7. So sanh voi cac he thong tuong tu

| Tieu chi | LeetCode | HackerRank | AdaptLearn |
|----------|----------|------------|------------|
| Difficulty | Static label | Static label | Dynamic Elo rating |
| Problem selection | User chon | User chon | AI recommend (MAB) |
| Knowledge tracking | Khong co | Basic topic tracking | BKT per-concept mastery |
| Spaced repetition | Khong co | Khong co | FSRS scheduling |
| Personalized hints | Khong co | Editorial (static) | LLM Socratic hints (dynamic) |
| Learning analytics | Basic stats | Basic stats | Instructor dashboard + A/B testing |

---

*Document nay nen duoc in ra va mang theo khi bao ve. Moi phan tuong ung voi 1 cau hoi co the duoc hoi boi hoi dong.*
