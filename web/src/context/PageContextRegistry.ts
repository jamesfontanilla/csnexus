import { useLocation } from 'react-router-dom';
import { useMemo } from 'react';

// Layout modes the content area can render in
export type LayoutMode = 'standard' | 'centered' | 'split';

// Sidebar navigation item (used by sidebarExtras)
export interface SidebarNavItem {
  id: string;
  to: string;
  label: string;
  icon: string;
  shortcut?: string;
  section: 'primary' | 'secondary';
}

// Per-route layout configuration
export interface PageContext {
  layoutMode: LayoutMode;
  /** Max-width for centered mode content. Default: 900px */
  centeredMaxWidth?: number;
  /** Whether to show the detail panel (split mode enables it automatically) */
  showDetailPanel?: boolean;
  /** Component to lazy-load into the detail panel */
  detailPanelComponent?: () => Promise<{ default: React.ComponentType }>;
  /** Whether this page activates focus mode automatically */
  autoFocusMode?: boolean;
  /** Override default sidebar width for this page */
  sidebarWidth?: number;
  /** Breadcrumb label overrides (route segment → display label) */
  breadcrumbLabels?: Record<string, string>;
  /** Additional sidebar navigation items (e.g., admin nav) */
  sidebarExtras?: SidebarNavItem[];
}

// Default page context for unmatched routes
const DEFAULT_PAGE_CONTEXT: PageContext = {
  layoutMode: 'standard',
  showDetailPanel: false,
};

/**
 * Static map of route patterns to their page context configuration.
 * Route patterns use `:param` syntax for dynamic segments.
 */
export const PAGE_CONTEXTS: Record<string, PageContext> = {
  '/': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/modules': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/modules/:moduleId/topics': {
    layoutMode: 'standard',
    showDetailPanel: false,
    breadcrumbLabels: { modules: 'Modules' },
  },
  '/topics/:topicId/subtopics': {
    layoutMode: 'standard',
    showDetailPanel: false,
    breadcrumbLabels: { topics: 'Topics' },
  },
  '/subtopics/:subtopicId/lesson': {
    layoutMode: 'split',
    showDetailPanel: true,
    detailPanelComponent: () => import('../components/shell/detail-panels/LessonTOC'),
    centeredMaxWidth: 680,
  },
  '/quiz/:scope/:scopeId': {
    layoutMode: 'centered',
    autoFocusMode: true,
    centeredMaxWidth: 720,
  },
  '/mock-exam': {
    layoutMode: 'centered',
    autoFocusMode: true,
    centeredMaxWidth: 720,
  },
  '/mock-exam/:attemptId/results': {
    layoutMode: 'centered',
    centeredMaxWidth: 720,
    showDetailPanel: false,
  },
  '/tutor': {
    layoutMode: 'split',
    showDetailPanel: true,
    detailPanelComponent: () => import('../components/shell/detail-panels/TutorContext'),
  },
  '/flashcards': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/decks/new': {
    layoutMode: 'centered',
    centeredMaxWidth: 720,
    showDetailPanel: false,
  },
  '/flashcards/decks/:deckId': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/study': {
    layoutMode: 'centered',
    autoFocusMode: true,
    centeredMaxWidth: 720,
  },
  '/flashcards/marketplace': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/analytics': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/exam': {
    layoutMode: 'centered',
    autoFocusMode: true,
    centeredMaxWidth: 720,
  },
  '/flashcards/social': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/generate': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/flashcards/admin': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/profile': {
    layoutMode: 'centered',
    centeredMaxWidth: 720,
    showDetailPanel: false,
  },
  '/settings': {
    layoutMode: 'centered',
    centeredMaxWidth: 720,
    showDetailPanel: false,
  },
  '/admin': {
    layoutMode: 'standard',
    sidebarWidth: 280,
  },
  '/analytics': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/leaderboard': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/goals': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/study-plan': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/readiness': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/focus': {
    layoutMode: 'centered',
    autoFocusMode: true,
    centeredMaxWidth: 720,
  },
  '/tournaments': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/mastery': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/onboarding': {
    layoutMode: 'centered',
    centeredMaxWidth: 720,
    showDetailPanel: false,
  },
  '/queue': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
  '/milestones': {
    layoutMode: 'standard',
    showDetailPanel: false,
  },
};

/**
 * Match a pathname against a route pattern with `:param` segments.
 * Returns true if the pathname matches the pattern.
 */
export function matchRoutePattern(pattern: string, pathname: string): boolean {
  const patternSegments = pattern.split('/').filter(Boolean);
  const pathSegments = pathname.split('/').filter(Boolean);

  if (patternSegments.length !== pathSegments.length) {
    return false;
  }

  return patternSegments.every((segment, i) => {
    // Dynamic segment matches anything
    if (segment.startsWith(':')) {
      return true;
    }
    return segment === pathSegments[i];
  });
}

/**
 * Find the PageContext for a given pathname by matching against registered patterns.
 * Returns the matched context or the default context for unmatched routes.
 */
export function resolvePageContext(pathname: string): PageContext {
  // Try exact match first (most common case, avoids iteration)
  if (PAGE_CONTEXTS[pathname]) {
    return PAGE_CONTEXTS[pathname];
  }

  // Try pattern matching for routes with dynamic segments
  for (const pattern of Object.keys(PAGE_CONTEXTS)) {
    if (pattern.includes(':') && matchRoutePattern(pattern, pathname)) {
      return PAGE_CONTEXTS[pattern];
    }
  }

  return DEFAULT_PAGE_CONTEXT;
}

/**
 * Hook that resolves the PageContext for the current route.
 * Uses React Router's useLocation to get the current pathname
 * and matches it against registered route patterns.
 */
export function usePageContext(): PageContext {
  const { pathname } = useLocation();

  return useMemo(() => resolvePageContext(pathname), [pathname]);
}
