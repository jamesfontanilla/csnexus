"""Repository tests for ReadinessRepository.

Tests run against an in-memory SQLite database with no mocks, verifying
that ORM queries and filters work correctly.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy.orm import Session

from app.features.readiness.models import ReadinessScoreHistory
from app.features.readiness.repository import ReadinessRepository
from app.features.users.models import User


def _seed_user(db: Session, *, email: str = "readiness@test.com") -> User:
    """Create a minimal user to satisfy FK constraints."""
    user = User(
        email=email,
        display_name="Readiness Tester",
        age=25,
        category="PROFESSIONAL",
        role="LEARNER",
        account_state="VERIFIED",
        password_hash="$2b$10$fakehash",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_history_record(
    user_id: int,
    score: int = 72,
    mastery_component: float = 80.0,
    retention_component: float = 65.0,
    mock_component: float = 70.0,
    coverage_component: float = 50.0,
    weights_used: str = '{"mastery":0.4,"retention":0.25,"mock_exam":0.25,"coverage":0.1}',
    computed_at: datetime | None = None,
) -> ReadinessScoreHistory:
    """Factory for ReadinessScoreHistory with sensible defaults."""
    return ReadinessScoreHistory(
        user_id=user_id,
        score=score,
        mastery_component=mastery_component,
        retention_component=retention_component,
        mock_component=mock_component,
        coverage_component=coverage_component,
        weights_used=weights_used,
        computed_at=computed_at or datetime.now(timezone.utc),
    )


class TestCreate:
    """Tests for BaseRepository.create (inherited) with ReadinessScoreHistory."""

    def test_create_persists_record(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        record = _make_history_record(user_id=user.id)
        result = repo.create(record)

        assert result.id is not None
        assert result.score == 72
        assert result.user_id == user.id

    def test_create_stores_all_components(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        record = _make_history_record(
            user_id=user.id,
            mastery_component=85.5,
            retention_component=70.2,
            mock_component=60.0,
            coverage_component=40.0,
        )
        result = repo.create(record)

        assert result.mastery_component == 85.5
        assert result.retention_component == 70.2
        assert result.mock_component == 60.0
        assert result.coverage_component == 40.0


class TestGetLatest:
    """Tests for ReadinessRepository.get_latest."""

    def test_returns_most_recent_record(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create(_make_history_record(user_id=user.id, score=50, computed_at=now - timedelta(hours=2)))
        repo.create(_make_history_record(user_id=user.id, score=75, computed_at=now - timedelta(hours=1)))
        repo.create(_make_history_record(user_id=user.id, score=60, computed_at=now - timedelta(hours=3)))

        latest = repo.get_latest(user_id=user.id)
        assert latest is not None
        assert latest.score == 75

    def test_returns_none_when_no_records(self, db_session: Session) -> None:
        repo = ReadinessRepository(db=db_session)
        result = repo.get_latest(user_id=999)
        assert result is None

    def test_filters_by_user_id(self, db_session: Session) -> None:
        user1 = _seed_user(db_session, email="user1@test.com")
        user2 = _seed_user(db_session, email="user2@test.com")
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create(_make_history_record(user_id=user1.id, score=80, computed_at=now))
        repo.create(_make_history_record(user_id=user2.id, score=60, computed_at=now))

        result = repo.get_latest(user_id=user2.id)
        assert result is not None
        assert result.score == 60


class TestGetScoreAtDate:
    """Tests for ReadinessRepository.get_score_at_date."""

    def test_returns_latest_record_on_or_before_date(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        target = date(2024, 6, 10)

        # Record on target date
        repo.create(_make_history_record(
            user_id=user.id, score=65, computed_at=datetime(2024, 6, 10, 14, 0, 0)
        ))
        # Record before target date
        repo.create(_make_history_record(
            user_id=user.id, score=55, computed_at=datetime(2024, 6, 8, 10, 0, 0)
        ))
        # Record after target date (should be excluded)
        repo.create(_make_history_record(
            user_id=user.id, score=80, computed_at=datetime(2024, 6, 12, 10, 0, 0)
        ))

        result = repo.get_score_at_date(user_id=user.id, target_date=target)
        assert result is not None
        assert result.score == 65

    def test_returns_none_when_no_records_before_date(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        # Only a future record
        repo.create(_make_history_record(
            user_id=user.id, score=80, computed_at=datetime(2024, 6, 15, 10, 0, 0)
        ))

        result = repo.get_score_at_date(user_id=user.id, target_date=date(2024, 6, 10))
        assert result is None

    def test_returns_most_recent_before_date_when_multiple(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)

        repo.create(_make_history_record(
            user_id=user.id, score=50, computed_at=datetime(2024, 6, 5, 10, 0, 0)
        ))
        repo.create(_make_history_record(
            user_id=user.id, score=60, computed_at=datetime(2024, 6, 8, 16, 0, 0)
        ))

        result = repo.get_score_at_date(user_id=user.id, target_date=date(2024, 6, 10))
        assert result is not None
        assert result.score == 60


class TestGetTrend:
    """Tests for ReadinessRepository.get_trend."""

    def test_returns_records_within_date_range(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        # Within range (last 30 days)
        repo.create(_make_history_record(user_id=user.id, score=50, computed_at=now - timedelta(days=5)))
        repo.create(_make_history_record(user_id=user.id, score=60, computed_at=now - timedelta(days=10)))
        repo.create(_make_history_record(user_id=user.id, score=70, computed_at=now - timedelta(days=20)))

        # Outside range
        repo.create(_make_history_record(user_id=user.id, score=40, computed_at=now - timedelta(days=35)))

        records = repo.get_trend(user_id=user.id, days=30)
        assert len(records) == 3
        # Should be ordered ascending by computed_at
        assert records[0].score == 70  # oldest within range
        assert records[2].score == 50  # most recent within range

    def test_returns_empty_list_when_no_records(self, db_session: Session) -> None:
        repo = ReadinessRepository(db=db_session)
        result = repo.get_trend(user_id=999, days=30)
        assert result == []

    def test_respects_days_parameter(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create(_make_history_record(user_id=user.id, score=50, computed_at=now - timedelta(days=3)))
        repo.create(_make_history_record(user_id=user.id, score=60, computed_at=now - timedelta(days=10)))

        # Only 7 days: should return 1 record
        records = repo.get_trend(user_id=user.id, days=7)
        assert len(records) == 1
        assert records[0].score == 50

    def test_filters_by_user_id(self, db_session: Session) -> None:
        user1 = _seed_user(db_session, email="trend1@test.com")
        user2 = _seed_user(db_session, email="trend2@test.com")
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create(_make_history_record(user_id=user1.id, score=70, computed_at=now - timedelta(days=2)))
        repo.create(_make_history_record(user_id=user2.id, score=80, computed_at=now - timedelta(days=2)))

        records = repo.get_trend(user_id=user1.id, days=30)
        assert len(records) == 1
        assert records[0].score == 70
