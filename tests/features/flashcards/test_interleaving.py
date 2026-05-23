"""Unit tests for the interleaving algorithm."""

from __future__ import annotations

from dataclasses import dataclass


from app.features.flashcards.algorithms.interleaving import interleave_cards


@dataclass
class FakeCard:
    """Minimal card object with a category attribute."""

    id: int
    category: str


def _make_cards(categories: list[str]) -> list[FakeCard]:
    """Build a list of FakeCard objects from category strings."""
    return [FakeCard(id=i, category=cat) for i, cat in enumerate(categories)]


class TestInterleaveCards:
    """Tests for interleave_cards."""

    def test_empty_list_returns_empty(self) -> None:
        result = interleave_cards([])
        assert result == []

    def test_single_card_returns_copy(self) -> None:
        cards = _make_cards(["verbal"])
        result = interleave_cards(cards)
        assert len(result) == 1
        assert result[0].category == "verbal"

    def test_does_not_modify_input(self) -> None:
        cards = _make_cards(["verbal"] * 5 + ["numerical"] * 5)
        original_order = [c.id for c in cards]
        interleave_cards(cards)
        assert [c.id for c in cards] == original_order

    def test_returns_new_list(self) -> None:
        cards = _make_cards(["verbal", "numerical"])
        result = interleave_cards(cards)
        assert result is not cards

    def test_all_same_category_returns_as_is(self) -> None:
        cards = _make_cards(["verbal"] * 10)
        result = interleave_cards(cards)
        assert len(result) == 10
        assert all(c.category == "verbal" for c in result)

    def test_two_categories_no_violation(self) -> None:
        cards = _make_cards(["verbal"] * 6 + ["numerical"] * 6)
        result = interleave_cards(cards, max_consecutive_same_category=3)
        assert len(result) == 12
        # Check no more than 3 consecutive same category
        for i in range(len(result) - 3):
            window = [result[j].category for j in range(i, i + 4)]
            assert len(set(window)) > 1, f"Violation at index {i}: {window}"

    def test_three_categories_interleaved(self) -> None:
        cards = _make_cards(
            ["verbal"] * 4 + ["numerical"] * 4 + ["analytical"] * 4
        )
        result = interleave_cards(cards, max_consecutive_same_category=3)
        assert len(result) == 12
        for i in range(len(result) - 3):
            window = [result[j].category for j in range(i, i + 4)]
            assert len(set(window)) > 1

    def test_preserves_all_cards(self) -> None:
        cards = _make_cards(["verbal"] * 5 + ["numerical"] * 3 + ["analytical"] * 2)
        result = interleave_cards(cards)
        assert sorted(c.id for c in result) == sorted(c.id for c in cards)

    def test_proportional_representation(self) -> None:
        cards = _make_cards(["verbal"] * 7 + ["numerical"] * 2 + ["analytical"] * 1)
        result = interleave_cards(cards)
        cat_counts = {}
        for c in result:
            cat_counts[c.category] = cat_counts.get(c.category, 0) + 1
        assert cat_counts["verbal"] == 7
        assert cat_counts["numerical"] == 2
        assert cat_counts["analytical"] == 1

    def test_custom_max_consecutive(self) -> None:
        cards = _make_cards(["verbal"] * 10 + ["numerical"] * 2)
        result = interleave_cards(cards, max_consecutive_same_category=5)
        assert len(result) == 12
        for i in range(len(result) - 5):
            window = [result[j].category for j in range(i, i + 6)]
            assert len(set(window)) > 1, f"Violation at index {i}: {window}"

    def test_max_consecutive_of_1(self) -> None:
        # With max_consecutive=1, alternation is required.
        # Only possible if no category has more than ceil(n/2) cards.
        cards = _make_cards(["verbal"] * 3 + ["numerical"] * 3)
        result = interleave_cards(cards, max_consecutive_same_category=1)
        for i in range(len(result) - 1):
            assert result[i].category != result[i + 1].category

    def test_heavily_skewed_distribution(self) -> None:
        # 8 verbal, 1 numerical, 1 analytical — constraint may be tight
        cards = _make_cards(["verbal"] * 8 + ["numerical"] * 1 + ["analytical"] * 1)
        result = interleave_cards(cards, max_consecutive_same_category=3)
        assert len(result) == 10
        # Verify constraint
        for i in range(len(result) - 3):
            window = [result[j].category for j in range(i, i + 4)]
            assert len(set(window)) > 1, f"Violation at index {i}: {window}"
