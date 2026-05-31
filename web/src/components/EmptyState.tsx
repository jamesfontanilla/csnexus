import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { GlassCard } from "./GlassCard";
import { GlassButton } from "./GlassButton";
import { scaleIn } from "../design-system";

interface EmptyStateProps {
  icon?: string;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

/**
 * Designed empty state with icon, message, and optional CTA.
 * Replaces plain text "No items found" patterns.
 */
export function EmptyState({
  icon = "📭",
  title,
  description,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <motion.div
      initial={scaleIn.initial}
      animate={scaleIn.animate}
      transition={scaleIn.transition}
    >
      <GlassCard
        blur="sm"
        style={{
          textAlign: "center",
          padding: "var(--space-12) var(--space-8)",
          maxWidth: "420px",
          margin: "0 auto",
        }}
      >
        <div
          style={{
            fontSize: "3rem",
            marginBottom: "var(--space-4)",
            filter: "grayscale(0.2)",
          }}
          aria-hidden="true"
        >
          {icon}
        </div>
        <h3
          style={{
            fontSize: "var(--font-size-lg)",
            fontWeight: 700,
            color: "var(--color-text)",
            marginBottom: "var(--space-2)",
          }}
        >
          {title}
        </h3>
        <p
          style={{
            fontSize: "var(--font-size-sm)",
            color: "var(--color-text-secondary)",
            lineHeight: 1.6,
            margin: 0,
            marginBottom: actionLabel ? "var(--space-6)" : 0,
          }}
        >
          {description}
        </p>
        {actionLabel && onAction && (
          <GlassButton variant="primary" size="md" onClick={onAction}>
            {actionLabel}
          </GlassButton>
        )}
      </GlassCard>
    </motion.div>
  );
}
