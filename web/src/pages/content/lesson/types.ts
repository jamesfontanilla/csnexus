/**
 * Type definitions for the enhanced lesson parser output.
 * Maps directly to the JSON structure produced by scripts/parse_lesson.py
 */

export interface ContentBlock {
  type: "prose" | "table" | "code" | "formula" | "tip" | "warning" | "example" | "step_by_step" | "list" | "svg" | "check_understanding";
  content: string | TableData | InlineCheck[];
  language?: string;
}

export interface TableData {
  headers: string[];
  rows: string[][];
}

export interface InlineCheck {
  question: string;
  answer: string;
  rationale?: string;
}

export interface LessonSegment {
  index: number;
  /** Sections belonging to this segment */
  sections: LessonSection[];
  estimated_minutes: number;
  /** Inline comprehension checks gating the "Continue" button */
  checks: InlineCheck[];
}

export interface LessonSection {
  title: string;
  blocks: ContentBlock[];
  difficulty: string[];
  word_count: number;
  estimated_reading_seconds: number;
  subsections?: LessonSection[];
}

export interface PracticeProblem {
  number: number;
  question: string;
  answer: string;
  explanation: string;
  difficulty: "easy" | "medium" | "hard";
}

export interface TOCEntry {
  title: string;
  index: number;
}

export interface LessonMetadata {
  title: string;
  estimated_reading_minutes: number;
  section_count: number;
  has_practice_problems: boolean;
  practice_problem_count: number;
  difficulty_distribution: Record<string, number>;
  total_word_count: number;
  /** Present when the lesson has been segmented */
  segment_count?: number;
  is_segmented?: boolean;
}

/** Legacy fields (still present for backward compat) */
export interface LessonContentLegacy {
  explanations: { title?: string; heading?: string; body: string }[];
  worked_examples: { title: string; problem?: string; solution?: string; body?: string }[];
  key_takeaways: string[];
  summary: string;
}

/** Full enhanced lesson content from the parser */
export interface EnhancedLessonContent extends LessonContentLegacy {
  metadata: LessonMetadata;
  table_of_contents: TOCEntry[];
  sections: LessonSection[];
  practice_problems: PracticeProblem[];
  memory_aids: string[];
  exam_strategies: string[];
  /** Populated for clerical-ability lessons — segments group sections into ~3-5 min chunks */
  segments?: LessonSegment[];
  is_segmented?: boolean;
}

export interface LessonResponse {
  id: number;
  subtopic_id: number;
  content_json: EnhancedLessonContent;
  status: string;
}
