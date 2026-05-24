/**
 * Type definitions for the enhanced lesson parser output.
 * Maps directly to the JSON structure produced by scripts/parse_lesson.py
 */

export interface ContentBlock {
  type: "prose" | "table" | "code" | "formula" | "tip" | "warning" | "example" | "step_by_step" | "list" | "svg";
  content: string | TableData;
  language?: string;
}

export interface TableData {
  headers: string[];
  rows: string[][];
}

export interface LessonSection {
  title: string;
  blocks: ContentBlock[];
  difficulty: string[];
  word_count: number;
  estimated_reading_seconds: number;
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
}

export interface LessonResponse {
  id: number;
  subtopic_id: number;
  content_json: EnhancedLessonContent;
  status: string;
}
