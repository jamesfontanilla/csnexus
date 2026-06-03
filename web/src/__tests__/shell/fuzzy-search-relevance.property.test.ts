// Feature: desktop-app-shell, Property 5: Fuzzy search returns relevant results
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { computeScore, fuzzySearch } from "../../utils/fuzzySearch";
import type { FuzzySearchItem } from "../../utils/fuzzySearch";

/**
 * **Validates: Requirements 6.2**
 *
 * Property 5: Fuzzy search returns relevant results
 *
 * For any non-empty search string and any set of command palette items,
 * all returned results SHALL contain at least a subsequence match of
 * the search string within the item's label or keywords, and results
 * SHALL be ordered by descending match score.
 */

// --- Arbitraries ---

const QUERY_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789";
const LABEL_CHARS = "abcdefghijklmnopqrstuvwxyz -";

/** Generate a non-empty alphanumeric query string (1–8 chars) */
const arbQuery = fc
  .array(fc.constantFrom(...QUERY_CHARS.split("")), { minLength: 1, maxLength: 8 })
  .map((chars) => chars.join(""));

/** Generate a non-empty label string (1–30 chars, letters/spaces/hyphens) */
const arbLabel = fc
  .array(fc.constantFrom(...LABEL_CHARS.split("")), { minLength: 1, maxLength: 30 })
  .map((chars) => chars.join(""));

/** Generate optional keywords (0–3 keywords) */
const arbKeywords = fc.option(
  fc.array(arbLabel, { minLength: 1, maxLength: 3 }),
  { nil: undefined }
);

/** Generate a FuzzySearchItem */
const arbItem: fc.Arbitrary<FuzzySearchItem> = fc.record({
  id: fc.uuid(),
  label: arbLabel,
  description: fc.constant(undefined),
  icon: fc.constant(undefined),
  section: fc.constantFrom("pages" as const, "actions" as const, "recent" as const),
  action: fc.constant(() => {}),
  keywords: arbKeywords,
});

/** Generate a non-empty list of items (1–10) */
const arbItems = fc.array(arbItem, { minLength: 1, maxLength: 10 });

// --- Helper ---

/** Check if `query` is a subsequence of `target` (case-insensitive) */
function isSubsequence(query: string, target: string): boolean {
  const q = query.toLowerCase();
  const t = target.toLowerCase();
  let qi = 0;
  for (let ti = 0; ti < t.length && qi < q.length; ti++) {
    if (t[ti] === q[qi]) qi++;
  }
  return qi === q.length;
}

// --- Property Tests ---

describe("Property 5: Fuzzy search returns relevant results", () => {
  it("all returned results have score > 0", () => {
    fc.assert(
      fc.property(arbQuery, arbItems, (query, items) => {
        const results = fuzzySearch(query, items);
        for (const r of results) {
          expect(r.score).toBeGreaterThan(0);
        }
      }),
      { numRuns: 100 }
    );
  });

  it("results are sorted by descending score", () => {
    fc.assert(
      fc.property(arbQuery, arbItems, (query, items) => {
        const results = fuzzySearch(query, items);
        for (let i = 1; i < results.length; i++) {
          expect(results[i - 1].score).toBeGreaterThanOrEqual(results[i].score);
        }
      }),
      { numRuns: 100 }
    );
  });

  it("for any result, at least one of (label, keywords) has a subsequence match with the query", () => {
    fc.assert(
      fc.property(arbQuery, arbItems, (query, items) => {
        const results = fuzzySearch(query, items);
        for (const r of results) {
          const labelMatch = isSubsequence(query, r.item.label);
          const keywordMatch = (r.item.keywords ?? []).some((kw) =>
            isSubsequence(query, kw)
          );
          // Description can also contribute to score, so also check it
          const descMatch = r.item.description
            ? isSubsequence(query, r.item.description)
            : false;
          expect(labelMatch || keywordMatch || descMatch).toBe(true);
        }
      }),
      { numRuns: 100 }
    );
  });

  it("items with no match (score=0 for label and keywords) are never in the result set", () => {
    fc.assert(
      fc.property(arbQuery, arbItems, (query, items) => {
        const results = fuzzySearch(query, items);
        const resultIds = new Set(results.map((r) => r.item.id));

        for (const item of items) {
          const labelScore = computeScore(query, item.label);
          const keywordScores = (item.keywords ?? []).map((kw) =>
            computeScore(query, kw)
          );
          const descScore = item.description
            ? computeScore(query, item.description)
            : 0;
          const maxScore = Math.max(labelScore, ...keywordScores, descScore);

          if (maxScore === 0) {
            expect(resultIds.has(item.id)).toBe(false);
          }
        }
      }),
      { numRuns: 100 }
    );
  });
});
