"""SQLAlchemy ORM models for the Mock Analytics feature slice.

Defines tables for post-mock exam diagnostic analysis:
- DiagnosticReport (diagnostic_reports)
- RecommendationRecord (recommendation_records)

Validates: Requirements 10.5, 12.5
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class DiagnosticReport(Base):
    """Persisted diagnostic analysis of a completed mock exam."""

    __tablename__ = "diagnostic_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    mock_exam_attempt_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("mock_exam_attempts.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    total_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # percentage, 1 decimal
    subtopic_breakdowns: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON
    highest_impact_areas: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON
    regression_alerts: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON
    difficulty_performance: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON
    predicted_score_range: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # JSON
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RecommendationRecord(Base):
    """Persisted actionable recommendation from a diagnostic report."""

    __tablename__ = "recommendation_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("diagnostic_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    subtopic_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subtopics.id", ondelete="CASCADE"),
        nullable=False,
    )
    subtopic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    target_accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_point_gain: Mapped[float] = mapped_column(Float, nullable=False)
    recommended_action: Mapped[str] = mapped_column(
        String(16), nullable=False
    )  # review, practice, re-learn
    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "recommended_action IN ('review', 'practice', 're-learn')",
            name="ck_recommendations_action",
        ),
    )
