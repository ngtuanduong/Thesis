# Development Setup Guide

**Project:** Adaptive Learning Platform for University Programming Courses

---

## Prerequisites

| Tool | Version | Check Command |
|------|---------|---------------|
| Docker & Docker Compose | 24+ / v2+ | `docker --version && docker compose version` |
| Node.js | 20+ | `node --version` |
| npm | 10+ | `npm --version` |
| Git | 2.x | `git --version` |

---

## Project Structure

```
KhoaLuan/
├── client/          # React frontend (Vite + TypeScript + Ant Design)
├── server/          # NestJS backend (Prisma ORM)
├── ai-service/      # FastAPI AI service (Python 3.12)
├── docker/          # Docker Compose + Dockerfiles
│   ├── docker-compose.yml
│   ├── backend.Dockerfile
│   ├── init-pgvector.sql
│   └── sandbox/     # Code execution sandbox
└── documents/       # Thesis documentation
```

---

## Step 1: Clone the Repository

```bash
git clone <repo-url> KhoaLuan
cd KhoaLuan
git checkout v2
```

---

## Step 2: Start Infrastructure (Docker)

Start PostgreSQL, Redis, and the AI service:

```bash
cd docker
docker compose up -d
```

This launches 3 containers:

| Container | Service | Port |
|-----------|---------|------|
| `adaptive-learning-db` | PostgreSQL 16 + pgvector | 5432 |
| `adaptive-learning-redis` | Redis 7 | 6379 |
| `adaptive-learning-ai` | FastAPI AI Service | 8000 |

Wait for all containers to be healthy:

```bash
docker compose ps
```

Verify the AI service is ready:

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

> **Note:** The AI service takes ~30 seconds on first start to download the embedding model (~90MB). Subsequent starts use the cached model.

---

## Step 3: Run Database Migrations

Push the Prisma schema to PostgreSQL:

```bash
cd docker
docker compose run --rm prisma-migrate
```

This creates all database tables including: users, problems, courses, submissions, concepts, knowledge graph edges, knowledge states, Elo ratings, MAB states, FSRS cards, etc.

---

## Step 4: Install Backend Dependencies & Seed Data

```bash
cd server
npm install
npx prisma generate
npx prisma db seed
```

The seed script creates:
- 4 users (admin, instructor, 2 students)
- 2 courses
- 30 programming problems with test cases
- 34 concepts across 7 topic groups
- 36 prerequisite edges (knowledge graph)
- 58 problem-concept mappings
- Elo ratings for all problems

---

## Step 5: Create Backend Environment File

Create `server/.env`:

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/adaptive_learning?schema=public"
JWT_SECRET="Duong-2025-Adaptive-Learning"
JWT_EXPIRATION="7d"
REDIS_HOST="localhost"
REDIS_PORT=6379
PORT=3333
NODE_ENV="development"
AI_SERVICE_URL="http://localhost:8000"
AI_SERVICE_KEY="dev-secret-key"
CLIENT_URL="http://localhost:5173"
```

---

## Step 6: Start the NestJS Backend

```bash
cd server
npm run start:dev
```

The backend starts on **http://localhost:3333** with hot reload.

Verify:

```bash
curl http://localhost:3333/api/problems | head -100
# Should return JSON array of problems
```

---

## Step 7: Start the React Frontend

```bash
cd client
npm install
npm run dev
```

The frontend starts on **http://localhost:5173** with HMR.

The Vite dev server proxies `/api/*` requests to `http://localhost:3333`.

---

## Step 8: Open the Application

Go to **http://localhost:5173** in your browser.

### Test Accounts

| Role | Email | Password |
|------|-------|----------|
| Student | `student1@example.com` | `password123` |
| Student | `student2@example.com` | `password123` |
| Instructor | `instructor@example.com` | `password123` |
| Admin | `admin@example.com` | `password123` |

---

## Service Architecture

```
Browser (localhost:5173)
  │
  ├─ /api/* ──proxy──> NestJS Backend (localhost:3333)
  │                      │
  │                      ├── PostgreSQL (localhost:5432)
  │                      ├── Redis (localhost:6379)
  │                      └── AI Service (localhost:8000)
  │                           ├── BKT (Knowledge Tracing)
  │                           ├── Elo (Difficulty Calibration)
  │                           ├── MAB (Problem Selection)
  │                           ├── FSRS (Spaced Repetition)
  │                           └── LLM Hints (OpenAI GPT-4o-mini)
  │
  └─ Static assets served by Vite
```

---

## Quick Start (All-in-One)

If the database is already seeded and `server/.env` exists, you can start everything with 3 terminal windows:

**Terminal 1 — Infrastructure:**
```bash
cd docker && docker compose up -d
```

**Terminal 2 — Backend:**
```bash
cd server && npm run start:dev
```

**Terminal 3 — Frontend:**
```bash
cd client && npm run dev
```

---

## Common Commands

### Docker

```bash
# Start all containers
cd docker && docker compose up -d

# Stop all containers
cd docker && docker compose down

# Rebuild AI service (after code changes)
cd docker && docker compose up -d --build ai-service

# View AI service logs
docker logs adaptive-learning-ai --tail 50 -f

# View backend logs (if running in Docker)
docker logs adaptive-learning-backend --tail 50 -f

# Access PostgreSQL directly
docker exec -it adaptive-learning-db psql -U postgres -d adaptive_learning

# Flush Redis cache
docker exec adaptive-learning-redis redis-cli FLUSHALL
```

### Prisma

```bash
cd server

# Regenerate Prisma client after schema changes
npx prisma generate

# Push schema changes to DB (no migration files)
npx prisma db push

# Re-seed the database
npx prisma db seed

# Open Prisma Studio (visual DB browser)
npx prisma studio
```

### Testing

```bash
# Run AI service unit tests (inside Docker)
docker exec adaptive-learning-ai python -m pytest tests/ -v

# Run AI service integration tests (requires seeded DB)
docker exec adaptive-learning-ai python -m pytest tests/test_integration.py -v
```

---

## Troubleshooting

### "AI service unavailable" on Knowledge Map or Dashboard

The AI service container may have old code. Rebuild it:

```bash
cd docker
docker compose up -d --build ai-service
docker exec adaptive-learning-redis redis-cli FLUSHALL
```

### Port already in use

Check what's using the port:

```bash
lsof -i :3333   # Backend
lsof -i :5173   # Frontend
lsof -i :8000   # AI service
lsof -i :5432   # PostgreSQL
```

Kill the process or change the port in the config.

### Database connection refused

Ensure PostgreSQL container is running and healthy:

```bash
docker compose ps
docker logs adaptive-learning-db --tail 20
```

### Prisma schema out of sync

If you see migration errors:

```bash
cd server
npx prisma db push --force-reset   # WARNING: drops all data
npx prisma db seed                 # Re-seed after reset
```

### AI service model download fails

The embedding model is cached in a Docker volume. If it fails:

```bash
docker volume rm docker_model_cache
cd docker && docker compose up -d --build ai-service
```

---

## Environment Variables Reference

### Server (`server/.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL connection string |
| `JWT_SECRET` | — | Secret key for JWT signing |
| `JWT_EXPIRATION` | `7d` | JWT token expiry |
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `PORT` | `3333` | NestJS server port |
| `NODE_ENV` | `development` | Environment mode |
| `AI_SERVICE_URL` | `http://localhost:8000` | FastAPI AI service URL |
| `AI_SERVICE_KEY` | `dev-secret-key` | Service-to-service auth key |
| `CLIENT_URL` | `http://localhost:5173` | CORS allowed origin |

### AI Service (set in `docker-compose.yml`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL async connection string |
| `AI_SERVICE_KEY` | `dev-secret-key` | Auth key for incoming requests |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection URL |
| `ENABLE_BKT` | `true` | Enable Knowledge Tracing layer |
| `ENABLE_ELO` | `true` | Enable Elo rating layer |
| `ENABLE_MAB` | `true` | Enable MAB selection layer |
| `ENABLE_FSRS` | `true` | Enable spaced repetition layer |
| `ENABLE_LLM` | `false` | Enable LLM hints (needs OpenAI key) |
| `OPENAI_API_KEY` | — | OpenAI API key (for hints) |
