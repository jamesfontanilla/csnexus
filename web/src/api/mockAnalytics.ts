import { apiClient } from "./client";

// ─── Response Types ─────────────────────────────────────────────────────────

export interface SubtopicBreakdown {
  subtopic_id: number;
  subtopic_name: string;
  questions_attempted: number;
  questions_correct: number;
  points_lost: number;
  avg_seconds_per_question: number;
  accuracy_percentage: number;
}

export interface DifficultyPerformance {
  easy: number | null;
  medium: number | null;
  hard: number | null;
}

export interface RegressionAlert {
  subtopic_id: number;
  decline_percentage_points: number;
}

export interface DiagnosticResponse {
  total_score: number;
  subtopic_breakdowns: SubtopicBreakdown[];
  highest_impact_areas: SubtopicBreakdown[];
  regression_alerts: RegressionAlert[];
  difficulty_performance: DifficultyPerformance;
}

export interface PredictionResponse {
  lower_bound: number | null;
  midpoint: number | null;
  upper_bound: number | null;
  confidence_level: string | null;
  message: string | null;
}

export interface Recommendation {
  id: number;
  subtopic_id: number;
  subtopic_name: string;
  current_accuracy: number;
  target_accuracy: number;
  estimated_point_gain: number;
  recommended_action: string;
  formatted_string: string;
  accepted_at: string | null;
}

export interface RecommendationsResponse {
  recommendations: Recommendation[];
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const mockAnalyticsApi = {
  getDiagnostic: (attemptId: number) =>
    apiClient.get<DiagnosticResponse>(`/v1/mock-analytics/${attemptId}`),

  getRecommendations: (attemptId: number) =>
    apiClient.get<RecommendationsResponse>(
      `/v1/mock-analytics/${attemptId}/recommendations`
    ),

  acceptRecommendation: (attemptId: number) =>
    apiClient.post<Recommendation>(
      `/v1/mock-analytics/${attemptId}/recommendations/:accept`
    ),

  getPrediction: () =>
    apiClient.get<PredictionResponse>("/v1/mock-analytics/prediction"),
};
