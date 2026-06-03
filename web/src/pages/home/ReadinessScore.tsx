import { Link } from "react-router-dom";
import { GlassCard } from "../../components/GlassCard";
import { GlassBadge } from "../../components/GlassBadge";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { AnimatedNumber } from "../../components/AnimatedNumber";
import { GradientText } from "../../components/GradientText";
import { useReadiness } from "../../hooks/useReadiness";
import type { DashboardResponse, TopImpactSubtopic } from "../../api/readiness";

const READINESS_LEVEL_COLORS: Record<string, string> = {
  "Not Ready": "var(--color-danger)",
  "Getting There": "var(--color-warning)",
  "Almost Ready": "var(--color-info)",
  "Exam Ready": "var(--color-success)",
};

const READINESS_LEVEL_BADGE: Record<string, "danger" | "warning" | "accent" | "success"> = {
  "Not Ready": "danger",
  "Getting There": "warning",
  "Almost Ready": "accent",
  "Exam Ready": "success",
};

/**
 * Primary readiness score widget for the dashboard.
 * Shows circular progress, readiness level, component breakdown, and delta.
 */
export function ReadinessScoreWidget() {
  const { dashboard, loading } = useReadiness();

  if (loading) {
    return (
      <GlassCard style={{ display: "flex", justifyContent: "center", padding: "var(--space-8)" }}>
        <GlassSkeleton width="160px" height="160px" borderRadius="50%" />
      </GlassCard>
    );
  }

  if (!dashboard) {
    return (
      <GlassCard style={{ textAlign: "center", padding: "var(--space-6)" }}>
        <p style={{ color: "var(--color-text-secondary)", margin: 0, fontSize: "var(--font-size-sm)" }}>
          Complete some activities to see your readiness score.
        </p>
        <Link
          to="/modules"
          style={{ color: "var(--color-accent)", fontSize: "var(--font-size-sm)", marginTop: "var(--space-2)", display: "inline-block" }}
        >
          Start studying →
        </Link>
      </GlassCard>
    );
  }

  return (
    <GlassCard style={{ padding: "var(--space-6)" }}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "var(--space-4)" }}>
        {/* Large circular score */}
        <ScoreCircle score={dashboard.score} level={dashboard.readiness_level} />

        {/* Delta badge */}
        {dashboard.delta !== null && dashboard.delta !== 0 && (
          <DeltaBadge delta={dashboard.delta} />
        )}

        {/* Stale data indicator */}
        {dashboard.stale_data && (
          <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-warning)", margin: 0 }}>
            ⚠️ Showing cached score — latest computation unavailable
          </p>
        )}

        {/* Component breakdown */}
        <ComponentBreakdown dashboard={dashboard} />

        {/* Score change summary */}
        {dashboard.score_change_summary && Math.abs(dashboard.score_change_summary.overall_delta) >= 5 && (
          <ScoreChangeBanner summary={dashboard.score_change_summary} />
        )}
      </div>
    </GlassCard>
  );
}

/**
 * Displays the top 3 subtopics with highest point impact.
 */
export function TopImpactWidget() {
  const { dashboard, loading } = useReadiness();

  if (loading || !dashboard || dashboard.top_impact_subtopics.length === 0) {
    return null;
  }

  return (
    <GlassCard>
      <h3 style={{ fontSize: "var(--font-size-sm)", fontWeight: 600, color: "var(--color-text)", marginBottom: "var(--space-3)" }}>
        🎯 Focus Areas (Most Impact)
      </h3>
      <div style={{ display: "grid", gap: "var(--space-2)" }}>
        {dashboard.top_impact_subtopics.map((item) => (
          <ImpactRow key={item.subtopic_id} item={item} />
        ))}
      </div>
    </GlassCard>
  );
}

// ─── Internal Components ────────────────────────────────────────────────────

function ScoreCircle({ score, level }: { score: number; level: string }) {
  const color = READINESS_LEVEL_COLORS[level] || "var(--color-accent)";

  return (
    <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div
        style={{
          width: 160,
          height: 160,
          borderRadius: "50%",
          border: `6px solid ${color}`,
          boxShadow: `0 0 32px ${color}44, inset 0 0 24px ${color}11`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "var(--glass-bg-subtle)",
        }}
      >
        <span style={{ fontSize: "var(--font-size-3xl)", fontWeight: 800, fontFamily: "var(--font-display)", lineHeight: 1 }}>
          <GradientText variant={score >= 80 ? "success" : score >= 50 ? "accent" : "danger"}>
            <AnimatedNumber value={score} duration={1200} />
          </GradientText>
        </span>
        <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", marginTop: "var(--space-1)", textTransform: "uppercase", letterSpacing: "0.06em" }}>
          Readiness
        </span>
      </div>
      <div style={{ marginTop: "var(--space-3)" }}>
        <GlassBadge label={level} color={READINESS_LEVEL_BADGE[level] || "primary"} size="md" />
      </div>
    </div>
  );
}

function DeltaBadge({ delta }: { delta: number }) {
  const positive = delta > 0;
  return (
    <span
      style={{
        fontSize: "var(--font-size-sm)",
        fontWeight: 600,
        color: positive ? "var(--color-success)" : "var(--color-danger)",
        padding: "var(--space-1) var(--space-2)",
        borderRadius: "var(--radius-full)",
        background: positive ? "rgba(100,255,100,0.08)" : "rgba(255,100,100,0.08)",
      }}
    >
      {positive ? "+" : ""}{delta} vs 7 days ago
    </span>
  );
}

function ComponentBreakdown({ dashboard }: { dashboard: DashboardResponse }) {
  const components = [
    { label: "Mastery", value: dashboard.components.mastery_component, color: "var(--color-accent)" },
    { label: "Retention", value: dashboard.components.retention_component, color: "var(--color-info)" },
    { label: "Mock Exams", value: dashboard.components.mock_component, color: "var(--color-success)" },
    { label: "Coverage", value: dashboard.components.coverage_component, color: "var(--color-warning)" },
  ];

  return (
    <div style={{ width: "100%", display: "grid", gap: "var(--space-3)" }}>
      {components.map(({ label, value, color }) => (
        <div key={label} style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
          <span style={{ width: 70, fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)" }}>
            {label}
          </span>
          <div style={{ flex: 1, height: 6, borderRadius: 3, background: "var(--glass-bg-subtle)", overflow: "hidden" }}>
            <div
              style={{
                width: `${Math.min(value, 100)}%`,
                height: "100%",
                borderRadius: 3,
                background: color,
                transition: "width 0.6s ease",
              }}
            />
          </div>
          <span style={{ width: 32, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", textAlign: "right" }}>
            {value.toFixed(0)}
          </span>
        </div>
      ))}
    </div>
  );
}

function ScoreChangeBanner({ summary }: { summary: NonNullable<DashboardResponse["score_change_summary"]> }) {
  const direction = summary.component_direction === "up" ? "📈" : "📉";
  return (
    <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", margin: 0, textAlign: "center" }}>
      {direction} Your {summary.primary_component} went {summary.component_direction} by {summary.component_magnitude.toFixed(1)} points
    </p>
  );
}

function ImpactRow({ item }: { item: TopImpactSubtopic }) {
  return (
    <Link
      to={`/subtopics/${item.subtopic_id}/lesson`}
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "var(--space-2)",
        borderRadius: "var(--radius-sm)",
        textDecoration: "none",
        color: "inherit",
      }}
    >
      <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)" }}>
        {item.subtopic_name}
      </span>
      <span style={{ fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-success)" }}>
        +{item.point_impact.toFixed(1)} pts
      </span>
    </Link>
  );
}
