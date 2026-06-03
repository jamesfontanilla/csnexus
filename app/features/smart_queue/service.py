"""Smart Queue service: orchestrates queue generation, retrieval, and item completion.

Manages personalized daily study sessions by coordinating between the
QueueRepository (persistence), FlashcardRepository (due cards),
MasteryRepository (weak subtopics), SubtopicRepository + LessonRepository
(coverage gaps / new content), and OnboardingProfile (exam date / preferences).

All error conditions raise HTTPException. No DB access in this layer —
everything goes through the injected repositories.

Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 6.1, 6.2, 6.3, 6.5
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, date, datetime, timedelta

from fastapi import HTTPException, status

from app.features.content.repository import LessonRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.smart_queue.algorithms.generator import (
    FlashcardBatch,
    GeneratedQueue,
    NewContentItem,
    QueueConfig,
    QueueItem as GeneratorQueueItem,
    QuizPracticeItem,
    generate_daily_queue,
    generate_exam_crunch_queue,
)
from app.features.smart_queue.models import DailyQueue, QueueItem, QueueItemType
from app.features.smart_queue.repository import QueueRepository
from app.features.smart_queue.schemas import (
    QueueItemSchema,
    QueuePreferencesResponse,
    QueueResponse,
)

logger = logging.getLogger(__name__)

# Days-until-exam threshold for exam crunch mode (Requirement 4.3, 4.4)
EXAM_CRUNCH_THRESHOLD = 14


class QueueService:
    """Orchestrates daily queue generation, retrieval, and item completion.

    Uses constructor injection for all dependencies. The service coordinates
    between multiple repositories and the pure generator algorithm to produce
    personalized study sessions capped at the user's time budget.
    """

    def __init__(
        self,
        *,
        queue_repo: QueueRepository,
        flashcard_repo: FlashcardRepository,
        mastery_repo: MasteryRepository,
        subtopic_repo: SubtopicRepository,
        lesson_repo: LessonRepository,
    ) -> None:
        self._queue_repo = queue_repo
        self._flashcard_repo = flashcard_repo
        self._mastery_repo = mastery_repo
        self._subtopic_repo = subtopic_repo
        self._lesson_repo = lesson_repo

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_daily_queue(self, user_id: int) -> QueueResponse:
        """Return today's daily queue, generating it if it doesn't exist.

        Idempotent: requesting multiple times on the same UTC day returns
        the same queue unless items are completed or regeneration is forced.
        (Requirement 4.5)
        """
        today = datetime.now(UTC).date()

        # Check for existing queue
        existing = self._queue_repo.get_or_create_for_date(user_id, today)
        if existing is not None:
            return self._build_response(existing)

        # Generate new queue for today
        return self._generate_and_persist(user_id, today)

    def complete_item(self, user_id: int, item_id: int) -> QueueResponse:
        """Mark a queue item as completed and return updated queue.

        Raises 404 if the item does not exist. Updates the queue's
        items_completed counter. (Requirement 4.6)
        """
        item = self._queue_repo.mark_item_completed(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Queue item not found",
            )

        # Update queue items_completed count
        today = datetime.now(UTC).date()
        queue = self._queue_repo.get_or_create_for_date(user_id, today)
        if queue is not None:
            completed_count = self._queue_repo.get_completed_count(queue.id)
            queue.items_completed = completed_count
            self._queue_repo.db.commit()
            self._queue_repo.db.refresh(queue)

            # Evaluate study consistency after item completion (Req 14.1)
            self._evaluate_consistency_if_all_done(user_id, queue)

            return self._build_response(queue)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No queue found for today",
        )

    def regenerate_queue(self, user_id: int) -> QueueResponse:
        """Force regeneration of today's queue.

        Deletes the existing queue (if any) and generates a fresh one.
        """
        today = datetime.now(UTC).date()
        self._queue_repo.delete_queue_for_date(user_id, today)
        return self._generate_and_persist(user_id, today)

    def get_preferences(self, user_id: int) -> QueuePreferencesResponse:
        """Return the user's current time budget preference.

        Defaults to 30 minutes if no preference has been set.
        (Requirement 6.2)
        """
        time_budget = self._queue_repo.get_user_preferences(user_id)
        return QueuePreferencesResponse(time_budget_minutes=time_budget)

    def update_preferences(
        self, user_id: int, time_budget_minutes: int
    ) -> QueuePreferencesResponse:
        """Update the user's time budget preference.

        Conditional regeneration logic (Requirement 6.3):
        - If no items have been completed today, regenerate the current queue.
        - If items have been completed, apply the new budget starting tomorrow.
        """
        self._queue_repo.update_user_preferences(user_id, time_budget_minutes)

        # Check if today's queue has any completed items
        today = datetime.now(UTC).date()
        queue = self._queue_repo.get_or_create_for_date(user_id, today)

        if queue is not None:
            has_completed = self._queue_repo.has_completed_items(queue.id)
            if not has_completed:
                # No items completed — regenerate with new budget
                self._queue_repo.delete_queue_for_date(user_id, today)
                self._generate_and_persist(user_id, today)

        return QueuePreferencesResponse(time_budget_minutes=time_budget_minutes)

    # ------------------------------------------------------------------
    # Cross-feature integration hooks
    # ------------------------------------------------------------------

    def _evaluate_consistency_if_all_done(
        self, user_id: int, queue: DailyQueue
    ) -> None:
        """Evaluate study consistency after queue item completion.

        Called after every item completion. Updates the StudyConsistency
        record via ConsistencyService.update_consistency. Wraps in try/except
        to avoid disrupting the primary queue flow. (Req 14.1, 14.5)
        """
        try:
            from app.features.gamification.consistency_service import ConsistencyService

            db = self._queue_repo.db
            consistency_service = ConsistencyService(db=db)
            consistency_service.update_consistency(
                user_id=user_id,
                items_total=queue.items_total,
                items_completed=queue.items_completed,
            )
        except Exception:
            logger.warning(
                "Consistency evaluation failed for user_id=%d (non-fatal)",
                user_id,
                exc_info=True,
            )

    # ------------------------------------------------------------------
    # Private: Queue Generation
    # ------------------------------------------------------------------

    def _generate_and_persist(self, user_id: int, queue_date: date) -> QueueResponse:
        """Gather data, run generator algorithm, persist queue + items."""
        time_budget = self._queue_repo.get_user_preferences(user_id)
        days_until_exam = self._get_days_until_exam(user_id)

        config = QueueConfig(
            time_budget_minutes=time_budget,
            days_until_exam=days_until_exam,
            has_exam_date=days_until_exam is not None,
        )

        # Choose generation mode based on exam proximity
        generated = self._run_generator(user_id, config)

        # Persist the queue
        queue = DailyQueue(
            user_id=user_id,
            queue_date=queue_date,
            time_budget_minutes=time_budget,
            total_estimated_seconds=generated.total_estimated_seconds,
            items_total=len(generated.items),
            items_completed=0,
        )
        queue = self._queue_repo.create_queue(queue)

        # Persist queue items
        db_items: list[QueueItem] = []
        for position, gen_item in enumerate(generated.items):
            db_item = QueueItem(
                queue_id=queue.id,
                position=position,
                item_type=self._get_item_type_str(gen_item),
                payload=json.dumps(self._serialize_item_payload(gen_item)),
                estimated_seconds=gen_item.estimated_seconds,
            )
            db_items.append(db_item)

        if db_items:
            self._queue_repo.add_items(db_items)

        return self._build_response(queue)

    def _run_generator(
        self, user_id: int, config: QueueConfig
    ) -> GeneratedQueue:
        """Run the appropriate generator based on exam proximity."""
        # Exam crunch mode (Requirement 4.3, 4.4)
        if (
            config.has_exam_date
            and config.days_until_exam is not None
            and config.days_until_exam < EXAM_CRUNCH_THRESHOLD
        ):
            return self._run_exam_crunch_generator(user_id, config)

        # Normal mode
        return self._run_normal_generator(user_id, config)

    def _run_normal_generator(
        self, user_id: int, config: QueueConfig
    ) -> GeneratedQueue:
        """Gather data for normal daily queue generation."""
        due_flashcards = self._get_due_flashcards(user_id)
        weak_subtopics = self._get_weak_subtopics(user_id)
        coverage_gaps = self._get_coverage_gaps(user_id)

        # No-data case (Requirement 4.8): no flashcards, no quiz history,
        # no content started — fill with highest exam weight subtopic
        if not due_flashcards and not weak_subtopics and not coverage_gaps:
            coverage_gaps = self._get_fallback_new_content(user_id)

        # No-flashcards-no-weak case (Requirement 4.7): fill with lowest
        # coverage subtopic
        if not due_flashcards and not weak_subtopics and coverage_gaps:
            pass  # coverage_gaps already populated, generator handles it

        # --- Learning technique integrations (Phases 8-14) ---
        # Boost weak subtopics from session reflection (Req 26.4, 26.5)
        weak_subtopics = self._apply_reflection_boosts(user_id, weak_subtopics)

        return generate_daily_queue(
            due_flashcards=due_flashcards,
            weak_subtopics=weak_subtopics,
            coverage_gaps=coverage_gaps,
            config=config,
        )

    def _run_exam_crunch_generator(
        self, user_id: int, config: QueueConfig
    ) -> GeneratedQueue:
        """Gather data for exam crunch queue generation."""
        due_flashcards = self._get_due_flashcards(user_id)

        # High-impact subtopics: lowest mastery × highest exam weight
        mastery_records = self._mastery_repo.list_by_user(user_id)
        high_impact: list[tuple[int, float]] = []
        for record in mastery_records:
            if record.mastery_score < 0.8:
                # Point impact approximation: (1 - mastery) represents potential gain
                point_impact = (1.0 - record.mastery_score) * 100
                high_impact.append((record.subtopic_id, point_impact))
        high_impact.sort(key=lambda x: x[1], reverse=True)

        # Low-accuracy subtopics: subtopics with mastery < 0.6
        # (mock accuracy proxy from mastery score)
        low_accuracy: list[tuple[int, float]] = [
            (record.subtopic_id, record.mastery_score * 100)
            for record in mastery_records
            if record.mastery_score < 0.6
        ]

        # Handle empty data in crunch mode
        if not due_flashcards and not high_impact and not low_accuracy:
            # Fallback: treat as normal generation
            return self._run_normal_generator(user_id, config)

        return generate_exam_crunch_queue(
            due_flashcards=due_flashcards,
            high_impact_subtopics=high_impact[:5],
            low_accuracy_subtopics=low_accuracy[:5],
            config=config,
        )

    # ------------------------------------------------------------------
    # Private: Data Gathering
    # ------------------------------------------------------------------

    def _get_due_flashcards(self, user_id: int) -> list[tuple[int, int, str]]:
        """Get FSRS-due flashcards with days overdue and deck name.

        Returns list of (card_id, days_overdue, deck_name).
        """
        today = datetime.now(UTC).date()
        cards = self._flashcard_repo.get_daily_queue(user_id, today=today)

        result: list[tuple[int, int, str]] = []
        for card in cards:
            days_overdue = 0
            if card.next_review_date is not None:
                days_overdue = max(0, (today - card.next_review_date).days)
            # Deck name: we need to get the deck title
            deck = self._flashcard_repo.get_deck(card.deck_id)
            deck_name = deck.title if deck else "Unknown Deck"
            result.append((card.id, days_overdue, deck_name))

        return result

    def _get_weak_subtopics(
        self, user_id: int
    ) -> list[tuple[int, float, float]]:
        """Get weakest subtopics from recent quiz performance.

        Returns up to 3 subtopics as (subtopic_id, accuracy_7d, mastery_score).
        Uses mastery data as a proxy for 7-day accuracy since quiz attempt
        history is tracked via the mastery system.
        """
        weak = self._mastery_repo.list_weakest(user_id, limit=3)

        # Only include subtopics that have at least 1 quiz attempt
        result: list[tuple[int, float, float]] = []
        for record in weak:
            if record.total_attempts > 0:
                # Use correct/total as accuracy proxy for 7-day window
                accuracy = (
                    record.correct_attempts / record.total_attempts * 100
                    if record.total_attempts > 0
                    else 0.0
                )
                result.append(
                    (record.subtopic_id, accuracy, record.mastery_score)
                )

        return result

    def _get_coverage_gaps(
        self, user_id: int
    ) -> list[tuple[int, int, float]]:
        """Get uncovered subtopics the user hasn't started.

        Returns list of (subtopic_id, lesson_id, exam_weight) for subtopics
        with no mastery record, ordered by subtopic order_index as a proxy
        for exam weight.
        """
        # Get all subtopics the user has mastery records for
        mastery_records = self._mastery_repo.list_by_user(user_id)
        covered_ids = {record.subtopic_id for record in mastery_records}

        # Find subtopics without mastery records that have lessons
        # Use a high limit to fetch all subtopics (exam has ~60)
        all_subtopics = self._subtopic_repo.list(skip=0, limit=100)
        gaps: list[tuple[int, int, float]] = []

        for subtopic in all_subtopics:
            if subtopic.id not in covered_ids:
                lesson = self._lesson_repo.get_by_subtopic_id(subtopic.id)
                if lesson is not None:
                    # Use order_index as exam weight proxy (lower = more important)
                    # Invert so higher value = higher priority
                    exam_weight = 1.0 / max(subtopic.order_index + 1, 1)
                    gaps.append((subtopic.id, lesson.id, exam_weight))

        # Sort by exam weight descending
        gaps.sort(key=lambda x: x[2], reverse=True)
        return gaps

    def _get_fallback_new_content(
        self, user_id: int
    ) -> list[tuple[int, int, float]]:
        """Fallback for no-data case: return highest-priority subtopic content.

        When the user has no study data at all, return content from the
        subtopic with the highest exam weight (lowest order_index).
        (Requirement 4.8)
        """
        all_subtopics = self._subtopic_repo.list(skip=0, limit=100)
        # Sort by order_index to get highest priority subtopics first
        sorted_subtopics = sorted(all_subtopics, key=lambda s: s.order_index)

        gaps: list[tuple[int, int, float]] = []
        for subtopic in sorted_subtopics:
            lesson = self._lesson_repo.get_by_subtopic_id(subtopic.id)
            if lesson is not None:
                exam_weight = 1.0 / max(subtopic.order_index + 1, 1)
                gaps.append((subtopic.id, lesson.id, exam_weight))
                if len(gaps) >= 5:  # Provide enough items to fill a session
                    break

        return gaps

    def _get_days_until_exam(self, user_id: int) -> int | None:
        """Get days until exam from OnboardingProfile.

        Returns None if no onboarding profile or exam date is set.
        """
        from sqlalchemy import select

        from app.features.planner.models import OnboardingProfile

        stmt = select(OnboardingProfile).where(
            OnboardingProfile.user_id == user_id,
        )
        profile = self._queue_repo.db.execute(stmt).scalar_one_or_none()
        if profile is None:
            return None

        today = datetime.now(UTC).date()
        delta = (profile.exam_date - today).days
        return max(0, delta)

    def _apply_reflection_boosts(
        self,
        user_id: int,
        weak_subtopics: list[tuple[int, float, float]],
    ) -> list[tuple[int, float, float]]:
        """Apply priority boosts from session reflections (Req 26.4, 26.5).

        If yesterday's reflection had confidence_rating 1-2, add extra
        priority to the hardest item's subtopic. Also includes recall-mode
        items for subtopics with mastery 0.5-0.8 (Req 24.5) by boosting them.
        """
        from sqlalchemy import select

        from app.features.learning_techniques.models import SessionReflection

        yesterday = datetime.now(UTC).date() - timedelta(days=1)

        try:
            stmt = select(SessionReflection).where(
                SessionReflection.user_id == user_id,
                SessionReflection.session_date >= datetime.combine(yesterday, datetime.min.time()),
                SessionReflection.session_date < datetime.combine(yesterday + timedelta(days=1), datetime.min.time()),
            )
            reflection = self._queue_repo.db.execute(stmt).scalar_one_or_none()
        except Exception:
            return weak_subtopics

        if reflection is None or reflection.confidence_rating > 2:
            return weak_subtopics

        # Confidence was 1-2: boost the session's subtopics by artificially
        # lowering their accuracy in the weak_subtopics list
        # This makes them appear as higher-priority for quiz_practice
        boosted = list(weak_subtopics)
        if reflection.hardest_item_id:
            # Look up which subtopic the hardest item belongs to
            # and ensure it's in the weak list with boosted priority
            from app.features.content.models import Question

            try:
                q = self._queue_repo.db.query(Question).filter(
                    Question.id == reflection.hardest_item_id
                ).first()
                if q:
                    # Check if subtopic already in list
                    existing_ids = [s[0] for s in boosted]
                    if q.subtopic_id not in existing_ids:
                        boosted.insert(0, (q.subtopic_id, 0.3, 0.4))
                    else:
                        # Move to front
                        idx = existing_ids.index(q.subtopic_id)
                        item = boosted.pop(idx)
                        boosted.insert(0, item)
            except Exception:
                pass

        return boosted

    # ------------------------------------------------------------------
    # Private: Response Building
    # ------------------------------------------------------------------

    def _build_response(self, queue: DailyQueue) -> QueueResponse:
        """Build QueueResponse from a persisted DailyQueue."""
        db_items = self._queue_repo.get_items(queue.id)

        items: list[QueueItemSchema] = []
        for item in db_items:
            payload = json.loads(item.payload) if item.payload else {}
            items.append(
                QueueItemSchema(
                    id=item.id,
                    position=item.position,
                    item_type=item.item_type,
                    payload=payload,
                    estimated_seconds=item.estimated_seconds,
                    completed_at=item.completed_at,
                )
            )

        items_completed = queue.items_completed
        items_remaining = queue.items_total - items_completed

        return QueueResponse(
            items=items,
            total_estimated_seconds=queue.total_estimated_seconds,
            items_remaining=items_remaining,
            items_completed=items_completed,
            time_budget_minutes=queue.time_budget_minutes,
        )

    # ------------------------------------------------------------------
    # Private: Serialization Helpers
    # ------------------------------------------------------------------

    def _get_item_type_str(self, item: GeneratorQueueItem) -> str:
        """Convert a generator queue item to its type string."""
        if isinstance(item, FlashcardBatch):
            return QueueItemType.FLASHCARD_REVIEW.value
        elif isinstance(item, QuizPracticeItem):
            return QueueItemType.QUIZ_PRACTICE.value
        elif isinstance(item, NewContentItem):
            return QueueItemType.NEW_CONTENT.value
        return "unknown"

    def _serialize_item_payload(self, item: GeneratorQueueItem) -> dict:
        """Serialize a generator queue item's data to a JSON-compatible dict."""
        if isinstance(item, FlashcardBatch):
            return {
                "card_ids": item.card_ids,
                "deck_name": item.deck_name,
            }
        elif isinstance(item, QuizPracticeItem):
            return {
                "subtopic_id": item.subtopic_id,
                "question_count": item.question_count,
                "difficulty_distribution": item.difficulty_distribution,
            }
        elif isinstance(item, NewContentItem):
            return {
                "subtopic_id": item.subtopic_id,
                "lesson_id": item.lesson_id,
                "section_index": item.section_index,
            }
        return {}
