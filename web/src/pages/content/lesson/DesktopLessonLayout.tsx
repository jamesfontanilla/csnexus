import { useEffect, useRef, useState, forwardRef } from "react";
import { Link } from "react-router-dom";
import type { EnhancedLessonContent, LessonSection, InlineCheck } from "./types";
import { BlockRenderer } from "./BlockRenderer";
import { SidebarTOC } from "./SidebarTOC";
import { PracticePanel, InlineLessonChat } from "./PracticePanel";
import { GlassProgressBar } from "../../../components/GlassProgressBar";
import { MarkdownText } from "../../../components/MarkdownText";
import { useReducedMotion } from "../../../design-system/motion";

interface DesktopLessonLayoutProps {
  content: EnhancedLessonContent;
  subtopicId: string;
  onMarkComplete: () => void;
  completing: boolean;
  completed: boolean;
}

/**
 * Three-column desktop layout for lesson reading:
 * - Left: Persistent sidebar TOC with scroll-spy
 * - Center: Main content with typed block rendering
 * - Right: Practice problems & study aids companion panel
 *
 * Falls back to a two-column layout (TOC + content) when no practice content,
 * and to a single wide column when no enhanced sections exist at all.
 */
export function DesktopLessonLayout({
  content,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: DesktopLessonLayoutProps) {
  // Dispatch to segmented layout when the lesson has been segmented by the parser
  if (content.is_segmented && Array.isArray(content.segments) && content.segments.length > 0) {
    return (
      <SegmentedLessonLayout
        content={content}
        subtopicId={subtopicId}
        onMarkComplete={onMarkComplete}
        completing={completing}
        completed={completed}
      />
    );
  }

  const [activeIndex, setActiveIndex] = useState(0);
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([]);
  const reducedMotion = useReducedMotion();

  // Use enhanced sections if available, fall back to legacy explanations
  const hasEnhancedSections = Array.isArray(content.sections) && content.sections.length > 0;

  // Build navigable sections: prefer enhanced, fall back to legacy explanations
  const sections: LessonSection[] = hasEnhancedSections
    ? content.sections!
    : content.explanations.map((exp) => ({
        title: (typeof exp === "string" ? "" : (exp.title || exp.heading || "Section")),
        blocks: [{
          type: "prose" as const,
          content: typeof exp === "string" ? exp : exp.body,
        }],
        difficulty: [],
        word_count: (typeof exp === "string" ? exp : exp.body).split(" ").length,
        estimated_reading_seconds: Math.ceil((typeof exp === "string" ? exp : exp.body).split(" ").length / 200 * 60),
      }));

  // Build metadata: use enhanced or synthesize from legacy
  const metadata = content.metadata || {
    title: "",
    estimated_reading_minutes: Math.ceil(sections.reduce((acc, s) => acc + s.word_count, 0) / 200),
    section_count: sections.length,
    has_practice_problems: false,
    practice_problem_count: 0,
    difficulty_distribution: {},
    total_word_count: sections.reduce((acc, s) => acc + s.word_count, 0),
  };

  // Intersection observer for scroll-spy
  useEffect(() => {
    if (sections.length === 0 || typeof IntersectionObserver === "undefined") return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const idx = sectionRefs.current.indexOf(entry.target as HTMLDivElement);
            if (idx >= 0) setActiveIndex(idx);
          }
        }
      },
      { rootMargin: "-100px 0px -50% 0px", threshold: 0.1 }
    );

    sectionRefs.current.forEach((ref) => {
      if (ref) observer.observe(ref);
    });

    return () => observer.disconnect();
  }, [sections.length]);

  function scrollToSection(idx: number) {
    sectionRefs.current[idx]?.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
  }

  const practiceProblems = Array.isArray(content.practice_problems) ? content.practice_problems : [];
  const memoryAids = Array.isArray(content.memory_aids) ? content.memory_aids : [];
  const examStrategies = Array.isArray(content.exam_strategies) ? content.exam_strategies : [];
  const keyTakeaways = Array.isArray(content.key_takeaways) ? content.key_takeaways : [];

  return (
    <div className="desktop-lesson-root page" style={{ maxWidth: "1400px", margin: "0 auto", padding: "1.5rem 2rem 4rem" }}>
      {/* Top bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
          ← Back
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            ~{metadata.estimated_reading_minutes} min read
          </span>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            {activeIndex + 1} / {sections.length}
          </span>
        </div>
      </div>

      <GlassProgressBar value={activeIndex + 1} max={sections.length} height={3} />

      {/* Three-column grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "220px 1fr 280px",
          gap: "2rem",
          marginTop: "1.5rem",
          alignItems: "start",
        }}
      >
        {/* Left: TOC sidebar */}
        <SidebarTOC
          sections={sections}
          metadata={metadata}
          activeIndex={activeIndex}
          onNavigate={scrollToSection}
        />

        {/* Center: Main content */}
        <main
          aria-label="Lesson content"
          style={{
            minWidth: 0,
            overflow: "hidden",
            maxWidth: 680,
            margin: "0 auto",
            lineHeight: 1.75,
            fontSize: "var(--font-size-base)",
          }}
        >
          {/* Title */}
          {metadata.title && (
            <h1 style={{ fontSize: "1.5rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 1.5rem 0" }}>
              {metadata.title}
            </h1>
          )}

          {/* Sections with typed blocks */}
          {sections.map((section, idx) => (
            <SectionBlock
              key={idx}
              section={section}
              ref={(el) => { sectionRefs.current[idx] = el; }}
            />
          ))}

          {/* Worked Examples (if separate from sections) */}
          {content.worked_examples.length > 0 && content.worked_examples[0].title !== "See lesson sections" && (
            <div style={{ marginTop: "2rem", paddingTop: "1.5rem", borderTop: "1px solid rgba(255,255,255,0.08)" }}>
              <h2 style={{ fontSize: "1.125rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 1rem 0" }}>
                💡 Worked Examples
              </h2>
              {content.worked_examples.map((ex, i) => (
                <div
                  key={i}
                  style={{
                    marginBottom: "1rem",
                    padding: "1rem",
                    background: "rgba(255,255,255,0.02)",
                    border: "1px solid rgba(255,255,255,0.08)",
                    borderRadius: "8px",
                  }}
                >
                  <h3 style={{ fontSize: "0.875rem", fontWeight: 600, margin: "0 0 0.5rem 0", color: "var(--color-text)" }}>
                    {ex.title}
                  </h3>
                  <MarkdownText
                    text={ex.body || `${ex.problem || ""}\n\n${ex.solution || ""}`}
                    style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }}
                  />
                </div>
              ))}
            </div>
          )}

          {/* Summary */}
          {content.summary && (
            <div style={{ marginTop: "2rem", padding: "1rem 1.25rem", background: "rgba(212, 165, 116, 0.04)", border: "1px solid rgba(212, 165, 116, 0.15)", borderRadius: "8px" }}>
              <h2 style={{ fontSize: "0.875rem", fontWeight: 600, margin: "0 0 0.5rem 0", color: "var(--color-accent, #d4a574)" }}>
                📝 Summary
              </h2>
              <MarkdownText text={content.summary} style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }} />
            </div>
          )}

          {/* Key Takeaways (inline in main content for visibility) */}
          {keyTakeaways.length > 0 && (
            <div style={{ marginTop: "2rem", padding: "1rem 1.25rem", background: "rgba(212, 165, 116, 0.04)", border: "1px solid rgba(212, 165, 116, 0.15)", borderRadius: "8px" }}>
              <h2 style={{ fontSize: "0.875rem", fontWeight: 600, margin: "0 0 0.5rem 0", color: "var(--color-accent, #d4a574)" }}>
                🔑 Key Takeaways
              </h2>
              <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                {keyTakeaways.map((t, i) => (
                  <li key={i} style={{ marginBottom: "0.25rem", fontSize: "0.8125rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                    <MarkdownText text={t} />
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Complete button */}
          <div style={{ marginTop: "2rem", display: "flex", justifyContent: "center" }}>
            {completed ? (
              <span style={{ color: "var(--color-success)", fontWeight: 600, fontSize: "0.875rem" }}>✓ Lesson completed</span>
            ) : (
              <button
                className="btn-glass btn-glass-primary"
                onClick={onMarkComplete}
                disabled={completing}
                aria-label="Mark lesson as complete"
                style={{ padding: "0.75rem 2.5rem", fontSize: "0.875rem" }}
              >
                {completing ? "Marking…" : "✓ Mark Complete"}
              </button>
            )}
          </div>
        </main>

        {/* Right: Practice panel + Study Buddy chat stacked, sticky */}
        <div
          style={{
            position: "sticky",
            top: "5rem",
            maxHeight: "calc(100vh - 6rem)",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "1.5rem",
          }}
        >
          <PracticePanel
            problems={practiceProblems}
            memoryAids={memoryAids}
            examStrategies={examStrategies}
            keyTakeaways={keyTakeaways}
            subtopicId={subtopicId}
            activeSectionIndex={activeIndex}
            lessonTitle={metadata.title}
          />

          {/* Study Buddy Chat — in right column below practice panel */}
          <section
            aria-label="Study Buddy"
            style={{
              padding: "0.75rem",
              background: "rgba(255, 255, 255, 0.02)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              borderRadius: "8px",
              flexShrink: 0,
            }}
          >
            <h3
              style={{
                fontSize: "0.75rem",
                fontWeight: 600,
                color: "var(--color-text)",
                margin: "0 0 0.5rem 0",
                display: "flex",
                alignItems: "center",
                gap: "0.375rem",
              }}
            >
              <span aria-hidden="true">🤖</span> Study Buddy
            </h3>
            <div style={{ height: "320px", display: "flex", flexDirection: "column" }}>
              <InlineLessonChat
                subtopicId={subtopicId}
                activeSectionIndex={activeIndex}
                lessonTitle={metadata.title}
              />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Section block with ref forwarding
// ---------------------------------------------------------------------------

const SectionBlock = forwardRef<HTMLDivElement, { section: LessonSection }>(
  function SectionBlock({ section }, ref) {
    return (
      <div
        ref={ref}
        style={{ marginBottom: "2.5rem", scrollMarginTop: "5rem" }}
      >
        <h2
          style={{
            fontSize: "1.125rem",
            fontWeight: 700,
            color: "var(--color-text)",
            margin: "0 0 0.75rem 0",
            paddingBottom: "0.5rem",
            borderBottom: "1px solid rgba(255,255,255,0.08)",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
          }}
        >
          {section.title}
          {section.difficulty.length > 0 && (
            <DifficultyBadges difficulties={section.difficulty} />
          )}
        </h2>

        {/* Render each typed block */}
        <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {section.blocks.map((block, i) => (
            <BlockRenderer key={i} block={block} />
          ))}
        </div>
      </div>
    );
  }
);

// ---------------------------------------------------------------------------
// Difficulty badges
// ---------------------------------------------------------------------------

function DifficultyBadges({ difficulties }: { difficulties: string[] }) {
  const colors: Record<string, string> = {
    easy: "rgba(80, 200, 120, 0.2)",
    medium: "rgba(212, 165, 116, 0.2)",
    hard: "rgba(220, 80, 80, 0.2)",
  };

  return (
    <span style={{ display: "inline-flex", gap: "0.25rem" }}>
      {difficulties.map((d) => (
        <span
          key={d}
          style={{
            fontSize: "0.5625rem",
            fontWeight: 700,
            padding: "0.1rem 0.35rem",
            borderRadius: "3px",
            background: colors[d] || "rgba(255,255,255,0.1)",
            textTransform: "uppercase",
            letterSpacing: "0.03em",
          }}
        >
          {d}
        </span>
      ))}
    </span>
  );
}


// ---------------------------------------------------------------------------
// Segmented lesson layout — one segment at a time with inline gate checks
// ---------------------------------------------------------------------------

/**
 * Renders clerical-ability (and other segmented) lessons as a sequence of
 * timed chunks (~3-5 min each). After reading each chunk the user answers
 * 2-3 inline checks before advancing to the next segment.
 *
 * Layout: two-column — left sidebar shows segment progress, right main content.
 */
function SegmentedLessonLayout({
  content,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: DesktopLessonLayoutProps) {
  const segments = content.segments!;
  const metadata = content.metadata;
  const [activeSegment, setActiveSegment] = useState(0);
  const [gateOpen, setGateOpen] = useState(false);
  const reducedMotion = useReducedMotion();
  const topRef = useRef<HTMLDivElement | null>(null);

  const currentSegment = segments[activeSegment];
  const isLastSegment = activeSegment === segments.length - 1;
  const hasChecks = currentSegment.checks.length > 0;

  function advanceSegment() {
    if (activeSegment < segments.length - 1) {
      setActiveSegment((i) => i + 1);
      setGateOpen(false);
      // Scroll back to top of content
      if (!reducedMotion) {
        topRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        topRef.current?.scrollIntoView({ block: "start" });
      }
    }
  }

  const practiceProblems = Array.isArray(content.practice_problems) ? content.practice_problems : [];
  const memoryAids = Array.isArray(content.memory_aids) ? content.memory_aids : [];
  const examStrategies = Array.isArray(content.exam_strategies) ? content.exam_strategies : [];
  const keyTakeaways = Array.isArray(content.key_takeaways) ? content.key_takeaways : [];

  return (
    <div
      className="desktop-lesson-root page"
      style={{ maxWidth: "1200px", margin: "0 auto", padding: "1.5rem 2rem 4rem" }}
    >
      {/* Top bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}
      >
        <Link
          to="/modules"
          aria-label="Back to modules"
          className="btn-glass"
          style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}
        >
          ← Back
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            ~{currentSegment.estimated_minutes} min this section
          </span>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            Part {activeSegment + 1} of {segments.length}
          </span>
        </div>
      </div>

      {/* Segment progress bar */}
      <GlassProgressBar value={activeSegment + (gateOpen ? 0.5 : 0)} max={segments.length} height={3} />

      {/* Two-column grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "200px 1fr",
          gap: "2rem",
          marginTop: "1.5rem",
          alignItems: "start",
        }}
      >
        {/* Left: segment navigation sidebar */}
        <aside
          style={{
            position: "sticky",
            top: "5rem",
            background: "rgba(255,255,255,0.02)",
            border: "1px solid rgba(255,255,255,0.07)",
            borderRadius: "8px",
            padding: "0.75rem",
          }}
          aria-label="Lesson parts"
        >
          {metadata.title && (
            <div
              style={{
                fontSize: "0.6875rem",
                fontWeight: 700,
                color: "var(--color-text-muted)",
                marginBottom: "0.75rem",
                textTransform: "uppercase",
                letterSpacing: "0.05em",
              }}
            >
              {metadata.title}
            </div>
          )}
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {segments.map((seg, idx) => {
              const isPast = idx < activeSegment;
              const isCurrent = idx === activeSegment;
              return (
                <li key={idx}>
                  <button
                    onClick={() => {
                      // Allow navigating back to completed segments
                      if (isPast || isCurrent) {
                        setActiveSegment(idx);
                        setGateOpen(false);
                      }
                    }}
                    disabled={idx > activeSegment}
                    aria-current={isCurrent ? "step" : undefined}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                      width: "100%",
                      padding: "0.4rem 0.5rem",
                      background: isCurrent ? "rgba(212, 165, 116, 0.08)" : "transparent",
                      border: "none",
                      borderLeft: isCurrent
                        ? "2px solid var(--color-accent, #d4a574)"
                        : "2px solid transparent",
                      borderRadius: "0 4px 4px 0",
                      cursor: idx > activeSegment ? "default" : "pointer",
                      textAlign: "left",
                      color: isCurrent
                        ? "var(--color-accent, #d4a574)"
                        : isPast
                        ? "var(--color-text-secondary)"
                        : "var(--color-text-muted)",
                      fontSize: "0.8125rem",
                      fontWeight: isCurrent ? 600 : 400,
                      marginBottom: "0.125rem",
                      opacity: idx > activeSegment ? 0.4 : 1,
                    }}
                  >
                    <span
                      style={{
                        fontSize: "0.625rem",
                        width: "1rem",
                        textAlign: "center",
                        flexShrink: 0,
                      }}
                    >
                      {isPast ? "✓" : isCurrent ? "▶" : "○"}
                    </span>
                    <span>
                      Part {idx + 1}
                      <span
                        style={{
                          display: "block",
                          fontSize: "0.625rem",
                          color: "var(--color-text-muted)",
                          fontWeight: 400,
                        }}
                      >
                        ~{seg.estimated_minutes} min
                      </span>
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        </aside>

        {/* Center+Right: content + gate */}
        <main
          ref={topRef}
          aria-label="Lesson content"
          style={{ minWidth: 0, overflow: "hidden" }}
        >
          {metadata.title && (
            <h1
              style={{
                fontSize: "1.5rem",
                fontWeight: 700,
                color: "var(--color-text)",
                margin: "0 0 1.5rem 0",
              }}
            >
              {metadata.title}
            </h1>
          )}

          {/* Sections in current segment */}
          {currentSegment.sections.map((section, idx) => (
            <SectionBlock key={idx} section={section} />
          ))}

          {/* Gate: checks OR direct advance */}
          {!gateOpen ? (
            <div
              style={{
                marginTop: "2rem",
                display: "flex",
                justifyContent: "center",
              }}
            >
              {hasChecks ? (
                <button
                  className="btn-glass btn-glass-primary"
                  onClick={() => setGateOpen(true)}
                  style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
                >
                  Check understanding →
                </button>
              ) : isLastSegment ? null : (
                <button
                  className="btn-glass btn-glass-primary"
                  onClick={advanceSegment}
                  style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
                >
                  Continue to Part {activeSegment + 2} →
                </button>
              )}
            </div>
          ) : (
            <SegmentGatePanel
              checks={currentSegment.checks}
              isLastSegment={isLastSegment}
              onAdvance={advanceSegment}
              onComplete={onMarkComplete}
              completing={completing}
              completed={completed}
            />
          )}

          {/* On last segment, show key takeaways + complete button inline */}
          {isLastSegment && gateOpen && (
            <>
              {keyTakeaways.length > 0 && (
                <div
                  style={{
                    marginTop: "2rem",
                    padding: "1rem 1.25rem",
                    background: "rgba(212, 165, 116, 0.04)",
                    border: "1px solid rgba(212, 165, 116, 0.15)",
                    borderRadius: "8px",
                  }}
                >
                  <h2
                    style={{
                      fontSize: "0.875rem",
                      fontWeight: 600,
                      margin: "0 0 0.5rem 0",
                      color: "var(--color-accent, #d4a574)",
                    }}
                  >
                    🔑 Key Takeaways
                  </h2>
                  <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
                    {keyTakeaways.map((t, i) => (
                      <li
                        key={i}
                        style={{
                          marginBottom: "0.25rem",
                          fontSize: "0.8125rem",
                          lineHeight: 1.5,
                          color: "var(--color-text)",
                        }}
                      >
                        <MarkdownText text={t} />
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {content.summary && (
                <div
                  style={{
                    marginTop: "1.5rem",
                    padding: "1rem 1.25rem",
                    background: "rgba(212, 165, 116, 0.04)",
                    border: "1px solid rgba(212, 165, 116, 0.15)",
                    borderRadius: "8px",
                  }}
                >
                  <h2
                    style={{
                      fontSize: "0.875rem",
                      fontWeight: 600,
                      margin: "0 0 0.5rem 0",
                      color: "var(--color-accent, #d4a574)",
                    }}
                  >
                    📝 Summary
                  </h2>
                  <MarkdownText
                    text={content.summary}
                    style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }}
                  />
                </div>
              )}
            </>
          )}

          {/* Practice panel sticks to bottom of content on last segment */}
          {isLastSegment && (practiceProblems.length > 0 || memoryAids.length > 0 || examStrategies.length > 0) && (
            <div style={{ marginTop: "2rem" }}>
              <PracticePanel
                problems={practiceProblems}
                memoryAids={memoryAids}
                examStrategies={examStrategies}
                keyTakeaways={keyTakeaways}
                subtopicId={subtopicId}
                activeSectionIndex={0}
                lessonTitle={metadata.title}
              />
            </div>
          )}

          {/* Study Buddy always present */}
          <section
            aria-label="Study Buddy"
            style={{
              marginTop: "1.5rem",
              padding: "0.75rem",
              background: "rgba(255, 255, 255, 0.02)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              borderRadius: "8px",
            }}
          >
            <h3
              style={{
                fontSize: "0.75rem",
                fontWeight: 600,
                color: "var(--color-text)",
                margin: "0 0 0.5rem 0",
                display: "flex",
                alignItems: "center",
                gap: "0.375rem",
              }}
            >
              <span aria-hidden="true">🤖</span> Study Buddy
            </h3>
            <div style={{ height: "260px", display: "flex", flexDirection: "column" }}>
              <InlineLessonChat
                subtopicId={subtopicId}
                activeSectionIndex={activeSegment}
                lessonTitle={metadata.title}
              />
            </div>
          </section>
        </main>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Segment gate: shows inline checks before allowing advance
// ---------------------------------------------------------------------------

interface SegmentGatePanelProps {
  checks: InlineCheck[];
  isLastSegment: boolean;
  onAdvance: () => void;
  onComplete: () => void;
  completing: boolean;
  completed: boolean;
}

function SegmentGatePanel({
  checks,
  isLastSegment,
  onAdvance,
  onComplete,
  completing,
  completed,
}: SegmentGatePanelProps) {
  const [revealed, setRevealed] = useState<Set<number>>(new Set());

  // Allow advancing once at least one check is revealed (soft gate — show, don't block)
  const canAdvance = checks.length === 0 || revealed.size > 0;

  function toggle(i: number) {
    setRevealed((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  }

  return (
    <div
      style={{
        marginTop: "2rem",
        padding: "1.25rem",
        background: "rgba(80, 200, 120, 0.04)",
        border: "1px solid rgba(80, 200, 120, 0.2)",
        borderRadius: "8px",
      }}
    >
      <div
        style={{
          fontSize: "0.75rem",
          fontWeight: 700,
          color: "rgba(80, 200, 120, 0.9)",
          marginBottom: "1rem",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
        }}
      >
        ✓ Quick Check — before you continue
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem", marginBottom: "1.25rem" }}>
        {checks.map((check, i) => {
          const isOpen = revealed.has(i);
          return (
            <div
              key={i}
              style={{
                background: "rgba(255,255,255,0.02)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "6px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  padding: "0.625rem 0.875rem",
                  fontSize: "0.875rem",
                  lineHeight: 1.55,
                  color: "var(--color-text)",
                  fontWeight: 500,
                }}
              >
                <MarkdownText text={`${i + 1}. ${check.question}`} />
              </div>
              <button
                onClick={() => toggle(i)}
                aria-expanded={isOpen}
                style={{
                  display: "block",
                  width: "100%",
                  padding: "0.4rem 0.875rem",
                  background: isOpen ? "rgba(80, 200, 120, 0.1)" : "rgba(255,255,255,0.03)",
                  border: "none",
                  borderTop: "1px solid rgba(255,255,255,0.06)",
                  cursor: "pointer",
                  textAlign: "left",
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: isOpen ? "rgba(80, 200, 120, 0.9)" : "var(--color-text-muted)",
                }}
              >
                {isOpen ? "▾ Hide answer" : "▸ Reveal answer"}
              </button>
              {isOpen && (
                <div
                  style={{
                    padding: "0.625rem 0.875rem",
                    background: "rgba(80, 200, 120, 0.06)",
                    borderTop: "1px solid rgba(80, 200, 120, 0.15)",
                    fontSize: "0.875rem",
                    lineHeight: 1.55,
                    color: "var(--color-text)",
                  }}
                >
                  <MarkdownText text={check.answer} />
                  {check.rationale && (
                    <div
                      style={{
                        marginTop: "0.375rem",
                        fontSize: "0.8125rem",
                        color: "var(--color-text-muted)",
                        fontStyle: "italic",
                      }}
                    >
                      <MarkdownText text={check.rationale} />
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Advance / Complete button */}
      <div style={{ display: "flex", justifyContent: "flex-end" }}>
        {completed ? (
          <span style={{ color: "var(--color-success)", fontWeight: 600, fontSize: "0.875rem" }}>
            ✓ Lesson completed
          </span>
        ) : isLastSegment ? (
          <button
            className="btn-glass btn-glass-primary"
            onClick={onComplete}
            disabled={completing || !canAdvance}
            aria-label="Mark lesson as complete"
            style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
          >
            {completing ? "Marking…" : "✓ Mark Complete"}
          </button>
        ) : (
          <button
            className="btn-glass btn-glass-primary"
            onClick={onAdvance}
            disabled={!canAdvance}
            aria-label="Continue to next part"
            style={{ padding: "0.625rem 2rem", fontSize: "0.875rem" }}
          >
            Continue →
          </button>
        )}
      </div>
    </div>
  );
}
