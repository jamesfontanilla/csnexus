import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ShellProvider } from "../../context/ShellContext";
import { Sidebar } from "../../components/shell/Sidebar";

function renderSidebar(initialPath = "/") {
  return render(
    <MemoryRouter initialEntries={[initialPath]}>
      <ShellProvider>
        <Sidebar />
      </ShellProvider>
    </MemoryRouter>
  );
}

describe("Sidebar component", () => {
  describe("accessibility (Requirements 13.1)", () => {
    it("renders a nav element with role=navigation and aria-label", () => {
      renderSidebar();
      const nav = screen.getByRole("navigation", { name: "Main navigation" });
      expect(nav).toBeInTheDocument();
    });
  });

  describe("navigation groups (Requirement 2.2)", () => {
    it("renders primary nav items: Dashboard, Modules, Flashcards, Tutor", () => {
      renderSidebar();
      expect(screen.getByText("Dashboard")).toBeInTheDocument();
      expect(screen.getByText("Modules")).toBeInTheDocument();
      expect(screen.getByText("Flashcards")).toBeInTheDocument();
      expect(screen.getByText("Tutor")).toBeInTheDocument();
    });

    it("renders secondary nav items: Analytics, Leaderboard, Goals, Study Plan, Readiness, Focus, Tournaments", () => {
      renderSidebar();
      expect(screen.getByText("Analytics")).toBeInTheDocument();
      expect(screen.getByText("Leaderboard")).toBeInTheDocument();
      expect(screen.getByText("Goals")).toBeInTheDocument();
      expect(screen.getByText("Study Plan")).toBeInTheDocument();
      expect(screen.getByText("Readiness")).toBeInTheDocument();
      expect(screen.getByText("Focus")).toBeInTheDocument();
      expect(screen.getByText("Tournaments")).toBeInTheDocument();
    });

    it("renders nav items as links with correct paths", () => {
      renderSidebar();
      expect(screen.getByText("Dashboard").closest("a")).toHaveAttribute("href", "/");
      expect(screen.getByText("Modules").closest("a")).toHaveAttribute("href", "/modules");
      expect(screen.getByText("Flashcards").closest("a")).toHaveAttribute("href", "/flashcards");
      expect(screen.getByText("Tutor").closest("a")).toHaveAttribute("href", "/tutor");
      expect(screen.getByText("Analytics").closest("a")).toHaveAttribute("href", "/analytics");
      expect(screen.getByText("Leaderboard").closest("a")).toHaveAttribute("href", "/leaderboard");
      expect(screen.getByText("Goals").closest("a")).toHaveAttribute("href", "/goals");
      expect(screen.getByText("Study Plan").closest("a")).toHaveAttribute("href", "/study-plan");
      expect(screen.getByText("Readiness").closest("a")).toHaveAttribute("href", "/readiness");
      expect(screen.getByText("Focus").closest("a")).toHaveAttribute("href", "/focus");
      expect(screen.getByText("Tournaments").closest("a")).toHaveAttribute("href", "/tournaments");
    });
  });

  describe("profile card (Requirement 2.4)", () => {
    it("renders a profile card with name and level/XP", () => {
      renderSidebar();
      expect(screen.getByText("Student")).toBeInTheDocument();
      expect(screen.getByText("Level 1 · 0 XP")).toBeInTheDocument();
    });
  });

  describe("glass-morphism styling (Requirements 12.1)", () => {
    it("applies sidebar CSS class for glass-morphism background", () => {
      renderSidebar();
      const nav = screen.getByRole("navigation", { name: "Main navigation" });
      expect(nav.className).toContain("sidebar");
    });
  });

  describe("active item highlighting (Requirement 2.3)", () => {
    it("highlights Dashboard link when on / route", () => {
      renderSidebar("/");
      const dashboardLink = screen.getByText("Dashboard").closest("a");
      expect(dashboardLink?.className).toContain("sidebar__nav-link--active");
    });

    it("highlights Modules link when on /modules route", () => {
      renderSidebar("/modules");
      const modulesLink = screen.getByText("Modules").closest("a");
      expect(modulesLink?.className).toContain("sidebar__nav-link--active");
    });
  });

  describe("collapse toggle button (Requirements 2.5, 2.6, 2.7)", () => {
    it("renders a toggle button with aria-label='Toggle sidebar'", () => {
      renderSidebar();
      const button = screen.getByRole("button", { name: "Toggle sidebar" });
      expect(button).toBeInTheDocument();
    });

    it("has aria-expanded=true when sidebar is expanded (default state)", () => {
      renderSidebar();
      const button = screen.getByRole("button", { name: "Toggle sidebar" });
      expect(button).toHaveAttribute("aria-expanded", "true");
    });

    it("collapses sidebar on click and sets aria-expanded=false", () => {
      renderSidebar();
      const button = screen.getByRole("button", { name: "Toggle sidebar" });

      fireEvent.click(button);

      expect(button).toHaveAttribute("aria-expanded", "false");
      const nav = screen.getByRole("navigation", { name: "Main navigation" });
      expect(nav.className).toContain("sidebar--collapsed");
    });

    it("expands sidebar on second click and restores aria-expanded=true", () => {
      renderSidebar();
      const button = screen.getByRole("button", { name: "Toggle sidebar" });

      fireEvent.click(button); // collapse
      fireEvent.click(button); // expand

      expect(button).toHaveAttribute("aria-expanded", "true");
      const nav = screen.getByRole("navigation", { name: "Main navigation" });
      expect(nav.className).not.toContain("sidebar--collapsed");
    });

    it("shows 'Collapse' label text when expanded", () => {
      renderSidebar();
      expect(screen.getByText("Collapse")).toBeInTheDocument();
    });

    it("hides label text when collapsed", () => {
      renderSidebar();
      const button = screen.getByRole("button", { name: "Toggle sidebar" });

      fireEvent.click(button);

      expect(screen.queryByText("Collapse")).not.toBeInTheDocument();
    });
  });
});
