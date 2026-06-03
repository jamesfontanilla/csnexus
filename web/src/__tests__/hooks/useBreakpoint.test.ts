import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useBreakpoint } from "../../hooks/useBreakpoint";

type ChangeListener = (event: { matches: boolean }) => void;

function createMockMatchMedia(initialDesktop: boolean, initialWide: boolean) {
  const listeners: Record<string, ChangeListener[]> = {};
  const mqls: Record<string, { matches: boolean }> = {};

  const mockMatchMedia = (query: string) => {
    const key = query;
    if (!listeners[key]) listeners[key] = [];

    let matches: boolean;
    if (query === "(min-width: 1024px)") {
      matches = initialDesktop;
    } else if (query === "(min-width: 1280px)") {
      matches = initialWide;
    } else {
      matches = false;
    }

    const mql = {
      matches,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: (_event: string, handler: ChangeListener) => {
        listeners[key].push(handler);
      },
      removeEventListener: (_event: string, handler: ChangeListener) => {
        listeners[key] = listeners[key].filter((h) => h !== handler);
      },
      dispatchEvent: () => false,
    };

    mqls[key] = mql;
    return mql;
  };

  const fireChange = (query: string, matches: boolean) => {
    // Update the mql's matches property so the hook reads the current state
    if (mqls[query]) {
      mqls[query].matches = matches;
    }
    if (listeners[query]) {
      listeners[query].forEach((handler) => handler({ matches }));
    }
  };

  return { mockMatchMedia, fireChange };
}

describe("useBreakpoint", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns isDesktop: false and isWideDesktop: false below 1024px", () => {
    const { mockMatchMedia } = createMockMatchMedia(false, false);
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { result } = renderHook(() => useBreakpoint());
    expect(result.current.isDesktop).toBe(false);
    expect(result.current.isWideDesktop).toBe(false);
  });

  it("returns isDesktop: true and isWideDesktop: false between 1024–1279px", () => {
    const { mockMatchMedia } = createMockMatchMedia(true, false);
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { result } = renderHook(() => useBreakpoint());
    expect(result.current.isDesktop).toBe(true);
    expect(result.current.isWideDesktop).toBe(false);
  });

  it("returns isDesktop: true and isWideDesktop: true at ≥1280px", () => {
    const { mockMatchMedia } = createMockMatchMedia(true, true);
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { result } = renderHook(() => useBreakpoint());
    expect(result.current.isDesktop).toBe(true);
    expect(result.current.isWideDesktop).toBe(true);
  });

  it("debounces state updates by 100ms on media query change", () => {
    const { mockMatchMedia, fireChange } = createMockMatchMedia(false, false);
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { result } = renderHook(() => useBreakpoint());
    expect(result.current.isDesktop).toBe(false);

    // Simulate viewport crossing 1024px
    act(() => {
      fireChange("(min-width: 1024px)", true);
    });

    // State should NOT update immediately (debounce pending)
    expect(result.current.isDesktop).toBe(false);

    // Advance past the 100ms debounce
    act(() => {
      vi.advanceTimersByTime(100);
    });

    expect(result.current.isDesktop).toBe(true);
  });

  it("debounces multiple rapid changes and only applies the last state", () => {
    const { mockMatchMedia, fireChange } = createMockMatchMedia(false, false);
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { result } = renderHook(() => useBreakpoint());

    // Rapid toggling (e.g., window snapping)
    act(() => {
      fireChange("(min-width: 1024px)", true);
    });
    act(() => {
      vi.advanceTimersByTime(50);
    });
    act(() => {
      fireChange("(min-width: 1024px)", false);
    });

    // Only 50ms has passed since last change, nothing committed yet
    expect(result.current.isDesktop).toBe(false);

    // Advance the full 100ms from the last change
    act(() => {
      vi.advanceTimersByTime(100);
    });

    // Should reflect the final state (false, since last fire was false)
    expect(result.current.isDesktop).toBe(false);
  });

  it("cleans up listeners on unmount", () => {
    const removeListeners: Array<() => void> = [];
    const mockMatchMedia = (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: (_event: string, _handler: ChangeListener) => {},
      removeEventListener: (_event: string, _handler: ChangeListener) => {
        removeListeners.push(() => {});
      },
      dispatchEvent: () => false,
    });

    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: mockMatchMedia,
    });

    const { unmount } = renderHook(() => useBreakpoint());
    unmount();

    // Two media queries should have their listeners removed
    expect(removeListeners.length).toBe(2);
  });
});
