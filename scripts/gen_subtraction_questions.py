"""
Generate 600 subtraction questions for the CSE Numerical Ability question bank.
200 Easy / 200 Medium / 200 Hard
"""
import json
import random
import math
from fractions import Fraction

random.seed(42)

questions = []
qid = 0

def make_q(difficulty, question, choices, answer, explanation, tags):
    global qid
    qid += 1
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Basic Operations",
        "subtopic": "Subtraction",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English"
    }

def shuffle_choices(correct, distractors):
    """Return shuffled choices list and the correct answer string."""
    all_c = [correct] + distractors
    random.shuffle(all_c)
    return all_c, correct

def fmt_num(n):
    """Format number with commas for display."""
    if isinstance(n, float):
        return f"{n:,.2f}"
    return f"{n:,}"

# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Whole number subtraction, no borrowing (40 questions) ---
for i in range(40):
    # Generate numbers where each digit of minuend >= corresponding digit of subtrahend
    if i < 20:
        # 2-digit
        a_tens = random.randint(3, 9)
        a_ones = random.randint(3, 9)
        b_tens = random.randint(1, a_tens - 1)
        b_ones = random.randint(0, a_ones)
        a = a_tens * 10 + a_ones
        b = b_tens * 10 + b_ones
    else:
        # 3-digit
        a_h = random.randint(4, 9)
        a_t = random.randint(3, 9)
        a_o = random.randint(2, 9)
        b_h = random.randint(1, a_h - 1)
        b_t = random.randint(0, a_t)
        b_o = random.randint(0, a_o)
        a = a_h * 100 + a_t * 10 + a_o
        b = b_h * 100 + b_t * 10 + b_o
    
    correct = a - b
    d1 = correct + random.choice([10, -10, 1, -1])
    d2 = correct + random.choice([11, -11, 2, -2])
    d3 = correct + random.choice([20, -20, 9, -9])
    distractors = [str(d1), str(d2), str(d3)]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Easy",
        f"What is {a} − {b}?",
        choices, ans,
        f"Subtract directly: {a} − {b} = {correct}. No borrowing is needed since each digit of the minuend is greater than or equal to the corresponding digit of the subtrahend.",
        ["subtraction", "whole numbers", "no borrowing"]
    ))

# --- Easy: Whole number subtraction with simple borrowing (40 questions) ---
for i in range(40):
    if i < 20:
        a = random.randint(50, 99)
        b = random.randint(10, a - 1)
    else:
        a = random.randint(200, 999)
        b = random.randint(100, a - 1)
    
    correct = a - b
    d1 = correct + random.choice([10, -10])
    d2 = correct + random.choice([1, -1, 100, -100])
    d3 = correct + random.choice([11, -11, 9, -9])
    # Ensure no duplicates and no negatives
    dists = set()
    for d in [d1, d2, d3]:
        if d != correct and d > 0:
            dists.add(str(d))
    while len(dists) < 3:
        dists.add(str(correct + random.randint(1, 20)))
    distractors = list(dists)[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Easy",
        f"What is {a} − {b}?",
        choices, ans,
        f"Subtract with borrowing as needed: {a} − {b} = {correct}.",
        ["subtraction", "whole numbers", "borrowing"]
    ))

# --- Easy: Subtraction from round numbers (20 questions) ---
for i in range(20):
    bases = [100, 200, 500, 1000]
    a = random.choice(bases)
    b = random.randint(1, a - 1)
    correct = a - b
    d1 = correct + random.choice([1, -1])
    d2 = correct + random.choice([10, -10])
    d3 = correct + random.choice([100, -100]) if a >= 500 else correct + random.choice([5, -5])
    dists = set()
    for d in [d1, d2, d3]:
        if d != correct and d > 0:
            dists.add(str(d))
    while len(dists) < 3:
        dists.add(str(correct + random.randint(2, 15)))
    distractors = list(dists)[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Easy",
        f"What is {fmt_num(a)} − {b}?",
        choices, ans,
        f"Subtract from a round number: {fmt_num(a)} − {b} = {correct}.",
        ["subtraction", "whole numbers", "round numbers"]
    ))

# --- Easy: Simple decimal subtraction (30 questions) ---
for i in range(30):
    if i < 15:
        # tenths
        a = round(random.uniform(5.0, 20.0), 1)
        b = round(random.uniform(1.0, a - 0.1), 1)
    else:
        # hundredths
        a = round(random.uniform(10.0, 100.0), 2)
        b = round(random.uniform(1.0, a - 0.01), 2)
    
    correct = round(a - b, 2)
    if i < 15:
        correct_str = f"{correct:.1f}"
    else:
        correct_str = f"{correct:.2f}"
    
    dists = set()
    # Generate unique distractors
    offsets = [0.1, -0.1, 0.2, -0.2, 0.3, -0.3, 0.5, -0.5, 1.0, -1.0, 1.5, -1.5, 2.0, -2.0]
    random.shuffle(offsets)
    for offset in offsets:
        d = round(correct + offset, 2)
        if d != correct and d > 0:
            ds = f"{d:.1f}" if i < 15 else f"{d:.2f}"
            if ds != correct_str:
                dists.add(ds)
        if len(dists) >= 5:
            break
    
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = round(correct + random.uniform(0.5, 3.0) * random.choice([1, -1]), 2)
        if d > 0:
            ds = f"{d:.1f}" if i < 15 else f"{d:.2f}"
            if ds != correct_str and ds not in distractors:
                distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Easy",
        f"What is {f'{a:.1f}' if i < 15 else f'{a:.2f}'} − {f'{b:.1f}' if i < 15 else f'{b:.2f}'}?",
        choices, ans,
        f"Align decimal points and subtract: {f'{a:.1f}' if i < 15 else f'{a:.2f}'} − {f'{b:.1f}' if i < 15 else f'{b:.2f}'} = {correct_str}.",
        ["subtraction", "decimals", "basic"]
    ))

# --- Easy: Simple fraction subtraction with like denominators (20 questions) ---
for i in range(20):
    denom = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    num_a = random.randint(max(2, denom // 2 + 1), denom - 1)
    num_b = random.randint(1, num_a - 1)
    
    result = Fraction(num_a - num_b, denom)
    correct_str = str(result)
    
    # Generate distractors
    dists = set()
    dists.add(str(Fraction(num_a + num_b, denom)))  # common mistake: adding
    dists.add(str(Fraction(num_a - num_b, denom * 2)))  # wrong denom
    dists.add(str(Fraction(num_a, denom)))  # forgot to subtract
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        fake_num = random.randint(1, denom - 1)
        fake = str(Fraction(fake_num, denom))
        if fake != correct_str and fake not in distractors:
            distractors.append(fake)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Easy",
        f"What is {num_a}/{denom} − {num_b}/{denom}?",
        choices, ans,
        f"With like denominators, subtract the numerators: {num_a}/{denom} − {num_b}/{denom} = {num_a - num_b}/{denom} = {correct_str}.",
        ["subtraction", "fractions", "like denominators"]
    ))

# --- Easy: Simple integer subtraction (30 questions) ---
for i in range(30):
    if i < 10:
        # positive - positive (result positive)
        a = random.randint(10, 50)
        b = random.randint(1, a - 1)
        correct = a - b
        q_text = f"What is {a} − {b}?"
        exp = f"Simple subtraction: {a} − {b} = {correct}."
    elif i < 20:
        # positive - negative (subtract negative = add)
        a = random.randint(5, 30)
        b = random.randint(1, 20)
        correct = a + b
        q_text = f"What is {a} − (−{b})?"
        exp = f"Subtracting a negative is adding: {a} − (−{b}) = {a} + {b} = {correct}."
    else:
        # negative - negative (simple cases)
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        correct = -a - (-b)  # = -a + b = b - a
        correct = b - a
        q_text = f"What is (−{a}) − (−{b})?"
        exp = f"Apply KCC: (−{a}) − (−{b}) = (−{a}) + {b} = {b - a}."
    
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 2, -2, 5, -5, 10, -10])
        if d != correct:
            dists.add(str(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(-15, 15)
        if d != correct and str(d) not in distractors:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Easy",
        q_text,
        choices, ans,
        exp,
        ["subtraction", "integers", "basic"]
    ))

# --- Easy: Simple word problems (20 questions) ---
easy_word_problems = [
    ("A store had {a} items in stock. After selling {b} items, how many remain?",
     "remaining stock", ["subtraction", "whole numbers", "word problem", "inventory"]),
    ("Maria has ₱{a}. She spent ₱{b} on supplies. How much money does she have left?",
     "remaining money", ["subtraction", "whole numbers", "word problem", "money"]),
    ("A class has {a} students. If {b} students are absent, how many are present?",
     "students present", ["subtraction", "whole numbers", "word problem", "attendance"]),
    ("A tank contains {a} liters of water. After using {b} liters, how many liters remain?",
     "remaining water", ["subtraction", "whole numbers", "word problem", "measurement"]),
    ("An office has {a} reams of paper. After distributing {b} reams, how many are left?",
     "remaining paper", ["subtraction", "whole numbers", "word problem", "inventory"]),
]

for i in range(20):
    template, context, tags = easy_word_problems[i % len(easy_word_problems)]
    a = random.randint(50, 500)
    b = random.randint(10, a - 5)
    correct = a - b
    q_text = template.format(a=a, b=b)
    
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 5, -5, 10, -10])
        if d != correct and d > 0:
            dists.add(str(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(1, 20)
        if str(d) not in distractors and d != correct:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Easy",
        q_text,
        choices, ans,
        f"Subtract to find the {context}: {a} − {b} = {correct}.",
        tags
    ))

# --- Easy: Estimation questions (20 questions) ---
for i in range(20):
    a = random.randint(100, 999)
    b = random.randint(50, a - 10)
    correct = a - b
    
    # Round to nearest 10 for estimation
    est_a = round(a, -1)
    est_b = round(b, -1)
    estimate = est_a - est_b
    
    q_text = f"Estimate the difference: {a} − {b} (round to the nearest ten before subtracting)."
    
    dists = set()
    dists.add(str(estimate + 10))
    dists.add(str(estimate - 10))
    dists.add(str(estimate + 20))
    dists.discard(str(estimate))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = estimate + random.choice([30, -30, 50])
        if str(d) != str(estimate) and str(d) not in distractors and d > 0:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(estimate), distractors)
    
    questions.append(make_q(
        "Easy",
        q_text,
        choices, ans,
        f"Round {a} to {est_a} and {b} to {est_b}. Then subtract: {est_a} − {est_b} = {estimate}.",
        ["subtraction", "estimation", "rounding"]
    ))

# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Multi-digit subtraction with multiple borrows (30 questions) ---
for i in range(30):
    if i < 15:
        a = random.randint(1000, 9999)
        b = random.randint(100, a - 1)
    else:
        a = random.randint(10000, 99999)
        b = random.randint(1000, a - 1)
    
    correct = a - b
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 10, -10, 100, -100, 11, -11])
        if d != correct and d > 0:
            dists.add(fmt_num(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(1, 200)
        ds = fmt_num(d)
        if ds != fmt_num(correct) and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(fmt_num(correct), distractors)
    
    questions.append(make_q(
        "Medium",
        f"What is {fmt_num(a)} − {fmt_num(b)}?",
        choices, ans,
        f"Subtract with careful borrowing: {fmt_num(a)} − {fmt_num(b)} = {fmt_num(correct)}.",
        ["subtraction", "whole numbers", "multiple borrowing"]
    ))

# --- Medium: Borrowing across zeros (20 questions) ---
for i in range(20):
    # Numbers with zeros that require cascading borrows
    bases = [1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 50000, 100000]
    if i < 10:
        a = random.choice([1000, 2000, 3000, 5000])
        b = random.randint(100, a - 1)
    else:
        a = random.choice([10000, 20000, 50000, 100000])
        b = random.randint(1000, a - 1)
    
    correct = a - b
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 10, -10, 100, -100])
        if d != correct and d > 0:
            dists.add(fmt_num(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(2, 50)
        ds = fmt_num(d)
        if ds != fmt_num(correct) and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(fmt_num(correct), distractors)
    
    questions.append(make_q(
        "Medium",
        f"What is {fmt_num(a)} − {fmt_num(b)}?",
        choices, ans,
        f"Borrowing across zeros: {fmt_num(a)} − {fmt_num(b)} = {fmt_num(correct)}. Use the cascade method or subtract each digit from 9 (last from 10) for the borrowed portion.",
        ["subtraction", "whole numbers", "borrowing across zeros"]
    ))

# --- Medium: Integer subtraction (30 questions) ---
for i in range(30):
    if i < 10:
        # negative - positive
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        correct = -a - b
        q_text = f"What is (−{a}) − {b}?"
        exp = f"Apply KCC: (−{a}) − {b} = (−{a}) + (−{b}) = −({a} + {b}) = {correct}."
    elif i < 20:
        # positive - larger positive (negative result)
        b = random.randint(20, 80)
        a = random.randint(1, b - 1)
        correct = a - b
        q_text = f"What is {a} − {b}?"
        exp = f"Since {a} < {b}, the result is negative: {a} − {b} = {correct}."
    else:
        # negative - negative (various magnitudes)
        a = random.randint(10, 60)
        b = random.randint(10, 60)
        correct = -a - (-b)  # = -a + b = b - a
        q_text = f"What is (−{a}) − (−{b})?"
        exp = f"Apply KCC: (−{a}) − (−{b}) = (−{a}) + {b} = {b - a}."
    
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 2, -2, 5, -5, 10, -10])
        if d != correct:
            dists.add(str(d))
    # Add common mistake: wrong sign
    dists.add(str(-correct))
    dists.discard(str(correct))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(-20, 20)
        if d != correct and str(d) not in distractors:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Medium",
        q_text,
        choices, ans,
        exp,
        ["subtraction", "integers", "sign rules"]
    ))

# --- Medium: Decimal subtraction with borrowing (30 questions) ---
for i in range(30):
    if i < 15:
        a = round(random.uniform(20.0, 200.0), 2)
        b = round(random.uniform(5.0, a - 0.5), 2)
    else:
        a = round(random.uniform(100.0, 5000.0), 2)
        b = round(random.uniform(10.0, a - 1.0), 2)
    
    correct = round(a - b, 2)
    correct_str = f"{correct:.2f}"
    
    dists = set()
    for _ in range(10):
        offset = round(random.choice([0.01, -0.01, 0.1, -0.1, 1.0, -1.0, 0.11, -0.11]), 2)
        d = round(correct + offset, 2)
        if d != correct and d > 0:
            dists.add(f"{d:.2f}")
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = round(correct + random.uniform(0.5, 3.0), 2)
        ds = f"{d:.2f}"
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Medium",
        f"What is {a:.2f} − {b:.2f}?",
        choices, ans,
        f"Align decimal points and subtract with borrowing: {a:.2f} − {b:.2f} = {correct_str}.",
        ["subtraction", "decimals", "borrowing"]
    ))

# --- Medium: Fraction subtraction with unlike denominators (30 questions) ---
for i in range(30):
    denoms = [(3, 4), (4, 5), (5, 6), (3, 5), (4, 7), (5, 8), (6, 7),
              (3, 8), (4, 9), (5, 9), (7, 8), (3, 7), (3, 5), (5, 12),
              (4, 6), (3, 10), (7, 10), (8, 9), (6, 8), (7, 12),
              (3, 4), (5, 7), (4, 11), (6, 11), (7, 9), (8, 11),
              (9, 10), (4, 7), (3, 11), (4, 5)]
    d1, d2 = denoms[i]
    
    # Ensure a/d1 > b/d2
    num_a = random.randint(max(2, d1 // 2 + 1), d1 - 1)
    num_b = random.randint(1, d2 - 1)
    
    frac_a = Fraction(num_a, d1)
    frac_b = Fraction(num_b, d2)
    
    if frac_a <= frac_b:
        num_a = d1 - 1
        frac_a = Fraction(num_a, d1)
    
    if frac_a <= frac_b:
        num_b = 1
        frac_b = Fraction(num_b, d2)
    
    result = frac_a - frac_b
    correct_str = str(result)
    
    dists = set()
    # Common mistakes
    dists.add(str(frac_a + frac_b))  # added instead
    dists.add(str(Fraction(num_a - num_b, d1 * d2)))  # wrong approach
    dists.add(str(Fraction(abs(num_a - num_b), max(1, abs(d1 - d2))) if d1 != d2 else Fraction(1, 2)))
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        fake = Fraction(random.randint(1, 20), random.randint(2, 24))
        fs = str(fake)
        if fs != correct_str and fs not in distractors:
            distractors.append(fs)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    lcd = (d1 * d2) // math.gcd(d1, d2)
    questions.append(make_q(
        "Medium",
        f"What is {num_a}/{d1} − {num_b}/{d2}?",
        choices, ans,
        f"Find LCD of {d1} and {d2} = {lcd}. Convert: {num_a}/{d1} = {num_a * (lcd // d1)}/{lcd}, {num_b}/{d2} = {num_b * (lcd // d2)}/{lcd}. Subtract numerators: {num_a * (lcd // d1)} − {num_b * (lcd // d2)} = {num_a * (lcd // d1) - num_b * (lcd // d2)}. Result: {correct_str}.",
        ["subtraction", "fractions", "unlike denominators"]
    ))

# --- Medium: Mixed number subtraction (20 questions) ---
for i in range(20):
    # Generate mixed numbers where subtraction requires borrowing from whole
    w1 = random.randint(4, 12)
    w2 = random.randint(1, w1 - 1)
    d = random.choice([3, 4, 5, 6, 8, 10, 12])
    n1 = random.randint(1, d - 1)
    n2 = random.randint(1, d - 1)
    
    frac1 = Fraction(w1 * d + n1, d)
    frac2 = Fraction(w2 * d + n2, d)
    
    if frac1 <= frac2:
        w1, w2 = w2 + 2, w2
        frac1 = Fraction(w1 * d + n1, d)
        frac2 = Fraction(w2 * d + n2, d)
    
    result = frac1 - frac2
    whole_part = int(result)
    frac_part = result - whole_part
    
    if frac_part == 0:
        correct_str = str(whole_part)
    else:
        correct_str = f"{whole_part} {frac_part}" if whole_part > 0 else str(result)
    # Use fraction format
    correct_str = str(result)
    # Convert to mixed number string
    if result >= 1:
        w = int(result)
        f_part = result - w
        if f_part == 0:
            correct_str = str(w)
        else:
            correct_str = f"{w} {f_part}"
    else:
        correct_str = str(result)
    
    dists = set()
    for offset in [Fraction(1, d), Fraction(-1, d), Fraction(1, 1), Fraction(-1, 1)]:
        fake = result + offset
        if fake > 0 and fake != result:
            if fake >= 1:
                fw = int(fake)
                ff = fake - fw
                if ff == 0:
                    dists.add(str(fw))
                else:
                    dists.add(f"{fw} {ff}")
            else:
                dists.add(str(fake))
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        fake_w = random.randint(1, w1)
        fake_n = random.randint(1, d - 1)
        fs = f"{fake_w} {Fraction(fake_n, d)}"
        if fs != correct_str and fs not in distractors:
            distractors.append(fs)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    # Format question
    q_text = f"What is {w1} {Fraction(n1, d)} − {w2} {Fraction(n2, d)}?"
    
    questions.append(make_q(
        "Medium",
        q_text,
        choices, ans,
        f"Subtract the mixed numbers: {w1} {Fraction(n1, d)} − {w2} {Fraction(n2, d)} = {correct_str}. {'Borrowing from the whole number was needed.' if Fraction(n1, d) < Fraction(n2, d) else 'Subtract whole parts and fraction parts separately.'}",
        ["subtraction", "fractions", "mixed numbers"]
    ))

# --- Medium: Word problems - money/payroll (20 questions) ---
medium_money_templates = [
    "An employee's gross salary is ₱{a:.2f}. If total deductions amount to ₱{b:.2f}, what is the net pay?",
    "A customer pays ₱{a:.2f} for a purchase of ₱{b:.2f}. How much change should be given?",
    "A department's budget allocation is ₱{a:.2f}. If ₱{b:.2f} has been spent, how much remains?",
    "The petty cash fund has ₱{a:.2f}. After a disbursement of ₱{b:.2f}, what is the remaining balance?",
    "An office supply budget of ₱{a:.2f} was reduced by ₱{b:.2f} due to cost-cutting. What is the new budget?",
]

for i in range(20):
    template = medium_money_templates[i % len(medium_money_templates)]
    a = round(random.uniform(5000, 50000), 2)
    b = round(random.uniform(500, a - 100), 2)
    correct = round(a - b, 2)
    correct_str = f"₱{correct:,.2f}"
    
    dists = set()
    for offset in [0.25, -0.25, 10, -10, 100, -100]:
        d = round(correct + offset, 2)
        if d != correct and d > 0:
            dists.add(f"₱{d:,.2f}")
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = round(correct + random.uniform(1, 500), 2)
        ds = f"₱{d:,.2f}"
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Medium",
        template.format(a=a, b=b),
        choices, ans,
        f"Subtract: ₱{a:,.2f} − ₱{b:,.2f} = {correct_str}.",
        ["subtraction", "decimals", "word problem", "money"]
    ))

# --- Medium: Word problems - measurement/inventory (20 questions) ---
medium_measure_templates = [
    "A water tank holds {a} liters. After {b} liters were consumed, how many liters remain?",
    "A warehouse had {a} units of product. After shipping {b} units, how many units are left?",
    "A road is {a:.3f} km long. If {b:.3f} km has been paved, how many km remain unpaved?",
    "A government office had {a} employees in January. By December, {b} had resigned. How many remain?",
    "A school received {a} textbooks. After distributing {b} to students, how many are in storage?",
]

for i in range(20):
    template = medium_measure_templates[i % len(medium_measure_templates)]
    if "km" in template:
        a = round(random.uniform(5, 50), 3)
        b = round(random.uniform(1, a - 0.5), 3)
        correct = round(a - b, 3)
        correct_str = f"{correct:.3f} km"
        dists = set()
        for offset in [0.001, -0.001, 0.01, -0.01, 0.1, -0.1]:
            d = round(correct + offset, 3)
            if d != correct and d > 0:
                dists.add(f"{d:.3f} km")
    else:
        a = random.randint(500, 10000)
        b = random.randint(50, a - 10)
        correct = a - b
        correct_str = fmt_num(correct)
        dists = set()
        for offset in [1, -1, 10, -10, 100, -100]:
            d = correct + offset
            if d != correct and d > 0:
                dists.add(fmt_num(d))
    
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if "km" in template:
            d = round(correct + random.uniform(0.1, 2), 3)
            ds = f"{d:.3f} km"
        else:
            d = correct + random.randint(2, 50)
            ds = fmt_num(d)
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Medium",
        template.format(a=a, b=b),
        choices, ans,
        f"Subtract to find the remaining amount: {correct_str}.",
        ["subtraction", "word problem", "measurement"]
    ))

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Large number subtraction with complex borrowing (30 questions) ---
for i in range(30):
    if i < 15:
        a = random.randint(100000, 999999)
        b = random.randint(10000, a - 1)
    else:
        a = random.randint(1000000, 9999999)
        b = random.randint(100000, a - 1)
    
    correct = a - b
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 10, -10, 100, -100, 1000, -1000])
        if d != correct and d > 0:
            dists.add(fmt_num(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(1, 5000)
        ds = fmt_num(d)
        if ds != fmt_num(correct) and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(fmt_num(correct), distractors)
    
    questions.append(make_q(
        "Hard",
        f"What is {fmt_num(a)} − {fmt_num(b)}?",
        choices, ans,
        f"Carefully subtract with multiple regroupings: {fmt_num(a)} − {fmt_num(b)} = {fmt_num(correct)}.",
        ["subtraction", "whole numbers", "large numbers"]
    ))

# --- Hard: Complex integer subtraction (30 questions) ---
for i in range(30):
    if i < 10:
        # Multiple integer operations
        a = random.randint(-50, 50)
        b = random.randint(-50, 50)
        c = random.randint(-50, 50)
        correct = a - b - c
        q_text = f"What is ({a}) − ({b}) − ({c})?"
        exp = f"Step by step: ({a}) − ({b}) = {a - b}. Then {a - b} − ({c}) = {a - b - c} = {correct}."
    elif i < 20:
        # Large integers
        a = random.randint(-200, 200)
        b = random.randint(-200, 200)
        correct = a - b
        if a >= 0 and b >= 0:
            q_text = f"What is {a} − {b}?"
        elif a >= 0 and b < 0:
            q_text = f"What is {a} − ({b})?"
        elif a < 0 and b >= 0:
            q_text = f"What is ({a}) − {b}?"
        else:
            q_text = f"What is ({a}) − ({b})?"
        exp = f"Apply KCC: ({a}) − ({b}) = ({a}) + ({-b}) = {correct}."
    else:
        # Temperature/elevation style
        scenarios = [
            ("The temperature dropped from {a}°C to {b}°C. What is the change in temperature?", "temperature"),
            ("A submarine is at {a} meters depth. It ascends {b} meters. What is its new depth?", "depth"),
        ]
        if i % 2 == 0:
            a_val = random.randint(-20, 40)
            b_val = random.randint(-30, a_val - 1)
            correct = b_val - a_val
            q_text = f"The temperature dropped from {a_val}°C to {b_val}°C. What is the change in temperature?"
            exp = f"Change = final − initial = {b_val} − {a_val} = {correct}°C."
        else:
            depth = -random.randint(50, 300)
            ascent = random.randint(10, abs(depth) - 5)
            correct = depth + ascent
            q_text = f"A submarine is at {depth} meters. It ascends {ascent} meters. What is its new position?"
            exp = f"New position = {depth} + {ascent} = {correct} meters."
    
    dists = set()
    dists.add(str(-correct))  # wrong sign
    for _ in range(10):
        d = correct + random.choice([1, -1, 2, -2, 5, -5, 10, -10])
        if d != correct:
            dists.add(str(d))
    dists.discard(str(correct))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(-30, 30)
        if d != correct and str(d) not in distractors:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    
    questions.append(make_q(
        "Hard",
        q_text,
        choices, ans,
        exp,
        ["subtraction", "integers", "complex"]
    ))

# --- Hard: Complex decimal subtraction (30 questions) ---
for i in range(30):
    if i < 10:
        # Thousandths
        a = round(random.uniform(50, 500), 3)
        b = round(random.uniform(10, a - 1), 3)
        correct = round(a - b, 3)
        correct_str = f"{correct:.3f}"
        a_str = f"{a:.3f}"
        b_str = f"{b:.3f}"
    elif i < 20:
        # Large money amounts
        a = round(random.uniform(10000, 100000), 2)
        b = round(random.uniform(1000, a - 100), 2)
        correct = round(a - b, 2)
        correct_str = f"{correct:,.2f}"
        a_str = f"{a:,.2f}"
        b_str = f"{b:,.2f}"
    else:
        # Multi-step: subtract two decimals from a total
        total = round(random.uniform(1000, 5000), 2)
        sub1 = round(random.uniform(100, total / 3), 2)
        sub2 = round(random.uniform(100, total / 3), 2)
        correct = round(total - sub1 - sub2, 2)
        correct_str = f"{correct:,.2f}"
        a_str = f"{total:,.2f}"
        b_str = f"{sub1:,.2f} and {sub2:,.2f}"
        a = total
        b = sub1 + sub2
    
    dists = set()
    for _ in range(10):
        if i < 10:
            offset = round(random.choice([0.001, -0.001, 0.01, -0.01, 0.1, -0.1]), 3)
            d = round(correct + offset, 3)
            if d != correct and d > 0:
                dists.add(f"{d:.3f}")
        else:
            offset = round(random.choice([0.01, -0.01, 0.1, -0.1, 1, -1, 10, -10]), 2)
            d = round(correct + offset, 2)
            if d != correct and d > 0:
                dists.add(f"{d:,.2f}")
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if i < 10:
            d = round(correct + random.uniform(0.01, 1), 3)
            ds = f"{d:.3f}"
        else:
            d = round(correct + random.uniform(1, 100), 2)
            ds = f"{d:,.2f}"
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    if i >= 20:
        q_text = f"From a total of ₱{a_str}, deductions of ₱{sub1:,.2f} and ₱{sub2:,.2f} were made. What is the remaining amount?"
    else:
        q_text = f"What is {a_str} − {b_str}?"
    
    questions.append(make_q(
        "Hard",
        q_text,
        choices, ans,
        f"Subtract carefully with decimal alignment: {correct_str}.",
        ["subtraction", "decimals", "complex"]
    ))

# --- Hard: Complex fraction subtraction (30 questions) ---
for i in range(30):
    if i < 15:
        # Unlike denominators with larger numbers
        d1 = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 15])
        d2 = random.choice([x for x in [3, 4, 5, 6, 7, 8, 9, 10, 12, 15] if x != d1])
        num_a = random.randint(max(2, d1 // 2 + 1), d1 - 1)
        num_b = random.randint(1, d2 - 1)
        
        frac_a = Fraction(num_a, d1)
        frac_b = Fraction(num_b, d2)
        
        if frac_a <= frac_b:
            num_a = d1 - 1
            frac_a = Fraction(num_a, d1)
        if frac_a <= frac_b:
            num_b = 1
            frac_b = Fraction(num_b, d2)
        
        result = frac_a - frac_b
        correct_str = str(result)
        q_text = f"What is {num_a}/{d1} − {num_b}/{d2}?"
        lcd = (d1 * d2) // math.gcd(d1, d2)
        exp = f"LCD of {d1} and {d2} = {lcd}. Convert and subtract: {correct_str}."
    else:
        # Mixed numbers with unlike denominators
        w1 = random.randint(5, 15)
        w2 = random.randint(1, w1 - 1)
        d1 = random.choice([3, 4, 5, 6, 8])
        d2 = random.choice([x for x in [3, 4, 5, 6, 8] if x != d1])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        
        frac1 = Fraction(w1 * d1 + n1, d1)
        frac2 = Fraction(w2 * d2 + n2, d2)
        
        if frac1 <= frac2:
            w1 = w2 + 3
            frac1 = Fraction(w1 * d1 + n1, d1)
        
        result = frac1 - frac2
        # Format as mixed number
        w_res = int(result)
        f_res = result - w_res
        if f_res == 0:
            correct_str = str(w_res)
        else:
            correct_str = f"{w_res} {f_res}"
        
        q_text = f"What is {w1} {n1}/{d1} − {w2} {n2}/{d2}?"
        exp = f"Convert to improper fractions, find LCD, subtract, and convert back: {correct_str}."
    
    dists = set()
    for offset in [Fraction(1, 12), Fraction(-1, 12), Fraction(1, 6), Fraction(-1, 6), Fraction(1, 1)]:
        fake = result + offset
        if fake > 0 and fake != result:
            if fake >= 1 and i >= 15:
                fw = int(fake)
                ff = fake - fw
                if ff == 0:
                    dists.add(str(fw))
                else:
                    dists.add(f"{fw} {ff}")
            else:
                dists.add(str(fake))
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if i < 15:
            fake = Fraction(random.randint(1, 20), random.randint(2, 30))
            fs = str(fake)
        else:
            fw = random.randint(1, w1)
            ff = Fraction(random.randint(1, 11), 12)
            fs = f"{fw} {ff}"
        if fs != correct_str and fs not in distractors:
            distractors.append(fs)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Hard",
        q_text,
        choices, ans,
        exp,
        ["subtraction", "fractions", "complex"]
    ))

# --- Hard: Multi-step word problems (40 questions) ---
hard_word_templates = [
    {
        "template": "A government agency has an annual budget of ₱{total:,.2f}. In Q1, ₱{q1:,.2f} was spent; in Q2, ₱{q2:,.2f} was spent; in Q3, ₱{q3:,.2f} was spent. How much budget remains for Q4?",
        "tags": ["subtraction", "word problem", "budget", "multi-step"],
    },
    {
        "template": "An employee earns ₱{gross:,.2f} monthly. Deductions include: income tax ₱{tax:,.2f}, PhilHealth ₱{ph:,.2f}, Pag-IBIG ₱{pi:,.2f}, and GSIS ₱{gsis:,.2f}. What is the net take-home pay?",
        "tags": ["subtraction", "word problem", "payroll", "multi-step"],
    },
    {
        "template": "A warehouse received {recv:,} units of supplies. On Monday, {m:,} units were issued; on Wednesday, {w:,} units; and on Friday, {f:,} units. How many units remain?",
        "tags": ["subtraction", "word problem", "inventory", "multi-step"],
    },
    {
        "template": "A municipality's population was {pop:,} in 2020. Over three years, {y1:,} people migrated out, {y2:,} people died, and {y3:,} new residents moved in. What is the population in 2023?",
        "tags": ["subtraction", "addition", "word problem", "population"],
    },
    {
        "template": "A contractor was given ₱{total:,.2f} for a project. Materials cost ₱{mat:,.2f}, labor cost ₱{lab:,.2f}, and permits cost ₱{perm:,.2f}. How much profit did the contractor make?",
        "tags": ["subtraction", "word problem", "finance", "multi-step"],
    },
]

for i in range(40):
    t_idx = i % len(hard_word_templates)
    t = hard_word_templates[t_idx]
    
    if t_idx == 0:
        total = round(random.uniform(500000, 5000000), 2)
        q1 = round(random.uniform(total * 0.15, total * 0.3), 2)
        q2 = round(random.uniform(total * 0.15, total * 0.3), 2)
        q3 = round(random.uniform(total * 0.15, total * 0.3), 2)
        correct = round(total - q1 - q2 - q3, 2)
        q_text = t["template"].format(total=total, q1=q1, q2=q2, q3=q3)
        correct_str = f"₱{correct:,.2f}"
        exp = f"Total spent: ₱{q1 + q2 + q3:,.2f}. Remaining: ₱{total:,.2f} − ₱{q1 + q2 + q3:,.2f} = {correct_str}."
    elif t_idx == 1:
        gross = round(random.uniform(20000, 80000), 2)
        tax = round(gross * random.uniform(0.05, 0.15), 2)
        ph = round(random.uniform(200, 900), 2)
        pi = round(random.uniform(100, 400), 2)
        gsis = round(gross * random.uniform(0.05, 0.12), 2)
        correct = round(gross - tax - ph - pi - gsis, 2)
        q_text = t["template"].format(gross=gross, tax=tax, ph=ph, pi=pi, gsis=gsis)
        correct_str = f"₱{correct:,.2f}"
        exp = f"Total deductions: ₱{tax + ph + pi + gsis:,.2f}. Net pay: ₱{gross:,.2f} − ₱{tax + ph + pi + gsis:,.2f} = {correct_str}."
    elif t_idx == 2:
        recv = random.randint(5000, 50000)
        m = random.randint(500, recv // 4)
        w = random.randint(500, recv // 4)
        f_val = random.randint(500, recv // 4)
        correct = recv - m - w - f_val
        q_text = t["template"].format(recv=recv, m=m, w=w, f=f_val)
        correct_str = fmt_num(correct)
        exp = f"Total issued: {fmt_num(m + w + f_val)}. Remaining: {fmt_num(recv)} − {fmt_num(m + w + f_val)} = {correct_str}."
    elif t_idx == 3:
        pop = random.randint(50000, 500000)
        y1 = random.randint(1000, 10000)
        y2 = random.randint(500, 5000)
        y3 = random.randint(2000, 15000)
        correct = pop - y1 - y2 + y3
        q_text = t["template"].format(pop=pop, y1=y1, y2=y2, y3=y3)
        correct_str = fmt_num(correct)
        exp = f"Population = {fmt_num(pop)} − {fmt_num(y1)} − {fmt_num(y2)} + {fmt_num(y3)} = {correct_str}."
    else:
        total = round(random.uniform(100000, 2000000), 2)
        mat = round(total * random.uniform(0.2, 0.4), 2)
        lab = round(total * random.uniform(0.2, 0.35), 2)
        perm = round(total * random.uniform(0.02, 0.08), 2)
        correct = round(total - mat - lab - perm, 2)
        q_text = t["template"].format(total=total, mat=mat, lab=lab, perm=perm)
        correct_str = f"₱{correct:,.2f}"
        exp = f"Total expenses: ₱{mat + lab + perm:,.2f}. Profit: ₱{total:,.2f} − ₱{mat + lab + perm:,.2f} = {correct_str}."
    
    dists = set()
    if isinstance(correct, float):
        for offset in [0.01, -0.01, 10, -10, 100, -100, 1000, -1000]:
            d = round(correct + offset, 2)
            if d != correct and d > 0:
                if "₱" in correct_str:
                    dists.add(f"₱{d:,.2f}")
                else:
                    dists.add(fmt_num(d))
    else:
        for offset in [1, -1, 10, -10, 100, -100, 1000, -1000]:
            d = correct + offset
            if d != correct and d > 0:
                dists.add(fmt_num(d))
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if isinstance(correct, float):
            d = round(correct + random.uniform(50, 5000), 2)
            ds = f"₱{d:,.2f}" if "₱" in correct_str else f"{d:,.2f}"
        else:
            d = correct + random.randint(50, 5000)
            ds = fmt_num(d)
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q(
        "Hard",
        q_text,
        choices, ans,
        exp,
        t["tags"]
    ))

# --- Hard: Conceptual and tricky questions (40 questions) ---
# These test understanding of subtraction properties and common traps

conceptual_questions = []

# Subtraction properties
conceptual_questions.append(make_q(
    "Hard",
    "Which of the following statements about subtraction is TRUE?",
    ["Subtraction is commutative", "Subtraction is associative", 
     "Subtracting zero from a number gives the same number", "Subtraction is distributive over addition"],
    "Subtracting zero from a number gives the same number",
    "a − 0 = a is the identity property of subtraction. Subtraction is neither commutative (a − b ≠ b − a) nor associative ((a − b) − c ≠ a − (b − c)).",
    ["subtraction", "properties", "conceptual"]
))

conceptual_questions.append(make_q(
    "Hard",
    "If a − b = 15 and a + b = 45, what is the value of a?",
    ["15", "25", "30", "35"],
    "30",
    "Add the two equations: (a − b) + (a + b) = 15 + 45 → 2a = 60 → a = 30.",
    ["subtraction", "algebra", "system of equations"]
))

conceptual_questions.append(make_q(
    "Hard",
    "If a − b = 15 and a + b = 45, what is the value of b?",
    ["10", "15", "20", "25"],
    "15",
    "From a = 30 (found by adding equations), substitute: 30 + b = 45 → b = 15.",
    ["subtraction", "algebra", "system of equations"]
))

conceptual_questions.append(make_q(
    "Hard",
    "What is the result of 1,000,000 − 999,999?",
    ["0", "1", "10", "100"],
    "1",
    "1,000,000 − 999,999 = 1. The numbers differ by exactly 1.",
    ["subtraction", "whole numbers", "mental math"]
))

conceptual_questions.append(make_q(
    "Hard",
    "If x − (−5) = 12, what is x?",
    ["7", "17", "−7", "−17"],
    "7",
    "x − (−5) = x + 5 = 12. Therefore x = 12 − 5 = 7.",
    ["subtraction", "integers", "algebra"]
))

conceptual_questions.append(make_q(
    "Hard",
    "What is (−1) − (−2) − (−3) − (−4)?",
    ["8", "−8", "10", "−10"],
    "8",
    "Apply KCC to each: (−1) + 2 + 3 + 4 = −1 + 9 = 8.",
    ["subtraction", "integers", "multiple operations"]
))

conceptual_questions.append(make_q(
    "Hard",
    "A number decreased by 47 gives 128. What is the number?",
    ["81", "175", "165", "185"],
    "175",
    "Let n − 47 = 128. Then n = 128 + 47 = 175.",
    ["subtraction", "word problem", "algebra"]
))

conceptual_questions.append(make_q(
    "Hard",
    "What is 10,000 − 1 − 2 − 3 − 4 − 5 − 6 − 7 − 8 − 9 − 10?",
    ["9,935", "9,945", "9,940", "9,955"],
    "9,945",
    "Sum of 1 to 10 = 55. Therefore 10,000 − 55 = 9,945.",
    ["subtraction", "whole numbers", "series"]
))

conceptual_questions.append(make_q(
    "Hard",
    "If 3/4 − x = 1/6, what is x?",
    ["7/12", "5/12", "11/12", "1/12"],
    "7/12",
    "x = 3/4 − 1/6. LCD = 12. x = 9/12 − 2/12 = 7/12.",
    ["subtraction", "fractions", "algebra"]
))

conceptual_questions.append(make_q(
    "Hard",
    "What is the difference between the largest 4-digit number and the smallest 4-digit number?",
    ["8,999", "9,000", "9,999", "8,000"],
    "8,999",
    "Largest 4-digit = 9,999. Smallest 4-digit = 1,000. Difference = 9,999 − 1,000 = 8,999.",
    ["subtraction", "whole numbers", "number properties"]
))

for q in conceptual_questions:
    questions.append(q)

# More conceptual/tricky hard questions
conceptual_questions2 = []

conceptual_questions2.append(make_q(
    "Hard",
    "What is 5.000 − 0.005?",
    ["4.995", "4.095", "4.905", "4.950"],
    "4.995",
    "Align decimals: 5.000 − 0.005 = 4.995. Borrow through the zeros.",
    ["subtraction", "decimals", "borrowing"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "A government office's budget was ₱2,500,000. After spending 35% of it, how much remains?",
    ["₱1,625,000", "₱875,000", "₱1,750,000", "₱1,500,000"],
    "₱1,625,000",
    "35% of 2,500,000 = 875,000. Remaining = 2,500,000 − 875,000 = ₱1,625,000. Alternatively, 65% × 2,500,000 = 1,625,000.",
    ["subtraction", "percentage", "word problem", "budget"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "What is 1 − 1/2 − 1/4 − 1/8?",
    ["1/8", "1/4", "3/8", "1/16"],
    "1/8",
    "LCD = 8. 8/8 − 4/8 − 2/8 − 1/8 = 1/8.",
    ["subtraction", "fractions", "multiple operations"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "The minuend is 8,456 and the difference is 3,789. What is the subtrahend?",
    ["4,667", "12,245", "4,677", "4,657"],
    "4,667",
    "Subtrahend = Minuend − Difference = 8,456 − 3,789 = 4,667.",
    ["subtraction", "terminology", "inverse"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "What is (−100) − (−100)?",
    ["−200", "200", "0", "100"],
    "0",
    "(−100) − (−100) = (−100) + 100 = 0. Any number minus itself equals zero.",
    ["subtraction", "integers", "properties"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "If the sum of two numbers is 100 and their difference is 36, what is the larger number?",
    ["64", "68", "72", "82"],
    "68",
    "Let the numbers be a and b where a > b. a + b = 100 and a − b = 36. Adding: 2a = 136, so a = 68.",
    ["subtraction", "addition", "algebra", "system of equations"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "What is 99,999 − 88,888?",
    ["11,111", "11,011", "10,111", "11,101"],
    "11,111",
    "Subtract digit by digit: 9−8=1 in each position. 99,999 − 88,888 = 11,111.",
    ["subtraction", "whole numbers", "pattern"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "A tank is 3/4 full. After using 2/5 of the tank's capacity, what fraction of the tank still has water?",
    ["7/20", "1/4", "3/10", "2/5"],
    "7/20",
    "Remaining = 3/4 − 2/5. LCD = 20. 15/20 − 8/20 = 7/20.",
    ["subtraction", "fractions", "word problem"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "What is 2.5 − 1.75 − 0.25?",
    ["0.5", "0.75", "1.0", "0.25"],
    "0.5",
    "Step by step: 2.5 − 1.75 = 0.75. Then 0.75 − 0.25 = 0.5.",
    ["subtraction", "decimals", "multiple operations"]
))

conceptual_questions2.append(make_q(
    "Hard",
    "The temperature at noon was 32.5°C. By midnight, it dropped to 18.7°C. What was the temperature decrease?",
    ["13.8°C", "14.2°C", "13.2°C", "51.2°C"],
    "13.8°C",
    "Decrease = 32.5 − 18.7 = 13.8°C.",
    ["subtraction", "decimals", "word problem", "temperature"]
))

for q in conceptual_questions2:
    questions.append(q)

# More hard conceptual questions to reach 40 total
more_conceptual = []

more_conceptual.append(make_q(
    "Hard",
    "What is 7 1/3 − 2 5/6?",
    ["4 1/2", "4 1/6", "5 1/6", "4 2/3"],
    "4 1/2",
    "Convert: 7 1/3 = 7 2/6. Since 2/6 < 5/6, borrow: 6 8/6 − 2 5/6 = 4 3/6 = 4 1/2.",
    ["subtraction", "fractions", "mixed numbers", "borrowing"]
))

more_conceptual.append(make_q(
    "Hard",
    "A rope is 15 3/4 meters long. If 8 7/8 meters is cut off, how long is the remaining piece?",
    ["6 7/8 meters", "7 1/8 meters", "7 7/8 meters", "6 1/8 meters"],
    "6 7/8 meters",
    "15 3/4 − 8 7/8. LCD = 8. 15 6/8 − 8 7/8. Borrow: 14 14/8 − 8 7/8 = 6 7/8 meters.",
    ["subtraction", "fractions", "mixed numbers", "word problem"]
))

more_conceptual.append(make_q(
    "Hard",
    "What is the value of 50,000 − 12,345 − 6,789?",
    ["30,866", "31,866", "30,966", "31,766"],
    "30,866",
    "50,000 − 12,345 = 37,655. Then 37,655 − 6,789 = 30,866.",
    ["subtraction", "whole numbers", "multi-step"]
))

more_conceptual.append(make_q(
    "Hard",
    "An employee worked 8.5 hours on Monday, 7.75 hours on Tuesday, and 9.25 hours on Wednesday. If the weekly requirement is 40 hours, how many more hours must be worked in the remaining 2 days?",
    ["14.5 hours", "15.5 hours", "14.0 hours", "15.0 hours"],
    "14.5 hours",
    "Hours worked: 8.5 + 7.75 + 9.25 = 25.5. Remaining: 40 − 25.5 = 14.5 hours.",
    ["subtraction", "addition", "decimals", "word problem"]
))

more_conceptual.append(make_q(
    "Hard",
    "What is (−45) − 23 − (−68)?",
    ["0", "−136", "68", "−68"],
    "0",
    "(−45) − 23 − (−68) = −45 − 23 + 68 = −68 + 68 = 0.",
    ["subtraction", "integers", "multiple operations"]
))

more_conceptual.append(make_q(
    "Hard",
    "A school has a budget of ₱1,500,000. Personnel costs are ₱875,000, MOOE is ₱412,500, and capital outlay is ₱156,250. What is the unallocated amount?",
    ["₱56,250", "₱156,250", "₱62,500", "₱46,250"],
    "₱56,250",
    "Total allocated: 875,000 + 412,500 + 156,250 = 1,443,750. Unallocated: 1,500,000 − 1,443,750 = ₱56,250.",
    ["subtraction", "addition", "word problem", "budget"]
))

more_conceptual.append(make_q(
    "Hard",
    "What is 3/5 − 1/4 − 1/10?",
    ["1/4", "3/20", "7/20", "1/5"],
    "1/4",
    "LCD = 20. 12/20 − 5/20 − 2/20 = 5/20 = 1/4.",
    ["subtraction", "fractions", "multiple operations"]
))

more_conceptual.append(make_q(
    "Hard",
    "The difference between two numbers is 2,847. If the smaller number is 5,693, what is the larger number?",
    ["8,540", "2,846", "8,440", "8,640"],
    "8,540",
    "Larger − Smaller = Difference. Larger = 5,693 + 2,847 = 8,540.",
    ["subtraction", "word problem", "inverse"]
))

more_conceptual.append(make_q(
    "Hard",
    "What is 100.00 − 33.33 − 33.33 − 33.34?",
    ["0.00", "0.01", "0.10", "1.00"],
    "0.00",
    "33.33 + 33.33 + 33.34 = 100.00. Therefore 100.00 − 100.00 = 0.00.",
    ["subtraction", "decimals", "precision"]
))

more_conceptual.append(make_q(
    "Hard",
    "A civil servant's monthly salary is ₱42,500. Tax is 12% of salary, PhilHealth is ₱900, Pag-IBIG is ₱200, and a loan payment is ₱3,500. What is the net pay?",
    ["₱32,800", "₱33,200", "₱32,600", "₱32,000"],
    "₱32,800",
    "Tax = 12% × 42,500 = 5,100. Total deductions = 5,100 + 900 + 200 + 3,500 = 9,700. Net = 42,500 − 9,700 = ₱32,800.",
    ["subtraction", "percentage", "word problem", "payroll"]
))

for q in more_conceptual:
    questions.append(q)

# ============================================================
# PAD TO EXACTLY 600 QUESTIONS
# ============================================================

# Count current questions by difficulty
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Before padding: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}, Total={len(questions)}")

# Deduplicate questions (keep first occurrence)
seen_texts = set()
deduped = []
for q in questions:
    if q["question"] not in seen_texts:
        seen_texts.add(q["question"])
        deduped.append(q)
questions = deduped

# Ensure no duplicate choices within any question
for q in questions:
    if len(set(q["choices"])) != len(q["choices"]):
        # Fix duplicate choices by regenerating unique distractors
        correct = q["answer"]
        unique_choices = {correct}
        new_choices = [correct]
        for c in q["choices"]:
            if c not in unique_choices:
                unique_choices.add(c)
                new_choices.append(c)
        # Pad if needed
        while len(new_choices) < 4:
            # Generate a simple offset distractor
            try:
                val = float(correct.replace(",", "").replace("₱", ""))
                offset = random.choice([0.3, -0.3, 0.7, -0.7, 1.1, -1.1, 2.3, -2.3])
                new_val = round(val + offset, 1)
                if "." in correct and len(correct.split(".")[-1]) == 1:
                    new_str = f"{new_val:.1f}"
                else:
                    new_str = f"{new_val:.2f}"
            except ValueError:
                new_str = correct + "_alt"
            if new_str not in unique_choices:
                unique_choices.add(new_str)
                new_choices.append(new_str)
        q["choices"] = new_choices[:4]
        random.shuffle(q["choices"])

# Recount after dedup
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"After dedup: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}, Total={len(questions)}")

# Trim excess questions if any difficulty exceeds 200
if easy_count > 200:
    easy_qs = [q for q in questions if q["difficulty"] == "Easy"]
    other_qs = [q for q in questions if q["difficulty"] != "Easy"]
    questions = easy_qs[:200] + other_qs
    easy_count = 200

if medium_count > 200:
    medium_qs = [q for q in questions if q["difficulty"] == "Medium"]
    other_qs = [q for q in questions if q["difficulty"] != "Medium"]
    questions = [q for q in questions if q["difficulty"] == "Easy"] + medium_qs[:200] + [q for q in questions if q["difficulty"] == "Hard"]
    medium_count = 200

if hard_count > 200:
    hard_qs = [q for q in questions if q["difficulty"] == "Hard"]
    other_qs = [q for q in questions if q["difficulty"] != "Hard"]
    questions = [q for q in questions if q["difficulty"] != "Hard"] + hard_qs[:200]
    hard_count = 200

# Pad Easy if needed
while easy_count < 200:
    a = random.randint(100, 9999)
    b = random.randint(10, a - 1)
    correct = a - b
    dists = set()
    for _ in range(10):
        d = correct + random.choice([1, -1, 10, -10, 5, -5])
        if d != correct and d > 0:
            dists.add(str(d))
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        d = correct + random.randint(1, 30)
        if str(d) not in distractors and d != correct:
            distractors.append(str(d))
    distractors = distractors[:3]
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q(
        "Easy", f"What is {a} − {b}?", choices, ans,
        f"Subtract: {a} − {b} = {correct}.",
        ["subtraction", "whole numbers", "computation"]
    ))
    easy_count += 1

# Pad Medium if needed
while medium_count < 200:
    choice = random.randint(0, 2)
    if choice == 0:
        # Decimal word problem
        a = round(random.uniform(1000, 50000), 2)
        b = round(random.uniform(100, a - 50), 2)
        correct = round(a - b, 2)
        correct_str = f"₱{correct:,.2f}"
        q_text = f"A fund of ₱{a:,.2f} had ₱{b:,.2f} disbursed. What is the remaining balance?"
        exp = f"₱{a:,.2f} − ₱{b:,.2f} = {correct_str}."
        tags = ["subtraction", "decimals", "word problem", "money"]
    elif choice == 1:
        # Integer
        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
        correct = a - b
        if b >= 0:
            q_text = f"What is ({a}) − {b}?" if a < 0 else f"What is {a} − {b}?"
        else:
            q_text = f"What is ({a}) − ({b})?" if a < 0 else f"What is {a} − ({b})?"
        correct_str = str(correct)
        exp = f"Apply subtraction rules: {q_text.replace('What is ', '').replace('?', '')} = {correct}."
        tags = ["subtraction", "integers", "computation"]
    else:
        # Fraction
        d1 = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
        d2 = random.choice([x for x in [3, 4, 5, 6, 7, 8, 9, 10] if x != d1])
        n1 = random.randint(max(2, d1 // 2 + 1), d1 - 1)
        n2 = random.randint(1, d2 - 1)
        fa = Fraction(n1, d1)
        fb = Fraction(n2, d2)
        if fa <= fb:
            n1 = d1 - 1
            fa = Fraction(n1, d1)
        result = fa - fb
        correct_str = str(result)
        q_text = f"What is {n1}/{d1} − {n2}/{d2}?"
        exp = f"Find LCD and subtract: {correct_str}."
        tags = ["subtraction", "fractions", "unlike denominators"]
    
    dists = set()
    if choice == 0:
        for offset in [0.01, -0.01, 1, -1, 10, -10]:
            d = round(correct + offset, 2)
            if d != correct and d > 0:
                dists.add(f"₱{d:,.2f}")
    elif choice == 1:
        for offset in [1, -1, 2, -2, 5, -5, 10, -10]:
            d = correct + offset
            if d != correct:
                dists.add(str(d))
    else:
        for offset in [Fraction(1, 12), Fraction(-1, 12), Fraction(1, 6)]:
            fake = result + offset
            if fake > 0 and fake != result:
                dists.add(str(fake))
    
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if choice == 0:
            d = round(correct + random.uniform(1, 500), 2)
            ds = f"₱{d:,.2f}"
        elif choice == 1:
            d = correct + random.randint(-20, 20)
            ds = str(d)
        else:
            ds = str(Fraction(random.randint(1, 15), random.randint(2, 20)))
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q("Medium", q_text, choices, ans, exp, tags))
    medium_count += 1

# Pad Hard if needed
while hard_count < 200:
    choice = random.randint(0, 2)
    if choice == 0:
        # Large number
        a = random.randint(100000, 9999999)
        b = random.randint(10000, a - 1)
        correct = a - b
        correct_str = fmt_num(correct)
        q_text = f"What is {fmt_num(a)} − {fmt_num(b)}?"
        exp = f"Subtract with careful regrouping: {fmt_num(a)} − {fmt_num(b)} = {correct_str}."
        tags = ["subtraction", "whole numbers", "large numbers"]
    elif choice == 1:
        # Complex decimal
        a = round(random.uniform(5000, 100000), 2)
        b = round(random.uniform(1000, a - 100), 2)
        correct = round(a - b, 2)
        correct_str = f"{correct:,.2f}"
        q_text = f"What is {a:,.2f} − {b:,.2f}?"
        exp = f"Align decimals and subtract: {correct_str}."
        tags = ["subtraction", "decimals", "large numbers"]
    else:
        # Mixed number with unlike denoms
        w1 = random.randint(6, 20)
        w2 = random.randint(1, w1 - 1)
        d1 = random.choice([3, 4, 5, 6, 8])
        d2 = random.choice([x for x in [3, 4, 5, 6, 8] if x != d1])
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        f1 = Fraction(w1 * d1 + n1, d1)
        f2 = Fraction(w2 * d2 + n2, d2)
        if f1 <= f2:
            w1 = w2 + 3
            f1 = Fraction(w1 * d1 + n1, d1)
        result = f1 - f2
        wr = int(result)
        fr = result - wr
        correct_str = f"{wr} {fr}" if fr != 0 else str(wr)
        q_text = f"What is {w1} {n1}/{d1} − {w2} {n2}/{d2}?"
        exp = f"Convert to improper fractions, find LCD, subtract: {correct_str}."
        tags = ["subtraction", "fractions", "mixed numbers", "complex"]
    
    dists = set()
    if choice == 0:
        for offset in [1, -1, 10, -10, 100, -100, 1000, -1000]:
            d = correct + offset
            if d != correct and d > 0:
                dists.add(fmt_num(d))
    elif choice == 1:
        for offset in [0.01, -0.01, 0.1, -0.1, 1, -1, 10, -10]:
            d = round(correct + offset, 2)
            if d != correct and d > 0:
                dists.add(f"{d:,.2f}")
    else:
        for offset in [Fraction(1, 12), Fraction(-1, 12), Fraction(1, 1), Fraction(-1, 1)]:
            fake = result + offset
            if fake > 0 and fake != result:
                fw = int(fake)
                ff = fake - fw
                dists.add(f"{fw} {ff}" if ff != 0 else str(fw))
    
    dists.discard(correct_str)
    distractors = list(dists)[:3]
    while len(distractors) < 3:
        if choice == 0:
            d = correct + random.randint(1, 5000)
            ds = fmt_num(d)
        elif choice == 1:
            d = round(correct + random.uniform(1, 100), 2)
            ds = f"{d:,.2f}"
        else:
            fw = random.randint(1, w1)
            ff = Fraction(random.randint(1, 11), 12)
            ds = f"{fw} {ff}"
        if ds != correct_str and ds not in distractors:
            distractors.append(ds)
    distractors = distractors[:3]
    choices, ans = shuffle_choices(correct_str, distractors)
    
    questions.append(make_q("Hard", q_text, choices, ans, exp, tags))
    hard_count += 1

# Final count
easy_final = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_final = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_final = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final: Easy={easy_final}, Medium={medium_final}, Hard={hard_final}, Total={len(questions)}")

# Reassign IDs sequentially
for idx, q in enumerate(questions, 1):
    q["id"] = idx

# Write output
output_path = r"c:\Users\Jaime\Documents\GitHub\csnexus\data\seed\questions\numerical-ability\basic-operations\subtraction\questions.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written {len(questions)} questions to {output_path}")
