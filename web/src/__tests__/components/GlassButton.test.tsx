import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, fireEvent } from "@testing-library/react";
import { GlassButton } from "../../components/GlassButton";

/**
 * Unit tests for GlassButton component.
 * Validates: Requirements 3.2, 3.7, 3.9
 */

// Mock matchMedia for prefers-reduced-motion
function mockMatchMedia(matches: boolean) {
  const listeners: Array<(e: MediaQueryListEvent) => void> = [];
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: (_event: string, handler: (e: MediaQueryListEvent) => void) => {
        listeners.push(handler);
      },
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

describe("GlassButton", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("icon rendering (Requirement 3.2)", () => {
    it("renders iconLeft before the label", () => {
      const { container } = render(
        <GlassButton iconLeft={<svg data-testid="icon-left" />}>
          Label
        </GlassButton>
      );

      const iconSpan = container.querySelector(".btn-icon-left");
      expect(iconSpan).not.toBeNull();
      expect(iconSpan!.querySelector("[data-testid='icon-left']")).not.toBeNull();

      // Verify icon comes before the label text in DOM order
      const button = container.querySelector("button")!;
      const children = Array.from(button.childNodes);
      const iconIndex = children.findIndex(
        (node) => node === iconSpan
      );
      const textIndex = children.findIndex(
        (node) => node.textContent === "Label" && node !== iconSpan
      );
      expect(iconIndex).toBeLessThan(textIndex);
    });

    it("renders iconRight after the label", () => {
      const { container } = render(
        <GlassButton iconRight={<svg data-testid="icon-right" />}>
          Label
        </GlassButton>
      );

      const iconSpan = container.querySelector(".btn-icon-right");
      expect(iconSpan).not.toBeNull();
      expect(iconSpan!.querySelector("[data-testid='icon-right']")).not.toBeNull();

      // Verify icon comes after the label text in DOM order
      const button = container.querySelector("button")!;
      const children = Array.from(button.childNodes);
      const iconIndex = children.findIndex(
        (node) => node === iconSpan
      );
      const textIndex = children.findIndex(
        (node) => node.textContent === "Label" && node !== iconSpan
      );
      expect(textIndex).toBeLessThan(iconIndex);
    });

    it("renders both iconLeft and iconRight simultaneously", () => {
      const { container } = render(
        <GlassButton
          iconLeft={<svg data-testid="icon-left" />}
          iconRight={<svg data-testid="icon-right" />}
        >
          Label
        </GlassButton>
      );

      expect(container.querySelector(".btn-icon-left")).not.toBeNull();
      expect(container.querySelector(".btn-icon-right")).not.toBeNull();
    });
  });

  describe("ripple skipped with prefers-reduced-motion (Requirement 3.7)", () => {
    it("does not create ripple elements when prefers-reduced-motion is active", () => {
      mockMatchMedia(true);

      const { container } = render(
        <GlassButton>Click me</GlassButton>
      );

      const button = container.querySelector("button")!;

      fireEvent.pointerDown(button, {
        clientX: 50,
        clientY: 25,
      });

      const ripple = container.querySelector(".btn-ripple");
      expect(ripple).toBeNull();
    });

    it("creates ripple elements when prefers-reduced-motion is not active", () => {
      mockMatchMedia(false);

      const { container } = render(
        <GlassButton>Click me</GlassButton>
      );

      const button = container.querySelector("button")!;

      fireEvent.pointerDown(button, {
        clientX: 50,
        clientY: 25,
      });

      const ripple = container.querySelector(".btn-ripple");
      expect(ripple).not.toBeNull();
    });
  });

  describe("variant rendering without regression (Requirement 3.9)", () => {
    const variants = ["primary", "secondary", "ghost", "danger"] as const;

    variants.forEach((variant) => {
      it(`renders ${variant} variant without errors`, () => {
        const { container } = render(
          <GlassButton variant={variant}>Button</GlassButton>
        );

        const button = container.querySelector("button");
        expect(button).not.toBeNull();
        expect(button!.className).toContain(`btn-glass-${variant}`);
        expect(button!.textContent).toContain("Button");
      });
    });

    it("applies btn-glass base class on all variants", () => {
      const variants = ["primary", "secondary", "ghost", "danger"] as const;

      variants.forEach((variant) => {
        const { container } = render(
          <GlassButton variant={variant}>Test</GlassButton>
        );

        const button = container.querySelector("button");
        expect(button!.className).toContain("btn-glass");
      });
    });
  });
});
