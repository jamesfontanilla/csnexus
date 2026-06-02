import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { Profile } from "../../pages/Profile";
import { ToastProvider } from "../../context/ToastContext";

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

describe("Profile page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders XP, level, and streak from /v1/xp/me", async () => {
    mockGet.mockImplementation((url: string) => {
      if (url === "/v1/xp/me") {
        return Promise.resolve({ cumulative_xp: 5000, level: 7, streak: 3 });
      }
      if (url === "/v1/achievements/me") {
        return Promise.resolve([{ achievement_id: "FIRST_LESSON", title: "First Lesson", granted_at: "2024-01-01T00:00:00Z" }]);
      }
      if (url === "/v1/auth/me") {
        return Promise.resolve({ display_name: "TestUser", username: "testuser", email: "test@example.com" });
      }
      return Promise.resolve({});
    });

    render(
      <MemoryRouter>
        <ToastProvider>
          <Profile />
        </ToastProvider>
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("7")).toBeInTheDocument(); // level
      expect(screen.getByText("5000")).toBeInTheDocument(); // XP
      expect(screen.getByText(/3/)).toBeInTheDocument(); // streak
      expect(screen.getByText("First Lesson")).toBeInTheDocument();
    });

    expect(mockGet).toHaveBeenCalledWith("/v1/xp/me");
    expect(mockGet).toHaveBeenCalledWith("/v1/achievements/me");
  });
});
