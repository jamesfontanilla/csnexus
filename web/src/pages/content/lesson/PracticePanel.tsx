import { useState, useRef, useEffect } from "react";
import type { PracticeProblem } from "./types";
import { apiClient } from "../../../api/client";
import { MarkdownText } from "../../../components/MarkdownText";

interface PracticePanelProps {
  problems: PracticeProblem[];
  memoryAids: string[];
  examStrategies: string[];
  keyTakeaways: string[];
  subtopicId: string;
  activeSectionIndex: number;
  lessonTitle: string;
}

/**
 * Companion panel for desktop layout.
 * Shows interactive practice problems, memory aids, exam strategies, key takeaways,
 * and an inline AI study buddy chat.
 */
export function PracticePanel({
  problems,
  memoryAids,
  examStrategies,
  keyTakeaways,
  subtopicId: _subtopicId,
  activeSectionIndex: _activeSectionIndex,
  lessonTitle: _lessonTitle,
}: PracticePanelProps) {
  // These props are passed through to InlineLessonChat in DesktopLessonLayout
  void _subtopicId; void _activeSectionIndex; void _lessonTitle;
  const [activeTab, setActiveTab] = useState<"practice" | "aids" | "takeaways">(
    problems.length > 0 ? "practice" : memoryAids.length > 0 || examStrategies.length > 0 ? "aids" : "takeaways"
  );

  const tabs = [
    { id: "practice" as const, label: "Practice", count: problems.length, show: problems.length > 0 },
    { id: "aids" as const, label: "Aids & Tips", count: memoryAids.length + examStrategies.length, show: memoryAids.length > 0 || examStrategies.length > 0 },
    { id: "takeaways" as const, label: "Takeaways", count: keyTakeaways.length, show: keyTakeaways.length > 0 },
  ].filter((t) => t.show);

  if (tabs.length === 0) return null;

  return (
    <aside
      aria-label="Practice and study aids"
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Tab bar */}
      <div role="tablist" aria-label="Study panel tabs" style={{ display: "flex", gap: "0.25rem", marginBottom: "0.75rem", borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "0.5rem", flexShrink: 0, flexWrap: "wrap" }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`tabpanel-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => setActiveTab(tab.id)}
            onKeyDown={(e) => {
              const visibleTabs = tabs;
              const currentIdx = visibleTabs.findIndex((t) => t.id === tab.id);
              let nextIdx = -1;
              if (e.key === "ArrowRight") nextIdx = (currentIdx + 1) % visibleTabs.length;
              else if (e.key === "ArrowLeft") nextIdx = (currentIdx - 1 + visibleTabs.length) % visibleTabs.length;
              else if (e.key === "Home") nextIdx = 0;
              else if (e.key === "End") nextIdx = visibleTabs.length - 1;
              if (nextIdx >= 0) {
                e.preventDefault();
                setActiveTab(visibleTabs[nextIdx].id);
                document.getElementById(`tab-${visibleTabs[nextIdx].id}`)?.focus();
              }
            }}
            style={{
              padding: "0.3rem 0.6rem",
              fontSize: "0.6875rem",
              fontWeight: activeTab === tab.id ? 600 : 400,
              background: activeTab === tab.id ? "rgba(212, 165, 116, 0.12)" : "transparent",
              border: "1px solid",
              borderColor: activeTab === tab.id ? "rgba(212, 165, 116, 0.3)" : "rgba(255,255,255,0.08)",
              borderRadius: "4px",
              cursor: "pointer",
              color: activeTab === tab.id ? "var(--color-accent, #d4a574)" : "var(--color-text-muted)",
              transition: "all 0.15s ease",
            }}
          >
            {tab.label}
            {tab.count > 0 && (
              <span style={{ marginLeft: "0.25rem", opacity: 0.6 }}>({tab.count})</span>
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div role="tabpanel" id={`tabpanel-${activeTab}`} aria-labelledby={`tab-${activeTab}`}>
        {activeTab === "practice" && <PracticeProblems problems={problems} />}
        {activeTab === "aids" && <AidsAndStrategies memoryAids={memoryAids} examStrategies={examStrategies} />}
        {activeTab === "takeaways" && <TakeawaysList items={keyTakeaways} />}
      </div>
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Inline Lesson Chat — embedded in the right panel
// ---------------------------------------------------------------------------

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface LessonChatResponse {
  interaction_id: number;
  response_text: string;
  detected_intent: string;
  context_json?: Record<string, unknown> | null;
}

export function InlineLessonChat({
  subtopicId,
  activeSectionIndex,
  lessonTitle,
}: {
  subtopicId: string;
  activeSectionIndex: number;
  lessonTitle: string;
}) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastInteractionId, setLastInteractionId] = useState<number | null>(null);
  const [contextJson, setContextJson] = useState<Record<string, unknown> | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    setTimeout(() => inputRef.current?.focus(), 100);
  }, []);

  useEffect(() => {
    setMessages([]);
    setInput("");
    setLoading(false);
    setLastInteractionId(null);
    setContextJson(null);
  }, [subtopicId, activeSectionIndex]);

  async function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = { role: "user", content: trimmed };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const history = updatedMessages.slice(-10).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const data = await apiClient.post<LessonChatResponse>("/v1/tutor/lesson-chat", {
        subtopic_id: Number(subtopicId),
        message: trimmed,
        active_section_index: activeSectionIndex,
        context_json: contextJson,
        history: history.slice(0, -1),
      });

      setMessages((prev) => [...prev, { role: "assistant", content: data.response_text }]);
      setLastInteractionId(data.interaction_id);
      setContextJson(data.context_json ?? contextJson);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that. Try again!" }]);
    } finally {
      setLoading(false);
    }
  }

  async function handleSendWithMessage(msg: string) {
    if (!msg.trim() || loading) return;

    const userMessage: ChatMessage = { role: "user", content: msg };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const history = updatedMessages.slice(-10).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const data = await apiClient.post<LessonChatResponse>("/v1/tutor/lesson-chat", {
        subtopic_id: Number(subtopicId),
        message: msg,
        active_section_index: activeSectionIndex,
        context_json: contextJson,
        history: history.slice(0, -1),
      });

      setMessages((prev) => [...prev, { role: "assistant", content: data.response_text }]);
      setLastInteractionId(data.interaction_id);
      setContextJson(data.context_json ?? contextJson);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Sorry, I couldn't process that. Try again!" }]);
    } finally {
      setLoading(false);
    }
  }

  async function handleRate(helpful: boolean) {
    if (!lastInteractionId) return;
    try {
      await apiClient.post(`/v1/tutor/interactions/${lastInteractionId}:rate`, { helpful });
    } catch {
      // Silent fail
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }} role="region" aria-label="Study buddy chat">
      {/* Messages area */}
      <div
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        style={{
          flex: 1,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "0.4rem",
          paddingBottom: "0.5rem",
          minHeight: 0,
        }}
      >
        {/* Welcome state */}
        {messages.length === 0 && (
          <div style={{ textAlign: "center", padding: "0.5rem 0" }}>
            <div aria-hidden="true" style={{ fontSize: "1.25rem", marginBottom: "0.375rem" }}>📚</div>
            <p style={{ fontSize: "0.6875rem", color: "var(--color-text)", marginBottom: "0.25rem", fontWeight: 500 }}>
              Study Buddy
            </p>
            <p style={{ fontSize: "0.625rem", color: "var(--color-text-muted)", lineHeight: 1.4, marginBottom: "0.625rem" }}>
              Ask about {lessonTitle || "this lesson"}
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.25rem", justifyContent: "center" }} role="group" aria-label="Quick actions">
              {[
                { label: "📝 Summarize", msg: "Summarize this section", ariaLabel: "Summarize this section" },
                { label: "🎯 Quiz me", msg: "Quiz me", ariaLabel: "Quiz me on this section" },
                { label: "💡 Example", msg: "Give me an example", ariaLabel: "Give me an example" },
                { label: "🧠 Remember", msg: "Help me remember this", ariaLabel: "Help me remember this" },
                { label: "📋 Exam tips", msg: "How is this tested?", ariaLabel: "How is this tested in the exam" },
              ].map((chip) => (
                <button
                  key={chip.label}
                  onClick={() => handleSendWithMessage(chip.msg)}
                  aria-label={chip.ariaLabel}
                  style={{
                    padding: "0.2rem 0.4rem",
                    fontSize: "0.5625rem",
                    borderRadius: "999px",
                    border: "1px solid rgba(212, 165, 116, 0.25)",
                    background: "rgba(212, 165, 116, 0.08)",
                    color: "var(--color-accent, #d4a574)",
                    cursor: "pointer",
                    transition: "background 0.15s",
                    whiteSpace: "nowrap",
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = "rgba(212, 165, 116, 0.15)"; }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = "rgba(212, 165, 116, 0.08)"; }}
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message bubbles */}
        {messages.map((msg, i) => (
          <div
            key={i}
            aria-label={msg.role === "user" ? "You said" : "Study buddy said"}
            style={{
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              maxWidth: "90%",
              padding: "0.375rem 0.5rem",
              borderRadius: msg.role === "user" ? "8px 8px 2px 8px" : "8px 8px 8px 2px",
              background: msg.role === "user"
                ? "rgba(212, 165, 116, 0.15)"
                : "rgba(255, 255, 255, 0.05)",
              border: `1px solid ${msg.role === "user" ? "rgba(212, 165, 116, 0.25)" : "rgba(255, 255, 255, 0.08)"}`,
            }}
          >
            <MarkdownText
              text={msg.content}
              style={{ fontSize: "0.6875rem", lineHeight: 1.5, color: "var(--color-text)" }}
            />
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div
            aria-label="Study buddy is typing"
            role="status"
            style={{
              alignSelf: "flex-start",
              padding: "0.375rem 0.5rem",
              borderRadius: "8px 8px 8px 2px",
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              fontSize: "0.6875rem",
              color: "var(--color-text-muted)",
            }}
          >
            <TypingDots />
            <span className="sr-only">Study buddy is thinking...</span>
          </div>
        )}

        {/* Rating */}
        {lastInteractionId && messages.length > 0 && messages[messages.length - 1].role === "assistant" && !loading && (
          <div style={{ display: "flex", gap: "0.25rem", alignSelf: "flex-start" }} role="group" aria-label="Rate this response">
            <button onClick={() => handleRate(true)} aria-label="Mark response as helpful" style={{ background: "none", border: "none", cursor: "pointer", fontSize: "0.625rem", opacity: 0.5, padding: "0.1rem" }} onMouseEnter={(e) => { e.currentTarget.style.opacity = "1"; }} onMouseLeave={(e) => { e.currentTarget.style.opacity = "0.5"; }}>👍</button>
            <button onClick={() => handleRate(false)} aria-label="Mark response as not helpful" style={{ background: "none", border: "none", cursor: "pointer", fontSize: "0.625rem", opacity: 0.5, padding: "0.1rem" }} onMouseEnter={(e) => { e.currentTarget.style.opacity = "1"; }} onMouseLeave={(e) => { e.currentTarget.style.opacity = "0.5"; }}>👎</button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{
          display: "flex",
          gap: "0.375rem",
          alignItems: "center",
          paddingTop: "0.5rem",
          borderTop: "1px solid rgba(255, 255, 255, 0.08)",
          flexShrink: 0,
        }}
        aria-label="Send a message to study buddy"
      >
        <label htmlFor="chat-input" className="sr-only">Type your question about this lesson</label>
        <input
          id="chat-input"
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask anything..."
          disabled={loading}
          autoComplete="off"
          style={{
            flex: 1,
            padding: "0.375rem 0.5rem",
            borderRadius: "6px",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            background: "rgba(255, 255, 255, 0.04)",
            color: "var(--color-text)",
            fontSize: "0.6875rem",
            outline: "none",
            transition: "border-color 0.15s",
            minWidth: 0,
          }}
          onFocus={(e) => { e.currentTarget.style.borderColor = "rgba(212, 165, 116, 0.4)"; }}
          onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)"; }}
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          aria-label="Send message"
          style={{
            width: "1.5rem",
            height: "1.5rem",
            borderRadius: "6px",
            border: "none",
            background: input.trim() && !loading ? "rgba(212, 165, 116, 0.8)" : "rgba(255, 255, 255, 0.08)",
            cursor: input.trim() && !loading ? "pointer" : "default",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "0.6875rem",
            color: "var(--color-text)",
            flexShrink: 0,
          }}
        >
          <span aria-hidden="true">↑</span>
        </button>
      </form>
    </div>
  );
}

function TypingDots() {
  return (
    <span style={{ display: "inline-flex", gap: "0.15rem", alignItems: "center" }}>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          style={{
            width: "0.3rem",
            height: "0.3rem",
            borderRadius: "50%",
            background: "var(--color-text-muted)",
            animation: `typingDot 1.2s infinite ${i * 0.2}s`,
            opacity: 0.4,
          }}
        />
      ))}
      <style>{`
        @keyframes typingDot {
          0%, 60%, 100% { opacity: 0.4; transform: translateY(0); }
          30% { opacity: 1; transform: translateY(-2px); }
        }
      `}</style>
    </span>
  );
}

// ---------------------------------------------------------------------------
// Practice Problems — interactive quiz cards
// ---------------------------------------------------------------------------

function PracticeProblems({ problems }: { problems: PracticeProblem[] }) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [score, setScore] = useState({ correct: 0, attempted: 0 });

  if (problems.length === 0) return null;

  const problem = problems[currentIdx];

  function handleReveal() {
    setRevealed(true);
    setScore((s) => ({ ...s, attempted: s.attempted + 1 }));
  }

  function handleNext(wasCorrect: boolean) {
    if (wasCorrect) setScore((s) => ({ ...s, correct: s.correct + 1 }));
    setRevealed(false);
    setCurrentIdx((i) => (i + 1) % problems.length);
  }

  const difficultyColors: Record<string, string> = {
    easy: "rgba(80, 200, 120, 0.2)",
    medium: "rgba(212, 165, 116, 0.2)",
    hard: "rgba(220, 80, 80, 0.2)",
  };

  return (
    <div>
      {/* Score header */}
      {score.attempted > 0 && (
        <div style={{ fontSize: "0.6875rem", color: "var(--color-text-muted)", marginBottom: "0.5rem", textAlign: "center" }}>
          {score.correct}/{score.attempted} correct
        </div>
      )}

      {/* Problem card */}
      <div
        style={{
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          overflow: "hidden",
          marginBottom: "0.5rem",
        }}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0.5rem 0.75rem", background: "rgba(255,255,255,0.03)", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <span style={{ fontSize: "0.625rem", fontWeight: 600, color: "var(--color-text-muted)" }}>
            #{problem.number} of {problems.length}
          </span>
          <span
            style={{
              fontSize: "0.5625rem",
              fontWeight: 700,
              padding: "0.1rem 0.4rem",
              borderRadius: "3px",
              background: difficultyColors[problem.difficulty] || "rgba(255,255,255,0.1)",
              textTransform: "uppercase",
              letterSpacing: "0.03em",
              color: "var(--color-text)",
            }}
          >
            {problem.difficulty}
          </span>
        </div>

        {/* Question */}
        <div style={{ padding: "0.75rem", fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }}>
          {problem.question}
        </div>

        {/* Answer area */}
        {!revealed ? (
          <button
            onClick={handleReveal}
            style={{
              width: "100%",
              padding: "0.5rem",
              background: "rgba(212, 165, 116, 0.06)",
              border: "none",
              borderTop: "1px solid rgba(255,255,255,0.06)",
              cursor: "pointer",
              fontSize: "0.75rem",
              fontWeight: 600,
              color: "var(--color-accent, #d4a574)",
            }}
          >
            Show Answer
          </button>
        ) : (
          <div style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}>
            <div style={{ padding: "0.5rem 0.75rem", background: "rgba(80, 200, 120, 0.04)" }}>
              <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "rgba(80, 200, 120, 0.8)", marginBottom: "0.25rem" }}>
                Answer
              </div>
              <div style={{ fontSize: "0.8125rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {problem.answer}
              </div>
              {problem.explanation && (
                <div style={{ marginTop: "0.375rem", fontSize: "0.75rem", color: "var(--color-text-secondary)", lineHeight: 1.5 }}>
                  {problem.explanation}
                </div>
              )}
            </div>
            {/* Self-assessment buttons */}
            <div style={{ display: "flex", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
              <button
                onClick={() => handleNext(false)}
                style={{
                  flex: 1,
                  padding: "0.4rem",
                  background: "rgba(220, 80, 80, 0.06)",
                  border: "none",
                  borderRight: "1px solid rgba(255,255,255,0.06)",
                  cursor: "pointer",
                  fontSize: "0.6875rem",
                  fontWeight: 600,
                  color: "rgba(220, 80, 80, 0.8)",
                }}
              >
                ✗ Got it wrong
              </button>
              <button
                onClick={() => handleNext(true)}
                style={{
                  flex: 1,
                  padding: "0.4rem",
                  background: "rgba(80, 200, 120, 0.06)",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "0.6875rem",
                  fontWeight: 600,
                  color: "rgba(80, 200, 120, 0.8)",
                }}
              >
                ✓ Got it right
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Problem navigation dots */}
      <div style={{ display: "flex", justifyContent: "center", gap: "0.25rem", flexWrap: "wrap" }}>
        {problems.map((_, i) => (
          <button
            key={i}
            onClick={() => { setCurrentIdx(i); setRevealed(false); }}
            aria-label={`Go to problem ${i + 1}`}
            style={{
              width: "0.5rem",
              height: "0.5rem",
              borderRadius: "50%",
              border: "none",
              cursor: "pointer",
              background: i === currentIdx
                ? "var(--color-accent, #d4a574)"
                : "rgba(255,255,255,0.15)",
              transition: "background 0.15s",
            }}
          />
        ))}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Memory Aids & Exam Strategies
// ---------------------------------------------------------------------------

function AidsAndStrategies({ memoryAids, examStrategies }: { memoryAids: string[]; examStrategies: string[] }) {
  return (
    <div>
      {memoryAids.length > 0 && (
        <div style={{ marginBottom: "1rem" }}>
          <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.375rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            🧠 Memory Aids
          </div>
          <ul style={{ margin: 0, paddingLeft: "1rem" }}>
            {memoryAids.map((aid, i) => (
              <li key={i} style={{ marginBottom: "0.375rem", fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {aid}
              </li>
            ))}
          </ul>
        </div>
      )}

      {examStrategies.length > 0 && (
        <div>
          <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.375rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
            🎯 Exam Strategies
          </div>
          <ul style={{ margin: 0, paddingLeft: "1rem" }}>
            {examStrategies.map((strategy, i) => (
              <li key={i} style={{ marginBottom: "0.375rem", fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
                {strategy}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Key Takeaways
// ---------------------------------------------------------------------------

function TakeawaysList({ items }: { items: string[] }) {
  return (
    <div>
      <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.5rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
        🔑 Key Takeaways
      </div>
      <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
        {items.map((item, i) => (
          <li
            key={i}
            style={{
              display: "flex",
              gap: "0.5rem",
              alignItems: "flex-start",
              marginBottom: "0.5rem",
              padding: "0.4rem 0.5rem",
              background: "rgba(212, 165, 116, 0.04)",
              borderRadius: "4px",
              border: "1px solid rgba(212, 165, 116, 0.1)",
            }}
          >
            <span style={{ flexShrink: 0, fontSize: "0.625rem", fontWeight: 700, color: "var(--color-accent, #d4a574)", marginTop: "0.125rem" }}>
              {i + 1}
            </span>
            <span style={{ fontSize: "0.75rem", lineHeight: 1.5, color: "var(--color-text)" }}>
              {item}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
