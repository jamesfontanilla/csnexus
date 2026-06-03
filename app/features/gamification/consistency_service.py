"""Service layer for Study Consistency tracking.

Replaces raw login streaks for users on the intelligent learning engine.
A day qualifies when the user completes ≥50% of their daily queue items
(by count). Merely logging in does not count.

Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.gamification.models import StudyConsistency


def _utctoday() -> date:
    return datetime.now(tz=timezone.utc).date()


class ConsistencyService:
    """Manage study consistency metrics for a user.

    Constructor injection pattern — accepts a SQLAlchemy session directly
    since StudyConsistency is a simple single-table model without a
    dedicated repository class.
    """

    QUALIFYING_THRESHOLD = 0.50  # 50% queue items by count

    def __init__(self, *, db: Session) -> None:
        self._db = db

    # ------------------------------------------------------------------
    # Core: update consistency after daily queue evaluation
    # ------------------------------------------------------------------

    def update_consistency(
        self,
        user_id: int,
        items_total: int,
        items_completed: int,
        *,
        evaluation_date: date | None = None,
    ) -> StudyConsistency:
        """Evaluate whether the given day qualifies as a consistent study day.

        A day qualifies when ``items_completed / items_total >= 0.50``.
        Merely logging in (items_total == 0 or items_completed == 0) does NOT
        qualify (Req 14.2).

        Args:
            user_id: The user whose consistency to update.
            items_total: Total queue items assigned for the day.
            items_completed: Number of items the user completed.
            evaluation_date: The calendar day being evaluated (defaults to UTC today).

        Returns:
            The updated StudyConsistency record.
        """
        today = evaluation_date or _utctoday()
        record = self._get_or_create(user_id)

        # Guard: no items or zero completed → not qualifying (Req 14.2)
        if items_total <= 0 or items_completed <= 0:
            self._handle_missed_day(record, today)
            return record

        completion_ratio = items_completed / items_total

        if completion_ratio >= self.QUALIFYING_THRESHOLD:
            self._handle_qualifying_day(record, today)
        else:
            self._handle_missed_day(record, today)

        return record

    # ------------------------------------------------------------------
    # Streak reset logic (Req 14.3)
    # ------------------------------------------------------------------

    def _handle_qualifying_day(
        self, record: StudyConsistency, today: date
    ) -> None:
        """Process a qualifying day — extend streak, update totals."""
        # Avoid double-counting the same day
        if record.last_qualifying_date == today:
            return

        # Check for gap: if last qualifying date is not yesterday,
        # the streak was already broken on the intervening day(s).
        if record.last_qualifying_date is not None:
            expected_previous = today - timedelta(days=1)
            if record.last_qualifying_date < expected_previous:
                # Missed day(s) in between → reset streak first
                record.current_streak = 0

        # Extend streak
        record.current_streak += 1
        record.total_consistent_days += 1
        record.last_qualifying_date = today

        # Update longest streak if current exceeds it
        if record.current_streak > record.longest_streak:
            record.longest_streak = record.current_streak

        self._db.commit()
        self._db.refresh(record)

    def _handle_missed_day(
        self, record: StudyConsistency, today: date
    ) -> None:
        """Process a missed day — reset current streak, preserve longest (Req 14.3)."""
        # Only reset if the missed day is actually after the last qualifying date
        # to avoid re-resetting on repeated calls for the same missed day.
        if record.last_qualifying_date is None or today > record.last_qualifying_date:
            record.current_streak = 0
            self._db.commit()
            self._db.refresh(record)

    # ------------------------------------------------------------------
    # Catch-up queue adjustment info (Req 14.5)
    # ------------------------------------------------------------------

    def get_missed_days_since_last_qualifying(
        self, user_id: int, *, reference_date: date | None = None
    ) -> int:
        """Return the number of days missed since the last qualifying date.

        This is used by the QueueService to determine how many catch-up
        FSRS-due cards to include. Returns 0 if user qualified yesterday
        or has never qualified (no catch-up needed for brand-new users).
        """
        today = reference_date or _utctoday()
        record = self._get_or_create(user_id)

        if record.last_qualifying_date is None:
            return 0

        days_gap = (today - record.last_qualifying_date).days - 1
        return max(0, days_gap)

    def needs_catch_up(
        self, user_id: int, *, reference_date: date | None = None
    ) -> bool:
        """Return True if the user missed at least one day and needs catch-up items."""
        return self.get_missed_days_since_last_qualifying(
            user_id, reference_date=reference_date
        ) > 0

    # ------------------------------------------------------------------
    # Migration: replace old streak with Study Consistency (Req 14.6)
    # ------------------------------------------------------------------

    def replace_streak_with_consistency(
        self,
        user_id: int,
        *,
        existing_longest_streak: int = 0,
    ) -> StudyConsistency:
        """Migrate a user from the old gamification streak to Study Consistency.

        Preserves the user's longest_streak from the old system so they don't
        lose recognition for past effort (Req 14.6, 15.1).

        Args:
            user_id: The user to migrate.
            existing_longest_streak: The longest streak from the old system.

        Returns:
            The initialized StudyConsistency record.
        """
        record = self._get_or_create(user_id)

        # Preserve the higher of the two longest_streak values
        if existing_longest_streak > record.longest_streak:
            record.longest_streak = existing_longest_streak

        # Reset current streak since we're starting fresh with the new metric
        record.current_streak = 0
        record.last_qualifying_date = None

        self._db.commit()
        self._db.refresh(record)
        return record

    # ------------------------------------------------------------------
    # Read access
    # ------------------------------------------------------------------

    def get_consistency(self, user_id: int) -> StudyConsistency:
        """Return the user's study consistency record, creating if needed."""
        return self._get_or_create(user_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_or_create(self, user_id: int) -> StudyConsistency:
        """Retrieve or initialize a StudyConsistency record for the user."""
        stmt = select(StudyConsistency).where(
            StudyConsistency.user_id == user_id
        )
        record = self._db.execute(stmt).scalar_one_or_none()

        if record is None:
            record = StudyConsistency(
                user_id=user_id,
                current_streak=0,
                longest_streak=0,
                total_consistent_days=0,
                last_qualifying_date=None,
            )
            self._db.add(record)
            self._db.commit()
            self._db.refresh(record)

        return record
