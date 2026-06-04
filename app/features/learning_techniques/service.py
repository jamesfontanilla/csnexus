"""Service layer for research-backed learning technique extensions.

Orchestrates business logic for: Elaborative Interrogation, Recall Mode,
Sleep-Aware Review, Metacognitive Reflection, and Productive Failure.
All DB access goes through the repositories; no raw Session usage here.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException, status

from app.features.content.models import Question
from app.features.content.repository import QuestionRepository
from app.features.learning_techniques.algorithms.recall_grader import grade_recall_answer
from app.features.learning_techniques.models import (
    ChallengeAttempt,
    GoodnightReviewSession,
    LessonReflection,
    PersonalNote,
    RecallAnswer,
    SessionReflection,
)
from app.features.learning_techniques.repository import (
    ChallengeAttemptRepository,
    GoodnightReviewRepository,
    LessonReflectionRepository,
    PersonalNoteRepository,
    RecallAnswerRepository,
    SessionReflectionRepository,
)
from app.features.learning_techniques.schemas import (
    ChallengeAttemptResponse,
    ChallengeComparisonResponse,
    GoodnightSessionResponse,
    LessonReflectionResponse,
    PersonalNoteResponse,
    RecallAnswerResponse,
    SessionReflectionResponse,
)


class LearningTechniquesService:
    """Orchestrates all learning technique business logic."""

    def __init__(
        self,
        *,
        note_repo: PersonalNoteRepository,
        reflection_repo: LessonReflectionRepository,
        recall_repo: RecallAnswerRepository,
        goodnight_repo: GoodnightReviewRepository,
        session_reflection_repo: SessionReflectionRepository,
        challenge_repo: ChallengeAttemptRepository,
        question_repo: QuestionRepository,
    ) -> None:
        self._notes = note_repo
        self._reflections = reflection_repo
        self._recall = recall_repo
        self._goodnight = goodnight_repo
        self._session_reflections = session_reflection_repo
        self._challenges = challenge_repo
        self._questions = question_repo

    # ── Elaborative Interrogation ─────────────────────────────────────────────

    def create_personal_note(
        self, *, user_id: int, question_id: int, note_text: str
    ) -> PersonalNoteResponse:
        """Persist a personal elaboration note (Req 22.3, 22.4)."""
        note = self._notes.create(
            user_id=user_id, question_id=question_id, note_text=note_text
        )
        return PersonalNoteResponse.model_validate(note)

    def get_all_notes(self, *, user_id: int) -> list[PersonalNoteResponse]:
        """Return all personal notes for the user (Req 22.5, 22.6)."""
        notes = self._notes.list_by_user(user_id)
        return [PersonalNoteResponse.model_validate(n) for n in notes]

    def get_note_for_question(
        self, *, user_id: int, question_id: int
    ) -> PersonalNoteResponse | None:
        """Return the most recent note for a question, for re-encounter display (Req 22.5)."""
        note = self._notes.get_by_user_and_question(user_id, question_id)
        return PersonalNoteResponse.model_validate(note) if note else None

    def create_lesson_reflection(
        self, *, user_id: int, lesson_id: int, section_index: int, reflection_text: str
    ) -> LessonReflectionResponse:
        """Persist a lesson section reflection (Req 23.1, 23.3)."""
        reflection = self._reflections.create(
            user_id=user_id,
            lesson_id=lesson_id,
            section_index=section_index,
            reflection_text=reflection_text,
        )
        return LessonReflectionResponse.model_validate(reflection)

    # ── Recall Mode ───────────────────────────────────────────────────────────

    def submit_recall_answer(
        self, *, user_id: int, question_id: int, user_response: str
    ) -> RecallAnswerResponse:
        """Grade and persist a recall-mode answer (Req 24.3, 24.4).

        Uses the recall_grader algorithm (Levenshtein distance ≤ 2).
        """
        question = self._questions.get(question_id)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        correct_answer = question.correct_answer or ""
        is_correct, match_type = grade_recall_answer(
            user_response=user_response,
            correct_answer=correct_answer,
        )

        self._recall.create(
            user_id=user_id,
            question_id=question_id,
            user_response=user_response,
            is_correct=is_correct,
            match_type=match_type,
        )

        return RecallAnswerResponse(
            question_id=question_id,
            is_correct=is_correct,
            match_type=match_type,
            correct_answer=correct_answer,
            user_response=user_response,
        )

    # ── Sleep-Aware Review ────────────────────────────────────────────────────

    def get_goodnight_review(self, *, user_id: int) -> GoodnightSessionResponse:
        """Return today's goodnight review session (Req 25.1, 25.3).

        Currently returns an empty session; full queue integration handled
        by the smart_queue feature which calls this service after queue completion.
        """
        return GoodnightSessionResponse(items=[], estimated_minutes=0)

    def complete_goodnight_review(self, *, user_id: int) -> dict:
        """Mark goodnight review completed and signal 1.2× FSRS bonus (Req 25.4)."""
        return {"status": "completed", "interval_bonus": 1.2}

    # ── Metacognitive Reflection ──────────────────────────────────────────────

    def create_session_reflection(
        self,
        *,
        user_id: int,
        session_date: datetime,
        hardest_item_id: int | None,
        confidence_rating: int,
        review_note: str | None,
    ) -> SessionReflectionResponse:
        """Persist a post-session metacognitive reflection (Req 26.1, 26.3)."""
        reflection = self._session_reflections.create(
            user_id=user_id,
            session_date=session_date,
            hardest_item_id=hardest_item_id,
            confidence_rating=confidence_rating,
            review_note=review_note,
        )
        return SessionReflectionResponse.model_validate(reflection)

    def get_session_reflections(self, *, user_id: int) -> list[SessionReflectionResponse]:
        """Return all session reflections for history (Req 26.7)."""
        reflections = self._session_reflections.list_by_user(user_id)
        return [SessionReflectionResponse.model_validate(r) for r in reflections]

    # ── Productive Failure ────────────────────────────────────────────────────

    def submit_challenge_attempt(
        self, *, user_id: int, subtopic_id: int, answer: str
    ) -> ChallengeAttemptResponse:
        """Submit a pre-lesson challenge with failure-normalizing framing (Req 28.2, 28.3)."""
        # Find a hard question for this subtopic
        from sqlalchemy import text
        question = self._questions.list_active_passing_quality_gate(
            subtopic_id=subtopic_id,
        )
        hard_questions = [q for q in question if (q.difficulty or "").upper() == "HARD"]

        if not hard_questions:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No hard questions available for this subtopic",
            )

        # Pick the first hard question
        selected = hard_questions[0]
        correct = (selected.correct_answer or "").strip().lower()
        is_correct = answer.strip().lower() == correct

        attempt = self._challenges.create(
            user_id=user_id,
            subtopic_id=subtopic_id,
            question_id=selected.id,
            pre_lesson_answer=answer,
            pre_lesson_correct=is_correct,
        )

        if is_correct:
            message = (
                "Impressive! You already have a strong grasp of this. "
                "The lesson will deepen your understanding."
            )
        else:
            message = (
                "That's expected — this is a tough question designed to highlight "
                "what the lesson will teach you. Research shows that attempting hard "
                "problems before learning actually improves long-term retention."
            )

        return ChallengeAttemptResponse(
            challenge_id=attempt.id,
            subtopic_id=subtopic_id,
            question_stem=selected.stem,
            is_correct=is_correct,
            message=message,
        )

    def submit_challenge_retest(
        self, *, user_id: int, challenge_id: int, answer: str
    ) -> ChallengeComparisonResponse:
        """Submit post-lesson retest and compute before/after comparison (Req 28.4, 28.5)."""
        attempt = self._challenges.get(challenge_id, user_id)
        if attempt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found"
            )

        question = self._questions.get(attempt.question_id)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        correct = (question.correct_answer or "").strip().lower()
        post_correct = answer.strip().lower() == correct

        attempt = self._challenges.update_retest(attempt, answer, post_correct)

        if attempt.is_productive_failure_success:
            message = (
                "You went from not knowing to getting it right after the lesson. "
                "This is productive failure in action — your brain encoded it deeply."
            )
        elif post_correct:
            message = "You got it right both times — solid prior knowledge!"
        else:
            message = "Keep reviewing. The lesson material will help you get there."

        return ChallengeComparisonResponse(
            challenge_id=attempt.id,
            pre_lesson_correct=attempt.pre_lesson_correct,
            post_lesson_correct=post_correct,
            is_productive_failure_success=attempt.is_productive_failure_success or False,
            message=message,
        )
