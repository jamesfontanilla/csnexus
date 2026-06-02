/**
 * init-preferences.ts — Synchronous pre-paint accessibility application.
 *
 * This module runs BEFORE React hydrates. It reads the accessibility
 * preferences from localStorage and applies `data-font-size` and
 * `data-reduced-motion` attributes to `<html>` to prevent FOUC.
 *
 * Must be imported at the very top of main.tsx (before React imports).
 */

const ACCESSIBILITY_KEY = "csnexus-settings-accessibility";

try {
  const raw = localStorage.getItem(ACCESSIBILITY_KEY);
  if (raw) {
    const prefs = JSON.parse(raw) as { fontSize?: string; reducedMotion?: string };
    const root = document.documentElement;

    if (prefs.fontSize && ["compact", "default", "large"].includes(prefs.fontSize)) {
      root.setAttribute("data-font-size", prefs.fontSize);
    }

    if (prefs.reducedMotion && ["system", "on", "off"].includes(prefs.reducedMotion)) {
      root.setAttribute("data-reduced-motion", prefs.reducedMotion);
    }
  }
} catch {
  // Silent fallback — localStorage unavailable or JSON malformed
}
