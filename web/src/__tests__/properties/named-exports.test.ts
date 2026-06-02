import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

/**
 * **Validates: Requirements 18.5**
 *
 * Property 21: New Components Are Named Exports
 *
 * For each new component file (Typography.tsx, ProgressRing.tsx, BottomNav.tsx),
 * the file must contain `export function` or `export const` and must NOT contain
 * `export default`.
 */

const COMPONENTS_DIR = resolve(import.meta.dirname, "../../components");

const NEW_COMPONENT_FILES = [
  "Typography.tsx",
  "ProgressRing.tsx",
  "BottomNav.tsx",
] as const;

describe("Property 21: New Components Are Named Exports", () => {
  it("each new component file uses named exports and has no default export", () => {
    fc.assert(
      fc.property(fc.constantFrom(...NEW_COMPONENT_FILES), (fileName) => {
        const filePath = resolve(COMPONENTS_DIR, fileName);
        const content = readFileSync(filePath, "utf-8");

        // Must contain at least one named export
        const hasNamedExport =
          content.includes("export function") ||
          content.includes("export const");
        expect(hasNamedExport).toBe(true);

        // Must NOT contain a default export
        const hasDefaultExport = /export\s+default\b/.test(content);
        expect(hasDefaultExport).toBe(false);
      }),
      { numRuns: 10 }
    );
  });

  // Explicit check per file for clear failure messages
  it.each(NEW_COMPONENT_FILES)("%s uses named exports only", (fileName) => {
    const filePath = resolve(COMPONENTS_DIR, fileName);
    const content = readFileSync(filePath, "utf-8");

    const hasNamedExport =
      content.includes("export function") ||
      content.includes("export const");
    expect(hasNamedExport).toBe(true);

    const hasDefaultExport = /export\s+default\b/.test(content);
    expect(hasDefaultExport).toBe(false);
  });
});
