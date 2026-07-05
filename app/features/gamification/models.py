"""SQLAlchemy ORM models for the gamification slice.

Seven tables:

- :class:`UserDailyGoal` — per-user per-day XP target tracking.
- :class:`StreakFreeze` — consumable streak protection tokens.
- :class:`XPMultiplier` — time-limited XP multipliers from various sources.
- :class:`Tournament` — competitive events with leaderboards.
- :class:`TournamentParticipant` — user enrollment + XP earned in a tournament.
- :class:`CompetenceMilestone` — exam-relevant competence milestone definitions.
- :class:`CompetenceMilestoneAward` — records of users earning milestones.
- :class:`StudyConsistency` — per-user study consistency tracking.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class UserDailyGoal(Base):
    """Per-user per-day XP target tracking."""

    __tablename__ = "user_daily_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_xp: Mapped[int] = mapped_column(
        Integer, nullable=False, default=50, server_default="50"
    )
    current_xp: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    goal_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
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
        UniqueConstraint("user_id", "goal_date", name="uq_user_daily_goals_user_date"),
    )


class StreakFreeze(Base):
    """Consumable streak protection token."""

    __tablename__ = "streak_freezes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    available: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default="1"
    )
    used_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
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


class XPMultiplier(Base):
    """Time-limited XP multiplier from various sources."""

    __tablename__ = "xp_multipliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    multiplier: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
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


class Tournament(Base):
    """Competitive event with leaderboard."""

    __tablename__ = "tournaments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(32), nullable=True)
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="UPCOMING", server_default="UPCOMING"
    )
    max_participants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prize_description: Mapped[str | None] = mapped_column(Text, nullable=True)
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
            "status IN ('UPCOMING', 'ACTIVE', 'COMPLETED')",
            name="ck_tournaments_status",
        ),
    )


class TournamentParticipant(Base):
    """User enrollment in a tournament + XP earned during the event."""

    __tablename__ = "tournament_participants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tournament_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tournaments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    xp_earned: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
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
        UniqueConstraint(
            "tournament_id", "user_id", name="uq_tournament_participants_tournament_user"
        ),
    )


class CompetenceMilestone(Base):
    """Definition of a competence milestone (seeded, not user-created)."""

    __tablename__ = "competence_milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # mastery, readiness, recovery, subtest
    threshold_config: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON: milestone-specific criteria
    xp_reward: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )  # XP granted to the user when this milestone is first awarded
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class CompetenceMilestoneAward(Base):
    """Record of a user earning a milestone — permanent, never revoked."""

    __tablename__ = "competence_milestone_awards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    milestone_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("competence_milestones.id", ondelete="CASCADE"),
        nullable=False,
    )
    triggering_values: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON: metric values at award time
    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )  # NULL = not yet shown to the user; set on first retrieval

    __table_args__ = (
        UniqueConstraint(
            "user_id", "milestone_id", name="uq_milestone_award_user_milestone"
        ),
    )


class StudyConsistency(Base):
    """Per-user study consistency tracking (replaces raw login streaks)."""

    __tablename__ = "study_consistency"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    current_streak: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    longest_streak: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    total_consistent_days: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    last_qualifying_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class MasteryScoreHistory(Base):
    """Append-only log of every mastery score change per subtopic per user.

    Written by the mastery service every time a subtopic's mastery_score
    changes. Enables accurate recovery milestone detection — we can find
    the exact date a subtopic was below 0.5 and when it crossed 0.8,
    instead of inferring from the current snapshot's updated_at.
    """

    __tablename__ = "mastery_score_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subtopic_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )
    mastery_score: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "ix_mastery_score_history_user_subtopic_recorded",
            "user_id", "subtopic_id", "recorded_at",
        ),
    )
