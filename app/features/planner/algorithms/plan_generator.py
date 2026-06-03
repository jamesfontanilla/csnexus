"""Study plan generation algorithm (Intelligent Learning Engine).

Generates a personalized, phased study schedule based on exam date,
mastery data, and available time. Deterministic given the same inputs.

Phases:
  1. Coverage — introduce all unmastered subtopics (max 3 new/day,
     review every 3rd study day).
  2. Weakness — deepen low-mastery subtopics via quiz/review.
  3. Review — final 20% of timeline for review + mock exams.

Mock exams: 1/week from week 2, 2/week in final 2 weeks.
Mastered subtopics (mastery_score >= 0.8) are skipped for returning users.

Requirements: 16.2, 16.3, 16.4, 17.1, 17.2, 17.3, 17.4, 17.5
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, timedelta


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PlanConfig:
    """Configuration for plan generation."""

    target_exam_date: date
    available_hours_per_day: float  # 0.25, 0.5, or 1.0
    exam_category: str  # "Professional" or "Sub-Professional"
    mastered_subtopic_ids: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class DailyAssignment:
    """A single day's assignment in the plan."""

    day_number: int
    date: date
    phase: str  # "coverage", "weakness", "review"
    new_subtopics: list[int] = field(default_factory=list)  # max 3 per day
    review_subtopics: list[int] = field(default_factory=list)
    mock_exam_scheduled: bool = False


@dataclass(frozen=True)
class GeneratedPlan:
    """The complete generated study plan."""

    assignments: list[DailyAssignment]
    total_days: int
    subtopics_per_week: int
    mock_exams_scheduled: int
    estimated_readiness_at_exam: float


# ---------------------------------------------------------------------------
# Exam date validation
# ---------------------------------------------------------------------------


class ExamDateValidationError(ValueError):
    """Raised when exam date is invalid (past or >365 days)."""

    pass


def validate_exam_date(exam_date: date, today: date | None = None) -> int:
    """Validate exam date is 1–365 days in the future.

    Args:
        exam_date: The target exam date.
        today: Override for testability. Defaults to date.today().

    Returns:
        Number of days until exam.

    Raises:
        ExamDateValidationError: If date is in the past or >365 days away.
    """
    if today is None:
        today = date.today()

    days_until_exam = (exam_date - today).days

    if days_until_exam < 1:
        raise ExamDateValidationError(
            "exam_date must be in the future (at least 1 day from today)"
        )
    if days_until_exam > 365:
        raise ExamDateValidationError(
            "exam_date must be within 365 days from today"
        )

    return days_until_exam


# ---------------------------------------------------------------------------
# Plan generation (pure function)
# ---------------------------------------------------------------------------


def generate_study_plan(
    all_subtopic_ids: list[int],
    config: PlanConfig,
    *,
    today: date | None = None,
) -> GeneratedPlan:
    """Generate a phased study plan.

    Algorithm:
      1. Validate exam date (1–365 days).
      2. Filter out already-mastered subtopics.
      3. Divide timeline: coverage (first ~80%) and review (final 20%).
      4. Coverage phase: max 3 new subtopics/day, review every 3rd day.
      5. Weakness phase fills any remaining coverage-phase days after all
         subtopics are introduced.
      6. Review phase: final 20% — review + mock exams.
      7. Mock exams: 1/week from week 2, 2/week in final 2 weeks.

    Pure function — no database access.

    Args:
        all_subtopic_ids: All subtopic IDs to consider.
        config: Plan configuration.
        today: Override for testability. Defaults to date.today().

    Returns:
        A GeneratedPlan with daily assignments.

    Raises:
        ExamDateValidationError: If exam date is invalid.
    """
    if today is None:
        today = date.today()

    total_days = validate_exam_date(config.target_exam_date, today)

    # Filter out mastered subtopics
    mastered_set = set(config.mastered_subtopic_ids)
    subtopics_to_cover = [
        sid for sid in all_subtopic_ids if sid not in mastered_set
    ]

    # Phase boundaries
    review_phase_days = max(1, math.ceil(total_days * 0.20))
    coverage_weakness_days = total_days - review_phase_days

    # Build assignments
    assignments: list[DailyAssignment] = []
    mock_exams_scheduled = 0

    # Track subtopic introduction
    subtopics_introduced: list[int] = []
    subtopic_queue = list(subtopics_to_cover)  # copy for consumption

    # Calculate mock exam schedule
    mock_exam_days = _compute_mock_exam_days(total_days)

    # --- Coverage + Weakness phase (first 80%) ---
    study_day_counter = 0  # counts actual study days for review spacing
    for day_num in range(1, coverage_weakness_days + 1):
        current_date = today + timedelta(days=day_num)
        study_day_counter += 1

        is_mock_day = day_num in mock_exam_days
        is_review_day = (study_day_counter % 3 == 0)  # every 3rd study day

        new_subs: list[int] = []
        review_subs: list[int] = []
        mock_scheduled = False

        if is_mock_day:
            mock_scheduled = True
            mock_exams_scheduled += 1

        # Determine phase for this day
        all_introduced = len(subtopic_queue) == 0

        if is_review_day and subtopics_introduced:
            # Review day: review previously introduced subtopics
            review_subs = _pick_review_subtopics(
                subtopics_introduced, day_num
            )
            phase = "weakness" if all_introduced else "coverage"
        elif not all_introduced:
            # Coverage: introduce up to 3 new subtopics
            count = min(3, len(subtopic_queue))
            new_subs = subtopic_queue[:count]
            subtopic_queue = subtopic_queue[count:]
            subtopics_introduced.extend(new_subs)
            phase = "coverage"
        else:
            # Weakness: all subtopics introduced, focus on review
            review_subs = _pick_review_subtopics(
                subtopics_introduced, day_num
            )
            phase = "weakness"

        assignments.append(
            DailyAssignment(
                day_number=day_num,
                date=current_date,
                phase=phase,
                new_subtopics=new_subs,
                review_subtopics=review_subs,
                mock_exam_scheduled=mock_scheduled,
            )
        )

    # --- Review phase (final 20%) ---
    for day_num in range(coverage_weakness_days + 1, total_days + 1):
        current_date = today + timedelta(days=day_num)

        is_mock_day = day_num in mock_exam_days
        mock_scheduled = False
        if is_mock_day:
            mock_scheduled = True
            mock_exams_scheduled += 1

        review_subs = _pick_review_subtopics(subtopics_introduced, day_num)

        assignments.append(
            DailyAssignment(
                day_number=day_num,
                date=current_date,
                phase="review",
                new_subtopics=[],
                review_subtopics=review_subs,
                mock_exam_scheduled=mock_scheduled,
            )
        )

    # Calculate subtopics per week
    if total_days >= 7:
        subtopics_per_week = math.ceil(
            len(subtopics_to_cover) / max(1, total_days // 7)
        )
    else:
        subtopics_per_week = len(subtopics_to_cover)

    # Estimate readiness at exam (simple projection)
    estimated_readiness = _estimate_readiness(
        total_subtopics=len(all_subtopic_ids),
        subtopics_to_cover=len(subtopics_to_cover),
        mastered_count=len(mastered_set),
        total_days=total_days,
        hours_per_day=config.available_hours_per_day,
    )

    return GeneratedPlan(
        assignments=assignments,
        total_days=total_days,
        subtopics_per_week=subtopics_per_week,
        mock_exams_scheduled=mock_exams_scheduled,
        estimated_readiness_at_exam=estimated_readiness,
    )


# ---------------------------------------------------------------------------
# Plan regeneration (pure function)
# ---------------------------------------------------------------------------


def regenerate_plan_from_today(
    existing_plan: GeneratedPlan,
    new_exam_date: date,
    completed_days: int,
    config: PlanConfig,
    all_subtopic_ids: list[int],
    *,
    today: date | None = None,
) -> GeneratedPlan:
    """Regenerate plan from current date forward.

    Preserves information about completed days and redistributes remaining
    subtopics across the new timeline.

    Args:
        existing_plan: The current plan.
        new_exam_date: Updated exam date.
        completed_days: Number of days already completed.
        config: Plan configuration (updated with new exam date).
        all_subtopic_ids: All subtopic IDs.
        today: Override for testability.

    Returns:
        A new GeneratedPlan from today forward.

    Raises:
        ExamDateValidationError: If new exam date is invalid.
    """
    if today is None:
        today = date.today()

    # Determine which subtopics were already introduced in completed days
    already_introduced: set[int] = set()
    for assignment in existing_plan.assignments[:completed_days]:
        already_introduced.update(assignment.new_subtopics)

    # Add already-mastered to the skip list
    mastered_plus_introduced = list(
        set(config.mastered_subtopic_ids) | already_introduced
    )

    new_config = PlanConfig(
        target_exam_date=new_exam_date,
        available_hours_per_day=config.available_hours_per_day,
        exam_category=config.exam_category,
        mastered_subtopic_ids=mastered_plus_introduced,
    )

    return generate_study_plan(
        all_subtopic_ids=all_subtopic_ids,
        config=new_config,
        today=today,
    )


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _compute_mock_exam_days(total_days: int) -> set[int]:
    """Compute which day numbers should have mock exams scheduled.

    Rules:
      - 1/week starting from week 2 (day 8+).
      - 2/week in the final 2 weeks (last 14 days).

    Returns:
        Set of day numbers (1-indexed) that have mock exams.
    """
    mock_days: set[int] = set()

    if total_days < 8:
        # Not enough days for week 2 — no mock exams
        return mock_days

    final_two_weeks_start = max(1, total_days - 13)

    # Regular mocks: 1/week from week 2 until final 2 weeks
    # Week 2 starts at day 8
    week_2_start = 8
    regular_end = min(final_two_weeks_start - 1, total_days)

    # Place one mock every 7 days starting from day 8
    day = week_2_start
    while day <= regular_end:
        mock_days.add(day)
        day += 7

    # Final 2 weeks: 2/week (every ~3-4 days)
    if total_days >= 15:
        # Place mocks every 3-4 days in the final 14 days
        day = final_two_weeks_start
        spacing = 3  # ~2/week = every 3.5 days
        while day <= total_days:
            mock_days.add(day)
            day += spacing
            # Alternate spacing to get ~2/week
            spacing = 4 if spacing == 3 else 3

    return mock_days


def _pick_review_subtopics(
    introduced: list[int], day_number: int
) -> list[int]:
    """Pick subtopics for review on a given day.

    Uses round-robin selection from introduced subtopics.

    Args:
        introduced: All subtopics introduced so far.
        day_number: Current day number for deterministic selection.

    Returns:
        List of 1-3 subtopic IDs for review.
    """
    if not introduced:
        return []

    count = min(3, len(introduced))
    start_idx = (day_number - 1) % len(introduced)

    result: list[int] = []
    for i in range(count):
        idx = (start_idx + i) % len(introduced)
        result.append(introduced[idx])

    return result


def _estimate_readiness(
    *,
    total_subtopics: int,
    subtopics_to_cover: int,
    mastered_count: int,
    total_days: int,
    hours_per_day: float,
) -> float:
    """Estimate projected readiness at exam date.

    Simple heuristic: mastery base (already mastered portion) +
    projected learning rate × available study time.

    Returns:
        Projected readiness score (0.0–100.0), clamped.
    """
    if total_subtopics == 0:
        return 0.0

    # Base readiness from already-mastered subtopics
    mastery_base = (mastered_count / total_subtopics) * 100.0

    # Projected coverage improvement
    # Assume ~60% mastery achievable per subtopic with available study time
    total_study_hours = total_days * hours_per_day
    # Rough model: each subtopic needs ~2 hours to reach 60% mastery
    achievable_subtopics = min(
        subtopics_to_cover, total_study_hours / 2.0
    )
    projected_new_mastery = (achievable_subtopics / total_subtopics) * 60.0

    estimated = mastery_base + projected_new_mastery
    return round(min(100.0, max(0.0, estimated)), 1)


# ---------------------------------------------------------------------------
# Legacy API (backward compatibility)
# ---------------------------------------------------------------------------
# The service.py and existing tests use the old function signature.
# These wrappers maintain backward compatibility.


@dataclass
class PlanDay:
    """A single planned activity for a day (legacy format)."""

    plan_date: date
    subtopic_id: int
    activity_type: str  # 'lesson', 'quiz', 'review', 'mock_exam'
    estimated_minutes: int


@dataclass
class SubtopicMasteryInput:
    """Simplified mastery data for plan generation (legacy format)."""

    subtopic_id: int
    mastery_score: float  # 0.0 to 1.0


# Keep the old generate_study_plan callable with keyword arguments.
# When called with the old-style keyword args (target_exam_date, target_score, etc.)
# it dispatches to the legacy implementation.
_original_generate_study_plan = generate_study_plan


def generate_study_plan(  # type: ignore[no-redef]
    all_subtopic_ids: list[int] | None = None,
    config: PlanConfig | None = None,
    *,
    today: date | None = None,
    # Legacy keyword arguments
    target_exam_date: date | None = None,
    available_hours_per_day: float | None = None,
    target_score: float | None = None,
    mastery_data: list[SubtopicMasteryInput] | None = None,
    now: date | None = None,
) -> GeneratedPlan | list[PlanDay]:
    """Unified entry point supporting both new and legacy call signatures.

    New API: generate_study_plan(all_subtopic_ids, config, today=...)
    Legacy API: generate_study_plan(target_exam_date=..., all_subtopic_ids=..., ...)
    """
    # Detect legacy call: if target_exam_date is provided as keyword
    if target_exam_date is not None:
        return _legacy_generate_study_plan(
            target_exam_date=target_exam_date,
            available_hours_per_day=available_hours_per_day or 1.0,
            target_score=target_score or 0.8,
            mastery_data=mastery_data or [],
            all_subtopic_ids=all_subtopic_ids or [],
            now=now or (today or date.today()),
        )

    # New API call
    if all_subtopic_ids is None or config is None:
        raise TypeError(
            "generate_study_plan requires (all_subtopic_ids, config) "
            "or legacy keyword arguments"
        )
    return _original_generate_study_plan(all_subtopic_ids, config, today=today)


def _legacy_generate_study_plan(
    *,
    target_exam_date: date,
    available_hours_per_day: float,
    target_score: float,
    mastery_data: list[SubtopicMasteryInput],
    all_subtopic_ids: list[int],
    now: date,
) -> list[PlanDay]:
    """Legacy implementation that returns list[PlanDay].

    Preserved for backward compatibility with existing service.py.
    """
    days_until_exam = (target_exam_date - now).days
    if days_until_exam <= 0:
        return []

    available_minutes_per_day = int(available_hours_per_day * 60)

    # Build mastery lookup
    mastery_map: dict[int, float] = {
        m.subtopic_id: m.mastery_score for m in mastery_data
    }

    # Prioritize subtopics: lower mastery = higher priority
    prioritized: list[tuple[int, float]] = []
    for sid in all_subtopic_ids:
        score = mastery_map.get(sid, 0.0)
        priority = 1.0 - score
        prioritized.append((sid, priority))

    # Sort by priority descending (weakest first)
    prioritized.sort(key=lambda x: x[1], reverse=True)

    # Categorize subtopics
    weak = [(sid, p) for sid, p in prioritized if p > 0.6]
    medium = [(sid, p) for sid, p in prioritized if 0.3 < p <= 0.6]
    strong = [(sid, p) for sid, p in prioritized if p <= 0.3]

    plan_days: list[PlanDay] = []
    current_date = now + timedelta(days=1)
    mock_exam_start = now + timedelta(days=int(days_until_exam * 0.8))

    day_index = 0
    while current_date <= target_exam_date:
        day_minutes_remaining = available_minutes_per_day
        day_index += 1

        # Mock exam days in the last 20%
        if current_date >= mock_exam_start and day_index % 3 == 0:
            if weak:
                sid = weak[day_index % len(weak)][0] if weak else all_subtopic_ids[0]
            elif all_subtopic_ids:
                sid = all_subtopic_ids[0]
            else:
                current_date += timedelta(days=1)
                continue
            plan_days.append(PlanDay(
                plan_date=current_date,
                subtopic_id=sid,
                activity_type="mock_exam",
                estimated_minutes=min(60, day_minutes_remaining),
            ))
            day_minutes_remaining -= 60
            if day_minutes_remaining <= 0:
                current_date += timedelta(days=1)
                continue

        # Weak subtopics: lessons and quizzes
        if weak and day_minutes_remaining >= 20:
            idx = day_index % len(weak)
            sid = weak[idx][0]
            activity = "lesson" if day_index % 2 == 0 else "quiz"
            minutes = min(30, day_minutes_remaining)
            plan_days.append(PlanDay(
                plan_date=current_date,
                subtopic_id=sid,
                activity_type=activity,
                estimated_minutes=minutes,
            ))
            day_minutes_remaining -= minutes

        # Medium subtopics: review
        if medium and day_minutes_remaining >= 15:
            idx = day_index % len(medium)
            sid = medium[idx][0]
            minutes = min(20, day_minutes_remaining)
            plan_days.append(PlanDay(
                plan_date=current_date,
                subtopic_id=sid,
                activity_type="review",
                estimated_minutes=minutes,
            ))
            day_minutes_remaining -= minutes

        # Strong subtopics: occasional reinforcement
        if strong and day_minutes_remaining >= 10 and day_index % 3 == 0:
            idx = day_index % len(strong)
            sid = strong[idx][0]
            minutes = min(15, day_minutes_remaining)
            plan_days.append(PlanDay(
                plan_date=current_date,
                subtopic_id=sid,
                activity_type="review",
                estimated_minutes=minutes,
            ))
            day_minutes_remaining -= minutes

        current_date += timedelta(days=1)

    return plan_days
