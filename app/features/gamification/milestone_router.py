"""FastAPI router for competence-based milestones and study consistency.

Mounts under ``/v1`` with tag ``gamification``. Provides:

- ``GET /v1/milestones`` — all milestones with status (locked/in_progress/earned)
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
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1", tags=["gamification"])


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class MilestoneStatusResponse(BaseModel):
    """A single milestone with its current status for the user."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str
    category: str
    status: str  # "locked", "in_progress", "earned"
    progress_percentage: float  # 0.0 to 100.0
    awarded_at: datetime | None = None


class MilestonesListResponse(BaseModel):
    """All milestones with their statuses."""

    milestones: list[MilestoneStatusResponse]


class ConsistencyMetricResponse(BaseModel):
    """Study consistency metric for the authenticated user."""

    current_streak: int
    longest_streak: int
    total_consistent_days: int
    last_qualifying_date: str | None = None


# ---------------------------------------------------------------------------
# Dependency factories
# ---------------------------------------------------------------------------


def get_milestone_service(db: Session = Depends(get_db)) -> MilestoneService:
    """Construct MilestoneService with DB session."""
    return MilestoneService(db=db)


def get_consistency_service(db: Session = Depends(get_db)) -> ConsistencyService:
    """Construct ConsistencyService with DB session."""
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

    Progress percentage is computed as:
    - Mastery milestones: qualifying subtopics / required count
    - Readiness milestones: consecutive qualifying days / 7
    - Recovery milestones (Comeback): 0 or 100
    - Recovery milestones (Resilient Learner): comeback count / 3

    Validates: Requirement 13.7
    """
    # Ensure milestone definitions exist
    service._ensure_milestones_seeded()

    # Fetch all milestone definitions
    all_milestones = db.execute(select(CompetenceMilestone)).scalars().all()

    # Fetch user's awards
    awards_stmt = select(CompetenceMilestoneAward).where(
        CompetenceMilestoneAward.user_id == user.id
    )
    awards = db.execute(awards_stmt).scalars().all()
    awards_by_milestone: dict[int, CompetenceMilestoneAward] = {
        a.milestone_id: a for a in awards
    }

    # Gather user data for progress computation
    mastery_data = service._get_mastery_data(user.id)
    score_history = service._get_score_history(user.id)
    comeback_subtopics = service._get_comeback_awarded_subtopics(user.id)

    results: list[MilestoneStatusResponse] = []

    for milestone in all_milestones:
        award = awards_by_milestone.get(milestone.id)

        if award is not None:
            # Earned
            results.append(
                MilestoneStatusResponse(
                    id=milestone.id,
                    slug=milestone.slug,
                    name=milestone.name,
                    description=milestone.description,
                    category=milestone.category,
                    status="earned",
                    progress_percentage=100.0,
                    awarded_at=award.awarded_at,
                )
            )
        else:
            # Compute progress
            progress = _compute_progress(
                milestone, mastery_data, score_history, comeback_subtopics
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
                    awarded_at=None,
                )
            )

    return MilestonesListResponse(milestones=results)


@router.get("/consistency", response_model=ConsistencyMetricResponse)
def get_consistency(
    user: User = Depends(get_current_user),
    service: ConsistencyService = Depends(get_consistency_service),
) -> ConsistencyMetricResponse:
    """Return study consistency metric for the authenticated user.

    Validates: Requirement 14.4
    """
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
) -> float:
    """Compute progress percentage for an unearned milestone.

    Returns a value from 0.0 to 100.0 (capped, never exceeds 100).

    - Mastery milestones: (qualifying count / required count) * 100
    - Readiness milestones: (max consecutive qualifying days / 7) * 100
    - Recovery (Comeback): 0 (binary — either earned or not)
    - Recovery (Resilient Learner): (comeback awards / 3) * 100
    """
    config = json.loads(milestone.threshold_config)

    if milestone.category == "mastery":
        return _compute_mastery_progress(config, mastery_data)
    elif milestone.category == "readiness":
        return _compute_readiness_progress(config, score_history)
    elif milestone.category == "recovery":
        return _compute_recovery_progress(milestone.slug, config, comeback_subtopics)
    return 0.0


def _compute_mastery_progress(config: dict, mastery_data: list) -> float:
    """Mastery: qualifying subtopics / required count * 100."""
    module_slug: str | None = config.get("module_slug")
    required_count: int = config.get("required_count", 1)
    threshold: float = config.get("threshold", 0.8)

    if module_slug is not None:
        relevant = [m for m in mastery_data if m.module_slug == module_slug]
    else:
        relevant = list(mastery_data)

    qualifying = [m for m in relevant if m.mastery_score >= threshold]
    progress = (len(qualifying) / required_count) * 100.0 if required_count > 0 else 0.0
    return min(progress, 100.0)


def _compute_readiness_progress(config: dict, score_history: list) -> float:
    """Readiness: max consecutive qualifying days / 7 * 100."""
    from datetime import date as date_type

    min_score: int = config.get("min_score", 70)
    consecutive_days: int = config.get("consecutive_days", 7)

    if not score_history:
        return 0.0

    # Build daily scores (last per day)
    daily_scores: dict[date_type, int] = {}
    for point in score_history:
        daily_scores[point.computed_date] = point.score

    if not daily_scores:
        return 0.0

    # Find max consecutive qualifying days
    qualifying_dates = sorted(
        d for d, s in daily_scores.items() if s >= min_score
    )

    if not qualifying_dates:
        return 0.0

    max_consecutive = 1
    current_consecutive = 1
    for i in range(1, len(qualifying_dates)):
        if (qualifying_dates[i] - qualifying_dates[i - 1]).days == 1:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    max_consecutive = max(max_consecutive, current_consecutive)
    progress = (max_consecutive / consecutive_days) * 100.0
    return min(progress, 100.0)


def _compute_recovery_progress(
    slug: str, config: dict, comeback_subtopics: set[int]
) -> float:
    """Recovery progress.

    - Comeback: binary (0 or 100, but if unearned always 0 since we can't
      partially detect a recovery in progress without historical snapshots).
    - Resilient Learner: comeback_count / required_comebacks * 100
    """
    if slug == "comeback":
        # Comeback is binary — either you've recovered a subtopic or not.
        # Without fine-grained history, partial progress isn't meaningful.
        return 0.0
    elif slug == "resilient-learner":
        required: int = config.get("required_comebacks", 3)
        count = len(comeback_subtopics)
        if required <= 0:
            return 0.0
        progress = (count / required) * 100.0
        return min(progress, 100.0)
    return 0.0
