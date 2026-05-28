# Prompt: Create a General Information Lesson for the Philippine CSE Reviewer

You are writing a lesson for a Philippine Civil Service Examination (CSE) reviewer app. The lesson must follow the exact structure, formatting, and pedagogical standards below. Every lesson you produce must pass automated validation and be parser-compatible.

---

## Context

- **Exam:** Philippine Civil Service Examination (BOTH Professional and Sub-Professional levels)
- **Module:** General Information
- **Topics covered:** Philippine Constitution, Code of Conduct and Ethical Standards for Public Officials and Employees (RA 6713), Peace and Human Rights Issues and Concepts, Environment Management and Protection
- **Note:** General Information appears on both exam levels with the same scope.
- **Audience:** Filipino adults preparing for the CSE — assume basic civics knowledge from high school
- **Tone:** Professional, authoritative but accessible. Cite specific laws, articles, and sections. Use real Philippine government examples.

### Exam Format (verified from CSC official announcements)

| Level | Items | Time | Passing |
|-------|-------|------|---------|
| Professional | 170 items | 3 hours 10 minutes | 80% |
| Sub-Professional | 165 items | 2 hours 40 minutes | 80% |

**General Information scope (both levels):** Philippine Constitution, RA 6713 (Code of Conduct), Peace and Human Rights Issues and Concepts, Environment Management and Protection

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

Place immediately AFTER a constitutional provision, law, or principle is introduced. Format:

```markdown
> 🤔 **Why does this work?** [2-4 sentences explaining the underlying RATIONALE of the law/provision — why it was enacted, what problem it solves, how it protects public interest. Not just restating what the law says.]
```

**Rules:**
- Explains WHY the provision exists, not WHAT it says
- Connect to real governance problems the law addresses
- Reference the legislative intent or constitutional principle behind the rule
- For ethics: explain why the prohibition prevents specific forms of corruption
- For rights: explain why the right is fundamental and what it protects against

**Examples:**

> 🤔 **Why does this work?** The prohibition on receiving gifts (RA 6713, Sec. 7d) exists because even small gifts create a psychological obligation to reciprocate — the "reciprocity norm." A public official who accepts a gift from a contractor may unconsciously favor that contractor in future decisions, even without explicit quid pro quo. The law removes this risk by prohibiting the gift entirely.

> 🤔 **Why does this work?** The Bill of Rights binds only the STATE (not private individuals) because its purpose is to protect citizens from government overreach. A private company firing an employee for speech is not a constitutional violation — it's a labor dispute. The Constitution specifically limits government power because the state has coercive force (police, courts, prisons) that private actors lack.

> 🤔 **Why does this work?** The three branches of government (executive, legislative, judicial) exist as separate entities with checks and balances because concentrating all power in one body historically leads to tyranny. Each branch can limit the others: the President vetoes laws, Congress controls the budget, and the Supreme Court can declare acts unconstitutional.

### Misconception Confrontation (≥2 per lesson)

```markdown
> ⚠️ **Misconception:** "[Quoted false belief about Philippine law/government]"
>
> **Why it fails:** [Specific provision, case, or example that disproves it]
>
> **Correct model:** [The accurate legal/constitutional understanding]
```

**Examples:**

> ⚠️ **Misconception:** "The President can declare martial law anytime there is a crisis."
>
> **Why it fails:** Article VII, Section 18 of the 1987 Constitution limits martial law to cases of invasion or rebellion AND when public safety requires it. Congress can revoke it, and the Supreme Court can review its factual basis. After the Marcos era, the framers deliberately constrained this power.
>
> **Correct model:** Martial law requires: (1) invasion or rebellion, (2) public safety necessity, (3) 60-day limit unless extended by Congress, (4) subject to Supreme Court review, (5) does not suspend the Constitution or civil courts.

### Check Your Understanding (≥1 block)

```markdown
### Check Your Understanding

**1.** [Question answerable in <10 seconds] → **[Answer]** ([brief rationale citing specific provision])
```

### Guided Practice (faded worked examples)

For General Information, guided practice involves analyzing scenarios:

```markdown
**1.** A government employee receives a ₱5,000 gift basket from a supplier during Christmas. Is this allowed?

- Step 1: Identify the applicable law: _____
- Step 2: Identify the specific section: _____
- Step 3: Apply the rule to the facts: _____
- Step 4: Conclusion: _____

**Answer:** RA 6713, Section 7(d) — Solicitation or acceptance of gifts. The gift exceeds the nominal value threshold and comes from someone with a pending transaction. NOT allowed. The employee must decline or return the gift.
```

### Which Method?

- 4-6 problems mixing different legal provisions, constitutional articles, or ethical scenarios
- Tests whether the learner can identify WHICH law/provision applies before answering

---

## SVG Diagrams

For General Information, SVGs are useful for:

```html
<svg width="400" height="300" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Max 400×300px -->
</svg>
```

**When to use SVGs:**
- Government structure diagrams (three branches, hierarchy)
- Checks and balances flowcharts (who checks whom)
- Bill-to-law process flowcharts
- Rights classification diagrams (political vs. civil vs. social/economic)
- RA 6713 obligations/prohibitions summary charts
- Constitutional amendment vs. revision process diagrams

---

## Content Quality Standards

1. **ACCURACY IS CRITICAL** — cite specific articles, sections, and Republic Act numbers. Verify against the actual text of the 1987 Philippine Constitution and relevant laws.
2. All legal citations must be correct (Article number, Section number, RA number)
3. Use real Philippine government examples: actual agencies (CSC, COA, DILG, DBM), actual positions, actual scenarios
4. Do NOT include outdated information — if a law has been amended, use the current version
5. For constitutional provisions, quote or closely paraphrase the actual text
6. Difficulty progression: recall → application → analysis
7. Line count target: **1,100–1,400 lines** (constitutional provisions need full text + explanation + application scenarios; RA 6713 has many sections requiring detailed coverage)
8. CSE-style format: (a) (b) (c) (d) with bold correct answer

---

## General Information-Specific Notes

### Philippine Constitution Topics
- Preamble and National Territory
- Bill of Rights (Article III) — most heavily tested
- Citizenship (Article IV)
- Suffrage (Article V)
- Legislative Department (Article VI)
- Executive Department (Article VII)
- Judicial Department (Article VIII)
- Constitutional Commissions (Article IX) — CSC, COMELEC, COA
- Accountability of Public Officers (Article XI)
- Social Justice and Human Rights (Article XIII)

### RA 6713 (Code of Conduct) Topics
- Norms of conduct (Section 4)
- Duties of public officials (Section 5)
- System of incentives and rewards (Section 6)
- Prohibited acts and transactions (Section 7)
- Statements and disclosure (Section 8) — SALN
- Penalties (Section 11)

### Peace and Human Rights Topics
- Universal Declaration of Human Rights
- Philippine Commission on Human Rights
- International Humanitarian Law basics
- Rights of indigenous peoples (IPRA)
- Rights of women and children

### Environment Topics
- Philippine Environmental Policy (PD 1151)
- Clean Air Act (RA 8749)
- Ecological Solid Waste Management Act (RA 9003)
- Clean Water Act (RA 9275)
- Environmental Impact Assessment system

---

## Your Task

Create a complete lesson for the subtopic: **[INSERT SUBTOPIC HERE]**

Follow every rule above. Do not skip any required section. VERIFY ALL LEGAL CITATIONS — accuracy of constitutional and statutory references is non-negotiable for this module.
