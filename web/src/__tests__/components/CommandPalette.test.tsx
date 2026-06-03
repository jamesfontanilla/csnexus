import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, fireEvent, act } from "@testing-library/react";
import React, { useEffect } from "react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell } from "../../context/ShellContext";
import { CommandPalette } from "../../components/shell/CommandPalette";

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return React.forwardRef(
          (
            {
              children,
              className,
              style,
              role,
              onClick,
              tabIndex,
              "aria-modal": ariaModal,
              "aria-label": ariaLabel,
              ..._rest
            }: Record<string, unknown>,
            ref: React.Ref<unknown>
          ) => {
            const Tag = tag as keyof JSX.IntrinsicElements;
            return React.createElement(
              Tag,
              {
                ref,
                className,
                style,
                role,
                onClick,
                tabIndex,
                "aria-modal": ariaModal,
                "aria-label": ariaLabel,
              },
              children as React.ReactNode
            );
          }
        );
      },
    }
  ),
  AnimatePresence: ({ children }: { children: React.ReactNode }) => (
    <>{children}</>
  ),
}));

// Mock the design system
vi.mock("../../design-system", () => ({
  useReducedMotion: () => false,
}));

// Mock useFocusTrap to return a simple ref
vi.mock("../../hooks/useFocusTrap", () => ({
  useFocusTrap: () => React.createRef(),
}));

function mockMatchMedia() {
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
}

// Component that opens the command palette on mount
function PaletteOpener() {
  const { actions } = useShell();
  useEffect(() => {
    actions.openCommandPalette();
  }, [actions]);
  return null;
}

// Helper to render CommandPalette inside required providers with palette open
function renderCommandPalette() {
  return render(
    <MemoryRouter>
      <ShellProvider>
        <PaletteOpener />
        <CommandPalette />
      </ShellProvider>
    </MemoryRouter>
  );
}

describe("CommandPalette Keyboard Navigation", () => {
  beforeEach(() => {
    mockMatchMedia();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("renders results when palette is open", async () => {
    const { getByRole, getAllByRole } = renderCommandPalette();

    // Wait for debounce
    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    expect(getByRole("listbox")).toBeInTheDocument();
    const options = getAllByRole("option");
    expect(options.length).toBeGreaterThan(0);
  });

  it("highlights first item by default", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    const options = getAllByRole("option");
    expect(options[0]).toHaveAttribute("aria-selected", "true");
  });

  it("ArrowDown moves highlight to next item", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    // Press ArrowDown
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowDown" });
    });

    const options = getAllByRole("option");
    expect(options[0]).toHaveAttribute("aria-selected", "false");
    expect(options[1]).toHaveAttribute("aria-selected", "true");
  });

  it("ArrowUp moves highlight to previous item", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    // Move down first
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowDown" });
    });
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowDown" });
    });

    // Confirm index 2
    let options = getAllByRole("option");
    expect(options[2]).toHaveAttribute("aria-selected", "true");

    // Press ArrowUp
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowUp" });
    });

    options = getAllByRole("option");
    expect(options[1]).toHaveAttribute("aria-selected", "true");
  });

  it("ArrowUp does not go below index 0 (clamped)", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    // Press ArrowUp multiple times while at 0
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowUp" });
    });
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowUp" });
    });
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowUp" });
    });

    const options = getAllByRole("option");
    expect(options[0]).toHaveAttribute("aria-selected", "true");
  });

  it("ArrowDown does not exceed last index (clamped to N-1)", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    const options = getAllByRole("option");
    const count = options.length;

    // Press ArrowDown more times than items exist
    for (let i = 0; i < count + 5; i++) {
      await act(async () => {
        fireEvent.keyDown(document, { key: "ArrowDown" });
      });
    }

    const updatedOptions = getAllByRole("option");
    expect(updatedOptions[count - 1]).toHaveAttribute("aria-selected", "true");
    expect(updatedOptions[0]).toHaveAttribute("aria-selected", "false");
  });

  it("highlights item on mouse hover", async () => {
    const { getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    const options = getAllByRole("option");

    // Hover over the third item
    await act(async () => {
      fireEvent.mouseEnter(options[2]);
    });

    const updatedOptions = getAllByRole("option");
    expect(updatedOptions[2]).toHaveAttribute("aria-selected", "true");
    expect(updatedOptions[0]).toHaveAttribute("aria-selected", "false");
  });

  it("resets highlighted index when query changes", async () => {
    const { getByLabelText, getAllByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    // Move highlight down
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowDown" });
    });
    await act(async () => {
      fireEvent.keyDown(document, { key: "ArrowDown" });
    });

    let options = getAllByRole("option");
    expect(options[2]).toHaveAttribute("aria-selected", "true");

    // Type a query
    const input = getByLabelText("Search commands");
    await act(async () => {
      fireEvent.change(input, { target: { value: "dash" } });
    });

    // Wait for debounce
    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    // First item in new results should be highlighted
    options = getAllByRole("option");
    if (options.length > 0) {
      expect(options[0]).toHaveAttribute("aria-selected", "true");
    }
  });

  it("Escape closes the palette", async () => {
    const { queryByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    expect(queryByRole("dialog")).toBeInTheDocument();

    await act(async () => {
      fireEvent.keyDown(document, { key: "Escape" });
    });

    expect(queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("clicking a result executes its action", async () => {
    const { getAllByRole, queryByRole } = renderCommandPalette();

    await act(async () => {
      vi.advanceTimersByTime(200);
    });

    const options = getAllByRole("option");

    // Click the first result
    await act(async () => {
      fireEvent.click(options[0]);
    });

    // Palette should close after clicking
    expect(queryByRole("dialog")).not.toBeInTheDocument();
  });
});
