# Native Android Performance Review

Date: June 9, 2026

## Task 15 Performance Hardening

This pass focuses on the large-data and interaction-heavy surfaces named in the spec:

- lessons
- analytics/progress
- flashcards
- admin lists
- quiz interaction
- mock exam timer
- offline sync processing

## Changes Landed

### Main-Thread Avoidance

- Lesson/module/topic/subtopic domain mapping now runs on `Dispatchers.Default` in `ContentRepository`.
- Flashcard cache read/write serialization work now runs off the immediate caller path in `FlashcardRepository`.
- Admin user filtering is now computed off the main thread in `AdminViewModel`, while preserving optimistic UI updates.

### Lazy/Stable Rendering

- High-volume list screens already used `LazyColumn`; this pass keeps that pattern as the default for modules, topics, subtopics, lessons, flashcards, admin, and progress surfaces.
- Lesson detail sections now provide stable keys/content types for explanation, example, section, and takeaway rows to reduce unnecessary recomposition churn.
- Admin and flashcard deck/user lists already use stable row keys by backend IDs.

### Motion/Rendering Discipline

- Reduced-motion preference is now globally resolved at the theme layer.
- Flashcard reveal and milestone emphasis animations honor that preference, limiting unnecessary animated work on accessibility-sensitive devices.

## Evidence And Review Notes

### Lesson Scroll

- Device/Compose coverage already exercises scroll-to-content behavior in `LessonRendererScreenTest`.
- The lesson reader continues to use lazy rendering for long lesson bodies, with stable keys added in this pass.

### Quiz Input Latency

- `QuizScreenTest` covers answer selection and submit/review transitions.
- Quiz interactions remain local-state-first, with answer selection reflected before submit/review processing.

### Chart Rendering

- Progress/readiness and flashcard analytics rely on text-plus-progress-visual summaries rather than heavyweight chart libraries.
- No blocking chart computation library is currently present in the native Android app.

### Flashcard Animation

- `FlashcardStudyScreenTest` covers reveal and session-complete flow.
- Reduced-motion handling now gates the reveal/crossfade timing for lower-motion configurations.

### Mock Exam Timer Accuracy

- `MockExamViewModelTest.timerTicksDownWhileExamIsActive` verifies countdown accuracy against coroutine test time.

### Sync Processing

- `OfflineSyncTest` continues to cover dedupe, success reconciliation, conflict handling, auth-expired failures, and restart visibility.

## Current Boundaries

- The app does not yet include Android Macrobenchmark or Baseline Profile modules.
- There is no remote image-heavy feed in the current native implementation, so dedicated image loader benchmarking is not yet required.
- If future parity adds media-rich lesson rendering or very large admin datasets, Task 15 should be extended with Paging 3 or a benchmark module instead of relying only on review notes.
