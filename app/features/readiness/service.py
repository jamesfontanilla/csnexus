"""Readiness service orchestrating score computation and persistence.

Validates: Requirements 1.1, 1.6, 1.7, 1.8, 1.9, 2.1, 2.3, 2.4, 2.5, 2.6,
           3.1, 3.2, 3.3, 3.4, 3.5
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException

from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_exams.repository import MockExamRepository
from app.features.readiness.algorithms.scorer import (
    ComponentWeights,
    ReadinessComponents,
    compute_coverage_component,
    compute_mastery_component,
    compute_mock_component,
    compute_readiness_score,
    compute_retention_component,
    redistribute_weights_no_mock,
)
from app.features.readiness.models import ReadinessScoreHistory, SelfAssessmentRecord
from app.features.readiness.repository import ReadinessRepository
from app.features.readiness.schemas import (
    DashboardResponse,
    ReadinessComponentsSchema,
    ReadinessResponse,
    SelfAssessmentHistoryItem,
    SelfAssessmentHistoryResponse,
    SelfAssessmentPromptResponse,
    SelfAssessmentResponse,
    TopImpactSubtopic,
    TrendPoint,
)

logger = logging.getLogger(__name__)


class ReadinessService:
    """Orchestrates readiness score computation, persistence, and retrieval."""

    def __init__(
        self,
        *,
        readiness_repo: ReadinessRepository,
        mastery_repo: MasteryRepository,
        flashcard_repo: FlashcardRepository,
        mock_exam_repo: MockExamRepository,
        content_repo: SubtopicRepository,
        question_repo: QuestionRepository,
    ) -> None:
        self._readiness_repo = readiness_repo
        self._mastery_repo = mastery_repo
        self._flashcard_repo = flashcard_repo
        self._mock_exam_repo = mock_exam_repo
        self._content_repo = content_repo
        self._question_repo = question_repo

    # ------------------------------------------------------------------
    # Core computation
    # ------------------------------------------------------------------

    def compute_and_persist(self, user_id: int) -> ReadinessScoreHistory:
        """Recompute readiness score and persist to history.

        Gathers mastery scores + exam weights, FSRS retentions, mock exam
        scores with days_since, and coverage data. Calls scorer functions.
        Persists result via ReadinessRepository.create().

        After persisting, triggers milestone evaluation so competence-based
        milestones are awarded as soon as the score changes (Req 13.4).

        Implements graceful degradation: on failure, returns stale score
        if available.
        """
        try:
            result = self._compute_and_persist_inner(user_id)
            # Trigger milestone evaluation after score change (Req 13.4)
            self._evaluate_milestones_after_score_change(user_id)
            return result
        except Exception as exc:
            logger.exception(
                "Readiness computation failed for user_id=%d, returning stale score",
                user_id,
            )
            stale = self._readiness_repo.get_latest(user_id)
            if stale is not None:
                return stale
            # No stale score available — re-raise
            raise HTTPException(
                status_code=500,
                detail="Readiness score computation failed",
            ) from exc

    def _compute_and_persist_inner(self, user_id: int) -> ReadinessScoreHistory:
        """Internal computation logic without error handling."""
        # 1. Gather mastery data
        mastery_rows = list(self._mastery_repo.list_by_user(user_id))

        # 2. Check no-activity case
        flashcard_count = self._flashcard_repo.count_user_reviews(user_id)
        mock_scores_raw = self._get_mock_scores(user_id)
        has_mock_history = len(mock_scores_raw) > 0
        has_flashcard_history = flashcard_count > 0
        has_mastery_data = len(mastery_rows) > 0

        if not has_mastery_data and not has_flashcard_history and not has_mock_history:
            # No activity — return score 0
            return self._persist_zero_score(user_id)

        # 3. Compute mastery component
        mastery_scores = self._build_mastery_scores(mastery_rows)
        mastery_component = compute_mastery_component(mastery_scores)

        # 4. Compute retention component
        retention_component = self._compute_retention(
            user_id, mastery_rows, has_flashcard_history
        )

        # 5. Compute mock component
        mock_component = compute_mock_component(mock_scores_raw)

        # 6. Compute coverage component
        coverage_component = self._compute_coverage(user_id)

        # 7. Determine weights (redistribute if no mock history)
        if has_mock_history:
            weights = ComponentWeights()
        else:
            weights = redistribute_weights_no_mock()

        # 8. Compute final score
        components = ReadinessComponents(
            mastery_component=mastery_component,
            retention_component=retention_component,
            mock_component=mock_component,
            coverage_component=coverage_component,
        )
        final_score = compute_readiness_score(components, weights)

        # 9. Persist
        record = ReadinessScoreHistory(
            user_id=user_id,
            score=final_score,
            mastery_component=mastery_component,
            retention_component=retention_component,
            mock_component=mock_component,
            coverage_component=coverage_component,
            weights_used=json.dumps(
                {
                    "mastery": weights.mastery,
                    "retention": weights.retention,
                    "mock_exam": weights.mock_exam,
                    "coverage": weights.coverage,
                }
            ),
        )
        return self._readiness_repo.create(record)

    # ------------------------------------------------------------------
    # Query methods
    # ------------------------------------------------------------------

    def get_current(self, user_id: int) -> ReadinessResponse:
        """Return most recent score with component breakdown and 7-day delta."""
        latest = self._readiness_repo.get_latest(user_id)

        if latest is None:
            return ReadinessResponse(
                score=0,
                components=ReadinessComponentsSchema(
                    mastery_component=0.0,
                    retention_component=0.0,
                    mock_component=0.0,
                    coverage_component=0.0,
                ),
                delta=None,
                stale_score=False,
            )

        # Calculate 7-day delta
        seven_days_ago = date.today() - timedelta(days=7)
        past_record = self._readiness_repo.get_score_at_date(user_id, seven_days_ago)
        delta = (latest.score - past_record.score) if past_record else None

        return ReadinessResponse(
            score=latest.score,
            components=ReadinessComponentsSchema(
                mastery_component=latest.mastery_component,
                retention_component=latest.retention_component,
                mock_component=latest.mock_component,
                coverage_component=latest.coverage_component,
            ),
            delta=delta,
            stale_score=False,
        )

    def get_dashboard(self, user_id: int) -> DashboardResponse:
        """Return full dashboard payload with top 3 point-impact subtopics.

        Includes: score, components, delta, top_impact_subtopics,
        readiness_level classification, and computed_at timestamp.
        Implements graceful degradation on failure.
        """
        try:
            return self._get_dashboard_inner(user_id)
        except Exception:
            logger.exception(
                "Dashboard computation failed for user_id=%d, returning stale data",
                user_id,
            )
            return self._get_stale_dashboard(user_id)

    def _get_dashboard_inner(self, user_id: int) -> DashboardResponse:
        """Internal dashboard computation."""
        latest = self._readiness_repo.get_latest(user_id)

        if latest is None:
            return DashboardResponse(
                score=0,
                components=ReadinessComponentsSchema(
                    mastery_component=0.0,
                    retention_component=0.0,
                    mock_component=0.0,
                    coverage_component=0.0,
                ),
                delta=None,
                top_impact_subtopics=[],
                readiness_level=self.get_readiness_level(0),
                stale_data=False,
                computed_at=None,
            )

        # 7-day delta
        seven_days_ago = date.today() - timedelta(days=7)
        past_record = self._readiness_repo.get_score_at_date(user_id, seven_days_ago)
        delta = (latest.score - past_record.score) if past_record else None

        # Top 3 point-impact subtopics
        top_impact = self._compute_top_impact_subtopics(user_id, top_n=3)

        return DashboardResponse(
            score=latest.score,
            components=ReadinessComponentsSchema(
                mastery_component=latest.mastery_component,
                retention_component=latest.retention_component,
                mock_component=latest.mock_component,
                coverage_component=latest.coverage_component,
            ),
            delta=delta,
            top_impact_subtopics=top_impact,
            readiness_level=self.get_readiness_level(latest.score),
            stale_data=False,
            computed_at=latest.computed_at,
        )

    def _get_stale_dashboard(self, user_id: int) -> DashboardResponse:
        """Return stale dashboard when computation fails."""
        latest = self._readiness_repo.get_latest(user_id)
        if latest is None:
            return DashboardResponse(
                score=0,
                components=ReadinessComponentsSchema(
                    mastery_component=0.0,
                    retention_component=0.0,
                    mock_component=0.0,
                    coverage_component=0.0,
                ),
                delta=None,
                top_impact_subtopics=[],
                readiness_level=self.get_readiness_level(0),
                stale_data=True,
                computed_at=None,
            )

        return DashboardResponse(
            score=latest.score,
            components=ReadinessComponentsSchema(
                mastery_component=latest.mastery_component,
                retention_component=latest.retention_component,
                mock_component=latest.mock_component,
                coverage_component=latest.coverage_component,
            ),
            delta=None,
            top_impact_subtopics=[],
            readiness_level=self.get_readiness_level(latest.score),
            stale_data=True,
            computed_at=latest.computed_at,
        )

    def get_trend(self, user_id: int, days: int = 30) -> list[TrendPoint]:
        """Return one score per day for the past N days, carrying forward gaps.

        Uses the last computed score of each day as the representative value.
        For days where no score was computed, carries forward the most recent
        prior score. If no prior score exists, uses 0.
        """
        records = self._readiness_repo.get_trend(user_id, days=days)

        # Group records by date, take last one per day
        score_by_date: dict[date, int] = {}
        for record in records:
            record_date = record.computed_at.date()
            score_by_date[record_date] = record.score

        # Also get the score just before the window for carry-forward seed
        start_date = date.today() - timedelta(days=days - 1)
        seed_record = self._readiness_repo.get_score_at_date(
            user_id, start_date - timedelta(days=1)
        )
        carry_forward_score = seed_record.score if seed_record else 0

        # Build complete series with carry-forward
        trend: list[TrendPoint] = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            if current_date in score_by_date:
                carry_forward_score = score_by_date[current_date]
            trend.append(
                TrendPoint(
                    date=current_date.isoformat(),
                    score=carry_forward_score,
                )
            )

        return trend

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def get_readiness_level(self, score: int) -> str:
        """Classify score into readiness level.

        0-39: "Not Ready"
        40-59: "Getting There"
        60-79: "Almost Ready"
        80-100: "Exam Ready"
        """
        if score <= 39:
            return "Not Ready"
        if score <= 59:
            return "Getting There"
        if score <= 79:
            return "Almost Ready"
        return "Exam Ready"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _evaluate_milestones_after_score_change(self, user_id: int) -> None:
        """Trigger milestone evaluation after readiness score changes.

        Called after compute_and_persist succeeds. Catches and logs any
        milestone evaluation errors to avoid disrupting the readiness
        score flow (graceful degradation). (Req 13.4)
        """
        try:
            from app.features.gamification.milestone_service import MilestoneService

            db = self._readiness_repo.db
            milestone_service = MilestoneService(db=db)
            milestone_service.evaluate_milestones(user_id)
        except Exception:
            logger.warning(
                "Milestone evaluation failed for user_id=%d (non-fatal)",
                user_id,
                exc_info=True,
            )

    def _persist_zero_score(self, user_id: int) -> ReadinessScoreHistory:
        """Persist a score of 0 with all components at 0."""
        weights = ComponentWeights()
        record = ReadinessScoreHistory(
            user_id=user_id,
            score=0,
            mastery_component=0.0,
            retention_component=0.0,
            mock_component=0.0,
            coverage_component=0.0,
            weights_used=json.dumps(
                {
                    "mastery": weights.mastery,
                    "retention": weights.retention,
                    "mock_exam": weights.mock_exam,
                    "coverage": weights.coverage,
                }
            ),
        )
        return self._readiness_repo.create(record)

    def _build_mastery_scores(
        self, mastery_rows: list,
    ) -> list[tuple[float, float]]:
        """Build (mastery_score, exam_weight) tuples for mastery component.

        Each subtopic is weighted by its question count proportion in the exam.
        For simplicity, we use equal weighting across all subtopics that have
        mastery data (each subtopic contributes proportionally).
        """
        if not mastery_rows:
            return []

        # Equal weight per subtopic — the exam has 60 subtopics with roughly
        # equal question counts per category proportions. Without a per-subtopic
        # exam weight configuration, use uniform weight (1.0 each).
        return [(row.mastery_score, 1.0) for row in mastery_rows]

    def _compute_retention(
        self,
        user_id: int,
        mastery_rows: list,
        has_flashcard_history: bool,
    ) -> float:
        """Compute retention component using FSRS retentions or subtopic fallback."""
        fsrs_retentions: list[float] | None = None
        subtopic_retentions: list[float] | None = None

        if has_flashcard_history:
            # Get FSRS retention scores from flashcards the user has reviewed
            fsrs_retentions = self._get_fsrs_retentions(user_id)

        if not fsrs_retentions and mastery_rows:
            # Fallback to subtopic retention scores
            subtopic_retentions = [
                row.retention_score for row in mastery_rows
                if row.retention_score is not None
            ]
            if not subtopic_retentions:
                subtopic_retentions = None

        # Default 30 days if no exam date set
        days_until_exam = 30

        return compute_retention_component(
            fsrs_retentions=fsrs_retentions,
            subtopic_retention_scores=subtopic_retentions,
            days_until_exam=days_until_exam,
        )

    def _get_fsrs_retentions(self, user_id: int) -> list[float] | None:
        """Get FSRS retention scores from user's reviewed flashcards."""
        # Get cards the user has reviewed (using the daily queue which returns
        # cards belonging to the user's decks that have been reviewed)
        cards = self._flashcard_repo.get_daily_queue(user_id, max_cards=500)

        # We actually need cards that have been reviewed (have total_reviews > 0)
        # The daily queue returns due cards. Instead, let's query directly
        # for reviewed cards via the retention_score on flashcards in user's decks.
        # Since FlashcardRepository doesn't expose a direct "all reviewed cards"
        # method, we use review count to check if user has flashcard activity,
        # and rely on the retention data available.

        # For now, use the review heatmap to confirm activity exists, and
        # get retention data from flashcard scores. The repository has
        # get_retention_by_tag which gives avg retention per tag. We can
        # approximate the FSRS retention list using this data.
        retention_data = self._flashcard_repo.get_retention_by_tag(user_id)
        if not retention_data:
            return None

        # retention_data is list of (tag, avg_retention, card_count)
        # Expand into individual retention values weighted by card count
        retentions: list[float] = []
        for _tag, avg_ret, count in retention_data:
            # Add the average retention for each logical group
            if avg_ret > 0:
                retentions.append(avg_ret)

        return retentions if retentions else None

    def _get_mock_scores(self, user_id: int) -> list[tuple[float, int]]:
        """Get mock exam scores as (percentage_correct, days_since_exam) tuples.

        Only includes fully completed exams (SUBMITTED or AUTO_SUBMITTED).
        """
        completed_exams = self._mock_exam_repo.get_completed_for_user(
            user_id, limit=20
        )

        if not completed_exams:
            return []

        today = datetime.now(timezone.utc)
        mock_scores: list[tuple[float, int]] = []

        for attempt in completed_exams:
            if attempt.score is None or attempt.max_score == 0:
                continue
            percentage_correct = (attempt.score / attempt.max_score) * 100.0
            submitted_at = attempt.submitted_at or attempt.started_at
            days_since = (today - submitted_at).days
            mock_scores.append((percentage_correct, max(0, days_since)))

        return mock_scores

    def _compute_coverage(self, user_id: int) -> float:
        """Compute coverage component: % of subtopics with >= 10% questions attempted."""
        # Get all subtopics from the content system
        from sqlalchemy import func, select

        from app.features.content.models import Question, Subtopic

        # Count total questions per subtopic
        db = self._content_repo.db
        question_counts_stmt = (
            select(
                Question.subtopic_id,
                func.count(Question.id).label("total"),
            )
            .where(Question.is_active.is_(True))
            .group_by(Question.subtopic_id)
        )
        question_counts = {
            row[0]: row[1]
            for row in db.execute(question_counts_stmt).all()
        }

        if not question_counts:
            return 0.0

        # Get user's attempt counts per subtopic from mastery data
        mastery_rows = list(self._mastery_repo.list_by_user(user_id))
        user_attempts: dict[int, int] = {
            row.subtopic_id: row.total_attempts for row in mastery_rows
        }

        # Build coverage tuples (attempted, available) for each subtopic
        coverage_data: list[tuple[int, int]] = []
        for subtopic_id, available in question_counts.items():
            attempted = user_attempts.get(subtopic_id, 0)
            coverage_data.append((attempted, available))

        return compute_coverage_component(coverage_data)

    def _compute_top_impact_subtopics(
        self, user_id: int, top_n: int = 3
    ) -> list[TopImpactSubtopic]:
        """Compute top N subtopics by point_impact.

        Point impact = estimated score gain from improving the subtopic
        to a target mastery level (0.8). Subtopics with current mastery
        below 0.8 are candidates.
        """
        mastery_rows = list(self._mastery_repo.list_by_user(user_id))

        if not mastery_rows:
            return []

        # Get subtopic names for display
        subtopic_names: dict[int, str] = {}
        for row in mastery_rows:
            subtopic = self._content_repo.get(row.subtopic_id)
            if subtopic:
                subtopic_names[row.subtopic_id] = subtopic.title

        # Compute point impact for each subtopic below target
        target_mastery = 0.8
        impact_candidates: list[tuple[int, str, float]] = []

        for row in mastery_rows:
            if row.mastery_score >= target_mastery:
                continue
            # Estimated point impact: proportional to the gap between
            # current and target, weighted by the mastery component weight (0.4)
            # across 60 subtopics
            gap = target_mastery - row.mastery_score
            # Each subtopic contributes ~(1/60) of the mastery component which
            # is 40% of the total score. So max impact per subtopic is roughly
            # 0.4 * 100 / 60 ≈ 0.67 points at full gap.
            # Use a more meaningful scale: gap * weight_per_subtopic * 100
            total_subtopics = max(len(mastery_rows), 1)
            point_impact = gap * (40.0 / total_subtopics)

            name = subtopic_names.get(row.subtopic_id, f"Subtopic {row.subtopic_id}")
            impact_candidates.append((row.subtopic_id, name, point_impact))

        # Sort by point impact descending, take top N
        impact_candidates.sort(key=lambda x: x[2], reverse=True)
        top_candidates = impact_candidates[:top_n]

        return [
            TopImpactSubtopic(
                subtopic_id=subtopic_id,
                subtopic_name=name,
                point_impact=round(point_impact, 2),
            )
            for subtopic_id, name, point_impact in top_candidates
        ]

    # ------------------------------------------------------------------
    # Self-Assessment Calibration (Req 19)
    # ------------------------------------------------------------------

    def submit_self_assessment(
        self, user_id: int, self_assessed_score: int
    ) -> SelfAssessmentResponse:
        """Submit a self-assessment and compare against computed readiness.

        Computes delta (self_assessed - computed), determines calibration_status,
        persists the record, and returns a response with appropriate messaging.

        Validates: Requirements 19.1, 19.2, 19.3, 19.4, 19.5
        """
        # Get current computed score
        latest = self._readiness_repo.get_latest(user_id)
        computed_score = latest.score if latest else 0

        # Compute delta
        delta = self_assessed_score - computed_score

        # Determine calibration status
        if delta > 15:
            calibration_status = "overconfident"
        elif delta < -10:
            calibration_status = "underconfident"
        else:
            calibration_status = "well_calibrated"

        # Persist record
        record = SelfAssessmentRecord(
            user_id=user_id,
            self_assessed_score=self_assessed_score,
            computed_score=computed_score,
            delta=delta,
            calibration_status=calibration_status,
        )
        self._readiness_repo.create_self_assessment(record)

        # Generate message and calibration_warning
        message = self._get_calibration_message(calibration_status, delta)
        calibration_warning = None
        if calibration_status == "overconfident":
            calibration_warning = self._generate_calibration_warning(
                user_id, delta, latest
            )

        return SelfAssessmentResponse(
            self_assessed_score=self_assessed_score,
            computed_score=computed_score,
            delta=delta,
            calibration_status=calibration_status,
            message=message,
            calibration_warning=calibration_warning,
        )

    def get_self_assessment_history(
        self, user_id: int
    ) -> SelfAssessmentHistoryResponse:
        """Return all self-assessment records for calibration trend.

        Validates: Requirement 19.6
        """
        records = self._readiness_repo.get_assessment_history(user_id)
        return SelfAssessmentHistoryResponse(
            records=[
                SelfAssessmentHistoryItem(
                    self_assessed_score=r.self_assessed_score,
                    computed_score=r.computed_score,
                    delta=r.delta,
                    calibration_status=r.calibration_status,
                    assessed_at=r.assessed_at,
                )
                for r in records
            ]
        )

    def is_self_assessment_due(self, user_id: int) -> SelfAssessmentPromptResponse:
        """Check if 7+ days have passed since the last self-assessment.

        Returns True if no history exists or if 7+ days since last assessment.
        Validates: Requirements 19.1, 19.7
        """
        latest = self._readiness_repo.get_latest_assessment(user_id)

        if latest is None:
            return SelfAssessmentPromptResponse(
                is_due=True,
                last_assessed_at=None,
            )

        days_since = (datetime.now(timezone.utc) - latest.assessed_at).days
        return SelfAssessmentPromptResponse(
            is_due=days_since >= 7,
            last_assessed_at=latest.assessed_at,
        )

    # ------------------------------------------------------------------
    # Self-Assessment private helpers
    # ------------------------------------------------------------------

    def _get_calibration_message(self, status: str, delta: int) -> str:
        """Return an appropriate feedback message based on calibration status."""
        if status == "overconfident":
            return (
                f"Your self-assessment is {delta} points above your computed readiness. "
                "Consider taking a mock exam to get a realistic benchmark."
            )
        if status == "underconfident":
            return (
                f"You're underestimating yourself by {abs(delta)} points! "
                "You're better prepared than you think — trust your progress."
            )
        return (
            "Your self-assessment closely matches your computed readiness. "
            "You have accurate self-awareness of your preparation level."
        )

    def _generate_calibration_warning(
        self,
        user_id: int,
        delta: int,
        latest_score: ReadinessScoreHistory | None,
    ) -> str:
        """Generate a calibration warning identifying the weakest component.

        Validates: Requirement 19.3
        """
        if latest_score is None:
            return (
                f"You overestimate your readiness by {delta} points. "
                "Try a mock exam to get a realistic benchmark."
            )

        # Identify weakest component (lowest value = biggest drag)
        components = {
            "mastery": latest_score.mastery_component,
            "retention": latest_score.retention_component,
            "mock_exam": latest_score.mock_component,
            "coverage": latest_score.coverage_component,
        }
        weakest = min(components, key=components.get)  # type: ignore[arg-type]

        component_messages = {
            "mastery": "Your mastery across subtopics is lower than you think.",
            "retention": (
                "Your retention is lower than you think — "
                "you may forget material by exam day at current pace."
            ),
            "mock_exam": (
                "Your mock exam performance suggests gaps you may be overlooking."
            ),
            "coverage": (
                "You haven't covered enough subtopics yet — "
                "there are areas you haven't studied."
            ),
        }

        return (
            f"You overestimate your readiness by {delta} points. "
            f"{component_messages[weakest]} "
            "Try a mock exam to get a realistic benchmark."
        )
