import { useEffect, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { usePageContext } from "../../context/PageContextRegistry";

interface BreadcrumbSegment {
  label: string;
  path: string;
}

/**
 * Formats a raw path segment into a display label.
 * Replaces hyphens with spaces and capitalizes the first letter.
 */
function formatSegmentLabel(segment: string): string {
  const withSpaces = segment.replace(/-/g, " ");
  return withSpaces.charAt(0).toUpperCase() + withSpaces.slice(1);
}

/**
 * Derives breadcrumb segments from the current location pathname
 * and optional label overrides from PageContext.
 */
function deriveBreadcrumbSegments(
  pathname: string,
  breadcrumbLabels?: Record<string, string>
): BreadcrumbSegment[] {
  const rawSegments = pathname.split("/").filter(Boolean);

  // Always start with Home for root
  const segments: BreadcrumbSegment[] = [{ label: "Home", path: "/" }];

  let currentPath = "";
  for (const segment of rawSegments) {
    currentPath += `/${segment}`;
    const label =
      breadcrumbLabels?.[segment] ?? formatSegmentLabel(segment);
    segments.push({ label, path: currentPath });
  }

  return segments;
}

/**
 * Determines which segments to display based on the overflow rule:
 * If more than 4 segments and not expanded, show first segment, ellipsis placeholder, and last 2 segments.
 * Otherwise show all segments.
 */
function getVisibleSegments(
  segments: BreadcrumbSegment[],
  expanded: boolean
): { visible: BreadcrumbSegment[]; hidden: BreadcrumbSegment[]; overflowing: boolean } {
  const OVERFLOW_THRESHOLD = 4;

  if (segments.length <= OVERFLOW_THRESHOLD || expanded) {
    return { visible: segments, hidden: [], overflowing: segments.length > OVERFLOW_THRESHOLD };
  }

  const first = segments[0];
  const lastTwo = segments.slice(-2);
  const hidden = segments.slice(1, segments.length - 2);

  return {
    visible: [first, ...lastTwo],
    hidden,
    overflowing: true,
  };
}

/**
 * BreadcrumbBar — a horizontal strip at the top of the Content_Area
 * showing the current navigation path with clickable ancestor segments.
 *
 * - Fixed 40px height with bottom border
 * - Derives segments from current location + PageContext.breadcrumbLabels
 * - Last segment is non-clickable with aria-current="page"
 * - Inactive segments are clickable React Router Links
 * - Collapses middle segments into ellipsis toggle when exceeding 4 segments
 */
export function BreadcrumbBar() {
  const { pathname } = useLocation();
  const { breadcrumbLabels } = usePageContext();
  const [ellipsisExpanded, setEllipsisExpanded] = useState(false);

  const segments = useMemo(
    () => deriveBreadcrumbSegments(pathname, breadcrumbLabels),
    [pathname, breadcrumbLabels]
  );

  // Reset expansion state when route changes
  useEffect(() => {
    setEllipsisExpanded(false);
  }, [pathname]);

  const { visible, hidden, overflowing } = getVisibleSegments(segments, ellipsisExpanded);

  return (
    <nav className="breadcrumb-bar" aria-label="Breadcrumb">
      <ol className="breadcrumb-bar__list">
        {ellipsisExpanded || !overflowing ? (
          // Render all segments (expanded or under threshold)
          segments.map((segment, index) => {
            const isLast = index === segments.length - 1;
            return (
              <li key={segment.path} className="breadcrumb-bar__item">
                {index > 0 && (
                  <span className="breadcrumb-bar__separator" aria-hidden="true">
                    ›
                  </span>
                )}
                {isLast ? (
                  <span
                    className="breadcrumb-bar__segment breadcrumb-bar__segment--current"
                    aria-current="page"
                  >
                    {segment.label}
                  </span>
                ) : (
                  <Link
                    to={segment.path}
                    className="breadcrumb-bar__segment breadcrumb-bar__segment--link"
                  >
                    {segment.label}
                  </Link>
                )}
              </li>
            );
          })
        ) : (
          // Collapsed view: first + ellipsis + last 2
          <>
            {/* First segment (Home) */}
            <li key={visible[0].path} className="breadcrumb-bar__item">
              <Link
                to={visible[0].path}
                className="breadcrumb-bar__segment breadcrumb-bar__segment--link"
              >
                {visible[0].label}
              </Link>
            </li>

            {/* Ellipsis toggle */}
            <li className="breadcrumb-bar__item breadcrumb-bar__item--ellipsis">
              <span className="breadcrumb-bar__separator" aria-hidden="true">
                ›
              </span>
              <button
                type="button"
                className="breadcrumb-bar__ellipsis-toggle"
                onClick={() => setEllipsisExpanded(true)}
                aria-label={`Show ${hidden.length} hidden breadcrumb segments`}
                title={hidden.map((s) => s.label).join(" › ")}
              >
                …
              </button>
            </li>

            {/* Last 2 segments */}
            {visible.slice(1).map((segment, index) => {
              const isLast = index === visible.length - 2;
              return (
                <li key={segment.path} className="breadcrumb-bar__item">
                  <span className="breadcrumb-bar__separator" aria-hidden="true">
                    ›
                  </span>
                  {isLast ? (
                    <span
                      className="breadcrumb-bar__segment breadcrumb-bar__segment--current"
                      aria-current="page"
                    >
                      {segment.label}
                    </span>
                  ) : (
                    <Link
                      to={segment.path}
                      className="breadcrumb-bar__segment breadcrumb-bar__segment--link"
                    >
                      {segment.label}
                    </Link>
                  )}
                </li>
              );
            })}
          </>
        )}
      </ol>
    </nav>
  );
}

// Export helpers for testing
export { deriveBreadcrumbSegments, formatSegmentLabel, getVisibleSegments };
export type { BreadcrumbSegment };
