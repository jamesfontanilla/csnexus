import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

// Control reduced motion from tests
let mockReducedMotion = false;

vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => mockReducedMotion,
  springDefault: { type: "spring", stiffness: 300, damping: 20 },
  springGentle: { type: "spring", stiffness: 200, damping: 25 },
  springBouncy: { type: "spring", stiffness: 400, damping: 15 },
  fadeIn: { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.3 } },
  slideUp: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { type: "spring" } },
  slideDown: { initial: { opacity: 0, y: -12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: 12 }, transition: { type: "spring" } },
  scaleIn: { initial: { opacity: 0, scale: 0.95 }, animate: { opacity: 1, scale: 1 }, exit: { opacity: 0, scale: 0.95 }, transition: { type: "spring" } },
  staggerContainer: { animate: { transition: { staggerChildren: 0.06 } } },
  staggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { type: "spring" } },
  cardStaggerContainer: { animate: { transition: { staggerChildren: 0.05 } } },
  cardStaggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.15 } },
  useMotionVariants: (v: Record<string, unknown>) => v,
  makeReducedVariants: (variants: Record<string, unknown>, reduced: boolean) => {
    if (!reduced) return variants;
    return { initial: { opacity: 1 }, animate: { opacity: 1 }, transition: { duration: 0 } };
  },
  pageTransition: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.5 } },
  hoverLift: { whileHover: { y: -2 }, transition: { duration: 0.15 } },
  pressFeedback: { whileTap: { scale: 0.97 }, whileHover: { scale: 1.02 }, transition: { type: "spring" } },
}));

vi.mock("../../hooks/useScrollReveal", () => ({
  useScrollReveal: () => {
    if (mockReducedMotion) {
      return [vi.fn(), { initial: { opacity: 1 }, animate: { opacity: 1 }, transition: { duration: 0 } }];
    }
    return [vi.fn(), { initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.4 } }];
  },
}));

vi.mock("../../hooks/useInView", () => ({
  useInView: () => [vi.fn(), true],
}));

vi.mock("../../stores/auth", () => ({
  isAuthenticated: () => false,
  login: vi.fn(),
  logout: vi.fn(),
  getToken: () => null,
  getLastAuthenticatedAt: () => null,
}));

// Mock framer-motion to render children directly
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return ({ children, style, className, ...rest }: Record<string, unknown>) => {
          const Tag = tag as keyof JSX.IntrinsicElements;
          // Extract initial/animate for testing reduced motion
          const initial = rest.initial as Record<string, unknown> | undefined;
          return (
            <Tag
              className={className as string}
              style={style as React.CSSProperties}
              data-initial-opacity={initial?.opacity}
              data-initial-y={initial?.y}
            >
              {children as React.ReactNode}
            </Tag>
          );
        };
      },
    }
  ),
  AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

function mockMatchMedia(reducedMotion: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: query === "(prefers-reduced-motion: reduce)" ? reducedMotion : false,
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

import { Home } from "../../pages/Home";

describe("Home page (Task 16.2)", () => {
  beforeEach(() => {
    mockReducedMotion = false;
    mockMatchMedia(false);
  });

  describe("Social proof section renders AnimatedCounter (Requirement 11.3)", () => {
    it("renders AnimatedNumber components in the social proof section", () => {
      const { container } = render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      // AnimatedNumber renders <span> with aria-live="polite" and data-duration attribute
      const animatedNumbers = container.querySelectorAll('span[aria-live="polite"][data-duration]');
      // Social proof section has 3 counters: Active Learners, Questions Answered, Pass Rate
      expect(animatedNumbers.length).toBeGreaterThanOrEqual(3);
    });

    it("renders counter labels for social proof metrics", () => {
      render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      expect(screen.getByText("Active Learners")).toBeInTheDocument();
      expect(screen.getByText("Questions Answered")).toBeInTheDocument();
      expect(screen.getByText("Pass Rate")).toBeInTheDocument();
    });
  });

  describe("Sections render in final state when prefers-reduced-motion is active (Requirement 11.6)", () => {
    it("renders all sections without scroll-triggered reveal animations", () => {
      mockReducedMotion = true;
      mockMatchMedia(true);

      const { container } = render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      // When reduced motion is active, useScrollReveal returns motionProps with opacity: 1
      // (no initial hidden state). All sections should be visible immediately.
      const motionDivs = container.querySelectorAll("[data-initial-opacity]");
      motionDivs.forEach((el) => {
        const opacity = el.getAttribute("data-initial-opacity");
        // In reduced motion, initial opacity should be 1 (final state)
        expect(opacity).toBe("1");
      });
    });

    it("does not apply translateY to sections when reduced motion is active", () => {
      mockReducedMotion = true;
      mockMatchMedia(true);

      const { container } = render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      const motionDivs = container.querySelectorAll("[data-initial-y]");
      motionDivs.forEach((el) => {
        const y = el.getAttribute("data-initial-y");
        // In reduced motion, y should be undefined (stripped) or not present
        expect(y === null || y === "undefined" || y === "").toBe(true);
      });
    });
  });
});
