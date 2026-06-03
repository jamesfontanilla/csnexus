"""SQLAlchemy models for the pretesting feature.

Requirements: 20.4, 21.3
"""

from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.sqlite import JSON

from app.infrastructure.database.base import Base


class PretestAttempt(Base):
    """Records a user's pretest before a lesson."""

    __tablename__ = "pretest_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=False, index=True)
    questions = Column(JSON, nullable=False)  # List of question dicts with answers
    score = Column(Float, nullable=False, default=0.0)
    total_questions = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
