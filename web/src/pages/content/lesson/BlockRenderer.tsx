import { useState } from "react";
import type { ContentBlock, TableData, InlineCheck } from "./types";
import { MarkdownText } from "../../../components/MarkdownText";

/**
 * Renders a single typed content block with a dedicated UI component.
 * This replaces the "dump everything through MarkdownText" approach.
 */
export function BlockRenderer({ block }: { block: ContentBlock }) {
  // Safety: if content is null/undefined, skip rendering
  if (block.content == null) return null;

  // check_understanding blocks carry InlineCheck[] — handle before string coercion
  if (block.type === "check_understanding") {
    const checks = Array.isArray(block.content) ? (block.content as InlineCheck[]) : [];
    const sectionTitle = typeof block.metadata?.section_title === "string" ? block.metadata.section_title : undefined;
    return <CheckUnderstandingBlock checks={checks} sectionTitle={sectionTitle} />;
  }

  // Coerce content to string for non-table types
  const textContent = typeof block.content === "string"
    ? block.content
    : typeof block.content === "object" && "headers" in block.content
      ? "" // table data handled separately
      : String(block.content);

  switch (block.type) {
    case "table":
      return <InteractiveTable data={block.content as TableData} />;
    case "formula":
      return <FormulaBlock content={textContent} language={block.language} />;
    case "code":
      return <CodeBlock content={textContent} language={block.language} />;
    case "tip":
      return <CalloutCard variant="tip" content={textContent} />;
    case "warning":
      return <CalloutCard variant="warning" content={textContent} />;
    case "example":
      return <ExampleCard content={textContent} />;
    case "step_by_step":
      return <StepByStepBlock content={textContent} />;
    case "list":
      return <StyledList content={textContent} />;
    case "svg":
      return <SvgBlock content={textContent} />;
    case "prose":
    default:
      return <ProseBlock content={textContent} />;
  }
}
// ---------------------------------------------------------------------------
// Block components
// ---------------------------------------------------------------------------

function ProseBlock({ content }: { content: string }) {
  if (!content || !content.trim()) return null;
  return (
    <div className="lesson-block lesson-block--prose">
      <MarkdownText text={content} style={{ lineHeight: 1.7, fontSize: "0.9rem", color: "var(--color-text)" }} />
    </div>
  );
}

function MultipleChoiceCheckCard({
  index,
  check,
  choices,
  selectedChoiceIndex,
  onSelect,
}: {
  index: number;
  check: InlineCheck;
  choices: string[];
  selectedChoiceIndex?: number;
  onSelect: (choiceIndex: number) => void;
}) {
  const correctChoiceIndex = resolveCorrectChoiceIndex(check, choices);
  const hasSelection = typeof selectedChoiceIndex === "number";
  const isCorrect = hasSelection && selectedChoiceIndex === correctChoiceIndex;
  const statusText = hasSelection
    ? isCorrect
      ? "Correct."
      : `Not quite. The best answer is ${choices[correctChoiceIndex]}.`
    : "";

  return (
    <div
      style={{
        background: "rgba(255,255,255,0.02)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: "6px",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "0.5rem 0.75rem",
          fontSize: "0.8125rem",
          lineHeight: 1.5,
          color: "var(--color-text)",
          fontWeight: 500,
        }}
      >
        <div style={{ fontSize: "0.625rem", fontWeight: 700, color: "var(--color-text-muted)", marginBottom: "0.35rem", textTransform: "uppercase", letterSpacing: "0.05em" }}>
          Question {index + 1}
        </div>
        <MarkdownText text={check.question} />
      </div>

      <div style={{ display: "grid", gap: "0.4rem", padding: "0 0.75rem 0.75rem" }}>
        {choices.map((choice, choiceIndex) => {
          const isSelected = selectedChoiceIndex === choiceIndex;
          const isAnswer = choiceIndex === correctChoiceIndex;
          return (
            <button
              key={choiceIndex}
              type="button"
              onClick={() => onSelect(choiceIndex)}
              aria-pressed={isSelected}
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: "0.55rem",
                width: "100%",
                padding: "0.55rem 0.7rem",
                background: isSelected
                  ? isAnswer
                    ? "rgba(80, 200, 120, 0.12)"
                    : "rgba(220, 80, 80, 0.1)"
                  : "rgba(255,255,255,0.03)",
                border: `1px solid ${
                  isSelected
                    ? isAnswer
                      ? "rgba(80, 200, 120, 0.35)"
                      : "rgba(220, 80, 80, 0.35)"
                    : "rgba(255,255,255,0.08)"
                }`,
                borderRadius: "6px",
                cursor: "pointer",
                textAlign: "left",
                color: "var(--color-text)",
                fontSize: "0.8rem",
                lineHeight: 1.5,
              }}
            >
              <span
                style={{
                  flexShrink: 0,
                  width: "1.2rem",
                  height: "1.2rem",
                  borderRadius: "999px",
                  display: "inline-flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "0.625rem",
                  fontWeight: 700,
                  background: isSelected
                    ? isAnswer
                      ? "rgba(80, 200, 120, 0.2)"
                      : "rgba(220, 80, 80, 0.2)"
                    : "rgba(255,255,255,0.08)",
                  color: isSelected
                    ? isAnswer
                      ? "rgba(80, 200, 120, 0.95)"
                      : "rgba(220, 80, 80, 0.95)"
                    : "var(--color-text-muted)",
                  marginTop: "0.05rem",
                }}
              >
                {String.fromCharCode(65 + choiceIndex)}
              </span>
              <span style={{ minWidth: 0, flex: 1 }}>
                <MarkdownText text={choice} />
              </span>
            </button>
          );
        })}
      </div>

      {hasSelection && (
        <div
          style={{
            padding: "0.55rem 0.75rem 0.75rem",
            borderTop: "1px solid rgba(255,255,255,0.06)",
            background: isCorrect ? "rgba(80, 200, 120, 0.05)" : "rgba(220, 80, 80, 0.05)",
            fontSize: "0.75rem",
            lineHeight: 1.55,
            color: "var(--color-text)",
          }}
        >
          <div style={{ fontWeight: 600, marginBottom: check.rationale ? "0.25rem" : 0, color: isCorrect ? "rgba(80, 200, 120, 0.95)" : "rgba(220, 80, 80, 0.95)" }}>
            {statusText}
          </div>
          {check.rationale && <MarkdownText text={check.rationale} />}
        </div>
      )}
    </div>
  );
}

function resolveCorrectChoiceIndex(check: InlineCheck, choices: string[]): number {
  if (typeof check.correct_choice_index === "number" && choices[check.correct_choice_index]) {
    return check.correct_choice_index;
  }

  const normalizedAnswer = normalizeChoiceText(check.answer);
  const choiceIndex = choices.findIndex((choice) => normalizeChoiceText(choice) === normalizedAnswer);
  if (choiceIndex >= 0) {
    return choiceIndex;
  }

  const letterIndex = parseChoiceLetter(check.answer, choices.length);
  if (letterIndex !== null) {
    return letterIndex;
  }

  return 0;
}

function parseChoiceLetter(answer: string, choiceCount: number): number | null {
  if (!answer) return null;
  const match = answer.trim().match(/^(?:choice\s*)?([abc])(?:[\).:\-\s].*)?$/i);
  if (!match) return null;
  const index = match[1].toUpperCase().charCodeAt(0) - 65;
  return index >= 0 && index < choiceCount ? index : null;
}

function normalizeChoiceText(text: string): string {
  return text
    .replace(/[`*_]/g, "")
    .replace(/\s+/g, " ")
    .replace(/[.?!]+$/g, "")
    .trim()
    .toLowerCase();
}

function resolveChoiceOptions(check: InlineCheck, sectionTitle: string | undefined, questionIndex: number): string[] {
  const explicitChoices = Array.isArray(check.choices)
    ? check.choices.map((choice) => choice.trim()).filter(Boolean)
    : [];

  if (explicitChoices.length >= 3) {
    return explicitChoices.slice(0, 3);
  }

  const answer = check.answer?.trim() || "Not sure";
  const pool = buildDistractorPool(check.question, sectionTitle, answer);
  const combined = [answer, ...pool];
  const unique: string[] = [];
  for (const option of combined) {
    if (!option) continue;
    if (unique.some((item) => normalizeChoiceText(item) === normalizeChoiceText(option))) {
      continue;
    }
    unique.push(option);
    if (unique.length === 3) break;
  }

  while (unique.length < 3) {
    unique.push(unique.length === 1 ? "It depends" : "None of these");
  }

  const rotation = questionIndex % 3;
  if (rotation === 1) {
    return [unique[1], unique[0], unique[2]];
  }
  if (rotation === 2) {
    return [unique[1], unique[2], unique[0]];
  }
  return unique;
}

function buildDistractorPool(question: string, sectionTitle: string | undefined, answer: string): string[] {
  const lowerTitle = (sectionTitle || "").toLowerCase();
  const pool: string[] = [];

  const add = (...items: string[]) => {
    for (const item of items) {
      if (!item) continue;
      if (normalizeChoiceText(item) === normalizeChoiceText(answer)) continue;
      if (pool.some((existing) => normalizeChoiceText(existing) === normalizeChoiceText(item))) continue;
      pool.push(item);
    }
  };

  const extractedAlternatives = extractQuestionAlternatives(question);
  add(...extractedAlternatives);

  if (/^(true|false)$/i.test(answer)) {
    add("True", "False", "It depends");
    return pool;
  }

  if (lowerTitle.includes("prefix")) {
    add("before", "after", "under or below", "many or multiple", "self", "between", "again or back");
  } else if (lowerTitle.includes("root")) {
    add("carry", "write", "look or see", "life", "time", "build", "small", "hear or listen", "water");
  } else if (lowerTitle.includes("suffix")) {
    add("without", "full of", "person who", "most", "state or quality", "adverb", "past tense");
  } else if (lowerTitle.includes("family")) {
    add("base word", "root", "affix", "same family", "different spelling");
  } else if (lowerTitle.includes("synonym")) {
    add("antonym", "tone", "register", "collocation", "context clue");
  } else if (lowerTitle.includes("antonym")) {
    add("synonym", "same meaning", "definition", "tone", "context clue");
  } else if (lowerTitle.includes("connotation")) {
    add("denotation", "grammar", "spelling", "syllable count", "dictionary meaning");
  } else if (lowerTitle.includes("context")) {
    add("dictionary guess", "part of speech", "sentence clue", "random guess", "word memory");
  } else if (lowerTitle.includes("idiom") || lowerTitle.includes("figurative")) {
    add("literal meaning", "word-for-word meaning", "dictionary definition", "surface meaning");
  } else if (lowerTitle.includes("connector")) {
    add("contrast", "cause", "addition", "example", "condition", "result");
  } else if (lowerTitle.includes("grammar")) {
    add("nearest noun", "plural verb", "object case", "sound", "part of speech");
  } else if (lowerTitle.includes("subject") || lowerTitle.includes("agreement") || lowerTitle.includes("collective") || lowerTitle.includes("there")) {
    add("singular verb", "plural verb", "head noun", "nearest noun", "subject phrase", "verb form");
  } else if (lowerTitle.includes("pronoun")) {
    add("antecedent", "ownership", "plural noun", "verb", "adjective");
  } else if (lowerTitle.includes("tense")) {
    add("simple past", "simple present", "future", "perfect", "progressive");
  } else if (lowerTitle.includes("contrast")) {
    add("addition", "cause", "example", "condition", "sequence");
  } else if (lowerTitle.includes("cause")) {
    add("contrast", "result", "condition", "example", "sequence");
  } else if (lowerTitle.includes("elimination")) {
    add("meaning", "grammar", "tone", "logic", "punctuation");
  } else if (lowerTitle.includes("register")) {
    add("casual", "formal", "technical", "neutral", "official");
  } else {
    add("not quite", "something else", "another clue", "best fit");
  }

  if (pool.length < 2) {
    add("Another choice", "Different choice", "Closest fit");
  }

  return pool;
}

function extractQuestionAlternatives(question: string): string[] {
  const matches: string[] = [];
  const orMatch = question.match(/:\s*(.+?)\s+or\s+(.+?)[?]?$/i);
  if (orMatch) {
    matches.push(orMatch[1].trim().replace(/[?.,]$/g, ""));
    matches.push(orMatch[2].trim().replace(/[?.,]$/g, ""));
  }

  const backtickMatches = [...question.matchAll(/`([^`]+)`/g)].map((match) => match[1].trim());
  matches.push(...backtickMatches);

  return matches.filter(Boolean);
}

function InteractiveTable({ data }: { data: TableData }) {
  if (!data || !data.headers) return null;

  return (
    <div className="lesson-block lesson-block--table">
      <div style={{ overflowX: "auto", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.1)" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.8125rem", lineHeight: 1.5 }}>
          <thead>
            <tr>
              {data.headers.map((h, i) => (
                <th
                  key={i}
                  style={{
                    padding: "0.5rem 0.75rem",
                    borderBottom: "2px solid rgba(255,255,255,0.15)",
                    borderRight: i < data.headers.length - 1 ? "1px solid rgba(255,255,255,0.08)" : "none",
                    textAlign: "left",
                    fontWeight: 600,
                    background: "rgba(212, 165, 116, 0.08)",
                    whiteSpace: "nowrap",
                    color: "var(--color-text)",
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.rows.map((row, ri) => (
              <tr key={ri} style={ri % 2 === 1 ? { background: "rgba(255,255,255,0.02)" } : undefined}>
                {row.map((cell, ci) => (
                  <td
                    key={ci}
                    style={{
                      padding: "0.4rem 0.75rem",
                      borderBottom: "1px solid rgba(255,255,255,0.06)",
                      borderRight: ci < data.headers.length - 1 ? "1px solid rgba(255,255,255,0.06)" : "none",
                      verticalAlign: "top",
                      color: "var(--color-text)",
                    }}
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function FormulaBlock({ content, language }: { content: string; language?: string }) {
  return (
    <div className="lesson-block lesson-block--formula">
      <div
        style={{
          background: "rgba(212, 165, 116, 0.04)",
          border: "1px solid rgba(212, 165, 116, 0.2)",
          borderRadius: "8px",
          padding: "1rem 1.25rem",
          fontFamily: "monospace",
          fontSize: "0.875rem",
          lineHeight: 1.6,
          whiteSpace: "pre-wrap",
          color: "var(--color-text)",
          position: "relative",
        }}
      >
        <span
          style={{
            position: "absolute",
            top: "0.375rem",
            right: "0.5rem",
            fontSize: "0.625rem",
            color: "var(--color-accent, #d4a574)",
            opacity: 0.7,
            textTransform: "uppercase",
            letterSpacing: "0.05em",
          }}
        >
          {language || "formula"}
        </span>
        {content}
      </div>
    </div>
  );
}

function CodeBlock({ content, language }: { content: string; language?: string }) {
  return (
    <div className="lesson-block lesson-block--code">
      <div
        style={{
          background: "rgba(0, 0, 0, 0.3)",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          padding: "1rem 1.25rem",
          fontFamily: "'Fira Code', 'Cascadia Code', monospace",
          fontSize: "0.8125rem",
          lineHeight: 1.6,
          whiteSpace: "pre-wrap",
          overflowX: "auto",
          color: "var(--color-text)",
          position: "relative",
        }}
      >
        {language && (
          <span
            style={{
              position: "absolute",
              top: "0.375rem",
              right: "0.5rem",
              fontSize: "0.625rem",
              color: "var(--color-text-muted)",
              opacity: 0.6,
              textTransform: "uppercase",
            }}
          >
            {language}
          </span>
        )}
        {content}
      </div>
    </div>
  );
}

function CalloutCard({ variant, content }: { variant: "tip" | "warning"; content: string }) {
  const config = {
    tip: {
      bg: "rgba(212, 165, 116, 0.06)",
      border: "rgba(212, 165, 116, 0.35)",
      icon: "💡",
      label: "Tip",
    },
    warning: {
      bg: "rgba(220, 80, 80, 0.06)",
      border: "rgba(220, 80, 80, 0.35)",
      icon: "⚠️",
      label: "Watch Out",
    },
  }[variant];

  return (
    <div className="lesson-block lesson-block--callout">
      <div
        style={{
          background: config.bg,
          borderLeft: `4px solid ${config.border}`,
          borderRadius: "0 8px 8px 0",
          padding: "0.75rem 1rem",
        }}
      >
        <div style={{ fontWeight: 600, fontSize: "0.75rem", marginBottom: "0.25rem", opacity: 0.8 }}>
          {config.icon} {config.label}
        </div>
        <MarkdownText text={content} style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }} />
      </div>
    </div>
  );
}

function ExampleCard({ content }: { content: string }) {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="lesson-block lesson-block--example">
      <div
        style={{
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: "8px",
          overflow: "hidden",
        }}
      >
        <button
          onClick={() => setExpanded(!expanded)}
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            padding: "0.5rem 0.75rem",
            background: "rgba(255,255,255,0.03)",
            border: "none",
            borderBottom: expanded ? "1px solid rgba(255,255,255,0.08)" : "none",
            cursor: "pointer",
            color: "var(--color-text)",
            fontSize: "0.75rem",
            fontWeight: 600,
          }}
        >
          <span style={{ transform: expanded ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.15s" }}>▶</span>
          Example
        </button>
        {expanded && (
          <div style={{ padding: "0.75rem 1rem" }}>
            <MarkdownText text={content} style={{ fontSize: "0.8125rem", lineHeight: 1.6, color: "var(--color-text)" }} />
          </div>
        )}
      </div>
    </div>
  );
}

function StepByStepBlock({ content }: { content: string }) {
  const steps = content.split("\n").filter((l) => l.trim());

  return (
    <div className="lesson-block lesson-block--steps">
      <div
        style={{
          background: "rgba(255,255,255,0.02)",
          border: "1px solid rgba(255,255,255,0.08)",
          borderRadius: "8px",
          padding: "0.75rem 1rem",
        }}
      >
        <div style={{ fontSize: "0.6875rem", fontWeight: 600, color: "var(--color-accent, #d4a574)", marginBottom: "0.5rem", textTransform: "uppercase", letterSpacing: "0.04em" }}>
          Step-by-Step
        </div>
        <ol style={{ margin: 0, paddingLeft: "1.25rem" }}>
          {steps.map((step, i) => {
            // Strip "Step N:" prefix if present
            const cleaned = step.replace(/^Step\s+\d+[:.]\s*/i, "").trim();
            return (
              <li key={i} style={{ marginBottom: "0.375rem", lineHeight: 1.6, fontSize: "0.8125rem", color: "var(--color-text)" }}>
                <MarkdownText text={cleaned} />
              </li>
            );
          })}
        </ol>
      </div>
    </div>
  );
}

function StyledList({ content }: { content: string }) {
  const lines = content.split("\n").filter((l) => l.trim());
  const isOrdered = /^\d+\./.test(lines[0]?.trim() || "");

  const items = lines.map((l) => l.replace(/^(\d+\.|[-*])\s*/, "").trim());

  const ListTag = isOrdered ? "ol" : "ul";

  return (
    <div className="lesson-block lesson-block--list">
      <ListTag style={{ margin: "0.25rem 0", paddingLeft: "1.5rem" }}>
        {items.map((item, i) => (
          <li key={i} style={{ marginBottom: "0.3rem", lineHeight: 1.6, fontSize: "0.875rem", color: "var(--color-text)" }}>
            <MarkdownText text={item} />
          </li>
        ))}
      </ListTag>
    </div>
  );
}

function SvgBlock({ content }: { content: string }) {
  const trimmed = content.trim();
  if (!(/^<svg[\s>]/i.test(trimmed) && /<\/svg>\s*$/i.test(trimmed))) {
    return null;
  }

  return (
    <div
      className="lesson-block lesson-block--svg"
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "1rem",
        background: "rgba(255,255,255,0.03)",
        borderRadius: "8px",
        border: "1px solid rgba(255,255,255,0.08)",
        overflow: "auto",
      }}
      dangerouslySetInnerHTML={{ __html: trimmed }}
      aria-label="Diagram"
      role="img"
    />
  );
}

// ---------------------------------------------------------------------------
// Check Your Understanding — inline interactive reveal cards
// ---------------------------------------------------------------------------

function CheckUnderstandingBlock({
  checks,
  sectionTitle,
}: {
  checks: InlineCheck[];
  sectionTitle?: string;
}) {
  const [revealed, setRevealed] = useState<Set<number>>(new Set());
  const [selectedChoices, setSelectedChoices] = useState<Record<number, number>>({});

  if (checks.length === 0) return null;

  function toggle(i: number) {
    setRevealed((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  }

  function selectChoice(questionIndex: number, choiceIndex: number) {
    setSelectedChoices((prev) => ({
      ...prev,
      [questionIndex]: choiceIndex,
    }));
  }

  return (
    <div
      className="lesson-block lesson-block--check"
      style={{
        background: "rgba(80, 200, 120, 0.04)",
        border: "1px solid rgba(80, 200, 120, 0.2)",
        borderRadius: "8px",
        padding: "0.875rem 1rem",
      }}
    >
      <div
        style={{
          fontSize: "0.6875rem",
          fontWeight: 700,
          color: "rgba(80, 200, 120, 0.9)",
          marginBottom: "0.625rem",
          textTransform: "uppercase",
          letterSpacing: "0.05em",
        }}
      >
        ✓ Check Your Understanding
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.625rem" }}>
        {checks.map((check, i) => {
          const choices = resolveChoiceOptions(check, sectionTitle, i);
          if (choices.length >= 3) {
            return (
              <MultipleChoiceCheckCard
                key={i}
                index={i}
                check={check}
                choices={choices}
                selectedChoiceIndex={selectedChoices[i]}
                onSelect={(choiceIndex) => selectChoice(i, choiceIndex)}
              />
            );
          }

          const isOpen = revealed.has(i);
          return (
            <div
              key={i}
              style={{
                background: "rgba(255,255,255,0.02)",
                border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "6px",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  padding: "0.5rem 0.75rem",
                  fontSize: "0.8125rem",
                  lineHeight: 1.5,
                  color: "var(--color-text)",
                  fontWeight: 500,
                }}
              >
                <MarkdownText text={check.question} />
              </div>
              <button
                type="button"
                onClick={() => toggle(i)}
                aria-expanded={isOpen}
                style={{
                  display: "block",
                  width: "100%",
                  padding: "0.35rem 0.75rem",
                  background: isOpen ? "rgba(80, 200, 120, 0.08)" : "rgba(255,255,255,0.03)",
                  border: "none",
                  borderTop: "1px solid rgba(255,255,255,0.06)",
                  cursor: "pointer",
                  textAlign: "left",
                  fontSize: "0.6875rem",
                  fontWeight: 600,
                  color: isOpen ? "rgba(80, 200, 120, 0.9)" : "var(--color-text-muted)",
                  letterSpacing: "0.03em",
                }}
              >
                {isOpen ? "▾ Hide answer" : "▸ Show answer"}
              </button>
              {isOpen && (
                <div
                  style={{
                    padding: "0.5rem 0.75rem",
                    background: "rgba(80, 200, 120, 0.05)",
                    borderTop: "1px solid rgba(80, 200, 120, 0.15)",
                    fontSize: "0.8125rem",
                    lineHeight: 1.5,
                    color: "var(--color-text)",
                  }}
                >
                  <MarkdownText text={check.answer} />
                  {check.rationale && (
                    <div
                      style={{
                        marginTop: "0.375rem",
                        fontSize: "0.75rem",
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
    </div>
  );
}
