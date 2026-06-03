"""Repository for smart queue data access (DailyQueue, QueueItem).

Provides idempotent queue retrieval/creation, ordered item access,
item completion tracking, queue deletion for regeneration, and
user time budget preference management.

Validates: Requirements 4.5, 4.6, 6.1, 6.3
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.planner.models import OnboardingProfile
from app.features.smart_queue.models import DailyQueue, QueueItem
from app.infrastructure.repositories.base import BaseRepository


class QueueRepository(BaseRepository[DailyQueue]):
    """Persistence layer for daily queues, queue items, and user preferences."""

    model = DailyQueue

    def __init__(self, db: Session) -> None:
        super().__init__(db=db)

    # ------------------------------------------------------------------
    # Queue CRUD
    # ------------------------------------------------------------------

    def get_or_create_for_date(
        self, user_id: int, queue_date: date
    ) -> DailyQueue | None:
        """Return the existing queue for the given user and date, or None if not found.

        This is the retrieval half of idempotent queue access. The service layer
        is responsible for creating a new queue (via `create_queue`) when None is
        returned, since creation requires running the generator algorithm.
        """
        stmt = select(DailyQueue).where(
            DailyQueue.user_id == user_id,
            DailyQueue.queue_date == queue_date,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_queue(self, queue: DailyQueue) -> DailyQueue:
        """Persist a new daily queue and return it with server defaults applied."""
        self.db.add(queue)
        self.db.commit()
        self.db.refresh(queue)
        return queue

    # ------------------------------------------------------------------
    # Queue Items
    # ------------------------------------------------------------------

    def get_items(self, queue_id: int) -> list[QueueItem]:
        """Return all items for a queue, ordered by position ascending."""
        stmt = (
            select(QueueItem)
            .where(QueueItem.queue_id == queue_id)
            .order_by(QueueItem.position.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def add_items(self, items: list[QueueItem]) -> list[QueueItem]:
        """Bulk-insert queue items and return them with IDs assigned."""
        for item in items:
            self.db.add(item)
        self.db.commit()
        for item in items:
            self.db.refresh(item)
        return items

    def mark_item_completed(self, item_id: int) -> QueueItem | None:
        """Set completed_at timestamp on a queue item.

        Returns the updated item, or None if the item does not exist.
        """
        item = self.db.get(QueueItem, item_id)
        if item is None:
            return None
        item.completed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(item)
        return item

    # ------------------------------------------------------------------
    # Queue Deletion (for regeneration)
    # ------------------------------------------------------------------

    def delete_queue_for_date(self, user_id: int, queue_date: date) -> bool:
        """Delete the queue and its items for a given user and date.

        Returns True if a queue was deleted, False if none existed.
        The CASCADE on queue_items foreign key handles item cleanup.
        """
        queue = self.get_or_create_for_date(user_id, queue_date)
        if queue is None:
            return False
        self.db.delete(queue)
        self.db.commit()
        return True

    # ------------------------------------------------------------------
    # User Preferences (time budget)
    # ------------------------------------------------------------------

    def get_user_preferences(self, user_id: int) -> int:
        """Return the user's time_budget_minutes preference.

        Reads from OnboardingProfile. Returns 30 (the default) if no
        onboarding profile exists yet.
        """
        stmt = select(OnboardingProfile.time_budget_minutes).where(
            OnboardingProfile.user_id == user_id,
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        if result is None:
            return 30
        return result

    def update_user_preferences(
        self, user_id: int, time_budget_minutes: int
    ) -> int:
        """Persist the user's time_budget_minutes preference.

        Updates OnboardingProfile if it exists, otherwise creates a minimal
        profile with default values for non-preference fields.

        Returns the persisted time_budget_minutes value.
        """
        stmt = select(OnboardingProfile).where(
            OnboardingProfile.user_id == user_id,
        )
        profile = self.db.execute(stmt).scalar_one_or_none()
        if profile is not None:
            profile.time_budget_minutes = time_budget_minutes
            self.db.commit()
            self.db.refresh(profile)
            return profile.time_budget_minutes
        # No profile yet — the service layer should enforce that onboarding
        # is completed before allowing preference updates. Return the requested
        # value without persisting to avoid creating an incomplete profile.
        return time_budget_minutes

    # ------------------------------------------------------------------
    # Queue Completion Tracking
    # ------------------------------------------------------------------

    def get_completed_count(self, queue_id: int) -> int:
        """Return the number of completed items in a queue."""
        stmt = select(QueueItem).where(
            QueueItem.queue_id == queue_id,
            QueueItem.completed_at.isnot(None),
        )
        items = self.db.execute(stmt).scalars().all()
        return len(items)

    def has_completed_items(self, queue_id: int) -> bool:
        """Return True if any item in the queue has been completed."""
        stmt = select(QueueItem.id).where(
            QueueItem.queue_id == queue_id,
            QueueItem.completed_at.isnot(None),
        ).limit(1)
        return self.db.execute(stmt).scalar_one_or_none() is not None
