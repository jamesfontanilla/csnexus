"""Generate 600 questions for the Exponents and Roots subtopic.

Produces exactly 200 Easy, 200 Medium, 200 Hard questions covering:
- Laws of exponents
- Square roots and cube roots
- Radical simplification
- Scientific notation
- Rational exponents
- Mixed operations
- Estimation
- Real-life applications

Usage:
    python -m scripts.gen_exponents_roots_questions
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "seed"
    / "questions"
    / "numerical-ability"
    / "basic-operations"
    / "exponents-and-roots"
    / "questions.json"
)

TEMPLATE = {
    "subtest": "Numerical Ability",
    "module": "Basic Operations",
    "subtopic": "Exponents and Roots",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}


def _q(
    qid: int,
    difficulty: str,
    question: str,
    choices: list[str],
    answer: str,
    explanation: str,
    tags: list[str],
) -> dict:
    return {
        **TEMPLATE,
        "id": qid,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


def _shuffle_choices(correct: str, distractors: list[str]) -> list[str]:
    """Return shuffled choices with correct answer included.

    Guarantees exactly 4 unique choices. If distractors contain duplicates
    or match the correct answer, generates numeric offsets as replacements.
    """
    # Deduplicate distractors and remove any that match correct
    unique = []
    seen = {correct}
    for d in distractors:
        if d not in seen:
            unique.append(d)
            seen.add(d)
        if len(unique) == 3:
            break

    # If we still need more distractors, generate numeric offsets
    offset = 1
    while len(unique) < 3:
        # Try to create a plausible distractor based on the correct answer
        try:
            val = int(correct)
            candidate = str(val + offset * random.choice([-1, 1]) * random.randint(2, 10))
        except ValueError:
            candidate = f"{correct}_alt{offset}"
        if candidate not in seen:
            unique.append(candidate)
            seen.add(candidate)
        offset += 1
        if offset > 50:  # safety valve
            unique.append(f"N/A_{offset}")
            break

    choices = [correct] + unique[:3]
    random.shuffle(choices)
    return choices


def generate_easy_questions(start_id: int) -> list[dict]:
    """Generate 200 Easy questions."""
    questions: list[dict] = []
    qid = start_id

    # --- Block 1: Basic power evaluation (40 questions) ---
    power_data = [
        (2, 3, 8), (2, 4, 16), (2, 5, 32), (2, 6, 64), (2, 7, 128),
        (2, 8, 256), (2, 9, 512), (2, 10, 1024),
        (3, 2, 9), (3, 3, 27), (3, 4, 81), (3, 5, 243),
        (4, 2, 16), (4, 3, 64), (4, 4, 256),
        (5, 2, 25), (5, 3, 125), (5, 4, 625),
        (6, 2, 36), (6, 3, 216), (7, 2, 49), (7, 3, 343),
        (8, 2, 64), (8, 3, 512), (9, 2, 81), (9, 3, 729),
        (10, 2, 100), (10, 3, 1000), (10, 4, 10000), (10, 5, 100000),
        (11, 2, 121), (12, 2, 144), (13, 2, 169), (14, 2, 196),
        (15, 2, 225), (16, 2, 256), (17, 2, 289), (18, 2, 324),
        (19, 2, 361), (20, 2, 400),
    ]
    for base, exp, ans in power_data:
        correct = str(ans)
        d1 = str(base * exp)
        d2 = str(ans + base)
        d3 = str(ans - base if ans - base > 0 else ans + exp)
        distractors = list({d1, d2, d3} - {correct})
        while len(distractors) < 3:
            distractors.append(str(ans + random.choice([1, 2, 3, -1, -2]) * random.randint(1, 5)))
        distractors = [d for d in distractors if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Easy",
            f"What is {base}^{exp}?",
            choices, correct,
            f"{base}^{exp} means {base} multiplied by itself {exp} times: {base}^{exp} = {ans}.",
            ["exponents", "powers", "basic computation"],
        ))
        qid += 1

    # --- Block 2: Perfect square roots (30 questions) ---
    squares = [(n, n*n) for n in range(1, 26)] + [(30, 900), (40, 1600), (50, 2500), (60, 3600), (100, 10000)]
    for root, sq in squares[:30]:
        correct = str(root)
        distractors = [str(root + 1), str(root - 1 if root > 1 else root + 2), str(sq // root if root != 0 else 2)]
        distractors = [d for d in distractors if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(str(root + random.randint(2, 5)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Easy",
            f"What is √{sq}?",
            choices, correct,
            f"√{sq} = {root} because {root}² = {root} × {root} = {sq}.",
            ["square roots", "perfect squares"],
        ))
        qid += 1

    # --- Block 3: Perfect cube roots (20 questions) ---
    cubes = [(n, n**3) for n in range(1, 11)] + [(11, 1331), (12, 1728), (15, 3375), (20, 8000)]
    for root, cb in cubes[:20]:
        correct = str(root)
        distractors = [str(root + 1), str(root - 1 if root > 1 else root + 2), str(root + 3)]
        distractors = [d for d in distractors if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Easy",
            f"What is ∛{cb}?",
            choices, correct,
            f"∛{cb} = {root} because {root}³ = {root} × {root} × {root} = {cb}.",
            ["cube roots", "perfect cubes"],
        ))
        qid += 1

    # --- Block 4: Zero exponent (15 questions) ---
    zero_bases = [2, 3, 5, 7, 10, 15, 25, 50, 100, 999, 1000, 47, 83, 256, 1024]
    for base in zero_bases:
        correct = "1"
        distractors = ["0", str(base), str(base - 1)]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Easy",
            f"What is {base}⁰?",
            choices, correct,
            f"Any non-zero number raised to the power of zero equals 1. Therefore {base}⁰ = 1.",
            ["zero exponent", "exponent rules"],
        ))
        qid += 1

    # --- Block 5: Negative exponents (basic) (20 questions) ---
    neg_exp_data = [
        (2, 1, 2, "1/2"), (2, 2, 4, "1/4"), (2, 3, 8, "1/8"),
        (2, 4, 16, "1/16"), (2, 5, 32, "1/32"),
        (3, 1, 3, "1/3"), (3, 2, 9, "1/9"), (3, 3, 27, "1/27"),
        (4, 1, 4, "1/4"), (4, 2, 16, "1/16"),
        (5, 1, 5, "1/5"), (5, 2, 25, "1/25"), (5, 3, 125, "1/125"),
        (10, 1, 10, "1/10"), (10, 2, 100, "1/100"),
        (10, 3, 1000, "1/1000"), (6, 2, 36, "1/36"),
        (7, 2, 49, "1/49"), (8, 2, 64, "1/64"), (9, 2, 81, "1/81"),
    ]
    for base, exp, denom, ans_str in neg_exp_data:
        correct = ans_str
        distractors = [f"-{denom}", str(denom), f"-{ans_str}"]
        distractors = [d for d in distractors if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Easy",
            f"What is {base}^(-{exp})?",
            choices, correct,
            f"A negative exponent means reciprocal: {base}^(-{exp}) = 1/{base}^{exp} = 1/{denom} = {ans_str}.",
            ["negative exponents", "reciprocals"],
        ))
        qid += 1

    # --- Block 6: Product rule (same base) (20 questions) ---
    prod_data = [
        (2, 3, 4, 7, 128), (2, 5, 3, 8, 256), (3, 2, 3, 5, 243),
        (3, 4, 2, 6, 729), (5, 2, 2, 4, 625), (5, 1, 3, 4, 625),
        (10, 2, 3, 5, 100000), (10, 4, 2, 6, 1000000),
        (2, 2, 2, 4, 16), (2, 6, 2, 8, 256),
        (4, 2, 3, 5, 1024), (3, 3, 3, 6, 729),
        (7, 1, 2, 3, 343), (6, 1, 2, 3, 216),
        (2, 4, 3, 7, 128), (5, 3, 1, 4, 625),
        (10, 1, 4, 5, 100000), (2, 1, 9, 10, 1024),
        (3, 1, 4, 5, 243), (4, 1, 2, 3, 64),
    ]
    for base, e1, e2, esum, ans in prod_data:
        correct = str(ans)
        distractors = [str(base**(e1*e2)), str(base**e1 + base**e2), str(ans // base)]
        distractors = [d for d in distractors if d != correct and d != "1"][:3]
        while len(distractors) < 3:
            distractors.append(str(ans + random.choice([-1, 1]) * random.randint(1, 20)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Easy",
            f"Simplify: {base}^{e1} × {base}^{e2}",
            choices, correct,
            f"Product rule: {base}^{e1} × {base}^{e2} = {base}^({e1}+{e2}) = {base}^{esum} = {ans}.",
            ["product of powers", "exponent rules"],
        ))
        qid += 1

    # --- Block 7: Quotient rule (same base) (20 questions) ---
    quot_data = [
        (2, 7, 3, 4, 16), (2, 8, 5, 3, 8), (2, 10, 7, 3, 8),
        (3, 5, 2, 3, 27), (3, 6, 4, 2, 9), (3, 4, 1, 3, 27),
        (5, 4, 2, 2, 25), (5, 3, 1, 2, 25), (5, 5, 3, 2, 25),
        (10, 6, 3, 3, 1000), (10, 5, 2, 3, 1000), (10, 8, 5, 3, 1000),
        (4, 3, 1, 2, 16), (4, 4, 2, 2, 16), (6, 3, 1, 2, 36),
        (7, 4, 2, 2, 49), (2, 6, 4, 2, 4), (2, 5, 2, 3, 8),
        (10, 4, 1, 3, 1000), (3, 3, 1, 2, 9),
    ]
    for base, e1, e2, ediff, ans in quot_data:
        correct = str(ans)
        distractors = [str(base**(e1+e2)), str(base**(e1*e2) if e1*e2 < 10 else ans*2), str(ans * base)]
        distractors = [d for d in distractors if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(str(ans + random.choice([-1, 1]) * random.randint(2, 15)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Easy",
            f"Simplify: {base}^{e1} ÷ {base}^{e2}",
            choices, correct,
            f"Quotient rule: {base}^{e1} ÷ {base}^{e2} = {base}^({e1}-{e2}) = {base}^{ediff} = {ans}.",
            ["quotient of powers", "exponent rules"],
        ))
        qid += 1

    # --- Block 8: Scientific notation identification (20 questions) ---
    sci_data = [
        (3500, "3.5 × 10³"), (45000, "4.5 × 10⁴"), (670000, "6.7 × 10⁵"),
        (8900000, "8.9 × 10⁶"), (120000, "1.2 × 10⁵"), (5600, "5.6 × 10³"),
        (91000, "9.1 × 10⁴"), (2300000, "2.3 × 10⁶"), (780, "7.8 × 10²"),
        (34000000, "3.4 × 10⁷"), (560000000, "5.6 × 10⁸"), (1200, "1.2 × 10³"),
        (99000, "9.9 × 10⁴"), (4100, "4.1 × 10³"), (250000, "2.5 × 10⁵"),
        (73000, "7.3 × 10⁴"), (8100, "8.1 × 10³"), (620000, "6.2 × 10⁵"),
        (15000, "1.5 × 10⁴"), (990000, "9.9 × 10⁵"),
    ]
    for num, sci in sci_data:
        correct = sci
        # Generate plausible wrong answers by changing exponent or coefficient
        parts = sci.split(" × 10")
        coeff = parts[0]
        exp_str = parts[1]
        exp_val = int(exp_str.replace("⁰","0").replace("¹","1").replace("²","2").replace("³","3").replace("⁴","4").replace("⁵","5").replace("⁶","6").replace("⁷","7").replace("⁸","8").replace("⁹","9"))
        sup_map = {0:"⁰",1:"¹",2:"²",3:"³",4:"⁴",5:"⁵",6:"⁶",7:"⁷",8:"⁸",9:"⁹"}
        def to_sup(n):
            if n < 0:
                return "⁻" + "".join(sup_map[int(d)] for d in str(abs(n)))
            return "".join(sup_map[int(d)] for d in str(n))
        d1 = f"{coeff} × 10{to_sup(exp_val + 1)}"
        d2 = f"{coeff} × 10{to_sup(exp_val - 1)}"
        d3 = f"{float(coeff)*10:.1f} × 10{to_sup(exp_val - 1)}"
        distractors = [d for d in [d1, d2, d3] if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Easy",
            f"Express {num:,} in scientific notation.",
            choices, correct,
            f"Move the decimal point until the coefficient is between 1 and 10. {num:,} = {sci}.",
            ["scientific notation", "powers of 10"],
        ))
        qid += 1

    # --- Block 9: Power of a power (21 questions) ---
    pop_data = [
        (2, 2, 3, 6, 64), (2, 3, 2, 6, 64), (3, 2, 2, 4, 81),
        (3, 2, 3, 6, 729), (2, 4, 2, 8, 256), (5, 2, 2, 4, 625),
        (10, 2, 2, 4, 10000), (10, 3, 2, 6, 1000000),
        (2, 2, 4, 8, 256), (2, 3, 3, 9, 512), (3, 1, 4, 4, 81),
        (4, 2, 2, 4, 256), (2, 5, 2, 10, 1024), (5, 1, 3, 3, 125),
        (10, 1, 3, 3, 1000), (2, 2, 5, 10, 1024), (3, 3, 2, 6, 729),
        (6, 1, 3, 3, 216), (7, 1, 2, 2, 49), (2, 1, 6, 6, 64),
        (5, 2, 3, 6, 15625),
    ]
    for base, e1, e2, eprod, ans in pop_data:
        correct = str(ans)
        wrong_add = base**(e1+e2) if (e1+e2) <= 10 else ans + 100
        distractors = [str(wrong_add), str(ans * 2), str(ans // 2 if ans > 2 else ans + 5)]
        distractors = [d for d in distractors if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(str(ans + random.randint(1, 20)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Easy",
            f"Simplify: ({base}^{e1})^{e2}",
            choices, correct,
            f"Power of a power rule: ({base}^{e1})^{e2} = {base}^({e1}×{e2}) = {base}^{eprod} = {ans}.",
            ["power of a power", "exponent rules"],
        ))
        qid += 1

    return questions


def generate_medium_questions(start_id: int) -> list[dict]:
    """Generate 200 Medium questions."""
    questions: list[dict] = []
    qid = start_id

    # --- Block 1: Simplify radical expressions (30 questions) ---
    radical_data = [
        (50, 5, 2, "5√2"), (72, 6, 2, "6√2"), (98, 7, 2, "7√2"),
        (200, 10, 2, "10√2"), (128, 8, 2, "8√2"), (32, 4, 2, "4√2"),
        (18, 3, 2, "3√2"), (8, 2, 2, "2√2"),
        (75, 5, 3, "5√3"), (48, 4, 3, "4√3"), (27, 3, 3, "3√3"),
        (12, 2, 3, "2√3"), (108, 6, 3, "6√3"), (147, 7, 3, "7√3"),
        (300, 10, 3, "10√3"),
        (45, 3, 5, "3√5"), (80, 4, 5, "4√5"), (125, 5, 5, "5√5"),
        (20, 2, 5, "2√5"), (180, 6, 5, "6√5"),
        (28, 2, 7, "2√7"), (63, 3, 7, "3√7"), (112, 4, 7, "4√7"),
        (44, 2, 11, "2√11"), (99, 3, 11, "3√11"),
        (52, 2, 13, "2√13"), (150, 5, 6, "5√6"),
        (162, 9, 2, "9√2"), (242, 11, 2, "11√2"), (288, 12, 2, "12√2"),
    ]
    for radicand, coeff, inner, ans_str in radical_data:
        correct = ans_str
        # Generate plausible wrong answers
        d1 = f"{coeff + 1}√{inner}"
        d2 = f"{coeff - 1}√{inner}" if coeff > 1 else f"{coeff}√{inner + 1}"
        d3 = f"{coeff}√{inner + 1}" if inner < 13 else f"{coeff + 2}√{inner}"
        distractors = [d for d in [d1, d2, d3] if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Medium",
            f"Simplify: √{radicand}",
            choices, correct,
            f"√{radicand} = √({coeff**2} × {inner}) = {coeff}√{inner}.",
            ["radicals", "simplification", "square roots"],
        ))
        qid += 1

    # --- Block 2: Rational exponents evaluation (25 questions) ---
    rat_exp_data = [
        ("8^(2/3)", 4, "∛8 = 2, then 2² = 4"),
        ("27^(2/3)", 9, "∛27 = 3, then 3² = 9"),
        ("16^(3/4)", 8, "⁴√16 = 2, then 2³ = 8"),
        ("32^(2/5)", 4, "⁵√32 = 2, then 2² = 4"),
        ("64^(2/3)", 16, "∛64 = 4, then 4² = 16"),
        ("125^(2/3)", 25, "∛125 = 5, then 5² = 25"),
        ("81^(3/4)", 27, "⁴√81 = 3, then 3³ = 27"),
        ("4^(5/2)", 32, "√4 = 2, then 2⁵ = 32"),
        ("9^(3/2)", 27, "√9 = 3, then 3³ = 27"),
        ("25^(3/2)", 125, "√25 = 5, then 5³ = 125"),
        ("16^(5/4)", 32, "⁴√16 = 2, then 2⁵ = 32"),
        ("8^(4/3)", 16, "∛8 = 2, then 2⁴ = 16"),
        ("27^(4/3)", 81, "∛27 = 3, then 3⁴ = 81"),
        ("64^(1/2)", 8, "√64 = 8"),
        ("64^(1/3)", 4, "∛64 = 4"),
        ("64^(5/6)", 32, "⁶√64 = 2, then 2⁵ = 32"),
        ("100^(3/2)", 1000, "√100 = 10, then 10³ = 1000"),
        ("49^(3/2)", 343, "√49 = 7, then 7³ = 343"),
        ("36^(3/2)", 216, "√36 = 6, then 6³ = 216"),
        ("4^(3/2)", 8, "√4 = 2, then 2³ = 8"),
        ("9^(5/2)", 243, "√9 = 3, then 3⁵ = 243"),
        ("16^(3/2)", 64, "√16 = 4, then 4³ = 64"),
        ("25^(1/2)", 5, "√25 = 5"),
        ("1000^(2/3)", 100, "∛1000 = 10, then 10² = 100"),
        ("32^(3/5)", 8, "⁵√32 = 2, then 2³ = 8"),
    ]
    for expr, ans, expl in rat_exp_data:
        correct = str(ans)
        distractors = [str(ans * 2), str(ans // 2 if ans > 2 else ans + 3), str(ans + 1)]
        distractors = [d for d in distractors if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(str(ans + random.randint(2, 10)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Medium",
            f"Evaluate: {expr}",
            choices, correct,
            f"{expl}. Therefore {expr} = {ans}.",
            ["rational exponents", "roots and powers"],
        ))
        qid += 1

    # --- Block 3: Scientific notation (small numbers) (20 questions) ---
    sci_small = [
        (0.005, "5 × 10⁻³"), (0.00032, "3.2 × 10⁻⁴"), (0.0071, "7.1 × 10⁻³"),
        (0.000045, "4.5 × 10⁻⁵"), (0.0000089, "8.9 × 10⁻⁶"),
        (0.062, "6.2 × 10⁻²"), (0.00091, "9.1 × 10⁻⁴"),
        (0.0000003, "3 × 10⁻⁷"), (0.0015, "1.5 × 10⁻³"),
        (0.00000072, "7.2 × 10⁻⁷"), (0.0044, "4.4 × 10⁻³"),
        (0.000056, "5.6 × 10⁻⁵"), (0.00000018, "1.8 × 10⁻⁷"),
        (0.0083, "8.3 × 10⁻³"), (0.000000025, "2.5 × 10⁻⁸"),
        (0.00067, "6.7 × 10⁻⁴"), (0.0000041, "4.1 × 10⁻⁶"),
        (0.093, "9.3 × 10⁻²"), (0.00012, "1.2 × 10⁻⁴"),
        (0.000000099, "9.9 × 10⁻⁸"),
    ]
    sup_map = {0:"⁰",1:"¹",2:"²",3:"³",4:"⁴",5:"⁵",6:"⁶",7:"⁷",8:"⁸",9:"⁹"}
    def to_sup(n):
        if n < 0:
            return "⁻" + "".join(sup_map[int(d)] for d in str(abs(n)))
        return "".join(sup_map[int(d)] for d in str(n))

    for num, sci in sci_small:
        correct = sci
        parts = sci.split(" × 10")
        coeff = parts[0]
        exp_str = parts[1]
        # Parse exponent
        exp_val = 0
        neg = False
        for ch in exp_str:
            if ch == "⁻":
                neg = True
            else:
                for k, v in sup_map.items():
                    if ch == v:
                        exp_val = exp_val * 10 + k
                        break
        if neg:
            exp_val = -exp_val
        d1 = f"{coeff} × 10{to_sup(exp_val + 1)}"
        d2 = f"{coeff} × 10{to_sup(exp_val - 1)}"
        d3 = f"{float(coeff)*10:.1f} × 10{to_sup(exp_val - 1)}" if float(coeff) < 9 else f"{float(coeff)/10:.2f} × 10{to_sup(exp_val + 1)}"
        distractors = [d for d in [d1, d2, d3] if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(f"{coeff} × 10{to_sup(exp_val + 2)}")
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Medium",
            f"Express {num} in scientific notation.",
            choices, correct,
            f"Move the decimal point right until coefficient is between 1 and 10. {num} = {sci}.",
            ["scientific notation", "negative exponents", "powers of 10"],
        ))
        qid += 1

    # --- Block 4: Negative base with exponent (20 questions) ---
    neg_base_data = [
        ((-2), 3, -8), ((-2), 4, 16), ((-2), 5, -32), ((-2), 6, 64),
        ((-3), 2, 9), ((-3), 3, -27), ((-3), 4, 81), ((-3), 5, -243),
        ((-4), 2, 16), ((-4), 3, -64), ((-5), 2, 25), ((-5), 3, -125),
        ((-1), 10, 1), ((-1), 11, -1), ((-1), 99, -1), ((-1), 100, 1),
        ((-6), 2, 36), ((-7), 2, 49), ((-10), 3, -1000), ((-2), 7, -128),
    ]
    for base, exp, ans in neg_base_data:
        correct = str(ans)
        sign_word = "even" if exp % 2 == 0 else "odd"
        result_sign = "positive" if ans > 0 else "negative"
        distractors = [str(-ans), str(abs(ans) + abs(base)), str(base * exp)]
        distractors = [d for d in distractors if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(str(ans + random.choice([-1, 1]) * random.randint(1, 10)))
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Medium",
            f"What is ({base})^{exp}?",
            choices, correct,
            f"Negative base with {sign_word} exponent gives a {result_sign} result. |{base}|^{exp} = {abs(ans)}, so ({base})^{exp} = {ans}.",
            ["negative bases", "sign rules", "exponents"],
        ))
        qid += 1

    # --- Block 5: Adding/subtracting radicals (20 questions) ---
    add_rad_data = [
        ("√12 + √27", "2√3 + 3√3", "5√3", ["4√3", "5√6", "6√3"]),
        ("√50 + √18", "5√2 + 3√2", "8√2", ["7√2", "8√4", "√68"]),
        ("√75 - √27", "5√3 - 3√3", "2√3", ["3√3", "√48", "2√6"]),
        ("√45 + √20", "3√5 + 2√5", "5√5", ["4√5", "5√10", "√65"]),
        ("√32 + √8", "4√2 + 2√2", "6√2", ["5√2", "6√4", "√40"]),
        ("√98 - √50", "7√2 - 5√2", "2√2", ["3√2", "√48", "12√2"]),
        ("√48 + √12", "4√3 + 2√3", "6√3", ["5√3", "6√6", "√60"]),
        ("√80 - √20", "4√5 - 2√5", "2√5", ["3√5", "2√10", "√60"]),
        ("√63 + √28", "3√7 + 2√7", "5√7", ["4√7", "5√14", "√91"]),
        ("√200 - √72", "10√2 - 6√2", "4√2", ["3√2", "16√2", "√128"]),
        ("3√2 + 5√2", "combine like radicals", "8√2", ["15√2", "8√4", "√64"]),
        ("7√3 - 2√3", "combine like radicals", "5√3", ["9√3", "5√6", "√75"]),
        ("√108 + √48", "6√3 + 4√3", "10√3", ["8√3", "10√6", "√156"]),
        ("√125 - √45", "5√5 - 3√5", "2√5", ["3√5", "2√10", "√80"]),
        ("√72 + √32", "6√2 + 4√2", "10√2", ["8√2", "10√4", "√104"]),
        ("√147 - √75", "7√3 - 5√3", "2√3", ["3√3", "12√3", "√72"]),
        ("2√50 + 3√2", "10√2 + 3√2", "13√2", ["5√52", "6√2", "13√4"]),
        ("√180 - √80", "6√5 - 4√5", "2√5", ["3√5", "10√5", "√100"]),
        ("√242 - √98", "11√2 - 7√2", "4√2", ["3√2", "18√2", "√144"]),
        ("√300 + √75", "10√3 + 5√3", "15√3", ["12√3", "15√6", "√375"]),
    ]
    for expr, steps, ans_str, dists in add_rad_data:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Medium",
            f"Simplify: {expr}",
            choices, correct,
            f"Simplify each radical first: {steps}. Result: {ans_str}.",
            ["radicals", "addition", "simplification"],
        ))
        qid += 1

    # --- Block 6: Scientific notation multiplication/division (20 questions) ---
    sci_ops = [
        ("(2 × 10³) × (3 × 10⁴)", "6 × 10⁷", "2×3=6; 10^(3+4)=10⁷"),
        ("(4 × 10⁵) × (2 × 10³)", "8 × 10⁸", "4×2=8; 10^(5+3)=10⁸"),
        ("(5 × 10²) × (6 × 10⁴)", "3 × 10⁷", "5×6=30=3×10¹; 10^(2+4+1)=10⁷"),
        ("(3 × 10⁶) × (3 × 10²)", "9 × 10⁸", "3×3=9; 10^(6+2)=10⁸"),
        ("(7 × 10³) × (2 × 10⁵)", "1.4 × 10⁹", "7×2=14=1.4×10¹; 10^(3+5+1)=10⁹"),
        ("(8 × 10⁴) ÷ (2 × 10²)", "4 × 10²", "8÷2=4; 10^(4-2)=10²"),
        ("(9 × 10⁷) ÷ (3 × 10³)", "3 × 10⁴", "9÷3=3; 10^(7-3)=10⁴"),
        ("(6 × 10⁹) ÷ (2 × 10⁴)", "3 × 10⁵", "6÷2=3; 10^(9-4)=10⁵"),
        ("(4.8 × 10⁶) ÷ (1.2 × 10²)", "4 × 10⁴", "4.8÷1.2=4; 10^(6-2)=10⁴"),
        ("(1.5 × 10⁸) × (4 × 10³)", "6 × 10¹¹", "1.5×4=6; 10^(8+3)=10¹¹"),
        ("(2.5 × 10⁴) × (4 × 10³)", "1 × 10⁸", "2.5×4=10=1×10¹; 10^(4+3+1)=10⁸"),
        ("(6 × 10⁵) ÷ (3 × 10⁸)", "2 × 10⁻³", "6÷3=2; 10^(5-8)=10⁻³"),
        ("(8 × 10³) × (5 × 10²)", "4 × 10⁶", "8×5=40=4×10¹; 10^(3+2+1)=10⁶"),
        ("(3.6 × 10⁷) ÷ (9 × 10⁴)", "4 × 10²", "3.6÷9=0.4=4×10⁻¹; 10^(7-4-1)=10²"),
        ("(2 × 10⁶) × (2 × 10⁶)", "4 × 10¹²", "2×2=4; 10^(6+6)=10¹²"),
        ("(5 × 10⁴) × (5 × 10⁴)", "2.5 × 10⁹", "5×5=25=2.5×10¹; 10^(4+4+1)=10⁹"),
        ("(1.2 × 10⁵) × (3 × 10²)", "3.6 × 10⁷", "1.2×3=3.6; 10^(5+2)=10⁷"),
        ("(7.2 × 10⁸) ÷ (3.6 × 10⁵)", "2 × 10³", "7.2÷3.6=2; 10^(8-5)=10³"),
        ("(4 × 10⁻²) × (3 × 10⁵)", "1.2 × 10⁴", "4×3=12=1.2×10¹; 10^(-2+5+1)=10⁴"),
        ("(9 × 10⁻³) × (2 × 10⁷)", "1.8 × 10⁵", "9×2=18=1.8×10¹; 10^(-3+7+1)=10⁵"),
    ]
    for expr, ans_str, expl in sci_ops:
        correct = ans_str
        # Generate distractors by tweaking exponent
        parts = ans_str.split(" × 10")
        coeff = parts[0]
        exp_part = parts[1] if len(parts) > 1 else "⁰"
        exp_val = 0
        neg = False
        for ch in exp_part:
            if ch == "⁻":
                neg = True
            else:
                for k, v in sup_map.items():
                    if ch == v:
                        exp_val = exp_val * 10 + k
                        break
        if neg:
            exp_val = -exp_val
        d1 = f"{coeff} × 10{to_sup(exp_val + 1)}"
        d2 = f"{coeff} × 10{to_sup(exp_val - 1)}"
        d3 = f"{float(coeff)*2} × 10{to_sup(exp_val)}" if float(coeff) < 5 else f"{float(coeff)/2} × 10{to_sup(exp_val + 1)}"
        distractors = [d for d in [d1, d2, d3] if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(f"{coeff} × 10{to_sup(exp_val + 2)}")
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Medium",
            f"Compute: {expr}",
            choices, correct,
            f"{expl}. Answer: {ans_str}.",
            ["scientific notation", "multiplication", "division"],
        ))
        qid += 1

    # --- Block 7: Multi-step exponent simplification (25 questions) ---
    multi_step = [
        ("2³ × 2⁴ ÷ 2⁵", "2^(3+4-5) = 2² = 4", "4", ["8", "16", "2"]),
        ("3² × 3³ ÷ 3⁴", "3^(2+3-4) = 3¹ = 3", "3", ["9", "27", "1"]),
        ("5⁴ ÷ 5² × 5¹", "5^(4-2+1) = 5³ = 125", "125", ["25", "625", "5"]),
        ("10³ × 10² ÷ 10⁴", "10^(3+2-4) = 10¹ = 10", "10", ["100", "1000", "1"]),
        ("2⁸ ÷ (2³ × 2²)", "2^(8-3-2) = 2³ = 8", "8", ["4", "16", "32"]),
        ("(3² × 3)³", "3^((2+1)×3) = 3⁹ = 19683", "19,683", ["729", "6,561", "2,187"]),
        ("(2⁴)² ÷ 2⁵", "2^(8-5) = 2³ = 8", "8", ["4", "16", "32"]),
        ("5⁰ + 5¹ + 5²", "1 + 5 + 25 = 31", "31", ["30", "26", "125"]),
        ("2⁰ + 3⁰ + 4⁰", "1 + 1 + 1 = 3", "3", ["9", "0", "1"]),
        ("10⁰ + 10¹ + 10²", "1 + 10 + 100 = 111", "111", ["110", "1000", "100"]),
        ("(4²)³ ÷ 4⁴", "4^(6-4) = 4² = 16", "16", ["64", "4", "256"]),
        ("6² × 6⁰", "36 × 1 = 36", "36", ["0", "12", "6"]),
        ("(2 × 3)³", "6³ = 216", "216", ["18", "36", "72"]),
        ("(2³)² × 2⁰", "2⁶ × 1 = 64", "64", ["32", "128", "8"]),
        ("3⁴ ÷ 3⁴", "3⁰ = 1", "1", ["0", "3", "81"]),
        ("7² × 7⁻²", "7^(2-2) = 7⁰ = 1", "1", ["0", "49", "7"]),
        ("2⁵ × 2⁻³", "2^(5-3) = 2² = 4", "4", ["8", "16", "2"]),
        ("10⁴ × 10⁻⁶", "10^(4-6) = 10⁻² = 0.01", "0.01", ["0.001", "0.1", "100"]),
        ("5³ × 5⁻¹", "5^(3-1) = 5² = 25", "25", ["5", "125", "1"]),
        ("(3⁻¹)²", "3⁻² = 1/9", "1/9", ["1/3", "1/6", "9"]),
        ("(2⁻²)³", "2⁻⁶ = 1/64", "1/64", ["1/8", "1/32", "64"]),
        ("4³ ÷ 2⁶", "(2²)³ ÷ 2⁶ = 2⁶ ÷ 2⁶ = 1", "1", ["2", "4", "8"]),
        ("9² ÷ 3⁴", "(3²)² ÷ 3⁴ = 3⁴ ÷ 3⁴ = 1", "1", ["3", "9", "0"]),
        ("8² ÷ 4³", "(2³)² ÷ (2²)³ = 2⁶ ÷ 2⁶ = 1", "1", ["2", "4", "8"]),
        ("27 × 3⁻³", "3³ × 3⁻³ = 3⁰ = 1", "1", ["0", "3", "9"]),
    ]
    for expr, expl, ans_str, dists in multi_step:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Medium",
            f"Simplify: {expr}",
            choices, correct,
            f"{expl}.",
            ["exponent rules", "multi-step", "simplification"],
        ))
        qid += 1

    # --- Block 8: Rationalizing denominators (15 questions) ---
    rationalize_data = [
        ("1/√2", "√2/2", "Multiply by √2/√2: √2/2"),
        ("3/√3", "√3", "Multiply by √3/√3: 3√3/3 = √3"),
        ("6/√2", "3√2", "Multiply by √2/√2: 6√2/2 = 3√2"),
        ("4/√2", "2√2", "Multiply by √2/√2: 4√2/2 = 2√2"),
        ("5/√5", "√5", "Multiply by √5/√5: 5√5/5 = √5"),
        ("10/√5", "2√5", "Multiply by √5/√5: 10√5/5 = 2√5"),
        ("2/√3", "2√3/3", "Multiply by √3/√3: 2√3/3"),
        ("8/√2", "4√2", "Multiply by √2/√2: 8√2/2 = 4√2"),
        ("12/√3", "4√3", "Multiply by √3/√3: 12√3/3 = 4√3"),
        ("6/√6", "√6", "Multiply by √6/√6: 6√6/6 = √6"),
        ("15/√3", "5√3", "Multiply by √3/√3: 15√3/3 = 5√3"),
        ("9/√3", "3√3", "Multiply by √3/√3: 9√3/3 = 3√3"),
        ("14/√7", "2√7", "Multiply by √7/√7: 14√7/7 = 2√7"),
        ("20/√5", "4√5", "Multiply by √5/√5: 20√5/5 = 4√5"),
        ("18/√6", "3√6", "Multiply by √6/√6: 18√6/6 = 3√6"),
    ]
    for expr, ans_str, expl in rationalize_data:
        correct = ans_str
        # Generate distractors
        if "√" in ans_str and "/" in ans_str:
            d1 = ans_str.replace("/", "×")
            d2 = expr  # unreduced form
            d3 = ans_str.split("/")[0]
        else:
            parts = ans_str.split("√")
            coeff = parts[0] if parts[0] else "1"
            rad = parts[1] if len(parts) > 1 else "2"
            c_val = int(coeff) if coeff.strip() else 1
            d1 = f"{c_val + 1}√{rad}"
            d2 = f"{c_val - 1}√{rad}" if c_val > 1 else f"{c_val + 2}√{rad}"
            d3 = f"{c_val}√{int(rad)*2}" if rad.isdigit() else f"{c_val*2}√{rad}"
        distractors = [d for d in [d1, d2, d3] if d != correct][:3]
        while len(distractors) < 3:
            distractors.append(expr)
        choices = _shuffle_choices(correct, distractors[:3])
        questions.append(_q(
            qid, "Medium",
            f"Rationalize the denominator: {expr}",
            choices, correct,
            f"{expl}.",
            ["radicals", "rationalization", "simplification"],
        ))
        qid += 1

    # --- Block 9: Estimation of roots (15 questions) ---
    est_data = [
        (30, 5, 6, 5), (40, 6, 7, 6), (50, 7, 8, 7),
        (60, 7, 8, 8), (70, 8, 9, 8), (85, 9, 10, 9),
        (110, 10, 11, 10), (130, 11, 12, 11), (150, 12, 13, 12),
        (170, 13, 14, 13), (200, 14, 15, 14), (250, 15, 16, 16),
        (300, 17, 18, 17), (500, 22, 23, 22), (750, 27, 28, 27),
    ]
    for radicand, low, high, nearest in est_data:
        correct = str(nearest)
        distractors = [str(nearest + 2), str(nearest - 2 if nearest > 2 else nearest + 3), str(nearest + 1)]
        distractors = [d for d in distractors if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Medium",
            f"Estimate √{radicand} to the nearest whole number.",
            choices, correct,
            f"{low}² = {low**2} and {high}² = {high**2}. Since {radicand} is between these, √{radicand} ≈ {nearest}.",
            ["estimation", "square roots", "number sense"],
        ))
        qid += 1

    # --- Block 10: Power of a product/quotient (10 questions) ---
    pop_prod = [
        ("(2×5)³", "10³ = 1000", "1,000", ["30", "150", "500"]),
        ("(3×4)²", "12² = 144", "144", ["24", "48", "72"]),
        ("(2×7)²", "14² = 196", "196", ["28", "98", "56"]),
        ("(5×3)²", "15² = 225", "225", ["30", "75", "150"]),
        ("(2/3)³", "2³/3³ = 8/27", "8/27", ["2/9", "6/9", "8/9"]),
        ("(3/4)²", "3²/4² = 9/16", "9/16", ["6/8", "3/8", "9/8"]),
        ("(1/2)⁴", "1/2⁴ = 1/16", "1/16", ["1/8", "4/2", "1/4"]),
        ("(2/5)³", "2³/5³ = 8/125", "8/125", ["6/15", "8/25", "2/15"]),
        ("(5/2)²", "5²/2² = 25/4", "25/4", ["10/4", "25/2", "5/4"]),
        ("(4/3)²", "4²/3² = 16/9", "16/9", ["8/6", "16/3", "4/9"]),
    ]
    for expr, expl, ans_str, dists in pop_prod:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Medium",
            f"Evaluate: {expr}",
            choices, correct,
            f"Apply the power to each factor: {expl}.",
            ["power of a product", "power of a quotient", "exponent rules"],
        ))
        qid += 1

    return questions


def generate_hard_questions(start_id: int) -> list[dict]:
    """Generate 200 Hard questions."""
    questions: list[dict] = []
    qid = start_id

    # --- Block 1: Complex multi-step exponent simplification (30 questions) ---
    complex_exp = [
        ("(2⁵ × 4³) ÷ 8²", "2⁵ × (2²)³ ÷ (2³)² = 2⁵ × 2⁶ ÷ 2⁶ = 2⁵ = 32", "32", ["16", "64", "8"]),
        ("(3⁴ × 9²) ÷ 27²", "3⁴ × 3⁴ ÷ 3⁶ = 3² = 9", "9", ["3", "27", "81"]),
        ("(16² × 2³) ÷ 4⁴", "(2⁴)² × 2³ ÷ (2²)⁴ = 2⁸ × 2³ ÷ 2⁸ = 2³ = 8", "8", ["4", "16", "32"]),
        ("(27 × 9²) ÷ 3⁷", "3³ × 3⁴ ÷ 3⁷ = 3⁰ = 1", "1", ["3", "9", "0"]),
        ("(2⁶ × 4²) ÷ (8² × 2)", "2⁶ × 2⁴ ÷ (2⁶ × 2) = 2¹⁰ ÷ 2⁷ = 2³ = 8", "8", ["4", "16", "2"]),
        ("(5³ × 25) ÷ 125", "5³ × 5² ÷ 5³ = 5² = 25", "25", ["5", "125", "1"]),
        ("(4⁵ ÷ 2⁶) × 2⁻²", "(2²)⁵ ÷ 2⁶ × 2⁻² = 2¹⁰ ÷ 2⁶ × 2⁻² = 2² = 4", "4", ["8", "2", "16"]),
        ("(9³ × 3⁻²) ÷ 27", "(3²)³ × 3⁻² ÷ 3³ = 3⁶ × 3⁻² ÷ 3³ = 3¹ = 3", "3", ["9", "1", "27"]),
        ("(8² × 16) ÷ (2⁵ × 4²)", "(2³)² × 2⁴ ÷ (2⁵ × 2⁴) = 2¹⁰ ÷ 2⁹ = 2", "2", ["4", "1", "8"]),
        ("(125 × 5⁻²)²", "(5³ × 5⁻²)² = (5¹)² = 25", "25", ["5", "125", "1"]),
        ("(2⁴)³ ÷ (4³ × 2²)", "2¹² ÷ (2⁶ × 2²) = 2¹² ÷ 2⁸ = 2⁴ = 16", "16", ["8", "32", "4"]),
        ("(3² × 3⁻¹)⁴", "(3¹)⁴ = 3⁴ = 81", "81", ["27", "9", "243"]),
        ("(64^(1/3))² × 2⁻¹", "4² × 1/2 = 16/2 = 8", "8", ["4", "16", "32"]),
        ("(2⁸ ÷ 4²) × (8 ÷ 2³)", "2⁸ ÷ 2⁴ × 2³ ÷ 2³ = 2⁴ × 1 = 16", "16", ["8", "32", "4"]),
        ("(81^(1/4))³ × 3⁻¹", "3³ × 3⁻¹ = 3² = 9", "9", ["3", "27", "1"]),
        ("(2⁻³)⁻² × 2⁻⁴", "2⁶ × 2⁻⁴ = 2² = 4", "4", ["8", "16", "1"]),
        ("(5² × 5⁻³)⁻²", "(5⁻¹)⁻² = 5² = 25", "25", ["1/25", "5", "125"]),
        ("(3⁴ × 3⁻²)³ ÷ 3⁵", "(3²)³ ÷ 3⁵ = 3⁶ ÷ 3⁵ = 3", "3", ["9", "1", "27"]),
        ("(4⁻¹ × 16)²", "(1/4 × 16)² = 4² = 16", "16", ["4", "64", "8"]),
        ("(2⁵ × 2⁻²)² ÷ 2⁴", "(2³)² ÷ 2⁴ = 2⁶ ÷ 2⁴ = 2² = 4", "4", ["8", "2", "16"]),
        ("(27^(2/3) × 3⁻¹)²", "(9 × 1/3)² = 3² = 9", "9", ["3", "27", "81"]),
        ("(16^(3/4) ÷ 2)²", "(8 ÷ 2)² = 4² = 16", "16", ["8", "32", "4"]),
        ("(32^(2/5))³", "(4)³ = 64", "64", ["32", "16", "128"]),
        ("(100^(1/2))³ ÷ 10²", "10³ ÷ 10² = 10", "10", ["100", "1", "1000"]),
        ("(8^(2/3) × 27^(1/3))²", "(4 × 3)² = 12² = 144", "144", ["36", "72", "108"]),
        ("(4^(3/2) × 9^(1/2)) ÷ 6", "(8 × 3) ÷ 6 = 24 ÷ 6 = 4", "4", ["6", "8", "2"]),
        ("(125^(2/3) ÷ 5)²", "(25 ÷ 5)² = 5² = 25", "25", ["5", "125", "625"]),
        ("(64^(1/6))⁴ × 2⁻²", "2⁴ × 2⁻² = 2² = 4", "4", ["8", "2", "16"]),
        ("(81^(1/2) × 27^(1/3)) ÷ 3²", "(9 × 3) ÷ 9 = 27 ÷ 9 = 3", "3", ["9", "1", "27"]),
        ("(16^(1/4) × 8^(1/3))³", "(2 × 2)³ = 4³ = 64", "64", ["8", "32", "16"]),
    ]
    for expr, expl, ans_str, dists in complex_exp:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            f"Simplify: {expr}",
            choices, correct,
            f"{expl}.",
            ["exponent rules", "multi-step", "advanced simplification"],
        ))
        qid += 1

    # --- Block 2: Word problems with exponents (30 questions) ---
    word_problems = [
        (
            "A bacteria colony doubles every hour. If it starts with 500 bacteria, how many will there be after 6 hours?",
            "500 × 2⁶ = 500 × 64 = 32,000",
            "32,000", ["16,000", "64,000", "3,000"]
        ),
        (
            "A computer file is 2⁸ kilobytes. How many kilobytes is that?",
            "2⁸ = 256 KB",
            "256", ["128", "512", "64"]
        ),
        (
            "A square garden has an area of 289 m². What is the length of one side?",
            "√289 = 17 m",
            "17 m", ["15 m", "19 m", "14 m"]
        ),
        (
            "A cube-shaped water tank has a volume of 1,728 cm³. What is the length of each edge?",
            "∛1728 = 12 cm",
            "12 cm", ["14 cm", "10 cm", "8 cm"]
        ),
        (
            "An investment of ₱10,000 grows by a factor of 1.1 each year. What is its value after 3 years? (Round to nearest peso)",
            "10,000 × (1.1)³ = 10,000 × 1.331 = ₱13,310",
            "₱13,310", ["₱13,000", "₱11,000", "₱13,100"]
        ),
        (
            "The distance from Earth to the Sun is approximately 1.5 × 10⁸ km. Express this in standard form.",
            "1.5 × 10⁸ = 150,000,000",
            "150,000,000 km", ["15,000,000 km", "1,500,000,000 km", "1,500,000 km"]
        ),
        (
            "A government office has 3⁴ employees. How many employees is that?",
            "3⁴ = 81",
            "81", ["12", "64", "27"]
        ),
        (
            "A population of 2,000 triples every decade. What will the population be after 3 decades?",
            "2,000 × 3³ = 2,000 × 27 = 54,000",
            "54,000", ["18,000", "6,000", "162,000"]
        ),
        (
            "A square tile has a side of 15 cm. What is its area?",
            "15² = 225 cm²",
            "225 cm²", ["30 cm²", "150 cm²", "200 cm²"]
        ),
        (
            "The mass of a hydrogen atom is approximately 1.67 × 10⁻²⁷ kg. What is the mass of 10³ hydrogen atoms in scientific notation?",
            "1.67 × 10⁻²⁷ × 10³ = 1.67 × 10⁻²⁴ kg",
            "1.67 × 10⁻²⁴ kg", ["1.67 × 10⁻³⁰ kg", "1.67 × 10⁻²¹ kg", "16.7 × 10⁻²⁷ kg"]
        ),
        (
            "A city's population is 4.5 × 10⁶. A neighboring town has 9 × 10⁴ people. How many times larger is the city?",
            "(4.5 × 10⁶) ÷ (9 × 10⁴) = 0.5 × 10² = 50 times",
            "50", ["500", "5", "5,000"]
        ),
        (
            "A cube has a surface area of 384 cm². If surface area = 6s², what is the edge length?",
            "6s² = 384 → s² = 64 → s = 8 cm",
            "8 cm", ["6 cm", "10 cm", "12 cm"]
        ),
        (
            "A radioactive substance has a half-life of 1 year. If you start with 800 grams, how much remains after 5 years?",
            "800 × (1/2)⁵ = 800 × 1/32 = 25 grams",
            "25 grams", ["50 grams", "12.5 grams", "100 grams"]
        ),
        (
            "A government budget of ₱2.4 × 10⁹ is divided equally among 8 × 10² departments. How much does each department receive?",
            "(2.4 × 10⁹) ÷ (8 × 10²) = 0.3 × 10⁷ = 3 × 10⁶ = ₱3,000,000",
            "₱3,000,000", ["₱300,000", "₱30,000,000", "₱3,000"]
        ),
        (
            "A server processes 2¹² requests per second. How many requests is that?",
            "2¹² = 4,096",
            "4,096", ["2,048", "8,192", "1,024"]
        ),
        (
            "The speed of light is 3 × 10⁸ m/s. How far does light travel in 5 × 10² seconds?",
            "(3 × 10⁸) × (5 × 10²) = 15 × 10¹⁰ = 1.5 × 10¹¹ m",
            "1.5 × 10¹¹ m", ["1.5 × 10¹⁰ m", "15 × 10⁸ m", "1.5 × 10⁶ m"]
        ),
        (
            "A square plot of land has an area of 6,400 m². What is the perimeter?",
            "Side = √6400 = 80 m. Perimeter = 4 × 80 = 320 m",
            "320 m", ["160 m", "640 m", "80 m"]
        ),
        (
            "If 5^x = 625, what is x?",
            "5⁴ = 625, so x = 4",
            "4", ["3", "5", "2"]
        ),
        (
            "If 2^x = 512, what is x?",
            "2⁹ = 512, so x = 9",
            "9", ["8", "10", "7"]
        ),
        (
            "If 3^x = 729, what is x?",
            "3⁶ = 729, so x = 6",
            "6", ["5", "7", "4"]
        ),
        (
            "A flash drive has a capacity of 2³² bytes. Express this in gigabytes (1 GB = 2³⁰ bytes).",
            "2³² ÷ 2³⁰ = 2² = 4 GB",
            "4 GB", ["2 GB", "8 GB", "1 GB"]
        ),
        (
            "The national debt is ₱1.44 × 10¹³. The population is 1.2 × 10⁸. What is the debt per person?",
            "(1.44 × 10¹³) ÷ (1.2 × 10⁸) = 1.2 × 10⁵ = ₱120,000",
            "₱120,000", ["₱12,000", "₱1,200,000", "₱1,200"]
        ),
        (
            "A cube-shaped room has a volume of 27 m³. What is the floor area?",
            "Edge = ∛27 = 3 m. Floor area = 3² = 9 m²",
            "9 m²", ["3 m²", "27 m²", "6 m²"]
        ),
        (
            "If the side of a square is doubled, by what factor does the area increase?",
            "New area = (2s)² = 4s². Factor = 4",
            "4", ["2", "8", "16"]
        ),
        (
            "If the edge of a cube is tripled, by what factor does the volume increase?",
            "New volume = (3s)³ = 27s³. Factor = 27",
            "27", ["9", "3", "81"]
        ),
        (
            "A photocopier reduces a document to (3/4) of its size each time. After 2 reductions, what fraction of the original size remains?",
            "(3/4)² = 9/16",
            "9/16", ["3/8", "6/8", "1/2"]
        ),
        (
            "A savings account earns 5% interest compounded annually. What is the growth factor after 4 years?",
            "(1.05)⁴ ≈ 1.2155. Closest to 1.22",
            "1.22", ["1.20", "1.25", "1.15"]
        ),
        (
            "How many zeros are in the standard form of 10⁸?",
            "10⁸ = 100,000,000 which has 8 zeros",
            "8", ["7", "9", "10"]
        ),
        (
            "A signal loses half its strength every 10 km. After 40 km, what fraction of the original strength remains?",
            "(1/2)⁴ = 1/16",
            "1/16", ["1/8", "1/32", "1/4"]
        ),
        (
            "The diameter of a red blood cell is about 7 × 10⁻⁶ m. Express this in micrometers (1 μm = 10⁻⁶ m).",
            "7 × 10⁻⁶ m ÷ 10⁻⁶ = 7 μm",
            "7 μm", ["0.7 μm", "70 μm", "0.07 μm"]
        ),
    ]
    for question, expl, ans_str, dists in word_problems:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            question,
            choices, correct,
            expl + ".",
            ["word problem", "application", "exponents and roots"],
        ))
        qid += 1

    # --- Block 3: Comparing expressions (20 questions) ---
    compare_data = [
        ("Which is greater: 2⁸ or 4³?", "2⁸ = 256; 4³ = 64. 2⁸ is greater.", "2⁸", ["4³", "They are equal", "Cannot be determined"]),
        ("Which is greater: 3⁴ or 4³?", "3⁴ = 81; 4³ = 64. 3⁴ is greater.", "3⁴", ["4³", "They are equal", "Cannot be determined"]),
        ("Which is greater: 2¹⁰ or 10³?", "2¹⁰ = 1024; 10³ = 1000. 2¹⁰ is greater.", "2¹⁰", ["10³", "They are equal", "Cannot be determined"]),
        ("Which is greater: 5³ or 3⁵?", "5³ = 125; 3⁵ = 243. 3⁵ is greater.", "3⁵", ["5³", "They are equal", "Cannot be determined"]),
        ("Which is equal: 4³ or 8²?", "4³ = 64; 8² = 64. They are equal.", "They are equal", ["4³ is greater", "8² is greater", "Cannot be determined"]),
        ("Which is greater: 2⁶ or 3⁴?", "2⁶ = 64; 3⁴ = 81. 3⁴ is greater.", "3⁴", ["2⁶", "They are equal", "Cannot be determined"]),
        ("Which is greater: 9² or 2⁷?", "9² = 81; 2⁷ = 128. 2⁷ is greater.", "2⁷", ["9²", "They are equal", "Cannot be determined"]),
        ("Which is greater: 5⁴ or 4⁵?", "5⁴ = 625; 4⁵ = 1024. 4⁵ is greater.", "4⁵", ["5⁴", "They are equal", "Cannot be determined"]),
        ("Which is greater: 10² or 2¹⁰?", "10² = 100; 2¹⁰ = 1024. 2¹⁰ is greater.", "2¹⁰", ["10²", "They are equal", "Cannot be determined"]),
        ("Which is equal: 2⁶ or 4³?", "2⁶ = 64; 4³ = (2²)³ = 2⁶ = 64. They are equal.", "They are equal", ["2⁶ is greater", "4³ is greater", "Cannot be determined"]),
        ("Which is greater: 16^(1/2) or 27^(1/3)?", "16^(1/2) = 4; 27^(1/3) = 3. 16^(1/2) is greater.", "16^(1/2)", ["27^(1/3)", "They are equal", "Cannot be determined"]),
        ("Which is greater: 25^(1/2) or 8^(2/3)?", "25^(1/2) = 5; 8^(2/3) = 4. 25^(1/2) is greater.", "25^(1/2)", ["8^(2/3)", "They are equal", "Cannot be determined"]),
        ("Which is greater: √200 or ∛1000?", "√200 ≈ 14.1; ∛1000 = 10. √200 is greater.", "√200", ["∛1000", "They are equal", "Cannot be determined"]),
        ("Which is greater: 2⁵ or 5²?", "2⁵ = 32; 5² = 25. 2⁵ is greater.", "2⁵", ["5²", "They are equal", "Cannot be determined"]),
        ("Which is equal: 9^(3/2) or 27?", "9^(3/2) = (√9)³ = 3³ = 27. They are equal.", "They are equal", ["9^(3/2) is greater", "27 is greater", "Cannot be determined"]),
        ("Which is greater: 4^(5/2) or 2⁵?", "4^(5/2) = (√4)⁵ = 2⁵ = 32. They are equal.", "They are equal", ["4^(5/2)", "2⁵", "Cannot be determined"]),
        ("Which is greater: 3⁶ or 9³?", "3⁶ = 729; 9³ = (3²)³ = 3⁶ = 729. Equal.", "They are equal", ["3⁶", "9³", "Cannot be determined"]),
        ("Which is greater: 2¹² or 4⁵?", "2¹² = 4096; 4⁵ = (2²)⁵ = 2¹⁰ = 1024. 2¹² is greater.", "2¹²", ["4⁵", "They are equal", "Cannot be determined"]),
        ("Which is greater: 8³ or 2⁹?", "8³ = (2³)³ = 2⁹ = 512. They are equal.", "They are equal", ["8³", "2⁹", "Cannot be determined"]),
        ("Which is greater: 5³ or 2⁷?", "5³ = 125; 2⁷ = 128. 2⁷ is greater.", "2⁷", ["5³", "They are equal", "Cannot be determined"]),
    ]
    for question, expl, ans_str, dists in compare_data:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            question,
            choices, correct,
            expl,
            ["comparison", "exponents", "evaluation"],
        ))
        qid += 1

    # --- Block 4: Negative rational exponents (20 questions) ---
    neg_rat = [
        ("4^(-3/2)", "1/4^(3/2) = 1/(√4)³ = 1/8", "1/8", ["1/4", "1/16", "-8"]),
        ("8^(-2/3)", "1/8^(2/3) = 1/(∛8)² = 1/4", "1/4", ["1/8", "1/2", "-4"]),
        ("9^(-3/2)", "1/9^(3/2) = 1/(√9)³ = 1/27", "1/27", ["1/9", "1/81", "-27"]),
        ("16^(-3/4)", "1/16^(3/4) = 1/(⁴√16)³ = 1/8", "1/8", ["1/16", "1/4", "-8"]),
        ("25^(-1/2)", "1/25^(1/2) = 1/√25 = 1/5", "1/5", ["1/25", "1/10", "-5"]),
        ("27^(-1/3)", "1/27^(1/3) = 1/∛27 = 1/3", "1/3", ["1/27", "1/9", "-3"]),
        ("32^(-2/5)", "1/32^(2/5) = 1/(⁵√32)² = 1/4", "1/4", ["1/32", "1/8", "-4"]),
        ("64^(-1/3)", "1/64^(1/3) = 1/∛64 = 1/4", "1/4", ["1/64", "1/8", "-4"]),
        ("100^(-3/2)", "1/100^(3/2) = 1/(√100)³ = 1/1000", "1/1000", ["1/100", "1/10", "-1000"]),
        ("49^(-1/2)", "1/49^(1/2) = 1/√49 = 1/7", "1/7", ["1/49", "1/14", "-7"]),
        ("81^(-1/4)", "1/81^(1/4) = 1/⁴√81 = 1/3", "1/3", ["1/81", "1/9", "-3"]),
        ("125^(-2/3)", "1/125^(2/3) = 1/(∛125)² = 1/25", "1/25", ["1/125", "1/5", "-25"]),
        ("36^(-3/2)", "1/36^(3/2) = 1/(√36)³ = 1/216", "1/216", ["1/36", "1/6", "-216"]),
        ("16^(-1/2)", "1/16^(1/2) = 1/√16 = 1/4", "1/4", ["1/16", "1/8", "-4"]),
        ("8^(-4/3)", "1/8^(4/3) = 1/(∛8)⁴ = 1/16", "1/16", ["1/8", "1/32", "-16"]),
        ("4^(-5/2)", "1/4^(5/2) = 1/(√4)⁵ = 1/32", "1/32", ["1/16", "1/64", "-32"]),
        ("27^(-2/3)", "1/27^(2/3) = 1/(∛27)² = 1/9", "1/9", ["1/27", "1/3", "-9"]),
        ("64^(-2/3)", "1/64^(2/3) = 1/(∛64)² = 1/16", "1/16", ["1/64", "1/4", "-16"]),
        ("1000^(-1/3)", "1/1000^(1/3) = 1/∛1000 = 1/10", "1/10", ["1/1000", "1/100", "-10"]),
        ("256^(-1/4)", "1/256^(1/4) = 1/⁴√256 = 1/4", "1/4", ["1/256", "1/16", "-4"]),
    ]
    for expr, expl, ans_str, dists in neg_rat:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            f"Evaluate: {expr}",
            choices, correct,
            f"{expl}.",
            ["negative rational exponents", "reciprocals", "advanced"],
        ))
        qid += 1

    # --- Block 5: Complex radical operations (25 questions) ---
    complex_rad = [
        ("√2 × √8", "√(2×8) = √16 = 4", "4", ["2√2", "8", "√10"]),
        ("√3 × √27", "√(3×27) = √81 = 9", "9", ["3√3", "27", "√30"]),
        ("√5 × √20", "√(5×20) = √100 = 10", "10", ["5√2", "√25", "2√5"]),
        ("√6 × √24", "√(6×24) = √144 = 12", "12", ["6√2", "√30", "2√6"]),
        ("√12 × √3", "√(12×3) = √36 = 6", "6", ["3√2", "√15", "2√3"]),
        ("√18 × √2", "√(18×2) = √36 = 6", "6", ["3√2", "√20", "2√3"]),
        ("√50 × √2", "√(50×2) = √100 = 10", "10", ["5√2", "√52", "2√5"]),
        ("(2√3)²", "4 × 3 = 12", "12", ["6", "4√3", "2√9"]),
        ("(3√2)²", "9 × 2 = 18", "18", ["6√2", "9√2", "12"]),
        ("(5√3)²", "25 × 3 = 75", "75", ["15√3", "25√3", "50"]),
        ("√(4/9)", "√4/√9 = 2/3", "2/3", ["4/9", "2/9", "√4/9"]),
        ("√(25/16)", "√25/√16 = 5/4", "5/4", ["25/16", "5/16", "√25/16"]),
        ("√(49/64)", "√49/√64 = 7/8", "7/8", ["49/64", "7/64", "√49/64"]),
        ("√(81/100)", "√81/√100 = 9/10", "9/10", ["81/100", "9/100", "√81/100"]),
        ("√(36/25)", "√36/√25 = 6/5", "6/5", ["36/25", "6/25", "√36/25"]),
        ("3√8 + 2√2", "3(2√2) + 2√2 = 6√2 + 2√2 = 8√2", "8√2", ["5√10", "6√2", "5√2"]),
        ("2√27 - √12", "2(3√3) - 2√3 = 6√3 - 2√3 = 4√3", "4√3", ["2√15", "√15", "3√3"]),
        ("√50 + √32 - √8", "5√2 + 4√2 - 2√2 = 7√2", "7√2", ["9√2", "5√2", "3√2"]),
        ("2√45 + 3√20", "2(3√5) + 3(2√5) = 6√5 + 6√5 = 12√5", "12√5", ["5√65", "10√5", "6√5"]),
        ("√75 - √48 + √27", "5√3 - 4√3 + 3√3 = 4√3", "4√3", ["2√3", "6√3", "√150"]),
        ("(√5 + √3)(√5 - √3)", "5 - 3 = 2 (difference of squares)", "2", ["√2", "2√15", "8"]),
        ("(√7 + √2)(√7 - √2)", "7 - 2 = 5", "5", ["√5", "√14", "9"]),
        ("(√6)³", "6√6", "6√6", ["36", "6³", "√216"]),
        ("(2√5)³", "8 × 5√5 = 40√5", "40√5", ["10√5", "8√5", "30√5"]),
        ("√(2⁸)", "2⁴ = 16", "16", ["8", "32", "2⁴√2"]),
    ]
    for expr, expl, ans_str, dists in complex_rad:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            f"Simplify: {expr}",
            choices, correct,
            f"{expl}.",
            ["radicals", "advanced operations", "simplification"],
        ))
        qid += 1

    # --- Block 6: Solving for unknown exponents (20 questions) ---
    solve_exp = [
        ("If 2^x = 64, what is x?", "2⁶ = 64", "6", ["5", "7", "8"]),
        ("If 3^x = 243, what is x?", "3⁵ = 243", "5", ["4", "6", "3"]),
        ("If 5^x = 3125, what is x?", "5⁵ = 3125", "5", ["4", "6", "3"]),
        ("If 4^x = 256, what is x?", "4⁴ = 256", "4", ["3", "5", "6"]),
        ("If 10^x = 1,000,000, what is x?", "10⁶ = 1,000,000", "6", ["5", "7", "8"]),
        ("If 2^x = 1/16, what is x?", "2⁻⁴ = 1/16", "-4", ["-3", "-5", "4"]),
        ("If 3^x = 1/27, what is x?", "3⁻³ = 1/27", "-3", ["-2", "-4", "3"]),
        ("If 5^x = 1/25, what is x?", "5⁻² = 1/25", "-2", ["-1", "-3", "2"]),
        ("If 10^x = 0.001, what is x?", "10⁻³ = 0.001", "-3", ["-2", "-4", "3"]),
        ("If 2^x = 1, what is x?", "2⁰ = 1", "0", ["1", "-1", "2"]),
        ("If 7^x = 1, what is x?", "7⁰ = 1", "0", ["1", "-1", "7"]),
        ("If 4^x = 1/64, what is x?", "4⁻³ = 1/64", "-3", ["-2", "-4", "3"]),
        ("If 9^x = 3, what is x?", "9^(1/2) = 3, so x = 1/2", "1/2", ["1", "2", "1/3"]),
        ("If 8^x = 2, what is x?", "8^(1/3) = 2, so x = 1/3", "1/3", ["1/2", "1", "3"]),
        ("If 16^x = 2, what is x?", "16^(1/4) = 2, so x = 1/4", "1/4", ["1/2", "1/8", "4"]),
        ("If 27^x = 9, what is x?", "27^(2/3) = 9, so x = 2/3", "2/3", ["1/3", "3/2", "2"]),
        ("If 32^x = 8, what is x?", "32^(3/5) = 8, so x = 3/5", "3/5", ["2/5", "1/2", "5/3"]),
        ("If 64^x = 16, what is x?", "64^(2/3) = 16, so x = 2/3", "2/3", ["1/3", "1/2", "3/2"]),
        ("If 125^x = 25, what is x?", "125^(2/3) = 25, so x = 2/3", "2/3", ["1/3", "2/5", "3/2"]),
        ("If 81^x = 27, what is x?", "81^(3/4) = 27, so x = 3/4", "3/4", ["1/2", "2/3", "4/3"]),
    ]
    for question, expl, ans_str, dists in solve_exp:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            question,
            choices, correct,
            f"{expl}, so x = {ans_str}.",
            ["solving equations", "exponents", "unknown exponent"],
        ))
        qid += 1

    # --- Block 7: Advanced scientific notation word problems (20 questions) ---
    sci_word = [
        (
            "Earth's mass is 5.97 × 10²⁴ kg. The Moon's mass is 7.35 × 10²² kg. Approximately how many times heavier is Earth than the Moon?",
            "(5.97 × 10²⁴) ÷ (7.35 × 10²²) ≈ 0.81 × 10² ≈ 81",
            "81", ["8.1", "810", "8,100"]
        ),
        (
            "A nanometer is 10⁻⁹ m. A virus is 120 nanometers long. Express this in meters using scientific notation.",
            "120 × 10⁻⁹ = 1.2 × 10⁻⁷ m",
            "1.2 × 10⁻⁷ m", ["1.2 × 10⁻⁹ m", "12 × 10⁻⁸ m", "1.2 × 10⁻⁶ m"]
        ),
        (
            "A government collected ₱3.2 × 10⁹ in taxes in January and ₱4.8 × 10⁹ in February. What is the total in scientific notation?",
            "3.2 × 10⁹ + 4.8 × 10⁹ = 8 × 10⁹",
            "8 × 10⁹", ["8 × 10¹⁸", "80 × 10⁸", "0.8 × 10¹⁰"]
        ),
        (
            "Light travels at 3 × 10⁸ m/s. How many meters does it travel in one minute (60 seconds)?",
            "3 × 10⁸ × 60 = 180 × 10⁸ = 1.8 × 10¹⁰ m",
            "1.8 × 10¹⁰ m", ["1.8 × 10⁸ m", "18 × 10⁸ m", "1.8 × 10⁹ m"]
        ),
        (
            "A hard drive stores 5 × 10¹¹ bytes. Each photo takes 4 × 10⁶ bytes. How many photos can it store?",
            "(5 × 10¹¹) ÷ (4 × 10⁶) = 1.25 × 10⁵ = 125,000",
            "125,000", ["12,500", "1,250,000", "1,250"]
        ),
        (
            "The Philippine GDP is approximately ₱2.2 × 10¹³. If it grows by 6%, what is the increase?",
            "0.06 × 2.2 × 10¹³ = 0.132 × 10¹³ = 1.32 × 10¹²",
            "₱1.32 × 10¹²", ["₱1.32 × 10¹¹", "₱1.32 × 10¹³", "₱13.2 × 10¹²"]
        ),
        (
            "A bacterium divides every 20 minutes. Starting with 1 bacterium, how many are there after 4 hours (12 divisions)?",
            "2¹² = 4,096",
            "4,096", ["2,048", "8,192", "1,024"]
        ),
        (
            "The distance to the nearest star (Proxima Centauri) is about 4 × 10¹³ km. Light travels 9.5 × 10¹² km per year. How many years does light take?",
            "(4 × 10¹³) ÷ (9.5 × 10¹²) ≈ 4.2 years",
            "4.2 years", ["42 years", "0.42 years", "420 years"]
        ),
        (
            "A microgram is 10⁻⁶ grams. A sample weighs 450 micrograms. Express this in grams.",
            "450 × 10⁻⁶ = 4.5 × 10⁻⁴ grams",
            "4.5 × 10⁻⁴ g", ["4.5 × 10⁻⁶ g", "4.5 × 10⁻³ g", "45 × 10⁻⁵ g"]
        ),
        (
            "A city uses 2.4 × 10⁷ liters of water daily. How much water is used in 30 days?",
            "2.4 × 10⁷ × 30 = 72 × 10⁷ = 7.2 × 10⁸ liters",
            "7.2 × 10⁸ L", ["7.2 × 10⁷ L", "72 × 10⁷ L", "7.2 × 10⁹ L"]
        ),
        (
            "An electron's mass is 9.1 × 10⁻³¹ kg. What is the mass of 10⁶ electrons?",
            "9.1 × 10⁻³¹ × 10⁶ = 9.1 × 10⁻²⁵ kg",
            "9.1 × 10⁻²⁵ kg", ["9.1 × 10⁻³⁷ kg", "9.1 × 10⁻²⁴ kg", "91 × 10⁻³¹ kg"]
        ),
        (
            "A government office processes 8 × 10³ documents per day. How many documents in 250 working days?",
            "8 × 10³ × 250 = 2,000 × 10³ = 2 × 10⁶",
            "2 × 10⁶", ["2 × 10⁵", "20 × 10⁵", "2 × 10⁷"]
        ),
        (
            "The area of the Philippines is approximately 3 × 10⁵ km². If the population is 1.2 × 10⁸, what is the population density per km²?",
            "(1.2 × 10⁸) ÷ (3 × 10⁵) = 0.4 × 10³ = 400 per km²",
            "400", ["40", "4,000", "4"]
        ),
        (
            "A computer performs 5 × 10⁹ operations per second. How many operations in 2 × 10⁻³ seconds?",
            "5 × 10⁹ × 2 × 10⁻³ = 10 × 10⁶ = 1 × 10⁷",
            "1 × 10⁷", ["1 × 10⁶", "1 × 10¹²", "1 × 10⁸"]
        ),
        (
            "A sheet of paper is 1 × 10⁻⁴ m thick. How tall is a stack of 5 × 10⁴ sheets?",
            "1 × 10⁻⁴ × 5 × 10⁴ = 5 × 10⁰ = 5 m",
            "5 m", ["0.5 m", "50 m", "500 m"]
        ),
        (
            "Annual rainfall is 2.5 × 10³ mm. Convert to meters.",
            "2.5 × 10³ mm × 10⁻³ m/mm = 2.5 m",
            "2.5 m", ["25 m", "0.25 m", "250 m"]
        ),
        (
            "A satellite orbits at 3.6 × 10⁴ km above Earth. Express this in meters.",
            "3.6 × 10⁴ km × 10³ m/km = 3.6 × 10⁷ m",
            "3.6 × 10⁷ m", ["3.6 × 10⁴ m", "3.6 × 10⁶ m", "36 × 10⁶ m"]
        ),
        (
            "A government fund of ₱5 × 10⁸ earns 4% interest annually. What is the interest earned in one year?",
            "0.04 × 5 × 10⁸ = 0.2 × 10⁸ = 2 × 10⁷ = ₱20,000,000",
            "₱2 × 10⁷", ["₱2 × 10⁶", "₱2 × 10⁸", "₱20 × 10⁶"]
        ),
        (
            "A DNA molecule is 3.4 × 10⁻¹⁰ m per base pair. A chromosome has 2 × 10⁸ base pairs. What is its length?",
            "3.4 × 10⁻¹⁰ × 2 × 10⁸ = 6.8 × 10⁻² m = 0.068 m",
            "6.8 × 10⁻² m", ["6.8 × 10⁻¹⁸ m", "6.8 × 10² m", "6.8 × 10⁻³ m"]
        ),
        (
            "A city produces 1.5 × 10⁴ tons of waste daily. How much in a year (365 days) in scientific notation?",
            "1.5 × 10⁴ × 365 = 5,475 × 10⁴ ≈ 5.475 × 10⁶ ≈ 5.5 × 10⁶ tons",
            "5.5 × 10⁶ tons", ["5.5 × 10⁵ tons", "5.5 × 10⁷ tons", "55 × 10⁵ tons"]
        ),
    ]
    for question, expl, ans_str, dists in sci_word:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            question,
            choices, correct,
            f"{expl}.",
            ["scientific notation", "word problem", "application"],
        ))
        qid += 1

    # --- Block 8: Conceptual/tricky questions (20 questions) ---
    conceptual = [
        (
            "What is the value of (-1)²⁰²⁶?",
            "Even exponent on -1 gives 1. (-1)²⁰²⁶ = 1",
            "1", ["-1", "0", "2026"]
        ),
        (
            "What is the value of (-1)²⁰²⁵?",
            "Odd exponent on -1 gives -1. (-1)²⁰²⁵ = -1",
            "-1", ["1", "0", "-2025"]
        ),
        (
            "If a² = 49, what are the possible values of a?",
            "a = 7 or a = -7",
            "7 or -7", ["7 only", "-7 only", "49"]
        ),
        (
            "Which is larger: 2³⁰⁰ or 3²⁰⁰?",
            "Compare: 2³ = 8 vs 3² = 9. So 3² > 2³. Raising both to 100th power: 3²⁰⁰ > 2³⁰⁰",
            "3²⁰⁰", ["2³⁰⁰", "They are equal", "Cannot be determined"]
        ),
        (
            "What is 0.1⁻² equal to?",
            "0.1⁻² = (1/10)⁻² = 10² = 100",
            "100", ["0.01", "-0.01", "10"]
        ),
        (
            "Simplify: (√2)⁶",
            "(√2)⁶ = (2^(1/2))⁶ = 2³ = 8",
            "8", ["4", "2√2", "16"]
        ),
        (
            "What is the units digit of 7²⁰²³?",
            "Powers of 7 cycle: 7,9,3,1. 2023 mod 4 = 3. Third in cycle = 3.",
            "3", ["7", "9", "1"]
        ),
        (
            "What is the units digit of 3¹⁰⁰?",
            "Powers of 3 cycle: 3,9,7,1. 100 mod 4 = 0. Fourth in cycle = 1.",
            "1", ["3", "9", "7"]
        ),
        (
            "If 2^a = 8 and 2^b = 32, what is 2^(a+b)?",
            "a=3, b=5. 2^(3+5) = 2⁸ = 256",
            "256", ["40", "128", "512"]
        ),
        (
            "If 3^x = 9 and 3^y = 27, what is 3^(x×y)?",
            "x=2, y=3. 3^(2×3) = 3⁶ = 729",
            "729", ["243", "81", "2187"]
        ),
        (
            "Simplify: 2^(1/2) × 2^(1/3) × 2^(1/6)",
            "2^(1/2 + 1/3 + 1/6) = 2^(3/6 + 2/6 + 1/6) = 2^(6/6) = 2¹ = 2",
            "2", ["4", "8", "√2"]
        ),
        (
            "What is (0.5)⁻³?",
            "(1/2)⁻³ = 2³ = 8",
            "8", ["-0.125", "0.125", "-8"]
        ),
        (
            "If √(x+5) = 7, what is x?",
            "Square both sides: x+5 = 49, so x = 44",
            "44", ["2", "49", "12"]
        ),
        (
            "If ∛(2x+1) = 3, what is x?",
            "Cube both sides: 2x+1 = 27, 2x = 26, x = 13",
            "13", ["9", "14", "27"]
        ),
        (
            "What is √(√81)?",
            "√81 = 9, then √9 = 3",
            "3", ["9", "√9", "81"]
        ),
        (
            "What is ∛(√64)?",
            "√64 = 8, then ∛8 = 2",
            "2", ["4", "8", "√8"]
        ),
        (
            "Simplify: (2^10 - 2^9) ÷ 2^8",
            "2^9(2-1) ÷ 2^8 = 2^9 ÷ 2^8 = 2",
            "2", ["1", "4", "512"]
        ),
        (
            "Simplify: (3^6 + 3^6 + 3^6) ÷ 3^5",
            "3 × 3^6 ÷ 3^5 = 3^7 ÷ 3^5 = 3² = 9",
            "9", ["3", "27", "6"]
        ),
        (
            "If 4^x = 8, what is x?",
            "(2²)^x = 2³ → 2^(2x) = 2³ → 2x = 3 → x = 3/2",
            "3/2", ["2", "3/4", "2/3"]
        ),
        (
            "If 9^x = 27, what is x?",
            "(3²)^x = 3³ → 3^(2x) = 3³ → 2x = 3 → x = 3/2",
            "3/2", ["2", "3", "2/3"]
        ),
    ]
    for question, expl, ans_str, dists in conceptual:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            question,
            choices, correct,
            f"{expl}.",
            ["conceptual", "advanced", "problem solving"],
        ))
        qid += 1

    # --- Block 9: Mixed expressions with radicals and exponents (15 questions) ---
    mixed_final = [
        ("√(3⁴)", "3² = 9", "9", ["3", "27", "81"]),
        ("∛(2⁹)", "2³ = 8", "8", ["4", "16", "512"]),
        ("√(5⁶)", "5³ = 125", "125", ["25", "625", "5"]),
        ("∛(3⁶)", "3² = 9", "9", ["27", "3", "81"]),
        ("(√3)⁴", "3² = 9", "9", ["3", "27", "√81"]),
        ("(∛2)⁹", "2³ = 8", "8", ["4", "16", "2"]),
        ("(√5)⁶", "5³ = 125", "125", ["25", "5", "625"]),
        ("√(2⁶ × 3²)", "2³ × 3 = 24", "24", ["12", "36", "18"]),
        ("∛(8 × 27)", "∛216 = 6", "6", ["12", "3", "9"]),
        ("√(4⁵)", "4^(5/2) = (√4)⁵ = 2⁵ = 32", "32", ["16", "64", "8"]),
        ("√(16 × 25 × 9)", "4 × 5 × 3 = 60", "60", ["30", "120", "45"]),
        ("∛(125 × 8)", "∛1000 = 10", "10", ["5", "20", "100"]),
        ("(3²)^(1/2) × (2³)^(1/3)", "3 × 2 = 6", "6", ["5", "9", "12"]),
        ("(4^(1/2))³ + (8^(1/3))²", "2³ + 2² = 8 + 4 = 12", "12", ["10", "6", "16"]),
        ("(9^(1/2) + 4^(1/2))²", "(3 + 2)² = 25", "25", ["13", "5", "49"]),
    ]
    for expr, expl, ans_str, dists in mixed_final:
        correct = ans_str
        distractors = [d for d in dists if d != correct][:3]
        choices = _shuffle_choices(correct, distractors)
        questions.append(_q(
            qid, "Hard",
            f"Evaluate: {expr}",
            choices, correct,
            f"{expl}.",
            ["mixed operations", "radicals and exponents", "advanced"],
        ))
        qid += 1

    return questions


def main() -> None:
    """Generate all 600 questions and write to JSON."""
    random.seed(42)  # Reproducible output

    easy = generate_easy_questions(start_id=1)
    medium = generate_medium_questions(start_id=201)
    hard = generate_hard_questions(start_id=401)

    all_questions = easy + medium + hard

    # Verify counts
    easy_count = sum(1 for q in all_questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in all_questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in all_questions if q["difficulty"] == "Hard")

    print(f"Generated {len(all_questions)} questions total:")
    print(f"  Easy: {easy_count}")
    print(f"  Medium: {medium_count}")
    print(f"  Hard: {hard_count}")

    # Validate all answers are in choices
    errors = []
    for q in all_questions:
        if q["answer"] not in q["choices"]:
            errors.append(f"ID {q['id']}: answer '{q['answer']}' not in choices {q['choices']}")
        if len(q["choices"]) != 4:
            errors.append(f"ID {q['id']}: has {len(q['choices'])} choices instead of 4")

    if errors:
        print(f"\n⚠️  {len(errors)} validation errors:")
        for e in errors[:20]:
            print(f"  - {e}")
    else:
        print("\n✅ All questions validated successfully.")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(all_questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWritten to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
