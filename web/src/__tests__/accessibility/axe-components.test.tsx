import { describe, it, expect, vi, beforeAll, afterEach } from "vitest";
import { render, cleanup } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

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
  useMotionValue: (initial: number) => ({
    get: () => initial,
    set: vi.fn(),
    onChange: () => () => {},
  }),
  animate: vi.fn().mockReturnValue({ stop: vi.fn() }),
}));

vi.mock("../../design-system", () => ({
  scaleIn: { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } },
  springGentle: { type: "spring" },
  springDefault: { type: "spring" },
  useReducedMotion: () => false,
}));

vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => false,
}));

vi.mock("../../hooks/useFocusTrap", () => ({
  useFocusTrap: () => ({ current: null }),
}));

beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
});

afterEach(() => {
  cleanup();
});

import { GlassModal } from "../../components/GlassModal";
import { GlassButton } from "../../components/GlassButton";
import { ProgressRing } from "../../components/ProgressRing";
import { BottomNav } from "../../components/BottomNav";

describe("Accessibility: axe-core component audits (Task 24.2)", () => {
  it("GlassModal has no accessibility violations", async () => {
    const { container } = render(
      <GlassModal isOpen={true} onClose={() => {}} title="Test Modal">
        <p>Modal content</p>
      </GlassModal>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("GlassButton (icon-only with aria-label) has no accessibility violations", async () => {
    const { container } = render(
      <GlassButton aria-label="Close menu" iconLeft={<span>✕</span>} />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("ProgressRing has no accessibility violations", async () => {
    const { container } = render(
      <ProgressRing size={120} value={75} label="Progress: 75%" />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("BottomNav has no accessibility violations", async () => {
    const { container } = render(
      <MemoryRouter initialEntries={["/modules"]}>
        <BottomNav />
      </MemoryRouter>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
