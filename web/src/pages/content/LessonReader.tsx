import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiClient } from "../../api/client";
import { GlassCard } from "../../components/GlassCard";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";
import { GlassProgressBar } from "../../components/GlassProgressBar";
import { MarkdownText } from "../../components/MarkdownText";
import { useToast } from "../../context/ToastContext";

interface LessonExplanation {
  title?: string;
  heading?: string;
  body: string;
}

interface LessonWorkedExample {
  title: string;
  problem?: string;
  solution?: string;
  body?: string;
}

interface LessonContent {
  explanations: LessonExplanation[];
  worked_examples: LessonWorkedExample[];
  key_takeaways: string[];
  summary: string;
}

interface LessonResponse {
  id: number;
  subtopic_id: number;
  content_json: LessonContent;
  status: string;
}

// Preamble sections rendered as fixed header content (not in dropdowns)
const PREAMBLE_TITLES = [
  "introduction",
  "why subject-verb agreement matters",
  "why subject-verb agreement is tested in the cse",
  "why parallelism matters",
  "why parallelism is tested in the cse",
  "why direct and indirect speech are tested in the cse",
  "common mistakes examinees make",
  "learning objectives",
  "focus areas",
];

function isPreambleSection(title: string): boolean {
  const lower = title.toLowerCase();
  return PREAMBLE_TITLES.some((p) => lower.includes(p)) ||
    lower.startsWith("why ") ||
    lower.includes("learning objective");
}

function isLearningObjectives(title: string): boolean {
  return title.toLowerCase().includes("learning objective");
}

export function LessonReader() {
  const { subtopicId } = useParams<{ subtopicId: string }>();
  const toast = useToast();
  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    explanations: true,
    examples: false,
    takeaways: false,
    summary: false,
  });

  useEffect(() => {
    apiClient
      .get<LessonResponse>(`/v1/subtopics/${subtopicId}/lesson`)
      .then((res) => setLesson(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [subtopicId]);

  async function handleMarkComplete() {
    setCompleting(true);
    try {
      await apiClient.post(`/v1/subtopics/${subtopicId}/lesson:complete`, {});
      setCompleted(true);
      toast.success("✅ Lesson marked complete");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to mark complete";
      toast.error(msg);
      setError(msg);
    } finally {
      setCompleting(false);
    }
  }

  function toggleSection(key: string) {
    setExpandedSections((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  if (loading) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 720 }}>
          <div style={{ marginBottom: "1.5rem" }}>
            <GlassSkeleton width="120px" height="1rem" />
          </div>
          <GlassSkeleton width="100%" height="4px" borderRadius="var(--radius-full)" />
          <div style={{ marginTop: "1.5rem", display: "flex", flexDirection: "column", gap: "1rem" }}>
            <GlassSkeleton width="60%" height="1.25rem" />
            <GlassSkeleton width="100%" height="6rem" borderRadius="var(--radius-lg)" />
            <GlassSkeleton width="100%" height="6rem" borderRadius="var(--radius-lg)" />
          </div>
        </div>
      </PageTransition>
    );
  }

  if (error) return <div className="page container error-text">{error}</div>;
  if (!lesson) return <div className="page container" style={{ color: "var(--color-text-secondary)" }}>Lesson not found.</div>;

  const content = lesson.content_json;

  // Separate preamble (intro, objectives) from numbered lesson sections
  const allExplanations = content.explanations.map((e) => ({
    title: (typeof e === "string" ? "" : (e.title || e.heading || "")),
    body: typeof e === "string" ? e : e.body,
    raw: typeof e === "string" ? e : `**${e.title || e.heading || ""}**\n\n${e.body}`,
  }));

  const preambleSections = allExplanations.filter((e) => isPreambleSection(e.title));
  const lessonSections = allExplanations.filter((e) => !isPreambleSection(e.title));

  const totalSteps = 4; // preamble + lesson + examples/takeaways + summary
  const expandedCount = Object.values(expandedSections).filter(Boolean).length;

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 720 }}>
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
          <Link
            to="/modules"
            aria-label="Back to modules"
            className="btn-glass"
            style={{ padding: "0.375rem 0.75rem", fontSize: "var(--font-size-sm)" }}
          >
            ← Back
          </Link>
          <div style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>
            Step {expandedCount} of {totalSteps}
          </div>
        </div>

        <GlassProgressBar value={expandedCount} max={totalSteps} height={4} />

        <article style={{ marginTop: "1.25rem" }}>

          {/* Preamble: Introduction + Learning Objectives (always visible, no dropdown) */}
          {preambleSections.length > 0 && (
            <div style={{ marginBottom: "1.5rem" }}>
              {preambleSections.map((section, i) => (
                isLearningObjectives(section.title) ? (
                  <LearningObjectivesCard key={i} body={section.body} />
                ) : (
                  <div key={i} style={{ marginBottom: "1rem" }}>
                    <MarkdownText text={section.raw} style={{ lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.9375rem" }} />
                  </div>
                )
              ))}
            </div>
          )}

          {/* Lesson Content Sections (numbered 4.1, 4.2, etc.) */}
          <CollapsibleSection
            title="📖 Lesson Content"
            expanded={expandedSections.explanations}
            onToggle={() => toggleSection("explanations")}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
              {lessonSections.map((section, i) => (
                <LessonSectionDropdown key={i} title={section.title} body={section.body} index={i} />
              ))}
            </div>
          </CollapsibleSection>

          {/* Worked Examples */}
          <CollapsibleSection
            title="💡 Worked Examples"
            expanded={expandedSections.examples}
            onToggle={() => toggleSection("examples")}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {content.worked_examples.map((e, i) => {
                const text = typeof e === "string" ? e : `**${e.title}**\n\n${e.problem || ""}${e.solution ? "\n\n" + e.solution : ""}${e.body ? "\n\n" + e.body : ""}`;
                return (
                  <GlassCard key={i} blur="sm">
                    <MarkdownText text={text} style={{ lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.9375rem" }} />
                  </GlassCard>
                );
              })}
            </div>
          </CollapsibleSection>

          {/* Key Takeaways */}
          <CollapsibleSection
            title="🔑 Key Takeaways"
            expanded={expandedSections.takeaways}
            onToggle={() => toggleSection("takeaways")}
          >
            <GlassCard blur="sm" style={{ background: "rgba(212, 165, 116, 0.06)", border: "1px solid rgba(212, 165, 116, 0.2)" }}>
              <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                {content.key_takeaways.map((text, i) => (
                  <li key={i} style={{ marginBottom: "0.375rem", lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.875rem" }}>
                    <MarkdownText text={text} />
                  </li>
                ))}
              </ul>
            </GlassCard>
          </CollapsibleSection>

          {/* Summary */}
          <CollapsibleSection
            title="📝 Summary"
            expanded={expandedSections.summary}
            onToggle={() => toggleSection("summary")}
          >
            <MarkdownText text={content.summary} style={{ lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.9375rem" }} />
          </CollapsibleSection>
        </article>

        {/* Complete button */}
        <div style={{ marginTop: "1.5rem", paddingBottom: "2rem" }}>
          {completed ? (
            <p style={{ color: "var(--color-success)", fontWeight: 600 }}>✓ Lesson completed</p>
          ) : (
            <button
              className="btn-glass btn-glass-primary"
              onClick={handleMarkComplete}
              disabled={completing}
              aria-label="Mark lesson as complete"
              style={{ padding: "0.75rem 1.5rem" }}
            >
              {completing ? "Marking…" : "Mark Complete"}
            </button>
          )}
        </div>
      </div>
    </PageTransition>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function LearningObjectivesCard({ body }: { body: string }) {
  // Extract bullet items from the body
  const items = body
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.startsWith("- ") || l.startsWith("* "))
    .map((l) => l.slice(2));

  return (
    <div
      style={{
        margin: "0.75rem 0",
        padding: "0.75rem 1rem",
        background: "rgba(212, 165, 116, 0.06)",
        border: "1px solid rgba(212, 165, 116, 0.2)",
        borderLeft: "3px solid var(--color-accent, #d4a574)",
        borderRadius: "var(--radius-md, 8px)",
      }}
    >
      <div style={{ fontWeight: 600, fontSize: "0.875rem", marginBottom: "0.5rem", color: "var(--color-accent, #d4a574)" }}>
        🎯 Learning Objectives
      </div>
      {items.length > 0 ? (
        <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
          {items.map((item, i) => (
            <li key={i} style={{ marginBottom: "0.25rem", lineHeight: 1.5, fontSize: "0.8125rem", color: "var(--color-text-secondary)" }}>
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <MarkdownText text={body} style={{ fontSize: "0.8125rem", lineHeight: 1.5, color: "var(--color-text-secondary)" }} />
      )}
    </div>
  );
}

function CollapsibleSection({
  title,
  expanded,
  onToggle,
  children,
}: {
  title: string;
  expanded: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <section aria-label={title} style={{ marginBottom: "1rem" }}>
      <button
        onClick={onToggle}
        aria-expanded={expanded}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          padding: "0.625rem 0",
          background: "none",
          border: "none",
          borderBottom: "1px solid var(--glass-border-medium)",
          cursor: "pointer",
          fontSize: "0.9375rem",
          fontWeight: 600,
          color: "var(--color-text)",
          textAlign: "left",
        }}
      >
        {title}
        <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)", transition: "transform var(--transition-fast)", transform: expanded ? "rotate(180deg)" : "rotate(0)" }}>
          ▼
        </span>
      </button>
      {expanded && (
        <div style={{ padding: "0.75rem 0", animation: "fadeIn 0.2s ease" }}>
          {children}
        </div>
      )}
    </section>
  );
}

function LessonSectionDropdown({ title, body, index }: { title: string; body: string; index: number }) {
  const [open, setOpen] = useState(index === 0);

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          padding: "0.5rem 0.75rem",
          background: open ? "rgba(212, 165, 116, 0.04)" : "rgba(255, 255, 255, 0.02)",
          border: "1px solid var(--glass-border-medium)",
          borderRadius: "var(--radius-md)",
          cursor: "pointer",
          fontSize: "0.875rem",
          fontWeight: 600,
          color: "var(--color-text)",
          textAlign: "left",
          transition: "background var(--transition-fast)",
        }}
      >
        <span style={{ flex: 1 }}>{title || `Section ${index + 1}`}</span>
        <span
          style={{
            fontSize: "0.6875rem",
            color: "var(--color-text-muted)",
            transition: "transform var(--transition-fast)",
            transform: open ? "rotate(180deg)" : "rotate(0)",
            flexShrink: 0,
            marginLeft: "0.5rem",
          }}
        >
          ▼
        </span>
      </button>
      {open && (
        <div
          style={{
            padding: "0.75rem 0.75rem 0.75rem 1rem",
            borderLeft: "2px solid var(--color-accent, #d4a574)",
            marginLeft: "0.5rem",
            marginTop: "0.25rem",
          }}
        >
          <MarkdownText text={body} style={{ lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.875rem" }} />
        </div>
      )}
    </div>
  );
}
