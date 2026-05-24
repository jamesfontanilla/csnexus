# Finding Missing Values in Averages

## Explanations

### Introduction

**Finding missing values in averages** is one of the most frequently tested problem types in the Philippine Civil Service Examination. Unlike straightforward average computation (where you add values and divide), these problems give you the average and ask you to work **backward** to determine an unknown quantity.

This skill appears everywhere in professional life:
- A teacher needs to know what score a student must earn on the final exam to achieve a target GPA
- A budget officer must determine how much a department can spend in December to stay within the annual average allocation
- An HR analyst calculates what salary offer would bring a team's average compensation to a target level
- A transportation planner determines what daily ridership is needed to meet quarterly targets
- An engineer identifies what measurement reading would keep the production average within tolerance

In the CSE, missing-value average problems test your ability to:
- Reverse the average formula (multiply instead of divide)
- Manage multi-step arithmetic under time pressure
- Interpret word problems and extract the correct numbers
- Verify answers logically (does the missing value make sense?)

### Common Mistakes Examinees Make

1. **Dividing when you should multiply** — computing Mean ÷ n instead of Mean × n to find the total
2. **Forgetting to subtract the known sum** — finding the required total but reporting it as the answer
3. **Miscounting the number of items** — especially when the problem says "5 tests" but lists only 4 known scores (the 5th is what you're solving for)
4. **Adding the average into the known values** — treating the given average as one of the data points
5. **Arithmetic errors in summation** — especially with 5+ numbers or decimals
6. **Not verifying the answer** — failing to check that plugging the answer back gives the stated average
7. **Confusing "new average" with "old average"** — in problems where a member is added or removed
8. **Ignoring whether the answer is reasonable** — a missing test score of 150 out of 100 is impossible

### Learning Objectives

After this lesson, you should be able to:
- Identify missing-value average problems correctly from word problem phrasing
- Convert a given average into a total sum using the formula Sum = Mean × Count
- Solve for one unknown number by subtracting known values from the required total
- Solve for multiple missing values using algebraic reasoning and grouped totals
- Handle multi-step average problems (added members, removed members, changing averages)
- Analyze how adding or removing values affects the mean
- Interpret practical average situations in workplace, school, and government contexts
- Solve CSE-style missing-average questions efficiently under time pressure

---

### 4.1 Review of the Average Formula

The **arithmetic mean** (average) connects three quantities:

$$
\text{Mean} = \frac{\text{Sum of All Values}}{\text{Number of Values (n)}}
$$

This formula can be rearranged into three equivalent forms:

| If you know... | You can find... | Formula |
|----------------|----------------|---------|
| Sum and n | Mean | Mean = Sum ÷ n |
| Mean and n | Sum | **Sum = Mean × n** |
| Sum and Mean | n | n = Sum ÷ Mean |

#### Why Rearrangement Matters

For missing-value problems, the second form is the key:

$$
\text{Sum} = \text{Mean} \times n
$$

This tells you: *if the average of n numbers is some value, then those n numbers must add up to Mean × n.* Once you know what the total **must** be, finding a missing piece is just subtraction.

#### The "Equal Sharing" Interpretation

Think of the average as what each item would be if the total were distributed equally. If 5 employees have an average salary of ₱30,000, the total payroll is ₱150,000. If you know 4 of the salaries, the 5th is whatever makes the total reach ₱150,000.

#### The "Balance Point" Interpretation

The average is the balance point of a dataset. If you know the average and all values except one, the missing value must be positioned so that the data still balances at the stated mean. Values below the mean create a "deficit" that the missing value must compensate for, and vice versa.

#### Visual Example

Suppose 4 numbers have an average of 50:

```
Required total = 50 × 4 = 200

Known values: 40, 55, 60
Known sum:    40 + 55 + 60 = 155

Missing value = 200 - 155 = 45

Verification: (40 + 55 + 60 + 45) ÷ 4 = 200 ÷ 4 = 50 ✓
```

---

### 4.2 Converting Average to Total Sum

This is the **first and most critical step** in every missing-value problem. Before you can find what's missing, you need to know what the total should be.

#### The Golden Rule

$$
\text{Total Sum} = \text{Mean} \times \text{Number of Values}
$$

#### Why This Step Is Essential

The average alone doesn't tell you individual values. But the **total** constrains them. If 6 numbers average 25, their total is exactly 150 — no matter how the individual values are distributed. This constraint is what makes solving for unknowns possible.

#### Easy Examples

**Example 1:** The average of 4 numbers is 20. What is their total sum?
- Total = 20 × 4 = **80**

**Example 2:** A student's average across 5 exams is 88. What is the total of all exam scores?
- Total = 88 × 5 = **440**

**Example 3:** The average monthly expense of a family is ₱18,000 over 12 months. What is the annual total?
- Total = 18,000 × 12 = **₱216,000**

#### Medium Examples

**Example 4:** The average daily output of a factory over 22 working days is 156 units. What is the total monthly production?
- Total = 156 × 22 = **3,432 units**

**Example 5:** A government office processes an average of 45 applications per day over a 5-day work week. What is the weekly total?
- Total = 45 × 5 = **225 applications**

#### Hard Examples

**Example 6:** The average score of 35 students on a standardized test is 78.4. What is the combined total of all scores?
- Total = 78.4 × 35 = **2,744**

**Example 7:** A delivery fleet's average fuel consumption is 12.5 liters per trip across 48 trips in a month. What is the total fuel used?
- Total = 12.5 × 48 = **600 liters**

---

### 4.3 Finding One Missing Value

This is the classic CSE problem type: you know the average, you know all values except one, and you must find the unknown.

#### Step-by-Step Procedure

1. **Identify** the given average and the total count of values (n)
2. **Compute** the required total: Required Sum = Mean × n
3. **Add** all known values: Known Sum = sum of given numbers
4. **Subtract** to find the missing value: Missing = Required Sum − Known Sum
5. **Verify** by including the answer and recomputing the average

#### Easy Examples

**Example 1:** The average of 5 numbers is 18. Four of the numbers are 15, 17, 20, and 22. What is the missing number?

```
Step 1: Required total = 18 × 5 = 90
Step 2: Known sum = 15 + 17 + 20 + 22 = 74
Step 3: Missing value = 90 − 74 = 16
Verify: (15 + 17 + 20 + 22 + 16) ÷ 5 = 90 ÷ 5 = 18 ✓
```

**Answer: 16**

**Example 2:** A student scored 82, 90, and 76 on three quizzes. What must she score on the 4th quiz to have an average of 84?

```
Step 1: Required total = 84 × 4 = 336
Step 2: Known sum = 82 + 90 + 76 = 248
Step 3: Missing score = 336 − 248 = 88
Verify: (82 + 90 + 76 + 88) ÷ 4 = 336 ÷ 4 = 84 ✓
```

**Answer: 88**

#### Medium Examples

**Example 3:** The average monthly electricity bill for a household over 6 months is ₱3,400. The bills for the first 5 months were ₱3,100, ₱3,600, ₱3,200, ₱3,800, and ₱2,900. What was the 6th month's bill?

```
Step 1: Required total = 3,400 × 6 = 20,400
Step 2: Known sum = 3,100 + 3,600 + 3,200 + 3,800 + 2,900 = 16,600
Step 3: Missing bill = 20,400 − 16,600 = 3,800
Verify: (3,100 + 3,600 + 3,200 + 3,800 + 2,900 + 3,800) ÷ 6 = 20,400 ÷ 6 = 3,400 ✓
```

**Answer: ₱3,800**

**Example 4:** A salesperson's average weekly sales over 4 weeks is ₱125,000. Sales for weeks 1–3 were ₱110,000, ₱140,000, and ₱130,000. What were the sales in week 4?

```
Step 1: Required total = 125,000 × 4 = 500,000
Step 2: Known sum = 110,000 + 140,000 + 130,000 = 380,000
Step 3: Missing = 500,000 − 380,000 = 120,000
```

**Answer: ₱120,000**

#### Hard Examples

**Example 5:** A team of 8 engineers has an average project completion time of 14.5 days. Seven of the completion times are: 12, 16, 13, 15, 17, 11, and 14 days. What is the 8th engineer's completion time?

```
Step 1: Required total = 14.5 × 8 = 116
Step 2: Known sum = 12 + 16 + 13 + 15 + 17 + 11 + 14 = 98
Step 3: Missing = 116 − 98 = 18
Verify: (12 + 16 + 13 + 15 + 17 + 11 + 14 + 18) ÷ 8 = 116 ÷ 8 = 14.5 ✓
```

**Answer: 18 days**

**Example 6:** The average score of 10 applicants on a civil service exam is 82.6. Nine of the scores are: 78, 85, 90, 76, 88, 80, 84, 79, and 82. What is the 10th applicant's score?

```
Step 1: Required total = 82.6 × 10 = 826
Step 2: Known sum = 78 + 85 + 90 + 76 + 88 + 80 + 84 + 79 + 82 = 742
Step 3: Missing = 826 − 742 = 84
Verify: (742 + 84) ÷ 10 = 826 ÷ 10 = 82.6 ✓
```

**Answer: 84**

---

### 4.4 Finding Multiple Missing Values

Sometimes a problem involves more than one unknown. These require additional information — typically a relationship between the unknowns or grouped sub-averages.

#### When Two Unknowns Exist

If two values are missing, you need one additional equation (a relationship between them) to solve the problem. Common relationships:
- One value is twice the other
- The two values differ by a specific amount
- The two values are equal
- One group's sub-average is given

#### Example with a Given Relationship

**Problem:** The average of 5 numbers is 30. Three of the numbers are 25, 35, and 28. The remaining two numbers are equal. Find them.

```
Step 1: Required total = 30 × 5 = 150
Step 2: Known sum = 25 + 35 + 28 = 88
Step 3: Sum of two unknowns = 150 − 88 = 62
Step 4: Since they're equal: each = 62 ÷ 2 = 31
```

**Answer: Both missing values are 31**

#### Example with a Difference Relationship

**Problem:** The average of 4 numbers is 40. Two of the numbers are 35 and 50. The other two differ by 10. Find them.

```
Step 1: Required total = 40 × 4 = 160
Step 2: Known sum = 35 + 50 = 85
Step 3: Sum of two unknowns = 160 − 85 = 75
Step 4: Let the smaller = x, larger = x + 10
        x + (x + 10) = 75
        2x + 10 = 75
        2x = 65
        x = 32.5, so the other = 42.5
```

**Answer: 32.5 and 42.5**

#### Example with Grouped Sub-Averages

**Problem:** A class of 30 students has an average score of 75. The 18 boys have an average of 72. What is the girls' average?

```
Step 1: Total class sum = 75 × 30 = 2,250
Step 2: Boys' total = 72 × 18 = 1,296
Step 3: Girls' total = 2,250 − 1,296 = 954
Step 4: Number of girls = 30 − 18 = 12
Step 5: Girls' average = 954 ÷ 12 = 79.5
```

**Answer: The girls' average is 79.5**

#### Example with Department Averages

**Problem:** A company has 3 departments. Department A (10 employees) averages ₱28,000. Department B (15 employees) averages ₱32,000. The company-wide average for all 40 employees is ₱31,000. What is Department C's average salary?

```
Step 1: Company total = 31,000 × 40 = 1,240,000
Step 2: Dept A total = 28,000 × 10 = 280,000
Step 3: Dept B total = 32,000 × 15 = 480,000
Step 4: Dept C total = 1,240,000 − 280,000 − 480,000 = 480,000
Step 5: Dept C employees = 40 − 10 − 15 = 15
Step 6: Dept C average = 480,000 ÷ 15 = ₱32,000
```

**Answer: Department C's average salary is ₱32,000**

---

### 4.5 Multi-Step Average Problems

These problems require organizing information across multiple stages. They often involve averages that change when members are added, removed, or when new information is revealed.

#### Type 1: Adding a New Member

**Problem:** The average age of 6 committee members is 42. A new member joins, and the average becomes 40. How old is the new member?

```
Step 1: Original total = 42 × 6 = 252
Step 2: New total = 40 × 7 = 280
Step 3: New member's age = 280 − 252 = 28
```

**Answer: 28 years old**

#### Type 2: Removing a Member

**Problem:** The average weight of 10 players is 72 kg. When one player leaves, the average becomes 71 kg. What is the weight of the player who left?

```
Step 1: Original total = 72 × 10 = 720
Step 2: New total (9 players) = 71 × 9 = 639
Step 3: Weight of player who left = 720 − 639 = 81 kg
```

**Answer: 81 kg**

#### Type 3: Replacing a Member

**Problem:** The average salary of 5 employees is ₱25,000. One employee earning ₱22,000 is replaced by a new hire. The new average becomes ₱26,000. What is the new hire's salary?

```
Step 1: Original total = 25,000 × 5 = 125,000
Step 2: New total = 26,000 × 5 = 130,000
Step 3: Increase in total = 130,000 − 125,000 = 5,000
Step 4: New hire's salary = 22,000 + 5,000 = 27,000
```

**Answer: ₱27,000**

#### Type 4: Combining Groups

**Problem:** Group A has 8 members with an average score of 85. Group B has 12 members with an average score of 90. What is the combined average?

```
Step 1: Group A total = 85 × 8 = 680
Step 2: Group B total = 90 × 12 = 1,080
Step 3: Combined total = 680 + 1,080 = 1,760
Step 4: Combined count = 8 + 12 = 20
Step 5: Combined average = 1,760 ÷ 20 = 88
```

**Answer: 88**

**Important:** The combined average is NOT (85 + 90) ÷ 2 = 87.5. You must weight by group size.

#### Type 5: Sequential Averages

**Problem:** After 4 innings, a batsman's average is 32 runs. After the 5th inning, his average increases to 36. How many runs did he score in the 5th inning?

```
Step 1: Total after 4 innings = 32 × 4 = 128
Step 2: Total after 5 innings = 36 × 5 = 180
Step 3: Runs in 5th inning = 180 − 128 = 52
```

**Answer: 52 runs**

#### Type 6: Correcting an Error

**Problem:** A teacher calculated the average of 20 students as 78. Later she discovered that one score was recorded as 65 instead of the correct 85. What is the correct average?

```
Step 1: Incorrect total = 78 × 20 = 1,560
Step 2: Correction = 85 − 65 = +20
Step 3: Correct total = 1,560 + 20 = 1,580
Step 4: Correct average = 1,580 ÷ 20 = 79
```

**Answer: 79**

---

### 4.6 Effect of Adding or Removing Values

Understanding how the average shifts when values are added or removed is crucial for CSE problems that ask "by how much does the average change?"

#### Adding a Value Greater Than the Current Average

When you add a number **larger** than the current average, the new average **increases**.

**Example:** Current average of 5 numbers = 40. A 6th number (52) is added.
- Original total = 40 × 5 = 200
- New total = 200 + 52 = 252
- New average = 252 ÷ 6 = 42
- The average increased by 2.

#### Adding a Value Less Than the Current Average

When you add a number **smaller** than the current average, the new average **decreases**.

**Example:** Current average of 4 numbers = 60. A 5th number (40) is added.
- Original total = 60 × 4 = 240
- New total = 240 + 40 = 280
- New average = 280 ÷ 5 = 56
- The average decreased by 4.

#### Adding a Value Equal to the Current Average

When you add a number **equal** to the current average, the average **stays the same**.

**Example:** Current average of 3 numbers = 50. A 4th number (50) is added.
- Original total = 50 × 3 = 150
- New total = 150 + 50 = 200
- New average = 200 ÷ 4 = 50
- No change.

#### Removing a Value Greater Than the Current Average

When you remove a number **larger** than the current average, the new average **decreases**.

**Example:** Average of 6 numbers = 50. Remove a value of 62.
- Original total = 50 × 6 = 300
- New total = 300 − 62 = 238
- New average = 238 ÷ 5 = 47.6
- The average decreased by 2.4.

#### Removing a Value Less Than the Current Average

When you remove a number **smaller** than the current average, the new average **increases**.

**Example:** Average of 5 numbers = 70. Remove a value of 55.
- Original total = 70 × 5 = 350
- New total = 350 − 55 = 295
- New average = 295 ÷ 4 = 73.75
- The average increased by 3.75.

#### Quick Rule Summary

| Action | Value vs. Average | Effect on Average |
|--------|------------------|-------------------|
| Add | Value > Average | Average increases |
| Add | Value < Average | Average decreases |
| Add | Value = Average | No change |
| Remove | Value > Average | Average decreases |
| Remove | Value < Average | Average increases |
| Remove | Value = Average | No change |

#### Sports Statistics Example

A basketball player's scoring average over 10 games is 22 points. In the 11th game, he scores 33 points.
- Original total = 22 × 10 = 220
- New total = 220 + 33 = 253
- New average = 253 ÷ 11 = 23
- His average increased by 1 point.

#### Salary Adjustment Example

A department of 8 employees has an average salary of ₱35,000. The lowest-paid employee (₱24,000) resigns.
- Original total = 35,000 × 8 = 280,000
- New total = 280,000 − 24,000 = 256,000
- New average = 256,000 ÷ 7 ≈ ₱36,571
- The average increased by approximately ₱1,571.

---

### 4.7 Practical Applications of Missing Averages

#### School Grades

A student needs an average of 85 across 6 subjects to qualify for honors. After 5 subjects, her scores are 88, 82, 90, 79, and 86. What minimum score does she need in the 6th subject?
- Required total = 85 × 6 = 510
- Current sum = 88 + 82 + 90 + 79 + 86 = 425
- Minimum 6th score = 510 − 425 = **85**

#### Employee Salaries

A company wants its 12-person team to have an average salary of ₱40,000. Eleven employees earn: ₱38K, ₱42K, ₱35K, ₱45K, ₱39K, ₱41K, ₱37K, ₱43K, ₱36K, ₱44K, ₱40K. What should the 12th employee's salary be?
- Required total = 40,000 × 12 = 480,000
- Known sum = 440,000
- 12th salary = 480,000 − 440,000 = **₱40,000**

#### Transportation Statistics

A bus company wants its fleet's average daily mileage to be 180 km across 10 buses. Nine buses logged: 175, 190, 165, 200, 185, 170, 195, 160, and 180 km. What must the 10th bus achieve?
- Required total = 180 × 10 = 1,800
- Known sum = 1,620
- 10th bus = 1,800 − 1,620 = **180 km**

#### Engineering Measurements

A quality control engineer needs the average thickness of 8 steel plates to be 5.0 mm. Seven plates measure: 4.8, 5.2, 4.9, 5.1, 5.3, 4.7, and 5.0 mm. What must the 8th plate measure?
- Required total = 5.0 × 8 = 40.0
- Known sum = 35.0
- 8th plate = 40.0 − 35.0 = **5.0 mm**

#### Budgeting

A department's average monthly spending must not exceed ₱250,000 over a fiscal year (12 months). After 11 months, total spending is ₱2,680,000. What is the maximum the department can spend in December?
- Maximum annual total = 250,000 × 12 = 3,000,000
- Remaining budget = 3,000,000 − 2,680,000 = **₱320,000**

#### Government Surveys

A municipality reports that the average household income across 500 surveyed households is ₱25,000. If 499 households have a combined income of ₱12,450,000, what is the 500th household's income?
- Required total = 25,000 × 500 = 12,500,000
- Missing = 12,500,000 − 12,450,000 = **₱50,000**

---

### 4.8 Using Tables, Charts, and Visual Models

#### Organizing Data in Tables

When a problem gives you many values, organize them in a table to avoid arithmetic errors:

| Employee | Score |
|----------|-------|
| Ana | 85 |
| Ben | 78 |
| Cara | 92 |
| Dan | 88 |
| Eva | ? |
| **Average** | **86** |

- Required total = 86 × 5 = 430
- Known sum = 85 + 78 + 92 + 88 = 343
- Eva's score = 430 − 343 = **87**

#### The "Running Total" Method

For problems with many numbers, keep a running total to reduce errors:

| Value | Running Total |
|-------|--------------|
| 45 | 45 |
| 52 | 97 |
| 38 | 135 |
| 61 | 196 |
| 44 | 240 |

This is faster and less error-prone than adding all numbers at once.

#### Comparison Chart for Group Problems

| Group | Count | Average | Total |
|-------|-------|---------|-------|
| Section A | 25 | 80 | 2,000 |
| Section B | 30 | 85 | 2,550 |
| **Combined** | **55** | **?** | **4,550** |

Combined average = 4,550 ÷ 55 = **82.7**

#### Balance Diagram

Think of the average as a fulcrum. Values above the average create surplus; values below create deficit. The missing value must balance the system.

```
Average = 50

Known values: 45 (-5), 55 (+5), 40 (-10), 60 (+10), ?
Net from known: -5 + 5 + (-10) + 10 = 0
Missing value must contribute 0 deviation → Missing = 50
```

This mental model helps you estimate quickly whether the missing value should be above or below the average.

---

### 4.9 Problem-Solving Strategies

#### Strategy 1: Always Find the Total First

No matter how complex the problem looks, start with:
$$\text{Total} = \text{Average} \times \text{Count}$$

This single step transforms every missing-value problem into a subtraction problem.

#### Strategy 2: Count Carefully

The most common error is miscounting n. Read the problem twice:
- "The average of 5 numbers..." → n = 5
- "A student took 4 exams and wants to know what to score on the 5th..." → n = 5 (not 4)
- "The average of a group of 8 is 50. One person leaves..." → original n = 8, new n = 7

#### Strategy 3: Check Answer Reasonableness

After solving, ask: "Does this answer make sense?"
- If the average is 80 and all known values are between 70–90, the missing value should also be in a reasonable range
- A missing test score above 100 (on a 100-point scale) is impossible
- A missing salary that's negative is impossible

#### Strategy 4: Use the Deviation Shortcut

Instead of computing the full total, think in terms of deviations from the average:

**Problem:** Average of 5 numbers is 60. Four numbers are 55, 65, 58, 62. Find the 5th.

Deviations from 60: −5, +5, −2, +2 = 0 net deviation.
Since the net deviation of known values is 0, the missing value must also have 0 deviation → Missing = 60.

**Problem:** Average of 4 numbers is 50. Three numbers are 45, 55, 48. Find the 4th.

Deviations from 50: −5, +5, −2 = −2 net deviation.
The missing value must compensate: deviation = +2 → Missing = 52.

#### Strategy 5: Work Backward from Answer Choices

On multiple-choice exams, you can plug each answer choice back in and check which one gives the stated average. This is slower but guarantees accuracy when you're unsure of your arithmetic.

#### Strategy 6: Identify the Problem Type First

Before computing, classify:
- **Simple missing value:** Know average, know all but one value
- **Added member:** Average changes when someone joins
- **Removed member:** Average changes when someone leaves
- **Replacement:** One value is swapped for another
- **Combined groups:** Two groups merge, find combined average
- **Corrected error:** A recorded value was wrong, find correct average

Each type has a specific approach. Identifying the type saves time.

---

### 4.10 Estimation and Mental Math Techniques

#### Technique 1: Estimate the Missing Value's Range

Before computing, note: the missing value should be "near" the average (unless the other values are extreme). If the average is 80 and known values are 75, 82, 78, 85, the missing value is probably between 70–90.

#### Technique 2: Use Round Numbers

When computing totals mentally:
- 85 × 6: Think 80 × 6 = 480, plus 5 × 6 = 30, total = 510
- 42 × 8: Think 40 × 8 = 320, plus 2 × 8 = 16, total = 336

#### Technique 3: Group Compatible Numbers When Summing

When adding known values: 23 + 47 + 35 + 15 + 30
- Group: (23 + 47) = 70, (35 + 15) = 50, + 30 = 150
- Much faster than sequential addition

#### Technique 4: The "Excess and Deficit" Method

For each known value, calculate how much it's above or below the average:
- Average = 40. Values: 38 (−2), 44 (+4), 36 (−4), 42 (+2)
- Net: −2 + 4 − 4 + 2 = 0
- Missing value = average + 0 = 40

This avoids computing large totals entirely.

#### Technique 5: Eliminate Unreasonable Choices

On the CSE, if choices are 45, 52, 78, 91 and you estimate the answer should be around 50, immediately eliminate 78 and 91. Now you only need to verify between 45 and 52.

#### Technique 6: Multiply by Decomposition

For Required Total = 78 × 5:
- 78 × 5 = (80 − 2) × 5 = 400 − 10 = 390

For Required Total = 86 × 7:
- 86 × 7 = (90 − 4) × 7 = 630 − 28 = 602

---

### 4.11 Common Errors in Missing-Average Problems

| Error | What Goes Wrong | How to Avoid It |
|-------|----------------|-----------------|
| Dividing instead of multiplying | Computes Mean ÷ n instead of Mean × n | Remember: to find total, MULTIPLY |
| Forgetting to subtract | Finds required total (e.g., 450) and writes it as the answer | The missing value = Total − Known Sum |
| Wrong count | Uses 4 instead of 5 when the problem says "5 numbers" | Re-read the problem; count explicitly |
| Adding the average as a value | Includes the given average (e.g., 85) as one of the known numbers | The average is NOT a data point |
| Arithmetic errors | 78 + 82 + 91 = 249 (should be 251) | Use running totals; double-check sums |
| Not verifying | Gets 47 but doesn't check if it produces the stated average | Always verify: (all values) ÷ n = stated average? |
| Impossible answers | Gets a score of 112 on a 100-point test | Check if the answer is within valid bounds |
| Confusing old/new average | Uses the new average where the old one belongs (or vice versa) | Label clearly: "original" vs. "new" |

---

## Step-by-Step Rules

### Finding a Single Missing Value
1. Identify the average and the total count (n)
2. Compute Required Total = Average × n
3. Sum all known values = Known Sum
4. Missing Value = Required Total − Known Sum
5. Verify: (Known Sum + Missing Value) ÷ n = Average

### Adding/Removing a Member
1. Compute Original Total = Original Average × Original Count
2. Compute New Total = New Average × New Count
3. Value of added member = New Total − Original Total
4. Value of removed member = Original Total − New Total

### Replacing a Member
1. Compute Original Total = Original Average × n
2. Compute New Total = New Average × n
3. Difference = New Total − Original Total
4. New member's value = Old member's value + Difference

### Combining Groups
1. Compute each group's total = Group Average × Group Count
2. Combined Total = sum of all group totals
3. Combined Count = sum of all group counts
4. Combined Average = Combined Total ÷ Combined Count

### Correcting an Error
1. Compute Incorrect Total = Incorrect Average × n
2. Correct Total = Incorrect Total − Wrong Value + Correct Value
3. Correct Average = Correct Total ÷ n

---

## Exam Strategies

1. **Multiply first, subtract second** — this two-step process solves 80% of missing-value problems
2. **Label your quantities** — write "Required Total," "Known Sum," "Missing" to stay organized
3. **Estimate before computing** — if the average is 75 and you have 5 values near 75, the missing value should be near 75 too
4. **Watch for "new average" problems** — these require computing TWO totals (before and after)
5. **Don't average averages** — when combining groups, always use weighted totals
6. **Verify with multiplication** — after finding the missing value, check that (all values) ÷ n = stated average
7. **Use answer choices** — on multiple choice, plug in the answer and verify; this catches arithmetic errors
8. **Manage your time** — simple missing-value problems should take 30–60 seconds; multi-step problems may take 90 seconds

---

## Mini Practice Set

**1.** The average of 5 numbers is 24. Four of them are 20, 25, 28, and 22. What is the 5th number?
**Answer:** 25
**Explanation:** Required total = 24 × 5 = 120. Known sum = 20 + 25 + 28 + 22 = 95. Missing = 120 − 95 = 25.

**2.** A student scored 78, 85, and 92 on three tests. What must she score on the 4th test to average 85?
**Answer:** 85
**Explanation:** Required total = 85 × 4 = 340. Known sum = 78 + 85 + 92 = 255. Missing = 340 − 255 = 85.

**3.** The average salary of 6 employees is ₱32,000. Five earn ₱30K, ₱35K, ₱28K, ₱34K, and ₱31K. What does the 6th earn?
**Answer:** ₱34,000
**Explanation:** Required total = 32,000 × 6 = 192,000. Known sum = 158,000. Missing = 192,000 − 158,000 = 34,000.

**4.** The average of 8 numbers is 15. What is their total sum?
**Answer:** 120
**Explanation:** Total = 15 × 8 = 120.

**5.** The average age of 4 friends is 25. Three of them are 22, 27, and 24. How old is the 4th?
**Answer:** 27
**Explanation:** Required total = 25 × 4 = 100. Known sum = 22 + 27 + 24 = 73. Missing = 100 − 73 = 27.

**6.** The average of 7 numbers is 40. Six of them sum to 235. What is the 7th number?
**Answer:** 45
**Explanation:** Required total = 40 × 7 = 280. Missing = 280 − 235 = 45.

**7.** A team of 5 has an average score of 88. A 6th member joins and the average drops to 85. What is the new member's score?
**Answer:** 73
**Explanation:** Original total = 88 × 5 = 440. New total = 85 × 6 = 510. New member = 510 − 440 = 70. Wait — let me recalculate: 85 × 6 = 510, 510 − 440 = 70. Answer: 70.

Actually, let me correct: Required total = 85 × 6 = 510. Original total = 88 × 5 = 440. New member's score = 510 − 440 = 70.

**Corrected Answer:** 70
**Explanation:** Original total = 88 × 5 = 440. New total = 85 × 6 = 510. New member = 510 − 440 = 70.

**8.** The average weight of 10 boxes is 25 kg. One box is removed and the average becomes 24 kg. What was the removed box's weight?
**Answer:** 34 kg
**Explanation:** Original total = 25 × 10 = 250. New total = 24 × 9 = 216. Removed = 250 − 216 = 34.

**9.** A factory's average daily output for 5 days is 150 units. Output for 4 days: 140, 160, 145, 155. What was the 5th day's output?
**Answer:** 150
**Explanation:** Required total = 150 × 5 = 750. Known sum = 140 + 160 + 145 + 155 = 600. Missing = 750 − 600 = 150.

**10.** The average of 3 numbers is 50. Two numbers are 45 and 60. Find the third.
**Answer:** 45
**Explanation:** Required total = 50 × 3 = 150. Known sum = 45 + 60 = 105. Missing = 150 − 105 = 45.

**11.** After 6 games, a player averages 18 points. After the 7th game, the average rises to 20. How many points in game 7?
**Answer:** 32
**Explanation:** Total after 6 = 18 × 6 = 108. Total after 7 = 20 × 7 = 140. Game 7 = 140 − 108 = 32.

**12.** The average monthly expense is ₱15,000 over 12 months. After 11 months, total spending is ₱162,000. What can be spent in month 12?
**Answer:** ₱18,000
**Explanation:** Annual total = 15,000 × 12 = 180,000. Month 12 = 180,000 − 162,000 = 18,000.

**13.** The average of 6 numbers is 35. Five of them are 30, 40, 32, 38, and 36. Find the 6th.
**Answer:** 34
**Explanation:** Required total = 35 × 6 = 210. Known sum = 30 + 40 + 32 + 38 + 36 = 176. Missing = 210 − 176 = 34.

**14.** A class of 20 students averages 82. If one student's score was incorrectly recorded as 70 instead of 90, what is the correct average?
**Answer:** 83
**Explanation:** Incorrect total = 82 × 20 = 1,640. Correct total = 1,640 − 70 + 90 = 1,660. Correct average = 1,660 ÷ 20 = 83.

**15.** The average of 4 numbers is 60. Two of them are 55 and 65. The other two are equal. Find them.
**Answer:** 60 each
**Explanation:** Required total = 60 × 4 = 240. Known sum = 55 + 65 = 120. Remaining = 240 − 120 = 120. Each = 120 ÷ 2 = 60.

**16.** Group A (10 people) averages 75. Group B (15 people) averages 80. What is the combined average?
**Answer:** 78
**Explanation:** A total = 75 × 10 = 750. B total = 80 × 15 = 1,200. Combined = 1,950 ÷ 25 = 78.

**17.** The average of 5 numbers is 50. If each number is increased by 5, what is the new average?
**Answer:** 55
**Explanation:** When each value increases by 5, the average also increases by 5. New average = 50 + 5 = 55.

**18.** A worker's average daily wage for 6 days is ₱800. For the first 5 days, he earned ₱750, ₱850, ₱780, ₱820, and ₱900. What did he earn on day 6?
**Answer:** ₱700
**Explanation:** Required total = 800 × 6 = 4,800. Known sum = 750 + 850 + 780 + 820 + 900 = 4,100. Missing = 4,800 − 4,100 = 700.

**19.** The average of 10 numbers is 45. One number (55) is removed. What is the new average?
**Answer:** Approximately 43.9
**Explanation:** Original total = 45 × 10 = 450. New total = 450 − 55 = 395. New average = 395 ÷ 9 ≈ 43.9.

**20.** An employee earning ₱28,000 is replaced by one earning ₱36,000 in a team of 5. The original average was ₱30,000. What is the new average?
**Answer:** ₱31,600
**Explanation:** Original total = 30,000 × 5 = 150,000. New total = 150,000 − 28,000 + 36,000 = 158,000. New average = 158,000 ÷ 5 = 31,600.

---

## Quick Recap

| Concept | Key Formula / Rule |
|---------|-------------------|
| Average to Total | Sum = Mean × n |
| Missing Value | Missing = (Mean × n) − Known Sum |
| Adding a Member | New member = (New Mean × New n) − Original Total |
| Removing a Member | Removed = Original Total − (New Mean × New n) |
| Replacing a Member | New value = Old value + (New Total − Old Total) |
| Combining Groups | Combined Mean = (Sum₁ + Sum₂) ÷ (n₁ + n₂) |
| Correcting an Error | Correct Total = Wrong Total − Wrong Value + Right Value |
| Effect of Adding | Value > Mean → average rises; Value < Mean → average falls |

---

## Memory Aids

- **"Multiply, then subtract"** — the two-step mantra for every missing-value problem
- **"Total = Average × Count"** — say this before every problem; it's your starting move
- **"The missing piece fills the gap"** — Required Total minus What You Have = What's Missing
- **"New minus Old = the newcomer"** — for added-member problems
- **"Old minus New = the leaver"** — for removed-member problems
- **"Never average averages"** — always compute weighted totals when combining groups
- **"Plug it back in"** — verify by recomputing the average with your answer included

---

## Mastery Checklist

After completing this lesson, you should be able to:

- ✅ Convert any given average into a total sum instantly
- ✅ Solve single missing-value problems in under 60 seconds
- ✅ Handle multiple missing values when relationships are given
- ✅ Solve added-member and removed-member problems correctly
- ✅ Compute combined averages using weighted totals (not averaging averages)
- ✅ Identify and correct errors in recorded averages
- ✅ Predict whether adding/removing a value will raise or lower the average
- ✅ Interpret missing-value problems in real-life contexts (grades, salaries, budgets, production)
- ✅ Estimate answers mentally before computing to catch errors
- ✅ Solve CSE-style missing-average questions confidently under time pressure
