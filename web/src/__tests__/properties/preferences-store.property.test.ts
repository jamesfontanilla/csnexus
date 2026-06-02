import { describe, it, expect, beforeEach } from "vitest";
import * as fc from "fast-check";
import {
  getStudyPreferences,
  getAccessibilityPreferences,
  setStudyPreference,
  setAccessibilityPreference,
} from "../../stores/preferences";
import type {
  StudyPreferences,
  AccessibilityPreferences,
} from "../../stores/preferences";

/**
 * **Validates: Requirements 6.3, 6.2, 3.5, 4.9**
 *
 * Property 1: Preferences Store Round-Trip
 *
 * For any valid preferences object (study or accessibility), writing it
 * to the Preferences_Store and then reading it back SHALL produce an
 * equivalent object.
 */

// --- Arbitraries ---

const dailyGoalMinutesArb = fc.integer({ min: 1, max: 36 }).map((n) => n * 5); // 5–180, step 5

const defaultQuizModeArb = fc.constantFrom(
  "practice" as const,
  "exam" as const,
  "power" as const
);

const isoDateArb = fc
  .integer({ min: 0, max: 29219 }) // days from 2020-01-01 to 2099-12-31
  .map((days) => {
    const base = new Date("2020-01-01T00:00:00Z");
    base.setUTCDate(base.getUTCDate() + days);
    return base.toISOString().slice(0, 10);
  });

const examDateArb = fc.oneof(isoDateArb, fc.constant(null));

const studyPreferencesArb: fc.Arbitrary<StudyPreferences> = fc.record({
  dailyGoalMinutes: dailyGoalMinutesArb,
  defaultQuizMode: defaultQuizModeArb,
  examDate: examDateArb,
});

const reducedMotionArb = fc.constantFrom(
  "system" as const,
  "on" as const,
  "off" as const
);

const fontSizeArb = fc.constantFrom(
  "compact" as const,
  "default" as const,
  "large" as const
);

const accessibilityPreferencesArb: fc.Arbitrary<AccessibilityPreferences> =
  fc.record({
    reducedMotion: reducedMotionArb,
    fontSize: fontSizeArb,
    soundEnabled: fc.boolean(),
    hapticEnabled: fc.boolean(),
  });

// --- Tests ---

describe("Property 1: Preferences Store Round-Trip", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("StudyPreferences round-trip: write then read produces equivalent object", () => {
    fc.assert(
      fc.property(studyPreferencesArb, (prefs) => {
        localStorage.clear();

        setStudyPreference("dailyGoalMinutes", prefs.dailyGoalMinutes);
        setStudyPreference("defaultQuizMode", prefs.defaultQuizMode);
        setStudyPreference("examDate", prefs.examDate);

        const read = getStudyPreferences();

        expect(read.dailyGoalMinutes).toBe(prefs.dailyGoalMinutes);
        expect(read.defaultQuizMode).toBe(prefs.defaultQuizMode);
        expect(read.examDate).toBe(prefs.examDate);
      }),
      { numRuns: 100 }
    );
  });

  it("AccessibilityPreferences round-trip: write then read produces equivalent object", () => {
    fc.assert(
      fc.property(accessibilityPreferencesArb, (prefs) => {
        localStorage.clear();

        setAccessibilityPreference("reducedMotion", prefs.reducedMotion);
        setAccessibilityPreference("fontSize", prefs.fontSize);
        setAccessibilityPreference("soundEnabled", prefs.soundEnabled);
        setAccessibilityPreference("hapticEnabled", prefs.hapticEnabled);

        const read = getAccessibilityPreferences();

        expect(read.reducedMotion).toBe(prefs.reducedMotion);
        expect(read.fontSize).toBe(prefs.fontSize);
        expect(read.soundEnabled).toBe(prefs.soundEnabled);
        expect(read.hapticEnabled).toBe(prefs.hapticEnabled);
      }),
      { numRuns: 100 }
    );
  });
});
