"""SQLAlchemy ORM models for the Readiness Score feature.

Defines the append-only history table for readiness score computations
and self-assessment calibration records.

Validates: Requirements 2.2, 19.2
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class ReadinessScoreHistory(Base):
    """Append-only history of readiness score computations."""

    __tablename__ = "readiness_score_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100
    mastery_component: Mapped[float] = mapped_column(Float, nullable=False)
    retention_component: Mapped[float] = mapped_column(Float, nullable=False)
    mock_component: Mapped[float] = mapped_column(Float, nullable=False)
    coverage_component: Mapped[float] = mapped_column(Float, nullable=False)
    weights_used: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # JSON: {"mastery":0.4,...}
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_readiness_history_user_computed", "user_id", "computed_at"),
    )


class SelfAssessmentRecord(Base):
    """Record of a user's self-assessed readiness vs computed readiness.

    Used for calibration tracking — identifies overconfidence and
    underconfidence patterns over time.
    """

    __tablename__ = "self_assessment_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    self_assessed_score: Mapped[int] = mapped_column(Integer, nullable=False)
    computed_score: Mapped[int] = mapped_column(Integer, nullable=False)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)
    calibration_status: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # overconfident, well_calibrated, underconfident
    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "self_assessed_score >= 0 AND self_assessed_score <= 100",
            name="ck_self_assessment_score_range",
        ),
        CheckConstraint(
            "calibration_status IN ('overconfident', 'well_calibrated', 'underconfident')",
            name="ck_calibration_status",
        ),
        Index("ix_self_assessment_user_assessed", "user_id", "assessed_at"),
    )
