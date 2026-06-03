"""Repository tests for QueueRepository.

Tests run against an in-memory SQLite database with no mocks, verifying
that ORM queries and filters work correctly.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.features.planner.models import OnboardingProfile
from app.features.smart_queue.models import DailyQueue, QueueItem
from app.features.smart_queue.repository import QueueRepository
from app.features.users.models import User


def _seed_user(db: Session, *, email: str = "queue@test.com") -> User:
    """Create a minimal user for FK constraints."""
    user = User(
        email=email,
        display_name="Queue Tester",
        age=25,
        category="PROFESSIONAL",
        role="LEARNER",
        account_state="VERIFIED",
        password_hash="$2b$10$fakehash",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_queue(
    user_id: int,
    *,
    queue_date: date | None = None,
    time_budget_minutes: int = 30,
    total_estimated_seconds: int = 1800,
    items_total: int = 5,
    items_completed: int = 0,
) -> DailyQueue:
    """Factory for DailyQueue with sensible defaults."""
    return DailyQueue(
        user_id=user_id,
        queue_date=queue_date or date.today(),
        time_budget_minutes=time_budget_minutes,
        total_estimated_seconds=total_estimated_seconds,
        items_total=items_total,
        items_completed=items_completed,
    )


def _make_item(
    queue_id: int,
    *,
    position: int = 1,
    item_type: str = "flashcard_review",
    payload: str = '{"card_ids": [1, 2, 3]}',
    estimated_seconds: int = 24,
) -> QueueItem:
    """Factory for QueueItem with sensible defaults."""
    return QueueItem(
        queue_id=queue_id,
        position=position,
        item_type=item_type,
        payload=payload,
        estimated_seconds=estimated_seconds,
    )


class TestGetOrCreateForDate:
    """Tests for QueueRepository.get_or_create_for_date."""

    def test_returns_none_when_no_queue_exists(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        result = repo.get_or_create_for_date(user.id, date.today())
        assert result is None

    def test_returns_existing_queue(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = _make_queue(user.id)
        repo.create_queue(queue)

        result = repo.get_or_create_for_date(user.id, date.today())
        assert result is not None
        assert result.id == queue.id
        assert result.time_budget_minutes == 30

    def test_filters_by_date(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        today = date.today()
        yesterday = today - timedelta(days=1)

        repo.create_queue(_make_queue(user.id, queue_date=today))
        repo.create_queue(_make_queue(user.id, queue_date=yesterday))

        result = repo.get_or_create_for_date(user.id, yesterday)
        assert result is not None
        assert result.queue_date == yesterday

    def test_filters_by_user_id(self, db_session: Session) -> None:
        user1 = _seed_user(db_session, email="user1@test.com")
        user2 = _seed_user(db_session, email="user2@test.com")
        repo = QueueRepository(db=db_session)

        repo.create_queue(_make_queue(user1.id))

        result = repo.get_or_create_for_date(user2.id, date.today())
        assert result is None


class TestCreateQueue:
    """Tests for QueueRepository.create_queue."""

    def test_persists_queue(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = _make_queue(user.id, time_budget_minutes=60, items_total=10)
        result = repo.create_queue(queue)

        assert result.id is not None
        assert result.time_budget_minutes == 60
        assert result.items_total == 10


class TestGetItems:
    """Tests for QueueRepository.get_items."""

    def test_returns_items_ordered_by_position(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        repo.add_items([
            _make_item(queue.id, position=3, item_type="new_content"),
            _make_item(queue.id, position=1, item_type="flashcard_review"),
            _make_item(queue.id, position=2, item_type="quiz_practice"),
        ])

        items = repo.get_items(queue.id)
        assert len(items) == 3
        assert items[0].position == 1
        assert items[1].position == 2
        assert items[2].position == 3

    def test_returns_empty_list_when_no_items(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        items = repo.get_items(queue.id)
        assert items == []


class TestMarkItemCompleted:
    """Tests for QueueRepository.mark_item_completed."""

    def test_sets_completed_at_timestamp(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        items = repo.add_items([_make_item(queue.id)])

        result = repo.mark_item_completed(items[0].id)
        assert result is not None
        assert result.completed_at is not None

    def test_returns_none_for_nonexistent_item(self, db_session: Session) -> None:
        repo = QueueRepository(db=db_session)
        result = repo.mark_item_completed(9999)
        assert result is None


class TestDeleteQueueForDate:
    """Tests for QueueRepository.delete_queue_for_date."""

    def test_deletes_existing_queue(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        repo.create_queue(_make_queue(user.id))
        deleted = repo.delete_queue_for_date(user.id, date.today())

        assert deleted is True
        assert repo.get_or_create_for_date(user.id, date.today()) is None

    def test_returns_false_when_no_queue_exists(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        deleted = repo.delete_queue_for_date(user.id, date.today())
        assert deleted is False


class TestGetUserPreferences:
    """Tests for QueueRepository.get_user_preferences."""

    def test_returns_default_30_when_no_profile(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        result = repo.get_user_preferences(user.id)
        assert result == 30

    def test_returns_profile_time_budget(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        profile = OnboardingProfile(
            user_id=user.id,
            exam_date=date.today() + timedelta(days=60),
            exam_category="Professional",
            time_budget_minutes=60,
        )
        db_session.add(profile)
        db_session.commit()

        result = repo.get_user_preferences(user.id)
        assert result == 60


class TestUpdateUserPreferences:
    """Tests for QueueRepository.update_user_preferences."""

    def test_updates_existing_profile(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        profile = OnboardingProfile(
            user_id=user.id,
            exam_date=date.today() + timedelta(days=60),
            exam_category="Professional",
            time_budget_minutes=30,
        )
        db_session.add(profile)
        db_session.commit()

        result = repo.update_user_preferences(user.id, 15)
        assert result == 15

        # Verify persisted
        assert repo.get_user_preferences(user.id) == 15

    def test_returns_value_when_no_profile_exists(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        result = repo.update_user_preferences(user.id, 60)
        assert result == 60


class TestHasCompletedItems:
    """Tests for QueueRepository.has_completed_items."""

    def test_returns_false_when_no_items_completed(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        repo.add_items([_make_item(queue.id)])

        assert repo.has_completed_items(queue.id) is False

    def test_returns_true_when_item_completed(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        items = repo.add_items([_make_item(queue.id)])
        repo.mark_item_completed(items[0].id)

        assert repo.has_completed_items(queue.id) is True


class TestGetCompletedCount:
    """Tests for QueueRepository.get_completed_count."""

    def test_returns_zero_when_none_completed(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        repo.add_items([
            _make_item(queue.id, position=1),
            _make_item(queue.id, position=2),
        ])

        assert repo.get_completed_count(queue.id) == 0

    def test_returns_correct_count(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = QueueRepository(db=db_session)

        queue = repo.create_queue(_make_queue(user.id))
        items = repo.add_items([
            _make_item(queue.id, position=1),
            _make_item(queue.id, position=2),
            _make_item(queue.id, position=3),
        ])
        repo.mark_item_completed(items[0].id)
        repo.mark_item_completed(items[1].id)

        assert repo.get_completed_count(queue.id) == 2
