# Prompt: Create a Verbal Ability Lesson for the Philippine CSE Reviewer

You are writing a lesson for a Philippine Civil Service Examination (CSE) reviewer app. The lesson must follow the exact structure, formatting, and pedagogical standards below. Every lesson you produce must pass automated validation and be parser-compatible.

---

## Context

- **Exam:** Philippine Civil Service Examination (Professional and Sub-Professional levels)
- **Module:** Verbal Ability (in English and Filipino)
- **Topics covered:** Grammar and Correct Usage (error recognition, sentence structure), Vocabulary (word meaning, sentence completion), Paragraph Organization, Reading Comprehension
- **Note:** Verbal Ability appears on BOTH Professional and Sub-Professional levels
- **Audience:** Filipino adults preparing for the CSE — assume intermediate English proficiency
- **Tone:** Professional, clear, encouraging but not condescending. Use Philippine government/civil service context in all examples.

### Exam Format (verified from CSC official announcements)

| Level | Items | Time | Passing |
|-------|-------|------|---------|
| Professional | 170 items | 3 hours 10 minutes | 80% |
| Sub-Professional | 165 items | 2 hours 40 minutes | 80% |

**Professional-level subtests:** General Information, Numerical Ability, Analytical Ability, Verbal Ability
**Sub-Professional subtests:** General Information, Numerical Ability, Clerical Ability, Verbal Ability

Sources: [CSC official exam advisory](https://csc.gov.ph), [TeachPinas CSE Coverage 2026](https://www.teachpinas.com/civil-service-exam-schedule-requirements-coverage), [Board Exams PH](https://boardexams.ph)

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

Place immediately AFTER a rule or procedure is introduced. Format:

```markdown
> 🤔 **Why does this work?** [2-4 sentences explaining the underlying LINGUISTIC principle — not restating the rule. Must be accurate, specific to the topic, and readable in under 15 seconds.]
```

**Rules:**
- Explains WHY the rule works, not WHAT the rule is
- For grammar: explain syntactic/morphological/phonological reasoning
- For reading comprehension: explain text structure or inference logic
- For vocabulary: explain semantic relationships or morphological patterns
- Distribute across content sections (not clustered together)

### Misconception Confrontation (≥2 per lesson)

Place near the content where the error is most likely. Format:

```markdown
> ⚠️ **Misconception:** "[Quoted false belief that examinees commonly hold]"
>
> **Why it fails:** [Concrete counterexample using a specific sentence or scenario — not abstract]
>
> **Correct model:** [The accurate understanding, stated clearly]
```

**Rules:**
- Derive from the "Common Mistakes" section
- Counterexample must use a real sentence (not "sometimes X happens")
- Three-part structure is mandatory

### Check Your Understanding (≥1 block per lesson)

Insert after every 2-3 content subsections. Format:

```markdown
### Check Your Understanding

**1.** [Question answerable in <10 seconds] → **[Answer]** ([brief rationale])
**2.** [Question] → **[Answer]** ([rationale])
**3.** [Question] → **[Answer]** ([rationale])
```

**Rules:**
- 2-4 questions per block
- Immediate recall only — no multi-step analysis
- Covers ONLY the preceding 2-3 subsections

### Guided Practice (faded worked examples)

```markdown
### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** "[Sentence with blank or error]"

- Step 1: Identify the grammar rule/pattern: _____
- Step 2: Apply the rule: _____
- Step 3: Select the correct form: _____

**Answer:** [Complete solution with explanation]
```

**Rules:**
- 3-5 problems with progressive fading (first gives more structure, last gives less)
- For verbal: steps involve identification, classification, or rule application
- Blanks use `_____` notation

### Which Method? (interleaved discrimination)

```markdown
### Which Method?

For each problem, identify the rule type and solve.

**1.** [Sentence]
- **Type:** [Grammar rule / Reading strategy / Vocabulary technique]
- **Answer:** [Correct answer]
- **Why:** [One-line rationale]
```

**Rules:**
- 4-6 problems mixing different sub-skills from the lesson
- Problems are NOT grouped by type — deliberately mixed
- Each answer includes type identification + answer + rationale

### Before You Practice (confidence check)

```markdown
### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] [Concrete ability statement matching actual lesson content]
- [ ] [Another concrete ability statement]
```

**Rules:**
- 4-6 items phrased as verb + specific skill
- Must correspond to actual content sections taught in THIS lesson
- NOT generic ("understand grammar") — specific ("Apply the proximity rule for either/or constructions")

### Connections (transfer bridges)

```markdown
### Connections

How this topic connects to other areas of the CSE:

- **[Topic Name]:** [1-sentence explanation of the structural link]
```

**Rules:**
- 3-5 connections
- Link to related grammar, vocabulary, comprehension, and sentence structure topics
- Each connection explains HOW the current skill transfers

---

## SVG Diagrams

For concepts that benefit from visual representation (decision flowcharts, sentence diagrams, tense timelines), include inline SVG:

```html
<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Max 400×300px, accessible colors, text labels on all elements -->
</svg>
```

**When to use SVGs in Verbal Ability:**
- Decision flowcharts (e.g., "Which conjunction type?" → check relationship → select)
- Tense timelines showing past/present/future with markers
- Sentence structure diagrams (subject-predicate trees)
- Pronoun case decision trees

---

## Content Quality Standards

1. All examples use Philippine government, civil service, and professional context
2. All questions are factually correct with unambiguous answers
3. Difficulty progression: Easy → Medium → Hard within practice sections
4. CSE-style multiple choice format: (a) (b) (c) (d) with bold correct answer
5. Line count target: **1,100–1,400 lines** (based on existing high-quality verbal lessons; grammar rules have many exceptions and examples, reading comp needs full passages, vocabulary needs word lists + context sentences)
6. No H2 sections other than Explanations, Worked Examples, Key Takeaways, Summary
7. Elaborative Interrogation explains principles, not procedures
8. Misconception counterexamples use concrete sentences, not abstract descriptions

---

## Example EI Callouts for Verbal Ability

**Grammar (Subject-Verb Agreement):**
> 🤔 **Why does this work?** Subject-verb agreement is determined by the grammatical number of the head noun in the subject phrase — not by meaning, proximity, or sound. English marks number on both nouns (-s = plural) and verbs (-s = singular), creating a cross-reference system.

**Reading Comprehension:**
> 🤔 **Why does this work?** Authors signal their purpose through word choice: persuasive writing uses loaded language and rhetorical questions; informative writing uses neutral, precise vocabulary. Tone is encoded in connotation — the same event described as "a bold initiative" vs. "a reckless gamble" reveals opposite attitudes.

**Vocabulary:**
> 🤔 **Why does this work?** Context clues work because writers anticipate that readers may not know every word, so they embed meaning signals nearby — definitions, examples, synonyms, contrasts, or logical inferences. The surrounding text constrains what the unknown word CAN mean.

---

## Your Task

Create a complete lesson for the subtopic: **[INSERT SUBTOPIC HERE]**

Follow every rule above. Do not skip any required section. Ensure all EI callouts explain genuine linguistic principles with 100% accuracy.
