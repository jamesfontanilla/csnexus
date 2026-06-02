import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiClient } from "../api/client";
import { logout } from "../stores/auth";
import { GlassCard } from "../components/GlassCard";
import { GlassButton } from "../components/GlassButton";
import { GlassSkeleton } from "../components/GlassSkeleton";
import { AnimatedNumber } from "../components/AnimatedNumber";
import { GradientText } from "../components/GradientText";
import { PageTransition } from "../components/PageTransition";
import { GlassProgressBar } from "../components/GlassProgressBar";
import { GlassBadge } from "../components/GlassBadge";
import { useToast } from "../context/ToastContext";

interface XPData {
  cumulative_xp: number;
  level: number;
  streak: number;
}

interface UserProfile {
  display_name: string;
  email: string;
  category: string;
}

interface Achievement {
  achievement_id: string;
  title: string;
  description: string;
  granted_at: string;
}

const gradientTextStyle: React.CSSProperties = {
  fontFamily: "var(--font-display)",
  letterSpacing: "-0.02em",
};

export function Profile() {
  const navigate = useNavigate();
  const toast = useToast();
  const [xp, setXp] = useState<XPData | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Editable display name
  const [editingName, setEditingName] = useState(false);
  const [nameInput, setNameInput] = useState("");
  const [savingName, setSavingName] = useState(false);

  useEffect(() => {
    Promise.all([
      apiClient.get<XPData>("/v1/xp/me"),
      apiClient.get<Achievement[]>("/v1/achievements/me"),
      apiClient.get<UserProfile>("/v1/auth/me"),
    ])
      .then(([xpRes, achRes, profileRes]) => {
        setXp(xpRes);
        setAchievements(achRes);
        setProfile(profileRes);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  function handleLogout() {
    apiClient.delete("/v1/auth/sessions/me").catch(() => {});
    logout();
    toast.info("Logged out successfully");
    navigate("/login");
  }

  function startEditingName() {
    if (profile) {
      setNameInput(profile.display_name);
      setEditingName(true);
    }
  }

  async function handleSaveName() {
    const trimmed = nameInput.trim();
    if (!trimmed || trimmed === profile?.display_name) {
      setEditingName(false);
      return;
    }
    setSavingName(true);
    try {
      const updated = await apiClient.patch<UserProfile>("/v1/users/me", {
        display_name: trimmed,
      });
      setProfile(updated);
      toast.success("Display name updated");
      setEditingName(false);
    } catch (err: unknown) {
      toast.error(err instanceof Error ? err.message : "Failed to update name");
    } finally {
      setSavingName(false);
    }
  }

  if (loading) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 600 }}>
          <h1 style={{ ...gradientTextStyle }}><GradientText variant="accent">Profile</GradientText></h1>
          <GlassSkeleton variant="card" />
        </div>
      </PageTransition>
    );
  }

  if (error) {
    return (
      <PageTransition>
        <div className="page container" style={{ maxWidth: 600 }}>
          <p style={{ color: "var(--color-danger)" }}>{error}</p>
        </div>
      </PageTransition>
    );
  }

  const xpPerLevel = 100;
  const xpInLevel = xp ? xp.cumulative_xp % xpPerLevel : 0;

  return (
    <PageTransition>
      <div className="page container" style={{ maxWidth: 600 }}>
        <h1 style={{ marginBottom: "var(--space-2)", ...gradientTextStyle }}>
          <GradientText variant="accent">Profile</GradientText>
        </h1>

        {profile && (
          <div style={{ marginBottom: "var(--space-6)" }}>
            {editingName ? (
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", marginBottom: "var(--space-1)" }}>
                <input
                  type="text"
                  value={nameInput}
                  onChange={(e) => setNameInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSaveName();
                    if (e.key === "Escape") setEditingName(false);
                  }}
                  maxLength={255}
                  autoFocus
                  aria-label="Display name"
                  style={{
                    flex: 1,
                    fontSize: "1.25rem",
                    fontWeight: 600,
                    padding: "var(--space-2) var(--space-3)",
                    background: "var(--glass-bg-subtle)",
                    border: "1px solid var(--glass-border-medium)",
                    borderRadius: "var(--radius-md)",
                    color: "var(--color-text)",
                    outline: "none",
                    fontFamily: "var(--font-family)",
                  }}
                />
                <GlassButton
                  size="sm"
                  variant="primary"
                  onClick={handleSaveName}
                  loading={savingName}
                  aria-label="Save display name"
                >
                  Save
                </GlassButton>
                <GlassButton
                  size="sm"
                  variant="ghost"
                  onClick={() => setEditingName(false)}
                  disabled={savingName}
                  aria-label="Cancel editing"
                >
                  ✕
                </GlassButton>
              </div>
            ) : (
              <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", marginBottom: "var(--space-1)" }}>
                <p style={{ fontSize: "1.25rem", fontWeight: 600, margin: 0, color: "var(--color-text)" }}>
                  {profile.display_name}
                </p>
                <button
                  onClick={startEditingName}
                  aria-label="Edit display name"
                  style={{
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    fontSize: "0.875rem",
                    color: "var(--color-text-muted)",
                    padding: "var(--space-1)",
                    borderRadius: "var(--radius-sm)",
                    transition: "color var(--duration-fast) ease",
                  }}
                >
                  ✏️
                </button>
              </div>
            )}
            <p style={{ fontSize: "var(--font-size-sm)", margin: 0, color: "var(--color-text-secondary)" }}>
              {profile.email}
            </p>
          </div>
        )}

        {xp && (
          <GlassCard>
            <h2 style={{ fontSize: "var(--font-size-sm)", fontWeight: 600, color: "var(--color-text-secondary)", textTransform: "uppercase", letterSpacing: "0.05em", marginTop: 0, marginBottom: "var(--space-5)" }}>
              <GradientText variant="accent">Progress</GradientText>
            </h2>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "var(--space-4)", textAlign: "center", marginBottom: "var(--space-5)" }}>
              <div>
                <p style={{ fontSize: "1.75rem", fontWeight: 700, margin: 0, fontFamily: "var(--font-display)" }}>
                  <GradientText variant="accent"><AnimatedNumber value={xp.level} /></GradientText>
                </p>
                <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", margin: 0 }}>Level</p>
              </div>
              <div>
                <p style={{ fontSize: "1.75rem", fontWeight: 700, margin: 0, fontFamily: "var(--font-display)", color: "var(--color-text)" }}>
                  <AnimatedNumber value={xp.cumulative_xp} duration={1200} />
                </p>
                <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", margin: 0 }}>Total XP</p>
              </div>
              <div>
                <p style={{ fontSize: "1.75rem", fontWeight: 700, margin: 0, fontFamily: "var(--font-display)", color: "var(--color-warning)" }}>
                  🔥 <AnimatedNumber value={xp.streak} />
                </p>
                <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)", margin: 0 }}>Day Streak</p>
              </div>
            </div>
            <GlassProgressBar
              value={xpInLevel}
              max={xpPerLevel}
              label={`XP to Level ${xp.level + 1}`}
              color="var(--color-primary)"
              animated
            />
          </GlassCard>
        )}

        <section aria-label="Achievements" style={{ marginTop: "var(--space-6)" }}>
          <h2 style={{ marginBottom: "var(--space-4)", ...gradientTextStyle }}>
            <GradientText variant="accent">Achievements</GradientText>
          </h2>
          {achievements.length === 0 ? (
            <GlassCard>
              <p style={{ color: "var(--color-text-secondary)", margin: 0 }}>No achievements yet. Keep learning!</p>
            </GlassCard>
          ) : (
            <div style={{ display: "grid", gap: "var(--space-3)" }}>
              {achievements.map((a) => (
                <GlassCard key={a.achievement_id}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}>
                      <span style={{ fontSize: "1.25rem" }}>🏅</span>
                      <strong style={{ color: "var(--color-text)" }}>{a.title}</strong>
                    </div>
                    <GlassBadge
                      label={new Date(a.granted_at).toLocaleDateString()}
                      color="success"
                    />
                  </div>
                </GlassCard>
              ))}
            </div>
          )}
        </section>

        {/* Settings */}
        <section style={{ marginTop: "var(--space-6)" }}>
          <Link to="/settings" style={{ textDecoration: "none", display: "block" }} aria-label="Go to Settings">
            <GlassCard>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)" }}>
                  <span style={{ fontSize: "1.25rem" }}>⚙️</span>
                  <div>
                    <p style={{ margin: 0, color: "var(--color-text)", fontSize: "var(--font-size-base)", fontWeight: 500 }}>Settings</p>
                    <p style={{ margin: 0, color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>Preferences, accessibility, and account</p>
                  </div>
                </div>
                <span style={{ color: "var(--color-text-muted)", fontSize: "1.25rem" }}>›</span>
              </div>
            </GlassCard>
          </Link>
        </section>

        <div style={{ marginTop: "var(--space-8)", display: "flex", gap: "var(--space-4)" }}>
          <Link to="/modules" style={{ textDecoration: "none" }} aria-label="Back to modules">
            <GlassButton variant="secondary">← Modules</GlassButton>
          </Link>
          <GlassButton variant="danger" onClick={handleLogout} aria-label="Log out">
            Log Out
          </GlassButton>
        </div>
      </div>
    </PageTransition>
  );
}
