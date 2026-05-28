# Requirements: Research-Backed Lesson Proper Refinement

## Overview

This spec refines lesson propers so their instructional sequence is grounded in learning-science evidence, not just section presence. It applies across `data/seed/lessons/**/lesson.md`, with subject-verb agreement as the reference implementation pattern.

The refinement is based on:

- Retrieval practice and test-enhanced learning: Roediger & Karpicke (2006), https://pubmed.ncbi.nlm.nih.gov/16507066/
- Effective learning techniques: Dunlosky et al. (2013), https://gwern.net/doc/psychology/spaced-repetition/2013-dunlosky.pdf
- Faded worked examples: Renkl, Atkinson, & Grosse (2004), https://link.springer.com/article/10.1023/B%3ATRUC.0000021815.74806.f6
- Interleaved practice: IES project summary for Rohrer/Dedrick/Hartwig/Cheung work, https://ies.ed.gov/use-work/awards/efficacy-study-interleaved-mathematics-practice
- Refutation text for misconceptions: Zengilowski et al. (2021) and Tippett lineage, https://pmc.ncbi.nlm.nih.gov/articles/PMC8784251/
- Explicit grammar instruction and SVA processing: Springer article on subject-verb agreement instruction, https://link.springer.com/article/10.1007/s10674-005-0331-0

## Definitions

- **Lesson Proper**: The instructional content under `## Explanations`, including rule explanations, examples, retrieval prompts, misconception blocks, guided practice, and transfer links.
- **Evidence Pattern**: A reusable instructional move grounded in research: retrieval prompt, elaborative why-question, misconception refutation, faded example, interleaved discrimination, confidence calibration, transfer bridge, or visual decision aid.
- **Domain-Fit Content**: Lesson content whose wording, examples, and practice items match the lesson topic. For example, grammar lessons must not contain generic math wording such as "set up the equation" unless the grammar topic truly requires it.
- **Faded Example**: A worked example sequence that gradually removes scaffolding: fully solved example -> partially completed example -> independent item.
- **Interleaved Discrimination**: A mixed practice section where learners must first identify which rule or method applies before solving.

## Requirement 1: Evidence-Based Lesson Proper Sequence

**User Story:** As a learner, I want each lesson proper to teach the concept in a research-backed order, so that I learn the rule, retrieve it, distinguish traps, and apply it independently.

### Acceptance Criteria

1. WHEN a lesson is refined, THE lesson proper SHALL follow this instructional pattern at least once: rule explanation -> worked example -> retrieval check -> misconception refutation -> faded practice -> mixed discrimination.
2. WHEN a lesson contains multiple major rules, EACH major rule SHALL include either a retrieval prompt or an elaborative "why does this work?" prompt near the rule.
3. WHEN the lesson has a `### Guided Practice` section, THE section SHALL include at least one faded item with blanks for learner completion.
4. WHEN the lesson has a `### Which Method?` section, THE section SHALL require learners to identify the relevant rule/method before answering.
5. THE lesson SHALL preserve parser compatibility with `parse_lesson_markdown()`.

## Requirement 2: Retrieval Practice

**User Story:** As a learner, I want frequent low-stakes recall prompts, so that I retain the rule beyond rereading.

### Acceptance Criteria

1. EACH refined lesson SHALL contain at least two retrieval prompts in the lesson proper.
2. Retrieval prompts SHALL ask learners to recall or identify a concept without immediately giving the answer in the question text.
3. For grammar lessons, retrieval prompts SHALL ask for subject, verb, rule, antecedent, clause type, or sentence function as appropriate.
4. For math lessons, retrieval prompts SHALL ask for operation, formula choice, relationship type, or setup.
5. For reasoning lessons, retrieval prompts SHALL ask for pattern, rule, transformation, assumption, or relation type.

## Requirement 3: Elaborative Interrogation

**User Story:** As a learner, I want "why" prompts tied to the rule, so that I understand the principle instead of memorizing a surface procedure.

### Acceptance Criteria

1. EACH refined lesson SHALL contain at least two domain-fit "Why does this work?" callouts.
2. A "Why does this work?" callout SHALL explain the underlying rule, relation, or cognitive cue in topic-specific language.
3. A grammar lesson SHALL NOT use arithmetic wording such as "computed answer", "equation", "ratio", or "formula" in elaborative callouts unless the grammar topic explicitly involves quantities.
4. A math lesson SHALL NOT use grammar-only wording such as "antecedent", "clause", or "modifier" unless the lesson explicitly discusses word-problem language.
5. A reasoning lesson SHALL explain why a pattern rule or logic relation remains consistent across examples.

## Requirement 4: Misconception Refutation

**User Story:** As a learner, I want common traps named and corrected, so that I can avoid attractive wrong answers on the CSE.

### Acceptance Criteria

1. EACH refined lesson SHALL contain at least two misconception blocks.
2. EACH misconception block SHALL include three parts: misconception, why it fails, correct model.
3. Misconceptions SHALL be domain-fit and specific to the lesson.
4. Generic fallback lines such as "A memorized shortcut always works" SHALL NOT appear unless rewritten with topic-specific detail.
5. The validator SHALL flag placeholder or generic misconception language.

## Requirement 5: Faded Worked Examples

**User Story:** As a learner, I want examples that gradually remove help, so that I can move from understanding to independent solving.

### Acceptance Criteria

1. EACH refined lesson SHALL contain at least one fully solved worked example.
2. EACH refined lesson SHALL contain at least one partially completed faded example.
3. EACH faded example SHALL remove meaningful steps, not just hide the final answer.
4. FOR subject-verb agreement, faded steps SHALL include true subject, subject number, rule, and verb choice.
5. FOR numerical lessons, faded steps SHALL include setup, operation/formula, computation, and reasonableness check.

## Requirement 6: Interleaved Discrimination Practice

**User Story:** As a learner, I want mixed items that force me to select the rule first, so that I do not simply repeat the last rule I studied.

### Acceptance Criteria

1. EACH refined lesson SHALL contain a `### Which Method?` or equivalent discrimination section.
2. The section SHALL include at least six mixed items.
3. Each item SHALL require naming the method/rule before solving.
4. For SVA, the mixed items SHALL include basic agreement, intervening phrases, compound subjects, proximity rule, indefinite pronouns, inverted sentences, collective nouns, and fractions/percentages where applicable.
5. The section SHALL include brief answer rationales.

## Requirement 7: Metacognitive Calibration

**User Story:** As a learner, I want a confidence check before practice, so that I can choose what to review instead of mistaking familiarity for mastery.

### Acceptance Criteria

1. EACH refined lesson SHALL contain a `### Before You Practice` section.
2. The confidence check SHALL list concrete skills, not vague confidence statements.
3. The confidence check SHALL use domain-fit wording.
4. The confidence check SHALL avoid placeholders such as `[Brief rationale]`.
5. Learners SHALL be prompted to revisit the relevant lesson section when confidence is low.

## Requirement 8: Dual Coding And Visual Decision Aids

**User Story:** As a learner, I want compact diagrams for rule selection, so that I can see how decisions branch.

### Acceptance Criteria

1. High-trap lessons SHALL include at least one visual decision aid.
2. Subject-verb agreement SHALL include a decision flow: find true subject -> strip modifiers -> check special construction -> choose verb.
3. Visual aids SHALL be parser-safe markdown or SVG under existing lesson sections.
4. Visual aids SHALL not replace textual explanation.
5. Visual aids SHALL be small enough to avoid bloating lessons beyond 2000 lines.

## Requirement 9: Domain-Fit Quality Gate

**User Story:** As a content maintainer, I want automated checks for artifacts, so that generic generated text does not slip into polished lessons.

### Acceptance Criteria

1. THE validation tooling SHALL flag placeholder text including `[Brief rationale]`, `TODO`, `_____` in answer-only contexts, and corrupted `??` markers.
2. THE validation tooling SHALL flag domain-mismatched phrases in lesson propers.
3. THE validation tooling SHALL report line-count violations below 800 or above 2000.
4. THE validation tooling SHALL parse each lesson with `parse_lesson_markdown()`.
5. THE validation tooling SHALL print per-file failures and an aggregate pass/fail summary.

## Requirement 10: Subject-Verb Agreement Reference Lesson

**User Story:** As a maintainer, I want one polished reference lesson, so that future refinements have a concrete model.

### Acceptance Criteria

1. `data/seed/lessons/verbal-ability/grammar/subject-verb-agreement/lesson.md` SHALL be refined first.
2. The SVA lesson SHALL contain no generic math artifacts such as "set up the equation" or "computed answer".
3. The SVA lesson SHALL contain no placeholder markers such as `[Brief rationale]` or `??`.
4. The SVA lesson SHALL be between 800 and 2000 lines.
5. The SVA lesson SHALL pass structural validation and domain-fit quality validation.

## Requirement 11: Full Corpus Coverage

**User Story:** As a content maintainer, I want every lesson proper covered by the same research-backed refinement process, so that quality is consistent across the whole CSE reviewer curriculum.

### Acceptance Criteria

1. THE refinement scope SHALL include every `lesson.md` file under `data/seed/lessons/`.
2. THE spec SHALL include an explicit lesson manifest listing all lesson propers to refine.
3. EACH lesson in the manifest SHALL be individually validated with `scripts/validate_lesson_proper_quality.py --lesson <path>`.
4. THE final corpus run SHALL validate all lessons with `scripts/validate_lesson_proper_quality.py`.
5. NO lesson proper SHALL be considered complete until it passes both the structural validator and the lesson proper quality validator.
