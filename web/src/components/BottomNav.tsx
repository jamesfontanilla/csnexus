import { useRef, useEffect, useCallback } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { motion, useMotionValue, animate } from "framer-motion";
import { useReducedMotion } from "../design-system/motion";

interface BottomNavItem {
  path: string;
  label: string;
  icon: React.ReactNode;
}

const BOTTOM_NAV_ITEMS: BottomNavItem[] = [
  { path: "/modules", label: "Study", icon: "📚" },
  { path: "/readiness", label: "Readiness", icon: "📊" },
  { path: "/mastery", label: "Mastery", icon: "🏆" },
  { path: "/profile", label: "Profile", icon: "👤" },
];

export function BottomNav() {
  const location = useLocation();
  const reducedMotion = useReducedMotion();
  const navRef = useRef<HTMLElement>(null);
  const indicatorX = useMotionValue(0);
  const indicatorWidth = useMotionValue(0);

  const getActiveIndex = useCallback((): number => {
    return BOTTOM_NAV_ITEMS.findIndex((item) =>
      location.pathname.startsWith(item.path)
    );
  }, [location.pathname]);

  const updateIndicator = useCallback(() => {
    const nav = navRef.current;
    if (!nav) return;

    const activeIndex = getActiveIndex();
    if (activeIndex === -1) return;

    const items = nav.querySelectorAll<HTMLElement>(".bottom-nav-item");
    const activeItem = items[activeIndex];
    if (!activeItem) return;

    const navRect = nav.getBoundingClientRect();
    const itemRect = activeItem.getBoundingClientRect();
    const targetX = itemRect.left - navRect.left;
    const targetWidth = itemRect.width;

    if (reducedMotion) {
      indicatorX.set(targetX);
      indicatorWidth.set(targetWidth);
    } else {
      animate(indicatorX, targetX, {
        type: "spring",
        stiffness: 300,
        damping: 25,
      });
      animate(indicatorWidth, targetWidth, {
        type: "spring",
        stiffness: 300,
        damping: 25,
      });
    }
  }, [getActiveIndex, reducedMotion, indicatorX, indicatorWidth]);

  useEffect(() => {
    updateIndicator();
  }, [updateIndicator]);

  // Update on resize
  useEffect(() => {
    function handleResize() {
      updateIndicator();
    }
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [updateIndicator]);

  const activeIndex = getActiveIndex();

  return (
    <nav ref={navRef} className="bottom-nav" aria-label="Bottom navigation">
      {activeIndex !== -1 && (
        <motion.div
          aria-hidden="true"
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            height: 2,
            background: "var(--color-accent)",
            borderRadius: 1,
            x: indicatorX,
            width: indicatorWidth,
          }}
        />
      )}
      {BOTTOM_NAV_ITEMS.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            `bottom-nav-item${isActive ? " active" : ""}`
          }
        >
          <span aria-hidden="true">{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
