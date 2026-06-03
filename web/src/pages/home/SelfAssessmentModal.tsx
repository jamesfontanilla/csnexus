import { useState } from "react";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GradientText } from "../../components/GradientText";
import { useSelfAssessment } from "../../hooks/useReadiness";
import type { SelfAssessmentResponse } from "../../api/readiness";

/**
 * Self-assessment calibration modal.
 * Shows when is_self_assessment_due returns true on dashboard load.
 * After submission, shows comparison and calibration feedback.
 */
export function SelfAssessmentModal({ onDismiss }: { onDismiss: () => void }) {
  const { submit } = useSelfAssessment();
  const [score, setScore] = useState(50);
  const [result, setResult] = useState<SelfAssessmentResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setSubmitting(true);
    const res = await submit(score);
    if (res) setResult(res);
    setSubmitting(false);
  }

  // Show result after submission
  if (result) {
    return (
      <div
        role="dialog"
        aria-labelledby="sa-result-title"
        aria-modal="true"
        style={{
          position: "fixed",
          inset: 0,
          zIndex: 1000,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "var(--space-4)",
          background: "rgba(0,0,0,0.5)",
          backdropFilter: "blur(4px)",
        }}
      >
        <GlassCard style={{ maxWidth: 420, width: "100%", padding: "var(--space-6)" }}>
          <h2
            id="sa-result-title"
            style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, marginBottom: "var(--space-4)", textAlign: "center" }}
          >
            <GradientText variant="accent">Calibration Result</GradientText>
          </h2>

          {/* Score comparison */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)", textAlign: "center", marginBottom: "var(--space-4)" }}>
            <div>
              <p style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, color: "var(--color-text)" }}>
                {result.self_assessed_score}
              </p>
              <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Your Estimate</p>
            </div>
            <div>
              <p style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, color: "var(--color-accent)" }}>
                {result.computed_score}
              </p>
              <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Actual Score</p>
            </div>
          </div>

          {/* Delta indicator */}
          <p style={{ textAlign: "center", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "var(--space-3)" }}>
            Difference: <strong>{result.delta > 0 ? "+" : ""}{result.delta}</strong>
          </p>

          {/* Calibration message */}
          <div
            style={{
              padding: "var(--space-3)",
              borderRadius: "var(--radius-md)",
              background: result.calibration_status === "overconfident"
                ? "rgba(255,200,100,0.08)"
                : result.calibration_status === "underconfident"
                ? "rgba(100,180,255,0.08)"
                : "rgba(100,255,100,0.08)",
              marginBottom: "var(--space-4)",
            }}
          >
            <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text)" }}>
              {result.message}
            </p>
            {result.calibration_warning && (
              <p style={{ margin: "var(--space-2) 0 0", fontSize: "var(--font-size-xs)", color: "var(--color-warning)" }}>
                {result.calibration_warning}
              </p>
            )}
          </div>

          <div style={{ textAlign: "center" }}>
            <GlassButton variant="primary" size="md" onClick={onDismiss}>
              Got it
            </GlassButton>
          </div>
        </GlassCard>
      </div>
    );
  }

  // Input form
  return (
    <div
      role="dialog"
      aria-labelledby="sa-title"
      aria-modal="true"
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 1000,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "var(--space-4)",
        background: "rgba(0,0,0,0.5)",
        backdropFilter: "blur(4px)",
      }}
    >
      <GlassCard style={{ maxWidth: 400, width: "100%", padding: "var(--space-6)" }}>
        <h2
          id="sa-title"
          style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, marginBottom: "var(--space-2)", textAlign: "center" }}
        >
          <GradientText variant="accent">How Ready Do You Feel?</GradientText>
        </h2>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", textAlign: "center", marginBottom: "var(--space-5)" }}>
          Rate your exam readiness from 0 to 100. We'll compare it to your actual performance.
        </p>

        {/* Slider input */}
        <div style={{ marginBottom: "var(--space-4)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "var(--space-2)" }}>
            <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Not Ready</span>
            <span style={{ fontSize: "var(--font-size-lg)", fontWeight: 700, color: "var(--color-accent)" }}>{score}</span>
            <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Exam Ready</span>
          </div>
          <input
            type="range"
            min={0}
            max={100}
            value={score}
            onChange={(e) => setScore(parseInt(e.target.value, 10))}
            aria-label="Self-assessed readiness score"
            style={{ width: "100%", cursor: "pointer" }}
          />
        </div>

        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "center" }}>
          <GlassButton variant="ghost" size="md" onClick={onDismiss} disabled={submitting}>
            Not now
          </GlassButton>
          <GlassButton variant="primary" size="md" onClick={handleSubmit} disabled={submitting}>
            {submitting ? "Submitting..." : "Submit"}
          </GlassButton>
        </div>
      </GlassCard>
    </div>
  );
}
