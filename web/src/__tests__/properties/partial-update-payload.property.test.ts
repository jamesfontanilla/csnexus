import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { buildPatchPayload } from "../../pages/settings/ProfileSection";

/**
 * **Validates: Requirements 2.8**
 *
 * Property 3: Partial Update Payload Correctness
 *
 * For any subset of profile fields (display_name, username, tz_name) that a
 * user modifies, the PATCH request payload SHALL contain exactly those fields
 * and no others.
 */

// --- Arbitraries ---

const profileArb = fc.record({
  display_name: fc.string({ minLength: 1, maxLength: 50 }),
  username: fc.string({ minLength: 1, maxLength: 30 }),
  tz_name: fc.string({ minLength: 1, maxLength: 50 }),
});

// --- Tests ---

describe("Property 3: Partial Update Payload Correctness", () => {
  it("payload keys match exactly the fields where original !== current", () => {
    fc.assert(
      fc.property(profileArb, profileArb, (original, current) => {
        const payload = buildPatchPayload(original, current);

        const expectedKeys = (
          ["display_name", "username", "tz_name"] as const
        ).filter((key) => original[key] !== current[key]);

        // Payload contains exactly the modified fields and no others
        expect(Object.keys(payload).sort()).toEqual([...expectedKeys].sort());
      }),
      { numRuns: 100 }
    );
  });

  it("payload values equal the current (modified) values for changed fields", () => {
    fc.assert(
      fc.property(profileArb, profileArb, (original, current) => {
        const payload = buildPatchPayload(original, current);

        for (const key of Object.keys(payload)) {
          expect(payload[key]).toBe(
            current[key as keyof typeof current]
          );
        }
      }),
      { numRuns: 100 }
    );
  });
});
