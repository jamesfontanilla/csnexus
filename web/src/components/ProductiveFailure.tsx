import { useState } from "react";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { GlassBadge } from "./GlassBadge";
import { GradientText } from "./GradientText";
import {
  learningTechniquesApi,
  type ChallengeAttemptResponse,
  type ChallengeComparisonResponse,
} from "../api/learningTechniques";

interface ProductiveFailureProps {
  subtopicId: number;
  onComplete: () => void;
  onSkip: () => void;
}

/**
 * Productive Failure UI — challenge problem with failure-normalizing framing.
 * Presents a hard question before the lesson, then allows retest after.
 * Requirements: 28.2, 28.3, 28.4
 */
export function ProductiveFailure({ subtopicId, onComplete, onSkip }: ProductiveFailureProps) {
  const [phase, setPhase] = useState<"challenge" | "result" | "retest" | "comparison">("challenge");
  const [answer, setAnswer] = useState("");
  const [challengeResult, setChallengeResult] = useState<ChallengeAttemptResponse | null>(null);
  const [comparison, setComparison] = useState<ChallengeComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmitChallenge() {
    if (!answer.trim()) return;
    setLoading(true);
    try {
      const res = await learningTechniquesApi.submitChallengeAttempt(subtopicId, answer.trim());
      setChallengeResult(res);
      setPhase("result");
    } catch {
      onSkip(); // Challenge not available
    } finally {
      setLoading(false);
    }
  }

  async function handleRetest() {
    if (!answer.trim() || !challengeResult) return;
    setLoading(true);
    try {
      const res = await learningTechniquesApi.submitChallengeRetest(challengeResult.challenge_id, answer.trim());
      setComparison(res);
      setPhase("comparison");
    } catch {
      onComplete();
    } finally {
      setLoading(false);
    }
  }

  if (phase === "challenge") {
    return (
      <GlassCard style={{ padding: "var(--space-5)" }}>
        <div style={{ textAlign: "center", marginBottom: "var(--space-4)" }}>
          <p style={{ fontSize: "1.5rem", marginBottom: "var(--space-1)" }}>🧩</p>
          <h3 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-2)" }}>
            <GradientText variant="accent">Challenge Problem</GradientText>
          </h3>
          <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", lineHeight: 1.5 }}>
            This is intentionally hard. Getting it wrong is part of the learning process —
            it primes your brain to absorb the lesson better.
          </p>
        </div>

        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", marginBottom: "var(--space-3)" }}>
          Try your best guess. There's no penalty for being wrong here.
        </p>

        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Your best guess..."
          aria-label="Challenge answer"
          onKeyDown={(e) => { if (e.key === "Enter") handleSubmitChallenge(); }}
          style={{
            width: "100%",
            padding: "var(--space-3)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--glass-border-light)",
            background: "var(--glass-bg-subtle)",
            color: "var(--color-text)",
            fontSize: "var(--font-size-base)",
            marginBottom: "var(--space-3)",
          }}
        />
        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end" }}>
          <GlassButton variant="ghost" size="sm" onClick={onSkip}>
            Skip
          </GlassButton>
          <GlassButton variant="primary" size="sm" onClick={handleSubmitChallenge} disabled={loading || !answer.trim()}>
            {loading ? "Checking..." : "Submit"}
          </GlassButton>
        </div>
      </GlassCard>
    );
  }

  if (phase === "result" && challengeResult) {
    return (
      <GlassCard style={{ padding: "var(--space-5)", textAlign: "center" }}>
        <GlassBadge
          label={challengeResult.is_correct ? "Got it!" : "Good try!"}
          color={challengeResult.is_correct ? "success" : "accent"}
          size="md"
        />
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", marginTop: "var(--space-3)", lineHeight: 1.6 }}>
          {challengeResult.message}
        </p>
        <GlassButton variant="primary" size="md" onClick={onComplete} style={{ marginTop: "var(--space-4)" }}>
          Start Lesson →
        </GlassButton>
      </GlassCard>
    );
  }

  if (phase === "retest" && challengeResult) {
    return (
      <GlassCard style={{ padding: "var(--space-5)" }}>
        <h3 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", textAlign: "center" }}>
          <GradientText variant="accent">Retest: Can you get it now?</GradientText>
        </h3>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", marginBottom: "var(--space-3)" }}>
          {challengeResult.question_stem}
        </p>
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Your answer after the lesson..."
          aria-label="Retest answer"
          onKeyDown={(e) => { if (e.key === "Enter") handleRetest(); }}
          style={{
            width: "100%",
            padding: "var(--space-3)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--glass-border-light)",
            background: "var(--glass-bg-subtle)",
            color: "var(--color-text)",
            fontSize: "var(--font-size-base)",
            marginBottom: "var(--space-3)",
          }}
        />
        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end" }}>
          <GlassButton variant="ghost" size="sm" onClick={onComplete}>
            Skip
          </GlassButton>
          <GlassButton variant="primary" size="sm" onClick={handleRetest} disabled={loading || !answer.trim()}>
            {loading ? "Checking..." : "Submit"}
          </GlassButton>
        </div>
      </GlassCard>
    );
  }

  if (phase === "comparison" && comparison) {
    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        {comparison.is_productive_failure_success ? (
          <>
            <p style={{ fontSize: "2rem", marginBottom: "var(--space-2)" }}>🎉</p>
            <GlassBadge label="Productive Failure Success!" color="success" size="md" />
          </>
        ) : comparison.post_lesson_correct ? (
          <>
            <p style={{ fontSize: "2rem", marginBottom: "var(--space-2)" }}>✨</p>
            <GlassBadge label="Strong Knowledge" color="success" size="md" />
          </>
        ) : (
          <>
            <p style={{ fontSize: "2rem", marginBottom: "var(--space-2)" }}>📚</p>
            <GlassBadge label="Keep Practicing" color="warning" size="md" />
          </>
        )}
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", marginTop: "var(--space-3)", lineHeight: 1.6 }}>
          {comparison.message}
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)", marginTop: "var(--space-4)" }}>
          <div>
            <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Before lesson</p>
            <p style={{ margin: 0, fontSize: "var(--font-size-base)", fontWeight: 600, color: comparison.pre_lesson_correct ? "var(--color-success)" : "var(--color-danger)" }}>
              {comparison.pre_lesson_correct ? "✓ Correct" : "✗ Wrong"}
            </p>
          </div>
          <div>
            <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>After lesson</p>
            <p style={{ margin: 0, fontSize: "var(--font-size-base)", fontWeight: 600, color: comparison.post_lesson_correct ? "var(--color-success)" : "var(--color-danger)" }}>
              {comparison.post_lesson_correct ? "✓ Correct" : "✗ Wrong"}
            </p>
          </div>
        </div>
        <GlassButton variant="primary" size="md" onClick={onComplete} style={{ marginTop: "var(--space-4)" }}>
          Continue
        </GlassButton>
      </GlassCard>
    );
  }

  return null;
}
