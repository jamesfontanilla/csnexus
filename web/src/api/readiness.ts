import { apiClient } from "./client";

// ─── Response Types ─────────────────────────────────────────────────────────

export interface ReadinessComponents {
  mastery_component: number;
  retention_component: number;
  mock_component: number;
  coverage_component: number;
}

export interface ReadinessResponse {
  score: number;
  components: ReadinessComponents;
  delta: number | null;
  stale_score: boolean;
}

export interface TopImpactSubtopic {
  subtopic_id: number;
  subtopic_name: string;
  point_impact: number;
}

export interface ScoreChangeSummary {
  primary_component: string;
  component_direction: string;
  component_magnitude: number;
  overall_delta: number;
}

export interface DashboardResponse {
  score: number;
  components: ReadinessComponents;
  delta: number | null;
  top_impact_subtopics: TopImpactSubtopic[];
  readiness_level: string;
  score_change_summary: ScoreChangeSummary | null;
  stale_data: boolean;
  computed_at: string | null;
}

export interface TrendPoint {
  date: string;
  score: number;
}

export interface TrendResponse {
  trend: TrendPoint[];
}

export interface SelfAssessmentRequest {
  self_assessed_score: number;
}

export interface SelfAssessmentResponse {
  self_assessed_score: number;
  computed_score: number;
  delta: number;
  calibration_status: string;
  message: string;
  calibration_warning: string | null;
}

export interface SelfAssessmentHistoryItem {
  self_assessed_score: number;
  computed_score: number;
  delta: number;
  calibration_status: string;
  assessed_at: string;
}

export interface SelfAssessmentHistoryResponse {
  records: SelfAssessmentHistoryItem[];
}

export interface SelfAssessmentPromptResponse {
  is_due: boolean;
  last_assessed_at: string | null;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const readinessApi = {
  getCurrent: () => apiClient.get<ReadinessResponse>("/v1/readiness"),

  getDashboard: () => apiClient.get<DashboardResponse>("/v1/readiness/dashboard"),

  getTrend: () => apiClient.get<TrendResponse>("/v1/readiness/trend"),

  submitSelfAssessment: (data: SelfAssessmentRequest) =>
    apiClient.post<SelfAssessmentResponse>("/v1/readiness/self-assessment", data),

  getSelfAssessmentHistory: () =>
    apiClient.get<SelfAssessmentHistoryResponse>("/v1/readiness/self-assessment/history"),

  getSelfAssessmentPrompt: () =>
    apiClient.get<SelfAssessmentPromptResponse>("/v1/readiness/self-assessment/prompt"),
};
