2# Order of Operations

## Explanations

### Introduction

**Order of Operations** is the universally agreed-upon set of rules that dictates the sequence in which mathematical operations must be performed when evaluating an expression. Without these rules, the same expression could yield multiple different answers depending on which operation you perform first — creating chaos in engineering, finance, programming, and every quantitative field.

This subtopic covers five critical areas:
- **Parentheses and Grouping Symbols** — solving innermost groups first
- **Exponents** — evaluating powers before basic arithmetic
- **Multiplication and Division** — equal priority, solved left to right
- **Addition and Subtraction** — equal priority, solved left to right
- **PEMDAS/BODMAS Application** — combining all rules into a systematic solving process

In the Philippine Civil Service Examination (CSE), order of operations questions appear as direct computation items in the Numerical Ability section. They test whether you can correctly evaluate expressions that combine multiple operations — a skill that underpins every other math topic on the exam. A single misstep in operation order cascades into a wrong answer, even if your arithmetic is perfect.

### Why Order of Operations Is Tested in the CSE

The Civil Service Exam tests order of operations because:
- Government employees compute budgets, payroll deductions, tax formulas, and statistical measures that involve multiple operations in a single expression
- Engineering and infrastructure calculations use formulas where incorrect operation order produces dangerous results (e.g., computing load-bearing capacity)
- Financial computations like compound interest, amortization, and tax brackets require strict operation sequencing
- Programming and spreadsheet formulas in government IT systems follow PEMDAS — an employee who misunderstands order of operations will create flawed formulas
- Statistical computations (mean, variance, weighted averages) require correct grouping and operation sequencing
- This topic efficiently separates examinees who understand mathematical structure from those who simply compute left to right

### Common Mistakes Examinees Make

1. **Performing addition before multiplication** — evaluating 3 + 4 × 2 as 14 instead of 11
2. **Ignoring parentheses** — skipping the grouping and jumping to multiplication or division
3. **Treating multiplication as higher priority than division** — they are EQUAL priority, solved left to right
4. **Treating addition as higher priority than subtraction** — they are EQUAL priority, solved left to right
5. **Incorrect exponent evaluation** — computing 2³ as 6 (multiplying base × exponent) instead of 8
6. **Forgetting that fraction bars act as grouping symbols** — the numerator and denominator must each be simplified before dividing
7. **Skipping steps and making arithmetic errors** — rushing through multi-operation expressions
8. **Mishandling negative signs with exponents** — confusing (-3)² = 9 with -3² = -9

### Learning Objectives

After this lesson, you should be able to:
- Identify the correct order of operations using PEMDAS/BODMAS
- Solve expressions using PEMDAS/BODMAS correctly and systematically
- Evaluate numerical expressions with multiple operations including parentheses, exponents, multiplication, division, addition, and subtraction
- Analyze expressions involving integers, decimals, fractions, and exponents
- Recognize and avoid common order-of-operations errors
- Solve CSE-style order of operations questions efficiently under time pressure

---

### 4.1 What Is the Order of Operations?

The **order of operations** is a set of rules that establishes which calculations are performed first in a mathematical expression. It exists to eliminate ambiguity — ensuring that everyone who evaluates the same expression arrives at the same answer.

#### Why We Need These Rules

Consider the expression: **8 + 4 × 3**

Without agreed-upon rules, two people could get different answers:
- Person A (left to right): 8 + 4 = 12, then 12 × 3 = **36**
- Person B (multiplication first): 4 × 3 = 12, then 8 + 12 = **20**

The correct answer is **20** because multiplication takes priority over addition. The order of operations is the universal agreement that makes this unambiguous.

#### The PEMDAS System

**PEMDAS** is the mnemonic used in the Philippines and the United States:

| Letter | Operation | Priority |
|--------|-----------|----------|
| **P** | Parentheses (Grouping Symbols) | 1st (highest) |
| **E** | Exponents (Powers and Roots) | 2nd |
| **M** | Multiplication | 3rd (tied with Division) |
| **D** | Division | 3rd (tied with Multiplication) |
| **A** | Addition | 4th (tied with Subtraction) |
| **S** | Subtraction | 4th (tied with Addition) |

#### The BODMAS System

**BODMAS** is the equivalent mnemonic used in the UK, Australia, and some Asian countries:

| Letter | Operation | Priority |
|--------|-----------|----------|
| **B** | Brackets (Grouping Symbols) | 1st (highest) |
| **O** | Orders (Exponents/Powers) | 2nd |
| **D** | Division | 3rd (tied with Multiplication) |
| **M** | Multiplication | 3rd (tied with Division) |
| **A** | Addition | 4th (tied with Subtraction) |
| **S** | Subtraction | 4th (tied with Addition) |

#### Critical Clarification: Tied Operations

A common misconception is that multiplication comes before division (because M appears before D in PEMDAS) and addition comes before subtraction. **This is wrong.**

- **Multiplication and Division have EQUAL priority** — evaluate left to right
- **Addition and Subtraction have EQUAL priority** — evaluate left to right

The left-to-right rule applies only to operations of equal priority. Higher-priority operations are always performed first regardless of position.

> 🤔 **Why does this work?** Multiplication and division are the same operation expressed differently — dividing by 2 is identical to multiplying by 1/2. Similarly, subtraction is addition of a negative. Because each pair is fundamentally one operation, they share the same priority. The left-to-right convention then resolves ambiguity the same way we read text: sequentially.

> ⚠️ **Misconception:** "In PEMDAS, multiplication always comes before division because M is listed before D."
>
> **Why it fails:** Evaluate 24 ÷ 6 × 2. If you multiply first: 24 ÷ 12 = 2 (wrong). Left to right: 24 ÷ 6 = 4, then 4 × 2 = 8 (correct). The mnemonic's letter order does NOT indicate priority between M and D.
>
> **Correct model:** M and D share the same priority level. When both appear, evaluate whichever comes first reading left to right. The same applies to A and S.

#### Simple Examples

**Example 1:** 5 + 3 × 2
- Multiplication first: 3 × 2 = 6
- Then addition: 5 + 6 = **11**

**Example 2:** 20 - 8 ÷ 4
- Division first: 8 ÷ 4 = 2
- Then subtraction: 20 - 2 = **18**

**Example 3:** 6 × 3 - 4 + 2
- Multiplication first: 6 × 3 = 18
- Then left to right: 18 - 4 + 2 = 14 + 2 = **16**

#### Real-Life Applications

| Context | Expression | Correct Evaluation |
|---------|-----------|-------------------|
| Payroll | Base pay + overtime hours × rate | Multiply first, then add |
| Budgeting | Total - (items × unit cost) | Parentheses first |
| Statistics | Sum of values ÷ count + adjustment | Divide first, then add |
| Engineering | Force × distance + friction × area | Each multiplication first, then add |
| Tax computation | Income - deductions × tax rate | Multiply first, then subtract |

---

### 4.2 Parentheses and Grouping Symbols

Grouping symbols tell you: "Solve what's inside me FIRST, before anything else." They override the normal priority of operations.

#### Types of Grouping Symbols

| Symbol | Name | Example |
|--------|------|---------|
| ( ) | Parentheses | (3 + 5) × 2 |
| [ ] | Brackets | [4 + (2 × 3)] ÷ 5 |
| { } | Braces | {[6 + 2] × (3 - 1)} |
| — (fraction bar) | Vinculum | (8 + 4) / (3 - 1) means evaluate top and bottom separately |

#### The Nesting Rule

When grouping symbols are nested (one inside another), **always work from the innermost group outward**.

Order of nesting (innermost to outermost): Parentheses → Brackets → Braces
```
{ [ ( innermost ) middle ] outermost }
```

#### Easy Examples

**Example 1:** (3 + 5) × 2
- Parentheses first: 3 + 5 = 8
- Then multiply: 8 × 2 = **16**

**Example 2:** 10 - (4 + 3)
- Parentheses first: 4 + 3 = 7
- Then subtract: 10 - 7 = **3**

**Example 3:** (12 - 4) ÷ (6 - 2)
- Left parentheses: 12 - 4 = 8
- Right parentheses: 6 - 2 = 4
- Then divide: 8 ÷ 4 = **2**

#### Medium Examples

**Example 4:** 3 × (4 + 5) - 2 × (8 - 3)
- First parentheses: 4 + 5 = 9
- Second parentheses: 8 - 3 = 5
- Multiplications: 3 × 9 = 27 and 2 × 5 = 10
- Subtraction: 27 - 10 = **17**

**Example 5:** [(8 + 2) × 3] - 5
- Innermost parentheses: 8 + 2 = 10
- Brackets: 10 × 3 = 30
- Subtraction: 30 - 5 = **25**

#### Hard Examples

**Example 6:** {[3 × (2 + 4)] + [5 × (8 - 6)]} ÷ 2
- Innermost: (2 + 4) = 6 and (8 - 6) = 2
- Brackets: [3 × 6] = 18 and [5 × 2] = 10
- Braces: {18 + 10} = 28
- Division: 28 ÷ 2 = **14**

**Example 7:** 100 - [(5 + 3) × (12 - 4)] ÷ 4
- Innermost: (5 + 3) = 8 and (12 - 4) = 8
- Brackets: [8 × 8] = 64
- Division: 64 ÷ 4 = 16
- Subtraction: 100 - 16 = **84**

#### Fraction Bars as Grouping Symbols

A fraction bar acts as both a division sign AND a grouping symbol. The entire numerator is one group and the entire denominator is another group.

> 🤔 **Why does this work?** A fraction bar is shorthand for division, and division requires knowing the complete dividend and divisor before computing. The bar visually separates the expression into "everything above" (dividend) and "everything below" (divisor), forcing you to simplify each part fully before dividing. This is why (3 + 5)/(2 + 2) = 8/4 = 2, not 3 + 5/2 + 2.

**Example 8:** (10 + 6) / (4 + 4)
- Numerator: 10 + 6 = 16
- Denominator: 4 + 4 = 8
- Division: 16 ÷ 8 = **2**

**Example 9:** (3 × 4 + 8) / (2 × 5)
- Numerator: 3 × 4 + 8 = 12 + 8 = 20
- Denominator: 2 × 5 = 10
- Division: 20 ÷ 10 = **2**

#### CSE-Style Example

**A government office orders 5 boxes of bond paper at ₱250 each and 3 boxes of folders at ₱180 each. If the office has a ₱2,000 budget, how much remains after the purchase?**

Expression: 2000 - (5 × 250 + 3 × 180)
- Inside parentheses: 5 × 250 = 1,250 and 3 × 180 = 540
- Add inside parentheses: 1,250 + 540 = 1,790
- Subtract: 2,000 - 1,790 = **₱210**

---

### 4.3 Exponents

An **exponent** (also called a power) tells you how many times to multiply a number (the base) by itself. Exponents are evaluated AFTER parentheses but BEFORE multiplication, division, addition, and subtraction.

#### Terminology

```
    exponent
      ↓
   base² = base × base
     ↑
   base
```

- **Base:** The number being multiplied
- **Exponent:** How many times the base is used as a factor
- **Power:** The result of the exponentiation

#### Common Powers to Memorize

| Expression | Expanded | Value |
|-----------|----------|-------|
| 2¹ | 2 | 2 |
| 2² | 2 × 2 | 4 |
| 2³ | 2 × 2 × 2 | 8 |
| 2⁴ | 2 × 2 × 2 × 2 | 16 |
| 2⁵ | 2 × 2 × 2 × 2 × 2 | 32 |
| 3² | 3 × 3 | 9 |
| 3³ | 3 × 3 × 3 | 27 |
| 4² | 4 × 4 | 16 |
| 5² | 5 × 5 | 25 |
| 5³ | 5 × 5 × 5 | 125 |
| 10² | 10 × 10 | 100 |
| 10³ | 10 × 10 × 10 | 1,000 |

#### Special Exponent Rules

**Zero Exponent:** Any non-zero number raised to the power of 0 equals 1.
```
5⁰ = 1
100⁰ = 1
(-7)⁰ = 1
```
Why? Because the pattern demands it: 5³ = 125, 5² = 25, 5¹ = 5, 5⁰ = 1 (each step divides by 5).

> 🤔 **Why does this work?** Each time you decrease the exponent by 1, you divide the result by the base. So 5³ = 125, 5² = 125 ÷ 5 = 25, 5¹ = 25 ÷ 5 = 5, and 5⁰ = 5 ÷ 5 = 1. This pattern holds for any non-zero base. Algebraically, x^n ÷ x^n = x^(n−n) = x⁰, and any non-zero number divided by itself equals 1.

**Exponent of 1:** Any number raised to the power of 1 equals itself.
```
7¹ = 7
1000¹ = 1000
```

**Negative Base with Even Exponent:** Result is positive.
```
(-3)² = (-3) × (-3) = 9
(-2)⁴ = (-2) × (-2) × (-2) × (-2) = 16
```

**Negative Base with Odd Exponent:** Result is negative.
```
(-3)³ = (-3) × (-3) × (-3) = -27
(-2)³ = (-2) × (-2) × (-2) = -8
```

#### Critical Distinction: -3² vs (-3)²

This is one of the most common errors on exams:

- **(-3)² = 9** — The parentheses mean "negative three, squared." The entire -3 is the base.
- **-3² = -9** — Without parentheses, only 3 is the base. This means -(3²) = -(9) = -9.

```
(-3)² = (-3) × (-3) = +9    ← base is -3
 -3²  = -(3 × 3) = -9       ← base is 3, then negate
```

> ⚠️ **Misconception:** "−5² equals 25 because you square the negative number."
>
> **Why it fails:** Without parentheses, the exponent binds only to 5. So −5² = −(5²) = −25, not +25. If you compute −5² as 25, you'd be saying that −5² = (−5)², which makes the parentheses meaningless. Test: your calculator gives −5² = −25.
>
> **Correct model:** The negative sign is a separate operation (multiplication by −1) applied AFTER the exponent. Only when the negative is inside parentheses — (−5)² — is the entire −5 used as the base, giving +25.

#### Step-by-Step Examples with Exponents

**Example 1:** 2³ + 4²
- Exponents first: 2³ = 8 and 4² = 16
- Addition: 8 + 16 = **24**

**Example 2:** 5 × 3² - 10
- Exponent first: 3² = 9
- Multiplication: 5 × 9 = 45
- Subtraction: 45 - 10 = **35**

**Example 3:** (2 + 3)² - 4²
- Parentheses first: 2 + 3 = 5
- Exponents: 5² = 25 and 4² = 16
- Subtraction: 25 - 16 = **9**

**Example 4:** 10 - 2³ + 3²
- Exponents: 2³ = 8 and 3² = 9
- Left to right: 10 - 8 + 9 = 2 + 9 = **11**

#### Common Exponent Mistakes

| Mistake | Wrong | Correct |
|---------|-------|---------|
| Multiplying base × exponent | 2³ = 6 | 2³ = 8 |
| Ignoring negative base rules | (-2)³ = 8 | (-2)³ = -8 |
| Confusing -x² with (-x)² | -5² = 25 | -5² = -25 |
| Forgetting zero exponent | 4⁰ = 0 | 4⁰ = 1 |

---

### 4.4 Multiplication and Division

Multiplication and division share the **same priority level** — they are performed AFTER parentheses and exponents, but BEFORE addition and subtraction. When both appear in an expression, evaluate them **left to right**.

#### The Left-to-Right Rule

When multiplication and division appear together without grouping symbols separating them, process them in the order they appear from left to right.

**Example 1:** 24 ÷ 6 × 2
- Left to right: 24 ÷ 6 = 4, then 4 × 2 = **8**
- NOT: 24 ÷ 12 = 2 (wrong — you cannot do 6 × 2 first)

**Example 2:** 5 × 8 ÷ 4
- Left to right: 5 × 8 = 40, then 40 ÷ 4 = **10**

**Example 3:** 36 ÷ 9 × 3 ÷ 2
- Left to right: 36 ÷ 9 = 4, then 4 × 3 = 12, then 12 ÷ 2 = **6**

#### Why Left to Right?

Consider: 12 ÷ 3 × 2

If multiplication went first: 12 ÷ 6 = 2
If left to right: 4 × 2 = 8

The mathematical convention is left to right, giving **8**. This is because division is the inverse of multiplication — they are the same operation expressed differently (dividing by 2 is multiplying by ½). Equal operations resolve by reading order.

> 🤔 **Why does this work?** When two operations have equal precedence, we need a tiebreaker. Left-to-right was chosen because it mirrors how we read expressions sequentially and because it produces results consistent with fraction notation. Writing 12 ÷ 3 × 2 is equivalent to (12/3) × 2 = 8, which matches the left-to-right reading. Any other convention would create inconsistency between inline and fraction notation.

#### Multiplication with Different Number Types

**Integers:**
```
(-4) × 5 = -20        (negative × positive = negative)
(-3) × (-7) = 21      (negative × negative = positive)
```

**Decimals:**
```
2.5 × 4 = 10.0
0.3 × 0.7 = 0.21      (1 decimal place × 1 decimal place = 2 decimal places)
```

**Fractions:**
```
(2/3) × (3/4) = 6/12 = 1/2    (multiply numerators, multiply denominators)
```

#### Division with Different Number Types

**Integers:**
```
(-20) ÷ 4 = -5        (negative ÷ positive = negative)
(-18) ÷ (-3) = 6      (negative ÷ negative = positive)
```

**Decimals:**
```
7.5 ÷ 2.5 = 3
0.48 ÷ 0.6 = 0.8
```

**Fractions:**
```
(3/4) ÷ (2/5) = (3/4) × (5/2) = 15/8    (multiply by reciprocal)
```

#### Common Computation Traps

**Trap 1:** Assuming multiplication always comes before division.
```
WRONG: 8 ÷ 2 × 4 → 8 ÷ 8 = 1
CORRECT: 8 ÷ 2 × 4 → 4 × 4 = 16 (left to right)
```

**Trap 2:** Forgetting sign rules in multiplication chains.
```
(-2) × (-3) × (-4) = 6 × (-4) = -24    (odd number of negatives = negative)
(-2) × (-3) × (-4) × (-1) = -24 × (-1) = 24    (even number of negatives = positive)
```

**Trap 3:** Decimal point placement errors.
```
0.2 × 0.3 = 0.06    (NOT 0.6)
Count total decimal places: 1 + 1 = 2 decimal places in answer
```

#### Easy Examples

**Example 1:** 6 × 5 ÷ 3
- Left to right: 30 ÷ 3 = **10**

**Example 2:** 48 ÷ 8 × 2
- Left to right: 6 × 2 = **12**

#### Medium Examples

**Example 3:** 3 × 4 ÷ 2 × 5
- Left to right: 12 ÷ 2 × 5 = 6 × 5 = **30**

**Example 4:** 100 ÷ 5 ÷ 4 × 3
- Left to right: 20 ÷ 4 × 3 = 5 × 3 = **15**

#### Hard Examples

**Example 5:** (-6) × 4 ÷ (-3) × 2 ÷ (-4)
- Left to right: -24 ÷ (-3) × 2 ÷ (-4) = 8 × 2 ÷ (-4) = 16 ÷ (-4) = **-4**

**Example 6:** 2.4 × 5 ÷ 0.3 × 2
- Left to right: 12 ÷ 0.3 × 2 = 40 × 2 = **80**

---

### 4.5 Addition and Subtraction

Addition and subtraction share the **same priority level** — they are performed LAST (after parentheses, exponents, multiplication, and division). When both appear, evaluate them **left to right**.

#### The Left-to-Right Rule for Addition and Subtraction

**Example 1:** 15 - 8 + 3
- Left to right: 15 - 8 = 7, then 7 + 3 = **10**
- NOT: 15 - 11 = 4 (wrong — you cannot add 8 + 3 first)

**Example 2:** 20 + 5 - 12 + 3 - 8
- Left to right: 25 - 12 + 3 - 8 = 13 + 3 - 8 = 16 - 8 = **8**

**Example 3:** 100 - 45 - 30 + 15
- Left to right: 55 - 30 + 15 = 25 + 15 = **40**

#### Combining Positive and Negative Numbers

When an expression has many terms with mixed signs, you can group positives and negatives separately:

**Example:** 8 - 3 + 5 - 7 + 2 - 1
- Positives: 8 + 5 + 2 = 15
- Negatives: 3 + 7 + 1 = 11
- Result: 15 - 11 = **4**

This shortcut works because addition is commutative and associative. However, on the CSE, always verify by going left to right if time permits.

#### Simplifying Long Expressions

For expressions with only addition and subtraction, rewrite subtraction as adding a negative:

**Example:** 50 - 23 + 8 - 15 + 30 - 42
= 50 + (-23) + 8 + (-15) + 30 + (-42)
= (50 + 8 + 30) + (-23 + -15 + -42)
= 88 + (-80)
= **8**

#### Easy Examples

**Example 1:** 9 + 4 - 6
- Left to right: 13 - 6 = **7**

**Example 2:** 25 - 10 - 5
- Left to right: 15 - 5 = **10**

#### Medium Examples

**Example 3:** 45 - 12 + 8 - 23 + 5
- Left to right: 33 + 8 - 23 + 5 = 41 - 23 + 5 = 18 + 5 = **23**

**Example 4:** -8 + 15 - 3 + 7 - 20
- Left to right: 7 - 3 + 7 - 20 = 4 + 7 - 20 = 11 - 20 = **-9**

#### Hard Examples

**Example 5:** 100 - 33 - 27 + 45 - 68 + 13
- Positives: 100 + 45 + 13 = 158
- Negatives: 33 + 27 + 68 = 128
- Result: 158 - 128 = **30**

**Example 6:** -15 + 42 - 38 + 21 - 7 + 3 - 16
- Positives: 42 + 21 + 3 = 66
- Negatives: 15 + 38 + 7 + 16 = 76
- Result: 66 - 76 = **-10**

---

### Check Your Understanding

**1.** In PEMDAS, which operations share the same priority level? → **Multiplication & Division (tied); Addition & Subtraction (tied)** (M/D are equal; A/S are equal — resolve left to right)
**2.** What is (-4)² versus -4²? → **(-4)² = 16; -4² = -16** (parentheses make -4 the base; without them, only 4 is squared)
**3.** In 30 ÷ 5 × 3, which operation do you perform first? → **30 ÷ 5 = 6** (same priority, so left to right)
**4.** Does a fraction bar act as a grouping symbol? → **Yes** (simplify numerator and denominator separately before dividing)

---

### 4.6 PEMDAS/BODMAS Application — Complete Walkthroughs

This section brings all the rules together. Every expression follows the same systematic process:

#### The Solving Procedure

```
Step 1: Identify and solve all Parentheses/Brackets (innermost first)
Step 2: Evaluate all Exponents/Orders
Step 3: Perform all Multiplication and Division (left to right)
Step 4: Perform all Addition and Subtraction (left to right)
```

#### Detailed Walkthrough 1 (Easy)

**Evaluate: 8 + 2 × 5**

| Step | Operation | Expression | Result |
|------|-----------|-----------|--------|
| 1 | No parentheses | — | — |
| 2 | No exponents | — | — |
| 3 | Multiplication: 2 × 5 | 8 + **10** | — |
| 4 | Addition: 8 + 10 | — | **18** |

#### Detailed Walkthrough 2 (Easy)

**Evaluate: 20 - 3 × 4 + 6**

| Step | Operation | Expression |
|------|-----------|-----------|
| 3 | Multiplication: 3 × 4 = 12 | 20 - 12 + 6 |
| 4 | Left to right: 20 - 12 = 8 | 8 + 6 |
| 4 | Addition: 8 + 6 | **14** |

#### Detailed Walkthrough 3 (Medium)

**Evaluate: 3 × (4 + 2)² - 10**

| Step | Operation | Expression |
|------|-----------|-----------|
| 1 | Parentheses: 4 + 2 = 6 | 3 × 6² - 10 |
| 2 | Exponent: 6² = 36 | 3 × 36 - 10 |
| 3 | Multiplication: 3 × 36 = 108 | 108 - 10 |
| 4 | Subtraction: 108 - 10 | **98** |

#### Detailed Walkthrough 4 (Medium)

**Evaluate: 48 ÷ (2 × 3) + 5² - 7**

| Step | Operation | Expression |
|------|-----------|-----------|
| 1 | Parentheses: 2 × 3 = 6 | 48 ÷ 6 + 5² - 7 |
| 2 | Exponent: 5² = 25 | 48 ÷ 6 + 25 - 7 |
| 3 | Division: 48 ÷ 6 = 8 | 8 + 25 - 7 |
| 4 | Left to right: 8 + 25 = 33 | 33 - 7 |
| 4 | Subtraction: 33 - 7 | **26** |

#### Detailed Walkthrough 5 (Hard)

**Evaluate: 2 × [3 + (4² - 6)] ÷ 5 + 1**

| Step | Operation | Expression |
|------|-----------|-----------|
| 1a | Inner parentheses exponent: 4² = 16 | 2 × [3 + (16 - 6)] ÷ 5 + 1 |
| 1b | Inner parentheses: 16 - 6 = 10 | 2 × [3 + 10] ÷ 5 + 1 |
| 1c | Brackets: 3 + 10 = 13 | 2 × 13 ÷ 5 + 1 |
| 3a | Multiplication: 2 × 13 = 26 | 26 ÷ 5 + 1 |
| 3b | Division: 26 ÷ 5 = 5.2 | 5.2 + 1 |
| 4 | Addition: 5.2 + 1 | **6.2** |

#### Detailed Walkthrough 6 (Hard)

**Evaluate: (8 + 2)² ÷ (3² + 4²) × 6 - 4**

| Step | Operation | Expression |
|------|-----------|-----------|
| 1a | First parentheses: 8 + 2 = 10 | 10² ÷ (3² + 4²) × 6 - 4 |
| 1b/2 | Exponents inside second group: 3² = 9, 4² = 16 | 10² ÷ (9 + 16) × 6 - 4 |
| 1c | Second parentheses: 9 + 16 = 25 | 10² ÷ 25 × 6 - 4 |
| 2 | Remaining exponent: 10² = 100 | 100 ÷ 25 × 6 - 4 |
| 3a | Division: 100 ÷ 25 = 4 | 4 × 6 - 4 |
| 3b | Multiplication: 4 × 6 = 24 | 24 - 4 |
| 4 | Subtraction: 24 - 4 | **20** |

#### Structured Solution Method

For complex expressions, write each step on a new line, underlining or highlighting the operation you're performing:

```
Original:  5 + 3 × (8 - 2)² ÷ 6
Step 1:    5 + 3 × (6)² ÷ 6        ← parentheses: 8-2=6
Step 2:    5 + 3 × 36 ÷ 6          ← exponent: 6²=36
Step 3a:   5 + 108 ÷ 6             ← multiply: 3×36=108
Step 3b:   5 + 18                   ← divide: 108÷6=18
Step 4:    23                       ← add: 5+18=23
```

This method prevents skipped steps and makes it easy to find errors.

---

### 4.7 Order of Operations with Fractions

Fractions add complexity because the fraction bar itself is a grouping symbol, and operations with fractions require LCD computation or reciprocal multiplication.

#### Fraction Bars as Grouping Symbols

When you see an expression written as a fraction, treat the numerator and denominator as separate groups:

**Example 1:** (12 + 8) / (4 + 1)
- Numerator: 12 + 8 = 20
- Denominator: 4 + 1 = 5
- Division: 20 ÷ 5 = **4**

**Example 2:** (3 × 5 - 1) / (2 + 5)
- Numerator: 3 × 5 - 1 = 15 - 1 = 14
- Denominator: 2 + 5 = 7
- Division: 14 ÷ 7 = **2**

**Example 3:** (4² + 3²) / (5 × 5)
- Numerator: 16 + 9 = 25
- Denominator: 5 × 5 = 25
- Division: 25 ÷ 25 = **1**

#### Mixed Operations with Fractions

**Example 4:** 1/2 + 1/3 × 3/4
- Multiplication first: 1/3 × 3/4 = 3/12 = 1/4
- Addition: 1/2 + 1/4 = 2/4 + 1/4 = **3/4**

**Example 5:** (2/3 + 1/6) × 12
- Parentheses first: 2/3 + 1/6 = 4/6 + 1/6 = 5/6
- Multiplication: 5/6 × 12 = 60/6 = **10**

**Example 6:** 3/4 ÷ (1/2 + 1/4) - 1/3
- Parentheses: 1/2 + 1/4 = 2/4 + 1/4 = 3/4
- Division: 3/4 ÷ 3/4 = 3/4 × 4/3 = 12/12 = 1
- Subtraction: 1 - 1/3 = 3/3 - 1/3 = **2/3**

#### CSE-Style Fraction Example

**A clerk processes 1/4 of the files in the morning and 1/3 of the remaining files in the afternoon. What fraction of the total files were processed?**

Expression: 1/4 + 1/3 × (1 - 1/4)
- Parentheses: 1 - 1/4 = 3/4
- Multiplication: 1/3 × 3/4 = 3/12 = 1/4
- Addition: 1/4 + 1/4 = **2/4 = 1/2**

---

### 4.8 Order of Operations with Decimals

Decimal expressions follow the same PEMDAS rules. The additional challenge is maintaining decimal point accuracy through multiple operations.

#### Decimal Alignment in Multi-Step Problems

**Example 1:** 2.5 + 1.5 × 4
- Multiplication first: 1.5 × 4 = 6.0
- Addition: 2.5 + 6.0 = **8.5**

**Example 2:** (3.2 + 1.8) × 2.5 - 1.5
- Parentheses: 3.2 + 1.8 = 5.0
- Multiplication: 5.0 × 2.5 = 12.5
- Subtraction: 12.5 - 1.5 = **11.0**

**Example 3:** 10.5 ÷ 3.5 + 2.4 × 5
- Division: 10.5 ÷ 3.5 = 3
- Multiplication: 2.4 × 5 = 12
- Addition: 3 + 12 = **15**

#### Realistic Financial Examples

**Example 4:** An employee earns ₱850.50 per day. After 22 working days, a ₱1,500.00 deduction is applied. What is the net pay?

Expression: 850.50 × 22 - 1500.00
- Multiplication: 850.50 × 22 = 18,711.00
- Subtraction: 18,711.00 - 1,500.00 = **₱17,211.00**

**Example 5:** A utility bill is computed as: base charge ₱250.75 + consumption 145.5 kWh × ₱9.50/kWh + VAT 12% of the subtotal.

Expression: 250.75 + 145.5 × 9.50 + 0.12 × (250.75 + 145.5 × 9.50)
- First, compute consumption: 145.5 × 9.50 = 1,382.25
- Subtotal: 250.75 + 1,382.25 = 1,633.00
- VAT: 0.12 × 1,633.00 = 195.96
- Total: 1,633.00 + 195.96 = **₱1,828.96**

#### Avoiding Decimal Placement Mistakes

**Common Error:** 0.5 × 0.4 = 2.0 (wrong — moved decimal wrong direction)
**Correct:** 0.5 × 0.4 = 0.20 (count decimal places: 1 + 1 = 2)

**Tip:** When multiplying decimals, count total decimal places in both factors. The product must have that many decimal places.

---

### 4.9 Order of Operations with Integers

Integer expressions require careful attention to sign rules combined with operation priority.

#### Sign Rules Review

| Operation | Rule | Example |
|-----------|------|---------|
| (+) × (+) | Positive | 3 × 4 = 12 |
| (-) × (-) | Positive | (-3) × (-4) = 12 |
| (+) × (-) | Negative | 3 × (-4) = -12 |
| (-) × (+) | Negative | (-3) × 4 = -12 |
| (+) ÷ (+) | Positive | 12 ÷ 3 = 4 |
| (-) ÷ (-) | Positive | (-12) ÷ (-3) = 4 |
| (+) ÷ (-) | Negative | 12 ÷ (-3) = -4 |
| (-) ÷ (+) | Negative | (-12) ÷ 3 = -4 |

#### Step-by-Step Sign Analysis

**Example 1:** -3 + 4 × (-2)
- Multiplication first: 4 × (-2) = -8
- Addition: -3 + (-8) = -3 - 8 = **-11**

**Example 2:** (-5)² - 3 × (-4)
- Exponent: (-5)² = 25
- Multiplication: 3 × (-4) = -12
- Subtraction: 25 - (-12) = 25 + 12 = **37**

**Example 3:** -2 × (3 - 7) + (-4)²
- Parentheses: 3 - 7 = -4
- Exponent: (-4)² = 16
- Multiplication: -2 × (-4) = 8
- Addition: 8 + 16 = **24**

**Example 4:** [(-6) + 2] × [(-3) - (-5)]
- First bracket: (-6) + 2 = -4
- Second bracket: (-3) - (-5) = -3 + 5 = 2
- Multiplication: (-4) × 2 = **-8**

#### Common Integer Sign Mistakes

**Mistake 1:** Subtracting a negative — forgetting that minus a negative is plus.
```
WRONG: 10 - (-3) = 7
CORRECT: 10 - (-3) = 10 + 3 = 13
```

**Mistake 2:** Squaring a negative without parentheses.
```
-4² = -(4²) = -16    (only 4 is squared)
(-4)² = (-4)(-4) = 16    (the entire -4 is squared)
```

**Mistake 3:** Multiplying before resolving the sign.
```
WRONG: -2 × -3 × -4 = 24 (assumed all negatives cancel)
CORRECT: (-2) × (-3) × (-4) = 6 × (-4) = -24 (odd negatives = negative)
```

### Check Your Understanding

**1.** What is the value of (2/3 + 1/6) × 12? → **10** (parentheses first: 4/6 + 1/6 = 5/6, then 5/6 × 12 = 10)
**2.** In -2 × (3 - 7) + (-4)², what do you evaluate first? → **Parentheses: 3 - 7 = -4** (P comes before E, M, D, A, S)
**3.** How many negative factors make the product negative? → **An odd number** (even negatives cancel to positive; odd negatives give negative)

---

### 4.10 Multi-Step Expressions

Complex CSE questions combine all operation types into a single expression. The key is systematic, step-by-step evaluation — never skip steps.

#### Easy Multi-Step Examples

**Example 1:** 4 + 6 × 2 - 3
- Multiplication: 6 × 2 = 12
- Left to right: 4 + 12 - 3 = 16 - 3 = **13**

**Example 2:** 15 ÷ 3 + 2 × 4
- Division: 15 ÷ 3 = 5
- Multiplication: 2 × 4 = 8
- Addition: 5 + 8 = **13**

**Example 3:** (7 + 3) × 2 - 5
- Parentheses: 7 + 3 = 10
- Multiplication: 10 × 2 = 20
- Subtraction: 20 - 5 = **15**

#### Medium Multi-Step Examples

**Example 4:** 2³ + 4 × (6 - 2) ÷ 8
- Parentheses: 6 - 2 = 4
- Exponent: 2³ = 8
- Multiplication: 4 × 4 = 16
- Division: 16 ÷ 8 = 2
- Addition: 8 + 2 = **10**

**Example 5:** 50 - 2 × (3² + 4) + 6
- Exponent inside parentheses: 3² = 9
- Parentheses: 9 + 4 = 13
- Multiplication: 2 × 13 = 26
- Left to right: 50 - 26 + 6 = 24 + 6 = **30**

**Example 6:** (12 + 8) ÷ 4 + 3 × (7 - 2)
- Parentheses: 12 + 8 = 20 and 7 - 2 = 5
- Division: 20 ÷ 4 = 5
- Multiplication: 3 × 5 = 15
- Addition: 5 + 15 = **20**

#### Hard Multi-Step Examples

**Example 7:** 3 × [2² + (15 - 3 × 4)] ÷ 3 + 7
- Innermost multiplication: 3 × 4 = 12
- Inner parentheses: 15 - 12 = 3
- Exponent: 2² = 4
- Brackets: 4 + 3 = 7
- Multiplication: 3 × 7 = 21
- Division: 21 ÷ 3 = 7
- Addition: 7 + 7 = **14**

**Example 8:** [(5 + 3)² - (6² - 2²)] ÷ (4 × 3)
- Parentheses: 5 + 3 = 8
- Exponents: 8² = 64, 6² = 36, 2² = 4
- Inner bracket subtraction: 36 - 4 = 32
- Outer bracket subtraction: 64 - 32 = 32
- Denominator: 4 × 3 = 12
- Division: 32 ÷ 12 = **8/3 ≈ 2.67**

#### Advanced CSE-Style Examples

**Example 9:** A government agency allocates a budget using this formula: Total = Base × (1 + Rate)² - Deductions ÷ 2

If Base = 100,000, Rate = 0.1, Deductions = 20,000:
- Parentheses: 1 + 0.1 = 1.1
- Exponent: 1.1² = 1.21
- Multiplication: 100,000 × 1.21 = 121,000
- Division: 20,000 ÷ 2 = 10,000
- Subtraction: 121,000 - 10,000 = **111,000**

**Example 10:** 5 × 4² - 3 × (2³ + 4) ÷ 6 + 2²
- Exponents: 4² = 16, 2³ = 8, 2² = 4
- Parentheses: 8 + 4 = 12
- Multiplications: 5 × 16 = 80 and 3 × 12 = 36
- Division: 36 ÷ 6 = 6
- Left to right: 80 - 6 + 4 = 74 + 4 = **78**

---

### 4.11 Estimation and Answer Checking

On the CSE, time is limited (approximately 1.5 minutes per item). Estimation helps you verify answers quickly or eliminate impossible choices without full computation.

#### Estimating Before Solving

Round each number to a convenient value, then apply PEMDAS to the rounded expression:

**Example:** 4.8 × (3.2 + 6.9) - 2.1²
- Estimate: 5 × (3 + 7) - 2² = 5 × 10 - 4 = 50 - 4 = 46
- Exact: 4.8 × 10.1 - 4.41 = 48.48 - 4.41 = 44.07

If choices are 44, 54, 34, 64 — your estimate of 46 points to **44** as the closest.

#### Checking Reasonableness

After computing, ask: "Does this answer make sense?"

- If you're adding positive numbers, the result must be larger than any addend
- If you're multiplying two numbers greater than 1, the result must be larger than either factor
- If you're dividing by a number greater than 1, the result must be smaller than the dividend
- Squaring a number greater than 1 makes it larger; squaring a number between 0 and 1 makes it smaller

#### Identifying Impossible Choices Quickly

**Example:** What is 12 + 3 × 8 - 4?
- Quick estimate: 12 + 24 - 4 ≈ 32
- If choices are: a) 8  b) 32  c) 84  d) 120
- Eliminate a) (too small), c) and d) (too large)
- Answer: **b) 32**

#### Last-Digit Checking

For expressions with only integers, the last digit of the answer depends on the last digits of the intermediate results:

**Example:** 7 × 9 + 3 × 4
- 7 × 9 = 63 (last digit 3)
- 3 × 4 = 12 (last digit 2)
- 63 + 12: last digit 3 + 2 = 5
- If only one choice ends in 5, that's your answer without full computation.

---

### 4.12 Common Errors in Order of Operations

Understanding these errors helps you avoid them and catch mistakes during answer-checking.

#### Error 1: Performing Addition Before Multiplication

```
WRONG: 5 + 3 × 4 = 8 × 4 = 32
CORRECT: 5 + 3 × 4 = 5 + 12 = 17
```
Multiplication ALWAYS comes before addition (unless parentheses override).

#### Error 2: Ignoring Grouping Symbols

```
WRONG: (6 + 2) × 3 = 6 + 6 = 12    (ignored parentheses, multiplied 2×3)
CORRECT: (6 + 2) × 3 = 8 × 3 = 24
```

#### Error 3: Incorrect Exponent Evaluation

```
WRONG: 2⁴ = 2 × 4 = 8    (multiplied base by exponent)
CORRECT: 2⁴ = 2 × 2 × 2 × 2 = 16
```

#### Error 4: Treating M as Higher Than D

```
WRONG: 12 ÷ 4 × 3 = 12 ÷ 12 = 1    (did multiplication first)
CORRECT: 12 ÷ 4 × 3 = 3 × 3 = 9    (left to right)
```

#### Error 5: Treating A as Higher Than S

```
WRONG: 10 - 3 + 5 = 10 - 8 = 2    (did addition first)
CORRECT: 10 - 3 + 5 = 7 + 5 = 12    (left to right)
```

#### Error 6: Sign Mistakes with Exponents

```
WRONG: -3² = 9    (squared the negative)
CORRECT: -3² = -(3²) = -9    (only 3 is squared without parentheses)
```

#### Error 7: Skipping Steps in Complex Expressions

```
WRONG: 2 + 3 × 4² = 2 + 12² = 2 + 144 = 146    (multiplied before exponentiating)
CORRECT: 2 + 3 × 4² = 2 + 3 × 16 = 2 + 48 = 50    (exponent first, then multiply)
```

#### Error 8: Arithmetic Carelessness Under Time Pressure

The CSE gives limited time per item. Rushing leads to:
- Skipping an operation step
- Misreading a digit or sign
- Confusing × with + or ÷ with -
- Selecting an answer that matches a partial computation (a common distractor design)

**Prevention:** Write each step clearly. Use estimation to verify. If your answer doesn't match any choice, recompute from the beginning rather than adjusting.

---

### Exam Strategies for Order of Operations

#### Strategy 1: Write Every Step

Never try to do multiple operations in your head simultaneously. Write each intermediate result. The 10 seconds spent writing saves the 60 seconds of recomputing after an error.

#### Strategy 2: Identify the First Operation

Before computing anything, scan the entire expression and identify which operation must be performed first:
- See parentheses? → Start there
- No parentheses but exponents? → Start there
- Only ×, ÷, +, -? → Find the leftmost × or ÷

#### Strategy 3: Estimate to Eliminate

Round numbers and quickly estimate the answer. Eliminate choices that are clearly too large or too small. On a 4-choice question, eliminating 2 choices gives you a 50% chance even if you must guess.

#### Strategy 4: Check the Distractors

CSE question designers create wrong choices by applying common errors:
- One choice is the "left-to-right" error (ignoring priority)
- One choice is the "addition before multiplication" error
- One choice is an arithmetic slip

If you recognize which error produces which distractor, you can confirm your answer is NOT one of the error-based choices.

#### Strategy 5: Use the Last-Digit Trick

For integer-only expressions, compute only the last digit of each intermediate step. If only one answer choice has that last digit, you've found the answer in seconds.

#### Strategy 6: Recognize Common Patterns

Memorize results of common sub-expressions:
- Any number × 0 = 0 (entire term vanishes)
- Any number ÷ itself = 1
- x² - y² = (x+y)(x-y) — sometimes faster than computing both squares
- (a+b)² = a² + 2ab + b² — useful for mental estimation

---

### Mini Practice Set

Test your understanding with these 20 problems. Answers and explanations follow.

**1.** 8 + 4 × 3 = ?

**2.** (8 + 4) × 3 = ?

**3.** 20 - 12 ÷ 4 + 1 = ?

**4.** 5² - 3 × 4 = ?

**5.** 2 × (7 + 3) - 4² = ?

**6.** 36 ÷ 6 × 3 - 2 = ?

**7.** 3 + 2³ × 4 - 10 = ?

**8.** (15 - 3) ÷ (2 + 4) = ?

**9.** 4 × 5 - 3 × 4 + 2 × 3 = ?

**10.** [(6 + 2) × 3 - 4] ÷ 5 = ?

**11.** -3² + (-3)² = ?

**12.** 1/2 + 1/4 × 2 = ?

**13.** (2.5 + 1.5) × 3 - 2.5 = ?

**14.** 10 - 2 × (3 + 1)² ÷ 8 = ?

**15.** 5 × 3² - (4 + 6) × 2 = ?

**16.** [4² + (3 × 2 - 1)] ÷ 7 = ?

**17.** (-4) × (-3) + (-2)³ = ?

**18.** (8 + 12) / (2 × 5) + 3² = ?

**19.** 2⁴ - 3 × (5 - 2) + 7 = ?

**20.** {[2 × (3 + 4)] - 5} × 3 = ?

---

#### Answers and Explanations

**1.** 8 + 4 × 3 = 8 + 12 = **20**
- Multiplication first: 4 × 3 = 12, then add 8.

**2.** (8 + 4) × 3 = 12 × 3 = **36**
- Parentheses first: 8 + 4 = 12, then multiply by 3.

**3.** 20 - 12 ÷ 4 + 1 = 20 - 3 + 1 = **18**
- Division first: 12 ÷ 4 = 3. Then left to right: 20 - 3 = 17, 17 + 1 = 18.

**4.** 5² - 3 × 4 = 25 - 12 = **13**
- Exponent: 5² = 25. Multiplication: 3 × 4 = 12. Subtraction: 25 - 12 = 13.

**5.** 2 × (7 + 3) - 4² = 2 × 10 - 16 = 20 - 16 = **4**
- Parentheses: 7 + 3 = 10. Exponent: 4² = 16. Multiply: 2 × 10 = 20. Subtract: 20 - 16 = 4.

**6.** 36 ÷ 6 × 3 - 2 = 6 × 3 - 2 = 18 - 2 = **16**
- Division and multiplication left to right: 36 ÷ 6 = 6, 6 × 3 = 18. Subtract: 18 - 2 = 16.

**7.** 3 + 2³ × 4 - 10 = 3 + 8 × 4 - 10 = 3 + 32 - 10 = **25**
- Exponent: 2³ = 8. Multiply: 8 × 4 = 32. Left to right: 3 + 32 - 10 = 25.

**8.** (15 - 3) ÷ (2 + 4) = 12 ÷ 6 = **2**
- Parentheses: 15 - 3 = 12 and 2 + 4 = 6. Division: 12 ÷ 6 = 2.

**9.** 4 × 5 - 3 × 4 + 2 × 3 = 20 - 12 + 6 = **14**
- Multiplications: 20, 12, 6. Left to right: 20 - 12 + 6 = 8 + 6 = 14.

**10.** [(6 + 2) × 3 - 4] ÷ 5 = [8 × 3 - 4] ÷ 5 = [24 - 4] ÷ 5 = 20 ÷ 5 = **4**
- Inner parentheses: 6 + 2 = 8. Brackets: 8 × 3 = 24, 24 - 4 = 20. Division: 20 ÷ 5 = 4.

**11.** -3² + (-3)² = -9 + 9 = **0**
- -3² = -(3²) = -9 (no parentheses around -3). (-3)² = 9. Sum: -9 + 9 = 0.

**12.** 1/2 + 1/4 × 2 = 1/2 + 2/4 = 1/2 + 1/2 = **1**
- Multiplication first: 1/4 × 2 = 2/4 = 1/2. Addition: 1/2 + 1/2 = 1.

**13.** (2.5 + 1.5) × 3 - 2.5 = 4.0 × 3 - 2.5 = 12.0 - 2.5 = **9.5**
- Parentheses: 2.5 + 1.5 = 4.0. Multiply: 4.0 × 3 = 12.0. Subtract: 12.0 - 2.5 = 9.5.

**14.** 10 - 2 × (3 + 1)² ÷ 8 = 10 - 2 × 16 ÷ 8 = 10 - 32 ÷ 8 = 10 - 4 = **6**
- Parentheses: 3 + 1 = 4. Exponent: 4² = 16. Multiply: 2 × 16 = 32. Divide: 32 ÷ 8 = 4. Subtract: 10 - 4 = 6.

**15.** 5 × 3² - (4 + 6) × 2 = 5 × 9 - 10 × 2 = 45 - 20 = **25**
- Parentheses: 4 + 6 = 10. Exponent: 3² = 9. Multiplications: 5 × 9 = 45, 10 × 2 = 20. Subtract: 45 - 20 = 25.

**16.** [4² + (3 × 2 - 1)] ÷ 7 = [16 + (6 - 1)] ÷ 7 = [16 + 5] ÷ 7 = 21 ÷ 7 = **3**
- Inner: 3 × 2 = 6, 6 - 1 = 5. Exponent: 4² = 16. Brackets: 16 + 5 = 21. Division: 21 ÷ 7 = 3.

**17.** (-4) × (-3) + (-2)³ = 12 + (-8) = **4**
- Multiplication: (-4) × (-3) = 12. Exponent: (-2)³ = -8. Addition: 12 + (-8) = 4.

**18.** (8 + 12) / (2 × 5) + 3² = 20 / 10 + 9 = 2 + 9 = **11**
- Numerator: 8 + 12 = 20. Denominator: 2 × 5 = 10. Division: 20 ÷ 10 = 2. Exponent: 3² = 9. Addition: 2 + 9 = 11.

**19.** 2⁴ - 3 × (5 - 2) + 7 = 16 - 3 × 3 + 7 = 16 - 9 + 7 = **14**
- Parentheses: 5 - 2 = 3. Exponent: 2⁴ = 16. Multiply: 3 × 3 = 9. Left to right: 16 - 9 + 7 = 7 + 7 = 14.

**20.** {[2 × (3 + 4)] - 5} × 3 = {[2 × 7] - 5} × 3 = {14 - 5} × 3 = 9 × 3 = **27**
- Innermost: 3 + 4 = 7. Brackets: 2 × 7 = 14. Braces: 14 - 5 = 9. Multiply: 9 × 3 = 27.

---

### Quick Recap

| Topic | Key Rule |
|-------|----------|
| PEMDAS priority | P → E → MD (left to right) → AS (left to right) |
| Parentheses | Always solve innermost grouping symbols first |
| Exponents | Evaluate powers before ×, ÷, +, - |
| Multiplication & Division | Equal priority — solve left to right |
| Addition & Subtraction | Equal priority — solve left to right |
| Fraction bars | Act as grouping symbols — simplify top and bottom separately |
| Negative exponents | -3² = -9 but (-3)² = 9 |
| Estimation | Round and compute to verify or eliminate choices |

### Memory Aids

- **"Please Excuse My Dear Aunt Sally"** — Parentheses, Exponents, Multiplication, Division, Addition, Subtraction
- **"MD are twins, AS are twins"** — Multiplication/Division have equal priority; Addition/Subtraction have equal priority. Twins walk left to right together.
- **"Innermost first, outermost last"** — For nested grouping symbols, always start from the deepest level
- **"Left to right for equals"** — When operations have the same priority, read left to right like a sentence
- **"Exponent means repeated multiplication, NOT base × power"** — 2³ = 2×2×2, not 2×3
- **"No parens around the negative? Only the positive is powered"** — -5² = -(5²) = -25, but (-5)² = 25

---

### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** Evaluate: 5 + 3 × 4²

- Step 1: Exponent first: 4² = 16
- Step 2: Multiplication: 3 × 16 = _____
- Step 3: Addition: 5 + _____ = _____

**Answer:** 3 × 16 = 48. Then 5 + 48 = **53**

**2.** Evaluate: (8 + 4) ÷ 3 + 2 × 5

- Step 1: Parentheses: 8 + 4 = _____
- Step 2: Division: _____ ÷ 3 = _____
- Step 3: Multiplication: 2 × 5 = _____
- Step 4: Addition: _____ + _____ = _____

**Answer:** 12 ÷ 3 = 4. 2 × 5 = 10. Then 4 + 10 = **14**

**3.** Evaluate: 3 × (2 + 5)² - 100

- Step 1: Parentheses: 2 + 5 = _____
- Step 2: Exponent: _____² = _____
- Step 3: Multiplication: 3 × _____ = _____
- Step 4: Subtraction: _____ - 100 = _____

**Answer:** 7² = 49. 3 × 49 = 147. Then 147 - 100 = **47**

**4.** Evaluate: 48 ÷ (2³ × 3) + 5 - 1

- Step 1: Exponent inside parentheses: 2³ = _____
- Step 2: Parentheses multiplication: _____ × 3 = _____
- Step 3: Division: 48 ÷ _____ = _____
- Step 4: Left to right: _____ + 5 - 1 = _____

**Answer:** 2³ = 8. 8 × 3 = 24. 48 ÷ 24 = 2. Then 2 + 5 - 1 = **6**

**5.** A government office computes a bonus using: Base × (1 + Rate)² - Deduction. If Base = 50,000, Rate = 0.1, Deduction = 5,000, find the bonus.

- Step 1: Parentheses: 1 + _____ = _____
- Step 2: Exponent: _____² = _____
- Step 3: Multiplication: _____ × _____ = _____
- Step 4: Subtraction: _____ - _____ = _____

**Answer:** 1 + 0.1 = 1.1. 1.1² = 1.21. 50,000 × 1.21 = 60,500. Then 60,500 - 5,000 = **₱55,500**

---

### Which Method?

For each problem, identify the first operation to perform and solve.

**1.** 7 + 2 × (3 + 1)
- **Type:** Parentheses first, then multiplication, then addition
- **Answer:** 15
- **Why:** (3 + 1) = 4, then 2 × 4 = 8, then 7 + 8 = 15.

**2.** 36 ÷ 9 × 4 - 2
- **Type:** Multiplication/Division left to right (no parentheses, no exponents)
- **Answer:** 14
- **Why:** 36 ÷ 9 = 4, then 4 × 4 = 16, then 16 - 2 = 14.

**3.** -4² + 3³
- **Type:** Exponents first (watch negative sign without parentheses)
- **Answer:** 11
- **Why:** -4² = -(16) = -16. 3³ = 27. Then -16 + 27 = 11.

**4.** (15 + 5) / (4 + 1) + 2²
- **Type:** Fraction bar as grouping symbol, then exponent, then addition
- **Answer:** 8
- **Why:** Numerator: 20. Denominator: 5. 20 ÷ 5 = 4. 2² = 4. Then 4 + 4 = 8.

**5.** 2 × 5 - 8 ÷ 4 + 1
- **Type:** Multiplication and division first (left to right), then addition/subtraction
- **Answer:** 9
- **Why:** 2 × 5 = 10. 8 ÷ 4 = 2. Then 10 - 2 + 1 = 9.

**6.** {[4 × (1 + 2)] - 7} × 2
- **Type:** Nested grouping symbols (innermost first)
- **Answer:** 10
- **Why:** (1 + 2) = 3. [4 × 3] = 12. {12 - 7} = 5. Then 5 × 2 = 10.

---

### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Apply PEMDAS priority correctly (parentheses → exponents → multiplication/division → addition/subtraction)
- [ ] Evaluate nested grouping symbols from innermost to outermost
- [ ] Distinguish between -x² and (-x)² and compute each correctly
- [ ] Process multiplication and division left to right at equal priority
- [ ] Process addition and subtraction left to right at equal priority
- [ ] Solve multi-step expressions combining all operation types

---

### Connections

How this topic connects to other areas of the CSE:

- **Exponents and Roots:** Order of operations dictates that exponents are evaluated before multiplication and addition — understanding PEMDAS priority is essential for correctly simplifying expressions with powers
- **Percentages:** Percentage formulas like discount = original × (1 − rate) require correct operation sequencing — computing the parentheses first, then multiplying, prevents errors in price calculations
- **Averages:** The mean formula (sum of values ÷ count) requires you to complete all additions in the numerator before dividing — a direct application of the fraction-bar-as-grouping-symbol rule
- **Word Problems:** Translating word problems into mathematical expressions demands correct placement of parentheses and operation priority — "5 more than 3 times a number" is 3x + 5, not (3)(x + 5)
- **Operations with Signed Numbers:** Combining sign rules with PEMDAS creates multi-layered problems where you must track both operation priority and sign changes simultaneously

### Mastery Checklist

After completing this lesson, you should be able to:
- ✅ State the PEMDAS/BODMAS priority order from memory
- ✅ Evaluate expressions with parentheses, exponents, multiplication, division, addition, and subtraction in the correct sequence
- ✅ Resolve tied operations (M/D and A/S) using the left-to-right rule
- ✅ Simplify nested grouping symbols from innermost to outermost
- ✅ Correctly distinguish between -x² and (-x)² in any expression
- ✅ Treat fraction bars as grouping symbols and simplify numerator/denominator separately
- ✅ Apply order of operations to expressions involving fractions, decimals, and integers
- ✅ Use estimation and last-digit checking to verify answers under time pressure
- ✅ Identify common PEMDAS errors in distractors and avoid them
- ✅ Solve CSE-style multi-step expressions efficiently within 1-2 minutes

---

## Worked Examples

### Example A: Multi-Operation Expression

**Problem:** Evaluate 4 × (3 + 2)² - 18 ÷ 3

**Solution:**
1. Parentheses: 3 + 2 = 5
2. Exponent: 5² = 25
3. Multiplication: 4 × 25 = 100
4. Division: 18 ÷ 3 = 6
5. Subtraction: 100 - 6 = **94**

### Example B: Nested Grouping Symbols

**Problem:** Evaluate {[2 × (5 + 1)] - 4} ÷ 2 + 3²

**Solution:**
1. Innermost parentheses: 5 + 1 = 6
2. Brackets: 2 × 6 = 12
3. Braces: 12 - 4 = 8
4. Division: 8 ÷ 2 = 4
5. Exponent: 3² = 9
6. Addition: 4 + 9 = **13**

### Example C: Fraction Bar as Grouping Symbol

**Problem:** Evaluate (5² - 1) / (4 + 2) + 2³

**Solution:**
1. Numerator exponent: 5² = 25
2. Numerator subtraction: 25 - 1 = 24
3. Denominator addition: 4 + 2 = 6
4. Division: 24 ÷ 6 = 4
5. Exponent: 2³ = 8
6. Addition: 4 + 8 = **12**

### Example D: Integer Signs with PEMDAS

**Problem:** Evaluate (-3)² + 4 × (-2) - (-6)

**Solution:**
1. Exponent: (-3)² = 9
2. Multiplication: 4 × (-2) = -8
3. Left to right: 9 + (-8) - (-6) = 9 - 8 + 6 = **7**

### Example E: CSE-Style Word Problem

**Problem:** A government office allocates ₱120,000 for supplies. They purchase 8 printers at ₱12,500 each and spend the remainder equally on 5 departments for office materials. How much does each department receive?

**Solution:**
1. Expression: (120,000 - 8 × 12,500) ÷ 5
2. Multiplication: 8 × 12,500 = 100,000
3. Parentheses subtraction: 120,000 - 100,000 = 20,000
4. Division: 20,000 ÷ 5 = **₱4,000 per department**

## Key Takeaways

- PEMDAS/BODMAS provides a universal, unambiguous order for evaluating mathematical expressions: Parentheses → Exponents → Multiplication/Division (left to right) → Addition/Subtraction (left to right)
- Multiplication and Division share equal priority — the mnemonic letter order does NOT mean M comes before D. The same applies to Addition and Subtraction.
- Grouping symbols (parentheses, brackets, braces, fraction bars) always override normal priority — solve innermost groups first
- The negative sign without parentheses is NOT part of the base: -3² = -9, but (-3)² = 9
- Writing every intermediate step prevents cascading errors in multi-operation expressions
- Estimation and last-digit checking are powerful verification tools under CSE time pressure
- Every other math topic on the CSE (percentages, ratios, averages, algebra) depends on correct operation sequencing

## Summary

Order of operations is the foundational rule system that ensures every mathematical expression has exactly one correct interpretation. The PEMDAS mnemonic — Parentheses, Exponents, Multiplication/Division (left to right), Addition/Subtraction (left to right) — provides the priority hierarchy that governs all computation. The most critical insight is that M and D share equal priority (resolved left to right), as do A and S — the mnemonic's letter sequence does not imply priority between tied operations.

For the Philippine Civil Service Examination, order of operations questions test whether you can systematically evaluate expressions combining multiple operation types without skipping steps or misapplying priority rules. Common distractors are designed around predictable errors: performing addition before multiplication, treating M as higher than D, or mishandling negative signs with exponents. The antidote is disciplined step-by-step evaluation, estimation for verification, and recognition of these error patterns in answer choices.

Mastery of this topic directly supports every other numerical ability subtopic on the CSE — from percentage calculations and ratio simplification to average computation and algebraic word problems. An examinee who consistently applies PEMDAS correctly eliminates an entire category of careless errors across the exam.
