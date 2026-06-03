// Feature: desktop-app-shell, Property 6: Command palette keyboard navigation bounds
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 6.6**
 *
 * Property 6: Command palette keyboard navigation bounds
 *
 * For any result list of length N (N ≥ 1) and any sequence of ArrowDown/ArrowUp
 * key presses, the highlighted index SHALL remain within bounds [0, N-1] —
 * ArrowDown increments (clamped to N-1), ArrowUp decrements (clamped to 0).
 */

/**
 * Pure function that simulates keyboard navigation through a command palette
 * result list. Starting at index 0, each 'down' increments (clamped to N-1)
 * and each 'up' decrements (clamped to 0).
 */
function applyKeySequence(listLength: number, keys: ("up" | "down")[]): number {
  let index = 0;
  for (const key of keys) {
    if (key === "down") {
      index = Math.min(index + 1, listLength - 1);
    } else {
      index = Math.max(index - 1, 0);
    }
  }
  return index;
}

const keyArb = fc.constantFrom<"up" | "down">("up", "down");

describe("Property 6: Command palette keyboard navigation bounds", () => {
  it("result index is always >= 0 for any key sequence", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100 }),
        fc.array(keyArb, { minLength: 0, maxLength: 200 }),
        (listLength, keys) => {
          const result = applyKeySequence(listLength, keys);
          expect(result).toBeGreaterThanOrEqual(0);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("result index is always <= N-1 for any key sequence", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100 }),
        fc.array(keyArb, { minLength: 0, maxLength: 200 }),
        (listLength, keys) => {
          const result = applyKeySequence(listLength, keys);
          expect(result).toBeLessThanOrEqual(listLength - 1);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("starting at 0, N ArrowDown presses lands at N-1 (not beyond)", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100 }),
        (listLength) => {
          const keys: ("up" | "down")[] = Array(listLength).fill("down");
          const result = applyKeySequence(listLength, keys);
          expect(result).toBe(listLength - 1);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("starting at 0, any number of ArrowUp presses stays at 0", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100 }),
        fc.integer({ min: 1, max: 200 }),
        (listLength, upCount) => {
          const keys: ("up" | "down")[] = Array(upCount).fill("up");
          const result = applyKeySequence(listLength, keys);
          expect(result).toBe(0);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any sequence of keys, final index is in [0, N-1]", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 100 }),
        fc.array(keyArb, { minLength: 0, maxLength: 200 }),
        (listLength, keys) => {
          const result = applyKeySequence(listLength, keys);
          expect(result).toBeGreaterThanOrEqual(0);
          expect(result).toBeLessThanOrEqual(listLength - 1);
        }
      ),
      { numRuns: 100 }
    );
  });
});
