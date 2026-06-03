import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GradientText } from "../../components/GradientText";
import { PageTransition } from "../../components/PageTransition";
import { useOnboarding } from "../../hooks/useOnboarding";
import type { OnboardingRequest } from "../../api/onboarding";

const EXAM_CATEGORIES = ["Professional", "Sub-Professional"] as const;
const TIME_BUDGETS = [15, 30, 60] as const;

export function Onboarding() {
  const navigate = useNavigate();
  const { submit, loading, error } = useOnboarding();

  const [examDate, setExamDate] = useState("");
  const [examCategory, setExamCategory] = useState<"Professional" | "Sub-Professional">("Professional");
  const [timeBudget, setTimeBudget] = useState<15 | 30 | 60>(30);
  const [warning, setWarning] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  function validateDate(dateStr: string): string | null {
    if (!dateStr) return "Please select an exam date";
    const selected = new Date(dateStr);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const diffDays = Math.floor((selected.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    if (diffDays < 1) return "Exam date must be in the future";
    if (diffDays > 365) return "Exam date must be within 365 days";
    return null;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const dateError = validateDate(examDate);
    if (dateError) {
      setValidationError(dateError);
      return;
    }
    setValidationError(null);

    const data: OnboardingRequest = {
      exam_date: examDate,
      exam_category: examCategory,
      time_budget_minutes: timeBudget,
    };

    const res = await submit(data);
    if (res) {
      if (res.warning) setWarning(res.warning);
      navigate("/");
    }
  }

  function handleSkip() {
    // Store skip flag so dashboard can show a persistent prompt
    localStorage.setItem("cse_onboarding_skipped", "true");
    navigate("/");
  }

  // Compute days until exam for warning display
  const daysUntilExam = examDate
    ? Math.floor((new Date(examDate).getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    : null;

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 520 }}>
        <div style={{ textAlign: "center", marginBottom: "var(--space-8)" }}>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              letterSpacing: "-0.02em",
              fontSize: "var(--font-size-3xl)",
              marginBottom: "var(--space-2)",
            }}
          >
            <GradientText variant="accent">Set Up Your Study Plan</GradientText>
          </h1>
          <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-base)" }}>
            Tell us about your exam so we can create a personalized study plan.
          </p>
        </div>

        <GlassCard>
          <form onSubmit={handleSubmit} style={{ display: "grid", gap: "var(--space-5)" }}>
            {/* Exam Date */}
            <div>
              <label
                htmlFor="exam-date"
                style={{
                  display: "block",
                  fontSize: "var(--font-size-sm)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  marginBottom: "var(--space-2)",
                }}
              >
                Exam Date
              </label>
              <input
                id="exam-date"
                type="date"
                value={examDate}
                onChange={(e) => {
                  setExamDate(e.target.value);
                  setValidationError(null);
                }}
                min={new Date(Date.now() + 86400000).toISOString().split("T")[0]}
                max={new Date(Date.now() + 365 * 86400000).toISOString().split("T")[0]}
                required
                aria-describedby="exam-date-hint"
                style={{
                  width: "100%",
                  padding: "var(--space-3)",
                  borderRadius: "var(--radius-md)",
                  border: "1px solid var(--glass-border-light)",
                  background: "var(--glass-bg-subtle)",
                  color: "var(--color-text)",
                  fontSize: "var(--font-size-base)",
                }}
              />
              <p
                id="exam-date-hint"
                style={{
                  fontSize: "var(--font-size-xs)",
                  color: "var(--color-text-muted)",
                  margin: "var(--space-1) 0 0",
                }}
              >
                Must be 1–365 days from today
              </p>
              {daysUntilExam !== null && daysUntilExam > 0 && daysUntilExam < 7 && (
                <p
                  role="alert"
                  style={{
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-warning)",
                    margin: "var(--space-2) 0 0",
                    fontWeight: 500,
                  }}
                >
                  ⚠️ Your exam is in {daysUntilExam} day{daysUntilExam !== 1 ? "s" : ""}. We'll create an intensive plan.
                </p>
              )}
            </div>

            {/* Exam Category */}
            <div>
              <label
                htmlFor="exam-category"
                style={{
                  display: "block",
                  fontSize: "var(--font-size-sm)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  marginBottom: "var(--space-2)",
                }}
              >
                Exam Category
              </label>
              <div style={{ display: "flex", gap: "var(--space-3)" }}>
                {EXAM_CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setExamCategory(cat)}
                    aria-pressed={examCategory === cat}
                    style={{
                      flex: 1,
                      padding: "var(--space-3)",
                      borderRadius: "var(--radius-md)",
                      border: `2px solid ${examCategory === cat ? "var(--color-accent)" : "var(--glass-border-light)"}`,
                      background: examCategory === cat ? "var(--color-accent-subtle)" : "var(--glass-bg-subtle)",
                      color: "var(--color-text)",
                      fontSize: "var(--font-size-sm)",
                      fontWeight: 500,
                      cursor: "pointer",
                      transition: "border-color 0.15s, background 0.15s",
                    }}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            {/* Time Budget */}
            <div>
              <label
                style={{
                  display: "block",
                  fontSize: "var(--font-size-sm)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  marginBottom: "var(--space-2)",
                }}
              >
                Daily Study Time
              </label>
              <div style={{ display: "flex", gap: "var(--space-3)" }}>
                {TIME_BUDGETS.map((mins) => (
                  <button
                    key={mins}
                    type="button"
                    onClick={() => setTimeBudget(mins)}
                    aria-pressed={timeBudget === mins}
                    style={{
                      flex: 1,
                      padding: "var(--space-3)",
                      borderRadius: "var(--radius-md)",
                      border: `2px solid ${timeBudget === mins ? "var(--color-accent)" : "var(--glass-border-light)"}`,
                      background: timeBudget === mins ? "var(--color-accent-subtle)" : "var(--glass-bg-subtle)",
                      color: "var(--color-text)",
                      fontSize: "var(--font-size-sm)",
                      fontWeight: 500,
                      cursor: "pointer",
                      transition: "border-color 0.15s, background 0.15s",
                    }}
                  >
                    {mins} min
                  </button>
                ))}
              </div>
            </div>

            {/* Error displays */}
            {(validationError || error) && (
              <p
                role="alert"
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-danger)",
                  margin: 0,
                  fontWeight: 500,
                }}
              >
                {validationError || error}
              </p>
            )}

            {warning && (
              <p
                role="status"
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-warning)",
                  margin: 0,
                }}
              >
                {warning}
              </p>
            )}

            {/* Actions */}
            <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end" }}>
              <GlassButton
                type="button"
                variant="ghost"
                size="md"
                onClick={handleSkip}
                disabled={loading}
              >
                Skip for now
              </GlassButton>
              <GlassButton
                type="submit"
                variant="primary"
                size="md"
                disabled={loading}
              >
                {loading ? "Creating plan..." : "Create My Plan"}
              </GlassButton>
            </div>
          </form>
        </GlassCard>
      </main>
    </PageTransition>
  );
}
