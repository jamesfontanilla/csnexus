import { useRef, useEffect } from "react";

const FOCUSABLE_SELECTORS = [
  'a[href]',
  'button:not([disabled])',
  'input:not([disabled])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

/**
 * Hook that traps keyboard focus within a container element.
 * Used by GlassModal to prevent focus from escaping the modal panel.
 *
 * - Saves the previously focused element on activation and restores it on cleanup.
 * - Suppresses Tab when zero focusable elements exist inside the container.
 * - Falls back to `document.body` if the trigger element is no longer in the DOM.
 */
export function useFocusTrap(isActive: boolean): React.RefObject<HTMLElement> {
  const containerRef = useRef<HTMLElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isActive) return;

    // Save the element that had focus before the trap activated
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus the container itself (it should have tabIndex={-1})
    containerRef.current?.focus();

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab' || !containerRef.current) return;

      const focusable = Array.from(
        containerRef.current.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTORS)
      ).filter(el => !el.closest('[aria-hidden="true"]'));

      // Suppress Tab entirely when no focusable elements exist
      if (focusable.length === 0) {
        e.preventDefault();
        return;
      }

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);

      // Return focus to the trigger element; fall back to body if gone
      if (previousFocusRef.current && document.body.contains(previousFocusRef.current)) {
        previousFocusRef.current.focus();
      } else {
        document.body.focus();
      }
    };
  }, [isActive]);

  return containerRef as React.RefObject<HTMLElement>;
}
