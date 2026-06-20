# Native Android Diagnostics Tooling

Date: June 9, 2026

## Decision

For production-native Android diagnostics, CSNexus should use:

- Firebase Crashlytics for crash reporting and fatal/non-fatal native exceptions
- Firebase Analytics only for release-approved product analytics events
- The in-app `AppLogger` abstraction as the single code path for developer diagnostics, request tracking, sync diagnostics, and screen-view breadcrumbs

## Why This Stack

- Crashlytics is the most common low-friction Android crash pipeline and fits the current Gradle/Compose stack cleanly.
- Firebase Analytics can be constrained to product-approved events while Crashlytics handles operational failures.
- Keeping `AppLogger` as the app-owned abstraction prevents SDK lock-in and lets us redact locally before any provider receives data.

## Privacy Rules

The Android app must never emit raw values for:

- access tokens
- refresh tokens
- passwords
- OTP or verification codes
- Authorization headers
- learner email/display-name style profile fields in diagnostics
- quiz answers where unnecessary
- lesson answer text where unnecessary
- tutor prompts, transcripts, or generated responses where privacy requires redaction
- admin-target identifying values in diagnostics

The current logger layer redacts these values before log formatting. Any Crashlytics or analytics integration must attach only already-redacted values or non-sensitive summaries.

## Required Release Setup

Before a production release:

1. Add Firebase project configuration for the Android package name.
2. Add `google-services.json` through local secure config or CI secrets, not source control.
3. Apply Firebase Gradle plugins only in release-ready configuration.
4. Keep Crashlytics collection disabled or gated for debug/internal builds unless explicitly approved.
5. Restrict analytics to approved event names and reviewed parameter sets.
6. Verify that request IDs, status classes, endpoint names, sync event IDs, and screen names are safe and redacted before export.
7. Perform a privacy review covering Google sign-in, tutor, analytics, and admin diagnostics.

## Current Scope In Repo

Implemented now:

- central `AppLogger`
- request/response diagnostics interceptor
- screen-view logging hook in navigation
- sync-event diagnostics in offline sync processing
- auth refresh/login/delete/logout logging with redaction
- unit coverage for redaction and representative diagnostics formatting

Not yet wired to an external provider:

- Crashlytics SDK dependency and plugin
- Firebase Analytics SDK dependency and event catalog
- release CI/provider credentials

That separation is intentional: Task 14 selects and documents the tooling now, while actual provider enablement should happen with release credentials and privacy sign-off.
