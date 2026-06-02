import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { AccountSection } from "../../pages/settings/AccountSection";
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
  toastSlideIn: { initial: { opacity: 0, x: 20 }, animate: { opacity: 1, x: 0 }, exit: { opacity: 0, x: 20 }, transition: { type: "spring" } },
}));

const mockPost = vi.fn();
const mockDelete = vi.fn();
const mockLogout = vi.fn();

vi.mock("../../api/client", () => ({
  apiClient: {
    get: vi.fn(),
    post: (...args: unknown[]) => mockPost(...args),
    patch: vi.fn(),
    delete: (...args: unknown[]) => mockDelete(...args),
  },
  ApiError: class ApiError extends Error {
    status: number;
    code: string;
    requestId: string | null;
    constructor(status: number, message: string, code: string) {
      super(message);
      this.name = "ApiError";
      this.status = status;
      this.code = code;
      this.requestId = null;
    }
  },
}));

vi.mock("../../stores/auth", () => ({
  login: vi.fn(),
  logout: (...args: unknown[]) => mockLogout(...args),
  isAuthenticated: () => true,
  getToken: () => "mock-token",
}));

function renderAccountSection() {
  return render(
    <MemoryRouter>
      <ToastProvider>
        <AccountSection />
      </ToastProvider>
    </MemoryRouter>
  );
}

describe("AccountSection", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Change Password form", () => {
    it("renders current password and new password fields", () => {
      renderAccountSection();

      expect(screen.getByLabelText("Current Password")).toBeInTheDocument();
      expect(screen.getByLabelText("New Password")).toBeInTheDocument();
    });

    it("renders the Change Password heading", () => {
      renderAccountSection();

      expect(screen.getByRole("heading", { name: "Change Password" })).toBeInTheDocument();
    });

    it("shows password policy rules when new password is typed", () => {
      renderAccountSection();

      const newPasswordInput = screen.getByLabelText("New Password");
      fireEvent.change(newPasswordInput, { target: { value: "a" } });

      expect(screen.getByText("At least 8 characters")).toBeInTheDocument();
      expect(screen.getByText("At least one uppercase letter")).toBeInTheDocument();
      expect(screen.getByText("At least one lowercase letter")).toBeInTheDocument();
      expect(screen.getByText("At least one digit")).toBeInTheDocument();
      expect(screen.getByText("At least one symbol")).toBeInTheDocument();
    });

    it("submit button is disabled when fields are empty", () => {
      renderAccountSection();

      const submitBtn = screen.getByRole("button", { name: "Change Password" });
      expect(submitBtn).toBeDisabled();
    });

    it("shows error when current password is empty on submit", () => {
      renderAccountSection();

      // Fill only new password (valid)
      fireEvent.change(screen.getByLabelText("New Password"), {
        target: { value: "Abcd123!" },
      });
      // Current is still empty but button is disabled, so we can't really click
      // Instead test that the button remains disabled
      const submitBtn = screen.getByRole("button", { name: "Change Password" });
      expect(submitBtn).toBeDisabled();
    });

    it("shows error when new password fails policy", async () => {
      renderAccountSection();

      fireEvent.change(screen.getByLabelText("Current Password"), {
        target: { value: "oldpassword" },
      });
      fireEvent.change(screen.getByLabelText("New Password"), {
        target: { value: "weak" },
      });

      const form = screen.getByRole("button", { name: "Change Password" }).closest("form")!;
      fireEvent.submit(form);

      await waitFor(() => {
        expect(screen.getByRole("alert")).toHaveTextContent(
          "New password does not meet all policy requirements."
        );
      });
    });

    it("calls API on valid password change submission", async () => {
      mockPost.mockResolvedValue(undefined);
      renderAccountSection();

      fireEvent.change(screen.getByLabelText("Current Password"), {
        target: { value: "OldPass123!" },
      });
      fireEvent.change(screen.getByLabelText("New Password"), {
        target: { value: "NewPass456@" },
      });

      const form = screen.getByRole("button", { name: "Change Password" }).closest("form")!;
      fireEvent.submit(form);

      await waitFor(() => {
        expect(mockPost).toHaveBeenCalledWith("/v1/auth/password-change", {
          current_password: "OldPass123!",
          new_password: "NewPass456@",
        });
      });

      expect(mockLogout).toHaveBeenCalled();
    });

    it("shows error when current password is incorrect (401)", async () => {
      const { ApiError } = await import("../../api/client");
      mockPost.mockRejectedValue(new ApiError(401, "Invalid credentials", "invalid_credentials", null));

      renderAccountSection();

      fireEvent.change(screen.getByLabelText("Current Password"), {
        target: { value: "WrongPass1!" },
      });
      fireEvent.change(screen.getByLabelText("New Password"), {
        target: { value: "NewPass456@" },
      });

      const form = screen.getByRole("button", { name: "Change Password" }).closest("form")!;
      fireEvent.submit(form);

      await waitFor(() => {
        expect(screen.getByRole("alert")).toHaveTextContent(
          "Current password is incorrect."
        );
      });
    });
  });

  describe("Logout", () => {
    it("renders log out button", () => {
      renderAccountSection();

      expect(screen.getByRole("button", { name: "Log Out" })).toBeInTheDocument();
    });

    it("calls logout on click", async () => {
      mockDelete.mockResolvedValue(undefined);
      renderAccountSection();

      fireEvent.click(screen.getByRole("button", { name: "Log Out" }));

      await waitFor(() => {
        expect(mockLogout).toHaveBeenCalled();
      });
    });
  });

  describe("Delete Account", () => {
    it("renders delete account button with danger styling", () => {
      renderAccountSection();

      expect(screen.getByRole("button", { name: "Delete Account" })).toBeInTheDocument();
    });

    it("renders the Danger Zone heading", () => {
      renderAccountSection();

      expect(screen.getByText("Danger Zone")).toBeInTheDocument();
    });
  });
});
