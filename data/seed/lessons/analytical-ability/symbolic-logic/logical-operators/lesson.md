# Logical Operators

## Introduction

**Logical Operators** are the connective symbols that join, modify, and relate propositions in symbolic logic. They are the grammar of formal reasoning — just as conjunctions and punctuation give structure to English sentences, logical operators give structure to logical arguments. In the Philippine Civil Service Examination (CSE), logical operator questions test your ability to interpret compound statements, evaluate truth conditions, and determine whether complex expressions are true or false.

This subtopic covers the following critical areas:
- **AND (Conjunction, ∧)** — both conditions must hold
- **OR (Disjunction, ∨)** — at least one condition must hold
- **NOT (Negation, ¬)** — reversing a truth value
- **IF-THEN (Conditional, →)** — directional implication
- **IF AND ONLY IF (Biconditional, ↔)** — two-way equivalence
- **Truth Tables** — systematic evaluation of all possible truth combinations
- **Compound Statements** — multi-operator expressions and their evaluation

Understanding logical operators is non-negotiable for civil service work. Government employees evaluate eligibility rules ("applicant must be Filipino AND at least 18 years old"), policy alternatives ("submit online OR in person"), conditional regulations ("if absent without leave, then salary is deducted"), and equivalence definitions ("an employee is regular if and only if they have completed probation"). Every administrative decision rests on correctly interpreting these logical structures.

### Why Logical Operators Are Tested in the CSE

The Civil Service Examination tests logical operators because:

- Administrative rules use AND/OR logic constantly — misreading "or" as "and" (or vice versa) changes eligibility outcomes
- Government regulations contain conditional statements that must be interpreted precisely
- Policy documents define terms using biconditional ("if and only if") language that establishes exact boundaries
- Negation appears in exclusion clauses, exceptions, and prohibitions — misinterpreting "not" leads to enforcement errors
- Compound conditions in memoranda require systematic evaluation, not intuition
- Both Professional and Sub-Professional levels include symbolic logic items testing operator comprehension
- Logical precision separates competent administrators from those who make costly interpretation errors

### Common Mistakes Examinees Make

1. **Confusing AND with OR** — believing that "A or B" requires both to be true (it requires only one)
2. **Misunderstanding inclusive OR** — not realizing that "A or B" in logic allows both to be true simultaneously
3. **Double-negation errors** — getting confused when negating an already-negative statement
4. **Reversing conditionals** — treating "If P then Q" as equivalent to "If Q then P"
5. **Confusing conditional with biconditional** — assuming "if P then Q" means "P if and only if Q"
6. **Ignoring operator precedence** — evaluating operators in the wrong order in compound statements
7. **Evaluating incomplete truth conditions** — not considering all possible combinations of truth values
8. **Relying on everyday language intuition** — formal logic operators have precise definitions that differ from casual speech

## Learning Objectives

After this lesson, you should be able to:

- Define each logical operator (∧, ∨, ¬, →, ↔) and state its truth conditions precisely
- Identify conjunctions, disjunctions, negations, conditionals, and biconditionals in natural language
- Interpret compound logical statements containing multiple operators
- Construct and analyze truth tables for any combination of operators
- Distinguish valid from invalid logical expressions using systematic evaluation
- Evaluate symbolic logic statements by applying operator precedence rules
- Recognize logically equivalent expressions (e.g., P → Q ≡ ¬P ∨ Q)
- Solve CSE-style logical operator questions efficiently under time pressure
- Eliminate incorrect answer choices by testing truth conditions strategically

---

## 4.1 What Are Logical Operators?

A **logical operator** (also called a **logical connective**) is a symbol that connects or modifies propositions to form compound statements. Operators define the relationship between the truth values of component propositions and the truth value of the resulting compound statement.

### Propositions and Truth Values

Before understanding operators, recall that a **proposition** is a declarative statement that is either true (T) or false (F):
- P = "The employee submitted the report." (either true or false)
- Q = "The deadline has passed." (either true or false)

Logical operators take one or more propositions and produce a new proposition whose truth value depends on the truth values of the inputs and the specific operator used.

### The Five Core Operators

| Operator | Symbol | Name | Type | English Equivalent |
|----------|--------|------|------|-------------------|
| AND | ∧ | Conjunction | Binary (two inputs) | "both...and..." |
| OR | ∨ | Disjunction | Binary (two inputs) | "either...or..." |
| NOT | ¬ | Negation | Unary (one input) | "it is not the case that..." |
| IF-THEN | → | Conditional | Binary (two inputs) | "if...then..." |
| IF AND ONLY IF | ↔ | Biconditional | Binary (two inputs) | "...if and only if..." |

### How Operators Differ from Everyday Language

In casual speech, "or" often means "one or the other but not both" (exclusive or). In formal logic, "or" (∨) means "at least one, possibly both" (inclusive or). This distinction trips up many examinees.

Similarly, "if...then..." in everyday speech often implies causation. In formal logic, → only describes a truth-value relationship — it says nothing about cause and effect.

**Workplace example:**
- "Employees may submit forms online OR at the office." — In logic, this means submitting at both is also acceptable (inclusive OR).
- "The employee is punctual AND hardworking." — Both conditions must be true for the compound statement to be true.
- "NOT all reports are complete." — At least one report is incomplete.

---

## 4.2 Conjunction (AND — ∧)

The **conjunction** operator combines two propositions and produces a compound statement that is true **only when both** component propositions are true.

### Symbol and Structure

- Symbol: **∧**
- Read as: "P and Q"
- Written: P ∧ Q
- True when: Both P is true AND Q is true
- False when: Either P is false, Q is false, or both are false

### Truth Table for Conjunction

| P | Q | P ∧ Q |
|---|---|-------|
| T | T | **T** |
| T | F | **F** |
| F | T | **F** |
| F | F | **F** |

**Key insight:** Conjunction is the strictest binary operator — it requires ALL conditions to hold. One false component kills the entire statement.

> 🤔 **Why does this work?** Each logical operator is defined entirely by its truth table — a fixed mapping from input truth values to output truth value. This means you never need to interpret meaning or context; you only need to know the inputs' truth values and look up the result. Conjunction requires both inputs true because it models the concept of "simultaneous satisfaction" — like a checklist where every box must be ticked. This mechanical, context-free evaluation is what makes formal logic reliable: the same inputs always produce the same output regardless of what the propositions are about.

### Easy Examples

- P = "Maria is punctual." Q = "Maria is hardworking."
  - P ∧ Q = "Maria is punctual AND hardworking."
  - True only if Maria is BOTH punctual AND hardworking.

- P = "The report is complete." Q = "The report is accurate."
  - P ∧ Q = "The report is complete AND accurate."
  - If the report is complete but inaccurate, P ∧ Q is FALSE.

### Medium Examples

- P = "The applicant has a bachelor's degree." Q = "The applicant has 3 years of experience."
  - P ∧ Q = "The applicant has a bachelor's degree AND 3 years of experience."
  - An applicant with a degree but only 2 years of experience makes P ∧ Q false.

- P = "The budget was approved." Q = "The director signed the memo." R = "The project is funded."
  - (P ∧ Q) → R = "If the budget was approved AND the director signed, then the project is funded."

### Advanced Examples

- "An employee qualifies for promotion if they have passed the CSE AND completed 5 years of service AND received a 'Very Satisfactory' rating."
  - Symbolic: P ∧ Q ∧ R (all three must be true)
  - Missing any single condition disqualifies the employee.

### Identifying Conjunctions in Natural Language

| Natural Language | Symbolic Form |
|-----------------|---------------|
| "P and Q" | P ∧ Q |
| "P but Q" | P ∧ Q |
| "P yet Q" | P ∧ Q |
| "P although Q" | P ∧ Q |
| "P however Q" | P ∧ Q |
| "Both P and Q" | P ∧ Q |
| "P as well as Q" | P ∧ Q |

**Important:** Words like "but," "yet," and "although" carry emotional contrast in English, but logically they function identically to "and" — both propositions must be true.

---

## 4.3 Disjunction (OR — ∨)

The **disjunction** operator combines two propositions and produces a compound statement that is true **when at least one** component proposition is true.

### Symbol and Structure

- Symbol: **∨**
- Read as: "P or Q"
- Written: P ∨ Q
- True when: P is true, Q is true, or both are true
- False when: Both P and Q are false

### Truth Table for Disjunction

| P | Q | P ∨ Q |
|---|---|-------|
| T | T | **T** |
| T | F | **T** |
| F | T | **T** |
| F | F | **F** |

**Key insight:** Disjunction is the most permissive binary operator — it only fails when EVERYTHING fails. One true component saves the entire statement.

### Inclusive OR vs. Exclusive OR

In formal logic, ∨ is **inclusive OR** — it allows both to be true:
- "Applicants may submit online OR in person." → Submitting both ways is logically acceptable.

**Exclusive OR** (XOR, sometimes written ⊕) means "one or the other but NOT both":
- "The traffic light is red OR green." → It cannot be both simultaneously.

**CSE default:** Unless explicitly stated otherwise, OR in logic questions means inclusive OR (∨).

### Easy Examples

- P = "The office is open on Saturday." Q = "The office is open on Sunday."
  - P ∨ Q = "The office is open on Saturday OR Sunday."
  - True if open Saturday only, Sunday only, or both days.

- P = "Juan passed the written exam." Q = "Juan passed the interview."
  - P ∨ Q = "Juan passed the written exam OR the interview."
  - False only if Juan failed BOTH.

### Medium Examples

- P = "The employee has a master's degree." Q = "The employee has 10 years of experience."
  - P ∨ Q = "The employee has a master's degree OR 10 years of experience."
  - Eligibility requires at least one — having both also qualifies.

- "Applicants must submit either a birth certificate OR a passport as proof of identity."
  - Submitting both is acceptable (inclusive OR).
  - Submitting neither disqualifies the applicant.

### Advanced Examples

- (P ∨ Q) ∧ R = "Either the budget is approved OR the emergency fund is released, AND the director signs."
  - The director's signature is mandatory (R must be true).
  - At least one funding source must be secured (P or Q or both).

### Identifying Disjunctions in Natural Language

| Natural Language | Symbolic Form |
|-----------------|---------------|
| "P or Q" | P ∨ Q |
| "Either P or Q" | P ∨ Q |
| "P or Q or both" | P ∨ Q |
| "At least one of P, Q" | P ∨ Q |
| "P unless Q" | P ∨ Q (equivalent to ¬Q → P) |

### Common Misunderstanding

Many examinees read "either...or..." as exclusive. In formal logic and in CSE questions, treat "or" as inclusive unless the question explicitly states "but not both."

---

## 4.4 Negation (NOT — ¬)

The **negation** operator is the only unary operator — it takes a single proposition and flips its truth value.

### Symbol and Structure

- Symbol: **¬**
- Read as: "not P" or "it is not the case that P"
- Written: ¬P
- True when: P is false
- False when: P is true

### Truth Table for Negation

| P | ¬P |
|---|-----|
| T | **F** |
| F | **T** |

**Key insight:** Negation is a truth-value inverter. Whatever P is, ¬P is the opposite.

### Easy Examples

- P = "The meeting is postponed."
  - ¬P = "The meeting is NOT postponed." (i.e., the meeting proceeds as scheduled)

- P = "All employees are managers."
  - ¬P = "NOT all employees are managers." (i.e., at least one employee is not a manager)

- P = "The document is signed."
  - ¬P = "The document is NOT signed."

### Medium Examples

- P = "The project is on schedule."
  - ¬P = "The project is NOT on schedule." (it is delayed or ahead)

- Negating a conjunction: P ∧ Q = "The report is complete AND accurate."
  - ¬(P ∧ Q) = "It is NOT the case that the report is both complete and accurate."
  - This means: the report is incomplete, OR inaccurate, OR both. (De Morgan's Law)

- Negating a disjunction: P ∨ Q = "The employee works onsite OR remotely."
  - ¬(P ∨ Q) = "The employee works NEITHER onsite NOR remotely."
  - This means: both P and Q are false. (De Morgan's Law)

### Advanced Examples — Double Negation

- ¬(¬P) = P (double negation cancels out)
- "It is not the case that the report is NOT complete" = "The report IS complete."

### Negating Quantified Statements

| Original | Negation |
|----------|----------|
| "All employees passed." | "At least one employee did NOT pass." |
| "Some employees are late." | "NO employees are late." |
| "No one is absent." | "At least one person IS absent." |

**Critical rule:** The negation of "all" is "not all" (which means "at least one is not"), NOT "none."

### Common Negation Errors

| Error | Why It's Wrong |
|-------|---------------|
| Negation of "All A are B" = "No A are B" | Wrong — correct negation is "Some A are not B" |
| Negation of "Some A are B" = "Some A are not B" | Wrong — correct negation is "No A are B" |
| ¬(P ∧ Q) = ¬P ∧ ¬Q | Wrong — correct is ¬P ∨ ¬Q (De Morgan's) |
| ¬(P ∨ Q) = ¬P ∨ ¬Q | Wrong — correct is ¬P ∧ ¬Q (De Morgan's) |

---

## 4.5 Conditional Operator (IF-THEN — →)

The **conditional** operator expresses a one-way implication: if the antecedent is true, then the consequent must also be true.

### Symbol and Structure

- Symbol: **→**
- Read as: "if P then Q" or "P implies Q"
- Written: P → Q
- P = antecedent (the condition/hypothesis)
- Q = consequent (the result/conclusion)
- False when: P is true AND Q is false (the promise is broken)
- True in all other cases

### Truth Table for Conditional

| P | Q | P → Q |
|---|---|-------|
| T | T | **T** |
| T | F | **F** |
| F | T | **T** |
| F | F | **T** |

**Key insight:** A conditional is false ONLY when the antecedent is true but the consequent is false. When the antecedent is false, the conditional is automatically true (vacuously true) — the promise was never triggered.

### Why "False → True" Is True

Think of P → Q as a promise: "If you pass the exam, I will buy you dinner."
- You pass, I buy dinner → Promise kept (T → T = T)
- You pass, I don't buy dinner → Promise broken (T → F = F)
- You don't pass, I buy dinner anyway → Promise not violated (F → T = T)
- You don't pass, I don't buy dinner → Promise not violated (F → F = T)

The promise only speaks about what happens when you pass. If you don't pass, the promise is irrelevant — not broken.

### Easy Examples

- P = "It rains." Q = "The roads become wet."
  - P → Q = "If it rains, then the roads become wet."
  - False only if it rains but roads stay dry.

- P = "The employee is late." Q = "A warning is issued."
  - P → Q = "If the employee is late, then a warning is issued."
  - The employee being on time says nothing about whether warnings are issued for other reasons.

### Medium Examples

- P = "The applicant passes the CSE." Q = "The applicant is eligible for permanent appointment."
  - P → Q = "If the applicant passes the CSE, then they are eligible for permanent appointment."
  - Passing is SUFFICIENT for eligibility.
  - But eligibility might also require other conditions (this conditional doesn't exclude that).

- "Employees receive overtime pay only if they work beyond 8 hours."
  - Let P = "receives overtime pay" and Q = "works beyond 8 hours"
  - "Only if" means: P → Q (receiving overtime requires working beyond 8 hours)
  - This is NOT the same as Q → P (working beyond 8 hours doesn't guarantee overtime pay — approval may be needed)

### Advanced Examples

- Contrapositive: P → Q is logically equivalent to ¬Q → ¬P
  - "If it rains, roads get wet" ≡ "If roads are NOT wet, it did NOT rain."
  - The contrapositive is ALWAYS valid.

- Converse: Q → P is NOT equivalent to P → Q
  - "If roads are wet, it rained" — INVALID (sprinklers could cause wet roads)

- Inverse: ¬P → ¬Q is NOT equivalent to P → Q
  - "If it doesn't rain, roads don't get wet" — INVALID (other causes exist)

### Recognizing Conditionals in Natural Language

| Natural Language | Symbolic Form |
|-----------------|---------------|
| "If P, then Q" | P → Q |
| "P implies Q" | P → Q |
| "P only if Q" | P → Q |
| "Q if P" | P → Q |
| "Q whenever P" | P → Q |
| "Q provided that P" | P → Q |
| "P is sufficient for Q" | P → Q |
| "Q is necessary for P" | P → Q |
| "All P are Q" | P → Q |
| "P unless Q" | ¬Q → P (equivalent to P ∨ Q) |

---

## 4.6 Biconditional Operator (IF AND ONLY IF — ↔)

The **biconditional** operator expresses two-way equivalence: both propositions must have the same truth value.

### Symbol and Structure

- Symbol: **↔**
- Read as: "P if and only if Q" (abbreviated "P iff Q")
- Written: P ↔ Q
- True when: P and Q have the SAME truth value (both true or both false)
- False when: P and Q have DIFFERENT truth values

### Truth Table for Biconditional

| P | Q | P ↔ Q |
|---|---|-------|
| T | T | **T** |
| T | F | **F** |
| F | T | **F** |
| F | F | **T** |

**Key insight:** The biconditional is true when both sides match. It is equivalent to (P → Q) ∧ (Q → P) — both directions of implication hold simultaneously.

### Difference Between Conditional and Biconditional

| Operator | Meaning | Example |
|----------|---------|---------|
| P → Q | P guarantees Q, but Q doesn't guarantee P | "If it rains, roads get wet." (Roads can be wet without rain.) |
| P ↔ Q | P guarantees Q AND Q guarantees P | "A figure is a square iff it has four equal sides and four right angles." (Each condition guarantees the other.) |

### Easy Examples

- P = "The switch is on." Q = "The light is lit."
  - P ↔ Q = "The switch is on if and only if the light is lit."
  - True when both are on or both are off. False when one is on and the other is off.

- P = "An integer is even." Q = "The integer is divisible by 2."
  - P ↔ Q = "An integer is even if and only if it is divisible by 2."
  - These are definitionally equivalent — always the same truth value.

### Medium Examples

- P = "An employee is regular." Q = "The employee has completed probation."
  - P ↔ Q = "An employee is regular if and only if they have completed probation."
  - Completing probation makes you regular (Q → P), and being regular means you completed probation (P → Q).

- P = "A triangle is equilateral." Q = "All three sides are equal."
  - P ↔ Q — true by geometric definition.

### Advanced Examples

- P ↔ Q is equivalent to (P → Q) ∧ (Q → P)
  - To prove a biconditional, you must prove BOTH directions.
  - To disprove it, find a case where one direction fails.

- P ↔ Q is also equivalent to (P ∧ Q) ∨ (¬P ∧ ¬Q)
  - "Either both are true, or both are false."

### Identifying Biconditionals in Natural Language

| Natural Language | Symbolic Form |
|-----------------|---------------|
| "P if and only if Q" | P ↔ Q |
| "P iff Q" | P ↔ Q |
| "P is equivalent to Q" | P ↔ Q |
| "P exactly when Q" | P ↔ Q |
| "P is necessary and sufficient for Q" | P ↔ Q |

### Common Trap: Conditional vs. Biconditional

"If you study, you will pass" (P → Q) does NOT mean "You will pass if and only if you study" (P ↔ Q). The conditional allows passing without studying; the biconditional does not.

---

## 4.7 Truth Tables

A **truth table** is a systematic method for evaluating every possible combination of truth values for the component propositions in a compound statement. It is the definitive tool for determining whether a compound statement is a tautology, contradiction, or contingency.

### Purpose of Truth Tables

- Determine the truth value of any compound statement for all possible inputs
- Prove logical equivalence between two expressions
- Identify tautologies (always true) and contradictions (always false)
- Verify the validity of logical arguments

### Building a Truth Table — Step by Step

**Step 1:** Identify all propositional variables (P, Q, R, etc.)

**Step 2:** Calculate the number of rows: 2^n where n = number of variables
- 2 variables → 4 rows
- 3 variables → 8 rows
- 4 variables → 16 rows

**Step 3:** List all possible truth-value combinations systematically

**Step 4:** Evaluate sub-expressions from innermost to outermost

**Step 5:** Compute the final column

### Example: Truth Table for (P ∧ Q) → R

Three variables → 2³ = 8 rows.

| P | Q | R | P ∧ Q | (P ∧ Q) → R |
|---|---|---|-------|-------------|
| T | T | T | T | **T** |
| T | T | F | T | **F** |
| T | F | T | F | **T** |
| T | F | F | F | **T** |
| F | T | T | F | **T** |
| F | T | F | F | **T** |
| F | F | T | F | **T** |
| F | F | F | F | **T** |

**Analysis:** This statement is false only when P and Q are both true but R is false. In all other cases, the antecedent (P ∧ Q) is false, making the conditional vacuously true.

### Example: Truth Table for ¬(P ∨ Q)

| P | Q | P ∨ Q | ¬(P ∨ Q) |
|---|---|-------|-----------|
| T | T | T | **F** |
| T | F | T | **F** |
| F | T | T | **F** |
| F | F | F | **T** |

**Analysis:** ¬(P ∨ Q) is true only when both P and Q are false. This is equivalent to ¬P ∧ ¬Q (De Morgan's Law).

### Operator Precedence (Evaluation Order)

When no parentheses are present, evaluate in this order:

| Priority | Operator | Name |
|----------|----------|------|
| 1 (highest) | ¬ | Negation |
| 2 | ∧ | Conjunction |
| 3 | ∨ | Disjunction |
| 4 | → | Conditional |
| 5 (lowest) | ↔ | Biconditional |

**Example:** P ∨ Q ∧ R means P ∨ (Q ∧ R), NOT (P ∨ Q) ∧ R.

**Best practice:** Always use parentheses to make evaluation order explicit. CSE questions typically include parentheses to avoid ambiguity.

### Tautologies, Contradictions, and Contingencies

| Type | Definition | Example |
|------|-----------|---------|
| Tautology | True in ALL rows of the truth table | P ∨ ¬P (law of excluded middle) |
| Contradiction | False in ALL rows of the truth table | P ∧ ¬P |
| Contingency | True in some rows, false in others | P ∧ Q |

---

## 4.8 Compound Statements

A **compound statement** uses multiple logical operators to express complex logical relationships. Evaluating compound statements requires careful attention to operator precedence and systematic decomposition.

### Combining Multiple Operators

Real-world logic rarely involves a single operator. Government policies, eligibility rules, and administrative conditions combine AND, OR, NOT, and IF-THEN in layered structures.

**Example 1:** (P ∧ Q) → R
- "If the applicant has a degree AND experience, then they qualify."
- Evaluate P ∧ Q first, then apply the conditional.

**Example 2:** ¬(P ∨ Q)
- "It is NOT the case that the employee works onsite OR remotely."
- Evaluate P ∨ Q first, then negate the result.
- Equivalent to: ¬P ∧ ¬Q (the employee works neither onsite nor remotely)

**Example 3:** (P → Q) ∧ (Q → R)
- "If it rains then roads are wet, AND if roads are wet then traffic slows."
- Two conditionals joined by conjunction. Both must hold.
- Allows chain reasoning: P → R (if it rains, traffic slows)

### Step-by-Step Evaluation

**Evaluate:** ¬P ∨ (Q ∧ R) when P = T, Q = T, R = F

1. Q ∧ R = T ∧ F = **F**
2. ¬P = ¬T = **F**
3. ¬P ∨ (Q ∧ R) = F ∨ F = **F**

**Evaluate:** (P → Q) ↔ (¬P ∨ Q) for all values

| P | Q | P → Q | ¬P | ¬P ∨ Q | (P → Q) ↔ (¬P ∨ Q) |
|---|---|-------|----|--------|---------------------|
| T | T | T | F | T | **T** |
| T | F | F | F | F | **T** |
| F | T | T | T | T | **T** |
| F | F | T | T | T | **T** |

**Result:** Always true — this proves P → Q ≡ ¬P ∨ Q (a fundamental logical equivalence).

### Nested Logic and Grouping

Parentheses determine evaluation order. Changing parentheses changes meaning:

- P ∧ (Q ∨ R) ≠ (P ∧ Q) ∨ R

**Proof:**

| P | Q | R | P ∧ (Q ∨ R) | (P ∧ Q) ∨ R |
|---|---|---|-------------|-------------|
| T | F | T | T ∧ T = **T** | F ∨ T = **T** |
| F | F | T | F ∧ T = **F** | F ∨ T = **T** |

Row 2 shows different results — the expressions are NOT equivalent.

### Multi-Step Evaluation Strategy

For complex expressions:
1. Identify the **main operator** (the one evaluated last based on precedence and parentheses)
2. Break the expression into sub-expressions around the main operator
3. Evaluate each sub-expression independently
4. Combine using the main operator

**Example:** ((P ∧ Q) → R) ∨ ¬S
- Main operator: ∨ (outermost)
- Left sub-expression: (P ∧ Q) → R
- Right sub-expression: ¬S
- Evaluate each side, then combine with OR

---

## 4.9 Validity and Logical Equivalence

Two expressions are **logically equivalent** if they have identical truth values in every possible scenario (every row of their truth tables matches).

### Key Logical Equivalences

| Equivalence | Name | Explanation |
|-------------|------|-------------|
| P → Q ≡ ¬P ∨ Q | Conditional as disjunction | "If P then Q" means "either not-P or Q" |
| ¬(P ∧ Q) ≡ ¬P ∨ ¬Q | De Morgan's Law 1 | Negating AND gives OR of negations |
| ¬(P ∨ Q) ≡ ¬P ∧ ¬Q | De Morgan's Law 2 | Negating OR gives AND of negations |
| P → Q ≡ ¬Q → ¬P | Contrapositive | Equivalent to the original conditional |
| P ↔ Q ≡ (P → Q) ∧ (Q → P) | Biconditional expansion | Both directions must hold |
| ¬(¬P) ≡ P | Double negation | Two negations cancel |
| P ∧ (Q ∨ R) ≡ (P ∧ Q) ∨ (P ∧ R) | Distribution of ∧ over ∨ | AND distributes over OR |
| P ∨ (Q ∧ R) ≡ (P ∨ Q) ∧ (P ∨ R) | Distribution of ∨ over ∧ | OR distributes over AND |

### De Morgan's Laws — Critical for CSE

De Morgan's Laws tell you how to negate compound statements:

**Law 1:** ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
- "It is NOT the case that both P and Q are true" = "Either P is false OR Q is false (or both)"
- Example: "It is NOT true that the report is complete AND accurate" = "The report is incomplete OR inaccurate."

**Law 2:** ¬(P ∨ Q) ≡ ¬P ∧ ¬Q
- "It is NOT the case that P or Q is true" = "Both P is false AND Q is false"
- Example: "It is NOT true that the employee works onsite OR remotely" = "The employee works neither onsite NOR remotely."

### Tautologies You Should Recognize

| Tautology | Name |
|-----------|------|
| P ∨ ¬P | Law of Excluded Middle |
| ¬(P ∧ ¬P) | Law of Non-Contradiction |
| (P → Q) ↔ (¬Q → ¬P) | Contrapositive Equivalence |
| (P → Q) ↔ (¬P ∨ Q) | Material Conditional |
| ((P → Q) ∧ P) → Q | Modus Ponens |
| ((P → Q) ∧ ¬Q) → ¬P | Modus Tollens |

### Contradictions You Should Recognize

| Contradiction | Why |
|---------------|-----|
| P ∧ ¬P | A proposition cannot be both true and false |
| (P → Q) ∧ P ∧ ¬Q | If P implies Q and P is true, Q cannot be false |

### Testing Logical Equivalence

To prove two expressions are equivalent:
1. Build truth tables for both expressions
2. Compare the final columns row by row
3. If every row matches, the expressions are logically equivalent

To disprove equivalence:
- Find ONE row where the truth values differ — that's a counterexample.

---

## 4.10 Practical Applications of Logical Operators

### Government and Public Service

- **Eligibility rules:** "An applicant qualifies if they are Filipino AND at least 18 years old AND have no pending criminal case." (P ∧ Q ∧ R)
- **Alternative compliance:** "Submit requirements via email OR in person at the office." (P ∨ Q)
- **Prohibitions:** "Government vehicles shall NOT be used for personal purposes." (¬P)
- **Conditional benefits:** "If the employee completes 15 years of service, then they are eligible for early retirement." (P → Q)
- **Definitional equivalence:** "An employee is considered AWOL if and only if they are absent without approved leave for 30 consecutive days." (P ↔ Q)

### Computer Programming and Information Systems

- **Boolean conditions:** `if (isAdmin AND isActive)` — conjunction in code
- **Fallback logic:** `if (primaryServer OR backupServer)` — disjunction in code
- **Access control:** `if (NOT isBlocked)` — negation in code
- **Validation rules:** `if (hasID AND (hasBirthCert OR hasPassport))` — nested operators
- **Database queries:** `WHERE status = 'active' AND department = 'HR'` — SQL conjunction

### Workplace Decision-Making

- **Meeting scheduling:** "The meeting proceeds if the quorum is met AND the chairperson is present." (P ∧ Q)
- **Leave approval:** "Leave is approved if the supervisor signs OR the department head signs." (P ∨ Q)
- **Policy exceptions:** "The rule does NOT apply to employees on probation." (¬P)
- **Performance evaluation:** "An employee receives a bonus if and only if their rating is 'Outstanding.'" (P ↔ Q)

### Legal and Administrative Reasoning

- **Contract clauses:** "The contract is valid if signed by both parties AND notarized." (P ∧ Q)
- **Regulatory compliance:** "A business permit is issued only if all requirements are submitted." (P → Q, where P = permit issued, Q = requirements submitted)
- **Exception handling:** "All employees must attend UNLESS they have approved leave." (¬Q → P, equivalent to P ∨ Q)

---

## 4.11 Step-by-Step Logical Operator Strategies

### The IOEV Method (Identify → Operator → Evaluate → Verify)

**Step 1: IDENTIFY** the propositions
- Label each simple statement (P, Q, R, etc.)
- Determine the truth value of each if given

**Step 2: OPERATOR** — determine which operator connects them
- Look for keywords: "and," "or," "not," "if...then," "if and only if"
- Identify the main operator (evaluated last)

**Step 3: EVALUATE** using the operator's truth table
- Apply the truth conditions for that specific operator
- Work from innermost parentheses outward

**Step 4: VERIFY** the result
- Check: does the answer make logical sense?
- Test with a counterexample if unsure

### Shortcut Methods for CSE Questions

**Conjunction shortcut:** If ANY component is false, the conjunction is false. Don't evaluate everything — find one false component and stop.

**Disjunction shortcut:** If ANY component is true, the disjunction is true. Find one true component and stop.

**Conditional shortcut:** A conditional is false ONLY when the antecedent is true and the consequent is false. If the antecedent is false, the conditional is automatically true — stop evaluating.

**Negation shortcut:** Just flip. T becomes F, F becomes T.

**Biconditional shortcut:** Check if both sides match. Same value = true. Different values = false.

### Elimination Strategies

When facing multiple-choice questions:

1. **Test with specific values:** Assign T/F to variables and check which answer choice matches
2. **Find the falsifying case:** For conditionals, look for T → F. If you can't find it, the statement is valid.
3. **Apply De Morgan's:** If a negated compound appears in choices, convert using De Morgan's Laws
4. **Check equivalences:** P → Q always equals ¬P ∨ Q. If one appears in the question and the other in the choices, they match.

### Rapid-Analysis for Time Pressure

| If you see... | Immediately know... |
|---------------|-------------------|
| P ∧ ¬P | Always FALSE (contradiction) |
| P ∨ ¬P | Always TRUE (tautology) |
| P → P | Always TRUE |
| ¬(P → Q) | Equivalent to P ∧ ¬Q |
| P ↔ P | Always TRUE |
| P ↔ ¬P | Always FALSE |

---

## 4.12 Common Errors in Logical Operators

### Error 1: Confusing Inclusive and Exclusive OR

**Wrong:** "A or B" means only one can be true.
**Correct:** In formal logic, P ∨ Q is inclusive — both can be true. The statement is false only when BOTH are false.

**CSE trap:** A question states "Employees may take vacation leave OR sick leave." An answer choice says "An employee who takes both is violating the rule." This is WRONG — inclusive OR allows both.

### Error 2: Incorrect Negation of Compound Statements

**Wrong:** ¬(P ∧ Q) = ¬P ∧ ¬Q
**Correct:** ¬(P ∧ Q) = ¬P ∨ ¬Q (De Morgan's Law)

**Wrong:** ¬(P ∨ Q) = ¬P ∨ ¬Q
**Correct:** ¬(P ∨ Q) = ¬P ∧ ¬Q (De Morgan's Law)

**Memory aid:** When you negate through parentheses, the operator FLIPS (∧ becomes ∨, and ∨ becomes ∧).

### Error 3: Reversing Conditional Direction

**Wrong:** "If P then Q" means the same as "If Q then P."
**Correct:** P → Q ≠ Q → P. The converse is NOT equivalent to the original.

**CSE trap:** "If an employee passes the CSE, they are eligible for appointment." A distractor says "If eligible for appointment, they passed the CSE." This reverses the conditional and is NOT guaranteed.

### Error 4: Ignoring Operator Precedence

**Wrong:** Evaluating P ∨ Q ∧ R as (P ∨ Q) ∧ R
**Correct:** ∧ has higher precedence than ∨, so P ∨ Q ∧ R = P ∨ (Q ∧ R)

### Error 5: Treating Conditional as Biconditional

**Wrong:** "If you study, you pass" means "You pass if and only if you study."
**Correct:** P → Q only guarantees one direction. The biconditional P ↔ Q requires both directions.

**CSE trap:** A question gives "If it rains, the event is cancelled." A distractor concludes "The event is cancelled only when it rains." This incorrectly adds the reverse direction.

### Error 6: Evaluating Statements Incompletely

**Wrong:** Checking only one row of a truth table and concluding the statement is always true/false.
**Correct:** You must check ALL rows. A statement is a tautology only if true in EVERY row.

### Error 7: Misinterpreting "Only If"

**Wrong:** "P only if Q" means "If Q then P" (Q → P)
**Correct:** "P only if Q" means "If P then Q" (P → Q)

**Memory aid:** "Only if" introduces the NECESSARY condition. "P only if Q" means Q is necessary for P — so if P is true, Q must be true: P → Q.

---

## 4.13 Advanced Symbolic Logic Analysis

### Nested Compound Statements

**Example 1:** Evaluate ((P → Q) ∧ (R ∨ ¬S)) → (P ∧ R → Q)

This requires:
1. Evaluate P → Q
2. Evaluate ¬S, then R ∨ ¬S
3. Combine with ∧
4. Evaluate P ∧ R, then P ∧ R → Q
5. Apply the main conditional

**Example 2:** ¬((P ∧ Q) ↔ (R → S))

1. Evaluate P ∧ Q
2. Evaluate R → S
3. Apply biconditional
4. Negate the result

### Symbolic Equivalence Transformations

Transform expressions into equivalent forms for easier evaluation:

| Original | Transformed | Rule Used |
|----------|-------------|-----------|
| P → Q | ¬P ∨ Q | Material conditional |
| ¬(P → Q) | P ∧ ¬Q | Negation of conditional |
| P ↔ Q | (P ∧ Q) ∨ (¬P ∧ ¬Q) | Biconditional expansion |
| ¬(P ↔ Q) | (P ∧ ¬Q) ∨ (¬P ∧ Q) | Negation of biconditional (XOR) |
| P → (Q → R) | (P ∧ Q) → R | Exportation |
| (P ∧ Q) → R | P → (Q → R) | Importation |

### Multi-Operator Deductions

**Given:** P → Q, Q → R, ¬R
**Derive:** ¬P

**Proof:**
1. Q → R (given)
2. ¬R (given)
3. ¬Q (from 1, 2 by Modus Tollens)
4. P → Q (given)
5. ¬P (from 3, 4 by Modus Tollens)

**Given:** P ∨ Q, ¬P, Q → R
**Derive:** R

**Proof:**
1. P ∨ Q (given)
2. ¬P (given)
3. Q (from 1, 2 by Disjunctive Syllogism)
4. Q → R (given)
5. R (from 3, 4 by Modus Ponens)

### Argument Validity Testing with Truth Tables

An argument is **valid** if there is no row where all premises are true but the conclusion is false.

**Test:** Premises: P → Q, P. Conclusion: Q.

| P | Q | P → Q | Premises both true? | Q |
|---|---|-------|--------------------|----|
| T | T | T | ✅ Yes | T ✅ |
| T | F | F | ❌ No (P → Q is F) | — |
| F | T | T | ❌ No (P is F) | — |
| F | F | T | ❌ No (P is F) | — |

Only row 1 has all premises true, and Q is true there. **Valid argument (Modus Ponens).**

---

## 4.14 CSE-Style Practice Examples

### Easy Example

**Question:** If P is TRUE and Q is FALSE, what is the truth value of P ∧ Q?

**Solution:** P ∧ Q requires BOTH to be true. P = T, Q = F. Since Q is false, P ∧ Q = **FALSE**.

### Medium Example

**Question:** Which expression is logically equivalent to ¬(P ∧ Q)?

A) ¬P ∧ ¬Q
B) ¬P ∨ ¬Q
C) P ∨ Q
D) ¬P → ¬Q

**Solution:** By De Morgan's Law, ¬(P ∧ Q) ≡ ¬P ∨ ¬Q. Answer: **B**.

### Hard Example

**Question:** Given P → Q and Q → R, which of the following MUST be true?

A) R → P
B) ¬P → ¬R
C) P → R
D) ¬R → Q

**Solution:** By Hypothetical Syllogism, P → Q and Q → R yield P → R. Answer: **C**.

Checking the others:
- A) R → P is the converse of P → R — not guaranteed.
- B) ¬P → ¬R is the inverse of P → R — not guaranteed.
- D) ¬R → Q contradicts Modus Tollens (¬R → ¬Q is valid, not ¬R → Q).

---

## Quick Recap

| Operator | Symbol | True When | False When |
|----------|--------|-----------|------------|
| Conjunction | ∧ | Both P and Q are true | At least one is false |
| Disjunction | ∨ | At least one is true | Both are false |
| Negation | ¬ | P is false | P is true |
| Conditional | → | P is false, OR Q is true | P is true AND Q is false |
| Biconditional | ↔ | P and Q have same value | P and Q have different values |

### Key Equivalences to Memorize

- P → Q ≡ ¬P ∨ Q
- ¬(P ∧ Q) ≡ ¬P ∨ ¬Q (De Morgan's 1)
- ¬(P ∨ Q) ≡ ¬P ∧ ¬Q (De Morgan's 2)
- P → Q ≡ ¬Q → ¬P (Contrapositive)
- P ↔ Q ≡ (P → Q) ∧ (Q → P)

### Common Traps

- "Or" in logic is inclusive (allows both true)
- "Only if" introduces the consequent, not the antecedent
- Negating a compound flips the operator (De Morgan's)
- Conditional is false ONLY when T → F
- Biconditional requires BOTH directions

---

## Memory Aids

**AND (∧) — "ALL must pass":** Think of a security checkpoint with two gates. Both gates must open. One locked gate = denied.

**OR (∨) — "ANY will do":** Think of a vending machine that accepts coins OR bills. Either works. Both also work. Only "nothing inserted" fails.

**NOT (¬) — "Flip the switch":** A light switch. If it's ON, flip to OFF. If it's OFF, flip to ON.

**IF-THEN (→) — "The promise":** A promise is broken ONLY when you said you'd do something (antecedent true) and didn't (consequent false). If you never made the promise (antecedent false), you can't break it.

**IFF (↔) — "The twin":** Two twins always match. Both happy or both sad. If one is happy and the other sad, something is wrong.

**De Morgan's — "Break and flip":** When negation enters parentheses, it BREAKS the operator (∧↔∨) and FLIPS each component (P→¬P).

**Precedence — "Not And Or Then Only":** ¬, ∧, ∨, →, ↔ (NAOTO — mnemonic for Filipino examinees).

---


---

### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Identify the type of problem and select the appropriate method
- [ ] Set up the correct equation or formula for the problem
- [ ] Execute calculations accurately and efficiently
- [ ] Verify answers by checking reasonableness
- [ ] Apply concepts to CSE-style word problems
- [ ] Avoid common mistakes and traps in this topic


---

### Which Method?

For each problem, identify the type and solve.

**1.** [Problem 1]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.

**2.** [Problem 2]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.

**3.** [Problem 3]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.

**4.** [Problem 4]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.

**5.** [Problem 5]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.

**6.** [Problem 6]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** This item checks whether the learner can name the right rule before solving.


---

### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** [Example 1]

- Step 1: Identify the relationship: _____
- Step 2: Set up the equation: _____
- Step 3: Solve: _____

**Answer:** [Complete solution]

**2.** [Example 2]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**3.** [Example 3]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**4.** [Example 4]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]

**5.** [Example 5]

- Step 1: _____
- Step 2: _____
- Step 3: _____

**Answer:** [Complete solution]


---

### Connections

How this topic connects to other areas of the CSE:

- **Logical Statements:** Operators combine the simple statements studied in the previous lesson
- **Conditional Reasoning:** The conditional operator (→) is the most frequently tested operator on the CSE
- **Truth and Validity:** Truth tables (operator outputs) are the foundation for evaluating argument validity
- **Syllogisms:** Syllogistic reasoning uses conjunction (AND) and conditional (IF-THEN) operators

### Mastery Checklist
After completing this lesson, you can now:

✅ Define all five logical operators and state their truth conditions precisely
✅ Identify conjunctions, disjunctions, negations, conditionals, and biconditionals in natural language
✅ Interpret compound logical statements containing multiple operators
✅ Construct and analyze truth tables for any combination of operators
✅ Distinguish valid from invalid logical expressions using systematic evaluation
✅ Apply De Morgan's Laws to negate compound statements correctly
✅ Recognize logically equivalent expressions and tautologies
✅ Evaluate symbolic logic statements by applying operator precedence rules
✅ Solve CSE-style logical operator questions efficiently under time pressure
✅ Eliminate incorrect answer choices by testing truth conditions strategically

> 🤔 **Why does this work?** Logical operators are defined entirely by their truth tables — fixed input-output mappings that never change regardless of content. This means you can evaluate any compound statement mechanically: determine each component's truth value, then look up the result in the truth table. The mechanical nature of truth-functional evaluation is what makes formal logic objective — two people applying the same rules to the same inputs will always reach the same conclusion.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.

> **Why does this work?** A valid reasoning rule must explain every given item consistently; testing the same rule across the full set prevents early-pattern traps.

### Check Your Understanding

1. What core idea from this section should you recall first?
2. Which method fits this type of question, and why?
3. What common error should you avoid?


### Mastery Checklist

- [ ] I can solve representative items accurately and quickly.
- [ ] I can explain common traps and how to avoid them.
- [ ] I can transfer this method to mixed-question sets.
