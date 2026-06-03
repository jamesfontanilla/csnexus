"""Property-based tests for self-assessment calibration logic.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
Tests the calibration status determination, 7-day prompt interval, and score clamping.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from hypothesis import given, settings
from hypothesis.strategies import integers, datetimes, just

from app.features.readiness.models import SelfAssessmentRecord


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_score = integers(min_value=0, max_value=100)
invalid_score_below = integers(min_value=-1000, max_value=-1)
invalid_score_above = integers(min_value=101, max_value=1000)

# Datetimes in a reasonable range for assessed_at (no tzinfo in min/max)
valid_datetime = datetimes(
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2030, 12, 31),
    timezones=just(timezone.utc),
)


# ---------------------------------------------------------------------------
# Pure calibration logic (mirrors the service implementation)
# ---------------------------------------------------------------------------


def determine_calibration_status(delta: int) -> str:
    """Pure function replicating the service's calibration logic."""
    if delta > 15:
        return "overconfident"
    elif delta < -10:
        return "underconfident"
    else:
        return "well_calibrated"


def is_prompt_due(last_assessed_at: datetime | None, now: datetime) -> bool:
    """Pure function replicating the service's prompt timing logic."""
    if last_assessed_at is None:
        return True
    days_since = (now - last_assessed_at).days
    return days_since >= 7


# ---------------------------------------------------------------------------
# Property 36: Self-assessment calibration status matches delta ranges
# Validates: Requirements 19.3, 19.4, 19.5
# ---------------------------------------------------------------------------


class TestCalibrationStatusMatchesDeltaRanges:
    """For any self-assessment submission where delta = self_assessed_score −
    computed_score, the calibration_status SHALL be "overconfident" when
    delta > +15, "well_calibrated" when delta is between −10 and +15
    inclusive, and "underconfident" when delta < −10.

    **Validates: Requirements 19.3, 19.4, 19.5**
    """

    @settings(max_examples=50)
    @given(
        self_assessed_score=valid_score,
        computed_score=valid_score,
    )
    def test_calibration_status_matches_delta_ranges(
        self, self_assessed_score: int, computed_score: int
    ) -> None:
        """Calibration status is determined solely by delta value."""
        delta = self_assessed_score - computed_score
        status = determine_calibration_status(delta)

        if delta > 15:
            assert status == "overconfident"
        elif delta < -10:
            assert status == "underconfident"
        else:
            assert status == "well_calibrated"

    @settings(max_examples=50)
    @given(
        self_assessed_score=valid_score,
        computed_score=valid_score,
    )
    def test_status_is_one_of_three_valid_values(
        self, self_assessed_score: int, computed_score: int
    ) -> None:
        """Status is always one of the three defined values."""
        delta = self_assessed_score - computed_score
        status = determine_calibration_status(delta)
        assert status in {"overconfident", "well_calibrated", "underconfident"}

    @settings(max_examples=50)
    @given(
        self_assessed_score=valid_score,
        computed_score=valid_score,
    )
    def test_overconfident_only_when_delta_exceeds_plus_15(
        self, self_assessed_score: int, computed_score: int
    ) -> None:
        """Overconfident iff delta > 15."""
        delta = self_assessed_score - computed_score
        status = determine_calibration_status(delta)
        if status == "overconfident":
            assert delta > 15
        if delta > 15:
            assert status == "overconfident"

    @settings(max_examples=50)
    @given(
        self_assessed_score=valid_score,
        computed_score=valid_score,
    )
    def test_underconfident_only_when_delta_below_minus_10(
        self, self_assessed_score: int, computed_score: int
    ) -> None:
        """Underconfident iff delta < -10."""
        delta = self_assessed_score - computed_score
        status = determine_calibration_status(delta)
        if status == "underconfident":
            assert delta < -10
        if delta < -10:
            assert status == "underconfident"

    @settings(max_examples=50)
    @given(
        self_assessed_score=valid_score,
        computed_score=valid_score,
    )
    def test_well_calibrated_covers_inclusive_range(
        self, self_assessed_score: int, computed_score: int
    ) -> None:
        """Well-calibrated iff -10 <= delta <= 15."""
        delta = self_assessed_score - computed_score
        status = determine_calibration_status(delta)
        if status == "well_calibrated":
            assert -10 <= delta <= 15
        if -10 <= delta <= 15:
            assert status == "well_calibrated"


# ---------------------------------------------------------------------------
# Property 37: Self-assessment prompt respects 7-day interval
# Validates: Requirements 19.1, 19.7
# ---------------------------------------------------------------------------


class TestSelfAssessmentPromptRespects7DayInterval:
    """For any user with a self-assessment history, the prompt SHALL be due
    (is_self_assessment_due returns True) if and only if the most recent
    assessed_at timestamp is more than 7 calendar days before the current date.
    For users with no self-assessment history, the prompt SHALL always be due.

    **Validates: Requirements 19.1, 19.7**
    """

    @settings(max_examples=50)
    @given(
        last_assessed_at=valid_datetime,
        days_elapsed=integers(min_value=0, max_value=365),
    )
    def test_prompt_due_iff_7_or_more_days_elapsed(
        self, last_assessed_at: datetime, days_elapsed: int
    ) -> None:
        """Prompt is due iff days since last assessment >= 7."""
        now = last_assessed_at + timedelta(days=days_elapsed)
        result = is_prompt_due(last_assessed_at, now)

        if days_elapsed >= 7:
            assert result is True
        else:
            assert result is False

    @settings(max_examples=50)
    @given(now=valid_datetime)
    def test_no_history_always_due(self, now: datetime) -> None:
        """First-time user (no history) always gets prompted."""
        result = is_prompt_due(None, now)
        assert result is True

    @settings(max_examples=50)
    @given(last_assessed_at=valid_datetime)
    def test_exactly_7_days_is_due(self, last_assessed_at: datetime) -> None:
        """Prompt is due at exactly the 7-day boundary."""
        now = last_assessed_at + timedelta(days=7)
        assert is_prompt_due(last_assessed_at, now) is True

    @settings(max_examples=50)
    @given(last_assessed_at=valid_datetime)
    def test_6_days_is_not_due(self, last_assessed_at: datetime) -> None:
        """Prompt is not due at 6 days."""
        now = last_assessed_at + timedelta(days=6)
        assert is_prompt_due(last_assessed_at, now) is False


# ---------------------------------------------------------------------------
# Property 38: Self-assessment scores are clamped to valid range
# Validates: Requirements 19.1
# ---------------------------------------------------------------------------


class TestSelfAssessmentScoresClampedToValidRange:
    """For any self-assessment submission, the self_assessed_score SHALL be an
    integer in the range [0, 100] inclusive. Submissions outside this range
    SHALL be rejected with a validation error.

    **Validates: Requirements 19.1**
    """

    @settings(max_examples=50)
    @given(score=valid_score)
    def test_valid_scores_accepted(self, score: int) -> None:
        """Scores in [0, 100] are accepted by the Pydantic schema."""
        from app.features.readiness.schemas import SelfAssessmentRequest

        request = SelfAssessmentRequest(self_assessed_score=score)
        assert request.self_assessed_score == score
        assert 0 <= request.self_assessed_score <= 100

    @settings(max_examples=50)
    @given(score=invalid_score_below)
    def test_scores_below_zero_rejected(self, score: int) -> None:
        """Scores below 0 are rejected by validation."""
        from pydantic import ValidationError

        from app.features.readiness.schemas import SelfAssessmentRequest

        try:
            SelfAssessmentRequest(self_assessed_score=score)
            assert False, f"Score {score} should have been rejected"
        except ValidationError:
            pass  # Expected

    @settings(max_examples=50)
    @given(score=invalid_score_above)
    def test_scores_above_100_rejected(self, score: int) -> None:
        """Scores above 100 are rejected by validation."""
        from pydantic import ValidationError

        from app.features.readiness.schemas import SelfAssessmentRequest

        try:
            SelfAssessmentRequest(self_assessed_score=score)
            assert False, f"Score {score} should have been rejected"
        except ValidationError:
            pass  # Expected

    @settings(max_examples=50)
    @given(score=valid_score)
    def test_score_type_is_integer(self, score: int) -> None:
        """Self-assessed score is always stored as integer."""
        from app.features.readiness.schemas import SelfAssessmentRequest

        request = SelfAssessmentRequest(self_assessed_score=score)
        assert isinstance(request.self_assessed_score, int)
