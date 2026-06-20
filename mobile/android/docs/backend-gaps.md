# Native Android Backend Gaps

These items were identified while executing the native Android rewrite tasks.

## Auth

- The backend now returns access + refresh tokens from `POST /v1/auth/sessions` and exposes `POST /v1/auth/sessions:refresh` with refresh rotation semantics.
- Native Android refresh is now wired for normal API traffic and offline-sync work through `SessionManager` + `SessionAuthenticator`.
- Google sign-in should use the native Android Google Identity/Credential Manager flow and exchange a Google ID token with `POST /v1/auth/google`; this still needs Google Cloud Android OAuth client configuration.

## Quiz Entrypoint

- Native quiz screen currently starts a sample subtopic quiz with `subtopicId = 1`.
- Production UX should launch quizzes from specific module/topic/subtopic context once screen-to-screen flow is refined.

## Release

- Crash reporting provider is not selected.
- Release signing requires `keystore.properties` or CI secrets.
- Play Store package identity is currently `com.csnexus.app`; confirm before publishing.
