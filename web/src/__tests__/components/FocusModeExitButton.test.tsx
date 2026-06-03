import { describe, it, expect } from "vitest";
import { render, screen, act, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell, type ShellActions } from "../../context/ShellContext";
import { FocusModeExitButton } from "../../components/shell/FocusModeExitButton";

let testActions: ShellActions;

function ActionsGrabber() {
  const { actions } = useShell();
  testActions = actions;
  return null;
}

function renderFocusModeExitButton() {
  return render(
    <MemoryRouter>
      <ShellProvider>
        <ActionsGrabber />
        <FocusModeExitButton />
      </ShellProvider>
    </MemoryRouter>
  );
}

describe("FocusModeExitButton", () => {
  it("does not render when focus mode is inactive", () => {
    renderFocusModeExitButton();
    expect(screen.queryByRole("button", { name: /exit focus mode/i })).not.toBeInTheDocument();
  });

  it("renders when focus mode is active", () => {
    renderFocusModeExitButton();
    act(() => testActions.enterFocusMode());
    expect(screen.getByRole("button", { name: /exit focus mode/i })).toBeInTheDocument();
  });

  it("has correct aria-label for accessibility", () => {
    renderFocusModeExitButton();
    act(() => testActions.enterFocusMode());
    const btn = screen.getByRole("button", { name: /exit focus mode/i });
    expect(btn).toHaveAttribute("aria-label", "Exit focus mode");
  });

  it("exits focus mode when clicked", () => {
    renderFocusModeExitButton();
    act(() => testActions.enterFocusMode());

    const btn = screen.getByRole("button", { name: /exit focus mode/i });
    fireEvent.click(btn);

    expect(screen.queryByRole("button", { name: /exit focus mode/i })).not.toBeInTheDocument();
  });

  it("has the focus-mode-exit-btn class for styling", () => {
    renderFocusModeExitButton();
    act(() => testActions.enterFocusMode());
    const btn = screen.getByRole("button", { name: /exit focus mode/i });
    expect(btn.classList.contains("focus-mode-exit-btn")).toBe(true);
  });
});
