import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiClient, ApiError } from "../../api/client";
import { logout } from "../../stores/auth";
import { GlassModal } from "../../components/GlassModal";
import { GlassButton } from "../../components/GlassButton";
import { useToast } from "../../context/ToastContext";

const CONFIRMATION_PHRASE = "DELETE MY ACCOUNT";

interface DeleteAccountDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DeleteAccountDialog({ open, onClose }: DeleteAccountDialogProps) {
  const navigate = useNavigate();
  const toast = useToast();

  const [phrase, setPhrase] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const phraseMatches = phrase === CONFIRMATION_PHRASE;

  async function handleConfirm() {
    if (!phraseMatches) return;

    setDeleting(true);
    setError(null);

    try {
      await apiClient.delete("/v1/users/me", {
        confirmation_phrase: CONFIRMATION_PHRASE,
      });
      toast.success("Account deleted successfully.");
      logout();
      navigate("/login", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 400) {
          setError("Confirmation phrase doesn't match.");
        } else {
          setError("Something went wrong. Please try again.");
        }
      } else {
        setError("Connection error. Please try again.");
      }
      setDeleting(false);
    }
  }

  function handleClose() {
    if (deleting) return;
    setPhrase("");
    setError(null);
    onClose();
  }

  return (
    <GlassModal isOpen={open} onClose={handleClose} title="Delete Account" size="sm">
      <div style={{ display: "flex", flexDirection: "column", gap: "var(--space-4)" }}>
        <p
          style={{
            color: "var(--color-danger)",
            fontSize: "var(--font-size-sm)",
            lineHeight: 1.5,
            margin: 0,
            fontWeight: 500,
          }}
        >
          This action is permanent and cannot be undone. All your data will be lost.
        </p>

        <div>
          <label
            htmlFor="delete-confirmation"
            style={{
              display: "block",
              fontSize: "var(--font-size-sm)",
              color: "var(--color-text-secondary)",
              marginBottom: "var(--space-2)",
            }}
          >
            Type <strong style={{ color: "var(--color-danger)" }}>{CONFIRMATION_PHRASE}</strong> to
            confirm:
          </label>
          <input
            id="delete-confirmation"
            type="text"
            value={phrase}
            onChange={(e) => {
              setPhrase(e.target.value);
              setError(null);
            }}
            disabled={deleting}
            autoComplete="off"
            spellCheck={false}
            style={{
              width: "100%",
              padding: "var(--space-2) var(--space-3)",
              background: "var(--glass-bg-subtle)",
              border: `1px solid ${phraseMatches ? "var(--color-danger)" : "var(--glass-border-medium)"}`,
              borderRadius: "var(--radius-md)",
              color: "var(--color-text)",
              fontSize: "var(--font-size-sm)",
              fontFamily: "inherit",
              outline: "none",
              boxSizing: "border-box",
            }}
          />
        </div>

        {error && (
          <p
            role="alert"
            style={{
              margin: 0,
              fontSize: "var(--font-size-sm)",
              color: "var(--color-danger)",
            }}
          >
            {error}
          </p>
        )}

        <div style={{ display: "flex", gap: "0.75rem", justifyContent: "flex-end" }}>
          <GlassButton
            variant="ghost"
            size="sm"
            onClick={handleClose}
            disabled={deleting}
          >
            Cancel
          </GlassButton>
          <GlassButton
            variant="danger"
            size="sm"
            onClick={handleConfirm}
            disabled={!phraseMatches || deleting}
            loading={deleting}
          >
            Delete My Account
          </GlassButton>
        </div>
      </div>
    </GlassModal>
  );
}
