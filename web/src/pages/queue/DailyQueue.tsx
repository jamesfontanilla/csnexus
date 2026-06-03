import { useNavigate } from "react-router-dom";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassProgressBar } from "../../components/GlassProgressBar";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { GradientText } from "../../components/GradientText";
import { EmptyState } from "../../components/EmptyState";
import { PageTransition } from "../../components/PageTransition";
import { useDailyQueue } from "../../hooks/useDailyQueue";
import type { QueueItem } from "../../api/queue";

const ITEM_TYPE_ICONS: Record<string, string> = {
  flashcard_review: "🃏",
  quiz_practice: "✅",
  new_content: "📚",
};

const ITEM_TYPE_LABELS: Record<string, string> = {
  flashcard_review: "Flashcard Review",
  quiz_practice: "Quiz Practice",
  new_content: "New Lesson",
};

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${seconds}s`;
  const mins = Math.round(seconds / 60);
  return `${mins} min`;
}

export function DailyQueue() {
  const navigate = useNavigate();
  const {
    queue,
    preferences,
    loading,
    error,
    completeItem,
    regenerate,
    updatePreferences,
  } = useDailyQueue();

  if (loading) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 640 }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", marginBottom: "var(--space-6)" }}>
            <GradientText variant="accent">Today's Study Queue</GradientText>
          </h1>
          <GlassSkeleton variant="card" />
          <div style={{ display: "grid", gap: "var(--space-3)", marginTop: "var(--space-4)" }}>
            {[1, 2, 3].map((i) => <GlassSkeleton key={i} variant="card" />)}
          </div>
        </main>
      </PageTransition>
    );
  }

  if (error && !queue) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 640 }}>
          <EmptyState
            icon="⚠️"
            title="Queue Unavailable"
            description={error}
          />
        </main>
      </PageTransition>
    );
  }

  if (!queue || queue.items.length === 0) {
    return (
      <PageTransition>
        <main className="page container" style={{ maxWidth: 640 }}>
          <EmptyState
            icon="🎉"
            title="All Done for Today!"
            description="You've completed your daily study session. Come back tomorrow for a fresh queue."
          />
        </main>
      </PageTransition>
    );
  }

  const totalItems = queue.items_completed + queue.items_remaining;
  const progress = totalItems > 0 ? (queue.items_completed / totalItems) * 100 : 0;
  const firstUncompleted = queue.items.find((item) => item.completed_at === null);

  function handleStartItem(item: QueueItem) {
    switch (item.item_type) {
      case "flashcard_review": {
        const cardIds = (item.payload.card_ids as number[]) || [];
        // Navigate to flashcard study with the specific cards
        navigate(`/flashcards/study?cards=${cardIds.join(",")}`);
        break;
      }
      case "quiz_practice": {
        const subtopicId = item.payload.subtopic_id as number;
        navigate(`/quiz/subtopic/${subtopicId}`);
        break;
      }
      case "new_content": {
        const subtopicId = item.payload.subtopic_id as number;
        navigate(`/subtopics/${subtopicId}/lesson`);
        break;
      }
    }
  }

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 640 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "var(--space-6)" }}>
          <h1 style={{ fontFamily: "var(--font-display)", letterSpacing: "-0.02em", margin: 0 }}>
            <GradientText variant="accent">Today's Study Queue</GradientText>
          </h1>
          <GlassButton variant="ghost" size="sm" onClick={() => regenerate()}>
            🔄 Regenerate
          </GlassButton>
        </div>

        {/* Progress summary */}
        <GlassCard style={{ marginBottom: "var(--space-5)" }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "var(--space-3)" }}>
            <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
              {queue.items_completed} of {totalItems} items completed
            </span>
            <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
              ~{formatDuration(queue.total_estimated_seconds)} total
            </span>
          </div>
          <GlassProgressBar value={progress} max={100} />

          {/* Time budget selector */}
          <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginTop: "var(--space-4)" }}>
            <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
              Budget:
            </span>
            {([15, 30, 60] as const).map((mins) => (
              <button
                key={mins}
                onClick={() => updatePreferences(mins)}
                aria-pressed={preferences?.time_budget_minutes === mins}
                style={{
                  padding: "var(--space-1) var(--space-2)",
                  borderRadius: "var(--radius-sm)",
                  border: `1px solid ${preferences?.time_budget_minutes === mins ? "var(--color-accent)" : "var(--glass-border-light)"}`,
                  background: preferences?.time_budget_minutes === mins ? "var(--color-accent-subtle)" : "transparent",
                  color: "var(--color-text)",
                  fontSize: "var(--font-size-xs)",
                  cursor: "pointer",
                }}
              >
                {mins}m
              </button>
            ))}
          </div>
        </GlassCard>

        {/* Start button */}
        {firstUncompleted && (
          <div style={{ marginBottom: "var(--space-5)", textAlign: "center" }}>
            <GlassButton
              variant="primary"
              size="lg"
              onClick={() => handleStartItem(firstUncompleted)}
            >
              ▶ Start Next: {ITEM_TYPE_LABELS[firstUncompleted.item_type]}
            </GlassButton>
          </div>
        )}

        {/* Queue items */}
        <div style={{ display: "grid", gap: "var(--space-3)" }}>
          {queue.items.map((item) => (
            <QueueItemCard
              key={item.id}
              item={item}
              onStart={() => handleStartItem(item)}
              onComplete={() => completeItem(item.id)}
            />
          ))}
        </div>
      </main>
    </PageTransition>
  );
}

interface QueueItemCardProps {
  item: QueueItem;
  onStart: () => void;
  onComplete: () => void;
}

function QueueItemCard({ item, onStart, onComplete }: QueueItemCardProps) {
  const isCompleted = item.completed_at !== null;
  const icon = ITEM_TYPE_ICONS[item.item_type] || "📋";
  const label = ITEM_TYPE_LABELS[item.item_type] || item.item_type;

  return (
    <GlassCard
      style={{
        opacity: isCompleted ? 0.6 : 1,
        display: "flex",
        alignItems: "center",
        gap: "var(--space-3)",
      }}
    >
      <span style={{ fontSize: "1.5rem" }}>{icon}</span>
      <div style={{ flex: 1 }}>
        <p
          style={{
            margin: 0,
            fontSize: "var(--font-size-sm)",
            fontWeight: 600,
            color: "var(--color-text)",
            textDecoration: isCompleted ? "line-through" : "none",
          }}
        >
          {label}
        </p>
        <p style={{ margin: 0, fontSize: "var(--font-size-xs)", color: "var(--color-text-muted)" }}>
          ~{formatDuration(item.estimated_seconds)}
        </p>
      </div>
      {isCompleted ? (
        <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-success)" }}>✓</span>
      ) : (
        <div style={{ display: "flex", gap: "var(--space-2)" }}>
          <GlassButton variant="ghost" size="sm" onClick={onStart}>
            Start
          </GlassButton>
          <GlassButton variant="ghost" size="sm" onClick={onComplete}>
            Skip
          </GlassButton>
        </div>
      )}
    </GlassCard>
  );
}
