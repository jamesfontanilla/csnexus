import { useState, useRef, type KeyboardEvent, type ClipboardEvent } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient } from "../../api/client";
import { PageTransition } from "../../components/PageTransition";
import { GlassCard } from "../../components/GlassCard";
import { GlassInput } from "../../components/GlassInput";
import { GlassButton } from "../../components/GlassButton";
import { GradientText } from "../../components/GradientText";
import { scaleIn } from "../../design-system";

const OTP_LENGTH = 6;

export function OTPVerification() {
  const navigate = useNavigate();
  const location = useLocation();
  const { email = "", purpose = "VERIFY_EMAIL" } =
    (location.state as { email?: string; purpose?: string }) ?? {};

  const [digits, setDigits] = useState<string[]>(Array(OTP_LENGTH).fill(""));
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const inputRefs = useRef<Array<HTMLInputElement | null>>(Array(OTP_LENGTH).fill(null));

  const isPasswordReset = purpose === "PASSWORD_RESET";
  const code = digits.join("");
  const isComplete = code.length === OTP_LENGTH && digits.every((d) => d !== "");

  function focusAt(index: number) {
    inputRefs.current[index]?.focus();
  }

  function handleDigitChange(index: number, value: string) {
    // Accept only a single digit
    const digit = value.replace(/\D/g, "").slice(-1);
    const next = [...digits];
    next[index] = digit;
    setDigits(next);

    if (digit && index < OTP_LENGTH - 1) {
      focusAt(index + 1);
    }
  }

  function handleKeyDown(index: number, e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Backspace") {
      if (digits[index]) {
        // Clear current box
        const next = [...digits];
        next[index] = "";
        setDigits(next);
      } else if (index > 0) {
        // Move back and clear previous box
        const next = [...digits];
        next[index - 1] = "";
        setDigits(next);
        focusAt(index - 1);
      }
      e.preventDefault();
    } else if (e.key === "ArrowLeft" && index > 0) {
      focusAt(index - 1);
    } else if (e.key === "ArrowRight" && index < OTP_LENGTH - 1) {
      focusAt(index + 1);
    }
  }

  function handlePaste(e: ClipboardEvent<HTMLInputElement>) {
    e.preventDefault();
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, OTP_LENGTH);
    if (!pasted) return;

    const next = Array(OTP_LENGTH).fill("");
    for (let i = 0; i < pasted.length; i++) {
      next[i] = pasted[i];
    }
    setDigits(next);
    // Focus the box after the last pasted digit, or the last box
    focusAt(Math.min(pasted.length, OTP_LENGTH - 1));
  }

  async function handleSubmit() {
    if (!isComplete || loading) return;
    setError(null);
    setLoading(true);

    try {
      if (isPasswordReset) {
        await apiClient.post("/v1/auth/password-resets", {
          email,
          code,
          new_password: newPassword,
        });
        navigate("/login", {
          state: { successMessage: "Password reset successfully. Sign in with your new password." },
        });
      } else {
        await apiClient.post("/v1/auth/email-verifications", {
          email,
          code,
          purpose: "VERIFY_EMAIL",
        });
        navigate("/login", {
          state: { successMessage: "Email verified. You can now sign in." },
        });
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Verification failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <PageTransition>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "calc(100vh - 4rem)",
          padding: "var(--space-8) var(--space-4)",
        }}
      >
        <motion.div
          initial={scaleIn.initial}
          animate={scaleIn.animate}
          transition={scaleIn.transition}
          style={{ width: "100%", maxWidth: "420px" }}
        >
          <GlassCard blur="lg" style={{ padding: "var(--space-10)" }}>
            {/* Header */}
            <div style={{ textAlign: "center", marginBottom: "var(--space-6)" }}>
              <div style={{ fontSize: "2.5rem", marginBottom: "var(--space-2)" }}>
                {isPasswordReset ? "🔑" : "✉️"}
              </div>
              <h1
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "var(--font-size-3xl)",
                  fontWeight: 800,
                  textAlign: "center",
                  marginBottom: "var(--space-1)",
                  letterSpacing: "-0.03em",
                }}
              >
                <GradientText variant="accent">
                  {isPasswordReset ? "Reset Password" : "Verify Email"}
                </GradientText>
              </h1>
              <p
                style={{
                  color: "var(--color-text-secondary)",
                  fontSize: "var(--font-size-sm)",
                  margin: 0,
                }}
              >
                Enter the 6-digit code sent to{" "}
                <span style={{ color: "var(--color-text)", fontWeight: 500 }}>
                  {email || "your email"}
                </span>
              </p>
            </div>

            {/* OTP digit boxes */}
            <div
              role="group"
              aria-label="One-time password input"
              style={{
                display: "flex",
                gap: "var(--space-2)",
                justifyContent: "center",
                marginBottom: "var(--space-6)",
              }}
            >
              {digits.map((digit, i) => (
                <input
                  key={i}
                  ref={(el) => { inputRefs.current[i] = el; }}
                  type="text"
                  inputMode="numeric"
                  autoComplete={i === 0 ? "one-time-code" : "off"}
                  aria-label={`Digit ${i + 1} of ${OTP_LENGTH}`}
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleDigitChange(i, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(i, e)}
                  onPaste={handlePaste}
                  onFocus={(e) => e.target.select()}
                  style={{
                    width: "48px",
                    height: "56px",
                    textAlign: "center",
                    fontSize: "var(--font-size-xl)",
                    fontWeight: 700,
                    fontFamily: "var(--font-mono, monospace)",
                    background: digit
                      ? "rgba(var(--color-accent-rgb, 139, 92, 246), 0.08)"
                      : "var(--glass-bg, rgba(255,255,255,0.05))",
                    border: `1.5px solid ${
                      digit
                        ? "var(--color-accent)"
                        : "var(--glass-border-light, rgba(255,255,255,0.12))"
                    }`,
                    borderRadius: "var(--radius-md, 10px)",
                    color: "var(--color-text)",
                    outline: "none",
                    transition: "border-color 0.15s, background 0.15s, box-shadow 0.15s",
                    caretColor: "transparent",
                    cursor: "text",
                  }}
                  onFocus={(e) => {
                    e.target.select();
                    (e.target as HTMLInputElement).style.borderColor = "var(--color-accent)";
                    (e.target as HTMLInputElement).style.boxShadow =
                      "0 0 0 2px rgba(var(--color-accent-rgb, 139, 92, 246), 0.25)";
                  }}
                  onBlur={(e) => {
                    (e.target as HTMLInputElement).style.borderColor = digit
                      ? "var(--color-accent)"
                      : "var(--glass-border-light, rgba(255,255,255,0.12))";
                    (e.target as HTMLInputElement).style.boxShadow = "none";
                  }}
                />
              ))}
            </div>

            {/* New password field for password reset */}
            {isPasswordReset && (
              <GlassInput
                id="new-password"
                label="New Password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                autoComplete="new-password"
              />
            )}

            {error && (
              <p
                role="alert"
                style={{
                  color: "var(--color-danger)",
                  fontSize: "var(--font-size-sm)",
                  marginBottom: "var(--space-4)",
                  padding: "var(--space-2) var(--space-3)",
                  borderRadius: "var(--radius-sm)",
                  background: "rgba(212, 100, 92, 0.1)",
                  border: "1px solid rgba(212, 100, 92, 0.25)",
                }}
              >
                {error}
              </p>
            )}

            <GlassButton
              variant="primary"
              type="button"
              onClick={handleSubmit}
              disabled={!isComplete || loading || (isPasswordReset && !newPassword)}
              loading={loading}
              aria-label="Verify code"
              style={{ width: "100%" }}
            >
              {isPasswordReset ? "Reset Password" : "Verify Email"}
            </GlassButton>

            <p
              style={{
                marginTop: "var(--space-6)",
                fontSize: "var(--font-size-sm)",
                textAlign: "center",
                color: "var(--color-text-secondary)",
              }}
            >
              <Link to="/login" style={{ color: "var(--color-accent)" }}>
                Back to login
              </Link>
            </p>
          </GlassCard>
        </motion.div>
      </div>
    </PageTransition>
  );
}
