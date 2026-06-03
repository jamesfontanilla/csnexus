"""Service tests for QueueService.

Tests business logic in isolation using mocked repositories.
Uses MagicMock(spec=RepositoryClass) to catch attribute typos at test time.
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.features.content.repository import LessonRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.smart_queue.models import DailyQueue, QueueItem
from app.features.smart_queue.repository import QueueRepository
from app.features.smart_queue.service import QueueService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_queue_repo() -> MagicMock:
    return MagicMock(spec=QueueRepository)


@pytest.fixture()
def mock_flashcard_repo() -> MagicMock:
    return MagicMock(spec=FlashcardRepository)


@pytest.fixture()
def mock_mastery_repo() -> MagicMock:
    return MagicMock(spec=MasteryRepository)


@pytest.fixture()
def mock_subtopic_repo() -> MagicMock:
    return MagicMock(spec=SubtopicRepository)


@pytest.fixture()
def mock_lesson_repo() -> MagicMock:
    return MagicMock(spec=LessonRepository)


@pytest.fixture()
def service(
    mock_queue_repo: MagicMock,
    mock_flashcard_repo: MagicMock,
    mock_mastery_repo: MagicMock,
    mock_subtopic_repo: MagicMock,
    mock_lesson_repo: MagicMock,
) -> QueueService:
    return QueueService(
        queue_repo=mock_queue_repo,
        flashcard_repo=mock_flashcard_repo,
        mastery_repo=mock_mastery_repo,
        subtopic_repo=mock_subtopic_repo,
        lesson_repo=mock_lesson_repo,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_daily_queue(
    *,
    queue_id: int = 1,
    user_id: int = 1,
    queue_date: date | None = None,
    time_budget_minutes: int = 30,
    total_estimated_seconds: int = 1800,
    items_total: int = 5,
    items_completed: int = 0,
) -> DailyQueue:
    queue = DailyQueue(
        user_id=user_id,
        queue_date=queue_date or date.today(),
        time_budget_minutes=time_budget_minutes,
        total_estimated_seconds=total_estimated_seconds,
        items_total=items_total,
        items_completed=items_completed,
    )
    queue.id = queue_id
    return queue


def _make_queue_item(
    *,
    item_id: int = 1,
    queue_id: int = 1,
    position: int = 0,
    item_type: str = "flashcard_review",
    payload: str = '{"card_ids": [1, 2, 3]}',
    estimated_seconds: int = 24,
    completed_at: datetime | None = None,
) -> QueueItem:
    item = QueueItem(
        queue_id=queue_id,
        position=position,
        item_type=item_type,
        payload=payload,
        estimated_seconds=estimated_seconds,
        completed_at=completed_at,
    )
    item.id = item_id
    return item


# ---------------------------------------------------------------------------
# get_daily_queue tests
# ---------------------------------------------------------------------------


class TestGetDailyQueue:
    """Tests for QueueService.get_daily_queue."""

    def test_returns_existing_queue(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        """When a queue already exists for today, return it without regenerating."""
        queue = _make_daily_queue()
        items = [
            _make_queue_item(item_id=1, position=0),
            _make_queue_item(item_id=2, position=1, item_type="quiz_practice"),
        ]

        mock_queue_repo.get_or_create_for_date.return_value = queue
        mock_queue_repo.get_items.return_value = items

        result = service.get_daily_queue(user_id=1)

        assert result.time_budget_minutes == 30
        assert result.items_completed == 0
        assert result.items_remaining == 5
        assert len(result.items) == 2

    def test_generates_new_queue_when_none_exists(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
        mock_flashcard_repo: MagicMock,
        mock_mastery_repo: MagicMock,
        mock_subtopic_repo: MagicMock,
        mock_lesson_repo: MagicMock,
    ) -> None:
        """When no queue exists for today, generate and persist a new one."""
        mock_queue_repo.get_or_create_for_date.return_value = None
        mock_queue_repo.get_user_preferences.return_value = 30

        # No exam date
        mock_queue_repo.db = MagicMock()
        mock_queue_repo.db.execute.return_value.scalar_one_or_none.return_value = None

        # No flashcards, no mastery
        mock_flashcard_repo.get_daily_queue.return_value = []
        mock_mastery_repo.list_weakest.return_value = []
        mock_mastery_repo.list_by_user.return_value = []

        # No coverage gaps either — triggers fallback
        mock_subtopic_repo.list.return_value = []

        # create_queue returns a queue with an ID
        created_queue = _make_daily_queue(items_total=0, total_estimated_seconds=0)
        mock_queue_repo.create_queue.return_value = created_queue
        mock_queue_repo.add_items.return_value = []
        mock_queue_repo.get_items.return_value = []

        result = service.get_daily_queue(user_id=1)

        mock_queue_repo.create_queue.assert_called_once()
        assert result.time_budget_minutes == 30


# ---------------------------------------------------------------------------
# complete_item tests
# ---------------------------------------------------------------------------


class TestCompleteItem:
    """Tests for QueueService.complete_item."""

    def test_marks_item_completed_and_returns_queue(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        item = _make_queue_item(completed_at=datetime.now(UTC))
        mock_queue_repo.mark_item_completed.return_value = item

        queue = _make_daily_queue(items_completed=1)
        mock_queue_repo.get_or_create_for_date.return_value = queue
        mock_queue_repo.get_completed_count.return_value = 1
        mock_queue_repo.get_items.return_value = [item]
        mock_queue_repo.db = MagicMock()

        result = service.complete_item(user_id=1, item_id=1)

        mock_queue_repo.mark_item_completed.assert_called_once_with(1)
        assert result.items_completed == 1

    def test_raises_404_when_item_not_found(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        mock_queue_repo.mark_item_completed.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.complete_item(user_id=1, item_id=9999)

        assert exc_info.value.status_code == 404

    def test_raises_404_when_no_queue_for_today(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        item = _make_queue_item(completed_at=datetime.now(UTC))
        mock_queue_repo.mark_item_completed.return_value = item
        mock_queue_repo.get_or_create_for_date.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.complete_item(user_id=1, item_id=1)

        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# regenerate_queue tests
# ---------------------------------------------------------------------------


class TestRegenerateQueue:
    """Tests for QueueService.regenerate_queue."""

    def test_deletes_existing_and_regenerates(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
        mock_flashcard_repo: MagicMock,
        mock_mastery_repo: MagicMock,
        mock_subtopic_repo: MagicMock,
    ) -> None:
        mock_queue_repo.get_user_preferences.return_value = 30
        mock_queue_repo.db = MagicMock()
        mock_queue_repo.db.execute.return_value.scalar_one_or_none.return_value = None

        mock_flashcard_repo.get_daily_queue.return_value = []
        mock_mastery_repo.list_weakest.return_value = []
        mock_mastery_repo.list_by_user.return_value = []
        mock_subtopic_repo.list.return_value = []

        created_queue = _make_daily_queue(items_total=0, total_estimated_seconds=0)
        mock_queue_repo.create_queue.return_value = created_queue
        mock_queue_repo.add_items.return_value = []
        mock_queue_repo.get_items.return_value = []

        result = service.regenerate_queue(user_id=1)

        mock_queue_repo.delete_queue_for_date.assert_called_once()
        mock_queue_repo.create_queue.assert_called_once()


# ---------------------------------------------------------------------------
# get_preferences tests
# ---------------------------------------------------------------------------


class TestGetPreferences:
    """Tests for QueueService.get_preferences."""

    def test_returns_user_preference(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        mock_queue_repo.get_user_preferences.return_value = 60

        result = service.get_preferences(user_id=1)

        assert result.time_budget_minutes == 60

    def test_returns_default_30(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        mock_queue_repo.get_user_preferences.return_value = 30

        result = service.get_preferences(user_id=1)

        assert result.time_budget_minutes == 30


# ---------------------------------------------------------------------------
# update_preferences tests
# ---------------------------------------------------------------------------


class TestUpdatePreferences:
    """Tests for QueueService.update_preferences."""

    def test_updates_and_regenerates_when_no_items_completed(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
        mock_flashcard_repo: MagicMock,
        mock_mastery_repo: MagicMock,
        mock_subtopic_repo: MagicMock,
    ) -> None:
        """If no items completed today, regenerate queue with new budget."""
        queue = _make_daily_queue(items_completed=0)
        mock_queue_repo.get_or_create_for_date.return_value = queue
        mock_queue_repo.has_completed_items.return_value = False
        mock_queue_repo.get_user_preferences.return_value = 60
        mock_queue_repo.db = MagicMock()
        mock_queue_repo.db.execute.return_value.scalar_one_or_none.return_value = None

        mock_flashcard_repo.get_daily_queue.return_value = []
        mock_mastery_repo.list_weakest.return_value = []
        mock_mastery_repo.list_by_user.return_value = []
        mock_subtopic_repo.list.return_value = []

        created_queue = _make_daily_queue(items_total=0, total_estimated_seconds=0)
        mock_queue_repo.create_queue.return_value = created_queue
        mock_queue_repo.add_items.return_value = []
        mock_queue_repo.get_items.return_value = []

        result = service.update_preferences(user_id=1, time_budget_minutes=60)

        assert result.time_budget_minutes == 60
        mock_queue_repo.update_user_preferences.assert_called_once_with(1, 60)
        mock_queue_repo.delete_queue_for_date.assert_called_once()

    def test_does_not_regenerate_when_items_completed(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        """If items have been completed, do NOT regenerate (apply from tomorrow)."""
        queue = _make_daily_queue(items_completed=2)
        mock_queue_repo.get_or_create_for_date.return_value = queue
        mock_queue_repo.has_completed_items.return_value = True

        result = service.update_preferences(user_id=1, time_budget_minutes=15)

        assert result.time_budget_minutes == 15
        mock_queue_repo.update_user_preferences.assert_called_once_with(1, 15)
        mock_queue_repo.delete_queue_for_date.assert_not_called()

    def test_no_regeneration_when_no_queue_exists(
        self,
        service: QueueService,
        mock_queue_repo: MagicMock,
    ) -> None:
        """If no queue exists for today, just persist the preference."""
        mock_queue_repo.get_or_create_for_date.return_value = None

        result = service.update_preferences(user_id=1, time_budget_minutes=15)

        assert result.time_budget_minutes == 15
        mock_queue_repo.delete_queue_for_date.assert_not_called()
