"""
Generate 600 multiple-choice questions for Percentage Increase and Decrease.
Distribution: 200 Easy, 200 Medium, 200 Hard
Output: data/seed/questions/numerical-ability/percentages/percentage-increase-and-decrease/questions.json
"""

import json
import random
import os
from pathlib import Path

random.seed(2024)

questions: list[dict] = []
current_id = 0


def next_id() -> int:
    global current_id
    current_id += 1
    return current_id


def make_q(difficulty: str, question: str, choices: list[str], answer: str,
           explanation: str, tags: list[str]) -> dict:
    return {
        "id": next_id(),
        "subtest": "Numerical Ability",
        "module": "Percentages",
        "subtopic": "Percentage Increase and Decrease",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


def fmt_pct(val: float) -> str:
    """Format a percentage value cleanly."""
    if val == int(val):
        return f"{int(val)}%"
    return f"{val:.2f}%".rstrip("0").rstrip(".")  + "%"


def fmt_pct_clean(val: float) -> str:
    """Format percentage for answer choices."""
    if val == int(val):
        return f"{int(val)}%"
    # Round to 2 decimal places
    rounded = round(val, 2)
    if rounded == int(rounded):
        return f"{int(rounded)}%"
    s = f"{rounded:.2f}".rstrip("0").rstrip(".")
    return f"{s}%"


def fmt_money(val: float) -> str:
    """Format as Philippine peso."""
    if val == int(val):
        return f"₱{int(val):,}"
    return f"₱{val:,.2f}"


def fmt_num(val: float) -> str:
    """Format a number cleanly."""
    if val == int(val):
        return f"{int(val):,}"
    return f"{val:,.2f}"


def generate_pct_distractors(correct_pct: float, count: int = 3) -> list[float]:
    """Generate percentage distractors near the correct answer."""
    distractors: set[float] = set()
    attempts = 0
    offsets = [5, -5, 10, -10, 3, -3, 8, -8, 15, -15, 2, -2, 1, -1, 20, -20]
    while len(distractors) < count and attempts < 200:
        offset = random.choice(offsets)
        d = round(correct_pct + offset, 2)
        if d != correct_pct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(round(correct_pct + len(distractors) * 7 + 3, 2))
    return list(distractors)[:count]


def generate_money_distractors(correct: float, count: int = 3) -> list[float]:
    """Generate money distractors."""
    distractors: set[float] = set()
    attempts = 0
    base_offsets = [500, -500, 1000, -1000, 2000, -2000, 1500, -1500, 3000, -3000, 5000, -5000]
    # Scale offsets based on magnitude
    scale = max(1, correct / 20)
    while len(distractors) < count and attempts < 200:
        offset = random.choice(base_offsets)
        # Scale offset to be reasonable relative to correct answer
        scaled_offset = offset * max(1, correct / 10000)
        d = round(correct + scaled_offset)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(round(correct + (len(distractors) + 1) * 1000))
    return list(distractors)[:count]


def generate_num_distractors(correct: float, count: int = 3) -> list[float]:
    """Generate numeric distractors."""
    distractors: set[float] = set()
    attempts = 0
    spread = max(5, abs(correct) * 0.15)
    while len(distractors) < count and attempts < 200:
        offset = random.uniform(-spread, spread)
        d = round(correct + offset)
        if d != correct and d > 0 and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(round(correct + (len(distractors) + 1) * 5))
    return list(distractors)[:count]


def shuffle_choices(correct_str: str, distractor_strs: list[str]) -> list[str]:
    """Shuffle correct answer among distractors, ensuring no duplicates."""
    import re as _re
    # Remove any distractors that match the correct answer or each other
    unique_distractors: list[str] = []
    seen = {correct_str}
    for d in distractor_strs:
        if d not in seen:
            unique_distractors.append(d)
            seen.add(d)
    # Pad if we lost distractors due to dedup
    fallback_idx = 0
    offsets = [3, 7, 11, 13, 17, 19, 23, 29, -3, -7, -11, -13]
    while len(unique_distractors) < 3 and fallback_idx < len(offsets):
        num_match = _re.search(r'[\d,.]+', correct_str)
        if num_match:
            try:
                val = float(num_match.group().replace(",", ""))
                new_val = val + offsets[fallback_idx]
                if new_val <= 0:
                    new_val = val + abs(offsets[fallback_idx])
                if "₱" in correct_str:
                    new_num_str = f"{int(new_val):,}" if new_val == int(new_val) else f"{new_val:,.2f}"
                elif "%" in correct_str:
                    new_num_str = f"{int(new_val)}" if new_val == int(new_val) else f"{new_val:.2f}".rstrip("0").rstrip(".")
                else:
                    new_num_str = f"{int(new_val):,}" if new_val == int(new_val) else f"{new_val:g}"
                # Rebuild the candidate preserving suffix (e.g., " increase")
                candidate = correct_str.replace(num_match.group(), new_num_str, 1)
                if candidate not in seen and candidate != correct_str:
                    unique_distractors.append(candidate)
                    seen.add(candidate)
            except ValueError:
                pass
        fallback_idx += 1
    choices = [correct_str] + unique_distractors[:3]
    random.shuffle(choices)
    return choices


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Category 1: Simple Percent Increase (50 questions) ---
easy_increase_scenarios = [
    ("salary", "A worker's salary increased from {orig} to {new}. What is the percent increase?",
     ["percent increase", "salary", "basic percentage change"]),
    ("population", "A barangay's population grew from {orig} to {new}. What is the percent increase?",
     ["percent increase", "population growth", "basic percentage change"]),
    ("price", "A product's price rose from {orig} to {new}. What is the percent increase?",
     ["percent increase", "price", "basic percentage change"]),
    ("students", "The number of students increased from {orig} to {new}. What is the percent increase?",
     ["percent increase", "enrollment", "basic percentage change"]),
    ("revenue", "A store's monthly revenue went from {orig} to {new}. What is the percent increase?",
     ["percent increase", "revenue", "basic percentage change"]),
]

easy_increase_rates = [5, 10, 15, 20, 25, 30, 40, 50, 8, 12]
easy_increase_bases = [100, 200, 300, 400, 500, 600, 800, 1000, 1200, 1500,
                       2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000,
                       18000, 20000, 22000, 25000, 28000, 30000, 32000, 35000, 40000, 45000,
                       50000, 55000, 60000, 70000, 75000, 80000, 90000, 100000, 120000, 150000,
                       160000, 180000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 750000]

for i in range(50):
    rate = easy_increase_rates[i % len(easy_increase_rates)]
    base = easy_increase_bases[i]
    new_val = int(base * (1 + rate / 100))
    scenario = easy_increase_scenarios[i % len(easy_increase_scenarios)]

    if "salary" in scenario[0] or "revenue" in scenario[0] or "price" in scenario[0]:
        orig_str = fmt_money(base)
        new_str = fmt_money(new_val)
    else:
        orig_str = fmt_num(base)
        new_str = fmt_num(new_val)

    question_text = scenario[1].format(orig=orig_str, new=new_str)
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    explanation = (f"Increase = {new_str} − {orig_str} = {fmt_num(new_val - base)}. "
                   f"Percent increase = {fmt_num(new_val - base)} ÷ {fmt_num(base)} × 100 = {rate}%.")
    questions.append(make_q("Easy", question_text, choices, correct, explanation, scenario[2]))


# --- Category 2: Simple Percent Decrease (50 questions) ---
easy_decrease_scenarios = [
    ("discount", "A shirt originally priced at {orig} is now on sale for {new}. What is the percent discount?",
     ["percent decrease", "discount", "basic percentage change"]),
    ("budget", "A department's budget was reduced from {orig} to {new}. What is the percent decrease?",
     ["percent decrease", "budget cut", "basic percentage change"]),
    ("inventory", "A warehouse's stock decreased from {orig} units to {new} units. What is the percent decrease?",
     ["percent decrease", "inventory", "basic percentage change"]),
    ("consumption", "Electricity consumption dropped from {orig} kWh to {new} kWh. What is the percent decrease?",
     ["percent decrease", "utility", "basic percentage change"]),
    ("employees", "The number of employees decreased from {orig} to {new}. What is the percent decrease?",
     ["percent decrease", "workforce", "basic percentage change"]),
]

easy_decrease_rates = [5, 10, 15, 20, 25, 30, 40, 50, 8, 12]
easy_decrease_bases = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200,
                       1400, 1500, 1600, 1800, 2000, 2200, 2400, 2500, 2800, 3000,
                       3200, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500,
                       8000, 8500, 9000, 9500, 10000, 12000, 14000, 15000, 16000, 18000,
                       20000, 22000, 24000, 25000, 28000, 30000, 35000, 40000, 45000, 50000]

for i in range(50):
    rate = easy_decrease_rates[i % len(easy_decrease_rates)]
    base = easy_decrease_bases[i]
    new_val = int(base * (1 - rate / 100))
    scenario = easy_decrease_scenarios[i % len(easy_decrease_scenarios)]

    if "discount" in scenario[0] or "budget" in scenario[0]:
        orig_str = fmt_money(base)
        new_str = fmt_money(new_val)
    else:
        orig_str = fmt_num(base)
        new_str = fmt_num(new_val)

    question_text = scenario[1].format(orig=orig_str, new=new_str)
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    decrease_amt = base - new_val
    explanation = (f"Decrease = {fmt_num(base)} − {fmt_num(new_val)} = {fmt_num(decrease_amt)}. "
                   f"Percent decrease = {fmt_num(decrease_amt)} ÷ {fmt_num(base)} × 100 = {rate}%.")
    questions.append(make_q("Easy", question_text, choices, correct, explanation, scenario[2]))


# --- Category 3: Find New Value After Increase (30 questions) ---
easy_new_val_increase_contexts = [
    "A product costs {orig}. After a {rate}% price increase, what is the new price?",
    "An employee earns {orig}. After a {rate}% raise, what is the new salary?",
    "A town has {orig} residents. After a {rate}% population increase, how many residents are there now?",
    "A store's inventory is {orig} items. After a {rate}% increase in stock, how many items are there?",
    "A bus fare is {orig}. After a {rate}% fare hike, what is the new fare?",
]

_easy_inc_nv_params = [
    (5, 200), (10, 400), (15, 600), (20, 800), (25, 1000),
    (30, 1200), (50, 1500), (5, 2000), (10, 2500), (15, 3000),
    (20, 4000), (25, 5000), (30, 6000), (50, 8000), (5, 10000),
    (10, 12000), (15, 15000), (20, 18000), (25, 20000), (30, 22000),
    (50, 25000), (5, 30000), (10, 35000), (15, 40000), (20, 45000),
    (25, 50000), (30, 60000), (50, 80000), (10, 100), (20, 500),
]

for i in range(30):
    rate, base = _easy_inc_nv_params[i]
    new_val = int(base * (1 + rate / 100))
    ctx = easy_new_val_increase_contexts[i % len(easy_new_val_increase_contexts)]

    if "costs" in ctx or "earns" in ctx or "fare" in ctx:
        orig_str = fmt_money(base)
        correct = fmt_money(new_val)
        distractors = [fmt_money(d) for d in generate_money_distractors(new_val)]
    else:
        orig_str = fmt_num(base)
        correct = fmt_num(new_val)
        distractors = [fmt_num(d) for d in generate_num_distractors(new_val)]

    question_text = ctx.format(orig=orig_str, rate=rate)
    choices = shuffle_choices(correct, distractors)
    explanation = f"New value = {fmt_num(base)} × {1 + rate/100:.2f} = {fmt_num(new_val)}."
    tags = ["percent increase", "find new value", "basic percentage change"]
    questions.append(make_q("Easy", question_text, choices, correct, explanation, tags))


# --- Category 4: Find New Value After Decrease (30 questions) ---
easy_new_val_decrease_contexts = [
    "A jacket costs {orig}. After a {rate}% discount, what is the sale price?",
    "A budget of {orig} is cut by {rate}%. What is the new budget?",
    "A school has {orig} students. After a {rate}% drop in enrollment, how many students remain?",
    "A factory produces {orig} units. After a {rate}% reduction, how many units are produced?",
    "Water consumption was {orig} liters. After a {rate}% decrease, what is the new consumption?",
]

_easy_dec_nv_params = [
    (5, 400), (10, 600), (15, 800), (20, 1000), (25, 1200),
    (30, 1500), (40, 2000), (50, 2500), (5, 3000), (10, 4000),
    (15, 5000), (20, 6000), (25, 8000), (30, 10000), (40, 12000),
    (50, 15000), (5, 18000), (10, 20000), (15, 25000), (20, 30000),
    (25, 35000), (30, 40000), (40, 45000), (50, 50000), (5, 60000),
    (10, 70000), (15, 80000), (20, 90000), (25, 100000), (30, 120000),
]

for i in range(30):
    rate, base = _easy_dec_nv_params[i]
    new_val = int(base * (1 - rate / 100))
    ctx = easy_new_val_decrease_contexts[i % len(easy_new_val_decrease_contexts)]

    if "costs" in ctx or "budget" in ctx:
        orig_str = fmt_money(base)
        correct = fmt_money(new_val)
        distractors = [fmt_money(d) for d in generate_money_distractors(new_val)]
    else:
        orig_str = fmt_num(base)
        correct = fmt_num(new_val)
        distractors = [fmt_num(d) for d in generate_num_distractors(new_val)]

    question_text = ctx.format(orig=orig_str, rate=rate)
    choices = shuffle_choices(correct, distractors)
    explanation = f"New value = {fmt_num(base)} × {1 - rate/100:.2f} = {fmt_num(new_val)}."
    tags = ["percent decrease", "find new value", "basic percentage change"]
    questions.append(make_q("Easy", question_text, choices, correct, explanation, tags))


# --- Category 5: Identify Direction of Change (20 questions) ---
direction_questions = [
    ("A worker's overtime hours went from 20 to 25 per month. This represents a percent ___.", "increase", 25.0),
    ("A store's daily customers dropped from 200 to 160. This represents a percent ___.", "decrease", 20.0),
    ("Monthly rent rose from ₱8,000 to ₱9,600. This represents a percent ___.", "increase", 20.0),
    ("The error rate fell from 10% to 8%. This represents a percent ___.", "decrease", 20.0),
    ("Production output grew from 500 to 600 units. This represents a percent ___.", "increase", 20.0),
    ("A company's debt shrank from ₱1,000,000 to ₱800,000. This represents a percent ___.", "decrease", 20.0),
    ("Enrollment climbed from 1,200 to 1,500 students. This represents a percent ___.", "increase", 25.0),
    ("Fuel consumption decreased from 40 liters to 32 liters per week. This represents a percent ___.", "decrease", 20.0),
    ("The passing rate improved from 60% to 75%. This represents a percent ___.", "increase", 25.0),
    ("A city's crime rate dropped from 80 to 60 incidents per month. This represents a percent ___.", "decrease", 25.0),
    ("Revenue surged from ₱500,000 to ₱650,000. This represents a percent ___.", "increase", 30.0),
    ("Paper usage was reduced from 3,000 to 2,400 sheets. This represents a percent ___.", "decrease", 20.0),
    ("The number of complaints rose from 45 to 54. This represents a percent ___.", "increase", 20.0),
    ("Processing time fell from 30 minutes to 24 minutes. This represents a percent ___.", "decrease", 20.0),
    ("A farmer's harvest grew from 800 kg to 1,000 kg. This represents a percent ___.", "increase", 25.0),
    ("Absenteeism dropped from 50 days to 35 days per year. This represents a percent ___.", "decrease", 30.0),
    ("Monthly savings increased from ₱5,000 to ₱6,500. This represents a percent ___.", "increase", 30.0),
    ("The defect rate improved from 6% to 4.5%. This represents a percent ___.", "decrease", 25.0),
    ("Electricity bills rose from ₱3,000 to ₱3,600. This represents a percent ___.", "increase", 20.0),
    ("Travel time decreased from 2 hours to 1.5 hours. This represents a percent ___.", "decrease", 25.0),
]

for q_text, direction, pct in direction_questions:
    correct = f"{direction} of {fmt_pct_clean(pct)}"
    if direction == "increase":
        wrong_dir = "decrease"
    else:
        wrong_dir = "increase"
    distractors = [
        f"{wrong_dir} of {fmt_pct_clean(pct)}",
        f"{direction} of {fmt_pct_clean(pct + 5)}",
        f"{direction} of {fmt_pct_clean(pct - 5 if pct > 5 else pct + 10)}",
    ]
    choices = shuffle_choices(correct, distractors)
    explanation = f"The value changed, and the percent change is {fmt_pct_clean(pct)}. Since the new value is {'higher' if direction == 'increase' else 'lower'} than the original, it is a {direction}."
    tags = ["identify direction", "percent change", "basic percentage change"]
    questions.append(make_q("Easy", q_text, choices, correct, explanation, tags))


# --- Category 6: Simple conceptual questions (20 questions) ---
conceptual_easy = [
    ("If a value doubles, what is the percent increase?", "100%", ["50%", "200%", "150%"],
     "Doubling means the new value is 2× the original. Increase = (2-1)/1 × 100 = 100%."),
    ("If a value triples, what is the percent increase?", "200%", ["100%", "300%", "150%"],
     "Tripling means the new value is 3× the original. Increase = (3-1)/1 × 100 = 200%."),
    ("If a value is halved, what is the percent decrease?", "50%", ["25%", "100%", "75%"],
     "Halving means the new value is 0.5× the original. Decrease = (1-0.5)/1 × 100 = 50%."),
    ("If a value increases by 100%, the new value is ___ times the original.", "2", ["1", "3", "1.5"],
     "100% increase means new = original + 100% of original = 2 × original."),
    ("A 50% decrease means the new value is what fraction of the original?", "1/2", ["1/4", "3/4", "2/3"],
     "50% decrease: new = original × (1 - 0.50) = original × 0.50 = 1/2 of original."),
    ("What is the percent increase from 50 to 75?", "50%", ["25%", "33%", "75%"],
     "Increase = 75 - 50 = 25. Percent = 25 ÷ 50 × 100 = 50%."),
    ("What is the percent decrease from 80 to 60?", "25%", ["20%", "33%", "15%"],
     "Decrease = 80 - 60 = 20. Percent = 20 ÷ 80 × 100 = 25%."),
    ("What is the percent increase from 200 to 250?", "25%", ["20%", "50%", "30%"],
     "Increase = 250 - 200 = 50. Percent = 50 ÷ 200 × 100 = 25%."),
    ("What is the percent decrease from 500 to 400?", "20%", ["25%", "10%", "15%"],
     "Decrease = 500 - 400 = 100. Percent = 100 ÷ 500 × 100 = 20%."),
    ("What is the percent increase from 40 to 50?", "25%", ["10%", "20%", "50%"],
     "Increase = 50 - 40 = 10. Percent = 10 ÷ 40 × 100 = 25%."),
    ("What is the percent decrease from 120 to 90?", "25%", ["30%", "20%", "33%"],
     "Decrease = 120 - 90 = 30. Percent = 30 ÷ 120 × 100 = 25%."),
    ("What is the percent increase from 300 to 360?", "20%", ["15%", "25%", "60%"],
     "Increase = 360 - 300 = 60. Percent = 60 ÷ 300 × 100 = 20%."),
    ("What is the percent decrease from 1,000 to 850?", "15%", ["10%", "20%", "25%"],
     "Decrease = 1,000 - 850 = 150. Percent = 150 ÷ 1,000 × 100 = 15%."),
    ("What is the percent increase from 60 to 78?", "30%", ["18%", "25%", "20%"],
     "Increase = 78 - 60 = 18. Percent = 18 ÷ 60 × 100 = 30%."),
    ("What is the percent decrease from 250 to 200?", "20%", ["25%", "50%", "10%"],
     "Decrease = 250 - 200 = 50. Percent = 50 ÷ 250 × 100 = 20%."),
    ("What is the percent increase from 150 to 180?", "20%", ["30%", "15%", "25%"],
     "Increase = 180 - 150 = 30. Percent = 30 ÷ 150 × 100 = 20%."),
    ("What is the percent decrease from 400 to 300?", "25%", ["20%", "33%", "75%"],
     "Decrease = 400 - 300 = 100. Percent = 100 ÷ 400 × 100 = 25%."),
    ("What is the percent increase from 80 to 100?", "25%", ["20%", "80%", "50%"],
     "Increase = 100 - 80 = 20. Percent = 20 ÷ 80 × 100 = 25%."),
    ("What is the percent decrease from 60 to 45?", "25%", ["15%", "33%", "20%"],
     "Decrease = 60 - 45 = 15. Percent = 15 ÷ 60 × 100 = 25%."),
    ("What is the percent increase from 1,000 to 1,200?", "20%", ["12%", "25%", "200%"],
     "Increase = 1,200 - 1,000 = 200. Percent = 200 ÷ 1,000 × 100 = 20%."),
]

for q_text, correct, dists, expl in conceptual_easy:
    choices = shuffle_choices(correct, dists)
    tags = ["conceptual", "percent change", "basic percentage change"]
    questions.append(make_q("Easy", q_text, choices, correct, expl, tags))


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Category 1: Percent Increase with Realistic Contexts (40 questions) ---
medium_increase_contexts = [
    ("A government employee's salary went from {orig} to {new}. What is the percent increase?",
     ["percent increase", "salary", "government", "medium difficulty"]),
    ("A city's annual budget grew from {orig} to {new}. What is the percent increase?",
     ["percent increase", "budget", "government", "medium difficulty"]),
    ("Monthly sales revenue increased from {orig} to {new}. What is the percent increase?",
     ["percent increase", "sales", "business", "medium difficulty"]),
    ("The number of daily commuters rose from {orig} to {new}. What is the percent increase?",
     ["percent increase", "transportation", "medium difficulty"]),
    ("A school's enrollment grew from {orig} to {new} students. What is the percent increase?",
     ["percent increase", "enrollment", "education", "medium difficulty"]),
]

medium_increase_rates = [6, 8, 12, 14, 16, 18, 22, 24, 28, 32, 35, 45, 55, 60, 75]
medium_increase_bases = [15000, 18000, 22000, 25000, 28000, 30000, 35000, 42000, 48000, 55000,
                         120000, 250000, 500000, 750000, 1200000,
                         16000, 19000, 21000, 23000, 26000, 33000, 36000, 38000, 44000, 52000,
                         65000, 85000, 95000, 110000, 140000, 175000, 220000, 280000, 320000, 400000,
                         450000, 550000, 650000, 800000, 1000000]

for i in range(40):
    rate = medium_increase_rates[i % len(medium_increase_rates)]
    base = medium_increase_bases[i]
    new_val = int(base * (1 + rate / 100))
    scenario = medium_increase_contexts[i % len(medium_increase_contexts)]

    if "salary" in scenario[0] or "budget" in scenario[0] or "revenue" in scenario[0]:
        orig_str = fmt_money(base)
        new_str = fmt_money(new_val)
    else:
        orig_str = fmt_num(base)
        new_str = fmt_num(new_val)

    question_text = scenario[0].format(orig=orig_str, new=new_str)
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    change = new_val - base
    explanation = (f"Increase = {fmt_num(new_val)} − {fmt_num(base)} = {fmt_num(change)}. "
                   f"Percent increase = {fmt_num(change)} ÷ {fmt_num(base)} × 100 = {rate}%.")
    questions.append(make_q("Medium", question_text, choices, correct, explanation, scenario[1]))


# --- Category 2: Percent Decrease with Realistic Contexts (40 questions) ---
medium_decrease_contexts = [
    ("A company's quarterly profit dropped from {orig} to {new}. What is the percent decrease?",
     ["percent decrease", "profit", "business", "medium difficulty"]),
    ("Government spending on a program was cut from {orig} to {new}. What is the percent decrease?",
     ["percent decrease", "budget cut", "government", "medium difficulty"]),
    ("The crime rate fell from {orig} to {new} incidents per month. What is the percent decrease?",
     ["percent decrease", "crime rate", "statistics", "medium difficulty"]),
    ("A factory's defect count dropped from {orig} to {new}. What is the percent decrease?",
     ["percent decrease", "quality control", "manufacturing", "medium difficulty"]),
    ("Electricity consumption decreased from {orig} kWh to {new} kWh. What is the percent decrease?",
     ["percent decrease", "utility", "consumption", "medium difficulty"]),
]

medium_decrease_rates = [6, 8, 12, 14, 16, 18, 22, 24, 28, 32, 35, 45, 55, 60, 75]
medium_decrease_bases = [12000, 16000, 20000, 24000, 30000, 36000, 40000, 48000, 50000, 60000,
                         80000, 100000, 150000, 200000, 500000,
                         14000, 17000, 19000, 22000, 26000, 32000, 38000, 42000, 45000, 55000,
                         65000, 75000, 90000, 125000, 180000, 240000, 300000, 350000, 420000, 480000,
                         520000, 600000, 700000, 850000, 950000]

for i in range(40):
    rate = medium_decrease_rates[i % len(medium_decrease_rates)]
    base = medium_decrease_bases[i]
    new_val = int(base * (1 - rate / 100))
    scenario = medium_decrease_contexts[i % len(medium_decrease_contexts)]

    if "profit" in scenario[0] or "spending" in scenario[0]:
        orig_str = fmt_money(base)
        new_str = fmt_money(new_val)
    else:
        orig_str = fmt_num(base)
        new_str = fmt_num(new_val)

    question_text = scenario[0].format(orig=orig_str, new=new_str)
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    change = base - new_val
    explanation = (f"Decrease = {fmt_num(base)} − {fmt_num(new_val)} = {fmt_num(change)}. "
                   f"Percent decrease = {fmt_num(change)} ÷ {fmt_num(base)} × 100 = {rate}%.")
    questions.append(make_q("Medium", question_text, choices, correct, explanation, scenario[1]))


# --- Category 3: Find Original Value (Reverse Problems) (40 questions) ---
medium_reverse_increase_contexts = [
    "After a {rate}% salary increase, an employee now earns {new}. What was the original salary?",
    "After a {rate}% price increase, a product now costs {new}. What was the original price?",
    "After a {rate}% growth, a city's population is now {new}. What was the original population?",
    "After a {rate}% increase in production, a factory now produces {new} units. What was the original output?",
]

medium_reverse_decrease_contexts = [
    "After a {rate}% discount, an item costs {new}. What was the original price?",
    "After a {rate}% budget cut, a department's budget is {new}. What was the original budget?",
    "After a {rate}% decrease, enrollment is now {new} students. What was the original enrollment?",
    "After a {rate}% reduction, a company has {new} employees. How many did it have originally?",
]

# 20 reverse-increase problems
_med_rev_inc_params = [
    (5, 10000), (8, 15000), (10, 20000), (12, 24000), (15, 25000),
    (20, 30000), (25, 32000), (30, 40000), (40, 50000), (50, 60000),
    (5, 18000), (8, 22000), (10, 28000), (12, 35000), (15, 42000),
    (20, 45000), (25, 48000), (30, 55000), (40, 65000), (50, 75000),
]
for i in range(20):
    rate, original = _med_rev_inc_params[i]
    new_val = int(original * (1 + rate / 100))
    ctx = medium_reverse_increase_contexts[i % len(medium_reverse_increase_contexts)]

    if "salary" in ctx or "price" in ctx or "costs" in ctx:
        new_str = fmt_money(new_val)
        correct = fmt_money(original)
        distractors = [fmt_money(d) for d in generate_money_distractors(original)]
    else:
        new_str = fmt_num(new_val)
        correct = fmt_num(original)
        distractors = [fmt_num(d) for d in generate_num_distractors(original)]

    question_text = ctx.format(rate=rate, new=new_str)
    choices = shuffle_choices(correct, distractors)
    multiplier = 1 + rate / 100
    explanation = f"Original = {fmt_num(new_val)} ÷ {multiplier:.2f} = {fmt_num(original)}."
    tags = ["reverse problem", "find original", "percent increase", "medium difficulty"]
    questions.append(make_q("Medium", question_text, choices, correct, explanation, tags))

# 20 reverse-decrease problems
_med_rev_dec_params = [
    (5, 10000), (8, 15000), (10, 20000), (12, 24000), (15, 25000),
    (20, 30000), (25, 40000), (30, 50000), (40, 60000), (50, 80000),
    (5, 12000), (8, 18000), (10, 22000), (12, 28000), (15, 35000),
    (20, 44000), (25, 52000), (30, 64000), (40, 72000), (50, 90000),
]
for i in range(20):
    rate, original = _med_rev_dec_params[i]
    new_val = int(original * (1 - rate / 100))
    ctx = medium_reverse_decrease_contexts[i % len(medium_reverse_decrease_contexts)]

    if "price" in ctx or "costs" in ctx or "budget" in ctx:
        new_str = fmt_money(new_val)
        correct = fmt_money(original)
        distractors = [fmt_money(d) for d in generate_money_distractors(original)]
    else:
        new_str = fmt_num(new_val)
        correct = fmt_num(original)
        distractors = [fmt_num(d) for d in generate_num_distractors(original)]

    question_text = ctx.format(rate=rate, new=new_str)
    choices = shuffle_choices(correct, distractors)
    multiplier = 1 - rate / 100
    explanation = f"Original = {fmt_num(new_val)} ÷ {multiplier:.2f} = {fmt_num(original)}."
    tags = ["reverse problem", "find original", "percent decrease", "medium difficulty"]
    questions.append(make_q("Medium", question_text, choices, correct, explanation, tags))


# --- Category 4: Simple Successive Changes (40 questions) ---
successive_easy_scenarios = [
    ("A product's price increases by {r1}% and then increases by {r2}%. What is the overall percent increase?",
     ["successive changes", "double increase", "multiplier method", "medium difficulty"]),
    ("A salary increases by {r1}% and then decreases by {r2}%. What is the net percent change?",
     ["successive changes", "increase then decrease", "multiplier method", "medium difficulty"]),
    ("A stock price decreases by {r1}% and then increases by {r2}%. What is the net percent change?",
     ["successive changes", "decrease then increase", "multiplier method", "medium difficulty"]),
    ("A population decreases by {r1}% and then decreases by {r2}%. What is the overall percent decrease?",
     ["successive changes", "double decrease", "multiplier method", "medium difficulty"]),
]

successive_rate_pairs = [
    (10, 10), (10, 20), (20, 10), (20, 20), (10, 30),
    (25, 20), (15, 10), (30, 10), (20, 25), (50, 20),
    (5, 15), (12, 8), (15, 25), (30, 20), (40, 15),
    (8, 12), (18, 10), (25, 30), (35, 15), (10, 40),
    (20, 15), (15, 20), (25, 10), (30, 25), (40, 30),
    (5, 10), (10, 5), (12, 15), (18, 20), (22, 12),
    (28, 10), (32, 15), (35, 20), (45, 25), (50, 30),
    (8, 20), (14, 10), (16, 25), (24, 15), (36, 20),
]

for i in range(40):
    scenario_idx = i % len(successive_easy_scenarios)
    scenario = successive_easy_scenarios[scenario_idx]
    r1, r2 = successive_rate_pairs[i]

    if scenario_idx == 0:  # increase, increase
        mult = (1 + r1/100) * (1 + r2/100)
        net_pct = round((mult - 1) * 100, 2)
        direction = "increase"
    elif scenario_idx == 1:  # increase, decrease
        mult = (1 + r1/100) * (1 - r2/100)
        net_pct = round(abs(mult - 1) * 100, 2)
        direction = "increase" if mult > 1 else "decrease"
    elif scenario_idx == 2:  # decrease, increase
        mult = (1 - r1/100) * (1 + r2/100)
        net_pct = round(abs(mult - 1) * 100, 2)
        direction = "increase" if mult > 1 else "decrease"
    else:  # decrease, decrease
        mult = (1 - r1/100) * (1 - r2/100)
        net_pct = round((1 - mult) * 100, 2)
        direction = "decrease"

    question_text = scenario[0].format(r1=r1, r2=r2)

    if net_pct == 0:
        correct = "0% (no change)"
        distractors = [f"{r1 + r2}%", f"{abs(r1 - r2)}%", f"{r1}%"]
    else:
        correct = f"{fmt_pct_clean(net_pct)} {direction}"
        wrong_simple = r1 + r2 if scenario_idx in [0, 3] else abs(r1 - r2)
        distractors_pcts = generate_pct_distractors(net_pct)
        distractors = [f"{fmt_pct_clean(d)} {direction}" for d in distractors_pcts[:2]]
        distractors.append(f"{wrong_simple}% {direction}")

    choices = shuffle_choices(correct, distractors[:3])
    m1 = 1 + r1/100 if scenario_idx in [0, 1] else 1 - r1/100
    m2 = 1 + r2/100 if scenario_idx in [0, 2] else 1 - r2/100
    explanation = (f"Multiplier = {m1:.2f} × {m2:.2f} = {mult:.4f}. "
                   f"Net change = {fmt_pct_clean(net_pct)} {direction}.")
    questions.append(make_q("Medium", question_text, choices, correct, explanation, scenario[1]))


# --- Category 5: Practical Application Problems (40 questions) ---
medium_practical = [
    # Salary problems
    ("An employee earning ₱{base:,} received a {rate}% raise. How much is the raise amount?",
     lambda base, rate: int(base * rate / 100),
     ["salary raise", "find amount", "practical application", "medium difficulty"]),
    # Discount problems
    ("A gadget priced at ₱{base:,} has a {rate}% discount. How much do you save?",
     lambda base, rate: int(base * rate / 100),
     ["discount", "find savings", "practical application", "medium difficulty"]),
    # Tax problems
    ("A purchase of ₱{base:,} has a {rate}% tax added. What is the total amount to pay?",
     lambda base, rate: int(base * (1 + rate / 100)),
     ["tax", "find total", "practical application", "medium difficulty"]),
    # Commission problems
    ("An agent earns {rate}% commission on ₱{base:,} in sales. What is the commission?",
     lambda base, rate: int(base * rate / 100),
     ["commission", "find amount", "practical application", "medium difficulty"]),
    # Comparison problems
    ("Last year, {base:,} people voted. This year, {rate}% more people voted. How many voted this year?",
     lambda base, rate: int(base * (1 + rate / 100)),
     ["percent increase", "find new value", "practical application", "medium difficulty"]),
]

medium_practical_params = [
    (25000, 10), (30000, 15), (18000, 20), (45000, 8), (22000, 12),
    (5000, 25), (8000, 30), (12000, 15), (3500, 20), (15000, 10),
    (2000, 12), (4500, 10), (7800, 15), (9000, 5), (6000, 8),
    (100000, 6), (250000, 5), (500000, 3), (80000, 10), (150000, 4),
    (50000, 20), (35000, 25), (28000, 30), (42000, 15), (60000, 12),
    (20000, 5), (32000, 8), (48000, 10), (55000, 6), (75000, 4),
    (10000, 15), (16000, 20), (24000, 25), (36000, 10), (40000, 8),
    (120000, 5), (200000, 10), (300000, 15), (450000, 8), (600000, 12),
]

for i in range(40):
    scenario = medium_practical[i % len(medium_practical)]
    base, rate = medium_practical_params[i]
    correct_val = scenario[1](base, rate)

    question_text = scenario[0].format(base=base, rate=rate)
    correct = fmt_money(correct_val)
    distractors = [fmt_money(d) for d in generate_money_distractors(correct_val)]
    choices = shuffle_choices(correct, distractors)

    if "raise" in scenario[0] or "save" in scenario[0] or "commission" in scenario[0]:
        explanation = f"Amount = {rate}% of ₱{base:,} = {rate/100:.2f} × {base:,} = ₱{correct_val:,}."
    elif "total" in scenario[0]:
        explanation = f"Total = ₱{base:,} × (1 + {rate/100:.2f}) = ₱{base:,} × {1+rate/100:.2f} = ₱{correct_val:,}."
    else:
        explanation = f"New value = {base:,} × {1+rate/100:.2f} = {correct_val:,}."

    questions.append(make_q("Medium", question_text, choices, correct, explanation, scenario[2]))


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Category 1: Complex Successive Changes (50 questions) ---
hard_successive_scenarios = [
    "A product's price increases by {r1}%, then decreases by {r2}%, then increases by {r3}%. What is the net percent change?",
    "An investment grows by {r1}%, then loses {r2}%, then gains {r3}%. What is the overall percent change?",
    "A salary is raised by {r1}%, then cut by {r2}%, then raised again by {r3}%. What is the net percent change from the original?",
    "A city's population grows by {r1}%, then shrinks by {r2}%, then grows by {r3}%. What is the net percent change?",
    "Revenue increases by {r1}%, then decreases by {r2}%, then increases by {r3}%. What is the overall percent change?",
]

hard_triple_rates = [
    (10, 10, 10), (20, 10, 5), (15, 20, 10), (25, 15, 10), (30, 20, 10),
    (10, 5, 20), (20, 25, 15), (40, 20, 10), (15, 10, 25), (50, 30, 20),
    (12, 8, 15), (18, 12, 10), (22, 18, 5), (35, 25, 15), (8, 5, 12),
    (10, 20, 30), (25, 10, 20), (30, 15, 25), (5, 10, 15), (20, 30, 10),
    (15, 5, 10), (10, 15, 20), (25, 20, 5), (40, 10, 15), (50, 25, 10),
    (6, 4, 8), (14, 10, 12), (16, 8, 20), (28, 15, 5), (32, 20, 12),
    (18, 10, 8), (24, 12, 15), (36, 18, 10), (42, 20, 8), (45, 30, 15),
    (8, 10, 25), (12, 15, 20), (20, 8, 12), (30, 12, 8), (35, 10, 20),
    (5, 8, 10), (10, 12, 8), (15, 8, 12), (22, 10, 15), (28, 20, 8),
    (33, 15, 12), (38, 20, 5), (44, 25, 10), (48, 30, 12), (55, 35, 15),
]

for i in range(50):
    scenario = hard_successive_scenarios[i % len(hard_successive_scenarios)]
    r1, r2, r3 = hard_triple_rates[i]

    # Pattern: increase, decrease, increase
    m1 = 1 + r1/100
    m2 = 1 - r2/100
    m3 = 1 + r3/100
    mult = m1 * m2 * m3
    net_pct = round(abs(mult - 1) * 100, 2)
    direction = "increase" if mult > 1 else "decrease"

    if net_pct == 0:
        correct = "0% (no net change)"
        distractors = [f"{r1}% increase", f"{r2}% decrease", f"{r3}% increase"]
    else:
        correct = f"{fmt_pct_clean(net_pct)} {direction}"
        # Common wrong answer: just adding/subtracting the rates
        wrong_simple = r1 - r2 + r3
        distractors_pcts = generate_pct_distractors(net_pct)
        distractors = [f"{fmt_pct_clean(d)} {direction}" for d in distractors_pcts[:2]]
        wrong_dir = "increase" if wrong_simple > 0 else "decrease"
        distractors.append(f"{abs(wrong_simple)}% {wrong_dir}")

    question_text = scenario.format(r1=r1, r2=r2, r3=r3)
    choices = shuffle_choices(correct, distractors[:3])
    explanation = (f"Multipliers: {m1:.2f} × {m2:.2f} × {m3:.2f} = {mult:.4f}. "
                   f"Net change = |{mult:.4f} − 1| × 100 = {fmt_pct_clean(net_pct)} {direction}.")
    tags = ["successive changes", "three changes", "multiplier method", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))


# --- Category 2: Reverse Successive Change Problems (40 questions) ---
hard_reverse_successive = [
    "After a {r1}% increase followed by a {r2}% decrease, a product costs ₱{final:,}. What was the original price?",
    "After a {r1}% decrease followed by a {r2}% increase, a salary is now ₱{final:,}. What was the original salary?",
    "After a {r1}% increase followed by another {r2}% increase, revenue is ₱{final:,}. What was the original revenue?",
    "After a {r1}% decrease followed by another {r2}% decrease, a budget is ₱{final:,}. What was the original budget?",
]

hard_reverse_params = [
    (20, 10, 50000), (10, 20, 40000), (25, 20, 30000), (15, 10, 60000),
    (30, 25, 45000), (20, 15, 80000), (10, 5, 100000), (40, 20, 36000),
    (25, 10, 54000), (50, 30, 42000), (12, 8, 75000), (20, 20, 48000),
    (15, 25, 32000), (30, 10, 70000), (10, 30, 56000), (25, 15, 90000),
    (20, 5, 114000), (35, 20, 27000), (8, 12, 66000), (40, 25, 21000),
    (15, 5, 44000), (22, 10, 55000), (18, 12, 62000), (28, 15, 38000),
    (35, 10, 72000), (12, 20, 85000), (45, 15, 28000), (10, 25, 96000),
    (30, 20, 52000), (20, 30, 64000), (25, 5, 78000), (15, 15, 46000),
    (40, 10, 33000), (50, 20, 24000), (8, 8, 88000), (22, 18, 58000),
    (18, 25, 42000), (32, 12, 68000), (28, 20, 35000), (45, 30, 26000),
]

for i in range(40):
    scenario_idx = i % len(hard_reverse_successive)
    scenario = hard_reverse_successive[scenario_idx]
    r1, r2, original = hard_reverse_params[i]

    if scenario_idx == 0:  # increase then decrease
        mult = (1 + r1/100) * (1 - r2/100)
    elif scenario_idx == 1:  # decrease then increase
        mult = (1 - r1/100) * (1 + r2/100)
    elif scenario_idx == 2:  # increase then increase
        mult = (1 + r1/100) * (1 + r2/100)
    else:  # decrease then decrease
        mult = (1 - r1/100) * (1 - r2/100)

    final_val = round(original * mult)
    # Recompute original from final to ensure clean division
    computed_original = round(final_val / mult)

    question_text = scenario.format(r1=r1, r2=r2, final=final_val)
    correct = fmt_money(computed_original)
    distractors = [fmt_money(d) for d in generate_money_distractors(computed_original)]
    choices = shuffle_choices(correct, distractors)
    explanation = (f"Combined multiplier = {mult:.4f}. "
                   f"Original = ₱{final_val:,} ÷ {mult:.4f} = {correct}.")
    tags = ["reverse problem", "successive changes", "find original", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))


# --- Category 3: "What percent increase needed to recover?" (30 questions) ---
recovery_rates = [10, 15, 20, 25, 30, 33, 40, 50, 60, 75, 5, 8, 12, 16, 35,
                  45, 55, 65, 70, 80, 22, 28, 32, 36, 42, 48, 52, 58, 62, 68]

for i in range(30):
    drop_rate = recovery_rates[i]
    # After dropping by drop_rate%, need to find recovery percent
    remaining_mult = 1 - drop_rate / 100
    recovery_pct = round((1 / remaining_mult - 1) * 100, 2)

    question_text = (f"A stock price dropped by {drop_rate}%. By what percent must it increase "
                     f"to return to its original value?")
    correct = fmt_pct_clean(recovery_pct)
    # Common wrong answer: same as the drop
    distractors = [f"{drop_rate}%"]
    other_dists = generate_pct_distractors(recovery_pct)
    for d in other_dists:
        if fmt_pct_clean(d) != f"{drop_rate}%" and fmt_pct_clean(d) != correct:
            distractors.append(fmt_pct_clean(d))
        if len(distractors) >= 3:
            break
    while len(distractors) < 3:
        distractors.append(fmt_pct_clean(recovery_pct + random.choice([7, 12, -7])))

    choices = shuffle_choices(correct, distractors[:3])
    explanation = (f"After a {drop_rate}% drop, the value is {remaining_mult:.4f} of the original. "
                   f"To return to 1.00: 1 ÷ {remaining_mult:.4f} = {1/remaining_mult:.4f}. "
                   f"Required increase = {fmt_pct_clean(recovery_pct)}.")
    tags = ["recovery problem", "reverse percentage", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))


# --- Category 4: Equal Increase and Decrease Pattern (20 questions) ---
equal_change_rates = [5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50, 6, 14, 16, 18, 22, 28, 32, 36]

for i in range(20):
    x = equal_change_rates[i]
    net_loss = round(x * x / 100, 2)

    question_text = (f"A value increases by {x}% and then decreases by {x}%. "
                     f"What is the net percent change?")
    correct = f"{fmt_pct_clean(net_loss)} decrease"
    distractors = [
        "0% (no change)",
        f"{fmt_pct_clean(net_loss)} increase",
        f"{x}% decrease",
    ]
    choices = shuffle_choices(correct, distractors)
    explanation = (f"When a value increases and decreases by the same percentage, "
                   f"net change = −(x²/100)% = −({x}²/100)% = −{fmt_pct_clean(net_loss)}. "
                   f"This is always a net decrease.")
    tags = ["equal change pattern", "successive changes", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))


# --- Category 5: Multi-Step Word Problems (30 questions) ---
hard_word_problems = [
    {
        "q": "A government office had 600 employees. Due to budget cuts, 20% were laid off. "
             "Later, 25% of the remaining employees were promoted. How many were promoted?",
        "answer": "120",
        "explanation": "After layoffs: 600 × 0.80 = 480 remain. Promoted: 480 × 0.25 = 120.",
        "distractors": ["150", "100", "130"],
        "tags": ["multi-step", "layoffs", "promotion", "hard"],
    },
    {
        "q": "A store marks up a product by 40% and then offers a 25% discount. "
             "If the original cost is ₱2,000, what is the final selling price?",
        "answer": "₱2,100",
        "explanation": "After 40% markup: ₱2,000 × 1.40 = ₱2,800. After 25% discount: ₱2,800 × 0.75 = ₱2,100.",
        "distractors": ["₱2,300", "₱2,000", "₱1,900"],
        "tags": ["multi-step", "markup", "discount", "hard"],
    },
    {
        "q": "A city's population was 200,000. It grew by 10% in the first year and 15% in the second year. "
             "What is the population after two years?",
        "answer": "253,000",
        "explanation": "Year 1: 200,000 × 1.10 = 220,000. Year 2: 220,000 × 1.15 = 253,000.",
        "distractors": ["250,000", "245,000", "260,000"],
        "tags": ["multi-step", "population growth", "successive increases", "hard"],
    },
    {
        "q": "An item's price was ₱5,000. It increased by 20% in January, then decreased by 15% in March. "
             "What is the price after both changes?",
        "answer": "₱5,100",
        "explanation": "After 20% increase: ₱5,000 × 1.20 = ₱6,000. After 15% decrease: ₱6,000 × 0.85 = ₱5,100.",
        "distractors": ["₱5,250", "₱5,000", "₱4,900"],
        "tags": ["multi-step", "successive changes", "hard"],
    },
    {
        "q": "A factory produced 8,000 units. Production increased by 25% in Q1 and decreased by 20% in Q2. "
             "How many units were produced in Q2?",
        "answer": "8,000",
        "explanation": "Q1: 8,000 × 1.25 = 10,000. Q2: 10,000 × 0.80 = 8,000.",
        "distractors": ["7,500", "8,500", "9,000"],
        "tags": ["multi-step", "production", "successive changes", "hard"],
    },
    {
        "q": "A worker's salary is ₱25,000. After a 20% increase and then a 10% tax deduction on the new salary, "
             "what is the take-home pay?",
        "answer": "₱27,000",
        "explanation": "After 20% raise: ₱25,000 × 1.20 = ₱30,000. After 10% tax: ₱30,000 × 0.90 = ₱27,000.",
        "distractors": ["₱28,000", "₱25,000", "₱26,500"],
        "tags": ["multi-step", "salary", "tax", "hard"],
    },
    {
        "q": "A company's revenue was ₱1,000,000. It grew by 30% in Year 1 and 20% in Year 2. "
             "What is the total percent increase over the two years?",
        "answer": "56%",
        "explanation": "Multiplier = 1.30 × 1.20 = 1.56. Total increase = 56%.",
        "distractors": ["50%", "60%", "45%"],
        "tags": ["multi-step", "revenue growth", "successive changes", "hard"],
    },
    {
        "q": "A school had 1,500 students. Enrollment dropped by 10% one year and then increased by 20% the next. "
             "How many students are there now?",
        "answer": "1,620",
        "explanation": "After 10% drop: 1,500 × 0.90 = 1,350. After 20% increase: 1,350 × 1.20 = 1,620.",
        "distractors": ["1,650", "1,500", "1,580"],
        "tags": ["multi-step", "enrollment", "successive changes", "hard"],
    },
    {
        "q": "An investment of ₱100,000 gains 15% in the first year and loses 10% in the second year. "
             "What is the value after two years?",
        "answer": "₱103,500",
        "explanation": "Year 1: ₱100,000 × 1.15 = ₱115,000. Year 2: ₱115,000 × 0.90 = ₱103,500.",
        "distractors": ["₱105,000", "₱100,000", "₱102,000"],
        "tags": ["multi-step", "investment", "successive changes", "hard"],
    },
    {
        "q": "A department's budget of ₱2,000,000 was increased by 15% and then 10% of the new budget "
             "was allocated to training. How much was allocated to training?",
        "answer": "₱230,000",
        "explanation": "New budget: ₱2,000,000 × 1.15 = ₱2,300,000. Training: ₱2,300,000 × 0.10 = ₱230,000.",
        "distractors": ["₱200,000", "₱250,000", "₱215,000"],
        "tags": ["multi-step", "budget", "allocation", "hard"],
    },
]

for prob in hard_word_problems:
    choices = shuffle_choices(prob["answer"], prob["distractors"])
    questions.append(make_q("Hard", prob["q"], choices, prob["answer"], prob["explanation"], prob["tags"]))


# More hard word problems (20 more)
hard_word_problems_2 = [
    {
        "q": "A product costs ₱4,000. The manufacturer increases the price by 30%, "
             "and then a retailer adds another 20% markup. What is the final retail price?",
        "answer": "₱6,240",
        "explanation": "After 30%: ₱4,000 × 1.30 = ₱5,200. After 20%: ₱5,200 × 1.20 = ₱6,240.",
        "distractors": ["₱6,000", "₱6,400", "₱5,800"],
        "tags": ["multi-step", "markup", "successive increases", "hard"],
    },
    {
        "q": "A government project's cost was estimated at ₱10,000,000. Due to delays, costs increased by 25%. "
             "Then a 10% contingency was added to the new cost. What is the final budget?",
        "answer": "₱13,750,000",
        "explanation": "After 25%: ₱10M × 1.25 = ₱12,500,000. After 10%: ₱12.5M × 1.10 = ₱13,750,000.",
        "distractors": ["₱13,500,000", "₱14,000,000", "₱12,750,000"],
        "tags": ["multi-step", "government project", "cost overrun", "hard"],
    },
    {
        "q": "A car's value depreciates by 15% each year. If it was bought for ₱800,000, "
             "what is its value after 2 years?",
        "answer": "₱578,000",
        "explanation": "Year 1: ₱800,000 × 0.85 = ₱680,000. Year 2: ₱680,000 × 0.85 = ₱578,000.",
        "distractors": ["₱560,000", "₱600,000", "₱544,000"],
        "tags": ["depreciation", "successive decreases", "hard"],
    },
    {
        "q": "A store offers a 20% discount on a ₱3,000 item, then charges 12% VAT on the discounted price. "
             "What is the final price?",
        "answer": "₱2,688",
        "explanation": "After 20% discount: ₱3,000 × 0.80 = ₱2,400. After 12% VAT: ₱2,400 × 1.12 = ₱2,688.",
        "distractors": ["₱2,640", "₱2,700", "₱2,760"],
        "tags": ["discount", "VAT", "multi-step", "hard"],
    },
    {
        "q": "An employee's salary was ₱40,000. It was increased by 10% in January, 5% in July, "
             "and then decreased by 8% in December. What is the final salary?",
        "answer": "₱42,504",
        "explanation": "Jan: ₱40,000 × 1.10 = ₱44,000. Jul: ₱44,000 × 1.05 = ₱46,200. Dec: ₱46,200 × 0.92 = ₱42,504.",
        "distractors": ["₱42,000", "₱43,000", "₱41,800"],
        "tags": ["multi-step", "salary", "three changes", "hard"],
    },
    {
        "q": "A population of 50,000 grows by 4% annually. What is the population after 3 years? (Round to nearest whole number)",
        "answer": "56,243",
        "explanation": "Year 1: 50,000 × 1.04 = 52,000. Year 2: 52,000 × 1.04 = 54,080. Year 3: 54,080 × 1.04 = 56,243.",
        "distractors": ["56,000", "56,500", "55,800"],
        "tags": ["compound growth", "population", "three years", "hard"],
    },
    {
        "q": "A company's stock rose 40% in Q1, fell 30% in Q2, and rose 20% in Q3. "
             "If the stock started at ₱100, what is its value after Q3?",
        "answer": "₱117.60",
        "explanation": "Q1: ₱100 × 1.40 = ₱140. Q2: ₱140 × 0.70 = ₱98. Q3: ₱98 × 1.20 = ₱117.60.",
        "distractors": ["₱120", "₱115", "₱130"],
        "tags": ["stock price", "successive changes", "hard"],
    },
    {
        "q": "A farmer's harvest was 2,000 kg. It increased by 15% the first season and 10% the second season. "
             "What is the total percent increase over both seasons?",
        "answer": "26.5%",
        "explanation": "Multiplier = 1.15 × 1.10 = 1.265. Total increase = 26.5%.",
        "distractors": ["25%", "27%", "30%"],
        "tags": ["successive increases", "agriculture", "hard"],
    },
    {
        "q": "After successive discounts of 20% and 10%, a laptop costs ₱36,000. What was the original price?",
        "answer": "₱50,000",
        "explanation": "Combined multiplier = 0.80 × 0.90 = 0.72. Original = ₱36,000 ÷ 0.72 = ₱50,000.",
        "distractors": ["₱48,000", "₱52,000", "₱45,000"],
        "tags": ["reverse problem", "successive discounts", "hard"],
    },
    {
        "q": "A worker's productivity increased from 80 units/day to 104 units/day after training. "
             "If the company has 50 such workers, how many additional units are produced daily in total?",
        "answer": "1,200",
        "explanation": "Increase per worker = 104 - 80 = 24 units. Total additional = 24 × 50 = 1,200 units.",
        "distractors": ["1,000", "1,400", "1,100"],
        "tags": ["productivity", "multi-step", "hard"],
    },
    {
        "q": "A municipality's tax collection was ₱5,000,000. It increased by 12% one year and 8% the next. "
             "How much more was collected in the second year compared to the original?",
        "answer": "₱1,048,000",
        "explanation": "Year 1: ₱5M × 1.12 = ₱5,600,000. Year 2: ₱5.6M × 1.08 = ₱6,048,000. Difference from original: ₱6,048,000 - ₱5,000,000 = ₱1,048,000.",
        "distractors": ["₱1,000,000", "₱1,100,000", "₱960,000"],
        "tags": ["tax collection", "successive increases", "hard"],
    },
    {
        "q": "A product's price increased by 60%. By what percent must it decrease to return to the original price?",
        "answer": "37.5%",
        "explanation": "After 60% increase, multiplier = 1.60. To return: 1 ÷ 1.60 = 0.625. Decrease needed = 1 - 0.625 = 0.375 = 37.5%.",
        "distractors": ["60%", "40%", "35%"],
        "tags": ["recovery problem", "reverse percentage", "hard"],
    },
    {
        "q": "A company had 1,000 employees. It hired 20% more, then 15% of all employees resigned. "
             "How many employees remain?",
        "answer": "1,020",
        "explanation": "After hiring: 1,000 × 1.20 = 1,200. After resignations: 1,200 × 0.85 = 1,020.",
        "distractors": ["1,050", "1,000", "980"],
        "tags": ["workforce", "successive changes", "hard"],
    },
    {
        "q": "A budget of ₱3,000,000 is cut by 10%, then the remaining budget is increased by 15%. "
             "What is the net percent change from the original budget?",
        "answer": "3.5% increase",
        "explanation": "Multiplier = 0.90 × 1.15 = 1.035. Net change = 3.5% increase.",
        "distractors": ["5% increase", "5% decrease", "3.5% decrease"],
        "tags": ["successive changes", "budget", "net change", "hard"],
    },
    {
        "q": "An item's price was ₱1,200. After a 25% increase and a 20% decrease, "
             "what is the difference between the final price and the original price?",
        "answer": "₱0 (no difference)",
        "explanation": "After 25% increase: ₱1,200 × 1.25 = ₱1,500. After 20% decrease: ₱1,500 × 0.80 = ₱1,200. No difference.",
        "distractors": ["₱60 less", "₱60 more", "₱120 less"],
        "tags": ["successive changes", "break even", "hard"],
    },
    {
        "q": "A government agency's error rate was 8%. After improvements, it dropped to 5%. "
             "What is the percent decrease in the error rate?",
        "answer": "37.5%",
        "explanation": "Decrease = 8 - 5 = 3 percentage points. Percent decrease = 3 ÷ 8 × 100 = 37.5%.",
        "distractors": ["3%", "60%", "30%"],
        "tags": ["percentage point vs percent change", "error rate", "hard"],
    },
    {
        "q": "A store's profit margin went from 12% to 15%. What is the percent increase in the profit margin?",
        "answer": "25%",
        "explanation": "Increase = 15 - 12 = 3 percentage points. Percent increase = 3 ÷ 12 × 100 = 25%.",
        "distractors": ["3%", "20%", "30%"],
        "tags": ["percentage point vs percent change", "profit margin", "hard"],
    },
    {
        "q": "A loan of ₱500,000 accumulates 5% interest annually. After 2 years of compound interest, "
             "how much interest has accumulated in total?",
        "answer": "₱51,250",
        "explanation": "Year 1: ₱500,000 × 0.05 = ₱25,000. Year 2: ₱525,000 × 0.05 = ₱26,250. Total interest = ₱51,250.",
        "distractors": ["₱50,000", "₱52,500", "₱55,000"],
        "tags": ["compound interest", "multi-step", "hard"],
    },
    {
        "q": "A product's price was ₱8,000. It was discounted by 15%, then the discounted price was further "
             "reduced by 10%. What single discount is equivalent to these two successive discounts?",
        "answer": "23.5%",
        "explanation": "Combined multiplier = 0.85 × 0.90 = 0.765. Equivalent single discount = 1 - 0.765 = 0.235 = 23.5%.",
        "distractors": ["25%", "22%", "20%"],
        "tags": ["equivalent discount", "successive discounts", "hard"],
    },
    {
        "q": "A city's water consumption decreased by 12% in summer due to conservation efforts, "
             "then increased by 18% in winter. If original consumption was 500,000 liters, "
             "what is the consumption after both changes?",
        "answer": "519,200 liters",
        "explanation": "Summer: 500,000 × 0.88 = 440,000. Winter: 440,000 × 1.18 = 519,200.",
        "distractors": ["530,000 liters", "510,000 liters", "525,000 liters"],
        "tags": ["successive changes", "water consumption", "hard"],
    },
]

for prob in hard_word_problems_2:
    choices = shuffle_choices(prob["answer"], prob["distractors"])
    questions.append(make_q("Hard", prob["q"], choices, prob["answer"], prob["explanation"], prob["tags"]))


# --- Category 6: Percentage Change with Non-Clean Numbers (30 questions) ---
hard_nonclean_increase_bases = [
    (840, 1092), (750, 990), (1250, 1625), (3600, 4680), (4800, 6240),
    (960, 1200), (1440, 1872), (2100, 2730), (3200, 4160), (5600, 7280),
    (720, 900), (1350, 1755), (2400, 3120), (4500, 5850), (6000, 7800),
]

hard_nonclean_decrease_bases = [
    (1200, 900), (1600, 1200), (2500, 1875), (3000, 2250), (4000, 3000),
    (4800, 3600), (5400, 4050), (6400, 4800), (7200, 5400), (8000, 6000),
    (9600, 7200), (1080, 810), (1440, 1080), (1800, 1350), (2160, 1620),
]

for i in range(15):
    orig, new_val = hard_nonclean_increase_bases[i]
    rate = round((new_val - orig) / orig * 100, 2)
    question_text = (f"The number of applicants for a government position increased from "
                     f"{orig:,} to {new_val:,}. What is the percent increase?")
    correct = fmt_pct_clean(rate)
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    change = new_val - orig
    explanation = (f"Increase = {new_val:,} − {orig:,} = {change:,}. "
                   f"Percent = {change:,} ÷ {orig:,} × 100 = {fmt_pct_clean(rate)}.")
    tags = ["percent increase", "non-clean numbers", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))

for i in range(15):
    orig, new_val = hard_nonclean_decrease_bases[i]
    rate = round((orig - new_val) / orig * 100, 2)
    question_text = (f"A department's monthly expenses dropped from ₱{orig:,} to ₱{new_val:,}. "
                     f"What is the percent decrease?")
    correct = fmt_pct_clean(rate)
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    change = orig - new_val
    explanation = (f"Decrease = ₱{orig:,} − ₱{new_val:,} = ₱{change:,}. "
                   f"Percent = {change:,} ÷ {orig:,} × 100 = {fmt_pct_clean(rate)}.")
    tags = ["percent decrease", "non-clean numbers", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))


# ============================================================
# OUTPUT
# ============================================================

# Verify counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}, Total: {len(questions)}")

# If we have fewer than 200 in any category, we need to pad
# Pad Easy if needed
while easy_count < 200:
    rate = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    base = random.choice([100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000])
    new_val = int(base * (1 + rate / 100))
    question_text = f"What is the percent increase from {base:,} to {new_val:,}?"
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    explanation = f"Increase = {new_val - base:,}. Percent = {new_val - base:,} ÷ {base:,} × 100 = {rate}%."
    tags = ["percent increase", "basic computation", "basic percentage change"]
    questions.append(make_q("Easy", question_text, choices, correct, explanation, tags))
    easy_count += 1

# Pad Medium if needed
while medium_count < 200:
    rate = random.choice([6, 8, 12, 14, 16, 18, 22, 24, 28, 32, 35, 45])
    base = random.choice([12000, 15000, 18000, 20000, 25000, 30000, 35000, 40000, 50000, 60000])
    new_val = int(base * (1 + rate / 100))
    question_text = f"A company's revenue grew from ₱{base:,} to ₱{new_val:,}. What is the percent increase?"
    correct = f"{rate}%"
    distractors = [fmt_pct_clean(d) for d in generate_pct_distractors(rate)]
    choices = shuffle_choices(correct, distractors)
    change = new_val - base
    explanation = f"Increase = ₱{change:,}. Percent = {change:,} ÷ {base:,} × 100 = {rate}%."
    tags = ["percent increase", "revenue", "medium difficulty"]
    questions.append(make_q("Medium", question_text, choices, correct, explanation, tags))
    medium_count += 1

# Pad Hard if needed
while hard_count < 200:
    r1 = random.choice([10, 15, 20, 25, 30, 35, 40])
    r2 = random.choice([5, 10, 15, 20, 25, 30])
    r3 = random.choice([5, 10, 15, 20, 25])
    m1, m2, m3 = 1 + r1/100, 1 - r2/100, 1 + r3/100
    mult = m1 * m2 * m3
    net_pct = round(abs(mult - 1) * 100, 2)
    direction = "increase" if mult > 1 else "decrease"
    question_text = (f"A value increases by {r1}%, decreases by {r2}%, then increases by {r3}%. "
                     f"What is the net percent change?")
    correct = f"{fmt_pct_clean(net_pct)} {direction}"
    distractors_pcts = generate_pct_distractors(net_pct)
    distractors = [f"{fmt_pct_clean(d)} {direction}" for d in distractors_pcts[:2]]
    distractors.append(f"{r1 - r2 + r3}% {direction}")
    choices = shuffle_choices(correct, distractors[:3])
    explanation = f"Multiplier = {m1:.2f} × {m2:.2f} × {m3:.2f} = {mult:.4f}. Net = {fmt_pct_clean(net_pct)} {direction}."
    tags = ["successive changes", "multiplier method", "hard"]
    questions.append(make_q("Hard", question_text, choices, correct, explanation, tags))
    hard_count += 1

# Final count check
easy_final = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_final = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_final = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final - Easy: {easy_final}, Medium: {medium_final}, Hard: {hard_final}, Total: {len(questions)}")

# Reassign IDs sequentially
for idx, q in enumerate(questions, 1):
    q["id"] = idx

# Write output
output_dir = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "numerical-ability" / "percentages" / "percentage-increase-and-decrease"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "questions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written {len(questions)} questions to {output_path}")
