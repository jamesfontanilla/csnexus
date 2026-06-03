"""SQLAlchemy ORM models for the Explanations feature slice.

Defines tables for static question explanations:
- QuestionExplanation (question_explanations)

Validates: Requirements 7.1
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class QuestionExplanation(Base):
    """Static explanation attached to a question."""

    __tablename__ = "question_explanations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    explanation_text: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # 50-2000 chars, markdown
    key_concept: Mapped[str] = mapped_column(String(100), nullable=False)
    related_subtopics: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON array of subtopic IDs, max 10
    cache_version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    concrete_examples: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # JSON array of strings, max 3 items × 100 chars. Filipino-context examples.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
