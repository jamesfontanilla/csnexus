import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { ProgressRing } from "../../components/ProgressRing";

/**
 * **Validates: Requirements 8.7**
 *
 * Property 12: ProgressRing Value Clamping
 *
 * For any float value (including negative, very large, Infinity, -Infinity),
 * the rendered stroke-dashoffset must correspond to a clamped percentage
 * in [0, 1] — meaning the offset is between 0 and the circumference.
 */

beforeAll(() => {
  // Mock matchMedia with reduced motion enabled so offset is set immediately
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: query.includes("prefers-reduced-motion"),
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
});

afterEach(() => {
  cleanup();
});

describe("Property 12: ProgressRing Value Clamping", () => {
  it("stroke-dashoffset corresponds to a percentage in [0, 1] for any float value", () => {
    const size = 100;
    const strokeWidth = 8;
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;

    fc.assert(
      fc.property(fc.float({ noNaN: true }), (value) => {
        const { container } = render(
          <ProgressRing size={size} value={value} />
        );

        // Get the progress circle (second circle element)
        const circles = container.querySelectorAll("circle");
        expect(circles.length).toBe(2);

        const progressCircle = circles[1];
        const offsetAttr = progressCircle.getAttribute("stroke-dashoffset");
        expect(offsetAttr).not.toBeNull();

        const offset = parseFloat(offsetAttr!);

        // The offset must be between 0 (100% filled) and circumference (0% filled)
        expect(offset).toBeGreaterThanOrEqual(0);
        expect(offset).toBeLessThanOrEqual(circumference);

        cleanup();
      })
    );
  });
});
