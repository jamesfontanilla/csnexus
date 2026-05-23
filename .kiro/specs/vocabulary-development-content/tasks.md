# Tasks

## Task 1: Create Synonyms subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/synonyms/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/synonyms/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Synonyms"

## Task 2: Create Antonyms subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/antonyms/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/antonyms/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Antonyms"

## Task 3: Create Context Clues subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/context-clues/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/context-clues/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Context Clues"

## Task 4: Create Multiple-Meaning Words subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/multiple-meaning-words/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/multiple-meaning-words/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Multiple-Meaning Words"

## Task 5: Create Commonly Confused Words subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/commonly-confused-words/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/commonly-confused-words/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Commonly Confused Words"

## Task 6: Create Homonyms, Homophones, and Homographs subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/homonyms-homophones-homographs/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/homonyms-homophones-homographs/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Homonyms, Homophones, and Homographs"

## Task 7: Create Word Formation subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/word-formation/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/word-formation/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Word Formation"

## Task 8: Create Idioms and Expressions subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/idioms-and-expressions/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/idioms-and-expressions/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Idioms and Expressions"

## Task 9: Create Analogies subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/analogies/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/analogies/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Analogies"

## Task 10: Create Denotation and Connotation subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/denotation-and-connotation/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/denotation-and-connotation/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Denotation and Connotation"

## Task 11: Create Formal vs. Informal Language subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/formal-vs-informal-language/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/formal-vs-informal-language/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Formal vs. Informal Language"

## Task 12: Create Technical Vocabulary subtopic content
- [ ] Create `data/seed/lessons/verbal-ability/vocabulary-development/technical-vocabulary/lesson.md` following the H2/H3 parser structure (800-1200 lines, Philippine CSE context, Easy/Medium/Hard examples)
- [ ] Create `data/seed/questions/verbal-ability/vocabulary-development/technical-vocabulary/questions.json` with exactly 600 questions (200 Easy + 200 Medium + 200 Hard), sequential IDs 1-600, module="Vocabulary Development", subtopic="Technical Vocabulary"

## Task 13: Update seed script for Vocabulary Development
Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12
- [ ] Add `VOCAB_LESSONS` and `VOCAB_QUESTIONS` path constants to `scripts/seed_content.py`
- [ ] Add `VOCAB_SUBTOPICS_CONFIG` list with all 12 subtopics as (slug, title, folder_name) tuples
- [ ] Add `seed_vocabulary_content(session)` function that creates "Vocabulary Development" Topic (order_index=2) and seeds all subtopics
- [ ] Update `seed_content()` to call `seed_vocabulary_content()` after grammar seeding
- [ ] Ensure idempotency (skip if "vocabulary-development" topic already exists)
- [ ] Ensure `FileNotFoundError` is raised for missing content files
