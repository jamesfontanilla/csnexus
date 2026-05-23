"""FSRS-inspired spaced repetition engine — pure functions only.

All functions in this module are deterministic and side-effect-free.
They operate on immutable dataclasses and return new instances.

Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 10.2
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, timedelta

from app.features.flashcards.models import ConfidenceLevel, ResponseType


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MIN_EASE_FACTOR: float = 1.3
MAX_EASE_FACTOR: float = 3.5
MIN_MEMORY_STABILITY: float = 0.1
MIN_REVIEW_INTERVAL: int = 1
MAX_REVIEW_INTERVAL: int = 365

# Confidence multipliers (Req 10.2)
CONFIDENCE_MULTIPLIERS: dict[ConfidenceLevel, float] = {
    ConfidenceLevel.GUESSED: 0.3,
    ConfidenceLevel.UNSURE: 0.5,
    ConfidenceLevel.CONFIDENT: 0.85,
    ConfidenceLevel.MASTERED: 1.0,
}


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CardState:
    """Immutable snapshot of a card's scheduling parameters (Req 5.1)."""

    ease_factor: float = 2.5
    retention_score: float = 0.0
    memory_stability: float = 1.0
    review_interval: int = 1
    lapse_count: int = 0
    last_review_date: date | None = None


@dataclass(frozen=True)
class SchedulingResult:
    """Output of compute_next_interval — new card state after a review."""

    ease_factor: float
    retention_score: float
    memory_stability: float
    review_interval: int
    lapse_count: int
    next_review_date: date


# ---------------------------------------------------------------------------
# Clamping Helpers
# ---------------------------------------------------------------------------


def _clamp_ease_factor(value: float) -> float:
    """Clamp ease_factor to [1.3, 3.5] (Req 5.8)."""
    return max(MIN_EASE_FACTOR, min(MAX_EASE_FACTOR, value))


def _clamp_memory_stability(value: float) -> float:
    """Clamp memory_stability to minimum 0.1 (Req 5.9)."""
    return max(MIN_MEMORY_STABILITY, value)


def _clamp_review_interval(value: int) -> int:
    """Clamp review_interval to [1, 365]."""
    return max(MIN_REVIEW_INTERVAL, min(MAX_REVIEW_INTERVAL, value))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def compute_next_interval(
    state: CardState,
    response: ResponseType,
    confidence: ConfidenceLevel,
    today: date,
) -> SchedulingResult:
    """Pure function: given current state + user response, compute next state.

    Deterministic: same inputs always produce same outputs (Req 5.10).

    Scheduling rules:
    - "remembered" + "mastered": interval × ease_factor, stability +10% (Req 5.2)
    - "remembered" + "confident": interval × (ease_factor × 0.85), stability unchanged (Req 5.3)
    - "remembered" + "unsure": interval = max(1, floor(interval × 0.5)), stability −10% (Req 5.4)
    - "remembered" + "guessed": uses confidence multiplier 0.3 on base interval (Req 10.2)
    - "forgot": interval = 1, lapse_count +1, ease −0.2, stability −30% (Req 5.5)
    - "skipped": no scheduling change, just advance the date

    Confidence multipliers are applied to the computed interval (Req 10.2).
    """
    ease_factor = state.ease_factor
    memory_stability = state.memory_stability
    review_interval = state.review_interval
    lapse_count = state.lapse_count

    if response == ResponseType.FORGOT:
        # Req 5.5: reset interval, increment lapse, decrease ease and stability
        review_interval = 1
        lapse_count += 1
        ease_factor -= 0.2
        memory_stability *= 0.7  # reduce by 30%

    elif response == ResponseType.REMEMBERED:
        # Compute base interval depending on confidence
        confidence_multiplier = CONFIDENCE_MULTIPLIERS[confidence]

        if confidence == ConfidenceLevel.MASTERED:
            # Req 5.2: multiply interval by ease_factor, increase stability by 10%
            raw_interval = state.review_interval * ease_factor
            memory_stability *= 1.1
        elif confidence == ConfidenceLevel.CONFIDENT:
            # Req 5.3: multiply interval by (ease_factor × 0.85), stability unchanged
            raw_interval = state.review_interval * (ease_factor * 0.85)
        elif confidence == ConfidenceLevel.UNSURE:
            # Req 5.4: interval = max(1, floor(current × 0.5)), stability −10%
            raw_interval = max(1, math.floor(state.review_interval * 0.5))
            memory_stability *= 0.9
        else:
            # ConfidenceLevel.GUESSED: apply multiplier to base calculation
            # Base calculation uses ease_factor, then multiplied by 0.3
            raw_interval = state.review_interval * ease_factor * confidence_multiplier

        # For mastered/confident/unsure, the confidence multiplier is already
        # embedded in the formula per requirements. For guessed, it's explicit.
        # The requirements define specific formulas per confidence level,
        # so we use raw_interval directly (multiplier already applied in formula).
        review_interval = max(1, math.floor(raw_interval))

    elif response == ResponseType.SKIPPED:
        # Skipped: no scheduling change, just set next review date
        pass

    # Apply clamping (Req 5.8, 5.9)
    ease_factor = _clamp_ease_factor(ease_factor)
    memory_stability = _clamp_memory_stability(memory_stability)
    review_interval = _clamp_review_interval(review_interval)

    # Compute retention score based on elapsed days since last review
    elapsed_days = 0.0
    if state.last_review_date is not None:
        elapsed_days = float((today - state.last_review_date).days)
    retention_score = compute_retention_score(memory_stability, elapsed_days)

    # Next review date
    next_review_date = today + timedelta(days=review_interval)

    return SchedulingResult(
        ease_factor=ease_factor,
        retention_score=retention_score,
        memory_stability=memory_stability,
        review_interval=review_interval,
        lapse_count=lapse_count,
        next_review_date=next_review_date,
    )


def compute_retention_score(
    memory_stability: float,
    elapsed_days: float,
) -> float:
    """Compute retention_score = e^(−elapsed_days / memory_stability) (Req 5.6).

    Returns a value in [0.0, 1.0].
    memory_stability is clamped to minimum 0.1 to avoid division by zero.
    """
    stability = max(MIN_MEMORY_STABILITY, memory_stability)
    return math.exp(-elapsed_days / stability)


def compute_mastery_percentage(
    successful_reviews: int,
    total_reviews: int,
    retention_score: float,
) -> float:
    """Compute mastery = (successful / total) × retention_score × 100 (Req 5.7).

    Returns a value capped at 100.0.
    If total_reviews is 0, returns 0.0.
    """
    if total_reviews <= 0:
        return 0.0
    raw = (successful_reviews / total_reviews) * retention_score * 100.0
    return min(100.0, raw)
