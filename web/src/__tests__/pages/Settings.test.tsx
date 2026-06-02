import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { Settings } from "../../pages/Settings";
import { ToastProvider } from "../../context/ToastContext";

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

vi.mock("../../design-system/motion", () => ({
  useReducedMotion: () => false,
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
}));

// Mock child sections so we only test the page shell
vi.mock("../../pages/settings/ProfileSection", () => ({
  ProfileSection: () => <div data-testid="profile-section">ProfileSection</div>,
}));

vi.mock("../../pages/settings/StudySection", () => ({
  StudySection: () => <div data-testid="study-section">StudySection</div>,
}));

vi.mock("../../pages/settings/AccessibilitySection", () => ({
  AccessibilitySection: () => <div data-testid="accessibility-section">AccessibilitySection</div>,
}));

vi.mock("../../pages/settings/AccountSection", () => ({
  AccountSection: () => <div data-testid="account-section">AccountSection</div>,
}));

function renderSettings() {
  return render(
    <MemoryRouter>
      <ToastProvider>
        <Settings />
      </ToastProvider>
    </MemoryRouter>
  );
}

describe("Settings page", () => {
  it("renders all four section headings", () => {
    renderSettings();

    expect(screen.getByText("Profile")).toBeInTheDocument();
    expect(screen.getByText("Study Preferences")).toBeInTheDocument();
    expect(screen.getByText("Accessibility & Display")).toBeInTheDocument();
    expect(screen.getByText("Account Management")).toBeInTheDocument();
  });

  it("renders all four section components", () => {
    renderSettings();

    expect(screen.getByTestId("profile-section")).toBeInTheDocument();
    expect(screen.getByTestId("study-section")).toBeInTheDocument();
    expect(screen.getByTestId("accessibility-section")).toBeInTheDocument();
    expect(screen.getByTestId("account-section")).toBeInTheDocument();
  });

  it("back button links to /profile", () => {
    renderSettings();

    const backLink = screen.getByLabelText("Back to profile");
    expect(backLink).toBeInTheDocument();
    expect(backLink).toHaveAttribute("href", "/profile");
  });

  it("displays the Settings title", () => {
    renderSettings();

    expect(screen.getByText("Settings")).toBeInTheDocument();
  });
});
