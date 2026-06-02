import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, act } from "@testing-library/react";
import { ToastProvider, useToast, ToastVariant } from "../../context/ToastContext";

/**
 * **Validates: Requirements 10.5**
 *
 * Property 14: Toast Variant Color Mapping
 *
 * THE Toast component SHALL support `success`, `error`, `warning`, and `info` variants
 * using the semantic color tokens for the left border accent and icon.
 * Each variant must render with the corresponding semantic color token.
 */

const expectedColorMap: Record<string, string> = {
  success: "var(--color-success)",
  error: "var(--color-danger)",
  warning: "var(--color-warning, #e6a817)",
  info: "var(--color-accent)",
};

function mockMatchMedia(matches: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

// Helper component that triggers a toast of the given variant via a button click
function ToastTrigger({ variant }: { variant: ToastVariant }) {
  const toast = useToast();
  return (
    <button data-testid="trigger" onClick={() => toast[variant](`Test ${variant} message`)}>
      trigger
    </button>
  );
}

describe("Property 14: Toast Variant Color Mapping", () => {
  beforeEach(() => {
    mockMatchMedia(false);
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("each toast variant renders with the corresponding semantic color token", () => {
    fc.assert(
      fc.property(
        fc.constantFrom("success", "error", "warning", "info"),
        (variant) => {
          const { container, unmount } = render(
            <ToastProvider>
              <ToastTrigger variant={variant as ToastVariant} />
            </ToastProvider>
          );

          // Trigger the toast
          act(() => {
            container.querySelector<HTMLButtonElement>('[data-testid="trigger"]')!.click();
          });

          // Find the toast element by its role
          const role = variant === "error" ? "alert" : "status";
          const toastEl = container.querySelector(`[role="${role}"]`) as HTMLElement;
          expect(toastEl).not.toBeNull();
          expect(toastEl.style.color).toBe(expectedColorMap[variant]);

          unmount();
        }
      ),
      { numRuns: 20 }
    );
  });
});
