"""Repository for readiness score persistence and retrieval.

Handles all database access for ReadinessScoreHistory and SelfAssessmentRecord.

Validates: Requirements 2.2, 2.3, 2.4, 19.2, 19.6, 19.7
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.readiness.models import ReadinessScoreHistory, SelfAssessmentRecord
from app.infrastructure.repositories.base import BaseRepository


class ReadinessRepository(BaseRepository[ReadinessScoreHistory]):
    """Persistence layer for readiness score history records."""

    model = ReadinessScoreHistory

    def __init__(self, db: Session) -> None:
        super().__init__(db=db)

    def get_latest(self, user_id: int) -> ReadinessScoreHistory | None:
        """Return the most recent score record for a user.

        Used by ReadinessService.get_current() to return the latest computed
        readiness score without triggering a recomputation.
        """
        stmt = (
            select(ReadinessScoreHistory)
            .where(ReadinessScoreHistory.user_id == user_id)
            .order_by(ReadinessScoreHistory.computed_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_score_at_date(
        self, user_id: int, target_date: date
    ) -> ReadinessScoreHistory | None:
        """Return the last score record computed on or before target_date.

        Used for delta calculation (e.g., comparing current score to 7 days ago).
        Returns the most recent record whose computed_at falls on or before
        the end of target_date.
        """
        end_of_day = datetime.combine(target_date, datetime.max.time())
        stmt = (
            select(ReadinessScoreHistory)
            .where(
                ReadinessScoreHistory.user_id == user_id,
                ReadinessScoreHistory.computed_at <= end_of_day,
            )
            .order_by(ReadinessScoreHistory.computed_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_trend(
        self, user_id: int, days: int = 30
    ) -> list[ReadinessScoreHistory]:
        """Return score records for the past N days, ordered by computed_at ascending.

        Returns all records within the date range so the service layer can
        select one representative score per day and carry forward gaps.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = (
            select(ReadinessScoreHistory)
            .where(
                ReadinessScoreHistory.user_id == user_id,
                ReadinessScoreHistory.computed_at >= cutoff,
            )
            .order_by(ReadinessScoreHistory.computed_at.asc())
        )
        return list(self.db.execute(stmt).scalars().all())


    # ------------------------------------------------------------------
    # Self-Assessment methods
    # ------------------------------------------------------------------

    def create_self_assessment(
        self, record: SelfAssessmentRecord
    ) -> SelfAssessmentRecord:
        """Persist a new self-assessment record.

        Validates: Requirement 19.2
        """
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_latest_assessment(self, user_id: int) -> SelfAssessmentRecord | None:
        """Return the most recent self-assessment record for a user.

        Used by is_self_assessment_due() to check timing.
        Validates: Requirement 19.7
        """
        stmt = (
            select(SelfAssessmentRecord)
            .where(SelfAssessmentRecord.user_id == user_id)
            .order_by(SelfAssessmentRecord.assessed_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_assessment_history(
        self, user_id: int
    ) -> list[SelfAssessmentRecord]:
        """Return all self-assessment records ordered by assessed_at descending.

        Validates: Requirement 19.6
        """
        stmt = (
            select(SelfAssessmentRecord)
            .where(SelfAssessmentRecord.user_id == user_id)
            .order_by(SelfAssessmentRecord.assessed_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())
