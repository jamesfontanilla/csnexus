"""
Generate 600 multiple-choice order-of-operations questions for the CSE Numerical Ability section.
Distribution: 200 Easy, 200 Medium, 200 Hard
Output: data/seed/questions/numerical-ability/basic-operations/order-of-operations/questions.json
"""

import json
import random
import os
from fractions import Fraction

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
        "subtopic": "Order of Operations",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Professional", "Sub-Professional"],
        "language": "English",
    }


def shuffle_choices(correct, distractors):
    """Return shuffled list of choices as strings."""
    all_choices = [str(correct)] + [str(d) for d in distractors]
    random.shuffle(all_choices)
    return all_choices


def generate_int_distractors(correct, count=3, spread=None):
    """Generate integer distractors near the correct answer."""
    if spread is None:
        spread = max(3, abs(correct) // 5 + 1)
    distractors = set()
    attempts = 0
    while len(distractors) < count and attempts < 200:
        offset = random.choice(
            [-1, 1, -2, 2, -3, 3, -spread, spread, -spread * 2, spread * 2]
        )
        d = correct + offset
        if d != correct and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(correct + len(distractors) + 1)
    return list(distractors)[:count]


def generate_decimal_distractors(correct, count=3):
    """Generate decimal distractors near the correct answer."""
    distractors = set()
    attempts = 0
    offsets = [0.5, -0.5, 1.0, -1.0, 2.0, -2.0, 0.1, -0.1, 1.5, -1.5, 3.0, -3.0]
    while len(distractors) < count and attempts < 200:
        offset = random.choice(offsets)
        d = round(correct + offset, 2)
        if d != correct and d not in distractors:
            distractors.add(d)
        attempts += 1
    while len(distractors) < count:
        distractors.add(round(correct + (len(distractors) + 1) * 0.5, 2))
    return list(distractors)[:count]


def format_num(val):
    """Format a number cleanly."""
    if isinstance(val, float):
        if val == int(val):
            return str(int(val))
        return f"{val:g}"
    return str(val)


# ============================================================
# EASY QUESTIONS (200)
# ============================================================

# --- Type 1: Simple two-operation (add/sub + mult/div) --- (50 questions)
for _ in range(50):
    a = random.randint(2, 20)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    op1 = random.choice(["+", "-"])
    op2 = random.choice(["*", "/"])

    if op2 == "/":
        # Ensure clean division
        c = random.randint(2, 9)
        b = c * random.randint(2, 9)

    if op2 == "*":
        mult_result = b * c
    else:
        mult_result = b // c

    if op1 == "+":
        correct = a + mult_result
        expr = f"{a} + {b} × {c}" if op2 == "*" else f"{a} + {b} ÷ {c}"
        expl = (
            f"Multiplication first: {b} × {c} = {mult_result}. Then addition: {a} + {mult_result} = {correct}."
            if op2 == "*"
            else f"Division first: {b} ÷ {c} = {mult_result}. Then addition: {a} + {mult_result} = {correct}."
        )
    else:
        correct = a - mult_result
        expr = f"{a} - {b} × {c}" if op2 == "*" else f"{a} - {b} ÷ {c}"
        expl = (
            f"Multiplication first: {b} × {c} = {mult_result}. Then subtraction: {a} - {mult_result} = {correct}."
            if op2 == "*"
            else f"Division first: {b} ÷ {c} = {mult_result}. Then subtraction: {a} - {mult_result} = {correct}."
        )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Easy",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "PEMDAS", "two operations"],
        )
    )


# --- Type 2: Simple parentheses --- (50 questions)
for _ in range(50):
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    c = random.randint(2, 9)
    op_inside = random.choice(["+", "-"])
    op_outside = random.choice(["*", "/"])

    if op_inside == "+":
        inside = a + b
    else:
        a, b = max(a, b), min(a, b)  # ensure positive
        inside = a - b

    if op_outside == "*":
        correct = inside * c
        expr = f"({a} {op_inside} {b}) × {c}"
        expl = f"Parentheses first: {a} {op_inside} {b} = {inside}. Then multiply: {inside} × {c} = {correct}."
    else:
        # Ensure clean division
        c = random.randint(2, 6)
        inside = c * random.randint(2, 9)
        # Rebuild a and b
        if op_inside == "+":
            a = random.randint(1, inside - 1)
            b = inside - a
        else:
            b = random.randint(1, 20)
            a = inside + b
        correct = inside // c
        expr = f"({a} {op_inside} {b}) ÷ {c}"
        expl = f"Parentheses first: {a} {op_inside} {b} = {inside}. Then divide: {inside} ÷ {c} = {correct}."

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Easy",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "parentheses", "grouping symbols"],
        )
    )


# --- Type 3: Simple exponent + one operation --- (40 questions)
for _ in range(40):
    base = random.randint(2, 6)
    exp = random.choice([2, 3])
    power = base**exp
    other = random.randint(1, 20)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        correct = power + other
        expr = f"{base}{'²' if exp == 2 else '³'} + {other}"
        expl = f"Exponent first: {base}{'²' if exp == 2 else '³'} = {power}. Then addition: {power} + {other} = {correct}."
    elif op == "-":
        correct = power - other
        expr = f"{base}{'²' if exp == 2 else '³'} - {other}"
        expl = f"Exponent first: {base}{'²' if exp == 2 else '³'} = {power}. Then subtraction: {power} - {other} = {correct}."
    else:
        correct = power * other
        expr = f"{base}{'²' if exp == 2 else '³'} × {other}"
        expl = f"Exponent first: {base}{'²' if exp == 2 else '³'} = {power}. Then multiplication: {power} × {other} = {correct}."

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Easy",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "exponents", "PEMDAS"],
        )
    )


# --- Type 4: Multiplication and division left-to-right --- (30 questions)
for _ in range(30):
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    c = random.randint(2, 6)
    # Ensure clean division
    product = a * b
    if product % c != 0:
        c = random.choice([d for d in range(2, 10) if product % d == 0] or [1])
    correct = product // c if c != 0 else product
    expr = f"{a} × {b} ÷ {c}"
    expl = f"Left to right: {a} × {b} = {product}, then {product} ÷ {c} = {correct}."

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Easy",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "multiplication", "division", "left to right"],
        )
    )


# --- Type 5: Addition and subtraction left-to-right --- (30 questions)
for _ in range(30):
    a = random.randint(10, 50)
    b = random.randint(1, 20)
    c = random.randint(1, 20)
    ops = random.choice(["+-", "-+", "--"])
    if ops == "+-":
        correct = a + b - c
        expr = f"{a} + {b} - {c}"
        expl = f"Left to right: {a} + {b} = {a + b}, then {a + b} - {c} = {correct}."
    elif ops == "-+":
        correct = a - b + c
        expr = f"{a} - {b} + {c}"
        expl = f"Left to right: {a} - {b} = {a - b}, then {a - b} + {c} = {correct}."
    else:
        correct = a - b - c
        expr = f"{a} - {b} - {c}"
        expl = f"Left to right: {a} - {b} = {a - b}, then {a - b} - {c} = {correct}."

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Easy",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "addition", "subtraction", "left to right"],
        )
    )


# ============================================================
# MEDIUM QUESTIONS (200)
# ============================================================

# --- Type 1: Three operations with parentheses --- (50 questions)
for _ in range(50):
    a = random.randint(2, 8)
    b = random.randint(2, 8)
    c = random.randint(2, 8)
    d = random.randint(1, 10)
    op_in = random.choice(["+", "-"])
    op_out = random.choice(["*"])
    op_final = random.choice(["+", "-"])

    if op_in == "+":
        inside = a + b
    else:
        a, b = max(a, b), min(a, b)
        inside = a - b

    mult_result = inside * c

    if op_final == "+":
        correct = mult_result + d
    else:
        correct = mult_result - d

    expr = f"({a} {op_in} {b}) × {c} {op_final} {d}"
    expl = (
        f"Parentheses: {a} {op_in} {b} = {inside}. "
        f"Multiply: {inside} × {c} = {mult_result}. "
        f"{'Add' if op_final == '+' else 'Subtract'}: {mult_result} {op_final} {d} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "parentheses", "three operations"],
        )
    )


# --- Type 2: Exponent with multiplication and add/sub --- (40 questions)
for _ in range(40):
    coeff = random.randint(2, 5)
    base = random.randint(2, 5)
    exp = 2
    power = base**exp
    other = random.randint(1, 20)
    op = random.choice(["+", "-"])

    mult_result = coeff * power
    if op == "+":
        correct = mult_result + other
    else:
        correct = mult_result - other

    expr = f"{coeff} × {base}² {op} {other}"
    expl = (
        f"Exponent: {base}² = {power}. "
        f"Multiply: {coeff} × {power} = {mult_result}. "
        f"{'Add' if op == '+' else 'Subtract'}: {mult_result} {op} {other} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "exponents", "multiplication"],
        )
    )


# --- Type 3: Division and multiplication with add/sub --- (35 questions)
for _ in range(35):
    # a ÷ b × c + d or a ÷ b × c - d
    b = random.randint(2, 8)
    quotient = random.randint(2, 9)
    a = b * quotient
    c = random.randint(2, 6)
    d = random.randint(1, 15)
    op = random.choice(["+", "-"])

    mult_result = quotient * c
    if op == "+":
        correct = mult_result + d
    else:
        correct = mult_result - d

    expr = f"{a} ÷ {b} × {c} {op} {d}"
    expl = (
        f"Left to right: {a} ÷ {b} = {quotient}, then {quotient} × {c} = {mult_result}. "
        f"{'Add' if op == '+' else 'Subtract'}: {mult_result} {op} {d} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "division", "multiplication", "left to right"],
        )
    )


# --- Type 4: Two parentheses groups --- (35 questions)
for _ in range(35):
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    c = random.randint(2, 10)
    d = random.randint(2, 10)
    op_in1 = random.choice(["+", "-"])
    op_in2 = random.choice(["+", "-"])
    op_between = random.choice(["+", "-", "*"])

    # For subtraction, ensure first operand > second to keep results positive
    if op_in1 == "-":
        a, b = max(a, b), min(a, b)
        if a == b:
            a += 1
    if op_in2 == "-":
        c, d = max(c, d), min(c, d)
        if c == d:
            c += 1

    if op_in1 == "+":
        g1 = a + b
    else:
        g1 = a - b

    if op_in2 == "+":
        g2 = c + d
    else:
        g2 = c - d

    if g2 == 0 and op_between == "*":
        c += 1
        g2 = c - d

    if op_between == "+":
        correct = g1 + g2
    elif op_between == "-":
        correct = g1 - g2
    else:
        correct = g1 * g2

    expr = f"({a} {op_in1} {b}) {('×' if op_between == '*' else op_between)} ({c} {op_in2} {d})"
    expl = (
        f"First group: {a} {op_in1} {b} = {g1}. "
        f"Second group: {c} {op_in2} {d} = {g2}. "
        f"{'Multiply' if op_between == '*' else 'Add' if op_between == '+' else 'Subtract'}: "
        f"{g1} {'×' if op_between == '*' else op_between} {g2} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "parentheses", "two groups"],
        )
    )


# --- Type 5: Decimal operations with PEMDAS --- (20 questions)
for _ in range(20):
    a = round(random.uniform(1.5, 10.0), 1)
    b = round(random.uniform(1.5, 5.0), 1)
    c = random.randint(2, 6)
    op = random.choice(["+", "-"])

    mult_result = round(b * c, 1)
    if op == "+":
        correct = round(a + mult_result, 1)
    else:
        correct = round(a - mult_result, 1)

    expr = f"{a} {op} {b} × {c}"
    expl = (
        f"Multiplication first: {b} × {c} = {mult_result}. "
        f"{'Add' if op == '+' else 'Subtract'}: {a} {op} {mult_result} = {correct}."
    )

    distractors = generate_decimal_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(format_num(correct), [format_num(d) for d in distractors]),
            format_num(correct),
            expl,
            ["order of operations", "decimals", "PEMDAS"],
        )
    )


# --- Type 6: Fraction bar as grouping symbol --- (20 questions)
for _ in range(20):
    a = random.randint(2, 15)
    b = random.randint(2, 15)
    c = random.randint(2, 8)
    d = random.randint(1, 7)
    op_num = random.choice(["+", "-", "*"])
    op_den = random.choice(["+", "-"])

    if op_num == "+":
        numerator = a + b
    elif op_num == "-":
        a, b = max(a, b), min(a, b)
        numerator = a - b
    else:
        numerator = a * b

    if op_den == "+":
        denominator = c + d
    else:
        c, d = max(c, d), min(c, d)
        denominator = c - d

    if denominator == 0:
        denominator = 1
        d = c - 1

    # Ensure clean division
    if numerator % denominator != 0:
        numerator = denominator * random.randint(2, 8)
        if op_num == "+":
            a = random.randint(1, numerator - 1)
            b = numerator - a
        elif op_num == "-":
            b = random.randint(1, 20)
            a = numerator + b
        else:
            # factor numerator
            factors = [(i, numerator // i) for i in range(2, numerator) if numerator % i == 0]
            if factors:
                a, b = random.choice(factors)
            else:
                a, b = 1, numerator

    correct = numerator // denominator
    num_expr = f"{a} {('×' if op_num == '*' else op_num)} {b}"
    den_expr = f"{c} {op_den} {d}"
    expr = f"({num_expr}) / ({den_expr})"
    expl = (
        f"Numerator: {a} {('×' if op_num == '*' else op_num)} {b} = {numerator}. "
        f"Denominator: {c} {op_den} {d} = {denominator}. "
        f"Divide: {numerator} ÷ {denominator} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Medium",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "fraction bar", "grouping symbols"],
        )
    )


# ============================================================
# HARD QUESTIONS (200)
# ============================================================

# --- Type 1: Nested parentheses with exponents --- (40 questions)
for _ in range(40):
    a = random.randint(2, 5)
    b = random.randint(1, 5)
    c = random.randint(2, 4)
    d = random.randint(2, 5)
    e = random.randint(1, 10)

    inner = a + b
    power = inner**c
    outer = d * power
    op = random.choice(["+", "-"])
    if op == "+":
        correct = outer + e
    else:
        correct = outer - e

    exp_sym = "²" if c == 2 else "³" if c == 3 else f"^{c}"
    expr = f"{d} × ({a} + {b}){exp_sym} {op} {e}"
    expl = (
        f"Parentheses: {a} + {b} = {inner}. "
        f"Exponent: {inner}{exp_sym} = {power}. "
        f"Multiply: {d} × {power} = {outer}. "
        f"{'Add' if op == '+' else 'Subtract'}: {outer} {op} {e} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "nested parentheses", "exponents"],
        )
    )


# --- Type 2: Multiple operations with brackets --- (40 questions)
for _ in range(40):
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    c = random.randint(2, 6)
    d = random.randint(1, 8)
    e = random.randint(2, 5)

    inner = a * b
    bracket = inner + c
    # Ensure clean division
    if bracket % e != 0:
        c = e * random.randint(1, 4) - inner
        if c <= 0:
            c = e - (inner % e)
            if c == 0:
                c = e
        bracket = inner + c

    divided = bracket // e
    op = random.choice(["+", "-"])
    if op == "+":
        correct = divided + d
    else:
        correct = divided - d

    expr = f"[{a} × {b} + {c}] ÷ {e} {op} {d}"
    expl = (
        f"Inside brackets: {a} × {b} = {inner}, then {inner} + {c} = {bracket}. "
        f"Divide: {bracket} ÷ {e} = {divided}. "
        f"{'Add' if op == '+' else 'Subtract'}: {divided} {op} {d} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "brackets", "multi-step"],
        )
    )


# --- Type 3: Integer expressions with negative numbers --- (35 questions)
for _ in range(35):
    a = random.randint(-8, -2)
    b = random.randint(2, 8)
    c = random.randint(-6, -1)
    op1 = random.choice(["*", "*"])
    op2 = random.choice(["+", "-"])

    mult_result = a * b
    if op2 == "+":
        correct = mult_result + c
    else:
        correct = mult_result - c

    expr = f"({a}) × {b} {op2} ({c})"
    expl = (
        f"Multiplication: ({a}) × {b} = {mult_result}. "
        f"{'Add' if op2 == '+' else 'Subtract'}: {mult_result} {op2} ({c}) = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "integers", "negative numbers"],
        )
    )


# --- Type 4: Exponent expressions with multiple terms --- (35 questions)
for _ in range(35):
    b1 = random.randint(2, 5)
    b2 = random.randint(2, 5)
    coeff1 = random.randint(2, 4)
    coeff2 = random.randint(2, 4)
    const = random.randint(1, 10)

    p1 = b1**2
    p2 = b2**2
    t1 = coeff1 * p1
    t2 = coeff2 * p2
    op = random.choice(["+", "-"])
    op2 = random.choice(["+", "-"])

    if op == "+":
        intermediate = t1 + t2
    else:
        intermediate = t1 - t2

    if op2 == "+":
        correct = intermediate + const
    else:
        correct = intermediate - const

    expr = f"{coeff1} × {b1}² {op} {coeff2} × {b2}² {op2} {const}"
    expl = (
        f"Exponents: {b1}² = {p1}, {b2}² = {p2}. "
        f"Multiply: {coeff1} × {p1} = {t1}, {coeff2} × {p2} = {t2}. "
        f"Combine: {t1} {op} {t2} = {intermediate}, then {intermediate} {op2} {const} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "exponents", "multi-term"],
        )
    )


# --- Type 5: Complex nested with division --- (25 questions)
for _ in range(25):
    a = random.randint(2, 6)
    b = random.randint(2, 6)
    d = random.randint(2, 5)
    e = random.randint(1, 8)
    divisor = random.randint(2, 5)

    inner = a + b
    product = inner * d
    # Choose c so that (product - c) is divisible by divisor
    # product - c ≡ 0 (mod divisor) → c ≡ product (mod divisor)
    base_c = product % divisor
    if base_c == 0:
        c = divisor  # avoid c=0
    else:
        c = base_c
    # Ensure c is positive and bracket is positive
    bracket = product - c
    while bracket <= 0:
        c -= divisor
        if c <= 0:
            c = base_c + divisor if base_c > 0 else divisor
            bracket = product - c
            break
        bracket = product - c

    # Final safety: verify clean division
    if bracket <= 0 or bracket % divisor != 0:
        # Fallback: construct from desired result
        divided = random.randint(3, 12)
        bracket = divided * divisor
        c = product - bracket
        if c <= 0:
            c = 1
            bracket = product - c
            divisor = 1
            divided = bracket

    divided = bracket // divisor
    correct = divided + e

    expr = f"[({a} + {b}) × {d} - {c}] ÷ {divisor} + {e}"
    expl = (
        f"Innermost: {a} + {b} = {inner}. "
        f"Multiply: {inner} × {d} = {product}. "
        f"Subtract: {product} - {c} = {bracket}. "
        f"Divide: {bracket} ÷ {divisor} = {divided}. "
        f"Add: {divided} + {e} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "nested", "complex expression"],
        )
    )


# --- Type 6: Squared parentheses minus squared parentheses --- (25 questions)
for _ in range(25):
    a = random.randint(3, 9)
    b = random.randint(1, 5)
    c = random.randint(2, 7)
    d = random.randint(1, 4)

    g1 = a + b
    g2 = c + d
    p1 = g1**2
    p2 = g2**2
    correct = p1 - p2

    expr = f"({a} + {b})² - ({c} + {d})²"
    expl = (
        f"First group: {a} + {b} = {g1}, squared: {g1}² = {p1}. "
        f"Second group: {c} + {d} = {g2}, squared: {g2}² = {p2}. "
        f"Subtract: {p1} - {p2} = {correct}."
    )

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            f"What is the value of {expr}?",
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            ["order of operations", "exponents", "parentheses", "difference of squares"],
        )
    )


# --- Type 7: Real-life word problems (Hard) --- (25 questions)
word_problem_templates = [
    {
        "template": "A government office purchases {n1} reams of paper at ₱{p1} each and {n2} ink cartridges at ₱{p2} each. If the total budget is ₱{budget}, how much remains?",
        "gen": lambda: (
            random.randint(5, 15),  # n1
            random.randint(150, 300),  # p1
            random.randint(2, 8),  # n2
            random.randint(500, 1200),  # p2
        ),
        "compute": lambda n1, p1, n2, p2: (n1 * p1 + n2 * p2, 15000),
        "tags": ["word problem", "budgeting", "order of operations"],
    },
    {
        "template": "An employee works {hrs} hours of overtime at ₱{rate} per hour. After a {pct}% tax deduction on overtime pay, what is the net overtime pay?",
        "gen": lambda: (
            random.randint(5, 20),  # hrs
            random.randint(80, 200),  # rate
            random.choice([10, 12, 15, 20]),  # pct
        ),
        "tags": ["word problem", "payroll", "order of operations"],
    },
    {
        "template": "A classroom has {rows} rows of {seats} seats each. If {absent} seats are empty, how many students are present?",
        "gen": lambda: (
            random.randint(4, 8),  # rows
            random.randint(6, 12),  # seats
            random.randint(3, 15),  # absent
        ),
        "tags": ["word problem", "classroom", "order of operations"],
    },
]

for i in range(25):
    idx = i % 3
    if idx == 0:
        n1 = random.randint(5, 15)
        p1 = random.randint(150, 300)
        n2 = random.randint(2, 8)
        p2 = random.randint(500, 1200)
        budget = n1 * p1 + n2 * p2 + random.randint(500, 3000)
        total_cost = n1 * p1 + n2 * p2
        correct = budget - total_cost
        question_text = (
            f"A government office purchases {n1} reams of paper at ₱{p1} each "
            f"and {n2} ink cartridges at ₱{p2} each. If the total budget is "
            f"₱{budget:,}, how much remains after the purchase?"
        )
        expl = (
            f"Paper cost: {n1} × {p1} = {n1 * p1}. "
            f"Ink cost: {n2} × {p2} = {n2 * p2}. "
            f"Total: {n1 * p1} + {n2 * p2} = {total_cost}. "
            f"Remaining: {budget} - {total_cost} = {correct}."
        )
        tags = ["word problem", "budgeting", "order of operations"]
    elif idx == 1:
        hrs = random.randint(5, 20)
        rate = random.randint(80, 200)
        pct = random.choice([10, 12, 15, 20])
        gross = hrs * rate
        tax = gross * pct // 100
        correct = gross - tax
        question_text = (
            f"An employee works {hrs} hours of overtime at ₱{rate} per hour. "
            f"After a {pct}% tax deduction on overtime pay, what is the net overtime pay?"
        )
        expl = (
            f"Gross overtime: {hrs} × {rate} = {gross}. "
            f"Tax: {gross} × {pct}/100 = {tax}. "
            f"Net: {gross} - {tax} = {correct}."
        )
        tags = ["word problem", "payroll", "order of operations"]
    else:
        rows = random.randint(4, 8)
        seats = random.randint(6, 12)
        absent = random.randint(3, 15)
        total = rows * seats
        correct = total - absent
        question_text = (
            f"A classroom has {rows} rows of {seats} seats each. "
            f"If {absent} seats are empty, how many students are present?"
        )
        expl = (
            f"Total seats: {rows} × {seats} = {total}. "
            f"Present: {total} - {absent} = {correct}."
        )
        tags = ["word problem", "classroom", "order of operations"]

    distractors = generate_int_distractors(correct)
    questions.append(
        make_q(
            "Hard",
            question_text,
            shuffle_choices(correct, distractors),
            str(correct),
            expl,
            tags,
        )
    )


# ============================================================
# OUTPUT
# ============================================================

# Trim to exactly 200 per difficulty
easy_qs = [q for q in questions if q["difficulty"] == "Easy"][:200]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"][:200]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"][:200]
questions = easy_qs + medium_qs + hard_qs

# Deduplicate by question text, keeping first occurrence
seen = set()
deduped = []
for q in questions:
    if q["question"] not in seen:
        seen.add(q["question"])
        deduped.append(q)
questions = deduped

easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"After dedup - Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}")

# Pad Easy if needed
while easy_count < 200:
    a = random.randint(5, 30)
    b = random.randint(2, 9)
    c = random.randint(2, 9)
    correct = a + b * c
    q_text = f"What is the value of {a} + {b} × {c}?"
    if q_text in seen:
        continue
    expl = f"Multiplication first: {b} × {c} = {b * c}. Then add: {a} + {b * c} = {correct}."
    distractors = generate_int_distractors(correct)
    q = make_q("Easy", q_text, shuffle_choices(correct, distractors), str(correct), expl,
               ["order of operations", "PEMDAS", "basic"])
    questions.append(q)
    seen.add(q_text)
    easy_count += 1

# Pad Medium if needed
while medium_count < 200:
    a = random.randint(2, 8)
    b = random.randint(2, 8)
    c = random.randint(2, 6)
    d = random.randint(1, 15)
    inside = a + b
    mult = inside * c
    correct = mult - d
    q_text = f"What is the value of ({a} + {b}) × {c} - {d}?"
    if q_text in seen:
        continue
    expl = f"Parentheses: {a} + {b} = {inside}. Multiply: {inside} × {c} = {mult}. Subtract: {mult} - {d} = {correct}."
    distractors = generate_int_distractors(correct)
    q = make_q("Medium", q_text, shuffle_choices(correct, distractors), str(correct), expl,
               ["order of operations", "parentheses", "PEMDAS"])
    questions.append(q)
    seen.add(q_text)
    medium_count += 1

# Pad Hard if needed
while hard_count < 200:
    a = random.randint(2, 5)
    b = random.randint(2, 5)
    d = random.randint(2, 5)
    inner = a + b
    power = inner**2
    result = d * power
    e = random.randint(1, 20)
    correct = result - e
    q_text = f"What is the value of {d} × ({a} + {b})² - {e}?"
    if q_text in seen:
        continue
    expl = (f"Parentheses: {a} + {b} = {inner}. Exponent: {inner}² = {power}. "
            f"Multiply: {d} × {power} = {result}. Subtract: {result} - {e} = {correct}.")
    distractors = generate_int_distractors(correct)
    q = make_q("Hard", q_text, shuffle_choices(correct, distractors), str(correct), expl,
               ["order of operations", "exponents", "nested", "PEMDAS"])
    questions.append(q)
    seen.add(q_text)
    hard_count += 1

# Re-assign IDs sequentially
for i, q in enumerate(questions, start=1):
    q["id"] = i

# Final verification
easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
print(f"Final - Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}")
print(f"Final Total: {len(questions)}")

# Write output
output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "seed", "questions", "numerical-ability", "basic-operations", "order-of-operations",
)
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "questions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Written to: {output_path}")
