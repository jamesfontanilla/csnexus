import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { flashcardsApi, Deck } from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { PageTransition } from "../../components/PageTransition";

interface GeneratedCard {
  front: string;
  back: string;
  card_type: string;
  difficulty: string;
  selected: boolean;
}

export function GenerateCards() {
  const navigate = useNavigate();
  const [lessonContent, setLessonContent] = useState("");
  const [cardCount, setCardCount] = useState(25);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cards, setCards] = useState<GeneratedCard[]>([]);
  const [termsExtracted, setTermsExtracted] = useState(0);

  // Deck selection for adding cards
  const [decks, setDecks] = useState<Deck[]>([]);
  const [selectedDeckId, setSelectedDeckId] = useState<number | null>(null);
  const [adding, setAdding] = useState(false);
  const [addSuccess, setAddSuccess] = useState<string | null>(null);

  useEffect(() => {
    flashcardsApi.getDecks().then(setDecks).catch(() => {});
  }, []);

  async function handleGenerate() {
    if (lessonContent.trim().length < 50) {
      setError("Lesson content must be at least 50 characters.");
      return;
    }
    setGenerating(true);
    setError(null);
    setCards([]);
    setAddSuccess(null);
    try {
      const result = await flashcardsApi.generateCards({
        lesson_content: lessonContent,
        lesson_id: 0,
        requested_card_count: cardCount,
      });
      setCards(result.cards.map((c) => ({ ...c, selected: true })));
      setTermsExtracted(result.terms_extracted);
    } catch (err: any) {
      setError(err?.message || "Generation failed. Try adding more content.");
    } finally {
      setGenerating(false);
    }
  }

  function toggleCard(index: number) {
    setCards((prev) =>
      prev.map((c, i) => (i === index ? { ...c, selected: !c.selected } : c))
    );
  }

  function selectAll() {
    setCards((prev) => prev.map((c) => ({ ...c, selected: true })));
  }

  function deselectAll() {
    setCards((prev) => prev.map((c) => ({ ...c, selected: false })));
  }

  async function handleAddToDeck() {
    if (!selectedDeckId) return;
    const selected = cards.filter((c) => c.selected);
    if (selected.length === 0) return;

    setAdding(true);
    setError(null);
    try {
      for (const card of selected) {
        await flashcardsApi.createCard(selectedDeckId, {
          front: card.front,
          back: card.back,
          card_type: card.card_type as any,
        });
      }
      setAddSuccess(`Added ${selected.length} cards to deck.`);
      setCards([]);
    } catch (err: any) {
      setError(err?.message || "Failed to add cards to deck.");
    } finally {
      setAdding(false);
    }
  }

  const selectedCount = cards.filter((c) => c.selected).length;

  const difficultyColor: Record<string, string> = {
    easy: "#10b981",
    medium: "#f59e0b",
    hard: "#ef4444",
  };

  return (
    <PageTransition>
      <main className="page container">
        <GlassButton
          variant="ghost"
          size="sm"
          onClick={() => navigate("/flashcards")}
          style={{ marginBottom: "1.5rem" }}
        >
          ← Back
        </GlassButton>

        <h1 style={{ fontSize: "var(--font-size-2xl)", color: "var(--color-text)", marginBottom: "1.5rem" }}>
          Generate Flashcards
        </h1>

        {/* Input section */}
        {cards.length === 0 && (
          <GlassCard style={{ marginBottom: "1.5rem" }}>
            <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
              <div>
                <label style={{ display: "block", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "0.375rem", fontWeight: 500 }}>
                  Paste lesson content (minimum 50 characters)
                </label>
                <textarea
                  value={lessonContent}
                  onChange={(e) => setLessonContent(e.target.value)}
                  placeholder="Paste your lesson text here. The generator will extract terms and create flashcards automatically..."
                  rows={10}
                  style={{
                    width: "100%",
                    padding: "0.75rem",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-medium)",
                    borderRadius: "var(--radius-sm)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                    resize: "vertical",
                  }}
                />
                <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: "0.25rem 0 0" }}>
                  {lessonContent.length} characters
                </p>
              </div>
              <div>
                <label style={{ display: "block", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", marginBottom: "0.375rem", fontWeight: 500 }}>
                  Cards to generate: {cardCount}
                </label>
                <input
                  type="range"
                  min={10}
                  max={50}
                  value={cardCount}
                  onChange={(e) => setCardCount(Number(e.target.value))}
                  style={{ width: "100%" }}
                />
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
                  <span>10</span>
                  <span>50</span>
                </div>
              </div>
              <GlassButton variant="primary" onClick={handleGenerate} loading={generating} disabled={lessonContent.trim().length < 50}>
                Generate Cards
              </GlassButton>
            </div>
          </GlassCard>
        )}

        {/* Error */}
        {error && (
          <GlassCard style={{ marginBottom: "1rem", background: "rgba(239,68,68,0.1)" }}>
            <p style={{ color: "var(--color-text)", margin: 0 }}>{error}</p>
          </GlassCard>
        )}

        {/* Success */}
        {addSuccess && (
          <GlassCard style={{ marginBottom: "1rem", background: "rgba(16,185,129,0.1)" }}>
            <p style={{ color: "var(--color-text)", margin: 0 }}>{addSuccess}</p>
          </GlassCard>
        )}

        {/* Generated cards */}
        {cards.length > 0 && (
          <>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "1rem", flexWrap: "wrap", gap: "0.75rem" }}>
              <p style={{ fontSize: "var(--font-size-base)", color: "var(--color-text)", margin: 0 }}>
                {termsExtracted} terms extracted · {cards.length} cards generated · {selectedCount} selected
              </p>
              <div style={{ display: "flex", gap: "0.5rem" }}>
                <GlassButton variant="ghost" size="sm" onClick={selectAll}>Select All</GlassButton>
                <GlassButton variant="ghost" size="sm" onClick={deselectAll}>Deselect All</GlassButton>
                <GlassButton variant="ghost" size="sm" onClick={() => setCards([])}>Clear</GlassButton>
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem", maxHeight: "50vh", overflowY: "auto", marginBottom: "1.5rem" }}>
              {cards.map((card, i) => (
                <GlassCard
                  key={i}
                  style={{ opacity: card.selected ? 1 : 0.5, cursor: "pointer" }}
                  onClick={() => toggleCard(i)}
                >
                  <div style={{ display: "flex", alignItems: "flex-start", gap: "0.75rem" }}>
                    <input
                      type="checkbox"
                      checked={card.selected}
                      onChange={() => toggleCard(i)}
                      onClick={(e) => e.stopPropagation()}
                      style={{ marginTop: "0.25rem", width: "1.125rem", height: "1.125rem" }}
                    />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ fontSize: "var(--font-size-base)", color: "var(--color-text)", margin: "0 0 0.25rem", fontWeight: 500 }}>
                        {card.front}
                      </p>
                      <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: "0 0 0.5rem" }}>
                        {card.back}
                      </p>
                      <div style={{ display: "flex", gap: "0.5rem" }}>
                        <span style={{ fontSize: "var(--font-size-sm)", padding: "0.125rem 0.5rem", borderRadius: "var(--radius-sm)", background: "var(--glass-bg-subtle)", color: "var(--color-accent)", textTransform: "capitalize" }}>
                          {card.card_type}
                        </span>
                        <span style={{ fontSize: "var(--font-size-sm)", padding: "0.125rem 0.5rem", borderRadius: "var(--radius-sm)", background: "var(--glass-bg-subtle)", color: difficultyColor[card.difficulty] || "var(--color-text-secondary)", textTransform: "capitalize" }}>
                          {card.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              ))}
            </div>

            {/* Add to deck */}
            <GlassCard>
              <h3 style={{ fontSize: "var(--font-size-base)", color: "var(--color-text)", margin: "0 0 1rem" }}>
                Add selected cards to a deck
              </h3>
              <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", alignItems: "center" }}>
                <select
                  value={selectedDeckId ?? ""}
                  onChange={(e) => setSelectedDeckId(e.target.value ? Number(e.target.value) : null)}
                  style={{
                    flex: "1 1 200px",
                    padding: "0.625rem",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-medium)",
                    borderRadius: "var(--radius-sm)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                  }}
                >
                  <option value="">Select a deck...</option>
                  {decks.map((d) => (
                    <option key={d.id} value={d.id}>{d.title}</option>
                  ))}
                </select>
                <GlassButton
                  variant="primary"
                  onClick={handleAddToDeck}
                  loading={adding}
                  disabled={!selectedDeckId || selectedCount === 0}
                >
                  Add {selectedCount} Cards
                </GlassButton>
              </div>
            </GlassCard>
          </>
        )}
      </main>
    </PageTransition>
  );
}
