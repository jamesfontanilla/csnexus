import { describe, it, expect } from "vitest";
import { render, screen, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell, type ShellActions } from "../../context/ShellContext";
import { ShellContainer } from "../../components/shell/ShellContainer";

let testActions: ShellActions;

function ActionsGrabber() {
  const { actions } = useShell();
  testActions = actions;
  return null;
}

function renderShellContainer(children?: React.ReactNode) {
  return render(
    <MemoryRouter>
      <ShellProvider>
        <ShellContainer>
          <ActionsGrabber />
          {children ?? <div data-testid="child">content</div>}
        </ShellContainer>
      </ShellProvider>
    </MemoryRouter>
  );
}

describe("ShellContainer", () => {
  it("renders children inside the grid container", () => {
    renderShellContainer();
    expect(screen.getByTestId("child")).toBeInTheDocument();
  });

  it("applies default shell-container class without modifiers", () => {
    const { container } = renderShellContainer();
    const el = container.firstElementChild!;
    expect(el.classList.contains("shell-container")).toBe(true);
    expect(el.classList.contains("shell-container--split")).toBe(false);
    expect(el.classList.contains("shell-container--focus")).toBe(false);
  });

  it("sets --sidebar-width CSS custom property from state (default 240px)", () => {
    const { container } = renderShellContainer();
    const el = container.firstElementChild as HTMLElement;
    expect(el.style.getPropertyValue("--sidebar-width")).toBe("240px");
  });

  it("sets --detail-panel-width CSS custom property from state (default 320px)", () => {
    const { container } = renderShellContainer();
    const el = container.firstElementChild as HTMLElement;
    expect(el.style.getPropertyValue("--detail-panel-width")).toBe("320px");
  });

  it("updates --sidebar-width when sidebar width changes", () => {
    const { container } = renderShellContainer();
    const el = container.firstElementChild as HTMLElement;

    act(() => testActions.setSidebarWidth(300));

    expect(el.style.getPropertyValue("--sidebar-width")).toBe("300px");
  });
});

describe("ShellContainer grid mode variants", () => {
  it("applies --focus class when focus mode is active", () => {
    const { container } = renderShellContainer();

    act(() => testActions.enterFocusMode());

    const el = container.firstElementChild!;
    expect(el.classList.contains("shell-container--focus")).toBe(true);
  });

  it("applies --split class when detail panel is open", () => {
    const { container } = renderShellContainer();

    act(() => testActions.toggleDetailPanel());

    const el = container.firstElementChild!;
    expect(el.classList.contains("shell-container--split")).toBe(true);
  });

  it("focus mode takes priority over split mode", () => {
    const { container } = renderShellContainer();

    act(() => testActions.toggleDetailPanel());
    act(() => testActions.enterFocusMode());

    const el = container.firstElementChild!;
    expect(el.classList.contains("shell-container--focus")).toBe(true);
    expect(el.classList.contains("shell-container--split")).toBe(false);
  });

  it("returns to default class after exiting focus mode", () => {
    const { container } = renderShellContainer();

    act(() => testActions.enterFocusMode());
    act(() => testActions.exitFocusMode());

    const el = container.firstElementChild!;
    expect(el.classList.contains("shell-container")).toBe(true);
    expect(el.classList.contains("shell-container--focus")).toBe(false);
  });
});
