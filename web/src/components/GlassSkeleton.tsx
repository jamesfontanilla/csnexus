interface GlassSkeletonProps {
  width?: string;
  height?: string;
  borderRadius?: string;
  variant?: "text" | "card" | "avatar" | "button";
}

export function GlassSkeleton({
  width = "100%",
  height = "1rem",
  borderRadius = "var(--radius-md)",
  variant,
}: GlassSkeletonProps) {
  if (variant === "card") {
    return (
      <div
        aria-hidden="true"
        style={{
          width,
          borderRadius: "var(--radius-lg)",
          background: "var(--glass-bg-subtle)",
          border: "1px solid var(--glass-border-light)",
          padding: "var(--space-6)",
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-3)",
        }}
      >
        <SkeletonBar width="40%" height="0.875rem" />
        <SkeletonBar width="100%" height="0.75rem" />
        <SkeletonBar width="75%" height="0.75rem" />
        <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "var(--space-2)" }}>
          <SkeletonBar width="5rem" height="2rem" borderRadius="var(--radius-sm)" />
          <SkeletonBar width="4rem" height="2rem" borderRadius="var(--radius-sm)" />
        </div>
      </div>
    );
  }

  if (variant === "avatar") {
    return (
      <div
        aria-hidden="true"
        style={{
          width: height,
          height,
          borderRadius: "var(--radius-full)",
          background:
            "linear-gradient(90deg, var(--glass-bg-subtle) 25%, var(--glass-bg-medium) 50%, var(--glass-bg-subtle) 75%)",
          backgroundSize: "200% 100%",
          animation: "glass-shimmer 1.5s ease-in-out infinite",
        }}
      />
    );
  }

  return <SkeletonBar width={width} height={height} borderRadius={borderRadius} />;
}

function SkeletonBar({
  width = "100%",
  height = "1rem",
  borderRadius = "var(--radius-md)",
}: {
  width?: string;
  height?: string;
  borderRadius?: string;
}) {
  return (
    <div
      aria-hidden="true"
      style={{
        width,
        height,
        borderRadius,
        background:
          "linear-gradient(90deg, var(--glass-bg-subtle) 25%, var(--glass-bg-medium) 50%, var(--glass-bg-subtle) 75%)",
        backgroundSize: "200% 100%",
        animation: "glass-shimmer 1.5s ease-in-out infinite",
      }}
    />
  );
}
