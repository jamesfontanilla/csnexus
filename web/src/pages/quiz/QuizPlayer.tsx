import { useEffect, useMemo, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient, ApiError } from "../../api/client";
import { PageTransition } from "../../components/PageTransition";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { AnimatedNumber } from "../../components/AnimatedNumber";
import { GradientText } from "../../components/GradientText";
import { InlineExplanation } from "../../components/InlineExplanation";
import { scaleIn, staggerContainer, staggerItem, springDefault, useReducedMotion } from "../../design-system";
import { soundCorrect, soundIncorrect, soundTap, hapticTap } from "../../utils/feedback";
import { prefetchExplanations } from "../../hooks/useExplanation";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface QuizQuestion {
  id: number;
  ordinal: number;
  stem: string;
  qtype: string;
  difficulty: string;
  options: string[] | null;
  selected_answer?: string | null;
  is_correct?: boolean;
  correct_answer?: string;
  explanation?: string;
}

interface QuizAttempt {
  attempt_id: number;
  status: string;
  score?: number;
  max_score?: number;
  started_at: string;
  time_limit_seconds: number | null;
  questions: QuizQuestion[];
  total_questions?: number;
}

// ---------------------------------------------------------------------------
// Quiz mode config
// ---------------------------------------------------------------------------

type QuizMode = "practice" | "exam" | "power";

interface ModeConfig {
  label: string;
  description: string;
  timeLimitSeconds: number;
  color: string;
  icon: string;
}

// ---------------------------------------------------------------------------
// SVG-aware rendering helpers
// ---------------------------------------------------------------------------

/** Detect if a string contains SVG and render it safely. */
function StemRenderer({ text }: { text: string }) {
  if (!text.includes("<svg")) {
    return <>{text}</>;
  }
  // Split into text part and SVG part
  const svgStart = text.indexOf("<svg");
  const textPart = text.slice(0, svgStart).trim();
  const svgPart = text.slice(svgStart).trim();

  return (
    <>
      {textPart && <span>{textPart}</span>}
      {svgPart && (
        <div
          style={{ marginTop: "0.75rem", display: "flex", justifyContent: "center", overflow: "auto" }}
          dangerouslySetInnerHTML={{ __html: svgPart }}
          role="img"
          aria-label="Question diagram"
        />
      )}
    </>
  );
}

/** Parse an option string that may contain "LABEL: <svg...>" format. */
function parseOption(opt: string): { label: string; hasSvg: boolean; svgContent: string } {
  const svgIdx = opt.indexOf("<svg");
  if (svgIdx === -1) {
    return { label: opt, hasSvg: false, svgContent: "" };
  }
  const label = opt.slice(0, svgIdx).replace(/:$/, "").trim();
  const svgContent = opt.slice(svgIdx);
  return { label, hasSvg: true, svgContent };
}

/** Render an option value (selected_answer or correct_answer) with SVG support. */
function OptionDisplay({ value, isCorrect }: { value: string; isCorrect?: boolean }) {
  const { label, hasSvg, svgContent } = parseOption(value);
  const color =
    isCorrect === true
      ? "var(--color-success)"
      : isCorrect === false
        ? "var(--color-danger)"
        : "var(--color-text-muted)";

  if (!hasSvg) {
    return <code style={{ color }}>{value}</code>;
  }

  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}>
      <code style={{ color, fontWeight: 600 }}>{label}</code>
      <span
        dangerouslySetInnerHTML={{ __html: svgContent }}
        style={{ display: "inline-block", verticalAlign: "middle" }}
      />
    </span>
  );
}

const MODES: Record<QuizMode, ModeConfig> = {
  practice: {
    label: "Practice Mode",
    description: "20 minutes — relaxed pace, review as you go",
    timeLimitSeconds: 20 * 60,
    color: "var(--color-success)",
    icon: "📖",
  },
  exam: {
    label: "Exam Mode",
    description: "15 minutes — simulates real CSE conditions",
    timeLimitSeconds: 15 * 60,
    color: "var(--color-accent)",
    icon: "📝",
  },
  power: {
    label: "Power Mode",
    description: "10 minutes — maximum challenge, fastest pace",
    timeLimitSeconds: 10 * 60,
    color: "var(--color-danger)",
    icon: "⚡",
  },
};

// ---------------------------------------------------------------------------
// Difficulty badge
// ---------------------------------------------------------------------------

const DIFFICULTY_STYLES: Record<string, { label: string; color: string; bg: string }> = {
  EASY: { label: "Easy", color: "var(--color-success)", bg: "var(--color-success)1a" },
  MEDIUM: { label: "Medium", color: "var(--color-accent)", bg: "var(--color-accent)1a" },
  HARD: { label: "Hard", color: "var(--color-danger)", bg: "var(--color-danger)1a" },
};

function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const style = DIFFICULTY_STYLES[difficulty] ?? {
    label: difficulty,
    color: "var(--color-text-secondary)",
    bg: "var(--glass-bg-subtle)",
  };
  return (
    <span
      aria-label={`Difficulty: ${style.label}`}
      style={{
        display: "inline-block",
        padding: "0.125rem 0.625rem",
        borderRadius: "var(--radius-full, 9999px)",
        fontSize: "0.75rem",
        fontWeight: 600,
        letterSpacing: "0.04em",
        color: style.color,
        background: style.bg,
        border: `1px solid ${style.color}44`,
      }}
    >
      {style.label}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Timer hook
// ---------------------------------------------------------------------------

function useCountdown(totalSeconds: number | null, onExpire: () => void) {
  const [remaining, setRemaining] = useState<number | null>(
    totalSeconds !== null ? totalSeconds : null
  );
  const expiredRef = useRef(false);
  // Keep onExpire in a ref so the interval always calls the latest version
  // without needing to restart the timer when the callback identity changes.
  const onExpireRef = useRef(onExpire);
  useEffect(() => { onExpireRef.current = onExpire; });

  useEffect(() => {
    if (totalSeconds === null) return;
    setRemaining(totalSeconds);
    expiredRef.current = false;

    const id = setInterval(() => {
      setRemaining((prev) => {
        if (prev === null) return null;
        const next = prev - 1;
        if (next <= 0 && !expiredRef.current) {
          expiredRef.current = true;
          clearInterval(id);
          onExpireRef.current();
          return 0;
        }
        return next;
      });
    }, 1000);

    return () => clearInterval(id);
  }, [totalSeconds]);

  return remaining;
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function timerColor(remaining: number): string {
  if (remaining < 30) return "var(--color-danger)";
  return "var(--color-text)";
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function QuizPlayer() {
  const { scope, scopeId } = useParams<{ scope: string; scopeId: string }>();
  const reducedMotion = useReducedMotion();

  // Phase: "select-mode" → "in-progress" → "submitted"
  // "lesson-blocked" is a special phase shown when the lesson isn't done yet
  const [phase, setPhase] = useState<"select-mode" | "in-progress" | "submitted" | "lesson-blocked">("select-mode");
  const [selectedMode, setSelectedMode] = useState<QuizMode | null>(null);

  const [attempt, setAttempt] = useState<QuizAttempt | null>(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // Memoized so it only recomputes when phase or attempt changes,
  // preventing the timer from restarting on unrelated renders.
  const computedTimeLimit = useMemo(() => {
    if (phase !== "in-progress" || !attempt?.time_limit_seconds) return null;
    const elapsed = Math.floor(
      (Date.now() - new Date(attempt.started_at).getTime()) / 1000
    );
    const left = attempt.time_limit_seconds - elapsed;
    return left > 0 ? left : 0;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, attempt?.attempt_id]);

  const remaining = useCountdown(
    computedTimeLimit,
    () => {
      // Auto-submit when timer expires
      if (phase === "in-progress" && attempt) {
        handleSubmitQuiz();
      }
    }
  );

  function startUrl(): string {
    switch (scope) {
      case "topic":
        return `/v1/topics/${scopeId}/quiz-attempts`;
      case "module":
        return `/v1/modules/${scopeId}/quiz-attempts`;
      default:
        return `/v1/subtopics/${scopeId}/quiz-attempts`;
    }
  }

  async function handleStartQuiz(mode: QuizMode) {
    setSelectedMode(mode);
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.post<QuizAttempt>(startUrl(), {
        time_limit_seconds: MODES[mode].timeLimitSeconds,
      });
      setAttempt(res);
      setCurrentIdx(0);
      setPhase("in-progress");
    } catch (err: unknown) {
      if (
        err instanceof ApiError &&
        err.status === 409 &&
        (err.code === "LESSON_NOT_COMPLETED" || err.message === "lesson_not_completed")
      ) {
        setPhase("lesson-blocked");
      } else {
        setError(err instanceof Error ? err.message : "Failed to start quiz");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleSelectAnswer(questionId: number, selected: string) {
    if (!attempt) return;
    hapticTap();
    soundTap();
    try {
      await apiClient.patch(
        `/v1/quiz-attempts/${attempt.attempt_id}/answers/${questionId}`,
        { selected_answer: selected }
      );
      setAttempt((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          questions: prev.questions.map((q) =>
            q.id === questionId ? { ...q, selected_answer: selected } : q
          ),
        };
      });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to save answer");
    }
  }

  async function handleSubmitQuiz() {
    if (!attempt || submitting) return;
    setSubmitting(true);
    try {
      const res = await apiClient.post<QuizAttempt>(
        `/v1/quiz-attempts/${attempt.attempt_id}:submit`
      );
      setAttempt(res);
      setPhase("submitted");
      // Prefetch explanations for offline access
      const questionIds = res.questions.map((q) => q.id);
      prefetchExplanations(questionIds);
      // Sound feedback based on result
      const score = res.score ?? 0;
      const maxScore = res.max_score ?? 1;
      if (score / maxScore >= 0.8) {
        soundCorrect();
      } else {
        soundIncorrect();
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to submit quiz");
    } finally {
      setSubmitting(false);
    }
  }

  // ---------------------------------------------------------------------------
  // Phase: Lesson not completed
  // ---------------------------------------------------------------------------

  if (phase === "lesson-blocked") {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 520 }}>
          <motion.div
            initial={scaleIn.initial}
            animate={scaleIn.animate}
            transition={scaleIn.transition}
          >
            <GlassCard blur="lg" style={{ textAlign: "center", padding: "2.5rem 2rem" }}>
              <div style={{ fontSize: "3.5rem", marginBottom: "1rem" }}>📖</div>
              <h1 style={{
                color: "var(--color-text)",
                fontSize: "1.375rem",
                marginBottom: "0.5rem",
              }}>
                Lesson Not Completed
              </h1>
              <p style={{
                color: "var(--color-text-secondary)",
                fontSize: "0.9375rem",
                lineHeight: 1.6,
                marginBottom: "1.75rem",
              }}>
                You need to finish reading the lesson before you can take the quiz.
                Complete the lesson first, then come back here to test your knowledge.
              </p>
              <div style={{ display: "flex", gap: "0.75rem", justifyContent: "center", flexWrap: "wrap" }}>
                <Link
                  to={scope === "subtopic" ? `/subtopics/${scopeId}/lesson` : "/modules"}
                  style={{ textDecoration: "none" }}
                >
                  <GlassButton variant="primary">
                    {scope === "subtopic" ? "Go to Lesson" : "Back to Modules"}
                  </GlassButton>
                </Link>
                <GlassButton
                  variant="secondary"
                  onClick={() => { setPhase("select-mode"); setError(null); }}
                >
                  ← Back
                </GlassButton>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </PageTransition>
    );
  }

  // ---------------------------------------------------------------------------
  // Phase: Mode selection
  // ---------------------------------------------------------------------------

  if (phase === "select-mode") {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 640 }}>
          <motion.div
            initial={scaleIn.initial}
            animate={scaleIn.animate}
            transition={scaleIn.transition}
          >
            <GlassCard blur="lg" style={{ textAlign: "center", marginBottom: "1.5rem" }}>
              <h1 style={{ color: "var(--color-text)", marginBottom: "0.25rem", fontSize: "1.5rem" }}>
                Choose Your Mode
              </h1>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem", margin: 0 }}>
                20 questions drawn randomly from the question bank
              </p>
            </GlassCard>
          </motion.div>

          {error && (
            <p style={{ color: "var(--color-danger)", marginBottom: "1rem", textAlign: "center" }}>
              {error}
            </p>
          )}

          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            style={{ display: "grid", gap: "0.75rem", marginBottom: "1.5rem" }}
          >
            {(Object.entries(MODES) as [QuizMode, ModeConfig][]).map(([key, cfg]) => (
              <motion.div key={key} variants={staggerItem} transition={springDefault}>
                <motion.button
                  onClick={() => handleStartQuiz(key)}
                  disabled={loading}
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.98 }}
                  transition={springDefault}
                  aria-label={`Start ${cfg.label}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "1rem",
                    width: "100%",
                    textAlign: "left",
                    cursor: loading ? "not-allowed" : "pointer",
                    padding: "1.25rem 1.5rem",
                    borderRadius: "var(--radius-md)",
                    background: "var(--glass-bg-subtle)",
                    border: `1.5px solid ${cfg.color}33`,
                    color: "var(--color-text)",
                    fontFamily: "var(--font-family)",
                    opacity: loading ? 0.6 : 1,
                    transition: "border-color 150ms ease, background 150ms ease",
                  }}
                >
                  <span style={{ fontSize: "2rem", lineHeight: 1 }}>{cfg.icon}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, fontSize: "1rem", color: cfg.color }}>
                      {cfg.label}
                    </div>
                    <div style={{ fontSize: "0.8125rem", color: "var(--color-text-secondary)", marginTop: "0.125rem" }}>
                      {cfg.description}
                    </div>
                  </div>
                  <div style={{
                    fontSize: "1.25rem",
                    fontWeight: 700,
                    color: cfg.color,
                    minWidth: "3.5rem",
                    textAlign: "right",
                  }}>
                    {cfg.timeLimitSeconds / 60}:00
                  </div>
                </motion.button>
              </motion.div>
            ))}
          </motion.div>

          <div style={{ textAlign: "center" }}>
            <Link to="/modules" style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem" }}>
              ← Back to Modules
            </Link>
          </div>
        </div>
      </PageTransition>
    );
  }

  // ---------------------------------------------------------------------------
  // Loading state (after mode selected, before attempt arrives)
  // ---------------------------------------------------------------------------

  if (loading) {
    return (
      <div className="page container" style={{ textAlign: "center" }}>
        <p style={{ color: "var(--color-text-secondary)" }}>Assembling your quiz…</p>
      </div>
    );
  }

  if (error && !attempt) {
    return (
      <PageTransition>
        <div className="page container">
          <p style={{ color: "var(--color-danger)" }}>{error}</p>
          <GlassButton variant="secondary" onClick={() => { setPhase("select-mode"); setError(null); }}>
            ← Back
          </GlassButton>
        </div>
      </PageTransition>
    );
  }

  if (!attempt) return null;

  // ---------------------------------------------------------------------------
  // Phase: Results
  // ---------------------------------------------------------------------------

  if (phase === "submitted") {
    const pct = attempt.max_score
      ? Math.round(((attempt.score ?? 0) / attempt.max_score) * 100)
      : 0;
    const isPassing = pct >= 80;

    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 720 }}>
          <motion.div
            initial={scaleIn.initial}
            animate={scaleIn.animate}
            transition={scaleIn.transition}
          >
            <GlassCard blur="lg" style={{ textAlign: "center", marginBottom: "1.5rem" }}>
              <h1 style={{ color: "var(--color-text)", marginBottom: "var(--space-2)", fontFamily: "var(--font-display)" }}>Quiz Results</h1>
              {selectedMode && (
                <p style={{ color: "var(--color-text-secondary)", fontSize: "0.8125rem", marginBottom: "var(--space-3)" }}>
                  {MODES[selectedMode].icon} {MODES[selectedMode].label}
                </p>
              )}
              <p style={{
                fontSize: "2.75rem",
                fontWeight: 800,
                margin: "var(--space-1) 0",
              }}>
                <GradientText variant={isPassing ? "success" : "danger"}>
                  <AnimatedNumber value={attempt.score ?? 0} duration={1200} /> / {attempt.max_score}
                </GradientText>
              </p>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem" }}>
                <AnimatedNumber value={pct} suffix="%" duration={1000} /> — {isPassing ? "✓ Passing" : "✗ Below passing (80%)"}
              </p>
            </GlassCard>
          </motion.div>

          {/* Summary jump links */}
          <div style={{ marginBottom: "1.5rem" }}>
            <p style={{
              color: "var(--color-text-secondary)",
              fontSize: "0.75rem",
              fontWeight: 600,
              textTransform: "uppercase",
              letterSpacing: "0.05em",
              marginBottom: "0.5rem",
            }}>
              Jump to Question
            </p>
            <div style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "0.375rem",
            }}>
              {attempt.questions.map((q, i) => {
                const isCorrect = q.is_correct === true;
                return (
                  <a
                    key={q.id}
                    href={`#result-q-${i + 1}`}
                    aria-label={`Jump to question ${i + 1} — ${isCorrect ? "correct" : "incorrect"}`}
                    style={{
                      width: "2rem",
                      height: "2rem",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      borderRadius: "var(--radius-sm, 6px)",
                      fontSize: "0.75rem",
                      fontWeight: 600,
                      textDecoration: "none",
                      border: `1px solid ${isCorrect ? "var(--color-success)" : "var(--color-danger)"}44`,
                      background: isCorrect ? "var(--color-success)1a" : "var(--color-danger)1a",
                      color: isCorrect ? "var(--color-success)" : "var(--color-danger)",
                      transition: "all 150ms ease",
                    }}
                  >
                    {i + 1}
                  </a>
                );
              })}
            </div>
          </div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            style={{ display: "grid", gap: "1rem" }}
          >
            {attempt.questions.map((q, i) => (
              <motion.div key={q.id} id={`result-q-${i + 1}`} variants={staggerItem} transition={springDefault}>
                <GlassCard blur="sm" style={{
                  borderLeft: `3px solid ${q.is_correct ? "var(--color-success)" : "var(--color-danger)"}`,
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
                    <span style={{ color: "var(--color-text-muted)", fontSize: "0.8125rem" }}>
                      {i + 1}.
                    </span>
                    {q.difficulty && <DifficultyBadge difficulty={q.difficulty} />}
                  </div>
                  <p style={{ color: "var(--color-text)", marginBottom: "0.5rem" }}>
                    <strong><StemRenderer text={q.stem} /></strong>
                  </p>
                  <p style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem" }}>
                    Your answer:{" "}
                    <OptionDisplay value={q.selected_answer ?? "(no answer)"} isCorrect={q.is_correct} />
                    {q.is_correct !== undefined && (
                      <span style={{ marginLeft: "0.5rem" }}>
                        {q.is_correct ? "✓" : "✗"}
                      </span>
                    )}
                  </p>
                  {!q.is_correct && q.correct_answer && (
                    <p style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem" }}>
                      Correct:{" "}
                      <OptionDisplay value={q.correct_answer} isCorrect={true} />
                    </p>
                  )}
                  <InlineExplanation questionId={q.id} fallbackText={q.explanation} />
                </GlassCard>
              </motion.div>
            ))}
          </motion.div>

          <div style={{ display: "flex", gap: "0.75rem", marginTop: "1.5rem" }}>
            <GlassButton variant="secondary" onClick={() => { setPhase("select-mode"); setAttempt(null); setError(null); }}>
              Try Again
            </GlassButton>
            <Link to="/modules" style={{ textDecoration: "none" }}>
              <GlassButton variant="primary">Back to Modules</GlassButton>
            </Link>
          </div>
        </div>
      </PageTransition>
    );
  }

  // ---------------------------------------------------------------------------
  // Phase: In-progress
  // ---------------------------------------------------------------------------

  const question = attempt.questions[currentIdx];
  if (!question) return null;

  const totalQuestions = attempt.questions.length;
  const answeredCount = attempt.questions.filter((q) => q.selected_answer != null).length;
  const modeConfig = selectedMode ? MODES[selectedMode] : null;
  const timerExpired = remaining === 0;

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 720 }}>

        {/* Sticky header: progress + timer */}
        <div style={{
          position: "sticky",
          top: 0,
          zIndex: 10,
          background: "var(--color-background)",
          paddingTop: "var(--space-3)",
          paddingBottom: "var(--space-3)",
        }}>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "0.75rem",
          }}>
            <div>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "0.875rem", margin: 0 }}>
                Question {currentIdx + 1} of {totalQuestions}
              </p>
              <p style={{ color: "var(--color-text-muted)", fontSize: "0.75rem", margin: 0 }}>
                {answeredCount} of {totalQuestions} answered
              </p>
            </div>

            {/* Timer */}
            {remaining !== null && attempt.time_limit_seconds !== null && (
              <div style={{
                display: "flex",
                alignItems: "center",
                gap: "0.375rem",
                padding: "0.375rem 0.875rem",
                borderRadius: "var(--radius-full, 9999px)",
                background: timerExpired
                  ? "rgba(212, 100, 92, 0.15)"
                  : "var(--glass-bg-subtle)",
                border: timerExpired
                  ? "1.5px solid var(--color-danger)"
                  : `1.5px solid ${timerColor(remaining)}44`,
              }}>
                <span style={{ fontSize: "0.875rem" }}>⏱</span>
                <span
                  className={remaining < 30 && remaining > 0 && !reducedMotion ? "timer-pulse" : undefined}
                  style={{
                    fontWeight: 700,
                    fontSize: "1rem",
                    color: timerExpired ? "var(--color-danger)" : timerColor(remaining),
                    fontVariantNumeric: "tabular-nums",
                    letterSpacing: "0.05em",
                  }}
                >
                  {timerExpired ? "Time Expired" : formatTime(remaining)}
                </span>
                {modeConfig && !timerExpired && (
                  <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
                    {modeConfig.icon}
                  </span>
                )}
              </div>
            )}
          </div>

          {/* Progress bar */}
          <div style={{
            height: 4,
            borderRadius: 2,
            background: "var(--glass-bg-medium)",
            overflow: "hidden",
          }}>
            <div style={{
              height: "100%",
              width: `${((currentIdx + 1) / totalQuestions) * 100}%`,
              background: modeConfig ? modeConfig.color : "var(--color-accent)",
              borderRadius: 2,
              transition: `width var(--duration-normal, 250ms) ease`,
            }} />
          </div>
        </div>

        {/* Question card */}
        <GlassCard blur="md" style={{ marginBottom: "1.25rem", padding: "var(--space-6)" }}>
          {/* Difficulty badge */}
          {question.difficulty && (
            <div style={{ marginBottom: "0.75rem" }}>
              <DifficultyBadge difficulty={question.difficulty} />
            </div>
          )}
          <h2 style={{
            color: "var(--color-text)",
            margin: 0,
            fontSize: "1.125rem",
            fontWeight: 600,
            lineHeight: 1.5,
            fontFamily: "var(--font-display)",
          }}>
            <StemRenderer text={question.stem} />
          </h2>
        </GlassCard>

        {/* Multiple choice options */}
        {question.qtype === "MULTIPLE_CHOICE" && question.options && (
          <div style={{ display: "grid", gap: "0.625rem" }}>
            {question.options.map((opt) => {
              const isSelected = question.selected_answer === opt;
              const { label, hasSvg, svgContent } = parseOption(opt);
              return (
                <motion.button
                  key={opt}
                  onClick={() => handleSelectAnswer(question.id, opt)}
                  whileHover={reducedMotion ? undefined : { scale: 1.01 }}
                  whileTap={reducedMotion ? undefined : { scale: 1.02 }}
                  transition={{ duration: 0.08, ease: [0.4, 0, 0.2, 1] }}
                  aria-label={`Select option: ${label}`}
                  aria-pressed={isSelected}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "0.75rem",
                    width: "100%",
                    textAlign: "left",
                    cursor: "pointer",
                    minHeight: "56px",
                    padding: "var(--space-4) var(--space-5)",
                    borderRadius: "var(--radius-md)",
                    background: isSelected ? "var(--glass-bg-medium)" : "var(--glass-bg-subtle)",
                    border: isSelected
                      ? "1.5px solid var(--color-accent)"
                      : "1px solid var(--glass-border-medium)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                    fontFamily: "var(--font-family)",
                    boxShadow: isSelected
                      ? "0 0 0 3px rgba(212,165,116,0.2)"
                      : "none",
                    transition: "box-shadow var(--duration-instant, 80ms) ease, border-color var(--duration-instant, 80ms) ease, background var(--duration-instant, 80ms) ease",
                    minWidth: "44px",
                  }}
                >
                  {hasSvg ? (
                    <>
                      <span style={{ fontWeight: 600, minWidth: "1.25rem" }}>{label}</span>
                      <span dangerouslySetInnerHTML={{ __html: svgContent }} />
                    </>
                  ) : (
                    <span>{opt}</span>
                  )}
                </motion.button>
              );
            })}
          </div>
        )}

        {/* Identification input */}
        {question.qtype === "IDENTIFICATION" && (
          <div style={{ marginBottom: "1rem" }}>
            <label
              htmlFor="identification-answer"
              style={{
                display: "block",
                marginBottom: "0.375rem",
                fontSize: "var(--font-size-sm)",
                color: "var(--color-text-secondary)",
              }}
            >
              Your Answer
            </label>
            <input
              id="identification-answer"
              type="text"
              className="glass-input"
              value={question.selected_answer ?? ""}
              onChange={(e) => handleSelectAnswer(question.id, e.target.value)}
            />
          </div>
        )}

        {error && (
          <p style={{ color: "var(--color-danger)", marginTop: "0.5rem", fontSize: "0.875rem" }}>
            {error}
          </p>
        )}

        {/* Navigation */}
        <div style={{ display: "flex", gap: "0.5rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
          <GlassButton
            variant="secondary"
            onClick={() => setCurrentIdx((i) => Math.max(0, i - 1))}
            disabled={currentIdx === 0}
            aria-label="Previous question"
          >
            Previous
          </GlassButton>
          {currentIdx < totalQuestions - 1 && (
            <GlassButton
              variant="primary"
              onClick={() => setCurrentIdx((i) => i + 1)}
              aria-label="Next question"
            >
              Next
            </GlassButton>
          )}
          <GlassButton
            variant={currentIdx === totalQuestions - 1 ? "primary" : "danger"}
            onClick={handleSubmitQuiz}
            disabled={submitting}
            loading={submitting}
            aria-label="Submit quiz"
            style={{ marginLeft: "auto" }}
          >
            {submitting ? "Submitting…" : "Submit Quiz"}
          </GlassButton>
        </div>

        {/* Question jump links */}
        <div style={{ marginTop: "1.5rem" }}>
          <p style={{
            color: "var(--color-text-secondary)",
            fontSize: "0.75rem",
            fontWeight: 600,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            marginBottom: "0.5rem",
          }}>
            Jump to Question
          </p>
          <div style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "0.375rem",
          }}>
            {attempt.questions.map((q, i) => {
              const isActive = i === currentIdx;
              const isAnswered = q.selected_answer != null;
              return (
                <button
                  key={q.id}
                  onClick={() => setCurrentIdx(i)}
                  aria-label={`Go to question ${i + 1}${isAnswered ? " (answered)" : ""}`}
                  aria-current={isActive ? "step" : undefined}
                  style={{
                    width: "2rem",
                    height: "2rem",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    borderRadius: "var(--radius-sm, 6px)",
                    fontSize: "0.75rem",
                    fontWeight: 600,
                    fontFamily: "var(--font-family)",
                    cursor: "pointer",
                    border: isActive
                      ? `2px solid ${modeConfig ? modeConfig.color : "var(--color-accent)"}`
                      : "1px solid var(--glass-border-medium)",
                    background: isAnswered
                      ? isActive
                        ? `${modeConfig ? modeConfig.color : "var(--color-accent)"}33`
                        : "var(--glass-bg-medium)"
                      : "var(--glass-bg-subtle)",
                    color: isActive
                      ? (modeConfig ? modeConfig.color : "var(--color-accent)")
                      : isAnswered
                        ? "var(--color-text)"
                        : "var(--color-text-muted)",
                    transition: "all 150ms ease",
                  }}
                >
                  {i + 1}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
