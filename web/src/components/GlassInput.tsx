import { forwardRef } from "react";
import "./GlassInput.css";

interface GlassInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export const GlassInput = forwardRef<HTMLInputElement, GlassInputProps>(
  ({ label, error, icon, className = "", id, value, maxLength, ...props }, ref) => {
    const inputId = id || `input-${label?.toLowerCase().replace(/\s+/g, "-") || "field"}`;
    const currentLength = typeof value === "string" ? value.length : 0;

    return (
      <div className="glass-input-group">
        {label && (
          <label htmlFor={inputId} className="glass-input-label">
            {label}
          </label>
        )}
        <div className="glass-input-wrapper">
          {icon && <span className="glass-input-icon" aria-hidden="true">{icon}</span>}
          <input
            ref={ref}
            id={inputId}
            className={`glass-input ${error ? "glass-input-error" : ""} ${className}`}
            aria-invalid={!!error}
            aria-describedby={error ? `${inputId}-error` : undefined}
            value={value}
            maxLength={maxLength}
            {...props}
          />
        </div>
        {maxLength !== undefined && (
          <span className="glass-input-char-count" data-testid="char-count">
            {currentLength}/{maxLength}
          </span>
        )}
        {error && (
          <p id={`${inputId}-error`} className="glass-input-error-text" role="alert" aria-live="polite">
            {error}
          </p>
        )}
      </div>
    );
  }
);
