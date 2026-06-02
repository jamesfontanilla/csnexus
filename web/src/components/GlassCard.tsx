import type { ReactNode, CSSProperties, KeyboardEvent } from "react";
import { motion, type TargetAndTransition } from "framer-motion";
import { useReducedMotion } from "../design-system/motion";

type Elevation = "flat" | "raised" | "floating";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  blur?: "sm" | "md" | "lg";
  elevation?: Elevation;
  premium?: boolean;
  hoverable?: boolean;
  lifted?: boolean;
  onClick?: () => void;
  style?: CSSProperties;
  as?: "div" | "section" | "article";
}

const elevationClassMap: Record<Elevation, string> = {
  flat: "glass-sm",
  raised: "glass-md",
  floating: "glass-lg",
};

const elevationShadowMap: Record<Elevation, string> = {
  flat: "var(--shadow-elevation-1)",
  raised: "var(--shadow-elevation-2)",
  floating: "var(--shadow-elevation-4)",
};

const elevationSurfaceMap: Record<Elevation, string> = {
  flat: "var(--surface-1)",
  raised: "var(--surface-2)",
  floating: "var(--surface-4)",
};

/** Shadow one level above the current elevation, used for hover */
const elevationHoverShadowMap: Record<Elevation, string> = {
  flat: "var(--shadow-elevation-1)",
  raised: "var(--shadow-elevation-3)",
  floating: "var(--shadow-elevation-4)",
};

export function GlassCard({
  children,
  className = "",
  blur = "md",
  elevation,
  premium = false,
  hoverable = false,
  lifted = false,
  onClick,
  style,
  as = "div",
}: GlassCardProps) {
  const reducedMotion = useReducedMotion();
  const Component = motion[as];

  // Determine effective elevation
  const effectiveElevation: Elevation | undefined = elevation;

  // Build class list
  const classes: string[] = ["glass-card"];

  if (effectiveElevation) {
    classes.push(elevationClassMap[effectiveElevation]);
  } else {
    // Legacy behavior: use blur prop for glass class
    classes.push(`glass-${blur}`);
  }

  if (premium) {
    classes.push("glass-card-premium");
  }

  if (className) {
    classes.push(className);
  }

  // Hover animation
  let hoverAnimation: TargetAndTransition | undefined;
  if (!reducedMotion) {
    if (effectiveElevation === "raised" || effectiveElevation === "floating") {
      hoverAnimation = {
        y: -2,
        boxShadow: elevationHoverShadowMap[effectiveElevation],
        transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] },
      };
    } else if (effectiveElevation === "flat") {
      // flat: border-color only (handled via CSS .glass-card:hover), no transform
      hoverAnimation = undefined;
    } else if (hoverable) {
      // Legacy hoverable behavior
      hoverAnimation = {
        scale: 1.01,
        y: -2,
        boxShadow: "var(--shadow-lifted)",
        transition: { type: "spring", stiffness: 300, damping: 20 },
      };
    }
  }

  const tapAnimation =
    (hoverable || effectiveElevation) && !reducedMotion
      ? { scale: 0.99 }
      : undefined;

  // Entrance animation
  const entranceInitial =
    !reducedMotion ? { opacity: 0, y: 8 } : undefined;
  const entranceAnimate =
    !reducedMotion ? { opacity: 1, y: 0 } : undefined;

  // Entrance transition (--duration-normal = 250ms)
  const entranceTransition = !reducedMotion
    ? { duration: 0.25, ease: [0.4, 0, 0.2, 1] }
    : { duration: 0 };

  // Inline styles
  const inlineStyle: CSSProperties = {
    position: "relative",
    padding: "var(--space-6)",
    willChange: hoverable || effectiveElevation ? "transform" : undefined,
    transform: lifted ? "translateY(-2px)" : undefined,
    boxShadow: effectiveElevation
      ? elevationShadowMap[effectiveElevation]
      : lifted
        ? "var(--shadow-lifted)"
        : undefined,
    backgroundColor: effectiveElevation
      ? elevationSurfaceMap[effectiveElevation]
      : undefined,
    ...style,
  };

  return (
    <Component
      className={classes.join(" ")}
      style={inlineStyle}
      initial={entranceInitial}
      animate={entranceAnimate}
      transition={entranceTransition}
      whileHover={hoverAnimation}
      whileTap={onClick ? tapAnimation : undefined}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e: KeyboardEvent) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {children}
    </Component>
  );
}
