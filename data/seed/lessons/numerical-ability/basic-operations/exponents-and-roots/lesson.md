# Exponents and Roots

## Explanations

### Introduction

**Exponents and roots** are two sides of the same coin — exponents express repeated multiplication, and roots reverse that process. When you write 2⁵ = 32, you are using an exponent. When you ask "what number multiplied by itself gives 25?" you are finding a root (√25 = 5). Together, they form the language of powers that underpins science, engineering, finance, and technology.

In the **Philippine Civil Service Examination (CSE)**, exponents and roots appear in direct computation items, scientific notation problems, estimation questions, and as sub-steps in algebra and data interpretation. Government employees encounter these concepts when working with population growth rates, compound interest on government bonds, unit conversions in engineering reports, and data storage calculations in IT departments.

This subtopic covers five critical areas:
- **Laws of Exponents** — the rules that govern how powers combine
- **Squares and Square Roots** — perfect squares, simplification, and estimation
- **Cubes and Cube Roots** — perfect cubes and their inverses
- **Scientific Notation** — expressing very large or very small numbers compactly
- **Rational Exponents and Radicals** — fractional powers and radical expressions

### Why Exponents and Roots Are Tested in the CSE

The Civil Service Exam tests exponents and roots because:
- Government financial analysts compute compound interest using exponential formulas
- IT personnel work with powers of 2 daily (KB, MB, GB, TB are all powers of 1024)
- Engineers and scientists express measurements in scientific notation (distances, populations, budgets)
- Statistical reports use squared deviations (variance) and square roots (standard deviation)
- Budget projections involving growth rates require understanding of exponential increase
- Area and volume calculations in public works require squares and cubes
- The ability to simplify exponential expressions quickly indicates strong numerical fluency

### Common Mistakes Examinees Make

1. **Adding exponents when multiplying bases** — computing 2³ × 3² as 6⁵ instead of keeping bases separate
2. **Misunderstanding negative exponents** — thinking 2⁻³ equals -8 instead of 1/8
3. **Confusing the zero exponent** — believing x⁰ = 0 instead of x⁰ = 1
4. **Incorrect radical simplification** — writing √50 = 25 instead of 5√2
5. **Misplacing the decimal in scientific notation** — writing 3,400 as 34 × 10² instead of 3.4 × 10³
6. **Multiplying base and exponent** — computing 5³ as 15 instead of 125
7. **Forgetting to apply exponent to all factors** — writing (2x)³ as 2x³ instead of 8x³
8. **Confusing square root with division by 2** — thinking √16 = 8 instead of 4

### Learning Objectives

After this lesson, you should be able to:
- Evaluate exponential expressions correctly for any integer exponent
- Apply all seven laws of exponents to simplify expressions
- Identify perfect squares and perfect cubes from memory
- Compute and estimate square roots and cube roots
- Simplify radical expressions including rationalizing denominators
- Convert between radical notation and rational exponents
- Express numbers in scientific notation and perform operations
- Solve CSE-style exponent and root questions efficiently under time pressure

---

### 4.1 What Are Exponents?

#### Definition

An **exponent** (also called a **power** or **index**) tells you how many times to multiply a number by itself. The number being multiplied is the **base**, and the small raised number is the **exponent**.

```
base^exponent = result
  2^5         = 2 × 2 × 2 × 2 × 2 = 32
```

We read 2⁵ as "two to the fifth power" or "two raised to five."

#### Terminology

| Term | Definition | Example |
|------|-----------|---------|
| Base | The number being multiplied repeatedly | In 3⁴, the base is 3 |
| Exponent | How many times the base is used as a factor | In 3⁴, the exponent is 4 |
| Power | The entire expression or its result | 3⁴ = 81 (81 is the fourth power of 3) |

#### Special Powers

| Power Name | Meaning | Example |
|-----------|---------|---------|
| Squared (²) | Base × Base | 5² = 5 × 5 = 25 |
| Cubed (³) | Base × Base × Base | 4³ = 4 × 4 × 4 = 64 |
| To the fourth (⁴) | Base used 4 times | 2⁴ = 2 × 2 × 2 × 2 = 16 |
| To the nth | Base used n times | aⁿ = a × a × ... × a (n times) |

> 🤔 **Why does this work?** Exponentiation is defined as repeated multiplication
> because it captures a pattern that arises naturally: computing areas (length × length),
> volumes (length × length × length), and compound growth (principal × rate × rate × ...).
> The exponent simply counts how many times the base appears as a factor, making it a
> compact notation for a process that would otherwise require writing the same number
> many times.

#### Powers of Common Bases

Memorize these — they appear constantly on the CSE:

**Powers of 2:**
```
2¹ = 2      2² = 4      2³ = 8      2⁴ = 16
2⁵ = 32     2⁶ = 64     2⁷ = 128    2⁸ = 256
2⁹ = 512    2¹⁰ = 1,024
```

**Powers of 3:**
```
3¹ = 3      3² = 9      3³ = 27     3⁴ = 81
3⁵ = 243    3⁶ = 729
```

**Powers of 5:**
```
5¹ = 5      5² = 25     5³ = 125    5⁴ = 625
```

**Powers of 10:**
```
10¹ = 10         10² = 100        10³ = 1,000
10⁴ = 10,000    10⁵ = 100,000    10⁶ = 1,000,000
```

#### Real-Life Applications

| Context | Example |
|---------|---------|
| Computer storage | 2¹⁰ = 1,024 bytes = 1 KB |
| Population growth | Population × (1.02)ⁿ for n years at 2% growth |
| Area calculation | Side² = area of a square |
| Volume calculation | Side³ = volume of a cube |
| Compound interest | Principal × (1 + rate)ⁿ |
| Scientific measurement | Speed of light ≈ 3 × 10⁸ m/s |

> ⚠️ **Misconception:** "To compute 5³, multiply 5 × 3 = 15."
>
> **Why it fails:** 5³ means 5 × 5 × 5 = 125, not 5 × 3. The exponent tells you
> how many times to use the base as a factor, not what to multiply the base by.
> If 5³ = 15 were true, then 5² would equal 10, but we know 5² = 25.
>
> **Correct model:** The exponent is a counter, not a multiplier. Read 5³ as
> "5 used as a factor 3 times" → 5 × 5 × 5 = 125.

---

### 4.2 Laws of Exponents

The laws of exponents are the rules that let you simplify expressions without expanding every power. These are **non-negotiable** for the CSE — nearly every exponent problem requires at least one of these rules.

#### Rule 1: Product of Powers (Same Base)

When multiplying powers with the **same base**, add the exponents.

```
a^m × a^n = a^(m+n)
```

**Why it works:** 2³ × 2⁴ = (2×2×2) × (2×2×2×2) = 2⁷ — you have 3 + 4 = 7 factors of 2.

**Examples:**
- 5² × 5³ = 5^(2+3) = 5⁵ = 3,125
- x⁴ × x⁶ = x^(4+6) = x¹⁰
- 10³ × 10² = 10⁵ = 100,000

**Common Error:** Do NOT multiply the bases. 5² × 5³ ≠ 25⁵.

#### Rule 2: Quotient of Powers (Same Base)

When dividing powers with the **same base**, subtract the exponents.

```
a^m ÷ a^n = a^(m-n)    (where a ≠ 0)
```

**Why it works:** 2⁵ ÷ 2² = (2×2×2×2×2) ÷ (2×2) = 2×2×2 = 2³ — you cancel 2 factors, leaving 5-2=3.

**Examples:**
- 7⁶ ÷ 7² = 7^(6-2) = 7⁴ = 2,401
- 10⁸ ÷ 10³ = 10⁵ = 100,000
- x⁹ ÷ x⁴ = x⁵

#### Rule 3: Power of a Power

When raising a power to another power, multiply the exponents.

```
(a^m)^n = a^(m×n)
```

**Why it works:** (2³)² = 2³ × 2³ = 2⁶ — you have the exponent 3 repeated 2 times.

**Examples:**
- (3²)⁴ = 3^(2×4) = 3⁸ = 6,561
- (x⁵)³ = x^(5×3) = x¹⁵
- (10²)³ = 10⁶ = 1,000,000

#### Rule 4: Power of a Product

When raising a product to a power, apply the exponent to each factor.

```
(a × b)^n = a^n × b^n
```

**Examples:**
- (2 × 3)⁴ = 2⁴ × 3⁴ = 16 × 81 = 1,296
- (5x)³ = 5³ × x³ = 125x³
- (3y²)² = 3² × (y²)² = 9y⁴

**Common Error:** (2x)³ ≠ 2x³. You must cube BOTH the 2 and the x: (2x)³ = 8x³.

#### Rule 5: Power of a Quotient

When raising a fraction to a power, apply the exponent to both numerator and denominator.

```
(a/b)^n = a^n / b^n    (where b ≠ 0)
```

**Examples:**
- (2/3)⁴ = 2⁴/3⁴ = 16/81
- (x/5)² = x²/25
- (3/4)³ = 27/64

#### Rule 6: Zero Exponent

Any non-zero number raised to the power of zero equals 1.

```
a⁰ = 1    (where a ≠ 0)
```

**Why it works:** By the quotient rule, a³ ÷ a³ = a^(3-3) = a⁰. But a³ ÷ a³ = 1. Therefore a⁰ = 1.

**Examples:**
- 5⁰ = 1
- 100⁰ = 1
- (-7)⁰ = 1
- (999,999)⁰ = 1

**Critical:** 0⁰ is undefined (not tested on the CSE). Every other base raised to 0 equals 1.

> 🤔 **Why does this work?** The zero exponent rule is not an arbitrary definition —
> it is forced by the quotient rule. If a^m ÷ a^m must equal a^(m-m) = a⁰ by the
> quotient rule, and any number divided by itself equals 1, then a⁰ must equal 1.
> The rule preserves internal consistency across all exponent laws.

#### Rule 7: Negative Exponent

A negative exponent means "take the reciprocal."

```
a^(-n) = 1/a^n    (where a ≠ 0)
```

**Why it works:** By the quotient rule, a² ÷ a⁵ = a^(2-5) = a⁻³. But expanding: (a×a)/(a×a×a×a×a) = 1/(a×a×a) = 1/a³. Therefore a⁻³ = 1/a³.

**Examples:**
- 2⁻³ = 1/2³ = 1/8
- 5⁻² = 1/5² = 1/25
- 10⁻⁴ = 1/10⁴ = 1/10,000 = 0.0001
- (3/4)⁻² = (4/3)² = 16/9

**Common Error:** 2⁻³ ≠ -8. The negative exponent means reciprocal, NOT negative result.

> ⚠️ **Misconception:** "A negative exponent makes the result negative."
>
> **Why it fails:** 2⁻³ = 1/2³ = 1/8 (positive, not -8). Similarly, 5⁻² = 1/25
> (positive, not -25). The negative sign in the exponent controls size (making the
> number a fraction), not the sign of the result.
>
> **Correct model:** A negative exponent means "reciprocal" — it flips the base to
> the denominator. The result's sign depends only on the base's sign and whether the
> exponent is odd or even, not on whether the exponent is negative.

#### Summary of All Seven Laws

| Law | Rule | Example |
|-----|------|---------|
| Product of Powers | a^m × a^n = a^(m+n) | 2³ × 2⁴ = 2⁷ |
| Quotient of Powers | a^m ÷ a^n = a^(m-n) | 5⁶ ÷ 5² = 5⁴ |
| Power of a Power | (a^m)^n = a^(mn) | (3²)⁴ = 3⁸ |
| Power of a Product | (ab)^n = a^n × b^n | (2x)³ = 8x³ |
| Power of a Quotient | (a/b)^n = a^n/b^n | (2/3)⁴ = 16/81 |
| Zero Exponent | a⁰ = 1 | 7⁰ = 1 |
| Negative Exponent | a^(-n) = 1/a^n | 4⁻² = 1/16 |

---

### 4.3 Positive, Zero, and Negative Exponents

Understanding the full spectrum of exponents — positive, zero, and negative — reveals a beautiful pattern.

#### The Exponent Pattern

Look at powers of 2 as the exponent decreases:

```
2⁴ = 16
2³ = 8     (÷2)
2² = 4     (÷2)
2¹ = 2     (÷2)
2⁰ = 1     (÷2)
2⁻¹ = 1/2  (÷2)
2⁻² = 1/4  (÷2)
2⁻³ = 1/8  (÷2)
```

Each time the exponent decreases by 1, the value is divided by the base. This pattern makes zero and negative exponents inevitable — they are not arbitrary definitions but natural consequences of the pattern.

#### Positive Exponents

Positive exponents mean straightforward repeated multiplication:
- 3⁴ = 3 × 3 × 3 × 3 = 81
- 10³ = 10 × 10 × 10 = 1,000
- 7² = 7 × 7 = 49

#### Zero Exponent

The zero exponent always yields 1 (for any non-zero base):
- 15⁰ = 1
- (-3)⁰ = 1
- (2/5)⁰ = 1

#### Negative Exponents

Negative exponents yield fractions (reciprocals):
- 4⁻¹ = 1/4
- 3⁻² = 1/9
- 10⁻³ = 1/1,000 = 0.001
- 2⁻⁵ = 1/32

#### Moving Factors Between Numerator and Denominator

A negative exponent in the numerator becomes positive in the denominator, and vice versa:

```
x⁻³/y⁻² = y²/x³
```

**Example:** Simplify 5⁻²/3⁻¹
```
5⁻²/3⁻¹ = 3¹/5² = 3/25
```

#### Sign of the Result vs. Sign of the Exponent

The sign of the exponent tells you about size (big or small), NOT about positive/negative:
- 2³ = 8 (positive base, positive result)
- 2⁻³ = 1/8 (positive base, still positive result — just small)
- (-2)³ = -8 (negative base, negative result because odd exponent)
- (-2)⁴ = 16 (negative base, positive result because even exponent)

**Rule for negative bases:**
- Negative base with **even** exponent → positive result
- Negative base with **odd** exponent → negative result

**Examples:**
- (-3)² = 9 (even → positive)
- (-3)³ = -27 (odd → negative)
- (-1)¹⁰⁰ = 1 (even → positive)
- (-1)⁹⁹ = -1 (odd → negative)

**Critical distinction:** (-3)² = 9, but -3² = -(3²) = -9. Parentheses matter.

> 🤔 **Why does this work?** When a negative base is raised to an even power, the
> negative signs pair up and cancel: (-2)⁴ = (-2)×(-2)×(-2)×(-2) = (+4)×(+4) = 16.
> Each pair of negatives produces a positive. With an odd exponent, one negative is
> left unpaired: (-2)³ = (-2)×(-2)×(-2) = (+4)×(-2) = -8. The parity of the exponent
> determines whether all negatives cancel.

### Check Your Understanding

**1.** What is 7⁰? → **1** (any non-zero base raised to zero equals 1)
**2.** What is 3⁻² as a fraction? → **1/9** (negative exponent means reciprocal: 1/3² = 1/9)
**3.** Is (-2)⁴ positive or negative? → **Positive** (negative base with even exponent gives positive result)
**4.** Which law applies to simplify x⁵ × x³? → **Product of Powers** (same base → add exponents: x⁸)

---

### 4.4 Squares and Square Roots

#### What Is Squaring?

**Squaring** a number means multiplying it by itself. The result is called a **perfect square**.

```
n² = n × n
5² = 5 × 5 = 25
```

#### Perfect Squares (Memorize These)

```
1² = 1       2² = 4       3² = 9       4² = 16      5² = 25
6² = 36      7² = 49      8² = 64      9² = 81      10² = 100
11² = 121    12² = 144    13² = 169    14² = 196    15² = 225
16² = 256    17² = 289    18² = 324    19² = 361    20² = 400
25² = 625    30² = 900    50² = 2,500  100² = 10,000
```

#### What Is a Square Root?

The **square root** of a number is the value that, when multiplied by itself, gives the original number.

```
√25 = 5    because 5 × 5 = 25
√144 = 12  because 12 × 12 = 144
```

The symbol √ is called the **radical sign**. The number under it is the **radicand**.

#### Properties of Square Roots

- √(a × b) = √a × √b (product rule for radicals)
- √(a / b) = √a / √b (quotient rule for radicals)
- (√a)² = a
- √(a²) = |a| (absolute value, since √ always returns non-negative)

#### Simplifying Square Roots

To simplify √n, find the largest perfect square factor of n:

**Example:** Simplify √72
1. Find perfect square factors: 72 = 36 × 2
2. Apply product rule: √72 = √36 × √2 = 6√2

**Example:** Simplify √200
1. Find perfect square factors: 200 = 100 × 2
2. Apply product rule: √200 = √100 × √2 = 10√2

**Example:** Simplify √48
1. Find perfect square factors: 48 = 16 × 3
2. Apply product rule: √48 = √16 × √3 = 4√3

> ⚠️ **Misconception:** "√50 = 25 because 50 ÷ 2 = 25."
>
> **Why it fails:** The square root asks "what number times itself equals 50?" not
> "what is half of 50?" Check: 25 × 25 = 625 ≠ 50. The correct answer is √50 = √(25×2)
> = 5√2 ≈ 7.07.
>
> **Correct model:** Square root is the inverse of squaring, not the inverse of doubling.
> To find √50, look for the largest perfect square factor (25), then √50 = √25 × √2 = 5√2.

#### Estimating Square Roots

For non-perfect squares, estimate by finding the two consecutive perfect squares it falls between:

**Example:** Estimate √40
- 6² = 36 and 7² = 49
- 40 is between 36 and 49, closer to 36
- √40 ≈ 6.3 (actual: 6.32...)

**Example:** Estimate √75
- 8² = 64 and 9² = 81
- 75 is between 64 and 81, closer to 81
- √75 ≈ 8.7 (actual: 8.66...)

> 🤔 **Why does this work?** The product rule for radicals (√(ab) = √a × √b) works
> because squaring both sides gives (√a × √b)² = (√a)² × (√b)² = a × b = (√(ab))².
> Since both sides are non-negative and their squares are equal, the values themselves
> must be equal. This is why you can "pull out" perfect square factors from under the
> radical sign.

---

### 4.5 Cubes and Cube Roots

#### What Is Cubing?

**Cubing** a number means multiplying it by itself three times. The result is a **perfect cube**.

```
n³ = n × n × n
4³ = 4 × 4 × 4 = 64
```

#### Perfect Cubes (Memorize These)

```
1³ = 1       2³ = 8       3³ = 27      4³ = 64      5³ = 125
6³ = 216     7³ = 343     8³ = 512     9³ = 729     10³ = 1,000
```

#### What Is a Cube Root?

The **cube root** of a number is the value that, when cubed, gives the original number.

```
∛27 = 3    because 3 × 3 × 3 = 27
∛125 = 5   because 5 × 5 × 5 = 125
∛-8 = -2   because (-2) × (-2) × (-2) = -8
```

**Key difference from square roots:** Cube roots CAN be negative. Since a negative number cubed is negative, ∛(-8) = -2 is perfectly valid.

#### Simplifying Cube Roots

To simplify ∛n, find the largest perfect cube factor:

**Example:** Simplify ∛54
1. Find perfect cube factors: 54 = 27 × 2
2. Apply product rule: ∛54 = ∛27 × ∛2 = 3∛2

**Example:** Simplify ∛250
1. Find perfect cube factors: 250 = 125 × 2
2. Apply product rule: ∛250 = ∛125 × ∛2 = 5∛2

#### Squares vs. Cubes — Quick Comparison

| Property | Squares/Square Roots | Cubes/Cube Roots |
|----------|---------------------|-----------------|
| Operation | n × n | n × n × n |
| Inverse | √n | ∛n |
| Negative inputs | √(-4) is NOT real | ∛(-8) = -2 (valid) |
| Application | Area | Volume |
| CSE frequency | Very common | Moderate |

> 🤔 **Why does this work?** Cube roots of negative numbers exist in the real numbers
> because multiplying three negative factors produces a negative result: (-2)³ = (-2)×(-2)×(-2)
> = (+4)×(-2) = -8. With square roots, two negative factors always produce a positive
> result, so no real number squared gives a negative. This asymmetry between even and
> odd roots is fundamental — all odd-index roots (∛, ⁵√, etc.) accept negative radicands.

### Check Your Understanding

**1.** What is √144? → **12** (12 × 12 = 144)
**2.** Simplify √75 → **5√3** (75 = 25 × 3, so √75 = √25 × √3 = 5√3)
**3.** What is ∛(-27)? → **-3** ((-3) × (-3) × (-3) = -27)
**4.** Between which two integers does √50 fall? → **Between 7 and 8** (7² = 49, 8² = 64)

---

### 4.6 Scientific Notation

#### What Is Scientific Notation?

**Scientific notation** expresses numbers as a product of a coefficient (between 1 and 10) and a power of 10:

```
a × 10^n    where 1 ≤ a < 10
```

**Examples:**
- 3,400 = 3.4 × 10³
- 0.0056 = 5.6 × 10⁻³
- 7,200,000 = 7.2 × 10⁶
- 0.000091 = 9.1 × 10⁻⁵

#### Converting to Scientific Notation

**For large numbers (≥10):** Move the decimal left until you have a number between 1 and 10. The exponent equals the number of places moved.

- 45,000 → 4.5 × 10⁴ (moved 4 places left)
- 123,000,000 → 1.23 × 10⁸ (moved 8 places left)

**For small numbers (< 1):** Move the decimal right until you have a number between 1 and 10. The exponent is negative and equals the number of places moved.

- 0.003 → 3.0 × 10⁻³ (moved 3 places right)
- 0.0000072 → 7.2 × 10⁻⁶ (moved 6 places right)

> ⚠️ **Misconception:** "3,400 in scientific notation is 34 × 10²."
>
> **Why it fails:** While 34 × 10² = 3,400 is arithmetically correct, it violates
> the scientific notation requirement that the coefficient must be between 1 and 10.
> Since 34 is not between 1 and 10, this is not proper scientific notation.
>
> **Correct model:** The coefficient must satisfy 1 ≤ a < 10. For 3,400: move the
> decimal until you get 3.4 (which is between 1 and 10), count 3 places moved,
> so 3,400 = 3.4 × 10³.

#### Operations with Scientific Notation

**Multiplication:** Multiply coefficients, add exponents.
```
(3 × 10⁴) × (2 × 10³) = 6 × 10⁷
```

**Division:** Divide coefficients, subtract exponents.
```
(8 × 10⁶) ÷ (4 × 10²) = 2 × 10⁴
```

**Addition/Subtraction:** Make exponents the same first, then add/subtract coefficients.
```
(5.2 × 10³) + (3.1 × 10³) = 8.3 × 10³
(4.0 × 10⁵) - (2.5 × 10⁴) = (4.0 × 10⁵) - (0.25 × 10⁵) = 3.75 × 10⁵
```

#### Philippine Government Context

Scientific notation is used in government work for:
- National budget: ₱5.268 trillion = ₱5.268 × 10¹² (2024 GAA)
- Population: ~115 million = 1.15 × 10⁸
- Land area: 300,000 km² = 3.0 × 10⁵ km²
- Microorganism counts in water quality testing: 2.5 × 10⁴ per mL

> 🤔 **Why does this work?** Scientific notation leverages the fact that our number
> system is base-10. Every time you move the decimal point one place, you multiply or
> divide by 10. The exponent on the 10 simply records how many places the decimal was
> shifted. This makes it trivial to compare magnitudes — 10⁸ is immediately recognizable
> as 100 times larger than 10⁶ — without counting zeros.

---

### 4.7 Rational Exponents and Radicals

#### What Are Rational Exponents?

A **rational exponent** is a fraction used as an exponent. It connects exponents and roots:

```
a^(1/n) = ⁿ√a    (the nth root of a)
a^(m/n) = ⁿ√(a^m) = (ⁿ√a)^m
```

**Examples:**
- 8^(1/3) = ∛8 = 2
- 27^(2/3) = (∛27)² = 3² = 9
- 16^(3/4) = (⁴√16)³ = 2³ = 8
- 25^(1/2) = √25 = 5

#### Converting Between Forms

| Radical Form | Rational Exponent Form |
|-------------|----------------------|
| √x | x^(1/2) |
| ∛x | x^(1/3) |
| ⁴√x | x^(1/4) |
| (√x)³ | x^(3/2) |
| (∛x)² | x^(2/3) |

#### Why Rational Exponents Are Useful

Rational exponents let you apply ALL seven laws of exponents to radical expressions:

**Example:** Simplify √x × ∛x
- Convert: x^(1/2) × x^(1/3)
- Product rule: x^(1/2 + 1/3) = x^(5/6)
- Result: ⁶√(x⁵)

**Example:** Simplify (√8)²
- Convert: (8^(1/2))² = 8^(2/2) = 8¹ = 8

> 🤔 **Why does this work?** The definition a^(1/n) = ⁿ√a is forced by the power-of-a-power
> rule. If (a^(1/n))^n must equal a^(n/n) = a¹ = a, then a^(1/n) must be the number
> whose nth power is a — which is exactly the definition of the nth root. Rational
> exponents are not a separate concept; they are the inevitable consequence of requiring
> the exponent laws to work for all rational numbers.

> ⚠️ **Misconception:** "To evaluate 27^(2/3), compute 27² first, then take the cube root."
>
> **Why it fails:** 27² = 729, and then ∛729 = 9 — this gives the correct answer, but
> the intermediate value (729) is unnecessarily large and error-prone. More critically,
> students who try this with larger bases (e.g., 64^(5/6)) get astronomically large
> intermediates that cause arithmetic mistakes.
>
> **Correct model:** Always take the root first, then raise to the power: 27^(2/3) =
> (∛27)² = 3² = 9. Root-first keeps numbers small and manageable. The formula
> a^(m/n) = (ⁿ√a)^m is computationally superior to ⁿ√(a^m) in nearly all cases.

### Check Your Understanding

**1.** What is 8^(1/3)? → **2** (the cube root of 8, since 2³ = 8)
**2.** Convert √x to rational exponent form → **x^(1/2)** (square root = exponent of 1/2)
**3.** Evaluate 16^(3/4) → **8** (⁴√16 = 2, then 2³ = 8)
**4.** Which is easier to compute: (∛27)² or ∛(27²)? → **(∛27)²** (root first keeps numbers small: 3² = 9 vs. ∛729 = 9)

---

### Exam Strategies

#### Strategy 1: Memorize Key Powers

The CSE rewards instant recall. Memorize powers of 2 through 2¹⁰, powers of 3 through 3⁶, and all perfect squares up to 20². This eliminates computation time on at least 30% of exponent questions.

#### Strategy 2: Use the Laws to Simplify Before Computing

Never expand large powers directly. If you see 2⁸ × 2⁻³, recognize it as 2⁵ = 32 immediately. The laws of exponents exist to avoid tedious multiplication.

#### Strategy 3: Check Sign Separately

For expressions with negative bases, determine the sign first (odd exponent → negative, even → positive), then compute the absolute value. This prevents sign errors from contaminating your arithmetic.

#### Strategy 4: Estimate Roots Using Perfect Square/Cube Neighbors

If √n is not a perfect square, bracket it between consecutive integers. On multiple-choice questions, this often eliminates 2-3 wrong answers immediately.

#### Strategy 5: Scientific Notation — Count Decimal Moves

For scientific notation conversions, physically count the decimal places moved. Point your pen at the decimal and count jumps. The direction tells you the sign: left = positive exponent, right = negative exponent.

#### Strategy 6: Convert Radicals to Rational Exponents for Complex Simplification

When combining different roots (√ and ∛ in the same expression), convert everything to rational exponents. The exponent laws then handle the simplification mechanically.

---

### Memory Aids

- **"Power means repeated multiplication, NOT base × exponent"** — 5³ = 5×5×5 = 125, not 5×3 = 15
- **"Negative exponent = flip to denominator"** — 2⁻³ = 1/2³ = 1/8 (reciprocal, not negative)
- **"Zero power = 1, always"** — Any non-zero base raised to 0 equals 1 (forced by the quotient rule)
- **"Even power kills the negative, odd power keeps it"** — (-3)⁴ = +81, (-3)³ = -27
- **"Root first, power second"** — For a^(m/n), compute ⁿ√a first, then raise to m (keeps numbers small)
- **"Scientific notation: coefficient between 1 and 10"** — If your coefficient is ≥10 or <1, adjust
- **"Same base? Add exponents (multiply). Same base? Subtract exponents (divide)."** — Product and quotient rules in one breath
- **"LARS: Left = Add (positive exponent), Right = Subtract (negative exponent)"** — For scientific notation decimal movement direction

---

### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** Simplify: 3⁴ × 3² ÷ 3³

- Step 1: Apply product rule to numerator: 3⁴ × 3² = 3^(4+2) = 3⁶
- Step 2: Apply quotient rule: 3⁶ ÷ 3³ = 3^(6-3) = _____
- Step 3: Evaluate: 3³ = _____

**Answer:** 3^(6-3) = 3³ = **27**

**2.** Simplify: (2³)² × 2⁻⁴

- Step 1: Power of a power: (2³)² = 2^(3×2) = _____
- Step 2: Product rule: _____ × 2⁻⁴ = 2^(_____ + _____) = _____
- Step 3: Evaluate: _____ = _____

**Answer:** (2³)² = 2⁶. Then 2⁶ × 2⁻⁴ = 2^(6+(-4)) = 2² = **4**

**3.** Simplify √128

- Step 1: Find the largest perfect square factor of 128: 128 = _____ × _____
- Step 2: Apply product rule: √128 = √_____ × √_____ = _____
- Step 3: Result: _____

**Answer:** 128 = 64 × 2. √128 = √64 × √2 = **8√2**

**4.** Convert 0.00045 to scientific notation

- Step 1: Move decimal right until coefficient is between 1 and 10: _____
- Step 2: Count places moved: _____ places to the _____
- Step 3: Write in scientific notation: _____ × 10^_____

**Answer:** 4.5 (moved 4 places right). Result: **4.5 × 10⁻⁴**

**5.** Evaluate 32^(2/5)

- Step 1: Take the 5th root first: ⁵√32 = _____ (since _____⁵ = 32)
- Step 2: Raise to the 2nd power: _____² = _____

**Answer:** ⁵√32 = 2 (since 2⁵ = 32). Then 2² = **4**

---

### Which Method?

For each problem, identify the type and solve.

**1.** 5⁴ × 5⁻²
- **Type:** Product of Powers (same base → add exponents)
- **Answer:** 5² = 25
- **Why:** 5^(4+(-2)) = 5² = 25.

**2.** √180
- **Type:** Radical simplification (find largest perfect square factor)
- **Answer:** 6√5
- **Why:** 180 = 36 × 5. √180 = √36 × √5 = 6√5.

**3.** Express 67,500,000 in scientific notation
- **Type:** Scientific notation conversion (large number → positive exponent)
- **Answer:** 6.75 × 10⁷
- **Why:** Move decimal 7 places left: 6.75. Exponent = +7.

**4.** (-2)⁵
- **Type:** Negative base with odd exponent (result is negative)
- **Answer:** -32
- **Why:** Odd exponent → negative. |(-2)⁵| = 32. Result: -32.

**5.** 81^(3/4)
- **Type:** Rational exponent (root first, then power)
- **Answer:** 27
- **Why:** ⁴√81 = 3 (since 3⁴ = 81). Then 3³ = 27.

**6.** (4 × 10⁵) × (3 × 10⁻²)
- **Type:** Scientific notation multiplication (multiply coefficients, add exponents)
- **Answer:** 1.2 × 10⁴
- **Why:** 4 × 3 = 12 = 1.2 × 10¹. Exponents: 5 + (-2) = 3. Total: 1.2 × 10^(1+3) = 1.2 × 10⁴.

---

### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Evaluate powers of integers (positive, zero, and negative exponents)
- [ ] Apply all seven laws of exponents to simplify expressions
- [ ] Determine the sign of a result when a negative base is raised to a power
- [ ] Simplify square roots by extracting perfect square factors
- [ ] Simplify cube roots by extracting perfect cube factors
- [ ] Convert numbers to and from scientific notation correctly
- [ ] Perform arithmetic operations with numbers in scientific notation
- [ ] Convert between radical notation and rational exponent form

---

### Mini Practice Set

Test your understanding with these 20 problems. Answers and explanations follow.

**1.** Evaluate: 4³

**2.** Evaluate: 2⁻⁵

**3.** Simplify: x⁷ × x⁴ ÷ x³

**4.** Evaluate: (-3)⁴

**5.** Evaluate: -3⁴

**6.** Simplify: (5²)³

**7.** Simplify: √242

**8.** Simplify: ∛(-216)

**9.** Evaluate: 9^(3/2)

**10.** Convert to scientific notation: 0.000308

**11.** Evaluate: (2/3)⁻²

**12.** Simplify: (4x³)²

**13.** Compute: (6 × 10³) ÷ (2 × 10⁻¹)

**14.** Estimate √90 to one decimal place

**15.** Simplify: 2⁴ × 3² ÷ (2² × 3)

**16.** Evaluate: 125^(2/3)

**17.** Simplify: √(50/2)

**18.** Evaluate: 10⁰ + 10¹ + 10²

**19.** Simplify: (x⁴y⁻²)³

**20.** A government server stores 2¹⁵ files. Express this as a number.

---

#### Answers and Explanations

**1.** 4³ = 4 × 4 × 4 = **64**
- Multiply 4 by itself three times.

**2.** 2⁻⁵ = 1/2⁵ = 1/32 = **0.03125**
- Negative exponent means reciprocal.

**3.** x⁷ × x⁴ ÷ x³ = x^(7+4-3) = **x⁸**
- Product rule (add 7+4=11), then quotient rule (subtract 11-3=8).

**4.** (-3)⁴ = 81 → **81**
- Even exponent with negative base → positive. 3⁴ = 81.

**5.** -3⁴ = -(3⁴) = **-81**
- No parentheses around -3, so only 3 is raised to the 4th power. Then negate.

**6.** (5²)³ = 5^(2×3) = 5⁶ = **15,625**
- Power of a power: multiply exponents.

**7.** √242 = √(121 × 2) = 11√2 → **11√2**
- Largest perfect square factor of 242 is 121 (11²).

**8.** ∛(-216) = **-6**
- Since (-6)³ = -216. Cube roots of negatives are valid.

**9.** 9^(3/2) = (√9)³ = 3³ = **27**
- Root first: √9 = 3. Then power: 3³ = 27.

**10.** 0.000308 = **3.08 × 10⁻⁴**
- Move decimal 4 places right to get 3.08. Exponent is -4.

**11.** (2/3)⁻² = (3/2)² = 9/4 = **9/4 or 2.25**
- Negative exponent flips the fraction, then square.

**12.** (4x³)² = 4² × (x³)² = 16x⁶ → **16x⁶**
- Power of a product: apply exponent to each factor.

**13.** (6 × 10³) ÷ (2 × 10⁻¹) = 3 × 10^(3-(-1)) = 3 × 10⁴ = **30,000**
- Divide coefficients: 6÷2=3. Subtract exponents: 3-(-1)=4.

**14.** √90: 9² = 81, 10² = 100. 90 is closer to 81. √90 ≈ **9.5** (actual: 9.49)
- Between 9 and 10, closer to 9.5.

**15.** 2⁴ × 3² ÷ (2² × 3) = 2^(4-2) × 3^(2-1) = 2² × 3¹ = 4 × 3 = **12**
- Apply quotient rule to each base separately.

**16.** 125^(2/3) = (∛125)² = 5² = **25**
- Cube root of 125 is 5. Then square: 25.

**17.** √(50/2) = √25 = **5**
- Simplify inside first: 50/2 = 25. Then √25 = 5.

**18.** 10⁰ + 10¹ + 10² = 1 + 10 + 100 = **111**
- Evaluate each power of 10 separately, then add.

**19.** (x⁴y⁻²)³ = x^(4×3) × y^(-2×3) = x¹²y⁻⁶ = **x¹²/y⁶**
- Power of a product with power of a power.

**20.** 2¹⁵ = 2¹⁰ × 2⁵ = 1,024 × 32 = **32,768 files**
- Break into known powers: 2¹⁰ = 1,024 and 2⁵ = 32.

---

### Connections

How this topic connects to other areas of the CSE:

- **Order of Operations:** PEMDAS places exponents at the second-highest priority — understanding when to evaluate powers before multiplication is essential for correct expression evaluation
- **Percentages:** Compound interest and percentage growth formulas use exponents directly: Final = Principal × (1 + rate)ⁿ, making exponent evaluation a prerequisite for financial calculations
- **Multiplication:** Exponentiation is defined as repeated multiplication — fluency with multiplication facts directly speeds up power evaluation
- **Estimation and Mental Math:** Knowing perfect squares and cubes enables rapid estimation of roots, which is tested both directly and as a sub-skill in multi-step problems
- **Operations with Signed Numbers:** Sign rules for negative bases raised to powers (even → positive, odd → negative) combine exponent knowledge with integer sign rules

---

### Mastery Checklist

After completing this lesson, you should be able to:
- ✅ Evaluate any integer power of a single-digit base from memory (2¹ through 2¹⁰, 3¹ through 3⁶, etc.)
- ✅ Apply all seven laws of exponents (product, quotient, power of power, power of product, power of quotient, zero, negative)
- ✅ Correctly determine the sign when a negative base is raised to any integer power
- ✅ Distinguish between -x² and (-x)² and evaluate each correctly
- ✅ Identify perfect squares up to 20² and perfect cubes up to 10³
- ✅ Simplify radical expressions by extracting perfect square/cube factors
- ✅ Estimate non-perfect square roots by bracketing between consecutive integers
- ✅ Convert any number to proper scientific notation (coefficient between 1 and 10)
- ✅ Perform multiplication and division with numbers in scientific notation
- ✅ Convert between radical notation and rational exponent form
- ✅ Evaluate expressions with rational exponents using the root-first strategy
- ✅ Solve CSE-style exponent and root problems within 1-2 minutes

---

## Worked Examples

### Example A: Applying Multiple Exponent Laws

**Problem:** Simplify (2³ × 2⁵) ÷ (2²)³

**Solution:**
1. Product rule in numerator: 2³ × 2⁵ = 2^(3+5) = 2⁸
2. Power of a power in denominator: (2²)³ = 2^(2×3) = 2⁶
3. Quotient rule: 2⁸ ÷ 2⁶ = 2^(8-6) = 2²
4. Evaluate: 2² = **4**

### Example B: Simplifying a Radical Expression

**Problem:** Simplify √(72x⁴y³) where x, y > 0

**Solution:**
1. Factor the radicand: 72x⁴y³ = 36 × 2 × x⁴ × y² × y
2. Identify perfect square factors: 36, x⁴, y²
3. Extract: √36 × √(x⁴) × √(y²) × √(2y)
4. Simplify: 6 × x² × y × √(2y)
5. Result: **6x²y√(2y)**

### Example C: Scientific Notation Division

**Problem:** The Philippine national budget is approximately ₱5.268 × 10¹² and the population is 1.15 × 10⁸. What is the per-capita budget?

**Solution:**
1. Set up division: (5.268 × 10¹²) ÷ (1.15 × 10⁸)
2. Divide coefficients: 5.268 ÷ 1.15 ≈ 4.58
3. Subtract exponents: 12 - 8 = 4
4. Result: 4.58 × 10⁴ = **₱45,800 per person**

### Example D: Rational Exponent Evaluation

**Problem:** Evaluate 64^(5/6)

**Solution:**
1. Take the 6th root first: ⁶√64 = 2 (since 2⁶ = 64)
2. Raise to the 5th power: 2⁵ = 32
3. Result: **32**

### Example E: CSE-Style Comparison Problem

**Problem:** Which is larger: 3⁸ or 8³?

**Solution:**
1. Evaluate 8³: 8 × 8 × 8 = 512
2. Evaluate 3⁸: 3⁴ × 3⁴ = 81 × 81 = 6,561
3. Compare: 6,561 > 512
4. Result: **3⁸ is larger**

## Key Takeaways

- Exponents express repeated multiplication; roots reverse that process. Together they form a unified system governed by seven laws.
- The seven laws of exponents (product, quotient, power of power, power of product, power of quotient, zero, negative) are the tools for simplifying any exponential expression without expanding.
- Negative exponents mean reciprocal (not negative result). Zero exponents always equal 1 (not zero). These are the two most common CSE traps.
- Perfect squares (1-400) and perfect cubes (1-1000) should be memorized for instant recall on exam day.
- Simplifying radicals means extracting the largest perfect square (or cube) factor from under the radical sign.
- Scientific notation requires the coefficient to be between 1 and 10 — this is the most common error in notation problems.
- Rational exponents unify exponents and roots: a^(m/n) = (ⁿ√a)^m. Always take the root first to keep numbers manageable.
- On the CSE, exponent problems reward pattern recognition and law application over brute-force computation.

## Summary

Exponents and roots are inverse operations that together form the language of powers — a compact notation for repeated multiplication and its reversal. The seven laws of exponents (product, quotient, power of power, power of product, power of quotient, zero exponent, and negative exponent) provide a complete toolkit for simplifying any exponential expression without tedious expansion. Mastery of these laws, combined with memorized perfect squares and cubes, enables rapid evaluation of the direct computation items that appear on the Philippine Civil Service Examination.

Beyond direct computation, exponents underpin scientific notation (essential for expressing government budgets, population figures, and technical measurements), radical simplification (tested in both standalone items and as sub-steps in algebra), and rational exponents (which unify the exponent and radical systems into a single framework). The most common CSE traps involve negative exponents (which mean reciprocal, not negative), the zero exponent (which always equals 1), and scientific notation format (coefficient must be between 1 and 10).

For exam success, prioritize memorization of key powers, instant application of the seven laws, and the root-first strategy for rational exponents. These three skills eliminate computation time and prevent the arithmetic errors that account for most wrong answers on exponent and root questions.
