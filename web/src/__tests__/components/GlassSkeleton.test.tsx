import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render } from "@testing-library/react";
import { GlassSkeleton } from "../../components/GlassSkeleton";

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

describe("GlassSkeleton", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("lines prop", () => {
    it("renders 3 skeleton bars when lines={3}", () => {
      const { container } = render(<GlassSkeleton lines={3} />);

      const skeletonBars = container.querySelectorAll(".skeleton");
      expect(skeletonBars).toHaveLength(3);
    });

    it("renders correct number of skeleton bars for various line counts", () => {
      const { container: container5 } = render(<GlassSkeleton lines={5} />);
      expect(container5.querySelectorAll(".skeleton")).toHaveLength(5);

      const { container: container1 } = render(<GlassSkeleton lines={1} />);
      expect(container1.querySelectorAll(".skeleton")).toHaveLength(1);
    });

    it("renders skeleton bars with decreasing widths", () => {
      const { container } = render(<GlassSkeleton lines={3} />);

      const skeletonBars = container.querySelectorAll(".skeleton");
      expect(skeletonBars[0]).toHaveStyle({ width: "100%" });
      expect(skeletonBars[1]).toHaveStyle({ width: "85%" });
      expect(skeletonBars[2]).toHaveStyle({ width: "70%" });
    });
  });

  describe("skeleton class and reduced-motion", () => {
    it("applies the .skeleton class to rendered bars", () => {
      const { container } = render(<GlassSkeleton />);

      const skeletonBar = container.querySelector(".skeleton");
      expect(skeletonBar).not.toBeNull();
      expect(skeletonBar).toHaveClass("skeleton");
    });

    it("applies the .skeleton class when prefers-reduced-motion is active", () => {
      mockMatchMedia(true);

      const { container } = render(<GlassSkeleton lines={3} />);

      // The .skeleton class is always applied — the CSS media query handles
      // disabling the animation. We verify the class is present so the
      // @media (prefers-reduced-motion: reduce) rule can take effect.
      const skeletonBars = container.querySelectorAll(".skeleton");
      expect(skeletonBars).toHaveLength(3);
      skeletonBars.forEach((bar) => {
        expect(bar).toHaveClass("skeleton");
      });
    });
  });
});
