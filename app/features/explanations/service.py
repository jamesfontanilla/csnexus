"""Business logic for inline question explanations and AI Tutor escalation.

Orchestrates between ExplanationRepository and TutorService.
All error conditions raise HTTPException. No DB access in this layer —
everything goes through the repository.

Validates: Requirements 7.2, 7.4, 7.5, 7.6, 8.1, 8.2, 8.3, 8.4
"""

from __future__ import annotations

import logging
from datetime import date, timezone
from datetime import datetime as dt
from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from app.features.explanations.models import QuestionExplanation
from app.features.explanations.repository import ExplanationRepository

if TYPE_CHECKING:
    from app.features.tutor.service import TutorService

logger = logging.getLogger(__name__)

# Maximum AI Tutor escalations allowed per user per day (Requirement 8.3)
MAX_DAILY_ESCALATIONS = 20


class ExplanationService:
    """Manages static question explanations and AI Tutor escalation.

    Receives ExplanationRepository and optionally TutorService via constructor
    injection. Never blocks the answer submission flow — missing explanations
    return None rather than raising.
    """

    def __init__(
        self,
        *,
        explanation_repo: ExplanationRepository,
        tutor_service: "TutorService | None" = None,
    ) -> None:
        self._explanation_repo = explanation_repo
        self._tutor_service = tutor_service
        # In-memory daily escalation counter: {(user_id, date_str): count}
        # In a production system this would be persisted or use Redis,
        # but for the current architecture a simple dict suffices since
        # the service is request-scoped (re-created per request).
        # We'll query the tutor repo for today's interaction count instead.
        self._escalation_counts: dict[tuple[int, str], int] = {}

    def get_explanation(self, question_id: int) -> QuestionExplanation | None:
        """Return the explanation for a question, or None if not stored.

        Never raises on not-found — the answer submission flow must not be
        blocked by missing explanations (Requirement 7.4).
        """
        return self._explanation_repo.get_by_question_id(question_id)

    def get_bulk_explanations(
        self, question_ids: list[int]
    ) -> dict[int, QuestionExplanation | None]:
        """Return explanations for multiple questions.

        Every requested ID appears in the result dict. Questions without a
        stored explanation are mapped to None (Requirement 7.6).
        """
        return self._explanation_repo.get_bulk(question_ids)

    def escalate_to_tutor(
        self,
        user_id: int,
        question_id: int,
        selected_answer: str | None = None,
    ) -> dict:
        """Escalate a question to the AI Tutor for deeper explanation.

        Checks the daily escalation limit (20/day per user). If the limit is
        exceeded, raises HTTP 429. Otherwise forwards the question context to
        the TutorService (Requirement 8.1, 8.2, 8.3, 8.4).
        """
        if self._tutor_service is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI Tutor service is not available",
            )

        # Check daily rate limit
        today = dt.now(timezone.utc).date()
        daily_count = self._get_daily_escalation_count(user_id, today)

        if daily_count >= MAX_DAILY_ESCALATIONS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Daily AI Tutor escalation limit reached (20/day). "
                    "Try reviewing the lesson for the relevant subtopic."
                ),
            )

        # Forward to TutorService (Requirement 8.1, 8.2)
        tutor_response = self._tutor_service.explain(
            user_id=user_id,
            question_id=question_id,
            selected_answer=selected_answer,
        )

        # Increment escalation count
        self._increment_daily_escalation_count(user_id, today)

        return {
            "interaction_id": tutor_response.interaction_id,
            "response_text": tutor_response.response_text,
            "interaction_type": tutor_response.interaction_type,
        }

    def _get_daily_escalation_count(self, user_id: int, today: date) -> int:
        """Get the number of escalations a user has made today.

        Uses the in-memory counter keyed by (user_id, date_string).
        """
        key = (user_id, today.isoformat())
        return self._escalation_counts.get(key, 0)

    def _increment_daily_escalation_count(self, user_id: int, today: date) -> None:
        """Increment the daily escalation counter for a user."""
        key = (user_id, today.isoformat())
        self._escalation_counts[key] = self._escalation_counts.get(key, 0) + 1
