import type { LessonSection, LessonMetadata } from "./types";

interface SidebarTOCProps {
  sections: LessonSection[];
  metadata: LessonMetadata;
  activeIndex: number;
  onNavigate: (index: number) => void;
}

/**
 * Persistent sidebar table-of-contents for desktop layout.
 * Shows section titles with scroll-spy highlighting, reading time, and progress.
 */
export function SidebarTOC({ sections, metadata, activeIndex, onNavigate }: SidebarTOCProps) {
  const completedSections = activeIndex + 1;
  const progressPercent = Math.round((completedSections / sections.length) * 100);

  return (
    <aside
      aria-label="Table of contents"
      style={{
        position: "sticky",
        top: "5rem",
        maxHeight: "calc(100vh - 6rem)",
        overflowY: "auto",
        paddingRight: "0.75rem",
        scrollbarWidth: "thin",
      }}
    >
      {/* Metadata header */}
      <div style={{ marginBottom: "1rem", paddingBottom: "0.75rem", borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginBottom: "0.25rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
          Reading Time
        </div>
        <div style={{ fontSize: "0.875rem", fontWeight: 600, color: "var(--color-text)" }}>
          ~{metadata.estimated_reading_minutes} min
        </div>
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginTop: "0.375rem" }}>
          {metadata.section_count} sections · {metadata.total_word_count.toLocaleString()} words
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ marginBottom: "1rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.625rem", color: "var(--color-text-muted)", marginBottom: "0.25rem" }}>
          <span>Progress</span>
          <span>{progressPercent}%</span>
        </div>
        <div style={{ height: "3px", borderRadius: "2px", background: "rgba(255,255,255,0.08)", overflow: "hidden" }}>
          <div
            style={{
              width: `${progressPercent}%`,
              height: "100%",
              background: "var(--color-accent, #d4a574)",
              borderRadius: "2px",
              transition: "width 0.3s ease",
            }}
          />
        </div>
      </div>

      {/* Section list */}
      <nav>
        <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
          {sections.map((section, idx) => {
            const isActive = idx === activeIndex;
            const isPast = idx < activeIndex;

            return (
              <li key={idx} style={{ marginBottom: "0.125rem" }}>
                <button
                  onClick={() => onNavigate(idx)}
                  title={section.title}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: "0.5rem",
                    width: "100%",
                    padding: "0.375rem 0.5rem",
                    background: isActive ? "rgba(212, 165, 116, 0.1)" : "transparent",
                    border: "none",
                    borderLeft: isActive ? "2px solid var(--color-accent, #d4a574)" : "2px solid transparent",
                    borderRadius: "0 4px 4px 0",
                    cursor: "pointer",
                    textAlign: "left",
                    transition: "all 0.15s ease",
                    color: isActive
                      ? "var(--color-accent, #d4a574)"
                      : isPast
                        ? "var(--color-text-secondary)"
                        : "var(--color-text-muted)",
                  }}
                >
                  {/* Section number indicator */}
                  <span
                    style={{
                      flexShrink: 0,
                      width: "1.25rem",
                      height: "1.25rem",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      borderRadius: "50%",
                      fontSize: "0.625rem",
                      fontWeight: 600,
                      background: isActive
                        ? "rgba(212, 165, 116, 0.2)"
                        : isPast
                          ? "rgba(80, 200, 120, 0.15)"
                          : "rgba(255,255,255,0.05)",
                      color: isActive
                        ? "var(--color-accent, #d4a574)"
                        : isPast
                          ? "rgba(80, 200, 120, 0.8)"
                          : "var(--color-text-muted)",
                    }}
                  >
                    {isPast ? "✓" : idx + 1}
                  </span>

                  {/* Title and time */}
                  <div style={{ minWidth: 0 }}>
                    <div
                      style={{
                        fontSize: "0.75rem",
                        fontWeight: isActive ? 600 : 400,
                        lineHeight: 1.3,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {section.title}
                    </div>
                    <div style={{ fontSize: "0.5625rem", color: "var(--color-text-muted)", marginTop: "0.125rem" }}>
                      {Math.ceil(section.estimated_reading_seconds / 60)} min
                      {section.difficulty.length > 0 && (
                        <> · {section.difficulty.join(", ")}</>
                      )}
                    </div>
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
