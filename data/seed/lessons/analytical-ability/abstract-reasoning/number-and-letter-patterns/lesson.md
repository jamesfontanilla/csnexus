# Number and Letter Patterns

## Introduction

Number and letter patterns test your ability to identify the rule governing a sequence and predict what comes next. Unlike shape patterns that rely on visual transformations, these patterns require recognizing mathematical relationships, alphabetical progressions, and combined alphanumeric rules.

On the Philippine Civil Service Examination, number and letter pattern questions appear in the Analytical Ability section under Abstract Reasoning. They range from simple arithmetic sequences to complex multi-rule patterns that combine numerical and alphabetical logic.

**Why these patterns matter for the CSE:**

- They measure logical reasoning and pattern recognition without requiring advanced math
- They test mental flexibility — switching between number rules and letter rules
- They evaluate your ability to work under time pressure with sequential data
- They appear consistently across both Professional and Sub-Professional levels

**Why memorization fails here:**

Sequences are generated from infinite combinations of starting values, step sizes, and rules. You cannot memorize answers. Instead, you must develop the skill of computing differences, identifying ratios, and tracking letter positions. Speed comes from practiced recognition of common pattern types.

**Common mistakes examinees make:**

- Computing only the first difference and assuming the pattern is arithmetic
- Forgetting that letters wrap around (after Z comes A)
- Confusing multiplication patterns with addition patterns when numbers grow quickly
- Not checking whether a sequence has two interleaved sub-sequences
- Rushing to answer without verifying the rule works for ALL given terms

## Learning Objectives

After this lesson, learners should be able to:

- Identify arithmetic sequences (constant addition or subtraction)
- Identify geometric sequences (constant multiplication or division)
- Recognize quadratic patterns (increasing differences)
- Identify letter sequences with constant or variable steps
- Recognize mixed alphanumeric patterns with dual rules
- Detect interleaved sequences (two patterns alternating)
- Apply systematic difference analysis to find hidden rules
- Solve CSE-style number and letter pattern questions within time constraints

## 1. Number Sequences — Fundamentals

### 1.1 Arithmetic Sequences (Constant Difference)

The simplest pattern: each term differs from the previous by a fixed amount.

**How to identify:** Compute the difference between consecutive terms. If all differences are equal, it is arithmetic.

| Sequence | Differences | Rule |
|----------|-------------|------|
| 3, 7, 11, 15, **19** | +4, +4, +4, +4 | Add 4 each step |
| 50, 43, 36, 29, **22** | -7, -7, -7, -7 | Subtract 7 each step |
| 5, 10, 15, 20, **25** | +5, +5, +5, +5 | Add 5 (skip counting) |

**Technique:** Always compute differences first. This is your default starting move for any number sequence.

<svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="37" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">5</text>
  <rect x="75" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="102" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">12</text>
  <rect x="140" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="167" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">19</text>
  <rect x="205" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="232" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">26</text>
  <rect x="270" y="30" width="55" height="35" fill="#fff3cd" stroke="#ffc107" rx="4" stroke-dasharray="4,2"/>
  <text x="297" y="52" text-anchor="middle" font-size="16" fill="#856404" font-family="sans-serif">?</text>
  <text x="70" y="22" text-anchor="middle" font-size="11" fill="#28a745">+7</text>
  <text x="135" y="22" text-anchor="middle" font-size="11" fill="#28a745">+7</text>
  <text x="200" y="22" text-anchor="middle" font-size="11" fill="#28a745">+7</text>
  <text x="265" y="22" text-anchor="middle" font-size="11" fill="#28a745">+7</text>
</svg>

**Answer:** 26 + 7 = **33**. The constant difference is +7.

### 1.2 Geometric Sequences (Constant Ratio)

Each term is multiplied by a fixed factor to get the next term.

**How to identify:** If differences are NOT constant but ratios between consecutive terms ARE constant, it is geometric.

| Sequence | Ratios | Rule |
|----------|--------|------|
| 2, 6, 18, 54, **162** | ×3, ×3, ×3, ×3 | Multiply by 3 |
| 4, 8, 16, 32, **64** | ×2, ×2, ×2, ×2 | Multiply by 2 |
| 1, 5, 25, 125, **625** | ×5, ×5, ×5, ×5 | Multiply by 5 |

**Key signal:** Numbers grow rapidly. If the sequence doubles or triples quickly, check for multiplication.

<svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="37" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">3</text>
  <rect x="85" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="112" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">9</text>
  <rect x="160" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="187" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">27</text>
  <rect x="235" y="30" width="55" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="262" y="52" text-anchor="middle" font-size="14" fill="#212529" font-family="monospace">81</text>
  <rect x="310" y="30" width="55" height="35" fill="#fff3cd" stroke="#ffc107" rx="4" stroke-dasharray="4,2"/>
  <text x="337" y="52" text-anchor="middle" font-size="16" fill="#856404" font-family="sans-serif">?</text>
  <text x="75" y="22" text-anchor="middle" font-size="11" fill="#dc3545">×3</text>
  <text x="150" y="22" text-anchor="middle" font-size="11" fill="#dc3545">×3</text>
  <text x="225" y="22" text-anchor="middle" font-size="11" fill="#dc3545">×3</text>
  <text x="300" y="22" text-anchor="middle" font-size="11" fill="#dc3545">×3</text>
</svg>

**Answer:** 81 × 3 = **243**. The constant ratio is ×3.

### 1.3 Perfect Squares and Cubes

Sequences based on n², n³, or other power functions.

| Sequence | Pattern | Rule |
|----------|---------|------|
| 1, 4, 9, 16, **25** | 1², 2², 3², 4², 5² | Perfect squares |
| 1, 8, 27, 64, **125** | 1³, 2³, 3³, 4³, 5³ | Perfect cubes |
| 4, 9, 16, 25, **36** | 2², 3², 4², 5², 6² | Squares starting from 2 |

**How to identify:** Check if each term is a perfect square or cube. Memorize squares up to 15² = 225 and cubes up to 6³ = 216.

**Quick reference — squares to memorize:**

| n | n² | n | n² |
|---|-----|---|-----|
| 1 | 1 | 9 | 81 |
| 2 | 4 | 10 | 100 |
| 3 | 9 | 11 | 121 |
| 4 | 16 | 12 | 144 |
| 5 | 25 | 13 | 169 |
| 6 | 36 | 14 | 196 |
| 7 | 49 | 15 | 225 |
| 8 | 64 | | |

### 1.4 Increasing Differences (Quadratic Patterns)

The differences between terms are not constant, but the differences OF the differences (second differences) are constant.

| Sequence | First Diffs | Second Diffs | Rule |
|----------|-------------|--------------|------|
| 2, 3, 5, 8, 12, **17** | +1, +2, +3, +4, +5 | +1, +1, +1, +1 | Diffs increase by 1 |
| 1, 4, 9, 16, 25 | +3, +5, +7, +9 | +2, +2, +2 | Diffs increase by 2 |

**Technique:** When first differences are not constant, compute second differences. If those are constant, you have a quadratic pattern.

<svg width="450" height="100" viewBox="0 0 450 100" xmlns="http://www.w3.org/2000/svg">
  <text x="225" y="15" text-anchor="middle" font-size="11" fill="#6c757d">First differences increase: +2, +3, +4, +5, +6</text>
  <rect x="10" y="40" width="50" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="35" y="62" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">1</text>
  <rect x="75" y="40" width="50" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="100" y="62" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">3</text>
  <rect x="140" y="40" width="50" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="165" y="62" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">6</text>
  <rect x="205" y="40" width="50" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="230" y="62" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">10</text>
  <rect x="270" y="40" width="50" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="295" y="62" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">15</text>
  <rect x="335" y="40" width="50" height="35" fill="#fff3cd" stroke="#ffc107" rx="4" stroke-dasharray="4,2"/>
  <text x="360" y="62" text-anchor="middle" font-size="16" fill="#856404" font-family="sans-serif">?</text>
  <text x="67" y="88" text-anchor="middle" font-size="10" fill="#28a745">+2</text>
  <text x="132" y="88" text-anchor="middle" font-size="10" fill="#28a745">+3</text>
  <text x="197" y="88" text-anchor="middle" font-size="10" fill="#28a745">+4</text>
  <text x="262" y="88" text-anchor="middle" font-size="10" fill="#28a745">+5</text>
  <text x="327" y="88" text-anchor="middle" font-size="10" fill="#28a745">+6</text>
</svg>

**Answer:** 15 + 6 = **21**. These are triangular numbers (sum of first n natural numbers).

## 2. Letter Sequences

### 2.1 Constant Step Forward

Letters advance by a fixed number of positions in the alphabet.

**Key tool:** Assign each letter a number (A=1, B=2, ... Z=26). Convert to numbers, find the pattern, convert back.

| Sequence | Positions | Step | Next |
|----------|-----------|------|------|
| A, C, E, G, **I** | 1, 3, 5, 7, 9 | +2 | I (9) |
| B, E, H, K, **N** | 2, 5, 8, 11, 14 | +3 | N (14) |
| D, H, L, P, **T** | 4, 8, 12, 16, 20 | +4 | T (20) |

**Technique:** Convert letters to positions, then treat it as a number sequence.

### 2.2 Constant Step Backward

Letters move backward through the alphabet.

| Sequence | Positions | Step | Next |
|----------|-----------|------|------|
| Z, X, V, T, **R** | 26, 24, 22, 20, 18 | -2 | R (18) |
| T, Q, N, K, **H** | 20, 17, 14, 11, 8 | -3 | H (8) |

### 2.3 Increasing Steps

The gap between letters grows by 1 each time.

| Sequence | Positions | Gaps | Next |
|----------|-----------|------|------|
| A, B, D, G, K, **P** | 1, 2, 4, 7, 11, 16 | +1, +2, +3, +4, +5 | P (16) |
| C, D, F, I, M, **R** | 3, 4, 6, 9, 13, 18 | +1, +2, +3, +4, +5 | R (18) |

**Technique:** When letter gaps are not constant, compute the gaps and check if THEY form a pattern.

### 2.4 Vowel and Special Sequences

Some patterns use only vowels (A, E, I, O, U) or follow other alphabetical subsets.

| Sequence | Rule |
|----------|------|
| A, E, I, O, **U** | Vowels in order |
| B, D, F, H, **J** | Even-positioned consonants (+2) |
| Z, Y, X, W, **V** | Reverse alphabet |

## 3. Mixed Alphanumeric Patterns

### 3.1 Parallel Rules

The letter and number each follow their own independent rule.

| Sequence | Letter Rule | Number Rule | Next |
|----------|-------------|-------------|------|
| A1, B2, C3, D4, **E5** | +1 position | +1 | E5 |
| A2, C4, E8, G16, **I32** | +2 positions | ×2 | I32 |
| Z1, X4, V9, T16, **R25** | -2 positions | perfect squares | R25 |

**Technique:** Separate the letter part from the number part. Analyze each independently.

<svg width="400" height="80" viewBox="0 0 400 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="25" width="60" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="40" y="47" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">A2</text>
  <rect x="85" y="25" width="60" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="115" y="47" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">C4</text>
  <rect x="160" y="25" width="60" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="190" y="47" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">E8</text>
  <rect x="235" y="25" width="60" height="35" fill="#f8f9fa" stroke="#dee2e6" rx="4"/>
  <text x="265" y="47" text-anchor="middle" font-size="13" fill="#212529" font-family="monospace">G16</text>
  <rect x="310" y="25" width="60" height="35" fill="#fff3cd" stroke="#ffc107" rx="4" stroke-dasharray="4,2"/>
  <text x="340" y="47" text-anchor="middle" font-size="16" fill="#856404" font-family="sans-serif">?</text>
  <text x="200" y="75" text-anchor="middle" font-size="10" fill="#6c757d">Letters: +2 positions | Numbers: ×2</text>
</svg>

**Answer:** G→I (position 7→9, +2) and 16×2=32. Next: **I32**.

### 3.2 Interleaved Sequences

Two separate sequences alternate positions: odd-indexed terms follow one rule, even-indexed terms follow another.

| Full Sequence | Odd Terms | Even Terms |
|---------------|-----------|------------|
| 2, 10, 5, 13, 8, 16, **11** | 2, 5, 8, 11 (+3) | 10, 13, 16 (+3) |
| 1, 20, 4, 17, 7, 14, **10** | 1, 4, 7, 10 (+3) | 20, 17, 14 (-3) |

**How to identify:** If differences alternate between two values or seem inconsistent, try separating odd and even positions.

### 3.3 Letter Pairs

Sequences of two-letter groups that follow a pattern.

| Sequence | Rule | Next |
|----------|------|------|
| AB, CD, EF, GH, **IJ** | Consecutive pairs, advancing by 2 | IJ |
| AZ, BY, CX, DW, **EV** | First +1, second -1 | EV |

## 4. Advanced Patterns (Hard)

### 4.1 Alternating Operations
> 🤔 **Why does this work?** The principle behind this operation follows from the fundamental properties of arithmetic. Understanding the "why" — not just the "how" — lets you recognize when to apply this method in unfamiliar problem contexts on the CSE.


The rule alternates between two operations.

| Sequence | Operations | Next |
|----------|-----------|------|
| 3, 6, 4, 8, 6, **12** | ×2, -2, ×2, -2, ×2 | 12 |
| 5, 8, 4, 7, 3, **6** | +3, -4, +3, -4, +3 | 6 |
| 2, 6, 7, 21, 22, **66** | ×3, +1, ×3, +1, ×3 | 66 |

**Technique:** If a single rule does not work, try alternating two operations. Check: does the pattern repeat every 2 steps?


> ⚠️ **Misconception:** "The formula always works the same way regardless of the problem context."

> **Why it fails:** CSE problems often present variations where the standard formula must be adapted. Blindly applying a memorized formula without checking the context leads to systematic errors.

> **Correct model:** Always read the problem to identify what type of relationship exists (direct, inverse, part-whole, etc.), then apply the appropriate formula. Verify your answer makes sense in the problem's context before selecting it.

### 4.2 Triple Operation Cycles

Three operations cycle: op1, op2, op3, op1, op2, op3...

| Sequence | Cycle | Next |
|----------|-------|------|
| 2, 5, 10, 7, 10, 20, **17** | +3, ×2, -3, +3, ×2, -3 | 17 |

**Technique:** If two operations do not explain the pattern, try three. Group terms in threes and check if each group follows the same internal pattern.


### Check Your Understanding

**1.** What is the key concept from this section? → **Review the preceding content to recall the main principle**

**2.** How would you apply this concept to a practical problem? → **Identify the type of relationship, set up the correct equation, and solve step by step**

**3.** What common mistake should you avoid here? → **Check the Common Mistakes section — verify your answer doesn't fall into these traps**

---

### 4.3 Fibonacci-Like Sequences
> 🤔 **Why does this work?** When you follow this procedure, you're exploiting a mathematical invariant — something that stays constant regardless of how you manipulate the numbers. Identifying that invariant is the key to solving problems efficiently rather than memorizing steps.


Each term is the sum of the two preceding terms.

| Sequence | Rule | Next |
|----------|------|------|
| 1, 1, 2, 3, 5, **8** | a + b = c | 3 + 5 = 8 |
| 2, 3, 5, 8, 13, **21** | a + b = c | 8 + 13 = 21 |
| 1, 4, 5, 9, 14, **23** | a + b = c | 9 + 14 = 23 |

**How to identify:** Check if each term equals the sum of the two before it.

### 4.4 Mirror/Palindrome Patterns

The sequence goes forward to a center point, then reverses.

| Sequence | Pattern | Next |
|----------|---------|------|
| A, B, C, D, C, **B** | Forward to D, then backward | B |
| 1, 3, 5, 7, 5, **3** | Up to 7, then back down | 3 |

### 4.5 Powers and Exponentials
> 🤔 **Why does this work?** This shortcut works because it's a special case of the more general rule. By understanding the underlying principle, you can verify your answer logically even if you forget the exact formula under exam pressure.


Terms are powers of a base number.

| Sequence | Pattern | Next |
|----------|---------|------|
| 2, 4, 8, 16, **32** | 2¹, 2², 2³, 2⁴, 2⁵ | 32 |
| 3, 9, 27, 81, **243** | 3¹, 3², 3³, 3⁴, 3⁵ | 243 |
| 4, 16, 64, 256, **1024** | 4¹, 4², 4³, 4⁴, 4⁵ | 1024 |

### 4.6 Prime Number Sequences

Terms are consecutive prime numbers.

| Sequence | Next |
|----------|------|
| 2, 3, 5, 7, **11** | 11 |
| 11, 13, 17, 19, **23** | 23 |
| 29, 31, 37, 41, **43** | 43 |

**Tip:** Memorize primes up to 50: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47.

## 5. Problem-Solving Strategy

Use this systematic approach for any number or letter pattern question:

**Step 1: Compute first differences** (5 seconds)

Subtract each term from the next. If all differences are equal → arithmetic sequence. Done.

**Step 2: Check for constant ratio** (5 seconds)

Divide each term by the previous. If all ratios are equal → geometric sequence. Done.

**Step 3: Compute second differences** (5 seconds)

If first differences are not constant, compute differences of the differences. If constant → quadratic pattern.

**Step 4: Check for alternating or interleaved patterns** (10 seconds)

- Do differences alternate between two values? → Alternating operations
- Separate odd and even positions — do they form independent sequences?

**Step 5: Check for special sequences** (5 seconds)

- Are terms perfect squares? Cubes? Primes? Fibonacci sums?
- For letters: convert to positions and repeat steps 1-4.

**Step 6: For mixed patterns** (10 seconds)

Separate the letter component from the number component. Analyze each independently.

**Time budget:** You should solve Easy questions in 15-20 seconds, Medium in 30-40 seconds, and Hard in 45-60 seconds.

## 6. Common Traps and How to Avoid Them

| Trap | Example | How to Avoid |
|------|---------|--------------|
| Assuming arithmetic when it is geometric | 2, 4, 8, 16 (not +2, +4, +8 — it is ×2) | Always check ratios if differences grow |
| Missing interleaved sequences | 1, 10, 2, 20, 3, 30 | If diffs seem random, split odd/even |
| Forgetting letter wrapping | After Z comes A (position 27 = 1) | Always use modulo 26 |
| Confusing n² with 2n | 1, 4, 9, 16 vs 2, 4, 6, 8 | Check: is 4 = 2² or 2×2? Context matters |
| Not verifying the rule on ALL terms | Finding +3 from first two terms but it fails on term 3 | Always verify across the entire sequence |

## 7. Practice Tips

1. **Build speed with mental math.** Practice computing differences and ratios without writing them down.
2. **Memorize key sequences.** Squares (1-225), cubes (1-216), primes (2-47), Fibonacci (1, 1, 2, 3, 5, 8, 13, 21, 34, 55).
3. **Know your alphabet positions.** At minimum, memorize: A=1, E=5, I=9, J=10, N=14, O=15, S=19, T=20, Z=26.
4. **Practice the "split and analyze" technique.** For any mixed pattern, immediately separate components.
5. **When stuck, try the answer choices.** Work backward — if the answer is X, what rule would produce it from the last given term?

> ?? **Why does this work?** Understanding the principle helps you choose the right method under exam pressure, even when the question format changes.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


### Guided Practice

1. Identify the question type.
2. Set up the correct model or formula.
3. Solve step by step and verify reasonableness.


### Which Method?

For each problem, decide first: ratio/proportion, arithmetic pattern, grammar rule, or context-clue strategy. Then solve using that method.


### Before You Practice

- I can identify the problem type before computing.
- I can explain why my chosen method is appropriate.
- I can check my final answer against context.


### Connections

This lesson connects to related CSE topics where the same reasoning pattern appears in a different surface form. Practice transfer by mapping structure, not just wording.


### Mastery Checklist

- [ ] I can solve representative items accurately and quickly.
- [ ] I can explain common traps and how to avoid them.
- [ ] I can transfer this method to mixed-question sets.

### Extended Practice Bank

The drills below strengthen transfer for **number and letter patterns** under timed CSE conditions.

**Drill 1.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 2.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 3.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 4.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 5.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 6.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 7.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 8.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 9.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 10.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 11.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 12.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 13.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 14.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 15.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 16.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 17.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 18.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 19.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 20.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 21.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 22.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 23.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 24.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 25.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 26.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 27.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 28.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 29.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 30.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 31.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 32.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 33.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 34.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 35.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 36.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 37.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 38.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 39.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 40.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 41.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 42.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 43.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 44.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 45.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 46.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 47.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 48.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 49.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 50.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 51.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 52.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 53.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 54.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

**Drill 55.** Identify the core pattern/rule before solving.
- Step 1: Classify the item type in one phrase.
- Step 2: State the rule you will test.
- Step 3: Solve, then verify against all given terms/clauses.
- Quick check: Could a different rule also fit all evidence?
- Reflection: Name one trap option and why it is wrong.

