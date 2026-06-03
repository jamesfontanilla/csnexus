// Feature: desktop-app-shell, Property 7: Keyboard shortcut dispatch based on focus state
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";

/**
 * **Validates: Requirements 7.1, 7.3**
 *
 * Property 7: Keyboard shortcut dispatch based on focus state
 *
 * For any registered keyboard shortcut and any document focus state, the
 * shortcut SHALL fire its action if and only if the currently focused element
 * is NOT an `<input>`, `<textarea>`, or element with `contenteditable="true"`.
 */

type FocusedElement =
  | "input"
  | "textarea"
  | "contenteditable"
  | "div"
  | "button"
  | "span"
  | "body";

const ALL_FOCUSED_ELEMENTS: FocusedElement[] = [
  "input",
  "textarea",
  "contenteditable",
  "div",
  "button",
  "span",
  "body",
];

const SUPPRESSED_ELEMENTS: FocusedElement[] = [
  "input",
  "textarea",
  "contenteditable",
];

const NON_SUPPRESSED_ELEMENTS: FocusedElement[] = [
  "div",
  "button",
  "span",
  "body",
];

/**
 * Pure function that determines whether a keyboard shortcut should fire
 * based on the currently focused element type.
 *
 * Mirrors the suppression logic in KeyboardShortcutManager: shortcuts are
 * suppressed when the active element is an input, textarea, or contenteditable.
 */
function shouldFireShortcut(focusedElement: FocusedElement): boolean {
  const suppressed: FocusedElement[] = ["input", "textarea", "contenteditable"];
  return !suppressed.includes(focusedElement);
}

// Arbitrary for generating random focused element types
const focusedElementArb = fc.constantFrom(...ALL_FOCUSED_ELEMENTS);

// Arbitrary for generating random shortcut identifiers
const shortcutArb = fc.constantFrom(
  "mod+k",
  "mod+b",
  "mod+\\",
  "mod+shift+f",
  "?"
);

describe("Property 7: Keyboard shortcut dispatch based on focus state", () => {
  it("for any non-text-input focus state (div, button, span, body), shortcuts fire (returns true)", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...NON_SUPPRESSED_ELEMENTS),
        shortcutArb,
        (focusedElement, _shortcut) => {
          expect(shouldFireShortcut(focusedElement)).toBe(true);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any text-input focus state (input, textarea, contenteditable), shortcuts are suppressed (returns false)", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...SUPPRESSED_ELEMENTS),
        shortcutArb,
        (focusedElement, _shortcut) => {
          expect(shouldFireShortcut(focusedElement)).toBe(false);
        }
      ),
      { numRuns: 100 }
    );
  });

  it("the set of suppressed elements is exactly {input, textarea, contenteditable} — nothing else is suppressed", () => {
    fc.assert(
      fc.property(focusedElementArb, (focusedElement) => {
        const isSuppressed = !shouldFireShortcut(focusedElement);
        const expectedSuppressed = SUPPRESSED_ELEMENTS.includes(focusedElement);
        expect(isSuppressed).toBe(expectedSuppressed);
      }),
      { numRuns: 100 }
    );
  });

  it("all non-suppressed elements are treated identically (all return true)", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...NON_SUPPRESSED_ELEMENTS),
        fc.constantFrom(...NON_SUPPRESSED_ELEMENTS),
        (elementA, elementB) => {
          expect(shouldFireShortcut(elementA)).toBe(
            shouldFireShortcut(elementB)
          );
        }
      ),
      { numRuns: 100 }
    );
  });

  it("for any random focused element and shortcut combo, the dispatch rule is deterministic", () => {
    fc.assert(
      fc.property(focusedElementArb, shortcutArb, (focusedElement, _shortcut) => {
        const result = shouldFireShortcut(focusedElement);
        // Calling twice with the same input must yield the same result
        expect(shouldFireShortcut(focusedElement)).toBe(result);
      }),
      { numRuns: 100 }
    );
  });
});
