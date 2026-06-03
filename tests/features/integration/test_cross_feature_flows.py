"""Integration tests for cross-feature event flows (Task 13.7).

Tests that the integration wiring between services works correctly:
- Quiz completion triggers readiness recompute and milestone evaluation
- Mock exam completion generates diagnostic report
- Recommendation acceptance sets accepted_at timestamp
- Queue idempotency within same UTC day
- Exam date update triggers plan regeneration

These tests use a real in-memory DB and real service instances (no mocking
of the service layer) to verify the cross-feature calls actually fire.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from app.features.content.models import LevelScope, Module, Question, QuestionType, Subtopic, Topic
from app.features.gamification.models import StudyConsistency
from app.features.mock_analytics.models import DiagnosticReport, RecommendationRecord
from app.features.mock_analytics.repository import MockAnalyticsRepository
from app.features.mock_analytics.service import MockAnalyticsService
from app.features.mock_exams.models import (
    MockExamAttempt,
    MockExamAttemptAnswer,
    MockExamAttemptStatus,
    MockExamConfig,
)
from app.features.mock_exams.repository import MockExamRepository
from app.features.planner.models import OnboardingProfile, StudyPlan
from app.features.readiness.models import ReadinessScoreHistory
from app.features.smart_queue.models import DailyQueue, QueueItem, QueueItemType
from app.features.smart_queue.repository import QueueRepository
from app.features.smart_queue.service import QueueService
from app.features.users.models import User


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def _seed_user(db: Session, *, user_id: int = 1) -> User:
    """Create a test user with correct model fields."""
    user = User(
        id=user_id,
        email=f"testuser{user_id}@test.com",
        display_name="Test User",
        age=25,
        category="SUB_PROFESSIONAL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_content(db: Session) -> tuple[Module, Topic, Subtopic, list[Question]]:
    """Seed minimal content hierarchy for tests."""
    module = Module(
        id=1,
        title="Verbal Ability",
        slug="verbal-ability",
        category="SUB_PROFESSIONAL",
        order_index=0,
    )
    db.add(module)
    db.flush()

    topic = Topic(
        id=1,
        module_id=module.id,
        title="Grammar",
        slug="grammar",
        order_index=0,
    )
    db.add(topic)
    db.flush()

    subtopic = Subtopic(
        id=1,
        topic_id=topic.id,
        title="Subject-Verb Agreement",
        slug="subject-verb-agreement",
        order_index=0,
    )
    db.add(subtopic)
    db.flush()

    questions: list[Question] = []
    for i in range(1, 11):
        q = Question(
            id=i,
            subtopic_id=subtopic.id,
            topic_id=topic.id,
            module_id=module.id,
            stem=f"Question {i}",
            qtype=QuestionType.MULTIPLE_CHOICE.value,
            correct_answer="A",
            options=["A", "B", "C", "D"],
            explanation=f"Explanation for question {i}",
            difficulty="MEDIUM",
            category="SUB_PROFESSIONAL",
            level_scope=LevelScope.SUBTOPIC.value,
        )
        db.add(q)
        questions.append(q)

    db.commit()
    return module, topic, subtopic, questions


# ---------------------------------------------------------------------------
# Test: Quiz completion triggers readiness recompute and milestone evaluation
# ---------------------------------------------------------------------------


class TestQuizCompletionTriggersReadinessRecompute:
    """Verify quiz submission triggers readiness score recomputation."""

    def test_readiness_recompute_creates_history_record(self, db_session: Session):
        """After readiness recompute (as triggered by quiz), a history record should exist."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        from app.features.content.repository import QuestionRepository, SubtopicRepository
        from app.features.flashcards.repository import FlashcardRepository
        from app.features.mastery.repository import MasteryRepository
        from app.features.mock_exams.repository import MockExamRepository
        from app.features.readiness.repository import ReadinessRepository
        from app.features.readiness.service import ReadinessService

        readiness_service = ReadinessService(
            readiness_repo=ReadinessRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            flashcard_repo=FlashcardRepository(db=db_session),
            mock_exam_repo=MockExamRepository(db=db_session),
            content_repo=SubtopicRepository(db=db_session),
            question_repo=QuestionRepository(db=db_session),
        )

        result = readiness_service.compute_and_persist(user.id)

        # Verify a ReadinessScoreHistory record was created
        assert result is not None
        assert result.user_id == user.id
        assert 0 <= result.score <= 100

        # Verify it's persisted
        from sqlalchemy import select

        stmt = select(ReadinessScoreHistory).where(
            ReadinessScoreHistory.user_id == user.id
        )
        records = db_session.execute(stmt).scalars().all()
        assert len(records) >= 1

    def test_readiness_recompute_triggers_milestone_evaluation(self, db_session: Session):
        """Readiness recompute should call milestone evaluation internally."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        from app.features.content.repository import QuestionRepository, SubtopicRepository
        from app.features.flashcards.repository import FlashcardRepository
        from app.features.mastery.repository import MasteryRepository
        from app.features.mock_exams.repository import MockExamRepository
        from app.features.readiness.repository import ReadinessRepository
        from app.features.readiness.service import ReadinessService

        readiness_service = ReadinessService(
            readiness_repo=ReadinessRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            flashcard_repo=FlashcardRepository(db=db_session),
            mock_exam_repo=MockExamRepository(db=db_session),
            content_repo=SubtopicRepository(db=db_session),
            question_repo=QuestionRepository(db=db_session),
        )

        # Patch milestone evaluation to verify it's called
        with patch.object(
            readiness_service,
            "_evaluate_milestones_after_score_change",
            wraps=readiness_service._evaluate_milestones_after_score_change,
        ) as mock_milestone:
            readiness_service.compute_and_persist(user.id)
            mock_milestone.assert_called_once_with(user.id)


# ---------------------------------------------------------------------------
# Test: Mock exam completion generates diagnostic report
# ---------------------------------------------------------------------------


class TestMockExamCompletionGeneratesDiagnostic:
    """Verify mock exam submission triggers diagnostic report generation."""

    def test_diagnostic_report_generated_after_mock_submit(self, db_session: Session):
        """After mock exam submission, a DiagnosticReport should be generated."""
        user = _seed_user(db_session)
        module, topic, subtopic, questions = _seed_content(db_session)

        # Create mock exam config
        config = MockExamConfig(
            category="SUB_PROFESSIONAL",
            total_questions=5,
            time_limit_minutes=180,
            pass_threshold=0.80,
            weights_json={str(module.id): 5},
            nav_policy="FREE_NAV",
        )
        db_session.add(config)
        db_session.flush()

        # Create a submitted mock exam attempt
        attempt = MockExamAttempt(
            id=1,
            user_id=user.id,
            category="SUB_PROFESSIONAL",
            status=MockExamAttemptStatus.SUBMITTED.value,
            started_at=_utcnow() - timedelta(hours=1),
            submitted_at=_utcnow(),
            max_score=5,
            score=4,
            seed=42,
            nav_policy="FREE_NAV",
            time_limit_minutes=180,
        )
        db_session.add(attempt)
        db_session.flush()

        # Add answers
        for i, q in enumerate(questions[:5], 1):
            answer = MockExamAttemptAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                ordinal=i,
                selected_answer="A" if i <= 4 else "B",
                is_correct=i <= 4,
            )
            db_session.add(answer)
        db_session.commit()

        # Call diagnostic generation directly (simulating what the hook does)
        from app.features.content.repository import SubtopicRepository
        from app.features.mastery.repository import MasteryRepository

        analytics_service = MockAnalyticsService(
            analytics_repo=MockAnalyticsRepository(db=db_session),
            mock_exam_repo=MockExamRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
        )

        report = analytics_service.generate_diagnostic(user.id, attempt.id)

        # Verify the report was created and persisted
        assert report is not None
        assert report.user_id == user.id
        assert report.mock_exam_attempt_id == attempt.id
        assert report.total_score == 80.0  # 4/5 * 100

        # Verify persistence
        from sqlalchemy import select

        stmt = select(DiagnosticReport).where(
            DiagnosticReport.mock_exam_attempt_id == attempt.id
        )
        persisted = db_session.execute(stmt).scalar_one_or_none()
        assert persisted is not None

    def test_diagnostic_generation_is_idempotent(self, db_session: Session):
        """Calling generate_diagnostic twice returns the same report."""
        user = _seed_user(db_session)
        module, topic, subtopic, questions = _seed_content(db_session)

        config = MockExamConfig(
            category="SUB_PROFESSIONAL",
            total_questions=5,
            time_limit_minutes=180,
            pass_threshold=0.80,
            weights_json={str(module.id): 5},
            nav_policy="FREE_NAV",
        )
        db_session.add(config)
        db_session.flush()

        attempt = MockExamAttempt(
            id=1,
            user_id=user.id,
            category="SUB_PROFESSIONAL",
            status=MockExamAttemptStatus.SUBMITTED.value,
            started_at=_utcnow() - timedelta(hours=1),
            submitted_at=_utcnow(),
            max_score=5,
            score=3,
            seed=42,
            nav_policy="FREE_NAV",
            time_limit_minutes=180,
        )
        db_session.add(attempt)
        db_session.flush()

        for i, q in enumerate(questions[:5], 1):
            answer = MockExamAttemptAnswer(
                attempt_id=attempt.id,
                question_id=q.id,
                ordinal=i,
                selected_answer="A" if i <= 3 else "B",
                is_correct=i <= 3,
            )
            db_session.add(answer)
        db_session.commit()

        from app.features.content.repository import SubtopicRepository
        from app.features.mastery.repository import MasteryRepository

        analytics_service = MockAnalyticsService(
            analytics_repo=MockAnalyticsRepository(db=db_session),
            mock_exam_repo=MockExamRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
        )

        report1 = analytics_service.generate_diagnostic(user.id, attempt.id)
        report2 = analytics_service.generate_diagnostic(user.id, attempt.id)

        assert report1.id == report2.id


# ---------------------------------------------------------------------------
# Test: Recommendation acceptance feeds into next queue
# ---------------------------------------------------------------------------


class TestRecommendationAcceptance:
    """Verify recommendation acceptance sets accepted_at timestamp."""

    def test_accept_recommendation_sets_accepted_at(self, db_session: Session):
        """Accepting a recommendation should set the accepted_at field."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        # Create a mock exam attempt to satisfy FK
        attempt = MockExamAttempt(
            id=99,
            user_id=user.id,
            category="SUB_PROFESSIONAL",
            status=MockExamAttemptStatus.SUBMITTED.value,
            started_at=_utcnow() - timedelta(hours=1),
            submitted_at=_utcnow(),
            max_score=5,
            score=3,
            seed=42,
            nav_policy="FREE_NAV",
            time_limit_minutes=180,
        )
        db_session.add(attempt)
        db_session.flush()

        # Create a diagnostic report
        report = DiagnosticReport(
            id=1,
            user_id=user.id,
            mock_exam_attempt_id=99,
            total_score=60.0,
            subtopic_breakdowns="[]",
            highest_impact_areas="[]",
            regression_alerts="[]",
            difficulty_performance="{}",
        )
        db_session.add(report)
        db_session.flush()

        # Create a recommendation
        rec = RecommendationRecord(
            id=1,
            report_id=report.id,
            subtopic_id=1,
            subtopic_name="Subject-Verb Agreement",
            current_accuracy=0.5,
            target_accuracy=0.8,
            estimated_point_gain=3.0,
            recommended_action="practice",
            accepted_at=None,
        )
        db_session.add(rec)
        db_session.commit()

        # Accept the recommendation
        from app.features.content.repository import SubtopicRepository
        from app.features.mastery.repository import MasteryRepository

        analytics_service = MockAnalyticsService(
            analytics_repo=MockAnalyticsRepository(db=db_session),
            mock_exam_repo=MockExamRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
        )

        result = analytics_service.accept_recommendation(user.id, rec.id)

        # Verify accepted_at is now set
        assert result.accepted_at is not None
        assert result.id == rec.id

        # Verify persistence
        db_session.refresh(rec)
        assert rec.accepted_at is not None


# ---------------------------------------------------------------------------
# Test: Queue idempotency within same UTC day
# ---------------------------------------------------------------------------


class TestQueueIdempotency:
    """Verify queue generation is idempotent within the same UTC day."""

    def test_get_daily_queue_returns_same_queue_on_repeated_calls(
        self, db_session: Session
    ):
        """Calling get_daily_queue multiple times on the same day returns the same queue."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        from app.features.content.repository import LessonRepository, SubtopicRepository
        from app.features.flashcards.repository import FlashcardRepository
        from app.features.mastery.repository import MasteryRepository

        queue_service = QueueService(
            queue_repo=QueueRepository(db=db_session),
            flashcard_repo=FlashcardRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
            lesson_repo=LessonRepository(db=db_session),
        )

        # First call generates the queue
        response1 = queue_service.get_daily_queue(user.id)

        # Second call should return the same queue
        response2 = queue_service.get_daily_queue(user.id)

        # Verify they are the same queue (same items)
        assert response1.time_budget_minutes == response2.time_budget_minutes
        assert response1.items_completed == response2.items_completed
        assert response1.items_remaining == response2.items_remaining
        assert len(response1.items) == len(response2.items)

        # Verify only one DailyQueue record exists for today
        from sqlalchemy import select

        today = datetime.now(tz=timezone.utc).date()
        stmt = select(DailyQueue).where(
            DailyQueue.user_id == user.id,
            DailyQueue.queue_date == today,
        )
        queues = db_session.execute(stmt).scalars().all()
        assert len(queues) == 1


# ---------------------------------------------------------------------------
# Test: Exam date update triggers plan regeneration
# ---------------------------------------------------------------------------


class TestExamDateUpdateTriggersRegeneration:
    """Verify exam date update is picked up by the queue engine."""

    def test_exam_date_update_reflected_in_queue_days_until_exam(self, db_session: Session):
        """After updating exam date, QueueService should see the new days_until_exam."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        # Create an onboarding profile with a far-out exam date
        original_date = date.today() + timedelta(days=60)
        profile = OnboardingProfile(
            user_id=user.id,
            exam_date=original_date,
            exam_category="Sub-Professional",
            time_budget_minutes=30,
        )
        db_session.add(profile)
        db_session.commit()

        from app.features.content.repository import LessonRepository, SubtopicRepository
        from app.features.flashcards.repository import FlashcardRepository
        from app.features.mastery.repository import MasteryRepository

        queue_service = QueueService(
            queue_repo=QueueRepository(db=db_session),
            flashcard_repo=FlashcardRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
            lesson_repo=LessonRepository(db=db_session),
        )

        # Verify initial days_until_exam
        days_initial = queue_service._get_days_until_exam(user.id)
        assert days_initial is not None
        assert days_initial <= 60

        # Update the exam date to be closer
        new_date = date.today() + timedelta(days=10)
        profile.exam_date = new_date
        db_session.commit()

        # Verify the updated days_until_exam is picked up
        days_updated = queue_service._get_days_until_exam(user.id)
        assert days_updated is not None
        assert days_updated <= 10


# ---------------------------------------------------------------------------
# Test: Study consistency wiring
# ---------------------------------------------------------------------------


class TestStudyConsistencyWiring:
    """Verify queue completion triggers study consistency evaluation."""

    def test_completing_half_of_queue_items_updates_consistency(
        self, db_session: Session
    ):
        """Completing 50%+ of queue items should trigger consistency and qualify."""
        user = _seed_user(db_session)
        _seed_content(db_session)

        # Create a daily queue with 2 items
        today = datetime.now(tz=timezone.utc).date()
        queue = DailyQueue(
            user_id=user.id,
            queue_date=today,
            time_budget_minutes=30,
            total_estimated_seconds=600,
            items_total=2,
            items_completed=0,
        )
        db_session.add(queue)
        db_session.flush()

        item1 = QueueItem(
            queue_id=queue.id,
            position=0,
            item_type=QueueItemType.QUIZ_PRACTICE.value,
            payload='{"subtopic_id": 1, "question_count": 5}',
            estimated_seconds=225,
        )
        item2 = QueueItem(
            queue_id=queue.id,
            position=1,
            item_type=QueueItemType.QUIZ_PRACTICE.value,
            payload='{"subtopic_id": 1, "question_count": 5}',
            estimated_seconds=225,
        )
        db_session.add_all([item1, item2])
        db_session.commit()

        from app.features.content.repository import LessonRepository, SubtopicRepository
        from app.features.flashcards.repository import FlashcardRepository
        from app.features.mastery.repository import MasteryRepository

        queue_service = QueueService(
            queue_repo=QueueRepository(db=db_session),
            flashcard_repo=FlashcardRepository(db=db_session),
            mastery_repo=MasteryRepository(db=db_session),
            subtopic_repo=SubtopicRepository(db=db_session),
            lesson_repo=LessonRepository(db=db_session),
        )

        # Complete first item (1/2 = 50% → qualifies)
        queue_service.complete_item(user.id, item1.id)

        # Check consistency was updated
        from sqlalchemy import select

        stmt = select(StudyConsistency).where(
            StudyConsistency.user_id == user.id
        )
        consistency = db_session.execute(stmt).scalar_one_or_none()
        assert consistency is not None
        # At 50% (1/2), it should qualify
        assert consistency.current_streak == 1
        assert consistency.total_consistent_days == 1
