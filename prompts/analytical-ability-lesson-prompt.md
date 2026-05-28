# Prompt: Create an Analytical Ability Lesson for the Philippine CSE Reviewer

You are writing a lesson for a Philippine Civil Service Examination (CSE) reviewer app. The lesson must follow the exact structure, formatting, and pedagogical standards below. Every lesson you produce must pass automated validation and be parser-compatible.

---

## Context

- **Exam:** Philippine Civil Service Examination (Professional and Sub-Professional levels)
- **Module:** Analytical Ability
- **Topics covered:** Word Association (single-word and paired-analogy approach), Identifying Assumptions and Conclusions, Logic (syllogisms, conditional reasoning, truth/validity), Data Interpretation (tables, graphs, charts)
- **Note:** Analytical Ability appears ONLY on the Professional-level exam (not Sub-Professional)
- **Audience:** Filipino adults preparing for the CSE — assume no prior formal logic training
- **Tone:** Professional, systematic, visual where possible. Build from concrete examples to abstract principles.

### Exam Format (verified from CSC official announcements)

| Level | Items | Time | Passing |
|-------|-------|------|---------|
| Professional | 170 items | 3 hours 10 minutes | 80% |

**Analytical Ability scope (Professional only):** Word Association (single-word and paired-analogy), Identifying Assumptions and Conclusions, Logic, Data Interpretation

Sources: [CSC official exam advisory](https://csc.gov.ph), [TeachPinas CSE Coverage 2026](https://www.teachpinas.com/civil-service-exam-schedule-requirements-coverage)

---

## Lesson Structure (Canonical Section Order)

Every lesson is a single markdown file. It MUST contain these H2 sections in this exact order:

```
## Explanations        ← All teaching content lives here as H3 subsections
## Worked Examples     ← 3-5 fully solved problems with step-by-step solutions
## Key Takeaways       ← Bullet list of 5-10 essential points
## Summary             ← 2-3 paragraph summary of the entire lesson
```

Within `## Explanations`, use this H3 ordering:

1. `### Introduction` — 2-3 paragraphs: what the topic is, why it matters, relevance to CSE
2. `### Why [Topic] Is Tested in the CSE` — bullet list of reasons for government employees
3. `### Common Mistakes Examinees Make` — numbered list of 5-8 common errors
4. `### Learning Objectives` — bullet list with action verbs
5. Content sections (`### 4.1 [Title]`, `### 4.2 [Title]`, etc.) — the actual teaching
6. `### Exam Strategies` — test-taking tips specific to this topic
7. `### Memory Aids` — mnemonics, acronyms, shortcuts
8. `### Guided Practice` — 3-5 faded worked examples
9. `### Which Method?` — 4-6 mixed-type discrimination problems
10. `### Before You Practice` — confidence self-assessment (4-6 checkbox items)
11. `### Mini Practice Set` — 15-20 full practice problems with answers
12. `### Connections` — 3-5 transfer bridges to other CSE topics
13. `### Mastery Checklist` — ✅ checklist of skills mastered

---

## Pedagogical Elements (REQUIRED — minimum counts)

### Elaborative Interrogation (≥3 per lesson)

Place immediately AFTER a rule, pattern, or logical principle is introduced. Format:

```markdown
> 🤔 **Why does this work?** [2-4 sentences explaining the underlying LOGICAL principle — not restating the procedure. Must be accurate and readable in under 15 seconds.]
```

**Rules:**
- Explains WHY the reasoning method works, not WHAT to do
- For abstract reasoning: explain why transformations are deterministic, why constraint intersection eliminates wrong answers
- For symbolic logic: explain truth-preservation, validity as structure-independence, why certain inference forms are reliable
- For word analogy: explain why precise predicate naming eliminates distractors, why relationship direction matters
- Distribute across content sections

**Examples:**

> 🤔 **Why does this work?** Figure series exploit the fact that visual transformations are constrained — a shape can only change in a finite number of ways (rotate, resize, recolor, move, add/remove elements). By systematically checking each transformation dimension, you reduce an open-ended question to a closed set of hypotheses.

> 🤔 **Why does this work?** A conditional P → Q is asymmetric because it only constrains what happens when P is true — it makes no claim about situations where P is false. This one-directional flow is why contrapositive (¬Q → ¬P) is valid but converse (Q → P) is not.

> 🤔 **Why does this work?** The bridge sentence method forces you to articulate the exact predicate connecting two words. Vague predicates match too many choices; specific predicates match only one. Only the correct answer satisfies the identical predicate.

### Misconception Confrontation (≥2 per lesson)

```markdown
> ⚠️ **Misconception:** "[Quoted false belief]"
>
> **Why it fails:** [Concrete counterexample — specific figure, specific argument, specific analogy pair]
>
> **Correct model:** [The accurate understanding]
```

### Check Your Understanding (≥1 block)

```markdown
### Check Your Understanding

**1.** [Question answerable in <10 seconds] → **[Answer]** ([brief rationale])
```

### Guided Practice (faded worked examples)

```markdown
**1.** [Problem description or figure reference]

- Step 1: Identify the pattern type: _____
- Step 2: State the rule: _____
- Step 3: Apply to predict the answer: _____

**Answer:** [Complete solution]
```

**Rules for Analytical Ability:**
- For abstract reasoning: steps involve pattern identification (rotation angle, element count, shading progression)
- For symbolic logic: steps involve premise identification, rule application, conclusion derivation
- For word analogy: steps involve relationship naming, bridge sentence formation, answer testing

### Which Method?

- 4-6 problems mixing different sub-skills
- For abstract reasoning: mix rotation, reflection, counting, shading problems
- For logic: mix modus ponens, modus tollens, invalid forms
- For analogy: mix synonym, part-whole, function, cause-effect relationships

---

## SVG Diagrams (CRITICAL for Analytical Ability)

Analytical ability lessons REQUIRE SVG diagrams more than any other module. Use inline SVG for:

```html
<svg width="360" height="120" viewBox="0 0 360 120" xmlns="http://www.w3.org/2000/svg">
  <!-- Max 400×300px, accessible colors, text labels -->
</svg>
```

**When to use SVGs:**
- **Figure series:** Show 3-4 figures in sequence with a "?" for the answer
- **Shape patterns:** Illustrate rotation, reflection, scaling transformations
- **Matrix reasoning:** Show 3×3 grids with the missing cell marked "?"
- **Odd-one-out:** Show 4-5 figures with labels A-E
- **Spatial relationships:** Show reference figures and answer choices
- **Venn diagrams:** For syllogism validity
- **Truth tables:** For logical operators (can be markdown tables instead)
- **Flowcharts:** For decision processes (which analogy type? which inference form?)

**SVG Design Rules:**
- Use distinct colors: `#2196F3` (blue), `#4CAF50` (green), `#E91E63` (pink), `#FF9800` (orange), `#9C27B0` (purple)
- Include text labels (`<text>` elements) for all meaningful components
- Use `stroke-width="2"` for main shapes, `stroke-width="1"` for grid lines
- Dashed lines for "missing" or "unknown" elements: `stroke-dasharray="3,2"`
- Number figures with small labels below: `<text x="40" y="95" font-size="10">1</text>`

---

## Content Quality Standards

1. All examples are logically valid and unambiguous — verify every answer
2. For logic: ensure all "valid" arguments are genuinely valid and all "invalid" ones are genuinely invalid
3. For patterns: ensure the rule you describe actually produces the shown sequence
4. For analogies: ensure the relationship type is correctly identified and the answer is the only one that fits
5. Difficulty progression: Easy → Medium → Hard
6. Line count target: **1,000–1,200 lines** (SVG diagrams add lines but explanations are more concise than verbal/numerical; logic and analogy lessons need many example pairs but not verbose prose)
7. Use Philippine context where natural (government office scenarios for logic, Filipino cultural references for analogies)

---

## Your Task

Create a complete lesson for the subtopic: **[INSERT SUBTOPIC HERE]**

Follow every rule above. Do not skip any required section. Ensure all logical reasoning is 100% valid, all patterns are deterministic, and all analogy relationships are correctly typed.
