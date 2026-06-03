import { useParams, Link } from "react-router-dom";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassBadge } from "../../components/GlassBadge";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { GradientText } from "../../components/GradientText";
import { AnimatedNumber } from "../../components/AnimatedNumber";
import { EmptyState } from "../../components/EmptyState";
import { PageTransition } from "../../components/PageTransition";
import { useMockAnalytics } from "../../hooks/useMockAnalytics";
import type { SubtopicBreakdown, Recommendation } from "../../api/mockAnalytics";

export function MockExamResults() {
  const { attemptId } = useParams<{ attemptId: string }>();
  const numericAttemptId = attemptId ? parseInt(attemptId, 10) : null;

  const {
    diagnostic,
    recommendations,
    prediction,
    loading,
    error,
    acceptRecommendation,
  } = useMockAnalytics(numericAttemptId);

  if (loading) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            <GradientText variant="accent">Mock Exam Results</GradientText>
          </h1>
          <GlassSkeleton variant="card" />
          <div style={{ display: "grid", gap: "var(--space-4)", marginTop: "var(--space-4)" }}>
            {[1, 2, 3].map((i) => <GlassSkeleton key={i} variant="card" />)}
          </div>
        </main>
      </PageTransition>
    );
  }

  if (error || !diagnostic) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <EmptyState
            icon="📊"
            title="Results Unavailable"
            description={error || "Could not load diagnostic report for this attempt."}
          />
        </main>
      </PageTransition>
    );
  }

  const passed = diagnostic.total_score >= 80;

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 720 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginBottom: "var(--space-6)" }}>
          <Link to="/mock-exam" style={{ textDecoration: "none" }}>
            <GlassButton variant="ghost" size="sm">←</GlassButton>
          </Link>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", margin: 0 }}>
            <GradientText variant="accent">Mock Exam Results</GradientText>
          </h1>
        </div>

        {/* Score header */}
        <GlassCard style={{ textAlign: "center", marginBottom: "var(--space-5)" }}>
          <div style={{ marginBottom: "var(--space-3)" }}>
            <span style={{ fontSize: "var(--font-size-4xl)", fontWeight: 800, fontFamily: "var(--font-display)" }}>
              <GradientText variant={passed ? "success" : "danger"}>
                <AnimatedNumber value={parseFloat(diagnostic.total_score.toFixed(1))} suffix="%" duration={1200} />
              </GradientText>
            </span>
          </div>
          <GlassBadge
            label={passed ? "PASSED" : "NEEDS IMPROVEMENT"}
            color={passed ? "success" : "danger"}
            size="md"
          />
        </GlassCard>

        {/* Predicted score range */}
        {prediction && prediction.midpoint !== null && (
          <GlassCard style={{ marginBottom: "var(--space-5)" }}>
            <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
              📈 Predicted Score Range
            </h2>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "var(--space-4)" }}>
              <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                {prediction.lower_bound?.toFixed(1)}%
              </span>
              <span style={{ fontSize: "var(--font-size-xl)", fontWeight: 700, color: "var(--color-text)" }}>
                {prediction.midpoint?.toFixed(1)}%
              </span>
              <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                {prediction.upper_bound?.toFixed(1)}%
              </span>
            </div>
            {prediction.confidence_level && (
              <p style={{ textAlign: "center", fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", marginTop: "var(--space-2)" }}>
                Confidence: {prediction.confidence_level}
              </p>
            )}
          </GlassCard>
        )}
        {prediction && prediction.midpoint === null && prediction.message && (
          <GlassCard style={{ marginBottom: "var(--space-5)" }}>
            <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", textAlign: "center", margin: 0 }}>
              {prediction.message}
            </p>
          </GlassCard>
        )}

        {/* Highest impact areas */}
        {diagnostic.highest_impact_areas.length > 0 && (
          <GlassCard style={{ marginBottom: "var(--space-5)" }}>
            <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
              🎯 Highest Impact Areas
            </h2>
            <div style={{ display: "grid", gap: "var(--space-2)" }}>
              {diagnostic.highest_impact_areas.map((area) => (
                <BreakdownRow key={area.subtopic_id} item={area} highlight />
              ))}
            </div>
          </GlassCard>
        )}

        {/* Regression alerts */}
        {diagnostic.regression_alerts.length > 0 && (
          <GlassCard style={{ marginBottom: "var(--space-5)", borderLeft: "3px solid var(--color-warning)" }}>
            <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-warning)" }}>
              ⚠️ Regression Alerts
            </h2>
            {diagnostic.regression_alerts.map((alert) => (
              <p key={alert.subtopic_id} style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", margin: "var(--space-1) 0" }}>
                Subtopic #{alert.subtopic_id} declined by {alert.decline_percentage_points.toFixed(1)} percentage points
              </p>
            ))}
          </GlassCard>
        )}

        {/* Difficulty performance */}
        <GlassCard style={{ marginBottom: "var(--space-5)" }}>
          <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
            📊 Performance by Difficulty
          </h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "var(--space-3)", textAlign: "center" }}>
            <DifficultyCell label="Easy" value={diagnostic.difficulty_performance.easy} />
            <DifficultyCell label="Medium" value={diagnostic.difficulty_performance.medium} />
            <DifficultyCell label="Hard" value={diagnostic.difficulty_performance.hard} />
          </div>
        </GlassCard>

        {/* Subtopic breakdown table */}
        <GlassCard style={{ marginBottom: "var(--space-5)" }}>
          <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
            📋 Full Breakdown
          </h2>
          <div style={{ display: "grid", gap: "var(--space-2)" }}>
            {diagnostic.subtopic_breakdowns.map((item) => (
              <BreakdownRow key={item.subtopic_id} item={item} />
            ))}
          </div>
        </GlassCard>

        {/* Recommendations */}
        {recommendations && recommendations.recommendations.length > 0 && (
          <GlassCard>
            <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
              💡 Recommendations
            </h2>
            <div style={{ display: "grid", gap: "var(--space-3)" }}>
              {recommendations.recommendations.map((rec) => (
                <RecommendationCard
                  key={rec.id}
                  recommendation={rec}
                  onAccept={acceptRecommendation}
                />
              ))}
            </div>
          </GlassCard>
        )}
      </main>
    </PageTransition>
  );
}

function BreakdownRow({ item, highlight }: { item: SubtopicBreakdown; highlight?: boolean }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "var(--space-2)",
        borderRadius: "var(--radius-sm)",
        background: highlight ? "var(--color-danger-subtle, rgba(255,100,100,0.05))" : "transparent",
      }}
    >
      <div style={{ flex: 1 }}>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", fontWeight: 500, color: "var(--color-text)" }}>
          {item.subtopic_name || `Subtopic #${item.subtopic_id}`}
        </p>
        <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          {item.questions_correct}/{item.questions_attempted} correct
        </p>
      </div>
      <div style={{ textAlign: "right" }}>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", fontWeight: 600, color: item.accuracy_percentage >= 80 ? "var(--color-success)" : "var(--color-danger)" }}>
          {item.accuracy_percentage.toFixed(0)}%
        </p>
        {item.points_lost > 0 && (
          <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
            -{item.points_lost} pts
          </p>
        )}
      </div>
    </div>
  );
}

function DifficultyCell({ label, value }: { label: string; value: number | null }) {
  return (
    <div>
      <p style={{ margin: 0, fontSize: "var(--font-size-lg)", fontWeight: 700, color: "var(--color-text)" }}>
        {value !== null ? `${value.toFixed(0)}%` : "—"}
      </p>
      <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
        {label}
      </p>
    </div>
  );
}

function RecommendationCard({ recommendation, onAccept }: { recommendation: Recommendation; onAccept: () => void }) {
  const isAccepted = recommendation.accepted_at !== null;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "var(--space-3)",
        borderRadius: "var(--radius-md)",
        border: "1px solid var(--glass-border-light)",
      }}
    >
      <div style={{ flex: 1 }}>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", fontWeight: 500, color: "var(--color-text)" }}>
          {recommendation.formatted_string}
        </p>
        <p style={{ margin: "var(--space-1) 0 0", fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          {recommendation.current_accuracy.toFixed(0)}% → {recommendation.target_accuracy.toFixed(0)}% | Action: {recommendation.recommended_action}
        </p>
      </div>
      {isAccepted ? (
        <GlassBadge label="Added" color="success" size="sm" />
      ) : (
        <GlassButton variant="ghost" size="sm" onClick={onAccept}>
          + Queue
        </GlassButton>
      )}
    </div>
  );
}
