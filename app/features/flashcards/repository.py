"""Repository for the Flashcard Learning Ecosystem.

Owns all database access for decks, flashcards, reviews, sessions,
marketplace, social, exam simulations, sync, and analytics queries.

All queries filter WHERE deleted_at IS NULL by default for soft-deleted entities.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from sqlalchemy import case, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.flashcards.models import (
    Deck,
    DeckBookmark,
    DeckComment,
    DeckRating,
    DeckReport,
    ExamSimulation,
    ExamSimulationAnswer,
    Flashcard,
    Follow,
    ReviewLog,
    StudySession,
)
from app.infrastructure.repositories.base import BaseRepository


class FlashcardRepository(BaseRepository[Deck]):
    """Persistence layer for the entire flashcard feature slice."""

    model = Deck

    def __init__(self, db: Session) -> None:
        super().__init__(db=db)

    # ------------------------------------------------------------------
    # Deck CRUD
    # ------------------------------------------------------------------

    def create_deck(self, deck: Deck) -> Deck:
        """Persist a new deck."""
        self.db.add(deck)
        self.db.commit()
        self.db.refresh(deck)
        return deck

    def get_deck(self, deck_id: int) -> Deck | None:
        """Return a deck by ID, excluding soft-deleted."""
        stmt = select(Deck).where(
            Deck.id == deck_id,
            Deck.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def update_deck(self, deck: Deck, **fields: object) -> Deck:
        """Apply fields to a deck and commit."""
        for key, value in fields.items():
            setattr(deck, key, value)
        self.db.commit()
        self.db.refresh(deck)
        return deck

    def soft_delete_deck(self, deck: Deck, deleted_at: datetime) -> None:
        """Soft-delete a deck and all its cards."""
        deck.deleted_at = deleted_at
        # Cascade soft-delete to all cards in the deck
        stmt = (
            select(Flashcard)
            .where(Flashcard.deck_id == deck.id, Flashcard.deleted_at.is_(None))
        )
        cards = self.db.execute(stmt).scalars().all()
        for card in cards:
            card.deleted_at = deleted_at
        self.db.commit()

    def list_user_decks(
        self,
        owner_id: int,
        *,
        category: str | None = None,
        visibility: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Deck], int]:
        """List decks for a user with optional filters. Returns (decks, total)."""
        base = select(Deck).where(
            Deck.owner_id == owner_id,
            Deck.deleted_at.is_(None),
        )
        if category:
            base = base.where(Deck.category == category)
        if visibility:
            base = base.where(Deck.visibility == visibility)

        count_stmt = select(func.count()).select_from(base.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        results = self.db.execute(
            base.order_by(Deck.updated_at.desc()).offset(skip).limit(limit)
        ).scalars().all()
        return list(results), total

    def duplicate_deck(self, original: Deck, new_owner_id: int) -> Deck:
        """Create a full copy of a deck with attribution."""
        new_deck = Deck(
            owner_id=new_owner_id,
            title=original.title,
            description=original.description,
            category=original.category,
            visibility="private",
            tags=original.tags,
            cloned_from_deck_id=original.id,
            cloned_from_user_id=original.owner_id,
        )
        self.db.add(new_deck)
        self.db.flush()

        # Copy all non-deleted cards
        cards = self.db.execute(
            select(Flashcard).where(
                Flashcard.deck_id == original.id,
                Flashcard.deleted_at.is_(None),
            )
        ).scalars().all()

        for card in cards:
            new_card = Flashcard(
                deck_id=new_deck.id,
                front=card.front,
                back=card.back,
                card_type=card.card_type,
                hints=card.hints,
                tags=card.tags,
                explanation=card.explanation,
            )
            self.db.add(new_card)

        # Increment clone count on original
        original.clone_count += 1
        self.db.commit()
        self.db.refresh(new_deck)
        return new_deck

    def get_deck_by_owner_and_title(
        self, owner_id: int, title: str
    ) -> Deck | None:
        """Check for unique title per owner (excluding soft-deleted)."""
        stmt = select(Deck).where(
            Deck.owner_id == owner_id,
            Deck.title == title,
            Deck.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    # ------------------------------------------------------------------
    # Flashcard CRUD
    # ------------------------------------------------------------------

    def create_flashcard(self, card: Flashcard) -> Flashcard:
        """Persist a new flashcard."""
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get_flashcard(self, card_id: int) -> Flashcard | None:
        """Return a flashcard by ID, excluding soft-deleted."""
        stmt = select(Flashcard).where(
            Flashcard.id == card_id,
            Flashcard.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def update_flashcard(self, card: Flashcard, **fields: object) -> Flashcard:
        """Apply fields to a flashcard and commit."""
        for key, value in fields.items():
            setattr(card, key, value)
        self.db.commit()
        self.db.refresh(card)
        return card

    def soft_delete_flashcard(
        self, card: Flashcard, deleted_at: datetime
    ) -> None:
        """Soft-delete a single flashcard."""
        card.deleted_at = deleted_at
        self.db.commit()

    def list_deck_flashcards(
        self, deck_id: int, *, skip: int = 0, limit: int = 50
    ) -> list[Flashcard]:
        """List non-deleted flashcards in a deck."""
        stmt = (
            select(Flashcard)
            .where(Flashcard.deck_id == deck_id, Flashcard.deleted_at.is_(None))
            .order_by(Flashcard.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_deck_flashcards(self, deck_id: int) -> int:
        """Count non-deleted flashcards in a deck."""
        stmt = select(func.count()).where(
            Flashcard.deck_id == deck_id,
            Flashcard.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one()

    # ------------------------------------------------------------------
    # Review Log
    # ------------------------------------------------------------------

    def record_review(self, review: ReviewLog) -> ReviewLog:
        """Insert a review log entry."""
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_review_history(
        self,
        user_id: int,
        card_id: int | None = None,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> list[ReviewLog]:
        """Get review history for a user, optionally filtered by card."""
        stmt = select(ReviewLog).where(ReviewLog.user_id == user_id)
        if card_id is not None:
            stmt = stmt.where(ReviewLog.card_id == card_id)
        stmt = stmt.order_by(ReviewLog.reviewed_at.desc()).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def get_review_by_client_event_id(
        self, client_event_id: str
    ) -> ReviewLog | None:
        """Look up a review by client_event_id for deduplication."""
        stmt = select(ReviewLog).where(
            ReviewLog.client_event_id == client_event_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    # ------------------------------------------------------------------
    # Review Queue
    # ------------------------------------------------------------------

    def get_daily_queue(
        self,
        user_id: int,
        *,
        deck_ids: list[int] | None = None,
        today: date | None = None,
        max_cards: int = 50,
    ) -> list[Flashcard]:
        """Get cards due for review, ordered by priority.

        Priority: overdue first (oldest next_review_date), then new cards.
        """
        if today is None:
            today = date.today()

        # Cards from user's decks that are due
        deck_filter = select(Deck.id).where(
            Deck.owner_id == user_id,
            Deck.deleted_at.is_(None),
        )
        if deck_ids:
            deck_filter = deck_filter.where(Deck.id.in_(deck_ids))

        stmt = (
            select(Flashcard)
            .where(
                Flashcard.deck_id.in_(deck_filter),
                Flashcard.deleted_at.is_(None),
                Flashcard.is_graduated.is_(False),
                or_(
                    Flashcard.next_review_date.is_(None),
                    Flashcard.next_review_date <= today,
                ),
            )
            .order_by(
                # Overdue cards first (NULL next_review_date = new cards last)
                case(
                    (Flashcard.next_review_date.is_(None), 1),
                    else_=0,
                ),
                Flashcard.next_review_date.asc(),
            )
            .limit(max_cards)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_queue_summary_counts(
        self, user_id: int, *, today: date | None = None
    ) -> dict[str, int]:
        """Get queue summary: total_due, overdue_count, new_today_count."""
        if today is None:
            today = date.today()

        deck_filter = select(Deck.id).where(
            Deck.owner_id == user_id,
            Deck.deleted_at.is_(None),
        )

        base = select(Flashcard).where(
            Flashcard.deck_id.in_(deck_filter),
            Flashcard.deleted_at.is_(None),
            Flashcard.is_graduated.is_(False),
        )

        # Total due (next_review_date <= today OR NULL)
        due_stmt = select(func.count()).select_from(
            base.where(
                or_(
                    Flashcard.next_review_date.is_(None),
                    Flashcard.next_review_date <= today,
                )
            ).subquery()
        )
        total_due = self.db.execute(due_stmt).scalar_one()

        # Overdue (next_review_date < today, not NULL)
        overdue_stmt = select(func.count()).select_from(
            base.where(Flashcard.next_review_date < today).subquery()
        )
        overdue_count = self.db.execute(overdue_stmt).scalar_one()

        # New today (next_review_date is NULL = never reviewed)
        new_stmt = select(func.count()).select_from(
            base.where(Flashcard.next_review_date.is_(None)).subquery()
        )
        new_today_count = self.db.execute(new_stmt).scalar_one()

        return {
            "total_due": total_due,
            "overdue_count": overdue_count,
            "new_today_count": new_today_count,
        }

    # ------------------------------------------------------------------
    # Study Sessions
    # ------------------------------------------------------------------

    def create_session(self, session: StudySession) -> StudySession:
        """Persist a new study session."""
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: int) -> StudySession | None:
        """Get a study session by ID."""
        return self.db.get(StudySession, session_id)

    def update_session(
        self, session: StudySession, **fields: object
    ) -> StudySession:
        """Update session fields and commit."""
        for key, value in fields.items():
            setattr(session, key, value)
        self.db.commit()
        self.db.refresh(session)
        return session

    # ------------------------------------------------------------------
    # Marketplace
    # ------------------------------------------------------------------

    def search_decks(
        self,
        *,
        query: str | None = None,
        category: str | None = None,
        sort_by: str = "newest",
        min_rating: int | None = None,
        min_cards: int | None = None,
        max_cards: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Deck], int]:
        """Search public decks for the marketplace."""
        base = select(Deck).where(
            Deck.visibility == "public",
            Deck.deleted_at.is_(None),
        )

        if query:
            pattern = f"%{query}%"
            base = base.where(
                or_(
                    Deck.title.ilike(pattern),
                    Deck.description.ilike(pattern),
                    Deck.tags.ilike(pattern),
                )
            )
        if category:
            base = base.where(Deck.category == category)
        if min_rating is not None:
            base = base.where(Deck.average_rating >= min_rating)

        count_stmt = select(func.count()).select_from(base.subquery())
        total = self.db.execute(count_stmt).scalar_one()

        # Sorting
        order = Deck.created_at.desc()  # default: newest
        if sort_by == "highest_rated":
            order = Deck.average_rating.desc().nulls_last()
        elif sort_by == "most_cloned":
            order = Deck.clone_count.desc()
        elif sort_by == "most_bookmarked":
            order = Deck.bookmark_count.desc()

        results = self.db.execute(
            base.order_by(order).offset(skip).limit(limit)
        ).scalars().all()
        return list(results), total

    def upsert_rating(
        self, deck_id: int, user_id: int, rating: int
    ) -> DeckRating:
        """Create or update a rating. Returns the rating row."""
        stmt = select(DeckRating).where(
            DeckRating.deck_id == deck_id,
            DeckRating.user_id == user_id,
        )
        existing = self.db.execute(stmt).scalar_one_or_none()
        if existing:
            existing.rating = rating
            self.db.commit()
            self.db.refresh(existing)
            return existing

        new_rating = DeckRating(
            deck_id=deck_id, user_id=user_id, rating=rating
        )
        self.db.add(new_rating)
        self.db.commit()
        self.db.refresh(new_rating)
        return new_rating

    def compute_average_rating(self, deck_id: int) -> tuple[float | None, int]:
        """Compute average rating and count for a deck."""
        stmt = select(
            func.avg(DeckRating.rating),
            func.count(DeckRating.id),
        ).where(DeckRating.deck_id == deck_id)
        row = self.db.execute(stmt).one()
        avg_val = float(row[0]) if row[0] is not None else None
        count_val = row[1]
        return avg_val, count_val

    def get_deck_ratings(
        self, deck_id: int, *, skip: int = 0, limit: int = 20
    ) -> list[DeckRating]:
        """List ratings for a deck."""
        stmt = (
            select(DeckRating)
            .where(DeckRating.deck_id == deck_id)
            .order_by(DeckRating.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    # ------------------------------------------------------------------
    # Social: Bookmarks
    # ------------------------------------------------------------------

    def create_bookmark(self, deck_id: int, user_id: int) -> DeckBookmark:
        """Bookmark a deck. Increments deck bookmark_count."""
        bookmark = DeckBookmark(deck_id=deck_id, user_id=user_id)
        self.db.add(bookmark)
        deck = self.db.get(Deck, deck_id)
        if deck:
            deck.bookmark_count += 1
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark

    def delete_bookmark(self, deck_id: int, user_id: int) -> bool:
        """Remove a bookmark. Returns True if deleted, False if not found."""
        stmt = select(DeckBookmark).where(
            DeckBookmark.deck_id == deck_id,
            DeckBookmark.user_id == user_id,
        )
        bookmark = self.db.execute(stmt).scalar_one_or_none()
        if not bookmark:
            return False
        self.db.delete(bookmark)
        deck = self.db.get(Deck, deck_id)
        if deck and deck.bookmark_count > 0:
            deck.bookmark_count -= 1
        self.db.commit()
        return True

    # ------------------------------------------------------------------
    # Social: Follows
    # ------------------------------------------------------------------

    def create_follow(self, follower_id: int, followed_id: int) -> Follow:
        """Create a follow relationship."""
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        self.db.add(follow)
        self.db.commit()
        self.db.refresh(follow)
        return follow

    def delete_follow(self, follower_id: int, followed_id: int) -> bool:
        """Remove a follow. Returns True if deleted."""
        stmt = select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id,
        )
        follow = self.db.execute(stmt).scalar_one_or_none()
        if not follow:
            return False
        self.db.delete(follow)
        self.db.commit()
        return True

    def get_followers(self, user_id: int) -> list[Follow]:
        """Get all followers of a user."""
        stmt = select(Follow).where(Follow.followed_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_following(self, user_id: int) -> list[Follow]:
        """Get all users that a user follows."""
        stmt = select(Follow).where(Follow.follower_id == user_id)
        return list(self.db.execute(stmt).scalars().all())

    def get_feed_decks(
        self, user_id: int, *, skip: int = 0, limit: int = 20
    ) -> list[Deck]:
        """Get recent public decks from followed creators."""
        followed_ids = select(Follow.followed_id).where(
            Follow.follower_id == user_id
        )
        stmt = (
            select(Deck)
            .where(
                Deck.owner_id.in_(followed_ids),
                Deck.visibility == "public",
                Deck.deleted_at.is_(None),
            )
            .order_by(Deck.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    # ------------------------------------------------------------------
    # Social: Comments
    # ------------------------------------------------------------------

    def create_comment(self, comment: DeckComment) -> DeckComment:
        """Persist a new comment."""
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def soft_delete_comment(
        self, comment: DeckComment, deleted_at: datetime
    ) -> None:
        """Soft-delete a comment."""
        comment.deleted_at = deleted_at
        self.db.commit()

    def get_comment(self, comment_id: int) -> DeckComment | None:
        """Get a comment by ID (including soft-deleted for ownership check)."""
        return self.db.get(DeckComment, comment_id)

    def list_deck_comments(
        self, deck_id: int, *, skip: int = 0, limit: int = 50
    ) -> list[DeckComment]:
        """List non-deleted comments for a deck, ordered by creation."""
        stmt = (
            select(DeckComment)
            .where(
                DeckComment.deck_id == deck_id,
                DeckComment.deleted_at.is_(None),
            )
            .order_by(DeckComment.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    # ------------------------------------------------------------------
    # Exam Simulation
    # ------------------------------------------------------------------

    def create_simulation(self, sim: ExamSimulation) -> ExamSimulation:
        """Persist a new exam simulation."""
        self.db.add(sim)
        self.db.commit()
        self.db.refresh(sim)
        return sim

    def get_simulation(self, sim_id: int) -> ExamSimulation | None:
        """Get an exam simulation by ID."""
        return self.db.get(ExamSimulation, sim_id)

    def record_exam_answer(self, answer: ExamSimulationAnswer) -> ExamSimulationAnswer:
        """Record an answer for an exam simulation."""
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def get_simulation_answers(
        self, simulation_id: int
    ) -> list[ExamSimulationAnswer]:
        """Get all answers for a simulation."""
        stmt = (
            select(ExamSimulationAnswer)
            .where(ExamSimulationAnswer.simulation_id == simulation_id)
            .order_by(ExamSimulationAnswer.id.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_historical_scores(
        self, user_id: int, *, limit: int = 10
    ) -> list[ExamSimulation]:
        """Get completed exam simulations for a user."""
        stmt = (
            select(ExamSimulation)
            .where(
                ExamSimulation.user_id == user_id,
                ExamSimulation.status == "completed",
            )
            .order_by(ExamSimulation.completed_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    # ------------------------------------------------------------------
    # Sync
    # ------------------------------------------------------------------

    def batch_upsert_reviews(
        self, reviews: list[ReviewLog]
    ) -> tuple[int, int, int]:
        """Batch insert reviews, deduplicating by client_event_id.

        Returns (accepted, duplicates, failures).
        """
        accepted = 0
        duplicates = 0
        failures = 0

        for review in reviews:
            if review.client_event_id:
                existing = self.get_review_by_client_event_id(
                    review.client_event_id
                )
                if existing:
                    duplicates += 1
                    continue
            try:
                self.db.add(review)
                self.db.flush()
                accepted += 1
            except IntegrityError:
                self.db.rollback()
                duplicates += 1

        if accepted > 0:
            self.db.commit()
        return accepted, duplicates, failures

    # ------------------------------------------------------------------
    # Reports
    # ------------------------------------------------------------------

    def create_report(self, report: DeckReport) -> DeckReport:
        """Create a deck report."""
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def count_reports(self, deck_id: int) -> int:
        """Count reports for a deck."""
        stmt = select(func.count()).where(DeckReport.deck_id == deck_id)
        return self.db.execute(stmt).scalar_one()

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def get_retention_by_tag(
        self, user_id: int
    ) -> list[tuple[str, float, int]]:
        """Get average retention per tag for a user's cards.

        Returns list of (tag, avg_retention, card_count).
        Tags are stored as JSON arrays in the tags column.
        """
        deck_filter = select(Deck.id).where(
            Deck.owner_id == user_id,
            Deck.deleted_at.is_(None),
        )
        stmt = (
            select(
                Flashcard.tags,
                func.avg(Flashcard.retention_score),
                func.count(Flashcard.id),
            )
            .where(
                Flashcard.deck_id.in_(deck_filter),
                Flashcard.deleted_at.is_(None),
                Flashcard.tags.isnot(None),
            )
            .group_by(Flashcard.tags)
        )
        rows = self.db.execute(stmt).all()
        results: list[tuple[str, float, int]] = []
        for tags_json, avg_ret, count in rows:
            if tags_json:
                results.append((tags_json, float(avg_ret), count))
        return results

    def get_review_heatmap(
        self,
        user_id: int,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[tuple[date, int, float]]:
        """Get daily review counts and avg retention for heatmap.

        Returns list of (date, review_count, avg_retention_at_time).
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=90)

        stmt = (
            select(
                func.date(ReviewLog.reviewed_at),
                func.count(ReviewLog.id),
            )
            .where(
                ReviewLog.user_id == user_id,
                func.date(ReviewLog.reviewed_at) >= start_date,
                func.date(ReviewLog.reviewed_at) <= end_date,
            )
            .group_by(func.date(ReviewLog.reviewed_at))
            .order_by(func.date(ReviewLog.reviewed_at).asc())
        )
        rows = self.db.execute(stmt).all()
        return [(row[0], row[1], 0.0) for row in rows]

    def get_admin_analytics(self) -> dict[str, object]:
        """Get admin-level analytics: top failed cards, engagement, etc."""
        # Top 20 most-failed cards
        top_failed_stmt = (
            select(
                ReviewLog.card_id,
                func.count(ReviewLog.id).label("fail_count"),
            )
            .where(ReviewLog.response_type == "forgot")
            .group_by(ReviewLog.card_id)
            .order_by(func.count(ReviewLog.id).desc())
            .limit(20)
        )
        top_failed = self.db.execute(top_failed_stmt).all()

        # Daily active reviewers (last 7 days)
        week_ago = date.today() - timedelta(days=7)
        active_stmt = select(
            func.count(func.distinct(ReviewLog.user_id))
        ).where(func.date(ReviewLog.reviewed_at) >= week_ago)
        active_reviewers = self.db.execute(active_stmt).scalar_one()

        return {
            "top_failed_cards": [
                {"card_id": r[0], "fail_count": r[1]} for r in top_failed
            ],
            "active_reviewers_7d": active_reviewers,
        }
