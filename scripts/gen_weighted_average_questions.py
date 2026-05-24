"""
Generate 600 multiple-choice questions for Weighted Average.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/numerical-ability/ratio-proportion-and-average/weighted-average/questions.json
"""

import json
import random
import math
import os
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path("data/seed/questions/numerical-ability/ratio-proportion-and-average/weighted-average")
OUTPUT_FILE = OUTPUT_DIR / "questions.json"

SUBTEST = "Numerical Ability"
MODULE = "Ratio, Proportion, and Average"
SUBTOPIC = "Weighted Average"
CATEGORIES = ["Professional", "Sub-Professional"]
LANGUAGE = "English"


def round2(x):
    """Round to 2 decimal places."""
    return round(x, 2)


def fmt(x):
    """Format number: remove trailing zeros for clean display."""
    if x == int(x):
        return str(int(x))
    return f"{x:.2f}".rstrip("0").rstrip(".")


def weighted_avg(values, weights):
    """Compute weighted average."""
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)


def generate_distractors_numeric(correct, count=3, spread=None):
    """Generate plausible numeric distractors."""
    if spread is None:
        spread = max(3, abs(correct) * 0.08)
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        attempts += 1
        strategy = random.choice(["offset", "swap_digit", "near", "arithmetic_error"])
        if strategy == "offset":
            offset = random.choice([-3, -2, -1, 1, 2, 3, 4, 5, -4, -5])
            d = round2(correct + offset)
        elif strategy == "swap_digit":
            d = round2(correct + random.uniform(-spread, spread))
        elif strategy == "near":
            d = round2(correct + random.choice([-1.5, -0.5, 0.5, 1.5, 2.5, -2.5]))
        else:
            d = round2(correct + random.choice([2, -2, 3, -3, 4, -4, 5, -5, 6, -6]))
        if d != round2(correct) and d > 0:
            distractors.add(d)
    result = list(distractors)[:count]
    # Fill if not enough
    fill_val = 1
    while len(result) < count:
        candidate = round2(correct + fill_val)
        if candidate != round2(correct) and candidate > 0 and candidate not in result:
            result.append(candidate)
        fill_val += 1
    return result


def make_choices(correct_str, distractors_str):
    """Shuffle correct answer among distractors."""
    choices = [correct_str] + list(distractors_str)
    random.shuffle(choices)
    return choices


# ============================================================
# EASY QUESTION GENERATORS (200 questions)
# ============================================================

def gen_easy_questions():
    questions = []

    # Type 1: Basic two-component weighted average with percentage weights (51 questions)
    subjects_pairs = [
        ("quizzes", "final exam"), ("homework", "test"), ("attendance", "exam"),
        ("classwork", "project"), ("oral recitation", "written exam"),
        ("participation", "major exam"), ("seatwork", "long test"),
        ("assignment", "periodical exam"), ("lab work", "lecture exam"),
        ("recitation", "final output"),
    ]
    for i in range(51):
        w1 = random.choice([20, 25, 30, 35, 40])
        w2 = 100 - w1
        s1 = random.randint(70, 98)
        s2 = random.randint(70, 98)
        correct = round2(s1 * (w1 / 100) + s2 * (w2 / 100))
        pair = subjects_pairs[i % len(subjects_pairs)]
        question_text = (
            f"A student's grade is computed as {pair[0]} ({w1}%) and {pair[1]} ({w2}%). "
            f"If the {pair[0]} score is {s1} and the {pair[1]} score is {s2}, "
            f"what is the weighted average?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        # Ensure no duplicates
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=5)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({s1} × {w1/100:.2f}) + ({s2} × {w2/100:.2f}) "
                f"= {fmt(round2(s1*w1/100))} + {fmt(round2(s2*w2/100))} = {correct_str}."
            ),
            "tags": ["weighted average", "grades", "percentage weights"],
        })

    # Type 2: Average price with two batches (50 questions)
    items_list = [
        "notebooks", "pens", "folders", "binders", "markers",
        "erasers", "rulers", "calculators", "USB drives", "mouse pads",
    ]
    for i in range(50):
        q1 = random.choice([50, 100, 150, 200, 250, 300, 400, 500])
        q2 = random.choice([50, 100, 150, 200, 250, 300, 400, 500])
        p1 = random.randint(10, 80) * 5  # prices in multiples of 5
        p2 = random.randint(10, 80) * 5
        while p1 == p2:
            p2 = random.randint(10, 80) * 5
        correct = round2((p1 * q1 + p2 * q2) / (q1 + q2))
        item = items_list[i % len(items_list)]
        question_text = (
            f"A store buys {q1} {item} at ₱{p1} each and {q2} {item} at ₱{p2} each. "
            f"What is the average cost per {item[:-1] if item.endswith('s') else item}?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=6)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": f"₱{correct_str}",
            "choices": make_choices(f"₱{correct_str}", [f"₱{d}" for d in dist_str]),
            "explanation": (
                f"Weighted average = ({p1} × {q1} + {p2} × {q2}) ÷ ({q1} + {q2}) "
                f"= {p1*q1} + {p2*q2}) ÷ {q1+q2} = {p1*q1+p2*q2} ÷ {q1+q2} = ₱{correct_str}."
            ),
            "tags": ["weighted average", "pricing", "inventory"],
        })

    # Type 3: Simple whole-number weights with two values (50 questions)
    contexts = [
        ("Section A", "Section B", "students", "average score"),
        ("Group 1", "Group 2", "members", "average rating"),
        ("Morning shift", "Afternoon shift", "workers", "average output"),
        ("Branch X", "Branch Y", "employees", "average salary (in thousands)"),
        ("Class 1", "Class 2", "pupils", "average grade"),
    ]
    for i in range(50):
        ctx = contexts[i % len(contexts)]
        n1 = random.randint(10, 50)
        n2 = random.randint(10, 50)
        v1 = random.randint(70, 95)
        v2 = random.randint(70, 95)
        while v1 == v2:
            v2 = random.randint(70, 95)
        correct = round2((v1 * n1 + v2 * n2) / (n1 + n2))
        question_text = (
            f"{ctx[0]} has {n1} {ctx[2]} with an {ctx[3]} of {v1}. "
            f"{ctx[1]} has {n2} {ctx[2]} with an {ctx[3]} of {v2}. "
            f"What is the combined {ctx[3]}?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=4)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({v1} × {n1} + {v2} × {n2}) ÷ ({n1} + {n2}) "
                f"= ({v1*n1} + {v2*n2}) ÷ {n1+n2} = {v1*n1+v2*n2} ÷ {n1+n2} = {correct_str}."
            ),
            "tags": ["weighted average", "combined average", "groups"],
        })

    # Type 4: Three-component equal-style weights (25 questions)
    for i in range(25):
        w1, w2, w3 = random.choice([
            (1, 2, 2), (1, 1, 3), (2, 2, 1), (1, 3, 1), (2, 1, 2),
            (3, 2, 1), (1, 2, 3), (2, 3, 1), (3, 1, 2), (1, 1, 2),
        ])
        v1 = random.randint(65, 98)
        v2 = random.randint(65, 98)
        v3 = random.randint(65, 98)
        total_w = w1 + w2 + w3
        correct = round2((v1*w1 + v2*w2 + v3*w3) / total_w)
        question_text = (
            f"Three test scores are {v1}, {v2}, and {v3} with weights {w1}, {w2}, and {w3} respectively. "
            f"What is the weighted average?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=5)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({v1}×{w1} + {v2}×{w2} + {v3}×{w3}) ÷ ({w1}+{w2}+{w3}) "
                f"= ({v1*w1} + {v2*w2} + {v3*w3}) ÷ {total_w} = {v1*w1+v2*w2+v3*w3} ÷ {total_w} = {correct_str}."
            ),
            "tags": ["weighted average", "whole-number weights", "computation"],
        })

    # Type 5: Conceptual / definition questions (25 questions)
    conceptual = [
        {
            "question": "What does a weighted average take into account that a simple average does not?",
            "choices": ["The relative importance of each value", "The number of decimal places", "The order of values", "The range of the data"],
            "answer": "The relative importance of each value",
            "explanation": "A weighted average multiplies each value by a weight representing its importance, unlike a simple average which treats all values equally.",
            "tags": ["weighted average", "definition", "concept"],
        },
        {
            "question": "In the weighted mean formula, what does the denominator represent?",
            "choices": ["The sum of all weights", "The number of values", "The largest weight", "The product of all weights"],
            "answer": "The sum of all weights",
            "explanation": "The weighted mean formula divides the sum of (value × weight) products by the sum of all weights, not the count of values.",
            "tags": ["weighted average", "formula", "concept"],
        },
        {
            "question": "If all weights in a weighted average are equal, the result is the same as:",
            "choices": ["The simple arithmetic average", "The median", "The mode", "The geometric mean"],
            "answer": "The simple arithmetic average",
            "explanation": "When all weights are equal, the weighted average formula reduces to the simple average formula since equal weights cancel out.",
            "tags": ["weighted average", "simple average", "concept"],
        },
        {
            "question": "A final exam worth 60% of the grade will affect the weighted average:",
            "choices": ["More than a quiz worth 10%", "Less than a quiz worth 10%", "The same as a quiz worth 10%", "Cannot be determined"],
            "answer": "More than a quiz worth 10%",
            "explanation": "A component with a larger weight (60% vs 10%) has a greater influence on the weighted average.",
            "tags": ["weighted average", "weights", "concept"],
        },
        {
            "question": "The weighted average of a data set must always fall:",
            "choices": ["Between the smallest and largest values", "Above the largest value", "Below the smallest value", "Exactly at the midpoint"],
            "answer": "Between the smallest and largest values",
            "explanation": "A weighted average is always between the minimum and maximum values in the data set, regardless of the weights assigned.",
            "tags": ["weighted average", "range", "concept"],
        },
        {
            "question": "Which of the following is the correct weighted mean formula?",
            "choices": ["Sum of (value × weight) divided by sum of weights", "Sum of values divided by number of values", "Sum of weights divided by sum of values", "Product of all values divided by sum of weights"],
            "answer": "Sum of (value × weight) divided by sum of weights",
            "explanation": "The weighted mean = Σ(x·w) / Σw, where x represents values and w represents weights.",
            "tags": ["weighted average", "formula", "concept"],
        },
        {
            "question": "A student scored 95 on a quiz (weight 20%) and 75 on an exam (weight 80%). The weighted average will be closest to:",
            "choices": ["75", "95", "85", "90"],
            "answer": "75",
            "explanation": "Since the exam has 80% weight, the average is pulled strongly toward 75. Exact: (95×0.20)+(75×0.80) = 19+60 = 79, which is closest to 75 among the choices.",
            "tags": ["weighted average", "estimation", "concept"],
        },
        {
            "question": "What happens to the weighted average if you increase the weight of the highest value?",
            "choices": ["The weighted average increases", "The weighted average decreases", "The weighted average stays the same", "The weighted average becomes zero"],
            "answer": "The weighted average increases",
            "explanation": "Increasing the weight of the highest value pulls the average upward, since that value now contributes more to the total.",
            "tags": ["weighted average", "effect of weights", "concept"],
        },
        {
            "question": "In computing GPA, the 'weights' are typically:",
            "choices": ["Credit hours or units", "The number of students", "The professor's rating", "The room number"],
            "answer": "Credit hours or units",
            "explanation": "GPA is computed by weighting each course grade by its credit hours (units), so courses with more units affect the GPA more.",
            "tags": ["weighted average", "GPA", "concept"],
        },
        {
            "question": "If weights are given as 30%, 30%, and 40%, their sum is:",
            "choices": ["100%", "90%", "110%", "1"],
            "answer": "100%",
            "explanation": "30% + 30% + 40% = 100%. When percentage weights sum to 100%, the denominator in the weighted average formula equals 1 (after converting to decimals).",
            "tags": ["weighted average", "percentage weights", "concept"],
        },
        {
            "question": "Which scenario requires a weighted average instead of a simple average?",
            "choices": ["Computing a grade where quizzes are 30% and exams are 70%", "Finding the average of five equal quiz scores", "Computing the median of a data set", "Counting the number of items in a list"],
            "answer": "Computing a grade where quizzes are 30% and exams are 70%",
            "explanation": "When components have different importance (different percentages), a weighted average is needed. Equal quiz scores use a simple average.",
            "tags": ["weighted average", "application", "concept"],
        },
        {
            "question": "Converting 45% to a decimal weight gives:",
            "choices": ["0.45", "4.5", "45", "0.045"],
            "answer": "0.45",
            "explanation": "To convert a percentage to a decimal, divide by 100: 45% ÷ 100 = 0.45.",
            "tags": ["weighted average", "percentage conversion", "concept"],
        },
        {
            "question": "Weights of 2, 3, and 5 mean the third value is counted how many times more than the first?",
            "choices": ["2.5 times more", "3 times more", "5 times more", "Equally"],
            "answer": "2.5 times more",
            "explanation": "The third value has weight 5 and the first has weight 2. The ratio is 5÷2 = 2.5, so the third value counts 2.5 times more.",
            "tags": ["weighted average", "interpreting weights", "concept"],
        },
        {
            "question": "A weighted average of 82 means:",
            "choices": ["The overall performance considering all weights is 82", "Every component scored exactly 82", "The highest score is 82", "The lowest score is 82"],
            "answer": "The overall performance considering all weights is 82",
            "explanation": "A weighted average represents the overall result after accounting for the different importance of each component. Individual scores may be above or below 82.",
            "tags": ["weighted average", "interpretation", "concept"],
        },
        {
            "question": "If a quiz (weight 10%) score increases by 10 points, the weighted average increases by:",
            "choices": ["1 point", "10 points", "0.1 points", "5 points"],
            "answer": "1 point",
            "explanation": "The change in weighted average = change in score × weight = 10 × 0.10 = 1 point.",
            "tags": ["weighted average", "sensitivity", "concept"],
        },
        {
            "question": "Which is NOT a valid weight in a weighted average problem?",
            "choices": ["A negative number", "A percentage", "A whole number", "A decimal"],
            "answer": "A negative number",
            "explanation": "Weights must be positive numbers (or zero). Negative weights are not used in standard weighted average calculations.",
            "tags": ["weighted average", "valid weights", "concept"],
        },
        {
            "question": "The simple average of 60 and 90 is 75. If 90 has twice the weight of 60, the weighted average is:",
            "choices": ["80", "75", "70", "85"],
            "answer": "80",
            "explanation": "With weights 1 and 2: (60×1 + 90×2) ÷ (1+2) = (60+180) ÷ 3 = 240 ÷ 3 = 80.",
            "tags": ["weighted average", "comparison", "concept"],
        },
        {
            "question": "In a weighted average, 'Σ' (sigma) means:",
            "choices": ["Sum of", "Product of", "Average of", "Square root of"],
            "answer": "Sum of",
            "explanation": "The Greek letter Σ (sigma) represents summation — adding up all the terms that follow it.",
            "tags": ["weighted average", "notation", "concept"],
        },
        {
            "question": "A company buys 1000 items at ₱10 and 1 item at ₱10,000. The weighted average price is closest to:",
            "choices": ["₱10", "₱10,000", "₱5,005", "₱5,000"],
            "answer": "₱10",
            "explanation": "With 1000 items at ₱10 and only 1 at ₱10,000: (10×1000+10000×1)÷1001 = 20000÷1001 ≈ ₱19.98, which is closest to ₱10.",
            "tags": ["weighted average", "dominant weight", "concept"],
        },
        {
            "question": "When solving for a missing score in a weighted average problem, you should:",
            "choices": ["Set up an equation with the unknown and solve algebraically", "Guess and check all answer choices", "Use the simple average formula", "Ignore the weights"],
            "answer": "Set up an equation with the unknown and solve algebraically",
            "explanation": "To find a missing value, set up the weighted average equation with the unknown as a variable, then solve using algebra.",
            "tags": ["weighted average", "missing value", "strategy"],
        },
        {
            "question": "Weights in a grading system represent:",
            "choices": ["How much each component contributes to the final grade", "The maximum possible score", "The number of questions", "The passing score"],
            "answer": "How much each component contributes to the final grade",
            "explanation": "Weights indicate the proportion of the final grade that each component (quiz, exam, project) accounts for.",
            "tags": ["weighted average", "grading", "concept"],
        },
        {
            "question": "If three scores are 80, 80, and 80 with weights 1, 5, and 10, the weighted average is:",
            "choices": ["80", "85", "75", "90"],
            "answer": "80",
            "explanation": "When all values are the same, the weighted average equals that value regardless of weights: (80×1+80×5+80×10)÷16 = 1280÷16 = 80.",
            "tags": ["weighted average", "equal values", "concept"],
        },
        {
            "question": "The denominator in a weighted average with percentage weights that sum to 100% equals:",
            "choices": ["1 (when converted to decimals)", "100", "The number of components", "0"],
            "answer": "1 (when converted to decimals)",
            "explanation": "When percentage weights sum to 100%, converting to decimals gives a sum of 1.00, making the denominator 1.",
            "tags": ["weighted average", "denominator", "concept"],
        },
        {
            "question": "A weighted average is useful when:",
            "choices": ["Different data points have different levels of importance", "All data points are equally important", "You only have one data point", "You want to find the median"],
            "answer": "Different data points have different levels of importance",
            "explanation": "Weighted averages are specifically designed for situations where some values should count more than others.",
            "tags": ["weighted average", "when to use", "concept"],
        },
        {
            "question": "If a student's quiz score (weight 40%) is 100 and exam score (weight 60%) is 100, the weighted average is:",
            "choices": ["100", "80", "90", "95"],
            "answer": "100",
            "explanation": "When all scores are the same value (100), the weighted average is also 100 regardless of weights: (100×0.40)+(100×0.60) = 40+60 = 100.",
            "tags": ["weighted average", "equal scores", "concept"],
        },
    ]
    questions.extend(conceptual)

    return questions


# ============================================================
# MEDIUM QUESTION GENERATORS (200 questions)
# ============================================================

def gen_medium_questions():
    questions = []

    # Type 1: Three-component percentage weights (40 questions)
    components_3 = [
        ("quizzes", "midterm exam", "final exam"),
        ("attendance", "project", "exam"),
        ("homework", "oral recitation", "written test"),
        ("lab work", "midterm", "final"),
        ("participation", "research paper", "comprehensive exam"),
    ]
    for i in range(40):
        comp = components_3[i % len(components_3)]
        w1 = random.choice([15, 20, 25, 30])
        w2 = random.choice([20, 25, 30, 35])
        w3 = 100 - w1 - w2
        if w3 <= 0:
            w3 = 40
            w2 = 100 - w1 - w3
        s1 = random.randint(70, 98)
        s2 = random.randint(65, 95)
        s3 = random.randint(68, 96)
        correct = round2(s1*(w1/100) + s2*(w2/100) + s3*(w3/100))
        question_text = (
            f"A student's grade is based on: {comp[0]} ({w1}%), {comp[1]} ({w2}%), "
            f"and {comp[2]} ({w3}%). Scores are {s1}, {s2}, and {s3} respectively. "
            f"What is the weighted average?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=4)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({s1}×{w1/100:.2f}) + ({s2}×{w2/100:.2f}) + ({s3}×{w3/100:.2f}) "
                f"= {fmt(round2(s1*w1/100))} + {fmt(round2(s2*w2/100))} + {fmt(round2(s3*w3/100))} = {correct_str}."
            ),
            "tags": ["weighted average", "three components", "grades"],
        })

    # Type 2: GPA computation (30 questions)
    course_names = ["Math", "English", "Science", "Filipino", "History", "PE", "TLE", "MAPEH", "AP", "Computer"]
    for i in range(30):
        num_courses = random.choice([3, 4, 5])
        courses = random.sample(course_names, num_courses)
        grades = [round(random.uniform(1.0, 3.0), 2) for _ in range(num_courses)]
        units = [random.choice([2, 3, 4, 5]) for _ in range(num_courses)]
        correct = round2(sum(g*u for g, u in zip(grades, units)) / sum(units))
        course_info = ", ".join(f"{c}={g:.2f} ({u} units)" for c, g, u in zip(courses, grades, units))
        question_text = (
            f"Compute the GPA given these courses and grades: {course_info}."
        )
        distractors = generate_distractors_numeric(correct, spread=0.3)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=0.4)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"GPA = Σ(grade × units) ÷ Σ(units) = "
                f"({' + '.join(f'{g:.2f}×{u}' for g, u in zip(grades, units))}) ÷ {sum(units)} "
                f"= {fmt(round2(sum(g*u for g, u in zip(grades, units))))} ÷ {sum(units)} = {correct_str}."
            ),
            "tags": ["weighted average", "GPA", "credit hours"],
        })

    # Type 3: Weighted average salary/income (30 questions)
    departments = ["Admin", "Operations", "Finance", "IT", "HR", "Marketing", "Legal", "Engineering"]
    for i in range(30):
        num_dept = random.choice([2, 3])
        depts = random.sample(departments, num_dept)
        employees = [random.randint(10, 80) for _ in range(num_dept)]
        salaries = [random.randint(20, 60) * 1000 for _ in range(num_dept)]
        correct = round2(sum(s*e for s, e in zip(salaries, employees)) / sum(employees))
        dept_info = "; ".join(f"{d}: {e} employees earning ₱{s:,}/month" for d, e, s in zip(depts, employees, salaries))
        question_text = (
            f"An agency has the following departments — {dept_info}. "
            f"What is the overall average monthly salary?"
        )
        distractors = generate_distractors_numeric(correct, spread=2000)
        correct_str = f"₱{fmt(correct)}"
        dist_str = [f"₱{fmt(d)}" for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=3000)
            dist_str = [f"₱{fmt(d)}" for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average salary = ({' + '.join(f'{s}×{e}' for s, e in zip(salaries, employees))}) ÷ {sum(employees)} "
                f"= {sum(s*e for s, e in zip(salaries, employees))} ÷ {sum(employees)} = {correct_str}."
            ),
            "tags": ["weighted average", "salary", "workplace"],
        })

    # Type 4: Finding missing score (40 questions)
    for i in range(40):
        w1 = random.choice([20, 25, 30, 35, 40])
        w2 = random.choice([20, 25, 30, 35])
        w3 = 100 - w1 - w2
        if w3 <= 0:
            w3 = 30
            w2 = 100 - w1 - w3
        s1 = random.randint(72, 95)
        s2 = random.randint(72, 95)
        # Choose a target that's achievable
        target = random.randint(78, 92)
        # Compute required s3
        needed = (target - s1*(w1/100) - s2*(w2/100)) / (w3/100)
        needed = round2(needed)
        if needed < 50 or needed > 100:
            # Adjust target
            target = random.randint(75, 88)
            needed = round2((target - s1*(w1/100) - s2*(w2/100)) / (w3/100))
        if needed < 50 or needed > 100:
            needed = 85
            target = round2(s1*(w1/100) + s2*(w2/100) + needed*(w3/100))
        correct = round2(needed)
        comp_names = random.choice([
            ("quiz", "midterm", "final exam"),
            ("homework", "project", "exam"),
            ("attendance", "classwork", "test"),
        ])
        question_text = (
            f"A student needs a weighted average of {fmt(round2(target))} to pass. "
            f"The grading system is: {comp_names[0]} ({w1}%) = {s1}, {comp_names[1]} ({w2}%) = {s2}, "
            f"{comp_names[2]} ({w3}%) = ?. What minimum score is needed on the {comp_names[2]}?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=5)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Set up: ({s1}×{w1/100:.2f}) + ({s2}×{w2/100:.2f}) + (x×{w3/100:.2f}) = {fmt(round2(target))}. "
                f"{fmt(round2(s1*w1/100))} + {fmt(round2(s2*w2/100))} + {w3/100:.2f}x = {fmt(round2(target))}. "
                f"{w3/100:.2f}x = {fmt(round2(target - s1*w1/100 - s2*w2/100))}. x = {correct_str}."
            ),
            "tags": ["weighted average", "missing value", "algebra"],
        })

    # Type 5: Performance rating (30 questions)
    criteria = [
        ("Productivity", "Quality", "Teamwork"),
        ("Efficiency", "Accuracy", "Communication"),
        ("Speed", "Reliability", "Initiative"),
        ("Output", "Compliance", "Cooperation"),
        ("Technical skill", "Problem-solving", "Punctuality"),
    ]
    for i in range(30):
        crit = criteria[i % len(criteria)]
        w1 = random.choice([30, 35, 40, 45, 50])
        w2 = random.choice([20, 25, 30, 35])
        w3 = 100 - w1 - w2
        if w3 <= 0:
            w3 = 20
            w2 = 100 - w1 - w3
        r1 = round(random.uniform(3.0, 5.0), 1)
        r2 = round(random.uniform(3.0, 5.0), 1)
        r3 = round(random.uniform(3.0, 5.0), 1)
        correct = round2(r1*(w1/100) + r2*(w2/100) + r3*(w3/100))
        question_text = (
            f"An employee's performance is rated on: {crit[0]} ({w1}%) = {r1}, "
            f"{crit[1]} ({w2}%) = {r2}, {crit[2]} ({w3}%) = {r3}. "
            f"What is the overall weighted rating?"
        )
        distractors = generate_distractors_numeric(correct, spread=0.4)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=0.5)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted rating = ({r1}×{w1/100:.2f}) + ({r2}×{w2/100:.2f}) + ({r3}×{w3/100:.2f}) "
                f"= {fmt(round2(r1*w1/100))} + {fmt(round2(r2*w2/100))} + {fmt(round2(r3*w3/100))} = {correct_str}."
            ),
            "tags": ["weighted average", "performance rating", "workplace"],
        })

    # Type 6: Inventory/batch pricing with 3 batches (30 questions)
    products = ["rice sacks", "cement bags", "steel bars", "plywood sheets", "paint cans",
                "tiles", "pipes", "wires (meters)", "lumber pieces", "glass panels"]
    for i in range(30):
        product = products[i % len(products)]
        q1 = random.randint(50, 300)
        q2 = random.randint(50, 300)
        q3 = random.randint(50, 300)
        p1 = random.randint(100, 500) * 10
        p2 = random.randint(100, 500) * 10
        p3 = random.randint(100, 500) * 10
        total_q = q1 + q2 + q3
        total_cost = p1*q1 + p2*q2 + p3*q3
        correct = round2(total_cost / total_q)
        question_text = (
            f"A supplier delivers {product} in three batches: "
            f"{q1} units at ₱{p1} each, {q2} units at ₱{p2} each, and {q3} units at ₱{p3} each. "
            f"What is the weighted average cost per unit?"
        )
        distractors = generate_distractors_numeric(correct, spread=200)
        correct_str = f"₱{fmt(correct)}"
        dist_str = [f"₱{fmt(d)}" for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=300)
            dist_str = [f"₱{fmt(d)}" for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({p1}×{q1} + {p2}×{q2} + {p3}×{q3}) ÷ ({q1}+{q2}+{q3}) "
                f"= {total_cost} ÷ {total_q} = {correct_str}."
            ),
            "tags": ["weighted average", "inventory", "batch pricing"],
        })

    return questions


# ============================================================
# HARD QUESTION GENERATORS (200 questions)
# ============================================================

def gen_hard_questions():
    questions = []

    # Type 1: Four-component weighted average (35 questions)
    for i in range(35):
        components = random.choice([
            ("quizzes", "assignments", "midterm", "final exam"),
            ("attendance", "projects", "oral exam", "written exam"),
            ("lab reports", "homework", "practical exam", "theory exam"),
            ("recitation", "seatwork", "long test", "periodical exam"),
        ])
        # Generate 4 weights that sum to 100
        w1 = random.choice([10, 15, 20])
        w2 = random.choice([15, 20, 25])
        w3 = random.choice([25, 30])
        w4 = 100 - w1 - w2 - w3
        if w4 <= 0:
            w4 = 35
            w3 = 100 - w1 - w2 - w4
        scores = [random.randint(65, 98) for _ in range(4)]
        weights_dec = [w1/100, w2/100, w3/100, w4/100]
        correct = round2(sum(s*w for s, w in zip(scores, weights_dec)))
        question_text = (
            f"A course grade is computed from: {components[0]} ({w1}%) = {scores[0]}, "
            f"{components[1]} ({w2}%) = {scores[1]}, {components[2]} ({w3}%) = {scores[2]}, "
            f"{components[3]} ({w4}%) = {scores[3]}. What is the final weighted grade?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=4)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({scores[0]}×{weights_dec[0]:.2f}) + ({scores[1]}×{weights_dec[1]:.2f}) "
                f"+ ({scores[2]}×{weights_dec[2]:.2f}) + ({scores[3]}×{weights_dec[3]:.2f}) "
                f"= {fmt(round2(scores[0]*weights_dec[0]))} + {fmt(round2(scores[1]*weights_dec[1]))} "
                f"+ {fmt(round2(scores[2]*weights_dec[2]))} + {fmt(round2(scores[3]*weights_dec[3]))} = {correct_str}."
            ),
            "tags": ["weighted average", "four components", "grades"],
        })

    # Type 2: Finding missing weight (35 questions)
    for i in range(35):
        # Two known weights, one unknown
        # Strategy: pick values and weights such that the weighted average is exact
        # (no rounding needed), ensuring reverse computation yields exact integer weight.
        attempts = 0
        while attempts < 100:
            attempts += 1
            v1 = random.randint(70, 95)
            v2 = random.randint(70, 95)
            v3 = random.randint(70, 95)
            w1 = random.randint(1, 5)
            w2 = random.randint(1, 5)
            w3_actual = random.randint(1, 6)
            total_w = w1 + w2 + w3_actual
            numerator = v1 * w1 + v2 * w2 + v3 * w3_actual
            # Only accept if the weighted average has at most 2 clean decimal places
            if numerator % total_w == 0 or (numerator * 100) % total_w == 0:
                break
        target_exact = numerator / total_w
        # Use exact representation
        if target_exact == int(target_exact):
            target_str = str(int(target_exact))
        else:
            target_str = f"{target_exact:.2f}".rstrip("0").rstrip(".")
        correct = w3_actual
        question_text = (
            f"Three scores are {v1} (weight {w1}), {v2} (weight {w2}), and {v3} (weight unknown). "
            f"If the weighted average is {target_str}, what is the unknown weight?"
        )
        distractors = generate_distractors_numeric(correct, spread=2)
        # Ensure integer distractors
        dist_ints = list(set([int(round(d)) for d in distractors if int(round(d)) != correct and int(round(d)) > 0]))[:3]
        while len(dist_ints) < 3:
            candidate = correct + random.choice([-2, -1, 1, 2, 3])
            if candidate > 0 and candidate != correct and candidate not in dist_ints:
                dist_ints.append(candidate)
        correct_str = str(correct)
        dist_str = [str(d) for d in dist_ints[:3]]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Set up: ({v1}×{w1} + {v2}×{w2} + {v3}×w) ÷ ({w1}+{w2}+w) = {target_str}. "
                f"Cross-multiply: {v1*w1}+{v2*w2}+{v3}w = {target_str}×({w1+w2}+w). "
                f"Solving: {v3}w - {target_str}w = {target_str}×{w1+w2} - {v1*w1+v2*w2}. "
                f"w({v3} - {target_str}) = {fmt(round2(target_exact*(w1+w2) - (v1*w1+v2*w2)))}. w = {correct_str}."
            ),
            "tags": ["weighted average", "missing weight", "algebra"],
        })

    # Type 3: Multi-section combined average (30 questions)
    for i in range(30):
        num_sections = random.choice([3, 4])
        section_sizes = [random.randint(15, 50) for _ in range(num_sections)]
        section_avgs = [random.randint(70, 95) for _ in range(num_sections)]
        total_students = sum(section_sizes)
        total_score = sum(a*s for a, s in zip(section_avgs, section_sizes))
        correct = round2(total_score / total_students)
        section_info = ", ".join(
            f"Section {chr(65+j)} ({section_sizes[j]} students, average {section_avgs[j]})"
            for j in range(num_sections)
        )
        question_text = (
            f"A test was given to {num_sections} sections: {section_info}. "
            f"What is the overall average score for all students combined?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=4)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = ({' + '.join(f'{a}×{s}' for a, s in zip(section_avgs, section_sizes))}) ÷ {total_students} "
                f"= {total_score} ÷ {total_students} = {correct_str}."
            ),
            "tags": ["weighted average", "combined sections", "statistics"],
        })

    # Type 4: Investment portfolio returns (25 questions)
    investment_types = ["bonds", "stocks", "mutual funds", "real estate", "time deposits", "treasury bills"]
    for i in range(25):
        num_inv = random.choice([3, 4])
        inv = random.sample(investment_types, num_inv)
        amounts = [random.randint(5, 50) * 10000 for _ in range(num_inv)]
        returns = [round(random.uniform(2, 15), 1) for _ in range(num_inv)]
        total_amount = sum(amounts)
        weighted_return = round2(sum(r*a for r, a in zip(returns, amounts)) / total_amount)
        correct = weighted_return
        inv_info = ", ".join(f"₱{a:,} in {t} ({r}% return)" for t, a, r in zip(inv, amounts, returns))
        question_text = (
            f"An investor allocates: {inv_info}. "
            f"What is the weighted average return on the total portfolio?"
        )
        distractors = generate_distractors_numeric(correct, spread=1.5)
        correct_str = f"{fmt(correct)}%"
        dist_str = [f"{fmt(d)}%" for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=2)
            dist_str = [f"{fmt(d)}%" for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted return = ({' + '.join(f'{r}×{a}' for r, a in zip(returns, amounts))}) ÷ {total_amount} "
                f"= {fmt(round2(sum(r*a for r, a in zip(returns, amounts))))} ÷ {total_amount} = {correct_str}."
            ),
            "tags": ["weighted average", "investment", "finance"],
        })

    # Type 5: Survey/population weighting (25 questions)
    regions = ["NCR", "Region I", "Region II", "Region III", "Region IV-A",
               "Region IV-B", "Region V", "Region VI", "Region VII", "Region VIII"]
    for i in range(25):
        num_reg = random.choice([3, 4])
        regs = random.sample(regions, num_reg)
        populations = [random.randint(2, 20) * 100000 for _ in range(num_reg)]
        values = [random.randint(15, 60) * 1000 for _ in range(num_reg)]  # income
        total_pop = sum(populations)
        correct = round2(sum(v*p for v, p in zip(values, populations)) / total_pop)
        reg_info = ", ".join(f"{r} (pop. {p:,}, avg income ₱{v:,})" for r, p, v in zip(regs, populations, values))
        question_text = (
            f"Regional income data: {reg_info}. "
            f"What is the population-weighted average income?"
        )
        distractors = generate_distractors_numeric(correct, spread=3000)
        correct_str = f"₱{fmt(correct)}"
        dist_str = [f"₱{fmt(d)}" for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=4000)
            dist_str = [f"₱{fmt(d)}" for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Weighted average = Σ(income × population) ÷ Σ(population) "
                f"= {sum(v*p for v, p in zip(values, populations))} ÷ {total_pop} = {correct_str}."
            ),
            "tags": ["weighted average", "population", "statistics"],
        })

    # Type 6: Complex missing value with target (30 questions)
    for i in range(30):
        # 4 components, one unknown, find the score needed for a target
        w1 = random.choice([10, 15, 20])
        w2 = random.choice([20, 25])
        w3 = random.choice([25, 30])
        w4 = 100 - w1 - w2 - w3
        if w4 <= 0:
            w4 = 30
            w3 = 100 - w1 - w2 - w4
        s1 = random.randint(72, 96)
        s2 = random.randint(72, 96)
        s3 = random.randint(72, 96)
        target = random.randint(80, 92)
        # Solve for s4
        known_sum = s1*(w1/100) + s2*(w2/100) + s3*(w3/100)
        needed = round2((target - known_sum) / (w4/100))
        if needed < 50 or needed > 100:
            target = random.randint(78, 88)
            needed = round2((target - known_sum) / (w4/100))
        if needed < 50 or needed > 100:
            needed = 85
            target = round2(known_sum + needed*(w4/100))
        correct = round2(needed)
        comp = random.choice([
            ("quizzes", "project", "midterm", "final exam"),
            ("homework", "lab", "oral exam", "written exam"),
            ("attendance", "recitation", "long test", "periodical exam"),
        ])
        question_text = (
            f"A student's grade has 4 components: {comp[0]} ({w1}%) = {s1}, "
            f"{comp[1]} ({w2}%) = {s2}, {comp[2]} ({w3}%) = {s3}, "
            f"{comp[3]} ({w4}%) = ?. What score is needed on the {comp[3]} "
            f"to achieve a weighted average of {fmt(round2(target))}?"
        )
        distractors = generate_distractors_numeric(correct)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str:
            distractors = generate_distractors_numeric(correct, spread=5)
            dist_str = [fmt(d) for d in distractors]
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str),
            "explanation": (
                f"Known contributions: {fmt(round2(s1*w1/100))} + {fmt(round2(s2*w2/100))} + {fmt(round2(s3*w3/100))} "
                f"= {fmt(round2(known_sum))}. Need: {fmt(round2(target))} - {fmt(round2(known_sum))} = {fmt(round2(target-known_sum))}. "
                f"Score needed: {fmt(round2(target-known_sum))} ÷ {w4/100:.2f} = {correct_str}."
            ),
            "tags": ["weighted average", "missing value", "four components"],
        })

    # Type 7: Comparing weighted vs simple average (20 questions)
    for i in range(20):
        num_vals = random.choice([3, 4])
        values = [random.randint(65, 98) for _ in range(num_vals)]
        weights = [random.randint(1, 5) for _ in range(num_vals)]
        wa = round2(weighted_avg(values, weights))
        sa = round2(sum(values) / len(values))
        diff = round2(abs(wa - sa))
        if wa > sa:
            relation = "higher"
        elif wa < sa:
            relation = "lower"
        else:
            values[0] += 3
            wa = round2(weighted_avg(values, weights))
            sa = round2(sum(values) / len(values))
            diff = round2(abs(wa - sa))
            relation = "higher" if wa > sa else "lower"
        correct = diff
        vals_str = ", ".join(str(v) for v in values)
        wts_str = ", ".join(str(w) for w in weights)
        question_text = (
            f"Scores are {vals_str} with weights {wts_str}. "
            f"By how much is the weighted average {relation} than the simple average?"
        )
        distractors = generate_distractors_numeric(correct, spread=2)
        correct_str = fmt(correct)
        dist_str = [fmt(d) for d in distractors]
        while correct_str in dist_str or "0" in dist_str:
            distractors = generate_distractors_numeric(correct, spread=3)
            dist_str = [fmt(d) for d in distractors]
            dist_str = [d for d in dist_str if d != "0"]
            while len(dist_str) < 3:
                dist_str.append(fmt(correct + random.choice([1, 2, 3])))
        questions.append({
            "question": question_text,
            "answer": correct_str,
            "choices": make_choices(correct_str, dist_str[:3]),
            "explanation": (
                f"Weighted average = {fmt(wa)}. Simple average = {fmt(sa)}. "
                f"Difference = |{fmt(wa)} - {fmt(sa)}| = {correct_str}."
            ),
            "tags": ["weighted average", "comparison", "simple average"],
        })

    return questions


# ============================================================
# MAIN: Assemble and write JSON
# ============================================================

def main():
    easy = gen_easy_questions()
    medium = gen_medium_questions()
    hard = gen_hard_questions()

    # Deduplicate within each difficulty level
    def dedupe(q_list):
        seen = set()
        result = []
        for q in q_list:
            if q["question"] not in seen:
                seen.add(q["question"])
                result.append(q)
        return result

    easy = dedupe(easy)[:200]
    medium = dedupe(medium)[:200]
    hard = dedupe(hard)[:200]

    # If any list is short, we need to know
    if len(easy) < 200:
        print(f"WARNING: Only {len(easy)} easy questions generated")
    if len(medium) < 200:
        print(f"WARNING: Only {len(medium)} medium questions generated")
    if len(hard) < 200:
        print(f"WARNING: Only {len(hard)} hard questions generated")

    all_questions = []
    id_counter = 1

    for difficulty, q_list in [("Easy", easy), ("Medium", medium), ("Hard", hard)]:
        for q in q_list:
            all_questions.append({
                "id": id_counter,
                "subtest": SUBTEST,
                "module": MODULE,
                "subtopic": SUBTOPIC,
                "difficulty": difficulty,
                "question": q["question"],
                "choices": q["choices"],
                "answer": q["answer"],
                "explanation": q["explanation"],
                "tags": q["tags"],
                "category": CATEGORIES,
                "language": LANGUAGE,
            })
            id_counter += 1

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_questions)} questions:")
    print(f"  Easy: {len(easy)}")
    print(f"  Medium: {len(medium)}")
    print(f"  Hard: {len(hard)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
