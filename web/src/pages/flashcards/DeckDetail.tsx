import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  flashcardsApi,
  Deck,
  FlashCard,
  CardCreate,
  CardType,
} from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

const CARD_TYPES: CardType[] = [
  "basic",
  "reverse",
  "cloze",
  "mcq",
  "true_false",
  "matching",
  "sequence",
];

export function DeckDetail() {
  const { deckId } = useParams<{ deckId: string }>();
  const navigate = useNavigate();

  const [deck, setDeck] = useState<Deck | null>(null);
  const [cards, setCards] = useState<FlashCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Add card form
  const [showAddForm, setShowAddForm] = useState(false);
  const [newFront, setNewFront] = useState("");
  const [newBack, setNewBack] = useState("");
  const [newType, setNewType] = useState<CardType>("basic");
  const [addLoading, setAddLoading] = useState(false);

  // Edit state
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editFront, setEditFront] = useState("");
  const [editBack, setEditBack] = useState("");
  const [editType, setEditType] = useState<CardType>("basic");

  // Deck edit state
  const [editingDeck, setEditingDeck] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editVisibility, setEditVisibility] = useState("");
  const [savingDeck, setSavingDeck] = useState(false);

  useEffect(() => {
    async function load() {
      if (!deckId) return;
      try {
        const id = parseInt(deckId, 10);
        const [deckRes, cardsRes] = await Promise.all([
          flashcardsApi.getDeck(id),
          flashcardsApi.getDeckCards(id),
        ]);
        setDeck(deckRes);
        setCards(cardsRes);
      } catch (err) {
        setError("Failed to load deck. Please try again.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [deckId]);

  async function handleAddCard(e: React.FormEvent) {
    e.preventDefault();
    if (!deckId || !newFront.trim() || !newBack.trim()) return;

    setAddLoading(true);
    try {
      const data: CardCreate = {
        front: newFront.trim(),
        back: newBack.trim(),
        card_type: newType,
      };
      const card = await flashcardsApi.createCard(parseInt(deckId, 10), data);
      setCards((prev) => [...prev, card]);
      setNewFront("");
      setNewBack("");
      setNewType("basic");
      setShowAddForm(false);
    } catch (err) {
      setError("Failed to add card.");
    } finally {
      setAddLoading(false);
    }
  }

  function startEdit(card: FlashCard) {
    setEditingId(card.id);
    setEditFront(card.front);
    setEditBack(card.back);
    setEditType(card.card_type);
  }

  async function handleSaveEdit(cardId: number) {
    if (!deckId) return;
    try {
      const updated = await flashcardsApi.updateCard(
        parseInt(deckId, 10),
        cardId,
        { front: editFront, back: editBack, card_type: editType }
      );
      setCards((prev) => prev.map((c) => (c.id === cardId ? updated : c)));
      setEditingId(null);
    } catch (err) {
      setError("Failed to update card.");
    }
  }

  async function handleDeleteCard(cardId: number) {
    if (!deckId) return;
    try {
      await flashcardsApi.deleteCard(parseInt(deckId, 10), cardId);
      setCards((prev) => prev.filter((c) => c.id !== cardId));
    } catch (err) {
      setError("Failed to delete card.");
    }
  }

  function handleStudy() {
    if (!deckId) return;
    navigate("/flashcards/study", { state: { deckIds: [parseInt(deckId, 10)] } });
  }

  if (loading) {
    return (
      <PageTransition>
        <main className="page container">
          <GlassSkeleton height="2rem" width="60%" />
          <div style={{ marginTop: "1rem" }}>
            <GlassSkeleton height="1rem" width="40%" />
          </div>
          <div style={{ marginTop: "2rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
            {[1, 2, 3].map((i) => (
              <GlassSkeleton key={i} height="5rem" />
            ))}
          </div>
        </main>
      </PageTransition>
    );
  }

  if (error && !deck) {
    return (
      <PageTransition>
        <main className="page container">
          <GlassCard>
            <p style={{ color: "var(--color-text)", textAlign: "center" }}>
              {error}
            </p>
            <div style={{ textAlign: "center", marginTop: "1rem" }}>
              <GlassButton onClick={() => navigate("/flashcards")}>
                Back to Flashcards
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
        {/* Back nav */}
        <GlassButton
          variant="ghost"
          size="sm"
          onClick={() => navigate("/flashcards")}
          style={{ marginBottom: "1.5rem" }}
        >
          ← Back
        </GlassButton>

        {/* Deck Header */}
        {deck && (
          <div style={{ marginBottom: "2rem" }}>
            <div
              style={{
                display: "flex",
                alignItems: "flex-start",
                justifyContent: "space-between",
                flexWrap: "wrap",
                gap: "1rem",
              }}
            >
              <div>
                <h1
                  style={{
                    fontSize: "var(--font-size-2xl)",
                    color: "var(--color-text)",
                    margin: "0 0 0.5rem",
                  }}
                >
                  {deck.title}
                </h1>
                {deck.description && (
                  <p
                    style={{
                      fontSize: "var(--font-size-base)",
                      color: "var(--color-text-secondary)",
                      margin: "0 0 0.75rem",
                    }}
                  >
                    {deck.description}
                  </p>
                )}
                <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
                  <span
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-accent)",
                      background: "var(--glass-bg-subtle)",
                      padding: "0.125rem 0.5rem",
                      borderRadius: "var(--radius-sm)",
                      textTransform: "capitalize",
                    }}
                  >
                    {deck.category}
                  </span>
                  <span
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      background: "var(--glass-bg-subtle)",
                      padding: "0.125rem 0.5rem",
                      borderRadius: "var(--radius-sm)",
                      textTransform: "capitalize",
                    }}
                  >
                    {deck.visibility}
                  </span>
                </div>
              </div>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <GlassButton variant="primary" onClick={handleStudy}>
                  Study This Deck
                </GlassButton>
                <GlassButton
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setEditingDeck(true);
                    setEditTitle(deck.title);
                    setEditDescription(deck.description || "");
                    setEditVisibility(deck.visibility);
                  }}
                >
                  Edit
                </GlassButton>
              </div>
            </div>

            {/* Deck edit form */}
            {editingDeck && (
              <GlassCard style={{ marginTop: "1rem" }}>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    placeholder="Deck title"
                    style={{ width: "100%", padding: "0.625rem", background: "var(--glass-bg-subtle)", border: "1px solid var(--glass-border-medium)", borderRadius: "var(--radius-sm)", color: "var(--color-text)", fontSize: "var(--font-size-base)" }}
                  />
                  <textarea
                    value={editDescription}
                    onChange={(e) => setEditDescription(e.target.value)}
                    placeholder="Description"
                    rows={2}
                    style={{ width: "100%", padding: "0.625rem", background: "var(--glass-bg-subtle)", border: "1px solid var(--glass-border-medium)", borderRadius: "var(--radius-sm)", color: "var(--color-text)", fontSize: "var(--font-size-base)", resize: "vertical" }}
                  />
                  <select
                    value={editVisibility}
                    onChange={(e) => setEditVisibility(e.target.value)}
                    style={{ padding: "0.625rem", background: "var(--glass-bg-subtle)", border: "1px solid var(--glass-border-medium)", borderRadius: "var(--radius-sm)", color: "var(--color-text)", fontSize: "var(--font-size-base)" }}
                  >
                    <option value="private">Private</option>
                    <option value="public">Public</option>
                    <option value="unlisted">Unlisted</option>
                  </select>
                  <div style={{ display: "flex", gap: "0.5rem" }}>
                    <GlassButton
                      variant="primary"
                      size="sm"
                      loading={savingDeck}
                      onClick={async () => {
                        if (!deckId) return;
                        setSavingDeck(true);
                        try {
                          const updated = await flashcardsApi.updateDeck(parseInt(deckId, 10), {
                            title: editTitle,
                            description: editDescription || undefined,
                            visibility: editVisibility,
                          });
                          setDeck(updated);
                          setEditingDeck(false);
                        } catch { setError("Failed to update deck."); }
                        finally { setSavingDeck(false); }
                      }}
                    >
                      Save
                    </GlassButton>
                    <GlassButton variant="ghost" size="sm" onClick={() => setEditingDeck(false)}>
                      Cancel
                    </GlassButton>
                  </div>
                </div>
              </GlassCard>
            )}
          </div>
        )}

        {/* Error banner */}
        {error && (
          <GlassCard style={{ marginBottom: "1rem", background: "rgba(239,68,68,0.1)" }}>
            <p style={{ color: "var(--color-text)", margin: 0 }}>{error}</p>
          </GlassCard>
        )}

        {/* Add Card Section */}
        <div style={{ marginBottom: "1.5rem" }}>
          {!showAddForm ? (
            <GlassButton
              variant="secondary"
              size="sm"
              onClick={() => setShowAddForm(true)}
            >
              + Add Card
            </GlassButton>
          ) : (
            <GlassCard>
              <form onSubmit={handleAddCard}>
                <h3
                  style={{
                    fontSize: "var(--font-size-base)",
                    color: "var(--color-text)",
                    margin: "0 0 1rem",
                  }}
                >
                  New Card
                </h3>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                  <textarea
                    placeholder="Front (question)"
                    value={newFront}
                    onChange={(e) => setNewFront(e.target.value)}
                    required
                    rows={2}
                    style={{
                      width: "100%",
                      padding: "0.625rem",
                      background: "var(--glass-bg-subtle)",
                      border: "1px solid var(--glass-border-medium)",
                      borderRadius: "var(--radius-sm)",
                      color: "var(--color-text)",
                      fontSize: "var(--font-size-base)",
                      resize: "vertical",
                    }}
                  />
                  <textarea
                    placeholder="Back (answer)"
                    value={newBack}
                    onChange={(e) => setNewBack(e.target.value)}
                    required
                    rows={2}
                    style={{
                      width: "100%",
                      padding: "0.625rem",
                      background: "var(--glass-bg-subtle)",
                      border: "1px solid var(--glass-border-medium)",
                      borderRadius: "var(--radius-sm)",
                      color: "var(--color-text)",
                      fontSize: "var(--font-size-base)",
                      resize: "vertical",
                    }}
                  />
                  <select
                    value={newType}
                    onChange={(e) => setNewType(e.target.value as CardType)}
                    style={{
                      padding: "0.625rem",
                      background: "var(--glass-bg-subtle)",
                      border: "1px solid var(--glass-border-medium)",
                      borderRadius: "var(--radius-sm)",
                      color: "var(--color-text)",
                      fontSize: "var(--font-size-base)",
                    }}
                  >
                    {CARD_TYPES.map((t) => (
                      <option key={t} value={t}>
                        {t.replace("_", " ")}
                      </option>
                    ))}
                  </select>
                  <div style={{ display: "flex", gap: "0.75rem" }}>
                    <GlassButton type="submit" variant="primary" size="sm" loading={addLoading}>
                      Add Card
                    </GlassButton>
                    <GlassButton
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowAddForm(false)}
                    >
                      Cancel
                    </GlassButton>
                  </div>
                </div>
              </form>
            </GlassCard>
          )}
        </div>

        {/* Card List */}
        <h2
          style={{
            fontSize: "var(--font-size-lg)",
            color: "var(--color-text)",
            margin: "0 0 1rem",
          }}
        >
          Cards ({cards.length})
        </h2>

        {cards.length === 0 ? (
          <GlassCard>
            <p
              style={{
                color: "var(--color-text-secondary)",
                textAlign: "center",
                margin: 0,
              }}
            >
              No cards in this deck yet. Add your first card above.
            </p>
          </GlassCard>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {cards.map((card) => (
              <GlassCard key={card.id}>
                {editingId === card.id ? (
                  <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                    <textarea
                      value={editFront}
                      onChange={(e) => setEditFront(e.target.value)}
                      rows={2}
                      style={{
                        width: "100%",
                        padding: "0.625rem",
                        background: "var(--glass-bg-subtle)",
                        border: "1px solid var(--glass-border-medium)",
                        borderRadius: "var(--radius-sm)",
                        color: "var(--color-text)",
                        fontSize: "var(--font-size-base)",
                        resize: "vertical",
                      }}
                    />
                    <textarea
                      value={editBack}
                      onChange={(e) => setEditBack(e.target.value)}
                      rows={2}
                      style={{
                        width: "100%",
                        padding: "0.625rem",
                        background: "var(--glass-bg-subtle)",
                        border: "1px solid var(--glass-border-medium)",
                        borderRadius: "var(--radius-sm)",
                        color: "var(--color-text)",
                        fontSize: "var(--font-size-base)",
                        resize: "vertical",
                      }}
                    />
                    <select
                      value={editType}
                      onChange={(e) => setEditType(e.target.value as CardType)}
                      style={{
                        padding: "0.625rem",
                        background: "var(--glass-bg-subtle)",
                        border: "1px solid var(--glass-border-medium)",
                        borderRadius: "var(--radius-sm)",
                        color: "var(--color-text)",
                        fontSize: "var(--font-size-base)",
                      }}
                    >
                      {CARD_TYPES.map((t) => (
                        <option key={t} value={t}>
                          {t.replace("_", " ")}
                        </option>
                      ))}
                    </select>
                    <div style={{ display: "flex", gap: "0.75rem" }}>
                      <GlassButton
                        variant="primary"
                        size="sm"
                        onClick={() => handleSaveEdit(card.id)}
                      >
                        Save
                      </GlassButton>
                      <GlassButton
                        variant="ghost"
                        size="sm"
                        onClick={() => setEditingId(null)}
                      >
                        Cancel
                      </GlassButton>
                    </div>
                  </div>
                ) : (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      gap: "1rem",
                    }}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p
                        style={{
                          fontSize: "var(--font-size-base)",
                          color: "var(--color-text)",
                          margin: "0 0 0.25rem",
                          fontWeight: 500,
                        }}
                      >
                        {card.front}
                      </p>
                      <p
                        style={{
                          fontSize: "var(--font-size-sm)",
                          color: "var(--color-text-secondary)",
                          margin: "0 0 0.25rem",
                        }}
                      >
                        {card.back}
                      </p>
                      <span
                        style={{
                          fontSize: "var(--font-size-sm)",
                          color: "var(--color-accent)",
                          textTransform: "capitalize",
                        }}
                      >
                        {card.card_type.replace("_", " ")}
                      </span>
                    </div>
                    <div style={{ display: "flex", gap: "0.5rem", flexShrink: 0 }}>
                      <GlassButton
                        variant="ghost"
                        size="sm"
                        onClick={() => startEdit(card)}
                      >
                        Edit
                      </GlassButton>
                      <GlassButton
                        variant="danger"
                        size="sm"
                        onClick={() => handleDeleteCard(card.id)}
                      >
                        Delete
                      </GlassButton>
                    </div>
                  </div>
                )}
              </GlassCard>
            ))}
          </div>
        )}
      </main>
    </PageTransition>
  );
}
