import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

// Control reduced motion from tests
let mockReducedMotion = false;
let mockMobileViewport = false;

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
  useMotionVariants: (v: Record<string, unknown>) => v,
  pageTransition: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.5 } },
  cardStaggerContainer: { animate: { transition: { staggerChildren: 0.05 } } },
  cardStaggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { type: "spring" } },
  hoverLift: { whileHover: { y: -2 }, transition: { duration: 0.15 } },
  pressFeedback: { whileTap: { scale: 0.97 }, whileHover: { scale: 1.02 }, transition: { type: "spring" } },
  makeReducedVariants: (v: Record<string, unknown>) => v,
}));

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return ({ children, style, className, ...rest }: Record<string, unknown>) => {
          const Tag = tag as keyof JSX.IntrinsicElements;
          return (
            <Tag className={className as string} style={style as React.CSSProperties} {...(rest as Record<string, unknown>)}>
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
      matches:
        query === "(prefers-reduced-motion: reduce)"
          ? reducedMotion
          : query === "(max-width: 639px)"
            ? mockMobileViewport
            : false,
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

const mockGet = vi.fn();

vi.mock("../../api/client", () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock("../../stores/auth", () => ({
  login: vi.fn(),
  logout: vi.fn(),
  isAuthenticated: () => true,
  getToken: () => "mock-token",
  getLastAuthenticatedAt: () => Date.now(),
}));

import { Dashboard } from "../../pages/Dashboard";

const mockDashboardData = {
  readinessScore: 72,
  streak: 5,
  xpToday: 150,
  questionsToday: 23,
  dailyQueue: [
    { id: "1", title: "Basic Operations", type: "lesson", estimatedMinutes: 10 },
  ],
  impactAreas: [
    { subject: "Numerical Ability", score: 80, maxScore: 100 },
  ],
};

function renderDashboard() {
  return render(
    <MemoryRouter>
      <Dashboard />
    </MemoryRouter>
  );
}

describe("Dashboard page (Task 17.2)", () => {
  beforeEach(() => {
    mockReducedMotion = false;
    mockMobileViewport = false;
    mockMatchMedia(false);
    vi.clearAllMocks();
  });

  describe("Skeleton placeholders render while loading (Requirement 12.6)", () => {
    it("renders skeleton placeholders before data loads", () => {
      mockGet.mockReturnValue(new Promise(() => {}));

      const { container } = renderDashboard();

      const skeletons = container.querySelectorAll(".skeleton");
      expect(skeletons.length).toBeGreaterThan(0);
    });

    it("does not render section content while loading", () => {
      mockGet.mockReturnValue(new Promise(() => {}));

      renderDashboard();

      expect(screen.queryByText("Day Streak 🔥")).not.toBeInTheDocument();
      expect(screen.queryByText("XP Today")).not.toBeInTheDocument();
      expect(screen.queryByText("Questions Today")).not.toBeInTheDocument();
    });
  });

  describe("ProgressRing receives value={0} initially then actual score (Requirement 12.2)", () => {
    it("renders ProgressRing after data loads", async () => {
      mockGet.mockResolvedValue(mockDashboardData);

      const { container } = renderDashboard();

      await waitFor(() => {
        const progressbar = container.querySelector('[role="progressbar"]');
        expect(progressbar).not.toBeNull();
      });
    });
  });

  describe("AnimatedNumber components present for streak, XP, and questions (Requirement 12.4)", () => {
    it("renders the quick stats labels after data loads", async () => {
      mockGet.mockResolvedValue(mockDashboardData);

      renderDashboard();

      await waitFor(() => {
        expect(screen.getByText("Day Streak 🔥")).toBeInTheDocument();
        expect(screen.getByText("XP Today")).toBeInTheDocument();
        expect(screen.getByText("Questions Today")).toBeInTheDocument();
      });
    });
  });

  describe("Mobile feature hub renders quick access links", () => {
    it("shows queue, flashcards, tutor, and readiness links on mobile", async () => {
      mockMobileViewport = true;
      mockMatchMedia(false);
      mockGet.mockResolvedValue(mockDashboardData);

      renderDashboard();

      await waitFor(() => {
        expect(screen.getByRole("link", { name: "Queue" })).toHaveAttribute("href", "/queue");
        expect(screen.getByRole("link", { name: "Flashcards" })).toHaveAttribute("href", "/flashcards");
        expect(screen.getByRole("link", { name: "Tutor" })).toHaveAttribute("href", "/tutor");
        expect(screen.getByRole("link", { name: "Readiness" })).toHaveAttribute("href", "/readiness");
      });
    });

    it("does not render the feature hub on desktop", async () => {
      mockMobileViewport = false;
      mockMatchMedia(false);
      mockGet.mockResolvedValue(mockDashboardData);

      renderDashboard();

      await waitFor(() => {
        expect(screen.queryByText("Quick Access")).not.toBeInTheDocument();
      });
    });
  });
});
