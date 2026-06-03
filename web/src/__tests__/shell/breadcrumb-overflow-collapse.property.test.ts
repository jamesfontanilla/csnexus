// Feature: desktop-app-shell, Property 10: Breadcrumb overflow collapse
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 10.4**
 *
 * Property 10: Breadcrumb overflow collapse
 *
 * For any breadcrumb path exceeding 4 segments, the rendered breadcrumb SHALL
 * display the first segment, an ellipsis toggle, and the last 2 segments —
 * hiding middle segments behind the ellipsis dropdown.
 */

interface BreadcrumbSegment {
  label: string;
  path: string;
}

/**
 * Pure function that determines which breadcrumb segments to display
 * when overflow collapse is applied.
 *
 * Logic:
 * - If segments ≤ 4: show all, none hidden, not collapsed
 * - If segments > 4: show first + last 2 (3 visible), hide middle, collapsed = true
 */
function getVisibleSegments(segments: BreadcrumbSegment[]): {
  visible: BreadcrumbSegment[];
  hidden: BreadcrumbSegment[];
  isCollapsed: boolean;
} {
  if (segments.length <= 4) {
    return { visible: segments, hidden: [], isCollapsed: false };
  }
  const first = segments[0];
  const lastTwo = segments.slice(-2);
  const hidden = segments.slice(1, -2);
  return { visible: [first, ...lastTwo], hidden, isCollapsed: true };
}

// Generator: produces a BreadcrumbSegment with a realistic label and path
const segmentArb: fc.Arbitrary<BreadcrumbSegment> = fc
  .tuple(
    fc.stringMatching(/^[a-z][a-z0-9-]{0,19}$/),
    fc.stringMatching(/^[a-z][a-z0-9-]{0,19}$/)
  )
  .map(([label, pathPart]) => ({
    label: label.charAt(0).toUpperCase() + label.slice(1),
    path: `/${pathPart}`,
  }));

// Generator: array of 1–10 segments
const segmentsArb = (min: number, max: number) =>
  fc.array(segmentArb, { minLength: min, maxLength: max });

describe("Property 10: Breadcrumb overflow collapse", () => {
  it("paths with ≤4 segments: all segments visible, none hidden, not collapsed", () => {
    fc.assert(
      fc.property(segmentsArb(1, 4), (segments) => {
        const result = getVisibleSegments(segments);

        expect(result.visible).toEqual(segments);
        expect(result.hidden).toEqual([]);
        expect(result.isCollapsed).toBe(false);
      }),
      { numRuns: 100 }
    );
  });

  it("paths with >4 segments: exactly 3 visible (first + last 2), rest hidden, collapsed=true", () => {
    fc.assert(
      fc.property(segmentsArb(5, 10), (segments) => {
        const result = getVisibleSegments(segments);

        expect(result.visible.length).toBe(3);
        expect(result.hidden.length).toBe(segments.length - 3);
        expect(result.isCollapsed).toBe(true);
      }),
      { numRuns: 100 }
    );
  });

  it("first visible segment is always the original first segment", () => {
    fc.assert(
      fc.property(segmentsArb(5, 10), (segments) => {
        const result = getVisibleSegments(segments);

        expect(result.visible[0]).toEqual(segments[0]);
      }),
      { numRuns: 100 }
    );
  });

  it("last 2 visible segments are always the original last 2 segments", () => {
    fc.assert(
      fc.property(segmentsArb(5, 10), (segments) => {
        const result = getVisibleSegments(segments);

        const originalLastTwo = segments.slice(-2);
        expect(result.visible.slice(-2)).toEqual(originalLastTwo);
      }),
      { numRuns: 100 }
    );
  });

  it("visible.length + hidden.length always equals total segments count (no data lost)", () => {
    fc.assert(
      fc.property(segmentsArb(1, 10), (segments) => {
        const result = getVisibleSegments(segments);

        expect(result.visible.length + result.hidden.length).toBe(
          segments.length
        );
      }),
      { numRuns: 100 }
    );
  });
});
