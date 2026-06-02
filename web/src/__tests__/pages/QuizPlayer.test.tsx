import { describe, it, expect, vi, beforeEach, beforeAll } from "vitest";
import { render, screen, waitFor, act } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";

// Control reduced motion from tests
let mockReducedMotion = false;

vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => mockReducedMotion,
  scaleIn: { initial: { opacity: 0, scale: 0.95 }, animate: { opacity: 1, scale: 1 }, transition: { duration: 0.25 } },
  staggerContainer: { animate: { transition: { staggerChildren: 0.05 } } },
  staggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 } },
  springDefault: { type: "spring", stiffness: 300, damping: 30 },
  slideUp: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { type: "spring" } },
  slideDown: { initial: { opacity: 0, y: -12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: 12 }, transition: { type: "spring" } },
  springGentle: { type: "spring", stiffness: 200, damping: 25 },
  springBouncy: { type: "spring", stiffness: 400, damping: 15 },
  fadeIn: { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 }, transition: { duration: 0.3 } },
  useMotionVariants: (v: Record<string, unknown>) => v,
  pageTransition: { initial: { opacity: 0, y: 12 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -8 }, transition: { duration: 0.5 } },
  cardStaggerContainer: { animate: { transition: { staggerChildren: 0.05 } } },
  cardStaggerItem: { initial: { opacity: 0, y: 8 }, animate: { opacity: 1, y: 0 }, transition: { type: "spring" } },
  hoverLift: { whileHover: { y: -2 }, transition: { duration: 0.15 } },
  pressFeedback: { whileTap: { scale: 0.97 }, whileHover: { scale: 1.02 }, transition: { type: "spring" } },
  makeReducedVariants: (v: Record<string, unknown>) => v,
}));

vi.mock("../../design-system", () => ({
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
}));

// Mock framer-motion
vi.mock("framer-motion", () => ({
  motion: new Proxy(
    {},
    {
      get: (_target, tag: string) => {
        return ({ children, style, className, whileTap, whileHover, ...rest }: Record<string, unknown>) => {
          const Tag = tag as keyof JSX.IntrinsicElements;
          return (
            <Tag
              className={className as string}
              style={style as React.CSSProperties}
              data-while-tap={whileTap ? JSON.stringify(whileTap) : undefined}
              data-while-hover={whileHover ? JSON.stringify(whileHover) : undefined}
              {...(rest as Record<string, unknown>)}
            >
              {children as React.ReactNode}
            </Tag>
          );
        };
      },
    }
  ),
  AnimatePresence: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));

vi.mock("../../utils/feedback", () => ({
  soundCorrect: vi.fn(),
  soundIncorrect: vi.fn(),
  soundTap: vi.fn(),
  hapticTap: vi.fn(),
}));

function mockMatchMedia(reducedMotion: boolean) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: query === "(prefers-reduced-motion: reduce)" ? reducedMotion : false,
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

const mockPost = vi.fn();
const mockPatch = vi.fn();

vi.mock("../../api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: (...args: unknown[]) => mockPost(...args),
    patch: (...args: unknown[]) => mockPatch(...args),
    delete: vi.fn(),
  },
  ApiError: class ApiError extends Error {
    status: number;
    code: string;
    constructor(msg: string, status: number, code: string) {
      super(msg);
      this.status = status;
      this.code = code;
    }
  },
}));

vi.mock("../../stores/auth", () => ({
  login: vi.fn(),
  logout: vi.fn(),
  isAuthenticated: () => true,
  getToken: () => "mock-token",
  getLastAuthenticatedAt: () => Date.now(),
}));

import { QuizPlayer } from "../../pages/quiz/QuizPlayer";

const mockAttemptInProgress = {
  attempt_id: 10,
  status: "IN_PROGRESS",
  started_at: new Date().toISOString(),
  time_limit_seconds: 1200,
  questions: [
    { id: 1, ordinal: 1, stem: "What is 2+2?", qtype: "MULTIPLE_CHOICE", difficulty: "EASY", options: ["3", "4", "5", "6"], selected_answer: null },
    { id: 2, ordinal: 2, stem: "Capital of PH?", qtype: "MULTIPLE_CHOICE", difficulty: "MEDIUM", options: ["Manila", "Cebu", "Davao", "Quezon"], selected_answer: null },
  ],
  total_questions: 2,
};

function renderQuizPlayer() {
  return render(
    <MemoryRouter initialEntries={["/quiz/subtopic/3"]}>
      <Routes>
        <Route path="/quiz/:scope/:scopeId" element={<QuizPlayer />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("QuizPlayer page (Task 18.5)", () => {
  beforeAll(() => {
    mockMatchMedia(false);
  });

  beforeEach(() => {
    mockReducedMotion = false;
    mockMatchMedia(false);
    vi.clearAllMocks();
  });

  describe("Time expired state is visually distinct from sub-30s warning (Requirement 13.6)", () => {
    it("timer expired state shows 'Time Expired' text with distinct background styling", async () => {
      // Create an attempt that started long ago so timer is at 0
      const expiredAttempt = {
        ...mockAttemptInProgress,
        started_at: new Date(Date.now() - 1200 * 1000 - 10000).toISOString(),
        time_limit_seconds: 1200,
      };
      mockPost.mockResolvedValue(expiredAttempt);

      renderQuizPlayer();

      // Click a mode to start the quiz
      const practiceBtn = await screen.findByLabelText("Start Practice Mode");
      await act(async () => {
        practiceBtn.click();
      });

      await waitFor(() => {
        expect(screen.getByText("Time Expired")).toBeInTheDocument();
      });

      // The "Time Expired" text should be present (distinct from just showing a countdown)
      const timerEl = screen.getByText("Time Expired");
      // The timer expired state has a distinct background (rgba(212, 100, 92, 0.15))
      // and a solid danger border, which is different from the sub-30s state
      const timerContainer = timerEl.closest("div");
      expect(timerContainer).not.toBeNull();
      // The expired state has a specific background and border that differs from sub-30s
      expect(timerContainer!.style.background).toContain("rgba(212, 100, 92, 0.15)");
      expect(timerContainer!.style.border).toContain("var(--color-danger)");
    });

    it("sub-30s warning state shows countdown numbers, not 'Time Expired'", async () => {
      // Create an attempt where timer has ~15 seconds left
      const warningAttempt = {
        ...mockAttemptInProgress,
        started_at: new Date(Date.now() - (1200 - 15) * 1000).toISOString(),
        time_limit_seconds: 1200,
      };
      mockPost.mockResolvedValue(warningAttempt);

      renderQuizPlayer();

      const practiceBtn = await screen.findByLabelText("Start Practice Mode");
      await act(async () => {
        practiceBtn.click();
      });

      await waitFor(() => {
        expect(screen.getByText("What is 2+2?")).toBeInTheDocument();
      });

      // Should NOT show "Time Expired" — should show a countdown
      expect(screen.queryByText("Time Expired")).not.toBeInTheDocument();
      // Timer should be visible with a formatted time
      const timerEl = screen.getByText(/\d{2}:\d{2}/);
      expect(timerEl).toBeInTheDocument();
      // Timer color should be danger (red) since < 30s
      expect(timerEl.style.color).toBe("var(--color-danger)");
    });
  });

  describe("Answer selection glow persists when prefers-reduced-motion is active (Requirement 13.7)", () => {
    it("selected answer has box-shadow glow regardless of reduced motion", async () => {
      mockReducedMotion = true;
      mockMatchMedia(true);

      mockPost.mockResolvedValue(mockAttemptInProgress);
      mockPatch.mockResolvedValue({});

      renderQuizPlayer();

      const practiceBtn = await screen.findByLabelText("Start Practice Mode");
      await act(async () => {
        practiceBtn.click();
      });

      await waitFor(() => {
        expect(screen.getByText("What is 2+2?")).toBeInTheDocument();
      });

      // Click an answer option
      const optionBtn = screen.getByLabelText("Select option: 4");
      await act(async () => {
        optionBtn.click();
      });

      await waitFor(() => {
        // After selection, the button should have the glow box-shadow
        // jsdom doesn't properly parse shorthand CSS, so check the style attribute string
        const styleAttr = optionBtn.getAttribute("style") || "";
        expect(styleAttr).toContain("rgba(212,165,116,0.2)");
      });

      // The border should also be the accent color
      const styleAttr2 = optionBtn.getAttribute("style") || "";
      expect(styleAttr2).toContain("var(--color-accent)");
    });

    it("scale animation is skipped when reduced motion is active but glow remains", async () => {
      mockReducedMotion = true;
      mockMatchMedia(true);

      mockPost.mockResolvedValue(mockAttemptInProgress);

      const { container } = renderQuizPlayer();

      const practiceBtn = await screen.findByLabelText("Start Practice Mode");
      await act(async () => {
        practiceBtn.click();
      });

      await waitFor(() => {
        expect(screen.getByText("What is 2+2?")).toBeInTheDocument();
      });

      // When reduced motion is active, whileTap should be undefined (no scale animation)
      const optionButtons = container.querySelectorAll('[aria-label^="Select option"]');
      optionButtons.forEach((btn) => {
        // data-while-tap should be undefined when reducedMotion is true
        expect(btn.getAttribute("data-while-tap")).toBeNull();
      });
    });
  });
});
