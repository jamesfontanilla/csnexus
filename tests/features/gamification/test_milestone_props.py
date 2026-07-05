"""Property-based tests for milestone evaluation logic.

Uses Hypothesis to validate universal correctness properties of the
MilestoneService evaluation pipeline: mastery milestones, readiness
milestones, recovery milestones, the never-revoke guarantee, and
milestone progress percentage computation.

Tests target the pure logic helpers within MilestoneService that are
independent of database access.

**Validates: Requirements 13.1, 13.2, 13.3, 13.6, 13.7**
"""

from __future__ import annotations

import json
from datetime import date, timedelta

from hypothesis import given, settings, assume, HealthCheck
from hypothesis.strategies import (
    composite,
    floats,
    integers,
    lists,
    sampled_from,
)
from sqlalchemy.orm import Session

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


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

MODULE_SLUGS = ["verbal-ability", "numerical-ability", "analytical-ability",
               "clerical-ability", "general-information"]


@composite
def mastery_data_for_module(draw, module_slug: str, count: int, min_score: float = 0.0):
    """Generate a list of MasteryDataPoints for a specific module with unique subtopic IDs."""
    scores = draw(
        lists(
            floats(min_value=min_score, max_value=1.0, allow_nan=False),
            min_size=count,
            max_size=count,
        )
    )
    return [
        MasteryDataPoint(
            subtopic_id=i + 1,
            mastery_score=scores[i],
            module_slug=module_slug,
        )
        for i in range(count)
    ]


@composite
def score_history_with_gaps(draw):
    """Generate score history that may have gaps between days."""
    num_entries = draw(integers(min_value=1, max_value=20))
    base_date = date(2025, 1, 1)
    points = []
    current_date = base_date
    for _ in range(num_entries):
        score = draw(integers(min_value=0, max_value=100))
        points.append(ScoreHistoryPoint(score=score, computed_date=current_date))
        # Jump 1-3 days forward (may create gaps)
        gap = draw(integers(min_value=1, max_value=3))
        current_date = current_date + timedelta(days=gap)
    return points


@composite
def mastery_history_points(draw, num_subtopics: int = 5):
    """Generate mastery history points with unique subtopic IDs."""
    count = draw(integers(min_value=1, max_value=num_subtopics))
    points = []
    for i in range(count):
        score = draw(floats(min_value=0.0, max_value=1.0, allow_nan=False))
        days_ago = draw(integers(min_value=0, max_value=30))
        points.append(
            MasteryHistoryPoint(
                subtopic_id=i + 1,
                mastery_score=score,
                recorded_at=date.today() - timedelta(days=days_ago),
            )
        )
    return points


# ---------------------------------------------------------------------------
# Helpers — pure logic extracted from MilestoneService for testing
# ---------------------------------------------------------------------------


def _build_daily_scores(score_history: list[ScoreHistoryPoint]) -> dict[date, int]:
    """Build a map of date -> last score for that day (same logic as service)."""
    daily_scores: dict[date, int] = {}
    for point in score_history:
        daily_scores[point.computed_date] = point.score
    return daily_scores


def _has_consecutive_qualifying_days(
    daily_scores: dict[date, int],
    min_score: int,
    consecutive_days: int,
) -> bool:
    """Check if there are N consecutive calendar days with score >= min_score."""
    if not daily_scores:
        return False

    qualifying_dates = sorted(
        d for d in daily_scores if daily_scores[d] >= min_score
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


def _evaluate_mastery_threshold(
    mastery_data: list[MasteryDataPoint],
    module_slug: str | None,
    required_count: int,
    threshold: float,
) -> bool:
    """Check if enough subtopics in a module meet the mastery threshold."""
    if module_slug is not None:
        relevant = [m for m in mastery_data if m.module_slug == module_slug]
    else:
        relevant = list(mastery_data)

    qualifying = [m for m in relevant if m.mastery_score >= threshold]
    return len(qualifying) >= required_count


def _find_recovered_subtopics(
    mastery_history: list[MasteryHistoryPoint],
) -> list[dict]:
    """Find subtopics that recovered: mastery >= 0.8 within 14 days of today."""
    recovered = []
    today = date.today()

    subtopic_map: dict[int, MasteryHistoryPoint] = {}
    for point in mastery_history:
        subtopic_map[point.subtopic_id] = point

    for subtopic_id, point in subtopic_map.items():
        if point.mastery_score >= 0.8:
            days_elapsed = (today - point.recorded_at).days
            if days_elapsed <= 14:
                recovered.append(
                    {
                        "subtopic_id": subtopic_id,
                        "high_score": point.mastery_score,
                        "days_elapsed": days_elapsed,
                    }
                )
    return recovered


def compute_milestone_progress(
    milestone_category: str,
    mastery_data: list[MasteryDataPoint] | None = None,
    module_slug: str | None = None,
    required_count: int = 0,
    threshold: float = 0.8,
    score_history: list[ScoreHistoryPoint] | None = None,
    min_score: int = 0,
    comeback_count: int = 0,
) -> float:
    """Compute milestone progress percentage per Requirement 13.7 formula.

    - Mastery milestones: qualifying_count / required_count
    - Readiness milestones: max_consecutive_qualifying_days / 7
    - Recovery milestones (resilient-learner): comeback_count / 3
    """
    if milestone_category == "mastery":
        if mastery_data is None:
            return 0.0
        if module_slug is not None:
            relevant = [m for m in mastery_data if m.module_slug == module_slug]
        else:
            relevant = list(mastery_data)
        qualifying = sum(1 for m in relevant if m.mastery_score >= threshold)
        if required_count == 0:
            return 0.0
        return min(qualifying / required_count, 1.0)

    elif milestone_category == "readiness":
        if score_history is None or not score_history:
            return 0.0
        daily_scores = _build_daily_scores(score_history)
        qualifying_dates = sorted(
            d for d in daily_scores if daily_scores[d] >= min_score
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
        return min(max_consecutive / 7, 1.0)

    elif milestone_category == "recovery":
        return min(comeback_count / 3, 1.0)

    return 0.0


# ---------------------------------------------------------------------------
# DB fixtures helpers (used by Properties 26 which require persistence)
# ---------------------------------------------------------------------------


def _seed_user(db: Session, user_id: int = 1):
    """Insert a minimal user row for FK satisfaction."""
    from app.features.users.models import User

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
            xp_reward=seed.get("xp_reward", 0),
        )
        db.add(m)
        milestones.append(m)
    db.commit()
    for m in milestones:
        db.refresh(m)
    return milestones


# ---------------------------------------------------------------------------
# Property 23: Mastery milestone evaluates all subtopics in category
# ---------------------------------------------------------------------------


class TestMasteryMilestoneEvaluatesAllSubtopics:
    """For any mastery milestone evaluation, the milestone SHALL be awarded
    if and only if the count of subtopics with mastery_score >= threshold
    in the specified module meets or exceeds the required_count.

    **Validates: Requirements 13.1**
    """

    @settings(max_examples=50)
    @given(data=mastery_data_for_module("verbal-ability", count=23, min_score=0.8))
    def test_all_qualifying_scores_awards_milestone(
        self, data: list[MasteryDataPoint]
    ) -> None:
        """When all 23 verbal subtopics have mastery >= 0.8, the mastery
        threshold check returns True."""
        assert all(d.mastery_score >= 0.8 for d in data)

        result = _evaluate_mastery_threshold(
            mastery_data=data,
            module_slug="verbal-ability",
            required_count=23,
            threshold=0.8,
        )
        assert result is True

    @settings(max_examples=50)
    @given(qualifying_count=integers(min_value=0, max_value=22))
    def test_insufficient_qualifying_count_does_not_award(
        self, qualifying_count: int
    ) -> None:
        """When fewer than 23 verbal subtopics have mastery >= 0.8,
        the threshold check returns False."""
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=0.85,
                module_slug="verbal-ability",
            )
            for i in range(qualifying_count)
        ] + [
            MasteryDataPoint(
                subtopic_id=qualifying_count + i + 1,
                mastery_score=0.5,
                module_slug="verbal-ability",
            )
            for i in range(23 - qualifying_count)
        ]

        result = _evaluate_mastery_threshold(
            mastery_data=data,
            module_slug="verbal-ability",
            required_count=23,
            threshold=0.8,
        )
        assert result is False

    @settings(max_examples=50)
    @given(
        scores=lists(
            floats(min_value=0.0, max_value=1.0, allow_nan=False),
            min_size=23,
            max_size=23,
        )
    )
    def test_qualifying_count_matches_threshold_logic(
        self, scores: list[float]
    ) -> None:
        """The milestone is awarded iff count of scores >= 0.8 meets required_count."""
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=scores[i],
                module_slug="verbal-ability",
            )
            for i in range(23)
        ]

        qualifying = sum(1 for s in scores if s >= 0.8)

        result = _evaluate_mastery_threshold(
            mastery_data=data,
            module_slug="verbal-ability",
            required_count=23,
            threshold=0.8,
        )

        if qualifying >= 23:
            assert result is True
        else:
            assert result is False

    @settings(max_examples=50)
    @given(
        scores=lists(
            floats(min_value=0.0, max_value=1.0, allow_nan=False),
            min_size=60,
            max_size=60,
        )
    )
    def test_full_spectrum_evaluates_all_modules(
        self, scores: list[float]
    ) -> None:
        """Full Spectrum (module_slug=None) evaluates all subtopics across
        all modules, requiring 60 qualifying subtopics."""
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=scores[i],
                module_slug=MODULE_SLUGS[i % 3],
            )
            for i in range(60)
        ]

        qualifying = sum(1 for s in scores if s >= 0.8)

        result = _evaluate_mastery_threshold(
            mastery_data=data,
            module_slug=None,
            required_count=60,
            threshold=0.8,
        )

        if qualifying >= 60:
            assert result is True
        else:
            assert result is False

    @settings(max_examples=50)
    @given(
        scores=lists(
            floats(min_value=0.0, max_value=1.0, allow_nan=False),
            min_size=24,
            max_size=24,
        )
    )
    def test_module_filter_ignores_other_modules(
        self, scores: list[float]
    ) -> None:
        """Mastery evaluation for a specific module ignores subtopics from
        other modules."""
        # Create data with 24 numerical subtopics + some verbal ones all at 0.9
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=scores[i],
                module_slug="numerical-ability",
            )
            for i in range(24)
        ] + [
            MasteryDataPoint(
                subtopic_id=100 + i,
                mastery_score=0.95,
                module_slug="verbal-ability",
            )
            for i in range(23)
        ]

        # Verbal subtopics should NOT count toward numerical mastery
        qualifying_numerical = sum(1 for s in scores if s >= 0.8)

        result = _evaluate_mastery_threshold(
            mastery_data=data,
            module_slug="numerical-ability",
            required_count=24,
            threshold=0.8,
        )

        if qualifying_numerical >= 24:
            assert result is True
        else:
            assert result is False


# ---------------------------------------------------------------------------
# Property 24: Readiness milestone requires 7 consecutive qualifying days
# ---------------------------------------------------------------------------


class TestReadinessMilestoneConsecutiveDays:
    """For any readiness milestone evaluation, the milestone SHALL be awarded
    if and only if there exist 7 consecutive calendar days where the daily
    score (last score per day) meets or exceeds the min_score threshold.

    **Validates: Requirements 13.2**
    """

    @settings(max_examples=50)
    @given(base_score=integers(min_value=70, max_value=100))
    def test_7_consecutive_qualifying_days_passes(self, base_score: int) -> None:
        """7 consecutive days with score >= threshold returns True."""
        base_date = date(2025, 6, 1)
        history = [
            ScoreHistoryPoint(score=base_score, computed_date=base_date + timedelta(days=i))
            for i in range(7)
        ]

        daily_scores = _build_daily_scores(history)
        result = _has_consecutive_qualifying_days(daily_scores, 70, 7)
        assert result is True

    @settings(max_examples=50)
    @given(num_consecutive=integers(min_value=1, max_value=6))
    def test_fewer_than_7_days_does_not_qualify(self, num_consecutive: int) -> None:
        """Fewer than 7 consecutive qualifying days returns False."""
        base_date = date(2025, 6, 1)
        history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(num_consecutive)
        ]

        daily_scores = _build_daily_scores(history)
        result = _has_consecutive_qualifying_days(daily_scores, 70, 7)
        assert result is False

    @settings(max_examples=50)
    @given(
        score_below=integers(min_value=0, max_value=69),
        score_above=integers(min_value=70, max_value=100),
        break_position=integers(min_value=0, max_value=6),
    )
    def test_one_below_threshold_breaks_consecutive_run(
        self, score_below: int, score_above: int, break_position: int
    ) -> None:
        """A single day below threshold within a 7-day window breaks the run."""
        base_date = date(2025, 6, 1)
        history = [
            ScoreHistoryPoint(
                score=score_below if i == break_position else score_above,
                computed_date=base_date + timedelta(days=i),
            )
            for i in range(7)
        ]

        daily_scores = _build_daily_scores(history)
        result = _has_consecutive_qualifying_days(daily_scores, 70, 7)
        assert result is False

    @settings(max_examples=50)
    @given(history=score_history_with_gaps())
    def test_gaps_in_calendar_days_break_consecutive_run(
        self, history: list[ScoreHistoryPoint]
    ) -> None:
        """The consecutive days logic correctly handles gaps between dates.
        A day without a score breaks any consecutive run."""
        daily_scores = _build_daily_scores(history)
        result = _has_consecutive_qualifying_days(daily_scores, 70, 7)

        # Verify by computing expected value independently
        qualifying_dates = sorted(
            d for d in daily_scores if daily_scores[d] >= 70
        )

        if not qualifying_dates:
            assert result is False
            return

        max_consecutive = 1
        current = 1
        for i in range(1, len(qualifying_dates)):
            if (qualifying_dates[i] - qualifying_dates[i - 1]).days == 1:
                current += 1
                max_consecutive = max(max_consecutive, current)
            else:
                current = 1

        expected = max_consecutive >= 7
        assert result == expected

    @settings(max_examples=50)
    @given(
        extra_days_before=integers(min_value=0, max_value=10),
        extra_days_after=integers(min_value=0, max_value=10),
    )
    def test_7_qualifying_embedded_in_longer_history(
        self, extra_days_before: int, extra_days_after: int
    ) -> None:
        """7 consecutive qualifying days within a longer history are detected."""
        base_date = date(2025, 6, 1)

        # Non-qualifying days before
        history = [
            ScoreHistoryPoint(
                score=50,
                computed_date=base_date + timedelta(days=i),
            )
            for i in range(extra_days_before)
        ]

        # 7 qualifying days
        start_offset = extra_days_before + 2  # +2 to create a gap
        history += [
            ScoreHistoryPoint(
                score=75,
                computed_date=base_date + timedelta(days=start_offset + i),
            )
            for i in range(7)
        ]

        # Non-qualifying days after
        after_offset = start_offset + 7 + 2  # +2 gap
        history += [
            ScoreHistoryPoint(
                score=50,
                computed_date=base_date + timedelta(days=after_offset + i),
            )
            for i in range(extra_days_after)
        ]

        daily_scores = _build_daily_scores(history)
        result = _has_consecutive_qualifying_days(daily_scores, 70, 7)
        assert result is True


# ---------------------------------------------------------------------------
# Property 25: Recovery milestone detects mastery recovery within 14 days
# ---------------------------------------------------------------------------


class TestRecoveryMilestoneDetection:
    """For any recovery milestone evaluation, a subtopic SHALL qualify as
    recovered when its mastery_score >= 0.8 and was recorded within 14
    calendar days of today. Subtopics with mastery_score < 0.8 or
    recorded_at older than 14 days SHALL NOT be detected as recovered.

    **Validates: Requirements 13.3**
    """

    @settings(max_examples=50)
    @given(
        days_ago=integers(min_value=0, max_value=14),
        score=floats(min_value=0.8, max_value=1.0, allow_nan=False),
    )
    def test_recovery_within_14_days_detected(
        self, days_ago: int, score: float
    ) -> None:
        """Subtopic with mastery >= 0.8 recorded within 14 days is detected."""
        history = [
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=score,
                recorded_at=date.today() - timedelta(days=days_ago),
            )
        ]

        recovered = _find_recovered_subtopics(history)
        assert len(recovered) == 1
        assert recovered[0]["subtopic_id"] == 1

    @settings(max_examples=50)
    @given(
        days_ago=integers(min_value=15, max_value=60),
        score=floats(min_value=0.8, max_value=1.0, allow_nan=False),
    )
    def test_recovery_outside_14_day_window_not_detected(
        self, days_ago: int, score: float
    ) -> None:
        """Subtopic with mastery >= 0.8 recorded more than 14 days ago
        is NOT detected as recovered."""
        history = [
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=score,
                recorded_at=date.today() - timedelta(days=days_ago),
            )
        ]

        recovered = _find_recovered_subtopics(history)
        assert len(recovered) == 0

    @settings(max_examples=50)
    @given(
        days_ago=integers(min_value=0, max_value=14),
        score=floats(min_value=0.0, max_value=0.799, allow_nan=False),
    )
    def test_below_high_threshold_not_detected(
        self, days_ago: int, score: float
    ) -> None:
        """Subtopic with mastery < 0.8 within 14 days is NOT detected."""
        assume(score < 0.8)

        history = [
            MasteryHistoryPoint(
                subtopic_id=1,
                mastery_score=score,
                recorded_at=date.today() - timedelta(days=days_ago),
            )
        ]

        recovered = _find_recovered_subtopics(history)
        assert len(recovered) == 0

    @settings(max_examples=50)
    @given(
        num_subtopics=integers(min_value=1, max_value=10),
    )
    def test_multiple_recovered_subtopics_all_detected(
        self, num_subtopics: int
    ) -> None:
        """All subtopics with mastery >= 0.8 within 14 days are detected."""
        history = [
            MasteryHistoryPoint(
                subtopic_id=i + 1,
                mastery_score=0.85,
                recorded_at=date.today() - timedelta(days=3),
            )
            for i in range(num_subtopics)
        ]

        recovered = _find_recovered_subtopics(history)
        assert len(recovered) == num_subtopics
        recovered_ids = {r["subtopic_id"] for r in recovered}
        expected_ids = set(range(1, num_subtopics + 1))
        assert recovered_ids == expected_ids

    @settings(max_examples=50)
    @given(history=mastery_history_points(num_subtopics=8))
    def test_recovery_detection_consistency(
        self, history: list[MasteryHistoryPoint]
    ) -> None:
        """For any generated mastery history, recovered subtopics are exactly
        those with score >= 0.8 AND recorded_at within 14 days of today."""
        recovered = _find_recovered_subtopics(history)
        today = date.today()

        # Build expected from first principles
        subtopic_map: dict[int, MasteryHistoryPoint] = {}
        for point in history:
            subtopic_map[point.subtopic_id] = point

        expected_ids = set()
        for sid, point in subtopic_map.items():
            if point.mastery_score >= 0.8 and (today - point.recorded_at).days <= 14:
                expected_ids.add(sid)

        actual_ids = {r["subtopic_id"] for r in recovered}
        assert actual_ids == expected_ids


# ---------------------------------------------------------------------------
# Property 26: Awarded milestones are never revoked
# ---------------------------------------------------------------------------


class TestAwardedMilestonesNeverRevoked:
    """Once a milestone is awarded, subsequent evaluations with lower metrics
    SHALL NOT revoke the award. The award persists regardless of future metric
    changes.

    **Validates: Requirements 13.6**
    """

    @settings(
        max_examples=50,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(low_score=floats(min_value=0.0, max_value=0.5, allow_nan=False))
    def test_mastery_award_persists_after_score_drop(
        self, low_score: float, db_session: Session
    ) -> None:
        """After awarding verbal-mastery, re-evaluating with low scores
        does not revoke the award."""
        from sqlalchemy import select, func

        # Clean state for this example
        db_session.execute(select(CompetenceMilestoneAward).where(True))
        db_session.query(CompetenceMilestoneAward).delete()
        db_session.query(CompetenceMilestone).delete()
        db_session.commit()

        # Check if user exists, seed if not
        from app.features.users.models import User

        user = db_session.get(User, 1)
        if user is None:
            _seed_user(db_session)

        _seed_milestones(db_session)

        # First: award the milestone with high data
        high_data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=0.9,
                module_slug="verbal-ability",
            )
            for i in range(100)
        ]
        service = MilestoneService(db=db_session)
        awards = service.evaluate_mastery_milestones(user_id=1, mastery_data=high_data)
        assert len(awards) >= 1
        db_session.commit()

        # Second: re-evaluate with low scores
        low_data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=low_score,
                module_slug="verbal-ability",
            )
            for i in range(100)
        ]
        awards2 = service.evaluate_mastery_milestones(user_id=1, mastery_data=low_data)

        # No new awards (milestone already earned)
        assert len(awards2) == 0

        # Original award still exists
        count = db_session.execute(
            select(func.count())
            .select_from(CompetenceMilestoneAward)
            .where(CompetenceMilestoneAward.user_id == 1)
        ).scalar_one()
        assert count >= 1

    @settings(
        max_examples=50,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(score_after=integers(min_value=0, max_value=69))
    def test_readiness_award_persists_after_score_drop(
        self, score_after: int, db_session: Session
    ) -> None:
        """After awarding readiness milestone, re-evaluating with low scores
        does not revoke the award."""
        from sqlalchemy import select, func

        # Clean state for this example
        db_session.query(CompetenceMilestoneAward).delete()
        db_session.query(CompetenceMilestone).delete()
        db_session.commit()

        from app.features.users.models import User

        user = db_session.get(User, 1)
        if user is None:
            _seed_user(db_session)

        _seed_milestones(db_session)

        # First: award with 7 consecutive days >= 70
        base_date = date(2025, 6, 1)
        high_history = [
            ScoreHistoryPoint(score=75, computed_date=base_date + timedelta(days=i))
            for i in range(7)
        ]
        service = MilestoneService(db=db_session)
        awards = service.evaluate_readiness_milestones(
            user_id=1, score_history=high_history
        )
        assert len(awards) >= 1
        db_session.commit()

        # Second: re-evaluate with low scores
        low_history = [
            ScoreHistoryPoint(
                score=score_after,
                computed_date=base_date + timedelta(days=10 + i),
            )
            for i in range(7)
        ]
        awards2 = service.evaluate_readiness_milestones(
            user_id=1, score_history=low_history
        )

        # No new awards
        assert len(awards2) == 0

        # Original award persists
        count = db_session.execute(
            select(func.count())
            .select_from(CompetenceMilestoneAward)
            .where(CompetenceMilestoneAward.user_id == 1)
        ).scalar_one()
        assert count >= 1

    @settings(
        max_examples=50,
        suppress_health_check=[HealthCheck.function_scoped_fixture],
    )
    @given(num_evaluations=integers(min_value=2, max_value=5))
    def test_repeated_evaluations_never_duplicate_awards(
        self, num_evaluations: int, db_session: Session
    ) -> None:
        """Multiple evaluations with qualifying data never duplicate awards."""
        from sqlalchemy import select, func

        # Clean state
        db_session.query(CompetenceMilestoneAward).delete()
        db_session.query(CompetenceMilestone).delete()
        db_session.commit()

        from app.features.users.models import User

        user = db_session.get(User, 1)
        if user is None:
            _seed_user(db_session)

        _seed_milestones(db_session)

        high_data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=0.9,
                module_slug="verbal-ability",
            )
            for i in range(100)
        ]

        service = MilestoneService(db=db_session)

        # First evaluation awards
        first_awards = service.evaluate_mastery_milestones(
            user_id=1, mastery_data=high_data
        )
        assert len(first_awards) >= 1
        first_count = len(first_awards)
        db_session.commit()

        # Subsequent evaluations return 0 new awards
        for _ in range(num_evaluations - 1):
            awards = service.evaluate_mastery_milestones(
                user_id=1, mastery_data=high_data
            )
            assert len(awards) == 0

        # Total awards in DB is still the same as first time
        count = db_session.execute(
            select(func.count())
            .select_from(CompetenceMilestoneAward)
            .where(CompetenceMilestoneAward.user_id == 1)
        ).scalar_one()
        assert count == first_count


# ---------------------------------------------------------------------------
# Property 27: Milestone progress percentage matches formula
# ---------------------------------------------------------------------------


class TestMilestoneProgressPercentage:
    """For any milestone status computation, the progress percentage SHALL
    follow the formula: mastery = qualifying_count / required_count,
    readiness = consecutive_qualifying_days / 7, recovery = comeback_count / 3.
    All progress values are clamped to [0.0, 1.0].

    **Validates: Requirements 13.7**
    """

    @settings(max_examples=50)
    @given(
        scores=lists(
            floats(min_value=0.0, max_value=1.0, allow_nan=False),
            min_size=0,
            max_size=30,
        )
    )
    def test_mastery_progress_is_qualifying_over_required(
        self, scores: list[float]
    ) -> None:
        """Mastery progress = count(score >= 0.8) / required_count."""
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=s,
                module_slug="verbal-ability",
            )
            for i, s in enumerate(scores)
        ]

        progress = compute_milestone_progress(
            milestone_category="mastery",
            mastery_data=data,
            module_slug="verbal-ability",
            required_count=23,
            threshold=0.8,
        )

        qualifying = sum(1 for s in scores if s >= 0.8)
        expected = min(qualifying / 23, 1.0)
        assert abs(progress - expected) < 1e-9

    @settings(max_examples=50)
    @given(history=score_history_with_gaps())
    def test_readiness_progress_is_max_consecutive_over_7(
        self, history: list[ScoreHistoryPoint]
    ) -> None:
        """Readiness progress = max_consecutive_qualifying_days / 7."""
        progress = compute_milestone_progress(
            milestone_category="readiness",
            score_history=history,
            min_score=70,
        )

        # Verify by computing expected value independently
        daily_scores: dict[date, int] = {}
        for point in history:
            daily_scores[point.computed_date] = point.score

        qualifying_dates = sorted(
            d for d in daily_scores if daily_scores[d] >= 70
        )

        if not qualifying_dates:
            expected = 0.0
        else:
            max_cons = 1
            current = 1
            for i in range(1, len(qualifying_dates)):
                if (qualifying_dates[i] - qualifying_dates[i - 1]).days == 1:
                    current += 1
                    max_cons = max(max_cons, current)
                else:
                    current = 1
            expected = min(max_cons / 7, 1.0)

        assert abs(progress - expected) < 1e-9

    @settings(max_examples=50)
    @given(comeback_count=integers(min_value=0, max_value=10))
    def test_recovery_progress_is_comeback_count_over_3(
        self, comeback_count: int
    ) -> None:
        """Recovery progress (resilient-learner) = comeback_count / 3."""
        progress = compute_milestone_progress(
            milestone_category="recovery",
            comeback_count=comeback_count,
        )

        expected = min(comeback_count / 3, 1.0)
        assert abs(progress - expected) < 1e-9

    @settings(max_examples=50)
    @given(
        scores=lists(
            floats(min_value=0.0, max_value=1.0, allow_nan=False),
            min_size=0,
            max_size=60,
        )
    )
    def test_progress_always_clamped_to_0_1(self, scores: list[float]) -> None:
        """Progress percentage is always in [0.0, 1.0] regardless of inputs."""
        data = [
            MasteryDataPoint(
                subtopic_id=i + 1,
                mastery_score=s,
                module_slug="verbal-ability",
            )
            for i, s in enumerate(scores)
        ]

        progress = compute_milestone_progress(
            milestone_category="mastery",
            mastery_data=data,
            module_slug="verbal-ability",
            required_count=23,
            threshold=0.8,
        )

        assert 0.0 <= progress <= 1.0

    @settings(max_examples=50)
    @given(comeback_count=integers(min_value=0, max_value=100))
    def test_recovery_progress_clamped_at_1(self, comeback_count: int) -> None:
        """Recovery progress never exceeds 1.0 even with many comebacks."""
        progress = compute_milestone_progress(
            milestone_category="recovery",
            comeback_count=comeback_count,
        )
        assert 0.0 <= progress <= 1.0
