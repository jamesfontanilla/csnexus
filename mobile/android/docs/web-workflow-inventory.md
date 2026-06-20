# Web Workflow Inventory For Native Android Parity

Source files scanned on 2026-06-08:

- `web/src/App.tsx`
- `web/src/pages/**`
- `web/src/components/**`
- `web/src/api/**`
- `web/src/stores/**`
- `web/src/sw/sync.ts`

## App Shell

- Public routes: `/`, `/login`, `/signup`, `/forgot-password`, `/verify-otp`.
- Protected routes use `AuthGuard`, which redirects unauthenticated users to `/login`.
- `AnimatePresence` wraps route changes with wait-mode transitions.
- The shell switches between `DesktopAppShell` and mobile `GlassNavbar` using `useBreakpoint`.
- Desktop shell includes sidebar/detail panel concepts, command palette items, focus mode entry/exit, breadcrumbs, recent pages, and keyboard-oriented quick actions.
- Mobile shell uses navbar-oriented navigation and the same routes.
- Unknown routes redirect to `/`.

## Auth Workflows

- Login posts email/password to `POST /v1/auth/sessions`, receives `access_token`, stores it in `localStorage`, and navigates to the authenticated app.
- Signup posts to `POST /v1/auth/signups`, then hands off to OTP verification.
- OTP verification supports email verification through `POST /v1/auth/email-verifications` and password reset through `POST /v1/auth/password-resets`.
- Forgot password starts with `POST /v1/auth/password-reset-requests`.
- Google sign-in is browser-based and posts an ID token to `POST /v1/auth/google`.
- Auth state is stored under `cse_auth_state` in `localStorage`.
- API 401 handling logs out and redirects to `/login`.
- No web refresh-token flow was found.

## Content And Lesson Workflows

- Modules load from `GET /v1/modules`.
- Topics load from `GET /v1/modules/{moduleId}/topics`.
- Subtopics load from `GET /v1/topics/{topicId}/subtopics`.
- Lessons load from `GET /v1/subtopics/{subtopicId}/lesson`.
- Lesson completion posts to `POST /v1/subtopics/{subtopicId}/lesson:complete`.
- Lesson content uses `content_json` with legacy fields and enhanced typed sections.
- Supported lesson block types include prose, table, code, formula, tip, warning, example, step_by_step, list, svg, and check_understanding.
- Segmented lessons include `segments`, segment indexes, estimated minutes, and comprehension checks.
- Lesson companion panels include lesson chat and practice interactions through `/v1/tutor/lesson-chat`.

## Quiz And Exam Workflows

- Quiz route has `scope` and `scopeId` route params.
- Supported quiz scopes are topic, module, and subtopic.
- Attempt creation posts to `/v1/topics/{id}/quiz-attempts`, `/v1/modules/{id}/quiz-attempts`, or `/v1/subtopics/{id}/quiz-attempts`.
- Answer persistence patches `/v1/quiz-attempts/{attemptId}/answers/{questionId}`.
- Submit posts to `/v1/quiz-attempts/{attemptId}:submit`.
- Web quiz states include select-mode, in-progress, submitted, and lesson-blocked behavior.
- Mock exam starts with `POST /v1/mock-exams/attempts`.
- Mock exam answers patch `/v1/mock-exams/attempts/{attemptId}/answers/{questionId}`.
- Mock exam submits through `POST /v1/mock-exams/attempts/{attemptId}:submit`.
- Mock exam reports focus loss through `POST /v1/mock-exams/attempts/{attemptId}:report-focus-loss`.
- Mock exam results use mock analytics endpoints for diagnostics, recommendations, and predictions.

## Progress, Analytics, And Motivation

- Dashboard uses `GET /v1/dashboard/me`.
- Analytics uses XP, mastery, weakest subtopics, and progress snapshot endpoints.
- Mastery uses mastery list, due reviews, and recommendations.
- Readiness has both planner readiness and richer readiness API helpers.
- Goals use daily goal, weekly summary, streak freezes, and target update endpoints.
- Leaderboard uses global leaderboards.
- Tournaments use tournament list, join, and tournament leaderboard endpoints.
- Milestones use milestones and consistency endpoints.
- Study plan uses planner plan, today tasks, create plan, complete task, and delete plan endpoints.
- Focus uses focus stats, session create, completion, abandon, and wellness endpoints.
- Queue uses daily queue, complete item, regenerate, and queue preferences endpoints.
- Onboarding uses onboarding submit, exam date update, and plan summary endpoints.

## Flashcard Workflows

- Deck list, deck detail, create deck, duplicate deck, update deck, delete deck.
- Card list, create card, update card, delete card.
- Study session create, session cards, card response, session end.
- Review queue and queue summary.
- Marketplace list, clone, ratings, comments, bookmarks.
- Analytics dashboard, heatmap, and recommendations.
- Exam simulation create, cards, answer, and complete.
- Social feed.
- Card generation.
- Flashcard admin analytics, flag deck, and feature deck.

## Admin Workflows

- Admin dashboard loads analytics and users.
- Admin user management supports search/list, ban/unban through patching `is_banned`, and delete.
- Flashcard admin exposes admin analytics and deck flag/feature actions.
- Web routes wrap admin pages in `AuthGuard`; explicit route-level admin gating was not found in `App.tsx`.
- Native Android must add role-aware route gating and confirmation dialogs for destructive actions.

## Local And Offline Behavior

- Auth token is stored in `localStorage`.
- Accessibility and feedback preferences use typed `localStorage` helpers.
- Focus timer state is persisted in `localStorage`.
- Onboarding skip is stored as `cse_onboarding_skipped`.
- Command palette recent pages use `sessionStorage`.
- Service worker sync reference drains pending events and posts to `/v1/progress:sync` with `client_event_id`, `kind`, `client_timestamp`, and `payload`.
- Android should translate these local concerns to encrypted storage, DataStore, Room, and WorkManager as appropriate.

