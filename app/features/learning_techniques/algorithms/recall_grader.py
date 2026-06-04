"""Recall grader algorithm for generation-effect fill-in-the-blank mode.

All functions are pure — no DB access, no side effects.
"""

from __future__ import annotations


def _levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def grade_recall_answer(
    user_response: str,
    correct_answer: str,
    levenshtein_threshold: int = 2,
) -> tuple[bool | None, str]:
    """Grade a recall answer by exact then fuzzy keyword matching.

    Returns (is_correct, match_type) where:
    - is_correct=True, match_type="exact"    — exact case-insensitive match
    - is_correct=True, match_type="fuzzy"    — within Levenshtein distance threshold
    - is_correct=None, match_type="needs_review" — no match; user self-assesses

    Property 40: Levenshtein distance ≤ 2 accepts fuzzy matches.
    """
    response = user_response.strip().lower()
    correct = correct_answer.strip().lower()

    if not response or not correct:
        return None, "needs_review"

    # Exact match
    if response == correct:
        return True, "exact"

    # Word-level fuzzy match — any word in response close to correct answer
    response_words = response.split()
    correct_words = correct.split()

    for r_word in response_words:
        for c_word in correct_words:
            if len(r_word) >= 3 and len(c_word) >= 3:  # skip trivially short words
                if _levenshtein_distance(r_word, c_word) <= levenshtein_threshold:
                    return True, "fuzzy"

    # Full string fuzzy match for single-word answers
    if " " not in correct and _levenshtein_distance(response, correct) <= levenshtein_threshold:
        return True, "fuzzy"

    return None, "needs_review"
