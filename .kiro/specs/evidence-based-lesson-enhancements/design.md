# Design Document: Evidence-Based Lesson Enhancements

## Overview

This design specifies how to enhance all ~60 existing lesson files with research-backed pedagogical elements while maintaining full backward compatibility with the existing parser and seed pipeline. The approach is additive — no existing content is removed or restructured, only new sections are inserted at defined positions.

## Research Foundation

Each enhancement maps to a specific finding from cognitive psychology:

| Enhancement | Research Basis | Key Finding |
|---|---|---|
| Distributed Retrieval Prompts | Roediger & Karpicke (2006); Weinstein et al. (2022) | Retrieval practice distributed throughout learning produces 30-50% better retention than massed practice at the end |
| Elaborative Interrogation | Dunlosky et al. (2013); Chi et al. (1989) | Asking "why?" doubles transfer performance by forcing schema construction |
| Misconception Confrontation | Tippett (2010); Kendeou et al. (2014) | Refutation texts produce significantly better conceptual change than standard exposition |
| Faded Worked Examples | Renkl et al. (2002); Atkinson et al. (2003) | Gradually removing solution steps produces better transfer than all-worked or all-practice |
| Interleaved Discrimination | Rohrer et al. (2015) | Mixing problem types lifts delayed test scores (61% vs 38% in controlled trials) |
| Metacognitive Calibration | Bjork & Bjork (2020); Kornell & Bjork (2007) | Confidence rating before practice improves self-assessment accuracy and directs effort |
| Dual Coding Visuals | Mayer (2021); Paivio (1986) | Combining verbal + visual representations strengthens memory traces vs either alone |
| Transfer Bridges | Gick & Holyoak (1983); Barnett & Ceci (2002) | Explicit structural analogies between domains enhance transfer of learning |

## Architecture

This feature is purely a content enhancement — no new backend services, APIs, or database schema changes are required. The architecture consists of:

1. **Content Layer** — Enhanced markdown lesson files in `data/seed/lessons/`
2. **Parsing Layer** — Existing `scripts/parse_lesson.py` (no changes required for core functionality; optional Task 13 adds metadata extraction)
3. **Validation Layer** — New `scripts/validate_enhanced_lessons.py` for structural compliance checking
4. **Seed Layer** — Existing `scripts/seed_all_content.py` and `scripts/update_lessons.py` (no changes required)

```
data/seed/lessons/***/lesson.md  →  parse_lesson_markdown()  →  LessonContent JSON  →  DB
                                          ↑
scripts/validate_enhanced_lessons.py  (checks structural compliance)
```

## Components and Interfaces

### Component: Enhanced Lesson File (Content)

Each `lesson.md` file is the primary deliverable. It interfaces with:
- **Parser** (`scripts/parse_lesson.py`) — consumed as input, produces JSON
- **Seed scripts** — load parsed JSON into the `lessons.content_json` column
- **Frontend** — renders the `sections` array with typed content blocks

### Component: Validation Script

`scripts/validate_enhanced_lessons.py` is a standalone CLI tool that:
- Input: filesystem path to `data/seed/lessons/`
- Output: structured report (stdout) with pass/fail per lesson
- Dependencies: `scripts/parse_lesson.py` (imports `parse_lesson_markdown`)

### Interface: Parser Block Type Mapping

New content elements map to existing parser block types:

| Lesson Element | Parser Block Type | Frontend Component |
|---|---|---|
| `> 🤔 **Why...**` | `tip` | TipCard (existing) |
| `> ⚠️ **Misconception...**` | `warning` | WarningCard (existing) |
| Check Your Understanding questions | `prose` / `list` | ProseBlock / ListBlock (existing) |
| Guided Practice blanks | `prose` / `step_by_step` | StepByStepBlock (existing) |
| SVG diagrams | `svg` | SvgBlock (existing) |

## Data Models

No new database models are introduced. The existing `Lesson.content_json` column (JSON type) stores the output of `parse_lesson_markdown()`. The enhanced lessons produce a richer JSON payload but within the same schema:

```python
# Existing LessonContent schema (unchanged)
class LessonContent(BaseModel):
    explanations: list[LessonExplanation]      # H3 sections → more entries after enhancement
    worked_examples: list[LessonWorkedExample]  # Unchanged
    key_takeaways: list[str]                    # Unchanged
    summary: str                                # Unchanged
```

The enhanced parser output (existing `metadata`, `sections`, `practice_problems` fields) will contain more entries but no structural changes.

### Optional Data Model Extension (Task 13)

If Task 13 is implemented, the parser output gains additional fields:

```python
# New optional fields in parse_lesson_markdown() output
{
    "retrieval_prompts": [{"question": str, "answer": str}],
    "guided_practice": [{"number": int, "problem": str, "steps": list, "answer": str}],
    "discrimination_practice": [{"number": int, "problem": str, "type": str, "answer": str}],
    "confidence_check": [str],
    "connections": [{"topic": str, "description": str}],
    "metadata": {
        ...existing fields...,
        "has_retrieval_prompts": bool,
        "has_guided_practice": bool,
        "has_discrimination_practice": bool,
        "has_confidence_check": bool,
        "has_connections": bool,
    }
}
```

## Enhanced Lesson Template

### Section Ordering

All lessons will follow this canonical section ordering within the `## Explanations` H2 block:

```markdown
# [Lesson Title]

## Explanations

### Introduction
[Existing content — what the topic is, why it matters]

### Why [Topic] Is Tested in the CSE
[Existing content — relevance to government work]

### Common Mistakes Examinees Make
[Existing content — numbered list of errors]

### Learning Objectives
[Existing content — measurable objectives]

---

### [Content Section 4.1]
[Existing content]

> 🤔 **Why does this work?** [Elaborative interrogation — placed after key rules]

> ⚠️ **Misconception:** "[False belief]"
> **Why it fails:** [Counterexample]
> **Correct model:** [Accurate understanding]

### [Content Section 4.2]
[Existing content]

### [Content Section 4.3]
[Existing content]

### Check Your Understanding
[2-4 quick recall questions covering sections 4.1-4.3]

### [Content Section 4.4]
[Existing content]

### [Content Section 4.5]
[Existing content]

### [Content Section 4.6]
[Existing content]

### Check Your Understanding
[2-4 quick recall questions covering sections 4.4-4.6]

### [Remaining content sections...]

---

### Exam Strategies
[Existing content — test-taking tips]

### Memory Aids
[Existing content — mnemonics and shortcuts]

---

### Guided Practice
[3-5 faded worked examples with progressive step removal]

### Which Method?
[4-6 mixed-type problems requiring method identification]

### Before You Practice
[Confidence self-assessment checklist]

### Mini Practice Set
[Existing content — 15-20 full practice problems]

---

### Connections
[3-5 explicit links to other curriculum topics]

### Mastery Checklist
[Existing content — ✅ items]
```

### Placement Rules

| New Section | Position | Rationale |
|---|---|---|
| Check Your Understanding | After every 2-3 content subsections | Distributed retrieval prevents forgetting during long lessons |
| Elaborative Interrogation (`> 🤔`) | Inline, immediately after rules/formulas | Prompts schema construction at the moment of encoding |
| Misconception Confrontation (`> ⚠️`) | Inline, near content where the error is likely | Refutation is most effective when the misconception is active |
| Guided Practice | After Exam Strategies, before Which Method? | Bridges reading → partial solving → full solving |
| Which Method? | After Guided Practice, before Confidence Check | Develops discrimination before independent practice |
| Before You Practice | Immediately before Mini Practice Set | Calibration is most useful right before self-testing |
| Connections | After Mini Practice Set, before Mastery Checklist | Transfer links are best processed after the topic is consolidated |

## Content Block Formats

### Check Your Understanding Format

```markdown
### Check Your Understanding

**1.** What sign does -48 ÷ 6 produce? → **Negative** (different signs → negative result)
**2.** Is 0 ÷ 7 defined? → **Yes, it equals 0** (zero divided by any non-zero number = 0)
**3.** What is the reciprocal of 5/8? → **8/5** (flip numerator and denominator)
```

Rules:
- 2-4 questions per block
- Single-line format: question → bold answer (brief rationale)
- Tests recall of the immediately preceding 2-3 sections
- No multi-step computation — instant recall only

### Elaborative Interrogation Format

```markdown
> 🤔 **Why does this work?** When you move the decimal point the same number
> of places in both the dividend and divisor, you are multiplying both by the
> same power of 10. Since (a × k) ÷ (b × k) = a ÷ b for any non-zero k,
> the quotient is unchanged. You're exploiting the identity property of division.
```

Rules:
- Blockquote with 🤔 emoji prefix
- 2-4 sentences explaining the *principle*, not restating the *procedure*
- Placed immediately after the rule/formula it explains
- Must be accurate and non-trivial

### Misconception Confrontation Format

```markdown
> ⚠️ **Misconception:** "Dividing always makes numbers smaller."
>
> **Why it fails:** 6 ÷ 0.5 = 12. Dividing by a number less than 1 produces
> a result LARGER than the original. You're asking "how many halves fit in 6?"
>
> **Correct model:** Division makes numbers smaller only when the divisor is
> greater than 1. When the divisor is between 0 and 1, division makes numbers larger.
```

Rules:
- Blockquote with ⚠️ emoji prefix
- Three-part structure: misconception → counterexample → correct model
- Concrete numbers/examples in the counterexample (not abstract)
- Derived from the "Common Mistakes" section content

### Faded Worked Example Format

```markdown
### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** Compute 5.6 ÷ 0.08

- Step 1: Move decimal _____ places right in both → _____ ÷ _____
- Step 2: Divide: _____ ÷ _____ = _____

**Answer:** Move 2 places → 560 ÷ 8 = 70

**2.** Compute 3/4 ÷ 5/8

- Step 1: Keep _____, Change to _____, Flip to _____
- Step 2: Multiply: _____ × _____ = _____
- Step 3: Simplify: _____ = _____

**Answer:** Keep 3/4, Change ÷ to ×, Flip 5/8 to 8/5 → 3/4 × 8/5 = 24/20 = 6/5

**3.** Compute -144 ÷ (-9)

- Step 1: Determine sign: _____ signs → _____ result
- Step 2: Divide absolute values: _____ ÷ _____ = _____
- Step 3: Apply sign: _____

**Answer:** Same signs → positive. 144 ÷ 9 = 16. Result: +16
```

Rules:
- 3-5 problems per section
- Progressive fading: first problem has more given steps, last has fewer
- Blanks use `_____` notation
- Complete answer follows each problem
- Difficulty increases through the section

### Interleaved Discrimination Format

```markdown
### Which Method?

For each problem, identify the type and solve.

**1.** -72 ÷ 8
- **Type:** Integer division (different signs)
- **Answer:** -9
- **Why:** Negative ÷ positive → negative. 72 ÷ 8 = 9.

**2.** 4.5 ÷ 0.09
- **Type:** Decimal division (divisor is decimal)
- **Answer:** 50
- **Why:** Move decimal 2 places: 450 ÷ 9 = 50.

**3.** 7/12 ÷ 2/3
- **Type:** Fraction division (KCF method)
- **Answer:** 7/8
- **Why:** 7/12 × 3/2 = 21/24 = 7/8.

**4.** 3,024 ÷ 6
- **Type:** Whole number long division (watch for zero placeholder)
- **Answer:** 504
- **Why:** 6 goes into 30 five times, 02 zero times (placeholder!), 24 four times.
```

Rules:
- 4-6 problems mixing all sub-skills from the lesson
- Each answer includes: Type identification, numerical answer, brief rationale
- Problems are NOT grouped by type — they are deliberately mixed
- For single-method lessons, problems test "applies vs. does not apply"

### Confidence Check Format

```markdown
### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Divide multi-digit whole numbers using long division
- [ ] Apply sign rules for integer division correctly
- [ ] Move decimal points correctly when dividing by a decimal
- [ ] Use Keep-Change-Flip for fraction and mixed number division
- [ ] Solve division word problems in Philippine government context
- [ ] Estimate division results to verify answers quickly
```

Rules:
- 4-6 items matching the lesson's actual content sections
- Phrased as concrete ability statements (verb + specific skill)
- Includes the instruction about focusing on low-confidence areas
- Checkbox format for visual clarity

### Transfer Bridge Format

```markdown
### Connections

How this topic connects to other areas of the CSE:

- **Percentages:** Finding "what percent is X of Y" requires dividing X by Y — decimal division is the core operation
- **Ratios:** Simplifying ratios like 24:36 requires dividing both terms by their GCF
- **Averages:** Computing the mean (sum ÷ count) is a division problem in every case
- **Proportion Word Problems:** Cross-multiplication produces a division step to isolate the unknown
- **Fractions (Basic Operations):** Converting fractions to decimals requires dividing numerator by denominator
```

Rules:
- 3-5 connections per lesson
- Each references an actual subtopic in the curriculum
- Format: `**[Topic Name]:** [1-sentence explanation of the structural link]`
- Connections should be genuinely useful, not forced

## Parser Compatibility Analysis

The existing `parse_lesson_markdown()` in `scripts/parse_lesson.py` handles the new sections as follows:

| New Element | Parser Behavior | Compatibility |
|---|---|---|
| `### Check Your Understanding` | Parsed as a regular H3 section under Explanations | ✅ Compatible |
| `> 🤔 **Why...**` blockquote | Detected as `BLOCK_TYPE_TIP` (💡/tip keyword in blockquote) | ✅ Compatible |
| `> ⚠️ **Misconception...**` blockquote | Detected as `BLOCK_TYPE_WARNING` (⚠️ in blockquote) | ✅ Compatible |
| `### Guided Practice` | Parsed as regular H3 section | ✅ Compatible |
| `### Which Method?` | Parsed as regular H3 section | ✅ Compatible |
| `### Before You Practice` | Parsed as regular H3 section | ✅ Compatible |
| `### Connections` | Parsed as regular H3 section | ✅ Compatible |
| `### Mini Practice Set` | Detected by `"mini practice" in lower_title` | ✅ Already handled |
| `### Mastery Checklist` | Detected by `"mastery checklist" in lower_title` | ✅ Already handled |
| `### Memory Aids` | Detected by `"memory aid" in lower_title` | ✅ Already handled |
| `### Exam Strategies` | Detected by `"exam strateg" in lower_title` | ✅ Already handled |
| Inline SVG | Detected by `<svg` regex pattern | ✅ Already handled |

**Conclusion:** No parser modifications are required. All new sections are either already recognized as special sections or will be parsed as standard content sections.

## Validation Script Design

### Location

`scripts/validate_enhanced_lessons.py`

### Algorithm

```
1. Discover all lesson.md files under data/seed/lessons/
2. For each lesson file:
   a. Read the markdown content
   b. Check for required sections (regex-based heading detection):
      - At least 1 "### Check Your Understanding"
      - At least 1 "> 🤔" blockquote
      - At least 2 "> ⚠️" blockquotes
      - "### Guided Practice" heading
      - "### Which Method?" or "### Discrimination Practice" heading
      - "### Before You Practice" heading
      - "### Connections" heading
      - "### Mastery Checklist" or mastery-related heading
   c. Run parse_lesson_markdown() and verify output has:
      - Non-empty explanations list
      - Non-empty worked_examples list
      - Non-empty key_takeaways list
      - Non-empty summary string
   d. Record pass/fail with details
3. Print summary report
```

### Output Format

```
=== Enhanced Lesson Validation Report ===

Total lessons: 60
Passing: 58
Failing: 2

FAILURES:
  data/seed/lessons/numerical-ability/basic-operations/estimation-and-mental-math/lesson.md
    ✗ Missing: Guided Practice
    ✗ Missing: Which Method?

  data/seed/lessons/verbal-ability/grammar/articles/lesson.md
    ✗ Missing: Misconception Confrontation (found 1, need ≥2)
    ✗ Parser error: empty key_takeaways

SECTION COVERAGE:
  Check Your Understanding:    60/60 (100%)
  Elaborative Interrogation:   60/60 (100%)
  Misconception Confrontation: 58/60 (97%)
  Guided Practice:             58/60 (97%)
  Which Method?:               58/60 (97%)
  Before You Practice:         60/60 (100%)
  Connections:                 60/60 (100%)
  Mastery Checklist:           60/60 (100%)
```

## Lesson Inventory and Grouping Strategy

### Module Breakdown

| Module | Topics | Subtopics (Lessons) |
|---|---|---|
| Numerical Ability | Basic Operations, Percentages, Ratio/Proportion/Average | 10 + 8 + 10 = 28 |
| Verbal Ability | Grammar, Reading Comprehension, Sentence Structure, Vocabulary Development | 10 + 5 + 4 + 8 = 27 |
| Analytical Ability | Abstract Reasoning, Symbolic Logic, Word Analogy | 7 + 5 + 7 = 19 |
| **Total** | | **~74 lessons** |

### Enhancement Batching

Lessons will be enhanced in batches by topic to maintain consistency within related content:

| Batch | Lessons | Priority |
|---|---|---|
| 1 | Numerical: Basic Operations (10) | High — most lessons, establishes template |
| 2 | Numerical: Percentages (8) | High — heavily tested on CSE |
| 3 | Numerical: Ratio/Proportion/Average (10) | High |
| 4 | Verbal: Grammar (10) | Medium |
| 5 | Verbal: Reading Comprehension (5) | Medium |
| 6 | Verbal: Sentence Structure (4) | Medium |
| 7 | Verbal: Vocabulary Development (8) | Medium |
| 8 | Analytical: Abstract Reasoning (7) | Medium — already has SVGs |
| 9 | Analytical: Symbolic Logic (5) | Lower |
| 10 | Analytical: Word Analogy (7) | Lower |

## Module-Specific Adaptation Notes

### Numerical Ability Lessons

- **Dual coding:** Concept relationship diagrams (e.g., inverse operations), number line visuals, place-value charts
- **Interleaving:** Mix whole number / integer / decimal / fraction variants of the same operation
- **Misconceptions:** Focus on sign errors, decimal placement, order-of-operations violations
- **Transfer bridges:** Heavy cross-linking between operations (addition↔subtraction, multiplication↔division) and to percentages/ratios

### Verbal Ability Lessons

- **Dual coding:** Decision flowcharts (e.g., "Which conjunction type?" → check relationship → select), sentence structure diagrams
- **Interleaving:** Mix rule-application vs. error-identification problems
- **Misconceptions:** Focus on commonly confused words, false friends, overgeneralized rules
- **Transfer bridges:** Link grammar rules to reading comprehension (recognizing structures in passages) and to vocabulary (word choice precision)

### Analytical Ability Lessons

- **Dual coding:** Already present (SVG diagrams) — verify coverage, add where missing
- **Interleaving:** Mix rotation/reflection/transformation identification
- **Misconceptions:** Focus on rotation vs. reflection confusion, pattern complexity overestimation
- **Transfer bridges:** Link abstract patterns to numerical sequences and to verbal analogy structures

## Risk Mitigation

| Risk | Mitigation |
|---|---|
| Enhanced lessons exceed 2000 lines | Monitor line count; trim verbose existing content if needed |
| New sections break parser | Validation script catches parser failures before deployment |
| Quality inconsistency across 74 lessons | Use the template strictly; validate with the script |
| Connections reference non-existent topics | Validation script cross-checks referenced topics against directory structure |
| SVG diagrams render poorly | Keep SVGs simple (max 400×300), test in frontend |

## Error Handling

- **Parser failure on enhanced lesson:** The validation script reports the specific file and error. The lesson is fixed before seeding.
- **Missing section in enhanced lesson:** The validation script reports which sections are missing. Enhancement is incomplete until all required sections pass.
- **Line count violation:** The validation script reports lessons exceeding 2000 lines or below 800 lines. Content is trimmed or expanded accordingly.
- **Broken connection reference:** The validation script checks that referenced subtopic directories exist. Broken links are fixed before the cross-validation task passes.

## Correctness Properties

### Property 1: Parser output completeness

For any enhanced Lesson_File L, `parse_lesson_markdown(L)` produces output where `len(output["explanations"]) >= 6` AND `len(output["worked_examples"]) >= 1` AND `len(output["key_takeaways"]) >= 3` AND `len(output["summary"]) > 20`.

**Validates: Requirements 10.1, 10.2, 10.4**

### Property 2: Section presence invariant

For any enhanced Lesson_File L, the markdown text contains at least 1 occurrence of `### Check Your Understanding`, at least 1 occurrence of `> 🤔`, at least 2 occurrences of `> ⚠️ **Misconception`, exactly 1 occurrence of `### Guided Practice`, exactly 1 occurrence of `### Which Method?`, exactly 1 occurrence of `### Before You Practice`, and exactly 1 occurrence of `### Connections`.

**Validates: Requirements 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1**

### Property 3: Line count bounds

For any enhanced Lesson_File L, `800 <= line_count(L) <= 2000`.

**Validates: Requirement 10.6**

### Property 4: Connection validity

For any connection entry in a `### Connections` section that references a topic name T, there exists a directory under `data/seed/lessons/` whose slug or title matches T.

**Validates: Requirements 8.3, 8.4**

## Testing Strategy

### Validation Script Tests

The validation script itself is tested by:
1. Running against un-enhanced lessons (baseline) — should report all sections missing
2. Running against a single manually-enhanced lesson — should pass
3. Running against a lesson with intentionally missing sections — should report specific failures

### Parser Compatibility Tests

Each enhanced lesson is verified by:
1. Calling `parse_lesson_markdown()` and asserting no exceptions
2. Asserting `len(output["explanations"]) >= 1`
3. Asserting `len(output["worked_examples"]) >= 1`
4. Asserting `len(output["key_takeaways"]) >= 1`
5. Asserting `len(output["summary"]) > 0`

### Seed Pipeline Tests

After all enhancements:
1. Run `scripts/update_lessons.py` — no errors
2. Spot-check 5 lessons in the database — `content_json` contains expected section count
3. Verify frontend renders enhanced lessons without layout breaks (manual check)

### Content Quality Checks (Manual)

For each batch (Tasks 2-11):
- Verify Elaborative Interrogation callouts explain principles, not procedures
- Verify Misconception Confrontation blocks use concrete counterexamples
- Verify Guided Practice fading is progressive (more help → less help)
- Verify Which Method? problems are genuinely mixed (not grouped by type)
- Verify Connections reference real cross-topic relationships
