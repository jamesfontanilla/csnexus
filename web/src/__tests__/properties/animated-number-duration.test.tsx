import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { AnimatedNumber } from "../../components/AnimatedNumber";

/**
 * **Validates: Requirements 16.5**
 *
 * Property 19: AnimatedNumber Duration Range
 *
 * For any value, the AnimatedNumber component's `data-duration` attribute
 * must be between 800 and 1500 (inclusive).
 */

beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
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

describe("Property 19: AnimatedNumber Duration Range", () => {
  it("data-duration is between 800 and 1500 for any value", () => {
    fc.assert(
      fc.property(fc.integer({ min: 0, max: 100000 }), (value) => {
        const { container } = render(<AnimatedNumber value={value} />);

        const span = container.querySelector("span");
        expect(span).not.toBeNull();

        const duration = Number(span!.getAttribute("data-duration"));
        expect(duration).toBeGreaterThanOrEqual(800);
        expect(duration).toBeLessThanOrEqual(1500);

        cleanup();
      }),
      { numRuns: 10 }
    );
  });

  it("data-duration clamps values below 800 up to 800", () => {
    const { container } = render(<AnimatedNumber value={50} duration={100} />);
    const span = container.querySelector("span");
    expect(Number(span!.getAttribute("data-duration"))).toBe(800);
  });

  it("data-duration clamps values above 1500 down to 1500", () => {
    const { container } = render(<AnimatedNumber value={50} duration={5000} />);
    const span = container.querySelector("span");
    expect(Number(span!.getAttribute("data-duration"))).toBe(1500);
  });
});
