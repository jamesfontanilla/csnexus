import { useState, useEffect } from "react";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { GradientText } from "./GradientText";
import { GlassSkeleton } from "./GlassSkeleton";
import { learningTechniquesApi, type GoodnightSessionResponse } from "../api/learningTechniques";

/**
 * Compact goodnight review UI — triggered at bedtime.
 * Shows 5-10 items with lowest confidence from today's study activity.
 * Requirements: 25.1, 25.2, 25.3
 */
export function GoodnightReview({ onDismiss }: { onDismiss: () => void }) {
  const [session, setSession] = useState<GoodnightSessionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    learningTechniquesApi.getGoodnightReview()
      .then(setSession)
      .catch(() => setSession(null))
      .finally(() => setLoading(false));
  }, []);

  async function handleComplete() {
    try {
      await learningTechniquesApi.completeGoodnightReview();
    } catch {
      // Non-critical
    }
    setCompleted(true);
  }

  if (loading) {
    return (
      <GlassCard style={{ padding: "var(--space-6)" }}>
        <GlassSkeleton variant="card" />
      </GlassCard>
    );
  }

  if (!session || session.items.length === 0) {
    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        <p style={{ fontSize: "1.5rem", marginBottom: "var(--space-2)" }}>🌙</p>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: 0 }}>
          No review items for tonight — you're all caught up! Sleep well.
        </p>
        <GlassButton variant="ghost" size="sm" onClick={onDismiss} style={{ marginTop: "var(--space-3)" }}>
          Dismiss
        </GlassButton>
      </GlassCard>
    );
  }

  if (completed) {
    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        <p style={{ fontSize: "2rem", marginBottom: "var(--space-2)" }}>🌙✨</p>
        <h3 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-2)" }}>
          <GradientText variant="accent">Sleep Consolidation Active</GradientText>
        </h3>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "var(--space-4)", lineHeight: 1.6 }}>
          Research shows that reviewing material before sleep enhances memory consolidation.
          Your brain will reinforce these concepts overnight. Good night!
        </p>
        <GlassButton variant="primary" size="md" onClick={onDismiss}>
          Good night 🌙
        </GlassButton>
      </GlassCard>
    );
  }

  const item = session.items[currentIdx];
  const totalItems = session.items.length;

  return (
    <GlassCard style={{ padding: "var(--space-5)" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-4)" }}>
        <h3 style={{ margin: 0, fontSize: "var(--font-size-sm)", fontWeight: 600 }}>
          🌙 Goodnight Review ({currentIdx + 1}/{totalItems})
        </h3>
        <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          ~{session.estimated_minutes} min
        </span>
      </div>

      {/* Question */}
      <p style={{ fontSize: "var(--font-size-base)", color: "var(--color-text)", marginBottom: "var(--space-4)", lineHeight: 1.6 }}>
        {item.stem}
      </p>

      {/* Answer reveal */}
      {showAnswer ? (
        <div
          style={{
            padding: "var(--space-3)",
            borderRadius: "var(--radius-sm)",
            background: "rgba(100,255,100,0.05)",
            borderLeft: "3px solid var(--color-success)",
            marginBottom: "var(--space-4)",
          }}
        >
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text)" }}>
            <strong>{item.correct_answer}</strong>
          </p>
        </div>
      ) : (
        <GlassButton variant="ghost" size="sm" onClick={() => setShowAnswer(true)} style={{ marginBottom: "var(--space-4)" }}>
          Show Answer
        </GlassButton>
      )}

      {/* Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <GlassButton variant="ghost" size="sm" onClick={onDismiss}>
          Skip rest
        </GlassButton>
        {currentIdx < totalItems - 1 ? (
          <GlassButton
            variant="primary"
            size="sm"
            onClick={() => { setCurrentIdx(currentIdx + 1); setShowAnswer(false); }}
          >
            Next →
          </GlassButton>
        ) : (
          <GlassButton variant="primary" size="sm" onClick={handleComplete}>
            Done ✓
          </GlassButton>
        )}
      </div>
    </GlassCard>
  );
}
