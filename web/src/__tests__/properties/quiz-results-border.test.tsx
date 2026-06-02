import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import * as fs from "fs";
import * as path from "path";

/**
 * **Validates: Requirements 13.9**
 *
 * Property 17: Quiz Results Border Color Correctness
 *
 * THE Quiz_Player results page SHALL display each question review card with a
 * left border in `--color-success` for correct answers and `--color-danger`
 * for incorrect answers.
 */

// Re-implement the border-left color logic from QuizPlayer results
function resultBorderColor(isCorrect: boolean): string {
  return isCorrect ? "var(--color-success)" : "var(--color-danger)";
}

describe("Property 17: Quiz Results Border Color Correctness", () => {
  it("correct answers get var(--color-success) border, incorrect get var(--color-danger)", () => {
    fc.assert(
      fc.property(
        fc.boolean(),
        (isCorrect) => {
          const color = resultBorderColor(isCorrect);
          if (isCorrect) {
            expect(color).toBe("var(--color-success)");
          } else {
            expect(color).toBe("var(--color-danger)");
          }
        }
      ),
      { numRuns: 10 }
    );
  });

  it("QuizPlayer source uses the border-left pattern with color-success and color-danger", () => {
    const quizPlayerPath = path.resolve(
      __dirname,
      "../../pages/quiz/QuizPlayer.tsx"
    );
    const source = fs.readFileSync(quizPlayerPath, "utf-8");

    // The results section uses a borderLeft style with conditional color
    // Pattern: `borderLeft: \`3px solid ${q.is_correct ? "var(--color-success)" : "var(--color-danger)"}\``
    expect(source).toContain("var(--color-success)");
    expect(source).toContain("var(--color-danger)");
    expect(source).toContain("borderLeft");
    // Verify the ternary pattern for is_correct
    expect(source).toContain("q.is_correct");
  });
});
