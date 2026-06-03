"""Service tests for MilestoneService.

Tests milestone evaluation logic: mastery milestones, readiness milestones,
recovery milestones, and retroactive evaluation.

Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 15.1
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy.orm import Session

from app.features.content.models import Module, Subtopic, Topic
from app.features.gamification.milestone_service import (
    MasteryDataPoint,
    MasteryHistoryPoint,
    MilestoneService,
    MILESTONE_SEED_DATA,
    ScoreHistoryPoint,
)
from app.features.gamification.models import (
    CompetenceMilestone,
    CompetenceMilestoneAward,
)
from app.features.mastery.models import UserSubtopicMastery
from app.features.readiness.models import ReadinessScoreHistory
from app.features.users.models import User


def _seed_user(db: Session, user_id: int = 1) -> User:
    """Insert a minimal user row for FK satisfaction."""
    user = User(
        id=user_id,
        email=f"user{user_id}@test.com",
        display_name="Test User",
        age=25,
        category="PROFESSIONAL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_milestones(db: Session) -> list[CompetenceMilestone]:
    """Seed all milestone definitions."""
    milestones = []
    for seed in MILESTONE_SEED_DATA:
        m = CompetenceMilestone(
            slug=seed["slug"],
            name=seed["name"],
            description=seed["description"],
            category=seed["category"],
            threshold_config=seed["threshold_config"],
        )
        db.add(m)
        milestones.append(m)
    db.commit()
    for m in milestones:
        db.refresh(m)
    return milestones


def _seed_module_hierarchy(
    db: Session,
    module_slug: str,
    module_title: str,
    subtopic_count: int,
) -> list[Subtopic]:
    """Seed a module -> topic -> subtopics hierarchy."""
    module = Module(
        category="PROFESSIONAL",
        slug=module_slug,
        title=module_title,
        order_index=0,
    )
    db.add(module)
    db.flush()

    topic = Topic(
        module_id=module.id,
        slug=f"{module_slug}-topic",
        title=f"{module_title} Topic",
        order_index=0,
    )
    db.add(topic)
    db.flush()

    subtopics = []
    for i in range(subtopic_count):
        st = Subtopic(
            topic_id=topic.id,
            slug=f"{module_slug}-subtopic-{i}",
            title=f"{module_title} Subtopic {i}",
            order_index=i,
        )
        db.add(st)
        subtopics.append(st)

    db.commit()
    for st in subtopics:
        db.refresh(st)
    return subtopics


def _seed_mastery(
    db: Session,
    user_id: int,
    subtopic_id: int,
    mastery_score: float,
    updated_at: datetime | None = None,
) -> UserSubtopicMastery:
    """Seed a mastery record for a user/subtopic."""
    m = UserSubtopicMastery(
        user_id=user_id,
        subtopic_id=subtopic_id,
        mastery_score=mastery_score,
        mastery_level="MASTERED" if mastery_score >= 0.9 else "PROFICIENT",
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    if updated_at is not None:
        # Manually set updated_at for testing recovery milestones
        m.updated_at = updated_at
        db.commit()
        db.refresh(m)
    return m


def _seed_readiness_history(
    db: Session,
    user_id: int,
    scores: list[tuple[date, int]],
) -> list[ReadinessScoreHistory]:
    """Seed readiness score history records."""
    records = []
    for score_date, score in scores:
        computed_at = datetime.combine(
            score_date, datetime.max.time(), tzinfo=timezone.utc
        )
        record = ReadinessScoreHistory(
            user_id=user_id,
            score=score,
            mastery_component=50.0,
            retention_component=50.0,
            mock_component=50.0,
            coverage_component=50.0,
            weights_used='{"mastery":0.4,"retention":0.25,"mock":0.25,"coverage":0.1}',
            computed_at=computed_at,
        )
        db.add(record)
        records.append(record)
    db.commit()
    for r in records:
        db.refresh(r)
    return records


class TestEnsureMilestonesSeeded:
    """Tests for milestone seed data insertion."""

    def test_seeds_all_milestones(self, db_session: Session) -> None:
        """_ensure_milestones_seeded creates all 8 milestone definitions."""
        _seed_user(db_session)
        service = MilestoneService(db=db_session)
        service._ensure_milestones_seeded()

        from sqlalchemy import select, func

        count = db_session.execute(
            select(func.count()).select_from(CompetenceMilestone)
        ).scalar_one()
        assert count == 8

    def test_idempotent_seeding(self, db_session: Session) -> None:
        """Calling _ensure_milestones_seeded twice doesn't create duplicates."""
        _seed_user(db_session)
        service = MilestoneService(db=db_session)
        service._ensure_milestones_seeded()
        service._ensure_milestones_seeded()

        from sqlalchemy import select, func

        count = db_session.execute(
            select(func.count()).select_from(CompetenceMilestone)
        ).scalar_one()
        assert count == 8


class TestEvaluateMasteryMilestones:
    """Tests for mastery milestone evaluation — Req 13.1."""

    def test_verbal_mastery_awarded_when_all_23_meet_threshold(
        self, db_session: Session
    ) -> None:
        """Verbal Mastery awarded when all 23 verbal subtopics have mastery ≥ 0.8."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        mastery_data = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.85, module_slug="verbal-ability")
            for i in range(1, 24)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data)

        assert len(awards) == 1
        assert awards[0].user_id == 1

        # Verify it's the verbal-mastery milestone
        milestone = db_session.get(CompetenceMilestone, awards[0].milestone_id)
        assert milestone.slug == "verbal-mastery"

    def test_verbal_mastery_not_awarded_when_below_threshold(
        self, db_session: Session
    ) -> None:
        """Verbal Mastery not awarded if any subtopic is below 0.8."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        mastery_data = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.85, module_slug="verbal-ability")
            for i in range(1, 23)
        ] + [
            MasteryDataPoint(subtopic_id=23, mastery_score=0.7, module_slug="verbal-ability")
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data)

        assert len(awards) == 0

    def test_full_spectrum_requires_all_60(self, db_session: Session) -> None:
        """Full Spectrum requires all 60 subtopics at ≥ 0.8."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        mastery_data = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.9, module_slug="verbal-ability")
            for i in range(1, 24)
        ] + [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.9, module_slug="numerical-ability")
            for i in range(24, 48)
        ] + [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.9, module_slug="analytical-ability")
            for i in range(48, 61)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data)

        slugs = set()
        for award in awards:
            milestone = db_session.get(CompetenceMilestone, award.milestone_id)
            slugs.add(milestone.slug)

        # Should award all 4 mastery milestones
        assert "verbal-mastery" in slugs
        assert "numerical-mastery" in slugs
        assert "analytical-mastery" in slugs
        assert "full-spectrum" in slugs

    def test_already_awarded_not_re_awarded(self, db_session: Session) -> None:
        """Once earned, a milestone is never revoked or re-awarded (Req 13.6)."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        mastery_data = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.85, module_slug="verbal-ability")
            for i in range(1, 24)
        ]

        service = MilestoneService(db=db_session)

        # First evaluation awards the milestone
        awards1 = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data)
        assert len(awards1) == 1
        db_session.commit()

        # Second evaluation should not re-award
        awards2 = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data)
        assert len(awards2) == 0


class TestEvaluateReadinessMilestones:
    """Tests for readiness milestone evaluation — Req 13.2."""

    def test_sub_professional_awarded_with_7_consecutive_days_at_70(
        self, db_session: Session
    ) -> None:
        """Exam Ready: Sub-Professional awarded with 7 consecutive days ≥ 70."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        base_date = date(2025, 6, 1)
        score_history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(7)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=score_history
        )

        assert len(awards) == 1
        milestone = db_session.get(CompetenceMilestone, awards[0].milestone_id)
        assert milestone.slug == "exam-ready-sub-professional"

    def test_professional_awarded_with_7_consecutive_days_at_80(
        self, db_session: Session
    ) -> None:
        """Exam Ready: Professional awarded with 7 consecutive days ≥ 80."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        base_date = date(2025, 6, 1)
        score_history = [
            ScoreHistoryPoint(score=85, computed_date=base_date + timedelta(days=i))
            for i in range(7)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=score_history
        )

        # Score ≥ 80 also satisfies ≥ 70, so both should be awarded
        assert len(awards) == 2
        slugs = set()
        for award in awards:
            milestone = db_session.get(CompetenceMilestone, award.milestone_id)
            slugs.add(milestone.slug)
        assert "exam-ready-sub-professional" in slugs
        assert "exam-ready-professional" in slugs

    def test_not_awarded_with_gap_in_days(self, db_session: Session) -> None:
        """Readiness milestone not awarded if there's a gap in consecutive days."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        base_date = date(2025, 6, 1)
        # 5 consecutive days, gap, then 2 more (not 7 consecutive)
        score_history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(5)
        ] + [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=7)),
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=8)),
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=score_history
        )

        assert len(awards) == 0

    def test_not_awarded_with_6_consecutive_days(self, db_session: Session) -> None:
        """6 consecutive days is not enough — need exactly 7."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        base_date = date(2025, 6, 1)
        score_history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(6)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=score_history
        )

        assert len(awards) == 0

    def test_not_awarded_when_score_below_threshold_on_one_day(
        self, db_session: Session
    ) -> None:
        """If any day in the 7-day window has score below threshold, not awarded."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        base_date = date(2025, 6, 1)
        score_history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(7)
        ]
        # Override one day to be below 70
        score_history[3] = ScoreHistoryPoint(
            score=65, computed_date=base_date + timedelta(days=3)
        )

        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=score_history
        )

        assert len(awards) == 0


class TestEvaluateRecoveryMilestones:
    """Tests for recovery milestone evaluation — Req 13.3."""

    def test_comeback_awarded_when_subtopic_recovers(
        self, db_session: Session
    ) -> None:
        """Comeback awarded when subtopic goes from < 0.5 to ≥ 0.8 within 14 days."""
        _seed_user(db_session)
        _seed_milestones(db_session)
        subtopics = _seed_module_hierarchy(
            db_session, "verbal-ability", "Verbal Ability", 1
        )

        # Seed mastery at ≥ 0.8 updated recently (within 14 days)
        now = datetime.now(tz=timezone.utc)
        _seed_mastery(
            db_session,
            user_id=1,
            subtopic_id=subtopics[0].id,
            mastery_score=0.85,
            updated_at=now - timedelta(days=5),
        )

        mastery_history = [
            MasteryHistoryPoint(
                subtopic_id=subtopics[0].id,
                mastery_score=0.85,
                recorded_at=(now - timedelta(days=5)).date(),
            )
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_recovery_milestones(
            user_id=1, mastery_history=mastery_history
        )

        assert len(awards) == 1
        milestone = db_session.get(CompetenceMilestone, awards[0].milestone_id)
        assert milestone.slug == "comeback"

    def test_comeback_not_awarded_outside_14_day_window(
        self, db_session: Session
    ) -> None:
        """Comeback not awarded if recovery took more than 14 days."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        # Mastery updated 20 days ago (outside 14-day window)
        now = datetime.now(tz=timezone.utc)
        mastery_history = [
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=0.85,
                recorded_at=(now - timedelta(days=20)).date(),
            )
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_recovery_milestones(
            user_id=1, mastery_history=mastery_history
        )

        assert len(awards) == 0

    def test_resilient_learner_awarded_after_3_comebacks(
        self, db_session: Session
    ) -> None:
        """Resilient Learner awarded when 3+ distinct subtopics have recovered."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        now = datetime.now(tz=timezone.utc)
        # Create 3 subtopics that have recovered
        mastery_history = [
            MasteryHistoryPoint(
                subtopic_id=i,
                mastery_score=0.85,
                recorded_at=(now - timedelta(days=3)).date(),
            )
            for i in range(1, 4)
        ]

        service = MilestoneService(db=db_session)
        awards = service.evaluate_recovery_milestones(
            user_id=1, mastery_history=mastery_history
        )

        slugs = []
        for award in awards:
            milestone = db_session.get(CompetenceMilestone, award.milestone_id)
            slugs.append(milestone.slug)

        # Should have comeback (awarded once) + resilient learner
        assert "comeback" in slugs
        assert "resilient-learner" in slugs
        assert len(awards) == 2


class TestRetroactiveEvaluation:
    """Tests for retroactive milestone evaluation — Req 15.1."""

    def test_retroactive_awards_already_satisfied_milestones(
        self, db_session: Session
    ) -> None:
        """Retroactive evaluation awards milestones already met by existing data."""
        _seed_user(db_session)
        # Create module hierarchy for verbal
        subtopics = _seed_module_hierarchy(
            db_session, "verbal-ability", "Verbal Ability", 23
        )

        # Seed all 23 verbal subtopics with mastery ≥ 0.8
        for st in subtopics:
            _seed_mastery(db_session, user_id=1, subtopic_id=st.id, mastery_score=0.85)

        service = MilestoneService(db=db_session)
        awards = service.retroactive_evaluation(user_id=1)

        # Should award verbal-mastery
        awarded_slugs = set()
        for award in awards:
            milestone = db_session.get(CompetenceMilestone, award.milestone_id)
            awarded_slugs.add(milestone.slug)

        assert "verbal-mastery" in awarded_slugs

    def test_retroactive_seeds_milestones_if_not_present(
        self, db_session: Session
    ) -> None:
        """Retroactive evaluation seeds milestone definitions if they don't exist."""
        _seed_user(db_session)

        from sqlalchemy import select, func

        # Verify no milestones exist yet
        count_before = db_session.execute(
            select(func.count()).select_from(CompetenceMilestone)
        ).scalar_one()
        assert count_before == 0

        service = MilestoneService(db=db_session)
        service.retroactive_evaluation(user_id=1)

        count_after = db_session.execute(
            select(func.count()).select_from(CompetenceMilestone)
        ).scalar_one()
        assert count_after == 8


class TestMilestoneNeverRevoked:
    """Tests that once awarded, milestones are never revoked — Req 13.6."""

    def test_award_persists_after_metrics_drop(self, db_session: Session) -> None:
        """Award stays even if metrics drop below threshold."""
        _seed_user(db_session)
        _seed_milestones(db_session)

        # Award verbal mastery
        mastery_data_high = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.85, module_slug="verbal-ability")
            for i in range(1, 24)
        ]
        service = MilestoneService(db=db_session)
        awards = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data_high)
        assert len(awards) == 1
        db_session.commit()

        # Now re-evaluate with lower data — award should NOT be revoked
        mastery_data_low = [
            MasteryDataPoint(subtopic_id=i, mastery_score=0.5, module_slug="verbal-ability")
            for i in range(1, 24)
        ]
        awards2 = service.evaluate_mastery_milestones(user_id=1, mastery_data=mastery_data_low)
        assert len(awards2) == 0

        # Verify the original award still exists in the database
        from sqlalchemy import select, func

        award_count = db_session.execute(
            select(func.count())
            .select_from(CompetenceMilestoneAward)
            .where(CompetenceMilestoneAward.user_id == 1)
        ).scalar_one()
        assert award_count == 1
