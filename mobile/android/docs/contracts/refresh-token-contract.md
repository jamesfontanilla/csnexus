# Refresh Token Contract

Status: implemented in repo. Backend now returns refresh tokens on login and exposes `POST /v1/auth/sessions:refresh`; keep this document aligned with the exported OpenAPI if the contract changes again.

## Goals

- Keep Android users signed in across launches without storing passwords.
- Allow access-token refresh before or after a protected request fails.
- Support refresh-token rotation.
- Prevent concurrent Android requests from creating refresh stampedes.
- Clear local auth state when the refresh token is invalid, revoked, expired, malformed, or replayed.

## Login Response

`POST /v1/auth/sessions`

Recommended success response:

```json
{
  "access_token": "jwt",
  "refresh_token": "opaque-refresh-token",
  "token_type": "bearer",
  "expires_in": 900,
  "refresh_expires_in": 2592000,
  "user": {
    "id": 123,
    "email": "learner@example.com",
    "display_name": "Learner",
    "role": "learner"
  }
}
```

The web currently consumes `access_token`. Android needs `refresh_token`, expiry metadata, and preferably user role metadata.

## Refresh Request

`POST /v1/auth/sessions:refresh`

Request:

```json
{
  "refresh_token": "opaque-refresh-token"
}
```

Headers:

- `Content-Type: application/json`
- No access token required.

## Refresh Success

```json
{
  "access_token": "new-jwt",
  "refresh_token": "new-opaque-refresh-token",
  "token_type": "bearer",
  "expires_in": 900,
  "refresh_expires_in": 2592000
}
```

If backend does not rotate refresh tokens on every refresh, it should either return the same refresh token or omit `refresh_token` and explicitly document non-rotation. Android will treat returned tokens as authoritative and atomically replace stored token state.

## Failure Codes

| HTTP | Code | Android behavior |
| --- | --- | --- |
| 400 | `MALFORMED_REFRESH_TOKEN` | Clear tokens and route to login. |
| 401 | `REFRESH_TOKEN_EXPIRED` | Clear tokens and route to login. |
| 401 | `REFRESH_TOKEN_REVOKED` | Clear tokens and route to login. |
| 401 | `REFRESH_TOKEN_REPLAYED` | Clear tokens, cancel protected sync, route to login. |
| 429 | `RATE_LIMITED` | Keep tokens, back off, show retry state if user-visible. |
| 500 | `SERVER_ERROR` | Keep tokens, retry with backoff where safe. |

## Android Session Behavior

1. `SessionManager` exposes a single auth state stream.
2. Protected requests attach the latest access token.
3. If access token is expired or a protected request returns 401, `SessionManager` performs one refresh for all waiting requests.
4. Successful refresh atomically updates encrypted token storage.
5. Permanent refresh failure clears tokens, pauses protected sync work, cancels in-flight protected calls, and navigates to login.
6. No token values are logged.

## Mock Fixtures

- `mobile/android/docs/contracts/fixtures/auth-refresh-success.json`
- `mobile/android/docs/contracts/fixtures/auth-refresh-rotated.json`
- `mobile/android/docs/contracts/fixtures/auth-refresh-revoked.json`
