# Prompt: Create a Clerical Ability Lesson for the Philippine CSE Reviewer

You are writing a lesson for a Philippine Civil Service Examination (CSE) reviewer app. The lesson must follow the exact structure, formatting, and pedagogical standards below. Every lesson you produce must pass automated validation and be parser-compatible.

---

## Context

- **Exam:** Philippine Civil Service Examination (Sub-Professional level ONLY — not on Professional)
- **Module:** Clerical Ability
- **Topics covered:** Filing/Clerical Operations/Alphabetizing, Spelling
- **Note:** The official CSC scope lists only Filing and Spelling. However, review materials commonly expand this to include coding/decoding and clerical checking as these test similar skills.
- **Audience:** Filipino adults preparing for the CSE — assume basic office skills familiarity
- **Tone:** Professional, precise, detail-oriented. Emphasize accuracy and speed since clerical tasks are timed.

### Exam Format (verified from CSC official announcements)

| Level | Items | Time | Passing |
|-------|-------|------|---------|
| Sub-Professional | 165 items | 2 hours 40 minutes | 80% |

**Clerical Ability scope (Sub-Professional only):** Filing/Clerical Operations/Alphabetizing, Spelling

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

Place immediately AFTER a rule or procedure is introduced. Format:

```markdown
> 🤔 **Why does this work?** [2-4 sentences explaining the underlying principle — why this clerical procedure produces accurate results, why this filing rule prevents errors, why this checking method catches discrepancies.]
```

**Rules:**
- Explains WHY the method works, not just HOW to do it
- For spelling: explain morphological patterns, etymology, or phonetic rules
- For filing: explain why alphabetical/numerical ordering systems prevent retrieval errors
- For coding: explain why systematic encoding/decoding prevents information loss
- For checking: explain why comparison strategies catch specific error types

**Examples:**

> 🤔 **Why does this work?** Alphabetical filing works because it imposes a single, universally agreed ordering on names — eliminating the ambiguity of filing by date, department, or subject. When everyone follows the same letter-by-letter comparison rule, any clerk can locate any file without knowing when it was created or what it contains.

> 🤔 **Why does this work?** Clerical checking catches transposition errors (switching two adjacent digits, like 1234 → 1243) because the human eye naturally reads groups of characters as chunks. By comparing character-by-character from left to right, you override the brain's tendency to "see" what it expects and force attention to each individual position.

### Misconception Confrontation (≥2 per lesson)

```markdown
> ⚠️ **Misconception:** "[Quoted false belief]"
>
> **Why it fails:** [Concrete counterexample]
>
> **Correct model:** [Accurate understanding]
```

### Check Your Understanding (≥1 block)

```markdown
### Check Your Understanding

**1.** [Question answerable in <10 seconds] → **[Answer]** ([brief rationale])
```

### Guided Practice, Which Method?, Before You Practice, Connections

Same format as other modules — see structure above.

---

## SVG Diagrams

For clerical ability, SVGs are useful for:

```html
<svg width="400" height="200" viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Max 400×300px -->
</svg>
```

**When to use SVGs in Clerical Ability:**
- Filing order flowcharts (decision tree: "Are first letters the same? → Compare second letters...")
- Coding/decoding key tables with visual mapping
- Error-spotting exercises showing two columns side-by-side with differences highlighted
- Alphabetization decision diagrams

---

## Content Quality Standards

1. All examples use Philippine government context: government forms (CS Form 212, SALN), agency names (CSC, DILG, DBM, COA), Filipino surnames (Santos, Reyes, Cruz, Dela Cruz, Garcia)
2. All spelling words are commonly tested on the CSE and genuinely tricky (accommodate, bureaucracy, liaison, personnel, supersede)
3. Filing examples use realistic Filipino name formats (surname-first, particles like "de," "dela," "delos")
4. Coding exercises use realistic government document codes
5. Accuracy is paramount — every answer must be verifiably correct
6. Speed tips are included since clerical sections are heavily time-pressured
7. Line count target: **900–1,100 lines** (clerical topics are more procedural and less conceptually deep; filing rules and spelling lists are compact but need many practice items)

---

## Clerical Ability-Specific Notes

### Spelling Topics
- Commonly misspelled words in government correspondence
- Words with silent letters, double letters, -ible/-able, -ence/-ance
- Philippine English spelling conventions vs. American English

### Filing/Alphabetizing Topics
- Letter-by-letter vs. word-by-word alphabetizing
- Filing rules for surnames with particles (Mc, Mac, De, Dela, Van, St.)
- Filing rules for numbers, abbreviations, and government agencies
- Cross-referencing and indexing

### Coding/Decoding Topics
- Letter-number substitution codes
- Position-based codes (A=1, B=2... or shifted alphabets)
- Symbol substitution systems
- Government document numbering systems

### Clerical Checking Topics
- Comparing names, numbers, and codes for exact matches
- Identifying transposition errors, omission errors, substitution errors
- Speed-accuracy tradeoff strategies

---

## Your Task

Create a complete lesson for the subtopic: **[INSERT SUBTOPIC HERE]**

Follow every rule above. Do not skip any required section. Ensure all answers are 100% correct — clerical ability demands perfect accuracy.
