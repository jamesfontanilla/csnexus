import { useId, useState, useEffect } from "react";
import { useReducedMotion } from "../design-system/motion";

interface ProgressRingProps {
  size: number;
  value: number;
  strokeWidth?: number;
  label?: string;
  children?: React.ReactNode;
}

export function ProgressRing({
  size,
  value,
  strokeWidth: strokeWidthProp = 8,
  label,
  children,
}: ProgressRingProps) {
  const id = useId();
  const reducedMotion = useReducedMotion();

  // Edge case: size ≤ 0 → return null
  if (size <= 0) return null;

  // Clamp strokeWidth: if > size/2, clamp to size/4
  const strokeWidth = strokeWidthProp > size / 2 ? size / 4 : strokeWidthProp;

  // Clamp value: NaN/undefined → 0, then clamp to [0, 100]
  const clamped = Math.min(100, Math.max(0, isNaN(value) ? 0 : value ?? 0));

  const center = size / 2;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const targetOffset = circumference * (1 - clamped / 100);

  // Mount animation: start at full circumference (0%), transition to target
  const [offset, setOffset] = useState(
    reducedMotion ? targetOffset : circumference
  );

  useEffect(() => {
    if (reducedMotion) {
      setOffset(targetOffset);
      return;
    }
    // Use requestAnimationFrame to ensure the initial render with full offset
    // is painted before transitioning to the target
    const rafId = requestAnimationFrame(() => {
      setOffset(targetOffset);
    });
    return () => cancelAnimationFrame(rafId);
  }, [targetOffset, reducedMotion, circumference]);

  const gradientId = `ring-gradient-${id}`;
  const filterId = `ring-glow-${id}`;

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role="progressbar"
      aria-valuenow={clamped}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={label}
    >
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="var(--color-accent)" />
          <stop offset="100%" stopColor="var(--color-metallic)" />
        </linearGradient>
        <filter id={filterId}>
          <feDropShadow
            dx="0"
            dy="0"
            stdDeviation="3"
            floodColor="var(--color-accent)"
            floodOpacity="0.6"
          />
        </filter>
      </defs>

      {/* Track circle */}
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke="var(--glass-bg-medium)"
        strokeWidth={strokeWidth}
      />

      {/* Progress circle */}
      <circle
        cx={center}
        cy={center}
        r={radius}
        fill="none"
        stroke={`url(#${gradientId})`}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        filter={clamped > 0 ? `url(#${filterId})` : undefined}
        transform={`rotate(-90 ${center} ${center})`}
        style={{
          transition: reducedMotion
            ? "none"
            : "stroke-dashoffset var(--duration-slow) var(--ease-decelerate)",
        }}
      />

      {/* Center content */}
      {(children || label) && (
        <foreignObject x="0" y="0" width={size} height={size}>
          <div
            style={{
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "var(--font-size-sm)",
              color: "var(--color-text)",
              textAlign: "center",
              padding: `${strokeWidth}px`,
            }}
          >
            {children || label}
          </div>
        </foreignObject>
      )}
    </svg>
  );
}
