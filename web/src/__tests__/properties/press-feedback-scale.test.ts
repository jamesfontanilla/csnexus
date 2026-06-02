import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { pressFeedback } from "../../design-system/motion";

/**
 * **Validates: Requirements 16.4**
 *
 * Property 20: Press Feedback Scale Values
 *
 * Asserts that pressFeedback.whileTap.scale === 0.97
 * and pressFeedback.whileHover.scale === 1.02
 */

describe("Property 20: Press Feedback Scale Values", () => {
  it("whileTap scale is exactly 0.97 and whileHover scale is exactly 1.02", () => {
    fc.assert(
      fc.property(fc.constant(null), () => {
        expect(pressFeedback.whileTap.scale).toBe(0.97);
        expect(pressFeedback.whileHover.scale).toBe(1.02);
      })
    );
  });
});
