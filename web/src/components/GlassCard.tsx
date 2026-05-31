import type { ReactNode, CSSProperties, KeyboardEvent } from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "../design-system";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  blur?: "sm" | "md" | "lg";
  hoverable?: boolean;
  lifted?: boolean;
  onClick?: () => void;
  style?: CSSProperties;
  as?: "div" | "section" | "article";
}

export function GlassCard({
  children,
  className = "",
  blur = "md",
  hoverable = false,
  lifted = false,
  onClick,
  style,
  as = "div",
}: GlassCardProps) {
  const reducedMotion = useReducedMotion();
  const Component = motion[as];

  const hoverAnimation =
    hoverable && !reducedMotion
      ? { scale: 1.01, y: -2, boxShadow: "var(--shadow-lifted)" }
      : {};

  const tapAnimation =
    hoverable && !reducedMotion ? { scale: 0.99 } : {};

  return (
    <Component
      className={`glass-${blur} glass-card ${className}`}
      style={{
        position: "relative",
        padding: "var(--space-6)",
        willChange: hoverable ? "transform" : undefined,
        transform: lifted ? "translateY(-2px)" : undefined,
        boxShadow: lifted ? "var(--shadow-lifted)" : undefined,
        ...style,
      }}
      whileHover={hoverAnimation}
      whileTap={onClick ? tapAnimation : undefined}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e: KeyboardEvent) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      {children}
    </Component>
  );
}
