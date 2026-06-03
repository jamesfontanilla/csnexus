// Feature: desktop-app-shell, Property 2: Detail panel resize clamping
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 5.5**
 *
 * Property 2: Detail panel resize clamping
 *
 * For any pointer X position during a detail panel drag operation, the
 * resulting detail panel width SHALL be clamped between 240px and 480px.
 */

const DETAIL_PANEL_MIN_WIDTH = 240;
const DETAIL_PANEL_MAX_WIDTH = 480;

/**
 * Pure function that mirrors the ResizeHandle clamping logic for the detail panel.
 * Unlike the sidebar, the detail panel has no snap-to-collapse behavior —
 * it simply clamps between min and max.
 */
function computeDetailPanelWidth(rawWidth: number): number {
  return Math.max(DETAIL_PANEL_MIN_WIDTH, Math.min(DETAIL_PANEL_MAX_WIDTH, rawWidth));
}

describe("Property 2: Detail panel resize clamping", () => {
  it("rawWidth within [240, 480] → result equals rawWidth exactly", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: DETAIL_PANEL_MIN_WIDTH, max: DETAIL_PANEL_MAX_WIDTH }),
        (rawWidth) => {
          const result = computeDetailPanelWidth(rawWidth);
          expect(result).toBe(rawWidth);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("rawWidth > 480 → result equals 480 (clamped to max)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: DETAIL_PANEL_MAX_WIDTH + 1, max: 2000 }),
        (rawWidth) => {
          const result = computeDetailPanelWidth(rawWidth);
          expect(result).toBe(DETAIL_PANEL_MAX_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("rawWidth < 240 → result equals 240 (clamped to min)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: DETAIL_PANEL_MIN_WIDTH - 1 }),
        (rawWidth) => {
          const result = computeDetailPanelWidth(rawWidth);
          expect(result).toBe(DETAIL_PANEL_MIN_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("no snap behavior — result is never a discrete snap value for any input", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: DETAIL_PANEL_MIN_WIDTH, max: DETAIL_PANEL_MAX_WIDTH }),
        (rawWidth) => {
          const result = computeDetailPanelWidth(rawWidth);
          // Unlike sidebar which snaps to 56px, detail panel always equals
          // the clamped rawWidth — no discrete snap targets
          expect(result).toBe(rawWidth);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any drag delta (−1000 to +1000), result is always within [240, 480]", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: -1000, max: 1000 }),
        (delta) => {
          // Simulate a drag starting from the default detail panel width (320px)
          const startWidth = 320;
          const rawWidth = startWidth + delta;
          const result = computeDetailPanelWidth(rawWidth);

          expect(result).toBeGreaterThanOrEqual(DETAIL_PANEL_MIN_WIDTH);
          expect(result).toBeLessThanOrEqual(DETAIL_PANEL_MAX_WIDTH);
        }
      ),
      { numRuns: 100 }
    );
  });
});
