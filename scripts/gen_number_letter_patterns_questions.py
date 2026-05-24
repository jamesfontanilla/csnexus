"""Generate Number and Letter Patterns questions for Abstract Reasoning.

Produces 600 questions (200 Easy, 200 Medium, 200 Hard) with SVG visuals
for number sequences, letter sequences, and mixed patterns.

Usage:
    python scripts/gen_number_letter_patterns_questions.py

Outputs:
    data/seed/questions/analytical-ability/abstract-reasoning/
        number-and-letter-patterns/questions.json
    data/seed/lessons/analytical-ability/abstract-reasoning/
        number-and-letter-patterns/lesson.md
"""

from __future__ import annotations

import json
import random
import re
import string
from pathlib import Path

random.seed(42)

OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "abstract-reasoning" / "number-and-letter-patterns"
)
OUTPUT_PATH = OUTPUT_DIR / "questions.json"

LESSON_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "lessons"
    / "analytical-ability" / "abstract-reasoning" / "number-and-letter-patterns"
    / "lesson.md"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------


def _svg_wrap(content: str, w: int = 400, h: int = 60) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _seq_svg(elements: list[str], w: int = 400, h: int = 60) -> str:
    """Render a sequence of text elements as SVG boxes with a ? at the end."""
    n = len(elements)
    total_slots = n + 1  # elements + question mark
    slot_w = w // total_slots
    parts: list[str] = []
    for i, el in enumerate(elements):
        cx = slot_w * i + slot_w // 2
        cy = h // 2
        # box
        bx = cx - slot_w // 2 + 4
        by = 8
        bw = slot_w - 8
        bh = h - 16
        parts.append(
            f"<rect x='{bx}' y='{by}' width='{bw}' height='{bh}' "
            f"fill='#f8f9fa' stroke='#dee2e6' rx='4'/>"
        )
        parts.append(
            f"<text x='{cx}' y='{cy + 5}' text-anchor='middle' "
            f"font-size='14' fill='#212529' font-family='monospace'>"
            f"{el}</text>"
        )
    # question mark slot
    cx = slot_w * n + slot_w // 2
    cy = h // 2
    bx = cx - slot_w // 2 + 4
    parts.append(
        f"<rect x='{bx}' y='8' width='{slot_w - 8}' height='{h - 16}' "
        f"fill='#fff3cd' stroke='#ffc107' rx='4' stroke-dasharray='4,2'/>"
    )
    parts.append(
        f"<text x='{cx}' y='{cy + 5}' text-anchor='middle' "
        f"font-size='16' fill='#856404' font-family='sans-serif'>?</text>"
    )
    return _svg_wrap("".join(parts), w=w, h=h)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

ALPHABET = string.ascii_uppercase  # A-Z


def _letter_pos(ch: str) -> int:
    """Return 1-based position of a letter (A=1, Z=26)."""
    return ord(ch.upper()) - ord('A') + 1


def _pos_letter(pos: int) -> str:
    """Return letter for 1-based position, wrapping around."""
    return ALPHABET[(pos - 1) % 26]


def _make_question(
    id_: int,
    difficulty: str,
    question: str,
    svg_question: str,
    choices: list[str],
    answer: str,
    explanation: str,
    tags: list[str],
) -> dict:
    """Build a question dict in the project's standard format."""
    return {
        "id": id_,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Number and Letter Patterns",
        "difficulty": difficulty,
        "question": f"{question}\n\n{svg_question}",
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


# ---------------------------------------------------------------------------
# EASY question generators — Number Sequences
# ---------------------------------------------------------------------------


def gen_add_constant(id_: int) -> dict:
    """Arithmetic sequence with constant addition (e.g., +3)."""
    step = random.randint(2, 9)
    start = random.randint(1, 20)
    seq = [start + step * i for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each number increases by {step}. "
                    f"{seq[3]} + {step} = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "arithmetic sequence",
              "addition"],
    )


def gen_subtract_constant(id_: int) -> dict:
    """Arithmetic sequence with constant subtraction."""
    step = random.randint(2, 8)
    start = random.randint(40, 80)
    seq = [start - step * i for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each number decreases by {step}. "
                    f"{seq[3]} - {step} = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "arithmetic sequence",
              "subtraction"],
    )


def gen_multiply_constant(id_: int) -> dict:
    """Geometric sequence with constant multiplication (×2, ×3)."""
    factor = random.choice([2, 3])
    start = random.randint(1, 5)
    seq = [start * (factor ** i) for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each number is multiplied by {factor}. "
                    f"{seq[3]} × {factor} = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "geometric sequence",
              "multiplication"],
    )


def gen_squares(id_: int) -> dict:
    """Perfect squares: 1, 4, 9, 16, 25..."""
    start_n = random.randint(1, 6)
    seq = [(start_n + i) ** 2 for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    n = start_n + 4
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are perfect squares: {start_n}²={seq[0]}, "
                    f"{start_n+1}²={seq[1]}, ... {n}²={seq[4]}.",
        tags=["abstract reasoning", "number patterns", "perfect squares"],
    )


def gen_add_increasing(id_: int) -> dict:
    """Differences increase by 1 each time: +1, +2, +3, +4..."""
    start = random.randint(1, 10)
    base_step = random.randint(1, 3)
    seq = [start]
    for i in range(4):
        seq.append(seq[-1] + base_step + i)
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    diffs = [seq[i+1] - seq[i] for i in range(4)]
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The differences increase by 1 each time: "
                    f"{', '.join('+' + str(d) for d in diffs)}. "
                    f"Next: {seq[3]} + {diffs[-1]} = {seq[4]}.",
        tags=["abstract reasoning", "number patterns",
              "increasing differences"],
    )


# ---------------------------------------------------------------------------
# EASY question generators — Letter Sequences
# ---------------------------------------------------------------------------


def gen_letter_forward(id_: int) -> dict:
    """Letters advance by a constant step (e.g., +2: A, C, E, G)."""
    step = random.randint(1, 3)
    start_pos = random.randint(1, 20)
    seq = [_pos_letter(start_pos + step * i) for i in range(5)]
    shown = seq[:4]
    answer = seq[4]
    wrong = _letter_distractors(start_pos + step * 4, step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What letter comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each letter advances {step} position(s) in the alphabet. "
                    f"After {shown[3]}, the next is {answer}.",
        tags=["abstract reasoning", "letter patterns",
              "forward progression"],
    )


def gen_letter_backward(id_: int) -> dict:
    """Letters go backward by a constant step (e.g., -2: Z, X, V, T)."""
    step = random.randint(1, 3)
    start_pos = random.randint(20, 26)
    seq = [_pos_letter(start_pos - step * i) for i in range(5)]
    shown = seq[:4]
    answer = seq[4]
    target_pos = start_pos - step * 4
    wrong = _letter_distractors(target_pos, step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What letter comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each letter moves {step} position(s) backward. "
                    f"After {shown[3]}, the next is {answer}.",
        tags=["abstract reasoning", "letter patterns",
              "backward progression"],
    )


def gen_letter_vowels(id_: int) -> dict:
    """Vowel sequence: A, E, I, O, U (or subsets)."""
    vowels = ['A', 'E', 'I', 'O', 'U']
    start = random.randint(0, 1)
    seq = vowels[start:start + 5] if start == 0 else vowels[start:] + vowels[:start]
    # Use first 4, ask for 5th
    if len(seq) < 5:
        seq = vowels + vowels  # wrap
        seq = seq[start:start + 5]
    shown = seq[:4]
    answer = seq[4]
    wrong_pool = [v for v in 'BCDFG' ]
    wrong = random.sample(wrong_pool, 3)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What letter comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The sequence follows the vowels in order: "
                    f"A, E, I, O, U. The next vowel is {answer}.",
        tags=["abstract reasoning", "letter patterns", "vowels"],
    )


def gen_even_numbers(id_: int) -> dict:
    """Even number sequence: 2, 4, 6, 8..."""
    start = random.choice([2, 4, 6, 8, 10])
    seq = [start + 2 * i for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], 2)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are consecutive even numbers (+2 each time). "
                    f"{seq[3]} + 2 = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "even numbers"],
    )


def gen_odd_numbers(id_: int) -> dict:
    """Odd number sequence: 1, 3, 5, 7..."""
    start = random.choice([1, 3, 5, 7, 9, 11])
    seq = [start + 2 * i for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], 2)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are consecutive odd numbers (+2 each time). "
                    f"{seq[3]} + 2 = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "odd numbers"],
    )


def gen_simple_mixed(id_: int) -> dict:
    """Simple mixed pattern: A1, B2, C3, D4, ?"""
    start_letter = random.randint(1, 20)
    start_num = random.randint(1, 5)
    seq = [f"{_pos_letter(start_letter + i)}{start_num + i}" for i in range(5)]
    shown = seq[:4]
    answer = seq[4]
    # Distractors
    wrong = [
        f"{_pos_letter(start_letter + 4)}{start_num + 3}",  # wrong number
        f"{_pos_letter(start_letter + 3)}{start_num + 4}",  # wrong letter
        f"{_pos_letter(start_letter + 5)}{start_num + 5}",  # both off by 1
    ]
    # Ensure no duplicates with answer
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append(f"{_pos_letter(start_letter + 6)}{start_num + 6}")
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Both the letter and number advance by 1 each step. "
                    f"After {shown[3]}, the next is {answer}.",
        tags=["abstract reasoning", "mixed patterns",
              "number-letter sequence"],
    )


def gen_counting_by_five(id_: int) -> dict:
    """Counting by 5: 5, 10, 15, 20..."""
    start = random.choice([5, 10, 15, 20, 25])
    seq = [start + 5 * i for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], 5)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each number increases by 5. "
                    f"{seq[3]} + 5 = {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "skip counting"],
    )


# ---------------------------------------------------------------------------
# MEDIUM question generators
# ---------------------------------------------------------------------------


def gen_alternating_add_sub(id_: int) -> dict:
    """Alternating +a, -b pattern: e.g., +5, -2, +5, -2..."""
    a = random.randint(3, 8)
    b = random.randint(1, a - 1)
    start = random.randint(5, 20)
    seq = [start]
    for i in range(5):
        if i % 2 == 0:
            seq.append(seq[-1] + a)
        else:
            seq.append(seq[-1] - b)
    # Show first 5, ask for 6th
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], a)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    op = f"+{a}" if len(seq) % 2 == 0 else f"-{b}"
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The pattern alternates: +{a}, -{b}, +{a}, -{b}... "
                    f"After {seq[4]}, apply {op} = {seq[5]}.",
        tags=["abstract reasoning", "number patterns",
              "alternating operations"],
    )


def gen_fibonacci_like(id_: int) -> dict:
    """Fibonacci-like: each term = sum of previous two."""
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    seq = [a, b]
    for _ in range(4):
        seq.append(seq[-1] + seq[-2])
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], seq[5] - seq[4])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each term is the sum of the two preceding terms. "
                    f"{seq[3]} + {seq[4]} = {seq[5]}.",
        tags=["abstract reasoning", "number patterns", "fibonacci"],
    )


def gen_letter_skip_increasing(id_: int) -> dict:
    """Letter skips increase: +1, +2, +3, +4..."""
    start_pos = random.randint(1, 10)
    positions = [start_pos]
    for i in range(1, 6):
        positions.append(positions[-1] + i)
    seq = [_pos_letter(p) for p in positions]
    shown = seq[:5]
    answer = seq[5]
    target_pos = positions[5]
    wrong = _letter_distractors(target_pos, 5)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    skips = [positions[i+1] - positions[i] for i in range(5)]
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What letter comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The gaps between letters increase by 1: "
                    f"{', '.join('+' + str(s) for s in skips)}. "
                    f"Next gap is +{skips[-1]}, giving {answer}.",
        tags=["abstract reasoning", "letter patterns",
              "increasing intervals"],
    )


def gen_two_interleaved_numbers(id_: int) -> dict:
    """Two interleaved sequences: odd positions +a, even positions +b."""
    a = random.randint(2, 5)
    b = random.randint(2, 5)
    s1_start = random.randint(1, 10)
    s2_start = random.randint(10, 20)
    seq = []
    for i in range(4):
        seq.append(s1_start + a * (i // 1) if i % 2 == 0
                   else s2_start + b * ((i - 1) // 1))
    # Rebuild properly
    s1 = [s1_start + a * i for i in range(3)]
    s2 = [s2_start + b * i for i in range(3)]
    seq = []
    for i in range(3):
        seq.append(s1[i])
        seq.append(s2[i])
    # Show 5, ask for 6th
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], b)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Two interleaved sequences: odd positions increase by "
                    f"{a} ({', '.join(str(x) for x in s1)}), even positions "
                    f"increase by {b} ({', '.join(str(x) for x in s2)}). "
                    f"Next even-position term: {seq[5]}.",
        tags=["abstract reasoning", "number patterns",
              "interleaved sequences"],
    )


def gen_cubes(id_: int) -> dict:
    """Cube numbers: 1, 8, 27, 64, 125..."""
    start_n = random.randint(1, 4)
    seq = [(start_n + i) ** 3 for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    n = start_n + 4
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are perfect cubes: {start_n}³={seq[0]}, "
                    f"{start_n+1}³={seq[1]}, ... {n}³={seq[4]}.",
        tags=["abstract reasoning", "number patterns", "perfect cubes"],
    )


def gen_prime_numbers(id_: int) -> dict:
    """Prime number sequence."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    start = random.randint(0, 8)
    seq = primes[start:start + 5]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are consecutive prime numbers. "
                    f"After {seq[3]}, the next prime is {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "prime numbers"],
    )


def gen_mixed_letter_number_step(id_: int) -> dict:
    """Mixed: letter +2, number ×2 (e.g., A2, C4, E8, G16, ?)."""
    l_step = random.randint(1, 3)
    n_factor = random.choice([2, 3])
    l_start = random.randint(1, 15)
    n_start = random.choice([1, 2, 3])
    seq = []
    for i in range(5):
        letter = _pos_letter(l_start + l_step * i)
        number = n_start * (n_factor ** i)
        seq.append(f"{letter}{number}")
    shown = seq[:4]
    answer = seq[4]
    # Distractors
    wrong = [
        f"{_pos_letter(l_start + l_step * 4)}{n_start * (n_factor ** 3)}",
        f"{_pos_letter(l_start + l_step * 3)}{n_start * (n_factor ** 4)}",
        f"{_pos_letter(l_start + l_step * 5)}{n_start * (n_factor ** 4)}",
    ]
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append(f"{_pos_letter(l_start + l_step * 5)}{n_start * (n_factor ** 5)}")
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Letters advance by {l_step}, numbers multiply by "
                    f"{n_factor}. After {shown[3]}, next is {answer}.",
        tags=["abstract reasoning", "mixed patterns",
              "dual-rule sequence"],
    )


def gen_letter_pairs(id_: int) -> dict:
    """Letter pairs with pattern: AB, CD, EF, GH, ?"""
    start = random.randint(1, 18)
    step = random.choice([2, 2, 4])
    seq = []
    for i in range(5):
        pos = start + step * i
        pair = _pos_letter(pos) + _pos_letter(pos + 1)
        seq.append(pair)
    shown = seq[:4]
    answer = seq[4]
    wrong_pos = start + step * 4
    wrong = [
        _pos_letter(wrong_pos) + _pos_letter(wrong_pos + 2),
        _pos_letter(wrong_pos - 1) + _pos_letter(wrong_pos),
        _pos_letter(wrong_pos + 1) + _pos_letter(wrong_pos + 2),
    ]
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append(_pos_letter(wrong_pos + 2) + _pos_letter(wrong_pos + 3))
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What letter pair comes next?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each pair consists of consecutive letters, and pairs "
                    f"advance by {step} positions. After {shown[3]}, "
                    f"next is {answer}.",
        tags=["abstract reasoning", "letter patterns", "letter pairs"],
    )


def gen_triangular_numbers(id_: int) -> dict:
    """Triangular numbers: 1, 3, 6, 10, 15, 21..."""
    start_n = random.randint(1, 4)
    seq = []
    for i in range(start_n, start_n + 5):
        seq.append(i * (i + 1) // 2)
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are triangular numbers (sum of first n natural "
                    f"numbers). Differences increase by 1 each time. "
                    f"Next: {seq[3]} + {seq[4] - seq[3]} = {seq[4]}.",
        tags=["abstract reasoning", "number patterns",
              "triangular numbers"],
    )


def gen_multiply_then_add(id_: int) -> dict:
    """Pattern: ×2 then +1 alternating (e.g., 3, 6, 7, 14, 15...)."""
    start = random.randint(2, 5)
    factor = random.choice([2, 3])
    add = random.randint(1, 3)
    seq = [start]
    for i in range(5):
        if i % 2 == 0:
            seq.append(seq[-1] * factor)
        else:
            seq.append(seq[-1] + add)
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], abs(seq[5] - seq[4]))
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    op = f"×{factor}" if len(shown) % 2 == 1 else f"+{add}"
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The pattern alternates: ×{factor}, +{add}, ×{factor}, "
                    f"+{add}... After {seq[4]}, apply {op} = {seq[5]}.",
        tags=["abstract reasoning", "number patterns",
              "alternating operations", "multiply-add"],
    )


# ---------------------------------------------------------------------------
# HARD question generators
# ---------------------------------------------------------------------------


def gen_nested_operation(id_: int) -> dict:
    """Nested: differences of differences are constant."""
    start = random.randint(1, 5)
    d1 = random.randint(2, 4)
    d2 = random.randint(1, 3)
    # Build: second differences are constant d2
    first_diffs = [d1 + d2 * i for i in range(5)]
    seq = [start]
    for d in first_diffs:
        seq.append(seq[-1] + d)
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], first_diffs[-1])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"First differences: {', '.join(str(d) for d in first_diffs[:5])}. "
                    f"Second differences are constant (+{d2}). "
                    f"Next first diff: {first_diffs[4] + d2}, but shown 5 terms "
                    f"so next diff is {first_diffs[4]}. "
                    f"{seq[4]} + {first_diffs[4]} = {seq[5]}.",
        tags=["abstract reasoning", "number patterns",
              "second differences", "advanced"],
    )


def gen_power_sequence(id_: int) -> dict:
    """Powers of a base: 2^1, 2^2, 2^3... or 3^1, 3^2..."""
    base = random.choice([2, 3, 4])
    start_exp = random.randint(1, 3)
    seq = [base ** (start_exp + i) for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    exp = start_exp + 4
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"These are powers of {base}: {base}^{start_exp}={seq[0]}, "
                    f"{base}^{start_exp+1}={seq[1]}, ... "
                    f"{base}^{exp}={seq[4]}.",
        tags=["abstract reasoning", "number patterns", "powers",
              "exponential"],
    )


def gen_alternating_sign(id_: int) -> dict:
    """Alternating positive/negative with growing magnitude."""
    start = random.randint(1, 4)
    step = random.randint(1, 3)
    seq = []
    for i in range(6):
        val = (start + step * i) * ((-1) ** i)
        seq.append(val)
    shown = [str(x) for x in seq[:5]]
    answer = str(seq[5])
    wrong = _number_distractors(seq[5], step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Signs alternate (+, -, +, -...) while magnitude "
                    f"increases by {step}. Next: {seq[5]}.",
        tags=["abstract reasoning", "number patterns",
              "alternating signs", "advanced"],
    )


def gen_letter_mirror(id_: int) -> dict:
    """Letters mirror around a center: A, B, C, D, C, B or expanding."""
    center = random.randint(5, 14)
    # Build: go forward then backward — need at least 6 elements
    half = random.randint(3, 5)
    positions = list(range(center - half, center + 1)) + \
                list(range(center - 1, center - half - 1, -1))
    # Guarantee at least 6 positions
    if len(positions) < 6:
        positions = positions + positions
    seq = [_pos_letter(p) for p in positions[:6]]
    shown = seq[:5]
    answer = seq[5]
    target_pos = positions[5]
    wrong = _letter_distractors(target_pos, 1)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=480)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What letter comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"The sequence mirrors around the center letter "
                    f"{_pos_letter(center)}. After reaching the center, "
                    f"it reverses. Next: {answer}.",
        tags=["abstract reasoning", "letter patterns", "mirror",
              "palindrome"],
    )


def gen_dual_rule_mixed(id_: int) -> dict:
    """Hard mixed: letter goes backward, number follows squares."""
    l_start = random.randint(20, 26)
    l_step = random.randint(2, 3)
    n_start = random.randint(1, 3)
    seq = []
    for i in range(5):
        letter = _pos_letter(l_start - l_step * i)
        number = (n_start + i) ** 2
        seq.append(f"{letter}{number}")
    shown = seq[:4]
    answer = seq[4]
    # Distractors
    wrong_letter = _pos_letter(l_start - l_step * 4)
    wrong = [
        f"{_pos_letter(l_start - l_step * 3)}{(n_start + 4) ** 2}",
        f"{wrong_letter}{(n_start + 3) ** 2}",
        f"{_pos_letter(l_start - l_step * 5)}{(n_start + 4) ** 2}",
    ]
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append(f"{_pos_letter(l_start - l_step * 5)}{(n_start + 5) ** 2}")
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Letters go backward by {l_step} positions; numbers are "
                    f"perfect squares ({n_start}²={n_start**2}, "
                    f"{n_start+1}²={(n_start+1)**2}...). "
                    f"Next: {answer}.",
        tags=["abstract reasoning", "mixed patterns", "dual-rule",
              "advanced"],
    )


def gen_cyclic_letters(id_: int) -> dict:
    """Cyclic pattern: ABC, BCD, CDE... (sliding window)."""
    start = random.randint(1, 20)
    window = random.randint(3, 4)
    seq = []
    for i in range(5):
        group = "".join(_pos_letter(start + i + j) for j in range(window))
        seq.append(group)
    shown = seq[:4]
    answer = seq[4]
    wrong = [
        "".join(_pos_letter(start + 4 + j + 1) for j in range(window)),
        "".join(_pos_letter(start + 3 + j) for j in range(window)),
        "".join(_pos_letter(start + 5 + j) for j in range(window)),
    ]
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append("".join(_pos_letter(start + 6 + j) for j in range(window)))
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What letter group comes next?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"A sliding window of {window} consecutive letters moves "
                    f"forward by 1 position each step. After {shown[3]}, "
                    f"next is {answer}.",
        tags=["abstract reasoning", "letter patterns", "sliding window",
              "cyclic"],
    )


def gen_triple_operation(id_: int) -> dict:
    """Three operations cycle: +a, ×b, -c, +a, ×b, -c..."""
    a = random.randint(2, 5)
    b = random.choice([2, 3])
    c = random.randint(1, 3)
    start = random.randint(2, 6)
    seq = [start]
    ops = [f"+{a}", f"×{b}", f"-{c}"]
    for i in range(6):
        op_idx = i % 3
        if op_idx == 0:
            seq.append(seq[-1] + a)
        elif op_idx == 1:
            seq.append(seq[-1] * b)
        else:
            seq.append(seq[-1] - c)
    shown = [str(x) for x in seq[:6]]
    answer = str(seq[6])
    wrong = _number_distractors(seq[6], abs(seq[6] - seq[5]))
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=540)
    next_op = ops[5 % 3]
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Three operations cycle: {', '.join(ops)}. "
                    f"After {seq[5]}, apply {next_op} = {seq[6]}.",
        tags=["abstract reasoning", "number patterns",
              "triple operation cycle", "advanced"],
    )


def gen_interleaved_letters_numbers(id_: int) -> dict:
    """Interleaved: A, 1, B, 2, C, 3, D, ? (number follows letter)."""
    l_start = random.randint(1, 20)
    n_start = random.randint(1, 10)
    l_step = random.randint(1, 2)
    n_step = random.randint(1, 3)
    seq = []
    for i in range(4):
        seq.append(_pos_letter(l_start + l_step * i))
        seq.append(str(n_start + n_step * i))
    # Show 7, ask for 8th
    shown = [str(x) for x in seq[:7]]
    answer = str(seq[7])
    wrong = _number_distractors(int(answer), n_step)
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown, w=560)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Letters and numbers alternate. Letters advance by "
                    f"{l_step}, numbers advance by {n_step}. "
                    f"Next number: {answer}.",
        tags=["abstract reasoning", "mixed patterns", "interleaved",
              "advanced"],
    )


def gen_square_plus_constant(id_: int) -> dict:
    """n² + k pattern: 2, 5, 10, 17, 26... (n² + 1)."""
    k = random.randint(0, 5)
    start_n = random.randint(1, 3)
    seq = [(start_n + i) ** 2 + k for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    n = start_n + 4
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Pattern: n² + {k}. Values: {start_n}²+{k}={seq[0]}, "
                    f"{start_n+1}²+{k}={seq[1]}, ... {n}²+{k}={seq[4]}.",
        tags=["abstract reasoning", "number patterns", "quadratic",
              "advanced"],
    )


def gen_product_adjacent(id_: int) -> dict:
    """Each term = product of two adjacent natural numbers: 1×2, 2×3, 3×4..."""
    start_n = random.randint(1, 5)
    seq = [(start_n + i) * (start_n + i + 1) for i in range(5)]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    n = start_n + 4
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"Each term is n×(n+1): {start_n}×{start_n+1}={seq[0]}, "
                    f"{start_n+1}×{start_n+2}={seq[1]}, ... "
                    f"{n}×{n+1}={seq[4]}.",
        tags=["abstract reasoning", "number patterns",
              "product of consecutives", "advanced"],
    )


def gen_double_letter_reverse(id_: int) -> dict:
    """Letter pairs where first goes forward, second goes backward."""
    f_start = random.randint(1, 10)
    b_start = random.randint(20, 26)
    step = random.randint(1, 3)
    seq = []
    for i in range(5):
        pair = _pos_letter(f_start + step * i) + _pos_letter(b_start - step * i)
        seq.append(pair)
    shown = seq[:4]
    answer = seq[4]
    wrong = [
        _pos_letter(f_start + step * 3) + _pos_letter(b_start - step * 4),
        _pos_letter(f_start + step * 4) + _pos_letter(b_start - step * 3),
        _pos_letter(f_start + step * 5) + _pos_letter(b_start - step * 5),
    ]
    wrong = [w for w in wrong if w != answer][:3]
    while len(wrong) < 3:
        wrong.append(_pos_letter(f_start + step * 5) + _pos_letter(b_start - step * 4))
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What letter pair comes next?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"First letter advances by {step}, second letter "
                    f"retreats by {step}. After {shown[3]}, next: {answer}.",
        tags=["abstract reasoning", "letter patterns",
              "bidirectional", "advanced"],
    )


def gen_digit_sum_pattern(id_: int) -> dict:
    """Numbers whose digit sums follow a pattern."""
    # Numbers with digit sum increasing by 1: 10, 11, 12, 13, 14...
    # Or: 19, 28, 37, 46, 55 (digit sum = 10)
    target_sum = random.randint(5, 12)
    # Generate numbers with this digit sum in ascending order
    candidates = []
    for n in range(10, 200):
        if sum(int(d) for d in str(n)) == target_sum:
            candidates.append(n)
        if len(candidates) >= 6:
            break
    if len(candidates) < 5:
        # Fallback
        candidates = [target_sum + 9 * i for i in range(6)]
    seq = candidates[:5]
    shown = [str(x) for x in seq[:4]]
    answer = str(seq[4])
    wrong = _number_distractors(seq[4], seq[4] - seq[3])
    choices, answer_str = _build_choices(answer, wrong)
    svg = _seq_svg(shown)
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="What number comes next in the sequence?",
        svg_question=svg,
        choices=choices,
        answer=answer_str,
        explanation=f"All numbers have a digit sum of {target_sum}. "
                    f"The next number with digit sum {target_sum} is {seq[4]}.",
        tags=["abstract reasoning", "number patterns", "digit sum",
              "advanced"],
    )


# ---------------------------------------------------------------------------
# Distractor and choice helpers
# ---------------------------------------------------------------------------


def _number_distractors(correct: int, step: int) -> list[str]:
    """Generate 3 plausible wrong answers for a number sequence."""
    candidates = set()
    offsets = [step, -step, step * 2, -step * 2, 1, -1, 2, -2,
               step + 1, step - 1]
    for off in offsets:
        val = correct + off
        if val != correct and val > 0:
            candidates.add(str(val))
        if len(candidates) >= 6:
            break
    # Also add some near misses
    for off in [3, -3, 5, -5]:
        val = correct + off
        if val != correct and val > 0:
            candidates.add(str(val))
    candidates.discard(str(correct))
    result = list(candidates)
    random.shuffle(result)
    return result[:3]


def _letter_distractors(correct_pos: int, step: int) -> list[str]:
    """Generate 3 plausible wrong letter answers."""
    # Normalize position to 1-26 range
    norm_pos = ((correct_pos - 1) % 26) + 1
    candidates = set()
    offsets = [1, -1, step, -step, 2, -2, step + 1, step - 1, 3, -3]
    for off in offsets:
        pos = norm_pos + off
        if 1 <= pos <= 26 and pos != norm_pos:
            candidates.add(_pos_letter(pos))
    candidates.discard(_pos_letter(norm_pos))
    result = list(candidates)
    random.shuffle(result)
    return result[:3]


def _build_choices(
    answer: str, wrong: list[str]
) -> tuple[list[str], str]:
    """Shuffle answer among wrong choices, return (choices, answer_str)."""
    # Ensure exactly 3 wrong + 1 correct, all unique
    wrong = [w for w in wrong if w != answer]
    # Remove duplicates while preserving order
    seen: set[str] = set()
    unique_wrong: list[str] = []
    for w in wrong:
        if w not in seen:
            seen.add(w)
            unique_wrong.append(w)
    wrong = unique_wrong[:3]

    # Generate fallback distractors if needed
    fallback_idx = 1
    while len(wrong) < 3:
        # Try numeric offset first
        try:
            num = int(answer)
            candidate = str(num + fallback_idx * 2)
            if candidate != answer and candidate not in wrong:
                wrong.append(candidate)
            else:
                fallback_idx += 1
                continue
        except ValueError:
            # For letter/mixed answers, shift letters
            if len(answer) == 1 and answer.isalpha():
                pos = _letter_pos(answer)
                candidate = _pos_letter(pos + fallback_idx)
                if candidate != answer and candidate not in wrong:
                    wrong.append(candidate)
                else:
                    fallback_idx += 1
                    continue
            else:
                # Mixed alphanumeric — append a variant
                candidate = answer[:-1] + chr(ord(answer[-1]) + fallback_idx) if answer else f"X{fallback_idx}"
                if candidate != answer and candidate not in wrong:
                    wrong.append(candidate)
                else:
                    fallback_idx += 1
                    continue
        fallback_idx += 1
        if fallback_idx > 20:
            # Last resort
            while len(wrong) < 3:
                wrong.append(f"{answer}{len(wrong) + 1}")
            break

    options = wrong + [answer]
    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    choices = [f"{labels[i]}: {options[i]}" for i in range(4)]
    # Find the correct one
    answer_str = ""
    for c in choices:
        if c.split(": ", 1)[1] == answer:
            answer_str = c
            break
    return choices, answer_str



# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

EASY_GENERATORS = [
    gen_add_constant,
    gen_subtract_constant,
    gen_multiply_constant,
    gen_squares,
    gen_add_increasing,
    gen_letter_forward,
    gen_letter_backward,
    gen_letter_vowels,
    gen_even_numbers,
    gen_odd_numbers,
    gen_simple_mixed,
    gen_counting_by_five,
]

MEDIUM_GENERATORS = [
    gen_alternating_add_sub,
    gen_fibonacci_like,
    gen_letter_skip_increasing,
    gen_two_interleaved_numbers,
    gen_cubes,
    gen_prime_numbers,
    gen_mixed_letter_number_step,
    gen_letter_pairs,
    gen_triangular_numbers,
    gen_multiply_then_add,
]

HARD_GENERATORS = [
    gen_nested_operation,
    gen_power_sequence,
    gen_alternating_sign,
    gen_letter_mirror,
    gen_dual_rule_mixed,
    gen_cyclic_letters,
    gen_triple_operation,
    gen_interleaved_letters_numbers,
    gen_square_plus_constant,
    gen_product_adjacent,
    gen_double_letter_reverse,
    gen_digit_sum_pattern,
]


def _extract_sequence_key(q: dict) -> str:
    """Extract a deduplication key from the question's SVG sequence."""
    texts = re.findall(
        r"<text[^>]*font-family='monospace'[^>]*>([^<]+)</text>",
        q["question"]
    )
    return "|".join(texts) if texts else ""


def _generate_batch(
    generators: list, count: int, start_id: int,
    seen_keys: set[str] | None = None,
) -> list[dict]:
    """Generate `count` unique questions by cycling through generators."""
    if seen_keys is None:
        seen_keys = set()
    questions: list[dict] = []
    id_ = start_id
    attempts = 0
    max_attempts = count * 15  # safety valve

    while len(questions) < count and attempts < max_attempts:
        gen_fn = generators[attempts % len(generators)]
        attempts += 1
        try:
            q = gen_fn(id_)
        except (IndexError, ValueError, ZeroDivisionError):
            continue

        key = _extract_sequence_key(q)
        if key and key in seen_keys:
            continue  # skip duplicate
        if key:
            seen_keys.add(key)

        questions.append(q)
        id_ += 1

    return questions


def main() -> None:
    questions: list[dict] = []
    seen_keys: set[str] = set()  # shared across all difficulties

    # 200 Easy
    easy = _generate_batch(EASY_GENERATORS, 200, start_id=1, seen_keys=seen_keys)
    questions.extend(easy)

    # 200 Medium
    medium = _generate_batch(MEDIUM_GENERATORS, 200, start_id=201, seen_keys=seen_keys)
    questions.extend(medium)

    # 200 Hard
    hard = _generate_batch(HARD_GENERATORS, 200, start_id=401, seen_keys=seen_keys)
    questions.extend(hard)

    # Reassign IDs sequentially
    for i, q in enumerate(questions, 1):
        q["id"] = i

    # Verify counts
    easy_count = sum(1 for q in questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in questions if q["difficulty"] == "Hard")
    print(
        f"Generated: {len(questions)} total | "
        f"Easy: {easy_count}, Medium: {medium_count}, Hard: {hard_count}"
    )

    # Write questions JSON
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
