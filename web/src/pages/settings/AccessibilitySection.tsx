import { useState, useEffect } from "react";
import {
  getAccessibilityPreferences,
  setAccessibilityPreference,
  applyAccessibilityToDOM,
  isSoundEnabled,
  setSoundEnabled,
  isHapticEnabled,
  setHapticEnabled,
} from "../../stores/preferences";
import type { AccessibilityPreferences } from "../../stores/preferences";

type ReducedMotionOption = AccessibilityPreferences["reducedMotion"];
type FontSizeOption = AccessibilityPreferences["fontSize"];

const REDUCED_MOTION_OPTIONS: { value: ReducedMotionOption; label: string }[] = [
  { value: "system", label: "System" },
  { value: "on", label: "On" },
  { value: "off", label: "Off" },
];

const FONT_SIZE_OPTIONS: { value: FontSizeOption; label: string }[] = [
  { value: "compact", label: "Compact" },
  { value: "default", label: "Default" },
  { value: "large", label: "Large" },
];

// --- Styles ---

const controlGroupStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: "var(--space-2)",
};

const labelStyle: React.CSSProperties = {
  fontSize: "var(--font-size-sm)",
  fontWeight: 500,
  color: "var(--color-text)",
};

const descriptionStyle: React.CSSProperties = {
  fontSize: "var(--font-size-xs)",
  color: "var(--color-text-muted)",
  margin: 0,
};

const segmentedGroupStyle: React.CSSProperties = {
  display: "flex",
  gap: "var(--space-1)",
  background: "var(--glass-bg-subtle)",
  border: "1px solid var(--glass-border-light)",
  borderRadius: "var(--radius-sm)",
  padding: "var(--space-1)",
};

const segmentButtonBase: React.CSSProperties = {
  flex: 1,
  padding: "var(--space-2) var(--space-3)",
  fontSize: "var(--font-size-sm)",
  fontWeight: 500,
  border: "none",
  borderRadius: "calc(var(--radius-sm) - 2px)",
  cursor: "pointer",
  transition: "background var(--transition-fast), color var(--transition-fast)",
  lineHeight: 1.4,
};

const toggleRowStyle: React.CSSProperties = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: "var(--space-3)",
};

const toggleTrackStyle = (active: boolean): React.CSSProperties => ({
  position: "relative",
  width: 44,
  height: 24,
  borderRadius: "var(--radius-full)",
  background: active ? "var(--color-accent)" : "var(--glass-bg-strong)",
  border: `1px solid ${active ? "var(--color-accent)" : "var(--glass-border-medium)"}`,
  cursor: "pointer",
  transition: "background var(--transition-fast), border-color var(--transition-fast)",
  flexShrink: 0,
});

const toggleThumbStyle = (active: boolean): React.CSSProperties => ({
  position: "absolute",
  top: 2,
  left: active ? 22 : 2,
  width: 18,
  height: 18,
  borderRadius: "50%",
  background: active ? "var(--color-primary)" : "var(--color-text-secondary)",
  transition: "left var(--transition-fast), background var(--transition-fast)",
});

export function AccessibilitySection() {
  const [reducedMotion, setReducedMotion] = useState<ReducedMotionOption>("system");
  const [fontSize, setFontSize] = useState<FontSizeOption>("default");
  const [soundOn, setSoundOn] = useState(true);
  const [hapticOn, setHapticOn] = useState(true);

  // Load on mount
  useEffect(() => {
    const prefs = getAccessibilityPreferences();
    setReducedMotion(prefs.reducedMotion);
    setFontSize(prefs.fontSize);
    setSoundOn(prefs.soundEnabled);
    setHapticOn(prefs.hapticEnabled);
  }, []);

  function handleReducedMotionChange(value: ReducedMotionOption) {
    setReducedMotion(value);
    setAccessibilityPreference("reducedMotion", value);
    applyAccessibilityToDOM();
  }

  function handleFontSizeChange(value: FontSizeOption) {
    setFontSize(value);
    setAccessibilityPreference("fontSize", value);
    applyAccessibilityToDOM();
  }

  function handleSoundToggle() {
    const next = !soundOn;
    setSoundOn(next);
    setSoundEnabled(next);
    applyAccessibilityToDOM();
  }

  function handleHapticToggle() {
    const next = !hapticOn;
    setHapticOn(next);
    setHapticEnabled(next);
    applyAccessibilityToDOM();
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-5)" }}>
      {/* Reduced Motion */}
      <div style={controlGroupStyle}>
        <label style={labelStyle} id="reduced-motion-label">
          Reduced Motion
        </label>
        <p style={descriptionStyle}>
          Control whether animations and transitions are shown.
        </p>
        <div
          role="radiogroup"
          aria-labelledby="reduced-motion-label"
          style={segmentedGroupStyle}
        >
          {REDUCED_MOTION_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              role="radio"
              aria-checked={reducedMotion === opt.value}
              onClick={() => handleReducedMotionChange(opt.value)}
              style={{
                ...segmentButtonBase,
                background:
                  reducedMotion === opt.value
                    ? "var(--glass-bg-strong)"
                    : "transparent",
                color:
                  reducedMotion === opt.value
                    ? "var(--color-text)"
                    : "var(--color-text-muted)",
                boxShadow:
                  reducedMotion === opt.value
                    ? "var(--shadow-subtle)"
                    : "none",
              }}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Font Size */}
      <div style={controlGroupStyle}>
        <label style={labelStyle} id="font-size-label">
          Font Size
        </label>
        <p style={descriptionStyle}>
          Adjust text size across the application.
        </p>
        <div
          role="radiogroup"
          aria-labelledby="font-size-label"
          style={segmentedGroupStyle}
        >
          {FONT_SIZE_OPTIONS.map((opt) => (
            <button
              key={opt.value}
              role="radio"
              aria-checked={fontSize === opt.value}
              onClick={() => handleFontSizeChange(opt.value)}
              style={{
                ...segmentButtonBase,
                background:
                  fontSize === opt.value
                    ? "var(--glass-bg-strong)"
                    : "transparent",
                color:
                  fontSize === opt.value
                    ? "var(--color-text)"
                    : "var(--color-text-muted)",
                boxShadow:
                  fontSize === opt.value
                    ? "var(--shadow-subtle)"
                    : "none",
              }}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>

      {/* Sound Effects Toggle */}
      <div style={controlGroupStyle}>
        <div style={toggleRowStyle}>
          <div>
            <label style={labelStyle} id="sound-label">
              Sound Effects
            </label>
            <p style={descriptionStyle}>
              Play audio feedback on interactions.
            </p>
          </div>
          <button
            role="switch"
            aria-checked={soundOn}
            aria-labelledby="sound-label"
            onClick={handleSoundToggle}
            style={{
              ...toggleTrackStyle(soundOn),
              border: "none",
              padding: 0,
              outline: "none",
            }}
          >
            <span style={toggleThumbStyle(soundOn)} />
          </button>
        </div>
      </div>

      {/* Haptic Feedback Toggle */}
      <div style={controlGroupStyle}>
        <div style={toggleRowStyle}>
          <div>
            <label style={labelStyle} id="haptic-label">
              Haptic Feedback
            </label>
            <p style={descriptionStyle}>
              Enable vibration feedback on supported devices.
            </p>
          </div>
          <button
            role="switch"
            aria-checked={hapticOn}
            aria-labelledby="haptic-label"
            onClick={handleHapticToggle}
            style={{
              ...toggleTrackStyle(hapticOn),
              border: "none",
              padding: 0,
              outline: "none",
            }}
          >
            <span style={toggleThumbStyle(hapticOn)} />
          </button>
        </div>
      </div>
    </div>
  );
}
