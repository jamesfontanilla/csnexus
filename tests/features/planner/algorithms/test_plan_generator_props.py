"""Property-based tests for the plan generator algorithm.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
Tests Properties 30-34 from the Intelligent Learning Engine design.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import (
    composite,
    integers,
    lists,
    sampled_from,
    sets,
)

from app.features.planner.algorithms.plan_generator import (
    DailyAssignment,
    ExamDateValidationError,
    GeneratedPlan,
    PlanConfig,
    validate_exam_date,
    _compute_mock_exam_days,
    _original_generate_study_plan,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_subtopic_id = integers(min_value=1, max_value=200)
valid_days_ahead = integers(min_value=1, max_value=365)
invalid_days_past = integers(min_value=-365, max_value=0)
invalid_days_far_future = integers(min_value=366, max_value=1000)
valid_hours_per_day = sampled_from([0.25, 0.5, 1.0])
valid_exam_category = sampled_from(["Professional", "Sub-Professional"])


@composite
def plan_config(draw, *, days_ahead: int | None = None):
    """Generate a valid PlanConfig with a random exam date."""
    today = date(2025, 1, 1)
    if days_ahead is None:
        days = draw(valid_days_ahead)
    else:
        days = days_ahead
    exam_date = today + timedelta(days=days)
    hours = draw(valid_hours_per_day)
    category = draw(valid_exam_category)
    return PlanConfig(
        target_exam_date=exam_date,
        available_hours_per_day=hours,
        exam_category=category,
        mastered_subtopic_ids=[],
    )


@composite
def plan_config_with_mastered(draw):
    """Generate a PlanConfig with some mastered subtopics."""
    today = date(2025, 1, 1)
    days = draw(integers(min_value=14, max_value=365))
    exam_date = today + timedelta(days=days)
    hours = draw(valid_hours_per_day)
    category = draw(valid_exam_category)
    mastered = draw(lists(valid_subtopic_id, min_size=1, max_size=30))
    return PlanConfig(
        target_exam_date=exam_date,
        available_hours_per_day=hours,
        exam_category=category,
        mastered_subtopic_ids=mastered,
    )


@composite
def subtopic_id_list(draw, min_size: int = 5, max_size: int = 60):
    """Generate a list of unique subtopic IDs."""
    count = draw(integers(min_value=min_size, max_value=max_size))
    ids = list(range(1, count + 1))
    return ids


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXED_TODAY = date(2025, 1, 1)


def _generate_plan(
    subtopic_ids: list[int], config: PlanConfig
) -> GeneratedPlan:
    """Helper to call the original generate_study_plan (new API)."""
    return _original_generate_study_plan(subtopic_ids, config, today=FIXED_TODAY)


# ---------------------------------------------------------------------------
# Property 30: Onboarding date validation accepts 1–365 days in future
# Validates: Requirements 16.2
# ---------------------------------------------------------------------------


class TestOnboardingDateValidation:
    """For any submitted exam_date, the validation SHALL accept dates that are
    between 1 and 365 calendar days from today (inclusive) and reject dates in
    the past or more than 365 days in the future.

    **Validates: Requirements 16.2**
    """

    @settings(max_examples=50)
    @given(days_ahead=valid_days_ahead)
    def test_valid_dates_accepted(self, days_ahead: int) -> None:
        """Dates 1-365 days in the future are accepted and return correct day count."""
        today = FIXED_TODAY
        exam_date = today + timedelta(days=days_ahead)
        result = validate_exam_date(exam_date, today=today)
        assert result == days_ahead, (
            f"Expected {days_ahead} days, got {result}"
        )

    @settings(max_examples=50)
    @given(days_past=invalid_days_past)
    def test_past_dates_rejected(self, days_past: int) -> None:
        """Dates in the past (0 or fewer days ahead) are rejected."""
        today = FIXED_TODAY
        exam_date = today + timedelta(days=days_past)
        with pytest.raises(ExamDateValidationError):
            validate_exam_date(exam_date, today=today)

    @settings(max_examples=50)
    @given(days_far=invalid_days_far_future)
    def test_far_future_dates_rejected(self, days_far: int) -> None:
        """Dates more than 365 days away are rejected."""
        today = FIXED_TODAY
        exam_date = today + timedelta(days=days_far)
        with pytest.raises(ExamDateValidationError):
            validate_exam_date(exam_date, today=today)

    @settings(max_examples=50)
    @given(days_ahead=valid_days_ahead)
    def test_return_value_is_positive_integer(self, days_ahead: int) -> None:
        """The returned day count is always a positive integer within [1, 365]."""
        today = FIXED_TODAY
        exam_date = today + timedelta(days=days_ahead)
        result = validate_exam_date(exam_date, today=today)
        assert 1 <= result <= 365, (
            f"Result {result} outside valid range [1, 365]"
        )


# ---------------------------------------------------------------------------
# Property 31: Study plan follows phase ordering (coverage → weakness → review)
# Validates: Requirements 17.1
# ---------------------------------------------------------------------------


class TestStudyPlanPhaseOrdering:
    """For any generated study plan, the timeline SHALL be divided into phases
    where coverage-gap subtopics are introduced first, weak areas are deepened
    second, and review/mock practice occupies the final 20% of the timeline.

    **Validates: Requirements 17.1**
    """

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=5, max_size=30),
        config=plan_config(),
    )
    def test_phases_appear_in_correct_order(
        self, subtopic_ids: list[int], config: PlanConfig
    ) -> None:
        """Coverage phase precedes weakness phase, which precedes review phase."""
        plan = _generate_plan(subtopic_ids, config)

        if not plan.assignments:
            return

        # Track first occurrence of each phase
        first_occurrence: dict[str, int] = {}
        for assignment in plan.assignments:
            if assignment.phase not in first_occurrence:
                first_occurrence[assignment.phase] = assignment.day_number

        # Coverage should come before or at the same time as weakness
        if "coverage" in first_occurrence and "weakness" in first_occurrence:
            assert first_occurrence["coverage"] <= first_occurrence["weakness"], (
                f"Coverage starts at day {first_occurrence['coverage']}, "
                f"but weakness starts at day {first_occurrence['weakness']}"
            )

        # Review should come after coverage and weakness
        if "review" in first_occurrence:
            if "coverage" in first_occurrence:
                assert first_occurrence["review"] > first_occurrence["coverage"], (
                    f"Review starts at day {first_occurrence['review']}, "
                    f"but coverage starts at day {first_occurrence['coverage']}"
                )

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=5, max_size=30),
        config=plan_config(),
    )
    def test_review_phase_occupies_final_portion(
        self, subtopic_ids: list[int], config: PlanConfig
    ) -> None:
        """Review phase assignments exist in the final 20% of the timeline."""
        plan = _generate_plan(subtopic_ids, config)

        if not plan.assignments:
            return

        total_days = plan.total_days
        if total_days < 5:
            return  # Too short to meaningfully verify proportions

        review_assignments = [
            a for a in plan.assignments if a.phase == "review"
        ]

        if not review_assignments:
            return

        # All review assignments should be in the last portion of the timeline
        first_review_day = min(a.day_number for a in review_assignments)
        # The review phase starts no earlier than 80% through the timeline
        # (allowing 1 day tolerance for rounding)
        expected_review_start = int(total_days * 0.80)
        assert first_review_day >= expected_review_start, (
            f"Review starts at day {first_review_day}, "
            f"expected no earlier than day {expected_review_start} "
            f"(80% of {total_days} days)"
        )

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=5, max_size=30),
        config=plan_config(),
    )
    def test_no_new_subtopics_in_review_phase(
        self, subtopic_ids: list[int], config: PlanConfig
    ) -> None:
        """Review phase should not introduce new subtopics."""
        plan = _generate_plan(subtopic_ids, config)

        review_assignments = [
            a for a in plan.assignments if a.phase == "review"
        ]

        for assignment in review_assignments:
            assert assignment.new_subtopics == [], (
                f"Day {assignment.day_number} (review phase) introduces "
                f"new subtopics: {assignment.new_subtopics}"
            )


# ---------------------------------------------------------------------------
# Property 32: Plan respects spaced introduction limits (max 3 new/day)
# Validates: Requirements 17.2
# ---------------------------------------------------------------------------


class TestPlanSpacedIntroductionLimits:
    """For any generated study plan, no single day SHALL introduce more than
    3 new subtopics, and review days SHALL be interspersed every 3 study days.

    **Validates: Requirements 17.2**
    """

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=5, max_size=60),
        config=plan_config(),
    )
    def test_max_3_new_subtopics_per_day(
        self, subtopic_ids: list[int], config: PlanConfig
    ) -> None:
        """No day introduces more than 3 new subtopics."""
        plan = _generate_plan(subtopic_ids, config)

        for assignment in plan.assignments:
            assert len(assignment.new_subtopics) <= 3, (
                f"Day {assignment.day_number} introduces "
                f"{len(assignment.new_subtopics)} subtopics, max is 3"
            )

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=10, max_size=60),
        days_ahead=integers(min_value=30, max_value=365),
    )
    def test_review_days_interspersed(
        self, subtopic_ids: list[int], days_ahead: int
    ) -> None:
        """Review days (days with review_subtopics and no new_subtopics)
        appear within the coverage/weakness phases, interspersed every ~3 days."""
        config = PlanConfig(
            target_exam_date=FIXED_TODAY + timedelta(days=days_ahead),
            available_hours_per_day=1.0,
            exam_category="Professional",
            mastered_subtopic_ids=[],
        )
        plan = _generate_plan(subtopic_ids, config)

        # Look at the coverage/weakness phase only
        non_review_assignments = [
            a for a in plan.assignments if a.phase != "review"
        ]

        if len(non_review_assignments) < 6:
            return  # Too short to verify spacing

        # Count review days (days where review_subtopics is non-empty and
        # no new subtopics are introduced) in the coverage phase
        review_days = [
            a for a in non_review_assignments
            if a.review_subtopics and not a.new_subtopics
        ]

        # With at least 6 coverage/weakness days, we should have some review days
        # (every 3rd study day is review)
        expected_min_review_days = len(non_review_assignments) // 4
        assert len(review_days) >= expected_min_review_days, (
            f"Expected at least {expected_min_review_days} review days "
            f"in {len(non_review_assignments)} non-review phase days, "
            f"got {len(review_days)}"
        )


# ---------------------------------------------------------------------------
# Property 33: Plan schedules mock exams at correct frequency
# Validates: Requirements 17.3
# ---------------------------------------------------------------------------


class TestPlanMockExamScheduling:
    """For any generated study plan with sufficient timeline (>= 2 weeks),
    mock exams SHALL be scheduled once per week starting from week 2,
    increasing to twice per week in the final 2 weeks before the exam date.

    **Validates: Requirements 17.3**
    """

    @settings(max_examples=50)
    @given(
        days_ahead=integers(min_value=14, max_value=365),
    )
    def test_mock_exams_start_from_week_2(self, days_ahead: int) -> None:
        """For timelines where the regular period exists (final_two_weeks_start >= 8),
        no mock exams are scheduled before day 8 (week 2 starts at day 8).
        When the entire timeline IS the final 2 weeks, earlier scheduling is expected."""
        mock_days = _compute_mock_exam_days(days_ahead)

        final_two_weeks_start = max(1, days_ahead - 13)

        # Only enforce the "no mocks before day 8" rule when the regular
        # period actually exists (i.e., when final_two_weeks_start >= 8)
        if final_two_weeks_start >= 8:
            for day in mock_days:
                assert day >= 8, (
                    f"Mock exam scheduled on day {day}, "
                    f"but should not start before day 8 (week 2)"
                )
        else:
            # When entire timeline is final-2-weeks intensive,
            # mocks can start from final_two_weeks_start
            for day in mock_days:
                assert day >= final_two_weeks_start, (
                    f"Mock exam scheduled on day {day}, "
                    f"but should not start before day {final_two_weeks_start}"
                )

    @settings(max_examples=50)
    @given(
        days_ahead=integers(min_value=1, max_value=7),
    )
    def test_no_mock_exams_for_short_timelines(self, days_ahead: int) -> None:
        """Timelines shorter than 8 days have no mock exams."""
        mock_days = _compute_mock_exam_days(days_ahead)
        assert len(mock_days) == 0, (
            f"Expected no mock exams for {days_ahead}-day timeline, "
            f"got {len(mock_days)}: {mock_days}"
        )

    @settings(max_examples=50)
    @given(
        days_ahead=integers(min_value=15, max_value=365),
    )
    def test_mock_exams_increase_in_final_2_weeks(self, days_ahead: int) -> None:
        """The final 2 weeks have more mock exams per week than earlier weeks."""
        mock_days = _compute_mock_exam_days(days_ahead)

        if not mock_days:
            return

        final_two_weeks_start = max(1, days_ahead - 13)

        # Count mocks in regular period vs final period
        regular_mocks = [d for d in mock_days if d < final_two_weeks_start]
        final_mocks = [d for d in mock_days if d >= final_two_weeks_start]

        if not regular_mocks or not final_mocks:
            return

        # Calculate frequency (mocks per week)
        regular_weeks = max(1, (final_two_weeks_start - 8) / 7)
        final_weeks = 2.0

        regular_freq = len(regular_mocks) / regular_weeks
        final_freq = len(final_mocks) / final_weeks

        # Final frequency should be >= regular frequency
        assert final_freq >= regular_freq - 0.1, (
            f"Final 2-week frequency ({final_freq:.2f}/week) "
            f"should be >= regular frequency ({regular_freq:.2f}/week)"
        )

    @settings(max_examples=50)
    @given(
        subtopic_ids=subtopic_id_list(min_size=10, max_size=30),
        days_ahead=integers(min_value=14, max_value=365),
    )
    def test_plan_mock_exams_match_computed_schedule(
        self, subtopic_ids: list[int], days_ahead: int
    ) -> None:
        """GeneratedPlan mock_exams_scheduled matches days with mock_exam_scheduled=True."""
        config = PlanConfig(
            target_exam_date=FIXED_TODAY + timedelta(days=days_ahead),
            available_hours_per_day=1.0,
            exam_category="Professional",
            mastered_subtopic_ids=[],
        )
        plan = _generate_plan(subtopic_ids, config)

        actual_mock_days = [
            a.day_number
            for a in plan.assignments
            if a.mock_exam_scheduled
        ]

        assert plan.mock_exams_scheduled == len(actual_mock_days), (
            f"Plan reports {plan.mock_exams_scheduled} mock exams, "
            f"but found {len(actual_mock_days)} days with mock_exam_scheduled=True"
        )


# ---------------------------------------------------------------------------
# Property 34: Plan excludes already-mastered subtopics
# Validates: Requirements 17.5
# ---------------------------------------------------------------------------


class TestPlanExcludesMasteredSubtopics:
    """For any returning user with existing mastery data, subtopics with
    mastery_score >= 0.8 SHALL NOT appear as new content introductions in the
    generated study plan.

    **Validates: Requirements 17.5**
    """

    @settings(max_examples=50)
    @given(
        config=plan_config_with_mastered(),
        extra_ids=subtopic_id_list(min_size=5, max_size=30),
    )
    def test_mastered_subtopics_not_introduced(
        self, config: PlanConfig, extra_ids: list[int]
    ) -> None:
        """Mastered subtopics never appear in new_subtopics of any day."""
        mastered_set = set(config.mastered_subtopic_ids)

        # Create a full list that includes some mastered and some unmastered
        all_ids = list(set(extra_ids) | mastered_set)

        plan = _generate_plan(all_ids, config)

        for assignment in plan.assignments:
            for sid in assignment.new_subtopics:
                assert sid not in mastered_set, (
                    f"Mastered subtopic {sid} was introduced as new "
                    f"on day {assignment.day_number}"
                )

    @settings(max_examples=50)
    @given(
        config=plan_config_with_mastered(),
        extra_ids=subtopic_id_list(min_size=5, max_size=30),
    )
    def test_plan_only_introduces_unmastered_subtopics(
        self, config: PlanConfig, extra_ids: list[int]
    ) -> None:
        """All introduced subtopics should be from the unmastered set."""
        mastered_set = set(config.mastered_subtopic_ids)
        all_ids = list(set(extra_ids) | mastered_set)

        plan = _generate_plan(all_ids, config)

        # Collect all introduced subtopics
        introduced: set[int] = set()
        for assignment in plan.assignments:
            introduced.update(assignment.new_subtopics)

        # None of the introduced should be in the mastered set
        overlap = introduced & mastered_set
        assert len(overlap) == 0, (
            f"Mastered subtopics introduced in plan: {overlap}"
        )

    @settings(max_examples=50)
    @given(
        days_ahead=integers(min_value=30, max_value=365),
    )
    def test_all_mastered_means_no_new_introductions(
        self, days_ahead: int
    ) -> None:
        """When all subtopics are mastered, no new subtopics are introduced."""
        all_ids = list(range(1, 21))
        config = PlanConfig(
            target_exam_date=FIXED_TODAY + timedelta(days=days_ahead),
            available_hours_per_day=1.0,
            exam_category="Professional",
            mastered_subtopic_ids=all_ids,  # All mastered
        )

        plan = _generate_plan(all_ids, config)

        for assignment in plan.assignments:
            assert assignment.new_subtopics == [], (
                f"Day {assignment.day_number} introduces subtopics "
                f"{assignment.new_subtopics} but all are mastered"
            )
