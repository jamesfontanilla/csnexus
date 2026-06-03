"""FastAPI router for the readiness score slice.

Mounts under ``/v1/readiness`` and exposes readiness score retrieval,
dashboard payload, and 30-day trend endpoints.

All routes require authentication via ``get_current_user``.

Validates: Requirements 2.3, 3.1, 3.4
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_exams.repository import MockExamRepository
from app.features.readiness.repository import ReadinessRepository
from app.features.readiness.schemas import (
    DashboardResponse,
    ReadinessResponse,
    SelfAssessmentHistoryResponse,
    SelfAssessmentPromptResponse,
    SelfAssessmentRequest,
    SelfAssessmentResponse,
    TrendResponse,
)
from app.features.readiness.service import ReadinessService
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/readiness", tags=["readiness"])


def get_readiness_service(db: Session = Depends(get_db)) -> ReadinessService:
    """Construct ReadinessService with all repository dependencies."""
    return ReadinessService(
        readiness_repo=ReadinessRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        flashcard_repo=FlashcardRepository(db=db),
        mock_exam_repo=MockExamRepository(db=db),
        content_repo=SubtopicRepository(db=db),
        question_repo=QuestionRepository(db=db),
    )


@router.get("", response_model=ReadinessResponse)
def get_current_readiness(
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> ReadinessResponse:
    """Return current readiness score with component breakdown and 7-day delta."""
    return service.get_current(user.id)


@router.get("/dashboard", response_model=DashboardResponse)
def get_readiness_dashboard(
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> DashboardResponse:
    """Return dashboard payload: score, components, delta, top impact areas, readiness level."""
    return service.get_dashboard(user.id)


@router.get("/trend", response_model=TrendResponse)
def get_readiness_trend(
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> TrendResponse:
    """Return 30-day readiness score trend with carry-forward for missing days."""
    trend_points = service.get_trend(user.id, days=30)
    return TrendResponse(trend=trend_points)


# ------------------------------------------------------------------
# Self-Assessment Calibration endpoints
# ------------------------------------------------------------------


@router.post("/self-assessment", response_model=SelfAssessmentResponse)
def submit_self_assessment(
    payload: SelfAssessmentRequest,
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> SelfAssessmentResponse:
    """Submit a self-assessed readiness score and receive calibration feedback.

    Validates self_assessed_score is 0-100 via Pydantic schema.
    """
    return service.submit_self_assessment(user.id, payload.self_assessed_score)


@router.get(
    "/self-assessment/history", response_model=SelfAssessmentHistoryResponse
)
def get_self_assessment_history(
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> SelfAssessmentHistoryResponse:
    """Return calibration history for the user."""
    return service.get_self_assessment_history(user.id)


@router.get(
    "/self-assessment/prompt", response_model=SelfAssessmentPromptResponse
)
def get_self_assessment_prompt(
    user: User = Depends(get_current_user),
    service: ReadinessService = Depends(get_readiness_service),
) -> SelfAssessmentPromptResponse:
    """Check if the self-assessment prompt is due (7+ days since last)."""
    return service.is_self_assessment_due(user.id)
