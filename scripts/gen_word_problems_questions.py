"""
Generate 600 word problems for the CSE Numerical Ability section.
200 Easy / 200 Medium / 200 Hard

Subtopic: Word Problems Using Basic Operations

Run: python scripts/gen_word_problems_questions.py
Output: data/seed/questions/numerical-ability/basic-operations/word-problems/questions.json
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
        "module": "Basic Operations",
        "subtopic": "Word Problems Using Basic Operations",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags
    })


def fmt(n):
    """Format number: integers with commas, floats trimmed."""
    if isinstance(n, float):
        if n == int(n):
            return f"{int(n):,}"
        s = f"{n:,.2f}"
        return s
    return f"{n:,}"


def peso(n):
    """Format as Philippine peso."""
    if isinstance(n, float):
        if n == int(n):
            return f"\u20b1{int(n):,}"
        return f"\u20b1{n:,.2f}"
    return f"\u20b1{n:,}"


def make_choices_int(correct, spread=None):
    """Generate 4 choices for an integer answer."""
    if spread is None:
        spread = max(3, abs(correct) // 8)
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        offset = random.choice([-3, -2, -1, 1, 2, 3]) * random.randint(1, max(1, spread))
        d = correct + offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(correct + len(distractors) + 1)
    choices = [fmt(correct)] + [fmt(d) for d in distractors]
    random.shuffle(choices)
    return choices, fmt(correct)


def make_choices_peso(correct, spread=None):
    """Generate 4 choices for a peso amount (integer)."""
    if spread is None:
        spread = max(50, abs(correct) // 10)
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        offset = random.choice([-3, -2, -1, 1, 2, 3]) * random.randint(1, max(1, spread // 10)) * 10
        d = correct + offset
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(correct + (len(distractors) + 1) * 100)
    choices = [peso(correct)] + [peso(d) for d in distractors]
    random.shuffle(choices)
    return choices, peso(correct)


def make_choices_decimal_peso(correct):
    """Generate 4 choices for a decimal peso amount."""
    correct_r = round(correct, 2)
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        offset = random.choice([-50, -25, -10, -5, 5, 10, 25, 50, 100, -100])
        d = round(correct_r + offset, 2)
        if d != correct_r and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(round(correct_r + (len(distractors) + 1) * 25, 2))
    choices = [peso(correct_r)] + [peso(d) for d in distractors]
    random.shuffle(choices)
    return choices, peso(correct_r)


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Single-step addition word problems (1-35) ---
easy_add_templates = [
    ("A government office has {a} employees in Building A and {b} employees in Building B. How many employees are there in total?",
     "total employees", "addition"),
    ("A school collected {a_p} from Section A and {b_p} from Section B for a field trip. What is the total collection?",
     "total collection", "addition"),
    ("A warehouse received {a} boxes on Monday and {b} boxes on Tuesday. How many boxes were received in total?",
     "total boxes", "addition"),
    ("A library has {a} fiction books and {b} non-fiction books. How many books does the library have in all?",
     "total books", "addition"),
    ("A municipal office processed {a} applications in the morning and {b} in the afternoon. How many applications were processed that day?",
     "total applications", "addition"),
    ("A barangay has {a} registered male voters and {b} registered female voters. What is the total number of registered voters?",
     "total voters", "addition"),
    ("A government hospital admitted {a} patients in January and {b} patients in February. What is the total number of admissions?",
     "total admissions", "addition"),
]

for i in range(35):
    template_data = easy_add_templates[i % len(easy_add_templates)]
    template, context, op = template_data
    a = random.randint(80, 500)
    b = random.randint(60, 450)
    correct = a + b
    if "{a_p}" in template:
        q_text = template.format(a_p=peso(a * 100), b_p=peso(b * 100))
        correct = (a + b) * 100
        choices, ans = make_choices_peso(correct)
        expl = f"Add the two amounts: {peso(a*100)} + {peso(b*100)} = {peso(correct)}."
    else:
        q_text = template.format(a=fmt(a), b=fmt(b))
        choices, ans = make_choices_int(correct)
        expl = f"Add the two quantities: {fmt(a)} + {fmt(b)} = {fmt(correct)}."
    add_q("Easy", q_text, choices, ans, expl,
          ["word problems", "addition", "single-step"])

# --- Easy: Single-step subtraction word problems (36-70) ---
easy_sub_templates = [
    ("A store had {a} items in stock. After selling {b} items, how many remain?",
     "remaining items", "subtraction"),
    ("An employee's gross salary is {a_p}. If deductions total {b_p}, what is the net pay?",
     "net pay", "subtraction"),
    ("A water tank contains {a} liters. If {b} liters are used, how many liters remain?",
     "remaining liters", "subtraction"),
    ("A government office had {a} reams of paper. After using {b} reams, how many are left?",
     "remaining reams", "subtraction"),
    ("A school has {a} enrolled students. If {b} students transferred out, how many remain?",
     "remaining students", "subtraction"),
    ("A budget of {a_p} had {b_p} spent on supplies. How much budget remains?",
     "remaining budget", "subtraction"),
    ("A warehouse had {a} relief packs. After distributing {b} packs, how many are left?",
     "remaining packs", "subtraction"),
]

for i in range(35):
    template_data = easy_sub_templates[i % len(easy_sub_templates)]
    template, context, op = template_data
    a = random.randint(200, 2000)
    b = random.randint(50, a - 20)
    correct = a - b
    if "{a_p}" in template:
        q_text = template.format(a_p=peso(a * 10), b_p=peso(b * 10))
        correct = (a - b) * 10
        choices, ans = make_choices_peso(correct)
        expl = f"Subtract: {peso(a*10)} - {peso(b*10)} = {peso(correct)}."
    else:
        q_text = template.format(a=fmt(a), b=fmt(b))
        choices, ans = make_choices_int(correct)
        expl = f"Subtract: {fmt(a)} - {fmt(b)} = {fmt(correct)}."
    add_q("Easy", q_text, choices, ans, expl,
          ["word problems", "subtraction", "single-step"])


# --- Easy: Single-step multiplication word problems (71-110) ---
easy_mul_templates = [
    ("A government office purchased {a} folders at {b_p} each. What is the total cost?",
     "total cost", ["word problems", "multiplication", "single-step", "procurement"]),
    ("A clerk processes {a} documents per hour. How many documents can she process in {b} hours?",
     "total documents", ["word problems", "multiplication", "single-step", "productivity"]),
    ("Each employee receives {b_p} as meal allowance per day. How much is the total meal allowance for {a} employees?",
     "total allowance", ["word problems", "multiplication", "single-step", "payroll"]),
    ("A printer produces {a} pages per minute. How many pages can it print in {b} minutes?",
     "total pages", ["word problems", "multiplication", "single-step", "production"]),
    ("A bus makes {a} trips per day carrying {b} passengers per trip. How many passengers are transported daily?",
     "total passengers", ["word problems", "multiplication", "single-step", "transportation"]),
    ("A farmer plants {a} seedlings per row. If there are {b} rows, how many seedlings are planted in total?",
     "total seedlings", ["word problems", "multiplication", "single-step", "agriculture"]),
    ("A factory produces {a} units per shift. How many units are produced in {b} shifts?",
     "total units", ["word problems", "multiplication", "single-step", "production"]),
    ("Each classroom has {a} chairs. If there are {b} classrooms, how many chairs are there in total?",
     "total chairs", ["word problems", "multiplication", "single-step", "inventory"]),
]

for i in range(40):
    template_data = easy_mul_templates[i % len(easy_mul_templates)]
    template, context, tags = template_data
    if "purchased" in template or "allowance" in template:
        a = random.randint(8, 60)
        b = random.randint(15, 250)
        correct = a * b
        q_text = template.format(a=fmt(a), b_p=peso(b))
        choices, ans = make_choices_peso(correct)
        expl = f"Multiply: {fmt(a)} × {peso(b)} = {peso(correct)}."
    else:
        a = random.randint(12, 80)
        b = random.randint(5, 30)
        correct = a * b
        q_text = template.format(a=fmt(a), b=fmt(b))
        choices, ans = make_choices_int(correct)
        expl = f"Multiply: {fmt(a)} × {fmt(b)} = {fmt(correct)}."
    add_q("Easy", q_text, choices, ans, expl, tags)

# --- Easy: Single-step division word problems (111-150) ---
easy_div_templates = [
    ("A total of {a} booklets are distributed equally among {b} schools. How many booklets does each school receive?",
     "booklets per school", ["word problems", "division", "single-step", "distribution"]),
    ("A government vehicle traveled {a} km on {b} liters of fuel. What is the fuel efficiency in km/L?",
     "km per liter", ["word problems", "division", "single-step", "transportation"]),
    ("An annual budget of {a_p} is divided into 12 monthly allocations. What is the monthly budget?",
     "monthly budget", ["word problems", "division", "single-step", "budgeting"]),
    ("A rope measuring {a} meters is cut into {b} equal pieces. How long is each piece?",
     "meters per piece", ["word problems", "division", "single-step", "measurement"]),
    ("A donation of {a_p} is shared equally among {b} families. How much does each family receive?",
     "per family", ["word problems", "division", "single-step", "sharing"]),
    ("A training has {a} participants seated at tables of {b}. How many tables are needed?",
     "tables", ["word problems", "division", "single-step", "grouping"]),
    ("A warehouse has {a} items packed in boxes of {b}. How many boxes are there?",
     "boxes", ["word problems", "division", "single-step", "packing"]),
    ("A project requires {a} work-hours completed by {b} workers equally. How many hours per worker?",
     "hours per worker", ["word problems", "division", "single-step", "labor"]),
]

for i in range(40):
    template_data = easy_div_templates[i % len(easy_div_templates)]
    template, context, tags = template_data
    if "annual budget" in template:
        monthly = random.randint(10, 80) * 1000
        a = monthly * 12
        correct = monthly
        q_text = template.format(a_p=peso(a))
        choices, ans = make_choices_peso(correct)
        expl = f"Divide: {peso(a)} ÷ 12 = {peso(correct)} per month."
    elif "donation" in template:
        b = random.choice([5, 6, 8, 10, 12, 15, 20, 25])
        per_family = random.randint(5, 50) * 100
        a = per_family * b
        correct = per_family
        q_text = template.format(a_p=peso(a), b=fmt(b))
        choices, ans = make_choices_peso(correct)
        expl = f"Divide: {peso(a)} ÷ {fmt(b)} = {peso(correct)} per family."
    else:
        b = random.choice([4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 25])
        quotient = random.randint(8, 120)
        a = quotient * b
        correct = quotient
        q_text = template.format(a=fmt(a), b=fmt(b))
        choices, ans = make_choices_int(correct)
        expl = f"Divide: {fmt(a)} ÷ {fmt(b)} = {fmt(correct)}."
    add_q("Easy", q_text, choices, ans, expl, tags)


# --- Easy: Identifying the operation (151-170) ---
easy_identify_op = [
    ("A government office has 234 employees in Division A and 189 in Division B. To find the total number of employees, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Addition",
     "Finding the total of two groups requires addition.",
     ["word problems", "operation identification", "addition"]),
    ("An employee earns ₱685 per day for 22 days. To find the monthly salary, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding the total from a rate and quantity requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
    ("A budget of ₱480,000 is shared equally among 12 departments. To find each department's share, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Division",
     "Distributing equally requires division.",
     ["word problems", "operation identification", "division"]),
    ("A store had 500 items and sold 185. To find the remaining stock, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Subtraction",
     "Finding what remains after removal requires subtraction.",
     ["word problems", "operation identification", "subtraction"]),
    ("A box contains 24 packets. To find how many packets are in 15 boxes, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding the total from equal groups requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
    ("A total of 360 passengers need transport. Each bus carries 45. To find the number of trips needed, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Division",
     "Finding how many groups of a given size fit into a total requires division.",
     ["word problems", "operation identification", "division"]),
    ("A company's revenue is ₱2,500,000 and expenses are ₱1,800,000. To find the profit, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Subtraction",
     "Finding the difference between revenue and expenses requires subtraction.",
     ["word problems", "operation identification", "subtraction"]),
    ("Three offices have 45, 62, and 38 employees. To find the total workforce, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Addition",
     "Combining multiple quantities requires addition.",
     ["word problems", "operation identification", "addition"]),
    ("A pipe is 120 meters long and must be cut into 8-meter pieces. To find the number of pieces, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Division",
     "Finding how many equal pieces fit into a length requires division.",
     ["word problems", "operation identification", "division"]),
    ("Each student needs 3 notebooks. To find how many notebooks are needed for 48 students, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding the total from a per-person quantity and number of people requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
    ("A tank has 2,000 liters. After using 750 liters, to find the remaining water, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Subtraction",
     "Finding what remains after consumption requires subtraction.",
     ["word problems", "operation identification", "subtraction"]),
    ("A school collected ₱15,000 from Grade 1 and ₱12,500 from Grade 2. To find the total collection, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Addition",
     "Combining collections requires addition.",
     ["word problems", "operation identification", "addition"]),
    ("An office has 240 chairs arranged in rows of 12. To find the number of rows, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Division",
     "Finding how many groups of a given size requires division.",
     ["word problems", "operation identification", "division"]),
    ("A worker earns ₱95 per hour. To find earnings for 8 hours, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding total earnings from hourly rate and hours requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
    ("A company had 450 employees. After 67 resigned, to find the current workforce, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Subtraction",
     "Finding the remaining count after departures requires subtraction.",
     ["word problems", "operation identification", "subtraction"]),
    ("A fleet of 6 trucks each carries 85 sacks. To find the total sacks transported, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding the total from equal loads requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
    ("A donation of ₱90,000 is split among 15 beneficiaries. To find each person's share, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Division",
     "Splitting equally requires division.",
     ["word problems", "operation identification", "division"]),
    ("A government office received 320 new files and already had 1,450 files. To find the total files, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Addition",
     "Combining existing and new quantities requires addition.",
     ["word problems", "operation identification", "addition"]),
    ("A project budget is ₱500,000. After spending ₱187,500, to find the remaining budget, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Subtraction",
     "Finding the remainder after spending requires subtraction.",
     ["word problems", "operation identification", "subtraction"]),
    ("A hall has 35 rows with 28 seats each. To find the total seating capacity, which operation should be used?",
     ["Addition", "Subtraction", "Multiplication", "Division"], "Multiplication",
     "Finding total from rows and seats per row requires multiplication.",
     ["word problems", "operation identification", "multiplication"]),
]

for q_text, choices, answer, explanation, tags in easy_identify_op:
    add_q("Easy", q_text, choices, answer, explanation, tags)


# --- Easy: Translation problems (171-190) ---
easy_translation = [
    ("Which mathematical expression represents 'the sum of 45 and 23'?",
     ["45 + 23", "45 - 23", "45 × 23", "45 ÷ 23"], "45 + 23",
     "'Sum of' indicates addition: 45 + 23.",
     ["word problems", "translation", "addition"]),
    ("Which expression represents '12 less than 50'?",
     ["50 - 12", "12 - 50", "50 + 12", "50 × 12"], "50 - 12",
     "'Less than' means subtract from the larger number: 50 - 12.",
     ["word problems", "translation", "subtraction"]),
    ("Which expression represents 'the product of 8 and 15'?",
     ["8 × 15", "8 + 15", "15 - 8", "15 ÷ 8"], "8 × 15",
     "'Product of' indicates multiplication: 8 × 15.",
     ["word problems", "translation", "multiplication"]),
    ("Which expression represents '96 divided equally among 8'?",
     ["96 ÷ 8", "96 × 8", "96 - 8", "96 + 8"], "96 ÷ 8",
     "'Divided equally among' indicates division: 96 ÷ 8.",
     ["word problems", "translation", "division"]),
    ("Which expression represents 'a salary of ₱25,000 increased by ₱3,500'?",
     ["25,000 + 3,500", "25,000 - 3,500", "25,000 × 3,500", "25,000 ÷ 3,500"], "25,000 + 3,500",
     "'Increased by' indicates addition: 25,000 + 3,500.",
     ["word problems", "translation", "addition"]),
    ("Which expression represents 'the total cost of 15 items at ₱245 each'?",
     ["15 × 245", "15 + 245", "245 - 15", "245 ÷ 15"], "15 × 245",
     "Total cost = quantity × unit price: 15 × 245.",
     ["word problems", "translation", "multiplication"]),
    ("Which expression represents 'the remaining budget after spending ₱45,000 from ₱120,000'?",
     ["120,000 - 45,000", "120,000 + 45,000", "45,000 - 120,000", "120,000 ÷ 45,000"],
     "120,000 - 45,000",
     "'Remaining after spending' indicates subtraction: 120,000 - 45,000.",
     ["word problems", "translation", "subtraction"]),
    ("Which expression represents 'the average of 78, 85, 92, and 65'?",
     ["(78 + 85 + 92 + 65) ÷ 4", "78 + 85 + 92 + 65", "78 × 85 × 92 × 65", "(78 + 65) ÷ 2"],
     "(78 + 85 + 92 + 65) ÷ 4",
     "Average = sum of all values ÷ count: (78 + 85 + 92 + 65) ÷ 4.",
     ["word problems", "translation", "average"]),
    ("Which expression represents 'twice the amount of ₱4,500'?",
     ["2 × 4,500", "4,500 + 2", "4,500 ÷ 2", "4,500 - 2"], "2 × 4,500",
     "'Twice' means multiply by 2: 2 × 4,500.",
     ["word problems", "translation", "multiplication"]),
    ("Which expression represents '₱36,000 shared equally among 4 employees'?",
     ["36,000 ÷ 4", "36,000 × 4", "36,000 - 4", "36,000 + 4"], "36,000 ÷ 4",
     "'Shared equally among' indicates division: 36,000 ÷ 4.",
     ["word problems", "translation", "division"]),
    ("Which expression represents '150 decreased by 38'?",
     ["150 - 38", "150 + 38", "38 - 150", "150 × 38"], "150 - 38",
     "'Decreased by' indicates subtraction: 150 - 38.",
     ["word problems", "translation", "subtraction"]),
    ("Which expression represents 'the combined total of 234, 189, and 312'?",
     ["234 + 189 + 312", "312 - 234 - 189", "234 × 189 × 312", "(234 + 312) ÷ 189"],
     "234 + 189 + 312",
     "'Combined total' indicates addition of all values.",
     ["word problems", "translation", "addition"]),
    ("Which expression represents '₱840 for 24 items, cost per item'?",
     ["840 ÷ 24", "840 × 24", "840 - 24", "840 + 24"], "840 ÷ 24",
     "Finding cost per item requires dividing total by quantity: 840 ÷ 24.",
     ["word problems", "translation", "division"]),
    ("Which expression represents '5 more than triple a number n'?",
     ["3n + 5", "3(n + 5)", "5n + 3", "3 + n + 5"], "3n + 5",
     "'Triple a number' is 3n; '5 more than' adds 5: 3n + 5.",
     ["word problems", "translation", "algebraic"]),
    ("Which expression represents 'the difference between 500 and 187'?",
     ["500 - 187", "187 - 500", "500 + 187", "500 ÷ 187"], "500 - 187",
     "'Difference between' means subtract the smaller from the larger: 500 - 187.",
     ["word problems", "translation", "subtraction"]),
    ("Which expression represents 'a daily rate of ₱750 for 22 working days'?",
     ["750 × 22", "750 + 22", "750 ÷ 22", "750 - 22"], "750 × 22",
     "Total earnings = daily rate × number of days: 750 × 22.",
     ["word problems", "translation", "multiplication"]),
    ("Which expression represents '₱18,600,000 divided into quarterly allocations'?",
     ["18,600,000 ÷ 4", "18,600,000 × 4", "18,600,000 - 4", "18,600,000 + 4"],
     "18,600,000 ÷ 4",
     "Quarterly means 4 periods per year: 18,600,000 ÷ 4.",
     ["word problems", "translation", "division"]),
    ("Which expression represents 'the total of 3 groups: 45, 62, and 38'?",
     ["45 + 62 + 38", "45 × 62 × 38", "(45 + 38) - 62", "62 - 45 + 38"], "45 + 62 + 38",
     "Finding the total of multiple groups requires addition.",
     ["word problems", "translation", "addition"]),
    ("Which expression represents '₱2,400 reduced by ₱850'?",
     ["2,400 - 850", "2,400 + 850", "850 - 2,400", "2,400 × 850"], "2,400 - 850",
     "'Reduced by' indicates subtraction: 2,400 - 850.",
     ["word problems", "translation", "subtraction"]),
    ("Which expression represents 'the area of a lot measuring 45 m by 32 m'?",
     ["45 × 32", "45 + 32", "45 - 32", "45 ÷ 32"], "45 × 32",
     "Area = length × width: 45 × 32.",
     ["word problems", "translation", "multiplication"]),
]

for q_text, choices, answer, explanation, tags in easy_translation:
    add_q("Easy", q_text, choices, answer, explanation, tags)


# --- Easy: Simple practical word problems (191-200) ---
easy_practical = [
    ("A government canteen serves 85 meals at lunch. If each meal costs ₱65, what is the total cost of lunch meals?",
     85 * 65, "Multiply: 85 × ₱65 = ₱5,525.", ["word problems", "multiplication", "practical"]),
    ("A clerk filed 342 documents on Monday and 278 on Tuesday. How many documents were filed in total?",
     342 + 278, "Add: 342 + 278 = 620.", ["word problems", "addition", "practical"]),
    ("A government vehicle's odometer reads 45,230 km at the start and 45,680 km at the end of the week. How many km were traveled?",
     45680 - 45230, "Subtract: 45,680 - 45,230 = 450 km.", ["word problems", "subtraction", "practical"]),
    ("A total of 1,080 exam papers are divided equally among 36 proctors. How many papers does each proctor receive?",
     1080 // 36, "Divide: 1,080 ÷ 36 = 30 papers per proctor.", ["word problems", "division", "practical"]),
    ("A barangay hall has 18 rows of chairs with 25 chairs per row. What is the seating capacity?",
     18 * 25, "Multiply: 18 × 25 = 450 seats.", ["word problems", "multiplication", "practical"]),
    ("An office supply budget is ₱24,000. If ₱8,750 is spent on paper and ₱6,200 on ink, how much remains?",
     24000 - 8750 - 6200, "Subtract: ₱24,000 - ₱8,750 - ₱6,200 = ₱9,050.", ["word problems", "subtraction", "practical"]),
    ("A government agency has 5 divisions with 48, 52, 45, 61, and 54 employees. What is the total workforce?",
     48 + 52 + 45 + 61 + 54, "Add all: 48 + 52 + 45 + 61 + 54 = 260.", ["word problems", "addition", "practical"]),
    ("A delivery truck makes 4 trips per day carrying 125 boxes each trip. How many boxes are delivered daily?",
     4 * 125, "Multiply: 4 × 125 = 500 boxes.", ["word problems", "multiplication", "practical"]),
    ("A school year has 200 school days. If 156 days have passed, how many school days remain?",
     200 - 156, "Subtract: 200 - 156 = 44 days.", ["word problems", "subtraction", "practical"]),
    ("A total of 2,520 relief goods are packed into bags of 18 items each. How many bags are needed?",
     2520 // 18, "Divide: 2,520 ÷ 18 = 140 bags.", ["word problems", "division", "practical"]),
]

for q_text, correct, explanation, tags in easy_practical:
    if correct > 5000:
        choices, ans = make_choices_peso(correct) if "₱" in q_text or "cost" in q_text else make_choices_int(correct)
    else:
        choices, ans = make_choices_int(correct)
    add_q("Easy", q_text, choices, ans, explanation, tags)


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Two-step word problems (201-260) ---
medium_two_step = [
    ("An employee earns ₱{rate} per day. If she works {days} days and her deductions total ₱{ded}, what is her net pay?",
     "multiply_subtract", ["word problems", "multi-step", "payroll"]),
    ("A store sold {a} items at ₱{price_a} each and {b} items at ₱{price_b} each. What is the total revenue?",
     "multiply_add", ["word problems", "multi-step", "sales"]),
    ("A budget of ₱{total} had ₱{spent} already spent. If the remainder is divided equally among {months} months, how much per month?",
     "subtract_divide", ["word problems", "multi-step", "budgeting"]),
    ("A warehouse received {recv} boxes and distributed {dist}. If the remaining boxes are stored in shelves of {per_shelf}, how many shelves are needed?",
     "subtract_divide_int", ["word problems", "multi-step", "inventory"]),
    ("A company has {emp} employees. Each receives a bonus of ₱{bonus}. If the company also pays ₱{tax} in taxes, what is the total expense?",
     "multiply_add_tax", ["word problems", "multi-step", "payroll"]),
]

for i in range(60):
    idx = i % len(medium_two_step)
    template, op_type, tags = medium_two_step[idx]

    if op_type == "multiply_subtract":
        rate = random.choice([550, 600, 650, 685, 700, 750, 800, 850, 900, 950])
        days = random.randint(18, 25)
        ded = random.randint(2, 8) * 500
        gross = rate * days
        correct = gross - ded
        q_text = template.format(rate=fmt(rate), days=days, ded=fmt(ded))
        choices, ans = make_choices_peso(correct)
        expl = f"Gross pay: {fmt(rate)} × {days} = {peso(gross)}. Net pay: {peso(gross)} - {peso(ded)} = {peso(correct)}."

    elif op_type == "multiply_add":
        a = random.randint(20, 80)
        b = random.randint(15, 60)
        price_a = random.randint(50, 300)
        price_b = random.randint(40, 250)
        rev_a = a * price_a
        rev_b = b * price_b
        correct = rev_a + rev_b
        q_text = template.format(a=fmt(a), price_a=fmt(price_a), b=fmt(b), price_b=fmt(price_b))
        choices, ans = make_choices_peso(correct)
        expl = f"Revenue A: {fmt(a)} × {peso(price_a)} = {peso(rev_a)}. Revenue B: {fmt(b)} × {peso(price_b)} = {peso(rev_b)}. Total: {peso(correct)}."

    elif op_type == "subtract_divide":
        months = random.choice([3, 4, 5, 6, 7, 8, 9])
        per_month = random.randint(20, 100) * 1000
        spent = random.randint(50, 300) * 1000
        total = spent + per_month * months
        correct = per_month
        q_text = template.format(total=fmt(total), spent=fmt(spent), months=months)
        choices, ans = make_choices_peso(correct)
        expl = f"Remaining: {peso(total)} - {peso(spent)} = {peso(total - spent)}. Per month: {peso(total - spent)} ÷ {months} = {peso(correct)}."

    elif op_type == "subtract_divide_int":
        per_shelf = random.choice([8, 10, 12, 15, 20, 24, 25])
        shelves_needed = random.randint(10, 40)
        dist = random.randint(50, 300)
        remaining = shelves_needed * per_shelf
        recv = remaining + dist
        correct = shelves_needed
        q_text = template.format(recv=fmt(recv), dist=fmt(dist), per_shelf=per_shelf)
        choices, ans = make_choices_int(correct)
        expl = f"Remaining: {fmt(recv)} - {fmt(dist)} = {fmt(remaining)}. Shelves: {fmt(remaining)} ÷ {per_shelf} = {fmt(correct)}."

    elif op_type == "multiply_add_tax":
        emp = random.randint(20, 100)
        bonus = random.randint(3, 15) * 1000
        tax = random.randint(50, 200) * 1000
        bonus_total = emp * bonus
        correct = bonus_total + tax
        q_text = template.format(emp=fmt(emp), bonus=fmt(bonus), tax=fmt(tax))
        choices, ans = make_choices_peso(correct)
        expl = f"Bonus total: {fmt(emp)} × {peso(bonus)} = {peso(bonus_total)}. Total expense: {peso(bonus_total)} + {peso(tax)} = {peso(correct)}."

    add_q("Medium", q_text, choices, ans, expl, tags)


# --- Medium: Decimal word problems (261-310) ---
medium_decimal = [
    ("An office supply purchase includes {a} pens at ₱{pa} each and {b} notebooks at ₱{pb} each. What is the total cost?",
     "two_items", ["word problems", "decimals", "multi-step", "procurement"]),
    ("An employee's daily rate is ₱{rate}. What is the total pay for {days} working days?",
     "rate_days", ["word problems", "decimals", "single-step", "payroll"]),
    ("A government vehicle traveled {km} km using {liters} liters of fuel. What is the fuel efficiency in km/L?",
     "efficiency", ["word problems", "decimals", "division", "transportation"]),
    ("A pipe measuring {length} meters is cut into pieces of {piece} meters each. How many complete pieces can be cut?",
     "cutting", ["word problems", "decimals", "division", "measurement"]),
    ("An item originally costs ₱{orig}. If a discount of ₱{disc} is applied, what is the sale price?",
     "discount", ["word problems", "decimals", "subtraction", "shopping"]),
]

for i in range(50):
    idx = i % len(medium_decimal)
    template, op_type, tags = medium_decimal[idx]

    if op_type == "two_items":
        a = random.randint(5, 30)
        b = random.randint(3, 20)
        pa = round(random.uniform(12.5, 85.75), 2)
        pb = round(random.uniform(25.0, 150.0), 2)
        # Make prices end in .25, .50, .75, or .00 for cleaner math
        pa = round(random.randint(12, 85) + random.choice([0, 0.25, 0.50, 0.75]), 2)
        pb = round(random.randint(25, 150) + random.choice([0, 0.25, 0.50, 0.75]), 2)
        total_a = round(a * pa, 2)
        total_b = round(b * pb, 2)
        correct = round(total_a + total_b, 2)
        q_text = template.format(a=a, pa=f"{pa:.2f}", b=b, pb=f"{pb:.2f}")
        choices, ans = make_choices_decimal_peso(correct)
        expl = f"Pens: {a} × ₱{pa:.2f} = ₱{total_a:,.2f}. Notebooks: {b} × ₱{pb:.2f} = ₱{total_b:,.2f}. Total: ₱{correct:,.2f}."

    elif op_type == "rate_days":
        rate = round(random.randint(500, 1500) + random.choice([0, 0.50, 0.25, 0.75]), 2)
        days = random.randint(15, 26)
        correct = round(rate * days, 2)
        q_text = template.format(rate=f"{rate:,.2f}", days=days)
        choices, ans = make_choices_decimal_peso(correct)
        expl = f"Total pay: ₱{rate:,.2f} × {days} = ₱{correct:,.2f}."

    elif op_type == "efficiency":
        # Make it divide evenly or to 1-2 decimal places
        eff = round(random.uniform(8.0, 18.0), 1)
        liters = round(random.uniform(20.0, 60.0), 1)
        km = round(eff * liters, 1)
        correct = eff
        q_text = template.format(km=f"{km}", liters=f"{liters}")
        distractors = set()
        attempts = 0
        while len(distractors) < 3 and attempts < 100:
            d = round(correct + random.choice([-2.5, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.5]), 1)
            if d != correct and d > 0:
                distractors.add(d)
            attempts += 1
        while len(distractors) < 3:
            distractors.add(round(correct + len(distractors) + 1, 1))
        choices = [f"{correct} km/L"] + [f"{d} km/L" for d in distractors]
        random.shuffle(choices)
        ans = f"{correct} km/L"
        expl = f"Fuel efficiency: {km} ÷ {liters} = {correct} km/L."

    elif op_type == "cutting":
        piece = round(random.choice([0.75, 1.25, 1.5, 2.25, 2.5, 3.75]), 2)
        num_pieces = random.randint(5, 20)
        leftover = round(random.uniform(0.1, piece - 0.1), 2)
        length = round(num_pieces * piece + leftover, 2)
        correct = num_pieces
        q_text = template.format(length=f"{length}", piece=f"{piece}")
        choices, ans = make_choices_int(correct)
        expl = f"Divide: {length} ÷ {piece} = {length/piece:.2f}. Complete pieces: {correct}."

    elif op_type == "discount":
        orig = round(random.randint(200, 2000) + random.choice([0, 0.50, 0.75, 0.25]), 2)
        disc = round(random.uniform(20, orig * 0.4), 2)
        disc = round(random.randint(20, int(orig * 0.3)) + random.choice([0, 0.25, 0.50, 0.75]), 2)
        correct = round(orig - disc, 2)
        q_text = template.format(orig=f"{orig:,.2f}", disc=f"{disc:,.2f}")
        choices, ans = make_choices_decimal_peso(correct)
        expl = f"Sale price: ₱{orig:,.2f} - ₱{disc:,.2f} = ₱{correct:,.2f}."

    add_q("Medium", q_text, choices, ans, expl, tags)


# --- Medium: Comparison and "more/less than" problems (311-340) ---
medium_comparison = [
    ("Department A has {a} employees. Department B has {diff} more employees than Department A. How many employees does Department B have?",
     "more_than_add", ["word problems", "comparison", "addition"]),
    ("Store A sold {a} items. Store B sold {diff} fewer items than Store A. How many items did Store B sell?",
     "fewer_than_sub", ["word problems", "comparison", "subtraction"]),
    ("Maria earns ₱{a} per month. Juan earns ₱{diff} less than Maria. How much does Juan earn?",
     "less_than_peso", ["word problems", "comparison", "subtraction", "payroll"]),
    ("A factory produced {a} units last month. This month it produced {mult} times as many. How many units were produced this month?",
     "times_as_many", ["word problems", "comparison", "multiplication"]),
    ("Maria has {total} books. She has {mult} times as many books as Juan. How many books does Juan have?",
     "times_divide", ["word problems", "comparison", "division"]),
    ("Office A processed {a} applications. Office B processed {diff} more than Office A. How many did both offices process in total?",
     "more_than_total", ["word problems", "comparison", "addition", "multi-step"]),
]

for i in range(30):
    idx = i % len(medium_comparison)
    template, op_type, tags = medium_comparison[idx]

    if op_type == "more_than_add":
        a = random.randint(80, 400)
        diff = random.randint(15, 100)
        correct = a + diff
        q_text = template.format(a=fmt(a), diff=fmt(diff))
        choices, ans = make_choices_int(correct)
        expl = f"Department B = Department A + {fmt(diff)} = {fmt(a)} + {fmt(diff)} = {fmt(correct)}."

    elif op_type == "fewer_than_sub":
        a = random.randint(100, 500)
        diff = random.randint(20, a // 2)
        correct = a - diff
        q_text = template.format(a=fmt(a), diff=fmt(diff))
        choices, ans = make_choices_int(correct)
        expl = f"Store B = Store A - {fmt(diff)} = {fmt(a)} - {fmt(diff)} = {fmt(correct)}."

    elif op_type == "less_than_peso":
        a = random.randint(20, 60) * 1000
        diff = random.randint(2, 10) * 1000
        correct = a - diff
        q_text = template.format(a=fmt(a), diff=fmt(diff))
        choices, ans = make_choices_peso(correct)
        expl = f"Juan's salary = Maria's - {peso(diff)} = {peso(a)} - {peso(diff)} = {peso(correct)}."

    elif op_type == "times_as_many":
        a = random.randint(100, 500)
        mult = random.choice([2, 3, 4, 5])
        correct = a * mult
        q_text = template.format(a=fmt(a), mult=mult)
        choices, ans = make_choices_int(correct)
        expl = f"This month = {mult} × {fmt(a)} = {fmt(correct)}."

    elif op_type == "times_divide":
        mult = random.choice([2, 3, 4, 5, 6])
        juan = random.randint(10, 50)
        total = juan * mult
        correct = juan
        q_text = template.format(total=fmt(total), mult=mult)
        choices, ans = make_choices_int(correct)
        expl = f"Juan's books = Maria's ÷ {mult} = {fmt(total)} ÷ {mult} = {fmt(correct)}."

    elif op_type == "more_than_total":
        a = random.randint(100, 400)
        diff = random.randint(20, 100)
        b = a + diff
        correct = a + b
        q_text = template.format(a=fmt(a), diff=fmt(diff))
        choices, ans = make_choices_int(correct)
        expl = f"Office B = {fmt(a)} + {fmt(diff)} = {fmt(b)}. Total = {fmt(a)} + {fmt(b)} = {fmt(correct)}."

    add_q("Medium", q_text, choices, ans, expl, tags)


# --- Medium: Average/mean problems (341-365) ---
medium_average = []
for i in range(25):
    count = random.choice([4, 5, 6])
    values = [random.randint(60, 98) for _ in range(count)]
    total = sum(values)
    # Ensure clean division
    remainder = total % count
    values[-1] += (count - remainder) if remainder != 0 else 0
    total = sum(values)
    correct = total // count
    values_str = ", ".join(str(v) for v in values)

    contexts = [
        f"A student's scores in {count} exams are: {values_str}. What is the average score?",
        f"The daily temperatures (°C) for {count} days were: {values_str}. What is the average temperature?",
        f"A clerk processed the following number of documents over {count} days: {values_str}. What is the daily average?",
        f"The enrollment in {count} sections is: {values_str}. What is the average enrollment per section?",
        f"A salesperson's weekly sales (in units) for {count} weeks were: {values_str}. What is the average weekly sales?",
    ]
    q_text = contexts[i % len(contexts)]
    choices, ans = make_choices_int(correct)
    expl = f"Sum = {fmt(total)}. Average = {fmt(total)} ÷ {count} = {fmt(correct)}."
    add_q("Medium", q_text, choices, ans, expl,
          ["word problems", "average", "division", "multi-step"])

# --- Medium: Practical government scenarios (366-400) ---
medium_govt = [
    ("A government agency has 3 divisions with 45, 38, and 52 employees. If each employee receives a ₱5,000 bonus, what is the total bonus expense?",
     (45 + 38 + 52) * 5000, "Total employees: 45 + 38 + 52 = 135. Total bonus: 135 × ₱5,000 = ₱675,000.",
     ["word problems", "multi-step", "payroll", "government"]),
    ("A municipality collected ₱2,450,000 in taxes. If 60% goes to the general fund, how much is allocated to the general fund?",
     int(2450000 * 0.60), "General fund: 60% of ₱2,450,000 = 0.60 × 2,450,000 = ₱1,470,000.",
     ["word problems", "percentage", "budgeting", "government"]),
    ("A public school has 1,200 students. If the student-to-teacher ratio is 40:1, how many teachers are needed?",
     1200 // 40, "Teachers needed: 1,200 ÷ 40 = 30 teachers.",
     ["word problems", "division", "ratio", "education"]),
    ("A government hospital has 250 beds. If the occupancy rate is 85%, how many beds are occupied?",
     int(250 * 0.85), "Occupied beds: 85% of 250 = 0.85 × 250 = 212 (rounded).",
     ["word problems", "percentage", "healthcare"]),
    ("A road project costs ₱45,000 per meter. If the road is 2.5 km long, what is the total project cost?",
     45000 * 2500, "Length in meters: 2.5 km = 2,500 m. Cost: 2,500 × ₱45,000 = ₱112,500,000.",
     ["word problems", "multiplication", "engineering", "unit conversion"]),
    ("A government office uses 15 reams of paper per week. How many reams are needed for 52 weeks?",
     15 * 52, "Annual usage: 15 × 52 = 780 reams.",
     ["word problems", "multiplication", "procurement"]),
    ("A fire truck carries 4,500 liters of water. If it uses 750 liters per deployment, how many deployments can it handle on one tank?",
     4500 // 750, "Deployments: 4,500 ÷ 750 = 6 deployments.",
     ["word problems", "division", "emergency services"]),
    ("A census team must survey 8,400 households. If there are 28 enumerators working equally, how many households per enumerator?",
     8400 // 28, "Households per enumerator: 8,400 ÷ 28 = 300.",
     ["word problems", "division", "census"]),
    ("A government vehicle fleet has 12 cars. Each car travels an average of 150 km/day. If fuel costs ₱58 per liter and efficiency is 10 km/L, what is the daily fleet fuel cost?",
     12 * 150 // 10 * 58, "Total km: 12 × 150 = 1,800. Liters: 1,800 ÷ 10 = 180. Cost: 180 × ₱58 = ₱10,440.",
     ["word problems", "multi-step", "transportation", "government"]),
    ("A public market has 180 stalls. If monthly rent is ₱3,500 per stall, what is the total monthly rental income?",
     180 * 3500, "Total rent: 180 × ₱3,500 = ₱630,000.",
     ["word problems", "multiplication", "revenue"]),
    ("A barangay received 2,400 sacks of rice for distribution. If each family gets 3 sacks, how many families can be served?",
     2400 // 3, "Families: 2,400 ÷ 3 = 800 families.",
     ["word problems", "division", "distribution"]),
    ("A government training program costs ₱2,500 per participant. If 85 employees attend, what is the total training cost?",
     2500 * 85, "Total cost: ₱2,500 × 85 = ₱212,500.",
     ["word problems", "multiplication", "training"]),
    ("A provincial road is 84 km long. If a maintenance crew covers 3.5 km per day, how many days to complete maintenance?",
     84 * 10 // 35, "Days: 84 ÷ 3.5 = 24 days.",
     ["word problems", "division", "decimals", "engineering"]),
    ("A government building's monthly electricity bill averages ₱187,500. What is the annual electricity expense?",
     187500 * 12, "Annual: ₱187,500 × 12 = ₱2,250,000.",
     ["word problems", "multiplication", "utilities"]),
    ("A city has 45 public schools. If the average enrollment is 1,250 students per school, what is the total student population?",
     45 * 1250, "Total students: 45 × 1,250 = 56,250.",
     ["word problems", "multiplication", "education"]),
    ("A government agency processed 15,600 applications in a year. What is the monthly average?",
     15600 // 12, "Monthly average: 15,600 ÷ 12 = 1,300 applications.",
     ["word problems", "division", "average"]),
    ("A public library acquired 840 new books to be distributed equally among 12 branches. How many books per branch?",
     840 // 12, "Books per branch: 840 ÷ 12 = 70.",
     ["word problems", "division", "distribution"]),
    ("A government employee's annual leave is 15 days. If she has used 9 days, how many leave days remain?",
     15 - 9, "Remaining leave: 15 - 9 = 6 days.",
     ["word problems", "subtraction", "leave management"]),
    ("A disaster relief operation needs 500 tents. If each tent costs ₱8,500, what is the total cost?",
     500 * 8500, "Total: 500 × ₱8,500 = ₱4,250,000.",
     ["word problems", "multiplication", "disaster relief"]),
    ("A government payroll covers 2,400 employees at an average salary of ₱25,000. What is the total monthly payroll?",
     2400 * 25000, "Total payroll: 2,400 × ₱25,000 = ₱60,000,000.",
     ["word problems", "multiplication", "payroll"]),
    ("A water district serves 12,500 households. If average monthly consumption is 15 cubic meters per household at ₱25 per cubic meter, what is the total monthly revenue?",
     12500 * 15 * 25, "Total: 12,500 × 15 × ₱25 = ₱4,687,500.",
     ["word problems", "multi-step", "utilities"]),
    ("A government hospital administered 8,400 vaccines in 28 days. What is the daily average?",
     8400 // 28, "Daily average: 8,400 ÷ 28 = 300 vaccines.",
     ["word problems", "division", "healthcare"]),
    ("A fleet of 8 garbage trucks each collects 12 tons per day. What is the total daily collection?",
     8 * 12, "Total: 8 × 12 = 96 tons.",
     ["word problems", "multiplication", "sanitation"]),
    ("A government office has an annual budget of ₱3,600,000 for supplies. If ₱1,450,000 has been spent in the first half, how much remains for the second half?",
     3600000 - 1450000, "Remaining: ₱3,600,000 - ₱1,450,000 = ₱2,150,000.",
     ["word problems", "subtraction", "budgeting"]),
    ("A public transportation system has 45 buses. Each bus makes 8 trips daily carrying 55 passengers per trip. How many passengers are served daily?",
     45 * 8 * 55, "Total: 45 × 8 × 55 = 19,800 passengers.",
     ["word problems", "multi-step", "transportation"]),
    ("A reforestation project plants 250 trees per hectare across 36 hectares. How many trees are planted?",
     250 * 36, "Total trees: 250 × 36 = 9,000.",
     ["word problems", "multiplication", "environment"]),
    ("A government canteen serves 450 employees daily. If each meal costs ₱75, what is the daily food expense?",
     450 * 75, "Daily expense: 450 × ₱75 = ₱33,750.",
     ["word problems", "multiplication", "food service"]),
    ("A provincial government has 18 municipalities. If the total IRA is ₱54,000,000 distributed equally, how much per municipality?",
     54000000 // 18, "Per municipality: ₱54,000,000 ÷ 18 = ₱3,000,000.",
     ["word problems", "division", "budgeting"]),
    ("A school building has 4 floors with 12 classrooms per floor. If each classroom has 45 chairs, what is the total number of chairs?",
     4 * 12 * 45, "Total: 4 × 12 × 45 = 2,160 chairs.",
     ["word problems", "multi-step", "inventory"]),
    ("A government printing office produces 2,500 copies per hour. How many copies can it produce in a 7.5-hour shift?",
     int(2500 * 7.5), "Total: 2,500 × 7.5 = 18,750 copies.",
     ["word problems", "multiplication", "decimals", "production"]),
    ("A city collected ₱8,750,000 in business permits. If there are 350 registered businesses paying equally, how much did each pay?",
     8750000 // 350, "Per business: ₱8,750,000 ÷ 350 = ₱25,000.",
     ["word problems", "division", "revenue"]),
    ("A government hospital has 180 nurses working in 3 shifts equally. How many nurses per shift?",
     180 // 3, "Per shift: 180 ÷ 3 = 60 nurses.",
     ["word problems", "division", "healthcare"]),
    ("A public works project requires 45,000 bags of cement at ₱280 per bag. What is the total cement cost?",
     45000 * 280, "Total: 45,000 × ₱280 = ₱12,600,000.",
     ["word problems", "multiplication", "engineering"]),
    ("A government agency's electricity consumption is 12,500 kWh per month at ₱9.50 per kWh. What is the monthly bill?",
     int(12500 * 9.50), "Monthly bill: 12,500 × ₱9.50 = ₱118,750.",
     ["word problems", "multiplication", "decimals", "utilities"]),
    ("A disaster response team distributed 7,200 food packs to 24 evacuation centers equally. How many packs per center?",
     7200 // 24, "Per center: 7,200 ÷ 24 = 300 packs.",
     ["word problems", "division", "disaster relief"]),
]

for q_text, correct, explanation, tags in medium_govt:
    if correct >= 10000 or "₱" in q_text:
        choices, ans = make_choices_peso(correct) if correct >= 10000 else make_choices_int(correct)
    else:
        choices, ans = make_choices_int(correct)
    add_q("Medium", q_text, choices, ans, explanation, tags)


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Three-step and complex multi-step problems (401-470) ---
hard_multi_step = [
    # Payroll with multiple components
    ("An employee earns ₱{base} basic pay, ₱{pera} PERA, and ₱{ot} overtime pay. Deductions are: tax ₱{tax}, SSS ₱{sss}, PhilHealth ₱{ph}, and Pag-IBIG ₱{pi}. What is the net pay?",
     "payroll_complex", ["word problems", "multi-step", "payroll", "government"]),
    # Multi-department budget
    ("A company has {d} departments. Department A has {a} employees at ₱{sa} each, Department B has {b} employees at ₱{sb} each. What is the total monthly payroll?",
     "dept_payroll", ["word problems", "multi-step", "payroll"]),
    # Inventory with receipts and distributions
    ("A warehouse starts with {start} items. It receives {recv} items and distributes {dist1} to Branch A and {dist2} to Branch B. How many items remain?",
     "inventory_flow", ["word problems", "multi-step", "inventory"]),
    # Revenue and profit
    ("A store's daily revenue is ₱{rev}. Daily expenses are: rent ₱{rent}, utilities ₱{util}, and salaries ₱{sal}. What is the daily profit?",
     "profit", ["word problems", "multi-step", "business"]),
    # Transportation with multiple legs
    ("A delivery truck travels {d1} km to the first stop, {d2} km to the second stop, and {d3} km back to base. If fuel efficiency is {eff} km/L and fuel costs ₱{fc}/L, what is the total fuel cost?",
     "transport_cost", ["word problems", "multi-step", "transportation"]),
    # Budget allocation with percentages
    ("A barangay budget of ₱{total} is allocated as follows: {p1}% for infrastructure, {p2}% for social services, and the rest for administration. How much is the administration budget?",
     "budget_remainder", ["word problems", "multi-step", "percentage", "budgeting"]),
    # Production with waste
    ("A factory produces {prod} units per day. If {waste}% are defective and discarded, how many good units are produced in {days} days?",
     "production_waste", ["word problems", "multi-step", "percentage", "production"]),
]

for i in range(70):
    idx = i % len(hard_multi_step)
    template, op_type, tags = hard_multi_step[idx]

    if op_type == "payroll_complex":
        base = random.randint(20, 45) * 1000
        pera = 2000
        ot = random.randint(2, 8) * 500
        tax = random.randint(2, 6) * 500
        sss = random.choice([900, 1125, 1200, 1350, 1500])
        ph = random.choice([350, 400, 450, 500, 550])
        pi = random.choice([100, 200, 300])
        gross = base + pera + ot
        deductions = tax + sss + ph + pi
        correct = gross - deductions
        q_text = template.format(base=fmt(base), pera=fmt(pera), ot=fmt(ot),
                                 tax=fmt(tax), sss=fmt(sss), ph=fmt(ph), pi=fmt(pi))
        choices, ans = make_choices_peso(correct)
        expl = f"Gross: {peso(base)} + {peso(pera)} + {peso(ot)} = {peso(gross)}. Deductions: {peso(tax)} + {peso(sss)} + {peso(ph)} + {peso(pi)} = {peso(deductions)}. Net: {peso(correct)}."

    elif op_type == "dept_payroll":
        a = random.randint(20, 60)
        b = random.randint(15, 50)
        sa = random.randint(18, 35) * 1000
        sb = random.randint(20, 40) * 1000
        payroll_a = a * sa
        payroll_b = b * sb
        correct = payroll_a + payroll_b
        q_text = template.format(d=2, a=a, sa=fmt(sa), b=b, sb=fmt(sb))
        choices, ans = make_choices_peso(correct)
        expl = f"Dept A: {a} × {peso(sa)} = {peso(payroll_a)}. Dept B: {b} × {peso(sb)} = {peso(payroll_b)}. Total: {peso(correct)}."

    elif op_type == "inventory_flow":
        start = random.randint(2000, 8000)
        recv = random.randint(500, 2000)
        dist1 = random.randint(300, start // 2)
        dist2 = random.randint(200, start // 3)
        correct = start + recv - dist1 - dist2
        q_text = template.format(start=fmt(start), recv=fmt(recv), dist1=fmt(dist1), dist2=fmt(dist2))
        choices, ans = make_choices_int(correct)
        expl = f"After receiving: {fmt(start)} + {fmt(recv)} = {fmt(start + recv)}. After distributing: {fmt(start + recv)} - {fmt(dist1)} - {fmt(dist2)} = {fmt(correct)}."

    elif op_type == "profit":
        rent = random.randint(5, 20) * 1000
        util = random.randint(2, 8) * 1000
        sal = random.randint(10, 30) * 1000
        expenses = rent + util + sal
        rev = expenses + random.randint(5, 25) * 1000
        correct = rev - expenses
        q_text = template.format(rev=fmt(rev), rent=fmt(rent), util=fmt(util), sal=fmt(sal))
        choices, ans = make_choices_peso(correct)
        expl = f"Total expenses: {peso(rent)} + {peso(util)} + {peso(sal)} = {peso(expenses)}. Profit: {peso(rev)} - {peso(expenses)} = {peso(correct)}."

    elif op_type == "transport_cost":
        d1 = random.randint(15, 60)
        d2 = random.randint(10, 45)
        d3 = random.randint(20, 70)
        eff = random.choice([8, 10, 12, 15])
        fc = random.choice([55, 58, 60, 62, 65, 68, 70, 72, 75])
        total_km = d1 + d2 + d3
        liters = total_km / eff
        correct = int(round(liters * fc))
        q_text = template.format(d1=d1, d2=d2, d3=d3, eff=eff, fc=fc)
        choices, ans = make_choices_peso(correct)
        expl = f"Total distance: {d1} + {d2} + {d3} = {total_km} km. Fuel: {total_km} ÷ {eff} = {liters:.1f} L. Cost: {liters:.1f} × {peso(fc)} = {peso(correct)}."

    elif op_type == "budget_remainder":
        total = random.randint(5, 20) * 100000
        p1 = random.choice([30, 35, 40, 45])
        p2 = random.choice([20, 25, 30])
        while p1 + p2 >= 90:
            p2 = random.choice([15, 20, 25])
        p_admin = 100 - p1 - p2
        correct = int(total * p_admin / 100)
        q_text = template.format(total=fmt(total), p1=p1, p2=p2)
        choices, ans = make_choices_peso(correct)
        expl = f"Administration: 100% - {p1}% - {p2}% = {p_admin}%. Amount: {p_admin}% of {peso(total)} = {peso(correct)}."

    elif op_type == "production_waste":
        prod = random.randint(200, 800)
        waste = random.choice([3, 4, 5, 6, 8, 10])
        days = random.randint(5, 20)
        good_per_day = int(prod * (100 - waste) / 100)
        correct = good_per_day * days
        q_text = template.format(prod=prod, waste=waste, days=days)
        choices, ans = make_choices_int(correct)
        expl = f"Good units/day: {prod} × {100-waste}% = {good_per_day}. Total in {days} days: {good_per_day} × {days} = {fmt(correct)}."

    add_q("Hard", q_text, choices, ans, expl, tags)


# --- Hard: Complex government/workplace scenarios (471-540) ---
hard_govt_scenarios = [
    ("A government agency has 5 divisions. Division A has 45 employees at ₱22,000/month, Division B has 38 at ₱25,000, Division C has 52 at ₱19,500, Division D has 30 at ₱28,000, and Division E has 25 at ₱32,000. What is the total monthly payroll?",
     45*22000 + 38*25000 + 52*19500 + 30*28000 + 25*32000,
     "A: 45×₱22,000=₱990,000. B: 38×₱25,000=₱950,000. C: 52×₱19,500=₱1,014,000. D: 30×₱28,000=₱840,000. E: 25×₱32,000=₱800,000. Total: ₱4,594,000.",
     ["word problems", "multi-step", "payroll", "government"]),
    ("A municipality's annual budget is ₱85,000,000. Personnel services take 45%, MOOE takes 30%, and capital outlay takes the rest. If the capital outlay is divided equally among 5 infrastructure projects, how much per project?",
     int(85000000 * 0.25 / 5),
     "Capital outlay: 100% - 45% - 30% = 25%. Amount: 25% of ₱85M = ₱21,250,000. Per project: ₱21,250,000 ÷ 5 = ₱4,250,000.",
     ["word problems", "multi-step", "percentage", "budgeting"]),
    ("A government hospital serves 450 patients daily. Each patient's average cost is ₱2,800. If the hospital operates 365 days a year and receives a government subsidy of ₱180,000,000 annually, how much additional revenue must it generate?",
     450 * 2800 * 365 - 180000000,
     "Annual cost: 450 × ₱2,800 × 365 = ₱459,900,000. Additional needed: ₱459,900,000 - ₱180,000,000 = ₱279,900,000.",
     ["word problems", "multi-step", "healthcare", "budgeting"]),
    ("A public school has 2,400 students. The school receives ₱1,500 per student from the government. If 35% goes to learning materials, 25% to maintenance, and the rest to other expenses, how much is allocated to other expenses?",
     int(2400 * 1500 * 0.40),
     "Total fund: 2,400 × ₱1,500 = ₱3,600,000. Other expenses: 100% - 35% - 25% = 40%. Amount: 40% of ₱3,600,000 = ₱1,440,000.",
     ["word problems", "multi-step", "percentage", "education"]),
    ("A construction project requires 12,500 bags of cement at ₱285 per bag, 450 cubic meters of gravel at ₱1,800 per cubic meter, and 280 cubic meters of sand at ₱1,200 per cubic meter. What is the total material cost?",
     12500*285 + 450*1800 + 280*1200,
     "Cement: 12,500 × ₱285 = ₱3,562,500. Gravel: 450 × ₱1,800 = ₱810,000. Sand: 280 × ₱1,200 = ₱336,000. Total: ₱4,708,500.",
     ["word problems", "multi-step", "engineering", "procurement"]),
    ("A government fleet has 15 vehicles. Each travels an average of 120 km/day with fuel efficiency of 8 km/L. If diesel costs ₱62.50/L, what is the monthly fuel expense (22 working days)?",
     int(15 * 120 / 8 * 62.50 * 22),
     "Daily fuel per vehicle: 120 ÷ 8 = 15 L. Fleet daily: 15 × 15 = 225 L. Daily cost: 225 × ₱62.50 = ₱14,062.50. Monthly: ₱14,062.50 × 22 = ₱309,375.",
     ["word problems", "multi-step", "transportation", "government"]),
    ("A disaster relief operation distributes rice, canned goods, and water. Each family pack contains 10 kg rice at ₱48/kg, 8 cans at ₱45 each, and 12 bottles of water at ₱15 each. If 2,500 family packs are prepared, what is the total cost?",
     (10*48 + 8*45 + 12*15) * 2500,
     "Per pack: rice ₱480 + cans ₱360 + water ₱180 = ₱1,020. Total: ₱1,020 × 2,500 = ₱2,550,000.",
     ["word problems", "multi-step", "disaster relief", "procurement"]),
    ("A government training center conducts 4 batches of training per month. Each batch has 35 participants. The cost per participant is ₱3,500 for materials and ₱1,200 for meals. What is the annual training expense?",
     4 * 35 * (3500 + 1200) * 12,
     "Per batch: 35 × (₱3,500 + ₱1,200) = 35 × ₱4,700 = ₱164,500. Monthly: 4 × ₱164,500 = ₱658,000. Annual: ₱658,000 × 12 = ₱7,896,000.",
     ["word problems", "multi-step", "training", "government"]),
    ("A city's water district charges ₱15.50 for the first 10 cubic meters and ₱22.75 for each additional cubic meter. If a government building uses 85 cubic meters, what is the water bill?",
     int(15.50 * 10 + 22.75 * 75),
     "First 10 m³: 10 × ₱15.50 = ₱155. Additional 75 m³: 75 × ₱22.75 = ₱1,706.25. Total: ₱155 + ₱1,706.25 = ₱1,861.25. Rounded: ₱1,861.",
     ["word problems", "multi-step", "utilities", "tiered pricing"]),
    ("A provincial government allocates ₱120,000,000 for road projects. If 40% goes to national roads (3 projects equally) and 60% to municipal roads (12 projects equally), how much does each municipal road project receive?",
     int(120000000 * 0.60 / 12),
     "Municipal allocation: 60% of ₱120M = ₱72,000,000. Per project: ₱72,000,000 ÷ 12 = ₱6,000,000.",
     ["word problems", "multi-step", "percentage", "budgeting"]),
    ("A government cafeteria serves breakfast (₱55/meal, 200 employees), lunch (₱85/meal, 350 employees), and snacks (₱35/meal, 150 employees) daily. What is the daily food service revenue?",
     55*200 + 85*350 + 35*150,
     "Breakfast: 200 × ₱55 = ₱11,000. Lunch: 350 × ₱85 = ₱29,750. Snacks: 150 × ₱35 = ₱5,250. Total: ₱46,000.",
     ["word problems", "multi-step", "food service"]),
    ("A government printing office prints 3 types of forms: Form A (5,000 copies at ₱3.50 each), Form B (8,000 copies at ₱2.75 each), and Form C (12,000 copies at ₱4.25 each). What is the total printing cost?",
     int(5000*3.50 + 8000*2.75 + 12000*4.25),
     "Form A: 5,000 × ₱3.50 = ₱17,500. Form B: 8,000 × ₱2.75 = ₱22,000. Form C: 12,000 × ₱4.25 = ₱51,000. Total: ₱90,500.",
     ["word problems", "multi-step", "procurement", "decimals"]),
    ("A census operation covers 15 municipalities. Each municipality has an average of 20 barangays with 500 households each. If each enumerator can survey 25 households per day and the census must be completed in 10 days, how many enumerators are needed?",
     15 * 20 * 500 // (25 * 10),
     "Total households: 15 × 20 × 500 = 150,000. Households per enumerator: 25 × 10 = 250. Enumerators: 150,000 ÷ 250 = 600.",
     ["word problems", "multi-step", "census", "planning"]),
    ("A government employee earns ₱32,000/month. She saves 15% of her salary. After 8 months of saving, she withdraws ₱12,000 for an emergency. How much savings remain?",
     int(32000 * 0.15 * 8 - 12000),
     "Monthly savings: 15% of ₱32,000 = ₱4,800. After 8 months: ₱4,800 × 8 = ₱38,400. After withdrawal: ₱38,400 - ₱12,000 = ₱26,400.",
     ["word problems", "multi-step", "savings", "percentage"]),
    ("A public market has 3 sections: dry goods (120 stalls at ₱4,500/month), wet market (85 stalls at ₱5,200/month), and food court (45 stalls at ₱6,800/month). What is the total monthly rental income?",
     120*4500 + 85*5200 + 45*6800,
     "Dry goods: 120 × ₱4,500 = ₱540,000. Wet market: 85 × ₱5,200 = ₱442,000. Food court: 45 × ₱6,800 = ₱306,000. Total: ₱1,288,000.",
     ["word problems", "multi-step", "revenue", "government"]),
]

for q_text, correct, explanation, tags in hard_govt_scenarios[:15]:
    choices, ans = make_choices_peso(correct)
    add_q("Hard", q_text, choices, ans, explanation, tags)


# --- Hard: More complex scenarios (continued 486-540) ---
hard_govt_scenarios_2 = [
    ("A government agency rents 3 floors of a building. Floor 1 has 2,500 sq ft at ₱350/sq ft/month, Floor 2 has 1,800 sq ft at ₱320/sq ft/month, and Floor 3 has 1,200 sq ft at ₱280/sq ft/month. What is the total monthly rent?",
     2500*350 + 1800*320 + 1200*280,
     "Floor 1: 2,500 × ₱350 = ₱875,000. Floor 2: 1,800 × ₱320 = ₱576,000. Floor 3: 1,200 × ₱280 = ₱336,000. Total: ₱1,787,000.",
     ["word problems", "multi-step", "real estate", "government"]),
    ("A school feeding program serves 1,500 students daily for 200 school days. Each meal costs ₱35. If the government subsidizes 70% and the school covers the rest, how much does the school pay annually?",
     int(1500 * 200 * 35 * 0.30),
     "Total cost: 1,500 × 200 × ₱35 = ₱10,500,000. School's share: 30% of ₱10,500,000 = ₱3,150,000.",
     ["word problems", "multi-step", "percentage", "education"]),
    ("A government hospital has 300 beds. Average occupancy is 80%. Each occupied bed costs ₱3,500/day to maintain. What is the monthly maintenance cost (30 days)?",
     int(300 * 0.80 * 3500 * 30),
     "Occupied beds: 80% of 300 = 240. Daily cost: 240 × ₱3,500 = ₱840,000. Monthly: ₱840,000 × 30 = ₱25,200,000.",
     ["word problems", "multi-step", "percentage", "healthcare"]),
    ("A city bus system has 60 buses. Each bus makes 12 trips/day carrying an average of 48 passengers at ₱15 per fare. What is the daily revenue?",
     60 * 12 * 48 * 15,
     "Daily passengers: 60 × 12 × 48 = 34,560. Revenue: 34,560 × ₱15 = ₱518,400.",
     ["word problems", "multi-step", "transportation", "revenue"]),
    ("A government employee's annual salary is ₱420,000. She receives a 13th month pay (1 month salary) and a ₱5,000 cash gift. If her annual tax is ₱45,600, what is her total annual take-home pay?",
     420000 + 420000 // 12 + 5000 - 45600,
     "Monthly salary: ₱420,000 ÷ 12 = ₱35,000. 13th month: ₱35,000. Total gross: ₱420,000 + ₱35,000 + ₱5,000 = ₱460,000. Take-home: ₱460,000 - ₱45,600 = ₱414,400.",
     ["word problems", "multi-step", "payroll", "tax"]),
    ("A provincial road project paves 2.5 km per week. The total road length is 45 km. If the project costs ₱8,500,000 per km, what is the total project cost and how many weeks will it take?",
     int(45 * 8500000),
     "Total cost: 45 × ₱8,500,000 = ₱382,500,000. Weeks: 45 ÷ 2.5 = 18 weeks. (Question asks for total cost.)",
     ["word problems", "multi-step", "engineering", "budgeting"]),
    ("A government warehouse stores 3 types of supplies: Type A (4,500 units at ₱125 each), Type B (2,800 units at ₱340 each), and Type C (1,200 units at ₱890 each). What is the total inventory value?",
     4500*125 + 2800*340 + 1200*890,
     "Type A: 4,500 × ₱125 = ₱562,500. Type B: 2,800 × ₱340 = ₱952,000. Type C: 1,200 × ₱890 = ₱1,068,000. Total: ₱2,582,500.",
     ["word problems", "multi-step", "inventory", "valuation"]),
    ("A city collects garbage from 45,000 households. Each household generates 2.5 kg/day. If disposal costs ₱3.20/kg, what is the monthly disposal cost (30 days)?",
     int(45000 * 2.5 * 3.20 * 30),
     "Daily waste: 45,000 × 2.5 = 112,500 kg. Daily cost: 112,500 × ₱3.20 = ₱360,000. Monthly: ₱360,000 × 30 = ₱10,800,000.",
     ["word problems", "multi-step", "sanitation", "decimals"]),
    ("A government IT department maintains 850 computers. Annual maintenance costs ₱4,500 per unit. If 12% of computers need replacement at ₱35,000 each, what is the total annual IT expense?",
     850*4500 + int(850*0.12)*35000,
     "Maintenance: 850 × ₱4,500 = ₱3,825,000. Replacements: 12% of 850 = 102 units. Replacement cost: 102 × ₱35,000 = ₱3,570,000. Total: ₱7,395,000.",
     ["word problems", "multi-step", "IT", "percentage"]),
    ("A public library system has 8 branches. Each branch has 15,000 books. If 5% of books are replaced annually at an average cost of ₱450 per book, what is the annual book replacement budget?",
     int(8 * 15000 * 0.05 * 450),
     "Total books: 8 × 15,000 = 120,000. Replaced: 5% of 120,000 = 6,000. Cost: 6,000 × ₱450 = ₱2,700,000.",
     ["word problems", "multi-step", "percentage", "library"]),
    ("A government agency sends 25 employees to a 5-day training in Manila. Costs per employee: airfare ₱8,500, hotel ₱3,200/night (4 nights), meals ₱1,500/day, and materials ₱2,000. What is the total training expense?",
     25 * (8500 + 3200*4 + 1500*5 + 2000),
     "Per employee: ₱8,500 + (4 × ₱3,200) + (5 × ₱1,500) + ₱2,000 = ₱8,500 + ₱12,800 + ₱7,500 + ₱2,000 = ₱30,800. Total: 25 × ₱30,800 = ₱770,000.",
     ["word problems", "multi-step", "training", "travel"]),
    ("A reforestation project covers 500 hectares. Each hectare requires 1,200 seedlings at ₱15 each, 50 kg of fertilizer at ₱28/kg, and 8 labor-days at ₱550/day. What is the total project cost?",
     500 * (1200*15 + 50*28 + 8*550),
     "Per hectare: seedlings ₱18,000 + fertilizer ₱1,400 + labor ₱4,400 = ₱23,800. Total: 500 × ₱23,800 = ₱11,900,000.",
     ["word problems", "multi-step", "environment", "agriculture"]),
    ("A government canteen buys supplies weekly: 200 kg rice at ₱52/kg, 80 kg meat at ₱320/kg, 50 kg vegetables at ₱85/kg, and 30 kg fish at ₱280/kg. What is the monthly supply cost (4 weeks)?",
     (200*52 + 80*320 + 50*85 + 30*280) * 4,
     "Weekly: rice ₱10,400 + meat ₱25,600 + vegetables ₱4,250 + fish ₱8,400 = ₱48,650. Monthly: ₱48,650 × 4 = ₱194,600.",
     ["word problems", "multi-step", "food service", "procurement"]),
    ("A telecommunications company installs fiber optic cable at 450 meters/day. The project is 12.6 km long. If the daily crew cost is ₱45,000 and materials cost ₱2,800/meter, what is the total project cost?",
     int(12600 / 450) * 45000 + 12600 * 2800,
     "Days needed: 12,600 ÷ 450 = 28 days. Labor: 28 × ₱45,000 = ₱1,260,000. Materials: 12,600 × ₱2,800 = ₱35,280,000. Total: ₱36,540,000.",
     ["word problems", "multi-step", "engineering", "telecommunications"]),
    ("A government payroll system processes salaries for 3 pay grades: Grade 1 (450 employees at ₱18,500), Grade 2 (280 employees at ₱24,000), and Grade 3 (120 employees at ₱35,000). If each employee also receives ₱2,000 PERA, what is the total monthly payroll?",
     450*18500 + 280*24000 + 120*35000 + (450+280+120)*2000,
     "Salaries: G1 ₱8,325,000 + G2 ₱6,720,000 + G3 ₱4,200,000 = ₱19,245,000. PERA: 850 × ₱2,000 = ₱1,700,000. Total: ₱20,945,000.",
     ["word problems", "multi-step", "payroll", "government"]),
    ("A city's annual tax collection target is ₱250,000,000. In Q1 they collected 22%, Q2 collected 28%, and Q3 collected 25%. How much must be collected in Q4 to meet the target?",
     int(250000000 * (1 - 0.22 - 0.28 - 0.25)),
     "Collected: 22% + 28% + 25% = 75%. Remaining: 25% of ₱250,000,000 = ₱62,500,000.",
     ["word problems", "multi-step", "percentage", "tax collection"]),
    ("A government hospital pharmacy stocks 3 medicines: Medicine A (2,000 vials at ₱185 each), Medicine B (1,500 vials at ₱420 each), and Medicine C (800 vials at ₱1,250 each). If 15% of stock expires and is discarded, what is the value of expired medicines?",
     int((2000*185 + 1500*420 + 800*1250) * 0.15),
     "Total stock value: ₱370,000 + ₱630,000 + ₱1,000,000 = ₱2,000,000. Expired: 15% of ₱2,000,000 = ₱300,000.",
     ["word problems", "multi-step", "percentage", "healthcare"]),
    ("A school district has 12 schools. Each school needs 45 computers at ₱28,000 each, 45 desks at ₱3,500 each, and 3 printers at ₱15,000 each. What is the total equipment budget?",
     12 * (45*28000 + 45*3500 + 3*15000),
     "Per school: computers ₱1,260,000 + desks ₱157,500 + printers ₱45,000 = ₱1,462,500. Total: 12 × ₱1,462,500 = ₱17,550,000.",
     ["word problems", "multi-step", "procurement", "education"]),
    ("A government vehicle pool has 20 cars (8 km/L), 10 vans (6 km/L), and 5 trucks (4 km/L). Each vehicle travels 100 km/day. If fuel costs ₱65/L, what is the daily fleet fuel cost?",
     int((20*100/8 + 10*100/6 + 5*100/4) * 65),
     "Cars: 20×100÷8=250L. Vans: 10×100÷6≈167L. Trucks: 5×100÷4=125L. Total: 542L. Cost: 542 × ₱65 = ₱35,230 (approx).",
     ["word problems", "multi-step", "transportation", "fleet management"]),
    ("A provincial sports complex has a swimming pool (50m × 25m × 2m). If water costs ₱45 per cubic meter and the pool is drained and refilled 4 times a year, what is the annual water cost?",
     50 * 25 * 2 * 45 * 4,
     "Pool volume: 50 × 25 × 2 = 2,500 m³. Per fill: 2,500 × ₱45 = ₱112,500. Annual: ₱112,500 × 4 = ₱450,000.",
     ["word problems", "multi-step", "volume", "utilities"]),
]

for q_text, correct, explanation, tags in hard_govt_scenarios_2[:20]:
    choices, ans = make_choices_peso(correct)
    add_q("Hard", q_text, choices, ans, explanation, tags)


# --- Hard: Tricky interpretation problems (541-580) ---
hard_tricky = [
    ("Maria has 3 times as many books as Juan. If Maria has 72 books, how many books does Juan have?",
     72 // 3, "Maria = 3 × Juan. So Juan = Maria ÷ 3 = 72 ÷ 3 = 24 books.",
     ["word problems", "comparison", "division", "tricky"]),
    ("A worker earns ₱750/day. He worked 22 days but was absent for 4 days without pay. What are his monthly earnings?",
     750 * (22 - 4), "Working days: 22 - 4 = 18. Earnings: 18 × ₱750 = ₱13,500.",
     ["word problems", "multi-step", "payroll", "tricky"]),
    ("A tank has 800 liters. On Monday 150 liters are used, on Tuesday 200 liters, and on Wednesday a refill of 100 liters is added. How many liters remain?",
     800 - 150 - 200 + 100, "After Mon: 800 - 150 = 650. After Tue: 650 - 200 = 450. After refill: 450 + 100 = 550 liters.",
     ["word problems", "multi-step", "inventory", "tricky"]),
    ("A store sells notebooks for ₱45 each. If a customer buys 5 notebooks and pays with a ₱500 bill, how much change does the customer receive?",
     500 - 5*45, "Cost: 5 × ₱45 = ₱225. Change: ₱500 - ₱225 = ₱275.",
     ["word problems", "multi-step", "money", "change"]),
    ("An office has 360 employees. If 2/3 are female, how many male employees are there?",
     360 - int(360 * 2/3), "Female: 2/3 of 360 = 240. Male: 360 - 240 = 120.",
     ["word problems", "fractions", "subtraction"]),
    ("A project is 5/8 complete. If the remaining work takes 15 more days, how many total days does the project take?",
     15 * 8 // 3, "Remaining: 1 - 5/8 = 3/8. If 3/8 = 15 days, then 1/8 = 5 days. Total: 8/8 = 40 days.",
     ["word problems", "fractions", "proportion", "tricky"]),
    ("A bus can carry 55 passengers. If 387 people need to be transported, how many trips are needed?",
     (387 + 54) // 55, "387 ÷ 55 = 7.036... Since you can't have a partial trip, 8 trips are needed.",
     ["word problems", "division", "rounding up", "tricky"]),
    ("An employee's salary increased by 10% to ₱33,000. What was the original salary?",
     33000 * 100 // 110, "New salary = 110% of original. Original = ₱33,000 ÷ 1.10 = ₱30,000.",
     ["word problems", "percentage", "reverse", "tricky"]),
    ("A store offers 'buy 3, get 1 free.' If each item costs ₱120, how much does a customer pay for 8 items?",
     6 * 120, "For every 4 items, pay for 3. 8 items = 2 groups of 4 = pay for 6. Cost: 6 × ₱120 = ₱720.",
     ["word problems", "multi-step", "discount", "tricky"]),
    ("A pipe fills a tank at 50 liters/minute. A drain empties it at 20 liters/minute. If both are open, how long to fill a 600-liter tank?",
     600 // (50 - 20), "Net fill rate: 50 - 20 = 30 L/min. Time: 600 ÷ 30 = 20 minutes.",
     ["word problems", "rate", "multi-step", "tricky"]),
    ("Two workers together can finish a job in 6 hours. Worker A alone takes 10 hours. How long does Worker B take alone?",
     15, "Combined rate: 1/6 job/hr. A's rate: 1/10. B's rate: 1/6 - 1/10 = 5/30 - 3/30 = 2/30 = 1/15. B takes 15 hours.",
     ["word problems", "rate", "work problem", "tricky"]),
    ("A car travels 60 km/h for 2 hours, then 80 km/h for 1.5 hours. What is the average speed for the entire trip?",
     int((60*2 + 80*1.5) / 3.5), "Total distance: 120 + 120 = 240 km. Total time: 3.5 hours. Average: 240 ÷ 3.5 ≈ 69 km/h.",
     ["word problems", "average speed", "multi-step"]),
    ("A rectangular lot is 3 times as long as it is wide. If the perimeter is 240 meters, what is the area?",
     30 * 90, "Let width = w. Length = 3w. Perimeter: 2(w + 3w) = 8w = 240. w = 30. Area: 30 × 90 = 2,700 sq m.",
     ["word problems", "geometry", "algebra"]),
    ("A merchant bought 100 items at ₱80 each. He sold 60 at ₱120 each and the rest at ₱65 each. What is the total profit or loss?",
     60*120 + 40*65 - 100*80, "Cost: 100 × ₱80 = ₱8,000. Revenue: (60 × ₱120) + (40 × ₱65) = ₱7,200 + ₱2,600 = ₱9,800. Profit: ₱9,800 - ₱8,000 = ₱1,800.",
     ["word problems", "multi-step", "profit/loss", "business"]),
    ("A government office has a monthly electricity budget of ₱85,000. In January they spent ₱92,000, February ₱78,000, and March ₱88,000. What is the total over/under budget for the quarter?",
     (92000 + 78000 + 88000) - 85000*3, "Budget: 3 × ₱85,000 = ₱255,000. Actual: ₱92,000 + ₱78,000 + ₱88,000 = ₱258,000. Over budget: ₱3,000.",
     ["word problems", "multi-step", "budgeting", "comparison"]),
    ("A school has 480 students. 3/8 joined the science club, 1/4 joined the math club, and the rest joined neither. How many students joined neither club?",
     480 - int(480*3/8) - int(480*1/4), "Science: 3/8 of 480 = 180. Math: 1/4 of 480 = 120. Neither: 480 - 180 - 120 = 180.",
     ["word problems", "fractions", "multi-step"]),
    ("A delivery service charges ₱100 for the first 3 km and ₱15 for each additional km. What is the charge for a 12-km delivery?",
     100 + (12-3)*15, "First 3 km: ₱100. Additional 9 km: 9 × ₱15 = ₱135. Total: ₱100 + ₱135 = ₱235.",
     ["word problems", "tiered pricing", "multi-step"]),
    ("A worker can paint 3 rooms per day. If there are 45 rooms to paint and the worker takes 2 days off per week, how many weeks to finish?",
     3, "Rooms per week: 3 × 5 = 15 (working 5 days). Weeks: 45 ÷ 15 = 3 weeks.",
     ["word problems", "rate", "multi-step", "scheduling"]),
    ("A company's profit was ₱450,000 in Q1, a loss of ₱120,000 in Q2, a profit of ₱380,000 in Q3, and a profit of ₱290,000 in Q4. What is the annual net profit?",
     450000 - 120000 + 380000 + 290000, "Net: ₱450,000 - ₱120,000 + ₱380,000 + ₱290,000 = ₱1,000,000.",
     ["word problems", "integers", "multi-step", "business"]),
    ("A government lot measures 120 m × 80 m. A building occupies 40 m × 30 m in the center. What is the area of the remaining open space?",
     120*80 - 40*30, "Lot area: 120 × 80 = 9,600 sq m. Building: 40 × 30 = 1,200 sq m. Open space: 9,600 - 1,200 = 8,400 sq m.",
     ["word problems", "geometry", "subtraction"]),
]

for q_text, correct, explanation, tags in hard_tricky:
    if correct >= 5000 and ("₱" in q_text or "peso" in explanation.lower() or "profit" in explanation.lower()):
        choices, ans = make_choices_peso(correct)
    else:
        choices, ans = make_choices_int(correct)
    add_q("Hard", q_text, choices, ans, explanation, tags)


# --- Hard: Generated multi-step with varied contexts (581-600) ---
hard_final = [
    ("A government agency rents 5 photocopiers at ₱8,500/month each. Each copier uses ₱3,200 worth of toner monthly. If the agency also pays ₱15,000/month for paper, what is the total monthly copying expense?",
     5*8500 + 5*3200 + 15000,
     "Rental: 5 × ₱8,500 = ₱42,500. Toner: 5 × ₱3,200 = ₱16,000. Paper: ₱15,000. Total: ₱73,500.",
     ["word problems", "multi-step", "office expenses"]),
    ("A city has 3 water treatment plants. Plant A processes 2,500 m³/day, Plant B processes 1,800 m³/day, and Plant C processes 3,200 m³/day. If the city needs 250,000 m³ per month (30 days), is the capacity sufficient? By how many m³/day is it over or under?",
     (2500 + 1800 + 3200) * 30 - 250000,
     "Daily capacity: 2,500 + 1,800 + 3,200 = 7,500 m³. Monthly: 7,500 × 30 = 225,000 m³. Shortfall: 250,000 - 225,000 = 25,000 m³ under. Daily shortfall: 25,000 ÷ 30 ≈ 833 m³/day.",
     ["word problems", "multi-step", "capacity planning"]),
    ("A government employee takes a taxi to work. The fare is ₱45 flag-down plus ₱13.50 per km. If the distance is 8 km and she takes a taxi both ways for 22 working days, what is the monthly taxi expense?",
     int((45 + 13.50*8) * 2 * 22),
     "One-way fare: ₱45 + (8 × ₱13.50) = ₱45 + ₱108 = ₱153. Daily: ₱153 × 2 = ₱306. Monthly: ₱306 × 22 = ₱6,732.",
     ["word problems", "multi-step", "transportation", "decimals"]),
    ("A printing company charges ₱5.50 per page for the first 1,000 pages, ₱4.25 for pages 1,001-5,000, and ₱3.00 for pages above 5,000. What is the cost of printing 8,000 pages?",
     int(1000*5.50 + 4000*4.25 + 3000*3.00),
     "First 1,000: 1,000 × ₱5.50 = ₱5,500. Next 4,000: 4,000 × ₱4.25 = ₱17,000. Last 3,000: 3,000 × ₱3.00 = ₱9,000. Total: ₱31,500.",
     ["word problems", "multi-step", "tiered pricing"]),
    ("A farmer harvests 3 crops per year. Crop 1 yields 2,400 kg sold at ₱45/kg, Crop 2 yields 1,800 kg at ₱62/kg, and Crop 3 yields 3,100 kg at ₱38/kg. If production costs are ₱180,000 per year, what is the annual profit?",
     2400*45 + 1800*62 + 3100*38 - 180000,
     "Revenue: ₱108,000 + ₱111,600 + ₱117,800 = ₱337,400. Profit: ₱337,400 - ₱180,000 = ₱157,400.",
     ["word problems", "multi-step", "agriculture", "profit"]),
    ("A government office building has 200 employees. Monthly expenses per employee: ₱150 for coffee, ₱85 for water, and ₱45 for tissue/soap. What is the annual pantry/hygiene budget?",
     200 * (150 + 85 + 45) * 12,
     "Monthly per employee: ₱150 + ₱85 + ₱45 = ₱280. Monthly total: 200 × ₱280 = ₱56,000. Annual: ₱56,000 × 12 = ₱672,000.",
     ["word problems", "multi-step", "office expenses"]),
    ("A school bus picks up students from 4 stops. Stop 1: 12 students, Stop 2: 15 students, Stop 3: 8 students board and 3 alight, Stop 4: 10 students board. How many students are on the bus after Stop 4?",
     12 + 15 + 8 - 3 + 10,
     "After Stop 1: 12. After Stop 2: 12 + 15 = 27. After Stop 3: 27 + 8 - 3 = 32. After Stop 4: 32 + 10 = 42.",
     ["word problems", "multi-step", "transportation", "sequential"]),
    ("A government project has 3 phases. Phase 1 costs ₱2,500,000 and takes 3 months. Phase 2 costs ₱4,200,000 and takes 5 months. Phase 3 costs ₱1,800,000 and takes 2 months. What is the average monthly cost across all phases?",
     (2500000 + 4200000 + 1800000) // (3 + 5 + 2),
     "Total cost: ₱2,500,000 + ₱4,200,000 + ₱1,800,000 = ₱8,500,000. Total months: 3 + 5 + 2 = 10. Average: ₱8,500,000 ÷ 10 = ₱850,000/month.",
     ["word problems", "multi-step", "average", "project management"]),
    ("A cooperative has 150 members. Each contributes ₱500/month. After 12 months, the cooperative earns ₱180,000 in interest. If the total (contributions + interest) is distributed equally, how much does each member receive?",
     (150*500*12 + 180000) // 150,
     "Total contributions: 150 × ₱500 × 12 = ₱900,000. With interest: ₱900,000 + ₱180,000 = ₱1,080,000. Per member: ₱1,080,000 ÷ 150 = ₱7,200.",
     ["word problems", "multi-step", "cooperative", "finance"]),
    ("A government hospital's emergency room sees an average of 85 patients/day. Each patient costs ₱1,250 in supplies. If the ER operates 365 days/year and the annual supply budget is ₱35,000,000, what is the budget surplus or deficit?",
     35000000 - 85*1250*365,
     "Annual cost: 85 × ₱1,250 × 365 = ₱38,828,125. Deficit: ₱35,000,000 - ₱38,828,125 = -₱3,828,125 (deficit of ₱3,828,125).",
     ["word problems", "multi-step", "healthcare", "budgeting"]),
    ("A city parking building has 5 floors with 80 slots each. Monthly rate is ₱3,500/slot. If average occupancy is 75%, what is the monthly parking revenue?",
     int(5 * 80 * 3500 * 0.75),
     "Total slots: 5 × 80 = 400. Occupied: 75% of 400 = 300. Revenue: 300 × ₱3,500 = ₱1,050,000.",
     ["word problems", "multi-step", "percentage", "revenue"]),
    ("A government employee earns ₱28,000/month. She allocates 30% for rent, 25% for food, 10% for transportation, 5% for utilities, and saves the rest. How much does she save monthly?",
     int(28000 * 0.30),
     "Allocated: 30% + 25% + 10% + 5% = 70%. Savings: 100% - 70% = 30%. Amount: 30% of ₱28,000 = ₱8,400.",
     ["word problems", "percentage", "budgeting", "personal finance"]),
    ("A construction crew of 12 workers can finish a road in 20 days. After 8 days, 4 workers leave. How many more days will the remaining workers need to finish?",
     18, "Total work: 12 × 20 = 240 worker-days. Done in 8 days: 12 × 8 = 96. Remaining: 240 - 96 = 144. With 8 workers: 144 ÷ 8 = 18 days.",
     ["word problems", "work problem", "multi-step", "tricky"]),
    ("A government vehicle depreciates by 15% per year. If it was purchased for ₱1,200,000, what is its value after 2 years?",
     int(1200000 * 0.85 * 0.85),
     "After year 1: ₱1,200,000 × 0.85 = ₱1,020,000. After year 2: ₱1,020,000 × 0.85 = ₱867,000.",
     ["word problems", "percentage", "depreciation", "multi-step"]),
    ("A school cafeteria sells 3 meal options: Option A (₱55, sold to 120 students), Option B (₱75, sold to 85 students), and Option C (₱95, sold to 45 students). If food cost is 60% of revenue, what is the daily profit?",
     int((120*55 + 85*75 + 45*95) * 0.40),
     "Revenue: (120×₱55) + (85×₱75) + (45×₱95) = ₱6,600 + ₱6,375 + ₱4,275 = ₱17,250. Profit: 40% of ₱17,250 = ₱6,900.",
     ["word problems", "multi-step", "percentage", "profit"]),
    ("A government agency has 3 shifts: morning (8 hours, 45 employees), afternoon (8 hours, 38 employees), and night (8 hours, 22 employees). If the hourly rate is ₱95 for day shifts and ₱120 for night shift, what is the daily labor cost?",
     (45 + 38) * 8 * 95 + 22 * 8 * 120,
     "Day shifts: (45 + 38) × 8 × ₱95 = 83 × 8 × ₱95 = ₱63,080. Night: 22 × 8 × ₱120 = ₱21,120. Total: ₱84,200.",
     ["word problems", "multi-step", "payroll", "shift differential"]),
    ("A provincial government distributes ₱50,000,000 to municipalities based on population. Municipality A (pop. 45,000), B (pop. 30,000), C (pop. 25,000). How much does Municipality A receive?",
     int(50000000 * 45000 / (45000 + 30000 + 25000)),
     "Total population: 45,000 + 30,000 + 25,000 = 100,000. A's share: 45,000/100,000 × ₱50,000,000 = ₱22,500,000.",
     ["word problems", "proportion", "distribution", "government"]),
    ("A factory operates 3 machines. Machine A produces 120 units/hour, B produces 95 units/hour, C produces 85 units/hour. If they run 8 hours/day for 25 days, what is the monthly output?",
     (120 + 95 + 85) * 8 * 25,
     "Hourly total: 120 + 95 + 85 = 300 units. Daily: 300 × 8 = 2,400. Monthly: 2,400 × 25 = 60,000 units.",
     ["word problems", "multi-step", "production"]),
    ("A government building uses 450 kWh/day. Electricity costs ₱9.50/kWh for the first 200 kWh and ₱12.00/kWh for excess. What is the daily electricity cost?",
     int(200*9.50 + 250*12.00),
     "First 200 kWh: 200 × ₱9.50 = ₱1,900. Excess 250 kWh: 250 × ₱12.00 = ₱3,000. Total: ₱4,900.",
     ["word problems", "tiered pricing", "utilities"]),
    ("A public works project employs 50 laborers at ₱550/day and 8 engineers at ₱2,200/day. If the project takes 45 days, what is the total labor cost?",
     (50*550 + 8*2200) * 45,
     "Daily cost: (50 × ₱550) + (8 × ₱2,200) = ₱27,500 + ₱17,600 = ₱45,100. Total: ₱45,100 × 45 = ₱2,029,500.",
     ["word problems", "multi-step", "engineering", "labor"]),
]

for q_text, correct, explanation, tags in hard_final:
    if correct >= 1000 and ("₱" in q_text or "cost" in q_text.lower() or "revenue" in q_text.lower() or "profit" in q_text.lower() or "budget" in q_text.lower() or "pay" in q_text.lower() or "expense" in q_text.lower()):
        choices, ans = make_choices_peso(correct)
    else:
        choices, ans = make_choices_int(correct)
    add_q("Hard", q_text, choices, ans, explanation, tags)


# --- Hard: Additional generated problems to reach 200 (fill remaining) ---
# Count current hard questions to determine how many more are needed
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
hard_additional_templates = [
    ("A government agency processes {apps} passport applications daily. Each application requires {pages} pages of documents printed at ₱{cost_per_page} per page. What is the daily printing cost for passport processing?",
     "print_cost", ["word problems", "multi-step", "government", "procurement"]),
    ("A provincial hospital has {beds} beds. If {occ}% are occupied and each occupied bed generates ₱{daily_rev} in revenue per day, what is the monthly revenue (30 days)?",
     "hospital_rev", ["word problems", "multi-step", "percentage", "healthcare"]),
    ("A government employee earns ₱{salary}/month. After {years} years of service, she receives a {pct}% salary increase. What is her new monthly salary?",
     "salary_increase", ["word problems", "percentage", "payroll"]),
    ("A city has {schools} public schools with an average of {students} students each. If the annual per-student allocation is ₱{alloc}, what is the total education budget?",
     "education_budget", ["word problems", "multi-step", "education", "budgeting"]),
    ("A delivery company has {trucks} trucks. Each truck delivers {packages} packages per day at ₱{rate} per package. If operating cost per truck is ₱{op_cost}/day, what is the daily net income?",
     "delivery_income", ["word problems", "multi-step", "business", "transportation"]),
    ("A government building has {floors} floors. Each floor has {rooms} offices using {kwh} kWh of electricity per day. At ₱{rate}/kWh, what is the monthly electricity bill (22 working days)?",
     "electricity", ["word problems", "multi-step", "utilities"]),
    ("A public market collects ₱{daily_fee} daily fee from each of its {stalls} stalls. If {pct}% of stalls are occupied on average, what is the monthly collection (30 days)?",
     "market_collection", ["word problems", "multi-step", "percentage", "revenue"]),
]

# Generate enough to fill to 200 hard questions
needed = 200 - hard_count
generated_extra = 0

while generated_extra < needed:
    idx = generated_extra % len(hard_additional_templates)
    template, op_type, tags = hard_additional_templates[idx]

    if op_type == "print_cost":
        apps = random.randint(80, 250)
        pages = random.randint(3, 8)
        cost_per_page = random.choice([3, 4, 5, 6])
        correct = apps * pages * cost_per_page
        q_text = template.format(apps=apps, pages=pages, cost_per_page=cost_per_page)
        choices, ans = make_choices_peso(correct)
        expl = f"Daily printing: {apps} × {pages} × ₱{cost_per_page} = {peso(correct)}."

    elif op_type == "hospital_rev":
        beds = random.choice([100, 150, 200, 250, 300])
        occ = random.choice([70, 75, 80, 85, 90])
        daily_rev = random.randint(2, 6) * 1000
        occupied = int(beds * occ / 100)
        correct = occupied * daily_rev * 30
        q_text = template.format(beds=beds, occ=occ, daily_rev=fmt(daily_rev))
        choices, ans = make_choices_peso(correct)
        expl = f"Occupied beds: {occ}% of {beds} = {occupied}. Monthly revenue: {occupied} × {peso(daily_rev)} × 30 = {peso(correct)}."

    elif op_type == "salary_increase":
        salary = random.randint(18, 45) * 1000
        years = random.randint(3, 10)
        pct = random.choice([5, 8, 10, 12, 15])
        increase = int(salary * pct / 100)
        correct = salary + increase
        q_text = template.format(salary=fmt(salary), years=years, pct=pct)
        choices, ans = make_choices_peso(correct)
        expl = f"Increase: {pct}% of {peso(salary)} = {peso(increase)}. New salary: {peso(salary)} + {peso(increase)} = {peso(correct)}."

    elif op_type == "education_budget":
        schools = random.randint(15, 50)
        students = random.randint(800, 1500)
        alloc = random.randint(10, 25) * 1000
        correct = schools * students * alloc
        q_text = template.format(schools=schools, students=fmt(students), alloc=fmt(alloc))
        choices, ans = make_choices_peso(correct)
        expl = f"Total students: {schools} × {fmt(students)} = {fmt(schools*students)}. Budget: {fmt(schools*students)} × {peso(alloc)} = {peso(correct)}."

    elif op_type == "delivery_income":
        trucks = random.randint(8, 25)
        packages = random.randint(30, 80)
        rate = random.randint(50, 150)
        # Ensure revenue > operating cost (realistic scenario)
        revenue_per_truck = packages * rate
        op_cost = random.randint(1, max(1, int(revenue_per_truck * 0.6) // 1000)) * 1000
        revenue = trucks * packages * rate
        total_op = trucks * op_cost
        correct = revenue - total_op
        if correct <= 0:
            op_cost = max(1000, int(revenue_per_truck * 0.3) // 1000 * 1000)
            total_op = trucks * op_cost
            correct = revenue - total_op
        q_text = template.format(trucks=trucks, packages=packages, rate=rate, op_cost=fmt(op_cost))
        choices, ans = make_choices_peso(correct)
        expl = f"Revenue: {trucks} × {packages} × {peso(rate)} = {peso(revenue)}. Operating cost: {trucks} × {peso(op_cost)} = {peso(total_op)}. Net: {peso(correct)}."

    elif op_type == "electricity":
        floors = random.randint(3, 8)
        rooms = random.randint(8, 20)
        kwh = random.randint(15, 40)
        rate_kwh = random.choice([9, 10, 11, 12])
        daily = floors * rooms * kwh * rate_kwh
        correct = daily * 22
        q_text = template.format(floors=floors, rooms=rooms, kwh=kwh, rate=rate_kwh)
        choices, ans = make_choices_peso(correct)
        expl = f"Daily usage: {floors} × {rooms} × {kwh} = {fmt(floors*rooms*kwh)} kWh. Daily cost: {fmt(floors*rooms*kwh)} × ₱{rate_kwh} = {peso(daily)}. Monthly: {peso(daily)} × 22 = {peso(correct)}."

    elif op_type == "market_collection":
        stalls = random.randint(100, 300)
        daily_fee = random.randint(50, 200)
        pct = random.choice([70, 75, 80, 85, 90])
        occupied = int(stalls * pct / 100)
        correct = occupied * daily_fee * 30
        q_text = template.format(daily_fee=daily_fee, stalls=stalls, pct=pct)
        choices, ans = make_choices_peso(correct)
        expl = f"Occupied stalls: {pct}% of {stalls} = {occupied}. Monthly: {occupied} × ₱{daily_fee} × 30 = {peso(correct)}."

    add_q("Hard", q_text, choices, ans, expl, tags)
    generated_extra += 1


# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count_final = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Generated: {len(questions)} total questions")
print(f"  Easy: {easy_count}")
print(f"  Medium: {medium_count}")
print(f"  Hard: {hard_count_final}")

# Warn if counts are off
if easy_count != 200:
    print(f"  WARNING: Expected 200 Easy, got {easy_count}")
if medium_count != 200:
    print(f"  WARNING: Expected 200 Medium, got {medium_count}")
if hard_count_final != 200:
    print(f"  WARNING: Expected 200 Hard, got {hard_count_final}")

# Write output
output_dir = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "numerical-ability" / "basic-operations" / "word-problems"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
