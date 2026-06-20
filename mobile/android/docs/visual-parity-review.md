# Native Android Visual And Motion Parity Review

Date: June 9, 2026

Method:

- compare current native routes and UI states against `visual-motion-baseline.md`
- read corresponding native source for shell, lesson, quiz, mock exam, flashcards, progress, settings, auth, and admin screens
- confirm critical lesson/quiz/flashcard/mock-exam behavior on the `codex_api36` emulator through direct instrumentation runs

This review is intentionally source-derived for parity execution in this repo, consistent with the earlier baseline capture approach.

## Major Workflow Review

| Workflow | Result | Notes |
| --- | --- | --- |
| Public home and auth entry | pass-with-convergence | Native now exposes a public home route plus login/signup/forgot-password/OTP entry flows. Visual styling is native Compose rather than the web glass-hero composition, but the route coverage and CTA intent are preserved. |
| Lessons | pass | Typed lesson blocks, segmented reading, inline checks, tutor companion, completion, offline banner, and reduced-motion-aware behavior are present. Device-tested in `LessonRendererScreenTest`. |
| Quiz | pass | Mode selection, answer states, result review, and reduced-motion-aware emphasis are present. Device-tested in `QuizScreenTest`. |
| Mock exam | pass | Timer, leave-confirmation, submit-confirmation, and results handoff are present. Device-tested in `MockExamScreenTest`. |
| Flashcard study | pass | Reveal, study modes, pending-sync messaging, and reduced-motion-aware reveal transitions are present. Device-tested in `FlashcardStudyScreenTest`. |
| Progress and analytics | pass-with-convergence | Native uses accessible progress and summary views in place of decorative web charts where appropriate. Text summaries and progress semantics are preserved. |
| Settings and profile | pass | Native preserves editable profile, password change, logout, delete-account flow, local preferences, and accessibility/display controls. |
| Admin | pass | Native preserves analytics summary, user search, optimistic moderation actions, delete confirmation, and role gating. |
| Shell/navigation | pass-with-convergence | Native uses top app bar, bottom navigation, and quick-navigation sheet instead of the web desktop shell, command palette, and glass navbar. This is an intentional platform adaptation rather than a WebView carry-over. |

## Motion Review

- reduced motion is now resolved from the saved native preference plus the system animation scale
- quiz answer emphasis respects reduced motion
- flashcard reveal/crossfade respects reduced motion
- milestone earned-state emphasis respects reduced motion
- lesson and analytics state changes remain restrained and readable without forcing web-style motion

## Remaining Non-Visual Parity Risks

- native Google sign-in is still blocked on Android OAuth and backend exchange confirmation
- refresh-token and sync-backend contracts still need backend confirmation before certification can be called final
- the authenticated dashboard route remains a native entry hub rather than a replica of every web home/dashboard data treatment
