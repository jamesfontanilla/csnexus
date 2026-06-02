import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { GlassModal } from "../../components/GlassModal";

/**
 * **Validates: Requirements 6.3, 17.6**
 *
 * Property 9: GlassModal Focus Trap Completeness
 *
 * When GlassModal is open with N focusable buttons inside:
 * - Tab from the last button wraps focus to the first button
 * - Shift+Tab from the first button wraps focus to the last button
 */

beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }),
  });
});

afterEach(() => {
  cleanup();
});

describe("Property 9: GlassModal Focus Trap Completeness", () => {
  it("Tab from last button wraps focus to first button", () => {
    fc.assert(
      fc.property(fc.integer({ min: 1, max: 8 }), (n) => {
        const { container } = render(
          <GlassModal isOpen title="Test" onClose={() => {}}>
            {Array.from({ length: n }, (_, i) => (
              <button key={i} data-testid={`btn-${i}`}>
                Button {i}
              </button>
            ))}
          </GlassModal>
        );

        const buttons = container.querySelectorAll("button");
        const firstButton = buttons[0];
        const lastButton = buttons[buttons.length - 1];

        // Focus the last button
        lastButton.focus();
        expect(document.activeElement).toBe(lastButton);

        // Dispatch Tab keydown on document (where useFocusTrap listens)
        const tabEvent = new KeyboardEvent("keydown", {
          key: "Tab",
          bubbles: true,
          cancelable: true,
        });
        document.dispatchEvent(tabEvent);

        // Focus should wrap to the first button
        expect(document.activeElement).toBe(firstButton);

        cleanup();
      })
    );
  });

  it("Shift+Tab from first button wraps focus to last button", () => {
    fc.assert(
      fc.property(fc.integer({ min: 1, max: 8 }), (n) => {
        const { container } = render(
          <GlassModal isOpen title="Test" onClose={() => {}}>
            {Array.from({ length: n }, (_, i) => (
              <button key={i} data-testid={`btn-${i}`}>
                Button {i}
              </button>
            ))}
          </GlassModal>
        );

        const buttons = container.querySelectorAll("button");
        const firstButton = buttons[0];
        const lastButton = buttons[buttons.length - 1];

        // Focus the first button
        firstButton.focus();
        expect(document.activeElement).toBe(firstButton);

        // Dispatch Shift+Tab keydown on document (where useFocusTrap listens)
        const shiftTabEvent = new KeyboardEvent("keydown", {
          key: "Tab",
          shiftKey: true,
          bubbles: true,
          cancelable: true,
        });
        document.dispatchEvent(shiftTabEvent);

        // Focus should wrap to the last button
        expect(document.activeElement).toBe(lastButton);

        cleanup();
      })
    );
  });
});
