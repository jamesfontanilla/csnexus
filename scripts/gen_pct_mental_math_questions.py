"""
Generate 600 questions for Percentage Mental Math and Shortcuts (CSE Numerical Ability).
200 Easy / 200 Medium / 200 Hard

Covers:
- Fraction-percent equivalents
- Benchmark percentage recognition
- Estimation problems
- Rapid mental computation (10%, 5%, 1% shortcuts)
- Percentage increase and decrease estimation
- Practical mental math applications
- Shortcut identification
- Approximation analysis
- Business and financial estimation
- Real-life numerical reasoning

Run: python scripts/gen_pct_mental_math_questions.py
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


def fmt_currency(val: float) -> str:
    """Format as Philippine Peso."""
    if val == int(val):
        return f"\u20b1{int(val):,}"
    return f"\u20b1{val:,.2f}"


def make_numeric_choices(correct: float, style: str = "plain") -> tuple[list[str], str]:
    """Generate 4 numeric choices with plausible distractors."""
    if style == "currency":
        fmt = fmt_currency
    else:
        fmt = fmt_num

    correct_str = fmt(correct)
    distractors: set[str] = set()
    attempts = 0

    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_10pct", "double", "half", "decimal_shift",
            "off_small", "off_large", "complement"
        ])
        if error_type == "off_10pct":
            d = correct * random.choice([0.9, 1.1, 0.8, 1.2])
        elif error_type == "double":
            d = correct * 2
        elif error_type == "half":
            d = correct / 2
        elif error_type == "decimal_shift":
            d = correct * random.choice([10, 0.1])
        elif error_type == "off_small":
            offset = correct * random.choice([0.05, 0.15, -0.05, -0.15, 0.25, -0.25])
            d = correct + offset
        elif error_type == "off_large":
            offset = correct * random.choice([0.5, -0.5, 0.75, -0.3])
            d = correct + offset
        elif error_type == "complement":
            # For percentage-of problems, a common error is computing the complement
            d = correct * random.choice([3, 1.5, 0.667])
        else:
            d = correct + random.randint(1, 50)

        if style == "currency":
            d = round(d, 2)
        else:
            d = round(d, 2) if d != int(d) else d

        d_str = fmt(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    # Fallback
    while len(distractors) < 3:
        d = correct + (len(distractors) + 1) * max(1, correct * 0.1)
        d_str = fmt(round(d, 2) if d != int(d) else d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


def make_pct_choices(correct_pct: float) -> tuple[list[str], str]:
    """Generate 4 percentage choices."""
    def fmt_p(v: float) -> str:
        if v == int(v):
            return f"{int(v)}%"
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return f"{s}%"

    correct_str = fmt_p(correct_pct)
    distractors: set[str] = set()
    attempts = 0

    while len(distractors) < 3 and attempts < 300:
        error_type = random.choice([
            "off_5", "off_10", "double", "half", "complement", "decimal_err"
        ])
        if error_type == "off_5":
            d = correct_pct + random.choice([-5, 5, -3, 3, -8, 8])
        elif error_type == "off_10":
            d = correct_pct + random.choice([-10, 10, -15, 15, -20, 20])
        elif error_type == "double":
            d = correct_pct * 2
        elif error_type == "half":
            d = correct_pct / 2
        elif error_type == "complement":
            d = 100 - correct_pct
        elif error_type == "decimal_err":
            d = correct_pct * random.choice([10, 0.1])
        else:
            d = correct_pct + random.randint(-10, 10)

        d = round(d, 2)
        d_str = fmt_p(d)
        if d_str != correct_str and d > 0 and d_str not in distractors:
            distractors.add(d_str)
        attempts += 1

    while len(distractors) < 3:
        d = correct_pct + (len(distractors) + 1) * 5
        d_str = fmt_p(d)
        if d_str != correct_str and d_str not in distractors:
            distractors.add(d_str)

    choices = [correct_str] + list(distractors)[:3]
    random.shuffle(choices)
    return choices, correct_str


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- E1: 10% of a number (40 questions) ---
easy_10pct_bases = [
    200, 350, 450, 500, 600, 750, 800, 900, 1000, 1200,
    1500, 1800, 2000, 2400, 2500, 3000, 3500, 4000, 4500, 5000,
    5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000,
    12000, 15000, 18000, 20000, 25000, 30000, 35000, 40000, 45000, 50000,
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

# --- E2: 50% of a number (30 questions) ---
easy_50pct_bases = [
    120, 240, 360, 480, 500, 600, 700, 800, 900, 1000,
    1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000,
    3200, 3600, 4000, 4400, 4800, 5000, 6000, 7000, 8000, 10000,
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

# --- E3: 25% of a number (30 questions) ---
easy_25pct_bases = [
    80, 120, 160, 200, 240, 280, 320, 360, 400, 440,
    480, 520, 560, 600, 640, 720, 800, 840, 960, 1000,
    1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4800, 6000,
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
    ("1/2", "50%", ["50%", "25%", "75%", "20%"]),
    ("1/4", "25%", ["25%", "50%", "20%", "75%"]),
    ("3/4", "75%", ["75%", "25%", "50%", "80%"]),
    ("1/5", "20%", ["20%", "25%", "10%", "15%"]),
    ("2/5", "40%", ["40%", "20%", "60%", "25%"]),
    ("3/5", "60%", ["60%", "40%", "75%", "30%"]),
    ("4/5", "80%", ["80%", "60%", "75%", "40%"]),
    ("1/10", "10%", ["10%", "1%", "20%", "5%"]),
    ("3/10", "30%", ["30%", "33%", "13%", "20%"]),
    ("7/10", "70%", ["70%", "17%", "30%", "75%"]),
    ("9/10", "90%", ["90%", "19%", "80%", "95%"]),
    ("1/3", "33.33%", ["33.33%", "30%", "25%", "66.67%"]),
    ("2/3", "66.67%", ["66.67%", "33.33%", "60%", "75%"]),
    ("1/8", "12.5%", ["12.5%", "18%", "8%", "25%"]),
    ("3/8", "37.5%", ["37.5%", "38%", "33%", "75%"]),
    ("5/8", "62.5%", ["62.5%", "58%", "65%", "50%"]),
    ("7/8", "87.5%", ["87.5%", "78%", "88%", "75%"]),
    ("1/20", "5%", ["5%", "20%", "10%", "2%"]),
    ("1/25", "4%", ["4%", "25%", "5%", "2.5%"]),
    ("1/50", "2%", ["2%", "5%", "50%", "0.2%"]),
    ("1/100", "1%", ["1%", "10%", "100%", "0.1%"]),
    ("1/6", "16.67%", ["16.67%", "60%", "6%", "33.33%"]),
    ("5/6", "83.33%", ["83.33%", "56%", "65%", "66.67%"]),
    ("3/20", "15%", ["15%", "20%", "30%", "3%"]),
    ("7/20", "35%", ["35%", "70%", "20%", "7%"]),
    ("9/20", "45%", ["45%", "90%", "20%", "9%"]),
    ("11/20", "55%", ["55%", "20%", "11%", "45%"]),
    ("13/20", "65%", ["65%", "13%", "20%", "35%"]),
    ("17/20", "85%", ["85%", "17%", "80%", "15%"]),
    ("19/20", "95%", ["95%", "19%", "90%", "5%"]),
]
random.shuffle(frac_pct_easy)

for frac, pct, ch in frac_pct_easy[:30]:
    random.shuffle(ch)
    add_q(
        "Easy",
        f"What percentage is equivalent to {frac}?",
        ch, pct,
        f"The fraction {frac} equals {pct}. This is a standard fraction-percent equivalent to memorize.",
        ["fraction-percent equivalents", "mental math", "recognition"]
    )

# --- E5: 5% of a number (20 questions) ---
easy_5pct_bases = [
    200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000,
    2200, 2400, 2600, 2800, 3000, 4000, 5000, 6000, 8000, 10000,
]
random.shuffle(easy_5pct_bases)

for base in easy_5pct_bases[:20]:
    correct = base * 0.05
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 5% of {base:,}?",
        choices, answer,
        f"Find 10% first: {base:,} ÷ 10 = {fmt_num(base*0.1)}. Then halve: {fmt_num(base*0.1)} ÷ 2 = {fmt_num(correct)}.",
        ["mental math", "5% shortcut", "benchmark percentage"]
    )

# --- E6: 1% of a number (20 questions) ---
easy_1pct_bases = [
    500, 800, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500,
    5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000, 50000,
]
random.shuffle(easy_1pct_bases)

for base in easy_1pct_bases[:20]:
    correct = base * 0.01
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 1% of {base:,}?",
        choices, answer,
        f"Move the decimal two places left: {base:,} → {fmt_num(correct)}.",
        ["mental math", "1% shortcut", "benchmark percentage"]
    )

# --- E7: 75% of a number (15 questions) ---
easy_75pct_bases = [
    80, 120, 160, 200, 240, 320, 400, 480, 600, 800,
    1000, 1200, 1600, 2000, 2400,
]
random.shuffle(easy_75pct_bases)

for base in easy_75pct_bases[:15]:
    correct = base * 0.75
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 75% of {base:,}?",
        choices, answer,
        f"75% = 3/4. {base:,} ÷ 4 = {fmt_num(base/4)}, × 3 = {fmt_num(correct)}.",
        ["mental math", "75% shortcut", "benchmark percentage"]
    )

# --- E8: Simple percentage of a number using 20% (15 questions) ---
easy_20pct_bases = [
    100, 150, 200, 250, 300, 350, 400, 450, 500, 600,
    750, 800, 1000, 1500, 2000,
]
random.shuffle(easy_20pct_bases)

for base in easy_20pct_bases[:15]:
    correct = base * 0.2
    choices, answer = make_numeric_choices(correct)
    add_q(
        "Easy",
        f"What is 20% of {base:,}?",
        choices, answer,
        f"20% = 1/5. {base:,} ÷ 5 = {fmt_num(correct)}. Or: 10% = {fmt_num(base*0.1)}, doubled = {fmt_num(correct)}.",
        ["mental math", "20% shortcut", "benchmark percentage"]
    )

# Fill remaining easy to reach 200
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
extra_easy_bases = list(range(100, 10001, 50))
random.shuffle(extra_easy_bases)
extra_pcts = [10, 25, 50, 20, 75, 5]
idx = 0
while easy_count < 200 and idx < len(extra_easy_bases):
    base = extra_easy_bases[idx]
    pct = random.choice(extra_pcts)
    correct = base * pct / 100
    if correct == int(correct):
        correct = int(correct)
        choices, answer = make_numeric_choices(correct)
        shortcut = {10: "move decimal 1 left", 25: "divide by 4", 50: "divide by 2",
                    20: "divide by 5", 75: "3/4 of the number", 5: "half of 10%"}
        add_q(
            "Easy",
            f"Using mental math, what is {pct}% of {base:,}?",
            choices, answer,
            f"{pct}% of {base:,}: {shortcut[pct]}. Answer = {fmt_num(correct)}.",
            ["mental math", "benchmark percentage", "percentage shortcuts"]
        )
        easy_count += 1
    idx += 1


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- M1: Decomposition (15% = 10% + 5%, etc.) (40 questions) ---
decomp_configs = [
    (15, "10% + 5%"),
    (30, "10% × 3"),
    (35, "25% + 10%"),
    (40, "50% − 10%"),
    (45, "50% − 5%"),
    (60, "50% + 10%"),
    (70, "50% + 20%"),
    (80, "50% + 25% + 5%"),
    (90, "100% − 10%"),
    (95, "100% − 5%"),
    (11, "10% + 1%"),
    (12, "10% + 2%"),
    (22, "20% + 2%"),
    (33, "25% + 8%"),
    (55, "50% + 5%"),
    (65, "50% + 15%"),
    (85, "75% + 10%"),
]

medium_decomp_bases = [
    200, 300, 400, 500, 600, 800, 1000, 1200, 1500, 1800,
    2000, 2400, 2500, 3000, 3200, 3500, 4000, 4500, 5000, 6000,
    6500, 7000, 7500, 8000, 9000, 10000, 12000, 15000, 16000, 18000,
    20000, 24000, 25000, 30000, 32000, 35000, 36000, 40000, 45000, 50000,
]
random.shuffle(medium_decomp_bases)

m1_count = 0
for base in medium_decomp_bases:
    if m1_count >= 40:
        break
    pct, decomp = random.choice(decomp_configs)
    correct = base * pct / 100
    if correct == int(correct):
        correct = int(correct)
        choices, answer = make_numeric_choices(correct)
        ten_pct = base * 0.1
        add_q(
            "Medium",
            f"What is {pct}% of {base:,}?",
            choices, answer,
            f"Decompose: {pct}% = {decomp}. 10% of {base:,} = {fmt_num(ten_pct)}. "
            f"Compute step by step to get {fmt_num(correct)}.",
            ["mental math", "decomposition", "percentage shortcuts"]
        )
        m1_count += 1

# --- M2: Fraction-percent applied (12.5%, 37.5%, 62.5%, 87.5%, 33.33%, 66.67%) (30 questions) ---
frac_pct_applied = [
    (12.5, "1/8", 8),
    (37.5, "3/8", 8),
    (62.5, "5/8", 8),
    (87.5, "7/8", 8),
    (33.33, "1/3", 3),
    (66.67, "2/3", 3),
    (16.67, "1/6", 6),
    (83.33, "5/6", 6),
]

m2_bases_8 = [64, 80, 96, 120, 160, 200, 240, 320, 400, 480, 560, 640, 720, 800, 960, 1600, 2400, 3200, 4000, 4800]
m2_bases_3 = [90, 120, 150, 180, 210, 240, 270, 300, 360, 450, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3600]
m2_bases_6 = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 720, 900, 1200, 1800, 2400, 3000, 3600, 4200, 4800, 5400]

random.shuffle(m2_bases_8)
random.shuffle(m2_bases_3)
random.shuffle(m2_bases_6)

m2_count = 0
for pct_val, frac_str, divisor in frac_pct_applied:
    if m2_count >= 30:
        break
    if divisor == 8:
        bases = m2_bases_8
    elif divisor == 3:
        bases = m2_bases_3
    else:
        bases = m2_bases_6

    for base in bases[:4]:
        if m2_count >= 30:
            break
        correct = base * pct_val / 100
        if correct == int(correct):
            correct = int(correct)
        choices, answer = make_numeric_choices(correct)
        add_q(
            "Medium",
            f"What is {pct_val}% of {base:,}?",
            choices, answer,
            f"{pct_val}% = {frac_str}. {base:,} ÷ {divisor} = {fmt_num(base/divisor)}"
            + (f", × {int(pct_val * divisor / 100)} = {fmt_num(correct)}." if pct_val not in (33.33, 16.67) else f" = {fmt_num(correct)}."),
            ["mental math", "fraction-percent equivalents", "applied computation"]
        )
        m2_count += 1

# --- M3: Practical mental math — discounts (25 questions) ---
discount_items = [
    ("shirt", 800), ("bag", 1200), ("shoes", 2500), ("watch", 3000),
    ("laptop", 35000), ("phone", 18000), ("tablet", 12000), ("jacket", 4500),
    ("dress", 2800), ("headphones", 3500), ("book", 600), ("backpack", 1500),
    ("sunglasses", 2000), ("perfume", 4000), ("sneakers", 5500),
    ("blouse", 1800), ("pants", 2200), ("skirt", 1600), ("belt", 900),
    ("wallet", 1400), ("umbrella", 750), ("cap", 500), ("scarf", 1100),
    ("gloves", 650), ("tie", 850),
]
discount_pcts = [10, 20, 25, 30, 40, 50, 15, 5]
random.shuffle(discount_items)

for i in range(25):
    item_name, price = discount_items[i % len(discount_items)]
    pct = random.choice(discount_pcts)
    discount_amt = price * pct / 100
    sale_price = price - discount_amt
    if discount_amt == int(discount_amt):
        discount_amt = int(discount_amt)
        sale_price = int(sale_price)
    choices, answer = make_numeric_choices(sale_price, "currency")
    add_q(
        "Medium",
        f"A {item_name} costs {fmt_currency(price)}. If it is {pct}% off, what is the sale price?",
        choices, answer,
        f"{pct}% of {fmt_currency(price)} = {fmt_currency(discount_amt)}. "
        f"Sale price = {fmt_currency(price)} − {fmt_currency(discount_amt)} = {fmt_currency(sale_price)}.",
        ["mental math", "discount", "practical application"]
    )

# --- M4: Percentage increase/decrease with multiplier (25 questions) ---
m4_scenarios = [
    ("salary", 20000, 10, "increase"),
    ("salary", 25000, 20, "increase"),
    ("salary", 30000, 15, "increase"),
    ("rent", 8000, 10, "increase"),
    ("rent", 12000, 25, "increase"),
    ("price", 1500, 20, "decrease"),
    ("price", 2400, 25, "decrease"),
    ("price", 5000, 10, "decrease"),
    ("price", 3600, 50, "decrease"),
    ("budget", 100000, 5, "decrease"),
    ("budget", 200000, 10, "decrease"),
    ("fare", 15, 20, "increase"),
    ("fare", 12, 25, "increase"),
    ("enrollment", 500, 10, "increase"),
    ("enrollment", 800, 25, "increase"),
    ("output", 1200, 50, "increase"),
    ("output", 2000, 20, "decrease"),
    ("expenses", 45000, 10, "decrease"),
    ("expenses", 60000, 20, "decrease"),
    ("population", 10000, 5, "increase"),
    ("population", 50000, 10, "increase"),
    ("stock price", 400, 25, "decrease"),
    ("stock price", 600, 50, "decrease"),
    ("revenue", 80000, 15, "increase"),
    ("revenue", 120000, 25, "increase"),
]
random.shuffle(m4_scenarios)

for context, base, pct, direction in m4_scenarios[:25]:
    if direction == "increase":
        new_val = base * (1 + pct / 100)
        multiplier = 1 + pct / 100
        verb = "increases"
    else:
        new_val = base * (1 - pct / 100)
        multiplier = 1 - pct / 100
        verb = "decreases"

    if new_val == int(new_val):
        new_val = int(new_val)

    use_currency = context in ("salary", "rent", "price", "budget", "fare", "expenses", "revenue", "stock price")
    style = "currency" if use_currency else "plain"
    choices, answer = make_numeric_choices(new_val, style)
    fmt_base = fmt_currency(base) if use_currency else fmt_num(base)
    fmt_new = fmt_currency(new_val) if use_currency else fmt_num(new_val)

    add_q(
        "Medium",
        f"A {context} of {fmt_base} {verb} by {pct}%. What is the new value?",
        choices, answer,
        f"Multiplier = {multiplier}. {fmt_base} × {multiplier} = {fmt_new}.",
        ["mental math", "percentage increase and decrease", "multiplier method"]
    )
