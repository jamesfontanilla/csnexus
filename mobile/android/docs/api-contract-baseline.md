# Web API Contract Baseline For Native Android

Baseline source: static scan of `web/src/api`, `web/src/pages`, `web/src/components`, and `web/src/sw` on 2026-06-08.

This document maps the web endpoint surface that the native app must preserve through typed DTOs, repositories, auth handling, and contract tests.

## Client Behavior

- API base URL is `import.meta.env.VITE_API_URL || ""`.
- Requests attach `Authorization: Bearer <token>` when `getToken()` returns a token.
- Requests send JSON bodies and expect JSON responses except HTTP 204.
- Error envelopes handled by web:
  - `{ "error": { "message": "...", "code": "..." } }`
  - FastAPI 422 `{ "detail": [{ "msg": "...", "loc": [...] }] }`
  - String detail `{ "detail": "..." }`
- Web captures `X-Request-ID`.
- Web logs out and redirects to `/login` on 401.
- Web client code still does not use refresh tokens directly, but the backend now exposes a native-facing refresh-token contract.

## Auth And Account

| Method | Endpoint | Web usage | Native notes |
| --- | --- | --- | --- |
| POST | `/v1/auth/sessions` | Email/password login | Returns access token, refresh token, token type, and expiry metadata for native clients. |
| POST | `/v1/auth/sessions:refresh` | Native refresh-token rotation | Returns a fresh access token and refresh token pair. |
| DELETE | `/v1/auth/sessions/me` | Logout | Clear encrypted token store and back stack. |
| GET | `/v1/auth/me` | Profile/settings current user | Source of truth for user profile and role if included. |
| POST | `/v1/auth/signups` | Signup | Native signup and OTP handoff. |
| POST | `/v1/auth/email-verifications` | OTP email verification | May return token after signup verification. |
| POST | `/v1/auth/password-reset-requests` | Forgot password | Start reset flow. |
| POST | `/v1/auth/password-resets` | OTP password reset | Reset password with OTP token/code. |
| POST | `/v1/auth/password-change` | Settings password change | Requires old/new password validation. |
| POST | `/v1/auth/google` | Browser Google ID token exchange | Android needs native Google credential and confirmed Android OAuth client ID. |
| PATCH | `/v1/users/me` | Profile update | Server-owned profile settings. |
| DELETE | `/v1/users/me` | Delete account | Destructive confirmation. |
| GET | `/v1/users/usernames:check?username=...` | Username availability | Debounced validation. |

## Content And Lessons

| Method | Endpoint | Web usage |
| --- | --- | --- |
| GET | `/v1/modules` | Module list |
| GET | `/v1/modules/{moduleId}/topics` | Topic list |
| GET | `/v1/topics/{topicId}/subtopics` | Subtopic list |
| GET | `/v1/subtopics/{subtopicId}/lesson` | Lesson reader |
| POST | `/v1/subtopics/{subtopicId}/lesson:complete` | Lesson completion |
| POST | `/v1/tutor/lesson-chat` | Lesson chat/practice companion |
| POST | `/v1/tutor/interactions/{interactionId}:rate` | Rate tutor interaction |

Lesson schema types seen in web:

- `LessonResponse`: `id`, `subtopic_id`, `content_json`, `status`.
- `content_json.metadata`: title, estimated reading minutes, section count, practice counts, difficulty distribution, word count, optional segment count.
- `content_json.sections`: section title, typed blocks, difficulty, word count, estimated reading seconds.
- `ContentBlock.type`: prose, table, code, formula, tip, warning, example, step_by_step, list, svg, check_understanding.
- `segments`: grouped sections, estimated minutes, checks.

## Quiz, Mock Exam, And Explanations

| Method | Endpoint | Web usage |
| --- | --- | --- |
| POST | `/v1/topics/{scopeId}/quiz-attempts` | Start topic quiz |
| POST | `/v1/modules/{scopeId}/quiz-attempts` | Start module quiz |
| POST | `/v1/subtopics/{scopeId}/quiz-attempts` | Start subtopic quiz |
| PATCH | `/v1/quiz-attempts/{attemptId}/answers/{questionId}` | Persist quiz answer |
| POST | `/v1/quiz-attempts/{attemptId}:submit` | Submit quiz |
| POST | `/v1/quiz-attempts/{attemptId}/recall-answer?question_id={questionId}` | Recall answer |
| GET | `/v1/explanations/{questionId}` | Explanation |
| POST | `/v1/explanations/bulk` | Bulk explanations |
| POST | `/v1/explanations/{questionId}/:escalate` | Escalate explanation |
| POST | `/v1/explanations/{questionId}/note` | Personal note |
| GET | `/v1/notes` | Notes list |
| POST | `/v1/mock-exams/attempts` | Start mock exam |
| PATCH | `/v1/mock-exams/attempts/{attemptId}/answers/{questionId}` | Persist mock answer |
| POST | `/v1/mock-exams/attempts/{attemptId}:submit` | Submit mock exam |
| POST | `/v1/mock-exams/attempts/{attemptId}:report-focus-loss` | Report focus loss |
| GET | `/v1/mock-analytics/{attemptId}` | Mock diagnostic result |
| GET | `/v1/mock-analytics/{attemptId}/recommendations` | Result recommendations |
| POST | `/v1/mock-analytics/{attemptId}/recommendations/:accept` | Accept recommendation |
| GET | `/v1/mock-analytics/prediction` | Prediction |

## Progress, Analytics, Motivation

| Method | Endpoint | Web usage |
| --- | --- | --- |
| GET | `/v1/dashboard/me` | Dashboard |
| GET | `/v1/xp/me` | XP and level |
| GET | `/v1/achievements/me` | Achievements |
| GET | `/v1/mastery/me` | Mastery |
| GET | `/v1/mastery/me/weakest` | Weakest subtopics |
| GET | `/v1/mastery/me/reviews/due` | Due reviews |
| GET | `/v1/mastery/me/recommendations` | Mastery recommendations |
| GET | `/v1/progress/snapshot` | Progress snapshot |
| GET | `/v1/leaderboards/global` | Leaderboard |
| GET | `/v1/goals/me/today` | Daily goal |
| GET | `/v1/goals/me/weekly` | Weekly summary |
| PUT | `/v1/goals/me/target` | Update target XP |
| GET | `/v1/streak/me/freezes` | Freeze count |
| GET | `/v1/milestones` | Milestones |
| GET | `/v1/consistency` | Consistency metric |
| GET | `/v1/tournaments` | Tournament list |
| POST | `/v1/tournaments/{id}:join` | Join tournament |
| GET | `/v1/tournaments/{id}/leaderboard` | Tournament leaderboard |

## Readiness, Planner, Focus, Queue, Onboarding

| Method | Endpoint | Web usage |
| --- | --- | --- |
| GET | `/v1/readiness` | Current readiness |
| GET | `/v1/readiness/dashboard` | Readiness dashboard |
| GET | `/v1/readiness/trend` | Readiness trend |
| POST | `/v1/readiness/self-assessment` | Submit self-assessment |
| GET | `/v1/readiness/self-assessment/history` | Assessment history |
| GET | `/v1/readiness/self-assessment/prompt` | Assessment prompt |
| GET | `/v1/planner/readiness/me` | Planner readiness |
| GET | `/v1/planner/plans/me` | Study plan |
| GET | `/v1/planner/plans/me/today` | Today tasks |
| POST | `/v1/planner/plans` | Create study plan |
| POST | `/v1/planner/plans/me/tasks/{taskId}:complete` | Complete plan task |
| DELETE | `/v1/planner/plans/me` | Delete plan |
| GET | `/v1/focus/sessions/me/stats` | Focus stats |
| POST | `/v1/focus/sessions` | Start focus session |
| POST | `/v1/focus/sessions/{sessionId}:complete` | Complete focus session |
| POST | `/v1/focus/sessions/{sessionId}:abandon` | Abandon focus session |
| GET | `/v1/focus/wellness/me` | Wellness alert |
| GET | `/v1/queue` | Daily queue |
| POST | `/v1/queue/items/{itemId}/:complete` | Complete queue item |
| POST | `/v1/queue/:regenerate` | Regenerate queue |
| GET | `/v1/queue/preferences` | Queue preferences |
| PATCH | `/v1/queue/preferences` | Update queue preferences |
| GET | `/v1/queue/goodnight` | Goodnight session |
| POST | `/v1/queue/goodnight/:complete` | Complete goodnight session |
| POST | `/v1/onboarding` | Submit onboarding |
| PATCH | `/v1/onboarding/exam-date` | Update exam date |
| GET | `/v1/onboarding/plan-summary` | Plan summary |

## Flashcards

| Method | Endpoint | Web usage |
| --- | --- | --- |
| GET | `/v1/flashcards/decks` | Deck list |
| GET | `/v1/flashcards/decks/{id}` | Deck detail |
| POST | `/v1/flashcards/decks` | Create deck |
| PATCH | `/v1/flashcards/decks/{id}` | Update deck |
| DELETE | `/v1/flashcards/decks/{id}` | Delete deck |
| POST | `/v1/flashcards/decks/{id}/duplicate` | Duplicate deck |
| GET | `/v1/flashcards/decks/{deckId}/cards` | Deck cards |
| POST | `/v1/flashcards/decks/{deckId}/cards` | Create card |
| PATCH | `/v1/flashcards/decks/{deckId}/cards/{cardId}` | Update card |
| DELETE | `/v1/flashcards/decks/{deckId}/cards/{cardId}` | Delete card |
| POST | `/v1/flashcards/sessions` | Create study session |
| GET | `/v1/flashcards/sessions/{sessionId}/cards` | Session cards |
| POST | `/v1/flashcards/sessions/{sessionId}/respond` | Respond to card |
| POST | `/v1/flashcards/sessions/{sessionId}/end` | End session |
| GET | `/v1/flashcards/queue` | Review queue |
| GET | `/v1/flashcards/queue/summary` | Queue summary |
| GET | `/v1/flashcards/marketplace` | Marketplace |
| POST | `/v1/flashcards/marketplace/{id}/clone` | Clone marketplace deck |
| POST | `/v1/flashcards/marketplace/{id}/ratings` | Rate deck |
| GET | `/v1/flashcards/marketplace/{id}/ratings` | Ratings/comments legacy |
| POST | `/v1/flashcards/marketplace/{id}/bookmark` | Bookmark |
| DELETE | `/v1/flashcards/marketplace/{id}/bookmark` | Remove bookmark |
| GET | `/v1/flashcards/marketplace/{deckId}/comments` | Comments |
| POST | `/v1/flashcards/marketplace/{deckId}/comments` | Add comment |
| DELETE | `/v1/flashcards/comments/{commentId}` | Delete comment |
| GET | `/v1/flashcards/analytics/dashboard` | Analytics dashboard |
| GET | `/v1/flashcards/analytics/heatmap` | Heatmap |
| GET | `/v1/flashcards/recommendations` | Recommendations |
| POST | `/v1/flashcards/exam-simulations` | Create exam simulation |
| GET | `/v1/flashcards/exam-simulations/{examId}/cards` | Exam cards |
| POST | `/v1/flashcards/exam-simulations/{examId}/answer` | Exam answer |
| POST | `/v1/flashcards/exam-simulations/{examId}/complete` | Complete exam |
| GET | `/v1/flashcards/feed` | Social feed |
| POST | `/v1/flashcards/generate` | Generate cards |
| GET | `/v1/flashcards/admin/analytics` | Admin analytics |
| POST | `/v1/flashcards/admin/decks/{id}/:flag` | Flag deck |
| POST | `/v1/flashcards/admin/decks/{id}/:feature` | Feature deck |

## Admin

| Method | Endpoint | Web usage |
| --- | --- | --- |
| GET | `/v1/admin/analytics` | Admin dashboard analytics |
| GET | `/v1/admin/users?limit=50` | Admin user list |
| PATCH | `/v1/admin/users/{id}` | Ban/unban via `is_banned` |
| DELETE | `/v1/admin/users/{id}` | Delete user |

## Offline Sync Reference

Web service worker reference posts:

```json
{
  "events": [
    {
      "client_event_id": "string",
      "kind": "string",
      "client_timestamp": "string",
      "payload": {}
    }
  ]
}
```

to `POST /v1/progress:sync`.

Expected response:

```json
{
  "accepted": [{ "client_event_id": "string" }],
  "rejected": [{ "client_event_id": "string", "reason": "string" }]
}
```

Android still needs a stricter contract for idempotency, auth expiry, conflict handling, partial rejection, retry, and server reconciliation.
