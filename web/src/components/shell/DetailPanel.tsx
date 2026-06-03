import { Suspense, useCallback, useEffect, useRef, useMemo, useState, type ComponentType } from "react";
import { motion } from "framer-motion";
import { useShell } from "../../context/ShellContext";
import { usePageContext } from "../../context/PageContextRegistry";
import { useReducedMotion } from "../../design-system";
import React from "react";

// --- Skeleton Loader Fallback ---

function DetailPanelSkeleton() {
  return (
    <div className="detail-panel__skeleton" aria-busy="true" aria-label="Loading panel content">
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--title" />
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--line" />
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--line" />
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--short" />
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--line" />
      <div className="detail-panel__skeleton-bar detail-panel__skeleton-bar--line" />
    </div>
  );
}

// --- Error Boundary ---

interface ErrorBoundaryState {
  hasError: boolean;
}

class DetailPanelErrorBoundary extends React.Component<
  { children: React.ReactNode; onRetry: () => void },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode; onRetry: () => void }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="detail-panel__error">
          <p className="detail-panel__error-message">Failed to load panel content.</p>
          <button
            className="detail-panel__error-retry"
            onClick={() => {
              this.setState({ hasError: false });
              this.props.onRetry();
            }}
          >
            Retry
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// --- Framer Motion variants ---

const DURATION_NORMAL = 0.25; // --duration-normal
const DURATION_INSTANT = 0.08; // --duration-instant for prefers-reduced-motion

function getPanelVariants(reducedMotion: boolean) {
  const duration = reducedMotion ? DURATION_INSTANT : DURATION_NORMAL;
  return {
    hidden: { x: reducedMotion ? 0 : "100%", opacity: reducedMotion ? 0 : 1 },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        duration,
        ease: [0, 0, 0.2, 1], // matches --ease-decelerate
      },
    },
    exit: {
      x: reducedMotion ? 0 : "100%",
      opacity: reducedMotion ? 0 : 1,
      transition: {
        duration,
        ease: [0.4, 0, 1, 1], // matches --ease-accelerate
      },
    },
  };
}

// --- Detail Panel Component ---

export function DetailPanel() {
  const { state, actions } = useShell();
  const pageContext = usePageContext();
  const panelRef = useRef<HTMLDivElement>(null);
  const [retryKey, setRetryKey] = useState(0);
  const reducedMotion = useReducedMotion();

  // Build the aria-label based on what's loaded
  const ariaLabel = useMemo(() => {
    if (pageContext.detailPanelComponent) {
      // Derive label from the component path or context
      return "Contextual detail panel";
    }
    return "Detail panel";
  }, [pageContext.detailPanelComponent]);

  // Lazy-load the contextual component from PageContext
  const LazyComponent = useMemo(() => {
    if (!pageContext.detailPanelComponent) return null;
    return React.lazy(pageContext.detailPanelComponent as () => Promise<{ default: ComponentType<object> }>);
  }, [pageContext.detailPanelComponent]);

  // Get motion variants based on reduced motion preference
  const panelVariants = useMemo(() => getPanelVariants(reducedMotion), [reducedMotion]);

  // Handle retry after error
  const handleRetry = useCallback(() => {
    setRetryKey((k) => k + 1);
  }, []);

  // Close panel
  const handleClose = useCallback(() => {
    actions.toggleDetailPanel();
  }, [actions]);

  // Escape key closes panel when it has focus
  useEffect(() => {
    const panel = panelRef.current;
    if (!panel || !state.detailPanelOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.stopPropagation();
        actions.toggleDetailPanel();
      }
    };

    panel.addEventListener("keydown", handleKeyDown);
    return () => panel.removeEventListener("keydown", handleKeyDown);
  }, [state.detailPanelOpen, actions]);

  if (!state.detailPanelOpen) return null;

  return (
    <motion.aside
      ref={panelRef}
      className="detail-panel"
      role="complementary"
      aria-label={ariaLabel}
      style={{ gridArea: "detail" }}
      variants={panelVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      tabIndex={-1}
    >
      <div className="detail-panel__header">
        <button
          className="detail-panel__close-btn"
          onClick={handleClose}
          aria-label="Close detail panel"
          type="button"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M4 4l8 8M12 4l-8 8"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </div>
      <div className="detail-panel__content">
        {LazyComponent ? (
          <DetailPanelErrorBoundary key={retryKey} onRetry={handleRetry}>
            <Suspense fallback={<DetailPanelSkeleton />}>
              <LazyComponent />
            </Suspense>
          </DetailPanelErrorBoundary>
        ) : (
          <div className="detail-panel__empty" />
        )}
      </div>
    </motion.aside>
  );
}
