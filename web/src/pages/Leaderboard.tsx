import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient } from "../api/client";
import { GlassCard } from "../components/GlassCard";
import { GlassSkeleton } from "../components/GlassSkeleton";
import { GradientText } from "../components/GradientText";
import { EmptyState } from "../components/EmptyState";
import { PageTransition } from "../components/PageTransition";
import { staggerContainer, staggerItem, springDefault } from "../design-system";

interface LeaderboardEntry {
  display_name: string;
  level: number;
  xp_window: number;
  category: string;
}

export function Leaderboard() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<LeaderboardEntry[]>("/v1/leaderboards/global")
      .then((res) => setEntries(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 720 }}>
          <h1 style={{ color: "var(--color-text)", fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            Leaderboard
          </h1>
          <GlassCard>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
              {[1, 2, 3, 4, 5].map((i) => (
                <GlassSkeleton key={i} height="2.5rem" />
              ))}
            </div>
          </GlassCard>
        </div>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 720 }}>
          <p style={{ color: "var(--color-danger)" }}>{error}</p>
        </div>
      </PageTransition>
    );
  }

  const RANK_MEDALS = ["🥇", "🥈", "🥉"];

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 720 }}>
        <h1 style={{ color: "var(--color-text)", fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
          Leaderboard
        </h1>

        {/* Top 3 Podium */}
        {entries.length >= 3 && (
          <div style={{ display: "flex", justifyContent: "center", gap: "var(--space-4)", marginBottom: "var(--space-8)", alignItems: "flex-end" }}>
            {[1, 0, 2].map((idx) => {
              const entry = entries[idx];
              const isFirst = idx === 0;
              return (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ ...springDefault, delay: idx * 0.1 }}
                  style={{ textAlign: "center", flex: "0 0 auto" }}
                >
                  <GlassCard
                    lifted={isFirst}
                    style={{
                      padding: isFirst ? "var(--space-6) var(--space-5)" : "var(--space-4) var(--space-4)",
                      minWidth: isFirst ? "120px" : "100px",
                    }}
                  >
                    <div style={{ fontSize: isFirst ? "2rem" : "1.5rem", marginBottom: "var(--space-2)" }}>
                      {RANK_MEDALS[idx]}
                    </div>
                    <div style={{
                      fontSize: isFirst ? "var(--font-size-base)" : "var(--font-size-sm)",
                      fontWeight: 700,
                      color: "var(--color-text)",
                      marginBottom: "var(--space-1)",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      maxWidth: "100px",
                    }}>
                      {entry.display_name}
                    </div>
                    <div style={{ fontSize: "var(--font-size-sm)" }}>
                      <GradientText variant="accent">{entry.xp_window.toLocaleString()} XP</GradientText>
                    </div>
                  </GlassCard>
                </motion.div>
              );
            })}
          </div>
        )}

        <GlassCard>
          <motion.div variants={staggerContainer} initial="initial" animate="animate">
            <table style={{ width: "100%", borderCollapse: "collapse" }} aria-label="Global leaderboard">
              <thead>
                <tr style={{ borderBottom: "1px solid var(--glass-border-medium)" }}>
                  <th style={{ textAlign: "left", padding: "var(--space-3) var(--space-2)", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", fontWeight: 600, letterSpacing: "0.04em", textTransform: "uppercase" }}>#</th>
                  <th style={{ textAlign: "left", padding: "var(--space-3) var(--space-2)", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", fontWeight: 600, letterSpacing: "0.04em", textTransform: "uppercase" }}>Name</th>
                  <th style={{ textAlign: "right", padding: "var(--space-3) var(--space-2)", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", fontWeight: 600, letterSpacing: "0.04em", textTransform: "uppercase" }}>Level</th>
                  <th style={{ textAlign: "right", padding: "var(--space-3) var(--space-2)", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", fontWeight: 600, letterSpacing: "0.04em", textTransform: "uppercase" }}>XP</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry, i) => (
                  <motion.tr
                    key={i}
                    variants={staggerItem}
                    className="leaderboard-row"
                    style={{
                      background: i < 3 ? "var(--glass-bg-medium)" : "var(--glass-bg-subtle)",
                      borderBottom: "1px solid var(--glass-border-light)",
                      transition: "background var(--transition-fast)",
                    }}
                  >
                    <td style={{ padding: "var(--space-3) var(--space-2)", color: "var(--color-text-muted)", fontSize: "var(--font-size-sm)", fontWeight: 600 }}>
                      {i < 3 ? RANK_MEDALS[i] : i + 1}
                    </td>
                    <td style={{ padding: "var(--space-3) var(--space-2)", color: "var(--color-text)", fontSize: "var(--font-size-base)", fontWeight: i < 3 ? 600 : 400 }}>{entry.display_name}</td>
                    <td style={{ textAlign: "right", padding: "var(--space-3) var(--space-2)", color: "var(--color-accent)", fontSize: "var(--font-size-sm)", fontWeight: 600 }}>{entry.level}</td>
                    <td style={{ textAlign: "right", padding: "var(--space-3) var(--space-2)", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", fontVariantNumeric: "tabular-nums" }}>{entry.xp_window.toLocaleString()}</td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </motion.div>
          {entries.length === 0 && (
            <EmptyState
              icon="🏆"
              title="No Entries Yet"
              description="Be the first to earn XP and claim the top spot."
            />
          )}
        </GlassCard>
        <Link
          to="/modules"
          style={{
            display: "inline-block",
            marginTop: "var(--space-6)",
            color: "var(--color-accent)",
            textDecoration: "none",
            fontSize: "var(--font-size-sm)",
            transition: "color var(--transition-fast)",
          }}
          aria-label="Back to modules"
        >
          ← Back
        </Link>
      </div>
    </PageTransition>
  );
}
