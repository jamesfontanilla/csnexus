import { openDB, type DBSchema, type IDBPDatabase } from "idb";
import type { ExplanationResponse } from "../api/explanations";

/**
 * IndexedDB store for offline caching of question explanations.
 * Keyed by question_id with cache_version for staleness detection.
 *
 * Requirements: 9.1, 9.2, 9.3, 9.4
 */

interface CachedExplanation {
  question_id: number;
  explanation: ExplanationResponse;
  cached_at: number;
}

interface ExplanationCacheDB extends DBSchema {
  explanations: {
    key: number;
    value: CachedExplanation;
  };
}

let dbPromise: Promise<IDBPDatabase<ExplanationCacheDB>> | null = null;

function getDB(): Promise<IDBPDatabase<ExplanationCacheDB>> {
  if (!dbPromise) {
    dbPromise = openDB<ExplanationCacheDB>("cse-explanations", 1, {
      upgrade(db) {
        db.createObjectStore("explanations", { keyPath: "question_id" });
      },
    });
  }
  return dbPromise;
}

/**
 * Retrieve a cached explanation by question ID.
 * Returns null if not cached.
 */
export async function getCachedExplanation(
  questionId: number
): Promise<ExplanationResponse | null> {
  try {
    const db = await getDB();
    const record = await db.get("explanations", questionId);
    return record?.explanation ?? null;
  } catch {
    return null;
  }
}

/**
 * Store a single explanation in the cache.
 */
export async function setCachedExplanation(
  questionId: number,
  explanation: ExplanationResponse
): Promise<void> {
  try {
    const db = await getDB();
    await db.put("explanations", {
      question_id: questionId,
      explanation,
      cached_at: Date.now(),
    });
  } catch {
    // Non-critical — silently fail
  }
}

/**
 * Bulk-store explanations in a single transaction.
 * Used by the prefetch logic on quiz/session load.
 */
export async function bulkSetCachedExplanations(
  entries: Array<{ questionId: number; explanation: ExplanationResponse }>
): Promise<void> {
  if (entries.length === 0) return;

  try {
    const db = await getDB();
    const tx = db.transaction("explanations", "readwrite");
    const store = tx.store;

    for (const { questionId, explanation } of entries) {
      await store.put({
        question_id: questionId,
        explanation,
        cached_at: Date.now(),
      });
    }

    await tx.done;
  } catch {
    // Non-critical — silently fail
  }
}

/**
 * Check if a cached explanation is stale by comparing cache_version.
 * Returns true if the cached version differs from the provided version.
 */
export async function isCacheStale(
  questionId: number,
  currentVersion: number
): Promise<boolean> {
  const cached = await getCachedExplanation(questionId);
  if (!cached) return true;
  return cached.cache_version !== currentVersion;
}

/**
 * Clear all cached explanations (e.g., on logout or cache invalidation).
 */
export async function clearExplanationCache(): Promise<void> {
  try {
    const db = await getDB();
    await db.clear("explanations");
  } catch {
    // Non-critical
  }
}
