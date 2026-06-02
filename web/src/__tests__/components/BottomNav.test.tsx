import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

// Track animate calls to verify reduced-motion behavior
const animateFnMock = vi.fn();
const motionValueSetMock = vi.fn();

// Control reduced motion from tests
let mockReducedMotion = false;

// Mock the design-system/motion module to control useReducedMotion
vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => mockReducedMotion,
}));

// Mock framer-motion
vi.mock("framer-motion", () => {
  return {
    motion: new Proxy(
      {},
      {
        get: (_target, tag: string) => {
          return ({
            children,
            className,
            style,
            ...rest
          }: Record<string, unknown>) => {
            const Tag = tag as keyof JSX.IntrinsicElements;
            return (
              <Tag
                className={className as string}
                style={style as React.CSSProperties}
                data-testid="motion-indicator"
                {...(rest as Record<string, unknown>)}
              >
                {children as React.ReactNode}
              </Tag>
            );
          };
        },
      }
    ),
    useMotionValue: (initial: number) => {
      let value = initial;
      return {
        get: () => value,
        set: (v: number) => {
          value = v;
          motionValueSetMock(v);
        },
        onChange: () => () => {},
      };
    },
    animate: (...args: unknown[]) => {
      animateFnMock(...args);
      return { stop: vi.fn() };
    },
  };
});

function mockMatchMedia(reducedMotion: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches:
        query === "(prefers-reduced-motion: reduce)" ? reducedMotion : false,
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

// Import after mocks are set up
import { BottomNav } from "../../components/BottomNav";

function renderBottomNav(initialPath: string) {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <BottomNav />
    </MemoryRouter>
  );
}

describe("BottomNav", () => {
  beforeEach(() => {
    mockReducedMotion = false;
    mockMatchMedia(false);
    animateFnMock.mockClear();
    motionValueSetMock.mockClear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("Active item has .active class (Requirement 15.2)", () => {
    it("applies .active class to the nav item matching the current route", () => {
      const { container } = renderBottomNav("/modules");

      const activeItems = container.querySelectorAll(".bottom-nav-item.active");
      expect(activeItems).toHaveLength(1);
      expect(activeItems[0]).toHaveTextContent("Study");
    });

    it("applies .active class to Readiness when on /readiness route", () => {
      const { container } = renderBottomNav("/readiness");

      const activeItems = container.querySelectorAll(".bottom-nav-item.active");
      expect(activeItems).toHaveLength(1);
      expect(activeItems[0]).toHaveTextContent("Readiness");
    });

    it("applies .active class to nested routes (e.g. /modules/lesson)", () => {
      const { container } = renderBottomNav("/modules/lesson/123");

      const activeItems = container.querySelectorAll(".bottom-nav-item.active");
      expect(activeItems).toHaveLength(1);
      expect(activeItems[0]).toHaveTextContent("Study");
    });

    it("does not apply .active class to non-matching items", () => {
      const { container } = renderBottomNav("/modules");

      const allItems = container.querySelectorAll(".bottom-nav-item");
      const inactiveItems = container.querySelectorAll(
        ".bottom-nav-item:not(.active)"
      );
      expect(inactiveItems).toHaveLength(allItems.length - 1);
    });
  });

  describe("Indicator animation respects prefers-reduced-motion (Requirement 15.6)", () => {
    it("uses animate() for indicator when reduced motion is NOT active", () => {
      mockReducedMotion = false;
      renderBottomNav("/modules");

      // When reduced motion is off, animate() should be called for the indicator
      expect(animateFnMock).toHaveBeenCalled();
    });

    it("uses .set() instead of animate() when prefers-reduced-motion is active", () => {
      mockReducedMotion = true;
      mockMatchMedia(true);
      animateFnMock.mockClear();
      motionValueSetMock.mockClear();

      // Mock getBoundingClientRect so updateIndicator doesn't bail out
      const originalGetBCR = Element.prototype.getBoundingClientRect;
      Element.prototype.getBoundingClientRect = function () {
        if (this.classList?.contains("bottom-nav-item")) {
          return { left: 80, top: 0, width: 80, height: 56, right: 160, bottom: 56, x: 80, y: 0, toJSON: () => ({}) } as DOMRect;
        }
        if (this.classList?.contains("bottom-nav")) {
          return { left: 0, top: 0, width: 320, height: 56, right: 320, bottom: 56, x: 0, y: 0, toJSON: () => ({}) } as DOMRect;
        }
        return { left: 0, top: 0, width: 0, height: 0, right: 0, bottom: 0, x: 0, y: 0, toJSON: () => ({}) } as DOMRect;
      };

      renderBottomNav("/modules");

      Element.prototype.getBoundingClientRect = originalGetBCR;

      // When reduced motion is on, animate() should NOT be called
      expect(animateFnMock).not.toHaveBeenCalled();
      // Instead, .set() should be called to jump instantly
      expect(motionValueSetMock).toHaveBeenCalled();
    });
  });
});
