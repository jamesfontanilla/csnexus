import { useCallback, useRef, type ReactNode } from "react";
import {
  useShell,
  SIDEBAR_MIN_WIDTH,
  SIDEBAR_MAX_WIDTH,
  SIDEBAR_COLLAPSED_WIDTH,
  DETAIL_PANEL_MIN_WIDTH,
  DETAIL_PANEL_MAX_WIDTH,
} from "../../context/ShellContext";
import { ResizeHandle } from "./ResizeHandle";
import { Sidebar } from "./Sidebar";
import { BreadcrumbBar } from "./BreadcrumbBar";
import { ContentArea } from "./ContentArea";
import { DetailPanel } from "./DetailPanel";
import { useAutoFocusMode } from "../../hooks/useAutoFocusMode";
import { useResponsivePanels } from "../../hooks/useResponsivePanels";
import "./shell.css";

interface ShellContainerProps {
  children: ReactNode;
}

export function ShellContainer({ children }: ShellContainerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const { state, actions } = useShell();

  // Auto-activate/deactivate focus mode based on PageContext.autoFocusMode
  useAutoFocusMode();

  // Responsive panel constraints: auto-collapse on narrow viewports,
  // enforce min content area width
  useResponsivePanels();

  const className = getContainerClassName(state.focusModeActive, state.detailPanelOpen);

  const handleSidebarResizeEnd = useCallback(
    (width: number) => {
      actions.setSidebarWidth(width);
    },
    [actions]
  );

  return (
    <div
      ref={containerRef}
      className={className}
      style={{
        "--sidebar-width": `${state.sidebarWidth}px`,
        "--detail-panel-width": `${state.detailPanelWidth}px`,
      } as React.CSSProperties}
    >
      {!state.focusModeActive && (
        <>
          <Sidebar />
          <ResizeHandle
            cssProperty="--sidebar-width"
            containerRef={containerRef}
            onResizeEnd={handleSidebarResizeEnd}
            gridArea="resize-handle"
            minWidth={SIDEBAR_MIN_WIDTH}
            maxWidth={SIDEBAR_MAX_WIDTH}
            snapBelowThreshold={{ threshold: 100, snapTo: SIDEBAR_COLLAPSED_WIDTH }}
            direction="left"
          />
        </>
      )}
      <div className="shell-main">
        {!state.focusModeActive && <BreadcrumbBar />}
        <ContentArea>{children}</ContentArea>
      </div>
      {state.detailPanelOpen && !state.focusModeActive && (
        <ResizeHandle
          cssProperty="--detail-panel-width"
          containerRef={containerRef}
          onResizeEnd={(width) => actions.setDetailPanelWidth(width)}
          gridArea="resize-detail"
          minWidth={DETAIL_PANEL_MIN_WIDTH}
          maxWidth={DETAIL_PANEL_MAX_WIDTH}
          direction="right"
        />
      )}
      {!state.focusModeActive && <DetailPanel />}
    </div>
  );
}

function getContainerClassName(focusModeActive: boolean, detailPanelOpen: boolean): string {
  if (focusModeActive) {
    return "shell-container shell-container--focus";
  }
  if (detailPanelOpen) {
    return "shell-container shell-container--split";
  }
  return "shell-container";
}

export { type ShellContainerProps };
