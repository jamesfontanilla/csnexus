import { useState, useEffect } from "react";

const DESKTOP_QUERY = "(min-width: 1024px)";
const WIDE_DESKTOP_QUERY = "(min-width: 1280px)";
const DEBOUNCE_MS = 100;

interface BreakpointState {
  /** True when viewport is ≥1024px */
  isDesktop: boolean;
  /** True when viewport is ≥1280px (sidebar defaults expanded) */
  isWideDesktop: boolean;
}

/**
 * Hook for detecting desktop breakpoints with 100ms debounce.
 *
 * - `isDesktop`: true at ≥1024px — activates the App Shell.
 * - `isWideDesktop`: true at ≥1280px — sidebar defaults to expanded.
 *   Between 1024–1279px the sidebar should default to collapsed.
 *
 * The 100ms debounce prevents layout flickering when the viewport rapidly
 * crosses the 1024px boundary (e.g., window snapping on Windows).
 */
export function useBreakpoint(): BreakpointState {
  const [state, setState] = useState<BreakpointState>(() => {
    if (typeof window === "undefined") {
      return { isDesktop: false, isWideDesktop: false };
    }
    return {
      isDesktop: window.matchMedia(DESKTOP_QUERY).matches,
      isWideDesktop: window.matchMedia(WIDE_DESKTOP_QUERY).matches,
    };
  });

  useEffect(() => {
    const desktopMql = window.matchMedia(DESKTOP_QUERY);
    const wideMql = window.matchMedia(WIDE_DESKTOP_QUERY);
    let timeoutId: ReturnType<typeof setTimeout> | null = null;

    const update = () => {
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
      }
      timeoutId = setTimeout(() => {
        setState({
          isDesktop: desktopMql.matches,
          isWideDesktop: wideMql.matches,
        });
        timeoutId = null;
      }, DEBOUNCE_MS);
    };

    desktopMql.addEventListener("change", update);
    wideMql.addEventListener("change", update);

    return () => {
      desktopMql.removeEventListener("change", update);
      wideMql.removeEventListener("change", update);
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
      }
    };
  }, []);

  return state;
}
