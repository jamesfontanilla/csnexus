import type { ReactNode, CSSProperties } from "react";

interface GradientTextProps {
  children: ReactNode;
  variant?: "accent" | "success" | "danger" | "info";
  as?: "span" | "p" | "h1" | "h2" | "h3";
  style?: CSSProperties;
  className?: string;
}

const GRADIENTS: Record<string, string> = {
  accent: "linear-gradient(135deg, #D4A574, #f0d9b5)",
  success: "linear-gradient(135deg, #8fbc8f, #b8d4b8)",
  danger: "linear-gradient(135deg, #d4645c, #e8a090)",
  info: "linear-gradient(135deg, #7eb8c9, #a8d4e0)",
};

/**
 * Text with a gradient fill. Use sparingly on key metrics, scores, and headings
 * to create visual focal points.
 */
export function GradientText({
  children,
  variant = "accent",
  as: Tag = "span",
  style,
  className,
}: GradientTextProps) {
  return (
    <Tag
      className={className}
      style={{
        background: GRADIENTS[variant],
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
        backgroundClip: "text",
        ...style,
      }}
    >
      {children}
    </Tag>
  );
}
