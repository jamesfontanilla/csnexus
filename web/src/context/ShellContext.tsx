import { createContext, useContext, useReducer, useCallback, useMemo } from "react";

// --- Constants ---

export const SIDEBAR_DEFAULT_WIDTH = 240;
export const SIDEBAR_COLLAPSED_WIDTH = 56;
export const SIDEBAR_MIN_WIDTH = 180;
export const SIDEBAR_MAX_WIDTH = 360;
export const DETAIL_PANEL_DEFAULT_WIDTH = 320;
export const DETAIL_PANEL_MIN_WIDTH = 240;
export const DETAIL_PANEL_MAX_WIDTH = 480;

// --- State Interfaces ---

export interface ShellState {
  sidebarCollapsed: boolean;
  sidebarWidth: number;
  detailPanelOpen: boolean;
  detailPanelWidth: number;
  focusModeActive: boolean;
  commandPaletteOpen: boolean;
  shortcutsOverlayOpen: boolean;
}

interface PreFocusModeState {
  sidebarCollapsed: boolean;
  sidebarWidth: number;
  detailPanelOpen: boolean;
}

interface ShellStateInternal extends ShellState {
  preFocusModeState: PreFocusModeState | null;
}

export interface ShellActions {
  toggleSidebar: () => void;
  setSidebarWidth: (width: number) => void;
  collapseSidebar: () => void;
  expandSidebar: () => void;
  toggleDetailPanel: () => void;
  setDetailPanelWidth: (width: number) => void;
  enterFocusMode: () => void;
  exitFocusMode: () => void;
  openCommandPalette: () => void;
  closeCommandPalette: () => void;
  openShortcutsOverlay: () => void;
  closeShortcutsOverlay: () => void;
}

// --- Reducer Actions ---

type ShellAction =
  | { type: "TOGGLE_SIDEBAR" }
  | { type: "SET_SIDEBAR_WIDTH"; width: number }
  | { type: "COLLAPSE_SIDEBAR" }
  | { type: "EXPAND_SIDEBAR" }
  | { type: "TOGGLE_DETAIL_PANEL" }
  | { type: "SET_DETAIL_PANEL_WIDTH"; width: number }
  | { type: "ENTER_FOCUS_MODE" }
  | { type: "EXIT_FOCUS_MODE" }
  | { type: "OPEN_COMMAND_PALETTE" }
  | { type: "CLOSE_COMMAND_PALETTE" }
  | { type: "OPEN_SHORTCUTS_OVERLAY" }
  | { type: "CLOSE_SHORTCUTS_OVERLAY" };

// --- Initial State ---

const initialState: ShellStateInternal = {
  sidebarCollapsed: false,
  sidebarWidth: SIDEBAR_DEFAULT_WIDTH,
  detailPanelOpen: false,
  detailPanelWidth: DETAIL_PANEL_DEFAULT_WIDTH,
  focusModeActive: false,
  commandPaletteOpen: false,
  shortcutsOverlayOpen: false,
  preFocusModeState: null,
};

// --- Reducer ---

export function shellReducer(
  state: ShellStateInternal,
  action: ShellAction
): ShellStateInternal {
  switch (action.type) {
    case "TOGGLE_SIDEBAR":
      return {
        ...state,
        sidebarCollapsed: !state.sidebarCollapsed,
        sidebarWidth: state.sidebarCollapsed
          ? SIDEBAR_DEFAULT_WIDTH
          : SIDEBAR_COLLAPSED_WIDTH,
      };

    case "SET_SIDEBAR_WIDTH":
      return {
        ...state,
        sidebarWidth: action.width,
        sidebarCollapsed: action.width <= SIDEBAR_COLLAPSED_WIDTH,
      };

    case "COLLAPSE_SIDEBAR":
      return {
        ...state,
        sidebarCollapsed: true,
        sidebarWidth: SIDEBAR_COLLAPSED_WIDTH,
      };

    case "EXPAND_SIDEBAR":
      return {
        ...state,
        sidebarCollapsed: false,
        sidebarWidth: SIDEBAR_DEFAULT_WIDTH,
      };

    case "TOGGLE_DETAIL_PANEL":
      return {
        ...state,
        detailPanelOpen: !state.detailPanelOpen,
      };

    case "SET_DETAIL_PANEL_WIDTH":
      return {
        ...state,
        detailPanelWidth: action.width,
      };

    case "ENTER_FOCUS_MODE":
      return {
        ...state,
        focusModeActive: true,
        preFocusModeState: {
          sidebarCollapsed: state.sidebarCollapsed,
          sidebarWidth: state.sidebarWidth,
          detailPanelOpen: state.detailPanelOpen,
        },
      };

    case "EXIT_FOCUS_MODE": {
      const snapshot = state.preFocusModeState;
      if (snapshot) {
        return {
          ...state,
          focusModeActive: false,
          sidebarCollapsed: snapshot.sidebarCollapsed,
          sidebarWidth: snapshot.sidebarWidth,
          detailPanelOpen: snapshot.detailPanelOpen,
          preFocusModeState: null,
        };
      }
      return {
        ...state,
        focusModeActive: false,
        preFocusModeState: null,
      };
    }

    case "OPEN_COMMAND_PALETTE":
      return { ...state, commandPaletteOpen: true };

    case "CLOSE_COMMAND_PALETTE":
      return { ...state, commandPaletteOpen: false };

    case "OPEN_SHORTCUTS_OVERLAY":
      return { ...state, shortcutsOverlayOpen: true };

    case "CLOSE_SHORTCUTS_OVERLAY":
      return { ...state, shortcutsOverlayOpen: false };

    default:
      return state;
  }
}

// --- Context ---

interface ShellContextValue {
  state: ShellState;
  actions: ShellActions;
}

const ShellContext = createContext<ShellContextValue | null>(null);

// --- Provider ---

export function ShellProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(shellReducer, initialState);

  const toggleSidebar = useCallback(() => dispatch({ type: "TOGGLE_SIDEBAR" }), []);
  const setSidebarWidth = useCallback(
    (width: number) => dispatch({ type: "SET_SIDEBAR_WIDTH", width }),
    []
  );
  const collapseSidebar = useCallback(() => dispatch({ type: "COLLAPSE_SIDEBAR" }), []);
  const expandSidebar = useCallback(() => dispatch({ type: "EXPAND_SIDEBAR" }), []);
  const toggleDetailPanel = useCallback(() => dispatch({ type: "TOGGLE_DETAIL_PANEL" }), []);
  const setDetailPanelWidth = useCallback(
    (width: number) => dispatch({ type: "SET_DETAIL_PANEL_WIDTH", width }),
    []
  );
  const enterFocusMode = useCallback(() => dispatch({ type: "ENTER_FOCUS_MODE" }), []);
  const exitFocusMode = useCallback(() => dispatch({ type: "EXIT_FOCUS_MODE" }), []);
  const openCommandPalette = useCallback(() => dispatch({ type: "OPEN_COMMAND_PALETTE" }), []);
  const closeCommandPalette = useCallback(() => dispatch({ type: "CLOSE_COMMAND_PALETTE" }), []);
  const openShortcutsOverlay = useCallback(
    () => dispatch({ type: "OPEN_SHORTCUTS_OVERLAY" }),
    []
  );
  const closeShortcutsOverlay = useCallback(
    () => dispatch({ type: "CLOSE_SHORTCUTS_OVERLAY" }),
    []
  );

  const actions: ShellActions = useMemo(
    () => ({
      toggleSidebar,
      setSidebarWidth,
      collapseSidebar,
      expandSidebar,
      toggleDetailPanel,
      setDetailPanelWidth,
      enterFocusMode,
      exitFocusMode,
      openCommandPalette,
      closeCommandPalette,
      openShortcutsOverlay,
      closeShortcutsOverlay,
    }),
    [
      toggleSidebar,
      setSidebarWidth,
      collapseSidebar,
      expandSidebar,
      toggleDetailPanel,
      setDetailPanelWidth,
      enterFocusMode,
      exitFocusMode,
      openCommandPalette,
      closeCommandPalette,
      openShortcutsOverlay,
      closeShortcutsOverlay,
    ]
  );

  const value: ShellContextValue = useMemo(
    () => ({
      state: {
        sidebarCollapsed: state.sidebarCollapsed,
        sidebarWidth: state.sidebarWidth,
        detailPanelOpen: state.detailPanelOpen,
        detailPanelWidth: state.detailPanelWidth,
        focusModeActive: state.focusModeActive,
        commandPaletteOpen: state.commandPaletteOpen,
        shortcutsOverlayOpen: state.shortcutsOverlayOpen,
      },
      actions,
    }),
    [state, actions]
  );

  return (
    <ShellContext.Provider value={value}>{children}</ShellContext.Provider>
  );
}

// --- Hook ---

export function useShell(): ShellContextValue {
  const ctx = useContext(ShellContext);
  if (!ctx) {
    throw new Error(
      "useShell must be used within a ShellProvider. " +
        "Wrap your component tree with <ShellProvider> before calling useShell()."
    );
  }
  return ctx;
}
