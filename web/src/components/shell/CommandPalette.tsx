import { useRef, useEffect, useCallback, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useShell } from "../../context/ShellContext";
import { useFocusTrap } from "../../hooks/useFocusTrap";
import { useReducedMotion } from "../../design-system";
import {
  fuzzySearch,
  groupBySection,
  SECTION_LABELS,
  SECTION_ORDER,
} from "../../utils/fuzzySearch";
import type { FuzzySearchResult } from "../../utils/fuzzySearch";
import {
  getNavigationItems,
  getActionItems,
  getRecentItems,
} from "./commandPaletteItems";

/**
 * Command Palette — a centered modal overlay (Cmd/Ctrl+K) providing fuzzy search
 * across navigation, actions, and content.
 *
 * Features:
 * - Auto-focused search input on open
 * - 150ms debounced fuzzy matching
 * - Results grouped by section: Pages, Actions, Recent
 * - Keyboard navigation: ArrowUp/ArrowDown with visible highlight
 * - Enter or click executes the highlighted action
 * - Escape closes the palette and restores focus
 * - Highlighted index clamped to [0, N-1]
 * - Focus trapping within the palette
 */
export function CommandPalette() {
  const { state, actions } = useShell();
  const { commandPaletteOpen } = state;
  const reducedMotion = useReducedMotion();
  const inputRef = useRef<HTMLInputElement>(null);
  const resultsContainerRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Search state
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  // Focus trapping — cycles Tab/Shift+Tab within the palette and restores focus on close
  const containerRef = useFocusTrap(commandPaletteOpen);

  // Collect all palette items
  const allItems = useMemo(() => {
    const navItems = getNavigationItems(navigate);
    const actionItems = getActionItems({
      toggleSidebar: actions.toggleSidebar,
      toggleDetailPanel: actions.toggleDetailPanel,
      enterFocusMode: actions.enterFocusMode,
      exitFocusMode: actions.exitFocusMode,
    });
    const recentItems = getRecentItems(navigate);
    return [...navItems, ...actionItems, ...recentItems];
  }, [navigate, actions]);

  // Debounce query by 150ms
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 150);
    return () => clearTimeout(timer);
  }, [query]);

  // Compute search results
  const results: FuzzySearchResult[] = useMemo(() => {
    return fuzzySearch(debouncedQuery, allItems);
  }, [debouncedQuery, allItems]);

  // Reset highlighted index when results change
  useEffect(() => {
    setHighlightedIndex(0);
  }, [results]);

  // Reset state when palette opens/closes
  useEffect(() => {
    if (commandPaletteOpen) {
      setQuery("");
      setDebouncedQuery("");
      setHighlightedIndex(0);
    }
  }, [commandPaletteOpen]);

  // Auto-focus the search input when the palette opens
  useEffect(() => {
    if (commandPaletteOpen) {
      requestAnimationFrame(() => {
        inputRef.current?.focus();
      });
    }
  }, [commandPaletteOpen]);

  // Execute the action at the given index
  const executeAction = useCallback(
    (index: number) => {
      if (index >= 0 && index < results.length) {
        const result = results[index];
        actions.closeCommandPalette();
        result.item.action();
      }
    },
    [results, actions]
  );

  // Scroll the highlighted item into view
  const scrollHighlightedIntoView = useCallback((index: number) => {
    const container = resultsContainerRef.current;
    if (!container) return;

    const items = container.querySelectorAll('[role="option"]');
    const target = items[index] as HTMLElement | undefined;
    if (target) {
      target.scrollIntoView({ block: "nearest" });
    }
  }, []);

  // Keyboard navigation handler
  useEffect(() => {
    if (!commandPaletteOpen) return;

    function handleKeyDown(e: KeyboardEvent) {
      switch (e.key) {
        case "ArrowDown": {
          e.preventDefault();
          setHighlightedIndex((prev) => {
            const next = Math.min(prev + 1, results.length - 1);
            requestAnimationFrame(() => scrollHighlightedIntoView(next));
            return next;
          });
          break;
        }
        case "ArrowUp": {
          e.preventDefault();
          setHighlightedIndex((prev) => {
            const next = Math.max(prev - 1, 0);
            requestAnimationFrame(() => scrollHighlightedIntoView(next));
            return next;
          });
          break;
        }
        case "Enter": {
          e.preventDefault();
          executeAction(highlightedIndex);
          break;
        }
        case "Escape": {
          e.preventDefault();
          e.stopPropagation();
          actions.closeCommandPalette();
          break;
        }
      }
    }

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [
    commandPaletteOpen,
    results.length,
    highlightedIndex,
    executeAction,
    actions,
    scrollHighlightedIntoView,
  ]);

  // Close on backdrop click
  const handleBackdropClick = useCallback(() => {
    actions.closeCommandPalette();
  }, [actions]);

  // Prevent clicks inside the modal from propagating to the backdrop
  const handleModalClick = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
  }, []);

  // Handle input change
  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setQuery(e.target.value);
    },
    []
  );

  // Handle result click
  const handleResultClick = useCallback(
    (index: number) => {
      executeAction(index);
    },
    [executeAction]
  );

  // Group results for rendering with section headers
  const groupedResults = useMemo(() => {
    return groupBySection(results);
  }, [results]);

  // Build a flat render list with section headers and items for index tracking
  const renderList = useMemo(() => {
    const list: Array<
      | { type: "header"; section: string }
      | { type: "item"; result: FuzzySearchResult; flatIndex: number }
    > = [];
    let flatIndex = 0;

    for (const section of SECTION_ORDER) {
      const sectionResults = groupedResults.get(section);
      if (sectionResults && sectionResults.length > 0) {
        list.push({ type: "header", section: SECTION_LABELS[section] });
        for (const result of sectionResults) {
          list.push({ type: "item", result, flatIndex });
          flatIndex++;
        }
      }
    }

    return list;
  }, [groupedResults]);

  // Animation configuration
  const backdropInitial = { opacity: 0 };
  const backdropAnimate = { opacity: 1 };
  const backdropExit = { opacity: 0 };
  const backdropTransition = reducedMotion
    ? { duration: 0.08 }
    : { duration: 0.2 };

  const panelInitial = reducedMotion
    ? { opacity: 0 }
    : { opacity: 0, scale: 0.96, y: -8 };
  const panelAnimate = reducedMotion
    ? { opacity: 1 }
    : { opacity: 1, scale: 1, y: 0 };
  const panelExit = reducedMotion
    ? { opacity: 0 }
    : { opacity: 0, scale: 0.96, y: -8 };
  const panelTransition = reducedMotion
    ? { duration: 0.08 }
    : { type: "spring" as const, stiffness: 300, damping: 25, mass: 0.8 };

  return (
    <AnimatePresence>
      {commandPaletteOpen && (
        <div
          className="command-palette-overlay"
          style={{
            position: "fixed",
            inset: 0,
            zIndex: "var(--z-modal)" as unknown as number,
            display: "flex",
            justifyContent: "center",
            alignItems: "flex-start",
            paddingTop: "20vh",
          }}
        >
          {/* Backdrop */}
          <motion.div
            className="command-palette-backdrop"
            initial={backdropInitial}
            animate={backdropAnimate}
            exit={backdropExit}
            transition={backdropTransition}
            onClick={handleBackdropClick}
            style={{
              position: "absolute",
              inset: 0,
              background: "rgba(10, 10, 10, 0.7)",
              backdropFilter: "blur(12px)",
              WebkitBackdropFilter: "blur(12px)",
            }}
          />

          {/* Modal Container */}
          <motion.div
            ref={containerRef as React.RefObject<HTMLDivElement>}
            role="dialog"
            aria-modal="true"
            aria-label="Command palette"
            tabIndex={-1}
            initial={panelInitial}
            animate={panelAnimate}
            exit={panelExit}
            transition={panelTransition}
            onClick={handleModalClick}
            className="command-palette"
            style={{
              position: "relative",
              width: "560px",
              maxWidth: "calc(100vw - 2rem)",
              maxHeight: "60vh",
              display: "flex",
              flexDirection: "column",
              borderRadius: "var(--radius-lg, 12px)",
              background: "var(--glass-bg-subtle)",
              backdropFilter: "var(--glass-blur-sm)",
              WebkitBackdropFilter: "var(--glass-blur-sm)",
              border: "1px solid var(--glass-border-light)",
              boxShadow:
                "0 24px 48px rgba(0, 0, 0, 0.4), 0 8px 16px rgba(0, 0, 0, 0.2)",
              overflow: "hidden",
            }}
          >
            {/* Search Input */}
            <div
              className="command-palette__search"
              style={{
                padding: "var(--space-3, 12px) var(--space-4, 16px)",
                borderBottom: "1px solid var(--glass-border-light)",
                flexShrink: 0,
              }}
            >
              <input
                ref={inputRef}
                type="text"
                placeholder="Type a command or search..."
                aria-label="Search commands"
                aria-activedescendant={
                  results.length > 0
                    ? `command-palette-item-${highlightedIndex}`
                    : undefined
                }
                aria-controls="command-palette-results"
                autoComplete="off"
                spellCheck={false}
                value={query}
                onChange={handleInputChange}
                style={{
                  width: "100%",
                  padding: "var(--space-2, 8px) 0",
                  border: "none",
                  outline: "none",
                  background: "transparent",
                  color: "var(--color-text)",
                  fontSize: "var(--font-size-base, 16px)",
                  fontFamily: "inherit",
                }}
              />
            </div>

            {/* Results Area */}
            <div
              ref={resultsContainerRef}
              id="command-palette-results"
              className="command-palette__results"
              role="listbox"
              aria-label="Command results"
              style={{
                flex: 1,
                overflowY: "auto",
                padding: "var(--space-2, 8px)",
                minHeight: "80px",
              }}
            >
              {results.length === 0 && debouncedQuery.trim() !== "" && (
                <div
                  className="command-palette__empty"
                  style={{
                    padding: "var(--space-4, 16px)",
                    textAlign: "center",
                    color: "var(--color-text-secondary)",
                    fontSize: "var(--font-size-sm, 14px)",
                  }}
                >
                  No results found for &ldquo;{debouncedQuery}&rdquo;
                </div>
              )}

              {renderList.map((entry) => {
                if (entry.type === "header") {
                  return (
                    <div
                      key={`header-${entry.section}`}
                      className="command-palette__section-header"
                      style={{
                        padding:
                          "var(--space-2, 8px) var(--space-3, 12px) var(--space-1, 4px)",
                        fontSize: "var(--font-size-xs, 11px)",
                        fontWeight: 600,
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                        color: "var(--color-text-secondary)",
                      }}
                    >
                      {entry.section}
                    </div>
                  );
                }

                const { result, flatIndex } = entry;
                const isHighlighted = flatIndex === highlightedIndex;

                return (
                  <div
                    key={result.item.id}
                    id={`command-palette-item-${flatIndex}`}
                    role="option"
                    aria-selected={isHighlighted}
                    className={`command-palette__item ${isHighlighted ? "command-palette__item--active" : ""}`}
                    onClick={() => handleResultClick(flatIndex)}
                    onMouseEnter={() => setHighlightedIndex(flatIndex)}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "var(--space-3, 12px)",
                      padding:
                        "var(--space-2, 8px) var(--space-3, 12px)",
                      borderRadius: "var(--radius-sm, 6px)",
                      cursor: "pointer",
                      background: isHighlighted
                        ? "var(--state-hover-bg)"
                        : "transparent",
                      transition: "background var(--duration-instant, 80ms)",
                    }}
                  >
                    <div
                      className="command-palette__item-content"
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        flex: 1,
                        minWidth: 0,
                      }}
                    >
                      <span
                        className="command-palette__item-label"
                        style={{
                          color: "var(--color-text)",
                          fontSize: "var(--font-size-sm, 14px)",
                          fontWeight: 500,
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {result.item.label}
                      </span>
                      {result.item.description && (
                        <span
                          className="command-palette__item-description"
                          style={{
                            color: "var(--color-text-secondary)",
                            fontSize: "var(--font-size-xs, 11px)",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap",
                          }}
                        >
                          {result.item.description}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
