"""FastAPI router for the mock-analytics slice.

Mounts under ``/v1/mock-analytics`` and exposes diagnostic report retrieval,
recommendations, recommendation acceptance, and predicted score range endpoints.

All routes require authentication via ``get_current_user``.

Validates: Requirements 10.1, 11.1, 12.1, 12.4
"""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_analytics.repository import MockAnalyticsRepository
from app.features.mock_analytics.schemas import (
    DiagnosticResponse,
    DifficultyPerformanceSchema,
    PredictionResponse,
    RecommendationSchema,
    RecommendationsResponse,
    RegressionAlertSchema,
    SubtopicBreakdownSchema,
)
from app.features.mock_analytics.service import MockAnalyticsService
from app.features.mock_exams.repository import MockExamRepository
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/mock-analytics", tags=["mock-analytics"])


def get_mock_analytics_service(
    db: Session = Depends(get_db),
) -> MockAnalyticsService:
    """Construct MockAnalyticsService with all repository dependencies."""
    return MockAnalyticsService(
        analytics_repo=MockAnalyticsRepository(db=db),
        mock_exam_repo=MockExamRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        subtopic_repo=SubtopicRepository(db=db),
    )


# ---------------------------------------------------------------------------
# Prediction endpoint — declared BEFORE /{attempt_id} to avoid path conflict
# ---------------------------------------------------------------------------


@router.get("/prediction", response_model=PredictionResponse)
def get_predicted_score(
    user: User = Depends(get_current_user),
    service: MockAnalyticsService = Depends(get_mock_analytics_service),
) -> PredictionResponse:
    """Get predicted score range based on mock exam history."""
    prediction = service.get_predicted_score(user.id)
    return PredictionResponse(**prediction)


# ---------------------------------------------------------------------------
# Diagnostic report and recommendations
# ---------------------------------------------------------------------------


@router.get("/{attempt_id}", response_model=DiagnosticResponse)
def get_diagnostic_report(
    attempt_id: int,
    user: User = Depends(get_current_user),
    service: MockAnalyticsService = Depends(get_mock_analytics_service),
) -> DiagnosticResponse:
    """Get diagnostic report for a completed mock exam attempt."""
    report = service.get_diagnostic(attempt_id)

    # Parse JSON fields back into structured schema objects
    subtopic_breakdowns_data = json.loads(report.subtopic_breakdowns)
    highest_impact_data = json.loads(report.highest_impact_areas)
    regression_alerts_data = json.loads(report.regression_alerts)
    difficulty_performance_data = json.loads(report.difficulty_performance)

    return DiagnosticResponse(
        total_score=report.total_score,
        subtopic_breakdowns=[
            SubtopicBreakdownSchema(**b) for b in subtopic_breakdowns_data
        ],
        highest_impact_areas=[
            SubtopicBreakdownSchema(**b) for b in highest_impact_data
        ],
        regression_alerts=[
            RegressionAlertSchema(**r) for r in regression_alerts_data
        ],
        difficulty_performance=DifficultyPerformanceSchema(**difficulty_performance_data),
    )


@router.get("/{attempt_id}/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    attempt_id: int,
    user: User = Depends(get_current_user),
    service: MockAnalyticsService = Depends(get_mock_analytics_service),
) -> RecommendationsResponse:
    """Get actionable recommendations for a diagnostic report."""
    records = service.get_recommendations(attempt_id)

    recommendations = [
        RecommendationSchema(
            id=rec.id,
            subtopic_id=rec.subtopic_id,
            subtopic_name=rec.subtopic_name,
            current_accuracy=rec.current_accuracy,
            target_accuracy=rec.target_accuracy,
            estimated_point_gain=rec.estimated_point_gain,
            recommended_action=rec.recommended_action,
            formatted_string=_format_recommendation(rec),
            accepted_at=rec.accepted_at,
        )
        for rec in records
    ]

    return RecommendationsResponse(recommendations=recommendations)


@router.post("/{attempt_id}/recommendations/:accept", response_model=RecommendationSchema)
def accept_recommendation(
    attempt_id: int,
    user: User = Depends(get_current_user),
    service: MockAnalyticsService = Depends(get_mock_analytics_service),
) -> RecommendationSchema:
    """Accept a recommendation, feeding it into the queue as a high-priority item."""
    recommendations = service.get_recommendations(attempt_id)

    # Find the first unaccepted recommendation
    unaccepted = [r for r in recommendations if r.accepted_at is None]
    if not unaccepted:
        raise HTTPException(
            status_code=404,
            detail="No unaccepted recommendations found for this attempt",
        )

    rec = service.accept_recommendation(user.id, unaccepted[0].id)

    return RecommendationSchema(
        id=rec.id,
        subtopic_id=rec.subtopic_id,
        subtopic_name=rec.subtopic_name,
        current_accuracy=rec.current_accuracy,
        target_accuracy=rec.target_accuracy,
        estimated_point_gain=rec.estimated_point_gain,
        recommended_action=rec.recommended_action,
        formatted_string=_format_recommendation(rec),
        accepted_at=rec.accepted_at,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _format_recommendation(rec) -> str:
    """Format a recommendation record into a human-readable string."""
    gain = round(rec.estimated_point_gain, 1)
    return f"Fix {rec.subtopic_name} to gain +{gain} points"
