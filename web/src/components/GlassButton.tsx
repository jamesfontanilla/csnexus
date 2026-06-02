import { useRef } from "react";
import { motion } from "framer-motion";
import { springDefault, useReducedMotion } from "../design-system";

interface GlassButtonProps {
  children?: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg" | "xl";
  disabled?: boolean;
  loading?: boolean;
  iconLeft?: React.ReactNode;
  iconRight?: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  type?: "button" | "submit" | "reset";
  className?: string;
  style?: React.CSSProperties;
  "aria-label"?: string;
}

const sizeStyles: Record<string, React.CSSProperties> = {
  sm: {
    padding: "var(--space-2) var(--space-3)",
    fontSize: "var(--font-size-sm)",
    minHeight: "32px",
  },
  md: {
    padding: "var(--space-3) var(--space-5)",
    fontSize: "var(--font-size-base)",
    minHeight: "40px",
  },
  lg: {
    padding: "var(--space-4) var(--space-7)",
    fontSize: "var(--font-size-lg)",
    minHeight: "48px",
  },
  xl: {
    padding: "var(--space-5) var(--space-10)",
    fontSize: "var(--font-size-xl)",
    minHeight: "56px",
  },
};

export function GlassButton({
  children,
  variant = "primary",
  size = "md",
  disabled = false,
  loading = false,
  iconLeft,
  iconRight,
  onClick,
  type = "button",
  className = "",
  style,
  ...rest
}: GlassButtonProps) {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const reducedMotion = useReducedMotion();

  function handlePointerDown(e: React.PointerEvent<HTMLButtonElement>) {
    if (disabled || loading || reducedMotion) return;
    const btn = buttonRef.current;
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const ripple = document.createElement("span");
    ripple.className = "btn-ripple";
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    btn.appendChild(ripple);
    ripple.addEventListener("animationend", () => ripple.remove(), { once: true });
  }

  const isDisabledOrLoading = disabled || loading;

  return (
    <motion.button
      ref={buttonRef}
      className={`btn-glass btn-glass-${variant} ${className}`}
      style={{
        ...sizeStyles[size],
        position: "relative",
        overflow: "hidden",
        cursor: isDisabledOrLoading ? "not-allowed" : undefined,
        ...style,
      }}
      onClick={onClick}
      type={type}
      disabled={disabled || loading}
      aria-busy={loading ? true : undefined}
      whileHover={!isDisabledOrLoading && !reducedMotion ? { scale: 1.02 } : undefined}
      whileTap={!isDisabledOrLoading && !reducedMotion ? { scale: 0.97 } : undefined}
      transition={springDefault}
      onPointerDown={handlePointerDown}
      {...rest}
    >
      {loading ? (
        <span
          className="btn-spinner"
          aria-hidden="true"
          style={{
            display: "inline-block",
            width: "1em",
            height: "1em",
            border: "2px solid currentColor",
            borderTopColor: "transparent",
            borderRadius: "50%",
            animation: "spin 0.6s linear infinite",
          }}
        />
      ) : (
        <>
          {iconLeft && (
            <span
              className="btn-icon btn-icon-left"
              aria-hidden="true"
              style={{ display: "inline-flex", marginRight: "0.5em" }}
            >
              {iconLeft}
            </span>
          )}
          {children}
          {iconRight && (
            <span
              className="btn-icon btn-icon-right"
              aria-hidden="true"
              style={{ display: "inline-flex", marginLeft: "0.5em" }}
            >
              {iconRight}
            </span>
          )}
        </>
      )}
    </motion.button>
  );
}
