import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { isValidPassword } from "../../pages/settings/AccountSection";

/**
 * **Validates: Requirements 5.2**
 *
 * Property 5: Password Validation Consistency
 *
 * For any string, the frontend password validation function SHALL reject
 * the string if and only if it fails at least one of: length < 8, no
 * uppercase letter, no lowercase letter, no digit, no symbol from the
 * allowed set.
 */

describe("Property 5: Password Validation Consistency", () => {
  it("isValidPassword(s) returns true iff s passes all five rules", () => {
    fc.assert(
      fc.property(fc.string(), (s) => {
        const hasMinLength = s.length >= 8;
        const hasUppercase = /[A-Z]/.test(s);
        const hasLowercase = /[a-z]/.test(s);
        const hasDigit = /[0-9]/.test(s);
        const hasSymbol = /[^A-Za-z0-9\s]/.test(s);

        const expected =
          hasMinLength && hasUppercase && hasLowercase && hasDigit && hasSymbol;
        const actual = isValidPassword(s);

        expect(actual).toBe(expected);
      }),
      { numRuns: 100 }
    );
  });
});
