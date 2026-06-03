import { describe, it, expect, vi, beforeAll } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { ResizeHandle } from "../../components/shell/ResizeHandle";

// jsdom doesn't define PointerEvent — polyfill it as a MouseEvent subclass
beforeAll(() => {
  if (typeof globalThis.PointerEvent === "undefined") {
    // @ts-expect-error polyfill for jsdom
    globalThis.PointerEvent = class PointerEvent extends MouseEvent {
      constructor(type: string, params: PointerEventInit = {}) {
        super(type, params);
      }
    };
  }
});

function createMockContainerRef(initialWidth = "240px") {
  const el = document.createElement("div");
  el.style.setProperty("--sidebar-width", initialWidth);
  el.style.setProperty("--detail-panel-width", "320px");
  return { current: el };
}

describe("ResizeHandle", () => {
  const defaultProps = {
    cssProperty: "--sidebar-width" as const,
    containerRef: createMockContainerRef(),
    onResizeEnd: vi.fn(),
    gridArea: "resize-handle",
    minWidth: 180,
    maxWidth: 360,
  };

  it("renders a separator element", () => {
    render(<ResizeHandle {...defaultProps} />);
    const handle = screen.getByRole("separator");
    expect(handle).toBeInTheDocument();
  });

  it("has correct ARIA attributes", () => {
    render(<ResizeHandle {...defaultProps} />);
    const handle = screen.getByRole("separator");
    expect(handle).toHaveAttribute("aria-orientation", "vertical");
    expect(handle).toHaveAttribute("aria-valuemin", "180");
    expect(handle).toHaveAttribute("aria-valuemax", "360");
    expect(handle).toHaveAttribute("tabindex", "0");
  });

  it("applies gridArea style", () => {
    render(<ResizeHandle {...defaultProps} gridArea="resize-detail" />);
    const handle = screen.getByRole("separator");
    expect(handle.style.gridArea).toBe("resize-detail");
  });

  it("has resize-handle class by default (not dragging)", () => {
    render(<ResizeHandle {...defaultProps} />);
    const handle = screen.getByRole("separator");
    expect(handle.className).toContain("resize-handle");
    expect(handle.className).not.toContain("resize-handle--dragging");
  });

  it("adds dragging class on pointerdown", () => {
    render(<ResizeHandle {...defaultProps} />);
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });
    expect(handle.className).toContain("resize-handle--dragging");
  });

  it("updates CSS custom property during pointermove", () => {
    const containerRef = createMockContainerRef("240px");
    render(<ResizeHandle {...defaultProps} containerRef={containerRef} />);
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });

    // Simulate pointermove on document
    fireEvent(
      document,
      new PointerEvent("pointermove", { clientX: 280, bubbles: true })
    );

    // Width should have increased by 40px (280-240) → 240 + 40 = 280
    expect(containerRef.current.style.getPropertyValue("--sidebar-width")).toBe(
      "280px"
    );
  });

  it("clamps width to maxWidth", () => {
    const containerRef = createMockContainerRef("240px");
    render(
      <ResizeHandle {...defaultProps} containerRef={containerRef} maxWidth={360} />
    );
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });

    // Move far right — should clamp at 360
    fireEvent(
      document,
      new PointerEvent("pointermove", { clientX: 500, bubbles: true })
    );

    expect(containerRef.current.style.getPropertyValue("--sidebar-width")).toBe(
      "360px"
    );
  });

  it("clamps width to minWidth", () => {
    const containerRef = createMockContainerRef("240px");
    render(
      <ResizeHandle {...defaultProps} containerRef={containerRef} minWidth={180} />
    );
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });

    // Move far left — should clamp at 180
    fireEvent(
      document,
      new PointerEvent("pointermove", { clientX: 100, bubbles: true })
    );

    expect(containerRef.current.style.getPropertyValue("--sidebar-width")).toBe(
      "180px"
    );
  });

  it("calls onResizeEnd with final width on pointerup", () => {
    const onResizeEnd = vi.fn();
    const containerRef = createMockContainerRef("240px");
    render(
      <ResizeHandle
        {...defaultProps}
        containerRef={containerRef}
        onResizeEnd={onResizeEnd}
      />
    );
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });
    fireEvent(
      document,
      new PointerEvent("pointerup", { clientX: 300, bubbles: true })
    );

    expect(onResizeEnd).toHaveBeenCalledWith(300);
  });

  it("snaps to snapTo value when below threshold", () => {
    const onResizeEnd = vi.fn();
    const containerRef = createMockContainerRef("240px");
    render(
      <ResizeHandle
        {...defaultProps}
        containerRef={containerRef}
        onResizeEnd={onResizeEnd}
        snapBelowThreshold={{ threshold: 100, snapTo: 56 }}
      />
    );
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });

    // Drag far left: 240 + (50 - 240) = 50, which is below 100 threshold → snap to 56
    fireEvent(
      document,
      new PointerEvent("pointerup", { clientX: 50, bubbles: true })
    );

    expect(onResizeEnd).toHaveBeenCalledWith(56);
  });

  it("resets to default on double-click (sidebar)", () => {
    const onResizeEnd = vi.fn();
    const containerRef = createMockContainerRef("300px");
    render(
      <ResizeHandle
        {...defaultProps}
        cssProperty="--sidebar-width"
        containerRef={containerRef}
        onResizeEnd={onResizeEnd}
      />
    );
    const handle = screen.getByRole("separator");

    fireEvent.doubleClick(handle);

    expect(containerRef.current.style.getPropertyValue("--sidebar-width")).toBe(
      "240px"
    );
    expect(onResizeEnd).toHaveBeenCalledWith(240);
  });

  it("resets to default on double-click (detail panel)", () => {
    const onResizeEnd = vi.fn();
    const containerRef = createMockContainerRef("400px");
    containerRef.current.style.setProperty("--detail-panel-width", "400px");
    render(
      <ResizeHandle
        {...defaultProps}
        cssProperty="--detail-panel-width"
        containerRef={containerRef}
        onResizeEnd={onResizeEnd}
      />
    );
    const handle = screen.getByRole("separator");

    fireEvent.doubleClick(handle);

    expect(
      containerRef.current.style.getPropertyValue("--detail-panel-width")
    ).toBe("320px");
    expect(onResizeEnd).toHaveBeenCalledWith(320);
  });

  it("removes dragging class on pointerup", () => {
    render(<ResizeHandle {...defaultProps} />);
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 240 });
    expect(handle.className).toContain("resize-handle--dragging");

    fireEvent(
      document,
      new PointerEvent("pointerup", { clientX: 240, bubbles: true })
    );

    expect(handle.className).not.toContain("resize-handle--dragging");
  });

  it("supports right direction (detail panel resize)", () => {
    const onResizeEnd = vi.fn();
    const containerRef = createMockContainerRef("320px");
    containerRef.current.style.setProperty("--detail-panel-width", "320px");
    render(
      <ResizeHandle
        cssProperty="--detail-panel-width"
        containerRef={containerRef}
        onResizeEnd={onResizeEnd}
        gridArea="resize-detail"
        minWidth={240}
        maxWidth={480}
        direction="right"
      />
    );
    const handle = screen.getByRole("separator");

    fireEvent.pointerDown(handle, { clientX: 800 });

    // Moving left by 40px should increase the detail panel width by 40px
    fireEvent(
      document,
      new PointerEvent("pointermove", { clientX: 760, bubbles: true })
    );

    expect(
      containerRef.current.style.getPropertyValue("--detail-panel-width")
    ).toBe("360px");
  });
});
