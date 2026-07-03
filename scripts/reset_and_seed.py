"""Reset the database and seed baseline fixtures.

Drops the existing schema, recreates tables, and loads the minimal fixtures
needed to make the system runnable:
1. Users (admin + learners)
2. Achievements
3. Placeholder content hierarchy and mock exam configs

Usage:
    python scripts/reset_and_seed.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.infrastructure.database.session import SessionLocal, engine
from app.infrastructure.database.base import Base

# Import ALL models so Base.metadata knows every table before create_all
from app.features.users.models import User  # noqa: F401
from app.features.auth.models import Session as AuthSession, LoginAttempt, UserLockout  # noqa: F401
from app.features.otp.models import OTP  # noqa: F401
from app.features.content.models import Module, Topic, Subtopic, Lesson, Question, QuestionRejectionLog  # noqa: F401
from app.features.quizzes.models import QuizAttempt, QuizAttemptAnswer  # noqa: F401
from app.features.mock_exams.models import MockExamConfig, MockExamAttempt, MockExamAttemptAnswer  # noqa: F401
from app.features.progress.models import LessonCompletion, UserTopicProgress, UserModuleProgress  # noqa: F401
from app.features.xp.models import UserXP, XPEvent  # noqa: F401
from app.features.achievements.models import Achievement, UserAchievement  # noqa: F401
from app.features.audit.models import AuditLog  # noqa: F401
from app.features.tutor.models import TutorInteraction  # noqa: F401
from app.features.focus.models import FocusSession  # noqa: F401
from app.features.planner.models import StudyPlan, StudyPlanDay  # noqa: F401
from app.features.mastery.models import UserSubtopicMastery, ReviewSchedule  # noqa: F401
from app.features.gamification.models import UserDailyGoal, StreakFreeze, XPMultiplier, Tournament, TournamentParticipant  # noqa: F401
from app.features.announcements.models import Announcement, AnnouncementDismissal  # noqa: F401

from scripts.seed import seed_database


def main():
    # Recreate all tables (fresh start)
    # Use raw DROP SCHEMA CASCADE to avoid FK ordering issues on Postgres
    from sqlalchemy import text

    with engine.begin() as conn:
        if str(engine.url).startswith("sqlite"):
            Base.metadata.drop_all(bind=conn)
        else:
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
    Base.metadata.create_all(bind=engine)
    print("Database reset complete.")

    session = SessionLocal()
    try:
        # Run the base seed (users + achievements + placeholder content).
        result = seed_database(session)
        print(f"Base seed: {result.get('status', 'unknown')}")
        print("\nDone! Baseline fixtures are ready.")
        print("  Professional learner: learner-pro@cse.local / Learner1Pass!")
        print("  Sub-Professional learner: learner-sub@cse.local / Learner1Pass!")
        print("  Admin: admin@cse.local / Admin1Pass!")

    finally:
        session.close()


if __name__ == "__main__":
    main()
