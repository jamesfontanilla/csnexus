import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { StudySection, daysUntil } from "../../pages/settings/StudySection";

// Mock the preferences store
const mockGetStudyPreferences = vi.fn();
const mockSetStudyPreference = vi.fn();

vi.mock("../../stores/preferences", () => ({
  getStudyPreferences: () => mockGetStudyPreferences(),
  setStudyPreference: (...args: unknown[]) => mockSetStudyPreference(...args),
}));

describe("StudySection", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetStudyPreferences.mockReturnValue({
      dailyGoalMinutes: 30,
      defaultQuizMode: "practice",
      examDate: null,
    });
  });

  it("renders with default values from the store", () => {
    render(<StudySection />);

    const slider = screen.getByLabelText("Daily study goal in minutes") as HTMLInputElement;
    expect(slider.value).toBe("30");
    expect(screen.getByText("30 minutes")).toBeInTheDocument();

    // Practice mode should be selected by default
    const practiceBtn = screen.getByRole("radio", { name: "Practice" });
    expect(practiceBtn).toHaveAttribute("aria-checked", "true");
  });

  it("loads stored preferences on mount", () => {
    mockGetStudyPreferences.mockReturnValue({
      dailyGoalMinutes: 60,
      defaultQuizMode: "exam",
      examDate: "2030-12-25",
    });

    render(<StudySection />);

    const slider = screen.getByLabelText("Daily study goal in minutes") as HTMLInputElement;
    expect(slider.value).toBe("60");
    expect(screen.getByText("60 minutes")).toBeInTheDocument();

    const examBtn = screen.getByRole("radio", { name: "Exam" });
    expect(examBtn).toHaveAttribute("aria-checked", "true");

    const dateInput = screen.getByLabelText("Target exam date") as HTMLInputElement;
    expect(dateInput.value).toBe("2030-12-25");
  });

  it("persists daily goal changes immediately", () => {
    render(<StudySection />);

    const slider = screen.getByLabelText("Daily study goal in minutes") as HTMLInputElement;
    fireEvent.change(slider, { target: { value: "45" } });

    expect(mockSetStudyPreference).toHaveBeenCalledWith("dailyGoalMinutes", 45);
    expect(screen.getByText("45 minutes")).toBeInTheDocument();
  });

  it("persists quiz mode changes immediately", () => {
    render(<StudySection />);

    const sprintBtn = screen.getByRole("radio", { name: "Sprint" });
    fireEvent.click(sprintBtn);

    expect(mockSetStudyPreference).toHaveBeenCalledWith("defaultQuizMode", "power");
    expect(sprintBtn).toHaveAttribute("aria-checked", "true");
  });

  it("persists exam date changes immediately", () => {
    render(<StudySection />);

    const dateInput = screen.getByLabelText("Target exam date") as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "2030-06-15" } });

    expect(mockSetStudyPreference).toHaveBeenCalledWith("examDate", "2030-06-15");
  });

  it("shows countdown when exam date is set", () => {
    mockGetStudyPreferences.mockReturnValue({
      dailyGoalMinutes: 30,
      defaultQuizMode: "practice",
      examDate: "2030-12-25",
    });

    render(<StudySection />);

    // Should show "X days remaining"
    expect(screen.getByText(/days remaining/)).toBeInTheDocument();
  });

  it("clears exam date when input is emptied", () => {
    mockGetStudyPreferences.mockReturnValue({
      dailyGoalMinutes: 30,
      defaultQuizMode: "practice",
      examDate: "2030-06-15",
    });

    render(<StudySection />);

    const dateInput = screen.getByLabelText("Target exam date") as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "" } });

    expect(mockSetStudyPreference).toHaveBeenCalledWith("examDate", null);
  });

  it("slider has correct min, max, step attributes", () => {
    render(<StudySection />);

    const slider = screen.getByLabelText("Daily study goal in minutes") as HTMLInputElement;
    expect(slider.min).toBe("5");
    expect(slider.max).toBe("180");
    expect(slider.step).toBe("5");
  });
});

describe("daysUntil", () => {
  it("returns 0 when target is today", () => {
    const today = new Date("2025-03-15T10:30:00");
    expect(daysUntil("2025-03-15", today)).toBe(0);
  });

  it("returns 1 for tomorrow", () => {
    const today = new Date("2025-03-15T23:59:00");
    expect(daysUntil("2025-03-16", today)).toBe(1);
  });

  it("returns correct count for a future date", () => {
    const today = new Date("2025-01-01T00:00:00");
    expect(daysUntil("2025-01-11", today)).toBe(10);
  });

  it("returns 0 for past dates (clamped to non-negative)", () => {
    const today = new Date("2025-06-01T12:00:00");
    expect(daysUntil("2025-05-01", today)).toBe(0);
  });
});
