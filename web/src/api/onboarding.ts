import { apiClient } from "./client";

// ─── Request/Response Types ─────────────────────────────────────────────────

export interface OnboardingRequest {
  exam_date: string; // ISO date string YYYY-MM-DD
  exam_category: "Professional" | "Sub-Professional";
  time_budget_minutes: 15 | 30 | 60;
}

export interface OnboardingResponse {
  confirmation: string;
  warning: string | null;
}

export interface ExamDateUpdateRequest {
  exam_date: string; // ISO date string YYYY-MM-DD
}

export interface ExamDateUpdateResponse {
  confirmation: string;
  warning: string | null;
}

export interface PlanSummaryResponse {
  total_days: number;
  subtopics_per_week: number;
  mock_exams_scheduled: number;
  estimated_readiness_at_exam: number;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const onboardingApi = {
  submit: (data: OnboardingRequest) =>
    apiClient.post<OnboardingResponse>("/v1/onboarding", data),

  updateExamDate: (data: ExamDateUpdateRequest) =>
    apiClient.patch<ExamDateUpdateResponse>("/v1/onboarding/exam-date", data),

  getPlanSummary: () =>
    apiClient.get<PlanSummaryResponse>("/v1/onboarding/plan-summary"),
};
