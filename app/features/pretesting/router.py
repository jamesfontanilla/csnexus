"""FastAPI router for pretesting endpoints.

Mounts under /v1/pretests. Provides pretest generation, submission,
and pre/post comparison.

Requirements: 20.1, 20.3, 20.4, 20.5, 20.6, 20.7
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.pretesting.repository import PretestRepository
from app.features.pretesting.schemas import (
    PretestComparisonResponse,
    PretestStartResponse,
    PretestSubmitRequest,
    PretestSubmitResponse,
)
from app.features.pretesting.service import PretestService
from app.features.progress.repository import ProgressRepository
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/pretests", tags=["pretests"])


def get_pretest_service(db: Session = Depends(get_db)) -> PretestService:
    """Construct PretestService with all dependencies."""
    return PretestService(
        pretest_repo=PretestRepository(db=db),
        question_repo=QuestionRepository(db=db),
        subtopic_repo=SubtopicRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        progress_repo=ProgressRepository(db=db),
    )


@router.post(
    "/{subtopic_id}/start",
    status_code=status.HTTP_201_CREATED,
    response_model=PretestStartResponse,
)
def start_pretest(
    subtopic_id: int,
    user: User = Depends(get_current_user),
    service: PretestService = Depends(get_pretest_service),
) -> PretestStartResponse:
    """Generate and return pretest questions for a subtopic.

    Skips if lesson already completed (returns 409).
    """
    return service.start_pretest(user.id, subtopic_id)


@router.post("/{pretest_id}/submit", response_model=PretestSubmitResponse)
def submit_pretest(
    pretest_id: int,
    payload: PretestSubmitRequest,
    user: User = Depends(get_current_user),
    service: PretestService = Depends(get_pretest_service),
) -> PretestSubmitResponse:
    """Submit pretest answers. Does NOT affect mastery scores."""
    answers = [
        {"question_id": a.question_id, "selected_answer": a.selected_answer}
        for a in payload.answers
    ]
    return service.submit_pretest(user.id, pretest_id, answers)


@router.get(
    "/{subtopic_id}/comparison",
    response_model=PretestComparisonResponse,
)
def get_comparison(
    subtopic_id: int,
    user: User = Depends(get_current_user),
    service: PretestService = Depends(get_pretest_service),
) -> PretestComparisonResponse:
    """Return pre vs post comparison for a subtopic."""
    return service.get_comparison(user.id, subtopic_id)
