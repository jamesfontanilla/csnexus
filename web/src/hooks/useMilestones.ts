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
      const [milestonesRes, consistencyRes] = await Promise.allSettled([
        milestonesApi.getAll(),
        milestonesApi.getConsistency(),
      ]);

      if (milestonesRes.status === "fulfilled") {
        setMilestones(milestonesRes.value);
      } else {
        setMilestones(null);
        setError(
          milestonesRes.reason instanceof Error
            ? milestonesRes.reason.message
            : "Failed to load milestones",
        );
      }

      if (consistencyRes.status === "fulfilled") {
        setConsistency(consistencyRes.value);
      } else {
        setConsistency(null);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  return { milestones, consistency, loading, error, refresh: fetchAll };
}
