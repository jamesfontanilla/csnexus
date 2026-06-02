import { describe, it, expect, vi, beforeEach } from "vitest";
import * as fc from "fast-check";
import { render } from "@testing-library/react";
import { GlassBadge } from "../../components/GlassBadge";

/**
 * **Validates: Requirements 7.4**
 *
 * Property 11: GlassBadge Color Variant Token Mapping
 *
 * THE GlassBadge SHALL support `color` variants mapped to the semantic color tokens:
 * `success`, `warning`, `danger`, `info`, and `accent`.
 * Each color variant must render with the corresponding CSS custom property as its text color.
 */

const expectedTokenMap: Record<string, string> = {
  success: "var(--color-success)",
  warning: "var(--color-warning)",
  danger: "var(--color-danger)",
  info: "var(--color-info)",
  accent: "var(--color-accent)",
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

describe("Property 11: GlassBadge Color Variant Token Mapping", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  it("renders with the corresponding CSS custom property for each color variant", () => {
    fc.assert(
      fc.property(
        fc.constantFrom("success", "warning", "danger", "info", "accent"),
        (color) => {
          const { container } = render(
            <GlassBadge label="test" color={color as "success" | "warning" | "danger" | "info" | "accent"} />
          );

          const badge = container.firstElementChild as HTMLElement;
          expect(badge).not.toBeNull();
          expect(badge.style.color).toBe(expectedTokenMap[color]);
        }
      )
    );
  });
});
