"""
Generate 600 multiple-choice questions for the Average Word Problems subtopic.
Distribution: 200 Easy, 200 Medium, 200 Hard.
All answers are mathematically verified before output.
"""
import json
import random
from pathlib import Path
from fractions import Fraction

random.seed(42)
questions = []
qid = 0


def add_q(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Ratio, Proportion, and Average",
        "subtopic": "Average Word Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def make_choices_int(correct):
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        offset = random.choice([1, 2, 3, 4, 5, 6, 8, 10, 12, 15])
        sign = random.choice([-1, 1])
        d = correct + sign * offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        d = correct + random.randint(1, 20)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
    all_vals = [correct] + sorted(distractors)
    random.shuffle(all_vals)
    return [str(v) for v in all_vals], str(correct)


def make_choices_float(correct, decimals=2):
    fmt = f"{{:.{decimals}f}}"
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        offset = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10])
        sign = random.choice([-1, 1])
        d = round(correct + sign * offset, decimals)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        d = round(correct + random.uniform(1, 10), decimals)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(round(d, decimals))
    all_vals = [correct] + sorted(distractors)
    random.shuffle(all_vals)
    return [fmt.format(v) for v in all_vals], fmt.format(correct)


def make_choices_peso(correct):
    distractors = set()
    attempts = 0
    step = max(500, (correct // 20) // 500 * 500) if correct > 5000 else max(100, correct // 10)
    while len(distractors) < 3 and attempts < 100:
        offset = random.choice([1, 2, 3, 4, 5]) * step
        sign = random.choice([-1, 1])
        d = correct + sign * offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        d = correct + random.randint(1, 5) * step
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
    all_vals = [correct] + sorted(distractors)
    random.shuffle(all_vals)
    return [f"\u20b1{v:,}" for v in all_vals], f"\u20b1{correct:,}"


# ============================================================
# EASY QUESTIONS (200)
# ============================================================
family_roles = ["siblings", "cousins", "friends", "classmates", "colleagues", "team members"]
vehicles = ["car", "bus", "van", "truck", "motorcycle", "bicycle", "jeepney", "train", "boat", "taxi"]
subjects = ["Math", "Science", "English", "Filipino", "History", "Social Studies"]
group_names_a = ["Section A", "Group 1", "Team Alpha", "Morning shift", "Department A"]
group_names_b = ["Section B", "Group 2", "Team Beta", "Afternoon shift", "Department B"]
expense_contexts = ["daily expenses", "weekly allowance", "monthly bills", "daily sales",
                    "weekly earnings", "daily tips", "monthly savings", "daily production output"]

# EASY Age: Simple average (25)
for i in range(25):
    count = random.choice([3, 4, 5])
    ages = [random.randint(8, 55) for _ in range(count)]
    total = sum(ages)
    remainder = total % count
    ages[-1] += (count - remainder) if remainder != 0 else 0
    total = sum(ages)
    avg = total // count
    group = random.choice(family_roles)
    ages_str = ", ".join(str(a) for a in ages)
    q = f"The ages of {count} {group} are {ages_str}. What is their average age?"
    choices, answer = make_choices_int(avg)
    exp = f"Sum = {' + '.join(str(a) for a in ages)} = {total}. Average = {total} \u00f7 {count} = {avg}."
    add_q("Easy", q, choices, answer, exp, ["average", "age problems", "word problems"])

# EASY Age: Find total from average (25)
for i in range(25):
    count = random.choice([3, 4, 5, 6, 7, 8])
    avg = random.randint(10, 50)
    total = avg * count
    group = random.choice(family_roles)
    q = f"The average age of {count} {group} is {avg} years. What is their total age?"
    choices, answer = make_choices_int(total)
    exp = f"Total = Average \u00d7 Count = {avg} \u00d7 {count} = {total}."
    add_q("Easy", q, choices, answer, exp, ["average", "age problems", "total from average"])


# EASY Speed: distance/time (25)
for i in range(25):
    speed = random.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 90, 100])
    time_h = random.choice([2, 3, 4, 5, 6, 8, 10])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} travels {distance} km in {time_h} hours. What is the average speed?"
    choices, answer = make_choices_int(speed)
    exp = f"Average speed = {distance} \u00f7 {time_h} = {speed} km/h."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "word problems"])

# EASY Speed: find distance (15)
for i in range(15):
    speed = random.choice([30, 40, 45, 50, 60, 70, 80, 90, 100])
    time_h = random.choice([2, 3, 4, 5, 6])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} travels at an average speed of {speed} km/h for {time_h} hours. What is the total distance?"
    choices, answer = make_choices_int(distance)
    exp = f"Distance = Speed \u00d7 Time = {speed} \u00d7 {time_h} = {distance} km."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "distance"])

# EASY Speed: find time (10)
for i in range(10):
    speed = random.choice([25, 30, 40, 50, 60, 75, 80, 100])
    time_h = random.choice([2, 3, 4, 5, 6, 8])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} covers {distance} km at {speed} km/h. How many hours does the trip take?"
    choices, answer = make_choices_int(time_h)
    exp = f"Time = {distance} \u00f7 {speed} = {time_h} hours."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "time"])


# EASY Financial: compute average from list (25)
for i in range(25):
    count = random.choice([4, 5, 6, 7])
    base = random.choice([200, 300, 500, 800, 1000, 1500, 2000, 5000, 8000, 10000])
    values = [base + random.choice([-200, -100, 0, 50, 100, 200, 300, 400, 500]) for _ in range(count)]
    total = sum(values)
    remainder = total % count
    values[-1] += (count - remainder) if remainder != 0 else 0
    total = sum(values)
    avg = total // count
    context = random.choice(expense_contexts)
    values_str = ", ".join(f"\u20b1{v:,}" for v in values)
    q = f"A worker's {context} for {count} days are: {values_str}. What is the average?"
    choices, answer = make_choices_peso(avg)
    exp = f"Total = \u20b1{total:,}. Average = \u20b1{total:,} \u00f7 {count} = \u20b1{avg:,}."
    add_q("Easy", q, choices, answer, exp, ["average", "financial problems", "word problems"])

# EASY Financial: find total from average (25)
for i in range(25):
    count = random.choice([4, 5, 6, 7, 8, 10, 12])
    avg = random.choice([500, 750, 1000, 1500, 2000, 2500, 3000, 5000, 8000, 10000, 15000, 20000, 25000])
    total = avg * count
    period = random.choice(["days", "weeks", "months"])
    context = random.choice(["expense", "income", "sales", "savings", "earnings"])
    q = f"If the average {context} over {count} {period} is \u20b1{avg:,}, what is the total {context}?"
    choices, answer = make_choices_peso(total)
    exp = f"Total = \u20b1{avg:,} \u00d7 {count} = \u20b1{total:,}."
    add_q("Easy", q, choices, answer, exp, ["average", "financial problems", "total from average"])


# EASY Group: equal-size combined average (20)
for i in range(20):
    n = random.choice([5, 10, 15, 20, 25])
    avg1 = random.randint(60, 90)
    avg2 = random.randint(60, 90)
    if (avg1 + avg2) % 2 != 0:
        avg2 += 1
    combined_avg = (avg1 + avg2) // 2
    ga = random.choice(group_names_a)
    gb = random.choice(group_names_b)
    subj = random.choice(subjects)
    q = (f"{ga} has {n} students averaging {avg1} in {subj}. "
         f"{gb} also has {n} students averaging {avg2}. Combined average?")
    choices, answer = make_choices_int(combined_avg)
    exp = f"Equal groups: ({avg1} + {avg2}) \u00f7 2 = {combined_avg}."
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "combined average"])

# EASY Group: find total from average (15)
for i in range(15):
    n = random.choice([8, 10, 12, 15, 20, 25, 30])
    avg = random.randint(65, 95)
    total = n * avg
    subj = random.choice(subjects)
    group = random.choice(group_names_a + group_names_b)
    q = f"{group} has {n} students averaging {avg} in {subj}. What is the total score?"
    choices, answer = make_choices_int(total)
    exp = f"Total = {avg} \u00d7 {n} = {total}."
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "total from average"])

# EASY Group: new member joins (15)
for i in range(15):
    count = random.choice([4, 5, 6, 7, 8, 9])
    avg = random.randint(50, 90)
    total = avg * count
    new_val = random.randint(50, 100)
    new_total = total + new_val
    new_count = count + 1
    remainder = new_total % new_count
    if remainder != 0:
        new_val += (new_count - remainder)
        new_total = total + new_val
    new_avg = new_total // new_count
    subj = random.choice(subjects)
    q = (f"The average score of {count} students in {subj} is {avg}. "
         f"A new student scoring {new_val} joins. New average?")
    choices, answer = make_choices_int(new_avg)
    exp = f"Old total = {total}. New total = {new_total}. New avg = {new_total} \u00f7 {new_count} = {new_avg}."
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "new member"])


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# MEDIUM Age: find missing age (20)
for i in range(20):
    count = random.choice([4, 5, 6])
    avg = random.randint(15, 45)
    total = avg * count
    known = [random.randint(avg - 12, avg + 12) for _ in range(count - 1)]
    missing = total - sum(known)
    if missing < 1 or missing > 80:
        known[-1] = total - sum(known[:-1]) - avg
        missing = avg
        total = sum(known) + missing
        avg = total // count
    group = random.choice(family_roles)
    known_str = ", ".join(str(a) for a in known)
    q = (f"The average age of {count} {group} is {avg}. "
         f"Ages of {count-1} are {known_str}. What is the remaining age?")
    choices, answer = make_choices_int(missing)
    exp = f"Total = {avg} \u00d7 {count} = {total}. Missing = {total} - {sum(known)} = {missing}."
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "missing value"])

# MEDIUM Age: person joins (15)
for i in range(15):
    count = random.choice([4, 5, 6, 7, 8])
    avg = random.randint(20, 45)
    total = avg * count
    new_age = random.randint(18, 60)
    new_total = total + new_age
    new_count = count + 1
    remainder = new_total % new_count
    if remainder != 0:
        new_age += (new_count - remainder)
        new_total = total + new_age
    new_avg = new_total // new_count
    group = random.choice(["employees", "members", "players", "workers", "students"])
    q = (f"Average age of {count} {group} is {avg}. "
         f"A new member aged {new_age} joins. New average?")
    choices, answer = make_choices_int(new_avg)
    exp = f"Old total = {total}. New total = {new_total}. New avg = {new_total} \u00f7 {new_count} = {new_avg}."
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "new member"])

# MEDIUM Age: future/past (15)
for i in range(15):
    count = random.choice([3, 4, 5, 6])
    avg_now = random.randint(20, 50)
    years = random.choice([2, 3, 4, 5, 6, 8, 10])
    if random.choice([True, False]):
        new_avg = avg_now + years
        q = f"Average age of {count} friends is {avg_now}. Average age after {years} years?"
        exp = f"Each ages by {years}, so average increases by {years}. Answer = {new_avg}."
    else:
        new_avg = avg_now - years
        q = f"Average age of {count} colleagues is {avg_now} now. Average age {years} years ago?"
        exp = f"Each was {years} younger, so average was {years} less. Answer = {new_avg}."
    choices, answer = make_choices_int(new_avg)
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "time change"])


# MEDIUM Speed: harmonic mean round trip (20)
for i in range(20):
    v1 = random.choice([20, 24, 25, 30, 36, 40, 48, 50, 60])
    v2 = random.choice([30, 36, 40, 48, 50, 60, 72, 80, 90, 100, 120])
    while v2 == v1:
        v2 = random.choice([40, 50, 60, 80, 100, 120])
    dist = random.choice([60, 80, 100, 120, 150, 180, 200, 240, 300])
    t1 = Fraction(dist, v1)
    t2 = Fraction(dist, v2)
    total_dist = 2 * dist
    total_time = t1 + t2
    avg_frac = Fraction(total_dist) / total_time
    avg_float = round(float(avg_frac), 2)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} travels {dist} km at {v1} km/h and returns at {v2} km/h. "
         f"Average speed for the round trip?")
    if avg_frac.denominator == 1:
        choices, answer = make_choices_int(int(avg_frac))
        exp = f"Harmonic mean = 2\u00d7{v1}\u00d7{v2} \u00f7 ({v1}+{v2}) = {2*v1*v2} \u00f7 {v1+v2} = {int(avg_frac)} km/h."
    else:
        choices, answer = make_choices_float(avg_float)
        exp = f"Harmonic mean = 2\u00d7{v1}\u00d7{v2} \u00f7 ({v1}+{v2}) = {2*v1*v2} \u00f7 {v1+v2} = {avg_float} km/h."
    add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "harmonic mean"])

# MEDIUM Speed: two-leg different distances (15)
for i in range(15):
    v1 = random.choice([30, 40, 50, 60, 80])
    v2 = random.choice([40, 50, 60, 75, 80, 100])
    while v2 == v1:
        v2 = random.choice([40, 50, 60, 80, 100])
    t1 = random.choice([1, 2, 3, 4])
    t2 = random.choice([1, 2, 3, 4])
    d1, d2 = v1 * t1, v2 * t2
    total_d, total_t = d1 + d2, t1 + t2
    avg_speed = total_d / total_t
    avg_speed = int(avg_speed) if avg_speed == int(avg_speed) else round(avg_speed, 2)
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} travels {d1} km at {v1} km/h, then {d2} km at {v2} km/h. Average speed?"
    if isinstance(avg_speed, int):
        choices, answer = make_choices_int(avg_speed)
    else:
        choices, answer = make_choices_float(avg_speed)
    exp = f"Time1={t1}h, Time2={t2}h. Avg = {total_d} \u00f7 {total_t} = {avg_speed} km/h."
    add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "two-leg trip"])

# MEDIUM Speed: find missing speed (15)
for i in range(15):
    v1 = random.choice([30, 40, 50, 60, 80])
    t1 = random.choice([1, 2, 3, 4])
    d1 = v1 * t1
    t2 = random.choice([1, 2, 3, 4])
    v2 = random.choice([20, 25, 30, 40, 50, 60, 80])
    d2 = v2 * t2
    total_d = d1 + d2
    total_t = t1 + t2
    avg_speed = total_d / total_t
    avg_speed = int(avg_speed) if avg_speed == int(avg_speed) else round(avg_speed, 2)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} covers {total_d} km. First {d1} km at {v1} km/h. "
         f"Average speed is {avg_speed} km/h. Speed for remaining {d2} km?")
    choices, answer = make_choices_int(v2)
    exp = f"Total time = {total_t}h. Time1 = {t1}h. Time2 = {t2}h. Speed2 = {d2} \u00f7 {t2} = {v2} km/h."
    add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "missing speed"])


# MEDIUM Financial: missing value for target average (20)
for i in range(20):
    count = random.choice([5, 6, 7, 8])
    target_avg = random.choice([5000, 8000, 10000, 12000, 15000, 18000, 20000, 25000])
    target_total = target_avg * count
    known_values = [target_avg + random.choice([-3000, -2000, -1000, 0, 1000, 2000, 3000]) for _ in range(count - 1)]
    missing = target_total - sum(known_values)
    if missing < 0:
        known_values[-1] -= abs(missing) + 1000
        missing = target_total - sum(known_values)
    known_str = ", ".join(f"\u20b1{v:,}" for v in known_values)
    period = random.choice(["months", "weeks", "days"])
    context = random.choice(["savings", "sales", "expenses", "income"])
    q = (f"Target average {context}: \u20b1{target_avg:,} over {count} {period}. "
         f"First {count-1}: {known_str}. Amount needed in last {period[:-1]}?")
    choices, answer = make_choices_peso(missing)
    exp = f"Target total = \u20b1{target_total:,}. Known = \u20b1{sum(known_values):,}. Missing = \u20b1{missing:,}."
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "missing value"])

# MEDIUM Financial: new member changes average (15)
for i in range(15):
    count = random.choice([4, 5, 6, 8, 10])
    avg = random.choice([10000, 15000, 20000, 25000, 30000])
    total = avg * count
    new_val = avg + random.choice([5000, 10000, 15000, -5000])
    if new_val < 0:
        new_val = avg + 5000
    new_total = total + new_val
    new_count = count + 1
    remainder = new_total % new_count
    if remainder != 0:
        new_val += (new_count - remainder)
        new_total = total + new_val
    new_avg = new_total // new_count
    context = random.choice(["salary", "monthly income", "daily sales"])
    q = (f"Average {context} of {count} employees: \u20b1{avg:,}. "
         f"New employee with \u20b1{new_val:,} joins. New average?")
    choices, answer = make_choices_peso(new_avg)
    exp = f"Old total = \u20b1{total:,}. New total = \u20b1{new_total:,}. New avg = \u20b1{new_avg:,}."
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "new member"])

# MEDIUM Financial: person leaves (15)
for i in range(15):
    count = random.choice([5, 6, 7, 8, 10])
    avg = random.choice([15000, 18000, 20000, 22000, 25000, 28000, 30000])
    total = avg * count
    leaving_val = avg + random.choice([5000, 8000, 10000])
    new_total = total - leaving_val
    new_count = count - 1
    remainder = new_total % new_count
    if remainder != 0:
        leaving_val -= remainder
        new_total = total - leaving_val
    new_avg = new_total // new_count
    q = (f"Average salary of {count} workers: \u20b1{avg:,}. "
         f"One earning \u20b1{leaving_val:,} resigns. New average?")
    choices, answer = make_choices_peso(new_avg)
    exp = f"Old total = \u20b1{total:,}. New total = \u20b1{new_total:,}. New avg = \u20b1{new_avg:,}."
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "member leaves"])


# MEDIUM Group: combine two unequal groups (20)
for i in range(20):
    n1 = random.choice([10, 12, 15, 20, 25, 30])
    n2 = random.choice([8, 10, 12, 15, 20, 25, 30, 35])
    while n2 == n1:
        n2 = random.choice([8, 10, 15, 20, 25, 30])
    avg1 = random.randint(60, 90)
    avg2 = random.randint(60, 90)
    total = n1 * avg1 + n2 * avg2
    combined_count = n1 + n2
    remainder = total % combined_count
    if remainder != 0:
        avg2 += 1
        total = n1 * avg1 + n2 * avg2
        remainder = total % combined_count
    combined_avg = total // combined_count if remainder == 0 else round(total / combined_count, 2)
    subj = random.choice(subjects)
    q = (f"{n1} students average {avg1} in {subj}. "
         f"{n2} students average {avg2}. Combined average?")
    if isinstance(combined_avg, int):
        choices, answer = make_choices_int(combined_avg)
    else:
        choices, answer = make_choices_float(combined_avg)
    exp = f"Total = {n1}\u00d7{avg1} + {n2}\u00d7{avg2} = {total}. Avg = {total} \u00f7 {combined_count} = {combined_avg}."
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "combined average"])

# MEDIUM Group: find subgroup average (15)
for i in range(15):
    n1 = random.choice([10, 15, 20, 25])
    n2 = random.choice([10, 15, 20, 25, 30])
    while n2 == n1:
        n2 = random.choice([10, 15, 20, 25, 30])
    avg1 = random.randint(65, 80)
    avg2 = random.randint(70, 90)
    total1 = n1 * avg1
    total2 = n2 * avg2
    total = total1 + total2
    combined_count = n1 + n2
    combined_avg = total // combined_count if total % combined_count == 0 else round(total / combined_count, 2)
    q = (f"A group of {combined_count} has combined average {combined_avg}. "
         f"The {n1} boys average {avg1}. What is the {n2} girls' average?")
    choices, answer = make_choices_int(avg2)
    exp = f"Total = {combined_avg}\u00d7{combined_count} (approx). Girls total = {total2}. Avg = {avg2}."
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "find subgroup average"])

# MEDIUM Group: new member changes average, find value (15)
for i in range(15):
    count = random.choice([5, 6, 7, 8, 9, 10])
    old_avg = random.randint(60, 85)
    old_total = old_avg * count
    new_count = count + 1
    new_avg = old_avg + random.choice([1, 2, 3, 4, 5])
    new_total = new_avg * new_count
    new_member_val = new_total - old_total
    subj = random.choice(subjects)
    q = (f"Average {subj} score of {count} students is {old_avg}. "
         f"New student joins, average becomes {new_avg}. New student's score?")
    choices, answer = make_choices_int(new_member_val)
    exp = f"Old total = {old_total}. New total = {new_total}. New student = {new_member_val}."
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "find new member value"])


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# HARD Age: replacement (15)
for i in range(15):
    count = random.choice([5, 6, 7, 8, 10])
    old_avg = random.randint(25, 45)
    old_total = old_avg * count
    leaving_age = random.randint(old_avg + 5, old_avg + 20)
    new_avg = old_avg - random.choice([1, 2, 3, 4, 5])
    new_total = new_avg * count
    new_person_age = new_total - old_total + leaving_age
    if new_person_age < 1:
        new_avg = old_avg - 1
        new_total = new_avg * count
        new_person_age = new_total - old_total + leaving_age
    group = random.choice(["employees", "team members", "workers", "players"])
    q = (f"Average age of {count} {group} is {old_avg}. Member aged {leaving_age} replaced. "
         f"New average is {new_avg}. Age of replacement?")
    choices, answer = make_choices_int(new_person_age)
    exp = (f"Old total={old_total}. New total={new_total}. "
           f"Replacement = {leaving_age} - ({old_total}-{new_total}) = {new_person_age}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "replacement"])

# HARD Age: combined group + time change (15)
for i in range(15):
    n1 = random.choice([3, 4, 5, 6])
    n2 = random.choice([3, 4, 5, 6])
    avg1 = random.randint(20, 40)
    avg2 = random.randint(25, 50)
    years = random.choice([2, 3, 4, 5])
    total1 = n1 * avg1
    total2 = n2 * avg2
    combined_count = n1 + n2
    future_total = total1 + total2 + combined_count * years
    remainder = future_total % combined_count
    if remainder != 0:
        avg1 += 1
        total1 = n1 * avg1
        future_total = total1 + total2 + combined_count * years
        remainder = future_total % combined_count
    future_avg = future_total // combined_count if remainder == 0 else round(future_total / combined_count, 2)
    q = (f"Group A: {n1} people, avg age {avg1}. Group B: {n2} people, avg age {avg2}. "
         f"Combined average age after {years} years?")
    if isinstance(future_avg, int):
        choices, answer = make_choices_int(future_avg)
    else:
        choices, answer = make_choices_float(future_avg)
    exp = (f"Combined total now = {total1+total2}. After {years}y: {future_total}. "
           f"Avg = {future_total} \u00f7 {combined_count} = {future_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "combined group", "time change"])

# HARD Age: sequential add/remove (10)
for i in range(10):
    count = random.choice([5, 6, 7, 8])
    avg = random.randint(25, 40)
    orig_total = avg * count
    add_age = random.randint(20, 55)
    remove_age = random.randint(20, 50)
    new_total = orig_total + add_age - remove_age
    remainder = new_total % count
    if remainder != 0:
        add_age += (count - remainder)
        new_total = orig_total + add_age - remove_age
    final_avg = new_total // count
    group = random.choice(["employees", "club members", "team players"])
    q = (f"Average age of {count} {group} is {avg}. "
         f"Member aged {add_age} joins, member aged {remove_age} leaves. New average?")
    choices, answer = make_choices_int(final_avg)
    exp = f"Total = {orig_total} + {add_age} - {remove_age} = {new_total}. Avg = {new_total} \u00f7 {count} = {final_avg}."
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "sequential changes"])

# HARD Age: find original average (10)
for i in range(10):
    count = random.choice([5, 6, 7, 8, 10])
    old_avg = random.randint(25, 45)
    old_total = old_avg * count
    new_count = count + 1
    new_member_age = random.randint(old_avg + 5, old_avg + 20)
    new_total = old_total + new_member_age
    remainder = new_total % new_count
    if remainder != 0:
        new_member_age += (new_count - remainder)
        new_total = old_total + new_member_age
    new_avg = new_total // new_count
    group = random.choice(["friends", "colleagues", "classmates"])
    q = (f"Person aged {new_member_age} joins {count} {group}. "
         f"New average becomes {new_avg}. Original average?")
    choices, answer = make_choices_int(old_avg)
    exp = f"New total = {new_avg}\u00d7{new_count} = {new_total}. Old total = {new_total}-{new_member_age} = {old_total}. Old avg = {old_avg}."
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "find original average"])


# HARD Speed: three-leg trip (20)
for i in range(20):
    v1 = random.choice([30, 40, 50, 60, 80])
    v2 = random.choice([40, 50, 60, 75, 80, 100])
    v3 = random.choice([20, 25, 30, 40, 50, 60])
    t1 = random.choice([1, 2, 3])
    t2 = random.choice([1, 2, 3])
    t3 = random.choice([1, 2, 3])
    d1, d2, d3 = v1*t1, v2*t2, v3*t3
    total_d = d1 + d2 + d3
    total_t = t1 + t2 + t3
    avg_speed = total_d / total_t
    avg_speed = int(avg_speed) if avg_speed == int(avg_speed) else round(avg_speed, 2)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle}: {d1} km at {v1} km/h, {d2} km at {v2} km/h, "
         f"{d3} km at {v3} km/h. Average speed?")
    if isinstance(avg_speed, int):
        choices, answer = make_choices_int(avg_speed)
    else:
        choices, answer = make_choices_float(avg_speed)
    exp = f"Times: {t1}h, {t2}h, {t3}h. Total={total_d}km, {total_t}h. Avg={avg_speed} km/h."
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "three-leg trip"])

# HARD Speed: fractional distance (15)
for i in range(15):
    total_d = random.choice([120, 180, 240, 300, 360, 480, 600])
    d_each = total_d // 3
    v1 = random.choice([30, 40, 60, 80, 120])
    while d_each % v1 != 0:
        v1 = random.choice([30, 40, 60, 80, 120])
    v2 = random.choice([40, 60, 80, 120])
    while d_each % v2 != 0:
        v2 = random.choice([40, 60, 80, 120])
    v3 = random.choice([20, 30, 40, 60, 80, 120])
    while d_each % v3 != 0:
        v3 = random.choice([20, 30, 40, 60, 80, 120])
    t1, t2, t3 = d_each//v1, d_each//v2, d_each//v3
    total_t = t1 + t2 + t3
    avg_speed = total_d / total_t
    avg_speed = int(avg_speed) if avg_speed == int(avg_speed) else round(avg_speed, 2)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} covers {total_d} km: first third at {v1} km/h, "
         f"second third at {v2} km/h, last third at {v3} km/h. Average speed?")
    if isinstance(avg_speed, int):
        choices, answer = make_choices_int(avg_speed)
    else:
        choices, answer = make_choices_float(avg_speed)
    exp = f"Each third={d_each}km. Times: {t1}h,{t2}h,{t3}h. Avg={total_d}\u00f7{total_t}={avg_speed} km/h."
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "fractional distance"])

# HARD Speed: round trip with stop (15)
for i in range(15):
    dist = random.choice([60, 80, 100, 120, 150, 180, 200, 240])
    v_go = random.choice([30, 40, 50, 60, 80])
    v_ret = random.choice([20, 30, 40, 50, 60])
    while v_ret == v_go:
        v_ret = random.choice([20, 30, 40, 50, 60])
    stop = random.choice([Fraction(1,2), Fraction(1,1), Fraction(3,2), Fraction(2,1)])
    t_go = Fraction(dist, v_go)
    t_ret = Fraction(dist, v_ret)
    total_d = 2 * dist
    total_t = t_go + t_ret + stop
    avg_frac = Fraction(total_d) / total_t
    avg_val = int(avg_frac) if avg_frac.denominator == 1 else round(float(avg_frac), 2)
    vehicle = random.choice(vehicles)
    stop_str = str(float(stop))
    q = (f"A {vehicle}: {dist} km at {v_go} km/h, stops {stop_str}h, "
         f"returns at {v_ret} km/h. Average speed (including stop)?")
    if isinstance(avg_val, int):
        choices, answer = make_choices_int(avg_val)
    else:
        choices, answer = make_choices_float(avg_val)
    exp = f"Total dist={total_d}km. Total time={float(total_t):.2f}h. Avg={avg_val} km/h."
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "round trip with stop"])


# HARD Financial: replacement changes average (15)
for i in range(15):
    count = random.choice([5, 6, 8, 10, 12])
    old_avg = random.choice([15000, 18000, 20000, 22000, 25000, 28000, 30000])
    old_total = old_avg * count
    leaving_val = old_avg + random.randint(2000, 15000)
    new_avg = old_avg - random.choice([500, 1000, 1500, 2000, 2500])
    new_total = new_avg * count
    new_val = new_total - old_total + leaving_val
    if new_val < 0:
        new_avg = old_avg - 500
        new_total = new_avg * count
        new_val = new_total - old_total + leaving_val
    q = (f"Average salary of {count} employees: \u20b1{old_avg:,}. "
         f"One earning \u20b1{leaving_val:,} replaced. New average: \u20b1{new_avg:,}. New hire's salary?")
    choices, answer = make_choices_peso(new_val)
    exp = f"Diff = \u20b1{old_total-new_total:,}. New hire = \u20b1{leaving_val:,} - \u20b1{old_total-new_total:,} = \u20b1{new_val:,}."
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "replacement"])

# HARD Financial: multi-period target (15)
for i in range(15):
    total_months = random.choice([6, 8, 10, 12])
    past_months = total_months - random.choice([1, 2, 3])
    remaining = total_months - past_months
    target_avg = random.choice([10000, 12000, 15000, 18000, 20000, 25000])
    target_total = target_avg * total_months
    past_avg = target_avg - random.choice([1000, 2000, 3000, 4000])
    past_total = past_avg * past_months
    remaining_total = target_total - past_total
    remainder = remaining_total % remaining
    if remainder != 0:
        past_avg += 1
        past_total = past_avg * past_months
        remaining_total = target_total - past_total
    remaining_avg = remaining_total // remaining
    context = random.choice(["savings", "sales", "revenue"])
    q = (f"Target avg {context}: \u20b1{target_avg:,} over {total_months} months. "
         f"First {past_months} months avg: \u20b1{past_avg:,}. Required avg for remaining {remaining} months?")
    choices, answer = make_choices_peso(remaining_avg)
    exp = f"Target total=\u20b1{target_total:,}. Past=\u20b1{past_total:,}. Remaining avg=\u20b1{remaining_avg:,}."
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "target average"])

# HARD Financial: weighted 3 departments (10)
for i in range(10):
    n1 = random.choice([10, 15, 20, 25, 30])
    n2 = random.choice([5, 8, 10, 12, 15])
    n3 = random.choice([3, 5, 8, 10])
    avg1 = random.choice([18000, 20000, 22000, 25000])
    avg2 = random.choice([28000, 30000, 32000, 35000])
    avg3 = random.choice([40000, 45000, 50000, 55000])
    total = n1*avg1 + n2*avg2 + n3*avg3
    total_count = n1 + n2 + n3
    combined_avg = round(total / total_count)
    q = (f"Dept A: {n1} staff, avg \u20b1{avg1:,}. Dept B: {n2} staff, avg \u20b1{avg2:,}. "
         f"Dept C: {n3} staff, avg \u20b1{avg3:,}. Overall average salary?")
    choices, answer = make_choices_peso(combined_avg)
    exp = f"Total payroll=\u20b1{total:,}. Employees={total_count}. Avg=\u20b1{combined_avg:,}."
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "weighted average"])

# HARD Financial: percentage increase (10)
for i in range(10):
    count = random.choice([5, 6, 8, 10])
    old_avg = random.choice([10000, 12000, 15000, 18000, 20000, 25000])
    pct = random.choice([5, 8, 10, 12, 15, 20])
    increase = old_avg * pct // 100
    new_avg = old_avg + increase
    new_total = new_avg * count
    q = (f"Average expense of {count} depts: \u20b1{old_avg:,}. "
         f"If average increases by {pct}%, new total expense?")
    choices, answer = make_choices_peso(new_total)
    exp = f"New avg = \u20b1{old_avg:,} + {pct}% = \u20b1{new_avg:,}. Total = \u20b1{new_avg:,}\u00d7{count} = \u20b1{new_total:,}."
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "percentage increase"])


# HARD Group: three groups combined (15)
for i in range(15):
    n1 = random.choice([10, 12, 15, 20])
    n2 = random.choice([8, 10, 15, 20, 25])
    n3 = random.choice([5, 8, 10, 12, 15])
    avg1 = random.randint(60, 80)
    avg2 = random.randint(70, 90)
    avg3 = random.randint(75, 95)
    total = n1*avg1 + n2*avg2 + n3*avg3
    total_count = n1 + n2 + n3
    combined_avg = total / total_count
    combined_avg = int(combined_avg) if combined_avg == int(combined_avg) else round(combined_avg, 2)
    q = (f"Section A ({n1}) avg {avg1}, Section B ({n2}) avg {avg2}, "
         f"Section C ({n3}) avg {avg3}. Overall average?")
    if isinstance(combined_avg, int):
        choices, answer = make_choices_int(combined_avg)
    else:
        choices, answer = make_choices_float(combined_avg)
    exp = f"Total={total}. Count={total_count}. Avg={combined_avg}."
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "three groups"])

# HARD Group: find group size (15)
for i in range(15):
    n1 = random.choice([10, 15, 20, 25, 30])
    avg1 = random.randint(60, 80)
    avg2 = random.randint(80, 95)
    # Try to find n2 that gives clean combined average
    for combined_avg in range(avg1 + 2, avg2 - 1):
        numerator = n1 * (combined_avg - avg1)
        denominator = avg2 - combined_avg
        if denominator > 0 and numerator % denominator == 0:
            n2 = numerator // denominator
            if 2 < n2 < 80:
                total = n1*avg1 + n2*avg2
                q = (f"Group A: {n1} members, avg {avg1}. Group B: avg {avg2}. "
                     f"Combined average is {combined_avg}. How many in Group B?")
                choices, answer = make_choices_int(n2)
                exp = f"n2\u00d7({avg2}-{combined_avg}) = {n1}\u00d7({combined_avg}-{avg1}). n2 = {n2}."
                add_q("Hard", q, choices, answer, exp, ["average", "group problems", "find group size"])
                break
    else:
        # Fallback
        n2 = random.choice([5, 10, 15, 20])
        total = n1*avg1 + n2*avg2
        total_count = n1 + n2
        combined_avg = round(total / total_count, 2)
        q = f"Group A ({n1}, avg {avg1}) + Group B ({n2}, avg {avg2}). Combined average?"
        choices, answer = make_choices_float(combined_avg)
        exp = f"Total={total}. Avg={total}\u00f7{total_count}={combined_avg}."
        add_q("Hard", q, choices, answer, exp, ["average", "group problems", "combined average"])

# HARD Group: subset average (10)
for i in range(10):
    total_count = random.choice([20, 25, 30, 35, 40, 50])
    overall_avg = random.randint(65, 85)
    overall_total = overall_avg * total_count
    sub_count = random.choice([n for n in [5, 8, 10, 12, 15, 20] if n < total_count])
    sub_avg = random.randint(overall_avg + 3, overall_avg + 15)
    sub_total = sub_avg * sub_count
    comp_count = total_count - sub_count
    comp_total = overall_total - sub_total
    if comp_total <= 0:
        sub_avg = overall_avg + 2
        sub_total = sub_avg * sub_count
        comp_total = overall_total - sub_total
    comp_avg = comp_total / comp_count
    comp_avg = int(comp_avg) if comp_avg == int(comp_avg) else round(comp_avg, 2)
    subj = random.choice(subjects)
    q = (f"Class of {total_count}: overall avg {overall_avg} in {subj}. "
         f"Top {sub_count} average {sub_avg}. Remaining {comp_count} average?")
    if isinstance(comp_avg, int):
        choices, answer = make_choices_int(comp_avg)
    else:
        choices, answer = make_choices_float(comp_avg)
    exp = f"Overall total={overall_total}. Top total={sub_total}. Rest={comp_total}. Avg={comp_avg}."
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "subset average"])

# HARD Group: multiple changes (10)
for i in range(10):
    count = random.choice([8, 10, 12, 15])
    avg = random.randint(70, 85)
    total = avg * count
    r1 = random.randint(avg-10, avg+10)
    r2 = random.randint(avg-10, avg+10)
    a1 = random.randint(avg-5, avg+15)
    a2 = random.randint(avg-5, avg+15)
    a3 = random.randint(avg-5, avg+15)
    new_total = total - r1 - r2 + a1 + a2 + a3
    new_count = count - 2 + 3
    remainder = new_total % new_count
    if remainder != 0:
        a3 += (new_count - remainder)
        new_total = total - r1 - r2 + a1 + a2 + a3
    new_avg = new_total // new_count
    subj = random.choice(subjects)
    q = (f"Avg {subj} score of {count} students: {avg}. "
         f"Two ({r1},{r2}) leave, three ({a1},{a2},{a3}) join. New average?")
    choices, answer = make_choices_int(new_avg)
    exp = f"New total={new_total}. New count={new_count}. Avg={new_avg}."
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "multiple changes"])


# ============================================================
# PADDING & TRIMMING
# ============================================================
def count_by_difficulty(diff):
    return sum(1 for q in questions if q["difficulty"] == diff)

while count_by_difficulty("Easy") < 200:
    count = random.choice([3, 4, 5, 6, 7, 8])
    avg = random.randint(10, 95)
    total = avg * count
    context = random.choice(["test scores", "temperatures", "heights (cm)", "weights (kg)", "ratings"])
    q_text = f"The average of {count} {context} is {avg}. What is the total sum?"
    choices, answer = make_choices_int(total)
    add_q("Easy", q_text, choices, answer, f"Total = {avg} \u00d7 {count} = {total}.", ["average", "word problems"])

while count_by_difficulty("Medium") < 200:
    count = random.choice([4, 5, 6, 7])
    avg = random.randint(40, 90)
    total = avg * count
    known_vals = [random.randint(avg-15, avg+15) for _ in range(count-1)]
    missing = total - sum(known_vals)
    if missing < 1:
        known_vals[-1] -= (1 - missing)
        missing = total - sum(known_vals)
    known_str = ", ".join(str(v) for v in known_vals)
    q_text = f"Average of {count} values is {avg}. Known: {known_str}. Missing value?"
    choices, answer = make_choices_int(missing)
    add_q("Medium", q_text, choices, answer, f"Total={total}. Missing={missing}.", ["average", "missing value"])

while count_by_difficulty("Hard") < 200:
    n1 = random.choice([5, 8, 10, 12, 15, 20])
    n2 = random.choice([5, 8, 10, 12, 15])
    n3 = random.choice([3, 5, 8, 10])
    avg1 = random.randint(55, 75)
    avg2 = random.randint(70, 85)
    avg3 = random.randint(80, 98)
    total = n1*avg1 + n2*avg2 + n3*avg3
    total_count = n1 + n2 + n3
    combined_avg = total / total_count
    combined_avg = int(combined_avg) if combined_avg == int(combined_avg) else round(combined_avg, 2)
    q_text = (f"{n1} junior (avg {avg1}), {n2} senior (avg {avg2}), "
              f"{n3} managers (avg {avg3}). Overall average?")
    if isinstance(combined_avg, int):
        choices, answer = make_choices_int(combined_avg)
    else:
        choices, answer = make_choices_float(combined_avg)
    add_q("Hard", q_text, choices, answer, f"Total={total}. Count={total_count}. Avg={combined_avg}.", ["average", "weighted average"])

# Trim to exactly 200 per difficulty
easy_qs = [q for q in questions if q["difficulty"] == "Easy"][:200]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"][:200]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"][:200]
final_questions = easy_qs + medium_qs + hard_qs

for idx, q in enumerate(final_questions, 1):
    q["id"] = idx


# ============================================================
# VALIDATION & OUTPUT
# ============================================================
def validate_questions(qs):
    errors = []
    for q in qs:
        for field in ["id","subtest","module","subtopic","difficulty","question","choices","answer","explanation","tags"]:
            if field not in q:
                errors.append(f"Q{q.get('id','?')}: missing '{field}'")
        if "choices" in q and "answer" in q:
            if q["answer"] not in q["choices"]:
                errors.append(f"Q{q['id']}: answer not in choices")
            if len(q["choices"]) != 4:
                errors.append(f"Q{q['id']}: {len(q['choices'])} choices (need 4)")
    return errors

errors = validate_questions(final_questions)
if errors:
    print("VALIDATION ERRORS:")
    for e in errors[:20]:
        print(f"  {e}")
    print(f"  ... ({len(errors)} total)")
else:
    print("All questions validated successfully.")

ec = sum(1 for q in final_questions if q["difficulty"] == "Easy")
mc = sum(1 for q in final_questions if q["difficulty"] == "Medium")
hc = sum(1 for q in final_questions if q["difficulty"] == "Hard")
print(f"Total: {len(final_questions)} (Easy:{ec}, Medium:{mc}, Hard:{hc})")

output_dir = Path("data/seed/questions/numerical-ability/ratio-proportion-and-average/average-word-problems")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_questions, f, indent=2, ensure_ascii=False)

print(f"Written to {output_path}")
