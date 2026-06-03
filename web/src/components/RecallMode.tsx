import { useState } from "react";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { GlassBadge } from "./GlassBadge";
import { learningTechniquesApi, type RecallAnswerResponse } from "../api/learningTechniques";

interface RecallModeProps {
  attemptId: number;
  questionId: number;
  stem: string;
  onComplete: (result: RecallAnswerResponse) => void;
}

/**
 * Recall Mode UI for quiz player — text input instead of MCQ options.
 * Grades using keyword matching + Levenshtein distance ≤ 2.
 * Requirements: 24.1, 24.4
 */
export function RecallMode({ attemptId, questionId, stem, onComplete }: RecallModeProps) {
  const [response, setResponse] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<RecallAnswerResponse | null>(null);

  async function handleSubmit() {
    if (!response.trim()) return;
    setSubmitting(true);
    try {
      const res = await learningTechniquesApi.submitRecallAnswer(attemptId, questionId, response.trim());
      setResult(res);
      onComplete(res);
    } catch {
      // Fall back to showing the input again
    } finally {
      setSubmitting(false);
    }
  }

  if (result) {
    return (
      <div style={{ marginTop: "var(--space-3)" }}>
        <div
          style={{
            padding: "var(--space-3)",
            borderRadius: "var(--radius-md)",
            background: result.is_correct === true
              ? "rgba(100,255,100,0.05)"
              : result.is_correct === false
              ? "rgba(255,100,100,0.05)"
              : "rgba(255,200,100,0.05)",
            border: `1px solid ${
              result.is_correct === true
                ? "var(--color-success)"
                : result.is_correct === false
                ? "var(--color-danger)"
                : "var(--color-warning)"
            }`,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", marginBottom: "var(--space-2)" }}>
            {result.match_type === "exact" && (
              <GlassBadge label="Exact Match ✓" color="success" size="sm" />
            )}
            {result.match_type === "fuzzy" && (
              <GlassBadge label="Close Enough ✓" color="success" size="sm" />
            )}
            {result.match_type === "needs_review" && (
              <GlassBadge label="Needs Review" color="warning" size="sm" />
            )}
          </div>
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text)" }}>
            Your answer: <strong>{result.user_response}</strong>
          </p>
          <p style={{ margin: "var(--space-1) 0 0", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
            Correct answer: <strong>{result.correct_answer}</strong>
          </p>
          {result.match_type === "needs_review" && (
            <p style={{ margin: "var(--space-2) 0 0", fontSize: "var(--font-size-xs)", color: "var(--color-warning)" }}>
              Your answer was too different from the expected answer. Review the material and try again later.
            </p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={{ marginTop: "var(--space-3)" }}>
      <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", marginBottom: "var(--space-2)" }}>
        🧠 Recall Mode — type your answer from memory
      </p>
      <input
        type="text"
        value={response}
        onChange={(e) => setResponse(e.target.value)}
        placeholder="Type your answer..."
        aria-label="Recall answer"
        onKeyDown={(e) => { if (e.key === "Enter") handleSubmit(); }}
        style={{
          width: "100%",
          padding: "var(--space-3)",
          borderRadius: "var(--radius-md)",
          border: "1px solid var(--glass-border-light)",
          background: "var(--glass-bg-subtle)",
          color: "var(--color-text)",
          fontSize: "var(--font-size-base)",
          marginBottom: "var(--space-2)",
        }}
      />
      <GlassButton variant="primary" size="sm" onClick={handleSubmit} disabled={submitting || !response.trim()}>
        {submitting ? "Checking..." : "Submit Answer"}
      </GlassButton>
    </div>
  );
}
