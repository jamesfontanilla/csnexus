"""FastAPI router for /v1/queue/* endpoints.

Exposes the Smart Daily Queue API:
- GET  /v1/queue              — get today's daily queue
- POST /v1/queue/items/{id}/:complete — mark item completed
- POST /v1/queue/:regenerate  — force regenerate today's queue
- GET  /v1/queue/preferences  — get time budget preference
- PATCH /v1/queue/preferences — update time budget

All routes require authentication via ``get_current_user``.

Validates: Requirements 4.5, 4.6, 6.1, 6.3, 6.4, 6.5
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.content.repository import LessonRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.smart_queue.repository import QueueRepository
from app.features.smart_queue.schemas import (
    QueuePreferencesResponse,
    QueuePreferencesSchema,
    QueueResponse,
)
from app.features.smart_queue.service import QueueService
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/queue", tags=["queue"])


def get_queue_service(db: Session = Depends(get_db)) -> QueueService:
    """Construct :class:`QueueService` with all repository dependencies."""
    return QueueService(
        queue_repo=QueueRepository(db=db),
        flashcard_repo=FlashcardRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
        subtopic_repo=SubtopicRepository(db=db),
        lesson_repo=LessonRepository(db=db),
    )


@router.get("", response_model=QueueResponse)
def get_daily_queue(
    user: User = Depends(get_current_user),
    service: QueueService = Depends(get_queue_service),
) -> QueueResponse:
    """Return today's daily queue, generating it if it doesn't exist.

    Idempotent: requesting multiple times on the same UTC day returns
    the same queue unless items are completed or regeneration is forced.
    (Requirement 4.5)
    """
    return service.get_daily_queue(user.id)


@router.post("/items/{item_id}/:complete", response_model=QueueResponse)
def complete_item(
    item_id: int,
    user: User = Depends(get_current_user),
    service: QueueService = Depends(get_queue_service),
) -> QueueResponse:
    """Mark a queue item as completed and return the updated queue.

    Raises 404 if the item does not exist. (Requirement 4.6)
    """
    return service.complete_item(user.id, item_id)


@router.post("/:regenerate", response_model=QueueResponse)
def regenerate_queue(
    user: User = Depends(get_current_user),
    service: QueueService = Depends(get_queue_service),
) -> QueueResponse:
    """Force regeneration of today's queue.

    Deletes the existing queue (if any) and generates a fresh one.
    """
    return service.regenerate_queue(user.id)


@router.get("/preferences", response_model=QueuePreferencesResponse)
def get_preferences(
    user: User = Depends(get_current_user),
    service: QueueService = Depends(get_queue_service),
) -> QueuePreferencesResponse:
    """Return the user's current time budget preference.

    Defaults to 30 minutes if no preference has been set. (Requirement 6.1)
    """
    return service.get_preferences(user.id)


@router.patch("/preferences", response_model=QueuePreferencesResponse)
def update_preferences(
    payload: QueuePreferencesSchema,
    user: User = Depends(get_current_user),
    service: QueueService = Depends(get_queue_service),
) -> QueuePreferencesResponse:
    """Update the user's time budget preference.

    Accepts 15, 30, or 60 minutes. Rejects other values with 422.
    If no items have been completed today, regenerates the current queue.
    Otherwise applies the new budget starting tomorrow.
    (Requirements 6.3, 6.4, 6.5)
    """
    return service.update_preferences(user.id, payload.time_budget_minutes)
