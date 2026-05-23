"""Generate 600 questions for Estimation and Mental Math subtopic.

Produces exactly 200 Easy, 200 Medium, 200 Hard questions covering:
- Rounding numbers
- Estimation techniques
- Mental addition/subtraction/multiplication/division
- Decimal and fraction estimation
- Answer reasonableness
- Real-life applications

Run: python scripts/gen_estimation_questions.py
"""

import json
import random
from pathlib import Path

random.seed(42)

OUTPUT_PATH = Path(__file__).resolve().parent.parent / (
    "data/seed/questions/numerical-ability/basic-operations/"
    "estimation-and-mental-math/questions.json"
)

COMMON_FIELDS = {
    "subtest": "Numerical Ability",
    "module": "Basic Operations",
    "subtopic": "Estimation and Mental Math",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}


def _shuffle_choices(correct, distractors):
    """Return shuffled choices list with correct answer included."""
    choices = [correct] + distractors
    random.shuffle(choices)
    return choices


questions: list[dict] = []
qid = 0
_used_questions: set[str] = set()  # Track question text to avoid duplicates


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Rounding to nearest ten (40 questions) ---
rounding_ten_data = []
_used_rounding_ten: set[int] = set()
for _ in range(40):
    for _attempt in range(50):
        n = random.randint(11, 999)
        if n not in _used_rounding_ten:
            _used_rounding_ten.add(n)
            break
    ones = n % 10
    if ones >= 5:
        rounded = n - ones + 10
    else:
        rounded = n - ones
    # Generate distractors
    d1 = rounded + 10
    d2 = rounded - 10
    d3 = rounded + 20 if random.random() > 0.5 else rounded - 20
    # Ensure no negatives or duplicates
    dists = list(set([d1, d2, d3]) - {rounded})
    while len(dists) < 3:
        dists.append(rounded + random.choice([30, -30, 40, -40]))
    dists = [d for d in dists if d >= 0]
    while len(dists) < 3:
        dists.append(rounded + random.randint(2, 5) * 10)
    dists = list(set(dists) - {rounded})[:3]
    rounding_ten_data.append((n, rounded, dists))

for n, rounded, dists in rounding_ten_data:
    qid += 1
    ones = n % 10
    direction = "up" if ones >= 5 else "down"
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"Round {n:,} to the nearest ten.",
        "choices": _shuffle_choices(f"{rounded:,}", [f"{d:,}" for d in dists]),
        "answer": f"{rounded:,}",
        "explanation": (
            f"The ones digit is {ones}. Since {ones} "
            f"{'≥ 5, round up' if ones >= 5 else '< 5, round down'}. "
            f"{n:,} rounded to the nearest ten is {rounded:,}."
        ),
        "tags": ["rounding", "nearest ten", "estimation"],
    })

# --- Rounding to nearest hundred (30 questions) ---
for _ in range(30):
    n = random.randint(101, 9999)
    tens = (n // 10) % 10
    hundreds = (n // 100) * 100
    if tens >= 5:
        rounded = hundreds + 100
    else:
        rounded = hundreds
    d1 = rounded + 100
    d2 = rounded - 100
    d3 = rounded + 200 if random.random() > 0.5 else rounded - 200
    dists = list(set([d1, d2, d3]) - {rounded})
    dists = [d for d in dists if d >= 0]
    while len(dists) < 3:
        dists.append(rounded + random.choice([300, 400, 500]))
    dists = list(set(dists) - {rounded})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"Round {n:,} to the nearest hundred.",
        "choices": _shuffle_choices(f"{rounded:,}", [f"{d:,}" for d in dists]),
        "answer": f"{rounded:,}",
        "explanation": (
            f"The tens digit is {tens}. Since {tens} "
            f"{'≥ 5, round up' if tens >= 5 else '< 5, round down'}. "
            f"{n:,} rounded to the nearest hundred is {rounded:,}."
        ),
        "tags": ["rounding", "nearest hundred", "estimation"],
    })

# --- Simple mental addition (40 questions) ---
for _ in range(40):
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    correct = a + b
    d1 = correct + random.randint(1, 5)
    d2 = correct - random.randint(1, 5)
    d3 = correct + random.randint(6, 12)
    dists = list(set([d1, d2, d3]) - {correct})
    while len(dists) < 3:
        dists.append(correct + random.choice([-8, 8, -12, 15]))
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"Mentally compute: {a} + {b} = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": f"{a} + {b} = {correct}.",
        "tags": ["mental math", "addition", "mental computation"],
    })

# --- Simple mental subtraction (30 questions) ---
for _ in range(30):
    a = random.randint(50, 200)
    b = random.randint(10, a - 1)
    correct = a - b
    d1 = correct + random.randint(1, 5)
    d2 = correct - random.randint(1, 5)
    d3 = correct + random.randint(6, 10)
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d >= 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([7, -7, 11, -3]))
    dists = [d for d in dists if d >= 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"Mentally compute: {a} - {b} = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": f"{a} - {b} = {correct}.",
        "tags": ["mental math", "subtraction", "mental computation"],
    })

# --- Multiply by 10/100/1000 (30 questions) ---
for _ in range(30):
    a = random.randint(2, 999)
    multiplier = random.choice([10, 100, 1000])
    correct = a * multiplier
    # Distractors: wrong number of zeros
    if multiplier == 10:
        dists = [a * 100, a * 1, a * 10 + a]
    elif multiplier == 100:
        dists = [a * 10, a * 1000, a * 100 + a]
    else:
        dists = [a * 100, a * 10000, a * 1000 + a]
    dists = list(set(dists) - {correct})[:3]
    while len(dists) < 3:
        dists.append(correct + random.choice([a, -a, a * 2]))
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"What is {a:,} × {multiplier:,}?",
        "choices": _shuffle_choices(f"{correct:,}", [f"{d:,}" for d in dists]),
        "answer": f"{correct:,}",
        "explanation": (
            f"Multiplying by {multiplier:,} means appending "
            f"{len(str(multiplier)) - 1} zero(s). "
            f"{a:,} × {multiplier:,} = {correct:,}."
        ),
        "tags": ["mental math", "multiplication", "powers of 10"],
    })

# --- Divide by 10/100 (15 questions) ---
for _ in range(15):
    multiplier = random.choice([10, 100])
    result = random.randint(2, 500)
    a = result * multiplier
    correct = result
    dists_set = set()
    dists_set.add(correct * 10)
    dists_set.add(a)
    dists_set.add(correct + random.randint(1, 10))
    dists_set.discard(correct)
    dists = list(dists_set)[:3]
    while len(dists) < 3:
        dists.append(correct + random.choice([5, -5, 20, -20]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": f"What is {a:,} ÷ {multiplier}?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": (
            f"Dividing by {multiplier} means removing "
            f"{len(str(multiplier)) - 1} zero(s). "
            f"{a:,} ÷ {multiplier} = {correct}."
        ),
        "tags": ["mental math", "division", "powers of 10"],
    })

# --- Simple estimation (which is closest) (15 questions) ---
for _ in range(15):
    a = random.randint(100, 900)
    b = random.randint(100, 900)
    correct = a + b
    # Choices are spread apart
    choices_raw = [correct, correct + 100, correct - 100, correct + 200]
    random.shuffle(choices_raw)
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Easy",
        "question": (
            f"Which is the best estimate for {a} + {b}?"
        ),
        "choices": [str(c) for c in sorted(choices_raw)],
        "answer": str(correct),
        "explanation": (
            f"{a} + {b} = {correct}. The best estimate is {correct}."
        ),
        "tags": ["estimation", "addition", "mental math"],
    })

# Ensure we have exactly 200 easy questions
easy_count = len([q for q in questions if q["difficulty"] == "Easy"])
assert easy_count == 200, f"Expected 200 easy, got {easy_count}"


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Rounding to nearest thousand (20 questions) ---
for _ in range(20):
    n = random.randint(1001, 99999)
    hundreds = (n // 100) % 10
    thousands = (n // 1000) * 1000
    if hundreds >= 5:
        rounded = thousands + 1000
    else:
        rounded = thousands
    d1 = rounded + 1000
    d2 = rounded - 1000
    d3 = thousands if hundreds >= 5 else thousands + 1000
    dists = list(set([d1, d2, d3]) - {rounded})
    dists = [d for d in dists if d >= 0]
    while len(dists) < 3:
        dists.append(rounded + random.choice([2000, 3000, -2000]))
    dists = [d for d in dists if d >= 0]
    dists = list(set(dists) - {rounded})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Round {n:,} to the nearest thousand.",
        "choices": _shuffle_choices(f"{rounded:,}", [f"{d:,}" for d in dists]),
        "answer": f"{rounded:,}",
        "explanation": (
            f"The hundreds digit is {hundreds}. Since {hundreds} "
            f"{'≥ 5, round up' if hundreds >= 5 else '< 5, round down'}. "
            f"{n:,} rounded to the nearest thousand is {rounded:,}."
        ),
        "tags": ["rounding", "nearest thousand", "estimation"],
    })

# --- Rounding decimals (20 questions) ---
for _ in range(20):
    # Round to nearest tenth
    whole = random.randint(0, 50)
    tenths = random.randint(0, 9)
    hundredths = random.randint(0, 9)
    n = whole + tenths / 10 + hundredths / 100
    n_str = f"{n:.2f}"
    if hundredths >= 5:
        rounded_val = whole + (tenths + 1) / 10
    else:
        rounded_val = whole + tenths / 10
    rounded_str = f"{rounded_val:.1f}"
    # Generate distractors that are always different from the answer
    candidate_dists = set()
    candidate_dists.add(f"{rounded_val + 0.1:.1f}")
    candidate_dists.add(f"{rounded_val - 0.1:.1f}")
    candidate_dists.add(f"{rounded_val + 0.2:.1f}")
    candidate_dists.add(f"{rounded_val - 0.2:.1f}")
    candidate_dists.add(f"{rounded_val + 1.0:.1f}")
    candidate_dists.discard(rounded_str)
    dists = list(candidate_dists)[:3]
    while len(dists) < 3:
        dists.append(f"{rounded_val + random.choice([0.3, 0.4, -0.3]):.1f}")
    dists = list(set(dists) - {rounded_str})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Round {n_str} to the nearest tenth.",
        "choices": _shuffle_choices(rounded_str, dists),
        "answer": rounded_str,
        "explanation": (
            f"The hundredths digit is {hundredths}. Since {hundredths} "
            f"{'≥ 5, round up' if hundredths >= 5 else '< 5, round down'}. "
            f"{n_str} rounded to the nearest tenth is {rounded_str}."
        ),
        "tags": ["rounding", "decimals", "nearest tenth"],
    })

# --- Mental multiplication by 5 and 25 (25 questions) ---
_used_mult_5_25: set[str] = set()
for _ in range(25):
    for _attempt in range(20):
        if random.random() > 0.5:
            # Multiply by 5
            a = random.randint(12, 198)
            correct = a * 5
            mult = 5
            expl = f"{a} × 5 = {a} × 10 ÷ 2 = {a * 10} ÷ 2 = {correct}."
        else:
            # Multiply by 25
            a = random.randint(4, 99)
            # Ensure divisible by 4 for clean division
            if a % 4 != 0:
                a = (a // 4 + 1) * 4
            correct = a * 25
            mult = 25
            expl = f"{a} × 25 = {a} ÷ 4 × 100 = {a // 4} × 100 = {correct}."
        q_key = f"{a}x{mult}"
        if q_key not in _used_mult_5_25:
            _used_mult_5_25.add(q_key)
            break
    d1 = correct + random.randint(5, 50)
    d2 = correct - random.randint(5, 50)
    d3 = correct + random.randint(51, 100)
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([25, -25, 75, -75]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Mentally compute: {a} × {mult} = ?",
        "choices": _shuffle_choices(f"{correct:,}", [f"{d:,}" for d in dists]),
        "answer": f"{correct:,}",
        "explanation": expl,
        "tags": ["mental math", "multiplication", "shortcuts"],
    })

# --- Mental subtraction with compensation (25 questions) ---
for _ in range(25):
    a = random.randint(100, 999)
    # Make b close to a round number
    base = random.choice([50, 100, 150, 200, 250, 300, 400, 500])
    offset = random.randint(1, 4)
    b = base - offset
    if b >= a:
        a = b + random.randint(10, 200)
    correct = a - b
    expl = (
        f"{a} - {b} = {a} - {base} + {offset} = "
        f"{a - base} + {offset} = {correct}."
    )
    d1 = correct + random.randint(1, 5)
    d2 = correct - random.randint(1, 5)
    d3 = a - base  # common error: forgot to add back
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d >= 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([10, -10, 7, -7]))
    dists = [d for d in dists if d >= 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Mentally compute: {a} - {b} = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": expl,
        "tags": ["mental math", "subtraction", "compensation"],
    })

# --- Front-end estimation (20 questions) ---
for _ in range(20):
    a = random.randint(100, 9000)
    b = random.randint(100, 9000)
    exact = a + b
    # Front-end: use leading digit × place value
    a_front = (a // 1000) * 1000 if a >= 1000 else (a // 100) * 100
    b_front = (b // 1000) * 1000 if b >= 1000 else (b // 100) * 100
    estimate = a_front + b_front
    # Generate 3 distractors different from estimate
    candidate_dists = [
        estimate + 500, estimate - 500, estimate + 1000,
        estimate - 1000, estimate + 200, estimate - 200,
        estimate + 1500, estimate + 2000,
    ]
    dists = [d for d in candidate_dists if d != estimate and d > 0]
    random.shuffle(dists)
    # Deduplicate
    seen = {estimate}
    final_dists = []
    for d in dists:
        if d not in seen and len(final_dists) < 3:
            seen.add(d)
            final_dists.append(d)
    while len(final_dists) < 3:
        new_d = estimate + random.randint(1, 20) * 100
        if new_d not in seen:
            seen.add(new_d)
            final_dists.append(new_d)
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Using front-end estimation, what is the best estimate for {a:,} + {b:,}?",
        "choices": _shuffle_choices(f"{estimate:,}", [f"{d:,}" for d in final_dists]),
        "answer": f"{estimate:,}",
        "explanation": (
            f"Front-end estimation: {a_front:,} + {b_front:,} = {estimate:,}. "
            f"(Exact answer: {exact:,})"
        ),
        "tags": ["estimation", "front-end", "addition"],
    })

# --- Compatible numbers for division (20 questions) ---
for _ in range(20):
    divisor = random.choice([3, 4, 5, 6, 7, 8, 9, 12, 15, 20, 25])
    quotient = random.randint(5, 100)
    compatible = divisor * quotient
    # Actual dividend is close but not exactly divisible
    offset = random.randint(1, divisor - 1)
    actual = compatible + offset
    qid += 1
    d1 = quotient + 1
    d2 = quotient - 1
    d3 = quotient + random.randint(2, 5)
    dists = list(set([d1, d2, d3]) - {quotient})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(quotient + random.choice([3, -3, 5, -5]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {quotient})[:3]
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": (
            f"Using compatible numbers, estimate {actual} ÷ {divisor}."
        ),
        "choices": _shuffle_choices(str(quotient), [str(d) for d in dists]),
        "answer": str(quotient),
        "explanation": (
            f"{actual} is close to {compatible}. "
            f"{compatible} ÷ {divisor} = {quotient}. "
            f"The best estimate is {quotient}."
        ),
        "tags": ["estimation", "compatible numbers", "division"],
    })

# --- Distributive property multiplication (20 questions) ---
for _ in range(20):
    a = random.randint(3, 12)
    # b is close to a round number
    base = random.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
    offset = random.randint(1, 3)
    if random.random() > 0.5:
        b = base - offset
        correct = a * b
        expl = (
            f"{a} × {b} = {a} × ({base} - {offset}) = "
            f"{a * base} - {a * offset} = {correct}."
        )
    else:
        b = base + offset
        correct = a * b
        expl = (
            f"{a} × {b} = {a} × ({base} + {offset}) = "
            f"{a * base} + {a * offset} = {correct}."
        )
    d1 = correct + random.randint(1, 10)
    d2 = correct - random.randint(1, 10)
    d3 = a * base  # common error: forgot the offset part
    dists = list(set([d1, d2, d3]) - {correct})
    while len(dists) < 3:
        dists.append(correct + random.choice([15, -15, 20, -20]))
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Mentally compute: {a} × {b} = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": expl,
        "tags": ["mental math", "multiplication", "distributive property"],
    })

# --- Division by 5 (15 questions) ---
for _ in range(15):
    result = random.randint(5, 200)
    a = result * 5
    correct = result
    d1 = correct + random.randint(1, 5)
    d2 = correct - random.randint(1, 5)
    d3 = a // 10  # common error: divided by 10 instead of 5
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([10, -10, 7]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Mentally compute: {a} ÷ 5 = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": (
            f"{a} ÷ 5 = {a} × 2 ÷ 10 = {a * 2} ÷ 10 = {correct}."
        ),
        "tags": ["mental math", "division", "divide by 5"],
    })

# --- Reasonableness / estimation word problems (20 questions) ---
reasonableness_scenarios = [
    ("A clerk adds {a:,} and {b:,}. Which is the most reasonable answer?",
     lambda a, b: a + b, "addition"),
    ("An office buys {a} items at ₱{b} each. Which is the best estimate of the total cost?",
     lambda a, b: a * b, "multiplication"),
    ("A budget of ₱{total:,} is split equally among {n} departments. Approximately how much does each get?",
     None, "division"),
]

for i in range(20):
    if i < 8:
        # Addition reasonableness
        a = random.randint(1000, 9000)
        b = random.randint(1000, 9000)
        correct = a + b
        q_text = f"A clerk adds {a:,} and {b:,}. Which is the most reasonable answer?"
        expl = f"{a:,} + {b:,} = {correct:,}."
        tags_q = ["estimation", "reasonableness", "addition"]
    elif i < 14:
        # Multiplication reasonableness
        a = random.randint(10, 50)
        b = random.randint(50, 500)
        correct = a * b
        q_text = f"An office buys {a} items at ₱{b} each. Which is the best estimate of the total cost?"
        expl = f"{a} × {b} = {correct:,}."
        tags_q = ["estimation", "reasonableness", "multiplication", "word problem"]
    else:
        # Division reasonableness
        n = random.choice([3, 4, 5, 6, 8, 10, 12])
        per_dept = random.randint(100, 5000)
        total = n * per_dept
        correct = per_dept
        a, b = total, n
        q_text = (
            f"A budget of ₱{total:,} is split equally among {n} departments. "
            f"Approximately how much does each department get?"
        )
        expl = f"₱{total:,} ÷ {n} = ₱{per_dept:,}."
        tags_q = ["estimation", "reasonableness", "division", "word problem"]

    # Generate spread-out distractors
    if correct > 1000:
        spread = correct // 5
    else:
        spread = max(correct // 3, 10)
    d1 = correct + spread
    d2 = correct - spread
    d3 = correct + spread * 2
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([spread * 3, -spread // 2]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": q_text,
        "choices": _shuffle_choices(f"₱{correct:,}" if "₱" in q_text else f"{correct:,}",
                                     [f"₱{d:,}" if "₱" in q_text else f"{d:,}" for d in dists]),
        "answer": f"₱{correct:,}" if "₱" in q_text else f"{correct:,}",
        "explanation": expl,
        "tags": tags_q,
    })

# --- Clustering estimation (15 questions) ---
for _ in range(15):
    center = random.randint(20, 500)
    count = random.randint(4, 6)
    numbers = [center + random.randint(-5, 5) for _ in range(count)]
    exact = sum(numbers)
    estimate = center * count
    nums_str = " + ".join(str(n) for n in numbers)
    d1 = estimate + center
    d2 = estimate - center
    d3 = exact + random.randint(10, 30)
    dists = list(set([d1, d2, d3]) - {estimate})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(estimate + random.choice([50, -50, 100]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {estimate})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Medium",
        "question": f"Using clustering, estimate: {nums_str}.",
        "choices": _shuffle_choices(str(estimate), [str(d) for d in dists]),
        "answer": str(estimate),
        "explanation": (
            f"All numbers cluster around {center}. "
            f"{count} × {center} = {estimate}. (Exact: {exact})"
        ),
        "tags": ["estimation", "clustering", "addition"],
    })

medium_count = len([q for q in questions if q["difficulty"] == "Medium"])
assert medium_count == 200, f"Expected 200 medium, got {medium_count}"

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Rounding with carry (20 questions) ---
for _ in range(20):
    # Numbers where rounding causes a carry (e.g., 9,950 → 10,000)
    # Build numbers with 9 in the target place
    place = random.choice(["hundred", "thousand"])
    if place == "hundred":
        # e.g., X,9YZ where Y >= 5
        thousands = random.randint(1, 9)
        tens = random.randint(5, 9)
        ones = random.randint(0, 9)
        n = thousands * 1000 + 900 + tens * 10 + ones
        rounded = (thousands + 1) * 1000
        decision_digit = tens
        target_name = "hundred"
    else:
        # e.g., X9,YZZ where Y >= 5
        ten_thousands = random.randint(1, 9)
        hundreds = random.randint(5, 9)
        rest = random.randint(0, 99)
        n = ten_thousands * 10000 + 9000 + hundreds * 100 + rest
        rounded = (ten_thousands + 1) * 10000
        decision_digit = hundreds
        target_name = "thousand"

    d1 = n  # common error: no rounding
    d2 = rounded - 1000 if place == "thousand" else rounded - 100
    d3 = rounded + 1000 if place == "thousand" else rounded + 100
    dists = list(set([d1, d2, d3]) - {rounded})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(rounded + random.choice([500, -500, 2000]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {rounded})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": f"Round {n:,} to the nearest {target_name}.",
        "choices": _shuffle_choices(f"{rounded:,}", [f"{d:,}" for d in dists]),
        "answer": f"{rounded:,}",
        "explanation": (
            f"The decision digit is {decision_digit} (≥ 5), so round up. "
            f"Since the {target_name}s digit is 9, rounding up causes a carry. "
            f"{n:,} → {rounded:,}."
        ),
        "tags": ["rounding", "carry", "estimation", "hard"],
    })

# --- Multi-step estimation word problems (25 questions) ---
for i in range(25):
    scenario = i % 6
    if scenario == 0:
        # Payroll estimation
        employees = random.randint(30, 200)
        salary = random.randint(15000, 45000)
        salary = (salary // 500) * 500  # round to 500
        correct = employees * salary
        emp_round = round(employees / 10) * 10
        sal_round = round(salary / 1000) * 1000
        estimate = emp_round * sal_round
        q_text = (
            f"A government agency has {employees} employees, each earning "
            f"₱{salary:,} monthly. Estimate the total monthly payroll."
        )
        expl = (
            f"{employees} ≈ {emp_round}, ₱{salary:,} ≈ ₱{sal_round:,}. "
            f"{emp_round} × ₱{sal_round:,} = ₱{estimate:,}. "
            f"(Exact: ₱{correct:,})"
        )
        answer_val = estimate
        tags_q = ["estimation", "payroll", "word problem", "multiplication"]
    elif scenario == 1:
        # Budget allocation
        items = random.randint(3, 5)
        amounts = [random.randint(5000, 50000) for _ in range(items)]
        correct = sum(amounts)
        rounded_amounts = [round(a / 1000) * 1000 for a in amounts]
        estimate = sum(rounded_amounts)
        amounts_str = ", ".join(f"₱{a:,}" for a in amounts)
        q_text = (
            f"A department's expenses are: {amounts_str}. "
            f"Estimate the total expenses."
        )
        expl = (
            f"Rounding each to the nearest thousand and adding: "
            f"₱{estimate:,}. (Exact: ₱{correct:,})"
        )
        answer_val = estimate
        tags_q = ["estimation", "budgeting", "word problem", "addition"]
    elif scenario == 2:
        # Discount calculation
        price = random.randint(500, 5000)
        price = (price // 50) * 50
        discount_pct = random.choice([15, 20, 25, 30, 35, 40])
        discount_amt = price * discount_pct // 100
        sale_price = price - discount_amt
        q_text = (
            f"An item costs ₱{price:,} with a {discount_pct}% discount. "
            f"Estimate the sale price."
        )
        expl = (
            f"{discount_pct}% of ₱{price:,} = ₱{discount_amt:,}. "
            f"Sale price = ₱{price:,} - ₱{discount_amt:,} = ₱{sale_price:,}."
        )
        answer_val = sale_price
        tags_q = ["estimation", "discount", "word problem", "percentage"]
    elif scenario == 3:
        # Travel time
        distance = random.randint(100, 600)
        speed = random.choice([40, 50, 60, 80, 100])
        hours = distance / speed
        hours_rounded = round(hours * 2) / 2  # round to nearest 0.5
        q_text = (
            f"A vehicle travels {distance} km at {speed} km/h. "
            f"Estimate the travel time in hours."
        )
        expl = f"{distance} ÷ {speed} ≈ {hours_rounded} hours. (Exact: {hours:.2f} hours)"
        answer_val = hours_rounded
        tags_q = ["estimation", "travel", "word problem", "division"]
    elif scenario == 4:
        # Percentage increase
        original = random.randint(1000, 10000)
        original = (original // 100) * 100
        pct = random.choice([5, 8, 10, 12, 15, 20])
        increase = original * pct // 100
        new_val = original + increase
        q_text = (
            f"A utility bill of ₱{original:,} increases by {pct}%. "
            f"Estimate the new bill amount."
        )
        expl = (
            f"{pct}% of ₱{original:,} = ₱{increase:,}. "
            f"New amount = ₱{original:,} + ₱{increase:,} = ₱{new_val:,}."
        )
        answer_val = new_val
        tags_q = ["estimation", "percentage", "word problem", "increase"]
    else:
        # Inventory
        shelves = random.randint(8, 25)
        per_shelf = random.randint(30, 200)
        correct = shelves * per_shelf
        s_round = round(shelves / 5) * 5 if shelves > 10 else shelves
        p_round = round(per_shelf / 10) * 10
        estimate = s_round * p_round
        q_text = (
            f"A warehouse has {shelves} shelves, each holding approximately "
            f"{per_shelf} boxes. Estimate the total number of boxes."
        )
        expl = (
            f"{shelves} ≈ {s_round}, {per_shelf} ≈ {p_round}. "
            f"{s_round} × {p_round} = {estimate}. (Exact: {correct})"
        )
        answer_val = estimate
        tags_q = ["estimation", "inventory", "word problem", "multiplication"]

    # Generate distractors
    if isinstance(answer_val, float):
        ans_str = str(answer_val)
        d_vals = [answer_val + 0.5, answer_val - 0.5, answer_val + 1]
        dists_str = [str(d) for d in d_vals if d != answer_val and d > 0][:3]
        while len(dists_str) < 3:
            dists_str.append(str(answer_val + random.choice([1.5, 2, -1])))
        dists_str = list(set(dists_str) - {ans_str})[:3]
        choices = _shuffle_choices(ans_str, dists_str)
        ans_final = ans_str
    else:
        spread = max(answer_val // 10, 100)
        d1 = answer_val + spread
        d2 = answer_val - spread
        d3 = answer_val + spread * 2
        dists = list(set([d1, d2, d3]) - {answer_val})
        dists = [d for d in dists if d > 0]
        while len(dists) < 3:
            dists.append(answer_val + random.choice([spread * 3, -spread * 2, spread // 2]))
        dists = [d for d in dists if d > 0]
        dists = list(set(dists) - {answer_val})[:3]
        peso = "₱" if "₱" in q_text else ""
        choices = _shuffle_choices(
            f"{peso}{answer_val:,}", [f"{peso}{d:,}" for d in dists]
        )
        ans_final = f"{peso}{answer_val:,}"

    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": q_text,
        "choices": choices,
        "answer": ans_final,
        "explanation": expl,
        "tags": tags_q,
    })

# --- Complex mental multiplication (25 questions) ---
_used_mult_hard: set[str] = set()
for _ in range(25):
    for _attempt in range(30):
        technique = random.choice(["near100", "square5", "double_halve", "by9", "by11"])
        if technique == "near100":
            # Multiply number near 100 by single digit
            offset = random.randint(1, 5)
            if random.random() > 0.5:
                b = 100 - offset
            else:
                b = 100 + offset
            a = random.randint(3, 15)
            correct = a * b
            if b < 100:
                expl = f"{a} × {b} = {a} × (100 - {100 - b}) = {a * 100} - {a * (100 - b)} = {correct}."
            else:
                expl = f"{a} × {b} = {a} × (100 + {b - 100}) = {a * 100} + {a * (b - 100)} = {correct}."
            tags_q = ["mental math", "multiplication", "near benchmark"]
            q_key = f"{a}x{b}"
            q_text = f"Mentally compute: {a} × {b} = ?"
        elif technique == "square5":
            tens_digit = random.randint(1, 9)
            b = tens_digit * 10 + 5
            a = b  # squaring
            correct = b * b
            product = tens_digit * (tens_digit + 1)
            expl = f"{b}² = {tens_digit} × {tens_digit + 1} = {product}, append 25 → {correct}."
            tags_q = ["mental math", "multiplication", "squaring", "pattern"]
            q_key = f"{b}sq"
            q_text = f"Mentally compute: {b}² = ?"
        elif technique == "double_halve":
            a = random.choice([4, 8, 12, 14, 16, 18, 22, 24, 26, 28, 32, 34, 36, 38, 42, 44, 46, 48])
            b = random.randint(15, 75)
            correct = a * b
            expl = f"{a} × {b} = {a // 2} × {b * 2} = {(a // 2)} × {b * 2} = {correct}."
            tags_q = ["mental math", "multiplication", "doubling halving"]
            q_key = f"{a}x{b}dh"
            q_text = f"Mentally compute: {a} × {b} = ?"
        elif technique == "by9":
            a = random.randint(12, 99)
            b = 9
            correct = a * 9
            expl = f"{a} × 9 = {a} × 10 - {a} = {a * 10} - {a} = {correct}."
            tags_q = ["mental math", "multiplication", "multiply by 9"]
            q_key = f"{a}x9"
            q_text = f"Mentally compute: {a} × {b} = ?"
        else:  # by11
            a = random.randint(12, 89)
            b = 11
            correct = a * 11
            expl = f"{a} × 11 = {a} × 10 + {a} = {a * 10} + {a} = {correct}."
            tags_q = ["mental math", "multiplication", "multiply by 11"]
            q_key = f"{a}x11"
            q_text = f"Mentally compute: {a} × {b} = ?"

        if q_key not in _used_mult_hard:
            _used_mult_hard.add(q_key)
            break

    d1 = correct + random.randint(1, 15)
    d2 = correct - random.randint(1, 15)
    d3 = correct + random.randint(16, 40)
    dists = list(set([d1, d2, d3]) - {correct})
    while len(dists) < 3:
        dists.append(correct + random.choice([20, -20, 50, -50]))
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": q_text,
        "choices": _shuffle_choices(f"{correct:,}", [f"{d:,}" for d in dists]),
        "answer": f"{correct:,}",
        "explanation": expl,
        "tags": tags_q,
    })

# --- Complex mental division (25 questions) ---
_used_div_hard: set[str] = set()
for _ in range(25):
    for _attempt in range(30):
        technique = random.choice(["by25", "by50", "simplify", "by4", "by8"])
        if technique == "by25":
            result = random.randint(4, 80)
            a = result * 25
            correct = result
            expl = f"{a} ÷ 25 = {a} × 4 ÷ 100 = {a * 4} ÷ 100 = {correct}."
            divisor = 25
            tags_q = ["mental math", "division", "divide by 25"]
        elif technique == "by50":
            result = random.randint(4, 60)
            a = result * 50
            correct = result
            expl = f"{a} ÷ 50 = {a} × 2 ÷ 100 = {a * 2} ÷ 100 = {correct}."
            divisor = 50
            tags_q = ["mental math", "division", "divide by 50"]
        elif technique == "simplify":
            divisor = random.choice([12, 15, 18, 24, 36])
            result = random.randint(5, 50)
            a = divisor * result
            correct = result
            if divisor % 4 == 0:
                step1 = a // 4
                step2 = divisor // 4
                expl = f"{a} ÷ {divisor} = ({a} ÷ 4) ÷ ({divisor} ÷ 4) = {step1} ÷ {step2} = {correct}."
            elif divisor % 3 == 0:
                step1 = a // 3
                step2 = divisor // 3
                expl = f"{a} ÷ {divisor} = ({a} ÷ 3) ÷ ({divisor} ÷ 3) = {step1} ÷ {step2} = {correct}."
            else:
                expl = f"{a} ÷ {divisor} = {correct}."
            tags_q = ["mental math", "division", "simplification"]
        elif technique == "by4":
            result = random.randint(10, 250)
            a = result * 4
            correct = result
            expl = f"{a} ÷ 4 = {a} ÷ 2 ÷ 2 = {a // 2} ÷ 2 = {correct}."
            divisor = 4
            tags_q = ["mental math", "division", "halve twice"]
        else:  # by8
            result = random.randint(5, 125)
            a = result * 8
            correct = result
            expl = f"{a} ÷ 8 = {a} ÷ 2 ÷ 2 ÷ 2 = {a // 2} ÷ 2 ÷ 2 = {a // 4} ÷ 2 = {correct}."
            divisor = 8
            tags_q = ["mental math", "division", "halve thrice"]

        q_key = f"{a}div{divisor}"
        if q_key not in _used_div_hard:
            _used_div_hard.add(q_key)
            break

    d1 = correct + random.randint(1, 5)
    d2 = correct - random.randint(1, 5)
    d3 = correct + random.randint(6, 15)
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([8, -8, 12, -3]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": f"Mentally compute: {a:,} ÷ {divisor} = ?",
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": expl,
        "tags": tags_q,
    })

# --- Estimation with decimals and percentages (25 questions) ---
for _ in range(25):
    scenario = random.choice(["decimal_add", "decimal_mult", "percent_of"])
    if scenario == "decimal_add":
        nums = [round(random.uniform(1, 50), 2) for _ in range(3)]
        exact = round(sum(nums), 2)
        rounded_nums = [round(n) for n in nums]
        estimate = sum(rounded_nums)
        nums_str = " + ".join(f"{n:.2f}" for n in nums)
        q_text = f"Estimate: {nums_str}"
        expl = (
            f"Rounding each to the nearest whole number: "
            f"{' + '.join(str(r) for r in rounded_nums)} = {estimate}. "
            f"(Exact: {exact})"
        )
        answer_val = estimate
        tags_q = ["estimation", "decimals", "addition"]
    elif scenario == "decimal_mult":
        a = round(random.uniform(2, 20), 1)
        b = round(random.uniform(2, 10), 1)
        exact = round(a * b, 2)
        a_round = round(a)
        b_round = round(b)
        estimate = a_round * b_round
        q_text = f"Estimate: {a} × {b}"
        expl = (
            f"{a} ≈ {a_round}, {b} ≈ {b_round}. "
            f"{a_round} × {b_round} = {estimate}. (Exact: {exact})"
        )
        answer_val = estimate
        tags_q = ["estimation", "decimals", "multiplication"]
    else:
        # Percentage of a number
        pct = random.choice([10, 15, 20, 25, 30, 40, 50, 75])
        base = random.randint(100, 5000)
        base = (base // 10) * 10
        correct = base * pct // 100
        q_text = f"Estimate {pct}% of {base:,}."
        if pct == 10:
            expl = f"10% of {base:,} = {base:,} ÷ 10 = {correct:,}."
        elif pct == 25:
            expl = f"25% of {base:,} = {base:,} ÷ 4 = {correct:,}."
        elif pct == 50:
            expl = f"50% of {base:,} = {base:,} ÷ 2 = {correct:,}."
        elif pct == 75:
            expl = f"75% of {base:,} = 3 × ({base:,} ÷ 4) = 3 × {base // 4:,} = {correct:,}."
        elif pct == 15:
            expl = f"15% of {base:,} = 10% + 5% = {base // 10} + {base // 20} = {correct:,}."
        elif pct == 20:
            expl = f"20% of {base:,} = {base:,} ÷ 5 = {correct:,}."
        else:
            expl = f"{pct}% of {base:,} = {base:,} × {pct}/100 = {correct:,}."
        answer_val = correct
        tags_q = ["estimation", "percentage", "mental math"]

    spread = max(answer_val // 5, 5)
    d1 = answer_val + spread
    d2 = answer_val - spread
    d3 = answer_val + spread * 2
    dists = list(set([d1, d2, d3]) - {answer_val})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(answer_val + random.choice([spread * 3, -spread * 2]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {answer_val})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": q_text,
        "choices": _shuffle_choices(str(answer_val), [str(d) for d in dists]),
        "answer": str(answer_val),
        "explanation": expl,
        "tags": tags_q,
    })

# --- Multi-operation mental math (25 questions) ---
for _ in range(25):
    op_type = random.choice(["add3", "sub_add", "mult_add", "chain"])
    if op_type == "add3":
        # Add three 3-digit numbers mentally
        a = random.randint(100, 500)
        b = random.randint(100, 500)
        c = random.randint(100, 500)
        correct = a + b + c
        q_text = f"Mentally compute: {a} + {b} + {c} = ?"
        expl = f"{a} + {b} + {c} = {a + b} + {c} = {correct}."
        tags_q = ["mental math", "addition", "multi-number"]
    elif op_type == "sub_add":
        a = random.randint(200, 900)
        b = random.randint(50, 200)
        c = random.randint(50, 200)
        correct = a - b + c
        q_text = f"Mentally compute: {a} - {b} + {c} = ?"
        expl = f"{a} - {b} + {c} = {a - b} + {c} = {correct}."
        tags_q = ["mental math", "mixed operations"]
    elif op_type == "mult_add":
        a = random.randint(5, 15)
        b = random.randint(10, 50)
        c = random.randint(10, 100)
        correct = a * b + c
        q_text = f"Mentally compute: {a} × {b} + {c} = ?"
        expl = f"{a} × {b} + {c} = {a * b} + {c} = {correct}."
        tags_q = ["mental math", "multiplication", "addition"]
    else:
        # Chain: double then add
        a = random.randint(20, 100)
        correct = a * 2 + a  # triple
        q_text = f"If you double {a} and then add {a} more, what do you get?"
        expl = f"Double {a} = {a * 2}. Add {a}: {a * 2} + {a} = {correct}."
        correct = a * 3
        tags_q = ["mental math", "doubling", "word problem"]

    d1 = correct + random.randint(1, 10)
    d2 = correct - random.randint(1, 10)
    d3 = correct + random.randint(11, 25)
    dists = list(set([d1, d2, d3]) - {correct})
    dists = [d for d in dists if d > 0]
    while len(dists) < 3:
        dists.append(correct + random.choice([15, -15, 30, -30]))
    dists = [d for d in dists if d > 0]
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": q_text,
        "choices": _shuffle_choices(str(correct), [str(d) for d in dists]),
        "answer": str(correct),
        "explanation": expl,
        "tags": tags_q,
    })

# --- Answer reasonableness / elimination (20 questions) ---
for _ in range(20):
    # Which answer is NOT reasonable?
    a = random.randint(100, 5000)
    b = random.randint(100, 5000)
    correct_sum = a + b
    # One choice is wildly off (the unreasonable one)
    unreasonable = correct_sum * random.choice([10, 100]) if random.random() > 0.5 else correct_sum // random.choice([10, 100])
    reasonable_choices = [
        correct_sum,
        correct_sum + random.randint(1, 50),
        correct_sum - random.randint(1, 50),
    ]
    qid += 1
    all_choices = reasonable_choices + [unreasonable]
    random.shuffle(all_choices)
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": (
            f"For the computation {a:,} + {b:,}, which answer is clearly "
            f"NOT reasonable?"
        ),
        "choices": [f"{c:,}" for c in all_choices],
        "answer": f"{unreasonable:,}",
        "explanation": (
            f"{a:,} + {b:,} should be approximately {correct_sum:,}. "
            f"The answer {unreasonable:,} is clearly unreasonable because it is "
            f"{'far too large' if unreasonable > correct_sum * 2 else 'far too small'}."
        ),
        "tags": ["estimation", "reasonableness", "elimination"],
    })

# --- Fraction/benchmark estimation (15 questions) ---
fraction_benchmarks = [
    (1, 4, 0.25, "1/4"),
    (1, 3, 0.33, "1/3"),
    (1, 2, 0.5, "1/2"),
    (2, 3, 0.67, "2/3"),
    (3, 4, 0.75, "3/4"),
    (1, 5, 0.2, "1/5"),
    (3, 8, 0.375, "3/8"),
    (5, 8, 0.625, "5/8"),
]

for i in range(15):
    # "Which benchmark is X/Y closest to?"
    num = random.randint(1, 19)
    den = random.randint(num + 1, 20)
    value = num / den

    # Find closest benchmark
    closest = min(fraction_benchmarks, key=lambda fb: abs(fb[2] - value))
    correct_label = closest[3]

    # Pick 3 other benchmarks as distractors
    others = [fb[3] for fb in fraction_benchmarks if fb[3] != correct_label]
    random.shuffle(others)
    dists = others[:3]

    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": f"Which benchmark fraction is {num}/{den} closest to?",
        "choices": _shuffle_choices(correct_label, dists),
        "answer": correct_label,
        "explanation": (
            f"{num}/{den} = {value:.3f}. "
            f"The closest benchmark is {correct_label} ({closest[2]})."
        ),
        "tags": ["estimation", "fractions", "benchmarks"],
    })

# --- Last-digit / parity elimination (20 questions) ---
for _ in range(20):
    a = random.randint(100, 9999)
    b = random.randint(100, 9999)
    correct = a + b
    last_digit = correct % 10
    # Create distractors with DIFFERENT last digits
    dists = []
    for offset in [1, 2, 3]:
        d = correct + offset
        if d % 10 != last_digit:
            dists.append(d)
    # Also add one that's further away
    dists.append(correct + random.choice([10, 20, -10, -20]) + random.randint(1, 3))
    dists = [d for d in dists if d > 0 and d != correct][:3]
    while len(dists) < 3:
        dists.append(correct + random.randint(11, 99))
    dists = list(set(dists) - {correct})[:3]
    qid += 1
    questions.append({
        "id": qid,
        **COMMON_FIELDS,
        "difficulty": "Hard",
        "question": f"What is {a:,} + {b:,}?",
        "choices": _shuffle_choices(f"{correct:,}", [f"{d:,}" for d in dists]),
        "answer": f"{correct:,}",
        "explanation": (
            f"{a:,} + {b:,} = {correct:,}. "
            f"Quick check: last digits {a % 10} + {b % 10} = {(a % 10 + b % 10)}, "
            f"so the answer must end in {last_digit}."
        ),
        "tags": ["mental math", "addition", "last digit", "verification"],
    })

hard_count = len([q for q in questions if q["difficulty"] == "Hard"])
assert hard_count == 200, f"Expected 200 hard, got {hard_count}"

# ============================================================
# FINAL VALIDATION AND OUTPUT
# ============================================================

# Validate totals
total = len(questions)
assert total == 600, f"Expected 600 questions, got {total}"

easy = len([q for q in questions if q["difficulty"] == "Easy"])
medium = len([q for q in questions if q["difficulty"] == "Medium"])
hard = len([q for q in questions if q["difficulty"] == "Hard"])
assert easy == 200, f"Easy: {easy}"
assert medium == 200, f"Medium: {medium}"
assert hard == 200, f"Hard: {hard}"

# Validate all required fields
required_fields = {"id", "subtest", "module", "subtopic", "difficulty",
                   "question", "choices", "answer", "explanation", "tags",
                   "category", "language"}
for q in questions:
    missing = required_fields - set(q.keys())
    assert not missing, f"Question {q['id']} missing fields: {missing}"
    assert len(q["choices"]) == 4, f"Question {q['id']} has {len(q['choices'])} choices"
    assert q["answer"] in q["choices"], (
        f"Question {q['id']}: answer '{q['answer']}' not in choices {q['choices']}"
    )

# Re-number IDs sequentially
for i, q in enumerate(questions, 1):
    q["id"] = i

# Write output
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {total} questions ({easy} Easy, {medium} Medium, {hard} Hard)")
print(f"   Output: {OUTPUT_PATH}")
