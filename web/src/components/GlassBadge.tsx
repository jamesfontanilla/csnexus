import { useReducedMotion } from "../design-system/motion";

interface GlassBadgeProps {
  label: string;
  color?: "primary" | "success" | "warning" | "danger" | "info" | "accent";
  size?: "sm" | "md";
  dot?: boolean;
  pulse?: boolean;
}

const colorMap: Record<string, { bg: string; border: string; text: string }> = {
  primary: {
    bg: "rgba(62, 39, 35, 0.2)",
    border: "rgba(62, 39, 35, 0.3)",
    text: "var(--color-highlight)",
  },
  success: {
    bg: "rgba(129, 199, 132, 0.15)",
    border: "rgba(129, 199, 132, 0.3)",
    text: "var(--color-success)",
  },
  warning: {
    bg: "rgba(255, 183, 77, 0.15)",
    border: "rgba(255, 183, 77, 0.3)",
    text: "var(--color-warning)",
  },
  danger: {
    bg: "rgba(229, 115, 115, 0.15)",
    border: "rgba(229, 115, 115, 0.3)",
    text: "var(--color-danger)",
  },
  info: {
    bg: "rgba(126, 184, 201, 0.15)",
    border: "rgba(126, 184, 201, 0.3)",
    text: "var(--color-info)",
  },
  accent: {
    bg: "rgba(212, 165, 116, 0.15)",
    border: "rgba(212, 165, 116, 0.3)",
    text: "var(--color-accent)",
  },
};

export function GlassBadge({
  label,
  color = "primary",
  size = "sm",
  dot,
  pulse,
}: GlassBadgeProps) {
  const reducedMotion = useReducedMotion();
  const colors = colorMap[color];
  const sizeStyles = size === "sm"
    ? { padding: "0.125rem 0.5rem", fontSize: "var(--font-size-xs)" }
    : { padding: "0.25rem 0.75rem", fontSize: "var(--font-size-sm)" };

  const showPulse = pulse && !reducedMotion;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: dot ? "0.375rem" : undefined,
        borderRadius: "var(--radius-full)",
        background: colors.bg,
        border: `1px solid ${colors.border}`,
        color: colors.text,
        fontWeight: 500,
        backdropFilter: "blur(8px)",
        WebkitBackdropFilter: "blur(8px)",
        ...sizeStyles,
      }}
    >
      {dot && (
        <span
          className={showPulse ? "badge-dot-pulse" : undefined}
          style={{
            width: "8px",
            height: "8px",
            borderRadius: "50%",
            background: "currentColor",
            flexShrink: 0,
          }}
        />
      )}
      {label}
    </span>
  );
}
