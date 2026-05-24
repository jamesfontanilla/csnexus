import { useState, useRef, useEffect } from "react";
import { apiClient } from "../../../api/client";
import { MarkdownText } from "../../../components/MarkdownText";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface LessonChatResponse {
  interaction_id: number;
  response_text: string;
  detected_intent: string;
}

interface LessonChatPanelProps {
  subtopicId: string;
  activeSectionIndex: number;
  lessonTitle: string;
}

/**
 * Floating chat panel that provides a pseudo-AI study buddy experience
 * within the lesson reader. Uses the lesson's own content to generate
 * contextual, rule-based responses.
 */
export function LessonChatPanel({ subtopicId, activeSectionIndex, lessonTitle }: LessonChatPanelProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastInteractionId, setLastInteractionId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input when panel opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  async function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage: ChatMessage = { role: "user", content: trimmed };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      // Send last 10 messages as history (keeping payload small)
      const history = updatedMessages.slice(-10).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const data = await apiClient.post<LessonChatResponse>("/v1/tutor/lesson-chat", {
        subtopic_id: Number(subtopicId),
        message: trimmed,
        active_section_index: activeSectionIndex,
        history: history.slice(0, -1), // Exclude the current message from history
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: data.response_text,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setLastInteractionId(data.interaction_id);
    } catch {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "Sorry, I couldn't process that. Try again in a moment!",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  async function handleRate(helpful: boolean) {
    if (!lastInteractionId) return;
    try {
      await apiClient.post(`/v1/tutor/interactions/${lastInteractionId}:rate`, { helpful });
    } catch {
      // Silent fail for rating
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  // Helper to send a message directly (for quick action chips)
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
        history: history.slice(0, -1),
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: data.response_text,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setLastInteractionId(data.interaction_id);
    } catch {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "Sorry, I couldn't process that. Try again in a moment!",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  }

  // Floating button when closed
  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        aria-label="Open study buddy chat"
        title="Ask your study buddy"
        style={{
          position: "fixed",
          bottom: "1.5rem",
          right: "1.5rem",
          width: "3.25rem",
          height: "3.25rem",
          borderRadius: "50%",
          background: "linear-gradient(135deg, rgba(212, 165, 116, 0.9), rgba(180, 130, 80, 0.9))",
          border: "1px solid rgba(255, 255, 255, 0.2)",
          boxShadow: "0 4px 20px rgba(212, 165, 116, 0.3), 0 2px 8px rgba(0,0,0,0.3)",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "1.5rem",
          zIndex: 1000,
          transition: "transform 0.2s ease, box-shadow 0.2s ease",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "scale(1.1)";
          e.currentTarget.style.boxShadow = "0 6px 24px rgba(212, 165, 116, 0.4), 0 3px 12px rgba(0,0,0,0.4)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.boxShadow = "0 4px 20px rgba(212, 165, 116, 0.3), 0 2px 8px rgba(0,0,0,0.3)";
        }}
      >
        💬
      </button>
    );
  }

  // Chat panel when open
  return (
    <div
      role="dialog"
      aria-label="Study buddy chat"
      aria-modal="true"
      onKeyDown={(e) => { if (e.key === "Escape") setIsOpen(false); }}
      style={{
        position: "fixed",
        bottom: "1.5rem",
        right: "1.5rem",
        width: "380px",
        maxWidth: "calc(100vw - 2rem)",
        height: "520px",
        maxHeight: "calc(100vh - 6rem)",
        borderRadius: "12px",
        border: "1px solid rgba(255, 255, 255, 0.12)",
        background: "rgba(26, 26, 30, 0.97)",
        backdropFilter: "blur(20px)",
        boxShadow: "0 8px 40px rgba(0,0,0,0.5), 0 2px 12px rgba(0,0,0,0.3)",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        zIndex: 1000,
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "0.75rem 1rem",
          borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "rgba(212, 165, 116, 0.05)",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <span style={{ fontSize: "1.125rem" }}>🤖</span>
          <div>
            <div style={{ fontSize: "0.8125rem", fontWeight: 600, color: "var(--color-text)" }}>
              Study Buddy
            </div>
            <div style={{ fontSize: "0.625rem", color: "var(--color-text-muted)" }}>
              {lessonTitle || "Lesson Assistant"}
            </div>
          </div>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          aria-label="Close chat"
          style={{
            background: "none",
            border: "none",
            cursor: "pointer",
            fontSize: "1.25rem",
            color: "var(--color-text-muted)",
            padding: "0.25rem",
            lineHeight: 1,
          }}
        >
          ✕
        </button>
      </div>

      {/* Messages area */}
      <div
        role="log"
        aria-live="polite"
        aria-label="Chat messages"
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "0.75rem",
          display: "flex",
          flexDirection: "column",
          gap: "0.5rem",
        }}
      >
        {/* Welcome message if no messages yet */}
        {messages.length === 0 && (
          <div style={{ padding: "1rem 0.5rem", textAlign: "center" }}>
            <div aria-hidden="true" style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>📚</div>
            <p style={{ fontSize: "0.8125rem", color: "var(--color-text)", marginBottom: "0.5rem", fontWeight: 500 }}>
              Hi! I'm your study buddy.
            </p>
            <p style={{ fontSize: "0.75rem", color: "var(--color-text-muted)", lineHeight: 1.5, marginBottom: "1rem" }}>
              Ask me anything about this lesson — I can explain concepts, give examples, quiz you, or share exam tips.
            </p>
            {/* Quick action chips */}
            <div style={{ display: "flex", flexWrap: "wrap", gap: "0.375rem", justifyContent: "center" }} role="group" aria-label="Quick actions">
              {[
                { label: "📝 Summarize", msg: "Summarize this section", ariaLabel: "Summarize this section" },
                { label: "🎯 Quiz me", msg: "Quiz me", ariaLabel: "Quiz me on this section" },
                { label: "💡 Example", msg: "Give me an example", ariaLabel: "Give me an example" },
                { label: "🧠 Memory tips", msg: "Help me remember this", ariaLabel: "Help me remember this" },
                { label: "📋 Exam tips", msg: "How is this tested in the CSE?", ariaLabel: "How is this tested in the exam" },
              ].map((chip) => (
                <button
                  key={chip.label}
                  onClick={() => handleSendWithMessage(chip.msg)}
                  aria-label={chip.ariaLabel}
                  style={{
                    padding: "0.3rem 0.6rem",
                    fontSize: "0.6875rem",
                    borderRadius: "999px",
                    border: "1px solid rgba(212, 165, 116, 0.25)",
                    background: "rgba(212, 165, 116, 0.08)",
                    color: "var(--color-accent, #d4a574)",
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                    whiteSpace: "nowrap",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "rgba(212, 165, 116, 0.15)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "rgba(212, 165, 116, 0.08)";
                  }}
                >
                  {chip.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message bubbles */}
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {/* Typing indicator */}
        {loading && (
          <div
            role="status"
            aria-label="Study buddy is typing"
            style={{
              alignSelf: "flex-start",
              padding: "0.5rem 0.75rem",
              borderRadius: "12px 12px 12px 4px",
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              fontSize: "0.8125rem",
              color: "var(--color-text-muted)",
            }}
          >
            <TypingDots />
            <span className="sr-only">Study buddy is thinking...</span>
          </div>
        )}

        {/* Rating buttons for last response */}
        {lastInteractionId && messages.length > 0 && messages[messages.length - 1].role === "assistant" && !loading && (
          <div style={{ display: "flex", gap: "0.375rem", alignSelf: "flex-start", marginTop: "-0.25rem" }} role="group" aria-label="Rate this response">
            <button
              onClick={() => handleRate(true)}
              aria-label="Mark response as helpful"
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                fontSize: "0.75rem",
                opacity: 0.5,
                transition: "opacity 0.15s",
                padding: "0.125rem",
              }}
              onMouseEnter={(e) => { e.currentTarget.style.opacity = "1"; }}
              onMouseLeave={(e) => { e.currentTarget.style.opacity = "0.5"; }}
            >
              👍
            </button>
            <button
              onClick={() => handleRate(false)}
              aria-label="Mark response as not helpful"
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                fontSize: "0.75rem",
                opacity: 0.5,
                transition: "opacity 0.15s",
                padding: "0.125rem",
              }}
              onMouseEnter={(e) => { e.currentTarget.style.opacity = "1"; }}
              onMouseLeave={(e) => { e.currentTarget.style.opacity = "0.5"; }}
            >
              👎
            </button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{
          padding: "0.625rem 0.75rem",
          borderTop: "1px solid rgba(255, 255, 255, 0.08)",
          display: "flex",
          gap: "0.5rem",
          alignItems: "center",
          flexShrink: 0,
        }}
        aria-label="Send a message to study buddy"
      >
        <label htmlFor="floating-chat-input" className="sr-only">Type your question about this lesson</label>
        <input
          id="floating-chat-input"
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about this lesson..."
          disabled={loading}
          autoComplete="off"
          style={{
            flex: 1,
            padding: "0.5rem 0.75rem",
            borderRadius: "8px",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            background: "rgba(255, 255, 255, 0.04)",
            color: "var(--color-text)",
            fontSize: "0.8125rem",
            outline: "none",
            transition: "border-color 0.15s",
          }}
          onFocus={(e) => { e.currentTarget.style.borderColor = "rgba(212, 165, 116, 0.4)"; }}
          onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)"; }}
        />
        <button
          type="submit"
          disabled={!input.trim() || loading}
          aria-label="Send message"
          style={{
            width: "2rem",
            height: "2rem",
            borderRadius: "8px",
            border: "none",
            background: input.trim() && !loading
              ? "rgba(212, 165, 116, 0.8)"
              : "rgba(255, 255, 255, 0.08)",
            cursor: input.trim() && !loading ? "pointer" : "default",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "0.875rem",
            transition: "background 0.15s",
            flexShrink: 0,
          }}
        >
          <span aria-hidden="true">↑</span>
        </button>
      </form>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div
      style={{
        alignSelf: isUser ? "flex-end" : "flex-start",
        maxWidth: "85%",
        padding: "0.5rem 0.75rem",
        borderRadius: isUser ? "12px 12px 4px 12px" : "12px 12px 12px 4px",
        background: isUser
          ? "rgba(212, 165, 116, 0.15)"
          : "rgba(255, 255, 255, 0.05)",
        border: `1px solid ${isUser ? "rgba(212, 165, 116, 0.25)" : "rgba(255, 255, 255, 0.08)"}`,
      }}
    >
      <MarkdownText
        text={message.content}
        style={{
          fontSize: "0.8125rem",
          lineHeight: 1.55,
          color: "var(--color-text)",
        }}
      />
    </div>
  );
}

function TypingDots() {
  return (
    <span style={{ display: "inline-flex", gap: "0.2rem", alignItems: "center" }}>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          style={{
            width: "0.375rem",
            height: "0.375rem",
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
