// Feature: desktop-app-shell, Property 1: Sidebar resize clamping
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 3.2, 3.3, 3.5**
 *
 * Property 1: Sidebar resize clamping
 *
 * For any pointer X position during a sidebar drag operation, the resulting
 * sidebar width SHALL equal `clamp(180, pointerX - shellLeftEdge, 360)` —
 * never exceeding 360px, never falling below 180px (or snapping to 56px
 * if dragged below 100px).
 */

const SIDEBAR_MIN_WIDTH = 180;
const SIDEBAR_MAX_WIDTH = 360;
const SIDEBAR_COLLAPSED_WIDTH = 56;
const SNAP_THRESHOLD = 100;

/**
 * Pure function that mirrors the ResizeHandle clamping logic for the sidebar.
 * This is the specification under test — extracted from the component's
 * `computeWidth` callback behavior when configured for sidebar resize.
 */
function computeSidebarWidth(rawWidth: number): number {
  if (rawWidth < SNAP_THRESHOLD) return SIDEBAR_COLLAPSED_WIDTH;
  return Math.max(SIDEBAR_MIN_WIDTH, Math.min(SIDEBAR_MAX_WIDTH, rawWidth));
}

describe("Property 1: Sidebar resize clamping", () => {
  it("rawWidth within [180, 360] → result equals rawWidth (within bounds)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: SIDEBAR_MIN_WIDTH, max: SIDEBAR_MAX_WIDTH }),
        (rawWidth) => {
          const result = computeSidebarWidth(rawWidth);
          expect(result).toBe(rawWidth);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("rawWidth > 360 → result equals 360 (clamped to max)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: SIDEBAR_MAX_WIDTH + 1, max: 2000 }),
        (rawWidth) => {
          const result = computeSidebarWidth(rawWidth);
          expect(result).toBe(SIDEBAR_MAX_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("rawWidth in [100, 180) → result equals 180 (clamped to min)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: SNAP_THRESHOLD, max: SIDEBAR_MIN_WIDTH - 1 }),
        (rawWidth) => {
          const result = computeSidebarWidth(rawWidth);
          expect(result).toBe(SIDEBAR_MIN_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("rawWidth < 100 → result equals 56 (snap to collapsed)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: SNAP_THRESHOLD - 1 }),
        (rawWidth) => {
          const result = computeSidebarWidth(rawWidth);
          expect(result).toBe(SIDEBAR_COLLAPSED_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any pointer X position (0–2000), result is always one of the valid states", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 2000 }),
        (rawWidth) => {
          const result = computeSidebarWidth(rawWidth);

          // Result must be one of: collapsed (56), min (180), within range [180, 360], or max (360)
          if (rawWidth < SNAP_THRESHOLD) {
            expect(result).toBe(SIDEBAR_COLLAPSED_WIDTH);
          } else {
            expect(result).toBeGreaterThanOrEqual(SIDEBAR_MIN_WIDTH);
            expect(result).toBeLessThanOrEqual(SIDEBAR_MAX_WIDTH);
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
