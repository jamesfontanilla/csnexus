import { useState } from "react";
import type { PracticeProblem } from "./types";

interface PracticePanelProps {
  problems: PracticeProblem[];
  memoryAids: string[];
  examStrategies: string[];
  keyTakeaways: string[];
}

/**
 * Companion panel for desktop layout.
 * Shows interactive practice problems, memory aids, exam strategies, and key takeaways.
 */
export function PracticePanel({ problems, memoryAids, examStrategies, keyTakeaways }: PracticePanelProps) {
  const [activeTab, setActiveTab] = useState<"practice" | "aids" | "takeaways">(
    problems.length > 0 ? "practice" : "takeaways"
  );

  const tabs = [
    { id: "practice" as const, label: "Practice", count: problems.length, show: problems.length > 0 },
    { id: "aids" as const, label: "Aids & Tips", count: memoryAids.length + examStrategies.length, show: memoryAids.length > 0 || examStrategies.length > 0 },
    { id: "takeaways" as const, label: "Takeaways", count: keyTakeaways.length, show: keyTakeaways.length > 0 },
  ].filter((t) => t.show);

  return (
    <aside
      aria-label="Practice and study aids"
      style={{
        position: "sticky",
        top: "5rem",
        maxHeight: "calc(100vh - 6rem)",
        overflowY: "auto",
        scrollbarWidth: "thin",
      }}
    >
      {/* Tab bar */}
      <div style={{ display: "flex", gap: "0.25rem", marginBottom: "0.75rem", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.5rem" }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: "0.3rem 0.6rem",
              fontSize: "0.6875rem",
              fontWeight: activeTab === tab.id ? 600 : 400,
              background: activeTab === tab.id ? "rgba(212, 165, 116, 0.12)" : "transparent",
              border: "1px solid",
              borderColor: activeTab === tab.id ? "rgba(212, 165, 116, 0.3)" : "rgba(255,255,255,0.08)",
              borderRadius: "4px",
              cursor: "pointer",
              color: activeTab === tab.id ? "var(--color-accent, #d4a574)" : "var(--color-text-muted)",
              transition: "all 0.15s ease",
            }}
          >
            {tab.label}
            {tab.count > 0 && (
              <span style={{ marginLeft: "0.25rem", opacity: 0.6 }}>({tab.count})</span>
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "practice" && <PracticeProblems problems={problems} />}
      {activeTab === "aids" && <AidsAndStrategies memoryAids={memoryAids} examStrategies={examStrategies} />}
      {activeTab === "takeaways" && <TakeawaysList items={keyTakeaways} />}
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Practice Problems — interactive quiz cards
// ---------------------------------------------------------------------------

function PracticeProblems({ problems }: { problems: PracticeProblem[] }) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [score, setScore] = useState({ correct: 0, attempted: 0 });

  if (problems.length === 0) return null;

  const problem = problems[currentIdx];

  function handleReveal() {
    setRevealed(true);
    setScore((s) => ({ ...s, attempted: s.attempted + 1 }));
  }

  function handleNext(wasCorrect: boolean) {
    if (wasCorrect) setScore((s) => ({ ...s, correct: s.correct + 1 }));
    setRevealed(false);
    setCurrentIdx((i) => (i + 1) % problems.length);
  }

  const difficultyColors: Record<string, string> = {
    easy: "rgba(80, 200, 120, 0.2)",
    medium: "rgba(212, 165, 116, 0.2)",
    hard: "rgba(220, 80, 80, 0.2)",
  };

  return (
    <div>
      {/* Score header */}
      {score.attempted > 0 && (
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginBottom: "0.5rem", textAlign: "center" }}>
          {score.correct}/{score.attempted} correct
        </div>
      )}

      {/* Problem card */}
      <div
        style={{
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          overflow: "hidden",
          marginBottom: "0.5rem",
        }}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0.5rem 0.75rem", background: "rgba(255,255,255,0.03)", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <span style={{ fontSize: "0.625rem", fontWeight: 600, color: "var(--color-text-muted)" }}>
            #{problem.number} of {problems.length}
          </span>
          <span
            style={{
              fontSize: "0.5625rem",
              fontWeight: 700,
              padding: "0.1rem 0.4rem",
              borderRadius: "3px",
              background: difficultyColors[problem.difficulty] || "rgba(255,255,255,0.1)",
              textTransform: "uppercase",
              letterSpacing: "0.03em",
              color: "var(--color-text)",
            }}
          >
            {problem.difficulty}
          </span>
        </div>

        {/* Question */}
        <div style={{ padding: "0.75rem", fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }}>
          {problem.question}
        </div>

        {/* Answer area */}
        {!revealed ? (
          <button
            onClick={handleReveal}
            style={{
              width: "100%",
              padding: "0.5rem",
              background: "rgba(212, 165, 116, 0.06)",
              border: "none",
              borderTop: "1px solid rgba(255,255,255,0.06)",
              cursor: "pointer",
              fontSize: "0.75rem",
              fontWeight: 600,
              color: "var(--color-accent, #d4a574)",
            }}
          >
            Show Answer
          </button>
        ) : (
          <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}>
            <div style={{ padding: "0.5rem 0.75rem", background: "rgba(80, 200, 120, 0.04)" }}>
              <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "rgba(80, 200, 120, 0.8)", marginBottom: "0.25rem" }}>
                Answer
              </div>
              <div style={{ fontSize: "0.8125rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {problem.answer}
              </div>
              {problem.explanation && (
                <div style={{ marginTop: "0.375rem", fontSize: "0.75rem", color: "var(--color-text-secondary)", lineHeight: 1.5 }}>
                  {problem.explanation}
                </div>
              )}
            </div>
            {/* Self-assessment buttons */}
            <div style={{ display: "flex", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
              <button
                onClick={() => handleNext(false)}
                style={{
                  flex: 1,
                  padding: "0.4rem",
                  background: "rgba(220, 80, 80, 0.06)",
                  border: "none",
                  borderRight: "1px solid rgba(255,255,255,0.06)",
                  cursor: "pointer",
                  fontSize: "0.6875rem",
                  fontWeight: 600,
                  color: "rgba(220, 80, 80, 0.8)",
                }}
              >
                ✗ Got it wrong
              </button>
              <button
                onClick={() => handleNext(true)}
                style={{
                  flex: 1,
                  padding: "0.4rem",
                  background: "rgba(80, 200, 120, 0.06)",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "0.6875rem",
                  fontWeight: 600,
                  color: "rgba(80, 200, 120, 0.8)",
                }}
              >
                ✓ Got it right
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Problem navigation dots */}
      <div style={{ display: "flex", justifyContent: "center", gap: "0.25rem", flexWrap: "wrap" }}>
        {problems.map((_, i) => (
          <button
            key={i}
            onClick={() => { setCurrentIdx(i); setRevealed(false); }}
            aria-label={`Go to problem ${i + 1}`}
            style={{
              width: "0.5rem",
              height: "0.5rem",
              borderRadius: "50%",
              border: "none",
              cursor: "pointer",
              background: i === currentIdx
                ? "var(--color-accent, #d4a574)"
                : "rgba(255,255,255,0.15)",
              transition: "background 0.15s",
            }}
          />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Memory Aids & Exam Strategies
// ---------------------------------------------------------------------------

function AidsAndStrategies({ memoryAids, examStrategies }: { memoryAids: string[]; examStrategies: string[] }) {
  return (
    <div>
      {memoryAids.length > 0 && (
        <div style={{ marginBottom: "1rem" }}>
          <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.375rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            🧠 Memory Aids
          </div>
          <ul style={{ margin: 0, paddingLeft: "1rem" }}>
            {memoryAids.map((aid, i) => (
              <li key={i} style={{ marginBottom: "0.375rem", fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {aid}
              </li>
            ))}
          </ul>
        </div>
      )}

      {examStrategies.length > 0 && (
        <div>
          <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.375rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            🎯 Exam Strategies
          </div>
          <ul style={{ margin: 0, paddingLeft: "1rem" }}>
            {examStrategies.map((strategy, i) => (
              <li key={i} style={{ marginBottom: "0.375rem", fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {strategy}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Key Takeaways
// ---------------------------------------------------------------------------

function TakeawaysList({ items }: { items: string[] }) {
  return (
    <div>
      <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.5rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
        🔑 Key Takeaways
      </div>
      <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
        {items.map((item, i) => (
          <li
            key={i}
            style={{
              display: "flex",
              gap: "0.5rem",
              alignItems: "flex-start",
              marginBottom: "0.5rem",
              padding: "0.4rem 0.5rem",
              background: "rgba(212, 165, 116, 0.04)",
              borderRadius: "4px",
              border: "1px solid rgba(212, 165, 116, 0.1)",
            }}
          >
            <span style={{ flexShrink: 0, fontSize: "0.625rem", fontWeight: 700, color: "var(--color-accent, #d4a574)", marginTop: "0.125rem" }}>
              {i + 1}
            </span>
            <span style={{ fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
              {item}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
