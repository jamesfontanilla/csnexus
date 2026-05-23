# Requirements Document

## Introduction

This feature adds a comprehensive Flashcard & Adaptive Study Ecosystem to CSNexus — a Gizmo-inspired system that enables Civil Service Exam candidates to create, study, and share flashcards with spaced repetition, pseudo-AI generation, social features, and offline support. The system integrates with existing XP, achievements, leaderboard, focus mode, and study session modules. It is organized into seven implementation phases: Core Flashcard System, Spaced Repetition & Review, Pseudo-AI System, Social & Community, Gamification & Integration, Offline & Performance, and Analytics & Admin.

## Glossary

- **Flashcard_Service**: The backend service (`app/features/flashcards/service.py`) that handles flashcard CRUD, study logic, and deck management
- **Deck**: An ordered collection of flashcards owned by a user, with metadata (title, description, tags, visibility, category)
- **Flashcard**: A single study item within a Deck containing a front face, back face, card type, and scheduling metadata
- **Card_Type**: One of: basic, reverse, cloze, mcq, true_false, matching, sequence
- **FSRS_Engine**: The Free Spaced Repetition Scheduler-inspired algorithm module (`app/features/flashcards/algorithms/fsrs.py`) that computes review intervals
- **Review_Queue**: The ordered list of flashcards due for review for a given user on a given day
- **Pseudo_AI_Generator**: The deterministic NLP module (`app/features/flashcards/algorithms/generator.py`) that generates flashcards from lesson content using heuristics, templates, and regex — no paid LLM APIs
- **Marketplace**: The public-facing deck browsing and sharing system where users can publish, clone, rate, and bookmark decks
- **Sync_Engine**: The frontend module that manages IndexedDB persistence, optimistic updates, conflict resolution, and background sync with the backend
- **Study_Mode**: A specific interaction pattern for reviewing flashcards (swipe, typing, rapid_recall, quiz, timed, exam_simulation)
- **Confidence_Level**: A user self-assessment on recall quality: guessed, unsure, confident, mastered
- **Retention_Score**: A per-card metric (0.0–1.0) representing estimated probability of recall at the current moment
- **Memory_Stability**: A per-card metric representing how resistant a memory is to forgetting, measured in days
- **Creator_Profile**: A public-facing user profile showing published decks, follower count, and mastery statistics

## Requirements

---

## Phase 1: Core Flashcard System

### Requirement 1: Flashcard CRUD

**User Story:** As a CSE examinee, I want to create flashcards of various types, so that I can build personalized study materials for different kinds of knowledge.

#### Acceptance Criteria

1. WHEN a user submits a valid flashcard creation request, THE Flashcard_Service SHALL create a Flashcard record with fields: front (1–1000 characters), back (1–2000 characters), card_type, hints (array of 0–5 strings, each max 200 characters), tags (array of 0–10 strings, each max 50 characters), and associate it with the specified Deck
2. THE Flashcard_Service SHALL support these Card_Type values: basic, reverse, cloze, mcq, true_false, matching, sequence
3. WHEN a flashcard of type "cloze" is created, THE Flashcard_Service SHALL validate that the front field contains at least one cloze deletion marker in the format `{{c1::answer::hint}}`
4. WHEN a flashcard of type "mcq" is created, THE Flashcard_Service SHALL validate that the back field contains a JSON object with "choices" (array of 3–6 strings) and "answer" (string matching one choice)
5. WHEN a flashcard of type "matching" is created, THE Flashcard_Service SHALL validate that the back field contains a JSON object with "pairs" (array of {left, right} objects, minimum 3 pairs, maximum 20 pairs)
6. WHEN a flashcard of type "sequence" is created, THE Flashcard_Service SHALL validate that the back field contains a JSON array of ordered items (minimum 3 items, maximum 20 items)
7. WHEN a user updates a flashcard, THE Flashcard_Service SHALL preserve the existing scheduling metadata (ease_factor, interval, retention_score, memory_stability) and re-validate the updated fields against the card's type-specific rules
8. WHEN a user deletes a flashcard, THE Flashcard_Service SHALL soft-delete the record by setting a deleted_at timestamp
9. THE Flashcard_Service SHALL enforce a maximum of 500 flashcards per deck
10. IF a flashcard creation or update request fails type-specific validation (criteria 3–6) or field constraints (criterion 1), THEN THE Flashcard_Service SHALL reject the request and return an error response indicating which field failed validation and why
11. IF a user attempts to create a flashcard in a deck that already contains 500 flashcards, THEN THE Flashcard_Service SHALL reject the request and return an error response indicating the deck has reached its maximum card capacity
12. WHEN a flashcard of type "basic", "reverse", or "true_false" is created, THE Flashcard_Service SHALL validate that both front and back fields are non-empty strings within the defined length constraints

### Requirement 2: Deck Management

**User Story:** As a CSE examinee, I want to organize my flashcards into decks with metadata, so that I can manage study materials by topic and share them with others.

#### Acceptance Criteria

1. WHEN a user creates a deck, THE Flashcard_Service SHALL store: title, description, tags, category (verbal, numerical, analytical), visibility (private, public, unlisted), and owner_id
2. THE Flashcard_Service SHALL enforce unique deck titles per user
3. WHEN a user sets deck visibility to "public", THE Flashcard_Service SHALL make the deck discoverable in the Marketplace
4. WHEN a user bookmarks a deck, THE Flashcard_Service SHALL create a bookmark record linking the user to the deck
5. WHEN a user duplicates a deck, THE Flashcard_Service SHALL create a full copy of the deck and all its flashcards under the requesting user's ownership, with a "Copied from" attribution field
6. WHEN a user deletes a deck, THE Flashcard_Service SHALL soft-delete the deck and all associated flashcards
7. THE Flashcard_Service SHALL support deck tagging with CSE-relevant tags (e.g., grammar, vocabulary, ratio, logic)
8. WHEN a user requests their decks, THE Flashcard_Service SHALL return paginated results with filtering by category, tags, and visibility

### Requirement 3: Study Modes

**User Story:** As a CSE examinee, I want multiple study modes for reviewing flashcards, so that I can choose the interaction style that best fits my learning preference and available time.

#### Acceptance Criteria

1. WHEN a user starts a study session in "swipe" mode, THE Flashcard_Service SHALL present cards one at a time and accept directional input: left (forgot), right (remembered), up (bookmark), down (skip)
2. WHEN a user starts a study session in "typing" mode, THE Flashcard_Service SHALL require the user to type the answer and validate it against the back field using case-insensitive comparison with configurable strictness (exact, contains, fuzzy)
3. WHEN a user starts a study session in "rapid_recall" mode, THE Flashcard_Service SHALL present cards with a configurable per-card time limit (default 5 seconds) and auto-advance on timeout
4. WHEN a user starts a study session in "quiz" mode, THE Flashcard_Service SHALL present cards as multiple-choice questions by generating distractors from other cards in the same deck
5. WHEN a user starts a study session in "timed" mode, THE Flashcard_Service SHALL enforce a total session time limit and track cards completed within that window
6. WHEN a user starts a study session in "exam_simulation" mode, THE Flashcard_Service SHALL present a fixed number of cards (configurable, default 50) with a total time limit, no answer reveals until completion, and a final score summary
7. WHEN a study session completes, THE Flashcard_Service SHALL record the session results: cards_reviewed, cards_correct, cards_incorrect, cards_skipped, duration_seconds, and study_mode

### Requirement 4: Swipe UI Interaction

**User Story:** As a CSE examinee using the mobile PWA, I want a swipe-based card interface with Framer Motion animations, so that reviewing flashcards feels fast and intuitive on touch devices.

#### Acceptance Criteria

1. WHEN a user swipes a card left, THE Flashcard_Service SHALL record the response as "forgot" and schedule the card for earlier re-review
2. WHEN a user swipes a card right, THE Flashcard_Service SHALL record the response as "remembered" and advance the card's review interval
3. WHEN a user swipes a card up, THE Flashcard_Service SHALL toggle the bookmark status on that card
4. WHEN a user swipes a card down, THE Flashcard_Service SHALL record the response as "skipped" and move to the next card without affecting scheduling
5. THE Flashcard_Service SHALL accept swipe responses via a POST endpoint that receives card_id, response_type (forgot, remembered, bookmarked, skipped), and optional confidence_level
6. WHEN a swipe response is recorded, THE Flashcard_Service SHALL return the updated card scheduling metadata in the response body

---

## Phase 2: Spaced Repetition & Review

### Requirement 5: FSRS-Inspired Spaced Repetition Algorithm

**User Story:** As a CSE examinee, I want an evidence-based spaced repetition algorithm to schedule my reviews, so that I retain information efficiently with minimal review sessions.

#### Acceptance Criteria

1. THE FSRS_Engine SHALL maintain per-card parameters: ease_factor (float, default 2.5), retention_score (float, 0.0–1.0), memory_stability (float, days, default 1.0, minimum 0.1), review_interval (integer, days, default 1, range 1–365), lapse_count (integer, default 0), and mastery_percentage (float, 0.0–100.0, default 0.0)
2. WHEN a user responds "remembered" with confidence "mastered", THE FSRS_Engine SHALL multiply the review_interval by the ease_factor, increase memory_stability by 10%, and clamp the resulting review_interval to a maximum of 365 days
3. WHEN a user responds "remembered" with confidence "confident", THE FSRS_Engine SHALL multiply the review_interval by (ease_factor × 0.85) and leave memory_stability unchanged
4. WHEN a user responds "remembered" with confidence "unsure", THE FSRS_Engine SHALL set the review_interval to max(1, floor(current_interval × 0.5)) and decrease memory_stability by 10%
5. WHEN a user responds "forgot", THE FSRS_Engine SHALL reset the review_interval to 1 day, increment lapse_count, decrease ease_factor by 0.2 (minimum 1.3), and reduce memory_stability by 30%
6. THE FSRS_Engine SHALL compute retention_score using the formula: retention_score = e^(−elapsed_days / memory_stability), where elapsed_days is the number of days since the card's last review date
7. THE FSRS_Engine SHALL compute mastery_percentage based on: (successful_reviews / total_reviews) × retention_score × 100, capped at 100.0, where successful_reviews is the count of reviews with response "remembered" (any confidence level) and total_reviews is the count of all reviews excluding "skipped"
8. WHEN ease_factor is adjusted, THE FSRS_Engine SHALL clamp it between 1.3 and 3.5
9. IF memory_stability would be reduced below 0.1 by any operation, THEN THE FSRS_Engine SHALL clamp memory_stability to 0.1
10. THE FSRS_Engine SHALL produce deterministic outputs: given identical card state and user response, the computed review_interval, ease_factor, memory_stability, and retention_score SHALL be identical across invocations
11. FOR ALL valid card states (parameters within their defined ranges), computing the next interval then simulating a review at that interval SHALL produce a retention_score within the target range of 0.85–0.95 (round-trip scheduling property)

### Requirement 6: Daily Review Queue

**User Story:** As a CSE examinee, I want a prioritized daily review queue, so that I focus on the cards most at risk of being forgotten.

#### Acceptance Criteria

1. WHEN a user requests their daily review queue, THE Flashcard_Service SHALL return cards ordered by priority: (1) overdue cards where next_review_date < today, sorted by days overdue descending, (2) cards due today where next_review_date = today, sorted by retention_score ascending, (3) cards not yet due but with retention_score < 0.7, sorted by retention_score ascending
2. THE Flashcard_Service SHALL include cards from all of the user's decks in the review queue unless the user filters by specific deck(s)
3. IF a card's next_review_date is earlier than or equal to today, THEN THE Flashcard_Service SHALL include it in the review queue
4. THE Flashcard_Service SHALL cap the daily review queue at a user-configurable maximum (default 50, range 10–200) by truncating the lowest-priority cards from the end of the sorted list
5. WHEN the review queue is exhausted, THE Flashcard_Service SHALL offer up to 20 bonus review cards from the user's weakest topics (lowest average retention_score by tag), excluding cards already reviewed in the current session
6. THE Flashcard_Service SHALL provide a queue summary endpoint returning: total_due (cards with next_review_date ≤ today), overdue_count (cards with next_review_date < today), new_today_count (cards with next_review_date = today that have never been reviewed), and estimated_review_minutes (total_due × 8 seconds, converted to minutes and rounded up to the nearest integer)
7. IF the user has no cards due for review and no weak cards, THEN THE Flashcard_Service SHALL return an empty queue list with all summary counts set to 0

### Requirement 7: Memory Retention Analytics

**User Story:** As a CSE examinee, I want to visualize my memory retention over time, so that I can identify weak areas and track improvement.

#### Acceptance Criteria

1. WHEN a user requests retention analytics, THE Flashcard_Service SHALL return per-tag retention averages computed as the mean retention_score of all cards with that tag
2. THE Flashcard_Service SHALL provide a forgetting curve endpoint that returns predicted retention_score values at day 1, 3, 7, 14, 30 for a given card or tag group
3. THE Flashcard_Service SHALL provide a retention heatmap endpoint returning daily review counts and average retention_score for the past 90 days
4. THE Flashcard_Service SHALL provide mastery graph data showing mastery_percentage progression over time per deck or tag, sampled at weekly intervals
5. WHEN retention analytics are requested with a date range, THE Flashcard_Service SHALL filter results to that range

### Requirement 8: Active Recall Enforcement

**User Story:** As a CSE examinee, I want the system to enforce active recall techniques, so that I build stronger memories through effortful retrieval rather than passive recognition.

#### Acceptance Criteria

1. WHEN a study session uses "typing" mode, THE Flashcard_Service SHALL require the user to type the answer before revealing the correct response
2. WHEN a study session uses "swipe" mode, THE Flashcard_Service SHALL require the user to submit a Confidence_Level (guessed, unsure, confident, mastered) before advancing to the next card
3. THE Flashcard_Service SHALL support a "delayed reveal" setting where the answer is hidden for a configurable duration (default 3 seconds) after the user indicates readiness
4. WHEN a user submits a typed answer, THE Flashcard_Service SHALL compare it against the correct answer and return: is_correct (boolean), similarity_score (0.0–1.0 using Levenshtein distance ratio), and the correct_answer

### Requirement 9: Interleaving System

**User Story:** As a CSE examinee, I want my review sessions to mix cards across different CSE ability areas, so that I develop the ability to context-switch between verbal, numerical, and analytical reasoning as required in the actual exam.

#### Acceptance Criteria

1. WHEN interleaving is enabled for a study session, THE Flashcard_Service SHALL mix cards from different categories (verbal, numerical, analytical) in a ratio proportional to the user's deck composition
2. THE Flashcard_Service SHALL prevent more than 3 consecutive cards from the same category when interleaving is active
3. WHEN a user enables interleaving, THE Flashcard_Service SHALL select cards from the review queue across all categories rather than processing one category at a time
4. THE Flashcard_Service SHALL allow users to toggle interleaving on or off per study session via a request parameter

### Requirement 10: Confidence Tracking

**User Story:** As a CSE examinee, I want to rate my confidence on each card recall, so that the system can distinguish between lucky guesses and genuine mastery.

#### Acceptance Criteria

1. WHEN a user reviews a card, THE Flashcard_Service SHALL accept a Confidence_Level value: guessed, unsure, confident, or mastered
2. THE FSRS_Engine SHALL weight the confidence level when computing the next review interval (guessed → interval × 0.3, unsure → interval × 0.5, confident → interval × 0.85, mastered → interval × 1.0 of the base calculation)
3. THE Flashcard_Service SHALL store confidence history per card as an array of {timestamp, confidence_level} records
4. WHEN a user requests card statistics, THE Flashcard_Service SHALL return the confidence distribution (count per level) and the trend (improving, stable, declining) based on the last 10 reviews
5. WHEN a card receives 5 consecutive "mastered" confidence ratings, THE Flashcard_Service SHALL mark the card as "graduated" and set its review_interval to the maximum (90 days)

---

## Phase 3: Pseudo-AI System

### Requirement 11: Pseudo-AI Flashcard Generator

**User Story:** As a CSE examinee, I want the system to automatically generate flashcards from lesson content using deterministic NLP, so that I can quickly build study decks without manually creating each card.

#### Acceptance Criteria

1. WHEN a user requests flashcard generation from a lesson, THE Pseudo_AI_Generator SHALL extract key terms and definitions using regex patterns matching "Term: Definition", "Term — Definition", bold markdown patterns (`**term**`), and italic markdown patterns (`*term*`) followed by a definition sentence, and SHALL extract terms from markdown table rows where the first column contains the term and subsequent columns contain the definition
2. WHEN generating cloze deletion cards, THE Pseudo_AI_Generator SHALL identify sentences containing extracted key terms, replace the term with a cloze marker in the format `{{c1::term::hint}}`, and use the original sentence as the front field
3. WHEN generating MCQ cards, THE Pseudo_AI_Generator SHALL use the correct definition as the answer and select 3 distractors from other definitions in the same lesson; IF fewer than 3 other definitions exist in the lesson, THEN THE Pseudo_AI_Generator SHALL draw distractors from other lessons within the same topic category
4. THE Pseudo_AI_Generator SHALL classify generated card difficulty using these thresholds: easy (term appears in the top 5000 English word frequency list AND definition contains 1 clause of 15 words or fewer), medium (term is NOT in the top 5000 frequency list OR definition contains 2–3 clauses), hard (term is not in the top 10000 frequency list AND definition contains more than 3 clauses or requires cross-referencing other terms)
5. THE Pseudo_AI_Generator SHALL generate at most 1 mnemonic suggestion per card for terms classified as medium or hard difficulty, selecting the best-fit pattern from: acronym (first letters of definition keywords), association chain (linking term to a common word), or rhyming pattern (from the predefined template library)
6. THE Pseudo_AI_Generator SHALL use no paid LLM APIs — all generation relies on regex, heuristics, templates, word frequency lists, and deterministic NLP rules
7. WHEN generation completes, THE Pseudo_AI_Generator SHALL return a preview containing all generated cards with their front field, back field, card_type, difficulty classification, and optional mnemonic, for user review before saving to a deck
8. THE Pseudo_AI_Generator SHALL produce between 10 and 50 cards per lesson, configurable by the user via a requested_card_count parameter (default 25); the distribution SHALL target approximately 40% basic definition cards, 35% cloze deletion cards, and 25% MCQ cards
9. IF the lesson content yields fewer extractable terms than the configured minimum of 10, THEN THE Pseudo_AI_Generator SHALL return an error indication stating the lesson has insufficient structured content, along with the count of terms that were successfully extracted
10. THE Pseudo_AI_Generator SHALL produce cards where the answer field is non-empty, contains at least 2 characters, and the front field differs from the back field after trimming whitespace

### Requirement 12: Pseudo-AI Recommendation Engine

**User Story:** As a CSE examinee, I want personalized study recommendations based on my performance data, so that I focus on the areas where I need the most improvement.

#### Acceptance Criteria

1. WHEN a user requests recommendations, THE Pseudo_AI_Generator SHALL identify the user's 5 weakest subtopics by computing average retention_score per tag and selecting the lowest
2. THE Pseudo_AI_Generator SHALL recommend public decks from the Marketplace that cover the user's weak subtopics, ranked by deck rating and relevance
3. THE Pseudo_AI_Generator SHALL compute ideal review intervals per user by analyzing their historical retention decay rate and recommending a personalized daily review count
4. THE Pseudo_AI_Generator SHALL generate targeted quiz suggestions by selecting cards with retention_score below 0.6 and grouping them into mini-quizzes of 10–20 cards
5. WHEN a user has no review history, THE Pseudo_AI_Generator SHALL recommend starter decks based on the user's selected exam category (Professional or Sub-Professional)

### Requirement 13: Pseudo-AI Explanation Engine

**User Story:** As a CSE examinee, I want contextual explanations when I get a card wrong, so that I understand the concept rather than just memorizing the answer.

#### Acceptance Criteria

1. WHEN a user answers a card incorrectly, THE Pseudo_AI_Generator SHALL return an explanation by matching the card's tags to a template library of concept explanations
2. THE Pseudo_AI_Generator SHALL reference the relevant lesson section by matching card tags to lesson subtopic slugs and returning a deep link to the lesson
3. THE Pseudo_AI_Generator SHALL provide rule-based educational mappings: for grammar cards → grammar rule templates, for vocabulary cards → etymology and usage templates, for numerical cards → formula and worked-example templates, for analytical cards → logic rule templates
4. WHEN no template matches a card's tags, THE Pseudo_AI_Generator SHALL return the card's stored explanation field as a fallback
5. THE Pseudo_AI_Generator SHALL use no paid LLM APIs for explanation generation — all explanations come from pre-authored templates and lesson content references

---

## Phase 4: Social & Community

### Requirement 14: Public Flashcard Marketplace

**User Story:** As a CSE examinee, I want to browse and use flashcard decks created by other users, so that I can benefit from community-created study materials.

#### Acceptance Criteria

1. WHEN a deck's visibility is set to "public", THE Marketplace SHALL make it discoverable via search and browse endpoints within the same request-response cycle (no eventual consistency delay)
2. THE Marketplace SHALL support searching decks by title, description, tags, and category with full-text matching, requiring a minimum query length of 2 characters
3. THE Marketplace SHALL support sorting results by: newest, highest_rated, most_cloned, most_bookmarked
4. WHEN a user rates a deck, THE Marketplace SHALL accept an integer rating from 1 to 5 inclusive, enforce one rating per user per deck, and compute the deck's average_rating as the arithmetic mean of all ratings rounded to 2 decimal places
5. IF a user submits a rating for a deck they have already rated, THEN THE Marketplace SHALL update the existing rating with the new value and recompute the deck's average_rating
6. WHEN a user clones a public deck, THE Marketplace SHALL create a full copy of the deck metadata (title, description, tags, category) and all associated flashcard content (front, back, card_type, hints, tags) under the user's ownership, excluding scheduling metadata, with an attribution field referencing the original deck_id and creator_id
7. THE Marketplace SHALL return paginated results using PaginatedResponse with filtering by category (verbal, numerical, analytical), minimum rating (1–5), and card count range (min_cards and max_cards as non-negative integers)
8. WHEN a deck is cloned, THE Marketplace SHALL increment the original deck's clone_count by 1
9. IF a user attempts to rate their own deck, THEN THE Marketplace SHALL reject the request with an error indicating that self-rating is not permitted

### Requirement 15: Creator Profiles

**User Story:** As a deck creator, I want a public profile showing my contributions and expertise, so that other users can discover and trust my study materials.

#### Acceptance Criteria

1. THE Creator_Profile SHALL display: username, total_xp, follower_count, published_deck_count, total_cards_created, and average_deck_rating
2. THE Creator_Profile SHALL list all public decks by the creator with their ratings and clone counts
3. THE Creator_Profile SHALL display mastery statistics: top 3 strongest categories and overall mastery_percentage
4. WHEN a user has published at least 1 public deck, THE Flashcard_Service SHALL make their Creator_Profile accessible via a public endpoint
5. THE Creator_Profile SHALL be accessible without authentication (public read)

### Requirement 16: Follow System

**User Story:** As a CSE examinee, I want to follow deck creators whose materials I find valuable, so that I receive updates when they publish new decks.

#### Acceptance Criteria

1. WHEN a user follows a creator, THE Flashcard_Service SHALL create a follow relationship record (follower_id, followed_id, created_at)
2. WHEN a user unfollows a creator, THE Flashcard_Service SHALL delete the follow relationship record
3. WHEN a followed creator publishes a new public deck, THE Flashcard_Service SHALL create a notification record for each follower
4. THE Flashcard_Service SHALL prevent a user from following themselves
5. THE Flashcard_Service SHALL return a user's follower_count and following_count on their profile
6. WHEN a user requests their feed, THE Flashcard_Service SHALL return recent public decks from followed creators, ordered by publish date descending, paginated

### Requirement 17: Comments & Discussions

**User Story:** As a CSE examinee, I want to comment on public decks to share study tips and ask questions, so that the community can collaborate on improving study materials.

#### Acceptance Criteria

1. WHEN a user posts a comment on a public deck, THE Flashcard_Service SHALL create a comment record with: user_id, deck_id, body, parent_comment_id (null for top-level), created_at
2. THE Flashcard_Service SHALL support threaded replies by allowing comments with a non-null parent_comment_id (maximum nesting depth: 2 levels)
3. THE Flashcard_Service SHALL return comments in chronological order with nested replies included
4. WHEN a user deletes their own comment, THE Flashcard_Service SHALL soft-delete it and display "[deleted]" in place of the body
5. THE Flashcard_Service SHALL enforce a maximum comment length of 1000 characters
6. THE Flashcard_Service SHALL return paginated comments (default 20 per page) for a given deck
7. WHEN a comment contains prohibited content (flagged by keyword filter), THE Flashcard_Service SHALL hold it for moderation review instead of publishing immediately

---

## Phase 5: Gamification & Integration

### Requirement 18: XP Integration

**User Story:** As a CSE examinee, I want to earn XP from flashcard activities, so that my flashcard study contributes to my overall platform progression.

#### Acceptance Criteria

1. WHEN a user ends a flashcard review session (by reviewing all cards in the session queue or explicitly stopping the session), THE Flashcard_Service SHALL call XP_Service.award() with source "flashcard_review", amount computed as (2 XP × cards_reviewed) + (1 XP × cards_marked_remembered), and a client_event_id of format "flashcard_review:{user_id}:{session_id}"
2. WHEN a user adds the 10th card to a newly created deck (within the same creation flow or subsequent edits before any XP was awarded for that deck), THE Flashcard_Service SHALL call XP_Service.award() with source "deck_created", amount 25, and client_event_id "deck_created:{user_id}:{deck_id}"
3. WHEN a user's deck is cloned by another user, THE Flashcard_Service SHALL call XP_Service.award() with source "deck_cloned", amount 10, user set to the original deck creator, and client_event_id "deck_cloned:{deck_id}:{cloner_user_id}"
4. WHEN a user reviews every card in their daily review queue (total_due reaches 0 for that day), THE Flashcard_Service SHALL call XP_Service.award() with source "daily_review_complete", amount 15, and client_event_id "daily_review_complete:{user_id}:{date_iso}"
5. WHEN computing any flashcard XP award, THE Flashcard_Service SHALL call XPMultiplierService.apply_multiplier(user_id, base_amount) and pass the returned value as the amount to XP_Service.award()
6. IF XP_Service.award() returns an existing event for the same client_event_id (idempotent replay), THEN THE Flashcard_Service SHALL treat the operation as successful without awarding duplicate XP
7. IF XP_Service.award() raises an exception, THEN THE Flashcard_Service SHALL still persist the flashcard session results and log the failure, allowing the XP award to be retried on the next sync

### Requirement 19: Achievement Integration

**User Story:** As a CSE examinee, I want to unlock flashcard-specific achievements, so that I have milestones to work toward in my flashcard study journey.

#### Acceptance Criteria

1. WHEN a user reviews 100 flashcards total, THE Flashcard_Service SHALL trigger achievement check for "Recall Rookie" badge
2. WHEN a user reviews 1000 flashcards total, THE Flashcard_Service SHALL trigger achievement check for "Flashcard Master" badge
3. WHEN a user maintains a 7-day consecutive review streak, THE Flashcard_Service SHALL trigger achievement check for "Week Warrior" badge
4. WHEN a user maintains a 30-day consecutive review streak, THE Flashcard_Service SHALL trigger achievement check for "Monthly Memorizer" badge
5. WHEN a user achieves 90% mastery on a deck (average mastery_percentage across all cards ≥ 90), THE Flashcard_Service SHALL trigger achievement check for "Deck Dominator" badge
6. WHEN a user publishes 5 public decks, THE Flashcard_Service SHALL trigger achievement check for "Community Contributor" badge
7. THE Flashcard_Service SHALL integrate with the existing achievement system by calling the achievement check service after qualifying events

### Requirement 20: Leaderboard Integration

**User Story:** As a CSE examinee, I want flashcard activity reflected in leaderboards, so that I can compete with other users on review consistency and mastery.

#### Acceptance Criteria

1. THE Flashcard_Service SHALL expose a "flashcard_review_streak" metric to the existing leaderboard system representing consecutive days with at least 1 completed review
2. THE Flashcard_Service SHALL expose a "total_cards_mastered" metric representing cards with mastery_percentage ≥ 90
3. THE Flashcard_Service SHALL expose a "deck_popularity_score" metric for creators, computed as: (clone_count × 3) + (bookmark_count × 2) + (average_rating × 10)
4. WHEN the leaderboard service requests flashcard metrics, THE Flashcard_Service SHALL return the computed values for the specified user_id or for all users (for ranking)

### Requirement 21: Focus Mode Integration

**User Story:** As a CSE examinee, I want to use flashcard study sessions within focus mode, so that my flashcard time counts toward my focus tracking and wellness checks.

#### Acceptance Criteria

1. WHEN a user starts a flashcard study session with focus_mode enabled, THE Flashcard_Service SHALL call the existing FocusService.start_session() with activity_type "flashcard_review"
2. WHEN a flashcard study session with focus_mode completes, THE Flashcard_Service SHALL call FocusService.complete_session() with the actual duration
3. WHEN a focus-mode flashcard session exceeds the wellness threshold (configurable, default 90 minutes), THE Flashcard_Service SHALL return a wellness reminder in the response
4. THE Flashcard_Service SHALL include focus_session_id in the study session response when focus_mode is active, allowing the frontend to display focus stats

### Requirement 22: Exam Simulation Mode

**User Story:** As a CSE examinee, I want to convert my flashcard decks into timed exam simulations, so that I can practice under exam-like conditions.

#### Acceptance Criteria

1. WHEN a user starts an exam simulation, THE Flashcard_Service SHALL accept parameters: deck_ids (1 to 10), question_count (minimum 10, default 50, maximum 150), time_limit_minutes (minimum 10, default 180, maximum 300), and category_distribution (optional percentages for verbal, numerical, analytical that must sum to exactly 100)
2. IF the specified decks contain fewer cards than the requested question_count, THEN THE Flashcard_Service SHALL reject the request with an error message indicating the available card count and the requested count
3. IF category_distribution is provided and a specified category has fewer available cards than its proportional share, THEN THE Flashcard_Service SHALL reject the request with an error message indicating which category has insufficient cards
4. THE Flashcard_Service SHALL select cards randomly from the specified decks, respecting the category_distribution if provided
5. WHILE an exam simulation is in progress, THE Flashcard_Service SHALL track elapsed time and lock each individual card answer upon per-card submission, preventing changes to that card's response
6. WHEN the time limit expires, THE Flashcard_Service SHALL auto-submit all unanswered cards as "skipped" and end the simulation
7. WHEN an exam simulation completes, THE Flashcard_Service SHALL return: total_score (percentage, 0.0–100.0), score_per_category (percentage per category), time_taken (in seconds), cards_correct, cards_incorrect, cards_skipped, and percentile_estimate (0–100, based on all historical exam simulation scores from all users for the same category_distribution)
8. IF fewer than 10 historical exam simulation scores exist for percentile computation, THEN THE Flashcard_Service SHALL return percentile_estimate as null
9. THE Flashcard_Service SHALL store exam simulation results for historical comparison and progress tracking

---

## Phase 6: Offline & Performance

### Requirement 23: IndexedDB Offline Storage

**User Story:** As a CSE examinee with unreliable internet, I want my flashcard decks and review progress stored locally, so that I can study without an internet connection.

#### Acceptance Criteria

1. WHEN a user downloads a deck for offline use, THE Sync_Engine SHALL store the complete deck data (metadata + all flashcards + scheduling state) in IndexedDB
2. THE Sync_Engine SHALL store pending review responses in IndexedDB when the device is offline
3. THE Sync_Engine SHALL store user progress data (review history, confidence ratings, streak data) in IndexedDB
4. WHEN the user opens the app offline, THE Sync_Engine SHALL serve the daily review queue from locally cached card scheduling data
5. THE Sync_Engine SHALL track a "last_synced_at" timestamp per deck to determine staleness
6. WHEN a deck has not been synced for more than 7 days and the device is online, THE Sync_Engine SHALL display a "stale data" indicator to the user

### Requirement 24: Sync Engine

**User Story:** As a CSE examinee, I want my offline study progress to sync reliably when I reconnect, so that no review data is lost and my progress is consistent across devices.

#### Acceptance Criteria

1. WHEN the device regains connectivity, THE Sync_Engine SHALL initiate upload of all pending review responses to the backend in chronological order within 5 seconds of detecting a stable connection
2. THE Sync_Engine SHALL use optimistic updates: apply changes locally before the next UI render and reconcile with the server asynchronously
3. WHEN a sync conflict occurs (server state differs from local state for the same card), THE Sync_Engine SHALL resolve using "last-write-wins" based on the review timestamp
4. IF a sync request fails, THEN THE Sync_Engine SHALL retry with exponential backoff (1s, 2s, 4s, 8s, max 60s) up to 10 attempts before marking the item as "sync_failed"
5. THE Sync_Engine SHALL batch pending sync items into groups of up to 50 to minimize network requests, sending any remaining items in a final smaller batch
6. WHEN sync completes successfully, THE Sync_Engine SHALL update the local "last_synced_at" timestamp and clear the pending queue
7. THE Sync_Engine SHALL expose sync status to the UI: synced, syncing, pending (count), failed (count)
8. THE Sync_Engine SHALL include a unique client_event_id with each review response so that the backend can deduplicate retried submissions and prevent duplicate review records
9. IF one or more items are in "sync_failed" status, THEN THE Sync_Engine SHALL display the failed count in the sync status and provide a manual "retry sync" action that re-enqueues all failed items for another full retry cycle
10. IF connectivity is lost during an in-progress batch upload, THEN THE Sync_Engine SHALL retain all unacknowledged items in the pending queue and resume from the first unacknowledged item when connectivity returns

### Requirement 25: PWA Offline Support

**User Story:** As a CSE examinee, I want the flashcard feature to work as a fully offline-capable PWA, so that I can install it and study anywhere without depending on connectivity.

#### Acceptance Criteria

1. THE Sync_Engine SHALL register flashcard-related API routes in the service worker's cache strategy (stale-while-revalidate for deck lists, cache-first for downloaded deck content)
2. WHEN the app is offline, THE Sync_Engine SHALL serve cached deck data and allow full study session completion using locally stored cards
3. THE Sync_Engine SHALL use the Background Sync API (where supported) to queue review submissions for automatic upload when connectivity returns
4. WHEN a user marks a deck for offline access, THE Sync_Engine SHALL pre-cache all card assets and scheduling data during the next online window
5. THE Sync_Engine SHALL limit offline storage to 50 MB per user, displaying a warning at 80% capacity

---

## Phase 7: Analytics & Admin

### Requirement 26: User Analytics Dashboard

**User Story:** As a CSE examinee, I want a personal analytics dashboard showing my flashcard study patterns and progress, so that I can make data-driven decisions about my study strategy.

#### Acceptance Criteria

1. THE Flashcard_Service SHALL provide an endpoint returning the user's overall retention percentage (mean retention_score across all active cards)
2. THE Flashcard_Service SHALL provide current and longest review streak (consecutive days with at least 1 review)
3. THE Flashcard_Service SHALL provide strongest and weakest subjects computed as the top 3 and bottom 3 tags by average retention_score
4. THE Flashcard_Service SHALL provide a mastery heatmap: a 90-day grid showing daily review activity intensity (0=none, 1=light, 2=moderate, 3=heavy based on cards reviewed)
5. THE Flashcard_Service SHALL provide study time analytics: total_minutes_studied, average_session_duration, cards_per_minute average
6. THE Flashcard_Service SHALL provide a "predicted exam readiness" score computed as: weighted average of mastery_percentage across all categories, weighted by CSE exam distribution (40% verbal, 30% numerical, 30% analytical)

### Requirement 27: Admin Analytics

**User Story:** As a platform administrator, I want analytics on flashcard usage across all users, so that I can identify content gaps, problematic cards, and engagement trends.

#### Acceptance Criteria

1. WHEN an admin requests flashcard analytics, THE Flashcard_Service SHALL return the top 20 most-failed cards (highest lapse_count across all users) with their deck and tag information
2. THE Flashcard_Service SHALL return the top 20 most-failed decks (lowest average retention_score across users who studied them)
3. THE Flashcard_Service SHALL return engagement metrics: daily_active_reviewers, average_cards_per_session, total_reviews_today, new_decks_created_today
4. THE Flashcard_Service SHALL return category breakdown: percentage of cards and reviews per category (verbal, numerical, analytical)
5. THE Flashcard_Service SHALL restrict admin analytics endpoints to users with the "admin" role using the existing RBAC middleware
6. THE Flashcard_Service SHALL return trending decks: public decks with the highest clone + bookmark growth in the past 7 days

### Requirement 28: Moderation System

**User Story:** As a platform administrator, I want to moderate public flashcard content, so that the marketplace remains high-quality and free of inappropriate material.

#### Acceptance Criteria

1. WHEN an admin flags a public deck for removal, THE Flashcard_Service SHALL set the deck's visibility to "removed" and remove it from marketplace search results
2. WHEN an admin bans a comment, THE Flashcard_Service SHALL soft-delete the comment and create an audit log entry with the admin_id, action, and reason
3. THE Flashcard_Service SHALL support a "featured" flag on decks that admins can toggle to promote high-quality community decks in marketplace results
4. WHEN an admin features a deck, THE Flashcard_Service SHALL display it in a "Featured Decks" section at the top of marketplace browse results
5. THE Flashcard_Service SHALL provide a moderation queue endpoint listing: reported decks, flagged comments, and decks pending review (sorted by report count descending)
6. WHEN a deck receives 3 or more user reports, THE Flashcard_Service SHALL automatically add it to the moderation queue
7. THE Flashcard_Service SHALL log all moderation actions to the existing audit system (AuditService) with action_type, target_id, target_type, and admin_id

---

## Cross-Cutting Requirements

### Requirement 29: Authentication & Authorization

**User Story:** As a platform user, I want flashcard endpoints to respect the existing auth system, so that my data is secure and only I can modify my own decks.

#### Acceptance Criteria

1. THE Flashcard_Service SHALL require a valid JWT token for all endpoints except: public deck browsing, public creator profiles, and public deck detail views
2. THE Flashcard_Service SHALL enforce ownership checks: only the deck owner can update, delete, or change visibility of their decks
3. WHEN an unauthenticated user attempts to access a protected endpoint, THE Flashcard_Service SHALL return HTTP 401 with the standard ErrorResponse format
4. WHEN an authenticated user attempts to modify another user's deck, THE Flashcard_Service SHALL return HTTP 403 with the standard ErrorResponse format
5. THE Flashcard_Service SHALL integrate with the existing `get_current_user` dependency from `app/common/deps.py`

### Requirement 30: API Conventions & Architecture

**User Story:** As a developer, I want the flashcard feature to follow existing CSNexus conventions, so that the codebase remains consistent and maintainable.

#### Acceptance Criteria

1. THE Flashcard_Service SHALL follow the feature-sliced architecture: models.py, schemas.py, repository.py, service.py, router.py under `app/features/flashcards/`
2. THE Flashcard_Service SHALL use the existing pagination pattern (PaginationParams, PaginatedResponse) for all list endpoints
3. THE Flashcard_Service SHALL use the existing error response format (ErrorResponse with message and code fields) for all error cases
4. THE Flashcard_Service SHALL support both SQLite (development) and PostgreSQL (production) without database-specific SQL
5. THE Flashcard_Service SHALL place algorithm modules (FSRS, generator, recommendation) under `app/features/flashcards/algorithms/`
6. THE Flashcard_Service SHALL use Pydantic 2.x schemas with `model_config = {"from_attributes": True}` for ORM serialization
7. THE Flashcard_Service SHALL use absolute imports from the app root (no relative imports)
8. THE Flashcard_Service SHALL include created_at and updated_at timestamps with server-side defaults on all database models
