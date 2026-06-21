import { useEffect, useMemo, useRef, useState } from "react";
import { PageTransition } from "../components/PageTransition";
import { GlassCard } from "../components/GlassCard";
import { GlassButton } from "../components/GlassButton";
import { MarkdownText } from "../components/MarkdownText";
import { apiClient } from "../api/client";

type ChatRole = "user" | "assistant";

interface TutorModule {
  id: number;
  title: string;
  category: string;
}

interface TutorTopic {
  id: number;
  title: string;
}

interface TutorSubtopic {
  id: number;
  title: string;
}

interface ChatMessage {
  role: ChatRole;
  content: string;
  isError?: boolean;
}

interface TutorResponseData {
  interaction_id: number;
  response_text: string;
  detected_intent: string;
  context_json?: Record<string, unknown> | null;
}

interface ModulesResponse {
  items: TutorModule[];
  total: number;
}

interface SelectOption {
  value: string;
  label: string;
}

const quickPrompts = [
  "Summarize this lesson",
  "Explain it simpler",
  "Give me an example",
  "Quiz me on this topic",
  "What should I remember?",
];

export function Tutor() {
  const [modules, setModules] = useState<TutorModule[]>([]);
  const [topics, setTopics] = useState<TutorTopic[]>([]);
  const [subtopics, setSubtopics] = useState<TutorSubtopic[]>([]);

  const [selectedModuleId, setSelectedModuleId] = useState("");
  const [selectedTopicId, setSelectedTopicId] = useState("");
  const [selectedSubtopicId, setSelectedSubtopicId] = useState("");

  const [modulesLoading, setModulesLoading] = useState(true);
  const [topicsLoading, setTopicsLoading] = useState(false);
  const [subtopicsLoading, setSubtopicsLoading] = useState(false);

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [lastInteractionId, setLastInteractionId] = useState<number | null>(null);
  const [contextJson, setContextJson] = useState<Record<string, unknown> | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const selectedModule = useMemo(
    () => modules.find((module) => String(module.id) === selectedModuleId) ?? null,
    [modules, selectedModuleId],
  );
  const selectedTopic = useMemo(
    () => topics.find((topic) => String(topic.id) === selectedTopicId) ?? null,
    [topics, selectedTopicId],
  );
  const selectedSubtopic = useMemo(
    () => subtopics.find((subtopic) => String(subtopic.id) === selectedSubtopicId) ?? null,
    [subtopics, selectedSubtopicId],
  );
  const selectedContextLabel = [
    selectedModule?.title ?? "Module",
    selectedTopic?.title ?? "Topic",
    selectedSubtopic?.title ?? "Subtopic",
  ].join(" / ");

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  useEffect(() => {
    let cancelled = false;
    setModulesLoading(true);

    apiClient
      .get<ModulesResponse>("/v1/modules")
      .then((response) => {
        if (cancelled) return;
        const loadedModules = response.items ?? [];
        setModules(loadedModules);
        if (loadedModules.length > 0) {
          setSelectedModuleId((current) => current || String(loadedModules[0].id));
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setErrorMessage(error instanceof Error ? error.message : "Failed to load tutor context.");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setModulesLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedModuleId) {
      setTopics([]);
      setSelectedTopicId("");
      setSubtopics([]);
      setSelectedSubtopicId("");
      return;
    }

    let cancelled = false;
    setTopicsLoading(true);
    setErrorMessage(null);

    apiClient
      .get<TutorTopic[]>(`/v1/modules/${selectedModuleId}/topics`)
      .then((response) => {
        if (cancelled) return;
        const loadedTopics = response ?? [];
        setTopics(loadedTopics);
        if (loadedTopics.length > 0) {
          const currentTopicExists = loadedTopics.some((topic) => String(topic.id) === selectedTopicId);
          setSelectedTopicId((current) => (current && currentTopicExists ? current : String(loadedTopics[0].id)));
        } else {
          setSelectedTopicId("");
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setTopics([]);
          setSelectedTopicId("");
          setErrorMessage(error instanceof Error ? error.message : "Failed to load topics.");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setTopicsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedModuleId]);

  useEffect(() => {
    if (!selectedTopicId) {
      setSubtopics([]);
      setSelectedSubtopicId("");
      return;
    }

    let cancelled = false;
    setSubtopicsLoading(true);
    setErrorMessage(null);

    apiClient
      .get<TutorSubtopic[]>(`/v1/topics/${selectedTopicId}/subtopics`)
      .then((response) => {
        if (cancelled) return;
        const loadedSubtopics = response ?? [];
        setSubtopics(loadedSubtopics);
        if (loadedSubtopics.length > 0) {
          const currentSubtopicExists = loadedSubtopics.some((subtopic) => String(subtopic.id) === selectedSubtopicId);
          setSelectedSubtopicId((current) => (current && currentSubtopicExists ? current : String(loadedSubtopics[0].id)));
        } else {
          setSelectedSubtopicId("");
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setSubtopics([]);
          setSelectedSubtopicId("");
          setErrorMessage(error instanceof Error ? error.message : "Failed to load subtopics.");
        }
      })
      .finally(() => {
        if (!cancelled) {
          setSubtopicsLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [selectedTopicId]);

  useEffect(() => {
    setMessages([]);
    setInput("");
    setContextJson(null);
    setLastInteractionId(null);
    setErrorMessage(null);
  }, [selectedSubtopicId]);

  useEffect(() => {
    if (selectedSubtopicId) {
      setTimeout(() => inputRef.current?.focus(), 120);
    }
  }, [selectedSubtopicId]);

  const moduleOptions = useMemo<SelectOption[]>(
    () => modules.map((module) => ({ value: String(module.id), label: module.title })),
    [modules],
  );
  const topicOptions = useMemo<SelectOption[]>(
    () => topics.map((topic) => ({ value: String(topic.id), label: topic.title })),
    [topics],
  );
  const subtopicOptions = useMemo<SelectOption[]>(
    () => subtopics.map((subtopic) => ({ value: String(subtopic.id), label: subtopic.title })),
    [subtopics],
  );

  async function sendMessage(rawMessage: string) {
    const trimmed = rawMessage.trim();
    if (!trimmed || sending || !selectedSubtopicId) {
      if (!selectedSubtopicId) {
        setErrorMessage("Select a subtopic first.");
      }
      return;
    }

    const userMessage: ChatMessage = { role: "user", content: trimmed };
    const nextMessages = [...messages, userMessage];
    const history = messages.slice(-10).map((message) => ({
      role: message.role,
      content: message.content,
    }));

    setMessages(nextMessages);
    setInput("");
    setSending(true);
    setErrorMessage(null);

    try {
      const data = await apiClient.post<TutorResponseData>("/v1/tutor/lesson-chat", {
        subtopic_id: Number(selectedSubtopicId),
        message: trimmed,
        context_json: contextJson,
        history,
      });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response_text },
      ]);
      setLastInteractionId(data.interaction_id);
      setContextJson(data.context_json ?? contextJson);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: error instanceof Error ? error.message : "Sorry, I could not answer that right now.",
          isError: true,
        },
      ]);
      setLastInteractionId(null);
      setErrorMessage("Could not reach the tutor.");
    } finally {
      setSending(false);
    }
  }

  const canSend = Boolean(selectedSubtopicId) && !sending;
  const transcriptEmpty = messages.length === 0;

  return (
    <PageTransition>
      <main className="page container" style={{ maxWidth: 1180 }}>
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "1rem", marginBottom: "1rem" }}>
          <div>
            <h1 style={{ margin: 0, fontSize: "var(--font-size-2xl)", fontWeight: 700, color: "var(--color-text)" }}>
              AI Tutor
            </h1>
          </div>
          <GlassButton
            variant="ghost"
            size="sm"
            onClick={() => {
              setMessages([]);
              setInput("");
              setContextJson(null);
              setLastInteractionId(null);
              setErrorMessage(null);
            }}
            disabled={!selectedSubtopicId}
          >
            New chat
          </GlassButton>
        </div>

        <div
          style={{
            display: "grid",
            gap: "1rem",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            alignItems: "start",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            <GlassCard>
              <div style={{ display: "grid", gap: "0.75rem" }}>
                <TutorSelect
                  label="Module"
                  value={selectedModuleId}
                  onChange={(value) => {
                    setSelectedModuleId(value);
                    setSelectedTopicId("");
                    setSelectedSubtopicId("");
                  }}
                  options={[
                    { value: "", label: modulesLoading ? "Loading modules..." : "Choose module" },
                    ...moduleOptions,
                  ]}
                  disabled={modulesLoading || moduleOptions.length === 0}
                />

                <TutorSelect
                  label="Topic"
                  value={selectedTopicId}
                  onChange={(value) => {
                    setSelectedTopicId(value);
                    setSelectedSubtopicId("");
                  }}
                  options={[
                    { value: "", label: topicsLoading ? "Loading topics..." : "Choose topic" },
                    ...topicOptions,
                  ]}
                  disabled={!selectedModuleId || topicsLoading || topicOptions.length === 0}
                />

                <TutorSelect
                  label="Subtopic"
                  value={selectedSubtopicId}
                  onChange={(value) => setSelectedSubtopicId(value)}
                  options={[
                    { value: "", label: subtopicsLoading ? "Loading subtopics..." : "Choose subtopic" },
                    ...subtopicOptions,
                  ]}
                  disabled={!selectedTopicId || subtopicsLoading || subtopicOptions.length === 0}
                />
              </div>
            </GlassCard>

            <GlassCard>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                  {quickPrompts.map((prompt) => (
                    <GlassButton
                      key={prompt}
                      variant="secondary"
                      size="sm"
                      disabled={!selectedSubtopicId || sending}
                      onClick={() => sendMessage(prompt)}
                    >
                      {prompt}
                    </GlassButton>
                  ))}
                </div>
                {errorMessage && (
                  <p style={{ margin: 0, color: "var(--color-danger, #d4645c)", fontSize: "var(--font-size-sm)" }}>
                    {errorMessage}
                  </p>
                )}
              </div>
            </GlassCard>

            <GlassCard>
              <div style={{ display: "grid", gap: "0.5rem", color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>
                <div style={{ color: "var(--color-text)", fontWeight: 600 }}>Current context</div>
                <div>{selectedModule?.title ?? "Module"}</div>
                <div>{selectedTopic?.title ?? "Topic"}</div>
                <div>{selectedSubtopic?.title ?? "Subtopic"}</div>
              </div>
            </GlassCard>
          </div>

          <GlassCard
            style={{
              minHeight: 680,
              display: "flex",
              flexDirection: "column",
              gap: "1rem",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "0.25rem" }}>
              <div style={{ color: "var(--color-text)", fontWeight: 600, fontSize: "var(--font-size-lg)" }}>
                Chat
              </div>
              <div style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>
              {selectedSubtopic ? selectedContextLabel : "Select a subtopic to begin."}
              </div>
            </div>

            <div
              role="log"
              aria-live="polite"
              aria-label="Tutor messages"
              style={{
                flex: 1,
                minHeight: 0,
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                gap: "0.75rem",
                paddingRight: "0.25rem",
              }}
            >
              {transcriptEmpty && (
                <div style={{ display: "grid", gap: "0.75rem", alignContent: "start", paddingTop: "0.25rem" }}>
                  <div style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>
                    Ask about the selected subtopic.
                  </div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                    {quickPrompts.map((prompt) => (
                      <GlassButton
                        key={prompt}
                        variant="ghost"
                        size="sm"
                        disabled={!selectedSubtopicId || sending}
                        onClick={() => sendMessage(prompt)}
                      >
                        {prompt}
                      </GlassButton>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message, index) => (
                <ChatBubble key={`${message.role}-${index}`} message={message} />
              ))}

              {sending && (
                <div
                  style={{
                    alignSelf: "flex-start",
                    padding: "0.75rem 1rem",
                    borderRadius: "1rem 1rem 1rem 0.25rem",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-light)",
                    color: "var(--color-text-secondary)",
                    fontSize: "var(--font-size-sm)",
                  }}
                >
                  Thinking...
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <div style={{ display: "grid", gap: "0.75rem" }}>
              {lastInteractionId && !sending && messages[messages.length - 1]?.role === "assistant" && !messages[messages.length - 1]?.isError && (
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", flexWrap: "wrap" }}>
                  <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>Was this helpful?</span>
                  <GlassButton variant="ghost" size="sm" onClick={() => apiClient.post(`/v1/tutor/interactions/${lastInteractionId}:rate`, { helpful: true }).catch(() => undefined)}>
                    👍
                  </GlassButton>
                  <GlassButton variant="ghost" size="sm" onClick={() => apiClient.post(`/v1/tutor/interactions/${lastInteractionId}:rate`, { helpful: false }).catch(() => undefined)}>
                    👎
                  </GlassButton>
                </div>
              )}

              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  void sendMessage(input);
                }}
                style={{ display: "grid", gap: "0.75rem" }}
              >
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(event) => setInput(event.target.value)}
                  disabled={!selectedSubtopicId || sending}
                  placeholder={selectedSubtopicId ? "Ask anything about this subtopic..." : "Choose a subtopic first"}
                  rows={4}
                  style={{
                    width: "100%",
                    resize: "vertical",
                    minHeight: 104,
                    padding: "0.875rem 1rem",
                    borderRadius: "var(--radius-md)",
                    border: "1px solid var(--glass-border-medium)",
                    background: "var(--glass-bg-subtle)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                    outline: "none",
                    fontFamily: "inherit",
                  }}
                />
                <div style={{ display: "flex", justifyContent: "flex-end" }}>
                  <GlassButton
                    variant="primary"
                    size="md"
                    type="submit"
                    loading={sending}
                    disabled={!canSend || !input.trim()}
                  >
                    Send
                  </GlassButton>
                </div>
              </form>
            </div>
          </GlassCard>
        </div>
      </main>
    </PageTransition>
  );
}

function TutorSelect({
  label,
  value,
  onChange,
  options,
  disabled,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: SelectOption[];
  disabled?: boolean;
}) {
  return (
    <label style={{ display: "grid", gap: "0.35rem" }}>
      <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)" }}>{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        style={{
          width: "100%",
          padding: "0.75rem 0.9rem",
          borderRadius: "var(--radius-md)",
          border: "1px solid var(--glass-border-medium)",
          background: "var(--glass-bg-subtle)",
          color: "var(--color-text)",
          fontSize: "var(--font-size-base)",
          fontFamily: "inherit",
          outline: "none",
        }}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div
      style={{
        alignSelf: isUser ? "flex-end" : "flex-start",
        maxWidth: "min(100%, 42rem)",
        width: "fit-content",
        padding: "0.85rem 1rem",
        borderRadius: isUser ? "1rem 1rem 0.25rem 1rem" : "1rem 1rem 1rem 0.25rem",
        background: isUser ? "rgba(212, 165, 116, 0.15)" : "var(--glass-bg-subtle)",
        border: `1px solid ${isUser ? "rgba(212, 165, 116, 0.28)" : message.isError ? "rgba(212, 100, 92, 0.3)" : "var(--glass-border-light)"}`,
        color: message.isError ? "var(--color-danger, #d4645c)" : "var(--color-text)",
      }}
    >
      <MarkdownText
        text={message.content}
        style={{
          fontSize: "var(--font-size-sm)",
          lineHeight: 1.6,
          whiteSpace: "pre-wrap",
        }}
      />
    </div>
  );
}
