"""Category interleaving algorithm for flashcard study sessions.

Reorders cards so that no more than `max_consecutive_same_category` consecutive
cards share the same category, while maintaining proportional representation.

Pure function — does not modify the input list.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Protocol, TypeVar


class HasCategory(Protocol):
    """Any object with a readable `category` attribute."""

    @property
    def category(self) -> str: ...


T = TypeVar("T", bound=HasCategory)


def interleave_cards(
    cards: list[T],
    max_consecutive_same_category: int = 3,
) -> list[T]:
    """Reorder cards so no more than N consecutive share the same category.

    Algorithm:
    1. Group cards by category.
    2. Build output via round-robin across categories (largest-first).
    3. Post-check: if any run exceeds max_consecutive, swap with the nearest
       card from a different category.

    If all cards belong to the same category the constraint cannot be satisfied
    — return them as-is (new list, input unchanged).

    Args:
        cards: List of objects with a `.category` attribute.
        max_consecutive_same_category: Maximum allowed consecutive same-category
            cards (default 3).

    Returns:
        A new list with the same elements reordered to satisfy the constraint.
    """
    if not cards:
        return []

    # Group cards by category, preserving insertion order within each group.
    groups: dict[str, list[T]] = defaultdict(list)
    for card in cards:
        groups[card.category].append(card)

    # If only one category exists, constraint is unsatisfiable — return copy.
    if len(groups) <= 1:
        return list(cards)

    # Greedy placement: place cards from the largest group first, interleaving
    # with cards from other groups to respect the max_consecutive constraint.
    # This avoids the round-robin issue where small groups get exhausted early,
    # leaving long runs of the dominant category at the end.
    result: list[T] = []
    category_order = sorted(groups.keys(), key=lambda c: len(groups[c]), reverse=True)
    iterators: dict[str, int] = {cat: 0 for cat in category_order}
    consecutive_count = 0
    last_category: str | None = None

    total_remaining = len(cards)
    while total_remaining > 0:
        placed = False
        # Try to place a card from the best available category.
        # Prefer the category with the most remaining cards, but respect the
        # consecutive constraint.
        for cat in sorted(
            category_order,
            key=lambda c: len(groups[c]) - iterators[c],
            reverse=True,
        ):
            remaining_in_cat = len(groups[cat]) - iterators[cat]
            if remaining_in_cat <= 0:
                continue
            if cat == last_category and consecutive_count >= max_consecutive_same_category:
                continue
            # Place this card.
            result.append(groups[cat][iterators[cat]])
            iterators[cat] += 1
            total_remaining -= 1
            if cat == last_category:
                consecutive_count += 1
            else:
                consecutive_count = 1
                last_category = cat
            placed = True
            break

        if not placed:
            # All remaining cards are from the same category that's at the
            # consecutive limit. We must place them anyway (constraint
            # unsatisfiable for this tail).
            for cat in category_order:
                while iterators[cat] < len(groups[cat]):
                    result.append(groups[cat][iterators[cat]])
                    iterators[cat] += 1
                    total_remaining -= 1
            break

    # Post-check: fix any remaining consecutive violations via swapping.
    result = _fix_consecutive_violations(result, max_consecutive_same_category)

    return result


def _fix_consecutive_violations(
    cards: list[T],
    max_consecutive: int,
) -> list[T]:
    """Scan for runs exceeding max_consecutive and swap to fix them.

    Uses a greedy approach: when a run exceeds the limit, find the best
    position to insert a separator card from a different category.

    Mutates and returns the same list object (caller already created a new list).
    """
    n = len(cards)
    if n <= max_consecutive:
        return cards

    # Multiple passes to resolve violations that swaps may introduce.
    max_passes = n  # Safety bound to prevent infinite loops.
    for _ in range(max_passes):
        violation_found = False
        i = 0
        while i < n:
            run_start = i
            current_cat = cards[i].category
            while i < n and cards[i].category == current_cat:
                i += 1
            run_length = i - run_start

            if run_length > max_consecutive:
                violation_found = True
                # Insert a separator at position run_start + max_consecutive.
                insert_pos = run_start + max_consecutive
                swap_idx = _find_swap_candidate(
                    cards, insert_pos, current_cat, max_consecutive
                )
                if swap_idx is not None:
                    cards[insert_pos], cards[swap_idx] = (
                        cards[swap_idx],
                        cards[insert_pos],
                    )
                    # Restart scanning from the swap point.
                    i = insert_pos + 1
                else:
                    # No valid swap found — skip this run (constraint unsatisfiable
                    # for this sub-sequence).
                    pass

        if not violation_found:
            break

    return cards


def _find_swap_candidate(
    cards: list[T],
    pos: int,
    avoid_category: str,
    max_consecutive: int,
) -> int | None:
    """Find the best card with a different category to swap into `pos`.

    Searches forward first (prefer later cards to avoid disturbing earlier
    settled positions), then backward.

    A candidate is valid if placing the card currently at `pos` (which has
    `avoid_category`) at the candidate's position would not create a new
    violation there.
    """
    n = len(cards)

    # Search forward.
    for j in range(pos + 1, n):
        if cards[j].category != avoid_category:
            if _swap_is_safe(cards, pos, j, avoid_category, max_consecutive):
                return j

    # Search backward.
    for j in range(pos - 1, -1, -1):
        if cards[j].category != avoid_category:
            if _swap_is_safe(cards, pos, j, avoid_category, max_consecutive):
                return j

    return None


def _swap_is_safe(
    cards: list[T],
    pos_a: int,
    pos_b: int,
    moving_cat: str,
    max_consecutive: int,
) -> bool:
    """Check that swapping cards[pos_a] and cards[pos_b] won't create a new violation at pos_b.

    We check whether placing a card of `moving_cat` at pos_b would create a
    run exceeding max_consecutive at that location.
    """
    n = len(cards)

    # Count how many consecutive cards of `moving_cat` would surround pos_b
    # if we placed `moving_cat` there.
    count = 1  # the card itself

    # Look left of pos_b.
    j = pos_b - 1
    while j >= 0 and j != pos_a and cards[j].category == moving_cat:
        count += 1
        j -= 1

    # Look right of pos_b.
    j = pos_b + 1
    while j < n and j != pos_a and cards[j].category == moving_cat:
        count += 1
        j += 1

    return count <= max_consecutive
