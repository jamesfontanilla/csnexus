"""SQLAlchemy ORM models for the Flashcard Learning Ecosystem.

Defines all tables for the flashcard feature slice:
- Deck (flashcard_decks)
- Flashcard (flashcards)
- ReviewLog (flashcard_review_logs)
- StudySession (flashcard_study_sessions)
- DeckRating (flashcard_deck_ratings)
- DeckBookmark (flashcard_deck_bookmarks)
- DeckComment (flashcard_deck_comments)
- Follow (flashcard_follows)
- DeckReport (flashcard_deck_reports)
- ExamSimulation (flashcard_exam_simulations)
- ExamSimulationAnswer (flashcard_exam_simulation_answers)
- FlashcardNotification (flashcard_notifications)

Validates: Requirements 30.1, 30.4, 30.8
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
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


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class DeckVisibility(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    UNLISTED = "unlisted"
    REMOVED = "removed"


class DeckCategory(str, Enum):
    VERBAL = "verbal"
    NUMERICAL = "numerical"
    ANALYTICAL = "analytical"


class CardType(str, Enum):
    BASIC = "basic"
    REVERSE = "reverse"
    CLOZE = "cloze"
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    MATCHING = "matching"
    SEQUENCE = "sequence"


class StudyMode(str, Enum):
    SWIPE = "swipe"
    TYPING = "typing"
    RAPID_RECALL = "rapid_recall"
    QUIZ = "quiz"
    TIMED = "timed"
    EXAM_SIMULATION = "exam_simulation"


class ConfidenceLevel(str, Enum):
    GUESSED = "guessed"
    UNSURE = "unsure"
    CONFIDENT = "confident"
    MASTERED = "mastered"


class ResponseType(str, Enum):
    FORGOT = "forgot"
    REMEMBERED = "remembered"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class Deck(Base):
    """A flashcard deck owned by a user."""

    __tablename__ = "flashcard_decks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(16), nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(16), nullable=False, default="private", server_default="private"
    )
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    clone_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    bookmark_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    average_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    is_featured: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    cloned_from_deck_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cloned_from_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("owner_id", "title", name="uq_flashcard_decks_owner_title"),
        CheckConstraint(
            "category IN ('verbal', 'numerical', 'analytical')",
            name="ck_flashcard_decks_category",
        ),
        CheckConstraint(
            "visibility IN ('private', 'public', 'unlisted', 'removed')",
            name="ck_flashcard_decks_visibility",
        ),
        Index("ix_flashcard_decks_owner_deleted", "owner_id", "deleted_at"),
        Index("ix_flashcard_decks_visibility_featured", "visibility", "is_featured"),
    )


class Flashcard(Base):
    """A single flashcard within a deck, with FSRS scheduling fields."""

    __tablename__ = "flashcards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    front: Mapped[str] = mapped_column(Text, nullable=False)
    back: Mapped[str] = mapped_column(Text, nullable=False)
    card_type: Mapped[str] = mapped_column(String(16), nullable=False)
    hints: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ease_factor: Mapped[float] = mapped_column(
        Float, nullable=False, default=2.5, server_default="2.5"
    )
    retention_score: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, server_default="0.0"
    )
    memory_stability: Mapped[float] = mapped_column(
        Float, nullable=False, default=1.0, server_default="1.0"
    )
    review_interval: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    lapse_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    mastery_percentage: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, server_default="0.0"
    )
    next_review_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_review_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    total_reviews: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    successful_reviews: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    is_graduated: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    is_bookmarked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "card_type IN ('basic', 'reverse', 'cloze', 'mcq', "
            "'true_false', 'matching', 'sequence')",
            name="ck_flashcards_card_type",
        ),
        CheckConstraint(
            "ease_factor >= 1.3 AND ease_factor <= 3.5",
            name="ck_flashcards_ease_factor",
        ),
        CheckConstraint(
            "memory_stability >= 0.1",
            name="ck_flashcards_memory_stability",
        ),
        CheckConstraint(
            "review_interval >= 1 AND review_interval <= 365",
            name="ck_flashcards_review_interval",
        ),
        Index("ix_flashcards_deck_next_review", "deck_id", "next_review_date"),
        Index("ix_flashcards_deck_deleted", "deck_id", "deleted_at"),
    )


class StudySession(Base):
    """A study session tracking mode, config, and results."""

    __tablename__ = "flashcard_study_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    study_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    deck_ids: Mapped[str] = mapped_column(Text, nullable=False)
    interleaving_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    focus_mode_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    focus_session_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    time_limit_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    card_time_limit_seconds: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    cards_reviewed: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cards_correct: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cards_incorrect: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cards_skipped: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "study_mode IN ('swipe', 'typing', 'rapid_recall', "
            "'quiz', 'timed', 'exam_simulation')",
            name="ck_study_sessions_mode",
        ),
    )


class ReviewLog(Base):
    """Append-only log of every card review event."""

    __tablename__ = "flashcard_review_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    card_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("flashcard_study_sessions.id", ondelete="SET NULL"),
        nullable=True,
    )
    response_type: Mapped[str] = mapped_column(String(16), nullable=False)
    confidence_level: Mapped[str | None] = mapped_column(String(16), nullable=True)
    ease_factor_before: Mapped[float] = mapped_column(Float, nullable=False)
    interval_before: Mapped[int] = mapped_column(Integer, nullable=False)
    ease_factor_after: Mapped[float] = mapped_column(Float, nullable=False)
    interval_after: Mapped[int] = mapped_column(Integer, nullable=False)
    typed_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    client_event_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "response_type IN ('forgot', 'remembered', 'skipped')",
            name="ck_review_logs_response_type",
        ),
        CheckConstraint(
            "confidence_level IN ('guessed', 'unsure', 'confident', 'mastered') "
            "OR confidence_level IS NULL",
            name="ck_review_logs_confidence",
        ),
        UniqueConstraint("client_event_id", name="uq_review_logs_client_event_id"),
        Index("ix_review_logs_user_reviewed", "user_id", "reviewed_at"),
        Index("ix_review_logs_card_reviewed", "card_id", "reviewed_at"),
    )


class DeckRating(Base):
    """One rating per user per deck (1-5 stars)."""

    __tablename__ = "flashcard_deck_ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("deck_id", "user_id", name="uq_deck_ratings_deck_user"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_deck_ratings_range"),
    )


class DeckBookmark(Base):
    """User bookmark on a deck."""

    __tablename__ = "flashcard_deck_bookmarks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("deck_id", "user_id", name="uq_deck_bookmarks_deck_user"),
    )


class DeckComment(Base):
    """Threaded comment on a deck (max nesting level 2)."""

    __tablename__ = "flashcard_deck_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    body: Mapped[str] = mapped_column(String(1000), nullable=False)
    parent_comment_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("flashcard_deck_comments.id", ondelete="CASCADE"),
        nullable=True,
    )
    nesting_level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    is_held_for_moderation: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("nesting_level <= 2", name="ck_deck_comments_nesting"),
    )


class Follow(Base):
    """Creator follow relationship (no self-follow allowed)."""

    __tablename__ = "flashcard_follows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    follower_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    followed_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uq_follows_pair"),
        CheckConstraint("follower_id != followed_id", name="ck_follows_no_self"),
    )


class DeckReport(Base):
    """User report on a deck (one per user per deck)."""

    __tablename__ = "flashcard_deck_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    deck_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reporter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "deck_id", "reporter_id", name="uq_deck_reports_deck_reporter"
        ),
    )


class ExamSimulation(Base):
    """A timed exam simulation session."""

    __tablename__ = "flashcard_exam_simulations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deck_ids: Mapped[str] = mapped_column(Text, nullable=False)
    question_count: Mapped[int] = mapped_column(Integer, nullable=False)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    category_distribution: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_per_category: Mapped[str | None] = mapped_column(Text, nullable=True)
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cards_correct: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cards_incorrect: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    cards_skipped: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    percentile_estimate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="in_progress", server_default="in_progress"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('in_progress', 'completed', 'timed_out')",
            name="ck_exam_sim_status",
        ),
        CheckConstraint(
            "question_count >= 10 AND question_count <= 150",
            name="ck_exam_sim_question_count",
        ),
        Index("ix_exam_simulations_user_status", "user_id", "status"),
    )


class ExamSimulationAnswer(Base):
    """Per-card answer in an exam simulation."""

    __tablename__ = "flashcard_exam_simulation_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    simulation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcard_exam_simulations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    card_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("flashcards.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    is_locked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    answered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "simulation_id", "card_id", name="uq_exam_sim_answers_sim_card"
        ),
    )


class FlashcardNotification(Base):
    """Notifications for follow/comment events."""

    __tablename__ = "flashcard_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    notification_type: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
