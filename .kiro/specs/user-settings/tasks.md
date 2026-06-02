# Implementation Plan: User Settings

## Overview

Implements a dedicated `/settings` route consolidating profile editing, study preferences, accessibility controls, and account management. The backend gains a `POST /v1/auth/password-change` endpoint and a `DELETE /v1/users/me` soft-delete endpoint. The frontend introduces a `Preferences_Store` (localStorage-backed typed store with migration), section components, and pre-paint accessibility application.

## Tasks

- [x] 1. Preferences Store and initialization
  - [x] 1.1 Create `Preferences_Store` module (`web/src/stores/preferences.ts`)
    - Implement `StudyPreferences` and `AccessibilityPreferences` interfaces
    - Implement typed getters with fallback defaults (`getStudyPreferences`, `getAccessibilityPreferences`)
    - Implement typed setters (`setStudyPreference`, `setAccessibilityPreference`)
    - Implement convenience methods (`isSoundEnabled`, `setSoundEnabled`, `isHapticEnabled`, `setHapticEnabled`)
    - Implement `applyAccessibilityToDOM()` — sets `data-font-size` and `data-reduced-motion` attributes on `<html>`
    - Implement backward-compatibility migration from `csnexus-feedback-enabled` legacy key into `soundEnabled`/`hapticEnabled`
    - Handle localStorage unavailability gracefully (fallback to in-memory defaults)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 4.9, 4.10_

  - [x] 1.2 Write property test: Preferences Store Round-Trip
    - **Property 1: Preferences Store Round-Trip**
    - **Validates: Requirements 6.3, 6.2, 3.5, 4.9**
    - Use fast-check to generate arbitrary valid `StudyPreferences` and `AccessibilityPreferences` objects
    - Assert write-then-read produces an equivalent object

  - [x] 1.3 Create `init-preferences.ts` module (`web/src/stores/init-preferences.ts`)
    - Synchronously read `csnexus-settings-accessibility` from localStorage
    - Apply `data-font-size` and `data-reduced-motion` attributes to `<html>` before React hydrates
    - Import eagerly in `web/src/main.tsx` (before React render call)
    - _Requirements: 4.10_

  - [x] 1.4 Refactor `FeedbackToggle` to delegate to `Preferences_Store`
    - Update `web/src/components/FeedbackToggle.tsx` to call `isSoundEnabled()` / `setSoundEnabled()` from the store
    - Update `web/src/utils/feedback.ts` to read sound/haptic state from the store instead of the legacy key
    - _Requirements: 4.7, 6.5_

- [x] 2. CSS utilities for accessibility preferences
  - [x] 2.1 Add font-size and reduced-motion CSS rules
    - Add `html[data-font-size="compact"] { font-size: 87.5%; }` and `html[data-font-size="large"] { font-size: 115%; }` to `web/src/design-system/utilities.css`
    - Add `html[data-reduced-motion="on"]` universal animation/transition suppression rule
    - _Requirements: 4.3, 4.5, 4.6_

- [x] 3. Backend: Password change endpoint
  - [x] 3.1 Add `PasswordChangeRequest` schema to `app/features/auth/schemas.py`
    - Fields: `current_password: str`, `new_password: str`
    - Apply existing password policy validation on `new_password` (8+ chars, uppercase, lowercase, digit, symbol)
    - _Requirements: 5.2_

  - [x] 3.2 Implement `change_password` method in `app/features/auth/service.py`
    - Verify `current_password` against stored hash
    - Validate `new_password` against password policy via existing `validate_password()` utility
    - Hash new password, persist to DB
    - Revoke all sessions for the user
    - Raise 401 if current password is incorrect, 400 if new password fails policy
    - _Requirements: 5.2, 5.3, 5.4_

  - [x] 3.3 Add `POST /v1/auth/password-change` route to `app/features/auth/router.py`
    - Requires authentication (`get_current_user` dependency)
    - Calls `service.change_password(user, payload)`
    - Returns 204 on success
    - _Requirements: 5.3_

  - [x] 3.4 Write backend tests for password change
    - Service test: correct password → success, wrong password → 401, bad new password → 400
    - Router test: 204 on success, 401 on wrong current password, 400 on policy violation
    - _Requirements: 5.2, 5.3_

- [x] 4. Backend: Account deletion endpoint
  - [x] 4.1 Add `DELETED` value to `AccountState` enum and update DB constraint
    - Add `DELETED = "DELETED"` to `AccountState` in `app/features/users/models.py`
    - Update `ck_users_account_state` CheckConstraint to include `'DELETED'`
    - _Requirements: 5.8_

  - [x] 4.2 Add `AccountDeleteRequest` schema to `app/features/users/schemas.py`
    - Field: `confirmation_phrase: str` (must equal `"DELETE MY ACCOUNT"`)
    - _Requirements: 5.7_

  - [x] 4.3 Implement `delete_account` method in `app/features/users/service.py`
    - Verify confirmation phrase
    - Set `user.account_state = "DELETED"`
    - Revoke all sessions via `AuthRepository.revoke_all_for_user()`
    - Raise 400 if phrase mismatch, 409 if already deleted
    - _Requirements: 5.7, 5.8_

  - [x] 4.4 Add `DELETE /v1/users/me` route to `app/features/users/router.py`
    - Requires authentication
    - Calls `service.delete_account(user, payload)`
    - Returns 204 on success
    - _Requirements: 5.8_

  - [x] 4.5 Write backend tests for account deletion
    - Service test: correct phrase → soft-delete + session revoke, wrong phrase → 400, already deleted → 409
    - Router test: 204 on success, 400 on bad phrase
    - _Requirements: 5.7, 5.8_

- [x] 5. Checkpoint - Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Frontend: Settings page structure and routing
  - [x] 6.1 Create `Settings.tsx` page component (`web/src/pages/Settings.tsx`)
    - Render four GlassCard sections: Profile, Study Preferences, Accessibility & Display, Account Management
    - Include back-navigation to Profile page
    - Apply glass design system aesthetic (GlassCard containers, design tokens)
    - _Requirements: 1.3, 1.4, 1.5_

  - [x] 6.2 Register `/settings` route in `web/src/App.tsx`
    - Add `<Route path="/settings" element={<AuthGuard><Settings /></AuthGuard>} />`
    - _Requirements: 1.1_

  - [x] 6.3 Add Settings navigation link to Profile page
    - Replace inline Preferences section in `web/src/pages/Profile.tsx` with a link/button to `/settings`
    - _Requirements: 1.2_

- [x] 7. Frontend: Profile section
  - [x] 7.1 Create `ProfileSection.tsx` component (`web/src/pages/settings/ProfileSection.tsx`)
    - Display name input (max 255 chars)
    - Username input with regex validation (`^[A-Za-z][A-Za-z0-9_]{2,29}$`)
    - Debounced username availability check via `GET /v1/users/usernames:check`
    - Loading indicator during availability check
    - Available/taken indicators
    - Timezone selector with IANA identifiers
    - Save button that PATCHes only modified fields to `/v1/users/me`
    - Success toast on save, inline errors on failure
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10_

  - [x] 7.2 Write property test: Username Validation Consistency
    - **Property 2: Username Validation Consistency**
    - **Validates: Requirements 2.2**
    - Use fast-check to generate arbitrary strings
    - Assert frontend validation accepts iff the string matches `^[A-Za-z][A-Za-z0-9_]{2,29}$`

  - [x] 7.3 Write property test: Partial Update Payload Correctness
    - **Property 3: Partial Update Payload Correctness**
    - **Validates: Requirements 2.8**
    - Use fast-check to generate subsets of profile fields with arbitrary valid data
    - Assert the constructed PATCH payload contains exactly the modified fields and no others

- [x] 8. Frontend: Study preferences section
  - [x] 8.1 Create `StudySection.tsx` component (`web/src/pages/settings/StudySection.tsx`)
    - Daily goal slider: 5–180 minutes, step 5, default 30
    - Default quiz mode selector: Practice / Exam / Power, default Practice
    - Exam date picker: no earlier than today
    - Countdown display when exam date is set (days remaining)
    - Persist changes immediately to `Preferences_Store`
    - Load stored values on mount, fallback to defaults
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

  - [x] 8.2 Write property test: Exam Countdown Calculation
    - **Property 4: Exam Countdown Calculation**
    - **Validates: Requirements 3.4**
    - Use fast-check to generate future dates and "today" dates
    - Assert countdown equals non-negative integer difference in days

- [x] 9. Frontend: Accessibility section
  - [x] 9.1 Create `AccessibilitySection.tsx` component (`web/src/pages/settings/AccessibilitySection.tsx`)
    - Reduced motion control: System / On / Off (default System)
    - Font size control: Compact / Default / Large (default Default)
    - Sound effects toggle (synced with `Preferences_Store` and `FeedbackToggle`)
    - Haptic feedback toggle (independent)
    - Persist changes immediately, call `applyAccessibilityToDOM()` on change
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9_

- [x] 10. Frontend: Account management section
  - [x] 10.1 Create `AccountSection.tsx` component (`web/src/pages/settings/AccountSection.tsx`)
    - Change password form: current password + new password fields with inline validation
    - Password policy enforcement (8+ chars, uppercase, lowercase, digit, symbol)
    - Logout button calling `DELETE /v1/auth/sessions/me` and clearing local auth state
    - Delete account button (danger variant)
    - _Requirements: 5.1, 5.2, 5.5, 5.6_

  - [x] 10.2 Create `DeleteAccountDialog.tsx` modal (`web/src/pages/settings/DeleteAccountDialog.tsx`)
    - Requires typing "DELETE MY ACCOUNT" to confirm
    - Calls `DELETE /v1/users/me` on confirmation
    - Closes without action on cancel
    - _Requirements: 5.7, 5.8, 5.9_

  - [x] 10.3 Write property test: Password Validation Consistency
    - **Property 5: Password Validation Consistency**
    - **Validates: Requirements 5.2**
    - Use fast-check to generate arbitrary strings
    - Assert frontend validation rejects iff the string fails at least one of: length < 8, no uppercase, no lowercase, no digit, no symbol

- [x] 11. Frontend unit tests
  - [x] 11.1 Write unit tests for Settings page and sections
    - `Settings.test.tsx`: renders all four sections, back navigation works
    - `ProfileSection.test.tsx`: input rendering, debounced username check, availability indicators, save/error flows
    - `StudySection.test.tsx`: control rendering with defaults, persistence on change
    - `AccessibilitySection.test.tsx`: toggle states, CSS application
    - `AccountSection.test.tsx`: password validation, logout flow, delete confirmation
    - `PreferencesStore.test.ts`: migration from legacy key, fallback on storage failure, typed getters
    - _Requirements: 1.1–6.5_

- [x] 12. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Backend follows the three-layer test strategy (repository → service → router)
- Frontend property tests use fast-check and live under `web/src/__tests__/properties/`

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "2.1", "3.1", "4.1"] },
    { "id": 1, "tasks": ["1.2", "1.3", "3.2", "4.2"] },
    { "id": 2, "tasks": ["1.4", "3.3", "4.3", "6.1"] },
    { "id": 3, "tasks": ["3.4", "4.4", "6.2", "6.3"] },
    { "id": 4, "tasks": ["4.5", "7.1", "8.1", "9.1"] },
    { "id": 5, "tasks": ["7.2", "7.3", "8.2", "10.1"] },
    { "id": 6, "tasks": ["10.2", "10.3"] },
    { "id": 7, "tasks": ["11.1"] }
  ]
}
```
