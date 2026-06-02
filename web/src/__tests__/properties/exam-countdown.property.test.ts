import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { daysUntil } from "../../pages/settings/StudySection";

/**
 * **Validates: Requirements 3.4**
 *
 * Property 4: Exam Countdown Calculation
 *
 * For any target exam date that is today or in the future, the displayed
 * countdown SHALL equal the non-negative integer difference in days between
 * the target date and today.
 */

// --- Helpers ---

/** Format a Date as an ISO date string (YYYY-MM-DD) */
function toISO(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/** Compute expected days between two dates normalized to midnight */
function expectedDaysDiff(targetISO: string, today: Date): number {
  const target = new Date(targetISO + "T00:00:00");
  const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const diffMs = target.getTime() - todayStart.getTime();
  return Math.max(0, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
}

// --- Arbitraries ---

/** Generate a "today" date within a reasonable range (2000–2099) */
const todayArb: fc.Arbitrary<Date> = fc
  .integer({ min: 0, max: 36524 }) // ~100 years of days
  .map((days) => {
    const base = new Date(2000, 0, 1);
    base.setDate(base.getDate() + days);
    return base;
  });

/** Generate a future offset in days (0 to 3650 = ~10 years ahead) */
const futureOffsetArb = fc.integer({ min: 0, max: 3650 });

/** Generate a past offset in days (1 to 3650 = ~10 years behind) */
const pastOffsetArb = fc.integer({ min: 1, max: 3650 });

// --- Tests ---

describe("Property 4: Exam Countdown Calculation", () => {
  it("for any future or today target date, daysUntil equals non-negative integer difference in days", () => {
    fc.assert(
      fc.property(todayArb, futureOffsetArb, (today, offset) => {
        // Generate target date that is >= today (offset 0 means same day)
        const target = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        target.setDate(target.getDate() + offset);
        const targetISO = toISO(target);

        const result = daysUntil(targetISO, today);

        // Result must be a non-negative integer
        expect(result).toBeGreaterThanOrEqual(0);
        expect(Number.isInteger(result)).toBe(true);

        // Result must equal the expected day difference
        expect(result).toBe(expectedDaysDiff(targetISO, today));

        // Result must equal the offset (since target = today + offset days)
        expect(result).toBe(offset);
      }),
      { numRuns: 100 }
    );
  });

  it("for any past target date, daysUntil is clamped to 0", () => {
    fc.assert(
      fc.property(todayArb, pastOffsetArb, (today, offset) => {
        // Generate target date that is strictly before today
        const target = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        target.setDate(target.getDate() - offset);
        const targetISO = toISO(target);

        const result = daysUntil(targetISO, today);

        // Past dates must always return 0 (clamped to non-negative)
        expect(result).toBe(0);
      }),
      { numRuns: 100 }
    );
  });
});
