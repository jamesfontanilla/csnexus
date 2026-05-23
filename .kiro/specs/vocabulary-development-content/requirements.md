# Requirements Document

## Introduction

This feature adds the "Vocabulary Development" content module to the Philippine Civil Service Exam (CSE) reviewer app. It is the second topic under the "Verbal Ability" subtest, following the existing "Grammar and Correct Usage" module. The feature involves authoring 12 subtopic lesson files and 12 corresponding question bank files (7,200 total questions), then updating the seed script to load this content into the database alongside the grammar content.

## Glossary

- **Seed_Script**: The Python script (`scripts/seed_content.py`) that parses flat content files and loads them into the database via SQLAlchemy models
- **Lesson_Parser**: The `parse_lesson_markdown()` function within the Seed_Script that splits lesson markdown by H2 sections and H3 subsections into a `LessonContent` JSON structure
- **Lesson_File**: A markdown file at `data/seed/lessons/verbal-ability/vocabulary-development/<subtopic-slug>/lesson.md` containing structured educational content
- **Question_File**: A JSON file at `data/seed/questions/verbal-ability/vocabulary-development/<subtopic-slug>/questions.json` containing an array of question objects
- **Subtopic**: One of 12 vocabulary development areas (e.g., synonyms, antonyms, context-clues) that maps to a `Subtopic` database record
- **Content_Hierarchy**: The database structure Module → Topic → Subtopic → Lesson/Questions
- **VOCAB_SUBTOPICS_CONFIG**: The ordered list of (slug, title, folder_name) tuples that drives the seed loop for vocabulary development content

## Requirements

### Requirement 1: Lesson File Structure

**User Story:** As a content author, I want each vocabulary development lesson to follow the parser-expected H2 structure, so that the Seed_Script can parse it into valid LessonContent JSON.

#### Acceptance Criteria

1. THE Lesson_File SHALL contain exactly four H2 sections in this order: `## Explanations`, `## Worked Examples`, `## Key Takeaways`, `## Summary`
2. WHEN the Lesson_Parser encounters the `## Explanations` section, THE Lesson_Parser SHALL split it into entries by H3 headings, producing an array of `{title, body}` objects
3. WHEN the Lesson_Parser encounters the `## Worked Examples` section, THE Lesson_Parser SHALL split it into entries by H3 headings, producing an array of `{title, problem, solution}` objects
4. WHEN the Lesson_Parser encounters the `## Key Takeaways` section, THE Lesson_Parser SHALL extract lines beginning with `- ` into a string array
5. THE Lesson_File SHALL have a top-level H1 heading matching the subtopic title
6. THE Lesson_File SHALL contain between 800 and 1200 lines of content
7. WHEN the `## Explanations` section contains H3 subsections, THE Lesson_Parser SHALL produce at least 6 entries for each vocabulary development subtopic

### Requirement 2: Lesson Content Quality

**User Story:** As a CSE examinee, I want vocabulary development lessons to use Philippine government and civil service context, so that the examples are relevant to the exam I am preparing for.

#### Acceptance Criteria

1. THE Lesson_File SHALL use Philippine government agencies, civil service roles, official documents, and Philippine cultural references in all examples
2. THE Lesson_File SHALL include an Introduction subsection explaining the concept and its relevance to the CSE
3. THE Lesson_File SHALL include a "Why <Subtopic> Is Tested in the CSE" subsection connecting the topic to government work and official communication
4. THE Lesson_File SHALL include a "Common Mistakes Examinees Make" subsection with 5 to 8 numbered specific errors
5. THE Lesson_File SHALL include a "Learning Objectives" subsection with 8 to 12 measurable objectives
6. WHEN a major concept section includes examples, THE Lesson_File SHALL provide examples at Easy, Medium, and Hard difficulty levels
7. THE Lesson_File SHALL use tables to present rules that have patterns or systematic mappings

### Requirement 3: Question File Schema

**User Story:** As a developer, I want each question JSON file to conform to the expected schema, so that the Seed_Script can load questions directly into the Question model without transformation errors.

#### Acceptance Criteria

1. THE Question_File SHALL contain a JSON array of exactly 600 question objects
2. THE Question_File SHALL contain exactly 200 questions with difficulty "Easy", 200 with difficulty "Medium", and 200 with difficulty "Hard"
3. THE Question_File SHALL assign sequential integer IDs from 1 to 600
4. WHEN a question object is defined, THE Question_File SHALL include all required fields: `id`, `subtest`, `module`, `subtopic`, `difficulty`, `question`, `choices`, `answer`, `explanation`, `tags`, `category`, `language`
5. THE Question_File SHALL set the `subtest` field to "Verbal Ability" for all questions
6. THE Question_File SHALL set the `module` field to "Vocabulary Development" for all questions
7. THE Question_File SHALL set the `subtopic` field to the Title Case name of the subtopic for all questions in that file
8. WHEN a question object specifies an `answer` value, THE Question_File SHALL ensure that value exactly matches one string in the `choices` array
9. THE Question_File SHALL provide exactly 4 choices per question
10. THE Question_File SHALL set the `category` field to `["Professional", "Sub-Professional"]` for all questions
11. THE Question_File SHALL set the `language` field to "English" for all questions
12. THE Question_File SHALL provide 2 to 3 lowercase string tags per question

### Requirement 4: Question Content Quality

**User Story:** As a CSE examinee, I want vocabulary questions to be varied, contextually relevant, and appropriately difficult, so that I can effectively prepare for the exam.

#### Acceptance Criteria

1. THE Question_File SHALL contain no duplicate or near-duplicate questions within the same file
2. THE Question_File SHALL use Philippine government and professional context in question stems and choices
3. THE Question_File SHALL include plausible distractors in all choices — no joke or obviously wrong answers
4. WHEN a question has difficulty "Easy", THE Question_File SHALL use common words, straightforward context, and familiar vocabulary
5. WHEN a question has difficulty "Medium", THE Question_File SHALL use less common words, require inference from context, and present moderate complexity
6. WHEN a question has difficulty "Hard", THE Question_File SHALL use advanced or formal vocabulary, subtle distinctions, complex sentence structures, or words with multiple meanings where context determines the answer
7. THE Question_File SHALL vary question formats across the 600 questions, including: meaning identification, sentence completion, fill-in-the-blank, correct usage identification, and context-based inference
8. WHEN a question includes an `explanation` field, THE Question_File SHALL provide a 1 to 2 sentence explanation of why the answer is correct

### Requirement 5: Subtopic Coverage

**User Story:** As a content manager, I want all 12 vocabulary development subtopics created with their lesson and question files, so that the module is complete for seeding.

#### Acceptance Criteria

1. THE Lesson_File SHALL exist at the path `data/seed/lessons/verbal-ability/vocabulary-development/<slug>/lesson.md` for each of the 12 subtopics
2. THE Question_File SHALL exist at the path `data/seed/questions/verbal-ability/vocabulary-development/<slug>/questions.json` for each of the 12 subtopics
3. THE Content_Hierarchy SHALL include these 12 subtopics in order: synonyms, antonyms, context-clues, multiple-meaning-words, commonly-confused-words, homonyms-homophones-homographs, word-formation, idioms-and-expressions, analogies, denotation-and-connotation, formal-vs-informal-language, technical-vocabulary
4. WHEN all 12 subtopics are created, THE Content_Hierarchy SHALL produce a total of 7,200 questions (12 subtopics × 600 questions each)

### Requirement 6: Seed Script Update

**User Story:** As a developer, I want the seed script updated to load vocabulary development content alongside grammar content, so that both topics are seeded into the database in a single run.

#### Acceptance Criteria

1. WHEN the Seed_Script executes, THE Seed_Script SHALL create a "Vocabulary Development" Topic record under the existing "Verbal Ability" Module
2. THE Seed_Script SHALL define a `VOCAB_SUBTOPICS_CONFIG` list containing all 12 subtopics as (slug, title, folder_name) tuples in the specified order
3. THE Seed_Script SHALL define `VOCAB_LESSONS` and `VOCAB_QUESTIONS` path constants pointing to `data/seed/lessons/verbal-ability/vocabulary-development` and `data/seed/questions/verbal-ability/vocabulary-development` respectively
4. WHEN the Seed_Script loads vocabulary development content, THE Seed_Script SHALL create Subtopic, Lesson, and Question records for both Professional and Sub-Professional categories
5. WHEN the Seed_Script has already seeded vocabulary development content, THE Seed_Script SHALL skip re-seeding (idempotent behavior)
6. IF a lesson or question file is missing for any configured subtopic, THEN THE Seed_Script SHALL raise a `FileNotFoundError` with the missing file path
7. THE Seed_Script SHALL assign `order_index=2` to the "Vocabulary Development" Topic (after "Grammar and Correct Usage" at `order_index=1`)

### Requirement 7: Valid JSON Output

**User Story:** As a developer, I want all question JSON files to be syntactically valid, so that `json.loads()` succeeds without errors during seeding.

#### Acceptance Criteria

1. THE Question_File SHALL be valid JSON parseable by Python's `json.loads()` without exceptions
2. THE Question_File SHALL contain no trailing commas after the last element in arrays or objects
3. THE Question_File SHALL properly escape special characters within string values (quotes, backslashes, newlines)
4. THE Question_File SHALL use UTF-8 encoding
