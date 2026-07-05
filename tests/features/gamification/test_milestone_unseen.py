"""Tests for the unseen-awards and mastery-score-history features.

Covers:
- get_unseen_awards() marks awards seen and returns only unseen ones
- MasteryScoreHistory rows are queryable via milestone service
- seen_at is set on first retrieval, not on second
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session

from app.features.gamification.milestone_service import MilestoneService, MILESTONE_SEED_DATA
from app.features.gamification.models import (
    CompetenceMilestone,
    CompetenceMilestoneAward,
    MasteryScoreHistory,
)
from app.features.users.models import AccountState, Category, Role, User


def _seed_user(db: Session, user_id: int = 1) -> User:
    user = User(
        id=user_id,
        email=f"u{user_id}@test.com",
        display_name="Test",
        age=25,
        category=Category.SUB_PROFESSIONAL,
        role=Role.USER,
        account_state=AccountState.VERIFIED,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_milestone(db: Session, slug: str = "verbal-mastery") -> CompetenceMilestone:
    seed = next(s for s in MILESTONE_SEED_DATA if s["slug"] == slug)
    m = CompetenceMilestone(
        slug=seed["slug"],
        name=seed["name"],
        description=seed["description"],
        category=seed["category"],
        threshold_config=seed["threshold_config"],
        xp_reward=seed.get("xp_reward", 0),
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def _give_award(
    db: Session,
    user_id: int,
    milestone: CompetenceMilestone,
    seen: bool = False,
) -> CompetenceMilestoneAward:
    award = CompetenceMilestoneAward(
        user_id=user_id,
        milestone_id=milestone.id,
        triggering_values=json.dumps({"test": True}),
        seen_at=datetime.now(timezone.utc) if seen else None,
    )
    db.add(award)
    db.commit()
    db.refresh(award)
    return award


# ---------------------------------------------------------------------------
# Unseen awards
# ---------------------------------------------------------------------------


class TestGetUnseenAwards:
    def test_returns_unseen_award_and_marks_it_seen(
        self, db_session: Session
    ) -> None:
        """get_unseen_awards returns the unseen award and sets seen_at."""
        _seed_user(db_session)
        milestone = _seed_milestone(db_session, "verbal-mastery")
        award = _give_award(db_session, user_id=1, milestone=milestone, seen=False)
        assert award.seen_at is None

        service = MilestoneService(db=db_session)
        unseen = service.get_unseen_awards(user_id=1)

        assert len(unseen) == 1
        assert unseen[0].id == award.id

        # seen_at is now set
        db_session.refresh(award)
        assert award.seen_at is not None

    def test_second_call_returns_empty(self, db_session: Session) -> None:
        """After the first call marks awards seen, the second call returns empty."""
        _seed_user(db_session)
        milestone = _seed_milestone(db_session, "verbal-mastery")
        _give_award(db_session, user_id=1, milestone=milestone, seen=False)

        service = MilestoneService(db=db_session)
        first = service.get_unseen_awards(user_id=1)
        assert len(first) == 1

        second = service.get_unseen_awards(user_id=1)
        assert len(second) == 0

    def test_already_seen_award_not_returned(self, db_session: Session) -> None:
        """Awards with seen_at already set are excluded."""
        _seed_user(db_session)
        milestone = _seed_milestone(db_session, "verbal-mastery")
        _give_award(db_session, user_id=1, milestone=milestone, seen=True)

        service = MilestoneService(db=db_session)
        unseen = service.get_unseen_awards(user_id=1)
        assert len(unseen) == 0

    def test_returns_only_this_users_unseen(self, db_session: Session) -> None:
        """Only the requesting user's unseen awards are returned."""
        _seed_user(db_session, user_id=1)
        _seed_user(db_session, user_id=2)
        milestone = _seed_milestone(db_session, "verbal-mastery")

        _give_award(db_session, user_id=1, milestone=milestone, seen=False)
        _give_award(db_session, user_id=2, milestone=milestone, seen=False)

        service = MilestoneService(db=db_session)
        unseen = service.get_unseen_awards(user_id=1)

        # Only user 1's award returned
        assert len(unseen) == 1
        assert unseen[0].user_id == 1

    def test_multiple_unseen_all_marked_seen(self, db_session: Session) -> None:
        """Multiple unseen awards are all returned and all marked seen."""
        _seed_user(db_session)
        m1 = _seed_milestone(db_session, "verbal-mastery")
        m2 = _seed_milestone(db_session, "numerical-mastery")

        _give_award(db_session, user_id=1, milestone=m1, seen=False)
        _give_award(db_session, user_id=1, milestone=m2, seen=False)

        service = MilestoneService(db=db_session)
        unseen = service.get_unseen_awards(user_id=1)

        assert len(unseen) == 2
        for award in unseen:
            db_session.refresh(award)
            assert award.seen_at is not None


# ---------------------------------------------------------------------------
# MasteryScoreHistory model
# ---------------------------------------------------------------------------


class TestMasteryScoreHistoryModel:
    def test_history_row_is_persisted(self, db_session: Session) -> None:
        """MasteryScoreHistory rows can be written and read back."""
        from app.features.content.models import Module, Subtopic, Topic

        _seed_user(db_session)

        module = Module(
            category="SUB_PROFESSIONAL", slug="verbal-ability",
            title="Verbal Ability", order_index=0,
        )
        db_session.add(module)
        db_session.flush()

        topic = Topic(
            module_id=module.id, slug="grammar",
            title="Grammar", order_index=0,
        )
        db_session.add(topic)
        db_session.flush()

        subtopic = Subtopic(
            topic_id=topic.id, slug="subject-verb",
            title="Subject-Verb Agreement", order_index=0,
        )
        db_session.add(subtopic)
        db_session.flush()

        entry = MasteryScoreHistory(
            user_id=1,
            subtopic_id=subtopic.id,
            mastery_score=0.72,
        )
        db_session.add(entry)
        db_session.commit()
        db_session.refresh(entry)

        assert entry.id is not None
        assert entry.mastery_score == 0.72
        assert entry.recorded_at is not None

    def test_service_reads_history_for_recovery(self, db_session: Session) -> None:
        """_get_mastery_history returns MasteryHistoryPoint rows from the table."""
        from app.features.content.models import Module, Subtopic, Topic
        from datetime import timedelta

        _seed_user(db_session)

        module = Module(
            category="SUB_PROFESSIONAL", slug="verbal-ability",
            title="Verbal Ability", order_index=0,
        )
        db_session.add(module)
        db_session.flush()
        topic = Topic(
            module_id=module.id, slug="grammar",
            title="Grammar", order_index=0,
        )
        db_session.add(topic)
        db_session.flush()
        subtopic = Subtopic(
            topic_id=topic.id, slug="subject-verb",
            title="Subject-Verb Agreement", order_index=0,
        )
        db_session.add(subtopic)
        db_session.flush()

        now = datetime.now(timezone.utc)

        # Write two history entries: a low then a high
        low = MasteryScoreHistory(
            user_id=1, subtopic_id=subtopic.id, mastery_score=0.35,
            recorded_at=now - timedelta(days=8),
        )
        high = MasteryScoreHistory(
            user_id=1, subtopic_id=subtopic.id, mastery_score=0.88,
            recorded_at=now - timedelta(days=2),
        )
        db_session.add_all([low, high])
        db_session.commit()

        service = MilestoneService(db=db_session)
        history = service._get_mastery_history(user_id=1)

        assert len(history) == 2
        scores = [h.mastery_score for h in history]
        assert 0.35 in scores
        assert 0.88 in scores

    def test_recovery_detection_uses_history_pairs(
        self, db_session: Session
    ) -> None:
        """_find_recovered_subtopics correctly identifies low→high pairs."""
        from app.features.gamification.milestone_service import MasteryHistoryPoint
        from datetime import date, timedelta

        service = MilestoneService(db=db_session)
        today = date.today()

        history = [
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=0.30,         # below 0.5 — low point
                recorded_at=today - timedelta(days=10),
            ),
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=0.85,         # above 0.8 — recovery within 10 days
                recorded_at=today - timedelta(days=3),
            ),
        ]

        recovered = service._find_recovered_subtopics(history)

        assert len(recovered) == 1
        assert recovered[0]["subtopic_id"] == 1
        assert recovered[0]["days_elapsed"] == 7

    def test_no_prior_low_means_no_recovery(self, db_session: Session) -> None:
        """A high score without a prior low does not count as a recovery."""
        from app.features.gamification.milestone_service import MasteryHistoryPoint
        from datetime import date, timedelta

        service = MilestoneService(db=db_session)
        today = date.today()

        # Only a high score — no low was ever recorded
        history = [
            MasteryHistoryPoint(
                subtopic_id=5,
                mastery_score=0.90,
                recorded_at=today - timedelta(days=2),
            ),
        ]

        recovered = service._find_recovered_subtopics(history)
        assert len(recovered) == 0
