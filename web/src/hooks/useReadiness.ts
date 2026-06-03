import { useState, useEffect, useCallback } from "react";
import {
  readinessApi,
  type ReadinessResponse,
  type DashboardResponse,
  type TrendResponse,
  type SelfAssessmentResponse,
  type SelfAssessmentHistoryResponse,
  type SelfAssessmentPromptResponse,
} from "../api/readiness";

interface UseReadinessReturn {
  score: ReadinessResponse | null;
  dashboard: DashboardResponse | null;
  trend: TrendResponse | null;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

/**
 * Hook for fetching and caching readiness score, dashboard data, and trend.
 * Fetches all three on mount and exposes a refresh callback.
 */
export function useReadiness(): UseReadinessReturn {
  const [score, setScore] = useState<ReadinessResponse | null>(null);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [trend, setTrend] = useState<TrendResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [scoreRes, dashboardRes, trendRes] = await Promise.all([
        readinessApi.getCurrent(),
        readinessApi.getDashboard(),
        readinessApi.getTrend(),
      ]);
      setScore(scoreRes);
      setDashboard(dashboardRes);
      setTrend(trendRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load readiness data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  return { score, dashboard, trend, loading, error, refresh: fetchAll };
}

interface UseSelfAssessmentReturn {
  prompt: SelfAssessmentPromptResponse | null;
  history: SelfAssessmentHistoryResponse | null;
  loading: boolean;
  error: string | null;
  submit: (score: number) => Promise<SelfAssessmentResponse | null>;
  refreshPrompt: () => Promise<void>;
  refreshHistory: () => Promise<void>;
}

/**
 * Hook for self-assessment calibration: check if prompt is due,
 * submit a score, and fetch history.
 */
export function useSelfAssessment(): UseSelfAssessmentReturn {
  const [prompt, setPrompt] = useState<SelfAssessmentPromptResponse | null>(null);
  const [history, setHistory] = useState<SelfAssessmentHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refreshPrompt = useCallback(async () => {
    try {
      const res = await readinessApi.getSelfAssessmentPrompt();
      setPrompt(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to check self-assessment");
    }
  }, []);

  const refreshHistory = useCallback(async () => {
    try {
      const res = await readinessApi.getSelfAssessmentHistory();
      setHistory(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load assessment history");
    }
  }, []);

  useEffect(() => {
    setLoading(true);
    Promise.all([refreshPrompt(), refreshHistory()]).finally(() => setLoading(false));
  }, [refreshPrompt, refreshHistory]);

  const submit = useCallback(async (score: number): Promise<SelfAssessmentResponse | null> => {
    try {
      const res = await readinessApi.submitSelfAssessment({ self_assessed_score: score });
      // Refresh prompt status after submission
      await refreshPrompt();
      return res;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit self-assessment");
      return null;
    }
  }, [refreshPrompt]);

  return { prompt, history, loading, error, submit, refreshPrompt, refreshHistory };
}
