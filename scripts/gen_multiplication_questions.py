"""
Generate 600 multiplication questions for the CSE Numerical Ability section.
200 Easy / 200 Medium / 200 Hard
"""

import json
import random
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
        "module": "Basic Operations",
        "subtopic": "Multiplication",
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
        return f"{n:,.2f}".rstrip('0').rstrip('.')
    return f"{n:,}"


def make_choices_int(correct, spread=None):
    """Generate 4 choices for an integer answer."""
    if spread is None:
        spread = max(5, abs(correct) // 8)
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
    choices = [str(correct)] + [str(d) for d in distractors]
    random.shuffle(choices)
    return [fmt(int(c)) if c.lstrip('-').isdigit() else c for c in choices], fmt(correct)


def make_choices_decimal(correct):
    """Generate 4 choices for a decimal answer."""
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        offset = random.choice([-0.3, -0.2, -0.1, 0.1, 0.2, 0.3, -1, 1, -0.5, 0.5])
        if abs(correct) > 10:
            offset *= 10
        d = round(correct + offset, 4)
        if d != correct and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < 3:
        distractors.add(round(correct + (len(distractors) + 1) * 0.1, 4))
    choices = [str(correct)] + [str(d) for d in distractors]
    random.shuffle(choices)
    return choices, str(correct)


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
    attempts = 0
    n, d = correct_frac.numerator, correct_frac.denominator
    candidates = [
        Fraction(n + 1, d), Fraction(n - 1, d) if n > 1 else Fraction(n + 2, d),
        Fraction(n, d + 1), Fraction(n, d - 1) if d > 1 else Fraction(n, d + 2),
        Fraction(n + 1, d + 1), Fraction(n * 2, d),
        Fraction(n, d * 2), Fraction(n + 2, d),
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

# --- Easy: Whole number multiplication (1-50) ---
easy_whole_pairs = [
    (7, 8), (9, 6), (12, 5), (15, 4), (11, 7), (8, 9), (6, 12),
    (13, 3), (14, 6), (16, 5), (18, 4), (9, 9), (7, 12), (8, 11),
    (5, 15), (17, 3), (19, 5), (20, 4), (6, 14), (11, 9),
    (23, 4), (25, 3), (21, 5), (12, 8), (15, 7), (24, 3), (13, 6),
    (16, 4), (22, 5), (10, 13), (9, 11), (8, 15), (7, 14), (6, 16),
    (14, 5), (18, 3), (20, 6), (11, 11), (12, 12), (25, 4),
]

for a, b in easy_whole_pairs[:40]:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Easy",
          f"What is {a} × {b}?",
          choices, ans,
          f"Multiply {a} by {b}: {a} × {b} = {fmt(product)}.",
          ["multiplication", "whole numbers", "basic computation"])

# --- Easy: Multiply by 10, 100 (41-55) ---
mult10_nums = [34, 56, 78, 125, 250, 47, 63, 89, 15, 92, 145, 208, 37, 64, 81]
for i, n in enumerate(mult10_nums):
    mult = random.choice([10, 100]) if i > 5 else 10
    product = n * mult
    choices, ans = make_choices_int(product)
    add_q("Easy",
          f"What is {n} × {mult}?",
          choices, ans,
          f"Multiplying by {mult} moves the decimal point {'one' if mult == 10 else 'two'} place(s) to the right: {n} × {mult} = {fmt(product)}.",
          ["multiplication", "whole numbers", "powers of 10"])

# --- Easy: Simple integer multiplication (56-80) ---
easy_int_pairs = [
    (-3, 5), (-4, 6), (-7, 2), (-8, 3), (-5, 9),
    (-2, -6), (-3, -4), (-5, -5), (-7, -3), (-9, -2),
    (4, -8), (6, -3), (9, -4), (5, -7), (3, -11),
    (-6, 8), (-4, 9), (-10, 5), (-2, 12), (-8, 4),
    (-1, 15), (-3, -9), (7, -6), (-5, 8), (-4, -7),
]

for a, b in easy_int_pairs:
    product = a * b
    sign_explain = "Same signs → positive" if (a > 0 and b > 0) or (a < 0 and b < 0) else "Different signs → negative"
    choices, ans = make_choices_int(product)
    add_q("Easy",
          f"What is ({a}) × ({b})?",
          choices, ans,
          f"{sign_explain}. |{abs(a)}| × |{abs(b)}| = {abs(product)}. Answer: {product}.",
          ["multiplication", "integers", "sign rules"])

# --- Easy: Simple decimal multiplication (81-110) ---
easy_dec_pairs = [
    (0.5, 6), (0.3, 7), (0.4, 8), (0.2, 9), (0.6, 5),
    (1.5, 4), (2.5, 6), (3.5, 2), (4.5, 8), (0.8, 5),
    (1.2, 5), (2.4, 3), (0.9, 9), (1.1, 7), (0.7, 6),
    (2.5, 4), (1.5, 8), (3.2, 5), (0.25, 4), (0.5, 12),
    (1.5, 6), (2.5, 8), (0.4, 15), (0.6, 12), (1.25, 4),
    (0.75, 8), (2.5, 10), (0.5, 14), (1.5, 10), (3.5, 4),
]

for a, b in easy_dec_pairs:
    product = round(a * b, 4)
    dp_a = len(str(a).split('.')[-1]) if '.' in str(a) else 0
    dp_b = len(str(b).split('.')[-1]) if '.' in str(b) else 0
    choices, ans = make_choices_decimal(product)
    add_q("Easy",
          f"What is {a} × {b}?",
          choices, ans,
          f"Multiply: {a} × {b} = {product}. Total decimal places: {dp_a + dp_b}.",
          ["multiplication", "decimals", "basic computation"])


# --- Easy: Simple fraction multiplication (111-140) ---
easy_frac_pairs = [
    ((1, 2), (1, 3)), ((1, 4), (1, 2)), ((2, 3), (3, 4)),
    ((1, 5), (5, 6)), ((3, 4), (2, 3)), ((1, 3), (3, 5)),
    ((2, 5), (5, 8)), ((1, 6), (3, 4)), ((4, 5), (1, 2)),
    ((1, 2), (2, 5)), ((3, 8), (4, 9)), ((2, 7), (7, 8)),
    ((5, 6), (3, 5)), ((1, 4), (4, 7)), ((3, 5), (5, 9)),
    ((1, 3), (6, 7)), ((2, 9), (3, 4)), ((4, 5), (5, 8)),
    ((1, 2), (4, 5)), ((3, 7), (7, 9)), ((5, 8), (2, 5)),
    ((1, 6), (2, 3)), ((4, 9), (3, 8)), ((2, 3), (9, 10)),
    ((7, 8), (4, 7)), ((5, 6), (2, 5)), ((3, 4), (8, 9)),
    ((1, 5), (10, 11)), ((2, 3), (3, 8)), ((5, 9), (3, 5)),
]

for (n1, d1), (n2, d2) in easy_frac_pairs:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    product = f1 * f2
    choices, ans = make_choices_fraction(product)
    add_q("Easy",
          f"What is {n1}/{d1} × {n2}/{d2}?",
          choices, ans,
          f"Multiply numerators: {n1} × {n2} = {n1*n2}. Multiply denominators: {d1} × {d2} = {d1*d2}. Result: {n1*n2}/{d1*d2} = {frac_str(product)}.",
          ["multiplication", "fractions", "basic computation"])

# --- Easy: Word problems (141-170) ---
easy_word_problems = [
    ("A box contains 24 pencils. How many pencils are in 5 boxes?", 24, 5, "pencils", "boxes"),
    ("Each folder costs ₱18. How much do 12 folders cost?", 18, 12, "pesos", "cost"),
    ("A bus carries 45 passengers per trip. How many passengers in 6 trips?", 45, 6, "passengers", "trips"),
    ("A worker earns ₱500 per day. How much does he earn in 7 days?", 500, 7, "pesos", "salary"),
    ("There are 8 rows of chairs with 15 chairs per row. How many chairs in total?", 8, 15, "chairs", "arrangement"),
    ("A pack has 36 sheets of paper. How many sheets in 4 packs?", 36, 4, "sheets", "supplies"),
    ("Each student needs 3 notebooks. How many notebooks for 28 students?", 3, 28, "notebooks", "supplies"),
    ("A carton holds 48 cans. How many cans in 9 cartons?", 48, 9, "cans", "inventory"),
    ("An employee types 65 words per minute. How many words in 8 minutes?", 65, 8, "words", "productivity"),
    ("A garden has 12 rows with 9 plants each. How many plants total?", 12, 9, "plants", "arrangement"),
    ("Each bag of rice weighs 25 kg. What is the total weight of 14 bags?", 25, 14, "kg", "weight"),
    ("A printer prints 35 pages per minute. How many pages in 6 minutes?", 35, 6, "pages", "productivity"),
    ("There are 7 classes with 40 students each. How many students total?", 7, 40, "students", "school"),
    ("A taxi charges ₱13 per km. How much for a 15-km ride?", 13, 15, "pesos", "transportation"),
    ("Each shelf holds 22 books. How many books on 8 shelves?", 22, 8, "books", "library"),
    ("A factory produces 150 units per hour. How many in 5 hours?", 150, 5, "units", "production"),
    ("Each tile is 4 cm wide. What is the width of 16 tiles placed side by side?", 4, 16, "cm", "measurement"),
    ("A nurse checks 11 patients per hour. How many in a 9-hour shift?", 11, 9, "patients", "healthcare"),
    ("Each box of markers contains 8 markers. How many markers in 25 boxes?", 8, 25, "markers", "supplies"),
    ("A delivery truck makes 6 trips per day carrying 75 packages each. How many packages daily?", 6, 75, "packages", "logistics"),
    ("A government office uses 14 reams of paper per week. How many reams in 4 weeks?", 14, 4, "reams", "office supplies"),
    ("Each classroom has 5 ceiling fans. How many fans in 18 classrooms?", 5, 18, "fans", "facilities"),
    ("A canteen serves 120 meals per day. How many meals in 6 days?", 120, 6, "meals", "food service"),
    ("Each envelope costs ₱3. How much for 85 envelopes?", 3, 85, "pesos", "office supplies"),
    ("A parking lot has 9 levels with 55 slots each. How many total slots?", 9, 55, "slots", "facilities"),
    ("A teacher grades 32 papers per hour. How many in 4 hours?", 32, 4, "papers", "education"),
    ("Each pack of batteries contains 6 pieces. How many batteries in 15 packs?", 6, 15, "batteries", "supplies"),
    ("A jogger runs 3 km per day. How many km in 25 days?", 3, 25, "km", "fitness"),
    ("A store sells 45 bottles of water per day. How many in 8 days?", 45, 8, "bottles", "sales"),
    ("Each floor of a building has 12 offices. How many offices in a 7-floor building?", 12, 7, "offices", "building"),
]

for text, a, b, unit, context in easy_word_problems:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Easy",
          text,
          choices, ans,
          f"Multiply: {a} × {b} = {fmt(product)} {unit}.",
          ["multiplication", "word problem", context])

# --- Easy: Multiply by 5 and 25 shortcuts (171-185) ---
mult5_nums = [18, 24, 36, 42, 56, 64, 72, 88, 96, 14, 32, 48, 66, 78, 84]
for n in mult5_nums:
    mult = 5
    product = n * mult
    choices, ans = make_choices_int(product)
    add_q("Easy",
          f"What is {n} × 5?",
          choices, ans,
          f"Shortcut: {n} × 10 = {n*10}, then divide by 2: {n*10} ÷ 2 = {product}.",
          ["multiplication", "whole numbers", "mental math"])

# --- Easy: Fill remaining to reach 200 with varied simple problems (186-200) ---
easy_extra = [
    (30, 7), (50, 9), (40, 8), (60, 6), (70, 5),
    (80, 4), (90, 3), (25, 8), (35, 6), (45, 7),
    (55, 4), (65, 3), (75, 8), (85, 2), (95, 6),
]
for a, b in easy_extra:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Easy",
          f"What is {a} × {b}?",
          choices, ans,
          f"{a} × {b} = {fmt(product)}.",
          ["multiplication", "whole numbers", "basic computation"])


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Multi-digit whole number multiplication (201-235) ---
med_whole_pairs = [
    (47, 36), (58, 43), (63, 27), (84, 56), (92, 38),
    (76, 45), (53, 67), (89, 24), (37, 85), (64, 73),
    (125, 16), (48, 95), (156, 12), (234, 8), (67, 54),
    (78, 39), (145, 23), (96, 47), (83, 62), (57, 88),
    (112, 25), (75, 64), (168, 15), (93, 46), (54, 78),
    (135, 24), (87, 53), (246, 9), (65, 72), (148, 17),
    (256, 13), (79, 48), (185, 22), (94, 56), (123, 45),
]

for a, b in med_whole_pairs:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Medium",
          f"What is {a} × {b}?",
          choices, ans,
          f"Using long multiplication: {a} × {b} = {fmt(product)}.",
          ["multiplication", "whole numbers", "long multiplication"])

# --- Medium: Integer multiplication with multiple factors (236-260) ---
med_int_problems = [
    ((-6), 7, (-3)), ((-4), (-5), 8), (9, (-7), (-2)),
    ((-3), (-8), (-2)), ((-5), 4, (-6)), ((-12), (-3), None),
    ((-15), 8, None), (7, (-13), None), ((-9), (-11), None),
    ((-25), 4, None), ((-6), (-6), (-6)), ((-2), (-3), (-4)),
    (5, (-8), 3), ((-7), 4, (-5)), ((-10), (-10), None),
    ((-14), 6, None), ((-8), (-9), None), (11, (-12), None),
    ((-3), (-5), (-7)), ((-4), 9, (-2)), (6, (-8), (-3)),
    ((-2), (-2), (-2), (-2)), ((-5), (-5), None), ((-13), 7, None),
    ((-16), (-4), None),
]

for item in med_int_problems:
    if len(item) == 3 and item[2] is not None:
        a, b, c = item
        product = a * b * c
        negs = sum(1 for x in [a, b, c] if x < 0)
        sign_rule = "even negatives → positive" if negs % 2 == 0 else "odd negatives → negative"
        choices, ans = make_choices_int(product)
        add_q("Medium",
              f"What is ({a}) × ({b}) × ({c})?",
              choices, ans,
              f"Count negatives: {negs} ({sign_rule}). |{abs(a)}| × |{abs(b)}| × |{abs(c)}| = {abs(product)}. Answer: {product}.",
              ["multiplication", "integers", "multiple factors"])
    elif len(item) == 4:
        a, b, c, d = item
        product = a * b * c * d
        negs = sum(1 for x in [a, b, c, d] if x < 0)
        sign_rule = "even negatives → positive" if negs % 2 == 0 else "odd negatives → negative"
        choices, ans = make_choices_int(product)
        add_q("Medium",
              f"What is ({a}) × ({b}) × ({c}) × ({d})?",
              choices, ans,
              f"Count negatives: {negs} ({sign_rule}). Product of absolutes = {abs(product)}. Answer: {product}.",
              ["multiplication", "integers", "multiple factors"])
    else:
        a, b = item[0], item[1]
        product = a * b
        sign_rule = "Same signs → positive" if (a > 0 and b > 0) or (a < 0 and b < 0) else "Different signs → negative"
        choices, ans = make_choices_int(product)
        add_q("Medium",
              f"What is ({a}) × ({b})?",
              choices, ans,
              f"{sign_rule}. |{abs(a)}| × |{abs(b)}| = {abs(product)}. Answer: {product}.",
              ["multiplication", "integers", "sign rules"])

# --- Medium: Decimal multiplication (261-295) ---
med_dec_pairs = [
    (3.4, 2.7), (5.6, 4.3), (0.45, 0.6), (1.25, 3.2), (7.8, 0.15),
    (2.75, 1.6), (0.35, 2.4), (4.5, 3.8), (6.25, 0.16), (0.125, 8),
    (9.5, 0.4), (1.75, 2.8), (0.65, 1.4), (3.25, 0.8), (8.4, 0.25),
    (2.5, 3.6), (0.48, 2.5), (5.75, 0.4), (1.35, 0.6), (4.8, 1.25),
    (0.75, 4.4), (6.5, 0.12), (2.25, 3.2), (0.85, 0.4), (7.5, 0.08),
    (3.6, 2.5), (1.44, 0.5), (0.36, 2.5), (4.25, 0.8), (9.2, 0.15),
    (2.8, 3.5), (0.55, 1.8), (6.4, 0.75), (1.6, 4.5), (8.5, 0.12),
]

for a, b in med_dec_pairs:
    product = round(a * b, 4)
    # Remove trailing zeros for display
    product_str = f"{product:.4f}".rstrip('0').rstrip('.')
    product_display = float(product_str)
    choices, ans = make_choices_decimal(product_display)
    add_q("Medium",
          f"What is {a} × {b}?",
          choices, ans,
          f"Multiply as whole numbers, then place decimal. {a} × {b} = {product_display}.",
          ["multiplication", "decimals", "computation"])


# --- Medium: Fraction multiplication including mixed numbers (296-335) ---
med_frac_pairs = [
    # proper × proper requiring simplification
    ((5, 6), (9, 10)), ((7, 12), (8, 21)), ((4, 9), (3, 8)),
    ((5, 8), (6, 15)), ((7, 10), (5, 14)), ((9, 16), (4, 3)),
    ((8, 15), (5, 12)), ((11, 12), (6, 11)), ((3, 14), (7, 9)),
    ((10, 21), (7, 15)),
    # mixed × whole
    ((7, 3), (5, 1)),  # 2 1/3 × 5 as improper
    ((9, 4), (4, 1)),  # 2 1/4 × 4
    ((11, 5), (10, 1)),  # 2 1/5 × 10
    ((7, 2), (6, 1)),  # 3 1/2 × 6
    ((13, 4), (8, 1)),  # 3 1/4 × 8
    # mixed × mixed
    ((5, 2), (7, 3)),  # 2 1/2 × 2 1/3
    ((7, 4), (8, 5)),  # 1 3/4 × 1 3/5
    ((10, 3), (9, 4)),  # 3 1/3 × 2 1/4
    ((11, 6), (12, 5)),  # 1 5/6 × 2 2/5
    ((9, 2), (5, 3)),  # 4 1/2 × 1 2/3
    # proper × proper
    ((5, 9), (3, 10)), ((7, 8), (4, 21)), ((6, 7), (14, 15)),
    ((8, 9), (3, 16)), ((11, 15), (5, 22)), ((4, 7), (21, 8)),
    ((9, 14), (7, 12)), ((5, 12), (8, 15)), ((13, 20), (4, 13)),
    ((7, 15), (10, 21)),
    # more mixed numbers
    ((15, 4), (8, 3)),  # 3 3/4 × 2 2/3
    ((11, 3), (9, 2)),  # 3 2/3 × 4 1/2
    ((17, 5), (5, 4)),  # 3 2/5 × 1 1/4
    ((8, 3), (15, 8)),  # 2 2/3 × 1 7/8
    ((13, 6), (12, 7)),  # 2 1/6 × 1 5/7
    ((7, 5), (25, 7)),  # 1 2/5 × 3 4/7
    ((16, 9), (3, 4)),  # 1 7/9 × 3/4
    ((14, 5), (15, 7)),  # 2 4/5 × 2 1/7
    ((9, 7), (14, 9)),  # 1 2/7 × 1 5/9
    ((22, 5), (5, 11)),  # 4 2/5 × 5/11
]

for (n1, d1), (n2, d2) in med_frac_pairs:
    f1 = Fraction(n1, d1)
    f2 = Fraction(n2, d2)
    product = f1 * f2

    # Display as mixed numbers if > 1 for the factors
    def display_frac(n, d):
        if n > d and d > 1:
            whole = n // d
            rem = n % d
            if rem == 0:
                return str(whole)
            return f"{whole} {rem}/{d}"
        if d == 1:
            return str(n)
        return f"{n}/{d}"

    f1_display = display_frac(n1, d1)
    f2_display = display_frac(n2, d2)

    choices, ans = make_choices_fraction(product)
    add_q("Medium",
          f"What is {f1_display} × {f2_display}?",
          choices, ans,
          f"Convert to improper fractions if needed: {n1}/{d1} × {n2}/{d2} = {n1*n2}/{d1*d2} = {frac_str(product)}.",
          ["multiplication", "fractions", "mixed numbers"])

# --- Medium: Word problems (336-380) ---
med_word_problems = [
    ("A government employee earns ₱685 per day. How much does she earn in 22 working days?",
     685, 22, "₱", "salary"),
    ("An office orders 36 boxes of folders at ₱245 per box. What is the total cost?",
     36, 245, "₱", "procurement"),
    ("A school bus makes 4 trips daily, carrying 56 students per trip. How many students are transported daily?",
     4, 56, "", "transportation"),
    ("A warehouse stores 125 cartons per shelf. If there are 48 shelves, how many cartons can be stored?",
     125, 48, "", "inventory"),
    ("Each government form requires 3 pages. How many pages are needed for 475 forms?",
     3, 475, "", "office supplies"),
    ("A water tank holds 250 liters. How many liters do 18 tanks hold?",
     250, 18, "", "capacity"),
    ("A clerk processes 78 applications per day. How many applications in 15 working days?",
     78, 15, "", "productivity"),
    ("Each relief pack costs ₱365. How much is needed for 240 families?",
     365, 240, "₱", "disaster relief"),
    ("A building has 14 floors with 26 rooms per floor. How many rooms total?",
     14, 26, "", "facilities"),
    ("A government vehicle travels 45 km per day. How far does it travel in 24 days?",
     45, 24, "km", "transportation"),
    ("An agency prints 1,250 copies of a report. Each copy uses 28 pages. How many pages total?",
     1250, 28, "", "printing"),
    ("A canteen serves 185 meals per day. How many meals in 26 working days?",
     185, 26, "", "food service"),
    ("Each training session accommodates 35 participants. How many participants in 16 sessions?",
     35, 16, "", "training"),
    ("A municipality has 67 barangays. Each barangay has 145 registered voters. How many voters total?",
     67, 145, "", "government"),
    ("A hospital uses 96 syringes per day. How many syringes in 30 days?",
     96, 30, "", "healthcare"),
    ("An employee's monthly salary is ₱28,500. What is the annual salary?",
     28500, 12, "₱", "salary"),
    ("A library acquires 45 new books per month. How many books in 8 months?",
     45, 8, "", "library"),
    ("Each computer costs ₱32,500. How much for 15 computers?",
     32500, 15, "₱", "procurement"),
    ("A road project covers 8 km per month. How many km in 14 months?",
     8, 14, "km", "infrastructure"),
    ("A call center handles 235 calls per agent per day. How many calls do 12 agents handle?",
     235, 12, "", "productivity"),
]

for text, a, b, prefix, context in med_word_problems[:20]:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Medium",
          text,
          choices, ans,
          f"Multiply: {a} × {b} = {fmt(product)}. Total: {prefix}{fmt(product)}.",
          ["multiplication", "word problem", context])


# --- Medium: Decimal word problems (381-400) ---
med_dec_word = [
    ("An item costs ₱45.75. How much do 8 items cost?", 45.75, 8, "₱"),
    ("A worker earns ₱87.50 per hour. How much for 6.5 hours?", 87.50, 6.5, "₱"),
    ("Gasoline costs ₱65.25 per liter. How much for 12 liters?", 65.25, 12, "₱"),
    ("A ribbon is 2.5 meters long. What is the total length of 14 ribbons?", 2.5, 14, ""),
    ("Each tile weighs 1.75 kg. What is the weight of 24 tiles?", 1.75, 24, ""),
    ("A pipe is 3.25 meters long. What is the total length of 8 pipes?", 3.25, 8, ""),
    ("Electricity costs ₱9.85 per kWh. What is the cost of 150 kWh?", 9.85, 150, "₱"),
    ("A car travels 12.5 km per liter. How far on 32 liters?", 12.5, 32, ""),
    ("Each bag of cement weighs 42.5 kg. What is the weight of 16 bags?", 42.5, 16, ""),
    ("A daily allowance is ₱175.50. How much for 20 days?", 175.50, 20, "₱"),
    ("Water costs ₱35.75 per cubic meter. What is the cost of 8.5 cubic meters?", 35.75, 8.5, "₱"),
    ("A rod is 0.75 meters long. What is the total length of 36 rods?", 0.75, 36, ""),
    ("Each notebook costs ₱28.50. How much for 15 notebooks?", 28.50, 15, "₱"),
    ("A vehicle uses 0.08 liters per km. How much fuel for 225 km?", 0.08, 225, ""),
    ("Overtime rate is 1.5 times ₱95.00 per hour. What is the overtime rate?", 1.5, 95, "₱"),
    ("A plot measures 12.5 m by 8.4 m. What is the area?", 12.5, 8.4, ""),
    ("Each pack weighs 2.25 kg. What is the total weight of 18 packs?", 2.25, 18, ""),
    ("A discount is 0.15 of ₱2,450. How much is the discount?", 0.15, 2450, "₱"),
    ("Tax rate is 0.12 of ₱15,800. How much is the tax?", 0.12, 15800, "₱"),
    ("A commission is 0.05 of ₱125,000. How much is the commission?", 0.05, 125000, "₱"),
]

for text, a, b, prefix in med_dec_word:
    product = round(a * b, 2)
    choices, ans = make_choices_decimal(product)
    add_q("Medium",
          text,
          choices, ans,
          f"Multiply: {a} × {b} = {product}.",
          ["multiplication", "decimals", "word problem"])

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Large number multiplication (401-425) ---
hard_whole_pairs = [
    (478, 263), (567, 348), (892, 456), (345, 678), (729, 534),
    (1250, 864), (2345, 67), (456, 789), (1875, 48), (3456, 23),
    (678, 945), (1234, 56), (987, 654), (2468, 35), (5678, 19),
    (834, 567), (1456, 78), (2789, 34), (4567, 25), (6789, 13),
    (375, 248), (1568, 45), (2345, 89), (768, 432), (1890, 56),
]

for a, b in hard_whole_pairs:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Hard",
          f"What is {fmt(a)} × {fmt(b)}?",
          choices, ans,
          f"Long multiplication: {fmt(a)} × {fmt(b)} = {fmt(product)}.",
          ["multiplication", "whole numbers", "large numbers"])

# --- Hard: Complex integer problems (426-450) ---
hard_int_problems = [
    ("What is (-15) × (-8) × (-3)?", -15 * -8 * -3),
    ("What is (-7) × 12 × (-4) × (-2)?", -7 * 12 * -4 * -2),
    ("What is (-25) × (-4) × 6?", -25 * -4 * 6),
    ("What is 13 × (-9) × (-5)?", 13 * -9 * -5),
    ("What is (-6)³?", (-6)**3),
    ("What is (-3)⁴?", (-3)**4),
    ("What is (-2)⁵?", (-2)**5),
    ("What is (-5)² × (-2)³?", (-5)**2 * (-2)**3),
    ("What is (-4)² × (-3)² × (-1)?", (-4)**2 * (-3)**2 * (-1)),
    ("What is (-8) × (-7) × (-5) × (-1)?", -8 * -7 * -5 * -1),
    ("What is (-12) × 15 × (-2)?", -12 * 15 * -2),
    ("What is (-9) × (-9) × (-9)?", (-9)**3),
    ("What is (-2)⁶?", (-2)**6),
    ("What is (-7)² × 3?", (-7)**2 * 3),
    ("What is (-4) × (-5) × (-6) × (-2)?", -4 * -5 * -6 * -2),
    ("What is (-11) × (-11)?", (-11)**2),
    ("What is (-3) × (-7) × 4 × (-2)?", -3 * -7 * 4 * -2),
    ("What is (-15) × (-4) × (-5)?", -15 * -4 * -5),
    ("What is (-8)² × (-2)?", (-8)**2 * (-2)),
    ("What is (-6) × (-6) × (-6) × (-6)?", (-6)**4),
    ("What is (-13) × 7 × (-3)?", -13 * 7 * -3),
    ("What is (-2) × (-3) × (-5) × (-7)?", -2 * -3 * -5 * -7),
    ("What is (-10)³?", (-10)**3),
    ("What is (-4)³ × (-1)?", (-4)**3 * (-1)),
    ("What is (-5) × (-5) × (-5) × (-5)?", (-5)**4),
]

for text, product in hard_int_problems:
    choices, ans = make_choices_int(product)
    negs_text = "positive" if product > 0 else "negative"
    add_q("Hard",
          text,
          choices, ans,
          f"Apply sign rules and compute. The product is {negs_text}: {product}.",
          ["multiplication", "integers", "exponents"])


# --- Hard: Complex decimal multiplication (451-480) ---
hard_dec_pairs = [
    (0.045, 0.06), (2.875, 3.2), (15.75, 0.004), (0.125, 0.48),
    (3.456, 2.5), (0.0075, 120), (4.875, 0.16), (0.625, 0.32),
    (12.35, 0.045), (0.0125, 64), (7.25, 1.36), (0.375, 2.48),
    (9.875, 0.08), (0.0625, 16), (5.44, 0.125), (1.875, 4.8),
    (0.225, 3.6), (6.75, 0.024), (0.0875, 24), (14.5, 0.035),
    (3.125, 0.64), (0.475, 1.8), (8.625, 0.12), (0.0375, 80),
    (2.56, 3.75), (0.175, 4.4), (11.25, 0.008), (0.5625, 0.8),
    (4.375, 0.24), (0.0225, 400),
]

for a, b in hard_dec_pairs:
    product = round(a * b, 6)
    # Clean display
    product_str = f"{product:.6f}".rstrip('0').rstrip('.')
    product_display = float(product_str)
    choices, ans = make_choices_decimal(product_display)
    dp_a = len(str(a).split('.')[-1]) if '.' in str(a) else 0
    dp_b = len(str(b).split('.')[-1]) if '.' in str(b) else 0
    add_q("Hard",
          f"What is {a} × {b}?",
          choices, ans,
          f"Multiply ignoring decimals, then place decimal point ({dp_a} + {dp_b} = {dp_a+dp_b} places). Result: {product_display}.",
          ["multiplication", "decimals", "precision"])

# --- Hard: Complex fraction multiplication (481-520) ---
hard_frac_pairs = [
    # Triple fraction multiplication
    ((5, 9), (3, 10), (6, 7)),
    ((7, 12), (8, 21), (3, 4)),
    ((4, 15), (5, 8), (6, 7)),
    ((9, 14), (7, 12), (8, 9)),
    ((11, 15), (5, 22), (6, 7)),
    # Complex mixed numbers
    ((15, 4), (22, 5)),  # 3 3/4 × 4 2/5
    ((23, 6), (18, 7)),  # 3 5/6 × 2 4/7
    ((17, 3), (21, 8)),  # 5 2/3 × 2 5/8
    ((25, 4), (14, 5)),  # 6 1/4 × 2 4/5
    ((19, 6), (24, 7)),  # 3 1/6 × 3 3/7
    ((31, 8), (16, 9)),  # 3 7/8 × 1 7/9
    ((27, 5), (20, 9)),  # 5 2/5 × 2 2/9
    ((13, 4), (32, 7)),  # 3 1/4 × 4 4/7
    ((29, 6), (15, 4)),  # 4 5/6 × 3 3/4
    ((11, 3), (27, 10)),  # 3 2/3 × 2 7/10
    # Fraction × whole requiring simplification
    ((7, 12), (36, 1)),
    ((5, 18), (24, 1)),
    ((11, 15), (45, 1)),
    ((8, 21), (63, 1)),
    ((13, 24), (48, 1)),
    # More complex proper fractions
    ((14, 15), (25, 28)),
    ((16, 21), (7, 24)),
    ((9, 20), (8, 27)),
    ((15, 16), (12, 25)),
    ((22, 35), (15, 44)),
    ((18, 25), (35, 36)),
    ((21, 32), (16, 49)),
    ((24, 35), (25, 36)),
    ((14, 27), (9, 28)),
    ((33, 40), (8, 11)),
]

for item in hard_frac_pairs:
    if len(item) == 3:
        (n1, d1), (n2, d2), (n3, d3) = item
        f1 = Fraction(n1, d1)
        f2 = Fraction(n2, d2)
        f3 = Fraction(n3, d3)
        product = f1 * f2 * f3
        choices, ans = make_choices_fraction(product)
        add_q("Hard",
              f"What is {n1}/{d1} × {n2}/{d2} × {n3}/{d3}?",
              choices, ans,
              f"Multiply all numerators: {n1}×{n2}×{n3} = {n1*n2*n3}. Multiply all denominators: {d1}×{d2}×{d3} = {d1*d2*d3}. Simplify: {frac_str(product)}.",
              ["multiplication", "fractions", "multiple fractions"])
    else:
        (n1, d1), (n2, d2) = item
        f1 = Fraction(n1, d1)
        f2 = Fraction(n2, d2)
        product = f1 * f2

        def display_frac2(n, d):
            if d == 1:
                return str(n)
            if n > d:
                whole = n // d
                rem = n % d
                if rem == 0:
                    return str(whole)
                return f"{whole} {rem}/{d}"
            return f"{n}/{d}"

        choices, ans = make_choices_fraction(product)
        add_q("Hard",
              f"What is {display_frac2(n1, d1)} × {display_frac2(n2, d2)}?",
              choices, ans,
              f"Convert to improper fractions: {n1}/{d1} × {n2}/{d2} = {n1*n2}/{d1*d2}. Simplify: {frac_str(product)}.",
              ["multiplication", "fractions", "mixed numbers"])


# --- Hard: Multi-step word problems (521-570) ---
hard_word_problems = [
    ("A government agency has 15 divisions. Each division has 8 sections with 12 employees each. If each employee handles 25 cases per month, how many total cases does the agency handle monthly?",
     15 * 8 * 12 * 25, "Total staff: 15 × 8 × 12 = 1,440. Total cases: 1,440 × 25 = 36,000."),
    ("A school orders 48 boxes of chalk at ₱125 per box and 36 boxes of markers at ₱285 per box. What is the total cost?",
     48 * 125 + 36 * 285, "Chalk: 48 × 125 = ₱6,000. Markers: 36 × 285 = ₱10,260. Total: ₱16,260."),
    ("A construction project requires 2,450 bags of cement at ₱265 per bag. What is the total cement cost?",
     2450 * 265, "2,450 × 265 = ₱649,250."),
    ("An office has 24 employees. Each earns ₱18,750 per month. What is the monthly payroll?",
     24 * 18750, "24 × 18,750 = ₱450,000."),
    ("A warehouse receives 156 pallets. Each pallet has 48 boxes, and each box contains 24 items. How many items total?",
     156 * 48 * 24, "156 × 48 = 7,488 boxes. 7,488 × 24 = 179,712 items."),
    ("A city has 85 barangays. Each barangay distributes 350 relief packs at ₱425 each. What is the total cost?",
     85 * 350 * 425, "Total packs: 85 × 350 = 29,750. Cost: 29,750 × 425 = ₱12,643,750."),
    ("A fleet of 18 vehicles each travels 145 km per day. If fuel costs ₱68 per km, what is the daily fuel expense?",
     18 * 145 * 68, "Total km: 18 × 145 = 2,610. Cost: 2,610 × 68 = ₱177,480."),
    ("A hospital has 12 wards with 35 beds each. If the daily cost per bed is ₱1,250, what is the daily operating cost for all beds?",
     12 * 35 * 1250, "Total beds: 12 × 35 = 420. Cost: 420 × 1,250 = ₱525,000."),
    ("A printing press produces 4,500 copies per hour. Each copy uses 32 pages. How many pages are printed in an 8-hour shift?",
     4500 * 32 * 8, "Copies per shift: 4,500 × 8 = 36,000. Pages: 36,000 × 32 = 1,152,000."),
    ("A government project employs 245 workers at ₱585 per day for 120 days. What is the total labor cost?",
     245 * 585 * 120, "Daily cost: 245 × 585 = ₱143,325. Total: 143,325 × 120 = ₱17,199,000."),
    ("An agency purchases 75 computers at ₱35,800 each and 75 monitors at ₱12,500 each. What is the total cost?",
     75 * 35800 + 75 * 12500, "Computers: 75 × 35,800 = ₱2,685,000. Monitors: 75 × 12,500 = ₱937,500. Total: ₱3,622,500."),
    ("A school cafeteria serves 450 students daily. Each meal costs ₱65. How much is spent on meals in 22 school days?",
     450 * 65 * 22, "Daily cost: 450 × 65 = ₱29,250. Monthly: 29,250 × 22 = ₱643,500."),
    ("A road project paves 125 meters per day using 8 trucks. Each truck carries 15 cubic meters of asphalt at ₱4,500 per cubic meter. What is the daily asphalt cost?",
     8 * 15 * 4500, "Volume: 8 × 15 = 120 m³. Cost: 120 × 4,500 = ₱540,000."),
    ("A municipality has 12,500 households. Each household uses an average of 185 kWh per month at ₱9.50 per kWh. What is the total monthly electricity cost for the municipality?",
     round(12500 * 185 * 9.5), "Total kWh: 12,500 × 185 = 2,312,500. Cost: 2,312,500 × 9.50 = ₱21,968,750."),
    ("A factory operates 3 shifts per day. Each shift produces 875 units. If each unit weighs 2.5 kg, what is the total daily production weight in kg?",
     round(3 * 875 * 2.5), "Units: 3 × 875 = 2,625. Weight: 2,625 × 2.5 = 6,562.5 kg. Rounded: 6,563 kg."),
]

for text, product, explanation in hard_word_problems[:15]:
    product_int = int(product)
    choices, ans = make_choices_int(product_int)
    add_q("Hard",
          text,
          choices, ans,
          explanation,
          ["multiplication", "word problem", "multi-step"])

# More hard word problems
hard_word_problems_2 = [
    ("A company has 3 branches. Branch A has 45 employees earning ₱22,000/month, Branch B has 38 employees earning ₱25,000/month, and Branch C has 52 employees earning ₱19,500/month. What is the total monthly payroll?",
     45*22000 + 38*25000 + 52*19500,
     "A: 45 × 22,000 = ₱990,000. B: 38 × 25,000 = ₱950,000. C: 52 × 19,500 = ₱1,014,000. Total: ₱2,954,000."),
    ("A delivery service charges ₱85 for the first 3 km and ₱12.50 for each additional km. What is the charge for a 27-km delivery?",
     int(85 + 24 * 12.5),
     "Additional km: 27 - 3 = 24. Additional charge: 24 × 12.50 = ₱300. Total: 85 + 300 = ₱385."),
    ("A farmer plants 48 rows of corn with 65 plants per row. If each plant yields 3 ears of corn, how many ears total?",
     48 * 65 * 3,
     "Plants: 48 × 65 = 3,120. Ears: 3,120 × 3 = 9,360."),
    ("A hotel has 8 floors. Each floor has 24 rooms. If the daily rate is ₱3,850 per room and occupancy is at 75% (144 rooms), what is the daily revenue?",
     144 * 3850,
     "Occupied rooms: 144. Revenue: 144 × 3,850 = ₱554,400."),
    ("A government office uses 15 air conditioning units. Each unit consumes 1.8 kWh. If electricity costs ₱11.50 per kWh and units run 10 hours daily, what is the daily AC cost?",
     int(15 * 1.8 * 11.5 * 10),
     "Consumption: 15 × 1.8 × 10 = 270 kWh. Cost: 270 × 11.50 = ₱3,105."),
    ("A publishing house prints 12,500 textbooks. Each book has 384 pages. If printing costs ₱0.45 per page, what is the total printing cost?",
     int(12500 * 384 * 0.45),
     "Pages: 12,500 × 384 = 4,800,000. Cost: 4,800,000 × 0.45 = ₱2,160,000."),
    ("A bus company operates 25 buses. Each bus makes 6 trips daily carrying 55 passengers at ₱45 per fare. What is the daily revenue?",
     25 * 6 * 55 * 45,
     "Passengers: 25 × 6 × 55 = 8,250. Revenue: 8,250 × 45 = ₱371,250."),
    ("A rice dealer buys 450 sacks at ₱1,850 per sack and sells them at ₱2,150 per sack. What is the total profit?",
     450 * (2150 - 1850),
     "Profit per sack: 2,150 - 1,850 = ₱300. Total profit: 450 × 300 = ₱135,000."),
    ("A construction company needs 1,875 square meters of tiles at ₱485 per square meter. Labor costs ₱125 per square meter. What is the total cost?",
     1875 * (485 + 125),
     "Cost per m²: 485 + 125 = ₱610. Total: 1,875 × 610 = ₱1,143,750."),
    ("A call center has 150 agents working 8 hours each. If each agent handles 12 calls per hour at an average revenue of ₱35 per call, what is the daily revenue?",
     150 * 8 * 12 * 35,
     "Calls: 150 × 8 × 12 = 14,400. Revenue: 14,400 × 35 = ₱504,000."),
]

for text, product, explanation in hard_word_problems_2[:10]:
    product_int = int(product)
    choices, ans = make_choices_int(product_int)
    add_q("Hard",
          text,
          choices, ans,
          explanation,
          ["multiplication", "word problem", "multi-step"])


# --- Hard: Decimal word problems (571-590) ---
hard_dec_word = [
    ("A government lot measures 45.75 m × 32.8 m. What is the area in square meters?",
     45.75 * 32.8, "Area = 45.75 × 32.8 = 1,500.6 m²."),
    ("An employee earns ₱756.25 per day with a 1.5× overtime rate. What is the overtime daily rate?",
     756.25 * 1.5, "756.25 × 1.5 = ₱1,134.375."),
    ("A tank holds 2,875.5 liters. If 0.85 of the tank is filled, how many liters are in the tank?",
     2875.5 * 0.85, "2,875.5 × 0.85 = 2,444.175 liters."),
    ("A wire is 125.75 meters long. If 0.64 of it is used, how many meters are used?",
     125.75 * 0.64, "125.75 × 0.64 = 80.48 meters."),
    ("A salary of ₱32,450.75 is taxed at 0.12. How much is the tax?",
     32450.75 * 0.12, "32,450.75 × 0.12 = ₱3,894.09."),
    ("A building's monthly electric bill averages ₱45,678.50. What is the annual cost?",
     45678.50 * 12, "45,678.50 × 12 = ₱548,142."),
    ("A pipe delivers 3.75 liters per minute. How many liters in 4.5 hours (270 minutes)?",
     3.75 * 270, "3.75 × 270 = 1,012.5 liters."),
    ("A vehicle's fuel efficiency is 8.75 km/L. With a 65-liter tank, what is the maximum range?",
     8.75 * 65, "8.75 × 65 = 568.75 km."),
    ("A contractor charges ₱1,875.50 per day. What is the cost for 45 days?",
     1875.50 * 45, "1,875.50 × 45 = ₱84,397.50."),
    ("A plot of land costs ₱12,500.75 per square meter. What is the cost of 28.5 square meters?",
     12500.75 * 28.5, "12,500.75 × 28.5 = ₱356,271.375."),
    ("Monthly rent is ₱15,750.25. What is the total rent for 2.5 years (30 months)?",
     15750.25 * 30, "15,750.25 × 30 = ₱472,507.50."),
    ("A machine produces 0.875 kg of output per minute. How much in 8.5 hours (510 minutes)?",
     0.875 * 510, "0.875 × 510 = 446.25 kg."),
    ("Insurance premium is 0.0325 of a ₱2,500,000 property. What is the annual premium?",
     0.0325 * 2500000, "0.0325 × 2,500,000 = ₱81,250."),
    ("A commission of 0.075 is earned on sales of ₱485,000. What is the commission?",
     0.075 * 485000, "0.075 × 485,000 = ₱36,375."),
    ("A loan of ₱150,000 has a monthly interest rate of 0.0175. What is the monthly interest?",
     0.0175 * 150000, "0.0175 × 150,000 = ₱2,625."),
    ("A factory produces 1,245.5 units per day at ₱85.75 per unit. What is the daily production value?",
     1245.5 * 85.75, "1,245.5 × 85.75 = ₱106,801.625."),
    ("A truck carries 3.75 tons per trip and makes 12 trips. If transport costs ₱2,450.50 per ton, what is the total transport cost?",
     3.75 * 12 * 2450.50, "Total tons: 3.75 × 12 = 45. Cost: 45 × 2,450.50 = ₱110,272.50."),
    ("A worker's hourly rate is ₱125.75. Night differential adds 0.10 of the hourly rate. What is the night differential per hour?",
     125.75 * 0.10, "125.75 × 0.10 = ₱12.575."),
    ("A rectangular pool measures 12.5 m × 8.75 m × 1.5 m. What is the volume in cubic meters?",
     12.5 * 8.75 * 1.5, "12.5 × 8.75 = 109.375. 109.375 × 1.5 = 164.0625 m³."),
    ("A company's revenue is ₱8,456,250.50. If expenses are 0.72 of revenue, what are the expenses?",
     8456250.50 * 0.72, "8,456,250.50 × 0.72 = ₱6,088,500.36."),
]

for text, product, explanation in hard_dec_word:
    product_rounded = round(product, 2)
    choices, ans = make_choices_decimal(product_rounded)
    add_q("Hard",
          text,
          choices, ans,
          explanation,
          ["multiplication", "decimals", "word problem", "multi-step"])


# --- Hard: Fraction word problems (591-600) and conceptual (fill to 600) ---
hard_frac_word = [
    ("A lot measures 3/4 hectare. If 2/5 of it is for a building and 1/3 of the remainder is for parking, what fraction of the lot is for parking?",
     Fraction(2, 5) * Fraction(1, 1) + Fraction(1, 3),  # placeholder
     "Remainder: 1 - 2/5 = 3/5. Parking: 1/3 × 3/5 = 1/5 of the lot.",
     Fraction(1, 5)),
    ("An employee spends 1/4 of his salary on rent, 1/3 of the remainder on food. What fraction of his salary goes to food?",
     None,
     "Remainder: 1 - 1/4 = 3/4. Food: 1/3 × 3/4 = 1/4.",
     Fraction(1, 4)),
    ("A tank is 5/8 full. If 2/3 of the water is used, what fraction of the tank still has water?",
     None,
     "Water used: 2/3 × 5/8 = 10/24 = 5/12. Remaining: 5/8 - 5/12 = 15/24 - 10/24 = 5/24.",
     Fraction(5, 24)),
    ("A project is 3/5 complete. If 1/4 of the remaining work is done today, what fraction of the total project is done today?",
     None,
     "Remaining: 1 - 3/5 = 2/5. Done today: 1/4 × 2/5 = 2/20 = 1/10.",
     Fraction(1, 10)),
    ("A recipe requires 2 3/4 cups of flour. If you want to make 1 1/2 times the recipe, how many cups of flour do you need?",
     None,
     "2 3/4 = 11/4. Multiply: 11/4 × 3/2 = 33/8 = 4 1/8 cups.",
     Fraction(33, 8)),
    ("A pipe fills 3/8 of a tank per hour. How much of the tank is filled in 2 2/3 hours?",
     None,
     "3/8 × 8/3 = 24/24 = 1. The tank is completely filled.",
     Fraction(1, 1)),
    ("A worker completes 5/12 of a task in one day. How much is completed in 1 4/5 days?",
     None,
     "5/12 × 9/5 = 45/60 = 3/4 of the task.",
     Fraction(3, 4)),
    ("A discount is 1/5 of the original price of ₱4,500. The tax is 3/20 of the discounted price. What fraction of the original price is the tax?",
     None,
     "Discounted price: 4/5 of original. Tax: 3/20 × 4/5 = 12/100 = 3/25 of original.",
     Fraction(3, 25)),
    ("A garden uses 2/3 of its area for vegetables and 3/4 of the vegetable area for tomatoes. What fraction of the total garden is for tomatoes?",
     None,
     "Tomatoes: 3/4 × 2/3 = 6/12 = 1/2 of the garden.",
     Fraction(1, 2)),
    ("A salary increase is 1/8 of the current salary of ₱24,000. If 2/5 of the increase goes to tax, what fraction of the original salary is taxed from the increase?",
     None,
     "Increase: 1/8. Tax on increase: 2/5 × 1/8 = 2/40 = 1/20 of original salary.",
     Fraction(1, 20)),
]

for text, _, explanation, answer_frac in hard_frac_word:
    choices, ans = make_choices_fraction(answer_frac)
    add_q("Hard",
          text,
          choices, ans,
          explanation,
          ["multiplication", "fractions", "word problem", "multi-step"])

# --- Fill remaining hard questions to reach exactly 200 hard (currently at ~190) ---
# Additional hard computation questions
hard_extra_whole = [
    (3789, 45), (4567, 38), (2345, 67), (6789, 24), (1234, 89),
    (5678, 43), (8765, 32), (9876, 15), (7654, 28), (4321, 56),
]

for a, b in hard_extra_whole:
    product = a * b
    choices, ans = make_choices_int(product)
    add_q("Hard",
          f"What is {fmt(a)} × {fmt(b)}?",
          choices, ans,
          f"Long multiplication: {fmt(a)} × {fmt(b)} = {fmt(product)}.",
          ["multiplication", "whole numbers", "large numbers"])

# Additional hard multi-step word problems
hard_extra_word = [
    ("A company ships 875 packages daily. Each package weighs 4.5 kg. Shipping costs ₱18.75 per kg. What is the daily shipping cost?",
     int(875 * 4.5 * 18.75),
     "Weight: 875 × 4.5 = 3,937.5 kg. Cost: 3,937.5 × 18.75 = ₱73,828."),
    ("A school has 36 classrooms. Each classroom has 45 students. If each student pays ₱1,250 per month in tuition, what is the monthly tuition revenue?",
     36 * 45 * 1250,
     "Students: 36 × 45 = 1,620. Revenue: 1,620 × 1,250 = ₱2,025,000."),
    ("A bakery produces 1,250 loaves per day at a cost of ₱28.50 per loaf. If sold at ₱45 per loaf, what is the daily profit?",
     int(1250 * (45 - 28.50)),
     "Profit per loaf: 45 - 28.50 = ₱16.50. Daily profit: 1,250 × 16.50 = ₱20,625."),
    ("A government project requires 15,000 man-hours. If 125 workers are deployed working 8 hours per day, how many days will the project take?",
     15000 // (125 * 8),
     "Man-hours per day: 125 × 8 = 1,000. Days: 15,000 ÷ 1,000 = 15 days."),
    ("A warehouse stores 48 pallets per row, 12 rows per section, and 5 sections. Each pallet holds 36 boxes. How many boxes total?",
     48 * 12 * 5 * 36,
     "Pallets: 48 × 12 × 5 = 2,880. Boxes: 2,880 × 36 = 103,680."),
    ("A telecommunications company has 2,450 cell towers. Each tower serves 1,875 subscribers. If each subscriber pays ₱599 monthly, what is the monthly revenue?",
     2450 * 1875 * 599,
     "Subscribers: 2,450 × 1,875 = 4,593,750. Revenue: 4,593,750 × 599 = ₱2,751,656,250."),
    ("A city bus system has 85 routes. Each route has 12 buses making 8 trips daily. If each trip averages 45 passengers at ₱15 fare, what is the daily revenue?",
     85 * 12 * 8 * 45 * 15,
     "Trips: 85 × 12 × 8 = 8,160. Passengers: 8,160 × 45 = 367,200. Revenue: 367,200 × 15 = ₱5,508,000."),
    ("A paper mill produces 12,500 reams per day. Each ream weighs 2.25 kg. If transport costs ₱3.50 per kg, what is the daily transport cost?",
     int(12500 * 2.25 * 3.50),
     "Weight: 12,500 × 2.25 = 28,125 kg. Cost: 28,125 × 3.50 = ₱98,437.50 ≈ ₱98,438."),
    ("A real estate developer sells 45 lots at ₱1,250,000 each. Commission is 5% of total sales. What is the commission?",
     int(45 * 1250000 * 0.05),
     "Sales: 45 × 1,250,000 = ₱56,250,000. Commission: 56,250,000 × 0.05 = ₱2,812,500."),
    ("A factory has 3 production lines. Line A produces 450 units/hr, Line B produces 375 units/hr, Line C produces 525 units/hr. In an 8-hour shift, how many total units are produced?",
     (450 + 375 + 525) * 8,
     "Total per hour: 450 + 375 + 525 = 1,350. Per shift: 1,350 × 8 = 10,800 units."),
]

for text, product, explanation in hard_extra_word:
    product_int = int(product)
    choices, ans = make_choices_int(product_int)
    add_q("Hard",
          text,
          choices, ans,
          explanation,
          ["multiplication", "word problem", "multi-step", "complex"])


# ============================================================
# BALANCE CHECK AND OUTPUT
# ============================================================

# Count by difficulty
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
med_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Easy: {easy_count}, Medium: {med_count}, Hard: {hard_count}, Total: {len(questions)}")

# If we have more than 200 in any category, trim
if easy_count > 200:
    easy_qs = [q for q in questions if q["difficulty"] == "Easy"][:200]
    other_qs = [q for q in questions if q["difficulty"] != "Easy"]
    questions = easy_qs + other_qs

if med_count > 200:
    med_qs = [q for q in questions if q["difficulty"] == "Medium"][:200]
    other_qs = [q for q in questions if q["difficulty"] != "Medium"]
    questions = med_qs + other_qs

if hard_count > 200:
    hard_qs = [q for q in questions if q["difficulty"] == "Hard"][:200]
    other_qs = [q for q in questions if q["difficulty"] != "Hard"]
    questions = hard_qs + other_qs

# If we need more questions in any category, generate simple fill questions
def fill_easy(needed):
    """Generate additional easy questions."""
    extra = []
    for i in range(needed):
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        product = a * b
        choices, ans = make_choices_int(product)
        extra.append({
            "id": 0,
            "subtest": "Numerical Ability",
            "module": "Basic Operations",
            "subtopic": "Multiplication",
            "difficulty": "Easy",
            "question": f"What is {a} × {b}?",
            "choices": choices,
            "answer": ans,
            "explanation": f"{a} × {b} = {product}.",
            "tags": ["multiplication", "whole numbers", "times table"]
        })
    return extra


def fill_medium(needed):
    """Generate additional medium questions."""
    extra = []
    for i in range(needed):
        a = random.randint(25, 99)
        b = random.randint(13, 49)
        product = a * b
        choices, ans = make_choices_int(product)
        extra.append({
            "id": 0,
            "subtest": "Numerical Ability",
            "module": "Basic Operations",
            "subtopic": "Multiplication",
            "difficulty": "Medium",
            "question": f"What is {a} × {b}?",
            "choices": choices,
            "answer": ans,
            "explanation": f"Long multiplication: {a} × {b} = {fmt(product)}.",
            "tags": ["multiplication", "whole numbers", "long multiplication"]
        })
    return extra


def fill_hard(needed):
    """Generate additional hard questions."""
    extra = []
    for i in range(needed):
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        product = a * b
        choices, ans = make_choices_int(product)
        extra.append({
            "id": 0,
            "subtest": "Numerical Ability",
            "module": "Basic Operations",
            "subtopic": "Multiplication",
            "difficulty": "Hard",
            "question": f"What is {a} × {b}?",
            "choices": choices,
            "answer": ans,
            "explanation": f"Long multiplication: {a} × {b} = {fmt(product)}.",
            "tags": ["multiplication", "whole numbers", "large numbers"]
        })
    return extra


# Recount after trimming
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
med_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

if easy_count < 200:
    questions.extend(fill_easy(200 - easy_count))
if med_count < 200:
    questions.extend(fill_medium(200 - med_count))
if hard_count < 200:
    questions.extend(fill_hard(200 - hard_count))

# Re-assign IDs
for i, q in enumerate(questions, 1):
    q["id"] = i

# Final count
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
med_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final - Easy: {easy_count}, Medium: {med_count}, Hard: {hard_count}, Total: {len(questions)}")

# Write JSON
import os
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          "data", "seed", "questions", "numerical-ability",
                          "basic-operations", "multiplication")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "questions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written {len(questions)} questions to {output_path}")
