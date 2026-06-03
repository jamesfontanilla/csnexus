"""Pydantic request/response schemas for readiness score endpoints.

Validates: Requirements 2.3, 3.1, 3.2, 3.3
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ReadinessComponentsSchema(BaseModel):
    """Breakdown of individual readiness score components."""

    mastery_component: float = Field(..., ge=0, le=100)
    retention_component: float = Field(..., ge=0, le=100)
    mock_component: float = Field(..., ge=0, le=100)
    coverage_component: float = Field(..., ge=0, le=100)


class ReadinessResponse(BaseModel):
    """Response for GET /v1/readiness — current score + components."""

    score: int = Field(..., ge=0, le=100)
    components: ReadinessComponentsSchema
    delta: int | None = Field(
        None, description="Score change vs 7 days ago. Null if no prior record."
    )
    stale_score: bool = Field(
        False, description="True if computation failed and a cached score is returned."
    )

    model_config = {"from_attributes": True}


class TopImpactSubtopic(BaseModel):
    """A subtopic with high potential score improvement."""

    subtopic_id: int
    subtopic_name: str
    point_impact: float = Field(
        ..., description="Estimated score improvement if this subtopic is mastered."
    )


class DashboardResponse(BaseModel):
    """Response for GET /v1/readiness/dashboard."""

    score: int = Field(..., ge=0, le=100)
    components: ReadinessComponentsSchema
    delta: int | None = None
    top_impact_subtopics: list[TopImpactSubtopic] = Field(
        default_factory=list,
        max_length=3,
        description="Top 3 subtopics with highest Point_Impact.",
    )
    readiness_level: str = Field(
        ...,
        description="Classification: Not Ready, Getting There, Almost Ready, Exam Ready.",
    )
    score_change_summary: ScoreChangeSummary | None = Field(
        None,
        description="Present when score changed >= 5 points since last login.",
    )
    stale_data: bool = False
    computed_at: datetime | None = None


class ScoreChangeSummary(BaseModel):
    """Summary of significant score change since last login."""

    primary_component: str = Field(
        ..., description="Component that changed most: mastery, retention, mock_exam, or coverage."
    )
    component_direction: str = Field(
        ..., description="'up' or 'down'."
    )
    component_magnitude: float = Field(
        ..., description="Absolute change in the primary component."
    )
    overall_delta: int = Field(
        ..., description="Overall score change."
    )


# Fix forward reference
DashboardResponse.model_rebuild()


class TrendPoint(BaseModel):
    """A single point in the 30-day readiness trend."""

    date: str = Field(..., description="ISO date string (YYYY-MM-DD).")
    score: int = Field(..., ge=0, le=100)


class TrendResponse(BaseModel):
    """Response for GET /v1/readiness/trend — 30-day score trend."""

    trend: list[TrendPoint] = Field(
        ..., description="One score per day for the past 30 days."
    )


# ------------------------------------------------------------------
# Self-Assessment Calibration schemas
# ------------------------------------------------------------------


class SelfAssessmentRequest(BaseModel):
    """Request body for POST /v1/readiness/self-assessment."""

    self_assessed_score: int = Field(
        ..., ge=0, le=100, description="User's self-assessed readiness score (0-100)."
    )


class SelfAssessmentResponse(BaseModel):
    """Response for POST /v1/readiness/self-assessment."""

    self_assessed_score: int = Field(..., ge=0, le=100)
    computed_score: int = Field(..., ge=0, le=100)
    delta: int = Field(
        ..., description="self_assessed_score minus computed_score."
    )
    calibration_status: str = Field(
        ...,
        description="One of: overconfident, well_calibrated, underconfident.",
    )
    message: str = Field(
        ..., description="Calibration feedback message for the user."
    )
    calibration_warning: str | None = Field(
        None,
        description="Present when user is overconfident (delta > +15).",
    )

    model_config = {"from_attributes": True}


class SelfAssessmentHistoryItem(BaseModel):
    """A single self-assessment record in the history."""

    self_assessed_score: int
    computed_score: int
    delta: int
    calibration_status: str
    assessed_at: datetime

    model_config = {"from_attributes": True}


class SelfAssessmentHistoryResponse(BaseModel):
    """Response for GET /v1/readiness/self-assessment/history."""

    records: list[SelfAssessmentHistoryItem] = Field(
        default_factory=list,
        description="All self-assessment records, most recent first.",
    )


class SelfAssessmentPromptResponse(BaseModel):
    """Response for GET /v1/readiness/self-assessment/prompt."""

    is_due: bool = Field(
        ..., description="True if 7+ days since last assessment or no history."
    )
    last_assessed_at: datetime | None = Field(
        None, description="Timestamp of the most recent self-assessment."
    )
