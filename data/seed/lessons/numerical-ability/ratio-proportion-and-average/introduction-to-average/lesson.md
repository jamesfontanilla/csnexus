# Introduction to Average (Mean)

## Explanations

### Introduction

An **average** (also called the **arithmetic mean**) is the single value that best represents a set of numbers by distributing the total equally among all items. Averages are one of the most practical mathematical tools in everyday life — from computing your semester grade to understanding national salary reports, from calculating fuel efficiency to interpreting government budget data per capita.

In the Philippine Civil Service Examination, average problems appear frequently because they test a candidate's ability to:
- Summarize numerical data quickly
- Work backward from summary statistics to find missing values
- Interpret what averages mean in real-world contexts
- Perform accurate arithmetic under time pressure

This subtopic covers six critical areas:
- **Meaning of Average (Mean)** — what averages represent and why they matter
- **Finding the Arithmetic Mean** — the standard computation procedure
- **Sum and Count Relationship** — the three-way formula connecting mean, total, and count
- **Interpreting Averages** — understanding what averages tell us (and don't tell us)
- **Comparing Averages** — using means to make decisions between groups
- **Practical Applications of Averages** — real-world scenarios tested in the CSE

### Why Averages Are Tested in the CSE

The Civil Service Exam tests averages because:
- Government employees compute average processing times for citizen services
- Budget officers calculate per-capita spending across municipalities
- HR personnel determine average salary grades for classification purposes
- Administrative officers track average daily output for performance evaluation
- Statistical reports submitted to oversight agencies use averages as summary measures
- Teachers compute average scores for grading and ranking
- Procurement officers calculate average unit costs across suppliers
- Average problems integrate addition, division, and algebraic reasoning — testing multiple skills simultaneously

### Common Mistakes Examinees Make

1. **Forgetting to divide** — computing the sum but writing it as the answer
2. **Dividing by the wrong number** — using the sum of values instead of the count of values as the divisor
3. **Miscounting items** — overlooking one value in the list or counting a value twice
4. **Arithmetic errors in addition** — especially with larger numbers or decimals
5. **Confusing average with median** — the average is the sum divided by count; the median is the middle value when sorted
6. **Rounding too early** — rounding intermediate results before the final division
7. **Misreading "missing value" problems** — not recognizing that the question asks for an unknown item, not the average itself
8. **Ignoring units** — mixing pesos with thousands of pesos, or minutes with hours

### Learning Objectives

After this lesson, you should be able to:
- Define average (mean) correctly and explain its purpose
- Compute the arithmetic mean accurately for any set of numbers
- Identify and apply the relationship between total sum, count, and mean
- Solve missing-value problems by working backward from a given average
- Interpret averages in real-life situations (grades, salaries, expenses, production)
- Compare averages between groups to draw logical conclusions
- Solve CSE-style average problems efficiently under time pressure

---

### 4.1 What Is an Average (Mean)?
> 🤔 **Why does this work?** The principle behind this operation follows from the fundamental properties of arithmetic. Understanding the "why" — not just the "how" — lets you recognize when to apply this method in unfamiliar problem contexts on the CSE.


The **arithmetic mean** (commonly called the "average") is the value you get when you distribute a total equally among all items in a group.

**Core Formula:**

$$
\text{Mean} = \frac{\text{Sum of All Values}}{\text{Number of Values}}
$$

Or written more compactly:

$$
\bar{x} = \frac{x_1 + x_2 + x_3 + \cdots + x_n}{n}
$$

#### The "Fair Share" Interpretation

Imagine 4 friends have the following amounts of money: ₱50, ₱30, ₱80, and ₱40. If they pooled all their money and split it equally, each person would get:

$$
\frac{50 + 30 + 80 + 40}{4} = \frac{200}{4} = ₱50
$$

The average (₱50) is the amount each person would have if the total were distributed fairly. Nobody actually has to give or receive money — the average simply tells us what "equal distribution" would look like.

#### The "Balancing Point" Interpretation

Think of the average as the balancing point on a number line. If you placed weights at positions 30, 50, 40, and 80, the balance point would be at 50. Values below the average "pull down" and values above "pull up" — the average is where these forces balance.

#### Why Averages Summarize Data

A single average can represent an entire dataset:
- "The average score on the exam was 78" tells you more about class performance than listing all 40 individual scores
- "The average daily temperature in Manila in March is 31°C" summarizes 31 days of data in one number
- "The average processing time for a business permit is 5 days" gives citizens a clear expectation

**Key insight:** The average may not equal any actual value in the dataset. If test scores are 70, 80, and 90, the average is 80 — which happens to match one score. But if scores are 70, 75, and 90, the average is 78.33 — a value no one actually scored.


> ⚠️ **Misconception:** "The formula always works the same way regardless of the problem context."

> **Why it fails:** CSE problems often present variations where the standard formula must be adapted. Blindly applying a memorized formula without checking the context leads to systematic errors.

> **Correct model:** Always read the problem to identify what type of relationship exists (direct, inverse, part-whole, etc.), then apply the appropriate formula. Verify your answer makes sense in the problem's context before selecting it.

---

### 4.2 Parts of the Average Formula

The average formula has three components. Understanding their relationship is the key to solving all average problems — including the tricky "find the missing value" type.

| Component | Symbol | Meaning |
|-----------|--------|---------|
| Sum (Total) | S | The result of adding all values together |
| Count (Number of items) | n | How many values are in the set |
| Mean (Average) | x̄ | The result of dividing the sum by the count |

#### The Three-Way Relationship

These three components are connected by a single equation that can be rearranged three ways:

$$
\text{Mean} = \frac{\text{Sum}}{n} \quad \Longleftrightarrow \quad \text{Sum} = \text{Mean} \times n \quad \Longleftrightarrow \quad n = \frac{\text{Sum}}{\text{Mean}}
$$

**This is the most important relationship in average problems.** If you know any two of the three values, you can find the third.

| If you know... | You can find... | Formula |
|----------------|----------------|---------|
| Sum and Count | Mean | Mean = Sum ÷ Count |
| Mean and Count | Sum | Sum = Mean × Count |
| Sum and Mean | Count | Count = Sum ÷ Mean |

#### Example: All Three Directions

A student's 5 quiz scores total 425 points.
- **Mean** = 425 ÷ 5 = **85**

A student's average across 4 exams is 88.
- **Total sum** = 88 × 4 = **352**

A student's scores sum to 270 and the average is 90.
- **Number of exams** = 270 ÷ 90 = **3**

#### Why All Values Affect the Mean

Every single value in the dataset contributes to the sum, which determines the mean. Changing even one value changes the average.

**Example:** Scores are 80, 85, 90, 95, 100. Mean = 450 ÷ 5 = 90.
If the 100 drops to 70: Mean = 420 ÷ 5 = 84. One value changed the average by 6 points.


> ⚠️ **Misconception:** "If my computed answer is close to one of the choices, it must be right."

> **Why it fails:** The CSE deliberately includes distractors that result from common errors — using the wrong operation, misidentifying the proportion type, or reversing the ratio. A "close" answer could be the result of a systematic mistake that the test writers anticipated.

> **Correct model:** Verify your setup before computing. Check that you've identified the correct proportion type, set up the equation properly, and solved accurately. A wrong setup with correct arithmetic still produces a wrong answer — and the CSE will include that wrong answer among the choices.

---


### Check Your Understanding

**1.** What is the key concept from this section? → **Review the preceding content to recall the main principle**

**2.** How would you apply this concept to a practical problem? → **Identify the type of relationship, set up the correct equation, and solve step by step**

**3.** What common mistake should you avoid here? → **Check the Common Mistakes section — verify your answer doesn't fall into these traps**

---

### 4.3 Computing the Arithmetic Mean
> 🤔 **Why does this work?** When you follow this procedure, you're exploiting a mathematical invariant — something that stays constant regardless of how you manipulate the numbers. Identifying that invariant is the key to solving problems efficiently rather than memorizing steps.


#### Step-by-Step Procedure

1. **List all values** in the dataset
2. **Add all values** to get the total sum
3. **Count** how many values there are
4. **Divide** the sum by the count
5. **Simplify** or round as needed

#### Easy Examples

**Example 1:** Find the average of 12, 15, 18, and 20.

$$
\text{Sum} = 12 + 15 + 18 + 20 = 65
$$
$$
\text{Count} = 4
$$
$$
\text{Mean} = \frac{65}{4} = 16.25
$$

**Example 2:** Find the average of 8, 10, 12, 14, and 16.

$$
\text{Sum} = 8 + 10 + 12 + 14 + 16 = 60
$$
$$
\text{Mean} = \frac{60}{5} = 12
$$

#### Medium Examples

**Example 3:** A government employee's monthly expenses for 6 months were: ₱15,200, ₱14,800, ₱16,500, ₱15,000, ₱17,300, and ₱14,200. Find the average monthly expense.

$$
\text{Sum} = 15{,}200 + 14{,}800 + 16{,}500 + 15{,}000 + 17{,}300 + 14{,}200 = 93{,}000
$$
$$
\text{Mean} = \frac{93{,}000}{6} = ₱15{,}500
$$

**Example 4:** A delivery truck traveled the following distances (in km) over 5 days: 145, 162, 138, 155, and 170. What is the average daily distance?

$$
\text{Sum} = 145 + 162 + 138 + 155 + 170 = 770
$$
$$
\text{Mean} = \frac{770}{5} = 154 \text{ km}
$$

#### Hard Examples

**Example 5:** The daily production output (in units) of a factory for 8 days was: 342, 358, 365, 371, 349, 380, 355, and 360. Find the average daily output.

$$
\text{Sum} = 342 + 358 + 365 + 371 + 349 + 380 + 355 + 360 = 2{,}880
$$
$$
\text{Mean} = \frac{2{,}880}{8} = 360 \text{ units}
$$

**Example 6:** An employee's performance ratings (out of 100) for 7 quarters were: 87.5, 92.3, 88.7, 91.0, 85.5, 93.2, and 89.8. Find the average rating.

$$
\text{Sum} = 87.5 + 92.3 + 88.7 + 91.0 + 85.5 + 93.2 + 89.8 = 628.0
$$
$$
\text{Mean} = \frac{628.0}{7} = 89.71 \text{ (rounded to two decimal places)}
$$

#### Verification Method

To verify your answer, multiply the mean by the count. You should get back the original sum:
- 16.25 × 4 = 65 ✓
- 12 × 5 = 60 ✓
- 15,500 × 6 = 93,000 ✓

---

### 4.4 Interpreting Averages

Computing an average is only half the skill. The CSE also tests whether you can **interpret** what an average means in context.

#### Averages as Representative Values

The average represents the "typical" value in a dataset — but with important caveats:
- It may not equal any actual data point
- It can be pulled by extreme values (outliers)
- It assumes all items are equally weighted

#### Workplace Examples

**Average Salary:** If the average salary in a department is ₱35,000, it means the total payroll divided by the number of employees equals ₱35,000. Some employees earn more, some earn less — the average is the balancing point.

**Average Processing Time:** If a government office processes permits in an average of 3 days, some permits take 1 day and others take 7 days. The average tells citizens what to generally expect, not a guarantee.

#### Transportation Examples

**Average Speed:** A bus traveling 240 km in 4 hours has an average speed of 60 km/h. The bus didn't travel at exactly 60 km/h the entire time — it sped up, slowed down, and stopped. The average summarizes the overall rate.

#### Business Examples

**Average Daily Sales:** A store's average daily sales of ₱25,000 means total weekly sales of ₱175,000 spread across 7 days. Monday might bring ₱40,000 and Tuesday only ₱15,000 — the average smooths these fluctuations.

#### What Averages Don't Tell You

- **Spread/variation:** Two classes can have the same average (80) but very different score distributions (one class: all scores between 75–85; another: scores from 50–100)
- **Individual values:** Knowing the average doesn't tell you any specific value
- **Distribution shape:** The average doesn't reveal whether most values are above or below it

---

### 4.5 Finding Missing Values Using Averages
> 🤔 **Why does this work?** This shortcut works because it's a special case of the more general rule. By understanding the underlying principle, you can verify your answer logically even if you forget the exact formula under exam pressure.


This is the most common "tricky" average problem type on the CSE. Instead of computing the average, you're given the average and must find a missing value.

#### The Key Insight

$$
\text{Total Sum} = \text{Mean} \times \text{Number of Values}
$$

If you know the desired average and the number of items, you know what the total must be. Subtract the known values from that total to find the missing one.

#### Step-by-Step Procedure

1. Compute the required total: Mean × Count
2. Add up all known values
3. Subtract known sum from required total
4. The difference is the missing value

#### Easy Example

**Problem:** A student scored 85, 90, and 78 on three tests. What score must she get on the 4th test to have an average of 85?

**Solution:**
- Required total = 85 × 4 = 340
- Known sum = 85 + 90 + 78 = 253
- Missing score = 340 − 253 = **87**

**Verification:** (85 + 90 + 78 + 87) ÷ 4 = 340 ÷ 4 = 85 ✓

#### Medium Example

**Problem:** The average monthly electricity bill for a family over 6 months is ₱3,200. If the bills for the first 5 months were ₱2,800, ₱3,500, ₱3,100, ₱3,400, and ₱2,900, what was the bill for the 6th month?

**Solution:**
- Required total = 3,200 × 6 = 19,200
- Known sum = 2,800 + 3,500 + 3,100 + 3,400 + 2,900 = 15,700
- Missing bill = 19,200 − 15,700 = **₱3,500**

#### Hard Example

**Problem:** A team of 8 employees has an average performance score of 88.5. Seven of the scores are: 92, 85, 90, 87, 91, 84, and 89. What is the 8th employee's score?

**Solution:**
- Required total = 88.5 × 8 = 708
- Known sum = 92 + 85 + 90 + 87 + 91 + 84 + 89 = 618
- Missing score = 708 − 618 = **90**

#### Variation: Effect of Adding a New Value

**Problem:** The average age of 5 employees is 32. A new employee joins. If the new average becomes 31, how old is the new employee?

**Solution:**
- Original total = 32 × 5 = 160
- New total = 31 × 6 = 186
- New employee's age = 186 − 160 = **26**

---

### 4.6 Comparing Averages

The CSE often presents scenarios where you must compare averages between groups to draw conclusions or make decisions.

#### Identifying Larger or Smaller Means

**Example:** Team A's sales figures (in thousands): 45, 52, 48, 55, 50. Team B's sales figures: 60, 42, 38, 65, 55.

- Team A average = 250 ÷ 5 = 50 thousand
- Team B average = 260 ÷ 5 = 52 thousand

Team B has a higher average, but notice Team B's values are more spread out (38 to 65) compared to Team A (45 to 55). The averages alone don't capture this difference in consistency.

#### Classroom Comparisons

**Example:** Section A (30 students) has an average score of 82. Section B (25 students) has an average score of 86. Which section performed better on average?

Section B performed better (86 > 82). But if the question asks for the **combined average** of both sections:

$$
\text{Combined average} = \frac{(82 \times 30) + (86 \times 25)}{30 + 25} = \frac{2{,}460 + 2{,}150}{55} = \frac{4{,}610}{55} = 83.82
$$

Note: The combined average is NOT simply (82 + 86) ÷ 2 = 84. You must weight by group size.

#### Workplace Productivity

**Example:** Branch A processes an average of 120 applications per day. Branch B processes an average of 95 applications per day. If Branch A has 8 employees and Branch B has 5 employees:

- Per-employee average for A = 120 ÷ 8 = 15 applications/employee
- Per-employee average for B = 95 ÷ 5 = 19 applications/employee

Branch B is actually more productive per employee despite lower total output.

---

### 4.7 Real-Life Applications of Averages

#### School Grades
A student's final grade is often the average of multiple assessments: quizzes, exams, projects. Understanding averages helps students know what scores they need to achieve a target grade.

#### Employee Salaries
Government salary standardization uses average compensation across positions and regions to ensure equitable pay scales.

#### Transportation Data
Average travel time, average speed, and average fuel consumption help transportation planners optimize routes and schedules.

#### Sports Statistics
Batting averages, points per game, and average completion rates are all arithmetic means used to evaluate athlete performance.

#### Budgeting
Average monthly expenses help families and organizations plan budgets and identify spending patterns.

#### Engineering Measurements
Average load capacity, average material strength, and average tolerance levels guide engineering decisions.

#### Government Reports
Per-capita income, average household size, average class size — government statistics rely heavily on averages to summarize population data.

#### Inventory Management
Average daily consumption rates determine reorder points and safety stock levels.

#### Population Studies
Average life expectancy, average family size, and average income per household inform policy decisions.

#### Survey Interpretation
Average satisfaction ratings, average response times, and average scores on standardized assessments guide organizational improvements.

---

### 4.8 Using Tables and Organized Data

When solving average problems, organizing data in tables prevents arithmetic errors — especially under exam time pressure.

#### Data Table Method

| Day | Sales (₱) |
|-----|-----------|
| Mon | 12,500 |
| Tue | 14,200 |
| Wed | 11,800 |
| Thu | 15,000 |
| Fri | 13,500 |
| **Total** | **67,000** |

Mean = 67,000 ÷ 5 = **₱13,400**

#### Grouped Computation Trick

When numbers are close to each other, pick a reference value and compute deviations:

Values: 78, 82, 80, 76, 84. Reference = 80.

| Value | Deviation from 80 |
|-------|-------------------|
| 78 | −2 |
| 82 | +2 |
| 80 | 0 |
| 76 | −4 |
| 84 | +4 |
| **Sum of deviations** | **0** |

Mean = 80 + (0 ÷ 5) = **80**

This shortcut is powerful when values cluster around a central number.

---

### 4.9 Problem-Solving Strategies

#### Strategy 1: Identify What's Given and What's Asked

Before computing anything, classify the problem:
- **Type A:** Given all values → find the mean
- **Type B:** Given the mean and some values → find a missing value
- **Type C:** Given the mean and count → find the total
- **Type D:** Comparing averages between groups

#### Strategy 2: Write the Formula First

Always start by writing:
$$
\text{Mean} = \frac{\text{Sum}}{n}
$$

Then plug in what you know and solve for what you don't.

#### Strategy 3: Check Reasonableness

Your answer must fall within the range of the given values (for Type A problems). If the values are between 70 and 95, the average cannot be 120 or 50.

#### Strategy 4: Verify by Reconstruction

After finding a missing value, plug it back in and verify the average matches.

#### Strategy 5: Use Estimation First

Before detailed computation, estimate: "These numbers are all around 80, so the average should be near 80." This catches gross arithmetic errors.

---

### 4.10 Estimation and Mental Math Techniques

#### Technique 1: Round and Adjust

Values: 47, 53, 49, 51, 50.
Round all to 50 → estimate = 50.
Actual: (47+53+49+51+50) ÷ 5 = 250 ÷ 5 = 50. Estimate was exact!

#### Technique 2: Pair Complementary Numbers

Values: 35, 65, 40, 60, 50.
Pair: (35+65)=100, (40+60)=100, plus 50 = 250.
Mean = 250 ÷ 5 = 50.

#### Technique 3: Use the Deviation Method

Values: 102, 98, 105, 95, 100.
Reference = 100. Deviations: +2, −2, +5, −5, 0. Sum = 0.
Mean = 100 + 0/5 = 100.

#### Technique 4: Factor Out Common Multiples

Values: 200, 300, 400, 500, 600.
Factor out 100: averages of 2, 3, 4, 5, 6 = 20 ÷ 5 = 4.
Mean = 4 × 100 = 400.

---

### 4.11 Common Errors in Average Problems

| Error | Example | Correct Approach |
|-------|---------|-----------------|
| Forgetting to divide | Sum = 360, writes 360 as answer | 360 ÷ 4 = 90 |
| Wrong divisor | 5 values, divides by 4 | Count carefully: n = 5 |
| Arithmetic mistake | 23 + 45 + 32 = 90 (wrong) | 23 + 45 + 32 = 100 |
| Confusing mean with median | Picks middle value | Compute sum ÷ count |
| Rounding too early | Rounds each value before adding | Add exact values first, round at end |
| Missing a value | Skips one number in the list | Re-count and verify against problem |

---

## Step-by-Step Rules

### Computing the Arithmetic Mean
1. List all values
2. Add all values to get the sum
3. Count the number of values (n)
4. Divide: Mean = Sum ÷ n
5. Verify: Mean × n should equal the sum

### Finding a Missing Value
1. Identify the target average and total count
2. Compute required total: Mean × Count
3. Add all known values
4. Subtract: Missing value = Required total − Known sum
5. Verify: Include the missing value and recompute the average

### Comparing Group Averages
1. Compute each group's average separately
2. For combined average: use weighted formula (not simple average of averages)
3. Compare and interpret in context

---

## Exam Strategies

1. **Estimate first** — mentally approximate the answer before computing
2. **Group compatible numbers** — pair values that sum to round numbers
3. **Use the deviation method** — when values cluster around a central number
4. **Check answer range** — the mean must be between the smallest and largest values
5. **Watch for "missing value" keywords** — "what score is needed," "find the unknown," "what must the value be"
6. **Don't average averages** — when combining groups, use weighted averages
7. **Verify with multiplication** — Mean × Count = Sum is your fastest check
8. **Manage time** — if stuck, estimate and move on; return if time permits

---

## Mini Practice Set

**1.** Find the average of 15, 20, 25, 30, and 35.
**Answer:** 25
**Explanation:** Sum = 125. Count = 5. Mean = 125 ÷ 5 = 25.

**2.** What is the mean of 8, 12, 16, and 24?
**Answer:** 15
**Explanation:** Sum = 60. Count = 4. Mean = 60 ÷ 4 = 15.

**3.** A student scored 88, 92, 76, and 84. What is her average?
**Answer:** 85
**Explanation:** Sum = 340. Count = 4. Mean = 340 ÷ 4 = 85.

**4.** The average of 5 numbers is 40. What is their sum?
**Answer:** 200
**Explanation:** Sum = Mean × Count = 40 × 5 = 200.

**5.** The average of 6 numbers is 15. If five of them are 12, 14, 16, 18, and 20, find the sixth.
**Answer:** 10
**Explanation:** Required sum = 15 × 6 = 90. Known sum = 80. Missing = 90 − 80 = 10.

**6.** Find the average of 100, 200, 300, 400, and 500.
**Answer:** 300
**Explanation:** Sum = 1,500. Count = 5. Mean = 1,500 ÷ 5 = 300.

**7.** A worker earned ₱450, ₱520, ₱480, and ₱550 over 4 days. What is the average daily earning?
**Answer:** ₱500
**Explanation:** Sum = 2,000. Count = 4. Mean = 2,000 ÷ 4 = 500.

**8.** The average height of 3 students is 160 cm. If two students are 155 cm and 165 cm, how tall is the third?
**Answer:** 160 cm
**Explanation:** Required sum = 160 × 3 = 480. Known = 155 + 165 = 320. Missing = 480 − 320 = 160.

**9.** What is the average of 2.5, 3.5, 4.0, and 5.0?
**Answer:** 3.75
**Explanation:** Sum = 15.0. Count = 4. Mean = 15.0 ÷ 4 = 3.75.

**10.** The average age of 4 employees is 28. A new employee aged 33 joins. What is the new average?
**Answer:** 29
**Explanation:** Original sum = 28 × 4 = 112. New sum = 112 + 33 = 145. New average = 145 ÷ 5 = 29.

**11.** Find the average of 72, 68, 75, 80, and 65.
**Answer:** 72
**Explanation:** Sum = 360. Count = 5. Mean = 360 ÷ 5 = 72.

**12.** A class of 10 students has an average score of 82. What is the total of all scores?
**Answer:** 820
**Explanation:** Sum = Mean × Count = 82 × 10 = 820.

**13.** The average of three numbers is 50. Two of the numbers are 45 and 60. What is the third?
**Answer:** 45
**Explanation:** Required sum = 50 × 3 = 150. Known = 45 + 60 = 105. Missing = 150 − 105 = 45.

**14.** A delivery van traveled 120 km, 135 km, 110 km, and 155 km over 4 days. What is the average distance per day?
**Answer:** 130 km
**Explanation:** Sum = 520. Count = 4. Mean = 520 ÷ 4 = 130.

**15.** The average of 8 numbers is 12.5. What is their sum?
**Answer:** 100
**Explanation:** Sum = 12.5 × 8 = 100.

**16.** Find the average: 1,000; 2,000; 3,000; 4,000.
**Answer:** 2,500
**Explanation:** Sum = 10,000. Count = 4. Mean = 10,000 ÷ 4 = 2,500.

**17.** A student needs an average of 90 across 5 exams. She scored 88, 92, 85, and 94 on the first four. What does she need on the 5th?
**Answer:** 91
**Explanation:** Required sum = 90 × 5 = 450. Known = 359. Missing = 450 − 359 = 91.

**18.** The average monthly rent for 12 months is ₱8,500. What is the total annual rent?
**Answer:** ₱102,000
**Explanation:** Sum = 8,500 × 12 = 102,000.

**19.** Team A averages 85 points; Team B averages 90 points. Which team has the higher average?
**Answer:** Team B
**Explanation:** 90 > 85, so Team B has the higher average score.

**20.** The average of 4 numbers is 25. If one number is removed and the new average is 20, what number was removed?
**Answer:** 40
**Explanation:** Original sum = 25 × 4 = 100. New sum = 20 × 3 = 60. Removed = 100 − 60 = 40.

---

## Quick Recap

| Concept | Key Point |
|---------|-----------|
| Meaning of Average | A single value representing equal distribution of the total |
| Formula | Mean = Sum ÷ Count |
| Sum-Count Relationship | Sum = Mean × Count; Count = Sum ÷ Mean |
| Interpreting Averages | Averages represent typical values but may not equal any actual data point |
| Comparing Averages | Use weighted averages when combining groups of different sizes |
| Missing Values | Required total − Known sum = Missing value |
| Practical Uses | Grades, salaries, expenses, production, speed, budgets |

---

## Memory Aids

- **"SAC"** — Sum, Average, Count. Know two, find the third.
- **"Sum = Average × Count"** — The golden equation for missing-value problems.
- **"Between the extremes"** — The average always falls between the smallest and largest values.
- **"Don't average averages"** — When combining groups, weight by group size.
- **"Multiply to verify"** — After computing the mean, multiply by n to check you get the sum back.

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

- **Weighted Average:** Simple averages are a special case of weighted averages where all weights are equal
- **Finding Missing Values in Averages:** The average formula rearranges to find missing values — same equation, different unknown
- **Basic Percentage Problems:** Averages and percentages both involve dividing a part by a total — the arithmetic is identical
- **Ratio and Proportion:** Averages can be expressed as ratios (sum:count) and proportions (average/total = 1/n)

### Mastery Checklist
After completing this lesson, you should be able to:

- ✅ Define average (mean) correctly
- ✅ Compute arithmetic mean accurately for any set of numbers
- ✅ Identify and use the Sum = Mean × Count relationship
- ✅ Solve missing-value average problems confidently
- ✅ Interpret averages in real-life contexts
- ✅ Compare averages between groups correctly (using weighted averages)
- ✅ Estimate averages mentally using shortcuts
- ✅ Avoid common arithmetic and conceptual errors
- ✅ Solve CSE-style average questions efficiently under time pressure

> 🤔 **Why does this work?** The arithmetic mean "levels out" a set of values — it finds the single value that, if every item equaled it, would produce the same total. Mathematically, mean = sum/count, which means sum = mean × count. This relationship is why the mean is the "balance point" of a data set: values above the mean contribute positive deviations that exactly cancel the negative deviations from values below it.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


> **Misconception:** "A memorized shortcut always works."

> **Why it fails:** Different question structures require different setups.

> **Correct model:** Identify the relationship first, then choose the method.


### Mastery Checklist

- [ ] I can solve representative items accurately and quickly.
- [ ] I can explain common traps and how to avoid them.
- [ ] I can transfer this method to mixed-question sets.
