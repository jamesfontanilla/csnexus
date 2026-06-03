import { useEffect, useRef } from "react";
import { useBreakpoint } from "./useBreakpoint";
import { useShell } from "../context/ShellContext";
import { usePageContext } from "../context/PageContextRegistry";

/**
 * Minimum content area width enforced by the auto-collapse constraint.
 * If sidebarWidth + detailPanelWidth > 50% of viewport, the detail panel
 * auto-collapses to preserve at least this much space for content.
 */
const MIN_CONTENT_AREA_WIDTH = 500;

/**
 * Hook that manages responsive panel behavior based on viewport breakpoints.
 *
 * Behavior:
 * - 1024–1279px: sidebar defaults to collapsed (56px), detail panel hidden
 * - ≥1280px: sidebar expanded (240px), detail panel visible where configured
 * - Auto-collapse constraint: if sidebarWidth + detailPanelWidth > 50% viewport,
 *   detail panel closes to maintain ≥500px content area
 * - Smooth transitions handled by CSS (grid-template-columns transition in shell.css)
 *
 * Important: This hook only sets defaults on breakpoint transitions.
 * It does NOT override user's explicit collapse/expand actions.
 */
export function useResponsivePanels(): void {
  const { isDesktop, isWideDesktop } = useBreakpoint();
  const { state, actions } = useShell();
  const { showDetailPanel } = usePageContext();

  // Track previous breakpoint values to detect transitions
  const prevIsDesktopRef = useRef<boolean | null>(null);
  const prevIsWideDesktopRef = useRef<boolean | null>(null);

  // Track whether the user has made an explicit sidebar/detail panel choice
  // this session (to avoid overriding their preference on breakpoint changes)
  const userHasSetSidebarRef = useRef(false);
  const userHasSetDetailPanelRef = useRef(false);

  // On breakpoint transitions, set panel defaults
  useEffect(() => {
    const prevIsDesktop = prevIsDesktopRef.current;
    const prevIsWideDesktop = prevIsWideDesktopRef.current;

    // First mount — set initial state based on current breakpoint
    const isInitial = prevIsDesktop === null;

    // Detect breakpoint transition (not just initial mount)
    const breakpointChanged =
      !isInitial &&
      (prevIsDesktop !== isDesktop || prevIsWideDesktop !== isWideDesktop);

    if (isInitial || breakpointChanged) {
      if (isDesktop && !isWideDesktop) {
        // 1024–1279px: collapse sidebar, hide detail panel
        if (!userHasSetSidebarRef.current || breakpointChanged) {
          actions.collapseSidebar();
        }
        if (state.detailPanelOpen && (!userHasSetDetailPanelRef.current || breakpointChanged)) {
          actions.toggleDetailPanel();
        }
      } else if (isWideDesktop) {
        // ≥1280px: expand sidebar, show detail panel where configured
        if (!userHasSetSidebarRef.current || breakpointChanged) {
          actions.expandSidebar();
        }
        if (showDetailPanel && !state.detailPanelOpen && (!userHasSetDetailPanelRef.current || breakpointChanged)) {
          actions.toggleDetailPanel();
        }
      }

      // Reset user preference tracking on breakpoint change
      if (breakpointChanged) {
        userHasSetSidebarRef.current = false;
        userHasSetDetailPanelRef.current = false;
      }
    }

    prevIsDesktopRef.current = isDesktop;
    prevIsWideDesktopRef.current = isWideDesktop;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isDesktop, isWideDesktop]);

  // Auto-collapse detail panel if panels exceed 50% viewport width
  useEffect(() => {
    if (!isDesktop || !state.detailPanelOpen) {
      return;
    }

    const checkConstraint = () => {
      const viewportWidth = window.innerWidth;
      const panelsTotalWidth = state.sidebarWidth + state.detailPanelWidth;
      const contentAreaWidth = viewportWidth - panelsTotalWidth - 8; // 8px for two resize handles (4px each)

      if (contentAreaWidth < MIN_CONTENT_AREA_WIDTH) {
        actions.toggleDetailPanel();
      }
    };

    // Check immediately
    checkConstraint();

    // Also check on resize
    const handleResize = () => {
      checkConstraint();
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [isDesktop, state.detailPanelOpen, state.sidebarWidth, state.detailPanelWidth, actions]);
}
