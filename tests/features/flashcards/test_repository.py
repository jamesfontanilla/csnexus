"""Repository tests for the flashcard feature slice (Task 5.2).

Per testing-standards.md: real in-memory SQLite, no mocks.
Each test seeds a User for FK targets and exercises FlashcardRepository.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.features.flashcards.models import (
    Deck,
    DeckComment,
    Flashcard,
    ReviewLog,
    StudySession,
)
from app.features.flashcards.repository import FlashcardRepository
from app.features.users.models import Category, User
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _make_user(
    db: Session, *, email: str = "alice@example.com"
) -> User:
    repo = UserRepository(db=db)
    username = email.split("@")[0].replace(".", "_")
    return repo.create(
        UserCreate(
            email=email,
            display_name="Test User",
            username=username,
            age=25,
            category=Category.PROFESSIONAL.value,
            password="Strong1Pass!",
        ),
        password_hash="bcrypt$fake$hash",
    )


def _make_deck(
    db: Session,
    owner_id: int,
    *,
    title: str = "Test Deck",
    category: str = "verbal",
    visibility: str = "private",
) -> Deck:
    deck = Deck(
        owner_id=owner_id,
        title=title,
        category=category,
        visibility=visibility,
    )
    db.add(deck)
    db.commit()
    db.refresh(deck)
    return deck


def _make_card(
    db: Session,
    deck_id: int,
    *,
    front: str = "What is X?",
    back: str = "X is Y.",
    card_type: str = "basic",
) -> Flashcard:
    card = Flashcard(
        deck_id=deck_id,
        front=front,
        back=back,
        card_type=card_type,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Deck CRUD
# ---------------------------------------------------------------------------


class TestDeckCRUD:
    def test_create_deck(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = Deck(owner_id=user.id, title="My Deck", category="verbal")
        result = repo.create_deck(deck)
        assert result.id is not None
        assert result.title == "My Deck"
        assert result.owner_id == user.id

    def test_get_deck_returns_none_for_missing(self, db_session: Session) -> None:
        repo = FlashcardRepository(db=db_session)
        assert repo.get_deck(999) is None

    def test_get_deck_excludes_soft_deleted(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        repo.soft_delete_deck(deck, _now())
        assert repo.get_deck(deck.id) is None

    def test_soft_delete_deck_cascades_to_cards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        _make_card(db_session, deck.id, front="Q1", back="A1")
        _make_card(db_session, deck.id, front="Q2", back="A2")

        repo.soft_delete_deck(deck, _now())

        # Cards should also be soft-deleted
        assert repo.count_deck_flashcards(deck.id) == 0

    def test_list_user_decks_filters_by_category(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        _make_deck(db_session, user.id, title="Verbal", category="verbal")
        _make_deck(db_session, user.id, title="Numerical", category="numerical")

        decks, total = repo.list_user_decks(user.id, category="verbal")
        assert total == 1
        assert decks[0].title == "Verbal"

    def test_list_user_decks_excludes_soft_deleted(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        repo.soft_delete_deck(deck, _now())

        decks, total = repo.list_user_decks(user.id)
        assert total == 0
        assert decks == []

    def test_duplicate_deck_copies_cards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        user2 = _make_user(db_session, email="bob@example.com")
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")
        _make_card(db_session, deck.id, front="Q1", back="A1")
        _make_card(db_session, deck.id, front="Q2", back="A2")

        clone = repo.duplicate_deck(deck, user2.id)
        assert clone.owner_id == user2.id
        assert clone.cloned_from_deck_id == deck.id
        assert clone.cloned_from_user_id == user.id
        assert repo.count_deck_flashcards(clone.id) == 2
        # Original clone_count incremented
        db_session.refresh(deck)
        assert deck.clone_count == 1

    def test_get_deck_by_owner_and_title(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        _make_deck(db_session, user.id, title="Unique Title")

        found = repo.get_deck_by_owner_and_title(user.id, "Unique Title")
        assert found is not None
        assert found.title == "Unique Title"

        not_found = repo.get_deck_by_owner_and_title(user.id, "Nonexistent")
        assert not_found is None


# ---------------------------------------------------------------------------
# Flashcard CRUD
# ---------------------------------------------------------------------------


class TestFlashcardCRUD:
    def test_create_flashcard(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = Flashcard(
            deck_id=deck.id, front="Q", back="A", card_type="basic"
        )
        result = repo.create_flashcard(card)
        assert result.id is not None
        assert result.ease_factor == 2.5
        assert result.review_interval == 1

    def test_get_flashcard_excludes_soft_deleted(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = _make_card(db_session, deck.id)
        repo.soft_delete_flashcard(card, _now())
        assert repo.get_flashcard(card.id) is None

    def test_list_deck_flashcards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        _make_card(db_session, deck.id, front="Q1", back="A1")
        _make_card(db_session, deck.id, front="Q2", back="A2")

        cards = repo.list_deck_flashcards(deck.id)
        assert len(cards) == 2

    def test_count_deck_flashcards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        _make_card(db_session, deck.id, front="Q1", back="A1")
        _make_card(db_session, deck.id, front="Q2", back="A2")
        _make_card(db_session, deck.id, front="Q3", back="A3")

        assert repo.count_deck_flashcards(deck.id) == 3


# ---------------------------------------------------------------------------
# Review Log
# ---------------------------------------------------------------------------


class TestReviewLog:
    def test_record_review(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = _make_card(db_session, deck.id)

        review = ReviewLog(
            user_id=user.id,
            card_id=card.id,
            response_type="remembered",
            confidence_level="confident",
            ease_factor_before=2.5,
            interval_before=1,
            ease_factor_after=2.5,
            interval_after=3,
            reviewed_at=_now(),
            client_event_id="evt-001",
        )
        result = repo.record_review(review)
        assert result.id is not None
        assert result.client_event_id == "evt-001"

    def test_get_review_by_client_event_id(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = _make_card(db_session, deck.id)

        review = ReviewLog(
            user_id=user.id,
            card_id=card.id,
            response_type="forgot",
            ease_factor_before=2.5,
            interval_before=1,
            ease_factor_after=2.3,
            interval_after=1,
            reviewed_at=_now(),
            client_event_id="dedup-123",
        )
        repo.record_review(review)

        found = repo.get_review_by_client_event_id("dedup-123")
        assert found is not None
        assert found.response_type == "forgot"

        not_found = repo.get_review_by_client_event_id("nonexistent")
        assert not_found is None

    def test_get_review_history(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = _make_card(db_session, deck.id)

        for i in range(3):
            repo.record_review(ReviewLog(
                user_id=user.id,
                card_id=card.id,
                response_type="remembered",
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.5,
                interval_after=1,
                reviewed_at=_now() - timedelta(hours=i),
                client_event_id=f"evt-{i}",
            ))

        history = repo.get_review_history(user.id, card.id)
        assert len(history) == 3


# ---------------------------------------------------------------------------
# Review Queue
# ---------------------------------------------------------------------------


class TestReviewQueue:
    def test_get_daily_queue_returns_due_cards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        # Card due yesterday (overdue)
        overdue = _make_card(db_session, deck.id, front="Overdue", back="A")
        overdue.next_review_date = date.today() - timedelta(days=1)
        db_session.commit()

        # Card due today
        today_card = _make_card(db_session, deck.id, front="Today", back="B")
        today_card.next_review_date = date.today()
        db_session.commit()

        # Card due tomorrow (not due)
        future = _make_card(db_session, deck.id, front="Future", back="C")
        future.next_review_date = date.today() + timedelta(days=1)
        db_session.commit()

        # New card (no review date)
        _make_card(db_session, deck.id, front="New", back="D")

        queue = repo.get_daily_queue(user.id, today=date.today())
        # Should include overdue, today, and new (not future)
        assert len(queue) == 3
        # Overdue first, then today, then new (NULL last)
        assert queue[0].front == "Overdue"
        assert queue[1].front == "Today"
        assert queue[2].front == "New"

    def test_get_daily_queue_excludes_graduated(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        card = _make_card(db_session, deck.id)
        card.is_graduated = True
        card.next_review_date = date.today() - timedelta(days=5)
        db_session.commit()

        queue = repo.get_daily_queue(user.id, today=date.today())
        assert len(queue) == 0

    def test_get_daily_queue_respects_max_cards(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        for i in range(10):
            _make_card(db_session, deck.id, front=f"Q{i}", back=f"A{i}")

        queue = repo.get_daily_queue(user.id, today=date.today(), max_cards=3)
        assert len(queue) == 3

    def test_get_queue_summary_counts(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        # 2 overdue
        for i in range(2):
            c = _make_card(db_session, deck.id, front=f"OD{i}", back="A")
            c.next_review_date = date.today() - timedelta(days=i + 1)
        # 1 new (no review date)
        _make_card(db_session, deck.id, front="New", back="B")
        db_session.commit()

        summary = repo.get_queue_summary_counts(user.id, today=date.today())
        assert summary["overdue_count"] == 2
        assert summary["new_today_count"] == 1
        assert summary["total_due"] == 3  # 2 overdue + 1 new


# ---------------------------------------------------------------------------
# Marketplace
# ---------------------------------------------------------------------------


class TestMarketplace:
    def test_search_decks_returns_public_only(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        _make_deck(db_session, user.id, title="Public", visibility="public")
        _make_deck(db_session, user.id, title="Private", visibility="private")

        results, total = repo.search_decks()
        assert total == 1
        assert results[0].title == "Public"

    def test_search_decks_with_query(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        _make_deck(db_session, user.id, title="Python Basics", visibility="public")
        _make_deck(db_session, user.id, title="Math Review", visibility="public")

        results, total = repo.search_decks(query="Python")
        assert total == 1
        assert results[0].title == "Python Basics"

    def test_search_decks_filters_by_category(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        _make_deck(db_session, user.id, title="V1", category="verbal", visibility="public")
        _make_deck(db_session, user.id, title="N1", category="numerical", visibility="public")

        results, total = repo.search_decks(category="numerical")
        assert total == 1
        assert results[0].title == "N1"

    def test_upsert_rating_creates_new(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")
        user2 = _make_user(db_session, email="bob@example.com")

        rating = repo.upsert_rating(deck.id, user2.id, 4)
        assert rating.rating == 4

    def test_upsert_rating_updates_existing(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")
        user2 = _make_user(db_session, email="bob@example.com")

        repo.upsert_rating(deck.id, user2.id, 3)
        updated = repo.upsert_rating(deck.id, user2.id, 5)
        assert updated.rating == 5

    def test_compute_average_rating(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")
        u2 = _make_user(db_session, email="bob@example.com")
        u3 = _make_user(db_session, email="carol@example.com")

        repo.upsert_rating(deck.id, u2.id, 4)
        repo.upsert_rating(deck.id, u3.id, 2)

        avg, count = repo.compute_average_rating(deck.id)
        assert count == 2
        assert avg == 3.0


# ---------------------------------------------------------------------------
# Social: Follows
# ---------------------------------------------------------------------------


class TestFollows:
    def test_create_and_delete_follow(self, db_session: Session) -> None:
        user1 = _make_user(db_session, email="alice@example.com")
        user2 = _make_user(db_session, email="bob@example.com")
        repo = FlashcardRepository(db=db_session)

        follow = repo.create_follow(user1.id, user2.id)
        assert follow.follower_id == user1.id
        assert follow.followed_id == user2.id

        followers = repo.get_followers(user2.id)
        assert len(followers) == 1

        deleted = repo.delete_follow(user1.id, user2.id)
        assert deleted is True

        followers = repo.get_followers(user2.id)
        assert len(followers) == 0

    def test_delete_nonexistent_follow_returns_false(self, db_session: Session) -> None:
        user1 = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        assert repo.delete_follow(user1.id, 999) is False

    def test_get_feed_decks(self, db_session: Session) -> None:
        user1 = _make_user(db_session, email="alice@example.com")
        user2 = _make_user(db_session, email="bob@example.com")
        repo = FlashcardRepository(db=db_session)

        # user1 follows user2
        repo.create_follow(user1.id, user2.id)

        # user2 has a public deck
        _make_deck(db_session, user2.id, title="Bob's Deck", visibility="public")
        # user2 has a private deck (should not appear)
        _make_deck(db_session, user2.id, title="Bob's Private", visibility="private")

        feed = repo.get_feed_decks(user1.id)
        assert len(feed) == 1
        assert feed[0].title == "Bob's Deck"


# ---------------------------------------------------------------------------
# Social: Comments
# ---------------------------------------------------------------------------


class TestComments:
    def test_create_and_list_comments(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")

        comment = DeckComment(
            deck_id=deck.id, user_id=user.id, body="Great deck!"
        )
        result = repo.create_comment(comment)
        assert result.id is not None

        comments = repo.list_deck_comments(deck.id)
        assert len(comments) == 1
        assert comments[0].body == "Great deck!"

    def test_soft_delete_comment(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id, visibility="public")

        comment = DeckComment(
            deck_id=deck.id, user_id=user.id, body="Delete me"
        )
        repo.create_comment(comment)
        repo.soft_delete_comment(comment, _now())

        comments = repo.list_deck_comments(deck.id)
        assert len(comments) == 0


# ---------------------------------------------------------------------------
# Sync (batch deduplication)
# ---------------------------------------------------------------------------


class TestSync:
    def test_batch_upsert_deduplicates_by_client_event_id(
        self, db_session: Session
    ) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)
        card = _make_card(db_session, deck.id)

        reviews = [
            ReviewLog(
                user_id=user.id,
                card_id=card.id,
                response_type="remembered",
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.5,
                interval_after=3,
                reviewed_at=_now(),
                client_event_id="sync-001",
            ),
            ReviewLog(
                user_id=user.id,
                card_id=card.id,
                response_type="forgot",
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.3,
                interval_after=1,
                reviewed_at=_now(),
                client_event_id="sync-002",
            ),
        ]
        accepted, duplicates, failures = repo.batch_upsert_reviews(reviews)
        assert accepted == 2
        assert duplicates == 0

        # Submit again — should all be duplicates
        reviews2 = [
            ReviewLog(
                user_id=user.id,
                card_id=card.id,
                response_type="remembered",
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.5,
                interval_after=3,
                reviewed_at=_now(),
                client_event_id="sync-001",
            ),
            ReviewLog(
                user_id=user.id,
                card_id=card.id,
                response_type="forgot",
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.3,
                interval_after=1,
                reviewed_at=_now(),
                client_event_id="sync-002",
            ),
        ]
        accepted2, duplicates2, _ = repo.batch_upsert_reviews(reviews2)
        assert accepted2 == 0
        assert duplicates2 == 2


# ---------------------------------------------------------------------------
# Study Sessions
# ---------------------------------------------------------------------------


class TestStudySessions:
    def test_create_and_get_session(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        session = StudySession(
            user_id=user.id,
            study_mode="swipe",
            deck_ids=f"[{deck.id}]",
            started_at=_now(),
        )
        result = repo.create_session(session)
        assert result.id is not None

        fetched = repo.get_session(result.id)
        assert fetched is not None
        assert fetched.study_mode == "swipe"

    def test_update_session(self, db_session: Session) -> None:
        user = _make_user(db_session)
        repo = FlashcardRepository(db=db_session)
        deck = _make_deck(db_session, user.id)

        session = StudySession(
            user_id=user.id,
            study_mode="typing",
            deck_ids=f"[{deck.id}]",
            started_at=_now(),
        )
        repo.create_session(session)
        updated = repo.update_session(
            session, cards_reviewed=5, cards_correct=3, ended_at=_now()
        )
        assert updated.cards_reviewed == 5
        assert updated.cards_correct == 3
        assert updated.ended_at is not None
