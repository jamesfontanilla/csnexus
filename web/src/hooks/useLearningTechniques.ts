import { useState, useCallback } from "react";
import {
  learningTechniquesApi,
  type ChallengeAttemptResponse,
  type ChallengeComparisonResponse,
  type GoodnightSessionResponse,
  type LessonReflection,
  type PersonalNote,
  type PretestComparisonResponse,
  type PretestStartResponse,
  type PretestSubmitResponse,
  type RecallAnswerResponse,
  type SessionReflection,
} from "../api/learningTechniques";

// ─── Notes (Elaborative Interrogation) ──────────────────────────────────────

interface UsePersonalNotesReturn {
  notes: PersonalNote[];
  loading: boolean;
  error: string | null;
  createNote: (questionId: number, noteText: string) => Promise<PersonalNote | null>;
  getAllNotes: () => Promise<void>;
}

export function usePersonalNotes(): UsePersonalNotesReturn {
  const [notes, setNotes] = useState<PersonalNote[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getAllNotes = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await learningTechniquesApi.getAllNotes();
      setNotes(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load notes");
    } finally {
      setLoading(false);
    }
  }, []);

  const createNote = useCallback(
    async (questionId: number, noteText: string): Promise<PersonalNote | null> => {
      setError(null);
      try {
        const note = await learningTechniquesApi.createNote(questionId, noteText);
        setNotes((prev) => [note, ...prev]);
        return note;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to save note");
        return null;
      }
    },
    []
  );

  return { notes, loading, error, createNote, getAllNotes };
}

// ─── Lesson Reflections ──────────────────────────────────────────────────────

interface UseLessonReflectionsReturn {
  loading: boolean;
  error: string | null;
  createLessonReflection: (
    lessonId: number,
    data: { section_index: number; reflection_text: string }
  ) => Promise<LessonReflection | null>;
}

export function useLessonReflections(): UseLessonReflectionsReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createLessonReflection = useCallback(
    async (
      lessonId: number,
      data: { section_index: number; reflection_text: string }
    ): Promise<LessonReflection | null> => {
      setLoading(true);
      setError(null);
      try {
        return await learningTechniquesApi.createLessonReflection(lessonId, data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to save reflection");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { loading, error, createLessonReflection };
}

// ─── Recall Mode ─────────────────────────────────────────────────────────────

interface UseRecallModeReturn {
  result: RecallAnswerResponse | null;
  loading: boolean;
  error: string | null;
  submitRecallAnswer: (
    attemptId: number,
    questionId: number,
    userResponse: string
  ) => Promise<RecallAnswerResponse | null>;
}

export function useRecallMode(): UseRecallModeReturn {
  const [result, setResult] = useState<RecallAnswerResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submitRecallAnswer = useCallback(
    async (
      attemptId: number,
      questionId: number,
      userResponse: string
    ): Promise<RecallAnswerResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await learningTechniquesApi.submitRecallAnswer(
          attemptId,
          questionId,
          userResponse
        );
        setResult(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit recall answer");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { result, loading, error, submitRecallAnswer };
}

// ─── Goodnight Review (Sleep-Aware Review) ───────────────────────────────────

interface UseGoodnightReviewReturn {
  session: GoodnightSessionResponse | null;
  loading: boolean;
  error: string | null;
  getGoodnightReview: () => Promise<void>;
  completeGoodnightReview: () => Promise<boolean>;
}

export function useGoodnightReview(): UseGoodnightReviewReturn {
  const [session, setSession] = useState<GoodnightSessionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getGoodnightReview = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await learningTechniquesApi.getGoodnightReview();
      setSession(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load goodnight review");
    } finally {
      setLoading(false);
    }
  }, []);

  const completeGoodnightReview = useCallback(async (): Promise<boolean> => {
    setError(null);
    try {
      await learningTechniquesApi.completeGoodnightReview();
      setSession(null);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to complete goodnight review");
      return false;
    }
  }, []);

  return { session, loading, error, getGoodnightReview, completeGoodnightReview };
}

// ─── Session Reflections (Metacognitive Reflection) ──────────────────────────

interface UseSessionReflectionsReturn {
  reflections: SessionReflection[];
  loading: boolean;
  error: string | null;
  createSessionReflection: (
    sessionDate: string,
    data: { hardest_item_id?: number; confidence_rating: number; review_note?: string }
  ) => Promise<SessionReflection | null>;
  getSessionReflections: () => Promise<void>;
}

export function useSessionReflections(): UseSessionReflectionsReturn {
  const [reflections, setReflections] = useState<SessionReflection[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getSessionReflections = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await learningTechniquesApi.getSessionReflections();
      setReflections(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load session reflections"
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const createSessionReflection = useCallback(
    async (
      sessionDate: string,
      data: { hardest_item_id?: number; confidence_rating: number; review_note?: string }
    ): Promise<SessionReflection | null> => {
      setError(null);
      try {
        const reflection = await learningTechniquesApi.createSessionReflection(
          sessionDate,
          data
        );
        setReflections((prev) => [reflection, ...prev]);
        return reflection;
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to save session reflection"
        );
        return null;
      }
    },
    []
  );

  return { reflections, loading, error, createSessionReflection, getSessionReflections };
}

// ─── Productive Failure (Challenge Attempts) ─────────────────────────────────

interface UseChallengeAttemptsReturn {
  attempt: ChallengeAttemptResponse | null;
  comparison: ChallengeComparisonResponse | null;
  loading: boolean;
  error: string | null;
  submitChallengeAttempt: (
    subtopicId: number,
    answer: string
  ) => Promise<ChallengeAttemptResponse | null>;
  submitChallengeRetest: (
    challengeId: number,
    answer: string
  ) => Promise<ChallengeComparisonResponse | null>;
}

export function useChallengeAttempts(): UseChallengeAttemptsReturn {
  const [attempt, setAttempt] = useState<ChallengeAttemptResponse | null>(null);
  const [comparison, setComparison] = useState<ChallengeComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submitChallengeAttempt = useCallback(
    async (
      subtopicId: number,
      answer: string
    ): Promise<ChallengeAttemptResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await learningTechniquesApi.submitChallengeAttempt(subtopicId, answer);
        setAttempt(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit challenge attempt");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const submitChallengeRetest = useCallback(
    async (
      challengeId: number,
      answer: string
    ): Promise<ChallengeComparisonResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await learningTechniquesApi.submitChallengeRetest(challengeId, answer);
        setComparison(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit challenge retest");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { attempt, comparison, loading, error, submitChallengeAttempt, submitChallengeRetest };
}

// ─── Pretesting ──────────────────────────────────────────────────────────────

interface UsePretestingReturn {
  pretest: PretestStartResponse | null;
  submitResult: PretestSubmitResponse | null;
  comparison: PretestComparisonResponse | null;
  loading: boolean;
  error: string | null;
  startPretest: (subtopicId: number) => Promise<PretestStartResponse | null>;
  submitPretest: (
    pretestId: number,
    answers: Array<{ question_id: number; selected_answer: string }>
  ) => Promise<PretestSubmitResponse | null>;
  getPretestComparison: (subtopicId: number) => Promise<PretestComparisonResponse | null>;
}

export function usePretesting(): UsePretestingReturn {
  const [pretest, setPretest] = useState<PretestStartResponse | null>(null);
  const [submitResult, setSubmitResult] = useState<PretestSubmitResponse | null>(null);
  const [comparison, setComparison] = useState<PretestComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startPretest = useCallback(
    async (subtopicId: number): Promise<PretestStartResponse | null> => {
      setLoading(true);
      setError(null);
      setPretest(null);
      setSubmitResult(null);
      try {
        const res = await learningTechniquesApi.startPretest(subtopicId);
        setPretest(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to start pretest");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const submitPretest = useCallback(
    async (
      pretestId: number,
      answers: Array<{ question_id: number; selected_answer: string }>
    ): Promise<PretestSubmitResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await learningTechniquesApi.submitPretest(pretestId, answers);
        setSubmitResult(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to submit pretest");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const getPretestComparison = useCallback(
    async (subtopicId: number): Promise<PretestComparisonResponse | null> => {
      setLoading(true);
      setError(null);
      try {
        const res = await learningTechniquesApi.getPretestComparison(subtopicId);
        setComparison(res);
        return res;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load comparison");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    pretest,
    submitResult,
    comparison,
    loading,
    error,
    startPretest,
    submitPretest,
    getPretestComparison,
  };
}
