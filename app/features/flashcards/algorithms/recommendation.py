"""Recommendation engine for flashcard study suggestions.

Pure functions that compute study recommendations based on user
performance data. No DB access — receives pre-computed metrics.

Requirements: 12.1-12.5
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WeakSubtopic:
    """A subtopic where the user is underperforming."""

    tag: str
    retention_score: float
    card_count: int


@dataclass
class StudyRecommendation:
    """A single study recommendation."""

    type: str  # "weak_area", "daily_review", "quiz", "starter"
    title: str
    description: str
    priority: int = 0  # higher = more important
    deck_id: int | None = None
    tag: str | None = None


@dataclass
class RecommendationResult:
    """Complete set of recommendations for a user."""

    weak_subtopics: list[WeakSubtopic] = field(default_factory=list)
    recommendations: list[StudyRecommendation] = field(default_factory=list)
    recommended_daily_cards: int = 20


def identify_weak_subtopics(
    tag_retention_data: list[tuple[str, float, int]],
    *,
    max_results: int = 5,
) -> list[WeakSubtopic]:
    """Identify the N weakest subtopics by retention score (Req 12.1).

    Args:
        tag_retention_data: List of (tag, avg_retention, card_count) tuples.
        max_results: Maximum number of weak subtopics to return.

    Returns:
        Sorted list of weakest subtopics (lowest retention first).
    """
    subtopics = [
        WeakSubtopic(tag=tag, retention_score=ret, card_count=count)
        for tag, ret, count in tag_retention_data
        if count > 0
    ]
    subtopics.sort(key=lambda s: s.retention_score)
    return subtopics[:max_results]


def compute_daily_review_count(
    total_due: int,
    current_streak: int,
    avg_session_cards: float = 20.0,
) -> int:
    """Recommend a personalized daily review count (Req 12.3).

    Factors:
    - Base: average session card count
    - Streak bonus: +2 cards per streak day (up to +20)
    - Due pressure: if many overdue, increase slightly

    Returns a value between 10 and 100.
    """
    base = avg_session_cards
    streak_bonus = min(20, current_streak * 2)
    due_pressure = min(20, total_due // 5)

    recommended = int(base + streak_bonus + due_pressure)
    return max(10, min(100, recommended))


def generate_recommendations(
    *,
    tag_retention_data: list[tuple[str, float, int]],
    total_due: int,
    total_cards: int,
    current_streak: int,
    has_any_decks: bool,
) -> RecommendationResult:
    """Generate a full set of study recommendations (Req 12.1-12.5).

    Args:
        tag_retention_data: Per-tag retention averages.
        total_due: Total cards due for review.
        total_cards: Total cards the user has.
        current_streak: Current study streak in days.
        has_any_decks: Whether the user has any decks.

    Returns:
        RecommendationResult with weak areas and actionable suggestions.
    """
    weak = identify_weak_subtopics(tag_retention_data)
    daily_count = compute_daily_review_count(total_due, current_streak)

    recommendations: list[StudyRecommendation] = []

    # Starter recommendation for new users (Req 12.5)
    if not has_any_decks or total_cards == 0:
        recommendations.append(StudyRecommendation(
            type="starter",
            title="Get Started",
            description="Browse the marketplace for starter decks in your weakest areas.",
            priority=100,
        ))

    # Weak area recommendations (Req 12.1, 12.2)
    for subtopic in weak:
        if subtopic.retention_score < 0.6:
            recommendations.append(StudyRecommendation(
                type="weak_area",
                title=f"Focus on: {subtopic.tag}",
                description=(
                    f"Your retention for '{subtopic.tag}' is "
                    f"{subtopic.retention_score:.0%}. Review these cards today."
                ),
                priority=80,
                tag=subtopic.tag,
            ))

    # Daily review recommendation
    if total_due > 0:
        recommendations.append(StudyRecommendation(
            type="daily_review",
            title=f"Review {min(daily_count, total_due)} cards today",
            description=(
                f"You have {total_due} cards due. "
                f"We recommend reviewing {min(daily_count, total_due)} today."
            ),
            priority=90,
        ))

    # Targeted quiz suggestion (Req 12.4)
    low_retention_tags = [s for s in weak if s.retention_score < 0.6]
    if low_retention_tags:
        recommendations.append(StudyRecommendation(
            type="quiz",
            title="Take a targeted quiz",
            description=(
                f"Quiz yourself on '{low_retention_tags[0].tag}' "
                f"to strengthen weak areas."
            ),
            priority=70,
            tag=low_retention_tags[0].tag,
        ))

    # Sort by priority (highest first)
    recommendations.sort(key=lambda r: r.priority, reverse=True)

    return RecommendationResult(
        weak_subtopics=weak,
        recommendations=recommendations,
        recommended_daily_cards=daily_count,
    )
