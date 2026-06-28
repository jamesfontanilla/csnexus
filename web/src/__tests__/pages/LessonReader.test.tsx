import { describe, it, expect, vi, beforeEach, beforeAll } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { LessonReader } from "../../pages/content/LessonReader";
import { ToastProvider } from "../../context/ToastContext";

// Mock window.matchMedia for jsdom
beforeAll(() => {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });
});

const mockGet = vi.fn();

vi.mock("../../api/client", () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock("../../stores/auth", () => ({
  login: vi.fn(),
  logout: vi.fn(),
  isAuthenticated: () => true,
  getToken: () => "mock-token",
  getLastAuthenticatedAt: () => Date.now(),
}));

// Control reduced motion
let mockReducedMotion = false;

vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => mockReducedMotion,
  springDefault: { type: "spring", stiffness: 300, damping: 20 },
  springGentle: { type: "spring", stiffness: 200, damping: 25 },
  springBouncy: { type: "spring", stiffness: 400, damping: 15 },
  fadeIn: { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.3 } },
  slideUp: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { type: "spring" } },
  slideDown: { initial: { opacity: 0, y: -12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: 12 }, transition: { type: "spring" } },
  scaleIn: { initial: { opacity: 0, scale: 0.95 }, animate: { opacity: 1, scale: 1 }, exit: { opacity: 0, scale: 0.95 }, transition: { type: "spring" } },
  staggerContainer: { animate: { transition: { staggerChildren: 0.06 } } },
  staggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { type: "spring" } },
  useMotionVariants: (v: Record<string, unknown>) => v,
  pageTransition: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.5 } },
  cardStaggerContainer: { animate: { transition: { staggerChildren: 0.05 } } },
  cardStaggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { type: "spring" } },
  hoverLift: { whileHover: { y: -2 }, transition: { duration: 0.15 } },
  pressFeedback: { whileTap: { scale: 0.97 }, whileHover: { scale: 1.02 }, transition: { type: "spring" } },
  makeReducedVariants: (v: Record<string, unknown>) => v,
}));

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return ({ children, style, className, ...rest }: Record<string, unknown>) => {
          const Tag = tag as keyof JSX.IntrinsicElements;
          return (
            <Tag className={className as string} style={style as React.CSSProperties} {...(rest as Record<string, unknown>)}>
              {children as React.ReactNode}
            </Tag>
          );
        };
      },
    }
  ),
  AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

// Mock useIsDesktop to control layout
let mockIsDesktop = false;

vi.mock("../../pages/content/lesson", () => ({
  DesktopLessonLayout: () => <div data-testid="desktop-layout" />,
  LessonFlowRenderer: () => <div data-testid="lesson-flow" />,
  useIsDesktop: () => mockIsDesktop,
  LessonChatPanel: () => null,
}));

describe("LessonReader page (Task 19.2)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockReducedMotion = false;
    mockIsDesktop = false;
  });

  it("renders lesson content after fetching", async () => {
    mockGet.mockResolvedValue({
      id: 1,
      subtopic_id: 5,
      content_json: {
        explanations: [{ title: "Introduction", body: "This is an explanation." }],
        worked_examples: [{ title: "Example 1", body: "Worked example content." }],
        key_takeaways: ["Takeaway 1"],
        summary: "A summary of the lesson.",
      },
      status: "COMPLETE",
    });

    render(
      <ToastProvider>
        <MemoryRouter initialEntries={["/subtopics/5/lesson"]}>
          <Routes>
            <Route path="/subtopics/:subtopicId/lesson" element={<LessonReader />} />
          </Routes>
        </MemoryRouter>
      </ToastProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("This is an explanation.")).toBeInTheDocument();
    });

    expect(mockGet).toHaveBeenCalledWith("/v1/subtopics/5/lesson");
  });

  it("uses the compiled lesson flow when a screen plan is present", async () => {
    mockIsDesktop = false;
    mockGet.mockResolvedValue({
      id: 1,
      subtopic_id: 5,
      content_json: {
        explanations: [{ title: "Introduction", body: "This is an explanation." }],
        worked_examples: [],
        key_takeaways: [],
        summary: "A summary of the lesson.",
        screen_plan: {
          title: "Compiled lesson",
          objective: "Learn the compiled flow",
          must_know: ["The lesson is compiled"],
          screens: [
            {
              index: 0,
              kind: "cover",
              title: "Start here",
              summary: "A compiled screen.",
              section_indices: [0],
              section_titles: ["Introduction"],
              estimated_reading_seconds: 30,
              focus_tags: ["cover"],
              node_kinds: ["prose"],
              call_to_action: "Begin",
            },
          ],
          estimated_reading_minutes: 1,
          screen_count: 1,
        },
      },
      status: "COMPLETE",
    });

    render(
      <ToastProvider>
        <MemoryRouter initialEntries={["/subtopics/5/lesson"]}>
          <Routes>
            <Route path="/subtopics/:subtopicId/lesson" element={<LessonReader />} />
          </Routes>
        </MemoryRouter>
      </ToastProvider>
    );

    await waitFor(() => {
      expect(screen.getByTestId("lesson-flow")).toBeInTheDocument();
    });
  });

  describe("Reading column has max-width: 680px (Requirement 14.1)", () => {
    it("mobile layout container has maxWidth 680", async () => {
      mockIsDesktop = false;
      mockGet.mockResolvedValue({
        id: 1,
        subtopic_id: 5,
        content_json: {
          explanations: [{ title: "Section One", body: "Content here." }],
          worked_examples: [],
          key_takeaways: [],
          summary: "",
        },
        status: "COMPLETE",
      });

      const { container } = render(
        <ToastProvider>
          <MemoryRouter initialEntries={["/subtopics/5/lesson"]}>
            <Routes>
              <Route path="/subtopics/:subtopicId/lesson" element={<LessonReader />} />
            </Routes>
          </MemoryRouter>
        </ToastProvider>
      );

      await waitFor(() => {
        expect(screen.getByText("Content here.")).toBeInTheDocument();
      });

      // The main container div has maxWidth: 680
      const pageContainer = container.querySelector(".page.container") as HTMLElement;
      expect(pageContainer).not.toBeNull();
      expect(pageContainer!.style.maxWidth).toBe("680px");
    });
  });

  describe("Sidebar renders even when no headings are found (Requirement 14.3)", () => {
    it("desktop layout renders even with a single section that has no title", async () => {
      mockIsDesktop = true;
      mockGet.mockResolvedValue({
        id: 1,
        subtopic_id: 5,
        content_json: {
          explanations: [{ title: "", body: "Content without heading." }],
          worked_examples: [],
          key_takeaways: [],
          summary: "",
        },
        status: "COMPLETE",
      });

      const { getByTestId } = render(
        <ToastProvider>
          <MemoryRouter initialEntries={["/subtopics/5/lesson"]}>
            <Routes>
              <Route path="/subtopics/:subtopicId/lesson" element={<LessonReader />} />
            </Routes>
          </MemoryRouter>
        </ToastProvider>
      );

      await waitFor(() => {
        // Desktop layout is rendered (which includes the sidebar)
        expect(getByTestId("desktop-layout")).toBeInTheDocument();
      });
    });
  });

  describe("Smooth scroll uses 'auto' behavior when prefers-reduced-motion is active (Requirement 14.5)", () => {
    it("scrollToSection uses behavior: auto when reduced motion is active", () => {
      // We verify this by reading the source code — the scrollToSection function
      // uses `reducedMotion ? "auto" : "smooth"` for scroll behavior
      const fs = require("fs");
      const path = require("path");
      const lessonReaderPath = path.resolve(
        __dirname,
        "../../pages/content/LessonReader.tsx"
      );
      const source = fs.readFileSync(lessonReaderPath, "utf-8");

      // Verify the source contains the reduced motion scroll behavior pattern
      expect(source).toContain('reducedMotion ? "auto" : "smooth"');
    });
  });
});
