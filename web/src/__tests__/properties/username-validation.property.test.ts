import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { isValidUsername } from "../../pages/settings/ProfileSection";

/**
 * **Validates: Requirements 2.2**
 *
 * Property 2: Username Validation Consistency
 *
 * For any string, the frontend username validation function SHALL accept
 * the string if and only if it matches the pattern `^[A-Za-z][A-Za-z0-9_]{2,29}$`.
 */

const USERNAME_RE = /^[A-Za-z][A-Za-z0-9_]{2,29}$/;

describe("Property 2: Username Validation Consistency", () => {
  it("isValidUsername(s) returns true iff s matches the canonical regex", () => {
    fc.assert(
      fc.property(fc.string(), (s) => {
        const expected = USERNAME_RE.test(s);
        const actual = isValidUsername(s);
        expect(actual).toBe(expected);
      }),
      { numRuns: 100 }
    );
  });
});
