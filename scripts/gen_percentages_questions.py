"""
Generate 600 questions for Fundamentals of Percentages (CSE Numerical Ability).
200 Easy / 200 Medium / 200 Hard

Covers:
- Meaning of percentage
- Fraction-to-percent conversion
- Decimal-to-percent conversion
- Percent-to-decimal conversion
- Percent-to-fraction conversion
- Equivalent value recognition
- Estimation questions
- Practical percentage applications
- Comparison and interpretation

Run: python scripts/gen_percentages_questions.py
Output: data/seed/questions/numerical-ability/percentages/fundamentals-of-percentages/questions.json
"""

import json
import random
from fractions import Fraction
from math import gcd
from pathlib import Path

random.seed(77)

questions: list[dict] = []
qid = 0

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "numerical-ability" / "percentages"
    / "fundamentals-of-percentages" / "questions.json"
)


def add_q(difficulty: str, question: str, choices: list[str],
           answer: str, explanation: str, tags: list[str]) -> None:
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Fundamentals of Percentages",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def fmt_pct(val: float) -> str:
    """Format a percentage value nicely."""
    if val == int(val):
        return f"{int(val)}%"
    # Remove trailing zeros
    s = f"{val:.4f}".rstrip("0").rstrip(".")
    return f"{s}%"


def fmt_dec(val: float) -> str:
    """Format a decimal value nicely."""
    if val == int(val):
        return str(int(val))
    s = f"{val:.6f}".rstrip("0").rstrip(".")
    return s


def fmt_frac(num: int, den: int) -> str:
    """Format a fraction in lowest terms."""
    g = gcd(abs(num), abs(den))
    return f"{num // g}/{den // g}"


def simplify(num: int, den: int) -> tuple[int, int]:
    """Return fraction in lowest terms."""
    g = gcd(abs(num), abs(den))
    return num // g, den // g


def make_pct_choices(correct_pct: float) -> tuple[list[str], str]:
    """Generate 4 percentage choices with plausible distractors."""
    correct_str = fmt_pct(correct_pct)
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        # Common error patterns
        error_type = random.choice([
            "shift_right", "shift_left", "off_by_small", "off_by_large",
            "half", "double", "complement"
        ])
        if error_type == "shift_right":
            d = correct_pct * 10
        elif error_type == "shift_left":
            d = correct_pct / 10
        elif error_type == "off_by_small":
            d = correct_pct + random.choice([-5, -3, -2, 2, 3, 5, 8, 10, -10])
        elif error_type == "off_by_large":
            d = correct_pct + random.choice([-15, -20, 15, 20, 25, -25])
        elif error_type == "half":
            d = correct_pct / 2
        elif error_type == "double":
            d = correct_pct * 2
        elif error_type == "complement":
            d = 100 - correct_pct
        else:
            d = correct_pct + random.randint(-10, 10)

        d = round(d, 4)
        d_str = fmt_pct(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    # Fallback
    while len(distractors) < 3:
        d = correct_pct + random.randint(1, 20)
        d_str = fmt_pct(d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)
    random.shuffle(choices)
    return choices, correct_str


def make_dec_choices(correct_dec: float) -> tuple[list[str], str]:
    """Generate 4 decimal choices with plausible distractors."""
    correct_str = fmt_dec(correct_dec)
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        error_type = random.choice([
            "shift_right", "shift_left", "off_small", "off_large", "times10"
        ])
        if error_type == "shift_right":
            d = correct_dec * 10
        elif error_type == "shift_left":
            d = correct_dec / 10
        elif error_type == "off_small":
            d = correct_dec + random.choice([-0.05, -0.02, 0.02, 0.05, 0.1, -0.1])
        elif error_type == "off_large":
            d = correct_dec + random.choice([-0.2, -0.3, 0.2, 0.3, 0.5, -0.5])
        elif error_type == "times10":
            d = correct_dec * 10
        else:
            d = correct_dec + random.uniform(-0.3, 0.3)

        d = round(d, 6)
        d_str = fmt_dec(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        d = correct_dec + (len(distractors) + 1) * 0.1
        d_str = fmt_dec(round(d, 4))
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)
    random.shuffle(choices)
    return choices, correct_str


def make_frac_choices(num: int, den: int) -> tuple[list[str], str]:
    """Generate 4 fraction choices with plausible distractors."""
    sn, sd = simplify(num, den)
    correct_str = f"{sn}/{sd}"
    distractors: set[str] = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 200:
        error_type = random.choice([
            "swap", "off_num", "off_den", "unsimplified_wrong", "complement"
        ])
        if error_type == "swap":
            dn, dd = sd, sn  # swapped
            if dd != 0:
                d_str = fmt_frac(dn, dd)
            else:
                d_str = ""
        elif error_type == "off_num":
            dn = sn + random.choice([-2, -1, 1, 2, 3])
            if dn > 0 and dn != sn:
                d_str = fmt_frac(dn, sd)
            else:
                d_str = ""
        elif error_type == "off_den":
            dd = sd + random.choice([-2, -1, 1, 2, 3, 5])
            if dd > 0 and dd != sd:
                d_str = fmt_frac(sn, dd)
            else:
                d_str = ""
        elif error_type == "unsimplified_wrong":
            factor = random.choice([2, 3, 5])
            dn, dd = sn * factor + 1, sd * factor
            d_str = fmt_frac(dn, dd)
        elif error_type == "complement":
            dn = sd - sn
            if dn > 0:
                d_str = fmt_frac(dn, sd)
            else:
                d_str = ""
        else:
            d_str = ""

        if d_str and d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        dn = sn + len(distractors) + 1
        d_str = fmt_frac(dn, sd)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- E1: Fraction to Percentage (simple denominators) ---
easy_frac_to_pct = [
    (1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
    (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (7, 20),
    (9, 20), (11, 20), (13, 20), (17, 20), (19, 20),
    (1, 25), (2, 25), (3, 25), (4, 25), (6, 25), (7, 25), (8, 25),
    (9, 25), (11, 25), (12, 25), (13, 25), (14, 25), (16, 25),
    (17, 25), (18, 25), (19, 25), (21, 25), (22, 25), (23, 25), (24, 25),
    (1, 50), (3, 50), (7, 50), (9, 50), (11, 50), (13, 50),
]
random.shuffle(easy_frac_to_pct)

for num, den in easy_frac_to_pct[:40]:
    pct = (num / den) * 100
    choices, answer = make_pct_choices(pct)
    add_q(
        "Easy",
        f"What is {num}/{den} expressed as a percentage?",
        choices, answer,
        f"Divide {num} by {den}: {num} ÷ {den} = {fmt_dec(num/den)}. "
        f"Multiply by 100: {fmt_dec(num/den)} × 100 = {fmt_pct(pct)}.",
        ["percentages", "fraction to percent", "conversion"]
    )

# --- E2: Decimal to Percentage (simple) ---
easy_decimals = [
    0.5, 0.25, 0.75, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9,
    0.05, 0.15, 0.35, 0.45, 0.55, 0.65, 0.85, 0.95,
    0.12, 0.18, 0.22, 0.28, 0.32, 0.38, 0.42, 0.48,
    0.52, 0.58, 0.62, 0.68, 0.72, 0.78, 0.82, 0.88, 0.92, 0.98,
    0.01, 0.02, 0.03, 0.04,
]
random.shuffle(easy_decimals)

for dec in easy_decimals[:40]:
    pct = dec * 100
    choices, answer = make_pct_choices(pct)
    add_q(
        "Easy",
        f"What is {fmt_dec(dec)} expressed as a percentage?",
        choices, answer,
        f"Multiply by 100: {fmt_dec(dec)} × 100 = {fmt_pct(pct)}.",
        ["percentages", "decimal to percent", "conversion"]
    )

# --- E3: Percentage to Decimal (simple) ---
easy_pcts_to_dec = [
    50, 25, 75, 10, 20, 30, 40, 60, 70, 80, 90,
    5, 15, 35, 45, 55, 65, 85, 95, 1, 2, 3, 4, 6, 7, 8, 9,
    12, 18, 22, 28, 32, 38, 42, 48, 52, 58, 62, 68, 72,
]
random.shuffle(easy_pcts_to_dec)

for pct in easy_pcts_to_dec[:40]:
    dec = pct / 100
    choices, answer = make_dec_choices(dec)
    add_q(
        "Easy",
        f"What is {pct}% expressed as a decimal?",
        choices, answer,
        f"Divide by 100: {pct} ÷ 100 = {fmt_dec(dec)}.",
        ["percentages", "percent to decimal", "conversion"]
    )

# --- E4: Percentage to Fraction (simple) ---
easy_pcts_to_frac = [
    25, 50, 75, 20, 40, 60, 80, 10, 30, 70, 90,
    5, 15, 35, 45, 55, 65, 85, 95,
    2, 4, 8, 12, 16, 24, 36, 48, 56, 64, 72, 84, 96,
]
random.shuffle(easy_pcts_to_frac)

for pct in easy_pcts_to_frac[:30]:
    num, den = simplify(pct, 100)
    choices, answer = make_frac_choices(pct, 100)
    add_q(
        "Easy",
        f"What is {pct}% expressed as a fraction in lowest terms?",
        choices, answer,
        f"Write as {pct}/100. Simplify: {pct}/100 = {num}/{den}.",
        ["percentages", "percent to fraction", "conversion"]
    )


# --- E5: Meaning / Conceptual (Easy) ---
meaning_easy = [
    ("What does 50% mean?", ["50 out of 100", "50 out of 50", "5 out of 100", "50 out of 1000"],
     "50 out of 100", "Percent means 'per hundred,' so 50% = 50 out of 100."),
    ("What does 25% mean?", ["25 out of 100", "25 out of 25", "2.5 out of 100", "25 out of 1000"],
     "25 out of 100", "25% means 25 per hundred, or 25 out of 100."),
    ("What does 100% represent?", ["The whole amount", "Half the amount", "Double the amount", "Nothing"],
     "The whole amount", "100% = 100/100 = 1, which represents the entire quantity."),
    ("What does 1% mean?", ["1 out of 100", "1 out of 10", "1 out of 1000", "10 out of 100"],
     "1 out of 100", "1% means 1 per hundred, or 1 out of every 100."),
    ("What does 75% mean?", ["75 out of 100", "7.5 out of 100", "75 out of 1000", "3 out of 4"],
     "75 out of 100", "75% literally means 75 per hundred. (Note: 3 out of 4 is equivalent but the literal meaning is 75 out of 100.)"),
    ("The word 'percent' comes from the Latin 'per centum.' What does 'centum' mean?",
     ["Hundred", "Thousand", "Ten", "Part"],
     "Hundred", "'Per centum' means 'per hundred,' so percent = per hundred."),
    ("If 30 out of 100 students passed, what percentage passed?",
     ["30%", "3%", "70%", "0.3%"],
     "30%", "30 out of 100 = 30/100 = 30%."),
    ("If a grid has 100 squares and 45 are shaded, what percentage is shaded?",
     ["45%", "4.5%", "55%", "450%"],
     "45%", "45 shaded squares out of 100 total = 45/100 = 45%."),
    ("Which symbol represents 'percent'?", ["%", "‰", "¢", "÷"],
     "%", "The % symbol represents percent (per hundred). ‰ is per mille (per thousand)."),
    ("What is 0% equivalent to?", ["Zero or nothing", "One", "One hundred", "Undefined"],
     "Zero or nothing", "0% = 0/100 = 0. It represents none of the whole."),
]

for q, ch, ans, exp in meaning_easy:
    add_q("Easy", q, ch, ans, exp, ["percentages", "meaning", "conceptual"])

# --- E6: Identify equivalent forms (Easy) ---
equiv_easy = [
    ("Which of the following is equivalent to 1/2?", ["50%", "25%", "75%", "20%"], "50%",
     "1/2 = 0.5 = 50%."),
    ("Which decimal is equivalent to 25%?", ["0.25", "2.5", "0.025", "25.0"], "0.25",
     "25% ÷ 100 = 0.25."),
    ("Which fraction is equivalent to 50%?", ["1/2", "1/4", "1/5", "2/3"], "1/2",
     "50% = 50/100 = 1/2."),
    ("Which percentage is equivalent to 0.1?", ["10%", "1%", "100%", "0.1%"], "10%",
     "0.1 × 100 = 10%."),
    ("Which decimal is equivalent to 75%?", ["0.75", "7.5", "0.075", "75.0"], "0.75",
     "75% ÷ 100 = 0.75."),
    ("Which fraction is equivalent to 20%?", ["1/5", "1/4", "1/3", "2/10"], "1/5",
     "20% = 20/100 = 1/5."),
    ("Which percentage is equivalent to 3/4?", ["75%", "34%", "43%", "25%"], "75%",
     "3 ÷ 4 = 0.75 → 0.75 × 100 = 75%."),
    ("Which decimal is equivalent to 10%?", ["0.1", "0.01", "1.0", "10.0"], "0.1",
     "10% ÷ 100 = 0.1."),
    ("Which fraction is equivalent to 10%?", ["1/10", "1/5", "1/100", "1/20"], "1/10",
     "10% = 10/100 = 1/10."),
    ("Which percentage is equivalent to 0.5?", ["50%", "5%", "0.5%", "500%"], "50%",
     "0.5 × 100 = 50%."),
    ("Which decimal is equivalent to 1%?", ["0.01", "0.1", "1.0", "0.001"], "0.01",
     "1% ÷ 100 = 0.01."),
    ("Which fraction is equivalent to 75%?", ["3/4", "7/5", "3/5", "7/10"], "3/4",
     "75% = 75/100 = 3/4."),
    ("Which percentage is equivalent to 1/4?", ["25%", "14%", "40%", "75%"], "25%",
     "1 ÷ 4 = 0.25 → 0.25 × 100 = 25%."),
    ("Which decimal is equivalent to 5%?", ["0.05", "0.5", "5.0", "0.005"], "0.05",
     "5% ÷ 100 = 0.05."),
    ("Which fraction is equivalent to 40%?", ["2/5", "4/5", "1/4", "4/10"], "2/5",
     "40% = 40/100 = 2/5."),
    ("Which percentage is equivalent to 0.01?", ["1%", "10%", "0.1%", "100%"], "1%",
     "0.01 × 100 = 1%."),
    ("Which decimal is equivalent to 100%?", ["1.0", "10.0", "0.1", "100.0"], "1.0",
     "100% ÷ 100 = 1.0."),
    ("Which fraction is equivalent to 80%?", ["4/5", "8/5", "3/4", "8/100"], "4/5",
     "80% = 80/100 = 4/5."),
    ("Which percentage is equivalent to 1/10?", ["10%", "1%", "100%", "0.1%"], "10%",
     "1 ÷ 10 = 0.1 → 0.1 × 100 = 10%."),
    ("Which decimal is equivalent to 50%?", ["0.5", "5.0", "0.05", "50.0"], "0.5",
     "50% ÷ 100 = 0.5."),
]

for q, ch, ans, exp in equiv_easy:
    add_q("Easy", q, ch, ans, exp, ["percentages", "equivalence", "recognition"])

# Ensure we have exactly 200 easy
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
# Fill remaining easy with more fraction-to-percent
extra_fracs = [(num, den) for num in range(1, 20) for den in [2, 4, 5, 10, 20, 25, 50]
               if num < den and (num, den) not in easy_frac_to_pct[:40]]
random.shuffle(extra_fracs)
idx = 0
while easy_count < 200 and idx < len(extra_fracs):
    num, den = extra_fracs[idx]
    pct = (num / den) * 100
    choices, answer = make_pct_choices(pct)
    add_q(
        "Easy",
        f"Convert {num}/{den} to a percentage.",
        choices, answer,
        f"{num} ÷ {den} = {fmt_dec(num/den)}. Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "fraction to percent", "conversion"]
    )
    easy_count += 1
    idx += 1


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- M1: Fraction to Percentage (harder denominators, repeating) ---
medium_frac_to_pct = [
    (1, 3), (2, 3), (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8),
    (1, 12), (5, 12), (7, 12), (11, 12),
    (1, 15), (2, 15), (4, 15), (7, 15), (8, 15), (11, 15), (13, 15), (14, 15),
    (1, 16), (3, 16), (5, 16), (7, 16), (9, 16), (11, 16), (13, 16), (15, 16),
    (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
    (1, 9), (2, 9), (4, 9), (5, 9), (7, 9), (8, 9),
    (3, 11), (5, 11), (7, 11), (9, 11),
]
random.shuffle(medium_frac_to_pct)

for num, den in medium_frac_to_pct[:35]:
    pct = round((num / den) * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Medium",
        f"What is {num}/{den} expressed as a percentage? (Round to two decimal places if needed.)",
        choices, answer,
        f"{num} ÷ {den} = {fmt_dec(round(num/den, 4))}. "
        f"Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "fraction to percent", "repeating decimals"]
    )

# --- M2: Decimal to Percentage (tricky decimals) ---
medium_decimals = [
    0.125, 0.375, 0.625, 0.875, 0.005, 0.015, 0.025, 0.035,
    0.045, 0.055, 0.065, 0.085, 0.095, 0.115, 0.135, 0.145,
    0.155, 0.165, 0.175, 0.185, 0.195, 0.225, 0.275, 0.325,
    0.425, 0.475, 0.525, 0.575, 0.675, 0.725, 0.775, 0.825,
    0.925, 0.975, 0.333, 0.667,
]
random.shuffle(medium_decimals)

for dec in medium_decimals[:30]:
    pct = round(dec * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Medium",
        f"Convert {fmt_dec(dec)} to a percentage.",
        choices, answer,
        f"{fmt_dec(dec)} × 100 = {fmt_pct(pct)}.",
        ["percentages", "decimal to percent", "conversion"]
    )

# --- M3: Percentage to Decimal (tricky values) ---
medium_pcts_to_dec = [
    0.5, 0.1, 0.25, 0.75, 1.5, 2.5, 3.5, 4.5,
    12.5, 37.5, 62.5, 87.5, 6.25, 18.75, 31.25, 43.75,
    56.25, 68.75, 81.25, 93.75, 125, 150, 175, 200,
    250, 300, 350, 112.5, 137.5, 162.5,
]
random.shuffle(medium_pcts_to_dec)

for pct in medium_pcts_to_dec[:30]:
    dec = pct / 100
    choices, answer = make_dec_choices(dec)
    add_q(
        "Medium",
        f"What is {fmt_pct(pct)} expressed as a decimal?",
        choices, answer,
        f"{fmt_pct(pct)} ÷ 100 = {fmt_dec(dec)}.",
        ["percentages", "percent to decimal", "conversion"]
    )

# --- M4: Percentage to Fraction (decimal percentages) ---
medium_pcts_to_frac = [
    (12.5, 1, 8), (37.5, 3, 8), (62.5, 5, 8), (87.5, 7, 8),
    (6.25, 1, 16), (18.75, 3, 16), (31.25, 5, 16), (43.75, 7, 16),
    (56.25, 9, 16), (68.75, 11, 16), (81.25, 13, 16), (93.75, 15, 16),
    (125, 5, 4), (150, 3, 2), (175, 7, 4), (200, 2, 1),
    (250, 5, 2), (300, 3, 1), (350, 7, 2), (133.33, 4, 3),
]
random.shuffle(medium_pcts_to_frac)

for pct_val, ans_num, ans_den in medium_pcts_to_frac[:20]:
    choices, answer = make_frac_choices(ans_num * ans_den, ans_den)
    # Fix: use actual answer
    correct_str = f"{ans_num}/{ans_den}"
    if correct_str not in choices:
        choices[0] = correct_str
        random.shuffle(choices)
    answer = correct_str
    add_q(
        "Medium",
        f"Express {fmt_pct(pct_val)} as a fraction in lowest terms.",
        choices, answer,
        f"{fmt_pct(pct_val)} = {pct_val}/100. Simplify to get {ans_num}/{ans_den}.",
        ["percentages", "percent to fraction", "simplification"]
    )


# --- M5: Comparison questions ---
comparison_medium = [
    ("Which is greater: 3/8 or 35%?", ["3/8", "35%", "They are equal", "Cannot be determined"],
     "3/8", "3/8 = 37.5%, which is greater than 35%."),
    ("Which is greater: 0.45 or 40%?", ["0.45", "40%", "They are equal", "Cannot be determined"],
     "0.45", "0.45 = 45%, which is greater than 40%."),
    ("Which is greater: 2/3 or 65%?", ["2/3", "65%", "They are equal", "Cannot be determined"],
     "2/3", "2/3 ≈ 66.67%, which is greater than 65%."),
    ("Which is greater: 0.8 or 75%?", ["0.8", "75%", "They are equal", "Cannot be determined"],
     "0.8", "0.8 = 80%, which is greater than 75%."),
    ("Which is greater: 5/8 or 60%?", ["5/8", "60%", "They are equal", "Cannot be determined"],
     "5/8", "5/8 = 62.5%, which is greater than 60%."),
    ("Which is smaller: 1/3 or 30%?", ["30%", "1/3", "They are equal", "Cannot be determined"],
     "30%", "1/3 ≈ 33.33%, so 30% is smaller."),
    ("Which is smaller: 0.12 or 15%?", ["0.12", "15%", "They are equal", "Cannot be determined"],
     "0.12", "0.12 = 12%, which is smaller than 15%."),
    ("Which is greater: 7/20 or 0.36?", ["0.36", "7/20", "They are equal", "Cannot be determined"],
     "0.36", "7/20 = 0.35, so 0.36 > 7/20."),
    ("Arrange from least to greatest: 1/4, 0.3, 28%", ["1/4, 28%, 0.3", "0.3, 28%, 1/4", "28%, 1/4, 0.3", "1/4, 0.3, 28%"],
     "1/4, 28%, 0.3", "1/4 = 25%, 28% = 28%, 0.3 = 30%. Order: 25% < 28% < 30%."),
    ("Arrange from least to greatest: 2/5, 0.38, 42%", ["0.38, 2/5, 42%", "2/5, 0.38, 42%", "42%, 2/5, 0.38", "0.38, 42%, 2/5"],
     "0.38, 2/5, 42%", "0.38 = 38%, 2/5 = 40%, 42% = 42%. Order: 38% < 40% < 42%."),
    ("Which value is NOT equivalent to the others: 0.25, 1/4, 25%, 2/5?",
     ["2/5", "0.25", "1/4", "25%"], "2/5",
     "0.25 = 1/4 = 25%. But 2/5 = 40%, which is different."),
    ("Which value is NOT equivalent to the others: 50%, 0.5, 1/2, 5/8?",
     ["5/8", "50%", "0.5", "1/2"], "5/8",
     "50% = 0.5 = 1/2. But 5/8 = 62.5%, which is different."),
    ("Which value is NOT equivalent to the others: 0.75, 75%, 3/4, 7/8?",
     ["7/8", "0.75", "75%", "3/4"], "7/8",
     "0.75 = 75% = 3/4. But 7/8 = 87.5%, which is different."),
    ("Which value is NOT equivalent to the others: 20%, 0.2, 1/5, 2/25?",
     ["2/25", "20%", "0.2", "1/5"], "2/25",
     "20% = 0.2 = 1/5. But 2/25 = 8%, which is different."),
    ("Which value is NOT equivalent to the others: 10%, 0.1, 1/10, 1/100?",
     ["1/100", "10%", "0.1", "1/10"], "1/100",
     "10% = 0.1 = 1/10. But 1/100 = 1%, which is different."),
]

for q, ch, ans, exp in comparison_medium:
    add_q("Medium", q, ch, ans, exp, ["percentages", "comparison", "equivalence"])

# --- M6: Practical application (Medium) ---
practical_medium = [
    ("A shirt originally costs ₱800. If it is on a 25% discount, how much is the discount?",
     ["₱200", "₱600", "₱250", "₱150"], "₱200",
     "25% of ₱800 = 0.25 × 800 = ₱200."),
    ("A student scored 36 out of 50 on a test. What is the percentage score?",
     ["72%", "36%", "64%", "82%"], "72%",
     "36/50 = 0.72 = 72%."),
    ("If VAT is 12%, how much tax is added to a ₱1,500 purchase?",
     ["₱180", "₱150", "₱120", "₱200"], "₱180",
     "12% of ₱1,500 = 0.12 × 1,500 = ₱180."),
    ("An employee's salary is ₱20,000. After a 5% raise, what is the new salary?",
     ["₱21,000", "₱20,500", "₱25,000", "₱21,500"], "₱21,000",
     "5% of ₱20,000 = ₱1,000. New salary = ₱20,000 + ₱1,000 = ₱21,000."),
    ("Out of 200 applicants, 150 passed the exam. What percentage passed?",
     ["75%", "150%", "25%", "50%"], "75%",
     "150/200 = 0.75 = 75%."),
    ("A factory produces 1,000 items. If 3% are defective, how many are defective?",
     ["30", "300", "3", "33"], "30",
     "3% of 1,000 = 0.03 × 1,000 = 30."),
    ("A budget of ₱500,000 allocates 40% to salaries. How much goes to salaries?",
     ["₱200,000", "₱400,000", "₱250,000", "₱300,000"], "₱200,000",
     "40% of ₱500,000 = 0.40 × 500,000 = ₱200,000."),
    ("If 60% of 500 employees are female, how many are male?",
     ["200", "300", "250", "100"], "200",
     "Female: 60% of 500 = 300. Male: 500 − 300 = 200 (or 40% of 500 = 200)."),
    ("A phone battery is at 35%. If full capacity is 4,000 mAh, how much charge remains?",
     ["1,400 mAh", "1,000 mAh", "2,600 mAh", "350 mAh"], "1,400 mAh",
     "35% of 4,000 = 0.35 × 4,000 = 1,400 mAh."),
    ("A survey shows 85% of 400 residents approve of a project. How many approve?",
     ["340", "320", "360", "380"], "340",
     "85% of 400 = 0.85 × 400 = 340."),
]

for q, ch, ans, exp in practical_medium:
    add_q("Medium", q, ch, ans, exp, ["percentages", "practical application", "word problem"])

# --- M7: Improper fractions / mixed numbers to percentage ---
improper_medium = [
    (5, 4), (7, 4), (9, 4), (11, 4),
    (3, 2), (5, 2), (7, 2), (9, 2),
    (6, 5), (7, 5), (8, 5), (9, 5),
    (11, 10), (13, 10), (17, 10), (19, 10),
    (11, 8), (13, 8), (15, 8), (17, 8),
]
random.shuffle(improper_medium)

for num, den in improper_medium[:20]:
    pct = round((num / den) * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Medium",
        f"What is {num}/{den} expressed as a percentage?",
        choices, answer,
        f"{num} ÷ {den} = {fmt_dec(round(num/den, 4))}. "
        f"Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "improper fraction", "conversion"]
    )

# Fill remaining medium
medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
extra_medium_decs = [round(random.uniform(0.01, 0.99), 3) for _ in range(100)]
idx = 0
while medium_count < 200 and idx < len(extra_medium_decs):
    dec = extra_medium_decs[idx]
    pct = round(dec * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Medium",
        f"Express {fmt_dec(dec)} as a percentage.",
        choices, answer,
        f"{fmt_dec(dec)} × 100 = {fmt_pct(pct)}.",
        ["percentages", "decimal to percent", "conversion"]
    )
    medium_count += 1
    idx += 1


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- H1: Complex fraction to percentage ---
hard_frac_to_pct = [
    (7, 12), (11, 12), (5, 14), (9, 14), (11, 14), (13, 14),
    (7, 16), (9, 16), (11, 16), (13, 16), (15, 16),
    (5, 18), (7, 18), (11, 18), (13, 18), (17, 18),
    (3, 13), (5, 13), (7, 13), (10, 13), (12, 13),
    (4, 11), (6, 11), (8, 11), (10, 11),
    (5, 17), (7, 17), (11, 17), (13, 17), (16, 17),
    (7, 19), (11, 19), (13, 19), (17, 19),
]
random.shuffle(hard_frac_to_pct)

for num, den in hard_frac_to_pct[:30]:
    pct = round((num / den) * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Hard",
        f"Convert {num}/{den} to a percentage. (Round to two decimal places.)",
        choices, answer,
        f"{num} ÷ {den} = {fmt_dec(round(num/den, 4))}. "
        f"Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "fraction to percent", "complex denominators"]
    )

# --- H2: Mixed numbers to percentage ---
mixed_hard = [
    (2, 1, 3), (3, 2, 5), (1, 5, 8), (2, 3, 7), (4, 1, 6),
    (1, 7, 12), (3, 5, 9), (2, 4, 11), (1, 3, 13), (5, 2, 7),
    (2, 5, 6), (3, 1, 8), (1, 11, 16), (4, 3, 8), (2, 7, 9),
    (1, 5, 12), (3, 7, 10), (2, 9, 20), (4, 3, 5), (1, 13, 25),
]
random.shuffle(mixed_hard)

for whole, frac_num, frac_den in mixed_hard[:20]:
    improper_num = whole * frac_den + frac_num
    pct = round((improper_num / frac_den) * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Hard",
        f"Convert {whole} {frac_num}/{frac_den} to a percentage. (Round to two decimal places.)",
        choices, answer,
        f"Convert to improper fraction: {whole} {frac_num}/{frac_den} = {improper_num}/{frac_den}. "
        f"{improper_num} ÷ {frac_den} = {fmt_dec(round(improper_num/frac_den, 4))}. "
        f"Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "mixed numbers", "improper fraction", "conversion"]
    )

# --- H3: Very small / very large percentages ---
extreme_pcts = [
    0.01, 0.05, 0.1, 0.15, 0.25, 0.33, 0.5, 0.75,
    400, 500, 750, 1000, 1250, 1500, 2000, 2500,
]
random.shuffle(extreme_pcts)

for pct in extreme_pcts[:15]:
    dec = pct / 100
    choices, answer = make_dec_choices(dec)
    add_q(
        "Hard",
        f"Convert {fmt_pct(pct)} to a decimal.",
        choices, answer,
        f"{fmt_pct(pct)} ÷ 100 = {fmt_dec(dec)}.",
        ["percentages", "percent to decimal", "extreme values"]
    )

# --- H4: Decimal percentages to fractions (no overlap with M4) ---
hard_pct_to_frac = [
    (16.67, 1, 6), (83.33, 5, 6),
    (11.11, 1, 9), (22.22, 2, 9), (44.44, 4, 9), (55.56, 5, 9),
    (77.78, 7, 9), (88.89, 8, 9), (14.29, 1, 7), (28.57, 2, 7),
    (42.86, 3, 7), (57.14, 4, 7), (71.43, 5, 7), (85.71, 6, 7),
    (9.09, 1, 11), (18.18, 2, 11), (27.27, 3, 11), (36.36, 4, 11),
    (45.45, 5, 11), (54.55, 6, 11),
]
random.shuffle(hard_pct_to_frac)

for pct_val, ans_num, ans_den in hard_pct_to_frac[:20]:
    correct_str = f"{ans_num}/{ans_den}"
    # Generate distractors
    dist_set: set[str] = set()
    for dn in [ans_num + 1, ans_num - 1 if ans_num > 1 else ans_num + 2, ans_den - ans_num]:
        if dn > 0:
            dist_set.add(f"{dn}/{ans_den}")
    dist_set.add(f"{ans_num}/{ans_den + 2}")
    dist_set.discard(correct_str)
    distractors = list(dist_set)[:3]
    while len(distractors) < 3:
        distractors.append(f"{ans_num + len(distractors) + 1}/{ans_den}")
    choices = [correct_str] + distractors
    random.shuffle(choices)
    add_q(
        "Hard",
        f"Express {fmt_pct(pct_val)} as a fraction in lowest terms.",
        choices, correct_str,
        f"{fmt_pct(pct_val)} ≈ {pct_val}/100. Simplify to get {ans_num}/{ans_den}.",
        ["percentages", "percent to fraction", "decimal percentages"]
    )


# --- H5: Multi-step practical problems ---
practical_hard = [
    ("A government office has 250 employees. If 68% are permanent and the rest are contractual, "
     "how many are contractual?",
     ["80", "170", "82", "68"], "80",
     "Contractual = 100% − 68% = 32%. 32% of 250 = 0.32 × 250 = 80."),
    ("An item costs ₱2,400 after a 20% discount. What was the original price?",
     ["₱3,000", "₱2,880", "₱2,800", "₱3,200"], "₱3,000",
     "After 20% discount, you pay 80%. So 0.80 × original = ₱2,400. Original = 2,400 ÷ 0.80 = ₱3,000."),
    ("A student needs 75% to pass. The test has 80 items. What is the minimum number of correct answers?",
     ["60", "75", "56", "64"], "60",
     "75% of 80 = 0.75 × 80 = 60 items."),
    ("If 12.5% of a number is 45, what is the number?",
     ["360", "562.5", "5.625", "450"], "360",
     "12.5% = 1/8. If 1/8 of x = 45, then x = 45 × 8 = 360."),
    ("A population of 50,000 grew by 4.5%. What is the new population?",
     ["52,250", "54,500", "52,500", "50,450"], "52,250",
     "4.5% of 50,000 = 0.045 × 50,000 = 2,250. New population = 50,000 + 2,250 = 52,250."),
    ("An employee pays 2% withholding tax and 12% income tax on a ₱35,000 salary. "
     "What is the total deduction?",
     ["₱4,900", "₱4,200", "₱700", "₱5,600"], "₱4,900",
     "Total tax rate = 2% + 12% = 14%. 14% of ₱35,000 = 0.14 × 35,000 = ₱4,900."),
    ("A store marks up an item by 60% then offers a 25% discount. If the cost price is ₱500, "
     "what is the selling price?",
     ["₱600", "₱675", "₱800", "₱500"], "₱600",
     "Marked price = 500 × 1.60 = ₱800. Discount = 25% of 800 = ₱200. Selling price = 800 − 200 = ₱600."),
    ("In an election, Candidate A got 45%, Candidate B got 35%, and Candidate C got the rest. "
     "If there were 8,000 voters, how many voted for Candidate C?",
     ["1,600", "2,000", "2,800", "3,600"], "1,600",
     "C's share = 100% − 45% − 35% = 20%. 20% of 8,000 = 0.20 × 8,000 = 1,600."),
    ("A machine's efficiency dropped from 95% to 76%. By how many percentage points did it drop?",
     ["19 percentage points", "19%", "25%", "20 percentage points"], "19 percentage points",
     "Drop = 95% − 76% = 19 percentage points."),
    ("If 3/8 of a class of 40 students are honor students, what percentage are NOT honor students?",
     ["62.5%", "37.5%", "75%", "25%"], "62.5%",
     "Honor students = 3/8 = 37.5%. Non-honor = 100% − 37.5% = 62.5%."),
    ("A loan of ₱100,000 charges 1.5% monthly interest. How much interest is charged in one month?",
     ["₱1,500", "₱15,000", "₱150", "₱15"], "₱1,500",
     "1.5% of ₱100,000 = 0.015 × 100,000 = ₱1,500."),
    ("A department's budget was cut by 15%. If the original budget was ₱2,000,000, "
     "what is the new budget?",
     ["₱1,700,000", "₱1,500,000", "₱1,850,000", "₱1,750,000"], "₱1,700,000",
     "Cut = 15% of 2,000,000 = ₱300,000. New budget = 2,000,000 − 300,000 = ₱1,700,000."),
    ("Convert 5/6 to a percentage and round to two decimal places.",
     ["83.33%", "83.67%", "80%", "85%"], "83.33%",
     "5 ÷ 6 = 0.8333... × 100 = 83.33%."),
    ("What is 7/11 as a percentage, rounded to two decimal places?",
     ["63.64%", "63.33%", "70%", "77%"], "63.64%",
     "7 ÷ 11 = 0.6364 × 100 = 63.64%."),
    ("If a product's price increased from ₱400 to ₱460, what is the percentage increase?",
     ["15%", "60%", "13%", "20%"], "15%",
     "Increase = 460 − 400 = 60. Percentage = 60/400 × 100 = 15%."),
]

for q, ch, ans, exp in practical_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "practical application", "multi-step"])

# --- H6: Percentage points vs percent change ---
pct_points_hard = [
    ("A candidate's approval rating rose from 30% to 45%. What is the increase in percentage points?",
     ["15 percentage points", "50%", "15%", "45%"], "15 percentage points",
     "Percentage point increase = 45% − 30% = 15 percentage points."),
    ("A candidate's approval rating rose from 30% to 45%. What is the percent change relative to the original?",
     ["50%", "15%", "15 percentage points", "45%"], "50%",
     "Percent change = (45 − 30)/30 × 100 = 15/30 × 100 = 50%."),
    ("Unemployment dropped from 8% to 6%. What is the decrease in percentage points?",
     ["2 percentage points", "25%", "2%", "75%"], "2 percentage points",
     "8% − 6% = 2 percentage points."),
    ("Unemployment dropped from 8% to 6%. What is the percent decrease relative to the original rate?",
     ["25%", "2%", "2 percentage points", "75%"], "25%",
     "Percent decrease = (8 − 6)/8 × 100 = 2/8 × 100 = 25%."),
    ("A passing rate improved from 60% to 75%. By how many percentage points did it improve?",
     ["15 percentage points", "25%", "15%", "20%"], "15 percentage points",
     "75% − 60% = 15 percentage points."),
]

for q, ch, ans, exp in pct_points_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "percentage points", "interpretation"])

# --- H7: Reverse percentage / finding the base ---
reverse_hard = [
    ("If 20% of a number is 36, what is the number?",
     ["180", "7.2", "720", "56"], "180",
     "20% × x = 36. x = 36 ÷ 0.20 = 180."),
    ("If 75% of a number is 150, what is the number?",
     ["200", "112.5", "225", "175"], "200",
     "75% × x = 150. x = 150 ÷ 0.75 = 200."),
    ("If 8% of a number is 24, what is the number?",
     ["300", "192", "30", "3"], "300",
     "8% × x = 24. x = 24 ÷ 0.08 = 300."),
    ("If 150% of a number is 90, what is the number?",
     ["60", "135", "45", "100"], "60",
     "150% × x = 90. x = 90 ÷ 1.50 = 60."),
    ("If 33.33% of a number is 50, what is approximately the number?",
     ["150", "16.67", "166.67", "100"], "150",
     "33.33% ≈ 1/3. If 1/3 of x = 50, then x = 50 × 3 = 150."),
    ("If 62.5% of a number is 100, what is the number?",
     ["160", "62.5", "250", "125"], "160",
     "62.5% = 5/8. If 5/8 of x = 100, then x = 100 × 8/5 = 160."),
    ("If 40% of a number is 120, what is 65% of the same number?",
     ["195", "78", "300", "180"], "195",
     "40% × x = 120, so x = 300. 65% of 300 = 0.65 × 300 = 195."),
    ("If 25% of a number equals 30% of 200, what is the number?",
     ["240", "60", "150", "80"], "240",
     "30% of 200 = 60. 25% × x = 60. x = 60 ÷ 0.25 = 240."),
    ("After a 10% discount, an item costs ₱4,500. What was the original price?",
     ["₱5,000", "₱4,950", "₱4,050", "₱5,500"], "₱5,000",
     "After 10% off, you pay 90%. 0.90 × original = 4,500. Original = 4,500 ÷ 0.90 = ₱5,000."),
    ("After a 30% increase, a salary became ₱39,000. What was the original salary?",
     ["₱30,000", "₱27,300", "₱50,700", "₱35,000"], "₱30,000",
     "After 30% increase, salary = 130% of original. 1.30 × x = 39,000. x = 39,000 ÷ 1.30 = ₱30,000."),
]

for q, ch, ans, exp in reverse_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "reverse percentage", "finding the base"])


# --- H8: Estimation and mental math (Hard) ---
estimation_hard = [
    ("Without computing exactly, which is closest to 7/13 as a percentage?",
     ["54%", "70%", "45%", "63%"], "54%",
     "7 ÷ 13 ≈ 0.538 ≈ 53.8%, closest to 54%."),
    ("Without computing exactly, which is closest to 5/9 as a percentage?",
     ["56%", "45%", "59%", "50%"], "56%",
     "5 ÷ 9 ≈ 0.556 ≈ 55.6%, closest to 56%."),
    ("Without computing exactly, which is closest to 8/13 as a percentage?",
     ["62%", "80%", "54%", "69%"], "62%",
     "8 ÷ 13 ≈ 0.615 ≈ 61.5%, closest to 62%."),
    ("Without computing exactly, which is closest to 11/17 as a percentage?",
     ["65%", "55%", "70%", "75%"], "65%",
     "11 ÷ 17 ≈ 0.647 ≈ 64.7%, closest to 65%."),
    ("Without computing exactly, which is closest to 9/14 as a percentage?",
     ["64%", "90%", "56%", "70%"], "64%",
     "9 ÷ 14 ≈ 0.643 ≈ 64.3%, closest to 64%."),
    ("Estimate: 0.4286 is closest to which common fraction-percentage?",
     ["3/7 ≈ 42.86%", "2/5 = 40%", "1/2 = 50%", "3/8 = 37.5%"], "3/7 ≈ 42.86%",
     "0.4286 × 100 = 42.86%, which is 3/7."),
    ("Estimate: 0.1875 is closest to which common fraction-percentage?",
     ["3/16 = 18.75%", "1/5 = 20%", "1/6 ≈ 16.67%", "1/4 = 25%"], "3/16 = 18.75%",
     "0.1875 × 100 = 18.75% = 3/16."),
    ("If 1/7 ≈ 14.29%, what is approximately 5/7 as a percentage?",
     ["71.43%", "57.14%", "85.71%", "42.86%"], "71.43%",
     "5/7 = 5 × (1/7) ≈ 5 × 14.29% = 71.43%."),
    ("If 1/9 ≈ 11.11%, what is approximately 7/9 as a percentage?",
     ["77.78%", "63.64%", "70%", "88.89%"], "77.78%",
     "7/9 = 7 × (1/9) ≈ 7 × 11.11% = 77.78%."),
    ("If 1/11 ≈ 9.09%, what is approximately 4/11 as a percentage?",
     ["36.36%", "40%", "44.44%", "27.27%"], "36.36%",
     "4/11 = 4 × (1/11) ≈ 4 × 9.09% = 36.36%."),
]

for q, ch, ans, exp in estimation_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "estimation", "mental math"])

# --- H9: Complex comparison and interpretation ---
interpretation_hard = [
    ("Department A has 120 employees with 90% attendance. Department B has 80 employees with 95% attendance. "
     "Which department has more employees present?",
     ["Department A", "Department B", "They are equal", "Cannot be determined"], "Department A",
     "A: 90% of 120 = 108 present. B: 95% of 80 = 76 present. 108 > 76."),
    ("Store X offers 30% off a ₱1,000 item. Store Y offers 20% off then an additional 10% off the same item. "
     "Which store gives a lower final price?",
     ["Store X", "Store Y", "They are equal", "Cannot be determined"], "Store X",
     "X: 1,000 × 0.70 = ₱700. Y: 1,000 × 0.80 = 800, then 800 × 0.90 = ₱720. Store X is cheaper."),
    ("A value increased by 25% then decreased by 20%. Is the final value equal to the original?",
     ["Yes, they are equal", "No, the final is greater", "No, the final is less", "Cannot be determined"],
     "Yes, they are equal",
     "Start with 100. +25% → 125. −20% of 125 → 125 × 0.80 = 100. They are equal."),
    ("A value decreased by 20% then increased by 25%. Is the final value equal to the original?",
     ["Yes, they are equal", "No, the final is greater", "No, the final is less", "Cannot be determined"],
     "Yes, they are equal",
     "Start with 100. −20% → 80. +25% of 80 → 80 × 1.25 = 100. They are equal."),
    ("A value increased by 50% then decreased by 50%. What percentage of the original remains?",
     ["75%", "100%", "50%", "25%"], "75%",
     "Start with 100. +50% → 150. −50% of 150 → 150 × 0.50 = 75. That's 75% of original."),
    ("If a price is increased by 20% and then the new price is increased by 20% again, "
     "what is the total percentage increase from the original?",
     ["44%", "40%", "42%", "48%"], "44%",
     "100 × 1.20 = 120. 120 × 1.20 = 144. Total increase = 44%."),
    ("A number is first increased by 10% and then decreased by 10%. "
     "The result is what percentage of the original?",
     ["99%", "100%", "90%", "110%"], "99%",
     "100 × 1.10 = 110. 110 × 0.90 = 99. Result is 99% of original."),
    ("If 40% of A equals 60% of B, what is the ratio A:B?",
     ["3:2", "2:3", "4:6", "6:4"], "3:2",
     "0.40A = 0.60B → A/B = 0.60/0.40 = 3/2. So A:B = 3:2."),
    ("If 25% of X equals 40% of 150, what is X?",
     ["240", "60", "37.5", "600"], "240",
     "40% of 150 = 60. 25% of X = 60. X = 60 ÷ 0.25 = 240."),
    ("Three candidates received 45%, 30%, and the rest of 12,000 votes. "
     "How many votes did the third candidate receive?",
     ["3,000", "2,400", "5,400", "3,600"], "3,000",
     "Third candidate: 100% − 45% − 30% = 25%. 25% of 12,000 = 3,000."),
]

for q, ch, ans, exp in interpretation_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "interpretation", "multi-step"])

# --- H10: Error identification (Hard) ---
error_hard = [
    ("A student converted 5% to 0.5. What error did they make?",
     ["Divided by 10 instead of 100", "Multiplied by 10", "Moved decimal right instead of left",
      "Forgot the percent sign"],
     "Divided by 10 instead of 100",
     "5% = 5 ÷ 100 = 0.05, not 0.5. The student only divided by 10."),
    ("A student wrote 3/8 = 38%. What error did they make?",
     ["Placed numerator and denominator side by side instead of dividing",
      "Multiplied 3 by 8", "Forgot to multiply by 100", "Divided 8 by 3"],
     "Placed numerator and denominator side by side instead of dividing",
     "Correct: 3 ÷ 8 = 0.375 = 37.5%. The student just wrote '3' and '8' together as 38."),
    ("A student converted 150% to 0.15. What error did they make?",
     ["Divided by 1000 instead of 100", "Moved decimal three places left",
      "Confused 150 with 15", "Multiplied instead of dividing"],
     "Divided by 1000 instead of 100",
     "150% ÷ 100 = 1.50. The student got 0.15, which is 150 ÷ 1000."),
    ("A student wrote 40% = 4/10 as the simplified fraction. Is this correct?",
     ["No, it should be 2/5", "Yes, it is correct", "No, it should be 4/100", "No, it should be 1/4"],
     "No, it should be 2/5",
     "40% = 40/100 = 2/5. While 4/10 equals 2/5, it is not in lowest terms."),
    ("A student says '0.25 as a percentage is 0.25%.' What is the correct answer?",
     ["25%", "0.25%", "2.5%", "250%"], "25%",
     "0.25 × 100 = 25%. The student forgot to multiply by 100."),
]

for q, ch, ans, exp in error_hard:
    add_q("Hard", q, ch, ans, exp, ["percentages", "error identification", "conceptual"])

# Fill remaining hard questions
hard_count = len([q for q in questions if q["difficulty"] == "Hard"])

# Generate more complex fraction-to-percent for filler
hard_filler_fracs = [(n, d) for d in range(7, 23) for n in range(1, d)
                     if gcd(n, d) == 1 and d not in [8, 10, 12, 16, 20]]
random.shuffle(hard_filler_fracs)
idx = 0
while hard_count < 200 and idx < len(hard_filler_fracs):
    num, den = hard_filler_fracs[idx]
    pct = round((num / den) * 100, 2)
    choices, answer = make_pct_choices(pct)
    add_q(
        "Hard",
        f"Express {num}/{den} as a percentage, rounded to two decimal places.",
        choices, answer,
        f"{num} ÷ {den} = {fmt_dec(round(num/den, 4))}. Multiply by 100: {fmt_pct(pct)}.",
        ["percentages", "fraction to percent", "complex conversion"]
    )
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

    # Trim to exactly 200 per difficulty if over
    if len(easy) > 200:
        excess = len(easy) - 200
        for _ in range(excess):
            for i, q in enumerate(questions):
                if q["difficulty"] == "Easy":
                    questions.pop(i)
                    break

    if len(medium) > 200:
        excess = len(medium) - 200
        for _ in range(excess):
            for i in range(len(questions) - 1, -1, -1):
                if questions[i]["difficulty"] == "Medium":
                    questions.pop(i)
                    break

    if len(hard) > 200:
        excess = len(hard) - 200
        for _ in range(excess):
            for i in range(len(questions) - 1, -1, -1):
                if questions[i]["difficulty"] == "Hard":
                    questions.pop(i)
                    break

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


def reassign_ids() -> None:
    """Reassign sequential IDs after any trimming."""
    for i, q in enumerate(questions, start=1):
        q["id"] = i


def main() -> None:
    validate_questions()

    # Trim to 600 total (200 per difficulty)
    final: list[dict] = []
    easy = [q for q in questions if q["difficulty"] == "Easy"][:200]
    medium = [q for q in questions if q["difficulty"] == "Medium"][:200]
    hard = [q for q in questions if q["difficulty"] == "Hard"][:200]
    final = easy + medium + hard

    # Reassign IDs
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
