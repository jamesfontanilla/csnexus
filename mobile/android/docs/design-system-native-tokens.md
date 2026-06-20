# Native Design System Token Spec

Task: `3.1 Extract web design tokens into native token spec`.

Baseline source: `mobile/android/docs/visual-motion-baseline.md` and the web files it references.

## Color Roles

| Native role | Web source value | Compose usage |
| --- | --- | --- |
| Background | `#080808` / `#050505` | `MaterialTheme.colorScheme.background` |
| Surface | `#1C1C1C` | `MaterialTheme.colorScheme.surface` |
| Raised surface | `#242424` approximation | `MaterialTheme.colorScheme.surfaceVariant` |
| Primary/accent | `#C9A84C` | Primary buttons, selected nav, progress |
| Secondary/metallic | `#E8C96A` | Secondary accent and highlights |
| Primary text | `#F0EBE0` | `onBackground`, `onSurface` |
| Secondary text | `#9A9A9A` | `onSurfaceVariant` |
| Muted text | `#666666` | `CSNexusTheme.tokens.semantic.textMuted` |
| Success | `#8FBC8F` | Correct states, positive badges |
| Warning | `#E8A838` | Offline banner, timers |
| Danger | `#D4645C` | Destructive actions, incorrect states |
| Info | `#7EB8C9` | Informational states |

## Spacing, Radius, Elevation

- Spacing keeps the 4px web base scale: 4, 8, 12, 16, 24, 32, 48, 64dp.
- Radius maps web 8, 12, 20, 28px to Compose dp.
- Elevation is restrained because the web's glass look relies more on translucency and borders than heavy shadows.

## Typography

Android uses system sans-serif for now while preserving the web hierarchy:

- Display/headline for product identity and major screen titles.
- Title for cards, sections, and dialogs.
- Body with relaxed line height for lesson reading.
- Label for buttons, chips, tabs, and metadata.

## Component States

Native components must provide:

- Loading: inline progress or skeleton.
- Empty: concise title/body and next action if available.
- Error: message, retry, and request diagnostics where available.
- Offline: persistent non-blocking banner.
- Selected: accent color and accessible selected state.
- Disabled: Material disabled state plus no hidden action.
- Focus: Android focus ring/semantic focus behavior.

## Motion

Native motion tokens mirror web durations:

- Instant: 80ms.
- Fast: 150ms.
- Normal: 250ms.
- Slow: 400ms.
- Page: 500ms.

Reduced motion uses instant/opacity-only behavior and disables decorative movement.
