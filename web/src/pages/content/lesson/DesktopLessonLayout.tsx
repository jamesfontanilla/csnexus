import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import type { EnhancedLessonContent, LessonSection } from "./types";
import { BlockRenderer } from "./BlockRenderer";
import { SidebarTOC } from "./SidebarTOC";
import { PracticePanel } from "./PracticePanel";
import { GlassProgressBar } from "../../../components/GlassProgressBar";
import { MarkdownText } from "../../../components/MarkdownText";

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
 */
export function DesktopLessonLayout({
  content,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: DesktopLessonLayoutProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Use enhanced sections if available, fall back to legacy
  const hasEnhancedSections = content.sections && content.sections.length > 0;
  const sections = hasEnhancedSections ? content.sections : [];

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
    sectionRefs.current[idx]?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // If no enhanced sections, fall back to legacy rendering
  if (!hasEnhancedSections) {
    return <LegacyDesktopFallback content={content} subtopicId={subtopicId} onMarkComplete={onMarkComplete} completing={completing} completed={completed} />;
  }

  const hasPracticeContent =
    content.practice_problems.length > 0 ||
    content.memory_aids.length > 0 ||
    content.exam_strategies.length > 0 ||
    content.key_takeaways.length > 0;

  return (
    <div style={{ maxWidth: "1400px", margin: "0 auto", padding: "1.5rem 2rem 4rem" }}>
      {/* Top bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
          ← Back
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            ~{content.metadata.estimated_reading_minutes} min read
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
          gridTemplateColumns: hasPracticeContent ? "220px 1fr 280px" : "220px 1fr",
          gap: "2rem",
          marginTop: "1.5rem",
          alignItems: "start",
        }}
      >
        {/* Left: TOC sidebar */}
        <SidebarTOC
          sections={sections}
          metadata={content.metadata}
          activeIndex={activeIndex}
          onNavigate={scrollToSection}
        />

        {/* Center: Main content */}
        <main aria-label="Lesson content" style={{ minWidth: 0 }}>
          {/* Title */}
          {content.metadata.title && (
            <h1 style={{ fontSize: "1.5rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 1.5rem 0" }}>
              {content.metadata.title}
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

        {/* Right: Practice panel */}
        {hasPracticeContent && (
          <PracticePanel
            problems={content.practice_problems}
            memoryAids={content.memory_aids}
            examStrategies={content.exam_strategies}
            keyTakeaways={content.key_takeaways}
          />
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Section block with ref forwarding
// ---------------------------------------------------------------------------

import { forwardRef } from "react";

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
// Legacy fallback (when enhanced sections aren't available)
// ---------------------------------------------------------------------------

function LegacyDesktopFallback({
  content,
  subtopicId: _subtopicId,
  onMarkComplete,
  completing,
  completed,
}: DesktopLessonLayoutProps) {
  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "1.5rem 2rem 4rem" }}>
      <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem", marginBottom: "1rem", display: "inline-block" }}>
        ← Back
      </Link>

      <article>
        {content.explanations.map((exp, i) => (
          <div key={i} style={{ marginBottom: "2rem" }}>
            {(exp.title || exp.heading) && (
              <h2 style={{ fontSize: "1.125rem", fontWeight: 700, color: "var(--color-text)", margin: "0 0 0.75rem 0" }}>
                {exp.title || exp.heading}
              </h2>
            )}
            <MarkdownText text={exp.body} style={{ lineHeight: 1.7, fontSize: "0.9rem", color: "var(--color-text)" }} />
          </div>
        ))}

        {content.key_takeaways.length > 0 && (
          <div style={{ marginTop: "2rem", padding: "1rem", background: "rgba(212, 165, 116, 0.04)", border: "1px solid rgba(212, 165, 116, 0.15)", borderRadius: "8px" }}>
            <h2 style={{ fontSize: "0.875rem", fontWeight: 600, margin: "0 0 0.5rem 0", color: "var(--color-accent, #d4a574)" }}>
              🔑 Key Takeaways
            </h2>
            <ul style={{ margin: 0, paddingLeft: "1.25rem" }}>
              {content.key_takeaways.map((t, i) => (
                <li key={i} style={{ marginBottom: "0.25rem", fontSize: "0.8125rem", lineHeight: 1.5, color: "var(--color-text)" }}>{t}</li>
              ))}
            </ul>
          </div>
        )}

        {content.summary && (
          <div style={{ marginTop: "1.5rem" }}>
            <h2 style={{ fontSize: "0.875rem", fontWeight: 600, margin: "0 0 0.5rem 0", color: "var(--color-text)" }}>📝 Summary</h2>
            <MarkdownText text={content.summary} style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }} />
          </div>
        )}
      </article>

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
    </div>
  );
}
