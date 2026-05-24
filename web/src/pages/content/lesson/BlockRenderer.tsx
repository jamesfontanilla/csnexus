import { useState } from "react";
import type { ContentBlock, TableData } from "./types";
import { MarkdownText } from "../../../components/MarkdownText";

/**
 * Renders a single typed content block with a dedicated UI component.
 * This replaces the "dump everything through MarkdownText" approach.
 */
export function BlockRenderer({ block }: { block: ContentBlock }) {
  switch (block.type) {
    case "table":
      return <InteractiveTable data={block.content as TableData} />;
    case "formula":
      return <FormulaBlock content={block.content as string} language={block.language} />;
    case "code":
      return <CodeBlock content={block.content as string} language={block.language} />;
    case "tip":
      return <CalloutCard variant="tip" content={block.content as string} />;
    case "warning":
      return <CalloutCard variant="warning" content={block.content as string} />;
    case "example":
      return <ExampleCard content={block.content as string} />;
    case "step_by_step":
      return <StepByStepBlock content={block.content as string} />;
    case "list":
      return <StyledList content={block.content as string} />;
    case "svg":
      return <SvgBlock content={block.content as string} />;
    case "prose":
    default:
      return <ProseBlock content={block.content as string} />;
  }
}

// ---------------------------------------------------------------------------
// Block components
// ---------------------------------------------------------------------------

function ProseBlock({ content }: { content: string }) {
  return (
    <div className="lesson-block lesson-block--prose">
      <MarkdownText text={content} style={{ lineHeight: 1.7, fontSize: "0.9rem" }} />
    </div>
  );
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
