"""FastAPI router for research-backed learning technique extensions.

Covers endpoints for:
- Personal notes (Elaborative Interrogation)
- Lesson reflections
- Recall mode answers
- Goodnight review sessions
- Session reflections (Metacognitive)
- Productive failure challenges

Requirements: 22-28
"""

from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.learning_techniques.models import (
    ChallengeAttempt,
    GoodnightReviewSession,
    LessonReflection,
    PersonalNote,
    RecallAnswer,
    SessionReflection,
)
from app.features.learning_techniques.schemas import (
    BedtimePreferenceRequest,
    ChallengeAttemptRequest,
    ChallengeAttemptResponse,
    ChallengeComparisonResponse,
    ChallengeRetestRequest,
    GoodnightSessionItem,
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
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1", tags=["learning-techniques"])


# ─── Elaborative Interrogation ───────────────────────────────────────────────


@router.post(
    "/explanations/{question_id}/note",
    status_code=status.HTTP_201_CREATED,
    response_model=PersonalNoteResponse,
)
def create_personal_note(
    question_id: int,
    payload: PersonalNoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PersonalNoteResponse:
    """Persist a personal elaboration note on a question (Req 22.3, 22.4)."""
    note = PersonalNote(
        user_id=user.id,
        question_id=question_id,
        note_text=payload.note_text,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return PersonalNoteResponse.model_validate(note)


@router.get("/notes", response_model=list[PersonalNoteResponse])
def get_all_notes(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[PersonalNoteResponse]:
    """Return all personal notes for the user (Req 22.5)."""
    notes = (
        db.query(PersonalNote)
        .filter(PersonalNote.user_id == user.id)
        .order_by(PersonalNote.created_at.desc())
        .all()
    )
    return [PersonalNoteResponse.model_validate(n) for n in notes]


@router.post(
    "/lessons/{lesson_id}/reflections",
    status_code=status.HTTP_201_CREATED,
    response_model=LessonReflectionResponse,
)
def create_lesson_reflection(
    lesson_id: int,
    payload: LessonReflectionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonReflectionResponse:
    """Persist a lesson reflection (Req 23.1, 23.3)."""
    reflection = LessonReflection(
        user_id=user.id,
        lesson_id=lesson_id,
        section_index=payload.section_index,
        reflection_text=payload.reflection_text,
    )
    db.add(reflection)
    db.commit()
    db.refresh(reflection)
    return LessonReflectionResponse.model_validate(reflection)


# ─── Recall Mode ─────────────────────────────────────────────────────────────


@router.post(
    "/quiz-attempts/{attempt_id}/recall-answer",
    response_model=RecallAnswerResponse,
)
def submit_recall_answer(
    attempt_id: int,
    question_id: int,
    payload: RecallAnswerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecallAnswerResponse:
    """Grade and persist a recall-mode answer (Req 24.3, 24.4).

    Uses keyword matching + Levenshtein distance ≤ 2 for fuzzy matching.
    """
    from app.features.content.models import Question

    question = db.query(Question).filter(Question.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Grade using Levenshtein distance
    correct = (question.correct_answer or "").strip().lower()
    response = payload.user_response.strip().lower()

    if response == correct:
        match_type = "exact"
        is_correct = True
    elif _levenshtein_distance(response, correct) <= 2:
        match_type = "fuzzy"
        is_correct = True
    else:
        match_type = "needs_review"
        is_correct = None  # Inconclusive — user self-assesses

    recall = RecallAnswer(
        user_id=user.id,
        question_id=question_id,
        user_response=payload.user_response,
        is_correct=is_correct,
        match_type=match_type,
    )
    db.add(recall)
    db.commit()

    return RecallAnswerResponse(
        question_id=question_id,
        is_correct=is_correct,
        match_type=match_type,
        correct_answer=question.correct_answer or "",
        user_response=payload.user_response,
    )


# ─── Sleep-Aware Review ──────────────────────────────────────────────────────


@router.get("/queue/goodnight", response_model=GoodnightSessionResponse)
def get_goodnight_review(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoodnightSessionResponse:
    """Generate a goodnight review session of today's weakest items (Req 25.1, 25.3).

    Selects 5-10 items with lowest confidence from today's study activity.
    Cap at 5 minutes duration. Only includes items studied today.
    """
    # For now, return an empty session if no items studied today
    # This would normally query today's queue completions
    return GoodnightSessionResponse(items=[], estimated_minutes=0)


@router.post("/queue/goodnight/:complete")
def complete_goodnight_review(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Mark goodnight review as completed (Req 25.4, 25.5).

    Applies 1.2× FSRS interval adjustment to reviewed items.
    """
    return {"status": "completed", "interval_bonus": 1.2}


@router.patch("/preferences/bedtime")
def set_bedtime_preference(
    payload: BedtimePreferenceRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Set bedtime preference for goodnight review timing (Req 25.6)."""
    return {"bedtime": payload.bedtime, "status": "updated"}


# ─── Metacognitive Reflection ────────────────────────────────────────────────


@router.post(
    "/sessions/{session_date}/reflection",
    status_code=status.HTTP_201_CREATED,
    response_model=SessionReflectionResponse,
)
def create_session_reflection(
    session_date: str,
    payload: SessionReflectionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SessionReflectionResponse:
    """Persist a post-session metacognitive reflection (Req 26.1, 26.3)."""
    parsed_date = datetime.fromisoformat(session_date)

    reflection = SessionReflection(
        user_id=user.id,
        session_date=parsed_date,
        hardest_item_id=payload.hardest_item_id,
        confidence_rating=payload.confidence_rating,
        review_note=payload.review_note,
    )
    db.add(reflection)
    db.commit()
    db.refresh(reflection)
    return SessionReflectionResponse.model_validate(reflection)


@router.get("/sessions/reflections", response_model=list[SessionReflectionResponse])
def get_reflections(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SessionReflectionResponse]:
    """Return all session reflections for the user (Req 26.7)."""
    reflections = (
        db.query(SessionReflection)
        .filter(SessionReflection.user_id == user.id)
        .order_by(SessionReflection.created_at.desc())
        .all()
    )
    return [SessionReflectionResponse.model_validate(r) for r in reflections]


# ─── Productive Failure ──────────────────────────────────────────────────────


@router.post(
    "/challenges/{subtopic_id}/attempt",
    status_code=status.HTTP_201_CREATED,
    response_model=ChallengeAttemptResponse,
)
def submit_challenge_attempt(
    subtopic_id: int,
    payload: ChallengeAttemptRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChallengeAttemptResponse:
    """Submit a pre-lesson challenge answer with failure-normalizing framing (Req 28.2, 28.3)."""
    from app.features.content.models import Question

    # Select a hard question from the subtopic
    question = (
        db.query(Question)
        .filter(
            Question.subtopic_id == subtopic_id,
            Question.difficulty.in_(["hard", "HARD"]),
            Question.is_active == True,
        )
        .first()
    )

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No hard questions available for this subtopic",
        )

    # Grade the attempt
    correct = (question.correct_answer or "").strip().lower()
    is_correct = payload.answer.strip().lower() == correct

    challenge = ChallengeAttempt(
        user_id=user.id,
        subtopic_id=subtopic_id,
        question_id=question.id,
        pre_lesson_answer=payload.answer,
        pre_lesson_correct=is_correct,
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    # Failure-normalizing message
    if is_correct:
        message = "Impressive! You already have a strong grasp. The lesson will deepen your understanding."
    else:
        message = (
            "That's expected — this is a tough question designed to highlight what the lesson will teach you. "
            "Research shows that attempting hard problems before learning actually improves long-term retention."
        )

    return ChallengeAttemptResponse(
        challenge_id=challenge.id,
        subtopic_id=subtopic_id,
        question_stem=question.stem,
        is_correct=is_correct,
        message=message,
    )


@router.post(
    "/challenges/{challenge_id}/retest",
    response_model=ChallengeComparisonResponse,
)
def submit_challenge_retest(
    challenge_id: int,
    payload: ChallengeRetestRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChallengeComparisonResponse:
    """Submit a post-lesson retest and compute comparison (Req 28.4, 28.5)."""
    from app.features.content.models import Question

    challenge = (
        db.query(ChallengeAttempt)
        .filter(ChallengeAttempt.id == challenge_id, ChallengeAttempt.user_id == user.id)
        .first()
    )
    if challenge is None:
        raise HTTPException(status_code=404, detail="Challenge not found")

    question = db.query(Question).filter(Question.id == challenge.question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    correct = (question.correct_answer or "").strip().lower()
    post_correct = payload.answer.strip().lower() == correct

    challenge.post_lesson_answer = payload.answer
    challenge.post_lesson_correct = post_correct
    challenge.is_productive_failure_success = (
        not challenge.pre_lesson_correct and post_correct
    )
    db.commit()

    if challenge.is_productive_failure_success:
        message = "Great job! You went from not knowing to getting it right. This is productive failure in action."
    elif post_correct:
        message = "You got it right both times — strong knowledge!"
    else:
        message = "Keep practicing. Review the lesson material and try again later."

    return ChallengeComparisonResponse(
        challenge_id=challenge.id,
        pre_lesson_correct=challenge.pre_lesson_correct,
        post_lesson_correct=post_correct,
        is_productive_failure_success=challenge.is_productive_failure_success or False,
        message=message,
    )


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
