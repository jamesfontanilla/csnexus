# Requirements Document

## Introduction

This feature implements research-backed learning intelligence across the CSNexus platform, transforming it from a content delivery system into an adaptive exam preparation engine. It introduces six interconnected capabilities: a composite Readiness Score that synthesizes mastery, retention, and mock exam data into a single 0–100 metric; a Smart Daily Queue that algorithmically generates personalized study sessions; inline question explanations with AI Tutor escalation; post-mock exam diagnostic analytics with actionable recommendations; competence-based gamification milestones tied to exam structure; and an exam date onboarding flow that makes the study planner the entry point to the platform.

## Glossary

- **Readiness_Engine**: The backend service (`app/features/readiness/service.py`) that computes and persists the composite readiness score per user
- **Readiness_Score**: A persistent 0–100 integer representing a user's overall exam preparedness, synthesized from mastery, retention, mock exam performance, and coverage data
- **Queue_Engine**: The backend service (`app/features/smart_queue/service.py`) that generates personalized daily study sessions
- **Daily_Queue**: An ordered list of study items (flashcard reviews, quiz questions, new content) generated for a user on a given day, capped by their time budget
- **Explanation_Service**: The backend service (`app/features/explanations/service.py`) that manages static question explanations and AI Tutor escalation
- **Explanation**: A rich text field attached to a question containing the reasoning behind the correct answer, visible immediately after answering
- **Mock_Analytics_Engine**: The backend service (`app/features/mock_analytics/service.py`) that produces diagnostic breakdowns after mock exam completion
- **Diagnostic_Report**: A structured analysis of a completed mock exam showing subtopic-level point loss, predicted score range, and actionable recommendations
- **Competence_Milestone**: A gamification achievement tied to exam-relevant competence thresholds rather than generic activity metrics
- **Study_Consistency**: A metric tracking days where the user followed their Smart Daily Queue, replacing raw login streaks
- **Onboarding_Engine**: The backend service (`app/features/onboarding/service.py`) that captures exam date and generates the initial personalized study plan
- **FSRS_Retention**: The projected probability of recall for a flashcard at a future date, computed using the FSRS algorithm's memory stability and elapsed time
- **Coverage_Gap**: A subtopic where the user has attempted fewer than 10% of available questions or has no mastery record
- **Time_Budget**: The user's preferred daily study session length (15, 30, or 60 minutes)
- **Point_Impact**: The estimated score improvement achievable by raising a specific subtopic's mastery from its current level to the target threshold

## Requirements

---

## Phase 1: Readiness Score System

### Requirement 1: Readiness Score Computation

**User Story:** As a CSE examinee, I want a single readiness score that tells me how prepared I am for my exam, so that I can gauge my overall progress without interpreting multiple disconnected metrics.

#### Acceptance Criteria

1. WHEN a user requests their readiness score, THE Readiness_Engine SHALL compute a composite score from 0 to 100 by combining: mastery component (weighted 40%), retention component (weighted 25%), mock exam component (weighted 25%), and coverage component (weighted 10%)
2. THE Readiness_Engine SHALL compute the mastery component as the weighted average of all UserSubtopicMastery.mastery_score values (each ranging from 0.0 to 1.0, scaled to 0–100) across the user's 60 subtopics, where each subtopic is weighted by its question count proportion in the exam; subtopics with no mastery record SHALL be treated as mastery_score 0.0
3. THE Readiness_Engine SHALL compute the retention component by averaging FSRS_Retention predictions across all flashcards the user has studied (at least one completed review), projected to their target_exam_date; IF the user has no flashcard history, THEN THE Readiness_Engine SHALL use the average of UserSubtopicMastery.retention_score values as a fallback
4. THE Readiness_Engine SHALL compute the mock exam component as the weighted average of the user's completed mock exam scores (percentage correct), where only fully completed exams (all questions answered) are included, recent exams (within 14 days) receive weight 1.0, exams 15–30 days old receive weight 0.7, and exams older than 30 days receive weight 0.4
5. THE Readiness_Engine SHALL compute the coverage component as the percentage of the 60 subtopics where the user has attempted at least 10% of available questions for that subtopic (where each subtopic has a minimum of 60 available questions in the question bank)
6. IF a user has no mock exam history, THEN THE Readiness_Engine SHALL redistribute the mock exam weight equally across mastery (52.5%) and retention (37.5%) while keeping coverage at 10%
7. IF a user has no exam date set, THEN THE Readiness_Engine SHALL compute the retention component using a default projection of 30 days from the current date
8. THE Readiness_Engine SHALL round the final composite score to the nearest integer using half-up rounding and clamp the result to the range 0–100 inclusive
9. IF a user has no study activity (no mastery records, no flashcard history, and no mock exam history), THEN THE Readiness_Engine SHALL return a readiness score of 0 without performing component calculations

### Requirement 2: Readiness Score Persistence and Updates

**User Story:** As a CSE examinee, I want my readiness score to update automatically as I study, so that I always see an accurate reflection of my current preparedness.

#### Acceptance Criteria

1. WHEN a user completes a quiz, mock exam, or flashcard review session, THE Readiness_Engine SHALL recompute and persist the updated readiness score within the same request transaction, completing the computation within 3 seconds
2. THE Readiness_Engine SHALL store a readiness score history record containing: user_id, score, computed_at timestamp, and the individual component values (mastery_component, retention_component, mock_component, coverage_component), retained for at least 365 days
3. WHEN a user requests their readiness score, THE Readiness_Engine SHALL return the most recently persisted score along with the component breakdown and the score delta compared to 7 days ago; IF no score record exists from 7 or more days ago, THEN THE Readiness_Engine SHALL return a null delta value
4. THE Readiness_Engine SHALL expose a readiness trend endpoint returning one readiness score per day for the past 30 days, using the last computed score of each day as the representative value; for days where no score was computed, THE Readiness_Engine SHALL carry forward the most recent prior score
5. IF a user has never completed any study activity, THEN THE Readiness_Engine SHALL return a readiness score of 0 with all components set to 0
6. IF the readiness score computation fails due to a data retrieval or calculation error, THEN THE Readiness_Engine SHALL return the most recently persisted score with a stale_score flag set to true and preserve the original study activity data for retry

### Requirement 3: Readiness Dashboard Display

**User Story:** As a CSE examinee, I want the readiness score to be the first thing I see on login, so that I have immediate context on where I stand.

#### Acceptance Criteria

1. WHEN a user loads the dashboard, THE Readiness_Engine SHALL return the current readiness score, component breakdown, 7-day delta, and the top 3 subtopics with the highest Point_Impact (most potential score gain if improved); IF fewer than 3 subtopics have Point_Impact data, THEN THE Readiness_Engine SHALL return only the available subtopics (minimum 0)
2. THE Readiness_Engine SHALL return a readiness_level classification: "Not Ready" (0–39), "Getting There" (40–59), "Almost Ready" (60–79), "Exam Ready" (80–100)
3. WHEN the readiness score changes by 5 or more points since the last login, THE Readiness_Engine SHALL include a score_change_summary field containing: the primary contributing component (mastery, retention, mock_exam, or coverage), the direction and magnitude of that component's change, and the overall score delta
4. WHEN a user loads the dashboard, THE Readiness_Engine SHALL return the dashboard response within 2 seconds measured from request receipt to response dispatch
5. IF the Readiness_Engine cannot compute the readiness score due to a service or data error, THEN THE Readiness_Engine SHALL return the last successfully persisted score with a stale_data flag set to true and the computed_at timestamp of that score

---

## Phase 2: Smart Daily Queue

### Requirement 4: Queue Generation Algorithm

**User Story:** As a CSE examinee, I want a personalized daily study session generated for me, so that I study the right things in the right order without decision fatigue.

#### Acceptance Criteria

1. WHEN a user requests their daily queue, THE Queue_Engine SHALL generate an ordered list of study items respecting this priority: (1) FSRS-due flashcards where next_review_date ≤ today, sorted by days overdue descending, (2) weakest subtopics from the user's last 7 days of quiz performance (3 subtopics with the lowest accuracy percentage, minimum 1 quiz attempt required to qualify), limited to 3 subtopics, (3) new content from Coverage_Gap subtopics the user has not yet started, ordered by exam weight descending
2. THE Queue_Engine SHALL cap the total estimated session duration at the user's configured Time_Budget (15, 30, or 60 minutes), using these time estimates: flashcard review = 8 seconds per card, quiz question = 45 seconds per question, new lesson content = 5 minutes per lesson section; IF the total duration of priority-1 items alone exceeds the Time_Budget, THEN THE Queue_Engine SHALL truncate the flashcard list to fit within the budget and omit lower-priority items
3. WHEN the user has an exam date set and fewer than 14 days remain, THE Queue_Engine SHALL allocate 60% of the time budget to FSRS-due items, 30% to quiz practice on subtopics with the highest Point_Impact, and 10% to review of previously completed content; new content SHALL NOT be introduced unless FSRS-due items consume less than 60% of the budget
4. WHEN the user has an exam date set and fewer than 7 days remain, THE Queue_Engine SHALL allocate 80% of the time budget to FSRS-due items and 20% to quiz practice on subtopics where the user's mock exam accuracy is below 60%, and SHALL exclude new content entirely
5. THE Queue_Engine SHALL generate the queue idempotently: requesting the queue multiple times on the same calendar day (determined by UTC midnight boundary) for the same user SHALL return the same ordered list unless the user completes items or explicitly regenerates
6. WHEN a user completes an item in the daily queue, THE Queue_Engine SHALL mark it as completed and update the remaining time budget for the session
7. IF the user has no FSRS-due flashcards and no weak subtopics (no quiz attempts in the last 7 days), THEN THE Queue_Engine SHALL fill the queue with new content from the subtopic with the lowest coverage percentage
8. IF the user has no study data (no flashcards created, no quiz history, and no content started), THEN THE Queue_Engine SHALL generate a queue consisting entirely of new content items starting from the subtopic with the highest exam weight in the user's selected exam_category

### Requirement 5: Queue Item Types

**User Story:** As a CSE examinee, I want my daily queue to mix different activity types, so that my study sessions maintain variety and engagement.

#### Acceptance Criteria

1. THE Queue_Engine SHALL support three item types in the daily queue: "flashcard_review" (batch of due flashcards), "quiz_practice" (set of questions from a weak subtopic), and "new_content" (lesson section from an uncovered subtopic)
2. WHEN generating a "flashcard_review" item, THE Queue_Engine SHALL include the card IDs (maximum 30 cards per batch), estimated duration (computed as card count × 8 seconds), and the deck name for context
3. WHEN generating a "quiz_practice" item, THE Queue_Engine SHALL include the subtopic_id, question count (5–10 questions), estimated duration (computed as question count × 45 seconds), and a difficulty distribution determined by the user's mastery_score for that subtopic: mastery_score < 0.4 yields 60% easy / 30% medium / 10% hard, mastery_score 0.4–0.7 yields 30% easy / 50% medium / 20% hard, mastery_score > 0.7 yields 10% easy / 40% medium / 50% hard
4. WHEN generating a "new_content" item, THE Queue_Engine SHALL include the subtopic_id, lesson_id, section index, and estimated reading time (5 minutes per section as defined in the Time_Budget estimates)
5. THE Queue_Engine SHALL not place more than 2 consecutive items of the same type in the queue; IF fewer than 2 item types are available for the session, THEN THE Queue_Engine SHALL place all available items sequentially without applying the variety constraint

### Requirement 6: Session Length Preferences

**User Story:** As a CSE examinee, I want to set my preferred daily study time, so that the system respects my schedule constraints.

#### Acceptance Criteria

1. THE Queue_Engine SHALL accept a Time_Budget preference of 15, 30, or 60 minutes per user, stored as a user setting
2. IF a user has not set a Time_Budget, THEN THE Queue_Engine SHALL default to 30 minutes
3. WHEN a user updates their Time_Budget, THE Queue_Engine SHALL regenerate the current day's queue if no item in that queue has been marked as completed; IF at least one item has been marked as completed, THEN THE Queue_Engine SHALL apply the new Time_Budget starting from the next day's queue generation
4. THE Queue_Engine SHALL return the total estimated duration in minutes, the number of items remaining, and the number of items completed alongside the queue response
5. IF a user submits a Time_Budget value other than 15, 30, or 60, THEN THE Queue_Engine SHALL reject the request with a validation error indicating the accepted values

---

## Phase 3: Inline Question Explanations

### Requirement 7: Static Explanation Storage and Retrieval

**User Story:** As a CSE examinee, I want to see a detailed explanation immediately after answering a question, so that I understand why the correct answer is right without navigating away.

#### Acceptance Criteria

1. THE Explanation_Service SHALL store an explanation field per question containing: explanation_text (markdown text, 50–2000 characters), key_concept (the principle being tested, max 100 characters), and related_subtopics (array of subtopic IDs that share the same concept, maximum 10 entries)
2. WHEN a user submits an answer to a question, THE Explanation_Service SHALL include the explanation in the response payload regardless of whether the answer was correct or incorrect
3. THE Explanation_Service SHALL support markdown formatting in explanation_text including bold, italic, code blocks, and bullet lists
4. IF a question does not have an explanation stored, THEN THE Explanation_Service SHALL return a null explanation field rather than blocking the answer submission flow
5. THE Explanation_Service SHALL expose a bulk retrieval endpoint accepting an array of question IDs (minimum 1, maximum 50) and returning their explanations, for offline caching purposes
6. IF the bulk retrieval request contains question IDs that have no stored explanation, THEN THE Explanation_Service SHALL return a null explanation entry for each missing ID rather than rejecting the entire request
7. IF the bulk retrieval request contains an empty array or more than 50 question IDs, THEN THE Explanation_Service SHALL reject the request with a validation error indicating the allowed range of 1 to 50 IDs

### Requirement 8: AI Tutor Escalation

**User Story:** As a CSE examinee, I want to ask follow-up questions when an explanation is not enough, so that I can resolve confusion without leaving the question context.

#### Acceptance Criteria

1. WHEN a user triggers the "Still confused? Ask why" action on an explanation, THE Explanation_Service SHALL forward the question context (question text, correct answer, explanation, user's answer) to the existing Tutor service
2. THE Explanation_Service SHALL pass the question's subtopic_id and key_concept to the Tutor service as context parameters so the tutor response is scoped to the relevant topic
3. THE Explanation_Service SHALL rate-limit AI Tutor escalations to 20 per user per day
4. IF the user has exceeded the daily AI Tutor escalation limit, THEN THE Explanation_Service SHALL return an error indicating the limit has been reached and suggest reviewing the lesson for the relevant subtopic

### Requirement 9: Offline Explanation Caching

**User Story:** As a CSE examinee studying without internet, I want explanations available offline, so that I can still learn from my mistakes when disconnected.

#### Acceptance Criteria

1. WHEN the frontend loads a quiz or study session, THE Explanation_Service bulk endpoint SHALL be called to prefetch explanations for all questions in the session
2. THE Explanation_Service SHALL return explanations with a cache_version field (integer, incremented on content update) so the frontend can determine if its cached copy is stale
3. THE Explanation_Service SHALL support conditional requests using If-None-Match headers with the cache_version, returning 304 Not Modified when the cached version is current
4. WHEN the frontend is offline, THE Explanation_Service cached data in IndexedDB SHALL be used to display explanations without network requests

---

## Phase 4: Post-Mock Exam Analytics

### Requirement 10: Diagnostic Breakdown

**User Story:** As a CSE examinee, I want a detailed diagnostic after each mock exam, so that I know exactly which subtopics cost me the most points.

#### Acceptance Criteria

1. WHEN a user completes a mock exam, THE Mock_Analytics_Engine SHALL generate a Diagnostic_Report containing: total_score (percentage correct, rounded to one decimal place), per-subtopic breakdown (subtopic_id, questions_attempted, questions_correct, points_lost where each incorrect answer equals 1 point lost), and time_per_subtopic (average seconds per question by subtopic, excluding any question answered in fewer than 2 seconds or more than 600 seconds)
2. WHEN a Diagnostic_Report is generated, THE Mock_Analytics_Engine SHALL rank subtopics by points_lost descending and return up to 5 as "highest impact areas"; IF fewer than 5 subtopics have points_lost greater than 0, THEN THE Mock_Analytics_Engine SHALL return only those subtopics with points_lost greater than 0
3. WHEN a Diagnostic_Report is generated, THE Mock_Analytics_Engine SHALL compare the current exam's per-subtopic accuracy against the user's historical average accuracy for each subtopic and flag subtopics that declined by more than 15 percentage points as "regression alerts"; IF the user has no prior exam history for a subtopic, THEN THE Mock_Analytics_Engine SHALL omit that subtopic from regression analysis
4. THE Mock_Analytics_Engine SHALL compute difficulty distribution performance: percentage correct at each difficulty level (easy, medium, hard) for the exam overall and per subtopic
5. WHEN a Diagnostic_Report is generated, THE Mock_Analytics_Engine SHALL persist the report with: user_id, mock_exam_id, generated_at timestamp, and all computed fields, so that users can retrieve past diagnostic reports

### Requirement 11: Predicted Score Range

**User Story:** As a CSE examinee, I want to know my predicted score range for the actual exam, so that I can set realistic expectations and identify how much improvement is needed.

#### Acceptance Criteria

1. WHEN a user has completed at least 2 mock exams, THE Mock_Analytics_Engine SHALL compute a predicted score range using: the weighted average of mock exam scores (recency-weighted per Requirement 1 criterion 4), adjusted by the user's current FSRS retention state (average retention_score across studied flashcards)
2. THE Mock_Analytics_Engine SHALL express the prediction as a range: lower_bound (predicted score minus standard deviation of mock scores, minimum 0), upper_bound (predicted score plus half standard deviation, maximum 100), and midpoint (the weighted average)
3. IF the user has completed fewer than 2 mock exams, THEN THE Mock_Analytics_Engine SHALL return a null predicted_score_range with a message indicating more mock exams are needed for prediction
4. THE Mock_Analytics_Engine SHALL include a confidence_level field: "low" (2–3 exams), "medium" (4–6 exams), "high" (7+ exams)

### Requirement 12: Actionable Recommendations

**User Story:** As a CSE examinee, I want specific recommendations after a mock exam telling me what to fix and how many points I can gain, so that I have a clear action plan.

#### Acceptance Criteria

1. WHEN a Diagnostic_Report is generated, THE Mock_Analytics_Engine SHALL produce up to 5 actionable recommendations, each containing: subtopic_name, current_accuracy (percentage), target_accuracy (80%), estimated_point_gain (computed as questions_in_exam_from_subtopic × (target_accuracy − current_accuracy) / 100), and recommended_action ("review", "practice", or "re-learn" based on current mastery level)
2. THE Mock_Analytics_Engine SHALL sort recommendations by estimated_point_gain descending
3. WHEN a user views recommendations, THE Mock_Analytics_Engine SHALL format them as human-readable strings (e.g., "Fix Ratio & Proportion and Verb Tenses to gain +9 points")
4. WHEN a user accepts a recommendation, THE Mock_Analytics_Engine SHALL feed the recommended subtopics into the Queue_Engine as high-priority items for the next daily queue generation
5. THE Mock_Analytics_Engine SHALL persist recommendations with the Diagnostic_Report so users can review past recommendations

---

## Phase 5: Competence-Based Gamification

### Requirement 13: Competence Milestones

**User Story:** As a CSE examinee, I want achievements tied to real exam competence rather than generic activity, so that earning them means I am genuinely improving.

#### Acceptance Criteria

1. THE Competence_Milestone system SHALL define milestones tied to exam structure: "Verbal Mastery" (all 23 verbal subtopics with mastery_score ≥ 0.8), "Numerical Mastery" (all 24 numerical subtopics with mastery_score ≥ 0.8), "Analytical Mastery" (all 13 analytical subtopics with mastery_score ≥ 0.8), "Full Spectrum" (all 60 subtopics with mastery_score ≥ 0.8)
2. THE Competence_Milestone system SHALL define readiness milestones: "Exam Ready: Sub-Professional" (readiness score ≥ 70 at end-of-day snapshot for 7 consecutive calendar days), "Exam Ready: Professional" (readiness score ≥ 80 at end-of-day snapshot for 7 consecutive calendar days), where the end-of-day snapshot is the last computed readiness score on each calendar day (UTC)
3. THE Competence_Milestone system SHALL define recovery milestones: "Comeback" (any subtopic recovered from mastery_score < 0.5 to mastery_score ≥ 0.8 within 14 calendar days, measured from the date the mastery_score was last recorded below 0.5), "Resilient Learner" (3 separate Comeback milestones achieved on 3 distinct subtopics)
4. WHEN a user's mastery data or readiness score changes, THE Competence_Milestone system SHALL evaluate all unearned milestones and award any that are newly satisfied
5. THE Competence_Milestone system SHALL persist milestone awards with: user_id, milestone_id, awarded_at timestamp, and the triggering metric values at time of award
6. THE Competence_Milestone system SHALL treat awarded milestones as permanent — once earned, a milestone SHALL NOT be revoked even if the user's metrics subsequently drop below the threshold
7. THE Competence_Milestone system SHALL expose an endpoint returning all milestones with their status: "locked" (no qualifying progress), "in_progress" (with percentage computed as: for mastery milestones, count of qualifying subtopics divided by total required; for readiness milestones, consecutive qualifying days divided by 7; for recovery milestones, count of Comeback awards divided by 3), or "earned" (with awarded_at date)
8. WHEN a user requests their milestone status, THE Competence_Milestone system SHALL return the response within 2 seconds

### Requirement 14: Study Consistency Metric

**User Story:** As a CSE examinee, I want my streak to reflect meaningful study behavior rather than just opening the app, so that maintaining it requires genuine effort.

#### Acceptance Criteria

1. THE Study_Consistency metric SHALL increment when a user completes at least 50% of their daily queue items (by count) on a given day
2. THE Study_Consistency metric SHALL NOT increment from merely logging in or opening the app without completing queue items
3. WHEN a user misses a day (does not meet the 50% threshold), THE Study_Consistency metric SHALL reset the current streak count to 0 but preserve the longest_streak historical record
4. THE Study_Consistency metric SHALL store: current_streak (consecutive qualifying days), longest_streak (all-time maximum), total_consistent_days (lifetime count of qualifying days), and last_qualifying_date
5. WHEN a user misses a day, THE Queue_Engine SHALL adjust the next day's queue to include catch-up items from the missed day's FSRS-due cards, rather than penalizing the user with a broken streak notification
6. THE Study_Consistency metric SHALL replace the existing streak logic in the gamification feature for users who have opted into the intelligent learning engine

### Requirement 15: Gamification Migration

**User Story:** As a CSE examinee, I want the transition from XP-based to competence-based gamification to preserve my existing progress, so that I do not lose recognition for past effort.

#### Acceptance Criteria

1. WHEN the competence-based gamification system activates for a user, THE Competence_Milestone system SHALL retroactively evaluate all milestones against the user's existing mastery data and award any that are already satisfied
2. THE Competence_Milestone system SHALL coexist with the existing XP system — XP continues to be earned from study activities, but milestones replace generic achievements as the primary progression indicator
3. THE Competence_Milestone system SHALL map existing achievement badges to competence milestones where applicable and preserve the original awarded_at date for retroactively matched milestones

---

## Phase 6: Exam Date Onboarding

### Requirement 16: Exam Date Capture

**User Story:** As a new CSE examinee, I want the platform to ask me when my exam is during my first session, so that everything is personalized from day one.

#### Acceptance Criteria

1. WHEN a user completes registration and logs in for the first time, THE Onboarding_Engine SHALL present an exam date capture flow before showing the main dashboard
2. THE Onboarding_Engine SHALL accept: exam_date (required, must be a future date between 1 and 365 calendar days from today inclusive), exam_category (Professional or Sub-Professional, required), and preferred Time_Budget (15, 30, or 60 minutes, optional, defaults to 30)
3. IF the user submits an exam_date that is in the past or more than 365 days from today, or omits a required field (exam_date or exam_category), THEN THE Onboarding_Engine SHALL reject the submission and return a validation error indicating which field failed and why
4. WHEN the user submits valid onboarding data, THE Onboarding_Engine SHALL create a StudyPlan record containing: target_exam_date, exam_category, and available_hours_per_day computed as Time_Budget divided by 60 (yielding 0.25, 0.5, or 1.0 hours)
5. IF a user skips the exam date capture, THEN THE Onboarding_Engine SHALL allow access to the dashboard but display a prompt to set an exam date on every dashboard load until one is configured
6. IF the submitted exam_date is fewer than 7 days from today, THEN THE Onboarding_Engine SHALL accept the submission but include a warning field in the response indicating the study plan will be compressed

### Requirement 17: Personalized Plan Generation

**User Story:** As a new CSE examinee, I want a study plan generated immediately after I set my exam date, so that I know what to study from day one.

#### Acceptance Criteria

1. WHEN a user sets their exam date, THE Onboarding_Engine SHALL generate a StudyPlan with daily tasks distributed across the available days, prioritizing: Coverage_Gap subtopics first (ensuring all 60 subtopics are introduced), then deepening weak areas, then review and mock exam practice in the final 20% of the timeline
2. THE Onboarding_Engine SHALL distribute subtopics across the plan timeline using a spaced introduction pattern: no more than 3 new subtopics per day, with review days interspersed every 3 study days
3. THE Onboarding_Engine SHALL allocate mock exam practice sessions at regular intervals: one per week starting from the second week, increasing to twice per week in the final 2 weeks before the exam
4. WHEN the plan is generated, THE Onboarding_Engine SHALL return a plan summary containing: total_days, subtopics_per_week, mock_exams_scheduled, and estimated_readiness_at_exam (projected readiness score based on plan completion)
5. IF the user already has mastery data (returning user setting a new exam date), THEN THE Onboarding_Engine SHALL skip already-mastered subtopics (mastery_score ≥ 0.8) and allocate their time slots to weaker areas

### Requirement 18: Exam Date Updates

**User Story:** As a CSE examinee, I want to update my exam date if it changes, so that my study plan adjusts accordingly.

#### Acceptance Criteria

1. WHEN a user updates their exam_date, THE Onboarding_Engine SHALL regenerate the StudyPlan from the current date forward, preserving completed days and redistributing remaining subtopics across the new timeline
2. THE Onboarding_Engine SHALL recalculate the Queue_Engine urgency parameters based on the new days-until-exam value
3. IF the new exam date is earlier than the original, THEN THE Onboarding_Engine SHALL compress the remaining plan and increase daily study intensity (more items per day) while respecting the Time_Budget cap
4. IF the new exam date is later than the original, THEN THE Onboarding_Engine SHALL add additional review cycles and mock exam sessions to fill the extended timeline
5. WHEN the exam date is updated, THE Readiness_Engine SHALL recompute the retention component using the new projection date
