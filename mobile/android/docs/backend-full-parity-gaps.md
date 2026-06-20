# Backend Full Parity Gap Register

This register tracks backend or configuration contracts needed before native Android full parity can be certified.

## Auth And Session

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Refresh-token endpoint not confirmed | Android cannot safely keep users signed in after access-token expiry. | Endpoint for refresh, token rotation behavior, expiry, replay/revoke handling, and failure codes. | complete |
| Login response refresh token not confirmed | Native token store cannot persist a refresh token. | `POST /v1/auth/sessions` should return access token, refresh token, token type, expiry, and optionally user/session metadata. | complete |
| Native Google OAuth client ID not configured in repo docs | Android Google sign-in cannot be completed safely. | Google Cloud Android OAuth client ID, package name, SHA-1/SHA-256 fingerprints, and backend accepted audience. | open |
| Google account linking behavior ambiguous | Native cannot handle existing email and linked Google account states correctly. | Backend response codes for new account, linked existing account, unverified email, email conflict, and rejected token. | open |

## Offline Sync

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| `/v1/progress:sync` idempotency semantics need confirmation | WorkManager could duplicate progress if retries race. | Idempotency guarantee keyed by `client_event_id` or explicit idempotency key. | complete |
| Offline mutation allow-list not defined | Native might queue unsafe operations. | Allow/deny list for lesson completion, inline checks, flashcard study, focus sessions, goals, settings, quiz submit, and mock exam submit. | complete |
| Conflict resolution response shape not defined | Android cannot explain conflicts or preserve server authority cleanly. | Response shape for accepted, rejected, conflict, stale, unauthorized, and permanently invalid events. | complete |
| Auth-expired sync behavior not defined | Pending work may fail silently after refresh failure. | Standard 401/403 response and retry-after-login policy. | complete |

## Lesson Content

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Lesson schema version metadata not confirmed | Android cannot know whether cached lessons are stale. | Version, updated timestamp, ETag, or content hash per lesson. | complete |
| Unknown lesson block fallback not defined | New server-driven content might be invisible or crash native rendering. | Supported block registry and unknown-block payload/fallback rules. | complete |
| Formula/SVG security rules not defined | Native needs safe rendering strategy for formulas and diagrams. | Allowed markup/schema, sanitization expectations, and accessibility fallback text. | complete |
| Inline check persistence unclear | Native cannot know whether reveal/check state affects progress. | Endpoint or schema rule for check answer, feedback, retry, and completion impact. | complete |

## Admin

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Role model not documented for native route gating | Android cannot safely hide admin routes without knowing role fields. | User role/permissions in `/v1/auth/me` or dedicated permissions endpoint. | complete |
| Admin audit metadata not documented | Native cannot display or log admin action results consistently. | Response fields for action actor, target, timestamp, request ID, and audit ID where available. | open |
| Flashcard admin moderation actions sparse | Native cannot implement full admin workflow beyond analytics/flag/feature. | Full list of admin flashcard moderation endpoints and state transitions. | open |

## Flashcards

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Offline study event sync not confirmed | Android cannot queue flashcard responses safely. | Idempotent event sync for session response and session end, including duplicate handling. | open |
| Generation queue behavior unclear | Native cannot show polished pending/progress states if generation is long-running. | Job ID, polling/subscription endpoint, status values, cancel/retry behavior. | open |
| Marketplace ownership and moderation states need schema confirmation | Native cannot consistently show clone/bookmark/rating/admin affordances. | Deck ownership, cloned source, featured, flagged, hidden, rating, comment, and permission fields. | open |

## Settings And Profile

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Server-owned versus local-only settings not documented | Native and web settings could drift. | Matrix of settings stored in Backend_API versus local client only. | complete |
| Study preferences endpoint unclear | Android cannot sync daily study preferences unless backend owns them. | Endpoint and schema for daily goal, quiz mode preference, reminders, accessibility/theme if cross-platform. | complete |
| Optimistic rollback behavior not standardized | Native settings UI could show saved values the server rejected. | Validation error shape and canonical response after settings mutation. | complete |

## Tutor And AI Flows

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Tutor streaming support not confirmed | Native cannot implement streaming response parity. | Decide non-streaming only or provide SSE/WebSocket/streaming HTTP contract. | complete |
| Tutor privacy/redaction policy not documented | Diagnostics may capture sensitive prompts or answers. | Logging and analytics redaction rules for tutor requests and responses. | complete |
| Lesson-context payload schema needs confirmation | Native lesson tutor may send incomplete context. | Required lesson/subtopic/module/question context fields for `/v1/tutor/lesson-chat` and `/v1/tutor/{action}`. | complete |

## Analytics And Charts

| Gap | Impact | Required contract | Status |
| --- | --- | --- | --- |
| Chart accessibility summaries not returned by backend | Native must derive summaries locally or request backend summaries. | Decide local derivation or add server-provided chart summary fields. | complete |
| Time range and filter contracts vary by screen | Native cannot create consistent filter UI across analytics. | Standard query params and response metadata for date ranges, filters, and empty states. | complete |
