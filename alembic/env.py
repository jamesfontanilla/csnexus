"""Alembic environment configuration.

Imports all feature models so that ``Base.metadata`` reflects every table
for autogenerate support. Uses DATABASE_URL from the project's session module.
"""

from __future__ import annotations

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Import all models so Base.metadata is fully populated for autogenerate.
# ---------------------------------------------------------------------------
from app.infrastructure.database.base import Base  # noqa: E402

# Existing feature models
from app.features.users.models import User  # noqa: E402, F401
from app.features.content.models import Module, Topic, Subtopic, Lesson, Question, QuestionRejectionLog  # noqa: E402, F401
from app.features.quizzes.models import QuizAttempt, QuizAttemptAnswer  # noqa: E402, F401
from app.features.progress.models import LessonCompletion, UserTopicProgress, UserModuleProgress  # noqa: E402, F401
from app.features.xp.models import UserXP, XPEvent  # noqa: E402, F401
from app.features.mastery.models import UserSubtopicMastery, ReviewSchedule  # noqa: E402, F401
from app.features.gamification.models import (  # noqa: E402, F401
    UserDailyGoal,
    StreakFreeze,
    XPMultiplier,
    Tournament,
    TournamentParticipant,
    CompetenceMilestone,
    CompetenceMilestoneAward,
    StudyConsistency,
)
from app.features.mock_exams.models import MockExamConfig, MockExamAttempt, MockExamAttemptAnswer  # noqa: E402, F401
from app.features.flashcards.models import (  # noqa: E402, F401
    Deck,
    Flashcard,
    StudySession,
    ReviewLog,
    DeckRating,
    DeckBookmark,
    DeckComment,
    Follow,
    DeckReport,
    ExamSimulation,
    ExamSimulationAnswer,
    FlashcardNotification,
)
from app.features.focus.models import FocusSession  # noqa: E402, F401
from app.features.tutor.models import TutorInteraction  # noqa: E402, F401
from app.features.otp.models import OTP  # noqa: E402, F401
from app.features.audit.models import AuditLog  # noqa: E402, F401
from app.features.achievements.models import Achievement, UserAchievement  # noqa: E402, F401
from app.features.planner.models import OnboardingProfile, StudyPlan, StudyPlanDay  # noqa: E402, F401

# Intelligent Learning Engine models (new)
from app.features.readiness.models import ReadinessScoreHistory, SelfAssessmentRecord  # noqa: E402, F401
from app.features.smart_queue.models import DailyQueue, QueueItem  # noqa: E402, F401
from app.features.explanations.models import QuestionExplanation  # noqa: E402, F401
from app.features.mock_analytics.models import DiagnosticReport, RecommendationRecord  # noqa: E402, F401

# ---------------------------------------------------------------------------

target_metadata = Base.metadata

# Override sqlalchemy.url with the project's configured DATABASE_URL so that
# alembic commands don't require manual .ini edits.
from app.infrastructure.database.session import DATABASE_URL  # noqa: E402

config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures context with just a URL — no Engine needed.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
