import { apiClient } from "./client";

// ─── Types ──────────────────────────────────────────────────────────────────

export interface PersonalNote {
  id: number;
  question_id: number;
  note_text: string;
  created_at: string;
}

export interface LessonReflection {
  id: number;
  lesson_id: number;
  section_index: number;
  reflection_text: string;
  created_at: string;
}

export interface RecallAnswerResponse {
  question_id: number;
  is_correct: boolean | null;
  match_type: string;
  correct_answer: string;
  user_response: string;
}

export interface GoodnightSessionItem {
  question_id: number;
  stem: string;
  correct_answer: string;
  confidence: number;
}

export interface GoodnightSessionResponse {
  items: GoodnightSessionItem[];
  estimated_minutes: number;
}

export interface SessionReflection {
  id: number;
  session_date: string;
  hardest_item_id: number | null;
  confidence_rating: number;
  review_note: string | null;
  created_at: string;
}

export interface ChallengeAttemptResponse {
  challenge_id: number;
  subtopic_id: number;
  question_stem: string;
  is_correct: boolean;
  message: string;
}

export interface ChallengeComparisonResponse {
  challenge_id: number;
  pre_lesson_correct: boolean | null;
  post_lesson_correct: boolean | null;
  is_productive_failure_success: boolean;
  message: string;
}

export interface PretestQuestion {
  id: number;
  stem: string;
  options: string[];
  key_concept: string;
}

export interface PretestStartResponse {
  pretest_id: number;
  subtopic_id: number;
  questions: PretestQuestion[];
}

export interface PretestSubmitResponse {
  pretest_id: number;
  score: number;
  total_questions: number;
  correct_count: number;
  weak_concepts: string[];
}

export interface PretestComparisonResponse {
  subtopic_id: number;
  pretest_score: number;
  post_lesson_score: number | null;
  improvement: number | null;
  message: string;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const learningTechniquesApi = {
  // Pretesting
  startPretest: (subtopicId: number) =>
    apiClient.post<PretestStartResponse>(`/v1/pretests/${subtopicId}/start`),

  submitPretest: (pretestId: number, answers: Array<{ question_id: number; selected_answer: string }>) =>
    apiClient.post<PretestSubmitResponse>(`/v1/pretests/${pretestId}/submit`, { answers }),

  getPretestComparison: (subtopicId: number) =>
    apiClient.get<PretestComparisonResponse>(`/v1/pretests/${subtopicId}/comparison`),

  // Elaborative Interrogation
  createNote: (questionId: number, noteText: string) =>
    apiClient.post<PersonalNote>(`/v1/explanations/${questionId}/note`, { note_text: noteText }),

  getAllNotes: () =>
    apiClient.get<PersonalNote[]>("/v1/notes"),

  createLessonReflection: (lessonId: number, data: { section_index: number; reflection_text: string }) =>
    apiClient.post<LessonReflection>(`/v1/lessons/${lessonId}/reflections`, data),

  // Recall Mode
  submitRecallAnswer: (attemptId: number, questionId: number, userResponse: string) =>
    apiClient.post<RecallAnswerResponse>(
      `/v1/quiz-attempts/${attemptId}/recall-answer?question_id=${questionId}`,
      { user_response: userResponse }
    ),

  // Sleep-Aware Review
  getGoodnightReview: () =>
    apiClient.get<GoodnightSessionResponse>("/v1/queue/goodnight"),

  completeGoodnightReview: () =>
    apiClient.post<{ status: string }>("/v1/queue/goodnight/:complete"),

  setBedtimePreference: (bedtime: string) =>
    apiClient.patch<{ bedtime: string }>("/v1/preferences/bedtime", { bedtime }),

  // Metacognitive Reflection
  createSessionReflection: (sessionDate: string, data: { hardest_item_id?: number; confidence_rating: number; review_note?: string }) =>
    apiClient.post<SessionReflection>(`/v1/sessions/${sessionDate}/reflection`, data),

  getSessionReflections: () =>
    apiClient.get<SessionReflection[]>("/v1/sessions/reflections"),

  // Productive Failure
  submitChallengeAttempt: (subtopicId: number, answer: string) =>
    apiClient.post<ChallengeAttemptResponse>(`/v1/challenges/${subtopicId}/attempt`, { answer }),

  submitChallengeRetest: (challengeId: number, answer: string) =>
    apiClient.post<ChallengeComparisonResponse>(`/v1/challenges/${challengeId}/retest`, { answer }),
};
