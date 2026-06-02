import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { readdirSync, readFileSync } from "node:fs";
import { resolve, join } from "node:path";

/**
 * **Validates: Requirements 18.6**
 *
 * Property 22: Components Do Not Import Token CSS as JS Module
 *
 * Scans all files in web/src/components/ and asserts none contain
 * `import.*tokens\.css` or `import.*utilities\.css` as JS module imports.
 */

const COMPONENTS_DIR = resolve(import.meta.dirname, "../../components");

function getComponentFiles(): string[] {
  const files = readdirSync(COMPONENTS_DIR);
  return files.filter(
    (f) => f.endsWith(".tsx") || f.endsWith(".ts") || f.endsWith(".jsx") || f.endsWith(".js")
  );
}

const FORBIDDEN_PATTERNS = [
  /import\s+.*tokens\.css/,
  /import\s+.*utilities\.css/,
] as const;

describe("Property 22: Components Do Not Import Token CSS as JS Module", () => {
  const componentFiles = getComponentFiles();

  it("no component file imports tokens.css or utilities.css as a JS module", () => {
    fc.assert(
      fc.property(fc.constantFrom(...componentFiles), (fileName) => {
        const filePath = join(COMPONENTS_DIR, fileName);
        const content = readFileSync(filePath, "utf-8");

        for (const pattern of FORBIDDEN_PATTERNS) {
          expect(content).not.toMatch(pattern);
        }
      }),
      { numRuns: 10 }
    );
  });

  // Explicit check per file for clear failure messages
  it.each(componentFiles)("%s does not import tokens.css or utilities.css", (fileName) => {
    const filePath = join(COMPONENTS_DIR, fileName);
    const content = readFileSync(filePath, "utf-8");

    for (const pattern of FORBIDDEN_PATTERNS) {
      expect(content).not.toMatch(pattern);
    }
  });
});
