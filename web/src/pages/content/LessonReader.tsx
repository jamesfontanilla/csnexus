import { useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiClient } from "../../api/client";
import { GlassCard } from "../../components/GlassCard";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";
import { GlassProgressBar } from "../../components/GlassProgressBar";
import { MarkdownText } from "../../components/MarkdownText";
import { useToast } from "../../context/ToastContext";
import { DesktopLessonLayout, useIsDesktop } from "./lesson";
import type { EnhancedLessonContent } from "./lesson";

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

function isPreambleSection(title: string): boolean {
  const lower = title.toLowerCase();
  return lower.includes("introduction") ||
    lower.startsWith("why ") ||
    lower.includes("learning objective") ||
    lower.includes("common mistakes examinees") ||
    lower.includes("focus areas");
}

function isLearningObjectives(title: string): boolean {
  return title.toLowerCase().includes("learning objective");
}

/** Extract short label from section title: "4.1 The Basic Rule" → "4.1" */
function shortLabel(title: string): string {
  const match = title.match(/^(\d+\.\d+)/);
  return match ? match[1] : title.slice(0, 8);
}

export function LessonReader() {
  const { subtopicId } = useParams<{ subtopicId: string }>();
  const toast = useToast();
  const isDesktop = useIsDesktop();
  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [activeNavIdx, setActiveNavIdx] = useState(0);
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    apiClient
      .get<LessonResponse>(`/v1/subtopics/${subtopicId}/lesson`)
      .then((res) => setLesson(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [subtopicId]);

  // Intersection observer for sticky nav highlighting
  useEffect(() => {
    if (!lesson || typeof IntersectionObserver === "undefined") return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const idx = sectionRefs.current.indexOf(entry.target as HTMLDivElement);
            if (idx >= 0) setActiveNavIdx(idx);
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px", threshold: 0.1 }
    );
    sectionRefs.current.forEach((ref) => { if (ref) observer.observe(ref); });
    return () => observer.disconnect();
  }, [lesson]);

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

  function scrollToSection(idx: number) {
    sectionRefs.current[idx]?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  if (loading) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 720 }}>
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

  // Desktop layout: three-column with typed block rendering
  if (isDesktop) {
    return (
      <PageTransition>
        <DesktopLessonLayout
          content={content as unknown as EnhancedLessonContent}
          subtopicId={subtopicId || ""}
          onMarkComplete={handleMarkComplete}
          completing={completing}
          completed={completed}
        />
      </PageTransition>
    );
  }

  // Mobile layout: original single-column
  const allExplanations = content.explanations.map((e) => ({
    title: (typeof e === "string" ? "" : (e.title || e.heading || "")),
    body: typeof e === "string" ? e : e.body,
    raw: typeof e === "string" ? e : `**${e.title || e.heading || ""}**\n\n${e.body}`,
  }));

  const preambleSections = allExplanations.filter((e) => isPreambleSection(e.title));
  const lessonSections = allExplanations.filter((e) => !isPreambleSection(e.title));
  const totalSteps = lessonSections.length;

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 720, paddingBottom: "5rem" }}>
        {/* Top bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
          <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
            ← Back
          </Link>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            {activeNavIdx + 1} / {totalSteps}
          </span>
        </div>

        <GlassProgressBar value={activeNavIdx + 1} max={totalSteps} height={3} />

        {/* Sticky section nav pills */}
        {lessonSections.length > 1 && (
          <nav
            aria-label="Section navigation"
            style={{
              position: "sticky",
              top: 0,
              zIndex: 10,
              background: "var(--color-bg, #1a1a1a)",
              padding: "0.5rem 0",
              marginBottom: "1rem",
              borderBottom: "1px solid rgba(255,255,255,0.06)",
              overflowX: "auto",
              display: "flex",
              gap: "0.25rem",
              scrollbarWidth: "none",
            }}
          >
            {lessonSections.map((s, idx) => (
              <button
                key={idx}
                onClick={() => scrollToSection(idx)}
                title={s.title}
                style={{
                  flexShrink: 0,
                  padding: "0.25rem 0.5rem",
                  fontSize: "0.6875rem",
                  fontWeight: idx === activeNavIdx ? 700 : 500,
                  borderRadius: "var(--radius-full, 999px)",
                  border: "1px solid",
                  borderColor: idx === activeNavIdx ? "var(--color-accent, #d4a574)" : "rgba(255,255,255,0.1)",
                  background: idx === activeNavIdx ? "rgba(212, 165, 116, 0.15)" : "transparent",
                  color: idx === activeNavIdx ? "var(--color-accent, #d4a574)" : "var(--color-text-muted)",
                  cursor: "pointer",
                  transition: "all 0.15s ease",
                  whiteSpace: "nowrap",
                }}
              >
                {shortLabel(s.title)}
              </button>
            ))}
          </nav>
        )}

        <article>
          {/* Preamble (always visible, compact) */}
          {preambleSections.length > 0 && (
            <div style={{ marginBottom: "1.25rem" }}>
              {preambleSections.map((section, i) => (
                isLearningObjectives(section.title) ? (
                  <LearningObjectivesCard key={i} body={section.body} />
                ) : (
                  <div key={i} style={{ marginBottom: "0.75rem" }}>
                    <MarkdownText text={section.raw} style={{ lineHeight: 1.5, color: "var(--color-text)", fontSize: "0.875rem" }} />
                  </div>
                )
              ))}
            </div>
          )}

          {/* Lesson sections (all expanded, scrollable with nav) */}
          {lessonSections.map((section, idx) => (
            <div
              key={idx}
              ref={(el) => { sectionRefs.current[idx] = el; }}
              style={{ marginBottom: "2rem", scrollMarginTop: "3.5rem" }}
            >
              <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                {section.title}
              </h3>
              <MarkdownText text={section.body} style={{ lineHeight: 1.6, color: "var(--color-text)", fontSize: "0.875rem" }} />
            </div>
          ))}

          {/* Worked Examples */}
          {content.worked_examples.length > 0 && content.worked_examples[0].title !== "See lesson sections" && (
            <div style={{ marginBottom: "2rem" }}>
              <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                💡 Worked Examples
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                {content.worked_examples.map((e, i) => {
                  const text = typeof e === "string" ? e : `**${e.title}**\n\n${e.problem || ""}${e.solution ? "\n\n" + e.solution : ""}${e.body ? "\n\n" + e.body : ""}`;
                  return (
                    <GlassCard key={i} blur="sm">
                      <MarkdownText text={text} style={{ lineHeight: 1.5, color: "var(--color-text)", fontSize: "0.8125rem" }} />
                    </GlassCard>
                  );
                })}
              </div>
            </div>
          )}

          {/* Key Takeaways */}
          {content.key_takeaways.length > 0 && (
            <div style={{ marginBottom: "2rem" }}>
              <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                🔑 Key Takeaways
              </h3>
              <GlassCard blur="sm" style={{ background: "rgba(212, 165, 116, 0.05)", border: "1px solid rgba(212, 165, 116, 0.15)" }}>
                <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                  {content.key_takeaways.map((text, i) => (
                    <li key={i} style={{ marginBottom: "0.25rem", lineHeight: 1.5, color: "var(--color-text)", fontSize: "0.8125rem" }}>
                      <MarkdownText text={text} />
                    </li>
                  ))}
                </ul>
              </GlassCard>
            </div>
          )}

          {/* Summary */}
          {content.summary && (
            <div style={{ marginBottom: "2rem" }}>
              <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                📝 Summary
              </h3>
              <MarkdownText text={content.summary} style={{ lineHeight: 1.5, color: "var(--color-text)", fontSize: "0.875rem" }} />
            </div>
          )}
        </article>

        {/* Sticky complete button */}
        <div
          style={{
            position: "fixed",
            bottom: 0,
            left: 0,
            right: 0,
            padding: "0.75rem 1rem",
            background: "linear-gradient(transparent, var(--color-bg, #1a1a1a) 30%)",
            display: "flex",
            justifyContent: "center",
            zIndex: 20,
          }}
        >
          {completed ? (
            <span style={{ color: "var(--color-success)", fontWeight: 600, fontSize: "0.875rem" }}>✓ Lesson completed</span>
          ) : (
            <button
              className="btn-glass btn-glass-primary"
              onClick={handleMarkComplete}
              disabled={completing}
              aria-label="Mark lesson as complete"
              style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
            >
              {completing ? "Marking…" : "✓ Mark Complete"}
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
  const items = body.split("\n").map((l) => l.trim()).filter((l) => l.startsWith("- ") || l.startsWith("* ")).map((l) => l.slice(2));

  return (
    <div style={{ margin: "0.5rem 0", padding: "0.6rem 0.75rem", background: "rgba(212, 165, 116, 0.05)", border: "1px solid rgba(212, 165, 116, 0.15)", borderLeft: "3px solid var(--color-accent, #d4a574)", borderRadius: "6px" }}>
      <div style={{ fontWeight: 600, fontSize: "0.8125rem", marginBottom: "0.375rem", color: "var(--color-accent, #d4a574)" }}>
        🎯 Learning Objectives
      </div>
      {items.length > 0 ? (
        <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
          {items.map((item, i) => (
            <li key={i} style={{ marginBottom: "0.2rem", lineHeight: 1.4, fontSize: "0.75rem", color: "var(--color-text-secondary)" }}>{item}</li>
          ))}
        </ul>
      ) : (
        <MarkdownText text={body} style={{ fontSize: "0.75rem", lineHeight: 1.4, color: "var(--color-text-secondary)" }} />
      )}
    </div>
  );
}
