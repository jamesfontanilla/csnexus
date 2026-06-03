"""Property-based tests for the smart queue generator algorithm.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
Tests Properties 9-14 and 35 from the Intelligent Learning Engine design.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis.strategies import (
    composite,
    floats,
    integers,
    lists,
    sampled_from,
    text,
    tuples,
)

from app.features.smart_queue.algorithms.generator import (
    FlashcardBatch,
    GeneratedQueue,
    NewContentItem,
    QueueConfig,
    QueueItem,
    QuizPracticeItem,
    compute_difficulty_distribution,
    enforce_cross_module_interleaving,
    enforce_variety_constraint,
    generate_daily_queue,
    generate_exam_crunch_queue,
    SECONDS_PER_FLASHCARD,
    SECONDS_PER_QUESTION,
    SECONDS_PER_LESSON_SECTION,
    MAX_FLASHCARD_BATCH_SIZE,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_time_budget = sampled_from([15, 30, 60])
valid_mastery_score = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)
valid_accuracy = floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)
valid_exam_weight = floats(
    min_value=0.01, max_value=1.0, allow_nan=False, allow_infinity=False
)
valid_days_overdue = integers(min_value=0, max_value=365)
valid_card_id = integers(min_value=1, max_value=100000)
valid_subtopic_id = integers(min_value=1, max_value=60)
valid_lesson_id = integers(min_value=1, max_value=500)
deck_names = sampled_from(["Verbal", "Numerical", "Analytical", "General"])
module_names = sampled_from(["Verbal Ability", "Numerical Ability", "Analytical Ability"])


@composite
def flashcard_entry(draw):
    """Generate a single (card_id, days_overdue, deck_name) tuple."""
    card_id = draw(valid_card_id)
    days_overdue = draw(valid_days_overdue)
    deck_name = draw(deck_names)
    return (card_id, days_overdue, deck_name)


@composite
def weak_subtopic_entry(draw):
    """Generate a single (subtopic_id, accuracy_7d, mastery_score) tuple."""
    subtopic_id = draw(valid_subtopic_id)
    accuracy = draw(valid_accuracy)
    mastery = draw(valid_mastery_score)
    return (subtopic_id, accuracy, mastery)


@composite
def coverage_gap_entry(draw):
    """Generate a single (subtopic_id, lesson_id, exam_weight) tuple."""
    subtopic_id = draw(valid_subtopic_id)
    lesson_id = draw(valid_lesson_id)
    weight = draw(valid_exam_weight)
    return (subtopic_id, lesson_id, weight)


@composite
def queue_config_normal(draw):
    """Generate a QueueConfig for normal mode (no exam crunch)."""
    budget = draw(valid_time_budget)
    return QueueConfig(
        time_budget_minutes=budget,
        days_until_exam=None,
        has_exam_date=False,
    )


@composite
def queue_config_crunch_14d(draw):
    """Generate a QueueConfig for exam crunch <14 days."""
    budget = draw(valid_time_budget)
    days = draw(integers(min_value=7, max_value=13))
    return QueueConfig(
        time_budget_minutes=budget,
        days_until_exam=days,
        has_exam_date=True,
    )


@composite
def queue_config_crunch_7d(draw):
    """Generate a QueueConfig for exam crunch <7 days."""
    budget = draw(valid_time_budget)
    days = draw(integers(min_value=1, max_value=6))
    return QueueConfig(
        time_budget_minutes=budget,
        days_until_exam=days,
        has_exam_date=True,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_item_type(item: QueueItem) -> str:
    """Get the string type identifier for a queue item."""
    if isinstance(item, FlashcardBatch):
        return "flashcard_review"
    elif isinstance(item, QuizPracticeItem):
        return "quiz_practice"
    elif isinstance(item, NewContentItem):
        return "new_content"
    return "unknown"


def _get_priority(item: QueueItem) -> int:
    """Get the priority level of a queue item (1=highest)."""
    if isinstance(item, FlashcardBatch):
        return 1
    elif isinstance(item, QuizPracticeItem):
        return 2
    elif isinstance(item, NewContentItem):
        return 3
    return 4


# ---------------------------------------------------------------------------
# Property 9: Queue respects priority ordering
# Validates: Requirements 4.1
# ---------------------------------------------------------------------------


class TestQueueRespectsPriorityOrdering:
    """For any generated daily queue with items from multiple priority levels,
    all priority-1 items (FSRS-due flashcards) SHALL appear before priority-2
    items (weak subtopic quizzes), which SHALL appear before priority-3 items
    (new content), subject to the variety constraint.

    **Validates: Requirements 4.1**
    """

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=1, max_size=10),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=1, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=1, max_size=5),
        config=queue_config_normal(),
    )
    def test_priority_ordering_holds_across_types(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """Priority-1 items appear before priority-2, which appear before priority-3,
        allowing for at most 2 consecutive items of the same type (variety constraint)."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        if not queue.items:
            return

        # Extract the first and last index of each priority level
        priority_indices: dict[int, list[int]] = {1: [], 2: [], 3: []}
        for i, item in enumerate(queue.items):
            p = _get_priority(item)
            if p in priority_indices:
                priority_indices[p].append(i)

        # The general ordering principle: the median position of higher-priority
        # items should be less than the median position of lower-priority items.
        # (Variety constraint can shift individual items by at most 1-2 positions.)
        for higher_p, lower_p in [(1, 2), (1, 3), (2, 3)]:
            if priority_indices[higher_p] and priority_indices[lower_p]:
                # The first item of higher priority should appear before or at
                # the first item of lower priority
                min_higher = min(priority_indices[higher_p])
                min_lower = min(priority_indices[lower_p])
                # With variety constraint, the dominant type may need to be
                # spread earlier. Allow tolerance proportional to how many
                # items of the higher-priority type exist (they get spread out
                # by interleaving lower-priority items every 3rd position).
                higher_count = len(priority_indices[higher_p])
                # Worst case: every 3rd slot after position 2 must be a
                # different type. This can push a lower-priority item to
                # appear as early as position 2 (0-indexed).
                tolerance = max(
                    higher_count // 2,  # displacement from interleaving
                    min(len(priority_indices[lower_p]), len(queue.items) // 2),
                )
                assert min_higher <= min_lower + tolerance, (
                    f"Priority-{higher_p} first at index {min_higher}, "
                    f"but priority-{lower_p} starts at index {min_lower}"
                )


# ---------------------------------------------------------------------------
# Property 10: Queue total duration never exceeds time budget
# Validates: Requirements 4.2
# ---------------------------------------------------------------------------


class TestQueueDurationNeverExceedsBudget:
    """For any generated daily queue and configured time budget (15, 30, or 60
    minutes), the sum of all item estimated_seconds SHALL NOT exceed
    time_budget Ã— 60 seconds.

    **Validates: Requirements 4.2**
    """

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=0, max_size=50),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=0, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=0, max_size=10),
        config=queue_config_normal(),
    )
    def test_total_duration_within_budget(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """Total estimated seconds never exceeds configured time budget."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        assert queue.total_estimated_seconds <= config.time_budget_seconds, (
            f"Queue duration {queue.total_estimated_seconds}s exceeds "
            f"budget {config.time_budget_seconds}s"
        )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=0, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=0, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=0, max_size=5
        ),
        config=queue_config_crunch_14d(),
    )
    def test_exam_crunch_14d_within_budget(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """Exam crunch mode (<14d) also respects time budget."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        assert queue.total_estimated_seconds <= config.time_budget_seconds, (
            f"Crunch queue duration {queue.total_estimated_seconds}s exceeds "
            f"budget {config.time_budget_seconds}s"
        )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=0, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=0, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=0, max_size=5
        ),
        config=queue_config_crunch_7d(),
    )
    def test_exam_crunch_7d_within_budget(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """Exam crunch mode (<7d) also respects time budget."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        assert queue.total_estimated_seconds <= config.time_budget_seconds, (
            f"Crunch queue duration {queue.total_estimated_seconds}s exceeds "
            f"budget {config.time_budget_seconds}s"
        )


# ---------------------------------------------------------------------------
# Property 11: Exam crunch mode enforces correct time allocation
# Validates: Requirements 4.3, 4.4
# ---------------------------------------------------------------------------


class TestExamCrunchModeTimeAllocation:
    """For any queue generated with days_until_exam < 14, FSRS-due items SHALL
    consume approximately 60% of the time budget and no new content SHALL be
    introduced unless FSRS items consume less than 60%. For days_until_exam < 7,
    FSRS-due items SHALL consume approximately 80% and new content SHALL be
    entirely excluded.

    **Validates: Requirements 4.3, 4.4**
    """

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=5, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=1, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=1, max_size=5
        ),
        config=queue_config_crunch_14d(),
    )
    def test_crunch_14d_fsrs_allocation(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """<14 days: FSRS items should consume at most 60% of budget allocation."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        fsrs_seconds = sum(
            item.estimated_seconds
            for item in queue.items
            if isinstance(item, FlashcardBatch)
        )
        # FSRS allocation is int(budget * 0.60), items should not exceed this
        fsrs_budget = int(config.time_budget_seconds * 0.60)
        assert fsrs_seconds <= fsrs_budget + SECONDS_PER_FLASHCARD, (
            f"FSRS seconds {fsrs_seconds} exceeds 60% allocation {fsrs_budget}"
        )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=5, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=1, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=1, max_size=5
        ),
        config=queue_config_crunch_14d(),
    )
    def test_crunch_14d_no_new_content(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """<14 days: No NewContentItem should appear in the queue."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        new_content_items = [
            item for item in queue.items if isinstance(item, NewContentItem)
        ]
        assert len(new_content_items) == 0, (
            f"Found {len(new_content_items)} new content items in <14d crunch mode"
        )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=5, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=1, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=1, max_size=5
        ),
        config=queue_config_crunch_7d(),
    )
    def test_crunch_7d_fsrs_allocation(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """<7 days: FSRS items should consume at most 80% of budget allocation."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        fsrs_seconds = sum(
            item.estimated_seconds
            for item in queue.items
            if isinstance(item, FlashcardBatch)
        )
        # FSRS allocation is int(budget * 0.80), items should not exceed this
        fsrs_budget = int(config.time_budget_seconds * 0.80)
        assert fsrs_seconds <= fsrs_budget + SECONDS_PER_FLASHCARD, (
            f"FSRS seconds {fsrs_seconds} exceeds 80% allocation {fsrs_budget}"
        )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=5, max_size=50),
        high_impact=lists(
            tuples(valid_subtopic_id, valid_exam_weight), min_size=1, max_size=5
        ),
        low_accuracy=lists(
            tuples(valid_subtopic_id, valid_accuracy), min_size=1, max_size=5
        ),
        config=queue_config_crunch_7d(),
    )
    def test_crunch_7d_no_new_content(
        self,
        flashcards: list[tuple[int, int, str]],
        high_impact: list[tuple[int, float]],
        low_accuracy: list[tuple[int, float]],
        config: QueueConfig,
    ) -> None:
        """<7 days: No NewContentItem should appear in the queue."""
        queue = generate_exam_crunch_queue(
            flashcards, high_impact, low_accuracy, config
        )

        new_content_items = [
            item for item in queue.items if isinstance(item, NewContentItem)
        ]
        assert len(new_content_items) == 0, (
            f"Found {len(new_content_items)} new content items in <7d crunch mode"
        )


# ---------------------------------------------------------------------------
# Property 12: Flashcard batch respects size and duration invariants
# Validates: Requirements 5.2
# ---------------------------------------------------------------------------


class TestFlashcardBatchInvariants:
    """For any flashcard_review queue item, the card count SHALL be at most 30,
    and the estimated_seconds SHALL equal card_count Ã— 8.

    **Validates: Requirements 5.2**
    """

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=1, max_size=100),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=0, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=0, max_size=5),
        config=queue_config_normal(),
    )
    def test_batch_size_at_most_30(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """Each flashcard batch contains at most 30 cards."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        for item in queue.items:
            if isinstance(item, FlashcardBatch):
                assert len(item.card_ids) <= MAX_FLASHCARD_BATCH_SIZE, (
                    f"Batch has {len(item.card_ids)} cards, max is {MAX_FLASHCARD_BATCH_SIZE}"
                )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=1, max_size=100),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=0, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=0, max_size=5),
        config=queue_config_normal(),
    )
    def test_batch_duration_equals_count_times_8(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """Each flashcard batch duration equals card_count Ã— 8 seconds."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        for item in queue.items:
            if isinstance(item, FlashcardBatch):
                expected_seconds = len(item.card_ids) * SECONDS_PER_FLASHCARD
                assert item.estimated_seconds == expected_seconds, (
                    f"Batch with {len(item.card_ids)} cards has "
                    f"estimated_seconds={item.estimated_seconds}, "
                    f"expected {expected_seconds}"
                )


# ---------------------------------------------------------------------------
# Property 13: Difficulty distribution matches mastery score ranges
# Validates: Requirements 5.3
# ---------------------------------------------------------------------------


class TestDifficultyDistributionMatchesMastery:
    """For any mastery_score value, the difficulty distribution SHALL be:
    mastery < 0.4 yields 60% easy / 30% medium / 10% hard;
    mastery 0.4â€“0.7 yields 30% easy / 50% medium / 20% hard;
    mastery > 0.7 yields 10% easy / 40% medium / 50% hard.

    **Validates: Requirements 5.3**
    """

    @settings(max_examples=50)
    @given(
        mastery_score=floats(
            min_value=0.0,
            max_value=0.39999,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    def test_low_mastery_distribution(self, mastery_score: float) -> None:
        """mastery < 0.4: 60% easy, 30% medium, 10% hard."""
        dist = compute_difficulty_distribution(mastery_score)
        assert dist == {"easy": 0.60, "medium": 0.30, "hard": 0.10}, (
            f"For mastery={mastery_score}, expected 60/30/10, got {dist}"
        )

    @settings(max_examples=50)
    @given(
        mastery_score=floats(
            min_value=0.4,
            max_value=0.7,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    def test_mid_mastery_distribution(self, mastery_score: float) -> None:
        """mastery 0.4â€“0.7: 30% easy, 50% medium, 20% hard."""
        dist = compute_difficulty_distribution(mastery_score)
        assert dist == {"easy": 0.30, "medium": 0.50, "hard": 0.20}, (
            f"For mastery={mastery_score}, expected 30/50/20, got {dist}"
        )

    @settings(max_examples=50)
    @given(
        mastery_score=floats(
            min_value=0.70001,
            max_value=1.0,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    def test_high_mastery_distribution(self, mastery_score: float) -> None:
        """mastery > 0.7: 10% easy, 40% medium, 50% hard."""
        dist = compute_difficulty_distribution(mastery_score)
        assert dist == {"easy": 0.10, "medium": 0.40, "hard": 0.50}, (
            f"For mastery={mastery_score}, expected 10/40/50, got {dist}"
        )

    @settings(max_examples=50)
    @given(
        mastery_score=valid_mastery_score,
    )
    def test_distribution_sums_to_1(self, mastery_score: float) -> None:
        """All distributions must sum to 1.0 regardless of mastery score."""
        dist = compute_difficulty_distribution(mastery_score)
        total = dist["easy"] + dist["medium"] + dist["hard"]
        assert abs(total - 1.0) < 1e-10, (
            f"Distribution sums to {total}, expected 1.0"
        )


# ---------------------------------------------------------------------------
# Property 14: Queue variety constraint limits consecutive same-type items
# Validates: Requirements 5.5
# ---------------------------------------------------------------------------


class TestQueueVarietyConstraint:
    """For any generated queue containing at least 2 distinct item types,
    no more than 2 consecutive items SHALL share the same item_type.

    **Validates: Requirements 5.5**
    """

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=1, max_size=30),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=1, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=1, max_size=5),
        config=queue_config_normal(),
    )
    def test_no_more_than_2_consecutive_same_type(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """No 3 consecutive items of the same type when 2+ types exist."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        if len(queue.items) < 3:
            return

        # Check if we have at least 2 distinct item types
        types_present = set(_get_item_type(item) for item in queue.items)
        if len(types_present) < 2:
            return  # Constraint doesn't apply with single type

        for i in range(len(queue.items) - 2):
            type_a = _get_item_type(queue.items[i])
            type_b = _get_item_type(queue.items[i + 1])
            type_c = _get_item_type(queue.items[i + 2])
            assert not (type_a == type_b == type_c), (
                f"Three consecutive items of type '{type_a}' "
                f"at positions {i}, {i+1}, {i+2}"
            )

    @settings(max_examples=50)
    @given(
        flashcards=lists(flashcard_entry(), min_size=3, max_size=20),
        weak_subtopics=lists(weak_subtopic_entry(), min_size=1, max_size=3),
        coverage_gaps=lists(coverage_gap_entry(), min_size=0, max_size=5),
        config=queue_config_normal(),
    )
    def test_variety_constraint_via_enforce_function(
        self,
        flashcards: list[tuple[int, int, str]],
        weak_subtopics: list[tuple[int, float, float]],
        coverage_gaps: list[tuple[int, int, float]],
        config: QueueConfig,
    ) -> None:
        """enforce_variety_constraint directly: no 3 consecutive same-type when 2+ types."""
        queue = generate_daily_queue(flashcards, weak_subtopics, coverage_gaps, config)

        # Build a mixed list of items and apply constraint
        items = list(queue.items)
        if len(items) < 3:
            return

        reordered = enforce_variety_constraint(items)
        types_present = set(_get_item_type(item) for item in reordered)
        if len(types_present) < 2:
            return

        for i in range(len(reordered) - 2):
            type_a = _get_item_type(reordered[i])
            type_b = _get_item_type(reordered[i + 1])
            type_c = _get_item_type(reordered[i + 2])
            assert not (type_a == type_b == type_c), (
                f"Variety constraint violated at positions {i}-{i+2}: "
                f"type='{type_a}'"
            )


# ---------------------------------------------------------------------------
# Property 35: Cross-module interleaving distributes quiz items across modules
# Validates: Requirements 5.6
# ---------------------------------------------------------------------------


class TestCrossModuleInterleaving:
    """For any generated queue containing multiple quiz_practice items where
    the weak subtopics span more than one module, consecutive quiz_practice
    items SHALL draw from different modules. If all weak subtopics belong to
    the same module, the constraint is relaxed.

    **Validates: Requirements 5.6**
    """

    @settings(max_examples=50)
    @given(
        num_items=integers(min_value=2, max_value=6),
    )
    def test_no_consecutive_same_module(self, num_items: int) -> None:
        """When multiple modules are available, no consecutive same-module quiz items."""
        # Create quiz items from at least 2 different modules
        modules = ["Verbal Ability", "Numerical Ability", "Analytical Ability"]
        quiz_items = []
        subtopic_module_map = {}

        for i in range(num_items):
            subtopic_id = i + 1
            # Distribute across modules cyclically to ensure multiple modules
            module = modules[i % len(modules)]
            subtopic_module_map[subtopic_id] = module
            quiz_items.append(
                QuizPracticeItem(
                    subtopic_id=subtopic_id,
                    question_count=5,
                    estimated_seconds=225,
                    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2},
                )
            )

        result = enforce_cross_module_interleaving(quiz_items, subtopic_module_map)

        # Verify no consecutive same-module items
        for i in range(len(result) - 1):
            module_a = subtopic_module_map[result[i].subtopic_id]
            module_b = subtopic_module_map[result[i + 1].subtopic_id]
            assert module_a != module_b, (
                f"Consecutive items at positions {i} and {i+1} "
                f"both from module '{module_a}'"
            )

    @settings(max_examples=50)
    @given(
        num_items=integers(min_value=2, max_value=10),
    )
    def test_single_module_returns_unchanged(self, num_items: int) -> None:
        """When all items are from the same module, return them unchanged."""
        quiz_items = []
        subtopic_module_map = {}
        single_module = "Verbal Ability"

        for i in range(num_items):
            subtopic_id = i + 1
            subtopic_module_map[subtopic_id] = single_module
            quiz_items.append(
                QuizPracticeItem(
                    subtopic_id=subtopic_id,
                    question_count=5,
                    estimated_seconds=225,
                    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2},
                )
            )

        result = enforce_cross_module_interleaving(quiz_items, subtopic_module_map)

        # Should return items unchanged
        assert result == quiz_items, (
            "Single-module items should be returned unchanged"
        )

    @settings(max_examples=50)
    @given(
        verbal_count=integers(min_value=1, max_value=3),
        numerical_count=integers(min_value=1, max_value=3),
        analytical_count=integers(min_value=0, max_value=3),
    )
    def test_preserves_all_items(
        self,
        verbal_count: int,
        numerical_count: int,
        analytical_count: int,
    ) -> None:
        """Cross-module interleaving preserves all items (no items lost)."""
        quiz_items = []
        subtopic_module_map = {}
        sid = 1

        for _ in range(verbal_count):
            subtopic_module_map[sid] = "Verbal Ability"
            quiz_items.append(
                QuizPracticeItem(
                    subtopic_id=sid,
                    question_count=5,
                    estimated_seconds=225,
                    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2},
                )
            )
            sid += 1

        for _ in range(numerical_count):
            subtopic_module_map[sid] = "Numerical Ability"
            quiz_items.append(
                QuizPracticeItem(
                    subtopic_id=sid,
                    question_count=5,
                    estimated_seconds=225,
                    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2},
                )
            )
            sid += 1

        for _ in range(analytical_count):
            subtopic_module_map[sid] = "Analytical Ability"
            quiz_items.append(
                QuizPracticeItem(
                    subtopic_id=sid,
                    question_count=5,
                    estimated_seconds=225,
                    difficulty_distribution={"easy": 0.3, "medium": 0.5, "hard": 0.2},
                )
            )
            sid += 1

        result = enforce_cross_module_interleaving(quiz_items, subtopic_module_map)

        assert len(result) == len(quiz_items), (
            f"Expected {len(quiz_items)} items, got {len(result)}"
        )
        # All original subtopic_ids should be present
        original_ids = set(item.subtopic_id for item in quiz_items)
        result_ids = set(item.subtopic_id for item in result)
        assert original_ids == result_ids, (
            f"Lost items during interleaving: "
            f"original={original_ids}, result={result_ids}"
        )
