"""Repository tests for MockAnalyticsRepository (Task 7.6).

Exercises all custom query methods against in-memory SQLite — no mocks,
per testing-standards.md. Each test seeds the required parent rows so
foreign-key constraints are honoured.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session

from app.features.content.models import (
    Difficulty,
    LevelScope,
    Module,
    Question,
    QuestionType,
    Subtopic,
    Topic,
)
from app.features.mock_analytics.models import DiagnosticReport, RecommendationRecord
from app.features.mock_analytics.repository import MockAnalyticsRepository
from app.features.mock_exams.models import (
    MockExamAttempt,
    MockExamAttemptAnswer,
    MockExamAttemptStatus,
    MockExamNavPolicy,
)
from app.features.users.models import Category
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate


# --- factories ---------------------------------------------------------------


def _make_user(db: Session, *, email: str = "tester@example.com") -> object:
    repo = UserRepository(db=db)
    username = email.split("@")[0].replace(".", "_")
    return repo.create(
        UserCreate(
            email=email,
            display_name="Tester",
            username=username,
            age=22,
            category=Category.PROFESSIONAL.value,
            password="Strong1Pass!",
        ),
        password_hash="bcrypt$fake$hash",
    )


def _seed_subtopic(db: Session, *, slug_prefix: str = "a") -> Subtopic:
    module = Module(
        category=Category.PROFESSIONAL.value,
        slug=f"mod-{slug_prefix}",
        title="Module",
        order_index=0,
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    topic = Topic(
        module_id=module.id,
        slug=f"top-{slug_prefix}",
        title="Topic",
        order_index=0,
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    subtopic = Subtopic(
        topic_id=topic.id,
        slug=f"sub-{slug_prefix}",
        title="Subtopic",
        order_index=0,
    )
    db.add(subtopic)
    db.commit()
    db.refresh(subtopic)
    return subtopic


def _seed_question(db: Session, subtopic: Subtopic, *, idx: int = 0) -> Question:
    q = Question(
        subtopic_id=subtopic.id,
        topic_id=subtopic.topic_id,
        module_id=1,
        category=Category.PROFESSIONAL.value,
        level_scope=LevelScope.MODULE.value,
        stem=f"Q{idx}?",
        options=["A", "B", "C", "D"],
        correct_answer="A",
        explanation="exp",
        difficulty=Difficulty.EASY.value,
        qtype=QuestionType.MULTIPLE_CHOICE.value,
        is_active=True,
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def _make_attempt(db: Session, user_id: int) -> MockExamAttempt:
    attempt = MockExamAttempt(
        user_id=user_id,
        category=Category.PROFESSIONAL.value,
        status=MockExamAttemptStatus.SUBMITTED.value,
        started_at=datetime.now(timezone.utc),
        submitted_at=datetime.now(timezone.utc),
        score=40,
        max_score=50,
        seed=123456,
        nav_policy=MockExamNavPolicy.FREE_NAV.value,
        time_limit_minutes=180,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


def _make_report(
    db: Session, user_id: int, attempt_id: int
) -> DiagnosticReport:
    report = DiagnosticReport(
        user_id=user_id,
        mock_exam_attempt_id=attempt_id,
        total_score=80.0,
        subtopic_breakdowns="[]",
        highest_impact_areas="[]",
        regression_alerts="[]",
        difficulty_performance="{}",
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def _make_recommendation(
    db: Session, report_id: int, subtopic_id: int, *, point_gain: float = 5.0
) -> RecommendationRecord:
    rec = RecommendationRecord(
        report_id=report_id,
        subtopic_id=subtopic_id,
        subtopic_name="Test Subtopic",
        current_accuracy=0.5,
        target_accuracy=0.8,
        estimated_point_gain=point_gain,
        recommended_action="practice",
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


# --- create_report -----------------------------------------------------------


def test_create_report_persists_and_returns(db_session: Session) -> None:
    user = _make_user(db_session)
    attempt = _make_attempt(db_session, user.id)
    repo = MockAnalyticsRepository(db=db_session)

    report = DiagnosticReport(
        user_id=user.id,
        mock_exam_attempt_id=attempt.id,
        total_score=75.5,
        subtopic_breakdowns='[{"id":1}]',
        highest_impact_areas='[{"id":1}]',
        regression_alerts="[]",
        difficulty_performance='{"easy":0.9}',
    )
    result = repo.create_report(report)

    assert result.id is not None
    assert result.total_score == 75.5
    assert result.user_id == user.id
    assert result.mock_exam_attempt_id == attempt.id
    assert result.generated_at is not None


# --- get_report --------------------------------------------------------------


def test_get_report_returns_report_by_attempt_id(db_session: Session) -> None:
    user = _make_user(db_session)
    attempt = _make_attempt(db_session, user.id)
    repo = MockAnalyticsRepository(db=db_session)
    _make_report(db_session, user.id, attempt.id)

    result = repo.get_report(attempt.id)

    assert result is not None
    assert result.mock_exam_attempt_id == attempt.id
    assert result.total_score == 80.0


def test_get_report_returns_none_when_not_found(db_session: Session) -> None:
    repo = MockAnalyticsRepository(db=db_session)
    assert repo.get_report(9999) is None


# --- get_recommendations -----------------------------------------------------


def test_get_recommendations_returns_sorted_by_point_gain(db_session: Session) -> None:
    user = _make_user(db_session)
    attempt = _make_attempt(db_session, user.id)
    report = _make_report(db_session, user.id, attempt.id)
    sub = _seed_subtopic(db_session, slug_prefix="rec")

    _make_recommendation(db_session, report.id, sub.id, point_gain=3.0)
    _make_recommendation(db_session, report.id, sub.id, point_gain=9.0)
    _make_recommendation(db_session, report.id, sub.id, point_gain=6.0)

    repo = MockAnalyticsRepository(db=db_session)
    recs = repo.get_recommendations(report.id)

    assert len(recs) == 3
    assert recs[0].estimated_point_gain == 9.0
    assert recs[1].estimated_point_gain == 6.0
    assert recs[2].estimated_point_gain == 3.0


def test_get_recommendations_returns_empty_list_for_no_recs(db_session: Session) -> None:
    repo = MockAnalyticsRepository(db=db_session)
    assert repo.get_recommendations(9999) == []


# --- accept_recommendation ---------------------------------------------------


def test_accept_recommendation_sets_timestamp(db_session: Session) -> None:
    user = _make_user(db_session)
    attempt = _make_attempt(db_session, user.id)
    report = _make_report(db_session, user.id, attempt.id)
    sub = _seed_subtopic(db_session, slug_prefix="acc")
    rec = _make_recommendation(db_session, report.id, sub.id)

    assert rec.accepted_at is None

    repo = MockAnalyticsRepository(db=db_session)
    result = repo.accept_recommendation(rec.id)

    assert result is not None
    assert result.accepted_at is not None


def test_accept_recommendation_returns_none_for_missing(db_session: Session) -> None:
    repo = MockAnalyticsRepository(db=db_session)
    assert repo.accept_recommendation(9999) is None


# --- get_historical_accuracy -------------------------------------------------


def test_get_historical_accuracy_computes_per_subtopic(db_session: Session) -> None:
    user = _make_user(db_session)
    sub_a = _seed_subtopic(db_session, slug_prefix="ha")
    sub_b = _seed_subtopic(db_session, slug_prefix="hb")

    q1 = _seed_question(db_session, sub_a, idx=0)
    q2 = _seed_question(db_session, sub_a, idx=1)
    q3 = _seed_question(db_session, sub_b, idx=2)

    attempt = _make_attempt(db_session, user.id)

    # sub_a: 1 correct, 1 wrong -> 0.5
    db_session.add(MockExamAttemptAnswer(
        attempt_id=attempt.id, question_id=q1.id, ordinal=1,
        selected_answer="A", is_correct=True,
        answered_at=datetime.now(timezone.utc),
    ))
    db_session.add(MockExamAttemptAnswer(
        attempt_id=attempt.id, question_id=q2.id, ordinal=2,
        selected_answer="B", is_correct=False,
        answered_at=datetime.now(timezone.utc),
    ))
    # sub_b: 1 correct -> 1.0
    db_session.add(MockExamAttemptAnswer(
        attempt_id=attempt.id, question_id=q3.id, ordinal=3,
        selected_answer="A", is_correct=True,
        answered_at=datetime.now(timezone.utc),
    ))
    db_session.commit()

    repo = MockAnalyticsRepository(db=db_session)
    accuracy = repo.get_historical_accuracy(user.id)

    assert sub_a.id in accuracy
    assert sub_b.id in accuracy
    assert accuracy[sub_a.id] == pytest.approx(0.5)
    assert accuracy[sub_b.id] == pytest.approx(1.0)


def test_get_historical_accuracy_excludes_in_progress_attempts(db_session: Session) -> None:
    user = _make_user(db_session)
    sub = _seed_subtopic(db_session, slug_prefix="ip")
    q = _seed_question(db_session, sub, idx=0)

    # Create an IN_PROGRESS attempt (not completed)
    attempt = MockExamAttempt(
        user_id=user.id,
        category=Category.PROFESSIONAL.value,
        status="IN_PROGRESS",
        started_at=datetime.now(timezone.utc),
        score=None,
        max_score=50,
        seed=999,
        nav_policy=MockExamNavPolicy.FREE_NAV.value,
        time_limit_minutes=180,
    )
    db_session.add(attempt)
    db_session.commit()
    db_session.refresh(attempt)

    db_session.add(MockExamAttemptAnswer(
        attempt_id=attempt.id, question_id=q.id, ordinal=1,
        selected_answer="A", is_correct=True,
        answered_at=datetime.now(timezone.utc),
    ))
    db_session.commit()

    repo = MockAnalyticsRepository(db=db_session)
    accuracy = repo.get_historical_accuracy(user.id)

    # Should be empty since the attempt is not COMPLETED
    assert accuracy == {}


def test_get_historical_accuracy_returns_empty_for_no_data(db_session: Session) -> None:
    user = _make_user(db_session)
    repo = MockAnalyticsRepository(db=db_session)
    assert repo.get_historical_accuracy(user.id) == {}
