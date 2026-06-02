import type { ReactNode, CSSProperties } from "react";
import { GradientText } from "./GradientText";

// ─── Heading ────────────────────────────────────────────────────────────────

interface HeadingProps {
  level: 1 | 2 | 3 | 4;
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  gradient?: boolean;
}

const headingStyles: Record<number, CSSProperties> = {
  1: {
    fontSize: "var(--heading-1-size)",
    fontWeight: "var(--heading-1-weight)" as unknown as number,
    lineHeight: "var(--heading-1-line-height)",
    letterSpacing: "var(--heading-1-letter-spacing)",
    fontFamily: "var(--heading-1-font)",
    color: "var(--color-text)",
    margin: 0,
  },
  2: {
    fontSize: "var(--heading-2-size)",
    fontWeight: "var(--heading-2-weight)" as unknown as number,
    lineHeight: "var(--heading-2-line-height)",
    letterSpacing: "var(--heading-2-letter-spacing)",
    fontFamily: "var(--heading-2-font)",
    color: "var(--color-text)",
    margin: 0,
  },
  3: {
    fontSize: "var(--heading-3-size)",
    fontWeight: "var(--heading-3-weight)" as unknown as number,
    lineHeight: "var(--heading-3-line-height)",
    letterSpacing: "var(--heading-3-letter-spacing)",
    fontFamily: "var(--heading-3-font)",
    color: "var(--color-text)",
    margin: 0,
  },
  4: {
    fontSize: "var(--heading-4-size)",
    fontWeight: "var(--heading-4-weight)" as unknown as number,
    lineHeight: "var(--heading-4-line-height)",
    letterSpacing: "var(--heading-4-letter-spacing)",
    fontFamily: "var(--heading-4-font)",
    color: "var(--color-text)",
    margin: 0,
  },
};

export function Heading({ level, children, className, style, gradient }: HeadingProps) {
  const Tag = `h${level}` as const;
  const mergedStyle: CSSProperties = { ...headingStyles[level], ...style };

  return (
    <Tag className={className} style={mergedStyle}>
      {gradient ? <GradientText>{children}</GradientText> : children}
    </Tag>
  );
}

// ─── Body ───────────────────────────────────────────────────────────────────

interface BodyProps {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
  size?: "sm" | "base" | "lg";
}

const bodySizeMap: Record<string, string> = {
  sm: "var(--font-size-sm)",
  base: "var(--font-size-base)",
  lg: "var(--font-size-lg)",
};

export function Body({ children, className, style, size = "base" }: BodyProps) {
  const baseStyle: CSSProperties = {
    fontSize: bodySizeMap[size],
    lineHeight: 1.7,
    color: "var(--color-text)",
    maxWidth: "680px",
    margin: 0,
  };

  return (
    <p className={className} style={{ ...baseStyle, ...style }}>
      {children}
    </p>
  );
}

// ─── Caption ────────────────────────────────────────────────────────────────

interface CaptionProps {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
}

export function Caption({ children, className, style }: CaptionProps) {
  const baseStyle: CSSProperties = {
    fontSize: "var(--font-size-sm)",
    lineHeight: 1.5,
    color: "var(--color-text-secondary)",
    margin: 0,
  };

  return (
    <span className={className} style={{ ...baseStyle, ...style }}>
      {children}
    </span>
  );
}

// ─── Label ──────────────────────────────────────────────────────────────────

interface LabelProps {
  children: ReactNode;
  htmlFor?: string;
  className?: string;
  style?: CSSProperties;
  required?: boolean;
}

export function Label({ children, htmlFor, className, style, required }: LabelProps) {
  const baseStyle: CSSProperties = {
    fontSize: "var(--font-size-sm)",
    fontWeight: 500,
    color: "var(--color-text)",
    lineHeight: 1.5,
  };

  return (
    <label htmlFor={htmlFor} className={className} style={{ ...baseStyle, ...style }}>
      {children}
      {required && (
        <span aria-hidden="true" style={{ color: "var(--color-danger)", marginLeft: "0.25em" }}>
          *
        </span>
      )}
    </label>
  );
}

// ─── Code ───────────────────────────────────────────────────────────────────

interface CodeProps {
  children: ReactNode;
  inline?: boolean;
  className?: string;
  style?: CSSProperties;
}

const CODE_FONT_STACK = '"JetBrains Mono", "Fira Code", "Cascadia Code", monospace';

export function Code({ children, inline = true, className, style }: CodeProps) {
  const baseStyle: CSSProperties = {
    fontFamily: CODE_FONT_STACK,
    fontSize: "var(--font-size-sm)",
    background: "var(--glass-bg-subtle)",
    border: "1px solid var(--glass-border-light)",
    borderRadius: "var(--radius-sm)",
    color: "var(--color-text)",
  };

  if (inline) {
    return (
      <code
        className={className}
        style={{ ...baseStyle, padding: "0 var(--space-2)", ...style }}
      >
        {children}
      </code>
    );
  }

  return (
    <pre
      className={className}
      style={{
        ...baseStyle,
        padding: "var(--space-4)",
        overflow: "auto",
        margin: 0,
        ...style,
      }}
    >
      <code style={{ fontFamily: CODE_FONT_STACK }}>{children}</code>
    </pre>
  );
}
