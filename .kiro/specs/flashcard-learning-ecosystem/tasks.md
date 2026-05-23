# Implementation Plan: Flashcard Learning Ecosystem

## Overview

This plan implements the Flashcard Learning Ecosystem in 7 phases following the feature-sliced architecture. Each phase builds incrementally on the previous, starting with core data models and CRUD, then layering spaced repetition, pseudo-AI generation, social features, gamification integrations, offline sync support, and admin analytics. Algorithm modules (FSRS, generator, interleaving, similarity) are implemented as pure functions under `app/features/flashcards/algorithms/` and tested with Hypothesis property-based tests.

## Tasks

- [x] 1. Set up project structure, models, and schemas
  - [x] 1.1 Create feature directory structure and `__init__.py` files
    - Create `app/features/flashcards/__init__.py`
    - Create `app/features/flashcards/algorithms/__init__.py`
    - Create `tests/features/flashcards/__init__.py`
    - _Requirements: 30.1, 30.5_

  - [x] 1.2 Implement SQLAlchemy ORM models
    - Create `app/features/flashcards/models.py` with all models: Deck, Flashcard, ReviewLog, StudySession, DeckRating, DeckBookmark, DeckComment, Follow, DeckReport, ExamSimulation, ExamSimulationAnswer, FlashcardNotification
    - Include all enums: DeckVisibility, DeckCategory, CardType, StudyMode, ConfidenceLevel, ResponseType
    - Include all constraints, indexes, and check constraints as specified in the design
    - _Requirements: 30.1, 30.4, 30.8_

  - [x] 1.3 Implement Pydantic schemas
    - Create `app/features/flashcards/schemas.py` with request/response schemas
    - DeckCreate, DeckUpdate, DeckResponse, DeckFilters
    - FlashcardCreate, FlashcardUpdate, FlashcardResponse
    - StudySessionStart, CardResponse, CardResponseResult, StudySessionSummary
    - QueueFilters, QueueSummary
    - MarketplaceSearch, DeckRatingCreate
    - ExamSimulationStart, ExamAnswer, ExamSimulationResult
    - SyncBatchRequest, SyncItem, SyncBatchResponse
    - AnalyticsFilters, RetentionAnalytics, UserDashboard
    - CreatorProfileResponse, CommentCreate, CommentResponse
    - Use `model_config = {"from_attributes": True}` for ORM serialization
    - _Requirements: 30.2, 30.3, 30.6_

- [x] 2. Implement FSRS spaced repetition algorithm
  - [x] 2.1 Implement FSRS engine pure functions
    - Create `app/features/flashcards/algorithms/fsrs.py`
    - Implement `CardState` frozen dataclass, `SchedulingResult` frozen dataclass
    - Implement `compute_next_interval(state, response, confidence, today)` with all interval formulas and confidence multipliers
    - Implement `compute_retention_score(memory_stability, elapsed_days)`
    - Implement `compute_mastery_percentage(successful_reviews, total_reviews, retention_score)`
    - Ensure all parameter clamping: ease_factor [1.3, 3.5], memory_stability ≥ 0.1, review_interval [1, 365]
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 10.2_

  - [x] 2.2 Write property test: FSRS interval computation correctness
    - **Property 1: FSRS interval computation correctness**
    - **Validates: Requirements 5.2, 5.3, 5.4, 5.5, 10.2**

  - [x] 2.3 Write property test: FSRS parameter invariants
    - **Property 2: FSRS parameter invariants**
    - **Validates: Requirements 5.1, 5.8, 5.9**

  - [x] 2.4 Write property test: FSRS determinism
    - **Property 3: FSRS determinism**
    - **Validates: Requirements 5.10**

  - [x] 2.5 Write property test: FSRS round-trip scheduling
    - **Property 4: FSRS round-trip scheduling**
    - **Validates: Requirements 5.11**

  - [x] 2.6 Write property test: Retention score formula
    - **Property 5: Retention score formula**
    - **Validates: Requirements 5.6**

  - [x] 2.7 Write property test: Mastery percentage formula
    - **Property 6: Mastery percentage formula**
    - **Validates: Requirements 5.7**

- [x] 3. Implement similarity and interleaving algorithms
  - [x] 3.1 Implement similarity engine
    - Create `app/features/flashcards/algorithms/similarity.py`
    - Implement `AnswerComparison` dataclass, `Strictness` enum
    - Implement `compare_typed_answer(user_answer, correct_answer, strictness)` using Levenshtein distance ratio
    - Support EXACT, CONTAINS, and FUZZY strictness modes
    - _Requirements: 8.4_

  - [x] 3.2 Write property test: Typed answer comparison
    - **Property 13: Typed answer comparison**
    - **Validates: Requirements 8.4**

  - [x] 3.3 Implement interleaving algorithm
    - Create `app/features/flashcards/algorithms/interleaving.py`
    - Implement `interleave_cards(cards, max_consecutive_same_category=3)`
    - Round-robin across categories, swap to fix consecutive violations
    - Pure function — does not modify input list
    - _Requirements: 9.1, 9.2_

  - [x] 3.4 Write property test: Interleaving constraint
    - **Property 12: Interleaving constraint**
    - **Validates: Requirements 9.1, 9.2**

- [x] 4. Checkpoint - Ensure all algorithm tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement repository layer
  - [x] 5.1 Implement FlashcardRepository
    - Create `app/features/flashcards/repository.py`
    - Deck CRUD methods: create_deck, get_deck, update_deck, soft_delete_deck, list_user_decks, duplicate_deck
    - Flashcard CRUD methods: create_flashcard, get_flashcard, update_flashcard, soft_delete_flashcard, list_deck_flashcards, count_deck_flashcards
    - Review methods: record_review, get_review_history, get_card_confidence_history
    - Queue methods: get_daily_queue (priority ordering), get_bonus_review_cards, get_queue_summary_counts
    - Session methods: create_session, update_session, get_session
    - Marketplace methods: search_decks (full-text), get_deck_ratings, upsert_rating, compute_average_rating
    - Social methods: create_bookmark, delete_bookmark, create_follow, delete_follow, get_followers, get_following, get_feed_decks
    - Comment methods: create_comment, soft_delete_comment, list_deck_comments
    - Exam methods: create_simulation, get_simulation, record_answer, get_simulation_answers, get_historical_scores
    - Sync methods: batch_upsert_reviews (deduplicate by client_event_id)
    - Analytics methods: get_retention_by_tag, get_review_heatmap, get_mastery_progression, get_admin_analytics
    - All queries filter `WHERE deleted_at IS NULL` by default
    - _Requirements: 1.1–1.12, 2.1–2.8, 6.1–6.7, 14.1–14.9, 15.1–15.5, 16.1–16.6, 17.1–17.7, 22.1–22.9, 26.1–26.6, 27.1–27.6, 28.1–28.7_

  - [x] 5.2 Write repository layer unit tests
    - Create `tests/features/flashcards/test_repository.py`
    - Test deck CRUD with soft-delete filtering
    - Test flashcard CRUD with deck association and capacity limit (500)
    - Test review log insertion and querying
    - Test queue query with priority ordering
    - Test marketplace search with full-text matching
    - Test rating computation queries
    - Test follow relationship CRUD
    - Test unique constraints (deck title per user, one rating per user per deck)
    - Use real in-memory SQLite DB via `db_session` fixture
    - _Requirements: 30.4_

- [ ] 6. Implement service layer - Core CRUD and study sessions
  - [x] 6.1 Implement FlashcardService - Deck and card CRUD
    - Create `app/features/flashcards/service.py`
    - Implement constructor with dependency injection (FlashcardRepository, XPService, AchievementService, FocusService)
    - Implement create_deck, update_deck, delete_deck, list_user_decks, duplicate_deck
    - Implement create_flashcard with type-specific validation (cloze, mcq, matching, sequence, basic/reverse/true_false)
    - Implement update_flashcard preserving scheduling metadata
    - Implement delete_flashcard (soft-delete)
    - Enforce deck capacity limit (500 cards)
    - Enforce unique deck titles per user
    - Enforce ownership checks on all mutations
    - _Requirements: 1.1–1.12, 2.1–2.8, 29.2_

  - [x] 6.2 Write property test: Card type-specific validation
    - **Property 7: Card type-specific validation**
    - **Validates: Requirements 1.3, 1.4, 1.5, 1.6, 1.12**

  - [x] 6.3 Write property test: Flashcard update preserves scheduling
    - **Property 8: Flashcard update preserves scheduling**
    - **Validates: Requirements 1.7**

  - [x] 6.4 Implement FlashcardService - Study sessions and review queue
    - Implement start_study_session (all 6 modes: swipe, typing, rapid_recall, quiz, timed, exam_simulation)
    - Implement record_response: call FSRS engine, update card scheduling, record review log, handle confidence tracking
    - Implement end_study_session: compute summary stats, award XP
    - Implement get_daily_queue with priority ordering and cap
    - Implement get_queue_summary with computed counts
    - Implement interleaving toggle (call interleaving algorithm when enabled)
    - Implement graduation logic (5 consecutive mastered → graduated)
    - _Requirements: 3.1–3.7, 4.1–4.6, 5.1–5.11, 6.1–6.7, 8.1–8.4, 9.1–9.4, 10.1–10.5_

  - [x] 6.5 Write property test: Daily queue priority ordering
    - **Property 9: Daily queue priority ordering**
    - **Validates: Requirements 6.1**

  - [x] 6.6 Write property test: Queue cap truncation
    - **Property 10: Queue cap truncation**
    - **Validates: Requirements 6.4**

  - [x] 6.7 Write property test: Queue summary computation
    - **Property 11: Queue summary computation**
    - **Validates: Requirements 6.6**

  - [x] 6.8 Write property test: Graduation after consecutive mastered reviews
    - **Property 14: Graduation after consecutive mastered reviews**
    - **Validates: Requirements 10.5**

  - [x] 6.9 Write property test: Study session result accuracy
    - **Property 15: Study session result accuracy**
    - **Validates: Requirements 3.7**

- [x] 7. Checkpoint - Ensure all core service tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement service layer - Marketplace, social, and deck operations
  - [x] 8.1 Implement FlashcardService - Marketplace and social features
    - Implement search_marketplace with full-text search, sorting, filtering, pagination
    - Implement rate_deck: enforce 1–5 range, one per user, no self-rating, recompute average
    - Implement clone_deck: full copy with attribution, increment clone_count, award XP to creator
    - Implement bookmark/unbookmark deck
    - Implement follow/unfollow creator (prevent self-follow, create notifications)
    - Implement get_creator_profile (public endpoint)
    - Implement get_feed (followed creators' recent decks)
    - Implement create_comment, delete_comment (soft-delete), list_comments with threading
    - Implement comment moderation keyword filter (hold for review)
    - _Requirements: 14.1–14.9, 15.1–15.5, 16.1–16.6, 17.1–17.7_

  - [x] 8.2 Write property test: Deck duplication content fidelity
    - **Property 16: Deck duplication content fidelity**
    - **Validates: Requirements 2.5, 14.6**

  - [x] 8.3 Write property test: Deck rating average computation
    - **Property 17: Deck rating average computation**
    - **Validates: Requirements 14.4, 14.5**

  - [x] 8.4 Write property test: Deck soft-delete cascades to all cards
    - **Property 24: Deck soft-delete cascades to all cards**
    - **Validates: Requirements 2.6**

- [ ] 9. Implement pseudo-AI generator and recommendation engine
  - [x] 9.1 Implement pseudo-AI flashcard generator
    - Create `app/features/flashcards/algorithms/generator.py`
    - Implement term extraction using regex patterns: "Term: Definition", "Term — Definition", bold markdown, italic markdown, markdown table rows
    - Implement difficulty classification using word frequency thresholds (easy/medium/hard)
    - Implement basic card generation (40% target)
    - Implement cloze deletion card generation (35% target) with `{{c1::term::hint}}` format
    - Implement MCQ card generation (25% target) with distractor selection
    - Implement mnemonic generation for medium/hard cards (acronym, association, rhyming)
    - Return GenerationResult preview with all cards for user review
    - Enforce 10–50 cards per lesson, error if < 10 terms extracted
    - No paid LLM APIs — all deterministic heuristics
    - _Requirements: 11.1–11.10_

  - [x] 9.2 Write property test: Generated card validity invariant
    - **Property 18: Generated card validity invariant**
    - **Validates: Requirements 11.10**

  - [x] 9.3 Write property test: Difficulty classification correctness
    - **Property 19: Difficulty classification correctness**
    - **Validates: Requirements 11.4**

  - [x] 9.4 Implement recommendation engine
    - Create `app/features/flashcards/algorithms/recommendation.py`
    - Implement weak subtopic identification (5 lowest retention_score tags)
    - Implement marketplace deck recommendations for weak areas
    - Implement personalized daily review count recommendation
    - Implement targeted quiz suggestions (cards with retention < 0.6)
    - Implement starter deck recommendations for new users
    - _Requirements: 12.1–12.5_

  - [x] 9.5 Implement explanation engine in service layer
    - Implement template-based explanations by card tag category
    - Grammar → grammar rule templates, vocabulary → etymology templates, numerical → formula templates, analytical → logic templates
    - Deep link to relevant lesson section by tag-to-slug matching
    - Fallback to card's stored explanation field
    - No paid LLM APIs
    - _Requirements: 13.1–13.5_

- [ ] 10. Implement gamification integrations
  - [x] 10.1 Implement XP integration
    - Call XPService.award() on session end: (2 × cards_reviewed) + (1 × cards_remembered)
    - Call XPService.award() on deck creation (10th card milestone): 25 XP
    - Call XPService.award() on deck clone (to original creator): 10 XP
    - Call XPService.award() on daily review complete: 15 XP
    - Apply XPMultiplierService.apply_multiplier() before all awards
    - Use client_event_id format for idempotency
    - Handle XP failures gracefully (persist session, log error)
    - _Requirements: 18.1–18.7_

  - [x] 10.2 Implement achievement integration
    - Trigger achievement checks at qualifying events: 100 reviews, 1000 reviews, 7-day streak, 30-day streak, 90% deck mastery, 5 published decks
    - Call existing AchievementService after qualifying events
    - _Requirements: 19.1–19.7_

  - [x] 10.3 Implement leaderboard and focus mode integration
    - Expose flashcard_review_streak, total_cards_mastered, deck_popularity_score metrics
    - Implement focus mode: call FocusService.start_session() and complete_session()
    - Return wellness reminder when session exceeds threshold
    - Include focus_session_id in response when active
    - _Requirements: 20.1–20.4, 21.1–21.4_

  - [x] 10.4 Write property test: Deck popularity score formula
    - **Property 20: Deck popularity score formula**
    - **Validates: Requirements 20.3**

- [ ] 11. Implement exam simulation and analytics
  - [x] 11.1 Implement exam simulation service methods
    - Implement start_exam_simulation: validate deck card counts, category distribution, select random cards
    - Implement submit_exam_answer: lock answer on submission, prevent changes
    - Implement complete_exam_simulation: compute scores, percentile estimate, store results
    - Handle time limit expiry (auto-submit skipped)
    - Reject if insufficient cards or category cards
    - _Requirements: 22.1–22.9_

  - [x] 11.2 Write property test: Exam simulation scoring
    - **Property 21: Exam simulation scoring**
    - **Validates: Requirements 22.7**

  - [x] 11.3 Implement user analytics dashboard
    - Overall retention percentage, current/longest streak
    - Strongest/weakest subjects (top/bottom 3 tags)
    - Mastery heatmap (90-day grid)
    - Study time analytics
    - Predicted exam readiness score (weighted by CSE distribution)
    - _Requirements: 26.1–26.6_

  - [x] 11.4 Write property test: Predicted exam readiness
    - **Property 22: Predicted exam readiness**
    - **Validates: Requirements 26.6**

  - [x] 11.5 Implement admin analytics and moderation
    - Top 20 most-failed cards and decks
    - Engagement metrics (daily active reviewers, avg cards/session, etc.)
    - Category breakdown
    - Trending decks (7-day growth)
    - Moderation queue (reported decks, flagged comments)
    - Flag deck for removal, toggle featured, ban comment
    - Auto-add to moderation queue at 3+ reports
    - Log all moderation actions to AuditService
    - Restrict to admin role via RBAC middleware
    - _Requirements: 27.1–27.6, 28.1–28.7_

- [x] 12. Checkpoint - Ensure all service layer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Implement sync endpoint and retention analytics
  - [x] 13.1 Implement batch sync endpoint
    - Implement POST `/v1/flashcards/sync` accepting SyncBatchRequest (max 50 items)
    - Deduplicate by client_event_id (skip already-persisted)
    - Process reviews in chronological order
    - Return accepted count, duplicate count, and failures
    - _Requirements: 24.1–24.10_

  - [x] 13.2 Write property test: Sync deduplication by client_event_id
    - **Property 23: Sync deduplication by client_event_id**
    - **Validates: Requirements 24.3, 24.8**

  - [x] 13.3 Implement retention analytics endpoints
    - Per-tag retention averages
    - Forgetting curve predictions (day 1, 3, 7, 14, 30)
    - Retention heatmap (90-day daily review counts + avg retention)
    - Mastery graph (weekly progression per deck/tag)
    - Date range filtering
    - _Requirements: 7.1–7.5_

- [x] 14. Implement router layer
  - [x] 14.1 Implement flashcard router - Deck and card endpoints
    - Create `app/features/flashcards/router.py`
    - POST `/v1/flashcards/decks` (201), GET `/v1/flashcards/decks` (200), GET `/v1/flashcards/decks/{id}` (200)
    - PATCH `/v1/flashcards/decks/{id}` (200), DELETE `/v1/flashcards/decks/{id}` (204)
    - POST `/v1/flashcards/decks/{id}/:duplicate` (201)
    - POST `/v1/flashcards/decks/{id}/cards` (201), GET `/v1/flashcards/decks/{id}/cards` (200)
    - PATCH `/v1/flashcards/cards/{id}` (200), DELETE `/v1/flashcards/cards/{id}` (204)
    - Wire dependency injection via `get_flashcard_service` factory
    - Use `get_current_user` dependency for auth
    - _Requirements: 29.1–29.5, 30.2, 30.3_

  - [x] 14.2 Implement flashcard router - Study session and queue endpoints
    - POST `/v1/flashcards/sessions` (201), POST `/v1/flashcards/sessions/{id}/respond` (200)
    - POST `/v1/flashcards/sessions/{id}/:end` (200)
    - GET `/v1/flashcards/queue` (200), GET `/v1/flashcards/queue/summary` (200)
    - _Requirements: 3.1–3.7, 6.1–6.7_

  - [x] 14.3 Implement flashcard router - Marketplace and social endpoints
    - GET `/v1/flashcards/marketplace` (200, public)
    - POST `/v1/flashcards/marketplace/{id}/:clone` (201)
    - POST `/v1/flashcards/marketplace/{id}/ratings` (201)
    - GET `/v1/flashcards/marketplace/{id}/comments` (200, public)
    - POST `/v1/flashcards/marketplace/{id}/comments` (201)
    - DELETE `/v1/flashcards/comments/{id}` (204)
    - GET `/v1/flashcards/creators/{id}` (200, public)
    - POST `/v1/flashcards/creators/{id}/:follow` (201)
    - DELETE `/v1/flashcards/creators/{id}/:follow` (204)
    - GET `/v1/flashcards/feed` (200)
    - _Requirements: 14.1–14.9, 15.1–15.5, 16.1–16.6, 17.1–17.7_

  - [x] 14.4 Implement flashcard router - Generation, analytics, exam, sync, and admin endpoints
    - POST `/v1/flashcards/generate` (201)
    - GET `/v1/flashcards/recommendations` (200)
    - GET `/v1/flashcards/analytics/retention` (200)
    - GET `/v1/flashcards/analytics/dashboard` (200)
    - GET `/v1/flashcards/analytics/heatmap` (200)
    - POST `/v1/flashcards/exam-simulations` (201)
    - POST `/v1/flashcards/exam-simulations/{id}/answer` (200)
    - POST `/v1/flashcards/exam-simulations/{id}/:complete` (200)
    - GET `/v1/flashcards/admin/analytics` (200, admin only)
    - GET `/v1/flashcards/admin/moderation` (200, admin only)
    - POST `/v1/flashcards/admin/decks/{id}/:flag` (200, admin only)
    - POST `/v1/flashcards/admin/decks/{id}/:feature` (200, admin only)
    - POST `/v1/flashcards/sync` (200)
    - Register router in `app/main.py`
    - _Requirements: 11.7, 12.1–12.5, 22.1–22.9, 26.1–26.6, 27.1–27.6, 28.1–28.7, 24.1–24.10_

- [x] 15. Write service and router layer tests
  - [x] 15.1 Write service layer unit tests
    - Create `tests/features/flashcards/test_service.py`
    - Test all business rule validations (card type, deck capacity, ownership)
    - Test FSRS scheduling integration (service calls algorithm, updates card)
    - Test XP award orchestration (verify XPService.award called with correct args)
    - Test achievement trigger points
    - Test study session lifecycle (start → respond → end)
    - Test exam simulation lifecycle with time enforcement
    - Test marketplace operations (rate, clone, search)
    - Test social operations (follow, comment, moderation)
    - Use MagicMock(spec=FlashcardRepository) for repository mocking
    - _Requirements: 30.1_

  - [x] 15.2 Write router layer unit tests
    - Create `tests/features/flashcards/test_router.py`
    - Test every endpoint: happy path + auth failure + validation failure
    - Test pagination parameter handling
    - Test public vs. authenticated endpoint access
    - Test admin-only endpoint gating
    - Use TestClient with mocked service via dependency_overrides
    - _Requirements: 29.1–29.5, 30.2, 30.3_

- [x] 16. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using Hypothesis (min 100 examples each)
- Unit tests validate specific examples and edge cases per the three-layer test strategy
- The offline/PWA requirements (23, 24, 25) are client-side concerns; only the backend sync endpoint (task 13.1) is implemented here
- Algorithm modules are pure functions with no DB access — tested independently of the service layer
- All XP/achievement/focus/leaderboard integrations use existing service interfaces

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["2.1", "3.1", "3.3"] },
    { "id": 3, "tasks": ["2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "3.2", "3.4"] },
    { "id": 4, "tasks": ["5.1"] },
    { "id": 5, "tasks": ["5.2", "6.1"] },
    { "id": 6, "tasks": ["6.2", "6.3", "6.4"] },
    { "id": 7, "tasks": ["6.5", "6.6", "6.7", "6.8", "6.9", "8.1", "9.1", "9.4", "9.5"] },
    { "id": 8, "tasks": ["8.2", "8.3", "8.4", "9.2", "9.3", "10.1", "10.2", "10.3"] },
    { "id": 9, "tasks": ["10.4", "11.1", "11.3", "11.5"] },
    { "id": 10, "tasks": ["11.2", "11.4", "13.1", "13.3"] },
    { "id": 11, "tasks": ["13.2", "14.1", "14.2", "14.3", "14.4"] },
    { "id": 12, "tasks": ["15.1", "15.2"] }
  ]
}
```
