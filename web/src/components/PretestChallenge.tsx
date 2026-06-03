import { useState } from "react";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { GradientText } from "./GradientText";
import { learningTechniquesApi, type PretestStartResponse, type PretestSubmitResponse } from "../api/learningTechniques";

interface PretestChallengeProps {
  subtopicId: number;
  onComplete: () => void;
  onSkip: () => void;
}

/**
 * Pretest challenge UI shown before first lesson visit.
 * Presents 3-5 questions with encouraging framing, then shows results.
 * Requirements: 20.1, 20.3, 20.5, 20.6
 */
export function PretestChallenge({ subtopicId, onComplete, onSkip }: PretestChallengeProps) {
  const [phase, setPhase] = useState<"intro" | "questions" | "results">("intro");
  const [pretest, setPretest] = useState<PretestStartResponse | null>(null);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [results, setResults] = useState<PretestSubmitResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [currentIdx, setCurrentIdx] = useState(0);

  async function handleStart() {
    setLoading(true);
    try {
      const res = await learningTechniquesApi.startPretest(subtopicId);
      setPretest(res);
      setPhase("questions");
    } catch {
      // Pretest not applicable (lesson done or not enough questions) — skip
      onSkip();
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit() {
    if (!pretest) return;
    setLoading(true);
    try {
      const answerList = pretest.questions.map((q) => ({
        question_id: q.id,
        selected_answer: answers[q.id] || "",
      }));
      const res = await learningTechniquesApi.submitPretest(pretest.pretest_id, answerList);
      setResults(res);
      setPhase("results");
    } catch {
      onComplete();
    } finally {
      setLoading(false);
    }
  }

  if (phase === "intro") {
    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, marginBottom: "var(--space-3)" }}>
          <GradientText variant="accent">Quick Knowledge Check</GradientText>
        </h2>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "var(--space-4)", lineHeight: 1.6 }}>
          Before diving into the lesson, let's see what you already know.
          Don't worry about getting things wrong — research shows this actually helps you learn better!
        </p>
        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "center" }}>
          <GlassButton variant="ghost" size="md" onClick={onSkip}>
            Skip to lesson
          </GlassButton>
          <GlassButton variant="primary" size="md" onClick={handleStart} disabled={loading}>
            {loading ? "Loading..." : "Let's try it!"}
          </GlassButton>
        </div>
      </GlassCard>
    );
  }

  if (phase === "questions" && pretest) {
    const question = pretest.questions[currentIdx];
    const totalQ = pretest.questions.length;

    return (
      <GlassCard style={{ padding: "var(--space-5)" }}>
        <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", marginBottom: "var(--space-3)" }}>
          Question {currentIdx + 1} of {totalQ} • Key concept: {question.key_concept}
        </p>
        <p style={{ fontSize: "var(--font-size-base)", fontWeight: 500, color: "var(--color-text)", marginBottom: "var(--space-4)", lineHeight: 1.6 }}>
          {question.stem}
        </p>
        <div style={{ display: "grid", gap: "var(--space-2)", marginBottom: "var(--space-4)" }}>
          {question.options.map((opt) => (
            <button
              key={opt}
              onClick={() => setAnswers({ ...answers, [question.id]: opt })}
              aria-pressed={answers[question.id] === opt}
              style={{
                padding: "var(--space-3)",
                borderRadius: "var(--radius-md)",
                border: `2px solid ${answers[question.id] === opt ? "var(--color-accent)" : "var(--glass-border-light)"}`,
                background: answers[question.id] === opt ? "var(--color-accent-subtle)" : "var(--glass-bg-subtle)",
                color: "var(--color-text)",
                fontSize: "var(--font-size-sm)",
                textAlign: "left",
                cursor: "pointer",
              }}
            >
              {opt}
            </button>
          ))}
        </div>
        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end" }}>
          {currentIdx > 0 && (
            <GlassButton variant="ghost" size="sm" onClick={() => setCurrentIdx(currentIdx - 1)}>
              Previous
            </GlassButton>
          )}
          {currentIdx < totalQ - 1 ? (
            <GlassButton variant="primary" size="sm" onClick={() => setCurrentIdx(currentIdx + 1)}>
              Next
            </GlassButton>
          ) : (
            <GlassButton variant="primary" size="sm" onClick={handleSubmit} disabled={loading}>
              {loading ? "Submitting..." : "See Results"}
            </GlassButton>
          )}
        </div>
      </GlassCard>
    );
  }

  if (phase === "results" && results) {
    const percentage = results.total_questions > 0
      ? Math.round((results.correct_count / results.total_questions) * 100)
      : 0;

    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, marginBottom: "var(--space-3)" }}>
          <GradientText variant="accent">Baseline Set!</GradientText>
        </h2>
        <p style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, marginBottom: "var(--space-2)" }}>
          {results.correct_count}/{results.total_questions} ({percentage}%)
        </p>
        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "var(--space-4)", lineHeight: 1.6 }}>
          {percentage >= 80
            ? "Great foundation! The lesson will help you master the finer details."
            : "Perfect — the lesson ahead will fill in these gaps. After completing it, you'll see how much you've improved!"}
        </p>
        {results.weak_concepts.length > 0 && (
          <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", marginBottom: "var(--space-4)" }}>
            Focus areas: {results.weak_concepts.join(", ")}
          </p>
        )}
        <GlassButton variant="primary" size="md" onClick={onComplete}>
          Start Lesson →
        </GlassButton>
      </GlassCard>
    );
  }

  return null;
}
