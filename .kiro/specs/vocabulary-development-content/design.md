# Design Document

## Overview

This design adds the "Vocabulary Development" content module to the CSE reviewer app. It follows the identical pattern established by the existing "Grammar and Correct Usage" module: flat content files (lesson markdown + question JSON) organized by subtopic slug, loaded into the database via the seed script.

The implementation is purely additive — no existing code changes except extending `scripts/seed_content.py` with a new topic config block.

## Architecture

### File Structure

```
data/seed/
├── lessons/verbal-ability/vocabulary-development/
│   ├── synonyms/lesson.md
│   ├── antonyms/lesson.md
│   ├── context-clues/lesson.md
│   ├── multiple-meaning-words/lesson.md
│   ├── commonly-confused-words/lesson.md
│   ├── homonyms-homophones-homographs/lesson.md
│   ├── word-formation/lesson.md
│   ├── idioms-and-expressions/lesson.md
│   ├── analogies/lesson.md
│   ├── denotation-and-connotation/lesson.md
│   ├── formal-vs-informal-language/lesson.md
│   └── technical-vocabulary/lesson.md
└── questions/verbal-ability/vocabulary-development/
    ├── synonyms/questions.json
    ├── antonyms/questions.json
    ├── context-clues/questions.json
    ├── multiple-meaning-words/questions.json
    ├── commonly-confused-words/questions.json
    ├── homonyms-homophones-homographs/questions.json
    ├── word-formation/questions.json
    ├── idioms-and-expressions/questions.json
    ├── analogies/questions.json
    ├── denotation-and-connotation/questions.json
    ├── formal-vs-informal-language/questions.json
    └── technical-vocabulary/questions.json
```

### Database Hierarchy

```
Module: "Verbal Ability" (per category)
  └── Topic: "Grammar and Correct Usage" (order_index=1) [existing]
  └── Topic: "Vocabulary Development" (order_index=2) [NEW]
        ├── Subtopic 1: "Synonyms"
        ├── Subtopic 2: "Antonyms"
        ├── Subtopic 3: "Context Clues"
        ├── Subtopic 4: "Multiple-Meaning Words"
        ├── Subtopic 5: "Commonly Confused Words"
        ├── Subtopic 6: "Homonyms, Homophones, and Homographs"
        ├── Subtopic 7: "Word Formation"
        ├── Subtopic 8: "Idioms and Expressions"
        ├── Subtopic 9: "Analogies"
        ├── Subtopic 10: "Denotation and Connotation"
        ├── Subtopic 11: "Formal vs. Informal Language"
        └── Subtopic 12: "Technical Vocabulary"
```

## Components

### Component 1: Lesson Markdown Files

**Purpose:** Provide structured educational content for each vocabulary subtopic.

**Parser Contract:** The existing `parse_lesson_markdown()` function in `scripts/seed_content.py` splits by H2 headings and H3 subheadings. Each lesson MUST conform to:

```markdown
# <Subtopic Title>

## Explanations

### Introduction
(concept overview, CSE relevance)

### Why <Subtopic> Is Tested in the CSE
(government work connection)

### Common Mistakes Examinees Make
(numbered list, 5-8 items)

### Learning Objectives
(bulleted list, 8-12 items)

---

### <N>. <Rule/Concept Title>
(detailed explanation with tables, Easy/Medium/Hard examples)
(repeat for 6-12 concept sections)

---

## Worked Examples

### Example 1: <Title>
**Problem:** ...
**Step-by-step solution:**
1. ...
**Answer:** ...

(5-7 worked examples)

---

## Key Takeaways

- (10-12 bullet points)

## Summary

(2-3 paragraphs)
```

**Parser Output:** The `parse_lesson_markdown()` function produces:
```json
{
  "explanations": [{"title": "...", "body": "..."}],
  "worked_examples": [{"title": "...", "problem": "", "solution": "..."}],
  "key_takeaways": ["...", "..."],
  "summary": "..."
}
```

**Constraints:**
- 800-1200 lines per lesson
- Philippine government/CSE context in all examples
- Tables for pattern-based rules
- Easy/Medium/Hard examples in each concept section

### Component 2: Question JSON Files

**Purpose:** Provide 600 multiple-choice questions per subtopic for the question bank.

**Schema per question object:**
```json
{
  "id": 1,
  "subtest": "Verbal Ability",
  "module": "Vocabulary Development",
  "subtopic": "<Title Case Subtopic Name>",
  "difficulty": "Easy|Medium|Hard",
  "question": "<question stem>",
  "choices": ["<A>", "<B>", "<C>", "<D>"],
  "answer": "<exact match to one choice>",
  "explanation": "<1-2 sentences>",
  "tags": ["<tag1>", "<tag2>"],
  "category": ["Professional", "Sub-Professional"],
  "language": "English"
}
```

**Constraints:**
- Exactly 600 objects per file (IDs 1-600)
- Distribution: 200 Easy + 200 Medium + 200 Hard
- `answer` must exactly match one string in `choices`
- 4 choices per question, all plausible
- No duplicate or near-duplicate questions
- Tags: 2-3 lowercase strings
- Valid JSON (no trailing commas, proper escaping, UTF-8)

### Component 3: Seed Script Extension

**File:** `scripts/seed_content.py`

**Changes:**

1. Add path constants:
```python
VOCAB_LESSONS = SEED_BASE / "lessons" / "verbal-ability" / "vocabulary-development"
VOCAB_QUESTIONS = SEED_BASE / "questions" / "verbal-ability" / "vocabulary-development"
```

2. Add subtopics config:
```python
VOCAB_SUBTOPICS_CONFIG: list[tuple[str, str, str]] = [
    ("synonyms", "Synonyms", "synonyms"),
    ("antonyms", "Antonyms", "antonyms"),
    ("context-clues", "Context Clues", "context-clues"),
    ("multiple-meaning-words", "Multiple-Meaning Words", "multiple-meaning-words"),
    ("commonly-confused-words", "Commonly Confused Words", "commonly-confused-words"),
    ("homonyms-homophones-homographs", "Homonyms, Homophones, and Homographs", "homonyms-homophones-homographs"),
    ("word-formation", "Word Formation", "word-formation"),
    ("idioms-and-expressions", "Idioms and Expressions", "idioms-and-expressions"),
    ("analogies", "Analogies", "analogies"),
    ("denotation-and-connotation", "Denotation and Connotation", "denotation-and-connotation"),
    ("formal-vs-informal-language", "Formal vs. Informal Language", "formal-vs-informal-language"),
    ("technical-vocabulary", "Technical Vocabulary", "technical-vocabulary"),
]
```

3. Add a `seed_vocabulary_content(session)` function that:
   - Creates a "Vocabulary Development" Topic under the existing "Verbal Ability" Module with `order_index=2`
   - Iterates `VOCAB_SUBTOPICS_CONFIG` to create Subtopic, Lesson, and Question records
   - Follows the same pattern as the existing grammar seeding loop
   - Is idempotent (checks if topic slug already exists before seeding)

4. Update `seed_content()` to call `seed_vocabulary_content()` after grammar seeding.

**Idempotency:** Check for existing "vocabulary-development" topic slug before creating records. If found, skip.

**Error handling:** Raise `FileNotFoundError` with the missing path if any lesson or question file is absent.

## Data Flow

```
lesson.md → parse_lesson_markdown() → LessonContent JSON → Lesson.content_json
questions.json → json.loads() → list[dict] → Question records (one per dict)
```

The seed script creates the hierarchy for BOTH Professional and Sub-Professional categories (same content, different Module parent records), matching the existing grammar pattern.

## Constraints

- No changes to existing models, schemas, or API endpoints
- No new dependencies
- Content files are static — no runtime generation
- The existing `parse_lesson_markdown()` function is reused without modification
- All 12 subtopics must be present before the seed script can run successfully for vocabulary development
