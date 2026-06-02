# Requirements Document

## Introduction

CSNexus is a Philippine Civil Service Exam preparation platform. The premium UI overhaul transforms the existing functional interface into a premium, "expensive-looking" experience inspired by Apple/Framer aesthetics — spatial layouts, generous whitespace, depth through blur and shadow, and rich micro-interactions — while remaining grounded in cognitive science research on how UI design affects learning outcomes.

The overhaul **extends** the existing design system (`tokens.css`, `utilities.css`, existing component library) rather than replacing it. All new tokens, components, and page layouts build on the **Obsidian + Gold palette**, glass utilities, and Framer Motion already in place.

The research basis for this overhaul:
- **Cognitive Load Theory (Sweller, 1988)**: Clean visual hierarchy reduces extraneous cognitive load and improves retention.
- **Aesthetic-Usability Effect (NNG)**: Aesthetically pleasing interfaces are perceived as more usable and trustworthy, increasing willingness to pay.
- **Typography and Readability**: Line length 50–75 characters, 1.5–1.7 line height, and WCAG AA contrast (4.5:1) measurably improve reading comprehension.
- **Feedback and Micro-interactions**: Visual feedback under 100ms reduces user anxiety; transitions of 200–400ms feel premium.
- **Spatial Design**: Generous whitespace signals quality and reduces cognitive load.
- **Color and Emotion**: Warm, dark interfaces reduce eye strain during extended study sessions.

---

## Glossary

- **Design_System**: The collection of CSS custom properties in `tokens.css` and utility classes in `utilities.css` that define the visual language of CSNexus.
- **Token**: A CSS custom property (e.g., `--color-accent`) that encodes a single design decision.
- **Component**: A reusable React component in `web/src/components/` that renders UI using Design_System tokens.
- **Page**: A React component in `web/src/pages/` that composes Components into a full screen.
- **Motion_System**: The set of animation tokens, easing curves, and Framer Motion configurations that govern all transitions and micro-interactions.
- **Glass_Surface**: A UI element using backdrop-filter blur, semi-transparent background, and border to create a frosted-glass appearance.
- **Elevation**: A visual layering concept expressed through shadow depth, blur intensity, and background opacity — surface-0 (base) through surface-4 (floating).
- **Spatial_Scale**: A named density setting (compact, comfortable, spacious) that adjusts padding and gap values across layouts.
- **Skeleton**: A placeholder UI element that mimics the shape of loading content using a shimmer animation.
- **Toast**: A transient notification that appears, persists briefly, and auto-dismisses.
- **ProgressRing**: An SVG-based circular progress indicator with gradient stroke.
- **Readiness_Score**: The hero metric on the authenticated dashboard representing a learner's overall exam readiness as a percentage.
- **WCAG_AA**: Web Content Accessibility Guidelines Level AA — minimum 4.5:1 contrast ratio for normal text, 3:1 for large text (≥18pt or ≥14pt bold).
- **Reduced_Motion**: The `prefers-reduced-motion: reduce` CSS media query that signals the user has requested minimal animation.
- **Touch_Target**: The interactive area of a UI element; minimum 44×44px on mobile per WCAG 2.5.5.
- **Tree_Shakeable**: A module that allows bundlers to eliminate unused exports, keeping bundle size minimal.

---

## Requirements

### Requirement 1: Design Token Enhancements

**User Story:** As a frontend developer, I want a complete, extended set of design tokens, so that I can build consistent UI without inventing ad-hoc values.

#### Acceptance Criteria

1. THE Design_System SHALL define explicit heading style tokens for h1 through h4 using the General Sans display font, including font-size, font-weight, line-height, and letter-spacing values drawn from the existing fluid type scale.
2. THE Design_System SHALL define surface elevation tokens `--surface-0` through `--surface-4` as CSS custom properties, where each level increases background opacity and shadow depth relative to the previous level.
3. THE Design_System SHALL define motion duration tokens: `--duration-instant: 80ms`, `--duration-fast: 150ms`, `--duration-normal: 250ms`, `--duration-slow: 400ms`, and `--duration-page: 500ms`.
4. THE Design_System SHALL define motion easing tokens: `--ease-standard` (cubic-bezier(0.4, 0, 0.2, 1)), `--ease-decelerate` (cubic-bezier(0, 0, 0.2, 1)), `--ease-accelerate` (cubic-bezier(0.4, 0, 1, 1)), and `--ease-spring` (cubic-bezier(0.34, 1.56, 0.64, 1)).
5. THE Design_System SHALL define spatial scale tokens: `--density-compact`, `--density-comfortable`, and `--density-spacious`, each mapping to a specific padding and gap value pair where both padding and gap values are strictly positive (greater than zero).
6. THE Design_System SHALL define semantic interactive state tokens for hover, active, focus, and disabled states using the Obsidian + Gold palette.
7. WHEN the Design_System tokens are updated, THE Design_System SHALL ensure all existing Components continue to render correctly, even if underlying CSS custom property names change, so that no existing component breaks due to token restructuring.

---

### Requirement 2: GlassCard Component Overhaul

**User Story:** As a learner, I want cards to feel tactile and layered, so that the interface communicates depth and quality during study sessions.

#### Acceptance Criteria

1. THE GlassCard SHALL support an `elevation` prop with values `flat`, `raised`, and `floating`, each mapping to a distinct combination of shadow depth, blur intensity, and background opacity from the surface elevation tokens.
2. WHEN a user hovers over a GlassCard with elevation `raised` or `floating`, THE GlassCard SHALL animate `translateY(-2px)` and increase shadow depth within 150ms using `--ease-standard`.
3. WHEN a user hovers over a GlassCard with the `premium` variant, THE GlassCard SHALL display an inner radial glow using the gold accent color at reduced opacity, regardless of the card's current elevation level (`flat`, `raised`, or `floating`).
4. WHEN the GlassCard entrance animation plays, THE GlassCard SHALL fade in and translate upward by 8px over `--duration-normal` (250ms).
5. WHILE `prefers-reduced-motion` is active, THE GlassCard SHALL skip all transform and opacity animations and render in its final state immediately.
6. THE GlassCard SHALL be Tree_Shakeable and introduce no new runtime dependencies beyond what is already installed.

---

### Requirement 3: GlassButton Component Overhaul

**User Story:** As a learner, I want buttons to respond immediately and expressively to my interactions, so that I feel confident my actions are registered.

#### Acceptance Criteria

1. THE GlassButton SHALL support size variants `sm`, `md`, `lg`, and `xl` with distinct padding, font-size, and minimum height values drawn from Design_System tokens.
2. THE GlassButton SHALL support icon placement via `iconLeft` and `iconRight` props that render an icon element adjacent to the label with consistent spacing.
3. THE GlassButton SHALL support a `loading` prop that, WHEN set to true, replaces the label with an animated spinner and sets `aria-busy="true"` on the button element.
4. WHEN a user clicks a GlassButton, THE GlassButton SHALL display a ripple effect that originates at the click coordinates and expands outward within `--duration-fast` (150ms).
5. WHEN a user presses a GlassButton, THE GlassButton SHALL scale to 0.97 on press and 1.02 on release using a spring easing curve.
6. WHEN the GlassButton `loading` prop is true OR the GlassButton is explicitly disabled or non-interactive, THE GlassButton SHALL display `cursor: not-allowed`.
7. WHILE `prefers-reduced-motion` is active, THE GlassButton SHALL skip scale and ripple animations and rely on background color change alone for press feedback; hover transitions and focus indicators SHALL continue to function normally.
8. THE GlassButton SHALL maintain a minimum Touch_Target of 44×44px on all size variants when rendered on a viewport width below 640px.
9. THE GlassButton SHALL expose all existing variant styles (`primary`, `secondary`, `ghost`, `danger`) unchanged so that no existing usage breaks.

---

### Requirement 4: Typography Component System

**User Story:** As a learner, I want consistent, readable text across all pages, so that I can study for extended periods without eye strain.

#### Acceptance Criteria

1. THE Design_System SHALL provide `Heading`, `Body`, `Caption`, `Label`, and `Code` React components that apply the correct font-family, font-size, line-height, and letter-spacing from Design_System tokens.
2. THE Heading component SHALL accept a `level` prop (1–4) that maps to the h1–h4 heading style tokens defined in Requirement 1.
3. THE Body component SHALL render with a line-height of 1.6–1.7 and a maximum line length of 75 characters (approximately 680px at base font size) to comply with readability research.
4. THE Caption component SHALL render at `--font-size-sm` with `--color-text-secondary` and a line-height of 1.5.
5. THE Code component SHALL render with a monospace font stack, a subtle glass background, and horizontal padding of `--space-2`.
6. WHEN any typography component is rendered, THE component SHALL meet WCAG_AA contrast requirements (minimum 4.5:1 for normal text, 3:1 for large text) against the default dark background.

---

### Requirement 5: GlassInput Component Overhaul

**User Story:** As a learner, I want form inputs to feel polished and provide clear feedback, so that I can complete forms confidently without confusion.

#### Acceptance Criteria

1. THE GlassInput SHALL implement a floating label animation where the label transitions from placeholder position to a smaller label above the input field WHEN the input receives focus or contains a value, completing within `--duration-fast` (150ms).
2. THE GlassInput SHALL support validation state props `error`, `success`, and `warning`, each applying a distinct border color and icon from the semantic color tokens.
3. WHEN the GlassInput `error` state is active, THE GlassInput SHALL display an error message string below the input field in `--color-danger` at `--font-size-sm`.
4. WHERE a `maxLength` prop is provided, THE GlassInput SHALL display a character count indicator showing current length versus maximum length.
5. WHEN a user focuses the GlassInput, THE GlassInput SHALL display a focus ring of 3px width in the gold accent color (`rgba(201, 168, 76, 0.4)`) to meet WCAG 2.4.11 focus appearance requirements.
6. THE GlassInput SHALL enforce a default height of 48px on mobile viewports, with 44px as the absolute minimum Touch_Target height.

---

### Requirement 6: GlassModal Component

**User Story:** As a learner, I want modals to feel intentional and focused, so that I am not distracted from the task at hand.

#### Acceptance Criteria

1. THE GlassModal SHALL render a backdrop with `backdrop-filter: blur(12px)` and a semi-transparent dark overlay when open.
2. WHEN the GlassModal opens, THE GlassModal SHALL animate its panel with a spring entrance (scale from 0.95 to 1.0, opacity from 0 to 1) over `--duration-normal` (250ms) using `--ease-spring`.
3. WHEN the GlassModal is open, THE GlassModal SHALL trap keyboard focus within the modal panel so that Tab and Shift+Tab cycle only through focusable elements inside the modal.
4. WHEN the user presses Escape, clicks the backdrop, or activates a close button, THE GlassModal SHALL close, wait for any exit animations to complete, and then return focus to the element that triggered the modal.
5. WHILE `prefers-reduced-motion` is active, THE GlassModal SHALL open and close without scale or translate animations, using opacity transition only at `--duration-fast` (150ms); spring easing SHALL be preserved for any non-transform properties, and only scale and translate animations SHALL be disabled.
6. THE GlassModal SHALL set `aria-modal="true"` and `role="dialog"` on the panel element, and include an `aria-labelledby` reference to the modal title.

---

### Requirement 7: GlassBadge Component

**User Story:** As a learner, I want status badges to communicate live and static states clearly, so that I can quickly understand my progress at a glance.

#### Acceptance Criteria

1. THE GlassBadge SHALL support a `dot` variant that renders a small colored circle indicator alongside the label text.
2. THE GlassBadge SHALL support a `pulse` prop that, WHEN set to true AND `prefers-reduced-motion` is not active, applies a repeating scale-and-opacity animation to the dot indicator to signal a live or active state.
3. WHILE `prefers-reduced-motion` is active, THE GlassBadge SHALL render the dot indicator in a static state without the pulse animation, regardless of the value of the `pulse` prop.
4. THE GlassBadge SHALL support `color` variants mapped to the semantic color tokens: `success`, `warning`, `danger`, `info`, and `accent`.

---

### Requirement 8: ProgressRing Component

**User Story:** As a learner, I want to see my readiness score as a prominent circular indicator, so that I can immediately understand my exam preparedness when I open the dashboard.

#### Acceptance Criteria

1. THE ProgressRing SHALL render as an SVG-based circular progress indicator with a gradient stroke using the gold gradient (`--color-accent` to `--color-metallic`).
2. WHEN the ProgressRing mounts, THE ProgressRing SHALL animate the stroke from 0% to the target value over `--duration-slow` (400ms) using `--ease-decelerate`.
3. THE ProgressRing SHALL accept `size` (number, in pixels), `value` (0–100), `strokeWidth` (number), and `label` (string) props.
4. WHEN the ProgressRing value is above 0, THE ProgressRing SHALL display a subtle glow effect on the stroke using a drop-shadow filter in the accent color.
5. WHILE `prefers-reduced-motion` is active, THE ProgressRing SHALL render at its final value immediately without the stroke animation.
6. THE ProgressRing SHALL include an `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, and `aria-label` on the SVG root element for screen reader accessibility.
7. WHEN the ProgressRing `value` prop is provided, THE ProgressRing SHALL clamp the value to the range 0–100 before applying any animation or reduced-motion behavior; values below 0 SHALL be treated as 0 and values above 100 SHALL be treated as 100.

---

### Requirement 9: Skeleton Component

**User Story:** As a learner, I want loading states to feel intentional rather than broken, so that I remain confident the app is working while content loads.

#### Acceptance Criteria

1. THE Skeleton component SHALL render a placeholder block with a shimmer animation that moves a warm-tinted highlight (using `--color-accent` at low opacity) from left to right over an exactly 2-second cycle with no tolerance for variation.
2. THE Skeleton component SHALL accept `width`, `height`, `borderRadius`, and `lines` props to match the shape of the content it replaces.
3. WHILE `prefers-reduced-motion` is active, THE Skeleton SHALL render as a static muted block without the shimmer animation.
4. THE Skeleton component SHALL use only CSS `transform` and `opacity` for the shimmer animation to avoid layout-triggering properties.

---

### Requirement 10: Toast/Notification Component

**User Story:** As a learner, I want brief, non-intrusive notifications, so that I receive feedback on my actions without losing my place in the study flow.

#### Acceptance Criteria

1. THE Toast component SHALL slide in from the top-right corner of the viewport over `--duration-fast` (150ms) using `--ease-decelerate`.
2. THE Toast component SHALL support stacking of multiple simultaneous toasts with a vertical gap of `--space-3` between each.
3. WHEN a Toast is displayed, THE Toast SHALL auto-dismiss after a configurable duration (default 4000ms) and display a progress bar that depletes over the same duration.
4. WHEN a user hovers over a Toast, THE Toast SHALL pause the auto-dismiss timer and the progress bar animation.
5. THE Toast component SHALL support `success`, `error`, `warning`, and `info` variants using the semantic color tokens for the left border accent and icon.
6. WHILE `prefers-reduced-motion` is active, THE Toast SHALL appear and disappear using opacity transition only, without the slide animation; the progress bar animation SHALL remain active regardless of reduced-motion preference.
7. THE Toast SHALL include `role="status"` for informational toasts and `role="alert"` for error toasts to ensure screen reader announcement.

---

### Requirement 11: Home/Landing Page Overhaul

**User Story:** As a prospective learner, I want the landing page to immediately communicate quality and trustworthiness, so that I feel confident investing time in CSNexus.

#### Acceptance Criteria

1. THE Home_Page SHALL render a hero section with display typography at `--font-size-5xl` or larger, using the animated gradient text effect on the primary headline.
2. THE Home_Page SHALL render feature cards in a responsive grid that, WHEN a user hovers over a card, applies the GlassCard elevation lift animation (translateY(-2px) + shadow increase).
3. THE Home_Page SHALL render a social proof section with at least one animated counter that counts up from 0 to its target value WHEN the section enters the viewport, not before.
4. WHEN a user scrolls the Home_Page, THE Home_Page SHALL reveal sections with a fade-up animation (opacity 0→1, translateY 16px→0) as each section enters the viewport.
5. WHEN section reveal animations play, THE Home_Page SHALL stagger child elements with a 50ms delay between each item, regardless of whether animations are active or reduced-motion mode is in effect.
6. WHILE `prefers-reduced-motion` is active, THE Home_Page SHALL render all sections in their final visible state without scroll-triggered reveal animations; hover animations such as card lift and gradient text effects SHALL remain active.

---

### Requirement 12: Dashboard Page Overhaul

**User Story:** As an authenticated learner, I want my dashboard to immediately show my readiness and daily priorities, so that I can start studying without navigating through menus.

#### Acceptance Criteria

1. THE Dashboard_Page SHALL render the Readiness_Score as the primary hero element using the ProgressRing component at a minimum size of 160px diameter.
2. WHEN the Dashboard_Page mounts, THE Dashboard_Page SHALL animate the Readiness_Score ProgressRing from 0 to the learner's current score.
3. THE Dashboard_Page SHALL render a daily queue card showing the next recommended study items with item type icons and estimated completion time.
4. THE Dashboard_Page SHALL render a quick stats row displaying current streak, XP earned today, and total questions answered today, each as an animated counter that counts up on mount.
5. THE Dashboard_Page SHALL render a top impact areas section with horizontal bar indicators showing relative performance per subject area.
6. WHEN the Dashboard_Page content loads, THE Dashboard_Page SHALL display Skeleton placeholders in the shape of each content section until data is available; section UI structure SHALL NOT render until data is fully loaded, and Skeleton placeholders SHALL disappear immediately (with no fade delay) when content becomes available.

---

### Requirement 13: Quiz Player Page Overhaul

**User Story:** As a learner taking a quiz, I want the interface to feel focused and responsive, so that I can concentrate on answering questions rather than fighting the UI.

#### Acceptance Criteria

1. THE Quiz_Player SHALL render the question card with a minimum padding of `--space-6` (24px) on all sides and a clear typographic hierarchy distinguishing question stem from answer options.
2. THE Quiz_Player SHALL render answer options as large tap targets with a minimum height of 56px and a minimum Touch_Target of 44×44px on mobile.
3. WHEN a learner selects an answer option, THE Quiz_Player SHALL animate the selected option with a scale-up (1.0→1.02) and border glow effect within `--duration-instant` (80ms).
4. THE Quiz_Player SHALL render a progress bar at the top of the page that fills smoothly as the learner advances through questions, using a CSS transition of `--duration-normal` (250ms).
5. WHEN the quiz timer drops below 30 seconds, THE Quiz_Player SHALL change the timer color to `--color-danger` and apply a subtle pulse animation to the timer display.
6. WHEN the quiz timer reaches exactly 0 seconds, THE Quiz_Player SHALL switch to a "time expired" state with distinct styling that is visually separate from the sub-30-second warning state.
7. WHILE `prefers-reduced-motion` is active, THE Quiz_Player SHALL skip the selection scale animation and timer pulse, relying on color change alone for state feedback; the border glow effect on answer selection SHALL remain active.
7. THE Quiz_Player results page SHALL animate the final score using an AnimatedNumber count-up over 1200ms on mount.
8. THE Quiz_Player results page SHALL display each question review card with a left border in `--color-success` for correct answers and `--color-danger` for incorrect answers.

---

### Requirement 14: Lesson Reader Page Overhaul

**User Story:** As a learner reading a lesson, I want a comfortable, distraction-free reading experience, so that I can absorb content effectively during extended study sessions.

#### Acceptance Criteria

1. THE Lesson_Reader SHALL constrain the reading content to a maximum width of 680px and center it within the viewport to maintain a line length of 50–75 characters.
2. THE Lesson_Reader SHALL render body text with a line-height of 1.75 and `--font-size-base` to comply with readability research standards.
3. THE Lesson_Reader SHALL render a reading progress indicator at the top of the page that fills as the learner scrolls through the lesson content.
4. WHEN the viewport width is 1024px or wider, THE Lesson_Reader SHALL render a section navigation sidebar that lists lesson headings and highlights the currently visible section; the sidebar SHALL remain visible even if section highlighting fails due to a technical issue.
5. WHEN the viewport width is below 1024px, THE Lesson_Reader SHALL render section navigation as a bottom sheet or collapsible panel rather than a sidebar.
6. WHEN a learner navigates between lesson sections, THE Lesson_Reader SHALL apply a smooth scroll transition unless `prefers-reduced-motion` is active.

---

### Requirement 15: Navigation Overhaul

**User Story:** As a learner, I want navigation to feel fluid and spatially coherent, so that I always know where I am and can move between sections without friction.

#### Acceptance Criteria

1. WHEN the viewport width is below 768px, THE Navigation SHALL render a bottom navigation bar with icons and labels for primary destinations.
2. WHEN a learner navigates to a new primary destination on mobile, THE Navigation bottom bar SHALL animate an active state indicator that slides between tab positions over `--duration-fast` (150ms).
3. WHEN the viewport width is 768px or wider, THE Navigation SHALL render a side navigation panel with hover states and an active indicator.
4. THE Navigation SHALL render breadcrumbs on all pages, including top-level pages.
5. WHEN a learner hovers over a navigation item, THE Navigation SHALL apply a background highlight transition within `--duration-fast` (150ms).
6. WHILE `prefers-reduced-motion` is active, THE Navigation active indicator SHALL move instantly to the new position without the slide animation.

---

### Requirement 16: Motion Design System

**User Story:** As a learner, I want all transitions and animations to feel consistent and intentional, so that the interface communicates quality rather than randomness.

#### Acceptance Criteria

1. THE Motion_System SHALL define page transition animations as a fade combined with a 12px upward translate over `--duration-page` (500ms) using `--ease-decelerate`.
2. THE Motion_System SHALL define card entrance animations as a stagger where each child element fades in and translates upward with a 50ms delay between items; both the fade (opacity) and translate (vertical position) effects SHALL be implemented.
3. THE Motion_System SHALL define hover lift as `translateY(-2px)` combined with an increased shadow, completing within `--duration-fast` (150ms) using `--ease-standard`.
4. THE Motion_System SHALL define press feedback as `scale(0.97)` on pointer-down and `scale(1.02)` on pointer-up, using `--ease-spring` for the release; this press feedback SHALL be active for any pointer-down/up event with no dependency on system state.
5. WHEN any animated number metric is displayed, THE Motion_System SHALL animate the value from 0 to its target using a count-up easing over a duration between 800ms and 1500ms.
6. THE Motion_System SHALL use only CSS `transform` and `opacity` properties for all animations to avoid triggering layout recalculation.
7. WHILE `prefers-reduced-motion` is active, THE Motion_System SHALL reduce all animation durations to `--duration-instant` (80ms) or less and eliminate translate/scale transforms, preserving only opacity transitions for state changes.

---

### Requirement 17: Accessibility Requirements

**User Story:** As a learner with accessibility needs, I want the premium UI to remain fully usable with assistive technologies, so that the visual overhaul does not exclude me.

#### Acceptance Criteria

1. THE Design_System SHALL ensure all interactive elements display a visible focus ring of 3px width in the gold accent color (`rgba(201, 168, 76, 0.4)`) when focused via keyboard.
2. THE Design_System SHALL ensure all text elements meet WCAG_AA contrast requirements: minimum 4.5:1 for normal text and 3:1 for large text (≥18pt or ≥14pt bold) against their background.
3. WHEN an icon-only button is rendered (no visible text label), THE component SHALL include an `aria-label` attribute with a descriptive text string; icon buttons that also display a visible text label MAY omit the `aria-label` attribute.
4. THE Design_System SHALL ensure all interactive elements on all viewport sizes have a minimum Touch_Target area of 44×44px.
5. WHILE `prefers-reduced-motion` is active, THE Motion_System SHALL apply the reduced-motion behavior defined in Requirement 16, Criterion 7 across all components and pages.
6. THE GlassModal SHALL implement focus trapping as defined in Requirement 6, Criterion 3.
7. THE Toast component SHALL use `role="alert"` for error toasts and `role="status"` for informational toasts as defined in Requirement 10, Criterion 7.

---

### Requirement 18: Performance Requirements

**User Story:** As a learner on a mid-range device, I want the premium UI to remain fast and smooth, so that visual richness does not come at the cost of usability.

#### Acceptance Criteria

1. THE Design_System SHALL not introduce any new CSS framework dependencies (no Tailwind, no Bootstrap, no new utility libraries).
2. THE Motion_System SHALL use only CSS `transform` and `opacity` properties for animations, avoiding any property that triggers layout recalculation (e.g., `width`, `height`, `top`, `left`, `margin`).
3. THE Design_System SHALL apply `backdrop-filter` only to elements that explicitly require it, not as a global or inherited style.
4. THE Design_System SHALL continue using Framer Motion (already installed) for complex JavaScript-driven animations and SHALL NOT introduce an additional animation library.
5. THE Component_Library SHALL export all new components as named exports from their individual module files so that bundlers can tree-shake unused components.
6. WHEN a new component is added to the Component_Library, THE component SHALL not import the entire design system token file as a JavaScript module — tokens SHALL be consumed via CSS custom properties only.
