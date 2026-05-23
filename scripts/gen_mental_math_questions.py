"""
Generate 600 questions for Percentage Mental Math and Shortcuts (CSE Numerical Ability).
200 Easy / 200 Medium / 200 Hard

Covers:
- Common fraction-percent equivalents
- Benchmark percentage recognition
- Estimation problems
- Rapid mental computation (10%, 5%, 1% shortcuts)
- Percentage increase and decrease estimation
- Practical mental math applications
- Shortcut identification
- Decomposition strategies
- Business and financial estimation
- Real-life numerical reasoning

Run: python scripts/gen_mental_math_questions.py
Output: data/seed/questions/numerical-ability/percentages/percentage-mental-math-and-shortcuts/questions.json
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
    / "percentage-mental-math-and-shortcuts" / "questions.json"
)


def add_q(difficulty: str, question: str, choices: list[str],
           answer: str, explanation: str, tags: list[str]) -> None:
    global qid
    qid += 1
    questions.append({
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Percentage Mental Math and Shortcuts",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    })


def fmt_num(val: float) -> str:
    """Format a number nicely (no trailing zeros)."""
    if val == int(val):
        return f"{int(val):,}"
    s = f"{val:,.4f}".rstrip("0").rstrip(".")
    return s


def fmt_peso(val: float) -> str:
    """Format as Philippine peso."""
    if val == int(val):
        return f"\u20b1{int(val):,}"
    return f"\u20b1{val:,.2f}"


def make_numeric_choices(correct: float, unit: str = "",
                         spread: str = "medium") -> tuple[list[str], str]:
    """Generate 4 numeric choices with plausible distractors."""
    def fmt(v: float) -> str:
        if v == int(v):
            base = f"{int(v):,}"
        else:
            base = f"{v:,.2f}".rstrip("0").rstrip(".")
        return f"{unit}{base}" if unit else base

    correct_str = fmt(correct)
    distractors: set[str] = set()
    attempts = 0

    while len(distractors) < 3 and attempts < 300:
        if spread == "tight":
            offsets = [0.9, 0.95, 1.05, 1.1, 1.15, 0.85]
        elif spread == "wide":
            offsets = [0.5, 0.1, 2.0, 10.0, 0.25, 1.5, 3.0]
        else:
            offsets = [0.5, 0.8, 1.2, 1.5, 2.0, 0.1, 10.0, 0.75, 1.25]

        factor = random.choice(offsets)
        d = correct * factor
        if d <= 0:
            d = correct + random.choice([10, 20, 50, 100, -10, -20])
        d = round(d, 2)
        d_str = fmt(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        d = correct + (len(distractors) + 1) * max(1, correct * 0.1)
        d_str = fmt(round(d, 2))
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str



def make_pct_choices(correct_pct: float) -> tuple[list[str], str]:
    """Generate 4 percentage choices with plausible distractors."""
    def fmt(v: float) -> str:
        if v == int(v):
            return f"{int(v)}%"
        return f"{v:.2f}%".rstrip("0").rstrip(".")  + "%"  if "." in f"{v}" else f"{int(v)}%"

    def fmt_pct(v: float) -> str:
        if v == int(v):
            return f"{int(v)}%"
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return f"{s}%"

    correct_str = fmt_pct(correct_pct)
    distractors: set[str] = set()
    attempts = 0

    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_small", "off_large", "half", "double", "complement", "decimal_shift"
        ])
        if error_type == "off_small":
            d = correct_pct + random.choice([-5, -3, -2, 2, 3, 5, 8, 10, -10])
        elif error_type == "off_large":
            d = correct_pct + random.choice([-15, -20, 15, 20, 25, -25])
        elif error_type == "half":
            d = correct_pct / 2
        elif error_type == "double":
            d = correct_pct * 2
        elif error_type == "complement":
            d = 100 - correct_pct
        elif error_type == "decimal_shift":
            d = correct_pct * 10 if correct_pct < 10 else correct_pct / 10
        else:
            d = correct_pct + random.randint(-10, 10)

        d = round(d, 2)
        d_str = fmt_pct(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        d = correct_pct + (len(distractors) + 1) * 5
        d_str = fmt_pct(round(d, 2))
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str



# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- E1: 10% shortcut (40 questions) ---
easy_10pct_bases = [
    200, 350, 450, 500, 600, 750, 800, 900, 1000, 1200,
    1500, 1800, 2000, 2400, 2500, 3000, 3200, 3500, 4000, 4500,
    5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500,
    10000, 12000, 15000, 18000, 20000, 25000, 30000, 35000, 40000, 50000,
]
random.shuffle(easy_10pct_bases)

for base in easy_10pct_bases[:40]:
    correct = base * 0.1
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 10% of {base:,}?",
        choices, answer,
        f"To find 10%, move the decimal one place left: {base:,} → {fmt_num(correct)}.",
        ["mental math", "10% shortcut", "benchmark percentage"]
    )


# --- E2: 50% shortcut (30 questions) ---
easy_50pct_bases = [
    120, 240, 360, 480, 500, 640, 720, 800, 900, 1000,
    1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000,
    3200, 3600, 4000, 4400, 4800, 5000, 5600, 6000, 6400, 7200,
]
random.shuffle(easy_50pct_bases)

for base in easy_50pct_bases[:30]:
    correct = base * 0.5
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 50% of {base:,}?",
        choices, answer,
        f"50% means half. {base:,} ÷ 2 = {fmt_num(correct)}.",
        ["mental math", "50% shortcut", "benchmark percentage"]
    )

# --- E3: 25% shortcut (30 questions) ---
easy_25pct_bases = [
    80, 120, 160, 200, 240, 320, 400, 480, 560, 600,
    640, 720, 800, 960, 1000, 1200, 1600, 2000, 2400, 2800,
    3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000, 6400, 8000,
]
random.shuffle(easy_25pct_bases)

for base in easy_25pct_bases[:30]:
    correct = base * 0.25
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 25% of {base:,}?",
        choices, answer,
        f"25% = 1/4. {base:,} ÷ 4 = {fmt_num(correct)}.",
        ["mental math", "25% shortcut", "benchmark percentage"]
    )


# --- E4: Fraction-percent equivalents recognition (30 questions) ---
frac_pct_easy = [
    ("1/2", 50), ("1/4", 25), ("3/4", 75), ("1/5", 20), ("2/5", 40),
    ("3/5", 60), ("4/5", 80), ("1/10", 10), ("3/10", 30), ("7/10", 70),
    ("9/10", 90), ("1/20", 5), ("1/100", 1), ("1/50", 2), ("1/25", 4),
    ("1/2", 50), ("1/4", 25), ("3/4", 75), ("2/5", 40), ("3/5", 60),
    ("1/8", 12.5), ("1/3", 33.33), ("2/3", 66.67), ("1/5", 20), ("4/5", 80),
    ("1/10", 10), ("1/20", 5), ("1/4", 25), ("3/4", 75), ("1/2", 50),
]
random.shuffle(frac_pct_easy)

used_frac_easy: set[str] = set()
count_e4 = 0
for frac_str, pct_val in frac_pct_easy:
    if count_e4 >= 30:
        break
    key = f"{frac_str}_{pct_val}"
    if key in used_frac_easy:
        continue
    used_frac_easy.add(key)
    choices, answer = make_pct_choices(pct_val)
    add_q(
        "Easy",
        f"What percentage is equivalent to {frac_str}?",
        choices, answer,
        f"{frac_str} = {answer}. This is a common fraction-percent equivalent to memorize.",
        ["fraction-percent equivalents", "mental math", "recognition"]
    )
    count_e4 += 1


# --- E5: 1% shortcut (20 questions) ---
easy_1pct_bases = [
    300, 500, 700, 800, 1000, 1200, 1500, 2000, 2500, 3000,
    3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000, 15000,
]
random.shuffle(easy_1pct_bases)

for base in easy_1pct_bases[:20]:
    correct = base * 0.01
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 1% of {base:,}?",
        choices, answer,
        f"To find 1%, move the decimal two places left: {base:,} → {fmt_num(correct)}.",
        ["mental math", "1% shortcut", "benchmark percentage"]
    )

# --- E6: 5% shortcut (20 questions) ---
easy_5pct_bases = [
    200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000,
    2400, 2800, 3000, 3200, 4000, 5000, 6000, 8000, 10000, 12000,
]
random.shuffle(easy_5pct_bases)

for base in easy_5pct_bases[:20]:
    correct = base * 0.05
    ten_pct = base * 0.1
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 5% of {base:,}?",
        choices, answer,
        f"Find 10% first: {fmt_num(ten_pct)}. Then halve it: {fmt_num(ten_pct)} ÷ 2 = {fmt_num(correct)}.",
        ["mental math", "5% shortcut", "benchmark percentage"]
    )


# --- E7: Simple practical mental math (30 questions) ---
practical_easy_data = [
    (500, 10, "discount", "A store offers 10% off on a {base}-item. How much is the discount?"),
    (1000, 10, "discount", "An item costs {base}. What is the 10% discount amount?"),
    (2000, 50, "half", "A gadget is priced at {base}. What is 50% of its price?"),
    (800, 25, "quarter", "A book costs {base}. What is 25% of its price?"),
    (1500, 10, "discount", "A bag is priced at {base}. How much is 10% off?"),
    (3000, 50, "half", "A phone costs {base}. What is half its price?"),
    (4000, 25, "quarter", "A laptop bag costs {base}. What is 25% of that?"),
    (600, 10, "discount", "A shirt costs {base}. What is 10% of that amount?"),
    (1200, 50, "half", "A pair of shoes costs {base}. What is 50% off?"),
    (2400, 25, "quarter", "A jacket costs {base}. What is 25% of its price?"),
    (5000, 10, "discount", "Monthly internet bill is {base}. What is 10% of it?"),
    (8000, 50, "half", "A tablet costs {base}. What is 50% of that?"),
    (1600, 25, "quarter", "A watch costs {base}. What is 25% of its price?"),
    (900, 10, "discount", "A meal costs {base}. What is 10% tip?"),
    (2000, 10, "discount", "A bill is {base}. What is 10% service charge?"),
    (3600, 50, "half", "A TV costs {base}. What is 50% of that?"),
    (4800, 25, "quarter", "A camera costs {base}. What is 25% of its price?"),
    (700, 10, "discount", "A grocery item costs {base}. What is 10% of that?"),
    (1400, 50, "half", "A blender costs {base}. What is 50% of its price?"),
    (2800, 25, "quarter", "A printer costs {base}. What is 25% of that?"),
    (10000, 10, "discount", "Monthly rent is {base}. What is 10% of it?"),
    (6000, 50, "half", "A bicycle costs {base}. What is 50% of that?"),
    (3200, 25, "quarter", "A desk costs {base}. What is 25% of its price?"),
    (400, 10, "discount", "A book costs {base}. What is 10% of that?"),
    (1800, 50, "half", "A chair costs {base}. What is 50% of its price?"),
    (2000, 25, "quarter", "A backpack costs {base}. What is 25% of that?"),
    (7500, 10, "discount", "A monthly bill is {base}. What is 10% of it?"),
    (4400, 50, "half", "An appliance costs {base}. What is 50% of that?"),
    (1200, 25, "quarter", "A subscription costs {base}. What is 25% of it?"),
    (9000, 10, "discount", "A salary advance is {base}. What is 10% of it?"),
]
random.shuffle(practical_easy_data)

for base, pct, _, q_template in practical_easy_data[:30]:
    correct = base * pct / 100
    q_text = q_template.format(base=f"\u20b1{base:,}")
    choices, answer = make_numeric_choices(correct, unit="\u20b1")
    add_q(
        "Easy",
        q_text,
        choices, answer,
        f"{pct}% of \u20b1{base:,} = \u20b1{base:,} × {pct/100} = {fmt_peso(correct)}.",
        ["mental math", "practical application", "percentage shortcuts"]
    )


# --- E8: Fill remaining easy with 75% shortcut ---
easy_75pct_bases = [
    80, 120, 160, 200, 240, 320, 400, 480, 560, 600,
    640, 720, 800, 960, 1000, 1200, 1600, 2000, 2400, 2800,
    3200, 3600, 4000, 4800, 5600, 6000, 6400, 7200, 8000, 10000,
]
random.shuffle(easy_75pct_bases)

easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
idx = 0
while easy_count < 210 and idx < len(easy_75pct_bases):
    base = easy_75pct_bases[idx]
    correct = base * 0.75
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 75% of {base:,}?",
        choices, answer,
        f"75% = 3/4. {base:,} ÷ 4 = {fmt_num(base/4)}, × 3 = {fmt_num(correct)}.",
        ["mental math", "75% shortcut", "benchmark percentage"]
    )
    easy_count += 1
    idx += 1


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================


# --- M1: Decomposition (15% = 10% + 5%) (25 questions) ---
med_15pct_bases = [
    400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200,
    2400, 2600, 2800, 3000, 3200, 3400, 3600, 4000, 4200, 4500,
    5000, 5500, 6000, 7000, 8000,
]
random.shuffle(med_15pct_bases)

for base in med_15pct_bases[:25]:
    correct = base * 0.15
    ten_pct = base * 0.1
    five_pct = base * 0.05
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"What is 15% of {base:,}?",
        choices, answer,
        f"Decompose: 15% = 10% + 5%. 10% of {base:,} = {fmt_num(ten_pct)}. "
        f"5% = {fmt_num(five_pct)}. Total: {fmt_num(ten_pct)} + {fmt_num(five_pct)} = {fmt_num(correct)}.",
        ["mental math", "decomposition", "percentage shortcuts"]
    )

# --- M2: Decomposition (35% = 25% + 10%) (20 questions) ---
med_35pct_bases = [
    400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200,
    2400, 2800, 3000, 3200, 3600, 4000, 4400, 4800, 5200, 6000,
]
random.shuffle(med_35pct_bases)

for base in med_35pct_bases[:20]:
    correct = base * 0.35
    q25 = base * 0.25
    q10 = base * 0.1
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"What is 35% of {base:,}?",
        choices, answer,
        f"Decompose: 35% = 25% + 10%. 25% of {base:,} = {fmt_num(q25)}. "
        f"10% = {fmt_num(q10)}. Total: {fmt_num(q25)} + {fmt_num(q10)} = {fmt_num(correct)}.",
        ["mental math", "decomposition", "percentage shortcuts"]
    )


# --- M3: Fraction-percent applied (12.5% = 1/8, 37.5% = 3/8, etc.) (25 questions) ---
frac_applied_medium = [
    (12.5, 8, 1, "1/8"),   # 12.5% = 1/8
    (37.5, 8, 3, "3/8"),   # 37.5% = 3/8
    (62.5, 8, 5, "5/8"),   # 62.5% = 5/8
    (87.5, 8, 7, "7/8"),   # 87.5% = 7/8
    (33.33, 3, 1, "1/3"),  # 33.33% = 1/3
    (66.67, 3, 2, "2/3"),  # 66.67% = 2/3
    (16.67, 6, 1, "1/6"),  # 16.67% = 1/6
    (83.33, 6, 5, "5/6"),  # 83.33% = 5/6
]

med_frac_bases = [
    160, 240, 320, 400, 480, 560, 640, 720, 800, 960,
    1200, 1440, 1600, 1920, 2400, 2880, 3200, 3600, 4000, 4800,
    5400, 6000, 6400, 7200, 8000,
]
random.shuffle(med_frac_bases)

count_m3 = 0
for base in med_frac_bases:
    if count_m3 >= 25:
        break
    pct_val, denom, numer, frac_str = random.choice(frac_applied_medium)
    # Ensure clean division
    if base % denom != 0:
        continue
    correct = base * numer / denom
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"What is {pct_val}% of {base:,}?",
        choices, answer,
        f"{pct_val}% = {frac_str}. {base:,} ÷ {denom} = {fmt_num(base/denom)}"
        + (f", × {numer} = {fmt_num(correct)}." if numer > 1 else f" = {fmt_num(correct)}."),
        ["mental math", "fraction-percent equivalents", "applied shortcuts"]
    )
    count_m3 += 1


# --- M4: Multiplier method for increase/decrease (25 questions) ---
multiplier_scenarios = [
    (10, "increase", 1.1, "× 1.1"),
    (20, "increase", 1.2, "× 1.2"),
    (25, "increase", 1.25, "× 1.25"),
    (50, "increase", 1.5, "× 1.5"),
    (10, "decrease", 0.9, "× 0.9"),
    (20, "decrease", 0.8, "× 0.8"),
    (25, "decrease", 0.75, "× 0.75"),
    (50, "decrease", 0.5, "× 0.5"),
]

med_mult_bases = [
    1000, 1200, 1500, 1600, 2000, 2400, 2500, 3000, 3200, 3500,
    4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500,
    9000, 10000, 12000, 15000, 20000,
]
random.shuffle(med_mult_bases)

for i, base in enumerate(med_mult_bases[:25]):
    pct, direction, mult, mult_str = multiplier_scenarios[i % len(multiplier_scenarios)]
    correct = base * mult
    if direction == "increase":
        q_text = f"A \u20b1{base:,} item increases by {pct}%. What is the new price?"
        exp = (f"Multiplier for +{pct}% is {mult_str}. "
               f"\u20b1{base:,} {mult_str} = {fmt_peso(correct)}.")
    else:
        q_text = f"A \u20b1{base:,} item is discounted by {pct}%. What is the sale price?"
        exp = (f"Multiplier for −{pct}% is {mult_str}. "
               f"\u20b1{base:,} {mult_str} = {fmt_peso(correct)}.")
    choices, answer = make_numeric_choices(correct, unit="\u20b1")
    add_q("Medium", q_text, choices, answer, exp,
          ["mental math", "multiplier method", "percentage increase decrease"])


# --- M5: Estimation questions (20 questions) ---
estimation_medium = [
    (19, 500, "20% of 500 = 100; actual 19% × 500 = 95. Estimate ≈ 95–100."),
    (21, 400, "20% of 400 = 80; actual 21% × 400 = 84. Estimate ≈ 80–84."),
    (49, 820, "50% of 820 = 410; actual 49% × 820 = 401.8. Estimate ≈ 400."),
    (26, 398, "25% of 400 = 100; actual 26% × 398 ≈ 103.5. Estimate ≈ 100."),
    (11, 3000, "10% of 3,000 = 300; add 1% (30) = 330. Exact: 330."),
    (9, 4500, "10% of 4,500 = 450; subtract 1% (45) = 405. Exact: 405."),
    (48, 1200, "50% of 1,200 = 600; subtract 2% (24) = 576. Exact: 576."),
    (31, 2000, "30% of 2,000 = 600; add 1% (20) = 620. Exact: 620."),
    (74, 800, "75% of 800 = 600; subtract 1% (8) = 592. Exact: 592."),
    (6, 7500, "5% of 7,500 = 375; add 1% (75) = 450. Exact: 450."),
    (14, 3500, "15% of 3,500 = 525; subtract 1% (35) = 490. Exact: 490."),
    (24, 1600, "25% of 1,600 = 400; subtract 1% (16) = 384. Exact: 384."),
    (51, 900, "50% of 900 = 450; add 1% (9) = 459. Exact: 459."),
    (33, 1500, "33% of 1,500 = 1/3 × 1,500 = 500; close. Exact: 495."),
    (8, 12500, "10% of 12,500 = 1,250; subtract 2% (250) = 1,000. Exact: 1,000."),
    (76, 2000, "75% of 2,000 = 1,500; add 1% (20) = 1,520. Exact: 1,520."),
    (4, 8500, "1% of 8,500 = 85; × 4 = 340. Exact: 340."),
    (12, 2500, "10% of 2,500 = 250; add 2% (50) = 300. Exact: 300."),
    (18, 4000, "20% of 4,000 = 800; subtract 2% (80) = 720. Exact: 720."),
    (99, 5000, "100% − 1% = 5,000 − 50 = 4,950. Exact: 4,950."),
]
random.shuffle(estimation_medium)

for pct, base, exp_text in estimation_medium[:20]:
    correct = base * pct / 100
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"Using mental math, what is {pct}% of {base:,}?",
        choices, answer,
        exp_text,
        ["mental math", "estimation", "decomposition"]
    )


# --- M6: Practical scenarios (taxes, tips, payroll) (25 questions) ---
practical_medium_data = [
    (5600, 12, "VAT", "An item costs \u20b1{base:,} before 12% VAT. How much is the VAT?"),
    (2400, 12, "VAT", "A service costs \u20b1{base:,}. How much is the 12% VAT?"),
    (8000, 12, "VAT", "A purchase totals \u20b1{base:,} before tax. What is the 12% VAT?"),
    (15000, 3, "PhilHealth", "Monthly salary is \u20b1{base:,}. What is the 3% PhilHealth share?"),
    (20000, 4, "Pag-IBIG", "Salary is \u20b1{base:,}. What is the 4% Pag-IBIG contribution?"),
    (25000, 5, "raise", "Salary is \u20b1{base:,}. What is a 5% raise amount?"),
    (30000, 10, "bonus", "Salary is \u20b1{base:,}. What is a 10% performance bonus?"),
    (1800, 15, "tip", "A restaurant bill is \u20b1{base:,}. What is a 15% tip?"),
    (2200, 15, "tip", "Your dinner bill is \u20b1{base:,}. How much is 15% tip?"),
    (3500, 30, "discount", "A jacket costs \u20b1{base:,} with 30% off. How much is the discount?"),
    (4500, 20, "discount", "A gadget costs \u20b1{base:,} with 20% off. What is the discount?"),
    (6000, 15, "discount", "An appliance is \u20b1{base:,} with 15% off. How much do you save?"),
    (12000, 5, "waste", "A project needs \u20b1{base:,} in materials. Add 5% for waste. How much extra?"),
    (35000, 30, "rent", "Monthly salary is \u20b1{base:,}. What is 30% for rent?"),
    (28000, 20, "savings", "Salary is \u20b1{base:,}. What is 20% for savings?"),
    (40000, 10, "tax", "Salary is \u20b1{base:,}. What is 10% withholding tax?"),
    (1500, 12, "VAT", "A meal costs \u20b1{base:,}. What is the 12% VAT?"),
    (9500, 5, "fee", "A transaction of \u20b1{base:,} has a 5% fee. How much is the fee?"),
    (7200, 25, "allocation", "A budget of \u20b1{base:,} allocates 25% to supplies. How much?"),
    (18000, 15, "deduction", "Salary is \u20b1{base:,}. Total deductions are 15%. How much?"),
    (22000, 12, "VAT", "A purchase is \u20b1{base:,} before 12% VAT. What is the tax?"),
    (4000, 20, "discount", "A shirt costs \u20b1{base:,} with 20% off. What is the discount?"),
    (16000, 10, "bonus", "Salary is \u20b1{base:,}. What is a 10% mid-year bonus?"),
    (50000, 2, "fee", "A loan of \u20b1{base:,} has a 2% processing fee. How much?"),
    (3000, 12, "VAT", "A service costs \u20b1{base:,}. What is the 12% VAT?"),
]
random.shuffle(practical_medium_data)

for base, pct, context, q_template in practical_medium_data[:25]:
    correct = base * pct / 100
    q_text = q_template.format(base=base)
    ten_pct = base * 0.1
    # Build explanation using decomposition
    if pct == 12:
        exp = f"10% of \u20b1{base:,} = {fmt_peso(ten_pct)}. 2% = {fmt_peso(base*0.02)}. 12% = {fmt_peso(ten_pct)} + {fmt_peso(base*0.02)} = {fmt_peso(correct)}."
    elif pct == 15:
        exp = f"10% of \u20b1{base:,} = {fmt_peso(ten_pct)}. 5% = {fmt_peso(base*0.05)}. 15% = {fmt_peso(ten_pct)} + {fmt_peso(base*0.05)} = {fmt_peso(correct)}."
    elif pct == 30:
        exp = f"10% of \u20b1{base:,} = {fmt_peso(ten_pct)}. 30% = 10% × 3 = {fmt_peso(correct)}."
    else:
        exp = f"{pct}% of \u20b1{base:,} = \u20b1{base:,} × {pct/100} = {fmt_peso(correct)}."
    choices, answer = make_numeric_choices(correct, unit="\u20b1")
    add_q("Medium", q_text, choices, answer, exp,
          ["mental math", "practical application", "percentage shortcuts"])


# --- M7: Complementary percentage (90%, 95%, 80%) (20 questions) ---
complement_bases = [
    1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200,
    3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000, 9000, 10000,
]
complement_pcts = [90, 95, 80, 85, 99, 90, 95, 80, 85, 99,
                   90, 95, 80, 85, 99, 90, 95, 80, 85, 99]
random.shuffle(complement_bases)

for i, base in enumerate(complement_bases[:20]):
    pct = complement_pcts[i]
    complement = 100 - pct
    correct = base * pct / 100
    subtract_val = base * complement / 100
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"What is {pct}% of {base:,}?",
        choices, answer,
        f"Use complement: {pct}% = 100% − {complement}%. "
        f"{complement}% of {base:,} = {fmt_num(subtract_val)}. "
        f"{base:,} − {fmt_num(subtract_val)} = {fmt_num(correct)}.",
        ["mental math", "complementary percentage", "shortcut"]
    )

# --- M8: Fill remaining medium with varied decomposition ---
decomp_pcts_med = [
    (20, "10% × 2"),
    (30, "10% × 3"),
    (40, "50% − 10%"),
    (45, "50% − 5%"),
    (60, "50% + 10%"),
    (70, "75% − 5%"),
]
decomp_bases_med = [
    500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400,
    1500, 1600, 1700, 1800, 1900, 2000, 2200, 2400, 2600, 2800,
    3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800,
    5000, 5200, 5400, 5600, 5800, 6000, 6500, 7000, 7500, 8000,
    8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000,
]
random.shuffle(decomp_bases_med)

medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
idx = 0
while medium_count < 220 and idx < len(decomp_bases_med):
    base = decomp_bases_med[idx]
    pct, method = decomp_pcts_med[idx % len(decomp_pcts_med)]
    correct = base * pct / 100
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Medium",
        f"Using mental math shortcuts, what is {pct}% of {base:,}?",
        choices, answer,
        f"Decompose: {pct}% = {method}. Result: {fmt_num(correct)}.",
        ["mental math", "decomposition", "benchmark percentage"]
    )
    medium_count += 1
    idx += 1



# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- H1: Complex decomposition (72%, 85%, 17%, etc.) (30 questions) ---
hard_decomp_data = [
    (72, 4500, "75% − 3%", "75% of 4,500 = 3,375. 3% = 135. 72% = 3,375 − 135 = 3,240."),
    (85, 2400, "75% + 10%", "75% of 2,400 = 1,800. 10% = 240. 85% = 1,800 + 240 = 2,040."),
    (17, 3000, "15% + 2%", "15% of 3,000 = 450. 2% = 60. 17% = 450 + 60 = 510."),
    (23, 2000, "25% − 2%", "25% of 2,000 = 500. 2% = 40. 23% = 500 − 40 = 460."),
    (38, 1500, "40% − 2%", "40% of 1,500 = 600. 2% = 30. 38% = 600 − 30 = 570."),
    (62, 3000, "60% + 2%", "60% of 3,000 = 1,800. 2% = 60. 62% = 1,800 + 60 = 1,860."),
    (78, 2000, "75% + 3%", "75% of 2,000 = 1,500. 3% = 60. 78% = 1,500 + 60 = 1,560."),
    (43, 4000, "40% + 3%", "40% of 4,000 = 1,600. 3% = 120. 43% = 1,600 + 120 = 1,720."),
    (67, 1800, "66.67% + 0.33%", "2/3 of 1,800 = 1,200. Add ~6: ≈ 1,206. Exact: 67% × 1,800 = 1,206."),
    (88, 2500, "90% − 2%", "90% of 2,500 = 2,250. 2% = 50. 88% = 2,250 − 50 = 2,200."),
    (92, 3500, "90% + 2%", "90% of 3,500 = 3,150. 2% = 70. 92% = 3,150 + 70 = 3,220."),
    (13, 6000, "10% + 3%", "10% of 6,000 = 600. 3% = 180. 13% = 600 + 180 = 780."),
    (27, 4000, "25% + 2%", "25% of 4,000 = 1,000. 2% = 80. 27% = 1,000 + 80 = 1,080."),
    (56, 2500, "50% + 6%", "50% of 2,500 = 1,250. 6% = 150. 56% = 1,250 + 150 = 1,400."),
    (83, 1200, "75% + 8%", "75% of 1,200 = 900. 8% = 96. 83% = 900 + 96 = 996."),
    (7, 8500, "5% + 2%", "5% of 8,500 = 425. 2% = 170. 7% = 425 + 170 = 595."),
    (94, 5000, "95% − 1%", "95% of 5,000 = 4,750. 1% = 50. 94% = 4,750 − 50 = 4,700."),
    (36, 2500, "35% + 1%", "35% of 2,500 = 875. 1% = 25. 36% = 875 + 25 = 900."),
    (58, 3000, "60% − 2%", "60% of 3,000 = 1,800. 2% = 60. 58% = 1,800 − 60 = 1,740."),
    (41, 6000, "40% + 1%", "40% of 6,000 = 2,400. 1% = 60. 41% = 2,400 + 60 = 2,460."),
    (73, 4000, "75% − 2%", "75% of 4,000 = 3,000. 2% = 80. 73% = 3,000 − 80 = 2,920."),
    (16, 7500, "15% + 1%", "15% of 7,500 = 1,125. 1% = 75. 16% = 1,125 + 75 = 1,200."),
    (84, 3000, "85% − 1%", "85% of 3,000 = 2,550. 1% = 30. 84% = 2,550 − 30 = 2,520."),
    (29, 5000, "30% − 1%", "30% of 5,000 = 1,500. 1% = 50. 29% = 1,500 − 50 = 1,450."),
    (64, 2500, "60% + 4%", "60% of 2,500 = 1,500. 4% = 100. 64% = 1,500 + 100 = 1,600."),
    (47, 4000, "50% − 3%", "50% of 4,000 = 2,000. 3% = 120. 47% = 2,000 − 120 = 1,880."),
    (91, 2000, "90% + 1%", "90% of 2,000 = 1,800. 1% = 20. 91% = 1,800 + 20 = 1,820."),
    (68, 1500, "70% − 2%", "70% of 1,500 = 1,050. 2% = 30. 68% = 1,050 − 30 = 1,020."),
    (54, 3500, "50% + 4%", "50% of 3,500 = 1,750. 4% = 140. 54% = 1,750 + 140 = 1,890."),
    (79, 6000, "80% − 1%", "80% of 6,000 = 4,800. 1% = 60. 79% = 4,800 − 60 = 4,740."),
]
random.shuffle(hard_decomp_data)

for pct, base, method, exp_text in hard_decomp_data[:30]:
    correct = base * pct / 100
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Hard",
        f"Using mental math, compute {pct}% of {base:,}.",
        choices, answer,
        exp_text,
        ["mental math", "complex decomposition", "percentage shortcuts"]
    )


# --- H2: Successive percentage changes (25 questions) ---
successive_data = [
    (2000, 10, 10, "increase", "decrease",
     "After +10%: 2,000 × 1.1 = 2,200. After −10%: 2,200 × 0.9 = 1,980."),
    (5000, 20, 20, "increase", "decrease",
     "After +20%: 5,000 × 1.2 = 6,000. After −20%: 6,000 × 0.8 = 4,800."),
    (3000, 25, 20, "increase", "decrease",
     "After +25%: 3,000 × 1.25 = 3,750. After −20%: 3,750 × 0.8 = 3,000."),
    (4000, 10, 20, "increase", "increase",
     "After +10%: 4,000 × 1.1 = 4,400. After +20%: 4,400 × 1.2 = 5,280."),
    (6000, 50, 50, "increase", "decrease",
     "After +50%: 6,000 × 1.5 = 9,000. After −50%: 9,000 × 0.5 = 4,500."),
    (8000, 25, 25, "decrease", "decrease",
     "After −25%: 8,000 × 0.75 = 6,000. After −25%: 6,000 × 0.75 = 4,500."),
    (1500, 20, 10, "increase", "decrease",
     "After +20%: 1,500 × 1.2 = 1,800. After −10%: 1,800 × 0.9 = 1,620."),
    (2500, 10, 10, "increase", "increase",
     "After +10%: 2,500 × 1.1 = 2,750. After +10%: 2,750 × 1.1 = 3,025."),
    (4800, 25, 10, "increase", "decrease",
     "After +25%: 4,800 × 1.25 = 6,000. After −10%: 6,000 × 0.9 = 5,400."),
    (10000, 10, 20, "decrease", "increase",
     "After −10%: 10,000 × 0.9 = 9,000. After +20%: 9,000 × 1.2 = 10,800."),
    (3600, 50, 25, "decrease", "increase",
     "After −50%: 3,600 × 0.5 = 1,800. After +25%: 1,800 × 1.25 = 2,250."),
    (7200, 25, 50, "increase", "decrease",
     "After +25%: 7,200 × 1.25 = 9,000. After −50%: 9,000 × 0.5 = 4,500."),
    (2000, 50, 10, "increase", "increase",
     "After +50%: 2,000 × 1.5 = 3,000. After +10%: 3,000 × 1.1 = 3,300."),
    (5000, 20, 25, "decrease", "decrease",
     "After −20%: 5,000 × 0.8 = 4,000. After −25%: 4,000 × 0.75 = 3,000."),
    (1200, 25, 20, "increase", "increase",
     "After +25%: 1,200 × 1.25 = 1,500. After +20%: 1,500 × 1.2 = 1,800."),
    (9000, 10, 10, "decrease", "decrease",
     "After −10%: 9,000 × 0.9 = 8,100. After −10%: 8,100 × 0.9 = 7,290."),
    (4000, 50, 20, "decrease", "increase",
     "After −50%: 4,000 × 0.5 = 2,000. After +20%: 2,000 × 1.2 = 2,400."),
    (6000, 10, 50, "increase", "decrease",
     "After +10%: 6,000 × 1.1 = 6,600. After −50%: 6,600 × 0.5 = 3,300."),
    (3000, 20, 10, "decrease", "increase",
     "After −20%: 3,000 × 0.8 = 2,400. After +10%: 2,400 × 1.1 = 2,640."),
    (8000, 10, 25, "increase", "decrease",
     "After +10%: 8,000 × 1.1 = 8,800. After −25%: 8,800 × 0.75 = 6,600."),
    (1600, 25, 10, "decrease", "increase",
     "After −25%: 1,600 × 0.75 = 1,200. After +10%: 1,200 × 1.1 = 1,320."),
    (2400, 50, 20, "increase", "decrease",
     "After +50%: 2,400 × 1.5 = 3,600. After −20%: 3,600 × 0.8 = 2,880."),
    (5000, 10, 50, "decrease", "increase",
     "After −10%: 5,000 × 0.9 = 4,500. After +50%: 4,500 × 1.5 = 6,750."),
    (7500, 20, 20, "increase", "increase",
     "After +20%: 7,500 × 1.2 = 9,000. After +20%: 9,000 × 1.2 = 10,800."),
    (4000, 25, 20, "decrease", "increase",
     "After −25%: 4,000 × 0.75 = 3,000. After +20%: 3,000 × 1.2 = 3,600."),
]
random.shuffle(successive_data)

for base, pct1, pct2, dir1, dir2, exp_text in successive_data[:25]:
    mult1 = (1 + pct1/100) if dir1 == "increase" else (1 - pct1/100)
    mult2 = (1 + pct2/100) if dir2 == "increase" else (1 - pct2/100)
    correct = base * mult1 * mult2
    dir1_word = "increased" if dir1 == "increase" else "decreased"
    dir2_word = "increased" if dir2 == "increase" else "decreased"
    q_text = (f"A \u20b1{base:,} item is {dir1_word} by {pct1}%, "
              f"then {dir2_word} by {pct2}%. What is the final price?")
    choices, answer = make_numeric_choices(correct, unit="\u20b1")
    add_q("Hard", q_text, choices, answer, exp_text,
          ["mental math", "successive percentage change", "multiplier method"])


# --- H3: Reverse percentage problems (25 questions) ---
reverse_data = [
    (2400, 20, "discount", "If the sale price is \u20b1{sale:,} after a 20% discount, what was the original price?",
     "Sale price = Original × 0.8. Original = \u20b1{sale:,} ÷ 0.8 = {orig}."),
    (1800, 10, "discount", "After a 10% discount, an item costs \u20b1{sale:,}. What was the original price?",
     "Sale price = Original × 0.9. Original = \u20b1{sale:,} ÷ 0.9 = {orig}."),
    (3750, 25, "discount", "An item costs \u20b1{sale:,} after a 25% discount. Original price?",
     "Sale price = Original × 0.75. Original = \u20b1{sale:,} ÷ 0.75 = {orig}."),
    (2500, 50, "discount", "After a 50% discount, the price is \u20b1{sale:,}. What was the original?",
     "Sale price = Original × 0.5. Original = \u20b1{sale:,} ÷ 0.5 = {orig}."),
    (1100, 10, "increase", "After a 10% increase, a salary is \u20b1{sale:,}. What was the original?",
     "New = Original × 1.1. Original = \u20b1{sale:,} ÷ 1.1 = {orig}."),
    (1200, 20, "increase", "After a 20% raise, a salary is \u20b1{sale:,}. What was the original?",
     "New = Original × 1.2. Original = \u20b1{sale:,} ÷ 1.2 = {orig}."),
    (1250, 25, "increase", "After a 25% increase, the value is \u20b1{sale:,}. Original value?",
     "New = Original × 1.25. Original = \u20b1{sale:,} ÷ 1.25 = {orig}."),
    (1500, 50, "increase", "After a 50% increase, the amount is \u20b1{sale:,}. What was the original?",
     "New = Original × 1.5. Original = \u20b1{sale:,} ÷ 1.5 = {orig}."),
]

reverse_bases = [
    2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500,
    7000, 7500, 8000, 8500, 9000, 10000, 12000, 15000, 18000, 20000,
    22000, 24000, 25000, 28000, 30000,
]
random.shuffle(reverse_bases)

for i, orig_base in enumerate(reverse_bases[:25]):
    template = reverse_data[i % len(reverse_data)]
    sale_val_template, pct, direction, q_template, exp_template = template
    if direction == "discount":
        mult = 1 - pct / 100
    else:
        mult = 1 + pct / 100
    sale_price = orig_base * mult
    # Ensure clean numbers
    sale_price = round(sale_price)
    q_text = q_template.format(sale=sale_price)
    exp_text = exp_template.format(sale=sale_price, orig=fmt_peso(orig_base))
    choices, answer = make_numeric_choices(orig_base, unit="\u20b1")
    add_q("Hard", q_text, choices, answer, exp_text,
          ["mental math", "reverse percentage", "working backward"])


# --- H4: Estimation with messy numbers (25 questions) ---
hard_estimation_data = [
    (17, 4873, "≈ 17% of 4,900 ≈ 15% + 2% = 735 + 98 = 833. Exact: 828.41."),
    (23, 7891, "≈ 25% of 7,900 = 1,975; subtract 2% (158) ≈ 1,817. Exact: 1,814.93."),
    (38, 2647, "≈ 40% of 2,650 = 1,060; subtract 2% (53) ≈ 1,007. Exact: 1,005.86."),
    (67, 3219, "≈ 2/3 of 3,200 ≈ 2,133; add small amount. Exact: 2,156.73."),
    (82, 4567, "≈ 80% of 4,600 = 3,680; add 2% (92) ≈ 3,772. Exact: 3,744.94."),
    (14, 8923, "≈ 15% of 9,000 = 1,350; subtract 1% (90) ≈ 1,260. Exact: 1,249.22."),
    (43, 5678, "≈ 40% of 5,700 = 2,280; add 3% (171) ≈ 2,451. Exact: 2,441.54."),
    (76, 3412, "≈ 75% of 3,400 = 2,550; add 1% (34) ≈ 2,584. Exact: 2,593.12."),
    (29, 6789, "≈ 30% of 6,800 = 2,040; subtract 1% (68) ≈ 1,972. Exact: 1,968.81."),
    (56, 4321, "≈ 50% of 4,300 = 2,150; add 6% (258) ≈ 2,408. Exact: 2,419.76."),
    (91, 2345, "≈ 90% of 2,350 = 2,115; add 1% (23) ≈ 2,138. Exact: 2,133.95."),
    (8, 9876, "≈ 10% of 9,900 = 990; subtract 2% (198) ≈ 792. Exact: 790.08."),
    (63, 1987, "≈ 60% of 2,000 = 1,200; add 3% (60) ≈ 1,260. Exact: 1,251.81."),
    (37, 5432, "≈ 40% of 5,400 = 2,160; subtract 3% (162) ≈ 1,998. Exact: 2,009.84."),
    (88, 3765, "≈ 90% of 3,800 = 3,420; subtract 2% (76) ≈ 3,344. Exact: 3,313.2."),
    (22, 8765, "≈ 20% of 8,800 = 1,760; add 2% (176) ≈ 1,936. Exact: 1,928.3."),
    (46, 6543, "≈ 50% of 6,500 = 3,250; subtract 4% (260) ≈ 2,990. Exact: 3,009.78."),
    (71, 2876, "≈ 70% of 2,900 = 2,030; add 1% (29) ≈ 2,059. Exact: 2,041.96."),
    (19, 5234, "≈ 20% of 5,200 = 1,040; subtract 1% (52) ≈ 988. Exact: 994.46."),
    (53, 7654, "≈ 50% of 7,700 = 3,850; add 3% (231) ≈ 4,081. Exact: 4,056.62."),
    (34, 4567, "≈ 35% of 4,600 = 1,610; subtract 1% (46) ≈ 1,564. Exact: 1,552.78."),
    (77, 3298, "≈ 75% of 3,300 = 2,475; add 2% (66) ≈ 2,541. Exact: 2,539.46."),
    (11, 9087, "≈ 10% of 9,100 = 910; add 1% (91) ≈ 1,001. Exact: 999.57."),
    (86, 2345, "≈ 85% of 2,350 = 1,998; add 1% (23) ≈ 2,021. Exact: 2,016.7."),
    (59, 4123, "≈ 60% of 4,100 = 2,460; subtract 1% (41) ≈ 2,419. Exact: 2,432.57."),
]
random.shuffle(hard_estimation_data)

for pct, base, exp_text in hard_estimation_data[:25]:
    correct = round(base * pct / 100, 2)
    # Round correct to nearest whole for cleaner choices
    correct_rounded = round(correct)
    choices, answer = make_numeric_choices(correct_rounded, spread="tight")
    add_q(
        "Hard",
        f"Estimate {pct}% of {base:,} using mental math. Which is closest?",
        choices, answer,
        exp_text,
        ["mental math", "estimation", "messy numbers"]
    )


# --- H5: "What percent is X of Y?" mental computation (25 questions) ---
what_pct_data = [
    (375, 1500, 25, "375/1,500 = 1/4 = 25%."),
    (240, 800, 30, "240/800 = 24/80 = 3/10 = 30%."),
    (180, 720, 25, "180/720 = 18/72 = 1/4 = 25%."),
    (450, 1800, 25, "450/1,800 = 45/180 = 1/4 = 25%."),
    (600, 2400, 25, "600/2,400 = 1/4 = 25%."),
    (150, 600, 25, "150/600 = 1/4 = 25%."),
    (200, 500, 40, "200/500 = 2/5 = 40%."),
    (350, 700, 50, "350/700 = 1/2 = 50%."),
    (120, 480, 25, "120/480 = 12/48 = 1/4 = 25%."),
    (900, 1200, 75, "900/1,200 = 9/12 = 3/4 = 75%."),
    (160, 640, 25, "160/640 = 16/64 = 1/4 = 25%."),
    (500, 2000, 25, "500/2,000 = 1/4 = 25%."),
    (300, 900, 33.33, "300/900 = 1/3 ≈ 33.33%."),
    (400, 1600, 25, "400/1,600 = 1/4 = 25%."),
    (250, 1000, 25, "250/1,000 = 1/4 = 25%."),
    (480, 1200, 40, "480/1,200 = 48/120 = 2/5 = 40%."),
    (360, 1200, 30, "360/1,200 = 36/120 = 3/10 = 30%."),
    (840, 1200, 70, "840/1,200 = 84/120 = 7/10 = 70%."),
    (125, 500, 25, "125/500 = 1/4 = 25%."),
    (750, 3000, 25, "750/3,000 = 1/4 = 25%."),
    (320, 800, 40, "320/800 = 32/80 = 2/5 = 40%."),
    (560, 800, 70, "560/800 = 56/80 = 7/10 = 70%."),
    (180, 600, 30, "180/600 = 18/60 = 3/10 = 30%."),
    (420, 600, 70, "420/600 = 42/60 = 7/10 = 70%."),
    (225, 900, 25, "225/900 = 1/4 = 25%."),
]
random.shuffle(what_pct_data)

for part, whole, pct_answer, exp_text in what_pct_data[:25]:
    choices, answer = make_pct_choices(pct_answer)
    add_q(
        "Hard",
        f"Using mental math, what percent is {part:,} of {whole:,}?",
        choices, answer,
        exp_text,
        ["mental math", "finding the rate", "fraction recognition"]
    )


# --- H6: Multi-step practical word problems (30 questions) ---
hard_practical = [
    ("A government office has 250 employees. If 68% are permanent, how many are contractual?",
     80, "Contractual = 100% − 68% = 32%. 32% of 250: 25% = 62.5, 7% = 17.5, total = 80."),
    ("A budget of \u20b12.4M allocates 35% to salaries and 15% to utilities. How much remains?",
     1200000, "35% + 15% = 50% allocated. Remaining = 50% of 2,400,000 = \u20b11,200,000."),
    ("An employee earns \u20b128,000. After a 10% raise and then 5% tax on the new salary, what is the take-home?",
     29260, "After 10% raise: 28,000 × 1.1 = 30,800. After 5% tax: 30,800 × 0.95 = 29,260."),
    ("A store marks up an item by 50% then offers 20% off. If the cost was \u20b12,000, what is the selling price?",
     2400, "After 50% markup: 2,000 × 1.5 = 3,000. After 20% off: 3,000 × 0.8 = 2,400."),
    ("Population grew from 12,000 to 15,000. What is the percent increase?",
     25, "Change = 3,000. 3,000/12,000 = 1/4 = 25%."),
    ("A salary decreased from \u20b140,000 to \u20b134,000. What percent decrease?",
     15, "Change = 6,000. 6,000/40,000 = 6/40 = 3/20 = 15%."),
    ("If 12% VAT is added to \u20b18,500, what is the total amount?",
     9520, "12% of 8,500: 10% = 850, 2% = 170. VAT = 1,020. Total = 8,500 + 1,020 = 9,520."),
    ("A project budget is \u20b1500,000. If 45% is spent, how much remains?",
     275000, "Remaining = 100% − 45% = 55%. 55% of 500,000: 50% = 250,000, 5% = 25,000. Total = 275,000."),
    ("An item's price dropped from \u20b13,200 to \u20b12,400. What percent decrease?",
     25, "Change = 800. 800/3,200 = 8/32 = 1/4 = 25%."),
    ("A student scored 42 out of 56. What is the percentage score?",
     75, "42/56 = 6/8 = 3/4 = 75%."),
    ("Monthly expenses: rent 30%, food 25%, transport 10%, savings 20%. What percent is unaccounted?",
     15, "30 + 25 + 10 + 20 = 85%. Unaccounted = 100% − 85% = 15%."),
    ("A \u20b115,000 appliance depreciates 20% per year. Value after 2 years?",
     9600, "Year 1: 15,000 × 0.8 = 12,000. Year 2: 12,000 × 0.8 = 9,600."),
    ("If 3/8 of 4,000 employees are female, how many are male?",
     2500, "3/8 = 37.5% female = 1,500. Male = 4,000 − 1,500 = 2,500 (or 5/8 × 4,000)."),
    ("A fare increased by 25% from \u20b112. What is the new fare?",
     15, "25% of 12 = 3. New fare = 12 + 3 = \u20b115."),
    ("A department's budget was cut by 15% from \u20b1800,000. New budget?",
     680000, "15% of 800,000: 10% = 80,000, 5% = 40,000. Cut = 120,000. New = 680,000."),
    ("An investment of \u20b150,000 earns 8% annually. How much interest after 1 year?",
     4000, "8% of 50,000: 10% = 5,000, subtract 2% (1,000) = 4,000."),
    ("A survey of 2,000 people: 45% agree, 30% disagree. How many are undecided?",
     500, "Undecided = 100% − 45% − 30% = 25%. 25% of 2,000 = 500."),
    ("A contractor estimates 5% material waste on \u20b1240,000 worth of supplies. Total cost with waste?",
     252000, "5% of 240,000 = 12,000. Total = 240,000 + 12,000 = 252,000."),
    ("If a \u20b16,400 item is sold at 87.5% of its price, what is the selling price?",
     5600, "87.5% = 7/8. 6,400 ÷ 8 = 800, × 7 = 5,600."),
    ("A class of 40 students: 75% passed. How many failed?",
     10, "Passed = 75% of 40 = 30. Failed = 40 − 30 = 10 (or 25% of 40 = 10)."),
    ("Monthly salary is \u20b132,000. Deductions: 3% PhilHealth, 2% Pag-IBIG, 10% tax. Net pay?",
     27200, "Total deductions = 15%. 15% of 32,000 = 4,800. Net = 32,000 − 4,800 = 27,200."),
    ("A barangay's population is 8,500. If it grows by 4%, what is the new population?",
     8840, "4% of 8,500: 1% = 85, × 4 = 340. New = 8,500 + 340 = 8,840."),
    ("A \u20b14,000 phone is on sale: 10% off, then additional 5% off the discounted price. Final price?",
     3420, "After 10% off: 4,000 × 0.9 = 3,600. After 5% off: 3,600 × 0.95 = 3,420."),
    ("Out of 1,200 applicants, 5/6 passed the screening. How many were eliminated?",
     200, "5/6 passed = 1,000. Eliminated = 1,200 − 1,000 = 200 (or 1/6 of 1,200 = 200)."),
    ("A \u20b125,000 salary: 12% goes to rent, 8% to transport. Combined amount?",
     5000, "12% + 8% = 20%. 20% of 25,000 = 5,000."),
    ("A tank is 60% full with 450 liters. What is the tank's full capacity?",
     750, "60% = 450 liters. 100% = 450 ÷ 0.6 = 750 liters."),
    ("If prices increase by 12% and your budget stays at \u20b110,000, how much purchasing power do you lose?",
     1071, "New cost of same goods: 10,000 × 1.12 = 11,200. Loss = 11,200 − 10,000 = 1,200. Or: you can now buy 10,000/11,200 ≈ 89.3% of what you could before, losing ≈ \u20b11,071 in value."),
    ("A company's revenue grew 20% to \u20b13.6M. What was last year's revenue?",
     3000000, "This year = Last year × 1.2. Last year = 3,600,000 ÷ 1.2 = 3,000,000."),
    ("An exam has 80 items. A student got 87.5% correct. How many wrong?",
     10, "87.5% = 7/8. Correct = 7/8 × 80 = 70. Wrong = 80 − 70 = 10."),
    ("A \u20b160,000 investment lost 10% in year 1 and gained 10% in year 2. Final value?",
     59400, "Year 1: 60,000 × 0.9 = 54,000. Year 2: 54,000 × 1.1 = 59,400."),
]
random.shuffle(hard_practical)

for q_text, correct_val, exp_text in hard_practical[:30]:
    # Determine if answer is a percentage or a number
    if correct_val <= 100 and "percent" in q_text.lower():
        choices, answer = make_pct_choices(correct_val)
    elif "\u20b1" in q_text and correct_val > 100:
        choices, answer = make_numeric_choices(correct_val, unit="\u20b1")
    else:
        choices, answer = make_numeric_choices(correct_val)
    add_q("Hard", q_text, choices, answer, exp_text,
          ["mental math", "multi-step", "practical application", "word problem"])


# --- H7: Shortcut identification / strategy questions (20 questions) ---
strategy_hard = [
    ("What is the fastest way to compute 75% of 2,800?",
     ["Divide by 4, multiply by 3", "Multiply by 0.75 directly",
      "Find 50% + 50% of 50%", "Find 100% − 25%"],
     "Divide by 4, multiply by 3",
     "75% = 3/4. Dividing by 4 then multiplying by 3 uses simple arithmetic: 2,800 ÷ 4 = 700, × 3 = 2,100."),
    ("To find 95% of a number mentally, the best shortcut is:",
     ["Subtract 5% from the number", "Multiply by 0.95",
      "Find 90% + 5%", "Find 100% − 10% + 5%"],
     "Subtract 5% from the number",
     "95% = 100% − 5%. Finding 5% (half of 10%) and subtracting is fastest."),
    ("To compute 12% of \u20b15,000 mentally, the most efficient decomposition is:",
     ["10% + 2%", "6% × 2", "1% × 12", "25% − 13%"],
     "10% + 2%",
     "10% of 5,000 = 500. 2% = 100. Total = 600. This uses the fewest mental steps."),
    ("What is 37.5% as a fraction?",
     ["3/8", "3/4", "5/8", "3/16"],
     "3/8",
     "37.5% = 37.5/100 = 375/1000 = 3/8."),
    ("Which benchmark decomposition is correct for 45%?",
     ["50% − 5%", "40% + 10%", "25% + 25%", "10% × 4.5"],
     "50% − 5%",
     "45% = 50% − 5%. This is efficient because both 50% and 5% are easy benchmarks."),
    ("To find 8% of a number, the fastest mental method is:",
     ["10% minus 2%", "1% times 8", "5% plus 3%", "4% times 2"],
     "10% minus 2%",
     "10% − 2% requires only two simple operations: find 10%, find 2% (or 1% × 2), subtract."),
    ("What multiplier represents a 25% decrease?",
     ["0.75", "0.25", "1.25", "0.80"],
     "0.75",
     "A 25% decrease means keeping 75% of the original: multiplier = 1 − 0.25 = 0.75."),
    ("If 10% of a number is 340, what is 30% of that number?",
     ["1,020", "340", "3,400", "102"],
     "1,020",
     "If 10% = 340, then 30% = 340 × 3 = 1,020."),
    ("If 25% of a number is 600, what is 75% of that number?",
     ["1,800", "600", "2,400", "450"],
     "1,800",
     "If 25% = 600, then 75% = 600 × 3 = 1,800."),
    ("If 1% of a number is 45, what is the number?",
     ["4,500", "450", "45,000", "4.5"],
     "4,500",
     "If 1% = 45, then 100% = 45 × 100 = 4,500."),
    ("Which is NOT equivalent to 62.5%?",
     ["5/6", "5/8", "0.625", "62.5/100"],
     "5/6",
     "62.5% = 5/8 = 0.625. But 5/6 ≈ 83.33%, which is different."),
    ("A price increases by 20% then decreases by 20%. The net effect is:",
     ["4% decrease", "No change", "4% increase", "2% decrease"],
     "4% decrease",
     "× 1.2 × 0.8 = 0.96 = 96% of original. Net effect: 4% decrease."),
    ("A price decreases by 10% then increases by 10%. The net effect is:",
     ["1% decrease", "No change", "1% increase", "10% decrease"],
     "1% decrease",
     "× 0.9 × 1.1 = 0.99 = 99% of original. Net effect: 1% decrease."),
    ("If 5% of a number is 75, what is 20% of that number?",
     ["300", "75", "150", "1,500"],
     "300",
     "If 5% = 75, then 1% = 15, so 20% = 15 × 20 = 300."),
    ("To estimate 33% of 9,100, the best approach is:",
     ["Divide by 3", "Multiply by 0.33", "Find 30% + 3%", "Find 25% + 8%"],
     "Divide by 3",
     "33% ≈ 1/3. 9,100 ÷ 3 ≈ 3,033. This is the fastest single-step method."),
    ("What is the complement of 87.5%?",
     ["12.5%", "13.5%", "22.5%", "7.5%"],
     "12.5%",
     "100% − 87.5% = 12.5%. Knowing complements helps compute large percentages by subtraction."),
    ("If an item costs \u20b11,000 after a 20% discount, the original price was:",
     ["\u20b11,250", "\u20b11,200", "\u20b11,000", "\u20b11,500"],
     "\u20b11,250",
     "Sale price = Original × 0.8. Original = 1,000 ÷ 0.8 = 1,250."),
    ("Two successive 50% discounts are equivalent to a single discount of:",
     ["75%", "100%", "50%", "25%"],
     "75%",
     "× 0.5 × 0.5 = 0.25 remaining = 75% total discount."),
    ("Three successive 10% increases are equivalent to approximately:",
     ["33.1% increase", "30% increase", "31% increase", "13.1% increase"],
     "33.1% increase",
     "1.1 × 1.1 × 1.1 = 1.331. Net increase = 33.1%."),
    ("If 50% of a number equals 10% of 3,000, what is the number?",
     ["600", "300", "1,500", "6,000"],
     "600",
     "10% of 3,000 = 300. So 50% of the number = 300. The number = 300 × 2 = 600."),
]
random.shuffle(strategy_hard)

for q_text, ch, ans, exp in strategy_hard[:20]:
    add_q("Hard", q_text, ch, ans, exp,
          ["mental math", "strategy", "shortcut identification"])


# --- H8: Fill remaining hard with complex applied problems ---
hard_fill_data = [
    (8, 37500, "10% of 37,500 = 3,750. 2% = 750. 8% = 3,750 − 750 = 3,000."),
    (16, 7500, "15% of 7,500 = 1,125. 1% = 75. 16% = 1,125 + 75 = 1,200."),
    (22, 4500, "20% of 4,500 = 900. 2% = 90. 22% = 900 + 90 = 990."),
    (28, 2500, "25% of 2,500 = 625. 3% = 75. 28% = 625 + 75 = 700."),
    (33, 6000, "33% of 6,000 ≈ 1/3 × 6,000 = 2,000. Exact: 1,980."),
    (44, 5000, "40% of 5,000 = 2,000. 4% = 200. 44% = 2,000 + 200 = 2,200."),
    (55, 3600, "50% of 3,600 = 1,800. 5% = 180. 55% = 1,800 + 180 = 1,980."),
    (66, 1500, "66% of 1,500 ≈ 2/3 × 1,500 = 1,000. Exact: 990."),
    (77, 4000, "75% of 4,000 = 3,000. 2% = 80. 77% = 3,000 + 80 = 3,080."),
    (88, 2500, "90% of 2,500 = 2,250. 2% = 50. 88% = 2,250 − 50 = 2,200."),
    (93, 3000, "90% of 3,000 = 2,700. 3% = 90. 93% = 2,700 + 90 = 2,790."),
    (97, 4000, "100% − 3% = 4,000 − 120 = 3,880."),
    (3, 15000, "1% of 15,000 = 150. 3% = 150 × 3 = 450."),
    (6, 8500, "5% of 8,500 = 425. 1% = 85. 6% = 425 + 85 = 510."),
    (14, 3500, "10% of 3,500 = 350. 4% = 140. 14% = 350 + 140 = 490."),
    (18, 4500, "20% of 4,500 = 900. 2% = 90. 18% = 900 − 90 = 810."),
    (24, 7500, "25% of 7,500 = 1,875. 1% = 75. 24% = 1,875 − 75 = 1,800."),
    (31, 2000, "30% of 2,000 = 600. 1% = 20. 31% = 600 + 20 = 620."),
    (39, 4000, "40% of 4,000 = 1,600. 1% = 40. 39% = 1,600 − 40 = 1,560."),
    (46, 3000, "45% of 3,000 = 1,350. 1% = 30. 46% = 1,350 + 30 = 1,380."),
    (52, 5000, "50% of 5,000 = 2,500. 2% = 100. 52% = 2,500 + 100 = 2,600."),
    (61, 2000, "60% of 2,000 = 1,200. 1% = 20. 61% = 1,200 + 20 = 1,220."),
    (69, 4000, "70% of 4,000 = 2,800. 1% = 40. 69% = 2,800 − 40 = 2,760."),
    (74, 6000, "75% of 6,000 = 4,500. 1% = 60. 74% = 4,500 − 60 = 4,440."),
    (81, 2000, "80% of 2,000 = 1,600. 1% = 20. 81% = 1,600 + 20 = 1,620."),
    (86, 5000, "85% of 5,000 = 4,250. 1% = 50. 86% = 4,250 + 50 = 4,300."),
    (96, 2500, "95% of 2,500 = 2,375. 1% = 25. 96% = 2,375 + 25 = 2,400."),
    (2, 45000, "1% of 45,000 = 450. 2% = 450 × 2 = 900."),
    (4, 12500, "1% of 12,500 = 125. 4% = 125 × 4 = 500."),
    (9, 6000, "10% of 6,000 = 600. 1% = 60. 9% = 600 − 60 = 540."),
]
random.shuffle(hard_fill_data)

hard_count = len([q for q in questions if q["difficulty"] == "Hard"])
idx = 0
while hard_count < 210 and idx < len(hard_fill_data):
    pct, base, exp_text = hard_fill_data[idx]
    correct = base * pct / 100
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Hard",
        f"Compute {pct}% of {base:,} using mental math shortcuts.",
        choices, answer,
        exp_text,
        ["mental math", "decomposition", "percentage shortcuts"]
    )
    hard_count += 1
    idx += 1



# ============================================================
# VALIDATION AND OUTPUT
# ============================================================

def validate_questions() -> None:
    """Validate all generated questions."""
    print(f"Total questions generated: {len(questions)}")
    easy = len([q for q in questions if q["difficulty"] == "Easy"])
    medium = len([q for q in questions if q["difficulty"] == "Medium"])
    hard = len([q for q in questions if q["difficulty"] == "Hard"])
    print(f"  Easy: {easy}, Medium: {medium}, Hard: {hard}")

    errors = 0
    for q in questions:
        if q["answer"] not in q["choices"]:
            print(f"  ERROR: Q{q['id']} answer '{q['answer']}' not in choices: {q['choices']}")
            errors += 1
        if len(q["choices"]) != 4:
            print(f"  ERROR: Q{q['id']} has {len(q['choices'])} choices (expected 4)")
            errors += 1
        if len(set(q["choices"])) != 4:
            print(f"  WARNING: Q{q['id']} has duplicate choices: {q['choices']}")
            errors += 1

    if errors:
        print(f"\n  {errors} errors/warnings found!")
    else:
        print("  All questions validated successfully.")


def main() -> None:
    validate_questions()

    # Trim to 600 total (200 per difficulty)
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
