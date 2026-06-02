import { describe, it, expect, beforeEach } from "vitest";
import {
  getStudyPreferences,
  getAccessibilityPreferences,
  setStudyPreference,
  setAccessibilityPreference,
  isSoundEnabled,
  setSoundEnabled,
  isHapticEnabled,
  setHapticEnabled,
  applyAccessibilityToDOM,
} from "../../stores/preferences";

describe("Preferences Store", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  describe("getStudyPreferences", () => {
    it("returns defaults when nothing is stored", () => {
      const prefs = getStudyPreferences();
      expect(prefs).toEqual({
        dailyGoalMinutes: 30,
        defaultQuizMode: "practice",
        examDate: null,
      });
    });

    it("returns stored values when present", () => {
      localStorage.setItem(
        "csnexus-settings-study",
        JSON.stringify({
          dailyGoalMinutes: 60,
          defaultQuizMode: "exam",
          examDate: "2025-12-01",
        })
      );
      const prefs = getStudyPreferences();
      expect(prefs.dailyGoalMinutes).toBe(60);
      expect(prefs.defaultQuizMode).toBe("exam");
      expect(prefs.examDate).toBe("2025-12-01");
    });

    it("fills missing fields with defaults", () => {
      localStorage.setItem(
        "csnexus-settings-study",
        JSON.stringify({ dailyGoalMinutes: 45 })
      );
      const prefs = getStudyPreferences();
      expect(prefs.dailyGoalMinutes).toBe(45);
      expect(prefs.defaultQuizMode).toBe("practice");
      expect(prefs.examDate).toBeNull();
    });
  });

  describe("getAccessibilityPreferences", () => {
    it("returns defaults when nothing is stored", () => {
      const prefs = getAccessibilityPreferences();
      expect(prefs).toEqual({
        reducedMotion: "system",
        fontSize: "default",
        soundEnabled: true,
        hapticEnabled: true,
      });
    });

    it("returns stored values when present", () => {
      localStorage.setItem(
        "csnexus-settings-accessibility",
        JSON.stringify({
          reducedMotion: "on",
          fontSize: "large",
          soundEnabled: false,
          hapticEnabled: false,
        })
      );
      const prefs = getAccessibilityPreferences();
      expect(prefs.reducedMotion).toBe("on");
      expect(prefs.fontSize).toBe("large");
      expect(prefs.soundEnabled).toBe(false);
      expect(prefs.hapticEnabled).toBe(false);
    });
  });

  describe("setStudyPreference", () => {
    it("persists a single field change", () => {
      setStudyPreference("dailyGoalMinutes", 90);
      const prefs = getStudyPreferences();
      expect(prefs.dailyGoalMinutes).toBe(90);
      expect(prefs.defaultQuizMode).toBe("practice");
    });
  });

  describe("setAccessibilityPreference", () => {
    it("persists a single field change", () => {
      setAccessibilityPreference("fontSize", "large");
      const prefs = getAccessibilityPreferences();
      expect(prefs.fontSize).toBe("large");
      expect(prefs.reducedMotion).toBe("system");
    });
  });

  describe("convenience methods", () => {
    it("isSoundEnabled returns true by default", () => {
      expect(isSoundEnabled()).toBe(true);
    });

    it("setSoundEnabled persists the value", () => {
      setSoundEnabled(false);
      expect(isSoundEnabled()).toBe(false);
    });

    it("isHapticEnabled returns true by default", () => {
      expect(isHapticEnabled()).toBe(true);
    });

    it("setHapticEnabled persists the value", () => {
      setHapticEnabled(false);
      expect(isHapticEnabled()).toBe(false);
    });
  });

  describe("backward-compatibility migration", () => {
    it("migrates legacy feedback key into accessibility prefs", () => {
      localStorage.setItem("csnexus-feedback-enabled", "false");
      const prefs = getAccessibilityPreferences();
      expect(prefs.soundEnabled).toBe(false);
      expect(prefs.hapticEnabled).toBe(false);
      // legacy key should be removed
      expect(localStorage.getItem("csnexus-feedback-enabled")).toBeNull();
    });

    it("migrates legacy feedback key value true", () => {
      localStorage.setItem("csnexus-feedback-enabled", "true");
      const prefs = getAccessibilityPreferences();
      expect(prefs.soundEnabled).toBe(true);
      expect(prefs.hapticEnabled).toBe(true);
      expect(localStorage.getItem("csnexus-feedback-enabled")).toBeNull();
    });

    it("does not migrate if accessibility prefs already exist", () => {
      localStorage.setItem(
        "csnexus-settings-accessibility",
        JSON.stringify({
          reducedMotion: "off",
          fontSize: "compact",
          soundEnabled: true,
          hapticEnabled: true,
        })
      );
      localStorage.setItem("csnexus-feedback-enabled", "false");
      const prefs = getAccessibilityPreferences();
      // should use existing prefs, not the legacy key
      expect(prefs.soundEnabled).toBe(true);
      // legacy key should remain untouched
      expect(localStorage.getItem("csnexus-feedback-enabled")).toBe("false");
    });
  });

  describe("applyAccessibilityToDOM", () => {
    it("sets data-font-size attribute on html element", () => {
      setAccessibilityPreference("fontSize", "large");
      applyAccessibilityToDOM();
      expect(document.documentElement.getAttribute("data-font-size")).toBe(
        "large"
      );
    });

    it("sets data-reduced-motion attribute on html element", () => {
      setAccessibilityPreference("reducedMotion", "on");
      applyAccessibilityToDOM();
      expect(document.documentElement.getAttribute("data-reduced-motion")).toBe(
        "on"
      );
    });

    it("sets default values when no preferences stored", () => {
      applyAccessibilityToDOM();
      expect(document.documentElement.getAttribute("data-font-size")).toBe(
        "default"
      );
      expect(document.documentElement.getAttribute("data-reduced-motion")).toBe(
        "system"
      );
    });
  });

  describe("localStorage unavailability", () => {
    it("returns defaults when localStorage throws", () => {
      const originalGetItem = Storage.prototype.getItem;
      const originalSetItem = Storage.prototype.setItem;
      const originalRemoveItem = Storage.prototype.removeItem;

      Storage.prototype.getItem = () => {
        throw new Error("SecurityError");
      };
      Storage.prototype.setItem = () => {
        throw new Error("SecurityError");
      };
      Storage.prototype.removeItem = () => {
        throw new Error("SecurityError");
      };

      const study = getStudyPreferences();
      expect(study.dailyGoalMinutes).toBe(30);

      const accessibility = getAccessibilityPreferences();
      expect(accessibility.soundEnabled).toBe(true);

      // Should not crash
      setStudyPreference("dailyGoalMinutes", 60);
      setAccessibilityPreference("fontSize", "large");

      Storage.prototype.getItem = originalGetItem;
      Storage.prototype.setItem = originalSetItem;
      Storage.prototype.removeItem = originalRemoveItem;
    });
  });
});
