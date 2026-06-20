# Native Android Scope Decisions

## Google Sign-In

The backend exposes `POST /v1/auth/google` for ID-token exchange. Android still needs a Google Cloud Android OAuth client and native Credential Manager / Google Identity implementation. The web button flow should not be reused.

## Admin

Admin routes are intentionally not exposed in the native learner navigation yet. Mobile admin should be scoped separately and gated by role-aware navigation if the product needs it.

## Notifications

Native notifications are not enabled yet. They should be added only after reminder/study-plan notification requirements are confirmed.

## Auth Refresh

The backend now returns access + refresh tokens and exposes `POST /v1/auth/sessions:refresh`. Native Android is wired to refresh on 401s and from offline sync without falling back to a WebView flow.
