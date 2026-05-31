import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient } from "../api/client";
import { GlassCard } from "../components/GlassCard";
import { GlassProgressBar } from "../components/GlassProgressBar";
import { GlassBadge } from "../components/GlassBadge";
import { GlassButton } from "../components/GlassButton";
import { GlassSkeleton } from "../components/GlassSkeleton";
import { GradientText } from "../components/GradientText";
import { EmptyState } from "../components/EmptyState";
import { PageTransition } from "../components/PageTransition";
import { staggerContainer, staggerItem, springDefault } from "../design-system";

interface SubtopicMastery {
  subtopic_id: number;
  subtopic_title: string;
  mastery_level: string;
  mastery_score: number;
  confidence_score: number;
  retention_score: number;
  total_attempts: number;
  correct_attempts: number;
  last_practiced_at: string | null;
}

interface ReviewDue {
  subtopic_id: number;
  subtopic_title: string;
  next_review_at: string;
  days_overdue: number;
  interval_days: number;
}

interface Recommendation {
  subtopic_id: number;
  subtopic_title: string;
  reason: string;
  priority: number;
  recommended_difficulty: string;
}

const LEVEL_COLORS: Record<string, string> = {
  BEGINNER: "var(--color-danger)",
  FAMILIAR: "var(--color-warning)",
  PROFICIENT: "var(--color-accent)",
  ADVANCED: "var(--color-success)",
  MASTERED: "var(--color-metallic)",
};

const LEVEL_BADGE_COLORS: Record<string, "danger" | "warning" | "accent" | "success" | "primary"> = {
  BEGINNER: "danger",
  FAMILIAR: "warning",
  PROFICIENT: "accent",
  ADVANCED: "success",
  MASTERED: "primary",
};

const REASON_LABELS: Record<string, string> = {
  weak_area: "Needs Practice",
  due_for_review: "Due for Review",
  next_in_sequence: "Next Up",
  challenge: "Challenge",
};

export function Mastery() {
  const [mastery, setMastery] = useState<SubtopicMastery[]>([]);
  const [dueReviews, setDueReviews] = useState<ReviewDue[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      apiClient.get<SubtopicMastery[]>("/v1/mastery/me"),
      apiClient.get<ReviewDue[]>("/v1/mastery/me/reviews/due"),
      apiClient.get<Recommendation[]>("/v1/mastery/me/recommendations"),
    ])
      .then(([m, r, rec]) => {
        setMastery(m);
        setDueReviews(r);
        setRecommendations(rec);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 800 }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            <GradientText variant="accent">Mastery Dashboard</GradientText>
          </h1>
          <div style={{ display: "grid", gap: "var(--space-4)" }}>
            <GlassSkeleton variant="card" />
            <GlassSkeleton variant="card" />
          </div>
        </div>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 800 }}>
          <p style={{ color: "var(--color-danger)" }}>{error}</p>
        </div>
      </PageTransition>
    );
  }

  // Count subtopics at each level.
  const levelCounts: Record<string, number> = {};
  for (const m of mastery) {
    levelCounts[m.mastery_level] = (levelCounts[m.mastery_level] || 0) + 1;
  }

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 800 }}>
        <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
          <GradientText variant="accent">Mastery Dashboard</GradientText>
        </h1>

        {/* Overall progress summary */}
        <GlassCard as="section" style={{ marginBottom: "var(--space-6)" }}>
          <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, color: "var(--color-text)", marginBottom: "var(--space-4)" }}>
            Overall Progress
          </h2>
          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap" }}
          >
            {["BEGINNER", "FAMILIAR", "PROFICIENT", "ADVANCED", "MASTERED"].map((level) => (
              <motion.div
                key={level}
                variants={staggerItem}
                transition={springDefault}
                style={{
                  padding: "var(--space-2) var(--space-4)",
                  borderRadius: "var(--radius-md)",
                  background: "var(--glass-bg-subtle)",
                  border: `1px solid ${LEVEL_COLORS[level]}33`,
                }}
              >
                <span style={{ fontWeight: 700, color: LEVEL_COLORS[level], fontSize: "var(--font-size-lg)", fontFamily: "var(--font-display)" }}>
                  {levelCounts[level] || 0}
                </span>{" "}
                <span style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>
                  {level.charAt(0) + level.slice(1).toLowerCase()}
                </span>
              </motion.div>
            ))}
          </motion.div>
        </GlassCard>

        {/* Due for Review */}
        {dueReviews.length > 0 && (
          <GlassCard as="section" style={{ marginBottom: "var(--space-6)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginBottom: "var(--space-4)" }}>
              <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, color: "var(--color-text)", margin: 0 }}>
                Due for Review
              </h2>
              <GlassBadge label={String(dueReviews.length)} color="danger" />
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {dueReviews.map((r) => (
                <li
                  key={r.subtopic_id}
                  style={{
                    padding: "var(--space-3) 0",
                    borderBottom: "1px solid var(--glass-border-light)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "var(--space-2)",
                  }}
                >
                  <span style={{ fontWeight: 500, color: "var(--color-text)" }}>{r.subtopic_title}</span>
                  <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-danger)", whiteSpace: "nowrap" }}>
                    {r.days_overdue != null ? `${r.days_overdue.toFixed(1)}d overdue` : "Overdue"}
                  </span>
                </li>
              ))}
            </ul>
          </GlassCard>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <GlassCard as="section" style={{ marginBottom: "var(--space-6)" }}>
            <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, color: "var(--color-text)", marginBottom: "var(--space-4)" }}>
              Recommended Next
            </h2>
            <motion.div
              variants={staggerContainer}
              initial="initial"
              animate="animate"
              style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}
            >
              {recommendations.map((rec) => (
                <motion.div
                  key={rec.subtopic_id}
                  variants={staggerItem}
                  transition={springDefault}
                  style={{
                    padding: "var(--space-3) var(--space-4)",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-light)",
                    borderRadius: "var(--radius-md)",
                    display: "flex",
                    alignItems: "center",
                    gap: "var(--space-3)",
                    flexWrap: "wrap",
                  }}
                >
                  <span style={{ fontWeight: 500, color: "var(--color-text)", flex: 1 }}>{rec.subtopic_title}</span>
                  <GlassBadge label={REASON_LABELS[rec.reason] || rec.reason} color="accent" />
                  <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)", letterSpacing: "0.04em", textTransform: "uppercase" }}>
                    {rec.recommended_difficulty}
                  </span>
                </motion.div>
              ))}
            </motion.div>
          </GlassCard>
        )}

        {/* Mastery per subtopic */}
        <GlassCard as="section">
          <h2 style={{ fontSize: "var(--font-size-lg)", fontWeight: 600, color: "var(--color-text)", marginBottom: "var(--space-4)" }}>
            Subtopic Mastery
          </h2>
          {mastery.length === 0 ? (
            <EmptyState
              icon="🎯"
              title="No Mastery Data Yet"
              description="Start practicing subtopics to track your mastery progress here."
            />
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-3)" }}>
              {mastery.map((m) => (
                <div key={m.subtopic_id}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-1)" }}>
                    <span style={{ color: "var(--color-text)", fontSize: "var(--font-size-sm)" }}>{m.subtopic_title}</span>
                    <GlassBadge label={m.mastery_level} color={LEVEL_BADGE_COLORS[m.mastery_level] || "primary"} />
                  </div>
                  <GlassProgressBar
                    value={m.mastery_score * 100}
                    label={`${m.subtopic_title} mastery: ${Math.round(m.mastery_score * 100)}%`}
                    color={LEVEL_COLORS[m.mastery_level]}
                    height={6}
                  />
                </div>
              ))}
            </div>
          )}
        </GlassCard>

        <div style={{ marginTop: "var(--space-6)" }}>
          <Link to="/modules" style={{ textDecoration: "none" }} aria-label="Back to modules">
            <GlassButton variant="ghost">← Back to Modules</GlassButton>
          </Link>
        </div>
      </div>
    </PageTransition>
  );
}
