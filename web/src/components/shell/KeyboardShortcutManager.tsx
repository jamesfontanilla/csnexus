import { useEffect } from "react";
import { useShell } from "../../context/ShellContext";

/**
 * Renders no DOM. Registers global keydown listeners that dispatch
 * shell actions for keyboard shortcuts.
 *
 * Shortcuts:
 *   Cmd/Ctrl+K       → open command palette
 *   Cmd/Ctrl+B       → toggle sidebar
 *   Cmd/Ctrl+\       → toggle detail panel
 *   Cmd/Ctrl+Shift+F → toggle focus mode
 *   Escape           → close topmost overlay
 *   ?                → open shortcuts cheat sheet
 *
 * Suppressed when focused element is <input>, <textarea>, contenteditable,
 * or within a [data-suppress-shortcuts] container.
 */
export function KeyboardShortcutManager(): null {
  const { state, actions } = useShell();

  useEffect(() => {
    function shouldSuppressShortcut(event: KeyboardEvent): boolean {
      const target = event.target as HTMLElement | null;
      if (!target || !target.tagName) return false;

      // Suppress when focused on text input elements
      const tagName = target.tagName.toLowerCase();
      if (tagName === "input" || tagName === "textarea") return true;
      if (target.isContentEditable || target.contentEditable === "true") return true;

      // Suppress when within a data-suppress-shortcuts container
      if (target.closest?.("[data-suppress-shortcuts]")) return true;

      return false;
    }

    function handleKeyDown(event: KeyboardEvent): void {
      const mod = event.metaKey || event.ctrlKey;

      // Escape always works (even in inputs) — closes topmost overlay
      if (event.key === "Escape") {
        if (state.commandPaletteOpen) {
          event.preventDefault();
          actions.closeCommandPalette();
          return;
        }
        if (state.shortcutsOverlayOpen) {
          event.preventDefault();
          actions.closeShortcutsOverlay();
          return;
        }
        if (state.detailPanelOpen) {
          event.preventDefault();
          actions.toggleDetailPanel();
          return;
        }
        if (state.focusModeActive) {
          event.preventDefault();
          actions.exitFocusMode();
          return;
        }
        return;
      }

      // All other shortcuts suppressed in text inputs
      if (shouldSuppressShortcut(event)) return;

      // Cmd/Ctrl+K → open command palette
      if (mod && event.key.toLowerCase() === "k" && !event.shiftKey) {
        event.preventDefault();
        actions.openCommandPalette();
        return;
      }

      // Cmd/Ctrl+B → toggle sidebar
      if (mod && event.key.toLowerCase() === "b" && !event.shiftKey) {
        event.preventDefault();
        actions.toggleSidebar();
        return;
      }

      // Cmd/Ctrl+\ → toggle detail panel
      if (mod && event.key === "\\" && !event.shiftKey) {
        event.preventDefault();
        actions.toggleDetailPanel();
        return;
      }

      // Cmd/Ctrl+Shift+F → toggle focus mode
      if (mod && event.shiftKey && event.key.toLowerCase() === "f") {
        event.preventDefault();
        if (state.focusModeActive) {
          actions.exitFocusMode();
        } else {
          actions.enterFocusMode();
        }
        return;
      }

      // ? (no modifier) → open shortcuts cheat sheet
      if (event.key === "?" && !mod && !event.altKey) {
        event.preventDefault();
        actions.openShortcutsOverlay();
        return;
      }
    }

    function handleWindowBlur(): void {
      // Clear any stale modifier state when user switches windows
      // (e.g., holds Cmd, switches to another app, releases Cmd there).
      // No explicit modifier tracking needed since we read event.metaKey/ctrlKey
      // per-event, but this is a hook point if we ever need stateful modifier tracking.
    }

    document.addEventListener("keydown", handleKeyDown);
    window.addEventListener("blur", handleWindowBlur);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("blur", handleWindowBlur);
    };
  }, [state, actions]);

  return null;
}
