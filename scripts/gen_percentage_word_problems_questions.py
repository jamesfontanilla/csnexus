"""
Generate 600 questions for Percentage Word Problems (CSE Numerical Ability).
200 Easy / 200 Medium / 200 Hard

Covers:
- Translating word problems into equations
- Finding the part, whole, or rate
- Multi-step percentage problems
- Discounts, taxes, commissions
- Salary and payroll computations
- Population and survey applications
- Business profit/loss scenarios
- Successive percentage changes
- Reverse percentage problems
- Percentage comparison and interpretation

Run: python scripts/gen_percentage_word_problems_questions.py
Output: data/seed/questions/numerical-ability/percentages/percentage-word-problems/questions.json
"""

import json
import random
from pathlib import Path

random.seed(42)

questions: list[dict] = []
qid = 0

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "numerical-ability" / "percentages"
    / "percentage-word-problems" / "questions.json"
)


def add_q(difficulty: str, question: str, choices: list[str],
           answer: str, explanation: str, tags: list[str]) -> None:
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Percentage Word Problems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def fmt_peso(val: float) -> str:
    """Format a peso value."""
    if val == int(val):
        return f"\u20b1{int(val):,}"
    return f"\u20b1{val:,.2f}"


def fmt_num(val: float) -> str:
    """Format a number nicely."""
    if val == int(val):
        return f"{int(val):,}"
    s = f"{val:.2f}".rstrip("0").rstrip(".")
    return s


def make_peso_choices(correct: float, spread: float = 0.2) -> tuple[list[str], str]:
    """Generate 4 peso-value choices with plausible distractors."""
    correct_str = fmt_peso(correct)
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_small", "off_medium", "wrong_base", "complement", "double_pct"
        ])
        if error_type == "off_small":
            d = correct * (1 + random.choice([-0.05, -0.10, 0.05, 0.10, 0.15, -0.15]))
        elif error_type == "off_medium":
            d = correct + random.choice([-500, -200, -100, 100, 200, 500, 1000, -1000])
        elif error_type == "wrong_base":
            d = correct * random.choice([0.8, 1.2, 0.9, 1.1, 1.25, 0.75])
        elif error_type == "complement":
            d = correct * random.choice([0.5, 2.0, 1.5, 0.67])
        else:
            d = correct * random.choice([1.12, 0.88, 1.3, 0.7])
        d = round(d, 2)
        if d == int(d):
            d = int(d)
        d_str = fmt_peso(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1
    while len(distractors) < 3:
        d = correct + (len(distractors) + 1) * 500
        d_str = fmt_peso(d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


def make_number_choices(correct: float) -> tuple[list[str], str]:
    """Generate 4 numeric choices with plausible distractors."""
    correct_str = fmt_num(correct)
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_small", "off_medium", "wrong_op", "complement"
        ])
        if error_type == "off_small":
            d = correct + random.choice([-5, -10, -15, 5, 10, 15, 20, -20])
        elif error_type == "off_medium":
            d = correct * random.choice([0.8, 1.2, 0.9, 1.1, 0.75, 1.25, 1.5, 0.5])
        elif error_type == "wrong_op":
            d = correct + random.choice([-50, -30, 30, 50, 100, -100])
        else:
            d = correct * random.choice([0.6, 1.4, 0.85, 1.15])
        d = round(d, 2)
        if d == int(d):
            d = int(d)
        d_str = fmt_num(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1
    while len(distractors) < 3:
        d = correct + (len(distractors) + 1) * 10
        d_str = fmt_num(d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


def make_pct_choices(correct: float) -> tuple[list[str], str]:
    """Generate 4 percentage choices with plausible distractors."""
    correct_str = f"{fmt_num(correct)}%"
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_small", "off_medium", "complement", "double", "half"
        ])
        if error_type == "off_small":
            d = correct + random.choice([-5, -3, -2, 2, 3, 5, 8, -8])
        elif error_type == "off_medium":
            d = correct + random.choice([-10, -15, 10, 15, 20, -20])
        elif error_type == "complement":
            d = 100 - correct
        elif error_type == "double":
            d = correct * 2
        else:
            d = correct / 2
        d = round(d, 2)
        if d == int(d):
            d = int(d)
        d_str = f"{fmt_num(d)}%"
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1
    while len(distractors) < 3:
        d = correct + (len(distractors) + 1) * 5
        d_str = f"{fmt_num(d)}%"
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- E1: Finding the Part (percent of a number) ---
# Template: "X% of Y is ___"
e1_data = [
    (10, 500), (20, 300), (25, 800), (50, 600), (15, 400),
    (30, 1000), (5, 2000), (40, 750), (75, 1200), (10, 3000),
    (20, 4500), (25, 2400), (50, 1800), (60, 500), (35, 2000),
    (12, 2500), (8, 5000), (45, 800), (80, 350), (90, 200),
    (15, 6000), (25, 3600), (10, 8000), (20, 1500), (30, 2500),
]

contexts_e1 = [
    ("A government office has {whole} employees. If {pct}% are assigned to fieldwork, "
     "how many employees are in fieldwork?"),
    ("A school has {whole} students. If {pct}% joined the science fair, "
     "how many students joined?"),
    ("A barangay has {whole} registered voters. If {pct}% voted in the last election, "
     "how many voted?"),
    ("A company has {whole} items in stock. If {pct}% are defective, "
     "how many items are defective?"),
    ("Out of {whole} applicants, {pct}% passed the screening. "
     "How many applicants passed?"),
]

random.shuffle(e1_data)
for i, (pct, whole) in enumerate(e1_data):
    part = pct / 100 * whole
    ctx = contexts_e1[i % len(contexts_e1)]
    q_text = ctx.format(whole=f"{whole:,}", pct=pct)
    choices, answer = make_number_choices(part)
    explanation = f"{pct}% of {whole:,} = {pct/100} \u00d7 {whole:,} = {fmt_num(part)}."
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the part", "basic application"])


# --- E2: Finding the Part (peso amounts) ---
e2_data = [
    (10, 5000), (20, 8000), (25, 12000), (15, 20000), (30, 6000),
    (5, 10000), (50, 4000), (40, 15000), (12, 25000), (8, 50000),
    (35, 10000), (75, 8000), (60, 5000), (45, 20000), (25, 16000),
    (10, 45000), (20, 35000), (15, 30000), (5, 80000), (30, 12000),
    (25, 40000), (50, 18000), (10, 25000), (20, 22000), (40, 9000),
]

contexts_e2 = [
    ("An employee earns \u20b1{whole:,} monthly. If {pct}% goes to rent, "
     "how much is spent on rent?"),
    ("A budget of \u20b1{whole:,} allocates {pct}% to supplies. "
     "How much is allocated to supplies?"),
    ("A family's monthly income is \u20b1{whole:,}. They save {pct}% each month. "
     "How much do they save?"),
    ("A project costs \u20b1{whole:,}. If {pct}% has been spent so far, "
     "how much has been spent?"),
    ("A store's daily revenue is \u20b1{whole:,}. If {pct}% comes from online sales, "
     "how much comes from online sales?"),
]

random.shuffle(e2_data)
for i, (pct, whole) in enumerate(e2_data):
    part = pct / 100 * whole
    ctx = contexts_e2[i % len(contexts_e2)]
    q_text = ctx.format(whole=whole, pct=pct)
    choices, answer = make_peso_choices(part)
    explanation = f"{pct}% of \u20b1{whole:,} = {pct/100} \u00d7 {whole:,} = {fmt_peso(part)}."
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the part", "peso amounts"])


# --- E3: Finding the Rate (what percent is X of Y?) ---
e3_data = [
    (30, 100), (45, 150), (60, 200), (18, 90), (24, 80),
    (36, 120), (50, 250), (75, 300), (40, 160), (90, 360),
    (15, 60), (28, 140), (35, 175), (48, 240), (72, 360),
    (20, 50), (12, 48), (56, 280), (63, 420), (80, 200),
    (100, 400), (150, 500), (27, 180), (42, 210), (55, 220),
]

contexts_e3 = [
    ("In a class of {whole} students, {part} passed the exam. "
     "What percentage of students passed?"),
    ("Out of {whole} items produced, {part} passed quality control. "
     "What percentage passed?"),
    ("A survey of {whole} residents found that {part} support the new policy. "
     "What percentage support it?"),
    ("Out of {whole} registered voters, {part} actually voted. "
     "What is the voter turnout percentage?"),
    ("A company received {whole} applications. If {part} were qualified, "
     "what percentage were qualified?"),
]

random.shuffle(e3_data)
for i, (part, whole) in enumerate(e3_data):
    rate = part / whole * 100
    ctx = contexts_e3[i % len(contexts_e3)]
    q_text = ctx.format(whole=whole, part=part)
    choices, answer = make_pct_choices(rate)
    explanation = f"{part} \u00f7 {whole} = {part/whole} = {fmt_num(rate)}%."
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the rate", "basic application"])


# --- E4: Finding the Whole (X is Y% of what number?) ---
e4_data = [
    (50, 25), (60, 20), (75, 50), (90, 30), (120, 40),
    (45, 15), (80, 10), (36, 12), (150, 75), (200, 80),
    (30, 25), (48, 60), (100, 50), (72, 36), (84, 42),
    (25, 5), (40, 8), (180, 90), (64, 16), (96, 24),
    (55, 10), (35, 7), (160, 80), (42, 14), (63, 21),
]

contexts_e4 = [
    ("{part} students passed the exam, which is {pct}% of the total. "
     "How many students took the exam?"),
    ("A store sold {part} items today, which is {pct}% of its inventory. "
     "How many items are in the inventory?"),
    ("{part} employees attended the seminar, representing {pct}% of the staff. "
     "How many employees are on staff?"),
    ("A candidate received {part} votes, which is {pct}% of all votes cast. "
     "How many total votes were cast?"),
    ("{part} residents signed the petition, which is {pct}% of the barangay population. "
     "What is the barangay population?"),
]

random.shuffle(e4_data)
for i, (part, pct) in enumerate(e4_data):
    whole = part / (pct / 100)
    ctx = contexts_e4[i % len(contexts_e4)]
    q_text = ctx.format(part=part, pct=pct)
    choices, answer = make_number_choices(whole)
    explanation = (f"{part} is {pct}% of the total. "
                   f"Total = {part} \u00f7 {pct/100} = {fmt_num(whole)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the whole", "basic application"])


# --- E5: Simple discount problems ---
e5_data = [
    (800, 25), (1200, 20), (500, 10), (2000, 15), (1500, 30),
    (3000, 50), (600, 5), (4000, 20), (900, 10), (1800, 25),
    (2500, 40), (700, 15), (1000, 20), (3500, 10), (4500, 30),
    (950, 50), (1600, 25), (2200, 20), (5000, 15), (750, 10),
    (1100, 5), (6000, 30), (8000, 25), (1400, 20), (2800, 15),
]

contexts_e5 = [
    ("A shirt originally costs \u20b1{price:,}. It is on a {pct}% discount. "
     "What is the sale price?"),
    ("A pair of shoes priced at \u20b1{price:,} has a {pct}% discount. "
     "How much will you pay?"),
    ("A bag costs \u20b1{price:,}. During a clearance sale, it is marked down {pct}%. "
     "What is the discounted price?"),
    ("An appliance originally priced at \u20b1{price:,} is on sale at {pct}% off. "
     "What is the sale price?"),
    ("A gadget costs \u20b1{price:,}. A {pct}% discount is applied. "
     "How much do you pay?"),
]

random.shuffle(e5_data)
for i, (price, pct) in enumerate(e5_data):
    discount_amt = price * pct / 100
    sale_price = price - discount_amt
    ctx = contexts_e5[i % len(contexts_e5)]
    q_text = ctx.format(price=price, pct=pct)
    choices, answer = make_peso_choices(sale_price)
    explanation = (f"{pct}% of \u20b1{price:,} = {fmt_peso(discount_amt)}. "
                   f"Sale price = \u20b1{price:,} \u2212 {fmt_peso(discount_amt)} = {fmt_peso(sale_price)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "discount", "real-life applications"])


# --- E6: Simple tax/VAT addition ---
e6_data = [
    (1000, 12), (2500, 12), (5000, 12), (1500, 12), (3000, 12),
    (800, 12), (4500, 12), (6000, 12), (7500, 12), (10000, 12),
    (2000, 12), (3500, 12), (4000, 12), (8000, 12), (9000, 12),
    (1200, 12), (1800, 12), (2200, 12), (2800, 12), (3200, 12),
    (500, 12), (750, 12), (1100, 12), (1350, 12), (1650, 12),
]

contexts_e6 = [
    ("A meal costs \u20b1{price:,} before VAT. If VAT is {pct}%, "
     "what is the total bill?"),
    ("A service fee is \u20b1{price:,} before tax. With {pct}% VAT added, "
     "how much is the total?"),
    ("An item is priced at \u20b1{price:,} exclusive of {pct}% VAT. "
     "What is the VAT-inclusive price?"),
    ("A repair job costs \u20b1{price:,} plus {pct}% VAT. "
     "What is the total amount to pay?"),
    ("A purchase totals \u20b1{price:,} before {pct}% tax. "
     "What is the final amount including tax?"),
]

random.shuffle(e6_data)
for i, (price, pct) in enumerate(e6_data):
    tax_amt = price * pct / 100
    total = price + tax_amt
    ctx = contexts_e6[i % len(contexts_e6)]
    q_text = ctx.format(price=price, pct=pct)
    choices, answer = make_peso_choices(total)
    explanation = (f"{pct}% of \u20b1{price:,} = {fmt_peso(tax_amt)}. "
                   f"Total = \u20b1{price:,} + {fmt_peso(tax_amt)} = {fmt_peso(total)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "tax", "VAT", "real-life applications"])


# --- E7: Complement problems (how many are NOT X?) ---
e7_data = [
    (500, 60), (400, 75), (300, 40), (800, 85), (200, 30),
    (1000, 70), (250, 80), (600, 55), (350, 20), (450, 65),
    (150, 40), (700, 90), (900, 45), (120, 25), (550, 50),
    (1200, 35), (160, 75), (240, 60), (320, 80), (480, 15),
    (640, 70), (180, 50), (280, 45), (360, 85), (420, 30),
]

contexts_e7 = [
    ("Out of {whole} examinees, {pct}% passed. How many failed?"),
    ("A school has {whole} students. If {pct}% are female, how many are male?"),
    ("A factory produced {whole} units. If {pct}% met quality standards, "
     "how many did NOT meet standards?"),
    ("Out of {whole} employees, {pct}% attended the training. "
     "How many did NOT attend?"),
    ("A survey of {whole} people found {pct}% in favor. "
     "How many were NOT in favor?"),
]

random.shuffle(e7_data)
for i, (whole, pct) in enumerate(e7_data):
    complement_pct = 100 - pct
    result = whole * complement_pct / 100
    ctx = contexts_e7[i % len(contexts_e7)]
    q_text = ctx.format(whole=whole, pct=pct)
    choices, answer = make_number_choices(result)
    explanation = (f"Those NOT in the {pct}% group = 100% \u2212 {pct}% = {complement_pct}%. "
                   f"{complement_pct}% of {whole} = {complement_pct/100} \u00d7 {whole} = {fmt_num(result)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "complement", "real-life applications"])


# --- E8: Simple salary/raise problems ---
e8_data = [
    (20000, 10), (25000, 5), (18000, 15), (30000, 8), (15000, 20),
    (22000, 12), (28000, 10), (35000, 5), (16000, 25), (40000, 10),
    (12000, 15), (24000, 20), (32000, 5), (19000, 10), (27000, 8),
    (21000, 15), (26000, 10), (33000, 5), (17000, 20), (38000, 10),
    (14000, 25), (23000, 12), (29000, 8), (36000, 5), (31000, 10),
]

contexts_e8 = [
    ("An employee earns \u20b1{salary:,} per month. After a {pct}% raise, "
     "what is the new monthly salary?"),
    ("A worker's salary is \u20b1{salary:,}. If given a {pct}% increase, "
     "how much will the new salary be?"),
    ("A government clerk earns \u20b1{salary:,}. A {pct}% salary adjustment is approved. "
     "What is the adjusted salary?"),
]

random.shuffle(e8_data)
for i, (salary, pct) in enumerate(e8_data):
    raise_amt = salary * pct / 100
    new_salary = salary + raise_amt
    ctx = contexts_e8[i % len(contexts_e8)]
    q_text = ctx.format(salary=salary, pct=pct)
    choices, answer = make_peso_choices(new_salary)
    explanation = (f"{pct}% of \u20b1{salary:,} = {fmt_peso(raise_amt)}. "
                   f"New salary = \u20b1{salary:,} + {fmt_peso(raise_amt)} = {fmt_peso(new_salary)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "salary increase", "real-life applications"])


# --- E9: Simple commission problems ---
e9_data = [
    (100000, 5), (200000, 3), (50000, 10), (150000, 4), (300000, 2),
    (80000, 8), (250000, 6), (120000, 5), (400000, 3), (60000, 10),
    (500000, 2), (180000, 5), (350000, 4), (90000, 8), (220000, 3),
    (75000, 6), (450000, 5), (130000, 10), (280000, 4), (160000, 5),
    (600000, 3), (700000, 2), (95000, 8), (110000, 5), (240000, 4),
]

contexts_e9 = [
    ("A sales agent earns a {pct}% commission. If she sold \u20b1{sales:,} worth of products, "
     "how much is her commission?"),
    ("A real estate broker receives {pct}% commission on sales. "
     "How much does he earn from a \u20b1{sales:,} property sale?"),
    ("An insurance agent gets {pct}% of total premiums collected. "
     "If she collected \u20b1{sales:,}, what is her commission?"),
]

random.shuffle(e9_data)
for i, (sales, pct) in enumerate(e9_data):
    commission = sales * pct / 100
    ctx = contexts_e9[i % len(contexts_e9)]
    q_text = ctx.format(sales=sales, pct=pct)
    choices, answer = make_peso_choices(commission)
    explanation = f"{pct}% of \u20b1{sales:,} = {pct/100} \u00d7 {sales:,} = {fmt_peso(commission)}."
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "commission", "real-life applications"])

# --- E10: Simple population/growth ---
e10_data = [
    (10000, 5), (20000, 10), (50000, 4), (8000, 15), (30000, 6),
    (15000, 8), (25000, 10), (40000, 5), (12000, 20), (60000, 3),
    (5000, 12), (35000, 10), (45000, 4), (18000, 5), (7000, 10),
    (9000, 15), (22000, 8), (28000, 5), (55000, 6), (70000, 2),
    (6000, 10), (11000, 5), (16000, 8), (32000, 10), (48000, 5),
]

random.shuffle(e10_data)
for i, (pop, pct) in enumerate(e10_data[:30]):
    growth = pop * pct / 100
    new_pop = pop + growth
    q_text = (f"A barangay has a population of {pop:,}. "
              f"If the population grew by {pct}% this year, what is the new population?")
    choices, answer = make_number_choices(new_pop)
    explanation = (f"{pct}% of {pop:,} = {fmt_num(growth)}. "
                   f"New population = {pop:,} + {fmt_num(growth)} = {fmt_num(new_pop)}.")
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "population growth", "real-life applications"])


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- M1: Reverse percentage (finding original after discount) ---
m1_data = [
    (1200, 20), (1500, 25), (2400, 20), (3600, 10), (4500, 25),
    (800, 20), (1800, 10), (2700, 25), (3200, 20), (5400, 10),
    (960, 20), (1350, 25), (2100, 30), (4000, 20), (6000, 25),
    (1440, 20), (2250, 25), (3150, 30), (4800, 20), (7200, 10),
    (1680, 20), (2625, 25), (3500, 30), (5600, 20), (8100, 10),
]

contexts_m1 = [
    ("After a {pct}% discount, a laptop costs \u20b1{final:,}. "
     "What was the original price?"),
    ("A phone is on sale at {pct}% off and now costs \u20b1{final:,}. "
     "What was the original price?"),
    ("After receiving a {pct}% markdown, an appliance sells for \u20b1{final:,}. "
     "What was the price before the markdown?"),
    ("A jacket costs \u20b1{final:,} after a {pct}% reduction. "
     "What was the original price?"),
    ("An item's sale price is \u20b1{final:,} after a {pct}% discount. "
     "Find the original price."),
]

random.shuffle(m1_data)
for i, (final_price, pct) in enumerate(m1_data):
    original = final_price / ((100 - pct) / 100)
    ctx = contexts_m1[i % len(contexts_m1)]
    q_text = ctx.format(final=final_price, pct=pct)
    choices, answer = make_peso_choices(original)
    remaining_pct = 100 - pct
    explanation = (f"After {pct}% off, the price is {remaining_pct}% of the original. "
                   f"Original = \u20b1{final_price:,} \u00f7 {remaining_pct/100} = {fmt_peso(original)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "reverse percentage", "discount"])


# --- M2: Reverse percentage (finding original after increase) ---
m2_data = [
    (23000, 15), (27500, 10), (34500, 15), (28800, 20), (31500, 5),
    (24200, 10), (33350, 15), (36000, 20), (26250, 5), (38500, 10),
    (21600, 8), (29900, 15), (32200, 10), (25300, 10), (37800, 5),
    (22000, 10), (30000, 20), (35000, 25), (27000, 8), (40000, 25),
    (19800, 10), (26400, 20), (31200, 4), (44000, 10), (48000, 20),
]

contexts_m2 = [
    ("After a {pct}% salary increase, an employee now earns \u20b1{new:,}. "
     "What was the original salary?"),
    ("A product's price after a {pct}% markup is \u20b1{new:,}. "
     "What was the cost price?"),
    ("After a {pct}% raise, a worker's monthly pay is \u20b1{new:,}. "
     "What was the pay before the raise?"),
    ("A stock's value after a {pct}% gain is \u20b1{new:,}. "
     "What was the original value?"),
    ("After a {pct}% increase, a budget is now \u20b1{new:,}. "
     "What was the original budget?"),
]

random.shuffle(m2_data)
for i, (new_val, pct) in enumerate(m2_data):
    original = new_val / ((100 + pct) / 100)
    ctx = contexts_m2[i % len(contexts_m2)]
    q_text = ctx.format(new=new_val, pct=pct)
    choices, answer = make_peso_choices(original)
    total_pct = 100 + pct
    explanation = (f"After {pct}% increase, the value is {total_pct}% of the original. "
                   f"Original = \u20b1{new_val:,} \u00f7 {total_pct/100} = {fmt_peso(original)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "reverse percentage", "salary increase"])


# --- M3: Discount then tax (two-step) ---
m3_data = [
    (5000, 20, 12), (8000, 15, 12), (10000, 25, 12), (3000, 10, 12),
    (6000, 30, 12), (12000, 20, 12), (4500, 15, 12), (7500, 25, 12),
    (9000, 10, 12), (15000, 20, 12), (2500, 30, 12), (11000, 15, 12),
    (4000, 20, 12), (6500, 25, 12), (8500, 10, 12), (3500, 15, 12),
    (5500, 20, 12), (7000, 30, 12), (9500, 25, 12), (13000, 10, 12),
    (2000, 20, 12), (14000, 15, 12), (16000, 25, 12), (18000, 10, 12),
    (20000, 20, 12),
]

random.shuffle(m3_data)
for i, (price, disc_pct, tax_pct) in enumerate(m3_data):
    discounted = price * (1 - disc_pct / 100)
    final = discounted * (1 + tax_pct / 100)
    final = round(final, 2)
    q_text = (f"An item costs \u20b1{price:,}. It has a {disc_pct}% discount, "
              f"and then {tax_pct}% VAT is applied to the discounted price. "
              f"What is the final price?")
    choices, answer = make_peso_choices(final)
    explanation = (f"Discounted price = \u20b1{price:,} \u00d7 {1 - disc_pct/100} = {fmt_peso(discounted)}. "
                   f"With {tax_pct}% VAT: {fmt_peso(discounted)} \u00d7 {1 + tax_pct/100} = {fmt_peso(final)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "multi-step", "discount", "tax"])


# --- M4: Profit percentage problems ---
m4_data = [
    (400, 520), (600, 780), (1000, 1300), (1500, 1950), (2000, 2600),
    (800, 1000), (1200, 1500), (2500, 3250), (3000, 3900), (500, 650),
    (750, 900), (1800, 2340), (900, 1080), (1100, 1430), (1400, 1820),
    (350, 490), (450, 585), (550, 715), (650, 845), (850, 1105),
    (950, 1235), (1050, 1365), (1250, 1625), (1350, 1755), (1600, 2080),
]

contexts_m4 = [
    ("A vendor buys goods for \u20b1{cost:,} and sells them for \u20b1{sell:,}. "
     "What is the profit percentage?"),
    ("A store purchased an item at \u20b1{cost:,} and sold it for \u20b1{sell:,}. "
     "What is the percentage profit based on cost?"),
    ("A trader bought products for \u20b1{cost:,} and sold them at \u20b1{sell:,}. "
     "Find the profit percentage."),
]

random.shuffle(m4_data)
for i, (cost, sell) in enumerate(m4_data):
    profit = sell - cost
    profit_pct = profit / cost * 100
    ctx = contexts_m4[i % len(contexts_m4)]
    q_text = ctx.format(cost=cost, sell=sell)
    choices, answer = make_pct_choices(profit_pct)
    explanation = (f"Profit = \u20b1{sell:,} \u2212 \u20b1{cost:,} = {fmt_peso(profit)}. "
                   f"Profit % = {fmt_peso(profit)} \u00f7 \u20b1{cost:,} \u00d7 100 = {fmt_num(profit_pct)}%.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "profit", "business"])


# --- M5: Salary with multiple deductions ---
m5_data = [
    (25000, 4, 3, 5), (30000, 4, 4, 5), (35000, 3, 4, 6),
    (28000, 4, 3, 5), (32000, 5, 4, 3), (40000, 4, 4, 5),
    (22000, 3, 3, 4), (38000, 4, 5, 6), (45000, 4, 4, 5),
    (20000, 3, 3, 5), (27000, 4, 4, 5), (33000, 5, 3, 4),
    (36000, 4, 4, 6), (42000, 3, 4, 5), (48000, 4, 5, 5),
    (18000, 3, 3, 4), (24000, 4, 3, 5), (29000, 4, 4, 5),
    (31000, 5, 4, 3), (37000, 4, 4, 6), (26000, 3, 3, 5),
    (34000, 4, 4, 5), (39000, 5, 4, 4), (43000, 4, 3, 5),
    (50000, 4, 4, 5),
]

random.shuffle(m5_data)
for i, (salary, ded1, ded2, ded3) in enumerate(m5_data):
    total_ded_pct = ded1 + ded2 + ded3
    total_ded = salary * total_ded_pct / 100
    net = salary - total_ded
    q_text = (f"An employee earns \u20b1{salary:,} monthly. Deductions are: "
              f"{ded1}% for Pag-IBIG, {ded2}% for PhilHealth, and {ded3}% for GSIS. "
              f"What is the net take-home pay?")
    choices, answer = make_peso_choices(net)
    explanation = (f"Total deductions = {ded1}% + {ded2}% + {ded3}% = {total_ded_pct}%. "
                   f"Deduction amount = {total_ded_pct}% of \u20b1{salary:,} = {fmt_peso(total_ded)}. "
                   f"Net pay = \u20b1{salary:,} \u2212 {fmt_peso(total_ded)} = {fmt_peso(net)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "salary deductions", "multi-step"])


# --- M6: Multi-step population/survey problems ---
m6_data = [
    (10000, 60, 80), (8000, 75, 60), (12000, 50, 90),
    (15000, 80, 70), (20000, 65, 85), (6000, 70, 50),
    (9000, 55, 80), (25000, 40, 75), (5000, 90, 60),
    (30000, 45, 80), (7000, 85, 40), (11000, 60, 70),
    (14000, 50, 80), (16000, 75, 60), (18000, 65, 50),
    (4000, 80, 75), (13000, 70, 60), (22000, 55, 80),
    (3000, 90, 70), (17000, 60, 85), (19000, 45, 60),
    (21000, 50, 70), (24000, 35, 80), (26000, 40, 75),
    (28000, 55, 60),
]

contexts_m6 = [
    ("A barangay has {pop:,} residents. {pct1}% are registered voters, "
     "and {pct2}% of registered voters actually voted. How many voted?"),
    ("A company has {pop:,} employees. {pct1}% are eligible for a bonus, "
     "and {pct2}% of those eligible received it. How many received the bonus?"),
    ("A school has {pop:,} students. {pct1}% joined the sports fest, "
     "and {pct2}% of participants won medals. How many won medals?"),
]

random.shuffle(m6_data)
for i, (pop, pct1, pct2) in enumerate(m6_data):
    intermediate = pop * pct1 / 100
    result = intermediate * pct2 / 100
    ctx = contexts_m6[i % len(contexts_m6)]
    q_text = ctx.format(pop=pop, pct1=pct1, pct2=pct2)
    choices, answer = make_number_choices(result)
    explanation = (f"First: {pct1}% of {pop:,} = {fmt_num(intermediate)}. "
                   f"Then: {pct2}% of {fmt_num(intermediate)} = {fmt_num(result)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "multi-step", "population"])


# --- M7: Budget allocation (finding remainder) ---
m7_data = [
    (1000000, 40, 30), (500000, 35, 25), (2000000, 45, 30),
    (800000, 50, 20), (1500000, 35, 40), (3000000, 30, 25),
    (600000, 45, 25), (1200000, 40, 35), (900000, 50, 30),
    (2500000, 35, 30), (400000, 40, 20), (1800000, 30, 35),
    (700000, 45, 30), (1100000, 50, 25), (1600000, 35, 25),
    (350000, 40, 30), (750000, 30, 40), (1300000, 45, 25),
    (950000, 50, 20), (2200000, 35, 30), (450000, 40, 25),
    (1400000, 30, 35), (850000, 45, 30), (1700000, 50, 25),
    (1900000, 35, 40),
]

random.shuffle(m7_data)
for i, (budget, pct1, pct2) in enumerate(m7_data):
    remainder_pct = 100 - pct1 - pct2
    remainder = budget * remainder_pct / 100
    q_text = (f"A department has a budget of \u20b1{budget:,}. "
              f"It allocates {pct1}% to personnel and {pct2}% to operations. "
              f"How much is left for other expenses?")
    choices, answer = make_peso_choices(remainder)
    explanation = (f"Remaining = 100% \u2212 {pct1}% \u2212 {pct2}% = {remainder_pct}%. "
                   f"{remainder_pct}% of \u20b1{budget:,} = {fmt_peso(remainder)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "budget allocation", "government"])


# --- M8: Markup/selling price problems ---
m8_data = [
    (500, 40), (800, 25), (1200, 30), (1500, 50), (2000, 35),
    (600, 60), (900, 20), (1100, 45), (1400, 25), (1800, 30),
    (700, 40), (1000, 50), (1300, 35), (1600, 20), (2200, 25),
    (400, 75), (550, 60), (750, 40), (950, 30), (1050, 50),
    (1250, 20), (1350, 45), (1450, 35), (1700, 25), (1900, 30),
]

random.shuffle(m8_data)
for i, (cost, markup_pct) in enumerate(m8_data):
    markup = cost * markup_pct / 100
    selling = cost + markup
    q_text = (f"A store buys an item for \u20b1{cost:,} and marks it up by {markup_pct}%. "
              f"What is the selling price?")
    choices, answer = make_peso_choices(selling)
    explanation = (f"Markup = {markup_pct}% of \u20b1{cost:,} = {fmt_peso(markup)}. "
                   f"Selling price = \u20b1{cost:,} + {fmt_peso(markup)} = {fmt_peso(selling)}.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "markup", "business"])


# --- M9: Percentage increase/decrease word problems ---
m9_data = [
    (18000, 20700, True), (5000, 5400, True), (450000, 531000, True),
    (800, 640, False), (500000, 425000, False), (24000, 21600, False),
    (12000, 15000, True), (9000, 12000, True), (3000, 2400, False),
    (40000, 46000, True), (25000, 20000, False), (16000, 20000, True),
    (7500, 9000, True), (6000, 4800, False), (10000, 8500, False),
    (35000, 42000, True), (28000, 21000, False), (15000, 18000, True),
    (20000, 17000, False), (45000, 54000, True), (32000, 24000, False),
    (8000, 10000, True), (11000, 8800, False), (50000, 60000, True),
    (22000, 17600, False),
]

random.shuffle(m9_data)
for i, (original, new_val, is_increase) in enumerate(m9_data):
    change = abs(new_val - original)
    pct_change = change / original * 100
    direction = "increase" if is_increase else "decrease"
    if is_increase:
        q_text = (f"A value changed from {original:,} to {new_val:,}. "
                  f"What is the percentage increase?")
    else:
        q_text = (f"A quantity dropped from {original:,} to {new_val:,}. "
                  f"What is the percentage decrease?")
    choices, answer = make_pct_choices(pct_change)
    explanation = (f"Change = {new_val:,} \u2212 {original:,} = {change:,} "
                   f"({'increase' if is_increase else 'decrease'}). "
                   f"Percentage = {change:,} \u00f7 {original:,} \u00d7 100 = {fmt_num(pct_change)}%.")
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", f"percentage {direction}", "computation"])


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- H1: Successive discounts ---
h1_data = [
    (2000, 20, 10), (3000, 25, 15), (5000, 30, 10), (4000, 20, 15),
    (6000, 15, 20), (8000, 25, 10), (1500, 30, 20), (2500, 20, 25),
    (3500, 15, 10), (4500, 25, 20), (7000, 10, 15), (9000, 20, 10),
    (10000, 30, 15), (1200, 25, 20), (1800, 20, 15), (2200, 15, 25),
    (2800, 30, 10), (3200, 20, 20), (3800, 25, 15), (4200, 10, 20),
    (5500, 20, 10), (6500, 15, 15), (7500, 25, 10), (8500, 20, 15),
    (9500, 30, 20),
]

random.shuffle(h1_data)
for i, (price, disc1, disc2) in enumerate(h1_data):
    after_first = price * (1 - disc1 / 100)
    final = after_first * (1 - disc2 / 100)
    final = round(final, 2)
    q_text = (f"A product priced at \u20b1{price:,} receives a {disc1}% discount, "
              f"then an additional {disc2}% discount on the reduced price. "
              f"What is the final price?")
    choices, answer = make_peso_choices(final)
    explanation = (f"After {disc1}% off: \u20b1{price:,} \u00d7 {1 - disc1/100} = {fmt_peso(after_first)}. "
                   f"After {disc2}% off: {fmt_peso(after_first)} \u00d7 {1 - disc2/100} = {fmt_peso(final)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "successive discounts", "multi-step"])


# --- H2: Successive changes (increase then decrease or vice versa) ---
h2_data = [
    (20000, 10, 10), (30000, 20, 20), (25000, 15, 10), (40000, 10, 15),
    (50000, 25, 20), (35000, 20, 10), (45000, 10, 25), (15000, 30, 20),
    (60000, 15, 15), (18000, 20, 25), (22000, 25, 10), (28000, 10, 20),
    (32000, 15, 25), (38000, 20, 15), (42000, 25, 20), (48000, 10, 10),
    (55000, 15, 20), (12000, 20, 10), (16000, 30, 15), (24000, 25, 25),
    (26000, 10, 30), (34000, 20, 20), (36000, 15, 10), (44000, 25, 15),
    (52000, 10, 20),
]

random.shuffle(h2_data)
for i, (original, inc_pct, dec_pct) in enumerate(h2_data):
    after_inc = original * (1 + inc_pct / 100)
    final = after_inc * (1 - dec_pct / 100)
    final = round(final, 2)
    q_text = (f"A salary of \u20b1{original:,} is increased by {inc_pct}%, "
              f"then the new salary is decreased by {dec_pct}%. "
              f"What is the final salary?")
    choices, answer = make_peso_choices(final)
    explanation = (f"After {inc_pct}% increase: \u20b1{original:,} \u00d7 {1 + inc_pct/100} = {fmt_peso(after_inc)}. "
                   f"After {dec_pct}% decrease: {fmt_peso(after_inc)} \u00d7 {1 - dec_pct/100} = {fmt_peso(final)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "successive changes", "multi-step"])


# --- H3: Markup then discount (find effective change) ---
h3_data = [
    (1000, 60, 25), (2000, 40, 20), (1500, 50, 30), (800, 75, 40),
    (3000, 30, 15), (2500, 40, 25), (1200, 50, 20), (1800, 60, 30),
    (4000, 25, 10), (5000, 30, 20), (600, 100, 50), (900, 80, 40),
    (1100, 60, 25), (1400, 50, 30), (1600, 40, 20), (700, 100, 40),
    (2200, 50, 25), (2800, 30, 15), (3200, 40, 20), (3500, 60, 30),
    (4500, 25, 15), (1300, 50, 25), (1700, 40, 30), (2100, 60, 20),
    (2600, 50, 25),
]

random.shuffle(h3_data)
for i, (cost, markup_pct, disc_pct) in enumerate(h3_data):
    marked_price = cost * (1 + markup_pct / 100)
    selling = marked_price * (1 - disc_pct / 100)
    selling = round(selling, 2)
    q_text = (f"A store marks up an item costing \u20b1{cost:,} by {markup_pct}%, "
              f"then offers a {disc_pct}% discount on the marked price. "
              f"What is the final selling price?")
    choices, answer = make_peso_choices(selling)
    explanation = (f"Marked price = \u20b1{cost:,} \u00d7 {1 + markup_pct/100} = {fmt_peso(marked_price)}. "
                   f"After {disc_pct}% discount: {fmt_peso(marked_price)} \u00d7 {1 - disc_pct/100} = {fmt_peso(selling)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "markup", "discount", "multi-step"])


# --- H4: Commission + base pay problems ---
h4_data = [
    (8000, 5, 200000), (10000, 3, 500000), (12000, 4, 300000),
    (15000, 6, 250000), (9000, 8, 150000), (7000, 5, 400000),
    (11000, 3, 600000), (13000, 4, 350000), (6000, 10, 100000),
    (14000, 5, 280000), (8500, 6, 220000), (9500, 4, 450000),
    (10500, 3, 550000), (11500, 5, 320000), (12500, 8, 180000),
    (7500, 6, 350000), (16000, 4, 400000), (5000, 10, 200000),
    (18000, 3, 700000), (20000, 5, 500000), (6500, 8, 250000),
    (8200, 5, 360000), (9800, 4, 420000), (11200, 6, 280000),
    (13500, 3, 650000),
]

random.shuffle(h4_data)
for i, (base_pay, comm_pct, sales) in enumerate(h4_data):
    commission = sales * comm_pct / 100
    total_income = base_pay + commission
    q_text = (f"A sales agent has a base pay of \u20b1{base_pay:,} plus {comm_pct}% commission on sales. "
              f"If she sold \u20b1{sales:,} worth of products this month, "
              f"what is her total income?")
    choices, answer = make_peso_choices(total_income)
    explanation = (f"Commission = {comm_pct}% of \u20b1{sales:,} = {fmt_peso(commission)}. "
                   f"Total income = \u20b1{base_pay:,} + {fmt_peso(commission)} = {fmt_peso(total_income)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "commission", "base pay", "multi-step"])


# --- H5: Compound growth (2 years) ---
h5_data = [
    (100000, 10, 10), (80000, 5, 8), (50000, 12, 10), (200000, 8, 6),
    (150000, 10, 5), (120000, 15, 10), (60000, 20, 15), (90000, 8, 12),
    (75000, 10, 10), (180000, 5, 5), (250000, 4, 6), (300000, 10, 8),
    (40000, 15, 20), (110000, 12, 8), (130000, 6, 10), (160000, 10, 12),
    (70000, 8, 8), (95000, 10, 15), (140000, 5, 10), (220000, 8, 4),
    (170000, 10, 10), (85000, 12, 8), (190000, 6, 6), (210000, 5, 8),
    (240000, 10, 5),
]

random.shuffle(h5_data)
for i, (principal, rate1, rate2) in enumerate(h5_data):
    after_y1 = principal * (1 + rate1 / 100)
    after_y2 = after_y1 * (1 + rate2 / 100)
    after_y2 = round(after_y2, 2)
    q_text = (f"A municipality's budget was \u20b1{principal:,}. "
              f"It grew by {rate1}% in the first year and {rate2}% in the second year. "
              f"What is the budget after two years?")
    choices, answer = make_peso_choices(after_y2)
    explanation = (f"After Year 1: \u20b1{principal:,} \u00d7 {1 + rate1/100} = {fmt_peso(after_y1)}. "
                   f"After Year 2: {fmt_peso(after_y1)} \u00d7 {1 + rate2/100} = {fmt_peso(after_y2)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "compound growth", "multi-step"])


# --- H6: Reverse successive change (find original given final) ---
h6_data = [
    (36000, 20, 10), (45360, 15, 12), (28800, 20, 20),
    (40500, 25, 10), (33600, 20, 15), (51200, 10, 20),
    (38400, 20, 25), (29700, 10, 10), (43200, 20, 10),
    (54000, 25, 20), (31500, 5, 10), (47250, 15, 25),
    (25200, 20, 10), (37800, 10, 15), (56700, 25, 10),
    (27000, 20, 25), (32400, 8, 10), (41400, 15, 20),
    (48600, 10, 10), (52500, 25, 15), (22500, 25, 10),
    (34200, 20, 5), (39600, 10, 20), (44100, 15, 10),
    (50400, 20, 10),
]

random.shuffle(h6_data)
for i, (final, inc_pct, dec_pct) in enumerate(h6_data):
    # final = original * (1 + inc/100) * (1 - dec/100)
    multiplier = (1 + inc_pct / 100) * (1 - dec_pct / 100)
    original = final / multiplier
    original = round(original, 2)
    q_text = (f"After a {inc_pct}% increase followed by a {dec_pct}% decrease, "
              f"a value became {fmt_peso(final)}. What was the original value?")
    choices, answer = make_peso_choices(original)
    explanation = (f"Net multiplier = {1 + inc_pct/100} \u00d7 {1 - dec_pct/100} = {round(multiplier, 4)}. "
                   f"Original = {fmt_peso(final)} \u00f7 {round(multiplier, 4)} = {fmt_peso(original)}.")
    add_q("Hard", q_text, choices, answer, explanation,
          ["percentage word problems", "reverse successive change", "multi-step"])


# --- H7: Complex word problems (CSE-style scenarios) ---
hard_scenarios = [
    # Scenario: Election with multiple candidates
    ("In a barangay election with 12,000 voters, Candidate A got 45%, "
     "Candidate B got 30%, and the rest went to Candidate C. "
     "How many more votes did A get than C?",
     ["2,400", "1,800", "3,000", "5,400"], "2,400",
     "A = 45% of 12,000 = 5,400. C = 25% of 12,000 = 3,000. "
     "Difference = 5,400 \u2212 3,000 = 2,400."),
    # Scenario: Depreciation
    ("A car worth \u20b1800,000 depreciates 15% per year. "
     "What is its value after 2 years?",
     ["\u20b1578,000", "\u20b1560,000", "\u20b1680,000", "\u20b1544,000"],
     "\u20b1578,000",
     "After Year 1: 800,000 \u00d7 0.85 = 680,000. "
     "After Year 2: 680,000 \u00d7 0.85 = 578,000."),
    # Scenario: Effective discount
    ("A store offers 20% off, then members get an extra 15% off the sale price. "
     "What is the effective total discount?",
     ["32%", "35%", "30%", "28%"], "32%",
     "Net multiplier = 0.80 \u00d7 0.85 = 0.68. "
     "Effective discount = 100% \u2212 68% = 32%."),
    # Scenario: Break-even
    ("A vendor bought 100 items at \u20b150 each. He sold 80 items at \u20b175 each "
     "and the rest at \u20b140 each. What is his profit percentage?",
     ["28%", "20%", "30%", "25%"], "28%",
     "Cost = 100 \u00d7 50 = 5,000. Revenue = (80 \u00d7 75) + (20 \u00d7 40) = 6,000 + 800 = 6,800. "
     "Profit = 6,800 \u2212 5,000 = 1,800. Profit % = 1,800/5,000 \u00d7 100 = 36%. "
     "Wait, let me recalculate: Profit % = 1,800 \u00f7 5,000 \u00d7 100 = 36%."),
    # Scenario: Salary comparison
    ("Juan earns 20% more than Maria. If Maria earns \u20b125,000, "
     "how much more does Juan earn than Maria?",
     ["\u20b15,000", "\u20b130,000", "\u20b14,000", "\u20b16,000"], "\u20b15,000",
     "Juan earns 20% more = 20% of 25,000 = 5,000 more."),
    # Scenario: Reverse VAT
    ("A receipt shows a VAT-inclusive total of \u20b13,360. "
     "If VAT is 12%, what is the pre-VAT amount?",
     ["\u20b13,000", "\u20b12,956.80", "\u20b13,200", "\u20b12,800"], "\u20b13,000",
     "VAT-inclusive = 112% of pre-VAT. Pre-VAT = 3,360 \u00f7 1.12 = \u20b13,000."),
    # Scenario: Mixed deductions
    ("An employee's gross pay is \u20b145,000. After 12% income tax and 4% SSS, "
     "what is the net pay?",
     ["\u20b137,800", "\u20b139,600", "\u20b136,000", "\u20b138,700"], "\u20b137,800",
     "Total deductions = 12% + 4% = 16%. Net = 84% of 45,000 = 0.84 \u00d7 45,000 = \u20b137,800."),
    # Scenario: Percentage of percentage
    ("In a school of 2,000 students, 60% are in high school. "
     "Of the high school students, 75% passed the national exam. "
     "What percentage of ALL students passed?",
     ["45%", "60%", "75%", "135%"], "45%",
     "High school = 60% of 2,000 = 1,200. Passed = 75% of 1,200 = 900. "
     "Percentage of all = 900/2,000 \u00d7 100 = 45%."),
]

# Fix the break-even problem (recalculate)
hard_scenarios[3] = (
    "A vendor bought 100 items at \u20b150 each. He sold 80 items at \u20b175 each "
    "and the rest at \u20b140 each. What is his profit percentage?",
    ["36%", "20%", "28%", "50%"], "36%",
    "Cost = 100 \u00d7 50 = \u20b15,000. Revenue = (80 \u00d7 75) + (20 \u00d7 40) = 6,000 + 800 = \u20b16,800. "
    "Profit = 6,800 \u2212 5,000 = \u20b11,800. Profit % = 1,800 \u00f7 5,000 \u00d7 100 = 36%.")

for q, ch, ans, exp in hard_scenarios:
    add_q("Hard", q, ch, ans, exp,
          ["percentage word problems", "CSE-style", "multi-step", "real-life applications"])


# --- H8: More complex CSE-style scenarios ---
hard_scenarios_2 = [
    ("A government project budget of \u20b12,000,000 is increased by 15% in Year 2, "
     "then decreased by 10% in Year 3. What is the Year 3 budget?",
     ["\u20b12,070,000", "\u20b12,100,000", "\u20b11,900,000", "\u20b12,050,000"],
     "\u20b12,070,000",
     "Year 2: 2,000,000 \u00d7 1.15 = 2,300,000. "
     "Year 3: 2,300,000 \u00d7 0.90 = \u20b12,070,000."),
    ("A worker's daily wage is \u20b1610. If the minimum wage increases by 6%, "
     "what is the new daily wage?",
     ["\u20b1646.60", "\u20b1670", "\u20b1636.60", "\u20b1700"],
     "\u20b1646.60",
     "6% of 610 = 36.60. New wage = 610 + 36.60 = \u20b1646.60."),
    ("A cooperative has 500 members. 70% are active, and 80% of active members "
     "paid their dues. How many active members have NOT paid?",
     ["70", "280", "350", "100"], "70",
     "Active = 70% of 500 = 350. Paid = 80% of 350 = 280. "
     "Not paid = 350 \u2212 280 = 70."),
    ("If the price of rice increased from \u20b142 to \u20b149 per kilo, "
     "what is the percentage increase? (Round to nearest whole number.)",
     ["17%", "14%", "7%", "20%"], "17%",
     "Increase = 49 \u2212 42 = 7. Percentage = 7 \u00f7 42 \u00d7 100 \u2248 16.67% \u2248 17%."),
    ("A student needs 75% to pass. The test has 60 items. "
     "If she already answered 30 correctly out of 40 items attempted, "
     "how many of the remaining 20 items must she get right to pass?",
     ["15", "10", "20", "12"], "15",
     "Need 75% of 60 = 45 correct. Already has 30. Needs 45 \u2212 30 = 15 more."),
    ("An office has 80 employees. 25% are on leave today. "
     "Of those present, 50% are in a meeting. "
     "How many employees are NOT in the meeting and NOT on leave?",
     ["30", "40", "20", "60"], "30",
     "On leave = 25% of 80 = 20. Present = 60. In meeting = 50% of 60 = 30. "
     "Not in meeting, not on leave = 60 \u2212 30 = 30."),
    ("A loan of \u20b1200,000 charges 1.5% monthly interest (simple). "
     "How much total interest is charged over 6 months?",
     ["\u20b118,000", "\u20b13,000", "\u20b112,000", "\u20b19,000"], "\u20b118,000",
     "Monthly interest = 1.5% of 200,000 = 3,000. "
     "Over 6 months = 3,000 \u00d7 6 = \u20b118,000."),
    ("A city's crime rate dropped from 120 incidents per month to 96. "
     "What is the percentage decrease?",
     ["20%", "24%", "25%", "16%"], "20%",
     "Decrease = 120 \u2212 96 = 24. Percentage = 24 \u00f7 120 \u00d7 100 = 20%."),
    ("Three departments share a \u20b1900,000 budget. Department A gets 40%, "
     "Department B gets 35%. How much more does A receive than B?",
     ["\u20b145,000", "\u20b150,000", "\u20b190,000", "\u20b135,000"], "\u20b145,000",
     "A = 40% of 900,000 = 360,000. B = 35% of 900,000 = 315,000. "
     "Difference = 360,000 \u2212 315,000 = \u20b145,000."),
    ("A product's price was increased by 25% then decreased by 20%. "
     "Is the final price equal to the original?",
     ["Yes, they are equal", "No, it is higher", "No, it is lower", "Cannot determine"],
     "Yes, they are equal",
     "Multiplier = 1.25 \u00d7 0.80 = 1.00. The final price equals the original."),
    ("An employee saves 15% of her \u20b132,000 salary. She spends 40% of her savings on a gadget. "
     "How much did the gadget cost?",
     ["\u20b11,920", "\u20b14,800", "\u20b12,880", "\u20b11,280"], "\u20b11,920",
     "Savings = 15% of 32,000 = 4,800. Gadget = 40% of 4,800 = \u20b11,920."),
    ("A farmer harvested 2,500 kg of rice. He sold 60% to a trader and 25% to a cooperative. "
     "How many kilograms did he keep?",
     ["375", "625", "500", "250"], "375",
     "Sold total = 60% + 25% = 85%. Kept = 15% of 2,500 = 375 kg."),
]

for q, ch, ans, exp in hard_scenarios_2:
    add_q("Hard", q, ch, ans, exp,
          ["percentage word problems", "CSE-style", "multi-step", "real-life applications"])


# --- H9: Percentage comparison problems ---
h9_data = [
    # (price_a, disc_a, price_b, disc_b) - which is cheaper?
    (2000, 30, 2200, 25), (1500, 20, 1800, 30), (3000, 40, 2500, 25),
    (4000, 25, 3500, 20), (1000, 15, 1200, 25), (5000, 30, 4500, 20),
    (2500, 20, 2800, 25), (1800, 25, 2000, 30), (3500, 35, 3000, 25),
    (6000, 40, 5000, 25), (2200, 15, 2500, 25), (4500, 30, 4000, 20),
    (1200, 10, 1500, 25), (2800, 20, 3200, 30), (3200, 25, 2800, 15),
    (1600, 30, 1400, 20), (7000, 35, 6000, 25), (900, 20, 1100, 30),
    (5500, 25, 5000, 20), (8000, 30, 7000, 20), (1100, 15, 1300, 25),
    (4200, 20, 3800, 10), (2600, 25, 3000, 30), (3800, 30, 3500, 20),
    (9000, 40, 8000, 30),
]

random.shuffle(h9_data)
for i, (pa, da, pb, db) in enumerate(h9_data[:25]):
    final_a = pa * (1 - da / 100)
    final_b = pb * (1 - db / 100)
    if final_a < final_b:
        answer_text = f"Store A (\u20b1{fmt_num(final_a)})"
        other = f"Store B (\u20b1{fmt_num(final_b)})"
    elif final_b < final_a:
        answer_text = f"Store B (\u20b1{fmt_num(final_b)})"
        other = f"Store A (\u20b1{fmt_num(final_a)})"
    else:
        answer_text = "They cost the same"
        other = f"Store A (\u20b1{fmt_num(final_a)})"

    choices = [answer_text, other, "They cost the same", "Cannot be determined"]
    # Remove duplicates
    choices = list(dict.fromkeys(choices))
    while len(choices) < 4:
        choices.append(f"Need more information")
    choices = choices[:4]
    random.shuffle(choices)

    q_text = (f"Store A sells an item at \u20b1{pa:,} with {da}% off. "
              f"Store B sells the same item at \u20b1{pb:,} with {db}% off. "
              f"Which store offers the lower final price?")
    explanation = (f"Store A: \u20b1{pa:,} \u00d7 {1 - da/100} = \u20b1{fmt_num(final_a)}. "
                   f"Store B: \u20b1{pb:,} \u00d7 {1 - db/100} = \u20b1{fmt_num(final_b)}. "
                   f"{'Store A' if final_a < final_b else 'Store B' if final_b < final_a else 'Both'} is cheaper.")
    add_q("Hard", q_text, choices, answer_text, explanation,
          ["percentage word problems", "comparison", "discount"])


# --- H10: Advanced CSE-style word problems ---
hard_scenarios_3 = [
    ("A company's revenue was \u20b15,000,000 last year. This year, revenue from products "
     "increased by 20% (products were 60% of last year's revenue) while revenue from "
     "services decreased by 10% (services were 40%). What is this year's total revenue?",
     ["\u20b15,400,000", "\u20b15,500,000", "\u20b15,200,000", "\u20b15,600,000"],
     "\u20b15,400,000",
     "Products last year = 60% of 5M = 3M. This year = 3M \u00d7 1.20 = 3.6M. "
     "Services last year = 40% of 5M = 2M. This year = 2M \u00d7 0.90 = 1.8M. "
     "Total = 3.6M + 1.8M = \u20b15,400,000."),
    ("A tank is 40% full with 200 liters. How many more liters are needed to fill it to 90%?",
     ["250", "450", "300", "200"], "250",
     "40% = 200 liters, so full capacity = 200 \u00f7 0.40 = 500 liters. "
     "90% = 0.90 \u00d7 500 = 450 liters. Need 450 \u2212 200 = 250 more liters."),
    ("In a class of 50, 60% are girls. If 5 more boys join, "
     "what percentage of the class are now girls?",
     ["54.55%", "60%", "50%", "56%"], "54.55%",
     "Girls = 60% of 50 = 30. New total = 50 + 5 = 55. "
     "Girls percentage = 30/55 \u00d7 100 \u2248 54.55%."),
    ("A salesperson must sell \u20b1500,000 to earn a 5% commission of \u20b125,000. "
     "She has sold \u20b1350,000 so far. How much more must she sell?",
     ["\u20b1150,000", "\u20b1125,000", "\u20b1175,000", "\u20b1200,000"], "\u20b1150,000",
     "Target = \u20b1500,000. Sold = \u20b1350,000. Remaining = 500,000 \u2212 350,000 = \u20b1150,000."),
    ("A family spends 30% of income on food, 25% on housing, 15% on transportation, "
     "and saves the rest. If they save \u20b19,000 per month, what is their monthly income?",
     ["\u20b130,000", "\u20b145,000", "\u20b136,000", "\u20b127,000"], "\u20b130,000",
     "Savings rate = 100% \u2212 30% \u2212 25% \u2212 15% = 30%. "
     "If 30% = \u20b19,000, then income = 9,000 \u00f7 0.30 = \u20b130,000."),
    ("A contractor completed 65% of a project in 26 days. "
     "At the same rate, how many total days will the project take?",
     ["40", "35", "45", "50"], "40",
     "65% takes 26 days. 1% takes 26/65 = 0.4 days. "
     "100% takes 0.4 \u00d7 100 = 40 days."),
    ("Two investments: \u20b1100,000 at 8% annual return and \u20b1150,000 at 5% annual return. "
     "What is the combined return as a percentage of total investment?",
     ["6.2%", "6.5%", "7%", "5.8%"], "6.2%",
     "Return 1 = 8% of 100,000 = 8,000. Return 2 = 5% of 150,000 = 7,500. "
     "Total return = 15,500. Total invested = 250,000. "
     "Combined rate = 15,500/250,000 \u00d7 100 = 6.2%."),
    ("A store's inventory decreased by 20% in January and increased by 25% in February. "
     "If the inventory at the end of February is 1,500 items, "
     "what was the inventory at the start of January?",
     ["1,500", "1,200", "1,800", "1,600"], "1,500",
     "Let original = x. After Jan: x \u00d7 0.80. After Feb: x \u00d7 0.80 \u00d7 1.25 = x \u00d7 1.00 = x. "
     "So original = 1,500."),
    ("A government employee's take-home pay is \u20b128,000 after 20% total deductions. "
     "What is the gross salary?",
     ["\u20b135,000", "\u20b133,600", "\u20b132,000", "\u20b136,000"], "\u20b135,000",
     "Take-home = 80% of gross. Gross = 28,000 \u00f7 0.80 = \u20b135,000."),
    ("A batch of 400 products has a 5% defect rate. After quality control removes defects, "
     "10% of the remaining good products are set aside as samples. "
     "How many products are available for sale?",
     ["342", "360", "380", "350"], "342",
     "Defective = 5% of 400 = 20. Good = 380. "
     "Samples = 10% of 380 = 38. Available = 380 \u2212 38 = 342."),
    ("If 40% of A equals 60% of B, and A + B = 500, what is A?",
     ["300", "200", "250", "350"], "300",
     "0.40A = 0.60B \u2192 A = 1.5B. Substitute: 1.5B + B = 500 \u2192 2.5B = 500 \u2192 B = 200. "
     "A = 1.5 \u00d7 200 = 300."),
    ("A phone originally costs \u20b120,000. Store A offers 15% off then 5% off the reduced price. "
     "Store B offers a flat 19% off. Which is cheaper and by how much?",
     ["Store B by \u20b150", "Store A by \u20b150", "They are equal", "Store B by \u20b1100"],
     "Store B by \u20b150",
     "Store A: 20,000 \u00d7 0.85 \u00d7 0.95 = 16,150. "
     "Store B: 20,000 \u00d7 0.81 = 16,200. Wait: "
     "A = 20,000 \u00d7 0.85 = 17,000 \u00d7 0.95 = 16,150. "
     "B = 20,000 \u00d7 0.81 = 16,200. Store A is cheaper by \u20b150."),
]

# Fix the last problem
hard_scenarios_3[-1] = (
    "A phone originally costs \u20b120,000. Store A offers 15% off then 5% off the reduced price. "
    "Store B offers a flat 19% off. Which is cheaper and by how much?",
    ["Store A by \u20b150", "Store B by \u20b150", "They are equal", "Store A by \u20b1100"],
    "Store A by \u20b150",
    "Store A: 20,000 \u00d7 0.85 = 17,000, then 17,000 \u00d7 0.95 = \u20b116,150. "
    "Store B: 20,000 \u00d7 0.81 = \u20b116,200. Store A is cheaper by \u20b150.")

for q, ch, ans, exp in hard_scenarios_3:
    add_q("Hard", q, ch, ans, exp,
          ["percentage word problems", "CSE-style", "advanced", "multi-step"])


# ============================================================
# FILLER: Ensure exactly 200 per difficulty
# ============================================================

# --- Easy fillers: more "find the part" with varied contexts ---
easy_filler_contexts = [
    "A library has {whole:,} books. If {pct}% are fiction, how many fiction books are there?",
    "A hospital has {whole:,} beds. If {pct}% are occupied, how many beds are occupied?",
    "A farm has {whole:,} hectares. If {pct}% is planted with rice, how many hectares have rice?",
    "A city has {whole:,} households. If {pct}% have internet access, how many have internet?",
    "A warehouse stores {whole:,} boxes. If {pct}% contain fragile items, how many are fragile?",
    "A fleet has {whole:,} vehicles. If {pct}% need maintenance, how many need maintenance?",
    "A building has {whole:,} units. If {pct}% are vacant, how many units are vacant?",
    "A plantation has {whole:,} trees. If {pct}% are mango trees, how many are mango trees?",
]

easy_filler_values = [
    (200, 35), (400, 45), (600, 55), (150, 60), (350, 20),
    (500, 70), (250, 40), (800, 15), (1000, 65), (450, 30),
    (300, 80), (550, 25), (650, 50), (750, 10), (850, 75),
    (180, 50), (220, 30), (280, 40), (320, 60), (380, 25),
    (420, 35), (480, 45), (520, 55), (580, 20), (620, 70),
    (680, 15), (720, 65), (780, 10), (820, 75), (880, 80),
    (920, 30), (960, 40), (1100, 50), (1200, 25), (1300, 60),
    (1400, 35), (1500, 45), (1600, 20), (1700, 55), (1800, 70),
]

random.shuffle(easy_filler_values)
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
idx = 0
while easy_count < 200 and idx < len(easy_filler_values):
    whole, pct = easy_filler_values[idx]
    part = whole * pct / 100
    ctx = easy_filler_contexts[idx % len(easy_filler_contexts)]
    q_text = ctx.format(whole=whole, pct=pct)
    choices, answer = make_number_choices(part)
    explanation = f"{pct}% of {whole:,} = {pct/100} \u00d7 {whole:,} = {fmt_num(part)}."
    add_q("Easy", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the part", "real-life applications"])
    easy_count += 1
    idx += 1


# --- Medium fillers: more reverse/practical problems ---
medium_filler_contexts = [
    ("If {pct}% of a number is {part}, what is the number?",
     "finding the whole"),
    ("A worker answered {part} items correctly on a {whole}-item test. What is the score in percent?",
     "finding the rate"),
    ("{part} out of {whole} employees were promoted. What percentage were promoted?",
     "finding the rate"),
    ("A tank is {pct}% full with {part} liters. What is the full capacity?",
     "finding the whole"),
]

medium_filler_data_whole = [
    (60, 25), (90, 30), (120, 40), (45, 15), (80, 20),
    (150, 50), (72, 24), (36, 12), (108, 36), (54, 18),
    (84, 28), (96, 32), (132, 44), (48, 16), (66, 22),
    (75, 25), (105, 35), (135, 45), (42, 14), (63, 21),
    (78, 26), (99, 33), (111, 37), (57, 19), (87, 29),
    (114, 38), (126, 42), (138, 46), (69, 23), (81, 27),
    (93, 31), (117, 39), (129, 43), (141, 47), (51, 17),
    (144, 48), (147, 49), (102, 34), (123, 41), (33, 11),
]

random.shuffle(medium_filler_data_whole)
medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
idx = 0
while medium_count < 200 and idx < len(medium_filler_data_whole):
    part, pct = medium_filler_data_whole[idx]
    whole = part / (pct / 100)
    q_text = f"If {pct}% of a number is {part}, what is the number?"
    choices, answer = make_number_choices(whole)
    explanation = f"{pct}% \u00d7 x = {part}. x = {part} \u00f7 {pct/100} = {fmt_num(whole)}."
    add_q("Medium", q_text, choices, answer, explanation,
          ["percentage word problems", "finding the whole", "reverse percentage"])
    medium_count += 1
    idx += 1


# --- Hard fillers: more multi-step and reverse problems ---
hard_filler_scenarios = [
    # Net effect problems
    ("A value is increased by {inc}% then decreased by {dec}%. "
     "What is the net percentage change from the original?",
     lambda inc, dec: round((((1 + inc/100) * (1 - dec/100)) - 1) * 100, 2)),
]

hard_filler_pairs = [
    (10, 10), (20, 20), (30, 30), (15, 15), (25, 25),
    (10, 20), (20, 10), (30, 10), (10, 30), (15, 20),
    (20, 15), (25, 10), (10, 25), (30, 20), (20, 30),
    (5, 5), (40, 40), (50, 50), (35, 15), (15, 35),
    (12, 8), (8, 12), (18, 12), (12, 18), (22, 8),
    (8, 22), (28, 12), (12, 28), (32, 18), (18, 32),
    (5, 10), (10, 5), (15, 5), (5, 15), (25, 5),
    (5, 25), (35, 5), (5, 35), (45, 5), (5, 45),
]

random.shuffle(hard_filler_pairs)
hard_count = len([q for q in questions if q["difficulty"] == "Hard"])
idx = 0
while hard_count < 200 and idx < len(hard_filler_pairs):
    inc, dec = hard_filler_pairs[idx]
    net = round((((1 + inc/100) * (1 - dec/100)) - 1) * 100, 2)
    if net > 0:
        direction = "increase"
        net_abs = net
    elif net < 0:
        direction = "decrease"
        net_abs = abs(net)
    else:
        direction = "no change"
        net_abs = 0

    q_text = (f"A price is increased by {inc}% then decreased by {dec}%. "
              f"What is the net percentage change from the original?")

    if net_abs == 0:
        correct_str = "No change (0%)"
        d1 = f"{inc - dec}% increase" if inc > dec else f"{dec - inc}% decrease"
        d2 = f"{round(net_abs + 1, 2)}% decrease"
        d3 = f"{round(net_abs + 2, 2)}% increase"
    elif direction == "increase":
        correct_str = f"{fmt_num(net_abs)}% increase"
        d1 = f"{fmt_num(net_abs)}% decrease"
        d2 = f"{inc - dec}% {'increase' if inc > dec else 'decrease'}"
        d3 = f"{fmt_num(net_abs + 2)}% increase"
    else:
        correct_str = f"{fmt_num(net_abs)}% decrease"
        d1 = f"{fmt_num(net_abs)}% increase"
        d2 = f"{abs(inc - dec)}% {'increase' if inc > dec else 'decrease'}"
        d3 = f"{fmt_num(net_abs + 2)}% decrease"

    choices = list(dict.fromkeys([correct_str, d1, d2, d3]))
    while len(choices) < 4:
        choices.append(f"{fmt_num(net_abs + len(choices))}% change")
    choices = choices[:4]
    random.shuffle(choices)

    multiplier = round((1 + inc/100) * (1 - dec/100), 4)
    explanation = (f"Net multiplier = {1 + inc/100} \u00d7 {1 - dec/100} = {multiplier}. "
                   f"Net change = ({multiplier} \u2212 1) \u00d7 100 = {fmt_num(net)}%. "
                   f"This is a {direction} of {fmt_num(net_abs)}%.")
    add_q("Hard", q_text, choices, correct_str, explanation,
          ["percentage word problems", "net percentage change", "successive changes"])
    hard_count += 1
    idx += 1


# ============================================================
# FINAL VALIDATION AND OUTPUT
# ============================================================

def validate_questions() -> None:
    """Validate all questions meet quality requirements."""
    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]

    print(f"Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")
    print(f"Total: {len(questions)}")

    # Verify answer is in choices
    errors = 0
    for q in questions:
        if q["answer"] not in q["choices"]:
            print(f"  ERROR: Q{q['id']} answer '{q['answer']}' not in choices")
            errors += 1
        if len(q["choices"]) != 4:
            print(f"  ERROR: Q{q['id']} has {len(q['choices'])} choices (expected 4)")
            errors += 1

    if errors:
        print(f"\n  {errors} errors found!")
    else:
        print("  All questions validated successfully.")


def main() -> None:
    validate_questions()

    # Take exactly 200 per difficulty
    easy = [q for q in questions if q["difficulty"] == "Easy"][:200]
    medium = [q for q in questions if q["difficulty"] == "Medium"][:200]
    hard = [q for q in questions if q["difficulty"] == "Hard"][:200]
    final = easy + medium + hard

    # Reassign sequential IDs
    for i, q in enumerate(final, start=1):
        q["id"] = i

    print(f"\nFinal count: {len(final)} questions")
    print(f"  Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(final, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
