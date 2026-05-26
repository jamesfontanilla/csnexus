# Percentage Increase and Decrease

## Explanations

### Introduction

**Percentage increase and decrease** problems are among the most frequently tested topics in the Numerical Ability section of the Philippine Civil Service Examination. These problems ask you to determine how much a quantity has grown or shrunk *relative to its original value*, expressed as a percentage.

Unlike basic percentage problems (which find a part, rate, or whole), percentage change problems focus on the **relationship between an original value and a new value**. The key question is always: "By what percent did the value go up or down?"

Percentage change appears in virtually every aspect of professional and daily life:
- **Salaries** — computing pay raises, salary cuts, and cost-of-living adjustments
- **Inflation** — measuring how prices rise over time
- **Discounts** — determining how much cheaper a sale item is compared to its original price
- **Population growth** — tracking how communities expand or contract
- **Taxes** — understanding rate changes and their impact on take-home pay
- **Inventory** — measuring stock increases or reductions
- **Transportation fares** — computing fare hikes and their percentage impact
- **Engineering measurements** — tolerance changes, efficiency improvements
- **Business reports** — revenue growth, profit decline, market share shifts
- **Government budgets** — year-over-year spending changes, allocation adjustments

The CSE tests percentage increase and decrease because government employees must:
1. Interpret budget reports showing year-over-year changes
2. Compute salary adjustments accurately
3. Analyze statistical trends in public data
4. Verify financial computations in procurement and auditing

**Common mistakes examinees make:**
1. Using the **new value** instead of the **original value** as the base (denominator)
2. Adding successive percentages directly (e.g., thinking +10% then −10% = 0%)
3. Confusing the **amount of change** with the **percent of change**
4. Forgetting to subtract when finding the decrease amount
5. Dividing by the wrong number in reverse problems
6. Misidentifying which value is "original" and which is "new"
7. Arithmetic errors when converting between decimals and percentages
8. Not checking whether the answer makes logical sense

### Learning Objectives

After this lesson, you should be able to:
- Determine percent increase accurately using the correct formula
- Determine percent decrease accurately using the correct formula
- Solve successive percentage change problems (multiple increases, multiple decreases, or mixed)
- Distinguish between increase and decrease situations using context clues
- Analyze practical percentage change applications in workplace and daily-life scenarios
- Apply the multiplier method for efficient successive-change computation
- Estimate percentage changes mentally to verify answers and eliminate wrong choices
- Avoid the most common traps in CSE percentage change problems

---

### 4.1 Understanding Percentage Change

**Percentage change** measures how much a quantity has increased or decreased *relative to its original value*, expressed as a percent.

There are two types:
- **Percent increase** — the value went UP from the original
- **Percent decrease** — the value went DOWN from the original

#### The Difference Between Actual Change and Percentage Change

Consider two scenarios:
- A salary goes from ₱20,000 to ₱22,000 → actual change = ₱2,000
- A salary goes from ₱50,000 to ₱52,000 → actual change = ₱2,000

Both have the same actual change (₱2,000), but the *percentage change* is different:
- First: 2,000 ÷ 20,000 = 0.10 = **10% increase**
- Second: 2,000 ÷ 50,000 = 0.04 = **4% increase**

The same ₱2,000 raise represents a much larger proportional change for the lower salary. This is why percentage change matters — it tells you the *relative* significance of a change.

#### Dual Coding Visual: Percentage Change Baseline

<svg width="380" height="220" viewBox="0 0 380 220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#60a5fa"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#34d399"/>
    </linearGradient>
    <pattern id="hatchPattern" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#f87171" stroke-width="2" />
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="url(#bgGrad)" rx="8" />

  <!-- Title -->
  <text x="190" y="24" text-anchor="middle" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="13" font-weight="bold">Visualizing Percentage Change (Base = Original)</text>

  <!-- Percent Increase -->
  <text x="20" y="52" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" font-weight="600">PERCENT INCREASE (e.g., +25%)</text>
  
  <!-- Original Value Bar (100%) -->
  <rect x="20" y="60" width="200" height="20" fill="url(#blueGrad)" rx="3" />
  <text x="120" y="73" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">Original Value: 100%</text>

  <!-- Increase Amount Bar (+25%) -->
  <rect x="222" y="60" width="50" height="20" fill="url(#greenGrad)" rx="3" />
  <text x="247" y="73" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">+25%</text>

  <!-- Total Bracket for New Value -->
  <path d="M 20 86 L 20 90 L 272 90 L 272 86" fill="none" stroke="#94a3b8" stroke-width="1" />
  <text x="146" y="101" text-anchor="middle" fill="#34d399" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">New Value = 125% of Original</text>

  <!-- Percent Decrease -->
  <text x="20" y="137" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10" font-weight="600">PERCENT DECREASE (e.g., -25%)</text>

  <!-- Original Value Bar Outline -->
  <rect x="20" y="145" width="200" height="20" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="3 2" rx="3" />

  <!-- Remaining New Value Bar (75%) -->
  <rect x="20" y="145" width="150" height="20" fill="url(#blueGrad)" rx="3" />
  <text x="95" y="158" text-anchor="middle" fill="#ffffff" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">New Value: 75%</text>

  <!-- Slashed Decrease Amount Bar (-25%) -->
  <rect x="170" y="145" width="30" height="20" fill="url(#hatchPattern)" rx="3" opacity="0.8" />
  <text x="185" y="158" text-anchor="middle" fill="#f87171" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">-25%</text>

  <!-- Total Bracket for Original -->
  <path d="M 20 171 L 20 175 L 200 175 L 200 171" fill="none" stroke="#94a3b8" stroke-width="1" />
  <text x="110" y="186" text-anchor="middle" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="9" font-weight="bold">Original Value = 100% (The Base)</text>
</svg>

> 🤔 **Why does this work?** The original value is the starting baseline or reference point.
> When we divide the change by the original value, we are calculating the change relative to
> that baseline. If we divided by the new value, we would be measuring the change relative to the
> final state, which violates the logic of progression through time. Measuring relative to the start
> ensures that a 10% increase means adding one-tenth of what you initially had.

> ⚠️ **Misconception:** "Percentage change is just the difference between the two numbers."
>
> **Why it fails:** An increase from ₱10 to ₱20 is a difference of ₱10, which is a 100% increase.
> An increase from ₱1,000 to ₱1,010 is also a difference of ₱10, but it is only a 1% increase.
> The wrong model treats both changes as identical, ignoring the scale of the starting amount.
>
> **Correct model:** Percentage change is relative, not absolute. You must always divide the amount
> of change by the original value to find what fraction of the starting amount was added or subtracted.

#### The Three Values You Must Identify

Every percentage change problem involves three values:

| Value | Description | Example |
|-------|-------------|---------|
| **Original Value** | The starting amount (BEFORE the change) | ₱20,000 |
| **New Value** | The ending amount (AFTER the change) | ₱22,000 |
| **Amount of Change** | The difference between new and original | ₱2,000 |

**Critical Rule:** The **original value** is ALWAYS the denominator (base) when computing percentage change. Never use the new value as the base.

#### The Core Formulas

**Percent Increase:**
```
Percent Increase = (New Value − Original Value) / Original Value × 100
```

**Percent Decrease:**
```
Percent Decrease = (Original Value − New Value) / Original Value × 100
```

**General Percentage Change Formula:**
```
Percent Change = (Amount of Change / Original Value) × 100
```

If the result is positive → increase. If negative → decrease.

#### How to Identify Original vs. New Value

**Clue words for the ORIGINAL value:**
- "was," "used to be," "previously," "before," "last year," "originally"
- The earlier time reference in the problem

**Clue words for the NEW value:**
- "is now," "became," "currently," "this year," "after," "new"
- The later time reference in the problem

**Example:** "A worker's salary *was* ₱25,000. It *is now* ₱28,000."
- Original = ₱25,000 (was)
- New = ₱28,000 (is now)

---

### 4.2 Finding Percent Increase

#### The Formula

```
Percent Increase = (New Value − Original Value) / Original Value × 100
```

Or equivalently:
```
Percent Increase = (Increase Amount / Original Value) × 100
```

#### Step-by-Step Process

Step 1: Identify the original value and the new value.
Step 2: Subtract: New Value − Original Value = Increase Amount.
Step 3: Divide: Increase Amount ÷ Original Value.
Step 4: Multiply by 100 to convert to percent.

#### Easy Examples

**Example 1: Salary Increase**

A government clerk's monthly salary increased from ₱18,000 to ₱20,700. What is the percent increase?

```
Step 1: Original = ₱18,000, New = ₱20,700
Step 2: Increase = 20,700 − 18,000 = ₱2,700
Step 3: 2,700 ÷ 18,000 = 0.15
Step 4: 0.15 × 100 = 15%
```

**Answer: 15% increase**

**Example 2: Population Growth**

A barangay's population grew from 5,000 to 5,400. What is the percent increase?

```
Step 1: Original = 5,000, New = 5,400
Step 2: Increase = 5,400 − 5,000 = 400
Step 3: 400 ÷ 5,000 = 0.08
Step 4: 0.08 × 100 = 8%
```

**Answer: 8% increase**

#### Medium Examples

**Example 3: Sales Growth**

A store's monthly revenue went from ₱450,000 to ₱531,000. Find the percent increase.

```
Step 1: Original = ₱450,000, New = ₱531,000
Step 2: Increase = 531,000 − 450,000 = ₱81,000
Step 3: 81,000 ÷ 450,000 = 0.18
Step 4: 0.18 × 100 = 18%
```

**Answer: 18% increase**

**Example 4: Transportation Fare Increase**

A jeepney fare rose from ₱9.00 to ₱12.00. What is the percent increase?

```
Step 1: Original = ₱9.00, New = ₱12.00
Step 2: Increase = 12.00 − 9.00 = ₱3.00
Step 3: 3.00 ÷ 9.00 = 0.3333...
Step 4: 0.3333 × 100 = 33.33%
```

**Answer: 33.33% increase (or 33⅓%)**

#### Hard Examples

**Example 5: Production Increase**

A factory produced 12,480 units last quarter and 15,600 units this quarter. What is the percent increase in production?

```
Step 1: Original = 12,480, New = 15,600
Step 2: Increase = 15,600 − 12,480 = 3,120
Step 3: 3,120 ÷ 12,480 = 0.25
Step 4: 0.25 × 100 = 25%
```

**Answer: 25% increase**

**Example 6: CSE-Style Problem**

The number of applicants for a government position increased from 840 to 1,092. By what percentage did the number of applicants increase?

```
Step 1: Original = 840, New = 1,092
Step 2: Increase = 1,092 − 840 = 252
Step 3: 252 ÷ 840 = 0.30
Step 4: 0.30 × 100 = 30%
```

**Answer: 30% increase**

**CSE Tip:** When the increase amount divides evenly into the original, the answer is a clean percentage. If you get a messy decimal, double-check your subtraction.

---

### 4.3 Finding Percent Decrease

#### The Formula

```
Percent Decrease = (Original Value − New Value) / Original Value × 100
```

Or equivalently:
```
Percent Decrease = (Decrease Amount / Original Value) × 100
```

#### Step-by-Step Process

Step 1: Identify the original value and the new value.
Step 2: Subtract: Original Value − New Value = Decrease Amount.
Step 3: Divide: Decrease Amount ÷ Original Value.
Step 4: Multiply by 100 to convert to percent.

#### Easy Examples

**Example 1: Discount**

A shirt originally priced at ₱800 is now on sale for ₱640. What is the percent decrease?

```
Step 1: Original = ₱800, New = ₱640
Step 2: Decrease = 800 − 640 = ₱160
Step 3: 160 ÷ 800 = 0.20
Step 4: 0.20 × 100 = 20%
```

**Answer: 20% decrease (20% discount)**

**Example 2: Budget Cut**

A department's budget was reduced from ₱500,000 to ₱425,000. What is the percent decrease?

```
Step 1: Original = ₱500,000, New = ₱425,000
Step 2: Decrease = 500,000 − 425,000 = ₱75,000
Step 3: 75,000 ÷ 500,000 = 0.15
Step 4: 0.15 × 100 = 15%
```

**Answer: 15% decrease**

#### Medium Examples

**Example 3: Population Decline**

A town's population decreased from 24,000 to 21,600. What is the percent decrease?

```
Step 1: Original = 24,000, New = 21,600
Step 2: Decrease = 24,000 − 21,600 = 2,400
Step 3: 2,400 ÷ 24,000 = 0.10
Step 4: 0.10 × 100 = 10%
```

**Answer: 10% decrease**

**Example 4: Utility Consumption Decrease**

A household's electricity consumption dropped from 350 kWh to 280 kWh. What is the percent decrease?

```
Step 1: Original = 350, New = 280
Step 2: Decrease = 350 − 280 = 70
Step 3: 70 ÷ 350 = 0.20
Step 4: 0.20 × 100 = 20%
```

**Answer: 20% decrease**

#### Hard Examples

**Example 5: Inventory Reduction**

A warehouse had 8,750 items in stock. After a clearance sale, only 6,125 items remain. What is the percent decrease?

```
Step 1: Original = 8,750, New = 6,125
Step 2: Decrease = 8,750 − 6,125 = 2,625
Step 3: 2,625 ÷ 8,750 = 0.30
Step 4: 0.30 × 100 = 30%
```

**Answer: 30% decrease**

**Example 6: CSE-Style Problem**

The error rate in a government office dropped from 12 errors per 100 documents to 9 errors per 100 documents. What is the percent decrease in the error rate?

```
Step 1: Original = 12, New = 9
Step 2: Decrease = 12 − 9 = 3
Step 3: 3 ÷ 12 = 0.25
Step 4: 0.25 × 100 = 25%
```

**Answer: 25% decrease**

**CSE Tip:** A common trap is computing 3 ÷ 9 = 33.33% instead of 3 ÷ 12 = 25%. Always divide by the ORIGINAL value, not the new value.

---

### Check Your Understanding

**1.** If a value drops from ₱250 to ₱200, what is the percent decrease? → **20%** (Decrease is ₱50. 50 ÷ 250 = 0.20 = 20%)
**2.** Circle the starting value in the problem: "Overtime hours went from 16 to 20." → **16** (16 is the original value before the increase)
**3.** If the new value is double the original value, what is the percent increase? → **100%** (Increase is equal to the original value, so 100% growth)

---

### 4.4 Successive Percent Changes

#### Why You Cannot Simply Add Percentages

This is the **most commonly tested trap** in CSE percentage problems.

**The Trap:** If a price increases by 20% and then decreases by 20%, is the final price the same as the original?

**NO.** The final price is LESS than the original.

Why? Because the 20% decrease applies to the *increased* value (a larger base), not the original value.

```
Original price: ₱1,000
After 20% increase: ₱1,000 × 1.20 = ₱1,200
After 20% decrease: ₱1,200 × 0.80 = ₱960

Final price: ₱960 (NOT ₱1,000)
Net change: ₱960 − ₱1,000 = −₱40 → 4% decrease
```

**Key Insight:** Each successive percentage change applies to the NEW base (the result of the previous change), not the original base.

> 🤔 **Why does this work?** Successive percentage changes apply to different bases.
> When a price increases by 20%, it becomes 120% of the original. When it then decreases by 20%,
> that 20% cut is calculated from the *new, higher* price (120%), not the original 100%.
> Since 20% of 120 is 24, subtracting 24 from 120 leaves you with 96%, resulting in a net 4% decrease.
> Compound interest operates on the same mathematical principle of updating the base after each change.

> ⚠️ **Misconception:** "If a value increases by 10% and then decreases by 10%, it returns to its original value because the percentages cancel out."
>
> **Why it fails:** Start with 100. A 10% increase makes it 110. A 10% decrease from 110 is 11 (not 10).
> Subtracting 11 from 110 gives 99. The final value is 99, which is 1% less than the original 100.
>
> **Correct model:** A percentage change changes the baseline. The second change operates on a new,
> modified baseline. Therefore, equal rates of increase and decrease never cancel out; they always
> result in a net decrease because the decrease is always applied to a larger baseline.

#### The Multiplier Method

The most efficient way to handle successive changes is the **multiplier method**.

**For an increase of r%:**
```
Multiplier = 1 + (r/100)
```

**For a decrease of r%:**
```
Multiplier = 1 − (r/100)
```

**For successive changes, multiply the multipliers together:**
```
Final Value = Original × Multiplier₁ × Multiplier₂ × ... × Multiplierₙ
```

#### Common Multipliers

| Change | Multiplier |
|--------|-----------|
| +10% | 1.10 |
| +20% | 1.20 |
| +25% | 1.25 |
| +50% | 1.50 |
| +100% | 2.00 |
| −10% | 0.90 |
| −20% | 0.80 |
| −25% | 0.75 |
| −50% | 0.50 |
| −5% | 0.95 |
| +5% | 1.05 |
| +15% | 1.15 |
| −15% | 0.85 |
| −30% | 0.70 |
| +30% | 1.30 |

#### Easy Examples

**Example 1: Two Successive Increases**

A product's price increases by 10% and then by another 10%. What is the overall percent increase?

```
Multiplier = 1.10 × 1.10 = 1.21
Overall change = 1.21 − 1 = 0.21 = 21% increase
```

**Answer: 21% increase (NOT 20%)**

**Example 2: Increase Then Decrease**

A salary increases by 25% and then decreases by 20%. What is the net percent change?

```
Multiplier = 1.25 × 0.80 = 1.00
Overall change = 1.00 − 1 = 0 = 0% change
```

**Answer: No net change (the salary returns to its original value)**

#### Medium Examples

**Example 3: Decrease Then Increase**

A stock price drops by 40% and then rises by 50%. What is the net percent change?

```
Multiplier = 0.60 × 1.50 = 0.90
Overall change = 0.90 − 1 = −0.10 = 10% decrease
```

**Answer: 10% net decrease**

**Verification with numbers:**
```
Original: ₱1,000
After 40% decrease: ₱1,000 × 0.60 = ₱600
After 50% increase: ₱600 × 1.50 = ₱900
Net change: (₱900 − ₱1,000) / ₱1,000 = −10%
```

**Example 4: Two Successive Decreases**

A company's workforce is reduced by 10% in January and by another 20% in June. What is the overall percent decrease?

```
Multiplier = 0.90 × 0.80 = 0.72
Overall change = 0.72 − 1 = −0.28 = 28% decrease
```

**Answer: 28% overall decrease (NOT 30%)**

#### Hard Examples

**Example 5: Three Successive Changes**

A government budget increases by 20%, then decreases by 10%, then increases by 5%. What is the net percent change?

```
Multiplier = 1.20 × 0.90 × 1.05 = 1.134
Overall change = 1.134 − 1 = 0.134 = 13.4% increase
```

**Answer: 13.4% net increase**

**Example 6: CSE-Style Successive Change**

An employee's salary was ₱30,000. It was increased by 15% in January and then decreased by 10% in July due to reduced hours. What is the salary after both changes, and what is the net percent change?

```
After 15% increase: ₱30,000 × 1.15 = ₱34,500
After 10% decrease: ₱34,500 × 0.90 = ₱31,050

Net multiplier: 1.15 × 0.90 = 1.035
Net change: 3.5% increase
Final salary: ₱31,050
```

**Answer: ₱31,050 (3.5% net increase from original)**

#### The "Equal Increase and Decrease" Pattern

A very common CSE question type: "A value increases by x% then decreases by x%. What is the net change?"

**Formula for equal increase then decrease (or vice versa):**
```
Net percent change = −(x²/100)%
```

This is always a NET DECREASE.

| Increase then Decrease | Net Change |
|----------------------|------------|
| +10% then −10% | −1% |
| +20% then −20% | −4% |
| +25% then −25% | −6.25% |
| +30% then −30% | −9% |
| +50% then −50% | −25% |

**Why it works:**
```
Multiplier = (1 + x/100)(1 − x/100) = 1 − (x/100)²
Net change = −(x/100)² × 100 = −x²/100 percent
```

---

### 4.5 Identifying Increase vs. Decrease

#### Recognizing Wording Clues

CSE problems use specific language to signal whether a situation involves an increase or a decrease. Recognizing these clues instantly saves time.

**Words/Phrases That Signal INCREASE:**
- increased, rose, grew, gained, went up
- markup, profit, appreciation, inflation
- expanded, climbed, surged, jumped
- "more than before," "higher than last year"
- raised, hiked, boosted, elevated

**Words/Phrases That Signal DECREASE:**
- decreased, dropped, fell, declined, went down
- discount, markdown, depreciation, deflation
- reduced, cut, shrank, contracted
- "less than before," "lower than last year"
- slashed, trimmed, diminished, lost

#### Contextual Analysis

Sometimes the wording is indirect. You must infer the direction from context:

| Situation | Type |
|-----------|------|
| "A store marks up its products by 30%" | Increase |
| "The government offers a 15% tax relief" | Decrease (in tax) |
| "Enrollment surged from 500 to 650" | Increase |
| "The defect rate improved from 8% to 5%" | Decrease (improvement = fewer defects) |
| "Inflation pushed prices from ₱100 to ₱112" | Increase |
| "Efficiency gains reduced processing time" | Decrease |

**CSE Tip:** Watch for the word "improved." In most contexts, improvement means a decrease in something negative (errors, time, cost) or an increase in something positive (output, accuracy, revenue). Read carefully.

#### Comparison Exercises

**Question:** "A worker's overtime hours went from 20 to 15 per month."
- Direction: **Decrease** (15 < 20)
- Amount: 20 − 15 = 5
- Percent: 5 ÷ 20 × 100 = 25% decrease

**Question:** "The passing rate improved from 72% to 81%."
- Direction: **Increase** (81% > 72%)
- Amount: 81 − 72 = 9 percentage points
- Percent increase in the rate: 9 ÷ 72 × 100 = 12.5% increase

**Note:** "9 percentage points" and "12.5% increase" are different things. The CSE may ask for either. Read the question carefully.

---

### 4.6 Practical Applications of Percentage Change

#### Shopping Discounts

A jacket originally costs ₱3,500. During a sale, it is marked down to ₱2,800. What is the percent discount?

```
Decrease = 3,500 − 2,800 = 700
Percent discount = 700 ÷ 3,500 × 100 = 20%
```

#### Salary Raises

A government employee earning ₱28,000 receives a raise to ₱30,800. What is the percent raise?

```
Increase = 30,800 − 28,000 = 2,800
Percent raise = 2,800 ÷ 28,000 × 100 = 10%
```

#### Inflation Rates

If a basket of goods cost ₱5,000 last year and costs ₱5,300 this year, what is the inflation rate?

```
Increase = 5,300 − 5,000 = 300
Inflation rate = 300 ÷ 5,000 × 100 = 6%
```

#### Tax Adjustments

A municipality's property tax rate changed from 2.5% to 3.0%. What is the percent increase in the tax rate?

```
Increase = 3.0 − 2.5 = 0.5
Percent increase = 0.5 ÷ 2.5 × 100 = 20%
```

#### Engineering Tolerances

A machine part's acceptable tolerance was 0.05 mm. After recalibration, it is now 0.04 mm. What is the percent decrease in tolerance?

```
Decrease = 0.05 − 0.04 = 0.01
Percent decrease = 0.01 ÷ 0.05 × 100 = 20%
```

#### Transportation Fare Increases

A bus fare increased from ₱15 to ₱18. What is the percent increase?

```
Increase = 18 − 15 = 3
Percent increase = 3 ÷ 15 × 100 = 20%
```

#### Inventory Changes

A warehouse started the month with 4,000 units and ended with 3,400 units. What is the percent decrease?

```
Decrease = 4,000 − 3,400 = 600
Percent decrease = 600 ÷ 4,000 × 100 = 15%
```

#### Government Budget Reports

A department's allocation went from ₱12 million to ₱15 million. What is the percent increase?

```
Increase = 15 − 12 = 3 million
Percent increase = 3 ÷ 12 × 100 = 25%
```

#### Business Profits and Losses

A company's quarterly profit dropped from ₱2.4 million to ₱1.8 million. What is the percent decrease?

```
Decrease = 2.4 − 1.8 = 0.6 million
Percent decrease = 0.6 ÷ 2.4 × 100 = 25%
```

#### Population Statistics

A city's population grew from 1,200,000 to 1,320,000 over five years. What is the percent growth?

```
Increase = 1,320,000 − 1,200,000 = 120,000
Percent growth = 120,000 ÷ 1,200,000 × 100 = 10%
```

---

### Check Your Understanding

**1.** If a price increases by 10% and then decreases by 10%, is the net change an increase, decrease, or no change? → **Net decrease of 1%** (Multiplier = 1.10 × 0.90 = 0.99)
**2.** What word in this sentence signals a decrease: "The office trimmed its processing queue from 12 days to 9 days."? → **Trimmed** (Signals reduction or decrease)
**3.** If an item's original price is ₱80 and it's marked up by 50%, what is the new price? → **₱120** (₱80 × 1.5 = ₱120)

---

### 4.7 Multi-Step Percentage Problems

#### Organizing Computations Logically

Multi-step problems require you to find intermediate values before reaching the final answer. The key is to work systematically.

#### Finding the Original Value (Reverse Problems)

**Type 1: Given the new value after an increase, find the original.**

Formula:
```
Original = New Value / (1 + rate/100)
```

**Example:** After a 20% increase, a salary is now ₱36,000. What was the original salary?

```
Original = 36,000 ÷ 1.20 = ₱30,000
```

**Verification:** ₱30,000 × 1.20 = ₱36,000 ✓

**Type 2: Given the new value after a decrease, find the original.**

Formula:
```
Original = New Value / (1 − rate/100)
```

**Example:** After a 25% discount, a laptop costs ₱22,500. What was the original price?

```
Original = 22,500 ÷ 0.75 = ₱30,000
```

**Verification:** ₱30,000 × 0.75 = ₱22,500 ✓

**Common Mistake:** Students often compute 25% of ₱22,500 (= ₱5,625) and add it back to get ₱28,125. This is WRONG because 25% of the discounted price is not the same as 25% of the original price.

> 🤔 **Why does this work?** To undo a 20% decrease, you cannot simply add 20% of the new value.
> A 20% decrease reduces a number to 80% (0.8) of its original. To restore it to 100% (1.0),
> you must find what factor multiplies 0.8 to get 1.0. That factor is 1 ÷ 0.8 = 1.25, which corresponds
> to a 25% increase. You must divide by the multiplier because multiplication and division are inverse operations.

> ⚠️ **Misconception:** "To find the original price before a 25% discount, just calculate 25% of the discounted price and add it."
>
> **Why it fails:** If a laptop is discounted by 25% to ₱30,000, 25% of ₱30,000 is ₱7,500. Adding it gives ₱37,500.
> But if you take a 25% discount of ₱37,500, you save ₱9,375, making the sale price ₱28,125, not ₱30,000.
>
> **Correct model:** The 25% discount was calculated from the *original* price, not the sale price.
> To find the original price, divide the sale price by the remaining percentage multiplier (1 - 0.25 = 0.75):
> ₱30,000 ÷ 0.75 = ₱40,000.

#### Finding the New Value

**Example:** A product costs ₱4,500. If the price increases by 12%, what is the new price?

```
New price = 4,500 × 1.12 = ₱5,040
```

#### Finding the Rate of Change

**Example:** A company had 250 employees last year and 300 this year. What is the percent change?

```
Change = 300 − 250 = 50
Percent change = 50 ÷ 250 × 100 = 20% increase
```

#### Advanced Multi-Step Problems

**Example 1: Successive Changes with Final Value Given**

After a 10% increase followed by a 20% decrease, a product costs ₱4,400. What was the original price?

```
Combined multiplier = 1.10 × 0.80 = 0.88
Original = 4,400 ÷ 0.88 = ₱5,000
```

**Verification:** ₱5,000 × 1.10 = ₱5,500 → ₱5,500 × 0.80 = ₱4,400 ✓

**Example 2: Finding What Increase Reverses a Decrease**

A stock dropped by 20%. By what percent must it increase to return to its original value?

```
After 20% decrease: multiplier = 0.80
To return to 1.00: need multiplier of 1/0.80 = 1.25
Required increase = 25%
```

**Answer: 25% increase is needed (NOT 20%)**

**Example 3: CSE-Style Complex Problem**

A government office had 500 employees. Due to budget cuts, 15% were laid off. Later, 10% of the remaining employees were promoted to senior positions. How many employees were promoted?

```
Step 1: After layoffs: 500 × 0.85 = 425 employees remain
Step 2: Promoted: 425 × 0.10 = 42.5 → 42 or 43 employees

If the question asks for exact computation: 42.5
If the question asks for whole people: 43 (round up) or 42 (round down)
```

**CSE Tip:** In real exam questions, the numbers are chosen so that intermediate results come out to whole numbers. If you get a decimal for a count of people, recheck your arithmetic.

---

### 4.8 Percentage Change Interpretation

#### Interpreting Statistical Reports

Government employees frequently encounter percentage changes in reports. Understanding what they mean — and what they don't mean — is critical.

**Example:** "The crime rate decreased by 15% this year."
- This means: crimes this year = 85% of crimes last year
- This does NOT mean: 15 fewer crimes occurred (unless last year had exactly 100)

**Example:** "Revenue grew by 200%."
- This means: new revenue = 3× the original (original + 200% of original)
- This does NOT mean: revenue doubled (that would be 100% growth)

#### Percentage Change vs. Percentage Point Change

These are different concepts that the CSE may test:

**Percentage point change:** The arithmetic difference between two percentages.
**Percent change:** The relative change in a percentage value.

**Example:** An approval rating went from 40% to 50%.
- Percentage point change: 50% − 40% = **10 percentage points**
- Percent change: (50 − 40) ÷ 40 × 100 = **25% increase**

Both are correct — they answer different questions.

#### Misleading Percentage Interpretations

**Trap 1: Small base, large percentage**
- "Sales increased by 500%!" sounds impressive
- But if sales went from 2 units to 12 units, the absolute change is only 10 units

**Trap 2: Comparing percentages with different bases**
- Department A grew by 50% (from 20 to 30 employees)
- Department B grew by 10% (from 200 to 220 employees)
- Department B added more people (20 vs. 10) despite a smaller percentage

**Trap 3: Percentage of a percentage**
- "Interest rates rose from 5% to 6%" — this is a 1 percentage point increase but a 20% increase in the rate itself

#### Workplace Examples

| Report Statement | Correct Interpretation |
|-----------------|----------------------|
| "Absenteeism dropped 30%" | If 100 absences before → now 70 absences |
| "Productivity rose 15%" | Output per worker is 1.15× what it was |
| "Budget increased 8%" | New budget = 1.08 × old budget |
| "Error rate fell from 5% to 4%" | 1 percentage point drop; 20% relative decrease |
| "Population grew 2.5% annually" | Each year's population = 1.025 × previous year |

---

### 4.9 Problem-Solving Strategies

#### Strategy 1: Identify the Original Value First

Before doing any math, ask: "What is the ORIGINAL value?" This is always your denominator.

**Quick identification:**
- The value that came FIRST in time
- The value BEFORE the change happened
- The value associated with "was," "used to be," "originally," "last year"

#### Strategy 2: Choose the Right Formula

| What You Know | What You Need | Formula |
|--------------|---------------|---------|
| Original and New | Percent change | (New − Original) ÷ Original × 100 |
| Original and Rate | New value | Original × (1 ± rate/100) |
| New and Rate (increase) | Original | New ÷ (1 + rate/100) |
| New and Rate (decrease) | Original | New ÷ (1 − rate/100) |
| Multiple changes | Net change | Multiply all multipliers, subtract 1 |

#### Strategy 3: Estimate Before Solving

Before computing, estimate the answer to eliminate obviously wrong choices.

**Example:** A price went from ₱400 to ₱500. Estimate the percent increase.
- The increase is ₱100 out of ₱400
- ₱100 is ¼ of ₱400
- Estimate: about 25%

If the choices are A) 10%, B) 20%, C) 25%, D) 50%, you can immediately eliminate A and D.

#### Strategy 4: Use Benchmark Percentages

Memorize these relationships for instant recognition:

| Fraction of Original | Percent Change |
|---------------------|---------------|
| Double (×2) | +100% |
| Triple (×3) | +200% |
| Half (×0.5) | −50% |
| Quarter (×0.25) | −75% |
| ×1.5 | +50% |
| ×0.75 | −25% |
| ×1.25 | +25% |
| ×0.80 | −20% |
| ×1.10 | +10% |
| ×0.90 | −10% |

#### Strategy 5: Verify Your Answer

After solving, check:
- If the value increased, your percent should be positive
- If the value decreased, your percent should be positive (stated as a decrease)
- The percent increase from A to B is NOT the same as the percent decrease from B to A
- If percent change > 100%, the new value should be more than double (for increase)

---

### 4.10 Estimation and Mental Math Techniques

#### Benchmark Percentage Estimation

When exact computation is difficult, use benchmarks to estimate:

**10% shortcut:** Move the decimal one place left.
- 10% of ₱4,500 = ₱450
- 10% of 1,230 = 123

**From 10%, derive others:**
- 5% = half of 10%
- 20% = double 10%
- 25% = 10% + 10% + 5%
- 1% = move decimal two places left

**Example:** Estimate the percent increase from 480 to 600.
- Change = 120
- 10% of 480 = 48
- 120 ÷ 48 ≈ 2.5 → about 25%
- Exact: 120 ÷ 480 = 0.25 = 25% ✓

#### Quick Multiplier Techniques

For successive changes, use approximate multipliers:

**Example:** +10% then +10%
- Quick estimate: 1.1 × 1.1 = 1.21 → about 21% total increase
- This is faster than computing each step separately

**Example:** −20% then +25%
- Quick: 0.8 × 1.25 = 1.0 → no net change
- Memorize: 20% decrease followed by 25% increase = break even

#### Mental Approximation Strategies

**For percent increase:**
- If the increase is about 1/10 of the original → ~10%
- If the increase is about 1/5 of the original → ~20%
- If the increase is about 1/4 of the original → ~25%
- If the increase is about 1/3 of the original → ~33%
- If the increase is about 1/2 of the original → ~50%

**Elimination strategy for multiple choice:**
- If original = 200 and new = 250, increase = 50
- 50 is ¼ of 200 → 25%
- Eliminate any choice that isn't 25%

#### Rapid Checking Methods

After solving, do a quick sanity check:
- Percent increase from 100 to 150 = 50% (not 33%)
- Percent decrease from 150 to 100 = 33.3% (not 50%)
- These are DIFFERENT — the base changes

---

### 4.11 Common Errors in Percentage Change Problems

#### Error 1: Using the Wrong Base

**Wrong:** Price went from ₱200 to ₱250. Percent increase = 50 ÷ 250 = 20%
**Right:** Percent increase = 50 ÷ 200 = 25%

The denominator is ALWAYS the original value.

#### Error 2: Adding Percentages Incorrectly

**Wrong:** +10% then +10% = +20%
**Right:** 1.10 × 1.10 = 1.21 → +21%

Successive percentages compound; they don't add.

#### Error 3: Confusing Increase and Decrease

**Wrong:** "The price dropped from ₱500 to ₱400. Percent decrease = 100 ÷ 400 = 25%"
**Right:** Percent decrease = 100 ÷ 500 = 20%

Even for decreases, divide by the ORIGINAL (larger) value.

#### Error 4: Arithmetic Carelessness

**Wrong:** 2,700 ÷ 18,000 = 0.015 → 1.5%
**Right:** 2,700 ÷ 18,000 = 0.15 → 15%

Double-check decimal placement. A quick estimate (2,700 is about 15% of 18,000 because 10% = 1,800 and 15% = 2,700) catches this.

#### Error 5: Incorrect Decimal Conversion

**Wrong:** 0.08 = 8% but student writes 0.8%
**Right:** 0.08 × 100 = 8%

Remember: multiply by 100 to convert decimal to percent.

#### Error 6: Misunderstanding Successive Changes

**Wrong:** "Price increased 20% then decreased 20%, so it's back to normal."
**Right:** Net effect = −(20²/100)% = −4% (a net decrease)

Equal increase and decrease NEVER cancel out. The net result is always a decrease.

#### Error 7: Reversing the Problem Incorrectly

**Wrong:** "After a 25% increase, the price is ₱500. Original = 500 − 25%(500) = 500 − 125 = ₱375"
**Right:** Original = 500 ÷ 1.25 = ₱400

You cannot subtract the percentage of the NEW value. You must divide by the multiplier.

---

### Exam Strategies

- **Read the question twice.** Determine whether it asks for percent increase, percent decrease, the new value, or the original value.
- **Identify the original value immediately.** Circle it mentally — it is your denominator.
- **Convert the problem to a multiplier.** This is faster than computing the change amount separately.
- **Estimate first.** Before computing, use benchmarks (10%, 25%, 50%) to narrow down the answer.
- **Watch for successive change traps.** If the problem mentions two or more changes, use the multiplier method — never add percentages.
- **Check the direction.** If the value went up, your answer should say "increase." If it went down, "decrease."
- **Verify with a quick reverse check.** If you found 20% increase, multiply the original by 1.20 and see if you get the new value.
- **Use elimination.** If the change is small relative to the original, eliminate large percentage choices. If the change is large, eliminate small ones.
- **Time management.** Simple percent change problems should take 30-45 seconds. Successive change problems may take 60-90 seconds. Budget accordingly.
- **Don't overthink.** If the numbers divide cleanly, trust the clean answer. CSE problems are designed to have neat solutions.

---

### Memory Aids

#### The "ORIGINAL is the DENOMINATOR" Rule
```
Percent Change = Change ÷ ORIGINAL × 100
                         ^^^^^^^^
                    ALWAYS the starting value
```

Think: "**O**riginal goes **O**n the bottom" (O-O rule)

#### Multiplier Mnemonic: "ADD for UP, SUBTRACT for DOWN"
- Increase of r%: multiplier = 1 + r/100 (add to 1)
- Decrease of r%: multiplier = 1 − r/100 (subtract from 1)

#### The "Never Add Percentages" Reminder
```
10% + 10% ≠ 20%
Instead: 1.10 × 1.10 = 1.21 → 21%
```

Think: "**M**ultiply **M**ultipliers for **M**ultiple changes" (Triple-M rule)

#### Reverse Problem Shortcut
- "After x% increase, value is V. Find original."
- Original = V ÷ (1 + x/100)
- Think: "**D**ivide to go **D**own in time" (D-D rule)

#### Equal Change Pattern
- +x% then −x% → net loss of x²/100 percent
- Quick mental math: +10% then −10% → lose 1%. +20% then −20% → lose 4%.

#### Benchmark Multipliers to Memorize
```
+10% = ×1.1    −10% = ×0.9
+20% = ×1.2    −20% = ×0.8
+25% = ×1.25   −25% = ×0.75
+50% = ×1.5    −50% = ×0.5
+100% = ×2     −100% = ×0 (gone!)
```

---

### Guided Practice

Complete the missing steps. Answers are provided below each problem.

**1.** A government agency's document processing time increased from 40 minutes to 50 minutes. Find the percent increase.

- Step 1: Identify original and new values: Original = _____, New = _____
- Step 2: Calculate actual increase: _____ − _____ = _____ minutes
- Step 3: Divide by original value: _____ ÷ _____ = _____
- Step 4: Convert to percentage: _____ × 100 = _____%

**Answer:** Original = 40, New = 50. Increase = 50 − 40 = 10. Divide: 10 ÷ 40 = 0.25. Percentage: 0.25 × 100 = **25%**

**2.** The cost of a commuter train ticket decreased from ₱60.00 to ₱48.00. Find the percent decrease.

- Step 1: Calculate actual decrease: 60 − 48 = _____
- Step 2: Divide decrease by original value: _____ ÷ 60 = _____
- Step 3: Convert to percentage: _____ × 100 = _____%

**Answer:** Decrease = 12. Divide: 12 ÷ 60 = 0.2. Percentage: 0.2 × 100 = **20%**

**3.** A department's travel budget increases by 20% in January, then decreases by 10% in June. What is the net percent change?

- Step 1: Write the multiplier for a 20% increase: _____
- Step 2: Write the multiplier for a 10% decrease: _____
- Step 3: Multiply the multipliers: _____ × _____ = _____
- Step 4: Calculate net change: _____ − 1 = _____ → _____%

**Answer:** +20% multiplier = 1.20. -10% multiplier = 0.90. Multiply: 1.20 × 0.90 = 1.08. Net change: 1.08 − 1 = 0.08 → **8% increase**

**4.** After receiving a 15% salary raise, a public officer earns ₱34,500. What was their original salary?

- Step 1: Write the multiplier for a 15% increase: _____
- Step 2: Set up the reverse division: ₱34,500 ÷ _____ = ₱_____
- Step 3: Compute original salary: ₱_____

**Answer:** +15% multiplier = 1.15. Division: 34,500 ÷ 1.15. Original salary: **₱30,000**

**5.** A stock falls by 50% on Monday. By what percent must it rise on Tuesday to return to its original price?

- Step 1: Determine value after 50% fall (as decimal): _____
- Step 2: Divide 1 by that value to find the restorative multiplier: 1 ÷ _____ = _____
- Step 3: Convert that multiplier to percentage increase: _____ − 1 = _____ → _____%

**Answer:** Value after drop = 0.50. Restorative multiplier = 1 ÷ 0.50 = 2.0. Percentage increase: 2.0 − 1 = 1.0 → **100% increase**

---

### Which Method?

For each problem, identify the problem type and solve.

**1.** A city's water reserve was 800 million liters. Due to dry weather, it fell by 15%. What is the new volume?
- **Type:** Finding the New Value after a Decrease (Multiplier Method)
- **Answer:** 680 million liters
- **Why:** Decreasing by 15% means the remaining volume is 85% of the original. Multiplier = 0.85. New volume = 800 × 0.85 = 680.

**2.** The passenger capacity of a bus line was increased from 200 to 230 passengers. Find the percent increase.
- **Type:** Finding the Percent Increase
- **Answer:** 15%
- **Why:** Increase = 230 − 200 = 30. Percent increase = 30 ÷ 200 × 100 = 15%.

**3.** A procurement item's cost is increased by 20% then decreased by 20%. What is the net percent change?
- **Type:** Equal Successive Increase and Decrease (compounding trap)
- **Answer:** 4% decrease
- **Why:** Use the equal change formula: −(x²/100)% → −(20²/100)% = −(400/100)% = −4%. Or: 1.20 × 0.80 = 0.96 (4% drop).

**4.** After a 12% budget cut, a department has ₱440,000 remaining. What was the original budget?
- **Type:** Finding the Original Value after a Decrease (Reverse problem)
- **Answer:** ₱500,000
- **Why:** Multiplier for 12% cut = 0.88. Original = 440,000 ÷ 0.88 = ₱500,000.

**5.** A municipality's active tax files grew by 8% last year and by 5% this year. What is the overall percent growth?
- **Type:** Successive Percent Increase (Multiple changes)
- **Answer:** 13.4% overall increase
- **Why:** Multipliers are 1.08 and 1.05. Combined multiplier = 1.08 × 1.05 = 1.134. Net change = 1.134 − 1 = 13.4%.

---

### Before You Practice

Rate your confidence (1-5) on each skill before attempting the problems below. Focus extra practice on areas where you rated 3 or below.

- [ ] Identify original and new values from context clues in a word problem
- [ ] Compute percentage increase accurately using the difference divided by original
- [ ] Compute percentage decrease accurately without dividing by the wrong base
- [ ] Use the multiplier method to compute successive percentage changes compound-wise
- [ ] Solve reverse percentage problems to find the original value before change
- [ ] Apply percentage change formulas in Philippine civil service and budget scenarios

---

### Mini Practice Set

**1.** A worker's salary increased from ₱22,000 to ₱25,300. What is the percent increase?
**Answer:** 15%
**Explanation:** Increase = 25,300 − 22,000 = 3,300. Percent = 3,300 ÷ 22,000 × 100 = 15%.

**2.** A laptop's price dropped from ₱45,000 to ₱36,000. What is the percent decrease?
**Answer:** 20%
**Explanation:** Decrease = 45,000 − 36,000 = 9,000. Percent = 9,000 ÷ 45,000 × 100 = 20%.

**3.** A town's population grew from 80,000 to 92,000. What is the percent increase?
**Answer:** 15%
**Explanation:** Increase = 92,000 − 80,000 = 12,000. Percent = 12,000 ÷ 80,000 × 100 = 15%.

**4.** After a 30% discount, a TV costs ₱14,000. What was the original price?
**Answer:** ₱20,000
**Explanation:** Original = 14,000 ÷ 0.70 = ₱20,000.

**5.** A product's price increases by 20% then decreases by 10%. What is the net percent change?
**Answer:** 8% increase
**Explanation:** Multiplier = 1.20 × 0.90 = 1.08. Net change = 8% increase.

**6.** A stock price fell by 25% then rose by 25%. What is the net percent change?
**Answer:** 6.25% decrease
**Explanation:** Multiplier = 0.75 × 1.25 = 0.9375. Net change = 1 − 0.9375 = 0.0625 = 6.25% decrease.

**7.** An employee's salary was increased by 10% to ₱33,000. What was the original salary?
**Answer:** ₱30,000
**Explanation:** Original = 33,000 ÷ 1.10 = ₱30,000.

**8.** A factory's output increased from 1,500 units to 1,950 units. What is the percent increase?
**Answer:** 30%
**Explanation:** Increase = 1,950 − 1,500 = 450. Percent = 450 ÷ 1,500 × 100 = 30%.

**9.** A budget was cut by 12%. If the new budget is ₱440,000, what was the original budget?
**Answer:** ₱500,000
**Explanation:** Original = 440,000 ÷ 0.88 = ₱500,000.

**10.** A price increases by 50% then decreases by 50%. What is the net percent change?
**Answer:** 25% decrease
**Explanation:** Multiplier = 1.50 × 0.50 = 0.75. Net change = 1 − 0.75 = 0.25 = 25% decrease.

**11.** The number of students in a class went from 40 to 52. What is the percent increase?
**Answer:** 30%
**Explanation:** Increase = 52 − 40 = 12. Percent = 12 ÷ 40 × 100 = 30%.

**12.** A company's expenses decreased from ₱800,000 to ₱680,000. What is the percent decrease?
**Answer:** 15%
**Explanation:** Decrease = 800,000 − 680,000 = 120,000. Percent = 120,000 ÷ 800,000 × 100 = 15%.

**13.** After two successive 10% increases, what is the overall percent increase?
**Answer:** 21%
**Explanation:** Multiplier = 1.10 × 1.10 = 1.21. Overall increase = 21%.

**14.** A jeepney fare went from ₱11 to ₱14. What is the approximate percent increase?
**Answer:** 27.27%
**Explanation:** Increase = 14 − 11 = 3. Percent = 3 ÷ 11 × 100 ≈ 27.27%.

**15.** A government office reduced paper usage from 5,000 sheets to 3,500 sheets per month. What is the percent decrease?
**Answer:** 30%
**Explanation:** Decrease = 5,000 − 3,500 = 1,500. Percent = 1,500 ÷ 5,000 × 100 = 30%.

**16.** A product costs ₱2,000. After a 15% increase followed by a 15% decrease, what is the final price?
**Answer:** ₱1,955
**Explanation:** 2,000 × 1.15 = 2,300. Then 2,300 × 0.85 = 1,955. Net: 2.25% decrease.

**17.** The enrollment at a school dropped from 1,200 to 1,020. What is the percent decrease?
**Answer:** 15%
**Explanation:** Decrease = 1,200 − 1,020 = 180. Percent = 180 ÷ 1,200 × 100 = 15%.

**18.** A stock dropped 40%. By what percent must it rise to return to its original value?
**Answer:** 66.67%
**Explanation:** After 40% drop, value = 0.60 of original. To return: 1 ÷ 0.60 = 1.6667. Need 66.67% increase.

**19.** A city's crime rate went from 120 incidents to 90 incidents per month. What is the percent decrease?
**Answer:** 25%
**Explanation:** Decrease = 120 − 90 = 30. Percent = 30 ÷ 120 × 100 = 25%.

**20.** A salary increases by 20%, then increases by 25%, then decreases by 10%. What is the net percent change?
**Answer:** 35% increase
**Explanation:** Multiplier = 1.20 × 1.25 × 0.90 = 1.35. Net change = 35% increase.

---

### Connections

How this topic connects to other areas of the CSE:

- **Fundamentals of Percentages:** Converting percentages to decimals is the mandatory first step before applying multipliers (e.g., −20% = 0.80)
- **Discounts, Markups, and Sales:** Commercial discounts represent percent decreases, while markups are percent increases — both apply the same baseline mathematics
- **Profit, Loss, and Tax:** Financial losses are percent decreases in revenue, and sales taxes (like VAT) represent percent increases on the shelf price
- **Ratio, Proportion, and Average:** Successive change rates link to compound growth ratios, and average monthly percentage changes are tested in advanced statistical charts

---

### Mastery Checklist

✅ Determine percent increase correctly using (New − Original) ÷ Original × 100
✅ Determine percent decrease accurately using (Original − New) ÷ Original × 100
✅ Solve successive percentage change problems using the multiplier method
✅ Distinguish between increase and decrease situations from context clues
✅ Analyze practical percentage change applications (salaries, discounts, budgets, population)
✅ Find the original value when given the new value and the percent change
✅ Interpret percentage changes in statistical reports correctly
✅ Differentiate between percentage point change and percent change
✅ Apply the equal-increase-and-decrease formula (−x²/100)
✅ Estimate percentage changes mentally using benchmark fractions
✅ Avoid the 7 most common percentage change errors
✅ Solve difficult CSE percentage change problems in under 60 seconds

---

> ?? **Why does this work?** Understanding the principle helps you choose the right method under exam pressure, even when the question format changes.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> ?? **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.

## Worked Examples

### Example 1: Percent Increase (Easy)

**Problem:** A government agency's local branch grew its registered security personnel from 40 officers to 50 officers over a year. What is the percent increase in the personnel count?

**Solution:**
1. **Identify the original and new values:**
   - Original Value = 40 officers (the starting number)
   - New Value = 50 officers (the final number)
2. **Find the actual increase amount:**
   - $\text{Increase Amount} = 50 - 40 = 10 \text{ officers}$
3. **Calculate the percent increase relative to the original:**
   - $\text{Percent Increase} = \frac{\text{Increase Amount}}{\text{Original Value}} \times 100$
   - $\text{Percent Increase} = \frac{10}{40} \times 100 = 0.25 \times 100 = \mathbf{25\%}$

**Verification:** 40 officers $\times$ 1.25 = 50 officers. The round-trip works!

---

### Example 2: Percent Decrease (Medium)

**Problem:** A department's procurement cost for high-volume office supplies dropped from ₱15,000 to ₱12,000 under a new supplier contract. Find the percent decrease.

**Solution:**
1. **Identify the original and new values:**
   - Original Value = ₱15,000
   - New Value = ₱12,000
2. **Find the actual decrease amount:**
   - $\text{Decrease Amount} = 15,000 - 12,000 = ₱3,000$
3. **Calculate the percent decrease relative to the original:**
   - $\text{Percent Decrease} = \frac{\text{Decrease Amount}}{\text{Original Value}} \times 100$
   - $\text{Percent Decrease} = \frac{3,000}{15,000} \times 100 = 0.20 \times 100 = \mathbf{20\%}$

**Verification:** ₱15,000 $\times$ 0.80 = ₱12,000. The decrease is correct!

---

### Example 3: Successive Changes (Medium)

**Problem:** An administrative officer's monthly salary of ₱30,000 increases by 10% in Year 1 due to promotion, and then increases by 20% in Year 2 under a nationwide government salary standardization plan. What is the final salary, and what is the net percent increase?

**Solution:**
1. **Set up the multipliers for both changes:**
   - Year 1 (+10%): Multiplier = 1.10
   - Year 2 (+20%): Multiplier = 1.20
2. **Calculate the combined multiplier:**
   - $\text{Combined Multiplier} = 1.10 \times 1.20 = 1.32$
3. **Compute the final salary:**
   - $\text{Final Salary} = 30,000 \times 1.32 = \mathbf{₱39,600}$
4. **Determine the net percent increase:**
   - $\text{Net Increase} = (1.32 - 1) \times 100 = \mathbf{32\%}$

**Verification by steps:**
- Salary after Year 1: ₱30,000 $\times$ 1.10 = ₱33,000
- Salary after Year 2: ₱33,000 $\times$ 1.20 = ₱39,600
- Overall percentage increase: (39,600 − 30,000) ÷ 30,000 = 9,600 ÷ 30,000 = 0.32 = 32% growth.

---

### Example 4: Finding the Original Value (Hard)

**Problem:** A brand-new municipal vehicle is purchased for ₱880,000, which includes a 10% local government purchase tax on top of the original manufacturer invoice price. What was the vehicle's original manufacturer invoice price?

**Solution:**
1. **Identify the given values:**
   - New Value (tax-inclusive price) = ₱880,000
   - Tax Rate = 10% increase
2. **Determine the multiplier:**
   - $\text{Multiplier} = 1 + 0.10 = 1.10$
3. **Calculate the original value by dividing the new value by the multiplier:**
   - $\text{Original Price} = \frac{\text{New Value}}{\text{Multiplier}}$
   - $\text{Original Price} = \frac{880,000}{1.10} = \mathbf{₱800,000}$

**Verification:** ₱800,000 $\times$ 1.10 = ₱880,000. Adding 10% of ₱800,000 (= ₱80,000) correctly yields ₱880,000.

---

### Example 5: Equal Change Pattern (Hard)

**Problem:** A cooperative's investment fund of ₱100,000 experiences a market contraction of 25% on Monday, followed by a recovery gain of 25% on Tuesday. What is the value of the fund at the end of Tuesday, and what is the total net percentage change?

**Solution:**
1. **Apply the successive multipliers:**
   - Monday (−25%): Multiplier = 0.75
   - Tuesday (+25%): Multiplier = 1.25
2. **Compute the combined multiplier:**
   - $\text{Combined Multiplier} = 0.75 \times 1.25 = 0.9375$
3. **Find the final value of the fund:**
   - $\text{Final Value} = 100,000 \times 0.9375 = \mathbf{₱93,750}$
4. **Find the net percentage change using the equal-change formula:**
   - $\text{Net Percent Change} = -(\frac{x^2}{100})\%$
   - $\text{Net Percent Change} = -(\frac{25^2}{100})\% = -(\frac{625}{100})\% = \mathbf{-6.25\%}$ (a 6.25% decrease)

**Verification:** 100,000 $\times$ (1 - 0.0625) = 100,000 $\times$ 0.9375 = ₱93,750.

---

## Key Takeaways

- **Original is the Base:** When calculating percentage change, the denominator is always the original value (the starting state before the change). Never use the new value as the denominator.
- **Successive Compounding:** Multi-step percentage changes compound sequentially and cannot be added or subtracted directly. A 10% raise followed by a 10% pay cut results in a net 1% loss, not a net 0% change.
- **The Multiplier is Faster:** To compute an increase of $r\%$, multiply by $(1 + r/100)$. To compute a decrease of $r\%$, multiply by $(1 - r/100)$.
- **Reversing Requires Division:** To find the original value when given the new value and the percent change, divide by the multiplier. Never subtract or add that percentage directly to/from the new value.
- **Difference in rating terms:** Percentage point change is the arithmetic difference between two percentage numbers, whereas percentage change is the relative growth of the rating itself.

---

## Summary

Percentage increase and decrease questions measure the relative growth or contraction of a quantity against its initial baseline. This lesson details the exact formulas for percent increase and decrease, both of which require dividing the absolute amount of change by the original baseline value. It details the compounding behavior of successive changes, introducing the multiplier method to compute compounding growth or decay efficiently while warning against the trap of adding percentages directly. It addresses reverse problems—finding the original value before a change—by dividing by the corresponding multiplier. Real-world civil service examples demonstrate how these concepts apply to salary hikes, tax adjustments, budget reductions, and statistical reports. Sanity-checking, mental estimations using friendly benchmark fractions, and systematic checking steps ensure that examinees can solve these problems rapidly and with absolute confidence.
