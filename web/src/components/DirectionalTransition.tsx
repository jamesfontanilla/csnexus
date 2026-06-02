import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "../design-system";

type Direction = "forward" | "back" | "fade";

interface DirectionalTransitionProps {
  children: ReactNode;
  direction?: Direction;
}

const variants = {
  forward: {
    initial: { opacity: 0, x: 24 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -16 },
  },
  back: {
    initial: { opacity: 0, x: -24 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: 16 },
  },
  fade: {
    initial: { opacity: 0, scale: 0.98 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.98 },
  },
};

/**
 * Directional page transition that varies animation based on navigation context.
 * - "forward": slides in from right (navigating deeper)
 * - "back": slides in from left (navigating up)
 * - "fade": crossfade (sibling/tab navigation)
 */
export function DirectionalTransition({
  children,
  direction = "forward",
}: DirectionalTransitionProps) {
  const reducedMotion = useReducedMotion();

  if (reducedMotion) {
    return <>{children}</>;
  }

  const v = variants[direction];

  return (
    <motion.div
      initial={v.initial}
      animate={v.animate}
      exit={v.exit}
      transition={{ type: "spring", stiffness: 300, damping: 28 }}
    >
      {children}
    </motion.div>
  );
}
