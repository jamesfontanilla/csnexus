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
import { readinessApi } from "../api/readiness";
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

interface QueueItemSchema {
  id: number;
  position: number;
  item_type: string;
  payload: Record<string, unknown>;
  estimated_seconds: number;
}

interface QueueResponse {
  items: QueueItemSchema[];
  total_estimated_seconds: number;
  items_remaining: number;
  items_completed: number;
  time_budget_minutes: number;
}

interface UserXPResponse {
  cumulative_xp: number;
  level: number;
  streak: number;
}

interface DashboardLoadState {
  readinessScore: number;
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

const FALLBACK_DASHBOARD_LOAD_STATE: DashboardLoadState = {
  readinessScore: 0,
  impactAreas: [],
};

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

function toTitleCase(value: string): string {
  return value
    .split(/[_\s-]+/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

function queueItemTypeToDashboardType(itemType: string): DailyQueueItem["type"] {
  if (itemType.includes("flashcard")) return "flashcard";
  if (itemType.includes("quiz")) return "quiz";
  if (itemType.includes("content") || itemType.includes("lesson")) return "lesson";
  return "review";
}

function extractQueueItemTitle(item: QueueItemSchema): string {
  const payload = item.payload ?? {};
  const keys = ["title", "name", "subtopic_name", "subtopic_title", "lesson_title", "deck_title", "topic_name"];

  for (const key of keys) {
    const value = payload[key];
    if (typeof value === "string" && value.trim()) {
      return value;
    }
  }

  return toTitleCase(item.item_type);
}

function mapQueueItem(item: QueueItemSchema): DailyQueueItem {
  return {
    id: String(item.id),
    title: extractQueueItemTitle(item),
    type: queueItemTypeToDashboardType(item.item_type),
    estimatedMinutes: Math.max(1, Math.ceil(item.estimated_seconds / 60)),
  };
}

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

    timeoutRef.current = setTimeout(() => {
      setLoading(false);
      setError(true);
    }, ERROR_TIMEOUT_MS);

    Promise.allSettled([
      readinessApi.getDashboard(),
      apiClient.get<UserXPResponse>("/v1/xp/me"),
      apiClient.get<QueueResponse>("/v1/queue"),
    ]).then((results) => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);

      const readinessResult = results[0];
      const xpResult = results[1];
      const queueResult = results[2];
      const hasAnySuccessfulResponse = results.some((result) => result.status === "fulfilled");

      if (!hasAnySuccessfulResponse) {
        setLoading(false);
        setError(true);
        return;
      }

      const xpData = xpResult.status === "fulfilled" ? xpResult.value : null;
      const queueData = queueResult.status === "fulfilled" ? queueResult.value : null;
      const readinessLoadState =
        readinessResult.status === "fulfilled"
          ? (() => {
              const topImpact = readinessResult.value.top_impact_subtopics ?? [];
              const highestImpact = Math.max(1, ...topImpact.map((item) => item.point_impact));

              return {
                readinessScore: readinessResult.value.score,
                impactAreas: topImpact.map((item) => ({
                  subject: item.subtopic_name,
                  score: item.point_impact,
                  maxScore: highestImpact,
                })),
              };
            })()
          : FALLBACK_DASHBOARD_LOAD_STATE;

      setData({
        readinessScore: readinessLoadState.readinessScore,
        streak: xpData?.streak ?? 0,
        xpToday: xpData?.cumulative_xp ?? 0,
        questionsToday: queueData?.items.length ?? 0,
        dailyQueue: queueData?.items.map(mapQueueItem) ?? [],
        impactAreas: readinessLoadState.impactAreas,
      });
      setLoading(false);
    }).catch(() => {
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
              Total XP
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
              Queue Items
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
