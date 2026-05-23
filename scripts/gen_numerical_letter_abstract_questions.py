"""
Generate 600 numerical, letter, and abstract analogy questions.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/word-analogy/numerical-letter-and-abstract-analogies/questions.json
"""
import json
import random
from pathlib import Path

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "word-analogy"
    / "numerical-letter-and-abstract-analogies"
    / "questions.json"
)

B = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Numerical, Letter, and Abstract Analogies",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

random.seed(42)
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def pos(letter: str) -> int:
    return ord(letter.upper()) - ord("A") + 1


def letter_at(p: int) -> str:
    return ALPHA[(p - 1) % 26]


def make_distractors_num(answer: int, count: int = 3) -> list[int]:
    """Generate numeric distractors that are plausible but wrong."""
    candidates = set()
    offsets = [-3, -2, -1, 1, 2, 3, 4, 5, -4, -5]
    for off in offsets:
        v = answer + off
        if v > 0 and v != answer:
            candidates.add(v)
    # Also add some multiplicative distractors
    for mult in [2, 3]:
        if answer // mult > 0 and answer // mult != answer:
            candidates.add(answer // mult)
        if answer * mult // 2 != answer:
            candidates.add(answer + answer // mult if answer // mult > 0 else answer + 2)
    candidates.discard(answer)
    candidates = [c for c in candidates if c > 0]
    random.shuffle(candidates)
    return candidates[:count]


def make_distractors_letter(answer: str, count: int = 3) -> list[str]:
    """Generate letter distractors near the answer."""
    p = pos(answer)
    candidates = set()
    for off in [-2, -1, 1, 2, 3, -3]:
        np = p + off
        if 1 <= np <= 26:
            candidates.add(letter_at(np))
    candidates.discard(answer)
    result = list(candidates)
    random.shuffle(result)
    return result[:count]


def shuffle_choices(choices: list[str], answer: str) -> list[str]:
    """Shuffle choices ensuring answer is included."""
    if answer not in choices:
        choices.append(answer)
    else:
        choices = list(set(choices))
        if answer not in choices:
            choices.append(answer)
    random.shuffle(choices)
    # Ensure exactly 4 choices
    choices = [c for c in choices if c != answer][:3]
    choices.append(answer)
    random.shuffle(choices)
    return choices


# ============================================================
# EASY GENERATORS (200 questions)
# ============================================================

def gen_easy_addition(n: int) -> list[tuple]:
    """Generate easy addition analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 20)
        c = random.randint(2, 20)
        k = random.randint(2, 9)
        b = a + k
        d = c + k
        key = (a, b, c, d)
        if key in used or a == c or b > 50 or d > 50:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = f"{a} plus {k} equals {b}. {c} plus {k} equals {d}. Rule: add {k}."
        questions.append((q, choices, ans, exp, ["number analogy", "addition"]))
    return questions


def gen_easy_subtraction(n: int) -> list[tuple]:
    """Generate easy subtraction analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 9)
        a = random.randint(k + 3, 30)
        c = random.randint(k + 3, 30)
        b = a - k
        d = c - k
        key = (a, b, c, d)
        if key in used or a == c or d < 1:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = f"{a} minus {k} equals {b}. {c} minus {k} equals {d}. Rule: subtract {k}."
        questions.append((q, choices, ans, exp, ["number analogy", "subtraction"]))
    return questions


def gen_easy_multiplication(n: int) -> list[tuple]:
    """Generate easy multiplication analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 6)
        a = random.randint(2, 12)
        c = random.randint(2, 12)
        b = a * k
        d = c * k
        key = (a, b, c, d)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = f"{a} times {k} equals {b}. {c} times {k} equals {d}. Rule: multiply by {k}."
        questions.append((q, choices, ans, exp, ["number analogy", "multiplication"]))
    return questions


def gen_easy_division(n: int) -> list[tuple]:
    """Generate easy division analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 6)
        b_val = random.randint(2, 12)
        d_val = random.randint(2, 12)
        a = b_val * k
        c = d_val * k
        key = (a, b_val, c, d_val)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d_val)
        dists = [str(x) for x in make_distractors_num(d_val)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b_val} :: {c} : ?"
        exp = f"{a} divided by {k} equals {b_val}. {c} divided by {k} equals {d_val}. Rule: divide by {k}."
        questions.append((q, choices, ans, exp, ["number analogy", "division"]))
    return questions


def gen_easy_letter_forward(n: int) -> list[tuple]:
    """Generate easy letter forward-movement analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 5)
        a_pos = random.randint(1, 20)
        c_pos = random.randint(1, 20)
        b_pos = a_pos + k
        d_pos = c_pos + k
        if b_pos > 26 or d_pos > 26 or a_pos == c_pos:
            continue
        key = (a_pos, c_pos, k)
        if key in used:
            continue
        used.add(key)
        a_let = letter_at(a_pos)
        b_let = letter_at(b_pos)
        c_let = letter_at(c_pos)
        d_let = letter_at(d_pos)
        ans = d_let
        dists = make_distractors_letter(ans)
        choices = shuffle_choices(dists, ans)
        q = f"{a_let} : {b_let} :: {c_let} : ?"
        exp = (f"{a_let}({a_pos}) + {k} = {b_let}({b_pos}). "
               f"{c_let}({c_pos}) + {k} = {d_let}({d_pos}). "
               f"Rule: move forward {k} positions.")
        questions.append((q, choices, ans, exp, ["letter analogy", "forward movement"]))
    return questions


def gen_easy_letter_backward(n: int) -> list[tuple]:
    """Generate easy letter backward-movement analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 5)
        a_pos = random.randint(k + 3, 26)
        c_pos = random.randint(k + 3, 26)
        b_pos = a_pos - k
        d_pos = c_pos - k
        if b_pos < 1 or d_pos < 1 or a_pos == c_pos:
            continue
        key = (a_pos, c_pos, k)
        if key in used:
            continue
        used.add(key)
        a_let = letter_at(a_pos)
        b_let = letter_at(b_pos)
        c_let = letter_at(c_pos)
        d_let = letter_at(d_pos)
        ans = d_let
        dists = make_distractors_letter(ans)
        choices = shuffle_choices(dists, ans)
        q = f"{a_let} : {b_let} :: {c_let} : ?"
        exp = (f"{a_let}({a_pos}) - {k} = {b_let}({b_pos}). "
               f"{c_let}({c_pos}) - {k} = {d_let}({d_pos}). "
               f"Rule: move backward {k} positions.")
        questions.append((q, choices, ans, exp, ["letter analogy", "backward movement"]))
    return questions


# ============================================================
# MEDIUM GENERATORS (200 questions)
# ============================================================

def gen_medium_square(n: int) -> list[tuple]:
    """Generate medium squaring analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 12)
        c = random.randint(2, 12)
        b = a * a
        d = c * c
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = f"{a} squared equals {b}. {c} squared equals {d}. Rule: square the number."
        questions.append((q, choices, ans, exp, ["number analogy", "squaring"]))
    return questions


def gen_medium_cube(n: int) -> list[tuple]:
    """Generate medium cubing analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 6)
        c = random.randint(2, 6)
        b = a ** 3
        d = c ** 3
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = f"{a} cubed equals {b}. {c} cubed equals {d}. Rule: cube the number."
        questions.append((q, choices, ans, exp, ["number analogy", "cubing"]))
    return questions


def gen_medium_sqrt(n: int) -> list[tuple]:
    """Generate medium square root analogy questions."""
    questions = []
    perfect_squares = [(i, i*i) for i in range(2, 16)]
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        idx1 = random.randint(0, len(perfect_squares) - 1)
        idx2 = random.randint(0, len(perfect_squares) - 1)
        if idx1 == idx2:
            continue
        root_a, sq_a = perfect_squares[idx1]
        root_c, sq_c = perfect_squares[idx2]
        key = (sq_a, sq_c)
        if key in used:
            continue
        used.add(key)
        ans = str(root_c)
        dists = [str(x) for x in make_distractors_num(root_c)]
        choices = shuffle_choices(dists, ans)
        q = f"{sq_a} : {root_a} :: {sq_c} : ?"
        exp = f"Square root of {sq_a} is {root_a}. Square root of {sq_c} is {root_c}. Rule: take the square root."
        questions.append((q, choices, ans, exp, ["number analogy", "square root"]))
    return questions


def gen_medium_square_plus_k(n: int) -> list[tuple]:
    """Generate medium x^2 + k analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.choice([1, -1, 2, -2])
        a = random.randint(3, 10)
        c = random.randint(3, 10)
        b = a * a + k
        d = c * c + k
        key = (a, c, k)
        if key in used or a == c or d < 1:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        op = f"plus {k}" if k > 0 else f"minus {abs(k)}"
        exp = (f"{a} squared {op} equals {b}. "
               f"{c} squared {op} equals {d}. "
               f"Rule: square then {'add' if k > 0 else 'subtract'} {abs(k)}.")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_medium_n_times_n_plus_1(n: int) -> list[tuple]:
    """Generate medium n*(n+1) analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 10)
        c = random.randint(2, 10)
        b = a * (a + 1)
        d = c * (c + 1)
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = (f"{a} times ({a}+1) equals {b}. "
               f"{c} times ({c}+1) equals {d}. "
               f"Rule: n times (n+1).")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_medium_double_plus_k(n: int) -> list[tuple]:
    """Generate medium 2n+k analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.choice([1, 3, -1])
        a = random.randint(3, 15)
        c = random.randint(3, 15)
        b = 2 * a + k
        d = 2 * c + k
        key = (a, c, k)
        if key in used or a == c or d < 1:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        op = f"plus {k}" if k > 0 else f"minus {abs(k)}"
        exp = (f"{a} times 2 {op} equals {b}. "
               f"{c} times 2 {op} equals {d}. "
               f"Rule: double then {'add' if k > 0 else 'subtract'} {abs(k)}.")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_medium_letter_mirror(n: int) -> list[tuple]:
    """Generate medium alphabet mirror analogy questions (A↔Z, B↔Y, etc.)."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a_pos = random.randint(1, 13)
        c_pos = random.randint(1, 13)
        b_pos = 27 - a_pos
        d_pos = 27 - c_pos
        key = (a_pos, c_pos)
        if key in used or a_pos == c_pos:
            continue
        used.add(key)
        a_let = letter_at(a_pos)
        b_let = letter_at(b_pos)
        c_let = letter_at(c_pos)
        d_let = letter_at(d_pos)
        ans = d_let
        dists = make_distractors_letter(ans)
        choices = shuffle_choices(dists, ans)
        q = f"{a_let} : {b_let} :: {c_let} : ?"
        exp = (f"{a_let}({a_pos}) mirrors to {b_let}({b_pos}), sum=27. "
               f"{c_let}({c_pos}) mirrors to {d_let}({d_pos}), sum=27. "
               f"Rule: alphabet mirror (positions sum to 27).")
        questions.append((q, choices, ans, exp, ["letter analogy", "mirror pattern"]))
    return questions


def gen_medium_letter_pair(n: int) -> list[tuple]:
    """Generate medium paired letter progression (AB : CD :: EF : GH)."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(2, 4)
        a1 = random.randint(1, 18)
        a2 = a1 + 1
        b1 = a1 + k
        b2 = a2 + k
        c1 = random.randint(1, 18)
        c2 = c1 + 1
        d1 = c1 + k
        d2 = c2 + k
        if b1 > 26 or b2 > 26 or d1 > 26 or d2 > 26:
            continue
        if a1 == c1:
            continue
        key = (a1, c1, k)
        if key in used:
            continue
        used.add(key)
        q_pair1 = letter_at(a1) + letter_at(a2)
        q_pair2 = letter_at(b1) + letter_at(b2)
        q_pair3 = letter_at(c1) + letter_at(c2)
        ans = letter_at(d1) + letter_at(d2)
        # Generate distractors
        dist_options = []
        for off in [-1, 1, 2]:
            dd1 = d1 + off
            dd2 = d2 + off
            if 1 <= dd1 <= 26 and 1 <= dd2 <= 26:
                dist_options.append(letter_at(dd1) + letter_at(dd2))
        dist_options = [d for d in dist_options if d != ans][:3]
        while len(dist_options) < 3:
            dist_options.append(letter_at(min(d1+3, 26)) + letter_at(min(d2+3, 26)))
        choices = shuffle_choices(dist_options, ans)
        q = f"{q_pair1} : {q_pair2} :: {q_pair3} : ?"
        exp = (f"Each letter advances by {k}. "
               f"{letter_at(a1)}+{k}={letter_at(b1)}, {letter_at(a2)}+{k}={letter_at(b2)}. "
               f"{letter_at(c1)}+{k}={letter_at(d1)}, {letter_at(c2)}+{k}={letter_at(d2)}. "
               f"Rule: both letters in pair advance by {k}.")
        questions.append((q, choices, ans, exp, ["letter analogy", "paired progression"]))
    return questions


# ============================================================
# HARD GENERATORS (200 questions)
# ============================================================

def gen_hard_cube_plus_k(n: int) -> list[tuple]:
    """Generate hard x^3 + k analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.choice([1, -1, 2, -2])
        a = random.randint(2, 6)
        c = random.randint(2, 6)
        b = a ** 3 + k
        d = c ** 3 + k
        key = (a, c, k)
        if key in used or a == c or d < 1:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        op = f"plus {k}" if k > 0 else f"minus {abs(k)}"
        exp = (f"{a} cubed {op} equals {b}. "
               f"{c} cubed {op} equals {d}. "
               f"Rule: cube then {'add' if k > 0 else 'subtract'} {abs(k)}.")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_hard_n_times_n_minus_1(n: int) -> list[tuple]:
    """Generate hard n*(n-1) analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(3, 12)
        c = random.randint(3, 12)
        b = a * (a - 1)
        d = c * (c - 1)
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = (f"{a} times ({a}-1) equals {b}. "
               f"{c} times ({c}-1) equals {d}. "
               f"Rule: n times (n-1).")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_hard_square_minus_1(n: int) -> list[tuple]:
    """Generate hard n^2 - 1 analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(3, 12)
        c = random.randint(3, 12)
        b = a * a - 1
        d = c * c - 1
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = (f"{a} squared minus 1 equals {b}. "
               f"{c} squared minus 1 equals {d}. "
               f"Rule: n squared minus 1.")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_hard_n_squared_plus_n(n: int) -> list[tuple]:
    """Generate hard n^2 + n analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 10)
        c = random.randint(2, 10)
        b = a * a + a
        d = c * c + c
        key = (a, c)
        if key in used or a == c:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = (f"{a} squared plus {a} equals {b}. "
               f"{c} squared plus {c} equals {d}. "
               f"Rule: n squared plus n (or n times (n+1)).")
        questions.append((q, choices, ans, exp, ["number analogy", "compound rule"]))
    return questions


def gen_hard_letter_converge(n: int) -> list[tuple]:
    """Generate hard converging letter pair (AZ : BY :: CX : DW)."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        # First pair: first letter goes +k, second letter goes -k
        k = random.randint(1, 3)
        a1 = random.randint(1, 10)
        a2 = random.randint(17, 26)
        b1 = a1 + k
        b2 = a2 - k
        c1 = b1 + k
        c2 = b2 - k
        d1 = c1 + k
        d2 = c2 - k
        if d1 > 26 or d2 < 1 or c1 > 26 or c2 < 1:
            continue
        key = (a1, a2, k)
        if key in used:
            continue
        used.add(key)
        pair1 = letter_at(a1) + letter_at(a2)
        pair2 = letter_at(b1) + letter_at(b2)
        pair3 = letter_at(c1) + letter_at(c2)
        ans = letter_at(d1) + letter_at(d2)
        # Distractors
        dist_options = []
        for off in [-1, 1, 2]:
            dd1 = d1 + off
            dd2 = d2 + off
            if 1 <= dd1 <= 26 and 1 <= dd2 <= 26:
                dist_options.append(letter_at(dd1) + letter_at(dd2))
        for off in [1, -1]:
            dd1 = d1 + off
            dd2 = d2 - off
            if 1 <= dd1 <= 26 and 1 <= dd2 <= 26:
                dist_options.append(letter_at(dd1) + letter_at(dd2))
        dist_options = [d for d in dist_options if d != ans][:3]
        while len(dist_options) < 3:
            dist_options.append(letter_at(min(d1+2, 26)) + letter_at(max(d2-2, 1)))
        choices = shuffle_choices(dist_options, ans)
        q = f"{pair1} : {pair2} :: {pair3} : ?"
        exp = (f"First letter +{k}, second letter -{k}. "
               f"{letter_at(a1)}+{k}={letter_at(b1)}, {letter_at(a2)}-{k}={letter_at(b2)}. "
               f"{letter_at(c1)}+{k}={letter_at(d1)}, {letter_at(c2)}-{k}={letter_at(d2)}. "
               f"Rule: converging pattern (first advances, second retreats by {k}).")
        questions.append((q, choices, ans, exp, ["letter analogy", "compound pattern"]))
    return questions

def gen_hard_letter_large_skip(n: int) -> list[tuple]:
    """Generate hard letter analogy with larger skips (5-8 positions)."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        k = random.randint(5, 8)
        a_pos = random.randint(1, 18)
        c_pos = random.randint(1, 18)
        b_pos = a_pos + k
        d_pos = c_pos + k
        if b_pos > 26 or d_pos > 26 or a_pos == c_pos:
            continue
        key = (a_pos, c_pos, k)
        if key in used:
            continue
        used.add(key)
        a_let = letter_at(a_pos)
        b_let = letter_at(b_pos)
        c_let = letter_at(c_pos)
        d_let = letter_at(d_pos)
        ans = d_let
        dists = make_distractors_letter(ans)
        choices = shuffle_choices(dists, ans)
        q = f"{a_let} : {b_let} :: {c_let} : ?"
        exp = (f"{a_let}({a_pos}) + {k} = {b_let}({b_pos}). "
               f"{c_let}({c_pos}) + {k} = {d_let}({d_pos}). "
               f"Rule: move forward {k} positions.")
        questions.append((q, choices, ans, exp, ["letter analogy", "large skip"]))
    return questions


def gen_hard_n_cubed_minus_n(n: int) -> list[tuple]:
    """Generate hard n^3 - n analogy questions."""
    questions = []
    used = set()
    attempts = 0
    while len(questions) < n and attempts < n * 10:
        attempts += 1
        a = random.randint(2, 7)
        c = random.randint(2, 7)
        b = a ** 3 - a
        d = c ** 3 - c
        key = (a, c)
        if key in used or a == c or d < 1:
            continue
        used.add(key)
        ans = str(d)
        dists = [str(x) for x in make_distractors_num(d)]
        choices = shuffle_choices(dists, ans)
        q = f"{a} : {b} :: {c} : ?"
        exp = (f"{a} cubed minus {a} equals {b}. "
               f"{c} cubed minus {c} equals {d}. "
               f"Rule: n cubed minus n.")
        questions.append((q, choices, ans, exp, ["number analogy", "advanced compound"]))
    return questions


# ============================================================
# ABSTRACT / SYMBOLIC (static hand-crafted questions)
# ============================================================

# fmt: off
ABSTRACT_EASY = [
("morning : evening :: beginning : ?",["middle","ending","starting","continuing"],"ending","Morning is the start of day, evening is the end. Beginning is the start, ending is the finish. Rule: start-to-end relationship.",["abstract analogy","temporal"]),
("question : answer :: problem : ?",["difficulty","solution","challenge","issue"],"solution","A question leads to an answer. A problem leads to a solution. Rule: problem-to-resolution.",["abstract analogy","process"]),
("winter : summer :: night : ?",["dark","day","moon","evening"],"day","Winter is the opposite season of summer. Night is the opposite of day. Rule: temporal opposites.",["abstract analogy","opposites"]),
("up : down :: left : ?",["side","right","forward","back"],"right","Up is the opposite of down. Left is the opposite of right. Rule: directional opposites.",["abstract analogy","direction"]),
("open : close :: start : ?",["begin","stop","run","go"],"stop","Open is the opposite of close. Start is the opposite of stop. Rule: action opposites.",["abstract analogy","opposites"]),
("hot : cold :: fast : ?",["quick","slow","speed","run"],"slow","Hot is the opposite of cold. Fast is the opposite of slow. Rule: quality opposites.",["abstract analogy","opposites"]),
("in : out :: above : ?",["over","below","up","high"],"below","In is the opposite of out. Above is the opposite of below. Rule: positional opposites.",["abstract analogy","direction"]),
("first : last :: top : ?",["high","bottom","upper","peak"],"bottom","First is the opposite of last. Top is the opposite of bottom. Rule: positional extremes.",["abstract analogy","opposites"]),
("before : after :: past : ?",["history","future","present","old"],"future","Before relates to after as past relates to future. Rule: temporal sequence.",["abstract analogy","temporal"]),
("cause : effect :: action : ?",["doing","reaction","movement","force"],"reaction","A cause produces an effect. An action produces a reaction. Rule: cause-to-result.",["abstract analogy","process"]),
]

ABSTRACT_MEDIUM = [
("seed : tree :: egg : ?",["nest","bird","shell","yolk"],"bird","A seed grows into a tree. An egg develops into a bird. Rule: origin-to-mature form.",["abstract analogy","transformation"]),
("blueprint : building :: recipe : ?",["kitchen","meal","ingredient","cook"],"meal","A blueprint guides building construction. A recipe guides meal preparation. Rule: plan-to-product.",["abstract analogy","process"]),
("rehearsal : performance :: practice : ?",["skill","exam","training","study"],"exam","A rehearsal prepares for a performance. Practice prepares for an exam. Rule: preparation-to-event.",["abstract analogy","sequence"]),
("symptom : diagnosis :: clue : ?",["mystery","solution","detective","crime"],"solution","A symptom leads to a diagnosis. A clue leads to a solution. Rule: evidence-to-conclusion.",["abstract analogy","process"]),
("raw : cooked :: rough : ?",["hard","polished","tough","crude"],"polished","Raw becomes cooked through processing. Rough becomes polished through refinement. Rule: unprocessed-to-refined.",["abstract analogy","transformation"]),
("input : output :: stimulus : ?",["nerve","response","brain","sense"],"response","Input produces output. A stimulus produces a response. Rule: trigger-to-result.",["abstract analogy","process"]),
("draft : final :: sketch : ?",["drawing","painting","pencil","canvas"],"painting","A draft becomes a final version. A sketch becomes a painting. Rule: preliminary-to-finished.",["abstract analogy","sequence"]),
("shallow : deep :: simple : ?",["easy","complex","basic","plain"],"complex","Shallow is the opposite of deep. Simple is the opposite of complex. Rule: degree opposites.",["abstract analogy","opposites"]),
("chaos : order :: conflict : ?",["war","peace","fight","battle"],"peace","Chaos is the opposite of order. Conflict is the opposite of peace. Rule: state opposites.",["abstract analogy","opposites"]),
("theory : practice :: plan : ?",["idea","execution","thought","design"],"execution","Theory is applied through practice. A plan is applied through execution. Rule: concept-to-application.",["abstract analogy","process"]),
]

ABSTRACT_HARD = [
("hypothesis : conclusion :: premise : ?",["argument","deduction","assumption","logic"],"deduction","A hypothesis leads to a conclusion through testing. A premise leads to a deduction through reasoning. Rule: starting point to derived result.",["abstract analogy","logic"]),
("catalyst : reaction :: stimulus : ?",["nerve","response","energy","force"],"response","A catalyst triggers a reaction. A stimulus triggers a response. Rule: trigger-to-outcome.",["abstract analogy","process"]),
("correlation : causation :: suspicion : ?",["doubt","proof","guess","theory"],"proof","Correlation suggests but doesn't confirm; causation confirms. Suspicion suggests; proof confirms. Rule: weak evidence to strong evidence.",["abstract analogy","logic"]),
("entropy : order :: inflation : ?",["money","stability","prices","economy"],"stability","Entropy disrupts order. Inflation disrupts stability. Rule: disruptive force to disrupted state.",["abstract analogy","opposites"]),
("abstraction : implementation :: design : ?",["plan","construction","idea","model"],"construction","Abstraction becomes implementation. Design becomes construction. Rule: concept-to-realization.",["abstract analogy","process"]),
("analysis : synthesis :: deconstruction : ?",["destruction","creation","breakdown","parts"],"creation","Analysis breaks down; synthesis builds up. Deconstruction breaks down; creation builds up. Rule: opposing intellectual processes.",["abstract analogy","opposites"]),
("axiom : theorem :: foundation : ?",["base","structure","ground","building"],"structure","An axiom supports a theorem. A foundation supports a structure. Rule: base-to-supported entity.",["abstract analogy","logic"]),
("induction : deduction :: specific : ?",["particular","general","detail","individual"],"general","Induction goes from specific to general. The opposite direction: specific relates to general. Rule: reasoning direction.",["abstract analogy","logic"]),
("potential : kinetic :: stored : ?",["saved","released","kept","held"],"released","Potential energy becomes kinetic energy. Stored energy becomes released energy. Rule: latent-to-active state.",["abstract analogy","transformation"]),
("microscope : cell :: telescope : ?",["lens","star","sky","space"],"star","A microscope reveals cells. A telescope reveals stars. Rule: instrument-to-revealed object.",["abstract analogy","tool-function"]),
]

SYMBOLIC_EASY = [
("+ : - :: x : ?",["÷","+","=","%"],"÷","Addition is the inverse of subtraction. Multiplication is the inverse of division. Rule: inverse operations.",["symbolic analogy","math operations"]),
("( : ) :: [ : ?",["(","<","]","{"],"]","Opening parenthesis pairs with closing parenthesis. Opening bracket pairs with closing bracket. Rule: opening-to-closing.",["symbolic analogy","brackets"]),
("1 : 1st :: 2 : ?",["2nd","two","second","II"],"2nd","1 becomes 1st (ordinal). 2 becomes 2nd (ordinal). Rule: cardinal to ordinal.",["symbolic analogy","number forms"]),
("< : > :: { : ?",["(","[","}","<"],"}","Less-than pairs with greater-than. Opening brace pairs with closing brace. Rule: opening-to-closing symbol.",["symbolic analogy","brackets"]),
("AM : PM :: sunrise : ?",["morning","sunset","noon","night"],"sunset","AM is the first half of day, PM is the second. Sunrise is the start, sunset is the end. Rule: day-half pairing.",["symbolic analogy","temporal"]),
]

SYMBOLIC_MEDIUM = [
("I : IV :: V : ?",["VI","VIII","IX","X"],"VIII","Roman numeral I + 3 = IV. V + 3 = VIII. Rule: add 3 in Roman numerals.",["symbolic analogy","roman numerals"]),
("cm : m :: mm : ?",["km","cm","dm","m"],"cm","Centimeters are 1/100 of meters. Millimeters are 1/10 of centimeters. Rule: smaller unit to next larger unit.",["symbolic analogy","measurement"]),
("H2O : water :: NaCl : ?",["sugar","salt","acid","gas"],"salt","H2O is the formula for water. NaCl is the formula for salt. Rule: chemical formula to common name.",["symbolic analogy","science"]),
("binary : 2 :: decimal : ?",["1","5","10","100"],"10","Binary is base 2. Decimal is base 10. Rule: number system to its base.",["symbolic analogy","number systems"]),
("% : 100 :: ‰ : ?",["10","1000","500","50"],"1000","Percent means per 100. Per mille means per 1000. Rule: symbol to denominator.",["symbolic analogy","math symbols"]),
]

SYMBOLIC_HARD = [
("π : circle :: e : ?",["square","growth","line","angle"],"growth","Pi is the fundamental constant of circles. Euler's number e is the fundamental constant of exponential growth. Rule: constant to its domain.",["symbolic analogy","math constants"]),
("∑ : sum :: ∏ : ?",["difference","product","quotient","integral"],"product","Sigma (∑) represents summation. Pi (∏) represents product. Rule: symbol to operation.",["symbolic analogy","math notation"]),
("∞ : finite :: 0 : ?",["nothing","nonzero","empty","null"],"nonzero","Infinity is the opposite of finite. Zero is the opposite of nonzero. Rule: mathematical opposites.",["symbolic analogy","math concepts"]),
("√ : square :: ∛ : ?",["cube","triangle","third","root"],"cube","Square root undoes squaring. Cube root undoes cubing. Rule: inverse operation pairing.",["symbolic analogy","math operations"]),
("dx : derivative :: ∫ : ?",["integral","sum","limit","function"],"integral","dx notation relates to derivatives. The integral sign relates to integrals. Rule: notation to operation.",["symbolic analogy","calculus"]),
]
# fmt: on


# ============================================================
# ASSEMBLY AND OUTPUT
# ============================================================

def build_questions() -> list[dict]:
    """Generate all 600 questions: 200 Easy, 200 Medium, 200 Hard."""

    # --- EASY (200) ---
    # 40 addition + 30 subtraction + 40 multiplication + 30 division
    # + 30 letter forward + 20 letter backward + 10 abstract/symbolic
    easy_qs = []
    easy_qs.extend(gen_easy_addition(40))
    easy_qs.extend(gen_easy_subtraction(30))
    easy_qs.extend(gen_easy_multiplication(40))
    easy_qs.extend(gen_easy_division(30))
    easy_qs.extend(gen_easy_letter_forward(30))
    easy_qs.extend(gen_easy_letter_backward(20))
    # Add static abstract/symbolic easy
    for item in ABSTRACT_EASY:
        easy_qs.append(item)
    for item in SYMBOLIC_EASY:
        easy_qs.append(item)
    # Trim or pad to exactly 200
    random.shuffle(easy_qs)
    easy_qs = easy_qs[:200]

    # --- MEDIUM (200) ---
    # 20 square + 10 cube + 15 sqrt + 25 square+k + 20 n*(n+1)
    # + 20 double+k + 15 mirror + 20 letter pair
    # + 10 abstract + 5 symbolic + fill remainder
    medium_qs = []
    medium_qs.extend(gen_medium_square(20))
    medium_qs.extend(gen_medium_cube(10))
    medium_qs.extend(gen_medium_sqrt(15))
    medium_qs.extend(gen_medium_square_plus_k(25))
    medium_qs.extend(gen_medium_n_times_n_plus_1(20))
    medium_qs.extend(gen_medium_double_plus_k(20))
    medium_qs.extend(gen_medium_letter_mirror(15))
    medium_qs.extend(gen_medium_letter_pair(20))
    # Add static abstract/symbolic medium
    for item in ABSTRACT_MEDIUM:
        medium_qs.append(item)
    for item in SYMBOLIC_MEDIUM:
        medium_qs.append(item)
    # Fill remainder with more compound questions
    remaining = 200 - len(medium_qs)
    if remaining > 0:
        medium_qs.extend(gen_medium_square_plus_k(remaining))
    random.shuffle(medium_qs)
    medium_qs = medium_qs[:200]

    # --- HARD (200) ---
    # 20 cube+k + 25 n*(n-1) + 25 n^2-1 + 25 n^2+n
    # + 25 converge + 25 large skip + 20 n^3-n
    # + 10 abstract + 5 symbolic + fill remainder
    hard_qs = []
    hard_qs.extend(gen_hard_cube_plus_k(20))
    hard_qs.extend(gen_hard_n_times_n_minus_1(25))
    hard_qs.extend(gen_hard_square_minus_1(25))
    hard_qs.extend(gen_hard_n_squared_plus_n(25))
    hard_qs.extend(gen_hard_letter_converge(25))
    hard_qs.extend(gen_hard_letter_large_skip(25))
    hard_qs.extend(gen_hard_n_cubed_minus_n(20))
    # Add static abstract/symbolic hard
    for item in ABSTRACT_HARD:
        hard_qs.append(item)
    for item in SYMBOLIC_HARD:
        hard_qs.append(item)
    # Fill remainder
    remaining = 200 - len(hard_qs)
    if remaining > 0:
        hard_qs.extend(gen_hard_n_times_n_minus_1(remaining))
    random.shuffle(hard_qs)
    hard_qs = hard_qs[:200]

    # --- Build final JSON list ---
    all_questions = []
    id_counter = 1

    for difficulty, q_list in [("Easy", easy_qs), ("Medium", medium_qs), ("Hard", hard_qs)]:
        for item in q_list:
            question_text, choices, answer, explanation, tags = item
            all_questions.append({
                "id": id_counter,
                **B,
                "difficulty": difficulty,
                "question": question_text,
                "choices": choices,
                "answer": answer,
                "explanation": explanation,
                "tags": ["word analogy"] + tags,
            })
            id_counter += 1

    return all_questions


def main():
    questions = build_questions()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {len(questions)} questions -> {OUTPUT}")
    # Verify distribution
    easy = sum(1 for q in questions if q["difficulty"] == "Easy")
    medium = sum(1 for q in questions if q["difficulty"] == "Medium")
    hard = sum(1 for q in questions if q["difficulty"] == "Hard")
    print(f"  Easy: {easy} | Medium: {medium} | Hard: {hard}")


if __name__ == "__main__":
    main()
