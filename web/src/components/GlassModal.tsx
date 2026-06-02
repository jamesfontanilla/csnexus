import { useEffect, useId } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { scaleIn, springGentle, useReducedMotion } from "../design-system";
import { useFocusTrap } from "../hooks/useFocusTrap";

interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  titleId?: string;
  children: React.ReactNode;
  size?: "sm" | "md" | "lg";
}

export function GlassModal({ isOpen, onClose, title, titleId: titleIdProp, children, size = "md" }: GlassModalProps) {
  const generatedId = useId();
  const titleId = titleIdProp ?? `glass-modal-title-${generatedId}`;

  const containerRef = useFocusTrap(isOpen);
  const reducedMotion = useReducedMotion();

  const sizeStyles: Record<string, React.CSSProperties> = {
    sm: { maxWidth: "400px" },
    md: { maxWidth: "560px" },
    lg: { maxWidth: "720px" },
  };

  // Handle Escape key to close
  useEffect(() => {
    if (!isOpen) return;

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Animation variants
  const panelInitial = reducedMotion
    ? { opacity: 0 }
    : scaleIn.initial;

  const panelAnimate = reducedMotion
    ? { opacity: 1 }
    : scaleIn.animate;

  const panelExit = reducedMotion
    ? { opacity: 0 }
    : scaleIn.exit;

  const panelTransition = reducedMotion
    ? { duration: 0.15 }
    : springGentle;

  return (
    <AnimatePresence>
      {isOpen && (
        <div
          style={{
            position: "fixed",
            inset: 0,
            zIndex: "var(--z-modal)" as unknown as number,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "1rem",
          }}
        >
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            style={{
              position: "absolute",
              inset: 0,
              background: "rgba(10, 10, 10, 0.7)",
              backdropFilter: "blur(12px)",
              WebkitBackdropFilter: "blur(12px)",
            }}
          />

          {/* Modal Panel */}
          <motion.div
            ref={containerRef as React.RefObject<HTMLDivElement>}
            className="glass-lg"
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            tabIndex={-1}
            initial={panelInitial}
            animate={panelAnimate}
            exit={panelExit}
            transition={panelTransition}
            style={{
              position: "relative",
              width: "100%",
              padding: "2rem",
              ...sizeStyles[size],
            }}
          >
            <h2
              id={titleId}
              style={{
                margin: "0 0 1rem",
                fontSize: "var(--font-size-xl)",
                fontWeight: 600,
                color: "var(--color-text)",
              }}
            >
              {title}
            </h2>
            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
