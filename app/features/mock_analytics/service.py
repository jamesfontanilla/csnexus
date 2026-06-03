"""Mock Analytics service: orchestrates diagnostic computation, persistence, and recommendations.

Validates: Requirements 10.1, 10.5, 11.1, 11.3, 12.1, 12.4
"""

from __future__ import annotations

import json
from datetime import timezone
from datetime import datetime as dt

from fastapi import HTTPException

from app.features.content.repository import SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_analytics.algorithms.diagnostics import (
    SubtopicDiagnostic,
    compute_diagnostic,
)
from app.features.mock_analytics.algorithms.prediction import (
    compute_predicted_score,
    generate_recommendations,
)
from app.features.mock_analytics.models import DiagnosticReport, RecommendationRecord
from app.features.mock_analytics.repository import MockAnalyticsRepository
from app.features.mock_exams.repository import MockExamRepository


class MockAnalyticsService:
    """Orchestrates post-mock exam analytics: diagnostics, predictions, recommendations."""

    def __init__(
        self,
        *,
        analytics_repo: MockAnalyticsRepository,
        mock_exam_repo: MockExamRepository,
        mastery_repo: MasteryRepository,
        subtopic_repo: SubtopicRepository,
    ) -> None:
        self._analytics_repo = analytics_repo
        self._mock_exam_repo = mock_exam_repo
        self._mastery_repo = mastery_repo
        self._subtopic_repo = subtopic_repo

    def generate_diagnostic(self, user_id: int, attempt_id: int) -> DiagnosticReport:
        """Gather answers, compute diagnostic breakdown, and persist the report.

        Raises HTTPException 404 if the attempt does not exist or does not
        belong to the user.
        """
        # Verify the attempt belongs to the user
        attempt = self._mock_exam_repo.get_attempt_for_user(attempt_id, user_id)
        if attempt is None:
            raise HTTPException(status_code=404, detail="Mock exam attempt not found")

        # Check if report already exists (idempotent)
        existing = self._analytics_repo.get_report(attempt_id)
        if existing is not None:
            return existing

        # Gather answer tuples for diagnostic computation
        answers = self._analytics_repo.get_attempt_answers_with_questions(attempt_id)

        # Get historical accuracy for regression detection
        historical_accuracy = self._analytics_repo.get_historical_accuracy(user_id)

        # Compute the diagnostic (pure function)
        diagnostic_result = compute_diagnostic(answers, historical_accuracy)

        # Serialize components to JSON for persistence
        subtopic_breakdowns_json = json.dumps([
            {
                "subtopic_id": b.subtopic_id,
                "questions_attempted": b.questions_attempted,
                "questions_correct": b.questions_correct,
                "points_lost": b.points_lost,
                "avg_seconds_per_question": b.avg_seconds_per_question,
                "accuracy_percentage": b.accuracy_percentage,
            }
            for b in diagnostic_result.subtopic_breakdowns
        ])

        highest_impact_json = json.dumps([
            {
                "subtopic_id": b.subtopic_id,
                "questions_attempted": b.questions_attempted,
                "questions_correct": b.questions_correct,
                "points_lost": b.points_lost,
                "avg_seconds_per_question": b.avg_seconds_per_question,
                "accuracy_percentage": b.accuracy_percentage,
            }
            for b in diagnostic_result.highest_impact_areas
        ])

        regression_alerts_json = json.dumps([
            {"subtopic_id": sid, "decline_percentage_points": decline}
            for sid, decline in diagnostic_result.regression_alerts
        ])

        difficulty_performance_json = json.dumps(diagnostic_result.difficulty_performance)

        # Create and persist the report
        report = DiagnosticReport(
            user_id=user_id,
            mock_exam_attempt_id=attempt_id,
            total_score=diagnostic_result.total_score,
            subtopic_breakdowns=subtopic_breakdowns_json,
            highest_impact_areas=highest_impact_json,
            regression_alerts=regression_alerts_json,
            difficulty_performance=difficulty_performance_json,
        )

        return self._analytics_repo.create_report(report)

    def get_diagnostic(self, attempt_id: int) -> DiagnosticReport:
        """Retrieve a persisted diagnostic report by attempt ID.

        Raises HTTPException 404 if no report exists for the given attempt.
        """
        report = self._analytics_repo.get_report(attempt_id)
        if report is None:
            raise HTTPException(
                status_code=404,
                detail="Diagnostic report not found for this attempt",
            )
        return report

    def get_recommendations(self, attempt_id: int) -> list[RecommendationRecord]:
        """Compute and return recommendations for a diagnostic report.

        If recommendations are already persisted for this report, returns
        the existing ones. Otherwise generates them from the diagnostic data
        and persists them.

        Raises HTTPException 404 if no diagnostic report exists.
        """
        report = self.get_diagnostic(attempt_id)

        # Check if recommendations already exist
        existing = self._analytics_repo.get_recommendations(report.id)
        if existing:
            return existing

        # Parse the subtopic breakdowns from the report
        subtopic_breakdowns_data = json.loads(report.subtopic_breakdowns)

        subtopic_diagnostics = [
            SubtopicDiagnostic(
                subtopic_id=b["subtopic_id"],
                questions_attempted=b["questions_attempted"],
                questions_correct=b["questions_correct"],
                points_lost=b["points_lost"],
                avg_seconds_per_question=b["avg_seconds_per_question"],
                accuracy_percentage=b["accuracy_percentage"],
            )
            for b in subtopic_breakdowns_data
        ]

        # Get subtopic names
        subtopic_ids = [d.subtopic_id for d in subtopic_diagnostics]
        subtopic_names = self._get_subtopic_names(subtopic_ids)

        # Get questions per subtopic in this exam
        questions_per_subtopic = self._analytics_repo.get_questions_per_subtopic_in_exam(
            attempt_id
        )

        # Get mastery scores for the user
        mastery_scores = self._get_mastery_scores(report.user_id, subtopic_ids)

        # Generate recommendations (pure function)
        recommendations = generate_recommendations(
            subtopic_diagnostics=subtopic_diagnostics,
            subtopic_names=subtopic_names,
            questions_per_subtopic_in_exam=questions_per_subtopic,
            mastery_scores=mastery_scores,
        )

        # Persist recommendations
        for rec in recommendations:
            record = RecommendationRecord(
                report_id=report.id,
                subtopic_id=rec.subtopic_id,
                subtopic_name=rec.subtopic_name,
                current_accuracy=rec.current_accuracy,
                target_accuracy=rec.target_accuracy,
                estimated_point_gain=rec.estimated_point_gain,
                recommended_action=rec.recommended_action,
            )
            self._analytics_repo.db.add(record)

        self._analytics_repo.db.commit()

        # Re-fetch to get server defaults applied
        return self._analytics_repo.get_recommendations(report.id)

    def accept_recommendation(
        self, user_id: int, recommendation_id: int
    ) -> RecommendationRecord:
        """Mark a recommendation as accepted.

        Raises HTTPException 404 if the recommendation does not exist.
        """
        result = self._analytics_repo.accept_recommendation(recommendation_id)
        if result is None:
            raise HTTPException(
                status_code=404, detail="Recommendation not found"
            )
        return result

    def get_predicted_score(self, user_id: int) -> dict:
        """Compute predicted score range from the user's mock exam history.

        Returns a dict with prediction fields, or a message if insufficient data.
        """
        today = dt.now(timezone.utc).date()

        # Get mock exam scores with days_since
        mock_scores = self._analytics_repo.get_user_mock_scores(user_id, today)

        if len(mock_scores) < 2:
            return {
                "lower_bound": None,
                "midpoint": None,
                "upper_bound": None,
                "confidence_level": None,
                "message": "At least 2 completed mock exams are needed for score prediction.",
            }

        # Get average retention from mastery data
        avg_retention = self._get_avg_retention(user_id)

        # Compute predicted score (pure function)
        prediction = compute_predicted_score(mock_scores, avg_retention)

        if prediction is None:
            return {
                "lower_bound": None,
                "midpoint": None,
                "upper_bound": None,
                "confidence_level": None,
                "message": "Unable to compute prediction from available data.",
            }

        return {
            "lower_bound": prediction.lower_bound,
            "midpoint": prediction.midpoint,
            "upper_bound": prediction.upper_bound,
            "confidence_level": prediction.confidence_level,
            "message": None,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_subtopic_names(self, subtopic_ids: list[int]) -> dict[int, str]:
        """Fetch subtopic titles by ID."""
        names: dict[int, str] = {}
        for sid in subtopic_ids:
            subtopic = self._subtopic_repo.get(sid)
            if subtopic is not None:
                names[sid] = subtopic.title
            else:
                names[sid] = f"Subtopic {sid}"
        return names

    def _get_mastery_scores(self, user_id: int, subtopic_ids: list[int]) -> dict[int, float]:
        """Fetch mastery scores for the given subtopics."""
        scores: dict[int, float] = {}
        for sid in subtopic_ids:
            mastery = self._mastery_repo.get_by_user_and_subtopic(user_id, sid)
            if mastery is not None:
                scores[sid] = mastery.mastery_score
            else:
                scores[sid] = 0.0
        return scores

    def _get_avg_retention(self, user_id: int) -> float:
        """Compute average retention_score across user's mastery records.

        Returns 0.85 as a sensible default if no mastery data exists.
        """
        mastery_records = self._mastery_repo.list_by_user(user_id)
        if not mastery_records:
            return 0.85

        total = sum(m.retention_score for m in mastery_records)
        return total / len(mastery_records)
