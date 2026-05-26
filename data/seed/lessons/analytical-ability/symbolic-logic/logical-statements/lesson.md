# Logical Statements

## Explanations

### Introduction

**Logical Statements** are the foundation of symbolic logic and deductive reasoning — the building blocks from which all valid arguments are constructed. A logical statement (also called a **proposition**) is a declarative sentence that is either true or false, but never both simultaneously. In the Philippine Civil Service Examination (CSE), logical statement questions test your ability to evaluate truth values, analyze conditional relationships, identify valid conclusions, and detect reasoning errors.

This subtopic covers the following critical areas:
- **True/False Reasoning** — determining whether statements and conclusions are logically true or false
- **Conditional Statements** — understanding "if-then" logic, contrapositives, converses, and inverses
- **Valid and Invalid Conclusions** — distinguishing conclusions that follow necessarily from premises versus those that do not
- **Symbolic Representation** — translating verbal statements into logical notation (P → Q, P ∧ Q, P ∨ Q, ¬P)
- **Common Logical Fallacies** — recognizing reasoning errors that appear convincing but are logically invalid
- **Multi-Statement Analysis** — drawing conclusions from sets of linked premises

Mastering logical statements is essential for any civil servant. Government employees interpret regulations, evaluate policy conditions, assess eligibility criteria, and make decisions based on conditional rules daily. The CSE tests logical reasoning because it directly measures the analytical thinking required for administrative, legal, and procedural work in public service.

### Why Logical Statements Are Tested in the CSE

The Civil Service Examination tests logical statements because:

- Government employees must interpret conditional rules in laws, memoranda, and administrative orders — "If the applicant meets criteria X, then benefit Y is granted"
- Public servants evaluate eligibility conditions that require precise logical reasoning — a single misinterpretation can deny services to qualified citizens or grant them to unqualified ones
- Administrative decision-making requires distinguishing between what is necessarily true versus what is merely possible
- Policy implementation demands understanding of sufficient and necessary conditions — knowing when a condition guarantees an outcome versus when it merely allows one
- Legal and regulatory interpretation requires recognizing when a conclusion follows from stated premises and when it does not
- Logical reasoning separates examinees who can think systematically from those who rely on intuition or guesswork
- Both Professional and Sub-Professional levels include symbolic logic items, making this a high-value preparation area
- The ability to detect logical fallacies protects against manipulation in negotiations, proposals, and administrative communications

### Common Mistakes Examinees Make

1. **Confusing the converse with the original statement** — believing that "If P then Q" automatically means "If Q then P" (it does not)
2. **Affirming the consequent** — concluding P from "If P then Q" and Q being true (invalid reasoning)
3. **Denying the antecedent** — concluding "not Q" from "If P then Q" and P being false (invalid reasoning)
4. **Treating possibility as certainty** — concluding that something must be true when it only might be true
5. **Ignoring qualifiers** — missing the difference between "all," "some," and "no" in premises
6. **Reversing conditional direction** — reading "only if" as "if" (they have different logical structures)
7. **Selecting partially correct answers** — choosing conclusions that sound reasonable but are not logically guaranteed by the premises
8. **Confusing sufficient and necessary conditions** — treating "sufficient for" as "required for" or vice versa

### Learning Objectives

After this lesson, you should be able to:

- Define logical statements and distinguish them from opinions, questions, and commands
- Identify the truth value of simple and compound statements
- Analyze conditional statements by identifying the antecedent and consequent
- Construct and evaluate the converse, inverse, and contrapositive of conditional statements
- Distinguish valid conclusions from invalid ones given a set of premises
- Recognize common logical fallacies including affirming the consequent and denying the antecedent
- Translate verbal statements into symbolic notation (P → Q, ¬P, P ∧ Q, P ∨ Q)
- Apply chain reasoning (transitivity) to derive conclusions from multiple linked premises
- Solve CSE-style symbolic logic questions efficiently under time pressure
- Eliminate incorrect answer choices using logical consistency testing

---

### 4.1 What Are Logical Statements?
> 🤔 **Why does this work?** The principle behind this operation follows from the fundamental properties of arithmetic. Understanding the "why" — not just the "how" — lets you recognize when to apply this method in unfamiliar problem contexts on the CSE.


A **logical statement** (or **proposition**) is a declarative sentence that has exactly one truth value — it is either **true** or **false**, but not both, and not neither.

#### What Qualifies as a Logical Statement

| Sentence | Logical Statement? | Why |
|----------|-------------------|-----|
| "Manila is the capital of the Philippines." | ✅ Yes | Declarative, verifiably true |
| "2 + 3 = 7" | ✅ Yes | Declarative, verifiably false |
| "All government employees pay taxes." | ✅ Yes | Declarative, has a truth value |
| "What time is the meeting?" | ❌ No | Question — no truth value |
| "Please submit your report." | ❌ No | Command — no truth value |
| "Wow, that's amazing!" | ❌ No | Exclamation — no truth value |
| "This painting is beautiful." | ❌ No | Subjective opinion — not objectively testable |
| "x + 5 = 10" | ❌ No | Open sentence — truth depends on unknown variable |

**Key principle:** A logical statement must be a complete declarative sentence whose truth can be determined (even if we don't currently know the answer). "There is life on Mars" is a logical statement — it is either true or false — even though we haven't confirmed which.

#### Simple vs. Compound Statements

A **simple statement** contains a single proposition:
- "The sun rises in the east." (P)
- "All employees must attend the seminar." (Q)

A **compound statement** combines two or more simple statements using logical connectors:
- "The sun rises in the east **and** sets in the west." (P ∧ Q)
- "Either the report is approved **or** it is returned for revision." (P ∨ Q)
- "**If** the budget is approved, **then** the project proceeds." (P → Q)

#### Truth Values in Practice

Every logical statement is assigned exactly one truth value:

| Statement | Truth Value | Reasoning |
|-----------|-------------|-----------|
| "The Philippines has 7,641 islands." | True | Verified geographic fact |
| "Water boils at 50°C at sea level." | False | Water boils at 100°C at sea level |
| "All triangles have three sides." | True | By definition |
| "Some birds cannot fly." | True | Penguins, ostriches, etc. |
| "No mammals lay eggs." | False | Platypus and echidna are mammals that lay eggs |

**Workplace example:** "All employees who have served for at least 15 years are eligible for early retirement." This is a logical statement — it is either true or false depending on the organization's policy. If the policy states this, the statement is true. If the threshold is 20 years, the statement is false.


> ⚠️ **Misconception:** "The formula always works the same way regardless of the problem context."

> **Why it fails:** CSE problems often present variations where the standard formula must be adapted. Blindly applying a memorized formula without checking the context leads to systematic errors.

> **Correct model:** Always read the problem to identify what type of relationship exists (direct, inverse, part-whole, etc.), then apply the appropriate formula. Verify your answer makes sense in the problem's context before selecting it.

---

### 4.2 True/False Reasoning

True/false reasoning is the skill of evaluating whether a conclusion is logically true, logically false, or cannot be determined from the given information.

#### Absolute Statements and Quantifiers

The words **all**, **every**, **no**, **none**, **some**, and **at least one** are called **quantifiers**. They determine the scope of a statement and are critical for evaluating truth.

| Quantifier | Meaning | To disprove, you need... |
|-----------|---------|--------------------------|
| All / Every | Without exception | One counterexample |
| No / None | Zero instances | One example that satisfies it |
| Some / At least one | One or more | Proof that zero exist |

**Critical insight for the CSE:** Universal statements ("All X are Y") are easy to disprove — you only need one counterexample. Existential statements ("Some X are Y") are easy to prove — you only need one example.

#### Evaluating Consistency Between Statements

When given multiple statements, check whether they can all be true simultaneously:

**Example 1:**
- Statement A: "All managers attend the Monday meeting."
- Statement B: "Carlos is a manager."
- Statement C: "Carlos does not attend the Monday meeting."

**Analysis:** If A and B are true, then Carlos must attend the Monday meeting. Statement C contradicts this. Therefore, A, B, and C cannot all be true simultaneously — they are **inconsistent**.

**Example 2:**
- Statement A: "Some employees work overtime."
- Statement B: "Maria is an employee."
- Statement C: "Maria does not work overtime."

**Analysis:** A says *some* employees work overtime — not all. Maria could be one who does or one who doesn't. All three statements can be true simultaneously — they are **consistent**.

#### The Difference Between "Must Be True" and "Could Be True"

This distinction is where most CSE examinees lose points:

| Category | Meaning | Example |
|----------|---------|---------|
| Must be true | Guaranteed by the premises — no alternative is possible | "All cats are mammals. Whiskers is a cat. Therefore, Whiskers is a mammal." |
| Could be true | Possible but not guaranteed — other scenarios exist | "Some cats are black. Whiskers is a cat. Therefore, Whiskers might be black." |
| Must be false | Contradicted by the premises | "No cats are reptiles. Whiskers is a cat. Therefore, Whiskers is a reptile." |

**CSE trap:** Many wrong answer choices present things that *could* be true but are not *necessarily* true. The correct answer is always what *must* be true given the premises.


> ⚠️ **Misconception:** "If my computed answer is close to one of the choices, it must be right."

> **Why it fails:** The CSE deliberately includes distractors that result from common errors — using the wrong operation, misidentifying the proportion type, or reversing the ratio. A "close" answer could be the result of a systematic mistake that the test writers anticipated.

> **Correct model:** Verify your setup before computing. Check that you've identified the correct proportion type, set up the equation properly, and solved accurately. A wrong setup with correct arithmetic still produces a wrong answer — and the CSE will include that wrong answer among the choices.

---


### Check Your Understanding

**1.** What is the key concept from this section? → **Review the preceding content to recall the main principle**

**2.** How would you apply this concept to a practical problem? → **Identify the type of relationship, set up the correct equation, and solve step by step**

**3.** What common mistake should you avoid here? → **Check the Common Mistakes section — verify your answer doesn't fall into these traps**

---

### 4.3 Conditional Statements
> 🤔 **Why does this work?** When you follow this procedure, you're exploiting a mathematical invariant — something that stays constant regardless of how you manipulate the numbers. Identifying that invariant is the key to solving problems efficiently rather than memorizing steps.


A **conditional statement** (also called an **implication**) has the form "If P, then Q" and is written symbolically as **P → Q**.

#### Structure of a Conditional Statement

| Component | Name | Role | Example |
|-----------|------|------|---------|
| P | Antecedent (hypothesis) | The condition | "If it rains" |
| Q | Consequent (conclusion) | The result | "the streets become wet" |
| P → Q | Conditional | The full statement | "If it rains, then the streets become wet." |

#### When Is a Conditional Statement True?

A conditional P → Q is **false only when P is true and Q is false**. In all other cases, it is considered true:

| P (Antecedent) | Q (Consequent) | P → Q (Conditional) |
|----------------|----------------|---------------------|
| True | True | **True** |
| True | False | **False** |
| False | True | **True** |
| False | False | **True** |

**Why is "False → True" considered true?** Because the conditional only makes a promise about what happens when P is true. If P is false, the promise is not violated regardless of Q's value. Think of it as: "If you pass the exam, I'll buy you dinner." If you don't pass the exam, I haven't broken my promise whether I buy dinner or not.

#### Recognizing Conditional Statements in Natural Language

Conditional statements don't always use "if...then" explicitly. Here are common phrasings:

| Natural Language | Logical Form |
|-----------------|--------------|
| "If P, then Q" | P → Q |
| "P implies Q" | P → Q |
| "P only if Q" | P → Q |
| "Q if P" | P → Q |
| "Q whenever P" | P → Q |
| "Q provided that P" | P → Q |
| "P is sufficient for Q" | P → Q |
| "Q is necessary for P" | P → Q |
| "All P are Q" | P → Q |

**Critical distinction — "if" vs. "only if":**
- "You pass **if** you study" means: If you study → you pass (studying guarantees passing)
- "You pass **only if** you study" means: If you pass → you studied (passing requires studying)

These are different statements! "Only if" reverses the direction.

#### Sufficient vs. Necessary Conditions

| Type | Meaning | Example |
|------|---------|---------|
| Sufficient condition | Guarantees the outcome (but isn't the only way) | "Being a square is sufficient for having four sides." (Squares have four sides, but so do rectangles.) |
| Necessary condition | Required for the outcome (but doesn't guarantee it) | "Having four sides is necessary for being a square." (You can't be a square without four sides, but four sides alone don't make a square.) |

**Workplace example:**
- "Passing the CSE is necessary for a permanent government position." (You need it, but it alone doesn't guarantee the position.)
- "Being appointed by the President is sufficient for becoming a department secretary." (The appointment guarantees the role.)

---

### 4.4 Types of Conditional Reasoning

Every conditional statement P → Q generates three related statements. Understanding which are logically valid and which are not is essential for the CSE.

#### The Four Related Conditionals

| Name | Form | Example (Original: "If it rains, the ground gets wet.") | Valid? |
|------|------|----------------------------------------------------------|--------|
| **Original (Direct)** | P → Q | If it rains, the ground gets wet. | Given as true |
| **Converse** | Q → P | If the ground is wet, it rained. | ❌ Not necessarily valid |
| **Inverse** | ¬P → ¬Q | If it doesn't rain, the ground doesn't get wet. | ❌ Not necessarily valid |
| **Contrapositive** | ¬Q → ¬P | If the ground is not wet, it didn't rain. | ✅ Always valid |

#### Why the Contrapositive Is Always Valid

The contrapositive is **logically equivalent** to the original statement. They always have the same truth value.

**Proof by example:**
- Original: "If a figure is a square, then it has four sides." (True)
- Contrapositive: "If a figure does not have four sides, then it is not a square." (Also true — guaranteed)

**Why it works:** If Q must follow from P, then the absence of Q guarantees the absence of P. If the ground isn't wet, rain couldn't have happened (assuming rain always wets the ground).

#### Why the Converse Is NOT Always Valid

The converse reverses the direction of implication. The original doesn't guarantee the reverse.

**Example showing converse failure:**
- Original: "If a figure is a square, then it has four sides." (True)
- Converse: "If a figure has four sides, then it is a square." (False — rectangles, rhombuses, and trapezoids also have four sides)

**CSE trap:** Many questions present the converse as if it were valid. If the original says "All managers attend meetings," the converse "All who attend meetings are managers" is NOT guaranteed.

#### Why the Inverse Is NOT Always Valid

The inverse negates both parts without reversing direction.

**Example showing inverse failure:**
- Original: "If it rains, the ground gets wet." (True)
- Inverse: "If it doesn't rain, the ground doesn't get wet." (False — sprinklers, flooding, or spills can wet the ground)

**Key insight:** The inverse and converse are contrapositives of each other. If one is invalid, so is the other.

#### Summary Table for Quick Reference

| Statement | Logically Equivalent To | Valid If Original Is True? |
|-----------|------------------------|---------------------------|
| Original: P → Q | Contrapositive: ¬Q → ¬P | ✅ Yes (given) |
| Contrapositive: ¬Q → ¬P | Original: P → Q | ✅ Yes (always) |
| Converse: Q → P | Inverse: ¬P → ¬Q | ❌ Not guaranteed |
| Inverse: ¬P → ¬Q | Converse: Q → P | ❌ Not guaranteed |

---

### 4.5 Valid and Invalid Conclusions
> 🤔 **Why does this work?** This shortcut works because it's a special case of the more general rule. By understanding the underlying principle, you can verify your answer logically even if you forget the exact formula under exam pressure.


A conclusion is **valid** if it follows necessarily from the given premises — there is no possible scenario where the premises are true but the conclusion is false.

#### Syllogistic Reasoning

A **syllogism** is an argument with two premises and one conclusion:

**Valid Syllogism (Modus Ponens):**
- Premise 1: All teachers are professionals.
- Premise 2: Maria is a teacher.
- Conclusion: Maria is a professional. ✅

**Why valid:** If ALL teachers are professionals (no exceptions), and Maria belongs to the group "teachers," she must also belong to the group "professionals."

**Invalid Syllogism (Undistributed Middle):**
- Premise 1: All teachers are professionals.
- Premise 2: Dr. Santos is a professional.
- Conclusion: Dr. Santos is a teacher. ❌

**Why invalid:** Being a professional doesn't require being a teacher. Doctors, engineers, and lawyers are also professionals.

#### Valid Argument Forms

| Form | Name | Structure | Example |
|------|------|-----------|---------|
| 1 | Modus Ponens | P → Q, P ∴ Q | If it rains, ground is wet. It rains. ∴ Ground is wet. |
| 2 | Modus Tollens | P → Q, ¬Q ∴ ¬P | If it rains, ground is wet. Ground is not wet. ∴ It didn't rain. |
| 3 | Hypothetical Syllogism | P → Q, Q → R ∴ P → R | If A then B. If B then C. ∴ If A then C. |
| 4 | Disjunctive Syllogism | P ∨ Q, ¬P ∴ Q | Either P or Q. Not P. ∴ Q. |

#### Invalid Argument Forms (Formal Fallacies)

| Form | Name | Structure | Why Invalid |
|------|------|-----------|-------------|
| 1 | Affirming the Consequent | P → Q, Q ∴ P | Q could be true for other reasons |
| 2 | Denying the Antecedent | P → Q, ¬P ∴ ¬Q | Q could still be true without P |

#### Testing Validity: The Counterexample Method

To test whether a conclusion is valid, try to construct a scenario where the premises are true but the conclusion is false:

**Test this argument:**
- Premise: "All government employees passed the CSE."
- Premise: "Juan passed the CSE."
- Conclusion: "Juan is a government employee."

**Counterexample:** Juan could be a reviewer, a student who passed for future use, or someone who passed but chose private employment. The premises are true, but the conclusion is false. Therefore, the argument is **invalid**.

---

### 4.6 Common Logical Fallacies

A **logical fallacy** is a reasoning error that makes an argument appear valid when it is not. CSE questions frequently use these as distractors.

#### Affirming the Consequent

**Structure:** If P, then Q. Q is true. Therefore, P is true. (INVALID)

**Example:**
- If it rains, the ground gets wet.
- The ground is wet.
- Therefore, it rained. ❌

**Why invalid:** The ground could be wet from a sprinkler, a spill, or morning dew. Rain is not the only cause of wet ground.

**CSE application:**
- If an employee is absent without leave, they receive a warning.
- Employee X received a warning.
- Therefore, Employee X was absent without leave. ❌ (The warning could be for tardiness, insubordination, etc.)

#### Denying the Antecedent

**Structure:** If P, then Q. P is false. Therefore, Q is false. (INVALID)

**Example:**
- If a student studies, the student passes.
- The student did not study.
- Therefore, the student did not pass. ❌

**Why invalid:** The student might pass through prior knowledge, guessing correctly, or other preparation methods. Not studying doesn't guarantee failure.

**CSE application:**
- If the budget is approved, the project proceeds.
- The budget was not approved.
- Therefore, the project does not proceed. ❌ (The project might proceed with alternative funding.)

#### Hasty Generalization

**Structure:** X is true in a few cases. Therefore, X is always true. (INVALID)

**Example:**
- Three employees in the office arrived late today.
- Therefore, all employees in the office are habitually late. ❌

**Why invalid:** A few instances do not establish a universal pattern. The sample is too small and may not be representative.

#### False Equivalence

**Structure:** A and B share one characteristic. Therefore, A and B are the same in all respects. (INVALID)

**Example:**
- Both managers and janitors work in the building.
- Therefore, managers and janitors have the same responsibilities. ❌

#### The Fallacy of the Undistributed Middle

**Structure:** All A are C. All B are C. Therefore, all A are B. (INVALID)

**Example:**
- All dogs are animals.
- All cats are animals.
- Therefore, all dogs are cats. ❌

**Why invalid:** Two groups can share a larger category without overlapping with each other.

---

### 4.7 Symbolic Representation of Statements

Symbolic logic uses letters and operators to represent statements concisely. This allows you to analyze logical structure without being distracted by content.

#### Basic Symbols

| Symbol | Name | Meaning | Example |
|--------|------|---------|---------|
| P, Q, R | Propositional variables | Stand for statements | P = "It is raining" |
| ¬ | Negation (NOT) | Opposite truth value | ¬P = "It is not raining" |
| ∧ | Conjunction (AND) | Both must be true | P ∧ Q = "It is raining and cold" |
| ∨ | Disjunction (OR) | At least one must be true | P ∨ Q = "It is raining or cold" |
| → | Conditional (IF...THEN) | Implication | P → Q = "If it rains, then it's cold" |
| ↔ | Biconditional (IF AND ONLY IF) | Both directions | P ↔ Q = "It rains if and only if it's cold" |

#### Truth Tables for Logical Operators

**Negation (¬P):**

| P | ¬P |
|---|-----|
| T | F |
| F | T |

**Conjunction (P ∧ Q) — true only when BOTH are true:**

| P | Q | P ∧ Q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

**Disjunction (P ∨ Q) — true when AT LEAST ONE is true:**

| P | Q | P ∨ Q |
|---|---|-------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

**Conditional (P → Q) — false only when P is true and Q is false:**

| P | Q | P → Q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

#### Translating English to Symbols

| English Statement | Symbolic Form |
|-------------------|---------------|
| "It is raining and it is cold." | P ∧ Q |
| "Either the report is late or it was not submitted." | P ∨ Q |
| "If the employee is qualified, then they are promoted." | P → Q |
| "The project is not approved." | ¬P |
| "The budget is approved if and only if the director signs." | P ↔ Q |
| "It is not the case that both conditions are met." | ¬(P ∧ Q) |
| "Neither the manager nor the supervisor approved." | ¬P ∧ ¬Q |

#### CSE-Style Symbolic Translation

**Question:** Let P = "The employee passed the evaluation" and Q = "The employee receives a bonus." Translate: "The employee does not receive a bonus unless they passed the evaluation."

**Analysis:** "Unless" means "if not." Rephrase: "If the employee did not pass the evaluation, then the employee does not receive a bonus." → ¬P → ¬Q. This is the inverse of P → Q, but "unless" in this context actually means Q → P (receiving a bonus requires passing). The safest translation: ¬P → ¬Q, which is equivalent to Q → P.

---

### 4.8 Analyzing Multiple Statements

When CSE questions provide multiple premises, you must combine them to derive a conclusion. The key technique is **chain reasoning** (hypothetical syllogism).

#### Chain Reasoning (Transitivity)

If you know P → Q and Q → R, you can conclude P → R.

**Example:**
- Premise 1: If an employee is late three times, they receive a memo.
- Premise 2: If an employee receives a memo, their performance rating drops.
- Conclusion: If an employee is late three times, their performance rating drops. ✅

**Symbolic:** (P → Q) ∧ (Q → R) → (P → R)

#### Combining Universal Statements

- Premise 1: All managers are college graduates.
- Premise 2: All college graduates passed the entrance exam.
- Conclusion: All managers passed the entrance exam. ✅

**Why valid:** The chain "manager → college graduate → passed entrance exam" is unbroken.

#### Combining Universal and Particular Statements

- Premise 1: All engineers are licensed professionals.
- Premise 2: Some licensed professionals work in government.
- Conclusion: Some engineers work in government. ❌

**Why invalid:** "Some licensed professionals work in government" doesn't specify which ones. The engineers might all be in the private sector.

#### Multi-Premise Analysis Strategy

1. **Identify the type of each premise** — universal (all/no) or particular (some)
2. **Map the chain** — which terms connect the premises?
3. **Check for breaks** — does "some" interrupt a universal chain?
4. **Test with counterexamples** — can you imagine a scenario where premises are true but the conclusion is false?

**Advanced Example:**
- Premise 1: All department heads attend the executive meeting.
- Premise 2: No one who attends the executive meeting is below Grade 24.
- Premise 3: Director Reyes is a department head.

**Valid conclusions:**
- Director Reyes attends the executive meeting. ✅ (from P1 + P3)
- Director Reyes is not below Grade 24. ✅ (from above + P2)
- No department head is below Grade 24. ✅ (from P1 + P2)

---

### 4.9 Practical Applications of Logical Statements

Logical reasoning is not abstract — it directly applies to civil service work:

#### Workplace Decision-Making

**Eligibility determination:**
- Rule: "If an applicant has at least 5 years of service AND holds a master's degree, they qualify for promotion."
- Symbolic: (P ∧ Q) → R
- Application: Check both conditions. If either is missing, the rule doesn't apply (but the applicant might qualify through other rules).

#### Government Policy Interpretation

**Conditional benefits:**
- Policy: "Employees are entitled to hazard pay only if they are assigned to conflict areas."
- Symbolic: Hazard pay → Conflict area assignment
- Meaning: Receiving hazard pay requires conflict area assignment. But being in a conflict area doesn't automatically guarantee hazard pay (other conditions may apply).

#### Legal and Procedural Analysis

**Regulatory compliance:**
- Regulation: "No government vehicle shall be used for personal purposes unless authorized by the head of office."
- Logical structure: Personal use → Authorization by head of office
- Contrapositive: No authorization → No personal use ✅

#### Administrative Reasoning

**Leave policy:**
- Rule 1: If an employee exhausts sick leave, they may use vacation leave for illness.
- Rule 2: If no leave credits remain, the absence is without pay.
- Chain: Exhausted sick leave → Use vacation leave. Exhausted all leave → Without pay.

---

### 4.10 Step-by-Step Logic Solving Strategies

#### The PCTV Method (Premises → Chain → Test → Verify)

**Step 1: PREMISES** — Read and identify all given statements. Label them.

**Step 2: CHAIN** — Connect premises that share terms. Build the logical chain.

**Step 3: TEST** — For each answer choice, ask: "Must this be true given the chain?"

**Step 4: VERIFY** — Try to construct a counterexample. If you can't, the conclusion is valid.

#### Elimination Strategy for Multiple Choice

When facing four answer choices:

1. **Eliminate contradictions** — any choice that contradicts a premise is immediately wrong
2. **Eliminate converses** — if the choice assumes the reverse of a given conditional, it's likely wrong
3. **Eliminate overstatements** — if the choice uses "all" when premises only support "some," eliminate it
4. **Eliminate irrelevant conclusions** — if the choice introduces information not in the premises, eliminate it

#### Time-Pressure Shortcuts

| Situation | Shortcut |
|-----------|----------|
| "All A are B" + "X is A" | X is B (Modus Ponens — instant valid conclusion) |
| "All A are B" + "X is not B" | X is not A (Modus Tollens — instant valid conclusion) |
| "If P then Q" + "Q is false" | P is false (Contrapositive — always valid) |
| "Some A are B" + "X is A" | Cannot conclude X is B (possibility, not certainty) |
| "All A are B" + "X is B" | Cannot conclude X is A (affirming the consequent — invalid) |

---

### 4.11 Common Errors in Logical Statements

#### Error 1: Reversing Conditional Statements

**Wrong thinking:** "If it rains, the ground gets wet" → "If the ground is wet, it rained"

**Correction:** The converse is not guaranteed. Multiple causes can produce the same effect.

#### Error 2: Assuming Converse Statements Are True

**Wrong thinking:** "All squares have four sides" → "All four-sided figures are squares"

**Correction:** The category "four-sided figures" is larger than "squares." Rectangles, rhombuses, and parallelograms also qualify.

#### Error 3: Confusing Possibility with Certainty

**Wrong thinking:** "Some employees are engineers. Juan is an employee. Therefore, Juan is an engineer."

**Correction:** "Some" means at least one, not all. Juan might or might not be an engineer.

#### Error 4: Overlooking Hidden Assumptions

**Wrong thinking:** "If the project is funded, it will succeed." (Assumes funding is the only factor.)

**Correction:** Success may require funding AND competent staff AND proper planning. Funding alone may be insufficient.

#### Error 5: Selecting Partially Correct Conclusions

**CSE trap:** An answer choice may be true in some scenarios but not guaranteed by the premises. Always choose what MUST be true, not what COULD be true.

#### Error 6: Confusing Sufficient and Necessary Conditions

| Statement | Sufficient? | Necessary? |
|-----------|-------------|------------|
| "Passing the CSE is required for permanent appointment." | No (other requirements exist) | Yes (you can't get appointed without it) |
| "A presidential appointment guarantees the position." | Yes (it's enough) | No (other paths may exist) |

---

### 4.12 Advanced Conditional Analysis

#### Nested Conditionals

Some CSE questions involve conditions within conditions:

**Example:** "If the budget is approved and the director signs, then the project proceeds only if the timeline is feasible."

**Symbolic:** (P ∧ Q) → (R → S), where:
- P = budget approved
- Q = director signs
- R = project proceeds
- S = timeline is feasible

**Meaning:** Even with budget approval and director's signature, the project proceeding still requires a feasible timeline.

#### Biconditional Statements

A biconditional (P ↔ Q) means "P if and only if Q" — both directions hold:
- P → Q (if P then Q)
- Q → P (if Q then P)

**Example:** "An employee is classified as regular if and only if they have completed probation."
- Completed probation → Regular ✅
- Regular → Completed probation ✅
- Not completed probation → Not regular ✅
- Not regular → Not completed probation ✅

#### Chains with Negation

**Example:**
- If the report is not submitted on time, the project is delayed.
- If the project is delayed, the client files a complaint.
- The client did not file a complaint.

**Chain:** ¬Submit → Delay → Complaint
**Given:** ¬Complaint
**By Modus Tollens:** ¬Complaint → ¬Delay → Submit (double contrapositive)
**Conclusion:** The report was submitted on time. ✅

---

## Mini Practice Set

**Instructions:** For each question, select the logically valid conclusion based on the given premises.

**1.** All licensed professionals passed the board exam. Dr. Cruz is a licensed professional. What can you conclude?

A) All who passed the board exam are licensed professionals
B) Dr. Cruz passed the board exam
C) Dr. Cruz is a doctor
D) Some licensed professionals did not pass the board exam

**2.** If an employee is promoted, their salary increases. Ana's salary did not increase. What can you conclude?

A) Ana was not promoted
B) Ana will never be promoted
C) Ana's salary decreased
D) Ana requested not to be promoted

**3.** Some government employees are lawyers. Pedro is a government employee. What can you conclude?

A) Pedro is a lawyer
B) Pedro is not a lawyer
C) Pedro might or might not be a lawyer
D) All government employees are lawyers

**4.** If it rains, the outdoor event is cancelled. The outdoor event was not cancelled. What can you conclude?

A) It will rain tomorrow
B) It did not rain
C) The event was moved indoors
D) The event was postponed

**5.** All managers attend the weekly briefing. All who attend the weekly briefing receive the memo. What can you conclude?

A) All who receive the memo are managers
B) All managers receive the memo
C) Some managers do not receive the memo
D) Only managers receive the memo

**6.** If P → Q and Q → R, which is valid?

A) R → P
B) P → R
C) ¬P → ¬R
D) Q → P

**7.** No student who failed the prerequisite can enroll in the advanced course. Mark enrolled in the advanced course. What can you conclude?

A) Mark is an excellent student
B) Mark did not fail the prerequisite
C) Mark will pass the advanced course
D) Mark took the prerequisite twice

**8.** If the document is classified, only authorized personnel may access it. The document is classified. What can you conclude?

A) No one can access the document
B) Only authorized personnel may access it
C) The document will be destroyed
D) Authorized personnel must access it

**9.** All birds have wings. Penguins are birds. Penguins cannot fly. What can you conclude?

A) All animals with wings can fly
B) Penguins have wings but cannot fly
C) Penguins are not really birds
D) Having wings is sufficient for flying

**10.** Either the project is approved or the funding is returned. The project is not approved. What can you conclude?

A) The project will be resubmitted
B) The funding is returned
C) The project failed review
D) No funding was allocated

**11.** If an applicant has a master's degree, they qualify for Grade 22. Liza qualifies for Grade 22. What can you conclude?

A) Liza has a master's degree
B) Liza might or might not have a master's degree
C) All Grade 22 employees have master's degrees
D) Liza applied for Grade 22

**12.** All contracts require legal review. All documents requiring legal review take at least 5 days. What can you conclude?

A) All documents take at least 5 days
B) All contracts take at least 5 days
C) Legal review always takes exactly 5 days
D) Only contracts require legal review

**13.** If the alarm sounds, evacuate the building. If you evacuate the building, proceed to the assembly area. The alarm sounded. What must you do?

A) Call the fire department
B) Proceed to the assembly area
C) Check if there is a fire
D) Wait for instructions

**14.** Some teachers are researchers. All researchers publish papers. What can you conclude?

A) All teachers publish papers
B) Some teachers publish papers
C) No teachers publish papers
D) All who publish papers are teachers

**15.** No unauthorized person may enter the restricted area. Guard Santos allowed Mr. Tan to enter the restricted area. What can you conclude?

A) Guard Santos violated protocol
B) Mr. Tan is authorized
C) Mr. Tan is a VIP
D) The restricted area is not secure

**16.** If P is true and Q is false, what is the truth value of P → Q?

A) True
B) False
C) Cannot be determined
D) Both true and false

**17.** "All employees must attend the training" is equivalent to which statement?

A) If someone is an employee, they must attend the training
B) If someone attends the training, they are an employee
C) Some employees must attend the training
D) Only employees attend the training

**18.** Which is the contrapositive of "If the store is open, customers can enter"?

A) If customers can enter, the store is open
B) If the store is closed, customers cannot enter
C) If customers cannot enter, the store is not open
D) If customers enter, the store must be open

**19.** All roses are flowers. Some flowers are red. What can you conclude?

A) All roses are red
B) Some roses are red
C) No valid conclusion about roses being red can be drawn
D) All red things are roses

**20.** If the condition P ∨ Q is true and P is false, what must be true?

A) Q is true
B) Q is false
C) Both P and Q are false
D) Cannot be determined

---

### Answers and Explanations

1. **B** — Modus Ponens: All licensed professionals passed the board exam + Dr. Cruz is a licensed professional → Dr. Cruz passed the board exam.

2. **A** — Modus Tollens: If promoted → salary increases. Salary did not increase → not promoted.

3. **C** — "Some" does not mean all. Pedro may or may not be among the lawyers.

4. **B** — Modus Tollens: If rain → cancelled. Not cancelled → no rain.

5. **B** — Chain reasoning: Managers → attend briefing → receive memo. Therefore, managers receive the memo.

6. **B** — Hypothetical Syllogism: P → Q and Q → R yields P → R.

7. **B** — Modus Tollens: Failed prerequisite → cannot enroll. Enrolled → did not fail prerequisite.

8. **B** — Direct application: Classified → only authorized personnel may access. Document is classified → only authorized personnel may access.

9. **B** — From premises: Penguins are birds → penguins have wings. Given: penguins cannot fly. Both facts coexist.

10. **B** — Disjunctive Syllogism: P ∨ Q, ¬P → Q. Project not approved → funding is returned.

11. **B** — Affirming the consequent is invalid. Liza might qualify through other means. We cannot conclude she has a master's degree.

12. **B** — Chain: Contracts → legal review → at least 5 days. Therefore, all contracts take at least 5 days.

13. **B** — Chain: Alarm → evacuate → assembly area. Alarm sounded → proceed to assembly area.

14. **B** — Some teachers are researchers + all researchers publish → some teachers publish papers.

15. **B** — The rule says no unauthorized person may enter. Santos allowed entry, so either Mr. Tan is authorized or Santos violated protocol. Given the logical structure (allowed to enter → authorized), B is the valid deduction.

16. **B** — By truth table: P → Q is false only when P is true and Q is false.

17. **A** — "All X are Y" translates to "If X, then Y."

18. **C** — Contrapositive of P → Q is ¬Q → ¬P. "If customers cannot enter, the store is not open."

19. **C** — "Some flowers are red" doesn't specify which flowers. Roses might or might not be among the red ones. No valid conclusion about roses being red.

20. **A** — Disjunctive Syllogism: P ∨ Q is true, P is false → Q must be true.

---

## Quick Recap

| Concept | Key Point |
|---------|-----------|
| Logical statement | Declarative sentence that is either true or false |
| Conditional (P → Q) | False only when P is true and Q is false |
| Contrapositive (¬Q → ¬P) | Always logically equivalent to the original |
| Converse (Q → P) | NOT guaranteed to be valid |
| Inverse (¬P → ¬Q) | NOT guaranteed to be valid |
| Modus Ponens | P → Q, P ∴ Q (valid) |
| Modus Tollens | P → Q, ¬Q ∴ ¬P (valid) |
| Affirming the Consequent | P → Q, Q ∴ P (INVALID) |
| Denying the Antecedent | P → Q, ¬P ∴ ¬Q (INVALID) |
| Chain Reasoning | P → Q, Q → R ∴ P → R (valid) |
| "All" statements | One counterexample disproves them |
| "Some" statements | One example proves them |

## Memory Aids

**CONTRAPOSITIVE = VALID** — Remember: "Contra-positive, contra-valid" — the contrapositive always matches the original.

**Converse TRAP** — "Converse = Conversation reversal = Direction reversed = NOT guaranteed"

**Modus Ponens** — "Ponens = Posit = Affirm the antecedent" → Valid
**Modus Tollens** — "Tollens = Toll = Deny the consequent" → Valid

**Fallacy Detection Mnemonic — AC/DA:**
- **A**ffirming the **C**onsequent = Invalid
- **D**enying the **A**ntecedent = Invalid

**Quantifier Quick-Check:**
- "ALL" = one exception kills it
- "SOME" = one example proves it
- "NO" = one example kills it


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
- **Why:** [Brief rationale]

**2.** [Problem 2]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**3.** [Problem 3]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**4.** [Problem 4]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**5.** [Problem 5]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]

**6.** [Problem 6]
- **Type:** [Type]
- **Answer:** [Answer]
- **Why:** [Brief rationale]


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

- **[Related Topic 1]:** [How this skill transfers or applies to that topic]
- **[Related Topic 2]:** [How understanding this concept helps with that topic]
- **[Related Topic 3]:** [Structural similarity between this and that topic]
- **[Related Topic 4]:** [How this skill is a prerequisite for that topic]
- **[Related Topic 5]:** [How both topics use similar reasoning or methods]

### Mastery Checklist
After completing this lesson, you can now:

✅ Identify logical statements and distinguish them from non-statements
✅ Determine truth values of simple and compound statements
✅ Analyze conditional statements (antecedent, consequent, truth table)
✅ Construct and evaluate converses, inverses, and contrapositives
✅ Apply Modus Ponens and Modus Tollens correctly
✅ Recognize and reject affirming the consequent and denying the antecedent
✅ Translate English statements into symbolic notation
✅ Use chain reasoning to derive conclusions from multiple premises
✅ Distinguish "must be true" from "could be true"
✅ Solve CSE-style logic questions using elimination strategies

> ?? **Why does this work?** Understanding the principle helps you choose the right method under exam pressure, even when the question format changes.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


### Mastery Checklist

- [ ] I can solve representative items accurately and quickly.
- [ ] I can explain common traps and how to avoid them.
- [ ] I can transfer this method to mixed-question sets.

