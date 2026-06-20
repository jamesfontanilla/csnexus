# Native Android Release Readiness Report

Date: June 9, 2026

## Status

Current certification state: not yet final full-parity release approval.

Task 16 execution is complete in the sense that the quality gate, parity review, artifact generation, and readiness reporting work have been performed. The app is device-testable and broadly feature-complete as a native Android app, but final release parity is still bounded by documented backend and configuration gaps.

## Completed Native Parity

- public home and auth flows
- lesson reading, inline checks, completion, offline read cache, and lesson tutor companion
- scoped quiz flows
- mock exam flow and results handoff
- progress, mastery, analytics, goals, readiness, study plan, focus, queue, onboarding, milestones
- profile and settings
- flashcards: decks, study, marketplace, analytics, exam, social, generate, admin gate
- leaderboards, tournaments, tutor, admin, release-readiness route
- centralized logging, privacy redaction, offline sync processing, accessibility/display preferences, and device hardening

## Known Backend Or Configuration Gaps

See [backend-full-parity-gaps.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/backend-full-parity-gaps.md) for the authoritative list.

Highest-impact open items:

1. native Google sign-in Android OAuth client configuration and backend audience acceptance
2. remaining backend-gap items in [backend-full-parity-gaps.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/backend-full-parity-gaps.md) that are not part of the current native blocker set

The progress-sync contract, lesson freshness/fallback contract, settings ownership contract, and tutor privacy/context contract are now documented and fixture-backed in the Android repo.

## Intentionally Excluded Items

None recorded with product approval in this repo snapshot.

## Test And Verification Evidence

Automated:

- `.\gradlew.bat testDebugUnitTest`
- `.\gradlew.bat assembleDebug`
- `.\gradlew.bat assembleDebugAndroidTest`
- `.\gradlew.bat assembleRelease`

Fixture-based contract checks:

- refresh-session success and rotation fixtures
- Google exchange success and unverified-email fixtures
- progress-sync accepted/rejected/conflict fixture shape

Device-executed on `codex_api36` via direct `adb shell am instrument`:

- `LessonRendererScreenTest`
- `QuizScreenTest`
- `FlashcardStudyScreenTest`
- `MockExamScreenTest`
- `AppDatabaseMigrationTest`

Source-derived review:

- [visual-parity-review.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/visual-parity-review.md)
- [accessibility-review.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/accessibility-review.md)
- [performance-review.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/performance-review.md)

## Supported Devices

See [device-support-policy.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/device-support-policy.md).

## Artifacts

Primary debug artifact:

- `mobile/android/app/build/outputs/apk/debug/app-debug.apk`

Android test artifact:

- `mobile/android/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk`

Release build artifact generated for validation:

- `mobile/android/app/build/outputs/apk/release/app-release-unsigned.apk`

Signed release artifact was not produced in this repo snapshot because signing credentials are intentionally kept out of source control.

## Install And Device-Test Commands

```powershell
adb install -r mobile/android/app/build/outputs/apk/debug/app-debug.apk
adb install -r mobile/android/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
adb shell am instrument -w -e class com.csnexus.app.feature.quizzes.ui.QuizScreenTest com.csnexus.app.debug.test/androidx.test.runner.AndroidJUnitRunner
```

## Release Commands

```powershell
cd mobile/android
.\gradlew.bat testDebugUnitTest
.\gradlew.bat assembleDebug
.\gradlew.bat assembleDebugAndroidTest
.\gradlew.bat assembleRelease
```

## Rollback Plan

1. keep `web/android` Capacitor wrapper available until native release acceptance is explicit
2. ship debug/internal native builds first
3. if a native release regresses critical auth, lesson, quiz, or sync behavior, halt rollout and point users back to the accepted web deployment while the native fix is prepared
4. avoid enabling external diagnostics providers or signed production rollout until backend-gap items and signing prerequisites are closed
