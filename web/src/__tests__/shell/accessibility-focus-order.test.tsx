/**
 * Accessibility: Focus order and ARIA landmarks
 *
 * Verifies that the shell's DOM structure provides correct:
 * 1. Focus order: Sidebar → BreadcrumbBar → ContentArea → DetailPanel
 * 2. No focus trapping in panels (only modal overlays trap focus)
 * 3. ARIA attributes: sidebar role="navigation", detail panel role="complementary",
 *    breadcrumb <nav> + <ol> + aria-current="page"
 *
 * Requirements: 13.1, 13.2, 13.3, 13.5, 13.7
 */
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider, useShell } from "../../context/ShellContext";
import { ShellContainer } from "../../components/shell/ShellContainer";

// Mock framer-motion to avoid animation complexities in tests
vi.mock("framer-motion", () => ({
  motion: {
    div: ({
      children,
      ...props
    }: React.PropsWithChildren<Record<string, unknown>>) => {
      const {
        initial: _initial,
        animate: _animate,
        exit: _exit,
        transition: _transition,
        variants: _variants,
        ...domProps
      } = props;
      return <div {...(domProps as React.HTMLAttributes<HTMLDivElement>)}>{children}</div>;
    },
    aside: ({
      children,
      ...props
    }: React.PropsWithChildren<Record<string, unknown>>) => {
      const {
        initial: _initial,
        animate: _animate,
        exit: _exit,
        transition: _transition,
        variants: _variants,
        ...domProps
      } = props;
      return <aside {...(domProps as React.HTMLAttributes<HTMLElement>)}>{children}</aside>;
    },
  },
  AnimatePresence: ({ children }: React.PropsWithChildren) => <>{children}</>,
}));

// Mock useAutoFocusMode and useResponsivePanels since they rely on browser APIs
vi.mock("../../hooks/useAutoFocusMode", () => ({
  useAutoFocusMode: () => {},
}));

vi.mock("../../hooks/useResponsivePanels", () => ({
  useResponsivePanels: () => {},
}));

function renderShell(initialRoute = "/modules/numerical-ability/topics") {
  return render(
    <MemoryRouter initialEntries={[initialRoute]}>
      <ShellProvider>
        <ShellContainer>
          <div data-testid="page-content">Page content here</div>
        </ShellContainer>
      </ShellProvider>
    </MemoryRouter>
  );
}

describe("Accessibility: Focus order and ARIA landmarks", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("ARIA landmarks", () => {
    it('sidebar has role="navigation" and aria-label="Main navigation"', () => {
      renderShell();
      const nav = screen.getByRole("navigation", { name: "Main navigation" });
      expect(nav).toBeInTheDocument();
    });

    it('sidebar collapse toggle has aria-expanded and aria-label="Toggle sidebar"', () => {
      renderShell();
      const toggle = screen.getByRole("button", { name: "Toggle sidebar" });
      expect(toggle).toBeInTheDocument();
      expect(toggle).toHaveAttribute("aria-expanded");
    });

    it("sidebar collapse toggle aria-expanded reflects expanded state (true when not collapsed)", () => {
      renderShell();
      const toggle = screen.getByRole("button", { name: "Toggle sidebar" });
      // Default state: sidebar is expanded, so aria-expanded should be "true"
      expect(toggle).toHaveAttribute("aria-expanded", "true");
    });

    it('breadcrumb uses <nav> with aria-label="Breadcrumb"', () => {
      renderShell();
      const breadcrumbNav = screen.getByRole("navigation", {
        name: "Breadcrumb",
      });
      expect(breadcrumbNav).toBeInTheDocument();
    });

    it("breadcrumb uses <ol> list structure", () => {
      renderShell();
      const breadcrumbNav = screen.getByRole("navigation", {
        name: "Breadcrumb",
      });
      const list = within(breadcrumbNav).getByRole("list");
      expect(list).toBeInTheDocument();
      expect(list.tagName).toBe("OL");
    });

    it('breadcrumb last segment has aria-current="page"', () => {
      renderShell();
      const currentSegment = screen.getByText("Topics");
      expect(currentSegment).toHaveAttribute("aria-current", "page");
    });

    it('resize handles have role="separator" and aria-orientation="vertical"', () => {
      renderShell();
      const separators = screen.getAllByRole("separator");
      expect(separators.length).toBeGreaterThanOrEqual(1);
      for (const separator of separators) {
        expect(separator).toHaveAttribute("aria-orientation", "vertical");
      }
    });
  });

  describe("Focus order follows visual layout", () => {
    it("DOM order is: Sidebar → ResizeHandle → BreadcrumbBar → ContentArea (no focus trapping)", () => {
      const { container } = renderShell();

      // Get the shell container (the grid parent)
      const shellContainer = container.querySelector(".shell-container");
      expect(shellContainer).not.toBeNull();

      // Check DOM child order within the grid
      const children = Array.from(shellContainer!.children);

      // First child should be the sidebar (nav element)
      const sidebarEl = children.find(
        (el) =>
          el.getAttribute("role") === "navigation" &&
          el.getAttribute("aria-label") === "Main navigation"
      );
      expect(sidebarEl).toBeDefined();

      // There should be a resize handle (separator) after the sidebar
      const firstSeparatorIdx = children.findIndex(
        (el) => el.getAttribute("role") === "separator"
      );
      const sidebarIdx = children.indexOf(sidebarEl!);
      expect(firstSeparatorIdx).toBeGreaterThan(sidebarIdx);

      // The .shell-main containing breadcrumb + content should come after
      const mainArea = children.find((el) =>
        el.classList.contains("shell-main")
      );
      expect(mainArea).toBeDefined();
      const mainIdx = children.indexOf(mainArea!);
      expect(mainIdx).toBeGreaterThan(firstSeparatorIdx);

      // Within shell-main: breadcrumb comes before content area
      const mainChildren = Array.from(mainArea!.children);
      const breadcrumbNavInMain = mainChildren.find(
        (el) =>
          el.getAttribute("aria-label") === "Breadcrumb" &&
          el.tagName.toLowerCase() === "nav"
      );
      const contentArea = mainChildren.find((el) =>
        el.classList.contains("content-area")
      );
      expect(breadcrumbNavInMain).toBeDefined();
      expect(contentArea).toBeDefined();

      const breadcrumbIdx = mainChildren.indexOf(breadcrumbNavInMain!);
      const contentIdx = mainChildren.indexOf(contentArea!);
      expect(breadcrumbIdx).toBeLessThan(contentIdx);
    });

    it("panels do not use focus trapping (no tabindex=-1 on non-modal panel containers)", () => {
      const { container } = renderShell();

      // Sidebar should NOT have tabIndex=-1 (it's navigable)
      const sidebar = container.querySelector('[role="navigation"][aria-label="Main navigation"]');
      expect(sidebar).not.toHaveAttribute("tabindex", "-1");

      // Content area should NOT have tabIndex=-1
      const contentArea = container.querySelector(".content-area");
      expect(contentArea).not.toHaveAttribute("tabindex", "-1");

      // Breadcrumb nav should NOT have tabIndex=-1
      const breadcrumb = container.querySelector('[aria-label="Breadcrumb"]');
      expect(breadcrumb).not.toHaveAttribute("tabindex", "-1");
    });

    it("resize handles are keyboard-accessible with tabIndex=0", () => {
      renderShell();
      const separators = screen.getAllByRole("separator");
      for (const separator of separators) {
        expect(separator).toHaveAttribute("tabindex", "0");
      }
    });
  });

  describe("Detail panel ARIA attributes (when open)", () => {
    function DetailPanelOpener() {
      const { actions } = useShell();
      React.useEffect(() => {
        actions.toggleDetailPanel();
      }, [actions]);
      return null;
    }

    function renderShellWithDetailPanel() {
      const { container } = render(
        <MemoryRouter initialEntries={["/modules"]}>
          <ShellProvider>
            <DetailPanelOpener />
            <ShellContainer>
              <div data-testid="page-content">Page content</div>
            </ShellContainer>
          </ShellProvider>
        </MemoryRouter>
      );
      return container;
    }

    it('detail panel has role="complementary" and aria-label when open', () => {
      renderShellWithDetailPanel();
      const panel = screen.getByRole("complementary");
      expect(panel).toBeInTheDocument();
      expect(panel).toHaveAttribute("aria-label");
    });

    it("detail panel close button is labeled for accessibility", () => {
      renderShellWithDetailPanel();
      const closeBtn = screen.getByRole("button", {
        name: "Close detail panel",
      });
      expect(closeBtn).toBeInTheDocument();
    });

    it("detail panel comes after main content in DOM order", () => {
      const container = renderShellWithDetailPanel();
      const shellContainer = container.querySelector(".shell-container");
      const children = Array.from(shellContainer!.children);

      const mainIdx = children.findIndex((el) =>
        el.classList.contains("shell-main")
      );
      const detailIdx = children.findIndex(
        (el) => el.getAttribute("role") === "complementary"
      );

      expect(detailIdx).toBeGreaterThan(mainIdx);
    });
  });
});
