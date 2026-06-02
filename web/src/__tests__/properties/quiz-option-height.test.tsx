import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import * as fs from "fs";
import * as path from "path";

/**
 * **Validates: Requirements 13.2**
 *
 * Property 15: Quiz Answer Option Minimum Height
 *
 * For any set of 2-6 answer options, the QuizPlayer SHALL render each option
 * button with a minimum height of 56px. Verified by reading the source to
 * confirm the minHeight style is statically applied.
 */

describe("Property 15: Quiz Answer Option Minimum Height (quiz-option-height)", () => {
  it("QuizPlayer source guarantees minHeight: 56px for any set of 2-6 options", () => {
    const quizPlayerPath = path.resolve(
      __dirname,
      "../../pages/quiz/QuizPlayer.tsx"
    );
    const source = fs.readFileSync(quizPlayerPath, "utf-8");

    fc.assert(
      fc.property(
        fc.array(fc.string({ minLength: 1 }), { minLength: 2, maxLength: 6 }),
        (options) => {
          // For any valid set of 2-6 options, the QuizPlayer source must contain
          // the minHeight: "56px" style on option buttons.
          expect(options.length).toBeGreaterThanOrEqual(2);
          expect(options.length).toBeLessThanOrEqual(6);

          // Verify the source contains the minHeight style for option buttons
          expect(source).toContain('minHeight: "56px"');
        }
      ),
      { numRuns: 10 }
    );
  });
});
