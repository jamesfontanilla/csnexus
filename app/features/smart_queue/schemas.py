"""Pydantic request/response schemas for smart queue endpoints.

Validates: Requirements 5.1, 5.2, 5.3, 5.4, 6.1, 6.4
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class QueueItemSchema(BaseModel):
    """A single item in the daily queue."""

    id: int
    position: int
    item_type: str = Field(
        ..., description="flashcard_review, quiz_practice, or new_content"
    )
    payload: dict = Field(
        ..., description="Type-specific data (card_ids, subtopic_id, etc.)"
    )
    estimated_seconds: int = Field(..., gt=0)
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class QueueResponse(BaseModel):
    """Response for GET /v1/queue — today's daily queue."""

    items: list[QueueItemSchema]
    total_estimated_seconds: int
    items_remaining: int
    items_completed: int
    time_budget_minutes: int = Field(
        ..., description="User's configured time budget (15, 30, or 60)."
    )


class QueuePreferencesSchema(BaseModel):
    """User's queue time budget preference."""

    time_budget_minutes: int = Field(
        ...,
        description="Preferred daily study time in minutes. Must be 15, 30, or 60.",
    )

    def model_post_init(self, __context: object) -> None:
        """Validate time_budget_minutes is one of the allowed values."""
        if self.time_budget_minutes not in (15, 30, 60):
            raise ValueError(
                "time_budget_minutes must be 15, 30, or 60"
            )


class QueuePreferencesResponse(BaseModel):
    """Response for GET /v1/queue/preferences."""

    time_budget_minutes: int
