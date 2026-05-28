# Truth and Validity

## Introduction

**Truth and Validity** are two of the most fundamental — and most confused — concepts in symbolic logic. In the Philippine Civil Service Examination (CSE), questions on truth and validity test whether you can separate *what is factually accurate* from *what is logically correct*. These are not the same thing, and confusing them is the single most common error examinees make in the Analytical Ability section.

A statement is **true** if it corresponds to reality. An argument is **valid** if its conclusion follows necessarily from its premises — regardless of whether those premises are actually true in the real world. This distinction is critical: you can have a perfectly valid argument built on false premises, and you can have true conclusions reached through completely broken reasoning.

Civil servants encounter this distinction daily. A policy memo might state: "All employees who complete training are eligible for promotion. Juan completed training. Therefore, Juan is eligible for promotion." The reasoning is valid — the conclusion follows from the premises. Whether the premises are actually true (did Juan really complete training? does the policy really say that?) is a separate question entirely.

Common mistakes examinees make in truth and validity questions:
- Assuming that a believable conclusion means the argument is valid
- Assuming that absurd premises mean the argument is invalid
- Confusing "the conclusion is true" with "the argument is valid"
- Rejecting valid arguments because the premises are factually false
- Accepting invalid arguments because the conclusion happens to be true
- Overlooking contradictions hidden within premise sets
- Treating possibility as certainty when evaluating conclusions
- Importing real-world knowledge instead of reasoning strictly from given premises

This lesson builds your ability to analyze logical structure independently of factual content — the exact skill the CSE is designed to measure.

## Learning Objectives

After this lesson, you should be able to:

- Define truth and validity correctly and explain why they are independent concepts
- Distinguish valid arguments from invalid arguments based on logical structure alone
- Identify contradictions in sets of statements
- Analyze logical consistency across multiple premises systematically
- Evaluate whether a conclusion follows necessarily from given premises
- Recognize common logical fallacies disguised as valid reasoning
- Solve CSE-style validity questions efficiently under time pressure
- Eliminate incorrect answer choices using structural analysis rather than intuition

---

## 4.1 What Are Truth and Validity?

In logic, **truth** and **validity** operate at different levels of analysis. Truth applies to individual *statements*. Validity applies to entire *arguments*. Mixing these up is like confusing the quality of ingredients with the quality of a recipe — they are related but fundamentally different things.

### Truth: A Property of Statements

A **statement** (also called a proposition) is a sentence that is either true or false. It makes a claim about the world.

| Statement | True or False? | Why? |
|-----------|---------------|------|
| "Manila is the capital of the Philippines." | True | Corresponds to fact |
| "The Earth is flat." | False | Contradicts established fact |
| "All government employees pay taxes." | True | Required by law |
| "Water boils at 50°C at sea level." | False | Contradicts physical reality |

Truth is about **factual accuracy** — does the statement match reality?

### Validity: A Property of Arguments

An **argument** is a set of statements (premises) offered in support of another statement (conclusion). Validity is about the *logical relationship* between premises and conclusion.

An argument is **valid** if and only if: it is impossible for all premises to be true while the conclusion is false.

Put differently: in a valid argument, IF the premises are true, the conclusion MUST be true. There is no escape — the conclusion is guaranteed by the logical structure.

| Argument | Valid? | Why? |
|----------|--------|------|
| All managers are employees. Carla is a manager. Therefore, Carla is an employee. | ✅ Valid | Conclusion is guaranteed by premises |
| All fish can fly. Tuna is a fish. Therefore, tuna can fly. | ✅ Valid | Structure is correct (premises are false, but that's irrelevant to validity) |
| All doctors are educated. Maria is educated. Therefore, Maria is a doctor. | ❌ Invalid | Conclusion is not guaranteed — Maria could be educated without being a doctor |

### The Key Insight

**Validity is about structure, not content.** You evaluate validity by asking: "Given the *form* of this argument, could the premises be true and the conclusion false?" You do NOT ask: "Are the premises actually true in the real world?"

This is why the "fish can fly" argument above is valid. The structure is:
1. All A are B.
2. X is an A.
3. Therefore, X is a B.

This structure guarantees the conclusion regardless of what A, B, and X represent. Whether we're talking about fish, managers, or unicorns — the logical form is airtight.

**CSE Trap:** Many exam questions present arguments with obviously false premises to test whether you can separate truth from validity. If you reject a valid argument because its premises are absurd, you've fallen into the trap.

> 🤔 **Why does this work?** Validity is structure-dependent because logical form is what preserves truth across all possible interpretations. When you test validity, you're asking: "Is there ANY interpretation where the premises are true but the conclusion is false?" If no such interpretation exists, the form itself guarantees truth-preservation — regardless of what the variables represent. This is why you can evaluate validity using abstract letters (All A are B; X is A; therefore X is B) without knowing what A, B, or X stand for. The form does the logical work; the content is irrelevant to the structural guarantee.

---

## 4.2 True Statements vs Valid Arguments

The independence of truth and validity creates four possible combinations. Understanding all four is essential for CSE success.

### The Four Combinations

| Premises | Structure | Conclusion | Classification |
|----------|-----------|------------|----------------|
| True | Valid | True | Sound argument (the gold standard) |
| False | Valid | May be true or false | Valid but unsound |
| True | Invalid | May be true or false | Invalid argument with true premises |
| False | Invalid | May be true or false | Invalid and unsound |

### Combination 1: True Premises + Valid Structure = Sound Argument

This is the ideal. The premises are factually correct AND the logic is airtight, so the conclusion is guaranteed to be true.

**Example:**
- All Philippine senators serve six-year terms. (True)
- Risa Hontiveros is a Philippine senator. (True)
- Therefore, Risa Hontiveros serves a six-year term. (True — and guaranteed)

A **sound** argument is one that is both valid AND has true premises. Soundness guarantees a true conclusion.

### Combination 2: False Premises + Valid Structure

The premises are factually wrong, but the logical structure is correct. The conclusion may or may not be true — validity alone cannot guarantee truth when premises are false.

**Example (conclusion happens to be false):**
- All fish can fly. (False)
- A shark is a fish. (True)
- Therefore, a shark can fly. (False)

The argument is VALID — the structure guarantees that IF all fish could fly and a shark is a fish, THEN a shark could fly. The structure works perfectly. The conclusion is false only because a premise is false.

**Example (conclusion happens to be true):**
- All mammals can fly. (False)
- All bats are mammals. (True)
- Therefore, all bats can fly. (True!)

Valid structure, false premise, but the conclusion is accidentally true. This does NOT make the argument sound — it's just a coincidence.

### Combination 3: True Premises + Invalid Structure

The premises are factually correct, but the reasoning is broken. The conclusion might be true, but it's not guaranteed by the premises.

**Example:**
- All teachers are professionals. (True)
- Dr. Santos is a professional. (True)
- Therefore, Dr. Santos is a teacher. (Not guaranteed — could be a doctor, lawyer, engineer)

Both premises are true. The conclusion might even be true (maybe Dr. Santos IS a teacher). But the argument is INVALID because the conclusion doesn't follow from the premises. Dr. Santos could be any kind of professional.

### Combination 4: False Premises + Invalid Structure

Everything is broken — false premises and bad logic.

**Example:**
- All birds are mammals. (False)
- All mammals live underwater. (False)
- Therefore, all fish are birds. (False, and doesn't even follow)

**CSE Strategy:** When evaluating validity, mentally replace the content with abstract symbols. If the structure works with ANY content, it's valid. If you can find ANY substitution where premises are true but conclusion is false, it's invalid.

---

## 4.3 Valid Arguments

A valid argument has one defining characteristic: **it is impossible for the premises to be true and the conclusion false simultaneously.** The conclusion is locked in by the logical structure — there is no scenario, no interpretation, no possible world where the premises hold but the conclusion fails.

### Characteristics of Valid Arguments

1. **Structural guarantee** — the conclusion follows from the form of the argument, not from the specific content
2. **No escape** — you cannot construct a counterexample where premises are true but conclusion is false
3. **Preservation of truth** — if truth goes in (true premises), truth must come out (true conclusion)
4. **Content-independence** — validity holds regardless of subject matter

### Common Valid Argument Forms

| Form Name | Structure | Example |
|-----------|-----------|---------|
| Modus Ponens | If P then Q. P. Therefore Q. | If it rains, roads are wet. It rains. Therefore, roads are wet. |
| Modus Tollens | If P then Q. Not Q. Therefore not P. | If it rains, roads are wet. Roads are not wet. Therefore, it did not rain. |
| Hypothetical Syllogism | If P then Q. If Q then R. Therefore if P then R. | If it rains, roads are wet. If roads are wet, traffic slows. Therefore, if it rains, traffic slows. |
| Disjunctive Syllogism | P or Q. Not P. Therefore Q. | The report is approved or rejected. It is not approved. Therefore, it is rejected. |
| Universal Instantiation | All A are B. X is an A. Therefore X is a B. | All teachers are professionals. Anna is a teacher. Therefore, Anna is a professional. |

### Easy Examples

**Example 1:**
- All government employees have IDs.
- Juan is a government employee.
- Therefore, Juan has an ID.

**Why valid:** Juan belongs to the category "government employees," and ALL members of that category have IDs. There is no way Juan can be a government employee without having an ID, given the first premise.

**Example 2:**
- If the office is closed, no transactions are processed.
- The office is closed.
- Therefore, no transactions are processed.

**Why valid:** Modus ponens — the condition is met, so the consequence must follow.

### Medium Examples

**Example 3:**
- All applicants who pass the exam are interviewed.
- All applicants who are interviewed submit additional documents.
- Rosa passed the exam.
- Therefore, Rosa submits additional documents.

**Why valid:** Chain reasoning (hypothetical syllogism + universal instantiation). Pass exam → interviewed → submit documents. Rosa passed, so she must submit documents.

**Example 4:**
- No employee on suspension may access the building.
- Mr. Reyes is on suspension.
- Therefore, Mr. Reyes may not access the building.

**Why valid:** Universal negative applied to a specific case. If NO suspended employees may access the building, and Reyes is suspended, then Reyes may not access it.

### Advanced Examples

**Example 5:**
- All projects exceeding ₱5 million require board approval.
- All projects requiring board approval undergo public consultation.
- The highway expansion project exceeds ₱5 million.
- Therefore, the highway expansion project undergoes public consultation.

**Why valid:** Three-step chain. Exceeds ₱5M → board approval → public consultation. The highway project exceeds ₱5M, so it must undergo public consultation.

**Example 6:**
- If a regulation is unconstitutional, it is void.
- If a regulation is void, agencies cannot enforce it.
- Regulation 2024-05 is unconstitutional.
- Therefore, agencies cannot enforce Regulation 2024-05.

**Why valid:** Hypothetical syllogism + modus ponens. Unconstitutional → void → unenforceable. The regulation is unconstitutional, so it is unenforceable.

**CSE Tip:** When you see a chain of "if-then" statements, trace the links. If the first condition is satisfied and every link connects, the final conclusion is valid.

---

## 4.4 Invalid Arguments

An argument is **invalid** when it is possible for the premises to be true while the conclusion is false. The conclusion might sound reasonable, might even be true in the real world — but it is not *guaranteed* by the premises. That gap between "sounds right" and "logically guaranteed" is exactly where CSE questions live.

### Characteristics of Invalid Arguments

1. **Logical gap** — the conclusion goes beyond what the premises support
2. **Counterexample exists** — you can imagine a scenario where premises are true but conclusion is false
3. **Hidden assumptions** — the argument requires unstated information to work
4. **Structure failure** — the form of the argument does not preserve truth

### Common Invalid Argument Forms

| Form Name | Structure | Why Invalid |
|-----------|-----------|-------------|
| Affirming the Consequent | If P then Q. Q. Therefore P. | Q could be true for other reasons |
| Denying the Antecedent | If P then Q. Not P. Therefore not Q. | Q might still be true through another path |
| Undistributed Middle | All A are C. All B are C. Therefore All A are B. | A and B could be different subsets of C |
| Illicit Conversion | All A are B. Therefore All B are A. | B is typically larger than A |
| Hasty Generalization | Some A are B. Therefore All A are B. | "Some" does not imply "all" |

### Easy Examples

**Example 1:**
- All doctors are educated.
- Maria is educated.
- Therefore, Maria is a doctor.

**Why invalid:** Maria could be educated without being a doctor — she could be a lawyer, teacher, engineer, or any other educated person. The premises don't eliminate these possibilities.

**Counterexample:** Imagine Maria is a lawyer. Both premises remain true (all doctors are still educated, and Maria is still educated), but the conclusion is false. Therefore, the argument is invalid.

**Example 2:**
- If it rains, the ground is wet.
- The ground is wet.
- Therefore, it rained.

**Why invalid:** The ground could be wet from a sprinkler, a burst pipe, or morning dew. Rain is sufficient for wet ground, but not necessary.

### Medium Examples

**Example 3:**
- All Civil Service passers are eligible for government positions.
- Pedro is eligible for a government position.
- Therefore, Pedro is a Civil Service passer.

**Why invalid:** Pedro might be eligible through other means — presidential appointment, elective office, or exemption provisions. Passing the CSE is one path to eligibility, not the only path.

**Example 4:**
- If an employee is absent without leave, a memo is issued.
- No memo was issued to Ana.
- Therefore, Ana was not absent without leave.

**Why valid (trick!):** This is actually modus tollens — a VALID form. If P then Q; not Q; therefore not P. Don't confuse this with denying the antecedent.

### Advanced Examples

**Example 5:**
- All licensed professionals passed a board exam.
- All doctors are licensed professionals.
- Mr. Cruz passed a board exam.
- Therefore, Mr. Cruz is a doctor.

**Why invalid:** Mr. Cruz could be any licensed professional who passed a board exam — a nurse, engineer, accountant, or architect. The premises establish that doctors are a subset of licensed professionals, but passing a board exam doesn't place someone specifically in the doctor subset.

**Example 6:**
- If the budget is approved, the project proceeds.
- The budget was not approved.
- Therefore, the project does not proceed.

**Why invalid:** This is denying the antecedent. The project might proceed through emergency funding, reallocation, or external grants. Budget approval is sufficient for the project to proceed, but the project might proceed without it.

**CSE Strategy:** When evaluating an argument, ask yourself: "Can I imagine a situation where all the premises are true but the conclusion is false?" If yes — even one scenario — the argument is invalid.

---

## 4.5 Contradictions

A **contradiction** occurs when two or more statements cannot all be true at the same time. They are mutually inconsistent — accepting one forces you to reject the other. Contradictions are logically impossible situations.

### What Makes a Contradiction

A set of statements is contradictory when:
- One statement directly negates another
- The statements together imply an impossibility
- No possible situation makes all statements true simultaneously

### Types of Contradictions

#### Direct Contradiction (Explicit Negation)

Two statements where one is the exact negation of the other:

| Statement A | Statement B | Contradiction? |
|-------------|-------------|---------------|
| "The office is open." | "The office is not open." | ✅ Yes |
| "All employees attended." | "Some employees did not attend." | ✅ Yes |
| "No reports were filed." | "At least one report was filed." | ✅ Yes |
| "The meeting is on Monday." | "The meeting is on Tuesday." | ✅ Yes (implicit — can't be both) |

#### Internal Inconsistency (Implied Contradiction)

Statements that don't directly negate each other but together create an impossible situation:

**Example 1:**
- "All team members are present."
- "Juan is a team member."
- "Juan is absent."

These three statements cannot all be true. If all team members are present and Juan is a team member, then Juan must be present — but the third statement says he's absent. Contradiction.

**Example 2:**
- "No employee may work more than 8 hours without overtime pay."
- "Maria worked 10 hours today."
- "Maria did not receive overtime pay."

If the policy applies and Maria worked 10 hours, she must receive overtime pay. The third statement contradicts what the first two together require.

**Example 3:**
- "All applicants must be at least 21 years old."
- "Carlos is an applicant."
- "Carlos is 19 years old."

Carlos cannot simultaneously be an applicant (which requires being 21+) and be 19 years old. The statements are internally inconsistent.

### Easy Examples

**Contradiction:**
- "The document is classified."
- "The document is available to the public."

If classified means restricted from public access, these cannot both be true.

**Not a contradiction:**
- "Some employees are late."
- "Some employees are on time."

These are perfectly compatible — different employees can have different arrival times.

### Medium Examples

**Contradiction:**
- "All Division Chiefs submitted their reports on time."
- "Mr. Reyes is a Division Chief."
- "Mr. Reyes submitted his report late."

**Not a contradiction:**
- "Most employees prefer flexible hours."
- "Some employees prefer fixed schedules."

These are compatible — "most" leaves room for "some" to differ.

### Advanced Examples

**Contradiction:**
- "If a project exceeds budget, it requires re-approval."
- "Project Alpha exceeds budget."
- "Project Alpha does not require re-approval."
- "All policies are enforced without exception."

The first three statements alone form a contradiction (given the conditional). The fourth statement reinforces it by eliminating any escape through non-enforcement.

**Not a contradiction (tricky):**
- "All managers attend meetings."
- "Not all employees attend meetings."

These are compatible — managers are a subset of employees. All managers can attend while some non-manager employees do not.

### Why Contradictions Matter

1. **A contradictory set of premises can "prove" anything.** In formal logic, from a contradiction, any conclusion follows (the principle of explosion). This means contradictory premises make an argument trivially valid but meaningless.
2. **CSE questions test your ability to spot hidden contradictions** in sets of statements.
3. **Contradictions signal errors in reasoning** — if your premises lead to a contradiction, at least one premise must be false.

**CSE Tip:** When a question asks "Which set of statements is contradictory?" look for statements that, taken together, create an impossible situation. Check whether universal claims conflict with specific cases.

---

## 4.6 Types of Logical Errors

Logical errors (fallacies) are patterns of invalid reasoning that appear convincing on the surface. CSE questions deliberately use these as distractors — answer choices that "feel right" but fail under logical analysis.

### Affirming the Consequent

**Structure:** If P then Q. Q is true. Therefore P is true.

**Why it fails:** Q might be true for reasons other than P. P is sufficient for Q, but not necessary.

**Easy example:**
- If it rains, the ground is wet.
- The ground is wet.
- Therefore, it rained. ❌

The ground could be wet from a garden hose, a spill, or condensation.

**Medium example:**
- If an employee passes the evaluation, they receive a bonus.
- Mr. Torres received a bonus.
- Therefore, Mr. Torres passed the evaluation. ❌

Mr. Torres might have received a bonus for perfect attendance, years of service, or a special award — not necessarily from passing the evaluation.

**Advanced example:**
- If a municipality achieves zero open defecation, it receives a sanitation award.
- Municipality X received a sanitation award.
- Therefore, Municipality X achieved zero open defecation. ❌

The award might have multiple qualifying criteria, or the municipality might have received a different category of sanitation award.

### Denying the Antecedent

**Structure:** If P then Q. P is false. Therefore Q is false.

**Why it fails:** Q might still be true through a different cause or condition.

**Easy example:**
- If you study, you will pass.
- You did not study.
- Therefore, you will not pass. ❌

You might pass through prior knowledge, lucky guessing, or natural aptitude.

**Medium example:**
- If the director approves, the project continues.
- The director did not approve.
- Therefore, the project does not continue. ❌

The project might continue through emergency authorization, acting director approval, or automatic continuation provisions.

**Advanced example:**
- If the procurement follows standard bidding, it is valid.
- The procurement did not follow standard bidding.
- Therefore, the procurement is not valid. ❌

The procurement might be valid through alternative methods: negotiated procurement, emergency purchase, or small-value procurement — all legitimate alternatives to standard bidding under Philippine procurement law.

### Circular Reasoning (Begging the Question)

**Structure:** P is true because Q. Q is true because P.

**Why it fails:** The conclusion is assumed in the premises — no new information is provided.

**Example:**
- "This policy is effective because it produces good results."
- "It produces good results because it is an effective policy."

The reasoning goes in a circle — neither statement provides independent support for the other.

### Overgeneralization (Hasty Generalization)

**Structure:** Some A are B. Therefore, all A are B.

**Why it fails:** A sample does not represent the whole unless proven.

**Example:**
- Some government offices close at 5:00 PM.
- Therefore, all government offices close at 5:00 PM. ❌

Some offices have extended hours, 24-hour operations, or different schedules.

### The Fallacy of the Undistributed Middle

**Structure:** All A are C. All B are C. Therefore, A and B are related.

**Why it fails:** Two groups can share a property without overlapping.

**Example:**
- All nurses are healthcare workers.
- All doctors are healthcare workers.
- Therefore, all nurses are doctors. ❌

Nurses and doctors are both healthcare workers but are distinct professions.

---

## 4.7 Testing Validity

Testing validity requires a systematic method — intuition is unreliable because invalid arguments often "feel" correct. Here are proven methods for determining whether an argument is valid.

### Method 1: The Counterexample Test

The most powerful method. To show an argument is INVALID, find one scenario where:
- All premises are true
- The conclusion is false

If such a scenario exists, the argument is invalid. If no such scenario is possible, the argument is valid.

**Example to test:**
- All teachers are college graduates.
- Ana is a college graduate.
- Therefore, Ana is a teacher.

**Counterexample:** Ana is an engineer (a college graduate who is not a teacher). Both premises remain true, but the conclusion is false. → INVALID.

**Example to test:**
- All managers must attend the meeting.
- Carlos is a manager.
- Therefore, Carlos must attend the meeting.

**Attempt counterexample:** Can Carlos be a manager who doesn't have to attend? No — the first premise says ALL managers must attend, with no exceptions. → VALID.

### Method 2: Logical Form Analysis

Strip the content and examine the abstract structure:

**Original:** "All nurses are licensed. Maria is licensed. Therefore, Maria is a nurse."

**Abstract form:** All A are B. X is B. Therefore X is A.

**Test the form:** All dogs are animals. A cat is an animal. Therefore, a cat is a dog. → Obviously false with true premises. → INVALID form.

### Method 3: Diagram Verification

Draw the relationships:

**Valid argument:**
```
┌─────────────────────┐
│    College Grads (B) │
│  ┌───────────┐      │
│  │Teachers(A)│      │
│  │  • Ana    │      │
│  └───────────┘      │
└─────────────────────┘
```
If Ana is in Teachers, she MUST be in College Grads. Valid.

**Invalid argument:**
```
┌─────────────────────┐
│    College Grads (B) │
│  ┌──────┐  • Ana   │
│  │Teach.│           │
│  │ (A)  │           │
│  └──────┘           │
└─────────────────────┘
```
Ana can be in College Grads without being in Teachers. Invalid.

### Method 4: Truth Table Approach (for conditional arguments)

For arguments involving if-then statements, check all possible truth combinations:

**Modus Ponens (Valid):**

| P | Q | P → Q | Given P is true and P → Q is true | Q must be? |
|---|---|-------|-----------------------------------|-----------|
| T | T | T | ✅ Consistent | True |
| T | F | F | ❌ P → Q would be false — not possible | — |

Only one consistent row exists, and Q is true in it. → Valid.

**Affirming the Consequent (Invalid):**

| P | Q | P → Q | Given Q is true and P → Q is true | P must be? |
|---|---|-------|-----------------------------------|-----------|
| T | T | T | ✅ Consistent | True |
| F | T | T | ✅ Consistent | False |

Two consistent rows exist — P can be either true or false. → Invalid.

### Practice: Test These Arguments

**Argument A:**
- If the alarm sounds, evacuate the building.
- The alarm sounded.
- Therefore, evacuate the building.

**Analysis:** Modus ponens. P → Q, P, therefore Q. → **VALID**

**Argument B:**
- All certified accountants passed the CPA exam.
- Mr. Lim passed the CPA exam.
- Therefore, Mr. Lim is a certified accountant.

**Analysis:** All A are B. X is B. Therefore X is A. Affirming the consequent with categories. → **INVALID** (Mr. Lim might have passed but not completed other certification requirements, or might not have applied for certification.)

**Argument C:**
- No unauthorized person may enter the restricted area.
- The janitor is not authorized.
- Therefore, the janitor may not enter the restricted area.

**Analysis:** No non-A may do B. X is non-A. Therefore X may not do B. → **VALID** (the janitor falls in the "unauthorized" category, which is excluded from entry.)

---

## 4.8 Symbolic Representation of Arguments

Translating arguments into symbols strips away misleading content and reveals the bare logical structure. This makes validity testing mechanical rather than intuitive.

### Basic Symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| P, Q, R | Propositions (statements) | P = "It rains" |
| → | "If...then" (conditional) | P → Q = "If it rains, then roads are wet" |
| ∧ | "And" (conjunction) | P ∧ Q = "It rains and roads are wet" |
| ∨ | "Or" (disjunction) | P ∨ Q = "It rains or roads are wet" |
| ¬ | "Not" (negation) | ¬P = "It does not rain" |
| ∴ | "Therefore" (conclusion) | ∴ Q = "Therefore, roads are wet" |

### Translating Arguments to Symbols

**Example 1 (Modus Ponens):**
- If it rains, the ground is wet. → P → Q
- It rains. → P
- Therefore, the ground is wet. → ∴ Q

**Symbolic form:** P → Q, P ∴ Q — **VALID**

**Example 2 (Modus Tollens):**
- If the employee is qualified, they are promoted. → P → Q
- The employee was not promoted. → ¬Q
- Therefore, the employee is not qualified. → ∴ ¬P

**Symbolic form:** P → Q, ¬Q ∴ ¬P — **VALID**

**Example 3 (Affirming the Consequent):**
- If it rains, the ground is wet. → P → Q
- The ground is wet. → Q
- Therefore, it rained. → ∴ P

**Symbolic form:** P → Q, Q ∴ P — **INVALID**

**Example 4 (Denying the Antecedent):**
- If you study, you pass. → P → Q
- You did not study. → ¬P
- Therefore, you did not pass. → ∴ ¬Q

**Symbolic form:** P → Q, ¬P ∴ ¬Q — **INVALID**

**Example 5 (Hypothetical Syllogism):**
- If the budget is approved, construction begins. → P → Q
- If construction begins, jobs are created. → Q → R
- Therefore, if the budget is approved, jobs are created. → ∴ P → R

**Symbolic form:** P → Q, Q → R ∴ P → R — **VALID**

### Advanced Symbolic Analysis

**Example 6 (Disjunctive Syllogism):**
- The report is either approved or returned for revision. → P ∨ Q
- The report was not approved. → ¬P
- Therefore, the report was returned for revision. → ∴ Q

**Symbolic form:** P ∨ Q, ¬P ∴ Q — **VALID**

**Example 7 (Constructive Dilemma):**
- If it rains, we stay inside. If it's sunny, we go to the park. → (P → Q) ∧ (R → S)
- It either rains or it's sunny. → P ∨ R
- Therefore, we either stay inside or go to the park. → ∴ Q ∨ S

**Symbolic form:** (P → Q) ∧ (R → S), P ∨ R ∴ Q ∨ S — **VALID**

**CSE Tip:** When you see a complex argument, assign letters to each distinct proposition and write out the symbolic form. The pattern will often match a known valid or invalid form, giving you the answer immediately.

---

## 4.9 Practical Applications of Validity

Understanding truth and validity isn't just exam preparation — it's a professional skill that civil servants use daily when interpreting policies, evaluating proposals, and making decisions.

### Workplace Decision-Making

**Eligibility Determination:**
- Policy: "All applicants with a master's degree qualify for Salary Grade 18."
- Fact: "Ms. Reyes has a master's degree."
- Valid conclusion: "Ms. Reyes qualifies for Salary Grade 18."
- Invalid conclusion: "Ms. Reyes is the only one who qualifies." (The policy doesn't say that.)

**Access Control:**
- Policy: "If an employee has security clearance Level 3, they may access classified files."
- Fact: "Mr. Santos does not have Level 3 clearance."
- Invalid conclusion: "Mr. Santos may not access classified files." (He might have Level 4 or 5, which presumably also grants access.)
- Valid conclusion: We cannot determine Mr. Santos's access from these premises alone.

### Government Policy Evaluation

**Budget Analysis:**
- "All departments that exceeded their budget must submit justification reports."
- "The Department of Health exceeded its budget."
- Valid: "The Department of Health must submit a justification report."
- Invalid: "Only the Department of Health exceeded its budget." (Other departments might have too.)

**Personnel Decisions:**
- "No employee with pending administrative cases may be promoted."
- "Officer Dela Cruz has a pending administrative case."
- Valid: "Officer Dela Cruz may not be promoted."
- Invalid: "Officer Dela Cruz will be terminated." (The policy only restricts promotion, not employment.)

### Legal Reasoning

**Regulatory Interpretation:**
- "If a business operates without a permit, it shall be closed."
- "Business X was closed."
- Invalid: "Business X operated without a permit." (It might have been closed for other reasons — health violations, structural hazards, etc.)

**Administrative Procedures:**
- "All FOIA requests must be responded to within 15 working days."
- "The agency did not respond within 15 working days."
- Valid: "The agency violated the FOIA requirement."

### Project Management

**Risk Assessment:**
- "If the contractor fails to deliver by the deadline, liquidated damages apply."
- "The contractor delivered on time."
- Invalid: "Liquidated damages do not apply." (They might apply for quality issues or other contract violations.)
- What we can say: The deadline-based trigger for liquidated damages was not activated.

---

## 4.10 Step-by-Step Validity Analysis Strategies

When facing a validity question on the CSE, follow this systematic approach rather than relying on gut feeling.

### The 5-Step Validity Check

**Step 1: Identify the premises and conclusion.**
Separate what is given (premises) from what is claimed to follow (conclusion). The conclusion often starts with "therefore," "hence," "so," or "it follows that."

**Step 2: Determine the logical form.**
Translate the argument into abstract structure. Replace specific content with letters (P, Q, A, B, X).

**Step 3: Check for known valid/invalid patterns.**
Compare the abstract form against the standard patterns:
- Modus Ponens (P → Q, P ∴ Q) — Valid
- Modus Tollens (P → Q, ¬Q ∴ ¬P) — Valid
- Affirming the Consequent (P → Q, Q ∴ P) — Invalid
- Denying the Antecedent (P → Q, ¬P ∴ ¬Q) — Invalid
- Universal Instantiation (All A are B, X is A ∴ X is B) — Valid
- Illicit Conversion (All A are B ∴ All B are A) — Invalid

**Step 4: Apply the counterexample test.**
If the form doesn't match a known pattern, try to construct a scenario where premises are true but conclusion is false. If you succeed → invalid. If you cannot → valid.

**Step 5: Verify your answer.**
Re-read the argument with your determination. Does it make logical sense? Did you misidentify any component?

### Time-Pressure Shortcuts

**Shortcut 1: Direction Check**
If the conclusion reverses the direction of a premise (e.g., premise says "All A are B" but conclusion says "X is A" based on X being B), it's almost certainly invalid.

**Shortcut 2: The "Could Be Otherwise" Test**
Ask: "Could the conclusion be false while everything stated in the premises remains true?" If yes → invalid. This takes 5 seconds and catches most errors.

**Shortcut 3: Scope Escalation Flag**
If the premises use "some" but the conclusion uses "all" (or premises are about a subset but conclusion is about the whole set), flag it as likely invalid.

**Shortcut 4: Negative Premise Rule**
If both premises are negative (No A are B, No B are C), no valid standard conclusion connects A and C. Eliminate any answer that claims such a connection.

**Shortcut 5: The Substitution Test**
Replace the content with something familiar. "All A are B, X is B, therefore X is A" becomes "All cats are animals, Rex is an animal, therefore Rex is a cat." If the substituted version is obviously wrong, the original is invalid too.

---

## 4.11 Common Errors in Truth and Validity Questions

These are the specific traps CSE question writers use. Knowing them in advance gives you a significant advantage.

### Error 1: Confusing Truth with Validity

**The trap:** An argument has a true conclusion, so examinees mark it as "valid."

**Reality:** A true conclusion can come from invalid reasoning. "All birds can fly. Penguins are birds. Therefore, penguins can fly" has a false conclusion from a valid structure. "All dogs are animals. My pet is an animal. Therefore, my pet is a dog" might have a true conclusion (if your pet IS a dog) but the reasoning is invalid.

**Defense:** Ignore whether the conclusion is actually true. Focus only on whether it MUST be true given the premises.

### Error 2: Rejecting Valid Arguments with False Premises

**The trap:** The premises are obviously false ("All fish can fly"), so examinees mark the argument as "invalid."

**Reality:** Validity is about structure, not factual accuracy. An argument with absurd premises can still be perfectly valid.

**Defense:** When you see ridiculous premises, that's a signal to focus purely on structure. The question is testing whether you can separate truth from validity.

### Error 3: Accepting Believable but Unsupported Conclusions

**The trap:** The conclusion sounds reasonable and is probably true in real life, so examinees accept it as valid.

**Example:** "Most government employees are honest. Juan is a government employee. Therefore, Juan is honest."

**Reality:** "Most" doesn't guarantee anything about a specific individual. Juan might be in the dishonest minority. The conclusion is not logically guaranteed.

**Defense:** Ask: "Is there ANY scenario where the premises are true but the conclusion is false?" If yes, it's invalid — regardless of how likely the conclusion seems.

### Error 4: Overlooking Hidden Contradictions

**The trap:** A set of statements seems consistent on first reading, but contains a buried contradiction.

**Example:**
- "All team leaders submitted reports by Friday."
- "Ms. Garcia is a team leader."
- "No reports were received before Saturday."

On quick reading, these might seem fine. But together they're contradictory: if all team leaders submitted by Friday, and Ms. Garcia is a team leader, then at least one report (hers) was received by Friday — contradicting "no reports were received before Saturday."

**Defense:** For contradiction questions, test each pair and triple of statements for consistency. Check whether universal claims conflict with specific cases.

### Error 5: Confusing Possibility with Certainty

**The trap:** The conclusion COULD be true given the premises, so examinees mark it as valid.

**Reality:** Validity requires that the conclusion MUST be true — not that it could be, might be, or probably is.

**Example:** "Some employees are managers. Some managers earn high salaries. Therefore, some employees earn high salaries."

This COULD be true, but it's not guaranteed. The "some employees" who are managers might not be the "some managers" who earn high salaries.

**Defense:** "Could be true" ≠ "must be true." Valid means guaranteed, not possible.

---

## 4.12 Advanced Validity and Contradiction Analysis

### Compound Arguments

Real CSE questions often combine multiple logical forms in a single argument. Analyze these by breaking them into component steps.

**Example:**
- If the project is approved, funding is released. (P → Q)
- If funding is released, construction begins. (Q → R)
- If construction begins, jobs are created. (R → S)
- The project is approved. (P)
- Therefore, jobs are created. (∴ S)

**Analysis:** Chain of hypothetical syllogisms + modus ponens.
- P → Q, Q → R gives P → R (hypothetical syllogism)
- P → R, R → S gives P → S (hypothetical syllogism)
- P → S, P gives S (modus ponens)
- **VALID**

### Nested Contradictions

**Example:**
- "All employees in Department A work Monday through Friday."
- "No employee in Department A works on weekends."
- "Mr. Cruz is in Department A."
- "Mr. Cruz worked last Saturday."

**Analysis:** Statements 1 and 2 are consistent with each other (they reinforce the same point). Statement 3 places Mr. Cruz in Department A. Statement 4 says he worked Saturday (a weekend). But statements 1-2 establish that Department A employees don't work weekends. Contradiction between {1, 2, 3} and {4}.

### Multi-Premise Validity Testing

**Example:**
- All licensed professionals passed a board exam. (A → B)
- All who passed a board exam studied for at least one year. (B → C)
- All who studied for at least one year have college degrees. (C → D)
- Dr. Reyes is a licensed professional. (Dr. Reyes ∈ A)
- Therefore, Dr. Reyes has a college degree. (∴ Dr. Reyes ∈ D)

**Analysis:** A → B → C → D. Dr. Reyes ∈ A. Therefore Dr. Reyes ∈ D. **VALID** — the chain is unbroken.

**Contrast (Invalid version):**
- All licensed professionals passed a board exam. (A → B)
- All who passed a board exam studied for at least one year. (B → C)
- Ms. Santos studied for at least one year. (Ms. Santos ∈ C)
- Therefore, Ms. Santos is a licensed professional. (∴ Ms. Santos ∈ A)

**Analysis:** A → B → C. Ms. Santos ∈ C. This does NOT mean Ms. Santos ∈ A. She could have studied for a year for reasons unrelated to board exams or licensing. **INVALID** — reasoning backward through the chain.

### Complex Contradiction Detection

**Set of statements:**
1. "If an employee is promoted, their salary increases."
2. "If an employee's salary increases, they move to a higher tax bracket."
3. "Officer Mendoza was promoted."
4. "Officer Mendoza's tax bracket did not change."

**Analysis:**
- From 1 and 3: Officer Mendoza's salary increases (modus ponens)
- From 2 and "salary increases": Officer Mendoza moves to a higher tax bracket (modus ponens)
- But statement 4 says the tax bracket didn't change
- **CONTRADICTION** between the derived conclusion and statement 4

---

## Exam Strategies

- **Read the question stem first.** Know whether you're being asked to identify a valid argument, an invalid argument, or a contradiction before reading the choices.
- **Translate to symbols immediately.** Don't get distracted by content. Convert to P → Q form and match against known patterns.
- **Use the substitution test for speed.** Replace abstract content with concrete, familiar examples to quickly see if the structure works.
- **Eliminate obviously invalid choices first.** In multiple-choice, removing 2 wrong answers makes the remaining decision much easier.
- **Watch for direction reversals.** The most common CSE trap is presenting the converse of a valid argument as if it were valid.
- **Don't import outside knowledge.** The question asks what follows from the GIVEN premises, not what you know about the real world.
- **Check for scope changes.** If premises say "some" but the conclusion says "all," it's almost certainly invalid.
- **Time allocation:** Spend no more than 45-60 seconds per validity question. If you can't determine validity in that time, use elimination and move on.

---

## Mini Practice Set

**1.** All engineers are problem-solvers. Marco is an engineer. Therefore, Marco is a problem-solver.
**Answer:** Valid
**Explanation:** Universal instantiation — Marco belongs to the category "engineers," and all engineers are problem-solvers, so Marco must be a problem-solver.

**2.** If it is Monday, the office is open. The office is open. Therefore, it is Monday.
**Answer:** Invalid
**Explanation:** Affirming the consequent — the office could be open on other days too (Tuesday through Friday).

**3.** All voters are citizens. Pedro is a citizen. Therefore, Pedro is a voter.
**Answer:** Invalid
**Explanation:** Illicit conversion — being a citizen doesn't guarantee being a voter (minors are citizens but not voters; unregistered adults are citizens but not voters).

**4.** No unauthorized person may enter the vault. The guard is unauthorized. Therefore, the guard may not enter the vault.
**Answer:** Valid
**Explanation:** The guard falls in the "unauthorized" category, which is completely excluded from vault entry.

**5.** If the report is late, a penalty is imposed. The report is not late. Therefore, no penalty is imposed.
**Answer:** Invalid
**Explanation:** Denying the antecedent — a penalty might be imposed for other reasons (errors, incomplete data, wrong format).

**6.** All mammals are warm-blooded. All dogs are mammals. Therefore, all dogs are warm-blooded.
**Answer:** Valid
**Explanation:** Hypothetical syllogism / transitive chain — dogs ⊂ mammals ⊂ warm-blooded.

**7.** Some employees are managers. All managers attend meetings. Therefore, some employees attend meetings.
**Answer:** Valid
**Explanation:** The employees who are managers must attend meetings (since all managers do). So at least some employees attend meetings.

**8.** "All staff must wear IDs." "Mr. Tan is a staff member." "Mr. Tan is not wearing an ID." — Are these statements consistent?
**Answer:** No — contradiction
**Explanation:** If all staff must wear IDs and Mr. Tan is staff, then Mr. Tan must wear an ID. The third statement contradicts this.

**9.** All birds have wings. Penguins are birds. Therefore, penguins have wings.
**Answer:** Valid
**Explanation:** Regardless of whether penguins can fly, the argument's structure is valid — if all birds have wings and penguins are birds, penguins must have wings (and they do — they just can't fly with them).

**10.** If a student passes all subjects, they graduate. Maria graduated. Therefore, Maria passed all subjects.
**Answer:** Invalid
**Explanation:** Affirming the consequent — Maria might have graduated through special provisions, appeals, or alternative requirements.

**11.** All contracts require signatures. This document has a signature. Therefore, this document is a contract.
**Answer:** Invalid
**Explanation:** Many documents have signatures (letters, memos, receipts) without being contracts. Having a signature is necessary for contracts but not exclusive to them.

**12.** No minor may purchase alcohol. Alex is a minor. Therefore, Alex may not purchase alcohol.
**Answer:** Valid
**Explanation:** Alex belongs to the "minor" category, which is completely excluded from alcohol purchasing.

**13.** If the alarm triggers, security responds. Security did not respond. Therefore, the alarm did not trigger.
**Answer:** Valid
**Explanation:** Modus tollens — P → Q, ¬Q, therefore ¬P. If the consequence didn't happen, the trigger didn't happen.

**14.** All accountants are detail-oriented. Some detail-oriented people are artists. Therefore, some accountants are artists.
**Answer:** Invalid
**Explanation:** The "some detail-oriented people" who are artists might not include any accountants. The overlap between detail-oriented artists and accountants is not guaranteed.

**15.** "Every employee received a bonus." "Ms. Cruz is an employee." "Ms. Cruz did not receive a bonus." — Consistent or contradictory?
**Answer:** Contradictory
**Explanation:** If every employee received a bonus and Ms. Cruz is an employee, she must have received one. The third statement contradicts this.

**16.** All squares are rectangles. All rectangles have four sides. Therefore, all squares have four sides.
**Answer:** Valid
**Explanation:** Transitive chain — squares ⊂ rectangles ⊂ four-sided figures.

**17.** If you exercise regularly, you stay healthy. You are not healthy. Therefore, you do not exercise regularly.
**Answer:** Valid
**Explanation:** Modus tollens — the consequent is false, so the antecedent must be false.

**18.** Some politicians are honest. Some honest people are teachers. Therefore, some politicians are teachers.
**Answer:** Invalid
**Explanation:** Two particular premises with "some" cannot guarantee a connection between the subjects. The honest politicians and the honest teachers might be completely different people.

**19.** All roses are flowers. All flowers need water. All things that need water are living organisms. Therefore, all roses are living organisms.
**Answer:** Valid
**Explanation:** Extended transitive chain — roses ⊂ flowers ⊂ need water ⊂ living organisms.

**20.** "No student failed the exam." "Carlos is a student." "Carlos failed the exam." — Consistent or contradictory?
**Answer:** Contradictory
**Explanation:** If no student failed and Carlos is a student, Carlos cannot have failed. The third statement directly contradicts what the first two together require.

---

## Quick Recap

- **Truth** is a property of individual statements — does the statement match reality?
- **Validity** is a property of arguments — does the conclusion follow necessarily from the premises?
- Truth and validity are **independent** — you can have valid arguments with false premises, and true conclusions from invalid reasoning
- A **sound** argument is both valid AND has true premises — this guarantees a true conclusion
- **Valid arguments** make the conclusion impossible to deny if the premises are accepted
- **Invalid arguments** have a logical gap — the conclusion goes beyond what the premises support
- **Contradictions** are sets of statements that cannot all be true simultaneously
- Test validity using: counterexample method, logical form analysis, diagram verification, or truth tables
- Common CSE traps: affirming the consequent, denying the antecedent, illicit conversion, undistributed middle
- Always evaluate structure, never content — ignore whether premises are factually true or false

---

## Memory Aids

- **"Valid = Vacuum-sealed"** — in a valid argument, the conclusion is sealed inside the premises. No air (alternative possibilities) can get in.
- **"Truth is about the WORLD, Validity is about the WIRING"** — truth checks facts against reality; validity checks whether the logical wiring connects premises to conclusion.
- **"Sound = Structure + Substance"** — a sound argument has both valid structure AND true premises.
- **"The Fish Test"** — if "All fish can fly, Tuna is a fish, therefore tuna can fly" bothers you, remember: validity doesn't care about truth. The structure is perfect.
- **"Reverse = Wrong"** — if the conclusion reverses the direction of a premise (All A are B → therefore All B are A), it's almost always invalid.
- **"Could ≠ Must"** — validity requires MUST, not COULD. If the conclusion could be false while premises are true, the argument is invalid.
- **"Two Negatives, No Conclusion"** — from two negative premises, no valid standard conclusion follows.

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

- **Logical Operators:** Truth tables define operator behavior, which determines argument validity
- **Conditional Reasoning:** Valid conditional argument forms (modus ponens, modus tollens) are key validity patterns
- **Syllogisms:** Syllogism validity is the most common validity-testing format on the CSE
- **Analytical Comprehension:** Evaluating argument validity in reading passages uses the same structural analysis

### Mastery Checklist
✅ Distinguish truth from validity correctly — they are independent properties
✅ Identify valid arguments by testing whether the conclusion is guaranteed
✅ Recognize invalid arguments by finding counterexamples
✅ Detect contradictions in sets of statements efficiently
✅ Translate arguments into symbolic form for structural analysis
✅ Apply modus ponens, modus tollens, and hypothetical syllogism correctly
✅ Recognize and reject affirming the consequent and denying the antecedent
✅ Evaluate logical consistency across multiple premises systematically
✅ Solve CSE validity questions within 45-60 seconds using shortcuts
✅ Eliminate incorrect answer choices using structural analysis rather than intuition

> 🤔 **Why does this work?** Separating truth from validity works because they are logically independent properties. Truth is about correspondence with reality (a property of individual statements); validity is about logical structure (a property of arguments). An argument can have false premises and still be valid, because validity only asks: "IF the premises WERE true, would the conclusion be guaranteed?" This conditional framing is what lets you evaluate structure without knowing facts.


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
