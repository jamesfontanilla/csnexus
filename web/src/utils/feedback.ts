/**
 * Sound & haptic feedback utilities.
 * All feedback respects user preferences and fails silently.
 */

import { isSoundEnabled, isHapticEnabled } from "../stores/preferences";

// --- Haptic Feedback ---

function vibrate(pattern: number | number[]): void {
  if (!isHapticEnabled()) return;
  try {
    navigator?.vibrate?.(pattern);
  } catch {
    // silent — not all browsers support this
  }
}

export function hapticTap(): void {
  vibrate(8);
}

export function hapticSuccess(): void {
  vibrate([10, 50, 10]);
}

export function hapticError(): void {
  vibrate([30, 20, 30]);
}

// --- Sound Feedback ---

let audioContext: AudioContext | null = null;

function getAudioContext(): AudioContext | null {
  if (!isSoundEnabled()) return null;
  try {
    if (!audioContext) {
      audioContext = new AudioContext();
    }
    if (audioContext.state === "suspended") {
      audioContext.resume();
    }
    return audioContext;
  } catch {
    return null;
  }
}

function playTone(frequency: number, duration: number, volume: number = 0.15, type: OscillatorType = "sine"): void {
  const ctx = getAudioContext();
  if (!ctx) return;

  const oscillator = ctx.createOscillator();
  const gainNode = ctx.createGain();

  oscillator.type = type;
  oscillator.frequency.setValueAtTime(frequency, ctx.currentTime);

  gainNode.gain.setValueAtTime(volume, ctx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

  oscillator.connect(gainNode);
  gainNode.connect(ctx.destination);

  oscillator.start(ctx.currentTime);
  oscillator.stop(ctx.currentTime + duration);
}

/** Soft pop — correct answer, successful action */
export function soundCorrect(): void {
  playTone(880, 0.12, 0.1);
  setTimeout(() => playTone(1100, 0.15, 0.08), 80);
}

/** Low thud — incorrect answer */
export function soundIncorrect(): void {
  playTone(220, 0.2, 0.12, "triangle");
}

/** Quick click — button press, selection */
export function soundTap(): void {
  playTone(600, 0.05, 0.06);
}

/** Rising chime — level up, achievement, milestone */
export function soundChime(): void {
  playTone(523, 0.15, 0.1);
  setTimeout(() => playTone(659, 0.15, 0.1), 100);
  setTimeout(() => playTone(784, 0.2, 0.12), 200);
}

/** Countdown warning tick */
export function soundTick(): void {
  playTone(440, 0.03, 0.04, "square");
}
