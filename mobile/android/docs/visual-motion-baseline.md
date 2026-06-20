# Visual And Motion Baseline

Task 1.3 is source-derived by request. Instead of requiring screenshots or recordings, this baseline was captured by reading the web files that define visual system, motion behavior, shell behavior, lesson formatting, assessment interactions, flashcard study, focus timers, and chart semantics.

Baseline captured on 2026-06-08.

## Source Files Read

| Area | Source files |
| --- | --- |
| App routing and shell switch | `web/src/App.tsx` |
| Design tokens | `web/src/design-system/tokens.css` |
| Motion presets | `web/src/design-system/motion.ts`, `web/src/design-system/animations.css` |
| Shared visual utilities | `web/src/design-system/utilities.css` |
| Glass components | `web/src/components/GlassCard.tsx`, `web/src/components/GlassButton.tsx`, `web/src/components/GlassInput.css`, `web/src/components/GlassNavbar.css`, `web/src/components/GlassModal.tsx` |
| Page transitions | `web/src/components/PageTransition.tsx`, `web/src/components/DirectionalTransition.tsx`, `web/src/components/CrossfadeContent.tsx` |
| Desktop shell | `web/src/components/shell/DesktopAppShell.tsx`, `web/src/components/shell/ContentArea.tsx`, `web/src/components/shell/DetailPanel.tsx`, `web/src/components/shell/CommandPalette.tsx`, `web/src/components/shell/shell.css` |
| Lesson rendering | `web/src/pages/content/LessonReader.tsx`, `web/src/pages/content/lesson/types.ts`, `web/src/pages/content/lesson/BlockRenderer.tsx`, `web/src/pages/content/lesson/DesktopLessonLayout.tsx`, `web/src/pages/content/lesson/PracticePanel.tsx`, `web/src/pages/content/lesson/LessonChatPanel.tsx` |
| Quiz and mock exam | `web/src/pages/quiz/QuizPlayer.tsx`, `web/src/pages/mock-exam/MockExamPlayer.tsx` |
| Flashcard study | `web/src/pages/flashcards/StudySession.tsx` |
| Focus | `web/src/pages/Focus.tsx` |
| Charts and progress | `web/src/components/Chart.tsx`, `web/src/components/HeatMap.tsx`, `web/src/components/ProgressRing.tsx` |

## Design Token Baseline

The web visual identity is an obsidian and refined-gold glass system.

| Token group | Web baseline | Native Android target |
| --- | --- | --- |
| Core palette | Near-black backgrounds `#080808`, `#050505`, surface `#1C1C1C`, accent gold `#C9A84C`, metallic gold `#E8C96A`, warm white text `#F0EBE0` | Compose color roles for background, surface, primary/accent, on-surface, outline, success, warning, danger, info |
| Semantic colors | Success `#8fbc8f`, warning `#e8a838`, danger `#d4645c`, info `#7eb8c9` | Dedicated semantic color tokens, not overloaded primary colors |
| Glass surfaces | Subtle/medium/strong translucent white overlays, blur sizes 20/30/40px, light/medium/strong borders | Material 3 surfaces using dark translucent overlays, border strokes, shadow/elevation approximation; no WebView blur dependency |
| Radius | 8px, 12px, 20px, 28px, full pill | Compose shape scale |
| Spacing | 4px base scale from 0 to 96px | Compose spacing object |
| Typography | Display: Clash Display fallback; body: Satoshi/Inter/system; line heights 1.2 to 2 | Android font fallback with matching hierarchy; avoid clipped dynamic type |
| Motion duration | 80ms instant, 150ms fast, 250ms normal, 400ms slow, 500ms page | Compose motion constants |
| Easing | Standard, decelerate, accelerate, spring cubic-bezier | Compose `tween`, `spring`, and reduced-motion variants |
| Interactive states | hover bg, active bg, focus ring, disabled opacity | Pressed/focused/selected/disabled states with Android semantics |

## Motion Primitive Baseline

| Primitive | Source behavior | Native Android mapping |
| --- | --- | --- |
| App shell switch | `App.tsx` crossfades desktop shell and mobile layout over 250ms with `easeInOut` | Adaptive scaffold switch with short fade; no DOM layout copy |
| Route/page transition | `PageTransition` uses slide-up: opacity plus y offset; disabled under reduced motion | Navigation Compose enter/exit transition with opacity and vertical offset |
| Directional transition | Forward slides from right, back from left, fade scales to 0.98 | Direction-aware navigation animation for nested learning flows |
| Content crossfade | Loading/content swaps fade with 4px y movement over 200ms | `AnimatedContent` or `Crossfade` for state changes |
| Spring presets | Default 300/20, gentle 200/25, bouncy 400/15 | Compose springs with matching stiffness/damping intent |
| Staggered lists | 60ms or 50ms child stagger with y=8 entrance | Lazy list item entrance where useful; avoid delaying task-critical content |
| Glass card entrance | opacity 0, y=8, 250ms; hover y=-2 or scale=1.01 | Card appear animation; hover becomes press/focus/selected feedback |
| Button feedback | hover scale 1.02, tap scale 0.97, ripple span, spinner 0.6s | Material ripple, pressed scale if appropriate, native progress indicator |
| Modal/palette | backdrop fade 200ms; panel scale 0.96/y=-8 with spring | Dialog/sheet with fade and scale; focus trap equivalent |
| Detail panel | slides from right over 250ms; reduced motion fades over 80ms | Navigation rail/detail pane on tablets, bottom sheet or secondary screen on phones |
| Progress ring | stroke-dashoffset animates over slow duration; role progressbar | Compose Canvas progress with accessibility progress semantics |
| Timer pulse | low-time pulse animation; reduced-motion disables | Subtle color/badge change, optional pulse if reduced motion off |
| Skeleton | shimmer-glow 2s; reduced-motion static | Static or shimmer skeleton based on system setting |
| Ambient background | drifting blobs and grain in CSS | Android should avoid expensive decorative motion unless proven performant |

## Reduced Motion Baseline

The web supports reduced motion in three ways:

- `useReducedMotion()` reads `prefers-reduced-motion`.
- Motion wrappers return plain children or strip transform movement.
- CSS caps animations/transitions to near-instant durations or disables specific animations.

Native Android must read the platform animator duration scale/reduced-motion equivalent and provide:

- No y/x/scale transitions when reduced motion is active.
- Static skeletons instead of shimmer.
- No pulsing timers or decorative ambient motion.
- Instant or 80ms opacity-only state changes where feedback is still needed.

## App Shell Baseline

| Shell behavior | Web baseline | Native Android target |
| --- | --- | --- |
| Desktop shell | CSS grid with sidebar, resize handle, main content, optional detail panel | Tablet/adaptive layout with navigation rail/sidebar and optional secondary pane |
| Mobile shell | Glass navbar layout | Bottom navigation/top app bar combination |
| Command palette | Cmd/Ctrl+K modal, fuzzy search, 150ms debounce, sections pages/actions/recent, arrow navigation, Enter execute, Escape close, focus trap | Android search/command sheet with keyboard support and accessible list selection |
| Recent pages | Stored in `sessionStorage` | DataStore recent destinations if retained |
| Focus mode | Shell hides panels, fixed exit button | Immersive study mode with explicit exit affordance |
| Content area | Scroll resets on route change; centered/standard/split layout modes | Per-destination scroll state and adaptive content width |
| Detail panel | Lazy contextual panel with skeleton, retryable error boundary, Escape close | Context sheet/pane with loading/error/retry states |

## Lesson Formatting Baseline

The enhanced lesson schema is defined in `types.ts` and rendered in `BlockRenderer.tsx`.

| Lesson element | Web behavior | Native Android target |
| --- | --- | --- |
| Prose | Markdown text with relaxed line height | Rich text/Markdown-compatible Compose renderer |
| Table | Horizontal scroll, headers, borders, alternating row tint | Horizontally scrollable table with header semantics |
| Formula | Monospace framed block with language label | Formula/text block with fallback and copy if later added |
| Code | Monospace dark block, language label, horizontal overflow | Compose code block with horizontal scroll and language label |
| Tip/warning | Colored callout cards | Native callout components |
| Example | Expandable/collapsible block with chevron rotation over 150ms | Expandable card or instant reveal under reduced motion |
| Step-by-step | Ordered list after stripping `Step N:` prefix | Ordered Compose block preserving step order |
| List | Ordered/unordered detection from text prefix | Native list renderer |
| SVG | Sanitized SVG string rendered as diagram if valid | Native vector/image rendering strategy or safe fallback |
| Check understanding | Inline reveal cards with answer/rationale and `aria-expanded` | Native inline checks with expanded state and accessibility announcements |
| Segmented lessons | `DesktopLessonLayout` dispatches segmented layout when parser marks lesson segmented | Segment-aware Android reader with gated continue behavior |
| Companion panels | Practice panel and lesson chat use `/v1/tutor/lesson-chat` and rating endpoints | Native bottom sheet/tab/companion screen with context and retry |

## Assessment Baseline

### Quiz

- Phases: `select-mode`, `in-progress`, `submitted`, and special `lesson-blocked`.
- Quiz mode cards animate with scale-in and staggered list entry.
- Answer options use pressed/hover scale, `aria-pressed`, selected styling, and disabled/submitting states.
- Sticky in-progress header includes question progress, timer, and progress bar.
- Timer auto-submits on expiry.
- Low-time timer pulse is disabled under reduced motion.
- Results scale in and list questions with staggered cards, correctness color, selected answer, correct answer, and inline explanation.
- Lesson-blocked state is triggered by 409 `LESSON_NOT_COMPLETED`.

Native target: preserve the state machine, scoped attempt URLs, timer behavior, selected/disabled/submitting states, accessibility labels, result review, and reduced-motion behavior.

### Mock Exam

- Start screen explains 50 questions, 3 hours, 80 percent pass, and lockout expectation.
- Active exam uses local countdown interval seeded from `remaining_seconds`.
- Visibility loss posts `:report-focus-loss`.
- Answer persistence patches each answer.
- Low-time timer uses `gentle-pulse` and `role="timer"`.
- Supports linear no-revisit disabled state when `nav_policy` is `LINEAR_NO_REVISIT`.
- Submitted results scale in, show score/pass status, weakness summary, per-question answer/correct/explanation cards.

Native target: preserve timer accuracy, focus-loss reporting policy, answer persistence, no-revisit disabling, submit loading, and result review.

## Flashcard Study Baseline

- Phases: loading, studying, summary, error.
- Study modes: swipe and typing.
- Swipe mode reveals back side on tap, then shows confidence actions.
- Typing mode checks answer similarity at 0.8 threshold and maps similarity to confidence.
- Confidence options: forgot/guessed, unsure, confident, mastered.
- Card changes use `AnimatePresence` wait mode with opacity/y transition.
- Progress bar width transitions over 300ms.
- Offline network failures queue `flashcard_review` events through IndexedDB and continue through the session, but cannot fully end the session offline.
- Summary shows reviewed count, correct count, XP earned, and duration.

Native target: implement native reveal/typing/confidence flow, preserve summary metrics, and replace browser IndexedDB with Room/WorkManager only after idempotent sync is confirmed.

## Focus Baseline

- State machine: `IDLE`, `WORKING`, `BREAK`, `PAUSED`, `DONE`.
- Modes: 25/5, 50/10, custom.
- Timer state persists in `localStorage` as `csnexus_focus_state`.
- Visibility changes while working increment distractions.
- Timer ticks every second and switches from work to break or done.
- Backend session create may fail without blocking local timer.
- Completion posts total focus minutes and distractions, then refreshes stats.
- Reset abandons server session if present.
- Timer display uses `role="timer"` and an accessible label.

Native target: use lifecycle-aware timer state, DataStore/Room persistence as needed, WorkManager sync only for idempotent completion, Android notification/background policy if later required.

## Chart And Analytics Baseline

- Charts are custom SVG, not a third-party chart library.
- Bar, line, donut, heat map, and progress ring expose `role="img"` or `role="progressbar"` and basic `aria-label`.
- Progress ring animates by stroke dash offset unless reduced motion is active.
- Heat map includes less/more legend.

Native target: use Compose Canvas or a vetted native chart library, preserve labels/legends/selected states, and provide richer accessible summaries than the current web labels where possible.

## Native Motion Mapping

| Web intent | Native Android mapping |
| --- | --- |
| Route crossfade/slide | Navigation Compose transitions with reduced-motion fallback |
| Desktop/mobile shell switch | Adaptive scaffold for phone/tablet |
| Hover feedback | Pressed, focused, selected, long-press, or menu affordance |
| Glass card hover/lift | Press/focus state, selected border, tonal elevation |
| Button ripple/scale/spinner | Material ripple, optional pressed scale, native loading indicator |
| Expandable lesson examples | Animated visibility or instant reveal |
| Inline check answer reveal | Expand/collapse with state announcement |
| Quiz answer feedback | Stable selected/disabled/submitting states and short press feedback |
| Flashcard reveal | Native flip/fade depending on reduced motion |
| Timer pulse | Non-blocking warning color/pulse with reduced-motion fallback |
| Chart transitions | Canvas animation with static accessible summary |
| Reward/XP feedback | Lightweight animation that never blocks navigation |
| Destructive admin action | Explicit confirmation dialog/sheet |
| Sync pending/failed | Status badges, snackbar/sheet retry, WorkManager state |

## Source-Derived Capture Completion

Task 1.3 is complete under the source-derived rule:

- Primary visual tokens were read and summarized.
- Motion primitives and reduced-motion behavior were read and mapped.
- Shell, lesson, quiz, mock exam, flashcard, focus, chart, and accessibility semantics were read from source.
- Native Android implementation targets are documented without requiring screenshot or recording files.
