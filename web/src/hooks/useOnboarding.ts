import { useState, useCallback } from "react";
import {
  onboardingApi,
  type OnboardingRequest,
  type OnboardingResponse,
  type PlanSummaryResponse,
} from "../api/onboarding";

interface UseOnboardingReturn {
  planSummary: PlanSummaryResponse | null;
  loading: boolean;
  error: string | null;
  submit: (data: OnboardingRequest) => Promise<OnboardingResponse | null>;
  updateExamDate: (examDate: string) => Promise<boolean>;
  fetchPlanSummary: () => Promise<void>;
}

/**
 * Hook for onboarding flow: submit exam date and preferences,
 * update exam date, and retrieve plan summary.
 */
export function useOnboarding(): UseOnboardingReturn {
  const [planSummary, setPlanSummary] = useState<PlanSummaryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = useCallback(
    async (data: OnboardingRequest): Promise<OnboardingResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await onboardingApi.submit(data);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit onboarding");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const updateExamDate = useCallback(async (examDate: string): Promise<boolean> => {
    setLoading(true);
    setError(null);
    try {
      await onboardingApi.updateExamDate({ exam_date: examDate });
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update exam date");
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchPlanSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await onboardingApi.getPlanSummary();
      setPlanSummary(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load plan summary");
    } finally {
      setLoading(false);
    }
  }, []);

  return { planSummary, loading, error, submit, updateExamDate, fetchPlanSummary };
}
