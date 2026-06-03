"""Service tests for the readiness feature — mocked repositories.

Tests business logic in isolation per testing-standards.md.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.models import UserSubtopicMastery
from app.features.mastery.repository import MasteryRepository
from app.features.mock_exams.models import MockExamAttempt
from app.features.mock_exams.repository import MockExamRepository
from app.features.readiness.models import ReadinessScoreHistory
from app.features.readiness.repository import ReadinessRepository
from app.features.readiness.service import ReadinessService


# ------------------------------------------------------------------
# Factories
# ------------------------------------------------------------------


def _make_mastery_row(**kwargs) -> MagicMock:
    defaults = {
        "id": 1,
        "user_id": 1,
        "subtopic_id": 1,
        "mastery_score": 0.6,
        "retention_score": 0.85,
        "total_attempts": 10,
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=UserSubtopicMastery)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


def _make_score_history(**kwargs) -> MagicMock:
    defaults = {
        "id": 1,
        "user_id": 1,
        "score": 65,
        "mastery_component": 60.0,
        "retention_component": 70.0,
        "mock_component": 55.0,
        "coverage_component": 40.0,
        "weights_used": '{"mastery": 0.4, "retention": 0.25, "mock_exam": 0.25, "coverage": 0.1}',
        "computed_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=ReadinessScoreHistory)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


def _make_mock_attempt(**kwargs) -> MagicMock:
    defaults = {
        "id": 1,
        "user_id": 1,
        "score": 40,
        "max_score": 50,
        "submitted_at": datetime.now(timezone.utc) - timedelta(days=5),
        "started_at": datetime.now(timezone.utc) - timedelta(days=5, hours=3),
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=MockExamAttempt)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------


@pytest.fixture
def mock_readiness_repo() -> MagicMock:
    return MagicMock(spec=ReadinessRepository)


@pytest.fixture
def mock_mastery_repo() -> MagicMock:
    return MagicMock(spec=MasteryRepository)


@pytest.fixture
def mock_flashcard_repo() -> MagicMock:
    return MagicMock(spec=FlashcardRepository)


@pytest.fixture
def mock_mock_exam_repo() -> MagicMock:
    return MagicMock(spec=MockExamRepository)


@pytest.fixture
def mock_content_repo() -> MagicMock:
    return MagicMock(spec=SubtopicRepository)


@pytest.fixture
def mock_question_repo() -> MagicMock:
    return MagicMock(spec=QuestionRepository)


@pytest.fixture
def service(
    mock_readiness_repo,
    mock_mastery_repo,
    mock_flashcard_repo,
    mock_mock_exam_repo,
    mock_content_repo,
    mock_question_repo,
) -> ReadinessService:
    return ReadinessService(
        readiness_repo=mock_readiness_repo,
        mastery_repo=mock_mastery_repo,
        flashcard_repo=mock_flashcard_repo,
        mock_exam_repo=mock_mock_exam_repo,
        content_repo=mock_content_repo,
        question_repo=mock_question_repo,
    )


# ------------------------------------------------------------------
# get_readiness_level tests
# ------------------------------------------------------------------


class TestGetReadinessLevel:
    def test_not_ready_at_zero(self, service):
        assert service.get_readiness_level(0) == "Not Ready"

    def test_not_ready_at_39(self, service):
        assert service.get_readiness_level(39) == "Not Ready"

    def test_getting_there_at_40(self, service):
        assert service.get_readiness_level(40) == "Getting There"

    def test_getting_there_at_59(self, service):
        assert service.get_readiness_level(59) == "Getting There"

    def test_almost_ready_at_60(self, service):
        assert service.get_readiness_level(60) == "Almost Ready"

    def test_almost_ready_at_79(self, service):
        assert service.get_readiness_level(79) == "Almost Ready"

    def test_exam_ready_at_80(self, service):
        assert service.get_readiness_level(80) == "Exam Ready"

    def test_exam_ready_at_100(self, service):
        assert service.get_readiness_level(100) == "Exam Ready"


# ------------------------------------------------------------------
# get_current tests
# ------------------------------------------------------------------


class TestGetCurrent:
    def test_returns_zero_when_no_history(self, service, mock_readiness_repo):
        mock_readiness_repo.get_latest.return_value = None

        result = service.get_current(user_id=1)

        assert result.score == 0
        assert result.delta is None
        assert result.stale_score is False

    def test_returns_latest_score_with_delta(self, service, mock_readiness_repo):
        latest = _make_score_history(score=72)
        past = _make_score_history(score=65)
        mock_readiness_repo.get_latest.return_value = latest
        mock_readiness_repo.get_score_at_date.return_value = past

        result = service.get_current(user_id=1)

        assert result.score == 72
        assert result.delta == 7

    def test_returns_null_delta_when_no_past_record(self, service, mock_readiness_repo):
        latest = _make_score_history(score=50)
        mock_readiness_repo.get_latest.return_value = latest
        mock_readiness_repo.get_score_at_date.return_value = None

        result = service.get_current(user_id=1)

        assert result.score == 50
        assert result.delta is None


# ------------------------------------------------------------------
# compute_and_persist tests
# ------------------------------------------------------------------


class TestComputeAndPersist:
    def test_no_activity_returns_score_zero(
        self, service, mock_mastery_repo, mock_flashcard_repo, mock_mock_exam_repo, mock_readiness_repo
    ):
        mock_mastery_repo.list_by_user.return_value = []
        mock_flashcard_repo.count_user_reviews.return_value = 0
        mock_mock_exam_repo.get_completed_for_user.return_value = []
        mock_readiness_repo.create.side_effect = lambda x: x

        result = service.compute_and_persist(user_id=1)

        assert result.score == 0
        assert result.mastery_component == 0.0
        assert result.retention_component == 0.0
        assert result.mock_component == 0.0
        assert result.coverage_component == 0.0

    def test_with_mastery_and_no_mock_redistributes_weights(
        self,
        service,
        mock_mastery_repo,
        mock_flashcard_repo,
        mock_mock_exam_repo,
        mock_readiness_repo,
        mock_content_repo,
    ):
        mastery_rows = [
            _make_mastery_row(subtopic_id=i, mastery_score=0.7, retention_score=0.8)
            for i in range(1, 4)
        ]
        mock_mastery_repo.list_by_user.return_value = mastery_rows
        mock_flashcard_repo.count_user_reviews.return_value = 0
        mock_flashcard_repo.get_retention_by_tag.return_value = []
        mock_mock_exam_repo.get_completed_for_user.return_value = []

        # Coverage computation needs db access through content_repo.db
        mock_db = MagicMock()
        mock_db.execute.return_value.all.return_value = []
        mock_content_repo.db = mock_db

        mock_readiness_repo.create.side_effect = lambda x: x

        result = service.compute_and_persist(user_id=1)

        # Score should be computed using no-mock weights
        # mastery: 0.7 * 100 = 70, retention (fallback): 0.8 * 100 = 80
        # With no-mock weights: 70 * 0.525 + 80 * 0.375 + 0 * 0 + 0 * 0.1 = 36.75 + 30 = 66.75 → 67
        assert result.score == 67
        assert '"mock_exam": 0.0' in result.weights_used

    def test_graceful_degradation_returns_stale_on_failure(
        self, service, mock_mastery_repo, mock_readiness_repo
    ):
        mock_mastery_repo.list_by_user.side_effect = RuntimeError("DB error")
        stale = _make_score_history(score=55)
        mock_readiness_repo.get_latest.return_value = stale

        result = service.compute_and_persist(user_id=1)

        assert result.score == 55

    def test_graceful_degradation_raises_when_no_stale(
        self, service, mock_mastery_repo, mock_readiness_repo
    ):
        mock_mastery_repo.list_by_user.side_effect = RuntimeError("DB error")
        mock_readiness_repo.get_latest.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.compute_and_persist(user_id=1)
        assert exc_info.value.status_code == 500


# ------------------------------------------------------------------
# get_trend tests
# ------------------------------------------------------------------


class TestGetTrend:
    def test_returns_30_day_trend_with_carry_forward(
        self, service, mock_readiness_repo
    ):
        # Simulate records only on days 5 and 15
        today = date.today()
        start_date = today - timedelta(days=29)

        record1 = _make_score_history(
            score=40,
            computed_at=datetime.combine(
                start_date + timedelta(days=5), datetime.min.time()
            ).replace(tzinfo=timezone.utc),
        )
        record2 = _make_score_history(
            score=60,
            computed_at=datetime.combine(
                start_date + timedelta(days=15), datetime.min.time()
            ).replace(tzinfo=timezone.utc),
        )

        mock_readiness_repo.get_trend.return_value = [record1, record2]
        mock_readiness_repo.get_score_at_date.return_value = None

        result = service.get_trend(user_id=1, days=30)

        assert len(result) == 30
        # First 5 days should be 0 (no seed record)
        assert result[0].score == 0
        assert result[4].score == 0
        # Day 5 onward should be 40
        assert result[5].score == 40
        assert result[14].score == 40
        # Day 15 onward should be 60
        assert result[15].score == 60
        assert result[29].score == 60

    def test_uses_seed_record_for_carry_forward(
        self, service, mock_readiness_repo
    ):
        seed = _make_score_history(score=30)
        mock_readiness_repo.get_trend.return_value = []
        mock_readiness_repo.get_score_at_date.return_value = seed

        result = service.get_trend(user_id=1, days=30)

        assert len(result) == 30
        # All should carry forward from seed
        assert all(point.score == 30 for point in result)


# ------------------------------------------------------------------
# get_dashboard tests
# ------------------------------------------------------------------


class TestGetDashboard:
    def test_returns_dashboard_with_no_history(self, service, mock_readiness_repo):
        mock_readiness_repo.get_latest.return_value = None

        result = service.get_dashboard(user_id=1)

        assert result.score == 0
        assert result.readiness_level == "Not Ready"
        assert result.top_impact_subtopics == []
        assert result.stale_data is False

    def test_returns_dashboard_with_data(
        self, service, mock_readiness_repo, mock_mastery_repo, mock_content_repo
    ):
        latest = _make_score_history(score=65)
        mock_readiness_repo.get_latest.return_value = latest
        mock_readiness_repo.get_score_at_date.return_value = None

        # Setup mastery data for top impact
        mastery_rows = [
            _make_mastery_row(subtopic_id=1, mastery_score=0.3),
            _make_mastery_row(subtopic_id=2, mastery_score=0.5),
            _make_mastery_row(subtopic_id=3, mastery_score=0.9),  # Above target
        ]
        mock_mastery_repo.list_by_user.return_value = mastery_rows

        # Mock subtopic lookups
        subtopic_mock = MagicMock()
        subtopic_mock.title = "Test Subtopic"
        mock_content_repo.get.return_value = subtopic_mock

        result = service.get_dashboard(user_id=1)

        assert result.score == 65
        assert result.readiness_level == "Almost Ready"
        # Should have 2 impact subtopics (subtopic 3 is above target)
        assert len(result.top_impact_subtopics) == 2

    def test_graceful_degradation_on_failure(
        self, service, mock_readiness_repo, mock_mastery_repo
    ):
        latest = _make_score_history(score=50)
        # First call in _get_dashboard_inner succeeds
        # But mastery lookup fails
        mock_readiness_repo.get_latest.return_value = latest
        mock_readiness_repo.get_score_at_date.side_effect = RuntimeError("DB error")

        result = service.get_dashboard(user_id=1)

        # Should return stale data
        assert result.score == 50
        assert result.stale_data is True
