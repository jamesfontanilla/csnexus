# Implementation Plan: Intelligent Learning Engine

## Overview

This plan implements fourteen interconnected learning intelligence capabilities across CSNexus, organized into seven core phases (Readiness Score, Smart Daily Queue, Inline Explanations, Post-Mock Exam Analytics, Competence-Based Gamification, Exam Date Onboarding, Readiness Self-Assessment Calibration) and seven research-backed learning technique extensions (Pretesting, Elaborative Interrogation, Generation Effect/Recall Mode, Sleep-Aware Review, Metacognitive Reflection, Concrete Examples, Productive Failure). The implementation follows the feature-sliced architecture with algorithm isolation, building four new feature slices and extending two existing ones.

## Tasks

- [ ] 1. Set up project structure and core data models
  - [ ] 1.1 Create Readiness feature slice directory structure and SQLAlchemy models
    - Create `app/features/readiness/` with `__init__.py`, `models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, and `algorithms/__init__.py`, `algorithms/scorer.py`
    - Implement `ReadinessScoreHistory` model with all fields (user_id, score, component values, weights_used, computed_at)
    - Add composite index on (user_id, computed_at)
    - _Requirements: 2.2_

  - [ ] 1.2 Create Smart Queue feature slice directory structure and SQLAlchemy models
    - Create `app/features/smart_queue/` with full slice structure including `algorithms/generator.py`
    - Implement `DailyQueue` model with unique constraint on (user_id, queue_date)
    - Implement `QueueItem` model with check constraint on item_type and index on (queue_id, position)
    - Implement `QueueItemType` enum
    - _Requirements: 4.5, 5.1_

  - [ ] 1.3 Create Explanations feature slice directory structure and SQLAlchemy models
    - Create `app/features/explanations/` with full slice structure
    - Implement `QuestionExplanation` model with unique index on question_id, cache_version field
    - _Requirements: 7.1_

  - [ ] 1.4 Create Mock Analytics feature slice directory structure and SQLAlchemy models
    - Create `app/features/mock_analytics/` with full slice structure including `algorithms/diagnostics.py` and `algorithms/prediction.py`
    - Implement `DiagnosticReport` model with unique constraint on mock_exam_attempt_id
    - Implement `RecommendationRecord` model with check constraint on recommended_action
    - _Requirements: 10.5, 12.5_

  - [ ] 1.5 Create Gamification extension models (CompetenceMilestone, CompetenceMilestoneAward, StudyConsistency)
    - Add `CompetenceMilestone` model with slug, category, threshold_config
    - Add `CompetenceMilestoneAward` model with unique constraint on (user_id, milestone_id)
    - Add `StudyConsistency` model with unique constraint on user_id
    - _Requirements: 13.5, 14.4_

  - [ ] 1.6 Create Onboarding extension model (OnboardingProfile, StudyPlan) and Self-Assessment model
    - Add `OnboardingProfile` model with check constraints on exam_category and time_budget_minutes
    - Add `StudyPlan` model with target_exam_date, exam_category, available_hours_per_day, total_days, subtopics_per_week, mock_exams_scheduled, plan_data (JSON), estimated_readiness_at_exam
    - Add `SelfAssessmentRecord` model with check constraints on score range and calibration_status, index on (user_id, assessed_at)
    - _Requirements: 16.2, 16.4, 17.4, 19.2_

  - [ ] 1.7 Generate Alembic migration for all new models
    - Create a single migration file covering all new tables
    - Verify migration runs cleanly against test database
    - _Requirements: 1.1, 2.2, 4.5, 7.1, 10.5, 13.5, 14.4, 16.4_

- [ ] 2. Implement Readiness Score algorithms and service
  - [ ] 2.1 Implement pure scoring functions in `app/features/readiness/algorithms/scorer.py`
    - Implement `compute_mastery_component` (weighted average by exam proportion)
    - Implement `compute_retention_component` (FSRS average with subtopic fallback)
    - Implement `compute_mock_component` (recency-weighted average: 1.0/0.7/0.4)
    - Implement `compute_coverage_component` (threshold-meeting subtopic percentage)
    - Implement `compute_readiness_score` (weighted sum, half-up rounding, 0-100 clamping)
    - Implement `redistribute_weights_no_mock` (52.5% mastery, 37.5% retention, 10% coverage)
    - Define `ComponentWeights`, `ReadinessComponents`, `ReadinessResult` dataclasses
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8_

  - [ ]* 2.2 Write property tests for readiness scorer (Properties 1-5)
    - **Property 1: Readiness score is a valid weighted composite**
    - **Property 2: Mastery component is a weighted average by exam proportion**
    - **Property 3: Retention component uses FSRS with subtopic fallback**
    - **Property 4: Mock component applies recency weighting**
    - **Property 5: Coverage component counts threshold-meeting subtopics**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8**

  - [ ] 2.3 Implement Readiness Pydantic schemas
    - Create `ReadinessResponse` (score, components, delta, stale_score flag)
    - Create `DashboardResponse` (score, components, delta, top_impact_subtopics, readiness_level, score_change_summary)
    - Create `TrendResponse` (list of TrendPoint with date and score)
    - _Requirements: 2.3, 3.1, 3.2, 3.3_

  - [ ] 2.4 Implement ReadinessRepository
    - `create(history_record)` — persist new score history entry
    - `get_latest(user_id)` — return most recent score record
    - `get_score_at_date(user_id, date)` — return score for delta calculation
    - `get_trend(user_id, days)` — return score records for past N days
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ] 2.5 Implement ReadinessService orchestrator
    - `compute_and_persist(user_id)` — gather data from mastery/flashcard/mock repos, call scorer, persist result
    - `get_current(user_id)` — return latest score with 7-day delta
    - `get_dashboard(user_id)` — return full dashboard payload with top 3 point-impact subtopics
    - `get_trend(user_id, days=30)` — return 30-day trend with carry-forward
    - `get_readiness_level(score)` — classify into Not Ready/Getting There/Almost Ready/Exam Ready
    - Implement graceful degradation (return stale score on failure)
    - Handle no-activity case (return score 0)
    - _Requirements: 1.1, 1.6, 1.7, 1.8, 1.9, 2.1, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ]* 2.6 Write property tests for trend carry-forward, point-impact ranking, and readiness level (Properties 6-8)
    - **Property 6: Trend carry-forward produces complete 30-day series**
    - **Property 7: Point-impact ranking returns correct top-N subtopics**
    - **Property 8: Readiness level classification matches defined ranges**
    - **Validates: Requirements 2.4, 3.1, 3.2**

  - [ ] 2.7 Implement Readiness router with API endpoints
    - `GET /v1/readiness` — current score + components
    - `GET /v1/readiness/dashboard` — dashboard payload
    - `GET /v1/readiness/trend` — 30-day trend
    - Wire dependency injection via `get_readiness_service` factory
    - _Requirements: 2.3, 3.1, 3.4_

  - [ ]* 2.8 Write unit tests for Readiness feature (repository, service, router layers)
    - Repository tests: get_latest, get_trend, get_score_at_date with real DB
    - Service tests: compute_and_persist happy path, no-activity case, stale fallback, no-mock redistribution
    - Router tests: all 3 endpoints happy path + error cases
    - _Requirements: 1.1, 2.1, 2.3, 2.4, 2.5, 2.6, 3.1, 3.4, 3.5_

- [ ] 3. Checkpoint - Ensure readiness score tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement Smart Daily Queue algorithms and service
  - [ ] 4.1 Implement pure queue generation functions in `app/features/smart_queue/algorithms/generator.py`
    - Define `QueueConfig`, `FlashcardBatch`, `QuizPracticeItem`, `NewContentItem`, `GeneratedQueue` dataclasses
    - Implement `generate_daily_queue` (priority ordering, time budget capping)
    - Implement `generate_exam_crunch_queue` (60/30/10 and 80/20 allocation modes)
    - Implement `compute_difficulty_distribution` (mastery-based percentages)
    - Implement `enforce_variety_constraint` (no more than 2 consecutive same-type)
    - Implement `enforce_cross_module_interleaving` (distribute quiz_practice items across Verbal/Numerical/Analytical modules where possible)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ]* 4.2 Write property tests for queue generator (Properties 9-14, 35)
    - **Property 9: Queue respects priority ordering**
    - **Property 10: Queue total duration never exceeds time budget**
    - **Property 11: Exam crunch mode enforces correct time allocation**
    - **Property 12: Flashcard batch respects size and duration invariants**
    - **Property 13: Difficulty distribution matches mastery score ranges**
    - **Property 14: Queue variety constraint limits consecutive same-type items**
    - **Property 35: Cross-module interleaving distributes quiz items across modules**
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 5.2, 5.3, 5.5, 5.6**

  - [ ] 4.3 Implement Smart Queue Pydantic schemas
    - Create `QueueResponse` (items, total_estimated_seconds, items_remaining, items_completed, time_budget_minutes)
    - Create `QueueItemSchema` (id, position, item_type, payload, estimated_seconds, completed_at)
    - Create `QueuePreferencesSchema` (time_budget_minutes with validation for 15/30/60)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 6.1, 6.4_

  - [ ] 4.4 Implement QueueRepository
    - `get_or_create_for_date(user_id, date)` — idempotent queue retrieval/creation
    - `get_items(queue_id)` — return ordered queue items
    - `mark_item_completed(item_id)` — set completed_at timestamp
    - `delete_queue_for_date(user_id, date)` — for regeneration
    - `get_user_preferences(user_id)` — return time budget preference
    - `update_user_preferences(user_id, time_budget)` — persist preference
    - _Requirements: 4.5, 4.6, 6.1, 6.3_

  - [ ] 4.5 Implement QueueService orchestrator
    - `get_daily_queue(user_id)` — idempotent generation per UTC day, calls generator algorithm
    - `complete_item(user_id, item_id)` — mark completed, update remaining budget
    - `regenerate_queue(user_id)` — force regeneration for today
    - `get_preferences(user_id)` — return current time budget
    - `update_preferences(user_id, time_budget)` — update with conditional regeneration logic
    - Handle no-data case (fill with new content from highest exam weight subtopic)
    - Handle no-flashcards-no-weak case (fill with lowest coverage subtopic)
    - Integrate exam crunch mode based on days_until_exam
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 6.1, 6.2, 6.3, 6.5_

  - [ ] 4.6 Implement Smart Queue router with API endpoints
    - `GET /v1/queue` — get today's daily queue
    - `POST /v1/queue/items/{id}/:complete` — mark item completed
    - `POST /v1/queue/:regenerate` — force regenerate
    - `GET /v1/queue/preferences` — get time budget preference
    - `PATCH /v1/queue/preferences` — update time budget
    - Wire dependency injection via `get_queue_service` factory
    - _Requirements: 4.5, 4.6, 6.1, 6.3, 6.4, 6.5_

  - [ ]* 4.7 Write unit tests for Smart Queue feature (repository, service, router layers)
    - Repository tests: get_or_create_for_date idempotency, mark_item_completed, preferences CRUD
    - Service tests: idempotent generation, exam crunch mode switching, no-data fallback, regeneration logic, preference update with conditional regen
    - Router tests: all 5 endpoints happy path + validation errors (invalid time budget)
    - _Requirements: 4.1, 4.5, 4.6, 4.7, 4.8, 5.5, 6.1, 6.3, 6.5_

- [ ] 5. Checkpoint - Ensure queue engine tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement Inline Question Explanations
  - [ ] 6.1 Implement Explanation Pydantic schemas
    - Create `ExplanationResponse` (explanation_text, key_concept, related_subtopics, cache_version)
    - Create `BulkExplanationRequest` (question_ids with min=1, max=50 validation)
    - Create `BulkExplanationResponse` (list of nullable explanation entries)
    - _Requirements: 7.1, 7.5, 7.7_

  - [ ] 6.2 Implement ExplanationRepository
    - `get_by_question_id(question_id)` — return explanation or None
    - `get_bulk(question_ids)` — return dict of question_id to explanation (None for missing)
    - _Requirements: 7.1, 7.4, 7.5, 7.6_

  - [ ] 6.3 Implement ExplanationService
    - `get_explanation(question_id)` — return explanation or None (never block answer flow)
    - `get_bulk_explanations(question_ids)` — return all with None for missing
    - `escalate_to_tutor(user_id, question_id)` — rate-limit check (20/day), forward to TutorService
    - Track daily escalation count per user
    - _Requirements: 7.2, 7.4, 7.5, 7.6, 8.1, 8.2, 8.3, 8.4_

  - [ ] 6.4 Implement Explanations router with API endpoints
    - `GET /v1/explanations/{question_id}` — get single explanation with ETag/cache_version support
    - `POST /v1/explanations/bulk` — bulk fetch (validate 1-50 IDs)
    - `POST /v1/explanations/{question_id}/:escalate` — AI Tutor escalation
    - Support conditional requests (If-None-Match → 304)
    - Wire dependency injection via `get_explanation_service` factory
    - _Requirements: 7.1, 7.5, 7.7, 8.1, 8.3, 9.2, 9.3_

  - [ ]* 6.5 Write unit tests for Explanations feature (repository, service, router layers)
    - Repository tests: get_by_question_id found/not-found, get_bulk with mixed results
    - Service tests: escalation rate limit (20/day), escalation over limit, bulk with missing IDs
    - Router tests: all 3 endpoints happy path, bulk validation (empty array, >50 IDs → 422), 304 conditional response
    - _Requirements: 7.1, 7.4, 7.5, 7.6, 7.7, 8.3, 8.4, 9.3_

- [ ] 7. Implement Post-Mock Exam Analytics
  - [ ] 7.1 Implement pure diagnostic functions in `app/features/mock_analytics/algorithms/diagnostics.py`
    - Define `SubtopicDiagnostic`, `DiagnosticResult` dataclasses
    - Implement `compute_diagnostic` (per-subtopic breakdown, points lost, time filtering for outliers)
    - Compute highest_impact_areas (top 5 by points_lost)
    - Compute regression_alerts (>15 percentage point decline)
    - Compute difficulty_performance (per-level accuracy)
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 7.2 Implement pure prediction functions in `app/features/mock_analytics/algorithms/prediction.py`
    - Define `PredictedRange`, `ActionableRecommendation` dataclasses
    - Implement `compute_predicted_score` (recency-weighted average, stddev bounds, clamping)
    - Implement `generate_recommendations` (top 5 by estimated_point_gain, action classification)
    - Return None for <2 exams
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 12.1, 12.2, 12.3_

  - [ ]* 7.3 Write property tests for diagnostics (Properties 16-19)
    - **Property 16: Diagnostic total score equals percentage correct**
    - **Property 17: Highest impact areas are top-5 by points lost**
    - **Property 18: Regression alerts fire on >15 percentage point decline**
    - **Property 19: Difficulty performance computes per-level accuracy**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**

  - [ ]* 7.4 Write property tests for prediction and recommendations (Properties 20-22)
    - **Property 20: Predicted score range follows formula with clamping**
    - **Property 21: Confidence level matches exam count ranges**
    - **Property 22: Recommendations are ranked by estimated point gain**
    - **Validates: Requirements 11.1, 11.2, 11.4, 12.1, 12.2, 12.3**

  - [ ] 7.5 Implement Mock Analytics Pydantic schemas
    - Create `DiagnosticResponse` (total_score, subtopic_breakdowns, highest_impact_areas, regression_alerts, difficulty_performance)
    - Create `PredictionResponse` (lower_bound, midpoint, upper_bound, confidence_level)
    - Create `RecommendationResponse` (subtopic_name, current_accuracy, target_accuracy, estimated_point_gain, recommended_action, formatted_string)
    - _Requirements: 10.1, 11.1, 12.1, 12.3_

  - [ ] 7.6 Implement MockAnalyticsRepository
    - `create_report(report)` — persist diagnostic report
    - `get_report(attempt_id)` — retrieve report by mock exam attempt
    - `get_recommendations(report_id)` — retrieve recommendations for a report
    - `accept_recommendation(recommendation_id)` — set accepted_at timestamp
    - `get_historical_accuracy(user_id)` — return per-subtopic historical averages
    - _Requirements: 10.5, 12.4, 12.5_

  - [ ] 7.7 Implement MockAnalyticsService orchestrator
    - `generate_diagnostic(user_id, attempt_id)` — gather answers, compute diagnostic, persist
    - `get_diagnostic(attempt_id)` — retrieve persisted report
    - `get_recommendations(attempt_id)` — compute and return recommendations
    - `accept_recommendation(user_id, recommendation_id)` — mark accepted, feed to QueueEngine
    - `get_predicted_score(user_id)` — compute prediction from mock history
    - _Requirements: 10.1, 10.5, 11.1, 11.3, 12.1, 12.4_

  - [ ] 7.8 Implement Mock Analytics router with API endpoints
    - `GET /v1/mock-analytics/{attempt_id}` — get diagnostic report
    - `GET /v1/mock-analytics/{attempt_id}/recommendations` — get recommendations
    - `POST /v1/mock-analytics/{attempt_id}/recommendations/:accept` — accept recommendation
    - `GET /v1/mock-analytics/prediction` — get predicted score range
    - Wire dependency injection via `get_mock_analytics_service` factory
    - _Requirements: 10.1, 11.1, 12.1, 12.4_

  - [ ]* 7.9 Write unit tests for Mock Analytics feature (repository, service, router layers)
    - Repository tests: create_report, get_report, accept_recommendation
    - Service tests: generate_diagnostic happy path, prediction with <2 exams (returns null), recommendation acceptance feeding queue
    - Router tests: all 4 endpoints happy path + not-found cases
    - _Requirements: 10.1, 10.5, 11.1, 11.3, 12.1, 12.4, 12.5_

- [ ] 8. Checkpoint - Ensure analytics tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement Competence-Based Gamification
  - [ ] 9.1 Implement milestone evaluation logic in gamification extension
    - Create milestone definition seed data (Verbal Mastery, Numerical Mastery, Analytical Mastery, Full Spectrum, Exam Ready: Sub-Professional, Exam Ready: Professional, Comeback, Resilient Learner)
    - Implement `evaluate_mastery_milestones(user_id, mastery_data)` — check all subtopics in category meet threshold
    - Implement `evaluate_readiness_milestones(user_id, score_history)` — check 7 consecutive qualifying days
    - Implement `evaluate_recovery_milestones(user_id, mastery_history)` — check <0.5 to ≥0.8 within 14 days
    - Implement `retroactive_evaluation(user_id)` — evaluate all milestones against existing data on activation
    - Ensure awarded milestones are never revoked
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 15.1_

  - [ ]* 9.2 Write property tests for milestone evaluation (Properties 23-27)
    - **Property 23: Mastery milestone evaluates all subtopics in category**
    - **Property 24: Readiness milestone requires 7 consecutive qualifying days**
    - **Property 25: Recovery milestone detects mastery recovery within 14 days**
    - **Property 26: Awarded milestones are never revoked**
    - **Property 27: Milestone progress percentage matches formula**
    - **Validates: Requirements 13.1, 13.2, 13.3, 13.6, 13.7**

  - [ ] 9.3 Implement Study Consistency tracking
    - Implement `update_consistency(user_id, items_total, items_completed)` — qualify day if ≥50% completed
    - Implement streak reset logic (reset current_streak, preserve longest_streak)
    - Implement catch-up queue adjustment for missed days
    - Implement `replace_streak_with_consistency(user_id)` — migrate from old gamification streak to new Study_Consistency metric, preserving longest_streak
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_

  - [ ]* 9.4 Write property tests for study consistency (Properties 28-29)
    - **Property 28: Study consistency qualifies on ≥50% queue completion**
    - **Property 29: Streak reset preserves longest streak**
    - **Validates: Requirements 14.1, 14.3**

  - [ ] 9.5 Implement Gamification router endpoints
    - `GET /v1/milestones` — return all milestones with status (locked/in_progress/earned)
    - `GET /v1/consistency` — return study consistency metric
    - Wire milestone evaluation into readiness score update flow (triggered after score change)
    - _Requirements: 13.7, 13.8, 14.4_

  - [ ]* 9.6 Write unit tests for Gamification extension (service, router layers)
    - Service tests: milestone evaluation triggers, retroactive evaluation, consistency update, streak reset
    - Router tests: milestones endpoint, consistency endpoint
    - _Requirements: 13.4, 13.7, 13.8, 14.1, 14.3, 15.1_

- [ ] 10. Implement Exam Date Onboarding
  - [ ] 10.1 Implement onboarding validation and plan generation logic
    - Implement exam date validation (1-365 days in future, reject past dates)
    - Implement `generate_study_plan` pure function in `app/features/planner/algorithms/plan_generator.py`: coverage phase → weakness phase → review phase (final 20%)
    - Implement `regenerate_plan_from_today` for exam date updates
    - Implement spaced introduction (max 3 new subtopics/day, review every 3 study days)
    - Implement mock exam scheduling (1/week from week 2, 2/week in final 2 weeks)
    - Skip already-mastered subtopics (mastery_score ≥ 0.8) for returning users
    - Persist generated plan as `StudyPlan` record with plan_data JSON
    - _Requirements: 16.2, 16.3, 16.4, 17.1, 17.2, 17.3, 17.4, 17.5_

  - [ ]* 10.2 Write property tests for onboarding and plan generation (Properties 30-34)
    - **Property 30: Onboarding date validation accepts 1–365 days in future**
    - **Property 31: Study plan follows phase ordering (coverage → weakness → review)**
    - **Property 32: Plan respects spaced introduction limits**
    - **Property 33: Plan schedules mock exams at correct frequency**
    - **Property 34: Plan excludes already-mastered subtopics**
    - **Validates: Requirements 16.2, 17.1, 17.2, 17.3, 17.5**

  - [ ] 10.3 Implement Onboarding Pydantic schemas
    - Create `OnboardingRequest` (exam_date, exam_category, time_budget_minutes with validation)
    - Create `OnboardingResponse` (confirmation, warning for <7 days)
    - Create `PlanSummaryResponse` (total_days, subtopics_per_week, mock_exams_scheduled, estimated_readiness_at_exam)
    - Create `ExamDateUpdateRequest` (exam_date with validation)
    - _Requirements: 16.2, 16.3, 16.6, 17.4_

  - [ ] 10.4 Implement Onboarding repository and service
    - Repository: `create_profile(profile)`, `get_profile(user_id)`, `update_exam_date(user_id, date)`
    - Service: `submit_onboarding(user_id, data)` — validate, create profile, generate plan, create StudyPlan record
    - Service: `update_exam_date(user_id, new_date)` — regenerate plan, recalculate urgency, trigger retention recompute
    - Service: `get_plan_summary(user_id)` — return plan summary
    - Handle skip case (allow dashboard access, persist prompt flag)
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 17.1, 17.4, 18.1, 18.2, 18.3, 18.4, 18.5_

  - [ ] 10.5 Implement Onboarding router with API endpoints
    - `POST /v1/onboarding` — submit exam date + preferences
    - `PATCH /v1/onboarding/exam-date` — update exam date
    - `GET /v1/onboarding/plan-summary` — get generated plan summary
    - Wire dependency injection via `get_onboarding_service` factory
    - _Requirements: 16.1, 16.2, 17.4, 18.1_

  - [ ]* 10.6 Write unit tests for Onboarding feature (repository, service, router layers)
    - Repository tests: create_profile, get_profile, update_exam_date
    - Service tests: valid submission, past date rejection, >365 days rejection, skip flow, exam date update with plan regeneration, returning user skips mastered subtopics
    - Router tests: all 3 endpoints happy path + validation errors (past date, invalid category, invalid time budget)
    - _Requirements: 16.2, 16.3, 16.5, 16.6, 17.1, 17.5, 18.1, 18.3, 18.4_

- [ ] 11. Checkpoint - Ensure gamification and onboarding tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement Readiness Self-Assessment Calibration
  - [ ] 12.1 Implement self-assessment service methods in ReadinessService
    - Implement `submit_self_assessment(user_id, self_assessed_score)` — compute delta, determine calibration_status (overconfident if delta > +15, well_calibrated if -10 to +15, underconfident if < -10), persist record, return response with appropriate messaging
    - Implement `get_self_assessment_history(user_id)` — return all self-assessment records for calibration trend
    - Implement `is_self_assessment_due(user_id)` — return True if 7+ days since last assessment or no history exists
    - Generate calibration_warning message for overconfident users (identify weakest component contributing to gap)
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7_

  - [ ] 12.2 Implement self-assessment Pydantic schemas
    - Create `SelfAssessmentRequest` (self_assessed_score: int, validated 0-100)
    - Create `SelfAssessmentResponse` (self_assessed_score, computed_score, delta, calibration_status, calibration_warning or encouraging message)
    - Create `SelfAssessmentHistoryResponse` (list of records with assessed_at, scores, delta, status)
    - Create `SelfAssessmentPromptResponse` (is_due: bool, last_assessed_at: datetime | None)
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6_

  - [ ] 12.3 Implement self-assessment repository methods
    - `create_self_assessment(record)` — persist new self-assessment record
    - `get_latest_assessment(user_id)` — return most recent record for prompt timing check
    - `get_assessment_history(user_id)` — return all records ordered by assessed_at descending
    - _Requirements: 19.2, 19.6, 19.7_

  - [ ] 12.4 Implement self-assessment router endpoints
    - `POST /v1/readiness/self-assessment` — submit self-assessed readiness score
    - `GET /v1/readiness/self-assessment/history` — get calibration history
    - `GET /v1/readiness/self-assessment/prompt` — check if prompt is due
    - Validate self_assessed_score is integer 0-100 (reject otherwise with INVALID_SELF_ASSESSMENT_SCORE)
    - _Requirements: 19.1, 19.6, 19.7_

  - [ ]* 12.5 Write property tests for self-assessment calibration (Properties 36-38)
    - **Property 36: Self-assessment calibration status matches delta ranges**
    - **Property 37: Self-assessment prompt respects 7-day interval**
    - **Property 38: Self-assessment scores are clamped to valid range**
    - **Validates: Requirements 19.1, 19.3, 19.4, 19.5, 19.7**

  - [ ]* 12.6 Write unit tests for self-assessment (repository, service, router layers)
    - Repository tests: create_self_assessment, get_latest_assessment, get_assessment_history
    - Service tests: overconfident case (delta > +15), well_calibrated case (-10 to +15), underconfident case (< -10), prompt due after 7 days, prompt not due within 7 days, first-time user (always due)
    - Router tests: submit happy path, invalid score (< 0, > 100, non-integer → 422), history endpoint, prompt endpoint
    - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7_

- [ ] 13. Integration wiring and cross-feature event flow
  - [ ] 13.1 Wire readiness score recomputation triggers
    - Hook into existing quiz completion flow to call `ReadinessService.compute_and_persist`
    - Hook into mock exam completion flow to trigger recompute
    - Hook into flashcard review session completion to trigger recompute
    - Ensure recompute runs within the same request transaction
    - Trigger milestone evaluation after score update
    - _Requirements: 2.1, 13.4_

  - [ ] 13.2 Wire mock exam completion to diagnostic generation
    - After mock exam submission, automatically call `MockAnalyticsService.generate_diagnostic`
    - Persist diagnostic report for later retrieval
    - _Requirements: 10.1, 10.5_

  - [ ] 13.3 Wire recommendation acceptance to queue engine
    - When user accepts a recommendation, feed subtopic into QueueService as high-priority item for next queue generation
    - _Requirements: 12.4_

  - [ ] 13.4 Wire study consistency tracking to queue completion
    - At end of day (or on next queue request), evaluate previous day's queue completion percentage
    - Update StudyConsistency record accordingly
    - Adjust next day's queue with catch-up items from missed FSRS-due cards
    - _Requirements: 14.1, 14.5_

  - [ ] 13.5 Wire onboarding to queue engine and readiness
    - After onboarding submission, initialize first daily queue
    - Set exam date for retention component projection
    - _Requirements: 16.4, 17.1, 18.2, 18.5_

  - [ ] 13.6 Register all new routers in FastAPI app
    - Mount readiness, smart_queue, explanations, mock_analytics routers in `app/main.py`
    - Mount milestones and consistency endpoints
    - Mount onboarding endpoints
    - _Requirements: All API endpoints_

  - [ ]* 13.7 Write integration tests for cross-feature event flows
    - Test: quiz completion triggers readiness recompute and milestone evaluation
    - Test: mock exam completion generates diagnostic report
    - Test: recommendation acceptance feeds into next queue
    - Test: queue idempotency within same UTC day
    - Test: exam date update triggers retention recompute
    - _Requirements: 2.1, 10.1, 12.4, 4.5, 18.5_

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Frontend: API client and shared hooks
  - [ ] 15.1 Add new API endpoints to `web/src/api/client.ts`
    - Add readiness endpoints (GET /readiness, /readiness/dashboard, /readiness/trend, POST/GET self-assessment)
    - Add queue endpoints (GET /queue, POST complete/regenerate, GET/PATCH preferences)
    - Add explanation endpoints (GET single, POST bulk, POST escalate)
    - Add mock analytics endpoints (GET diagnostic, GET recommendations, POST accept, GET prediction)
    - Add milestone and consistency endpoints
    - Add onboarding endpoints (POST, PATCH exam-date, GET plan-summary)
    - _Requirements: All API endpoints_

  - [ ] 15.2 Create shared React hooks for new features
    - `useReadiness()` — fetch and cache readiness score, dashboard data, trend
    - `useDailyQueue()` — fetch queue, complete items, regenerate
    - `useExplanation(questionId)` — fetch explanation with IndexedDB cache fallback
    - `useMockAnalytics(attemptId)` — fetch diagnostic, recommendations, prediction
    - `useMilestones()` — fetch milestone statuses
    - `useOnboarding()` — submit/update exam date, get plan summary
    - `useSelfAssessment()` — check if prompt due, submit, get history
    - _Requirements: 9.1, 9.4_

  - [ ] 15.3 Implement IndexedDB offline caching for explanations
    - Create IndexedDB store for question explanations keyed by question_id
    - Implement prefetch logic: on quiz/session load, bulk-fetch explanations and store in IndexedDB
    - Implement cache staleness check using cache_version field
    - Implement offline fallback: serve from IndexedDB when navigator.onLine is false
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ] 16. Frontend: Onboarding flow
  - [ ] 16.1 Build Onboarding page component (`web/src/pages/onboarding/Onboarding.tsx`)
    - Exam date picker (calendar input, validates 1-365 days in future)
    - Exam category selector (Professional / Sub-Professional)
    - Time budget selector (15 / 30 / 60 minutes)
    - Skip button with persistent prompt behavior
    - Warning display for <7 days exam dates
    - Submit calls POST /v1/onboarding, then redirects to dashboard
    - _Requirements: 16.1, 16.2, 16.3, 16.5, 16.6_

  - [ ] 16.2 Add onboarding route guard
    - Check if user has completed onboarding (has OnboardingProfile)
    - If not, redirect to onboarding page on first login
    - If skipped, show persistent banner on dashboard prompting to set exam date
    - Add route to React Router: `/onboarding`
    - _Requirements: 16.1, 16.5_

- [ ] 17. Frontend: Dashboard with Readiness Score
  - [ ] 17.1 Build Readiness Score dashboard widget (`web/src/pages/home/ReadinessScore.tsx`)
    - Large circular progress indicator showing 0-100 score
    - Readiness level label (Not Ready / Getting There / Almost Ready / Exam Ready)
    - Component breakdown visualization (4 bars: mastery, retention, mock, coverage)
    - 7-day delta indicator (+/- badge)
    - Score change summary when delta ≥ 5
    - Stale data indicator when stale_data flag is true
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ] 17.2 Build Top Impact Areas widget
    - Display top 3 subtopics with highest Point_Impact
    - Show estimated point gain for each
    - Link each to the relevant subtopic study page
    - _Requirements: 3.1_

  - [ ] 17.3 Build Readiness Trend chart
    - 30-day line chart showing readiness score over time
    - Fetch from GET /v1/readiness/trend
    - Handle carry-forward gaps gracefully in visualization
    - _Requirements: 2.4_

  - [ ] 17.4 Build Self-Assessment prompt modal
    - Show modal when `is_self_assessment_due` returns true on dashboard load
    - Slider or number input for 0-100 self-assessment
    - After submission, show comparison: self-assessed vs computed with delta
    - Display calibration_warning for overconfident users, encouraging message for well-calibrated/underconfident
    - Dismissible (don't show again for 7 days)
    - _Requirements: 19.1, 19.3, 19.4, 19.5, 19.7_

  - [ ] 17.5 Integrate readiness score as primary dashboard element
    - Replace or augment existing Home page to show readiness score as the first/largest widget
    - Position daily queue CTA ("Start Today's Study") prominently below readiness score
    - _Requirements: 3.1_

- [ ] 18. Frontend: Daily Queue player
  - [ ] 18.1 Build Daily Queue page (`web/src/pages/queue/DailyQueue.tsx`)
    - Display ordered list of queue items with type icons (flashcard/quiz/lesson)
    - Show estimated duration per item and total session time
    - Show progress bar (items completed / items total)
    - "Start" button launches the first uncompleted item
    - _Requirements: 4.5, 5.1, 6.4_

  - [ ] 18.2 Build queue item execution flow
    - Flashcard review: navigate to flashcard study session with the specific card IDs
    - Quiz practice: navigate to quiz player with the specific subtopic and question count/difficulty
    - New content: navigate to lesson reader at the specific section
    - On completion of each item, call POST /v1/queue/items/{id}/:complete and return to queue
    - _Requirements: 4.6, 5.2, 5.3, 5.4_

  - [ ] 18.3 Build queue preferences settings
    - Time budget selector (15/30/60 min) in user settings or queue page header
    - Call PATCH /v1/queue/preferences on change
    - Show regeneration notice when applicable
    - _Requirements: 6.1, 6.3, 6.5_

  - [ ] 18.4 Add queue route to React Router
    - Route: `/queue` (or `/study/today`)
    - Add navigation link in main navbar
    - _Requirements: 4.5_

- [ ] 19. Frontend: Inline explanations in Quiz Player
  - [ ] 19.1 Modify existing QuizPlayer to show explanations after answer submission
    - After user selects an answer, display explanation panel below the question
    - Show explanation_text (render markdown), key_concept badge, related subtopics links
    - Show "Still confused? Ask why" button for AI Tutor escalation
    - Handle null explanations gracefully (don't show panel)
    - _Requirements: 7.2, 7.3, 7.4, 8.1_

  - [ ] 19.2 Implement AI Tutor escalation UI
    - "Still confused? Ask why" button calls POST /v1/explanations/{id}/:escalate
    - Display tutor response inline below the explanation
    - Show rate limit message when 20/day limit reached
    - _Requirements: 8.1, 8.3, 8.4_

  - [ ] 19.3 Prefetch explanations on quiz session start
    - On quiz load, call POST /v1/explanations/bulk with all question IDs in the session
    - Store in IndexedDB for offline access
    - Serve from cache when offline
    - _Requirements: 9.1, 9.4_

- [ ] 20. Frontend: Mock Exam Analytics
  - [ ] 20.1 Build Mock Exam Results page (`web/src/pages/mock-exam/MockExamResults.tsx`)
    - Display total score with pass/fail indicator (80% threshold)
    - Per-subtopic breakdown table (subtopic, questions, correct, points lost)
    - Highest impact areas highlighted
    - Regression alerts with warning styling
    - Difficulty distribution chart (easy/medium/hard accuracy)
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [ ] 20.2 Build Predicted Score Range widget
    - Display predicted range (lower–upper) with midpoint
    - Confidence level indicator (low/medium/high)
    - "Take more mock exams for better prediction" message when <2 exams
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ] 20.3 Build Actionable Recommendations panel
    - List up to 5 recommendations with subtopic name, current vs target accuracy, estimated point gain
    - Human-readable formatted string (e.g., "Fix Ratio & Proportion to gain +4 points")
    - "Add to my study queue" button per recommendation (calls POST accept)
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ] 20.4 Wire mock exam completion to analytics page
    - After mock exam submission, redirect to MockExamResults page
    - Trigger diagnostic generation on backend (via existing mock exam completion flow)
    - _Requirements: 10.1_

- [ ] 21. Frontend: Milestones and Consistency
  - [ ] 21.1 Build Milestones page (`web/src/pages/milestones/Milestones.tsx`)
    - Display all milestones grouped by category (mastery, readiness, recovery)
    - Show status: locked (greyed), in_progress (with progress bar), earned (with date)
    - Progress percentage for in_progress milestones
    - _Requirements: 13.7_

  - [ ] 21.2 Build Study Consistency widget (dashboard or profile)
    - Display current streak, longest streak, total consistent days
    - Calendar heatmap showing qualifying days
    - _Requirements: 14.4_

  - [ ] 21.3 Add milestones route to React Router
    - Route: `/milestones`
    - Add navigation link in main navbar or profile section
    - _Requirements: 13.7_

- [ ] 22. Data seeding and migration
  - [ ] 22.1 Seed competence milestone definitions
    - Create seed script for 8 milestone definitions (Verbal Mastery, Numerical Mastery, Analytical Mastery, Full Spectrum, Exam Ready: Sub-Professional, Exam Ready: Professional, Comeback, Resilient Learner)
    - Include threshold_config JSON for each
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 22.2 Generate and seed question explanations
    - Create script to batch-generate explanations for all 36,000 questions
    - Each explanation includes: explanation_text (50-2000 chars), key_concept, related_subtopics
    - Seed into question_explanations table
    - _Requirements: 7.1_

  - [ ] 22.3 Modify existing quiz answer submission to include explanations
    - Update existing quiz router/service to include explanation in answer response payload
    - Ensure backward compatibility (null explanation if not yet seeded)
    - _Requirements: 7.2, 7.4_

  - [ ] 22.4 Modify existing mock exam submission to trigger diagnostic generation
    - Hook MockAnalyticsService.generate_diagnostic into the existing mock exam completion flow
    - _Requirements: 10.1, 10.5_

- [ ] 23. Final deployment verification
  - [ ] 23.1 End-to-end smoke test
    - New user registers → onboarding flow → exam date set → plan generated
    - Dashboard shows readiness score 0 → daily queue generated with new content
    - Complete quiz → explanation shown → readiness score updates
    - Complete mock exam → analytics page shows diagnostic + recommendations
    - Accept recommendation → appears in next day's queue
    - Self-assessment prompt appears after 7 days
    - Milestone awarded when threshold met
    - _Requirements: All_

  - [ ] 23.2 Offline functionality verification
    - Load quiz with explanations while online
    - Go offline → answer questions → explanations still display from IndexedDB
    - _Requirements: 9.1, 9.4_

  - [ ] 23.3 Performance verification
    - Dashboard loads within 2 seconds (Req 3.4)
    - Readiness computation completes within 3 seconds (Req 2.1)
    - Milestone status returns within 2 seconds (Req 13.8)
    - _Requirements: 2.1, 3.4, 13.8_

- [ ] 24. Implement Pretesting System (Phase 8)
  - [ ] 24.1 Create PretestAttempt model and migration
    - Add PretestAttempt table with user_id, subtopic_id, questions JSON, score, created_at
    - _Requirements: 20.4, 21.3_
  - [ ] 24.2 Implement pretest generation algorithm
    - Select 3-5 questions covering distinct key_concepts at easy-medium difficulty
    - Ensure questions are from the subtopic's question bank
    - _Requirements: 20.1, 20.2_
  - [ ] 24.3 Implement pretest service and router
    - POST /v1/pretests/{subtopic_id}/start — generate and return pretest questions
    - POST /v1/pretests/{pretest_id}/submit — submit answers, persist results
    - GET /v1/pretests/{subtopic_id}/comparison — return pre vs post comparison
    - Skip pretest if lesson already completed (Req 20.7)
    - _Requirements: 20.1, 20.3, 20.4, 20.5, 20.6, 20.7_
  - [ ] 24.4 Wire pretest results into Queue_Engine
    - Record which key_concepts user got wrong, prioritize in future quiz_practice
    - Ensure pretest scores do NOT affect mastery component
    - _Requirements: 21.1, 21.2, 21.3_
  - [ ]* 24.5 Write tests for pretesting
    - Property test: pretest scores do not affect mastery (Property 39)
    - Unit tests: pretest generation covers distinct key_concepts, skip logic for completed lessons
    - _Requirements: 20.2, 20.7, 21.2_

- [ ] 25. Implement Elaborative Interrogation (Phase 9)
  - [ ] 25.1 Create PersonalNote and LessonReflection models
    - PersonalNote: user_id, question_id, note_text (500 chars max), created_at
    - LessonReflection: user_id, lesson_id, section_index, reflection_text, created_at
    - _Requirements: 22.3, 23.3_
  - [ ] 25.2 Implement elaborative prompt service and router
    - POST /v1/explanations/{question_id}/note — persist personal note (no grading)
    - GET /v1/notes — return all notes grouped by subtopic
    - POST /v1/lessons/{lesson_id}/reflections — persist lesson reflection
    - Display previous note on re-encounter (Req 22.5)
    - _Requirements: 22.1, 22.3, 22.4, 22.5, 22.6, 23.1, 23.3_
  - [ ] 25.3 Surface lesson reflections in daily queue as review items
    - _Requirements: 23.5_
  - [ ]* 25.4 Write unit tests for elaborative interrogation
    - Test note persistence and retrieval, skippable prompts, note display on re-encounter
    - _Requirements: 22.2, 22.5, 23.4_

- [ ] 26. Implement Generation Effect / Recall Mode (Phase 10)
  - [ ] 26.1 Create RecallAnswer model and recall grading algorithm
    - RecallAnswer: user_id, question_id, user_response, is_correct, match_type, created_at
    - Implement grade_recall_answer with keyword matching + Levenshtein distance ≤ 2
    - _Requirements: 24.1, 24.3, 24.4_
  - [ ] 26.2 Implement recall question generation from existing MCQs
    - Convert MCQ correct answer into a blank within the stem
    - _Requirements: 24.2_
  - [ ] 26.3 Implement recall mode in quiz service and router
    - POST /v1/quiz-attempts/{attempt_id}/recall-answer — grade and persist recall answer
    - Track recall accuracy separately, weight 1.5× in mastery calculation
    - _Requirements: 24.3, 24.4, 24.6_
  - [ ] 26.4 Integrate recall items into Queue_Engine
    - Include recall-mode items for subtopics with mastery 0.5-0.8
    - _Requirements: 24.5_
  - [ ]* 26.5 Write tests for recall mode
    - Property test: Levenshtein distance ≤ 2 accepts fuzzy matches (Property 40)
    - Unit tests: MCQ-to-recall conversion, "needs review" for inconclusive matches
    - _Requirements: 24.3, 24.4_

- [ ] 27. Implement Sleep-Aware Review (Phase 11)
  - [ ] 27.1 Create GoodnightReviewSession model and bedtime preference
    - GoodnightReviewSession: user_id, session_date, items JSON, completed_at, bedtime_preference
    - Add bedtime_preference field to user settings (default 22:00)
    - _Requirements: 25.1, 25.2, 25.6_
  - [ ] 27.2 Implement goodnight review generation algorithm
    - Select 5-10 items with lowest confidence from today's study activity
    - Cap at 5 minutes duration
    - Only include items studied today (no new material)
    - _Requirements: 25.1, 25.3, 25.7_
  - [ ] 27.3 Implement goodnight review service and router
    - GET /v1/queue/goodnight — generate and return goodnight session
    - POST /v1/queue/goodnight/:complete — mark completed, apply 1.2× FSRS interval adjustment
    - PATCH /v1/preferences/bedtime — set bedtime preference
    - _Requirements: 25.1, 25.2, 25.4, 25.5_
  - [ ] 27.4 Implement bedtime inference from usage patterns
    - Average last activity timestamp over past 7 days
    - _Requirements: 25.6_
  - [ ]* 27.5 Write tests for sleep-aware review
    - Property test: goodnight review only contains today's items (Property 41)
    - Property test: goodnight review ≤ 10 items (Property 42)
    - Unit tests: 1.2× interval adjustment on completion, no penalty on skip
    - _Requirements: 25.1, 25.4, 25.5, 25.7_

- [ ] 28. Implement Post-Session Metacognitive Reflection (Phase 12)
  - [ ] 28.1 Create SessionReflection model
    - id, user_id, session_date, hardest_item_id, confidence_rating (1-5), review_note (nullable text), created_at
    - _Requirements: 26.3_
  - [ ] 28.2 Implement reflection service and router
    - POST /v1/sessions/{date}/reflection — persist reflection
    - GET /v1/sessions/reflections — return reflection history
    - _Requirements: 26.1, 26.3, 26.7_
  - [ ] 28.3 Wire reflection into Queue_Engine
    - Hardest item gets priority boost (level 2) in next day's queue
    - Confidence 1-2 adds extra review items for session's subtopics
    - _Requirements: 26.4, 26.5_
  - [ ]* 28.4 Write tests for metacognitive reflection
    - Property test: confidence 1-2 boosts next-day queue (Property 43)
    - Unit tests: reflection persistence, priority boost logic
    - _Requirements: 26.4, 26.5_

- [ ] 29. Implement Concrete Example Anchoring (Phase 13)
  - [ ] 29.1 Add concrete_examples field to QuestionExplanation model
    - Add column: concrete_examples (Text, nullable, JSON array of strings max 3 items × 100 chars)
    - Run migration
    - _Requirements: 27.1_
  - [ ] 29.2 Update explanation response to include concrete examples
    - Display in a visually distinct callout labeled "Think of it like this:"
    - Degrade gracefully when no examples stored
    - _Requirements: 27.2, 27.5_
  - [ ] 29.3 Generate concrete examples for existing question bank
    - Create script to batch-generate Filipino-context concrete examples for all questions with explanations
    - Use contexts: jeepneys, barangays, government offices, Filipino names
    - _Requirements: 27.1, 27.3_
  - [ ] 29.4 Include concrete examples in flashcard generation
    - _Requirements: 27.4_
  - [ ]* 29.5 Write unit tests for concrete examples
    - Test graceful degradation when field is null
    - Test that examples array is limited to 3 items
    - _Requirements: 27.2, 27.5_

- [ ] 30. Implement Productive Failure Sequences (Phase 14)
  - [ ] 30.1 Create ChallengeAttempt model
    - id, user_id, subtopic_id, question_id, pre_lesson_answer, pre_lesson_correct, post_lesson_answer, post_lesson_correct, is_productive_failure_success, created_at
    - _Requirements: 28.5_
  - [ ] 30.2 Implement challenge problem selection in Queue_Engine
    - Prepend a hard-difficulty question before new_content items when mastery < 0.4
    - Limit to 1 challenge problem per daily queue session
    - Only for subtopics with mastery < 0.4
    - _Requirements: 28.1, 28.6, 28.7_
  - [ ] 30.3 Implement challenge service and router
    - POST /v1/challenges/{subtopic_id}/attempt — submit pre-lesson attempt with failure-normalizing framing
    - POST /v1/challenges/{challenge_id}/retest — submit post-lesson retest, compute comparison
    - Track productive_failure_success flag
    - _Requirements: 28.2, 28.3, 28.4, 28.5_
  - [ ]* 30.4 Write tests for productive failure
    - Property test: challenge problems only for mastery < 0.4 (Property 44)
    - Property test: max 1 challenge per queue (Property 45)
    - Unit tests: before/after comparison display, productive_failure_success flagging
    - _Requirements: 28.1, 28.5, 28.6, 28.7_

- [ ] 31. Frontend: New learning technique UIs
  - [ ] 31.1 Build Pretest Challenge UI
    - Present pretest before first lesson visit with encouraging framing
    - Show before/after comparison after lesson completion
    - _Requirements: 20.1, 20.3, 20.5, 20.6_
  - [ ] 31.2 Build Elaborative Interrogation UI
    - "Why does this make sense?" text input after incorrect answers
    - Display previous personal notes on re-encounter
    - Collapsible prompts in lesson reader at key concept sections
    - _Requirements: 22.1, 22.2, 22.5, 23.1, 23.2_
  - [ ] 31.3 Build Recall Mode UI in Quiz Player
    - Text input field instead of MCQ options
    - "Needs review" state with self-assessment option
    - _Requirements: 24.1, 24.4_
  - [ ] 31.4 Build Goodnight Review UI
    - Compact flashcard session triggered at bedtime
    - Show "sleep consolidation" message on completion
    - _Requirements: 25.1, 25.2, 25.3_
  - [ ] 31.5 Build Session Reflection UI
    - 30-second reflection prompt after queue completion
    - Hardest item selector, confidence slider, optional note
    - _Requirements: 26.1, 26.2, 26.6_
  - [ ] 31.6 Build Concrete Examples callout in explanation display
    - Visually distinct callout: "Think of it like this:"
    - Filipino-context examples below explanation text
    - _Requirements: 27.2, 27.3_
  - [ ] 31.7 Build Productive Failure UI
    - Challenge problem with failure-normalizing framing
    - Before/after comparison after lesson
    - _Requirements: 28.2, 28.3, 28.4_

- [ ] 32. Final checkpoint - All phases verified
  - Ensure all tests pass for phases 8-14, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation after each major phase
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases per the three-layer testing strategy
- The implementation uses Python with FastAPI, SQLAlchemy, and Hypothesis for property-based testing
- All algorithm modules are pure functions with no DB access, enabling isolated testing
- Cross-feature wiring (task 12) depends on all individual features being implemented first

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"] },
    { "id": 1, "tasks": ["1.7"] },
    { "id": 2, "tasks": ["2.1", "4.1", "6.1", "7.1", "7.2"] },
    { "id": 3, "tasks": ["2.2", "2.3", "2.4", "4.2", "4.3", "4.4", "6.2", "7.3", "7.4", "7.5", "7.6"] },
    { "id": 4, "tasks": ["2.5", "4.5", "6.3", "7.7"] },
    { "id": 5, "tasks": ["2.6", "2.7", "4.6", "6.4", "7.8"] },
    { "id": 6, "tasks": ["2.8", "4.7", "6.5", "7.9"] },
    { "id": 7, "tasks": ["9.1", "9.3", "10.1"] },
    { "id": 8, "tasks": ["9.2", "9.4", "9.5", "10.2", "10.3", "10.4"] },
    { "id": 9, "tasks": ["9.6", "10.5", "10.6"] },
    { "id": 10, "tasks": ["12.1", "12.2", "12.3"] },
    { "id": 11, "tasks": ["12.4", "12.5", "12.6"] },
    { "id": 12, "tasks": ["13.1", "13.2", "13.3", "13.4", "13.5", "13.6"] },
    { "id": 13, "tasks": ["13.7"] },
    { "id": 14, "tasks": ["15.1", "15.2", "15.3", "22.1", "22.2"] },
    { "id": 15, "tasks": ["16.1", "16.2", "17.1", "17.2", "17.3", "17.4", "17.5"] },
    { "id": 16, "tasks": ["18.1", "18.2", "18.3", "18.4", "19.1", "19.2", "19.3"] },
    { "id": 17, "tasks": ["20.1", "20.2", "20.3", "20.4", "21.1", "21.2", "21.3"] },
    { "id": 18, "tasks": ["22.3", "22.4"] },
    { "id": 19, "tasks": ["23.1", "23.2", "23.3"] },
    { "id": 20, "tasks": ["24.1", "25.1", "26.1", "28.1", "29.1", "30.1"] },
    { "id": 21, "tasks": ["24.2", "24.3", "25.2", "26.2", "26.3", "27.1", "27.2", "29.2", "30.2"] },
    { "id": 22, "tasks": ["24.4", "24.5", "25.3", "25.4", "26.4", "26.5", "27.3", "27.4", "27.5", "28.2", "28.3", "28.4", "29.3", "29.4", "29.5", "30.3", "30.4"] },
    { "id": 23, "tasks": ["31.1", "31.2", "31.3", "31.4", "31.5", "31.6", "31.7"] },
    { "id": 24, "tasks": ["32"] }
  ]
}
```
