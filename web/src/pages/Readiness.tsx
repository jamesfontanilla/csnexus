import { useState, useEffect } from "react";
import { apiClient } from "../api/client";
import { GlassCard } from "../components/GlassCard";
import { GlassBadge } from "../components/GlassBadge";
import { GlassSkeleton } from "../components/GlassSkeleton";
import { AnimatedNumber } from "../components/AnimatedNumber";
import { GradientText } from "../components/GradientText";
import { EmptyState } from "../components/EmptyState";
import { PageTransition } from "../components/PageTransition";

interface ReadinessData {
  passing_probability: number;
  predicted_score: number;
  readiness_percentage: number;
  recommended_hours_remaining: number;
  strengths: string[];
  weaknesses: string[];
  confidence_level: string;
}

const CONFIDENCE_COLORS: Record<string, string> = {
  low: "var(--color-danger)",
  moderate: "var(--color-warning)",
  high: "var(--color-success)",
  very_high: "var(--color-info)",
};

const CONFIDENCE_BADGE_COLORS: Record<string, "danger" | "warning" | "success" | "accent"> = {
  low: "danger",
  moderate: "warning",
  high: "success",
  very_high: "accent",
};

export function Readiness() {
  const [data, setData] = useState<ReadinessData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.get<ReadinessData>("/v1/planner/readiness/me")
      .then(setData)
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            <GradientText variant="accent">Exam Readiness</GradientText>
          </h1>
          <GlassCard style={{ display: "flex", justifyContent: "center", marginBottom: "var(--space-6)" }}>
            <GlassSkeleton width="160px" height="160px" borderRadius="50%" />
          </GlassCard>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "var(--space-4)" }}>
            {[1, 2, 3, 4].map((i) => (
              <GlassSkeleton key={i} variant="card" />
            ))}
          </div>
        </main>
      </PageTransition>
    );
  }

  if (!data) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 720 }}>
          <EmptyState
            icon="📊"
            title="No Readiness Data"
            description="Complete some quizzes and lessons to generate your readiness report."
          />
        </main>
      </PageTransition>
    );
  }

  const confidenceColor = CONFIDENCE_COLORS[data.confidence_level] || "var(--color-text-muted)";

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 720 }}>
        <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
          <GradientText variant="accent">Exam Readiness</GradientText>
        </h1>

        {/* Big readiness circle */}
        <GlassCard style={{ display: "flex", justifyContent: "center", marginBottom: "var(--space-6)", padding: "var(--space-8)" }}>
          <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center", gap: "var(--space-4)" }}>
            {/* Outer glow ring */}
            <div style={{
              width: 200,
              height: 200,
              borderRadius: "50%",
              border: `3px solid ${confidenceColor}22`,
              position: "absolute",
              top: -10,
              left: -10,
            }} />
            <div style={{
              width: 160,
              height: 160,
              borderRadius: "50%",
              border: `6px solid ${confidenceColor}`,
              boxShadow: `0 0 32px ${confidenceColor}44, inset 0 0 24px ${confidenceColor}11`,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              background: "var(--glass-bg-subtle)",
            }}>
              <span style={{ fontSize: "var(--font-size-3xl)", fontWeight: 800, fontFamily: "var(--font-display)", lineHeight: 1 }}>
                <GradientText variant={data.readiness_percentage >= 80 ? "success" : data.readiness_percentage >= 50 ? "accent" : "danger"}>
                  <AnimatedNumber value={data.readiness_percentage} suffix="%" duration={1400} />
                </GradientText>
              </span>
              <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", letterSpacing: "0.06em", textTransform: "uppercase", marginTop: "var(--space-1)" }}>Ready</span>
            </div>
            <GlassBadge
              label={data.confidence_level.replace("_", " ")}
              color={CONFIDENCE_BADGE_COLORS[data.confidence_level] || "primary"}
              size="md"
            />
          </div>
        </GlassCard>

        {/* Stats grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: "var(--space-4)", marginBottom: "var(--space-6)" }}>
          <GlassCard style={{ textAlign: "center" }}>
            <p style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, margin: "0 0 var(--space-1)", fontFamily: "var(--font-display)" }}>
              <GradientText variant="success">
                <AnimatedNumber value={parseFloat((data.passing_probability * 100).toFixed(1))} suffix="%" duration={1200} />
              </GradientText>
            </p>
            <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", margin: 0, letterSpacing: "0.03em" }}>Passing Probability</p>
          </GlassCard>
          <GlassCard style={{ textAlign: "center" }}>
            <p style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, margin: "0 0 var(--space-1)", fontFamily: "var(--font-display)" }}>
              <GradientText variant="accent">
                <AnimatedNumber value={parseFloat((data.predicted_score * 100).toFixed(1))} suffix="%" duration={1200} />
              </GradientText>
            </p>
            <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", margin: 0, letterSpacing: "0.03em" }}>Predicted Score</p>
          </GlassCard>
          <GlassCard style={{ textAlign: "center" }}>
            <p style={{ fontSize: "var(--font-size-2xl)", fontWeight: 700, margin: "0 0 var(--space-1)", fontFamily: "var(--font-display)" }}>
              <GradientText variant="info">
                <AnimatedNumber value={data.recommended_hours_remaining} suffix="h" duration={1000} />
              </GradientText>
            </p>
            <p style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)", margin: 0, letterSpacing: "0.03em" }}>Recommended Hours</p>
          </GlassCard>
        </div>

        {/* Strengths and Weaknesses */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <GlassCard as="section">
            <h3 style={{ fontSize: "var(--font-size-sm)", fontWeight: 600, color: "var(--color-success)", marginBottom: "var(--space-3)", letterSpacing: "0.02em" }}>
              💪 Strengths
            </h3>
            {data.strengths.length === 0 ? (
              <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                Keep studying to build strengths!
              </p>
            ) : (
              <ul style={{ paddingLeft: "var(--space-4)", fontSize: "var(--font-size-sm)", color: "var(--color-text)", margin: 0 }}>
                {data.strengths.map((s, i) => <li key={i} style={{ marginBottom: "var(--space-1)" }}>{s}</li>)}
              </ul>
            )}
          </GlassCard>
          <GlassCard as="section">
            <h3 style={{ fontSize: "var(--font-size-sm)", fontWeight: 600, color: "var(--color-danger)", marginBottom: "var(--space-3)", letterSpacing: "0.02em" }}>
              ⚠️ Needs Work
            </h3>
            {data.weaknesses.length === 0 ? (
              <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                No weak areas detected!
              </p>
            ) : (
              <ul style={{ paddingLeft: "var(--space-4)", fontSize: "var(--font-size-sm)", color: "var(--color-text)", margin: 0 }}>
                {data.weaknesses.map((w, i) => <li key={i} style={{ marginBottom: "var(--space-1)" }}>{w}</li>)}
              </ul>
            )}
          </GlassCard>
        </div>
      </main>
    </PageTransition>
  );
}
