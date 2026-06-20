# Idempotent Offline Sync Contract

Status: confirmed native contract for the current Android sync pipeline. The web service-worker shape informed the first pass, and the Android app now pins the accepted/rejected/conflict response shape with fixture coverage and WorkManager retry handling.

## Goals

- Queue only conflict-safe mutations while offline.
- Prevent duplicate progress from repeated retries.
- Preserve Backend_API as source of truth.
- Surface permanent failures and conflicts to the user.

## Event Identity

The native app uses one stable identity per queued mutation:

- `client_event_id` is the local event identifier and is stable for the lifetime of the queued event.
- `idempotency_key` is the server idempotency key used for deduplication.
- The current Android implementation derives the key as `<event_kind>:<sha256(payload_json)>` and reuses that same value as the local sync row ID.
- If the same payload is queued again, the key must remain identical so retries do not create duplicate server-side effects.

## Endpoint

`POST /v1/progress:sync`

Request:

```json
{
  "events": [
    {
      "client_event_id": "uuid",
      "idempotency_key": "uuid-or-stable-key",
      "kind": "lesson.completed",
      "client_timestamp": "2026-06-08T00:00:00Z",
      "payload_hash": "sha256",
      "payload": {
        "subtopic_id": 42,
        "lesson_id": 1001
      }
    }
  ]
}
```

Response:

```json
{
  "accepted": [
    {
      "client_event_id": "uuid",
      "server_event_id": "server-id",
      "server_state": {}
    }
  ],
  "rejected": [
    {
      "client_event_id": "uuid",
      "reason": "invalid_payload",
      "retryable": false
    }
  ],
  "conflicts": [
    {
      "client_event_id": "uuid",
      "reason": "stale_client_state",
      "server_state": {}
    }
  ]
}
```

Auth-expired behavior:

- If the sync request returns `401` or `403`, Android keeps the event in `failed` state, stops treating protected sync as ready, and requires the user to sign back in before retrying.
- A refresh failure does not discard the queued event.

## Event Allow-List

| Event kind | Offline queue allowed? | Notes |
| --- | --- | --- |
| `lesson.completed` | yes, if idempotent | Server response must confirm completion. |
| `lesson.inline_check_answered` | yes, if backend persists checks | Needs check ID and answer semantics. |
| `flashcard.card_reviewed` | yes, if idempotent | Must not double-advance spaced repetition. |
| `flashcard.session_ended` | yes, if idempotent | Server should reconcile card responses. |
| `focus.session_completed` | yes, if idempotent | Timer data must include server validation rules. |
| `goal.target_updated` | maybe | Prefer online unless rollback semantics are clear. |
| `settings.updated` | maybe | Queue only server-owned settings with conflict response. |
| `quiz.answer_saved` | no by default | Active quizzes should be online unless backend explicitly supports offline attempts. |
| `quiz.submitted` | no by default | Final scoring must be server-authoritative. |
| `mock_exam.submitted` | no by default | High-stakes timed submission should not queue unless backend explicitly supports it. |

Current Android allow-list:

- `lesson.completed`
- `flashcard.card_reviewed`
- `flashcard.session_ended`
- `focus.session_completed`
- `goal.target_updated`
- `settings.updated`

Current Android deny-list:

- `quiz.answer_saved`
- `quiz.submitted`
- `mock_exam.submitted`

## Android Sync Behavior

1. Store events in Room with status, idempotency key, payload hash, attempt count, user ID, created timestamp, and last error.
2. Use WorkManager with network constraints and exponential backoff.
3. Attach access token through normal auth path.
4. If access token is expired, refresh through SessionManager before sync.
5. If refresh fails, pause protected sync until login.
6. Remove accepted events only after server acknowledgment.
7. Keep rejected non-retryable events visible until user dismisses or resolves them.
8. Preserve server state on conflicts.

## Response Semantics

- `accepted` items remove the matching queued event from local storage once the server acknowledges them.
- `rejected` items stay visible with the server-provided reason and are only retried if the server marks them retryable.
- `conflicts` items stay visible with the server state attached so the user can resolve the mismatch before retrying.
- If the response omits a category, treat it as empty rather than an error.

## Verification Notes

- `mobile/android/docs/contracts/fixtures/progress-sync-mixed-response.json`
- `mobile/android/app/src/test/java/com/csnexus/app/core/contracts/ApiContractFixtureTest.kt`
- `mobile/android/app/src/test/java/com/csnexus/app/core/sync/OfflineSyncTest.kt`

## Mock Fixture

- `mobile/android/docs/contracts/fixtures/progress-sync-mixed-response.json`
