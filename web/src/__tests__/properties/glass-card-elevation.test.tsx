import { describe, it, expect, beforeAll } from "vitest";
import * as fc from "fast-check";
import { render } from "@testing-library/react";
import { GlassCard } from "../../components/GlassCard";

/**
 * **Validates: Requirements 2.1**
 *
 * Property 2: GlassCard Elevation Produces Distinct Visual Levels
 *
 * For any pair of distinct elevation values, the rendered GlassCard
 * must produce different class names or inline style values, ensuring
 * each elevation level is visually distinguishable.
 */

type Elevation = "flat" | "raised" | "floating";

beforeAll(() => {
  // Mock window.matchMedia for jsdom (required by useReducedMotion)
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

describe("Property 2: GlassCard Elevation Produces Distinct Visual Levels", () => {
  it("any two distinct elevations produce different class names or inline styles", () => {
    fc.assert(
      fc.property(
        fc.uniqueArray(fc.constantFrom<Elevation>("flat", "raised", "floating"), {
          minLength: 2,
          maxLength: 2,
        }),
        ([elevationA, elevationB]) => {
          const { container: containerA } = render(
            <GlassCard elevation={elevationA}>A</GlassCard>
          );
          const { container: containerB } = render(
            <GlassCard elevation={elevationB}>B</GlassCard>
          );

          const elA = containerA.firstElementChild as HTMLElement;
          const elB = containerB.firstElementChild as HTMLElement;

          const classA = elA.className;
          const classB = elB.className;
          const styleA = elA.getAttribute("style") ?? "";
          const styleB = elB.getAttribute("style") ?? "";

          // At least one of class or style must differ between the two elevations
          const classesDiffer = classA !== classB;
          const stylesDiffer = styleA !== styleB;

          expect(classesDiffer || stylesDiffer).toBe(true);
        }
      )
    );
  });
});
