import type { ReactNode } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useReducedMotion } from "../design-system";

interface CrossfadeContentProps {
  /** Unique key that changes when content swaps (e.g., "loading" vs "loaded") */
  contentKey: string;
  children: React.ReactNode;
}

/**
 * Crossfade wrapper for smooth transitions between loading/content states.
 * Prevents the hard-swap from skeleton to real content.
 */
export function CrossfadeContent({ contentKey, children }: CrossfadeContentProps) {
  const reducedMotion = useReducedMotion();

  if (reducedMotion) {
    return <>{children}</>;
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={contentKey}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -4 }}
        transition={{ duration: 0.2, ease: "easeOut" }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
