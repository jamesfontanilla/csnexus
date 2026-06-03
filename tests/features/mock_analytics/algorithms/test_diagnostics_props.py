"""Property-based tests for diagnostics computation (Properties 16-19).

Uses Hypothesis to validate universal correctness properties of the
compute_diagnostic pure function.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from app.features.mock_analytics.algorithms.diagnostics import (
    compute_diagnostic,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

DIFFICULTIES = ["easy", "medium", "hard"]


@st.composite
def answer_tuple(draw):
    """Generate a single answer tuple: (subtopic_id, is_correct, question_id, seconds, difficulty)."""
    subtopic_id = draw(st.integers(min_value=1, max_value=50))
    is_correct = draw(st.booleans())
    question_id = draw(st.integers(min_value=1, max_value=10000))
    seconds = draw(st.floats(min_value=0.5, max_value=900.0, allow_nan=False, allow_infinity=False))
    difficulty = draw(st.sampled_from(DIFFICULTIES))
    return (subtopic_id, is_correct, question_id, seconds, difficulty)


@st.composite
def answers_list(draw, min_size=1, max_size=100):
    """Generate a non-empty list of answer tuples."""
    return draw(st.lists(answer_tuple(), min_size=min_size, max_size=max_size))


@st.composite
def answers_with_historical(draw):
    """Generate answers and a historical_accuracy dict that overlaps with some subtopics."""
    answers = draw(answers_list(min_size=1, max_size=60))
    subtopic_ids = list({a[0] for a in answers})

    # Pick a subset of subtopic_ids to have historical data
    count = draw(st.integers(min_value=0, max_value=len(subtopic_ids)))
    selected = draw(
        st.lists(
            st.sampled_from(subtopic_ids),
            min_size=count,
            max_size=count,
            unique=True,
        )
    ) if subtopic_ids else []

    historical_accuracy = {}
    for sid in selected:
        historical_accuracy[sid] = draw(
            st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
        )

    return answers, historical_accuracy


# ---------------------------------------------------------------------------
# Property 16: Diagnostic total score equals percentage correct
# Validates: Requirements 10.1
# ---------------------------------------------------------------------------


class TestProperty16DiagnosticTotalScore:
    """**Validates: Requirements 10.1**"""

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_total_score_equals_percentage_correct(self, answers):
        """For any set of mock exam answers, total_score = (correct/total) * 100, rounded to 1 decimal."""
        result = compute_diagnostic(answers, historical_accuracy={})

        total_correct = sum(1 for _, is_correct, *_ in answers if is_correct)
        total_questions = len(answers)
        expected_score = round(total_correct / total_questions * 100, 1)

        assert result.total_score == expected_score

    @given(answers=answers_list(min_size=1, max_size=50))
    @settings(max_examples=50)
    def test_total_score_ignores_time_outliers_for_correctness(self, answers):
        """Time outliers (<2s or >600s) are excluded from time averages but NOT from correctness."""
        result = compute_diagnostic(answers, historical_accuracy={})

        # total_score must always be based on ALL answers regardless of time
        total_correct = sum(1 for _, is_correct, *_ in answers if is_correct)
        total_questions = len(answers)
        expected_score = round(total_correct / total_questions * 100, 1)

        assert result.total_score == expected_score

    @settings(max_examples=50)
    @given(data=st.data())
    def test_total_score_bounded_zero_to_hundred(self, data):
        """Total score is always in [0.0, 100.0]."""
        answers = data.draw(answers_list(min_size=1, max_size=80))
        result = compute_diagnostic(answers, historical_accuracy={})

        assert 0.0 <= result.total_score <= 100.0


# ---------------------------------------------------------------------------
# Property 17: Highest impact areas are top-5 by points lost
# Validates: Requirements 10.2
# ---------------------------------------------------------------------------


class TestProperty17HighestImpactAreas:
    """**Validates: Requirements 10.2**"""

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_highest_impact_at_most_five(self, answers):
        """highest_impact_areas contains at most 5 subtopics."""
        result = compute_diagnostic(answers, historical_accuracy={})

        assert len(result.highest_impact_areas) <= 5

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_highest_impact_only_positive_points_lost(self, answers):
        """highest_impact_areas only includes subtopics with points_lost > 0."""
        result = compute_diagnostic(answers, historical_accuracy={})

        for area in result.highest_impact_areas:
            assert area.points_lost > 0

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_highest_impact_sorted_by_points_lost_desc(self, answers):
        """highest_impact_areas is sorted by points_lost descending."""
        result = compute_diagnostic(answers, historical_accuracy={})

        if len(result.highest_impact_areas) > 1:
            for i in range(len(result.highest_impact_areas) - 1):
                assert (
                    result.highest_impact_areas[i].points_lost
                    >= result.highest_impact_areas[i + 1].points_lost
                )

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_highest_impact_is_top5_from_breakdowns(self, answers):
        """highest_impact_areas matches top-5 from subtopic_breakdowns filtered and sorted."""
        result = compute_diagnostic(answers, historical_accuracy={})

        # Manually compute expected
        with_loss = [b for b in result.subtopic_breakdowns if b.points_lost > 0]
        sorted_by_loss = sorted(with_loss, key=lambda b: b.points_lost, reverse=True)
        expected = sorted_by_loss[:5]

        assert result.highest_impact_areas == expected


# ---------------------------------------------------------------------------
# Property 18: Regression alerts fire on >15 percentage point decline
# Validates: Requirements 10.3
# ---------------------------------------------------------------------------


class TestProperty18RegressionAlerts:
    """**Validates: Requirements 10.3**"""

    @given(data=answers_with_historical())
    @settings(max_examples=50)
    def test_regression_alerts_only_for_decline_above_15(self, data):
        """Regression alerts only fire when decline > 15 percentage points."""
        answers, historical_accuracy = data
        result = compute_diagnostic(answers, historical_accuracy)

        for subtopic_id, decline in result.regression_alerts:
            assert decline > 15.0

    @given(data=answers_with_historical())
    @settings(max_examples=50)
    def test_regression_alerts_only_for_subtopics_with_history(self, data):
        """Regression alerts only include subtopics that have historical data."""
        answers, historical_accuracy = data
        result = compute_diagnostic(answers, historical_accuracy)

        for subtopic_id, _ in result.regression_alerts:
            assert subtopic_id in historical_accuracy

    @given(data=answers_with_historical())
    @settings(max_examples=50)
    def test_regression_alerts_completeness(self, data):
        """Every subtopic with historical data and >15 decline must appear in alerts."""
        answers, historical_accuracy = data
        result = compute_diagnostic(answers, historical_accuracy)

        # Compute current accuracy per subtopic from breakdowns
        current_accuracy_map = {
            b.subtopic_id: b.accuracy_percentage
            for b in result.subtopic_breakdowns
        }

        alert_subtopics = {sid for sid, _ in result.regression_alerts}

        for subtopic_id, hist_acc in historical_accuracy.items():
            if subtopic_id in current_accuracy_map:
                decline = hist_acc - current_accuracy_map[subtopic_id]
                if decline > 15.0:
                    assert subtopic_id in alert_subtopics
                else:
                    assert subtopic_id not in alert_subtopics

    @given(data=answers_with_historical())
    @settings(max_examples=50)
    def test_regression_decline_value_is_correct(self, data):
        """The decline value in each alert matches historical - current, rounded to 1 decimal."""
        answers, historical_accuracy = data
        result = compute_diagnostic(answers, historical_accuracy)

        current_accuracy_map = {
            b.subtopic_id: b.accuracy_percentage
            for b in result.subtopic_breakdowns
        }

        for subtopic_id, decline in result.regression_alerts:
            expected_decline = round(
                historical_accuracy[subtopic_id] - current_accuracy_map[subtopic_id], 1
            )
            assert decline == expected_decline


# ---------------------------------------------------------------------------
# Property 19: Difficulty performance computes per-level accuracy
# Validates: Requirements 10.4
# ---------------------------------------------------------------------------


class TestProperty19DifficultyPerformance:
    """**Validates: Requirements 10.4**"""

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_difficulty_performance_per_level_accuracy(self, answers):
        """difficulty_performance contains correct percentage grouped by difficulty level."""
        result = compute_diagnostic(answers, historical_accuracy={})

        # Manually compute expected per-level accuracy
        difficulty_data: dict[str, list[bool]] = {}
        for _, is_correct, _, _, difficulty in answers:
            if difficulty not in difficulty_data:
                difficulty_data[difficulty] = []
            difficulty_data[difficulty].append(is_correct)

        for level, results in difficulty_data.items():
            correct = sum(1 for r in results if r)
            total = len(results)
            expected_accuracy = round(correct / total * 100, 1)
            assert level in result.difficulty_performance
            assert result.difficulty_performance[level] == expected_accuracy

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_difficulty_performance_only_present_levels(self, answers):
        """difficulty_performance only contains levels that have at least one question."""
        result = compute_diagnostic(answers, historical_accuracy={})

        present_levels = {a[4] for a in answers}
        assert set(result.difficulty_performance.keys()) == present_levels

    @given(answers=answers_list(min_size=1, max_size=100))
    @settings(max_examples=50)
    def test_difficulty_performance_values_bounded(self, answers):
        """All difficulty performance values are in [0.0, 100.0]."""
        result = compute_diagnostic(answers, historical_accuracy={})

        for level, accuracy in result.difficulty_performance.items():
            assert 0.0 <= accuracy <= 100.0
