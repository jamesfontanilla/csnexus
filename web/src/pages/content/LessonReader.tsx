import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiClient } from "../../api/client";
import { GlassCard } from "../../components/GlassCard";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";
import { GlassProgressBar } from "../../components/GlassProgressBar";
import { MarkdownText } from "../../components/MarkdownText";
import { XPGainAnimation } from "../../components/XPGainAnimation";
import { useToast } from "../../context/ToastContext";
import { useReducedMotion } from "../../design-system/motion";
import { DesktopLessonLayout, BlockRenderer, useIsDesktop } from "./lesson";
import { LessonChatPanel } from "./lesson";
import type { EnhancedLessonContent, LessonSegment, InlineCheck } from "./lesson";

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

interface LessonCompleteApiResponse {
  lesson_id: number;
  user_id: number;
  completed_at: string;
  awarded_xp: number;
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

// ---------------------------------------------------------------------------
// Reading Progress Bar — fixed at top of viewport
// ---------------------------------------------------------------------------

function ReadingProgressBar({ progress }: { progress: number }) {
  return (
    <div
      aria-hidden="true"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        height: "3px",
        zIndex: 9999,
        background: "transparent",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          background: "linear-gradient(90deg, var(--color-accent), var(--color-metallic))",
          transition: "width 100ms linear",
        }}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Mobile Section Navigation — collapsible bottom panel
// ---------------------------------------------------------------------------

interface MobileSectionNavProps {
  sections: { title: string }[];
  activeIndex: number;
  onNavigate: (index: number) => void;
}

function MobileSectionNav({ sections, activeIndex, onNavigate }: MobileSectionNavProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (sections.length <= 1) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        background: "var(--color-surface, #1C1C1C)",
        borderTop: "1px solid var(--glass-border-medium, rgba(255,255,255,0.10))",
        backdropFilter: "blur(12px)",
        maxHeight: isOpen ? "60vh" : "44px",
        transition: "max-height 0.25s var(--ease-standard, cubic-bezier(0.4, 0, 0.2, 1))",
        overflow: "hidden",
      }}
    >
      {/* Toggle header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Section navigation"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          padding: "0.625rem 1rem",
          background: "transparent",
          border: "none",
          color: "var(--color-text)",
          cursor: "pointer",
          fontSize: "0.8125rem",
          fontWeight: 600,
          minHeight: "44px",
        }}
      >
        <span>
          §{activeIndex + 1} / {sections.length} — {sections[activeIndex]?.title || "Sections"}
        </span>
        <span
          style={{
            transform: isOpen ? "rotate(180deg)" : "rotate(0deg)",
            transition: "transform 0.2s ease",
            fontSize: "0.75rem",
          }}
        >
          ▲
        </span>
      </button>

      {/* Section list */}
      {isOpen && (
        <nav
          aria-label="Lesson sections"
          style={{
            padding: "0 1rem 1rem",
            overflowY: "auto",
            maxHeight: "calc(60vh - 44px)",
          }}
        >
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {sections.map((section, idx) => {
              const isActive = idx === activeIndex;
              return (
                <li key={idx}>
                  <button
                    onClick={() => {
                      onNavigate(idx);
                      setIsOpen(false);
                    }}
                    style={{
                      display: "block",
                      width: "100%",
                      padding: "0.5rem 0.75rem",
                      background: isActive ? "rgba(201, 168, 76, 0.1)" : "transparent",
                      border: "none",
                      borderLeft: isActive ? "2px solid var(--color-accent)" : "2px solid transparent",
                      borderRadius: "0 4px 4px 0",
                      cursor: "pointer",
                      textAlign: "left",
                      color: isActive ? "var(--color-accent)" : "var(--color-text-secondary)",
                      fontSize: "0.8125rem",
                      fontWeight: isActive ? 600 : 400,
                      marginBottom: "0.125rem",
                    }}
                  >
                    {idx + 1}. {section.title}
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main LessonReader Component
// ---------------------------------------------------------------------------

export function LessonReader() {
  const { subtopicId } = useParams<{ subtopicId: string }>();
  const toast = useToast();
  const isDesktop = useIsDesktop();
  const reducedMotion = useReducedMotion();
  const [lesson, setLesson] = useState<LessonResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [completing, setCompleting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [xpGained, setXpGained] = useState(0);
  const [activeNavIdx, setActiveNavIdx] = useState(0);
  const [readingProgress, setReadingProgress] = useState(0);
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Reading progress via scroll event
  useEffect(() => {
    function handleScroll() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) {
        setReadingProgress(0);
        return;
      }
      const progress = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100));
      setReadingProgress(progress);
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // initial
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

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

  const scrollToSection = useCallback((idx: number) => {
    sectionRefs.current[idx]?.scrollIntoView({
      behavior: reducedMotion ? "auto" : "smooth",
      block: "start",
    });
  }, [reducedMotion]);

  async function handleMarkComplete() {
    setCompleting(true);
    try {
      const res = await apiClient.post<LessonCompleteApiResponse>(
        `/v1/subtopics/${subtopicId}/lesson:complete`,
        {}
      );
      setCompleted(true);
      if (res.awarded_xp > 0) {
        setXpGained(res.awarded_xp);
      } else {
        toast.success("✅ Lesson already completed");
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to mark complete";
      toast.error(msg);
      setError(msg);
    } finally {
      setCompleting(false);
    }
  }

  if (loading) {
    return (
      <PageTransition>
        <ReadingProgressBar progress={0} />
        <div className="page container" style={{ maxWidth: 680, margin: "0 auto" }}>
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
        <ReadingProgressBar progress={readingProgress} />
        <XPGainAnimation amount={xpGained} onComplete={() => { setXpGained(0); toast.success("✅ Lesson completed"); }} />
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

  const enhancedContent = content as unknown as EnhancedLessonContent;

  // Mobile segmented layout — used for clerical-ability lessons
  if (enhancedContent.is_segmented && Array.isArray(enhancedContent.segments) && enhancedContent.segments.length > 0) {
    return (
      <PageTransition>
        <ReadingProgressBar progress={readingProgress} />
        <XPGainAnimation amount={xpGained} onComplete={() => { setXpGained(0); toast.success("✅ Lesson completed"); }} />
        <MobileSegmentedReader
          content={enhancedContent}
          subtopicId={subtopicId || ""}
          onMarkComplete={handleMarkComplete}
          completing={completing}
          completed={completed}
        />
      </PageTransition>
    );
  }

  // Mobile layout: single-column with reading-optimized typography
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
      <ReadingProgressBar progress={readingProgress} />
      <XPGainAnimation amount={xpGained} onComplete={() => { setXpGained(0); toast.success("✅ Lesson completed"); }} />
      <div
        className="page container"
        style={{
          maxWidth: 680,
          margin: "0 auto",
          paddingBottom: "5rem",
          lineHeight: 1.75,
          fontSize: "var(--font-size-base)",
        }}
      >
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

        <article>
          {/* Preamble (always visible, compact) */}
          {preambleSections.length > 0 && (
            <div style={{ marginBottom: "1.25rem" }}>
              {preambleSections.map((section, i) => (
                isLearningObjectives(section.title) ? (
                  <LearningObjectivesCard key={i} body={section.body} />
                ) : (
                  <div key={i} style={{ marginBottom: "0.75rem" }}>
                    <MarkdownText text={section.raw} style={{ lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }} />
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
              <MarkdownText text={section.body} style={{ lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }} />
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
                      <MarkdownText text={text} style={{ lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }} />
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
                    <li key={i} style={{ marginBottom: "0.25rem", lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }}>
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
              <MarkdownText text={content.summary} style={{ lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }} />
            </div>
          )}
        </article>

        {/* Sticky complete button */}
        <div
          style={{
            position: "fixed",
            bottom: lessonSections.length > 1 ? "44px" : 0,
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

        {/* Floating chat panel */}
        <LessonChatPanel
          subtopicId={subtopicId || ""}
          activeSectionIndex={activeNavIdx}
          lessonTitle={content.explanations[0]?.title || content.explanations[0]?.heading || ""}
        />
      </div>

      {/* Mobile section navigation — collapsible bottom panel */}
      <MobileSectionNav
        sections={lessonSections}
        activeIndex={activeNavIdx}
        onNavigate={scrollToSection}
      />
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

// ---------------------------------------------------------------------------
// Mobile segmented reader — one segment at a time with gate checks
// ---------------------------------------------------------------------------

interface MobileSegmentedReaderProps {
  content: EnhancedLessonContent;
  subtopicId: string;
  onMarkComplete: () => void;
  completing: boolean;
  completed: boolean;
}

function MobileSegmentedReader({
  content,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: MobileSegmentedReaderProps) {
  const segments = content.segments!;
  const [activeSegment, setActiveSegment] = useState(0);
  const [gateOpen, setGateOpen] = useState(false);
  const reducedMotion = useReducedMotion();
  const topRef = useRef<HTMLDivElement | null>(null);

  const current = segments[activeSegment];
  const isLast = activeSegment === segments.length - 1;
  const hasChecks = current.checks.length > 0;

  function scrollTop() {
    topRef.current?.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
  }

  function advance() {
    setActiveSegment((i) => i + 1);
    setGateOpen(false);
    scrollTop();
  }

  const keyTakeaways = Array.isArray(content.key_takeaways) ? content.key_takeaways : [];

  return (
    <div
      ref={topRef}
      className="page container"
      style={{ maxWidth: 680, margin: "0 auto", paddingBottom: "5rem", lineHeight: 1.75 }}
    >
      {/* Top bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
          ← Back
        </Link>
        <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
          Part {activeSegment + 1} / {segments.length} · ~{current.estimated_minutes} min
        </span>
      </div>

      <GlassProgressBar value={activeSegment + (gateOpen ? 0.5 : 0)} max={segments.length} height={3} />

      <article style={{ marginTop: "1.25rem" }}>
        {/* Render sections in current segment using typed BlockRenderer */}
        {current.sections.map((section, si) => (
          <div key={si} style={{ marginBottom: "2rem", scrollMarginTop: "3.5rem" }}>
            <h3 style={{
              fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)",
              margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)",
              paddingBottom: "0.375rem",
            }}>
              {section.title}
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {section.blocks.map((block, bi) => (
                <BlockRenderer key={bi} block={block} />
              ))}
            </div>
          </div>
        ))}

        {/* Gate or advance */}
        {!gateOpen ? (
          <div style={{ display: "flex", justifyContent: "center", marginTop: "1.5rem" }}>
            {hasChecks ? (
              <button
                className="btn-glass btn-glass-primary"
                onClick={() => setGateOpen(true)}
                style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
              >
                Check understanding →
              </button>
            ) : !isLast ? (
              <button
                className="btn-glass btn-glass-primary"
                onClick={advance}
                style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
              >
                Continue to Part {activeSegment + 2} →
              </button>
            ) : null}
          </div>
        ) : (
          <MobileGatePanel
            checks={current.checks}
            isLast={isLast}
            onAdvance={advance}
            onComplete={onMarkComplete}
            completing={completing}
            completed={completed}
          />
        )}

        {/* Last segment: key takeaways + summary after gate */}
        {isLast && gateOpen && (
          <>
            {keyTakeaways.length > 0 && (
              <div style={{ marginTop: "2rem" }}>
                <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                  🔑 Key Takeaways
                </h3>
                <GlassCard blur="sm" style={{ background: "rgba(212, 165, 116, 0.05)", border: "1px solid rgba(212, 165, 116, 0.15)" }}>
                  <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                    {keyTakeaways.map((t, i) => (
                      <li key={i} style={{ marginBottom: "0.25rem", lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }}>
                        <MarkdownText text={t} />
                      </li>
                    ))}
                  </ul>
                </GlassCard>
              </div>
            )}
            {content.summary && (
              <div style={{ marginTop: "1.5rem" }}>
                <h3 style={{ fontSize: "0.9375rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.5rem 0", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.375rem" }}>
                  📝 Summary
                </h3>
                <MarkdownText text={content.summary} style={{ lineHeight: 1.75, color: "var(--color-text)", fontSize: "var(--font-size-base)" }} />
              </div>
            )}
          </>
        )}
      </article>

      {/* Segment nav dots at bottom */}
      {segments.length > 1 && (
        <div style={{ position: "fixed", bottom: 0, left: 0, right: 0, padding: "0.5rem 1rem", background: "var(--color-surface, #1C1C1C)", borderTop: "1px solid rgba(255,255,255,0.08)", display: "flex", justifyContent: "center", alignItems: "center", gap: "0.5rem", zIndex: 20 }}>
          {segments.map((_, idx) => {
            const past = idx < activeSegment;
            const curr = idx === activeSegment;
            return (
              <button
                key={idx}
                onClick={() => { if (past || curr) { setActiveSegment(idx); setGateOpen(false); scrollTop(); } }}
                disabled={idx > activeSegment}
                aria-label={`Part ${idx + 1}`}
                style={{
                  width: curr ? "1.5rem" : "0.5rem",
                  height: "0.5rem",
                  borderRadius: "9999px",
                  background: curr ? "var(--color-accent, #d4a574)" : past ? "rgba(212,165,116,0.4)" : "rgba(255,255,255,0.15)",
                  border: "none",
                  cursor: idx > activeSegment ? "default" : "pointer",
                  transition: "width 0.2s ease, background 0.2s ease",
                  padding: 0,
                }}
              />
            );
          })}
        </div>
      )}

      <LessonChatPanel
        subtopicId={subtopicId}
        activeSectionIndex={activeSegment}
        lessonTitle={content.metadata?.title || ""}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Mobile gate panel
// ---------------------------------------------------------------------------

interface MobileGatePanelProps {
  checks: InlineCheck[];
  isLast: boolean;
  onAdvance: () => void;
  onComplete: () => void;
  completing: boolean;
  completed: boolean;
}

function MobileGatePanel({ checks, isLast, onAdvance, onComplete, completing, completed }: MobileGatePanelProps) {
  const [revealed, setRevealed] = useState<Set<number>>(new Set());
  const canAdvance = checks.length === 0 || revealed.size > 0;

  function toggle(i: number) {
    setRevealed((prev) => { const next = new Set(prev); next.has(i) ? next.delete(i) : next.add(i); return next; });
  }

  return (
    <div style={{ marginTop: "1.5rem", padding: "1rem", background: "rgba(80,200,120,0.04)", border: "1px solid rgba(80,200,120,0.2)", borderRadius: "8px" }}>
      <div style={{ fontSize: "0.6875rem", fontWeight: 700, color: "rgba(80,200,120,0.9)", marginBottom: "0.875rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>
        ✓ Quick Check
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.625rem", marginBottom: "1rem" }}>
        {checks.map((check, i) => {
          const open = revealed.has(i);
          return (
            <div key={i} style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "6px", overflow: "hidden" }}>
              <div style={{ padding: "0.5rem 0.75rem", fontSize: "0.875rem", lineHeight: 1.55, color: "var(--color-text)" }}>
                <MarkdownText text={`${i + 1}. ${check.question}`} />
              </div>
              <button
                onClick={() => toggle(i)}
                style={{ display: "block", width: "100%", padding: "0.35rem 0.75rem", background: open ? "rgba(80,200,120,0.1)" : "rgba(255,255,255,0.03)", border: "none", borderTop: "1px solid rgba(255,255,255,0.06)", cursor: "pointer", textAlign: "left", fontSize: "0.75rem", fontWeight: 600, color: open ? "rgba(80,200,120,0.9)" : "var(--color-text-muted)" }}
              >
                {open ? "▾ Hide" : "▸ Show answer"}
              </button>
              {open && (
                <div style={{ padding: "0.5rem 0.75rem", background: "rgba(80,200,120,0.06)", borderTop: "1px solid rgba(80,200,120,0.15)", fontSize: "0.875rem", lineHeight: 1.55, color: "var(--color-text)" }}>
                  <MarkdownText text={check.answer} />
                  {check.rationale && <div style={{ marginTop: "0.25rem", fontSize: "0.75rem", color: "var(--color-text-muted)", fontStyle: "italic" }}><MarkdownText text={check.rationale} /></div>}
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        {completed ? (
          <span style={{ color: "var(--color-success)", fontWeight: 600, fontSize: "0.875rem" }}>✓ Completed</span>
        ) : isLast ? (
          <button className="btn-glass btn-glass-primary" onClick={onComplete} disabled={completing || !canAdvance} style={{ padding: "0.625rem 1.5rem", fontSize: "0.875rem" }}>
            {completing ? "Marking…" : "✓ Mark Complete"}
          </button>
        ) : (
          <button className="btn-glass btn-glass-primary" onClick={onAdvance} disabled={!canAdvance} style={{ padding: "0.625rem 1.5rem", fontSize: "0.875rem" }}>
            Continue →
          </button>
        )}
      </div>
    </div>
  );
}
