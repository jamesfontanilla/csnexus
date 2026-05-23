"""
Generate 600 questions for Operations with Signed Numbers.
200 Easy / 200 Medium / 200 Hard

Covers:
- Absolute value
- Integer addition (same sign, different sign)
- Integer subtraction (KCC)
- Integer multiplication (sign rules)
- Integer division (sign rules)
- Mixed operations / PEMDAS with integers
- Comparing and ordering signed numbers
- Real-life applications (temperature, finance, elevation)
"""
import json
import random

random.seed(2024)

questions: list[dict] = []
qid = 0


def make_q(difficulty: str, question: str, choices: list[str], answer: str,
            explanation: str, tags: list[str]) -> dict:
    global qid
    qid += 1
    return {
        "id": qid,
        "subtest": "Numerical Ability",
        "module": "Basic Operations",
        "subtopic": "Operations with Signed Numbers",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English",
    }


def shuffle_choices(correct: str, distractors: list[str]) -> tuple[list[str], str]:
    """Return shuffled choices and the correct answer string."""
    all_c = [correct] + distractors[:3]
    # Ensure no duplicates
    seen = set()
    unique = []
    for c in all_c:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    # Pad if needed
    while len(unique) < 4:
        offset = random.choice([1, -1, 2, -2])
        try:
            val = int(correct) + offset
            candidate = str(val)
        except ValueError:
            candidate = str(offset)
        if candidate not in seen:
            seen.add(candidate)
            unique.append(candidate)
    random.shuffle(unique)
    return unique, correct


def make_distractors_int(correct: int, spread: int = 5) -> list[str]:
    """Generate 3 unique integer distractors near the correct answer."""
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 50:
        offset = random.randint(1, spread) * random.choice([1, -1])
        d = correct + offset
        if d != correct:
            distractors.add(str(d))
        attempts += 1
    # Also add sign-flipped distractor if not already present
    if str(-correct) not in distractors and -correct != correct:
        distractors.add(str(-correct))
    result = list(distractors)[:3]
    while len(result) < 3:
        result.append(str(correct + random.choice([10, -10, 7, -7])))
    return result[:3]


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Easy: Absolute Value (30 questions) ---
abs_values_used: set[int] = set()
for i in range(30):
    if i < 20:
        n = random.randint(-99, -1)
        while n in abs_values_used:
            n = random.randint(-99, -1)
    else:
        n = random.randint(1, 99)
        while n in abs_values_used:
            n = random.randint(1, 99)
    abs_values_used.add(n)
    correct = abs(n)
    distractors = [str(-correct), str(correct + random.choice([1, -1])),
                   str(n) if n < 0 else str(-n)]
    choices, ans = shuffle_choices(str(correct), distractors)
    if n < 0:
        q_text = f"What is |{n}|?"
        expl = f"Absolute value is distance from zero. |{n}| = {correct}."
    else:
        q_text = f"What is |{n}|?"
        expl = f"Absolute value of a positive number is itself. |{n}| = {correct}."
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["absolute value", "integers", "signed numbers"]))

# --- Easy: Addition same sign (35 questions) ---
for i in range(35):
    if i < 18:
        # Both negative, small
        a = random.randint(-20, -1)
        b = random.randint(-20, -1)
    else:
        # Both positive
        a = random.randint(1, 30)
        b = random.randint(1, 30)
    correct = a + b
    distractors = make_distractors_int(correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({a}) + ({b})?"
    if a < 0 and b < 0:
        expl = (f"Same signs (both negative): add absolute values "
                f"{abs(a)} + {abs(b)} = {abs(correct)}, keep negative. "
                f"Result: {correct}.")
    else:
        expl = f"Both positive: {a} + {b} = {correct}."
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["addition", "integers", "same sign"]))

# --- Easy: Addition different sign (35 questions) ---
for i in range(35):
    a = random.randint(-25, -1)
    b = random.randint(1, 25)
    if random.random() < 0.5:
        a, b = b, a  # swap order
    correct = a + b
    distractors = make_distractors_int(correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({a}) + ({b})?"
    bigger = a if abs(a) > abs(b) else b
    expl = (f"Different signs: subtract absolute values |{abs(a)} - {abs(b)}| = "
            f"{abs(correct)}, take sign of number with larger absolute value "
            f"({bigger}). Result: {correct}.")
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["addition", "integers", "different sign"]))

# --- Easy: Subtraction basic (35 questions) ---
for i in range(35):
    a = random.randint(-15, 15)
    b = random.randint(-15, 15)
    while b == 0:
        b = random.randint(-15, 15)
    correct = a - b
    distractors = make_distractors_int(correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    if b < 0:
        q_text = f"What is {a} − ({b})?"
        expl = (f"KCC: {a} − ({b}) = {a} + ({-b}) = {correct}.")
    else:
        q_text = f"What is {a} − {b}?"
        expl = f"{a} − {b} = {correct}."
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["subtraction", "integers", "KCC"]))

# --- Easy: Multiplication basic (35 questions) ---
for i in range(35):
    a = random.randint(-12, 12)
    b = random.randint(-12, 12)
    while a == 0 or b == 0:
        a = random.randint(-12, 12)
        b = random.randint(-12, 12)
    correct = a * b
    distractors = make_distractors_int(correct, spread=8)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({a}) × ({b})?"
    sign_word = "positive" if (a > 0) == (b > 0) else "negative"
    sign_reason = "Same signs" if (a > 0) == (b > 0) else "Different signs"
    expl = (f"{sign_reason} → {sign_word}. "
            f"{abs(a)} × {abs(b)} = {abs(correct)}. Result: {correct}.")
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["multiplication", "integers", "sign rules"]))

# --- Easy: Division basic (30 questions) ---
for i in range(30):
    divisor = random.choice([-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9])
    quotient = random.randint(-10, 10)
    while quotient == 0:
        quotient = random.randint(-10, 10)
    dividend = divisor * quotient
    correct = quotient
    distractors = make_distractors_int(correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({dividend}) ÷ ({divisor})?"
    sign_reason = "Same signs" if (dividend > 0) == (divisor > 0) else "Different signs"
    sign_word = "positive" if (dividend > 0) == (divisor > 0) else "negative"
    expl = (f"{sign_reason} → {sign_word}. "
            f"{abs(dividend)} ÷ {abs(divisor)} = {abs(correct)}. Result: {correct}.")
    questions.append(make_q("Easy", q_text, choices, ans, expl,
                            ["division", "integers", "sign rules"]))

assert len(questions) == 200, f"Easy count: {len(questions)}"

# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Medium: Absolute value of expressions (25 questions) ---
for i in range(25):
    a = random.randint(-30, 30)
    b = random.randint(-30, 30)
    while a + b == 0:
        b = random.randint(-30, 30)
    inner = a + b
    correct = abs(inner)
    distractors = make_distractors_int(correct)
    # Add common mistake: |a| + |b|
    wrong_sum = abs(a) + abs(b)
    if str(wrong_sum) not in distractors and wrong_sum != correct:
        distractors[0] = str(wrong_sum)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is |{a} + ({b})|?"
    expl = (f"First evaluate inside: {a} + ({b}) = {inner}. "
            f"Then absolute value: |{inner}| = {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["absolute value", "expressions", "integers"]))

# --- Medium: Addition with 3 terms (25 questions) ---
for i in range(25):
    a = random.randint(-30, 30)
    b = random.randint(-30, 30)
    c = random.randint(-30, 30)
    correct = a + b + c
    distractors = make_distractors_int(correct, spread=7)
    choices, ans = shuffle_choices(str(correct), distractors)
    parts = []
    for x in [a, b, c]:
        parts.append(f"({x})" if x < 0 else str(x))
    q_text = f"What is {parts[0]} + {parts[1]} + {parts[2]}?"
    pos_sum = sum(x for x in [a, b, c] if x > 0)
    neg_sum = sum(x for x in [a, b, c] if x < 0)
    expl = (f"Group positives: {pos_sum}. Group negatives: {neg_sum}. "
            f"Combine: {pos_sum} + ({neg_sum}) = {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["addition", "integers", "multiple terms"]))

# --- Medium: Subtraction with negatives (25 questions) ---
for i in range(25):
    a = random.randint(-40, 40)
    b = random.randint(-40, -1)  # always negative subtrahend
    correct = a - b  # subtracting a negative = adding
    distractors = make_distractors_int(correct, spread=8)
    # Common mistake: a + b (forgetting to flip)
    wrong = a + b
    if str(wrong) not in [str(correct)] + distractors and wrong != correct:
        distractors[0] = str(wrong)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is {a} − ({b})?"
    expl = (f"KCC: {a} − ({b}) = {a} + ({-b}) = {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["subtraction", "integers", "double negative"]))

# --- Medium: Multiplication with 3 factors (25 questions) ---
for i in range(25):
    a = random.randint(-8, 8)
    b = random.randint(-8, 8)
    c = random.randint(-8, 8)
    while a == 0 or b == 0 or c == 0:
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)
        c = random.randint(-8, 8)
    correct = a * b * c
    neg_count = sum(1 for x in [a, b, c] if x < 0)
    sign_word = "negative" if neg_count % 2 == 1 else "positive"
    distractors = make_distractors_int(correct, spread=15)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({a})({b})({c})?"
    expl = (f"{neg_count} negative factor(s) → {'odd' if neg_count % 2 == 1 else 'even'} "
            f"→ {sign_word}. {abs(a)} × {abs(b)} × {abs(c)} = {abs(correct)}. "
            f"Result: {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["multiplication", "integers", "multiple factors"]))

# --- Medium: Division chained (20 questions) ---
for i in range(20):
    # Create a ÷ b ÷ c where results are integers
    c_val = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
    b_val = random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
    quotient_final = random.randint(-8, 8)
    while quotient_final == 0:
        quotient_final = random.randint(-8, 8)
    mid = quotient_final * c_val
    dividend = mid * b_val
    # dividend ÷ b_val = mid, mid ÷ c_val = quotient_final
    correct = quotient_final
    distractors = make_distractors_int(correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    q_text = f"What is ({dividend}) ÷ ({b_val}) ÷ ({c_val})?"
    expl = (f"Left to right: ({dividend}) ÷ ({b_val}) = {mid}. "
            f"Then {mid} ÷ ({c_val}) = {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["division", "integers", "chained operations"]))

# --- Medium: Comparing/ordering signed numbers (20 questions) ---
for i in range(20):
    nums = random.sample(range(-20, 21), 5)
    sorted_nums = sorted(nums)
    if i < 10:
        # Least to greatest
        correct_str = ", ".join(str(x) for x in sorted_nums)
        wrong1 = ", ".join(str(x) for x in sorted(nums, reverse=True))
        wrong2 = ", ".join(str(x) for x in sorted(nums, key=abs))
        wrong3 = ", ".join(str(x) for x in sorted(nums, key=abs, reverse=True))
        choices, ans = shuffle_choices(correct_str, [wrong1, wrong2, wrong3])
        q_text = (f"Arrange from least to greatest: "
                  f"{', '.join(str(x) for x in nums)}")
        expl = (f"On the number line, leftmost is least. "
                f"Correct order: {correct_str}.")
        tags = ["comparing", "ordering", "least to greatest"]
    else:
        # Greatest to least
        sorted_desc = sorted(nums, reverse=True)
        correct_str = ", ".join(str(x) for x in sorted_desc)
        wrong1 = ", ".join(str(x) for x in sorted_nums)
        wrong2 = ", ".join(str(x) for x in sorted(nums, key=abs, reverse=True))
        wrong3 = ", ".join(str(x) for x in sorted(nums, key=abs))
        choices, ans = shuffle_choices(correct_str, [wrong1, wrong2, wrong3])
        q_text = (f"Arrange from greatest to least: "
                  f"{', '.join(str(x) for x in nums)}")
        expl = (f"On the number line, rightmost is greatest. "
                f"Correct order: {correct_str}.")
        tags = ["comparing", "ordering", "greatest to least"]
    questions.append(make_q("Medium", q_text, choices, ans, expl, tags))

# --- Medium: PEMDAS with signed numbers (30 questions) ---
for i in range(30):
    if i < 10:
        # Pattern: a + b × c
        a = random.randint(-15, 15)
        b = random.randint(-8, 8)
        c = random.randint(-8, 8)
        while b == 0 or c == 0:
            b = random.randint(-8, 8)
            c = random.randint(-8, 8)
        correct = a + b * c
        product = b * c
        distractors = make_distractors_int(correct, spread=10)
        # Common mistake: (a+b)*c
        wrong = (a + b) * c
        if str(wrong) != str(correct) and str(wrong) not in distractors:
            distractors[0] = str(wrong)
        choices, ans = shuffle_choices(str(correct), distractors)
        b_str = f"({b})" if b < 0 else str(b)
        c_str = f"({c})" if c < 0 else str(c)
        a_str = f"({a})" if a < 0 else str(a)
        q_text = f"What is {a_str} + {b_str} × {c_str}?"
        expl = (f"Multiply first: {b} × {c} = {product}. "
                f"Then add: {a} + {product} = {correct}.")
    elif i < 20:
        # Pattern: a × b + c × d
        a = random.randint(-6, 6)
        b = random.randint(-6, 6)
        c = random.randint(-6, 6)
        d = random.randint(-6, 6)
        while a == 0 or b == 0 or c == 0 or d == 0:
            a = random.randint(-6, 6)
            b = random.randint(-6, 6)
            c = random.randint(-6, 6)
            d = random.randint(-6, 6)
        correct = a * b + c * d
        distractors = make_distractors_int(correct, spread=12)
        choices, ans = shuffle_choices(str(correct), distractors)
        parts = [f"({x})" if x < 0 else str(x) for x in [a, b, c, d]]
        q_text = f"What is {parts[0]} × {parts[1]} + {parts[2]} × {parts[3]}?"
        expl = (f"Multiply first: {a} × {b} = {a*b} and {c} × {d} = {c*d}. "
                f"Then add: {a*b} + {c*d} = {correct}.")
    else:
        # Pattern: a - b × c
        a = random.randint(-15, 15)
        b = random.randint(-8, 8)
        c = random.randint(-8, 8)
        while b == 0 or c == 0:
            b = random.randint(-8, 8)
            c = random.randint(-8, 8)
        correct = a - b * c
        product = b * c
        distractors = make_distractors_int(correct, spread=10)
        choices, ans = shuffle_choices(str(correct), distractors)
        b_str = f"({b})" if b < 0 else str(b)
        c_str = f"({c})" if c < 0 else str(c)
        a_str = f"({a})" if a < 0 else str(a)
        q_text = f"What is {a_str} − {b_str} × {c_str}?"
        expl = (f"Multiply first: {b} × {c} = {product}. "
                f"Then subtract: {a} − {product} = {correct}.")
    questions.append(make_q("Medium", q_text, choices, ans, expl,
                            ["PEMDAS", "order of operations", "integers"]))

# --- Medium: Real-life word problems (30 questions) ---
temperature_templates = [
    ("The temperature was {a}°C in the morning. By afternoon it rose by {b}°C. "
     "What is the afternoon temperature?", "add"),
    ("The temperature was {a}°C. It then dropped by {b}°C. "
     "What is the new temperature?", "subtract_pos"),
    ("At midnight the temperature was {a}°C. By dawn it fell {b}°C further. "
     "What was the temperature at dawn?", "subtract_pos"),
]

finance_templates = [
    ("A government office had a surplus of ₱{a}. It then incurred expenses of ₱{b}. "
     "What is the net balance?", "subtract_pos"),
    ("An employee earned ₱{a} in overtime but was deducted ₱{b} for absences. "
     "What is the net change in pay?", "subtract_pos"),
    ("A trader gained ₱{a} on Monday and lost ₱{b} on Tuesday. "
     "What is the net result?", "subtract_pos"),
]

elevation_templates = [
    ("A diver is at {a} meters (below sea level). She ascends {b} meters. "
     "What is her new position?", "add_pos"),
    ("A mountain base is at {a} meters elevation. The peak is {b} meters higher. "
     "What is the peak elevation?", "add_pos"),
]

for i in range(30):
    if i < 12:
        template, op = random.choice(temperature_templates)
        a = random.randint(-20, 15)
        b = random.randint(3, 25)
        if op == "add":
            correct = a + b
            expl = f"{a} + {b} = {correct}°C."
        else:
            correct = a - b
            expl = f"{a} − {b} = {correct}°C."
        q_text = template.format(a=a, b=b)
        tags_list = ["word problem", "temperature", "signed numbers"]
    elif i < 24:
        template, op = random.choice(finance_templates)
        a = random.randint(5000, 50000)
        a = (a // 1000) * 1000  # round to thousands
        b = random.randint(3000, 40000)
        b = (b // 1000) * 1000
        correct = a - b
        q_text = template.format(a=f"{a:,}", b=f"{b:,}")
        expl = f"{a:,} − {b:,} = {correct:,}."
        correct_str = f"{correct:,}"
        distractors = [f"{correct + 1000:,}", f"{correct - 1000:,}",
                       f"{a + b:,}"]
        choices, ans = shuffle_choices(correct_str, distractors)
        questions.append(make_q("Medium", q_text, choices, ans, expl,
                                ["word problem", "finance", "signed numbers"]))
        continue
    else:
        template, op = random.choice(elevation_templates)
        a = random.randint(-200, -10)
        b = random.randint(20, 150)
        correct = a + b
        q_text = template.format(a=a, b=b)
        expl = f"{a} + {b} = {correct} meters."
        tags_list = ["word problem", "elevation", "signed numbers"]
    distractors = make_distractors_int(correct, spread=8)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Medium", q_text, choices, ans, expl, tags_list))

assert len(questions) == 400, f"After medium: {len(questions)}"

# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Hard: Complex absolute value expressions (25 questions) ---
for i in range(25):
    a = random.randint(-20, 20)
    b = random.randint(-20, 20)
    c = random.randint(-20, 20)
    while a - b == 0:
        b = random.randint(-20, 20)
    if i < 12:
        # |a - b| + c
        inner = a - b
        correct = abs(inner) + c
        q_text = f"What is |{a} − ({b})| + ({c})?"
        expl = (f"Inside: {a} − ({b}) = {a - b}. "
                f"|{a - b}| = {abs(inner)}. "
                f"Then {abs(inner)} + ({c}) = {correct}.")
    else:
        # |a| - |b| + c
        correct = abs(a) - abs(b) + c
        q_text = f"What is |{a}| − |{b}| + ({c})?"
        expl = (f"|{a}| = {abs(a)}, |{b}| = {abs(b)}. "
                f"{abs(a)} − {abs(b)} + ({c}) = {correct}.")
    distractors = make_distractors_int(correct, spread=8)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["absolute value", "expressions", "multi-step"]))

# --- Hard: Exponent with sign (−x² vs (−x)²) (20 questions) ---
# Use unique bases for each sub-group to avoid duplicates
neg_sq_bases = list(range(2, 12))  # 10 unique bases for −base²
random.shuffle(neg_sq_bases)
paren_sq_bases = list(range(2, 12))  # 10 unique bases for (−base)²
random.shuffle(paren_sq_bases)
for i in range(20):
    if i < 10:
        base = neg_sq_bases[i]
        # −base²
        correct = -(base ** 2)
        q_text = f"What is −{base}²?"
        expl = (f"−{base}² = −({base}²) = −{base**2}. "
                f"The exponent applies only to {base}, not the negative sign.")
        wrong = base ** 2  # forgetting the negative
    else:
        base = paren_sq_bases[i - 10]
        # (−base)²
        correct = base ** 2
        q_text = f"What is (−{base})²?"
        expl = (f"(−{base})² = (−{base})(−{base}) = {base**2}. "
                f"Same signs → positive.")
        wrong = -(base ** 2)  # thinking it stays negative
    distractors = make_distractors_int(correct, spread=10)
    if str(wrong) not in [str(correct)] + distractors:
        distractors[0] = str(wrong)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["exponents", "sign rules", "PEMDAS"]))

# --- Hard: Multi-step PEMDAS (35 questions) ---
for i in range(35):
    if i < 12:
        # (a + b) × c − d
        a = random.randint(-10, 10)
        b = random.randint(-10, 10)
        c = random.randint(-6, 6)
        d = random.randint(-15, 15)
        while c == 0:
            c = random.randint(-6, 6)
        correct = (a + b) * c - d
        a_str = f"({a})" if a < 0 else str(a)
        b_str = f"({b})" if b < 0 else str(b)
        c_str = f"({c})" if c < 0 else str(c)
        d_str = f"({d})" if d < 0 else str(d)
        q_text = f"What is ({a_str} + {b_str}) × {c_str} − {d_str}?"
        paren_val = a + b
        prod = paren_val * c
        expl = (f"Parentheses: {a} + {b} = {paren_val}. "
                f"Multiply: {paren_val} × {c} = {prod}. "
                f"Subtract: {prod} − {d} = {correct}.")
    elif i < 24:
        # a² + b × c
        a = random.randint(-7, 7)
        b = random.randint(-8, 8)
        c = random.randint(-8, 8)
        while a == 0 or b == 0 or c == 0:
            a = random.randint(-7, 7)
            b = random.randint(-8, 8)
            c = random.randint(-8, 8)
        correct = a**2 + b * c
        q_text = f"What is ({a})² + ({b}) × ({c})?"
        expl = (f"Exponent: ({a})² = {a**2}. "
                f"Multiply: {b} × {c} = {b*c}. "
                f"Add: {a**2} + {b*c} = {correct}.")
    else:
        # a × b − c ÷ d
        d = random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
        c_mult = random.randint(-8, 8)
        while c_mult == 0:
            c_mult = random.randint(-8, 8)
        c = d * c_mult  # ensure clean division
        a = random.randint(-8, 8)
        b = random.randint(-8, 8)
        while a == 0 or b == 0:
            a = random.randint(-8, 8)
            b = random.randint(-8, 8)
        correct = a * b - c // d
        q_text = (f"What is ({a}) × ({b}) − ({c}) ÷ ({d})?")
        expl = (f"Multiply: {a} × {b} = {a*b}. "
                f"Divide: {c} ÷ {d} = {c//d}. "
                f"Subtract: {a*b} − {c//d} = {correct}.")
    distractors = make_distractors_int(correct, spread=12)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["PEMDAS", "multi-step", "integers"]))

# --- Hard: Nested brackets/grouping (25 questions) ---
for i in range(25):
    if i < 13:
        # [a + b] ÷ [c × d]
        c = random.randint(-6, 6)
        d = random.randint(-6, 6)
        while c == 0 or d == 0:
            c = random.randint(-6, 6)
            d = random.randint(-6, 6)
        denom = c * d
        quotient = random.randint(-8, 8)
        while quotient == 0:
            quotient = random.randint(-8, 8)
        numer = denom * quotient
        # Split numer into a + b
        a = random.randint(-30, 30)
        b = numer - a
        correct = quotient
        q_text = f"What is [({a}) + ({b})] ÷ [({c}) × ({d})]?"
        expl = (f"Numerator: {a} + {b} = {numer}. "
                f"Denominator: {c} × {d} = {denom}. "
                f"Divide: {numer} ÷ {denom} = {correct}.")
    else:
        # −(a − b) + c
        a = random.randint(-15, 15)
        b = random.randint(-15, 15)
        c = random.randint(-15, 15)
        inner = a - b
        correct = -inner + c
        q_text = f"What is −({a} − ({b})) + ({c})?"
        expl = (f"Inside: {a} − ({b}) = {a - b}. "
                f"Negate: −({a - b}) = {-(a-b)}. "
                f"Add: {-(a-b)} + {c} = {correct}.")
    distractors = make_distractors_int(correct, spread=8)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["grouping", "brackets", "multi-step"]))

# --- Hard: Multiplication with 4+ factors (20 questions) ---
for i in range(20):
    num_factors = random.choice([4, 5])
    factors = [random.randint(-5, 5) for _ in range(num_factors)]
    while 0 in factors:
        factors = [random.randint(-5, 5) for _ in range(num_factors)]
    correct = 1
    for f in factors:
        correct *= f
    neg_count = sum(1 for f in factors if f < 0)
    sign_word = "negative" if neg_count % 2 == 1 else "positive"
    abs_product = 1
    for f in factors:
        abs_product *= abs(f)
    distractors = make_distractors_int(correct, spread=20)
    # Add sign-flipped as distractor
    if str(-correct) not in [str(correct)] + distractors:
        distractors[0] = str(-correct)
    choices, ans = shuffle_choices(str(correct), distractors)
    factors_str = "".join(f"({f})" for f in factors)
    q_text = f"What is {factors_str}?"
    expl = (f"{neg_count} negative factor(s) (odd → negative, even → positive) "
            f"→ {sign_word}. Absolute values: "
            f"{' × '.join(str(abs(f)) for f in factors)} = {abs_product}. "
            f"Result: {correct}.")
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["multiplication", "multiple factors", "sign counting"]))

# --- Hard: Complex word problems (35 questions) ---
for i in range(35):
    if i < 10:
        # Multi-day temperature
        start = random.randint(-10, 10)
        changes = [random.randint(-15, 15) for _ in range(3)]
        while all(c == 0 for c in changes):
            changes = [random.randint(-15, 15) for _ in range(3)]
        correct = start + sum(changes)
        change_strs = []
        for idx, ch in enumerate(changes):
            day = ["Monday", "Tuesday", "Wednesday"][idx]
            if ch > 0:
                change_strs.append(f"rose {ch}°C on {day}")
            elif ch < 0:
                change_strs.append(f"dropped {abs(ch)}°C on {day}")
            else:
                change_strs.append(f"stayed the same on {day}")
        q_text = (f"The temperature on Sunday was {start}°C. It "
                  f"{', '.join(change_strs)}. "
                  f"What was the temperature on Wednesday night?")
        calc = f"{start} + ({') + ('.join(str(c) for c in changes)}) = {correct}"
        expl = f"Calculate: {start} + {' + '.join(f'({c})' for c in changes)} = {correct}°C."
        tags_list = ["word problem", "temperature", "multi-step"]
    elif i < 20:
        # Financial multi-transaction
        initial = random.randint(10, 100) * 1000
        transactions = [random.randint(-50, 50) * 1000 for _ in range(3)]
        while all(t == 0 for t in transactions):
            transactions = [random.randint(-50, 50) * 1000 for _ in range(3)]
        correct = initial + sum(transactions)
        labels = ["received a grant", "paid expenses", "collected fees"]
        parts_desc = []
        for idx, t in enumerate(transactions):
            if t > 0:
                parts_desc.append(f"{labels[idx]} of ₱{abs(t):,}")
            else:
                parts_desc.append(f"{labels[idx]} of ₱{abs(t):,}")
        q_text = (f"A barangay started with ₱{initial:,}. It then "
                  f"{', '.join(parts_desc)}. What is the final balance?")
        expl = (f"{initial:,} + {' + '.join(f'({t:,})' for t in transactions)} "
                f"= {correct:,}.")
        correct_str = f"{correct:,}"
        distractors = [f"{correct + 5000:,}", f"{correct - 5000:,}",
                       f"{initial + sum(abs(t) for t in transactions):,}"]
        choices, ans = shuffle_choices(correct_str, distractors)
        questions.append(make_q("Hard", q_text, choices, ans, expl,
                                ["word problem", "finance", "multi-step"]))
        continue
    elif i < 28:
        # Elevation difference
        elev_a = random.randint(-300, -10)
        elev_b = random.randint(100, 5000)
        correct = elev_b - elev_a
        q_text = (f"Point A is at {elev_a} meters (below sea level). "
                  f"Point B is at {elev_b} meters (above sea level). "
                  f"What is the difference in elevation between B and A?")
        expl = f"{elev_b} − ({elev_a}) = {elev_b} + {abs(elev_a)} = {correct} meters."
        tags_list = ["word problem", "elevation", "subtraction"]
    else:
        # Inventory multi-adjustment
        initial_inv = random.randint(200, 1000)
        received = random.randint(50, 300)
        shipped = random.randint(100, 400)
        damaged = random.randint(5, 50)
        correct = initial_inv + received - shipped - damaged
        q_text = (f"A warehouse had {initial_inv} units. It received {received} units, "
                  f"shipped out {shipped} units, and had {damaged} units damaged. "
                  f"What is the final inventory?")
        expl = (f"{initial_inv} + {received} − {shipped} − {damaged} = {correct} units.")
        tags_list = ["word problem", "inventory", "multi-step"]
    distractors = make_distractors_int(correct, spread=15)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl, tags_list))

# --- Hard: Mixed operations with division and exponents (20 questions) ---
for i in range(20):
    if i < 10:
        # (−a)^n + b ÷ c
        base = random.randint(2, 5)
        exp = random.choice([2, 3])
        power_val = (-base) ** exp
        c = random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6])
        b_mult = random.randint(-8, 8)
        while b_mult == 0:
            b_mult = random.randint(-8, 8)
        b = c * b_mult
        correct = power_val + b // c
        q_text = f"What is (−{base}){'²' if exp == 2 else '³'} + ({b}) ÷ ({c})?"
        expl = (f"(−{base}){'²' if exp == 2 else '³'} = {power_val}. "
                f"({b}) ÷ ({c}) = {b//c}. "
                f"{power_val} + {b//c} = {correct}.")
    else:
        # −a² × b + c
        a = random.randint(2, 7)
        b = random.randint(-6, 6)
        c = random.randint(-20, 20)
        while b == 0:
            b = random.randint(-6, 6)
        neg_sq = -(a ** 2)
        product = neg_sq * b
        correct = product + c
        b_str = f"({b})" if b < 0 else str(b)
        c_str = f"({c})" if c < 0 else str(c)
        q_text = f"What is −{a}² × {b_str} + {c_str}?"
        expl = (f"−{a}² = −{a**2}. "
                f"Multiply: −{a**2} × {b} = {product}. "
                f"Add: {product} + {c} = {correct}.")
    distractors = make_distractors_int(correct, spread=15)
    choices, ans = shuffle_choices(str(correct), distractors)
    questions.append(make_q("Hard", q_text, choices, ans, expl,
                            ["exponents", "PEMDAS", "multi-step"]))

# --- Hard: Conceptual / tricky (20 questions) ---
conceptual_questions = [
    {
        "q": "What is the value of (−1)¹⁰⁰?",
        "correct": "1",
        "distractors": ["-1", "0", "100"],
        "expl": "(−1) raised to an even power equals 1. 100 is even, so (−1)¹⁰⁰ = 1.",
        "tags": ["exponents", "conceptual", "sign rules"],
    },
    {
        "q": "What is the value of (−1)⁹⁹?",
        "correct": "-1",
        "distractors": ["1", "0", "-99"],
        "expl": "(−1) raised to an odd power equals −1. 99 is odd, so (−1)⁹⁹ = −1.",
        "tags": ["exponents", "conceptual", "sign rules"],
    },
    {
        "q": "If x = −5, what is −x²?",
        "correct": "-25",
        "distractors": ["25", "-10", "10"],
        "expl": "−x² = −(x²) = −((−5)²) = −(25) = −25. The exponent applies to x, then negate.",
        "tags": ["exponents", "variables", "sign rules"],
    },
    {
        "q": "If x = −5, what is (−x)²?",
        "correct": "25",
        "distractors": ["-25", "10", "-10"],
        "expl": "(−x)² = (−(−5))² = (5)² = 25.",
        "tags": ["exponents", "variables", "sign rules"],
    },
    {
        "q": "What is 0 − (−7)?",
        "correct": "7",
        "distractors": ["-7", "0", "14"],
        "expl": "0 − (−7) = 0 + 7 = 7. Subtracting a negative is adding.",
        "tags": ["subtraction", "zero", "conceptual"],
    },
    {
        "q": "Which is greater: −|−5| or |−5|?",
        "correct": "|−5|",
        "distractors": ["−|−5|", "They are equal", "Cannot be determined"],
        "expl": "|−5| = 5 and −|−5| = −5. Since 5 > −5, |−5| is greater.",
        "tags": ["absolute value", "comparing", "conceptual"],
    },
    {
        "q": "What is the sum of a number and its opposite?",
        "correct": "0",
        "distractors": ["The number itself", "Twice the number", "Undefined"],
        "expl": "A number plus its opposite always equals zero: x + (−x) = 0.",
        "tags": ["addition", "opposites", "conceptual"],
    },
    {
        "q": "If a × b > 0 and a < 0, what must be true about b?",
        "correct": "b < 0",
        "distractors": ["b > 0", "b = 0", "b could be positive or negative"],
        "expl": "If the product is positive and a is negative, b must also be negative (same signs → positive product).",
        "tags": ["multiplication", "sign rules", "reasoning"],
    },
    {
        "q": "If a + b < 0 and |a| > |b|, what is the sign of a?",
        "correct": "Negative",
        "distractors": ["Positive", "Zero", "Cannot be determined"],
        "expl": "The sum is negative and a has the larger absolute value, so a must be negative (it dominates the sum).",
        "tags": ["addition", "absolute value", "reasoning"],
    },
    {
        "q": "What is |−3| × |−4| − |−12|?",
        "correct": "0",
        "distractors": ["12", "-12", "24"],
        "expl": "|−3| = 3, |−4| = 4, |−12| = 12. So 3 × 4 − 12 = 12 − 12 = 0.",
        "tags": ["absolute value", "multiplication", "multi-step"],
    },
    {
        "q": "What is (−2)⁴ − 2⁴?",
        "correct": "0",
        "distractors": ["32", "-32", "16"],
        "expl": "(−2)⁴ = 16 (even power → positive). 2⁴ = 16. So 16 − 16 = 0.",
        "tags": ["exponents", "sign rules", "conceptual"],
    },
    {
        "q": "What is (−2)³ + 2³?",
        "correct": "0",
        "distractors": ["16", "-16", "8"],
        "expl": "(−2)³ = −8 (odd power → negative). 2³ = 8. So −8 + 8 = 0.",
        "tags": ["exponents", "sign rules", "conceptual"],
    },
    {
        "q": "A submarine at −80 m descends another 45 m, then ascends 60 m. What is its final depth?",
        "correct": "-65",
        "distractors": ["-185", "-25", "65"],
        "expl": "−80 + (−45) + 60 = −80 − 45 + 60 = −125 + 60 = −65 meters.",
        "tags": ["word problem", "elevation", "multi-step"],
    },
    {
        "q": "The product of five negative integers is always:",
        "correct": "Negative",
        "distractors": ["Positive", "Zero", "Cannot be determined"],
        "expl": "5 negative factors (odd count) → negative product.",
        "tags": ["multiplication", "sign counting", "conceptual"],
    },
    {
        "q": "The product of six negative integers is always:",
        "correct": "Positive",
        "distractors": ["Negative", "Zero", "Cannot be determined"],
        "expl": "6 negative factors (even count) → positive product.",
        "tags": ["multiplication", "sign counting", "conceptual"],
    },
    {
        "q": "What is −(−(−(−5)))?",
        "correct": "5",
        "distractors": ["-5", "0", "20"],
        "expl": "Work from inside out: −5 → −(−5)=5 → −(5)=−5 → −(−5)=5.",
        "tags": ["negation", "conceptual", "multi-step"],
    },
    {
        "q": "What is −(−(−7))?",
        "correct": "-7",
        "distractors": ["7", "0", "21"],
        "expl": "Work from inside out: −7 → −(−7)=7 → −(7)=−7.",
        "tags": ["negation", "conceptual", "multi-step"],
    },
    {
        "q": "If |x| = 9, what are the possible values of x?",
        "correct": "9 or −9",
        "distractors": ["9 only", "−9 only", "0"],
        "expl": "Absolute value of 9 is 9, and absolute value of −9 is also 9. Both satisfy |x| = 9.",
        "tags": ["absolute value", "conceptual", "equations"],
    },
    {
        "q": "What is (−6 + 2)(−3 − 1)?",
        "correct": "16",
        "distractors": ["-16", "8", "-8"],
        "expl": "(−6 + 2) = −4. (−3 − 1) = −4. (−4)(−4) = 16. Same signs → positive.",
        "tags": ["PEMDAS", "multiplication", "grouping"],
    },
    {
        "q": "What is [(−2)³ × (−3)] ÷ (−6)?",
        "correct": "-4",
        "distractors": ["4", "-24", "24"],
        "expl": "(−2)³ = −8. (−8)(−3) = 24. 24 ÷ (−6) = −4.",
        "tags": ["exponents", "PEMDAS", "multi-step"],
    },
]

for cq in conceptual_questions:
    choices, ans = shuffle_choices(cq["correct"], cq["distractors"])
    questions.append(make_q("Hard", cq["q"], choices, ans, cq["expl"], cq["tags"]))

assert len(questions) == 600, f"Final count: {len(questions)}"

# ============================================================
# VALIDATION & OUTPUT
# ============================================================

# Validate counts
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")

print(f"Total questions: {len(questions)}")
print(f"  Easy: {easy_count}")
print(f"  Medium: {medium_count}")
print(f"  Hard: {hard_count}")

assert easy_count == 200, f"Expected 200 Easy, got {easy_count}"
assert medium_count == 200, f"Expected 200 Medium, got {medium_count}"
assert hard_count == 200, f"Expected 200 Hard, got {hard_count}"

# Validate all questions have required fields
required_fields = ["id", "subtest", "module", "subtopic", "difficulty",
                   "question", "choices", "answer", "explanation", "tags",
                   "category", "language"]
for q in questions:
    for field in required_fields:
        assert field in q, f"Question {q['id']} missing field: {field}"
    assert len(q["choices"]) == 4, f"Question {q['id']} has {len(q['choices'])} choices"
    assert q["answer"] in q["choices"], f"Question {q['id']}: answer not in choices"

# Validate no duplicate questions
seen_questions = set()
for q in questions:
    if q["question"] in seen_questions:
        print(f"WARNING: Duplicate question at id {q['id']}: {q['question'][:50]}")
    seen_questions.add(q["question"])

print("All validations passed!")

# Write output
from pathlib import Path

output_dir = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / \
    "numerical-ability" / "basic-operations" / "operations-with-signed-numbers"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "questions.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
