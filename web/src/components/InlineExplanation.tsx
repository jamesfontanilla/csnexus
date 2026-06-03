import { useState } from "react";
import { Link } from "react-router-dom";
import { GlassCard } from "./GlassCard";
import { GlassBadge } from "./GlassBadge";
import { GlassButton } from "./GlassButton";
import { useExplanation } from "../hooks/useExplanation";

interface InlineExplanationProps {
  questionId: number;
  /** Simple explanation text from the quiz response (fallback) */
  fallbackText?: string;
}

/**
 * Rich inline explanation panel shown after answer submission.
 * Displays explanation text (markdown), key concept badge, related subtopic links,
 * and "Still confused? Ask why" escalation button.
 *
 * Requirements: 7.2, 7.3, 7.4, 8.1
 */
export function InlineExplanation({ questionId, fallbackText }: InlineExplanationProps) {
  const { explanation, loading, escalate } = useExplanation(questionId);
  const [tutorResponse, setTutorResponse] = useState<string | null>(null);
  const [escalating, setEscalating] = useState(false);
  const [escalationError, setEscalationError] = useState<string | null>(null);

  async function handleEscalate() {
    setEscalating(true);
    setEscalationError(null);
    const response = await escalate();
    if (response) {
      setTutorResponse(response);
    } else {
      setEscalationError("Rate limit reached (20/day) or tutor unavailable.");
    }
    setEscalating(false);
  }

  // Don't render anything if no explanation and no fallback
  if (!explanation && !fallbackText && !loading) return null;

  // Loading state — show fallback if available
  if (loading && !explanation) {
    if (fallbackText) {
      return (
        <div style={{ marginTop: "var(--space-3)", padding: "var(--space-3)", borderRadius: "var(--radius-md)", background: "var(--glass-bg-subtle)" }}>
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
            {fallbackText}
          </p>
        </div>
      );
    }
    return null;
  }

  // Rich explanation available
  if (explanation) {
    return (
      <div
        style={{
          marginTop: "var(--space-3)",
          borderRadius: "var(--radius-md)",
          border: "1px solid var(--glass-border-light)",
          overflow: "hidden",
        }}
      >
        {/* Key concept badge */}
        <div style={{ padding: "var(--space-3) var(--space-4)", borderBottom: "1px solid var(--glass-border-light)", display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
          <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Key Concept:</span>
          <GlassBadge label={explanation.key_concept} color="accent" size="sm" />
        </div>

        {/* Explanation text */}
        <div style={{ padding: "var(--space-4)" }}>
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text)", lineHeight: 1.7, whiteSpace: "pre-wrap" }}>
            {explanation.explanation_text}
          </p>

          {/* Related subtopics */}
          {explanation.related_subtopics.length > 0 && (
            <div style={{ marginTop: "var(--space-3)", display: "flex", gap: "var(--space-2)", flexWrap: "wrap", alignItems: "center" }}>
              <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Related:</span>
              {explanation.related_subtopics.map((id) => (
                <Link
                  key={id}
                  to={`/subtopics/${id}/lesson`}
                  style={{ fontSize: "var(--font-size-xs)", color: "var(--color-accent)", textDecoration: "none" }}
                >
                  Subtopic #{id}
                </Link>
              ))}
            </div>
          )}

          {/* Concrete examples callout */}
          {explanation.concrete_examples && explanation.concrete_examples.length > 0 && (
            <div
              style={{
                marginTop: "var(--space-3)",
                padding: "var(--space-3)",
                borderRadius: "var(--radius-sm)",
                background: "rgba(212,165,116,0.06)",
                borderLeft: "3px solid var(--color-accent)",
              }}
            >
              <p style={{ margin: "0 0 var(--space-2)", fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-accent)" }}>
                💡 Think of it like this:
              </p>
              {explanation.concrete_examples.map((example, idx) => (
                <p key={idx} style={{ margin: "var(--space-1) 0", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", lineHeight: 1.5 }}>
                  • {example}
                </p>
              ))}
            </div>
          )}
        </div>

        {/* AI Tutor escalation */}
        <div style={{ padding: "var(--space-3) var(--space-4)", borderTop: "1px solid var(--glass-border-light)" }}>
          {tutorResponse ? (
            <div style={{ padding: "var(--space-3)", borderRadius: "var(--radius-sm)", background: "var(--glass-bg-subtle)" }}>
              <p style={{ margin: 0, fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-accent)", marginBottom: "var(--space-1)" }}>
                🤖 AI Tutor
              </p>
              <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text)", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
                {tutorResponse}
              </p>
            </div>
          ) : (
            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
              <GlassButton
                variant="ghost"
                size="sm"
                onClick={handleEscalate}
                disabled={escalating}
              >
                {escalating ? "Asking..." : "Still confused? Ask why"}
              </GlassButton>
              {escalationError && (
                <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-warning)" }}>
                  {escalationError}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Fallback to simple text
  if (fallbackText) {
    return (
      <div style={{ marginTop: "var(--space-3)", padding: "var(--space-3)", borderRadius: "var(--radius-md)", background: "var(--glass-bg-subtle)" }}>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
          {fallbackText}
        </p>
      </div>
    );
  }

  return null;
}
