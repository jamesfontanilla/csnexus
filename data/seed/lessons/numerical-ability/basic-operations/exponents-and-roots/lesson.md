# Exponents and Roots

## Introduction

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

## 4.1 What Are Exponents?

### Definition

An **exponent** (also called a **power** or **index**) tells you how many times to multiply a number by itself. The number being multiplied is the **base**, and the small raised number is the **exponent**.

```
base^exponent = result
  2^5         = 2 × 2 × 2 × 2 × 2 = 32
```

We read 2⁵ as "two to the fifth power" or "two raised to five."

### Terminology

| Term | Definition | Example |
|------|-----------|---------|
| Base | The number being multiplied repeatedly | In 3⁴, the base is 3 |
| Exponent | How many times the base is used as a factor | In 3⁴, the exponent is 4 |
| Power | The entire expression or its result | 3⁴ = 81 (81 is the fourth power of 3) |

### Special Powers

| Power Name | Meaning | Example |
|-----------|---------|---------|
| Squared (²) | Base × Base | 5² = 5 × 5 = 25 |
| Cubed (³) | Base × Base × Base | 4³ = 4 × 4 × 4 = 64 |
| To the fourth (⁴) | Base used 4 times | 2⁴ = 2 × 2 × 2 × 2 = 16 |
| To the nth | Base used n times | aⁿ = a × a × ... × a (n times) |

### Powers of Common Bases

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

### Real-Life Applications

| Context | Example |
|---------|---------|
| Computer storage | 2¹⁰ = 1,024 bytes = 1 KB |
| Population growth | Population × (1.02)ⁿ for n years at 2% growth |
| Area calculation | Side² = area of a square |
| Volume calculation | Side³ = volume of a cube |
| Compound interest | Principal × (1 + rate)ⁿ |
| Scientific measurement | Speed of light ≈ 3 × 10⁸ m/s |

---

## 4.2 Laws of Exponents

The laws of exponents are the rules that let you simplify expressions without expanding every power. These are **non-negotiable** for the CSE — nearly every exponent problem requires at least one of these rules.

### Rule 1: Product of Powers (Same Base)

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

### Rule 2: Quotient of Powers (Same Base)

When dividing powers with the **same base**, subtract the exponents.

```
a^m ÷ a^n = a^(m-n)    (where a ≠ 0)
```

**Why it works:** 2⁵ ÷ 2² = (2×2×2×2×2) ÷ (2×2) = 2×2×2 = 2³ — you cancel 2 factors, leaving 5-2=3.

**Examples:**
- 7⁶ ÷ 7² = 7^(6-2) = 7⁴ = 2,401
- 10⁸ ÷ 10³ = 10⁵ = 100,000
- x⁹ ÷ x⁴ = x⁵

### Rule 3: Power of a Power

When raising a power to another power, multiply the exponents.

```
(a^m)^n = a^(m×n)
```

**Why it works:** (2³)² = 2³ × 2³ = 2⁶ — you have the exponent 3 repeated 2 times.

**Examples:**
- (3²)⁴ = 3^(2×4) = 3⁸ = 6,561
- (x⁵)³ = x^(5×3) = x¹⁵
- (10²)³ = 10⁶ = 1,000,000

### Rule 4: Power of a Product

When raising a product to a power, apply the exponent to each factor.

```
(a × b)^n = a^n × b^n
```

**Examples:**
- (2 × 3)⁴ = 2⁴ × 3⁴ = 16 × 81 = 1,296
- (5x)³ = 5³ × x³ = 125x³
- (3y²)² = 3² × (y²)² = 9y⁴

**Common Error:** (2x)³ ≠ 2x³. You must cube BOTH the 2 and the x: (2x)³ = 8x³.

### Rule 5: Power of a Quotient

When raising a fraction to a power, apply the exponent to both numerator and denominator.

```
(a/b)^n = a^n / b^n    (where b ≠ 0)
```

**Examples:**
- (2/3)⁴ = 2⁴/3⁴ = 16/81
- (x/5)² = x²/25
- (3/4)³ = 27/64

### Rule 6: Zero Exponent

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

### Rule 7: Negative Exponent

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

### Summary of All Seven Laws

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

## 4.3 Positive, Zero, and Negative Exponents

Understanding the full spectrum of exponents — positive, zero, and negative — reveals a beautiful pattern.

### The Exponent Pattern

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

### Positive Exponents

Positive exponents mean straightforward repeated multiplication:
- 3⁴ = 3 × 3 × 3 × 3 = 81
- 10³ = 10 × 10 × 10 = 1,000
- 7² = 7 × 7 = 49

### Zero Exponent

The zero exponent always yields 1 (for any non-zero base):
- 15⁰ = 1
- (-3)⁰ = 1
- (2/5)⁰ = 1

### Negative Exponents

Negative exponents yield fractions (reciprocals):
- 4⁻¹ = 1/4
- 3⁻² = 1/9
- 10⁻³ = 1/1,000 = 0.001
- 2⁻⁵ = 1/32

### Moving Factors Between Numerator and Denominator

A negative exponent in the numerator becomes positive in the denominator, and vice versa:

```
x⁻³/y⁻² = y²/x³
```

**Example:** Simplify 5⁻²/3⁻¹
```
5⁻²/3⁻¹ = 3¹/5² = 3/25
```

### Sign of the Result vs. Sign of the Exponent

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

---

## 4.4 Squares and Square Roots

### What Is Squaring?

**Squaring** a number means multiplying it by itself. The result is called a **perfect square**.

```
n² = n × n
5² = 5 × 5 = 25
```

### Perfect Squares (Memorize These)

```
1² = 1       2² = 4       3² = 9       4² = 16      5² = 25
6² = 36      7² = 49      8² = 64      9² = 81      10² = 100
11² = 121    12² = 144    13² = 169    14² = 196    15² = 225
16² = 256    17² = 289    18² = 324    19² = 361    20² = 400
25² = 625    30² = 900    50² = 2,500  100² = 10,000
```

### What Is a Square Root?

The **square root** of a number is the value that, when multiplied by itself, gives the original number. It is the inverse of squaring.

```
√n = x  means  x² = n
√25 = 5  because  5² = 25
√144 = 12  because  12² = 144
```

The symbol √ is called the **radical sign**. The number under it is the **radicand**.

### Properties of Square Roots

- √(a × b) = √a × √b (product rule for radicals)
- √(a/b) = √a / √b (quotient rule for radicals)
- (√a)² = a
- √(a²) = |a| (absolute value, because both 5 and -5 squared give 25)

### Simplifying Square Roots

Not every number is a perfect square. To simplify √n, find the largest perfect square factor.

**Method:** Factor the radicand and extract perfect square factors.

**Example:** √50
```
√50 = √(25 × 2) = √25 × √2 = 5√2
```

**Example:** √72
```
√72 = √(36 × 2) = √36 × √2 = 6√2
```

**Example:** √200
```
√200 = √(100 × 2) = √100 × √2 = 10√2
```

**Example:** √48
```
√48 = √(16 × 3) = √16 × √3 = 4√3
```

**Step-by-step method:**
1. Find the largest perfect square that divides the radicand
2. Write the radicand as (perfect square) × (remaining factor)
3. Take the square root of the perfect square outside the radical
4. Leave the remaining factor under the radical

### Estimating Square Roots

For non-perfect squares, estimate by finding the two consecutive perfect squares it falls between.

**Example:** Estimate √40
- 6² = 36 and 7² = 49
- 40 is between 36 and 49, closer to 36
- √40 ≈ 6.3

**Example:** Estimate √75
- 8² = 64 and 9² = 81
- 75 is between 64 and 81, closer to 81
- √75 ≈ 8.7

### CSE Application: Area Problems

If a square has area 196 m², what is its side length?
- Side = √196 = 14 m

---

## 4.5 Cubes and Cube Roots

### What Is Cubing?

**Cubing** a number means multiplying it by itself three times. The result is a **perfect cube**.

```
n³ = n × n × n
4³ = 4 × 4 × 4 = 64
```

### Perfect Cubes (Memorize These)

```
1³ = 1       2³ = 8       3³ = 27      4³ = 64      5³ = 125
6³ = 216     7³ = 343     8³ = 512     9³ = 729     10³ = 1,000
```

### What Is a Cube Root?

The **cube root** of a number is the value that, when cubed, gives the original number.

```
∛n = x  means  x³ = n
∛27 = 3  because  3³ = 27
∛125 = 5  because  5³ = 125
∛1000 = 10  because  10³ = 1000
```

### Key Difference from Square Roots

Cube roots can be negative (because a negative number cubed is negative):
- ∛(-8) = -2 because (-2)³ = -8
- ∛(-27) = -3 because (-3)³ = -27
- ∛(-125) = -5 because (-5)³ = -125

Square roots of negative numbers are not real numbers, but cube roots of negative numbers are perfectly valid.

### Simplifying Cube Roots

Extract perfect cube factors from under the radical.

**Example:** ∛54
```
∛54 = ∛(27 × 2) = ∛27 × ∛2 = 3∛2
```

**Example:** ∛128
```
∛128 = ∛(64 × 2) = ∛64 × ∛2 = 4∛2
```

**Example:** ∛250
```
∛250 = ∛(125 × 2) = ∛125 × ∛2 = 5∛2
```

### CSE Application: Volume Problems

If a cube has volume 343 cm³, what is its side length?
- Side = ∛343 = 7 cm

A water tank in the shape of a cube holds 8,000 liters. What is the length of each edge in decimeters?
- Edge = ∛8000 = 20 dm

---

## 4.6 Radical Expressions

### Radical Notation

A radical expression uses the radical sign (√) to indicate a root:

```
ⁿ√a = a^(1/n)
```

- √a = square root (index 2, usually not written)
- ∛a = cube root (index 3)
- ⁴√a = fourth root (index 4)

### Simplifying Radicals

The goal is to remove all perfect-power factors from under the radical.

**For square roots:** Extract perfect square factors.
```
√75 = √(25 × 3) = 5√3
√180 = √(36 × 5) = 6√5
√98 = √(49 × 2) = 7√2
```

**For cube roots:** Extract perfect cube factors.
```
∛40 = ∛(8 × 5) = 2∛5
∛108 = ∛(27 × 4) = 3∛4
∛192 = ∛(64 × 3) = 4∛3
```

### Adding and Subtracting Radicals

You can only add or subtract radicals with the **same radicand** (like terms).

```
3√5 + 7√5 = 10√5
8√2 - 3√2 = 5√2
```

**You cannot combine:** 3√2 + 4√3 (different radicands — leave as is)

Sometimes you must simplify first to find like radicals:

**Example:** √12 + √27
```
√12 = √(4×3) = 2√3
√27 = √(9×3) = 3√3
2√3 + 3√3 = 5√3
```

**Example:** √50 - √18
```
√50 = √(25×2) = 5√2
√18 = √(9×2) = 3√2
5√2 - 3√2 = 2√2
```

### Multiplying Radicals

Multiply the numbers under the radicals together (same index required):

```
√a × √b = √(a×b)
```

**Examples:**
- √3 × √12 = √36 = 6
- √5 × √5 = √25 = 5
- 2√3 × 4√6 = 8√18 = 8 × 3√2 = 24√2

### Rationalizing the Denominator

A simplified radical expression should not have a radical in the denominator. To remove it, multiply top and bottom by the radical.

**Example:** 1/√3
```
1/√3 × (√3/√3) = √3/3
```

**Example:** 5/√2
```
5/√2 × (√2/√2) = 5√2/2
```

**Example:** 6/√5
```
6/√5 × (√5/√5) = 6√5/5
```

### Relationship Between Radicals and Exponents

Every radical can be written as a fractional exponent:
```
√a = a^(1/2)
∛a = a^(1/3)
ⁿ√a = a^(1/n)
ⁿ√(a^m) = a^(m/n)
```

This connection is the bridge to rational exponents (Section 4.7).

---

## 4.7 Rational Exponents

### What Are Rational Exponents?

A **rational exponent** is a fraction used as an exponent. It combines the concepts of powers and roots into one notation.

```
a^(m/n) = ⁿ√(a^m) = (ⁿ√a)^m
```

The **denominator** of the fraction is the root index. The **numerator** is the power.

### Converting Between Forms

| Rational Exponent | Radical Form | Value |
|------------------|-------------|-------|
| 8^(1/3) | ∛8 | 2 |
| 25^(1/2) | √25 | 5 |
| 16^(3/4) | (⁴√16)³ | (2)³ = 8 |
| 27^(2/3) | (∛27)² | (3)² = 9 |
| 32^(3/5) | (⁵√32)³ | (2)³ = 8 |

### How to Evaluate Rational Exponents

**Strategy:** Take the root first (denominator), then raise to the power (numerator). This keeps numbers small.

**Example:** 8^(2/3)
```
Step 1: Take cube root of 8 → ∛8 = 2
Step 2: Square the result → 2² = 4
Answer: 8^(2/3) = 4
```

**Example:** 16^(3/4)
```
Step 1: Take fourth root of 16 → ⁴√16 = 2
Step 2: Cube the result → 2³ = 8
Answer: 16^(3/4) = 8
```

**Example:** 27^(4/3)
```
Step 1: Take cube root of 27 → ∛27 = 3
Step 2: Raise to 4th power → 3⁴ = 81
Answer: 27^(4/3) = 81
```

### Negative Rational Exponents

Combine the negative exponent rule with the rational exponent:

```
a^(-m/n) = 1/a^(m/n)
```

**Example:** 4^(-3/2)
```
Step 1: Compute 4^(3/2) = (√4)³ = 2³ = 8
Step 2: Take reciprocal → 1/8
Answer: 4^(-3/2) = 1/8
```

### Laws of Exponents Apply to Rational Exponents

All seven laws work with fractions:

**Example:** x^(1/2) × x^(1/3) = x^(1/2 + 1/3) = x^(5/6)

**Example:** (y^(2/3))⁶ = y^(2/3 × 6) = y⁴

**Example:** a^(3/4) ÷ a^(1/4) = a^(3/4 - 1/4) = a^(2/4) = a^(1/2) = √a

---

## 4.8 Scientific Notation

### What Is Scientific Notation?

**Scientific notation** expresses a number as a product of a coefficient (between 1 and 10) and a power of 10.

```
a × 10^n    where 1 ≤ a < 10 and n is an integer
```

### Why Use Scientific Notation?

- Very large numbers: The Philippine national budget is approximately ₱5,768,000,000,000 = 5.768 × 10¹²
- Very small numbers: A bacterium is about 0.000001 m = 1 × 10⁻⁶ m
- Easier comparison: Which is larger, 3.2 × 10⁸ or 9.1 × 10⁷? The first — higher power of 10 wins.

### Converting Standard Form to Scientific Notation

**Rule:** Move the decimal point until you have a number between 1 and 10. Count the moves.
- Moved LEFT → positive exponent (number was large)
- Moved RIGHT → negative exponent (number was small)

**Example:** 45,000,000
```
4.5 × 10⁷  (decimal moved 7 places left)
```

**Example:** 0.00032
```
3.2 × 10⁻⁴  (decimal moved 4 places right)
```

**Example:** 6,020,000,000,000,000,000,000,000
```
6.02 × 10²³  (Avogadro's number)
```

### Converting Scientific Notation to Standard Form

**Rule:** Move the decimal point by the number of places indicated by the exponent.
- Positive exponent → move RIGHT (make the number larger)
- Negative exponent → move LEFT (make the number smaller)

**Example:** 3.7 × 10⁵ = 370,000

**Example:** 2.1 × 10⁻³ = 0.0021

**Example:** 8.05 × 10⁸ = 805,000,000

### Multiplying in Scientific Notation

Multiply the coefficients and add the exponents:

```
(a × 10^m) × (b × 10^n) = (a × b) × 10^(m+n)
```

**Example:** (3 × 10⁴) × (2 × 10³)
```
= (3 × 2) × 10^(4+3)
= 6 × 10⁷
```

**Example:** (4.5 × 10⁶) × (2 × 10³)
```
= (4.5 × 2) × 10^(6+3)
= 9 × 10⁹
```

**Example:** (5 × 10³) × (8 × 10⁵)
```
= (5 × 8) × 10^(3+5)
= 40 × 10⁸
= 4 × 10⁹  (adjust coefficient to be between 1 and 10)
```

### Dividing in Scientific Notation

Divide the coefficients and subtract the exponents:

```
(a × 10^m) ÷ (b × 10^n) = (a/b) × 10^(m-n)
```

**Example:** (8 × 10⁹) ÷ (2 × 10³)
```
= (8/2) × 10^(9-3)
= 4 × 10⁶
```

**Example:** (6.4 × 10⁷) ÷ (3.2 × 10²)
```
= (6.4/3.2) × 10^(7-2)
= 2 × 10⁵
```

### Powers of 10 Quick Reference

| Power | Value | Name |
|-------|-------|------|
| 10⁻⁶ | 0.000001 | one millionth |
| 10⁻³ | 0.001 | one thousandth |
| 10⁻² | 0.01 | one hundredth |
| 10⁻¹ | 0.1 | one tenth |
| 10⁰ | 1 | one |
| 10¹ | 10 | ten |
| 10² | 100 | hundred |
| 10³ | 1,000 | thousand |
| 10⁶ | 1,000,000 | million |
| 10⁹ | 1,000,000,000 | billion |
| 10¹² | 1,000,000,000,000 | trillion |

---

## 4.9 Operations Involving Exponents and Roots

### Combining Exponent Laws in Multi-Step Problems

CSE problems often require applying multiple laws in sequence.

**Example:** Simplify (2³ × 2⁵) ÷ 2⁴
```
Step 1: Product rule in numerator → 2^(3+5) = 2⁸
Step 2: Quotient rule → 2^(8-4) = 2⁴ = 16
```

**Example:** Simplify (3² × 3⁴)² ÷ 3¹⁰
```
Step 1: Product rule inside parentheses → (3⁶)²
Step 2: Power of a power → 3¹²
Step 3: Quotient rule → 3^(12-10) = 3² = 9
```

**Example:** Simplify 5⁰ + 5¹ + 5⁻¹
```
= 1 + 5 + 1/5
= 6 + 0.2
= 6.2 or 31/5
```

### Mixing Radicals and Exponents

**Example:** Simplify √(4⁶)
```
√(4⁶) = (4⁶)^(1/2) = 4³ = 64
```

**Example:** Simplify ∛(8⁴)
```
∛(8⁴) = (8⁴)^(1/3) = 8^(4/3) = (∛8)⁴ = 2⁴ = 16
```

**Example:** Simplify √(9) × √(16)
```
= 3 × 4 = 12
Or: √(9 × 16) = √144 = 12
```

### Expressions with Multiple Bases

**Example:** Simplify (2³ × 3²) × (2² × 3⁴)
```
Group same bases: 2^(3+2) × 3^(2+4) = 2⁵ × 3⁶ = 32 × 729 = 23,328
```

**Example:** Simplify (6⁴) ÷ (2⁴ × 3⁴)
```
6⁴ = (2×3)⁴ = 2⁴ × 3⁴
So: (2⁴ × 3⁴) ÷ (2⁴ × 3⁴) = 1
```

---

## 4.10 Estimation and Number Sense

### Estimating Powers

When exact computation is impractical, use known values to bracket the answer.

**Example:** Estimate 3⁷
- 3⁶ = 729 and 3⁷ = 3 × 729 = 2,187
- If you only remember 3⁶ = 729, multiply by 3

**Example:** Is 2¹⁰ closer to 500 or 1,000?
- 2¹⁰ = 1,024 → closer to 1,000

### Estimating Roots

**Example:** Estimate √150
- 12² = 144 and 13² = 169
- 150 is between 144 and 169, closer to 144
- √150 ≈ 12.2

**Example:** Estimate ∛100
- 4³ = 64 and 5³ = 125
- 100 is between 64 and 125, closer to 125
- ∛100 ≈ 4.6

### Quick Checks for Exponent Answers

- Any positive base raised to a positive exponent gives a positive result
- 2¹⁰ ≈ 1,000 (useful benchmark)
- 10ⁿ has (n+1) digits when n is a positive integer
- If base > 1, larger exponent → larger result
- If 0 < base < 1, larger exponent → smaller result

### Elimination Strategies

**Example:** What is 4⁵?
- Choices: a) 256  b) 512  c) 1,024  d) 1,280
- 4⁴ = 256, so 4⁵ = 4 × 256 = 1,024 → answer is c)
- Quick check: 4⁵ must end in 4 (since 4¹=4, 4²=16, 4³=64, 4⁴=256, 4⁵=1024). Wait — it ends in 4. Only c) ends in 4.

---

## 4.11 Common Errors in Exponents and Roots

### Error 1: Adding Exponents When Bases Are Different

```
WRONG: 2³ × 3² = 6⁵
CORRECT: 2³ × 3² = 8 × 9 = 72 (cannot combine different bases)
```

The product rule (add exponents) only works when the bases are the SAME.

### Error 2: Thinking Negative Exponent Means Negative Number

```
WRONG: 5⁻² = -25
CORRECT: 5⁻² = 1/5² = 1/25
```

Negative exponent = reciprocal, not negative value.

### Error 3: Thinking x⁰ = 0

```
WRONG: 7⁰ = 0
CORRECT: 7⁰ = 1 (any non-zero base to the zero power equals 1)
```

### Error 4: Incorrect Radical Simplification

```
WRONG: √50 = 25 (divided by 2 instead of finding square root)
CORRECT: √50 = √(25×2) = 5√2 ≈ 7.07
```

### Error 5: Adding Radicals with Different Radicands

```
WRONG: √2 + √3 = √5
CORRECT: √2 + √3 cannot be simplified further (≈ 1.41 + 1.73 = 3.14)
```

You can only add radicals with the same radicand, just like you can only add like terms.

### Error 6: Scientific Notation Coefficient Out of Range

```
WRONG: 45 × 10³ (coefficient must be between 1 and 10)
CORRECT: 4.5 × 10⁴
```

### Error 7: Multiplying Base by Exponent

```
WRONG: 5³ = 15 (multiplied 5 × 3)
CORRECT: 5³ = 5 × 5 × 5 = 125
```

### Error 8: Forgetting to Apply Exponent to Coefficient

```
WRONG: (3x)² = 3x²
CORRECT: (3x)² = 9x² (the 3 is also squared)
```

### Error 9: Wrong Direction in Scientific Notation

```
WRONG: 0.0045 = 4.5 × 10³ (moved decimal right but used positive exponent)
CORRECT: 0.0045 = 4.5 × 10⁻³ (small number → negative exponent)
```

---

## Exam Strategies

### Strategy 1: Memorize Key Powers

Know these cold:
- Powers of 2 up to 2¹⁰
- Powers of 3 up to 3⁶
- Perfect squares up to 20²
- Perfect cubes up to 10³

This eliminates computation time on 60%+ of exponent questions.

### Strategy 2: Use the Last-Digit Pattern

Powers of any base follow a repeating last-digit pattern:
- Powers of 2: 2, 4, 8, 6, 2, 4, 8, 6... (cycle of 4)
- Powers of 3: 3, 9, 7, 1, 3, 9, 7, 1... (cycle of 4)
- Powers of 4: 4, 6, 4, 6... (cycle of 2)
- Powers of 7: 7, 9, 3, 1, 7, 9, 3, 1... (cycle of 4)

If only one choice has the correct last digit, you have the answer without full computation.

### Strategy 3: Estimate Before Computing

For √n, quickly identify the two perfect squares it falls between. This eliminates 2-3 choices immediately.

### Strategy 4: Convert Everything to the Same Base

When comparing or simplifying, express all terms with the same base:
- 4³ = (2²)³ = 2⁶
- 8² = (2³)² = 2⁶
- Therefore 4³ = 8²

### Strategy 5: Check with Small Numbers

If unsure about a rule, test it with base 2 or 3:
- Does (a^m)^n = a^(m+n) or a^(mn)?
- Test: (2²)³ = 4³ = 64. Is that 2⁵=32 or 2⁶=64? It's 2⁶. So the rule is multiply.

---

## Mini Practice Set

Test your understanding with these 20 problems. Answers and explanations follow.

**1.** What is 3⁴?

**2.** Simplify: 2⁵ × 2³

**3.** Simplify: 10⁷ ÷ 10⁴

**4.** What is 5⁰?

**5.** What is 2⁻⁴?

**6.** Simplify: (3²)³

**7.** What is √196?

**8.** Simplify: √72

**9.** What is ∛216?

**10.** Simplify: √12 + √48

**11.** What is 8^(2/3)?

**12.** Express 0.00056 in scientific notation.

**13.** Compute: (4 × 10⁵) × (3 × 10²)

**14.** What is (-2)⁵?

**15.** Simplify: 6/√3

**16.** What is 16^(3/4)?

**17.** Simplify: (5³ × 5²) ÷ 5⁴

**18.** Express 7,200,000 in scientific notation.

**19.** Estimate √90 to the nearest integer.

**20.** What is 9⁻¹ + 9⁰ + 9¹?

---

#### Answers and Explanations

**1.** 3⁴ = **81**
- 3 × 3 × 3 × 3 = 9 × 9 = 81

**2.** 2⁵ × 2³ = 2⁸ = **256**
- Product rule: add exponents 5+3=8; 2⁸ = 256

**3.** 10⁷ ÷ 10⁴ = 10³ = **1,000**
- Quotient rule: subtract exponents 7-4=3

**4.** 5⁰ = **1**
- Any non-zero number to the zero power equals 1

**5.** 2⁻⁴ = 1/2⁴ = **1/16**
- Negative exponent means reciprocal: 1/16

**6.** (3²)³ = 3⁶ = **729**
- Power of a power: multiply exponents 2×3=6; 3⁶ = 729

**7.** √196 = **14**
- 14² = 196

**8.** √72 = **6√2**
- √72 = √(36×2) = 6√2

**9.** ∛216 = **6**
- 6³ = 216

**10.** √12 + √48 = 2√3 + 4√3 = **6√3**
- √12 = 2√3; √48 = 4√3; combine like radicals

**11.** 8^(2/3) = **4**
- ∛8 = 2; 2² = 4

**12.** 0.00056 = **5.6 × 10⁻⁴**
- Move decimal 4 places right; small number → negative exponent

**13.** (4 × 10⁵) × (3 × 10²) = **1.2 × 10⁸**
- 4×3=12; 10^(5+2)=10⁷; 12×10⁷ = 1.2×10⁸

**14.** (-2)⁵ = **-32**
- Odd exponent with negative base → negative result; 2⁵=32

**15.** 6/√3 = **2√3**
- Rationalize: 6/√3 × √3/√3 = 6√3/3 = 2√3

**16.** 16^(3/4) = **8**
- ⁴√16 = 2; 2³ = 8

**17.** (5³ × 5²) ÷ 5⁴ = 5⁵ ÷ 5⁴ = 5¹ = **5**
- Product rule: 3+2=5; Quotient rule: 5-4=1

**18.** 7,200,000 = **7.2 × 10⁶**
- Move decimal 6 places left

**19.** √90 ≈ **9** (actually ≈ 9.49, nearest integer is 9)
- 9² = 81, 10² = 100; 90 is between, closer to 81

**20.** 9⁻¹ + 9⁰ + 9¹ = 1/9 + 1 + 9 = **10 1/9** (or 91/9)
- 1/9 + 1 + 9 = 91/9

---

## Quick Recap

| Topic | Key Rule |
|-------|----------|
| Exponent definition | a^n = a multiplied by itself n times |
| Product of powers | a^m × a^n = a^(m+n) — same base, add exponents |
| Quotient of powers | a^m ÷ a^n = a^(m-n) — same base, subtract exponents |
| Power of a power | (a^m)^n = a^(mn) — multiply exponents |
| Zero exponent | a⁰ = 1 for any a ≠ 0 |
| Negative exponent | a^(-n) = 1/a^n — take the reciprocal |
| Square root | √n is the number that squared gives n |
| Cube root | ∛n is the number that cubed gives n |
| Simplifying radicals | Extract largest perfect square/cube factor |
| Rational exponents | a^(m/n) = (ⁿ√a)^m — denominator is root, numerator is power |
| Scientific notation | a × 10^n where 1 ≤ a < 10 |

## Memory Aids

- **"Same base, add the pace"** — when multiplying same bases, add exponents
- **"Power to a power, multiply the tower"** — nested exponents get multiplied
- **"Zero hero"** — anything to the zero is 1 (the hero number)
- **"Negative means flip"** — negative exponent flips to the denominator
- **"Denominator is the root, numerator is the boot (power)"** — for rational exponents
- **"Left is positive, right is negative"** — moving decimal left in scientific notation gives positive exponent
- **"Factor and extract"** — for simplifying radicals, find the biggest perfect square/cube factor
- **"Last digit cycles"** — powers of any base repeat their last digit in a cycle of 4 or less

## Mastery Checklist

After completing this lesson and practice set, confirm you can:

✅ Evaluate any base raised to a positive integer exponent
✅ Apply all seven laws of exponents correctly
✅ Simplify expressions with zero and negative exponents
✅ Identify perfect squares up to 20² and perfect cubes up to 10³
✅ Compute exact square roots and cube roots of perfect powers
✅ Simplify radical expressions by extracting perfect factors
✅ Add, subtract, and multiply radical expressions
✅ Rationalize denominators with single-term radicals
✅ Convert between radical notation and rational exponents
✅ Evaluate expressions with rational exponents
✅ Express numbers in scientific notation correctly
✅ Multiply and divide numbers in scientific notation
✅ Estimate roots using perfect square/cube benchmarks
✅ Avoid all common exponent and root errors
✅ Solve CSE-style problems efficiently using elimination and estimation
