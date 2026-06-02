import { describe, it, expect, vi, beforeEach } from "vitest";
import * as fc from "fast-check";
import { render } from "@testing-library/react";
import { GlassButton } from "../../components/GlassButton";

/**
 * **Validates: Requirements 3.6**
 *
 * Property 4: GlassButton Cursor Invariant
 *
 * When the GlassButton `loading` prop is true OR the GlassButton is explicitly
 * disabled, the button SHALL display `cursor: not-allowed`.
 */

function mockMatchMedia(matches: boolean) {
  const listeners: Array<(e: MediaQueryListEvent) => void> = [];
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: (_event: string, handler: (e: MediaQueryListEvent) => void) => {
        listeners.push(handler);
      },
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

describe("Property 4: GlassButton Cursor Invariant", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  it("displays cursor: not-allowed when loading or disabled is true", () => {
    fc.assert(
      fc.property(fc.boolean(), fc.boolean(), (loading, disabled) => {
        const shouldBeNotAllowed = loading || disabled;

        if (!shouldBeNotAllowed) return; // skip when both are false — property only applies when either is true

        const { container } = render(
          <GlassButton loading={loading} disabled={disabled}>
            Click me
          </GlassButton>
        );

        const button = container.querySelector("button");
        expect(button).not.toBeNull();
        expect(button!.style.cursor).toBe("not-allowed");
      })
    );
  });

  it("does not display cursor: not-allowed when both loading and disabled are false", () => {
    const { container } = render(
      <GlassButton loading={false} disabled={false}>
        Click me
      </GlassButton>
    );

    const button = container.querySelector("button");
    expect(button).not.toBeNull();
    expect(button!.style.cursor).not.toBe("not-allowed");
  });
});
