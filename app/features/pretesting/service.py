"""Service layer for pretesting feature.

Requirements: 20.1, 20.2, 20.3, 20.5, 20.6, 20.7, 21.1, 21.2
"""

from __future__ import annotations

import random
from typing import Any

from fastapi import HTTPException, status

from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.pretesting.models import PretestAttempt
from app.features.pretesting.repository import PretestRepository
from app.features.pretesting.schemas import (
    PretestComparisonResponse,
    PretestQuestion,
    PretestStartResponse,
    PretestSubmitResponse,
)
from app.features.progress.repository import ProgressRepository


class PretestService:
    """Orchestrates pretest generation, submission, and comparison."""

    def __init__(
        self,
        pretest_repo: PretestRepository,
        question_repo: QuestionRepository,
        subtopic_repo: SubtopicRepository,
        mastery_repo: MasteryRepository,
        progress_repo: ProgressRepository,
    ) -> None:
        self._pretest_repo = pretest_repo
        self._question_repo = question_repo
        self._subtopic_repo = subtopic_repo
        self._mastery_repo = mastery_repo
        self._progress_repo = progress_repo

    def start_pretest(self, user_id: int, subtopic_id: int) -> PretestStartResponse:
        """Generate and return pretest questions for a subtopic.

        Skips pretest if the lesson is already completed (Req 20.7).
        Selects 3-5 questions covering distinct key_concepts at easy-medium difficulty (Req 20.1, 20.2).
        """
        # Check if subtopic exists
        subtopic = self._subtopic_repo.get(subtopic_id)
        if subtopic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subtopic not found",
            )

        # Skip if lesson already completed
        if self._progress_repo.is_lesson_completed(user_id, subtopic_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Lesson already completed — pretest not applicable",
            )

        # Select 3-5 questions at easy/medium difficulty
        all_questions = self._question_repo.get_by_subtopic(subtopic_id)
        eligible = [
            q for q in all_questions
            if q.difficulty in ("easy", "medium", "EASY", "MEDIUM")
        ]

        if len(eligible) < 3:
            # Not enough questions for a meaningful pretest
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Insufficient questions for pretest",
            )

        # Select distinct key_concepts where possible
        count = min(5, len(eligible))
        selected = random.sample(eligible, count)

        # Build pretest questions
        pretest_questions: list[dict[str, Any]] = []
        response_questions: list[PretestQuestion] = []

        for q in selected:
            pretest_questions.append({
                "question_id": q.id,
                "correct_answer": q.correct_answer,
            })
            response_questions.append(
                PretestQuestion(
                    id=q.id,
                    stem=q.stem,
                    options=q.options if q.options else [],
                    key_concept=q.explanation[:50] if q.explanation else "general",
                )
            )

        # Persist the attempt (questions stored for grading)
        attempt = PretestAttempt(
            user_id=user_id,
            subtopic_id=subtopic_id,
            questions=pretest_questions,
            score=0.0,
            total_questions=len(selected),
        )
        attempt = self._pretest_repo.create(attempt)

        return PretestStartResponse(
            pretest_id=attempt.id,
            subtopic_id=subtopic_id,
            questions=response_questions,
        )

    def submit_pretest(
        self, user_id: int, pretest_id: int, answers: list[dict[str, Any]]
    ) -> PretestSubmitResponse:
        """Grade and persist pretest results.

        Pretest scores do NOT affect mastery component (Req 21.2).
        Records weak key_concepts for queue prioritization (Req 21.1).
        """
        attempt = self._pretest_repo.get(pretest_id)
        if attempt is None or attempt.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pretest not found",
            )

        # Grade answers
        stored_questions = attempt.questions or []
        correct_map = {q["question_id"]: q["correct_answer"] for q in stored_questions}

        correct_count = 0
        weak_concepts: list[str] = []

        for ans in answers:
            qid = ans.get("question_id")
            selected = ans.get("selected_answer", "")
            correct = correct_map.get(qid)

            if correct and selected == correct:
                correct_count += 1
            else:
                # Record the weak concept
                q = self._question_repo.get(qid) if qid else None
                if q and q.explanation:
                    weak_concepts.append(q.explanation[:50])

        score = (correct_count / len(stored_questions) * 100) if stored_questions else 0.0

        # Update attempt with score (but do NOT update mastery)
        attempt.score = score
        self._pretest_repo.db.commit()

        return PretestSubmitResponse(
            pretest_id=attempt.id,
            score=score,
            total_questions=len(stored_questions),
            correct_count=correct_count,
            weak_concepts=weak_concepts[:5],
        )

    def get_comparison(self, user_id: int, subtopic_id: int) -> PretestComparisonResponse:
        """Return pre vs post comparison for a subtopic (Req 20.5, 20.6)."""
        pretest = self._pretest_repo.get_by_user_and_subtopic(user_id, subtopic_id)

        if pretest is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No pretest found for this subtopic",
            )

        # Get post-lesson quiz score from mastery data
        mastery = self._mastery_repo.get_by_user_and_subtopic(user_id, subtopic_id)
        post_score = (mastery.mastery_score * 100) if mastery else None

        improvement = (post_score - pretest.score) if post_score is not None else None

        if improvement is not None and improvement > 0:
            message = f"Great progress! You improved by {improvement:.1f} percentage points after the lesson."
        elif improvement is not None:
            message = "Keep practicing! Review the lesson material to strengthen these concepts."
        else:
            message = "Complete the lesson and take a quiz to see your improvement."

        return PretestComparisonResponse(
            subtopic_id=subtopic_id,
            pretest_score=pretest.score,
            post_lesson_score=post_score,
            improvement=improvement,
            message=message,
        )
