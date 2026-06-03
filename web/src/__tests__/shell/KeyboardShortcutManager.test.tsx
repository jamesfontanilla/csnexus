import { describe, it, expect, beforeEach } from "vitest";
import { render, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell, type ShellState } from "../../context/ShellContext";
import { KeyboardShortcutManager } from "../../components/shell/KeyboardShortcutManager";

let shellState: ShellState;

function StateReader() {
  const { state } = useShell();
  shellState = state;
  return null;
}

function renderManager() {
  return render(
    <MemoryRouter>
      <ShellProvider>
        <StateReader />
        <KeyboardShortcutManager />
      </ShellProvider>
    </MemoryRouter>
  );
}

function fireKeyDown(key: string, opts: Partial<KeyboardEventInit> = {}) {
  const event = new KeyboardEvent("keydown", {
    key,
    bubbles: true,
    cancelable: true,
    ...opts,
  });
  act(() => {
    document.dispatchEvent(event);
  });
  return event;
}

describe("KeyboardShortcutManager", () => {
  beforeEach(() => {
    renderManager();
  });

  it("renders no DOM (returns null)", () => {
    const { container } = render(
      <MemoryRouter>
        <ShellProvider>
          <KeyboardShortcutManager />
        </ShellProvider>
      </MemoryRouter>
    );
    // The component returns null, so the only child is from React internals
    expect(container.innerHTML).toBe("");
  });

  describe("Cmd/Ctrl+K → open command palette", () => {
    it("opens command palette on Ctrl+K", () => {
      expect(shellState.commandPaletteOpen).toBe(false);
      fireKeyDown("k", { ctrlKey: true });
      expect(shellState.commandPaletteOpen).toBe(true);
    });

    it("opens command palette on Meta+K (macOS)", () => {
      expect(shellState.commandPaletteOpen).toBe(false);
      fireKeyDown("k", { metaKey: true });
      expect(shellState.commandPaletteOpen).toBe(true);
    });
  });

  describe("Cmd/Ctrl+B → toggle sidebar", () => {
    it("toggles sidebar collapsed state on Ctrl+B", () => {
      expect(shellState.sidebarCollapsed).toBe(false);
      fireKeyDown("b", { ctrlKey: true });
      expect(shellState.sidebarCollapsed).toBe(true);
    });

    it("toggles back on second Ctrl+B", () => {
      fireKeyDown("b", { ctrlKey: true });
      expect(shellState.sidebarCollapsed).toBe(true);
      fireKeyDown("b", { ctrlKey: true });
      expect(shellState.sidebarCollapsed).toBe(false);
    });
  });

  describe("Cmd/Ctrl+\\ → toggle detail panel", () => {
    it("toggles detail panel on Ctrl+\\", () => {
      expect(shellState.detailPanelOpen).toBe(false);
      fireKeyDown("\\", { ctrlKey: true });
      expect(shellState.detailPanelOpen).toBe(true);
    });
  });

  describe("Cmd/Ctrl+Shift+F → toggle focus mode", () => {
    it("enters focus mode on Ctrl+Shift+F", () => {
      expect(shellState.focusModeActive).toBe(false);
      fireKeyDown("f", { ctrlKey: true, shiftKey: true });
      expect(shellState.focusModeActive).toBe(true);
    });

    it("exits focus mode on second Ctrl+Shift+F", () => {
      fireKeyDown("f", { ctrlKey: true, shiftKey: true });
      expect(shellState.focusModeActive).toBe(true);
      fireKeyDown("f", { ctrlKey: true, shiftKey: true });
      expect(shellState.focusModeActive).toBe(false);
    });
  });

  describe("? → open shortcuts cheat sheet", () => {
    it("opens shortcuts overlay when ? is pressed with no modifier", () => {
      expect(shellState.shortcutsOverlayOpen).toBe(false);
      fireKeyDown("?");
      expect(shellState.shortcutsOverlayOpen).toBe(true);
    });

    it("does NOT open shortcuts overlay when Ctrl+? is pressed", () => {
      fireKeyDown("?", { ctrlKey: true });
      expect(shellState.shortcutsOverlayOpen).toBe(false);
    });
  });

  describe("Escape → close topmost overlay", () => {
    it("closes command palette when open", () => {
      fireKeyDown("k", { ctrlKey: true });
      expect(shellState.commandPaletteOpen).toBe(true);
      fireKeyDown("Escape");
      expect(shellState.commandPaletteOpen).toBe(false);
    });

    it("closes shortcuts overlay when open (and palette is closed)", () => {
      fireKeyDown("?");
      expect(shellState.shortcutsOverlayOpen).toBe(true);
      fireKeyDown("Escape");
      expect(shellState.shortcutsOverlayOpen).toBe(false);
    });

    it("closes detail panel when open (and no overlays open)", () => {
      fireKeyDown("\\", { ctrlKey: true });
      expect(shellState.detailPanelOpen).toBe(true);
      fireKeyDown("Escape");
      expect(shellState.detailPanelOpen).toBe(false);
    });

    it("prioritises command palette over shortcuts overlay", () => {
      // Open both
      fireKeyDown("?");
      fireKeyDown("k", { ctrlKey: true });
      expect(shellState.commandPaletteOpen).toBe(true);
      expect(shellState.shortcutsOverlayOpen).toBe(true);
      // Escape closes palette first
      fireKeyDown("Escape");
      expect(shellState.commandPaletteOpen).toBe(false);
      expect(shellState.shortcutsOverlayOpen).toBe(true);
    });

    it("exits focus mode when Escape is pressed and no overlays/panels open", () => {
      fireKeyDown("f", { ctrlKey: true, shiftKey: true });
      expect(shellState.focusModeActive).toBe(true);
      fireKeyDown("Escape");
      expect(shellState.focusModeActive).toBe(false);
    });
  });

  describe("shortcut suppression in text inputs", () => {
    it("suppresses shortcuts when focus is on an input element", () => {
      const input = document.createElement("input");
      document.body.appendChild(input);
      input.focus();

      const event = new KeyboardEvent("keydown", {
        key: "b",
        ctrlKey: true,
        bubbles: true,
        cancelable: true,
      });
      Object.defineProperty(event, "target", { value: input });

      act(() => {
        document.dispatchEvent(event);
      });

      expect(shellState.sidebarCollapsed).toBe(false);
      document.body.removeChild(input);
    });

    it("suppresses shortcuts when focus is on a textarea", () => {
      const textarea = document.createElement("textarea");
      document.body.appendChild(textarea);
      textarea.focus();

      const event = new KeyboardEvent("keydown", {
        key: "k",
        ctrlKey: true,
        bubbles: true,
        cancelable: true,
      });
      Object.defineProperty(event, "target", { value: textarea });

      act(() => {
        document.dispatchEvent(event);
      });

      expect(shellState.commandPaletteOpen).toBe(false);
      document.body.removeChild(textarea);
    });

    it("suppresses shortcuts when focus is on contenteditable element", () => {
      const div = document.createElement("div");
      div.contentEditable = "true";
      document.body.appendChild(div);
      div.focus();

      const event = new KeyboardEvent("keydown", {
        key: "b",
        ctrlKey: true,
        bubbles: true,
        cancelable: true,
      });
      Object.defineProperty(event, "target", { value: div });

      act(() => {
        document.dispatchEvent(event);
      });

      expect(shellState.sidebarCollapsed).toBe(false);
      document.body.removeChild(div);
    });

    it("suppresses shortcuts within [data-suppress-shortcuts] container", () => {
      const container = document.createElement("div");
      container.setAttribute("data-suppress-shortcuts", "");
      const child = document.createElement("div");
      container.appendChild(child);
      document.body.appendChild(container);
      child.focus();

      const event = new KeyboardEvent("keydown", {
        key: "b",
        ctrlKey: true,
        bubbles: true,
        cancelable: true,
      });
      Object.defineProperty(event, "target", { value: child });

      act(() => {
        document.dispatchEvent(event);
      });

      expect(shellState.sidebarCollapsed).toBe(false);
      document.body.removeChild(container);
    });

    it("does NOT suppress Escape even when focused on an input", () => {
      // Open command palette first
      fireKeyDown("k", { ctrlKey: true });
      expect(shellState.commandPaletteOpen).toBe(true);

      // Now Escape from an input should still close it
      const input = document.createElement("input");
      document.body.appendChild(input);
      input.focus();

      const event = new KeyboardEvent("keydown", {
        key: "Escape",
        bubbles: true,
        cancelable: true,
      });
      Object.defineProperty(event, "target", { value: input });

      act(() => {
        document.dispatchEvent(event);
      });

      expect(shellState.commandPaletteOpen).toBe(false);
      document.body.removeChild(input);
    });
  });
});
