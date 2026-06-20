# Settings And Profile Ownership Contract

Status: confirmed native ownership contract for the current Android settings surface.

## Goals

- Avoid drifting web and Android settings.
- Persist cross-platform settings through Backend_API.
- Persist Android-only preferences locally through DataStore.
- Roll back optimistic UI when Backend_API rejects changes.

## Ownership Matrix

| Setting or profile field | Proposed owner | Known web source | Native persistence |
| --- | --- | --- | --- |
| Email | Server | `/v1/auth/me` | Read-only or server mutation if backend supports it. |
| Username | Server | `/v1/users/usernames:check`, `/v1/users/me` | Backend validation and update. |
| Display name | Server | `/v1/users/me` | Backend update with rollback. |
| Timezone | Server | `/v1/users/me` | Backend update with rollback. |
| Password change | Server | `/v1/auth/password-change` | Online-only mutation. |
| Delete account | Server | `/v1/users/me` | Online-only destructive action. |
| Daily XP target | Server | `/v1/goals/me/target` | Backend update with rollback. |
| Queue preferences | Server | `/v1/queue/preferences` | Backend update. |
| Bedtime | Server | `/v1/preferences/bedtime` | Backend update if Android exposes it. |
| Daily study goal minutes | Local | `localStorage` preference | DataStore. |
| Default quiz mode | Local | `localStorage` preference | DataStore. |
| Exam date | Local | `localStorage` preference | DataStore. |
| Feedback enabled | Local | `localStorage` preference | DataStore. |
| Accessibility font size | Local | `localStorage` preference | DataStore. |
| Reduced motion | Local/system | Browser/system behavior | Android system setting plus DataStore if explicit app toggle exists. |
| Theme preference | Local | Settings UI | DataStore. |
| Notification preferences | Local/device | Settings UI | Android notification permission and local preference only. |
| Sound feedback | Local | `localStorage` preference | DataStore. |
| Haptic feedback | Local | `localStorage` preference | DataStore. |

## Mutation Response

Canonical success response for server-owned settings:

```json
{
  "status": "ok",
  "settings": {
    "daily_goal_xp": 50
  },
  "updated_at": "2026-06-08T00:00:00Z"
}
```

Canonical validation error:

```json
{
  "error": {
    "message": "Daily goal must be between 10 and 500 XP.",
    "code": "INVALID_DAILY_GOAL",
    "fields": {
      "target_xp": "out_of_range"
    }
  }
}
```

Android behavior:

1. Disable save while request is in flight.
2. Optionally show optimistic value.
3. Replace with canonical server response on success.
4. Roll back and show specific error on failure.
5. Queue offline only if the setting is allow-listed by the sync contract.

For endpoint-specific resource updates that return a domain document instead of the generic settings envelope, Android accepts the resource document as canonical for that endpoint and still applies the same rollback/error rules.
