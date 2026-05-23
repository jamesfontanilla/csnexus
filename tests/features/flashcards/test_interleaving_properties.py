"""Property-based tests for the interleaving algorithm.

**Validates: Requirements 9.1, 9.2**

Uses Hypothesis to verify universal properties of interleave_cards across
randomly generated inputs.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from hypothesis import given, settings
from hypothesis.strategies import integers, lists, sampled_from

from app.features.flashcards.algorithms.interleaving import interleave_cards


# ---------------------------------------------------------------------------
# Test infrastructure
# ---------------------------------------------------------------------------

CATEGORIES = ["verbal", "numerical", "analytical"]


@dataclass
class FakeCard:
    """Minimal card object satisfying the HasCategory protocol."""

    id: int
    category: str


def _fake_cards_strategy():
    """Strategy that generates lists of FakeCards with unique IDs."""
    return lists(
        sampled_from(CATEGORIES),
        min_size=0,
        max_size=50,
    ).map(lambda cats: [FakeCard(id=i, category=c) for i, c in enumerate(cats)])


# ---------------------------------------------------------------------------
# Property 12: Interleaving constraint
# ---------------------------------------------------------------------------


class TestInterleavingProperties:
    """Property-based tests for interleave_cards."""

    @given(
        cards=_fake_cards_strategy(),
        max_consecutive=integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_output_length_equals_input_length(
        self, cards: list[FakeCard], max_consecutive: int
    ) -> None:
        """No cards are lost or duplicated — output length matches input."""
        result = interleave_cards(cards, max_consecutive_same_category=max_consecutive)
        assert len(result) == len(cards)

    @given(
        cards=_fake_cards_strategy(),
        max_consecutive=integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_output_contains_same_elements_as_input(
        self, cards: list[FakeCard], max_consecutive: int
    ) -> None:
        """Output contains exactly the same elements as input (set equality by id)."""
        result = interleave_cards(cards, max_consecutive_same_category=max_consecutive)
        assert sorted(c.id for c in result) == sorted(c.id for c in cards)

    @given(
        cards=_fake_cards_strategy(),
        max_consecutive=integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_no_consecutive_violation(
        self, cards: list[FakeCard], max_consecutive: int
    ) -> None:
        """No more than max_consecutive consecutive cards share the same category.

        The constraint is unsatisfiable when:
        - All cards belong to the same category (only 1 distinct category), OR
        - The largest category group is too large relative to the other cards
          and max_consecutive. Specifically, if the largest group has more than
          max_consecutive * (other_cards + 1) cards, there aren't enough
          "separator" cards from other categories to break up the runs.

        In these cases the algorithm does its best but cannot guarantee the
        constraint, so we skip the assertion.
        """
        result = interleave_cards(cards, max_consecutive_same_category=max_consecutive)

        distinct_categories = set(c.category for c in cards)
        if len(distinct_categories) <= 1:
            # Only one category — constraint is trivially unsatisfiable
            return

        # Check if the constraint is mathematically satisfiable.
        # With `other_cards` cards from other categories acting as separators,
        # we can create at most (other_cards + 1) slots for the dominant category.
        # Each slot holds at most max_consecutive cards.
        category_counts = Counter(c.category for c in cards)
        max_group_size = max(category_counts.values())
        other_cards = len(cards) - max_group_size
        max_satisfiable = max_consecutive * (other_cards + 1)

        if max_group_size > max_satisfiable:
            # Constraint is unsatisfiable given the distribution — skip
            return

        # Scan for runs exceeding max_consecutive
        if not result:
            return

        run_length = 1
        for i in range(1, len(result)):
            if result[i].category == result[i - 1].category:
                run_length += 1
            else:
                run_length = 1
            assert run_length <= max_consecutive, (
                f"Run of {run_length} consecutive '{result[i].category}' cards "
                f"exceeds max_consecutive={max_consecutive} at index {i}"
            )

    @given(
        cards=_fake_cards_strategy(),
        max_consecutive=integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_category_counts_preserved(
        self, cards: list[FakeCard], max_consecutive: int
    ) -> None:
        """Category counts are preserved (proportional representation)."""
        result = interleave_cards(cards, max_consecutive_same_category=max_consecutive)
        input_counts = Counter(c.category for c in cards)
        output_counts = Counter(c.category for c in result)
        assert input_counts == output_counts

    @given(
        cards=_fake_cards_strategy(),
        max_consecutive=integers(min_value=1, max_value=10),
    )
    @settings(max_examples=100)
    def test_input_list_not_modified(
        self, cards: list[FakeCard], max_consecutive: int
    ) -> None:
        """Input list is not modified (pure function)."""
        original_ids = [c.id for c in cards]
        original_categories = [c.category for c in cards]
        interleave_cards(cards, max_consecutive_same_category=max_consecutive)
        assert [c.id for c in cards] == original_ids
        assert [c.category for c in cards] == original_categories

    @given(max_consecutive=integers(min_value=1, max_value=10))
    @settings(max_examples=100)
    def test_empty_input_returns_empty_output(self, max_consecutive: int) -> None:
        """Empty input returns empty output."""
        result = interleave_cards([], max_consecutive_same_category=max_consecutive)
        assert result == []
