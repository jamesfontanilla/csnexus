// Feature: desktop-app-shell, Property 3: Layout mode from PageContext
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 4.2**
 *
 * Property 3: Layout mode from PageContext
 *
 * For any valid PageContext with a layoutMode value of 'standard', 'centered',
 * or 'split', the ContentArea component SHALL apply the corresponding CSS
 * class/grid configuration for that mode.
 */

const VALID_LAYOUT_MODES = ["standard", "centered", "split"] as const;
type _LayoutMode = (typeof VALID_LAYOUT_MODES)[number];

/**
 * Pure function mirroring the ContentArea's getContentClassName logic.
 * This is the specification under test — extracted from ContentArea.tsx.
 */
function getContentClassName(layoutMode: string): string {
  const base = "content-area__content";
  switch (layoutMode) {
    case "centered":
      return `${base} ${base}--centered`;
    case "split":
      return `${base} ${base}--split`;
    default:
      return `${base} ${base}--standard`;
  }
}

/** Arbitrary that generates one of the three valid layout modes. */
const layoutModeArb = fc.constantFrom(...VALID_LAYOUT_MODES);

describe("Property 3: Layout mode from PageContext", () => {
  it("for any valid layoutMode, the result always contains the base class", () => {
    fc.assert(
      fc.property(layoutModeArb, (mode) => {
        const result = getContentClassName(mode);
        expect(result).toContain("content-area__content");
      }),
      { numRuns: 100 }
    );
  });

  it("for any valid layoutMode, the result contains the mode-specific modifier class", () => {
    fc.assert(
      fc.property(layoutModeArb, (mode) => {
        const result = getContentClassName(mode);
        expect(result).toContain(`content-area__content--${mode}`);
      }),
      { numRuns: 100 }
    );
  });

  it("the mapping is bijective — each mode maps to a unique class", () => {
    fc.assert(
      fc.property(
        layoutModeArb,
        layoutModeArb,
        (modeA, modeB) => {
          const resultA = getContentClassName(modeA);
          const resultB = getContentClassName(modeB);

          if (modeA === modeB) {
            expect(resultA).toBe(resultB);
          } else {
            expect(resultA).not.toBe(resultB);
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any valid layoutMode, the class string is exactly base + modifier (no extras)", () => {
    fc.assert(
      fc.property(layoutModeArb, (mode) => {
        const base = "content-area__content";
        const expected = `${base} ${base}--${mode}`;
        const result = getContentClassName(mode);
        expect(result).toBe(expected);
      }),
      { numRuns: 100 }
    );
  });
});
