import { useState } from "react";
import { GlassButton } from "./GlassButton";
import { learningTechniquesApi } from "../api/learningTechniques";

interface ElaborativePromptProps {
  questionId: number;
  /** Previously saved note for this question (shown on re-encounter) */
  previousNote?: string | null;
}

/**
 * "Why does this make sense?" elaborative interrogation prompt.
 * Shown after incorrect answers. Persists personal notes without grading.
 * Requirements: 22.1, 22.2, 22.5
 */
export function ElaborativePrompt({ questionId, previousNote }: ElaborativePromptProps) {
  const [expanded, setExpanded] = useState(false);
  const [noteText, setNoteText] = useState("");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  async function handleSave() {
    if (!noteText.trim()) return;
    setSaving(true);
    try {
      await learningTechniquesApi.createNote(questionId, noteText.trim());
      setSaved(true);
    } catch {
      // Silent fail — non-critical
    } finally {
      setSaving(false);
    }
  }

  // Show previous note if available
  if (previousNote && !expanded) {
    return (
      <div
        style={{
          marginTop: "var(--space-3)",
          padding: "var(--space-3)",
          borderRadius: "var(--radius-sm)",
          background: "rgba(212,165,116,0.06)",
          borderLeft: "3px solid var(--color-accent)",
        }}
      >
        <p style={{ margin: 0, fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-accent)", marginBottom: "var(--space-1)" }}>
          📝 Your previous note:
        </p>
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", fontStyle: "italic" }}>
          "{previousNote}"
        </p>
        <button
          onClick={() => setExpanded(true)}
          style={{
            marginTop: "var(--space-2)",
            fontSize: "var(--font-size-xs)",
            color: "var(--color-accent)",
            background: "none",
            border: "none",
            cursor: "pointer",
            padding: 0,
          }}
        >
          Update note →
        </button>
      </div>
    );
  }

  if (!expanded) {
    return (
      <button
        onClick={() => setExpanded(true)}
        style={{
          marginTop: "var(--space-3)",
          display: "block",
          width: "100%",
          padding: "var(--space-2) var(--space-3)",
          borderRadius: "var(--radius-sm)",
          border: "1px dashed var(--glass-border-light)",
          background: "transparent",
          color: "var(--color-text-muted)",
          fontSize: "var(--font-size-xs)",
          cursor: "pointer",
          textAlign: "left",
        }}
      >
        💭 Why does this make sense? Write a note to yourself...
      </button>
    );
  }

  if (saved) {
    return (
      <div
        style={{
          marginTop: "var(--space-3)",
          padding: "var(--space-3)",
          borderRadius: "var(--radius-sm)",
          background: "rgba(100,255,100,0.05)",
          borderLeft: "3px solid var(--color-success)",
        }}
      >
        <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-success)" }}>
          ✓ Note saved — you'll see it next time you encounter this question.
        </p>
      </div>
    );
  }

  return (
    <div
      style={{
        marginTop: "var(--space-3)",
        padding: "var(--space-3)",
        borderRadius: "var(--radius-md)",
        border: "1px solid var(--glass-border-light)",
      }}
    >
      <p style={{ margin: "0 0 var(--space-2)", fontSize: "var(--font-size-xs)", fontWeight: 600, color: "var(--color-text-secondary)" }}>
        💭 Why does this make sense? (no grading — just for you)
      </p>
      <textarea
        value={noteText}
        onChange={(e) => setNoteText(e.target.value)}
        maxLength={500}
        placeholder="Write in your own words why the correct answer makes sense..."
        aria-label="Personal elaboration note"
        style={{
          width: "100%",
          minHeight: 60,
          padding: "var(--space-2)",
          borderRadius: "var(--radius-sm)",
          border: "1px solid var(--glass-border-light)",
          background: "var(--glass-bg-subtle)",
          color: "var(--color-text)",
          fontSize: "var(--font-size-sm)",
          resize: "vertical",
          fontFamily: "inherit",
        }}
      />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "var(--space-2)" }}>
        <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          {noteText.length}/500
        </span>
        <div style={{ display: "flex", gap: "var(--space-2)" }}>
          <GlassButton variant="ghost" size="sm" onClick={() => setExpanded(false)}>
            Cancel
          </GlassButton>
          <GlassButton variant="primary" size="sm" onClick={handleSave} disabled={saving || !noteText.trim()}>
            {saving ? "Saving..." : "Save"}
          </GlassButton>
        </div>
      </div>
    </div>
  );
}
