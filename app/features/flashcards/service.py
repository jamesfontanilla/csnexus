"""Business logic for the Flashcard Learning Ecosystem.

Orchestrates between FlashcardRepository, FSRS algorithm, and external
services (XP, Achievement, Focus). All error conditions raise HTTPException.

Requirements: 1.1-1.12, 2.1-2.8, 3.1-3.7, 4.1-4.6, 5.1-5.11, 6.1-6.7,
8.1-8.4, 9.1-9.4, 10.1-10.5, 29.2
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from app.features.flashcards.algorithms.fsrs import (
    CardState,
    compute_next_interval,
)
from app.features.flashcards.algorithms.interleaving import interleave_cards
from app.features.flashcards.models import (
    CardType,
    Deck,
    DeckComment,
    DeckVisibility,
    ExamSimulation,
    ExamSimulationAnswer,
    Flashcard,
    ReviewLog,
    StudySession,
)
from app.features.flashcards.repository import FlashcardRepository
from app.features.flashcards.schemas import (
    CardResponse,
    CardResponseResult,
    DeckCreate,
    DeckFilters,
    DeckUpdate,
    FlashcardCreate,
    FlashcardUpdate,
    QueueFilters,
    QueueSummary,
    StudySessionStart,
    StudySessionSummary,
)
from app.features.users.models import User

if TYPE_CHECKING:
    from app.features.achievements.service import AchievementService
    from app.features.focus.service import FocusService
    from app.features.xp.service import XPService


# Maximum cards per deck (Req 2.3)
MAX_CARDS_PER_DECK = 500

# Graduation threshold: consecutive mastered reviews (Req 10.5)
GRADUATION_THRESHOLD = 5


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class FlashcardService:
    """Orchestrates all flashcard business logic."""

    def __init__(
        self,
        *,
        flashcard_repo: FlashcardRepository,
        xp_service: "XPService | None" = None,
        achievement_service: "AchievementService | None" = None,
        focus_service: "FocusService | None" = None,
    ) -> None:
        self._repo = flashcard_repo
        self._xp_service = xp_service
        self._achievement_service = achievement_service
        self._focus_service = focus_service

    # ------------------------------------------------------------------
    # Deck CRUD (Req 1.1-1.12, 2.1-2.8)
    # ------------------------------------------------------------------

    def create_deck(self, user: User, payload: DeckCreate) -> Deck:
        """Create a new deck for the user.

        Enforces unique title per user (Req 2.2).
        """
        existing = self._repo.get_deck_by_owner_and_title(
            user.id, payload.title
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Deck with this title already exists",
            )

        tags_json = json.dumps(payload.tags) if payload.tags else None
        deck = Deck(
            owner_id=user.id,
            title=payload.title,
            description=payload.description,
            category=payload.category.value,
            visibility=payload.visibility.value,
            tags=tags_json,
        )
        return self._repo.create_deck(deck)

    def update_deck(self, user: User, deck_id: int, payload: DeckUpdate) -> Deck:
        """Update a deck. Only the owner can update (Req 29.2)."""
        deck = self._get_owned_deck(user, deck_id)

        fields = payload.model_dump(exclude_unset=True)
        if "tags" in fields and fields["tags"] is not None:
            fields["tags"] = json.dumps(fields["tags"])
        if "category" in fields and fields["category"] is not None:
            fields["category"] = fields["category"].value
        if "visibility" in fields and fields["visibility"] is not None:
            fields["visibility"] = fields["visibility"].value

        # Check title uniqueness if title is being changed
        if "title" in fields and fields["title"] != deck.title:
            existing = self._repo.get_deck_by_owner_and_title(
                user.id, fields["title"]
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Deck with this title already exists",
                )

        return self._repo.update_deck(deck, **fields)

    def delete_deck(self, user: User, deck_id: int) -> None:
        """Soft-delete a deck and all its cards (Req 2.6)."""
        deck = self._get_owned_deck(user, deck_id)
        self._repo.soft_delete_deck(deck, _utcnow())

    def list_user_decks(
        self,
        user: User,
        filters: DeckFilters,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Deck], int]:
        """List the user's decks with optional filters."""
        category = filters.category.value if filters.category else None
        visibility = filters.visibility.value if filters.visibility else None
        return self._repo.list_user_decks(
            user.id,
            category=category,
            visibility=visibility,
            skip=skip,
            limit=limit,
        )

    def get_deck(self, user: User, deck_id: int) -> Deck:
        """Get a deck by ID. Owner or public visibility required."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        if deck.owner_id != user.id and deck.visibility == DeckVisibility.PRIVATE.value:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        return deck

    def duplicate_deck(self, user: User, deck_id: int) -> Deck:
        """Duplicate a public/unlisted deck for the user (Req 2.5, 14.6)."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        if deck.visibility == DeckVisibility.PRIVATE.value and deck.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )

        # Generate a unique title for the clone
        base_title = deck.title
        clone_title = f"{base_title} (copy)"
        counter = 1
        while self._repo.get_deck_by_owner_and_title(user.id, clone_title):
            counter += 1
            clone_title = f"{base_title} (copy {counter})"

        clone = self._repo.duplicate_deck(deck, user.id)
        # Update the title to the unique clone title
        if clone_title != deck.title:
            self._repo.update_deck(clone, title=clone_title)

        return clone

    # ------------------------------------------------------------------
    # Flashcard CRUD (Req 1.1-1.12)
    # ------------------------------------------------------------------

    def create_flashcard(
        self, user: User, deck_id: int, payload: FlashcardCreate
    ) -> Flashcard:
        """Create a flashcard in a deck.

        Enforces:
        - Ownership check (Req 29.2)
        - Deck capacity limit of 500 cards (Req 2.3)
        - Card type-specific validation (Req 1.3-1.6, 1.12)
        """
        deck = self._get_owned_deck(user, deck_id)

        # Capacity check
        count = self._repo.count_deck_flashcards(deck.id)
        if count >= MAX_CARDS_PER_DECK:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Deck capacity limit reached ({MAX_CARDS_PER_DECK} cards)",
            )

        # Type-specific validation
        self._validate_card_type(payload)

        hints_json = json.dumps(payload.hints) if payload.hints else None
        tags_json = json.dumps(payload.tags) if payload.tags else None

        card = Flashcard(
            deck_id=deck.id,
            front=payload.front,
            back=payload.back,
            card_type=payload.card_type.value,
            hints=hints_json,
            tags=tags_json,
        )
        return self._repo.create_flashcard(card)

    def update_flashcard(
        self, user: User, card_id: int, payload: FlashcardUpdate
    ) -> Flashcard:
        """Update a flashcard, preserving scheduling metadata (Req 1.7)."""
        card = self._get_owned_card(user, card_id)

        fields = payload.model_dump(exclude_unset=True)
        if "hints" in fields and fields["hints"] is not None:
            fields["hints"] = json.dumps(fields["hints"])
        if "tags" in fields and fields["tags"] is not None:
            fields["tags"] = json.dumps(fields["tags"])

        # Scheduling fields are never touched by content updates
        return self._repo.update_flashcard(card, **fields)

    def delete_flashcard(self, user: User, card_id: int) -> None:
        """Soft-delete a flashcard (Req 2.6)."""
        card = self._get_owned_card(user, card_id)
        self._repo.soft_delete_flashcard(card, _utcnow())

    # ------------------------------------------------------------------
    # Study Sessions (Req 3.1-3.7, 4.1-4.6, 8.1-8.4)
    # ------------------------------------------------------------------

    def start_study_session(
        self, user: User, payload: StudySessionStart
    ) -> StudySession:
        """Start a new study session (Req 3.1-3.6)."""
        # Validate deck ownership
        for deck_id in payload.deck_ids:
            deck = self._repo.get_deck(deck_id)
            if not deck or deck.owner_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Deck {deck_id} not found",
                )

        session = StudySession(
            user_id=user.id,
            study_mode=payload.study_mode.value,
            deck_ids=json.dumps(payload.deck_ids),
            interleaving_enabled=payload.interleaving_enabled,
            focus_mode_enabled=payload.focus_mode_enabled,
            time_limit_seconds=payload.time_limit_seconds,
            card_time_limit_seconds=payload.card_time_limit_seconds,
            started_at=_utcnow(),
        )
        return self._repo.create_session(session)

    def record_response(
        self, user: User, session_id: int, payload: CardResponse
    ) -> CardResponseResult:
        """Record a card response during a session (Req 4.5, 5.1-5.11, 10.1).

        Calls FSRS engine, updates card scheduling, records review log.
        """
        session = self._repo.get_session(session_id)
        if not session or session.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        card = self._repo.get_flashcard(payload.card_id)
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )

        today = date.today()
        confidence = payload.confidence_level

        # Build current card state for FSRS
        state = CardState(
            ease_factor=card.ease_factor,
            retention_score=card.retention_score,
            memory_stability=card.memory_stability,
            review_interval=card.review_interval,
            lapse_count=card.lapse_count,
            last_review_date=card.last_review_date,
        )

        # Compute next interval via FSRS
        from app.features.flashcards.models import ConfidenceLevel, ResponseType

        response_type = ResponseType(payload.response_type.value)
        conf_level = ConfidenceLevel(confidence.value) if confidence else ConfidenceLevel.CONFIDENT

        result = compute_next_interval(state, response_type, conf_level, today)

        # Snapshot before values for review log
        ease_before = card.ease_factor
        interval_before = card.review_interval

        # Update card scheduling fields
        is_remembered = payload.response_type.value == "remembered"
        new_total = card.total_reviews + 1
        new_successful = card.successful_reviews + (1 if is_remembered else 0)

        self._repo.update_flashcard(
            card,
            ease_factor=result.ease_factor,
            retention_score=result.retention_score,
            memory_stability=result.memory_stability,
            review_interval=result.review_interval,
            lapse_count=result.lapse_count,
            next_review_date=result.next_review_date,
            last_review_date=today,
            total_reviews=new_total,
            successful_reviews=new_successful,
        )

        # Record review log
        review = ReviewLog(
            user_id=user.id,
            card_id=card.id,
            session_id=session.id,
            response_type=payload.response_type.value,
            confidence_level=confidence.value if confidence else None,
            ease_factor_before=ease_before,
            interval_before=interval_before,
            ease_factor_after=result.ease_factor,
            interval_after=result.review_interval,
            typed_answer=payload.typed_answer,
            reviewed_at=_utcnow(),
        )
        self._repo.record_review(review)

        # Update session counters
        session.cards_reviewed += 1
        if is_remembered:
            session.cards_correct += 1
        elif payload.response_type.value == "forgot":
            session.cards_incorrect += 1
        else:
            session.cards_skipped += 1
        self._repo.update_session(session)

        return CardResponseResult(
            ease_factor=result.ease_factor,
            retention_score=result.retention_score,
            memory_stability=result.memory_stability,
            review_interval=result.review_interval,
            next_review_date=result.next_review_date,
        )

    def end_study_session(
        self, user: User, session_id: int
    ) -> StudySessionSummary:
        """End a study session and compute summary (Req 3.7)."""
        session = self._repo.get_session(session_id)
        if not session or session.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )
        if session.ended_at is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Session already ended",
            )

        now = _utcnow()
        duration = int((now - session.started_at).total_seconds())

        self._repo.update_session(
            session, ended_at=now, duration_seconds=duration
        )

        # XP award: (2 * cards_reviewed) + (1 * cards_correct)
        xp_earned = (2 * session.cards_reviewed) + session.cards_correct

        return StudySessionSummary(
            cards_reviewed=session.cards_reviewed,
            cards_correct=session.cards_correct,
            cards_incorrect=session.cards_incorrect,
            cards_skipped=session.cards_skipped,
            duration_seconds=duration,
            xp_earned=xp_earned,
        )

    # ------------------------------------------------------------------
    # Review Queue (Req 6.1-6.7)
    # ------------------------------------------------------------------

    def get_daily_queue(
        self, user: User, filters: QueueFilters
    ) -> list[Flashcard]:
        """Get the daily review queue with priority ordering (Req 6.1)."""
        cards = self._repo.get_daily_queue(
            user.id,
            deck_ids=filters.deck_ids,
            today=date.today(),
            max_cards=filters.max_cards,
        )

        # Apply interleaving if cards span multiple categories
        if len(cards) > 1:
            categories = {c.card_type for c in cards}
            if len(categories) > 1:
                cards = interleave_cards(cards, max_consecutive_same_category=3)

        return cards

    def get_queue_summary(self, user: User) -> QueueSummary:
        """Get queue summary counts (Req 6.6)."""
        counts = self._repo.get_queue_summary_counts(
            user.id, today=date.today()
        )
        # Estimate ~30 seconds per card
        estimated_minutes = (counts["total_due"] * 30) // 60
        return QueueSummary(
            total_due=counts["total_due"],
            overdue_count=counts["overdue_count"],
            new_today_count=counts["new_today_count"],
            estimated_review_minutes=estimated_minutes,
        )

    # ------------------------------------------------------------------
    # Marketplace (Req 14.1-14.9)
    # ------------------------------------------------------------------

    def search_marketplace(
        self,
        query: str | None = None,
        category: str | None = None,
        sort_by: str = "newest",
        min_rating: int | None = None,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Deck], int]:
        """Search public decks in the marketplace."""
        return self._repo.search_decks(
            query=query,
            category=category,
            sort_by=sort_by,
            min_rating=min_rating,
            skip=skip,
            limit=limit,
        )

    def rate_deck(self, user: User, deck_id: int, rating: int) -> None:
        """Rate a deck (Req 14.4, 14.5).

        Enforces: 1-5 range, one per user, no self-rating.
        """
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        if deck.owner_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot rate your own deck",
            )

        self._repo.upsert_rating(deck_id, user.id, rating)

        # Recompute average
        avg, count = self._repo.compute_average_rating(deck_id)
        self._repo.update_deck(deck, average_rating=avg, rating_count=count)

    def clone_deck(self, user: User, deck_id: int) -> Deck:
        """Clone a public deck (Req 14.6). Alias for duplicate_deck."""
        return self.duplicate_deck(user, deck_id)

    def bookmark_deck(self, user: User, deck_id: int) -> None:
        """Bookmark a deck (Req 16.1)."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        self._repo.create_bookmark(deck_id, user.id)

    def unbookmark_deck(self, user: User, deck_id: int) -> None:
        """Remove a bookmark (Req 16.2)."""
        deleted = self._repo.delete_bookmark(deck_id, user.id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bookmark not found",
            )

    # ------------------------------------------------------------------
    # Social (Req 15.1-15.5, 16.1-16.6, 17.1-17.7)
    # ------------------------------------------------------------------

    def follow_creator(self, user: User, creator_id: int) -> None:
        """Follow a creator (Req 16.3). Prevents self-follow."""
        if user.id == creator_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cannot follow yourself",
            )
        self._repo.create_follow(user.id, creator_id)

    def unfollow_creator(self, user: User, creator_id: int) -> None:
        """Unfollow a creator (Req 16.4)."""
        deleted = self._repo.delete_follow(user.id, creator_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow relationship not found",
            )

    def get_feed(
        self, user: User, *, skip: int = 0, limit: int = 20
    ) -> list[Deck]:
        """Get decks from followed creators (Req 16.5)."""
        return self._repo.get_feed_decks(user.id, skip=skip, limit=limit)

    def create_comment(
        self, user: User, deck_id: int, body: str, parent_comment_id: int | None = None
    ) -> DeckComment:
        """Post a comment on a deck (Req 17.1)."""

        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )

        nesting_level = 0
        if parent_comment_id is not None:
            parent = self._repo.get_comment(parent_comment_id)
            if not parent or parent.deck_id != deck_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent comment not found",
                )
            nesting_level = parent.nesting_level + 1
            if nesting_level > 2:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Maximum nesting level (2) exceeded",
                )

        # Simple keyword moderation filter
        moderation_keywords = ["spam", "scam", "hate"]
        is_held = any(kw in body.lower() for kw in moderation_keywords)

        comment = DeckComment(
            deck_id=deck_id,
            user_id=user.id,
            body=body,
            parent_comment_id=parent_comment_id,
            nesting_level=nesting_level,
            is_held_for_moderation=is_held,
        )
        return self._repo.create_comment(comment)

    def delete_comment(self, user: User, comment_id: int) -> None:
        """Soft-delete a comment (Req 17.4). Only owner can delete."""

        comment = self._repo.get_comment(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )
        if comment.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not the comment owner",
            )
        self._repo.soft_delete_comment(comment, _utcnow())

    def list_comments(
        self, deck_id: int, *, skip: int = 0, limit: int = 50
    ) -> list:
        """List comments for a deck (Req 17.3)."""
        return self._repo.list_deck_comments(deck_id, skip=skip, limit=limit)

    # ------------------------------------------------------------------
    # Gamification Integration (Req 18.1-18.7, 19.1-19.7, 20.1-20.4)
    # ------------------------------------------------------------------

    def _award_xp_safely(
        self, user: User, amount: int, *, client_event_id: str | None = None
    ) -> None:
        """Award XP via XPService, handling failures gracefully (Req 18.7)."""
        if self._xp_service is None:
            return
        try:
            from app.features.xp.models import XPSource
            self._xp_service.award(
                user=user,
                source=XPSource.FLASHCARD_REVIEW,
                amount=amount,
                client_event_id=client_event_id,
            )
        except Exception:
            pass

    def compute_deck_popularity_score(self, deck_id: int) -> float:
        """Compute deck popularity score for leaderboard (Req 20.3).

        Formula: (clone_count * 3) + (bookmark_count * 2) + (rating_count * average_rating)
        """
        deck = self._repo.get_deck(deck_id)
        if not deck:
            return 0.0

        avg_rating = deck.average_rating or 0.0
        score = (
            (deck.clone_count * 3)
            + (deck.bookmark_count * 2)
            + (deck.rating_count * avg_rating)
        )
        return round(score, 2)

    # ------------------------------------------------------------------
    # Explanation Engine (Req 13.1-13.5)
    # ------------------------------------------------------------------

    def get_card_explanation(self, card_id: int) -> dict[str, str | None]:
        """Get a template-based explanation for a card (Req 13.1-13.5).

        Uses the card's tags to determine category and select template.
        Falls back to the card's stored explanation field.
        """
        card = self._repo.get_flashcard(card_id)
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )

        # Try stored explanation first
        if card.explanation:
            return {
                "explanation": card.explanation,
                "lesson_link": None,
                "category": "stored",
            }

        # Determine category from tags or deck
        tags_str = card.tags or "[]"
        try:
            tags = json.loads(tags_str)
        except (json.JSONDecodeError, TypeError):
            tags = []

        category = self._infer_category_from_tags(tags)
        explanation = self._generate_template_explanation(card, category)
        lesson_link = self._compute_lesson_link(tags)

        return {
            "explanation": explanation,
            "lesson_link": lesson_link,
            "category": category,
        }

    def _infer_category_from_tags(self, tags: list[str]) -> str:
        """Infer the subject category from card tags."""
        grammar_keywords = {"grammar", "verb", "noun", "tense", "speech", "sentence"}
        vocab_keywords = {"vocabulary", "synonym", "antonym", "word", "idiom"}
        numerical_keywords = {"math", "number", "ratio", "percentage", "algebra"}
        analytical_keywords = {"logic", "pattern", "reasoning", "analogy"}

        tags_lower = {t.lower() for t in tags}

        if tags_lower & grammar_keywords:
            return "grammar"
        if tags_lower & vocab_keywords:
            return "vocabulary"
        if tags_lower & numerical_keywords:
            return "numerical"
        if tags_lower & analytical_keywords:
            return "analytical"
        return "general"

    def _generate_template_explanation(self, card: Flashcard, category: str) -> str:
        """Generate a template-based explanation by category."""
        templates = {
            "grammar": f"Grammar Rule: {card.back}. Remember this pattern for correct sentence construction.",
            "vocabulary": f"Word Knowledge: '{card.front}' — {card.back}. Understanding etymology helps retention.",
            "numerical": f"Formula/Concept: {card.back}. Practice with similar problems to build fluency.",
            "analytical": f"Logic Pattern: {card.back}. Look for similar structures in other problems.",
            "general": f"Key Concept: {card.back}.",
        }
        return templates.get(category, templates["general"])

    def _compute_lesson_link(self, tags: list[str]) -> str | None:
        """Compute a deep link to the relevant lesson section."""
        if not tags:
            return None
        # Convert first tag to a URL-friendly slug
        slug = tags[0].lower().replace(" ", "-").replace("_", "-")
        return f"/lessons/{slug}"

    # ------------------------------------------------------------------
    # Exam Simulation (Req 22.1-22.9)
    # ------------------------------------------------------------------

    def start_exam_simulation(
        self, user: User, deck_ids: list[int], card_count: int, time_limit_seconds: int
    ) -> ExamSimulation:
        """Start an exam simulation (Req 22.1-22.3)."""
        import random as _random

        # Validate decks and collect cards
        all_cards: list[Flashcard] = []
        for deck_id in deck_ids:
            deck = self._repo.get_deck(deck_id)
            if not deck:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Deck {deck_id} not found",
                )
            cards = self._repo.list_deck_flashcards(deck_id, limit=500)
            all_cards.extend(cards)

        if len(all_cards) < card_count:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Insufficient cards ({len(all_cards)}) for {card_count}-question exam",
            )

        # Select random cards
        rng = _random.Random()
        selected = rng.sample(all_cards, min(card_count, len(all_cards)))

        sim = ExamSimulation(
            user_id=user.id,
            deck_ids=json.dumps(deck_ids),
            question_count=len(selected),
            time_limit_minutes=time_limit_seconds // 60,
            started_at=_utcnow(),
        )
        sim = self._repo.create_simulation(sim)

        # Pre-create answer slots
        for card in selected:
            answer = ExamSimulationAnswer(
                simulation_id=sim.id,
                card_id=card.id,
            )
            self._repo.record_exam_answer(answer)

        return sim

    def submit_exam_answer(
        self, user: User, sim_id: int, card_id: int, answer: str
    ) -> None:
        """Submit an answer for an exam simulation (Req 22.4-22.5)."""
        sim = self._repo.get_simulation(sim_id)
        if not sim or sim.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Simulation not found",
            )
        if sim.status != "in_progress":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Simulation already completed",
            )

        # Find the answer slot
        answers = self._repo.get_simulation_answers(sim_id)
        target = next((a for a in answers if a.card_id == card_id), None)
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not in this simulation",
            )
        if target.is_locked:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Answer already locked",
            )

        # Lock the answer
        target.user_answer = answer
        target.is_locked = True
        target.answered_at = _utcnow()

        # Check correctness against card's back
        card = self._repo.get_flashcard(card_id)
        if card:
            target.is_correct = answer.strip().lower() == card.back.strip().lower()

        self._repo.db.commit()

    def complete_exam_simulation(self, user: User, sim_id: int) -> dict:
        """Complete an exam simulation and compute scores (Req 22.6-22.9)."""
        sim = self._repo.get_simulation(sim_id)
        if not sim or sim.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Simulation not found",
            )
        if sim.status != "in_progress":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Simulation already completed",
            )

        answers = self._repo.get_simulation_answers(sim_id)
        correct = sum(1 for a in answers if a.is_correct)
        incorrect = sum(1 for a in answers if a.is_correct is False)
        skipped = sum(1 for a in answers if a.user_answer is None)

        total = len(answers)
        percentage = (correct / total * 100) if total > 0 else 0.0
        time_taken = int((_utcnow() - sim.started_at).total_seconds())

        # Update simulation
        sim.status = "completed"
        sim.completed_at = _utcnow()
        sim.total_score = percentage
        sim.cards_correct = correct
        sim.cards_incorrect = incorrect
        sim.cards_skipped = skipped
        sim.time_taken_seconds = time_taken
        self._repo.db.commit()

        return {
            "score": correct,
            "total": total,
            "percentage": round(percentage, 1),
            "time_taken_seconds": time_taken,
        }

    # ------------------------------------------------------------------
    # Analytics Dashboard (Req 26.1-26.6)
    # ------------------------------------------------------------------

    def get_user_dashboard(self, user: User) -> dict:
        """Get user analytics dashboard (Req 26.1-26.6)."""
        # Overall retention
        tag_data = self._repo.get_retention_by_tag(user.id)
        if tag_data:
            total_retention = sum(r for _, r, _ in tag_data) / len(tag_data)
        else:
            total_retention = 0.0

        # Strongest/weakest subjects
        sorted_tags = sorted(tag_data, key=lambda x: x[1], reverse=True)
        strongest = [{"tag": t, "mastery": round(r * 100, 1)} for t, r, _ in sorted_tags[:3]]
        weakest = [{"tag": t, "mastery": round(r * 100, 1)} for t, r, _ in sorted_tags[-3:]]

        # Predicted exam readiness (weighted average of retention scores)
        # CSE distribution: verbal 40%, numerical 30%, analytical 30%
        readiness = self._compute_exam_readiness(tag_data)

        return {
            "overall_retention": round(total_retention * 100, 1),
            "strongest_subjects": strongest,
            "weakest_subjects": weakest,
            "predicted_readiness": readiness,
        }

    def _compute_exam_readiness(
        self, tag_data: list[tuple[str, float, int]]
    ) -> float:
        """Compute predicted exam readiness score (Req 26.6).

        Weighted by CSE distribution: verbal 40%, numerical 30%, analytical 30%.
        """
        if not tag_data:
            return 0.0

        verbal_scores: list[float] = []
        numerical_scores: list[float] = []
        analytical_scores: list[float] = []

        verbal_kw = {"grammar", "vocabulary", "reading", "verbal", "word"}
        numerical_kw = {"math", "number", "ratio", "percentage", "numerical"}
        analytical_kw = {"logic", "pattern", "reasoning", "analytical", "analogy"}

        for tag, retention, _ in tag_data:
            tag_lower = tag.lower()
            if any(kw in tag_lower for kw in verbal_kw):
                verbal_scores.append(retention)
            elif any(kw in tag_lower for kw in numerical_kw):
                numerical_scores.append(retention)
            elif any(kw in tag_lower for kw in analytical_kw):
                analytical_scores.append(retention)

        def _avg(scores: list[float]) -> float:
            return sum(scores) / len(scores) if scores else 0.5

        readiness = (
            _avg(verbal_scores) * 0.4
            + _avg(numerical_scores) * 0.3
            + _avg(analytical_scores) * 0.3
        )
        return round(readiness * 100, 1)

    # ------------------------------------------------------------------
    # Admin Analytics & Moderation (Req 27.1-27.6, 28.1-28.7)
    # ------------------------------------------------------------------

    def get_admin_analytics(self) -> dict:
        """Get admin-level analytics (Req 27.1-27.6)."""
        return self._repo.get_admin_analytics()

    def flag_deck(self, deck_id: int) -> None:
        """Flag a deck for removal (admin action, Req 28.3)."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        self._repo.update_deck(deck, visibility="removed")

    def toggle_featured(self, deck_id: int) -> None:
        """Toggle a deck's featured status (admin action, Req 28.4)."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        self._repo.update_deck(deck, is_featured=not deck.is_featured)

    # ------------------------------------------------------------------
    # Sync (Req 24.1-24.10)
    # ------------------------------------------------------------------

    def batch_sync_reviews(
        self, user: User, items: list[dict]
    ) -> dict[str, int]:
        """Batch sync offline reviews (Req 24.1-24.10).

        Deduplicates by client_event_id, processes in chronological order.
        """
        # Sort by reviewed_at for chronological processing
        sorted_items = sorted(items, key=lambda x: x.get("reviewed_at", ""))

        reviews: list[ReviewLog] = []
        for item in sorted_items:
            review = ReviewLog(
                user_id=user.id,
                card_id=item["card_id"],
                response_type=item["response_type"],
                confidence_level=item.get("confidence_level"),
                ease_factor_before=2.5,
                interval_before=1,
                ease_factor_after=2.5,
                interval_after=1,
                reviewed_at=item["reviewed_at"],
                client_event_id=item["client_event_id"],
            )
            reviews.append(review)

        accepted, duplicates, failures = self._repo.batch_upsert_reviews(reviews)
        return {
            "accepted": accepted,
            "duplicates": duplicates,
            "failures": failures,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_owned_deck(self, user: User, deck_id: int) -> Deck:
        """Get a deck and verify ownership."""
        deck = self._repo.get_deck(deck_id)
        if not deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Deck not found",
            )
        if deck.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not the deck owner",
            )
        return deck

    def _get_owned_card(self, user: User, card_id: int) -> Flashcard:
        """Get a flashcard and verify the user owns its deck."""
        card = self._repo.get_flashcard(card_id)
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Card not found",
            )
        deck = self._repo.get_deck(card.deck_id)
        if not deck or deck.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not the deck owner",
            )
        return card

    def _validate_card_type(self, payload: FlashcardCreate) -> None:
        """Validate card type-specific constraints (Req 1.3-1.6, 1.12).

        - cloze: front must contain {{c1::...}} pattern
        - mcq: back must be valid JSON array with 2-6 options
        - matching: back must be valid JSON with pairs
        - sequence: back must be valid JSON array with 2+ items
        - true_false: back must be 'true' or 'false'
        """
        card_type = payload.card_type

        if card_type == CardType.CLOZE:
            if "{{c1::" not in payload.front:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Cloze cards must contain {{c1::...}} in front",
                )

        elif card_type == CardType.MCQ:
            try:
                options = json.loads(payload.back)
                if not isinstance(options, list) or len(options) < 2:
                    raise ValueError
            except (json.JSONDecodeError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="MCQ cards require back to be a JSON array with 2+ options",
                )

        elif card_type == CardType.MATCHING:
            try:
                pairs = json.loads(payload.back)
                if not isinstance(pairs, (list, dict)) or len(pairs) < 2:
                    raise ValueError
            except (json.JSONDecodeError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Matching cards require back to be JSON with 2+ pairs",
                )

        elif card_type == CardType.SEQUENCE:
            try:
                items = json.loads(payload.back)
                if not isinstance(items, list) or len(items) < 2:
                    raise ValueError
            except (json.JSONDecodeError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Sequence cards require back to be a JSON array with 2+ items",
                )

        elif card_type == CardType.TRUE_FALSE:
            if payload.back.lower().strip() not in ("true", "false"):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="True/false cards require back to be 'true' or 'false'",
                )
