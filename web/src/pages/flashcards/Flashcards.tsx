import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { flashcardsApi, Deck, QueueSummary } from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

export function Flashcards() {
  const navigate = useNavigate();
  const [decks, setDecks] = useState<Deck[]>([]);
  const [queueSummary, setQueueSummary] = useState<QueueSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openMenuId, setOpenMenuId] = useState<number | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [decksRes, queueRes] = await Promise.all([
          flashcardsApi.getDecks(),
          flashcardsApi.getQueueSummary(),
        ]);
        setDecks(decksRes);
        setQueueSummary(queueRes);
      } catch (err) {
        setError("Failed to load flashcard data. Please try again.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  }

  async function handleDeleteDeck(deckId: number) {
    const confirmed = window.confirm(
      "Are you sure you want to delete this deck? This action cannot be undone."
    );
    if (!confirmed) return;
    try {
      await flashcardsApi.deleteDeck(deckId);
      setDecks((prev) => prev.filter((d) => d.id !== deckId));
    } catch {
      setError("Failed to delete deck. Please try again.");
    }
  }

  if (loading) {
    return (
      <PageTransition>
        <main className="page container">
          <div style={{ marginBottom: "2rem" }}>
            <GlassSkeleton height="6rem" />
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {[1, 2, 3, 4].map((i) => (
              <GlassSkeleton key={i} height="10rem" />
            ))}
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
          Flashcards
        </h1>

        {/* Queue Summary */}
        {queueSummary && queueSummary.due_count > 0 && (
          <GlassCard
            style={{ marginBottom: "2rem", cursor: "pointer" }}
            hoverable
            onClick={() => navigate("/flashcards/study")}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                flexWrap: "wrap",
                gap: "1rem",
              }}
            >
              <div>
                <p
                  style={{
                    fontSize: "var(--font-size-lg)",
                    color: "var(--color-text)",
                    fontWeight: 600,
                    margin: 0,
                  }}
                >
                  {queueSummary.due_count} cards due today
                </p>
                <p
                  style={{
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    margin: "0.25rem 0 0",
                  }}
                >
                  {queueSummary.overdue_count > 0 &&
                    `${queueSummary.overdue_count} overdue · `}
                  ~{queueSummary.estimated_minutes} min estimated
                </p>
              </div>
              <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
                <GlassButton
                  variant="primary"
                  size="sm"
                  onClick={() => {
                    navigate("/flashcards/study", { state: { mode: "swipe" } });
                  }}
                >
                  Study Now
                </GlassButton>
                <GlassButton
                  variant="secondary"
                  size="sm"
                  onClick={() => {
                    navigate("/flashcards/study", { state: { mode: "typing" } });
                  }}
                >
                  Type Mode
                </GlassButton>
              </div>
            </div>
          </GlassCard>
        )}

        {/* Decks Header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "1.5rem",
          }}
        >
          <h2
            style={{
              fontSize: "var(--font-size-lg)",
              color: "var(--color-text)",
              margin: 0,
            }}
          >
            Your Decks
          </h2>
          <GlassButton
            variant="primary"
            size="sm"
            onClick={() => navigate("/flashcards/decks/new")}
          >
            + Create Deck
          </GlassButton>
        </div>

        {/* Decks Grid */}
        {decks.length === 0 ? (
          <GlassCard>
            <div style={{ textAlign: "center", padding: "2rem 0" }}>
              <p
                style={{
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-base)",
                  margin: "0 0 1rem",
                }}
              >
                No decks yet. Create your first deck or browse the marketplace.
              </p>
              <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
                <GlassButton
                  variant="primary"
                  onClick={() => navigate("/flashcards/decks/new")}
                >
                  Create Deck
                </GlassButton>
                <GlassButton
                  variant="secondary"
                  onClick={() => navigate("/flashcards/marketplace")}
                >
                  Browse Marketplace
                </GlassButton>
              </div>
            </div>
          </GlassCard>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {decks.map((deck) => (
              <GlassCard
                key={deck.id}
                hoverable
                onClick={() => navigate(`/flashcards/decks/${deck.id}`)}
              >
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "0.75rem",
                    height: "100%",
                    position: "relative",
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
                    <div style={{ display: "flex", alignItems: "center", gap: "0.25rem" }}>
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
                      <div style={{ position: "relative" }}>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setOpenMenuId(openMenuId === deck.id ? null : deck.id);
                          }}
                          style={{
                            background: "none",
                            border: "none",
                            cursor: "pointer",
                            padding: "0.25rem",
                            fontSize: "var(--font-size-lg)",
                            color: "var(--color-text-secondary)",
                            lineHeight: 1,
                          }}
                          aria-label="Deck options"
                        >
                          ⋮
                        </button>
                        {openMenuId === deck.id && (
                          <div
                            style={{
                              position: "absolute",
                              top: "100%",
                              right: 0,
                              background: "var(--glass-bg)",
                              border: "1px solid var(--glass-border)",
                              borderRadius: "var(--radius-sm)",
                              boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
                              zIndex: 10,
                              minWidth: "8rem",
                              overflow: "hidden",
                            }}
                          >
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setOpenMenuId(null);
                                navigate(`/flashcards/decks/${deck.id}`);
                              }}
                              style={{
                                display: "block",
                                width: "100%",
                                padding: "0.5rem 1rem",
                                border: "none",
                                background: "none",
                                color: "var(--color-text)",
                                fontSize: "var(--font-size-sm)",
                                textAlign: "left",
                                cursor: "pointer",
                              }}
                            >
                              Edit
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setOpenMenuId(null);
                                handleDeleteDeck(deck.id);
                              }}
                              style={{
                                display: "block",
                                width: "100%",
                                padding: "0.5rem 1rem",
                                border: "none",
                                background: "none",
                                color: "var(--color-error, #ef4444)",
                                fontSize: "var(--font-size-sm)",
                                textAlign: "left",
                                cursor: "pointer",
                              }}
                            >
                              Delete
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    {deck.card_count} card{deck.card_count !== 1 ? "s" : ""}
                  </p>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                      marginTop: "auto",
                    }}
                  >
                    Last updated {formatDate(deck.updated_at)}
                  </p>
                </div>
              </GlassCard>
            ))}
          </div>
        )}

        {/* Quick Links */}
        <div
          style={{
            display: "flex",
            gap: "1rem",
            marginTop: "2rem",
            flexWrap: "wrap",
          }}
        >
          <Link to="/flashcards/generate" style={{ textDecoration: "none" }}>
            <GlassButton variant="ghost" size="sm">
              Generate
            </GlassButton>
          </Link>
          <Link to="/flashcards/marketplace" style={{ textDecoration: "none" }}>
            <GlassButton variant="ghost" size="sm">
              Marketplace
            </GlassButton>
          </Link>
          <Link to="/flashcards/analytics" style={{ textDecoration: "none" }}>
            <GlassButton variant="ghost" size="sm">
              Analytics
            </GlassButton>
          </Link>
          <Link to="/flashcards/social" style={{ textDecoration: "none" }}>
            <GlassButton variant="ghost" size="sm">
              Social
            </GlassButton>
          </Link>
        </div>
      </main>
    </PageTransition>
  );
}
