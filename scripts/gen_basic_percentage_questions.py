"""
Generate 600 multiple-choice questions for Basic Percentage Problems.
Distribution: 200 Easy, 200 Medium, 200 Hard

Subtopic: Basic Percentage Problems
Module: Percentages
Subtest: Numerical Ability

Run: python scripts/gen_basic_percentage_questions.py
Output: data/seed/questions/numerical-ability/percentages/basic-percentage-problems/questions.json
"""

import json
import random
from pathlib import Path

random.seed(44)

questions = []
qid = 0


def add_q(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Basic Percentage Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def fmt(n):
    """Format number with commas for thousands."""
    if isinstance(n, float):
        if n == int(n):
            return f"{int(n):,}"
        s = f"{n:,.10f}".rstrip('0').rstrip('.')
        return s
    return f"{n:,}"


def fmt_pct(n):
    """Format a percentage value cleanly."""
    if n == int(n):
        return f"{int(n)}%"
    return f"{n:g}%"


def fmt_money(n):
    """Format as Philippine peso."""
    if isinstance(n, float) and n != int(n):
        return f"₱{n:,.2f}"
    return f"₱{int(n):,}"


def make_choices_numeric(correct, count=3, spread=None, fmt_func=fmt):
    """Generate 4 choices for a numeric answer."""
    if spread is None:
        spread = max(3, abs(correct) // 8) if correct != 0 else 5
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        if abs(correct) > 100:
            offset = random.choice([-3, -2, -1, 1, 2, 3]) * random.randint(1, max(1, spread))
        elif abs(correct) > 10:
            offset = random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        else:
            offset = random.choice([-3, -2, -1, 1, 2, 3])
        d = correct + offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct + len(distractors) + 1)
    correct_str = fmt_func(correct)
    choices = [correct_str] + [fmt_func(d) for d in distractors]
    random.shuffle(choices)
    return choices, correct_str


def make_choices_pct(correct_pct, count=3):
    """Generate 4 choices for a percentage answer."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        if correct_pct >= 50:
            offset = random.choice([-15, -10, -5, 5, 10, 15])
        elif correct_pct >= 10:
            offset = random.choice([-8, -5, -3, -2, 2, 3, 5, 8])
        else:
            offset = random.choice([-3, -2, -1, 1, 2, 3, 5])
        d = correct_pct + offset
        if d != correct_pct and d > 0 and d <= 200 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct_pct + len(distractors) + 1)
    correct_str = fmt_pct(correct_pct)
    choices = [correct_str] + [fmt_pct(d) for d in distractors]
    random.shuffle(choices)
    return choices, correct_str


def make_choices_money(correct, count=3):
    """Generate 4 choices for a money answer."""
    spread = max(500, abs(correct) // 8)
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        offset = random.choice([-3, -2, -1, 1, 2, 3]) * random.randint(1, max(1, spread))
        d = correct + offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct + (len(distractors) + 1) * 1000)
    correct_str = fmt_money(correct)
    choices = [correct_str] + [fmt_money(d) for d in distractors]
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Finding the Part (direct "What is X% of Y?") (1-50) ---
easy_part_data = [
    (10, 200), (20, 150), (25, 80), (50, 120), (75, 200),
    (10, 500), (20, 300), (25, 400), (50, 600), (30, 100),
    (40, 250), (60, 150), (10, 350), (20, 450), (25, 160),
    (50, 340), (75, 400), (5, 200), (15, 400), (30, 500),
    (10, 700), (20, 800), (25, 240), (50, 900), (75, 120),
    (40, 500), (60, 300), (80, 250), (90, 200), (10, 1000),
    (20, 1000), (25, 1000), (50, 1000), (5, 600), (15, 200),
    (30, 200), (40, 150), (60, 500), (70, 300), (80, 500),
    (10, 450), (20, 250), (25, 320), (50, 480), (75, 160),
    (5, 400), (15, 300), (30, 400), (40, 200), (60, 250),
]

for rate, whole in easy_part_data:
    part = rate * whole / 100
    choices, ans = make_choices_numeric(int(part))
    add_q("Easy",
          f"What is {rate}% of {fmt(whole)}?",
          choices, ans,
          f"Convert {rate}% to decimal: {rate/100}. Multiply: {rate/100} × {fmt(whole)} = {fmt(int(part))}.",
          ["percentages", "finding the part", "basic percentage problems"])

# --- Easy: Finding the Rate (direct "X is what % of Y?") (51-100) ---
easy_rate_data = [
    (20, 100), (15, 60), (30, 150), (45, 90), (50, 200),
    (12, 48), (36, 120), (18, 72), (25, 50), (40, 80),
    (60, 300), (75, 500), (24, 96), (35, 140), (80, 200),
    (10, 50), (16, 64), (27, 108), (42, 168), (63, 252),
    (90, 300), (48, 240), (56, 280), (72, 360), (84, 420),
    (100, 500), (150, 600), (200, 800), (250, 1000), (120, 480),
    (9, 36), (14, 56), (21, 84), (32, 128), (44, 176),
    (55, 220), (66, 264), (77, 308), (88, 352), (99, 396),
    (6, 30), (8, 40), (12, 60), (15, 75), (18, 90),
    (24, 120), (33, 150), (36, 180), (42, 210), (54, 240),
]

for part, whole in easy_rate_data:
    rate = part / whole * 100
    choices, ans = make_choices_pct(rate)
    add_q("Easy",
          f"{fmt(part)} is what percent of {fmt(whole)}?",
          choices, ans,
          f"Divide the part by the whole: {fmt(part)} ÷ {fmt(whole)} = {part/whole}. Multiply by 100: {part/whole} × 100 = {fmt_pct(rate)}.",
          ["percentages", "finding the percentage", "basic percentage problems"])

# --- Easy: Finding the Whole (direct "X is Y% of what?") (101-150) ---
easy_whole_data = [
    (20, 25), (50, 50), (30, 10), (15, 75), (40, 20),
    (60, 30), (45, 25), (80, 40), (100, 50), (12, 20),
    (24, 40), (36, 60), (48, 80), (10, 5), (90, 30),
    (75, 25), (150, 50), (200, 25), (35, 70), (18, 30),
    (27, 45), (64, 80), (56, 70), (42, 60), (28, 40),
    (16, 20), (32, 40), (8, 10), (72, 90), (54, 60),
    (21, 30), (14, 20), (63, 70), (81, 90), (9, 10),
    (6, 15), (33, 75), (22, 50), (44, 80), (55, 25),
    (66, 30), (77, 35), (88, 40), (99, 45), (11, 50),
    (13, 25), (17, 50), (19, 20), (23, 25), (29, 50),
]

for part, rate in easy_whole_data:
    whole = part / (rate / 100)
    choices, ans = make_choices_numeric(int(whole))
    add_q("Easy",
          f"{fmt(part)} is {rate}% of what number?",
          choices, ans,
          f"Divide the part by the rate (as decimal): {fmt(part)} ÷ {rate/100} = {fmt(int(whole))}.",
          ["percentages", "finding the whole", "basic percentage problems"])


# --- Easy: Simple word problems - discounts/scores (151-200) ---
easy_word_problems = [
    # (context, rate, whole, question_template, answer_type)
    # Finding the part in context
    ("A student scored {rate}% on a {whole}-item test. How many items did the student answer correctly?",
     80, 50, "part"),
    ("A store offers a {rate}% discount on a ₱{whole} item. How much is the discount?",
     10, 300, "part"),
    ("In a class of {whole} students, {rate}% are boys. How many boys are there?",
     60, 40, "part"),
    ("A worker saves {rate}% of a ₱{whole} salary. How much is saved?",
     20, 15000, "part"),
    ("A test has {whole} items. If {rate}% are multiple choice, how many are multiple choice?",
     75, 80, "part"),
    ("A bag contains {whole} marbles. If {rate}% are red, how many red marbles are there?",
     30, 50, "part"),
    ("A school has {whole} teachers. If {rate}% are female, how many female teachers are there?",
     70, 60, "part"),
    ("A farm has {whole} hectares. If {rate}% is planted with rice, how many hectares have rice?",
     40, 200, "part"),
    ("A library has {whole} books. If {rate}% are fiction, how many fiction books are there?",
     25, 800, "part"),
    ("A company has {whole} employees. If {rate}% work overtime, how many work overtime?",
     15, 200, "part"),
    # Finding the rate in context
    ("A student got 36 correct out of {whole} items. What is the percentage score?",
     36, 45, "rate"),
    ("Out of {whole} applicants, 120 were hired. What percentage were hired?",
     120, 400, "rate"),
    ("A team won 18 out of {whole} games. What is the win percentage?",
     18, 24, "rate"),
    ("Out of {whole} products, 15 were defective. What is the defect rate?",
     15, 300, "rate"),
    ("A student answered 28 correctly out of {whole} items. What is the score?",
     28, 35, "rate"),
    ("Out of {whole} registered voters, 360 voted. What percentage voted?",
     360, 600, "rate"),
    ("A factory produced {whole} items and 50 failed inspection. What percent failed?",
     50, 500, "rate"),
    ("Out of {whole} employees, 270 attended the seminar. What percentage attended?",
     270, 450, "rate"),
    ("A survey of {whole} people found 84 prefer tea. What percent prefer tea?",
     84, 120, "rate"),
    ("Out of {whole} deliveries, 48 arrived late. What is the late delivery rate?",
     48, 800, "rate"),
    # Finding the whole in context
    ("A student answered 42 items correctly, which is {rate}% of the total. How many items are on the test?",
     42, 70, "whole"),
    ("₱600 is {rate}% of the total bill. What is the total bill?",
     600, 20, "whole"),
    ("A team won 15 games, which is {rate}% of all games played. How many games were played?",
     15, 60, "whole"),
    ("₱450 represents {rate}% of a worker's daily wage. What is the daily wage?",
     450, 50, "whole"),
    ("24 students passed, which is {rate}% of the class. How many students are in the class?",
     24, 80, "whole"),
    ("A deposit of ₱5,000 is {rate}% of the total price. What is the total price?",
     5000, 25, "whole"),
    ("36 employees are absent, which is {rate}% of the workforce. How many employees are there total?",
     36, 10, "whole"),
    ("₱1,200 is the {rate}% tip on a restaurant bill. What is the bill amount?",
     1200, 15, "whole"),
    ("A candidate received 180 votes, which is {rate}% of total votes. How many total votes were cast?",
     180, 30, "whole"),
    ("₱750 is the {rate}% commission earned. What were the total sales?",
     750, 5, "whole"),
    # More finding the part
    ("What is {rate}% of ₱{whole}?", 5, 2000, "part"),
    ("What is {rate}% of {whole}?", 50, 360, "part"),
    ("What is {rate}% of {whole}?", 20, 750, "part"),
    ("What is {rate}% of ₱{whole}?", 10, 4500, "part"),
    ("What is {rate}% of {whole}?", 25, 480, "part"),
    ("What is {rate}% of {whole}?", 75, 320, "part"),
    ("What is {rate}% of ₱{whole}?", 30, 1200, "part"),
    ("What is {rate}% of {whole}?", 40, 350, "part"),
    ("What is {rate}% of ₱{whole}?", 60, 5000, "part"),
    ("What is {rate}% of {whole}?", 80, 450, "part"),
    # More finding the rate
    ("What percent of {whole} is 56?", 56, 280, "rate"),
    ("What percent of {whole} is 90?", 90, 600, "rate"),
    ("What percent of {whole} is 24?", 24, 160, "rate"),
    ("What percent of {whole} is 35?", 35, 175, "rate"),
    ("What percent of {whole} is 48?", 48, 320, "rate"),
    # More finding the whole
    ("84 is {rate}% of what number?", 84, 60, "whole"),
    ("45 is {rate}% of what number?", 45, 75, "whole"),
    ("39 is {rate}% of what number?", 39, 30, "whole"),
    ("56 is {rate}% of what number?", 56, 80, "whole"),
    ("100 is {rate}% of what number?", 100, 40, "whole"),
]

for item in easy_word_problems:
    template = item[0]
    val1 = item[1]
    val2 = item[2]
    answer_type = item[3]

    if answer_type == "part":
        rate = val1
        whole = val2
        part = rate * whole / 100
        q_text = template.format(rate=rate, whole=fmt(whole))
        choices, ans = make_choices_numeric(int(part))
        expl = f"Convert {rate}% to decimal ({rate/100}) and multiply by {fmt(whole)}: {rate/100} × {fmt(whole)} = {fmt(int(part))}."
        tags = ["percentages", "finding the part", "word problem"]
    elif answer_type == "rate":
        part = val1
        whole = val2
        rate = part / whole * 100
        q_text = template.format(rate=rate, whole=fmt(whole))
        choices, ans = make_choices_pct(rate)
        expl = f"Divide the part by the whole: {fmt(part)} ÷ {fmt(whole)} = {part/whole}. Multiply by 100 to get {fmt_pct(rate)}."
        tags = ["percentages", "finding the percentage", "word problem"]
    else:  # whole
        part = val1
        rate = val2
        whole = part / (rate / 100)
        q_text = template.format(rate=rate, whole=fmt(int(whole)))
        choices, ans = make_choices_numeric(int(whole))
        expl = f"Divide the part by the rate as decimal: {fmt(part)} ÷ {rate/100} = {fmt(int(whole))}."
        tags = ["percentages", "finding the whole", "word problem"]

    add_q("Easy", q_text, choices, ans, expl, tags)


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Finding the Part with larger/decimal rates (201-250) ---
medium_part_data = [
    (12, 750), (18, 450), (22, 1500), (35, 2400), (45, 1800),
    (55, 3200), (65, 4000), (72, 2500), (85, 6000), (95, 4200),
    (8, 12500), (14, 8500), (28, 3500), (33, 9000), (42, 7500),
    (58, 6500), (62, 4800), (78, 3600), (88, 5500), (92, 8000),
    (2.5, 4000), (7.5, 6000), (12.5, 8000), (15, 9200), (17.5, 4000),
    (3, 15000), (6, 25000), (9, 35000), (11, 45000), (13, 55000),
    (16, 18750), (19, 12500), (23, 8000), (27, 15000), (31, 20000),
    (37, 5000), (43, 7000), (47, 9000), (53, 11000), (57, 13000),
    (63, 15000), (67, 17000), (73, 19000), (77, 21000), (83, 23000),
    (87, 25000), (93, 27000), (97, 29000), (4.5, 20000), (5.5, 18000),
]

for rate, whole in medium_part_data:
    part = rate * whole / 100
    if part == int(part):
        part = int(part)
        choices, ans = make_choices_numeric(part)
    else:
        part = round(part, 2)
        choices, ans = make_choices_numeric(part, fmt_func=lambda x: fmt(round(x, 2)))
    add_q("Medium",
          f"What is {fmt_pct(rate)} of {fmt(whole)}?",
          choices, ans,
          f"Convert {fmt_pct(rate)} to decimal: {rate/100}. Multiply: {rate/100} × {fmt(whole)} = {fmt(part)}.",
          ["percentages", "finding the part", "basic percentage problems"])

# --- Medium: Finding the Rate in workplace contexts (251-300) ---
medium_rate_contexts = [
    ("A government office has {whole} employees. If {part} are contractual, what percentage are contractual?",
     45, 300),
    ("Out of a ₱{whole} budget, ₱{part} was spent on supplies. What percentage was spent on supplies?",
     18000, 120000),
    ("A factory produced {whole} units and {part} passed quality control. What is the pass rate?",
     4560, 6000),
    ("In a city of {whole} households, {part} have internet access. What percentage have internet?",
     2700, 4500),
    ("A school has {whole} students. If {part} joined the field trip, what percentage joined?",
     252, 360),
    ("Out of {whole} registered voters, {part} cast their ballots. What is the voter turnout?",
     8400, 12000),
    ("A hospital has {whole} beds. If {part} are occupied, what is the occupancy rate?",
     168, 240),
    ("Out of ₱{whole} in revenue, ₱{part} is profit. What is the profit margin?",
     45000, 300000),
    ("A warehouse received {whole} shipments. If {part} arrived on time, what is the on-time rate?",
     855, 900),
    ("Out of {whole} loan applications, {part} were approved. What is the approval rate?",
     1050, 1500),
    ("A company's {whole} employees were surveyed. {part} expressed satisfaction. What is the satisfaction rate?",
     612, 720),
    ("Out of {whole} items in inventory, {part} are in good condition. What percentage are in good condition?",
     3780, 4200),
    ("A project has {whole} milestones. If {part} are completed, what percentage is complete?",
     56, 80),
    ("Out of {whole} training hours planned, {part} have been delivered. What percentage has been delivered?",
     135, 180),
    ("A fleet of {whole} vehicles was inspected. {part} passed. What is the pass rate?",
     228, 300),
    ("Out of {whole} customer complaints, {part} were resolved within 24 hours. What is the resolution rate?",
     420, 600),
    ("A municipality has {whole} barangays. {part} have completed their development plans. What percentage?",
     27, 36),
    ("Out of {whole} pages in a report, {part} have been reviewed. What percentage has been reviewed?",
     84, 120),
    ("A call center handled {whole} calls. {part} were resolved on first contact. What is the first-call resolution rate?",
     1680, 2400),
    ("Out of {whole} scholarship applicants, {part} qualified. What percentage qualified?",
     375, 500),
    ("A department's {whole} tasks for the quarter are tracked. {part} are done. What percentage is complete?",
     144, 180),
    ("Out of {whole} parcels shipped, {part} arrived undamaged. What is the safe delivery rate?",
     4650, 5000),
    ("A survey of {whole} commuters found {part} use public transport. What percentage use public transport?",
     840, 1200),
    ("Out of {whole} exam takers, {part} scored above 80%. What percentage scored above 80%?",
     270, 450),
    ("A farm harvested {whole} kg of produce. {part} kg met export quality. What percentage met export quality?",
     6300, 9000),
]

for template, part, whole in medium_rate_contexts[:25]:
    rate = part / whole * 100
    q_text = template.format(part=fmt(part), whole=fmt(whole))
    choices, ans = make_choices_pct(rate)
    expl = f"Divide {fmt(part)} by {fmt(whole)}: {fmt(part)} ÷ {fmt(whole)} = {part/whole}. Multiply by 100 = {fmt_pct(rate)}."
    add_q("Medium", q_text, choices, ans, expl,
          ["percentages", "finding the percentage", "workplace context"])


# --- Medium: Finding the Rate (more direct) (301-325) ---
medium_rate_direct = [
    (126, 840), (195, 1300), (288, 1200), (378, 2700), (456, 3800),
    (522, 5800), (648, 7200), (735, 4900), (891, 9900), (972, 10800),
    (1125, 7500), (1350, 9000), (1575, 10500), (1800, 12000), (2025, 13500),
    (2250, 15000), (2475, 16500), (2700, 18000), (2925, 19500), (3150, 21000),
    (3375, 22500), (3600, 24000), (3825, 25500), (4050, 27000), (4275, 28500),
]

for part, whole in medium_rate_direct:
    rate = part / whole * 100
    choices, ans = make_choices_pct(rate)
    add_q("Medium",
          f"What percent of {fmt(whole)} is {fmt(part)}?",
          choices, ans,
          f"Divide {fmt(part)} by {fmt(whole)}: {fmt(part)} ÷ {fmt(whole)} = {part/whole}. Multiply by 100 = {fmt_pct(rate)}.",
          ["percentages", "finding the percentage", "basic percentage problems"])

# --- Medium: Finding the Whole in workplace contexts (326-375) ---
medium_whole_contexts = [
    ("A salesperson earned ₱{part} in commission at a {rate}% rate. What were the total sales?",
     4500, 6),
    ("₱{part} was allocated for training, which is {rate}% of the department budget. What is the total budget?",
     180000, 15),
    ("A candidate received {part} votes, representing {rate}% of total votes. How many total votes were cast?",
     13500, 45),
    ("{part} employees attended the meeting, which is {rate}% of the staff. How many staff members are there?",
     84, 28),
    ("₱{part} in taxes represents {rate}% of gross income. What is the gross income?",
     36000, 12),
    ("A project completed {part} tasks, which is {rate}% of all tasks. How many total tasks are there?",
     126, 42),
    ("{part} students passed the exam, representing {rate}% of test takers. How many took the exam?",
     360, 72),
    ("₱{part} in savings represents {rate}% of monthly income. What is the monthly income?",
     8000, 16),
    ("{part} items were sold, which is {rate}% of inventory. What is the total inventory?",
     450, 18),
    ("A department processed {part} applications, which is {rate}% of submissions. How many were submitted?",
     840, 56),
    ("₱{part} was spent on utilities, representing {rate}% of operating costs. What are total operating costs?",
     27000, 9),
    ("{part} hectares are irrigated, which is {rate}% of total farmland. How many hectares of farmland are there?",
     1200, 48),
    ("₱{part} in interest earned represents a {rate}% annual rate. What is the principal?",
     15000, 5),
    ("{part} buses are operational, which is {rate}% of the fleet. How many buses are in the fleet?",
     72, 80),
    ("₱{part} in penalties represents {rate}% of the contract value. What is the contract value?",
     25000, 2.5),
    ("{part} patients recovered, which is {rate}% of admissions. How many patients were admitted?",
     285, 95),
    ("₱{part} in donations represents {rate}% of the fundraising goal. What is the goal?",
     375000, 75),
    ("{part} parcels were delivered on time, representing {rate}% of shipments. How many shipments were there?",
     1680, 84),
    ("₱{part} in overtime pay represents {rate}% of base salary. What is the base salary?",
     7500, 25),
    ("{part} trees survived, which is {rate}% of those planted. How many trees were planted?",
     540, 90),
    ("₱{part} in fuel costs is {rate}% of the transportation budget. What is the transportation budget?",
     48000, 32),
    ("{part} complaints were resolved, representing {rate}% of total complaints. How many total complaints?",
     210, 70),
    ("₱{part} in rent is {rate}% of monthly expenses. What are total monthly expenses?",
     22500, 30),
    ("{part} units passed inspection, which is {rate}% of production. What is total production?",
     2850, 95),
    ("₱{part} in marketing spend is {rate}% of revenue. What is the revenue?",
     120000, 8),
    ("{part} students enrolled in the program, representing {rate}% of eligible students. How many are eligible?",
     168, 56),
    ("₱{part} in maintenance costs is {rate}% of the building's value. What is the building's value?",
     500000, 2),
    ("{part} vehicles passed emission testing, which is {rate}% of those tested. How many were tested?",
     432, 72),
    ("₱{part} in bonuses represents {rate}% of annual profit. What is the annual profit?",
     250000, 10),
    ("{part} documents were processed, representing {rate}% of the backlog. How many documents are in the backlog?",
     630, 63),
    ("₱{part} in scholarship funds disbursed is {rate}% of the endowment. What is the endowment?",
     840000, 35),
    ("{part} residents participated, which is {rate}% of the community. How many residents are in the community?",
     1500, 12),
    ("₱{part} in equipment costs is {rate}% of the capital budget. What is the capital budget?",
     675000, 45),
    ("{part} calls were answered within 30 seconds, representing {rate}% of all calls. How many calls total?",
     2160, 72),
    ("₱{part} in travel expenses is {rate}% of the annual budget. What is the annual budget?",
     90000, 6),
    ("{part} hectares were reforested, which is {rate}% of the target area. What is the target area?",
     420, 35),
    ("₱{part} in bad debts is {rate}% of total receivables. What are total receivables?",
     54000, 3),
    ("{part} students graduated, representing {rate}% of those who enrolled. How many enrolled?",
     456, 76),
    ("₱{part} in insurance premiums is {rate}% of the insured value. What is the insured value?",
     36000, 1.5),
    ("{part} projects were completed on time, which is {rate}% of all projects. How many projects total?",
     48, 64),
    ("₱{part} in research funding is {rate}% of the university budget. What is the university budget?",
     180000, 12),
    ("{part} employees received promotions, representing {rate}% of eligible staff. How many are eligible?",
     45, 15),
    ("₱{part} in export revenue is {rate}% of total revenue. What is total revenue?",
     2400000, 40),
    ("{part} patients were vaccinated, which is {rate}% of the target population. What is the target?",
     7200, 60),
    ("₱{part} in penalties collected is {rate}% of violations issued. What is the total value of violations?",
     135000, 9),
    ("{part} units were recalled, representing {rate}% of production. What is total production?",
     180, 1.5),
    ("₱{part} in grants disbursed is {rate}% of approved funding. What is approved funding?",
     450000, 75),
    ("{part} applications were denied, which is {rate}% of submissions. How many were submitted?",
     96, 8),
    ("₱{part} in dividends is {rate}% of investment. What is the investment?",
     60000, 4),
    ("{part} seats were filled, representing {rate}% of capacity. What is the capacity?",
     270, 90),
]

for template, part, rate in medium_whole_contexts:
    whole = part / (rate / 100)
    if whole == int(whole):
        whole = int(whole)
    else:
        whole = round(whole, 2)
    q_text = template.format(part=fmt(part), rate=fmt_pct(rate).replace('%', ''))
    if isinstance(whole, int) or whole == int(whole):
        choices, ans = make_choices_numeric(int(whole))
    else:
        choices, ans = make_choices_numeric(whole, fmt_func=lambda x: fmt(round(x, 2)))
    expl = f"Divide the part by the rate as decimal: {fmt(part)} ÷ {rate/100} = {fmt(int(whole) if whole == int(whole) else whole)}."
    add_q("Medium", q_text, choices, ans, expl,
          ["percentages", "finding the whole", "workplace context"])


# --- Medium: Discount/Tax/Salary word problems (376-400) ---
medium_applied = [
    ("A laptop costs ₱{price}. If there is a {rate}% discount, what is the sale price?",
     35000, 15, "discount"),
    ("An item costs ₱{price} before VAT. With {rate}% VAT, what is the total price?",
     8500, 12, "add_tax"),
    ("A government employee earns ₱{price} monthly. After a {rate}% raise, what is the new salary?",
     28000, 10, "increase"),
    ("A phone originally costs ₱{price}. It is on sale at {rate}% off. What is the sale price?",
     18000, 20, "discount"),
    ("A meal costs ₱{price}. With a {rate}% service charge, what is the total?",
     1200, 10, "add_tax"),
    ("An employee's salary is ₱{price}. If {rate}% is deducted for taxes, what is the take-home pay?",
     32000, 15, "deduct"),
    ("A TV costs ₱{price}. A {rate}% discount is applied. What is the discounted price?",
     45000, 25, "discount"),
    ("A product costs ₱{price}. After adding {rate}% markup, what is the selling price?",
     5000, 40, "increase"),
    ("A worker earns ₱{price} daily. If {rate}% goes to transportation, how much is left for other expenses?",
     800, 20, "deduct"),
    ("A house costs ₱{price}. The buyer pays a {rate}% down payment. How much is the down payment?",
     2500000, 20, "part_only"),
    ("A car costs ₱{price}. Insurance is {rate}% of the car's value per year. How much is the annual insurance?",
     850000, 3, "part_only"),
    ("A contractor quotes ₱{price}. A {rate}% penalty is charged for late completion. How much is the penalty?",
     500000, 5, "part_only"),
    ("A loan of ₱{price} has a {rate}% annual interest rate. How much interest is charged in one year?",
     200000, 12, "part_only"),
    ("A company's revenue is ₱{price}. If {rate}% is profit, how much is the profit?",
     1500000, 18, "part_only"),
    ("A budget of ₱{price} allocates {rate}% to personnel. How much goes to personnel?",
     3000000, 45, "part_only"),
    ("A shipment of ₱{price} worth of goods has {rate}% damaged. What is the value of damaged goods?",
     750000, 4, "part_only"),
    ("A city's annual budget is ₱{price}. If {rate}% goes to infrastructure, how much is that?",
     50000000, 22, "part_only"),
    ("An investment of ₱{price} yields {rate}% return. How much is the return?",
     400000, 8, "part_only"),
    ("A school's budget is ₱{price}. {rate}% is allocated for teacher training. How much is allocated?",
     2000000, 7, "part_only"),
    ("A factory's output is {price} units. If {rate}% are premium grade, how many premium units are produced?",
     12000, 35, "part_only"),
    ("A hospital's budget is ₱{price}. {rate}% goes to medical supplies. How much is spent on supplies?",
     8000000, 28, "part_only"),
    ("A farm produces {price} kg of crops. {rate}% is exported. How many kg are exported?",
     50000, 42, "part_only"),
    ("A company has {price} customers. {rate}% renewed their contracts. How many renewed?",
     8000, 85, "part_only"),
    ("A warehouse stores {price} items. {rate}% are perishable. How many perishable items are stored?",
     15000, 24, "part_only"),
    ("A government agency processes {price} applications monthly. {rate}% are approved. How many are approved?",
     6000, 68, "part_only"),
]

for template, price, rate, problem_type in medium_applied:
    if problem_type == "discount":
        discount = price * rate / 100
        answer = price - discount
        q_text = template.format(price=fmt(price), rate=rate)
        choices, ans = make_choices_money(int(answer))
        expl = f"Discount = {rate}% of {fmt_money(price)} = {fmt_money(int(discount))}. Sale price = {fmt_money(price)} - {fmt_money(int(discount))} = {fmt_money(int(answer))}."
    elif problem_type == "add_tax":
        tax = price * rate / 100
        answer = price + tax
        q_text = template.format(price=fmt(price), rate=rate)
        choices, ans = make_choices_money(int(answer))
        expl = f"Tax/charge = {rate}% of {fmt_money(price)} = {fmt_money(int(tax))}. Total = {fmt_money(price)} + {fmt_money(int(tax))} = {fmt_money(int(answer))}."
    elif problem_type == "increase":
        increase = price * rate / 100
        answer = price + increase
        q_text = template.format(price=fmt(price), rate=rate)
        choices, ans = make_choices_money(int(answer))
        expl = f"Increase = {rate}% of {fmt_money(price)} = {fmt_money(int(increase))}. New amount = {fmt_money(price)} + {fmt_money(int(increase))} = {fmt_money(int(answer))}."
    elif problem_type == "deduct":
        deduction = price * rate / 100
        answer = price - deduction
        q_text = template.format(price=fmt(price), rate=rate)
        choices, ans = make_choices_money(int(answer))
        expl = f"Deduction = {rate}% of {fmt_money(price)} = {fmt_money(int(deduction))}. Remaining = {fmt_money(price)} - {fmt_money(int(deduction))} = {fmt_money(int(answer))}."
    else:  # part_only
        answer = price * rate / 100
        q_text = template.format(price=fmt(price), rate=rate)
        if answer >= 1000:
            choices, ans = make_choices_money(int(answer))
        else:
            choices, ans = make_choices_numeric(int(answer))
        expl = f"Multiply: {rate}% of {fmt(price)} = {rate/100} × {fmt(price)} = {fmt(int(answer))}."

    add_q("Medium", q_text, choices, ans, expl,
          ["percentages", "applied percentage", "workplace context"])


# --- Medium: Additional percentage interpretation (to reach 200) ---
medium_extra = [
    ("If 28% of a number is 84, what is 50% of the same number?",
     84 / 0.28 * 0.50, "The number = 84 ÷ 0.28 = 300. 50% of 300 = 150."),
    ("If 15% of a number is 45, what is 40% of the same number?",
     45 / 0.15 * 0.40, "The number = 45 ÷ 0.15 = 300. 40% of 300 = 120."),
    ("If 20% of a number is 60, what is 75% of the same number?",
     60 / 0.20 * 0.75, "The number = 60 ÷ 0.20 = 300. 75% of 300 = 225."),
    ("If 35% of a number is 140, what is 60% of the same number?",
     140 / 0.35 * 0.60, "The number = 140 ÷ 0.35 = 400. 60% of 400 = 240."),
    ("If 12% of a number is 36, what is 25% of the same number?",
     36 / 0.12 * 0.25, "The number = 36 ÷ 0.12 = 300. 25% of 300 = 75."),
    ("A class has 45 students. If 80% passed math and 60% passed science, and everyone passed at least one, what is the maximum number who passed both?",
     45 * 0.60, "Maximum overlap = min(80%, 60%) of 45 = 60% × 45 = 27 students."),
    ("An item's price was ₱400. After a 25% increase, what is the new price?",
     400 * 1.25, "New price = ₱400 × 1.25 = ₱500."),
    ("An item's price was ₱600. After a 15% decrease, what is the new price?",
     600 * 0.85, "New price = ₱600 × 0.85 = ₱510."),
    ("A population of 50,000 decreased by 4%. What is the new population?",
     50000 * 0.96, "New population = 50,000 × 0.96 = 48,000."),
    ("A salary of ₱22,000 increased by 12%. What is the new salary?",
     22000 * 1.12, "New salary = ₱22,000 × 1.12 = ₱24,640."),
    ("If a number is increased by 50%, the result is 450. What is the number?",
     450 / 1.50, "Number × 1.50 = 450. Number = 450 ÷ 1.50 = 300."),
    ("If a number is decreased by 20%, the result is 320. What is the number?",
     320 / 0.80, "Number × 0.80 = 320. Number = 320 ÷ 0.80 = 400."),
    ("A store sold 240 items on Monday and 300 items on Tuesday. What is the percentage increase from Monday to Tuesday?",
     (300 - 240) / 240 * 100, "Increase = 60. Rate = 60 ÷ 240 × 100 = 25%."),
    ("A company's expenses dropped from ₱500,000 to ₱425,000. What is the percentage decrease?",
     (500000 - 425000) / 500000 * 100, "Decrease = ₱75,000. Rate = 75,000 ÷ 500,000 × 100 = 15%."),
    ("Production increased from 8,000 to 9,200 units. What is the percentage increase?",
     (9200 - 8000) / 8000 * 100, "Increase = 1,200. Rate = 1,200 ÷ 8,000 × 100 = 15%."),
    ("A town's population went from 40,000 to 38,000. What is the percentage decrease?",
     (40000 - 38000) / 40000 * 100, "Decrease = 2,000. Rate = 2,000 ÷ 40,000 × 100 = 5%."),
    ("Revenue grew from ₱1,200,000 to ₱1,500,000. What is the percentage growth?",
     (1500000 - 1200000) / 1200000 * 100, "Growth = ₱300,000. Rate = 300,000 ÷ 1,200,000 × 100 = 25%."),
    ("A test score improved from 60 to 78. What is the percentage improvement?",
     (78 - 60) / 60 * 100, "Improvement = 18. Rate = 18 ÷ 60 × 100 = 30%."),
    ("Enrollment dropped from 1,500 to 1,350. What is the percentage decrease?",
     (1500 - 1350) / 1500 * 100, "Decrease = 150. Rate = 150 ÷ 1,500 × 100 = 10%."),
    ("A stock price rose from ₱80 to ₱100. What is the percentage increase?",
     (100 - 80) / 80 * 100, "Increase = ₱20. Rate = 20 ÷ 80 × 100 = 25%."),
    ("Fuel consumption decreased from 500 liters to 450 liters. What is the percentage decrease?",
     (500 - 450) / 500 * 100, "Decrease = 50. Rate = 50 ÷ 500 × 100 = 10%."),
    ("A worker's output increased from 120 units to 150 units per day. What is the percentage increase?",
     (150 - 120) / 120 * 100, "Increase = 30. Rate = 30 ÷ 120 × 100 = 25%."),
    ("A company's debt decreased from ₱2,000,000 to ₱1,600,000. What is the percentage reduction?",
     (2000000 - 1600000) / 2000000 * 100, "Reduction = ₱400,000. Rate = 400,000 ÷ 2,000,000 × 100 = 20%."),
    ("Crime incidents dropped from 800 to 680 in a year. What is the percentage decrease?",
     (800 - 680) / 800 * 100, "Decrease = 120. Rate = 120 ÷ 800 × 100 = 15%."),
    ("A school's passing rate improved from 72% to 81%. What is the percentage point increase?",
     81 - 72, "Percentage point increase = 81% - 72% = 9 percentage points."),
]

for q_text, answer, expl in medium_extra:
    answer_val = round(answer)
    if "percentage" in q_text.lower() or "percent" in q_text.lower() and "₱" not in str(answer_val):
        if answer_val <= 100:
            choices, ans = make_choices_pct(answer_val)
        else:
            choices, ans = make_choices_numeric(answer_val)
    elif answer_val >= 1000:
        choices, ans = make_choices_money(answer_val)
    else:
        choices, ans = make_choices_numeric(answer_val)
    add_q("Medium", q_text, choices, ans, expl,
          ["percentages", "percentage change", "interpretation"])


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Multi-step percentage problems (401-450) ---
hard_multistep = [
    # (description, computation steps)
    ("A shirt costs ₱1,500. It is discounted by 20%, then an additional 10% off the discounted price. What is the final price?",
     1500 * 0.80 * 0.90,
     "First discount: 20% off ₱1,500 = ₱1,500 × 0.80 = ₱1,200. Second discount: 10% off ₱1,200 = ₱1,200 × 0.90 = ₱1,080."),
    ("An employee earns ₱40,000. Deductions: 12% tax, 4% PhilHealth, 2% Pag-IBIG (all on gross). What is the net pay?",
     40000 * (1 - 0.12 - 0.04 - 0.02),
     "Total deductions = 12% + 4% + 2% = 18%. Net pay = ₱40,000 × (1 - 0.18) = ₱40,000 × 0.82 = ₱32,800."),
    ("A budget of ₱5,000,000 allocates 40% to personnel and 25% to operations. How much remains for capital outlay?",
     5000000 * (1 - 0.40 - 0.25),
     "Remaining = 100% - 40% - 25% = 35%. Capital outlay = 35% × ₱5,000,000 = ₱1,750,000."),
    ("A product costs ₱2,000. A 30% markup is applied, then a 10% discount on the marked-up price. What is the final selling price?",
     2000 * 1.30 * 0.90,
     "Marked-up price = ₱2,000 × 1.30 = ₱2,600. After 10% discount: ₱2,600 × 0.90 = ₱2,340."),
    ("A company has 500 employees. 60% are male. Of the males, 25% are managers. How many male managers are there?",
     500 * 0.60 * 0.25,
     "Males = 60% of 500 = 300. Male managers = 25% of 300 = 75."),
    ("A school has 1,200 students. 55% are female. Of the females, 40% are honor students. How many female honor students?",
     1200 * 0.55 * 0.40,
     "Females = 55% of 1,200 = 660. Female honor students = 40% of 660 = 264."),
    ("A city has 80,000 households. 70% have electricity. Of those with electricity, 45% have internet. How many have internet?",
     80000 * 0.70 * 0.45,
     "With electricity = 70% of 80,000 = 56,000. With internet = 45% of 56,000 = 25,200."),
    ("A factory produces 10,000 units. 95% pass initial inspection. Of those that pass, 90% pass final inspection. How many pass both?",
     10000 * 0.95 * 0.90,
     "Pass initial = 95% of 10,000 = 9,500. Pass both = 90% of 9,500 = 8,550."),
    ("A store's revenue is ₱800,000. Cost of goods is 60% of revenue. Operating expenses are 25% of revenue. What is the profit?",
     800000 * (1 - 0.60 - 0.25),
     "Profit = 100% - 60% - 25% = 15% of revenue. Profit = 15% × ₱800,000 = ₱120,000."),
    ("An item costs ₱3,500. First a 15% discount is applied, then 12% VAT is added to the discounted price. What is the final price?",
     3500 * 0.85 * 1.12,
     "After discount: ₱3,500 × 0.85 = ₱2,975. After VAT: ₱2,975 × 1.12 = ₱3,332."),
    ("A salary of ₱50,000 gets a 6% increase. From the new salary, 10% is deducted for tax. What is the take-home pay?",
     50000 * 1.06 * 0.90,
     "New salary = ₱50,000 × 1.06 = ₱53,000. After tax: ₱53,000 × 0.90 = ₱47,700."),
    ("A population of 200,000 grows by 5% in year 1, then 3% in year 2. What is the population after 2 years?",
     200000 * 1.05 * 1.03,
     "After year 1: 200,000 × 1.05 = 210,000. After year 2: 210,000 × 1.03 = 216,300."),
    ("A company's 2,000 employees: 45% are in operations, 30% in admin, rest in sales. How many are in sales?",
     2000 * (1 - 0.45 - 0.30),
     "Sales = 100% - 45% - 30% = 25%. Sales employees = 25% × 2,000 = 500."),
    ("A project budget is ₱10,000,000. Phase 1 uses 35%, Phase 2 uses 40% of the remainder. How much is left for Phase 3?",
     10000000 * (1 - 0.35) * (1 - 0.40),
     "After Phase 1: ₱10,000,000 × 0.65 = ₱6,500,000. After Phase 2: ₱6,500,000 × 0.60 = ₱3,900,000."),
    ("A farmer harvests 8,000 kg. 10% is lost to spoilage. Of the remainder, 75% is sold locally. How many kg are sold locally?",
     8000 * 0.90 * 0.75,
     "After spoilage: 8,000 × 0.90 = 7,200 kg. Sold locally: 7,200 × 0.75 = 5,400 kg."),
    ("A tank holds 5,000 liters. 20% evaporates in week 1. 15% of the remainder evaporates in week 2. How much is left?",
     5000 * 0.80 * 0.85,
     "After week 1: 5,000 × 0.80 = 4,000 L. After week 2: 4,000 × 0.85 = 3,400 L."),
    ("A store buys goods for ₱120,000. It marks up by 50%, then offers a 20% sale. What is the sale price?",
     120000 * 1.50 * 0.80,
     "Marked-up: ₱120,000 × 1.50 = ₱180,000. Sale price: ₱180,000 × 0.80 = ₱144,000."),
    ("A survey of 3,000 people: 52% are female. Of females, 65% support a policy. How many females support it?",
     3000 * 0.52 * 0.65,
     "Females = 52% of 3,000 = 1,560. Supporters = 65% of 1,560 = 1,014."),
    ("A company's revenue dropped 10% in Q1, then grew 20% in Q2 (from Q1 level). If original revenue was ₱2,000,000, what is Q2 revenue?",
     2000000 * 0.90 * 1.20,
     "Q1 revenue: ₱2,000,000 × 0.90 = ₱1,800,000. Q2 revenue: ₱1,800,000 × 1.20 = ₱2,160,000."),
    ("A school's 800 students: 35% are in STEM. Of STEM students, 60% are male. How many male STEM students?",
     800 * 0.35 * 0.60,
     "STEM students = 35% of 800 = 280. Male STEM = 60% of 280 = 168."),
]

for q_text, answer, expl in hard_multistep[:20]:
    answer = int(round(answer))
    choices, ans = make_choices_numeric(answer, fmt_func=lambda x: fmt_money(int(x)) if answer >= 1000 else fmt(int(x)))
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "multi-step", "applied percentage"])


# --- Hard: Reverse percentage (finding original after increase/decrease) (451-500) ---
hard_reverse = [
    ("After a 20% increase, an employee's salary is ₱36,000. What was the original salary?",
     36000, 1.20, "₱36,000 = 1.20 × Original. Original = ₱36,000 ÷ 1.20 = ₱30,000."),
    ("After a 25% discount, a TV costs ₱22,500. What was the original price?",
     22500, 0.75, "₱22,500 = 0.75 × Original. Original = ₱22,500 ÷ 0.75 = ₱30,000."),
    ("After a 10% price increase, a product costs ₱5,500. What was the original price?",
     5500, 1.10, "₱5,500 = 1.10 × Original. Original = ₱5,500 ÷ 1.10 = ₱5,000."),
    ("After a 15% salary raise, an employee earns ₱34,500. What was the previous salary?",
     34500, 1.15, "₱34,500 = 1.15 × Original. Original = ₱34,500 ÷ 1.15 = ₱30,000."),
    ("After a 30% discount, a bag costs ₱2,100. What was the original price?",
     2100, 0.70, "₱2,100 = 0.70 × Original. Original = ₱2,100 ÷ 0.70 = ₱3,000."),
    ("After a 5% increase, rent is ₱15,750. What was the previous rent?",
     15750, 1.05, "₱15,750 = 1.05 × Original. Original = ₱15,750 ÷ 1.05 = ₱15,000."),
    ("After a 40% markup, an item sells for ₱8,400. What was the cost?",
     8400, 1.40, "₱8,400 = 1.40 × Cost. Cost = ₱8,400 ÷ 1.40 = ₱6,000."),
    ("After a 12% tax deduction, take-home pay is ₱35,200. What is the gross salary?",
     35200, 0.88, "₱35,200 = 0.88 × Gross. Gross = ₱35,200 ÷ 0.88 = ₱40,000."),
    ("After a 35% discount, a dress costs ₱3,250. What was the original price?",
     3250, 0.65, "₱3,250 = 0.65 × Original. Original = ₱3,250 ÷ 0.65 = ₱5,000."),
    ("After an 8% raise, a worker earns ₱27,000. What was the previous wage?",
     27000, 1.08, "₱27,000 = 1.08 × Original. Original = ₱27,000 ÷ 1.08 = ₱25,000."),
    ("After a 50% increase, production is 9,000 units. What was the original production?",
     9000, 1.50, "9,000 = 1.50 × Original. Original = 9,000 ÷ 1.50 = 6,000 units."),
    ("After a 20% decrease, enrollment is 4,800. What was the previous enrollment?",
     4800, 0.80, "4,800 = 0.80 × Original. Original = 4,800 ÷ 0.80 = 6,000."),
    ("After a 15% discount, a gadget costs ₱12,750. What was the original price?",
     12750, 0.85, "₱12,750 = 0.85 × Original. Original = ₱12,750 ÷ 0.85 = ₱15,000."),
    ("After a 6% salary increase, monthly pay is ₱42,400. What was the previous salary?",
     42400, 1.06, "₱42,400 = 1.06 × Original. Original = ₱42,400 ÷ 1.06 = ₱40,000."),
    ("After a 10% decrease in staff, a company has 450 employees. How many did it have before?",
     450, 0.90, "450 = 0.90 × Original. Original = 450 ÷ 0.90 = 500 employees."),
    ("After a 25% increase, a city's population is 250,000. What was the previous population?",
     250000, 1.25, "250,000 = 1.25 × Original. Original = 250,000 ÷ 1.25 = 200,000."),
    ("After a 45% discount, a sofa costs ₱16,500. What was the original price?",
     16500, 0.55, "₱16,500 = 0.55 × Original. Original = ₱16,500 ÷ 0.55 = ₱30,000."),
    ("After a 2% monthly interest charge, a loan balance is ₱51,000. What was the principal?",
     51000, 1.02, "₱51,000 = 1.02 × Principal. Principal = ₱51,000 ÷ 1.02 = ₱50,000."),
    ("After a 18% tax, net income is ₱328,000. What is the gross income?",
     328000, 0.82, "₱328,000 = 0.82 × Gross. Gross = ₱328,000 ÷ 0.82 = ₱400,000."),
    ("After a 60% increase in funding, a program's budget is ₱4,800,000. What was the original budget?",
     4800000, 1.60, "₱4,800,000 = 1.60 × Original. Original = ₱4,800,000 ÷ 1.60 = ₱3,000,000."),
    ("After a 5% decrease, water consumption is 9,500 liters. What was the previous consumption?",
     9500, 0.95, "9,500 = 0.95 × Original. Original = 9,500 ÷ 0.95 = 10,000 liters."),
    ("After a 30% increase, a company's profit is ₱1,950,000. What was the previous profit?",
     1950000, 1.30, "₱1,950,000 = 1.30 × Original. Original = ₱1,950,000 ÷ 1.30 = ₱1,500,000."),
    ("After a 22% discount, a refrigerator costs ₱23,400. What was the original price?",
     23400, 0.78, "₱23,400 = 0.78 × Original. Original = ₱23,400 ÷ 0.78 = ₱30,000."),
    ("After a 4% raise, a pension is ₱20,800. What was the previous pension?",
     20800, 1.04, "₱20,800 = 1.04 × Original. Original = ₱20,800 ÷ 1.04 = ₱20,000."),
    ("After a 16% decrease in crime, a city reports 2,100 incidents. How many were there before?",
     2100, 0.84, "2,100 = 0.84 × Original. Original = 2,100 ÷ 0.84 = 2,500 incidents."),
    ("After a 75% increase, a stock price is ₱350. What was the original price?",
     350, 1.75, "₱350 = 1.75 × Original. Original = ₱350 ÷ 1.75 = ₱200."),
    ("After a 8% discount, a service fee is ₱4,600. What was the original fee?",
     4600, 0.92, "₱4,600 = 0.92 × Original. Original = ₱4,600 ÷ 0.92 = ₱5,000."),
    ("After a 12% increase, monthly expenses are ₱56,000. What were they before?",
     56000, 1.12, "₱56,000 = 1.12 × Original. Original = ₱56,000 ÷ 1.12 = ₱50,000."),
    ("After a 33⅓% discount, a painting costs ₱40,000. What was the original price?",
     40000, 2/3, "₱40,000 = (2/3) × Original. Original = ₱40,000 ÷ (2/3) = ₱40,000 × 1.5 = ₱60,000."),
    ("After a 20% decrease in output, a factory produces 12,000 units. What was the previous output?",
     12000, 0.80, "12,000 = 0.80 × Original. Original = 12,000 ÷ 0.80 = 15,000 units."),
]

for q_text, final_value, multiplier, expl in hard_reverse[:30]:
    original = final_value / multiplier
    original = int(round(original))
    if original >= 1000:
        choices, ans = make_choices_money(original)
    else:
        choices, ans = make_choices_numeric(original)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "reverse percentage", "finding original value"])


# --- Hard: Percentage comparison and interpretation (501-550) ---
hard_comparison = [
    ("Department A has 150 employees with 80% attendance. Department B has 200 employees with 65% attendance. Which department has more employees present, and by how many?",
     150 * 0.80 - 200 * 0.65, "A: 80% of 150 = 120. B: 65% of 200 = 130. Department B has more by 10.",
     "Department B by 10"),
    ("Store A earned ₱500,000 with a 20% profit margin. Store B earned ₱800,000 with a 12% profit margin. Which store made more profit, and how much more?",
     800000 * 0.12 - 500000 * 0.20, "A: 20% of ₱500,000 = ₱100,000. B: 12% of ₱800,000 = ₱96,000. Store A made ₱4,000 more.",
     "Store A by ₱4,000"),
    ("City X has 50,000 voters with 72% turnout. City Y has 40,000 voters with 85% turnout. Which city had more voters turn out?",
     50000 * 0.72, "X: 72% of 50,000 = 36,000. Y: 85% of 40,000 = 34,000. City X had more (36,000 vs 34,000).",
     "City X with 36,000"),
    ("Factory A produces 5,000 units with 3% defect rate. Factory B produces 8,000 units with 2% defect rate. Which has more defective units?",
     8000 * 0.02, "A: 3% of 5,000 = 150. B: 2% of 8,000 = 160. Factory B has more defective units (160 vs 150).",
     "Factory B with 160"),
    ("School A has 600 students with 85% passing rate. School B has 450 students with 92% passing rate. How many more students passed in School A?",
     600 * 0.85 - 450 * 0.92, "A: 85% of 600 = 510. B: 92% of 450 = 414. School A has 96 more passers.",
     "96"),
]

# Generate these as structured questions
comparison_questions = [
    # Simpler comparison format for multiple choice
    ("Department A has 200 employees with 75% attendance. Department B has 150 employees with 90% attendance. How many employees are present in Department A?",
     int(200 * 0.75), "75% of 200 = 0.75 × 200 = 150 employees present."),
    ("Department A has 200 employees with 75% attendance. Department B has 150 employees with 90% attendance. How many employees are present in Department B?",
     int(150 * 0.90), "90% of 150 = 0.90 × 150 = 135 employees present."),
    ("A company allocates 35% of ₱2,000,000 to Project X and 28% of ₱3,000,000 to Project Y. How much does Project X receive?",
     int(2000000 * 0.35), "35% of ₱2,000,000 = 0.35 × 2,000,000 = ₱700,000."),
    ("A company allocates 35% of ₱2,000,000 to Project X and 28% of ₱3,000,000 to Project Y. How much does Project Y receive?",
     int(3000000 * 0.28), "28% of ₱3,000,000 = 0.28 × 3,000,000 = ₱840,000."),
    ("Region A has 120,000 residents with 68% employment rate. How many are employed?",
     int(120000 * 0.68), "68% of 120,000 = 0.68 × 120,000 = 81,600."),
    ("Region B has 95,000 residents with 74% employment rate. How many are employed?",
     int(95000 * 0.74), "74% of 95,000 = 0.74 × 95,000 = 70,300."),
    ("A survey shows 55% of 2,000 urban respondents and 42% of 3,000 rural respondents support a policy. How many urban supporters are there?",
     int(2000 * 0.55), "55% of 2,000 = 0.55 × 2,000 = 1,100."),
    ("A survey shows 55% of 2,000 urban respondents and 42% of 3,000 rural respondents support a policy. How many rural supporters are there?",
     int(3000 * 0.42), "42% of 3,000 = 0.42 × 3,000 = 1,260."),
    ("Hospital A has 300 beds with 88% occupancy. How many beds are occupied?",
     int(300 * 0.88), "88% of 300 = 0.88 × 300 = 264 beds."),
    ("Hospital B has 450 beds with 76% occupancy. How many beds are occupied?",
     int(450 * 0.76), "76% of 450 = 0.76 × 450 = 342 beds."),
    ("Branch A sold 4,000 units with 15% return rate. How many units were returned?",
     int(4000 * 0.15), "15% of 4,000 = 0.15 × 4,000 = 600 units."),
    ("Branch B sold 6,000 units with 8% return rate. How many units were returned?",
     int(6000 * 0.08), "8% of 6,000 = 0.08 × 6,000 = 480 units."),
    ("Team A completed 85% of 200 assigned tasks. How many tasks did Team A complete?",
     int(200 * 0.85), "85% of 200 = 0.85 × 200 = 170 tasks."),
    ("Team B completed 92% of 150 assigned tasks. How many tasks did Team B complete?",
     int(150 * 0.92), "92% of 150 = 0.92 × 150 = 138 tasks."),
    ("A farm produces 12,000 kg with 5% wastage. How many kg are wasted?",
     int(12000 * 0.05), "5% of 12,000 = 0.05 × 12,000 = 600 kg."),
    ("A farm produces 8,000 kg with 7.5% wastage. How many kg are wasted?",
     int(8000 * 0.075), "7.5% of 8,000 = 0.075 × 8,000 = 600 kg."),
    ("Candidate A received 45% of 80,000 votes. How many votes did Candidate A get?",
     int(80000 * 0.45), "45% of 80,000 = 0.45 × 80,000 = 36,000 votes."),
    ("Candidate B received 38% of 80,000 votes. How many votes did Candidate B get?",
     int(80000 * 0.38), "38% of 80,000 = 0.38 × 80,000 = 30,400 votes."),
    ("A company's Q1 revenue is ₱1,200,000 with 22% profit margin. What is the Q1 profit?",
     int(1200000 * 0.22), "22% of ₱1,200,000 = 0.22 × 1,200,000 = ₱264,000."),
    ("A company's Q2 revenue is ₱1,500,000 with 18% profit margin. What is the Q2 profit?",
     int(1500000 * 0.18), "18% of ₱1,500,000 = 0.18 × 1,500,000 = ₱270,000."),
    ("A school's Grade 10 has 320 students with 78% passing rate. How many passed?",
     int(320 * 0.78), "78% of 320 = 0.78 × 320 = 249.6 ≈ 250 students."),
    ("A school's Grade 11 has 280 students with 82% passing rate. How many passed?",
     int(280 * 0.82), "82% of 280 = 0.82 × 280 = 229.6 ≈ 230 students."),
    ("An office has 45 staff with 20% on leave. How many are on leave?",
     int(45 * 0.20), "20% of 45 = 0.20 × 45 = 9 staff."),
    ("An office has 60 staff with 15% on leave. How many are on leave?",
     int(60 * 0.15), "15% of 60 = 0.15 × 60 = 9 staff."),
    ("A warehouse has 25,000 items with 1.2% damage rate. How many items are damaged?",
     int(25000 * 0.012), "1.2% of 25,000 = 0.012 × 25,000 = 300 items."),
    ("A warehouse has 40,000 items with 0.8% damage rate. How many items are damaged?",
     int(40000 * 0.008), "0.8% of 40,000 = 0.008 × 40,000 = 320 items."),
    ("A fleet of 80 buses has 92.5% operational rate. How many are operational?",
     int(80 * 0.925), "92.5% of 80 = 0.925 × 80 = 74 buses."),
    ("A fleet of 120 buses has 85% operational rate. How many are operational?",
     int(120 * 0.85), "85% of 120 = 0.85 × 120 = 102 buses."),
    ("A bank has ₱50,000,000 in deposits with 3.5% interest rate. How much interest is paid annually?",
     int(50000000 * 0.035), "3.5% of ₱50,000,000 = 0.035 × 50,000,000 = ₱1,750,000."),
    ("A bank has ₱80,000,000 in deposits with 2.25% interest rate. How much interest is paid annually?",
     int(80000000 * 0.0225), "2.25% of ₱80,000,000 = 0.0225 × 80,000,000 = ₱1,800,000."),
]

for q_text, answer, expl in comparison_questions[:30]:
    if answer >= 10000:
        choices, ans = make_choices_money(answer)
    else:
        choices, ans = make_choices_numeric(answer)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "comparison", "interpretation"])


# --- Hard: Complex word problems with decimal/fractional rates (551-580) ---
hard_complex_rates = [
    ("A company's annual revenue is ₱45,000,000. If 2.8% goes to research and development, how much is the R&D budget?",
     45000000 * 0.028, "2.8% of ₱45,000,000 = 0.028 × 45,000,000 = ₱1,260,000."),
    ("A city's population of 1,250,000 grew by 1.6% last year. How many people were added?",
     1250000 * 0.016, "1.6% of 1,250,000 = 0.016 × 1,250,000 = 20,000 people."),
    ("An investment of ₱2,500,000 yields 4.8% annual return. How much is earned in one year?",
     2500000 * 0.048, "4.8% of ₱2,500,000 = 0.048 × 2,500,000 = ₱120,000."),
    ("A factory's defect rate is 0.5%. If 200,000 units are produced, how many are defective?",
     200000 * 0.005, "0.5% of 200,000 = 0.005 × 200,000 = 1,000 units."),
    ("A loan of ₱1,800,000 charges 1.25% monthly interest. How much interest is charged per month?",
     1800000 * 0.0125, "1.25% of ₱1,800,000 = 0.0125 × 1,800,000 = ₱22,500."),
    ("A government bond worth ₱500,000 pays 6.5% annual interest. How much interest is received per year?",
     500000 * 0.065, "6.5% of ₱500,000 = 0.065 × 500,000 = ₱32,500."),
    ("A company's 15,000 employees have a 0.8% absentee rate daily. How many are absent on a typical day?",
     15000 * 0.008, "0.8% of 15,000 = 0.008 × 15,000 = 120 employees."),
    ("A hospital's 2,400 annual admissions have a 3.75% readmission rate. How many readmissions occur?",
     2400 * 0.0375, "3.75% of 2,400 = 0.0375 × 2,400 = 90 readmissions."),
    ("A municipality collected ₱12,500,000 in taxes. If 0.4% is allocated to disaster preparedness, how much is that?",
     12500000 * 0.004, "0.4% of ₱12,500,000 = 0.004 × 12,500,000 = ₱50,000."),
    ("A shipping company delivers 75,000 packages monthly with a 1.8% loss rate. How many packages are lost?",
     75000 * 0.018, "1.8% of 75,000 = 0.018 × 75,000 = 1,350 packages."),
    ("A bank's ₱3,200,000,000 in assets has a 0.15% non-performing loan ratio. What is the value of non-performing loans?",
     3200000000 * 0.0015, "0.15% of ₱3,200,000,000 = 0.0015 × 3,200,000,000 = ₱4,800,000."),
    ("A power plant operates at 87.5% efficiency. If input energy is 16,000 megawatts, how much useful energy is produced?",
     16000 * 0.875, "87.5% of 16,000 = 0.875 × 16,000 = 14,000 megawatts."),
    ("A school's 1,800 students have a 97.5% attendance rate. How many are present on a typical day?",
     1800 * 0.975, "97.5% of 1,800 = 0.975 × 1,800 = 1,755 students."),
    ("A construction project's ₱25,000,000 budget has a 3.2% contingency fund. How much is the contingency?",
     25000000 * 0.032, "3.2% of ₱25,000,000 = 0.032 × 25,000,000 = ₱800,000."),
    ("A farm's 4,500 hectares has 2.4% allocated to organic farming. How many hectares are organic?",
     4500 * 0.024, "2.4% of 4,500 = 0.024 × 4,500 = 108 hectares."),
    ("An airline's 12,000 flights per month have a 99.2% on-time rate. How many flights are on time?",
     12000 * 0.992, "99.2% of 12,000 = 0.992 × 12,000 = 11,904 flights."),
    ("A company's ₱8,000,000 payroll has 6.25% allocated to bonuses. How much is the bonus pool?",
     8000000 * 0.0625, "6.25% of ₱8,000,000 = 0.0625 × 8,000,000 = ₱500,000."),
    ("A reservoir holds 2,000,000 liters. If 0.75% evaporates daily, how many liters evaporate per day?",
     2000000 * 0.0075, "0.75% of 2,000,000 = 0.0075 × 2,000,000 = 15,000 liters."),
    ("A university's 8,500 graduates have a 94.5% employment rate within 6 months. How many are employed?",
     8500 * 0.945, "94.5% of 8,500 = 0.945 × 8,500 = 8,032.5 ≈ 8,033 graduates."),
    ("A government agency's ₱150,000,000 budget allocates 0.6% to staff wellness programs. How much is allocated?",
     150000000 * 0.006, "0.6% of ₱150,000,000 = 0.006 × 150,000,000 = ₱900,000."),
    ("A telecom company has 2,500,000 subscribers with a 1.4% monthly churn rate. How many subscribers leave per month?",
     2500000 * 0.014, "1.4% of 2,500,000 = 0.014 × 2,500,000 = 35,000 subscribers."),
    ("A city's 350,000 registered vehicles have a 2.6% accident rate annually. How many accidents occur?",
     350000 * 0.026, "2.6% of 350,000 = 0.026 × 350,000 = 9,100 accidents."),
    ("A pharmaceutical company produces 500,000 tablets with 99.8% purity rate. How many meet purity standards?",
     500000 * 0.998, "99.8% of 500,000 = 0.998 × 500,000 = 499,000 tablets."),
    ("A solar farm generates 8,000 kWh daily at 22.5% efficiency from 35,556 kWh of solar input. How much energy is generated?",
     8000, "22.5% efficiency means 22.5% of input becomes output. Output = 0.225 × 35,556 ≈ 8,000 kWh."),
    ("A water treatment plant processes 5,000,000 liters daily with 0.02% contamination rate. How many liters are contaminated?",
     5000000 * 0.0002, "0.02% of 5,000,000 = 0.0002 × 5,000,000 = 1,000 liters."),
    ("A call center's 500 agents have a 4.6% daily absence rate. How many agents are absent on a typical day?",
     500 * 0.046, "4.6% of 500 = 0.046 × 500 = 23 agents."),
    ("A mining company extracts 120,000 tons of ore with 3.5% mineral content. How many tons of mineral are extracted?",
     120000 * 0.035, "3.5% of 120,000 = 0.035 × 120,000 = 4,200 tons."),
    ("A retail chain's ₱75,000,000 annual sales has a 1.8% shrinkage rate. What is the value of shrinkage?",
     75000000 * 0.018, "1.8% of ₱75,000,000 = 0.018 × 75,000,000 = ₱1,350,000."),
    ("A province's 450,000 hectares of forest lost 0.3% to deforestation last year. How many hectares were lost?",
     450000 * 0.003, "0.3% of 450,000 = 0.003 × 450,000 = 1,350 hectares."),
    ("A blood bank has 8,000 units in storage with a 2.25% expiration rate monthly. How many units expire per month?",
     8000 * 0.0225, "2.25% of 8,000 = 0.0225 × 8,000 = 180 units."),
]

for q_text, answer, expl in hard_complex_rates:
    answer = int(round(answer))
    if answer >= 10000:
        choices, ans = make_choices_money(answer)
    else:
        choices, ans = make_choices_numeric(answer)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "decimal rates", "applied percentage"])


# --- Hard: Finding the Whole with complex contexts (581-600) ---
hard_whole_complex = [
    ("A company's bad debt expense of ₱2,700,000 represents 1.8% of total receivables. What are total receivables?",
     2700000, 1.8, "₱2,700,000 ÷ 0.018 = ₱150,000,000."),
    ("A hospital's 135 ICU patients represent 4.5% of total admissions. How many total admissions?",
     135, 4.5, "135 ÷ 0.045 = 3,000 admissions."),
    ("A city's 7,500 reported crimes represent 0.6% of the population. What is the population?",
     7500, 0.6, "7,500 ÷ 0.006 = 1,250,000."),
    ("A factory's 420 rejected items represent 2.8% of production. What is total production?",
     420, 2.8, "420 ÷ 0.028 = 15,000 units."),
    ("A scholarship fund disbursed ₱3,750,000, which is 12.5% of the endowment. What is the endowment?",
     3750000, 12.5, "₱3,750,000 ÷ 0.125 = ₱30,000,000."),
    ("An insurance claim of ₱180,000 represents 7.2% of the policy value. What is the policy value?",
     180000, 7.2, "₱180,000 ÷ 0.072 = ₱2,500,000."),
    ("A company's 84 overseas employees represent 3.5% of total staff. How many total employees?",
     84, 3.5, "84 ÷ 0.035 = 2,400 employees."),
    ("A province's 2,250 hectares of protected forest is 0.9% of total land area. What is the total land area?",
     2250, 0.9, "2,250 ÷ 0.009 = 250,000 hectares."),
    ("A bank's ₱4,500,000 in non-performing loans is 0.25% of total assets. What are total assets?",
     4500000, 0.25, "₱4,500,000 ÷ 0.0025 = ₱1,800,000,000."),
    ("A university's 156 PhD holders represent 6.5% of faculty. How many faculty members are there?",
     156, 6.5, "156 ÷ 0.065 = 2,400 faculty."),
    ("A government agency's ₱960,000 travel budget is 1.6% of its total budget. What is the total budget?",
     960000, 1.6, "₱960,000 ÷ 0.016 = ₱60,000,000."),
    ("A company's 225 customer complaints represent 0.15% of transactions. How many transactions?",
     225, 0.15, "225 ÷ 0.0015 = 150,000 transactions."),
    ("A farm's 840 organic hectares represent 5.6% of total farmland. How many hectares total?",
     840, 5.6, "840 ÷ 0.056 = 15,000 hectares."),
    ("A city's 18,000 electric vehicles represent 2.4% of registered vehicles. How many vehicles are registered?",
     18000, 2.4, "18,000 ÷ 0.024 = 750,000 vehicles."),
    ("A company's ₱1,125,000 advertising spend is 4.5% of revenue. What is the revenue?",
     1125000, 4.5, "₱1,125,000 ÷ 0.045 = ₱25,000,000."),
    ("A school's 48 special education students represent 3.2% of enrollment. What is total enrollment?",
     48, 3.2, "48 ÷ 0.032 = 1,500 students."),
    ("A hospital's ₱2,400,000 equipment maintenance cost is 0.8% of equipment value. What is the equipment value?",
     2400000, 0.8, "₱2,400,000 ÷ 0.008 = ₱300,000,000."),
    ("A telecom company's 42,000 dropped calls represent 1.4% of total calls. How many total calls?",
     42000, 1.4, "42,000 ÷ 0.014 = 3,000,000 calls."),
    ("A municipality's 675 building permits represent 2.7% of total structures. How many structures?",
     675, 2.7, "675 ÷ 0.027 = 25,000 structures."),
    ("A company's ₱540,000 training budget is 0.36% of annual revenue. What is annual revenue?",
     540000, 0.36, "₱540,000 ÷ 0.0036 = ₱150,000,000."),
]

for q_text, part, rate, expl in hard_whole_complex:
    whole = part / (rate / 100)
    whole = int(round(whole))
    if whole >= 10000:
        choices, ans = make_choices_money(whole)
    else:
        choices, ans = make_choices_numeric(whole)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "finding the whole", "complex context"])


# --- Hard: Additional multi-step and CSE-style (to fill remaining hard slots) ---
hard_additional = [
    ("A government employee's gross salary is ₱55,000. After 10% income tax and 3% PhilHealth deduction, what is the net pay?",
     55000 * (1 - 0.10 - 0.03), "Total deductions = 13%. Net = ₱55,000 × 0.87 = ₱47,850."),
    ("A store bought goods for ₱80,000 and sold them at a 35% profit. What is the selling price?",
     80000 * 1.35, "Selling price = ₱80,000 × 1.35 = ₱108,000."),
    ("A town's 25,000 households: 64% have water supply, 48% have sewage. If 36% have both, how many have at least one?",
     25000 * (0.64 + 0.48 - 0.36), "At least one = (64% + 48% - 36%) × 25,000 = 76% × 25,000 = 19,000."),
    ("A company's expenses: 42% salaries, 18% rent, 12% utilities, 8% supplies. What percentage remains for other costs?",
     100 - 42 - 18 - 12 - 8, "Remaining = 100% - 42% - 18% - 12% - 8% = 20%."),
    ("A product's price increased by 25% then decreased by 20%. If the final price is ₱6,000, what was the original?",
     6000 / (1.25 * 0.80), "Final = Original × 1.25 × 0.80 = Original × 1.00. Original = ₱6,000 ÷ 1.00 = ₱6,000."),
    ("A school has 1,500 students. 40% are in STEM, 35% in ABM, and the rest in HUMSS. How many are in HUMSS?",
     1500 * 0.25, "HUMSS = 100% - 40% - 35% = 25%. Students = 25% × 1,500 = 375."),
    ("A worker earns ₱18,000 monthly. If living expenses are 65% and savings are 20%, how much is left for leisure?",
     18000 * (1 - 0.65 - 0.20), "Leisure = 100% - 65% - 20% = 15%. Amount = 15% × ₱18,000 = ₱2,700."),
    ("A batch of 2,500 products: 92% pass first inspection. Of failures, 50% are reworked successfully. How many total good products?",
     2500 * 0.92 + 2500 * 0.08 * 0.50, "Pass first: 2,300. Failures: 200. Reworked: 100. Total good: 2,300 + 100 = 2,400."),
    ("A company's revenue grew 15% from Year 1 to Year 2, and 10% from Year 2 to Year 3. If Year 3 revenue is ₱7,590,000, what was Year 1?",
     7590000 / (1.15 * 1.10), "Year 1 × 1.15 × 1.10 = ₱7,590,000. Year 1 = ₱7,590,000 ÷ 1.265 = ₱6,000,000."),
    ("A tank is 75% full with 4,500 liters. If 20% of the water is used, how many liters remain?",
     4500 * 0.80, "Water remaining = 4,500 × 0.80 = 3,600 liters."),
    ("An office has 80 staff. 25% took vacation in January, 30% in February (different people). What percentage took no vacation in either month?",
     100 - 25 - 30, "No vacation = 100% - 25% - 30% = 45%."),
    ("A farmer sold 60% of his 5,000 kg harvest at ₱50/kg and the rest at ₱35/kg. What is the total revenue?",
     5000 * 0.60 * 50 + 5000 * 0.40 * 35, "Revenue = (3,000 × ₱50) + (2,000 × ₱35) = ₱150,000 + ₱70,000 = ₱220,000."),
    ("A loan of ₱100,000 at 12% annual interest compounded annually. What is the balance after 1 year?",
     100000 * 1.12, "Balance = ₱100,000 × 1.12 = ₱112,000."),
    ("A city's budget: 50% for services, 30% for infrastructure. If services get ₱75,000,000, how much does infrastructure get?",
     75000000 / 0.50 * 0.30, "Total budget = ₱75,000,000 ÷ 0.50 = ₱150,000,000. Infrastructure = 30% × ₱150,000,000 = ₱45,000,000."),
    ("A company's 3,000 employees: 55% male. Of males, 20% are in management. Of females, 15% are in management. How many total managers?",
     3000 * 0.55 * 0.20 + 3000 * 0.45 * 0.15, "Male managers: 1,650 × 0.20 = 330. Female managers: 1,350 × 0.15 = 202.5 ≈ 203. Total ≈ 533."),
    ("A product costs ₱4,000. After 20% markup and then 12% VAT on the marked-up price, what does the customer pay?",
     4000 * 1.20 * 1.12, "Marked up: ₱4,000 × 1.20 = ₱4,800. With VAT: ₱4,800 × 1.12 = ₱5,376."),
    ("A survey of 4,000 people: 45% male. Of males, 60% exercise regularly. Of females, 70% exercise regularly. How many exercise regularly?",
     4000 * 0.45 * 0.60 + 4000 * 0.55 * 0.70, "Males exercising: 1,800 × 0.60 = 1,080. Females: 2,200 × 0.70 = 1,540. Total = 2,620."),
    ("A building's value is ₱12,000,000. Annual depreciation is 5%. What is the value after 1 year?",
     12000000 * 0.95, "Value after 1 year = ₱12,000,000 × 0.95 = ₱11,400,000."),
    ("A company allocates 8% of ₱25,000,000 revenue to marketing. Of the marketing budget, 40% goes to digital ads. How much for digital ads?",
     25000000 * 0.08 * 0.40, "Marketing = 8% × ₱25,000,000 = ₱2,000,000. Digital = 40% × ₱2,000,000 = ₱800,000."),
    ("A government project received ₱8,000,000. If 15% is for admin costs and 70% of the remainder is for construction, how much is for construction?",
     8000000 * 0.85 * 0.70, "After admin: ₱8,000,000 × 0.85 = ₱6,800,000. Construction: ₱6,800,000 × 0.70 = ₱4,760,000."),
    ("A company had 800 employees. It hired 10% more, then 5% of the new total resigned. How many employees remain?",
     800 * 1.10 * 0.95, "After hiring: 800 × 1.10 = 880. After resignations: 880 × 0.95 = 836."),
    ("A store's inventory of 6,000 items: 30% are electronics, 45% are clothing, rest are groceries. How many grocery items?",
     6000 * 0.25, "Groceries = 100% - 30% - 45% = 25%. Items = 25% × 6,000 = 1,500."),
    ("A municipality's ₱20,000,000 budget: 55% for personnel, 20% for MOOE. The rest is for capital outlay. How much for capital outlay?",
     20000000 * 0.25, "Capital = 100% - 55% - 20% = 25%. Amount = 25% × ₱20,000,000 = ₱5,000,000."),
    ("A factory's 4,000 workers: 85% are regular, rest are contractual. If 10% of regular workers get promoted, how many are promoted?",
     4000 * 0.85 * 0.10, "Regular = 85% × 4,000 = 3,400. Promoted = 10% × 3,400 = 340."),
    ("A school's 2,000 students: 48% are female. Of females, 30% are scholars. Of males, 25% are scholars. How many total scholars?",
     2000 * 0.48 * 0.30 + 2000 * 0.52 * 0.25, "Female scholars: 960 × 0.30 = 288. Male scholars: 1,040 × 0.25 = 260. Total = 548."),
    ("A company's profit was ₱2,000,000 last year. It increased by 15% this year. Next year it's projected to increase by 20% from this year. What is the projected profit?",
     2000000 * 1.15 * 1.20, "This year: ₱2,000,000 × 1.15 = ₱2,300,000. Next year: ₱2,300,000 × 1.20 = ₱2,760,000."),
    ("A water tank holds 10,000 liters. 15% is used on Day 1, then 20% of the remainder on Day 2. How much is left after Day 2?",
     10000 * 0.85 * 0.80, "After Day 1: 10,000 × 0.85 = 8,500. After Day 2: 8,500 × 0.80 = 6,800 liters."),
    ("A company's 5,000 products: 4% are defective. Of defective items, 75% can be repaired. How many cannot be repaired?",
     5000 * 0.04 * 0.25, "Defective = 4% × 5,000 = 200. Cannot repair = 25% × 200 = 50."),
    ("A budget of ₱3,000,000: 40% for salaries, 15% for rent, 10% for utilities. How much remains for other expenses?",
     3000000 * (1 - 0.40 - 0.15 - 0.10), "Remaining = 35% × ₱3,000,000 = ₱1,050,000."),
    ("A real estate agent earns 3% commission on the first ₱1,000,000 and 5% on the amount above ₱1,000,000. If a property sold for ₱3,500,000, what is the total commission?",
     1000000 * 0.03 + 2500000 * 0.05, "First ₱1M: 3% × 1,000,000 = ₱30,000. Above: 5% × 2,500,000 = ₱125,000. Total = ₱155,000."),
    ("A company's sales: Q1 = ₱1,200,000, Q2 = ₱1,500,000, Q3 = ₱1,800,000, Q4 = ₱2,100,000. What percentage of annual sales occurred in Q4?",
     2100000 / (1200000 + 1500000 + 1800000 + 2100000) * 100, "Annual = ₱6,600,000. Q4 rate = 2,100,000 ÷ 6,600,000 × 100 ≈ 31.82%."),
    ("A government office has 120 staff. 75% are permanent, 15% are contractual, and the rest are job-order. How many are job-order?",
     120 * 0.10, "Job-order = 100% - 75% - 15% = 10%. Staff = 10% × 120 = 12."),
    ("A company's ₱4,000,000 revenue: 60% from Product A, 25% from Product B, rest from Product C. How much from Product C?",
     4000000 * 0.15, "Product C = 15% × ₱4,000,000 = ₱600,000."),
    ("A hospital has 500 beds. Monday occupancy is 84%, Tuesday is 76%. How many more beds are occupied on Monday?",
     500 * 0.84 - 500 * 0.76, "Monday: 420. Tuesday: 380. Difference = 40 beds."),
    ("A salary of ₱30,000 has the following deductions: SSS 4.5%, PhilHealth 2%, Pag-IBIG 2%, tax 8%. What is the net pay?",
     30000 * (1 - 0.045 - 0.02 - 0.02 - 0.08), "Total deductions = 16.5%. Net = ₱30,000 × 0.835 = ₱25,050."),
    ("A project is 40% complete after spending ₱3,200,000. What is the estimated total project cost?",
     3200000 / 0.40, "Total = ₱3,200,000 ÷ 0.40 = ₱8,000,000."),
    ("A company's workforce: 2,400 in Year 1, grew 8% in Year 2, then 5% in Year 3. How many employees in Year 3?",
     2400 * 1.08 * 1.05, "Year 2: 2,400 × 1.08 = 2,592. Year 3: 2,592 × 1.05 = 2,721.6 ≈ 2,722."),
    ("A store offers 'buy 2 get 1 free' on ₱500 items. What is the effective discount percentage?",
     (500 / (3 * 500)) * 100, "You pay for 2 but get 3. Savings = ₱500 out of ₱1,500 = 33.33%."),
    ("A government agency's budget increased from ₱45,000,000 to ₱54,000,000. What is the percentage increase?",
     (54000000 - 45000000) / 45000000 * 100, "Increase = ₱9,000,000. Rate = 9,000,000 ÷ 45,000,000 × 100 = 20%."),
    ("A company's profit margin decreased from 25% to 20%. If revenue stayed at ₱10,000,000, how much less profit was earned?",
     10000000 * 0.25 - 10000000 * 0.20, "Old profit: ₱2,500,000. New profit: ₱2,000,000. Difference = ₱500,000."),
    ("A farm's yield: 80% of 5,000 kg is Grade A (₱60/kg), rest is Grade B (₱35/kg). What is total revenue?",
     5000 * 0.80 * 60 + 5000 * 0.20 * 35, "Grade A: 4,000 × ₱60 = ₱240,000. Grade B: 1,000 × ₱35 = ₱35,000. Total = ₱275,000."),
    ("A company's 1,000 employees: 60% attended training. Of attendees, 85% passed the assessment. How many passed?",
     1000 * 0.60 * 0.85, "Attendees = 600. Passed = 85% × 600 = 510."),
    ("A municipality collected ₱8,000,000 in taxes. 45% goes to the general fund, 30% to development, rest to reserves. How much to reserves?",
     8000000 * 0.25, "Reserves = 100% - 45% - 30% = 25%. Amount = 25% × ₱8,000,000 = ₱2,000,000."),
    ("A product's cost is ₱1,200. Markup is 60%. A loyal customer gets 15% off the selling price. What does the customer pay?",
     1200 * 1.60 * 0.85, "Selling price = ₱1,200 × 1.60 = ₱1,920. Customer pays: ₱1,920 × 0.85 = ₱1,632."),
    ("A school's enrollment: 1,800 in 2023, decreased 5% in 2024, then increased 10% in 2025. What is 2025 enrollment?",
     1800 * 0.95 * 1.10, "2024: 1,800 × 0.95 = 1,710. 2025: 1,710 × 1.10 = 1,881."),
    ("A company's ₱6,000,000 annual budget: 35% Q1, 25% Q2, 22% Q3, rest Q4. How much is the Q4 budget?",
     6000000 * (1 - 0.35 - 0.25 - 0.22), "Q4 = 18% × ₱6,000,000 = ₱1,080,000."),
    ("A warehouse ships 3,000 orders. 5% are returned. Of returns, 60% are refunded and 40% are exchanged. How many are refunded?",
     3000 * 0.05 * 0.60, "Returns = 5% × 3,000 = 150. Refunded = 60% × 150 = 90."),
    ("A bank offers 4% interest on savings. If a depositor earned ₱18,000 in interest, what is the deposit amount?",
     18000 / 0.04, "Deposit = ₱18,000 ÷ 0.04 = ₱450,000."),
    ("A company's revenue: ₱3,000,000 domestic (growing 10% annually) and ₱2,000,000 international (growing 15% annually). What is total revenue next year?",
     3000000 * 1.10 + 2000000 * 1.15, "Domestic: ₱3,300,000. International: ₱2,300,000. Total = ₱5,600,000."),
    ("A government employee contributes 5% of ₱35,000 salary to SSS and the employer matches 8%. What is the total monthly SSS contribution?",
     35000 * 0.05 + 35000 * 0.08, "Employee: ₱1,750. Employer: ₱2,800. Total = ₱4,550."),
]

for q_text, answer, expl in hard_additional:
    answer = int(round(answer))
    if answer >= 1000:
        choices, ans = make_choices_money(answer)
    elif answer <= 100 and ("percent" in q_text.lower() or "%" in expl):
        choices, ans = make_choices_pct(answer)
    else:
        choices, ans = make_choices_numeric(answer)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "multi-step", "CSE-style"])

# --- Hard: Final batch to reach 200 hard questions ---
hard_final = [
    ("A company's total assets are ₱15,000,000. Liabilities are 65% of assets. What is the equity (assets minus liabilities)?",
     15000000 * (1 - 0.65), "Liabilities = 65% × ₱15,000,000 = ₱9,750,000. Equity = ₱15,000,000 - ₱9,750,000 = ₱5,250,000."),
    ("A school's 1,200 students took an exam. 75% passed. Of those who failed, 40% will retake. How many will retake?",
     1200 * 0.25 * 0.40, "Failed = 25% × 1,200 = 300. Retakers = 40% × 300 = 120."),
    ("A company's monthly expenses: ₱120,000 rent (fixed) plus 8% of revenue for commissions. If revenue is ₱2,500,000, what are total expenses?",
     120000 + 2500000 * 0.08, "Commissions = 8% × ₱2,500,000 = ₱200,000. Total = ₱120,000 + ₱200,000 = ₱320,000."),
    ("A product's price was ₱800. It increased by 50%, then the new price decreased by 40%. What is the final price?",
     800 * 1.50 * 0.60, "After increase: ₱800 × 1.50 = ₱1,200. After decrease: ₱1,200 × 0.60 = ₱720."),
    ("A government agency has 600 employees. 80% are permanent. Of permanent staff, 15% have master's degrees. How many permanent staff have master's degrees?",
     600 * 0.80 * 0.15, "Permanent = 480. With master's = 15% × 480 = 72."),
    ("A company's sales team of 50 people: each has a target of ₱500,000. If the team achieved 88% of total target, what is total actual sales?",
     50 * 500000 * 0.88, "Total target = 50 × ₱500,000 = ₱25,000,000. Actual = 88% × ₱25,000,000 = ₱22,000,000."),
    ("A city's water supply: 40% from dams, 35% from groundwater, rest from rainwater harvesting. If total supply is 500,000,000 liters, how much from rainwater?",
     500000000 * 0.25, "Rainwater = 100% - 40% - 35% = 25%. Amount = 25% × 500,000,000 = 125,000,000 liters."),
    ("A hospital's 400 nurses: 70% work day shift, 20% night shift, 10% rotating. If 5% of day-shift nurses are on leave, how many day-shift nurses are working?",
     400 * 0.70 * 0.95, "Day shift = 280. Working = 95% × 280 = 266."),
    ("A company earned ₱5,000,000 in Q1. Q2 was 20% higher than Q1. Q3 was 10% lower than Q2. What was Q3 revenue?",
     5000000 * 1.20 * 0.90, "Q2 = ₱5,000,000 × 1.20 = ₱6,000,000. Q3 = ₱6,000,000 × 0.90 = ₱5,400,000."),
    ("A farm has 2,000 animals: 45% cattle, 30% goats, rest poultry. If 12% of cattle are sold, how many cattle remain?",
     2000 * 0.45 * 0.88, "Cattle = 900. After selling 12%: 900 × 0.88 = 792."),
    ("A project's ₱6,000,000 budget: Phase 1 spent 30%, Phase 2 spent 45% of the original budget. How much is left for Phase 3?",
     6000000 * (1 - 0.30 - 0.45), "Remaining = 25% × ₱6,000,000 = ₱1,500,000."),
    ("A company's 10,000 customers: 65% are active. Of active customers, 20% made a purchase this month. How many purchased this month?",
     10000 * 0.65 * 0.20, "Active = 6,500. Purchased = 20% × 6,500 = 1,300."),
    ("A salary of ₱45,000 is subject to: 5% SSS, 2% PhilHealth, 2% Pag-IBIG, and 15% income tax. What is the total deduction amount?",
     45000 * (0.05 + 0.02 + 0.02 + 0.15), "Total rate = 24%. Deductions = 24% × ₱45,000 = ₱10,800."),
    ("A store's inventory worth ₱2,400,000: 55% is fast-moving, 30% is slow-moving, rest is dead stock. What is the value of dead stock?",
     2400000 * 0.15, "Dead stock = 15% × ₱2,400,000 = ₱360,000."),
    ("A company's workforce grew from 1,500 to 1,800 over 2 years. What is the total percentage growth?",
     (1800 - 1500) / 1500 * 100, "Growth = 300 ÷ 1,500 × 100 = 20%."),
    ("A government office processed 5,000 permits. 88% were approved, 7% were denied, rest are pending. How many are pending?",
     5000 * 0.05, "Pending = 100% - 88% - 7% = 5%. Count = 5% × 5,000 = 250."),
    ("A company's ₱3,500,000 marketing budget: 45% for TV ads, 30% for digital, 15% for print, rest for events. How much for events?",
     3500000 * 0.10, "Events = 100% - 45% - 30% - 15% = 10%. Amount = 10% × ₱3,500,000 = ₱350,000."),
    ("A factory's output increased 12% from January to February, then decreased 8% from February to March. If January output was 5,000 units, what was March output?",
     5000 * 1.12 * 0.92, "February: 5,000 × 1.12 = 5,600. March: 5,600 × 0.92 = 5,152."),
    ("A loan of ₱250,000 at 10% annual interest. After paying ₱50,000 of principal, interest is recalculated. What is the new annual interest?",
     (250000 - 50000) * 0.10, "New principal = ₱200,000. Interest = 10% × ₱200,000 = ₱20,000."),
    ("A company's 800 employees: 40% in Manila, 35% in Cebu, rest in Davao. If Manila office grows by 10%, how many total employees will the company have?",
     800 * 0.40 * 1.10 + 800 * 0.35 + 800 * 0.25, "Manila: 320 × 1.10 = 352. Cebu: 280. Davao: 200. Total = 832."),
]

for q_text, answer, expl in hard_final:
    answer = int(round(answer))
    if answer >= 1000:
        choices, ans = make_choices_money(answer)
    elif answer <= 100 and ("percent" in q_text.lower() or "%" in expl):
        choices, ans = make_choices_pct(answer)
    else:
        choices, ans = make_choices_numeric(answer)
    add_q("Hard", q_text, choices, ans, expl,
          ["percentages", "multi-step", "CSE-style"])

# Verify counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Total questions: {len(questions)}")
print(f"  Easy: {easy_count}")
print(f"  Medium: {medium_count}")
print(f"  Hard: {hard_count}")

# Reassign sequential IDs
for i, q in enumerate(questions, 1):
    q["id"] = i

# Write output
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
output_dir = project_root / "data" / "seed" / "questions" / "numerical-ability" / "percentages" / "basic-percentage-problems"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\nWritten to: {output_path}")
