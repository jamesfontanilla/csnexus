import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface XPGainAnimationProps {
  /** Amount of XP gained. Animation triggers when this is > 0. */
  amount: number;
  /** Called after the animation fully completes (exit finished). */
  onComplete?: () => void;
}

/**
 * Animated XP gain overlay. Shows a "+N XP" badge that scales in with a
 * spring, holds for ~1.5s, then floats up and fades out. Uses framer-motion
 * and respects prefers-reduced-motion via framer's built-in support.
 *
 * Usage:
 *   <XPGainAnimation amount={xpGained} onComplete={() => setXpGained(0)} />
 */
export function XPGainAnimation({ amount, onComplete }: XPGainAnimationProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (amount > 0) {
      setVisible(true);
    }
  }, [amount]);

  // Auto-dismiss after the badge has been visible long enough
  useEffect(() => {
    if (!visible) return;
    const timer = setTimeout(() => setVisible(false), 1800);
    return () => clearTimeout(timer);
  }, [visible]);

  const handleExitComplete = useCallback(() => {
    onComplete?.();
  }, [onComplete]);

  return (
    <AnimatePresence onExitComplete={handleExitComplete}>
      {visible && (
        <motion.div
          key="xp-gain"
          initial={{ opacity: 0, scale: 0.5, y: 0 }}
          animate={{ opacity: 1, scale: 1, y: -8 }}
          exit={{ opacity: 0, scale: 0.8, y: -40 }}
          transition={{
            duration: 0.4,
            ease: [0.22, 1, 0.36, 1],
          }}
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            zIndex: 10000,
            pointerEvents: "none",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "0.5rem",
          }}
        >
          {/* Expanding glow ring */}
          <motion.div
            initial={{ scale: 0, opacity: 0.8 }}
            animate={{ scale: 2.5, opacity: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            style={{
              position: "absolute",
              width: "80px",
              height: "80px",
              borderRadius: "50%",
              background: "radial-gradient(circle, rgba(212, 165, 116, 0.4) 0%, transparent 70%)",
            }}
          />

          {/* XP badge */}
          <motion.div
            initial={{ scale: 0.5, rotate: -10 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{
              type: "spring",
              stiffness: 400,
              damping: 12,
              delay: 0.05,
            }}
            style={{
              background: "linear-gradient(135deg, rgba(212, 165, 116, 0.25), rgba(212, 165, 116, 0.1))",
              backdropFilter: "blur(20px)",
              WebkitBackdropFilter: "blur(20px)",
              border: "1px solid rgba(212, 165, 116, 0.4)",
              borderRadius: "16px",
              padding: "1rem 1.75rem",
              boxShadow: "0 8px 32px rgba(212, 165, 116, 0.3), 0 0 60px rgba(212, 165, 116, 0.1)",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <motion.span
                initial={{ rotate: -30, scale: 0 }}
                animate={{ rotate: 0, scale: 1 }}
                transition={{ type: "spring", stiffness: 500, damping: 15, delay: 0.15 }}
                style={{ fontSize: "1.5rem" }}
                aria-hidden="true"
              >
                ⚡
              </motion.span>
              <span
                role="status"
                aria-live="polite"
                style={{
                  fontSize: "1.5rem",
                  fontWeight: 800,
                  background: "linear-gradient(135deg, #d4a574, #f0d9b5)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                }}
              >
                +{amount} XP
              </span>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
