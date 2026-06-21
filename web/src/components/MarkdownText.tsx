import React, { useState } from "react";

/**
 * Lightweight inline markdown renderer.
 * Handles: **bold**, *italic*, `code`, - bullet lists, | tables |,
 * ##/###/#### section boxes, > blockquote callouts, and line breaks.
 * No external dependencies.
 */
export function MarkdownText({ text, style }: { text: string; style?: React.CSSProperties }) {
  const blocks = splitByHeadingSections(text);

  return (
    <div style={style}>
      {blocks.map((block, i) =>
        block.type === "section" ? (
          <SectionBox key={i} level={block.level} title={block.title} body={block.body} />
        ) : (
          <RawMarkdownBlock key={i} text={block.text} />
        )
      )}
    </div>
  );
}

type ContentBlock =
  | { type: "raw"; text: string }
  | { type: "section"; level: 2 | 3 | 4; title: string; body: string };

function splitByHeadingSections(text: string): ContentBlock[] {
  const lines = text.split("\n");
  const blocks: ContentBlock[] = [];
  let rawBuffer: string[] = [];
  let sectionTitle: string | null = null;
  let sectionLevel: 2 | 3 | 4 | null = null;
  let sectionBuffer: string[] = [];

  function flushRaw() {
    const joined = rawBuffer.join("\n").trim();
    if (joined) blocks.push({ type: "raw", text: joined });
    rawBuffer = [];
  }

  function flushSection() {
    if (sectionTitle !== null && sectionLevel !== null) {
      blocks.push({
        type: "section",
        level: sectionLevel,
        title: sectionTitle,
        body: sectionBuffer.join("\n").trim(),
      });
      sectionTitle = null;
      sectionLevel = null;
      sectionBuffer = [];
    }
  }

  for (const line of lines) {
    const trimmed = line.trim();
    const headingMatch = trimmed.match(/^(#{2,4})\s+(.+)$/);
    if (headingMatch) {
      if (sectionTitle !== null) flushSection();
      else flushRaw();
      sectionLevel = headingMatch[1].length as 2 | 3 | 4;
      sectionTitle = headingMatch[2].trim();
      sectionBuffer = [];
    } else if (sectionTitle !== null) {
      sectionBuffer.push(line);
    } else {
      rawBuffer.push(line);
    }
  }
  if (sectionTitle !== null) flushSection();
  else flushRaw();

  return blocks;
}

function SectionBox({ level, title, body }: { level: 2 | 3 | 4; title: string; body: string }) {
  const isLevel2 = level === 2;
  const isLevel3 = level === 3;
  return (
    <div
      style={{
        margin: isLevel2 ? "0.875rem 0" : "0.75rem 0",
        border: "1px solid var(--glass-border-medium, rgba(255,255,255,0.12))",
        borderRadius: "var(--radius-md, 8px)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: isLevel2 ? "0.45rem 0.85rem" : "0.4rem 0.75rem",
          background: isLevel2 ? "rgba(212, 165, 116, 0.12)" : isLevel3 ? "rgba(212, 165, 116, 0.09)" : "rgba(212, 165, 116, 0.08)",
          borderBottom: "1px solid var(--glass-border-medium, rgba(255,255,255,0.12))",
          fontWeight: isLevel2 ? 700 : 600,
          fontSize: isLevel2 ? "0.875rem" : "0.8125rem",
          color: "var(--color-text)",
        }}
      >
        <InlineMarkdown text={title} />
      </div>
      {body && (
        <div style={{ padding: isLevel2 ? "0.6rem 0.85rem" : "0.5rem 0.75rem" }}>
          <RawMarkdownBlock text={body} />
        </div>
      )}
    </div>
  );
}

function CalloutBox({ text, variant }: { text: string; variant: "tip" | "warning" | "note" }) {
  const styles: Record<string, { bg: string; border: string; icon: string }> = {
    tip: { bg: "rgba(212, 165, 116, 0.06)", border: "rgba(212, 165, 116, 0.3)", icon: "💡" },
    warning: { bg: "rgba(220, 80, 80, 0.06)", border: "rgba(220, 80, 80, 0.3)", icon: "⚠️" },
    note: { bg: "rgba(100, 160, 220, 0.06)", border: "rgba(100, 160, 220, 0.3)", icon: "📝" },
  };
  const s = styles[variant];

  // Strip leading emoji if already present in text
  const cleanText = text.replace(/^[💡⚠️🧠📝]\s*/, "").replace(/^\*\*/, "").replace(/\*\*$/, "");

  return (
    <div
      style={{
        margin: "0.5rem 0",
        padding: "0.5rem 0.75rem",
        background: s.bg,
        borderLeft: `3px solid ${s.border}`,
        borderRadius: "0 var(--radius-sm, 4px) var(--radius-sm, 4px) 0",
        fontSize: "0.8125rem",
        lineHeight: 1.5,
      }}
    >
      <InlineMarkdown text={cleanText} />
    </div>
  );
}

function CSEExample({ question, details }: { question: string; details: string[] }) {
  const [revealed, setRevealed] = useState(false);

  // Separate choices from explanation
  const choicesLine = details.find((l) => l.startsWith("- (") || l.startsWith("* ("));
  const explanationLine = details.find((l) => l.startsWith("- *") || l.startsWith("* *"));

  // Extract difficulty badge
  const diffMatch = question.match(/^\*\*(Easy|Medium|Hard):\*\*/);
  const difficulty = diffMatch ? diffMatch[1] : "";
  const questionText = question.replace(/^\*\*(Easy|Medium|Hard):\*\*\s*/, "");

  const badgeColors: Record<string, string> = {
    Easy: "rgba(80, 200, 120, 0.2)",
    Medium: "rgba(212, 165, 116, 0.2)",
    Hard: "rgba(220, 80, 80, 0.2)",
  };

  return (
    <div style={{ margin: "0.5rem 0", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "6px", overflow: "hidden" }}>
      <div style={{ padding: "0.5rem 0.75rem", background: "rgba(255,255,255,0.02)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.25rem" }}>
          {difficulty && (
            <span style={{ fontSize: "0.625rem", fontWeight: 700, padding: "0.1rem 0.4rem", borderRadius: "3px", background: badgeColors[difficulty] || "rgba(255,255,255,0.1)", textTransform: "uppercase", letterSpacing: "0.03em" }}>
              {difficulty}
            </span>
          )}
        </div>
        <p style={{ margin: 0, fontSize: "0.8125rem", lineHeight: 1.5 }}>
          <InlineMarkdown text={questionText} />
        </p>
        {choicesLine && (
          <p style={{ margin: "0.25rem 0 0 0", fontSize: "0.75rem", color: "var(--color-text-secondary)" }}>
            <InlineMarkdown text={choicesLine.slice(2)} />
          </p>
        )}
      </div>
      {!revealed ? (
        <button
          onClick={() => setRevealed(true)}
          style={{ width: "100%", padding: "0.375rem", background: "rgba(212, 165, 116, 0.06)", border: "none", borderTop: "1px solid rgba(255,255,255,0.06)", cursor: "pointer", fontSize: "0.6875rem", color: "var(--color-accent, #d4a574)", fontWeight: 600 }}
        >
          Show Answer
        </button>
      ) : (
        <div style={{ padding: "0.4rem 0.75rem", borderTop: "1px solid rgba(255,255,255,0.06)", background: "rgba(80, 200, 120, 0.04)", fontSize: "0.75rem", lineHeight: 1.5 }}>
          {explanationLine && <InlineMarkdown text={explanationLine.slice(2)} />}
        </div>
      )}
    </div>
  );
}

function RawMarkdownBlock({ text }: { text: string }) {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];
  let bulletBuffer: string[] = [];
  let tableBuffer: string[] = [];
  let key = 0;
  let i = 0;

  function flushBullets() {
    if (bulletBuffer.length > 0) {
      elements.push(
        <ul key={key++} style={{ margin: "0.25rem 0", paddingLeft: "1.25rem" }}>
          {bulletBuffer.map((b, bi) => (
            <li key={bi} style={{ marginBottom: "0.2rem", lineHeight: 1.5, fontSize: "inherit" }}>
              <InlineMarkdown text={b} />
            </li>
          ))}
        </ul>
      );
      bulletBuffer = [];
    }
  }

  function flushTable() {
    if (tableBuffer.length > 0) {
      elements.push(<MarkdownTable key={key++} rows={tableBuffer} />);
      tableBuffer = [];
    }
  }

  while (i < lines.length) {
    const trimmed = lines[i].trim();

    // SVG block: <svg ...> ... </svg>
    if (/^\s*<svg[\s>]/i.test(lines[i])) {
      flushBullets();
      flushTable();
      const svgLines: string[] = [lines[i]];
      // Check if SVG closes on the same line
      if (/<\/svg>/i.test(lines[i])) {
        elements.push(<SvgBlock key={key++} svg={lines[i].trim()} />);
        i++;
        continue;
      }
      // Multi-line SVG
      i++;
      while (i < lines.length) {
        svgLines.push(lines[i]);
        if (/<\/svg>/i.test(lines[i])) {
          i++;
          break;
        }
        i++;
      }
      elements.push(<SvgBlock key={key++} svg={svgLines.join("\n").trim()} />);
      continue;
    }

    // Blockquote callouts: > prefixed lines
    if (trimmed.startsWith("> ")) {
      flushBullets();
      flushTable();
      const calloutLines: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith("> ")) {
        calloutLines.push(lines[i].trim().slice(2));
        i++;
      }
      const calloutText = calloutLines.join(" ");
      const isWarning = calloutText.includes("⚠️") || calloutText.toLowerCase().includes("critical") || calloutText.toLowerCase().includes("common trap");
      const isTip = calloutText.includes("💡") || calloutText.includes("🧠");
      elements.push(<CalloutBox key={key++} text={calloutText} variant={isWarning ? "warning" : isTip ? "tip" : "note"} />);
      continue;
    }

    // Standalone emoji callouts (stripped blockquotes from parser)
    if (trimmed.startsWith("💡") || trimmed.startsWith("⚠️") || trimmed.startsWith("🧠")) {
      flushBullets();
      flushTable();
      const calloutLines: string[] = [trimmed];
      i++;
      while (i < lines.length && lines[i].trim() && !lines[i].trim().startsWith("|") && !lines[i].trim().startsWith("#") && !lines[i].trim().startsWith(">")) {
        calloutLines.push(lines[i].trim());
        i++;
      }
      const calloutText = calloutLines.join(" ");
      const isWarning = calloutText.includes("⚠️");
      elements.push(<CalloutBox key={key++} text={calloutText} variant={isWarning ? "warning" : "tip"} />);
      continue;
    }

    // Table row: starts and ends with |
    if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
      flushBullets();
      tableBuffer.push(trimmed);
      i++;
      continue;
    }

    // Flush pending table
    flushTable();

    // CSE-Style interactive example: **Easy:**/**Medium:**/**Hard:** followed by choices
    if (/^\*\*(Easy|Medium|Hard):\*\*/.test(trimmed)) {
      flushBullets();
      const questionLine = trimmed;
      const exampleLines: string[] = [];
      i++;
      // Collect subsequent bullet lines (choices + explanation)
      while (i < lines.length && (lines[i].trim().startsWith("- ") || lines[i].trim().startsWith("* ") || lines[i].trim() === "")) {
        if (lines[i].trim()) exampleLines.push(lines[i].trim());
        i++;
      }
      elements.push(<CSEExample key={key++} question={questionLine} details={exampleLines} />);
      continue;
    }

    // Bullet point (- or *)
    if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
      bulletBuffer.push(trimmed.slice(2));
      i++;
      continue;
    }

    // Flush pending bullets
    flushBullets();

    // Horizontal rule — skip
    if (trimmed === "---" || trimmed === "***" || trimmed === "- - -") {
      i++;
      continue;
    }

    // Empty line — skip (no <br> spam)
    if (trimmed === "") {
      i++;
      continue;
    }

    // Regular paragraph
    elements.push(
      <p key={key++} style={{ margin: "0 0 0.375rem 0", lineHeight: 1.6 }}>
        <InlineMarkdown text={trimmed} />
      </p>
    );
    i++;
  }

  flushBullets();
  flushTable();

  return <>{elements}</>;
}

/**
 * Renders a markdown table with compact styling and distinct columns.
 */
function MarkdownTable({ rows }: { rows: string[] }) {
  function parseCells(row: string): string[] {
    return row.split("|").slice(1, -1).map((cell) => cell.trim());
  }

  function isSeparatorRow(row: string): boolean {
    return /^\|[\s\-:|]+\|$/.test(row);
  }

  const sepIdx = rows.findIndex(isSeparatorRow);
  const headerRows = sepIdx > 0 ? rows.slice(0, sepIdx) : [];
  const bodyRows = sepIdx >= 0 ? rows.slice(sepIdx + 1) : rows;

  const colCount = headerRows.length > 0
    ? parseCells(headerRows[0]).length
    : bodyRows.length > 0 ? parseCells(bodyRows[0]).length : 0;

  function normalizedCells(row: string): string[] {
    const cells = parseCells(row);
    while (cells.length < colCount) cells.push("");
    return cells.slice(0, colCount);
  }

  return (
    <div style={{ overflowX: "auto", margin: "0.5rem 0", borderRadius: "4px", border: "1px solid rgba(255,255,255,0.1)" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.8125rem", lineHeight: 1.4, tableLayout: "auto" }}>
        {headerRows.length > 0 && (
          <thead>
            {headerRows.map((row, ri) => (
              <tr key={ri}>
                {normalizedCells(row).map((cell, ci) => (
                  <th
                    key={ci}
                    style={{
                      padding: "0.35rem 0.5rem",
                      borderBottom: "2px solid rgba(255,255,255,0.15)",
                      borderRight: ci < colCount - 1 ? "1px solid rgba(255,255,255,0.08)" : "none",
                      textAlign: "left",
                      fontWeight: 600,
                      background: "rgba(212, 165, 116, 0.08)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    <InlineMarkdown text={cell} />
                  </th>
                ))}
              </tr>
            ))}
          </thead>
        )}
        <tbody>
          {bodyRows.map((row, ri) => (
            <tr key={ri} style={ri % 2 === 1 ? { background: "rgba(255,255,255,0.02)" } : undefined}>
              {normalizedCells(row).map((cell, ci) => (
                <td
                  key={ci}
                  style={{
                    padding: "0.3rem 0.5rem",
                    borderBottom: "1px solid rgba(255,255,255,0.06)",
                    borderRight: ci < colCount - 1 ? "1px solid rgba(255,255,255,0.06)" : "none",
                    textAlign: "left",
                    verticalAlign: "top",
                  }}
                >
                  <InlineMarkdown text={cell} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/**
 * Renders an inline SVG diagram safely using dangerouslySetInnerHTML.
 * Only allows content that starts with a valid <svg tag.
 */
function SvgBlock({ svg }: { svg: string }) {
  // Basic validation: must start with <svg and end with </svg>
  const trimmed = svg.trim();
  if (!(/^<svg[\s>]/i.test(trimmed) && /<\/svg>\s*$/i.test(trimmed))) {
    return null;
  }

  return (
    <div
      style={{
        margin: "0.75rem 0",
        display: "flex",
        justifyContent: "center",
        overflow: "auto",
        padding: "0.5rem",
        background: "rgba(255,255,255,0.03)",
        borderRadius: "var(--radius-md, 8px)",
        border: "1px solid rgba(255,255,255,0.08)",
      }}
      dangerouslySetInnerHTML={{ __html: trimmed }}
      aria-label="Diagram"
      role="img"
    />
  );
}

/**
 * Renders inline markdown: **bold**, *italic*, `code`, ~~strikethrough~~
 */
function InlineMarkdown({ text }: { text: string }) {
  const parts: React.ReactNode[] = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    // Bold: **text**
    const boldMatch = remaining.match(/^(.*?)\*\*(.+?)\*\*(.*)/s);
    if (boldMatch) {
      if (boldMatch[1]) parts.push(<span key={key++}>{boldMatch[1]}</span>);
      parts.push(<strong key={key++}>{boldMatch[2]}</strong>);
      remaining = boldMatch[3];
      continue;
    }

    // Italic: *text*
    const italicMatch = remaining.match(/^(.*?)\*(.+?)\*(.*)/s);
    if (italicMatch) {
      if (italicMatch[1]) parts.push(<span key={key++}>{italicMatch[1]}</span>);
      parts.push(<em key={key++}>{italicMatch[2]}</em>);
      remaining = italicMatch[3];
      continue;
    }

    // Inline code: `text`
    const codeMatch = remaining.match(/^(.*?)`(.+?)`(.*)/s);
    if (codeMatch) {
      if (codeMatch[1]) parts.push(<span key={key++}>{codeMatch[1]}</span>);
      parts.push(
        <code key={key++} style={{ background: "rgba(255,255,255,0.06)", padding: "0.1rem 0.3rem", borderRadius: "3px", fontSize: "0.85em" }}>
          {codeMatch[2]}
        </code>
      );
      remaining = codeMatch[3];
      continue;
    }

    // No more patterns
    parts.push(<span key={key++}>{remaining}</span>);
    break;
  }

  return <>{parts}</>;
}
