import { useState, useRef, useEffect } from "react";

interface GlassSelectOption {
  value: string;
  label: string;
}

interface GlassSelectProps {
  value: string;
  onChange: (value: string) => void;
  options: GlassSelectOption[];
  style?: React.CSSProperties;
  "aria-label"?: string;
  disabled?: boolean;
}

/**
 * Custom select dropdown styled with the glass design system.
 * Replaces native <select> to avoid browser-default light dropdown popups.
 */
export function GlassSelect({ value, onChange, options, style, "aria-label": ariaLabel, disabled = false }: GlassSelectProps) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const selectedLabel = options.find((o) => o.value === value)?.label ?? value;

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={containerRef} style={{ position: "relative", ...style }}>
      <button
        type="button"
        onClick={() => {
          if (!disabled) setOpen((prev) => !prev);
        }}
        aria-label={ariaLabel}
        aria-expanded={open}
        aria-haspopup="listbox"
        disabled={disabled}
        style={{
          width: "100%",
          padding: "0.5rem 2rem 0.5rem 0.75rem",
          background: "var(--glass-bg-subtle)",
          border: "1px solid var(--glass-border-medium)",
          borderRadius: "var(--radius-sm)",
          color: "var(--color-text)",
          fontSize: "var(--font-size-sm)",
          fontFamily: "inherit",
          textAlign: "left",
          cursor: disabled ? "not-allowed" : "pointer",
          opacity: disabled ? 0.7 : 1,
          outline: "none",
          position: "relative",
          transition: "border-color 150ms ease",
        }}
      >
        {selectedLabel}
        <span
          aria-hidden="true"
          style={{
            position: "absolute",
            right: "0.75rem",
            top: "50%",
            transform: "translateY(-50%)",
            fontSize: "0.6rem",
            color: "var(--color-text-muted)",
            pointerEvents: "none",
          }}
        >
          ▼
        </span>
      </button>

      {open && !disabled && (
        <ul
          role="listbox"
          style={{
            position: "absolute",
            top: "calc(100% + 4px)",
            left: 0,
            right: 0,
            margin: 0,
            padding: "var(--space-1) 0",
            listStyle: "none",
            background: "var(--glass-bg-strong, #1e1e32)",
            border: "1px solid var(--glass-border-medium)",
            borderRadius: "var(--radius-sm)",
            boxShadow: "0 8px 24px rgba(0,0,0,0.5)",
            zIndex: 100,
            maxHeight: 200,
            overflowY: "auto",
          }}
        >
          {options.map((opt) => (
            <li
              key={opt.value}
              role="option"
              aria-selected={opt.value === value}
              onClick={() => {
                onChange(opt.value);
                setOpen(false);
              }}
              style={{
                padding: "0.5rem 0.75rem",
                fontSize: "var(--font-size-sm)",
                color: opt.value === value ? "var(--color-accent)" : "var(--color-text)",
                background: opt.value === value ? "rgba(212, 165, 116, 0.08)" : "transparent",
                cursor: "pointer",
                transition: "background 100ms ease",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.background = "rgba(255,255,255,0.05)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.background =
                  opt.value === value ? "rgba(212, 165, 116, 0.08)" : "transparent";
              }}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
