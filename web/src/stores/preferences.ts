/**
 * Preferences Store — typed localStorage wrapper for client-side settings.
 *
 * Storage keys:
 *   - "csnexus-settings-study" → JSON of StudyPreferences
 *   - "csnexus-settings-accessibility" → JSON of AccessibilityPreferences
 *
 * Handles:
 *   - Typed getters with fallback defaults
 *   - Typed setters that persist immediately
 *   - Backward-compatibility migration from legacy "csnexus-feedback-enabled" key
 *   - Graceful fallback to in-memory defaults when localStorage is unavailable
 *   - DOM attribute application for accessibility preferences
 */

// --- Interfaces ---

export interface StudyPreferences {
  dailyGoalMinutes: number; // 5–180, step 5, default 30
  defaultQuizMode: "practice" | "exam" | "power"; // default 'practice'
  examDate: string | null; // ISO date string or null
}

export interface AccessibilityPreferences {
  reducedMotion: "system" | "on" | "off"; // default 'system'
  fontSize: "compact" | "default" | "large"; // default 'default'
  soundEnabled: boolean; // default true
  hapticEnabled: boolean; // default true
}

// --- Constants ---

const STUDY_KEY = "csnexus-settings-study";
const ACCESSIBILITY_KEY = "csnexus-settings-accessibility";
const LEGACY_FEEDBACK_KEY = "csnexus-feedback-enabled";

const DEFAULT_STUDY: StudyPreferences = {
  dailyGoalMinutes: 30,
  defaultQuizMode: "practice",
  examDate: null,
};

const DEFAULT_ACCESSIBILITY: AccessibilityPreferences = {
  reducedMotion: "system",
  fontSize: "default",
  soundEnabled: true,
  hapticEnabled: true,
};

// --- localStorage helpers ---

function storageAvailable(): boolean {
  try {
    const testKey = "__storage_test__";
    localStorage.setItem(testKey, "1");
    localStorage.removeItem(testKey);
    return true;
  } catch {
    return false;
  }
}

function readJSON<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(key);
    if (raw === null) return null;
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

function writeJSON<T>(key: string, value: T): void {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // Quota exceeded or localStorage disabled — silent fallback
  }
}

// --- Migration ---

/**
 * Migrate the legacy "csnexus-feedback-enabled" key into the new
 * accessibility preferences namespace.
 *
 * If "csnexus-settings-accessibility" already exists, skip migration.
 * If the legacy key exists, read its boolean value and use it for both
 * soundEnabled and hapticEnabled, then delete the legacy key.
 *
 * This is idempotent: once migration writes the new key and removes
 * the legacy key, subsequent calls are a no-op.
 */
function runMigration(): void {
  if (!storageAvailable()) return;

  try {
    const existing = localStorage.getItem(ACCESSIBILITY_KEY);
    if (existing !== null) return; // already migrated or user has new prefs

    const legacyValue = localStorage.getItem(LEGACY_FEEDBACK_KEY);
    if (legacyValue === null) return; // nothing to migrate

    const feedbackEnabled = legacyValue !== "false";
    const migrated: AccessibilityPreferences = {
      ...DEFAULT_ACCESSIBILITY,
      soundEnabled: feedbackEnabled,
      hapticEnabled: feedbackEnabled,
    };

    writeJSON(ACCESSIBILITY_KEY, migrated);
    localStorage.removeItem(LEGACY_FEEDBACK_KEY);
  } catch {
    // Silent — migration is best-effort
  }
}

// --- Getters ---

export function getStudyPreferences(): StudyPreferences {
  if (!storageAvailable()) return { ...DEFAULT_STUDY };

  const stored = readJSON<Partial<StudyPreferences>>(STUDY_KEY);
  if (!stored) return { ...DEFAULT_STUDY };

  return {
    dailyGoalMinutes: stored.dailyGoalMinutes ?? DEFAULT_STUDY.dailyGoalMinutes,
    defaultQuizMode: stored.defaultQuizMode ?? DEFAULT_STUDY.defaultQuizMode,
    examDate: stored.examDate ?? DEFAULT_STUDY.examDate,
  };
}

export function getAccessibilityPreferences(): AccessibilityPreferences {
  runMigration();

  if (!storageAvailable()) return { ...DEFAULT_ACCESSIBILITY };

  const stored = readJSON<Partial<AccessibilityPreferences>>(ACCESSIBILITY_KEY);
  if (!stored) return { ...DEFAULT_ACCESSIBILITY };

  return {
    reducedMotion: stored.reducedMotion ?? DEFAULT_ACCESSIBILITY.reducedMotion,
    fontSize: stored.fontSize ?? DEFAULT_ACCESSIBILITY.fontSize,
    soundEnabled: stored.soundEnabled ?? DEFAULT_ACCESSIBILITY.soundEnabled,
    hapticEnabled: stored.hapticEnabled ?? DEFAULT_ACCESSIBILITY.hapticEnabled,
  };
}

// --- Setters ---

export function setStudyPreference<K extends keyof StudyPreferences>(
  key: K,
  value: StudyPreferences[K]
): void {
  const current = getStudyPreferences();
  current[key] = value;
  writeJSON(STUDY_KEY, current);
}

export function setAccessibilityPreference<K extends keyof AccessibilityPreferences>(
  key: K,
  value: AccessibilityPreferences[K]
): void {
  const current = getAccessibilityPreferences();
  current[key] = value;
  writeJSON(ACCESSIBILITY_KEY, current);
}

// --- Convenience methods ---

export function isSoundEnabled(): boolean {
  return getAccessibilityPreferences().soundEnabled;
}

export function setSoundEnabled(enabled: boolean): void {
  setAccessibilityPreference("soundEnabled", enabled);
}

export function isHapticEnabled(): boolean {
  return getAccessibilityPreferences().hapticEnabled;
}

export function setHapticEnabled(enabled: boolean): void {
  setAccessibilityPreference("hapticEnabled", enabled);
}

// --- DOM Application ---

/**
 * Apply accessibility preferences to the document root element.
 * Sets `data-font-size` and `data-reduced-motion` attributes on `<html>`.
 */
export function applyAccessibilityToDOM(): void {
  const prefs = getAccessibilityPreferences();
  const root = document.documentElement;

  // Font size: only set attribute for non-default values, or always set for clarity
  root.setAttribute("data-font-size", prefs.fontSize);

  // Reduced motion: set attribute so CSS rules can respond
  root.setAttribute("data-reduced-motion", prefs.reducedMotion);
}
