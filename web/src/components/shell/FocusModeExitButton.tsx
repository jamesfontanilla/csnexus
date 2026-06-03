import { useShell } from "../../context/ShellContext";

/**
 * Floating "exit focus mode" button rendered in the top-right corner
 * when focus mode is active. Has reduced opacity (0.5) that increases
 * to 1 on hover for minimal distraction.
 *
 * Requirements: 8.2
 */
export function FocusModeExitButton() {
  const { state, actions } = useShell();

  if (!state.focusModeActive) return null;

  return (
    <button
      className="focus-mode-exit-btn"
      onClick={actions.exitFocusMode}
      aria-label="Exit focus mode"
      type="button"
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M2 2h5v2H4v3H2V2zm7 0h5v5h-2V4H9V2zM2 9h2v3h3v2H2V9zm12 0v5H9v-2h3V9h2z"
          fill="currentColor"
        />
      </svg>
      <span className="focus-mode-exit-btn__label">Exit Focus</span>
    </button>
  );
}
