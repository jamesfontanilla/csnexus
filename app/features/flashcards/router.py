"""FastAPI router for the Flashcard Learning Ecosystem.

Mounts all flashcard endpoints under /v1/flashcards.
Uses get_current_user for auth and get_flashcard_service for DI.

Requirements: 29.1-29.5, 30.2, 30.3
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user, require_admin
from app.common.schemas.request import PaginationParams
from app.features.flashcards.repository import FlashcardRepository
from app.features.flashcards.schemas import (
    CardResponse,
    CardResponseResult,
    CommentCreate,
    DeckCreate,
    DeckFilters,
    DeckRatingCreate,
    DeckResponse,
    DeckUpdate,
    ExamAnswer,
    ExamSimulationStart,
    FlashcardCreate,
    FlashcardResponse,
    FlashcardUpdate,
    GenerateRequest,
    MarketplaceSearch,
    QueueFilters,
    QueueSummary,
    StudySessionStart,
    StudySessionSummary,
    SyncBatchRequest,
    SyncBatchResponse,
)
from app.features.flashcards.service import FlashcardService
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/flashcards", tags=["flashcards"])


# ---------------------------------------------------------------------------
# Dependency injection
# ---------------------------------------------------------------------------


def get_flashcard_service(
    db: Session = Depends(get_db),
) -> FlashcardService:
    """Construct FlashcardService for the request scope."""
    return FlashcardService(flashcard_repo=FlashcardRepository(db=db))


# ---------------------------------------------------------------------------
# Deck CRUD endpoints
# ---------------------------------------------------------------------------


@router.post("/decks", status_code=status.HTTP_201_CREATED, response_model=DeckResponse)
def create_deck(
    payload: DeckCreate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> DeckResponse:
    """Create a new flashcard deck."""
    return service.create_deck(user, payload)


@router.get("/decks", response_model=list[DeckResponse])
def list_decks(
    pagination: PaginationParams = Depends(),
    filters: DeckFilters = Depends(),
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """List the current user's decks."""
    decks, _ = service.list_user_decks(
        user, filters, skip=pagination.skip, limit=pagination.limit
    )
    return decks


@router.get("/decks/{deck_id}", response_model=DeckResponse)
def get_deck(
    deck_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> DeckResponse:
    """Get a deck by ID."""
    return service.get_deck(user, deck_id)


@router.patch("/decks/{deck_id}", response_model=DeckResponse)
def update_deck(
    deck_id: int,
    payload: DeckUpdate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> DeckResponse:
    """Update a deck."""
    return service.update_deck(user, deck_id, payload)


@router.delete("/decks/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deck(
    deck_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> None:
    """Soft-delete a deck."""
    service.delete_deck(user, deck_id)


@router.post("/decks/{deck_id}/:duplicate", status_code=status.HTTP_201_CREATED, response_model=DeckResponse)
def duplicate_deck(
    deck_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> DeckResponse:
    """Duplicate a deck."""
    return service.duplicate_deck(user, deck_id)


# ---------------------------------------------------------------------------
# Flashcard CRUD endpoints
# ---------------------------------------------------------------------------


@router.post("/decks/{deck_id}/cards", status_code=status.HTTP_201_CREATED, response_model=FlashcardResponse)
def create_flashcard(
    deck_id: int,
    payload: FlashcardCreate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> FlashcardResponse:
    """Create a flashcard in a deck."""
    return service.create_flashcard(user, deck_id, payload)


@router.get("/decks/{deck_id}/cards", response_model=list[FlashcardResponse])
def list_flashcards(
    deck_id: int,
    pagination: PaginationParams = Depends(),
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """List flashcards in a deck."""
    deck = service.get_deck(user, deck_id)
    return service._repo.list_deck_flashcards(
        deck.id, skip=pagination.skip, limit=pagination.limit
    )


@router.patch("/cards/{card_id}", response_model=FlashcardResponse)
def update_flashcard(
    card_id: int,
    payload: FlashcardUpdate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> FlashcardResponse:
    """Update a flashcard."""
    return service.update_flashcard(user, card_id, payload)


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flashcard(
    card_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> None:
    """Soft-delete a flashcard."""
    service.delete_flashcard(user, card_id)


# ---------------------------------------------------------------------------
# Study session and queue endpoints
# ---------------------------------------------------------------------------


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
def start_session(
    payload: StudySessionStart,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Start a study session."""
    session = service.start_study_session(user, payload)
    return {"id": session.id, "study_mode": session.study_mode}


@router.post("/sessions/{session_id}/respond", response_model=CardResponseResult)
def record_response(
    session_id: int,
    payload: CardResponse,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> CardResponseResult:
    """Record a card response during a session."""
    return service.record_response(user, session_id, payload)


@router.post("/sessions/{session_id}/:end", response_model=StudySessionSummary)
def end_session(
    session_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> StudySessionSummary:
    """End a study session."""
    return service.end_study_session(user, session_id)


@router.get("/queue", response_model=list[FlashcardResponse])
def get_queue(
    filters: QueueFilters = Depends(),
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """Get the daily review queue."""
    return service.get_daily_queue(user, filters)


@router.get("/queue/summary", response_model=QueueSummary)
def get_queue_summary(
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> QueueSummary:
    """Get queue summary counts."""
    return service.get_queue_summary(user)


# ---------------------------------------------------------------------------
# Marketplace and social endpoints
# ---------------------------------------------------------------------------


@router.get("/marketplace", response_model=list[DeckResponse])
def search_marketplace(
    search: MarketplaceSearch = Depends(),
    pagination: PaginationParams = Depends(),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """Browse/search public decks (public endpoint)."""
    category = search.category.value if search.category else None
    decks, _ = service.search_marketplace(
        query=search.query,
        category=category,
        sort_by=search.sort_by,
        min_rating=search.min_rating,
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return decks


@router.post("/marketplace/{deck_id}/:clone", status_code=status.HTTP_201_CREATED, response_model=DeckResponse)
def clone_deck(
    deck_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> DeckResponse:
    """Clone a public deck."""
    return service.clone_deck(user, deck_id)


@router.post("/marketplace/{deck_id}/ratings", status_code=status.HTTP_201_CREATED)
def rate_deck(
    deck_id: int,
    payload: DeckRatingCreate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Rate a deck."""
    service.rate_deck(user, deck_id, payload.rating)
    return {"status": "ok"}


@router.get("/marketplace/{deck_id}/comments")
def list_comments(
    deck_id: int,
    pagination: PaginationParams = Depends(),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """List comments for a deck (public)."""
    return service.list_comments(deck_id, skip=pagination.skip, limit=pagination.limit)


@router.post("/marketplace/{deck_id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    deck_id: int,
    payload: CommentCreate,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Post a comment on a deck."""
    comment = service.create_comment(user, deck_id, payload.body, payload.parent_comment_id)
    return {"id": comment.id}


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> None:
    """Delete own comment."""
    service.delete_comment(user, comment_id)


@router.post("/creators/{creator_id}/:follow", status_code=status.HTTP_201_CREATED)
def follow_creator(
    creator_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Follow a creator."""
    service.follow_creator(user, creator_id)
    return {"status": "ok"}


@router.delete("/creators/{creator_id}/:follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_creator(
    creator_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> None:
    """Unfollow a creator."""
    service.unfollow_creator(user, creator_id)


@router.get("/feed", response_model=list[DeckResponse])
def get_feed(
    pagination: PaginationParams = Depends(),
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> list:
    """Get followed creators' recent decks."""
    return service.get_feed(user, skip=pagination.skip, limit=pagination.limit)


# ---------------------------------------------------------------------------
# Generation, analytics, exam, sync, and admin endpoints
# ---------------------------------------------------------------------------


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_flashcards_endpoint(
    payload: GenerateRequest,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Generate flashcards from lesson content."""
    from app.features.flashcards.algorithms.generator import generate_flashcards as gen

    result = gen(payload.lesson_content, payload.lesson_id)
    if result.error:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail=result.error)
    return {
        "cards": [
            {"front": c.front, "back": c.back, "card_type": c.card_type.value, "difficulty": c.difficulty.value}
            for c in result.cards
        ],
        "terms_extracted": result.terms_extracted,
    }


@router.get("/recommendations")
def get_recommendations(
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Get study recommendations."""
    from app.features.flashcards.algorithms.recommendation import generate_recommendations

    tag_data = service._repo.get_retention_by_tag(user.id)
    counts = service._repo.get_queue_summary_counts(user.id)
    decks, _ = service._repo.list_user_decks(user.id)

    result = generate_recommendations(
        tag_retention_data=tag_data,
        total_due=counts["total_due"],
        total_cards=0,
        current_streak=0,
        has_any_decks=len(decks) > 0,
    )
    return {
        "recommendations": [
            {"type": r.type, "title": r.title, "description": r.description}
            for r in result.recommendations
        ],
        "recommended_daily_cards": result.recommended_daily_cards,
    }


@router.get("/analytics/dashboard")
def get_dashboard(
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Get user analytics dashboard."""
    return service.get_user_dashboard(user)


@router.get("/analytics/retention")
def get_retention(
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Get retention analytics."""
    tag_data = service._repo.get_retention_by_tag(user.id)
    return {
        "per_tag_retention": [
            {"tag": t, "average_retention": r, "card_count": c}
            for t, r, c in tag_data
        ]
    }


@router.get("/analytics/heatmap")
def get_heatmap(
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Get review heatmap."""
    data = service._repo.get_review_heatmap(user.id)
    return {
        "heatmap": [
            {"date": str(d), "review_count": c, "average_retention": r}
            for d, c, r in data
        ]
    }


@router.post("/exam-simulations", status_code=status.HTTP_201_CREATED)
def start_exam(
    payload: ExamSimulationStart,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Start an exam simulation."""
    sim = service.start_exam_simulation(
        user, payload.deck_ids, payload.card_count, payload.time_limit_seconds
    )
    return {"id": sim.id, "question_count": sim.question_count}


@router.post("/exam-simulations/{sim_id}/answer")
def submit_exam_answer(
    sim_id: int,
    payload: ExamAnswer,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Submit an exam answer."""
    service.submit_exam_answer(user, sim_id, payload.card_id, payload.answer)
    return {"status": "ok"}


@router.post("/exam-simulations/{sim_id}/:complete")
def complete_exam(
    sim_id: int,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Complete an exam simulation."""
    return service.complete_exam_simulation(user, sim_id)


@router.post("/sync")
def batch_sync(
    payload: SyncBatchRequest,
    user: User = Depends(get_current_user),
    service: FlashcardService = Depends(get_flashcard_service),
) -> SyncBatchResponse:
    """Batch sync offline reviews."""
    items = [item.model_dump() for item in payload.items]
    result = service.batch_sync_reviews(user, items)
    return SyncBatchResponse(**result)


# ---------------------------------------------------------------------------
# Admin endpoints
# ---------------------------------------------------------------------------


@router.get("/admin/analytics")
def admin_analytics(
    user: User = Depends(require_admin),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Admin analytics (admin only)."""
    return service.get_admin_analytics()


@router.post("/admin/decks/{deck_id}/:flag")
def flag_deck(
    deck_id: int,
    user: User = Depends(require_admin),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Flag a deck for removal (admin only)."""
    service.flag_deck(deck_id)
    return {"status": "ok"}


@router.post("/admin/decks/{deck_id}/:feature")
def feature_deck(
    deck_id: int,
    user: User = Depends(require_admin),
    service: FlashcardService = Depends(get_flashcard_service),
) -> dict:
    """Toggle deck featured status (admin only)."""
    service.toggle_featured(deck_id)
    return {"status": "ok"}
