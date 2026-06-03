import { useState, useEffect, useCallback } from "react";
import {
  mockAnalyticsApi,
  type DiagnosticResponse,
  type RecommendationsResponse,
  type PredictionResponse,
} from "../api/mockAnalytics";

interface UseMockAnalyticsReturn {
  diagnostic: DiagnosticResponse | null;
  recommendations: RecommendationsResponse | null;
  prediction: PredictionResponse | null;
  loading: boolean;
  error: string | null;
  acceptRecommendation: () => Promise<void>;
  refreshRecommendations: () => Promise<void>;
}

/**
 * Hook for fetching mock exam analytics for a given attempt.
 * Loads diagnostic report, recommendations, and prediction.
 */
export function useMockAnalytics(attemptId: number | null): UseMockAnalyticsReturn {
  const [diagnostic, setDiagnostic] = useState<DiagnosticResponse | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationsResponse | null>(null);
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (attemptId === null) return;

    let cancelled = false;

    async function fetch() {
      setLoading(true);
      setError(null);
      try {
        const [diagRes, recsRes, predRes] = await Promise.all([
          mockAnalyticsApi.getDiagnostic(attemptId!),
          mockAnalyticsApi.getRecommendations(attemptId!),
          mockAnalyticsApi.getPrediction(),
        ]);
        if (!cancelled) {
          setDiagnostic(diagRes);
          setRecommendations(recsRes);
          setPrediction(predRes);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load analytics");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    fetch();
    return () => { cancelled = true; };
  }, [attemptId]);

  const acceptRecommendation = useCallback(async () => {
    if (attemptId === null) return;
    try {
      await mockAnalyticsApi.acceptRecommendation(attemptId);
      // Refresh recommendations to reflect the acceptance
      const updated = await mockAnalyticsApi.getRecommendations(attemptId);
      setRecommendations(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to accept recommendation");
    }
  }, [attemptId]);

  const refreshRecommendations = useCallback(async () => {
    if (attemptId === null) return;
    try {
      const updated = await mockAnalyticsApi.getRecommendations(attemptId);
      setRecommendations(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to refresh recommendations");
    }
  }, [attemptId]);

  return {
    diagnostic,
    recommendations,
    prediction,
    loading,
    error,
    acceptRecommendation,
    refreshRecommendations,
  };
}
