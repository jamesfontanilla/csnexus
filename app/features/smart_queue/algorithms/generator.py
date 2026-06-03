"""Pure queue generation logic: builds ordered study items within a time budget.

All functions in this module are pure — no database access, no side effects.
The service layer orchestrates data retrieval and calls these functions.

Validates: Requirements 4.1, 4.2, 4.3, 4.4, 5.2, 5.3, 5.4, 5.5, 5.6
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SECONDS_PER_FLASHCARD = 8
SECONDS_PER_QUESTION = 45
SECONDS_PER_LESSON_SECTION = 300  # 5 minutes
MAX_FLASHCARD_BATCH_SIZE = 30
MIN_QUIZ_QUESTIONS = 5
MAX_QUIZ_QUESTIONS = 10


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QueueConfig:
    """Configuration for queue generation."""

    time_budget_minutes: int  # 15, 30, or 60
    days_until_exam: int | None
    has_exam_date: bool

    @property
    def time_budget_seconds(self) -> int:
        return self.time_budget_minutes * 60


@dataclass(frozen=True)
class FlashcardBatch:
    """A batch of FSRS-due flashcards to review."""

    card_ids: list[int]  # max 30
    estimated_seconds: int  # count × 8
    deck_name: str


@dataclass(frozen=True)
class QuizPracticeItem:
    """A set of quiz questions from a weak subtopic."""

    subtopic_id: int
    question_count: int  # 5-10
    estimated_seconds: int  # count × 45
    difficulty_distribution: dict[str, float]  # easy/medium/hard percentages


@dataclass(frozen=True)
class NewContentItem:
    """A lesson section from an uncovered subtopic."""

    subtopic_id: int
    lesson_id: int
    section_index: int
    estimated_seconds: int  # 300 (5 min)


QueueItem = Union[FlashcardBatch, QuizPracticeItem, NewContentItem]


@dataclass(frozen=True)
class GeneratedQueue:
    """The result of queue generation."""

    items: list[QueueItem]
    total_estimated_seconds: int
    items_by_type: dict[str, int]


# ---------------------------------------------------------------------------
# Core Generation Functions
# ---------------------------------------------------------------------------


def generate_daily_queue(
    due_flashcards: list[tuple[int, int, str]],
    # (card_id, days_overdue, deck_name)
    weak_subtopics: list[tuple[int, float, float]],
    # (subtopic_id, accuracy_7d, mastery_score)
    coverage_gaps: list[tuple[int, int, float]],
    # (subtopic_id, lesson_id, exam_weight)
    config: QueueConfig,
) -> GeneratedQueue:
    """Generate ordered queue respecting priority and time budget.

    Priority ordering:
    1. FSRS-due flashcards sorted by days_overdue descending
    2. Weakest 3 subtopics from last 7 days of quiz performance
    3. New content from coverage gap subtopics ordered by exam weight

    If priority-1 alone exceeds budget, truncate flashcards and omit
    lower-priority items.

    Args:
        due_flashcards: Flashcards due for review with days overdue and deck name.
        weak_subtopics: Weakest subtopics (max 3 used) with accuracy and mastery.
        coverage_gaps: Uncovered subtopics with lesson IDs and exam weights.
        config: Queue configuration (time budget, exam info).

    Returns:
        GeneratedQueue with ordered items capped at time budget.
    """
    budget = config.time_budget_seconds
    items: list[QueueItem] = []
    used_seconds = 0

    # Priority 1: FSRS-due flashcards sorted by days_overdue descending
    sorted_flashcards = sorted(due_flashcards, key=lambda x: x[1], reverse=True)
    flashcard_items, used_seconds = _build_flashcard_batches(
        sorted_flashcards, budget, used_seconds
    )
    items.extend(flashcard_items)

    # Priority 2: Weakest 3 subtopics for quiz practice
    remaining_budget = budget - used_seconds
    if remaining_budget > 0:
        limited_weak = weak_subtopics[:3]
        quiz_items, used_seconds = _build_quiz_items(
            limited_weak, budget, used_seconds
        )
        items.extend(quiz_items)

    # Priority 3: New content from coverage gaps by exam weight descending
    remaining_budget = budget - used_seconds
    if remaining_budget > 0:
        sorted_gaps = sorted(coverage_gaps, key=lambda x: x[2], reverse=True)
        content_items, used_seconds = _build_content_items(
            sorted_gaps, budget, used_seconds
        )
        items.extend(content_items)

    # Apply variety constraint
    items = enforce_variety_constraint(items)

    return _build_generated_queue(items)


def generate_exam_crunch_queue(
    due_flashcards: list[tuple[int, int, str]],
    high_impact_subtopics: list[tuple[int, float]],
    # (subtopic_id, point_impact)
    low_accuracy_subtopics: list[tuple[int, float]],
    # (subtopic_id, mock_accuracy)
    config: QueueConfig,
) -> GeneratedQueue:
    """Generate queue for exam crunch mode (<14 days or <7 days until exam).

    Mode 1 (<14 days): 60% FSRS, 30% high-impact quiz, 10% review.
        No new content unless FSRS items consume less than 60% of budget.
    Mode 2 (<7 days): 80% FSRS, 20% quiz on subtopics with <60% mock accuracy.
        No new content at all.

    Args:
        due_flashcards: Flashcards due for review.
        high_impact_subtopics: Subtopics with highest point impact.
        low_accuracy_subtopics: Subtopics where mock accuracy < 60%.
        config: Queue configuration.

    Returns:
        GeneratedQueue with exam-crunch-optimized ordering.
    """
    budget = config.time_budget_seconds
    items: list[QueueItem] = []
    used_seconds = 0

    days = config.days_until_exam
    if days is not None and days < 7:
        # Mode 2: 80% FSRS, 20% quiz on low-accuracy subtopics
        fsrs_budget = int(budget * 0.80)
        quiz_budget = budget - fsrs_budget

        sorted_flashcards = sorted(due_flashcards, key=lambda x: x[1], reverse=True)
        flashcard_items, used_seconds = _build_flashcard_batches(
            sorted_flashcards, fsrs_budget, 0
        )
        items.extend(flashcard_items)

        # Quiz on low-accuracy subtopics
        quiz_subtopics = [
            (sid, acc, 0.5) for sid, acc in low_accuracy_subtopics if acc < 60.0
        ]
        quiz_items, quiz_used = _build_quiz_items(
            quiz_subtopics, used_seconds + quiz_budget, used_seconds
        )
        items.extend(quiz_items)
        used_seconds += quiz_used - used_seconds if quiz_used > used_seconds else 0
    else:
        # Mode 1: 60% FSRS, 30% high-impact quiz, 10% review
        fsrs_budget = int(budget * 0.60)
        quiz_budget = int(budget * 0.30)
        review_budget = budget - fsrs_budget - quiz_budget

        sorted_flashcards = sorted(due_flashcards, key=lambda x: x[1], reverse=True)
        flashcard_items, used_seconds = _build_flashcard_batches(
            sorted_flashcards, fsrs_budget, 0
        )
        items.extend(flashcard_items)

        # High-impact quiz practice
        quiz_subtopics = [
            (sid, 0.0, 0.5) for sid, _ in high_impact_subtopics
        ]
        quiz_items, quiz_used = _build_quiz_items(
            quiz_subtopics, used_seconds + quiz_budget, used_seconds
        )
        items.extend(quiz_items)
        used_seconds = quiz_used

        # Review: add flashcards from the remaining budget if available
        # (review is essentially more FSRS cards or previously seen content)
        remaining = sorted_flashcards[
            sum(len(b.card_ids) for b in flashcard_items if isinstance(b, FlashcardBatch)):
        ]
        if remaining and review_budget > 0:
            review_items, used_seconds = _build_flashcard_batches(
                remaining, used_seconds + review_budget, used_seconds
            )
            items.extend(review_items)

    # Apply variety constraint
    items = enforce_variety_constraint(items)

    return _build_generated_queue(items)


# ---------------------------------------------------------------------------
# Difficulty Distribution
# ---------------------------------------------------------------------------


def compute_difficulty_distribution(mastery_score: float) -> dict[str, float]:
    """Return difficulty percentages based on mastery level.

    Args:
        mastery_score: User's mastery score for the subtopic (0.0-1.0).

    Returns:
        Dict with keys "easy", "medium", "hard" mapping to percentages (0.0-1.0).

    Ranges:
        mastery < 0.4: 60% easy, 30% medium, 10% hard
        0.4 <= mastery <= 0.7: 30% easy, 50% medium, 20% hard
        mastery > 0.7: 10% easy, 40% medium, 50% hard
    """
    if mastery_score < 0.4:
        return {"easy": 0.60, "medium": 0.30, "hard": 0.10}
    elif mastery_score <= 0.7:
        return {"easy": 0.30, "medium": 0.50, "hard": 0.20}
    else:
        return {"easy": 0.10, "medium": 0.40, "hard": 0.50}


# ---------------------------------------------------------------------------
# Variety Constraint
# ---------------------------------------------------------------------------


def enforce_variety_constraint(
    items: list[QueueItem],
) -> list[QueueItem]:
    """Reorder items so no more than 2 consecutive share the same type.

    Uses a greedy approach: always places the item type with the most
    remaining items, as long as it doesn't create a run of 3.

    Args:
        items: Ordered list of queue items.

    Returns:
        Reordered list respecting the variety constraint, or the original
        list if fewer than 2 types exist or constraint is infeasible.
    """
    if not items:
        return items

    # Check if we have at least 2 distinct types
    types_present = set(_get_item_type(item) for item in items)
    if len(types_present) < 2:
        return items

    # Feasibility check: most frequent type can appear at most 2*(others+1)
    from collections import Counter
    type_counts = Counter(_get_item_type(item) for item in items)
    max_count = max(type_counts.values())
    others_count = len(items) - max_count
    if max_count > 2 * (others_count + 1):
        return items

    # Priority-preserving greedy with lookahead:
    # Try items in original order, but when placing an item would make it
    # impossible to satisfy the constraint for remaining items, skip it.
    remaining = list(items)
    result: list[QueueItem] = []

    while remaining:
        placed = False
        for i, item in enumerate(remaining):
            if _can_place(result, item):
                # Check if placing this item leaves a solvable state
                tentative_remaining = remaining[:i] + remaining[i + 1:]
                if _is_feasible_after(result + [item], tentative_remaining):
                    result.append(remaining.pop(i))
                    placed = True
                    break

        if not placed:
            # Fallback: place any valid item without lookahead
            for i, item in enumerate(remaining):
                if _can_place(result, item):
                    result.append(remaining.pop(i))
                    placed = True
                    break

        if not placed:
            # Truly infeasible — return original
            return items

    return result


def enforce_cross_module_interleaving(
    quiz_items: list[QuizPracticeItem],
    subtopic_module_map: dict[int, str],
) -> list[QuizPracticeItem]:
    """Reorder quiz_practice items so consecutive items draw from different modules.

    If all items belong to the same module, return them unchanged.

    Args:
        quiz_items: List of quiz practice items to reorder.
        subtopic_module_map: Mapping of subtopic_id to module name
            ("Verbal Ability", "Numerical Ability", "Analytical Ability").

    Returns:
        Reordered list with cross-module interleaving where possible.
    """
    if len(quiz_items) <= 1:
        return quiz_items

    # Check if all items are from the same module
    modules = set(
        subtopic_module_map.get(item.subtopic_id, "Unknown")
        for item in quiz_items
    )
    if len(modules) <= 1:
        return quiz_items

    # Group by module
    by_module: dict[str, list[QuizPracticeItem]] = {}
    for item in quiz_items:
        module = subtopic_module_map.get(item.subtopic_id, "Unknown")
        if module not in by_module:
            by_module[module] = []
        by_module[module].append(item)

    # Round-robin across modules
    result: list[QuizPracticeItem] = []
    module_keys = list(by_module.keys())
    idx = 0

    while any(by_module[m] for m in module_keys):
        module = module_keys[idx % len(module_keys)]
        if by_module[module]:
            result.append(by_module[module].pop(0))
        idx += 1

    return result


# ---------------------------------------------------------------------------
# Private Helpers
# ---------------------------------------------------------------------------


def _build_flashcard_batches(
    flashcards: list[tuple[int, int, str]],
    budget_limit: int,
    used_so_far: int,
) -> tuple[list[FlashcardBatch], int]:
    """Build flashcard batches from sorted flashcards within budget."""
    items: list[FlashcardBatch] = []
    used = used_so_far

    # Group by deck_name
    by_deck: dict[str, list[int]] = {}
    for card_id, _, deck_name in flashcards:
        if deck_name not in by_deck:
            by_deck[deck_name] = []
        by_deck[deck_name].append(card_id)

    for deck_name, card_ids in by_deck.items():
        # Split into batches of max 30
        for i in range(0, len(card_ids), MAX_FLASHCARD_BATCH_SIZE):
            batch_cards = card_ids[i : i + MAX_FLASHCARD_BATCH_SIZE]
            estimated = len(batch_cards) * SECONDS_PER_FLASHCARD

            if used + estimated > budget_limit:
                # Truncate to fit remaining budget
                remaining_budget = budget_limit - used
                cards_that_fit = remaining_budget // SECONDS_PER_FLASHCARD
                if cards_that_fit > 0:
                    truncated = batch_cards[:cards_that_fit]
                    est = len(truncated) * SECONDS_PER_FLASHCARD
                    items.append(
                        FlashcardBatch(
                            card_ids=truncated,
                            estimated_seconds=est,
                            deck_name=deck_name,
                        )
                    )
                    used += est
                return items, used

            items.append(
                FlashcardBatch(
                    card_ids=batch_cards,
                    estimated_seconds=estimated,
                    deck_name=deck_name,
                )
            )
            used += estimated

    return items, used


def _build_quiz_items(
    weak_subtopics: list[tuple[int, float, float]],
    budget_limit: int,
    used_so_far: int,
) -> tuple[list[QuizPracticeItem], int]:
    """Build quiz practice items from weak subtopics within budget."""
    items: list[QuizPracticeItem] = []
    used = used_so_far

    for subtopic_id, _, mastery_score in weak_subtopics:
        # Determine question count (5-10, based on remaining budget)
        remaining = budget_limit - used
        max_questions = min(MAX_QUIZ_QUESTIONS, remaining // SECONDS_PER_QUESTION)
        question_count = max(MIN_QUIZ_QUESTIONS, min(max_questions, MAX_QUIZ_QUESTIONS))

        if question_count < MIN_QUIZ_QUESTIONS:
            break

        estimated = question_count * SECONDS_PER_QUESTION
        if used + estimated > budget_limit:
            break

        difficulty = compute_difficulty_distribution(mastery_score)
        items.append(
            QuizPracticeItem(
                subtopic_id=subtopic_id,
                question_count=question_count,
                estimated_seconds=estimated,
                difficulty_distribution=difficulty,
            )
        )
        used += estimated

    return items, used


def _build_content_items(
    coverage_gaps: list[tuple[int, int, float]],
    budget_limit: int,
    used_so_far: int,
) -> tuple[list[NewContentItem], int]:
    """Build new content items from coverage gaps within budget."""
    items: list[NewContentItem] = []
    used = used_so_far

    for subtopic_id, lesson_id, _ in coverage_gaps:
        if used + SECONDS_PER_LESSON_SECTION > budget_limit:
            break

        items.append(
            NewContentItem(
                subtopic_id=subtopic_id,
                lesson_id=lesson_id,
                section_index=0,
                estimated_seconds=SECONDS_PER_LESSON_SECTION,
            )
        )
        used += SECONDS_PER_LESSON_SECTION

    return items, used


def _build_generated_queue(items: list[QueueItem]) -> GeneratedQueue:
    """Build the final GeneratedQueue from a list of items."""
    total_seconds = sum(_get_estimated_seconds(item) for item in items)
    type_counts: dict[str, int] = {}
    for item in items:
        item_type = _get_item_type(item)
        type_counts[item_type] = type_counts.get(item_type, 0) + 1

    return GeneratedQueue(
        items=items,
        total_estimated_seconds=total_seconds,
        items_by_type=type_counts,
    )


def _get_item_type(item: QueueItem) -> str:
    """Get the string type identifier for a queue item."""
    if isinstance(item, FlashcardBatch):
        return "flashcard_review"
    elif isinstance(item, QuizPracticeItem):
        return "quiz_practice"
    elif isinstance(item, NewContentItem):
        return "new_content"
    return "unknown"


def _get_estimated_seconds(item: QueueItem) -> int:
    """Get estimated seconds for any queue item type."""
    return item.estimated_seconds


def _can_place(result: list[QueueItem], item: QueueItem) -> bool:
    """Check if placing item at end of result violates variety constraint."""
    if len(result) < 2:
        return True

    item_type = _get_item_type(item)
    last_type = _get_item_type(result[-1])
    second_last_type = _get_item_type(result[-2])

    return not (item_type == last_type == second_last_type)


def _is_feasible_after(
    result: list[QueueItem], remaining: list[QueueItem]
) -> bool:
    """Check if the variety constraint can still be satisfied given the current
    result and the remaining items to place.

    Uses the mathematical condition: the most frequent type in remaining
    must not exceed 2 * (other_remaining + 1), adjusted for what's already
    at the tail of result.
    """
    if not remaining:
        return True

    from collections import Counter

    type_counts = Counter(_get_item_type(item) for item in remaining)

    # If the last 1-2 items in result are the same type, that type effectively
    # needs even more "breaks" from remaining items of other types.
    if len(result) >= 1:
        last_type = _get_item_type(result[-1])
        consecutive_at_end = 1
        if len(result) >= 2 and _get_item_type(result[-2]) == last_type:
            consecutive_at_end = 2

        if consecutive_at_end == 2:
            # The next item MUST be a different type
            # If all remaining are the same type as last, infeasible
            if all(_get_item_type(item) == last_type for item in remaining):
                return False

    # General feasibility: no type can have more than 2*(others+1) items
    total = len(remaining)
    max_count = max(type_counts.values())
    others_count = total - max_count
    return max_count <= 2 * (others_count + 1)
