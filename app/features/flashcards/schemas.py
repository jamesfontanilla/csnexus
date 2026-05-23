"""Pydantic schemas for the Flashcard Learning Ecosystem.

Organized by domain concern:
- Deck CRUD (DeckCreate, DeckUpdate, DeckResponse, DeckFilters)
- Flashcard CRUD (FlashcardCreate, FlashcardUpdate, FlashcardResponse)
- Study Sessions (StudySessionStart, CardResponse, CardResponseResult, StudySessionSummary)
- Review Queue (QueueFilters, QueueSummary)
- Marketplace (MarketplaceSearch, DeckRatingCreate)
- Exam Simulation (ExamSimulationStart, ExamAnswer, ExamSimulationResult)
- Offline Sync (SyncBatchRequest, SyncItem, SyncBatchResponse)
- Analytics (AnalyticsFilters, RetentionAnalytics, UserDashboard)
- Social (CreatorProfileResponse, CommentCreate, CommentResponse)

Requirements: 30.2, 30.3, 30.6
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.features.flashcards.models import (
    CardType,
    ConfidenceLevel,
    DeckCategory,
    DeckVisibility,
    ResponseType,
    StudyMode,
)


# ---------------------------------------------------------------------------
# Deck schemas
# ---------------------------------------------------------------------------


class DeckCreate(BaseModel):
    """Create payload for a flashcard deck (Req 2.1)."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: DeckCategory
    visibility: DeckVisibility = DeckVisibility.PRIVATE
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: list[str]) -> list[str]:
        for tag in v:
            if len(tag) > 50:
                raise ValueError("each tag must be at most 50 characters")
            if not tag.strip():
                raise ValueError("tags must be non-empty strings")
        return v

    @field_validator("visibility")
    @classmethod
    def _no_removed_visibility(cls, v: DeckVisibility) -> DeckVisibility:
        if v == DeckVisibility.REMOVED:
            raise ValueError("cannot set visibility to 'removed' on creation")
        return v


class DeckUpdate(BaseModel):
    """Partial update payload for a deck. All fields optional."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    category: DeckCategory | None = None
    visibility: DeckVisibility | None = None
    tags: list[str] | None = None

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        if len(v) > 10:
            raise ValueError("a deck may have at most 10 tags")
        for tag in v:
            if len(tag) > 50:
                raise ValueError("each tag must be at most 50 characters")
            if not tag.strip():
                raise ValueError("tags must be non-empty strings")
        return v


class DeckResponse(BaseModel):
    """Read-side projection of a Deck, including computed fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str | None = None
    category: str
    visibility: str
    tags: str | None = None
    clone_count: int = 0
    bookmark_count: int = 0
    average_rating: float | None = None
    rating_count: int = 0
    is_featured: bool = False
    cloned_from_deck_id: int | None = None
    cloned_from_user_id: int | None = None
    created_at: datetime
    updated_at: datetime


class DeckFilters(BaseModel):
    """Query filters for listing user decks (Req 2.8)."""

    category: DeckCategory | None = None
    visibility: DeckVisibility | None = None
    tags: list[str] | None = None


# ---------------------------------------------------------------------------
# Flashcard schemas
# ---------------------------------------------------------------------------


class FlashcardCreate(BaseModel):
    """Create payload for a flashcard (Req 1.1).

    Field constraints:
    - front: 1-1000 characters
    - back: 1-2000 characters
    - hints: 0-5 items, each max 200 characters
    - tags: 0-10 items, each max 50 characters
    """

    front: str = Field(min_length=1, max_length=1000)
    back: str = Field(min_length=1, max_length=2000)
    card_type: CardType
    hints: list[str] = Field(default_factory=list, max_length=5)
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("hints")
    @classmethod
    def _validate_hints(cls, v: list[str]) -> list[str]:
        for hint in v:
            if len(hint) > 200:
                raise ValueError("each hint must be at most 200 characters")
            if not hint.strip():
                raise ValueError("hints must be non-empty strings")
        return v

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: list[str]) -> list[str]:
        for tag in v:
            if len(tag) > 50:
                raise ValueError("each tag must be at most 50 characters")
            if not tag.strip():
                raise ValueError("tags must be non-empty strings")
        return v


class FlashcardUpdate(BaseModel):
    """Partial update payload for a flashcard. card_type is NOT updatable."""

    front: str | None = Field(default=None, min_length=1, max_length=1000)
    back: str | None = Field(default=None, min_length=1, max_length=2000)
    hints: list[str] | None = None
    tags: list[str] | None = None

    @field_validator("hints")
    @classmethod
    def _validate_hints(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        if len(v) > 5:
            raise ValueError("a flashcard may have at most 5 hints")
        for hint in v:
            if len(hint) > 200:
                raise ValueError("each hint must be at most 200 characters")
            if not hint.strip():
                raise ValueError("hints must be non-empty strings")
        return v

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        if len(v) > 10:
            raise ValueError("a flashcard may have at most 10 tags")
        for tag in v:
            if len(tag) > 50:
                raise ValueError("each tag must be at most 50 characters")
            if not tag.strip():
                raise ValueError("tags must be non-empty strings")
        return v


class FlashcardResponse(BaseModel):
    """Read-side projection of a flashcard including scheduling state."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    deck_id: int
    front: str
    back: str
    card_type: str
    hints: str | None = None
    tags: str | None = None
    explanation: str | None = None
    ease_factor: float = 2.5
    retention_score: float = 0.0
    memory_stability: float = 1.0
    review_interval: int = 1
    lapse_count: int = 0
    mastery_percentage: float = 0.0
    next_review_date: date | None = None
    last_review_date: date | None = None
    total_reviews: int = 0
    successful_reviews: int = 0
    is_graduated: bool = False
    is_bookmarked: bool = False
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# Study Session schemas
# ---------------------------------------------------------------------------


class StudySessionStart(BaseModel):
    """Payload to start a study session (Req 3.1-3.6)."""

    study_mode: StudyMode
    deck_ids: list[int] = Field(min_length=1)
    interleaving_enabled: bool = False
    focus_mode_enabled: bool = False
    time_limit_seconds: int | None = Field(default=None, gt=0)
    card_time_limit_seconds: int | None = Field(default=None, gt=0)


class CardResponse(BaseModel):
    """Payload for recording a card response during a session (Req 4.5, 10.1)."""

    card_id: int
    response_type: ResponseType
    confidence_level: ConfidenceLevel | None = None
    typed_answer: str | None = None


class CardResponseResult(BaseModel):
    """Result returned after recording a card response (Req 8.4)."""

    is_correct: bool | None = None
    similarity_score: float | None = None
    correct_answer: str | None = None
    ease_factor: float
    retention_score: float
    memory_stability: float
    review_interval: int
    next_review_date: date | None = None


class StudySessionSummary(BaseModel):
    """Summary returned when a study session ends (Req 3.7)."""

    cards_reviewed: int = 0
    cards_correct: int = 0
    cards_incorrect: int = 0
    cards_skipped: int = 0
    duration_seconds: int = 0
    xp_earned: int = 0


# ---------------------------------------------------------------------------
# Review Queue schemas
# ---------------------------------------------------------------------------


class QueueFilters(BaseModel):
    """Filters for the daily review queue (Req 6.2, 6.4)."""

    deck_ids: list[int] | None = None
    max_cards: int = Field(default=50, ge=10, le=200)


class QueueSummary(BaseModel):
    """Queue summary counts (Req 6.6)."""

    total_due: int = 0
    overdue_count: int = 0
    new_today_count: int = 0
    estimated_review_minutes: int = 0


# ---------------------------------------------------------------------------
# Marketplace schemas
# ---------------------------------------------------------------------------


class MarketplaceSearch(BaseModel):
    """Search/filter parameters for marketplace browsing (Req 14.2, 14.3, 14.7)."""

    query: str | None = Field(default=None, min_length=2)
    category: DeckCategory | None = None
    sort_by: str = Field(default="newest")
    min_rating: int | None = Field(default=None, ge=1, le=5)
    min_cards: int | None = Field(default=None, ge=0)
    max_cards: int | None = Field(default=None, ge=0)

    @field_validator("sort_by")
    @classmethod
    def _validate_sort_by(cls, v: str) -> str:
        allowed = {"newest", "highest_rated", "most_cloned", "most_bookmarked"}
        if v not in allowed:
            raise ValueError(
                f"sort_by must be one of: {', '.join(sorted(allowed))}"
            )
        return v


class DeckRatingCreate(BaseModel):
    """Payload for rating a deck (Req 14.4)."""

    rating: int = Field(ge=1, le=5)


# ---------------------------------------------------------------------------
# Exam Simulation schemas
# ---------------------------------------------------------------------------


class ExamSimulationStart(BaseModel):
    """Payload to start an exam simulation (Req 3.6)."""

    deck_ids: list[int] = Field(min_length=1)
    card_count: int = Field(default=50, ge=10, le=150)
    time_limit_seconds: int = Field(ge=60)


class ExamAnswer(BaseModel):
    """Payload for submitting an exam answer."""

    card_id: int
    answer: str = Field(min_length=1)


class CategoryBreakdown(BaseModel):
    """Score breakdown for a single category in exam results."""

    category: str
    correct: int
    total: int
    percentage: float


class ExamSimulationResult(BaseModel):
    """Result returned when an exam simulation completes."""

    score: int
    total: int
    percentage: float
    category_breakdown: list[CategoryBreakdown]
    percentile_estimate: int | None = None
    time_taken_seconds: int = 0


# ---------------------------------------------------------------------------
# Offline Sync schemas
# ---------------------------------------------------------------------------


class SyncItem(BaseModel):
    """A single offline review to sync (Req 24.8)."""

    client_event_id: str = Field(min_length=1, max_length=64)
    card_id: int
    response_type: ResponseType
    confidence_level: ConfidenceLevel | None = None
    reviewed_at: datetime


class SyncBatchRequest(BaseModel):
    """Batch sync request for offline reviews (Req 24.5)."""

    items: list[SyncItem] = Field(min_length=1, max_length=50)


class SyncBatchResponse(BaseModel):
    """Response from the batch sync endpoint."""

    accepted: int = 0
    duplicates: int = 0
    failures: int = 0


# ---------------------------------------------------------------------------
# Analytics schemas
# ---------------------------------------------------------------------------


class AnalyticsFilters(BaseModel):
    """Filters for analytics endpoints (Req 7.5)."""

    start_date: date | None = None
    end_date: date | None = None
    tags: list[str] | None = None
    deck_ids: list[int] | None = None


class TagRetention(BaseModel):
    """Per-tag retention average (Req 7.1)."""

    tag: str
    average_retention: float
    card_count: int


class ForgettingCurvePoint(BaseModel):
    """A single point on the forgetting curve (Req 7.2)."""

    day: int
    predicted_retention: float


class HeatmapDay(BaseModel):
    """One day in the retention heatmap (Req 7.3)."""

    date: date
    review_count: int
    average_retention: float


class RetentionAnalytics(BaseModel):
    """Retention analytics response (Req 7.1-7.3)."""

    per_tag_retention: list[TagRetention] = Field(default_factory=list)
    forgetting_curve: list[ForgettingCurvePoint] = Field(default_factory=list)
    heatmap: list[HeatmapDay] = Field(default_factory=list)


class SubjectStrength(BaseModel):
    """A subject (tag) with its mastery level."""

    tag: str
    mastery_percentage: float


class UserDashboard(BaseModel):
    """User analytics dashboard response."""

    overall_retention: float = 0.0
    current_streak: int = 0
    longest_streak: int = 0
    strongest_subjects: list[SubjectStrength] = Field(default_factory=list)
    weakest_subjects: list[SubjectStrength] = Field(default_factory=list)
    predicted_readiness: float = 0.0


# ---------------------------------------------------------------------------
# Social / Creator schemas
# ---------------------------------------------------------------------------


class CreatorProfileResponse(BaseModel):
    """Public creator profile (Req 15.1-15.5)."""

    model_config = ConfigDict(from_attributes=True)

    username: str
    total_xp: int = 0
    follower_count: int = 0
    published_deck_count: int = 0
    total_cards_created: int = 0
    average_deck_rating: float | None = None
    public_decks: list[DeckResponse] = Field(default_factory=list)


class CommentCreate(BaseModel):
    """Payload for posting a comment on a deck (Req 17.1, 17.5)."""

    body: str = Field(min_length=1, max_length=1000)
    parent_comment_id: int | None = None


class CommentResponse(BaseModel):
    """Read-side projection of a deck comment (Req 17.3)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    username: str
    body: str
    parent_comment_id: int | None = None
    nesting_level: int = 0
    created_at: datetime


# ---------------------------------------------------------------------------
# Generation schemas
# ---------------------------------------------------------------------------


class GenerateRequest(BaseModel):
    """Payload for generating flashcards from lesson content (Req 11.7)."""

    lesson_content: str = Field(min_length=50)
    lesson_id: int
    requested_card_count: int = Field(default=25, ge=10, le=50)
