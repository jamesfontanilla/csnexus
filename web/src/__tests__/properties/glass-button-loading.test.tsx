import { describe, it, expect, beforeAll, afterEach } from "vitest";
import * as fc from "fast-check";
import { render, cleanup } from "@testing-library/react";
import { GlassButton } from "../../components/GlassButton";

/**
 * **Validates: Requirements 3.3**
 *
 * Property 3: GlassButton Loading State Invariant
 *
 * When GlassButton is rendered with `loading={true}`, the button element
 * must have `aria-busy="true"` and the label text must NOT be present in the DOM.
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

describe("Property 3: GlassButton Loading State Invariant", () => {
  it("sets aria-busy='true' and hides label text when loading", () => {
    fc.assert(
      fc.property(fc.string({ minLength: 1 }), (label) => {
        const { container, queryByText } = render(
          <GlassButton loading>{label}</GlassButton>
        );

        const button = container.querySelector("button");
        expect(button).not.toBeNull();
        expect(button!.getAttribute("aria-busy")).toBe("true");
        expect(queryByText(label)).toBeNull();

        cleanup();
      })
    );
  });
});
