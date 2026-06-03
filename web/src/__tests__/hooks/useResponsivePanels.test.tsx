import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell, SIDEBAR_COLLAPSED_WIDTH, SIDEBAR_DEFAULT_WIDTH } from "../../context/ShellContext";
import { useResponsivePanels } from "../../hooks/useResponsivePanels";
import type { ReactNode } from "react";

// Mock useBreakpoint with controllable return value
const mockBreakpoint = { isDesktop: true, isWideDesktop: true };
vi.mock("../../hooks/useBreakpoint", () => ({
  useBreakpoint: () => mockBreakpoint,
}));

function createWrapper(initialRoute: string = "/") {
  return function Wrapper({ children }: { children: ReactNode }) {
    return (
      <MemoryRouter initialEntries={[initialRoute]}>
        <ShellProvider>{children}</ShellProvider>
      </MemoryRouter>
    );
  };
}

/**
 * Combined hook that exposes both useResponsivePanels and useShell
 * for test assertions.
 */
function useResponsivePanelsWithShell() {
  useResponsivePanels();
  return useShell();
}

describe("useResponsivePanels", () => {
  beforeEach(() => {
    // Default: wide desktop
    mockBreakpoint.isDesktop = true;
    mockBreakpoint.isWideDesktop = true;
    // Mock window.innerWidth for constraint checks
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1440,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("initial state based on viewport", () => {
    it("expands sidebar on wide desktop (≥1280px) on mount", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = true;

      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/"),
      });

      expect(result.current.state.sidebarCollapsed).toBe(false);
      expect(result.current.state.sidebarWidth).toBe(SIDEBAR_DEFAULT_WIDTH);
    });

    it("collapses sidebar on narrow desktop (1024–1279px) on mount", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = false;

      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/"),
      });

      expect(result.current.state.sidebarCollapsed).toBe(true);
      expect(result.current.state.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);
    });

    it("opens detail panel on wide desktop when page context configures it", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = true;

      // /subtopics/:subtopicId/lesson has showDetailPanel: true
      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/subtopics/123/lesson"),
      });

      expect(result.current.state.detailPanelOpen).toBe(true);
    });

    it("hides detail panel on narrow desktop even if page configures it", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = false;

      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/subtopics/123/lesson"),
      });

      expect(result.current.state.detailPanelOpen).toBe(false);
    });
  });

  describe("breakpoint transitions", () => {
    it("collapses sidebar when transitioning from wide to narrow desktop", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = true;

      const { result, rerender } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/"),
      });

      expect(result.current.state.sidebarCollapsed).toBe(false);

      // Simulate breakpoint change to narrow desktop
      act(() => {
        mockBreakpoint.isWideDesktop = false;
      });
      rerender();

      expect(result.current.state.sidebarCollapsed).toBe(true);
      expect(result.current.state.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);
    });

    it("expands sidebar when transitioning from narrow to wide desktop", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = false;

      const { result, rerender } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/"),
      });

      expect(result.current.state.sidebarCollapsed).toBe(true);

      // Simulate breakpoint change to wide desktop
      act(() => {
        mockBreakpoint.isWideDesktop = true;
      });
      rerender();

      expect(result.current.state.sidebarCollapsed).toBe(false);
      expect(result.current.state.sidebarWidth).toBe(SIDEBAR_DEFAULT_WIDTH);
    });
  });

  describe("auto-collapse constraint (50% viewport rule)", () => {
    it("closes detail panel when panels exceed 50% of viewport width", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = true;
      // Set a narrow viewport where sidebar(240) + detail(320) = 560 > 50% of 1000 = 500
      Object.defineProperty(window, "innerWidth", { value: 1000, writable: true, configurable: true });

      // Use a route with detail panel configured
      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/subtopics/123/lesson"),
      });

      // The hook should have opened the detail panel (wide desktop + showDetailPanel)
      // but then immediately closed it due to the constraint check
      // sidebar(240) + detail(320) = 560 > 500 (50% of 1000), and content = 1000 - 560 - 8 = 432 < 500
      expect(result.current.state.detailPanelOpen).toBe(false);
    });

    it("keeps detail panel open when panels fit within 50% of viewport", () => {
      mockBreakpoint.isDesktop = true;
      mockBreakpoint.isWideDesktop = true;
      // Set a wide viewport: sidebar(240) + detail(320) = 560, 50% of 1440 = 720, content = 1440 - 560 - 8 = 872 > 500
      Object.defineProperty(window, "innerWidth", { value: 1440, writable: true, configurable: true });

      const { result } = renderHook(() => useResponsivePanelsWithShell(), {
        wrapper: createWrapper("/subtopics/123/lesson"),
      });

      expect(result.current.state.detailPanelOpen).toBe(true);
    });
  });
});
