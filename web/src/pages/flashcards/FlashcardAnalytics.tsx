import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  flashcardsApi,
  AnalyticsDashboard,
  HeatmapEntry,
  Recommendation,
} from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";
import { useMediaQuery } from "../../hooks/useMediaQuery";

export function FlashcardAnalytics() {
  const navigate = useNavigate();
  const isMobile = useMediaQuery("(max-width: 639px)");
  const [dashboard, setDashboard] = useState<AnalyticsDashboard | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [heatmap, setHeatmap] = useState<HeatmapEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [dashRes, recsRes] = await Promise.all([
          flashcardsApi.getDashboard(),
          flashcardsApi.getRecommendations(),
        ]);
        setDashboard(dashRes);
        setRecommendations(recsRes);
        try {
          const heatRes = await flashcardsApi.getHeatmap();
          setHeatmap(heatRes);
        } catch { /* non-critical */ }
      } catch (err) {
        setError("Failed to load analytics. Please try again.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <PageTransition>
        <main className="page container">
          <h1
            style={{
              fontSize: "var(--font-size-2xl)",
              color: "var(--color-text)",
              marginBottom: "1.5rem",
            }}
          >
            Flashcard Analytics
          </h1>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {[1, 2, 3, 4].map((i) => (
              <GlassSkeleton key={i} height="8rem" />
            ))}
          </div>
          <div style={{ marginTop: "2rem" }}>
            <GlassSkeleton height="12rem" />
          </div>
        </main>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <main className="page container">
          <GlassCard>
            <p style={{ color: "var(--color-text)", textAlign: "center" }}>
              {error}
            </p>
            <div style={{ textAlign: "center", marginTop: "1rem" }}>
              <GlassButton onClick={() => window.location.reload()}>
                Retry
              </GlassButton>
            </div>
          </GlassCard>
        </main>
      </PageTransition>
    );
  }

  if (!dashboard) return null;

  return (
    <PageTransition>
      <main className="page container">
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "1.5rem",
            flexWrap: "wrap",
            gap: "1rem",
          }}
        >
          <h1
            style={{
              fontSize: isMobile ? "var(--font-size-xl)" : "var(--font-size-2xl)",
              color: "var(--color-text)",
              margin: 0,
            }}
          >
            Flashcard Analytics
          </h1>
            <GlassButton
              variant="ghost"
              size="sm"
              onClick={() => navigate("/flashcards")}
              style={{ width: isMobile ? "100%" : undefined }}
            >
              ← Back
            </GlassButton>
          </div>

        {/* Overall Retention */}
        <GlassCard style={{ marginBottom: "1.5rem", textAlign: "center" }}>
          <p
            style={{
              fontSize: "var(--font-size-sm)",
              color: "var(--color-text-secondary)",
              margin: "0 0 0.5rem",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            Overall Retention
          </p>
          <p
            style={{
              fontSize: isMobile ? "3rem" : "4rem",
              color: "var(--color-accent)",
              fontWeight: 700,
              margin: 0,
              lineHeight: 1,
            }}
          >
            {Math.round(dashboard.overall_retention)}%
          </p>
          <p
            style={{
              fontSize: "var(--font-size-sm)",
              color: "var(--color-text-secondary)",
              margin: "0.5rem 0 0",
            }}
          >
            {dashboard.total_cards_studied} cards studied across{" "}
            {dashboard.total_sessions} sessions
          </p>
        </GlassCard>

        {/* Predicted Readiness */}
        <GlassCard style={{ marginBottom: "1.5rem" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              flexWrap: "wrap",
              gap: "1rem",
              flexDirection: isMobile ? "column" : "row",
              alignItems: isMobile ? "flex-start" : "center",
            }}
          >
            <div>
              <p
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-text-secondary)",
                  margin: "0 0 0.25rem",
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                Predicted Exam Readiness
              </p>
              <p
                style={{
                  fontSize: isMobile ? "var(--font-size-xl)" : "var(--font-size-2xl)",
                  color: "var(--color-text)",
                  fontWeight: 700,
                  margin: 0,
                }}
              >
                {Math.round(dashboard.predicted_readiness)}%
              </p>
            </div>
            <div
              style={{
                width: isMobile ? "100%" : "120px",
                height: "8px",
                background: "var(--glass-bg-subtle)",
                borderRadius: "var(--radius-sm)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${dashboard.predicted_readiness}%`,
                  height: "100%",
                  background:
                    dashboard.predicted_readiness >= 80
                      ? "#10b981"
                      : dashboard.predicted_readiness >= 50
                      ? "#f59e0b"
                      : "#ef4444",
                  borderRadius: "var(--radius-sm)",
                }}
              />
            </div>
          </div>
        </GlassCard>

        {/* Strongest / Weakest Subjects */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "1.5rem",
            marginBottom: "2rem",
          }}
        >
          {/* Strongest */}
          <GlassCard>
            <h2
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: "0 0 1rem",
              }}
            >
              Strongest Subjects
            </h2>
            {dashboard.strongest_subjects.length === 0 ? (
              <p
                style={{
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-sm)",
                  margin: 0,
                }}
              >
                Not enough data yet.
              </p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                {dashboard.strongest_subjects.map((subject) => (
                  <div
                    key={subject.category}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "var(--font-size-base)",
                        color: "var(--color-text)",
                        textTransform: "capitalize",
                      }}
                    >
                      {subject.category}
                    </span>
                    <span
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "#10b981",
                        fontWeight: 600,
                      }}
                    >
                      {Math.round(subject.retention_rate)}%
                    </span>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>

          {/* Weakest */}
          <GlassCard>
            <h2
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: "0 0 1rem",
              }}
            >
              Weakest Subjects
            </h2>
            {dashboard.weakest_subjects.length === 0 ? (
              <p
                style={{
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-sm)",
                  margin: 0,
                }}
              >
                Not enough data yet.
              </p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                {dashboard.weakest_subjects.map((subject) => (
                  <div
                    key={subject.category}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <span
                      style={{
                        fontSize: "var(--font-size-base)",
                        color: "var(--color-text)",
                        textTransform: "capitalize",
                      }}
                    >
                      {subject.category}
                    </span>
                    <span
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "#ef4444",
                        fontWeight: 600,
                      }}
                    >
                      {Math.round(subject.retention_rate)}%
                    </span>
                  </div>
                ))}
              </div>
            )}
          </GlassCard>
        </div>

        {/* Heatmap */}
        {heatmap.length > 0 && (
          <GlassCard style={{ marginBottom: "2rem" }}>
            <h2 style={{ fontSize: "var(--font-size-lg)", color: "var(--color-text)", margin: "0 0 1rem" }}>
              Review Heatmap (Last 90 Days)
            </h2>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "3px" }}>
              {heatmap.map((entry) => {
                const intensity = Math.min(1, entry.cards_reviewed / 20);
                const bg = entry.cards_reviewed === 0
                  ? "var(--glass-bg-subtle)"
                  : `rgba(99, 102, 241, ${0.2 + intensity * 0.8})`;
                return (
                  <div
                    key={entry.date}
                    title={`${entry.date}: ${entry.cards_reviewed} reviews`}
                    style={{
                      width: "12px",
                      height: "12px",
                      borderRadius: "2px",
                      background: bg,
                    }}
                  />
                );
              })}
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0.5rem", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
              <span>Less</span>
              <div style={{ display: "flex", gap: "3px" }}>
                {[0.2, 0.4, 0.6, 0.8, 1].map((v) => (
                  <div key={v} style={{ width: "12px", height: "12px", borderRadius: "2px", background: `rgba(99, 102, 241, ${v})` }} />
                ))}
              </div>
              <span>More</span>
            </div>
          </GlassCard>
        )}

        {/* Recommendations */}
        <h2
          style={{
            fontSize: "var(--font-size-lg)",
            color: "var(--color-text)",
            margin: "0 0 1rem",
          }}
        >
          Recommendations
        </h2>
        {recommendations.length === 0 ? (
          <GlassCard>
            <p
              style={{
                color: "var(--color-text-secondary)",
                textAlign: "center",
                margin: 0,
              }}
            >
              No recommendations yet. Keep studying to get personalized suggestions.
            </p>
          </GlassCard>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {recommendations.map((rec) => (
              <GlassCard
                key={rec.id}
                hoverable
                onClick={() => navigate(`/flashcards/decks/${rec.deck_id}`)}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "1rem",
                  }}
                >
                  <div>
                    <p
                      style={{
                        fontSize: "var(--font-size-base)",
                        color: "var(--color-text)",
                        margin: "0 0 0.25rem",
                        fontWeight: 500,
                      }}
                    >
                      {rec.deck_title}
                    </p>
                    <p
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text-secondary)",
                        margin: 0,
                      }}
                    >
                      {rec.reason}
                    </p>
                  </div>
                  <span
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-accent)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    Priority {rec.priority}
                  </span>
                </div>
              </GlassCard>
            ))}
          </div>
        )}
      </main>
    </PageTransition>
  );
}
