import type { ReactNode } from "react";
import { ShellProvider } from "../../context/ShellContext";
import { ShellContainer } from "./ShellContainer";
import { CommandPalette } from "./CommandPalette";
import { ShortcutsCheatSheet } from "./ShortcutsCheatSheet";
import { KeyboardShortcutManager } from "./KeyboardShortcutManager";
import { FocusModeExitButton } from "./FocusModeExitButton";

interface DesktopAppShellProps {
  children: ReactNode;
}

/**
 * Top-level wrapper for the desktop layout.
 * Provides shell context (sidebar state, focus mode, etc.) and renders
 * children inside the CSS Grid shell container.
 *
 * Usage in App.tsx:
 *   <DesktopAppShell>
 *     <Routes>...</Routes>
 *   </DesktopAppShell>
 */
export function DesktopAppShell({ children }: DesktopAppShellProps) {
  return (
    <ShellProvider>
      <ShellContainer>{children}</ShellContainer>
      <CommandPalette />
      <ShortcutsCheatSheet />
      <FocusModeExitButton />
      <KeyboardShortcutManager />
    </ShellProvider>
  );
}
