"""
Generate 600 multiple-choice questions for Introduction to Average (Mean).
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/numerical-ability/ratio-proportion-and-average/introduction-to-average/questions.json
"""

import json
import random
import os
from pathlib import Path

random.seed(42)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "seed" / "questions" / "numerical-ability" / "ratio-proportion-and-average" / "introduction-to-average"
SUBTEST = "Numerical Ability"
MODULE = "Ratio, Proportion, and Average"
SUBTOPIC = "Introduction to Average (Mean)"


def generate_distractors_numeric(correct, count=3, min_val=1, is_int=True):
    """Generate plausible numeric distractors near the correct answer."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        attempts += 1
        strategy = random.choice(["offset", "double", "half", "random_near"])
        if strategy == "offset":
            offset = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            d = correct + offset
        elif strategy == "double":
            d = correct * 2
        elif strategy == "half":
            d = correct / 2 if correct > 2 else correct + random.randint(2, 5)
        else:
            spread = max(int(abs(correct) * 0.2), 5)
            d = correct + random.randint(-spread, spread)
        if is_int:
            d = int(round(d))
        else:
            d = round(d, 2)
        if d != correct and d >= min_val and d not in distractors:
            distractors.add(d)
    while len(distractors) < count:
        d = correct + len(distractors) + 1
        if is_int:
            d = int(d)
        distractors.add(d)
    return list(distractors)[:count]


def format_number(n, is_int=True):
    """Format number for display."""
    if is_int:
        return str(int(n))
    return f"{n:.2f}" if n != int(n) else str(int(n))


def make_choices(correct, distractors, is_int=True):
    """Shuffle correct answer with distractors and return (choices, answer_str)."""
    fmt = lambda x: format_number(x, is_int)
    all_vals = [correct] + distractors
    random.shuffle(all_vals)
    choices = [fmt(v) for v in all_vals]
    answer = fmt(correct)
    return choices, answer


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

def generate_easy_questions():
    questions = []
    qid = 1

    # Type 1: Simple average of small whole numbers (50 questions)
    for _ in range(50):
        n = random.randint(3, 5)
        values = [random.randint(5, 50) for _ in range(n)]
        total = sum(values)
        # Ensure clean division
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n

        vals_str = ", ".join(str(v) for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=1)
        choices, answer = make_choices(mean, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"What is the average of {vals_str}?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Add all values: {' + '.join(str(v) for v in values)} = {total}. "
                          f"Divide by {n}: {total} ÷ {n} = {mean}.",
            "tags": ["average", "mean", "basic computation"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: Find the sum given average and count (30 questions)
    seen_type2 = set()
    while len([q for q in questions if "sum and count relationship" in q.get("tags", []) and q["question"].startswith("The average of")]) < 30:
        n = random.randint(3, 10)
        mean = random.randint(10, 60)
        key = (n, mean)
        if key in seen_type2:
            continue
        seen_type2.add(key)
        total = mean * n

        distractors = generate_distractors_numeric(total, 3, min_val=1)
        choices, answer = make_choices(total, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"The average of {n} numbers is {mean}. What is their sum?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = Mean × Count = {mean} × {n} = {total}.",
            "tags": ["average", "sum and count relationship"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Average of evenly spaced numbers (20 questions)
    for _ in range(20):
        while True:
            start = random.randint(5, 50)
            step = random.randint(2, 10)
            n = random.randint(3, 6)
            values = [start + i * step for i in range(n)]
            total = sum(values)
            if total % n == 0:
                break
        mean = total // n

        vals_str = ", ".join(str(v) for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=1)
        choices, answer = make_choices(mean, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"Find the average of {vals_str}.",
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = {' + '.join(str(v) for v in values)} = {total}. "
                          f"Count = {n}. Mean = {total} ÷ {n} = {mean}.",
            "tags": ["average", "arithmetic sequence", "basic computation"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 4: Simple missing value (30 questions)
    for _ in range(30):
        n = random.randint(3, 5)
        mean = random.randint(15, 60)
        total = mean * n
        known = []
        for i in range(n - 1):
            v = mean + random.randint(-10, 10)
            known.append(v)
        missing = total - sum(known)
        # Ensure positive
        if missing < 1:
            known[-1] -= (1 - missing + 5)
            missing = total - sum(known)

        known_str = ", ".join(str(v) for v in known)
        distractors = generate_distractors_numeric(missing, 3, min_val=1)
        choices, answer = make_choices(missing, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"The average of {n} numbers is {mean}. If {n-1} of the numbers are {known_str}, what is the missing number?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Required sum = {mean} × {n} = {total}. Known sum = {' + '.join(str(v) for v in known)} = {sum(known)}. "
                          f"Missing = {total} - {sum(known)} = {missing}.",
            "tags": ["average", "missing value", "sum and count relationship"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Conceptual / interpretation (20 questions)
    concepts = [
        ("What does the average (mean) represent?",
         ["The sum of values divided equally among all items",
          "The middle value when data is sorted",
          "The most frequently occurring value",
          "The difference between the highest and lowest values"],
         "The sum of values divided equally among all items",
         "The arithmetic mean distributes the total sum equally among all values in the set."),
        ("If the average of 4 numbers is 20, what is their total sum?",
         ["80", "20", "5", "100"],
         "80",
         "Sum = Mean × Count = 20 × 4 = 80."),
        ("Which formula correctly computes the arithmetic mean?",
         ["Sum of values ÷ Number of values",
          "Number of values ÷ Sum of values",
          "Sum of values × Number of values",
          "Largest value − Smallest value"],
         "Sum of values ÷ Number of values",
         "The arithmetic mean is calculated by dividing the sum of all values by the number of values."),
        ("The average of 10, 20, and 30 must be:",
         ["Between 10 and 30",
          "Greater than 30",
          "Less than 10",
          "Exactly 10 or 30"],
         "Between 10 and 30",
         "The mean always falls between the minimum and maximum values in the dataset."),
        ("If all 5 values in a dataset are equal to 12, what is the average?",
         ["12", "60", "5", "2.4"],
         "12",
         "When all values are equal, the average equals that value: 60 ÷ 5 = 12."),
        ("A student scored 70, 80, and 90. The average is 80. This means:",
         ["The total of 240 is shared equally as 80 per test",
          "The student always scored exactly 80",
          "80 is the highest possible average",
          "Most scores are below 80"],
         "The total of 240 is shared equally as 80 per test",
         "The average (80) represents equal distribution of the total (240) across 3 tests."),
        ("What happens to the average if you add a value larger than the current average?",
         ["The average increases",
          "The average decreases",
          "The average stays the same",
          "The average becomes zero"],
         "The average increases",
         "Adding a value above the current mean pulls the average upward."),
        ("The average of 5 numbers is 30. If one number is removed and the average of the remaining 4 is 28, what was removed?",
         ["38", "30", "28", "22"],
         "38",
         "Original sum = 30 × 5 = 150. New sum = 28 × 4 = 112. Removed = 150 - 112 = 38."),
        ("Which statement about averages is FALSE?",
         ["The average must equal one of the values in the dataset",
          "The average can be a decimal even if all values are whole numbers",
          "The average is affected by every value in the dataset",
          "The average falls between the smallest and largest values"],
         "The average must equal one of the values in the dataset",
         "The average does NOT have to equal any actual value. For example, the average of 3 and 4 is 3.5."),
        ("If the average of 6 numbers is 10, and one number changes from 8 to 14, the new average is:",
         ["11", "10", "12", "9"],
         "11",
         "Original sum = 60. Change adds 6 (14-8=6). New sum = 66. New average = 66 ÷ 6 = 11."),
    ]

    for q_text, ch, ans, expl in concepts:
        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": q_text,
            "choices": ch,
            "answer": ans,
            "explanation": expl,
            "tags": ["average", "conceptual understanding"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 6: Average with money context (20 questions)
    items_context = ["daily allowance", "daily earnings", "weekly savings", "daily expenses"]
    for _ in range(20):
        n = random.randint(3, 6)
        base = random.choice([50, 100, 150, 200, 250, 300, 500])
        values = [base + random.randint(-20, 20) * 5 for _ in range(n)]
        # Make divisible
        total = sum(values)
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n
        context = random.choice(items_context)

        vals_str = ", ".join(f"₱{v}" for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=1)
        choices, answer = make_choices(mean, distractors)
        choices = [f"₱{c}" if not c.startswith("₱") else c for c in choices]
        answer = f"₱{answer}" if not answer.startswith("₱") else answer

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"A worker's {context} for {n} days were {vals_str}. What is the average {context}?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = {' + '.join(str(v) for v in values)} = {total}. "
                          f"Average = {total} ÷ {n} = ₱{mean}.",
            "tags": ["average", "money", "practical application"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 7: Average of test scores (20 questions)
    for _ in range(20):
        n = random.randint(3, 5)
        values = [random.randint(60, 100) for _ in range(n)]
        total = sum(values)
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n

        vals_str = ", ".join(str(v) for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=50)
        choices, answer = make_choices(mean, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"A student's test scores are {vals_str}. What is the average score?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = {' + '.join(str(v) for v in values)} = {total}. "
                          f"Count = {n}. Average = {total} ÷ {n} = {mean}.",
            "tags": ["average", "test scores", "basic computation"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 8: Count from sum and average (fill to 200)
    seen_type8 = set()
    while len(questions) < 200:
        n = random.randint(3, 10)
        mean = random.randint(10, 60)
        key = (n, mean)
        if key in seen_type8:
            continue
        seen_type8.add(key)
        total = mean * n

        distractors = generate_distractors_numeric(n, 3, min_val=2)
        choices, answer = make_choices(n, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": f"A set of numbers has a sum of {total} and an average of {mean}. How many numbers are in the set?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Count = Sum ÷ Mean = {total} ÷ {mean} = {n}.",
            "tags": ["average", "sum and count relationship"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

def generate_medium_questions(start_id):
    questions = []
    qid = start_id

    # Type 1: Missing value with more numbers (40 questions)
    for _ in range(40):
        n = random.randint(5, 7)
        mean = random.randint(50, 95)
        total = mean * n
        known = []
        for i in range(n - 1):
            v = mean + random.randint(-15, 15)
            known.append(v)
        missing = total - sum(known)
        if missing < 1:
            known[-1] -= (1 - missing + 10)
            missing = total - sum(known)

        known_str = ", ".join(str(v) for v in known)
        distractors = generate_distractors_numeric(missing, 3, min_val=1)
        choices, answer = make_choices(missing, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": f"The average of {n} numbers is {mean}. If {n-1} of the numbers are {known_str}, what is the remaining number?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Required sum = {mean} × {n} = {total}. Known sum = {sum(known)}. "
                          f"Missing = {total} - {sum(known)} = {missing}.",
            "tags": ["average", "missing value", "medium computation"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: New member changes average (36 questions)
    for _ in range(36):
        n = random.randint(4, 8)
        old_mean = random.randint(25, 80)
        old_total = old_mean * n
        # New member joins
        new_n = n + 1
        new_mean = old_mean + random.choice([-3, -2, -1, 1, 2, 3])
        new_total = new_mean * new_n
        new_value = new_total - old_total

        if new_value < 1:
            new_mean = old_mean + 3
            new_total = new_mean * new_n
            new_value = new_total - old_total

        distractors = generate_distractors_numeric(new_value, 3, min_val=1)
        choices, answer = make_choices(new_value, distractors)

        context = random.choice([
            f"The average age of {n} employees is {old_mean}. A new employee joins and the average becomes {new_mean}. What is the new employee's age?",
            f"The average score of {n} students is {old_mean}. A new student joins and the average becomes {new_mean}. What is the new student's score?",
            f"The average weight of {n} packages is {old_mean} kg. A new package is added and the average becomes {new_mean} kg. What is the weight of the new package?",
        ])

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": context,
            "choices": choices,
            "answer": answer,
            "explanation": f"Original sum = {old_mean} × {n} = {old_total}. New sum = {new_mean} × {new_n} = {new_total}. "
                          f"New value = {new_total} - {old_total} = {new_value}.",
            "tags": ["average", "new member", "sum and count relationship"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Removing a value changes average (35 questions)
    seen_removed = set()
    count_removed = 0
    while count_removed < 30:
        n = random.randint(5, 8)
        old_mean = random.randint(30, 80)
        old_total = old_mean * n
        new_n = n - 1
        new_mean = old_mean + random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        new_total = new_mean * new_n
        removed = old_total - new_total

        if removed < 1:
            new_mean = old_mean - 4
            new_total = new_mean * new_n
            removed = old_total - new_total

        key = (n, old_mean, new_mean)
        if key in seen_removed:
            continue
        seen_removed.add(key)

        distractors = generate_distractors_numeric(removed, 3, min_val=1)
        choices, answer = make_choices(removed, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": f"The average of {n} numbers is {old_mean}. When one number is removed, the average of the remaining {new_n} numbers becomes {new_mean}. What number was removed?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Original sum = {old_mean} × {n} = {old_total}. New sum = {new_mean} × {new_n} = {new_total}. "
                          f"Removed = {old_total} - {new_total} = {removed}.",
            "tags": ["average", "removed value", "sum and count relationship"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1
        count_removed += 1

    # Type 4: Workplace/salary average problems (30 questions)
    for _ in range(30):
        n = random.randint(4, 8)
        base_salary = random.choice([15000, 18000, 20000, 22000, 25000, 28000, 30000, 35000])
        values = [base_salary + random.randint(-3000, 3000) for _ in range(n)]
        total = sum(values)
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n

        vals_str = ", ".join(f"₱{v:,}" for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=10000)
        choices, answer = make_choices(mean, distractors)
        choices = [f"₱{int(c.replace('₱', '').replace(',', '')):,}" if c.replace('₱', '').replace(',', '').lstrip('-').isdigit() else c for c in choices]
        answer = f"₱{mean:,}"

        context = random.choice([
            f"The monthly salaries of {n} employees are {vals_str}. What is the average salary?",
            f"A department has {n} staff members earning {vals_str} respectively. Find the average monthly pay.",
        ])

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": context,
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = {total:,}. Count = {n}. Average = {total:,} ÷ {n} = ₱{mean:,}.",
            "tags": ["average", "salary", "workplace", "practical application"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Average speed/distance problems (25 questions)
    for _ in range(25):
        n = random.randint(3, 6)
        base_dist = random.choice([80, 100, 120, 150, 200])
        values = [base_dist + random.randint(-30, 30) for _ in range(n)]
        total = sum(values)
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n

        vals_str = ", ".join(f"{v} km" for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=30)
        choices, answer = make_choices(mean, distractors)
        choices = [f"{c} km" for c in choices]
        answer = f"{mean} km"

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": f"A delivery truck traveled {vals_str} over {n} days. What is the average daily distance?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Total distance = {total} km. Days = {n}. Average = {total} ÷ {n} = {mean} km.",
            "tags": ["average", "distance", "transportation", "practical application"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 6: Score needed to achieve target average (40 questions)
    for _ in range(40):
        n_total = random.randint(4, 6)
        target_mean = random.randint(75, 95)
        target_total = target_mean * n_total
        n_known = n_total - 1
        known = [target_mean + random.randint(-12, 12) for _ in range(n_known)]
        needed = target_total - sum(known)
        if needed < 50 or needed > 100:
            # Adjust to keep in reasonable score range
            known = [target_mean + random.randint(-5, 5) for _ in range(n_known)]
            needed = target_total - sum(known)

        known_str = ", ".join(str(v) for v in known)
        distractors = generate_distractors_numeric(needed, 3, min_val=1)
        choices, answer = make_choices(needed, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": f"A student wants an average of {target_mean} across {n_total} exams. Her scores on the first {n_known} exams are {known_str}. What score does she need on the last exam?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Required sum = {target_mean} × {n_total} = {target_total}. "
                          f"Current sum = {sum(known)}. Needed = {target_total} - {sum(known)} = {needed}.",
            "tags": ["average", "target score", "missing value"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

def generate_hard_questions(start_id):
    questions = []
    qid = start_id

    # Type 1: Weighted/combined averages (40 questions)
    for _ in range(40):
        n1 = random.randint(10, 40)
        n2 = random.randint(10, 40)
        mean1 = random.randint(60, 90)
        mean2 = random.randint(60, 90)
        total_n = n1 + n2
        combined_total = mean1 * n1 + mean2 * n2
        # Ensure clean division
        remainder = combined_total % total_n
        if remainder != 0:
            mean1 += 1
            combined_total = mean1 * n1 + mean2 * n2
            remainder = combined_total % total_n
        if remainder != 0:
            # Force it
            combined_total = (combined_total // total_n) * total_n
            # Recalculate mean1
            mean1 = (combined_total - mean2 * n2) // n1
            combined_total = mean1 * n1 + mean2 * n2

        combined_mean = combined_total // total_n if total_n > 0 and combined_total % total_n == 0 else round(combined_total / total_n, 2)
        is_int = isinstance(combined_mean, int) or combined_mean == int(combined_mean)
        if is_int:
            combined_mean = int(combined_mean)

        distractors = generate_distractors_numeric(combined_mean, 3, min_val=50, is_int=is_int)
        choices, answer = make_choices(combined_mean, distractors, is_int=is_int)

        context = random.choice([
            f"Section A has {n1} students with an average score of {mean1}. Section B has {n2} students with an average score of {mean2}. What is the combined average of both sections?",
            f"Branch A has {n1} employees with an average salary grade of {mean1}. Branch B has {n2} employees with an average salary grade of {mean2}. What is the overall average salary grade?",
        ])

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": context,
            "choices": choices,
            "answer": answer,
            "explanation": f"Combined sum = ({mean1} × {n1}) + ({mean2} × {n2}) = {mean1*n1} + {mean2*n2} = {combined_total}. "
                          f"Total count = {n1} + {n2} = {total_n}. Combined average = {combined_total} ÷ {total_n} = {combined_mean}.",
            "tags": ["average", "weighted average", "combined groups"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: Replacing a value changes the average (35 questions)
    for _ in range(35):
        n = random.randint(5, 10)
        old_mean = random.randint(40, 80)
        old_total = old_mean * n
        increase = random.randint(2, 8)
        new_mean = old_mean + increase
        new_total = new_mean * n
        diff = new_total - old_total  # how much the replaced value increased by

        old_value = random.randint(20, old_mean - 5)
        new_value = old_value + diff

        distractors = generate_distractors_numeric(new_value, 3, min_val=1)
        choices, answer = make_choices(new_value, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": f"The average of {n} numbers is {old_mean}. If one number ({old_value}) is replaced by a new number, the average becomes {new_mean}. What is the new number?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Old sum = {old_mean} × {n} = {old_total}. New sum = {new_mean} × {n} = {new_total}. "
                          f"Difference = {new_total} - {old_total} = {diff}. New number = {old_value} + {diff} = {new_value}.",
            "tags": ["average", "replacement", "advanced computation"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Consecutive/series average problems (30 questions)
    for _ in range(30):
        start = random.randint(10, 50)
        n = random.randint(5, 15)
        # Consecutive integers
        values = list(range(start, start + n))
        total = sum(values)
        mean = total / n
        is_int = mean == int(mean)
        if is_int:
            mean = int(mean)

        distractors = generate_distractors_numeric(mean, 3, min_val=1, is_int=is_int)
        choices, answer = make_choices(mean, distractors, is_int=is_int)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": f"What is the average of all integers from {start} to {start + n - 1}?",
            "choices": choices,
            "answer": answer,
            "explanation": f"For consecutive integers from {start} to {start+n-1}, the average = (first + last) ÷ 2 = ({start} + {start+n-1}) ÷ 2 = {start + start+n-1} ÷ 2 = {mean}.",
            "tags": ["average", "consecutive integers", "series"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 4: Multi-step average problems (35 questions)
    for _ in range(35):
        # Average of first group + average of second group, find overall or missing
        n1 = random.randint(3, 6)
        n2 = random.randint(3, 6)
        mean1 = random.randint(50, 90)
        overall_mean = random.randint(55, 85)
        overall_n = n1 + n2
        overall_total = overall_mean * overall_n
        total1 = mean1 * n1
        total2 = overall_total - total1
        mean2 = total2 // n2
        # Ensure clean
        if total2 % n2 != 0:
            overall_mean += 1
            overall_total = overall_mean * overall_n
            total2 = overall_total - total1
            mean2 = total2 // n2
            if total2 % n2 != 0:
                mean1 = overall_mean  # simplify
                total1 = mean1 * n1
                total2 = overall_total - total1
                mean2 = total2 // n2 if total2 % n2 == 0 else round(total2 / n2, 2)

        if isinstance(mean2, float) and mean2 != int(mean2):
            continue  # skip non-clean ones

        mean2 = int(mean2) if isinstance(mean2, float) else mean2
        if mean2 < 10:
            continue

        distractors = generate_distractors_numeric(mean2, 3, min_val=10)
        choices, answer = make_choices(mean2, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": f"The average of {n1} numbers is {mean1}. The average of all {overall_n} numbers combined is {overall_mean}. What is the average of the other {n2} numbers?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum of first group = {mean1} × {n1} = {total1}. Total sum = {overall_mean} × {overall_n} = {overall_total}. "
                          f"Sum of second group = {overall_total} - {total1} = {total2}. Average of second group = {total2} ÷ {n2} = {mean2}.",
            "tags": ["average", "combined groups", "multi-step"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Average with decimal values / larger datasets (30 questions)
    for _ in range(30):
        n = random.randint(6, 10)
        base = random.randint(100, 500)
        values = [base + random.randint(-50, 50) for _ in range(n)]
        total = sum(values)
        remainder = total % n
        values[-1] += (n - remainder) if remainder != 0 else 0
        total = sum(values)
        mean = total // n

        vals_str = ", ".join(str(v) for v in values)
        distractors = generate_distractors_numeric(mean, 3, min_val=50)
        choices, answer = make_choices(mean, distractors)

        context = random.choice([
            f"A factory's daily production (in units) over {n} days was: {vals_str}. What is the average daily production?",
            f"The monthly electricity consumption (in kWh) for {n} months was: {vals_str}. Find the average monthly consumption.",
            f"A government office processed the following number of applications over {n} days: {vals_str}. What is the average daily processing rate?",
        ])

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": context,
            "choices": choices,
            "answer": answer,
            "explanation": f"Sum = {total}. Count = {n}. Average = {total} ÷ {n} = {mean}.",
            "tags": ["average", "large dataset", "workplace"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 6: Average changed by adding/subtracting constant (30 questions)
    for _ in range(30):
        n = random.randint(4, 8)
        old_mean = random.randint(30, 80)
        constant = random.randint(2, 10)
        operation = random.choice(["added to", "subtracted from"])
        if operation == "added to":
            new_mean = old_mean + constant
        else:
            new_mean = old_mean - constant

        distractors = generate_distractors_numeric(new_mean, 3, min_val=1)
        choices, answer = make_choices(new_mean, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": f"The average of {n} numbers is {old_mean}. If {constant} is {operation} each number, what is the new average?",
            "choices": choices,
            "answer": answer,
            "explanation": f"When a constant is {operation} every value, the average changes by the same amount. "
                          f"New average = {old_mean} {'+ ' + str(constant) if operation == 'added to' else '- ' + str(constant)} = {new_mean}.",
            "tags": ["average", "constant change", "properties of mean"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Pad to exactly 200 if needed with additional hard problems
    while len(questions) < 200:
        n = random.randint(5, 9)
        mean = random.randint(40, 90)
        total = mean * n
        # Two missing values
        n_known = n - 2
        known = [mean + random.randint(-10, 10) for _ in range(n_known)]
        remaining_sum = total - sum(known)
        # Give one constraint: the two missing values are equal
        missing_each = remaining_sum // 2
        if remaining_sum % 2 != 0:
            known[-1] += 1
            remaining_sum = total - sum(known)
            missing_each = remaining_sum // 2
        if missing_each < 5:
            continue

        known_str = ", ".join(str(v) for v in known)
        distractors = generate_distractors_numeric(missing_each, 3, min_val=1)
        choices, answer = make_choices(missing_each, distractors)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": f"The average of {n} numbers is {mean}. If {n_known} of the numbers are {known_str} and the remaining two numbers are equal, what is each of the two equal numbers?",
            "choices": choices,
            "answer": answer,
            "explanation": f"Required sum = {mean} × {n} = {total}. Known sum = {sum(known)}. "
                          f"Remaining sum = {total} - {sum(known)} = {remaining_sum}. Each equal number = {remaining_sum} ÷ 2 = {missing_each}.",
            "tags": ["average", "two unknowns", "advanced"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# MAIN
# ============================================================

def main():
    print("Generating Easy questions...")
    easy = generate_easy_questions()
    print(f"  Generated {len(easy)} Easy questions")

    print("Generating Medium questions...")
    medium = generate_medium_questions(start_id=len(easy) + 1)
    print(f"  Generated {len(medium)} Medium questions")

    print("Generating Hard questions...")
    hard = generate_hard_questions(start_id=len(easy) + len(medium) + 1)
    print(f"  Generated {len(hard)} Hard questions")

    all_questions = easy + medium + hard

    # Re-number IDs sequentially
    for i, q in enumerate(all_questions, 1):
        q["id"] = i

    print(f"\nTotal questions: {len(all_questions)}")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")

    # Validate
    for q in all_questions:
        assert q["answer"] in q["choices"], f"Q{q['id']}: Answer '{q['answer']}' not in choices {q['choices']}"
        assert len(q["choices"]) == 4, f"Q{q['id']}: Expected 4 choices, got {len(q['choices'])}"

    # Deduplicate by question text
    seen = set()
    deduped = []
    for q in all_questions:
        if q["question"] not in seen:
            seen.add(q["question"])
            deduped.append(q)
    if len(deduped) < len(all_questions):
        print(f"  Removed {len(all_questions) - len(deduped)} duplicate(s)")
        all_questions = deduped

    # Re-number IDs after dedup
    for i, q in enumerate(all_questions, 1):
        q["id"] = i

    print(f"  Final count: {len(all_questions)}")

    assert len(all_questions) >= 600, f"Only {len(all_questions)} unique questions generated, need 600. Increase generation counts."
    all_questions = all_questions[:600]
    # Re-number again after trim
    for i, q in enumerate(all_questions, 1):
        q["id"] = i

    # Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"\nOutput written to: {output_path}")


if __name__ == "__main__":
    main()
