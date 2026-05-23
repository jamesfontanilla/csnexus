"""
Generate 600 division questions for the CSE Numerical Ability section.
200 Easy / 200 Medium / 200 Hard

Run: python scripts/gen_division_questions.py
Output: data/seed/questions/numerical-ability/basic-operations/division/questions.json
"""

import json
import random
from fractions import Fraction
from pathlib import Path

random.seed(43)

questions = []
qid = 0


def add_q(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Basic Operations",
        "subtopic": "Division",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags
    })


def fmt(n):
    """Format number with commas for thousands."""
    if isinstance(n, float):
        if n == int(n):
            return f"{int(n):,}"
        # Remove trailing zeros
        s = f"{n:,.10f}".rstrip('0').rstrip('.')
        return s
    return f"{n:,}"


def make_choices_int(correct, spread=None):
    """Generate 4 choices for an integer answer."""
    if spread is None:
        spread = max(3, abs(correct) // 8)
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        offset = random.choice([-3, -2, -1, 1, 2, 3]) * random.randint(1, max(1, spread))
        d = correct + offset
        if d != correct and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(correct + len(distractors) + 1)
    choices = [fmt(correct)] + [fmt(d) for d in distractors]
    random.shuffle(choices)
    return choices, fmt(correct)


def make_choices_decimal(correct, precision=2):
    """Generate 4 choices for a decimal answer."""
    distractors = set()
    attempts = 0
    correct_r = round(correct, precision)
    while len(distractors) < 3 and attempts < 100:
        if abs(correct_r) > 10:
            offset = random.choice([-3, -2, -1, 1, 2, 3])
        else:
            offset = random.choice([-0.5, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.5, 1, -1])
        d = round(correct_r + offset, precision)
        if d != correct_r and d not in distractors and d != 0:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(round(correct_r + (len(distractors) + 1) * 0.5, precision))
    fmt_c = fmt(correct_r)
    choices = [fmt_c] + [fmt(d) for d in distractors]
    random.shuffle(choices)
    return choices, fmt_c


def frac_str(f):
    """Convert Fraction to display string."""
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) > abs(f.denominator):
        whole = f.numerator // f.denominator
        rem = abs(f.numerator % f.denominator)
        if rem == 0:
            return str(whole)
        return f"{whole} {rem}/{f.denominator}"
    return f"{f.numerator}/{f.denominator}"


def make_choices_fraction(correct_frac):
    """Generate 4 choices for a fraction answer."""
    correct_str = frac_str(correct_frac)
    distractors = set()
    n, d = correct_frac.numerator, correct_frac.denominator
    candidates = [
        Fraction(n + 1, d), Fraction(abs(n - 1), d) if n > 1 else Fraction(n + 2, d),
        Fraction(n, d + 1), Fraction(n, max(1, d - 1)),
        Fraction(n + 1, d + 1), Fraction(n * 2, d),
        Fraction(n, d * 2), Fraction(n + 2, d),
        Fraction(d, n) if n != 0 else Fraction(1, d),
    ]
    for c in candidates:
        if c != correct_frac and c > 0 and len(distractors) < 3:
            distractors.add(frac_str(c))
        if len(distractors) >= 3:
            break
    while len(distractors) < 3:
        distractors.add(frac_str(Fraction(n + len(distractors) + 2, d + 1)))
    choices = [correct_str] + list(distractors)
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Basic whole number division (1-40) ---
easy_whole_pairs = [
    (56, 7), (72, 8), (63, 9), (48, 6), (81, 9),
    (45, 5), (36, 4), (54, 6), (42, 7), (64, 8),
    (96, 12), (84, 7), (108, 9), (120, 10), (144, 12),
    (75, 5), (132, 11), (90, 6), (78, 6), (91, 7),
    (156, 12), (168, 14), (180, 15), (192, 16), (204, 12),
    (216, 18), (225, 15), (240, 20), (252, 14), (270, 18),
    (288, 16), (300, 25), (315, 15), (336, 21), (350, 25),
    (360, 24), (378, 18), (396, 22), (420, 28), (450, 25),
]

for dividend, divisor in easy_whole_pairs:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Easy",
          f"What is {fmt(dividend)} ÷ {divisor}?",
          choices, ans,
          f"Divide {fmt(dividend)} by {divisor}: {fmt(dividend)} ÷ {divisor} = {fmt(quotient)}.",
          ["division", "whole numbers", "basic computation"])

# --- Easy: Division by 10, 100 (41-55) ---
div10_nums = [340, 560, 780, 1250, 2500, 470, 630, 890, 150, 920, 1450, 2080, 370, 640, 810]
for n in div10_nums:
    divisor = random.choice([10, 100]) if n >= 1000 else 10
    quotient = n / divisor
    if quotient == int(quotient):
        quotient = int(quotient)
        choices, ans = make_choices_int(quotient)
    else:
        choices, ans = make_choices_decimal(quotient)
    add_q("Easy",
          f"What is {fmt(n)} ÷ {divisor}?",
          choices, ans,
          f"Dividing by {divisor} moves the decimal point {'one' if divisor == 10 else 'two'} place(s) to the left: {fmt(n)} ÷ {divisor} = {fmt(quotient)}.",
          ["division", "whole numbers", "powers of 10"])

# --- Easy: Simple integer division (56-80) ---
easy_int_pairs = [
    (-36, 6), (-48, 8), (-72, 9), (-54, 6), (-45, 5),
    (-24, -3), (-56, -7), (-63, -9), (-40, -5), (-81, -9),
    (42, -6), (54, -9), (72, -8), (35, -7), (60, -12),
    (-84, 12), (-96, 8), (-108, 12), (-120, 15), (-150, 10),
    (-30, -6), (48, -4), (-64, 8), (-100, -25), (90, -15),
]

for dividend, divisor in easy_int_pairs:
    quotient = dividend // divisor
    sign_explain = "Same signs → positive" if (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0) else "Different signs → negative"
    choices, ans = make_choices_int(quotient)
    add_q("Easy",
          f"What is ({dividend}) ÷ ({divisor})?",
          choices, ans,
          f"{sign_explain}. |{abs(dividend)}| ÷ |{abs(divisor)}| = {abs(quotient)}. Answer: {quotient}.",
          ["division", "integers", "sign rules"])

# --- Easy: Simple decimal division (81-115) ---
easy_dec_pairs = [
    (4.8, 2), (7.2, 3), (9.6, 4), (12.5, 5), (14.4, 6),
    (16.8, 7), (19.2, 8), (22.5, 9), (3.6, 2), (8.4, 4),
    (6.3, 3), (15.6, 6), (24.5, 5), (27.2, 8), (18.9, 7),
    (4.5, 0.5), (7.2, 0.6), (8.4, 0.7), (9.6, 0.8), (3.6, 0.9),
    (12.0, 0.4), (15.0, 0.5), (2.4, 0.3), (6.4, 0.8), (10.5, 0.5),
    (0.48, 6), (0.72, 8), (0.36, 4), (0.81, 9), (0.56, 7),
    (2.5, 0.5), (4.8, 1.2), (7.5, 2.5), (9.0, 1.5), (6.0, 1.2),
]

for dividend, divisor in easy_dec_pairs:
    quotient = round(dividend / divisor, 4)
    if quotient == int(quotient):
        quotient = int(quotient)
        choices, ans = make_choices_int(quotient)
    else:
        choices, ans = make_choices_decimal(quotient)
    if isinstance(divisor, float) and divisor != int(divisor):
        expl = f"Move decimal to make divisor whole, then divide: {fmt(quotient)}."
    else:
        expl = f"Divide: {dividend} ÷ {divisor} = {fmt(quotient)}."
    add_q("Easy",
          f"What is {dividend} ÷ {divisor}?",
          choices, ans,
          expl,
          ["division", "decimals", "basic computation"])


# --- Easy: Simple fraction division (116-150) ---
easy_frac_pairs = [
    ((1, 2), (1, 4)), ((2, 3), (1, 3)), ((3, 4), (1, 2)),
    ((1, 3), (2, 3)), ((4, 5), (2, 5)), ((5, 6), (1, 6)),
    ((1, 2), (3, 4)), ((2, 5), (1, 5)), ((3, 8), (1, 8)),
    ((1, 4), (1, 2)), ((3, 5), (1, 5)), ((7, 8), (1, 4)),
    ((2, 3), (4, 9)), ((5, 6), (5, 12)), ((1, 3), (1, 6)),
    ((4, 7), (2, 7)), ((3, 4), (3, 8)), ((5, 9), (5, 18)),
    ((1, 2), (1, 6)), ((2, 3), (1, 9)), ((3, 5), (3, 10)),
    ((7, 10), (7, 20)), ((4, 9), (2, 9)), ((1, 4), (1, 8)),
    ((5, 8), (5, 16)), ((2, 7), (1, 7)), ((3, 10), (1, 10)),
    ((1, 5), (2, 5)), ((4, 5), (8, 15)), ((6, 7), (3, 7)),
    ((1, 3), (2, 9)), ((5, 6), (1, 3)), ((2, 5), (4, 15)),
    ((3, 4), (1, 4)), ((7, 9), (7, 18)),
]

for (n1, d1), (n2, d2) in easy_frac_pairs[:35]:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    result = f1 / f2
    choices, ans = make_choices_fraction(result)
    add_q("Easy",
          f"What is {n1}/{d1} ÷ {n2}/{d2}?",
          choices, ans,
          f"Apply KCF: {n1}/{d1} × {d2}/{n2} = {frac_str(result)}.",
          ["division", "fractions", "keep-change-flip"])

# --- Easy: Whole number ÷ fraction (151-165) ---
easy_whole_frac = [
    (2, (1, 4)), (3, (1, 2)), (4, (2, 3)), (5, (1, 5)),
    (6, (3, 4)), (8, (1, 2)), (10, (2, 5)), (3, (3, 8)),
    (4, (1, 3)), (6, (2, 3)), (9, (3, 4)), (7, (1, 7)),
    (12, (3, 4)), (5, (5, 6)), (8, (4, 5)),
]

for whole, (n, d) in easy_whole_frac:
    f_whole = Fraction(whole, 1)
    f_div = Fraction(n, d)
    result = f_whole / f_div
    choices, ans = make_choices_fraction(result) if result.denominator != 1 else make_choices_int(int(result))
    if result.denominator == 1:
        ans_str = str(int(result))
    else:
        ans_str = ans
    add_q("Easy",
          f"What is {whole} ÷ {n}/{d}?",
          choices, ans,
          f"{whole}/1 × {d}/{n} = {frac_str(result)}.",
          ["division", "fractions", "whole number by fraction"])

# --- Easy: Simple word problems (166-200) ---
easy_word_problems = [
    ("A box contains 144 pencils to be shared equally among 12 students. How many pencils does each student get?",
     144, 12, "pencils per student", ["division", "word problem", "sharing"]),
    ("An office has 96 folders distributed equally into 8 cabinets. How many folders per cabinet?",
     96, 8, "folders per cabinet", ["division", "word problem", "distribution"]),
    ("A teacher has 180 test papers to check over 5 days. How many papers per day?",
     180, 5, "papers per day", ["division", "word problem", "rate"]),
    ("A rope measuring 72 meters is cut into 9 equal pieces. How long is each piece?",
     72, 9, "meters", ["division", "word problem", "measurement"]),
    ("A government office received 240 reams of paper for 6 departments. How many reams per department?",
     240, 6, "reams per department", ["division", "word problem", "distribution"]),
    ("There are 350 chairs arranged in 14 rows. How many chairs per row?",
     350, 14, "chairs per row", ["division", "word problem", "arrangement"]),
    ("A total of 480 relief packs are distributed to 16 barangays. How many packs per barangay?",
     480, 16, "packs per barangay", ["division", "word problem", "distribution"]),
    ("An employee earns ₱36,000 per month. What is the daily rate for 24 working days?",
     36000, 24, "pesos per day", ["division", "word problem", "payroll"]),
    ("A school has 525 students divided into 15 sections. How many students per section?",
     525, 15, "students per section", ["division", "word problem", "grouping"]),
    ("A warehouse has 1,200 boxes stored in 25 shelves equally. How many boxes per shelf?",
     1200, 25, "boxes per shelf", ["division", "word problem", "storage"]),
    ("A bus can carry 45 passengers. If 360 people need transport, how many trips are needed?",
     360, 45, "trips", ["division", "word problem", "transportation"]),
    ("A farmer harvested 864 mangoes packed in crates of 24. How many crates are needed?",
     864, 24, "crates", ["division", "word problem", "packing"]),
    ("A budget of ₱15,000 is split equally among 5 projects. How much per project?",
     15000, 5, "pesos per project", ["division", "word problem", "budgeting"]),
    ("A printer produces 2,400 pages in 8 hours. How many pages per hour?",
     2400, 8, "pages per hour", ["division", "word problem", "rate"]),
    ("A road is 168 km long. If a crew paves 7 km per day, how many days to finish?",
     168, 7, "days", ["division", "word problem", "rate"]),
    ("A library has 756 books arranged equally on 9 shelves. How many books per shelf?",
     756, 9, "books per shelf", ["division", "word problem", "arrangement"]),
    ("An agency distributed 1,050 IDs to 15 offices. How many IDs per office?",
     1050, 15, "IDs per office", ["division", "word problem", "distribution"]),
    ("A tank holds 500 liters. If 25 liters are used per day, how many days will it last?",
     500, 25, "days", ["division", "word problem", "consumption"]),
    ("A company has 288 employees in 12 departments. How many employees per department?",
     288, 12, "employees per department", ["division", "word problem", "organization"]),
    ("A shipment of 1,680 items is packed into boxes of 40. How many boxes are needed?",
     1680, 40, "boxes", ["division", "word problem", "packing"]),
    ("A total of 450 seedlings are planted in rows of 18. How many rows?",
     450, 18, "rows", ["division", "word problem", "arrangement"]),
    ("An office uses 936 sheets of paper in 6 weeks. How many sheets per week?",
     936, 6, "sheets per week", ["division", "word problem", "consumption"]),
    ("A training has 270 participants seated at tables of 9. How many tables are needed?",
     270, 9, "tables", ["division", "word problem", "grouping"]),
    ("A municipality's annual budget of ₱84,000 is divided into 12 monthly allocations. How much per month?",
     84000, 12, "pesos per month", ["division", "word problem", "budgeting"]),
    ("A factory produces 2,520 units in 7 days. What is the daily output?",
     2520, 7, "units per day", ["division", "word problem", "production"]),
    ("A 195-page document is divided into 13 chapters of equal length. How many pages per chapter?",
     195, 13, "pages per chapter", ["division", "word problem", "organization"]),
    ("A water tank of 640 liters is shared among 8 households. How many liters each?",
     640, 8, "liters per household", ["division", "word problem", "sharing"]),
    ("A government vehicle travels 504 km on 7 full tanks. How many km per tank?",
     504, 7, "km per tank", ["division", "word problem", "fuel"]),
    ("A total of 1,125 voters are assigned to 9 precincts. How many voters per precinct?",
     1125, 9, "voters per precinct", ["division", "word problem", "assignment"]),
    ("An NGO distributes 3,600 meals over 12 days. How many meals per day?",
     3600, 12, "meals per day", ["division", "word problem", "distribution"]),
    ("A cable measuring 225 meters is cut into 15-meter segments. How many segments?",
     225, 15, "segments", ["division", "word problem", "measurement"]),
    ("A school cafeteria serves 1,440 students in 6 lunch periods. How many per period?",
     1440, 6, "students per period", ["division", "word problem", "scheduling"]),
    ("A donation of ₱48,000 is split among 16 families. How much per family?",
     48000, 16, "pesos per family", ["division", "word problem", "sharing"]),
    ("A parking lot has 378 spaces in 14 rows. How many spaces per row?",
     378, 14, "spaces per row", ["division", "word problem", "arrangement"]),
    ("A project requires 2,160 work-hours completed by 9 workers. How many hours per worker?",
     2160, 9, "hours per worker", ["division", "word problem", "labor"]),
]

for text, dividend, divisor, unit, tags in easy_word_problems:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Easy", text, choices, ans,
          f"{fmt(dividend)} ÷ {divisor} = {fmt(quotient)} {unit}.",
          tags)


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Multi-digit whole number division (201-235) ---
medium_whole_pairs = [
    (1296, 16), (2352, 28), (3456, 32), (4725, 45), (5184, 36),
    (6048, 48), (7344, 54), (8192, 64), (9216, 72), (10080, 63),
    (1575, 25), (2688, 42), (3780, 35), (4914, 27), (5832, 54),
    (6561, 81), (7056, 84), (8100, 75), (9450, 63), (10800, 45),
    (11232, 36), (12544, 56), (13500, 54), (14400, 64), (15625, 25),
    (16384, 128), (17280, 96), (18900, 75), (19600, 56), (20736, 72),
    (2145, 33), (3276, 39), (4368, 52), (5460, 65), (6552, 78),
]

for dividend, divisor in medium_whole_pairs:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Medium",
          f"What is {fmt(dividend)} ÷ {divisor}?",
          choices, ans,
          f"Using long division: {fmt(dividend)} ÷ {divisor} = {fmt(quotient)}. Verify: {fmt(quotient)} × {divisor} = {fmt(dividend)}.",
          ["division", "whole numbers", "long division"])

# --- Medium: Division with remainders (236-255) ---
medium_remainder_pairs = [
    (500, 7), (1000, 13), (2500, 17), (3000, 19), (750, 11),
    (1234, 23), (4567, 31), (8901, 43), (6789, 37), (2345, 29),
    (999, 16), (1500, 22), (3333, 47), (5555, 53), (7777, 61),
    (1111, 14), (2222, 33), (4444, 57), (6666, 71), (8888, 83),
]

for dividend, divisor in medium_remainder_pairs:
    quotient = dividend // divisor
    remainder = dividend % divisor
    choices, ans = make_choices_int(quotient)
    add_q("Medium",
          f"What is the quotient when {fmt(dividend)} is divided by {divisor}?",
          choices, ans,
          f"{fmt(dividend)} ÷ {divisor} = {quotient} remainder {remainder}. Verify: {quotient} × {divisor} + {remainder} = {fmt(dividend)}.",
          ["division", "whole numbers", "remainder"])

# --- Medium: Integer division with larger numbers (256-280) ---
medium_int_pairs = [
    (-144, 12), (-225, -15), (336, -14), (-468, 18), (-576, -24),
    (720, -16), (-864, 36), (-1024, -32), (1296, -27), (-1500, 25),
    (-1728, -48), (2025, -45), (-2304, 64), (-2700, -54), (3125, -25),
    (-3600, 72), (-4032, -56), (4500, -75), (-5040, 63), (-5625, -75),
    (-192, -16), (256, -8), (-324, 18), (441, -21), (-512, -64),
]

for dividend, divisor in medium_int_pairs:
    quotient = dividend // divisor
    # Python floor division for negatives differs from truncation; use int division
    quotient = int(dividend / divisor)
    sign_explain = "Same signs → positive" if (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0) else "Different signs → negative"
    choices, ans = make_choices_int(quotient)
    add_q("Medium",
          f"What is ({fmt(dividend)}) ÷ ({fmt(divisor)})?",
          choices, ans,
          f"{sign_explain}. |{fmt(abs(dividend))}| ÷ |{fmt(abs(divisor))}| = {fmt(abs(quotient))}. Answer: {fmt(quotient)}.",
          ["division", "integers", "sign rules"])

# --- Medium: Decimal division (281-320) ---
medium_dec_pairs = [
    (45.36, 4), (78.54, 6), (123.75, 5), (256.32, 8), (189.72, 9),
    (34.56, 1.2), (67.89, 2.3), (98.76, 3.4), (12.96, 0.36), (25.92, 0.72),
    (456.75, 32.5), (187.2, 7.8), (345.6, 14.4), (567.84, 23.66), (234.5, 6.7),
    (0.0525, 0.005), (0.1296, 0.012), (0.3456, 0.024), (0.756, 0.063), (0.918, 0.054),
    (15.75, 1.25), (28.35, 2.25), (47.25, 3.15), (63.75, 4.25), (84.5, 6.5),
    (3847.5, 5), (2835.0, 4.5), (1575.0, 12.5), (9450.0, 37.5), (6250.0, 25.0),
    (0.48, 0.06), (0.96, 0.12), (1.44, 0.18), (2.56, 0.32), (3.24, 0.36),
    (156.8, 3.2), (245.7, 4.5), (378.4, 5.6), (492.8, 6.4), (617.5, 9.5),
]

for dividend, divisor in medium_dec_pairs:
    quotient = round(dividend / divisor, 4)
    if quotient == int(quotient):
        quotient_i = int(quotient)
        choices, ans = make_choices_int(quotient_i)
    else:
        # Determine appropriate precision
        prec = 2 if abs(quotient) >= 1 else 4
        quotient = round(dividend / divisor, prec)
        choices, ans = make_choices_decimal(quotient, prec)
    add_q("Medium",
          f"What is {dividend} ÷ {divisor}?",
          choices, ans,
          f"Divide: {dividend} ÷ {divisor} = {fmt(quotient) if isinstance(quotient, int) else quotient}. Move decimal points as needed to make divisor whole.",
          ["division", "decimals", "decimal placement"])


# --- Medium: Fraction division (321-360) ---
medium_frac_pairs = [
    ((2, 3), (4, 7)), ((5, 6), (10, 3)), ((3, 7), (9, 14)),
    ((4, 5), (12, 25)), ((7, 8), (21, 16)), ((5, 12), (15, 8)),
    ((8, 9), (4, 3)), ((3, 10), (9, 20)), ((7, 12), (14, 9)),
    ((11, 15), (22, 45)), ((2, 9), (4, 27)), ((5, 8), (15, 32)),
    ((9, 14), (3, 7)), ((4, 11), (8, 33)), ((7, 15), (14, 45)),
    ((6, 7), (12, 35)), ((8, 11), (16, 33)), ((3, 13), (9, 26)),
    ((10, 21), (5, 7)), ((12, 25), (4, 15)), ((5, 9), (25, 36)),
    ((7, 10), (21, 40)), ((9, 16), (27, 32)), ((11, 18), (22, 27)),
    ((4, 15), (8, 45)), ((13, 20), (26, 15)), ((3, 14), (9, 28)),
    ((8, 15), (4, 5)), ((5, 11), (10, 33)), ((7, 16), (21, 32)),
]

for (n1, d1), (n2, d2) in medium_frac_pairs:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    result = f1 / f2
    choices, ans = make_choices_fraction(result)
    add_q("Medium",
          f"What is {n1}/{d1} ÷ {n2}/{d2}?",
          choices, ans,
          f"KCF: {n1}/{d1} × {d2}/{n2} = {frac_str(result)}.",
          ["division", "fractions", "keep-change-flip"])

# --- Medium: Mixed number division (361-385) ---
medium_mixed_pairs = [
    ((2, 1, 3), (1, 1, 2)), ((3, 1, 4), (1, 1, 8)), ((4, 2, 5), (1, 1, 10)),
    ((5, 1, 2), (2, 3, 4)), ((1, 3, 4), (7, 8, 1)), ((2, 2, 3), (1, 1, 3)),
    ((3, 3, 5), (1, 4, 5)), ((6, 1, 4), (2, 1, 2)), ((4, 1, 6), (1, 2, 3)),
    ((7, 1, 2), (3, 3, 4)), ((2, 5, 8), (1, 3, 16)), ((3, 1, 3), (2, 2, 9)),
    ((5, 2, 3), (1, 5, 6)), ((4, 3, 8), (1, 3, 4)), ((8, 1, 3), (2, 7, 9)),
    ((1, 1, 5), (3, 5, 1)), ((2, 3, 7), (1, 2, 7)), ((6, 2, 3), (3, 1, 3)),
    ((9, 1, 4), (3, 1, 8)), ((3, 5, 6), (1, 11, 12)), ((7, 2, 5), (2, 1, 5)),
    ((4, 5, 9), (2, 2, 9)), ((5, 3, 4), (2, 7, 8)), ((10, 1, 2), (3, 1, 2)),
    ((8, 3, 4), (2, 5, 8)),
]

for (w1, n1, d1), (w2, n2, d2) in medium_mixed_pairs:
    f1 = Fraction(w1 * d1 + n1, d1)
    f2 = Fraction(w2 * d2 + n2, d2)
    result = f1 / f2
    choices, ans = make_choices_fraction(result)
    add_q("Medium",
          f"What is {w1} {n1}/{d1} ÷ {w2} {n2}/{d2}?",
          choices, ans,
          f"Convert: {frac_str(f1)} ÷ {frac_str(f2)}. KCF: {frac_str(f1)} × {f2.denominator}/{f2.numerator} = {frac_str(result)}.",
          ["division", "fractions", "mixed numbers"])

# --- Medium: Word problems (386-400) ---
medium_word_problems = [
    ("A government agency's quarterly budget is ₱2,450,000 to be distributed equally among 35 field offices. How much does each office receive?",
     2450000, 35, "pesos", ["division", "word problem", "budgeting"]),
    ("A vehicle traveled 1,575 km on 75 liters of fuel. What is the fuel efficiency in km/L?",
     1575, 75, "km/L", ["division", "word problem", "fuel efficiency"]),
    ("A municipality has 47,520 registered voters in 132 precincts. How many voters per precinct?",
     47520, 132, "voters per precinct", ["division", "word problem", "assignment"]),
    ("A warehouse received 8,736 items to be packed in boxes of 48. How many boxes are needed?",
     8736, 48, "boxes", ["division", "word problem", "packing"]),
    ("An employee's annual salary is ₱456,000. What is the monthly salary?",
     456000, 12, "pesos per month", ["division", "word problem", "payroll"]),
    ("A construction project requires 15,120 bricks laid over 63 days. How many bricks per day?",
     15120, 63, "bricks per day", ["division", "word problem", "construction"]),
    ("A school's total enrollment of 2,856 students is divided into 42 sections. How many students per section?",
     2856, 42, "students per section", ["division", "word problem", "organization"]),
    ("A water district serves 9,450 households with 75 service trucks. How many households per truck?",
     9450, 75, "households per truck", ["division", "word problem", "service"]),
    ("A printing press produces 86,400 copies in 72 hours. What is the hourly output?",
     86400, 72, "copies per hour", ["division", "word problem", "production"]),
    ("A donation of ₱1,260,000 is distributed to 84 beneficiaries. How much per beneficiary?",
     1260000, 84, "pesos per beneficiary", ["division", "word problem", "distribution"]),
    ("A highway project covers 2,340 km divided into 65 segments. How many km per segment?",
     2340, 65, "km per segment", ["division", "word problem", "engineering"]),
    ("A government hospital administered 12,600 vaccines over 28 days. How many per day?",
     12600, 28, "vaccines per day", ["division", "word problem", "healthcare"]),
    ("A total of 5,832 exam booklets are distributed to 54 testing centers. How many per center?",
     5832, 54, "booklets per center", ["division", "word problem", "distribution"]),
    ("A city's annual garbage collection is 18,720 tons handled by 48 trucks. How many tons per truck?",
     18720, 48, "tons per truck", ["division", "word problem", "sanitation"]),
    ("A telecommunications company installed 7,344 meters of cable in 54 days. How many meters per day?",
     7344, 54, "meters per day", ["division", "word problem", "installation"]),
    ("A regional office processed 4,536 applications over 63 working days. How many applications per day?",
     4536, 63, "applications per day", ["division", "word problem", "processing"]),
    ("A fleet of 36 buses transported 16,200 passengers in one day. How many passengers per bus?",
     16200, 36, "passengers per bus", ["division", "word problem", "transportation"]),
    ("A government canteen served 11,340 meals in 42 days. How many meals per day?",
     11340, 42, "meals per day", ["division", "word problem", "food service"]),
    ("A public library acquired 6,825 new books distributed to 75 branches. How many books per branch?",
     6825, 75, "books per branch", ["division", "word problem", "distribution"]),
    ("A training center conducted 3,456 hours of instruction over 96 sessions. How many hours per session?",
     3456, 96, "hours per session", ["division", "word problem", "education"]),
    ("A provincial government allocated ₱3,780,000 for 84 infrastructure projects. How much per project?",
     3780000, 84, "pesos per project", ["division", "word problem", "budgeting"]),
    ("A census team surveyed 14,256 households across 66 enumerators. How many households per enumerator?",
     14256, 66, "households per enumerator", ["division", "word problem", "census"]),
    ("A power cooperative serves 8,928 connections maintained by 48 linemen. How many connections per lineman?",
     8928, 48, "connections per lineman", ["division", "word problem", "utilities"]),
    ("A document archive contains 25,200 files organized into 56 categories. How many files per category?",
     25200, 56, "files per category", ["division", "word problem", "organization"]),
    ("A reforestation project planted 19,440 trees across 72 hectares. How many trees per hectare?",
     19440, 72, "trees per hectare", ["division", "word problem", "environment"]),
]

for text, dividend, divisor, unit, tags in medium_word_problems:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Medium", text, choices, ans,
          f"{fmt(dividend)} ÷ {divisor} = {fmt(quotient)} {unit}.",
          tags)


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Large number division (401-430) ---
hard_whole_pairs = [
    (248832, 432), (314685, 567), (456750, 750), (518400, 864),
    (629748, 756), (746496, 864), (823543, 343), (912384, 576),
    (103680, 288), (207360, 576), (311040, 432), (414720, 648),
    (165888, 384), (276480, 512), (387072, 672), (497664, 768),
    (155520, 360), (233280, 540), (349920, 810), (466560, 720),
    (186624, 432), (279936, 648), (373248, 864), (559872, 768),
    (124416, 288), (186624, 324), (248832, 576), (373248, 432),
    (145152, 336), (217728, 504), (290304, 672), (362880, 504),
]

for dividend, divisor in hard_whole_pairs[:30]:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Hard",
          f"What is {fmt(dividend)} ÷ {fmt(divisor)}?",
          choices, ans,
          f"Long division: {fmt(dividend)} ÷ {fmt(divisor)} = {fmt(quotient)}. Verify: {fmt(quotient)} × {fmt(divisor)} = {fmt(dividend)}.",
          ["division", "whole numbers", "large numbers"])

# --- Hard: Complex integer division (431-455) ---
hard_int_pairs = [
    (-15625, -125), (27648, -192), (-34560, 240), (-46656, -324),
    (59049, -243), (-72900, 540), (-86400, -720), (103680, -864),
    (-116640, 972), (-131072, -512), (145800, -810), (-162000, 1080),
    (-186624, -1296), (207360, -1440), (-233280, 1620), (-259200, -1800),
    (291600, -2025), (-324000, 2250), (-362880, -2520), (405000, -2700),
    (-450000, 3125), (-518400, -3600), (583200, -4050), (-648000, 4500),
    (-729000, -4500),
]

for dividend, divisor in hard_int_pairs:
    quotient = int(dividend / divisor)
    sign_explain = "Same signs → positive" if (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0) else "Different signs → negative"
    choices, ans = make_choices_int(quotient)
    add_q("Hard",
          f"What is ({fmt(dividend)}) ÷ ({fmt(divisor)})?",
          choices, ans,
          f"{sign_explain}. |{fmt(abs(dividend))}| ÷ |{fmt(abs(divisor))}| = {fmt(abs(quotient))}. Answer: {fmt(quotient)}.",
          ["division", "integers", "large numbers"])

# --- Hard: Complex decimal division (456-490) ---
hard_dec_pairs = [
    (456.192, 3.84), (789.375, 6.25), (1234.56, 12.8),
    (2345.67, 34.5), (3456.78, 45.6), (4567.89, 56.7),
    (567.84, 0.048), (891.072, 0.096), (123.456, 0.0064),
    (0.27648, 0.0192), (0.38880, 0.0270), (0.46656, 0.0324),
    (98.765, 1.25), (76.544, 2.36), (54.321, 3.45),
    (1575.0, 0.125), (2835.0, 0.225), (4725.0, 0.375),
    (8437.5, 6.75), (6562.5, 8.75), (3281.25, 4.375),
    (15.876, 1.32), (27.648, 2.304), (39.204, 3.267),
    (187.5, 0.015), (375.0, 0.025), (562.5, 0.045),
    (0.6561, 0.081), (0.8192, 0.064), (1.2288, 0.096),
    (234.567, 7.89), (456.789, 12.34), (678.912, 23.45),
    (891.234, 34.56), (1023.456, 45.67),
]

for dividend, divisor in hard_dec_pairs:
    quotient = round(dividend / divisor, 4)
    if quotient == int(quotient):
        quotient_i = int(quotient)
        choices, ans = make_choices_int(quotient_i)
        add_q("Hard",
              f"What is {dividend} ÷ {divisor}?",
              choices, ans,
              f"Move decimal points to make divisor whole, then divide: {dividend} ÷ {divisor} = {fmt(quotient_i)}.",
              ["division", "decimals", "complex computation"])
    else:
        prec = 2 if abs(quotient) >= 1 else 4
        quotient_r = round(dividend / divisor, prec)
        choices, ans = make_choices_decimal(quotient_r, prec)
        add_q("Hard",
              f"What is {dividend} ÷ {divisor}?",
              choices, ans,
              f"Move decimal points to make divisor whole, then divide: {dividend} ÷ {divisor} ≈ {quotient_r}.",
              ["division", "decimals", "complex computation"])


# --- Hard: Complex fraction division (491-530) ---
hard_frac_pairs = [
    ((7, 12), (14, 15)), ((11, 18), (33, 54)), ((13, 20), (39, 50)),
    ((17, 24), (51, 32)), ((19, 30), (57, 40)), ((23, 36), (46, 45)),
    ((5, 14), (15, 49)), ((8, 21), (16, 63)), ((9, 22), (27, 44)),
    ((11, 24), (33, 40)), ((13, 28), (39, 56)), ((15, 32), (45, 64)),
    ((7, 18), (21, 54)), ((10, 27), (20, 81)), ((14, 33), (28, 99)),
    ((16, 35), (48, 105)), ((17, 40), (51, 80)), ((19, 42), (57, 84)),
    ((21, 44), (63, 88)), ((23, 48), (69, 96)), ((25, 54), (75, 108)),
    ((4, 13), (12, 39)), ((6, 17), (18, 51)), ((8, 19), (24, 57)),
    ((10, 23), (30, 69)), ((12, 29), (36, 87)), ((14, 31), (42, 93)),
    ((16, 37), (48, 111)), ((18, 41), (54, 123)), ((20, 43), (60, 129)),
    ((3, 11), (9, 44)), ((5, 13), (15, 52)), ((7, 17), (21, 68)),
    ((9, 19), (27, 76)), ((11, 23), (33, 92)), ((13, 29), (39, 116)),
    ((15, 31), (45, 124)), ((17, 37), (51, 148)), ((19, 41), (57, 164)),
    ((21, 43), (63, 172)),
]

for (n1, d1), (n2, d2) in hard_frac_pairs:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    result = f1 / f2
    choices, ans = make_choices_fraction(result)
    add_q("Hard",
          f"What is {n1}/{d1} ÷ {n2}/{d2}?",
          choices, ans,
          f"KCF: {n1}/{d1} × {d2}/{n2} = {frac_str(result)}.",
          ["division", "fractions", "complex fractions"])

# --- Hard: Complex mixed number division (531-560) ---
hard_mixed_pairs = [
    ((5, 3, 8), (2, 5, 16)), ((7, 2, 9), (3, 4, 27)), ((9, 5, 12), (4, 7, 24)),
    ((11, 3, 14), (5, 9, 28)), ((6, 7, 15), (3, 11, 30)), ((8, 5, 18), (4, 7, 36)),
    ((12, 3, 16), (6, 5, 32)), ((10, 7, 20), (5, 9, 40)), ((14, 5, 24), (7, 11, 48)),
    ((3, 5, 7), (1, 8, 21)), ((4, 7, 9), (2, 5, 18)), ((5, 11, 12), (2, 7, 24)),
    ((6, 5, 8), (3, 3, 16)), ((7, 3, 10), (3, 7, 20)), ((8, 7, 12), (4, 5, 24)),
    ((9, 2, 15), (4, 8, 45)), ((10, 3, 7), (5, 1, 14)), ((11, 5, 9), (5, 7, 18)),
    ((13, 2, 11), (6, 5, 22)), ((15, 3, 8), (7, 5, 16)), ((4, 5, 6), (2, 1, 3)),
    ((6, 3, 4), (3, 1, 8)), ((8, 2, 5), (4, 1, 10)), ((10, 5, 6), (5, 1, 12)),
    ((12, 7, 8), (6, 3, 16)), ((14, 3, 5), (7, 1, 10)), ((16, 5, 9), (8, 2, 27)),
    ((3, 7, 8), (1, 5, 16)), ((5, 5, 6), (2, 7, 12)), ((7, 3, 4), (3, 5, 8)),
]

for (w1, n1, d1), (w2, n2, d2) in hard_mixed_pairs:
    f1 = Fraction(w1 * d1 + n1, d1)
    f2 = Fraction(w2 * d2 + n2, d2)
    result = f1 / f2
    choices, ans = make_choices_fraction(result)
    add_q("Hard",
          f"What is {w1} {n1}/{d1} ÷ {w2} {n2}/{d2}?",
          choices, ans,
          f"Convert: {frac_str(f1)} ÷ {frac_str(f2)}. KCF: {frac_str(result)}.",
          ["division", "fractions", "mixed numbers", "complex"])

# --- Hard: Multi-step and order of operations (561-580) ---
multi_step_problems = [
    ("What is (48 ÷ 6) × (72 ÷ 9)?", (48 // 6) * (72 // 9), "48 ÷ 6 = 8; 72 ÷ 9 = 8; 8 × 8 = 64."),
    ("What is 144 ÷ (12 ÷ 3)?", 144 // (12 // 3), "12 ÷ 3 = 4; 144 ÷ 4 = 36."),
    ("What is (225 ÷ 15) + (168 ÷ 14)?", 225 // 15 + 168 // 14, "225 ÷ 15 = 15; 168 ÷ 14 = 12; 15 + 12 = 27."),
    ("What is (1000 ÷ 25) - (576 ÷ 24)?", 1000 // 25 - 576 // 24, "1000 ÷ 25 = 40; 576 ÷ 24 = 24; 40 - 24 = 16."),
    ("What is 360 ÷ (5 × 6)?", 360 // (5 * 6), "5 × 6 = 30; 360 ÷ 30 = 12."),
    ("What is (2400 ÷ 48) × 3?", (2400 // 48) * 3, "2400 ÷ 48 = 50; 50 × 3 = 150."),
    ("What is 5000 ÷ (125 ÷ 5)?", 5000 // (125 // 5), "125 ÷ 5 = 25; 5000 ÷ 25 = 200."),
    ("What is (729 ÷ 27) × (512 ÷ 64)?", (729 // 27) * (512 // 64), "729 ÷ 27 = 27; 512 ÷ 64 = 8; 27 × 8 = 216."),
    ("What is (1296 ÷ 36) - (1024 ÷ 32)?", 1296 // 36 - 1024 // 32, "1296 ÷ 36 = 36; 1024 ÷ 32 = 32; 36 - 32 = 4."),
    ("What is (4500 ÷ 75) + (3600 ÷ 45)?", 4500 // 75 + 3600 // 45, "4500 ÷ 75 = 60; 3600 ÷ 45 = 80; 60 + 80 = 140."),
    ("What is 7200 ÷ (24 × 15)?", 7200 // (24 * 15), "24 × 15 = 360; 7200 ÷ 360 = 20."),
    ("What is (8100 ÷ 90) × (6400 ÷ 80)?", (8100 // 90) * (6400 // 80), "8100 ÷ 90 = 90; 6400 ÷ 80 = 80; 90 × 80 = 7,200."),
    ("What is (15000 ÷ 250) - (12000 ÷ 300)?", 15000 // 250 - 12000 // 300, "15000 ÷ 250 = 60; 12000 ÷ 300 = 40; 60 - 40 = 20."),
    ("What is 9600 ÷ (32 × 12)?", 9600 // (32 * 12), "32 × 12 = 384; 9600 ÷ 384 = 25."),
    ("What is (2025 ÷ 45) + (1764 ÷ 42)?", 2025 // 45 + 1764 // 42, "2025 ÷ 45 = 45; 1764 ÷ 42 = 42; 45 + 42 = 87."),
    ("What is (3375 ÷ 75) × (2744 ÷ 56)?", (3375 // 75) * (2744 // 56), "3375 ÷ 75 = 45; 2744 ÷ 56 = 49; 45 × 49 = 2,205."),
    ("What is 10000 ÷ (50 × 8)?", 10000 // (50 * 8), "50 × 8 = 400; 10000 ÷ 400 = 25."),
    ("What is (5184 ÷ 72) + (4096 ÷ 64)?", 5184 // 72 + 4096 // 64, "5184 ÷ 72 = 72; 4096 ÷ 64 = 64; 72 + 64 = 136."),
    ("What is (6561 ÷ 81) - (4913 ÷ 17)?", 6561 // 81 - 4913 // 17, "6561 ÷ 81 = 81; 4913 ÷ 17 = 289; 81 - 289 = -208."),
    ("What is (7776 ÷ 108) × 5?", (7776 // 108) * 5, "7776 ÷ 108 = 72; 72 × 5 = 360."),
]

for text, result, expl in multi_step_problems:
    choices, ans = make_choices_int(result)
    add_q("Hard", text, choices, ans, expl,
          ["division", "order of operations", "multi-step"])


# --- Hard: Complex word problems (581-600) ---
hard_word_problems = [
    ("A government project worth ₱12,456,000 is to be completed in 36 months. If the monthly expenditure is equal, what is the monthly cost?",
     12456000, 36, "pesos per month", ["division", "word problem", "budgeting", "large numbers"]),
    ("A city's water supply of 2,592,000 liters must last 864 households for one day. How many liters per household?",
     2592000, 864, "liters per household", ["division", "word problem", "resource allocation"]),
    ("A national highway spanning 1,728 km is divided into 48 maintenance zones. How many km per zone?",
     1728, 48, "km per zone", ["division", "word problem", "engineering"]),
    ("A government hospital's annual medicine budget of ₱8,640,000 serves 7,200 patients. What is the average cost per patient?",
     8640000, 7200, "pesos per patient", ["division", "word problem", "healthcare"]),
    ("A telecommunications tower serves 186,624 subscribers across 432 sectors. How many subscribers per sector?",
     186624, 432, "subscribers per sector", ["division", "word problem", "telecommunications"]),
    ("A disaster relief fund of ₱45,360,000 is distributed to 756 barangays. How much per barangay?",
     45360000, 756, "pesos per barangay", ["division", "word problem", "disaster relief"]),
    ("A census counted 3,628,800 residents in a province with 5,040 barangays. What is the average population per barangay?",
     3628800, 5040, "residents per barangay", ["division", "word problem", "statistics"]),
    ("A power plant generates 518,400 kWh daily for 7,200 households. How many kWh per household per day?",
     518400, 7200, "kWh per household", ["division", "word problem", "utilities"]),
    ("A school district's total enrollment of 248,832 students is spread across 576 schools. What is the average enrollment per school?",
     248832, 576, "students per school", ["division", "word problem", "education"]),
    ("A national vaccination drive administered 1,296,000 doses over 540 vaccination sites. How many doses per site?",
     1296000, 540, "doses per site", ["division", "word problem", "healthcare"]),
    ("A government fleet of vehicles traveled a combined 746,496 km in a year across 864 vehicles. What is the average km per vehicle?",
     746496, 864, "km per vehicle", ["division", "word problem", "transportation"]),
    ("A public works project used 362,880 cubic meters of concrete over 504 days. What is the daily usage?",
     362880, 504, "cubic meters per day", ["division", "word problem", "construction"]),
    ("A national library system has 1,555,200 books distributed among 3,600 branches. How many books per branch?",
     1555200, 3600, "books per branch", ["division", "word problem", "library"]),
    ("A social welfare program disbursed ₱2,073,600 to 1,440 beneficiaries. How much per beneficiary?",
     2073600, 1440, "pesos per beneficiary", ["division", "word problem", "social welfare"]),
    ("A government data center processes 9,331,200 transactions monthly across 8,640 terminals. How many transactions per terminal?",
     9331200, 8640, "transactions per terminal", ["division", "word problem", "technology"]),
    ("An agricultural program distributed 414,720 seedlings to 648 farms. How many seedlings per farm?",
     414720, 648, "seedlings per farm", ["division", "word problem", "agriculture"]),
    ("A postal service delivered 2,799,360 parcels in a year using 3,240 delivery personnel. How many parcels per person?",
     2799360, 3240, "parcels per person", ["division", "word problem", "postal service"]),
    ("A fire department responded to 103,680 calls in a year across 288 stations. How many calls per station?",
     103680, 288, "calls per station", ["division", "word problem", "emergency services"]),
    ("A public transportation system carried 5,598,720 passengers monthly across 6,480 routes. How many passengers per route?",
     5598720, 6480, "passengers per route", ["division", "word problem", "transportation"]),
    ("A government payroll of ₱186,624,000 is distributed to 4,320 employees. What is the average salary?",
     186624000, 4320, "pesos per employee", ["division", "word problem", "payroll"]),
]

for text, dividend, divisor, unit, tags in hard_word_problems:
    quotient = dividend // divisor
    choices, ans = make_choices_int(quotient)
    add_q("Hard", text, choices, ans,
          f"{fmt(dividend)} ÷ {fmt(divisor)} = {fmt(quotient)} {unit}.",
          tags)


# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Generated: {len(questions)} total questions")
print(f"  Easy: {easy_count}")
print(f"  Medium: {medium_count}")
print(f"  Hard: {hard_count}")

# Write output
output_dir = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "numerical-ability" / "basic-operations" / "division"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
