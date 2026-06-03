import { useState, useEffect, useCallback } from "react";
import { explanationsApi, type ExplanationResponse } from "../api/explanations";
import {
  getCachedExplanation,
  setCachedExplanation,
  bulkSetCachedExplanations,
} from "../stores/explanationCache";

interface UseExplanationReturn {
  explanation: ExplanationResponse | null;
  loading: boolean;
  error: string | null;
  escalate: () => Promise<string | null>;
}

/**
 * Hook for fetching a single question explanation with IndexedDB cache fallback.
 * Checks IndexedDB first, then falls back to API, storing the result for offline access.
 */
export function useExplanation(questionId: number | null): UseExplanationReturn {
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (questionId === null) {
      setExplanation(null);
      return;
    }

    let cancelled = false;

    async function fetch() {
      setLoading(true);
      setError(null);

      try {
        // Check IndexedDB cache first
        const cached = await getCachedExplanation(questionId!);
        if (cached && !cancelled) {
          setExplanation(cached);
          setLoading(false);

          // Background freshness check — if online, validate cache_version
          if (navigator.onLine) {
            try {
              const fresh = await explanationsApi.get(questionId!);
              if (!cancelled && fresh.cache_version !== cached.cache_version) {
                setExplanation(fresh);
                await setCachedExplanation(questionId!, fresh);
              }
            } catch {
              // Stale cache is acceptable; don't overwrite with error
            }
          }
          return;
        }

        // No cache — fetch from API (only if online)
        if (!navigator.onLine) {
          if (!cancelled) setExplanation(null);
          return;
        }

        const fresh = await explanationsApi.get(questionId!);
        if (!cancelled) {
          setExplanation(fresh);
          await setCachedExplanation(questionId!, fresh);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load explanation");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetch();
    return () => { cancelled = true; };
  }, [questionId]);

  const escalate = useCallback(async (): Promise<string | null> => {
    if (questionId === null) return null;
    try {
      const res = await explanationsApi.escalate(questionId);
      return res.response;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to escalate to tutor");
      return null;
    }
  }, [questionId]);

  return { explanation, loading, error, escalate };
}

/**
 * Prefetch explanations for a batch of question IDs and store them in IndexedDB.
 * Call this on quiz/session load for offline access.
 */
export async function prefetchExplanations(questionIds: number[]): Promise<void> {
  if (questionIds.length === 0) return;

  try {
    const res = await explanationsApi.getBulk(questionIds);
    const entries: Array<{ questionId: number; explanation: ExplanationResponse }> = [];

    res.explanations.forEach((exp, idx) => {
      if (exp !== null) {
        entries.push({ questionId: questionIds[idx], explanation: exp });
      }
    });

    await bulkSetCachedExplanations(entries);
  } catch {
    // Non-critical — explanations can be fetched individually on demand
  }
}
