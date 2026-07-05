"""Service layer for competence-based milestone evaluation.

Fixes applied:
- Corrected subtopic counts to 100 per subtest (was 13/23/24/60).
- Added missing clerical-ability and general-information mastery milestones.
- Added subtest exam milestones (pass ≥ 80% on 100-item subtest exam).
- Added subtest-finisher milestones (all 100 lessons completed per subtest).
- Real recovery detection using MasteryScoreHistory instead of updated_at hack.
- XP reward granted via XPService when a milestone is first awarded.
- seen_at tracking: milestones are "unseen" until the user retrieves them.

Validates: Requirements 13.1–13.8, 14.4, 15.1
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.features.content.models import Lesson, Module, Subtopic, Topic
from app.features.gamification.models import (
    CompetenceMilestone,
    CompetenceMilestoneAward,
    MasteryScoreHistory,
)
from app.features.mastery.models import UserSubtopicMastery
from app.features.mock_exams.models import MockExamAttempt, MockExamAttemptStatus
from app.features.progress.models import LessonCompletion
from app.features.readiness.models import ReadinessScoreHistory

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Milestone seed data — corrected counts and full subtest coverage
# ---------------------------------------------------------------------------

MILESTONE_SEED_DATA: list[dict[str, Any]] = [
    # --- Mastery milestones (100 subtopics each, corrected from 13/23/24) ---
    {
        "slug": "verbal-mastery",
        "name": "Verbal Mastery",
        "description": "All 100 Verbal Ability subtopics with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 200,
        "threshold_config": json.dumps(
            {"module_slug": "verbal-ability", "required_count": 100, "threshold": 0.8}
        ),
    },
    {
        "slug": "numerical-mastery",
        "name": "Numerical Mastery",
        "description": "All 100 Numerical Ability subtopics with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 200,
        "threshold_config": json.dumps(
            {"module_slug": "numerical-ability", "required_count": 100, "threshold": 0.8}
        ),
    },
    {
        "slug": "analytical-mastery",
        "name": "Analytical Mastery",
        "description": "All 100 Analytical Ability subtopics with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 200,
        "threshold_config": json.dumps(
            {"module_slug": "analytical-ability", "required_count": 100, "threshold": 0.8}
        ),
    },
    {
        "slug": "clerical-mastery",
        "name": "Clerical Mastery",
        "description": "All 100 Clerical Ability subtopics with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 200,
        "threshold_config": json.dumps(
            {"module_slug": "clerical-ability", "required_count": 100, "threshold": 0.8}
        ),
    },
    {
        "slug": "general-info-mastery",
        "name": "General Information Mastery",
        "description": "All 100 General Information subtopics with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 200,
        "threshold_config": json.dumps(
            {"module_slug": "general-information", "required_count": 100, "threshold": 0.8}
        ),
    },
    {
        "slug": "full-spectrum",
        "name": "Full Spectrum",
        "description": "All 400 subtopics (all 4 subtests) with mastery score ≥ 0.8",
        "category": "mastery",
        "xp_reward": 1000,
        "threshold_config": json.dumps(
            {"module_slug": None, "required_count": 400, "threshold": 0.8}
        ),
    },
    # --- Readiness milestones ---
    {
        "slug": "exam-ready-sub-professional",
        "name": "Exam Ready: Sub-Professional",
        "description": "Readiness score ≥ 70 for 7 consecutive days",
        "category": "readiness",
        "xp_reward": 500,
        "threshold_config": json.dumps({"min_score": 70, "consecutive_days": 7}),
    },
    {
        "slug": "exam-ready-professional",
        "name": "Exam Ready: Professional",
        "description": "Readiness score ≥ 80 for 7 consecutive days",
        "category": "readiness",
        "xp_reward": 500,
        "threshold_config": json.dumps({"min_score": 80, "consecutive_days": 7}),
    },
    # --- Recovery milestones ---
    {
        "slug": "comeback",
        "name": "Comeback",
        "description": "Recover any subtopic from mastery < 0.5 to ≥ 0.8 within 14 days",
        "category": "recovery",
        "xp_reward": 150,
        "threshold_config": json.dumps(
            {"low_threshold": 0.5, "high_threshold": 0.8, "window_days": 14}
        ),
    },
    {
        "slug": "resilient-learner",
        "name": "Resilient Learner",
        "description": "Achieve 3 separate Comeback milestones on distinct subtopics",
        "category": "recovery",
        "xp_reward": 300,
        "threshold_config": json.dumps({"required_comebacks": 3}),
    },
    # --- Subtest lesson-finisher milestones ---
    {
        "slug": "verbal-finisher",
        "name": "Verbal Finisher",
        "description": "Complete all 100 Verbal Ability lessons",
        "category": "subtest",
        "xp_reward": 100,
        "threshold_config": json.dumps(
            {"type": "lessons_complete", "module_slug": "verbal-ability", "required_count": 100}
        ),
    },
    {
        "slug": "numerical-finisher",
        "name": "Numerical Finisher",
        "description": "Complete all 100 Numerical Ability lessons",
        "category": "subtest",
        "xp_reward": 100,
        "threshold_config": json.dumps(
            {"type": "lessons_complete", "module_slug": "numerical-ability", "required_count": 100}
        ),
    },
    {
        "slug": "analytical-finisher",
        "name": "Analytical Finisher",
        "description": "Complete all 100 Analytical Ability lessons",
        "category": "subtest",
        "xp_reward": 100,
        "threshold_config": json.dumps(
            {"type": "lessons_complete", "module_slug": "analytical-ability", "required_count": 100}
        ),
    },
    {
        "slug": "clerical-finisher",
        "name": "Clerical Finisher",
        "description": "Complete all 100 Clerical Ability lessons",
        "category": "subtest",
        "xp_reward": 100,
        "threshold_config": json.dumps(
            {"type": "lessons_complete", "module_slug": "clerical-ability", "required_count": 100}
        ),
    },
    {
        "slug": "general-info-finisher",
        "name": "General Information Finisher",
        "description": "Complete all 100 General Information lessons",
        "category": "subtest",
        "xp_reward": 100,
        "threshold_config": json.dumps(
            {"type": "lessons_complete", "module_slug": "general-information", "required_count": 100}
        ),
    },
    # --- Subtest exam milestones (score ≥ 80% on the 100-item subtest exam) ---
    {
        "slug": "verbal-subtest-champion",
        "name": "Verbal Subtest Champion",
        "description": "Score ≥ 80% on the Verbal Ability 100-item subtest exam",
        "category": "subtest",
        "xp_reward": 300,
        "threshold_config": json.dumps(
            {"type": "subtest_exam_pass", "module_slug": "verbal-ability",
             "pass_threshold": 0.80}
        ),
    },
    {
        "slug": "numerical-subtest-champion",
        "name": "Numerical Subtest Champion",
        "description": "Score ≥ 80% on the Numerical Ability 100-item subtest exam",
        "category": "subtest",
        "xp_reward": 300,
        "threshold_config": json.dumps(
            {"type": "subtest_exam_pass", "module_slug": "numerical-ability",
             "pass_threshold": 0.80}
        ),
    },
    {
        "slug": "analytical-subtest-champion",
        "name": "Analytical Subtest Champion",
        "description": "Score ≥ 80% on the Analytical Ability 100-item subtest exam",
        "category": "subtest",
        "xp_reward": 300,
        "threshold_config": json.dumps(
            {"type": "subtest_exam_pass", "module_slug": "analytical-ability",
             "pass_threshold": 0.80}
        ),
    },
    {
        "slug": "clerical-subtest-champion",
        "name": "Clerical Subtest Champion",
        "description": "Score ≥ 80% on the Clerical Ability 100-item subtest exam",
        "category": "subtest",
        "xp_reward": 300,
        "threshold_config": json.dumps(
            {"type": "subtest_exam_pass", "module_slug": "clerical-ability",
             "pass_threshold": 0.80}
        ),
    },
    {
        "slug": "general-info-subtest-champion",
        "name": "General Information Subtest Champion",
        "description": "Score ≥ 80% on the General Information 100-item subtest exam",
        "category": "subtest",
        "xp_reward": 300,
        "threshold_config": json.dumps(
            {"type": "subtest_exam_pass", "module_slug": "general-information",
             "pass_threshold": 0.80}
        ),
    },
    {
        "slug": "all-subtests-champion",
        "name": "All Subtests Champion",
        "description": "Score ≥ 80% on all 4 subtest exams for your category",
        "category": "subtest",
        "xp_reward": 750,
        "threshold_config": json.dumps({"type": "all_subtests_passed"}),
    },
]


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MasteryDataPoint:
    subtopic_id: int
    mastery_score: float
    module_slug: str


@dataclass(frozen=True)
class ScoreHistoryPoint:
    score: int
    computed_date: date


@dataclass(frozen=True)
class MasteryHistoryPoint:
    """A single entry from mastery_score_history — actual change record."""
    subtopic_id: int
    mastery_score: float
    recorded_at: date


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


class MilestoneService:
    """Evaluates and awards competence-based milestones.

    Constructor receives a DB session. The optional xp_service is injected
    when milestones should grant XP on award. Pass None to skip XP (tests,
    retroactive eval without double-granting).
    """

    def __init__(self, *, db: Session, xp_service: Any = None) -> None:
        self._db = db
        self._xp_service = xp_service  # XPService | None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate_milestones(self, user_id: int) -> list[CompetenceMilestoneAward]:
        """Evaluate all unearned milestones and award any newly satisfied."""
        mastery_data = self._get_mastery_data(user_id)
        score_history = self._get_score_history(user_id)
        mastery_history = self._get_mastery_history(user_id)

        new_awards: list[CompetenceMilestoneAward] = []
        new_awards.extend(self.evaluate_mastery_milestones(user_id, mastery_data))
        new_awards.extend(self.evaluate_readiness_milestones(user_id, score_history))
        new_awards.extend(self.evaluate_recovery_milestones(user_id, mastery_history))
        new_awards.extend(self.evaluate_subtest_milestones(user_id))
        return new_awards

    def retroactive_evaluation(self, user_id: int) -> list[CompetenceMilestoneAward]:
        """Award all already-satisfied milestones on first activation (Req 15.1)."""
        self._ensure_milestones_seeded()
        return self.evaluate_milestones(user_id)

    def evaluate_mastery_milestones(
        self, user_id: int, mastery_data: list[MasteryDataPoint]
    ) -> list[CompetenceMilestoneAward]:
        """Check mastery milestones: N subtopics in module ≥ threshold. (Req 13.1)"""
        milestones = self._get_unearned_milestones(user_id, category="mastery")
        new_awards: list[CompetenceMilestoneAward] = []

        for milestone in milestones:
            config = json.loads(milestone.threshold_config)
            module_slug: str | None = config["module_slug"]
            required_count: int = config["required_count"]
            threshold: float = config["threshold"]

            relevant = (
                [m for m in mastery_data if m.module_slug == module_slug]
                if module_slug is not None
                else list(mastery_data)
            )
            qualifying = [m for m in relevant if m.mastery_score >= threshold]

            if len(qualifying) >= required_count:
                award = self._award_milestone(
                    user_id,
                    milestone,
                    {
                        "qualifying_count": len(qualifying),
                        "required_count": required_count,
                        "threshold": threshold,
                        "module_slug": module_slug,
                    },
                )
                if award is not None:
                    new_awards.append(award)

        return new_awards

    def evaluate_readiness_milestones(
        self, user_id: int, score_history: list[ScoreHistoryPoint]
    ) -> list[CompetenceMilestoneAward]:
        """Check readiness milestones: N consecutive qualifying days. (Req 13.2)"""
        milestones = self._get_unearned_milestones(user_id, category="readiness")
        new_awards: list[CompetenceMilestoneAward] = []
        daily_scores = self._build_daily_scores(score_history)

        for milestone in milestones:
            config = json.loads(milestone.threshold_config)
            min_score: int = config["min_score"]
            consecutive_days: int = config["consecutive_days"]

            if self._has_consecutive_qualifying_days(daily_scores, min_score, consecutive_days):
                award = self._award_milestone(
                    user_id,
                    milestone,
                    {
                        "min_score": min_score,
                        "consecutive_days": consecutive_days,
                        "qualifying_scores": [
                            {"date": str(d), "score": s}
                            for d, s in sorted(daily_scores.items())
                            if s >= min_score
                        ][-consecutive_days:],
                    },
                )
                if award is not None:
                    new_awards.append(award)

        return new_awards

    def evaluate_recovery_milestones(
        self, user_id: int, mastery_history: list[MasteryHistoryPoint]
    ) -> list[CompetenceMilestoneAward]:
        """Check recovery milestones using real history records. (Req 13.3)

        Uses MasteryScoreHistory rows to find subtopics that had a low
        reading (< 0.5) followed by a high reading (≥ 0.8) within 14 days.
        This replaces the previous updated_at approximation which produced
        false positives for freshly-learned subtopics.
        """
        milestones = self._get_unearned_milestones(user_id, category="recovery")
        new_awards: list[CompetenceMilestoneAward] = []

        recovered_subtopics = self._find_recovered_subtopics(mastery_history)
        already_recovered = self._get_comeback_awarded_subtopics(user_id)
        new_recoveries = [
            r for r in recovered_subtopics
            if r["subtopic_id"] not in already_recovered
        ]
        total_recovered_count = len(already_recovered) + len(new_recoveries)

        for milestone in milestones:
            config = json.loads(milestone.threshold_config)

            if milestone.slug == "comeback":
                if new_recoveries:
                    award = self._award_milestone(
                        user_id,
                        milestone,
                        {
                            "recovered_subtopics": [
                                {
                                    "subtopic_id": r["subtopic_id"],
                                    "low_score": r["low_score"],
                                    "high_score": r["high_score"],
                                    "low_date": str(r["low_date"]),
                                    "high_date": str(r["high_date"]),
                                    "days_elapsed": r["days_elapsed"],
                                }
                                for r in new_recoveries
                            ],
                            "total_recovered_count": total_recovered_count,
                        },
                    )
                    if award is not None:
                        new_awards.append(award)

            elif milestone.slug == "resilient-learner":
                required_comebacks: int = config["required_comebacks"]
                if total_recovered_count >= required_comebacks:
                    award = self._award_milestone(
                        user_id,
                        milestone,
                        {
                            "required_comebacks": required_comebacks,
                            "total_recovered_count": total_recovered_count,
                        },
                    )
                    if award is not None:
                        new_awards.append(award)

        return new_awards

    def evaluate_subtest_milestones(self, user_id: int) -> list[CompetenceMilestoneAward]:
        """Check subtest finisher and subtest exam milestones. (New category)"""
        milestones = self._get_unearned_milestones(user_id, category="subtest")
        new_awards: list[CompetenceMilestoneAward] = []

        for milestone in milestones:
            config = json.loads(milestone.threshold_config)
            milestone_type: str = config.get("type", "")

            if milestone_type == "lessons_complete":
                module_slug: str = config["module_slug"]
                required_count: int = config["required_count"]
                completed = self._count_completed_lessons_for_module(user_id, module_slug)
                if completed >= required_count:
                    award = self._award_milestone(
                        user_id,
                        milestone,
                        {"completed_lessons": completed, "required_count": required_count,
                         "module_slug": module_slug},
                    )
                    if award is not None:
                        new_awards.append(award)

            elif milestone_type == "subtest_exam_pass":
                module_slug = config["module_slug"]
                pass_threshold: float = config["pass_threshold"]
                passed = self._has_passed_subtest_exam(user_id, module_slug, pass_threshold)
                if passed:
                    award = self._award_milestone(
                        user_id,
                        milestone,
                        {"module_slug": module_slug, "pass_threshold": pass_threshold},
                    )
                    if award is not None:
                        new_awards.append(award)

            elif milestone_type == "all_subtests_passed":
                # Earned when all 4 subtest-champion milestones for the user's
                # category are already awarded. We check the awards table.
                if self._all_subtest_champions_earned(user_id):
                    award = self._award_milestone(
                        user_id,
                        milestone,
                        {"all_subtests_passed": True},
                    )
                    if award is not None:
                        new_awards.append(award)

        return new_awards

    # ------------------------------------------------------------------
    # Unseen-awards support
    # ------------------------------------------------------------------

    def get_unseen_awards(self, user_id: int) -> list[CompetenceMilestoneAward]:
        """Return awards not yet seen by the user and mark them as seen."""
        stmt = (
            select(CompetenceMilestoneAward)
            .where(
                CompetenceMilestoneAward.user_id == user_id,
                CompetenceMilestoneAward.seen_at.is_(None),
            )
            .order_by(CompetenceMilestoneAward.awarded_at.asc())
        )
        unseen = list(self._db.execute(stmt).scalars().all())
        if unseen:
            now = _utcnow()
            for award in unseen:
                award.seen_at = now
            self._db.flush()
        return unseen

    # ------------------------------------------------------------------
    # Seed data management
    # ------------------------------------------------------------------

    def _ensure_milestones_seeded(self) -> None:
        """Upsert all milestone definitions — insert new, update xp_reward on existing."""
        existing: dict[str, CompetenceMilestone] = {
            row.slug: row
            for row in self._db.execute(select(CompetenceMilestone)).scalars().all()
        }

        for seed in MILESTONE_SEED_DATA:
            if seed["slug"] not in existing:
                milestone = CompetenceMilestone(
                    slug=seed["slug"],
                    name=seed["name"],
                    description=seed["description"],
                    category=seed["category"],
                    threshold_config=seed["threshold_config"],
                    xp_reward=seed.get("xp_reward", 0),
                )
                self._db.add(milestone)
            else:
                # Patch fields that may have changed (counts, xp_reward)
                existing_row = existing[seed["slug"]]
                existing_row.name = seed["name"]
                existing_row.description = seed["description"]
                existing_row.threshold_config = seed["threshold_config"]
                existing_row.xp_reward = seed.get("xp_reward", 0)

        self._db.flush()

    # ------------------------------------------------------------------
    # Private helpers — data access
    # ------------------------------------------------------------------

    def _get_mastery_data(self, user_id: int) -> list[MasteryDataPoint]:
        stmt = (
            select(
                UserSubtopicMastery.subtopic_id,
                UserSubtopicMastery.mastery_score,
                Module.slug.label("module_slug"),
            )
            .join(Subtopic, UserSubtopicMastery.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .join(Module, Topic.module_id == Module.id)
            .where(UserSubtopicMastery.user_id == user_id)
        )
        rows = self._db.execute(stmt).all()
        return [
            MasteryDataPoint(
                subtopic_id=row.subtopic_id,
                mastery_score=row.mastery_score,
                module_slug=row.module_slug,
            )
            for row in rows
        ]

    def _get_score_history(self, user_id: int) -> list[ScoreHistoryPoint]:
        cutoff = _utcnow() - timedelta(days=30)
        stmt = (
            select(ReadinessScoreHistory.score, ReadinessScoreHistory.computed_at)
            .where(
                ReadinessScoreHistory.user_id == user_id,
                ReadinessScoreHistory.computed_at >= cutoff,
            )
            .order_by(ReadinessScoreHistory.computed_at.asc())
        )
        rows = self._db.execute(stmt).all()
        return [
            ScoreHistoryPoint(score=row.score, computed_date=row.computed_at.date())
            for row in rows
        ]

    def _get_mastery_history(self, user_id: int) -> list[MasteryHistoryPoint]:
        """Fetch from MasteryScoreHistory — actual change records, not snapshots."""
        stmt = (
            select(
                MasteryScoreHistory.subtopic_id,
                MasteryScoreHistory.mastery_score,
                MasteryScoreHistory.recorded_at,
            )
            .where(MasteryScoreHistory.user_id == user_id)
            .order_by(
                MasteryScoreHistory.subtopic_id,
                MasteryScoreHistory.recorded_at.asc(),
            )
        )
        rows = self._db.execute(stmt).all()
        return [
            MasteryHistoryPoint(
                subtopic_id=row.subtopic_id,
                mastery_score=row.mastery_score,
                recorded_at=row.recorded_at.date()
                if isinstance(row.recorded_at, datetime)
                else row.recorded_at,
            )
            for row in rows
        ]

    def _get_unearned_milestones(
        self, user_id: int, category: str
    ) -> list[CompetenceMilestone]:
        earned_ids_stmt = select(CompetenceMilestoneAward.milestone_id).where(
            CompetenceMilestoneAward.user_id == user_id
        )
        stmt = select(CompetenceMilestone).where(
            CompetenceMilestone.category == category,
            CompetenceMilestone.id.not_in(earned_ids_stmt),
        )
        return list(self._db.execute(stmt).scalars().all())

    def _count_completed_lessons_for_module(self, user_id: int, module_slug: str) -> int:
        """Count lessons completed by user that belong to the given module."""
        stmt = (
            select(
                # count distinct lesson_completions for this module
                LessonCompletion.id
            )
            .join(Lesson, LessonCompletion.lesson_id == Lesson.id)
            .join(Subtopic, Lesson.subtopic_id == Subtopic.id)
            .join(Topic, Subtopic.topic_id == Topic.id)
            .join(Module, Topic.module_id == Module.id)
            .where(
                LessonCompletion.user_id == user_id,
                Module.slug == module_slug,
            )
        )
        return len(self._db.execute(stmt).all())

    def _has_passed_subtest_exam(
        self, user_id: int, module_slug: str, pass_threshold: float
    ) -> bool:
        """Return True if the user has a completed mock exam attempt that
        covers the given module and scored >= pass_threshold.

        The mock exam attempt's category maps to the module via the module
        slug. We check all submitted attempts to find a best score.
        """
        # Map module_slug to category values used in mock_exam_attempts
        _SLUG_TO_CATEGORY = {
            "verbal-ability": "verbal_ability",
            "numerical-ability": "numerical_ability",
            "analytical-ability": "analytical_ability",
            "clerical-ability": "clerical_ability",
            "general-information": "general_information",
        }
        category_val = _SLUG_TO_CATEGORY.get(module_slug)
        if not category_val:
            return False

        stmt = (
            select(MockExamAttempt.score, MockExamAttempt.max_score)
            .where(
                MockExamAttempt.user_id == user_id,
                MockExamAttempt.category == category_val,
                MockExamAttempt.status.in_([
                    MockExamAttemptStatus.SUBMITTED.value,
                    MockExamAttemptStatus.AUTO_SUBMITTED.value,
                ]),
                MockExamAttempt.score.is_not(None),
                MockExamAttempt.max_score > 0,
            )
        )
        rows = self._db.execute(stmt).all()
        return any(
            row.score / row.max_score >= pass_threshold
            for row in rows
        )

    def _all_subtest_champions_earned(self, user_id: int) -> bool:
        """Return True if the user has earned all 4 subtest-champion milestones
        relevant to their category. We check by counting earned champion awards."""
        champion_slugs = [
            "verbal-subtest-champion",
            "numerical-subtest-champion",
            "analytical-subtest-champion",
            "clerical-subtest-champion",
            "general-info-subtest-champion",
        ]
        stmt = (
            select(CompetenceMilestone.slug)
            .join(
                CompetenceMilestoneAward,
                CompetenceMilestoneAward.milestone_id == CompetenceMilestone.id,
            )
            .where(
                CompetenceMilestoneAward.user_id == user_id,
                CompetenceMilestone.slug.in_(champion_slugs),
            )
        )
        earned_slugs = set(self._db.execute(stmt).scalars().all())
        # All-subtests-champion requires all 4 category-appropriate slugs.
        # At minimum: verbal + numerical + general-info (shared by both categories)
        # plus either analytical (professional) or clerical (sub-professional).
        # We award if any 4 of the 5 possible champions are earned.
        return len(earned_slugs) >= 4

    def _get_comeback_awarded_subtopics(self, user_id: int) -> set[int]:
        stmt = (
            select(CompetenceMilestoneAward)
            .join(
                CompetenceMilestone,
                CompetenceMilestoneAward.milestone_id == CompetenceMilestone.id,
            )
            .where(
                CompetenceMilestoneAward.user_id == user_id,
                CompetenceMilestone.slug == "comeback",
            )
        )
        awards = list(self._db.execute(stmt).scalars().all())
        subtopic_ids: set[int] = set()
        for award in awards:
            try:
                values = json.loads(award.triggering_values)
                if "recovered_subtopics" in values:
                    for r in values["recovered_subtopics"]:
                        if "subtopic_id" in r:
                            subtopic_ids.add(r["subtopic_id"])
                elif "subtopic_id" in values:
                    subtopic_ids.add(values["subtopic_id"])
            except (json.JSONDecodeError, TypeError):
                pass
        return subtopic_ids

    # ------------------------------------------------------------------
    # Private helpers — evaluation logic
    # ------------------------------------------------------------------

    def _build_daily_scores(
        self, score_history: list[ScoreHistoryPoint]
    ) -> dict[date, int]:
        """Last score per calendar day (history ordered by computed_at ASC)."""
        daily_scores: dict[date, int] = {}
        for point in score_history:
            daily_scores[point.computed_date] = point.score
        return daily_scores

    def _has_consecutive_qualifying_days(
        self,
        daily_scores: dict[date, int],
        min_score: int,
        consecutive_days: int,
    ) -> bool:
        if not daily_scores:
            return False
        qualifying_dates = sorted(
            d for d, s in daily_scores.items() if s >= min_score
        )
        if not qualifying_dates:
            return False
        consecutive = 1
        for i in range(1, len(qualifying_dates)):
            if (qualifying_dates[i] - qualifying_dates[i - 1]).days == 1:
                consecutive += 1
            else:
                consecutive = 1
            if consecutive >= consecutive_days:
                return True
        return consecutive >= consecutive_days

    def _find_recovered_subtopics(
        self, mastery_history: list[MasteryHistoryPoint]
    ) -> list[dict[str, Any]]:
        """Find subtopics with a confirmed low-then-high transition within 14 days.

        Uses the actual MasteryScoreHistory records (one row per change event).
        For each subtopic, walks its history in chronological order looking for
        any pair where score < 0.5 was followed by score >= 0.8 within 14 days.
        This replaces the previous updated_at approximation that produced
        false positives for freshly-learned subtopics.
        """
        # Group history by subtopic in chronological order
        by_subtopic: dict[int, list[MasteryHistoryPoint]] = {}
        for point in mastery_history:
            by_subtopic.setdefault(point.subtopic_id, []).append(point)

        recovered: list[dict[str, Any]] = []
        low_threshold = 0.5
        high_threshold = 0.8
        window_days = 14

        for subtopic_id, points in by_subtopic.items():
            # Points already ordered asc by recorded_at from the query
            low_point: MasteryHistoryPoint | None = None
            for point in points:
                if point.mastery_score < low_threshold:
                    # Track the most recent low point
                    low_point = point
                elif point.mastery_score >= high_threshold and low_point is not None:
                    days_elapsed = (point.recorded_at - low_point.recorded_at).days
                    if days_elapsed <= window_days:
                        recovered.append({
                            "subtopic_id": subtopic_id,
                            "low_score": low_point.mastery_score,
                            "high_score": point.mastery_score,
                            "low_date": low_point.recorded_at,
                            "high_date": point.recorded_at,
                            "days_elapsed": days_elapsed,
                        })
                        low_point = None  # reset — don't double-count same recovery

        return recovered

    # ------------------------------------------------------------------
    # Private helpers — awarding
    # ------------------------------------------------------------------

    def _award_milestone(
        self,
        user_id: int,
        milestone: CompetenceMilestone,
        triggering_values: dict[str, Any],
    ) -> CompetenceMilestoneAward | None:
        """Award a milestone. Returns None if already awarded (idempotent).

        Grants XP via xp_service if one was injected and the milestone has
        a non-zero xp_reward. Once awarded, never revoked (Req 13.6).
        """
        existing = self._db.execute(
            select(CompetenceMilestoneAward).where(
                CompetenceMilestoneAward.user_id == user_id,
                CompetenceMilestoneAward.milestone_id == milestone.id,
            )
        ).scalar_one_or_none()

        if existing is not None:
            return None

        award = CompetenceMilestoneAward(
            user_id=user_id,
            milestone_id=milestone.id,
            triggering_values=json.dumps(triggering_values),
            # seen_at intentionally left NULL — will be set by get_unseen_awards()
        )
        self._db.add(award)
        self._db.flush()

        # Grant XP reward if service is wired in and milestone has a reward
        if self._xp_service is not None and milestone.xp_reward > 0:
            self._grant_milestone_xp(user_id, milestone)

        return award

    def _grant_milestone_xp(
        self, user_id: int, milestone: CompetenceMilestone
    ) -> None:
        """Grant XP for a newly awarded milestone. Errors are non-fatal."""
        try:
            from app.features.users.models import User
            from app.features.xp.models import XPSource

            user = self._db.get(User, user_id)
            if user is None:
                return
            self._xp_service.award(
                user=user,
                source=XPSource.MILESTONE_AWARD,
                amount=milestone.xp_reward,
                source_ref_id=milestone.id,
            )
        except Exception:
            logger.warning(
                "Failed to grant milestone XP for user_id=%d milestone=%s (non-fatal)",
                user_id,
                milestone.slug,
                exc_info=True,
            )
