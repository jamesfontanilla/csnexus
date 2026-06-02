import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, fireEvent } from "@testing-library/react";
import { GlassModal } from "../../components/GlassModal";

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
            "aria-modal": ariaModal,
            "aria-labelledby": ariaLabelledby,
            tabIndex,
            initial,
            animate,
            exit: _exit,
            transition: _transition,
            onClick,
            ...rest
          }: Record<string, unknown>) => {
            const Tag = tag as keyof JSX.IntrinsicElements;
            return (
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              <Tag
                className={className as string}
                style={style as React.CSSProperties}
                role={role as string}
                aria-modal={ariaModal as unknown as boolean | undefined}
                aria-labelledby={ariaLabelledby as string}
                tabIndex={tabIndex as number}
                onClick={onClick as React.MouseEventHandler}
                data-initial={initial ? JSON.stringify(initial) : undefined}
                data-animate={animate ? JSON.stringify(animate) : undefined}
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

describe("GlassModal", () => {
  const defaultProps = {
    isOpen: true,
    onClose: vi.fn(),
    title: "Test Modal Title",
  };

  beforeEach(() => {
    mockMatchMedia(false);
    defaultProps.onClose = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe("ARIA attributes (Requirements 6.4, 6.6)", () => {
    it('has role="dialog" on the modal panel', () => {
      const { getByRole } = render(
        <GlassModal {...defaultProps}>
          <p>Modal content</p>
        </GlassModal>
      );

      const dialog = getByRole("dialog");
      expect(dialog).toBeInTheDocument();
    });

    it('has aria-modal="true" on the modal panel', () => {
      const { getByRole } = render(
        <GlassModal {...defaultProps}>
          <p>Modal content</p>
        </GlassModal>
      );

      const dialog = getByRole("dialog");
      expect(dialog).toHaveAttribute("aria-modal", "true");
    });

    it("has aria-labelledby referencing the title element's id", () => {
      const { getByRole, getByText } = render(
        <GlassModal {...defaultProps}>
          <p>Modal content</p>
        </GlassModal>
      );

      const dialog = getByRole("dialog");
      const titleElement = getByText("Test Modal Title");

      const ariaLabelledby = dialog.getAttribute("aria-labelledby");
      expect(ariaLabelledby).toBeTruthy();
      expect(titleElement.getAttribute("id")).toBe(ariaLabelledby);
    });

    it("uses custom titleId when provided", () => {
      const { getByRole, getByText } = render(
        <GlassModal {...defaultProps} titleId="custom-title-id">
          <p>Modal content</p>
        </GlassModal>
      );

      const dialog = getByRole("dialog");
      const titleElement = getByText("Test Modal Title");

      expect(dialog).toHaveAttribute("aria-labelledby", "custom-title-id");
      expect(titleElement).toHaveAttribute("id", "custom-title-id");
    });
  });

  describe("Escape key closes modal (Requirement 6.4)", () => {
    it("calls onClose when Escape key is pressed", () => {
      render(
        <GlassModal {...defaultProps}>
          <p>Modal content</p>
        </GlassModal>
      );

      fireEvent.keyDown(document, { key: "Escape" });

      expect(defaultProps.onClose).toHaveBeenCalledTimes(1);
    });

    it("does not call onClose for other keys", () => {
      render(
        <GlassModal {...defaultProps}>
          <p>Modal content</p>
        </GlassModal>
      );

      fireEvent.keyDown(document, { key: "Enter" });
      fireEvent.keyDown(document, { key: "Tab" });
      fireEvent.keyDown(document, { key: "a" });

      expect(defaultProps.onClose).not.toHaveBeenCalled();
    });

    it("does not call onClose when modal is closed", () => {
      render(
        <GlassModal {...defaultProps} isOpen={false}>
          <p>Modal content</p>
        </GlassModal>
      );

      fireEvent.keyDown(document, { key: "Escape" });

      expect(defaultProps.onClose).not.toHaveBeenCalled();
    });
  });
});
