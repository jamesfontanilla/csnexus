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

const mockIsAuthenticated = vi.fn(() => false);

vi.mock("../../stores/auth", () => ({
  isAuthenticated: () => mockIsAuthenticated(),
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
    mockIsAuthenticated.mockReturnValue(false);
  });

  describe("Homepage copy stays aligned with README product claims", () => {
    it("does not show fabricated user-count social proof", () => {
      render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      expect(screen.queryByText("Active Learners")).not.toBeInTheDocument();
      expect(screen.queryByText("Questions Answered")).not.toBeInTheDocument();
      expect(screen.queryByText("Pass Rate")).not.toBeInTheDocument();
    });

    it("highlights the real product features from the README", () => {
      render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      expect(screen.getByText("Structured Lessons")).toBeInTheDocument();
      expect(screen.getByText("Practice Quizzes")).toBeInTheDocument();
      expect(screen.getByText("Timed Mock Exams")).toBeInTheDocument();
      expect(screen.getByText("XP & Levels")).toBeInTheDocument();
      expect(screen.getByText("Leaderboards")).toBeInTheDocument();
      expect(screen.getByText("Achievements")).toBeInTheDocument();
    });

    it("shows a direct dashboard entry point for signed-in users", () => {
      mockIsAuthenticated.mockReturnValue(true);

      render(
        <MemoryRouter>
          <Home />
        </MemoryRouter>
      );

      expect(screen.getByRole("link", { name: "Open dashboard" })).toHaveAttribute("href", "/dashboard");
      expect(screen.getByRole("link", { name: "Continue studying" })).toHaveAttribute("href", "/modules");
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
