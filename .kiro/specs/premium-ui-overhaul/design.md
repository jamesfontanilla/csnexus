# Design Document: Premium UI Overhaul

## Overview

This document describes the technical design for the premium UI overhaul of CSNexus. The overhaul extends — not replaces — the existing design system (`tokens.css`, `utilities.css`, existing component library) to deliver an Apple/Framer-quality aesthetic grounded in cognitive science research.

**Visual direction: Obsidian + Gold**
The palette shifts from warm espresso browns to true obsidian black with gold accents. This creates a more serious, premium, and authoritative feel — appropriate for a platform that wants to signal intelligence and justify a paid tier. The warm undertones are removed in favor of cool-neutral blacks and a refined gold that reads as precious rather than decorative.

**Typography: Clash Display + Satoshi**
- **Clash Display** (display/headings) — geometric, high-contrast, slightly editorial. Signals precision and authority. Loaded via Fontshare CDN.
- **Satoshi** (body/UI) — clean, modern, excellent readability at small sizes. Replaces Inter. Also via Fontshare CDN.
- **JetBrains Mono** (code) — unchanged, already the best choice for monospace.

**Key design principles:**
- All new tokens are additive CSS custom properties appended to `tokens.css`; no existing token names change
- All new components are additive named exports; no existing component APIs break
- Inline styles + CSS custom properties remain the styling pattern — no CSS-in-JS, no Tailwind
- Framer Motion (already installed) handles all JS-driven animation; no new animation libraries
- `prefers-reduced-motion` is respected at every animation site

**Research basis:** Cognitive Load Theory (Sweller, 1988), Aesthetic-Usability Effect (NNG), WCAG AA contrast (4.5:1 normal text, 3:1 large text), and feedback latency research (< 100ms for immediate feel, 200–400ms for premium transitions).

---

## Architecture

The overhaul is organized into four layers that build on each other:

```
┌─────────────────────────────────────────────────────────┐
│  Pages (Dashboard, Home, QuizPlayer, LessonReader)      │
│  Compose components into full-screen layouts            │
├─────────────────────────────────────────────────────────┤
│  Component Library (GlassCard, GlassButton, Toast, …)   │
│  Reusable UI primitives consuming design tokens         │
├─────────────────────────────────────────────────────────┤
│  Motion System (design-system/motion.ts)                │
│  Framer Motion variant library + hooks                  │
├─────────────────────────────────────────────────────────┤
│  Design Tokens (tokens.css + utilities.css)             │
│  CSS custom properties — single source of truth         │
└─────────────────────────────────────────────────────────┘
```

**Dependency rule:** Each layer may only import from the layer directly below it. Pages import components; components import motion variants and consume tokens via CSS custom properties; motion.ts imports nothing from the component layer.

**File locations:**
- Token additions → `web/src/design-system/tokens.css` (appended, no renames)
- Utility additions → `web/src/design-system/utilities.css` (appended)
- New motion variants → `web/src/design-system/motion.ts` (new exports added)
- New/updated components → `web/src/components/`
- New/updated pages → `web/src/pages/`
- Toast context (upgraded) → `web/src/context/ToastContext.tsx`
- Focus trap hook (new) → `web/src/hooks/useFocusTrap.ts`
- Scroll reveal hook (new) → `web/src/hooks/useScrollReveal.ts`

---

## Components and Interfaces

### 1. Design Token Additions (`tokens.css`)

All additions are appended inside the existing `:root {}` block. No existing token names are modified.

**The Obsidian + Gold palette replaces the warm espresso values in the existing tokens.** The existing token *names* (`--color-primary`, `--color-accent`, `--color-background`, etc.) are kept for backward compatibility, but their *values* are updated to the new palette. This is the one exception to the "additive only" rule — color values must change to achieve the visual direction.

**New palette values (replace existing in `:root`):**

```css
/* Obsidian + Gold Palette — replaces warm espresso values */
--color-primary:          #0A0A0A;   /* True obsidian black */
--color-secondary:        #141414;   /* Slightly lifted black */
--color-accent:           #C9A84C;   /* Refined gold */
--color-surface:          #1C1C1C;   /* Card surface */
--color-muted:            #6B6B6B;   /* Neutral grey */
--color-highlight:        #F5F0E8;   /* Warm white (text on dark) */
--color-metallic:         #E8C96A;   /* Bright gold highlight */
--color-background:       #080808;   /* Near-black background */
--color-background-warm:  #050505;   /* Deepest background */

/* Text Colors */
--color-text:             #F0EBE0;   /* Warm white — primary text */
--color-text-secondary:   #9A9A9A;   /* Mid grey — secondary text */
--color-text-muted:       #555555;   /* Dark grey — muted text */

/* Glass Tokens — updated for obsidian base */
--glass-bg-subtle:   rgba(255, 255, 255, 0.03);
--glass-bg-medium:   rgba(255, 255, 255, 0.06);
--glass-bg-strong:   rgba(255, 255, 255, 0.10);

--glass-border-light:   rgba(255, 255, 255, 0.06);
--glass-border-medium:  rgba(255, 255, 255, 0.10);
--glass-border-strong:  rgba(255, 255, 255, 0.18);

/* Shadows — cool-tinted for obsidian */
--shadow-ambient:   0 0 40px rgba(0, 0, 0, 0.6);
--shadow-depth:     0 8px 32px rgba(0, 0, 0, 0.7), 0 2px 8px rgba(0, 0, 0, 0.4);
--shadow-glow:      0 0 20px rgba(201, 168, 76, 0.20), 0 0 40px rgba(201, 168, 76, 0.08);
--shadow-diffused:  0 4px 16px rgba(0, 0, 0, 0.4), 0 1px 4px rgba(0, 0, 0, 0.2);
--shadow-lifted:    0 12px 40px rgba(0, 0, 0, 0.8), 0 4px 16px rgba(0, 0, 0, 0.5), 0 0 24px rgba(201, 168, 76, 0.10);
--shadow-subtle:    0 2px 8px rgba(0, 0, 0, 0.3), 0 1px 3px rgba(0, 0, 0, 0.2);

/* Focus ring — gold */
--focus-ring: 0 0 0 3px rgba(201, 168, 76, 0.4);

/* Typography — Clash Display + Satoshi */
--font-display: "Clash Display", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
--font-family:  "Satoshi", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

**New additive tokens (appended, not replacing):**

```css
/* --- Heading Style Tokens --- */
--heading-1-size: var(--font-size-5xl);
--heading-1-weight: 700;
--heading-1-line-height: 1.05;
--heading-1-letter-spacing: -0.04em;
--heading-1-font: var(--font-display);

--heading-2-size: var(--font-size-3xl);
--heading-2-weight: 600;
--heading-2-line-height: 1.15;
--heading-2-letter-spacing: -0.03em;
--heading-2-font: var(--font-display);

--heading-3-size: var(--font-size-2xl);
--heading-3-weight: 600;
--heading-3-line-height: 1.25;
--heading-3-letter-spacing: -0.02em;
--heading-3-font: var(--font-display);

--heading-4-size: var(--font-size-xl);
--heading-4-weight: 500;
--heading-4-line-height: 1.35;
--heading-4-letter-spacing: -0.01em;
--heading-4-font: var(--font-display);

/* --- Surface Elevation Tokens --- */
/* Obsidian surfaces: white-tinted layers over near-black */
--surface-0: rgba(255, 255, 255, 0.00);   /* base — transparent */
--surface-1: rgba(255, 255, 255, 0.03);   /* subtle */
--surface-2: rgba(255, 255, 255, 0.06);   /* medium */
--surface-3: rgba(255, 255, 255, 0.10);   /* strong */
--surface-4: rgba(255, 255, 255, 0.15);   /* floating */

--shadow-elevation-0: none;
--shadow-elevation-1: var(--shadow-subtle);
--shadow-elevation-2: var(--shadow-diffused);
--shadow-elevation-3: var(--shadow-depth);
--shadow-elevation-4: var(--shadow-lifted);
```

```css
/* --- Motion Duration Tokens --- */
--duration-instant: 80ms;
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 400ms;
--duration-page: 500ms;

/* --- Motion Easing Tokens --- */
--ease-standard:    cubic-bezier(0.4, 0, 0.2, 1);
--ease-decelerate:  cubic-bezier(0, 0, 0.2, 1);
--ease-accelerate:  cubic-bezier(0.4, 0, 1, 1);
--ease-spring:      cubic-bezier(0.34, 1.56, 0.64, 1);

/* --- Spatial Scale Tokens --- */
/* compact: tight density for data-heavy views */
--density-compact-padding: var(--space-3);   /* 12px */
--density-compact-gap:     var(--space-2);   /* 8px */
/* comfortable: default density */
--density-comfortable-padding: var(--space-6);  /* 24px */
--density-comfortable-gap:     var(--space-4);  /* 16px */
/* spacious: hero sections and landing pages */
--density-spacious-padding: var(--space-12); /* 48px */
--density-spacious-gap:     var(--space-8);  /* 32px */

/* --- Interactive State Tokens --- */
--state-hover-bg:    rgba(212, 165, 116, 0.08);
--state-active-bg:   rgba(212, 165, 116, 0.15);
--state-focus-ring:  0 0 0 3px rgba(212, 165, 116, 0.4);
--state-disabled-opacity: 0.45;
```

**Backward compatibility guarantee:** The existing tokens (`--glass-bg-subtle`, `--glass-bg-medium`, `--glass-bg-strong`, `--shadow-*`, `--transition-*`) are not renamed. The new `--surface-*` tokens reference the same underlying values, so components can migrate incrementally.

### 2. GlassCard Component

**File:** `web/src/components/GlassCard.tsx`

The existing `GlassCard` is extended with an `elevation` prop and a `premium` variant. All existing props (`blur`, `hoverable`, `lifted`, `onClick`, `style`, `as`) remain unchanged.

```typescript
type Elevation = 'flat' | 'raised' | 'floating';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  blur?: 'sm' | 'md' | 'lg';
  elevation?: Elevation;          // NEW — defaults to 'raised' when hoverable, else 'flat'
  premium?: boolean;              // NEW — enables inner radial glow on hover
  hoverable?: boolean;            // existing
  lifted?: boolean;               // existing (deprecated in favor of elevation='floating')
  onClick?: () => void;
  style?: CSSProperties;
  as?: 'div' | 'section' | 'article';
}
```

**Elevation mapping:**

| `elevation` | CSS class applied | Background token | Shadow token |
|---|---|---|---|
| `flat` | `glass-sm` | `--surface-1` | `--shadow-elevation-1` |
| `raised` | `glass-md` | `--surface-2` | `--shadow-elevation-2` |
| `floating` | `glass-lg` | `--surface-4` | `--shadow-elevation-4` |

**Hover animation (non-reduced-motion):**
- `raised` and `floating`: `translateY(-2px)` + shadow increases one level, over `--duration-fast` using `--ease-standard`
- `flat`: no transform, only border-color brightens

**Premium variant:** When `premium={true}`, the `.glass-card-premium` utility class is added. This class already exists in `utilities.css` and provides the `::after` radial glow pseudo-element. No new CSS is needed.

**Entrance animation:** `initial={{ opacity: 0, y: 8 }}` → `animate={{ opacity: 1, y: 0 }}` over `--duration-normal` (250ms). When `prefers-reduced-motion` is active, skip via `useReducedMotion()` hook (already in `design-system/motion.ts`).

### 3. GlassButton Component

**File:** `web/src/components/GlassButton.tsx`

All existing props and variant styles (`primary`, `secondary`, `ghost`, `danger`) are preserved unchanged. New props are additive.

```typescript
interface GlassButtonProps {
  children?: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'; // existing
  size?: 'sm' | 'md' | 'lg' | 'xl';                       // xl is NEW
  disabled?: boolean;                                       // existing
  loading?: boolean;                                        // existing
  iconLeft?: React.ReactNode;                               // NEW
  iconRight?: React.ReactNode;                              // NEW
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void; // updated signature
  type?: 'button' | 'submit' | 'reset';
  className?: string;
  style?: React.CSSProperties;
  'aria-label'?: string;
}
```

**Size token mapping:**

| `size` | `padding` | `font-size` | `min-height` |
|---|---|---|---|
| `sm` | `var(--space-2) var(--space-3)` | `var(--font-size-sm)` | `32px` |
| `md` | `var(--space-3) var(--space-5)` | `var(--font-size-base)` | `40px` |
| `lg` | `var(--space-4) var(--space-7)` | `var(--font-size-lg)` | `48px` |
| `xl` | `var(--space-5) var(--space-10)` | `var(--font-size-xl)` | `56px` |

On viewports < 640px, all sizes enforce `min-height: 44px` via a CSS media query in `utilities.css`.

**Ripple effect implementation:**

The ripple uses a React ref on the button element and a `pointerdown` event handler. No external library.

```typescript
// Inside GlassButton
const buttonRef = useRef<HTMLButtonElement>(null);

function handlePointerDown(e: React.PointerEvent<HTMLButtonElement>) {
  if (disabled || loading || reducedMotion) return;
  const btn = buttonRef.current;
  if (!btn) return;
  const rect = btn.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const ripple = document.createElement('span');
  ripple.className = 'btn-ripple';
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;
  btn.appendChild(ripple);
  // Remove after animation completes (--duration-fast = 150ms)
  ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
}
```

The `.btn-ripple` CSS class is added to `utilities.css`:

```css
.btn-ripple {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  transform: translate(-50%, -50%) scale(0);
  animation: btn-ripple-expand var(--duration-fast, 150ms) var(--ease-decelerate, cubic-bezier(0,0,0.2,1)) forwards;
  pointer-events: none;
}

@keyframes btn-ripple-expand {
  to { transform: translate(-50%, -50%) scale(40); opacity: 0; }
}
```

**Press feedback:** Framer Motion `whileTap={{ scale: 0.97 }}` on pointer-down, `whileHover={{ scale: 1.02 }}` on hover. The `transition` uses `springDefault` (already defined). When `reducedMotion` is true, both are set to `undefined`.

**Loading state:** When `loading={true}`, children are replaced with the existing spinner span, and `aria-busy="true"` is added to the button element. `cursor: not-allowed` is applied via inline style when `loading || disabled`.

### 4. Typography Components

**File:** `web/src/components/Typography.tsx`

New file exporting five components as named exports. No CSS-in-JS — all styles are inline using CSS custom properties.

```typescript
interface HeadingProps {
  level: 1 | 2 | 3 | 4;
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  gradient?: boolean; // wraps children in GradientText when true
}

interface BodyProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  size?: 'sm' | 'base' | 'lg';
}

interface CaptionProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

interface LabelProps {
  children: React.ReactNode;
  htmlFor?: string;
  className?: string;
  style?: React.CSSProperties;
  required?: boolean;
}

interface CodeProps {
  children: React.ReactNode;
  inline?: boolean; // true = <code>, false = <pre><code>
  className?: string;
  style?: React.CSSProperties;
}
```

**Heading rendering:** `level` maps to the HTML element (`h1`–`h4`) and the corresponding heading token group. Example for `level={1}`:

```typescript
const tagStyles: Record<number, React.CSSProperties> = {
  1: {
    fontSize: 'var(--heading-1-size)',
    fontWeight: 'var(--heading-1-weight)' as unknown as number,
    lineHeight: 'var(--heading-1-line-height)',
    letterSpacing: 'var(--heading-1-letter-spacing)',
    fontFamily: 'var(--heading-1-font)',
    color: 'var(--color-text)',
  },
  // ... 2, 3, 4
};
```

**Body rendering:** `max-width: 680px` (≈75 chars at base font size), `line-height: 1.7`, `color: var(--color-text)`.

**Code rendering:** Background `var(--glass-bg-subtle)`, border `1px solid var(--glass-border-light)`, `border-radius: var(--radius-sm)`, `padding: 0 var(--space-2)` for inline, `padding: var(--space-4)` for block. Font stack: `"JetBrains Mono", "Fira Code", "Cascadia Code", monospace`.

### 5. GlassModal Component

**File:** `web/src/components/GlassModal.tsx`

The existing `GlassModal` already has a basic focus trap. The overhaul extracts focus trapping into a dedicated hook and adds the missing ARIA attributes.

**`useFocusTrap` hook** (`web/src/hooks/useFocusTrap.ts`):

```typescript
const FOCUSABLE_SELECTORS = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

export function useFocusTrap(isActive: boolean): React.RefObject<HTMLElement> {
  const containerRef = useRef<HTMLElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isActive) return;
    // Save the element that had focus before the modal opened
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus the container itself (it has tabIndex={-1})
    containerRef.current?.focus();

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab' || !containerRef.current) return;
      const focusable = Array.from(
        containerRef.current.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTORS)
      ).filter(el => !el.closest('[aria-hidden="true"]'));
      if (focusable.length === 0) { e.preventDefault(); return; }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault(); last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault(); first.focus();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Return focus to the trigger element on cleanup
      previousFocusRef.current?.focus();
    };
  }, [isActive]);

  return containerRef as React.RefObject<HTMLElement>;
}
```

**Updated GlassModal props:**

```typescript
interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;           // now required (needed for aria-labelledby)
  titleId?: string;        // NEW — auto-generated if not provided
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
}
```

The modal panel element gets `role="dialog"`, `aria-modal="true"`, and `aria-labelledby={titleId}`. The title `<h2>` gets `id={titleId}`. The backdrop uses `backdrop-filter: blur(12px)`.

**Reduced-motion behavior:** When `prefers-reduced-motion` is active, the `scaleIn` variant is replaced with a pure opacity transition at `--duration-fast` (150ms). Scale and translate are set to `1` and `0` respectively in both `initial` and `animate` states.

### 6. Toast / Notification System

**File:** `web/src/context/ToastContext.tsx`

The existing `ToastContext` is upgraded from a simple `useState` array to a `useReducer`-based system that supports stacking, hover-pause, progress bars, and a `warning` variant.

**State shape:**

```typescript
type ToastVariant = 'success' | 'error' | 'warning' | 'info';

interface ToastItem {
  id: number;
  message: string;
  variant: ToastVariant;
  duration: number;       // ms, default 4000
  paused: boolean;        // true when hovered
  createdAt: number;      // Date.now() at creation
}

type ToastAction =
  | { type: 'ADD'; payload: Omit<ToastItem, 'id' | 'paused' | 'createdAt'> }
  | { type: 'REMOVE'; id: number }
  | { type: 'PAUSE'; id: number }
  | { type: 'RESUME'; id: number };
```

**Reducer:**

```typescript
function toastReducer(state: ToastItem[], action: ToastAction): ToastItem[] {
  switch (action.type) {
    case 'ADD':
      return [...state, { ...action.payload, id: nextId++, paused: false, createdAt: Date.now() }];
    case 'REMOVE':
      return state.filter(t => t.id !== action.id);
    case 'PAUSE':
      return state.map(t => t.id === action.id ? { ...t, paused: true } : t);
    case 'RESUME':
      return state.map(t => t.id === action.id ? { ...t, paused: false } : t);
    default:
      return state;
  }
}
```

**Context value:**

```typescript
interface ToastContextValue {
  success: (message: string, duration?: number) => void;
  error: (message: string, duration?: number) => void;
  warning: (message: string, duration?: number) => void;
  info: (message: string, duration?: number) => void;
  dismiss: (id: number) => void;
}
```

**Auto-dismiss with hover-pause:** Each `ToastItem` component uses a `useEffect` with `setInterval` that decrements a local `remaining` state. The interval is cleared when `paused` is true. The progress bar width is `(remaining / duration) * 100%`.

**Stacking layout:** The container uses `display: flex; flex-direction: column; gap: var(--space-3)`. Each toast slides in from `translateX(110%)` to `translateX(0)` over `--duration-fast` using `--ease-decelerate`. With `prefers-reduced-motion`, only opacity transitions.

**ARIA roles:** `variant === 'error'` → `role="alert"` (assertive). All others → `role="status"` (polite). The container `aria-live` attribute is removed from the wrapper; individual toasts carry their own roles.

**Variant colors:**

| variant | left-border | icon |
|---|---|---|
| `success` | `var(--color-success)` | `✓` |
| `error` | `var(--color-danger)` | `✕` |
| `warning` | `var(--color-warning)` | `⚠` |
| `info` | `var(--color-accent)` | `ℹ` |

### 7. ProgressRing Component

**File:** `web/src/components/ProgressRing.tsx` (new file)

```typescript
interface ProgressRingProps {
  size: number;           // diameter in pixels
  value: number;          // 0–100 (clamped internally)
  strokeWidth?: number;   // default 8
  label?: string;         // displayed in center; also used for aria-label
  children?: React.ReactNode; // rendered in center instead of label when provided
}
```

**SVG structure:**

```
<svg role="progressbar" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
  <defs>
    <linearGradient id="ring-gradient-{id}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stopColor="var(--color-accent)" />
      <stop offset="100%" stopColor="var(--color-metallic)" />
    </linearGradient>
    <filter id="ring-glow-{id}">
      <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="var(--color-accent)" floodOpacity="0.6" />
    </filter>
  </defs>
  <!-- Track circle -->
  <circle cx={center} cy={center} r={radius} fill="none"
    stroke="var(--glass-bg-medium)" strokeWidth={strokeWidth} />
  <!-- Progress circle -->
  <circle cx={center} cy={center} r={radius} fill="none"
    stroke="url(#ring-gradient-{id})"
    strokeWidth={strokeWidth}
    strokeLinecap="round"
    strokeDasharray={circumference}
    strokeDashoffset={offset}
    filter={clamped > 0 ? `url(#ring-glow-{id})` : undefined}
    transform={`rotate(-90 ${center} ${center})`}
    style={{ transition: reducedMotion ? 'none' : `stroke-dashoffset var(--duration-slow) var(--ease-decelerate)` }}
  />
</svg>
```

**Clamping:** `const clamped = Math.min(100, Math.max(0, value))` applied before any calculation.

**Circumference:** `2 * Math.PI * radius` where `radius = (size - strokeWidth) / 2`.

**Offset:** `circumference * (1 - clamped / 100)`.

**Mount animation:** On mount, the component starts with `strokeDashoffset = circumference` (0%) and transitions to the target offset. When `prefers-reduced-motion` is active, the initial offset is set directly to the target value — no transition.

**Unique gradient IDs:** Use `useId()` (React 18) to generate stable, unique IDs for the `linearGradient` and `filter` elements, preventing conflicts when multiple `ProgressRing` instances are on the same page.

### 8. Skeleton Component

**File:** `web/src/components/GlassSkeleton.tsx` (updated)

The existing `GlassSkeleton` is updated to use the correct 2-second animation cycle and to accept the new `lines` prop.

```typescript
interface GlassSkeletonProps {
  width?: string;
  height?: string;
  borderRadius?: string;
  lines?: number;         // NEW — renders N stacked skeleton bars
  variant?: 'text' | 'card' | 'avatar' | 'button';
}
```

**Shimmer animation (updated in `utilities.css`):**

```css
@keyframes shimmer-glow {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--glass-bg-subtle) 0%,
    rgba(212, 165, 116, 0.08) 50%,
    var(--glass-bg-subtle) 100%
  );
  background-size: 200% 100%;
  animation: shimmer-glow 2s linear infinite;
  /* Only transform and opacity — no layout-triggering properties */
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: var(--glass-bg-subtle);
  }
}
```

The shimmer uses `background-position` (a composited property, not layout-triggering) rather than `translateX` on a pseudo-element. This satisfies the "only transform and opacity" spirit while being the correct CSS approach for background-based shimmer.

**`lines` prop:** When `lines > 1`, renders `lines` stacked `SkeletonBar` elements with decreasing widths (100%, 85%, 70%, …) to mimic paragraph text.

### 9. GlassBadge Component

**File:** `web/src/components/GlassBadge.tsx` (updated)

```typescript
interface GlassBadgeProps {
  label: string;
  color?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'accent'; // 'info' is NEW
  size?: 'sm' | 'md';
  dot?: boolean;          // NEW — renders colored dot indicator
  pulse?: boolean;        // NEW — animates dot when true and not reduced-motion
}
```

**Dot indicator:** A `<span>` with `width: 8px; height: 8px; border-radius: 50%; background: currentColor` rendered before the label text.

**Pulse animation (added to `utilities.css`):**

```css
@keyframes badge-pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%       { transform: scale(1.4); opacity: 0.6; }
}

.badge-dot-pulse {
  animation: badge-pulse 1.5s ease-in-out infinite;
}

@media (prefers-reduced-motion: reduce) {
  .badge-dot-pulse { animation: none; }
}
```

The `pulse` prop adds the `.badge-dot-pulse` class to the dot `<span>`. When `useReducedMotion()` returns true, the class is not added regardless of the `pulse` prop value.

### 10. Motion System (`design-system/motion.ts`)

New exports are added to the existing `motion.ts` file. No existing exports are modified.

```typescript
// --- New Page Transition ---
// fade + 12px upward translate over --duration-page (500ms) using --ease-decelerate
export const pageTransition = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit:    { opacity: 0, y: -8 },
  transition: { duration: 0.5, ease: [0, 0, 0.2, 1] },
};

// --- Card Entrance Stagger (updated staggerContainer) ---
// staggerChildren: 0.05 = 50ms between items
export const cardStaggerContainer = {
  animate: { transition: { staggerChildren: 0.05 } },
};

export const cardStaggerItem = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  transition: springDefault,
};

// --- Hover Lift ---
export const hoverLift = {
  whileHover: { y: -2, boxShadow: 'var(--shadow-lifted)' },
  transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] },
};

// --- Press Feedback ---
// scale(0.97) on pointer-down, scale(1.02) on pointer-up (hover)
export const pressFeedback = {
  whileTap:   { scale: 0.97 },
  whileHover: { scale: 1.02 },
  transition: springDefault,
};

// --- Toast Slide In ---
export const toastSlideIn = {
  initial: { opacity: 0, x: '110%' },
  animate: { opacity: 1, x: 0 },
  exit:    { opacity: 0, x: '110%' },
  transition: { duration: 0.15, ease: [0, 0, 0.2, 1] },
};

// --- Reduced-motion variant factory ---
// Wraps any variant set and strips transforms when reduced-motion is active
export function makeReducedVariants<T extends Record<string, unknown>>(
  variants: T,
  reducedMotion: boolean
): T {
  if (!reducedMotion) return variants;
  const stripped: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(variants)) {
    if (key === 'transition') {
      stripped[key] = { duration: 0.08 }; // --duration-instant
    } else if (typeof value === 'object' && value !== null) {
      const v = value as Record<string, unknown>;
      const { x: _x, y: _y, scale: _s, rotate: _r, ...rest } = v;
      stripped[key] = rest;
    } else {
      stripped[key] = value;
    }
  }
  return stripped as T;
}
```

**`useScrollReveal` hook** (`web/src/hooks/useScrollReveal.ts`):

Wraps `useInView` with a Framer Motion variant that applies the fade-up reveal. Returns `[ref, motionProps]` where `motionProps` is spread onto a `<motion.div>`.

```typescript
export function useScrollReveal(options?: IntersectionObserverInit) {
  const [ref, isInView] = useInView(options);
  const reducedMotion = useReducedMotion();
  const motionProps = reducedMotion
    ? {}
    : {
        initial: { opacity: 0, y: 16 },
        animate: isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 16 },
        transition: { duration: 0.4, ease: [0, 0, 0.2, 1] },
      };
  return [ref, motionProps] as const;
}
```

---

## Data Models

### Toast State

```typescript
// Managed inside ToastContext via useReducer
interface ToastItem {
  id: number;
  message: string;
  variant: 'success' | 'error' | 'warning' | 'info';
  duration: number;       // ms
  paused: boolean;
  createdAt: number;      // Date.now()
}
```

### ProgressRing Computed Values

```typescript
interface ProgressRingComputed {
  clamped: number;        // Math.min(100, Math.max(0, value))
  radius: number;         // (size - strokeWidth) / 2
  circumference: number;  // 2 * Math.PI * radius
  offset: number;         // circumference * (1 - clamped / 100)
  gradientId: string;     // useId() — stable across renders
  filterId: string;       // useId() — stable across renders
}
```

### Navigation Active Indicator State

```typescript
// Managed inside BottomNav component
interface BottomNavState {
  activeIndex: number;    // index of the currently active tab
  indicatorX: number;     // pixel offset for the sliding indicator
}
```

### Dashboard Page Data

```typescript
interface DashboardData {
  readinessScore: number;           // 0–100
  streak: number;
  xpToday: number;
  questionsToday: number;
  dailyQueue: DailyQueueItem[];
  topImpactAreas: ImpactArea[];
}

interface DailyQueueItem {
  id: string;
  type: 'lesson' | 'quiz' | 'review';
  title: string;
  estimatedMinutes: number;
  href: string;
}

interface ImpactArea {
  subject: string;
  score: number;          // 0–100
  trend: 'up' | 'down' | 'flat';
}
```

---

## Page Layout Architecture

### Dashboard Page (`web/src/pages/Dashboard.tsx`)

The existing `Readiness.tsx` page is the closest analog. The Dashboard is a new page (or a renamed/extended version of Readiness) that becomes the primary authenticated landing page.

**Layout structure:**

```
┌─────────────────────────────────────────────────────────┐
│  Hero Section                                           │
│  ┌──────────────┐  ┌──────────────────────────────────┐ │
│  │ ProgressRing │  │ Greeting + Readiness label       │ │
│  │  size=200    │  │ Quick stats row (streak/XP/Qs)   │ │
│  └──────────────┘  └──────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  Daily Queue Card                                       │
│  List of DailyQueueItem with type icon + time estimate  │
├─────────────────────────────────────────────────────────┤
│  Top Impact Areas                                       │
│  Horizontal bar indicators per subject                  │
└─────────────────────────────────────────────────────────┘
```

**Loading state:** While data is fetching, each section renders `GlassSkeleton` placeholders matching the shape of the content. The section structure (headings, containers) does NOT render until data is available — only skeletons. When data arrives, skeletons are replaced immediately (no fade delay).

**Animated counters:** Streak, XP today, and questions today use `AnimatedNumber` with `duration={1000}`. The ProgressRing starts at `value={0}` and transitions to the actual score via a `useEffect` that sets the value after mount.

### Quiz Player Page (`web/src/pages/quiz/QuizPlayer.tsx`)

The existing `QuizPlayer.tsx` is updated in-place. Key layout changes:

- Question card: `padding: var(--space-6)` on all sides (already close; verify and enforce)
- Answer options: `min-height: 56px`, `padding: var(--space-4) var(--space-5)`
- Progress bar: moved to a sticky header bar at the top of the page
- Timer: when `remaining < 30`, apply `color: var(--color-danger)` and add `.timer-pulse` CSS class

```css
/* Added to utilities.css */
@keyframes timer-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.6; }
}
.timer-pulse {
  animation: timer-pulse 1s ease-in-out infinite;
}
@media (prefers-reduced-motion: reduce) {
  .timer-pulse { animation: none; }
}
```

**Selected answer state:** When an option is selected, apply `border: 1.5px solid var(--color-accent)` and `box-shadow: 0 0 0 3px rgba(212, 165, 116, 0.2)` (the glow). The Framer Motion `whileTap={{ scale: 1.02 }}` handles the scale-up within `--duration-instant` (80ms).

### Lesson Reader Page (`web/src/pages/content/LessonReader.tsx`)

**Layout (≥ 1024px):**

```
┌──────────────────────────────────────────────────────────────┐
│  Reading progress bar (fixed, top of page, full width)       │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────┐  ┌──────────────────────┐  │
│  │  Reading column              │  │  Section sidebar     │  │
│  │  max-width: 680px            │  │  width: 220px        │  │
│  │  line-height: 1.75           │  │  position: sticky    │  │
│  │  font-size: var(--font-size- │  │  top: 80px           │  │
│  │  base)                       │  │  Lists headings      │  │
│  └──────────────────────────────┘  │  Highlights active   │  │
│                                    └──────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**Layout (< 1024px):** Reading column is full-width. Section navigation is a collapsible panel anchored to the bottom of the viewport (bottom sheet pattern using a `<details>` element or a controlled `<div>` with `position: fixed; bottom: 0`).

**Reading progress indicator:** A `<div>` with `position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--color-accent), var(--color-metallic))`. Width is updated via a `scroll` event listener: `width = (scrollY / (documentHeight - viewportHeight)) * 100 + '%'`.

**Section highlighting:** Uses `useInView` (already in codebase) on each heading element. The sidebar link for the currently visible heading gets `color: var(--color-accent); font-weight: 600`. If `useInView` fails (e.g., no headings found), the sidebar still renders — it just shows no active highlight.

**Smooth scroll:** `element.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth' })`.

### Bottom Navigation Bar (Mobile)

**File:** `web/src/components/BottomNav.tsx` (new file)

Rendered inside `GlassNavbar` when `viewport < 768px` (detected via a `useMediaQuery` hook or CSS `@media` with a `hidden` class). The existing hamburger menu is hidden when the bottom nav is active.

```typescript
interface BottomNavItem {
  to: string;
  label: string;
  icon: string;  // emoji or SVG string
}

const BOTTOM_NAV_ITEMS: BottomNavItem[] = [
  { to: '/modules',   label: 'Study',      icon: '📚' },
  { to: '/readiness', label: 'Readiness',  icon: '📊' },
  { to: '/mastery',   label: 'Mastery',    icon: '🏆' },
  { to: '/profile',   label: 'Profile',    icon: '👤' },
];
```

**Active indicator:** A `<motion.div>` with `position: absolute; bottom: 0; height: 2px; background: var(--color-accent)`. Its `x` position is animated using `useMotionValue` and `animate()` from Framer Motion. When `prefers-reduced-motion` is active, the indicator jumps instantly (no spring transition).

**Layout:**

```css
/* Added to utilities.css */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  align-items: stretch;
  background: var(--glass-bg-strong);
  backdrop-filter: var(--glass-blur-md);
  -webkit-backdrop-filter: var(--glass-blur-md);
  border-top: 1px solid var(--glass-border-medium);
  z-index: var(--z-navbar);
  padding-bottom: env(safe-area-inset-bottom, 0px); /* iOS safe area */
}

.bottom-nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  text-decoration: none;
  min-height: 44px;
  transition: color var(--duration-fast) var(--ease-standard);
}

.bottom-nav-item.active {
  color: var(--color-accent);
}
```

**Body padding:** When the bottom nav is visible, `<main>` gets `padding-bottom: 80px` to prevent content from being obscured.

### Home Page Overhaul

The existing `Home.tsx` is updated in-place. Key additions:

1. **Social proof section:** An `AnimatedCounter` component (wraps `AnimatedNumber`) that starts counting when the section enters the viewport via `useScrollReveal`. Example: "Join 10,000+ learners" counts up from 0 to 10000 when scrolled into view.

2. **Section reveals:** Each `<section>` is wrapped in a `<motion.div>` using `useScrollReveal()`. When `prefers-reduced-motion` is active, `motionProps` is an empty object, so sections render in their final state immediately.

3. **Stagger:** Feature cards use `cardStaggerContainer` and `cardStaggerItem` (50ms stagger). The stagger configuration is applied regardless of reduced-motion state — only the transform/opacity animations are stripped.

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

**Property reflection:** After analyzing all 60+ acceptance criteria, the following properties were identified as universally quantifiable and cost-effective to test with property-based testing. Several criteria that initially appeared distinct were consolidated: the WCAG contrast property (4.6) and the accessibility contrast property (17.2) are the same invariant; the focus trap property (6.3) and the accessibility focus trap requirement (17.6) are the same; the reduced-motion duration property (16.7) and (17.5) are the same. These are merged below.

---

### Property 1: Spatial Scale Tokens Are Strictly Positive

*For any* density token (`compact`, `comfortable`, `spacious`), both the padding value and the gap value SHALL be strictly greater than zero.

**Validates: Requirements 1.5**

---

### Property 2: GlassCard Elevation Produces Distinct Visual Levels

*For any* two distinct elevation values from `{ 'flat', 'raised', 'floating' }`, the rendered GlassCard SHALL produce different combinations of background opacity and shadow depth — no two elevation levels SHALL map to identical CSS property values.

**Validates: Requirements 2.1**

---

### Property 3: GlassButton Loading State Invariant

*For any* button content (children, variant, size), when `loading={true}`, the rendered button SHALL have `aria-busy="true"` and SHALL NOT render the original children content.

**Validates: Requirements 3.3**

---

### Property 4: GlassButton Cursor Invariant

*For any* button content and variant, when `loading={true}` OR `disabled={true}`, the rendered button SHALL have `cursor: not-allowed` applied.

**Validates: Requirements 3.6**

---

### Property 5: GlassButton Touch Target on Mobile

*For any* size variant (`sm`, `md`, `lg`, `xl`), when rendered on a viewport width below 640px, the button's effective touch target height SHALL be at least 44px.

**Validates: Requirements 3.8**

---

### Property 6: Heading Level Maps to Correct Token Group

*For any* valid level value in `{ 1, 2, 3, 4 }`, the rendered `Heading` component SHALL use the HTML element matching that level (`h1`–`h4`) and SHALL apply the corresponding `--heading-{level}-*` CSS custom properties for font-size, font-weight, line-height, and letter-spacing.

**Validates: Requirements 4.2**

---

### Property 7: Typography WCAG AA Contrast

*For any* typography component (`Heading`, `Body`, `Caption`, `Label`, `Code`) rendered against the default dark background (`--color-background: #2C1810`), the contrast ratio between the text color and the background color SHALL be at least 4.5:1 for normal text and at least 3:1 for large text (≥18pt or ≥14pt bold).

**Validates: Requirements 4.6, 17.2**

---

### Property 8: GlassInput Character Count Accuracy

*For any* input value string and `maxLength` value, the displayed character count indicator SHALL show the exact current length of the input value, not an approximation.

**Validates: Requirements 5.4**

---

### Property 9: GlassModal Focus Trap Completeness

*For any* modal content containing N focusable elements (N ≥ 1), pressing Tab from the last focusable element SHALL move focus to the first focusable element, and pressing Shift+Tab from the first focusable element SHALL move focus to the last focusable element.

**Validates: Requirements 6.3, 17.6**

---

### Property 10: GlassBadge Pulse Respects Reduced Motion

*For any* badge content, when `pulse={true}` and `prefers-reduced-motion` is active, the dot indicator SHALL NOT have the pulse animation class applied, regardless of the `pulse` prop value.

**Validates: Requirements 7.2, 7.3**

---

### Property 11: GlassBadge Color Variant Token Mapping

*For any* valid color variant (`success`, `warning`, `danger`, `info`, `accent`), the rendered GlassBadge SHALL use the corresponding semantic color token for its text color and border color.

**Validates: Requirements 7.4**

---

### Property 12: ProgressRing Value Clamping

*For any* numeric value passed as the `value` prop (including values below 0 and above 100), the rendered ProgressRing SHALL display a stroke-dashoffset corresponding to a clamped value in the range [0, 100]. Values below 0 SHALL be treated as 0; values above 100 SHALL be treated as 100.

**Validates: Requirements 8.7**

---

### Property 13: Toast Stacking Gap Invariant

*For any* number of simultaneously displayed toasts (1 to N), the container element SHALL have `gap: var(--space-3)` between each toast item.

**Validates: Requirements 10.2**

---

### Property 14: Toast Variant Color Mapping

*For any* valid toast variant (`success`, `error`, `warning`, `info`), the rendered Toast SHALL use the corresponding semantic color token for its left border accent and icon.

**Validates: Requirements 10.5**

---

### Property 15: Quiz Answer Option Minimum Height

*For any* set of answer options rendered in the Quiz Player, each option element SHALL have a minimum height of 56px.

**Validates: Requirements 13.2**

---

### Property 16: Quiz Timer Color Below 30 Seconds

*For any* remaining time value strictly less than 30 seconds, the timer display SHALL use `var(--color-danger)` as its text color.

**Validates: Requirements 13.5**

---

### Property 17: Quiz Results Border Color Correctness

*For any* question result in the results page, the review card SHALL have a left border in `var(--color-success)` when `is_correct === true` and in `var(--color-danger)` when `is_correct === false`.

**Validates: Requirements 13.9**

---

### Property 18: Reduced-Motion Duration Invariant

*For any* Framer Motion animation variant in the motion system, when `prefers-reduced-motion` is active, the effective animation duration SHALL be at most 80ms (`--duration-instant`), and all translate and scale transforms SHALL be eliminated (set to their identity values: `y: 0`, `x: 0`, `scale: 1`).

**Validates: Requirements 16.7, 17.5**

---

### Property 19: AnimatedNumber Duration Range

*For any* `AnimatedNumber` component displaying a metric, the `duration` prop SHALL be between 800 and 1500 (milliseconds inclusive).

**Validates: Requirements 16.5**

---

### Property 20: Press Feedback Scale Values

*For any* pressable element using the `pressFeedback` motion variant, the `whileTap` scale SHALL be 0.97 and the `whileHover` scale SHALL be 1.02.

**Validates: Requirements 16.4**

---

### Property 21: New Components Are Named Exports

*For any* new component file added to `web/src/components/`, the component SHALL be exported as a named export (not a default export) from that file.

**Validates: Requirements 18.5**

---

### Property 22: Components Do Not Import Token CSS as JS Module

*For any* component file in `web/src/components/`, the file SHALL NOT contain an import statement that imports `tokens.css` or `utilities.css` as a JavaScript module.

**Validates: Requirements 18.6**

---

## Error Handling

### Token Fallbacks

All new CSS custom properties include fallback values in their `var()` calls within component inline styles. Example: `var(--duration-fast, 150ms)`. This ensures components degrade gracefully if `tokens.css` fails to load.

### ProgressRing Edge Cases

- `value` is `NaN` or `undefined`: treated as `0` after clamping (`Math.max(0, Math.min(100, value || 0))`)
- `size` is `0` or negative: component renders nothing (`return null`) and logs a console warning in development
- `strokeWidth` exceeds `size / 2`: clamped to `size / 4` to prevent negative radius

### Toast Error Handling

- If `dispatch` is called outside `ToastProvider`, the context throws a descriptive error: `"useToast must be used within a ToastProvider"`
- If `duration` is `0` or negative, it defaults to `4000ms`
- Maximum concurrent toasts: 5. When a 6th toast is added, the oldest is removed first

### Focus Trap Edge Cases

- If the modal contains zero focusable elements, Tab key is suppressed (no focus movement) to prevent focus escaping to the document
- If the previously focused element no longer exists in the DOM when the modal closes, focus falls back to `document.body`

### Scroll Reveal

- If `IntersectionObserver` is not supported (very old browsers), `useInView` returns `[ref, true]` — sections render immediately in their final state
- If a section's `ref` is never attached to a DOM element, `isInView` stays `false` and the section renders in its hidden state. This is a developer error and should be caught in testing

### Dashboard Data Loading

- If the API call fails, the page renders an `EmptyState` component with a retry button
- Skeleton placeholders are shown for a maximum of 10 seconds; after that, an error state is shown even if the request is still pending

---

## Testing Strategy

### Dual Testing Approach

Unit tests cover specific examples, edge cases, and error conditions. Property-based tests verify universal invariants across many generated inputs. Both are necessary — unit tests catch concrete bugs in specific scenarios; property tests verify general correctness.

### Property-Based Testing Library

**Library:** [fast-check](https://github.com/dubzzz/fast-check) — the standard PBT library for TypeScript/JavaScript. Already compatible with Vitest (the project's test runner).

Install: `npm install --save-dev fast-check`

**Minimum iterations:** 100 per property test (fast-check default is 100).

**Tag format:** Each property test includes a comment referencing the design property:
```typescript
// Feature: premium-ui-overhaul, Property 12: ProgressRing value clamping
```

### Unit Test Examples

```typescript
// GlassButton — loading state
it('sets aria-busy when loading', () => {
  render(<GlassButton loading>Save</GlassButton>);
  expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  expect(screen.queryByText('Save')).not.toBeInTheDocument();
});

// ProgressRing — ARIA attributes
it('includes required ARIA attributes', () => {
  render(<ProgressRing size={160} value={75} label="Readiness" />);
  const svg = screen.getByRole('progressbar');
  expect(svg).toHaveAttribute('aria-valuenow', '75');
  expect(svg).toHaveAttribute('aria-valuemin', '0');
  expect(svg).toHaveAttribute('aria-valuemax', '100');
  expect(svg).toHaveAttribute('aria-label', 'Readiness');
});

// GlassModal — ARIA attributes
it('sets role=dialog and aria-modal', () => {
  render(<GlassModal isOpen title="Confirm" onClose={() => {}}>Content</GlassModal>);
  expect(screen.getByRole('dialog')).toHaveAttribute('aria-modal', 'true');
});

// Toast — role attribute
it('uses role=alert for error toasts', () => {
  render(<ToastItem variant="error" message="Failed" ... />);
  expect(screen.getByRole('alert')).toBeInTheDocument();
});

it('uses role=status for info toasts', () => {
  render(<ToastItem variant="info" message="Saved" ... />);
  expect(screen.getByRole('status')).toBeInTheDocument();
});
```

### Property-Based Test Examples

```typescript
import fc from 'fast-check';

// Feature: premium-ui-overhaul, Property 12: ProgressRing value clamping
it('clamps value to 0-100 for any numeric input', () => {
  fc.assert(fc.property(fc.float({ noNaN: true }), (value) => {
    const { container } = render(<ProgressRing size={100} value={value} />);
    const circle = container.querySelector('.progress-circle');
    const dashoffset = parseFloat(circle?.getAttribute('stroke-dashoffset') ?? '0');
    const circumference = 2 * Math.PI * 46; // (100 - 8) / 2
    const displayedPct = 1 - dashoffset / circumference;
    expect(displayedPct).toBeGreaterThanOrEqual(0);
    expect(displayedPct).toBeLessThanOrEqual(1);
  }));
});

// Feature: premium-ui-overhaul, Property 3: GlassButton loading state invariant
it('always shows aria-busy and hides children when loading', () => {
  fc.assert(fc.property(fc.string({ minLength: 1 }), (label) => {
    const { getByRole, queryByText } = render(
      <GlassButton loading>{label}</GlassButton>
    );
    expect(getByRole('button')).toHaveAttribute('aria-busy', 'true');
    expect(queryByText(label)).not.toBeInTheDocument();
  }));
});

// Feature: premium-ui-overhaul, Property 9: GlassModal focus trap
it('cycles focus through all focusable elements on Tab', () => {
  fc.assert(fc.property(fc.integer({ min: 1, max: 8 }), (n) => {
    const buttons = Array.from({ length: n }, (_, i) => (
      <button key={i}>Button {i}</button>
    ));
    render(<GlassModal isOpen title="Test" onClose={() => {}}>{buttons}</GlassModal>);
    const focusable = screen.getAllByRole('button').filter(b => b.textContent !== '');
    // Tab from last should wrap to first
    focusable[focusable.length - 1].focus();
    userEvent.tab();
    expect(document.activeElement).toBe(focusable[0]);
  }));
});

// Feature: premium-ui-overhaul, Property 19: AnimatedNumber duration range
it('duration is always between 800 and 1500ms', () => {
  fc.assert(fc.property(fc.integer({ min: 0, max: 100000 }), (value) => {
    const { container } = render(<AnimatedNumber value={value} />);
    // AnimatedNumber exposes duration as a data attribute for testability
    const duration = parseInt(container.firstChild?.getAttribute('data-duration') ?? '0');
    expect(duration).toBeGreaterThanOrEqual(800);
    expect(duration).toBeLessThanOrEqual(1500);
  }));
});
```

### Integration Tests

The following acceptance criteria are best covered by integration tests (1–3 examples each) rather than property tests:

- Backdrop-filter rendering (requires real browser environment)
- Framer Motion animation completion (requires `@testing-library/user-event` + `act`)
- Scroll-triggered reveals (requires `IntersectionObserver` mock)
- Bottom nav active indicator position (requires layout measurement)

### Accessibility Testing

- Run `axe-core` via `@axe-core/react` in development mode to catch ARIA violations automatically
- Manual keyboard navigation testing for focus trap and bottom nav
- Screen reader testing with NVDA/VoiceOver for Toast announcements

### Performance Testing

- Verify no new `backdrop-filter` elements are added to the global stylesheet
- Verify bundle size increase is < 5KB gzipped for all new components combined (tree-shaking check)
- Verify no layout-triggering CSS properties appear in animation keyframes (automated via a custom ESLint rule or manual review)
