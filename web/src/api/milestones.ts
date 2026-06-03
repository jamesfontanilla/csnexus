import { apiClient } from "./client";

// ─── Response Types ─────────────────────────────────────────────────────────

export interface MilestoneStatus {
  id: number;
  slug: string;
  name: string;
  description: string;
  category: string;
  status: "locked" | "in_progress" | "earned";
  progress_percentage: number;
  awarded_at: string | null;
}

export interface MilestonesListResponse {
  milestones: MilestoneStatus[];
}

export interface ConsistencyMetric {
  current_streak: number;
  longest_streak: number;
  total_consistent_days: number;
  last_qualifying_date: string | null;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const milestonesApi = {
  getAll: () => apiClient.get<MilestonesListResponse>("/v1/milestones"),

  getConsistency: () => apiClient.get<ConsistencyMetric>("/v1/consistency"),
};
