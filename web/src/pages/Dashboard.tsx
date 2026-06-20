import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { apiClient } from "../api/client";
import { GlassCard } from "../components/GlassCard";
import { GlassSkeleton } from "../components/GlassSkeleton";
import { GlassProgressBar } from "../components/GlassProgressBar";
import { AnimatedNumber } from "../components/AnimatedNumber";
import { ProgressRing } from "../components/ProgressRing";
import { EmptyState } from "../components/EmptyState";
import { PageTransition } from "../components/PageTransition";
import { GradientText } from "../components/GradientText";
import { useMediaQuery } from "../hooks/useMediaQuery";

// --- TypeScript Interfaces ---

export interface DailyQueueItem {
  id: string;
  title: string;
  type: "lesson" | "quiz" | "flashcard" | "review";
  estimatedMinutes: number;
}

export interface ImpactArea {
  subject: string;
  score: number;
  maxScore: number;
}

export interface DashboardData {
  readinessScore: number;
  streak: number;
  xpToday: number;
  questionsToday: number;
  dailyQueue: DailyQueueItem[];
  impactAreas: ImpactArea[];
}

// --- Constants ---

const TYPE_ICONS: Record<DailyQueueItem["type"], string> = {
  lesson: "📖",
  quiz: "✍️",
  flashcard: "🃏",
  review: "🔄",
};

const ERROR_TIMEOUT_MS = 10_000;

const MOBILE_FEATURES = [
  {
    to: "/queue",
    title: "Queue",
    icon: "🔄",
    description: "Daily plan",
  },
  {
    to: "/flashcards",
    title: "Flashcards",
    icon: "🃏",
    description: "Decks and study",
  },
  {
    to: "/tutor",
    title: "Tutor",
    icon: "🤖",
    description: "Guided help",
  },
  {
    to: "/focus",
    title: "Focus",
    icon: "⏱️",
    description: "Study timer",
  },
  {
    to: "/readiness",
    title: "Readiness",
    icon: "📊",
    description: "Exam state",
  },
  {
    to: "/analytics",
    title: "Analytics",
    icon: "📈",
    description: "Progress detail",
  },
  {
    to: "/leaderboard",
    title: "Leaderboard",
    icon: "🏆",
    description: "Rankings",
  },
  {
    to: "/study-plan",
    title: "Study Plan",
    icon: "🗓️",
    description: "Schedule",
  },
] as const;

// --- Component ---

export function Dashboard() {
  const isMobile = useMediaQuery("(max-width: 639px)");
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  function fetchDashboard() {
    setLoading(true);
    setError(false);
    setAnimatedScore(0);

    // Start the 10s error timeout
    timeoutRef.current = setTimeout(() => {
      setLoading(false);
      setError(true);
    }, ERROR_TIMEOUT_MS);

    apiClient
      .get<DashboardData>("/v1/dashboard/me")
      .then((result) => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setData(result);
        setLoading(false);
      })
      .catch(() => {
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        setLoading(false);
        setError(true);
      });
  }

  useEffect(() => {
    fetchDashboard();
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  // Animate readiness score from 0 to actual value on data arrival
  useEffect(() => {
    if (data) {
      // Small delay to ensure ProgressRing mounts at 0 first
      const raf = requestAnimationFrame(() => {
        setAnimatedScore(data.readinessScore);
      });
      return () => cancelAnimationFrame(raf);
    }
  }, [data]);

  // --- Loading State ---
  if (loading) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 800 }}>
          <h1
            style={{
              fontFamily: "var(--font-display)",
              letterSpacing: "-0.02em",
              marginBottom: "var(--space-6)",
            }}
          >
            <GradientText variant="accent">Dashboard</GradientText>
          </h1>

          {/* Hero skeleton */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              marginBottom: "var(--space-6)",
            }}
          >
            <GlassSkeleton width="200px" height="200px" borderRadius="50%" />
          </div>

          {/* Quick stats skeleton */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(3, 1fr)",
              gap: "var(--space-4)",
              marginBottom: "var(--space-6)",
            }}
          >
            <GlassSkeleton variant="card" />
            <GlassSkeleton variant="card" />
            <GlassSkeleton variant="card" />
          </div>

          {/* Daily queue skeleton */}
          <GlassSkeleton variant="card" height="180px" />

          {/* Impact areas skeleton */}
          <div style={{ marginTop: "var(--space-6)" }}>
            <GlassSkeleton lines={4} height="1.25rem" />
          </div>
        </main>
      </PageTransition>
    );
  }

  // --- Error State ---
  if (error || !data) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 800 }}>
          <EmptyState
            icon="⚠️"
            title="Unable to Load Dashboard"
            description="Something went wrong while fetching your dashboard data. Please try again."
            actionLabel="Retry"
            onAction={fetchDashboard}
          />
        </main>
      </PageTransition>
    );
  }

  // --- Loaded State ---
  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 800 }}>
        <h1
          style={{
            fontFamily: "var(--font-display)",
            letterSpacing: "-0.02em",
            marginBottom: "var(--space-6)",
          }}
        >
          <GradientText variant="accent">Dashboard</GradientText>
        </h1>

        {/* Hero Section — ProgressRing */}
        <section
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: "var(--space-6)",
          }}
        >
          <ProgressRing size={200} value={animatedScore} label="Readiness">
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <span
                style={{
                  fontSize: "var(--font-size-2xl)",
                  fontWeight: 700,
                  fontFamily: "var(--font-display)",
                }}
              >
                <AnimatedNumber value={animatedScore} suffix="%" duration={1000} />
              </span>
              <span
                style={{
                  fontSize: "var(--font-size-xs)",
                  color: "var(--color-text-secondary)",
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                }}
              >
                Readiness
              </span>
            </div>
          </ProgressRing>
        </section>

        {isMobile && (
          <section style={{ marginBottom: "var(--space-6)" }}>
            <h2
              style={{
                fontSize: "var(--font-size-lg)",
                fontWeight: 600,
                fontFamily: "var(--font-display)",
                color: "var(--color-text)",
                marginBottom: "var(--space-3)",
              }}
            >
              Quick Access
            </h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                gap: "var(--space-3)",
              }}
            >
              {MOBILE_FEATURES.map((feature) => (
                <Link
                  key={feature.to}
                  to={feature.to}
                  aria-label={feature.title}
                  style={{
                    textDecoration: "none",
                    display: "block",
                    minWidth: 0,
                  }}
                >
                  <GlassCard
                    hoverable
                    as="article"
                    style={{
                      height: "100%",
                      minHeight: "7.5rem",
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "space-between",
                      gap: "var(--space-3)",
                    }}
                  >
                    <span
                      aria-hidden="true"
                      style={{
                        fontSize: "1.4rem",
                        lineHeight: 1,
                        color: "var(--color-accent)",
                      }}
                    >
                      {feature.icon}
                    </span>
                    <div style={{ minWidth: 0 }}>
                      <p
                        style={{
                          margin: 0,
                          fontSize: "var(--font-size-base)",
                          fontWeight: 600,
                          color: "var(--color-text)",
                        }}
                      >
                        {feature.title}
                      </p>
                      <p
                        style={{
                          margin: "0.25rem 0 0",
                          fontSize: "var(--font-size-xs)",
                          color: "var(--color-text-secondary)",
                        }}
                      >
                        {feature.description}
                      </p>
                    </div>
                  </GlassCard>
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* Quick Stats Row */}
        <section
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "var(--space-4)",
            marginBottom: "var(--space-6)",
          }}
        >
          <GlassCard style={{ textAlign: "center" }}>
            <p
              style={{
                fontSize: "var(--font-size-2xl)",
                fontWeight: 700,
                margin: "0 0 var(--space-1)",
                fontFamily: "var(--font-display)",
              }}
            >
              <GradientText variant="accent">
                <AnimatedNumber value={data.streak} duration={1000} />
              </GradientText>
            </p>
            <p
              style={{
                fontSize: "var(--font-size-xs)",
                color: "var(--color-text-secondary)",
                margin: 0,
                letterSpacing: "0.03em",
              }}
            >
              Day Streak 🔥
            </p>
          </GlassCard>

          <GlassCard style={{ textAlign: "center" }}>
            <p
              style={{
                fontSize: "var(--font-size-2xl)",
                fontWeight: 700,
                margin: "0 0 var(--space-1)",
                fontFamily: "var(--font-display)",
              }}
            >
              <GradientText variant="success">
                <AnimatedNumber value={data.xpToday} duration={1000} suffix=" XP" />
              </GradientText>
            </p>
            <p
              style={{
                fontSize: "var(--font-size-xs)",
                color: "var(--color-text-secondary)",
                margin: 0,
                letterSpacing: "0.03em",
              }}
            >
              XP Today
            </p>
          </GlassCard>

          <GlassCard style={{ textAlign: "center" }}>
            <p
              style={{
                fontSize: "var(--font-size-2xl)",
                fontWeight: 700,
                margin: "0 0 var(--space-1)",
                fontFamily: "var(--font-display)",
              }}
            >
              <GradientText variant="info">
                <AnimatedNumber value={data.questionsToday} duration={1000} />
              </GradientText>
            </p>
            <p
              style={{
                fontSize: "var(--font-size-xs)",
                color: "var(--color-text-secondary)",
                margin: 0,
                letterSpacing: "0.03em",
              }}
            >
              Questions Today
            </p>
          </GlassCard>
        </section>

        {/* Daily Queue Card */}
        <section style={{ marginBottom: "var(--space-6)" }}>
          <h2
            style={{
              fontSize: "var(--font-size-lg)",
              fontWeight: 600,
              fontFamily: "var(--font-display)",
              color: "var(--color-text)",
              marginBottom: "var(--space-3)",
            }}
          >
            Daily Queue
          </h2>
          <GlassCard elevation="raised">
            {data.dailyQueue.length === 0 ? (
              <p
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-text-secondary)",
                  margin: 0,
                }}
              >
                No items in your queue today. Great job!
              </p>
            ) : (
              <ul
                style={{
                  listStyle: "none",
                  padding: 0,
                  margin: 0,
                  display: "flex",
                  flexDirection: "column",
                  gap: "var(--space-3)",
                }}
              >
                {data.dailyQueue.map((item) => (
                  <li
                    key={item.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "var(--space-3)",
                      padding: "var(--space-2) 0",
                      borderBottom: "1px solid var(--glass-border-light)",
                    }}
                  >
                    <span
                      style={{ fontSize: "1.25rem" }}
                      aria-hidden="true"
                    >
                      {TYPE_ICONS[item.type]}
                    </span>
                    <span
                      style={{
                        flex: 1,
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text)",
                      }}
                    >
                      {item.title}
                    </span>
                    <span
                      style={{
                        fontSize: "var(--font-size-xs)",
                        color: "var(--color-text-muted)",
                        whiteSpace: "nowrap",
                      }}
                    >
                      ~{item.estimatedMinutes} min
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </GlassCard>
        </section>

        {/* Top Impact Areas */}
        <section>
          <h2
            style={{
              fontSize: "var(--font-size-lg)",
              fontWeight: 600,
              fontFamily: "var(--font-display)",
              color: "var(--color-text)",
              marginBottom: "var(--space-3)",
            }}
          >
            Top Impact Areas
          </h2>
          <GlassCard>
            {data.impactAreas.length === 0 ? (
              <p
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-text-secondary)",
                  margin: 0,
                }}
              >
                Complete more activities to see your impact areas.
              </p>
            ) : (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "var(--space-4)",
                }}
              >
                {data.impactAreas.map((area) => (
                  <GlassProgressBar
                    key={area.subject}
                    value={area.score}
                    max={area.maxScore}
                    label={area.subject}
                    animated
                  />
                ))}
              </div>
            )}
          </GlassCard>
        </section>
      </main>
    </PageTransition>
  );
}
