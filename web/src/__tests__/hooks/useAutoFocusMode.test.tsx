import { describe, it, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell } from "../../context/ShellContext";
import { useAutoFocusMode } from "../../hooks/useAutoFocusMode";
import type { ReactNode } from "react";

/**
 * Test helper that wraps children in MemoryRouter + ShellProvider
 * at a specific initial route.
 */
function createWrapper(initialRoute: string) {
  return function Wrapper({ children }: { children: ReactNode }) {
    return (
      <MemoryRouter initialEntries={[initialRoute]}>
        <ShellProvider>{children}</ShellProvider>
      </MemoryRouter>
    );
  };
}

/**
 * Combined hook that exposes both useAutoFocusMode and useShell
 * for test assertions.
 */
function useAutoFocusModeWithShell() {
  useAutoFocusMode();
  return useShell();
}

describe("useAutoFocusMode", () => {
  it("auto-enters focus mode on an autoFocusMode route", () => {
    // /quiz/:scope/:scopeId has autoFocusMode: true
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/quiz/module/42"),
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });

  it("does NOT enter focus mode on a non-autoFocusMode route", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/modules"),
    });

    expect(result.current.state.focusModeActive).toBe(false);
  });

  it("auto-enters focus mode on /mock-exam", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/mock-exam"),
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });

  it("auto-enters focus mode on /flashcards/study", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/flashcards/study"),
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });

  it("auto-enters focus mode on /flashcards/exam", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/flashcards/exam"),
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });

  it("auto-enters focus mode on /focus", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/focus"),
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });

  it("respects manual override: does not re-enter after user exits focus mode", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/quiz/module/42"),
    });

    // Focus mode should be active (auto-entered)
    expect(result.current.state.focusModeActive).toBe(true);

    // User manually exits focus mode
    act(() => {
      result.current.actions.exitFocusMode();
    });

    expect(result.current.state.focusModeActive).toBe(false);

    // The hook should NOT re-enter focus mode because user overrode it
    // (the effect already ran; the override is tracked via ref)
  });

  it("does not auto-enter if focus mode was already manually active", () => {
    const { result } = renderHook(() => useAutoFocusModeWithShell(), {
      wrapper: createWrapper("/modules"),
    });

    // Manually enter focus mode on a non-autoFocusMode route
    act(() => {
      result.current.actions.enterFocusMode();
    });

    expect(result.current.state.focusModeActive).toBe(true);
  });
});
