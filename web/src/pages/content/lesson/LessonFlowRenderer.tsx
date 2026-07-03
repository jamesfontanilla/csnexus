import { useEffect, useMemo, useState } from "react";
import type { CSSProperties, ReactNode } from "react";
import { Link } from "react-router-dom";
import type {
  EnhancedLessonContent,
  LessonScreen,
  LessonScreenPlan,
  LessonSection,
} from "./types";
import { BlockRenderer } from "./BlockRenderer";
import { PracticePanel, InlineLessonChat } from "./PracticePanel";
import { LessonChatPanel } from "./LessonChatPanel";
import { GlassProgressBar } from "../../../components/GlassProgressBar";
import { GlassCard } from "../../../components/GlassCard";
import { MarkdownText } from "../../../components/MarkdownText";
import { useReducedMotion } from "../../../design-system/motion";

interface LessonFlowRendererProps {
  content: EnhancedLessonContent;
  subtopicId: string;
  onMarkComplete: () => void;
  completing: boolean;
  completed: boolean;
  layout: "desktop" | "mobile";
}

export function LessonFlowRenderer({
  content,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
  layout,
}: LessonFlowRendererProps) {
  const plan = content.screen_plan;

  if (!plan || plan.screens.length === 0) {
    return null;
  }

  return layout === "desktop" ? (
    <DesktopLessonFlow
      content={content}
      plan={plan}
      subtopicId={subtopicId}
      onMarkComplete={onMarkComplete}
      completing={completing}
      completed={completed}
    />
  ) : (
    <MobileLessonFlow
      content={content}
      plan={plan}
      subtopicId={subtopicId}
      onMarkComplete={onMarkComplete}
      completing={completing}
      completed={completed}
    />
  );
}

interface FlowProps {
  content: EnhancedLessonContent;
  plan: LessonScreenPlan;
  subtopicId: string;
  onMarkComplete: () => void;
  completing: boolean;
  completed: boolean;
}

function DesktopLessonFlow({
  content,
  plan,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: FlowProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [bookmarked, setBookmarked] = useState(false);
  const reducedMotion = useReducedMotion();

  const current = plan.screens[activeIndex];
  const currentSections = useMemo(
    () => resolveSections(content.sections ?? [], current.section_indices),
    [content.sections, current.section_indices]
  );

  useEffect(() => {
    setActiveIndex(0);
    setBookmarked(false);
  }, [plan.screen_count, subtopicId]);

  function goTo(index: number) {
    if (index < 0 || index >= plan.screens.length) return;
    setActiveIndex(index);
    if (!reducedMotion) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      window.scrollTo(0, 0);
    }
  }

  const practiceProblems = Array.isArray(content.practice_problems) ? content.practice_problems : [];
  const memoryAids = Array.isArray(content.memory_aids) ? content.memory_aids : [];
  const examStrategies = Array.isArray(content.exam_strategies) ? content.exam_strategies : [];
  const keyTakeaways = Array.isArray(content.key_takeaways) ? content.key_takeaways : [];
  const lessonTitle = plan.title || content.metadata?.title || "";

  return (
    <div
      className="desktop-lesson-root page"
      style={{
        maxWidth: "1400px",
        margin: "0 auto",
        padding: "1.5rem 2rem 1rem",
        display: "flex",
        flexDirection: "column",
        minHeight: "100dvh",
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem", gap: "1rem" }}>
        <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
          Back
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", minWidth: 0 }}>
          <button
            type="button"
            onClick={() => setBookmarked((value) => !value)}
            aria-pressed={bookmarked}
            aria-label={bookmarked ? "Remove bookmark" : "Bookmark lesson"}
            className="btn-glass"
            style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}
          >
            {bookmarked ? "Bookmarked" : "Bookmark"}
          </button>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)", whiteSpace: "nowrap" }}>
            ~{plan.estimated_reading_minutes} min
          </span>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)", whiteSpace: "nowrap" }}>
            {activeIndex + 1} / {plan.screen_count}
          </span>
        </div>
      </div>

      <GlassProgressBar value={activeIndex + 1} max={plan.screen_count} height={3} />

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "230px minmax(0, 1fr) 300px",
          gap: "1.5rem",
          marginTop: "1.5rem",
          alignItems: "stretch",
          flex: "1 1 auto",
          minHeight: 0,
          overflow: "hidden",
        }}
      >
        <ScreenNavigator plan={plan} activeIndex={activeIndex} onNavigate={goTo} />

        <main
          aria-label="Lesson screen"
          style={{
            minWidth: 0,
            maxWidth: 720,
            margin: "0 auto",
            width: "100%",
            minHeight: 0,
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <ScreenChrome
            screen={current}
            lessonTitle={lessonTitle}
            screenCount={plan.screen_count}
            activeIndex={activeIndex}
            onPrevious={() => goTo(activeIndex - 1)}
            onNext={() => goTo(activeIndex + 1)}
            onComplete={onMarkComplete}
            completing={completing}
            completed={completed}
          >
            <ScreenBody
              content={content}
              plan={plan}
              screen={current}
              currentSections={currentSections}
              subtopicId={subtopicId}
            />
          </ScreenChrome>
        </main>

        <aside
          style={{
            position: "sticky",
            top: "5rem",
            maxHeight: "calc(100vh - 6rem)",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "1.25rem",
          }}
        >
          <PracticePanel
            problems={practiceProblems}
            memoryAids={memoryAids}
            examStrategies={examStrategies}
            keyTakeaways={keyTakeaways}
            subtopicId={subtopicId}
            activeSectionIndex={current.section_indices[0] ?? activeIndex}
            lessonTitle={lessonTitle}
          />

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
            <h3 style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--color-text)", margin: "0 0 0.5rem 0" }}>
              Study Buddy
            </h3>
            <div style={{ height: "320px", display: "flex", flexDirection: "column" }}>
              <InlineLessonChat
                subtopicId={subtopicId}
                activeSectionIndex={current.section_indices[0] ?? activeIndex}
                lessonTitle={lessonTitle}
              />
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

function MobileLessonFlow({
  content,
  plan,
  subtopicId,
  onMarkComplete,
  completing,
  completed,
}: FlowProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const [bookmarked, setBookmarked] = useState(false);
  const reducedMotion = useReducedMotion();

  const current = plan.screens[activeIndex];
  const currentSections = useMemo(
    () => resolveSections(content.sections ?? [], current.section_indices),
    [content.sections, current.section_indices]
  );

  useEffect(() => {
    setActiveIndex(0);
    setBookmarked(false);
  }, [plan.screen_count, subtopicId]);

  function goTo(index: number) {
    if (index < 0 || index >= plan.screens.length) return;
    setActiveIndex(index);
    if (!reducedMotion) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      window.scrollTo(0, 0);
    }
  }

  const practiceProblems = Array.isArray(content.practice_problems) ? content.practice_problems : [];
  const memoryAids = Array.isArray(content.memory_aids) ? content.memory_aids : [];
  const examStrategies = Array.isArray(content.exam_strategies) ? content.exam_strategies : [];
  const keyTakeaways = Array.isArray(content.key_takeaways) ? content.key_takeaways : [];
  const lessonTitle = plan.title || content.metadata?.title || "";

  return (
    <div
      className="page container"
      style={{
        maxWidth: 680,
        margin: "0 auto",
        paddingBottom: "1rem",
        lineHeight: 1.75,
        display: "flex",
        flexDirection: "column",
        minHeight: "100dvh",
        overflow: "hidden",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem", gap: "0.75rem" }}>
        <Link to="/modules" aria-label="Back to modules" className="btn-glass" style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}>
          Back
        </Link>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <button
            type="button"
            onClick={() => setBookmarked((value) => !value)}
            aria-pressed={bookmarked}
            aria-label={bookmarked ? "Remove bookmark" : "Bookmark lesson"}
            className="btn-glass"
            style={{ padding: "0.3rem 0.6rem", fontSize: "0.75rem" }}
          >
            {bookmarked ? "Bookmarked" : "Bookmark"}
          </button>
          <span style={{ fontSize: "0.75rem", color: "var(--color-text-muted)" }}>
            {activeIndex + 1} / {plan.screen_count}
          </span>
        </div>
      </div>

      <GlassProgressBar value={activeIndex + 1} max={plan.screen_count} height={3} />

      <div style={{ flex: "1 1 auto", minHeight: 0, overflow: "hidden", display: "flex", flexDirection: "column" }}>
        <ScreenChrome
          screen={current}
          lessonTitle={lessonTitle}
          screenCount={plan.screen_count}
          activeIndex={activeIndex}
          onPrevious={() => goTo(activeIndex - 1)}
          onNext={() => goTo(activeIndex + 1)}
          onComplete={onMarkComplete}
          completing={completing}
          completed={completed}
          compact
        >
          <ScreenBody
            content={content}
            plan={plan}
            screen={current}
            currentSections={currentSections}
            subtopicId={subtopicId}
            compact
          />
        </ScreenChrome>
      </div>

      {current.kind !== "practice" && (practiceProblems.length > 0 || memoryAids.length > 0 || examStrategies.length > 0) && (
        <div style={{ marginTop: "1.5rem" }}>
          <PracticePanel
            problems={practiceProblems}
            memoryAids={memoryAids}
            examStrategies={examStrategies}
            keyTakeaways={keyTakeaways}
            subtopicId={subtopicId}
            activeSectionIndex={current.section_indices[0] ?? activeIndex}
            lessonTitle={lessonTitle}
          />
        </div>
      )}

      <MobileScreenNavigator
        plan={plan}
        activeIndex={activeIndex}
        onNavigate={goTo}
      />

      <LessonChatPanel
        subtopicId={subtopicId}
        activeSectionIndex={current.section_indices[0] ?? activeIndex}
        lessonTitle={lessonTitle}
      />
    </div>
  );
}

function ScreenChrome({
  screen,
  lessonTitle,
  screenCount,
  activeIndex,
  onPrevious,
  onNext,
  onComplete,
  completing,
  completed,
  compact = false,
  children,
}: {
  screen: LessonScreen;
  lessonTitle: string;
  screenCount: number;
  activeIndex: number;
  onPrevious: () => void;
  onNext: () => void;
  onComplete: () => void;
  completing: boolean;
  completed: boolean;
  compact?: boolean;
  children: ReactNode;
}) {
  const hasPrevious = activeIndex > 0;
  const hasNext = activeIndex < screenCount - 1;

  return (
    <article
      style={{
        marginTop: compact ? "1rem" : 0,
        padding: compact ? "0" : "0",
        height: "100%",
        minHeight: 0,
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "0.75rem",
          marginBottom: "0.75rem",
          flexWrap: "wrap",
        }}
      >
        <div style={{ minWidth: 0 }}>
          <div style={{ fontSize: "0.6875rem", fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--color-accent, #d4a574)" }}>
            {screenLabel(screen.kind)}
          </div>
          <h1 style={{ fontSize: compact ? "1.25rem" : "1.5rem", fontWeight: 700, color: "var(--color-text)", margin: "0.25rem 0 0" }}>
            {screen.title || lessonTitle}
          </h1>
        </div>

        <div style={{ textAlign: "right", color: "var(--color-text-muted)", fontSize: "0.75rem" }}>
          Screen {screen.index + 1} of {screenCount}
          <div>{screen.call_to_action || "Continue learning"}</div>
        </div>
      </div>

      <GlassCard
        blur="sm"
        style={{
          padding: compact ? "0.95rem" : "1.1rem 1.2rem",
          borderRadius: "12px",
          flex: "1 1 auto",
          minHeight: 0,
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {screen.summary && (
          <div style={{ marginBottom: "1rem", color: "var(--color-text-muted)", fontSize: compact ? "0.8rem" : "0.875rem", lineHeight: 1.65 }}>
            {screen.summary}
          </div>
        )}

        <div style={{ minHeight: 0, overflow: "hidden", display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          {children}
        </div>
      </GlassCard>

      <div style={{ display: "flex", justifyContent: "space-between", gap: "0.5rem", marginTop: "1rem", flexWrap: "wrap" }}>
        <button
          type="button"
          className="btn-glass"
          onClick={onPrevious}
          disabled={!hasPrevious}
          style={{ padding: "0.625rem 1rem", minWidth: "7rem" }}
        >
          Previous
        </button>
        {completed ? (
          <span style={{ color: "var(--color-success)", fontWeight: 600, alignSelf: "center" }}>
            Lesson completed
          </span>
        ) : hasNext ? (
          <button
            type="button"
            className="btn-glass btn-glass-primary"
            onClick={onNext}
            style={{ padding: "0.625rem 1rem", minWidth: "7rem" }}
          >
            Next
          </button>
        ) : (
          <button
            type="button"
            className="btn-glass btn-glass-primary"
            onClick={onComplete}
            disabled={completing}
            style={{ padding: "0.625rem 1rem", minWidth: "7rem" }}
          >
            {completing ? "Marking..." : "Complete"}
          </button>
        )}
      </div>
    </article>
  );
}

function ScreenBody({
  content,
  plan,
  screen,
  currentSections,
  subtopicId,
  compact = false,
}: {
  content: EnhancedLessonContent;
  plan: LessonScreenPlan;
  screen: LessonScreen;
  currentSections: LessonSection[];
  subtopicId: string;
  compact?: boolean;
}) {
  const lessonTitle = plan.title || content.metadata?.title || "";

  switch (screen.kind) {
    case "cover":
      return (
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <p style={{ margin: 0, color: "var(--color-text)", fontSize: compact ? "0.9rem" : "1rem", lineHeight: 1.7 }}>
            {content.summary}
          </p>
          <div style={{ display: "grid", gap: "0.75rem" }}>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
              <Badge>~{plan.estimated_reading_minutes} min</Badge>
              <Badge>{plan.screen_count} screens</Badge>
              <Badge>{content.metadata?.section_count ?? currentSections.length} sections</Badge>
            </div>
            {plan.objective && (
              <GlassCard blur="sm" style={{ padding: "0.9rem 1rem", background: "rgba(212, 165, 116, 0.05)" }}>
                <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-accent, #d4a574)" }}>
                  Learning outcome
                </div>
                <div style={{ marginTop: "0.35rem", lineHeight: 1.7, color: "var(--color-text)" }}>
                  {plan.objective}
                </div>
              </GlassCard>
            )}
            {plan.must_know.length > 0 && (
              <GlassCard blur="sm" style={{ padding: "0.9rem 1rem" }}>
                <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-text-muted)" }}>
                  Must know
                </div>
                <ul style={{ margin: "0.65rem 0 0", paddingLeft: "1.25rem" }}>
                  {plan.must_know.slice(0, 4).map((item, index) => (
                    <li key={index} style={{ marginBottom: "0.35rem", lineHeight: 1.6, color: "var(--color-text)" }}>
                      {item}
                    </li>
                  ))}
                </ul>
              </GlassCard>
            )}
          </div>
        </div>
      );

    case "objectives":
      return (
        <ListCard
          title="Learning objectives"
          items={content.learning_objectives.length > 0 ? content.learning_objectives : plan.must_know}
        />
      );

    case "overview":
      return (
        <div style={{ display: "grid", gap: "0.75rem" }}>
          <GlassCard blur="sm" style={{ padding: "0.9rem 1rem" }}>
            <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-text-muted)" }}>
              Section map
            </div>
            <ul style={{ margin: "0.75rem 0 0", paddingLeft: "1.25rem" }}>
              {(content.table_of_contents || []).map((entry) => (
                <li key={entry.index} style={{ marginBottom: "0.35rem", lineHeight: 1.6 }}>
                  {entry.title}
                </li>
              ))}
            </ul>
          </GlassCard>
        </div>
      );

    case "practice":
      return (
        <PracticePanel
          problems={content.practice_problems ?? []}
          memoryAids={content.memory_aids ?? []}
          examStrategies={content.exam_strategies ?? []}
          keyTakeaways={content.key_takeaways ?? []}
          subtopicId={subtopicId}
          activeSectionIndex={screen.section_indices[0] ?? 0}
          lessonTitle={lessonTitle}
        />
      );

    case "remember":
      return <ListCard title="Memory aids" items={content.memory_aids ?? []} />;

    case "strategy":
      return <ListCard title="Exam strategies" items={content.exam_strategies ?? []} />;

    case "takeaway":
    case "summary":
      return (
        <div style={{ display: "grid", gap: "0.75rem" }}>
          <ListCard title="Key takeaways" items={content.key_takeaways ?? []} />
          {content.summary && (
            <GlassCard blur="sm" style={{ padding: "0.9rem 1rem" }}>
              <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-text-muted)" }}>
                Summary
              </div>
              <div style={{ marginTop: "0.5rem", lineHeight: 1.7 }}>
                <MarkdownText text={content.summary} />
              </div>
            </GlassCard>
          )}
        </div>
      );

    case "completion":
      return (
        <div style={{ display: "grid", gap: "0.75rem" }}>
          <GlassCard blur="sm" style={{ padding: "1rem 1.1rem", background: "rgba(80, 200, 120, 0.04)" }}>
            <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "rgba(80, 200, 120, 0.9)" }}>
              Complete
            </div>
            <p style={{ margin: "0.6rem 0 0", lineHeight: 1.7, color: "var(--color-text)" }}>
              You have reached the end of {lessonTitle || "the lesson"}. Review the takeaways, then mark the lesson complete when you are ready.
            </p>
          </GlassCard>
        </div>
      );

    default:
      return (
        <div style={{ display: "grid", gap: "1rem" }}>
          {currentSections.map((section, index) => (
            <SectionCard key={`${section.title}-${index}`} section={section} depth={0} />
          ))}
        </div>
      );
  }
}

function SectionCard({ section, depth }: { section: LessonSection; depth: number }) {
  const headingStyle: CSSProperties = {
    fontSize: depth === 0 ? "1.05rem" : depth === 1 ? "0.95rem" : "0.875rem",
    fontWeight: depth === 0 ? 700 : 600,
    color: "var(--color-text)",
    margin: "0 0 0.75rem 0",
    paddingBottom: "0.45rem",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
  };

  return (
    <section style={{ paddingLeft: depth > 0 ? "0.75rem" : 0 }}>
      <h2 style={headingStyle}>{section.title}</h2>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {section.blocks.map((block, index) => (
          <BlockRenderer key={`${section.title}-${index}`} block={block} />
        ))}
      </div>
      {section.subsections?.length ? (
        <div style={{ marginTop: "0.9rem", display: "grid", gap: "0.9rem" }}>
          {section.subsections.map((subsection, index) => (
            <SectionCard key={`${subsection.title}-${index}`} section={subsection} depth={depth + 1} />
          ))}
        </div>
      ) : null}
    </section>
  );
}

function ScreenNavigator({
  plan,
  activeIndex,
  onNavigate,
}: {
  plan: LessonScreenPlan;
  activeIndex: number;
  onNavigate: (index: number) => void;
}) {
  return (
    <aside
      aria-label="Lesson screens"
      style={{
        position: "sticky",
        top: "5rem",
        maxHeight: "calc(100vh - 6rem)",
        overflowY: "auto",
        paddingRight: "0.5rem",
      }}
    >
      <div style={{ marginBottom: "1rem", paddingBottom: "0.75rem", borderBottom: "1px solid rgba(255,255,255,0.08)" }}>
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginBottom: "0.25rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
          Screen flow
        </div>
        <div style={{ fontSize: "0.875rem", fontWeight: 600, color: "var(--color-text)" }}>
          {plan.screen_count} screens
        </div>
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginTop: "0.35rem" }}>
          {plan.estimated_reading_minutes} minute guide
        </div>
      </div>

      <nav>
        <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
          {plan.screens.map((screen) => {
            const isActive = screen.index === activeIndex;
            const isPast = screen.index < activeIndex;
            return (
              <li key={screen.index} style={{ marginBottom: "0.25rem" }}>
                <button
                  type="button"
                  onClick={() => onNavigate(screen.index)}
                  aria-current={isActive ? "step" : undefined}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: "0.55rem",
                    width: "100%",
                    padding: "0.4rem 0.5rem",
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
                      fontWeight: 700,
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
                    {isPast ? "✓" : screen.index + 1}
                  </span>
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontSize: "0.75rem", fontWeight: isActive ? 600 : 400, lineHeight: 1.3 }}>
                      {screen.title}
                    </div>
                    <div style={{ fontSize: "0.5625rem", color: "var(--color-text-muted)", marginTop: "0.125rem" }}>
                      {screenLabel(screen.kind)}
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

function MobileScreenNavigator({
  plan,
  activeIndex,
  onNavigate,
}: {
  plan: LessonScreenPlan;
  activeIndex: number;
  onNavigate: (index: number) => void;
}) {
  const [open, setOpen] = useState(false);

  if (plan.screens.length <= 1) return null;

  return (
    <div
      style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 40,
        background: "var(--color-surface, #1C1C1C)",
        borderTop: "1px solid rgba(255,255,255,0.08)",
        backdropFilter: "blur(12px)",
        maxHeight: open ? "60vh" : "44px",
        transition: "max-height 0.25s ease",
        overflow: "hidden",
      }}
    >
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        aria-label="Lesson screen navigation"
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
          Screen {activeIndex + 1} / {plan.screens.length} - {plan.screens[activeIndex]?.title || "Lesson"}
        </span>
        <span style={{ transform: open ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s ease" }}>
          ▲
        </span>
      </button>

      {open && (
        <nav aria-label="Lesson screens" style={{ padding: "0 1rem 1rem", overflowY: "auto", maxHeight: "calc(60vh - 44px)" }}>
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {plan.screens.map((screen) => {
              const isActive = screen.index === activeIndex;
              return (
                <li key={screen.index}>
                  <button
                    type="button"
                    onClick={() => {
                      onNavigate(screen.index);
                      setOpen(false);
                    }}
                    style={{
                      display: "block",
                      width: "100%",
                      padding: "0.5rem 0.75rem",
                      background: isActive ? "rgba(212, 165, 116, 0.1)" : "transparent",
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
                    {screen.index + 1}. {screen.title}
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

function Badge({ children }: { children: ReactNode }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        padding: "0.25rem 0.55rem",
        borderRadius: "999px",
        background: "rgba(255,255,255,0.06)",
        border: "1px solid rgba(255,255,255,0.08)",
        fontSize: "0.6875rem",
        color: "var(--color-text)",
      }}
    >
      {children}
    </span>
  );
}

function ListCard({ title, items }: { title: string; items: string[] }) {
  return (
    <GlassCard blur="sm" style={{ padding: "0.9rem 1rem" }}>
      <div style={{ fontSize: "0.6875rem", fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--color-text-muted)" }}>
        {title}
      </div>
      <ul style={{ margin: "0.75rem 0 0", paddingLeft: "1.25rem" }}>
        {items.length > 0 ? (
          items.map((item, index) => (
            <li key={index} style={{ marginBottom: "0.35rem", lineHeight: 1.6, color: "var(--color-text)" }}>
              <MarkdownText text={item} />
            </li>
          ))
        ) : (
          <li style={{ color: "var(--color-text-muted)" }}>Nothing to show yet.</li>
        )}
      </ul>
    </GlassCard>
  );
}

function screenLabel(kind: string): string {
  return {
    cover: "Cover",
    objectives: "Objectives",
    overview: "Overview",
    concept: "Concept",
    definition: "Definition",
    example: "Example",
    visualization: "Visualization",
    quick_check: "Quick Check",
    practice: "Practice",
    strategy: "Strategy",
    remember: "Remember",
    takeaway: "Takeaway",
    summary: "Summary",
    completion: "Completion",
  }[kind] || kind;
}

function resolveSections(sections: LessonSection[], selectedIndices: number[]): LessonSection[] {
  if (!selectedIndices.length) {
    return [];
  }
  return selectedIndices
    .map((index) => sections[index])
    .filter((section): section is LessonSection => Boolean(section));
}
