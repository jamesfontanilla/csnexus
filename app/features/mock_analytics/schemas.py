"""Pydantic request/response schemas for mock analytics endpoints.

Validates: Requirements 10.1, 11.1, 12.1, 12.3
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SubtopicBreakdownSchema(BaseModel):
    """Per-subtopic diagnostic breakdown."""

    subtopic_id: int
    subtopic_name: str = ""
    questions_attempted: int
    questions_correct: int
    points_lost: int
    avg_seconds_per_question: float
    accuracy_percentage: float


class DifficultyPerformanceSchema(BaseModel):
    """Accuracy per difficulty level."""

    easy: float | None = None
    medium: float | None = None
    hard: float | None = None


class RegressionAlertSchema(BaseModel):
    """A subtopic that showed significant decline."""

    subtopic_id: int
    decline_percentage_points: float


class DiagnosticResponse(BaseModel):
    """Response for GET /v1/mock-analytics/{attempt_id}."""

    total_score: float = Field(..., description="Percentage correct, 1 decimal.")
    subtopic_breakdowns: list[SubtopicBreakdownSchema]
    highest_impact_areas: list[SubtopicBreakdownSchema] = Field(
        ..., max_length=5, description="Top 5 subtopics by points lost."
    )
    regression_alerts: list[RegressionAlertSchema]
    difficulty_performance: DifficultyPerformanceSchema


class PredictionResponse(BaseModel):
    """Response for GET /v1/mock-analytics/prediction."""

    lower_bound: float | None = Field(None, ge=0, le=100)
    midpoint: float | None = Field(None, ge=0, le=100)
    upper_bound: float | None = Field(None, ge=0, le=100)
    confidence_level: str | None = Field(
        None, description="low, medium, or high. Null if < 2 exams."
    )
    message: str | None = Field(
        None,
        description="Explanation when prediction unavailable.",
    )


class RecommendationSchema(BaseModel):
    """A single actionable recommendation."""

    id: int
    subtopic_id: int
    subtopic_name: str
    current_accuracy: float
    target_accuracy: float
    estimated_point_gain: float
    recommended_action: str = Field(
        ..., description="review, practice, or re-learn"
    )
    formatted_string: str = Field(
        ..., description="Human-readable recommendation string."
    )
    accepted_at: datetime | None = None


class RecommendationsResponse(BaseModel):
    """Response for GET /v1/mock-analytics/{attempt_id}/recommendations."""

    recommendations: list[RecommendationSchema] = Field(
        ..., max_length=5
    )
