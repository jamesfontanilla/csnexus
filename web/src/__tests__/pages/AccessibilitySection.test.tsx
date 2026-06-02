import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { AccessibilitySection } from "../../pages/settings/AccessibilitySection";

// Mock the preferences store
const mockGetAccessibilityPreferences = vi.fn();
const mockSetAccessibilityPreference = vi.fn();
const mockApplyAccessibilityToDOM = vi.fn();
const mockIsSoundEnabled = vi.fn();
const mockSetSoundEnabled = vi.fn();
const mockIsHapticEnabled = vi.fn();
const mockSetHapticEnabled = vi.fn();

vi.mock("../../stores/preferences", () => ({
  getAccessibilityPreferences: () => mockGetAccessibilityPreferences(),
  setAccessibilityPreference: (...args: unknown[]) => mockSetAccessibilityPreference(...args),
  applyAccessibilityToDOM: () => mockApplyAccessibilityToDOM(),
  isSoundEnabled: () => mockIsSoundEnabled(),
  setSoundEnabled: (...args: unknown[]) => mockSetSoundEnabled(...args),
  isHapticEnabled: () => mockIsHapticEnabled(),
  setHapticEnabled: (...args: unknown[]) => mockSetHapticEnabled(...args),
}));

describe("AccessibilitySection", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGetAccessibilityPreferences.mockReturnValue({
      reducedMotion: "system",
      fontSize: "default",
      soundEnabled: true,
      hapticEnabled: true,
    });
    mockIsSoundEnabled.mockReturnValue(true);
    mockIsHapticEnabled.mockReturnValue(true);
  });

  it("renders reduced motion options with System selected by default", () => {
    render(<AccessibilitySection />);

    const systemBtn = screen.getByRole("radio", { name: "System" });
    const onBtn = screen.getByRole("radio", { name: "On" });
    const offBtn = screen.getByRole("radio", { name: "Off" });

    expect(systemBtn).toHaveAttribute("aria-checked", "true");
    expect(onBtn).toHaveAttribute("aria-checked", "false");
    expect(offBtn).toHaveAttribute("aria-checked", "false");
  });

  it("renders font size options with Default selected by default", () => {
    render(<AccessibilitySection />);

    const compactBtn = screen.getByRole("radio", { name: "Compact" });
    const defaultBtn = screen.getByRole("radio", { name: "Default" });
    const largeBtn = screen.getByRole("radio", { name: "Large" });

    expect(defaultBtn).toHaveAttribute("aria-checked", "true");
    expect(compactBtn).toHaveAttribute("aria-checked", "false");
    expect(largeBtn).toHaveAttribute("aria-checked", "false");
  });

  it("renders sound and haptic toggle switches", () => {
    render(<AccessibilitySection />);

    const soundSwitch = screen.getByRole("switch", { name: "Sound Effects" });
    const hapticSwitch = screen.getByRole("switch", { name: "Haptic Feedback" });

    expect(soundSwitch).toHaveAttribute("aria-checked", "true");
    expect(hapticSwitch).toHaveAttribute("aria-checked", "true");
  });

  it("selecting a reduced motion option persists and applies to DOM", () => {
    render(<AccessibilitySection />);

    const onBtn = screen.getByRole("radio", { name: "On" });
    fireEvent.click(onBtn);

    expect(mockSetAccessibilityPreference).toHaveBeenCalledWith("reducedMotion", "on");
    expect(mockApplyAccessibilityToDOM).toHaveBeenCalled();
    expect(onBtn).toHaveAttribute("aria-checked", "true");
  });

  it("selecting a font size option persists and applies to DOM", () => {
    render(<AccessibilitySection />);

    const largeBtn = screen.getByRole("radio", { name: "Large" });
    fireEvent.click(largeBtn);

    expect(mockSetAccessibilityPreference).toHaveBeenCalledWith("fontSize", "large");
    expect(mockApplyAccessibilityToDOM).toHaveBeenCalled();
    expect(largeBtn).toHaveAttribute("aria-checked", "true");
  });

  it("toggling sound off calls setSoundEnabled(false) and applies DOM", () => {
    render(<AccessibilitySection />);

    const soundSwitch = screen.getByRole("switch", { name: "Sound Effects" });
    fireEvent.click(soundSwitch);

    expect(mockSetSoundEnabled).toHaveBeenCalledWith(false);
    expect(mockApplyAccessibilityToDOM).toHaveBeenCalled();
    expect(soundSwitch).toHaveAttribute("aria-checked", "false");
  });

  it("toggling haptic off calls setHapticEnabled(false) and applies DOM", () => {
    render(<AccessibilitySection />);

    const hapticSwitch = screen.getByRole("switch", { name: "Haptic Feedback" });
    fireEvent.click(hapticSwitch);

    expect(mockSetHapticEnabled).toHaveBeenCalledWith(false);
    expect(mockApplyAccessibilityToDOM).toHaveBeenCalled();
    expect(hapticSwitch).toHaveAttribute("aria-checked", "false");
  });

  it("loads stored preferences on mount", () => {
    mockGetAccessibilityPreferences.mockReturnValue({
      reducedMotion: "on",
      fontSize: "large",
      soundEnabled: false,
      hapticEnabled: false,
    });

    render(<AccessibilitySection />);

    expect(screen.getByRole("radio", { name: "On" })).toHaveAttribute("aria-checked", "true");
    expect(screen.getByRole("radio", { name: "Large" })).toHaveAttribute("aria-checked", "true");
    expect(screen.getByRole("switch", { name: "Sound Effects" })).toHaveAttribute("aria-checked", "false");
    expect(screen.getByRole("switch", { name: "Haptic Feedback" })).toHaveAttribute("aria-checked", "false");
  });

  it("sound and haptic toggles are independent", () => {
    render(<AccessibilitySection />);

    const soundSwitch = screen.getByRole("switch", { name: "Sound Effects" });
    fireEvent.click(soundSwitch);

    // Sound toggled off
    expect(soundSwitch).toHaveAttribute("aria-checked", "false");
    // Haptic still on
    expect(screen.getByRole("switch", { name: "Haptic Feedback" })).toHaveAttribute("aria-checked", "true");
  });
});
