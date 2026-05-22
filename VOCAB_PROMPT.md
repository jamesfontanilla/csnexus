# Master Prompt — Topic 2: Vocabulary Development

Paste this into Kiro Web. It will generate the lesson markdown and questions JSON for each subtopic, one at a time.

---

## THE PROMPT

```
You are generating content for a Philippine Civil Service Exam (CSE) reviewer app. You are creating Topic 2: "Vocabulary Development" under the "Verbal Ability" subtest.

## CONTEXT

This is a FastAPI + SQLAlchemy project. Content lives in flat files that get seeded into the database:
- Lessons: `data/seed/lessons/verbal-ability/vocabulary-development/<subtopic-slug>/lesson.md`
- Questions: `data/seed/questions/verbal-ability/vocabulary-development/<subtopic-slug>/questions.json`

The seed script parses the lesson markdown by H2 sections and H3 subsections. The question JSON is loaded directly into the Question model.

## SUBTOPICS TO CREATE (in order)

1. synonyms
2. antonyms
3. context-clues
4. multiple-meaning-words
5. commonly-confused-words
6. homonyms-homophones-homographs
7. word-formation
8. idioms-and-expressions
9. analogies
10. denotation-and-connotation
11. formal-vs-informal-language
12. technical-vocabulary

## OUTPUT FORMAT — LESSON (lesson.md)

Each lesson MUST use exactly these H2 sections (the parser depends on them):

```markdown
# <Subtopic Title>

## Explanations

### Introduction
(What the concept is, why it matters, why it's tested in the CSE)

### Why <Subtopic> Is Tested in the CSE
(Connection to government work, official communication, exam coverage)

### Common Mistakes Examinees Make
(Numbered list of 5-8 specific errors)

### Learning Objectives
(Bulleted list of 8-12 measurable objectives)

---

### <Section Number>. <Rule/Concept Title>
(Detailed explanation with tables, examples, and CSE-style examples at Easy/Medium/Hard)

(Repeat for all major rules/concepts — aim for 6-12 sections depending on subtopic complexity)

---

## Worked Examples

### Example 1: <Descriptive Title>
**Problem:** (Present a CSE-style question)
**Step-by-step solution:**
1. ...
2. ...
**Answer:** ...

(Provide 5-7 worked examples covering different difficulty levels and sub-rules)

---

## Key Takeaways

- (10-12 bullet points summarizing the most important rules and strategies)

## Summary

(2-3 paragraph summary of the entire lesson, emphasizing exam strategy)
```

### LESSON CONTENT RULES:
- All content must be specific to the Philippine Civil Service Examination (Professional and Sub-Professional levels)
- Use Filipino/Philippine government context in examples (government agencies, civil servants, official documents, Philippine culture)
- Include tables for rules that have patterns
- Each major section should have CSE-style examples at Easy, Medium, and Hard levels
- Lessons should be 800-1200 lines long (comprehensive but focused)
- Use `---` horizontal rules to separate major sections
- H3 headings under `## Explanations` become individual lesson entries in the app

## OUTPUT FORMAT — QUESTIONS (questions.json)

A JSON array of exactly 600 question objects: 200 Easy + 200 Medium + 200 Hard.

Each question object:
```json
{
  "id": <sequential integer starting at 1>,
  "subtest": "Verbal Ability",
  "module": "Vocabulary Development",
  "subtopic": "<Subtopic Title in Title Case>",
  "difficulty": "Easy" | "Medium" | "Hard",
  "question": "<question stem>",
  "choices": ["<option A>", "<option B>", "<option C>", "<option D>"],
  "answer": "<exact string matching one of the choices>",
  "explanation": "<1-2 sentence explanation of why the answer is correct>",
  "tags": ["<tag1>", "<tag2>"],
  "category": ["Professional", "Sub-Professional"],
  "language": "English"
}
```

### QUESTION RULES:
- Exactly 600 questions per subtopic: 200 Easy, 200 Medium, 200 Hard
- IDs are sequential 1-600
- The `answer` field must EXACTLY match one string in `choices`
- 4 choices per question, always
- Choices should be plausible — no joke answers
- Tags should be 2-3 descriptive tags per question (lowercase)
- Questions must be unique — no duplicates or near-duplicates
- Use CSE-appropriate vocabulary and Philippine government/professional context
- Question formats to use (vary across the 600):
  - "Choose the word closest in meaning to the underlined/capitalized word"
  - "Which word best completes the sentence?"
  - "Choose the correct word to fill the blank"
  - "Which of the following is a synonym/antonym of ___?"
  - "Based on context, ___ most likely means:"
  - "Identify the correct usage"
  - Sentence-based questions with blanks
- Difficulty guidelines:
  - **Easy:** Common words, straightforward context, familiar vocabulary
  - **Medium:** Less common words, requires inference from context, moderate complexity
  - **Hard:** Advanced/formal vocabulary, subtle distinctions, complex sentence structures, words with multiple meanings where context determines the answer

## EXECUTION INSTRUCTIONS

Generate ONE subtopic at a time. For each subtopic, produce:
1. The complete `lesson.md` file
2. The complete `questions.json` file (all 600 questions)

Start with subtopic 1: **Synonyms**

After I confirm, proceed to the next subtopic. Do not skip ahead.

File paths:
- Lesson: `data/seed/lessons/verbal-ability/vocabulary-development/synonyms/lesson.md`
- Questions: `data/seed/questions/verbal-ability/vocabulary-development/synonyms/questions.json`

## QUALITY CHECKS BEFORE OUTPUTTING:
- [ ] Lesson has exactly 4 H2 sections: Explanations, Worked Examples, Key Takeaways, Summary
- [ ] Questions JSON is valid JSON (no trailing commas, proper escaping)
- [ ] Exactly 200 Easy + 200 Medium + 200 Hard = 600 total
- [ ] All `answer` values match exactly one item in their `choices` array
- [ ] No duplicate questions
- [ ] IDs are sequential 1-600
- [ ] `module` field is "Vocabulary Development" (not "Grammar and Correct Usage")
- [ ] Philippine CSE context throughout
- [ ] Tags are lowercase strings
```

---

## USAGE NOTES

- Paste the entire prompt above into Kiro Web
- After each subtopic is generated, save the files to the correct paths
- Then say "Next subtopic" to continue
- After all 12 subtopics are done, update `scripts/seed_content.py` to add the Vocabulary Development topic with its subtopics config
- The seed script will need a new `VOCAB_LESSONS` and `VOCAB_QUESTIONS` path, and a `VOCAB_SUBTOPICS_CONFIG` list mirroring the grammar one
