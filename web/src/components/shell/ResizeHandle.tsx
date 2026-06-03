import { useCallback, useRef, useState } from "react";

interface ResizeHandleProps {
  /** CSS custom property name to update during drag */
  cssProperty: "--sidebar-width" | "--detail-panel-width";
  /** Ref to the container element where CSS property is set */
  containerRef: React.RefObject<HTMLDivElement | null>;
  /** Called on pointerup with the final pixel width */
  onResizeEnd: (width: number) => void;
  /** Grid area name for placement */
  gridArea: string;
  /** Min/max constraints */
  minWidth: number;
  maxWidth: number;
  /** Optional: snap-to value when below threshold */
  snapBelowThreshold?: { threshold: number; snapTo: number };
  /** Direction: 'left' means dragging right increases width, 'right' means dragging left increases width */
  direction?: "left" | "right";
}

/**
 * A 4px-wide interactive resize handle rendered between shell panels.
 *
 * During drag, updates CSS custom properties directly on the container element
 * (no React re-renders per pointer-move) for smooth 60fps resizing.
 * Commits the final width to shell state on pointer-up.
 */
export function ResizeHandle({
  cssProperty,
  containerRef,
  onResizeEnd,
  gridArea,
  minWidth,
  maxWidth,
  snapBelowThreshold,
  direction = "left",
}: ResizeHandleProps) {
  const [isDragging, setIsDragging] = useState(false);
  const dragState = useRef<{
    startX: number;
    startWidth: number;
  } | null>(null);
  const handleRef = useRef<HTMLDivElement>(null);
  const lastCommittedWidth = useRef<number>(0);

  const computeWidth = useCallback(
    (clientX: number): number => {
      if (!dragState.current) return minWidth;

      const delta =
        direction === "left"
          ? clientX - dragState.current.startX
          : dragState.current.startX - clientX;

      const rawWidth = dragState.current.startWidth + delta;

      // Snap-to-collapse behavior
      if (snapBelowThreshold && rawWidth < snapBelowThreshold.threshold) {
        return snapBelowThreshold.snapTo;
      }

      // Clamp to min/max
      return Math.max(minWidth, Math.min(maxWidth, rawWidth));
    },
    [direction, minWidth, maxWidth, snapBelowThreshold]
  );

  const handlePointerMove = useCallback(
    (e: PointerEvent) => {
      const container = containerRef.current;
      if (!container || !dragState.current) return;

      const width = computeWidth(e.clientX);
      lastCommittedWidth.current = width;
      container.style.setProperty(cssProperty, `${width}px`);
    },
    [containerRef, cssProperty, computeWidth]
  );

  const handlePointerUp = useCallback(
    (e: PointerEvent) => {
      document.removeEventListener("pointermove", handlePointerMove);
      document.removeEventListener("pointerup", handlePointerUp);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";

      const width = computeWidth(e.clientX);
      lastCommittedWidth.current = width;
      dragState.current = null;
      setIsDragging(false);
      onResizeEnd(width);
    },
    [handlePointerMove, computeWidth, onResizeEnd]
  );

  const handlePointerDown = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      e.preventDefault();

      const container = containerRef.current;
      if (!container) return;

      // Read current width from the CSS property
      const currentValue = container.style.getPropertyValue(cssProperty);
      const startWidth = parseInt(currentValue, 10) || minWidth;

      dragState.current = {
        startX: e.clientX,
        startWidth,
      };
      lastCommittedWidth.current = startWidth;
      setIsDragging(true);

      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";

      document.addEventListener("pointermove", handlePointerMove);
      document.addEventListener("pointerup", handlePointerUp);
    },
    [containerRef, cssProperty, minWidth, handlePointerMove, handlePointerUp]
  );

  const handleDoubleClick = useCallback(() => {
    const container = containerRef.current;
    if (!container) return;

    // Reset to default (midpoint or standard default for the property)
    const defaultWidth = cssProperty === "--sidebar-width" ? 240 : 320;
    container.style.setProperty(cssProperty, `${defaultWidth}px`);
    onResizeEnd(defaultWidth);
  }, [containerRef, cssProperty, onResizeEnd]);

  return (
    <div
      ref={handleRef}
      className={`resize-handle ${isDragging ? "resize-handle--dragging" : ""}`}
      style={{ gridArea }}
      role="separator"
      aria-orientation="vertical"
      aria-valuenow={lastCommittedWidth.current}
      aria-valuemin={minWidth}
      aria-valuemax={maxWidth}
      tabIndex={0}
      onPointerDown={handlePointerDown}
      onDoubleClick={handleDoubleClick}
    />
  );
}

export { type ResizeHandleProps };
