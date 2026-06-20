import { apiClient } from "./client";

// ─── Enums / Literals ───────────────────────────────────────────────────────

export type DeckCategory = "verbal" | "numerical" | "analytical";
export type DeckVisibility = "private" | "public" | "unlisted";
export type CardType = "basic" | "reverse" | "cloze" | "mcq" | "true_false" | "matching" | "sequence";
export type StudyMode = "swipe" | "typing" | "rapid_recall" | "quiz" | "timed" | "exam_simulation";
export type ResponseType = "forgot" | "remembered" | "skipped";
export type ConfidenceLevel = "guessed" | "unsure" | "confident" | "mastered";

// ─── Deck Types ─────────────────────────────────────────────────────────────

export interface Deck {
  id: number;
  title: string;
  description: string | null;
  category: DeckCategory;
  visibility: DeckVisibility;
  tags: string | null;
  card_count: number;
  average_rating: number;
  created_at: string;
  updated_at: string;
}

export interface DeckCreate {
  title: string;
  category: DeckCategory;
  visibility: DeckVisibility;
  description?: string;
  tags?: string[];
}

// ─── Card Types ─────────────────────────────────────────────────────────────

export interface FlashCard {
  id: number;
  deck_id: number;
  front: string;
  back: string;
  card_type: CardType;
  hints: string[];
  tags: string[];
  created_at: string;
}

export interface CardCreate {
  front: string;
  back: string;
  card_type: CardType;
  hints?: string[];
  tags?: string[];
}

export interface CardUpdate {
  front?: string;
  back?: string;
  hints?: string[];
  tags?: string[];
}

// ─── Study Session Types ────────────────────────────────────────────────────

export interface StudySession {
  id: number;
  deck_ids: number[];
  study_mode: StudyMode;
  status: string;
  cards_reviewed: number;
  cards_correct: number;
  xp_earned: number;
  started_at: string;
  ended_at: string | null;
}

export interface SessionCreate {
  deck_ids: number[];
  study_mode: StudyMode;
}

export interface SessionCard {
  id: number;
  card_id: number;
  front: string;
  back: string;
  card_type: CardType;
  hints: string[];
}

export interface SessionResponse {
  card_id: number;
  response_type: ResponseType;
  confidence: ConfidenceLevel;
}

export interface SessionSummary {
  cards_reviewed: number;
  cards_correct: number;
  xp_earned: number;
  duration_seconds: number;
}

// ─── Review Queue Types ─────────────────────────────────────────────────────

export interface QueueCard {
  id: number;
  card_id: number;
  front: string;
  back: string;
  deck_title: string;
  due_at: string;
}

export interface QueueSummary {
  due_count: number;
  overdue_count: number;
  estimated_minutes: number;
}

// ─── Marketplace Types ──────────────────────────────────────────────────────

export interface MarketplaceDeck {
  id: number;
  title: string;
  description: string | null;
  category: DeckCategory;
  creator_name: string;
  average_rating: number;
  rating_count: number;
  clone_count: number;
  card_count: number;
}

export interface DeckRating {
  rating: number;
}

export interface DeckComment {
  id: number;
  user_name: string;
  comment: string;
  score: number;
  created_at: string;
}

// ─── Analytics Types ────────────────────────────────────────────────────────

export interface AnalyticsDashboard {
  overall_retention: number;
  total_cards_studied: number;
  total_sessions: number;
  strongest_subjects: SubjectStat[];
  weakest_subjects: SubjectStat[];
  predicted_readiness: number;
}

export interface SubjectStat {
  category: string;
  retention_rate: number;
  cards_studied: number;
}

export interface HeatmapEntry {
  date: string;
  cards_reviewed: number;
  retention_rate: number;
}

export interface Recommendation {
  id: number;
  deck_id: number;
  deck_title: string;
  reason: string;
  priority: number;
}

// ─── Exam Simulation Types ──────────────────────────────────────────────────

export interface ExamSimulation {
  id: number;
  deck_ids: number[];
  card_count: number;
  time_limit_minutes: number;
  status: string;
  score: number | null;
  percentage: number | null;
  time_taken_seconds: number | null;
  started_at: string;
  completed_at: string | null;
}

export interface ExamCreate {
  deck_ids: number[];
  card_count: number;
  time_limit_minutes: number;
}

export interface ExamCard {
  id: number;
  card_id: number;
  front: string;
  back: string;
  card_type: CardType;
}

export interface ExamAnswer {
  card_id: number;
  answer: string;
}

export interface ExamResult {
  score: number;
  total: number;
  percentage: number;
  time_taken_seconds: number;
  xp_earned: number;
}

// ─── API Functions ──────────────────────────────────────────────────────────

export const flashcardsApi = {
  // Decks
  getDecks: () => apiClient.get<Deck[]>("/v1/flashcards/decks"),
  getDeck: (id: number) => apiClient.get<Deck>(`/v1/flashcards/decks/${id}`),
  createDeck: (data: DeckCreate) => apiClient.post<Deck>("/v1/flashcards/decks", data),
  duplicateDeck: (id: number) => apiClient.post<Deck>(`/v1/flashcards/decks/${id}/:duplicate`),

  // Cards
  getDeckCards: (deckId: number) => apiClient.get<FlashCard[]>(`/v1/flashcards/decks/${deckId}/cards`),
  createCard: (deckId: number, data: CardCreate) => apiClient.post<FlashCard>(`/v1/flashcards/decks/${deckId}/cards`, data),
  updateCard: (_deckId: number, cardId: number, data: CardUpdate) => apiClient.patch<FlashCard>(`/v1/flashcards/cards/${cardId}`, data),
  deleteCard: (_deckId: number, cardId: number) => apiClient.delete<void>(`/v1/flashcards/cards/${cardId}`),

  // Study Sessions
  createSession: (data: SessionCreate) => apiClient.post<StudySession>("/v1/flashcards/sessions", data),
  getSessionCards: (sessionId: number) => apiClient.get<SessionCard[]>(`/v1/flashcards/sessions/${sessionId}/cards`),
  respondToCard: (sessionId: number, data: SessionResponse) => apiClient.post<void>(`/v1/flashcards/sessions/${sessionId}/respond`, data),
  endSession: (sessionId: number) => apiClient.post<SessionSummary>(`/v1/flashcards/sessions/${sessionId}/:end`),

  // Review Queue
  getQueue: () => apiClient.get<QueueCard[]>("/v1/flashcards/queue"),
  getQueueSummary: () => apiClient.get<QueueSummary>("/v1/flashcards/queue/summary"),

  // Marketplace
  getMarketplace: (params?: { search?: string; category?: string; sort?: string }) => {
    const query = new URLSearchParams();
    if (params?.search) query.set("search", params.search);
    if (params?.category) query.set("category", params.category);
    if (params?.sort) query.set("sort", params.sort);
    const qs = query.toString();
    return apiClient.get<MarketplaceDeck[]>(`/v1/flashcards/marketplace${qs ? `?${qs}` : ""}`);
  },
  cloneDeck: (id: number) => apiClient.post<Deck>(`/v1/flashcards/marketplace/${id}/:clone`),
  rateDeck: (id: number, data: DeckRating) => apiClient.post<void>(`/v1/flashcards/marketplace/${id}/ratings`, data),
  getDeckComments: (id: number) => apiClient.get<DeckComment[]>(`/v1/flashcards/marketplace/${id}/comments`),

  // Analytics
  getDashboard: () => apiClient.get<AnalyticsDashboard>("/v1/flashcards/analytics/dashboard"),
  getHeatmap: () => apiClient.get<HeatmapEntry[]>("/v1/flashcards/analytics/heatmap"),
  getRecommendations: () => apiClient.get<Recommendation[]>("/v1/flashcards/recommendations"),

  // Exam Simulations
  createExam: (data: ExamCreate) => apiClient.post<ExamSimulation>("/v1/flashcards/exam-simulations", data),
  getExamCards: (examId: number) => apiClient.get<ExamCard[]>(`/v1/flashcards/exam-simulations/${examId}/cards`),
  answerExamCard: (examId: number, data: ExamAnswer) => apiClient.post<void>(`/v1/flashcards/exam-simulations/${examId}/answer`, data),
  completeExam: (examId: number) => apiClient.post<ExamResult>(`/v1/flashcards/exam-simulations/${examId}/complete`),

  // Social / Feed
  getFeed: () => apiClient.get<Deck[]>("/v1/flashcards/feed"),

  // Deck management
  deleteDeck: (id: number) => apiClient.delete<void>(`/v1/flashcards/decks/${id}`),
  updateDeck: (id: number, data: { title?: string; description?: string; category?: string; visibility?: string }) =>
    apiClient.patch<Deck>(`/v1/flashcards/decks/${id}`, data),
  bookmarkDeck: (id: number) => apiClient.post<void>(`/v1/flashcards/marketplace/${id}/bookmark`),
  unbookmarkDeck: (id: number) => apiClient.delete<void>(`/v1/flashcards/marketplace/${id}/bookmark`),
  getComments: (deckId: number) => apiClient.get<DeckComment[]>(`/v1/flashcards/marketplace/${deckId}/comments`),
  postComment: (deckId: number, data: { body: string; parent_comment_id?: number }) =>
    apiClient.post<{ id: number }>(`/v1/flashcards/marketplace/${deckId}/comments`, data),
  deleteComment: (commentId: number) => apiClient.delete<void>(`/v1/flashcards/comments/${commentId}`),

  // Admin
  getAdminAnalytics: () => apiClient.get<{ top_failed_cards: Array<{ card_id: number; fail_count: number }>; active_reviewers_7d: number }>("/v1/flashcards/admin/analytics"),
  flagDeck: (id: number) => apiClient.post<void>(`/v1/flashcards/admin/decks/${id}/:flag`),
  featureDeck: (id: number) => apiClient.post<void>(`/v1/flashcards/admin/decks/${id}/:feature`),

  // Card Generation
  generateCards: (data: { lesson_content: string; lesson_id: number; requested_card_count: number }) =>
    apiClient.post<{ cards: Array<{ front: string; back: string; card_type: string; difficulty: string }>; terms_extracted: number }>("/v1/flashcards/generate", data),
};
