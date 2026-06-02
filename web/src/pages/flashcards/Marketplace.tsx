import { useState, useEffect, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  flashcardsApi,
  MarketplaceDeck,
  DeckCategory,
} from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { GlassSelect } from "../../components/GlassSelect";
import { EmptyState } from "../../components/EmptyState";
import { CrossfadeContent } from "../../components/CrossfadeContent";
import { PageTransition } from "../../components/PageTransition";

type SortOption = "popular" | "rating" | "newest";

const CATEGORIES: (DeckCategory | "all")[] = ["all", "verbal", "numerical", "analytical"];
const SORT_OPTIONS: { value: SortOption; label: string }[] = [
  { value: "popular", label: "Most Popular" },
  { value: "rating", label: "Highest Rated" },
  { value: "newest", label: "Newest" },
];

export function Marketplace() {
  const navigate = useNavigate();
  const [decks, setDecks] = useState<MarketplaceDeck[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [category, setCategory] = useState<DeckCategory | "all">("all");
  const [sort, setSort] = useState<SortOption>("popular");
  const [cloningId, setCloningId] = useState<number | null>(null);
  const [ratingDeckId, setRatingDeckId] = useState<number | null>(null);
  const [ratingScore, setRatingScore] = useState(0);
  const [commentDeckId, setCommentDeckId] = useState<number | null>(null);
  const [comments, setComments] = useState<Array<{ id: number; user_name: string; comment: string; created_at: string }>>([]);
  const [newComment, setNewComment] = useState("");
  const [loadingComments, setLoadingComments] = useState(false);
  const commentsAbortControllerRef = useRef<AbortController | null>(null);

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  const fetchDecks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params: { search?: string; category?: string; sort?: string } = {};
      if (debouncedSearch.trim()) params.search = debouncedSearch.trim();
      if (category !== "all") params.category = category;
      params.sort = sort;
      const result = await flashcardsApi.getMarketplace(params);
      setDecks(result);
    } catch (err) {
      setError("Failed to load marketplace. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [debouncedSearch, category, sort]);

  useEffect(() => {
    fetchDecks();
  }, [fetchDecks]);

  // Cleanup abort controller on unmount
  useEffect(() => {
    return () => {
      if (commentsAbortControllerRef.current) {
        commentsAbortControllerRef.current.abort();
      }
    };
  }, []);

  async function handleClone(deckId: number) {
    setCloningId(deckId);
    try {
      await flashcardsApi.cloneDeck(deckId);
      // Update clone count locally
      setDecks((prev) =>
        prev.map((d) =>
          d.id === deckId ? { ...d, clone_count: d.clone_count + 1 } : d
        )
      );
    } catch (err) {
      setError("Failed to clone deck.");
    } finally {
      setCloningId(null);
    }
  }

  async function handleRate(deckId: number) {
    if (ratingScore < 1 || ratingScore > 5) return;
    try {
      await flashcardsApi.rateDeck(deckId, { score: ratingScore });
      setRatingDeckId(null);
      setRatingScore(0);
      fetchDecks();
    } catch (err) {
      setError("Failed to submit rating.");
    }
  }

  function renderStars(rating: number) {
    const full = Math.floor(rating);
    const half = rating - full >= 0.5;
    let stars = "★".repeat(full);
    if (half) stars += "½";
    return stars || "☆";
  }

  if (loading && decks.length === 0) {
    return (
      <PageTransition>
        <main className="page container">
          <h1
            style={{
              fontSize: "var(--font-size-2xl)",
              color: "var(--color-text)",
              marginBottom: "var(--space-6)",
              fontFamily: "var(--font-display)",
            }}
          >
            Marketplace
          </h1>
          <GlassSkeleton height="3rem" />
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
              gap: "var(--space-6)",
              marginTop: "var(--space-6)",
            }}
          >
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <GlassSkeleton key={i} variant="card" />
            ))}
          </div>
        </main>
      </PageTransition>
    );
  }

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
              fontSize: "var(--font-size-2xl)",
              color: "var(--color-text)",
              margin: 0,
              fontFamily: "var(--font-display)",
              letterSpacing: "-0.02em",
            }}
          >
            Marketplace
          </h1>
          <GlassButton
            variant="ghost"
            size="sm"
            onClick={() => navigate("/flashcards")}
          >
            ← Back
          </GlassButton>
        </div>

        {/* Filters */}
        <GlassCard style={{ marginBottom: "1.5rem" }}>
          <div
            style={{
              display: "flex",
              gap: "1rem",
              flexWrap: "wrap",
              alignItems: "center",
            }}
          >
            <input
              type="text"
              placeholder="Search decks..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                flex: "1 1 200px",
                padding: "0.625rem",
                background: "var(--glass-bg-subtle)",
                border: "1px solid var(--glass-border-medium)",
                borderRadius: "var(--radius-sm)",
                color: "var(--color-text)",
                fontSize: "var(--font-size-base)",
              }}
            />
            <GlassSelect
              value={category}
              onChange={(v) => setCategory(v as DeckCategory | "all")}
              options={CATEGORIES.map((c) => ({
                value: c,
                label: c === "all" ? "All Categories" : c.charAt(0).toUpperCase() + c.slice(1),
              }))}
              aria-label="Category filter"
            />
            <GlassSelect
              value={sort}
              onChange={(v) => setSort(v as SortOption)}
              options={SORT_OPTIONS.map((opt) => ({ value: opt.value, label: opt.label }))}
              aria-label="Sort order"
            />
          </div>
        </GlassCard>

        {/* Error */}
        {error && (
          <GlassCard style={{ marginBottom: "1rem", background: "rgba(239,68,68,0.1)" }}>
            <p style={{ color: "var(--color-text)", margin: 0 }}>{error}</p>
          </GlassCard>
        )}

        {/* Results */}
        <CrossfadeContent contentKey={loading ? "loading" : "loaded"}>
        {decks.length === 0 && !loading ? (
          <EmptyState
            icon="🔍"
            title="No Decks Found"
            description="Try adjusting your search or filters to find what you're looking for."
            actionLabel="Clear Filters"
            onAction={() => { setSearch(""); setCategory("all"); setSort("popular"); }}
          />
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {decks.map((deck) => (
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
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical",
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
                    by {deck.creator_name} · {deck.card_count} cards
                  </p>

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "1rem",
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                    }}
                  >
                    <span style={{ color: "#f59e0b" }}>
                      {renderStars(deck.average_rating)} ({deck.rating_count})
                    </span>
                    <span>{deck.clone_count} clones</span>
                  </div>

                  {/* Rating inline */}
                  {ratingDeckId === deck.id && (
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        flexWrap: "wrap",
                      }}
                    >
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          onClick={() => setRatingScore(star)}
                          style={{
                            background: "none",
                            border: "none",
                            cursor: "pointer",
                            fontSize: "var(--font-size-lg)",
                            color: star <= ratingScore ? "#f59e0b" : "var(--color-text-secondary)",
                            padding: "0.125rem",
                          }}
                          aria-label={`Rate ${star} star${star > 1 ? "s" : ""}`}
                        >
                          ★
                        </button>
                      ))}
                      <GlassButton
                        variant="primary"
                        size="sm"
                        onClick={() => handleRate(deck.id)}
                        disabled={ratingScore < 1}
                      >
                        Submit
                      </GlassButton>
                      <GlassButton
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                          setRatingDeckId(null);
                          setRatingScore(0);
                        }}
                      >
                        Cancel
                      </GlassButton>
                    </div>
                  )}

                  <div
                    style={{
                      display: "flex",
                      gap: "0.5rem",
                      marginTop: "auto",
                    }}
                  >
                    <GlassButton
                      variant="primary"
                      size="sm"
                      loading={cloningId === deck.id}
                      onClick={() => handleClone(deck.id)}
                    >
                      Clone
                    </GlassButton>
                    <GlassButton
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        flashcardsApi.bookmarkDeck(deck.id).catch(() => {});
                      }}
                    >
                      🔖
                    </GlassButton>
                    {ratingDeckId !== deck.id && (
                      <GlassButton
                        variant="ghost"
                        size="sm"
                        onClick={() => setRatingDeckId(deck.id)}
                      >
                        Rate
                      </GlassButton>
                    )}
                    <GlassButton
                      variant="ghost"
                      size="sm"
                      onClick={async () => {
                        if (commentDeckId === deck.id) {
                          // Cancel any pending request
                          if (commentsAbortControllerRef.current) {
                            commentsAbortControllerRef.current.abort();
                          }
                          setCommentDeckId(null);
                          return;
                        }
                        
                        // Cancel previous request if any
                        if (commentsAbortControllerRef.current) {
                          commentsAbortControllerRef.current.abort();
                        }
                        
                        setCommentDeckId(deck.id);
                        setLoadingComments(true);
                        
                        // Create new abort controller for this request
                        const abortController = new AbortController();
                        commentsAbortControllerRef.current = abortController;
                        
                        try {
                          const res = await flashcardsApi.getComments(deck.id);
                          // Only update if this request wasn't aborted
                          if (!abortController.signal.aborted) {
                            setComments(res);
                          }
                        } catch (err) {
                          if (!abortController.signal.aborted) {
                            setComments([]);
                          }
                        } finally {
                          if (!abortController.signal.aborted) {
                            setLoadingComments(false);
                          }
                        }
                      }}
                    >
                      💬
                    </GlassButton>
                  </div>

                  {/* Inline comments */}
                  {commentDeckId === deck.id && (
                    <div style={{ marginTop: "0.75rem", borderTop: "1px solid var(--glass-border-medium)", paddingTop: "0.75rem" }}>
                      {loadingComments ? (
                        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>Loading...</p>
                      ) : (
                        <>
                          {comments.length === 0 && (
                            <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: "0 0 0.5rem" }}>No comments yet.</p>
                          )}
                          {comments.map((c) => (
                            <div key={c.id} style={{ marginBottom: "0.5rem" }}>
                              <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text)", margin: 0 }}>
                                <strong>{c.user_name}</strong>: {c.comment}
                              </p>
                            </div>
                          ))}
                          <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.5rem" }}>
                            <input
                              type="text"
                              value={newComment}
                              onChange={(e) => setNewComment(e.target.value)}
                              placeholder="Add a comment..."
                              style={{ flex: 1, padding: "0.375rem 0.5rem", background: "var(--glass-bg-subtle)", border: "1px solid var(--glass-border-medium)", borderRadius: "var(--radius-sm)", color: "var(--color-text)", fontSize: "var(--font-size-sm)" }}
                              onKeyDown={(e) => {
                                if (e.key === "Enter" && newComment.trim()) {
                                  flashcardsApi.postComment(deck.id, { body: newComment.trim() }).then((res) => {
                                    setComments((prev) => [...prev, { id: res.id, user_name: "You", comment: newComment.trim(), created_at: new Date().toISOString() }]);
                                    setNewComment("");
                                  }).catch(() => {});
                                }
                              }}
                            />
                            <GlassButton
                              variant="primary"
                              size="sm"
                              disabled={!newComment.trim()}
                              onClick={() => {
                                flashcardsApi.postComment(deck.id, { body: newComment.trim() }).then((res) => {
                                  setComments((prev) => [...prev, { id: res.id, user_name: "You", comment: newComment.trim(), created_at: new Date().toISOString() }]);
                                  setNewComment("");
                                }).catch(() => {});
                              }}
                            >
                              Post
                            </GlassButton>
                          </div>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </GlassCard>
            ))}
          </div>
        )}
        </CrossfadeContent>
      </main>
    </PageTransition>
  );
}
