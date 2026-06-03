"""Repository for pretesting feature.

Requirements: 20.4
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.features.pretesting.models import PretestAttempt


class PretestRepository:
    """Data access for pretest attempts."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, attempt: PretestAttempt) -> PretestAttempt:
        """Persist a new pretest attempt."""
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get(self, pretest_id: int) -> PretestAttempt | None:
        """Get a pretest attempt by ID."""
        return (
            self.db.query(PretestAttempt)
            .filter(PretestAttempt.id == pretest_id)
            .first()
        )

    def get_by_user_and_subtopic(
        self, user_id: int, subtopic_id: int
    ) -> PretestAttempt | None:
        """Get the user's pretest for a subtopic (most recent)."""
        return (
            self.db.query(PretestAttempt)
            .filter(
                PretestAttempt.user_id == user_id,
                PretestAttempt.subtopic_id == subtopic_id,
            )
            .order_by(PretestAttempt.created_at.desc())
            .first()
        )

    def has_pretest(self, user_id: int, subtopic_id: int) -> bool:
        """Check if a user has already taken a pretest for a subtopic."""
        return (
            self.db.query(PretestAttempt)
            .filter(
                PretestAttempt.user_id == user_id,
                PretestAttempt.subtopic_id == subtopic_id,
            )
            .first()
            is not None
        )
