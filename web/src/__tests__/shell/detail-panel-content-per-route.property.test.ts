// Feature: desktop-app-shell, Property 4: Detail panel contextual content per route
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import {
  PAGE_CONTEXTS,
  resolvePageContext,
} from "../../context/PageContextRegistry";

/**
 * **Validates: Requirements 5.7**
 *
 * Property 4: Detail panel contextual content per route
 *
 * For any route that has a PageContext with a defined `detailPanelComponent`,
 * the DetailPanel SHALL render the component resolved from that dynamic import.
 *
 * We verify:
 * 1. Routes with `showDetailPanel: true` AND `detailPanelComponent` defined →
 *    the component factory is a callable function returning a Promise.
 * 2. Routes without `detailPanelComponent` → the field is undefined/absent.
 * 3. `resolvePageContext` returns consistent results for any registered route.
 */

// Partition routes into those WITH and WITHOUT a detailPanelComponent
const allRoutePatterns = Object.keys(PAGE_CONTEXTS);

const routesWithDetailComponent = allRoutePatterns.filter(
  (pattern) => PAGE_CONTEXTS[pattern].detailPanelComponent != null
);

const routesWithoutDetailComponent = allRoutePatterns.filter(
  (pattern) => PAGE_CONTEXTS[pattern].detailPanelComponent == null
);

/**
 * Generate a concrete pathname from a route pattern by replacing
 * `:param` segments with realistic placeholder values.
 */
function instantiatePattern(pattern: string): string {
  return pattern.replace(/:([a-zA-Z]+)/g, "test-param-value");
}

describe("Property 4: Detail panel contextual content per route", () => {
  it("routes with detailPanelComponent have a callable factory that returns a Promise", () => {
    // Use constantFrom to pick random routes that have detailPanelComponent
    fc.assert(
      fc.property(
        fc.constantFrom(...routesWithDetailComponent),
        (routePattern) => {
          const context = PAGE_CONTEXTS[routePattern];

          // detailPanelComponent must be defined
          expect(context.detailPanelComponent).toBeDefined();
          // It must be a function
          expect(typeof context.detailPanelComponent).toBe("function");
          // Calling it must return a thenable (Promise)
          const result = context.detailPanelComponent!();
          expect(result).toBeDefined();
          expect(typeof result.then).toBe("function");
        }
      ),
      { numRuns: 100 }
    );
  });

  it("routes without detailPanelComponent have it undefined", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...routesWithoutDetailComponent),
        (routePattern) => {
          const context = PAGE_CONTEXTS[routePattern];

          // detailPanelComponent must be undefined/null
          expect(context.detailPanelComponent).toBeUndefined();
        }
      ),
      { numRuns: 100 }
    );
  });

  it("resolvePageContext returns consistent PageContext for any registered route pattern", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...allRoutePatterns),
        (routePattern) => {
          const pathname = instantiatePattern(routePattern);
          const resolved = resolvePageContext(pathname);
          const expected = PAGE_CONTEXTS[routePattern];

          // The resolved context should match the registered one
          expect(resolved.layoutMode).toBe(expected.layoutMode);
          expect(resolved.showDetailPanel).toBe(expected.showDetailPanel);
          expect(resolved.autoFocusMode).toBe(expected.autoFocusMode);
          expect(resolved.centeredMaxWidth).toBe(expected.centeredMaxWidth);
          expect(resolved.sidebarWidth).toBe(expected.sidebarWidth);

          // Detail panel component consistency
          if (expected.detailPanelComponent) {
            expect(resolved.detailPanelComponent).toBeDefined();
            expect(typeof resolved.detailPanelComponent).toBe("function");
          } else {
            expect(resolved.detailPanelComponent).toBeUndefined();
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  it("routes with showDetailPanel: true always define a detailPanelComponent or are intentionally panel-less", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...allRoutePatterns),
        (routePattern) => {
          const context = PAGE_CONTEXTS[routePattern];

          if (context.showDetailPanel && context.detailPanelComponent) {
            // If showDetailPanel is true AND component is defined,
            // the factory must be callable and return a Promise
            expect(typeof context.detailPanelComponent).toBe("function");
            const result = context.detailPanelComponent();
            expect(typeof result.then).toBe("function");
          } else if (!context.showDetailPanel) {
            // If showDetailPanel is false/undefined, detailPanelComponent should not be set
            expect(context.detailPanelComponent).toBeUndefined();
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
