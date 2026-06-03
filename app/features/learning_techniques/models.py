"""SQLAlchemy models for research-backed learning technique extensions.

Covers:
- Personal notes (Elaborative Interrogation, Req 22.3)
- Lesson reflections (Elaborative Interrogation, Req 23.3)
- Recall answers (Generation Effect / Recall Mode, Req 24.1)
- Goodnight review sessions (Sleep-Aware Review, Req 25.1)
- Session reflections (Metacognitive Reflection, Req 26.3)
- Challenge attempts (Productive Failure, Req 28.5)
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.sqlite import JSON

from app.infrastructure.database.base import Base


# ─── Elaborative Interrogation ───────────────────────────────────────────────


class PersonalNote(Base):
    """User's personal elaboration note on a question (Req 22.3)."""

    __tablename__ = "personal_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    note_text = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class LessonReflection(Base):
    """User's reflection at a key concept section in a lesson (Req 23.3)."""

    __tablename__ = "lesson_reflections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    section_index = Column(Integer, nullable=False, default=0)
    reflection_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


# ─── Generation Effect / Recall Mode ────────────────────────────────────────


class RecallAnswer(Base):
    """Records a recall-mode (free-text) answer attempt (Req 24.1)."""

    __tablename__ = "recall_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, index=True)
    user_response = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)  # None = "needs review"
    match_type = Column(
        String(20), nullable=True
    )  # "exact", "fuzzy", "needs_review"
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


# ─── Sleep-Aware Review ──────────────────────────────────────────────────────


class GoodnightReviewSession(Base):
    """A bedtime review session of today's weakest items (Req 25.1)."""

    __tablename__ = "goodnight_review_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_date = Column(DateTime, nullable=False)
    items = Column(JSON, nullable=False)  # List of item dicts
    completed_at = Column(DateTime, nullable=True)
    bedtime_preference = Column(String(5), nullable=True, default="22:00")


# ─── Metacognitive Reflection ────────────────────────────────────────────────


class SessionReflection(Base):
    """Post-session metacognitive reflection (Req 26.3)."""

    __tablename__ = "session_reflections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_date = Column(DateTime, nullable=False)
    hardest_item_id = Column(Integer, nullable=True)
    confidence_rating = Column(
        Integer, nullable=False, default=3
    )
    review_note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "confidence_rating >= 1 AND confidence_rating <= 5",
            name="ck_confidence_rating_range",
        ),
    )


# ─── Productive Failure ──────────────────────────────────────────────────────


class ChallengeAttempt(Base):
    """Records a productive failure challenge attempt (Req 28.5)."""

    __tablename__ = "challenge_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subtopic_id = Column(Integer, ForeignKey("subtopics.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    pre_lesson_answer = Column(Text, nullable=True)
    pre_lesson_correct = Column(Boolean, nullable=True)
    post_lesson_answer = Column(Text, nullable=True)
    post_lesson_correct = Column(Boolean, nullable=True)
    is_productive_failure_success = Column(Boolean, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
