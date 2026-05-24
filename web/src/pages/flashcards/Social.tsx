import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { flashcardsApi, Deck } from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

type Tab = "feed" | "following";

export function Social() {
  const [activeTab, setActiveTab] = useState<Tab>("feed");
  const [feedDecks, setFeedDecks] = useState<Deck[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadFeed() {
      if (activeTab !== "feed") return;
      setLoading(true);
      setError(null);
      try {
        const decks = await flashcardsApi.getFeed();
        setFeedDecks(decks);
      } catch {
        setError("Failed to load feed.");
      } finally {
        setLoading(false);
      }
    }
    loadFeed();
  }, [activeTab]);

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
          Social
        </h1>

        {/* Tab Navigation */}
        <div
          style={{
            display: "flex",
            gap: "0.5rem",
            marginBottom: "1.5rem",
            borderBottom: "1px solid var(--glass-border)",
            paddingBottom: "0.5rem",
          }}
        >
          <button
            onClick={() => setActiveTab("feed")}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "var(--radius-sm)",
              border: "none",
              background:
                activeTab === "feed"
                  ? "var(--color-accent)"
                  : "transparent",
              color:
                activeTab === "feed"
                  ? "var(--color-text-on-accent, #fff)"
                  : "var(--color-text-secondary)",
              cursor: "pointer",
              fontSize: "var(--font-size-base)",
              fontWeight: 500,
            }}
          >
            Feed
          </button>
          <button
            onClick={() => setActiveTab("following")}
            style={{
              padding: "0.5rem 1rem",
              borderRadius: "var(--radius-sm)",
              border: "none",
              background:
                activeTab === "following"
                  ? "var(--color-accent)"
                  : "transparent",
              color:
                activeTab === "following"
                  ? "var(--color-text-on-accent, #fff)"
                  : "var(--color-text-secondary)",
              cursor: "pointer",
              fontSize: "var(--font-size-base)",
              fontWeight: 500,
            }}
          >
            Following
          </button>
        </div>

        {/* Feed Tab */}
        {activeTab === "feed" && (
          <>
            {loading ? (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fill, minmax(280px, 1fr))",
                  gap: "1.5rem",
                }}
              >
                {[1, 2, 3].map((i) => (
                  <GlassSkeleton key={i} height="10rem" />
                ))}
              </div>
            ) : error ? (
              <GlassCard>
                <p
                  style={{
                    color: "var(--color-text)",
                    textAlign: "center",
                  }}
                >
                  {error}
                </p>
              </GlassCard>
            ) : feedDecks.length === 0 ? (
              <GlassCard>
                <div style={{ textAlign: "center", padding: "2rem 0" }}>
                  <p
                    style={{
                      color: "var(--color-text-secondary)",
                      fontSize: "var(--font-size-base)",
                      margin: "0 0 1rem",
                    }}
                  >
                    No decks in your feed yet. Follow creators from the
                    marketplace to see their decks here.
                  </p>
                  <Link
                    to="/flashcards/marketplace"
                    style={{ textDecoration: "none" }}
                  >
                    <GlassButton variant="primary">
                      Browse Marketplace
                    </GlassButton>
                  </Link>
                </div>
              </GlassCard>
            ) : (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fill, minmax(280px, 1fr))",
                  gap: "1.5rem",
                }}
              >
                {feedDecks.map((deck) => (
                  <GlassCard key={deck.id}>
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "0.75rem",
                        height: "100%",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          alignItems: "flex-start",
                          justifyContent: "space-between",
                        }}
                      >
                        <h3
                          style={{
                            fontSize: "var(--font-size-base)",
                            color: "var(--color-text)",
                            margin: 0,
                            fontWeight: 600,
                          }}
                        >
                          {deck.title}
                        </h3>
                        <span
                          style={{
                            fontSize: "var(--font-size-sm)",
                            color: "var(--color-accent)",
                            background: "var(--glass-bg-subtle)",
                            padding: "0.125rem 0.5rem",
                            borderRadius: "var(--radius-sm)",
                            textTransform: "capitalize",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {deck.category}
                        </span>
                      </div>
                      {deck.description && (
                        <p
                          style={{
                            fontSize: "var(--font-size-sm)",
                            color: "var(--color-text-secondary)",
                            margin: 0,
                          }}
                        >
                          {deck.description}
                        </p>
                      )}
                      <p
                        style={{
                          fontSize: "var(--font-size-sm)",
                          color: "var(--color-text-secondary)",
                          margin: 0,
                        }}
                      >
                        {deck.card_count} card
                        {deck.card_count !== 1 ? "s" : ""}
                      </p>
                      <div style={{ marginTop: "auto" }}>
                        <Link
                          to="/flashcards/marketplace"
                          style={{ textDecoration: "none" }}
                        >
                          <GlassButton variant="ghost" size="sm">
                            View
                          </GlassButton>
                        </Link>
                      </div>
                    </div>
                  </GlassCard>
                ))}
              </div>
            )}
          </>
        )}

        {/* Following Tab */}
        {activeTab === "following" && (
          <GlassCard>
            <div style={{ textAlign: "center", padding: "2rem 0" }}>
              <p
                style={{
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-base)",
                  margin: 0,
                }}
              >
                Manage who you follow from deck pages
              </p>
            </div>
          </GlassCard>
        )}
      </main>
    </PageTransition>
  );
}
