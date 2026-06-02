import { describe, it, expect, beforeAll, afterEach, vi } from "vitest";
import * as fc from "fast-check";
import { render, cleanup, act } from "@testing-library/react";
import { ToastProvider, useToast } from "../../context/ToastContext";

/**
 * **Validates: Requirements 10.2**
 *
 * Property 13: Toast Stacking Gap Invariant
 *
 * When N toasts are rendered (1 ≤ N ≤ 5), the toast container must use
 * `gap: var(--space-3)` in its inline style to maintain consistent vertical
 * spacing between stacked toasts.
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

// Capture toast API from inside the provider
let capturedToast: ReturnType<typeof useToast> | null = null;

function ToastCapture() {
  capturedToast = useToast();
  return null;
}

describe("Property 13: Toast Stacking Gap Invariant", () => {
  it("toast container has gap: var(--space-3) for any number of toasts", () => {
    // Mock setInterval to prevent toast auto-dismiss timers from running
    const intervalIds: ReturnType<typeof setInterval>[] = [];
    vi.spyOn(global, "setInterval").mockImplementation(((
      _handler: TimerHandler,
      _timeout?: number
    ) => {
      const id = 999 as unknown as ReturnType<typeof setInterval>;
      intervalIds.push(id);
      return id;
    }) as unknown as typeof setInterval);

    try {
      fc.assert(
        fc.property(fc.integer({ min: 1, max: 5 }), (n) => {
          capturedToast = null;

          const { baseElement } = render(
            <ToastProvider>
              <ToastCapture />
            </ToastProvider>
          );

          // Add N toasts
          act(() => {
            for (let i = 0; i < n; i++) {
              capturedToast!.info(`Toast message ${i}`);
            }
          });

          // The toast container is the div with aria-live="polite"
          const container = baseElement.querySelector('[aria-live="polite"]');
          expect(container).not.toBeNull();

          const style = (container as HTMLElement).style;
          expect(style.gap).toBe("var(--space-3)");

          cleanup();
        }),
        { numRuns: 20 }
      );
    } finally {
      vi.restoreAllMocks();
    }
  });
});
