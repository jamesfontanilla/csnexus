import { useEffect, useState } from "react";
import {
  getStudyPreferences,
  setStudyPreference,
  type StudyPreferences,
} from "../../stores/preferences";

type QuizMode = StudyPreferences["defaultQuizMode"];

const QUIZ_MODES: { value: QuizMode; label: string }[] = [
  { value: "practice", label: "Practice" },
  { value: "exam", label: "Exam" },
  { value: "power", label: "Sprint" },
];

/**
 * Calculate the number of days remaining until `targetDate` from today.
 * Returns a non-negative integer (0 if the date is today).
 */
export function daysUntil(targetDate: string, today: Date = new Date()): number {
  const target = new Date(targetDate + "T00:00:00");
  const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const diff = target.getTime() - todayStart.getTime();
  return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
}

/** ISO date string for today (YYYY-MM-DD) in local time */
function todayISO(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

// --- Styles ---

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: "var(--font-size-sm)",
  fontWeight: 500,
  color: "var(--color-text-secondary)",
  marginBottom: "var(--space-2)",
};

const fieldGroupStyle: React.CSSProperties = {
  marginTop: "var(--space-5)",
};

const sliderStyle: React.CSSProperties = {
  width: "100%",
  accentColor: "var(--color-accent)",
  cursor: "pointer",
};

const modeButtonBaseStyle: React.CSSProperties = {
  flex: 1,
  padding: "var(--space-2) var(--space-3)",
  borderWidth: "1px",
  borderStyle: "solid",
  borderColor: "var(--glass-border-medium)",
  borderRadius: "var(--radius-sm)",
  background: "var(--glass-bg-subtle)",
  color: "var(--color-text-secondary)",
  fontSize: "var(--font-size-sm)",
  fontWeight: 500,
  cursor: "pointer",
  transition: "all 150ms ease",
};

const modeButtonActiveStyle: React.CSSProperties = {
  ...modeButtonBaseStyle,
  background: "var(--color-accent)",
  color: "var(--color-primary)",
  borderColor: "var(--color-accent)",
  fontWeight: 600,
};

const dateInputStyle: React.CSSProperties = {
  width: "100%",
  padding: "var(--space-2) var(--space-3)",
  background: "var(--glass-bg-subtle)",
  border: "1px solid var(--glass-border-medium)",
  borderRadius: "var(--radius-md)",
  color: "var(--color-text)",
  fontSize: "var(--font-size-sm)",
  fontFamily: "inherit",
  outline: "none",
};

const countdownStyle: React.CSSProperties = {
  marginTop: "var(--space-2)",
  fontSize: "var(--font-size-sm)",
  color: "var(--color-accent)",
  fontWeight: 500,
};

export function StudySection() {
  const [dailyGoal, setDailyGoal] = useState(30);
  const [quizMode, setQuizMode] = useState<QuizMode>("practice");
  const [examDate, setExamDate] = useState<string | null>(null);

  // Load stored values on mount
  useEffect(() => {
    const prefs = getStudyPreferences();
    setDailyGoal(prefs.dailyGoalMinutes);
    setQuizMode(prefs.defaultQuizMode);
    setExamDate(prefs.examDate);
  }, []);

  function handleGoalChange(value: number) {
    setDailyGoal(value);
    setStudyPreference("dailyGoalMinutes", value);
  }

  function handleModeChange(mode: QuizMode) {
    setQuizMode(mode);
    setStudyPreference("defaultQuizMode", mode);
  }

  function handleDateChange(value: string) {
    const date = value || null;
    setExamDate(date);
    setStudyPreference("examDate", date);
  }

  return (
    <div>
      {/* Daily goal slider */}
      <div>
        <label htmlFor="daily-goal-slider" style={labelStyle}>
          Daily Study Goal
        </label>
        <input
          id="daily-goal-slider"
          type="range"
          min={5}
          max={180}
          step={5}
          value={dailyGoal}
          onChange={(e) => handleGoalChange(Number(e.target.value))}
          style={sliderStyle}
          aria-valuenow={dailyGoal}
          aria-valuemin={5}
          aria-valuemax={180}
          aria-label="Daily study goal in minutes"
        />
        <p
          style={{
            margin: "var(--space-1) 0 0",
            fontSize: "var(--font-size-sm)",
            color: "var(--color-text)",
            fontWeight: 600,
          }}
        >
          {dailyGoal} minutes
        </p>
      </div>

      {/* Quiz mode selector */}
      <div style={fieldGroupStyle}>
        <span style={labelStyle}>Default Quiz Mode</span>
        <div
          style={{ display: "flex", gap: "var(--space-2)" }}
          role="radiogroup"
          aria-label="Default quiz mode"
        >
          {QUIZ_MODES.map((mode) => (
            <button
              key={mode.value}
              type="button"
              role="radio"
              aria-checked={quizMode === mode.value}
              onClick={() => handleModeChange(mode.value)}
              style={quizMode === mode.value ? modeButtonActiveStyle : modeButtonBaseStyle}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      {/* Exam date picker */}
      <div style={fieldGroupStyle}>
        <label htmlFor="exam-date-picker" style={labelStyle}>
          Target Exam Date
        </label>
        <input
          id="exam-date-picker"
          type="date"
          min={todayISO()}
          value={examDate ?? ""}
          onChange={(e) => handleDateChange(e.target.value)}
          style={dateInputStyle}
          aria-label="Target exam date"
        />
        {examDate && (
          <p style={countdownStyle} aria-live="polite">
            {daysUntil(examDate) === 0
              ? "Exam day is today!"
              : `${daysUntil(examDate)} day${daysUntil(examDate) === 1 ? "" : "s"} remaining`}
          </p>
        )}
      </div>
    </div>
  );
}
