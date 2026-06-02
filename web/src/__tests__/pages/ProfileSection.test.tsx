import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ProfileSection } from "../../pages/settings/ProfileSection";
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

const mockGet = vi.fn();
const mockPatch = vi.fn();

vi.mock("../../api/client", () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    post: vi.fn(),
    patch: (...args: unknown[]) => mockPatch(...args),
    delete: vi.fn(),
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
  logout: vi.fn(),
  isAuthenticated: () => true,
  getToken: () => "mock-token",
}));

function renderProfileSection() {
  return render(
    <MemoryRouter>
      <ToastProvider>
        <ProfileSection />
      </ToastProvider>
    </MemoryRouter>
  );
}

const mockUser = {
  id: 1,
  display_name: "Test User",
  username: "testuser",
  tz_name: "Asia/Manila",
};

describe("ProfileSection", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGet.mockImplementation((url: string) => {
      if (url === "/v1/auth/me") {
        return Promise.resolve({ ...mockUser });
      }
      return Promise.resolve({});
    });
  });

  it("shows loading state initially", () => {
    mockGet.mockReturnValue(new Promise(() => {})); // never resolves
    renderProfileSection();

    expect(screen.getByText("Loading profile…")).toBeInTheDocument();
  });

  it("renders display name, username, and timezone inputs after loading", async () => {
    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByLabelText("Display name")).toBeInTheDocument();
    });

    const displayNameInput = screen.getByLabelText("Display name") as HTMLInputElement;
    const usernameInput = screen.getByLabelText("Username") as HTMLInputElement;
    const timezoneSelect = screen.getByLabelText("Timezone") as HTMLSelectElement;

    expect(displayNameInput.value).toBe("Test User");
    expect(usernameInput.value).toBe("testuser");
    expect(timezoneSelect.value).toBe("Asia/Manila");
  });

  it("shows error when profile fails to load", async () => {
    mockGet.mockRejectedValue(new Error("Network error"));
    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByText("Failed to load profile data.")).toBeInTheDocument();
    });
  });

  it("shows validation error for invalid username format", async () => {
    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByLabelText("Username")).toBeInTheDocument();
    });

    const usernameInput = screen.getByLabelText("Username");
    fireEvent.change(usernameInput, { target: { value: "1bad" } });

    expect(
      screen.getByText("Must be 3–30 chars, start with a letter, letters/digits/underscores only")
    ).toBeInTheDocument();
  });

  it("save button is disabled when no changes are made", async () => {
    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByLabelText("Save profile changes")).toBeInTheDocument();
    });

    const saveBtn = screen.getByLabelText("Save profile changes");
    expect(saveBtn).toBeDisabled();
  });

  it("save button becomes enabled when changes are made", async () => {
    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByLabelText("Display name")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText("Display name"), {
      target: { value: "New Name" },
    });

    const saveBtn = screen.getByLabelText("Save profile changes");
    expect(saveBtn).not.toBeDisabled();
  });

  it("calls PATCH with only modified fields on save", async () => {
    mockPatch.mockResolvedValue({
      ...mockUser,
      display_name: "New Name",
    });

    renderProfileSection();

    await waitFor(() => {
      expect(screen.getByLabelText("Display name")).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText("Display name"), {
      target: { value: "New Name" },
    });

    fireEvent.click(screen.getByLabelText("Save profile changes"));

    await waitFor(() => {
      expect(mockPatch).toHaveBeenCalledWith("/v1/users/me", {
        display_name: "New Name",
      });
    });
  });
});
