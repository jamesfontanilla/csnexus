# Tasks: Research-Backed Lesson Proper Refinement

## Overview

This task plan makes the research-backed lesson proper refinements executable. It starts with validation tooling, then creates a polished subject-verb agreement reference lesson, then scales the pattern across the lesson corpus.

## Tasks

- [x] 1. Build lesson proper quality validator
  - [x] 1.1 Create `scripts/validate_lesson_proper_quality.py`
    - Discover all `lesson.md` files under `data/seed/lessons`
    - Support `--lesson` for validating one lesson
    - Import and run `parse_lesson_markdown()`
    - Report pass/fail counts and per-file failures
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [x] 1.2 Add structural evidence checks
    - Check for at least two "Why does this work?" callouts
    - Check for at least two misconception blocks
    - Check for `Guided Practice`, `Which Method?`, `Before You Practice`, `Connections`, and `Mastery Checklist`
    - Check that `Which Method?` has at least six items where feasible
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 6.1, 6.2_

  - [x] 1.3 Add domain-fit artifact checks
    - Flag `[Brief rationale]`, `TODO`, and corrupted `??` markers
    - Flag grammar lessons containing "set up the equation", "computed answer", "ratio", "inverse", or "part-whole"
    - Flag math lessons containing unrelated grammar terms
    - Print exact line numbers for each artifact
    - _Requirements: 3.3, 3.4, 4.4, 7.4, 9.1, 9.2_

  - [x] 1.4 Add line-count and parser checks
    - Verify every lesson is 800 to 2000 lines
    - Verify parser returns non-empty `explanations`, `worked_examples`, `key_takeaways`, and `summary`
    - _Requirements: 1.5, 9.3, 9.4_

- [x] 2. Refine subject-verb agreement as reference lesson
  - [x] 2.1 Audit current SVA lesson
    - Run `scripts/validate_lesson_proper_quality.py --lesson data/seed/lessons/verbal-ability/grammar/subject-verb-agreement/lesson.md`
    - Record all structural, line-count, parser, and domain-fit failures
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [x] 2.2 Rebuild SVA lesson proper sequence
    - Organize rules into SVA clusters: basic rule, intervening phrases, compound subjects, proximity rule, indefinite pronouns, collective nouns, inverted sentences, number phrases, relative pronouns, percentages/fractions
    - Ensure each cluster has rule, example, trap, and recall prompt
    - _Requirements: 1.1, 1.2, 2.1, 2.3, 10.1_

  - [x] 2.3 Add SVA-specific retrieval prompts
    - Add at least two retrieval checks near rule sections
    - Prompts must ask for true subject, subject number, rule, or verb choice
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 2.4 Add SVA-specific elaborative callouts
    - Add at least two "Why does this work?" callouts
    - Explain head subject, modifier stripping, and proximity rule in grammar language
    - Remove generic math phrasing
    - _Requirements: 3.1, 3.2, 3.3, 10.2_

  - [x] 2.5 Add SVA misconception refutations
    - Include at least two misconception blocks
    - Required misconceptions: nearest noun controls agreement; sounds-right means correct
    - Optional misconceptions: "and always means plural"; all collective nouns are plural
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [x] 2.6 Add faded worked examples
    - Include full worked examples and partially completed examples
    - Faded steps must include true subject, number, rule, and verb choice
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 2.7 Add interleaved SVA discrimination practice
    - Include at least six mixed items
    - Each item asks learners to name the rule before answering
    - Include brief rationales
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 2.8 Add confidence and transfer sections
    - Rewrite `Before You Practice` with concrete SVA skills
    - Ensure `Connections` links to pronouns, clauses, sentence structure, and modifiers where relevant
    - _Requirements: 7.1, 7.2, 7.3, 7.5_

  - [x] 2.9 Add SVA visual decision aid
    - Add a compact flowchart for SVA rule selection
    - Keep parser-safe markdown or SVG
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [x] 2.10 Verify SVA lesson
    - Run enhanced lesson validator
    - Run lesson proper quality validator
    - Confirm no placeholder or domain-fit failures
    - Confirm line count is 800 to 2000
    - Confirm seed parser compatibility
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 10.5_

- [x] 3. Apply reference pattern to remaining grammar lessons
  - [x] 3.1 Audit all grammar lessons
    - Run quality validator against `data/seed/lessons/verbal-ability/grammar/**/lesson.md`
    - Prioritize lessons with placeholders, generic math language, or line-count failures
    - _Requirements: 9.1, 9.2, 9.3_

  - [x] 3.2 Refine verb-tenses lesson
    - Add tense timeline decision aid
    - Add interleaved tense discrimination practice
    - _Requirements: 1.1, 3.1, 5.1, 6.1, 8.1_

  - [x] 3.3 Refine pronouns lesson
    - Add antecedent tracing retrieval prompts
    - Add misconception blocks for case and agreement traps
    - _Requirements: 1.1, 2.1, 4.1, 6.1_

  - [x] 3.4 Refine prepositions lesson
    - Add spatial/function discrimination practice
    - Add faded examples for phrase analysis
    - _Requirements: 1.1, 5.1, 6.1_

  - [x] 3.5 Refine conjunctions lesson
    - Add relationship-identification practice
    - Add decision aid for coordinating/subordinating/correlative conjunctions
    - _Requirements: 6.1, 8.1_

  - [x] 3.6 Refine remaining grammar lessons
    - Articles, modifiers, parallelism, active/passive voice, direct/indirect speech
    - Ensure each passes quality validator
    - _Requirements: 1.1, 9.1, 9.2, 9.3_

- [x] 4. Apply pattern to verbal non-grammar lessons
  - [x] 4.1 Refine reading comprehension lessons
    - Convert retrieval prompts to passage-focused recall
    - Add faded passage analysis examples
    - Add interleaved question-type discrimination
    - _Requirements: 1.1, 2.1, 5.1, 6.1_

  - [x] 4.2 Refine sentence structure lessons
    - Add clause/sentence decision aids
    - Add misconception blocks for fragment/run-on/classification traps
    - _Requirements: 4.1, 6.1, 8.1_

  - [x] 4.3 Refine vocabulary lessons
    - Add context-fit discrimination practice
    - Add refutations for "closest synonym always works" and "tone does not matter"
    - _Requirements: 4.1, 6.1_

- [x] 5. Apply pattern to numerical and analytical lessons
  - [x] 5.1 Audit numerical lessons for grammar artifacts and placeholders
    - Keep math-specific phrasing where appropriate
    - Remove unrelated grammar terms
    - _Requirements: 9.1, 9.2_

  - [x] 5.2 Refine numerical lessons with faded examples
    - Add full -> partial -> independent problem sequences
    - Add mixed method choice practice
    - _Requirements: 5.1, 5.2, 6.1_

  - [x] 5.3 Refine analytical lessons with pattern discrimination
    - Add rule-selection prompts before solution steps
    - Add visual or symbolic decision aids where useful
    - _Requirements: 2.5, 6.1, 8.1_

- [x] 6. Final validation and seed verification
  - [x] 6.1 Run structural validator
    - Execute `scripts/validate_enhanced_lessons.py`
    - Confirm 100% pass rate
    - _Requirements: 9.4_

  - [x] 6.2 Run lesson proper quality validator
    - Execute `scripts/validate_lesson_proper_quality.py`
    - Confirm 100% pass rate
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [x] 6.3 Run seed pipeline
    - Execute `scripts/update_lessons.py` or `scripts/seed_all_content.py`
    - Confirm no parser or database errors
    - _Requirements: 1.5, 9.4_

  - [x] 6.4 Spot-check rendered lesson quality
    - Manually inspect SVA, one math lesson, one reading lesson, and one reasoning lesson
    - Confirm no visible placeholders or domain mismatch
    - _Requirements: 9.1, 9.2, 10.5_

- [x] 7. Execute full lesson proper manifest
  - [x] 7.1 Refine every lesson listed in `ALL_LESSON_PROPERS.md`
    - Work through each manifest checkbox by module and topic
    - Mark a lesson complete only after it passes single-lesson quality validation
    - _Requirements: 11.1, 11.2, 11.3, 11.5_

  - [x] 7.2 Run per-lesson validation loop
    - For each lesson, execute `scripts/validate_lesson_proper_quality.py --lesson <lesson_path>`
    - Fix all reported failures before moving to the next lesson
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 11.3_

  - [x] 7.3 Run final full-corpus quality gate
    - Execute `scripts/validate_lesson_proper_quality.py`
    - Confirm `Passing: 74` and `Failing: 0`
    - _Requirements: 9.5, 11.4, 11.5_

## Execution Notes

- The SVA lesson is the reference implementation. Do not batch-edit the full corpus until SVA passes the quality validator.
- Use the older `evidence-based-lesson-enhancements` spec for section presence. Use this spec for quality, sequencing, and research alignment.
- Keep lessons parser-safe: avoid new H2 sections outside existing parser expectations.
- Prefer compact, high-signal content over padding. The 800-line minimum should be satisfied with real examples, not repeated generic drills.

