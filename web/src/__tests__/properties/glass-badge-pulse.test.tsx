import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { GlassBadge } from "../../components/GlassBadge";

/**
 * **Validates: Requirements 7.2, 7.3**
 *
 * Property 10: GlassBadge Pulse Respects Reduced Motion
 *
 * When `prefers-reduced-motion: reduce` is active, the GlassBadge must NOT
 * apply the `.badge-dot-pulse` class to the dot indicator, regardless of
 * the `pulse` prop value. This ensures users who prefer reduced motion
 * see a static dot indicator.
 */

beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: query === "(prefers-reduced-motion: reduce)",
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

describe("Property 10: GlassBadge Pulse Respects Reduced Motion", () => {
  it("does not apply .badge-dot-pulse class when prefers-reduced-motion is active", () => {
    fc.assert(
      fc.property(fc.string(), (label) => {
        const { container } = render(
          <GlassBadge label={label} dot pulse />
        );

        const pulseElement = container.querySelector(".badge-dot-pulse");
        expect(pulseElement).toBeNull();

        cleanup();
      })
    );
  });
});
