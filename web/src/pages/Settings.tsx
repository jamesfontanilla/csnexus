import { Link } from "react-router-dom";
import { GlassCard } from "../components/GlassCard";
import { GlassButton } from "../components/GlassButton";
import { PageTransition } from "../components/PageTransition";
import { GradientText } from "../components/GradientText";
import { AccessibilitySection } from "./settings/AccessibilitySection";
import { AccountSection } from "./settings/AccountSection";
import { ProfileSection } from "./settings/ProfileSection";
import { StudySection } from "./settings/StudySection";

const gradientTextStyle: React.CSSProperties = {
  fontFamily: "var(--font-display)",
  letterSpacing: "-0.02em",
};

export function Settings() {
  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 600 }}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginBottom: "var(--space-6)" }}>
          <Link to="/profile" style={{ textDecoration: "none" }} aria-label="Back to profile">
            <GlassButton variant="ghost" size="sm">
              ←
            </GlassButton>
          </Link>
          <h1 style={{ margin: 0, ...gradientTextStyle }}>
            <GradientText variant="accent">Settings</GradientText>
          </h1>
        </div>

        <div style={{ display: "grid", gap: "var(--space-5)" }}>
          <section aria-labelledby="settings-profile">
            <GlassCard>
              <h2
                id="settings-profile"
                style={{
                  fontSize: "var(--font-size-lg)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  margin: 0,
                  marginBottom: "var(--space-4)",
                }}
              >
                Profile
              </h2>
              <ProfileSection />
            </GlassCard>
          </section>

          <section aria-labelledby="settings-study">
            <GlassCard>
              <h2
                id="settings-study"
                style={{
                  fontSize: "var(--font-size-lg)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  margin: 0,
                  marginBottom: "var(--space-4)",
                }}
              >
                Study Preferences
              </h2>
              <StudySection />
            </GlassCard>
          </section>

          <section aria-labelledby="settings-accessibility">
            <GlassCard>
              <h2
                id="settings-accessibility"
                style={{
                  fontSize: "var(--font-size-lg)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  margin: 0,
                  marginBottom: "var(--space-4)",
                }}
              >
                Accessibility & Display
              </h2>
              <AccessibilitySection />
            </GlassCard>
          </section>

          <section aria-labelledby="settings-account">
            <GlassCard>
              <h2
                id="settings-account"
                style={{
                  fontSize: "var(--font-size-lg)",
                  fontWeight: 600,
                  color: "var(--color-text)",
                  margin: 0,
                  marginBottom: "var(--space-4)",
                }}
              >
                Account Management
              </h2>
              <AccountSection />
            </GlassCard>
          </section>
        </div>
      </div>
    </PageTransition>
  );
}
