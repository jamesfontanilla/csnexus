"""Levenshtein distance-based answer comparison for typed answer study mode."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Strictness(str, Enum):
    """Comparison strictness modes for typed answer validation."""

    EXACT = "exact"
    CONTAINS = "contains"
    FUZZY = "fuzzy"


@dataclass(frozen=True)
class AnswerComparison:
    """Result of comparing a user's typed answer against the correct answer."""

    is_correct: bool
    similarity_score: float  # 0.0–1.0 Levenshtein ratio
    correct_answer: str


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))

    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost is 0 if characters match, 1 otherwise
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (0 if c1 == c2 else 1)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def _levenshtein_ratio(s1: str, s2: str) -> float:
    """Compute the Levenshtein similarity ratio: 1 - (distance / max(len(s1), len(s2))).

    Returns 1.0 for identical strings, 0.0 for completely different strings.
    Returns 1.0 if both strings are empty.
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    distance = _levenshtein_distance(s1, s2)
    return 1.0 - (distance / max_len)


def compare_typed_answer(
    user_answer: str,
    correct_answer: str,
    strictness: Strictness = Strictness.CONTAINS,
) -> AnswerComparison:
    """Compare a user's typed answer against the correct answer.

    Strictness modes:
    - EXACT: case-insensitive exact match (after stripping whitespace)
    - CONTAINS: correct answer appears within user answer (case-insensitive, after stripping)
    - FUZZY: Levenshtein ratio >= 0.8 considered correct

    Always computes the Levenshtein similarity_score regardless of strictness mode.
    """
    user_stripped = user_answer.strip()
    correct_stripped = correct_answer.strip()

    user_lower = user_stripped.lower()
    correct_lower = correct_stripped.lower()

    # Always compute similarity score based on stripped, lowercased strings
    similarity_score = _levenshtein_ratio(user_lower, correct_lower)

    if strictness == Strictness.EXACT:
        is_correct = user_lower == correct_lower
    elif strictness == Strictness.CONTAINS:
        is_correct = correct_lower in user_lower
    elif strictness == Strictness.FUZZY:
        is_correct = similarity_score >= 0.8
    else:
        # Defensive fallback — should never happen with the enum
        is_correct = False

    return AnswerComparison(
        is_correct=is_correct,
        similarity_score=similarity_score,
        correct_answer=correct_answer,
    )
