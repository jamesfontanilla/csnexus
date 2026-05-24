import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { flashcardsApi } from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

interface AdminData {
  top_failed_cards: Array<{ card_id: number; fail_count: number }>;
  active_reviewers_7d: number;
}

export function FlashcardAdmin() {
  const navigate = useNavigate();
  const [data, setData] = useState<AdminData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [flaggingId, setFlaggingId] = useState<number | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const res = await flashcardsApi.getAdminAnalytics();
        setData(res);
      } catch {
        setError("Failed to load admin data. You may not have admin access.");
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
          <h1 style={{ fontSize: "var(--font-size-2xl)", color: "var(--color-text)", marginBottom: "1.5rem" }}>
            Flashcard Admin
          </h1>
          <GlassSkeleton height="12rem" />
        </main>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <main className="page container">
          <GlassCard>
            <p style={{ color: "var(--color-text)", textAlign: "center" }}>{error}</p>
            <div style={{ textAlign: "center", marginTop: "1rem" }}>
              <GlassButton onClick={() => navigate("/flashcards")}>Back</GlassButton>
            </div>
          </GlassCard>
        </main>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <main className="page container">
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1.5rem", flexWrap: "wrap", gap: "1rem" }}>
          <h1 style={{ fontSize: "var(--font-size-2xl)", color: "var(--color-text)", margin: 0 }}>
            Flashcard Admin
          </h1>
          <GlassButton variant="ghost" size="sm" onClick={() => navigate("/flashcards")}>
            ← Back
          </GlassButton>
        </div>

        {/* Engagement Stats */}
        <GlassCard style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "var(--font-size-lg)", color: "var(--color-text)", margin: "0 0 1rem" }}>
            Engagement (Last 7 Days)
          </h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "1rem" }}>
            <div style={{ textAlign: "center" }}>
              <p style={{ fontSize: "var(--font-size-2xl)", color: "var(--color-accent)", fontWeight: 700, margin: 0 }}>
                {data?.active_reviewers_7d ?? 0}
              </p>
              <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: "0.25rem 0 0" }}>
                Active Reviewers
              </p>
            </div>
          </div>
        </GlassCard>

        {/* Top Failed Cards */}
        <GlassCard style={{ marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "var(--font-size-lg)", color: "var(--color-text)", margin: "0 0 1rem" }}>
            Top Failed Cards
          </h2>
          {(!data?.top_failed_cards || data.top_failed_cards.length === 0) ? (
            <p style={{ color: "var(--color-text-secondary)", margin: 0 }}>No data yet.</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {data.top_failed_cards.map((card, i) => (
                <div key={card.card_id} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.5rem", borderRadius: "var(--radius-sm)", background: i < 3 ? "rgba(239,68,68,0.05)" : "transparent" }}>
                  <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)" }}>
                    Card #{card.card_id}
                  </span>
                  <span style={{ fontSize: "var(--font-size-sm)", color: "#ef4444", fontWeight: 600 }}>
                    {card.fail_count} failures
                  </span>
                </div>
              ))}
            </div>
          )}
        </GlassCard>

        {/* Moderation Actions */}
        <GlassCard>
          <h2 style={{ fontSize: "var(--font-size-lg)", color: "var(--color-text)", margin: "0 0 1rem" }}>
            Moderation Actions
          </h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", flexWrap: "wrap" }}>
              <input
                type="number"
                placeholder="Deck ID to flag"
                value={flaggingId ?? ""}
                onChange={(e) => setFlaggingId(e.target.value ? Number(e.target.value) : null)}
                style={{ width: "120px", padding: "0.5rem", background: "var(--glass-bg-subtle)", border: "1px solid var(--glass-border-medium)", borderRadius: "var(--radius-sm)", color: "var(--color-text)", fontSize: "var(--font-size-sm)" }}
              />
              <GlassButton
                variant="danger"
                size="sm"
                disabled={!flaggingId}
                onClick={async () => {
                  if (!flaggingId) return;
                  try {
                    await flashcardsApi.flagDeck(flaggingId);
                    alert(`Deck ${flaggingId} flagged for removal.`);
                    setFlaggingId(null);
                  } catch { alert("Failed to flag deck."); }
                }}
              >
                Flag for Removal
              </GlassButton>
              <GlassButton
                variant="secondary"
                size="sm"
                disabled={!flaggingId}
                onClick={async () => {
                  if (!flaggingId) return;
                  try {
                    await flashcardsApi.featureDeck(flaggingId);
                    alert(`Deck ${flaggingId} featured status toggled.`);
                    setFlaggingId(null);
                  } catch { alert("Failed to toggle featured."); }
                }}
              >
                Toggle Featured
              </GlassButton>
            </div>
          </div>
        </GlassCard>
      </main>
    </PageTransition>
  );
}
