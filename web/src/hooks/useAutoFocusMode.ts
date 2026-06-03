import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { usePageContext } from "../context/PageContextRegistry";
import { useShell } from "../context/ShellContext";

/**
 * Hook that manages automatic focus mode activation for routes
 * configured with `autoFocusMode: true` in their PageContext.
 *
 * Behavior:
 * - Auto-enters focus mode when navigating to an autoFocusMode page
 * - Auto-exits focus mode when navigating away from an autoFocusMode page
 *   (only if focus mode was auto-activated, not manually triggered)
 * - Respects manual override: if the user exits focus mode on an
 *   autoFocusMode page, the hook won't re-enter for that session
 * - Navigating between two autoFocusMode pages maintains focus mode
 *   without flicker (no exit + re-enter)
 *
 * Should be called inside a component that has access to both
 * ShellContext and React Router (e.g., ShellContainer).
 */
export function useAutoFocusMode(): void {
  const { pathname } = useLocation();
  const { autoFocusMode } = usePageContext();
  const { state, actions } = useShell();

  // Track whether focus mode was auto-activated (vs manually triggered)
  const autoActivatedRef = useRef(false);

  // Track routes where user manually overrode auto-focus (exited focus mode)
  // Using a Set of pathnames for the current session
  const overriddenPathsRef = useRef<Set<string>>(new Set());

  // Track the previous autoFocusMode value to detect transitions
  const prevAutoFocusModeRef = useRef<boolean | undefined>(undefined);

  // Track the previous focusModeActive state to detect manual exit
  const prevFocusModeActiveRef = useRef(state.focusModeActive);

  useEffect(() => {
    const wasFocusModeActive = prevFocusModeActiveRef.current;

    // Detect manual exit: focus mode was active and auto-activated,
    // but now it's inactive — user manually exited
    if (
      wasFocusModeActive &&
      !state.focusModeActive &&
      autoActivatedRef.current &&
      autoFocusMode
    ) {
      // User manually exited focus mode on this autoFocusMode page
      overriddenPathsRef.current.add(pathname);
      autoActivatedRef.current = false;
    }

    // Update previous state ref
    prevFocusModeActiveRef.current = state.focusModeActive;
  }, [state.focusModeActive, autoFocusMode, pathname]);

  useEffect(() => {
    const wasAutoFocusMode = prevAutoFocusModeRef.current;

    if (autoFocusMode) {
      // Navigating TO an autoFocusMode page
      if (!state.focusModeActive) {
        // Only auto-enter if user hasn't manually overridden this path
        if (!overriddenPathsRef.current.has(pathname)) {
          actions.enterFocusMode();
          autoActivatedRef.current = true;
        }
      } else if (wasAutoFocusMode) {
        // Navigating between two autoFocusMode pages — maintain focus mode
        // No action needed, focus mode stays active, no flicker
      } else {
        // Focus mode was already active (manually triggered) before landing here
        // Don't track this as auto-activated
      }
    } else {
      // Navigating AWAY from an autoFocusMode page
      if (wasAutoFocusMode && state.focusModeActive && autoActivatedRef.current) {
        // Auto-exit only if focus mode was auto-activated
        actions.exitFocusMode();
        autoActivatedRef.current = false;
      }
    }

    prevAutoFocusModeRef.current = autoFocusMode;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname, autoFocusMode]);
}
