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


def _ensure_auth_session_schema() -> None:
    """Patch auth session columns that ``create_all`` cannot add to old DBs."""

    from sqlalchemy import inspect, text

    from app.infrastructure.database.session import engine

    inspector = inspect(engine)
    if "sessions" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("sessions")}
    dialect = engine.dialect.name

    statements: list[str] = []
    if "refresh_jti" not in columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE sessions ADD COLUMN IF NOT EXISTS refresh_jti VARCHAR(64)"
            )
        else:
            statements.append("ALTER TABLE sessions ADD COLUMN refresh_jti VARCHAR(64)")

    if "refresh_expires_at" not in columns:
        if dialect == "postgresql":
            statements.append(
                "ALTER TABLE sessions ADD COLUMN IF NOT EXISTS refresh_expires_at TIMESTAMP WITH TIME ZONE"
            )
        else:
            statements.append(
                "ALTER TABLE sessions ADD COLUMN refresh_expires_at DATETIME"
            )

    index_names = {index["name"] for index in inspector.get_indexes("sessions")}
    if "ix_sessions_refresh_jti" not in index_names:
        statements.append(
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_sessions_refresh_jti "
            "ON sessions (refresh_jti)"
        )

    if not statements:
        return

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def _ensure_milestone_enrichment_schema() -> None:
    """Add milestone enrichment columns added in migration b3e1d5f9a2c8.

    Mirrors what the Alembic migration does but runs at startup via
    create_all / inspect so it works even when Alembic can't run
    (e.g. PgBouncer transaction-mode session poolers).
    """
    from sqlalchemy import inspect, text
    from app.infrastructure.database.session import engine

    inspector = inspect(engine)
    dialect = engine.dialect.name

    # 1. competence_milestones.xp_reward
    if "competence_milestones" in inspector.get_table_names():
        cols = {c["name"] for c in inspector.get_columns("competence_milestones")}
        if "xp_reward" not in cols:
            stmt = (
                "ALTER TABLE competence_milestones "
                "ADD COLUMN IF NOT EXISTS xp_reward INTEGER NOT NULL DEFAULT 0"
                if dialect == "postgresql"
                else "ALTER TABLE competence_milestones ADD COLUMN xp_reward INTEGER NOT NULL DEFAULT 0"
            )
            with engine.begin() as conn:
                conn.execute(text(stmt))

    # 2. competence_milestone_awards.seen_at
    if "competence_milestone_awards" in inspector.get_table_names():
        cols = {c["name"] for c in inspector.get_columns("competence_milestone_awards")}
        if "seen_at" not in cols:
            stmt = (
                "ALTER TABLE competence_milestone_awards "
                "ADD COLUMN IF NOT EXISTS seen_at TIMESTAMP WITH TIME ZONE"
                if dialect == "postgresql"
                else "ALTER TABLE competence_milestone_awards ADD COLUMN seen_at DATETIME"
            )
            with engine.begin() as conn:
                conn.execute(text(stmt))

    # 3. mastery_score_history table
    if "mastery_score_history" not in inspector.get_table_names():
        if dialect == "postgresql":
            stmt = """
                CREATE TABLE IF NOT EXISTS mastery_score_history (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    subtopic_id INTEGER NOT NULL REFERENCES subtopics(id) ON DELETE CASCADE,
                    mastery_score FLOAT NOT NULL,
                    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """
        else:
            stmt = """
                CREATE TABLE IF NOT EXISTS mastery_score_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    subtopic_id INTEGER NOT NULL REFERENCES subtopics(id) ON DELETE CASCADE,
                    mastery_score REAL NOT NULL,
                    recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        with engine.begin() as conn:
            conn.execute(text(stmt))
        # Create index separately
        with engine.begin() as conn:
            idx_stmt = (
                "CREATE INDEX IF NOT EXISTS ix_mastery_score_history_user_subtopic_recorded "
                "ON mastery_score_history (user_id, subtopic_id, recorded_at)"
                if dialect == "postgresql"
                else
                "CREATE INDEX IF NOT EXISTS ix_mastery_score_history_user_subtopic_recorded "
                "ON mastery_score_history (user_id, subtopic_id, recorded_at)"
            )
            conn.execute(text(idx_stmt))


def _ensure_question_difficulty_schema() -> None:
    """Patch the questions difficulty check so ``Ultra`` is accepted."""

    from sqlalchemy import inspect, text

    from app.infrastructure.database.session import engine

    inspector = inspect(engine)
    if "questions" not in inspector.get_table_names():
        return

    checks = inspector.get_check_constraints("questions")
    difficulty_check = next(
        (
            constraint
            for constraint in checks
            if constraint.get("name") == "ck_questions_difficulty"
        ),
        None,
    )
    if difficulty_check is not None and "ULTRA" in str(difficulty_check.get("sqltext", "")):
        return

    if engine.dialect.name == "postgresql":
        statements = [
            "ALTER TABLE questions DROP CONSTRAINT IF EXISTS ck_questions_difficulty",
            (
                "ALTER TABLE questions ADD CONSTRAINT ck_questions_difficulty "
                "CHECK (difficulty IN ('EASY', 'MEDIUM', 'HARD', 'ULTRA'))"
            ),
        ]
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))
        return

    if engine.dialect.name == "sqlite":
        with engine.begin() as connection:
            connection.exec_driver_sql("PRAGMA writable_schema = ON")
            try:
                result = connection.exec_driver_sql(
                    "UPDATE sqlite_master "
                    "SET sql = REPLACE(sql, ?, ?) "
                    "WHERE type = 'table' AND name = 'questions'",
                    (
                        "difficulty IN ('EASY', 'MEDIUM', 'HARD')",
                        "difficulty IN ('EASY', 'MEDIUM', 'HARD', 'ULTRA')",
                    ),
                )
                if result.rowcount == 0:
                    return
            finally:
                connection.exec_driver_sql("PRAGMA writable_schema = OFF")

        # Close pooled SQLite connections so the updated schema is reloaded.
        engine.dispose()
        return


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Start the scheduler on app boot, auto-seed if DB is empty."""

    # Ensure tables exist and seed if empty (handles ephemeral deploys
    # like Render free tier where the SQLite file is wiped on restart).
    from app.infrastructure.database.base import Base
    from app.infrastructure.database.session import SessionLocal, engine

    try:
        Base.metadata.create_all(bind=engine)
        _ensure_auth_session_schema()
        _ensure_question_difficulty_schema()
        _ensure_milestone_enrichment_schema()
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
