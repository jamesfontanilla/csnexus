# Native Android Device Support Policy

Date: June 9, 2026

## SDK Policy

- `minSdk`: 24 (Android 7.0)
- `targetSdk`: 36
- `compileSdk`: 36

This keeps the native app available on still-common Android devices while aligning release behavior with the current Android platform target.

## Screen And Form-Factor Support

- Phones: supported from compact handsets through large phones
- Tablets: supported for content, analytics, flashcards, and admin read/write flows
- Foldables: supported in standard resized-window behavior; no device-specific fold posture UI is implemented
- Chromebooks/Desktop mode: not a primary release target, but Compose layouts should remain functional at wide widths

## Orientation Policy

- Portrait: primary supported orientation for all workflows
- Landscape: supported where Compose layouts naturally reflow without clipping, especially lessons, analytics, quiz review, and admin lists
- No flow in the native app currently depends on a landscape-only interaction

## Input And Accessibility Expectations

- Touch is the primary input mode
- Hardware keyboard input should remain usable in auth, tutor, settings, admin search, and free-text study surfaces
- TalkBack, system font scaling, and reduced motion are treated as first-class support requirements

## Test Device Matrix

Minimum verification set for parity and hardening:

1. Compact phone, API 24 or newer
2. Modern phone, current target API
3. Large phone or small tablet
4. Emulator/device with TalkBack or accessibility scanner available

Local verification executed in this repo has primarily used:

- Android emulator `codex_api36`
- API level 36
- debug builds and targeted instrumented tests

## Release Gate For Device Support

Before calling a release candidate ready:

1. `testDebugUnitTest` must pass
2. `assembleDebug` must pass
3. targeted Compose/instrumented coverage for lessons, quiz, flashcards, and mock exam must pass on the active emulator/device
4. the accessibility and performance review docs in this folder must be updated if support assumptions change
