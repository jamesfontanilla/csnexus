"""Onboarding service — exam date capture, plan generation, and updates.

Orchestrates the onboarding flow: validates user input, creates an
OnboardingProfile, generates a personalized StudyPlan via the plan
generator algorithm, and handles exam date updates with plan regeneration.

Requirements: 16.1–16.6, 17.1, 17.4, 18.1–18.5
"""

from __future__ import annotations

import json
from datetime import date
from dataclasses import asdict

from fastapi import HTTPException, status

from app.features.content.repository import SubtopicRepository
from app.features.mastery.repository import MasteryRepository
from app.features.planner.algorithms.plan_generator import (
    ExamDateValidationError,
    GeneratedPlan,
    PlanConfig,
    generate_study_plan,
    regenerate_plan_from_today,
    validate_exam_date,
)
from app.features.planner.models import OnboardingProfile, StudyPlan
from app.features.planner.repository import (
    OnboardingRepository,
    StudyPlanRepository,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TIME_BUDGET_TO_HOURS: dict[int, float] = {
    15: 0.25,
    30: 0.5,
    60: 1.0,
}

_VALID_CATEGORIES = ("Professional", "Sub-Professional")
_VALID_TIME_BUDGETS = (15, 30, 60)


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class OnboardingService:
    """Handles exam date onboarding, plan generation, and exam date updates.

    Constructor injection: receives planner repository, mastery repository,
    and content repository.
    """

    def __init__(
        self,
        *,
        onboarding_repo: OnboardingRepository,
        plan_repo: StudyPlanRepository,
        mastery_repo: MasteryRepository,
        content_repo: SubtopicRepository,
    ) -> None:
        self._onboarding_repo = onboarding_repo
        self._plan_repo = plan_repo
        self._mastery_repo = mastery_repo
        self._content_repo = content_repo

    # -------------------------------------------------------------------
    # Submit onboarding
    # -------------------------------------------------------------------

    def submit_onboarding(
        self,
        user_id: int,
        *,
        exam_date: date,
        exam_category: str,
        time_budget_minutes: int = 30,
    ) -> dict:
        """Validate onboarding input, create profile, generate plan.

        Returns a dict with confirmation data and optional warning.

        Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6
        """
        # --- Validation ---
        self._validate_exam_category(exam_category)
        self._validate_time_budget(time_budget_minutes)

        today = date.today()
        try:
            days_until_exam = validate_exam_date(exam_date, today)
        except ExamDateValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            ) from e

        # --- Check for existing profile (idempotent — update if exists) ---
        existing_profile = self._onboarding_repo.get_profile(user_id)
        if existing_profile is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Onboarding already completed. Use PATCH /onboarding/exam-date to update.",
            )

        # --- Create OnboardingProfile ---
        profile = OnboardingProfile(
            user_id=user_id,
            exam_date=exam_date,
            exam_category=exam_category,
            time_budget_minutes=time_budget_minutes,
        )
        self._onboarding_repo.create_profile(profile)

        # --- Generate study plan ---
        generated_plan = self._generate_plan(
            user_id=user_id,
            exam_date=exam_date,
            exam_category=exam_category,
            time_budget_minutes=time_budget_minutes,
            today=today,
        )

        # --- Persist StudyPlan record ---
        self._persist_study_plan(
            user_id=user_id,
            exam_date=exam_date,
            exam_category=exam_category,
            time_budget_minutes=time_budget_minutes,
            generated_plan=generated_plan,
        )

        # --- Build response ---
        warning = None
        if days_until_exam < 7:
            warning = (
                "Your exam is in fewer than 7 days. "
                "The study plan will be compressed to fit the available time."
            )

        return {
            "status": "completed",
            "total_days": generated_plan.total_days,
            "subtopics_per_week": generated_plan.subtopics_per_week,
            "mock_exams_scheduled": generated_plan.mock_exams_scheduled,
            "estimated_readiness_at_exam": generated_plan.estimated_readiness_at_exam,
            "warning": warning,
        }

    # -------------------------------------------------------------------
    # Skip onboarding
    # -------------------------------------------------------------------

    def skip_onboarding(self, user_id: int) -> dict:
        """Allow dashboard access without onboarding, persist prompt flag.

        Requirements: 16.5
        """
        # We don't create a profile — the absence of a profile IS the
        # skip signal. The router/dashboard checks for profile existence.
        return {
            "status": "skipped",
            "show_onboarding_prompt": True,
        }

    # -------------------------------------------------------------------
    # Update exam date
    # -------------------------------------------------------------------

    def update_exam_date(self, user_id: int, *, new_exam_date: date) -> dict:
        """Regenerate plan with new exam date, recalculate urgency.

        Requirements: 18.1, 18.2, 18.3, 18.4, 18.5
        """
        today = date.today()

        # Validate new date
        try:
            days_until_exam = validate_exam_date(new_exam_date, today)
        except ExamDateValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            ) from e

        # Get existing profile
        profile = self._onboarding_repo.get_profile(user_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No onboarding profile found. Complete onboarding first.",
            )

        # Update profile exam date
        self._onboarding_repo.update_exam_date(user_id, new_exam_date)

        # Get existing plan to determine completed days
        existing_plan_record = self._plan_repo.get_active_plan(user_id)
        completed_days = 0
        if existing_plan_record and existing_plan_record.plan_data:
            # Count completed days from plan_data
            try:
                plan_data = json.loads(existing_plan_record.plan_data)
                completed_days = sum(
                    1 for day in plan_data
                    if day.get("date") and day["date"] < today.isoformat()
                )
            except (json.JSONDecodeError, TypeError):
                completed_days = 0

        # Abandon old plan if exists
        if existing_plan_record:
            self._plan_repo.abandon_plan(existing_plan_record)

        # Regenerate plan
        generated_plan = self._generate_plan(
            user_id=user_id,
            exam_date=new_exam_date,
            exam_category=profile.exam_category,
            time_budget_minutes=profile.time_budget_minutes,
            today=today,
        )

        # Persist new plan
        self._persist_study_plan(
            user_id=user_id,
            exam_date=new_exam_date,
            exam_category=profile.exam_category,
            time_budget_minutes=profile.time_budget_minutes,
            generated_plan=generated_plan,
        )

        warning = None
        if days_until_exam < 7:
            warning = (
                "Your exam is in fewer than 7 days. "
                "The study plan will be compressed to fit the available time."
            )

        return {
            "status": "updated",
            "total_days": generated_plan.total_days,
            "subtopics_per_week": generated_plan.subtopics_per_week,
            "mock_exams_scheduled": generated_plan.mock_exams_scheduled,
            "estimated_readiness_at_exam": generated_plan.estimated_readiness_at_exam,
            "warning": warning,
        }

    # -------------------------------------------------------------------
    # Get plan summary
    # -------------------------------------------------------------------

    def get_plan_summary(self, user_id: int) -> dict:
        """Return plan summary for the user.

        Requirements: 17.4
        """
        profile = self._onboarding_repo.get_profile(user_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No onboarding profile found. Complete onboarding first.",
            )

        plan = self._plan_repo.get_active_plan(user_id)
        if plan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active study plan found.",
            )

        return {
            "total_days": plan.total_days,
            "subtopics_per_week": plan.subtopics_per_week,
            "mock_exams_scheduled": plan.mock_exams_scheduled,
            "estimated_readiness_at_exam": plan.estimated_readiness_at_exam,
            "target_exam_date": plan.target_exam_date.isoformat() if plan.target_exam_date else None,
            "exam_category": plan.exam_category,
        }

    # -------------------------------------------------------------------
    # Check if onboarding is complete
    # -------------------------------------------------------------------

    def has_completed_onboarding(self, user_id: int) -> bool:
        """Return True if user has an onboarding profile (not skipped)."""
        return self._onboarding_repo.get_profile(user_id) is not None

    # -------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------

    def _validate_exam_category(self, exam_category: str) -> None:
        """Raise 422 if category is invalid."""
        if exam_category not in _VALID_CATEGORIES:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"exam_category must be one of: {', '.join(_VALID_CATEGORIES)}"
                ),
            )

    def _validate_time_budget(self, time_budget_minutes: int) -> None:
        """Raise 422 if time budget is invalid."""
        if time_budget_minutes not in _VALID_TIME_BUDGETS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"time_budget_minutes must be one of: "
                    f"{', '.join(str(v) for v in _VALID_TIME_BUDGETS)}"
                ),
            )

    def _generate_plan(
        self,
        *,
        user_id: int,
        exam_date: date,
        exam_category: str,
        time_budget_minutes: int,
        today: date,
    ) -> GeneratedPlan:
        """Generate a study plan using the plan generator algorithm."""
        # Get all subtopic IDs
        all_subtopics = list(self._content_repo.list(skip=0, limit=1000))
        all_subtopic_ids = [s.id for s in all_subtopics]

        # Get mastered subtopics (mastery_score >= 0.8) for returning users
        mastery_rows = list(self._mastery_repo.list_by_user(user_id))
        mastered_ids = [
            m.subtopic_id
            for m in mastery_rows
            if m.mastery_score >= 0.8
        ]

        # Build config
        available_hours = _TIME_BUDGET_TO_HOURS.get(time_budget_minutes, 0.5)
        config = PlanConfig(
            target_exam_date=exam_date,
            available_hours_per_day=available_hours,
            exam_category=exam_category,
            mastered_subtopic_ids=mastered_ids,
        )

        # Generate plan (new API)
        generated_plan = generate_study_plan(
            all_subtopic_ids=all_subtopic_ids,
            config=config,
            today=today,
        )

        return generated_plan

    def _persist_study_plan(
        self,
        *,
        user_id: int,
        exam_date: date,
        exam_category: str,
        time_budget_minutes: int,
        generated_plan: GeneratedPlan,
    ) -> StudyPlan:
        """Persist a GeneratedPlan as a StudyPlan record."""
        available_hours = _TIME_BUDGET_TO_HOURS.get(time_budget_minutes, 0.5)

        # Serialize assignments to JSON
        plan_data_json = json.dumps([
            {
                "day_number": a.day_number,
                "date": a.date.isoformat(),
                "phase": a.phase,
                "new_subtopics": a.new_subtopics,
                "review_subtopics": a.review_subtopics,
                "mock_exam_scheduled": a.mock_exam_scheduled,
            }
            for a in generated_plan.assignments
        ])

        plan = StudyPlan(
            user_id=user_id,
            target_exam_date=exam_date,
            available_hours_per_day=available_hours,
            target_score=0.8,  # default target score
            status="ACTIVE",
            exam_category=exam_category,
            total_days=generated_plan.total_days,
            subtopics_per_week=generated_plan.subtopics_per_week,
            mock_exams_scheduled=generated_plan.mock_exams_scheduled,
            plan_data=plan_data_json,
            estimated_readiness_at_exam=generated_plan.estimated_readiness_at_exam,
        )
        return self._plan_repo.create(plan)
