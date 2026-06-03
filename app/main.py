"""FastAPI application entrypoint.

This module exposes the ``app`` object that ``uvicorn app.main:app`` resolves
to. It wires middlewares, exception handlers, and all feature routers.

Middleware add-order matters: Starlette processes middlewares in reverse-add
order (last-added runs first). We add logging first, then auth, so the
request flow is: logging → auth → route handler.

Setting ``DISABLE_SCHEDULER=1`` in the environment makes ``start_scheduler``
a no-op; the test suite sets this in ``conftest.py`` so timers do not run
during unit tests.
"""

from __future__ import annotations

# Load .env file if present (development convenience — production uses real env vars)
from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.common.middlewares.auth import AuthMiddleware
from app.common.middlewares.error_handler import register_exception_handlers
from app.common.middlewares.logging import RequestLoggingMiddleware
from app.common.middlewares.rate_limit import limiter
from app.common.middlewares.security_headers import SecurityHeadersMiddleware
from app.features.achievements.router import router as achievement_router
from app.features.admin.router import router as admin_router
from app.features.audit.router import router as audit_router
from app.features.mastery.router import router as mastery_router
from app.features.auth.router import router as auth_router
from app.features.content.router import router as content_router
from app.features.gamification.router import router as gamification_router
from app.features.gamification.milestone_router import router as milestone_router
from app.features.tutor.router import router as tutor_router
from app.features.focus.router import router as focus_router
from app.features.explanations.router import router as explanations_router
from app.features.flashcards.router import router as flashcard_router
from app.features.planner.router import router as planner_router
from app.features.planner.onboarding_router import router as onboarding_router
from app.features.leaderboards.router import router as leaderboard_router
from app.features.mock_exams.router import router as mock_exam_router
from app.features.mock_analytics.router import router as mock_analytics_router
from app.features.otp.router import router as otp_router
from app.features.progress.router import router as progress_router
from app.features.quizzes.router import router as quiz_router
from app.features.readiness.router import router as readiness_router
from app.features.smart_queue.router import router as smart_queue_router
from app.features.users.router import router as users_router
from app.features.xp.router import router as xp_router
from app.features.pretesting.router import router as pretest_router
from app.features.learning_techniques.router import router as learning_techniques_router
from app.infrastructure.scheduler.jobs import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Start the scheduler on app boot, auto-seed if DB is empty."""

    # Ensure tables exist and seed if empty (handles ephemeral deploys
    # like Render free tier where the SQLite file is wiped on restart).
    from app.infrastructure.database.base import Base
    from app.infrastructure.database.session import SessionLocal, engine

    try:
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()
        try:
            from app.features.users.models import User

            import os
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@cse.local")
            admin_exists = session.query(User).filter(
                User.email == admin_email
            ).first()
            if admin_exists is None:
                from scripts.seed import seed_database

                seed_database(session)

            # Always run content seed — it's non-destructive (skips existing
            # content by slug) so it's safe on every boot. This ensures new
            # lessons/questions added to data/seed/ land in production
            # automatically on the next deploy.
            from scripts.seed_all_content import main as seed_all_content

            seed_all_content()
        finally:
            session.close()
    except Exception as exc:
        import logging

        logging.getLogger(__name__).error(
            "DB initialization failed (app will still boot): %s", exc
        )
        # Non-fatal: app boots without DB init. Endpoints that need the DB
        # will fail individually, but /health will still respond.

    # --- Build CrossLessonRegistry once at startup (Req 4.1, 4.2) ----------
    # Avoids per-request DB queries for concept lookup. The registry is
    # stored on app.state and exposed via get_cross_lesson_registry dep.
    from app.features.tutor.algorithms.cross_lesson_registry import (
        CrossLessonRegistry,
    )

    try:
        session = SessionLocal()
        try:
            from app.features.content.models import Lesson, Subtopic

            lessons_with_subtopics = (
                session.query(Lesson.content_json, Lesson.subtopic_id, Subtopic.title)
                .join(Subtopic, Lesson.subtopic_id == Subtopic.id)
                .all()
            )
            lesson_dicts: list[dict] = []
            for content_json, subtopic_id, subtopic_title in lessons_with_subtopics:
                entry = dict(content_json) if content_json else {}
                entry["subtopic_id"] = subtopic_id
                entry["subtopic_title"] = subtopic_title
                lesson_dicts.append(entry)

            app.state.cross_lesson_registry = CrossLessonRegistry.build_from_lessons(
                lesson_dicts
            )
        finally:
            session.close()
    except Exception as exc:
        import logging

        logging.getLogger(__name__).warning(
            "CrossLessonRegistry build failed (chat will work without cross-refs): %s",
            exc,
        )
        # Non-fatal: the engine handles registry=None gracefully (Req 4.7).
        app.state.cross_lesson_registry = CrossLessonRegistry()

    start_scheduler()
    try:
        yield
    finally:
        stop_scheduler()


app = FastAPI(lifespan=lifespan)

# Attach the rate limiter state to the app (required by slowapi).
app.state.limiter = limiter

# --- Middlewares -----------------------------------------------------------
# Starlette processes in reverse-add order: LAST added runs FIRST.
# We add CORS LAST so it runs FIRST and handles OPTIONS preflight
# before any other middleware touches the request.
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthMiddleware)

# --- CORS (added last = runs first) ----------------------------------------
import os

from fastapi.middleware.cors import CORSMiddleware

_ENV = os.environ.get("APP_ENV", "development")
_CORS_ORIGINS: list[str] = (
    ["https://csnexus.space", "https://www.csnexus.space"]
    if _ENV == "production"
    else ["https://csnexus.space", "https://www.csnexus.space", "http://localhost:5173"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception handlers ----------------------------------------------------
register_exception_handlers(app)

# slowapi 429 handler — returns the canonical ErrorResponse envelope.
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Feature routers -------------------------------------------------------
# Each router already carries its own prefix (e.g. /v1/auth, /v1, /v1/admin).
app.include_router(auth_router)
app.include_router(otp_router)
app.include_router(users_router)
app.include_router(content_router)
app.include_router(progress_router)
app.include_router(xp_router)
app.include_router(quiz_router)
app.include_router(mock_exam_router)
app.include_router(leaderboard_router)
app.include_router(achievement_router)
app.include_router(admin_router)
app.include_router(audit_router)
app.include_router(mastery_router)
app.include_router(gamification_router)
app.include_router(milestone_router)
app.include_router(tutor_router)
app.include_router(planner_router)
app.include_router(onboarding_router)
app.include_router(focus_router)
app.include_router(flashcard_router)
app.include_router(explanations_router)
app.include_router(readiness_router)
app.include_router(smart_queue_router)
app.include_router(mock_analytics_router)
app.include_router(pretest_router)
app.include_router(learning_techniques_router)


# --- Health probe ----------------------------------------------------------


@app.get("/health")
def health() -> dict[str, str]:
    """Unauthenticated health probe per ``api-standard.md``."""
    return {"status": "ok"}
