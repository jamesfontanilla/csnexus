import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { GlassInput } from "../../components/GlassInput";

/**
 * **Validates: Requirements 5.4**
 *
 * Property 8: GlassInput Character Count Accuracy
 *
 * When a GlassInput is rendered with a `value` and `maxLength` prop,
 * the displayed character count must equal `value.length`.
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

describe("Property 8: GlassInput Character Count Accuracy", () => {
  it("displayed count equals value.length for any string and maxLength", () => {
    fc.assert(
      fc.property(
        fc.string(),
        fc.integer({ min: 1, max: 500 }),
        (value, maxLength) => {
          const { getByTestId } = render(
            <GlassInput value={value} maxLength={maxLength} onChange={() => {}} />
          );

          const charCount = getByTestId("char-count");
          expect(charCount.textContent).toBe(`${value.length}/${maxLength}`);

          cleanup();
        }
      ),
      { numRuns: 10 }
    );
  });
});
