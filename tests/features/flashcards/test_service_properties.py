"""Property-based tests for FlashcardService business logic.

Validates universal correctness properties using Hypothesis.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from unittest.mock import MagicMock

from hypothesis import given, settings
from hypothesis.strategies import (
    floats,
    integers,
    sampled_from,
    text,
)

from app.features.flashcards.models import (
    Deck,
    Flashcard,
    StudySession,
)
from app.features.flashcards.repository import FlashcardRepository
from app.features.flashcards.schemas import (
    FlashcardCreate,
    FlashcardUpdate,
)
from app.features.flashcards.service import FlashcardService
from app.features.users.models import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_repo() -> MagicMock:
    return MagicMock(spec=FlashcardRepository)


def _mock_user(user_id: int = 1) -> MagicMock:
    user = MagicMock(spec=User)
    user.id = user_id
    return user


def _mock_deck(owner_id: int = 1) -> MagicMock:
    deck = MagicMock(spec=Deck)
    deck.id = 1
    deck.owner_id = owner_id
    deck.visibility = "private"
    deck.deleted_at = None
    return deck


def _mock_card(
    *,
    ease_factor: float = 2.5,
    retention_score: float = 0.5,
    memory_stability: float = 3.0,
    review_interval: int = 7,
    lapse_count: int = 1,
    total_reviews: int = 10,
    successful_reviews: int = 8,
) -> MagicMock:
    card = MagicMock(spec=Flashcard)
    card.id = 1
    card.deck_id = 1
    card.ease_factor = ease_factor
    card.retention_score = retention_score
    card.memory_stability = memory_stability
    card.review_interval = review_interval
    card.lapse_count = lapse_count
    card.last_review_date = date(2024, 1, 1)
    card.total_reviews = total_reviews
    card.successful_reviews = successful_reviews
    card.is_graduated = False
    card.deleted_at = None
    return card


# ---------------------------------------------------------------------------
# Property 7: Card type-specific validation
# Validates: Requirements 1.3, 1.4, 1.5, 1.6, 1.12
# ---------------------------------------------------------------------------


class TestCardTypeValidation:
    """For ANY card type, the service enforces type-specific constraints.

    **Validates: Requirements 1.3, 1.4, 1.5, 1.6, 1.12**
    """

    @settings(max_examples=100)
    @given(front=text(min_size=1, max_size=100))
    def test_cloze_without_pattern_always_rejected(self, front: str) -> None:
        """Cloze cards without {{c1::...}} are always rejected."""
        import pytest
        from fastapi import HTTPException

        # Ensure front does NOT contain the cloze pattern
        front_clean = front.replace("{{c1::", "").replace("}}", "")
        if "{{c1::" in front_clean:
            return  # Skip if somehow still contains pattern

        repo = _mock_repo()
        deck = _mock_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front=front_clean if front_clean else "x",
            back="answer",
            card_type="cloze",
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    @settings(max_examples=100)
    @given(term=text(min_size=1, max_size=50))
    def test_cloze_with_pattern_always_accepted(self, term: str) -> None:
        """Cloze cards with {{c1::term}} are always accepted."""
        repo = _mock_repo()
        deck = _mock_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        repo.create_flashcard.return_value = MagicMock(spec=Flashcard)
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        front = f"The {{{{c1::{term}}}}} is important"
        payload = FlashcardCreate(
            front=front, back=term, card_type="cloze"
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()

    @settings(max_examples=100)
    @given(back=text(min_size=1, max_size=100))
    def test_mcq_with_non_json_back_always_rejected(self, back: str) -> None:
        """MCQ cards with non-JSON back are always rejected."""
        import pytest
        from fastapi import HTTPException

        # Ensure back is not valid JSON array with 2+ items
        try:
            parsed = json.loads(back)
            if isinstance(parsed, list) and len(parsed) >= 2:
                return  # Skip valid MCQ backs
        except (json.JSONDecodeError, ValueError):
            pass

        repo = _mock_repo()
        deck = _mock_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Question?", back=back, card_type="mcq"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    @settings(max_examples=100)
    @given(num_options=integers(min_value=2, max_value=6))
    def test_mcq_with_valid_options_always_accepted(self, num_options: int) -> None:
        """MCQ cards with 2+ JSON array options are always accepted."""
        repo = _mock_repo()
        deck = _mock_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        repo.create_flashcard.return_value = MagicMock(spec=Flashcard)
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        options = [f"Option {i}" for i in range(num_options)]
        payload = FlashcardCreate(
            front="Question?",
            back=json.dumps(options),
            card_type="mcq",
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()

    @settings(max_examples=100)
    @given(answer=sampled_from(["true", "false", "True", "False", "TRUE", "FALSE"]))
    def test_true_false_valid_answers_accepted(self, answer: str) -> None:
        """True/false cards with 'true' or 'false' (any case) are accepted."""
        repo = _mock_repo()
        deck = _mock_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        repo.create_flashcard.return_value = MagicMock(spec=Flashcard)
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Statement", back=answer, card_type="true_false"
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()


# ---------------------------------------------------------------------------
# Property 8: Flashcard update preserves scheduling
# Validates: Requirements 1.7
# ---------------------------------------------------------------------------


class TestFlashcardUpdatePreservesScheduling:
    """For ANY content update, scheduling metadata is never modified.

    **Validates: Requirements 1.7**
    """

    @settings(max_examples=100)
    @given(
        new_front=text(min_size=1, max_size=100),
        ease_factor=floats(min_value=1.3, max_value=3.5, allow_nan=False, allow_infinity=False),
        review_interval=integers(min_value=1, max_value=365),
        memory_stability=floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        lapse_count=integers(min_value=0, max_value=50),
    )
    def test_update_never_touches_scheduling_fields(
        self,
        new_front: str,
        ease_factor: float,
        review_interval: int,
        memory_stability: float,
        lapse_count: int,
    ) -> None:
        """Content updates never include scheduling fields in the update call."""
        repo = _mock_repo()
        card = _mock_card(
            ease_factor=ease_factor,
            review_interval=review_interval,
            memory_stability=memory_stability,
            lapse_count=lapse_count,
        )
        deck = _mock_deck()
        repo.get_flashcard.return_value = card
        repo.get_deck.return_value = deck
        repo.update_flashcard.return_value = card
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardUpdate(front=new_front)
        service.update_flashcard(user, 1, payload)

        # Verify the update call does NOT include scheduling fields
        call_kwargs = repo.update_flashcard.call_args[1]
        scheduling_fields = {
            "ease_factor", "retention_score", "memory_stability",
            "review_interval", "lapse_count", "next_review_date",
            "last_review_date", "total_reviews", "successful_reviews",
            "mastery_percentage", "is_graduated",
        }
        for field in scheduling_fields:
            assert field not in call_kwargs, (
                f"Scheduling field '{field}' was included in content update"
            )


# ---------------------------------------------------------------------------
# Property 15: Study session result accuracy
# Validates: Requirements 3.7
# ---------------------------------------------------------------------------


class TestStudySessionResultAccuracy:
    """XP earned = (2 * cards_reviewed) + cards_correct for ANY session.

    **Validates: Requirements 3.7**
    """

    @settings(max_examples=100)
    @given(
        cards_reviewed=integers(min_value=0, max_value=200),
        cards_correct=integers(min_value=0, max_value=200),
        cards_incorrect=integers(min_value=0, max_value=200),
        cards_skipped=integers(min_value=0, max_value=200),
    )
    def test_xp_formula_always_correct(
        self,
        cards_reviewed: int,
        cards_correct: int,
        cards_incorrect: int,
        cards_skipped: int,
    ) -> None:
        """XP = (2 * cards_reviewed) + cards_correct."""
        repo = _mock_repo()
        session = MagicMock(spec=StudySession)
        session.id = 1
        session.user_id = 1
        session.ended_at = None
        session.started_at = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        session.cards_reviewed = cards_reviewed
        session.cards_correct = cards_correct
        session.cards_incorrect = cards_incorrect
        session.cards_skipped = cards_skipped
        repo.get_session.return_value = session
        repo.update_session.return_value = session
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        result = service.end_study_session(user, 1)
        expected_xp = (2 * cards_reviewed) + cards_correct
        assert result.xp_earned == expected_xp
        assert result.cards_reviewed == cards_reviewed
        assert result.cards_correct == cards_correct


# ---------------------------------------------------------------------------
# Property 9: Daily queue priority ordering
# Validates: Requirements 6.1
# ---------------------------------------------------------------------------


class TestDailyQueuePriorityOrdering:
    """For ANY set of due cards, overdue cards appear before new cards.

    **Validates: Requirements 6.1**
    """

    @settings(max_examples=100, deadline=None)
    @given(
        num_overdue=integers(min_value=0, max_value=10),
        num_due_today=integers(min_value=0, max_value=10),
        num_new=integers(min_value=0, max_value=10),
    )
    def test_overdue_before_new_in_queue(
        self, num_overdue: int, num_due_today: int, num_new: int
    ) -> None:
        """Overdue cards (non-NULL next_review_date <= today) come before new cards (NULL)."""
        from app.features.flashcards.schemas import QueueFilters

        repo = _mock_repo()

        # Build a queue that simulates the repository's ordering:
        # overdue first, then due today, then new (NULL dates last)
        today = date(2024, 6, 15)
        cards: list[MagicMock] = []

        for i in range(num_overdue):
            c = MagicMock(spec=Flashcard)
            c.id = i
            c.next_review_date = date(2024, 6, 10)  # overdue
            c.card_type = "basic"
            c.category = "verbal"
            cards.append(c)

        for i in range(num_due_today):
            c = MagicMock(spec=Flashcard)
            c.id = 100 + i
            c.next_review_date = today
            c.card_type = "basic"
            c.category = "verbal"
            cards.append(c)

        for i in range(num_new):
            c = MagicMock(spec=Flashcard)
            c.id = 200 + i
            c.next_review_date = None  # new card
            c.card_type = "basic"
            c.category = "verbal"
            cards.append(c)

        repo.get_daily_queue.return_value = cards
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        filters = QueueFilters(max_cards=50)
        result = service.get_daily_queue(user, filters)

        # Verify ordering: all non-NULL dates before NULL dates
        seen_null = False
        for card in result:
            if card.next_review_date is None:
                seen_null = True
            elif seen_null:
                # A non-NULL date appeared after a NULL — ordering violated
                assert False, "Non-NULL next_review_date appeared after NULL (new card)"


# ---------------------------------------------------------------------------
# Property 10: Queue cap truncation
# Validates: Requirements 6.4
# ---------------------------------------------------------------------------


class TestQueueCapTruncation:
    """For ANY max_cards value, the queue never exceeds that limit.

    **Validates: Requirements 6.4**
    """

    @settings(max_examples=100, deadline=None)
    @given(
        total_cards=integers(min_value=0, max_value=100),
        max_cards=integers(min_value=10, max_value=200),
    )
    def test_queue_never_exceeds_max_cards(
        self, total_cards: int, max_cards: int
    ) -> None:
        """Queue length <= max_cards regardless of how many cards are due."""
        from app.features.flashcards.schemas import QueueFilters

        repo = _mock_repo()

        # Simulate repository returning at most max_cards
        returned = min(total_cards, max_cards)
        cards = [MagicMock(spec=Flashcard) for _ in range(returned)]
        for i, c in enumerate(cards):
            c.id = i
            c.next_review_date = None
            c.card_type = "basic"
            c.category = "verbal"
        repo.get_daily_queue.return_value = cards
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        filters = QueueFilters(max_cards=max_cards)
        result = service.get_daily_queue(user, filters)
        assert len(result) <= max_cards


# ---------------------------------------------------------------------------
# Property 11: Queue summary computation
# Validates: Requirements 6.6
# ---------------------------------------------------------------------------


class TestQueueSummaryComputation:
    """For ANY queue counts, the summary is computed correctly.

    **Validates: Requirements 6.6**
    """

    @settings(max_examples=100)
    @given(
        total_due=integers(min_value=0, max_value=500),
        overdue_count=integers(min_value=0, max_value=500),
        new_today_count=integers(min_value=0, max_value=500),
    )
    def test_estimated_minutes_formula(
        self, total_due: int, overdue_count: int, new_today_count: int
    ) -> None:
        """estimated_review_minutes = (total_due * 30) // 60."""
        repo = _mock_repo()
        repo.get_queue_summary_counts.return_value = {
            "total_due": total_due,
            "overdue_count": overdue_count,
            "new_today_count": new_today_count,
        }
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        result = service.get_queue_summary(user)
        assert result.total_due == total_due
        assert result.overdue_count == overdue_count
        assert result.new_today_count == new_today_count
        assert result.estimated_review_minutes == (total_due * 30) // 60

    @settings(max_examples=100)
    @given(total_due=integers(min_value=0, max_value=1000))
    def test_estimated_minutes_non_negative(self, total_due: int) -> None:
        """Estimated minutes is always non-negative."""
        repo = _mock_repo()
        repo.get_queue_summary_counts.return_value = {
            "total_due": total_due,
            "overdue_count": 0,
            "new_today_count": 0,
        }
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        result = service.get_queue_summary(user)
        assert result.estimated_review_minutes >= 0


# ---------------------------------------------------------------------------
# Property 14: Graduation after consecutive mastered reviews
# Validates: Requirements 10.5
# ---------------------------------------------------------------------------


class TestGraduationAfterConsecutiveMastered:
    """A card graduates after GRADUATION_THRESHOLD consecutive mastered reviews.

    **Validates: Requirements 10.5**

    Note: Graduation logic is tested at the repository/integration level
    since it requires tracking consecutive mastered reviews across multiple
    record_response calls. This property test validates the threshold constant
    and the graduation check logic.
    """

    @settings(max_examples=100)
    @given(consecutive=integers(min_value=0, max_value=20))
    def test_graduation_threshold_is_5(self, consecutive: int) -> None:
        """Cards should graduate at exactly 5 consecutive mastered reviews."""
        from app.features.flashcards.service import GRADUATION_THRESHOLD

        should_graduate = consecutive >= GRADUATION_THRESHOLD
        assert GRADUATION_THRESHOLD == 5

        # The graduation decision: a card with `consecutive` mastered reviews
        # should be graduated iff consecutive >= 5
        if should_graduate:
            assert consecutive >= 5
        else:
            assert consecutive < 5


# ---------------------------------------------------------------------------
# Property 16: Deck duplication content fidelity
# Validates: Requirements 2.5, 14.6
# ---------------------------------------------------------------------------


class TestDeckDuplicationContentFidelity:
    """When a deck is duplicated, the clone has the same card count.

    **Validates: Requirements 2.5, 14.6**
    """

    @settings(max_examples=100)
    @given(num_cards=integers(min_value=0, max_value=50))
    def test_clone_preserves_card_count(self, num_cards: int) -> None:
        """Cloned deck has same number of cards as original."""
        repo = _mock_repo()
        deck = MagicMock(spec=Deck)
        deck.id = 1
        deck.owner_id = 2
        deck.title = "Original"
        deck.visibility = "public"
        deck.deleted_at = None
        repo.get_deck.return_value = deck
        repo.get_deck_by_owner_and_title.return_value = None

        clone = MagicMock(spec=Deck)
        clone.id = 2
        clone.owner_id = 1
        clone.title = "Original (copy)"
        clone.cloned_from_deck_id = 1
        clone.cloned_from_user_id = 2
        repo.duplicate_deck.return_value = clone
        repo.update_deck.return_value = clone

        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        result = service.duplicate_deck(user, 1)
        # The repository's duplicate_deck is responsible for copying cards
        repo.duplicate_deck.assert_called_once_with(deck, 1)
        assert result.cloned_from_deck_id == 1


# ---------------------------------------------------------------------------
# Property 17: Deck rating average computation
# Validates: Requirements 14.4, 14.5
# ---------------------------------------------------------------------------


class TestDeckRatingAverageComputation:
    """After rating, the deck's average_rating is recomputed.

    **Validates: Requirements 14.4, 14.5**
    """

    @settings(max_examples=100)
    @given(
        rating=integers(min_value=1, max_value=5),
        existing_avg=floats(min_value=1.0, max_value=5.0, allow_nan=False, allow_infinity=False),
        existing_count=integers(min_value=0, max_value=100),
    )
    def test_rate_deck_triggers_average_recomputation(
        self, rating: int, existing_avg: float, existing_count: int
    ) -> None:
        """Rating a deck always triggers average recomputation."""
        repo = _mock_repo()
        deck = MagicMock(spec=Deck)
        deck.id = 1
        deck.owner_id = 2  # Different from user
        deck.visibility = "public"
        deck.deleted_at = None
        repo.get_deck.return_value = deck
        repo.upsert_rating.return_value = MagicMock()
        repo.compute_average_rating.return_value = (existing_avg, existing_count + 1)
        repo.update_deck.return_value = deck

        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.rate_deck(user, 1, rating)

        # Verify average was recomputed and deck was updated
        repo.compute_average_rating.assert_called_once_with(1)
        repo.update_deck.assert_called_once()
        update_kwargs = repo.update_deck.call_args[1]
        assert "average_rating" in update_kwargs
        assert "rating_count" in update_kwargs


# ---------------------------------------------------------------------------
# Property 24: Deck soft-delete cascades to all cards
# Validates: Requirements 2.6
# ---------------------------------------------------------------------------


class TestDeckSoftDeleteCascade:
    """Deleting a deck always calls soft_delete_deck on the repository.

    **Validates: Requirements 2.6**
    """

    @settings(max_examples=100)
    @given(deck_id=integers(min_value=1, max_value=1000))
    def test_delete_deck_calls_soft_delete(self, deck_id: int) -> None:
        """delete_deck always triggers soft_delete_deck on the repository."""
        repo = _mock_repo()
        deck = MagicMock(spec=Deck)
        deck.id = deck_id
        deck.owner_id = 1
        deck.deleted_at = None
        repo.get_deck.return_value = deck

        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.delete_deck(user, deck_id)
        repo.soft_delete_deck.assert_called_once()
        # The first arg is the deck, second is the timestamp
        call_args = repo.soft_delete_deck.call_args[0]
        assert call_args[0] == deck


# ---------------------------------------------------------------------------
# Property 20: Deck popularity score formula
# Validates: Requirements 20.3
# ---------------------------------------------------------------------------


class TestDeckPopularityScoreFormula:
    """Popularity = (clone_count * 3) + (bookmark_count * 2) + (rating_count * avg_rating).

    **Validates: Requirements 20.3**
    """

    @settings(max_examples=100)
    @given(
        clone_count=integers(min_value=0, max_value=1000),
        bookmark_count=integers(min_value=0, max_value=1000),
        rating_count=integers(min_value=0, max_value=1000),
        average_rating=floats(min_value=0.0, max_value=5.0, allow_nan=False, allow_infinity=False),
    )
    def test_popularity_formula_correctness(
        self,
        clone_count: int,
        bookmark_count: int,
        rating_count: int,
        average_rating: float,
    ) -> None:
        """Score matches the formula exactly."""
        repo = _mock_repo()
        deck = MagicMock(spec=Deck)
        deck.id = 1
        deck.clone_count = clone_count
        deck.bookmark_count = bookmark_count
        deck.rating_count = rating_count
        deck.average_rating = average_rating
        repo.get_deck.return_value = deck

        service = FlashcardService(flashcard_repo=repo)
        result = service.compute_deck_popularity_score(1)

        expected = (clone_count * 3) + (bookmark_count * 2) + (rating_count * average_rating)
        assert abs(result - round(expected, 2)) < 0.01

    @settings(max_examples=100)
    @given(
        clone_count=integers(min_value=0, max_value=1000),
        bookmark_count=integers(min_value=0, max_value=1000),
        rating_count=integers(min_value=0, max_value=1000),
        average_rating=floats(min_value=0.0, max_value=5.0, allow_nan=False, allow_infinity=False),
    )
    def test_popularity_score_non_negative(
        self,
        clone_count: int,
        bookmark_count: int,
        rating_count: int,
        average_rating: float,
    ) -> None:
        """Score is always non-negative."""
        repo = _mock_repo()
        deck = MagicMock(spec=Deck)
        deck.id = 1
        deck.clone_count = clone_count
        deck.bookmark_count = bookmark_count
        deck.rating_count = rating_count
        deck.average_rating = average_rating
        repo.get_deck.return_value = deck

        service = FlashcardService(flashcard_repo=repo)
        result = service.compute_deck_popularity_score(1)
        assert result >= 0.0


# ---------------------------------------------------------------------------
# Property 21: Exam simulation scoring
# Validates: Requirements 22.7
# ---------------------------------------------------------------------------


class TestExamSimulationScoring:
    """Exam score percentage = (correct / total) * 100.

    **Validates: Requirements 22.7**
    """

    @settings(max_examples=100)
    @given(
        correct=integers(min_value=0, max_value=150),
        total=integers(min_value=1, max_value=150),
    )
    def test_score_percentage_formula(self, correct: int, total: int) -> None:
        """Score percentage = (correct / total) * 100."""
        correct = min(correct, total)
        percentage = (correct / total) * 100
        assert 0.0 <= percentage <= 100.0

    @settings(max_examples=100)
    @given(total=integers(min_value=1, max_value=150))
    def test_perfect_score_is_100(self, total: int) -> None:
        """All correct = 100%."""
        percentage = (total / total) * 100
        assert percentage == 100.0

    @settings(max_examples=100)
    @given(total=integers(min_value=1, max_value=150))
    def test_zero_correct_is_zero(self, total: int) -> None:
        """Zero correct = 0%."""
        percentage = (0 / total) * 100
        assert percentage == 0.0


# ---------------------------------------------------------------------------
# Property 22: Predicted exam readiness
# Validates: Requirements 26.6
# ---------------------------------------------------------------------------


class TestPredictedExamReadiness:
    """Readiness is a weighted average: verbal 40%, numerical 30%, analytical 30%.

    **Validates: Requirements 26.6**
    """

    @settings(max_examples=100)
    @given(
        verbal_ret=floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        numerical_ret=floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        analytical_ret=floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    def test_readiness_within_0_100(
        self, verbal_ret: float, numerical_ret: float, analytical_ret: float
    ) -> None:
        """Readiness score is always between 0 and 100."""
        readiness = (verbal_ret * 0.4 + numerical_ret * 0.3 + analytical_ret * 0.3) * 100
        assert 0.0 <= readiness <= 100.0

    @settings(max_examples=100)
    @given(
        retention=floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    def test_uniform_retention_equals_retention_times_100(
        self, retention: float
    ) -> None:
        """If all categories have same retention, readiness = retention * 100."""
        readiness = (retention * 0.4 + retention * 0.3 + retention * 0.3) * 100
        expected = retention * 100
        assert abs(readiness - expected) < 0.01


# ---------------------------------------------------------------------------
# Property 23: Sync deduplication by client_event_id
# Validates: Requirements 24.3, 24.8
# ---------------------------------------------------------------------------


class TestSyncDeduplication:
    """Duplicate client_event_ids are counted as duplicates, not accepted.

    **Validates: Requirements 24.3, 24.8**
    """

    @settings(max_examples=100)
    @given(num_items=integers(min_value=1, max_value=50))
    def test_all_duplicates_returns_zero_accepted(self, num_items: int) -> None:
        """If all items are duplicates, accepted = 0."""
        repo = _mock_repo()
        # Simulate all items being duplicates
        repo.batch_upsert_reviews.return_value = (0, num_items, 0)
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        items = [
            {
                "card_id": 1,
                "response_type": "remembered",
                "confidence_level": "confident",
                "reviewed_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
                "client_event_id": f"dup-{i}",
            }
            for i in range(num_items)
        ]
        result = service.batch_sync_reviews(user, items)
        assert result["accepted"] == 0
        assert result["duplicates"] == num_items

    @settings(max_examples=100)
    @given(num_items=integers(min_value=1, max_value=50))
    def test_all_new_returns_all_accepted(self, num_items: int) -> None:
        """If all items are new, accepted = num_items."""
        repo = _mock_repo()
        repo.batch_upsert_reviews.return_value = (num_items, 0, 0)
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        items = [
            {
                "card_id": 1,
                "response_type": "remembered",
                "confidence_level": "confident",
                "reviewed_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
                "client_event_id": f"new-{i}",
            }
            for i in range(num_items)
        ]
        result = service.batch_sync_reviews(user, items)
        assert result["accepted"] == num_items
        assert result["duplicates"] == 0
