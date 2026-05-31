import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { apiClient } from "../../api/client";
import { PageTransition } from "../../components/PageTransition";
import { GlassCard } from "../../components/GlassCard";
import { GlassInput } from "../../components/GlassInput";
import { GlassButton } from "../../components/GlassButton";
import { GradientText } from "../../components/GradientText";
import { GoogleSignInWithCategoryPicker } from "../../components/GoogleSignInButton";
import { scaleIn } from "../../design-system";

export function Signup() {
  const navigate = useNavigate();
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [email, setEmail] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState("");
  const [category, setCategory] = useState("PROFESSIONAL");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await apiClient.post("/v1/auth/signups", {
        email,
        display_name: displayName,
        username,
        password,
        age: parseInt(age, 10),
        category,
      });
      navigate("/verify-otp", { state: { email, purpose: "VERIFY_EMAIL" } });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Signup failed";
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
                <GradientText variant="accent">Create Account</GradientText>
              </h1>
              <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", margin: 0 }}>
                Start your CSE prep journey
              </p>
            </div>

            {/* Google OAuth */}
            <GoogleSignInWithCategoryPicker />

            {/* Divider */}
            <div style={{ display: "flex", alignItems: "center", margin: "var(--space-5) 0", gap: "var(--space-3)" }}>
              <div style={{ flex: 1, height: "1px", background: "var(--glass-border-light)" }} />
              <span style={{ fontSize: "var(--font-size-sm)", color: "var(--color-text-muted)", whiteSpace: "nowrap" }}>or</span>
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
              <form onSubmit={handleSubmit} aria-label="Signup form">
                <GlassInput id="signup-email" label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required autoComplete="email" />
                <GlassInput id="signup-display-name" label="Display Name" type="text" value={displayName} onChange={(e) => setDisplayName(e.target.value)} required maxLength={255} placeholder="Your name" autoComplete="name" />
                <GlassInput id="signup-username" label="Username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} required minLength={3} maxLength={30} placeholder="Choose a username" autoComplete="username" />
                <GlassInput id="signup-password" label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="new-password" />
                <p style={{ color: "var(--color-text-muted)", fontSize: "var(--font-size-sm)", marginTop: "calc(-1 * var(--space-2))", marginBottom: "var(--space-3)" }}>
                  Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special character
                </p>
                <GlassInput id="signup-age" label="Age" type="number" min={15} max={100} value={age} onChange={(e) => setAge(e.target.value)} required />

                <div style={{ marginBottom: "var(--space-4)" }}>
                  <label htmlFor="signup-category" style={{ display: "block", marginBottom: "var(--space-1)", fontSize: "var(--font-size-sm)", fontWeight: 500, color: "var(--color-text-secondary)" }}>
                    Category
                  </label>
                  <select
                    id="signup-category"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    aria-label="Exam category"
                    style={{ width: "100%", padding: "var(--space-2) var(--space-3)", fontSize: "var(--font-size-base)", borderRadius: "var(--radius-md)", background: "rgba(255, 255, 255, 0.05)", border: "1px solid var(--glass-border-light)", color: "var(--color-text)" }}
                  >
                    <option value="PROFESSIONAL">Professional</option>
                    <option value="SUB_PROFESSIONAL">Sub-Professional</option>
                  </select>
                </div>

                {error && (
                  <p role="alert" style={{ color: "var(--color-danger)", fontSize: "var(--font-size-sm)", marginBottom: "var(--space-4)", padding: "var(--space-2) var(--space-3)", borderRadius: "var(--radius-sm)", background: "rgba(212, 100, 92, 0.1)", border: "1px solid rgba(212, 100, 92, 0.25)" }}>
                    {error}
                  </p>
                )}

                <GlassButton variant="primary" type="submit" disabled={loading} loading={loading} aria-label="Sign up" style={{ width: "100%", marginTop: "var(--space-2)" }}>
                  Sign Up
                </GlassButton>
              </form>
            )}

            <p style={{ marginTop: "var(--space-6)", fontSize: "var(--font-size-sm)", textAlign: "center", color: "var(--color-text-secondary)" }}>
              Already have an account?{" "}
              <Link to="/login" style={{ color: "var(--color-accent)", fontWeight: 500 }}>Log in</Link>
            </p>
          </GlassCard>
        </motion.div>
      </div>
    </PageTransition>
  );
}
