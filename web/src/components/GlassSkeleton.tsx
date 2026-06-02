interface GlassSkeletonProps {
  width?: string;
  height?: string;
  borderRadius?: string;
  lines?: number;
  variant?: "text" | "card" | "avatar" | "button";
}

export function GlassSkeleton({
  width = "100%",
  height = "1rem",
  borderRadius = "var(--radius-md)",
  lines,
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
        className="skeleton"
        style={{
          width: height,
          height,
          borderRadius: "var(--radius-full)",
        }}
      />
    );
  }

  if (lines && lines > 1) {
    return (
      <div
        aria-hidden="true"
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "var(--space-2)",
          width,
        }}
      >
        {Array.from({ length: lines }, (_, i) => {
          const lineWidth = `${Math.max(100 - i * 15, 10)}%`;
          return (
            <SkeletonBar
              key={i}
              width={lineWidth}
              height={height}
              borderRadius={borderRadius}
            />
          );
        })}
      </div>
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
      className="skeleton"
      style={{
        width,
        height,
        borderRadius,
      }}
    />
  );
}
