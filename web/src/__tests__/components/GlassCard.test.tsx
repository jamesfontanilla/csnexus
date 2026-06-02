import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { GlassCard } from "../../components/GlassCard";

// Mock framer-motion to inspect props passed to the rendered element
vi.mock("framer-motion", () => {
  const actual = vi.importActual("framer-motion");
  return {
    ...actual,
    motion: new Proxy(
      {},
      {
        get: (_target, tag: string) => {
          // Return a component that renders the tag and forwards relevant props
          return ({
            children,
            className,
            style,
            initial,
            animate,
            transition,
            whileHover,
            whileTap,
            ...rest
          }: Record<string, unknown>) => {
            const Tag = tag as keyof JSX.IntrinsicElements;
            return (
              <Tag
                className={className as string}
                style={style as React.CSSProperties}
                data-initial={initial ? JSON.stringify(initial) : undefined}
                data-animate={animate ? JSON.stringify(animate) : undefined}
                data-transition={
                  transition ? JSON.stringify(transition) : undefined
                }
                data-testid="glass-card"
                {...(rest as Record<string, unknown>)}
              >
                {children as React.ReactNode}
              </Tag>
            );
          };
        },
      }
    ),
  };
});

function mockMatchMedia(reducedMotion: boolean) {
  const listeners: Array<(e: MediaQueryListEvent) => void> = [];
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches:
        query === "(prefers-reduced-motion: reduce)" ? reducedMotion : false,
      media: query,
      onchange: null,
      addEventListener: (_event: string, handler: () => void) => {
        listeners.push(handler);
      },
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
}

describe("GlassCard", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("premium prop", () => {
    it("adds .glass-card-premium class when premium={true}", () => {
      const { getByTestId } = render(
        <GlassCard premium={true}>Premium content</GlassCard>
      );

      const card = getByTestId("glass-card");
      expect(card).toHaveClass("glass-card-premium");
    });

    it("does not add .glass-card-premium class when premium={false}", () => {
      const { getByTestId } = render(
        <GlassCard premium={false}>Regular content</GlassCard>
      );

      const card = getByTestId("glass-card");
      expect(card).not.toHaveClass("glass-card-premium");
    });

    it("does not add .glass-card-premium class by default", () => {
      const { getByTestId } = render(<GlassCard>Default content</GlassCard>);

      const card = getByTestId("glass-card");
      expect(card).not.toHaveClass("glass-card-premium");
    });
  });

  describe("entrance animation with prefers-reduced-motion", () => {
    it("applies entrance animation when reduced motion is NOT active", () => {
      mockMatchMedia(false);

      const { getByTestId } = render(
        <GlassCard>Animated content</GlassCard>
      );

      const card = getByTestId("glass-card");
      const initial = card.getAttribute("data-initial");
      const animate = card.getAttribute("data-animate");

      expect(initial).not.toBeNull();
      const initialParsed = JSON.parse(initial!);
      expect(initialParsed).toEqual({ opacity: 0, y: 8 });

      expect(animate).not.toBeNull();
      const animateParsed = JSON.parse(animate!);
      expect(animateParsed).toEqual({ opacity: 1, y: 0 });
    });

    it("skips entrance animation when prefers-reduced-motion is active", () => {
      mockMatchMedia(true);

      const { getByTestId } = render(
        <GlassCard>No animation content</GlassCard>
      );

      const card = getByTestId("glass-card");
      const initial = card.getAttribute("data-initial");
      const animate = card.getAttribute("data-animate");

      // When reduced motion is active, initial and animate should be undefined (no transform/opacity animation)
      expect(initial).toBeNull();
      expect(animate).toBeNull();
    });
  });
});
