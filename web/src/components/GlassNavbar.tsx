import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { isAuthenticated } from "../stores/auth";
import { apiClient } from "../api/client";
import { slideDown, springDefault } from "../design-system";
import "./GlassNavbar.css";

interface XPData {
  cumulative_xp: number;
  level: number;
  streak: number;
}

const NAV_LINKS = [
  { to: "/modules", label: "Modules" },
  { to: "/flashcards", label: "Flashcards" },
  { to: "/mastery", label: "Mastery" },
  { to: "/focus", label: "Focus" },
  { to: "/study-plan", label: "Study Plan" },
  { to: "/readiness", label: "Readiness" },
  { to: "/goals", label: "Goals" },
  { to: "/tournaments", label: "Tournaments" },
  { to: "/analytics", label: "Analytics" },
  { to: "/leaderboard", label: "Leaderboard" },
];

export function GlassNavbar() {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [xp, setXp] = useState<XPData | null>(null);

  useEffect(() => {
    function handleScroll() {
      setScrolled(window.scrollY > 10);
    }
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  // Fetch XP data once on mount and when the user navigates back to a page
  // after potentially earning XP. Use a cancellation flag to avoid setting
  // state on an unmounted component.
  useEffect(() => {
    if (!isAuthenticated()) return;
    let cancelled = false;
    apiClient.get<XPData>("/v1/xp/me")
      .then((data) => { if (!cancelled) setXp(data); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [location.pathname]);

  const authenticated = isAuthenticated();

  return (
    <header
      className="glass-navbar"
      style={{
        background: scrolled ? "var(--glass-bg-medium)" : "transparent",
        backdropFilter: scrolled ? "var(--glass-blur-md)" : "none",
        WebkitBackdropFilter: scrolled ? "var(--glass-blur-md)" : "none",
        borderBottom: scrolled
          ? "1px solid var(--glass-border-light)"
          : "1px solid transparent",
        boxShadow: scrolled
          ? "0 4px 24px rgba(26, 15, 10, 0.4), 0 1px 3px rgba(0, 0, 0, 0.2)"
          : "none",
      }}
    >
      {/* Logo */}
      <Link to="/" className="glass-navbar-logo" aria-label="CSNexus Home">
        🎓 CSNexus
      </Link>

      {/* Desktop Nav */}
      {authenticated && (
        <nav aria-label="Main navigation" className="glass-navbar-desktop">
          {NAV_LINKS.map((link) => {
            const active = location.pathname.startsWith(link.to);
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`glass-navbar-link${active ? " active" : ""}`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      )}

      {/* Right side */}
      <div className="glass-navbar-right">
        {authenticated && xp && (
          <Link
            to="/profile"
            className="glass-navbar-xp"
            aria-label={`Level ${xp.level}, ${xp.cumulative_xp} XP, ${xp.streak} day streak`}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              padding: "0.25rem 0.75rem",
              borderRadius: "var(--radius-full, 9999px)",
              background: "var(--glass-bg-subtle)",
              border: "1px solid var(--glass-border-light)",
              textDecoration: "none",
              fontSize: "0.8125rem",
              fontWeight: 600,
              color: "var(--color-text)",
              whiteSpace: "nowrap",
            }}
          >
            <span style={{ color: "var(--color-accent)" }}>⚡ {xp.cumulative_xp.toLocaleString()}</span>
            <span style={{ color: "var(--color-text-muted)", fontSize: "0.6875rem" }}>Lv{xp.level}</span>
            {xp.streak > 0 && (
              <span style={{ color: "var(--color-warning)" }}>🔥{xp.streak}</span>
            )}
          </Link>
        )}
        {authenticated && (
          <Link to="/profile" className="glass-navbar-profile" aria-label="Profile">
            👤
          </Link>
        )}
        {/* Mobile hamburger */}
        {authenticated && (
          <button
            className="glass-navbar-hamburger"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label={menuOpen ? "Close menu" : "Open menu"}
            aria-expanded={menuOpen}
          >
            {menuOpen ? "✕" : "☰"}
          </button>
        )}
      </div>

      {/* Mobile drawer */}
      <AnimatePresence>
        {menuOpen && authenticated && (
          <motion.nav
            className="glass-md glass-mobile-drawer"
            aria-label="Mobile navigation"
            initial={slideDown.initial}
            animate={slideDown.animate}
            exit={slideDown.exit}
            transition={springDefault}
          >
            {NAV_LINKS.map((link) => {
              const active = location.pathname.startsWith(link.to);
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`glass-mobile-drawer-link${active ? " active" : ""}`}
                >
                  {link.label}
                </Link>
              );
            })}
            <Link to="/profile" className="glass-mobile-drawer-link">
              Profile
            </Link>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
