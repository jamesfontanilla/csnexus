/**
 * Fuzzy search utility for the Command Palette.
 *
 * Scoring approach (no external library):
 * 1. Exact prefix match → score 100
 * 2. Word boundary match → score 80
 * 3. Substring match → score 60
 * 4. Character sequence match (fuzzy) → score 40
 * 5. No match → filtered out
 *
 * Results are sorted by score descending within each section.
 */

export interface FuzzySearchItem {
  id: string;
  label: string;
  description?: string;
  icon?: React.ReactNode;
  section: "pages" | "actions" | "recent";
  action: () => void;
  keywords?: string[];
}

export interface FuzzySearchResult {
  item: FuzzySearchItem;
  score: number;
}

/**
 * Compute the fuzzy match score for a query against a target string.
 * Returns 0 if no match.
 */
export function computeScore(query: string, target: string): number {
  const q = query.toLowerCase();
  const t = target.toLowerCase();

  if (q.length === 0) return 0;

  // Exact prefix match
  if (t.startsWith(q)) {
    return 100;
  }

  // Word boundary match — query matches start of any word in target
  const words = t.split(/[\s\-_/]+/);
  for (const word of words) {
    if (word.startsWith(q)) {
      return 80;
    }
  }

  // Substring match
  if (t.includes(q)) {
    return 60;
  }

  // Character sequence match (fuzzy) — all chars of query appear in order
  let qi = 0;
  for (let ti = 0; ti < t.length && qi < q.length; ti++) {
    if (t[ti] === q[qi]) {
      qi++;
    }
  }
  if (qi === q.length) {
    return 40;
  }

  return 0;
}

/**
 * Run fuzzy search across a list of items. Returns matching items sorted
 * by score descending, grouped by section order (pages → actions → recent).
 */
export function fuzzySearch(
  query: string,
  items: FuzzySearchItem[]
): FuzzySearchResult[] {
  if (!query.trim()) {
    // No query — return all items grouped by section, no scoring
    return items.map((item) => ({ item, score: 100 }));
  }

  const results: FuzzySearchResult[] = [];

  for (const item of items) {
    // Score against label first
    let bestScore = computeScore(query, item.label);

    // Also check keywords
    if (item.keywords) {
      for (const kw of item.keywords) {
        const kwScore = computeScore(query, kw);
        if (kwScore > bestScore) {
          bestScore = kwScore;
        }
      }
    }

    // Check description
    if (item.description) {
      const descScore = computeScore(query, item.description);
      // Description matches score slightly less
      if (descScore * 0.8 > bestScore) {
        bestScore = descScore * 0.8;
      }
    }

    if (bestScore > 0) {
      results.push({ item, score: bestScore });
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);

  return results;
}

/** Section display order for grouped rendering */
export const SECTION_ORDER: FuzzySearchItem["section"][] = [
  "pages",
  "actions",
  "recent",
];

/** Section labels for display */
export const SECTION_LABELS: Record<FuzzySearchItem["section"], string> = {
  pages: "Pages",
  actions: "Actions",
  recent: "Recent",
};

/**
 * Group results by section, maintaining sort order within groups.
 */
export function groupBySection(
  results: FuzzySearchResult[]
): Map<FuzzySearchItem["section"], FuzzySearchResult[]> {
  const grouped = new Map<FuzzySearchItem["section"], FuzzySearchResult[]>();

  for (const section of SECTION_ORDER) {
    const sectionResults = results.filter((r) => r.item.section === section);
    if (sectionResults.length > 0) {
      grouped.set(section, sectionResults);
    }
  }

  return grouped;
}
