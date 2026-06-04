import { NavLink } from "react-router-dom";
import { useShell } from "../../context/ShellContext";

// --- Navigation Item Definitions ---

export interface SidebarNavItem {
  id: string;
  to: string;
  label: string;
  icon: React.ReactNode;
  section: "primary" | "secondary";
  /** Keyboard shortcut hint displayed as tooltip on hover */
  shortcut?: string;
}

const PRIMARY_NAV_ITEMS: SidebarNavItem[] = [
  { id: "dashboard", to: "/", label: "Dashboard", icon: <DashboardIcon />, section: "primary" },
  { id: "queue", to: "/queue", label: "Daily Queue", icon: <QueueIcon />, section: "primary" },
  { id: "modules", to: "/modules", label: "Modules", icon: <ModulesIcon />, section: "primary" },
  { id: "flashcards", to: "/flashcards", label: "Flashcards", icon: <FlashcardsIcon />, section: "primary" },
  { id: "tutor", to: "/tutor", label: "Tutor", icon: <TutorIcon />, section: "primary" },
];

const SECONDARY_NAV_ITEMS: SidebarNavItem[] = [
  { id: "milestones", to: "/milestones", label: "Milestones", icon: <MilestonesIcon />, section: "secondary" },
  { id: "analytics", to: "/analytics", label: "Analytics", icon: <AnalyticsIcon />, section: "secondary" },
  { id: "leaderboard", to: "/leaderboard", label: "Leaderboard", icon: <LeaderboardIcon />, section: "secondary" },
  { id: "goals", to: "/goals", label: "Goals", icon: <GoalsIcon />, section: "secondary" },
  { id: "study-plan", to: "/study-plan", label: "Study Plan", icon: <StudyPlanIcon />, section: "secondary" },
  { id: "readiness", to: "/readiness", label: "Readiness", icon: <ReadinessIcon />, section: "secondary" },
  { id: "focus", to: "/focus", label: "Focus", icon: <FocusIcon />, section: "secondary" },
  { id: "tournaments", to: "/tournaments", label: "Tournaments", icon: <TournamentsIcon />, section: "secondary" },
];

// --- Sidebar Component ---

export function Sidebar() {
  const { state, actions } = useShell();
  const collapsed = state.sidebarCollapsed;

  return (
    <nav
      role="navigation"
      aria-label="Main navigation"
      className={`sidebar ${collapsed ? "sidebar--collapsed" : ""}`}
    >
      <ProfileCard collapsed={collapsed} />

      <div className="sidebar__nav-groups">
        <NavGroup items={PRIMARY_NAV_ITEMS} collapsed={collapsed} />
        <div className="sidebar__divider" />
        <NavGroup items={SECONDARY_NAV_ITEMS} collapsed={collapsed} />
      </div>

      <button
        type="button"
        className="sidebar__collapse-toggle"
        onClick={actions.toggleSidebar}
        aria-expanded={!collapsed}
        aria-label="Toggle sidebar"
        title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        <span className="sidebar__collapse-toggle-icon" aria-hidden="true">
          <CollapseToggleIcon collapsed={collapsed} />
        </span>
        {!collapsed && (
          <span className="sidebar__collapse-toggle-label">Collapse</span>
        )}
      </button>
    </nav>
  );
}

// --- Profile Card ---

function ProfileCard({ collapsed }: { collapsed: boolean }) {
  return (
    <div className="sidebar__profile">
      <div className="sidebar__profile-avatar" aria-hidden="true">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <circle cx="16" cy="16" r="16" fill="var(--glass-bg-strong)" />
          <circle cx="16" cy="12" r="6" fill="var(--color-text-secondary)" />
          <path d="M6 28c0-5.5 4.5-10 10-10s10 4.5 10 10" fill="var(--color-text-secondary)" />
        </svg>
      </div>
      {!collapsed && (
        <div className="sidebar__profile-info">
          <span className="sidebar__profile-name">Student</span>
          <span className="sidebar__profile-level">Level 1 · 0 XP</span>
        </div>
      )}
    </div>
  );
}

// --- Navigation Group ---

function NavGroup({ items, collapsed }: { items: SidebarNavItem[]; collapsed: boolean }) {
  return (
    <ul className="sidebar__nav-list">
      {items.map((item) => (
        <li key={item.id} className="sidebar__nav-item">
          <NavLink
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `sidebar__nav-link ${isActive ? "sidebar__nav-link--active" : ""}`
            }
            title={
              collapsed
                ? item.shortcut
                  ? `${item.label} (${item.shortcut})`
                  : item.label
                : item.shortcut
                  ? item.shortcut
                  : undefined
            }
          >
            <span className="sidebar__nav-icon" aria-hidden="true">
              {item.icon}
            </span>
            {!collapsed && (
              <span className="sidebar__nav-label">{item.label}</span>
            )}
            {!collapsed && item.shortcut && (
              <kbd
                className="sidebar__nav-shortcut"
                aria-hidden="true"
                style={{
                  marginLeft: "auto",
                  padding: "2px 6px",
                  borderRadius: "var(--radius-xs, 4px)",
                  border: "1px solid var(--glass-border-medium)",
                  background: "var(--glass-bg-subtle)",
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-xs, 11px)",
                  fontFamily: "inherit",
                  fontWeight: 500,
                  whiteSpace: "nowrap",
                  opacity: 0.7,
                }}
              >
                {item.shortcut}
              </kbd>
            )}
          </NavLink>
        </li>
      ))}
    </ul>
  );
}

// --- Icons (inline SVGs) ---

function DashboardIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="1" y="1" width="7" height="7" rx="1.5" />
      <rect x="10" y="1" width="7" height="4" rx="1.5" />
      <rect x="10" y="7" width="7" height="10" rx="1.5" />
      <rect x="1" y="10" width="7" height="7" rx="1.5" />
    </svg>
  );
}

function ModulesIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 3h12a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V3z" />
      <path d="M5 1v2M9 1v2M13 1v2" />
      <path d="M5 9h8M5 12h5" />
    </svg>
  );
}

function FlashcardsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="12" height="10" rx="1.5" />
      <rect x="1" y="2" width="12" height="10" rx="1.5" opacity="0.4" />
      <path d="M6 8h6M6 11h3" />
    </svg>
  );
}

function TutorIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 14V4a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6l-3 3V14z" />
      <path d="M6 6h6M6 9h4" />
    </svg>
  );
}

function AnalyticsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 15V9M7 15V5M11 15V8M15 15V3" />
    </svg>
  );
}

function LeaderboardIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 10h3v6H5zM10 7h3v9h-3zM1 13h3v3H1zM14 4h3v12h-3z" />
    </svg>
  );
}

function GoalsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="9" r="7" />
      <circle cx="9" cy="9" r="4" />
      <circle cx="9" cy="9" r="1" fill="currentColor" />
    </svg>
  );
}

function StudyPlanIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 3h12a1 1 0 011 1v11a1 1 0 01-1 1H3a1 1 0 01-1-1V4a1 1 0 011-1z" />
      <path d="M2 6h14" />
      <path d="M6 9l2 2 4-4" />
    </svg>
  );
}

function ReadinessIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 2l2.5 5H15l-4 3.5 1.5 5.5L9 13l-3.5 3 1.5-5.5L3 7h3.5L9 2z" />
    </svg>
  );
}

function FocusIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="9" cy="9" r="7" />
      <path d="M9 5v4l3 2" />
    </svg>
  );
}

function TournamentsIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 2h8v3a4 4 0 01-8 0V2z" />
      <path d="M5 4H3a1 1 0 00-1 1v1a3 3 0 003 3" />
      <path d="M13 4h2a1 1 0 011 1v1a3 3 0 01-3 3" />
      <path d="M9 9v3" />
      <path d="M6 14h6" />
      <path d="M7 14v2h4v-2" />
    </svg>
  );
}

function QueueIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 4h12" />
      <path d="M3 9h8" />
      <path d="M3 14h5" />
      <path d="M14 10l2 2-2 2" />
    </svg>
  );
}

function MilestonesIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M4 15V3" />
      <path d="M4 3l8 3-8 3" />
    </svg>
  );
}

function CollapseToggleIcon({ collapsed }: { collapsed: boolean }) {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 18 18"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{ transform: collapsed ? "rotate(180deg)" : undefined, transition: "transform var(--duration-fast) var(--ease-standard)" }}
    >
      <path d="M12 3L6 9l6 6" />
    </svg>
  );
}
