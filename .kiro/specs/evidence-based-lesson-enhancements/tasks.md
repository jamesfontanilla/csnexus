# Implementation Plan: Evidence-Based Lesson Enhancements

## Overview

This plan enhances all ~74 existing lesson files with research-backed pedagogical elements: distributed retrieval prompts, elaborative interrogation, misconception confrontation, faded worked examples, interleaved discrimination practice, metacognitive confidence checks, transfer bridges, and dual coding visuals. Implementation proceeds in phases: tooling first, then batch enhancement by module, then cross-validation.

## Tasks

- [x] 1. Create validation tooling and reference template
  - [x] 1.1 Create validation script
    - Create `scripts/validate_enhanced_lessons.py`
    - Discover all `lesson.md` files under `data/seed/lessons/`
    - Check for required sections: Check Your Understanding (≥1), Elaborative Interrogation (≥1), Misconception Confrontation (≥2), Guided Practice, Which Method?, Before You Practice, Connections, Mastery Checklist
    - Run `parse_lesson_markdown()` on each and verify non-empty output fields
    - Print summary report with pass/fail counts and per-file failure details
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6_

  - [x] 1.2 Create enhanced lesson template reference
    - Create `data/seed/lessons/ENHANCED_TEMPLATE.md`
    - Show canonical section ordering with placeholder content
    - Include format examples for each new section type
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 1.3 Baseline validation run
    - Run validation script against current un-enhanced lessons
    - Confirm all sections correctly reported as missing (baseline)
    - _Requirements: 12.1, 12.2_


- [x] 2. Enhance Numerical Ability — Basic Operations (10 lessons)
  - [x] 2.1 Enhance fundamental-number-concepts lesson
    - Add 2 Elaborative Interrogation callouts, 2 Misconception Confrontation blocks
    - Add 1 Check Your Understanding block, Guided Practice, Which Method?, Before You Practice, Connections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 10.1, 11.1_

  - [x] 2.2 Enhance addition lesson
    - Add 2 Elaborative Interrogation callouts, 2 Misconception Confrontation blocks
    - Add 1-2 Check Your Understanding blocks, Guided Practice, Which Method?, Before You Practice, Connections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 6.1, 6.2, 7.1, 7.2, 8.1, 8.2, 10.1, 11.1_

  - [x] 2.3 Enhance subtraction lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.4 Enhance multiplication lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.5 Enhance division lesson
    - Add all required enhanced sections plus 1 Dual_Coding_Visual SVG (multiplication↔division inverse)
    - Add 2 Check Your Understanding blocks (after integer division, after fraction division)
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 9.3, 10.1, 11.1_

  - [x] 2.6 Enhance order-of-operations lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.7 Enhance exponents-and-roots lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.8 Enhance operations-with-signed-numbers lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.9 Enhance estimation-and-mental-math lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 2.10 Enhance word-problems lesson
    - Add all required enhanced sections with 6 Which Method? problems (identify operation)
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 6.3, 7.1, 8.1, 10.1, 11.1_


- [x] 3. Enhance Numerical Ability — Percentages (8 lessons)
  - [x] 3.1 Enhance fundamentals-of-percentages lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.2 Enhance basic-percentage-problems lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.3 Enhance percentage-increase-and-decrease lesson
    - Add all required enhanced sections plus 1 Dual_Coding_Visual (original vs new value diagram)
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1_

  - [x] 3.4 Enhance discounts-markups-and-sales lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.5 Enhance profit-loss-and-tax lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.6 Enhance percentage-applications lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.7 Enhance percentage-word-problems lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 3.8 Enhance percentage-mental-math-and-shortcuts lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 4. Enhance Numerical Ability — Ratio, Proportion, and Average (10 lessons)
  - [x] 4.1 Enhance introduction-to-ratios lesson
    - Add all required enhanced sections
    - Verify parser compatibility
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.2 Enhance types-of-ratios lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.3 Enhance ratio-word-problems lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.4 Enhance direct-and-inverse-proportions lesson
    - Add all required enhanced sections plus 1 Dual_Coding_Visual (direct vs inverse graph)
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1_

  - [x] 4.5 Enhance proportion-word-problems lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.6 Enhance scale-and-map-problems lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.7 Enhance introduction-to-average lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.8 Enhance weighted-average lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.9 Enhance finding-missing-values-in-averages lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 4.10 Enhance average-word-problems lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 5. Enhance Verbal Ability — Grammar (10 lessons)
  - [x] 5.1 Enhance subject-verb-agreement lesson
    - Add all required enhanced sections
    - Add 1 Dual_Coding_Visual (decision flowchart for SVA rules)
    - Adapt Which Method? to "which SVA rule applies?"
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 6.6, 7.1, 8.1, 9.2, 10.1, 11.1_

  - [x] 5.2 Enhance verb-tenses lesson
    - Add all required enhanced sections
    - Add 1 Dual_Coding_Visual (timeline diagram for tenses)
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 9.2, 10.1, 11.1_

  - [x] 5.3 Enhance pronouns lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.4 Enhance prepositions lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.5 Enhance conjunctions lesson
    - Add all required enhanced sections
    - Add 1 Dual_Coding_Visual (conjunction type decision flowchart)
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 9.2, 10.1, 11.1_

  - [x] 5.6 Enhance articles lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.7 Enhance modifiers lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.8 Enhance parallelism lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.9 Enhance active-and-passive-voice lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 5.10 Enhance direct-and-indirect-speech lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 6. Enhance Verbal Ability — Reading Comprehension (5 lessons)
  - [x] 6.1 Enhance fundamentals-of-reading-comprehension lesson
    - Add all required enhanced sections
    - Adapt Guided Practice to passage-based exercises with faded analysis steps
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 6.2 Enhance vocabulary-in-context lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 6.3 Enhance analytical-comprehension lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 6.4 Enhance authors-purpose-and-tone lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 6.5 Enhance organization-of-ideas lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

- [x] 7. Enhance Verbal Ability — Sentence Structure (4 lessons)
  - [x] 7.1 Enhance basic-components-of-a-sentence lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 7.2 Enhance clauses lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 7.3 Enhance types-of-sentences-by-purpose lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 7.4 Enhance types-of-sentences-by-structure lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 8. Enhance Verbal Ability — Vocabulary Development (8 lessons)
  - [x] 8.1 Enhance synonyms lesson
    - Add all required enhanced sections
    - Adapt Which Method? to "which synonym fits this specific context?"
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 6.6, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.2 Enhance antonyms lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.3 Enhance context-clues lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.4 Enhance word-formation lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.5 Enhance idioms-and-expressions lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.6 Enhance analogies lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.7 Enhance denotation-and-connotation lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 8.8 Enhance formal-and-informal-language lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 4.1, 5.1, 5.7, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 9. Enhance Analytical Ability — Abstract Reasoning (7 lessons)
  - [x] 9.1 Enhance shape-patterns lesson
    - Add all required enhanced sections (leverage existing SVGs for Req 9)
    - Add Check Your Understanding blocks between pattern type sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 9.8, 10.1, 11.1_

  - [x] 9.2 Enhance figure-series lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 9.3 Enhance number-and-letter-patterns lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 9.4 Enhance odd-one-out lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 9.5 Enhance odd-one-out-problems lesson
    - Add all required enhanced sections (or merge with odd-one-out if duplicate content)
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 9.6 Enhance matrix-reasoning lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 9.7 Enhance spatial-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

- [x] 10. Enhance Analytical Ability — Symbolic Logic (5 lessons)
  - [x] 10.1 Enhance logical-statements lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 10.2 Enhance logical-operators lesson
    - Add all required enhanced sections
    - Add 1 Dual_Coding_Visual (truth table or Venn diagram SVG)
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1_

  - [x] 10.3 Enhance conditional-reasoning lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 10.4 Enhance syllogisms lesson
    - Add all required enhanced sections
    - Add 1 Dual_Coding_Visual (Venn diagram for syllogism validity)
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1_

  - [x] 10.5 Enhance truth-and-validity lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_


- [x] 11. Enhance Analytical Ability — Word Analogy (7 lessons)
  - [x] 11.1 Enhance synonym-and-antonym-analogies lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.2 Enhance part-whole-and-classification-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.3 Enhance function-and-purpose-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.4 Enhance cause-effect-and-progression-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.5 Enhance symbolic-characteristic-and-location-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.6 Enhance language-meaning-and-context-relationships lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

  - [x] 11.7 Enhance numerical-letter-and-abstract-analogies lesson
    - Add all required enhanced sections
    - _Requirements: 1.4, 2.1, 3.1, 3.8, 4.1, 5.1, 5.8, 6.1, 7.1, 8.1, 10.1, 11.1_

- [x] 12. Cross-validate and finalize
  - [x] 12.1 Run full validation
    - Execute `scripts/validate_enhanced_lessons.py` against all enhanced lessons
    - Confirm 100% pass rate on required sections
    - _Requirements: 12.1, 12.2, 12.5_

  - [x] 12.2 Verify Connections bidirectionality
    - Spot-check 10 randomly selected connection pairs for reverse links
    - Verify all referenced subtopic directories exist
    - _Requirements: 8.3, 8.4, 8.5_

  - [x] 12.3 Seed pipeline verification
    - Run `scripts/seed_all_content.py` or `scripts/update_lessons.py`
    - Confirm all enhanced lessons seed without errors
    - Verify parsed JSON output for 5 sample lessons contains new sections
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.6_

  - [x] 12.4 Line count audit
    - Verify no enhanced lesson exceeds 2000 lines
    - Verify no enhanced lesson falls below 800 lines
    - _Requirements: 10.6_


- [ ] 13. Optional: Enhance parser to extract new sections as structured metadata
  - [ ] 13.1 Add retrieval prompt extraction
    - Detect `### Check Your Understanding` sections in `parse_lesson_markdown()`
    - Extract as `retrieval_prompts` field (list of {question, answer} objects)
    - _Requirements: 1.5_

  - [ ] 13.2 Add guided practice extraction
    - Detect `### Guided Practice` sections
    - Extract as `guided_practice` field (list of faded example objects)
    - _Requirements: 1.6_

  - [ ] 13.3 Add discrimination practice extraction
    - Detect `### Which Method?` or `### Discrimination Practice` sections
    - Extract as `discrimination_practice` field
    - _Requirements: 1.7_

  - [ ] 13.4 Add confidence check extraction
    - Detect `### Before You Practice` sections
    - Extract as `confidence_check` field (list of skill strings)
    - _Requirements: 1.9_

  - [ ] 13.5 Add connections extraction
    - Detect `### Connections` sections
    - Extract as `connections` field (list of {topic, description} objects)
    - _Requirements: 1.8_

  - [ ] 13.6 Update metadata flags
    - Add boolean flags to metadata: `has_retrieval_prompts`, `has_guided_practice`, `has_discrimination_practice`, `has_confidence_check`, `has_connections`
    - Ensure backward compatibility for lessons without new sections
    - _Requirements: 10.1, 10.3_

  - [ ] 13.7 Add unit tests for new parser logic
    - Test extraction of each new section type
    - Test backward compatibility with un-enhanced lessons
    - _Requirements: 10.1_

## Task Dependency Graph

```json
{
  "waves": [
    {
      "name": "Wave 1: Tooling",
      "tasks": ["1"],
      "dependsOn": []
    },
    {
      "name": "Wave 2: Content Enhancement (parallel)",
      "tasks": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
      "dependsOn": ["1"]
    },
    {
      "name": "Wave 3: Cross-validation",
      "tasks": ["12"],
      "dependsOn": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    },
    {
      "name": "Wave 4: Optional Parser Enhancement",
      "tasks": ["13"],
      "dependsOn": ["12"]
    }
  ]
}
```

## Notes

- Tasks 2-11 can be executed in parallel since each operates on independent lesson files
- Task 12 (cross-validation) depends on ALL enhancement tasks (2-11) being complete
- Task 13 (parser enhancement) is optional and depends on Task 12 passing
- Each subtask within Tasks 2-11 follows the same pattern: add the 8 required section types, verify parser compatibility
- The "all required enhanced sections" shorthand means: ≥1 Check Your Understanding, ≥3 Elaborative Interrogation, ≥2 Misconception Confrontation, Guided Practice, Which Method?, Before You Practice, Connections, Mastery Checklist (if not already present)
- Lessons that already have Memory Aids, Exam Strategies, or Mastery Checklist sections should preserve them in place — do not duplicate
