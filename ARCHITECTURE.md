# CSNexus — Application Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                             │
│                              ╔═══════════════════════════════════╗                           │
│                              ║     FRONTEND  (React 18 PWA)      ║                           │
│                              ╚═══════════════════════════════════╝                           │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐    │
│  │  web/src/                                                                           │    │
│  │                                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────────────────────────┐   │    │
│  │  │  PAGES (Route-level components)                                              │   │    │
│  │  │                                                                              │   │    │
│  │  │  auth/          content/         quiz/         mock-exam/     flashcards/     │   │    │
│  │  │  ├─ Login       ├─ ModuleList    └─ QuizPlayer └─ MockExam    ├─ Flashcards  │   │    │
│  │  │  ├─ Signup      ├─ TopicList                      Player      ├─ DeckDetail  │   │    │
│  │  │  ├─ ForgotPwd   ├─ SubtopicList                              ├─ CreateDeck  │   │    │
│  │  │  └─ OTPVerify   └─ LessonReader                              ├─ StudySession│   │    │
│  │  │                                                               ├─ Marketplace │   │    │
│  │  │  Home  Leaderboard  Mastery  Analytics  Goals  Tournaments    ├─ Analytics   │   │    │
│  │  │  Profile  AdminDashboard  Tutor  StudyPlan  Readiness  Focus  ├─ ExamSim     │   │    │
│  │  │                                                               ├─ Social      │   │    │
│  │  │                                                               ├─ Generate    │   │    │
│  │  │                                                               └─ Admin       │   │    │
│  │  └──────────────────────────────────────────────────────────────────────────────┘   │    │
│  │                                                                                     │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌───────────────┐   │    │
│  │  │ components/│  │  stores/   │  │  hooks/    │  │ context/ │  │ design-system/│   │    │
│  │  │ GlassNavbar│  │ auth.ts    │  │ Custom     │  │ Toast    │  │ Tokens &      │   │    │
│  │  │ AuthGuard  │  │ (JWT/      │  │ React      │  │ Provider │  │ Base UI       │   │    │
│  │  │ Ambient BG │  │  localStorage│ │ hooks     │  │          │  │ Components    │   │    │
│  │  └────────────┘  └────────────┘  └────────────┘  └──────────┘  └───────────────┘   │    │
│  │                                                                                     │    │
│  │  ┌──────────────────────┐  ┌──────────────────────────────────────────────────┐     │    │
│  │  │  api/client.ts       │  │  sw/ (Service Worker)                            │     │    │
│  │  │  Typed fetch wrapper │  │  ├─ Offline-first caching (StaleWhileRevalidate) │     │    │
│  │  │  Auto Bearer token   │  │  ├─ IndexedDB persistence (idb)                  │     │    │
│  │  │  401 auto-logout     │  │  └─ PWA installability (vite-plugin-pwa)         │     │    │
│  │  │  Error envelope parse│  │                                                  │     │    │
│  │  └──────────┬───────────┘  └──────────────────────────────────────────────────┘     │    │
│  └─────────────┼───────────────────────────────────────────────────────────────────────┘    │
│                │                                                                            │
│                │  REST API (JSON) — /v1/* endpoints                                         │
│                │  Vite dev proxy → localhost:8000                                            │
│                ▼                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                     │    │
│  │                         ╔═══════════════════════════════════╗                        │    │
│  │                         ║    BACKEND  (FastAPI + Uvicorn)    ║                        │    │
│  │                         ╚═══════════════════════════════════╝                        │    │
│  │                                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │  MIDDLEWARE PIPELINE  (reverse-add order: last added → first executed)        │  │    │
│  │  │                                                                               │  │    │
│  │  │  Request ──► CORS ──► Auth (permissive JWT decode) ──► Security Headers       │  │    │
│  │  │          ──► Request Logging (X-Request-ID) ──► Rate Limiting (slowapi)       │  │    │
│  │  │          ──► Error Handler (500 envelope) ──► Route Handler                   │  │    │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │  COMMON DEPENDENCIES  (app/common/deps.py)                                    │  │    │
│  │  │                                                                               │  │    │
│  │  │  get_current_user ──► require_admin ──► require_no_active_mock                │  │    │
│  │  │  PaginationParams    PaginatedResponse[T]    ErrorResponse                    │  │    │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │  FEATURE MODULES  (app/features/ — 19 slices)                                 │  │    │
│  │  │  Each slice: models.py → schemas.py → repository.py → service.py → router.py │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────────────────────────────────────────────────────────────┐  │  │    │
│  │  │  │  LEARNING CORE                                                          │  │  │    │
│  │  │  │  ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌───────────┐   │  │  │    │
│  │  │  │  │ content  │ │ quizzes  │ │ mock_exams │ │ mastery  │ │flashcards │   │  │  │    │
│  │  │  │  │ Modules  │ │ Adaptive │ │ Timed full │ │ Per-sub  │ │ FSRS algo │   │  │  │    │
│  │  │  │  │ Topics   │ │ quiz     │ │ length CSE │ │ topic    │ │ Decks &   │   │  │  │    │
│  │  │  │  │ Subtopics│ │ engine   │ │ simulation │ │ skill    │ │ spaced    │   │  │  │    │
│  │  │  │  │ Lessons  │ │          │ │            │ │ tracking │ │ repetition│   │  │  │    │
│  │  │  │  │ Questions│ │          │ │            │ │          │ │           │   │  │  │    │
│  │  │  │  └──────────┘ └──────────┘ └────────────┘ └──────────┘ └───────────┘   │  │  │    │
│  │  │  └─────────────────────────────────────────────────────────────────────────┘  │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────────────────────────────────────────────────────────────┐  │  │    │
│  │  │  │  GAMIFICATION & ENGAGEMENT                                              │  │  │    │
│  │  │  │  ┌──────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────┐ ┌──────────┐  │  │  │    │
│  │  │  │  │achievements  │ │   xp     │ │ gamification │ │focus │ │ planner  │  │  │  │    │
│  │  │  │  │ Badges &     │ │ Points & │ │ Streaks &    │ │Pomo- │ │ Study    │  │  │  │    │
│  │  │  │  │ milestones   │ │ levels   │ │ challenges   │ │doro  │ │ schedule │  │  │  │    │
│  │  │  │  └──────────────┘ └──────────┘ └──────────────┘ └──────┘ └──────────┘  │  │  │    │
│  │  │  └─────────────────────────────────────────────────────────────────────────┘  │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────────────────────────────────────────────────────────────┐  │  │    │
│  │  │  │  USER & AUTH                                                            │  │  │    │
│  │  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                                │  │  │    │
│  │  │  │  │  auth    │ │  users   │ │   otp    │                                │  │  │    │
│  │  │  │  │ JWT +    │ │ Profiles │ │ Email    │                                │  │  │    │
│  │  │  │  │ Google   │ │ Roles    │ │ verify   │                                │  │  │    │
│  │  │  │  │ OAuth    │ │ Category │ │ + offline│                                │  │  │    │
│  │  │  │  └──────────┘ └──────────┘ └──────────┘                                │  │  │    │
│  │  │  └─────────────────────────────────────────────────────────────────────────┘  │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────────────────────────────────────────────────────────────┐  │  │    │
│  │  │  │  PLATFORM & ADMIN                                                       │  │  │    │
│  │  │  │  ┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │  │    │
│  │  │  │  │leaderboards  │ │ progress │ │  admin   │ │  audit   │ │  tutor   │  │  │  │    │
│  │  │  │  │ Rankings     │ │ Tracking │ │ Dashboard│ │ Action   │ │ AI help  │  │  │  │    │
│  │  │  │  │              │ │          │ │ Mgmt     │ │ logging  │ │          │  │  │  │    │
│  │  │  │  └──────────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │  │    │
│  │  │  │  ┌──────────────┐                                                       │  │  │    │
│  │  │  │  │announcements │                                                       │  │  │    │
│  │  │  │  │ System msgs  │                                                       │  │  │    │
│  │  │  │  └──────────────┘                                                       │  │  │    │
│  │  │  └─────────────────────────────────────────────────────────────────────────┘  │  │    │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                     │    │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │    │
│  │  │  INFRASTRUCTURE LAYER  (app/infrastructure/)                                   │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────────────────┐  │  │    │
│  │  │  │  database/       │  │  repositories/  │  │  external/                   │  │  │    │
│  │  │  │  ├─ base.py      │  │  └─ BaseRepo    │  │  ├─ base.py (ABC)            │  │  │    │
│  │  │  │  │  (Declarative │  │     Generic[M]  │  │  ├─ google_oauth.py          │  │  │    │
│  │  │  │  │   Base)       │  │     CRUD ops    │  │  ├─ smtp_otp_sender.py       │  │  │    │
│  │  │  │  ├─ session.py   │  │                 │  │  └─ offline_otp_writer.py    │  │  │    │
│  │  │  │  │  (Engine,     │  │                 │  │                              │  │  │    │
│  │  │  │  │   SessionLocal│  │                 │  │                              │  │  │    │
│  │  │  │  │   get_db dep) │  │                 │  │                              │  │  │    │
│  │  │  │  └─ pragmas.py   │  │                 │  │                              │  │  │    │
│  │  │  │    (WAL, FK=ON)  │  │                 │  │                              │  │  │    │
│  │  │  └─────────────────┘  └─────────────────┘  └──────────────────────────────┘  │  │    │
│  │  │                                                                               │  │    │
│  │  │  ┌─────────────────┐  ┌─────────────────────────────────────────────────────┐ │  │    │
│  │  │  │  security/       │  │  scheduler/ (APScheduler)                          │ │  │    │
│  │  │  │  ├─ jwt.py       │  │  ├─ cleanup_expired_otps (hourly)                  │ │  │    │
│  │  │  │  ├─ passwords.py │  │  └─ rotate_offline_otp_log (daily 00:05 UTC)       │ │  │    │
│  │  │  │  └─ rng.py       │  │                                                    │ │  │    │
│  │  │  └─────────────────┘  └─────────────────────────────────────────────────────┘ │  │    │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │    │
│  │                                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────────────────────┘    │
│                │                                                                            │
│                │  SQLAlchemy ORM                                                            │
│                ▼                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                         ╔═══════════════════════════════════╗                        │    │
│  │                         ║          DATA LAYER               ║                        │    │
│  │                         ╚═══════════════════════════════════╝                        │    │
│  │                                                                                     │    │
│  │  ┌──────────────────────────────┐    ┌──────────────────────────────────────────┐   │    │
│  │  │  DATABASE                    │    │  SEED CONTENT (data/seed/)               │   │    │
│  │  │                              │    │                                          │   │    │
│  │  │  DEV:  SQLite (data/cse.db)  │    │  lessons/                               │   │    │
│  │  │  PROD: PostgreSQL (Supabase) │    │  ├─ verbal-ability/ (23 subtopics)      │   │    │
│  │  │                              │    │  ├─ numerical-ability/ (24 subtopics)   │   │    │
│  │  │  Pool: 5 + 10 overflow       │    │  └─ analytical-ability/ (13 subtopics) │   │    │
│  │  │  SSL: required (prod)        │    │                                          │   │    │
│  │  │  pre_ping: True              │    │  questions/                              │   │    │
│  │  │                              │    │  └─ 600 per subtopic (200 E/M/H)        │   │    │
│  │  └──────────────────────────────┘    └──────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                         ╔═══════════════════════════════════╗                        │    │
│  │                         ║      EXTERNAL SERVICES            ║                        │    │
│  │                         ╚═══════════════════════════════════╝                        │    │
│  │                                                                                     │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐   │    │
│  │  │ Google OAuth   │  │ Brevo/Resend   │  │ cron-job.org   │  │ UptimeRobot     │   │    │
│  │  │ (Social login) │  │ (Email OTP)    │  │ (Keep-alive)   │  │ (Monitoring)    │   │    │
│  │  └────────────────┘  └────────────────┘  └────────────────┘  └─────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐    │
│  │                         ╔═══════════════════════════════════╗                        │    │
│  │                         ║      DEPLOYMENT (Zero-Cost)       ║                        │    │
│  │                         ╚═══════════════════════════════════╝                        │    │
│  │                                                                                     │    │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                        │    │
│  │  │ Render         │  │ Vercel         │  │ Supabase       │                        │    │
│  │  │ (Backend API)  │  │ (Frontend CDN) │  │ (PostgreSQL)   │                        │    │
│  │  │ Auto-deploy    │  │ Static deploys │  │ 500MB free     │                        │    │
│  │  │ from GitHub    │  │ Global CDN     │  │ Session pooler │                        │    │
│  │  └────────────────┘  └────────────────┘  └────────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║  REQUEST FLOW (single feature slice example: Content)                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

  Client GET /v1/modules
       │
       ▼
  ┌─────────────┐     ┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
  │   CORS      │ ──► │    Auth     │ ──► │ Security Headers │ ──► │ Request Logging │
  │ (preflight) │     │ (decode JWT)│     │ (HSTS, CSP, etc) │     │ (X-Request-ID)  │
  └─────────────┘     └─────────────┘     └──────────────────┘     └────────┬────────┘
                                                                             │
       ┌─────────────────────────────────────────────────────────────────────┘
       ▼
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │  ROUTER (content/router.py)                                                     │
  │  @router.get("/modules")                                                        │
  │  def list_modules(pagination, user=Depends(require_no_active_mock), service)    │
  └──────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ Depends(get_module_service)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │  SERVICE (content/service.py)                                                   │
  │  ModuleService.list_for_user(user, skip, limit)                                 │
  │  - Business logic: category isolation, pagination                               │
  │  - Raises HTTPException on policy violations                                    │
  └──────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ self.module_repo.list(...)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │  REPOSITORY (content/repository.py extends BaseRepository[Module])              │
  │  ModuleRepository.list_by_category(category, skip, limit)                       │
  │  - SQLAlchemy ORM queries only                                                  │
  │  - No business logic                                                            │
  └──────────────────────────────────────┬──────────────────────────────────────────┘
                                         │ SQLAlchemy Session
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │  DATABASE                                                                       │
  │  SELECT * FROM modules WHERE category = ? LIMIT ? OFFSET ?                      │
  └─────────────────────────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║  CONTENT HIERARCHY (CSE Syllabus)                                                            ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

  Module (category: PROFESSIONAL | SUB_PROFESSIONAL)
    │
    ├── Verbal Ability
    │   ├── Grammar (10 subtopics)
    │   ├── Reading Comprehension (5 subtopics)
    │   └── Vocabulary Development (8 subtopics)
    │
    ├── Numerical Ability
    │   ├── Basic Operations (10 subtopics)
    │   ├── Percentages (8 subtopics)
    │   └── Ratio, Proportion & Average (6 subtopics)
    │
    └── Analytical Ability
        ├── Abstract Reasoning (subtopics)
        ├── Symbolic Logic (5 subtopics)
        └── Word Analogy (7 subtopics)

  Each Subtopic owns:
    ├── 1 Lesson (Markdown → JSON: sections, examples, key takeaways)
    └── 600 Questions (200 Easy + 200 Medium + 200 Hard)


╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║  TEST ARCHITECTURE                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

  tests/
  ├── conftest.py                    In-memory SQLite, function-scoped fixtures
  ├── features/
  │   └── <feature>/
  │       ├── test_repository.py     Real DB, no mocks
  │       ├── test_service.py        Mocked repository (MagicMock(spec=...))
  │       └── test_router.py         Mocked service, TestClient HTTP assertions
  ├── infrastructure/                Base repository, DB, security tests
  ├── common/                        Middleware, schema, dependency tests
  └── smoke/                         End-to-end API smoke tests

  Tools: pytest | httpx | pytest-mock | hypothesis (property-based)
```
