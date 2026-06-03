"""Property-based tests for Study Consistency tracking.

Uses Hypothesis to validate universal correctness properties of the
ConsistencyService's qualification logic and streak preservation.

The ``db_session`` fixture is reused across generated examples (each example
operates on disjoint data after a reset). ``HealthCheck.function_scoped_fixture``
is suppressed for this reason.
"""

from __future__ import annotations

from datetime import date, timedelta

from hypothesis import HealthCheck, given, settings, assume
from hypothesis.strategies import (
    booleans,
    composite,
    integers,
    lists,
)
from sqlalchemy.orm import Session

from app.features.gamification.consistency_service import ConsistencyService
from app.features.gamification.models import StudyConsistency
from app.features.users.models import User


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

_PBT_SETTINGS = dict(
    max_examples=50,
    deadline=None,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.function_scoped_fixture,
    ],
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _reset_state(db: Session) -> None:
    """Clear rows from prior Hypothesis examples so the next one starts clean."""
    db.query(StudyConsistency).delete()
    db.query(User).delete()
    db.commit()


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


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------


@composite
def qualifying_day_inputs(draw):
    """Generate (items_total, items_completed) pairs where items_total > 0."""
    items_total = draw(integers(min_value=1, max_value=200))
    items_completed = draw(integers(min_value=0, max_value=items_total))
    return items_total, items_completed


@composite
def day_sequence(draw):
    """Generate a sequence of qualifying/non-qualifying day booleans (1-20 days)."""
    length = draw(integers(min_value=1, max_value=20))
    days = draw(lists(booleans(), min_size=length, max_size=length))
    return days


# ---------------------------------------------------------------------------
# Property 28: Study consistency qualifies on ≥50% queue completion
# Validates: Requirements 14.1
# ---------------------------------------------------------------------------


class TestConsistencyQualifiesOnThreshold:
    """For any items_total > 0 and items_completed in [0, items_total],
    the day qualifies if and only if items_completed / items_total >= 0.5.

    **Validates: Requirements 14.1**
    """

    @settings(**_PBT_SETTINGS)
    @given(inputs=qualifying_day_inputs())
    def test_qualification_matches_threshold(
        self, inputs: tuple[int, int], db_session: Session
    ) -> None:
        """A day qualifies iff completion ratio >= 0.50."""
        _reset_state(db_session)
        items_total, items_completed = inputs
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)
        today = date(2025, 6, 15)

        result = service.update_consistency(
            user_id=1,
            items_total=items_total,
            items_completed=items_completed,
            evaluation_date=today,
        )

        ratio = items_completed / items_total
        if ratio >= 0.5:
            assert result.current_streak == 1, (
                f"Expected qualifying day for ratio {ratio:.3f} "
                f"(completed={items_completed}, total={items_total})"
            )
            assert result.total_consistent_days == 1
            assert result.last_qualifying_date == today
        else:
            assert result.current_streak == 0, (
                f"Expected non-qualifying day for ratio {ratio:.3f} "
                f"(completed={items_completed}, total={items_total})"
            )


# ---------------------------------------------------------------------------
# Property 29: Streak reset preserves longest streak
# Validates: Requirements 14.3
# ---------------------------------------------------------------------------


class TestStreakResetPreservesLongest:
    """For any sequence of qualifying and non-qualifying days,
    longest_streak never decreases.

    **Validates: Requirements 14.3**
    """

    @settings(**_PBT_SETTINGS)
    @given(days=day_sequence())
    def test_longest_streak_never_decreases(
        self, days: list[bool], db_session: Session
    ) -> None:
        """Longest streak is monotonically non-decreasing over any day sequence."""
        _reset_state(db_session)
        _seed_user(db_session)
        service = ConsistencyService(db=db_session)
        base_date = date(2025, 1, 1)

        prev_longest = 0

        for i, qualifies in enumerate(days):
            eval_date = base_date + timedelta(days=i)

            if qualifies:
                items_total = 10
                items_completed = 8  # 80% — qualifies
            else:
                items_total = 10
                items_completed = 2  # 20% — does not qualify

            service.update_consistency(
                user_id=1,
                items_total=items_total,
                items_completed=items_completed,
                evaluation_date=eval_date,
            )

            record = service.get_consistency(user_id=1)
            assert record.longest_streak >= prev_longest, (
                f"longest_streak decreased from {prev_longest} to "
                f"{record.longest_streak} on day {i} "
                f"(qualifies={qualifies}, sequence={days[:i+1]})"
            )
            prev_longest = record.longest_streak
