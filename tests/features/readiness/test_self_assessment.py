"""Unit tests for self-assessment calibration (repository, service, router layers).

Tests cover:
- Repository: create_self_assessment, get_latest_assessment, get_assessment_history
- Service: overconfident/well_calibrated/underconfident cases, prompt timing
- Router: submit happy path, invalid score validation, history, prompt endpoints

Validates: Requirements 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.common.middlewares.auth import AuthMiddleware
from app.common.middlewares.error_handler import register_exception_handlers
from app.common.middlewares.logging import RequestLoggingMiddleware
from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_exams.repository import MockExamRepository
from app.features.readiness.models import ReadinessScoreHistory, SelfAssessmentRecord
from app.features.readiness.repository import ReadinessRepository
from app.features.readiness.router import get_readiness_service, router as readiness_router
from app.features.readiness.schemas import (
    SelfAssessmentHistoryResponse,
    SelfAssessmentPromptResponse,
    SelfAssessmentResponse,
)
from app.features.readiness.service import ReadinessService
from app.features.users.models import AccountState, Category, Role, User


# ===========================================================================
# Factories
# ===========================================================================


def _seed_user(db: Session, *, email: str = "selfassess@test.com") -> User:
    """Create a minimal user to satisfy FK constraints."""
    user = User(
        email=email,
        display_name="Self-Assessment Tester",
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


def _make_assessment_record(
    user_id: int,
    self_assessed_score: int = 70,
    computed_score: int = 60,
    delta: int = 10,
    calibration_status: str = "well_calibrated",
    assessed_at: datetime | None = None,
) -> SelfAssessmentRecord:
    """Factory for SelfAssessmentRecord with sensible defaults."""
    return SelfAssessmentRecord(
        user_id=user_id,
        self_assessed_score=self_assessed_score,
        computed_score=computed_score,
        delta=delta,
        calibration_status=calibration_status,
        assessed_at=assessed_at or datetime.now(timezone.utc),
    )


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


def _make_user_obj(**overrides: object) -> User:
    defaults: dict[str, object] = {
        "id": 1,
        "email": "alice@example.com",
        "display_name": "Alice",
        "age": 25,
        "category": Category.PROFESSIONAL.value,
        "role": Role.LEARNER.value,
        "account_state": AccountState.VERIFIED.value,
        "is_banned": False,
        "tz_name": "UTC",
        "password_hash": "x",
        "cross_category_preview": False,
    }
    return User(**{**defaults, **overrides})


# ===========================================================================
# Repository Tests — Real DB, No Mocks
# ===========================================================================


class TestRepositoryCreateSelfAssessment:
    """Tests for ReadinessRepository.create_self_assessment."""

    def test_persists_record(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        record = _make_assessment_record(user_id=user.id)

        result = repo.create_self_assessment(record)

        assert result.id is not None
        assert result.user_id == user.id
        assert result.self_assessed_score == 70
        assert result.computed_score == 60
        assert result.delta == 10
        assert result.calibration_status == "well_calibrated"

    def test_stores_overconfident_status(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        record = _make_assessment_record(
            user_id=user.id,
            self_assessed_score=90,
            computed_score=60,
            delta=30,
            calibration_status="overconfident",
        )

        result = repo.create_self_assessment(record)
        assert result.calibration_status == "overconfident"
        assert result.delta == 30


class TestRepositoryGetLatestAssessment:
    """Tests for ReadinessRepository.get_latest_assessment."""

    def test_returns_most_recent(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create_self_assessment(
            _make_assessment_record(
                user_id=user.id, delta=5, assessed_at=now - timedelta(days=10)
            )
        )
        repo.create_self_assessment(
            _make_assessment_record(
                user_id=user.id, delta=20, assessed_at=now - timedelta(days=2)
            )
        )
        repo.create_self_assessment(
            _make_assessment_record(
                user_id=user.id, delta=-15, assessed_at=now - timedelta(days=5)
            )
        )

        latest = repo.get_latest_assessment(user_id=user.id)
        assert latest is not None
        assert latest.delta == 20  # The most recent one (2 days ago)

    def test_returns_none_when_no_records(self, db_session: Session) -> None:
        repo = ReadinessRepository(db=db_session)
        result = repo.get_latest_assessment(user_id=999)
        assert result is None

    def test_filters_by_user_id(self, db_session: Session) -> None:
        user1 = _seed_user(db_session, email="user1@assess.com")
        user2 = _seed_user(db_session, email="user2@assess.com")
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create_self_assessment(
            _make_assessment_record(user_id=user1.id, delta=10, assessed_at=now)
        )
        repo.create_self_assessment(
            _make_assessment_record(user_id=user2.id, delta=-5, assessed_at=now)
        )

        result = repo.get_latest_assessment(user_id=user2.id)
        assert result is not None
        assert result.delta == -5


class TestRepositoryGetAssessmentHistory:
    """Tests for ReadinessRepository.get_assessment_history."""

    def test_returns_all_records_descending(self, db_session: Session) -> None:
        user = _seed_user(db_session)
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create_self_assessment(
            _make_assessment_record(user_id=user.id, delta=5, assessed_at=now - timedelta(days=14))
        )
        repo.create_self_assessment(
            _make_assessment_record(user_id=user.id, delta=20, assessed_at=now - timedelta(days=7))
        )
        repo.create_self_assessment(
            _make_assessment_record(user_id=user.id, delta=-12, assessed_at=now)
        )

        history = repo.get_assessment_history(user_id=user.id)
        assert len(history) == 3
        # Most recent first
        assert history[0].delta == -12
        assert history[1].delta == 20
        assert history[2].delta == 5

    def test_returns_empty_list_when_no_records(self, db_session: Session) -> None:
        repo = ReadinessRepository(db=db_session)
        result = repo.get_assessment_history(user_id=999)
        assert result == []

    def test_filters_by_user_id(self, db_session: Session) -> None:
        user1 = _seed_user(db_session, email="hist1@assess.com")
        user2 = _seed_user(db_session, email="hist2@assess.com")
        repo = ReadinessRepository(db=db_session)
        now = datetime.now(timezone.utc)

        repo.create_self_assessment(
            _make_assessment_record(user_id=user1.id, delta=10, assessed_at=now)
        )
        repo.create_self_assessment(
            _make_assessment_record(user_id=user1.id, delta=5, assessed_at=now - timedelta(days=7))
        )
        repo.create_self_assessment(
            _make_assessment_record(user_id=user2.id, delta=-5, assessed_at=now)
        )

        history = repo.get_assessment_history(user_id=user1.id)
        assert len(history) == 2


# ===========================================================================
# Service Tests — Mocked Repository
# ===========================================================================


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


class TestServiceOverconfident:
    """Service correctly identifies overconfident (delta > +15)."""

    def test_overconfident_when_delta_exceeds_15(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=50)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=70)

        assert result.delta == 20
        assert result.calibration_status == "overconfident"
        assert result.calibration_warning is not None

    def test_overconfident_at_boundary_16(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=50)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=66)

        assert result.delta == 16
        assert result.calibration_status == "overconfident"


class TestServiceWellCalibrated:
    """Service correctly identifies well_calibrated (-10 <= delta <= +15)."""

    def test_well_calibrated_at_zero_delta(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=60)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=60)

        assert result.delta == 0
        assert result.calibration_status == "well_calibrated"
        assert result.calibration_warning is None

    def test_well_calibrated_at_upper_boundary_15(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=50)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=65)

        assert result.delta == 15
        assert result.calibration_status == "well_calibrated"

    def test_well_calibrated_at_lower_boundary_minus_10(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=70)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=60)

        assert result.delta == -10
        assert result.calibration_status == "well_calibrated"


class TestServiceUnderconfident:
    """Service correctly identifies underconfident (delta < -10)."""

    def test_underconfident_when_delta_below_minus_10(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=80)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=60)

        assert result.delta == -20
        assert result.calibration_status == "underconfident"
        assert result.calibration_warning is None

    def test_underconfident_at_boundary_minus_11(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = _make_score_history(score=71)
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=60)

        assert result.delta == -11
        assert result.calibration_status == "underconfident"


class TestServicePromptDue:
    """Service correctly determines when self-assessment prompt is due."""

    def test_prompt_due_after_7_days(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        latest = MagicMock(spec=SelfAssessmentRecord)
        latest.assessed_at = datetime.now(timezone.utc) - timedelta(days=8)
        mock_readiness_repo.get_latest_assessment.return_value = latest

        result = service.is_self_assessment_due(user_id=1)

        assert result.is_due is True
        assert result.last_assessed_at == latest.assessed_at

    def test_prompt_not_due_within_7_days(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        latest = MagicMock(spec=SelfAssessmentRecord)
        latest.assessed_at = datetime.now(timezone.utc) - timedelta(days=3)
        mock_readiness_repo.get_latest_assessment.return_value = latest

        result = service.is_self_assessment_due(user_id=1)

        assert result.is_due is False
        assert result.last_assessed_at == latest.assessed_at

    def test_first_time_user_always_due(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest_assessment.return_value = None

        result = service.is_self_assessment_due(user_id=1)

        assert result.is_due is True
        assert result.last_assessed_at is None

    def test_prompt_due_at_exactly_7_days(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        latest = MagicMock(spec=SelfAssessmentRecord)
        latest.assessed_at = datetime.now(timezone.utc) - timedelta(days=7)
        mock_readiness_repo.get_latest_assessment.return_value = latest

        result = service.is_self_assessment_due(user_id=1)

        assert result.is_due is True


class TestServiceNoScoreHistory:
    """Service handles user with no readiness score history."""

    def test_uses_zero_computed_score_when_no_history(
        self, service: ReadinessService, mock_readiness_repo: MagicMock
    ) -> None:
        mock_readiness_repo.get_latest.return_value = None
        mock_readiness_repo.create_self_assessment.side_effect = lambda x: x

        result = service.submit_self_assessment(user_id=1, self_assessed_score=50)

        assert result.computed_score == 0
        assert result.delta == 50
        assert result.calibration_status == "overconfident"


# ===========================================================================
# Router Tests — Mocked Service, HTTP Client
# ===========================================================================


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=ReadinessService)


@pytest.fixture
def authed_user() -> User:
    return _make_user_obj()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(readiness_router)

    fastapi_app.dependency_overrides[get_readiness_service] = lambda: mock_service
    fastapi_app.dependency_overrides[get_current_user] = lambda: authed_user

    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


class TestRouterSubmitHappyPath:
    """POST /v1/readiness/self-assessment happy path."""

    def test_submit_returns_200_with_calibration(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.submit_self_assessment.return_value = SelfAssessmentResponse(
            self_assessed_score=70,
            computed_score=60,
            delta=10,
            calibration_status="well_calibrated",
            message="Your self-assessment closely matches your computed readiness.",
            calibration_warning=None,
        )

        response = client.post(
            "/v1/readiness/self-assessment",
            json={"self_assessed_score": 70},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["self_assessed_score"] == 70
        assert data["computed_score"] == 60
        assert data["delta"] == 10
        assert data["calibration_status"] == "well_calibrated"
        assert data["calibration_warning"] is None

    def test_submit_overconfident_includes_warning(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.submit_self_assessment.return_value = SelfAssessmentResponse(
            self_assessed_score=90,
            computed_score=60,
            delta=30,
            calibration_status="overconfident",
            message="Your self-assessment is 30 points above your computed readiness.",
            calibration_warning="You overestimate your readiness by 30 points.",
        )

        response = client.post(
            "/v1/readiness/self-assessment",
            json={"self_assessed_score": 90},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["calibration_status"] == "overconfident"
        assert data["calibration_warning"] is not None


class TestRouterSubmitValidation:
    """POST /v1/readiness/self-assessment validation errors."""

    def test_score_below_zero_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/v1/readiness/self-assessment",
            json={"self_assessed_score": -1},
        )
        assert response.status_code == 422

    def test_score_above_100_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/v1/readiness/self-assessment",
            json={"self_assessed_score": 101},
        )
        assert response.status_code == 422

    def test_missing_score_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/v1/readiness/self-assessment",
            json={},
        )
        assert response.status_code == 422

    def test_non_integer_score_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/v1/readiness/self-assessment",
            json={"self_assessed_score": "abc"},
        )
        assert response.status_code == 422


class TestRouterHistory:
    """GET /v1/readiness/self-assessment/history endpoint."""

    def test_returns_200_with_history(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.get_self_assessment_history.return_value = (
            SelfAssessmentHistoryResponse(
                records=[
                    {
                        "self_assessed_score": 70,
                        "computed_score": 60,
                        "delta": 10,
                        "calibration_status": "well_calibrated",
                        "assessed_at": "2024-06-10T14:00:00+00:00",
                    }
                ]
            )
        )

        response = client.get("/v1/readiness/self-assessment/history")

        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert len(data["records"]) == 1
        assert data["records"][0]["calibration_status"] == "well_calibrated"

    def test_returns_empty_records_for_new_user(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.get_self_assessment_history.return_value = (
            SelfAssessmentHistoryResponse(records=[])
        )

        response = client.get("/v1/readiness/self-assessment/history")

        assert response.status_code == 200
        data = response.json()
        assert data["records"] == []


class TestRouterPrompt:
    """GET /v1/readiness/self-assessment/prompt endpoint."""

    def test_returns_200_when_due(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.is_self_assessment_due.return_value = (
            SelfAssessmentPromptResponse(
                is_due=True,
                last_assessed_at=None,
            )
        )

        response = client.get("/v1/readiness/self-assessment/prompt")

        assert response.status_code == 200
        data = response.json()
        assert data["is_due"] is True
        assert data["last_assessed_at"] is None

    def test_returns_200_when_not_due(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        assessed_at = datetime.now(timezone.utc) - timedelta(days=3)
        mock_service.is_self_assessment_due.return_value = (
            SelfAssessmentPromptResponse(
                is_due=False,
                last_assessed_at=assessed_at,
            )
        )

        response = client.get("/v1/readiness/self-assessment/prompt")

        assert response.status_code == 200
        data = response.json()
        assert data["is_due"] is False
        assert data["last_assessed_at"] is not None
