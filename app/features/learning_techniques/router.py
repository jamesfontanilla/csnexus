"""FastAPI router for research-backed learning technique extensions.

Thin routing layer — all business logic lives in LearningTechniquesService.
Covers endpoints for:
- Personal notes (Elaborative Interrogation, Req 22)
- Lesson reflections (Req 23)
- Recall mode answers (Req 24)
- Goodnight review sessions (Req 25)
- Session reflections / Metacognitive Reflection (Req 26)
- Productive failure challenges (Req 28)
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import QuestionRepository
from app.features.learning_techniques.repository import (
    ChallengeAttemptRepository,
    GoodnightReviewRepository,
    LessonReflectionRepository,
    PersonalNoteRepository,
    RecallAnswerRepository,
    SessionReflectionRepository,
)
from app.features.learning_techniques.schemas import (
    BedtimePreferenceRequest,
    ChallengeAttemptRequest,
    ChallengeAttemptResponse,
    ChallengeComparisonResponse,
    ChallengeRetestRequest,
    GoodnightSessionResponse,
    LessonReflectionCreate,
    LessonReflectionResponse,
    PersonalNoteCreate,
    PersonalNoteResponse,
    RecallAnswerRequest,
    RecallAnswerResponse,
    SessionReflectionCreate,
    SessionReflectionResponse,
)
from app.features.learning_techniques.service import LearningTechniquesService
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1", tags=["learning-techniques"])


def _get_service(db: Session = Depends(get_db)) -> LearningTechniquesService:
    return LearningTechniquesService(
        note_repo=PersonalNoteRepository(db),
        reflection_repo=LessonReflectionRepository(db),
        recall_repo=RecallAnswerRepository(db),
        goodnight_repo=GoodnightReviewRepository(db),
        session_reflection_repo=SessionReflectionRepository(db),
        challenge_repo=ChallengeAttemptRepository(db),
        question_repo=QuestionRepository(db),
    )


# ── Elaborative Interrogation ─────────────────────────────────────────────────


@router.post(
    "/explanations/{question_id}/note",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonalNoteResponse,
)
def create_personal_note(
    question_id: int,
    payload: PersonalNoteCreate,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> PersonalNoteResponse:
    """Persist a personal elaboration note on a question (Req 22.3, 22.4)."""
    return service.create_personal_note(
        user_id=user.id, question_id=question_id, note_text=payload.note_text
    )


@router.get("/notes", response_model=list[PersonalNoteResponse])
def get_all_notes(
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> list[PersonalNoteResponse]:
    """Return all personal notes for the user (Req 22.5, 22.6)."""
    return service.get_all_notes(user_id=user.id)


@router.post(
    "/lessons/{lesson_id}/reflections",
    status_code=status.HTTP_201_CREATED,
    response_model=LessonReflectionResponse,
)
def create_lesson_reflection(
    lesson_id: int,
    payload: LessonReflectionCreate,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> LessonReflectionResponse:
    """Persist a lesson section reflection (Req 23.1, 23.3)."""
    return service.create_lesson_reflection(
        user_id=user.id,
        lesson_id=lesson_id,
        section_index=payload.section_index,
        reflection_text=payload.reflection_text,
    )


# ── Recall Mode ───────────────────────────────────────────────────────────────


@router.post(
    "/quiz-attempts/{attempt_id}/recall-answer",
    response_model=RecallAnswerResponse,
)
def submit_recall_answer(
    attempt_id: int,
    question_id: int,
    payload: RecallAnswerRequest,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> RecallAnswerResponse:
    """Grade and persist a recall-mode answer using Levenshtein ≤ 2 (Req 24.3, 24.4)."""
    return service.submit_recall_answer(
        user_id=user.id,
        question_id=question_id,
        user_response=payload.user_response,
    )


# ── Sleep-Aware Review ────────────────────────────────────────────────────────


@router.get("/queue/goodnight", response_model=GoodnightSessionResponse)
def get_goodnight_review(
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> GoodnightSessionResponse:
    """Return today's goodnight review session (Req 25.1, 25.3)."""
    return service.get_goodnight_review(user_id=user.id)


@router.post("/queue/goodnight/:complete")
def complete_goodnight_review(
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> dict:
    """Mark goodnight review completed; signals 1.2× FSRS interval bonus (Req 25.4)."""
    return service.complete_goodnight_review(user_id=user.id)


@router.patch("/preferences/bedtime")
def set_bedtime_preference(
    payload: BedtimePreferenceRequest,
    user: User = Depends(get_current_user),
) -> dict:
    """Set bedtime preference for goodnight review timing (Req 25.6)."""
    # Preference stored in user settings — stub returning updated value
    return {"bedtime": payload.bedtime, "status": "updated"}


# ── Metacognitive Reflection ──────────────────────────────────────────────────


@router.post(
    "/sessions/{session_date}/reflection",
    status_code=status.HTTP_201_CREATED,
    response_model=SessionReflectionResponse,
)
def create_session_reflection(
    session_date: str,
    payload: SessionReflectionCreate,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> SessionReflectionResponse:
    """Persist a post-session metacognitive reflection (Req 26.1, 26.3)."""
    parsed_date = datetime.fromisoformat(session_date)
    return service.create_session_reflection(
        user_id=user.id,
        session_date=parsed_date,
        hardest_item_id=payload.hardest_item_id,
        confidence_rating=payload.confidence_rating,
        review_note=payload.review_note,
    )


@router.get("/sessions/reflections", response_model=list[SessionReflectionResponse])
def get_reflections(
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> list[SessionReflectionResponse]:
    """Return all session reflections for history (Req 26.7)."""
    return service.get_session_reflections(user_id=user.id)


# ── Productive Failure ────────────────────────────────────────────────────────


@router.post(
    "/challenges/{subtopic_id}/attempt",
    status_code=status.HTTP_201_CREATED,
    response_model=ChallengeAttemptResponse,
)
def submit_challenge_attempt(
    subtopic_id: int,
    payload: ChallengeAttemptRequest,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> ChallengeAttemptResponse:
    """Submit a pre-lesson challenge with failure-normalizing framing (Req 28.2, 28.3)."""
    return service.submit_challenge_attempt(
        user_id=user.id, subtopic_id=subtopic_id, answer=payload.answer
    )


@router.post(
    "/challenges/{challenge_id}/retest",
    response_model=ChallengeComparisonResponse,
)
def submit_challenge_retest(
    challenge_id: int,
    payload: ChallengeRetestRequest,
    user: User = Depends(get_current_user),
    service: LearningTechniquesService = Depends(_get_service),
) -> ChallengeComparisonResponse:
    """Submit post-lesson retest and return before/after comparison (Req 28.4, 28.5)."""
    return service.submit_challenge_retest(
        user_id=user.id, challenge_id=challenge_id, answer=payload.answer
    )
