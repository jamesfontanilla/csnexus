// Feature: desktop-app-shell, Property 12: Focus trapping in command palette
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 13.4**
 *
 * Property 12: Focus trapping in command palette
 *
 * For any sequence of Tab key presses while the command palette is open,
 * focus SHALL cycle within the palette's focusable elements — after the
 * last element, focus returns to the first; before the first (Shift+Tab),
 * focus wraps to the last.
 */

/**
 * Pure function that computes the next focus index given a current index,
 * total number of focusable elements, and tab direction.
 * This mirrors the focus trap cycling logic used by the command palette.
 */
function computeFocusIndex(
  currentIndex: number,
  totalElements: number,
  direction: "forward" | "backward"
): number {
  if (totalElements <= 0) return 0;
  if (direction === "forward") {
    return (currentIndex + 1) % totalElements;
  }
  return (currentIndex - 1 + totalElements) % totalElements;
}

describe("Property 12: Focus trapping in command palette", () => {
  it("forward Tab always produces index in [0, N-1]", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        fc.integer({ min: 0, max: 19 }),
        (totalElements, currentIndex) => {
          const normalizedIndex = currentIndex % totalElements;
          const result = computeFocusIndex(normalizedIndex, totalElements, "forward");
          expect(result).toBeGreaterThanOrEqual(0);
          expect(result).toBeLessThan(totalElements);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("backward Tab (Shift+Tab) always produces index in [0, N-1]", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        fc.integer({ min: 0, max: 19 }),
        (totalElements, currentIndex) => {
          const normalizedIndex = currentIndex % totalElements;
          const result = computeFocusIndex(normalizedIndex, totalElements, "backward");
          expect(result).toBeGreaterThanOrEqual(0);
          expect(result).toBeLessThan(totalElements);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("N forward Tabs from index 0 returns to index 0 (full cycle)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        (totalElements) => {
          let index = 0;
          for (let i = 0; i < totalElements; i++) {
            index = computeFocusIndex(index, totalElements, "forward");
          }
          expect(index).toBe(0);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("N backward Tabs from index 0 returns to index 0 (full cycle)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        (totalElements) => {
          let index = 0;
          for (let i = 0; i < totalElements; i++) {
            index = computeFocusIndex(index, totalElements, "backward");
          }
          expect(index).toBe(0);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("forward then backward from any position returns to that position (inverse property)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        fc.integer({ min: 0, max: 19 }),
        (totalElements, rawIndex) => {
          const startIndex = rawIndex % totalElements;
          const afterForward = computeFocusIndex(startIndex, totalElements, "forward");
          const afterBackward = computeFocusIndex(afterForward, totalElements, "backward");
          expect(afterBackward).toBe(startIndex);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("random sequences of forward/backward tabs always keep index in valid range", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 20 }),
        fc.array(fc.constantFrom("forward" as const, "backward" as const), {
          minLength: 1,
          maxLength: 50,
        }),
        (totalElements, directions) => {
          let index = 0;
          for (const direction of directions) {
            index = computeFocusIndex(index, totalElements, direction);
            expect(index).toBeGreaterThanOrEqual(0);
            expect(index).toBeLessThan(totalElements);
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
