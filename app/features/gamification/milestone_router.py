"""FastAPI router for competence-based milestones and study consistency.

Mounts under ``/v1`` with tag ``gamification``. Provides:

- ``GET /v1/milestones`` — all milestones with status (locked/in_progress/earned)
- ``GET /v1/milestones/unseen`` — newly awarded milestones not yet seen; marks them seen
- ``GET /v1/consistency`` — study consistency metric for the authenticated user

Validates: Requirements 13.7, 13.8, 14.4
"""

from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.gamification.consistency_service import ConsistencyService
from app.features.gamification.milestone_service import MilestoneService
from app.features.gamification.models import (
    CompetenceMilestone,
    CompetenceMilestoneAward,
    StudyConsistency,
)
from app.features.users.models import User
from app.features.xp.repository import XPRepository
from app.features.xp.service import XPService
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1", tags=["gamification"])


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class MilestoneStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    category: str
    status: str  # "locked", "in_progress", "earned"
    progress_percentage: float
    xp_reward: int
    awarded_at: datetime | None = None


class MilestonesListResponse(BaseModel):
    milestones: list[MilestoneStatusResponse]


class UnseenAwardsResponse(BaseModel):
    """Newly earned milestones the user hasn't seen yet."""
    awards: list[MilestoneStatusResponse]
    count: int


class ConsistencyMetricResponse(BaseModel):
    current_streak: int
    longest_streak: int
    total_consistent_days: int
    last_qualifying_date: str | None = None


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------


def _build_xp_service(db: Session) -> XPService:
    return XPService(xp_repo=XPRepository(db=db))


def get_milestone_service(db: Session = Depends(get_db)) -> MilestoneService:
    return MilestoneService(db=db, xp_service=_build_xp_service(db))


def get_consistency_service(db: Session = Depends(get_db)) -> ConsistencyService:
    return ConsistencyService(db=db)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/milestones", response_model=MilestonesListResponse)
def get_milestones(
    user: User = Depends(get_current_user),
    service: MilestoneService = Depends(get_milestone_service),
    db: Session = Depends(get_db),
) -> MilestonesListResponse:
    """Return all milestones with status: locked, in_progress, or earned.

    Validates: Requirement 13.7
    """
    service._ensure_milestones_seeded()

    all_milestones = db.execute(select(CompetenceMilestone)).scalars().all()

    awards_stmt = select(CompetenceMilestoneAward).where(
        CompetenceMilestoneAward.user_id == user.id
    )
    awards = db.execute(awards_stmt).scalars().all()
    awards_by_milestone: dict[int, CompetenceMilestoneAward] = {
        a.milestone_id: a for a in awards
    }

    mastery_data = service._get_mastery_data(user.id)
    score_history = service._get_score_history(user.id)
    comeback_subtopics = service._get_comeback_awarded_subtopics(user.id)

    results: list[MilestoneStatusResponse] = []

    for milestone in all_milestones:
        award = awards_by_milestone.get(milestone.id)

        if award is not None:
            results.append(
                MilestoneStatusResponse(
                    id=milestone.id,
                    slug=milestone.slug,
                    name=milestone.name,
                    description=milestone.description,
                    category=milestone.category,
                    status="earned",
                    progress_percentage=100.0,
                    xp_reward=getattr(milestone, "xp_reward", 0) or 0,
                    awarded_at=award.awarded_at,
                )
            )
        else:
            progress = _compute_progress(
                milestone, mastery_data, score_history, comeback_subtopics, service, user.id
            )
            status_label = "in_progress" if progress > 0.0 else "locked"
            results.append(
                MilestoneStatusResponse(
                    id=milestone.id,
                    slug=milestone.slug,
                    name=milestone.name,
                    description=milestone.description,
                    category=milestone.category,
                    status=status_label,
                    progress_percentage=round(progress, 1),
                    xp_reward=getattr(milestone, "xp_reward", 0) or 0,
                    awarded_at=None,
                )
            )

    return MilestonesListResponse(milestones=results)


@router.get("/milestones/unseen", response_model=UnseenAwardsResponse)
def get_unseen_milestones(
    user: User = Depends(get_current_user),
    service: MilestoneService = Depends(get_milestone_service),
    db: Session = Depends(get_db),
) -> UnseenAwardsResponse:
    """Return newly earned milestones not yet shown to the user, then mark them seen.

    Designed for the frontend to call on page load / app focus to drive
    milestone-unlock toast notifications.
    """
    unseen_awards = service.get_unseen_awards(user.id)
    db.commit()

    if not unseen_awards:
        return UnseenAwardsResponse(awards=[], count=0)

    # Fetch milestone definitions for the unseen awards
    milestone_ids = [a.milestone_id for a in unseen_awards]
    milestones_stmt = select(CompetenceMilestone).where(
        CompetenceMilestone.id.in_(milestone_ids)
    )
    milestones_by_id: dict[int, CompetenceMilestone] = {
        m.id: m for m in db.execute(milestones_stmt).scalars().all()
    }

    responses = [
        MilestoneStatusResponse(
            id=milestones_by_id[a.milestone_id].id,
            slug=milestones_by_id[a.milestone_id].slug,
            name=milestones_by_id[a.milestone_id].name,
            description=milestones_by_id[a.milestone_id].description,
            category=milestones_by_id[a.milestone_id].category,
            status="earned",
            progress_percentage=100.0,
            xp_reward=getattr(milestones_by_id[a.milestone_id], "xp_reward", 0) or 0,
            awarded_at=a.awarded_at,
        )
        for a in unseen_awards
        if a.milestone_id in milestones_by_id
    ]

    return UnseenAwardsResponse(awards=responses, count=len(responses))


@router.get("/consistency", response_model=ConsistencyMetricResponse)
def get_consistency(
    user: User = Depends(get_current_user),
    service: ConsistencyService = Depends(get_consistency_service),
) -> ConsistencyMetricResponse:
    """Return study consistency metric. Validates: Requirement 14.4"""
    record = service.get_consistency(user.id)
    return ConsistencyMetricResponse(
        current_streak=record.current_streak,
        longest_streak=record.longest_streak,
        total_consistent_days=record.total_consistent_days,
        last_qualifying_date=(
            record.last_qualifying_date.isoformat()
            if record.last_qualifying_date
            else None
        ),
    )


# ---------------------------------------------------------------------------
# Progress computation helpers
# ---------------------------------------------------------------------------


def _compute_progress(
    milestone: CompetenceMilestone,
    mastery_data: list,
    score_history: list,
    comeback_subtopics: set[int],
    service: MilestoneService,
    user_id: int,
) -> float:
    config = json.loads(milestone.threshold_config)

    if milestone.category == "mastery":
        return _compute_mastery_progress(config, mastery_data)
    elif milestone.category == "readiness":
        return _compute_readiness_progress(config, score_history)
    elif milestone.category == "recovery":
        return _compute_recovery_progress(milestone.slug, config, comeback_subtopics)
    elif milestone.category == "subtest":
        return _compute_subtest_progress(config, service, user_id)
    return 0.0


def _compute_mastery_progress(config: dict, mastery_data: list) -> float:
    module_slug: str | None = config.get("module_slug")
    required_count: int = config.get("required_count", 1)
    threshold: float = config.get("threshold", 0.8)

    relevant = (
        [m for m in mastery_data if m.module_slug == module_slug]
        if module_slug is not None
        else list(mastery_data)
    )
    qualifying = [m for m in relevant if m.mastery_score >= threshold]
    progress = (len(qualifying) / required_count) * 100.0 if required_count > 0 else 0.0
    return min(progress, 100.0)


def _compute_readiness_progress(config: dict, score_history: list) -> float:
    from datetime import date as date_type

    min_score: int = config.get("min_score", 70)
    consecutive_days: int = config.get("consecutive_days", 7)

    if not score_history:
        return 0.0

    daily_scores: dict[date_type, int] = {}
    for point in score_history:
        daily_scores[point.computed_date] = point.score

    qualifying_dates = sorted(
        d for d, s in daily_scores.items() if s >= min_score
    )
    if not qualifying_dates:
        return 0.0

    max_consecutive = current_consecutive = 1
    for i in range(1, len(qualifying_dates)):
        if (qualifying_dates[i] - qualifying_dates[i - 1]).days == 1:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    max_consecutive = max(max_consecutive, current_consecutive)
    return min((max_consecutive / consecutive_days) * 100.0, 100.0)


def _compute_recovery_progress(
    slug: str, config: dict, comeback_subtopics: set[int]
) -> float:
    if slug == "comeback":
        return 0.0  # binary — can't show partial without fine-grained history
    elif slug == "resilient-learner":
        required: int = config.get("required_comebacks", 3)
        count = len(comeback_subtopics)
        return min((count / required) * 100.0, 100.0) if required > 0 else 0.0
    return 0.0


def _compute_subtest_progress(
    config: dict, service: MilestoneService, user_id: int
) -> float:
    milestone_type: str = config.get("type", "")

    if milestone_type == "lessons_complete":
        module_slug: str = config["module_slug"]
        required_count: int = config["required_count"]
        completed = service._count_completed_lessons_for_module(user_id, module_slug)
        return min((completed / required_count) * 100.0, 100.0) if required_count > 0 else 0.0

    elif milestone_type == "subtest_exam_pass":
        # Binary — either passed or not
        module_slug = config["module_slug"]
        pass_threshold: float = config["pass_threshold"]
        passed = service._has_passed_subtest_exam(user_id, module_slug, pass_threshold)
        return 100.0 if passed else 0.0

    elif milestone_type == "all_subtests_passed":
        passed = service._all_subtest_champions_earned(user_id)
        return 100.0 if passed else 0.0

    return 0.0
