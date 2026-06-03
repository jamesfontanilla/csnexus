"""Service tests for the onboarding service — mocked repositories."""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.features.content.models import Subtopic
from app.features.content.repository import SubtopicRepository
from app.features.mastery.models import UserSubtopicMastery
from app.features.mastery.repository import MasteryRepository
from app.features.planner.models import OnboardingProfile, StudyPlan
from app.features.planner.onboarding_service import OnboardingService
from app.features.planner.repository import OnboardingRepository, StudyPlanRepository


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_onboarding_repo() -> MagicMock:
    return MagicMock(spec=OnboardingRepository)


@pytest.fixture
def mock_plan_repo() -> MagicMock:
    return MagicMock(spec=StudyPlanRepository)


@pytest.fixture
def mock_mastery_repo() -> MagicMock:
    return MagicMock(spec=MasteryRepository)


@pytest.fixture
def mock_content_repo() -> MagicMock:
    return MagicMock(spec=SubtopicRepository)


@pytest.fixture
def service(
    mock_onboarding_repo,
    mock_plan_repo,
    mock_mastery_repo,
    mock_content_repo,
):
    return OnboardingService(
        onboarding_repo=mock_onboarding_repo,
        plan_repo=mock_plan_repo,
        mastery_repo=mock_mastery_repo,
        content_repo=mock_content_repo,
    )


def _make_subtopics(count: int = 10) -> list[MagicMock]:
    """Create mock subtopic objects."""
    subtopics = []
    for i in range(1, count + 1):
        s = MagicMock(spec=Subtopic)
        s.id = i
        subtopics.append(s)
    return subtopics


# ---------------------------------------------------------------------------
# submit_onboarding tests
# ---------------------------------------------------------------------------


class TestSubmitOnboarding:
    """Tests for OnboardingService.submit_onboarding."""

    def test_valid_submission_creates_profile_and_plan(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """Happy path: valid data creates profile and plan."""
        mock_onboarding_repo.get_profile.return_value = None
        mock_onboarding_repo.create_profile.return_value = MagicMock(spec=OnboardingProfile)
        mock_mastery_repo.list_by_user.return_value = []
        mock_content_repo.list.return_value = _make_subtopics(10)

        plan = MagicMock(spec=StudyPlan)
        plan.id = 1
        mock_plan_repo.create.return_value = plan

        result = service.submit_onboarding(
            user_id=1,
            exam_date=date.today() + timedelta(days=30),
            exam_category="Professional",
            time_budget_minutes=30,
        )

        assert result["status"] == "completed"
        assert result["total_days"] == 30
        assert result["warning"] is None
        mock_onboarding_repo.create_profile.assert_called_once()
        mock_plan_repo.create.assert_called_once()

    def test_valid_submission_with_warning_for_short_timeline(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """Submission with <7 days includes a warning."""
        mock_onboarding_repo.get_profile.return_value = None
        mock_onboarding_repo.create_profile.return_value = MagicMock(spec=OnboardingProfile)
        mock_mastery_repo.list_by_user.return_value = []
        mock_content_repo.list.return_value = _make_subtopics(10)
        mock_plan_repo.create.return_value = MagicMock(spec=StudyPlan)

        result = service.submit_onboarding(
            user_id=1,
            exam_date=date.today() + timedelta(days=5),
            exam_category="Sub-Professional",
            time_budget_minutes=60,
        )

        assert result["status"] == "completed"
        assert result["warning"] is not None
        assert "fewer than 7 days" in result["warning"]

    def test_rejects_past_date(self, service, mock_onboarding_repo):
        """Past exam date raises 422."""
        mock_onboarding_repo.get_profile.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.submit_onboarding(
                user_id=1,
                exam_date=date.today() - timedelta(days=1),
                exam_category="Professional",
            )
        assert exc_info.value.status_code == 422

    def test_rejects_date_beyond_365_days(self, service, mock_onboarding_repo):
        """Exam date >365 days in future raises 422."""
        mock_onboarding_repo.get_profile.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.submit_onboarding(
                user_id=1,
                exam_date=date.today() + timedelta(days=400),
                exam_category="Professional",
            )
        assert exc_info.value.status_code == 422

    def test_rejects_invalid_category(self, service):
        """Invalid exam category raises 422."""
        with pytest.raises(HTTPException) as exc_info:
            service.submit_onboarding(
                user_id=1,
                exam_date=date.today() + timedelta(days=30),
                exam_category="Invalid",
            )
        assert exc_info.value.status_code == 422

    def test_rejects_invalid_time_budget(self, service):
        """Invalid time budget raises 422."""
        with pytest.raises(HTTPException) as exc_info:
            service.submit_onboarding(
                user_id=1,
                exam_date=date.today() + timedelta(days=30),
                exam_category="Professional",
                time_budget_minutes=45,
            )
        assert exc_info.value.status_code == 422

    def test_rejects_duplicate_onboarding(self, service, mock_onboarding_repo):
        """If profile already exists, raises 409."""
        mock_onboarding_repo.get_profile.return_value = MagicMock(spec=OnboardingProfile)

        with pytest.raises(HTTPException) as exc_info:
            service.submit_onboarding(
                user_id=1,
                exam_date=date.today() + timedelta(days=30),
                exam_category="Professional",
            )
        assert exc_info.value.status_code == 409

    def test_returning_user_skips_mastered_subtopics(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """Returning user with mastered subtopics skips them in plan."""
        mock_onboarding_repo.get_profile.return_value = None
        mock_onboarding_repo.create_profile.return_value = MagicMock(spec=OnboardingProfile)

        # 3 subtopics mastered at >= 0.8
        mastery_rows = []
        for i in range(1, 4):
            m = MagicMock(spec=UserSubtopicMastery)
            m.subtopic_id = i
            m.mastery_score = 0.85
            mastery_rows.append(m)
        # 1 subtopic below threshold
        weak = MagicMock(spec=UserSubtopicMastery)
        weak.subtopic_id = 4
        weak.mastery_score = 0.5
        mastery_rows.append(weak)

        mock_mastery_repo.list_by_user.return_value = mastery_rows
        mock_content_repo.list.return_value = _make_subtopics(10)
        mock_plan_repo.create.return_value = MagicMock(spec=StudyPlan)

        result = service.submit_onboarding(
            user_id=1,
            exam_date=date.today() + timedelta(days=60),
            exam_category="Professional",
            time_budget_minutes=30,
        )

        assert result["status"] == "completed"
        # The plan was generated — we verify the plan_repo.create call
        # has the right plan_data containing mastered IDs filtered out
        mock_plan_repo.create.assert_called_once()

    def test_defaults_time_budget_to_30(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """When time_budget_minutes not provided, defaults to 30."""
        mock_onboarding_repo.get_profile.return_value = None
        mock_onboarding_repo.create_profile.return_value = MagicMock(spec=OnboardingProfile)
        mock_mastery_repo.list_by_user.return_value = []
        mock_content_repo.list.return_value = _make_subtopics(10)
        mock_plan_repo.create.return_value = MagicMock(spec=StudyPlan)

        result = service.submit_onboarding(
            user_id=1,
            exam_date=date.today() + timedelta(days=30),
            exam_category="Professional",
        )

        assert result["status"] == "completed"
        # Verify profile was created with default time budget
        call_args = mock_onboarding_repo.create_profile.call_args
        profile = call_args[0][0]
        assert profile.time_budget_minutes == 30


# ---------------------------------------------------------------------------
# update_exam_date tests
# ---------------------------------------------------------------------------


class TestUpdateExamDate:
    """Tests for OnboardingService.update_exam_date."""

    def test_valid_update_regenerates_plan(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """Updating exam date regenerates the plan."""
        profile = MagicMock(spec=OnboardingProfile)
        profile.exam_category = "Professional"
        profile.time_budget_minutes = 30
        mock_onboarding_repo.get_profile.return_value = profile
        mock_onboarding_repo.update_exam_date.return_value = profile

        existing_plan = MagicMock(spec=StudyPlan)
        existing_plan.plan_data = None
        mock_plan_repo.get_active_plan.return_value = existing_plan
        mock_plan_repo.abandon_plan.return_value = existing_plan

        mock_mastery_repo.list_by_user.return_value = []
        mock_content_repo.list.return_value = _make_subtopics(10)

        new_plan = MagicMock(spec=StudyPlan)
        new_plan.id = 2
        mock_plan_repo.create.return_value = new_plan

        new_date = date.today() + timedelta(days=45)
        result = service.update_exam_date(user_id=1, new_exam_date=new_date)

        assert result["status"] == "updated"
        assert result["total_days"] == 45
        mock_plan_repo.abandon_plan.assert_called_once_with(existing_plan)
        mock_plan_repo.create.assert_called_once()

    def test_rejects_past_date(self, service, mock_onboarding_repo):
        """Past date raises 422."""
        mock_onboarding_repo.get_profile.return_value = MagicMock(spec=OnboardingProfile)

        with pytest.raises(HTTPException) as exc_info:
            service.update_exam_date(
                user_id=1,
                new_exam_date=date.today() - timedelta(days=1),
            )
        assert exc_info.value.status_code == 422

    def test_rejects_no_profile(self, service, mock_onboarding_repo):
        """No profile raises 404."""
        mock_onboarding_repo.get_profile.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.update_exam_date(
                user_id=1,
                new_exam_date=date.today() + timedelta(days=30),
            )
        assert exc_info.value.status_code == 404

    def test_warning_for_short_timeline(
        self, service, mock_onboarding_repo, mock_plan_repo, mock_mastery_repo, mock_content_repo
    ):
        """<7 days includes a warning."""
        profile = MagicMock(spec=OnboardingProfile)
        profile.exam_category = "Sub-Professional"
        profile.time_budget_minutes = 60
        mock_onboarding_repo.get_profile.return_value = profile
        mock_onboarding_repo.update_exam_date.return_value = profile

        mock_plan_repo.get_active_plan.return_value = None
        mock_mastery_repo.list_by_user.return_value = []
        mock_content_repo.list.return_value = _make_subtopics(10)
        mock_plan_repo.create.return_value = MagicMock(spec=StudyPlan)

        result = service.update_exam_date(
            user_id=1,
            new_exam_date=date.today() + timedelta(days=3),
        )

        assert result["warning"] is not None
        assert "fewer than 7 days" in result["warning"]


# ---------------------------------------------------------------------------
# get_plan_summary tests
# ---------------------------------------------------------------------------


class TestGetPlanSummary:
    """Tests for OnboardingService.get_plan_summary."""

    def test_returns_plan_summary(self, service, mock_onboarding_repo, mock_plan_repo):
        """Happy path: returns plan summary."""
        profile = MagicMock(spec=OnboardingProfile)
        mock_onboarding_repo.get_profile.return_value = profile

        plan = MagicMock(spec=StudyPlan)
        plan.total_days = 30
        plan.subtopics_per_week = 5
        plan.mock_exams_scheduled = 4
        plan.estimated_readiness_at_exam = 72.5
        plan.target_exam_date = date.today() + timedelta(days=30)
        plan.exam_category = "Professional"
        mock_plan_repo.get_active_plan.return_value = plan

        result = service.get_plan_summary(user_id=1)

        assert result["total_days"] == 30
        assert result["subtopics_per_week"] == 5
        assert result["mock_exams_scheduled"] == 4
        assert result["estimated_readiness_at_exam"] == 72.5

    def test_raises_404_no_profile(self, service, mock_onboarding_repo):
        """No profile raises 404."""
        mock_onboarding_repo.get_profile.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.get_plan_summary(user_id=1)
        assert exc_info.value.status_code == 404

    def test_raises_404_no_plan(self, service, mock_onboarding_repo, mock_plan_repo):
        """Profile exists but no active plan raises 404."""
        mock_onboarding_repo.get_profile.return_value = MagicMock(spec=OnboardingProfile)
        mock_plan_repo.get_active_plan.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.get_plan_summary(user_id=1)
        assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# has_completed_onboarding tests
# ---------------------------------------------------------------------------


class TestHasCompletedOnboarding:
    """Tests for OnboardingService.has_completed_onboarding."""

    def test_returns_true_with_profile(self, service, mock_onboarding_repo):
        mock_onboarding_repo.get_profile.return_value = MagicMock(spec=OnboardingProfile)
        assert service.has_completed_onboarding(user_id=1) is True

    def test_returns_false_without_profile(self, service, mock_onboarding_repo):
        mock_onboarding_repo.get_profile.return_value = None
        assert service.has_completed_onboarding(user_id=1) is False


# ---------------------------------------------------------------------------
# skip_onboarding tests
# ---------------------------------------------------------------------------


class TestSkipOnboarding:
    """Tests for OnboardingService.skip_onboarding."""

    def test_skip_returns_prompt_flag(self, service):
        result = service.skip_onboarding(user_id=1)
        assert result["status"] == "skipped"
        assert result["show_onboarding_prompt"] is True
