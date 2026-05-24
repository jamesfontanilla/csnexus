"""
Generate 600 multiple-choice questions for Finding Missing Values in Averages.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/numerical-ability/ratio-proportion-and-average/finding-missing-values-in-averages/questions.json
"""

import json
import random
import os
from pathlib import Path

random.seed(42)

SUBTEST = "Numerical Ability"
MODULE = "Ratio, Proportion, and Average"
SUBTOPIC = "Finding Missing Values in Averages"


def generate_distractors_numeric(correct, count=3, min_val=1, spread=None):
    """Generate plausible wrong numeric answers near the correct answer."""
    if spread is None:
        spread = max(5, abs(correct) // 5) if correct != 0 else 5
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        attempts += 1
        offset = random.choice([-1, 1]) * random.randint(1, spread)
        d = correct + offset
        if d >= min_val and d != correct:
            distractors.add(d)
    result = list(distractors)[:count]
    while len(result) < count:
        result.append(correct + len(result) + 1)
    return result


def generate_distractors_float(correct, count=3, decimals=1):
    """Generate plausible wrong answers for decimal results."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        attempts += 1
        offset = random.choice([-1, 1]) * round(random.uniform(0.5, 5.0), decimals)
        d = round(correct + offset, decimals)
        if d > 0 and d != correct:
            distractors.add(d)
    result = list(distractors)[:count]
    while len(result) < count:
        result.append(round(correct + (len(result) + 1) * 0.5, decimals))
    return result


def make_choices(correct, distractors):
    """Shuffle correct answer among distractors."""
    choices = [str(correct)] + [str(d) for d in distractors[:3]]
    random.shuffle(choices)
    return choices


def fmt(val):
    """Format a number: remove trailing zeros for floats, use commas for large ints."""
    if isinstance(val, float):
        if val == int(val):
            return f"{int(val):,}" if abs(val) >= 1000 else str(int(val))
        return f"{val:,.1f}" if abs(val) >= 1000 else f"{val:.1f}"
    return f"{val:,}" if abs(val) >= 1000 else str(val)


# ============================================================
# EASY QUESTION GENERATORS (200 questions)
# ============================================================

def gen_easy_questions():
    questions = []
    qid = 1

    # Type 1: Simple missing value (small numbers, 3-5 items)
    contexts_easy = [
        ("numbers", "number", None),
        ("quiz scores", "score", None),
        ("test scores", "score", None),
        ("ages", "age", "years old"),
        ("weights", "weight", "kg"),
        ("heights", "height", "cm"),
        ("prices", "price", "pesos"),
        ("temperatures", "temperature", "°C"),
    ]

    for i in range(65):
        ctx = contexts_easy[i % len(contexts_easy)]
        n = random.randint(3, 5)
        avg = random.randint(15, 95)
        total = avg * n
        # Generate n-1 known values that sum to less than total
        known = []
        remaining = total
        for j in range(n - 2):
            val = random.randint(max(avg - 15, 5), avg + 15)
            known.append(val)
            remaining -= val
        # Last known value
        last_known = random.randint(max(avg - 12, 5), avg + 12)
        known.append(last_known)
        remaining -= last_known
        missing = remaining

        # Ensure missing is positive and reasonable
        if missing < 1 or missing > avg * 2:
            # Regenerate with controlled values
            known = [avg + random.randint(-10, 10) for _ in range(n - 1)]
            known_sum = sum(known)
            missing = total - known_sum
            if missing < 1:
                known[-1] -= (1 - missing + 5)
                missing = total - sum(known)

        known_str = ", ".join(str(k) for k in known)
        unit_str = f" {ctx[2]}" if ctx[2] else ""

        question_text = (
            f"The average of {n} {ctx[0]} is {avg}. "
            f"If {n-1} of the {ctx[0]} are {known_str}, what is the missing {ctx[1]}?"
        )

        distractors = generate_distractors_numeric(missing, 3, min_val=1)
        choices = make_choices(missing, distractors)
        explanation = (
            f"Total sum = {avg} × {n} = {total}. "
            f"Known sum = {' + '.join(str(k) for k in known)} = {sum(known)}. "
            f"Missing {ctx[1]} = {total} − {sum(known)} = {missing}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": question_text,
            "choices": choices,
            "answer": str(missing),
            "explanation": explanation,
            "tags": ["averages", "missing values", "mean", "total sum"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 2: Find the total sum given average and count (35 questions)
    for i in range(35):
        n = random.randint(3, 10)
        avg = random.randint(10, 100)
        total = avg * n

        question_text = f"The average of {n} numbers is {avg}. What is their total sum?"
        distractors = generate_distractors_numeric(total, 3, min_val=10)
        choices = make_choices(total, distractors)
        explanation = f"Total sum = Average × Count = {avg} × {n} = {total}."

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": question_text,
            "choices": choices,
            "answer": str(total),
            "explanation": explanation,
            "tags": ["averages", "total sum", "mean"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Student needs a score to achieve target average (40 questions)
    subjects = ["Math", "Science", "English", "Filipino", "History",
                "Social Studies", "Computer", "PE"]
    for i in range(40):
        n_exams = random.randint(4, 6)
        target_avg = random.randint(75, 95)
        target_total = target_avg * n_exams
        known_scores = [random.randint(target_avg - 15, target_avg + 10)
                        for _ in range(n_exams - 1)]
        known_sum = sum(known_scores)
        needed = target_total - known_sum

        # Ensure needed is between 50 and 100
        attempts = 0
        while (needed < 50 or needed > 100) and attempts < 50:
            known_scores = [random.randint(target_avg - 12, target_avg + 8)
                           for _ in range(n_exams - 1)]
            known_sum = sum(known_scores)
            needed = target_total - known_sum
            attempts += 1

        if needed < 50 or needed > 100:
            needed = target_avg
            known_scores = [target_avg + random.randint(-5, 5) for _ in range(n_exams - 2)]
            known_scores.append(target_total - sum(known_scores) - needed)
            known_sum = sum(known_scores)

        scores_str = ", ".join(str(s) for s in known_scores)
        question_text = (
            f"A student scored {scores_str} on {n_exams - 1} exams. "
            f"What score must she get on the next exam to have an average of {target_avg}?"
        )

        distractors = generate_distractors_numeric(needed, 3, min_val=50, spread=8)
        choices = make_choices(needed, distractors)
        explanation = (
            f"Required total = {target_avg} × {n_exams} = {target_total}. "
            f"Known sum = {known_sum}. "
            f"Needed score = {target_total} − {known_sum} = {needed}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": question_text,
            "choices": choices,
            "answer": str(needed),
            "explanation": explanation,
            "tags": ["averages", "missing score", "target average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 4: Simple workplace missing value (salary, expense) (40 questions)
    workplace_contexts = [
        ("daily earnings", "₱", [400, 600]),
        ("monthly expenses", "₱", [10000, 20000]),
        ("weekly sales", "₱", [5000, 15000]),
        ("daily production output", "", [100, 300]),
        ("hourly customers served", "", [10, 50]),
    ]

    for i in range(40):
        ctx = workplace_contexts[i % len(workplace_contexts)]
        n = random.randint(4, 6)
        low, high = ctx[2]
        avg = random.randint(low, high)
        # Make avg divisible by 5 or 10 for cleaner numbers
        avg = (avg // 5) * 5
        total = avg * n
        known = []
        for j in range(n - 1):
            val = avg + random.randint(-avg // 5, avg // 5)
            val = (val // 5) * 5  # Round to nearest 5
            known.append(val)
        known_sum = sum(known)
        missing = total - known_sum

        if missing < low // 2:
            known[-1] -= (low // 2 - missing + 10)
            known[-1] = (known[-1] // 5) * 5
            known_sum = sum(known)
            missing = total - known_sum

        prefix = ctx[1]
        known_str = ", ".join(f"{prefix}{fmt(k)}" for k in known)

        question_text = (
            f"The average of {n} {ctx[0]} is {prefix}{fmt(avg)}. "
            f"If {n-1} of them are {known_str}, what is the missing value?"
        )

        distractors = generate_distractors_numeric(missing, 3, min_val=1, spread=avg // 5)
        choices = make_choices(f"{prefix}{fmt(missing)}", [f"{prefix}{fmt(d)}" for d in distractors])
        explanation = (
            f"Total = {avg} × {n} = {total}. "
            f"Known sum = {known_sum}. "
            f"Missing = {total} − {known_sum} = {missing}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": question_text,
            "choices": choices,
            "answer": f"{prefix}{fmt(missing)}",
            "explanation": explanation,
            "tags": ["averages", "missing values", "workplace", ctx[0]],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Effect of adding a value equal to average (35 questions)
    for i in range(35):
        n = random.randint(3, 7)
        avg = random.randint(20, 90)
        new_val = avg + random.choice([-5, -3, 0, 3, 5, 8, -8, 10, -10])
        old_total = avg * n
        new_total = old_total + new_val
        new_avg = new_total / (n + 1)

        if new_avg == int(new_avg):
            new_avg = int(new_avg)
            question_text = (
                f"The average of {n} numbers is {avg}. "
                f"If a new number {new_val} is added, what is the new average?"
            )
            distractors = generate_distractors_numeric(new_avg, 3, min_val=1)
            choices = make_choices(new_avg, distractors)
            explanation = (
                f"Original total = {avg} × {n} = {old_total}. "
                f"New total = {old_total} + {new_val} = {new_total}. "
                f"New average = {new_total} ÷ {n+1} = {new_avg}."
            )
            answer_str = str(new_avg)
        else:
            new_avg_r = round(new_avg, 1)
            question_text = (
                f"The average of {n} numbers is {avg}. "
                f"If a new number {new_val} is added, what is the new average?"
            )
            distractors = generate_distractors_float(new_avg_r, 3)
            choices = make_choices(new_avg_r, distractors)
            explanation = (
                f"Original total = {avg} × {n} = {old_total}. "
                f"New total = {old_total} + {new_val} = {new_total}. "
                f"New average = {new_total} ÷ {n+1} = {new_avg_r}."
            )
            answer_str = str(new_avg_r)

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Easy",
            "question": question_text,
            "choices": choices,
            "answer": answer_str,
            "explanation": explanation,
            "tags": ["averages", "adding values", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# MEDIUM QUESTION GENERATORS (200 questions)
# ============================================================

def gen_medium_questions():
    questions = []
    qid = 201

    # Type 1: Missing value with larger numbers / more items (50 questions)
    contexts_med = [
        ("monthly electricity bills", "₱", [2000, 5000]),
        ("weekly sales figures", "₱", [50000, 150000]),
        ("daily distances traveled (km)", "", [100, 250]),
        ("quarterly performance scores", "", [70, 98]),
        ("monthly production outputs (units)", "", [500, 2000]),
    ]

    for i in range(50):
        ctx = contexts_med[i % len(contexts_med)]
        n = random.randint(5, 8)
        low, high = ctx[2]
        avg = random.randint(low, high)
        avg = (avg // 10) * 10 if avg > 100 else avg
        total = avg * n
        known = []
        for j in range(n - 1):
            val = avg + random.randint(-avg // 6, avg // 6)
            if avg > 100:
                val = (val // 10) * 10
            known.append(val)
        known_sum = sum(known)
        missing = total - known_sum

        if missing < low // 2 or missing > high * 2:
            known = [avg + random.randint(-avg // 8, avg // 8) for _ in range(n - 1)]
            if avg > 100:
                known = [(k // 10) * 10 for k in known]
            known_sum = sum(known)
            missing = total - known_sum

        prefix = ctx[1]
        known_str = ", ".join(f"{prefix}{fmt(k)}" for k in known)

        question_text = (
            f"A company's average {ctx[0]} over {n} periods is {prefix}{fmt(avg)}. "
            f"The values for {n-1} periods are {known_str}. "
            f"What is the missing value?"
        )

        distractors = generate_distractors_numeric(missing, 3, min_val=1,
                                                    spread=max(10, avg // 8))
        choices = make_choices(f"{prefix}{fmt(missing)}", [f"{prefix}{fmt(d)}" for d in distractors])
        explanation = (
            f"Required total = {avg} × {n} = {fmt(total)}. "
            f"Known sum = {fmt(known_sum)}. "
            f"Missing = {fmt(total)} − {fmt(known_sum)} = {fmt(missing)}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": f"{prefix}{fmt(missing)}",
            "explanation": explanation,
            "tags": ["averages", "missing values", "workplace", ctx[0].split()[0]],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: Adding a new member (40 questions)
    member_contexts = [
        ("employees", "salary", "₱", [25000, 45000]),
        ("students", "score", "", [70, 95]),
        ("players", "points per game", "", [15, 35]),
        ("workers", "daily output", "", [80, 200]),
        ("committee members", "age", "", [25, 55]),
    ]

    for i in range(40):
        ctx = member_contexts[i % len(member_contexts)]
        n_orig = random.randint(4, 10)
        low, high = ctx[3]
        orig_avg = random.randint(low, high)
        if orig_avg > 1000:
            orig_avg = (orig_avg // 1000) * 1000
        new_avg = orig_avg + random.choice([-3, -2, -1, 1, 2, 3, -4, -5, 4, 5])
        orig_total = orig_avg * n_orig
        new_total = new_avg * (n_orig + 1)
        new_member = new_total - orig_total

        if new_member < 0 or new_member > high * 2:
            new_avg = orig_avg - random.randint(1, 3)
            new_total = new_avg * (n_orig + 1)
            new_member = new_total - orig_total

        prefix = ctx[2]
        question_text = (
            f"The average {ctx[1]} of {n_orig} {ctx[0]} is {prefix}{fmt(orig_avg)}. "
            f"A new {ctx[0][:-1] if ctx[0].endswith('s') else ctx[0]} joins and the average becomes {prefix}{fmt(new_avg)}. "
            f"What is the new member's {ctx[1]}?"
        )

        distractors = generate_distractors_numeric(new_member, 3, min_val=1,
                                                    spread=max(5, abs(new_member) // 5))
        choices = make_choices(f"{prefix}{fmt(new_member)}", [f"{prefix}{fmt(d)}" for d in distractors])
        explanation = (
            f"Original total = {orig_avg} × {n_orig} = {fmt(orig_total)}. "
            f"New total = {new_avg} × {n_orig + 1} = {fmt(new_total)}. "
            f"New member's {ctx[1]} = {fmt(new_total)} − {fmt(orig_total)} = {fmt(new_member)}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": f"{prefix}{fmt(new_member)}",
            "explanation": explanation,
            "tags": ["averages", "adding member", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 3: Removing a member (40 questions)
    for i in range(40):
        ctx = member_contexts[i % len(member_contexts)]
        n_orig = random.randint(5, 12)
        low, high = ctx[3]
        orig_avg = random.randint(low, high)
        if orig_avg > 1000:
            orig_avg = (orig_avg // 1000) * 1000

        # The removed member's value determines the new average
        removed = orig_avg + random.randint(-15, 20)
        if removed < low // 2:
            removed = low
        orig_total = orig_avg * n_orig
        new_total = orig_total - removed
        new_n = n_orig - 1
        new_avg_exact = new_total / new_n

        # Ensure clean division
        attempts = 0
        while new_avg_exact != int(new_avg_exact) and attempts < 20:
            removed = orig_avg + random.randint(-10, 15)
            orig_total = orig_avg * n_orig
            new_total = orig_total - removed
            new_avg_exact = new_total / new_n
            attempts += 1

        if new_avg_exact != int(new_avg_exact):
            # Force clean numbers
            new_avg_int = orig_avg + random.choice([-1, 1, -2, 2])
            new_total = new_avg_int * new_n
            removed = orig_total - new_total
            new_avg_exact = new_avg_int

        new_avg_exact = int(new_avg_exact)
        prefix = ctx[2]

        question_text = (
            f"The average {ctx[1]} of {n_orig} {ctx[0]} is {prefix}{fmt(orig_avg)}. "
            f"When one {ctx[0][:-1] if ctx[0].endswith('s') else ctx[0]} leaves, "
            f"the average becomes {prefix}{fmt(new_avg_exact)}. "
            f"What was the {ctx[1]} of the one who left?"
        )

        distractors = generate_distractors_numeric(removed, 3, min_val=1,
                                                    spread=max(5, abs(removed) // 5))
        choices = make_choices(f"{prefix}{fmt(removed)}", [f"{prefix}{fmt(d)}" for d in distractors])
        explanation = (
            f"Original total = {orig_avg} × {n_orig} = {fmt(orig_total)}. "
            f"New total = {new_avg_exact} × {new_n} = {fmt(new_avg_exact * new_n)}. "
            f"Removed = {fmt(orig_total)} − {fmt(new_avg_exact * new_n)} = {fmt(removed)}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": f"{prefix}{fmt(removed)}",
            "explanation": explanation,
            "tags": ["averages", "removing member", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 4: Sequential average (after n innings/games, average changes) (35 questions)
    seq_contexts = [
        ("innings", "runs", "batsman"),
        ("games", "points", "player"),
        ("matches", "goals", "striker"),
        ("rounds", "score", "contestant"),
        ("days", "sales (₱)", "salesperson"),
    ]

    for i in range(35):
        ctx = seq_contexts[i % len(seq_contexts)]
        n_before = random.randint(4, 12)
        avg_before = random.randint(20, 80)
        avg_after = avg_before + random.randint(1, 8)
        total_before = avg_before * n_before
        total_after = avg_after * (n_before + 1)
        latest_value = total_after - total_before

        question_text = (
            f"After {n_before} {ctx[0]}, a {ctx[2]}'s average is {avg_before} {ctx[1]}. "
            f"After the next {ctx[0][:-1] if ctx[0].endswith('s') else ctx[0]}, "
            f"the average increases to {avg_after}. "
            f"How many {ctx[1]} were scored in the latest {ctx[0][:-1] if ctx[0].endswith('s') else ctx[0]}?"
        )

        distractors = generate_distractors_numeric(latest_value, 3, min_val=1, spread=10)
        choices = make_choices(latest_value, distractors)
        explanation = (
            f"Total after {n_before} {ctx[0]} = {avg_before} × {n_before} = {total_before}. "
            f"Total after {n_before + 1} {ctx[0]} = {avg_after} × {n_before + 1} = {total_after}. "
            f"Latest = {total_after} − {total_before} = {latest_value}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": str(latest_value),
            "explanation": explanation,
            "tags": ["averages", "sequential", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 5: Correcting an error (35 questions)
    for i in range(35):
        n = random.randint(10, 30)
        wrong_avg = random.randint(60, 90)
        wrong_total = wrong_avg * n
        wrong_val = random.randint(50, 85)
        correct_val = wrong_val + random.randint(5, 25)
        correction = correct_val - wrong_val
        correct_total = wrong_total + correction
        correct_avg_exact = correct_total / n

        # Ensure clean division
        attempts = 0
        while correct_avg_exact != int(correct_avg_exact) and attempts < 30:
            correction = random.choice([n, 2*n, n//2]) if n > 4 else random.randint(1, 5) * n
            correct_val = wrong_val + correction
            correct_total = wrong_total + correction
            correct_avg_exact = correct_total / n
            attempts += 1

        if correct_avg_exact != int(correct_avg_exact):
            # Force it
            correct_avg_exact = wrong_avg + random.randint(1, 3)
            correct_total = correct_avg_exact * n
            correction = correct_total - wrong_total
            correct_val = wrong_val + correction

        correct_avg_exact = int(correct_avg_exact)

        question_text = (
            f"A teacher calculated the average of {n} students as {wrong_avg}. "
            f"Later, she found that one score was recorded as {wrong_val} instead of {correct_val}. "
            f"What is the correct average?"
        )

        distractors = generate_distractors_numeric(correct_avg_exact, 3, min_val=50, spread=4)
        choices = make_choices(correct_avg_exact, distractors)
        explanation = (
            f"Incorrect total = {wrong_avg} × {n} = {fmt(wrong_total)}. "
            f"Correction = {correct_val} − {wrong_val} = +{correction}. "
            f"Correct total = {fmt(wrong_total)} + {correction} = {fmt(correct_total)}. "
            f"Correct average = {fmt(correct_total)} ÷ {n} = {correct_avg_exact}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": str(correct_avg_exact),
            "explanation": explanation,
            "tags": ["averages", "error correction", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# HARD QUESTION GENERATORS (200 questions)
# ============================================================

def gen_hard_questions():
    questions = []
    qid = 401

    # Type 1: Combined group averages (50 questions)
    group_contexts = [
        ("Section A", "Section B", "students", "score"),
        ("Department A", "Department B", "employees", "salary (₱)"),
        ("Branch 1", "Branch 2", "workers", "daily output"),
        ("Team Alpha", "Team Beta", "members", "rating"),
        ("Morning shift", "Afternoon shift", "staff", "items processed"),
    ]

    for i in range(50):
        ctx = group_contexts[i % len(group_contexts)]
        n1 = random.randint(8, 30)
        n2 = random.randint(8, 30)
        avg1 = random.randint(60, 95)
        avg2 = random.randint(60, 95)
        total1 = avg1 * n1
        total2 = avg2 * n2
        combined_total = total1 + total2
        combined_n = n1 + n2
        combined_avg_exact = combined_total / combined_n

        # Try to get clean numbers
        attempts = 0
        while combined_avg_exact != int(combined_avg_exact) and attempts < 30:
            n1 = random.randint(8, 25)
            n2 = random.randint(8, 25)
            avg1 = random.randint(60, 95)
            avg2 = random.randint(60, 95)
            total1 = avg1 * n1
            total2 = avg2 * n2
            combined_total = total1 + total2
            combined_n = n1 + n2
            combined_avg_exact = combined_total / combined_n
            attempts += 1

        if combined_avg_exact != int(combined_avg_exact):
            combined_avg_exact = round(combined_avg_exact, 1)
        else:
            combined_avg_exact = int(combined_avg_exact)

        question_text = (
            f"{ctx[0]} has {n1} {ctx[2]} with an average {ctx[3]} of {avg1}. "
            f"{ctx[1]} has {n2} {ctx[2]} with an average {ctx[3]} of {avg2}. "
            f"What is the combined average {ctx[3]} of all {combined_n} {ctx[2]}?"
        )

        if isinstance(combined_avg_exact, float):
            distractors = generate_distractors_float(combined_avg_exact, 3)
        else:
            distractors = generate_distractors_numeric(combined_avg_exact, 3, min_val=50, spread=5)
        choices = make_choices(combined_avg_exact, distractors)
        explanation = (
            f"{ctx[0]} total = {avg1} × {n1} = {fmt(total1)}. "
            f"{ctx[1]} total = {avg2} × {n2} = {fmt(total2)}. "
            f"Combined total = {fmt(combined_total)}. "
            f"Combined average = {fmt(combined_total)} ÷ {combined_n} = {combined_avg_exact}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": str(combined_avg_exact),
            "explanation": explanation,
            "tags": ["averages", "combined groups", "weighted average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 2: Finding a group's average given combined average (40 questions)
    for i in range(40):
        ctx = group_contexts[i % len(group_contexts)]
        n1 = random.randint(10, 25)
        n2 = random.randint(10, 25)
        combined_n = n1 + n2
        avg1 = random.randint(65, 90)
        combined_avg = random.randint(avg1 - 5, avg1 + 10)
        combined_total = combined_avg * combined_n
        total1 = avg1 * n1
        total2 = combined_total - total1
        avg2_exact = total2 / n2

        attempts = 0
        while avg2_exact != int(avg2_exact) and attempts < 30:
            n1 = random.randint(10, 20)
            n2 = random.randint(10, 20)
            combined_n = n1 + n2
            avg1 = random.randint(65, 90)
            combined_avg = avg1 + random.randint(-3, 5)
            combined_total = combined_avg * combined_n
            total1 = avg1 * n1
            total2 = combined_total - total1
            avg2_exact = total2 / n2
            attempts += 1

        if avg2_exact != int(avg2_exact):
            avg2_exact = round(avg2_exact, 1)
        else:
            avg2_exact = int(avg2_exact)

        if avg2_exact < 0:
            continue

        question_text = (
            f"A group of {combined_n} {ctx[2]} has a combined average {ctx[3]} of {combined_avg}. "
            f"If {ctx[0]} ({n1} {ctx[2]}) has an average of {avg1}, "
            f"what is {ctx[1]}'s average {ctx[3]} ({n2} {ctx[2]})?"
        )

        if isinstance(avg2_exact, float):
            distractors = generate_distractors_float(avg2_exact, 3)
        else:
            distractors = generate_distractors_numeric(avg2_exact, 3, min_val=40, spread=5)
        choices = make_choices(avg2_exact, distractors)
        explanation = (
            f"Combined total = {combined_avg} × {combined_n} = {fmt(combined_total)}. "
            f"{ctx[0]} total = {avg1} × {n1} = {fmt(total1)}. "
            f"{ctx[1]} total = {fmt(combined_total)} − {fmt(total1)} = {fmt(total2)}. "
            f"{ctx[1]} average = {fmt(total2)} ÷ {n2} = {avg2_exact}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": str(avg2_exact),
            "explanation": explanation,
            "tags": ["averages", "group average", "weighted average", "missing group"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Replacement problems (35 questions)
    for i in range(35):
        n = random.randint(5, 12)
        orig_avg = random.randint(60, 90)
        old_val = orig_avg + random.randint(-15, -5)
        new_avg = orig_avg + random.randint(1, 4)
        orig_total = orig_avg * n
        new_total = new_avg * n
        diff = new_total - orig_total
        new_val = old_val + diff

        question_text = (
            f"The average score of {n} students is {orig_avg}. "
            f"One student who scored {old_val} is replaced by another. "
            f"The new average becomes {new_avg}. "
            f"What is the replacement student's score?"
        )

        distractors = generate_distractors_numeric(new_val, 3, min_val=50, spread=8)
        choices = make_choices(new_val, distractors)
        explanation = (
            f"Original total = {orig_avg} × {n} = {fmt(orig_total)}. "
            f"New total = {new_avg} × {n} = {fmt(new_total)}. "
            f"Increase = {fmt(new_total)} − {fmt(orig_total)} = {diff}. "
            f"Replacement's score = {old_val} + {diff} = {new_val}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": str(new_val),
            "explanation": explanation,
            "tags": ["averages", "replacement", "changing average"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 4: Multi-step budget/target problems (40 questions)
    budget_contexts = [
        ("monthly budget", "₱", 12, [15000, 30000]),
        ("quarterly sales target", "₱", 4, [200000, 500000]),
        ("weekly production target", "", 5, [500, 1500]),
        ("semester grade target", "", 6, [75, 95]),
        ("annual savings goal", "₱", 12, [5000, 15000]),
    ]

    for i in range(40):
        ctx = budget_contexts[i % len(budget_contexts)]
        n = ctx[2]
        low, high = ctx[3]
        target_avg = random.randint(low, high)
        if target_avg > 1000:
            target_avg = (target_avg // 1000) * 1000
        target_total = target_avg * n

        # Generate completed periods
        completed = n - random.randint(1, 3)
        remaining = n - completed
        completed_values = [target_avg + random.randint(-target_avg // 8, target_avg // 8)
                           for _ in range(completed)]
        if target_avg > 1000:
            completed_values = [(v // 100) * 100 for v in completed_values]
        completed_sum = sum(completed_values)
        needed_total = target_total - completed_sum
        needed_avg = needed_total / remaining

        if needed_avg != int(needed_avg) and target_avg > 100:
            # Adjust to get clean numbers
            completed_sum = target_total - (int(needed_avg) + 1) * remaining
            needed_total = target_total - completed_sum
            needed_avg = needed_total / remaining

        if needed_avg == int(needed_avg):
            needed_avg = int(needed_avg)
        else:
            needed_avg = round(needed_avg, 1)

        prefix = ctx[1]

        if remaining == 1:
            question_text = (
                f"A target average of {prefix}{fmt(target_avg)} must be maintained over {n} periods. "
                f"After {completed} periods, the total is {prefix}{fmt(completed_sum)}. "
                f"What value is needed in the last period to meet the target?"
            )
            answer_val = needed_total
        else:
            question_text = (
                f"A target average of {prefix}{fmt(target_avg)} must be maintained over {n} periods. "
                f"After {completed} periods, the total is {prefix}{fmt(completed_sum)}. "
                f"What average is needed over the remaining {remaining} periods to meet the target?"
            )
            answer_val = needed_avg

        if isinstance(answer_val, float):
            distractors = generate_distractors_float(answer_val, 3)
        else:
            distractors = generate_distractors_numeric(answer_val, 3, min_val=1,
                                                        spread=max(5, abs(answer_val) // 8))
        choices = make_choices(f"{prefix}{fmt(answer_val)}", [f"{prefix}{fmt(d)}" for d in distractors])
        explanation = (
            f"Target total = {target_avg} × {n} = {fmt(target_total)}. "
            f"Remaining needed = {fmt(target_total)} − {fmt(completed_sum)} = {fmt(needed_total)}. "
            + (f"Needed value = {fmt(needed_total)}." if remaining == 1
               else f"Needed average = {fmt(needed_total)} ÷ {remaining} = {fmt(needed_avg)}.")
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": f"{prefix}{fmt(answer_val)}",
            "explanation": explanation,
            "tags": ["averages", "target average", "multi-step", "budgeting"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Three-group combined average (find one group's average) (35 questions)
    for i in range(35):
        n1 = random.randint(5, 15)
        n2 = random.randint(5, 15)
        n3 = random.randint(5, 15)
        total_n = n1 + n2 + n3
        avg1 = random.randint(60, 90)
        avg2 = random.randint(60, 90)
        combined_avg = random.randint(min(avg1, avg2) - 2, max(avg1, avg2) + 2)
        combined_total = combined_avg * total_n
        total1 = avg1 * n1
        total2 = avg2 * n2
        total3 = combined_total - total1 - total2
        avg3_exact = total3 / n3

        attempts = 0
        while (avg3_exact != int(avg3_exact) or avg3_exact < 40 or avg3_exact > 100) and attempts < 40:
            n1 = random.randint(5, 12)
            n2 = random.randint(5, 12)
            n3 = random.randint(5, 12)
            total_n = n1 + n2 + n3
            avg1 = random.randint(65, 85)
            avg2 = random.randint(65, 85)
            combined_avg = random.randint(min(avg1, avg2), max(avg1, avg2))
            combined_total = combined_avg * total_n
            total1 = avg1 * n1
            total2 = avg2 * n2
            total3 = combined_total - total1 - total2
            avg3_exact = total3 / n3
            attempts += 1

        if avg3_exact != int(avg3_exact) or avg3_exact < 40 or avg3_exact > 100:
            continue

        avg3_exact = int(avg3_exact)

        question_text = (
            f"A company has 3 departments. Department A ({n1} employees) averages {avg1}. "
            f"Department B ({n2} employees) averages {avg2}. "
            f"The overall average for all {total_n} employees is {combined_avg}. "
            f"What is Department C's average ({n3} employees)?"
        )

        distractors = generate_distractors_numeric(avg3_exact, 3, min_val=40, spread=6)
        choices = make_choices(avg3_exact, distractors)
        explanation = (
            f"Overall total = {combined_avg} × {total_n} = {fmt(combined_total)}. "
            f"Dept A total = {avg1} × {n1} = {fmt(total1)}. "
            f"Dept B total = {avg2} × {n2} = {fmt(total2)}. "
            f"Dept C total = {fmt(combined_total)} − {fmt(total1)} − {fmt(total2)} = {fmt(total3)}. "
            f"Dept C average = {fmt(total3)} ÷ {n3} = {avg3_exact}."
        )

        questions.append({
            "id": qid,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": str(avg3_exact),
            "explanation": explanation,
            "tags": ["averages", "three groups", "weighted average", "missing group"],
            "category": ["Professional", "Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


# ============================================================
# MAIN
# ============================================================

def deduplicate(questions):
    """Remove duplicate questions by question text."""
    seen = set()
    unique = []
    for q in questions:
        if q["question"] not in seen:
            seen.add(q["question"])
            unique.append(q)
    return unique


def main():
    easy = deduplicate(gen_easy_questions())
    medium = deduplicate(gen_medium_questions())
    hard = deduplicate(gen_hard_questions())

    # Ensure exactly 200 each
    if len(easy) < 200:
        print(f"WARNING: Only {len(easy)} unique Easy questions generated")
    if len(medium) < 200:
        print(f"WARNING: Only {len(medium)} unique Medium questions generated")
    if len(hard) < 200:
        print(f"WARNING: Only {len(hard)} unique Hard questions generated")

    easy = easy[:200]
    medium = medium[:200]
    hard = hard[:200]

    # Re-number IDs sequentially
    all_questions = []
    for idx, q in enumerate(easy + medium + hard, start=1):
        q["id"] = idx
        all_questions.append(q)

    # Final dedup check
    all_questions = deduplicate(all_questions)
    # Re-number again after dedup
    for idx, q in enumerate(all_questions, start=1):
        q["id"] = idx

    # Validate
    if len(all_questions) < 600:
        print(f"WARNING: After global dedup, only {len(all_questions)} unique questions. Padding...")
        # Generate extra easy questions to fill
        extra_needed = 600 - len(all_questions)
        existing_texts = {q["question"] for q in all_questions}
        extra_id = len(all_questions) + 1
        for i in range(extra_needed * 3):
            n = random.randint(3, 6)
            avg = random.randint(10, 99)
            total = avg * n
            known = [avg + random.randint(-12, 12) for _ in range(n - 1)]
            known_sum = sum(known)
            missing = total - known_sum
            if missing < 1:
                continue
            known_str = ", ".join(str(k) for k in known)
            qt = f"The average of {n} values is {avg}. If {n-1} of them are {known_str}, what is the missing value?"
            if qt in existing_texts:
                continue
            existing_texts.add(qt)
            distractors = generate_distractors_numeric(missing, 3, min_val=1)
            choices = make_choices(missing, distractors)
            all_questions.append({
                "id": extra_id,
                "subtest": SUBTEST,
                "module": MODULE,
                "subtopic": SUBTOPIC,
                "difficulty": "Easy",
                "question": qt,
                "choices": choices,
                "answer": str(missing),
                "explanation": f"Total = {avg} × {n} = {total}. Known sum = {known_sum}. Missing = {total} − {known_sum} = {missing}.",
                "tags": ["averages", "missing values", "mean"],
                "category": ["Professional", "Sub-Professional"],
                "language": "English"
            })
            extra_id += 1
            if len(all_questions) >= 600:
                break

    all_questions = all_questions[:600]
    for idx, q in enumerate(all_questions, start=1):
        q["id"] = idx

    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"
    easy_count = sum(1 for q in all_questions if q["difficulty"] == "Easy")
    med_count = sum(1 for q in all_questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in all_questions if q["difficulty"] == "Hard")
    print(f"Generated: {easy_count} Easy, {med_count} Medium, {hard_count} Hard")
    print(f"Total: {len(all_questions)}")

    # Verify all answers are in choices
    errors = 0
    for q in all_questions:
        if q["answer"] not in q["choices"]:
            print(f"ERROR: Q{q['id']} answer '{q['answer']}' not in choices {q['choices']}")
            errors += 1
    if errors:
        print(f"\n{errors} questions have answer/choice mismatches!")
    else:
        print("All answers verified in choices.")

    # Write output
    output_dir = Path(__file__).parent.parent / "data" / "seed" / "questions" / \
        "numerical-ability" / "ratio-proportion-and-average" / "finding-missing-values-in-averages"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "questions.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
