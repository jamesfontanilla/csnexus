"""Pydantic request/response schemas for the study planner feature."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Legacy schemas (existing plan management)
# ---------------------------------------------------------------------------


class CreatePlanRequest(BaseModel):
    """Request body for creating a study plan."""

    target_exam_date: date
    available_hours_per_day: float = Field(ge=0.5, le=12.0)
    target_score: float = Field(ge=0.5, le=1.0)


class StudyPlanResponse(BaseModel):
    """Response for a study plan."""

    id: int
    target_exam_date: date
    available_hours_per_day: float
    target_score: float
    status: str
    total_days: int
    days_remaining: int
    completion_percentage: float

    model_config = {"from_attributes": True}


class PlanDayResponse(BaseModel):
    """Response for a single day's task in the plan."""

    id: int
    plan_date: date
    subtopic_title: str
    activity_type: str
    estimated_minutes: int
    completed: bool

    model_config = {"from_attributes": True}


class ReadinessResponse(BaseModel):
    """Response for exam readiness prediction."""

    passing_probability: float
    predicted_score: float
    readiness_percentage: float
    recommended_hours_remaining: float
    strengths: list[str]
    weaknesses: list[str]
    confidence_level: str


# ---------------------------------------------------------------------------
# Onboarding schemas (Intelligent Learning Engine)
# Requirements: 16.2, 16.3, 16.6, 17.4
# ---------------------------------------------------------------------------

_VALID_EXAM_CATEGORIES = ("Professional", "Sub-Professional")
_VALID_TIME_BUDGETS = (15, 30, 60)


class OnboardingRequest(BaseModel):
    """Request body for initial onboarding submission.

    Captures exam date, category, and optional time budget preference.
    """

    exam_date: date
    exam_category: str
    time_budget_minutes: int = Field(default=30)

    @field_validator("exam_date")
    @classmethod
    def _exam_date_must_be_future(cls, v: date) -> date:
        today = date.today()
        days_until = (v - today).days
        if days_until < 1:
            raise ValueError("exam_date must be in the future (at least 1 day from today)")
        if days_until > 365:
            raise ValueError("exam_date must be within 365 days from today")
        return v

    @field_validator("exam_category")
    @classmethod
    def _validate_exam_category(cls, v: str) -> str:
        if v not in _VALID_EXAM_CATEGORIES:
            raise ValueError(
                f"exam_category must be one of: {', '.join(_VALID_EXAM_CATEGORIES)}"
            )
        return v

    @field_validator("time_budget_minutes")
    @classmethod
    def _validate_time_budget(cls, v: int) -> int:
        if v not in _VALID_TIME_BUDGETS:
            raise ValueError(
                f"time_budget_minutes must be one of: {', '.join(str(t) for t in _VALID_TIME_BUDGETS)}"
            )
        return v


class OnboardingResponse(BaseModel):
    """Response after successful onboarding submission.

    Includes a confirmation message and an optional warning when
    the exam date is fewer than 7 days away.
    """

    confirmation: str
    warning: str | None = None


class PlanSummaryResponse(BaseModel):
    """Summary of the generated study plan returned after onboarding.

    Provides high-level metrics about the personalized plan.
    """

    total_days: int
    subtopics_per_week: int
    mock_exams_scheduled: int
    estimated_readiness_at_exam: float


class ExamDateUpdateRequest(BaseModel):
    """Request body for updating the exam date after initial onboarding."""

    exam_date: date

    @field_validator("exam_date")
    @classmethod
    def _exam_date_must_be_future(cls, v: date) -> date:
        today = date.today()
        days_until = (v - today).days
        if days_until < 1:
            raise ValueError("exam_date must be in the future (at least 1 day from today)")
        if days_until > 365:
            raise ValueError("exam_date must be within 365 days from today")
        return v
