"""Property-based tests for predicted score range and recommendations.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import (
    composite,
    floats,
    integers,
    lists,
    text,
)

from app.features.mock_analytics.algorithms.diagnostics import SubtopicDiagnostic
from app.features.mock_analytics.algorithms.prediction import (
    ActionableRecommendation,
    PredictedRange,
    compute_predicted_score,
    generate_recommendations,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_score_pct = floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)
valid_days_since = integers(min_value=0, max_value=365)
valid_retention = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)
valid_mastery = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)
valid_accuracy_pct = floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)
valid_questions_count = integers(min_value=1, max_value=50)
valid_subtopic_id = integers(min_value=1, max_value=1000)


@composite
def mock_score_entry(draw):
    """Generate a valid (score_pct, days_since) tuple."""
    score = draw(valid_score_pct)
    days = draw(valid_days_since)
    return (score, days)


@composite
def mock_scores_list(draw, min_size=2, max_size=20):
    """Generate a list of mock score entries with at least min_size entries."""
    entries = draw(
        lists(mock_score_entry(), min_size=min_size, max_size=max_size)
    )
    return entries


@composite
def subtopic_diagnostic(draw):
    """Generate a valid SubtopicDiagnostic."""
    subtopic_id = draw(valid_subtopic_id)
    questions_attempted = draw(integers(min_value=1, max_value=50))
    questions_correct = draw(integers(min_value=0, max_value=questions_attempted))
    points_lost = questions_attempted - questions_correct
    avg_seconds = draw(
        floats(min_value=2.0, max_value=600.0, allow_nan=False, allow_infinity=False)
    )
    accuracy_percentage = round(questions_correct / questions_attempted * 100, 1)
    return SubtopicDiagnostic(
        subtopic_id=subtopic_id,
        questions_attempted=questions_attempted,
        questions_correct=questions_correct,
        points_lost=points_lost,
        avg_seconds_per_question=round(avg_seconds, 1),
        accuracy_percentage=accuracy_percentage,
    )


@composite
def subtopic_diagnostics_below_target(draw, target_pct=80.0):
    """Generate a list of SubtopicDiagnostics where all are below target accuracy."""
    count = draw(integers(min_value=1, max_value=10))
    diagnostics = []
    for i in range(count):
        subtopic_id = i + 1
        questions_attempted = draw(integers(min_value=1, max_value=50))
        # Ensure accuracy is below target
        max_correct = int(questions_attempted * target_pct / 100.0) - 1
        if max_correct < 0:
            max_correct = 0
        questions_correct = draw(integers(min_value=0, max_value=max(0, max_correct)))
        points_lost = questions_attempted - questions_correct
        avg_seconds = draw(
            floats(min_value=2.0, max_value=600.0, allow_nan=False, allow_infinity=False)
        )
        accuracy_percentage = round(
            questions_correct / questions_attempted * 100, 1
        ) if questions_attempted > 0 else 0.0
        diagnostics.append(
            SubtopicDiagnostic(
                subtopic_id=subtopic_id,
                questions_attempted=questions_attempted,
                questions_correct=questions_correct,
                points_lost=points_lost,
                avg_seconds_per_question=round(avg_seconds, 1),
                accuracy_percentage=accuracy_percentage,
            )
        )
    return diagnostics


# ---------------------------------------------------------------------------
# Property 20: Predicted score range follows formula with clamping
# Validates: Requirements 11.1, 11.2
# ---------------------------------------------------------------------------


class TestPredictedScoreRangeFollowsFormulaWithClamping:
    """For ANY valid mock scores (>=2) and retention value,
    compute_predicted_score should produce a range where:
    - lower_bound >= 0
    - upper_bound <= 100
    - lower_bound <= midpoint <= upper_bound

    **Validates: Requirements 11.1, 11.2**
    """

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=2, max_size=20),
        avg_retention=valid_retention,
    )
    def test_lower_bound_is_non_negative(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.2

        lower_bound must always be >= 0 (clamped).
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.lower_bound >= 0.0

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=2, max_size=20),
        avg_retention=valid_retention,
    )
    def test_upper_bound_is_at_most_100(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.2

        upper_bound must always be <= 100 (clamped).
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.upper_bound <= 100.0

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=2, max_size=20),
        avg_retention=valid_retention,
    )
    def test_ordering_lower_midpoint_upper(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.1, 11.2

        lower_bound <= midpoint <= upper_bound must always hold.
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.lower_bound <= result.midpoint
        assert result.midpoint <= result.upper_bound


# ---------------------------------------------------------------------------
# Property 21: Confidence level matches exam count ranges
# Validates: Requirements 11.4
# ---------------------------------------------------------------------------


class TestConfidenceLevelMatchesExamCountRanges:
    """For ANY number of exams >= 2, the confidence_level field must follow:
    - 2-3 exams = "low"
    - 4-6 exams = "medium"
    - 7+ exams = "high"

    **Validates: Requirements 11.4**
    """

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=2, max_size=3),
        avg_retention=valid_retention,
    )
    def test_low_confidence_for_2_to_3_exams(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.4

        2-3 exams should yield confidence_level = "low".
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.confidence_level == "low"

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=4, max_size=6),
        avg_retention=valid_retention,
    )
    def test_medium_confidence_for_4_to_6_exams(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.4

        4-6 exams should yield confidence_level = "medium".
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.confidence_level == "medium"

    @settings(max_examples=50)
    @given(
        mock_scores=mock_scores_list(min_size=7, max_size=20),
        avg_retention=valid_retention,
    )
    def test_high_confidence_for_7_plus_exams(
        self,
        mock_scores: list[tuple[float, int]],
        avg_retention: float,
    ) -> None:
        """Validates: Requirements 11.4

        7+ exams should yield confidence_level = "high".
        """
        result = compute_predicted_score(mock_scores, avg_retention)
        assert result is not None
        assert result.confidence_level == "high"


# ---------------------------------------------------------------------------
# Property 22: Recommendations are ranked by estimated point gain
# Validates: Requirements 12.1, 12.2, 12.3
# ---------------------------------------------------------------------------


class TestRecommendationsRankedByEstimatedPointGain:
    """For ANY valid set of subtopic diagnostics below target accuracy,
    generate_recommendations should produce results that are:
    - Sorted by estimated_point_gain descending
    - Maximum 5 items
    - Only include subtopics below target accuracy

    **Validates: Requirements 12.1, 12.2, 12.3**
    """

    @settings(max_examples=50)
    @given(
        diagnostics=subtopic_diagnostics_below_target(),
        mastery=valid_mastery,
    )
    def test_recommendations_sorted_descending_by_point_gain(
        self,
        diagnostics: list[SubtopicDiagnostic],
        mastery: float,
    ) -> None:
        """Validates: Requirements 12.2

        Recommendations must be sorted by estimated_point_gain descending.
        """
        subtopic_names = {d.subtopic_id: f"Subtopic {d.subtopic_id}" for d in diagnostics}
        questions_per_subtopic = {d.subtopic_id: d.questions_attempted for d in diagnostics}
        mastery_scores = {d.subtopic_id: mastery for d in diagnostics}

        result = generate_recommendations(
            subtopic_diagnostics=diagnostics,
            subtopic_names=subtopic_names,
            questions_per_subtopic_in_exam=questions_per_subtopic,
            mastery_scores=mastery_scores,
            target_accuracy=0.80,
        )

        for i in range(len(result) - 1):
            assert result[i].estimated_point_gain >= result[i + 1].estimated_point_gain

    @settings(max_examples=50)
    @given(
        diagnostics=subtopic_diagnostics_below_target(),
        mastery=valid_mastery,
    )
    def test_recommendations_max_5_items(
        self,
        diagnostics: list[SubtopicDiagnostic],
        mastery: float,
    ) -> None:
        """Validates: Requirements 12.1

        At most 5 recommendations should be returned.
        """
        subtopic_names = {d.subtopic_id: f"Subtopic {d.subtopic_id}" for d in diagnostics}
        questions_per_subtopic = {d.subtopic_id: d.questions_attempted for d in diagnostics}
        mastery_scores = {d.subtopic_id: mastery for d in diagnostics}

        result = generate_recommendations(
            subtopic_diagnostics=diagnostics,
            subtopic_names=subtopic_names,
            questions_per_subtopic_in_exam=questions_per_subtopic,
            mastery_scores=mastery_scores,
            target_accuracy=0.80,
        )

        assert len(result) <= 5

    @settings(max_examples=50)
    @given(
        diagnostics=subtopic_diagnostics_below_target(),
        mastery=valid_mastery,
    )
    def test_recommendations_only_below_target(
        self,
        diagnostics: list[SubtopicDiagnostic],
        mastery: float,
    ) -> None:
        """Validates: Requirements 12.1, 12.3

        Only subtopics with current_accuracy < target_accuracy should appear.
        """
        subtopic_names = {d.subtopic_id: f"Subtopic {d.subtopic_id}" for d in diagnostics}
        questions_per_subtopic = {d.subtopic_id: d.questions_attempted for d in diagnostics}
        mastery_scores = {d.subtopic_id: mastery for d in diagnostics}
        target = 0.80
        target_pct = target * 100.0

        result = generate_recommendations(
            subtopic_diagnostics=diagnostics,
            subtopic_names=subtopic_names,
            questions_per_subtopic_in_exam=questions_per_subtopic,
            mastery_scores=mastery_scores,
            target_accuracy=target,
        )

        for rec in result:
            assert rec.current_accuracy < target_pct
