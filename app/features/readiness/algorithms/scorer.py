"""Pure scoring functions for readiness score computation.

All functions in this module are pure — no database access, no side effects.
The service layer orchestrates data retrieval and calls these functions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentWeights:
    """Weights for each readiness score component. Must sum to 1.0."""

    mastery: float = 0.40
    retention: float = 0.25
    mock_exam: float = 0.25
    coverage: float = 0.10


@dataclass(frozen=True)
class ReadinessComponents:
    """Individual component scores, each on a 0-100 scale."""

    mastery_component: float
    retention_component: float
    mock_component: float
    coverage_component: float


@dataclass(frozen=True)
class ReadinessResult:
    """Final readiness score with breakdown."""

    score: int  # 0-100, clamped and rounded half-up
    components: ReadinessComponents
    weights: ComponentWeights


def compute_mastery_component(
    mastery_scores: list[tuple[float, float]],
) -> float:
    """Weighted average of mastery scores by exam question proportion.

    Args:
        mastery_scores: List of (mastery_score, exam_weight) tuples.
            mastery_score is 0.0–1.0, exam_weight is the proportion of
            exam questions for that subtopic.

    Returns:
        Component score on 0–100 scale. Returns 0.0 for empty input.
    """
    if not mastery_scores:
        return 0.0

    total_weight = sum(weight for _, weight in mastery_scores)
    if total_weight == 0.0:
        return 0.0

    weighted_sum = sum(score * weight for score, weight in mastery_scores)
    return (weighted_sum / total_weight) * 100.0


def compute_retention_component(
    fsrs_retentions: list[float] | None,
    subtopic_retention_scores: list[float] | None,
    days_until_exam: int,
) -> float:
    """Average FSRS retention projected to exam date, or fallback to subtopic retention.

    Args:
        fsrs_retentions: List of FSRS retention probabilities (0.0–1.0) projected
            to the exam date. None or empty triggers fallback.
        subtopic_retention_scores: Fallback list of subtopic retention scores (0.0–1.0).
            Used when fsrs_retentions is None or empty.
        days_until_exam: Days until exam. Defaults to 30 if no exam date set.

    Returns:
        Component score on 0–100 scale. Returns 0.0 if both inputs are None/empty.
    """
    if fsrs_retentions:
        return (sum(fsrs_retentions) / len(fsrs_retentions)) * 100.0

    if subtopic_retention_scores:
        return (sum(subtopic_retention_scores) / len(subtopic_retention_scores)) * 100.0

    return 0.0


def compute_mock_component(
    mock_scores: list[tuple[float, int]],
) -> float:
    """Recency-weighted average of mock exam scores.

    Args:
        mock_scores: List of (percentage_correct, days_since_exam) tuples.
            percentage_correct is 0–100.
            Only fully completed exams should be included by the caller.

    Returns:
        Component score on 0–100 scale. Returns 0.0 for empty input.

    Weighting:
        - days_since_exam <= 14: weight 1.0
        - days_since_exam 15–30: weight 0.7
        - days_since_exam > 30: weight 0.4
    """
    if not mock_scores:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0

    for percentage_correct, days_since in mock_scores:
        if days_since <= 14:
            weight = 1.0
        elif days_since <= 30:
            weight = 0.7
        else:
            weight = 0.4

        weighted_sum += percentage_correct * weight
        total_weight += weight

    if total_weight == 0.0:
        return 0.0

    return weighted_sum / total_weight


def compute_coverage_component(
    subtopic_coverage: list[tuple[int, int]],
    threshold: float = 0.10,
) -> float:
    """Percentage of subtopics where user attempted >= threshold of available questions.

    Args:
        subtopic_coverage: List of (attempted, available) tuples per subtopic.
            Each subtopic has a minimum of 60 available questions.
        threshold: Minimum fraction of available questions that must be attempted
            for a subtopic to count as "covered". Defaults to 0.10 (10%).

    Returns:
        Component score on 0–100 scale (percentage of subtopics meeting threshold).
        Returns 0.0 for empty input.
    """
    if not subtopic_coverage:
        return 0.0

    meeting_threshold = 0
    for attempted, available in subtopic_coverage:
        if available > 0 and attempted >= threshold * available:
            meeting_threshold += 1

    return (meeting_threshold / len(subtopic_coverage)) * 100.0


def _round_half_up(x: float) -> int:
    """Round to nearest integer using half-up rounding (0.5 rounds up)."""
    return int(math.floor(x + 0.5))


def compute_readiness_score(
    components: ReadinessComponents,
    weights: ComponentWeights,
) -> int:
    """Combine components with weights, round half-up, clamp to 0-100.

    Args:
        components: Individual component scores (each 0-100).
        weights: Weight for each component (should sum to 1.0).

    Returns:
        Final readiness score as integer, clamped to [0, 100].
    """
    raw_score = (
        components.mastery_component * weights.mastery
        + components.retention_component * weights.retention
        + components.mock_component * weights.mock_exam
        + components.coverage_component * weights.coverage
    )

    rounded = _round_half_up(raw_score)
    return max(0, min(100, rounded))


def redistribute_weights_no_mock() -> ComponentWeights:
    """Return adjusted weights when user has no mock exam history.

    Redistributes mock_exam weight (25%) equally across mastery and retention:
        - mastery: 40% + 12.5% = 52.5%
        - retention: 25% + 12.5% = 37.5%
        - mock_exam: 0%
        - coverage: 10% (unchanged)

    Returns:
        ComponentWeights with redistributed values.
    """
    return ComponentWeights(
        mastery=0.525,
        retention=0.375,
        mock_exam=0.0,
        coverage=0.10,
    )
