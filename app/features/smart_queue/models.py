"""SQLAlchemy ORM models for the Smart Queue feature slice.

Defines tables for personalized daily study session management:
- DailyQueue (daily_queues) — one queue per user per UTC day
- QueueItem (queue_items) — individual items within a daily queue
- QueueItemType (enum) — supported queue item types

Validates: Requirements 4.5, 5.1
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class QueueItemType(str, Enum):
    """Supported item types within a daily queue."""

    FLASHCARD_REVIEW = "flashcard_review"
    QUIZ_PRACTICE = "quiz_practice"
    NEW_CONTENT = "new_content"


class DailyQueue(Base):
    """One queue per user per UTC day."""

    __tablename__ = "daily_queues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    queue_date: Mapped[date] = mapped_column(Date, nullable=False)
    time_budget_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    total_estimated_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    items_total: Mapped[int] = mapped_column(Integer, nullable=False)
    items_completed: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("user_id", "queue_date", name="uq_daily_queue_user_date"),
    )


class QueueItem(Base):
    """Individual item within a daily queue."""

    __tablename__ = "queue_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    queue_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("daily_queues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    item_type: Mapped[str] = mapped_column(String(20), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)  # JSON: type-specific data
    estimated_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('flashcard_review', 'quiz_practice', 'new_content')",
            name="ck_queue_items_type",
        ),
        Index("ix_queue_items_queue_position", "queue_id", "position"),
    )
