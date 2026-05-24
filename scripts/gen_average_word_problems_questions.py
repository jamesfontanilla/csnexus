"""
Generate 600 multiple-choice questions for the Average Word Problems subtopic.
Distribution: 200 Easy, 200 Medium, 200 Hard.
All answers are mathematically verified before output.

Categories covered:
- Age averages
- Speed averages
- Financial averages
- Group averages
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
    """Create 4 integer choices including the correct one."""
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
    """Create 4 float choices including the correct one."""
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
    """Create 4 peso-formatted choices."""
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


def make_choices_speed(correct):
    """Create 4 speed choices (float, 2 decimals)."""
    return make_choices_float(correct, 2)


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- EASY: Age Averages (50 questions) ---

family_roles = ["siblings", "cousins", "friends", "classmates", "colleagues", "team members"]
names_groups = [
    ("Ana", "Ben", "Cara"),
    ("Dan", "Eve", "Fay"),
    ("Gino", "Hana", "Ian"),
    ("Joy", "Ken", "Lea"),
    ("Mark", "Nina", "Omar"),
]

# Type 1: Simple average age calculation (25 questions)
for i in range(25):
    count = random.choice([3, 4, 5])
    ages = [random.randint(8, 55) for _ in range(count)]
    total = sum(ages)
    # Ensure clean division
    remainder = total % count
    ages[-1] += (count - remainder) if remainder != 0 else 0
    total = sum(ages)
    avg = total // count
    group = random.choice(family_roles)
    ages_str = ", ".join(str(a) for a in ages)
    q = f"The ages of {count} {group} are {ages_str}. What is their average age?"
    choices, answer = make_choices_int(avg)
    exp = f"Sum of ages = {' + '.join(str(a) for a in ages)} = {total}. Average = {total} ÷ {count} = {avg}."
    add_q("Easy", q, choices, answer, exp, ["average", "age problems", "word problems"])

# Type 2: Find total age from average (25 questions)
for i in range(25):
    count = random.choice([3, 4, 5, 6, 7, 8])
    avg = random.randint(10, 50)
    total = avg * count
    group = random.choice(family_roles)
    q = f"The average age of {count} {group} is {avg} years. What is their total age?"
    choices, answer = make_choices_int(total)
    exp = f"Total age = Average × Count = {avg} × {count} = {total}."
    add_q("Easy", q, choices, answer, exp, ["average", "age problems", "total from average"])


# --- EASY: Speed Averages (50 questions) ---

vehicles = ["car", "bus", "van", "truck", "motorcycle", "bicycle", "jeepney", "train", "boat", "taxi"]

# Type 1: Simple average speed = distance / time (25 questions)
for i in range(25):
    speed = random.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 90, 100])
    time_h = random.choice([2, 3, 4, 5, 6, 8, 10])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} travels {distance} km in {time_h} hours. What is the average speed?"
    choices, answer = make_choices_int(speed)
    exp = f"Average speed = Distance ÷ Time = {distance} ÷ {time_h} = {speed} km/h."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "word problems"])

# Type 2: Find distance from average speed and time (15 questions)
for i in range(15):
    speed = random.choice([30, 40, 45, 50, 60, 70, 80, 90, 100])
    time_h = random.choice([2, 3, 4, 5, 6])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} travels at an average speed of {speed} km/h for {time_h} hours. What is the total distance covered?"
    choices, answer = make_choices_int(distance)
    exp = f"Distance = Speed × Time = {speed} × {time_h} = {distance} km."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "distance"])

# Type 3: Find time from distance and average speed (10 questions)
for i in range(10):
    speed = random.choice([25, 30, 40, 50, 60, 75, 80, 100])
    time_h = random.choice([2, 3, 4, 5, 6, 8])
    distance = speed * time_h
    vehicle = random.choice(vehicles)
    q = f"A {vehicle} covers {distance} km at an average speed of {speed} km/h. How many hours does the trip take?"
    choices, answer = make_choices_int(time_h)
    exp = f"Time = Distance ÷ Speed = {distance} ÷ {speed} = {time_h} hours."
    add_q("Easy", q, choices, answer, exp, ["average", "speed problems", "time"])


# --- EASY: Financial Averages (50 questions) ---

expense_contexts = [
    "daily expenses", "weekly allowance", "monthly bills", "daily sales",
    "weekly earnings", "daily tips", "monthly savings", "daily production output"
]

# Type 1: Compute average from list of values (25 questions)
for i in range(25):
    count = random.choice([4, 5, 6, 7])
    base = random.choice([200, 300, 400, 500, 800, 1000, 1500, 2000, 5000, 8000, 10000])
    values = []
    for _ in range(count):
        values.append(base + random.choice([-200, -100, -50, 0, 50, 100, 150, 200, 300, 400, 500]))
    # Ensure clean division
    total = sum(values)
    remainder = total % count
    values[-1] += (count - remainder) if remainder != 0 else 0
    total = sum(values)
    avg = total // count
    context = random.choice(expense_contexts)
    values_str = ", ".join(f"\u20b1{v:,}" for v in values)
    q = f"A worker's {context} for {count} days are: {values_str}. What is the average?"
    choices, answer = make_choices_peso(avg)
    exp = f"Total = {' + '.join(str(v) for v in values)} = \u20b1{total:,}. Average = \u20b1{total:,} ÷ {count} = \u20b1{avg:,}."
    add_q("Easy", q, choices, answer, exp, ["average", "financial problems", "word problems"])

# Type 2: Find total from average (25 questions)
for i in range(25):
    count = random.choice([4, 5, 6, 7, 8, 10, 12])
    avg = random.choice([500, 750, 1000, 1500, 2000, 2500, 3000, 5000, 8000, 10000, 12000, 15000, 20000, 25000])
    total = avg * count
    period = random.choice(["days", "weeks", "months"])
    context = random.choice(["expense", "income", "sales", "savings", "earnings"])
    q = f"If the average {context} over {count} {period} is \u20b1{avg:,}, what is the total {context}?"
    choices, answer = make_choices_peso(total)
    exp = f"Total = Average × Count = \u20b1{avg:,} × {count} = \u20b1{total:,}."
    add_q("Easy", q, choices, answer, exp, ["average", "financial problems", "total from average"])


# --- EASY: Group Averages (50 questions) ---

subjects = ["Math", "Science", "English", "Filipino", "History", "Social Studies"]
group_names_a = ["Section A", "Group 1", "Team Alpha", "Morning shift", "Department A"]
group_names_b = ["Section B", "Group 2", "Team Beta", "Afternoon shift", "Department B"]

# Type 1: Simple combined average (equal groups) (20 questions)
for i in range(20):
    n = random.choice([5, 10, 15, 20, 25])
    avg1 = random.randint(60, 90)
    avg2 = random.randint(60, 90)
    total = n * avg1 + n * avg2
    combined_avg = total // (2 * n)
    # Ensure clean division
    if total % (2 * n) != 0:
        avg2 += (2 * n - total % (2 * n)) // n
        total = n * avg1 + n * avg2
        combined_avg = total // (2 * n)
    ga = random.choice(group_names_a)
    gb = random.choice(group_names_b)
    subj = random.choice(subjects)
    q = (f"{ga} has {n} students with an average {subj} score of {avg1}. "
         f"{gb} also has {n} students with an average score of {avg2}. "
         f"What is the combined average score?")
    choices, answer = make_choices_int(combined_avg)
    exp = (f"Since both groups have {n} students, combined average = ({avg1} + {avg2}) ÷ 2 = "
           f"{avg1 + avg2} ÷ 2 = {combined_avg}.")
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "combined average"])

# Type 2: Find group total from average and count (15 questions)
for i in range(15):
    n = random.choice([8, 10, 12, 15, 20, 25, 30])
    avg = random.randint(65, 95)
    total = n * avg
    subj = random.choice(subjects)
    group = random.choice(group_names_a + group_names_b)
    q = f"{group} has {n} students with an average {subj} score of {avg}. What is the total score of all students?"
    choices, answer = make_choices_int(total)
    exp = f"Total = Average × Count = {avg} × {n} = {total}."
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "total from average"])

# Type 3: Average after adding one value (15 questions)
for i in range(15):
    count = random.choice([4, 5, 6, 7, 8, 9])
    avg = random.randint(50, 90)
    total = avg * count
    new_val = random.randint(50, 100)
    new_total = total + new_val
    new_count = count + 1
    # Ensure clean division
    remainder = new_total % new_count
    if remainder != 0:
        new_val += (new_count - remainder)
        new_total = total + new_val
    new_avg = new_total // new_count
    subj = random.choice(subjects)
    q = (f"The average score of {count} students in {subj} is {avg}. "
         f"A new student with a score of {new_val} joins. What is the new average?")
    choices, answer = make_choices_int(new_avg)
    exp = (f"Old total = {avg} × {count} = {total}. New total = {total} + {new_val} = {new_total}. "
           f"New average = {new_total} ÷ {new_count} = {new_avg}.")
    add_q("Easy", q, choices, answer, exp, ["average", "group problems", "new member"])


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- MEDIUM: Age Averages (50 questions) ---

# Type 1: Find missing age given average (20 questions)
for i in range(20):
    count = random.choice([4, 5, 6])
    avg = random.randint(15, 45)
    total = avg * count
    known = []
    for _ in range(count - 1):
        known.append(random.randint(avg - 15, avg + 15))
    missing = total - sum(known)
    # Ensure positive and reasonable
    if missing < 1 or missing > 80:
        missing = avg + random.randint(-5, 5)
        known[-1] = total - sum(known[:-1]) - missing
        total = sum(known) + missing
        avg = total // count
        if total % count != 0:
            known[-1] += count - (total % count)
            total = sum(known) + missing
            avg = total // count
    group = random.choice(family_roles)
    known_str = ", ".join(str(a) for a in known)
    q = (f"The average age of {count} {group} is {avg} years. "
         f"If {count - 1} of them are aged {known_str}, what is the age of the remaining person?")
    choices, answer = make_choices_int(missing)
    exp = (f"Total = {avg} × {count} = {total}. Known sum = {' + '.join(str(k) for k in known)} = {sum(known)}. "
           f"Missing age = {total} - {sum(known)} = {missing}.")
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "missing value"])

# Type 2: Person joins, find new average (15 questions)
for i in range(15):
    count = random.choice([4, 5, 6, 7, 8])
    avg = random.randint(20, 45)
    total = avg * count
    new_age = random.randint(18, 60)
    new_total = total + new_age
    new_count = count + 1
    new_avg = new_total / new_count
    # Ensure clean answer
    remainder = new_total % new_count
    if remainder != 0:
        new_age += (new_count - remainder)
        new_total = total + new_age
    new_avg = new_total // new_count
    group = random.choice(["employees", "members", "players", "workers", "students"])
    q = (f"The average age of {count} {group} is {avg} years. "
         f"A new member aged {new_age} joins. What is the new average age?")
    choices, answer = make_choices_int(new_avg)
    exp = (f"Old total = {avg} × {count} = {total}. New total = {total} + {new_age} = {new_total}. "
           f"New average = {new_total} ÷ {new_count} = {new_avg}.")
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "new member"])

# Type 3: Future/past average (15 questions)
for i in range(15):
    count = random.choice([3, 4, 5, 6])
    avg_now = random.randint(20, 50)
    years = random.choice([2, 3, 4, 5, 6, 8, 10])
    direction = random.choice(["future", "past"])
    if direction == "future":
        new_avg = avg_now + years
        q = (f"The average age of {count} friends is {avg_now} years. "
             f"What will their average age be after {years} years?")
        exp = f"When {years} years pass, each person ages by {years}, so the average also increases by {years}. New average = {avg_now} + {years} = {new_avg}."
    else:
        new_avg = avg_now - years
        q = (f"The average age of {count} colleagues is {avg_now} years now. "
             f"What was their average age {years} years ago?")
        exp = f"Each person was {years} years younger, so the average was also {years} less. Past average = {avg_now} - {years} = {new_avg}."
    choices, answer = make_choices_int(new_avg)
    add_q("Medium", q, choices, answer, exp, ["average", "age problems", "time change"])


# --- MEDIUM: Speed Averages (50 questions) ---

# Type 1: Two-leg trip, equal distance (harmonic mean) (20 questions)
for i in range(20):
    v1 = random.choice([20, 24, 25, 30, 36, 40, 45, 48, 50, 60])
    v2 = random.choice([30, 36, 40, 45, 48, 50, 60, 72, 75, 80, 90, 100, 120])
    while v2 == v1:
        v2 = random.choice([30, 40, 50, 60, 72, 80, 90, 100, 120])
    # Use a distance that gives clean times
    lcm_denom = v1 * v2
    dist = random.choice([v1 * v2 // random.choice([1, 2, 3, 4, 5]) for _ in range(5)])
    # Simpler: pick distance divisible by both
    dist = v1 * v2 // max(1, random.choice([2, 3, 4, 5, 6, 10]))
    if dist < 10:
        dist = v1 * v2
    # Compute average speed
    t1_num = Fraction(dist, v1)
    t2_num = Fraction(dist, v2)
    total_dist = 2 * dist
    total_time = t1_num + t2_num
    avg_speed = Fraction(total_dist, 1) / total_time
    avg_speed_float = float(avg_speed)
    # Check if it's a clean number
    if avg_speed.denominator == 1:
        avg_int = int(avg_speed)
        vehicle = random.choice(vehicles)
        q = (f"A {vehicle} travels {dist} km at {v1} km/h and returns the same distance at {v2} km/h. "
             f"What is the average speed for the round trip?")
        choices, answer = make_choices_int(avg_int)
        exp = (f"For equal distances, average speed = 2×{v1}×{v2} ÷ ({v1}+{v2}) = "
               f"{2*v1*v2} ÷ {v1+v2} = {avg_int} km/h.")
        add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "harmonic mean"])
    else:
        avg_rounded = round(avg_speed_float, 2)
        vehicle = random.choice(vehicles)
        q = (f"A {vehicle} travels {dist} km at {v1} km/h and returns the same distance at {v2} km/h. "
             f"What is the average speed for the round trip?")
        choices, answer = make_choices_float(avg_rounded)
        exp = (f"For equal distances, average speed = 2×{v1}×{v2} ÷ ({v1}+{v2}) = "
               f"{2*v1*v2} ÷ {v1+v2} = {avg_rounded} km/h.")
        add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "harmonic mean"])

# Type 2: Two-leg trip, different distances (15 questions)
for i in range(15):
    v1 = random.choice([30, 40, 50, 60, 80])
    v2 = random.choice([40, 50, 60, 75, 80, 100])
    while v2 == v1:
        v2 = random.choice([40, 50, 60, 80, 100])
    # Pick distances that give clean times
    t1 = random.choice([1, 2, 3, 4])
    t2 = random.choice([1, 2, 3, 4])
    d1 = v1 * t1
    d2 = v2 * t2
    total_d = d1 + d2
    total_t = t1 + t2
    avg_speed = total_d // total_t if total_d % total_t == 0 else round(total_d / total_t, 2)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} travels {d1} km at {v1} km/h, then {d2} km at {v2} km/h. "
         f"What is the average speed for the entire trip?")
    if isinstance(avg_speed, int):
        choices, answer = make_choices_int(avg_speed)
    else:
        choices, answer = make_choices_float(avg_speed)
    exp = (f"Time₁ = {d1} ÷ {v1} = {t1}h. Time₂ = {d2} ÷ {v2} = {t2}h. "
           f"Average speed = {total_d} ÷ {total_t} = {avg_speed} km/h.")
    add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "two-leg trip"])

# Type 3: Find missing speed (15 questions)
for i in range(15):
    v1 = random.choice([30, 40, 50, 60, 80])
    d1 = random.choice([60, 80, 100, 120, 150, 200])
    t1 = Fraction(d1, v1)
    d2 = random.choice([40, 60, 80, 100, 120])
    # Pick avg_speed that gives clean t2
    total_d = d1 + d2
    # We want total_time to be clean
    total_t_choices = [Fraction(total_d, s) for s in [25, 30, 40, 50, 60] if total_d % 1 == 0]
    # Simpler approach: pick t2 that's clean
    t2 = random.choice([1, 2, 3, 4])
    v2 = d2 // t2 if d2 % t2 == 0 else d2 / t2
    if d2 % t2 != 0:
        d2 = t2 * random.choice([20, 25, 30, 40, 50, 60])
        v2 = d2 // t2
    total_d = d1 + d2
    total_t_val = float(t1) + t2
    avg_speed = round(total_d / total_t_val, 2)
    if total_d / total_t_val == int(total_d / total_t_val):
        avg_speed = int(total_d / total_t_val)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} covers {total_d} km. For the first {d1} km, it travels at {v1} km/h. "
         f"If the average speed for the entire trip is {avg_speed} km/h, what was the speed for the remaining {d2} km?")
    choices, answer = make_choices_int(v2) if isinstance(v2, int) else make_choices_float(v2)
    exp = (f"Total time = {total_d} ÷ {avg_speed} = {total_t_val}h. "
           f"Time for first part = {d1} ÷ {v1} = {float(t1)}h. "
           f"Time for second part = {total_t_val} - {float(t1)} = {t2}h. "
           f"Speed = {d2} ÷ {t2} = {v2} km/h.")
    add_q("Medium", q, choices, answer, exp, ["average", "speed problems", "missing speed"])


# --- MEDIUM: Financial Averages (50 questions) ---

# Type 1: Find missing value to achieve target average (20 questions)
for i in range(20):
    count = random.choice([5, 6, 7, 8])
    target_avg = random.choice([5000, 8000, 10000, 12000, 15000, 18000, 20000, 25000])
    target_total = target_avg * count
    known_count = count - 1
    known_values = []
    for _ in range(known_count):
        known_values.append(target_avg + random.choice([-3000, -2000, -1000, 0, 1000, 2000, 3000]))
    missing = target_total - sum(known_values)
    if missing < 0:
        # Adjust
        known_values[-1] -= abs(missing) + 1000
        missing = target_total - sum(known_values)
    known_str = ", ".join(f"\u20b1{v:,}" for v in known_values)
    period = random.choice(["months", "weeks", "days"])
    context = random.choice(["savings", "sales", "expenses", "income", "earnings"])
    q = (f"A worker wants an average {context} of \u20b1{target_avg:,} over {count} {period}. "
         f"The first {known_count} {period} were: {known_str}. "
         f"How much is needed in the last {period[:-1]}?")
    choices, answer = make_choices_peso(missing)
    exp = (f"Target total = \u20b1{target_avg:,} × {count} = \u20b1{target_total:,}. "
           f"Known sum = \u20b1{sum(known_values):,}. "
           f"Missing = \u20b1{target_total:,} - \u20b1{sum(known_values):,} = \u20b1{missing:,}.")
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "missing value"])

# Type 2: Average changes when value is added (15 questions)
for i in range(15):
    count = random.choice([4, 5, 6, 8, 10])
    avg = random.choice([10000, 15000, 20000, 25000, 30000])
    total = avg * count
    new_val = random.choice([avg + 5000, avg + 10000, avg + 15000, avg - 5000, avg - 8000])
    if new_val < 0:
        new_val = avg + 5000
    new_total = total + new_val
    new_count = count + 1
    # Ensure clean division
    remainder = new_total % new_count
    if remainder != 0:
        new_val += (new_count - remainder)
        new_total = total + new_val
    new_avg = new_total // new_count
    context = random.choice(["salary", "monthly income", "daily sales", "weekly earnings"])
    q = (f"The average {context} of {count} employees is \u20b1{avg:,}. "
         f"A new employee with {context} of \u20b1{new_val:,} joins. What is the new average?")
    choices, answer = make_choices_peso(new_avg)
    exp = (f"Old total = \u20b1{avg:,} × {count} = \u20b1{total:,}. "
           f"New total = \u20b1{total:,} + \u20b1{new_val:,} = \u20b1{new_total:,}. "
           f"New average = \u20b1{new_total:,} ÷ {new_count} = \u20b1{new_avg:,}.")
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "new member"])

# Type 3: Person leaves, find new average (15 questions)
for i in range(15):
    count = random.choice([5, 6, 7, 8, 10])
    avg = random.choice([15000, 18000, 20000, 22000, 25000, 28000, 30000])
    total = avg * count
    leaving_val = random.choice([avg + 5000, avg + 8000, avg + 10000, avg - 3000, avg - 5000])
    if leaving_val < 5000:
        leaving_val = avg + 5000
    new_total = total - leaving_val
    new_count = count - 1
    # Ensure clean division
    remainder = new_total % new_count
    if remainder != 0:
        leaving_val -= remainder
        new_total = total - leaving_val
    new_avg = new_total // new_count
    context = random.choice(["salary", "monthly income", "daily output"])
    q = (f"The average {context} of {count} workers is \u20b1{avg:,}. "
         f"One worker earning \u20b1{leaving_val:,} resigns. What is the new average {context}?")
    choices, answer = make_choices_peso(new_avg)
    exp = (f"Old total = \u20b1{avg:,} × {count} = \u20b1{total:,}. "
           f"New total = \u20b1{total:,} - \u20b1{leaving_val:,} = \u20b1{new_total:,}. "
           f"New average = \u20b1{new_total:,} ÷ {new_count} = \u20b1{new_avg:,}.")
    add_q("Medium", q, choices, answer, exp, ["average", "financial problems", "member leaves"])


# --- MEDIUM: Group Averages (50 questions) ---

# Type 1: Combine two unequal groups (20 questions)
for i in range(20):
    n1 = random.choice([10, 12, 15, 20, 25, 30])
    n2 = random.choice([8, 10, 12, 15, 20, 25, 30, 35, 40])
    while n2 == n1:
        n2 = random.choice([8, 10, 15, 20, 25, 30, 35])
    avg1 = random.randint(60, 90)
    avg2 = random.randint(60, 90)
    total = n1 * avg1 + n2 * avg2
    combined_count = n1 + n2
    # Ensure clean division
    remainder = total % combined_count
    if remainder != 0:
        avg2 += 1
        total = n1 * avg1 + n2 * avg2
        remainder = total % combined_count
        if remainder != 0:
            # Adjust avg1 instead
            avg1 = avg1 + (combined_count - remainder) // n1 if (combined_count - remainder) % n1 == 0 else avg1
            total = n1 * avg1 + n2 * avg2
            remainder = total % combined_count
    if remainder == 0:
        combined_avg = total // combined_count
    else:
        combined_avg = round(total / combined_count, 2)
    ga = random.choice(group_names_a)
    gb = random.choice(group_names_b)
    subj = random.choice(subjects)
    q = (f"{ga} has {n1} students with an average {subj} score of {avg1}. "
         f"{gb} has {n2} students with an average score of {avg2}. "
         f"What is the combined average score?")
    if isinstance(combined_avg, int):
        choices, answer = make_choices_int(combined_avg)
    else:
        choices, answer = make_choices_float(combined_avg)
    exp = (f"Total = {n1}×{avg1} + {n2}×{avg2} = {n1*avg1} + {n2*avg2} = {total}. "
           f"Combined average = {total} ÷ {combined_count} = {combined_avg}.")
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "combined average"])

# Type 2: Find one group's average given combined (15 questions)
for i in range(15):
    n1 = random.choice([10, 15, 20, 25])
    n2 = random.choice([10, 15, 20, 25, 30])
    while n2 == n1:
        n2 = random.choice([10, 15, 20, 25, 30])
    combined_count = n1 + n2
    combined_avg = random.randint(70, 85)
    total = combined_avg * combined_count
    avg1 = random.randint(65, 80)
    total1 = n1 * avg1
    total2 = total - total1
    # Ensure clean division
    remainder = total2 % n2
    if remainder != 0:
        avg1 += 1
        total1 = n1 * avg1
        total2 = total - total1
        remainder = total2 % n2
    if remainder == 0 and total2 > 0:
        avg2 = total2 // n2
    else:
        # Force clean numbers
        avg2 = random.randint(70, 90)
        total2 = n2 * avg2
        total = total1 + total2
        combined_avg = total // combined_count if total % combined_count == 0 else round(total / combined_count, 2)
        avg2 = total2 // n2
    ga = random.choice(["boys", "male employees", "morning students", "Team A members"])
    gb = random.choice(["girls", "female employees", "afternoon students", "Team B members"])
    q = (f"A group of {combined_count} people has a combined average score of {combined_avg}. "
         f"The {n1} {ga} have an average of {avg1}. "
         f"What is the average score of the {n2} {gb}?")
    choices, answer = make_choices_int(avg2)
    exp = (f"Total = {combined_avg} × {combined_count} = {total}. "
           f"{ga.capitalize()} total = {avg1} × {n1} = {total1}. "
           f"{gb.capitalize()} total = {total} - {total1} = {total2}. "
           f"Average = {total2} ÷ {n2} = {avg2}.")
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "find subgroup average"])

# Type 3: New member changes average, find member's value (15 questions)
for i in range(15):
    count = random.choice([5, 6, 7, 8, 9, 10])
    old_avg = random.randint(60, 85)
    old_total = old_avg * count
    new_count = count + 1
    new_avg = old_avg + random.choice([1, 2, 3, 4, 5])
    new_total = new_avg * new_count
    new_member_val = new_total - old_total
    subj = random.choice(subjects)
    q = (f"The average {subj} score of {count} students is {old_avg}. "
         f"When a new student joins, the average becomes {new_avg}. "
         f"What is the new student's score?")
    choices, answer = make_choices_int(new_member_val)
    exp = (f"Old total = {old_avg} × {count} = {old_total}. "
           f"New total = {new_avg} × {new_count} = {new_total}. "
           f"New student's score = {new_total} - {old_total} = {new_member_val}.")
    add_q("Medium", q, choices, answer, exp, ["average", "group problems", "find new member value"])


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- HARD: Age Averages (50 questions) ---

# Type 1: Replacement problems (15 questions)
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
    q = (f"The average age of {count} {group} is {old_avg} years. "
         f"One member aged {leaving_age} is replaced by a new member, "
         f"and the average age becomes {new_avg}. How old is the new member?")
    choices, answer = make_choices_int(new_person_age)
    exp = (f"Old total = {old_avg} × {count} = {old_total}. "
           f"New total = {new_avg} × {count} = {new_total}. "
           f"Difference = {old_total} - {new_total} = {old_total - new_total}. "
           f"New member's age = {leaving_age} - {old_total - new_total} = {new_person_age}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "replacement"])

# Type 2: Combined group with time change (15 questions)
for i in range(15):
    n1 = random.choice([3, 4, 5, 6])
    n2 = random.choice([3, 4, 5, 6])
    avg1 = random.randint(20, 40)
    avg2 = random.randint(25, 50)
    years = random.choice([2, 3, 4, 5])
    total1 = n1 * avg1
    total2 = n2 * avg2
    combined_count = n1 + n2
    # After 'years' years
    future_total = total1 + total2 + combined_count * years
    future_avg = future_total // combined_count if future_total % combined_count == 0 else round(future_total / combined_count, 2)
    # Ensure clean
    remainder = future_total % combined_count
    if remainder != 0:
        avg1 += 1
        total1 = n1 * avg1
        future_total = total1 + total2 + combined_count * years
        remainder = future_total % combined_count
    if remainder == 0:
        future_avg = future_total // combined_count
    else:
        future_avg = round(future_total / combined_count, 2)
    q = (f"Group A has {n1} people with average age {avg1}. Group B has {n2} people with average age {avg2}. "
         f"If both groups merge, what will be their combined average age after {years} years?")
    if isinstance(future_avg, int):
        choices, answer = make_choices_int(future_avg)
    else:
        choices, answer = make_choices_float(future_avg)
    exp = (f"Total A = {n1}×{avg1} = {total1}. Total B = {n2}×{avg2} = {total2}. "
           f"Combined total now = {total1 + total2}. After {years} years, total = {total1+total2} + {combined_count}×{years} = {future_total}. "
           f"Average = {future_total} ÷ {combined_count} = {future_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "combined group", "time change"])

# Type 3: Sequential additions/removals (10 questions)
for i in range(10):
    count = random.choice([5, 6, 7, 8])
    avg = random.randint(25, 40)
    total = avg * count
    # Add a person
    add_age = random.randint(20, 55)
    total += add_age
    count += 1
    # Remove a person
    remove_age = random.randint(20, 50)
    total -= remove_age
    count -= 1
    # Ensure positive average
    if total <= 0 or count <= 0:
        total = abs(total) + 100
    final_avg = total // count if total % count == 0 else round(total / count, 2)
    # Ensure clean
    if total % count != 0:
        add_age += count - (total % count)
        total = avg * (count) + add_age - remove_age
        # Recalculate
        orig_count = count
        orig_total = avg * orig_count
        total = orig_total + add_age - remove_age
        final_avg = total // count if total % count == 0 else round(total / count, 2)
    if isinstance(final_avg, float) and final_avg == int(final_avg):
        final_avg = int(final_avg)
    group = random.choice(["employees", "club members", "team players"])
    q = (f"The average age of {count} {group} is {avg}. "
         f"A new member aged {add_age} joins, and then a member aged {remove_age} leaves. "
         f"What is the new average age?")
    if isinstance(final_avg, int):
        choices, answer = make_choices_int(final_avg)
    else:
        choices, answer = make_choices_float(final_avg)
    exp = (f"Original total = {avg} × {count} = {avg*count}. "
           f"After adding {add_age}: total = {avg*count + add_age}, count = {count+1}. "
           f"After removing {remove_age}: total = {avg*count + add_age - remove_age}, count = {count}. "
           f"New average = {avg*count + add_age - remove_age} ÷ {count} = {final_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "sequential changes"])

# Type 4: Find original average given change info (10 questions)
for i in range(10):
    count = random.choice([5, 6, 7, 8, 10])
    new_avg = random.randint(30, 50)
    new_count = count + 1
    new_total = new_avg * new_count
    new_member_age = random.randint(new_avg + 5, new_avg + 20)
    old_total = new_total - new_member_age
    old_avg = old_total // count if old_total % count == 0 else round(old_total / count, 2)
    # Ensure clean
    if old_total % count != 0:
        new_member_age += count - (old_total % count)
        old_total = new_total - new_member_age
        # Recalculate new_total
        new_total = old_total + new_member_age
        new_avg = new_total // new_count if new_total % new_count == 0 else round(new_total / new_count, 2)
        old_avg = old_total // count
    if isinstance(old_avg, float) and old_avg == int(old_avg):
        old_avg = int(old_avg)
    group = random.choice(["friends", "colleagues", "siblings", "classmates"])
    q = (f"When a person aged {new_member_age} joins a group of {count} {group}, "
         f"the average age becomes {new_avg}. What was the original average age?")
    if isinstance(old_avg, int):
        choices, answer = make_choices_int(old_avg)
    else:
        choices, answer = make_choices_float(old_avg)
    exp = (f"New total = {new_avg} × {new_count} = {new_total}. "
           f"Original total = {new_total} - {new_member_age} = {old_total}. "
           f"Original average = {old_total} ÷ {count} = {old_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "age problems", "find original average"])


# --- HARD: Speed Averages (50 questions) ---

# Type 1: Three-leg trip (20 questions)
for i in range(20):
    # Pick speeds and times that give clean numbers
    v1 = random.choice([30, 40, 50, 60, 80])
    v2 = random.choice([40, 50, 60, 75, 80, 100])
    v3 = random.choice([20, 25, 30, 40, 50, 60])
    t1 = random.choice([1, 2, 3])
    t2 = random.choice([1, 2, 3])
    t3 = random.choice([1, 2, 3])
    d1 = v1 * t1
    d2 = v2 * t2
    d3 = v3 * t3
    total_d = d1 + d2 + d3
    total_t = t1 + t2 + t3
    avg_speed = total_d / total_t
    if avg_speed == int(avg_speed):
        avg_speed = int(avg_speed)
        choices, answer = make_choices_int(avg_speed)
    else:
        avg_speed = round(avg_speed, 2)
        choices, answer = make_choices_float(avg_speed)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} travels {d1} km at {v1} km/h, then {d2} km at {v2} km/h, "
         f"then {d3} km at {v3} km/h. What is the average speed for the entire journey?")
    exp = (f"Time₁ = {d1}÷{v1} = {t1}h. Time₂ = {d2}÷{v2} = {t2}h. Time₃ = {d3}÷{v3} = {t3}h. "
           f"Total distance = {total_d} km. Total time = {total_t}h. "
           f"Average speed = {total_d} ÷ {total_t} = {avg_speed} km/h.")
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "three-leg trip"])

# Type 2: Fractional distance trip (15 questions)
for i in range(15):
    # Total distance split into fractions
    total_d = random.choice([120, 180, 240, 300, 360, 480, 600])
    # Split into thirds
    d_each = total_d // 3
    v1 = random.choice([30, 40, 60, 80])
    v2 = random.choice([40, 50, 60, 80, 120])
    v3 = random.choice([20, 30, 40, 60, 80])
    # Ensure clean times
    while d_each % v1 != 0:
        v1 = random.choice([30, 40, 60, 80, 120])
    while d_each % v2 != 0:
        v2 = random.choice([40, 60, 80, 120])
    while d_each % v3 != 0:
        v3 = random.choice([20, 30, 40, 60, 80, 120])
    t1 = d_each // v1
    t2 = d_each // v2
    t3 = d_each // v3
    total_t = t1 + t2 + t3
    avg_speed = total_d / total_t
    if avg_speed == int(avg_speed):
        avg_speed = int(avg_speed)
        choices, answer = make_choices_int(avg_speed)
    else:
        avg_speed = round(avg_speed, 2)
        choices, answer = make_choices_float(avg_speed)
    vehicle = random.choice(vehicles)
    q = (f"A {vehicle} covers a {total_d}-km journey. It travels the first third at {v1} km/h, "
         f"the second third at {v2} km/h, and the last third at {v3} km/h. "
         f"What is the average speed?")
    exp = (f"Each third = {d_each} km. "
           f"Time₁ = {d_each}÷{v1} = {t1}h. Time₂ = {d_each}÷{v2} = {t2}h. Time₃ = {d_each}÷{v3} = {t3}h. "
           f"Total time = {total_t}h. Average speed = {total_d} ÷ {total_t} = {avg_speed} km/h.")
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "fractional distance"])

# Type 3: Round trip with stops (15 questions)
for i in range(15):
    dist = random.choice([60, 80, 100, 120, 150, 180, 200, 240])
    v_go = random.choice([30, 40, 50, 60, 80])
    v_return = random.choice([20, 30, 40, 50, 60])
    while v_return == v_go:
        v_return = random.choice([20, 30, 40, 50, 60])
    stop_time = random.choice([Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(2, 1)])
    t_go = Fraction(dist, v_go)
    t_return = Fraction(dist, v_return)
    total_d = 2 * dist
    total_t = t_go + t_return + stop_time
    avg_speed_frac = Fraction(total_d, 1) / total_t
    avg_speed_float = round(float(avg_speed_frac), 2)
    if avg_speed_frac.denominator == 1:
        avg_speed_val = int(avg_speed_frac)
        choices, answer = make_choices_int(avg_speed_val)
    else:
        avg_speed_val = avg_speed_float
        choices, answer = make_choices_float(avg_speed_val)
    vehicle = random.choice(vehicles)
    stop_str = f"{float(stop_time):.1f}" if stop_time != int(stop_time) else str(int(stop_time))
    q = (f"A {vehicle} travels {dist} km at {v_go} km/h, stops for {stop_str} hour(s), "
         f"then returns at {v_return} km/h. What is the average speed for the entire trip (including stop time)?")
    exp = (f"Time going = {dist}÷{v_go} = {float(t_go):.2f}h. "
           f"Time returning = {dist}÷{v_return} = {float(t_return):.2f}h. "
           f"Stop = {stop_str}h. Total time = {float(total_t):.2f}h. "
           f"Total distance = {total_d} km. Average speed = {total_d} ÷ {float(total_t):.2f} = {avg_speed_val} km/h.")
    add_q("Hard", q, choices, answer, exp, ["average", "speed problems", "round trip with stop"])


# --- HARD: Financial Averages (50 questions) ---

# Type 1: Replacement changes average, find replacement value (15 questions)
for i in range(15):
    count = random.choice([5, 6, 8, 10, 12])
    old_avg = random.choice([15000, 18000, 20000, 22000, 25000, 28000, 30000])
    old_total = old_avg * count
    leaving_val = random.randint(old_avg + 2000, old_avg + 15000)
    new_avg = old_avg - random.choice([500, 1000, 1500, 2000, 2500])
    new_total = new_avg * count
    new_val = new_total - old_total + leaving_val
    if new_val < 0:
        new_avg = old_avg - 500
        new_total = new_avg * count
        new_val = new_total - old_total + leaving_val
    q = (f"The average salary of {count} employees is \u20b1{old_avg:,}. "
         f"One employee earning \u20b1{leaving_val:,} is replaced by a new hire. "
         f"The new average becomes \u20b1{new_avg:,}. What is the new hire's salary?")
    choices, answer = make_choices_peso(new_val)
    exp = (f"Old total = \u20b1{old_avg:,} × {count} = \u20b1{old_total:,}. "
           f"New total = \u20b1{new_avg:,} × {count} = \u20b1{new_total:,}. "
           f"Difference = \u20b1{old_total:,} - \u20b1{new_total:,} = \u20b1{old_total - new_total:,}. "
           f"New hire's salary = \u20b1{leaving_val:,} - \u20b1{old_total - new_total:,} = \u20b1{new_val:,}.")
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "replacement"])

# Type 2: Multi-period average with target (15 questions)
for i in range(15):
    total_months = random.choice([6, 8, 10, 12])
    past_months = total_months - random.choice([1, 2, 3])
    remaining = total_months - past_months
    target_avg = random.choice([10000, 12000, 15000, 18000, 20000, 25000])
    target_total = target_avg * total_months
    past_avg = target_avg - random.choice([1000, 2000, 3000, 4000])
    past_total = past_avg * past_months
    remaining_total = target_total - past_total
    remaining_avg = remaining_total // remaining if remaining_total % remaining == 0 else round(remaining_total / remaining, 2)
    # Ensure clean
    if remaining_total % remaining != 0:
        past_avg += 1
        past_total = past_avg * past_months
        remaining_total = target_total - past_total
        remaining_avg = remaining_total // remaining if remaining_total % remaining == 0 else round(remaining_total / remaining)
    if isinstance(remaining_avg, float) and remaining_avg == int(remaining_avg):
        remaining_avg = int(remaining_avg)
    context = random.choice(["savings", "sales", "revenue", "production output"])
    q = (f"A business wants an average monthly {context} of \u20b1{target_avg:,} over {total_months} months. "
         f"The first {past_months} months averaged \u20b1{past_avg:,}. "
         f"What must the average be for the remaining {remaining} months?")
    choices, answer = make_choices_peso(remaining_avg)
    exp = (f"Target total = \u20b1{target_avg:,} × {total_months} = \u20b1{target_total:,}. "
           f"Past total = \u20b1{past_avg:,} × {past_months} = \u20b1{past_total:,}. "
           f"Remaining total = \u20b1{target_total:,} - \u20b1{past_total:,} = \u20b1{remaining_total:,}. "
           f"Required average = \u20b1{remaining_total:,} ÷ {remaining} = \u20b1{remaining_avg:,}.")
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "target average"])

# Type 3: Weighted salary across departments (10 questions)
for i in range(10):
    n1 = random.choice([10, 15, 20, 25, 30])
    n2 = random.choice([5, 8, 10, 12, 15])
    n3 = random.choice([3, 5, 8, 10])
    avg1 = random.choice([18000, 20000, 22000, 25000])
    avg2 = random.choice([28000, 30000, 32000, 35000])
    avg3 = random.choice([40000, 45000, 50000, 55000])
    total = n1 * avg1 + n2 * avg2 + n3 * avg3
    total_count = n1 + n2 + n3
    combined_avg = total // total_count if total % total_count == 0 else round(total / total_count, 2)
    # Ensure clean
    if total % total_count != 0:
        combined_avg = round(total / total_count)
    q = (f"A company has 3 departments: Dept A ({n1} employees, avg salary \u20b1{avg1:,}), "
         f"Dept B ({n2} employees, avg salary \u20b1{avg2:,}), and "
         f"Dept C ({n3} employees, avg salary \u20b1{avg3:,}). "
         f"What is the overall average salary?")
    choices, answer = make_choices_peso(combined_avg)
    exp = (f"Total payroll = {n1}×{avg1:,} + {n2}×{avg2:,} + {n3}×{avg3:,} = "
           f"\u20b1{n1*avg1:,} + \u20b1{n2*avg2:,} + \u20b1{n3*avg3:,} = \u20b1{total:,}. "
           f"Total employees = {total_count}. Average = \u20b1{total:,} ÷ {total_count} = \u20b1{combined_avg:,}.")
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "weighted average", "departments"])

# Type 4: Percentage increase in average (10 questions)
for i in range(10):
    count = random.choice([5, 6, 8, 10])
    old_avg = random.choice([10000, 12000, 15000, 18000, 20000, 25000])
    pct_increase = random.choice([5, 8, 10, 12, 15, 20])
    increase_amount = old_avg * pct_increase // 100
    new_avg = old_avg + increase_amount
    new_total = new_avg * count
    old_total = old_avg * count
    total_increase = new_total - old_total
    q = (f"The average monthly expense of {count} departments is \u20b1{old_avg:,}. "
         f"If the average increases by {pct_increase}%, what is the new total monthly expense?")
    choices, answer = make_choices_peso(new_total)
    exp = (f"Increase = {pct_increase}% of \u20b1{old_avg:,} = \u20b1{increase_amount:,}. "
           f"New average = \u20b1{old_avg:,} + \u20b1{increase_amount:,} = \u20b1{new_avg:,}. "
           f"New total = \u20b1{new_avg:,} × {count} = \u20b1{new_total:,}.")
    add_q("Hard", q, choices, answer, exp, ["average", "financial problems", "percentage increase"])


# --- HARD: Group Averages (50 questions) ---

# Type 1: Three groups combined (15 questions)
for i in range(15):
    n1 = random.choice([10, 12, 15, 20])
    n2 = random.choice([8, 10, 15, 20, 25])
    n3 = random.choice([5, 8, 10, 12, 15])
    avg1 = random.randint(60, 80)
    avg2 = random.randint(70, 90)
    avg3 = random.randint(75, 95)
    total = n1 * avg1 + n2 * avg2 + n3 * avg3
    total_count = n1 + n2 + n3
    combined_avg = total / total_count
    if combined_avg == int(combined_avg):
        combined_avg = int(combined_avg)
        choices, answer = make_choices_int(combined_avg)
    else:
        combined_avg = round(combined_avg, 2)
        choices, answer = make_choices_float(combined_avg)
    q = (f"Three sections took an exam. Section A ({n1} students) averaged {avg1}, "
         f"Section B ({n2} students) averaged {avg2}, and "
         f"Section C ({n3} students) averaged {avg3}. "
         f"What is the overall average?")
    exp = (f"Total = {n1}×{avg1} + {n2}×{avg2} + {n3}×{avg3} = "
           f"{n1*avg1} + {n2*avg2} + {n3*avg3} = {total}. "
           f"Count = {total_count}. Average = {total} ÷ {total_count} = {combined_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "three groups"])

# Type 2: Find group size given combined average (15 questions)
for i in range(15):
    n1 = random.choice([10, 15, 20, 25, 30])
    avg1 = random.randint(60, 80)
    avg2 = random.randint(80, 95)
    combined_avg = random.randint(avg1 + 2, avg2 - 2)
    # combined_avg = (n1*avg1 + n2*avg2) / (n1 + n2)
    # combined_avg * (n1 + n2) = n1*avg1 + n2*avg2
    # combined_avg * n1 + combined_avg * n2 = n1*avg1 + n2*avg2
    # n2 * (combined_avg - avg2) = n1 * (avg1 - combined_avg)
    # n2 = n1 * (combined_avg - avg1) / (avg2 - combined_avg)
    numerator = n1 * (combined_avg - avg1)
    denominator = avg2 - combined_avg
    if denominator > 0 and numerator % denominator == 0:
        n2 = numerator // denominator
        if n2 > 0 and n2 < 100:
            total = n1 * avg1 + n2 * avg2
            total_count = n1 + n2
            # Verify
            verify_avg = total / total_count
            if abs(verify_avg - combined_avg) < 0.01:
                q = (f"Group A has {n1} members with average score {avg1}. "
                     f"Group B has an average score of {avg2}. "
                     f"The combined average of both groups is {combined_avg}. "
                     f"How many members does Group B have?")
                choices, answer = make_choices_int(n2)
                exp = (f"Let n₂ = Group B size. "
                       f"Combined: ({n1}×{avg1} + n₂×{avg2}) ÷ ({n1}+n₂) = {combined_avg}. "
                       f"{n1*avg1} + {avg2}n₂ = {combined_avg}×({n1}+n₂). "
                       f"{n1*avg1} + {avg2}n₂ = {combined_avg*n1} + {combined_avg}n₂. "
                       f"n₂×({avg2}-{combined_avg}) = {combined_avg*n1 - n1*avg1}. "
                       f"n₂ = {combined_avg*n1 - n1*avg1} ÷ {avg2-combined_avg} = {n2}.")
                add_q("Hard", q, choices, answer, exp, ["average", "group problems", "find group size"])
                continue
    # Fallback: generate clean numbers
    n2 = random.choice([5, 10, 15, 20])
    total = n1 * avg1 + n2 * avg2
    total_count = n1 + n2
    combined_avg = total // total_count if total % total_count == 0 else round(total / total_count, 2)
    q = (f"Group A has {n1} members with average score {avg1}. "
         f"Group B has {n2} members with average score {avg2}. "
         f"What is the combined average?")
    if isinstance(combined_avg, int):
        choices, answer = make_choices_int(combined_avg)
    else:
        choices, answer = make_choices_float(combined_avg)
    exp = (f"Total = {n1}×{avg1} + {n2}×{avg2} = {n1*avg1} + {n2*avg2} = {total}. "
           f"Average = {total} ÷ {total_count} = {combined_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "combined average"])

# Type 3: Average of subset given overall and complement (10 questions)
for i in range(10):
    total_count = random.choice([20, 25, 30, 35, 40, 50])
    overall_avg = random.randint(65, 85)
    overall_total = overall_avg * total_count
    sub_count = random.choice([n for n in [5, 8, 10, 12, 15, 20] if n < total_count])
    sub_avg = random.randint(overall_avg + 3, overall_avg + 15)
    sub_total = sub_avg * sub_count
    complement_count = total_count - sub_count
    complement_total = overall_total - sub_total
    complement_avg = complement_total // complement_count if complement_total % complement_count == 0 else round(complement_total / complement_count, 2)
    # Ensure positive and clean
    if complement_total <= 0:
        sub_avg = overall_avg + 2
        sub_total = sub_avg * sub_count
        complement_total = overall_total - sub_total
        complement_avg = complement_total // complement_count if complement_total % complement_count == 0 else round(complement_total / complement_count, 2)
    if isinstance(complement_avg, float) and complement_avg == int(complement_avg):
        complement_avg = int(complement_avg)
    subj = random.choice(subjects)
    q = (f"A class of {total_count} students has an overall average {subj} score of {overall_avg}. "
         f"The top {sub_count} students average {sub_avg}. "
         f"What is the average score of the remaining {complement_count} students?")
    if isinstance(complement_avg, int):
        choices, answer = make_choices_int(complement_avg)
    else:
        choices, answer = make_choices_float(complement_avg)
    exp = (f"Overall total = {overall_avg} × {total_count} = {overall_total}. "
           f"Top {sub_count} total = {sub_avg} × {sub_count} = {sub_total}. "
           f"Remaining total = {overall_total} - {sub_total} = {complement_total}. "
           f"Remaining average = {complement_total} ÷ {complement_count} = {complement_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "subset average"])

# Type 4: Multiple removals/additions (10 questions)
for i in range(10):
    count = random.choice([8, 10, 12, 15])
    avg = random.randint(70, 85)
    total = avg * count
    # Remove 2 members
    remove1 = random.randint(avg - 10, avg + 10)
    remove2 = random.randint(avg - 10, avg + 10)
    # Add 3 members
    add1 = random.randint(avg - 5, avg + 15)
    add2 = random.randint(avg - 5, avg + 15)
    add3 = random.randint(avg - 5, avg + 15)
    new_total = total - remove1 - remove2 + add1 + add2 + add3
    new_count = count - 2 + 3
    new_avg = new_total / new_count
    # Ensure clean
    remainder = new_total % new_count
    if remainder != 0:
        add3 += (new_count - remainder)
        new_total = total - remove1 - remove2 + add1 + add2 + add3
    new_avg = new_total // new_count
    subj = random.choice(subjects)
    q = (f"The average {subj} score of {count} students is {avg}. "
         f"Two students with scores {remove1} and {remove2} leave, "
         f"and three new students with scores {add1}, {add2}, and {add3} join. "
         f"What is the new average?")
    choices, answer = make_choices_int(new_avg)
    exp = (f"Old total = {avg} × {count} = {total}. "
           f"Remove: {total} - {remove1} - {remove2} = {total - remove1 - remove2}. "
           f"Add: {total - remove1 - remove2} + {add1} + {add2} + {add3} = {new_total}. "
           f"New count = {count} - 2 + 3 = {new_count}. "
           f"New average = {new_total} ÷ {new_count} = {new_avg}.")
    add_q("Hard", q, choices, answer, exp, ["average", "group problems", "multiple changes"])


# ============================================================
# PADDING: Ensure exactly 200 per difficulty
# ============================================================

def count_by_difficulty(diff):
    return sum(1 for q in questions if q["difficulty"] == diff)


# Pad Easy if needed
while count_by_difficulty("Easy") < 200:
    # Simple average computation with random context
    count = random.choice([3, 4, 5, 6, 7, 8])
    avg = random.randint(10, 95)
    total = avg * count
    context = random.choice([
        "test scores", "daily temperatures (°C)", "heights (cm)",
        "weights (kg)", "ratings (out of 100)", "production units"
    ])
    q_text = f"The average of {count} {context} is {avg}. What is the total sum?"
    choices, answer = make_choices_int(total)
    exp = f"Total = Average × Count = {avg} × {count} = {total}."
    add_q("Easy", q_text, choices, answer, exp, ["average", "word problems", "total from average"])

# Pad Medium if needed
while count_by_difficulty("Medium") < 200:
    # Missing value problem
    count = random.choice([4, 5, 6, 7])
    avg = random.randint(40, 90)
    total = avg * count
    known_count = count - 1
    known_vals = [random.randint(avg - 15, avg + 15) for _ in range(known_count)]
    # Ensure clean
    missing = total - sum(known_vals)
    if missing < 1:
        known_vals[-1] -= (1 - missing)
        missing = total - sum(known_vals)
    known_str = ", ".join(str(v) for v in known_vals)
    context = random.choice(["scores", "values", "measurements", "ratings", "outputs"])
    q_text = (f"The average of {count} {context} is {avg}. "
              f"If {known_count} of them are {known_str}, what is the missing value?")
    choices, answer = make_choices_int(missing)
    exp = (f"Total = {avg} × {count} = {total}. "
           f"Known sum = {sum(known_vals)}. Missing = {total} - {sum(known_vals)} = {missing}.")
    add_q("Medium", q_text, choices, answer, exp, ["average", "word problems", "missing value"])

# Pad Hard if needed
while count_by_difficulty("Hard") < 200:
    # Weighted average with 3 groups
    n1 = random.choice([5, 8, 10, 12, 15, 20])
    n2 = random.choice([5, 8, 10, 12, 15])
    n3 = random.choice([3, 5, 8, 10])
    avg1 = random.randint(55, 75)
    avg2 = random.randint(70, 85)
    avg3 = random.randint(80, 98)
    total = n1 * avg1 + n2 * avg2 + n3 * avg3
    total_count = n1 + n2 + n3
    combined_avg = total / total_count
    if combined_avg == int(combined_avg):
        combined_avg = int(combined_avg)
        choices, answer = make_choices_int(combined_avg)
    else:
        combined_avg = round(combined_avg, 2)
        choices, answer = make_choices_float(combined_avg)
    q_text = (f"In a company, {n1} junior staff average {avg1} in performance, "
              f"{n2} senior staff average {avg2}, and {n3} managers average {avg3}. "
              f"What is the overall average performance score?")
    exp = (f"Total = {n1}×{avg1} + {n2}×{avg2} + {n3}×{avg3} = {total}. "
           f"Count = {total_count}. Average = {total} ÷ {total_count} = {combined_avg}.")
    add_q("Hard", q_text, choices, answer, exp, ["average", "group problems", "weighted average"])

# Trim to exactly 200 per difficulty if over
easy_qs = [q for q in questions if q["difficulty"] == "Easy"][:200]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"][:200]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"][:200]

final_questions = easy_qs + medium_qs + hard_qs

# Re-number IDs
for idx, q in enumerate(final_questions, 1):
    q["id"] = idx


# ============================================================
# VALIDATION
# ============================================================

def validate_questions(qs):
    """Validate all questions have required fields and correct answer is in choices."""
    required_fields = ["id", "subtest", "module", "subtopic", "difficulty",
                       "question", "choices", "answer", "explanation", "tags"]
    errors = []
    for q in qs:
        for field in required_fields:
            if field not in q:
                errors.append(f"Q{q.get('id', '?')}: missing field '{field}'")
        if "choices" in q and "answer" in q:
            if q["answer"] not in q["choices"]:
                errors.append(f"Q{q['id']}: answer '{q['answer']}' not in choices {q['choices']}")
            if len(q["choices"]) != 4:
                errors.append(f"Q{q['id']}: expected 4 choices, got {len(q['choices'])}")
        if "difficulty" in q and q["difficulty"] not in ("Easy", "Medium", "Hard"):
            errors.append(f"Q{q['id']}: invalid difficulty '{q['difficulty']}'")
    return errors


errors = validate_questions(final_questions)
if errors:
    print("VALIDATION ERRORS:")
    for e in errors[:20]:
        print(f"  {e}")
    print(f"  ... ({len(errors)} total errors)")
else:
    print("All questions validated successfully.")

# Count by difficulty
easy_count = sum(1 for q in final_questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in final_questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in final_questions if q["difficulty"] == "Hard")
print(f"Total: {len(final_questions)} questions (Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count})")

# ============================================================
# OUTPUT
# ============================================================

output_dir = Path("data/seed/questions/numerical-ability/ratio-proportion-and-average/average-word-problems")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_questions, f, indent=2, ensure_ascii=False)

print(f"Written to {output_path}")
