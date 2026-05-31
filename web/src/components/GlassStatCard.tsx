import type { ReactNode } from "react";
import { GlassCard } from "./GlassCard";
import { GradientText } from "./GradientText";

interface GlassStatCardProps {
  title: string;
  value: string | number;
  icon?: ReactNode;
  trend?: { direction: "up" | "down"; label: string };
}

export function GlassStatCard({ title, value, icon, trend }: GlassStatCardProps) {
  return (
    <GlassCard blur="sm" hoverable>
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
        <div>
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)", color: "var(--color-text-secondary)", fontWeight: 500, letterSpacing: "0.02em" }}>
            {title}
          </p>
          <p style={{ margin: "var(--space-1) 0 0", fontSize: "var(--font-size-2xl)", fontWeight: 700, fontFamily: "var(--font-display)", fontVariantNumeric: "tabular-nums" }}>
            <GradientText variant="accent">{value}</GradientText>
          </p>
          {trend && (
            <span style={{ fontSize: "var(--font-size-xs)", color: trend.direction === "up" ? "var(--color-success)" : "var(--color-danger)", fontWeight: 500 }}>
              {trend.direction === "up" ? "↑" : "↓"} {trend.label}
            </span>
          )}
        </div>
        {icon && (
          <span style={{ fontSize: "1.5rem", color: "var(--color-accent)", opacity: 0.8 }} aria-hidden="true">
            {icon}
          </span>
        )}
      </div>
    </GlassCard>
  );
}
