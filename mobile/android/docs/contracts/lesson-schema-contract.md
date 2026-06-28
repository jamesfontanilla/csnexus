# Lesson Schema Versioning And Native Block Contract

Status: confirmed native contract for the current lesson renderer behavior. The native mapper already handles unknown block types safely and the contract is now pinned by fixture-backed tests.

## Goals

- Let Android render server-driven lessons without WebView.
- Keep cached lessons fresh through version metadata.
- Provide safe behavior for unknown block types.
- Preserve formatting nuance from the web lesson reader.

## Lesson Response

Recommended fields:

```json
{
  "id": 1001,
  "subtopic_id": 42,
  "status": "published",
  "schema_version": 2,
  "content_version": "2026-06-08T00:00:00Z",
  "etag": "lesson-1001-v2",
  "content_json": {}
}
```

Android cache freshness should use `schema_version`, `content_version`, `updated_at`, `etag`, or a content hash. At least one stable freshness field is required.

Android stores the freshness fields on the lesson model and cache entry so the app can compare future payloads against the cached version without parsing the full lesson body.

## Supported Block Types

| Block type | Native renderer requirement |
| --- | --- |
| `prose` | Rich text/Markdown-compatible text with accessible reading order. |
| `table` | Horizontally scrollable table with header semantics and summary fallback. |
| `code` | Monospace block, horizontal scroll, language label if present. |
| `formula` | Monospace/math renderer or accessible fallback text. |
| `tip` | Informational callout. |
| `warning` | Warning callout. |
| `example` | Expandable or clearly framed example. |
| `step_by_step` | Ordered step renderer. |
| `list` | Ordered/unordered list renderer. |
| `svg` | Sanitized diagram renderer or image alternative with content description. |
| `check_understanding` | Inline check list with answer/reveal/feedback behavior. |

Lesson sections may also include optional `subsections` entries. These reuse the same section shape, preserve deeper lesson headings, and remain safe for clients that still render only the top-level `sections` array.

The parser may also emit:

- `learning_objectives`: a flat list of the lesson's stated objectives.
- `guided_session`: a card-oriented outline with `objective`, `must_know`, and `steps` so mobile can render a bite-sized guided flow.

Sanitization rules:

- `formula` blocks are rendered as inert text/monospace content. Android does not execute formula markup.
- `svg` blocks are never executed as raw XML. Android treats them as inert media text and only surfaces the fallback text or a safe image alternative if the backend provides one.
- If the backend supplies diagram source text, the renderer must keep it read-only and non-interactive.

## Unknown Block Fallback

Unknown blocks should not crash or disappear silently. Recommended representation:

```json
{
  "type": "new_block_type",
  "content": {},
  "fallback_text": "This activity is available in the web app until Android support is added.",
  "requires_client_capability": "new_block_type"
}
```

Android behavior:

- Show `fallback_text` if present.
- Log redacted block type and lesson ID.
- Mark the Parity_Matrix/backend gap if a user-visible block is unsupported.

## Verification

- `mobile/android/app/src/test/java/com/csnexus/app/feature/content/data/ContentMappersTest.kt`
- `mobile/android/app/src/main/java/com/csnexus/app/feature/content/data/ContentMappers.kt`

## Completion And Inline Checks

Lesson completion remains server-authoritative through `POST /v1/subtopics/{subtopicId}/lesson:complete`.

Inline checks need one of these explicit rules:

- Reveal-only: no server persistence, no progress effect.
- Persisted answer: backend endpoint records answer/feedback.
- Gated segment: answer state controls segment progression.

Current Android behavior is:

- Standalone `check_understanding` blocks are reveal-only and are not persisted to the server.
- Segmented lessons may gate local segment advancement until at least one inline check in the segment has been revealed.
- Check reveal state is local to the lesson session and resets on reload.
