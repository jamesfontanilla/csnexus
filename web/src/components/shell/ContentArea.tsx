import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { usePageContext } from "../../context/PageContextRegistry";
import { useReducedMotion } from "../../design-system";
import type { ReactNode } from "react";

interface ContentAreaProps {
  children: ReactNode;
}

const PAGE_TRANSITION_DURATION = 0.25; // 250ms matches --duration-page intent for shell transitions
const PAGE_TRANSITION_DURATION_REDUCED = 0.08; // 80ms = --duration-instant for prefers-reduced-motion
const PAGE_TRANSITION_EASING = [0, 0, 0.2, 1]; // --ease-decelerate

/**
 * Scrollable content region inside the shell main area.
 * Applies layout-mode-specific styling (standard, centered, split),
 * resets scroll on route change, and wraps content with Framer Motion
 * page transitions (fade + 12px upward translate).
 */
export function ContentArea({ children }: ContentAreaProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const { pathname } = useLocation();
  const { layoutMode, centeredMaxWidth } = usePageContext();
  const reducedMotion = useReducedMotion();

  // Reset scroll to top on route change
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = 0;
    }
  }, [pathname]);

  const contentClassName = getContentClassName(layoutMode);
  const contentStyle =
    layoutMode === "centered" && centeredMaxWidth
      ? { maxWidth: `${centeredMaxWidth}px` }
      : undefined;

  const duration = reducedMotion ? PAGE_TRANSITION_DURATION_REDUCED : PAGE_TRANSITION_DURATION;
  const yOffset = reducedMotion ? 0 : 12;

  return (
    <div ref={scrollRef} className="content-area">
      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={pathname}
          className={contentClassName}
          style={contentStyle}
          initial={{ opacity: 0, y: yOffset }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: reducedMotion ? 0 : -12 }}
          transition={{
            duration,
            ease: PAGE_TRANSITION_EASING,
          }}
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

function getContentClassName(layoutMode: string): string {
  const base = "content-area__content";
  switch (layoutMode) {
    case "centered":
      return `${base} ${base}--centered`;
    case "split":
      return `${base} ${base}--split`;
    default:
      return `${base} ${base}--standard`;
  }
}

export { type ContentAreaProps };
