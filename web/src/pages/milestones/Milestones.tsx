import { GlassCard } from "../../components/GlassCard";
import { GlassBadge } from "../../components/GlassBadge";
import { GlassProgressBar } from "../../components/GlassProgressBar";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { GradientText } from "../../components/GradientText";
import { EmptyState } from "../../components/EmptyState";
import { PageTransition } from "../../components/PageTransition";
import { useMilestones } from "../../hooks/useMilestones";
import type { MilestoneStatus } from "../../api/milestones";

const CATEGORY_EMOJIS: Record<string, string> = {
  mastery: "🏆",
  readiness: "🎯",
  recovery: "💪",
  subtest: "📋",
};

const CATEGORY_LABELS: Record<string, string> = {
  mastery: "Subject Mastery",
  readiness: "Exam Readiness",
  recovery: "Comeback & Resilience",
  subtest: "Subtest Progress",
};

export function Milestones() {
  const { milestones, consistency, loading, error } = useMilestones();

  if (loading) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            <GradientText variant="accent">Milestones</GradientText>
          </h1>
          <div style={{ display: "grid", gap: "var(--space-4)" }}>
            {[1, 2, 3, 4].map((i) => <GlassSkeleton key={i} variant="card" />)}
          </div>
        </main>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <EmptyState icon="⚠️" title="Could Not Load Milestones" description={error} />
        </main>
      </PageTransition>
    );
  }

  // Group milestones by category
  const grouped: Record<string, MilestoneStatus[]> = {};
  for (const m of milestones?.milestones ?? []) {
    if (!grouped[m.category]) grouped[m.category] = [];
    grouped[m.category].push(m);
  }

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 720 }}>
        <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
          <GradientText variant="accent">Milestones</GradientText>
        </h1>

        {/* Study consistency widget */}
        {consistency && (
          <GlassCard style={{ marginBottom: "var(--space-6)" }}>
            <h2 style={{ fontSize: "var(--font-size-base)", fontWeight: 600, marginBottom: "var(--space-3)", color: "var(--color-text)" }}>
              📅 Study Consistency
            </h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "var(--space-4)", textAlign: "center" }}>
              <div>
                <p style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, fontFamily: "var(--font-display)", color: "var(--color-accent)" }}>
                  {consistency.current_streak}
                </p>
                <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Current Streak</p>
              </div>
              <div>
                <p style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, fontFamily: "var(--font-display)", color: "var(--color-text)" }}>
                  {consistency.longest_streak}
                </p>
                <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Longest Streak</p>
              </div>
              <div>
                <p style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, fontFamily: "var(--font-display)", color: "var(--color-text)" }}>
                  {consistency.total_consistent_days}
                </p>
                <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>Total Days</p>
              </div>
            </div>
          </GlassCard>
        )}

        {/* Milestones grouped by category */}
        {Object.entries(grouped).map(([category, items]) => (
          <section key={category} style={{ marginBottom: "var(--space-6)" }} aria-labelledby={`milestone-cat-${category}`}>
            <h2
              id={`milestone-cat-${category}`}
              style={{
                fontSize: "var(--font-size-lg)",
                fontWeight: 600,
                color: "var(--color-text)",
                marginBottom: "var(--space-3)",
              }}
            >
              {CATEGORY_EMOJIS[category] || "🏅"} {CATEGORY_LABELS[category] || category}
            </h2>
            <div style={{ display: "grid", gap: "var(--space-3)" }}>
              {items.map((milestone) => (
                <MilestoneCard key={milestone.id} milestone={milestone} />
              ))}
            </div>
          </section>
        ))}

        {(!milestones || milestones.milestones.length === 0) && (
          <EmptyState icon="🏅" title="No Milestones Yet" description="Milestones will appear as you progress." />
        )}
      </main>
    </PageTransition>
  );
}

function MilestoneCard({ milestone }: { milestone: MilestoneStatus }) {
  const isEarned = milestone.status === "earned";
  const isLocked = milestone.status === "locked";

  return (
    <GlassCard
      style={{
        opacity: isLocked ? 0.5 : 1,
        display: "flex",
        alignItems: "center",
        gap: "var(--space-3)",
      }}
    >
      <div
        style={{
          width: 40,
          height: 40,
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1.2rem",
          background: isEarned
            ? "var(--color-success-subtle, rgba(100,255,100,0.1))"
            : "var(--glass-bg-subtle)",
          border: `2px solid ${isEarned ? "var(--color-success)" : "var(--glass-border-light)"}`,
          filter: isLocked ? "grayscale(1)" : "none",
        }}
      >
        {isEarned ? "✨" : isLocked ? "🔒" : "⏳"}
      </div>
      <div style={{ flex: 1 }}>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", fontWeight: 600, color: "var(--color-text)" }}>
          {milestone.name}
        </p>
        <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          {milestone.description}
        </p>
        {milestone.status === "in_progress" && (
          <div style={{ marginTop: "var(--space-2)" }}>
            <GlassProgressBar value={milestone.progress_percentage} max={100} />
          </div>
        )}
      </div>
      <div>
        {isEarned && milestone.awarded_at && (
          <GlassBadge label="Earned" color="success" size="sm" />
        )}
        {milestone.status === "in_progress" && (
          <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
            {milestone.progress_percentage.toFixed(0)}%
          </span>
        )}
        {milestone.xp_reward > 0 && (
          <p style={{ margin: "var(--space-1) 0 0", fontSize: "var(--font-size-xs)", color: "var(--color-accent)", textAlign: "right" }}>
            +{milestone.xp_reward} XP
          </p>
        )}
      </div>
    </GlassCard>
  );
}
