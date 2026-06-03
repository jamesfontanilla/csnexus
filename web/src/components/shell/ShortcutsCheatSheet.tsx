import { useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useShell } from "../../context/ShellContext";
import { useFocusTrap } from "../../hooks/useFocusTrap";
import { useReducedMotion } from "../../design-system";

/**
 * Keyboard shortcuts grouped by category for display in the cheat sheet.
 */
interface ShortcutEntry {
  keys: string;
  description: string;
}

interface ShortcutCategory {
  label: string;
  shortcuts: ShortcutEntry[];
}

const SHORTCUT_CATEGORIES: ShortcutCategory[] = [
  {
    label: "Navigation",
    shortcuts: [
      { keys: "Ctrl+K", description: "Command Palette" },
      { keys: "?", description: "This help" },
    ],
  },
  {
    label: "Panels",
    shortcuts: [
      { keys: "Ctrl+B", description: "Toggle Sidebar" },
      { keys: "Ctrl+\\", description: "Toggle Detail Panel" },
    ],
  },
  {
    label: "Actions",
    shortcuts: [
      { keys: "Ctrl+Shift+F", description: "Toggle Focus Mode" },
      { keys: "Escape", description: "Close overlay/panel" },
    ],
  },
];

/**
 * Detect macOS to show ⌘ instead of Ctrl.
 */
function isMac(): boolean {
  return typeof navigator !== "undefined" &&
    /Mac|iPod|iPhone|iPad/.test(navigator.platform);
}

/**
 * Format key combo for display, replacing Ctrl with ⌘ on macOS.
 */
function formatKeys(keys: string): string {
  if (isMac()) {
    return keys.replace(/Ctrl\+/g, "⌘");
  }
  return keys;
}

/**
 * ShortcutsCheatSheet — a keyboard-navigable overlay that displays all
 * available keyboard shortcuts grouped by category.
 *
 * - Activated by pressing `?` (via KeyboardShortcutManager calling actions.openShortcutsOverlay())
 * - Reads `state.shortcutsOverlayOpen` from useShell() — renders nothing when false
 * - Close on Escape key or close button (calls actions.closeShortcutsOverlay())
 * - Focus-trapped for accessibility (Requirement 13.6)
 * - Glass-morphism backdrop styling consistent with CommandPalette
 *
 * Requirements: 7.4, 7.5, 13.6
 */
export function ShortcutsCheatSheet() {
  const { state, actions } = useShell();
  const { shortcutsOverlayOpen } = state;
  const reducedMotion = useReducedMotion();

  // Focus trapping — cycles Tab/Shift+Tab within the overlay
  const containerRef = useFocusTrap(shortcutsOverlayOpen);

  // Close on Escape
  useEffect(() => {
    if (!shortcutsOverlayOpen) return;

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        actions.closeShortcutsOverlay();
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [shortcutsOverlayOpen, actions]);

  // Close on backdrop click
  const handleBackdropClick = useCallback(() => {
    actions.closeShortcutsOverlay();
  }, [actions]);

  // Prevent clicks inside the modal from propagating to backdrop
  const handleModalClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
  }, []);

  // Animation configuration
  const backdropTransition = reducedMotion
    ? { duration: 0.08 }
    : { duration: 0.2 };

  const panelInitial = reducedMotion
    ? { opacity: 0 }
    : { opacity: 0, scale: 0.96, y: -8 };
  const panelAnimate = reducedMotion
    ? { opacity: 1 }
    : { opacity: 1, scale: 1, y: 0 };
  const panelExit = reducedMotion
    ? { opacity: 0 }
    : { opacity: 0, scale: 0.96, y: -8 };
  const panelTransition = reducedMotion
    ? { duration: 0.08 }
    : { type: "spring" as const, stiffness: 300, damping: 25, mass: 0.8 };

  return (
    <AnimatePresence>
      {shortcutsOverlayOpen && (
        <div
          className="shortcuts-overlay"
          style={{
            position: "fixed",
            inset: 0,
            zIndex: "var(--z-modal)" as unknown as number,
            display: "flex",
            justifyContent: "center",
            alignItems: "flex-start",
            paddingTop: "15vh",
          }}
        >
          {/* Backdrop */}
          <motion.div
            className="shortcuts-overlay__backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={backdropTransition}
            onClick={handleBackdropClick}
            style={{
              position: "absolute",
              inset: 0,
              background: "rgba(10, 10, 10, 0.7)",
              backdropFilter: "blur(12px)",
              WebkitBackdropFilter: "blur(12px)",
            }}
          />

          {/* Modal Container */}
          <motion.div
            ref={containerRef as React.RefObject<HTMLDivElement>}
            role="dialog"
            aria-modal="true"
            aria-label="Keyboard shortcuts"
            tabIndex={-1}
            initial={panelInitial}
            animate={panelAnimate}
            exit={panelExit}
            transition={panelTransition}
            onClick={handleModalClick}
            className="shortcuts-overlay__panel"
            style={{
              position: "relative",
              width: "480px",
              maxWidth: "calc(100vw - 2rem)",
              maxHeight: "70vh",
              display: "flex",
              flexDirection: "column",
              borderRadius: "var(--radius-lg, 12px)",
              background: "var(--glass-bg-subtle)",
              backdropFilter: "var(--glass-blur-sm)",
              WebkitBackdropFilter: "var(--glass-blur-sm)",
              border: "1px solid var(--glass-border-light)",
              boxShadow:
                "0 24px 48px rgba(0, 0, 0, 0.4), 0 8px 16px rgba(0, 0, 0, 0.2)",
              overflow: "hidden",
            }}
          >
            {/* Header */}
            <div
              className="shortcuts-overlay__header"
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "var(--space-4, 16px) var(--space-5, 20px)",
                borderBottom: "1px solid var(--glass-border-light)",
                flexShrink: 0,
              }}
            >
              <h2
                style={{
                  margin: 0,
                  fontSize: "var(--font-size-lg, 18px)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                }}
              >
                Keyboard Shortcuts
              </h2>
              <button
                type="button"
                onClick={() => actions.closeShortcutsOverlay()}
                aria-label="Close shortcuts overlay"
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  width: "28px",
                  height: "28px",
                  border: "none",
                  borderRadius: "var(--radius-sm, 6px)",
                  background: "transparent",
                  color: "var(--color-text-secondary)",
                  cursor: "pointer",
                  transition: "background var(--duration-instant, 80ms)",
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.background =
                    "var(--state-hover-bg)";
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.background = "transparent";
                }}
              >
                <CloseIcon />
              </button>
            </div>

            {/* Shortcuts Content */}
            <div
              className="shortcuts-overlay__content"
              style={{
                flex: 1,
                overflowY: "auto",
                padding: "var(--space-4, 16px) var(--space-5, 20px)",
                display: "flex",
                flexDirection: "column",
                gap: "var(--space-5, 20px)",
              }}
            >
              {SHORTCUT_CATEGORIES.map((category) => (
                <div key={category.label} className="shortcuts-overlay__category">
                  <h3
                    style={{
                      margin: "0 0 var(--space-3, 12px) 0",
                      fontSize: "var(--font-size-xs, 11px)",
                      fontWeight: 600,
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                      color: "var(--color-text-secondary)",
                    }}
                  >
                    {category.label}
                  </h3>
                  <ul
                    style={{
                      listStyle: "none",
                      margin: 0,
                      padding: 0,
                      display: "flex",
                      flexDirection: "column",
                      gap: "var(--space-2, 8px)",
                    }}
                  >
                    {category.shortcuts.map((shortcut) => (
                      <li
                        key={shortcut.keys}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "space-between",
                          padding: "var(--space-2, 8px) var(--space-3, 12px)",
                          borderRadius: "var(--radius-sm, 6px)",
                          background: "var(--glass-bg-strong, rgba(255,255,255,0.03))",
                        }}
                      >
                        <span
                          style={{
                            color: "var(--color-text)",
                            fontSize: "var(--font-size-sm, 14px)",
                          }}
                        >
                          {shortcut.description}
                        </span>
                        <kbd
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            gap: "var(--space-1, 4px)",
                            padding: "var(--space-1, 4px) var(--space-2, 8px)",
                            borderRadius: "var(--radius-xs, 4px)",
                            border: "1px solid var(--glass-border-medium)",
                            background: "var(--glass-bg-subtle)",
                            color: "var(--color-text-secondary)",
                            fontSize: "var(--font-size-xs, 11px)",
                            fontFamily: "inherit",
                            fontWeight: 500,
                            whiteSpace: "nowrap",
                          }}
                        >
                          {formatKeys(shortcut.keys)}
                        </kbd>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

// --- Close Icon ---

function CloseIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M4 4l8 8M12 4l-8 8" />
    </svg>
  );
}
