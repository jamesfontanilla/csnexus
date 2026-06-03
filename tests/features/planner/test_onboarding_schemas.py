"""Unit tests for onboarding Pydantic schemas.

Tests validation behavior of OnboardingRequest, OnboardingResponse,
PlanSummaryResponse, and ExamDateUpdateRequest.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.features.planner.schemas import (
    ExamDateUpdateRequest,
    OnboardingRequest,
    OnboardingResponse,
    PlanSummaryResponse,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TODAY = date.today()


def _future_date(days: int = 30) -> date:
    return _TODAY + timedelta(days=days)


# ---------------------------------------------------------------------------
# OnboardingRequest — happy paths
# ---------------------------------------------------------------------------


class TestOnboardingRequestValid:
    """Valid OnboardingRequest construction."""

    def test_minimal_valid_request(self) -> None:
        req = OnboardingRequest(
            exam_date=_future_date(30),
            exam_category="Professional",
        )
        assert req.exam_date == _future_date(30)
        assert req.exam_category == "Professional"
        assert req.time_budget_minutes == 30  # default

    def test_sub_professional_category(self) -> None:
        req = OnboardingRequest(
            exam_date=_future_date(60),
            exam_category="Sub-Professional",
            time_budget_minutes=15,
        )
        assert req.exam_category == "Sub-Professional"
        assert req.time_budget_minutes == 15

    def test_time_budget_60(self) -> None:
        req = OnboardingRequest(
            exam_date=_future_date(90),
            exam_category="Professional",
            time_budget_minutes=60,
        )
        assert req.time_budget_minutes == 60

    def test_exam_date_tomorrow(self) -> None:
        req = OnboardingRequest(
            exam_date=_future_date(1),
            exam_category="Professional",
        )
        assert req.exam_date == _future_date(1)

    def test_exam_date_365_days(self) -> None:
        req = OnboardingRequest(
            exam_date=_future_date(365),
            exam_category="Professional",
        )
        assert req.exam_date == _future_date(365)


# ---------------------------------------------------------------------------
# OnboardingRequest — validation failures
# ---------------------------------------------------------------------------


class TestOnboardingRequestInvalid:
    """OnboardingRequest rejects invalid inputs."""

    def test_past_exam_date_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OnboardingRequest(
                exam_date=_TODAY - timedelta(days=1),
                exam_category="Professional",
            )
        assert "exam_date must be in the future" in str(exc_info.value)

    def test_today_exam_date_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OnboardingRequest(
                exam_date=_TODAY,
                exam_category="Professional",
            )
        assert "exam_date must be in the future" in str(exc_info.value)

    def test_exam_date_over_365_days_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OnboardingRequest(
                exam_date=_future_date(366),
                exam_category="Professional",
            )
        assert "within 365 days" in str(exc_info.value)

    def test_invalid_exam_category_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OnboardingRequest(
                exam_date=_future_date(30),
                exam_category="Invalid",
            )
        assert "exam_category must be one of" in str(exc_info.value)

    def test_invalid_time_budget_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            OnboardingRequest(
                exam_date=_future_date(30),
                exam_category="Professional",
                time_budget_minutes=45,
            )
        assert "time_budget_minutes must be one of" in str(exc_info.value)

    def test_missing_exam_date_rejected(self) -> None:
        with pytest.raises(ValidationError):
            OnboardingRequest(exam_category="Professional")  # type: ignore[call-arg]

    def test_missing_exam_category_rejected(self) -> None:
        with pytest.raises(ValidationError):
            OnboardingRequest(exam_date=_future_date(30))  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# OnboardingResponse
# ---------------------------------------------------------------------------


class TestOnboardingResponse:
    """OnboardingResponse construction."""

    def test_confirmation_without_warning(self) -> None:
        resp = OnboardingResponse(confirmation="Plan created successfully.")
        assert resp.confirmation == "Plan created successfully."
        assert resp.warning is None

    def test_confirmation_with_warning(self) -> None:
        resp = OnboardingResponse(
            confirmation="Plan created successfully.",
            warning="Your exam is in fewer than 7 days. The study plan will be compressed.",
        )
        assert resp.warning is not None
        assert "compressed" in resp.warning


# ---------------------------------------------------------------------------
# PlanSummaryResponse
# ---------------------------------------------------------------------------


class TestPlanSummaryResponse:
    """PlanSummaryResponse construction."""

    def test_valid_plan_summary(self) -> None:
        resp = PlanSummaryResponse(
            total_days=90,
            subtopics_per_week=5,
            mock_exams_scheduled=12,
            estimated_readiness_at_exam=72.5,
        )
        assert resp.total_days == 90
        assert resp.subtopics_per_week == 5
        assert resp.mock_exams_scheduled == 12
        assert resp.estimated_readiness_at_exam == 72.5


# ---------------------------------------------------------------------------
# ExamDateUpdateRequest
# ---------------------------------------------------------------------------


class TestExamDateUpdateRequest:
    """ExamDateUpdateRequest validation."""

    def test_valid_future_date(self) -> None:
        req = ExamDateUpdateRequest(exam_date=_future_date(60))
        assert req.exam_date == _future_date(60)

    def test_past_date_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ExamDateUpdateRequest(exam_date=_TODAY - timedelta(days=5))
        assert "exam_date must be in the future" in str(exc_info.value)

    def test_today_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ExamDateUpdateRequest(exam_date=_TODAY)
        assert "exam_date must be in the future" in str(exc_info.value)

    def test_over_365_days_rejected(self) -> None:
        with pytest.raises(ValidationError) as exc_info:
            ExamDateUpdateRequest(exam_date=_future_date(400))
        assert "within 365 days" in str(exc_info.value)
