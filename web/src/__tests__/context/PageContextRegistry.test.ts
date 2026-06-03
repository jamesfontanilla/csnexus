import { describe, it, expect } from 'vitest';
import {
  matchRoutePattern,
  resolvePageContext,
  PAGE_CONTEXTS,
} from '../../context/PageContextRegistry';

describe('matchRoutePattern', () => {
  it('matches exact static paths', () => {
    expect(matchRoutePattern('/modules', '/modules')).toBe(true);
    expect(matchRoutePattern('/profile', '/profile')).toBe(true);
    expect(matchRoutePattern('/', '/')).toBe(true);
  });

  it('does not match different static paths', () => {
    expect(matchRoutePattern('/modules', '/profile')).toBe(false);
    expect(matchRoutePattern('/settings', '/admin')).toBe(false);
  });

  it('matches paths with single dynamic segment', () => {
    expect(matchRoutePattern('/subtopics/:subtopicId/lesson', '/subtopics/123/lesson')).toBe(true);
    expect(matchRoutePattern('/subtopics/:subtopicId/lesson', '/subtopics/abc-def/lesson')).toBe(true);
  });

  it('matches paths with multiple dynamic segments', () => {
    expect(matchRoutePattern('/quiz/:scope/:scopeId', '/quiz/module/42')).toBe(true);
    expect(matchRoutePattern('/modules/:moduleId/topics', '/modules/numerical-ability/topics')).toBe(true);
  });

  it('does not match when segment count differs', () => {
    expect(matchRoutePattern('/quiz/:scope/:scopeId', '/quiz/module')).toBe(false);
    expect(matchRoutePattern('/modules', '/modules/123/topics')).toBe(false);
  });

  it('does not match when static segments differ', () => {
    expect(matchRoutePattern('/subtopics/:subtopicId/lesson', '/subtopics/123/quiz')).toBe(false);
  });

  it('handles root path correctly', () => {
    expect(matchRoutePattern('/', '/')).toBe(true);
    expect(matchRoutePattern('/', '/modules')).toBe(false);
  });
});

describe('resolvePageContext', () => {
  it('returns correct context for dashboard', () => {
    const ctx = resolvePageContext('/');
    expect(ctx.layoutMode).toBe('standard');
    expect(ctx.showDetailPanel).toBe(false);
  });

  it('returns correct context for modules list', () => {
    const ctx = resolvePageContext('/modules');
    expect(ctx.layoutMode).toBe('standard');
    expect(ctx.showDetailPanel).toBe(false);
  });

  it('returns correct context for module topics with dynamic segment', () => {
    const ctx = resolvePageContext('/modules/numerical-ability/topics');
    expect(ctx.layoutMode).toBe('standard');
    expect(ctx.showDetailPanel).toBe(false);
    expect(ctx.breadcrumbLabels).toEqual({ modules: 'Modules' });
  });

  it('returns correct context for lesson reader (split mode)', () => {
    const ctx = resolvePageContext('/subtopics/abc-123/lesson');
    expect(ctx.layoutMode).toBe('split');
    expect(ctx.showDetailPanel).toBe(true);
    expect(ctx.centeredMaxWidth).toBe(680);
    expect(ctx.detailPanelComponent).toBeDefined();
  });

  it('returns correct context for quiz (centered + autoFocusMode)', () => {
    const ctx = resolvePageContext('/quiz/module/42');
    expect(ctx.layoutMode).toBe('centered');
    expect(ctx.autoFocusMode).toBe(true);
    expect(ctx.centeredMaxWidth).toBe(720);
  });

  it('returns correct context for mock exam', () => {
    const ctx = resolvePageContext('/mock-exam');
    expect(ctx.layoutMode).toBe('centered');
    expect(ctx.autoFocusMode).toBe(true);
    expect(ctx.centeredMaxWidth).toBe(720);
  });

  it('returns correct context for tutor (split mode)', () => {
    const ctx = resolvePageContext('/tutor');
    expect(ctx.layoutMode).toBe('split');
    expect(ctx.showDetailPanel).toBe(true);
    expect(ctx.detailPanelComponent).toBeDefined();
  });

  it('returns correct context for flashcards study (centered + autoFocusMode)', () => {
    const ctx = resolvePageContext('/flashcards/study');
    expect(ctx.layoutMode).toBe('centered');
    expect(ctx.autoFocusMode).toBe(true);
    expect(ctx.centeredMaxWidth).toBe(720);
  });

  it('returns correct context for profile (centered)', () => {
    const ctx = resolvePageContext('/profile');
    expect(ctx.layoutMode).toBe('centered');
    expect(ctx.centeredMaxWidth).toBe(720);
    expect(ctx.showDetailPanel).toBe(false);
  });

  it('returns correct context for settings (centered)', () => {
    const ctx = resolvePageContext('/settings');
    expect(ctx.layoutMode).toBe('centered');
    expect(ctx.centeredMaxWidth).toBe(720);
    expect(ctx.showDetailPanel).toBe(false);
  });

  it('returns correct context for admin (standard, wider sidebar)', () => {
    const ctx = resolvePageContext('/admin');
    expect(ctx.layoutMode).toBe('standard');
    expect(ctx.sidebarWidth).toBe(280);
  });

  it('returns default context for unknown routes', () => {
    const ctx = resolvePageContext('/some/unknown/route');
    expect(ctx.layoutMode).toBe('standard');
    expect(ctx.showDetailPanel).toBe(false);
  });

  it('all PAGE_CONTEXTS entries are resolvable by their own pattern', () => {
    // For static routes, resolvePageContext should return the exact entry
    for (const [pattern, expectedCtx] of Object.entries(PAGE_CONTEXTS)) {
      if (!pattern.includes(':')) {
        const resolved = resolvePageContext(pattern);
        expect(resolved).toBe(expectedCtx);
      }
    }
  });
});
