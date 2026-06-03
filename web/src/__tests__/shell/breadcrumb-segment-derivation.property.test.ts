// Feature: desktop-app-shell, Property 9: Breadcrumb segment derivation
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import {
  deriveBreadcrumbSegments,
  formatSegmentLabel,
} from "../../components/shell/BreadcrumbBar";

/**
 * **Validates: Requirements 10.1, 10.3**
 *
 * Property 9: Breadcrumb segment derivation
 *
 * For any route path and associated PageContext breadcrumb labels, the
 * generated breadcrumb segments SHALL produce one clickable segment per
 * path component, with labels matching PageContext.breadcrumbLabels
 * overrides where defined, and the raw path segment capitalized otherwise.
 */

const ALPHA_NUM_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789";

/**
 * Arbitrary: generates a non-empty alphanumeric string (no hyphens).
 */
const arbAlphaNum = fc
  .array(fc.constantFrom(...ALPHA_NUM_CHARS.split("")), { minLength: 1, maxLength: 8 })
  .map((chars) => chars.join(""));

/**
 * Arbitrary: generates a single valid path segment (lowercase alphanumeric with optional hyphens).
 * Format: word(-word)* — never starts or ends with a hyphen.
 */
const arbPathSegment = fc
  .tuple(
    arbAlphaNum,
    fc.array(arbAlphaNum, { minLength: 0, maxLength: 2 })
  )
  .map(([first, rest]) => (rest.length > 0 ? [first, ...rest].join("-") : first));

/**
 * Arbitrary: generates an array of 1–5 path segments.
 */
const arbPathSegments = fc.array(arbPathSegment, { minLength: 1, maxLength: 5 });

const LABEL_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ";

/**
 * Arbitrary: generates a non-empty display label string.
 */
const arbLabel = fc
  .array(fc.constantFrom(...LABEL_CHARS.split("")), { minLength: 1, maxLength: 12 })
  .map((chars) => chars.join(""));

/**
 * Arbitrary: generates a breadcrumbLabels map that may override some segments.
 * Given the segments array, randomly picks a subset to override with custom labels.
 */
function arbBreadcrumbLabels(segments: string[]) {
  return fc
    .subarray(segments, { minLength: 0 })
    .chain((subset) =>
      fc.tuple(
        fc.constant(subset),
        fc.array(arbLabel, { minLength: subset.length, maxLength: subset.length })
      )
    )
    .map(([keys, values]) => {
      const map: Record<string, string> = {};
      keys.forEach((key, i) => {
        map[key] = values[i];
      });
      return map;
    });
}

describe("Property 9: Breadcrumb segment derivation", () => {
  it("for any path with N segments, the result has N+1 entries (N path components + Home)", () => {
    fc.assert(
      fc.property(arbPathSegments, (segments) => {
        const pathname = "/" + segments.join("/");
        const result = deriveBreadcrumbSegments(pathname);
        expect(result).toHaveLength(segments.length + 1);
      }),
      { numRuns: 100 }
    );
  });

  it("the first segment is always { label: 'Home', path: '/' }", () => {
    fc.assert(
      fc.property(arbPathSegments, (segments) => {
        const pathname = "/" + segments.join("/");
        const result = deriveBreadcrumbSegments(pathname);
        expect(result[0]).toEqual({ label: "Home", path: "/" });
      }),
      { numRuns: 100 }
    );
  });

  it("each segment's path is the cumulative path up to that component", () => {
    fc.assert(
      fc.property(arbPathSegments, (segments) => {
        const pathname = "/" + segments.join("/");
        const result = deriveBreadcrumbSegments(pathname);

        // First is always "/"
        expect(result[0].path).toBe("/");

        // Each subsequent segment's path is cumulative
        let expectedPath = "";
        for (let i = 0; i < segments.length; i++) {
          expectedPath += `/${segments[i]}`;
          expect(result[i + 1].path).toBe(expectedPath);
        }
      }),
      { numRuns: 100 }
    );
  });

  it("when breadcrumbLabels provides a mapping for a segment, that label is used", () => {
    fc.assert(
      fc.property(
        arbPathSegments.chain((segments) =>
          fc.tuple(fc.constant(segments), arbBreadcrumbLabels(segments))
        ),
        ([segments, labels]) => {
          const pathname = "/" + segments.join("/");
          const result = deriveBreadcrumbSegments(pathname, labels);

          for (let i = 0; i < segments.length; i++) {
            const seg = segments[i];
            if (labels[seg] !== undefined) {
              expect(result[i + 1].label).toBe(labels[seg]);
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });

  it("when no mapping exists, the segment label equals formatSegmentLabel(rawSegment)", () => {
    fc.assert(
      fc.property(
        arbPathSegments.chain((segments) =>
          fc.tuple(fc.constant(segments), arbBreadcrumbLabels(segments))
        ),
        ([segments, labels]) => {
          const pathname = "/" + segments.join("/");
          const result = deriveBreadcrumbSegments(pathname, labels);

          for (let i = 0; i < segments.length; i++) {
            const seg = segments[i];
            if (labels[seg] === undefined) {
              expect(result[i + 1].label).toBe(formatSegmentLabel(seg));
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
