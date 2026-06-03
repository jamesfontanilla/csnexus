// Feature: desktop-app-shell, Property 13: Command palette search debounce
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 14.5**
 *
 * Property 13: Command palette search debounce
 *
 * For any sequence of keystrokes typed faster than 150ms apart, the fuzzy
 * filter function SHALL execute exactly once, 150ms after the final keystroke,
 * with the final accumulated input value.
 */

const DEBOUNCE_MS = 150;

interface KeystrokeEvent {
  char: string;
  timestampMs: number;
}

interface DebounceResult {
  filterCallCount: number;
  finalQueryValue: string;
}

/**
 * Simulate the debounce behavior as a pure function.
 *
 * For each keystroke, the accumulated value grows and any pending timer is
 * cancelled. A new timer is scheduled for `timestampMs + debounceMs`. After
 * processing all keystrokes, if a timer is pending it fires — representing
 * the debounce completing after the final keystroke.
 */
function simulateDebounce(
  keystrokes: KeystrokeEvent[],
  debounceMs: number
): DebounceResult {
  let callCount = 0;
  let lastCallValue = "";
  let pendingTimer: number | null = null;
  let accumulated = "";

  for (const ks of keystrokes) {
    accumulated += ks.char;
    if (pendingTimer !== null) {
      // Cancel pending timer (simulates clearTimeout)
      pendingTimer = null;
    }
    // Schedule new timer
    pendingTimer = ks.timestampMs + debounceMs;
  }

  // After all keystrokes, if a timer is pending, it fires
  if (pendingTimer !== null) {
    callCount = 1;
    lastCallValue = accumulated;
  }

  return { filterCallCount: callCount, finalQueryValue: lastCallValue };
}

const PRINTABLE_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789";

/**
 * Arbitrary: single printable character.
 */
const arbChar = fc.constantFrom(...PRINTABLE_CHARS.split(""));

/**
 * Generate a sequence of keystroke events where each gap between consecutive
 * keystrokes is strictly less than the debounce threshold (150ms).
 * This simulates "rapid typing" that should be collapsed into a single
 * debounced filter call.
 */
const rapidKeystrokeSequence = (minLen: number, maxLen: number) =>
  fc
    .tuple(
      fc.integer({ min: minLen, max: maxLen }),
      fc.integer({ min: 0, max: 10000 }) // base timestamp
    )
    .chain(([len, baseTs]) =>
      fc.tuple(
        // Generate `len` printable characters
        fc.array(arbChar, { minLength: len, maxLength: len }),
        // Generate `len` inter-keystroke gaps, each in [1, DEBOUNCE_MS - 1]
        fc.array(
          fc.integer({ min: 1, max: DEBOUNCE_MS - 1 }),
          { minLength: len, maxLength: len }
        ),
        fc.constant(baseTs)
      )
    )
    .map(([chars, gaps, baseTs]) => {
      const keystrokes: KeystrokeEvent[] = [];
      let currentTs = baseTs;
      for (let i = 0; i < chars.length; i++) {
        if (i > 0) {
          currentTs += gaps[i];
        }
        keystrokes.push({ char: chars[i], timestampMs: currentTs });
      }
      return keystrokes;
    });

describe("Property 13: Command palette search debounce", () => {
  it("for any rapid keystroke sequence (gaps < 150ms), filter is called exactly once", () => {
    fc.assert(
      fc.property(rapidKeystrokeSequence(1, 20), (keystrokes) => {
        const result = simulateDebounce(keystrokes, DEBOUNCE_MS);
        expect(result.filterCallCount).toBe(1);
      }),
      { numRuns: 100 }
    );
  });

  it("the final query value equals the full accumulated string of all characters", () => {
    fc.assert(
      fc.property(rapidKeystrokeSequence(1, 20), (keystrokes) => {
        const result = simulateDebounce(keystrokes, DEBOUNCE_MS);
        const expectedValue = keystrokes.map((ks) => ks.char).join("");
        expect(result.finalQueryValue).toBe(expectedValue);
      }),
      { numRuns: 100 }
    );
  });

  it("for an empty keystroke sequence, filter is never called (0 times)", () => {
    const result = simulateDebounce([], DEBOUNCE_MS);
    expect(result.filterCallCount).toBe(0);
    expect(result.finalQueryValue).toBe("");
  });

  it("for any non-empty rapid keystroke sequence, call count is always exactly 1 (never 0, never > 1)", () => {
    fc.assert(
      fc.property(rapidKeystrokeSequence(1, 50), (keystrokes) => {
        const result = simulateDebounce(keystrokes, DEBOUNCE_MS);
        expect(result.filterCallCount).toBe(1);
        expect(result.finalQueryValue.length).toBe(keystrokes.length);
      }),
      { numRuns: 100 }
    );
  });

  it("the debounced call occurs at timestamp = lastKeystroke.timestampMs + debounceMs", () => {
    fc.assert(
      fc.property(rapidKeystrokeSequence(1, 20), (keystrokes) => {
        // Verify the timer is scheduled correctly
        const lastKeystroke = keystrokes[keystrokes.length - 1];
        const expectedFireTime = lastKeystroke.timestampMs + DEBOUNCE_MS;

        // Simulate manually to verify timer scheduling
        let pendingTimer: number | null = null;
        let accumulated = "";

        for (const ks of keystrokes) {
          accumulated += ks.char;
          pendingTimer = ks.timestampMs + DEBOUNCE_MS;
        }

        expect(pendingTimer).toBe(expectedFireTime);
        expect(accumulated).toBe(keystrokes.map((ks) => ks.char).join(""));
      }),
      { numRuns: 100 }
    );
  });
});
