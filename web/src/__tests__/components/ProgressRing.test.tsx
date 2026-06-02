import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { ProgressRing } from "../../components/ProgressRing";

function mockMatchMedia(reducedMotion: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches:
        query === "(prefers-reduced-motion: reduce)" ? reducedMotion : false,
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

describe("ProgressRing", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("ARIA attributes", () => {
    it("has role='progressbar' with correct aria-valuenow, aria-valuemin, aria-valuemax, and aria-label", () => {
      const { container } = render(
        <ProgressRing size={100} value={75} label="Test" />
      );

      const svg = container.querySelector("svg");
      expect(svg).not.toBeNull();
      expect(svg).toHaveAttribute("role", "progressbar");
      expect(svg).toHaveAttribute("aria-valuenow", "75");
      expect(svg).toHaveAttribute("aria-valuemin", "0");
      expect(svg).toHaveAttribute("aria-valuemax", "100");
      expect(svg).toHaveAttribute("aria-label", "Test");
    });
  });

  describe("reduced-motion skips mount animation", () => {
    it("sets stroke-dashoffset to target value immediately when reduced-motion is active", () => {
      mockMatchMedia(true);

      const size = 100;
      const value = 75;
      const strokeWidth = 8;
      const radius = (size - strokeWidth) / 2;
      const circumference = 2 * Math.PI * radius;
      const expectedOffset = circumference * (1 - value / 100);

      const { container } = render(
        <ProgressRing size={size} value={value} strokeWidth={strokeWidth} />
      );

      const circles = container.querySelectorAll("circle");
      // The second circle is the progress circle
      const progressCircle = circles[1];
      expect(progressCircle).not.toBeNull();

      const dashoffset = progressCircle.getAttribute("stroke-dashoffset");
      expect(Number(dashoffset)).toBeCloseTo(expectedOffset, 2);
    });
  });

  describe("size=0 returns null", () => {
    it("renders nothing when size is 0", () => {
      const { container } = render(<ProgressRing size={0} value={50} />);

      const svg = container.querySelector("svg");
      expect(svg).toBeNull();
    });
  });
});
