"""Repository for mock analytics persistence and retrieval.

Owns all database access for diagnostic reports and recommendations.
Queries join against mock_exam_attempt_answers and questions to compute
per-subtopic historical accuracy.

Validates: Requirements 10.5, 12.4, 12.5
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import Integer, func, select
from sqlalchemy.orm import Session

from app.features.content.models import Question
from app.features.mock_analytics.models import DiagnosticReport, RecommendationRecord
from app.features.mock_exams.models import (
    MockExamAttempt,
    MockExamAttemptAnswer,
    MockExamAttemptStatus,
)
from app.infrastructure.repositories.base import BaseRepository


class MockAnalyticsRepository(BaseRepository[DiagnosticReport]):
    """Persistence layer for post-mock exam diagnostic analytics."""

    model = DiagnosticReport

    def __init__(self, db: Session) -> None:
        super().__init__(db=db)

    def create_report(self, report: DiagnosticReport) -> DiagnosticReport:
        """Persist a diagnostic report and return it with server defaults applied."""
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get_report(self, attempt_id: int) -> DiagnosticReport | None:
        """Retrieve a diagnostic report by mock exam attempt ID."""
        stmt = select(DiagnosticReport).where(
            DiagnosticReport.mock_exam_attempt_id == attempt_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_recommendations(self, report_id: int) -> list[RecommendationRecord]:
        """Retrieve all recommendations for a given diagnostic report.

        Results are sorted by estimated_point_gain descending so the
        highest-impact recommendations appear first.
        """
        stmt = (
            select(RecommendationRecord)
            .where(RecommendationRecord.report_id == report_id)
            .order_by(RecommendationRecord.estimated_point_gain.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def accept_recommendation(self, recommendation_id: int) -> RecommendationRecord | None:
        """Set the accepted_at timestamp on a recommendation.

        Returns the updated record, or None if the recommendation does not exist.
        """
        recommendation = self.db.get(RecommendationRecord, recommendation_id)
        if recommendation is None:
            return None
        recommendation.accepted_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation

    def get_historical_accuracy(self, user_id: int) -> dict[int, float]:
        """Return per-subtopic historical average accuracy across all submitted mock exams.

        Joins mock_exam_attempts -> mock_exam_attempt_answers -> questions to
        group by subtopic_id and compute (correct / attempted) for each subtopic.

        Only includes answers from submitted attempts (SUBMITTED or AUTO_SUBMITTED)
        where is_correct is not NULL (i.e., graded answers).

        Returns a dict mapping subtopic_id -> average accuracy as a float 0.0–1.0.
        """
        # SQLite stores booleans as 0/1 so AVG(is_correct) gives the
        # fraction of correct answers directly. For Postgres portability
        # we cast to Integer explicitly.
        stmt = (
            select(
                Question.subtopic_id,
                (
                    func.sum(func.cast(MockExamAttemptAnswer.is_correct, Integer))
                    * 1.0
                    / func.count(MockExamAttemptAnswer.id)
                ).label("accuracy"),
            )
            .join(
                MockExamAttempt,
                MockExamAttemptAnswer.attempt_id == MockExamAttempt.id,
            )
            .join(
                Question,
                MockExamAttemptAnswer.question_id == Question.id,
            )
            .where(
                MockExamAttempt.user_id == user_id,
                MockExamAttempt.status.in_([
                    MockExamAttemptStatus.SUBMITTED.value,
                    MockExamAttemptStatus.AUTO_SUBMITTED.value,
                ]),
                MockExamAttemptAnswer.is_correct.isnot(None),
            )
            .group_by(Question.subtopic_id)
        )
        rows = self.db.execute(stmt).all()
        return {subtopic_id: float(accuracy) for subtopic_id, accuracy in rows}

    def get_user_mock_scores(self, user_id: int, today: date) -> list[tuple[float, int]]:
        """Return (score_pct, days_since) for each submitted mock exam attempt.

        Only includes submitted/auto-submitted attempts with a non-null score.
        score_pct is computed as (score / max_score * 100).
        days_since is computed from submitted_at relative to ``today``.

        Returns list sorted by submitted_at ascending (oldest first).
        """
        stmt = (
            select(
                MockExamAttempt.score,
                MockExamAttempt.max_score,
                MockExamAttempt.submitted_at,
            )
            .where(
                MockExamAttempt.user_id == user_id,
                MockExamAttempt.status.in_([
                    MockExamAttemptStatus.SUBMITTED.value,
                    MockExamAttemptStatus.AUTO_SUBMITTED.value,
                ]),
                MockExamAttempt.score.isnot(None),
            )
            .order_by(MockExamAttempt.submitted_at.asc())
        )
        rows = self.db.execute(stmt).all()
        results: list[tuple[float, int]] = []
        for score, max_score, submitted_at in rows:
            if max_score <= 0:
                continue
            score_pct = score / max_score * 100.0
            days_since = (today - submitted_at.date()).days
            results.append((score_pct, max(0, days_since)))
        return results

    def get_attempt_answers_with_questions(
        self, attempt_id: int
    ) -> list[tuple[int, bool, int, float, str]]:
        """Return answer tuples for diagnostic computation.

        Each tuple is (subtopic_id, is_correct, question_id, seconds, difficulty).

        Only includes graded answers (is_correct IS NOT NULL). Time (seconds)
        is computed as the difference between consecutive answered_at timestamps
        for the same attempt (sorted by ordinal). The first answer uses 30s default.
        Answers without answered_at use 30s default.
        """
        stmt = (
            select(
                MockExamAttemptAnswer.question_id,
                MockExamAttemptAnswer.is_correct,
                MockExamAttemptAnswer.answered_at,
                MockExamAttemptAnswer.ordinal,
                Question.subtopic_id,
                Question.difficulty,
            )
            .join(Question, MockExamAttemptAnswer.question_id == Question.id)
            .where(
                MockExamAttemptAnswer.attempt_id == attempt_id,
                MockExamAttemptAnswer.is_correct.isnot(None),
            )
            .order_by(MockExamAttemptAnswer.ordinal)
        )
        rows = self.db.execute(stmt).all()

        # Compute per-question seconds from consecutive answered_at timestamps
        results: list[tuple[int, bool, int, float, str]] = []
        prev_answered_at: datetime | None = None
        for question_id, is_correct, answered_at, _ordinal, subtopic_id, difficulty in rows:
            if answered_at is not None and prev_answered_at is not None:
                seconds = (answered_at - prev_answered_at).total_seconds()
                # Clamp unreasonable negatives to default
                if seconds < 0:
                    seconds = 30.0
            else:
                seconds = 30.0  # default when timing unavailable
            prev_answered_at = answered_at
            results.append((subtopic_id, bool(is_correct), question_id, seconds, difficulty))
        return results

    def get_questions_per_subtopic_in_exam(self, attempt_id: int) -> dict[int, int]:
        """Return the count of questions per subtopic in a mock exam attempt.

        Used for estimated_point_gain calculation in recommendations.
        """
        stmt = (
            select(
                Question.subtopic_id,
                func.count(MockExamAttemptAnswer.id).label("count"),
            )
            .join(Question, MockExamAttemptAnswer.question_id == Question.id)
            .where(MockExamAttemptAnswer.attempt_id == attempt_id)
            .group_by(Question.subtopic_id)
        )
        rows = self.db.execute(stmt).all()
        return {subtopic_id: count for subtopic_id, count in rows}
