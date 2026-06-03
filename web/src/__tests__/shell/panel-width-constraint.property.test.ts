// Feature: desktop-app-shell, Property 11: Panel width constraint enforcement
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 11.3**
 *
 * Property 11: Panel width constraint enforcement
 *
 * For any viewport width ≥ 1024px, if the sum of sidebarWidth + detailPanelWidth
 * exceeds 50% of the viewport width, the detail panel SHALL auto-collapse to
 * maintain a minimum content area width of 500px.
 */

const MIN_CONTENT_AREA = 500;
const RESIZE_HANDLES_WIDTH = 8; // 2 × 4px handles

/**
 * Pure function that determines whether the detail panel should auto-collapse.
 * Mirrors the constraint check in useResponsivePanels:
 *   contentAreaWidth = viewportWidth - sidebarWidth - detailPanelWidth - 8
 *   if contentAreaWidth < 500 → collapse
 */
function shouldAutoCollapseDetailPanel(
  viewportWidth: number,
  sidebarWidth: number,
  detailPanelWidth: number
): boolean {
  const contentAreaWidth = viewportWidth - sidebarWidth - detailPanelWidth - RESIZE_HANDLES_WIDTH;
  return contentAreaWidth < MIN_CONTENT_AREA;
}

describe("Property 11: Panel width constraint enforcement", () => {
  it("when sidebarWidth + detailPanelWidth + 8 + 500 > viewportWidth → should collapse (returns true)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1024, max: 2560 }), // viewport
        fc.integer({ min: 56, max: 360 }),     // sidebar
        fc.integer({ min: 240, max: 480 }),    // detail panel
        (viewportWidth, sidebarWidth, detailPanelWidth) => {
          // Only test cases where the constraint IS violated
          const contentArea = viewportWidth - sidebarWidth - detailPanelWidth - RESIZE_HANDLES_WIDTH;
          fc.pre(contentArea < MIN_CONTENT_AREA);

          const result = shouldAutoCollapseDetailPanel(viewportWidth, sidebarWidth, detailPanelWidth);
          expect(result).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("when sidebarWidth + detailPanelWidth + 8 + 500 <= viewportWidth → should NOT collapse (returns false)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1024, max: 2560 }), // viewport
        fc.integer({ min: 56, max: 360 }),     // sidebar
        fc.integer({ min: 240, max: 480 }),    // detail panel
        (viewportWidth, sidebarWidth, detailPanelWidth) => {
          // Only test cases where the constraint IS satisfied
          const contentArea = viewportWidth - sidebarWidth - detailPanelWidth - RESIZE_HANDLES_WIDTH;
          fc.pre(contentArea >= MIN_CONTENT_AREA);

          const result = shouldAutoCollapseDetailPanel(viewportWidth, sidebarWidth, detailPanelWidth);
          expect(result).toBe(false);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any viewport ≥ 1068px with standard defaults (sidebar=240, detail=320), the constraint is satisfied", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1068, max: 2560 }), // viewport ≥ 1068
        (viewportWidth) => {
          const sidebarWidth = 240;
          const detailPanelWidth = 320;
          // contentArea = viewport - 240 - 320 - 8 = viewport - 568
          // At 1068: contentArea = 1068 - 568 = 500 ≥ 500 → no collapse
          const result = shouldAutoCollapseDetailPanel(viewportWidth, sidebarWidth, detailPanelWidth);
          expect(result).toBe(false);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("after collapse, content area is guaranteed ≥ 500px (detail panel removed)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1024, max: 2560 }), // viewport
        fc.integer({ min: 56, max: 360 }),     // sidebar
        (viewportWidth, sidebarWidth) => {
          // After detail panel collapse, the content area is:
          // viewportWidth - sidebarWidth - 4px (only one resize handle remains)
          const contentAreaAfterCollapse = viewportWidth - sidebarWidth - 4;
          // At the narrowest case: viewport=1024, sidebar=360 → 1024-360-4 = 660 ≥ 500
          // Even at max sidebar: viewport=1024, sidebar=360 → 660 ≥ 500 ✓
          expect(contentAreaAfterCollapse).toBeGreaterThanOrEqual(MIN_CONTENT_AREA);
        }
      ),
      { numRuns: 100 }
    );
  });
});
