import { useState, useEffect, useCallback } from "react";
import {
  milestonesApi,
  type MilestonesListResponse,
  type ConsistencyMetric,
} from "../api/milestones";

interface UseMilestonesReturn {
  milestones: MilestonesListResponse | null;
  consistency: ConsistencyMetric | null;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

/**
 * Hook for fetching milestone statuses and study consistency metrics.
 */
export function useMilestones(): UseMilestonesReturn {
  const [milestones, setMilestones] = useState<MilestonesListResponse | null>(null);
  const [consistency, setConsistency] = useState<ConsistencyMetric | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [milestonesRes, consistencyRes] = await Promise.all([
        milestonesApi.getAll(),
        milestonesApi.getConsistency(),
      ]);
      setMilestones(milestonesRes);
      setConsistency(consistencyRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load milestones");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  return { milestones, consistency, loading, error, refresh: fetchAll };
}
