import type { FuzzySearchItem } from "../../utils/fuzzySearch";

/**
 * Static navigation items for the command palette.
 * These mirror the sidebar nav items and represent all navigable pages.
 */
export function getNavigationItems(
  navigate: (path: string) => void
): FuzzySearchItem[] {
  return [
    {
      id: "nav-dashboard",
      label: "Dashboard",
      section: "pages",
      keywords: ["home", "overview"],
      action: () => navigate("/"),
    },
    {
      id: "nav-modules",
      label: "Modules",
      section: "pages",
      keywords: ["subjects", "topics", "lessons"],
      action: () => navigate("/modules"),
    },
    {
      id: "nav-flashcards",
      label: "Flashcards",
      section: "pages",
      keywords: ["cards", "deck", "study"],
      action: () => navigate("/flashcards"),
    },
    {
      id: "nav-tutor",
      label: "Tutor",
      section: "pages",
      keywords: ["chat", "ai", "help"],
      action: () => navigate("/tutor"),
    },
    {
      id: "nav-analytics",
      label: "Analytics",
      section: "pages",
      keywords: ["stats", "progress", "performance"],
      action: () => navigate("/analytics"),
    },
    {
      id: "nav-leaderboard",
      label: "Leaderboard",
      section: "pages",
      keywords: ["ranking", "competition"],
      action: () => navigate("/leaderboard"),
    },
    {
      id: "nav-goals",
      label: "Goals",
      section: "pages",
      keywords: ["targets", "objectives"],
      action: () => navigate("/goals"),
    },
    {
      id: "nav-study-plan",
      label: "Study Plan",
      section: "pages",
      keywords: ["schedule", "plan"],
      action: () => navigate("/study-plan"),
    },
    {
      id: "nav-readiness",
      label: "Readiness",
      section: "pages",
      keywords: ["exam", "preparation"],
      action: () => navigate("/readiness"),
    },
    {
      id: "nav-profile",
      label: "Profile",
      section: "pages",
      keywords: ["account", "user", "settings"],
      action: () => navigate("/profile"),
    },
    {
      id: "nav-settings",
      label: "Settings",
      section: "pages",
      keywords: ["preferences", "config"],
      action: () => navigate("/settings"),
    },
  ];
}

/**
 * Shell action items for the command palette.
 */
export function getActionItems(shellActions: {
  toggleSidebar: () => void;
  toggleDetailPanel: () => void;
  enterFocusMode: () => void;
  exitFocusMode: () => void;
}): FuzzySearchItem[] {
  return [
    {
      id: "action-toggle-sidebar",
      label: "Toggle Sidebar",
      description: "Show or hide the sidebar navigation",
      section: "actions",
      keywords: ["sidebar", "navigation", "panel", "collapse", "expand"],
      action: shellActions.toggleSidebar,
    },
    {
      id: "action-toggle-detail",
      label: "Toggle Detail Panel",
      description: "Show or hide the detail panel",
      section: "actions",
      keywords: ["detail", "panel", "side", "context"],
      action: shellActions.toggleDetailPanel,
    },
    {
      id: "action-focus-mode",
      label: "Enter Focus Mode",
      description: "Hide all panels for distraction-free work",
      section: "actions",
      keywords: ["focus", "distraction", "fullscreen", "zen"],
      action: shellActions.enterFocusMode,
    },
    {
      id: "action-exit-focus",
      label: "Exit Focus Mode",
      description: "Restore normal panel layout",
      section: "actions",
      keywords: ["focus", "exit", "restore"],
      action: shellActions.exitFocusMode,
    },
  ];
}

/**
 * Get recent pages from sessionStorage.
 */
const RECENT_STORAGE_KEY = "csnexus_recent_pages";
const MAX_RECENT = 5;

export interface RecentPage {
  path: string;
  label: string;
}

export function getRecentPages(): RecentPage[] {
  try {
    const raw = sessionStorage.getItem(RECENT_STORAGE_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as RecentPage[];
  } catch {
    return [];
  }
}

export function addRecentPage(path: string, label: string): void {
  try {
    const pages = getRecentPages().filter((p) => p.path !== path);
    pages.unshift({ path, label });
    sessionStorage.setItem(
      RECENT_STORAGE_KEY,
      JSON.stringify(pages.slice(0, MAX_RECENT))
    );
  } catch {
    // sessionStorage not available — silently skip
  }
}

export function getRecentItems(
  navigate: (path: string) => void
): FuzzySearchItem[] {
  return getRecentPages().map((page) => ({
    id: `recent-${page.path}`,
    label: page.label,
    description: page.path,
    section: "recent" as const,
    action: () => navigate(page.path),
  }));
}
