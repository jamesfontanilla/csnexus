"""Service tests for StudyConsistency tracking.

The ConsistencyService uses a SQLAlchemy session directly (no separate
repository), so tests run against the real in-memory DB per the project's
repository-test pattern.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from sqlalchemy.orm import Session

from app.features.gamification.consistency_service import ConsistencyService
from app.features.gamification.models import StudyConsistency
from app.features.users.models import User


def _seed_user(db: Session, user_id: int = 1) -> User:
    """Insert a minimal user row for FK satisfaction."""
    user = User(
        id=user_id,
        email=f"user{user_id}@test.com",
        display_name="Test User",
        age=25,
        category="PROFESSIONAL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class TestUpdateConsistency:
    """Tests for update_consistency — Req 14.1, 14.2."""

    def test_qualifying_day_increments_streak(self, db_session: Session) -> None:
        """≥50% completed qualifies the day (Req 14.1)."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)
        today = date(2025, 6, 15)

        result = service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=5,
            evaluation_date=today,
        )

        assert result.current_streak == 1
        assert result.total_consistent_days == 1
        assert result.last_qualifying_date == today

    def test_exactly_50_percent_qualifies(self, db_session: Session) -> None:
        """Boundary: exactly 50% qualifies."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.update_consistency(
            user_id=1,
            items_total=4,
            items_completed=2,
            evaluation_date=date(2025, 6, 15),
        )

        assert result.current_streak == 1

    def test_below_50_percent_does_not_qualify(self, db_session: Session) -> None:
        """Below 50% does not qualify."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=4,
            evaluation_date=date(2025, 6, 15),
        )

        assert result.current_streak == 0
        assert result.total_consistent_days == 0

    def test_zero_items_does_not_qualify(self, db_session: Session) -> None:
        """Zero total items (login only) does not qualify (Req 14.2)."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.update_consistency(
            user_id=1,
            items_total=0,
            items_completed=0,
            evaluation_date=date(2025, 6, 15),
        )

        assert result.current_streak == 0
        assert result.total_consistent_days == 0

    def test_zero_completed_does_not_qualify(self, db_session: Session) -> None:
        """Having items but completing none does not qualify (Req 14.2)."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=0,
            evaluation_date=date(2025, 6, 15),
        )

        assert result.current_streak == 0

    def test_consecutive_qualifying_days_build_streak(
        self, db_session: Session
    ) -> None:
        """Multiple consecutive qualifying days increase the streak."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        for i in range(5):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 10) + timedelta(days=i),
            )

        record = service.get_consistency(user_id=1)
        assert record.current_streak == 5
        assert record.longest_streak == 5
        assert record.total_consistent_days == 5

    def test_same_day_does_not_double_count(self, db_session: Session) -> None:
        """Calling update_consistency twice for the same day doesn't double count."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)
        today = date(2025, 6, 15)

        service.update_consistency(
            user_id=1, items_total=10, items_completed=6, evaluation_date=today
        )
        service.update_consistency(
            user_id=1, items_total=10, items_completed=8, evaluation_date=today
        )

        record = service.get_consistency(user_id=1)
        assert record.current_streak == 1
        assert record.total_consistent_days == 1


class TestStreakReset:
    """Tests for streak reset logic — Req 14.3."""

    def test_missed_day_resets_current_preserves_longest(
        self, db_session: Session
    ) -> None:
        """Missing a day resets current_streak but keeps longest_streak (Req 14.3)."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        # Build a 3-day streak
        for i in range(3):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 10) + timedelta(days=i),
            )

        record = service.get_consistency(user_id=1)
        assert record.current_streak == 3
        assert record.longest_streak == 3

        # Miss day 4, report on day 4 with below threshold
        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=2,
            evaluation_date=date(2025, 6, 13),
        )

        record = service.get_consistency(user_id=1)
        assert record.current_streak == 0
        assert record.longest_streak == 3  # preserved

    def test_gap_day_resets_streak_on_next_qualifying(
        self, db_session: Session
    ) -> None:
        """If there's a gap between qualifying days, streak resets then starts fresh."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        # Day 1 qualifies
        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 10),
        )
        # Skip day 2, qualify on day 3
        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 12),
        )

        record = service.get_consistency(user_id=1)
        # Streak resets due to gap, then new qualifying day = 1
        assert record.current_streak == 1
        assert record.longest_streak == 1
        assert record.total_consistent_days == 2

    def test_longest_streak_grows_with_new_record(
        self, db_session: Session
    ) -> None:
        """Longest streak updates when current exceeds it."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        # Build 2-day streak
        for i in range(2):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 10) + timedelta(days=i),
            )

        # Miss a day
        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=1,
            evaluation_date=date(2025, 6, 12),
        )

        # Build 4-day streak
        for i in range(4):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 13) + timedelta(days=i),
            )

        record = service.get_consistency(user_id=1)
        assert record.current_streak == 4
        assert record.longest_streak == 4


class TestCatchUpQueue:
    """Tests for catch-up queue adjustment info — Req 14.5."""

    def test_no_missed_days_returns_zero(self, db_session: Session) -> None:
        """No gap since last qualifying → 0 missed days."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 15),
        )

        missed = service.get_missed_days_since_last_qualifying(
            user_id=1, reference_date=date(2025, 6, 16)
        )
        assert missed == 0

    def test_missed_days_returns_gap_count(self, db_session: Session) -> None:
        """Two missed days → returns 2."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 10),
        )

        missed = service.get_missed_days_since_last_qualifying(
            user_id=1, reference_date=date(2025, 6, 13)
        )
        assert missed == 2

    def test_brand_new_user_returns_zero(self, db_session: Session) -> None:
        """No qualifying date at all → 0 (no catch-up for new users)."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        missed = service.get_missed_days_since_last_qualifying(
            user_id=1, reference_date=date(2025, 6, 15)
        )
        assert missed == 0

    def test_needs_catch_up_true_when_missed(self, db_session: Session) -> None:
        """needs_catch_up returns True when days were missed."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 10),
        )

        assert service.needs_catch_up(
            user_id=1, reference_date=date(2025, 6, 13)
        ) is True

    def test_needs_catch_up_false_when_consecutive(
        self, db_session: Session
    ) -> None:
        """needs_catch_up returns False when qualified yesterday."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        service.update_consistency(
            user_id=1,
            items_total=10,
            items_completed=8,
            evaluation_date=date(2025, 6, 14),
        )

        assert service.needs_catch_up(
            user_id=1, reference_date=date(2025, 6, 15)
        ) is False


class TestReplaceStreakWithConsistency:
    """Tests for migration — Req 14.6."""

    def test_preserves_existing_longest_streak(self, db_session: Session) -> None:
        """Migration preserves the old system's longest_streak."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.replace_streak_with_consistency(
            user_id=1, existing_longest_streak=15
        )

        assert result.longest_streak == 15
        assert result.current_streak == 0
        assert result.last_qualifying_date is None

    def test_keeps_higher_longest_streak(self, db_session: Session) -> None:
        """If new system already has higher longest_streak, keeps it."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        # Build a streak in the new system first
        for i in range(5):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 10) + timedelta(days=i),
            )

        # Migrate with lower old streak
        result = service.replace_streak_with_consistency(
            user_id=1, existing_longest_streak=3
        )

        assert result.longest_streak == 5  # new system's streak is higher

    def test_resets_current_streak_on_migration(self, db_session: Session) -> None:
        """Migration resets current_streak to start fresh with new metric."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        # Build a streak
        for i in range(3):
            service.update_consistency(
                user_id=1,
                items_total=10,
                items_completed=8,
                evaluation_date=date(2025, 6, 10) + timedelta(days=i),
            )

        result = service.replace_streak_with_consistency(
            user_id=1, existing_longest_streak=0
        )

        assert result.current_streak == 0
        assert result.last_qualifying_date is None

    def test_migration_for_new_user(self, db_session: Session) -> None:
        """Migration works for a user with no existing consistency record."""
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)

        result = service.replace_streak_with_consistency(
            user_id=1, existing_longest_streak=10
        )

        assert result.longest_streak == 10
        assert result.current_streak == 0
        assert result.total_consistent_days == 0
