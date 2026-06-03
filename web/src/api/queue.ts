import { apiClient } from "./client";

// ─── Response Types ─────────────────────────────────────────────────────────

export interface QueueItem {
  id: number;
  position: number;
  item_type: "flashcard_review" | "quiz_practice" | "new_content";
  payload: Record<string, unknown>;
  estimated_seconds: number;
  completed_at: string | null;
}

export interface QueueResponse {
  items: QueueItem[];
  total_estimated_seconds: number;
  items_remaining: number;
  items_completed: number;
  time_budget_minutes: number;
}

export interface QueuePreferencesResponse {
  time_budget_minutes: number;
}

export interface QueuePreferencesRequest {
  time_budget_minutes: 15 | 30 | 60;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const queueApi = {
  getDaily: () => apiClient.get<QueueResponse>("/v1/queue"),

  completeItem: (itemId: number) =>
    apiClient.post<QueueResponse>(`/v1/queue/items/${itemId}/:complete`),

  regenerate: () => apiClient.post<QueueResponse>("/v1/queue/:regenerate"),

  getPreferences: () =>
    apiClient.get<QueuePreferencesResponse>("/v1/queue/preferences"),

  updatePreferences: (data: QueuePreferencesRequest) =>
    apiClient.patch<QueuePreferencesResponse>("/v1/queue/preferences", data),
};
