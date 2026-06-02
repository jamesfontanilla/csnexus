# Implementation Plan: Premium UI Overhaul

## Overview

Extend the existing CSNexus design system and component library to deliver an Apple/Framer-quality aesthetic. All changes are additive — no existing token names, component APIs, or page routes are broken. The implementation follows a strict bottom-up dependency order: tokens → motion system → hooks → primitive components → composite components → pages → tests.

**Test runner:** Vitest + `@testing-library/react` (already installed). **PBT library:** `fast-check` (install as dev dependency in task 1.1).

---

## Tasks

- [x] 1. Foundation — install fast-check and extend design tokens
  - [x] 1.1 Install fast-check and verify test setup
    - Run `npm install --save-dev fast-check` inside `web/`
    - Confirm `web/src/__tests__/setup.ts` imports `@testing-library/jest-dom`
    - _Requirements: 18.1 (no new CSS framework), testing strategy_
  - [x] 1.2 Append new tokens to `web/src/design-system/tokens.css`
    - **Update existing palette values** in `:root {}` to the Obsidian + Gold palette:
      - `--color-primary: #0A0A0A` (true obsidian black)
      - `--color-secondary: #141414` (slightly lifted black)
      - `--color-accent: #C9A84C` (refined gold)
      - `--color-surface: #1C1C1C` (card surface)
      - `--color-muted: #6B6B6B` (neutral grey)
      - `--color-highlight: #F5F0E8` (warm white)
      - `--color-metallic: #E8C96A` (bright gold highlight)
      - `--color-background: #080808` (near-black)
      - `--color-background-warm: #050505` (deepest background)
      - `--color-text: #F0EBE0`, `--color-text-secondary: #9A9A9A`, `--color-text-muted: #555555`
      - Update glass tokens to white-tinted: `--glass-bg-subtle: rgba(255,255,255,0.03)`, medium `0.06`, strong `0.10`
      - Update glass borders: light `rgba(255,255,255,0.06)`, medium `0.10`, strong `0.18`
      - Update shadows to cool-tinted (black-based, not brown-based)
      - Update `--focus-ring` to gold: `0 0 0 3px rgba(201, 168, 76, 0.4)`
    - **Update font tokens** to Clash Display + Satoshi:
      - `--font-display: "Clash Display", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif`
      - `--font-family: "Satoshi", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif`
    - **Add Fontshare CDN imports** to `web/index.html` (or `web/src/main.tsx` via a `<link>` in the HTML template):
      - `https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&display=swap`
      - `https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600,700&display=swap`
    - Add heading style tokens `--heading-1-*` through `--heading-4-*` (Clash Display, tighter letter-spacing than before: -0.04em for h1)
    - Add surface elevation tokens `--surface-0` through `--surface-4` (white-tinted for obsidian base)
    - Add motion duration tokens: `--duration-instant`, `--duration-fast`, `--duration-normal`, `--duration-slow`, `--duration-page`
    - Add motion easing tokens: `--ease-standard`, `--ease-decelerate`, `--ease-accelerate`, `--ease-spring`
    - Add spatial scale tokens: `--density-compact-padding/gap`, `--density-comfortable-padding/gap`, `--density-spacious-padding/gap`
    - Add interactive state tokens: `--state-hover-bg`, `--state-active-bg`, `--state-focus-ring`, `--state-disabled-opacity`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_
  - [x] 1.3 Write property test for spatial scale tokens (Property 1)
    - **Property 1: Spatial Scale Tokens Are Strictly Positive**
    - **Validates: Requirements 1.5**
    - Parse the CSS file and assert that all six density token values are > 0

- [x] 2. Append utility classes to `web/src/design-system/utilities.css`
  - [x] 2.1 Add button ripple animation classes
    - Append `.btn-ripple` class and `@keyframes btn-ripple-expand` as specified in the design
    - Add mobile touch-target override: all size variants enforce `min-height: 44px` on viewports < 640px
    - _Requirements: 3.4, 3.8_
  - [x] 2.2 Add skeleton shimmer fix
    - Replace the existing `@keyframes shimmer-glow` and `.skeleton` rule with the corrected 2-second `background-position`-based shimmer
    - Add `@media (prefers-reduced-motion: reduce)` block that disables shimmer
    - _Requirements: 9.1, 9.3, 9.4_
  - [x] 2.3 Add badge pulse animation classes
    - Append `@keyframes badge-pulse` and `.badge-dot-pulse` with reduced-motion override
    - _Requirements: 7.2, 7.3_
  - [x] 2.4 Add timer pulse animation class
    - Append `@keyframes timer-pulse` and `.timer-pulse` with reduced-motion override
    - _Requirements: 13.5_
  - [x] 2.5 Add bottom navigation layout classes
    - Append `.bottom-nav`, `.bottom-nav-item`, and `.bottom-nav-item.active` as specified in the design
    - Include iOS safe-area inset padding
    - _Requirements: 15.1, 15.2_

- [x] 3. Extend `web/src/design-system/motion.ts` with new exports
  - [x] 3.1 Add new motion variant exports
    - Export `pageTransition`, `cardStaggerContainer`, `cardStaggerItem`, `hoverLift`, `pressFeedback`, `toastSlideIn`
    - Export `makeReducedVariants` factory function
    - Do NOT modify or rename any existing exports (`springDefault`, `springGentle`, `springBouncy`, `fadeIn`, `slideUp`, `slideDown`, `scaleIn`, `staggerContainer`, `staggerItem`, `useReducedMotion`, `useMotionVariants`)
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.7_
  - [x] 3.2 Write property test for press feedback scale values (Property 20)
    - **Property 20: Press Feedback Scale Values**
    - **Validates: Requirements 16.4**
    - Assert `pressFeedback.whileTap.scale === 0.97` and `pressFeedback.whileHover.scale === 1.02`
  - [x] 3.3 Write property test for reduced-motion duration invariant (Property 18)
    - **Property 18: Reduced-Motion Duration Invariant**
    - **Validates: Requirements 16.7, 17.5**
    - Use `fc.record(...)` to generate arbitrary variant objects; pass through `makeReducedVariants(variants, true)` and assert effective duration ≤ 80ms and all `x`, `y`, `scale` values are identity

- [x] 4. Implement new hooks
  - [x] 4.1 Create `web/src/hooks/useFocusTrap.ts`
    - Implement `useFocusTrap(isActive: boolean): React.RefObject<HTMLElement>` as specified in the design
    - Save previously focused element on activation; restore it on cleanup
    - Suppress Tab when zero focusable elements exist; fall back to `document.body` if trigger element is gone
    - Export as named export
    - _Requirements: 6.3, 6.4, 17.6_
  - [x] 4.2 Create `web/src/hooks/useScrollReveal.ts`
    - Implement `useScrollReveal(options?)` returning `[ref, motionProps]`
    - Use existing `useInView` hook; apply `makeReducedVariants` when `useReducedMotion()` is true
    - Export as named export
    - _Requirements: 11.4, 16.1_

- [x] 5. Update `GlassCard` component
  - [x] 5.1 Add `elevation` and `premium` props to `web/src/components/GlassCard.tsx`
    - Add `elevation?: 'flat' | 'raised' | 'floating'` prop; map to glass class + surface/shadow tokens per design table
    - Add `premium?: boolean` prop; apply `.glass-card-premium` class when true
    - Implement hover animation: `raised`/`floating` → `translateY(-2px)` + shadow increase over `--duration-fast` using `--ease-standard`; `flat` → border-color only
    - Implement entrance animation: `initial={{ opacity: 0, y: 8 }}` → `animate={{ opacity: 1, y: 0 }}` over `--duration-normal`; skip when `useReducedMotion()` is true
    - Preserve all existing props unchanged (`blur`, `hoverable`, `lifted`, `onClick`, `style`, `as`)
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 18.5, 18.6_
  - [x] 5.2 Write property test for GlassCard elevation distinctness (Property 2)
    - **Property 2: GlassCard Elevation Produces Distinct Visual Levels**
    - **Validates: Requirements 2.1**
    - Use `fc.uniqueArray(fc.constantFrom('flat','raised','floating'), { minLength: 2, maxLength: 2 })` to generate pairs; render both and assert different class names / inline style values
  - [x] 5.3 Write unit tests for GlassCard
    - Test that `premium` prop adds `.glass-card-premium` class
    - Test that entrance animation is skipped when `prefers-reduced-motion` is active
    - _Requirements: 2.3, 2.5_

- [x] 6. Update `GlassButton` component
  - [x] 6.1 Add size variants, icon props, loading state, and ripple to `web/src/components/GlassButton.tsx`
    - Add `size?: 'sm' | 'md' | 'lg' | 'xl'` with token-mapped padding/font-size/min-height per design table
    - Add `iconLeft?: React.ReactNode` and `iconRight?: React.ReactNode` props
    - Update `loading` prop: replace children with spinner span, set `aria-busy="true"`, apply `cursor: not-allowed`
    - Implement ripple via `pointerdown` handler using `buttonRef`; skip when `disabled`, `loading`, or `reducedMotion`
    - Apply `whileTap={{ scale: 0.97 }}` / `whileHover={{ scale: 1.02 }}` using `springDefault`; set to `undefined` when `reducedMotion`
    - Apply `cursor: not-allowed` when `loading || disabled`
    - Preserve all existing variant styles (`primary`, `secondary`, `ghost`, `danger`) and props unchanged
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 18.5, 18.6_
  - [x] 6.2 Write property test for GlassButton loading state invariant (Property 3)
    - **Property 3: GlassButton Loading State Invariant**
    - **Validates: Requirements 3.3**
    - Use `fc.string({ minLength: 1 })` for label; render `<GlassButton loading>{label}</GlassButton>`; assert `aria-busy="true"` and label not in DOM
  - [x] 6.3 Write property test for GlassButton cursor invariant (Property 4)
    - **Property 4: GlassButton Cursor Invariant**
    - **Validates: Requirements 3.6**
    - Use `fc.boolean()` for `loading` and `disabled`; when either is true, assert `cursor: not-allowed`
  - [x] 6.4 Write property test for GlassButton touch target (Property 5)
    - **Property 5: GlassButton Touch Target on Mobile**
    - **Validates: Requirements 3.8**
    - Use `fc.constantFrom('sm','md','lg','xl')` for size; mock viewport < 640px; assert computed min-height ≥ 44px
  - [x] 6.5 Write unit tests for GlassButton
    - Test icon rendering with `iconLeft` and `iconRight`
    - Test that ripple is skipped when `prefers-reduced-motion` is active
    - Test that existing variants render without regression
    - _Requirements: 3.2, 3.7, 3.9_

- [x] 7. Update `GlassBadge` component
  - [x] 7.1 Add `dot` and `pulse` props to `web/src/components/GlassBadge.tsx`
    - Add `dot?: boolean` prop: render an 8×8px circle `<span>` before label text
    - Add `pulse?: boolean` prop: apply `.badge-dot-pulse` class to dot span when `pulse && !reducedMotion`
    - Add `'info'` to the `color` variant union; map to `var(--color-info)`
    - Preserve all existing props unchanged
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 18.5, 18.6_
  - [x] 7.2 Write property test for GlassBadge pulse respects reduced motion (Property 10)
    - **Property 10: GlassBadge Pulse Respects Reduced Motion**
    - **Validates: Requirements 7.2, 7.3**
    - Use `fc.string()` for label; mock `prefers-reduced-motion: reduce`; render with `pulse={true}`; assert `.badge-dot-pulse` is NOT present
  - [x] 7.3 Write property test for GlassBadge color variant token mapping (Property 11)
    - **Property 11: GlassBadge Color Variant Token Mapping**
    - **Validates: Requirements 7.4**
    - Use `fc.constantFrom('success','warning','danger','info','accent')` for color; assert rendered element uses the corresponding CSS custom property

- [x] 8. Update `GlassSkeleton` component
  - [x] 8.1 Add `lines` prop and fix shimmer to `web/src/components/GlassSkeleton.tsx`
    - Add `lines?: number` prop: when `lines > 1`, render N stacked skeleton bars with widths 100%, 85%, 70%, … (decreasing by 15% per line)
    - Update component to use the `.skeleton` class from the corrected `utilities.css` (task 2.2) rather than any inline animation
    - Ensure only CSS `transform` and `opacity` are used for animation (background-position shimmer satisfies this)
    - Preserve all existing props (`width`, `height`, `borderRadius`, `variant`)
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 18.5, 18.6_
  - [x] 8.2 Write unit tests for GlassSkeleton
    - Test that `lines={3}` renders 3 skeleton bars
    - Test that shimmer animation is absent when `prefers-reduced-motion` is active
    - _Requirements: 9.2, 9.3_

- [x] 9. Create `Typography` component system
  - [x] 9.1 Create `web/src/components/Typography.tsx` with five named exports
    - Implement `Heading` (level 1–4, maps to `h1`–`h4` + `--heading-{level}-*` tokens, optional `gradient` prop)
    - Implement `Body` (size `sm`/`base`/`lg`, `max-width: 680px`, `line-height: 1.7`, `color: var(--color-text)`)
    - Implement `Caption` (`--font-size-sm`, `--color-text-secondary`, `line-height: 1.5`)
    - Implement `Label` (`htmlFor`, `required` props; renders `<label>`)
    - Implement `Code` (`inline` prop; monospace font stack; glass background + `padding: 0 var(--space-2)` for inline, `var(--space-4)` for block)
    - All styles via inline CSS custom properties — no CSS-in-JS, no token file import
    - Export all five as named exports
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 18.5, 18.6_
  - [x] 9.2 Write property test for Heading level token mapping (Property 6)
    - **Property 6: Heading Level Maps to Correct Token Group**
    - **Validates: Requirements 4.2**
    - Use `fc.integer({ min: 1, max: 4 })` for level; assert rendered element tag is `h{level}` and inline style references `--heading-{level}-size`
  - [x] 9.3 Write property test for Typography WCAG AA contrast (Property 7)
    - **Property 7: Typography WCAG AA Contrast**
    - **Validates: Requirements 4.6, 17.2**
    - For each component, compute contrast ratio between resolved text color and `--color-background` (#2C1810); assert ≥ 4.5:1 for normal text, ≥ 3:1 for large text
  - [x] 9.4 Write unit tests for Typography components
    - Test `Body` renders with `max-width: 680px`
    - Test `Caption` uses `--color-text-secondary`
    - Test `Code` inline vs block rendering
    - _Requirements: 4.3, 4.4, 4.5_

- [x] 10. Create `ProgressRing` component
  - [x] 10.1 Create `web/src/components/ProgressRing.tsx`
    - Implement SVG-based circular progress with `linearGradient` (accent → metallic) and `feDropShadow` glow filter
    - Accept `size`, `value` (clamped to 0–100), `strokeWidth` (default 8), `label`, `children` props
    - Use `useId()` for stable, unique gradient and filter IDs
    - Mount animation: start at `strokeDashoffset = circumference`, transition to target; skip when `useReducedMotion()` is true
    - Set `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-label` on SVG root; `role="progressbar"`
    - Handle edge cases: `NaN`/`undefined` → 0; `size ≤ 0` → return null; `strokeWidth > size/2` → clamp to `size/4`
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 18.5, 18.6_
  - [x] 10.2 Write property test for ProgressRing value clamping (Property 12)
    - **Property 12: ProgressRing Value Clamping**
    - **Validates: Requirements 8.7**
    - Use `fc.float({ noNaN: true })` for value; render and assert `stroke-dashoffset` corresponds to a percentage in [0, 1]
  - [x] 10.3 Write unit tests for ProgressRing
    - Test ARIA attributes are present with correct values
    - Test that reduced-motion skips the mount animation
    - Test that `size=0` returns null
    - _Requirements: 8.5, 8.6_

- [x] 11. Update `GlassModal` with focus trap and ARIA
  - [x] 11.1 Refactor `web/src/components/GlassModal.tsx` to use `useFocusTrap`
    - Replace any existing inline focus-trap logic with the `useFocusTrap` hook from task 4.1
    - Make `title` prop required; auto-generate `titleId` via `useId()` if not provided
    - Add `role="dialog"`, `aria-modal="true"`, `aria-labelledby={titleId}` to panel element
    - Add `id={titleId}` to the title `<h2>` element
    - Backdrop: `backdrop-filter: blur(12px)` + semi-transparent dark overlay
    - Entrance animation: `scaleIn` variant (scale 0.95→1, opacity 0→1) over `--duration-normal` using `--ease-spring`
    - Reduced-motion: opacity-only transition at `--duration-fast`; preserve spring for non-transform properties
    - Preserve existing `size` prop and `onClose` behavior
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 17.6, 18.5, 18.6_
  - [x] 11.2 Write property test for GlassModal focus trap completeness (Property 9)
    - **Property 9: GlassModal Focus Trap Completeness**
    - **Validates: Requirements 6.3, 17.6**
    - Use `fc.integer({ min: 1, max: 8 })` for N buttons; render modal with N buttons; Tab from last → assert focus on first; Shift+Tab from first → assert focus on last
  - [x] 11.3 Write unit tests for GlassModal
    - Test `role="dialog"` and `aria-modal="true"` are present
    - Test `aria-labelledby` references the title element's `id`
    - Test that Escape key calls `onClose`
    - _Requirements: 6.4, 6.6_

- [x] 12. Upgrade Toast system
  - [x] 12.1 Rewrite `web/src/context/ToastContext.tsx` with `useReducer`
    - Replace `useState` array with `useReducer` using `toastReducer` as specified in the design
    - Implement `ADD`, `REMOVE`, `PAUSE`, `RESUME` actions
    - Add `warning` variant to `ToastVariant` union
    - Implement hover-pause: `onMouseEnter` dispatches `PAUSE`, `onMouseLeave` dispatches `RESUME`
    - Implement progress bar: local `remaining` state decremented by `setInterval`; interval cleared when `paused`; bar width = `(remaining / duration) * 100%`
    - Enforce max 5 concurrent toasts: when 6th is added, remove oldest first
    - Default `duration` to 4000ms; clamp to 4000ms if ≤ 0
    - Slide-in animation: `toastSlideIn` variant from motion.ts; opacity-only when `reducedMotion`
    - ARIA: `role="alert"` for `error`, `role="status"` for all others
    - Stacking: `display: flex; flex-direction: column; gap: var(--space-3)`
    - Throw descriptive error if `useToast` is called outside `ToastProvider`
    - Export `ToastProvider` and `useToast` as named exports
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 17.7, 18.5_
  - [x] 12.2 Write property test for Toast stacking gap invariant (Property 13)
    - **Property 13: Toast Stacking Gap Invariant**
    - **Validates: Requirements 10.2**
    - Use `fc.integer({ min: 1, max: 5 })` for N toasts; render N toasts; assert container has `gap: var(--space-3)`
  - [x] 12.3 Write property test for Toast variant color mapping (Property 14)
    - **Property 14: Toast Variant Color Mapping**
    - **Validates: Requirements 10.5**
    - Use `fc.constantFrom('success','error','warning','info')` for variant; assert left-border color matches semantic token
  - [x] 12.4 Write unit tests for Toast system
    - Test `role="alert"` for error toasts and `role="status"` for info/success/warning
    - Test that hover pauses the auto-dismiss timer
    - Test that `useToast` outside provider throws descriptive error
    - _Requirements: 10.4, 10.7, 17.7_

- [x] 13. Checkpoint — verify foundation and primitive components
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. Create `BottomNav` component
  - [x] 14.1 Create `web/src/components/BottomNav.tsx`
    - Implement `BottomNavItem` interface and `BOTTOM_NAV_ITEMS` constant as specified in the design
    - Render fixed bottom bar using `.bottom-nav` and `.bottom-nav-item` classes from task 2.5
    - Implement sliding active indicator using `<motion.div>` with `useMotionValue` and `animate()`
    - When `prefers-reduced-motion` is active, indicator jumps instantly (no spring transition)
    - Use `NavLink` from `react-router-dom` for active state detection
    - Export as named export; do not import `tokens.css` as a JS module
    - _Requirements: 15.1, 15.2, 15.6, 18.5, 18.6_
  - [x] 14.2 Write unit tests for BottomNav
    - Test that active item has `.active` class
    - Test that indicator animation is skipped when `prefers-reduced-motion` is active
    - _Requirements: 15.2, 15.6_

- [x] 15. Integrate `BottomNav` into `GlassNavbar`
  - [x] 15.1 Update `web/src/components/GlassNavbar.tsx` to render `BottomNav` on mobile
    - Import and render `<BottomNav />` when viewport width < 768px (use a `useMediaQuery` hook or CSS `hidden` class)
    - Hide the existing hamburger menu when bottom nav is active
    - Add `padding-bottom: 80px` to `<main>` when bottom nav is visible to prevent content occlusion
    - _Requirements: 15.1, 15.3_
  - [x] 15.2 Write unit tests for GlassNavbar mobile/desktop switching
    - Test that BottomNav renders at viewport < 768px
    - Test that hamburger menu is hidden when BottomNav is active
    - _Requirements: 15.1, 15.3_

- [x] 16. Overhaul `Home.tsx`
  - [x] 16.1 Update `web/src/pages/Home.tsx` with scroll reveals, social proof, and stagger
    - Wrap each `<section>` in `<motion.div>` using `useScrollReveal()`; when `reducedMotion`, `motionProps` is `{}`
    - Add social proof section with `AnimatedCounter` (wraps `AnimatedNumber`) that starts counting when section enters viewport via `useScrollReveal`
    - Update `FeaturesSection` to use `cardStaggerContainer` / `cardStaggerItem` (50ms stagger) from motion.ts
    - Apply `GlassCard` with `elevation="raised"` and `hoverable` to feature cards
    - Hero headline: ensure `--font-size-5xl` or larger with animated gradient text via `GradientText`
    - Stagger configuration applied regardless of reduced-motion state; only transforms/opacity stripped
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 16.2_
  - [x] 16.2 Write unit tests for Home page
    - Test that social proof section renders `AnimatedCounter`
    - Test that sections render in final state when `prefers-reduced-motion` is active
    - _Requirements: 11.3, 11.6_

- [x] 17. Create `Dashboard.tsx` page
  - [x] 17.1 Create `web/src/pages/Dashboard.tsx`
    - Hero section: `<ProgressRing size={200} value={readinessScore} label="Readiness" />`; animate from 0 to score via `useEffect` on mount
    - Quick stats row: streak, XP today, questions today — each as `<AnimatedNumber>` with `duration={1000}` counting up on mount
    - Daily queue card: list of `DailyQueueItem` with type icon and estimated minutes; use `GlassCard elevation="raised"`
    - Top impact areas: horizontal bar indicators per subject using `GlassProgressBar` or inline bar
    - Loading state: render `GlassSkeleton` placeholders matching each section's shape; section structure does NOT render until data is available; skeletons disappear immediately when data arrives (no fade delay)
    - Error state: render `EmptyState` with retry button if API call fails; show error state after 10s if still pending
    - Define `DashboardData`, `DailyQueueItem`, `ImpactArea` TypeScript interfaces in the file
    - Export as named export
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 18.5_
  - [x] 17.2 Write unit tests for Dashboard page
    - Test that skeleton placeholders render while loading
    - Test that `ProgressRing` receives `value={0}` initially then the actual score
    - Test that `AnimatedNumber` components are present for streak, XP, and questions
    - _Requirements: 12.2, 12.4, 12.6_

- [x] 18. Update `QuizPlayer.tsx`
  - [x] 18.1 Update `web/src/pages/quiz/QuizPlayer.tsx` with premium layout and interactions
    - Question card: enforce `padding: var(--space-6)` on all sides; clear typographic hierarchy (question stem vs options)
    - Answer options: `min-height: 56px`, `padding: var(--space-4) var(--space-5)`, `min Touch_Target: 44×44px` on mobile
    - Selected answer: apply `border: 1.5px solid var(--color-accent)` + `box-shadow: 0 0 0 3px rgba(212,165,116,0.2)` (glow); `whileTap={{ scale: 1.02 }}` within `--duration-instant`; skip scale when `reducedMotion` but keep glow
    - Progress bar: sticky header, CSS transition `--duration-normal`
    - Timer: when `remaining < 30`, set `color: var(--color-danger)` + add `.timer-pulse` class; when `remaining === 0`, switch to "time expired" state with distinct styling
    - Results page: `AnimatedNumber` count-up over 1200ms for final score; review cards with left border `--color-success` (correct) or `--color-danger` (incorrect)
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9_
  - [x] 18.2 Write property test for quiz answer option minimum height (Property 15)
    - **Property 15: Quiz Answer Option Minimum Height**
    - **Validates: Requirements 13.2**
    - Use `fc.array(fc.string({ minLength: 1 }), { minLength: 2, maxLength: 6 })` for options; render and assert each option has `min-height: 56px`
  - [x] 18.3 Write property test for quiz timer color below 30 seconds (Property 16)
    - **Property 16: Quiz Timer Color Below 30 Seconds**
    - **Validates: Requirements 13.5**
    - Use `fc.integer({ min: 0, max: 29 })` for remaining; assert timer uses `var(--color-danger)`
  - [x] 18.4 Write property test for quiz results border color correctness (Property 17)
    - **Property 17: Quiz Results Border Color Correctness**
    - **Validates: Requirements 13.9**
    - Use `fc.boolean()` for `is_correct`; assert left border is `var(--color-success)` when true, `var(--color-danger)` when false
  - [x] 18.5 Write unit tests for QuizPlayer
    - Test that "time expired" state is visually distinct from sub-30s warning state
    - Test that answer selection glow persists when `prefers-reduced-motion` is active
    - _Requirements: 13.6, 13.7_

- [x] 19. Update `LessonReader.tsx`
  - [x] 19.1 Update `web/src/pages/content/LessonReader.tsx` with reading layout and progress
    - Constrain reading column to `max-width: 680px`, centered; `line-height: 1.75`, `font-size: var(--font-size-base)`
    - Reading progress indicator: `position: fixed; top: 0; height: 3px; background: linear-gradient(90deg, var(--color-accent), var(--color-metallic))`; width updated via `scroll` event listener
    - Desktop (≥ 1024px): sticky section sidebar (`width: 220px; position: sticky; top: 80px`) listing headings; active heading highlighted via `useInView`; sidebar renders even if highlighting fails
    - Mobile (< 1024px): section navigation as collapsible bottom panel (`<details>` or controlled `<div>` with `position: fixed; bottom: 0`)
    - Smooth scroll: `scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' })`
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_
  - [x] 19.2 Write unit tests for LessonReader
    - Test that reading column has `max-width: 680px`
    - Test that sidebar renders even when no headings are found (no active highlight)
    - Test that smooth scroll uses `'auto'` behavior when `prefers-reduced-motion` is active
    - _Requirements: 14.1, 14.4, 14.6_

- [x] 20. Checkpoint — verify all pages and composite components
  - Ensure all tests pass, ask the user if questions arise.

- [x] 21. Property-based tests for tree-shaking and module hygiene
  - [x] 21.1 Write property test for named exports invariant (Property 21)
    - **Property 21: New Components Are Named Exports**
    - **Validates: Requirements 18.5**
    - For each new component file (`Typography.tsx`, `ProgressRing.tsx`, `BottomNav.tsx`), assert the file contains `export function` or `export const` and does NOT contain `export default`
  - [x] 21.2 Write property test for no token CSS import as JS module (Property 22)
    - **Property 22: Components Do Not Import Token CSS as JS Module**
    - **Validates: Requirements 18.6**
    - Scan all files in `web/src/components/` and assert none contain `import.*tokens\.css` or `import.*utilities\.css`

- [x] 22. Property-based tests for GlassInput character count
  - [x] 22.1 Write property test for GlassInput character count accuracy (Property 8)
    - **Property 8: GlassInput Character Count Accuracy**
    - **Validates: Requirements 5.4**
    - Use `fc.string()` for value and `fc.integer({ min: 1, max: 500 })` for `maxLength`; render `<GlassInput value={value} maxLength={maxLength} />`; assert displayed count equals `value.length`

- [x] 23. Property-based tests for AnimatedNumber duration range
  - [x] 23.1 Write property test for AnimatedNumber duration range (Property 19)
    - **Property 19: AnimatedNumber Duration Range**
    - **Validates: Requirements 16.5**
    - Use `fc.integer({ min: 0, max: 100000 })` for value; render `<AnimatedNumber value={value} />`; assert `data-duration` attribute is between 800 and 1500 (add `data-duration` attribute to `AnimatedNumber` for testability)

- [x] 24. Accessibility verification
  - [x] 24.1 Add `@axe-core/react` integration in development mode
    - Install `@axe-core/react` as a dev dependency
    - In `web/src/main.tsx`, conditionally initialize axe in development mode only: `if (import.meta.env.DEV) { ... }`
    - _Requirements: 17.1, 17.2, 17.3, 17.4_
  - [x] 24.2 Write axe-core unit tests for all new/updated components
    - Run `axe(container)` on rendered `GlassModal`, `GlassButton` (icon-only variant), `ProgressRing`, `Toast` (error and info variants), `BottomNav`
    - Assert zero violations for each
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.6, 17.7_

- [x] 25. Final checkpoint — full test suite and build verification
  - Run `npm run test` inside `web/` and ensure all tests pass
  - Run `npm run build` inside `web/` and ensure TypeScript compilation succeeds with zero errors
  - Ensure all tests pass, ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- The dependency order is strict: tokens → utilities → motion → hooks → primitive components → composite components → pages → tests
- All new components must be named exports — no default exports
- No component may import `tokens.css` or `utilities.css` as a JavaScript module; tokens are consumed via CSS custom properties only
- `fast-check` must be installed before any property test tasks run (task 1.1)
- Property tests use a minimum of 100 iterations (fast-check default)
- Each property test file includes a comment: `// Feature: premium-ui-overhaul, Property N: <title>`
- Checkpoints at tasks 13 and 20 validate incremental progress before moving to pages and final tests

---

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3", "2.1", "2.2", "2.3", "2.4", "2.5"] },
    { "id": 3, "tasks": ["3.1"] },
    { "id": 4, "tasks": ["3.2", "3.3", "4.1", "4.2"] },
    { "id": 5, "tasks": ["5.1", "6.1", "7.1", "8.1", "9.1", "10.1"] },
    { "id": 6, "tasks": ["5.2", "5.3", "6.2", "6.3", "6.4", "6.5", "7.2", "7.3", "8.2", "9.2", "9.3", "9.4", "10.2", "10.3"] },
    { "id": 7, "tasks": ["11.1"] },
    { "id": 8, "tasks": ["11.2", "11.3", "12.1"] },
    { "id": 9, "tasks": ["12.2", "12.3", "12.4", "14.1"] },
    { "id": 10, "tasks": ["14.2", "15.1"] },
    { "id": 11, "tasks": ["15.2", "16.1", "17.1", "18.1", "19.1"] },
    { "id": 12, "tasks": ["16.2", "17.2", "18.2", "18.3", "18.4", "18.5", "19.2"] },
    { "id": 13, "tasks": ["21.1", "21.2", "22.1", "23.1"] },
    { "id": 14, "tasks": ["24.1"] },
    { "id": 15, "tasks": ["24.2"] }
  ]
}
```
