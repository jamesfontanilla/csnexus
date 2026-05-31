import { createContext, useCallback, useContext, useState } from "react";

type ToastType = "success" | "error" | "info";

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

interface ToastContextValue {
  success: (message: string) => void;
  error: (message: string) => void;
  info: (message: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

let nextId = 0;

const TOAST_COLORS: Record<ToastType, { bg: string; border: string; text: string; icon: string }> = {
  success: {
    bg: "rgba(143, 188, 143, 0.15)",
    border: "rgba(143, 188, 143, 0.3)",
    text: "var(--color-success)",
    icon: "✓",
  },
  error: {
    bg: "rgba(212, 100, 92, 0.15)",
    border: "rgba(212, 100, 92, 0.3)",
    text: "var(--color-danger)",
    icon: "✕",
  },
  info: {
    bg: "rgba(212, 165, 116, 0.15)",
    border: "rgba(212, 165, 116, 0.3)",
    text: "var(--color-accent)",
    icon: "ℹ",
  },
};

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((message: string, type: ToastType) => {
    const id = nextId++;
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  const success = useCallback((msg: string) => addToast(msg, "success"), [addToast]);
  const error = useCallback((msg: string) => addToast(msg, "error"), [addToast]);
  const info = useCallback((msg: string) => addToast(msg, "info"), [addToast]);

  return (
    <ToastContext.Provider value={{ success, error, info }}>
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
          gap: "var(--space-2)",
          zIndex: "var(--z-toast)",
          pointerEvents: "none",
          maxWidth: "360px",
          width: "calc(100vw - 2rem)",
        }}
      >
        {toasts.map((toast) => {
          const colors = TOAST_COLORS[toast.type];
          return (
            <div
              key={toast.id}
              role="alert"
              className="toast"
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
                alignItems: "center",
                gap: "var(--space-2)",
              }}
            >
              <span aria-hidden="true" style={{ fontSize: "0.875rem", fontWeight: 700, flexShrink: 0 }}>
                {colors.icon}
              </span>
              {toast.message}
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return ctx;
}
