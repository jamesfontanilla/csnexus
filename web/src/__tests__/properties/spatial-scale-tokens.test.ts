import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

/**
 * **Validates: Requirements 1.5**
 *
 * Property 1: Spatial Scale Tokens Are Strictly Positive
 *
 * Parses tokens.css and asserts that all six density token values
 * resolve to strictly positive values (> 0).
 */

const TOKENS_PATH = resolve(import.meta.dirname, "../../design-system/tokens.css");

const DENSITY_TOKENS = [
  "--density-compact-padding",
  "--density-compact-gap",
  "--density-comfortable-padding",
  "--density-comfortable-gap",
  "--density-spacious-padding",
  "--density-spacious-gap",
] as const;

function parseCssCustomProperties(css: string): Map<string, string> {
  const props = new Map<string, string>();
  // Match CSS custom property declarations: --name: value;
  const regex = /--([\w-]+)\s*:\s*([^;]+);/g;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(css)) !== null) {
    props.set(`--${match[1]}`, match[2].trim());
  }
  return props;
}

function resolveVar(value: string, props: Map<string, string>): string {
  // Resolve var(--token-name) references recursively
  const varRegex = /var\((--[\w-]+)\)/g;
  let resolved = value;
  let iterations = 0;
  while (resolved.includes("var(") && iterations < 10) {
    resolved = resolved.replace(varRegex, (_, varName) => {
      return props.get(varName) ?? "0";
    });
    iterations++;
  }
  return resolved;
}

function parseToPixels(value: string): number {
  // Convert rem values to pixels (assuming 16px base)
  const remMatch = value.match(/^([\d.]+)rem$/);
  if (remMatch) {
    return parseFloat(remMatch[1]) * 16;
  }
  // Try px values
  const pxMatch = value.match(/^([\d.]+)px$/);
  if (pxMatch) {
    return parseFloat(pxMatch[1]);
  }
  // Try plain number
  const num = parseFloat(value);
  if (!isNaN(num)) {
    return num;
  }
  return 0;
}

describe("Property 1: Spatial Scale Tokens Are Strictly Positive", () => {
  const css = readFileSync(TOKENS_PATH, "utf-8");
  const props = parseCssCustomProperties(css);

  it("all six density tokens resolve to strictly positive values", () => {
    fc.assert(
      fc.property(
        fc.constantFrom(...DENSITY_TOKENS),
        (tokenName) => {
          const rawValue = props.get(tokenName);
          expect(rawValue).toBeDefined();

          const resolved = resolveVar(rawValue!, props);
          const numericValue = parseToPixels(resolved);

          expect(numericValue).toBeGreaterThan(0);
        }
      )
    );
  });

  // Explicit check for each token to provide clear failure messages
  it.each(DENSITY_TOKENS)("%s resolves to a strictly positive value", (tokenName) => {
    const rawValue = props.get(tokenName);
    expect(rawValue).toBeDefined();

    const resolved = resolveVar(rawValue!, props);
    const numericValue = parseToPixels(resolved);

    expect(numericValue).toBeGreaterThan(0);
  });
});
