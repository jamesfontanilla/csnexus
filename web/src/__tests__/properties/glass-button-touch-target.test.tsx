import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

/**
 * **Validates: Requirements 3.8**
 *
 * Property 5: GlassButton Touch Target on Mobile
 *
 * Verifies that the CSS media query in utilities.css enforces
 * min-height: 44px for all GlassButton size variants on viewports < 640px.
 * Since JSDOM doesn't support CSS media queries, we verify the rule exists
 * in the stylesheet for each size variant.
 */

const UTILITIES_PATH = resolve(
  import.meta.dirname,
  "../../design-system/utilities.css"
);

const BUTTON_SIZES = ["sm", "md", "lg", "xl"] as const;

function extractMobileMediaBlock(css: string): string | null {
  // Find the @media (max-width: 639px) block that contains glass-btn rules
  const mediaRegex = /@media\s*\(\s*max-width:\s*639px\s*\)\s*\{([\s\S]*?\})\s*\}/g;
  let match: RegExpExecArray | null;
  while ((match = mediaRegex.exec(css)) !== null) {
    const block = match[1];
    if (block.includes("glass-btn-")) {
      return block;
    }
  }
  return null;
}

describe("Property 5: GlassButton Touch Target on Mobile", () => {
  const css = readFileSync(UTILITIES_PATH, "utf-8");
  const mobileBlock = extractMobileMediaBlock(css);

  it("mobile media query block exists for button touch targets", () => {
    expect(mobileBlock).not.toBeNull();
  });

  it("all button size variants have min-height >= 44px in mobile media query", () => {
    fc.assert(
      fc.property(fc.constantFrom(...BUTTON_SIZES), (size) => {
        expect(mobileBlock).not.toBeNull();

        // Assert the size class is referenced in the mobile block
        const sizeClass = `.glass-btn-${size}`;
        expect(mobileBlock).toContain(sizeClass);

        // Assert min-height is set to at least 44px
        // Extract the min-height value from the block
        const minHeightRegex = /min-height:\s*([\d.]+)px/;
        const minHeightMatch = mobileBlock!.match(minHeightRegex);
        expect(minHeightMatch).not.toBeNull();

        const minHeightValue = parseFloat(minHeightMatch![1]);
        expect(minHeightValue).toBeGreaterThanOrEqual(44);
      })
    );
  });
});
