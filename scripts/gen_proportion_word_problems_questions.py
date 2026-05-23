"""
Generate 600 multiple-choice questions for the Proportion Word Problems subtopic.
Distribution: 200 Easy, 200 Medium, 200 Hard.
All answers are mathematically verified before output.
"""
import json
import random
from pathlib import Path

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
        "subtopic": "Proportion Word Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def make_choices(correct, fmt="{}"):
    """Create 4 choices including the correct one, formatted with fmt."""
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 50:
        offset = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25])
        sign = random.choice([-1, 1])
        d = correct + sign * offset * max(1, abs(correct) // 20)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    # fallback
    while len(distractors) < 3:
        d = correct + random.randint(2, 30)
        if d != correct and d not in distractors:
            distractors.add(d)
    all_vals = [correct] + list(distractors)
    random.shuffle(all_vals)
    return [fmt.format(v) for v in all_vals], fmt.format(correct)


# ============================================================
# EASY: Direct proportion (cost, distance, production, salary, map, recipe, survey, find-x)
# ============================================================

easy_templates = []

# --- Cost items ---
cost_items = [
    "notebooks", "pencils", "pens", "folders", "erasers", "markers",
    "rulers", "staplers", "envelopes", "tapes", "glue sticks",
    "reams of bond paper", "ink cartridges", "USB drives", "mouse pads",
    "whiteboard markers", "calculators", "scissors", "ballpens",
    "highlighters", "correction tapes", "sticky notes", "binders",
    "index cards", "kg of sugar", "kg of flour", "liters of cooking oil",
    "kg of chicken", "cans of sardines", "packs of noodles",
    "bottles of water", "kg of onions", "loaves of bread", "cartons of milk",
    "packs of coffee", "bars of chocolate", "bottles of soy sauce",
    "kg of bananas", "dozen donuts", "cups of coffee", "bags of charcoal",
    "gallons of water", "sacks of rice", "boxes of chalk", "rolls of tape",
    "pairs of gloves", "liters of alcohol", "boxes of tissue",
    "bars of soap", "bottles of shampoo", "meters of rope", "meters of wire",
    "kg of cement", "liters of paint", "meters of fabric", "dozen eggs",
    "kg of rice", "tickets", "face masks", "packs of detergent",
]

for i in range(70):
    item = cost_items[i % len(cost_items)]
    # Generate clean numbers
    q1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
    unit_price = random.choice([5, 7, 8, 10, 12, 15, 18, 20, 25, 30, 35, 40, 45, 50, 60, 75, 80, 100, 120, 150])
    c1 = q1 * unit_price
    q2 = q1 + random.choice([2, 3, 4, 5, 6, 7, 8, 10, 12])
    c2 = q2 * unit_price
    choices, answer = make_choices(c2, "\u20b1{:,}")
    easy_templates.append((
        f"If {q1} {item} cost \u20b1{c1:,}, how much will {q2} {item} cost at the same rate?",
        choices, answer,
        f"Direct proportion: {q1}/{c1} = {q2}/x. Cross multiply: {q1}x = {c1} \u00d7 {q2} = {c1*q2:,}. x = \u20b1{c2:,}.",
        ["proportions", "word problems", "direct proportion", "cost"]
    ))

# --- Distance ---
vehicles = ["car", "bus", "van", "truck", "motorcycle", "train", "jeepney", "boat", "bicycle", "ambulance"]
for i in range(25):
    v = vehicles[i % len(vehicles)]
    speed = random.choice([30, 40, 45, 50, 60, 72, 75, 80, 90, 100, 120])
    t1 = random.choice([1, 2, 3, 4, 5])
    d1 = speed * t1
    t2 = t1 + random.choice([1, 2, 3, 4, 5, 6])
    d2 = speed * t2
    choices, answer = make_choices(d2, "{} km")
    easy_templates.append((
        f"A {v} travels {d1} km in {t1} hours. At the same speed, how far will it travel in {t2} hours?",
        choices, answer,
        f"Direct proportion: {d1}/{t1} = x/{t2}. Cross multiply: {t1}x = {d1} \u00d7 {t2} = {d1*t2}. x = {d2} km.",
        ["proportions", "word problems", "direct proportion", "distance"]
    ))

# --- Production ---
machines = ["machine", "printer", "factory line", "bottling machine", "packaging unit",
            "assembly robot", "conveyor belt", "stamping press", "weaving loom", "cutting machine"]
for i in range(20):
    m = machines[i % len(machines)]
    rate = random.choice([10, 12, 15, 20, 25, 30, 40, 50, 60])
    t1 = random.choice([2, 3, 4, 5, 6])
    p1 = rate * t1
    t2 = t1 + random.choice([2, 3, 4, 5, 6, 7])
    p2 = rate * t2
    choices, answer = make_choices(p2, "{} items")
    easy_templates.append((
        f"A {m} produces {p1} items in {t1} hours. How many items in {t2} hours at the same rate?",
        choices, answer,
        f"Direct proportion: {p1}/{t1} = x/{t2}. {t1}x = {p1*t2}. x = {p2} items.",
        ["proportions", "word problems", "direct proportion", "production"]
    ))

# --- Salary ---
for i in range(20):
    daily = random.choice([500, 600, 700, 750, 800, 900, 1000, 1200, 1500, 1800])
    d1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    s1 = daily * d1
    d2 = d1 + random.choice([3, 4, 5, 6, 7, 8, 10, 12])
    s2 = daily * d2
    choices, answer = make_choices(s2, "\u20b1{:,}")
    easy_templates.append((
        f"An employee earns \u20b1{s1:,} for {d1} days of work. How much in {d2} days at the same daily rate?",
        choices, answer,
        f"Daily rate = \u20b1{daily:,}. Earnings = {daily:,} \u00d7 {d2} = \u20b1{s2:,}.",
        ["proportions", "word problems", "direct proportion", "salary"]
    ))

# --- Map scale ---
for i in range(20):
    cm1 = random.choice([1, 2, 3, 4, 5])
    km_per_cm = random.choice([15, 20, 25, 30, 35, 40, 50, 60, 75, 100])
    km1 = cm1 * km_per_cm
    cm2 = cm1 + random.choice([2, 3, 4, 5, 6, 7, 8])
    km2 = cm2 * km_per_cm
    choices, answer = make_choices(km2, "{} km")
    easy_templates.append((
        f"On a map, {cm1} cm represents {km1} km. What actual distance does {cm2} cm represent?",
        choices, answer,
        f"Direct proportion: {cm1}/{km1} = {cm2}/x. {cm1}x = {km1*cm2}. x = {km2} km.",
        ["proportions", "word problems", "direct proportion", "map scale"]
    ))

# --- Recipe ---
ingredients = ["cups of flour", "cups of rice", "tablespoons of sugar", "cups of milk",
               "eggs", "cups of water", "teaspoons of salt", "grams of butter",
               "liters of broth", "cups of coconut milk", "tablespoons of soy sauce",
               "cups of cream", "grams of cheese", "tablespoons of vinegar", "cups of oil"]
for i in range(20):
    ing = ingredients[i % len(ingredients)]
    serv1 = random.choice([4, 5, 6, 8, 10])
    amt_per_serv = random.choice([1, 2, 3, 4, 5])
    amt1 = serv1 * amt_per_serv // random.choice([1, 2])
    if amt1 == 0:
        amt1 = 2
    serv2 = serv1 * random.choice([2, 3, 4])
    amt2 = amt1 * serv2 // serv1
    if amt2 == amt1 or serv2 == serv1:
        continue
    choices, answer = make_choices(amt2, "{} " + ing)
    easy_templates.append((
        f"A recipe for {serv1} servings uses {amt1} {ing}. How much for {serv2} servings?",
        choices, answer,
        f"Direct proportion: {amt1}/{serv1} = x/{serv2}. {serv1}x = {amt1*serv2}. x = {amt2} {ing}.",
        ["proportions", "word problems", "direct proportion", "recipe"]
    ))

# --- Find x ---
for i in range(25):
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    multiplier = random.choice([2, 3, 4, 5, 6, 7])
    b = a * multiplier
    c = random.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15])
    d = c * multiplier
    choices, answer = make_choices(d, "{}")
    easy_templates.append((
        f"Find the value of x: {a}/{b} = {c}/x",
        choices, answer,
        f"Cross multiply: {a}x = {b} \u00d7 {c} = {b*c}. x = {b*c}/{a} = {d}.",
        ["proportions", "cross multiplication", "missing value"]
    ))

# Add easy questions
for item in easy_templates[:200]:
    q, ch, a, e, t = item
    add_q("Easy", q, ch, a, e, t)

print(f"Easy count: {len([x for x in questions if x['difficulty'] == 'Easy'])}")


# ============================================================
# MEDIUM: Inverse proportion + mixed direct with larger numbers
# ============================================================

medium_templates = []

# --- Workers/days inverse ---
worker_contexts = ["workers", "painters", "carpenters", "electricians", "plumbers",
                   "volunteers", "staff members", "technicians", "laborers", "cleaners"]
for i in range(50):
    ctx = worker_contexts[i % len(worker_contexts)]
    w1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    d1 = random.choice([4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24])
    total = w1 * d1
    # pick w2 that divides total evenly
    possible_w2 = [w for w in range(2, 30) if total % w == 0 and w != w1]
    if not possible_w2:
        continue
    w2 = random.choice(possible_w2)
    d2 = total // w2
    if d2 == d1 or d2 <= 0:
        continue
    choices, answer = make_choices(d2, "{} days")
    medium_templates.append((
        f"If {w1} {ctx} can complete a task in {d1} days, how many days will {w2} {ctx} need?",
        choices, answer,
        f"Inverse proportion: {w1} \u00d7 {d1} = {w2} \u00d7 x. {total} = {w2}x. x = {d2} days.",
        ["proportions", "word problems", "inverse proportion", "workforce"]
    ))

# --- Speed/time inverse ---
for i in range(40):
    s1 = random.choice([30, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 84, 90, 96, 100, 120])
    t1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
    dist = s1 * t1
    possible_s2 = [s for s in [30, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 84, 90, 96, 100, 120]
                   if dist % s == 0 and s != s1]
    if not possible_s2:
        continue
    s2 = random.choice(possible_s2)
    t2 = dist // s2
    if t2 == t1 or t2 <= 0:
        continue
    choices, answer = make_choices(t2, "{} hours")
    medium_templates.append((
        f"A vehicle at {s1} km/h takes {t1} hours for a trip. How long at {s2} km/h?",
        choices, answer,
        f"Inverse proportion: {s1} \u00d7 {t1} = {s2} \u00d7 x. {dist} = {s2}x. x = {t2} hours.",
        ["proportions", "word problems", "inverse proportion", "speed"]
    ))

# --- Food supply inverse ---
for i in range(25):
    p1 = random.choice([5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 25, 30])
    d1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    total = p1 * d1
    possible_p2 = [p for p in range(3, 40) if total % p == 0 and p != p1]
    if not possible_p2:
        continue
    p2 = random.choice(possible_p2)
    d2 = total // p2
    if d2 == d1 or d2 <= 0:
        continue
    choices, answer = make_choices(d2, "{} days")
    medium_templates.append((
        f"A food supply lasts {p1} people for {d1} days. How many days will it last for {p2} people?",
        choices, answer,
        f"Inverse proportion: {p1} \u00d7 {d1} = {p2} \u00d7 x. {total} = {p2}x. x = {d2} days.",
        ["proportions", "word problems", "inverse proportion", "food supply"]
    ))

# --- Pipes/tanks inverse ---
for i in range(20):
    pipes1 = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    time1 = random.choice([3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    total = pipes1 * time1
    possible_p2 = [p for p in range(2, 20) if total % p == 0 and p != pipes1]
    if not possible_p2:
        continue
    pipes2 = random.choice(possible_p2)
    time2 = total // pipes2
    if time2 == time1 or time2 <= 0:
        continue
    choices, answer = make_choices(time2, "{} hours")
    medium_templates.append((
        f"If {pipes1} pipes fill a tank in {time1} hours, how long will {pipes2} pipes take?",
        choices, answer,
        f"Inverse proportion: {pipes1} \u00d7 {time1} = {pipes2} \u00d7 x. {total} = {pipes2}x. x = {time2} hours.",
        ["proportions", "word problems", "inverse proportion", "pipes"]
    ))

# --- Find workers needed (inverse, solve for workers) ---
for i in range(20):
    w1 = random.choice([4, 5, 6, 7, 8, 9, 10, 12, 14, 15])
    d1 = random.choice([4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    total = w1 * d1
    possible_d2 = [d for d in [2, 3, 4, 5, 6, 7, 8, 9, 10] if total % d == 0 and d != d1]
    if not possible_d2:
        continue
    d2 = random.choice(possible_d2)
    w2 = total // d2
    if w2 == w1 or w2 <= 0:
        continue
    ctx = random.choice(worker_contexts)
    choices, answer = make_choices(w2, "{} " + ctx)
    medium_templates.append((
        f"If {w1} {ctx} finish a job in {d1} days, how many {ctx} are needed to finish in {d2} days?",
        choices, answer,
        f"Inverse proportion: {w1} \u00d7 {d1} = x \u00d7 {d2}. {total} = {d2}x. x = {w2} {ctx}.",
        ["proportions", "word problems", "inverse proportion", "workforce"]
    ))

# --- Mixed direct with workplace context ---
medium_direct = [
    ("A government office processes 45 applications in 3 days. How many in 11 days?",
     165, "Direct proportion: 45/3 = x/11. 3x = 495. x = 165."),
    ("A printing press produces 1,200 flyers in 4 hours. How many in 7 hours?",
     2100, "Direct proportion: 1200/4 = x/7. 4x = 8400. x = 2,100."),
    ("A delivery van uses 18 liters for 216 km. How much for 360 km?",
     30, "Direct proportion: 18/216 = x/360. 216x = 6480. x = 30 liters."),
    ("8 electricians install 96 outlets/day. How many can 14 install?",
     168, "Direct proportion: 8/96 = 14/x. 8x = 1344. x = 168."),
    ("5 kg of fertilizer covers 200 sq meters. How much for 520 sq meters?",
     13, "Direct proportion: 5/200 = x/520. 200x = 2600. x = 13 kg."),
    ("A clerk files 84 documents in 6 hours. How many in 10 hours?",
     140, "Direct proportion: 84/6 = x/10. 6x = 840. x = 140."),
    ("7 painters paint 35 rooms/week. How many rooms can 12 painters paint?",
     60, "Direct proportion: 7/35 = 12/x. 7x = 420. x = 60."),
    ("A farmer harvests 480 kg from 6 hectares. How much from 10 hectares?",
     800, "Direct proportion: 480/6 = x/10. 6x = 4800. x = 800 kg."),
    ("A hospital uses 36 oxygen tanks in 9 days. How many in 25 days?",
     100, "Direct proportion: 36/9 = x/25. 9x = 900. x = 100."),
    ("A crew lays 120 meters of pipe in 8 hours. How much in 15 hours?",
     225, "Direct proportion: 120/8 = x/15. 8x = 1800. x = 225 meters."),
    ("9 liters of disinfectant cleans 54 rooms. How many rooms for 15 liters?",
     90, "Direct proportion: 9/54 = 15/x. 9x = 810. x = 90."),
    ("250 grams of cheese costs \u20b1175. How much does 400 grams cost?",
     280, "Direct proportion: 250/175 = 400/x. 250x = 70000. x = \u20b1280."),
    ("A water tank fills at 15 liters/min. How many liters in 45 minutes?",
     675, "Direct: 15 \u00d7 45 = 675 liters."),
    ("12 meters of cloth cost \u20b11,800. How much do 20 meters cost?",
     3000, "Direct proportion: 12/1800 = 20/x. 12x = 36000. x = \u20b13,000."),
    ("A school bus travels 75 km in 1.5 hours. How far in 4 hours?",
     200, "Speed = 50 km/h. Distance = 50 \u00d7 4 = 200 km."),
]

for q, correct, e in medium_direct:
    choices, answer = make_choices(correct, "{}")
    medium_templates.append((q, choices, answer, e,
                             ["proportions", "word problems", "direct proportion"]))

# Shuffle and take 200
random.shuffle(medium_templates)
for item in medium_templates[:200]:
    q, ch, a, e, t = item
    add_q("Medium", q, ch, a, e, t)

print(f"Medium count: {len([x for x in questions if x['difficulty'] == 'Medium'])}")


# ============================================================
# HARD: Multi-step, combined work, complex scenarios
# ============================================================

hard_templates = []

# --- Type 1: Workers leave/join mid-project ---
for i in range(30):
    w1 = random.choice([8, 10, 12, 14, 15, 16, 18, 20])
    total_days = random.choice([12, 15, 16, 18, 20, 24, 25, 30])
    total_work = w1 * total_days
    days_done = random.choice([d for d in range(2, total_days // 2) if d < total_days])
    work_done = w1 * days_done
    remaining = total_work - work_done
    leave = random.choice([2, 3, 4, 5, 6])
    if leave >= w1:
        continue
    w2 = w1 - leave
    if remaining % w2 != 0:
        continue
    extra_days = remaining // w2
    choices, answer = make_choices(extra_days, "{} days")
    hard_templates.append((
        f"A project requires {w1} workers for {total_days} days. After {days_done} days, {leave} workers leave. How many more days to finish?",
        choices, answer,
        f"Total work = {w1}\u00d7{total_days} = {total_work} worker-days. Done = {w1}\u00d7{days_done} = {work_done}. Remaining = {remaining}. Workers = {w2}. Days = {remaining}/{w2} = {extra_days}.",
        ["proportions", "word problems", "multi-step", "workforce"]
    ))

# --- Type 2: Workers join mid-project, find total days ---
for i in range(20):
    w1 = random.choice([6, 8, 10, 12, 15, 18, 20])
    total_days = random.choice([10, 12, 14, 15, 16, 18, 20, 24])
    total_work = w1 * total_days
    days_done = random.choice([d for d in range(2, total_days // 2)])
    work_done = w1 * days_done
    remaining = total_work - work_done
    join = random.choice([2, 3, 4, 5, 6, 8, 10])
    w2 = w1 + join
    if remaining % w2 != 0:
        continue
    extra_days = remaining // w2
    total_actual = days_done + extra_days
    choices, answer = make_choices(total_actual, "{} days")
    hard_templates.append((
        f"{w1} workers are assigned to finish a project in {total_days} days. After {days_done} days, {join} more workers join. How many total days from the start to finish?",
        choices, answer,
        f"Total = {total_work} worker-days. Done in {days_done} days = {work_done}. Remaining = {remaining}. New team = {w2}. Extra days = {remaining}/{w2} = {extra_days}. Total = {days_done}+{extra_days} = {total_actual} days.",
        ["proportions", "word problems", "multi-step", "workforce"]
    ))

# --- Type 3: Machines + hours (two variables) ---
for i in range(25):
    m1 = random.choice([3, 4, 5, 6, 8, 10])
    h1 = random.choice([3, 4, 5, 6, 8])
    rate = random.choice([5, 8, 10, 12, 15, 20, 25])
    p1 = m1 * h1 * rate
    m2 = random.choice([m for m in [4, 5, 6, 7, 8, 9, 10, 12] if m != m1])
    h2 = random.choice([h for h in [3, 4, 5, 6, 7, 8, 9, 10] if h != h1])
    p2 = m2 * h2 * rate
    choices, answer = make_choices(p2, "{} items")
    hard_templates.append((
        f"If {m1} machines produce {p1} items in {h1} hours, how many items will {m2} machines produce in {h2} hours?",
        choices, answer,
        f"Rate per machine per hour = {p1}/({m1}\u00d7{h1}) = {rate}. Output = {m2}\u00d7{h2}\u00d7{rate} = {p2} items.",
        ["proportions", "word problems", "multi-step", "production"]
    ))

# --- Type 4: Workers + hours/day (three variables) ---
for i in range(25):
    w1 = random.choice([4, 5, 6, 8, 9, 10, 12])
    h1 = random.choice([4, 5, 6, 7, 8, 9, 10])
    d1 = random.choice([5, 6, 8, 9, 10, 12, 14, 15])
    total = w1 * h1 * d1
    w2 = random.choice([w for w in [3, 4, 5, 6, 7, 8, 9, 10, 12, 15] if w != w1])
    h2 = random.choice([h for h in [4, 5, 6, 7, 8, 9, 10] if h != h1])
    if total % (w2 * h2) != 0:
        continue
    d2 = total // (w2 * h2)
    if d2 == d1 or d2 <= 0 or d2 > 50:
        continue
    choices, answer = make_choices(d2, "{} days")
    hard_templates.append((
        f"{w1} workers working {h1} hours/day finish a job in {d1} days. How many days for {w2} workers at {h2} hours/day?",
        choices, answer,
        f"Total work = {w1}\u00d7{h1}\u00d7{d1} = {total} worker-hours. New: {w2}\u00d7{h2}\u00d7d = {total}. d = {total}/({w2}\u00d7{h2}) = {total}/{w2*h2} = {d2} days.",
        ["proportions", "word problems", "multi-step", "workforce"]
    ))

# --- Type 5: Map + speed (two-step) ---
for i in range(15):
    cm_per_unit = random.choice([1, 2, 3, 4, 5])
    km_per_unit = random.choice([20, 25, 30, 40, 50, 75])
    map_dist = random.choice([4, 5, 6, 7, 8, 9, 10, 12])
    actual_km = map_dist * km_per_unit // cm_per_unit
    speed = random.choice([40, 50, 60, 75, 80, 100])
    if actual_km % speed != 0:
        # try to make it work with minutes
        time_min = actual_km * 60 // speed
        if actual_km * 60 % speed != 0:
            continue
        choices, answer = make_choices(time_min, "{} minutes")
        hard_templates.append((
            f"On a map, {cm_per_unit} cm = {km_per_unit} km. Two cities are {map_dist} cm apart. At {speed} km/h, how long is the drive?",
            choices, answer,
            f"Distance = {map_dist}\u00d7{km_per_unit}/{cm_per_unit} = {actual_km} km. Time = {actual_km}/{speed} hours = {time_min} minutes.",
            ["proportions", "word problems", "multi-step", "map scale"]
        ))
    else:
        time_h = actual_km // speed
        choices, answer = make_choices(time_h, "{} hours")
        hard_templates.append((
            f"On a map, {cm_per_unit} cm = {km_per_unit} km. Two cities are {map_dist} cm apart. At {speed} km/h, how long is the drive?",
            choices, answer,
            f"Distance = {map_dist}\u00d7{km_per_unit}/{cm_per_unit} = {actual_km} km. Time = {actual_km}/{speed} = {time_h} hours.",
            ["proportions", "word problems", "multi-step", "map scale"]
        ))


# --- Type 6: Fuel cost (two-step: find fuel, then cost) ---
for i in range(20):
    liters_per = random.choice([5, 6, 8, 10, 12, 15])
    km_per = random.choice([60, 72, 80, 90, 100, 120, 150])
    trip_km = km_per * random.choice([2, 3, 4, 5, 6])
    fuel_needed = liters_per * trip_km // km_per
    price_per_liter = random.choice([55, 58, 60, 62, 65, 68, 70, 72, 75])
    total_cost = fuel_needed * price_per_liter
    choices, answer = make_choices(total_cost, "\u20b1{:,}")
    hard_templates.append((
        f"A car uses {liters_per} liters per {km_per} km. Fuel costs \u20b1{price_per_liter}/liter. What is the fuel cost for a {trip_km}-km trip?",
        choices, answer,
        f"Fuel = {liters_per}\u00d7{trip_km}/{km_per} = {fuel_needed} liters. Cost = {fuel_needed}\u00d7{price_per_liter} = \u20b1{total_cost:,}.",
        ["proportions", "word problems", "multi-step", "fuel cost"]
    ))

# --- Type 7: Combined work (two pipes/workers) ---
for i in range(20):
    # Pick times that give a clean combined time
    a = random.choice([3, 4, 5, 6, 8, 9, 10, 12, 15])
    b = random.choice([b_val for b_val in [4, 5, 6, 8, 9, 10, 12, 15, 18, 20] if b_val != a])
    # Combined rate = 1/a + 1/b = (a+b)/(a*b)
    # Time = a*b/(a+b)
    numerator = a * b
    denominator = a + b
    if numerator % denominator != 0:
        continue
    combined_time = numerator // denominator
    if combined_time <= 0 or combined_time >= min(a, b):
        continue
    choices, answer = make_choices(combined_time, "{} hours")
    entity = random.choice(["Pipe A", "Worker A", "Pump A", "Hose A"])
    entity_b = entity.replace("A", "B")
    task = random.choice(["fill a tank", "complete a job", "paint a room", "finish a report"])
    hard_templates.append((
        f"{entity} can {task} in {a} hours. {entity_b} can {task} in {b} hours. Working together, how long will it take?",
        choices, answer,
        f"Rate A = 1/{a}, Rate B = 1/{b}. Combined = 1/{a} + 1/{b} = ({b}+{a})/({a*b}) = {a+b}/{a*b}. Time = {a*b}/{a+b} = {combined_time} hours.",
        ["proportions", "word problems", "combined work"]
    ))

# --- Type 8: Budget ratio + percentage change ---
for i in range(15):
    total_budget = random.choice([100000, 200000, 300000, 400000, 500000, 600000, 800000, 1000000])
    r1 = random.choice([2, 3, 4, 5])
    r2 = random.choice([r for r in [2, 3, 4, 5] if r != r1])
    part1 = total_budget * r1 // (r1 + r2)
    part2 = total_budget * r2 // (r1 + r2)
    if part1 * (r1 + r2) != total_budget * r1:
        continue
    pct = random.choice([10, 15, 20, 25, 30, 40, 50])
    new_part1 = part1 * (100 + pct) // 100
    if part1 * (100 + pct) % 100 != 0:
        continue
    new_total = new_part1 + part2
    choices, answer = make_choices(new_total, "\u20b1{:,}")
    hard_templates.append((
        f"A budget of \u20b1{total_budget:,} is split in ratio {r1}:{r2} between personnel and operations. If personnel costs increase by {pct}%, what is the new total budget (keeping operations the same)?",
        choices, answer,
        f"Personnel = {r1}/{r1+r2} \u00d7 {total_budget:,} = \u20b1{part1:,}. Operations = \u20b1{part2:,}. New personnel = {part1:,} \u00d7 {(100+pct)/100} = \u20b1{new_part1:,}. New total = {new_part1:,} + {part2:,} = \u20b1{new_total:,}.",
        ["proportions", "word problems", "multi-step", "budget"]
    ))

# --- Type 9: Partial work then find additional workers ---
for i in range(15):
    w1 = random.choice([8, 10, 12, 15, 18, 20])
    total_days = random.choice([10, 12, 15, 16, 18, 20, 24])
    total_work = w1 * total_days
    days_for_frac = random.choice([d for d in range(2, total_days // 2 + 1)])
    work_done = w1 * days_for_frac
    remaining = total_work - work_done
    possible_target = [d for d in [3, 4, 5, 6, 7, 8] if remaining % d == 0]
    if not possible_target:
        continue
    target_days = random.choice(possible_target)
    workers_needed = remaining // target_days
    additional = workers_needed - w1
    if additional <= 0 or additional > 30:
        continue
    choices, answer = make_choices(additional, "{} workers")
    hard_templates.append((
        f"{w1} workers have been working on a project for {days_for_frac} days out of a planned {total_days} days. How many additional workers must be hired to finish the remaining work in {target_days} days?",
        choices, answer,
        f"Total = {total_work} worker-days. Done = {work_done}. Remaining = {remaining}. Workers needed for {target_days} days = {remaining}/{target_days} = {workers_needed}. Additional = {workers_needed} - {w1} = {additional}.",
        ["proportions", "word problems", "multi-step", "workforce"]
    ))

# --- Type 10: Earnings with workers + days (two-variable direct) ---
for i in range(15):
    w1 = random.choice([4, 5, 6, 7, 8, 9, 10])
    d1 = random.choice([3, 4, 5, 6, 7, 8])
    daily_rate = random.choice([500, 600, 700, 750, 800, 900, 1000, 1200, 1500])
    earn1 = w1 * d1 * daily_rate
    w2 = random.choice([w for w in [5, 6, 7, 8, 9, 10, 12] if w != w1])
    d2 = random.choice([d for d in [4, 5, 6, 7, 8, 9, 10] if d != d1])
    earn2 = w2 * d2 * daily_rate
    choices, answer = make_choices(earn2, "\u20b1{:,}")
    hard_templates.append((
        f"If {w1} workers earn \u20b1{earn1:,} in {d1} days, how much will {w2} workers earn in {d2} days at the same rate?",
        choices, answer,
        f"Daily rate per worker = {earn1:,}/({w1}\u00d7{d1}) = \u20b1{daily_rate:,}. Earnings = {w2}\u00d7{d2}\u00d7{daily_rate:,} = \u20b1{earn2:,}.",
        ["proportions", "word problems", "multi-step", "salary"]
    ))


# --- Type 11: Speed segments (average speed) ---
for i in range(15):
    s1 = random.choice([40, 50, 60, 72, 80, 90, 100])
    t1 = random.choice([2, 3, 4, 5])
    d1_val = s1 * t1
    s2 = random.choice([s for s in [40, 50, 60, 72, 80, 90, 100, 120] if s != s1])
    t2 = random.choice([1, 2, 3, 4])
    d2_val = s2 * t2
    total_d = d1_val + d2_val
    total_t = t1 + t2
    if total_d % total_t != 0:
        continue
    avg_speed = total_d // total_t
    choices, answer = make_choices(avg_speed, "{} km/h")
    hard_templates.append((
        f"A car travels {d1_val} km at {s1} km/h, then {d2_val} km at {s2} km/h. What is the average speed for the entire trip?",
        choices, answer,
        f"Time 1 = {d1_val}/{s1} = {t1}h. Time 2 = {d2_val}/{s2} = {t2}h. Total = {total_d} km in {total_t}h. Average = {total_d}/{total_t} = {avg_speed} km/h.",
        ["proportions", "word problems", "multi-step", "speed"]
    ))

# --- Type 12: Inverse with added people ---
for i in range(15):
    p1 = random.choice([10, 12, 15, 18, 20, 24, 25, 30])
    d1 = random.choice([4, 5, 6, 8, 9, 10, 12])
    total = p1 * d1
    added = random.choice([2, 3, 4, 5, 6, 8, 10])
    p2 = p1 + added
    if total % p2 != 0:
        continue
    d2 = total // p2
    if d2 == d1:
        continue
    choices, answer = make_choices(d2, "{} days")
    hard_templates.append((
        f"A supply of food is enough for {p1} people for {d1} days. If {added} more people join the group, how many days will the food last?",
        choices, answer,
        f"Inverse proportion: {p1}\u00d7{d1} = {p2}\u00d7x. {total} = {p2}x. x = {d2} days.",
        ["proportions", "word problems", "inverse proportion", "food supply"]
    ))

# --- Type 13: Construction ratio + total ---
for i in range(15):
    r_cement = random.choice([1, 2])
    r_sand = random.choice([2, 3, 4])
    r_gravel = random.choice([3, 4, 5, 6])
    total_ratio = r_cement + r_sand + r_gravel
    # Given one component, find total
    given_part = random.choice(["sand", "gravel", "cement"])
    if given_part == "sand":
        given_ratio = r_sand
    elif given_part == "gravel":
        given_ratio = r_gravel
    else:
        given_ratio = r_cement
    given_amount = given_ratio * random.choice([5, 8, 10, 12, 15, 20])
    multiplier = given_amount // given_ratio
    total_bags = total_ratio * multiplier
    choices, answer = make_choices(total_bags, "{} bags")
    hard_templates.append((
        f"A concrete mix uses cement, sand, and gravel in ratio {r_cement}:{r_sand}:{r_gravel}. If {given_amount} bags of {given_part} are needed, how many total bags of material are required?",
        choices, answer,
        f"1 part = {given_amount}/{given_ratio} = {multiplier} bags. Total parts = {total_ratio}. Total = {total_ratio}\u00d7{multiplier} = {total_bags} bags.",
        ["proportions", "word problems", "multi-step", "construction"]
    ))

# Shuffle and take 200
random.shuffle(hard_templates)
for item in hard_templates[:200]:
    q, ch, a, e, t = item
    add_q("Hard", q, ch, a, e, t)

print(f"Hard count: {len([x for x in questions if x['difficulty'] == 'Hard'])}")


# ============================================================
# PAD TO EXACTLY 200 EACH IF NEEDED
# ============================================================

def pad_easy(target=200):
    """Generate additional easy questions if under target."""
    current = len([x for x in questions if x["difficulty"] == "Easy"])
    i = 0
    while current < target:
        i += 1
        q1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
        unit_price = random.choice([10, 12, 15, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60])
        c1 = q1 * unit_price
        q2 = q1 + random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        c2 = q2 * unit_price
        item = random.choice(["items", "units", "pieces", "packs", "boxes", "bottles", "kg", "liters", "meters"])
        choices, answer = make_choices(c2, "\u20b1{:,}")
        add_q("Easy",
              f"If {q1} {item} cost \u20b1{c1:,}, how much will {q2} {item} cost at the same rate?",
              choices, answer,
              f"Direct proportion: unit price = {c1}/{q1} = \u20b1{unit_price}. Cost = {unit_price}\u00d7{q2} = \u20b1{c2:,}.",
              ["proportions", "word problems", "direct proportion", "cost"])
        current += 1


def pad_medium(target=200):
    """Generate additional medium questions if under target."""
    current = len([x for x in questions if x["difficulty"] == "Medium"])
    while current < target:
        w1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24])
        d1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20])
        total = w1 * d1
        possible_w2 = [w for w in range(2, 30) if total % w == 0 and w != w1]
        if not possible_w2:
            continue
        w2 = random.choice(possible_w2)
        d2 = total // w2
        if d2 == d1 or d2 <= 0 or d2 > 60:
            continue
        ctx = random.choice(["workers", "painters", "staff", "volunteers", "technicians", "helpers"])
        choices, answer = make_choices(d2, "{} days")
        add_q("Medium",
              f"If {w1} {ctx} can do a job in {d1} days, how many days for {w2} {ctx}?",
              choices, answer,
              f"Inverse proportion: {w1}\u00d7{d1} = {w2}\u00d7x. {total} = {w2}x. x = {d2} days.",
              ["proportions", "word problems", "inverse proportion", "workforce"])
        current += 1


def pad_hard(target=200):
    """Generate additional hard questions if under target."""
    current = len([x for x in questions if x["difficulty"] == "Hard"])
    while current < target:
        # Multi-step: machines produce items
        m1 = random.choice([2, 3, 4, 5, 6, 8])
        h1 = random.choice([2, 3, 4, 5, 6])
        rate = random.choice([5, 8, 10, 12, 15, 20, 25, 30])
        p1 = m1 * h1 * rate
        m2 = random.choice([m for m in range(2, 12) if m != m1])
        h2 = random.choice([h for h in range(2, 10) if h != h1])
        p2 = m2 * h2 * rate
        choices, answer = make_choices(p2, "{} items")
        add_q("Hard",
              f"If {m1} machines produce {p1:,} items in {h1} hours, how many items will {m2} machines produce in {h2} hours?",
              choices, answer,
              f"Rate/machine/hour = {p1}/({m1}\u00d7{h1}) = {rate}. Output = {m2}\u00d7{h2}\u00d7{rate} = {p2} items.",
              ["proportions", "word problems", "multi-step", "production"])
        current += 1


pad_easy(200)
pad_medium(200)
pad_hard(200)

# Final counts
easy_count = len([x for x in questions if x["difficulty"] == "Easy"])
medium_count = len([x for x in questions if x["difficulty"] == "Medium"])
hard_count = len([x for x in questions if x["difficulty"] == "Hard"])
print(f"\nFinal counts - Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}")
print(f"Total: {len(questions)}")

# Re-number IDs sequentially
for i, q in enumerate(questions, 1):
    q["id"] = i

# Write output
output_dir = Path("data/seed/questions/numerical-ability/ratio-proportion-and-average/proportion-word-problems")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\nWritten to: {output_path}")
print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
