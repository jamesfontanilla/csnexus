"""FastAPI router for the AI tutor feature.

Mounts under ``/v1/tutor`` and exposes rule-based explanation endpoints.
All routes require authentication.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import (
    LessonRepository,
    QuestionRepository,
    SubtopicRepository,
)
from app.features.mastery.repository import MasteryRepository
from app.features.tutor.algorithms.cross_lesson_registry import CrossLessonRegistry
from app.features.tutor.repository import TutorRepository
from app.features.tutor.schemas import (
    LessonChatRequest,
    LessonChatResponse,
    RateRequest,
    SimilarQuestionResponse,
    StepByStepResponse,
    TutorRequest,
    TutorResponse,
)
from app.features.tutor.service import TutorService
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/tutor", tags=["tutor"])


# ---------------------------------------------------------------------------
# Cross-Lesson Registry dependency (built once at startup, stored on app.state)
# ---------------------------------------------------------------------------


def get_cross_lesson_registry(request: Request) -> CrossLessonRegistry:
    """Return the CrossLessonRegistry built at app startup.

    The registry is stored on ``app.state.cross_lesson_registry`` by the
    lifespan handler in ``app/main.py``. If the build failed at startup,
    the lifespan stores an empty registry so this always returns a usable
    instance (the engine handles empty registries gracefully per Req 4.7).
    """
    return request.app.state.cross_lesson_registry


def _get_tutor_service(
    db: Session = Depends(get_db),
    registry: CrossLessonRegistry = Depends(get_cross_lesson_registry),
) -> TutorService:
    """Construct TutorService for the request."""
    return TutorService(
        tutor_repo=TutorRepository(db=db),
        question_repo=QuestionRepository(db=db),
        subtopic_repo=SubtopicRepository(db=db),
        lesson_repo=LessonRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        cross_lesson_registry=registry,
    )


@router.post("/explain", response_model=TutorResponse)
def tutor_explain(
    payload: TutorRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> TutorResponse:
    """Get an explanation for a question's answer."""
    return service.explain(
        user_id=user.id,
        question_id=payload.question_id,
        selected_answer=payload.selected_answer,
    )


@router.post("/simplify", response_model=TutorResponse)
def tutor_simplify(
    payload: TutorRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> TutorResponse:
    """Get a simplified explanation for a question."""
    return service.simplify(
        user_id=user.id,
        question_id=payload.question_id,
    )


@router.post("/similar", response_model=SimilarQuestionResponse)
def tutor_similar(
    payload: TutorRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> SimilarQuestionResponse:
    """Generate a similar practice question."""
    return service.similar_question(
        user_id=user.id,
        question_id=payload.question_id,
    )


@router.post("/hint", response_model=TutorResponse)
def tutor_hint(
    payload: TutorRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> TutorResponse:
    """Get a hint for a question without revealing the answer."""
    return service.hint(
        user_id=user.id,
        question_id=payload.question_id,
    )


@router.post("/step-by-step", response_model=StepByStepResponse)
def tutor_step_by_step(
    payload: TutorRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> StepByStepResponse:
    """Get a step-by-step breakdown of the solution."""
    return service.step_by_step_explain(
        user_id=user.id,
        question_id=payload.question_id,
    )


@router.post("/interactions/{interaction_id}:rate")
def rate_interaction(
    interaction_id: int,
    payload: RateRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> dict[str, str]:
    """Rate a tutor interaction as helpful or not."""
    service.rate_interaction(interaction_id, payload.helpful)
    return {"status": "ok"}


@router.post("/lesson-chat", response_model=LessonChatResponse)
def lesson_chat(
    payload: LessonChatRequest,
    user: User = Depends(get_current_user),
    service: TutorService = Depends(_get_tutor_service),
) -> LessonChatResponse:
    """Chat with the AI study buddy about the current lesson.

    Accepts the user's message along with the subtopic ID and optional
    active section index. Returns a contextual response generated from
    the lesson's own content.
    """
    return service.lesson_chat(
        user_id=user.id,
        subtopic_id=payload.subtopic_id,
        message=payload.message,
        active_section_index=payload.active_section_index,
        context_json=payload.context_json,
    )
