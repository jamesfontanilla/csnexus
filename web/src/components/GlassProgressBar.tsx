import { useEffect, useRef, useState } from "react";

interface GlassProgressBarProps {
  value: number;
  max?: number;
  label?: string;
  animated?: boolean;
  height?: number;
  color?: string;
}

export function GlassProgressBar({
  value,
  max = 100,
  label,
  animated = false,
  height = 8,
  color,
}: GlassProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  const [displayPct, setDisplayPct] = useState(0);
  const prevPct = useRef(0);

  useEffect(() => {
    let rafId: number;

    const from = prevPct.current;
    const to = percentage;
    prevPct.current = percentage;

    if (from === to) {
      setDisplayPct(to);
      return;
    }

    const startTime = performance.now();
    const duration = 500;

    function tick(now: number) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      // Spring-like ease with overshoot
      const eased = t < 1
        ? 1 - Math.pow(1 - t, 3) * Math.cos(t * Math.PI * 0.5)
        : 1;
      setDisplayPct(from + (to - from) * eased);
      if (t < 1) rafId = requestAnimationFrame(tick);
    }

    rafId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafId);
  }, [percentage]);

  return (
    <div className="glass-progress" role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max} aria-label={label}>
      {label && (
        <span style={{ display: "block", marginBottom: "var(--space-1)", fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)" }}>
          {label}
        </span>
      )}
      <div
        style={{
          height: `${height}px`,
          borderRadius: "var(--radius-full)",
          background: "var(--glass-bg-subtle)",
          border: "1px solid var(--glass-border-light)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${displayPct}%`,
            height: "100%",
            borderRadius: "var(--radius-full)",
            background: color || "linear-gradient(90deg, var(--color-accent), var(--color-metallic))",
            boxShadow: "inset 0 1px 2px rgba(255, 255, 255, 0.2), 0 0 8px rgba(212, 165, 116, 0.2)",
            animation: animated ? "gentle-pulse 2s ease-in-out infinite" : "none",
          }}
        />
      </div>
    </div>
  );
}
