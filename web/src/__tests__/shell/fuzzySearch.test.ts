import { describe, it, expect } from 'vitest';
import {
  computeScore,
  fuzzySearch,
  groupBySection,
  FuzzySearchItem,
} from '../../utils/fuzzySearch';

describe('computeScore', () => {
  it('returns 100 for exact prefix match', () => {
    expect(computeScore('dash', 'Dashboard')).toBe(100);
    expect(computeScore('Dashboard', 'Dashboard')).toBe(100);
  });

  it('returns 80 for word boundary match', () => {
    expect(computeScore('plan', 'Study Plan')).toBe(80);
    expect(computeScore('panel', 'Detail Panel')).toBe(80);
  });

  it('returns 60 for substring match', () => {
    expect(computeScore('ard', 'Leaderboard')).toBe(60);
    expect(computeScore('ash', 'Dashboard')).toBe(60);
  });

  it('returns 40 for character sequence (fuzzy) match', () => {
    expect(computeScore('dbd', 'Dashboard')).toBe(40);
    expect(computeScore('flsh', 'Flashcards')).toBe(40);
  });

  it('returns 0 for no match', () => {
    expect(computeScore('xyz', 'Dashboard')).toBe(0);
    expect(computeScore('zzz', 'Modules')).toBe(0);
  });

  it('returns 0 for empty query', () => {
    expect(computeScore('', 'Dashboard')).toBe(0);
  });

  it('is case-insensitive', () => {
    expect(computeScore('DASH', 'Dashboard')).toBe(100);
    expect(computeScore('dash', 'DASHBOARD')).toBe(100);
  });
});

describe('fuzzySearch', () => {
  const items: FuzzySearchItem[] = [
    { id: '1', label: 'Dashboard', section: 'pages', action: () => {} },
    { id: '2', label: 'Modules', section: 'pages', action: () => {}, keywords: ['subjects'] },
    { id: '3', label: 'Toggle Sidebar', section: 'actions', action: () => {}, keywords: ['sidebar', 'collapse'] },
    { id: '4', label: 'Settings', section: 'pages', action: () => {} },
    { id: '5', label: 'Dashboard', section: 'recent', action: () => {} },
  ];

  it('returns all items when query is empty (palette open state)', () => {
    const results = fuzzySearch('', items);
    expect(results).toHaveLength(items.length);
  });

  it('filters out items with no match', () => {
    const results = fuzzySearch('xyz', items);
    expect(results).toHaveLength(0);
  });

  it('returns matching items sorted by score descending', () => {
    const results = fuzzySearch('dash', items);
    expect(results.length).toBe(2); // Both Dashboard items
    expect(results[0].score).toBe(100);
    expect(results[1].score).toBe(100);
  });

  it('matches against keywords', () => {
    const results = fuzzySearch('subjects', items);
    expect(results.length).toBe(1);
    expect(results[0].item.id).toBe('2');
    expect(results[0].score).toBe(100);
  });

  it('takes the highest score from label or keywords', () => {
    const results = fuzzySearch('sidebar', items);
    expect(results.length).toBeGreaterThan(0);
    const toggleItem = results.find((r) => r.item.id === '3');
    expect(toggleItem).toBeDefined();
    expect(toggleItem!.score).toBe(100); // keyword exact prefix
  });

  it('sorts by score descending', () => {
    const results = fuzzySearch('s', items);
    const scores = results.map((r) => r.score);
    for (let i = 1; i < scores.length; i++) {
      expect(scores[i]).toBeLessThanOrEqual(scores[i - 1]);
    }
  });
});

describe('groupBySection', () => {
  const items: FuzzySearchItem[] = [
    { id: '1', label: 'Dashboard', section: 'pages', action: () => {} },
    { id: '2', label: 'Toggle Sidebar', section: 'actions', action: () => {} },
    { id: '3', label: 'Dashboard', section: 'recent', action: () => {} },
    { id: '4', label: 'Modules', section: 'pages', action: () => {} },
  ];

  it('groups results by section', () => {
    const results = fuzzySearch('d', items);
    const grouped = groupBySection(results);
    expect(grouped.get('pages')!.length).toBeGreaterThanOrEqual(1);
    expect(grouped.get('recent')!.length).toBeGreaterThanOrEqual(1);
  });

  it('returns empty map when no results', () => {
    const grouped = groupBySection([]);
    expect(grouped.size).toBe(0);
  });

  it('maintains section order: pages, actions, recent', () => {
    const results = fuzzySearch('d', items);
    const grouped = groupBySection(results);
    const keys = [...grouped.keys()];
    // pages should come before recent in the order
    const pagesIdx = keys.indexOf('pages');
    const recentIdx = keys.indexOf('recent');
    if (pagesIdx !== -1 && recentIdx !== -1) {
      expect(pagesIdx).toBeLessThan(recentIdx);
    }
  });
});
