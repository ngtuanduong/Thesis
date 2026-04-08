# Code Execution Architecture — Phan tich chuyen sau

> Document rieng ve kien truc thuc thi ma nguon (Online Judge Engine) trong he thong AdaptLearn.
> Bao gom: hien trang, so sanh voi cac he thong lon, phan tich bottleneck, va lo trinh nang cap.

---

## 1. Bai toan code execution trong Online Judge

Moi he thong Online Judge deu phai giai quyet **3 bai toan cot loi**:

| Bai toan | Yeu cau | Hau qua neu khong giai quyet |
|----------|---------|------------------------------|
| **Isolation** | Code cua user khong duoc truy cap he thong host | User chay `os.system("rm -rf /")` → mat toan bo data |
| **Resource Control** | Gioi han RAM, CPU, thoi gian cho moi submission | 1 vong lap vo han → server treo |
| **Scalability** | Xu ly nhieu submission dong thoi | Contest 1000 user → queue bao hoa, ket qua tra cham hang phut |

---

## 2. Kien truc hien tai cua AdaptLearn

### 2.1 Flow xu ly submission

```
┌─────────┐     ┌──────────────────┐     ┌──────────────────────┐
│ Browser  │────►│ NestJS API       │────►│ PostgreSQL           │
│ (React)  │     │ POST /submissions│     │ status = PENDING     │
└─────────┘     └────────┬─────────┘     └──────────────────────┘
                         │                          
                         │ fire-and-forget (khong await)
                         ▼                          
                ┌────────────────────┐              
                │ executeSubmission()│              
                │ (background)      │              
                └────────┬──────────┘              
                         │                          
                         ▼ update status = RUNNING  
                ┌────────────────────┐              
                │ CodeExecutionSvc   │              
                │ for each testCase: │              
                │   docker run ...   │──────┐      
                └────────────────────┘      │      
                                            ▼      
                                   ┌──────────────┐
                                   │Docker sandbox │
                                   │--memory=256m  │
                                   │--cpus=0.5     │
                                   │--network=none │
                                   │timeout 5s     │
                                   └──────┬───────┘
                                          │        
                                          ▼        
                                  update status =  
                                  ACCEPTED /       
                                  WRONG_ANSWER /   
                                  TIME_LIMIT /     
                                  RUNTIME_ERROR    
                                          │        
                                          ▼        
                              ┌───────────────────┐
                              │ Adaptive Layers   │
                              │ BKT + Elo + MAB   │
                              │ + FSRS update     │
                              └───────────────────┘
```

### 2.2 Chi tiet implementation

**File**: `server/src/submissions/code-execution.service.ts`

```typescript
// Moi test case = 1 docker container
for (const testCase of testCases) {
    const result = await this.runSingleTest(code, testCase);
    if (result.status !== ACCEPTED) return result;  // dung ngay khi sai
}
```

**Docker command cho moi test case**:
```bash
docker run --rm \
  --memory=256m \        # RAM limit
  --cpus=0.5 \           # CPU limit
  --network=none \       # Khong co mang
  code-sandbox:latest \
  sh -c "echo '<base64_code>' | base64 -d | timeout 5 python3"
```

**Bao mat hien tai**:
- ✅ Network isolation: `--network=none` → khong truy cap internet
- ✅ Memory limit: 256MB → khong OOM kill server
- ✅ CPU limit: 0.5 core → khong chiem het CPU
- ✅ Timeout: 5 giay → khong chay mai
- ✅ Base64 encoding: Chong shell injection
- ✅ `--rm`: Container tu dong xoa sau khi chay
- ⚠️ Shared kernel: Docker container dung chung kernel voi host

### 2.3 Diem manh cua thiet ke hien tai

1. **Fire-and-forget**: `create()` tra ve ngay voi PENDING, khong block user
2. **Status state machine**: PENDING → RUNNING → terminal (frontend polling)
3. **Sequential test execution**: Dung ngay khi sai → tiet kiem tai nguyen
4. **Don gian, de hieu**: 1 file, ~260 dong code, de debug

### 2.4 Diem yeu / Bottleneck

| Van de | Chi tiet | Anh huong |
|--------|----------|-----------|
| **1 container/test case** | 5 test cases = 5 `docker run` tuan tu | Overhead ~500ms-1s moi container startup |
| **Khong co queue** | Submission chay truc tiep tren NestJS process | 50 submission dong thoi = 50 Docker containers |
| **Khong co worker pool** | Khong gioi han so container dong thoi | 100 containers × 256MB = 25GB RAM |
| **Khong co container reuse** | Moi test case tao container moi | Lap lai overhead khoi tao |
| **Single server** | Khong phan tan worker ra nhieu may | Scale doc boi hardware |

---

## 3. Cac he thong lon giai quyet nhu the nao

### 3.1 Kien truc chung cua moi Online Judge lon

**TAT CA** cac he thong lon deu dung cung 1 pattern:

```
User → API Gateway → Message Queue → Worker Pool → Sandbox → Result Store → Notify User
                         ↑                ↑
                    Decouple           Scale rieng
                    ingestion          execution
                    khoi execution     theo tai
```

**Nguyen tac cot loi**: **Queue tach biet viec nhan submission khoi viec thuc thi**.
API server chi viet vao queue roi tra ve. Worker tu keo job va xu ly.
2 tang scale doc lap.

### 3.2 LeetCode

**Quy mo**: ~200,000 submissions / 2 gio contest, peak 5,000 submissions/phut dau

**Kien truc**:
```
React SPA → API Microservices → Kafka (message queue) → Worker Pool (Docker) → S3 (test cases) → PostgreSQL
                                     ↑                      ↑
                                Kafka partitioning     Pre-scale 100+ container
                                absorb burst           truoc contest 5 phut
```

**Ky thuat dac biet**:
- **Kafka**: Queue throughput hang tram nghin msg/s, partition cho parallel consumption
- **Two-phase testing**: Contest chi chay **10% test case** (pretest) → tra ket qua trong vai giay. **90% con lai** chay sau contest ket thuc (system testing). Hieu qua: **10x capacity** voi cung infrastructure.
- **Pre-scaling**: Biet truoc thoi gian contest → scale up 100+ worker container truoc 5 phut
- **Kafka partitioning**: Moi partition xu ly boi 1 consumer group → song song hoa tu nhien

**Latency**:
- Pretest: 2-5 giay
- Full system test: defer, vài phut den vài gio sau contest

### 3.3 Codeforces

**Quy mo**: 10,000+ user dong thoi, ~50 submissions/giay peak

**Kien truc**:
```
PHP Web App → Custom Queue → Dedicated Judge Servers (vat ly) → testlib.h checker
                                    ↑
                              Intel Core i3-8100 @ 3.60GHz
                              Process-level isolation
```

**Dac diem**:
- **Physical dedicated servers**: Khong dung cloud, khong dung Docker
- **Custom queue**: Khi judge machine ranh → lay submission dau tien tu queue
- **testlib.h**: Thu vien C++ chuan cho checker, validator, generator
- **Polygon**: Platform rieng cho tao de bai (polygon.codeforces.com)
- **Two-phase testing**: Giong LeetCode — pretest trong contest, system test sau contest
- **Status hien thi**: User thay "In Queue" khi dang cho, "System testing: d%" khi system test

**Scaling**: Vertical (may manh hon) + queue buffer cho burst. Mike Mirzayanov quan ly infrastructure thu cong.

### 3.4 Judge0 (Open-source, phổ biến nhất)

**Quy mo**: Open-source, duoc dung boi nhieu platform nho-vua

**Kien truc**:
```
REST API (Ruby on Rails) → PostgreSQL → Redis + Resque (queue) → Worker → Isolate sandbox
                                              ↑                      ↑
                                         Redis = cache + queue   Isolate = Linux namespaces
                                                                 + cgroups (nhe hon Docker)
```

**Dac diem**:
- **Isolate sandbox**: Khong dung Docker ma dung **Isolate** — tool chuyen dung cho untrusted code, dung Linux namespaces + cgroups truc tiep. Nhe hon Docker (~10ms startup vs ~50ms).
- **Redis + Resque**: Job queue tich hop voi Redis (vua lam cache vua lam queue)
- **60+ ngon ngu**: Tat ca compile/runtime cai san trong Docker image `judge0/compilers`
- **Modular**: Deploy tren nhieu may bang cach them worker

### 3.5 DMOJ (Don Mills Online Judge)

**Kien truc**:
```
Django Web App ←── Bridge Protocol ──→ Judge Server(s) → Sandbox
      ↑                                      ↑
  Co the nhieu Judge Server               multiprocessing.Pipe()
  connect vao 1 Web App                   cho IPC
```

**Dac diem**:
- **Bridge Protocol**: Judge server connect ve web app qua protocol rieng
- **Nhieu Judge server**: Scale bang cach them judge machine
- **Re-entrant grading**: Judge nhan submission moi truoc khi submission cu xong teardown

---

## 4. So sanh cong nghe Sandbox

| Cong nghe | Co che | Startup | Overhead | Bao mat | Dung boi |
|-----------|--------|---------|----------|---------|----------|
| **Docker** | Namespaces + cgroups (shared kernel) | ~50ms | ~0% | Trung binh (shared kernel) | AdaptLearn, nhieu platform |
| **Isolate** | Namespaces + cgroups (purpose-built) | ~10ms | ~0% | Cao | Judge0, IOI |
| **nsjail** | Namespaces + cgroups + seccomp-bpf | ~20ms | ~0% | Cao | Google kCTF |
| **gVisor** | User-space kernel, syscall interception | ~200ms | ~800ns/syscall | Rat cao | Google Cloud Run |
| **Firecracker** | KVM microVM (kernel rieng) | 125ms (28ms snapshot) | ~15% | Rat cao (hardware isolation) | AWS Lambda, Fargate |

**Tai sao AdaptLearn dung Docker**:
- Docker da quen thuoc trong ecosystem (Docker Compose cho toan bo he thong)
- Startup ~50ms la chap nhan duoc cho 5s timeout
- Muc bao mat du cho thesis evaluation (50-60 trusted university students)
- Production-grade system nen upgrade len **nsjail** hoac **Firecracker**

**Docker KHONG phai security boundary cho untrusted code o production**:
- Container dung chung kernel voi host → kernel exploit co the escape
- Giai phap: them seccomp profile, read-only rootfs, drop capabilities
- Ly tuong: Firecracker microVM (moi submission co kernel rieng)

---

## 5. So sanh cong nghe Message Queue

| Tieu chi | Kafka | RabbitMQ | Redis Streams | BullMQ (Redis) |
|----------|-------|----------|---------------|----------------|
| **Throughput** | 100K+ msg/s | ~50K msg/s | ~1M msg/s | ~50K msg/s |
| **Persistence** | Disk, long-term | Disk, short-term | In-memory | In-memory + persistence |
| **Scalability** | Rat cao (partition) | Trung binh | Trung binh | Trung binh |
| **Complexity** | Cao (Zookeeper/KRaft) | Trung binh | Thap | Thap |
| **Node.js support** | kafkajs | amqplib | ioredis | bullmq (native) |
| **Phu hop cho** | >10K user, contest | Medium platform | Nho, da co Redis | **NestJS (tich hop tot)** |

**Tai sao BullMQ la lua chon tot nhat cho AdaptLearn neu can scale**:
- AdaptLearn **da co Redis** trong stack (dung cho AI service cache)
- BullMQ co **@nestjs/bullmq** module — tich hop voi NestJS DI system
- Khong can them infrastructure moi (khong nhu Kafka can cluster rieng)
- Du manh cho 200-500 user (vai tram submission/phut)
- Chi khi vuot 10K user moi can chuyen sang Kafka

---

## 6. Lo trinh nang cap (Upgrade Roadmap)

### Level 0: Hien tai (du cho thesis — 50-60 user)

```
API → fire-and-forget → docker run truc tiep
```
- ✅ Don gian, de debug
- ✅ Du cho evaluation experiment
- ⚠️ Khong co gioi han concurrent containers

### Level 1: Them Concurrency Limiter (1-2 gio code)

```typescript
// Them vao CodeExecutionService
private semaphore = new Semaphore(10); // max 10 concurrent containers

async executeCode(code, language, testCases) {
    await this.semaphore.acquire();
    try {
        // ... existing Docker logic
    } finally {
        this.semaphore.release();
    }
}
```
- ✅ Chong RAM overflow (10 × 256MB = 2.5GB, an toan)
- ✅ Submission thu 11 tro di phai cho — nhung frontend da polling, user thay "Running..."
- ✅ Khong can them dependency

### Level 2: BullMQ Queue (1-2 ngay code)

```
API → BullMQ Queue (Redis) → Worker Process → Docker → DB update
         ↑                        ↑
    @nestjs/bullmq            concurrency: 10
    tich hop san              retry: 3 lan
```

**Thay doi cu the**:
1. Install `@nestjs/bullmq bullmq`
2. Tao `SubmissionProcessor` (BullMQ worker)
3. `SubmissionsService.create()` thay `this.executeSubmission()` bang `queue.add('execute', data)`
4. Worker pull job tu queue, goi `CodeExecutionService.executeCode()`
5. Config: `concurrency: 10`, `attempts: 3`, `backoff: exponential`

**Loi ich**:
- Queue buffer absorb burst (100 submission → xu ly 10 cai/luc)
- Retry tu dong khi Docker fail
- Monitoring: BullMQ dashboard (Bull Board)
- Da co Redis trong stack → khong can infrastructure moi

### Level 3: Distributed Workers (production-grade)

```
API → Kafka/BullMQ → Worker Machine 1 (10 containers)
                   → Worker Machine 2 (10 containers)
                   → Worker Machine 3 (10 containers)
                   → ...
```

- Worker chay tren may rieng, connect ve queue
- Auto-scale worker theo queue depth (Kubernetes HPA)
- Firecracker thay Docker cho strong isolation

### Level 4: LeetCode-grade (enterprise)

```
API → Kafka → Worker Pool (auto-scale) → Firecracker microVM
                                        → Pre-warm container pool
                                        → Two-phase testing
                                        → Geographic distribution
```

### So sanh cac level

| Level | User | Concurrent | Infrastructure | Code thay doi |
|-------|------|-----------|----------------|---------------|
| **0 (hien tai)** | 50-60 | 5-10 | 1 server | Khong |
| **1 (semaphore)** | 100 | 10 (gioi han) | 1 server | ~20 dong |
| **2 (BullMQ)** | 500 | 10/worker | 1 server + Redis | ~200 dong |
| **3 (distributed)** | 5,000 | 10/worker × N workers | N servers | Them config |
| **4 (enterprise)** | 100,000+ | Thousands | Kubernetes cluster | Rewrite |

---

## 7. Phan tich chi tiet: Tai sao hien tai du cho thesis?

### 7.1 Worst-case scenario cho thesis evaluation

**Gia dinh**: 60 sinh vien, 4 tuan thi nghiem, 3 bai/tuan

```
Tong submissions ≈ 60 × 3 × 4 × 5 (trung binh 5 lan submit/bai) = 3,600 submission
Tong submissions/tuan = 900
Tong submissions/ngay (5 ngay lam viec) = 180
Peak 1 gio (tat ca lam bai cung luc) = 60 submission
Peak 1 phut (burst) = 10 submission
```

**Resource consumption khi peak**:
- 10 container × 256MB = 2.5GB RAM → Server 8GB du thoai mai
- 10 container × 0.5 CPU = 5 cores → Server 4-core chap nhan duoc
- Moi container chay 1-5 giay → throughput ~2-10 submission/giay

**Ket luan**: Hien tai du. Khong can queue. Khong can scale.

### 7.2 Khi nao THAT SU can upgrade?

| Tinh huong | Can Level | Ly do |
|------------|-----------|-------|
| Thesis evaluation (60 user) | 0 | Peak 10 concurrent, 2.5GB RAM |
| Trien khai cho 1 lop (100 user) | 1 | Semaphore chong RAM spike |
| Nhieu lop cung dung (500 user) | 2 | Queue + retry + monitoring |
| Toan truong (5000 user) | 3 | Distributed workers |
| Platform cong khai (LeetCode-like) | 4 | Full rewrite |

---

## 8. Two-Phase Testing — Bai hoc tu LeetCode va Codeforces

**Concept**: Khong chay tat ca test case ngay luc submit.

```
Phase 1 (ngay luc submit): Chay 2-3 test case co ban → tra ket qua trong 2-3 giay
Phase 2 (background/sau deadline): Chay toan bo test case → cap nhat ket qua chinh thuc
```

**Loi ich**:
- 5 test case → chi chay 1 → **5x capacity** voi cung infrastructure
- User nhan feedback nhanh hon (2s thay vi 10s)
- Server xu ly nhieu submission hon

**AdaptLearn chua can**: Vi moi problem chi co 5-7 test case, va chi co 60 user.
Nhung neu scale, day la optimization dau tien nen lam.

---

## 9. Bao mat: Defense-in-Depth cho Code Execution

### 9.1 Hien tai (AdaptLearn)

```
Layer 1: Docker container isolation (namespace, cgroup)
Layer 2: --network=none (khong co mang)
Layer 3: --memory=256m, --cpus=0.5 (resource limit)
Layer 4: timeout 5s (thoi gian gioi han)
Layer 5: base64 encoding (chong shell injection)
Layer 6: --rm (tu dong xoa container)
```

### 9.2 Best practice cua industry (them vao neu can)

```
Layer 7: seccomp-bpf profile (chan syscall nguy hiem nhu ptrace, mount)
Layer 8: Read-only root filesystem (--read-only)
Layer 9: Drop all capabilities (--cap-drop=ALL)
Layer 10: Run as nobody user (--user=nobody)
Layer 11: Ephemeral tmpfs cho writable paths only
```

**Docker command nang cap**:
```bash
docker run --rm \
  --memory=256m \
  --cpus=0.5 \
  --network=none \
  --read-only \
  --cap-drop=ALL \
  --user=nobody \
  --tmpfs /tmp:size=64m \
  --security-opt=no-new-privileges \
  --security-opt seccomp=sandbox-profile.json \
  code-sandbox:latest \
  ...
```

### 9.3 Production-grade (ngoai scope thesis)

| Cap do | Cong nghe | Bao ve |
|--------|-----------|--------|
| Process | seccomp-bpf + capabilities drop | Chan syscall nguy hiem |
| Container | Docker + read-only + no-network | Namespace isolation |
| MicroVM | **Firecracker** | Hardware-level isolation, kernel rieng |
| Infrastructure | Network segmentation | Judge machine tren subnet rieng |

---

## 10. Cau hoi hoi dong va cau tra loi

### Q: "He thong co xu ly duoc khi 1000 user submit cung luc khong?"

**A**: Thiet ke hien tai phuc vu 50-60 user cua thi nghiem. Voi 1000 user dong thoi, can nang cap len kien truc queue-based (BullMQ + worker pool). Kien truc hien tai da chuan bi san cho viec nay: `executeSubmission()` da tach khoi `create()`, status da la state machine (PENDING → RUNNING → terminal), va he thong da co Redis. Chi can them ~200 dong code de tich hop BullMQ. Cac he thong lon nhu LeetCode dung Kafka + pre-scaled worker pool + two-phase testing de xu ly 200,000 submission/contest.

### Q: "Docker co an toan khong cho viec chay code cua nguoi dung?"

**A**: Docker cung cap namespace isolation va cgroup resource limit — du an toan cho moi truong tin cay (sinh vien trong truong). He thong them cac lop bao mat: network disabled, memory limit, CPU limit, timeout, base64 encoding. Tuy nhien, Docker dung chung kernel voi host — o production voi untrusted users, nen dung Firecracker microVM (AWS Lambda dung cong nghe nay) hoac them seccomp-bpf profile de chan syscall nguy hiem.

### Q: "LeetCode lam the nao de tra ket qua nhanh trong contest?"

**A**: Two-phase testing. Trong contest chi chay 10% test case (pretest) → tra ket qua trong 2-3 giay. 90% test case con lai chay sau contest (system testing). Ky thuat nay tang capacity len 10 lan voi cung infrastructure. Codeforces dung cach tuong tu. AdaptLearn chua can vi moi problem chi co 5-7 test case va 60 user.

### Q: "Tai sao khong dung serverless (AWS Lambda) thay vi Docker?"

**A**: AWS Lambda co cold start 500ms-2s, va khong cho phep chay Docker-in-Docker. Firecracker (cong nghe cua Lambda) la lua chon tot, nhung yeu cau KVM support va phuc tap de setup. Docker don gian hon, da tich hop voi Docker Compose cua he thong, va du cho scope thesis. Neu trien khai production, Firecracker voi snapshot (boot 28ms) la lua chon toi uu.

### Q: "So sanh he thong cua ban voi Judge0?"

**A**: Judge0 dung Isolate sandbox (nhe hon Docker, purpose-built cho OJ), Redis + Resque queue, va Ruby on Rails API. AdaptLearn dung Docker (pho bien hon, de setup), chua co queue (du cho 60 user), va NestJS API. Diem khac biet chinh: AdaptLearn khong chi la judge — no la **adaptive learning platform** voi 5 layer AI. Code execution chi la 1 phan, khong phai toan bo he thong.

---

## 11. Tai lieu tham khao

### He thong thuc te
- LeetCode Contest System Design — systemdesignschool.io, hellointerview.com
- Codeforces Judge Systems — codeforces.com/blog/entry/16586
- Judge0 Open Source — github.com/judge0/judge0
- DMOJ Online Judge — github.com/DMOJ/online-judge
- Sphere Engine Documentation — docs.sphere-engine.com

### Cong nghe sandbox
- Firecracker MicroVM — firecracker-microvm.github.io
- gVisor — gvisor.dev/docs/architecture_guide/performance
- nsjail — github.com/google/nsjail
- Figma Engineering: Sandboxing and Workload Isolation — figma.com/blog

### Nghien cuu hoc thuat
- "Robust and Scalable Online Code Execution System" — IEEE, 2020
- "Online Judge System: Requirements, Architecture, and Experiences" — World Scientific, IJSEKE, 2022
- "A Survey on Online Judge Systems and Their Applications" — arXiv:1710.05913
- "A Cloud-Native Online Judge System" — Academia Sinica
- "A Comparison of Sandbox Technologies Used in Online Judge Systems" — ResearchGate

---

*Document nay la phu luc cho ARCHITECTURE-AND-DESIGN-DECISIONS.md.
In kem khi bao ve de tra loi cac cau hoi ve scalability va code execution.*
