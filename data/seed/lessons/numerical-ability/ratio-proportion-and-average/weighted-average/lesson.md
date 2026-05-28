# Weighted Average

## Explanations

### Introduction

A **weighted average** is a type of mean where each value in a data set is multiplied by a predetermined weight that reflects its relative importance before the products are summed and divided by the total of all weights. Unlike a simple (arithmetic) average — where every value contributes equally — a weighted average acknowledges that some values matter more than others in a given context.

Weighted averages are everywhere in professional and academic life:
- **Grades and GPA** — a final exam worth 60% of your grade affects your average far more than a quiz worth 10%
- **Salary analysis** — computing the average salary across departments of different sizes
- **Inventory costing** — determining the average cost per unit when batches were purchased at different prices and quantities
- **Surveys and statistics** — weighting responses by population size so that larger groups influence the result proportionally
- **Transportation** — computing average speed over segments of different distances
- **Finance** — calculating portfolio returns where each investment has a different allocation
- **Government statistics** — combining regional data where regions have different populations

In the Philippine Civil Service Examination, weighted-average problems appear because they test a candidate's ability to:
- Assign appropriate importance to different data points
- Perform multi-step arithmetic accurately
- Interpret real-world scenarios where equal treatment of values would produce misleading results

### Why Weighted Averages Differ from Simple Averages

A simple average treats all values equally: add them up, divide by the count. A weighted average treats values unequally based on assigned importance (weights). When all weights are equal, the weighted average reduces to the simple average — making the simple average a special case of the weighted average.

### Common Mistakes Examinees Make

1. **Using simple average when weights are given** — ignoring the weights entirely and just averaging the values
2. **Forgetting to divide by total weight** — multiplying values by weights but then dividing by the count of values instead of the sum of weights
3. **Misidentifying what the weights are** — confusing the values with the weights (e.g., treating scores as weights and weights as scores)
4. **Incorrect percentage-to-decimal conversion** — using 40 instead of 0.40 when weights are given as percentages
5. **Rounding too early** — rounding intermediate products before completing the computation
6. **Assuming weights must sum to 1 or 100%** — weights can be any positive numbers; only their relative proportions matter
7. **Arithmetic errors in multiplication** — especially with decimals and multi-digit numbers under time pressure

### Learning Objectives

After this lesson, you should be able to:
- Define weighted average correctly and explain when it is used instead of a simple average
- Distinguish between simple average and weighted average with concrete examples
- Identify weights and their corresponding values in any problem context
- Apply the weighted mean formula accurately with decimal, percentage, and whole-number weights
- Solve practical weighted-average problems involving grades, GPA, business, finance, and surveys
- Interpret weighted data logically and explain what the result means in context
- Find missing values (unknown scores or unknown weights) given a target weighted average
- Solve CSE-style weighted-average questions efficiently under time pressure

---

### 4.1 What Is a Weighted Average?
> 🤔 **Why does this work?** The principle behind this operation follows from the fundamental properties of arithmetic. Understanding the "why" — not just the "how" — lets you recognize when to apply this method in unfamiliar problem contexts on the CSE.


A **weighted average** (also called a **weighted mean**) is a calculation that takes into account the varying degrees of importance of the numbers in a data set. Each value is multiplied by a weight, and the sum of these products is divided by the sum of the weights.

#### The Core Idea

Imagine you have three exam scores: 80, 90, and 70. If all exams are equally important, the simple average is:

$$\frac{80 + 90 + 70}{3} = 80$$

But what if the third exam is a comprehensive final worth twice as much as each of the first two? Now the scores carry different importance:
- Exam 1: weight = 1
- Exam 2: weight = 1
- Exam 3: weight = 2

The weighted average becomes:

$$\frac{(80)(1) + (90)(1) + (70)(2)}{1 + 1 + 2} = \frac{80 + 90 + 140}{4} = \frac{310}{4} = 77.5$$

Notice the weighted average (77.5) is lower than the simple average (80) because the lowest score (70) carried the most weight.

#### The Formula

$$\text{Weighted Mean} = \frac{\sum (x \cdot w)}{\sum w} = \frac{x_1 w_1 + x_2 w_2 + \cdots + x_n w_n}{w_1 + w_2 + \cdots + w_n}$$

Where:
- $x_i$ = each individual value (score, price, measurement, etc.)
- $w_i$ = the weight assigned to that value (importance, frequency, quantity, percentage, etc.)
- $\sum w$ = the total of all weights

#### Why Some Values Contribute More

In real life, not all data points are created equal:
- A final exam tests comprehensive understanding — it *should* count more than a pop quiz
- A factory that produces 10,000 units affects the industry average more than one producing 50 units
- A city with 2 million residents should influence a national average more than a town of 5,000

The weighted average is a **"fair importance" system** — it ensures that the final result reflects the actual significance of each component.

#### Visual Interpretation: The Balance Point

Think of a weighted average as the balance point on a number line. Values with larger weights pull the average toward them more strongly, just as heavier objects on a seesaw pull the balance point toward their side.

- If a score of 90 has weight 3 and a score of 60 has weight 1, the weighted average will be much closer to 90 (specifically: 82.5) because 90 "pulls" three times harder.


> ⚠️ **Misconception:** "The formula always works the same way regardless of the problem context."

> **Why it fails:** CSE problems often present variations where the standard formula must be adapted. Blindly applying a memorized formula without checking the context leads to systematic errors.

> **Correct model:** Always read the problem to identify what type of relationship exists (direct, inverse, part-whole, etc.), then apply the appropriate formula. Verify your answer makes sense in the problem's context before selecting it.

---

### 4.2 Simple Average vs. Weighted Average

#### Simple (Arithmetic) Average

$$\text{Simple Average} = \frac{\text{Sum of all values}}{\text{Number of values}}$$

Every value contributes equally. If you have 5 quiz scores, each quiz contributes exactly 1/5 (20%) to the average.

#### Weighted Average

$$\text{Weighted Average} = \frac{\sum (x \cdot w)}{\sum w}$$

Values contribute proportionally to their assigned weights. A quiz worth 10% contributes far less than a final exam worth 50%.

#### Side-by-Side Comparison

| Feature | Simple Average | Weighted Average |
|---------|---------------|-----------------|
| Weight distribution | Equal for all values | Varies by importance |
| Formula denominator | Count of values | Sum of weights |
| When to use | All items equally important | Items have different importance |
| Special case | Weighted average where all weights = 1 | General case |
| Example | Average of 5 quiz scores (equal weight) | Final grade (quizzes 20%, midterm 30%, final 50%) |

#### Example: When They Give Different Results

A student has these scores:
- Quizzes: 95 (weight: 20%)
- Midterm: 80 (weight: 30%)
- Final Exam: 70 (weight: 50%)

**Simple average:** (95 + 80 + 70) ÷ 3 = 81.67

**Weighted average:** (95 × 0.20) + (80 × 0.30) + (70 × 0.50) = 19 + 24 + 35 = **78**

The weighted average is lower because the lowest score (70) carries the highest weight (50%). The simple average would mislead the student into thinking their performance is better than the grading system actually reflects.

#### When They Are Equal

If all weights are the same, the weighted average equals the simple average:
- Scores: 85, 90, 80 with weights 1, 1, 1
- Weighted: (85×1 + 90×1 + 80×1) ÷ (1+1+1) = 255 ÷ 3 = 85
- Simple: (85 + 90 + 80) ÷ 3 = 85 ✓


> ⚠️ **Misconception:** "If my computed answer is close to one of the choices, it must be right."

> **Why it fails:** The CSE deliberately includes distractors that result from common errors — using the wrong operation, misidentifying the proportion type, or reversing the ratio. A "close" answer could be the result of a systematic mistake that the test writers anticipated.

> **Correct model:** Verify your setup before computing. Check that you've identified the correct proportion type, set up the equation properly, and solved accurately. A wrong setup with correct arithmetic still produces a wrong answer — and the CSE will include that wrong answer among the choices.

---


### Check Your Understanding

**1.** What is the key concept from this section? → **Review the preceding content to recall the main principle**

**2.** How would you apply this concept to a practical problem? → **Identify the type of relationship, set up the correct equation, and solve step by step**

**3.** What common mistake should you avoid here? → **Check the Common Mistakes section — verify your answer doesn't fall into these traps**

---

### 4.3 Understanding Weights
> 🤔 **Why does this work?** When you follow this procedure, you're exploiting a mathematical invariant — something that stays constant regardless of how you manipulate the numbers. Identifying that invariant is the key to solving problems efficiently rather than memorizing steps.


#### What Are Weights?

Weights are numbers that represent the **relative importance** or **frequency** of each value in a data set. They tell you "how much this value should count" in the final average.

Weights can be expressed as:
- **Percentages:** 20%, 30%, 50% (must sum to 100% for a complete system)
- **Decimals:** 0.20, 0.30, 0.50 (must sum to 1.0 for a complete system)
- **Whole numbers:** 2, 3, 5 (represent relative importance or actual counts/quantities)
- **Fractions:** 1/5, 3/10, 1/2

#### Identifying Weights in Problems

Look for these clue words:
- "worth," "counts for," "accounts for" → percentage weights
- "units," "items," "students," "hours" → frequency/quantity weights
- "importance," "credit hours," "multiplier" → relative importance weights

**Example clues:**
- "The quiz is worth 30% of the grade" → weight = 0.30
- "She worked 20 hours at ₱150/hr and 15 hours at ₱200/hr" → weights are 20 and 15 (hours)
- "Course A is 3 credit hours, Course B is 4 credit hours" → weights are 3 and 4

#### Why Larger Weights Dominate

A weight of 5 means that value is counted 5 times, while a weight of 1 means it is counted once. The value with weight 5 has five times the "pull" on the final average.

**Example:**
- Value A = 100, weight = 1
- Value B = 50, weight = 9

Weighted average = (100×1 + 50×9) ÷ (1+9) = (100 + 450) ÷ 10 = 55

Even though 100 is much larger than 50, the average is only 55 — very close to 50 — because 50 has nine times the weight.

#### Weights Do Not Need to Sum to 1 or 100

A common misconception is that weights must add up to 1 (or 100%). They don't. What matters is their **relative proportion**.

These three sets of weights produce the same weighted average:
- Weights: 1, 2, 3 (sum = 6)
- Weights: 2, 4, 6 (sum = 12)
- Weights: 10%, 20%, 30% → but only if you divide by 60% (the actual sum), not 100%

However, in grading systems, weights typically do sum to 100% because they represent the complete breakdown of a course grade.

---

### 4.4 Computing Weighted Averages

#### Step-by-Step Procedure

1. **Identify the values** ($x$) and their corresponding **weights** ($w$)
2. **Multiply** each value by its weight: compute $x_i \times w_i$ for each pair
3. **Sum** all the weighted products: $\sum (x \cdot w)$
4. **Sum** all the weights: $\sum w$
5. **Divide** the total weighted product by the total weight: $\frac{\sum (x \cdot w)}{\sum w}$

#### Example with Percentage Weights

A student's grade breakdown:
- Attendance: 85, weight = 10%
- Quizzes: 78, weight = 20%
- Project: 92, weight = 30%
- Final Exam: 88, weight = 40%

**Step 1:** Convert percentages to decimals: 0.10, 0.20, 0.30, 0.40

**Step 2:** Multiply each score by its weight:
- 85 × 0.10 = 8.5
- 78 × 0.20 = 15.6
- 92 × 0.30 = 27.6
- 88 × 0.40 = 35.2

**Step 3:** Sum the products: 8.5 + 15.6 + 27.6 + 35.2 = 86.9

**Step 4:** Sum the weights: 0.10 + 0.20 + 0.30 + 0.40 = 1.00

**Step 5:** Divide: 86.9 ÷ 1.00 = **86.9**

The student's weighted average grade is **86.9**.

#### Example with Whole-Number Weights

A company buys supplies in three batches:
- Batch 1: 100 units at ₱45 each
- Batch 2: 250 units at ₱40 each
- Batch 3: 150 units at ₱50 each

What is the weighted average cost per unit?

Here, the **values** are the prices (₱45, ₱40, ₱50) and the **weights** are the quantities (100, 250, 150).

$$\frac{(45)(100) + (40)(250) + (50)(150)}{100 + 250 + 150} = \frac{4500 + 10000 + 7500}{500} = \frac{22000}{500} = ₱44$$

The weighted average cost is ₱44 per unit — pulled toward ₱40 because that batch had the most units.

#### Example with Decimal Weights

An employee's performance rating is based on:
- Productivity: 4.2 out of 5 (weight: 0.50)
- Teamwork: 3.8 out of 5 (weight: 0.30)
- Punctuality: 4.5 out of 5 (weight: 0.20)

$$\frac{(4.2)(0.50) + (3.8)(0.30) + (4.5)(0.20)}{0.50 + 0.30 + 0.20} = \frac{2.10 + 1.14 + 0.90}{1.00} = \frac{4.14}{1.00} = 4.14$$

#### Verification Check

After computing a weighted average, verify that your answer falls **between the smallest and largest values** in the data set. If it doesn't, you made an error.

In the batch example: the answer (₱44) is between ₱40 and ₱50 ✓

---

### 4.5 Weighted Average in Grades and GPA
> 🤔 **Why does this work?** This shortcut works because it's a special case of the more general rule. By understanding the underlying principle, you can verify your answer logically even if you forget the exact formula under exam pressure.


#### Percentage-Based Grading

Most Philippine schools use percentage-based grading where components have different weights:

| Component | Score | Weight |
|-----------|-------|--------|
| Quizzes | 88 | 25% |
| Assignments | 92 | 15% |
| Midterm Exam | 79 | 25% |
| Final Exam | 84 | 35% |

Weighted average = (88×0.25) + (92×0.15) + (79×0.25) + (84×0.35)
= 22 + 13.8 + 19.75 + 29.4 = **84.95**

#### GPA (Grade Point Average) with Credit Hours

In college, courses have different credit hours (units). A 5-unit course affects your GPA more than a 2-unit course.

| Course | Grade | Credit Hours |
|--------|-------|-------------|
| Math | 1.25 | 5 |
| English | 1.50 | 3 |
| History | 2.00 | 3 |
| PE | 1.00 | 2 |

GPA = $\frac{(1.25)(5) + (1.50)(3) + (2.00)(3) + (1.00)(2)}{5 + 3 + 3 + 2}$

= $\frac{6.25 + 4.50 + 6.00 + 2.00}{13} = \frac{18.75}{13} = 1.44$

The GPA is 1.44 — pulled toward the Math grade because Math has the most credit hours.

#### Why Major Exams Carry More Weight

A final exam tests cumulative understanding of an entire semester's material. A single quiz tests one lesson. It would be unfair to let a 10-minute quiz count as much as a 3-hour comprehensive exam. Weighted grading ensures that assessments measuring deeper, broader knowledge have proportionally greater influence on the final grade.

---

### 4.6 Weighted Average in Business and Finance

#### Inventory Costing (Weighted Average Method)

Businesses that buy inventory at different prices use weighted averages to determine the cost of goods sold.

A store purchases rice:
- January: 200 sacks at ₱1,800 each
- March: 350 sacks at ₱1,950 each
- June: 150 sacks at ₱2,100 each

Weighted average cost = $\frac{(1800)(200) + (1950)(350) + (2100)(150)}{200 + 350 + 150}$

= $\frac{360000 + 682500 + 315000}{700} = \frac{1357500}{700} = ₱1,939.29$

#### Weighted Average Salary

A government agency has employees across pay grades:
- 40 employees earning ₱25,000/month
- 25 employees earning ₱35,000/month
- 10 employees earning ₱55,000/month

Average salary = $\frac{(25000)(40) + (35000)(25) + (55000)(10)}{40 + 25 + 10}$

= $\frac{1000000 + 875000 + 550000}{75} = \frac{2425000}{75} = ₱32,333.33$

The simple average of the three salaries would be (25000+35000+55000)÷3 = ₱38,333.33 — significantly higher and misleading because it ignores that most employees are in the lowest pay grade.

#### Investment Portfolio Returns

An investor allocates funds:
- 60% in bonds returning 5%
- 30% in stocks returning 12%
- 10% in real estate returning 8%

Weighted return = (5×0.60) + (12×0.30) + (8×0.10) = 3.0 + 3.6 + 0.8 = **7.4%**

---

### 4.7 Weighted Average in Statistics and Surveys

#### Population Weighting

When computing a national average from regional data, each region must be weighted by its population.

| Region | Average Income | Population |
|--------|---------------|-----------|
| NCR | ₱45,000 | 13,000,000 |
| Region IV-A | ₱28,000 | 16,000,000 |
| Region VII | ₱22,000 | 8,000,000 |

National weighted average = $\frac{(45000)(13) + (28000)(16) + (22000)(8)}{13 + 16 + 8}$ (in millions)

= $\frac{585000 + 448000 + 176000}{37} = \frac{1209000}{37} = ₱32,675.68$

A simple average of the three incomes (₱31,666.67) would underweight NCR's high income and overweight Region VII's lower income relative to their actual populations.

#### Survey Weighting

If a survey samples 500 people from a city of 2 million and 500 people from a town of 50,000, the raw average of responses would overrepresent the small town. Weighting by population corrects this bias.

#### Grouped Data

When data is presented in frequency tables (e.g., "30 students scored 80–89, 15 students scored 90–99"), the midpoint of each class interval is the value and the frequency is the weight.

---

### 4.8 Finding Missing Values in Weighted Averages

This is a common CSE question type: given a target weighted average and some known values, find the unknown.

#### Type 1: Finding a Missing Score

A student needs a weighted average of 85. The grading system is:
- Quiz: 80 (weight 30%)
- Project: 90 (weight 20%)
- Final Exam: ? (weight 50%)

Set up the equation:

$$\frac{(80)(0.30) + (90)(0.20) + (x)(0.50)}{1.00} = 85$$

$$24 + 18 + 0.50x = 85$$

$$0.50x = 85 - 42 = 43$$

$$x = 86$$

The student needs **86** on the final exam.

#### Type 2: Finding a Missing Weight

A teacher assigns weights to three components. Quizzes (score: 88) have weight 2, the midterm (score: 76) has weight 3, and the final exam (score: 92) has an unknown weight $w$. The overall weighted average is 85. Find $w$.

$$\frac{(88)(2) + (76)(3) + (92)(w)}{2 + 3 + w} = 85$$

$$\frac{176 + 228 + 92w}{5 + w} = 85$$

$$404 + 92w = 85(5 + w)$$

$$404 + 92w = 425 + 85w$$

$$7w = 21$$

$$w = 3$$

#### Type 3: Target Average Problems

"What minimum score does a student need on the final exam (worth 40%) to achieve an overall average of at least 80, given quiz average = 75 (worth 25%) and midterm = 82 (worth 35%)?"

$$\frac{(75)(0.25) + (82)(0.35) + (x)(0.40)}{1.00} \geq 80$$

$$18.75 + 28.7 + 0.40x \geq 80$$

$$0.40x \geq 32.55$$

$$x \geq 81.375$$

The student needs at least **82** (rounding up to the nearest whole number).

#### Verification Strategy

After finding the missing value, plug it back into the original formula and confirm the weighted average matches the target.

---

### 4.9 Using Tables and Organized Computation

#### Why Tables Help

Weighted-average problems involve multiple multiplications and a final division. Organizing data in a table prevents errors:

| Component | Value (x) | Weight (w) | Product (x × w) |
|-----------|-----------|-----------|-----------------|
| Quiz | 85 | 0.20 | 17.0 |
| Midterm | 78 | 0.30 | 23.4 |
| Final | 90 | 0.50 | 45.0 |
| **Total** | | **1.00** | **85.4** |

Weighted Average = 85.4 ÷ 1.00 = **85.4**

#### Recognizing Weighted Contributions

From the table above, you can see that the Final Exam contributes 45.0 out of 85.4 total "points" — over half the weighted average comes from one component. This visual breakdown helps you understand which component drives the result.

#### Comparison Charts

When comparing two students or two scenarios, side-by-side tables make differences immediately visible:

| Component | Weight | Student A Score | A's Product | Student B Score | B's Product |
|-----------|--------|----------------|-------------|----------------|-------------|
| Quiz | 0.30 | 90 | 27.0 | 75 | 22.5 |
| Exam | 0.70 | 80 | 56.0 | 88 | 61.6 |
| **Total** | **1.00** | | **83.0** | | **84.1** |

Student B has a higher weighted average despite a lower quiz score because the exam (where B excels) carries more weight.

---

### 4.10 Problem-Solving Strategies

#### Strategy 1: Identify Values and Weights First

Before computing anything, clearly label:
- What are the **values** (scores, prices, rates)?
- What are the **weights** (percentages, quantities, hours, credit units)?

#### Strategy 2: Check That Weights Are Consistent

If weights are percentages, they should sum to 100% (or the problem should specify that only partial weights are given). If they're quantities, just sum them for the denominator.

#### Strategy 3: Estimate Before Computing

Before doing exact arithmetic, estimate:
- The weighted average must fall between the minimum and maximum values
- It will be closer to the value with the largest weight

If scores are 70, 80, 90 with weights 10%, 20%, 70%, the answer must be between 70 and 90, and closer to 90. Quick estimate: around 85. (Exact: 84)

#### Strategy 4: Use Elimination on Multiple Choice

If you estimate the weighted average is around 85, and the choices are 78, 82, 84, 90 — you can likely eliminate 78 and 90 immediately, then compute more carefully between 82 and 84.

#### Strategy 5: Simplify Weights When Possible

Weights of 20%, 30%, 50% can be thought of as 2:3:5 (multiply by 10). This avoids decimal multiplication:

$$\frac{(85)(2) + (78)(3) + (90)(5)}{2 + 3 + 5} = \frac{170 + 234 + 450}{10} = \frac{854}{10} = 85.4$$

---

### 4.11 Estimation and Mental Math Techniques

#### Technique 1: Anchor to the Dominant Weight

Find the value with the largest weight. The weighted average will be close to that value. Then adjust for the other values.

**Example:** Scores 92, 75, 80 with weights 60%, 25%, 15%.
- Anchor: 92 (weight 60%) → start estimate at 92
- The other scores (75, 80) are lower, so the average will be pulled down
- Rough adjustment: about 7–10 points down → estimate ~84
- Exact: (92×0.60)+(75×0.25)+(80×0.15) = 55.2+18.75+12 = 85.95

#### Technique 2: Deviation Method

Choose a reference value (often the middle value or the value with the highest weight). Compute deviations from it, weight the deviations, and add to the reference.

**Example:** Values 80, 85, 90 with weights 3, 5, 2. Reference = 85.
- Deviations: 80−85=−5, 85−85=0, 90−85=+5
- Weighted deviations: (−5)(3)+(0)(5)+(5)(2) = −15+0+10 = −5
- Total weight: 10
- Adjustment: −5÷10 = −0.5
- Weighted average: 85 + (−0.5) = **84.5**

This is faster when values are close together.

#### Technique 3: Grouping Compatible Numbers

When multiplying mentally, group numbers that produce round products:
- 25 × 4 = 100
- 50 × 2 = 100
- 75 × 4 = 300

Look for these patterns to speed up computation.

---

### 4.12 Common Errors in Weighted-Average Problems

| Error | What Goes Wrong | How to Avoid |
|-------|----------------|-------------|
| Ignoring weights | Computing (80+90+70)÷3 when weights are given | Always check if weights are specified |
| Wrong denominator | Dividing by count of values instead of sum of weights | Write $\sum w$ explicitly |
| Swapped values/weights | Multiplying weight × weight or value × value | Label clearly: which column is x? which is w? |
| Percentage confusion | Using 40 instead of 0.40 | Convert all percentages to decimals first |
| Premature rounding | Rounding 23.6 to 24 before adding other products | Keep full precision until the final step |
| Answer outside range | Getting 95 when all values are between 70 and 90 | Verify: min ≤ answer ≤ max |
| Incomplete weights | Using only some components and ignoring others | Ensure all components are included |

---

## Step-by-Step Rules Summary

### Computing a Weighted Average
1. List all values and their weights in a table
2. Convert percentage weights to decimals if needed
3. Multiply each value by its weight
4. Sum all products
5. Sum all weights
6. Divide total products by total weights
7. Verify the answer is between the minimum and maximum values

### Finding a Missing Value
1. Set up the weighted average equation with the unknown as $x$
2. Multiply known values by their weights
3. Express the unknown term as $x \times w$
4. Set the equation equal to the target average (times total weight)
5. Solve for $x$
6. Verify by substituting back

### Finding a Missing Weight
1. Set up the equation with unknown weight $w$
2. Cross-multiply to eliminate the fraction
3. Expand and collect terms with $w$
4. Solve for $w$
5. Verify the answer is positive and reasonable

---

## Exam Strategies for CSE

1. **Read the problem twice** — identify values and weights before touching your pencil
2. **Set up a mini-table** on scratch paper — prevents mixing up numbers
3. **Estimate first** — know the ballpark before computing
4. **Convert percentages immediately** — 30% → 0.30 to avoid errors
5. **Check your denominator** — the most common error is dividing by the wrong number
6. **Use elimination** — if your estimate says ~85, cross out choices far from 85
7. **Verify at the end** — plug your answer back in if time permits
8. **Watch for "at least" language** — these require rounding up, not down

---

## Real CSE-Like Examples

### Easy Example 1

**Problem:** A student's grade is computed as: Quizzes (40%) and Final Exam (60%). If the quiz average is 80 and the final exam score is 90, what is the weighted average?

**Solution:**
- (80 × 0.40) + (90 × 0.60) = 32 + 54 = **86**

### Easy Example 2

**Problem:** A store sells 200 items at ₱50 each and 300 items at ₱70 each. What is the average selling price per item?

**Solution:**
- (50 × 200 + 70 × 300) ÷ (200 + 300) = (10000 + 21000) ÷ 500 = 31000 ÷ 500 = **₱62**

### Medium Example 1

**Problem:** An employee's performance rating uses: Productivity (50%), Quality (30%), Attendance (20%). Scores are 88, 92, and 75 respectively. What is the overall rating?

**Solution:**
- (88 × 0.50) + (92 × 0.30) + (75 × 0.20) = 44 + 27.6 + 15 = **86.6**

### Medium Example 2

**Problem:** A student needs a weighted average of at least 85. Quizzes (30%) = 82, Midterm (30%) = 80. What minimum score is needed on the Final Exam (40%)?

**Solution:**
- (82 × 0.30) + (80 × 0.30) + (x × 0.40) = 85
- 24.6 + 24 + 0.40x = 85
- 0.40x = 36.4
- x = **91**

### Hard Example 1

**Problem:** Three sections took the same test. Section A (35 students) averaged 78, Section B (28 students) averaged 84, Section C (17 students) averaged 91. What is the overall average for all students?

**Solution:**
- (78×35 + 84×28 + 91×17) ÷ (35+28+17)
- (2730 + 2352 + 1547) ÷ 80
- 6629 ÷ 80 = **82.86**

### Hard Example 2

**Problem:** A company has three products. Product X costs ₱120 (weight unknown), Product Y costs ₱85 (weight 4), Product Z costs ₱150 (weight 2). If the weighted average cost is ₱110, find the weight of Product X.

**Solution:**
- (120w + 85×4 + 150×2) ÷ (w + 4 + 2) = 110
- (120w + 340 + 300) ÷ (w + 6) = 110
- 120w + 640 = 110w + 660
- 10w = 20
- w = **2**

---

## Mini Practice Set (20 Questions)

**1.** A grade is 30% quizzes (score: 76) and 70% exam (score: 88). What is the weighted average?
**Answer:** (76×0.30)+(88×0.70) = 22.8+61.6 = **84.4**

**2.** A factory produces 400 units at ₱25 and 600 units at ₱30. What is the average cost per unit?
**Answer:** (25×400+30×600)÷1000 = (10000+18000)÷1000 = **₱28**

**3.** Three tests with weights 1, 2, 3 have scores 90, 80, 70. Find the weighted average.
**Answer:** (90×1+80×2+70×3)÷6 = (90+160+210)÷6 = 460÷6 = **76.67**

**4.** A student scored 85 (weight 40%) and 95 (weight 60%). What is the weighted average?
**Answer:** (85×0.40)+(95×0.60) = 34+57 = **91**

**5.** Compute the weighted average: values 60, 70, 80 with weights 5, 3, 2.
**Answer:** (60×5+70×3+80×2)÷10 = (300+210+160)÷10 = 670÷10 = **67**

**6.** A worker earns ₱500/hr for 6 hours and ₱700/hr for 4 hours. What is the average hourly rate?
**Answer:** (500×6+700×4)÷10 = (3000+2800)÷10 = 5800÷10 = **₱580**

**7.** Course grades: Math=1.5 (5 units), English=2.0 (3 units), Science=1.75 (4 units). Find GPA.
**Answer:** (1.5×5+2.0×3+1.75×4)÷12 = (7.5+6+7)÷12 = 20.5÷12 = **1.71**

**8.** A survey: Group A (200 people) rates 4.2, Group B (800 people) rates 3.6. Weighted average rating?
**Answer:** (4.2×200+3.6×800)÷1000 = (840+2880)÷1000 = 3720÷1000 = **3.72**

**9.** Scores: 88 (weight 25%), 76 (weight 25%), 94 (weight 50%). Weighted average?
**Answer:** (88×0.25)+(76×0.25)+(94×0.50) = 22+19+47 = **88**

**10.** A student needs 80 weighted average. Quiz=72 (20%), Midterm=78 (30%), Final=? (50%). Find Final.
**Answer:** 14.4+23.4+0.50x=80 → 0.50x=42.2 → x=**84.4**

**11.** Products: A=₱150 (qty 30), B=₱200 (qty 20), C=₱100 (qty 50). Average price per unit?
**Answer:** (150×30+200×20+100×50)÷100 = (4500+4000+5000)÷100 = **₱135**

**12.** Weights 2, 3, 5 with values 100, 80, 60. Weighted average?
**Answer:** (100×2+80×3+60×5)÷10 = (200+240+300)÷10 = 740÷10 = **74**

**13.** A class of 20 students averages 82; another class of 30 students averages 88. Combined average?
**Answer:** (82×20+88×30)÷50 = (1640+2640)÷50 = 4280÷50 = **85.6**

**14.** Rating components: Speed=90 (15%), Accuracy=85 (45%), Teamwork=80 (40%). Overall?
**Answer:** (90×0.15)+(85×0.45)+(80×0.40) = 13.5+38.25+32 = **83.75**

**15.** A driver travels 120 km at 60 km/h and 80 km at 40 km/h. What is the average speed?
**Answer:** Total distance=200, Total time=120/60+80/40=2+2=4 hrs. Average speed=200÷4=**50 km/h**
(Note: This is a harmonic-weighted problem, but if treated as weighted average of speeds by distance: (60×120+40×80)÷200=(7200+3200)÷200=52. The true average speed uses time, not distance.)

**16.** Investments: ₱100,000 at 6% return, ₱200,000 at 8% return. Weighted average return?
**Answer:** (6×100000+8×200000)÷300000 = (600000+1600000)÷300000 = 2200000÷300000 = **7.33%**

**17.** Exam breakdown: Written=78 (weight 3), Practical=92 (weight 2). Weighted average?
**Answer:** (78×3+92×2)÷5 = (234+184)÷5 = 418÷5 = **83.6**

**18.** A student's weighted average is 87. Quiz=90 (30%), Project=x (20%), Exam=85 (50%). Find x.
**Answer:** (90×0.30)+(x×0.20)+(85×0.50)=87 → 27+0.20x+42.5=87 → 0.20x=17.5 → x=**87.5**

**19.** Three departments: Dept A (50 staff, avg age 32), Dept B (30 staff, avg age 45), Dept C (20 staff, avg age 28). Company average age?
**Answer:** (32×50+45×30+28×20)÷100 = (1600+1350+560)÷100 = 3510÷100 = **35.1**

**20.** Weighted average of 72, 84, 96 with weights 1:2:1?
**Answer:** (72×1+84×2+96×1)÷4 = (72+168+96)÷4 = 336÷4 = **84**

---

## Quick Recap

| Concept | Key Point |
|---------|-----------|
| Weighted Average | Mean where values are multiplied by importance weights before averaging |
| Formula | $\frac{\sum(x \cdot w)}{\sum w}$ |
| Weights | Numbers representing relative importance (%, decimals, or whole numbers) |
| vs. Simple Average | Simple average = weighted average with all weights equal |
| Range Check | Answer must fall between minimum and maximum values |
| Missing Values | Set up equation, substitute knowns, solve for unknown |
| Applications | Grades, GPA, inventory, salary, surveys, finance, statistics |

---

## Memory Aids

1. **"Multiply then Divide"** — Always multiply each value by its weight first, THEN divide by total weight
2. **"Heavier pulls harder"** — The value with the biggest weight pulls the average toward itself
3. **"Between the extremes"** — Your answer must be between the smallest and largest values
4. **"Weights are the WHY"** — Weights tell you WHY some values matter more
5. **"Percent means per-hundred"** — 40% = 0.40, always convert before multiplying
6. **"Sum the bottom"** — The denominator is the sum of WEIGHTS, not the count of values

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

- **Introduction to Average:** Weighted average generalizes simple average — when all weights are equal, they produce the same result
- **Basic Percentage Problems:** Weights are often expressed as percentages — computing weighted averages requires percentage arithmetic
- **Finding Missing Values in Averages:** The weighted average formula can be rearranged to find missing weights or values
- **Proportion Word Problems:** Weighted averages use proportional reasoning — each component contributes proportionally to the total

### Mastery Checklist
After completing this lesson, you should be able to:

- ✅ Define weighted average correctly and explain its purpose
- ✅ Distinguish weighted average from simple average with examples
- ✅ Identify weights and values in any problem context
- ✅ Compute weighted averages with percentage, decimal, and whole-number weights
- ✅ Solve missing-value problems (find unknown score or weight)
- ✅ Interpret weighted data and explain what drives the result
- ✅ Apply weighted averages to grades, GPA, business, finance, and surveys
- ✅ Estimate weighted averages mentally for quick elimination
- ✅ Verify answers using the range check and substitution
- ✅ Solve CSE-style weighted-average questions confidently under time pressure

> 🤔 **Why does this work?** Weighted average accounts for the fact that not all data points contribute equally to the total. A simple average assumes equal weights (each item counts once), but when groups have different sizes, each group's average must be scaled by its proportion of the total. Mathematically, weighted average = Σ(value × weight) / Σ(weights), which reduces to simple average when all weights are equal.


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
- **Introduction To Average**: Reinforces this topic through a closely related reasoning pattern.
