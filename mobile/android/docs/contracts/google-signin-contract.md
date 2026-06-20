# Native Google Sign-In Contract

Status: partially specified. The Android app now uses the CSNexus Web OAuth client as its Credential Manager `serverClientId`, but the Android OAuth client ID, package name, and certificate fingerprints still need to be confirmed in Google Cloud and accepted by Backend_API.

## Goals

- Use native Android Google sign-in, not a WebView or browser DOM flow.
- Exchange a Google ID token or authorization credential with Backend_API.
- Let Backend_API issue normal CSNexus access and refresh tokens.
- Support account linking and clear error states.

## Required Configuration

| Item | Required value |
| --- | --- |
| Android package | `com.csnexus.app` unless publishing identity changes |
| Android OAuth client ID | TBD |
| SHA-1 fingerprint | TBD |
| SHA-256 fingerprint | TBD |
| Accepted backend audience | `783266149311-i5viqa65l37rpe66dtv1dvv8vaq671ao.apps.googleusercontent.com` |
| Web client ID reuse allowed? | Yes. Use the web client ID as the Android app's `serverClientId`. |

## Exchange Endpoint

`POST /v1/auth/google`

Recommended Android request:

```json
{
  "id_token": "google-id-token",
  "platform": "android",
  "android_package": "com.csnexus.app"
}
```

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
  },
  "account_status": "signed_in"
}
```

## Backend Verification Requirements

Backend_API must validate:

- Google token signature.
- Issuer.
- Audience.
- Expiry.
- Email verification.
- Package/audience pairing for Android.
- Existing user linking rules.

## Error States

| HTTP | Code | Android state |
| --- | --- | --- |
| 400 | `GOOGLE_TOKEN_MISSING` | Show sign-in error and retry. |
| 401 | `GOOGLE_TOKEN_INVALID` | Retry Google sign-in. |
| 401 | `GOOGLE_TOKEN_EXPIRED` | Retry Google sign-in. |
| 403 | `GOOGLE_EMAIL_UNVERIFIED` | Explain account cannot be used until verified. |
| 409 | `GOOGLE_EMAIL_CONFLICT` | Offer account-link flow if backend supports it. |
| 429 | `RATE_LIMITED` | Back off and show retry. |

## Android UI States

- Loading Google credential.
- User cancelled.
- Credential unavailable.
- Backend exchange loading.
- Account conflict.
- Unverified email.
- Signed in.
- Retry after network error.

## Mock Fixtures

- `mobile/android/docs/contracts/fixtures/google-exchange-success.json`
- `mobile/android/docs/contracts/fixtures/google-exchange-unverified-email.json`
