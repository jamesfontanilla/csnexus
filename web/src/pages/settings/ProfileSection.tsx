import { useCallback, useEffect, useRef, useState } from "react";
import { apiClient, ApiError } from "../../api/client";
import { GlassButton } from "../../components/GlassButton";
import { useToast } from "../../context/ToastContext";

// --- Types ---

interface UserProfile {
  id: number;
  display_name: string;
  username: string | null;
  tz_name: string;
}

// --- Validation ---

const USERNAME_RE = /^[A-Za-z][A-Za-z0-9_]{2,29}$/;

/**
 * Validates a username against the canonical regex.
 * Exported for property testing.
 */
export function isValidUsername(value: string): boolean {
  return USERNAME_RE.test(value);
}

/**
 * Computes the PATCH payload by comparing current values to original values.
 * Only includes fields that differ. Exported for property testing.
 */
export function buildPatchPayload(
  original: { display_name: string; username: string; tz_name: string },
  current: { display_name: string; username: string; tz_name: string }
): Record<string, string> {
  const payload: Record<string, string> = {};
  if (current.display_name !== original.display_name) {
    payload.display_name = current.display_name;
  }
  if (current.username !== original.username) {
    payload.username = current.username;
  }
  if (current.tz_name !== original.tz_name) {
    payload.tz_name = current.tz_name;
  }
  return payload;
}

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
  marginTop: "var(--space-5)",
};

const inlineErrorStyle: React.CSSProperties = {
  marginTop: "var(--space-1)",
  fontSize: "var(--font-size-sm)",
  color: "var(--color-danger)",
};

const indicatorStyle: React.CSSProperties = {
  marginTop: "var(--space-1)",
  fontSize: "var(--font-size-sm)",
  display: "flex",
  alignItems: "center",
  gap: "var(--space-1)",
};

// --- Timezone list ---

function getTimezones(): string[] {
  try {
    return Intl.supportedValuesOf("timeZone");
  } catch {
    // Fallback for environments that don't support this API
    return ["UTC", "America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles", "Europe/London", "Asia/Manila", "Asia/Tokyo"];
  }
}

// --- Component ---

const DEBOUNCE_MS = 400;

export function ProfileSection() {
  const toast = useToast();

  // Original user data (from API)
  const [original, setOriginal] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Editable fields
  const [displayName, setDisplayName] = useState("");
  const [username, setUsername] = useState("");
  const [tzName, setTzName] = useState("");

  // Username availability state
  const [usernameChecking, setUsernameChecking] = useState(false);
  const [usernameAvailable, setUsernameAvailable] = useState<boolean | null>(null);
  const [usernameError, setUsernameError] = useState<string | null>(null);

  // Save state
  const [saving, setSaving] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});

  // Debounce ref
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Timezones
  const timezones = useRef(getTimezones()).current;

  // Load user profile on mount
  useEffect(() => {
    apiClient
      .get<UserProfile>("/v1/auth/me")
      .then((user) => {
        setOriginal(user);
        setDisplayName(user.display_name);
        setUsername(user.username ?? "");
        setTzName(user.tz_name);
      })
      .catch(() => {
        // Error loading user — handled gracefully
      })
      .finally(() => setLoading(false));
  }, []);

  // Debounced username availability check
  const checkUsername = useCallback((value: string) => {
    // Clear previous state
    setUsernameAvailable(null);
    setUsernameError(null);

    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Don't check if invalid format
    if (!isValidUsername(value)) {
      return;
    }

    // Don't check if it's the same as original
    if (original && value === original.username) {
      return;
    }

    setUsernameChecking(true);

    debounceRef.current = setTimeout(async () => {
      try {
        const result = await apiClient.get<{ available: boolean }>(
          `/v1/users/usernames:check?username=${encodeURIComponent(value)}`
        );
        setUsernameAvailable(result.available);
        if (!result.available) {
          setUsernameError("Username is taken");
        }
      } catch {
        // Network error — clear indicators, allow form submission (backend validates)
        setUsernameAvailable(null);
      } finally {
        setUsernameChecking(false);
      }
    }, DEBOUNCE_MS);
  }, [original]);

  function handleUsernameChange(value: string) {
    setUsername(value);
    setFieldErrors((prev) => {
      const next = { ...prev };
      delete next.username;
      return next;
    });

    if (value && !isValidUsername(value)) {
      setUsernameError("Must be 3–30 chars, start with a letter, letters/digits/underscores only");
      setUsernameAvailable(null);
      setUsernameChecking(false);
      if (debounceRef.current) clearTimeout(debounceRef.current);
      return;
    }

    setUsernameError(null);
    checkUsername(value);
  }

  async function handleSave() {
    if (!original) return;

    const payload = buildPatchPayload(
      {
        display_name: original.display_name,
        username: original.username ?? "",
        tz_name: original.tz_name,
      },
      { display_name: displayName, username, tz_name: tzName }
    );

    // Nothing to save
    if (Object.keys(payload).length === 0) return;

    setSaving(true);
    setFieldErrors({});

    try {
      const updated = await apiClient.patch<UserProfile>("/v1/users/me", payload);
      setOriginal(updated);
      setDisplayName(updated.display_name);
      setUsername(updated.username ?? "");
      setTzName(updated.tz_name);
      setUsernameAvailable(null);
      toast.success("Profile updated successfully");
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        if (err.status === 409 || err.code === "USERNAME_TAKEN") {
          setFieldErrors({ username: "Username is already taken" });
        } else if (err.status === 422) {
          // Try to parse field-level errors
          setFieldErrors({ _general: err.message });
        } else {
          setFieldErrors({ _general: err.message });
        }
      } else {
        setFieldErrors({ _general: "Failed to save profile" });
      }
    } finally {
      setSaving(false);
    }
  }

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  if (loading) {
    return (
      <p style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-sm)" }}>
        Loading profile…
      </p>
    );
  }

  if (!original) {
    return (
      <p style={{ color: "var(--color-danger)", fontSize: "var(--font-size-sm)" }}>
        Failed to load profile data.
      </p>
    );
  }

  const hasChanges =
    displayName !== original.display_name ||
    username !== (original.username ?? "") ||
    tzName !== original.tz_name;

  return (
    <div>
      {/* Display Name */}
      <div>
        <label htmlFor="profile-display-name" style={labelStyle}>
          Display Name
        </label>
        <input
          id="profile-display-name"
          type="text"
          value={displayName}
          onChange={(e) => {
            setDisplayName(e.target.value);
            setFieldErrors((prev) => {
              const next = { ...prev };
              delete next.display_name;
              return next;
            });
          }}
          maxLength={255}
          style={inputStyle}
          aria-label="Display name"
          aria-describedby={fieldErrors.display_name ? "profile-display-name-error" : undefined}
        />
        {fieldErrors.display_name && (
          <p id="profile-display-name-error" style={inlineErrorStyle} role="alert">
            {fieldErrors.display_name}
          </p>
        )}
      </div>

      {/* Username */}
      <div style={fieldGroupStyle}>
        <label htmlFor="profile-username" style={labelStyle}>
          Username
        </label>
        <input
          id="profile-username"
          type="text"
          value={username}
          onChange={(e) => handleUsernameChange(e.target.value)}
          maxLength={30}
          style={inputStyle}
          aria-label="Username"
          aria-describedby={
            usernameError
              ? "profile-username-error"
              : fieldErrors.username
                ? "profile-username-field-error"
                : undefined
          }
        />
        {/* Loading indicator */}
        {usernameChecking && (
          <p style={{ ...indicatorStyle, color: "var(--color-text-muted)" }} aria-live="polite">
            <span
              aria-hidden="true"
              style={{
                display: "inline-block",
                width: "0.75em",
                height: "0.75em",
                border: "2px solid currentColor",
                borderTopColor: "transparent",
                borderRadius: "50%",
                animation: "spin 0.6s linear infinite",
              }}
            />
            Checking availability…
          </p>
        )}
        {/* Available indicator */}
        {!usernameChecking && usernameAvailable === true && (
          <p style={{ ...indicatorStyle, color: "var(--color-success)" }} aria-live="polite">
            <span aria-hidden="true">✓</span> Username available
          </p>
        )}
        {/* Taken / validation error */}
        {!usernameChecking && usernameError && (
          <p id="profile-username-error" style={inlineErrorStyle} role="alert" aria-live="polite">
            {usernameAvailable === false && <span aria-hidden="true">✗ </span>}
            {usernameError}
          </p>
        )}
        {/* Field error from save */}
        {fieldErrors.username && (
          <p id="profile-username-field-error" style={inlineErrorStyle} role="alert">
            {fieldErrors.username}
          </p>
        )}
      </div>

      {/* Timezone */}
      <div style={fieldGroupStyle}>
        <label htmlFor="profile-timezone" style={labelStyle}>
          Timezone
        </label>
        <select
          id="profile-timezone"
          value={tzName}
          onChange={(e) => setTzName(e.target.value)}
          style={inputStyle}
          aria-label="Timezone"
        >
          {timezones.map((tz) => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </div>

      {/* General error */}
      {fieldErrors._general && (
        <p style={{ ...inlineErrorStyle, marginTop: "var(--space-4)" }} role="alert">
          {fieldErrors._general}
        </p>
      )}

      {/* Save button */}
      <div style={{ marginTop: "var(--space-6)" }}>
        <GlassButton
          variant="primary"
          onClick={handleSave}
          disabled={!hasChanges || saving || (usernameError !== null && usernameAvailable !== null)}
          loading={saving}
          aria-label="Save profile changes"
        >
          Save Changes
        </GlassButton>
      </div>
    </div>
  );
}
