"""FastAPI router for the exam date onboarding flow.

Mounts under ``/v1/onboarding`` and exposes endpoints for initial
onboarding submission, exam date updates, and plan summary retrieval.

All routes require authentication via ``get_current_user``.

Requirements: 16.1, 16.2, 17.4, 18.1
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.planner.onboarding_service import OnboardingService
from app.features.planner.repository import (
    OnboardingRepository,
    StudyPlanRepository,
)
from app.features.planner.schemas import (
    ExamDateUpdateRequest,
    OnboardingRequest,
    PlanSummaryResponse,
)
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/onboarding", tags=["onboarding"])


def get_onboarding_service(db: Session = Depends(get_db)) -> OnboardingService:
    """Construct OnboardingService with all repository dependencies."""
    return OnboardingService(
        onboarding_repo=OnboardingRepository(db=db),
        plan_repo=StudyPlanRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        content_repo=SubtopicRepository(db=db),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def submit_onboarding(
    payload: OnboardingRequest,
    user: User = Depends(get_current_user),
    service: OnboardingService = Depends(get_onboarding_service),
) -> dict:
    """Submit exam date and preferences to complete onboarding.

    Creates an OnboardingProfile, generates a personalized StudyPlan,
    and returns a confirmation with plan metrics.
    """
    return service.submit_onboarding(
        user_id=user.id,
        exam_date=payload.exam_date,
        exam_category=payload.exam_category,
        time_budget_minutes=payload.time_budget_minutes,
    )


@router.patch("/exam-date")
def update_exam_date(
    payload: ExamDateUpdateRequest,
    user: User = Depends(get_current_user),
    service: OnboardingService = Depends(get_onboarding_service),
) -> dict:
    """Update the exam date and regenerate the study plan.

    Abandons the existing plan and creates a new one aligned to the
    updated exam date.
    """
    return service.update_exam_date(
        user_id=user.id,
        new_exam_date=payload.exam_date,
    )


@router.get("/plan-summary", response_model=PlanSummaryResponse)
def get_plan_summary(
    user: User = Depends(get_current_user),
    service: OnboardingService = Depends(get_onboarding_service),
) -> PlanSummaryResponse:
    """Return the generated study plan summary for the authenticated user."""
    return service.get_plan_summary(user.id)
