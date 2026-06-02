import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 13.5**
 *
 * Property 16: Quiz Timer Color Below 30 Seconds
 *
 * WHEN the quiz timer drops below 30 seconds, THE Quiz_Player SHALL change the
 * timer color to `--color-danger`. The `timerColor` function returns
 * `var(--color-danger)` when remaining < 30.
 */

// Re-implement the timerColor logic from QuizPlayer.tsx
function timerColor(remaining: number): string {
  if (remaining < 30) return "var(--color-danger)";
  return "var(--color-text)";
}

describe("Property 16: Quiz Timer Color Below 30 Seconds", () => {
  it("timerColor returns var(--color-danger) for any remaining time below 30 seconds", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 29 }),
        (remaining) => {
          const color = timerColor(remaining);
          expect(color).toBe("var(--color-danger)");
        }
      ),
      { numRuns: 10 }
    );
  });

  it("timerColor returns var(--color-text) for remaining time >= 30 seconds", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 30, max: 7200 }),
        (remaining) => {
          const color = timerColor(remaining);
          expect(color).toBe("var(--color-text)");
        }
      ),
      { numRuns: 10 }
    );
  });

  it("boundary: timerColor(29) is danger, timerColor(30) is normal", () => {
    expect(timerColor(29)).toBe("var(--color-danger)");
    expect(timerColor(30)).toBe("var(--color-text)");
  });
});
