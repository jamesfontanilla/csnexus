import { useState, useEffect, useCallback } from "react";
import {
  queueApi,
  type QueueResponse,
  type QueuePreferencesResponse,
} from "../api/queue";

interface UseDailyQueueReturn {
  queue: QueueResponse | null;
  preferences: QueuePreferencesResponse | null;
  loading: boolean;
  error: string | null;
  completeItem: (itemId: number) => Promise<void>;
  regenerate: () => Promise<void>;
  updatePreferences: (timeBudget: 15 | 30 | 60) => Promise<void>;
  refresh: () => Promise<void>;
}

/**
 * Hook for managing the daily study queue.
 * Fetches queue and preferences on mount, and exposes actions for
 * completing items, regenerating, and updating time budget.
 */
export function useDailyQueue(): UseDailyQueueReturn {
  const [queue, setQueue] = useState<QueueResponse | null>(null);
  const [preferences, setPreferences] = useState<QueuePreferencesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [queueRes, prefsRes] = await Promise.all([
        queueApi.getDaily(),
        queueApi.getPreferences(),
      ]);
      setQueue(queueRes);
      setPreferences(prefsRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load daily queue");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  const completeItem = useCallback(async (itemId: number) => {
    try {
      const updatedQueue = await queueApi.completeItem(itemId);
      setQueue(updatedQueue);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to complete item");
    }
  }, []);

  const regenerate = useCallback(async () => {
    try {
      const updatedQueue = await queueApi.regenerate();
      setQueue(updatedQueue);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to regenerate queue");
    }
  }, []);

  const updatePreferences = useCallback(async (timeBudget: 15 | 30 | 60) => {
    try {
      const updatedPrefs = await queueApi.updatePreferences({
        time_budget_minutes: timeBudget,
      });
      setPreferences(updatedPrefs);
      // Preference change may regenerate the queue — refetch
      const updatedQueue = await queueApi.getDaily();
      setQueue(updatedQueue);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update preferences");
    }
  }, []);

  return {
    queue,
    preferences,
    loading,
    error,
    completeItem,
    regenerate,
    updatePreferences,
    refresh: fetchAll,
  };
}
