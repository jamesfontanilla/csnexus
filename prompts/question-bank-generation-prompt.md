# Prompt: Generate Question Banks for Clerical Ability — Alphabetical Filing

Generate a question bank in JSON format for the specified subtopic. Each bank must contain exactly **600 questions**: 200 Easy, 200 Medium, 200 Hard.

---

## JSON Format (one question object)

```json
{
  "id": 1,
  "subtest": "Clerical Ability",
  "module": "Alphabetical Filing",
  "subtopic": "[SUBTOPIC NAME]",
  "difficulty": "Easy|Medium|Hard",
  "question": "[Question text]",
  "choices": ["A", "B", "C", "D"],
  "answer": "[Correct choice — must exactly match one of the choices]",
  "explanation": "[1-2 sentence explanation of why the answer is correct]",
  "tags": ["tag1", "tag2"],
  "category": ["Sub-Professional"],
  "language": "English"
}
```

The output must be a valid JSON array: `[ {...}, {...}, ... ]`

---

## Difficulty Definitions

### Easy (200 questions)
- 2-3 entries to arrange
- Single rule application (one comparison type)
- Obvious differences (first letter/digit differs)
- No format conversion needed
- No tiebreakers

### Medium (200 questions)
- 3-4 entries to arrange
- May require 2 comparison steps (e.g., same prefix, compare numbers)
- Differences appear at 2nd or 3rd position
- May involve one format conversion
- May require identifying the rule type

### Hard (200 questions)
- 4-5 entries to arrange
- Multiple rules in one question (mixed entry types)
- Subtle differences (similar-looking entries)
- Format conversion required
- Tiebreakers needed (time, document number)
- Traps designed to catch common errors

---

## Question Types (mix these across all difficulties)

### Type 1: "Which comes first?"
```json
{
  "question": "Which of the following should be filed FIRST?",
  "choices": ["Entry A", "Entry B", "Entry C", "Entry D"]
}
```

### Type 2: "Which comes last?"
```json
{
  "question": "Which of the following should be filed LAST?",
  "choices": ["Entry A", "Entry B", "Entry C", "Entry D"]
}
```

### Type 3: "What is the correct order?"
```json
{
  "question": "Arrange the following in correct filing order: [entries]. Which sequence is correct?",
  "choices": ["A, B, C", "B, A, C", "C, A, B", "A, C, B"]
}
```

### Type 4: "Which position?"
```json
{
  "question": "In what position would [entry] be filed among the following?",
  "choices": ["1st", "2nd", "3rd", "4th"]
}
```

### Type 5: "Which rule applies?"
```json
{
  "question": "What filing rule should be applied to arrange [entry]?",
  "choices": ["Rule A", "Rule B", "Rule C", "Rule D"]
}
```

---

## Subtopic-Specific Rules

### Business and Office Filing
- Company names: file as written, first word = primary unit
- "The" at beginning: move to end
- Numbers: spell out (7-Eleven → Seven-Eleven)
- Acronyms: file letter by letter as written (CSC under C-S-C)
- Government offices: distinctive word first (Dept. of Education → Education, Dept. of)
- Tags to use: company-name, numeric-name, acronym, government-office, the-rule, mixed-filing

### Numerical Filing
- Account numbers: digit-by-digit comparison, shorter-first rule
- Code numbers: prefix alphabetically, then numeric portion as WHOLE NUMBER (not string)
- Ascending (default) vs descending order
- Hyphenated codes: segment-by-segment (prefix-year-sequence)
- Mixed alphanumeric: letters before numbers
- Tags to use: account-number, code-number, ascending, descending, hyphenated-code, mixed-alphanumeric

### Chronological Filing
- Date hierarchy: Year → Month → Day
- Months compared by number (Jan=1...Dec=12), NOT alphabetically
- Philippine format: MM/DD/YYYY
- Ascending (oldest first, default) vs descending (newest first)
- Time tiebreaker: AM before PM, earlier hour first
- Document number tiebreaker when dates/times match
- Tags to use: date-comparison, month-order, year-priority, ascending, descending, time-tiebreaker, format-conversion, mixed-format

---

## Philippine Government Context

Use these real entities in questions:
- Agencies: CSC, COA, DILG, DBM, DENR, DOH, DepEd, DOLE, DPWH, DOT, DOJ, DSWD, NBI, PNP, BIR, BSP
- Organizations: PhilHealth, Pag-IBIG, SSS, GSIS, TESDA, PAGASA
- Companies: Globe Telecom, PLDT, Manila Water, Jollibee, San Miguel Corporation, Ayala Corporation, SM Investments, BDO, Metrobank
- Budget codes: PS-101, MOOE-205, CO-301
- Document codes: DTN-2024-0001, CSC-NCR-001, COA-R3-045
- Dates: Use 2023-2025 range, Philippine holidays, SALN deadlines (April 30), fiscal year (Jan-Dec)

---

## Critical Rules for Accuracy

1. **Every answer must be verifiably correct.** Double-check all comparisons.
2. **Distractors must be plausible** — they should represent common errors (e.g., filing "The Manila Hotel" under T instead of M).
3. **No duplicate questions.** Each question must test a unique combination.
4. **Explanations must cite the specific rule** that determines the answer.
5. **IDs must be sequential** (1 through 600).
6. **Difficulty distribution:** IDs 1-200 = Easy, 201-400 = Medium, 401-600 = Hard.

---

## Output Instructions

Generate the complete JSON array. Start with `[` and end with `]`. No markdown code fences — just raw JSON.

**Subtopic to generate:** [INSERT: "Business and Office Filing" OR "Numerical Filing" OR "Chronological Filing"]

Generate all 600 questions now.
