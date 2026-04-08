# AdaptLearn — Adaptive Learning Platform for University Programming Courses

## Overview

A thesis project implementing a 5-layer adaptive learning platform that personalizes programming education through Bayesian Knowledge Tracing (BKT), Dynamic Elo Rating, Hierarchical Multi-Armed Bandits, FSRS Spaced Repetition, and LLM-powered Socratic hints.

Students submit code solutions that are executed in a Docker sandbox, and the platform continuously updates a personalized learner model to recommend problems at the right difficulty, schedule reviews at optimal intervals, and generate context-aware hints when students are stuck.

## Architecture

The system follows a three-service architecture:

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  React SPA   │─────>│  NestJS API      │─────>│  FastAPI AI      │
│  (Vite)      │<─────│  Gateway         │<─────│  Service         │
│  Port 5173   │      │  Port 3000       │      │  Port 8000       │
└──────────────┘      └──────┬───────────┘      └──────┬───────────┘
                             │                         │
                      ┌──────┴───────────┐      ┌──────┴───────────┐
                      │  PostgreSQL 16   │      │  Redis 7         │
                      │  + pgVector      │      │  Cache / Queue   │
                      │  Port 5432       │      │  Port 6379       │
                      └──────────────────┘      └──────────────────┘
```

- **React Frontend** — Single-page application with CodeMirror editor, knowledge-graph visualization (React Flow), and Ant Design UI components.
- **NestJS API Gateway** — REST API with JWT authentication, Prisma ORM, Swagger docs, and Docker-sandboxed code execution.
- **FastAPI AI Service** — Adaptive learning engine with sentence-transformer embeddings, BKT/Elo/MAB/FSRS algorithms, and LLM hint generation via OpenAI.

## Tech Stack

| Component        | Technology                                  | Purpose                                      |
| ---------------- | ------------------------------------------- | -------------------------------------------- |
| Frontend         | React 18 + TypeScript + Ant Design + Vite   | Student/instructor UI with code editor        |
| Backend          | NestJS 10 + Prisma ORM                      | API gateway, auth, submission orchestration   |
| AI Service       | FastAPI + SQLAlchemy + sentence-transformers | Adaptive algorithms, embeddings, LLM hints    |
| Database         | PostgreSQL 16 + pgVector                    | Relational data + vector similarity search    |
| Cache            | Redis 7                                     | Session cache, rate limiting, queue           |
| Code Execution   | Docker sandbox (isolated containers)        | Safe student code execution with resource limits |
| Documentation    | Swagger / OpenAPI at `/api/docs`            | Interactive API reference                     |

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 16 (with pgVector extension)
- Redis 7
- Docker (for code execution sandbox and optional containerized deployment)

### Running with Docker (Recommended)

The fastest way to start all services:

```bash
cd docker
docker compose up -d
```

This starts PostgreSQL (with pgVector), Redis, the NestJS backend, and the FastAPI AI service. The frontend runs separately for hot-reload during development.

Then start the frontend:

```bash
cd client
npm install
npm run dev
```

Run database migrations (first time only):

```bash
docker compose --profile tools run --rm prisma-migrate
```

### Running for Development

If you prefer running services natively:

**1. Database & Cache**

```bash
# Start PostgreSQL and Redis via Docker
cd docker
docker compose up postgres redis -d
```

**2. Backend (NestJS)**

```bash
cd server
npm install
cp .env.example .env        # Configure DATABASE_URL, JWT_SECRET, etc.
npx prisma generate
npx prisma db push           # Apply schema to database
npm run start:dev            # Starts on http://localhost:3000
```

**3. AI Service (FastAPI)**

```bash
cd ai-service
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**4. Frontend (React)**

```bash
cd client
npm install
npm run dev                  # Starts on http://localhost:5173
```

### Database Setup

```bash
cd server

# Generate Prisma client
npx prisma generate

# Push schema to database (development)
npx prisma db push

# Or run migrations (production)
npx prisma migrate dev

# Seed with sample data
npx prisma db seed

# Seed adaptive learning data
npx ts-node prisma/seed-adaptive.ts

# Open Prisma Studio (database GUI)
npx prisma studio
```

## API Documentation

Interactive Swagger documentation is available at:

```
http://localhost:3000/api/docs
```

All API routes are prefixed with `/api`. Authentication uses JWT Bearer tokens.

## Project Structure

```
.
├── client/                     # React frontend (Vite + TypeScript)
│   ├── src/
│   │   ├── api/                # API client functions
│   │   ├── components/         # Reusable UI components
│   │   ├── layouts/            # Page layout wrappers
│   │   ├── pages/              # Route-level page components
│   │   ├── routes/             # React Router configuration
│   │   └── types/              # TypeScript type definitions
│   └── vite.config.ts
│
├── server/                     # NestJS backend
│   ├── prisma/
│   │   ├── schema.prisma       # Database schema
│   │   ├── seed.ts             # Base seed data
│   │   └── seed-adaptive.ts    # Adaptive learning seed data
│   └── src/
│       ├── adaptive/           # Adaptive learning proxy layer
│       ├── admin/              # Admin dashboard endpoints
│       ├── ai/                 # AI service client
│       ├── auth/               # JWT authentication
│       ├── common/             # Shared middleware, guards, filters
│       ├── concepts/           # Knowledge graph concepts
│       ├── courses/            # Course management
│       ├── instructor/         # Instructor-specific endpoints
│       ├── prisma/             # Prisma database module
│       ├── problems/           # Programming problems CRUD
│       ├── recommendations/    # Content-based recommendations
│       ├── skills/             # User skill embeddings
│       ├── submissions/        # Code submission & execution
│       └── users/              # User management
│
├── ai-service/                 # FastAPI AI microservice
│   ├── app/
│   │   ├── models/             # SQLAlchemy models
│   │   ├── routers/            # API route handlers
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic (BKT, Elo, MAB, FSRS)
│   │   ├── config.py           # Service configuration
│   │   ├── database.py         # Async database setup
│   │   └── main.py             # FastAPI application entry
│   ├── tests/                  # Pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker/
    ├── docker-compose.yml      # Full-stack orchestration
    ├── backend.Dockerfile       # NestJS container
    ├── init-pgvector.sql       # pgVector extension init
    └── sandbox/                # Code execution sandbox image
```

## Adaptive Learning Layers

The platform implements five complementary adaptive layers, each targeting a different aspect of personalized learning:

1. **BKT (Bayesian Knowledge Tracing)** — Estimates per-concept mastery probability using a Hidden Markov Model. Tracks `P(learned)`, `P(guess)`, `P(slip)`, and `P(transit)` to determine when a student has truly mastered a concept vs. guessing correctly.

2. **Dynamic Elo Rating** — Maintains dual Elo ratings for both students and problems. After each submission, ratings adjust based on whether the outcome was expected. This provides a continuous difficulty-calibrated measure of student ability.

3. **Hierarchical Multi-Armed Bandit (MAB)** — Uses Thompson Sampling at two levels (concept selection and problem selection within a concept) to balance exploration of new topics against exploitation of known weak areas. Maximizes learning efficiency over time.

4. **FSRS Spaced Repetition** — Implements the Free Spaced Repetition Scheduler algorithm to schedule review of previously solved problems at optimal intervals, combating the forgetting curve with increasing review gaps as retention strengthens.

5. **LLM Socratic Hints** — Generates progressive, Socratic-style hints using an LLM (via OpenAI API). Hints are context-aware, considering the student's code, error messages, knowledge state, and a configurable hint level (from gentle nudge to near-solution).

## Testing

**Backend (NestJS)**

```bash
cd server
npm test                # Run unit tests
npm run test:e2e        # Run end-to-end tests (if configured)
```

**AI Service (FastAPI)**

```bash
cd ai-service
source .venv/bin/activate
pytest                  # Run all tests
pytest -v               # Verbose output
```

**Frontend (React)**

```bash
cd client
npm test                # Run tests (if configured)
```

## Environment Variables

Key environment variables (see `.env.example` files in each service):

| Variable           | Service   | Description                          |
| ------------------ | --------- | ------------------------------------ |
| `DATABASE_URL`     | Backend   | PostgreSQL connection string         |
| `JWT_SECRET`       | Backend   | Secret key for JWT signing           |
| `JWT_EXPIRATION`   | Backend   | Token expiry (e.g., `7d`)           |
| `AI_SERVICE_URL`   | Backend   | FastAPI service URL                  |
| `AI_SERVICE_KEY`   | Both      | Shared service authentication key    |
| `REDIS_HOST`       | Backend   | Redis hostname                       |
| `EMBEDDING_MODEL`  | AI Svc    | Sentence-transformer model name      |
| `CLIENT_URL`       | Backend   | Frontend origin for CORS             |

## License

MIT
