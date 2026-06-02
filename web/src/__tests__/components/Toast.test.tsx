import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, fireEvent, waitFor } from "@testing-library/react";
import { ToastProvider, useToast } from "../../context/ToastContext";

// Mock framer-motion to render elements with forwarded props
vi.mock("framer-motion", () => {
  return {
    motion: new Proxy(
      {},
      {
        get: (_target, tag: string) => {
          return ({
            children,
            className,
            style,
            role,
            initial,
            animate,
            exit,
            transition,
            layout,
            onMouseEnter,
            onMouseLeave,
            ...rest
          }: Record<string, unknown>) => {
            const Tag = tag as keyof JSX.IntrinsicElements;
            return (
              <Tag
                className={className as string}
                style={style as React.CSSProperties}
                role={role as string}
                onMouseEnter={onMouseEnter as React.MouseEventHandler}
                onMouseLeave={onMouseLeave as React.MouseEventHandler}
                {...(rest as Record<string, unknown>)}
              >
                {children as React.ReactNode}
              </Tag>
            );
          };
        },
      }
    ),
    AnimatePresence: ({ children }: { children: React.ReactNode }) => (
      <>{children}</>
    ),
  };
});

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

// Helper component that triggers a toast on button click
function ToastTrigger({
  variant,
  message,
  duration,
}: {
  variant: "success" | "error" | "warning" | "info";
  message: string;
  duration?: number;
}) {
  const toast = useToast();
  return (
    <button onClick={() => toast[variant](message, duration)}>
      Trigger {variant}
    </button>
  );
}

describe("Toast System", () => {
  beforeEach(() => {
    mockMatchMedia(false);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("ARIA roles (Requirements 10.7, 17.7)", () => {
    it('renders role="alert" for error toasts', () => {
      const { getByRole, getByText } = render(
        <ToastProvider>
          <ToastTrigger variant="error" message="Something went wrong" />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger error"));

      const alert = getByRole("alert");
      expect(alert).toBeInTheDocument();
      expect(alert).toHaveTextContent("Something went wrong");
    });

    it('renders role="status" for info toasts', () => {
      const { getByRole, getByText } = render(
        <ToastProvider>
          <ToastTrigger variant="info" message="Info message" />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger info"));

      const status = getByRole("status");
      expect(status).toBeInTheDocument();
      expect(status).toHaveTextContent("Info message");
    });

    it('renders role="status" for success toasts', () => {
      const { getByRole, getByText } = render(
        <ToastProvider>
          <ToastTrigger variant="success" message="Success message" />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger success"));

      const status = getByRole("status");
      expect(status).toBeInTheDocument();
      expect(status).toHaveTextContent("Success message");
    });

    it('renders role="status" for warning toasts', () => {
      const { getByRole, getByText } = render(
        <ToastProvider>
          <ToastTrigger variant="warning" message="Warning message" />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger warning"));

      const status = getByRole("status");
      expect(status).toBeInTheDocument();
      expect(status).toHaveTextContent("Warning message");
    });
  });

  describe("Hover pauses auto-dismiss timer (Requirement 10.4)", () => {
    it("toast has onMouseEnter handler that pauses dismissal", () => {
      const { getByRole, getByText, queryByRole } = render(
        <ToastProvider>
          <ToastTrigger variant="info" message="Hover me" />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger info"));
      const toast = getByRole("status");
      expect(toast).toBeInTheDocument();

      // Fire mouseEnter — this should dispatch PAUSE action
      // The toast should still exist in the DOM (re-query after state update)
      fireEvent.mouseEnter(toast);
      expect(queryByRole("status")).toBeInTheDocument();

      // Fire mouseLeave — this should dispatch RESUME action
      const toastAfterPause = getByRole("status");
      fireEvent.mouseLeave(toastAfterPause);
      expect(queryByRole("status")).toBeInTheDocument();
    });

    it("auto-dismisses when not hovered", async () => {
      const { getByText, queryByRole } = render(
        <ToastProvider>
          <ToastTrigger variant="info" message="Will dismiss" duration={500} />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger info"));

      // Wait for the toast to auto-dismiss
      await waitFor(
        () => {
          expect(queryByRole("status")).not.toBeInTheDocument();
        },
        { timeout: 3000 }
      );
    });

    it("hovered toast persists longer than unhovered toast", async () => {
      // Render two toasts: one hovered, one not
      function DualToastTrigger() {
        const toast = useToast();
        return (
          <button
            onClick={() => {
              toast.info("Hovered toast", 600);
              toast.info("Unhovered toast", 600);
            }}
          >
            Trigger both
          </button>
        );
      }

      const { getByText, getAllByRole, queryAllByRole } = render(
        <ToastProvider>
          <DualToastTrigger />
        </ToastProvider>
      );

      fireEvent.click(getByText("Trigger both"));
      const toasts = getAllByRole("status");
      expect(toasts).toHaveLength(2);

      // Hover over the first toast only
      fireEvent.mouseEnter(toasts[0]);

      // Wait for the unhovered toast to dismiss
      await waitFor(
        () => {
          const remaining = queryAllByRole("status");
          expect(remaining.length).toBeLessThan(2);
        },
        { timeout: 3000 }
      );

      // The hovered toast should still be present
      const remaining = queryAllByRole("status");
      expect(remaining.length).toBe(1);
      expect(remaining[0]).toHaveTextContent("Hovered toast");
    });
  });

  describe("useToast outside provider (Requirement 17.7)", () => {
    it("throws a descriptive error when used outside ToastProvider", () => {
      // Suppress React error boundary console output
      const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});

      function BadComponent() {
        useToast();
        return <div>Should not render</div>;
      }

      expect(() => render(<BadComponent />)).toThrow(
        /useToast must be used within a ToastProvider/
      );

      consoleSpy.mockRestore();
    });
  });
});
