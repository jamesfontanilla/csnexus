"""Repository for question explanation persistence and retrieval.

Handles all database access for QuestionExplanation records.

Validates: Requirements 7.1, 7.4, 7.5, 7.6
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.explanations.models import QuestionExplanation
from app.infrastructure.repositories.base import BaseRepository


class ExplanationRepository(BaseRepository[QuestionExplanation]):
    """Persistence layer for question explanations."""

    model = QuestionExplanation

    def __init__(self, db: Session) -> None:
        super().__init__(db=db)

    def get_by_question_id(self, question_id: int) -> QuestionExplanation | None:
        """Return the explanation for a given question, or None if not stored.

        Uses the unique index on question_id for an efficient lookup.
        Returns None rather than raising when no explanation exists,
        allowing the service layer to pass through without blocking
        the answer submission flow (Requirement 7.4).
        """
        stmt = select(QuestionExplanation).where(
            QuestionExplanation.question_id == question_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_bulk(self, question_ids: list[int]) -> dict[int, QuestionExplanation | None]:
        """Return a mapping of question_id to explanation for each requested ID.

        Questions without a stored explanation are mapped to None rather than
        omitted, so the caller always receives an entry for every requested ID
        (Requirement 7.6).
        """
        stmt = select(QuestionExplanation).where(
            QuestionExplanation.question_id.in_(question_ids)
        )
        results = self.db.execute(stmt).scalars().all()

        explanation_map: dict[int, QuestionExplanation | None] = {
            qid: None for qid in question_ids
        }
        for explanation in results:
            explanation_map[explanation.question_id] = explanation

        return explanation_map
