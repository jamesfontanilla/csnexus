import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
  useRef,
  useState,
} from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toastSlideIn, useReducedMotion } from "../design-system/motion";

// --- Types ---

export type ToastVariant = "success" | "error" | "warning" | "info";

interface ToastItem {
  id: number;
  message: string;
  variant: ToastVariant;
  duration: number;
  paused: boolean;
  createdAt: number;
}

interface ToastContextValue {
  success: (message: string, duration?: number) => void;
  error: (message: string, duration?: number) => void;
  warning: (message: string, duration?: number) => void;
  info: (message: string, duration?: number) => void;
}

// --- Reducer ---

type ToastAction =
  | { type: "ADD"; toast: ToastItem }
  | { type: "REMOVE"; id: number }
  | { type: "PAUSE"; id: number }
  | { type: "RESUME"; id: number };

const MAX_TOASTS = 5;

function toastReducer(state: ToastItem[], action: ToastAction): ToastItem[] {
  switch (action.type) {
    case "ADD": {
      const next = [...state, action.toast];
      // Enforce max 5 concurrent toasts: remove oldest first
      if (next.length > MAX_TOASTS) {
        return next.slice(next.length - MAX_TOASTS);
      }
      return next;
    }
    case "REMOVE":
      return state.filter((t) => t.id !== action.id);
    case "PAUSE":
      return state.map((t) =>
        t.id === action.id ? { ...t, paused: true } : t
      );
    case "RESUME":
      return state.map((t) =>
        t.id === action.id ? { ...t, paused: false } : t
      );
    default:
      return state;
  }
}

// --- Context ---

const ToastContext = createContext<ToastContextValue | null>(null);

let nextId = 0;

const DEFAULT_DURATION = 4000;

function clampDuration(duration: number | undefined): number {
  if (duration === undefined || duration <= 0) return DEFAULT_DURATION;
  return duration;
}

// --- Toast Colors ---

const TOAST_COLORS: Record<
  ToastVariant,
  { bg: string; border: string; text: string; icon: string; progressColor: string }
> = {
  success: {
    bg: "rgba(143, 188, 143, 0.15)",
    border: "rgba(143, 188, 143, 0.3)",
    text: "var(--color-success)",
    icon: "✓",
    progressColor: "var(--color-success)",
  },
  error: {
    bg: "rgba(212, 100, 92, 0.15)",
    border: "rgba(212, 100, 92, 0.3)",
    text: "var(--color-danger)",
    icon: "✕",
    progressColor: "var(--color-danger)",
  },
  warning: {
    bg: "rgba(212, 165, 116, 0.15)",
    border: "rgba(212, 165, 116, 0.3)",
    text: "var(--color-warning, #e6a817)",
    icon: "⚠",
    progressColor: "var(--color-warning, #e6a817)",
  },
  info: {
    bg: "rgba(212, 165, 116, 0.15)",
    border: "rgba(212, 165, 116, 0.3)",
    text: "var(--color-accent)",
    icon: "ℹ",
    progressColor: "var(--color-accent)",
  },
};

// --- Individual Toast Component ---

function ToastItemComponent({
  toast,
  onPause,
  onResume,
  onRemove,
}: {
  toast: ToastItem;
  onPause: (id: number) => void;
  onResume: (id: number) => void;
  onRemove: (id: number) => void;
}) {
  const reducedMotion = useReducedMotion();
  const [remaining, setRemaining] = useState(toast.duration);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (toast.paused) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      return;
    }

    intervalRef.current = setInterval(() => {
      setRemaining((prev) => {
        const next = prev - 50;
        if (next <= 0) {
          return 0;
        }
        return next;
      });
    }, 50);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [toast.paused]);

  useEffect(() => {
    if (remaining <= 0) {
      onRemove(toast.id);
    }
  }, [remaining, toast.id, onRemove]);

  const colors = TOAST_COLORS[toast.variant];
  const progressWidth = (remaining / toast.duration) * 100;

  // ARIA: role="alert" for error, role="status" for all others
  const role = toast.variant === "error" ? "alert" : "status";

  // Animation variants: opacity-only when reducedMotion
  const variants = reducedMotion
    ? {
        initial: { opacity: 0 },
        animate: { opacity: 1 },
        exit: { opacity: 0 },
        transition: { duration: 0.08 },
      }
    : toastSlideIn;

  return (
    <motion.div
      layout
      initial={variants.initial}
      animate={variants.animate}
      exit={variants.exit}
      transition={variants.transition}
      role={role}
      onMouseEnter={() => onPause(toast.id)}
      onMouseLeave={() => onResume(toast.id)}
      style={{
        padding: "var(--space-3) var(--space-5)",
        background: colors.bg,
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        border: `1px solid ${colors.border}`,
        borderRadius: "var(--radius-md)",
        boxShadow: "var(--shadow-depth)",
        color: colors.text,
        fontSize: "var(--font-size-sm)",
        fontWeight: 500,
        pointerEvents: "auto",
        display: "flex",
        flexDirection: "column",
        gap: "var(--space-1, 4px)",
        overflow: "hidden",
        position: "relative",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
        <span
          aria-hidden="true"
          style={{ fontSize: "0.875rem", fontWeight: 700, flexShrink: 0 }}
        >
          {colors.icon}
        </span>
        {toast.message}
      </div>
      {/* Progress bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "3px",
          background: "rgba(255, 255, 255, 0.1)",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressWidth}%`,
            background: colors.progressColor,
            transition: "width 50ms linear",
          }}
        />
      </div>
    </motion.div>
  );
}

// --- Provider ---

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, dispatch] = useReducer(toastReducer, []);

  const addToast = useCallback((message: string, variant: ToastVariant, duration?: number) => {
    const id = nextId++;
    const clampedDuration = clampDuration(duration);
    dispatch({
      type: "ADD",
      toast: {
        id,
        message,
        variant,
        duration: clampedDuration,
        paused: false,
        createdAt: Date.now(),
      },
    });
  }, []);

  const handleRemove = useCallback((id: number) => {
    dispatch({ type: "REMOVE", id });
  }, []);

  const handlePause = useCallback((id: number) => {
    dispatch({ type: "PAUSE", id });
  }, []);

  const handleResume = useCallback((id: number) => {
    dispatch({ type: "RESUME", id });
  }, []);

  const success = useCallback(
    (msg: string, duration?: number) => addToast(msg, "success", duration),
    [addToast]
  );
  const error = useCallback(
    (msg: string, duration?: number) => addToast(msg, "error", duration),
    [addToast]
  );
  const warning = useCallback(
    (msg: string, duration?: number) => addToast(msg, "warning", duration),
    [addToast]
  );
  const info = useCallback(
    (msg: string, duration?: number) => addToast(msg, "info", duration),
    [addToast]
  );

  return (
    <ToastContext.Provider value={{ success, error, warning, info }}>
      {children}
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: "fixed",
          top: "var(--space-4)",
          right: "var(--space-4)",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-3)",
          zIndex: "var(--z-toast)",
          pointerEvents: "none",
          maxWidth: "360px",
          width: "calc(100vw - 2rem)",
        }}
      >
        <AnimatePresence mode="popLayout">
          {toasts.map((toast) => (
            <ToastItemComponent
              key={toast.id}
              toast={toast}
              onPause={handlePause}
              onResume={handleResume}
              onRemove={handleRemove}
            />
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

// --- Hook ---

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error(
      "useToast must be used within a ToastProvider. " +
        "Wrap your component tree with <ToastProvider> before calling useToast()."
    );
  }
  return ctx;
}
