import { apiClient } from "./client";

// ─── Response Types ─────────────────────────────────────────────────────────

export interface ExplanationResponse {
  explanation_text: string;
  key_concept: string;
  related_subtopics: number[];
  cache_version: number;
  concrete_examples: string[] | null;
}

export interface BulkExplanationResponse {
  explanations: (ExplanationResponse | null)[];
}

export interface EscalationResponse {
  response: string;
  question_id: number;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const explanationsApi = {
  get: (questionId: number) =>
    apiClient.get<ExplanationResponse>(`/v1/explanations/${questionId}`),

  getBulk: (questionIds: number[]) =>
    apiClient.post<BulkExplanationResponse>("/v1/explanations/bulk", {
      question_ids: questionIds,
    }),

  escalate: (questionId: number) =>
    apiClient.post<EscalationResponse>(`/v1/explanations/${questionId}/:escalate`),
};
