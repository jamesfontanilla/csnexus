import { useState } from "react";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { GradientText } from "./GradientText";
import { learningTechniquesApi } from "../api/learningTechniques";

interface SessionReflectionPromptProps {
  sessionDate: string;
  /** Items from today's session to pick "hardest" from */
  sessionItems?: Array<{ id: number; label: string }>;
  onComplete: () => void;
  onSkip: () => void;
}

/**
 * 30-second post-session metacognitive reflection prompt.
 * Shown after queue completion with hardest item selector, confidence slider, optional note.
 * Requirements: 26.1, 26.2, 26.6
 */
export function SessionReflectionPrompt({
  sessionDate,
  sessionItems = [],
  onComplete,
  onSkip,
}: SessionReflectionPromptProps) {
  const [hardestItemId, setHardestItemId] = useState<number | null>(null);
  const [confidence, setConfidence] = useState(3);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setSubmitting(true);
    try {
      await learningTechniquesApi.createSessionReflection(sessionDate, {
        hardest_item_id: hardestItemId ?? undefined,
        confidence_rating: confidence,
        review_note: note.trim() || undefined,
      });
      onComplete();
    } catch {
      onComplete(); // Don't block on failure
    } finally {
      setSubmitting(false);
    }
  }

  const confidenceLabels = ["Very low", "Low", "Moderate", "High", "Very high"];

  return (
    <GlassCard style={{ padding: "var(--space-5)" }}>
      <h3 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-2)", textAlign: "center" }}>
        <GradientText variant="accent">Quick Reflection</GradientText>
      </h3>
      <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", textAlign: "center", marginBottom: "var(--space-4)" }}>
        Takes 30 seconds — helps your brain consolidate what you studied
      </p>

      {/* Hardest item selector */}
      {sessionItems.length > 0 && (
        <div style={{ marginBottom: "var(--space-4)" }}>
          <label style={{ display: "block", fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-text-secondary)", marginBottom: "var(--space-2)" }}>
            What felt hardest today?
          </label>
          <select
            value={hardestItemId ?? ""}
            onChange={(e) => setHardestItemId(e.target.value ? parseInt(e.target.value) : null)}
            aria-label="Hardest item"
            style={{
              width: "100%",
              padding: "var(--space-2)",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--glass-border-light)",
              background: "var(--glass-bg-subtle)",
              color: "var(--color-text)",
              fontSize: "var(--font-size-sm)",
            }}
          >
            <option value="">None in particular</option>
            {sessionItems.map((item) => (
              <option key={item.id} value={item.id}>{item.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Confidence slider */}
      <div style={{ marginBottom: "var(--space-4)" }}>
        <label style={{ display: "block", fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-text-secondary)", marginBottom: "var(--space-2)" }}>
          How confident do you feel about today's material?
        </label>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
          <input
            type="range"
            min={1}
            max={5}
            value={confidence}
            onChange={(e) => setConfidence(parseInt(e.target.value))}
            aria-label="Confidence rating"
            style={{ flex: 1 }}
          />
          <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", minWidth: 80, textAlign: "right" }}>
            {confidenceLabels[confidence - 1]}
          </span>
        </div>
      </div>

      {/* Optional note */}
      <div style={{ marginBottom: "var(--space-4)" }}>
        <label style={{ display: "block", fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-text-secondary)", marginBottom: "var(--space-2)" }}>
          Anything to remember? (optional)
        </label>
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          maxLength={1000}
          placeholder="What surprised you? What needs more review?"
          aria-label="Review note"
          style={{
            width: "100%",
            minHeight: 50,
            padding: "var(--space-2)",
            borderRadius: "var(--radius-sm)",
            border: "1px solid var(--glass-border-light)",
            background: "var(--glass-bg-subtle)",
            color: "var(--color-text)",
            fontSize: "var(--font-size-sm)",
            resize: "vertical",
            fontFamily: "inherit",
          }}
        />
      </div>

      <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end" }}>
        <GlassButton variant="ghost" size="sm" onClick={onSkip}>
          Skip
        </GlassButton>
        <GlassButton variant="primary" size="sm" onClick={handleSubmit} disabled={submitting}>
          {submitting ? "Saving..." : "Done"}
        </GlassButton>
      </div>
    </GlassCard>
  );
}
