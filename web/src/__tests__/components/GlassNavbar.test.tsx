import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

// Control useMediaQuery return value from tests
let mockIsMobile = false;

// Control isAuthenticated return value from tests
let mockAuthenticated = true;

// Mock the useMediaQuery hook
vi.mock("../../pages/content/lesson/useMediaQuery", () => ({
  useMediaQuery: () => mockIsMobile,
}));

// Mock the auth store
vi.mock("../../stores/auth", () => ({
  isAuthenticated: () => mockAuthenticated,
}));

// Mock the API client to prevent real network calls
vi.mock("../../api/client", () => ({
  apiClient: {
    get: vi.fn(() => Promise.resolve({ cumulative_xp: 100, level: 2, streak: 3 })),
  },
}));

// Mock the design-system module
vi.mock("../../design-system", () => ({
  slideDown: { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } },
  springDefault: { type: "spring" },
}));

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return ({ children, className, style, ...rest }: Record<string, unknown>) => {
          const Tag = tag as keyof JSX.IntrinsicElements;
          return (
            <Tag className={className as string} style={style as React.CSSProperties} {...rest}>
              {children as React.ReactNode}
            </Tag>
          );
        };
      },
    }
  ),
  AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  useMotionValue: (initial: number) => ({
    get: () => initial,
    set: vi.fn(),
    onChange: () => () => {},
  }),
  animate: vi.fn().mockReturnValue({ stop: vi.fn() }),
}));

// Mock the design-system/motion module for BottomNav's useReducedMotion
vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => false,
}));

// Import after mocks are set up
import { GlassNavbar } from "../../components/GlassNavbar";

function renderGlassNavbar(initialPath = "/modules") {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <GlassNavbar />
    </MemoryRouter>
  );
}

describe("GlassNavbar mobile/desktop switching", () => {
  beforeEach(() => {
    mockIsMobile = false;
    mockAuthenticated = true;
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.body.style.paddingBottom = "";
  });

  describe("BottomNav renders at viewport < 768px (Requirement 15.1)", () => {
    it("renders BottomNav when viewport is mobile and user is authenticated", () => {
      mockIsMobile = true;
      mockAuthenticated = true;

      const { container } = renderGlassNavbar("/modules");

      const bottomNav = container.querySelector(".bottom-nav");
      expect(bottomNav).not.toBeNull();
    });

    it("does NOT render BottomNav when viewport is desktop", () => {
      mockIsMobile = false;
      mockAuthenticated = true;

      const { container } = renderGlassNavbar("/modules");

      const bottomNav = container.querySelector(".bottom-nav");
      expect(bottomNav).toBeNull();
    });

    it("does NOT render BottomNav when user is not authenticated", () => {
      mockIsMobile = true;
      mockAuthenticated = false;

      const { container } = renderGlassNavbar("/");

      const bottomNav = container.querySelector(".bottom-nav");
      expect(bottomNav).toBeNull();
    });
  });

  describe("Hamburger menu is hidden when BottomNav is active (Requirement 15.3)", () => {
    it("does NOT render hamburger button when BottomNav is active (mobile + authenticated)", () => {
      mockIsMobile = true;
      mockAuthenticated = true;

      const { container } = renderGlassNavbar("/modules");

      const hamburger = container.querySelector(".glass-navbar-hamburger");
      expect(hamburger).toBeNull();
    });

    it("renders hamburger button on desktop when authenticated", () => {
      mockIsMobile = false;
      mockAuthenticated = true;

      const { container } = renderGlassNavbar("/modules");

      const hamburger = container.querySelector(".glass-navbar-hamburger");
      expect(hamburger).not.toBeNull();
    });

    it("does NOT render mobile drawer when BottomNav is active", () => {
      mockIsMobile = true;
      mockAuthenticated = true;

      const { container } = renderGlassNavbar("/modules");

      const drawer = container.querySelector(".glass-mobile-drawer");
      expect(drawer).toBeNull();
    });
  });
});
