import { describe, it, expect, vi } from "vitest";
import { render, act } from "@testing-library/react";
import {
  ShellProvider,
  useShell,
  shellReducer,
  SIDEBAR_DEFAULT_WIDTH,
  SIDEBAR_COLLAPSED_WIDTH,
  DETAIL_PANEL_DEFAULT_WIDTH,
} from "../../context/ShellContext";

// --- Reducer unit tests ---

describe("shellReducer", () => {
  const defaultState = () => ({
    sidebarCollapsed: false,
    sidebarWidth: SIDEBAR_DEFAULT_WIDTH,
    detailPanelOpen: false,
    detailPanelWidth: DETAIL_PANEL_DEFAULT_WIDTH,
    focusModeActive: false,
    commandPaletteOpen: false,
    shortcutsOverlayOpen: false,
    preFocusModeState: null,
  });

  describe("sidebar actions", () => {
    it("TOGGLE_SIDEBAR collapses when expanded", () => {
      const state = defaultState();
      const next = shellReducer(state, { type: "TOGGLE_SIDEBAR" });
      expect(next.sidebarCollapsed).toBe(true);
      expect(next.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);
    });

    it("TOGGLE_SIDEBAR expands when collapsed", () => {
      const state = { ...defaultState(), sidebarCollapsed: true, sidebarWidth: SIDEBAR_COLLAPSED_WIDTH };
      const next = shellReducer(state, { type: "TOGGLE_SIDEBAR" });
      expect(next.sidebarCollapsed).toBe(false);
      expect(next.sidebarWidth).toBe(SIDEBAR_DEFAULT_WIDTH);
    });

    it("SET_SIDEBAR_WIDTH updates width and sets collapsed if at collapsed width", () => {
      const state = defaultState();
      const next = shellReducer(state, { type: "SET_SIDEBAR_WIDTH", width: SIDEBAR_COLLAPSED_WIDTH });
      expect(next.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);
      expect(next.sidebarCollapsed).toBe(true);
    });

    it("SET_SIDEBAR_WIDTH sets collapsed to false for widths above collapsed", () => {
      const state = { ...defaultState(), sidebarCollapsed: true, sidebarWidth: SIDEBAR_COLLAPSED_WIDTH };
      const next = shellReducer(state, { type: "SET_SIDEBAR_WIDTH", width: 200 });
      expect(next.sidebarWidth).toBe(200);
      expect(next.sidebarCollapsed).toBe(false);
    });

    it("COLLAPSE_SIDEBAR sets collapsed state", () => {
      const state = defaultState();
      const next = shellReducer(state, { type: "COLLAPSE_SIDEBAR" });
      expect(next.sidebarCollapsed).toBe(true);
      expect(next.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);
    });

    it("EXPAND_SIDEBAR restores default width", () => {
      const state = { ...defaultState(), sidebarCollapsed: true, sidebarWidth: SIDEBAR_COLLAPSED_WIDTH };
      const next = shellReducer(state, { type: "EXPAND_SIDEBAR" });
      expect(next.sidebarCollapsed).toBe(false);
      expect(next.sidebarWidth).toBe(SIDEBAR_DEFAULT_WIDTH);
    });
  });

  describe("detail panel actions", () => {
    it("TOGGLE_DETAIL_PANEL opens when closed", () => {
      const state = defaultState();
      const next = shellReducer(state, { type: "TOGGLE_DETAIL_PANEL" });
      expect(next.detailPanelOpen).toBe(true);
    });

    it("TOGGLE_DETAIL_PANEL closes when open", () => {
      const state = { ...defaultState(), detailPanelOpen: true };
      const next = shellReducer(state, { type: "TOGGLE_DETAIL_PANEL" });
      expect(next.detailPanelOpen).toBe(false);
    });

    it("SET_DETAIL_PANEL_WIDTH updates width", () => {
      const state = defaultState();
      const next = shellReducer(state, { type: "SET_DETAIL_PANEL_WIDTH", width: 400 });
      expect(next.detailPanelWidth).toBe(400);
    });
  });

  describe("focus mode (Requirement 8.3)", () => {
    it("ENTER_FOCUS_MODE snapshots current state and activates", () => {
      const state = { ...defaultState(), sidebarWidth: 300, detailPanelOpen: true };
      const next = shellReducer(state, { type: "ENTER_FOCUS_MODE" });
      expect(next.focusModeActive).toBe(true);
      expect(next.preFocusModeState).toEqual({
        sidebarCollapsed: false,
        sidebarWidth: 300,
        detailPanelOpen: true,
      });
    });

    it("EXIT_FOCUS_MODE restores from snapshot", () => {
      const state = {
        ...defaultState(),
        focusModeActive: true,
        sidebarCollapsed: true,
        sidebarWidth: SIDEBAR_COLLAPSED_WIDTH,
        detailPanelOpen: false,
        preFocusModeState: {
          sidebarCollapsed: false,
          sidebarWidth: 280,
          detailPanelOpen: true,
        },
      };
      const next = shellReducer(state, { type: "EXIT_FOCUS_MODE" });
      expect(next.focusModeActive).toBe(false);
      expect(next.sidebarCollapsed).toBe(false);
      expect(next.sidebarWidth).toBe(280);
      expect(next.detailPanelOpen).toBe(true);
      expect(next.preFocusModeState).toBeNull();
    });

    it("EXIT_FOCUS_MODE without snapshot just deactivates", () => {
      const state = { ...defaultState(), focusModeActive: true, preFocusModeState: null };
      const next = shellReducer(state, { type: "EXIT_FOCUS_MODE" });
      expect(next.focusModeActive).toBe(false);
      expect(next.preFocusModeState).toBeNull();
    });

    it("focus mode round-trip restores exact state", () => {
      const initial = {
        ...defaultState(),
        sidebarCollapsed: false,
        sidebarWidth: 300,
        detailPanelOpen: true,
      };
      const afterEnter = shellReducer(initial, { type: "ENTER_FOCUS_MODE" });
      const afterExit = shellReducer(afterEnter, { type: "EXIT_FOCUS_MODE" });

      expect(afterExit.sidebarCollapsed).toBe(initial.sidebarCollapsed);
      expect(afterExit.sidebarWidth).toBe(initial.sidebarWidth);
      expect(afterExit.detailPanelOpen).toBe(initial.detailPanelOpen);
      expect(afterExit.focusModeActive).toBe(false);
    });
  });

  describe("overlay actions", () => {
    it("OPEN_COMMAND_PALETTE opens", () => {
      const next = shellReducer(defaultState(), { type: "OPEN_COMMAND_PALETTE" });
      expect(next.commandPaletteOpen).toBe(true);
    });

    it("CLOSE_COMMAND_PALETTE closes", () => {
      const state = { ...defaultState(), commandPaletteOpen: true };
      const next = shellReducer(state, { type: "CLOSE_COMMAND_PALETTE" });
      expect(next.commandPaletteOpen).toBe(false);
    });

    it("OPEN_SHORTCUTS_OVERLAY opens", () => {
      const next = shellReducer(defaultState(), { type: "OPEN_SHORTCUTS_OVERLAY" });
      expect(next.shortcutsOverlayOpen).toBe(true);
    });

    it("CLOSE_SHORTCUTS_OVERLAY closes", () => {
      const state = { ...defaultState(), shortcutsOverlayOpen: true };
      const next = shellReducer(state, { type: "CLOSE_SHORTCUTS_OVERLAY" });
      expect(next.shortcutsOverlayOpen).toBe(false);
    });
  });

  it("returns same state for unknown action", () => {
    const state = defaultState();
    // @ts-expect-error testing unknown action
    const next = shellReducer(state, { type: "UNKNOWN" });
    expect(next).toBe(state);
  });
});

// --- Provider + Hook tests ---

describe("ShellProvider and useShell", () => {
  it("throws when useShell is used outside provider", () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});

    function BadComponent() {
      useShell();
      return <div>Should not render</div>;
    }

    expect(() => render(<BadComponent />)).toThrow(
      /useShell must be used within a ShellProvider/
    );

    consoleSpy.mockRestore();
  });

  it("provides initial state", () => {
    let capturedState: ReturnType<typeof useShell>["state"] | null = null;

    function Consumer() {
      const { state } = useShell();
      capturedState = state;
      return null;
    }

    render(
      <ShellProvider>
        <Consumer />
      </ShellProvider>
    );

    expect(capturedState).toEqual({
      sidebarCollapsed: false,
      sidebarWidth: SIDEBAR_DEFAULT_WIDTH,
      detailPanelOpen: false,
      detailPanelWidth: DETAIL_PANEL_DEFAULT_WIDTH,
      focusModeActive: false,
      commandPaletteOpen: false,
      shortcutsOverlayOpen: false,
    });
  });

  it("actions mutate state correctly", () => {
    let capturedCtx: ReturnType<typeof useShell> | null = null;

    function Consumer() {
      capturedCtx = useShell();
      return null;
    }

    render(
      <ShellProvider>
        <Consumer />
      </ShellProvider>
    );

    act(() => {
      capturedCtx!.actions.toggleSidebar();
    });

    expect(capturedCtx!.state.sidebarCollapsed).toBe(true);
    expect(capturedCtx!.state.sidebarWidth).toBe(SIDEBAR_COLLAPSED_WIDTH);

    act(() => {
      capturedCtx!.actions.openCommandPalette();
    });

    expect(capturedCtx!.state.commandPaletteOpen).toBe(true);
  });

  it("does not expose preFocusModeState in public state", () => {
    let capturedState: ReturnType<typeof useShell>["state"] | null = null;

    function Consumer() {
      const { state } = useShell();
      capturedState = state;
      return null;
    }

    render(
      <ShellProvider>
        <Consumer />
      </ShellProvider>
    );

    expect(capturedState).not.toHaveProperty("preFocusModeState");
  });
});
