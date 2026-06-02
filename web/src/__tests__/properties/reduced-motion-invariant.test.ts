import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { makeReducedVariants } from "../../design-system/motion";

/**
 * **Validates: Requirements 16.7, 17.5**
 *
 * Property 18: Reduced-Motion Duration Invariant
 *
 * When `makeReducedVariants(variants, true)` is called with reduced motion enabled,
 * the resulting transition duration must be ≤ 0.08 (80ms) and all spatial transform
 * values (x, y, scale) must be stripped from variant objects.
 */

describe("Property 18: Reduced-Motion Duration Invariant", () => {
  const variantObjectArb = fc.record({
    opacity: fc.oneof(fc.double({ min: 0, max: 1, noNaN: true }), fc.constant(undefined)),
    x: fc.oneof(fc.double({ min: -500, max: 500, noNaN: true }), fc.constant(undefined)),
    y: fc.oneof(fc.double({ min: -500, max: 500, noNaN: true }), fc.constant(undefined)),
    scale: fc.oneof(fc.double({ min: 0.1, max: 3, noNaN: true }), fc.constant(undefined)),
  });

  const variantsArb = fc.record({
    initial: variantObjectArb,
    animate: variantObjectArb,
    exit: fc.oneof(variantObjectArb, fc.constant(undefined)),
    transition: fc.record({
      duration: fc.double({ min: 0.01, max: 5, noNaN: true }),
    }),
  });

  it("effective duration is ≤ 0.08 (80ms) when reduced motion is active", () => {
    fc.assert(
      fc.property(variantsArb, (variants) => {
        const result = makeReducedVariants(variants, true);
        const transition = result.transition as { duration: number } | undefined;

        expect(transition).toBeDefined();
        expect(transition!.duration).toBeLessThanOrEqual(0.08);
      })
    );
  });

  it("x, y, and scale values are stripped from all variant objects", () => {
    fc.assert(
      fc.property(variantsArb, (variants) => {
        const result = makeReducedVariants(variants, true);

        for (const [key, value] of Object.entries(result)) {
          if (key === "transition") continue;
          if (typeof value === "object" && value !== null) {
            const obj = value as Record<string, unknown>;
            expect(obj).not.toHaveProperty("x");
            expect(obj).not.toHaveProperty("y");
            expect(obj).not.toHaveProperty("scale");
          }
        }
      })
    );
  });

  it("non-spatial properties (e.g., opacity) are preserved", () => {
    fc.assert(
      fc.property(variantsArb, (variants) => {
        const result = makeReducedVariants(variants, true);

        for (const [key, value] of Object.entries(result)) {
          if (key === "transition") continue;
          if (typeof value === "object" && value !== null) {
            const original = variants[key as keyof typeof variants] as
              | Record<string, unknown>
              | undefined;
            if (original && "opacity" in original && original.opacity !== undefined) {
              expect((value as Record<string, unknown>).opacity).toBe(original.opacity);
            }
          }
        }
      })
    );
  });

  it("returns variants unchanged when reduced motion is false", () => {
    fc.assert(
      fc.property(variantsArb, (variants) => {
        const result = makeReducedVariants(variants, false);
        expect(result).toBe(variants);
      })
    );
  });
});
