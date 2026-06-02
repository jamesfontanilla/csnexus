import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiClient, ApiError } from "../../api/client";
import { logout } from "../../stores/auth";
import { GlassButton } from "../../components/GlassButton";
import { useToast } from "../../context/ToastContext";
import { DeleteAccountDialog } from "./DeleteAccountDialog";

// --- Password Validation ---

/**
 * Validates a password against the policy rules:
 * - 8+ characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one digit
 * - At least one symbol (non-alphanumeric, non-whitespace)
 *
 * Exported for property testing (task 10.3).
 */
export function isValidPassword(value: string): boolean {
  if (value.length < 8) return false;
  if (!/[A-Z]/.test(value)) return false;
  if (!/[a-z]/.test(value)) return false;
  if (!/[0-9]/.test(value)) return false;
  if (!/[^A-Za-z0-9\s]/.test(value)) return false;
  return true;
}

interface PasswordRule {
  label: string;
  test: (v: string) => boolean;
}

const PASSWORD_RULES: PasswordRule[] = [
  { label: "At least 8 characters", test: (v) => v.length >= 8 },
  { label: "At least one uppercase letter", test: (v) => /[A-Z]/.test(v) },
  { label: "At least one lowercase letter", test: (v) => /[a-z]/.test(v) },
  { label: "At least one digit", test: (v) => /[0-9]/.test(v) },
  { label: "At least one symbol", test: (v) => /[^A-Za-z0-9\s]/.test(v) },
];

// --- Styles ---

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: "var(--font-size-sm)",
  fontWeight: 500,
  color: "var(--color-text-secondary)",
  marginBottom: "var(--space-2)",
};

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "var(--space-2) var(--space-3)",
  background: "var(--glass-bg-subtle)",
  border: "1px solid var(--glass-border-medium)",
  borderRadius: "var(--radius-md)",
  color: "var(--color-text)",
  fontSize: "var(--font-size-sm)",
  fontFamily: "inherit",
  outline: "none",
  boxSizing: "border-box",
};

const fieldGroupStyle: React.CSSProperties = {
  marginTop: "var(--space-4)",
};

const inlineErrorStyle: React.CSSProperties = {
  marginTop: "var(--space-2)",
  fontSize: "var(--font-size-sm)",
  color: "var(--color-danger)",
};

const ruleListStyle: React.CSSProperties = {
  listStyle: "none",
  padding: 0,
  margin: "var(--space-2) 0 0 0",
  fontSize: "var(--font-size-xs)",
  display: "flex",
  flexDirection: "column",
  gap: "var(--space-1)",
};

const separatorStyle: React.CSSProperties = {
  height: 1,
  background: "var(--glass-border-light)",
  margin: "var(--space-5) 0",
  border: "none",
};

// --- Component ---

export function AccountSection() {
  const toast = useToast();
  const navigate = useNavigate();

  // Password change state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [changingPassword, setChangingPassword] = useState(false);

  // Delete account state
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  // --- Password Change ---

  async function handlePasswordChange(e: React.FormEvent) {
    e.preventDefault();
    setPasswordError(null);

    if (!currentPassword.trim()) {
      setPasswordError("Current password is required.");
      return;
    }

    if (!isValidPassword(newPassword)) {
      setPasswordError("New password does not meet all policy requirements.");
      return;
    }

    setChangingPassword(true);
    try {
      await apiClient.post("/v1/auth/password-change", {
        current_password: currentPassword,
        new_password: newPassword,
      });
      toast.success("Password changed successfully. Please log in again.");
      logout();
      navigate("/login", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 401) {
          setPasswordError("Current password is incorrect.");
        } else if (err.status === 400) {
          setPasswordError(err.message || "New password does not meet policy requirements.");
        } else {
          setPasswordError("Something went wrong. Please try again.");
        }
      } else {
        setPasswordError("Connection error. Please try again.");
      }
    } finally {
      setChangingPassword(false);
    }
  }

  // --- Logout ---

  async function handleLogout() {
    try {
      await apiClient.delete("/v1/auth/sessions/me");
    } catch {
      // Even if the API call fails, clear local state
    }
    logout();
    navigate("/login", { replace: true });
  }

  // --- Render ---

  const newPasswordTouched = newPassword.length > 0;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
      {/* Change Password Form */}
      <form onSubmit={handlePasswordChange} noValidate>
        <h3
          style={{
            fontSize: "var(--font-size-base)",
            fontWeight: 600,
            color: "var(--color-text)",
            margin: 0,
            marginBottom: "var(--space-3)",
          }}
        >
          Change Password
        </h3>

        <div>
          <label htmlFor="current-password" style={labelStyle}>
            Current Password
          </label>
          <input
            id="current-password"
            type="password"
            autoComplete="current-password"
            value={currentPassword}
            onChange={(e) => {
              setCurrentPassword(e.target.value);
              setPasswordError(null);
            }}
            style={inputStyle}
          />
        </div>

        <div style={fieldGroupStyle}>
          <label htmlFor="new-password" style={labelStyle}>
            New Password
          </label>
          <input
            id="new-password"
            type="password"
            autoComplete="new-password"
            value={newPassword}
            onChange={(e) => {
              setNewPassword(e.target.value);
              setPasswordError(null);
            }}
            style={inputStyle}
          />

          {/* Inline password policy feedback */}
          {newPasswordTouched && (
            <ul style={ruleListStyle} aria-label="Password requirements">
              {PASSWORD_RULES.map((rule) => {
                const passes = rule.test(newPassword);
                return (
                  <li
                    key={rule.label}
                    style={{
                      color: passes ? "var(--color-success)" : "var(--color-text-muted)",
                    }}
                  >
                    <span aria-hidden="true">{passes ? "✓" : "○"}</span>{" "}
                    {rule.label}
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        {passwordError && (
          <p style={inlineErrorStyle} role="alert">
            {passwordError}
          </p>
        )}

        <div style={{ marginTop: "var(--space-4)" }}>
          <GlassButton
            type="submit"
            variant="primary"
            size="sm"
            loading={changingPassword}
            disabled={changingPassword || !currentPassword || !newPassword}
          >
            Change Password
          </GlassButton>
        </div>
      </form>

      <hr style={separatorStyle} />

      {/* Logout */}
      <div>
        <h3
          style={{
            fontSize: "var(--font-size-base)",
            fontWeight: 600,
            color: "var(--color-text)",
            margin: 0,
            marginBottom: "var(--space-2)",
          }}
        >
          Session
        </h3>
        <p
          style={{
            fontSize: "var(--font-size-xs)",
            color: "var(--color-text-muted)",
            margin: "0 0 var(--space-3) 0",
          }}
        >
          Log out of your current session on this device.
        </p>
        <GlassButton variant="secondary" size="sm" onClick={handleLogout}>
          Log Out
        </GlassButton>
      </div>

      <hr style={separatorStyle} />

      {/* Delete Account */}
      <div>
        <h3
          style={{
            fontSize: "var(--font-size-base)",
            fontWeight: 600,
            color: "var(--color-danger)",
            margin: 0,
            marginBottom: "var(--space-2)",
          }}
        >
          Danger Zone
        </h3>
        <p
          style={{
            fontSize: "var(--font-size-xs)",
            color: "var(--color-text-muted)",
            margin: "0 0 var(--space-3) 0",
          }}
        >
          Permanently delete your account and all associated data. This action cannot be undone.
        </p>
        <GlassButton
          variant="danger"
          size="sm"
          onClick={() => setShowDeleteDialog(true)}
        >
          Delete Account
        </GlassButton>
      </div>

      <DeleteAccountDialog open={showDeleteDialog} onClose={() => setShowDeleteDialog(false)} />
    </div>
  );
}
