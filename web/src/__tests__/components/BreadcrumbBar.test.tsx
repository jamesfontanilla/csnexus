import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { BreadcrumbBar, deriveBreadcrumbSegments, formatSegmentLabel, getVisibleSegments } from "../../components/shell/BreadcrumbBar";

function renderBreadcrumb(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <BreadcrumbBar />
    </MemoryRouter>
  );
}

describe("BreadcrumbBar", () => {
  it("renders a nav element with aria-label Breadcrumb", () => {
    renderBreadcrumb("/modules");
    const nav = screen.getByRole("navigation", { name: "Breadcrumb" });
    expect(nav).toBeInTheDocument();
  });

  it("renders an ordered list inside the nav", () => {
    renderBreadcrumb("/modules");
    const list = screen.getByRole("list");
    expect(list).toBeInTheDocument();
  });

  it("renders Home as first segment for any path", () => {
    renderBreadcrumb("/modules/numerical-ability");
    expect(screen.getByText("Home")).toBeInTheDocument();
  });

  it("marks the last segment with aria-current=page", () => {
    renderBreadcrumb("/modules");
    const current = screen.getByText("Modules");
    expect(current).toHaveAttribute("aria-current", "page");
  });

  it("renders inactive segments as links", () => {
    renderBreadcrumb("/modules/numerical-ability");
    const homeLink = screen.getByRole("link", { name: "Home" });
    expect(homeLink).toHaveAttribute("href", "/");

    const modulesLink = screen.getByRole("link", { name: "Modules" });
    expect(modulesLink).toHaveAttribute("href", "/modules");
  });

  it("renders the last segment as text (not a link)", () => {
    renderBreadcrumb("/modules/numerical-ability");
    const current = screen.getByText("Numerical ability");
    expect(current).toHaveAttribute("aria-current", "page");
    expect(current.tagName).not.toBe("A");
  });

  it("renders chevron separators between segments", () => {
    const { container } = renderBreadcrumb("/modules/topics");
    const separators = container.querySelectorAll(".breadcrumb-bar__separator");
    // Home > Modules > Topics = 2 separators
    expect(separators).toHaveLength(2);
  });

  it("renders Home as current page for root path", () => {
    renderBreadcrumb("/");
    const current = screen.getByText("Home");
    expect(current).toHaveAttribute("aria-current", "page");
  });

  it("applies correct CSS classes for styling", () => {
    const { container } = renderBreadcrumb("/modules/topics");
    expect(container.querySelector(".breadcrumb-bar")).toBeInTheDocument();
    expect(container.querySelector(".breadcrumb-bar__list")).toBeInTheDocument();
    expect(container.querySelector(".breadcrumb-bar__segment--current")).toBeInTheDocument();
    expect(container.querySelector(".breadcrumb-bar__segment--link")).toBeInTheDocument();
  });
});

describe("formatSegmentLabel", () => {
  it("capitalizes first letter of a single word", () => {
    expect(formatSegmentLabel("modules")).toBe("Modules");
  });

  it("replaces hyphens with spaces and capitalizes", () => {
    expect(formatSegmentLabel("numerical-ability")).toBe("Numerical ability");
  });

  it("handles single character", () => {
    expect(formatSegmentLabel("a")).toBe("A");
  });

  it("handles empty string", () => {
    expect(formatSegmentLabel("")).toBe("");
  });
});

describe("deriveBreadcrumbSegments", () => {
  it("returns only Home for root path", () => {
    const segments = deriveBreadcrumbSegments("/");
    expect(segments).toEqual([{ label: "Home", path: "/" }]);
  });

  it("derives segments from path", () => {
    const segments = deriveBreadcrumbSegments("/modules/topics");
    expect(segments).toEqual([
      { label: "Home", path: "/" },
      { label: "Modules", path: "/modules" },
      { label: "Topics", path: "/modules/topics" },
    ]);
  });

  it("uses breadcrumbLabels overrides when provided", () => {
    const labels = { modules: "All Modules", topics: "Topic List" };
    const segments = deriveBreadcrumbSegments("/modules/topics", labels);
    expect(segments).toEqual([
      { label: "Home", path: "/" },
      { label: "All Modules", path: "/modules" },
      { label: "Topic List", path: "/modules/topics" },
    ]);
  });

  it("falls back to formatted label when no override exists", () => {
    const labels = { modules: "Modules" };
    const segments = deriveBreadcrumbSegments("/modules/numerical-ability", labels);
    expect(segments[2].label).toBe("Numerical ability");
  });
});


describe("getVisibleSegments", () => {
  const makeSegments = (count: number) =>
    Array.from({ length: count }, (_, i) => ({
      label: `Segment ${i}`,
      path: `/${Array.from({ length: i }, (_, j) => `seg${j}`).join("/")}`,
    }));

  it("returns all segments when count <= 4", () => {
    const segments = makeSegments(4);
    const result = getVisibleSegments(segments, false);
    expect(result.visible).toEqual(segments);
    expect(result.hidden).toEqual([]);
    expect(result.overflowing).toBe(false);
  });

  it("collapses middle segments when count > 4 and not expanded", () => {
    const segments = makeSegments(6);
    const result = getVisibleSegments(segments, false);
    // first + last 2 = 3 visible
    expect(result.visible).toHaveLength(3);
    expect(result.visible[0]).toEqual(segments[0]);
    expect(result.visible[1]).toEqual(segments[4]);
    expect(result.visible[2]).toEqual(segments[5]);
    // hidden = middle 3 segments (index 1, 2, 3)
    expect(result.hidden).toHaveLength(3);
    expect(result.hidden).toEqual(segments.slice(1, 4));
    expect(result.overflowing).toBe(true);
  });

  it("returns all segments when expanded regardless of count", () => {
    const segments = makeSegments(7);
    const result = getVisibleSegments(segments, true);
    expect(result.visible).toEqual(segments);
    expect(result.hidden).toEqual([]);
    expect(result.overflowing).toBe(true);
  });

  it("handles exactly 5 segments (threshold + 1)", () => {
    const segments = makeSegments(5);
    const result = getVisibleSegments(segments, false);
    // first + last 2 = 3 visible, 2 hidden
    expect(result.visible).toHaveLength(3);
    expect(result.hidden).toHaveLength(2);
    expect(result.visible[0]).toEqual(segments[0]);
    expect(result.visible[1]).toEqual(segments[3]);
    expect(result.visible[2]).toEqual(segments[4]);
  });
});

describe("BreadcrumbBar overflow collapse", () => {
  function renderBreadcrumb(path: string) {
    return render(
      <MemoryRouter initialEntries={[path]}>
        <BreadcrumbBar />
      </MemoryRouter>
    );
  }

  it("does not show ellipsis when path has 4 or fewer segments", () => {
    // /a/b/c = Home + a + b + c = 4 segments
    renderBreadcrumb("/a/b/c");
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("shows ellipsis toggle when path exceeds 4 segments", () => {
    // /a/b/c/d = Home + a + b + c + d = 5 segments
    renderBreadcrumb("/a/b/c/d");
    const ellipsisButton = screen.getByRole("button");
    expect(ellipsisButton).toBeInTheDocument();
    expect(ellipsisButton).toHaveTextContent("…");
  });

  it("shows first segment and last 2 segments when collapsed", () => {
    // Home > A > B > C > D > E = 6 segments total
    renderBreadcrumb("/a/b/c/d/e");
    // Home should be a link
    expect(screen.getByRole("link", { name: "Home" })).toBeInTheDocument();
    // Last segment (E) should have aria-current
    expect(screen.getByText("E")).toHaveAttribute("aria-current", "page");
    // Second-to-last (D) should be a link
    expect(screen.getByRole("link", { name: "D" })).toBeInTheDocument();
    // Middle segments (A, B, C) should NOT be visible
    expect(screen.queryByText("A")).not.toBeInTheDocument();
    expect(screen.queryByText("B")).not.toBeInTheDocument();
    expect(screen.queryByText("C")).not.toBeInTheDocument();
  });

  it("expands to show all segments when ellipsis is clicked", () => {
    renderBreadcrumb("/a/b/c/d/e");
    // Click the ellipsis button
    const ellipsisButton = screen.getByRole("button");
    fireEvent.click(ellipsisButton);
    // Now all segments should be visible
    expect(screen.getByText("Home")).toBeInTheDocument();
    expect(screen.getByText("A")).toBeInTheDocument();
    expect(screen.getByText("B")).toBeInTheDocument();
    expect(screen.getByText("C")).toBeInTheDocument();
    expect(screen.getByText("D")).toBeInTheDocument();
    expect(screen.getByText("E")).toBeInTheDocument();
    // Ellipsis button should no longer be visible
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("ellipsis button has accessible aria-label with hidden segment count", () => {
    renderBreadcrumb("/a/b/c/d/e");
    const ellipsisButton = screen.getByRole("button");
    // 6 segments: Home, A, B, C, D, E → hidden = A, B, C = 3 segments
    expect(ellipsisButton).toHaveAttribute(
      "aria-label",
      "Show 3 hidden breadcrumb segments"
    );
  });
});
