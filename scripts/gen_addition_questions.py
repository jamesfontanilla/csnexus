"""
Generate 600 multiple-choice addition questions for the CSE Numerical Ability section.
Distribution: 200 Easy, 200 Medium, 200 Hard
Output: data/seed/questions/numerical-ability/basic-operations/addition/questions.json
"""

import json
import random
import os
from fractions import Fraction
from math import gcd

random.seed(42)

questions = []
current_id = 0


def next_id():
    global current_id
    current_id += 1
    return current_id


def make_q(difficulty, question, choices, answer, explanation, tags):
    return {
        "id": next_id(),
        "subtest": "Numerical Ability",
        "module": "Basic Operations",
        "subtopic": "Addition",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    }


def generate_distractors_int(correct, count=3, spread=None):
    """Generate integer distractors near the correct answer."""
    if spread is None:
        spread = max(5, abs(correct) // 10 + 1)
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 100:
        offset = random.choice([-3, -2, -1, 1, 2, 3, -10, 10, -spread, spread])
        d = correct + offset
        if d != correct and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct + len(distractors) + 1)
    return list(distractors)[:count]


def generate_distractors_decimal(correct, count=3):
    """Generate decimal distractors near the correct answer."""
    distractors = set()
    attempts = 0
    offsets = [0.1, -0.1, 1.0, -1.0, 0.01, -0.01, 10, -10, 0.5, -0.5]
    while len(distractors) < count and attempts < 100:
        offset = random.choice(offsets)
        d = round(correct + offset, 4)
        if d != correct and d not in distractors and d > 0:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(round(correct + (len(distractors) + 1) * 0.1, 4))
    return list(distractors)[:count]


def format_decimal(val):
    """Format a decimal value cleanly."""
    if val == int(val):
        return str(int(val))
    return f"{val:g}"


def format_fraction(f):
    """Format a Fraction as a string."""
    if f.denominator == 1:
        return str(f.numerator)
    if abs(f.numerator) > f.denominator:
        whole = abs(f.numerator) // f.denominator
        remainder = abs(f.numerator) % f.denominator
        sign = "-" if f.numerator < 0 else ""
        if remainder == 0:
            return f"{sign}{whole}"
        return f"{sign}{whole} {remainder}/{f.denominator}"
    return f"{f.numerator}/{f.denominator}"


def fraction_distractors(correct_frac, count=3):
    """Generate fraction distractors."""
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        # Various ways to create wrong answers
        strategy = random.choice(["num_off", "den_off", "unsimplified", "swap"])
        if strategy == "num_off":
            off = random.choice([-2, -1, 1, 2])
            d = Fraction(correct_frac.numerator + off, correct_frac.denominator)
        elif strategy == "den_off":
            new_den = correct_frac.denominator + random.choice([-1, 1, 2])
            if new_den > 0:
                d = Fraction(correct_frac.numerator, new_den)
            else:
                d = Fraction(correct_frac.numerator + 1, correct_frac.denominator)
        elif strategy == "unsimplified":
            d = Fraction(correct_frac.numerator + random.randint(1, 3),
                         correct_frac.denominator + random.randint(1, 3))
        else:
            d = Fraction(correct_frac.denominator, correct_frac.numerator) if correct_frac.numerator != 0 else Fraction(1, 2)
        if d != correct_frac and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct_frac + Fraction(len(distractors) + 1, 7))
    return [format_fraction(d) for d in list(distractors)[:count]]


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Whole number addition (no regrouping) - 25 questions ---
easy_whole_simple = [
    (23, 45), (12, 34), (51, 37), (42, 16), (30, 25),
    (61, 28), (14, 53), (72, 15), (33, 44), (20, 59),
    (41, 38), (55, 23), (64, 15), (11, 67), (36, 42),
    (73, 16), (24, 51), (82, 13), (45, 32), (17, 61),
    (53, 26), (31, 48), (66, 22), (44, 35), (27, 52)
]

for a, b in easy_whole_simple:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Easy",
        f"What is {a:,} + {b:,}?",
        choices,
        str(correct),
        f"Add the numbers: {a} + {b} = {correct}.",
        ["addition", "whole numbers", "no regrouping"]
    ))


# --- Easy: Whole number addition (with regrouping) - 25 questions ---
easy_whole_regroup = [
    (48, 35), (67, 28), (59, 34), (76, 47), (88, 25),
    (95, 38), (64, 79), (57, 86), (39, 74), (46, 68),
    (83, 49), (77, 56), (68, 45), (54, 89), (92, 39),
    (156, 87), (234, 89), (178, 45), (267, 56), (345, 78),
    (189, 234), (456, 167), (278, 345), (123, 489), (567, 245)
]

for a, b in easy_whole_regroup:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    exp = f"Add {a} + {b}. "
    if (a % 10 + b % 10) >= 10:
        ones_sum = a % 10 + b % 10
        exp += f"Ones: {a%10} + {b%10} = {ones_sum} (write {ones_sum%10}, carry {ones_sum//10}). "
    exp += f"The sum is {correct}."
    questions.append(make_q(
        "Easy",
        f"What is {a:,} + {b:,}?",
        choices,
        str(correct),
        exp,
        ["addition", "whole numbers", "regrouping"]
    ))

# --- Easy: Single-digit addition facts - 15 questions ---
easy_single = [
    (7, 8), (9, 6), (8, 5), (6, 7), (9, 9),
    (8, 8), (7, 6), (9, 4), (5, 8), (6, 9),
    (7, 9), (8, 6), (9, 7), (5, 9), (8, 7)
]

for a, b in easy_single:
    correct = a + b
    dists = generate_distractors_int(correct, spread=3)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Easy",
        f"What is {a} + {b}?",
        choices,
        str(correct),
        f"{a} + {b} = {correct}.",
        ["addition", "whole numbers", "single digit"]
    ))

# --- Easy: Integer addition (same sign) - 20 questions ---
easy_int_same = [
    (-3, -5), (-7, -2), (-10, -4), (-6, -8), (-1, -9),
    (-12, -5), (-8, -7), (-15, -3), (-4, -11), (-20, -6),
    (-13, -14), (-9, -9), (-25, -5), (-16, -7), (-11, -12),
    (-30, -10), (-22, -8), (-17, -13), (-19, -6), (-14, -16)
]

for a, b in easy_int_same:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Easy",
        f"What is ({a}) + ({b})?",
        choices,
        str(correct),
        f"Both numbers are negative. Add absolute values: {abs(a)} + {abs(b)} = {abs(a)+abs(b)}. Attach negative sign: {correct}.",
        ["addition", "integers", "same sign"]
    ))


# --- Easy: Integer addition (different sign) - 20 questions ---
easy_int_diff = [
    (8, -3), (-5, 9), (12, -7), (-10, 15), (6, -6),
    (-14, 20), (18, -11), (-9, 4), (7, -12), (-16, 25),
    (20, -8), (-13, 7), (15, -15), (-4, 10), (11, -3),
    (-22, 30), (25, -17), (-8, 19), (14, -6), (-18, 12)
]

for a, b in easy_int_diff:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    abs_a, abs_b = abs(a), abs(b)
    if abs_a > abs_b:
        sign_word = "positive" if a > 0 else "negative"
        exp = f"Different signs: subtract {abs_b} from {abs_a} = {abs_a - abs_b}. The number with larger absolute value is {a}, which is {sign_word}. Answer: {correct}."
    elif abs_b > abs_a:
        sign_word = "positive" if b > 0 else "negative"
        exp = f"Different signs: subtract {abs_a} from {abs_b} = {abs_b - abs_a}. The number with larger absolute value is {b}, which is {sign_word}. Answer: {correct}."
    else:
        exp = f"The absolute values are equal ({abs_a}), so the sum is 0."
    questions.append(make_q(
        "Easy",
        f"What is ({a}) + ({b})?",
        choices,
        str(correct),
        exp,
        ["addition", "integers", "different signs"]
    ))

# --- Easy: Decimal addition (simple) - 25 questions ---
easy_decimals = [
    (1.5, 2.3), (3.4, 1.2), (5.6, 2.1), (4.3, 3.5), (7.2, 1.6),
    (2.8, 4.1), (6.5, 1.3), (3.7, 2.2), (8.1, 0.7), (5.4, 3.3),
    (1.25, 2.50), (3.75, 1.25), (4.50, 2.25), (6.10, 1.80), (2.45, 3.30),
    (0.5, 0.3), (0.8, 0.1), (0.6, 0.7), (0.9, 0.4), (0.25, 0.75),
    (1.1, 2.9), (3.6, 4.4), (5.5, 2.5), (7.3, 1.7), (9.8, 0.2)
]

for a, b in easy_decimals:
    correct = round(a + b, 4)
    dists = generate_distractors_decimal(correct)
    choices = [format_decimal(correct)] + [format_decimal(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Easy",
        f"What is {a} + {b}?",
        choices,
        format_decimal(correct),
        f"Align decimal points and add: {a} + {b} = {format_decimal(correct)}.",
        ["addition", "decimals", "basic"]
    ))


# --- Easy: Fraction addition (like denominators) - 20 questions ---
easy_frac_like = [
    (1, 5, 2, 5), (2, 7, 3, 7), (1, 4, 2, 4), (3, 8, 1, 8), (2, 9, 4, 9),
    (1, 6, 3, 6), (5, 12, 1, 12), (3, 10, 4, 10), (2, 5, 1, 5), (4, 9, 2, 9),
    (1, 3, 1, 3), (3, 7, 2, 7), (5, 8, 1, 8), (2, 11, 5, 11), (4, 15, 7, 15),
    (1, 4, 1, 4), (3, 5, 1, 5), (2, 3, 1, 3), (7, 10, 1, 10), (5, 6, 1, 6)
]

for n1, d1, n2, d2 in easy_frac_like:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    raw_num = n1 + n2
    raw_frac = Fraction(raw_num, d1)
    exp = f"Like denominators: {n1}/{d1} + {n2}/{d2} = ({n1}+{n2})/{d1} = {raw_num}/{d1}"
    if raw_frac != correct:
        exp += f" = {correct_str} (simplified)"
    exp += "."
    questions.append(make_q(
        "Easy",
        f"What is {n1}/{d1} + {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "like denominators"]
    ))

# --- Easy: Fraction addition (unlike, simple) - 15 questions ---
easy_frac_unlike = [
    (1, 2, 1, 3), (1, 4, 1, 2), (1, 3, 1, 6), (2, 5, 1, 10), (1, 2, 1, 4),
    (1, 3, 1, 4), (1, 5, 1, 2), (2, 3, 1, 6), (1, 4, 1, 3), (3, 4, 1, 8),
    (1, 6, 1, 2), (1, 5, 2, 5), (1, 2, 1, 6), (1, 3, 2, 9), (1, 4, 3, 8)
]

for n1, d1, n2, d2 in easy_frac_unlike:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    from math import lcm
    lcd = lcm(d1, d2)
    new_n1 = n1 * (lcd // d1)
    new_n2 = n2 * (lcd // d2)
    exp = f"LCD of {d1} and {d2} is {lcd}. Convert: {n1}/{d1} = {new_n1}/{lcd}, {n2}/{d2} = {new_n2}/{lcd}. Add: {new_n1}/{lcd} + {new_n2}/{lcd} = {new_n1+new_n2}/{lcd}"
    if Fraction(new_n1+new_n2, lcd) != correct:
        exp += f" = {correct_str}"
    exp += "."
    questions.append(make_q(
        "Easy",
        f"What is {n1}/{d1} + {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "unlike denominators"]
    ))


# --- Easy: Word problems (whole numbers) - 20 questions ---
easy_word_problems = [
    ("A government office has {a} employees in Building A and {b} employees in Building B. How many employees are there in total?",
     45, 38, ["addition", "whole numbers", "word problem"]),
    ("A clerk filed {a} documents in the morning and {b} documents in the afternoon. How many documents were filed in total?",
     67, 54, ["addition", "whole numbers", "word problem"]),
    ("Department A has {a} chairs and Department B has {b} chairs. What is the total number of chairs?",
     120, 85, ["addition", "whole numbers", "word problem"]),
    ("A school has {a} male students and {b} female students. What is the total enrollment?",
     234, 198, ["addition", "whole numbers", "word problem"]),
    ("A barangay collected {a} sacks of rice and received {b} more sacks as donation. How many sacks in all?",
     150, 75, ["addition", "whole numbers", "word problem"]),
    ("An office supply room has {a} reams of paper. A delivery of {b} reams arrived. How many reams are there now?",
     48, 36, ["addition", "whole numbers", "word problem"]),
    ("A library has {a} fiction books and {b} non-fiction books. What is the total number of books?",
     567, 433, ["addition", "whole numbers", "word problem"]),
    ("A government vehicle traveled {a} km on Monday and {b} km on Tuesday. What is the total distance?",
     125, 98, ["addition", "whole numbers", "word problem"]),
    ("A cashier received {a} payments in the morning and {b} payments in the afternoon. How many payments were received?",
     89, 76, ["addition", "whole numbers", "word problem"]),
    ("A municipality has {a} registered voters in Zone 1 and {b} in Zone 2. What is the combined total?",
     1250, 980, ["addition", "whole numbers", "word problem"]),
    ("A warehouse has {a} boxes of supplies. Another shipment of {b} boxes arrived. Total boxes?",
     340, 275, ["addition", "whole numbers", "word problem"]),
    ("An agency processed {a} applications in January and {b} in February. Total applications processed?",
     456, 389, ["addition", "whole numbers", "word problem"]),
    ("A canteen sold {a} meals on Monday and {b} meals on Tuesday. How many meals were sold in two days?",
     185, 210, ["addition", "whole numbers", "word problem"]),
    ("A training seminar had {a} attendees on Day 1 and {b} on Day 2. Total attendees?",
     78, 92, ["addition", "whole numbers", "word problem"]),
    ("A city has {a} public schools and {b} private schools. How many schools in total?",
     145, 67, ["addition", "whole numbers", "word problem"]),
    ("A hospital has {a} nurses and {b} doctors. What is the total medical staff?",
     320, 85, ["addition", "whole numbers", "word problem"]),
    ("A post office delivered {a} letters and {b} packages today. Total items delivered?",
     567, 123, ["addition", "whole numbers", "word problem"]),
    ("A farm harvested {a} kg of rice and {b} kg of corn. Total harvest in kg?",
     890, 456, ["addition", "whole numbers", "word problem"]),
    ("A bus carried {a} passengers in the morning trip and {b} in the afternoon trip. Total passengers?",
     47, 53, ["addition", "whole numbers", "word problem"]),
    ("An office has {a} desktop computers and {b} laptops. How many computers in total?",
     35, 28, ["addition", "whole numbers", "word problem"]),
]

for template, a, b, tags in easy_word_problems:
    correct = a + b
    question_text = template.format(a=f"{a:,}", b=f"{b:,}")
    dists = generate_distractors_int(correct)
    choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Easy",
        question_text,
        choices,
        f"{correct:,}",
        f"Add the two quantities: {a:,} + {b:,} = {correct:,}.",
        tags
    ))

# --- Easy: Properties of addition - 15 questions ---
easy_properties = [
    ("Which property of addition states that a + b = b + a?", 
     ["Commutative Property", "Associative Property", "Identity Property", "Distributive Property"],
     "Commutative Property",
     "The commutative property states that the order of addends does not change the sum: a + b = b + a."),
    ("What is the sum of any number and zero?",
     ["The number itself", "Zero", "One", "Undefined"],
     "The number itself",
     "The identity property of addition states that adding zero to any number gives that same number: a + 0 = a."),
    ("If 15 + 23 = 38, what is 23 + 15?",
     ["38", "53", "8", "35"],
     "38",
     "By the commutative property, 23 + 15 = 15 + 23 = 38."),
    ("Which property allows us to regroup addends: (a + b) + c = a + (b + c)?",
     ["Associative Property", "Commutative Property", "Identity Property", "Closure Property"],
     "Associative Property",
     "The associative property states that grouping of addends does not affect the sum."),
    ("What is 456 + 0?",
     ["456", "0", "457", "455"],
     "456",
     "Adding zero to any number gives that same number (identity property): 456 + 0 = 456."),
    ("Using the associative property, (7 + 3) + 5 = 7 + (3 + 5). What is the sum?",
     ["15", "12", "10", "17"],
     "15",
     "(7 + 3) + 5 = 10 + 5 = 15. Also, 7 + (3 + 5) = 7 + 8 = 15. Both give 15."),
    ("What are the addends in the expression 12 + 8 = 20?",
     ["12 and 8", "12 and 20", "8 and 20", "20 and 12"],
     "12 and 8",
     "Addends are the numbers being added. In 12 + 8 = 20, the addends are 12 and 8, and 20 is the sum."),
    ("What is the sum called in an addition sentence?",
     ["The total or result", "The addend", "The factor", "The difference"],
     "The total or result",
     "In addition, the result of combining addends is called the sum (or total)."),
    ("If a + b = c, then b + a = ?",
     ["c", "a", "b", "0"],
     "c",
     "By the commutative property, changing the order of addends does not change the sum."),
    ("What is 0 + 0?",
     ["0", "1", "Undefined", "2"],
     "0",
     "Zero plus zero equals zero: 0 + 0 = 0."),
    ("Which of the following demonstrates the identity property? ",
     ["99 + 0 = 99", "5 + 3 = 3 + 5", "(2+3)+4 = 2+(3+4)", "6 + 6 = 12"],
     "99 + 0 = 99",
     "The identity property shows that adding 0 to a number gives the same number: 99 + 0 = 99."),
    ("The sum of two whole numbers is always a whole number. This illustrates the:",
     ["Closure Property", "Commutative Property", "Associative Property", "Identity Property"],
     "Closure Property",
     "The closure property states that performing addition on two numbers in a set always produces a result within the same set."),
    ("What is the additive identity?",
     ["0", "1", "-1", "Infinity"],
     "0",
     "The additive identity is 0 because adding 0 to any number does not change it."),
    ("(25 + 75) + 50 = 25 + (75 + 50). Both equal:",
     ["150", "100", "125", "175"],
     "150",
     "(25 + 75) + 50 = 100 + 50 = 150. Also 25 + (75 + 50) = 25 + 125 = 150."),
    ("If you rearrange 3 + 7 + 5 as 7 + 3 + 5, which property did you use?",
     ["Commutative Property", "Associative Property", "Distributive Property", "Identity Property"],
     "Commutative Property",
     "Rearranging the order of addends uses the commutative property."),
]

for q_text, ch, ans, exp in easy_properties:
    questions.append(make_q(
        "Easy", q_text, ch, ans, exp,
        ["addition", "properties", "conceptual"]
    ))


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Multi-digit whole number addition - 30 questions ---
medium_whole = []
random.seed(100)
for _ in range(30):
    a = random.randint(1000, 9999)
    b = random.randint(1000, 9999)
    medium_whole.append((a, b))

for a, b in medium_whole:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Medium",
        f"What is {a:,} + {b:,}?",
        choices,
        f"{correct:,}",
        f"Add column by column with regrouping as needed: {a:,} + {b:,} = {correct:,}.",
        ["addition", "whole numbers", "multi-digit"]
    ))

# --- Medium: Three-number addition - 20 questions ---
random.seed(200)
for _ in range(20):
    a = random.randint(100, 999)
    b = random.randint(100, 999)
    c = random.randint(100, 999)
    correct = a + b + c
    dists = generate_distractors_int(correct)
    choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Medium",
        f"What is {a} + {b} + {c}?",
        choices,
        f"{correct:,}",
        f"Add: {a} + {b} = {a+b}, then {a+b} + {c} = {correct}.",
        ["addition", "whole numbers", "three addends"]
    ))

# --- Medium: Integer addition (larger numbers) - 25 questions ---
medium_integers = [
    (-45, 78), (67, -89), (-123, 56), (234, -189), (-67, -45),
    (-150, 200), (89, -134), (-78, 78), (156, -200), (-300, 175),
    (-56, -89), (245, -100), (-178, 90), (99, -99), (-234, 300),
    (-45, -67), (123, -45), (-89, 150), (200, -350), (-125, -75),
    (450, -500), (-67, 234), (89, -89), (-156, 78), (-200, 350)
]

for a, b in medium_integers:
    correct = a + b
    dists = generate_distractors_int(correct)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    if (a > 0 and b > 0) or (a < 0 and b < 0):
        exp = f"Same signs: add absolute values {abs(a)} + {abs(b)} = {abs(a)+abs(b)}, keep the sign. Answer: {correct}."
    elif abs(a) == abs(b):
        exp = f"Equal absolute values with opposite signs cancel out. Answer: 0."
    else:
        larger = a if abs(a) > abs(b) else b
        exp = f"Different signs: {abs(a)} - {abs(b)} = {abs(correct) if correct != 0 else 0}. Sign of larger absolute value ({larger}). Answer: {correct}."
    questions.append(make_q(
        "Medium",
        f"What is ({a}) + ({b})?",
        choices,
        str(correct),
        exp,
        ["addition", "integers", "medium"]
    ))


# --- Medium: Decimal addition (multi-place) - 25 questions ---
medium_decimals = [
    (12.45, 8.78), (23.67, 15.89), (45.05, 9.95), (67.89, 23.45), (34.56, 78.99),
    (1.234, 5.678), (9.876, 3.456), (12.005, 7.995), (0.456, 0.789), (3.14, 2.86),
    (100.50, 99.75), (45.678, 12.345), (78.9, 1.234), (56.78, 43.22), (89.01, 10.99),
    (234.56, 89.78), (0.125, 0.875), (15.75, 24.50), (67.89, 32.11), (99.99, 0.01),
    (5.555, 4.445), (123.4, 56.78), (0.001, 0.999), (45.67, 54.33), (78.125, 21.875)
]

for a, b in medium_decimals:
    correct = round(a + b, 4)
    dists = generate_distractors_decimal(correct)
    choices = [format_decimal(correct)] + [format_decimal(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Medium",
        f"What is {a} + {b}?",
        choices,
        format_decimal(correct),
        f"Align decimal points: {a} + {b} = {format_decimal(correct)}.",
        ["addition", "decimals", "multi-place"]
    ))

# --- Medium: Fraction addition (unlike denominators) - 25 questions ---
medium_fractions = [
    (2, 3, 3, 4), (5, 6, 1, 4), (3, 8, 2, 5), (4, 9, 1, 3), (5, 7, 2, 3),
    (7, 12, 3, 8), (2, 5, 4, 7), (3, 10, 2, 15), (5, 8, 3, 10), (1, 6, 5, 9),
    (4, 5, 2, 3), (7, 8, 1, 6), (3, 4, 5, 12), (2, 9, 5, 6), (4, 7, 3, 14),
    (5, 9, 2, 3), (1, 8, 3, 4), (7, 10, 1, 5), (2, 7, 5, 14), (3, 5, 7, 15),
    (4, 11, 2, 3), (5, 6, 7, 18), (1, 4, 5, 16), (8, 9, 1, 6), (3, 7, 4, 21)
]

for n1, d1, n2, d2 in medium_fractions:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    from math import lcm
    lcd = lcm(d1, d2)
    new_n1 = n1 * (lcd // d1)
    new_n2 = n2 * (lcd // d2)
    total_num = new_n1 + new_n2
    exp = f"LCD of {d1} and {d2} = {lcd}. Convert: {n1}/{d1} = {new_n1}/{lcd}, {n2}/{d2} = {new_n2}/{lcd}. Sum = {total_num}/{lcd} = {correct_str}."
    questions.append(make_q(
        "Medium",
        f"What is {n1}/{d1} + {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "unlike denominators"]
    ))


# --- Medium: Mixed number addition - 20 questions ---
medium_mixed = [
    (2, 1, 4, 3, 2, 3), (1, 3, 5, 2, 1, 4), (4, 2, 7, 1, 5, 7),
    (3, 1, 3, 2, 1, 6), (5, 3, 8, 1, 5, 8), (2, 4, 9, 3, 2, 9),
    (1, 2, 5, 4, 3, 10), (6, 1, 2, 2, 3, 4), (3, 5, 6, 4, 1, 3),
    (7, 2, 3, 1, 5, 6), (2, 3, 7, 5, 1, 14), (4, 1, 8, 3, 3, 8),
    (1, 7, 12, 2, 5, 6), (5, 2, 9, 3, 4, 9), (3, 1, 5, 6, 2, 5),
    (8, 3, 4, 2, 1, 2), (4, 5, 12, 3, 7, 12), (2, 1, 6, 7, 5, 6),
    (6, 2, 5, 1, 3, 10), (3, 4, 15, 5, 2, 5)
]

for whole1, n1, d1, whole2, n2, d2 in medium_mixed:
    f1 = Fraction(whole1 * d1 + n1, d1)
    f2 = Fraction(whole2 * d2 + n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    exp = f"Convert to improper: {whole1} {n1}/{d1} = {f1.numerator}/{f1.denominator}, {whole2} {n2}/{d2} = {f2.numerator}/{f2.denominator}. Add and simplify: {correct_str}."
    questions.append(make_q(
        "Medium",
        f"What is {whole1} {n1}/{d1} + {whole2} {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "mixed numbers"]
    ))

# --- Medium: Money word problems - 20 questions ---
medium_money = [
    ("An employee's basic pay is ₱{a} and overtime pay is ₱{b}. What is the total pay?",
     18500.00, 3245.75),
    ("Office supplies cost ₱{a} and printing costs ₱{b}. Total expense?",
     2345.50, 1678.25),
    ("A government vehicle's fuel cost ₱{a} and maintenance cost ₱{b}. Total vehicle expense?",
     4567.00, 2890.50),
    ("Monthly rent is ₱{a} and utilities are ₱{b}. Total monthly overhead?",
     15000.00, 4567.89),
    ("Training fee is ₱{a} and travel allowance is ₱{b}. Total training cost?",
     5000.00, 3456.78),
    ("First quarter revenue: ₱{a}. Second quarter revenue: ₱{b}. Total for two quarters?",
     125000.50, 134567.75),
    ("Salary: ₱{a}. Bonus: ₱{b}. Total compensation?",
     25000.00, 5000.00),
    ("Electric bill: ₱{a}. Water bill: ₱{b}. Total utilities?",
     3456.78, 1234.56),
    ("Purchase of chairs: ₱{a}. Purchase of tables: ₱{b}. Total furniture cost?",
     12450.00, 8975.50),
    ("Morning sales: ₱{a}. Afternoon sales: ₱{b}. Total daily sales?",
     45678.90, 38912.45),
    ("January expenses: ₱{a}. February expenses: ₱{b}. Two-month total?",
     67890.25, 72345.80),
    ("Airfare: ₱{a}. Hotel: ₱{b}. Total travel cost?",
     8500.00, 6750.00),
    ("Food allowance: ₱{a}. Transportation allowance: ₱{b}. Total allowances?",
     3500.00, 2800.00),
    ("Printing: ₱{a}. Binding: ₱{b}. Total document preparation cost?",
     1250.75, 450.25),
    ("Equipment A: ₱{a}. Equipment B: ₱{b}. Total equipment cost?",
     34567.00, 28945.50),
    ("Tax collected from Zone 1: ₱{a}. Zone 2: ₱{b}. Total tax?",
     89012.34, 76543.21),
    ("Salary loan payment: ₱{a}. Emergency loan payment: ₱{b}. Total deductions?",
     2500.00, 1500.00),
    ("Paper cost: ₱{a}. Ink cost: ₱{b}. Total printing supplies?",
     890.50, 2345.75),
    ("Catering: ₱{a}. Venue rental: ₱{b}. Total event cost?",
     15000.00, 8000.00),
    ("Health insurance: ₱{a}. Life insurance: ₱{b}. Total insurance premiums?",
     1200.00, 850.50),
]

for template, a, b in medium_money:
    correct = round(a + b, 2)
    question_text = template.format(a=f"{a:,.2f}", b=f"{b:,.2f}")
    dists = generate_distractors_decimal(correct)
    correct_str = f"{correct:,.2f}"
    choices = [correct_str] + [f"{d:,.2f}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Medium",
        question_text,
        choices,
        correct_str,
        f"Add: ₱{a:,.2f} + ₱{b:,.2f} = ₱{correct_str}.",
        ["addition", "decimals", "money", "word problem"]
    ))


# --- Medium: Estimation questions - 15 questions ---
medium_estimation = [
    ("Estimate the sum of 487 + 312 by rounding to the nearest hundred.",
     ["800", "700", "900", "1,000"], "800",
     "487 rounds to 500, 312 rounds to 300. Estimate: 500 + 300 = 800."),
    ("Estimate: 1,876 + 2,345 (round to nearest thousand).",
     ["4,000", "3,000", "5,000", "4,200"], "4,000",
     "1,876 rounds to 2,000; 2,345 rounds to 2,000. Estimate: 2,000 + 2,000 = 4,000."),
    ("Estimate: 67 + 45 + 89 (round to nearest ten).",
     ["200", "190", "210", "180"], "200",
     "67≈70, 45≈50, 89≈90. Estimate: 70+50+90 = 210. Closest: 200 (actual is 201)."),
    ("Which is the best estimate for 4,567 + 3,891?",
     ["8,500", "7,500", "9,000", "8,000"], "8,500",
     "4,567≈4,500 and 3,891≈4,000. Estimate: 4,500+4,000=8,500. Actual: 8,458."),
    ("Estimate: 995 + 1,005.",
     ["2,000", "1,900", "2,100", "1,800"], "2,000",
     "995≈1,000 and 1,005≈1,000. Estimate: 1,000+1,000=2,000. Actual: 2,000."),
    ("Round to the nearest ten and estimate: 78 + 43.",
     ["120", "110", "130", "100"], "120",
     "78≈80, 43≈40. Estimate: 80+40=120. Actual: 121."),
    ("Estimate: 2,499 + 3,501 (nearest thousand).",
     ["6,000", "5,000", "7,000", "5,500"], "6,000",
     "2,499≈2,000 (or 2,500), 3,501≈4,000 (or 3,500). Best estimate: 6,000. Actual: 6,000."),
    ("Which is closest to 156 + 289?",
     ["450", "350", "550", "400"], "450",
     "156≈150, 289≈300. Estimate: 150+300=450. Actual: 445."),
    ("Estimate: 8.7 + 3.2 (round to nearest whole number).",
     ["12", "11", "13", "10"], "12",
     "8.7≈9, 3.2≈3. Estimate: 9+3=12. Actual: 11.9≈12."),
    ("Estimate: 45.6 + 54.8 (round to nearest ten).",
     ["100", "90", "110", "80"], "100",
     "45.6≈50, 54.8≈50. Estimate: 50+50=100. Actual: 100.4."),
    ("Using front-end estimation, estimate 567 + 234.",
     ["800", "700", "900", "750"], "800",
     "Front-end: 500+200=700. Adjust: 67+34≈100. Total estimate: 800. Actual: 801."),
    ("Estimate: 12,345 + 7,890 (nearest thousand).",
     ["20,000", "19,000", "21,000", "18,000"], "20,000",
     "12,345≈12,000; 7,890≈8,000. Estimate: 12,000+8,000=20,000. Actual: 20,235."),
    ("Which pair of compatible numbers best estimates 73 + 28?",
     ["75 + 25 = 100", "70 + 30 = 100", "80 + 20 = 100", "73 + 27 = 100"],
     "75 + 25 = 100",
     "73≈75 and 28≈25 are the closest compatible numbers. 75+25=100. Actual: 101."),
    ("Estimate: 999 + 1.",
     ["1,000", "999", "1,001", "990"], "1,000",
     "999 + 1 = 1,000 exactly. No estimation needed — this is exact."),
    ("Estimate the sum: 3,456 + 2,789 + 1,234 (nearest thousand).",
     ["7,000", "8,000", "6,000", "7,500"], "7,000",
     "3,456≈3,000; 2,789≈3,000; 1,234≈1,000. Estimate: 3,000+3,000+1,000=7,000. Actual: 7,479."),
]

for q_text, ch, ans, exp in medium_estimation:
    questions.append(make_q(
        "Medium", q_text, ch, ans, exp,
        ["addition", "estimation", "mental math"]
    ))


# --- Medium: Word problems (various contexts) - 20 questions ---
medium_word_various = [
    ("A government agency has three divisions with 234, 189, and 312 employees respectively. What is the total number of employees?",
     234 + 189 + 312, ["735", "725", "745", "715"]),
    ("A municipal treasurer collected taxes of ₱45,678 in Week 1, ₱52,345 in Week 2, and ₱38,912 in Week 3. What is the total collection?",
     45678 + 52345 + 38912, ["136,935", "135,935", "137,935", "134,935"]),
    ("A warehouse received 1,250 boxes on Monday, 980 on Wednesday, and 1,456 on Friday. Total boxes received?",
     1250 + 980 + 1456, ["3,686", "3,586", "3,786", "3,486"]),
    ("An office building has 5 floors with 45, 52, 38, 61, and 47 rooms respectively. How many rooms in total?",
     45+52+38+61+47, ["243", "233", "253", "223"]),
    ("A city's population grew by 1,234 in 2020, 2,567 in 2021, and 1,890 in 2022. What is the total population growth over three years?",
     1234+2567+1890, ["5,691", "5,591", "5,791", "5,491"]),
    ("A student scored 78, 85, 92, and 88 on four exams. What is the total score?",
     78+85+92+88, ["343", "333", "353", "323"]),
    ("A delivery truck made stops delivering 45, 67, 23, and 89 packages. Total packages delivered?",
     45+67+23+89, ["224", "214", "234", "204"]),
    ("Three barangays have populations of 4,567, 3,890, and 5,234. Combined population?",
     4567+3890+5234, ["13,691", "13,591", "13,791", "13,491"]),
    ("A government project has Phase 1 costing ₱2,345,000, Phase 2 costing ₱1,890,000, and Phase 3 costing ₱3,456,000. Total project cost?",
     2345000+1890000+3456000, ["7,691,000", "7,591,000", "7,791,000", "7,491,000"]),
    ("An inventory count shows: pens (456), folders (234), paper clips (1,200), and staplers (89). Total items?",
     456+234+1200+89, ["1,979", "1,969", "1,989", "1,959"]),
    ("A bus route has 23 passengers at Stop 1, picks up 15 at Stop 2, and 8 more at Stop 3. How many passengers after Stop 3?",
     23+15+8, ["46", "44", "48", "42"]),
    ("Monthly electric bills: Jan ₱3,456, Feb ₱3,789, Mar ₱4,012. Total for Q1?",
     3456+3789+4012, ["11,257", "11,157", "11,357", "11,057"]),
    ("A farmer harvested 567 kg from Field A, 890 kg from Field B, and 345 kg from Field C. Total harvest?",
     567+890+345, ["1,802", "1,792", "1,812", "1,782"]),
    ("Registration: Day 1 had 234 registrants, Day 2 had 345, Day 3 had 189. Total registrants?",
     234+345+189, ["768", "758", "778", "748"]),
    ("A school library acquired 125 books in June, 89 in July, and 156 in August. Total new books?",
     125+89+156, ["370", "360", "380", "350"]),
    ("Votes counted: Candidate A got 12,345; Candidate B got 10,987; Candidate C got 8,654. Total votes cast?",
     12345+10987+8654, ["31,986", "31,886", "32,086", "31,786"]),
    ("A construction project used 2,345 bags of cement in Month 1 and 1,987 bags in Month 2. Total cement used?",
     2345+1987, ["4,332", "4,232", "4,432", "4,132"]),
    ("Office attendance: Monday 45, Tuesday 48, Wednesday 42, Thursday 50, Friday 47. Total attendance for the week?",
     45+48+42+50+47, ["232", "222", "242", "212"]),
    ("A clinic served 89 patients on Monday, 76 on Tuesday, and 95 on Wednesday. Total patients in 3 days?",
     89+76+95, ["260", "250", "270", "240"]),
    ("Budget allocations: Education ₱5,678,000, Health ₱3,456,000, Infrastructure ₱4,321,000. Total?",
     5678000+3456000+4321000, ["13,455,000", "13,355,000", "13,555,000", "13,255,000"]),
]

for q_text, correct_val, ch in medium_word_various:
    correct_str = f"{correct_val:,}"
    if correct_str not in ch:
        ch[0] = correct_str
    questions.append(make_q(
        "Medium", q_text, ch, correct_str,
        f"Add all given values to get the total: {correct_str}.",
        ["addition", "whole numbers", "word problem", "multi-step"]
    ))


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Large number addition - 25 questions ---
random.seed(300)
for _ in range(25):
    a = random.randint(10000, 99999)
    b = random.randint(10000, 99999)
    correct = a + b
    dists = generate_distractors_int(correct, spread=100)
    choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Hard",
        f"What is {a:,} + {b:,}?",
        choices,
        f"{correct:,}",
        f"Add with careful regrouping: {a:,} + {b:,} = {correct:,}.",
        ["addition", "whole numbers", "large numbers"]
    ))

# --- Hard: Multiple large number addition - 20 questions ---
random.seed(400)
for _ in range(20):
    nums = [random.randint(1000, 9999) for _ in range(random.randint(3, 5))]
    correct = sum(nums)
    dists = generate_distractors_int(correct, spread=50)
    nums_str = " + ".join(f"{n:,}" for n in nums)
    choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Hard",
        f"What is {nums_str}?",
        choices,
        f"{correct:,}",
        f"Add all numbers sequentially: sum = {correct:,}.",
        ["addition", "whole numbers", "multiple addends"]
    ))

# --- Hard: Integer addition (multiple integers) - 25 questions ---
random.seed(500)
hard_multi_int = []
for _ in range(25):
    count = random.randint(3, 5)
    nums = [random.randint(-500, 500) for _ in range(count)]
    # Ensure not all zero
    while sum(abs(n) for n in nums) == 0:
        nums = [random.randint(-500, 500) for _ in range(count)]
    hard_multi_int.append(nums)

for nums in hard_multi_int:
    correct = sum(nums)
    dists = generate_distractors_int(correct)
    nums_display = " + ".join(f"({n})" for n in nums)
    choices = [str(correct)] + [str(d) for d in dists]
    random.shuffle(choices)
    pos_sum = sum(n for n in nums if n > 0)
    neg_sum = sum(abs(n) for n in nums if n < 0)
    exp = f"Positives sum: {pos_sum}. Negatives sum: -{neg_sum}. Net: {pos_sum} - {neg_sum} = {correct}."
    questions.append(make_q(
        "Hard",
        f"What is {nums_display}?",
        choices,
        str(correct),
        exp,
        ["addition", "integers", "multiple addends"]
    ))


# --- Hard: Complex decimal addition - 25 questions ---
hard_decimals = [
    (1234.567, 890.456), (5678.901, 2345.678), (9012.345, 1234.567),
    (456.789, 123.456, 789.012), (1000.001, 999.999),
    (0.1234, 0.5678, 0.3089), (12345.67, 8901.23),
    (567.89, 432.11, 1000.00), (99.999, 0.001, 100.0),
    (3456.78, 2345.67, 1234.56), (7890.12, 3456.78),
    (0.999, 0.001, 1.0), (45678.9, 12345.6),
    (234.567, 890.123, 456.789), (1.111, 2.222, 3.333, 4.444),
    (9999.99, 0.01), (5555.55, 4444.45),
    (123.456, 789.012, 345.678), (6789.01, 2345.67, 890.12),
    (0.125, 0.250, 0.375, 0.250), (4567.89, 5432.11),
    (1234.5, 678.90, 12.345), (8765.43, 1234.57),
    (345.678, 654.322), (9876.54, 123.46, 5000.00)
]

for item in hard_decimals:
    if isinstance(item, tuple):
        nums = list(item)
    else:
        nums = [item]
    correct = round(sum(nums), 4)
    dists = generate_distractors_decimal(correct)
    nums_str = " + ".join(str(n) for n in nums)
    choices = [format_decimal(correct)] + [format_decimal(d) for d in dists]
    random.shuffle(choices)
    questions.append(make_q(
        "Hard",
        f"What is {nums_str}?",
        choices,
        format_decimal(correct),
        f"Align decimal points and add carefully: {nums_str} = {format_decimal(correct)}.",
        ["addition", "decimals", "complex"]
    ))

# --- Hard: Complex fraction addition - 25 questions ---
hard_fractions = [
    (5, 6, 7, 8), (3, 7, 5, 9), (7, 12, 11, 18), (4, 15, 7, 20),
    (8, 9, 5, 12), (11, 15, 7, 10), (9, 14, 5, 21), (13, 20, 7, 15),
    (5, 8, 7, 12), (11, 16, 3, 8), (7, 9, 8, 15), (4, 7, 9, 14),
    (13, 18, 5, 12), (7, 11, 3, 22), (8, 15, 11, 20), (9, 16, 7, 24),
    (5, 14, 9, 21), (11, 12, 7, 18), (3, 8, 5, 6), (7, 15, 8, 9),
    (13, 24, 5, 16), (9, 20, 7, 12), (11, 14, 3, 7), (5, 9, 7, 12),
    (8, 11, 5, 22)
]

for n1, d1, n2, d2 in hard_fractions:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    from math import lcm
    lcd = lcm(d1, d2)
    new_n1 = n1 * (lcd // d1)
    new_n2 = n2 * (lcd // d2)
    total_num = new_n1 + new_n2
    exp = f"LCD({d1},{d2}) = {lcd}. {n1}/{d1} = {new_n1}/{lcd}; {n2}/{d2} = {new_n2}/{lcd}. Sum = {total_num}/{lcd} = {correct_str}."
    questions.append(make_q(
        "Hard",
        f"What is {n1}/{d1} + {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "complex denominators"]
    ))


# --- Hard: Complex mixed number addition - 20 questions ---
hard_mixed = [
    (5, 7, 8, 3, 5, 6), (4, 11, 12, 6, 7, 18), (7, 5, 9, 8, 7, 12),
    (3, 8, 15, 9, 11, 20), (6, 13, 14, 4, 9, 21), (8, 3, 7, 5, 4, 9),
    (2, 7, 10, 11, 9, 15), (9, 5, 6, 3, 7, 8), (4, 11, 16, 7, 13, 24),
    (6, 9, 14, 5, 11, 21), (3, 7, 12, 8, 5, 8), (7, 4, 5, 6, 3, 10),
    (5, 8, 9, 4, 7, 12), (8, 5, 7, 3, 9, 14), (2, 11, 15, 9, 7, 10),
    (10, 3, 4, 7, 5, 12), (4, 9, 11, 8, 7, 22), (6, 7, 9, 5, 8, 18),
    (3, 13, 20, 7, 9, 15), (9, 5, 8, 4, 11, 12)
]

for whole1, n1, d1, whole2, n2, d2 in hard_mixed:
    f1 = Fraction(whole1 * d1 + n1, d1)
    f2 = Fraction(whole2 * d2 + n2, d2)
    correct = f1 + f2
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    exp = f"Convert: {whole1} {n1}/{d1} = {f1.numerator}/{f1.denominator}; {whole2} {n2}/{d2} = {f2.numerator}/{f2.denominator}. Find LCD, add, simplify: {correct_str}."
    questions.append(make_q(
        "Hard",
        f"What is {whole1} {n1}/{d1} + {whole2} {n2}/{d2}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "mixed numbers", "complex"]
    ))

# --- Hard: Multi-step word problems - 30 questions ---
hard_word_problems = [
    ("A government agency's budget has: Personnel Services ₱12,456,780; MOOE ₱8,934,215; Capital Outlay ₱5,678,900; Financial Expenses ₱1,234,567. What is the total budget?",
     12456780+8934215+5678900+1234567,
     ["28,304,462", "28,204,462", "28,404,462", "28,104,462"]),
    ("A city has 5 districts with populations: 45,678; 38,912; 52,345; 41,890; 36,789. Total population?",
     45678+38912+52345+41890+36789,
     ["215,614", "215,514", "215,714", "215,414"]),
    ("An employee's monthly deductions are: Tax ₱3,456.78; SSS ₱1,200.00; PhilHealth ₱900.00; Pag-IBIG ₱200.00; Loan ₱2,500.00. Total deductions?",
     None, ["8,256.78", "8,156.78", "8,356.78", "8,056.78"]),
    ("A construction project requires: 12,345 bags of cement, 8,901 cubic meters of gravel, 5,678 cubic meters of sand, and 3,456 steel bars. What is the total number of materials?",
     12345+8901+5678+3456,
     ["30,380", "30,280", "30,480", "30,180"]),
    ("Quarterly sales: Q1 ₱2,345,678; Q2 ₱3,456,789; Q3 ₱2,890,123; Q4 ₱4,567,890. Annual sales?",
     2345678+3456789+2890123+4567890,
     ["13,260,480", "13,160,480", "13,360,480", "13,060,480"]),
    ("A school's enrollment over 4 years: 2019: 1,234; 2020: 1,345; 2021: 1,456; 2022: 1,567. Total students enrolled over 4 years?",
     1234+1345+1456+1567,
     ["5,602", "5,502", "5,702", "5,402"]),
    ("Monthly utility bills for a year: ₱3,456 + ₱3,789 + ₱4,012 + ₱3,890 + ₱4,234 + ₱4,567 + ₱4,890 + ₱5,123 + ₱4,678 + ₱4,345 + ₱3,901 + ₱3,567. Total annual utility cost?",
     3456+3789+4012+3890+4234+4567+4890+5123+4678+4345+3901+3567,
     ["50,452", "50,352", "50,552", "50,252"]),
    ("A warehouse inventory: Electronics (2,345 units), Furniture (1,890 units), Office Supplies (5,678 units), Cleaning Materials (3,456 units), Safety Equipment (1,234 units). Total inventory?",
     2345+1890+5678+3456+1234,
     ["14,603", "14,503", "14,703", "14,403"]),
    ("Travel expenses: Airfare ₱8,500.50; Hotel ₱12,450.00; Meals ₱4,567.75; Transportation ₱2,345.25; Miscellaneous ₱1,890.50. Total travel cost?",
     None, ["29,754.00", "29,654.00", "29,854.00", "29,554.00"]),
    ("A project timeline: Phase 1 takes 45 days, Phase 2 takes 67 days, Phase 3 takes 89 days, Phase 4 takes 34 days, Phase 5 takes 56 days. Total project duration?",
     45+67+89+34+56,
     ["291", "281", "301", "271"]),
]

for q_text, correct_val, ch in hard_word_problems[:10]:
    if correct_val is None:
        correct_str = ch[0]
    else:
        correct_str = f"{correct_val:,}"
        if correct_str not in ch:
            ch[0] = correct_str
    questions.append(make_q(
        "Hard", q_text, ch, correct_str,
        f"Add all values carefully with regrouping. Total: {correct_str}.",
        ["addition", "word problem", "multi-step", "government context"]
    ))


hard_word_problems_2 = [
    ("A government employee earns: Basic ₱25,000; PERA ₱2,000; Overtime ₱5,678.50; Hazard Pay ₱1,500; Night Differential ₱890.75. What is the gross income?",
     None, ["35,069.25", "35,169.25", "34,969.25", "35,269.25"]),
    ("Five municipalities collected taxes: ₱1,234,567; ₱2,345,678; ₱1,890,123; ₱3,456,789; ₱2,678,901. Total provincial tax collection?",
     1234567+2345678+1890123+3456789+2678901,
     ["11,606,058", "11,506,058", "11,706,058", "11,406,058"]),
    ("A hospital admitted patients: ICU (23), Ward A (45), Ward B (67), Ward C (89), ER (34), OPD (156). Total patients?",
     23+45+67+89+34+156,
     ["414", "404", "424", "394"]),
    ("Annual budget breakdown: Salaries ₱45,678,900; Benefits ₱12,345,678; Operations ₱8,901,234; Maintenance ₱5,678,901; Capital ₱15,234,567. Total?",
     45678900+12345678+8901234+5678901+15234567,
     ["87,839,280", "87,739,280", "87,939,280", "87,639,280"]),
    ("A delivery company's weekly distances (km): Mon 234.5, Tue 189.75, Wed 267.8, Thu 145.25, Fri 312.6, Sat 98.5. Total weekly distance?",
     None, ["1,248.40", "1,238.40", "1,258.40", "1,228.40"]),
    ("Inventory additions over 6 months: 1,234; 2,345; 1,567; 3,456; 2,890; 1,789. Total items added?",
     1234+2345+1567+3456+2890+1789,
     ["13,281", "13,181", "13,381", "13,081"]),
    ("A school's book collection by subject: Math (2,345), Science (1,890), English (3,456), Filipino (2,678), Social Studies (1,567), TLE (890). Total books?",
     2345+1890+3456+2678+1567+890,
     ["12,826", "12,726", "12,926", "12,626"]),
    ("Construction materials cost: Cement ₱234,567; Steel ₱456,789; Sand ₱123,456; Gravel ₱189,012; Wood ₱345,678. Total materials cost?",
     234567+456789+123456+189012+345678,
     ["1,349,502", "1,339,502", "1,359,502", "1,329,502"]),
    ("A farmer's harvest (kg): Rice 5,678; Corn 3,456; Vegetables 2,345; Fruits 1,890; Root crops 1,234. Total harvest?",
     5678+3456+2345+1890+1234,
     ["14,603", "14,503", "14,703", "14,403"]),
    ("Government employees by department: DENR (3,456), DepEd (45,678), DOH (12,345), DPWH (8,901), DSWD (5,678). Total employees?",
     3456+45678+12345+8901+5678,
     ["76,058", "75,958", "76,158", "75,858"]),
    ("A company's expenses: Rent ₱45,000; Salaries ₱234,567; Utilities ₱12,345; Supplies ₱8,901; Insurance ₱5,678; Marketing ₱23,456. Total monthly expenses?",
     45000+234567+12345+8901+5678+23456,
     ["329,947", "329,847", "330,047", "329,747"]),
    ("Voter turnout by precinct: P1 (567), P2 (890), P3 (1,234), P4 (456), P5 (789), P6 (1,023), P7 (678). Total voters?",
     567+890+1234+456+789+1023+678,
     ["5,637", "5,537", "5,737", "5,437"]),
    ("A fleet of vehicles consumed fuel (liters): V1 (234.5), V2 (189.75), V3 (312.8), V4 (156.25), V5 (278.9). Total fuel consumption?",
     None, ["1,172.20", "1,162.20", "1,182.20", "1,152.20"]),
    ("Annual rainfall (mm) by month: 123.4, 89.5, 156.7, 234.8, 312.9, 278.6, 345.2, 289.1, 267.3, 198.4, 145.6, 112.3. Total annual rainfall?",
     None, ["2,553.80", "2,543.80", "2,563.80", "2,533.80"]),
    ("A payroll has 8 employees earning: ₱18,500; ₱22,000; ₱19,750; ₱25,000; ₱21,500; ₱23,450; ₱20,800; ₱24,000. Total payroll?",
     18500+22000+19750+25000+21500+23450+20800+24000,
     ["175,000", "174,000", "176,000", "173,000"]),
    ("Infrastructure projects: Road (₱12,345,678), Bridge (₱8,901,234), School (₱5,678,901), Hospital (₱15,234,567), Water System (₱3,456,789). Total infrastructure budget?",
     12345678+8901234+5678901+15234567+3456789,
     ["45,617,169", "45,517,169", "45,717,169", "45,417,169"]),
    ("A census counts households: Urban (23,456), Suburban (15,678), Rural (34,567), Coastal (8,901), Mountain (5,234). Total households?",
     23456+15678+34567+8901+5234,
     ["87,836", "87,736", "87,936", "87,636"]),
    ("Daily transactions: Mon (1,234), Tue (2,345), Wed (1,890), Thu (2,567), Fri (3,456). Weekly total?",
     1234+2345+1890+2567+3456,
     ["11,492", "11,392", "11,592", "11,292"]),
    ("A warehouse ships: Week 1 (4,567 units), Week 2 (5,678 units), Week 3 (3,890 units), Week 4 (6,234 units). Monthly shipments?",
     4567+5678+3890+6234,
     ["20,369", "20,269", "20,469", "20,169"]),
    ("Tax collections by type: Income Tax ₱45,678,901; VAT ₱34,567,890; Excise ₱12,345,678; Customs ₱23,456,789. Total tax revenue?",
     45678901+34567890+12345678+23456789,
     ["116,049,258", "115,949,258", "116,149,258", "115,849,258"]),
]

for q_text, correct_val, ch in hard_word_problems_2:
    if correct_val is None:
        correct_str = ch[0]
    else:
        correct_str = f"{correct_val:,}"
        if correct_str not in ch:
            ch[0] = correct_str
    questions.append(make_q(
        "Hard", q_text, ch, correct_str,
        f"Sum all given values carefully. Total: {correct_str}.",
        ["addition", "word problem", "multi-step", "government context"]
    ))


# --- Hard: Three-fraction addition - 15 questions ---
hard_three_fractions = [
    (1, 3, 1, 4, 1, 5), (2, 5, 3, 7, 1, 2), (3, 8, 5, 12, 1, 6),
    (4, 9, 2, 3, 5, 18), (7, 10, 3, 5, 1, 4), (5, 6, 2, 9, 1, 3),
    (3, 7, 4, 21, 2, 3), (1, 8, 3, 4, 5, 6), (2, 15, 4, 5, 1, 3),
    (7, 12, 5, 8, 1, 6), (3, 10, 7, 15, 2, 5), (4, 7, 3, 14, 5, 7),
    (5, 9, 1, 6, 7, 18), (2, 11, 5, 22, 3, 11), (8, 15, 3, 10, 1, 6)
]

for n1, d1, n2, d2, n3, d3 in hard_three_fractions:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    f3 = Fraction(n3, d3)
    correct = f1 + f2 + f3
    correct_str = format_fraction(correct)
    dists = fraction_distractors(correct)
    choices = [correct_str] + dists
    random.shuffle(choices)
    from math import lcm
    lcd12 = lcm(d1, d2)
    lcd_all = lcm(lcd12, d3)
    exp = f"LCD of {d1}, {d2}, {d3} = {lcd_all}. Convert all fractions, add numerators, simplify: {correct_str}."
    questions.append(make_q(
        "Hard",
        f"What is {n1}/{d1} + {n2}/{d2} + {n3}/{d3}?",
        choices,
        correct_str,
        exp,
        ["addition", "fractions", "three fractions", "complex"]
    ))

# --- Hard: Mixed operations conceptual - 15 questions ---
hard_conceptual = [
    ("If a + 567 = 1,234, what is the value of a?",
     ["667", "657", "677", "647"], "667",
     "a = 1,234 - 567 = 667. Verify: 667 + 567 = 1,234. ✓"),
    ("The sum of three consecutive integers is 99. What is the largest integer?",
     ["34", "33", "35", "32"], "34",
     "Let the integers be n, n+1, n+2. Sum: 3n+3=99, 3n=96, n=32. Largest: 32+2=34."),
    ("If x + y = 45 and x = 23, what is x + y + 55?",
     ["100", "95", "105", "90"], "100",
     "x + y = 45. Therefore x + y + 55 = 45 + 55 = 100."),
    ("What must be added to 3/8 to get 1?",
     ["5/8", "3/8", "1/8", "7/8"], "5/8",
     "1 - 3/8 = 8/8 - 3/8 = 5/8. Verify: 3/8 + 5/8 = 8/8 = 1. ✓"),
    ("The sum of two numbers is 1,000. One number is 378. What is the other?",
     ["622", "612", "632", "628"], "622",
     "Other number = 1,000 - 378 = 622. Verify: 378 + 622 = 1,000. ✓"),
    ("What is the sum of the first 10 positive integers?",
     ["55", "45", "50", "60"], "55",
     "Sum = n(n+1)/2 = 10(11)/2 = 55. Or: 1+2+3+4+5+6+7+8+9+10 = 55."),
    ("If adding 0.75 to a number gives 3.25, what is the number?",
     ["2.50", "2.75", "2.25", "3.00"], "2.50",
     "Number = 3.25 - 0.75 = 2.50. Verify: 2.50 + 0.75 = 3.25. ✓"),
    ("The sum of two consecutive even numbers is 54. What are the numbers?",
     ["26 and 28", "24 and 30", "22 and 32", "25 and 29"], "26 and 28",
     "Let numbers be n and n+2. n + n+2 = 54, 2n = 52, n = 26. Numbers: 26 and 28."),
    ("What is (-25) + (-25) + 50?",
     ["0", "-50", "50", "25"], "0",
     "(-25) + (-25) = -50. Then -50 + 50 = 0."),
    ("A number increased by 2/3 of itself equals 50. What is the number?",
     ["30", "25", "35", "20"], "30",
     "n + (2/3)n = 50. (5/3)n = 50. n = 50 × 3/5 = 30. Verify: 30 + 20 = 50. ✓"),
    ("What is the sum of all odd numbers from 1 to 19?",
     ["100", "90", "110", "95"], "100",
     "Odd numbers: 1,3,5,7,9,11,13,15,17,19. Count=10. Sum = 10² = 100."),
    ("If the sum of 5 numbers is 250, and four of them are 45, 67, 38, and 52, what is the fifth?",
     ["48", "58", "38", "68"], "48",
     "Fifth = 250 - (45+67+38+52) = 250 - 202 = 48."),
    ("What is 999 + 99 + 9?",
     ["1,107", "1,097", "1,117", "1,207"], "1,107",
     "999 + 99 = 1,098. 1,098 + 9 = 1,107."),
    ("The sum of a number and its additive inverse is always:",
     ["0", "1", "The number itself", "Undefined"], "0",
     "A number plus its additive inverse (opposite) always equals 0: n + (-n) = 0."),
    ("What is 1/2 + 1/3 + 1/6?",
     ["1", "5/6", "2/3", "11/6"], "1",
     "LCD=6. 1/2=3/6, 1/3=2/6, 1/6=1/6. Sum: 3/6+2/6+1/6 = 6/6 = 1."),
]

for q_text, ch, ans, exp in hard_conceptual:
    questions.append(make_q(
        "Hard", q_text, ch, ans, exp,
        ["addition", "conceptual", "problem solving"]
    ))


# ============================================================
# OUTPUT
# ============================================================

# Count by difficulty
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Generated questions: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}, Total={len(questions)}")

# If we have fewer than 600, we need to pad. Let's check and add more if needed.
# We'll generate additional questions to reach exactly 200 per difficulty.

def pad_easy(target=200):
    """Generate additional easy questions to reach target."""
    current = sum(1 for q in questions if q["difficulty"] == "Easy")
    needed = target - current
    if needed <= 0:
        return
    random.seed(600)
    for i in range(needed):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        correct = a + b
        dists = generate_distractors_int(correct)
        choices = [str(correct)] + [str(d) for d in dists]
        random.shuffle(choices)
        questions.append(make_q(
            "Easy",
            f"What is {a} + {b}?",
            choices,
            str(correct),
            f"Add: {a} + {b} = {correct}.",
            ["addition", "whole numbers", "two-digit"]
        ))


def pad_medium(target=200):
    """Generate additional medium questions to reach target."""
    current = sum(1 for q in questions if q["difficulty"] == "Medium")
    needed = target - current
    if needed <= 0:
        return
    random.seed(700)
    for i in range(needed):
        a = random.randint(100, 9999)
        b = random.randint(100, 9999)
        correct = a + b
        dists = generate_distractors_int(correct)
        choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
        random.shuffle(choices)
        questions.append(make_q(
            "Medium",
            f"What is {a:,} + {b:,}?",
            choices,
            f"{correct:,}",
            f"Add with regrouping: {a:,} + {b:,} = {correct:,}.",
            ["addition", "whole numbers", "computation"]
        ))


def pad_hard(target=200):
    """Generate additional hard questions to reach target."""
    current = sum(1 for q in questions if q["difficulty"] == "Hard")
    needed = target - current
    if needed <= 0:
        return
    random.seed(800)
    for i in range(needed):
        nums = [random.randint(1000, 99999) for _ in range(random.randint(2, 4))]
        correct = sum(nums)
        dists = generate_distractors_int(correct, spread=100)
        nums_str = " + ".join(f"{n:,}" for n in nums)
        choices = [f"{correct:,}"] + [f"{d:,}" for d in dists]
        random.shuffle(choices)
        questions.append(make_q(
            "Hard",
            f"What is {nums_str}?",
            choices,
            f"{correct:,}",
            f"Add all numbers: {correct:,}.",
            ["addition", "whole numbers", "large numbers", "multiple addends"]
        ))


pad_easy(200)
pad_medium(200)
pad_hard(200)

# Final count
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final count: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}, Total={len(questions)}")

# Reassign IDs sequentially
for i, q in enumerate(questions, 1):
    q["id"] = i

# Write output
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          "data", "seed", "questions", "numerical-ability",
                          "basic-operations", "addition")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "questions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
