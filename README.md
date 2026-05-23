# CSNexus

A full-stack learning platform that helps Filipino candidates prepare for the **Civil Service Examination (CSE)**. The system covers both Professional and Sub-Professional levels with structured lessons, adaptive quizzes, mock exams, progress tracking, and gamification — all tailored to the Philippine CSE syllabus.

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Content Coverage](#content-coverage)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database](#database)
- [Running Tests](#running-tests)
- [Scripts](#scripts)
- [Deployment](#deployment)
- [API Overview](#api-overview)
- [Contributing](#contributing)
- [License](#license)

---

## Architecture

CSNexus uses a **feature-sliced architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (PWA)                        │
│         React 18 + TypeScript + Vite + IndexedDB        │
│              Offline-first, installable                  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (JSON)
┌────────────────────────▼────────────────────────────────┐
│                   Backend (FastAPI)                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐    │
│  │  Router  │→ │ Service  │→ │    Repository      │    │
│  │ (HTTP)   │  │ (Logic)  │  │ (SQLAlchemy ORM)   │    │
│  └──────────┘  └──────────┘  └─────────┬──────────┘    │
│                                         │               │
│  Middlewares: Auth, CORS, Rate Limit,   │               │
│  Logging, Security Headers, Errors      │               │
└─────────────────────────────────────────┼───────────────┘
                                          │
                         ┌────────────────▼────────────────┐
                         │         Database                 │
                         │  SQLite (dev) / PostgreSQL (prod)│
                         └─────────────────────────────────┘
```

Each feature module follows the pattern: `models.py → schemas.py → repository.py → service.py → router.py`

---

## Tech Stack

### Backend

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Runtime |
| FastAPI | Web framework, auto-generated OpenAPI docs |
| SQLAlchemy 2.x | ORM and database abstraction |
| Pydantic 2.x | Request/response validation |
| Uvicorn | ASGI server |
| APScheduler | Background job scheduling |
| PyJWT | JSON Web Token authentication |
| bcrypt | Password hashing |
| slowapi | Rate limiting |
| google-auth | Google OAuth verification |
| psycopg2 | PostgreSQL driver (production) |

### Frontend

| Technology | Purpose |
|-----------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| Vite 5 | Build tool and dev server |
| React Router 6 | Client-side routing |
| Framer Motion | Animations |
| IndexedDB (idb) | Offline data persistence |
| vite-plugin-pwa | Service worker and PWA manifest |
| Vitest | Unit testing |
| Testing Library | Component testing |

### Dev Tools

| Tool | Purpose |
|------|---------|
| pytest | Test runner |
| hypothesis | Property-based testing |
| httpx | HTTP client for route tests |
| ruff | Linting and formatting |
| mypy | Static type checking |
| bandit | Security analysis |

---

## Project Structure

```
csnexus/
├── app/                          # FastAPI backend
│   ├── main.py                   # App entrypoint, middleware wiring, router mounting
│   ├── common/                   # Shared utilities
│   │   ├── deps.py               # Common FastAPI dependencies
│   │   ├── middlewares/          # Auth, CORS, error handling, logging, rate limit, security headers
│   │   └── schemas/              # Shared request/response schemas (PaginationParams, ErrorResponse)
│   ├── features/                 # Feature modules (18 total)
│   │   ├── achievements/         # Badges and achievement tracking
│   │   ├── admin/                # Admin dashboard and management
│   │   ├── announcements/        # System announcements
│   │   ├── audit/                # Audit logging
│   │   ├── auth/                 # JWT authentication, Google OAuth
│   │   ├── content/              # Lessons, questions, modules, topics, subtopics
│   │   ├── focus/                # Focus/study session tracking
│   │   ├── gamification/         # Streaks, challenges, rewards
│   │   ├── leaderboards/         # Competitive rankings
│   │   ├── mastery/              # Skill mastery tracking per subtopic
│   │   ├── mock_exams/           # Full-length timed practice exams
│   │   ├── otp/                  # Email OTP verification
│   │   ├── planner/              # Study planner and scheduling
│   │   ├── progress/             # Learning progress tracking
│   │   ├── quizzes/              # Adaptive quiz engine
│   │   ├── tutor/                # AI tutor interactions
│   │   ├── users/                # User profiles and management
│   │   └── xp/                   # Experience points system
│   └── infrastructure/           # Cross-cutting infrastructure
│       ├── database/             # Engine, session, base model, pragmas
│       ├── external/             # External service adapters (email, OAuth)
│       ├── repositories/         # BaseRepository generic class
│       ├── scheduler/            # APScheduler job definitions
│       └── security/             # Password hashing, JWT utilities
├── data/
│   ├── cse.db                    # Local SQLite database
│   └── seed/                     # Seed content (lessons + questions)
│       ├── lessons/              # Markdown lesson files
│       └── questions/            # JSON question banks
├── scripts/                      # Content generation and seeding scripts
├── tests/                        # Test suite (mirrors app structure)
│   ├── conftest.py               # Shared fixtures (in-memory SQLite)
│   ├── common/                   # Middleware and schema tests
│   ├── features/                 # Per-feature test modules
│   ├── infrastructure/           # Database and repository tests
│   └── smoke/                    # End-to-end smoke tests
├── web/                          # React PWA frontend
│   ├── src/
│   │   ├── api/                  # API client layer
│   │   ├── components/           # Reusable UI components
│   │   ├── context/              # React context providers
│   │   ├── design-system/        # Design tokens and base components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── pages/                # Route-level page components
│   │   ├── stores/               # State management
│   │   ├── sw/                   # Service worker logic
│   │   └── utils/                # Utility functions
│   ├── content/                  # Static content for offline access
│   ├── dist/                     # Production build output
│   └── public/                   # Static assets
├── .env.example                  # Environment variable template
├── pyproject.toml                # Python project config (deps, tools)
├── render.yaml                   # Render deployment blueprint
├── Procfile                      # Process definition for PaaS
└── DEPLOY.md                     # Detailed deployment guide
```

---

## Features

### Learning System
- **Structured Lessons** — Markdown-based lessons parsed into sections (explanations, worked examples, key takeaways, summary)
- **Adaptive Quizzes** — Questions drawn from a bank of 600 per subtopic (200 Easy / 200 Medium / 200 Hard)
- **Mock Exams** — Full-length timed exams simulating the real CSE (50 questions, 180 minutes, configurable per category)
- **Mastery Tracking** — Per-subtopic skill mastery with progression metrics

### Gamification
- **XP System** — Experience points earned through quizzes, lessons, and streaks
- **Achievements** — Unlockable badges for milestones (MVP + Phase 2 sets)
- **Leaderboards** — Competitive rankings across users
- **Streaks & Challenges** — Daily engagement incentives

### User Management
- **JWT Authentication** — Secure token-based auth with refresh tokens
- **Google OAuth** — "Continue with Google" social login
- **Email OTP** — Verification via Brevo/Resend with offline fallback logging
- **Role-Based Access** — Admin and Learner roles with separate permissions
- **Category Selection** — Professional or Sub-Professional exam track

### Platform
- **Progressive Web App** — Installable, offline-capable via service workers
- **Offline Lessons** — IndexedDB-backed lesson storage for study without internet
- **Study Planner** — Scheduled study sessions with reminders
- **Focus Sessions** — Timed study tracking (Pomodoro-style)
- **AI Tutor** — Contextual help and explanations
- **Audit Logging** — Admin action tracking
- **Rate Limiting** — slowapi-based request throttling
- **Request Tracing** — X-Request-ID on every request for debugging

---

## Content Coverage

The platform covers all three CSE subtests with comprehensive lesson content and question banks:

### Verbal Ability (3 topics, 23 subtopics)

| Topic | Subtopics |
|-------|-----------|
| Grammar | Subject-Verb Agreement, Verb Tenses, Pronouns, Prepositions, Articles, Conjunctions, Modifiers, Parallelism, Active/Passive Voice, Direct/Indirect Speech |
| Reading Comprehension | Fundamentals, Organization of Ideas, Author's Purpose & Tone, Analytical Comprehension, Vocabulary in Context |
| Vocabulary Development | Synonyms, Antonyms, Context Clues, Word Formation, Idioms & Expressions, Analogies, Denotation & Connotation, Formal/Informal Language |

### Numerical Ability (3 topics, 24 subtopics)

| Topic | Subtopics |
|-------|-----------|
| Basic Operations | Fundamental Number Concepts, Addition, Subtraction, Multiplication, Division, Order of Operations, Exponents & Roots, Signed Numbers, Estimation & Mental Math, Word Problems |
| Percentages | Fundamentals, Basic Problems, Increase & Decrease, Word Problems, Applications, Discounts/Markups/Sales, Profit/Loss/Tax, Mental Math & Shortcuts |
| Ratio, Proportion & Average | Introduction to Ratios, Types of Ratios, Ratio Word Problems, Direct & Inverse Proportions, Proportion Word Problems, Scale & Map Problems |

### Analytical Ability (3 topics, 13 subtopics)

| Topic | Subtopics |
|-------|-----------|
| Abstract Reasoning | Shape Patterns |
| Symbolic Logic | Logical Statements, Logical Operators, Conditional Reasoning, Syllogisms, Truth & Validity |
| Word Analogy | Synonym & Antonym Analogies, Part-Whole & Classification, Function & Purpose, Cause-Effect & Progression, Language/Meaning/Context, Symbolic/Characteristic/Location, Numerical/Letter/Abstract |

Each subtopic includes a full lesson (800-1200 lines) and 600 questions (200 per difficulty level).

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for the frontend)
- Git

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/csnexus.git
cd csnexus

# Install Python dependencies (with dev tools)
pip install -e ".[dev]"

# Copy environment config
cp .env.example .env

# Run the backend server
uvicorn app.main:app --reload
```

The server starts at `http://localhost:8000`. On first boot, it automatically:
1. Creates all database tables
2. Seeds the database with default users and content (if empty)

Default admin credentials: `admin@cse.local` / `Admin1Pass!`

### Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The frontend starts at `http://localhost:5173` and proxies API calls to the backend.

### Full Stack (both running)

Terminal 1:
```bash
uvicorn app.main:app --reload
```

Terminal 2:
```bash
cd web && npm run dev
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | No | `sqlite:///data/cse.db` | Database connection string |
| `JWT_SECRET` | Yes (prod) | `change-me-...` | Secret for signing JWTs |
| `BREVO_API_KEY` | No | — | Brevo email API key for OTP delivery |
| `EMAIL_FROM_ADDR` | No | `CSNexus <noreply@csnexus.space>` | Sender address for emails |
| `OTP_OFFLINE_LOG_PATH` | No | `data/otp_offline.log` | Fallback OTP log when email is unconfigured |
| `GOOGLE_CLIENT_ID` | No | — | Google OAuth client ID |
| `APP_ENV` | No | `development` | `development` or `production` (controls CORS, HSTS) |
| `ADMIN_EMAIL` | No | `admin@cse.local` | Admin user email for seeding |
| `ADMIN_PASSWORD` | No | `Admin1Pass!` | Admin user password for seeding |
| `DISABLE_SCHEDULER` | No | — | Set to `1` to disable background jobs |

---

## Database

### Development (SQLite)

Zero configuration. The app creates `data/cse.db` automatically on first run.

### Production (PostgreSQL via Supabase)

Set `DATABASE_URL` to your Supabase Session pooler connection string:

```
postgresql://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres
```

The app automatically:
- Normalizes `postgres://` to `postgresql+psycopg2://`
- Appends `sslmode=require` if not present
- Configures connection pooling (pool_size=5, max_overflow=10, pool_pre_ping=True)

### Seeding

On first boot (when no admin user exists), the app auto-seeds:
- Admin user + 2 learner users
- Content hierarchy (modules → topics → subtopics → lessons → questions)
- Achievement definitions
- Mock exam configurations

Manual seed:
```bash
python -m scripts.seed
```

Full content seed (lessons + questions from `data/seed/`):
```bash
python -m scripts.seed_all_content
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific feature's tests
pytest tests/features/auth/

# Run only service-layer tests
pytest -k "test_service"

# Type checking
mypy app/

# Linting
ruff check app/ tests/

# Security scan
bandit -r app/
```

### Test Architecture

Tests use an **in-memory SQLite database** with function-scoped fixtures for full isolation:

- **Repository tests** — Real DB queries, no mocks
- **Service tests** — Mocked repositories (`MagicMock(spec=...)`)
- **Router tests** — Mocked services, `TestClient` HTTP assertions

---

## Scripts

### Content Generation

Scripts in `scripts/` generate question banks programmatically:

```bash
# Generate questions for a specific subtopic
python scripts/gen_addition_questions.py
python scripts/gen_synonyms_questions.py

# Seed all content into the database
python -m scripts.seed_all_content

# Reset and re-seed everything
python -m scripts.reset_and_seed
```

### Utility Scripts

| Script | Purpose |
|--------|---------|
| `seed.py` | Minimal fixture seed (users, content hierarchy, achievements) |
| `seed_content.py` | Seed lessons and questions from `data/seed/` files |
| `seed_all_content.py` | Full content seeding pipeline |
| `reset_and_seed.py` | Drop all tables, recreate, and seed from scratch |
| `parse_lesson.py` | Parse lesson markdown into structured JSON |
| `smoke_test.py` | Quick API smoke test |
| `update_lessons.py` | Update existing lessons from modified markdown files |
| `add_missing_subtopics.py` | Add new subtopics to existing topics |

---

## Deployment

The project deploys on a **zero-cost stack**:

| Layer | Service |
|-------|---------|
| Database | Supabase (500 MB PostgreSQL, free) |
| Backend | Render (750 hrs/month, auto-deploy from GitHub) |
| Frontend | Vercel (unlimited static deploys, global CDN) |
| Email | Brevo/Resend (3,000 emails/month free) |
| Keep-alive | cron-job.org + UptimeRobot (prevents Render sleep) |

See [DEPLOY.md](DEPLOY.md) for the full step-by-step deployment guide.

### Quick Deploy

```bash
# Backend (Render auto-deploys from main branch)
# Build: pip install -e .
# Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Frontend (Vercel)
cd web && npm run build
# Output: web/dist/
```

---

## API Overview

All endpoints are prefixed with `/v1/` (via feature routers). Interactive docs available at `/docs` (Swagger) and `/redoc`.

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (unauthenticated) |
| POST | `/v1/auth/register` | User registration |
| POST | `/v1/auth/login` | Email/password login |
| POST | `/v1/auth/google` | Google OAuth login |
| GET | `/v1/content/modules` | List modules by category |
| GET | `/v1/content/lessons/{id}` | Get lesson content |
| GET | `/v1/content/questions` | Get questions (filtered) |
| POST | `/v1/quizzes/start` | Start a quiz session |
| POST | `/v1/quizzes/{id}/submit` | Submit quiz answers |
| POST | `/v1/mock-exams/start` | Start a mock exam |
| GET | `/v1/progress/summary` | User progress summary |
| GET | `/v1/leaderboards` | Leaderboard rankings |
| GET | `/v1/achievements` | User achievements |
| GET | `/v1/xp/summary` | XP and level info |

### Response Format

Success responses use the resource directly. Error responses follow a consistent envelope:

```json
{
  "error": {
    "message": "Item not found",
    "code": "NOT_FOUND"
  }
}
```

### Pagination

All list endpoints accept `skip` and `limit` query parameters:

```
GET /v1/content/questions?skip=0&limit=20
```

Response includes `items`, `total`, `skip`, and `limit`.

---

## Contributing

1. Create a feature branch from `main`
2. Follow the [code conventions](.kiro/steering/code-conventions.md) (feature-sliced architecture, type hints, absolute imports)
3. Write tests for all three layers (repository, service, router)
4. Run `ruff check`, `mypy`, and `pytest` before pushing
5. Open a PR with a clear description

---

## License

Proprietary. All rights reserved.
