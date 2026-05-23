"""Service layer tests for the flashcard feature (Task 6.1).

Per testing-standards.md: mocked repository, no DB access.
Tests business logic in isolation using MagicMock(spec=FlashcardRepository).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.flashcards.models import (
    Deck,
    Flashcard,
    StudySession,
)
from app.features.flashcards.repository import FlashcardRepository
from app.features.flashcards.schemas import (
    CardResponse,
    DeckCreate,
    DeckUpdate,
    FlashcardCreate,
    FlashcardUpdate,
    StudySessionStart,
)
from app.features.flashcards.service import FlashcardService, MAX_CARDS_PER_DECK
from app.features.users.models import User


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _mock_repo() -> MagicMock:
    return MagicMock(spec=FlashcardRepository)


def _mock_user(user_id: int = 1) -> MagicMock:
    user = MagicMock(spec=User)
    user.id = user_id
    return user


def _make_deck(
    deck_id: int = 1,
    owner_id: int = 1,
    title: str = "Test Deck",
    category: str = "verbal",
    visibility: str = "private",
) -> MagicMock:
    deck = MagicMock(spec=Deck)
    deck.id = deck_id
    deck.owner_id = owner_id
    deck.title = title
    deck.category = category
    deck.visibility = visibility
    deck.deleted_at = None
    deck.clone_count = 0
    return deck


def _make_card(
    card_id: int = 1,
    deck_id: int = 1,
    front: str = "Q",
    back: str = "A",
    card_type: str = "basic",
) -> MagicMock:
    card = MagicMock(spec=Flashcard)
    card.id = card_id
    card.deck_id = deck_id
    card.front = front
    card.back = back
    card.card_type = card_type
    card.ease_factor = 2.5
    card.retention_score = 0.0
    card.memory_stability = 1.0
    card.review_interval = 1
    card.lapse_count = 0
    card.last_review_date = None
    card.total_reviews = 0
    card.successful_reviews = 0
    card.is_graduated = False
    card.deleted_at = None
    return card


# ---------------------------------------------------------------------------
# Deck CRUD Tests
# ---------------------------------------------------------------------------


class TestCreateDeck:
    def test_creates_deck_successfully(self) -> None:
        repo = _mock_repo()
        repo.get_deck_by_owner_and_title.return_value = None
        repo.create_deck.return_value = _make_deck()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = DeckCreate(
            title="Test Deck", category="verbal", visibility="private"
        )
        result = service.create_deck(user, payload)

        assert result is not None
        repo.create_deck.assert_called_once()

    def test_raises_409_on_duplicate_title(self) -> None:
        repo = _mock_repo()
        repo.get_deck_by_owner_and_title.return_value = _make_deck()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = DeckCreate(
            title="Test Deck", category="verbal", visibility="private"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_deck(user, payload)
        assert exc_info.value.status_code == 409


class TestUpdateDeck:
    def test_updates_deck_successfully(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.update_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = DeckUpdate(description="Updated description")
        service.update_deck(user, 1, payload)
        repo.update_deck.assert_called_once()

    def test_raises_404_when_deck_not_found(self) -> None:
        repo = _mock_repo()
        repo.get_deck.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = DeckUpdate(description="Updated")
        with pytest.raises(HTTPException) as exc_info:
            service.update_deck(user, 999, payload)
        assert exc_info.value.status_code == 404

    def test_raises_403_when_not_owner(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(owner_id=2)
        repo.get_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        payload = DeckUpdate(description="Hacked")
        with pytest.raises(HTTPException) as exc_info:
            service.update_deck(user, 1, payload)
        assert exc_info.value.status_code == 403

    def test_raises_409_on_title_conflict(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(title="Original")
        repo.get_deck.return_value = deck
        repo.get_deck_by_owner_and_title.return_value = _make_deck(title="Taken")
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = DeckUpdate(title="Taken")
        with pytest.raises(HTTPException) as exc_info:
            service.update_deck(user, 1, payload)
        assert exc_info.value.status_code == 409


class TestDeleteDeck:
    def test_soft_deletes_deck(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        service.delete_deck(user, 1)
        repo.soft_delete_deck.assert_called_once()

    def test_raises_404_when_not_found(self) -> None:
        repo = _mock_repo()
        repo.get_deck.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.delete_deck(user, 999)
        assert exc_info.value.status_code == 404


class TestDuplicateDeck:
    def test_duplicates_public_deck(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(owner_id=2, visibility="public")
        repo.get_deck.return_value = deck
        repo.get_deck_by_owner_and_title.return_value = None
        clone = _make_deck(deck_id=2, owner_id=1)
        repo.duplicate_deck.return_value = clone
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.duplicate_deck(user, 1)
        repo.duplicate_deck.assert_called_once()

    def test_raises_404_for_private_deck_of_other_user(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(owner_id=2, visibility="private")
        repo.get_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        with pytest.raises(HTTPException) as exc_info:
            service.duplicate_deck(user, 1)
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Flashcard CRUD Tests
# ---------------------------------------------------------------------------


class TestCreateFlashcard:
    def test_creates_basic_card(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 10
        repo.create_flashcard.return_value = _make_card()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="What is X?", back="X is Y.", card_type="basic"
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()

    def test_raises_422_when_deck_at_capacity(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = MAX_CARDS_PER_DECK
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Q", back="A", card_type="basic"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    def test_raises_422_for_cloze_without_pattern(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="No cloze pattern here", back="Answer", card_type="cloze"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    def test_accepts_valid_cloze_card(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        repo.create_flashcard.return_value = _make_card(card_type="cloze")
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="The {{c1::sun}} rises in the east",
            back="sun",
            card_type="cloze",
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()

    def test_raises_422_for_mcq_with_invalid_back(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Which is correct?",
            back="not json",
            card_type="mcq",
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    def test_accepts_valid_mcq_card(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        repo.create_flashcard.return_value = _make_card(card_type="mcq")
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Which is correct?",
            back=json.dumps(["A", "B", "C"]),
            card_type="mcq",
        )
        service.create_flashcard(user, 1, payload)
        repo.create_flashcard.assert_called_once()

    def test_raises_422_for_true_false_invalid(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="The sky is blue", back="maybe", card_type="true_false"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422

    def test_raises_422_for_sequence_invalid(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        repo.count_deck_flashcards.return_value = 0
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardCreate(
            front="Order these",
            back=json.dumps(["only one"]),
            card_type="sequence",
        )
        with pytest.raises(HTTPException) as exc_info:
            service.create_flashcard(user, 1, payload)
        assert exc_info.value.status_code == 422


class TestUpdateFlashcard:
    def test_updates_card_preserving_scheduling(self) -> None:
        repo = _mock_repo()
        card = _make_card()
        deck = _make_deck()
        repo.get_flashcard.return_value = card
        repo.get_deck.return_value = deck
        repo.update_flashcard.return_value = card
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardUpdate(front="Updated question")
        service.update_flashcard(user, 1, payload)

        # Verify only content fields are passed, not scheduling
        call_kwargs = repo.update_flashcard.call_args[1]
        assert "front" in call_kwargs
        assert "ease_factor" not in call_kwargs
        assert "review_interval" not in call_kwargs

    def test_raises_404_when_card_not_found(self) -> None:
        repo = _mock_repo()
        repo.get_flashcard.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = FlashcardUpdate(front="Updated")
        with pytest.raises(HTTPException) as exc_info:
            service.update_flashcard(user, 999, payload)
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Study Session Tests
# ---------------------------------------------------------------------------


class TestStartStudySession:
    def test_starts_session_successfully(self) -> None:
        repo = _mock_repo()
        deck = _make_deck()
        repo.get_deck.return_value = deck
        session = MagicMock(spec=StudySession)
        session.id = 1
        repo.create_session.return_value = session
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = StudySessionStart(
            study_mode="swipe", deck_ids=[1]
        )
        service.start_study_session(user, payload)
        repo.create_session.assert_called_once()

    def test_raises_404_for_nonexistent_deck(self) -> None:
        repo = _mock_repo()
        repo.get_deck.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = StudySessionStart(
            study_mode="swipe", deck_ids=[999]
        )
        with pytest.raises(HTTPException) as exc_info:
            service.start_study_session(user, payload)
        assert exc_info.value.status_code == 404


class TestEndStudySession:
    def test_ends_session_with_summary(self) -> None:
        repo = _mock_repo()
        session = MagicMock(spec=StudySession)
        session.id = 1
        session.user_id = 1
        session.ended_at = None
        session.started_at = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        session.cards_reviewed = 10
        session.cards_correct = 7
        session.cards_incorrect = 2
        session.cards_skipped = 1
        repo.get_session.return_value = session
        repo.update_session.return_value = session
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        result = service.end_study_session(user, 1)
        assert result.cards_reviewed == 10
        assert result.cards_correct == 7
        assert result.xp_earned == (2 * 10) + 7  # 27

    def test_raises_404_when_session_not_found(self) -> None:
        repo = _mock_repo()
        repo.get_session.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.end_study_session(user, 999)
        assert exc_info.value.status_code == 404

    def test_raises_409_when_already_ended(self) -> None:
        repo = _mock_repo()
        session = MagicMock(spec=StudySession)
        session.user_id = 1
        session.ended_at = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        repo.get_session.return_value = session
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.end_study_session(user, 1)
        assert exc_info.value.status_code == 409


# ---------------------------------------------------------------------------
# Record Response Tests
# ---------------------------------------------------------------------------


class TestRecordResponse:
    def test_records_remembered_response(self) -> None:
        repo = _mock_repo()
        session = MagicMock(spec=StudySession)
        session.id = 1
        session.user_id = 1
        session.cards_reviewed = 0
        session.cards_correct = 0
        session.cards_incorrect = 0
        session.cards_skipped = 0
        repo.get_session.return_value = session

        card = _make_card()
        repo.get_flashcard.return_value = card
        repo.update_flashcard.return_value = card
        repo.record_review.return_value = MagicMock()
        repo.update_session.return_value = session
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = CardResponse(
            card_id=1,
            response_type="remembered",
            confidence_level="confident",
        )
        result = service.record_response(user, 1, payload)

        assert result.ease_factor is not None
        assert result.review_interval >= 1
        repo.update_flashcard.assert_called_once()
        repo.record_review.assert_called_once()

    def test_raises_404_for_missing_session(self) -> None:
        repo = _mock_repo()
        repo.get_session.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = CardResponse(
            card_id=1, response_type="remembered", confidence_level="confident"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.record_response(user, 999, payload)
        assert exc_info.value.status_code == 404

    def test_raises_404_for_missing_card(self) -> None:
        repo = _mock_repo()
        session = MagicMock(spec=StudySession)
        session.id = 1
        session.user_id = 1
        repo.get_session.return_value = session
        repo.get_flashcard.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        payload = CardResponse(
            card_id=999, response_type="forgot", confidence_level="unsure"
        )
        with pytest.raises(HTTPException) as exc_info:
            service.record_response(user, 1, payload)
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Queue Tests
# ---------------------------------------------------------------------------


class TestGetQueueSummary:
    def test_returns_summary(self) -> None:
        repo = _mock_repo()
        repo.get_queue_summary_counts.return_value = {
            "total_due": 15,
            "overdue_count": 5,
            "new_today_count": 3,
        }
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        result = service.get_queue_summary(user)
        assert result.total_due == 15
        assert result.overdue_count == 5
        assert result.new_today_count == 3
        assert result.estimated_review_minutes == 7  # (15 * 30) // 60


# ---------------------------------------------------------------------------
# Marketplace Tests
# ---------------------------------------------------------------------------


class TestRateDeck:
    def test_rates_deck_successfully(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(owner_id=2, visibility="public")
        repo.get_deck.return_value = deck
        repo.upsert_rating.return_value = MagicMock()
        repo.compute_average_rating.return_value = (4.0, 1)
        repo.update_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.rate_deck(user, 1, 4)
        repo.upsert_rating.assert_called_once_with(1, 1, 4)

    def test_raises_403_on_self_rating(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(owner_id=1)
        repo.get_deck.return_value = deck
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        with pytest.raises(HTTPException) as exc_info:
            service.rate_deck(user, 1, 5)
        assert exc_info.value.status_code == 403

    def test_raises_404_for_missing_deck(self) -> None:
        repo = _mock_repo()
        repo.get_deck.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.rate_deck(user, 999, 3)
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# Social Tests
# ---------------------------------------------------------------------------


class TestFollowCreator:
    def test_follows_successfully(self) -> None:
        repo = _mock_repo()
        repo.create_follow.return_value = MagicMock()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.follow_creator(user, 2)
        repo.create_follow.assert_called_once_with(1, 2)

    def test_raises_422_on_self_follow(self) -> None:
        repo = _mock_repo()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        with pytest.raises(HTTPException) as exc_info:
            service.follow_creator(user, 1)
        assert exc_info.value.status_code == 422


class TestUnfollowCreator:
    def test_unfollows_successfully(self) -> None:
        repo = _mock_repo()
        repo.delete_follow.return_value = True
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.unfollow_creator(user, 2)
        repo.delete_follow.assert_called_once_with(1, 2)

    def test_raises_404_when_not_following(self) -> None:
        repo = _mock_repo()
        repo.delete_follow.return_value = False
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        with pytest.raises(HTTPException) as exc_info:
            service.unfollow_creator(user, 2)
        assert exc_info.value.status_code == 404


class TestCreateComment:
    def test_creates_comment_successfully(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(visibility="public")
        repo.get_deck.return_value = deck
        comment_mock = MagicMock()
        repo.create_comment.return_value = comment_mock
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        service.create_comment(user, 1, "Great deck!")
        repo.create_comment.assert_called_once()

    def test_raises_404_for_missing_deck(self) -> None:
        repo = _mock_repo()
        repo.get_deck.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.create_comment(user, 999, "Comment")
        assert exc_info.value.status_code == 404

    def test_holds_comment_with_moderation_keyword(self) -> None:
        repo = _mock_repo()
        deck = _make_deck(visibility="public")
        repo.get_deck.return_value = deck
        repo.create_comment.return_value = MagicMock()
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        service.create_comment(user, 1, "This is spam content")
        # Verify the comment was created with is_held_for_moderation=True
        call_args = repo.create_comment.call_args[0][0]
        assert call_args.is_held_for_moderation is True


class TestDeleteComment:
    def test_deletes_own_comment(self) -> None:
        repo = _mock_repo()
        comment = MagicMock()
        comment.user_id = 1
        comment.deleted_at = None
        repo.get_comment.return_value = comment
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        service.delete_comment(user, 1)
        repo.soft_delete_comment.assert_called_once()

    def test_raises_403_for_other_users_comment(self) -> None:
        repo = _mock_repo()
        comment = MagicMock()
        comment.user_id = 2
        repo.get_comment.return_value = comment
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user(user_id=1)

        with pytest.raises(HTTPException) as exc_info:
            service.delete_comment(user, 1)
        assert exc_info.value.status_code == 403

    def test_raises_404_for_missing_comment(self) -> None:
        repo = _mock_repo()
        repo.get_comment.return_value = None
        service = FlashcardService(flashcard_repo=repo)
        user = _mock_user()

        with pytest.raises(HTTPException) as exc_info:
            service.delete_comment(user, 999)
        assert exc_info.value.status_code == 404
