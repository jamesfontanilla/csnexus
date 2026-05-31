import type { CSSProperties } from "react";
import { useEffect, useRef, useState } from "react";
import { useReducedMotion } from "../design-system";

interface AnimatedNumberProps {
  value: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  style?: CSSProperties;
  className?: string;
}

/**
 * Animated number counter that smoothly ticks up/down to the target value.
 * Uses requestAnimationFrame for smooth 60fps animation with an ease-out curve.
 * Respects prefers-reduced-motion via the useReducedMotion hook.
 */
export function AnimatedNumber({
  value,
  duration = 800,
  prefix = "",
  suffix = "",
  style,
  className,
}: AnimatedNumberProps) {
  const reducedMotion = useReducedMotion();
  const [display, setDisplay] = useState(value);
  const prevValue = useRef(value);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    const from = prevValue.current;
    const to = value;
    prevValue.current = value;

    if (from === to || reducedMotion) {
      setDisplay(to);
      return;
    }

    const startTime = performance.now();
    const diff = to - from;

    function tick(now: number) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(from + diff * eased);
      setDisplay(current);

      if (progress < 1) {
        rafRef.current = requestAnimationFrame(tick);
      }
    }

    rafRef.current = requestAnimationFrame(tick);

    return () => {
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [value, duration, reducedMotion]);

  return (
    <span
      className={className}
      style={{ fontVariantNumeric: "tabular-nums", ...style }}
      aria-live="polite"
      aria-atomic="true"
    >
      {prefix}{display}{suffix}
    </span>
  );
}
