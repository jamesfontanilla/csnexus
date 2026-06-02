import { useState, useEffect } from "react";

// --- Spring Presets ---
export const springDefault = { type: "spring" as const, stiffness: 300, damping: 20 };
export const springGentle = { type: "spring" as const, stiffness: 200, damping: 25 };
export const springBouncy = { type: "spring" as const, stiffness: 400, damping: 15 };

// --- Animation Variants ---
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: { duration: 0.3 },
};

export const slideUp = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: springDefault,
};

export const slideDown = {
  initial: { opacity: 0, y: -12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 12 },
  transition: springDefault,
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 },
  transition: springGentle,
};

export const staggerContainer = {
  animate: { transition: { staggerChildren: 0.06 } },
};

export const staggerItem = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  transition: springDefault,
};

// --- Hooks ---
export function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mediaQuery.matches);

    function handleChange(event: MediaQueryListEvent) {
      setReducedMotion(event.matches);
    }

    mediaQuery.addEventListener("change", handleChange);
    return () => mediaQuery.removeEventListener("change", handleChange);
  }, []);

  return reducedMotion;
}

export function useMotionVariants(variants: Record<string, unknown>): Record<string, unknown> {
  const reducedMotion = useReducedMotion();

  if (reducedMotion) {
    return {
      ...variants,
      transition: { duration: 0 },
    };
  }

  return variants;
}

// --- New Page Transition ---
export const pageTransition = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: { duration: 0.5, ease: [0, 0, 0.2, 1] },
};

// --- Card Entrance Stagger ---
export const cardStaggerContainer = {
  animate: { transition: { staggerChildren: 0.05 } },
};

export const cardStaggerItem = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  transition: springDefault,
};

// --- Hover Lift ---
export const hoverLift = {
  whileHover: { y: -2, boxShadow: "var(--shadow-lifted)" },
  transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] },
};

// --- Press Feedback ---
export const pressFeedback = {
  whileTap: { scale: 0.97 },
  whileHover: { scale: 1.02 },
  transition: springDefault,
};

// --- Toast Slide In ---
export const toastSlideIn = {
  initial: { opacity: 0, x: "110%" },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: "110%" },
  transition: { duration: 0.15, ease: [0, 0, 0.2, 1] },
};

// --- Reduced-motion variant factory ---
export function makeReducedVariants<T extends Record<string, unknown>>(
  variants: T,
  reducedMotion: boolean
): T {
  if (!reducedMotion) return variants;
  const stripped: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(variants)) {
    if (key === "transition") {
      stripped[key] = { duration: 0.08 };
    } else if (typeof value === "object" && value !== null) {
      const v = value as Record<string, unknown>;
      const { x: _x, y: _y, scale: _s, rotate: _r, ...rest } = v;
      stripped[key] = rest;
    } else {
      stripped[key] = value;
    }
  }
  return stripped as T;
}
