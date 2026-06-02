# Requirements Document

## Introduction

A dedicated Settings page for CSNexus that consolidates user-configurable preferences into a single, organized interface. The page replaces the inline "Preferences" section currently embedded in the Profile page and expands it to cover profile editing, study preferences, accessibility controls, and account management. Profile settings persist via the existing `PATCH /v1/users/me` backend endpoint; study and accessibility preferences are stored client-side (localStorage) since they affect only the local UI; account-level actions (password change, account deletion) use the existing auth API surface.

## Glossary

- **Settings_Page**: The dedicated `/settings` route that renders all user-configurable options grouped by section.
- **Profile_Section**: The settings section that manages server-persisted user identity fields (display name, username, timezone).
- **Study_Section**: The settings section for client-side study preferences (daily goal, quiz mode, target exam date).
- **Accessibility_Section**: The settings section for client-side display and feedback preferences (reduced motion, font size, sound, haptics).
- **Account_Section**: The settings section for destructive or security-sensitive account operations (password change, logout, deletion).
- **Preferences_Store**: The localStorage-backed persistence layer for client-side settings (study + accessibility).
- **Username_Checker**: The existing `GET /v1/users/usernames:check` endpoint used for real-time username availability validation.
- **User_API**: The existing `PATCH /v1/users/me` endpoint that persists `display_name`, `username`, and `tz_name`.
- **Auth_API**: The existing auth routes under `/v1/auth` for password resets and session management.

## Requirements

### Requirement 1: Settings Page Navigation

**User Story:** As a user, I want to access my settings from both the Profile page and the main navigation, so that I can quickly find and adjust my preferences regardless of where I am in the app.

#### Acceptance Criteria

1. THE Settings_Page SHALL be accessible at the `/settings` route within the authenticated area of the application.
2. WHEN a user navigates to the Profile page, THE Profile_Section SHALL display a visible link or button that navigates to the Settings_Page.
3. THE Settings_Page SHALL display a back-navigation control that returns the user to the Profile page.
4. THE Settings_Page SHALL render section headings for Profile, Study Preferences, Accessibility & Display, and Account Management in that order.
5. THE Settings_Page SHALL follow the existing glass design system aesthetic (GlassCard containers, design token colors, consistent spacing).

### Requirement 2: Profile Settings

**User Story:** As a user, I want to edit my display name, username, and timezone from the Settings page, so that I can keep my profile information current.

#### Acceptance Criteria

1. THE Profile_Section SHALL display the current display name in an editable text input with a maximum length of 255 characters.
2. THE Profile_Section SHALL display the current username in an editable text input constrained to 3–30 characters, starting with a letter, containing only letters, digits, or underscores.
3. WHEN a user modifies the username field, THE Username_Checker SHALL be queried after a debounce period to check availability.
4. WHILE the username availability check is pending, THE Profile_Section SHALL display a loading indicator adjacent to the username input.
5. WHEN the Username_Checker returns `available: false`, THE Profile_Section SHALL display an inline error message stating the username is taken.
6. WHEN the Username_Checker returns `available: true`, THE Profile_Section SHALL display a confirmation indicator adjacent to the username input.
7. THE Profile_Section SHALL display a timezone selector populated with IANA timezone identifiers, defaulting to the user's current `tz_name`.
8. WHEN a user submits profile changes, THE User_API SHALL be called with only the modified fields.
9. WHEN the User_API returns a successful response, THE Profile_Section SHALL display a success toast notification.
10. IF the User_API returns a validation error, THEN THE Profile_Section SHALL display the error message inline near the relevant field.

### Requirement 3: Study Preferences

**User Story:** As a user, I want to configure my daily study goal, default quiz mode, and target exam date, so that the app adapts to my study plan and I see a motivational countdown.

#### Acceptance Criteria

1. THE Study_Section SHALL display a daily study goal control that allows selecting a value between 5 and 180 minutes in 5-minute increments, defaulting to 30 minutes.
2. THE Study_Section SHALL display a default quiz mode selector with options: Practice, Exam, and Power, defaulting to Practice.
3. THE Study_Section SHALL display a target exam date picker that accepts a date no earlier than today.
4. WHEN a target exam date is set, THE Study_Section SHALL display a countdown showing the number of days remaining until the exam.
5. WHEN any study preference is changed, THE Preferences_Store SHALL persist the updated value immediately.
6. WHEN the Settings_Page loads, THE Study_Section SHALL read stored values from the Preferences_Store, falling back to defaults if no stored value exists.

### Requirement 4: Accessibility and Display Preferences

**User Story:** As a user, I want to control motion, font size, sound effects, and haptic feedback, so that I can tailor the interface to my sensory and readability needs.

#### Acceptance Criteria

1. THE Accessibility_Section SHALL display a reduced motion control with three options: System (default), On, and Off.
2. WHEN reduced motion is set to System, THE Settings_Page SHALL respect the operating system's `prefers-reduced-motion` media query.
3. WHEN reduced motion is set to On, THE Settings_Page SHALL suppress all CSS animations and motion-based transitions application-wide.
4. WHEN reduced motion is set to Off, THE Settings_Page SHALL enable all animations regardless of the system preference.
5. THE Accessibility_Section SHALL display a font size preference control with three options: Compact, Default, and Large.
6. WHEN font size preference is changed, THE Settings_Page SHALL apply corresponding CSS custom property overrides to the document root.
7. THE Accessibility_Section SHALL display a sound effects toggle that reflects and controls the same underlying preference as the existing FeedbackToggle component.
8. THE Accessibility_Section SHALL display a haptic feedback toggle as a separate control independent of the sound effects toggle.
9. WHEN any accessibility preference is changed, THE Preferences_Store SHALL persist the updated value immediately.
10. WHEN the application loads, THE Preferences_Store SHALL apply persisted accessibility preferences before first paint to prevent a flash of default styling.

### Requirement 5: Account Management

**User Story:** As a user, I want to change my password, log out, or delete my account from a single place, so that I have full control over my account security and lifecycle.

#### Acceptance Criteria

1. THE Account_Section SHALL display a "Change Password" action that navigates to or opens an inline form for password change.
2. WHEN a user initiates a password change, THE Account_Section SHALL require the current password and a new password meeting the existing password policy (8+ characters, uppercase, lowercase, digit, symbol).
3. WHEN the password change is submitted, THE Auth_API SHALL be called via the password-reset flow to rotate the password and revoke all sessions.
4. WHEN the password change succeeds, THE Account_Section SHALL display a success toast and redirect the user to the login page.
5. THE Account_Section SHALL display a "Log Out" button that calls `DELETE /v1/auth/sessions/me` and clears local auth state.
6. THE Account_Section SHALL display a "Delete Account" button styled with a danger variant.
7. WHEN a user clicks "Delete Account", THE Account_Section SHALL present a confirmation dialog requiring the user to type a confirmation phrase before proceeding.
8. IF the user confirms account deletion, THEN THE Account_Section SHALL call the appropriate backend endpoint to schedule or execute account deletion.
9. IF the user cancels the deletion confirmation, THEN THE Account_Section SHALL close the dialog without taking action.

### Requirement 6: Client-Side Preference Persistence

**User Story:** As a user, I want my study and accessibility preferences to survive page reloads and app reinstalls on the same browser, so that I do not need to reconfigure settings repeatedly.

#### Acceptance Criteria

1. THE Preferences_Store SHALL use localStorage as the primary storage mechanism with a namespaced key prefix (`csnexus-settings-`).
2. THE Preferences_Store SHALL serialize all preference values as JSON under their respective keys.
3. FOR ALL valid preference objects, reading after writing SHALL produce an equivalent object (round-trip property).
4. IF localStorage is unavailable or throws a quota error, THEN THE Preferences_Store SHALL fall back to in-memory defaults without crashing.
5. THE Preferences_Store SHALL expose a typed API (TypeScript interface) so consumers access preferences through getters with fallback defaults, not raw `localStorage.getItem` calls.
