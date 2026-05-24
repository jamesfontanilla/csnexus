import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { flashcardsApi, DeckCreate, DeckCategory, DeckVisibility } from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { PageTransition } from "../../components/PageTransition";

const CATEGORIES: { value: DeckCategory; label: string }[] = [
  { value: "verbal", label: "Verbal" },
  { value: "numerical", label: "Numerical" },
  { value: "analytical", label: "Analytical" },
];

const VISIBILITIES: { value: DeckVisibility; label: string; desc: string }[] = [
  { value: "private", label: "Private", desc: "Only you can see this deck" },
  { value: "public", label: "Public", desc: "Visible in the marketplace" },
  { value: "unlisted", label: "Unlisted", desc: "Accessible via link only" },
];

export function CreateDeck() {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState<DeckCategory>("verbal");
  const [visibility, setVisibility] = useState<DeckVisibility>("private");
  const [tagsInput, setTagsInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    setError(null);

    const tags = tagsInput
      .split(",")
      .map((t) => t.trim())
      .filter((t) => t.length > 0);

    const data: DeckCreate = {
      title: title.trim(),
      category,
      visibility,
      description: description.trim() || undefined,
      tags: tags.length > 0 ? tags : undefined,
    };

    try {
      const deck = await flashcardsApi.createDeck(data);
      navigate(`/flashcards/decks/${deck.id}`);
    } catch (err: any) {
      setError(err?.message || "Failed to create deck. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 600 }}>
        <GlassButton
          variant="ghost"
          size="sm"
          onClick={() => navigate("/flashcards")}
          style={{ marginBottom: "1.5rem" }}
        >
          ← Back
        </GlassButton>

        <h1
          style={{
            fontSize: "var(--font-size-2xl)",
            color: "var(--color-text)",
            marginBottom: "1.5rem",
          }}
        >
          Create New Deck
        </h1>

        {error && (
          <GlassCard style={{ marginBottom: "1rem", background: "rgba(239,68,68,0.1)" }}>
            <p style={{ color: "var(--color-text)", margin: 0 }}>{error}</p>
          </GlassCard>
        )}

        <GlassCard>
          <form onSubmit={handleSubmit}>
            <div style={{ display: "flex", flexDirection: "column", gap: "1.25rem" }}>
              {/* Title */}
              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    marginBottom: "0.375rem",
                    fontWeight: 500,
                  }}
                >
                  Title *
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Grammar Rules"
                  required
                  maxLength={255}
                  style={{
                    width: "100%",
                    padding: "0.625rem",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-medium)",
                    borderRadius: "var(--radius-sm)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                  }}
                />
              </div>

              {/* Description */}
              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    marginBottom: "0.375rem",
                    fontWeight: 500,
                  }}
                >
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="What's this deck about?"
                  rows={3}
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
              </div>

              {/* Category */}
              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    marginBottom: "0.375rem",
                    fontWeight: 500,
                  }}
                >
                  Category *
                </label>
                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                  {CATEGORIES.map((c) => (
                    <GlassButton
                      key={c.value}
                      type="button"
                      variant={category === c.value ? "primary" : "ghost"}
                      size="sm"
                      onClick={() => setCategory(c.value)}
                    >
                      {c.label}
                    </GlassButton>
                  ))}
                </div>
              </div>

              {/* Visibility */}
              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    marginBottom: "0.375rem",
                    fontWeight: 500,
                  }}
                >
                  Visibility
                </label>
                <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                  {VISIBILITIES.map((v) => (
                    <label
                      key={v.value}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                        cursor: "pointer",
                        padding: "0.5rem",
                        borderRadius: "var(--radius-sm)",
                        background: visibility === v.value ? "var(--glass-bg-subtle)" : "transparent",
                        border: visibility === v.value ? "1px solid var(--color-accent)" : "1px solid transparent",
                      }}
                    >
                      <input
                        type="radio"
                        name="visibility"
                        value={v.value}
                        checked={visibility === v.value}
                        onChange={() => setVisibility(v.value)}
                        style={{ accentColor: "var(--color-accent)" }}
                      />
                      <div>
                        <span style={{ fontSize: "var(--font-size-base)", color: "var(--color-text)" }}>
                          {v.label}
                        </span>
                        <p style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", margin: "0.125rem 0 0" }}>
                          {v.desc}
                        </p>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Tags */}
              <div>
                <label
                  style={{
                    display: "block",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                    marginBottom: "0.375rem",
                    fontWeight: 500,
                  }}
                >
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  value={tagsInput}
                  onChange={(e) => setTagsInput(e.target.value)}
                  placeholder="e.g. grammar, tenses, verbs"
                  style={{
                    width: "100%",
                    padding: "0.625rem",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-medium)",
                    borderRadius: "var(--radius-sm)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                  }}
                />
              </div>

              {/* Submit */}
              <div style={{ display: "flex", gap: "1rem", paddingTop: "0.5rem" }}>
                <GlassButton type="submit" variant="primary" loading={loading}>
                  Create Deck
                </GlassButton>
                <GlassButton
                  type="button"
                  variant="ghost"
                  onClick={() => navigate("/flashcards")}
                >
                  Cancel
                </GlassButton>
              </div>
            </div>
          </form>
        </GlassCard>
      </main>
    </PageTransition>
  );
}
