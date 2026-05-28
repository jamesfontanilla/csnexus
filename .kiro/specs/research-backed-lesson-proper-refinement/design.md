# Design: Research-Backed Lesson Proper Refinement

## Purpose

The existing evidence-based enhancement work checks whether lessons contain required sections. This refinement adds a stricter quality layer: the sections must be instructional, topic-specific, and sequenced according to learning-science principles.

The design has two parts:

1. A content transformation pattern for lesson authors or scripts.
2. A validation layer that catches missing evidence patterns, placeholders, and domain-mismatched text.

## Research-To-Implementation Map

| Research Basis | Design Rule | Lesson Proper Implementation |
| --- | --- | --- |
| Roediger & Karpicke retrieval practice | Learners must recall, not just reread | Insert short recall prompts after major rules |
| Dunlosky et al. effective learning techniques | Use practice testing, distributed recall, elaborative interrogation | Add "Check Your Understanding" and "Why does this work?" near content sections |
| Renkl/Atkinson faded examples | Move gradually from example study to independent problem solving | Guided Practice uses full -> partial -> independent items |
| Rohrer interleaving | Practice should include method selection | "Which Method?" mixes similar trap types |
| Refutation text literature | Misconceptions need explicit correction | Misconception -> why it fails -> correct model |
| Explicit grammar instruction | Rules should be stated clearly and contrasted | Grammar lessons include explicit rule, contrastive examples, and targeted feedback |
| Dual coding / multimedia learning | Visual decision aids support rule selection | Add compact flowcharts or diagrams where useful |

## Lesson Proper Architecture

Each refined lesson should organize the instructional core around this loop:

```text
Rule explanation
Worked example
Retrieval prompt
Misconception refutation
Faded practice
Interleaved discrimination
Confidence check
Transfer connection
```

This loop can appear once for short lessons or repeat across major subrules in longer lessons.

## Subject-Verb Agreement Reference Model

For SVA, the lesson should use the following rule clusters:

1. Basic singular/plural agreement
2. Intervening phrases and clauses
3. Compound subjects with `and`
4. Compound subjects with `or/nor`
5. Indefinite pronouns
6. Collective nouns
7. Inverted sentences
8. `the number of` vs `a number of`
9. Relative pronouns and antecedents
10. Fractions, percentages, titles, and amounts

Each cluster should have:

- One concise rule statement
- One correct example
- One trap example
- One retrieval prompt
- One brief rationale

## Section Templates

### Retrieval Prompt

```markdown
### Check Your Understanding

1. In the sentence below, what is the true subject?
2. Is the subject singular or plural?
3. Which verb agrees with that subject, and why?
```

### Elaborative Callout

```markdown
> **Why does this work?** The verb agrees with the head subject because modifiers describe the subject but do not change its number.
```

### Misconception Refutation

```markdown
> **Misconception:** "The noun closest to the verb controls agreement."
>
> **Why it fails:** The closest noun may be inside a prepositional phrase and may not be the subject.
>
> **Correct model:** Strip modifiers first, then match the verb to the head subject.
```

### Faded Worked Example

```markdown
### Guided Practice

**Problem:** The list of approved applicants (is/are) posted.

- Step 1: True subject = _____
- Step 2: Subject number = _____
- Step 3: Correct verb = _____
- Step 4: Why? _____
```

### Interleaved Discrimination

```markdown
### Which Method?

For each item, name the rule first: basic agreement, intervening phrase, proximity rule, indefinite pronoun, collective noun, inverted sentence, or fraction/percentage.
```

## Validator Design

Create `scripts/validate_lesson_proper_quality.py`.

The validator should:

1. Discover `lesson.md` files under `data/seed/lessons`.
2. Optionally accept `--lesson path/to/lesson.md`.
3. Parse each lesson with `parse_lesson_markdown()`.
4. Check structural evidence patterns:
   - At least two "Why does this work?" callouts
   - At least two misconception blocks
   - At least one faded example cue in `Guided Practice`
   - At least six items in `Which Method?`
   - `Before You Practice`, `Connections`, and `Mastery Checklist`
5. Check quality artifacts:
   - `[Brief rationale]`
   - `TODO`
   - `??`
   - "set up the equation" in grammar lessons
   - "computed answer" in grammar lessons
   - "ratio", "inverse", or "part-whole" in grammar lessons unless context allows it
6. Check line count:
   - Minimum 800 lines
   - Maximum 2000 lines
7. Print a pass/fail report.

## Execution Strategy

Implementation should proceed in small waves:

1. Tooling first: validator and SVA-specific audit.
2. Reference lesson: polish subject-verb agreement until it passes.
3. Grammar lessons: apply the same pattern to remaining grammar lessons.
4. Verbal lessons: adapt pattern to reading, vocabulary, and sentence structure.
5. Numerical and analytical lessons: apply with domain-specific wording and mixed-method practice.
6. Final validation and seed pipeline run.

## Non-Goals

- This spec does not require changing database models.
- This spec does not require frontend changes.
- This spec does not require new H2 markdown sections beyond parser-supported structure.
- This spec does not replace the existing evidence-based enhancement spec; it tightens quality and sequencing.

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Lessons pass structure but contain generic filler | Add domain-fit artifact checks |
| Lessons become too long | Enforce 2000-line cap |
| Lesson proper becomes repetitive | Use rule clusters and mixed practice instead of repeated boilerplate |
| Grammar lessons receive math phrasing | Add grammar-specific banned phrase checks |
| Automated expansion lowers content quality | Require reference lesson review before batch rollout |
