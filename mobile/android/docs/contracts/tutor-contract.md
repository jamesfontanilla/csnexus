# Native Tutor Lesson-Chat Contract

Status: confirmed native contract for the current Android tutor surface.

## Goals

- Keep the lesson companion usable without a WebView.
- Send enough lesson context for grounded tutor replies.
- Preserve privacy by redacting message content from diagnostics.
- Keep backward compatibility with older `context_json` behavior on the backend.
- Use a non-streaming request/response contract only; Android does not require SSE/WebSocket streaming for the current tutor surface.

## Request Shape

`POST /v1/tutor/lesson-chat`

Recommended Android request:

```json
{
  "message": "Explain this line",
  "context": "lesson-42",
  "subtopic_id": 42,
  "active_section_index": 2,
  "history": [
    { "role": "user", "content": "Can you explain this?" },
    { "role": "assistant", "content": "Sure." }
  ]
}
```

## Response Shape

Current Android contract accepts the existing tutor response envelope:

```json
{
  "interaction_id": 123,
  "response_text": "Here is the explanation...",
  "detected_intent": "lesson_chat",
  "response": "legacy fallback",
  "answer": "legacy fallback"
}
```

Android resolves `response_text`, then `response`, then `answer`.

## Lesson Context

The lesson companion sends the minimal structured context needed for grounded replies:

- `context`: lesson identifier or scope tag
- `subtopic_id`: numeric subtopic id when available
- `active_section_index`: currently visible section/segment index
- `history`: rolling recent turns, ordered oldest to newest

If the backend adds more tutor-specific context fields later, Android should treat them as optional and preserve backward compatibility with the existing payload.

## Privacy Rules

- Do not log raw tutor prompts or history entries in diagnostics.
- Redact `message`, `history`, and similar content-bearing fields.
- Keep request IDs, endpoint names, and error codes visible for debugging.
- Treat lesson-chat transcripts as sensitive learner content.

## Verification

- `mobile/android/app/src/test/java/com/csnexus/app/core/contracts/ApiContractFixtureTest.kt`
- `mobile/android/app/src/test/java/com/csnexus/app/core/logging/DiagnosticsPolicyTest.kt`
- `mobile/android/app/src/main/java/com/csnexus/app/feature/tutor/data/TutorApi.kt`
- `mobile/android/app/src/main/java/com/csnexus/app/feature/tutor/data/TutorRepository.kt`
