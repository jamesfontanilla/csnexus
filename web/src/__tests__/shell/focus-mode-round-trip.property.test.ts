// Feature: desktop-app-shell, Property 8: Focus mode round-trip state restoration
import { describe, it, expect } from "vitest";
import * as fc from "fast-check";
import { shellReducer } from "../../context/ShellContext";

/**
 * **Validates: Requirements 8.3**
 *
 * Property 8: Focus mode round-trip state restoration
 *
 * For any valid shell layout state (sidebar width, collapsed/expanded, detail
 * panel open/closed), entering focus mode and then exiting it SHALL restore
 * the exact previous layout state —
 * `exitFocusMode(enterFocusMode(state)) === state`.
 */

/**
 * Arbitrary that generates valid shell states meeting preconditions:
 * - focusModeActive: false (must start NOT in focus mode)
 * - preFocusModeState: null (must start without snapshot)
 */
const validShellState = fc.record({
  sidebarCollapsed: fc.boolean(),
  sidebarWidth: fc.integer({ min: 56, max: 360 }),
  detailPanelOpen: fc.boolean(),
  detailPanelWidth: fc.integer({ min: 240, max: 480 }),
  focusModeActive: fc.constant(false as const),
  commandPaletteOpen: fc.boolean(),
  shortcutsOverlayOpen: fc.boolean(),
  preFocusModeState: fc.constant(null as null),
});

function roundTripFocusMode(state: ReturnType<typeof validShellState extends fc.Arbitrary<infer T> ? () => T : never>) {
  const afterEnter = shellReducer(state, { type: "ENTER_FOCUS_MODE" });
  const afterExit = shellReducer(afterEnter, { type: "EXIT_FOCUS_MODE" });
  return afterExit;
}

describe("Property 8: Focus mode round-trip state restoration", () => {
  it("sidebarCollapsed is restored after enter/exit focus mode", () => {
    fc.assert(
      fc.property(validShellState, (state) => {
        const afterExit = roundTripFocusMode(state);
        expect(afterExit.sidebarCollapsed).toBe(state.sidebarCollapsed);
      }),
      { numRuns: 100 }
    );
  });

  it("sidebarWidth is restored after enter/exit focus mode", () => {
    fc.assert(
      fc.property(validShellState, (state) => {
        const afterExit = roundTripFocusMode(state);
        expect(afterExit.sidebarWidth).toBe(state.sidebarWidth);
      }),
      { numRuns: 100 }
    );
  });

  it("detailPanelOpen is restored after enter/exit focus mode", () => {
    fc.assert(
      fc.property(validShellState, (state) => {
        const afterExit = roundTripFocusMode(state);
        expect(afterExit.detailPanelOpen).toBe(state.detailPanelOpen);
      }),
      { numRuns: 100 }
    );
  });

  it("focusModeActive is false after exit", () => {
    fc.assert(
      fc.property(validShellState, (state) => {
        const afterExit = roundTripFocusMode(state);
        expect(afterExit.focusModeActive).toBe(false);
      }),
      { numRuns: 100 }
    );
  });

  it("preFocusModeState is null after exit (snapshot cleared)", () => {
    fc.assert(
      fc.property(validShellState, (state) => {
        const afterExit = roundTripFocusMode(state);
        expect(afterExit.preFocusModeState).toBeNull();
      }),
      { numRuns: 100 }
    );
  });
});
