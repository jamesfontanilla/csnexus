import { useState } from "react";
import { isSoundEnabled, setSoundEnabled } from "../stores/preferences";

/**
 * Toggle for sound/haptic feedback preferences.
 * Renders as a small icon button suitable for settings or navbar.
 */
export function FeedbackToggle() {
  const [enabled, setEnabled] = useState(isSoundEnabled);

  function toggle() {
    const next = !enabled;
    setEnabled(next);
    setSoundEnabled(next);
  }

  return (
    <button
      onClick={toggle}
      aria-label={enabled ? "Disable sound feedback" : "Enable sound feedback"}
      aria-pressed={enabled}
      title={enabled ? "Sound on" : "Sound off"}
      style={{
        background: "var(--glass-bg-subtle)",
        border: "1px solid var(--glass-border-light)",
        borderRadius: "var(--radius-sm)",
        padding: "var(--space-2)",
        cursor: "pointer",
        fontSize: "1rem",
        lineHeight: 1,
        color: enabled ? "var(--color-accent)" : "var(--color-text-muted)",
        transition: "color var(--transition-fast), background var(--transition-fast)",
      }}
    >
      {enabled ? "🔊" : "🔇"}
    </button>
  );
}
