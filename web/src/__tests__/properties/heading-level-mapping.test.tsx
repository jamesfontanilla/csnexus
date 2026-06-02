import { describe, it, expect, beforeAll } from "vitest";
import * as fc from "fast-check";
import { render } from "@testing-library/react";
import { Heading } from "../../components/Typography";

/**
 * **Validates: Requirements 4.2**
 *
 * Property 6: Heading Level Maps to Correct Token Group
 *
 * For any heading level 1–4, the rendered element tag must be `h{level}`
 * and the inline style must reference `--heading-{level}-size` for fontSize.
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

describe("Property 6: Heading Level Maps to Correct Token Group", () => {
  it("rendered element tag is h{level} and inline style references --heading-{level}-size", () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 1, max: 4 }),
        (level) => {
          const { container } = render(
            <Heading level={level as 1 | 2 | 3 | 4}>Test</Heading>
          );

          const el = container.firstElementChild as HTMLElement;

          // Assert the rendered element tag matches h{level}
          expect(el.tagName.toLowerCase()).toBe(`h${level}`);

          // Assert the inline style references the correct heading size token
          const style = el.getAttribute("style") ?? "";
          expect(style).toContain(`var(--heading-${level}-size)`);
        }
      )
    );
  });
});
