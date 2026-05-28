# Prompt: Create a Numerical Ability Lesson for the Philippine CSE Reviewer

You are writing a lesson for a Philippine Civil Service Examination (CSE) reviewer app. The lesson must follow the exact structure, formatting, and pedagogical standards below. Every lesson you produce must pass automated validation and be parser-compatible.

---

## Context

- **Exam:** Philippine Civil Service Examination (Professional and Sub-Professional levels)
- **Module:** Numerical Ability
- **Topics covered:** Basic Operations (integers, fractions, decimals), Word Problems (age, work, distance, mixture), Number Series and Sequence, Percentages, Ratio/Proportion/Average
- **Note:** Professional level includes Number Series; Sub-Professional covers Basic Operations and Word Problems only
- **Audience:** Filipino adults preparing for the CSE — assume high school math proficiency
- **Tone:** Professional, clear, step-by-step. Use Philippine government/civil service context (₱ currency, government salaries, budget allocations, VAT, PhilHealth/Pag-IBIG deductions).

### Exam Format (verified from CSC official announcements)

| Level | Items | Time | Passing |
|-------|-------|------|---------|
| Professional | 170 items | 3 hours 10 minutes | 80% |
| Sub-Professional | 165 items | 2 hours 40 minutes | 80% |

**Professional Numerical scope:** Basic Operations, Word Problems, Number Series and Sequence
**Sub-Professional Numerical scope:** Basic Operations, Word Problems

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

Place immediately AFTER a formula, rule, or procedure is introduced. Format:

```markdown
> 🤔 **Why does this work?** [2-4 sentences explaining the underlying MATHEMATICAL principle — not restating the procedure. Must be accurate and readable in under 15 seconds.]
```

**Rules:**
- Explains WHY the math works, not HOW to do it
- Reference mathematical properties: distributive, commutative, associative, inverse operations, identity elements
- Concrete reasoning: "Dividing both sides by the same number preserves equality because..."
- Distribute across content sections (not clustered together)

**Examples:**

> 🤔 **Why does this work?** The equation P = R × W is simply the definition of "percentage" restated algebraically. "25% of 80" means "25 per hundred of 80," which is (25/100) × 80. Since division and multiplication are inverse operations, you can isolate any one variable by rearranging.

> 🤔 **Why does this work?** Cross-multiplication works because if a/b = c/d, then multiplying both sides by bd gives ad = bc. This transforms a proportion into a simple equation with one unknown.

> 🤔 **Why does this work?** Successive percentage changes compound multiplicatively because each change creates a new base. 0.80 × 0.90 = 0.72, meaning you keep 72% — a 28% total reduction, not 30%.

### Misconception Confrontation (≥2 per lesson)

Place near the content where the error is most likely. Format:

```markdown
> ⚠️ **Misconception:** "[Quoted false belief]"
>
> **Why it fails:** [Concrete counterexample with specific numbers showing the error]
>
> **Correct model:** [The accurate understanding]
```

**Rules:**
- Counterexample MUST use specific numbers (e.g., "6 ÷ 0.5 = 12, not smaller")
- Derive from the "Common Mistakes" section
- Three-part structure is mandatory

### Check Your Understanding (≥1 block per lesson)

Insert after every 2-3 content subsections. Format:

```markdown
### Check Your Understanding

**1.** [Question answerable in <10 seconds] → **[Answer]** ([brief rationale])
**2.** [Question] → **[Answer]** ([rationale])
**3.** [Question] → **[Answer]** ([rationale])
```

### Guided Practice (faded worked examples)

```markdown
### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** Compute [problem]

- Step 1: [Given step]
- Step 2: _____ [operation] _____ = _____
- Step 3: _____

**Answer:** [Complete solution]
```

**Rules:**
- 3-5 problems with progressive fading
- First problem provides more completed steps, last provides fewer
- Blanks use `_____` notation
- Steps involve computation (not identification)

### Which Method? (interleaved discrimination)

```markdown
**1.** [Problem]
- **Type:** [Problem type/method]
- **Answer:** [Numerical answer]
- **Why:** [One-line rationale for why this method applies]
```

**Rules:**
- 4-6 problems mixing different sub-skills
- Deliberately NOT grouped by type
- Tests whether the learner can identify the correct approach before solving

### Before You Practice

- 4-6 items as concrete ability statements
- Must match actual content sections (not generic)

### Connections

- 3-5 links to other numerical topics and word-problem applications
- Format: `- **[Topic]:** [How this skill transfers]`

---

## SVG Diagrams

For concepts that benefit from visual representation, include inline SVG:

```html
<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Max 400×300px, accessible colors, text labels -->
</svg>
```

**When to use SVGs in Numerical Ability:**
- Number lines showing operations (addition/subtraction of signed numbers)
- Percentage bar diagrams (original → increase/decrease → new value)
- Ratio/proportion visual comparisons
- Place value charts
- Fraction models (area models, number lines)
- Inverse operation relationship diagrams (multiplication ↔ division)

---

## Content Quality Standards

1. All examples use Philippine context: ₱ currency, government salaries (₱25,000-₱80,000 range), VAT (12%), PhilHealth, Pag-IBIG, SSS/GSIS deductions, barangay/municipal budgets
2. All computations are verified correct — double-check every answer
3. Difficulty progression: Easy → Medium → Hard
4. CSE-style format: (a) (b) (c) (d) with bold correct answer
5. Line count target: **1,000–1,300 lines** (based on existing high-quality numerical lessons; formulas + worked examples + verification steps need room but shouldn't pad)
6. Include verification steps ("Check: 15% of 25,000 = 3,750 ✓")
7. Mental math shortcuts where applicable (10% = move decimal, 25% = ÷4)

---

## Your Task

Create a complete lesson for the subtopic: **[INSERT SUBTOPIC HERE]**

Follow every rule above. Do not skip any required section. Ensure all computations are 100% correct and all EI callouts explain genuine mathematical principles.
