import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient } from "../../api/client";
import { login } from "../../stores/auth";
import { PageTransition } from "../../components/PageTransition";
import { GlassCard } from "../../components/GlassCard";
import { GlassInput } from "../../components/GlassInput";
import { GlassButton } from "../../components/GlassButton";
import { GradientText } from "../../components/GradientText";
import { GoogleSignInWithCategoryPicker } from "../../components/GoogleSignInButton";
import { scaleIn } from "../../design-system";

interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export function Login() {
  const navigate = useNavigate();
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await apiClient.post<LoginResponse>("/v1/auth/sessions", {
        email,
        password,
      });
      login(res.access_token);
      navigate("/modules");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Login failed";
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
            {/* Logo mark */}
            <div style={{ textAlign: "center", marginBottom: "var(--space-6)" }}>
              <div style={{ fontSize: "2.5rem", marginBottom: "var(--space-2)" }}>🎓</div>
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
                <GradientText variant="accent">Welcome back</GradientText>
              </h1>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", margin: 0 }}>
                Sign in to continue your prep
              </p>
            </div>

            {/* Google OAuth */}
            <GoogleSignInWithCategoryPicker />

            {/* Divider */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                margin: "var(--space-5) 0",
                gap: "var(--space-3)",
              }}
            >
              <div style={{ flex: 1, height: "1px", background: "var(--glass-border-light)" }} />
              <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", whiteSpace: "nowrap" }}>
                or
              </span>
              <div style={{ flex: 1, height: "1px", background: "var(--glass-border-light)" }} />
            </div>

            {/* Continue with Email toggle */}
            {!showEmailForm ? (
              <GlassButton
                variant="secondary"
                type="button"
                onClick={() => setShowEmailForm(true)}
                aria-label="Continue with email"
                style={{ width: "100%" }}
              >
                Continue with Email
              </GlassButton>
            ) : (
              <form onSubmit={handleSubmit} aria-label="Login form">
                <GlassInput
                  id="login-email"
                  label="Email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                />

                <GlassInput
                  id="login-password"
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                />

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
                  type="submit"
                  disabled={loading}
                  loading={loading}
                  aria-label="Log in"
                  style={{ width: "100%", marginTop: "var(--space-2)" }}
                >
                  Log In
                </GlassButton>

                <p style={{ marginTop: "var(--space-3)", fontSize: "var(--font-size-sm)", textAlign: "center" }}>
                  <Link to="/forgot-password" style={{ color: "var(--color-accent)" }}>
                    Forgot password?
                  </Link>
                </p>
              </form>
            )}

            <p
              style={{
                marginTop: "var(--space-6)",
                fontSize: "var(--font-size-sm)",
                textAlign: "center",
                color: "var(--color-text-secondary)",
              }}
            >
              Don't have an account?{" "}
              <Link to="/signup" style={{ color: "var(--color-accent)", fontWeight: 500 }}>
                Sign up
              </Link>
            </p>
          </GlassCard>
        </motion.div>
      </div>
    </PageTransition>
  );
}
