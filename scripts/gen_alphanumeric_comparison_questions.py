"""
Generate 600 alphanumeric comparison questions for the CSE reviewer.
Distribution: 200 Easy, 200 Medium, 200 Hard (IDs 1-200, 201-400, 401-600)

Question type targets (no single type > 18%):
  simple-pair      90  (15.0%)
  find-identical  105  (17.5%)
  find-different   95  (15.8%)
  error-type       90  (15.0%)
  count-identical  70  (11.7%)
  spot-the-error   70  (11.7%)
  mixed-record     45  ( 7.5%)
  position         35  ( 5.8%)
"""

import json
import random
from pathlib import Path

random.seed(42)

# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

AGENCIES = ["CSC", "COA", "DILG", "DBM", "DOH", "DOLE", "DPWH", "DOT",
            "DOJ", "DSWD", "NBI", "BIR", "BSP", "DENR", "DepEd"]
REGIONS  = ["NCR", "R1", "R2", "R3", "R4A", "R4B", "R5", "R6", "R7",
            "R8", "R9", "R10", "R11", "R12", "CAR", "BARMM"]
YEARS    = ["2022", "2023", "2024", "2025"]
MONTHS   = ["01", "02", "03", "04", "05", "06",
            "07", "08", "09", "10", "11", "12"]
BUDGET_TYPES = ["PS", "MOOE", "CO", "OR", "DV"]
BUDGET_CODES = ["101", "102", "201", "202", "205", "301", "302"]
POSITION_OFFICES = ["OSEC", "HRMO", "ADMIN", "LEGAL", "AUDIT", "PLANS"]

def rand_seq(width):
    return str(random.randint(1, 10**width - 1)).zfill(width)

# ---------------------------------------------------------------------------
# Code generators
# ---------------------------------------------------------------------------

def make_csc_code():
    ag = random.choice(AGENCIES)
    return f"{ag}-{random.choice(YEARS)}-{random.choice(MONTHS)}-{rand_seq(4)}"

def make_csc_regional_code():
    ag = random.choice(["CSC", "COA", "DILG", "DOH"])
    rg = random.choice(REGIONS)
    return f"{ag}-{rg}-{random.choice(YEARS)}-{rand_seq(3)}"

def make_budget_code():
    return f"{random.choice(BUDGET_TYPES)}-{random.choice(BUDGET_CODES)}-{random.choice(YEARS)}-{rand_seq(3)}"

def make_position_code():
    return f"{random.choice(POSITION_OFFICES)}-{rand_seq(5)}-{rand_seq(3)}"

def make_obligation_code():
    bt = random.choice(["OR", "DV", "OBR"])
    return f"{bt}-{random.choice(BUDGET_CODES)}-{random.choice(YEARS)}-{random.choice(MONTHS)}-{rand_seq(4)}"

def make_short_code():
    ag = random.choice(["COA", "CSC", "NBI", "BIR"])
    return f"{ag}-R{random.randint(1,13)}-{rand_seq(3)}"

def make_saln_code():
    """SALN-YYYY-NNNNN"""
    return f"SALN-{random.choice(YEARS)}-{rand_seq(5)}"

def make_leave_code():
    """LF-YYYY-MM-NNNNN"""
    return f"LF-{random.choice(YEARS)}-{random.choice(MONTHS)}-{rand_seq(5)}"

def make_payroll_code():
    """PR-YYYY-MM-NNN"""
    return f"PR-{random.choice(YEARS)}-{random.choice(MONTHS)}-{rand_seq(3)}"

def make_check_code():
    """CHK-NNNNNNNN"""
    return f"CHK-{rand_seq(8)}"

def random_code(complexity="simple"):
    if complexity == "simple":
        return random.choice([make_short_code, make_budget_code, make_payroll_code])()
    elif complexity == "medium":
        return random.choice([make_csc_code, make_csc_regional_code,
                               make_budget_code, make_saln_code, make_leave_code])()
    else:
        return random.choice([make_csc_regional_code, make_position_code,
                               make_obligation_code, make_check_code])()

# ---------------------------------------------------------------------------
# Error injectors
# ---------------------------------------------------------------------------

def inject_substitution(code):
    chars = list(code)
    candidates = [i for i, c in enumerate(chars) if c not in "-./"]
    if not candidates:
        return None, None
    pos = random.choice(candidates)
    orig = chars[pos]
    digit_subs = {"0": "8", "1": "7", "2": "3", "3": "8", "4": "9",
                  "5": "6", "6": "8", "7": "1", "8": "3", "9": "6"}
    letter_subs = {"O": "0", "I": "1", "S": "5", "Z": "2", "B": "8",
                   "G": "6", "A": "4", "E": "3", "C": "G", "D": "O"}
    if orig in digit_subs:
        new = digit_subs[orig]
    elif orig in letter_subs:
        new = letter_subs[orig]
    elif orig.isdigit():
        new = str((int(orig) + random.randint(1, 8)) % 10)
    else:
        new = chr((ord(orig) - ord('A') + random.randint(1, 5)) % 26 + ord('A'))
    if new == orig:
        new = chr((ord(orig) - ord('A') + 3) % 26 + ord('A')) if orig.isalpha() else str((int(orig)+3)%10)
    chars[pos] = new
    return "".join(chars), f"substitution at position {pos+1} ('{orig}'→'{new}')"

def inject_transposition(code):
    chars = list(code)
    candidates = [i for i in range(len(chars)-1)
                  if chars[i] not in "-./\\" and chars[i+1] not in "-./\\"
                  and chars[i] != chars[i+1]]
    if not candidates:
        return None, None
    pos = random.choice(candidates)
    chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
    return "".join(chars), f"transposition at positions {pos+1}-{pos+2}"

def inject_omission(code):
    chars = list(code)
    candidates = [i for i, c in enumerate(chars) if c not in "-./"]
    if not candidates:
        return None, None
    pos = random.choice(candidates)
    removed = chars[pos]
    del chars[pos]
    return "".join(chars), f"omission of '{removed}' at position {pos+1}"

def inject_addition(code):
    chars = list(code)
    candidates = [i for i, c in enumerate(chars) if c not in "-./"]
    if not candidates:
        return None, None
    pos = random.choice(candidates)
    orig = chars[pos]
    extra = str(random.randint(0, 9)) if orig.isdigit() else chr(random.randint(ord('A'), ord('Z')))
    chars.insert(pos, extra)
    return "".join(chars), f"addition of '{extra}' at position {pos+1}"

def inject_separator_change(code):
    if "-" not in code:
        return None, None
    new_sep = random.choice([".", "/", " "])
    idx = code.index("-")
    return code[:idx] + new_sep + code[idx+1:], f"separator changed from '-' to '{new_sep}'"

def inject_leading_zero(code):
    parts = code.split("-")
    candidates = [i for i, p in enumerate(parts) if p.startswith("0") and len(p) > 1 and p.isdigit()]
    if not candidates:
        return None, None
    idx = random.choice(candidates)
    parts[idx] = parts[idx][1:]
    return "-".join(parts), f"omission of leading zero in segment {idx+1}"

EASY_INJECTORS   = [inject_substitution, inject_transposition]
MEDIUM_INJECTORS = [inject_substitution, inject_transposition, inject_omission, inject_separator_change]
HARD_INJECTORS   = [inject_substitution, inject_transposition, inject_omission, inject_addition,
                    inject_separator_change, inject_leading_zero]

def apply_injector(code, injectors, max_tries=20):
    """Try injectors until one produces a valid modification."""
    for _ in range(max_tries):
        inj = random.choice(injectors)
        mod, desc = inj(code)
        if mod and mod != code:
            return mod, desc
    # fallback: substitute last char
    mod = code[:-1] + ("9" if code[-1] != "9" else "8")
    return mod, "substitution at last position"

# ---------------------------------------------------------------------------
# Error classification helpers
# ---------------------------------------------------------------------------

def _derive_error_type(a, b):
    """Derive canonical error type label from two strings."""
    if a == b:
        return "Substitution"
    if len(a) == len(b):
        diffs = [(i, ca, cb) for i, (ca, cb) in enumerate(zip(a, b)) if ca != cb]
        if len(diffs) == 2:
            i, ca, cb = diffs[0]
            j, da, db = diffs[1]
            if j == i + 1 and ca == db and cb == da:
                return "Transposition"
        return "Substitution"
    return "Omission" if len(a) > len(b) else "Addition"

def _answer_label_for_diff(code_a, code_b):
    """Pick the best-fit 'No, they differ by...' choice label."""
    t = _derive_error_type(code_a, code_b)
    if t in ("Omission", "Addition"):
        segs_a, segs_b = code_a.split("-"), code_b.split("-")
        is_lz = any(
            sa.isdigit() and sb.isdigit() and len(sa) != len(sb)
            for sa, sb in zip(segs_a, segs_b)
        ) or len(segs_a) != len(segs_b)
        return "No, they differ by a leading zero" if (is_lz and t == "Omission") else "No, they differ by one character"
    sep_a = [c for c in code_a if c in "-./\\ "]
    sep_b = [c for c in code_b if c in "-./\\ "]
    if sep_a != sep_b:
        return "No, they differ by spacing or separators"
    return "No, they differ by one character"

# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def build_q(qid, difficulty, question, choices, answer, explanation, tags):
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Alphanumeric Comparison",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }

# ---------------------------------------------------------------------------
# Question builders
# ---------------------------------------------------------------------------

# ── Type 1: Simple pair ───────────────────────────────────────────────────

SIMPLE_PAIR_STEMS = [
    "Are the following codes EXACTLY identical?",
    "Do the two codes below match exactly?",
    "Compare the two codes. Are they exactly the same?",
    "Are Code A and Code B identical in every character?",
    "Do these two document codes match character for character?",
]

def make_simple_pair_question(qid, difficulty, code_complexity, injectors):
    """Simple pair — 50% identical, 50% different."""
    stem = random.choice(SIMPLE_PAIR_STEMS)
    identical = random.random() < 0.5
    code = random_code(code_complexity)
    if identical:
        code_a, code_b = code, code
        answer = "Yes, they are identical"
        explanation = f"Both codes are exactly '{code}' — every character, separator, and leading zero matches."
        tags = ["simple-pair", "identical", "alphanumeric-code"]
    else:
        mod, desc = apply_injector(code, injectors)
        code_a, code_b = (code, mod) if random.random() < 0.5 else (mod, code)
        answer = _answer_label_for_diff(code_a, code_b)
        explanation = f"The codes are NOT identical. Difference: {desc}. Compare character by character, segment by segment."
        tags = ["simple-pair", "different", "alphanumeric-code"]
    choices = [
        "Yes, they are identical",
        "No, they differ by one character",
        "No, they differ by spacing or separators",
        "No, they differ by a leading zero",
    ]
    question = f"{stem}\n\nCode A: {code_a}\nCode B: {code_b}"
    return build_q(qid, difficulty, question, choices, answer, explanation, tags)

# ── Type 2: Find-identical ────────────────────────────────────────────────

FIND_IDENTICAL_STEMS = [
    "Which of the following pairs of codes is EXACTLY identical?",
    "Which pair below shows two codes that match perfectly?",
    "Identify the pair where both codes are exactly the same.",
    "Which of the following code pairs has NO discrepancy?",
    "Select the pair where Code A and Code B are identical.",
]

def make_find_identical_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(FIND_IDENTICAL_STEMS)
    correct_code = random_code(code_complexity)
    pairs = [(correct_code, correct_code)]
    for _ in range(3):
        c = random_code(code_complexity)
        mod, _ = apply_injector(c, injectors)
        pairs.append((c, mod))
    random.shuffle(pairs)
    correct_idx = next(i for i, (a, b) in enumerate(pairs) if a == b)
    labels = ["A", "B", "C", "D"]
    choices = [f"{labels[i]}. {p[0]}  /  {p[1]}" for i, p in enumerate(pairs)]
    answer = choices[correct_idx]
    explanation = (f"Pair {labels[correct_idx]} ({pairs[correct_idx][0]}) is identical — "
                   f"all characters, separators, and leading zeros match. "
                   f"The other pairs each contain at least one discrepancy.")
    return build_q(qid, difficulty, stem, choices, answer, explanation,
                   ["find-identical", "alphanumeric-code"])

# ── Type 3: Find-different ────────────────────────────────────────────────

FIND_DIFFERENT_STEMS = [
    "Which of the following pairs of codes is NOT exactly identical?",
    "Which pair below contains a discrepancy?",
    "Identify the pair where the two codes do NOT match.",
    "Which code pair has at least one character difference?",
    "Select the pair where Code A and Code B differ.",
]

def make_find_different_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(FIND_DIFFERENT_STEMS)
    pairs = [(random_code(code_complexity),) * 2 for _ in range(3)]
    pairs = [(c, c) for c in [random_code(code_complexity) for _ in range(3)]]
    c = random_code(code_complexity)
    mod, desc = apply_injector(c, injectors)
    pairs.append((c, mod))
    random.shuffle(pairs)
    diff_idx = next(i for i, (a, b) in enumerate(pairs) if a != b)
    labels = ["A", "B", "C", "D"]
    choices = [f"{labels[i]}. {p[0]}  /  {p[1]}" for i, p in enumerate(pairs)]
    answer = choices[diff_idx]
    explanation = (f"Pair {labels[diff_idx]} contains a discrepancy: {desc}. "
                   f"The other three pairs are exactly identical.")
    return build_q(qid, difficulty, stem, choices, answer, explanation,
                   ["find-different", "alphanumeric-code"])

# ── Type 4: Error-type ────────────────────────────────────────────────────

ERROR_TYPE_STEMS = [
    "What type of discrepancy exists between the following two codes?",
    "How would you classify the difference between these two codes?",
    "What kind of error was made when transcribing the second code?",
    "Which error type best describes the difference between Code A and Code B?",
    "A clerk transcribed Code A as Code B. What type of error occurred?",
]

def make_error_type_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(ERROR_TYPE_STEMS)
    code = random_code(code_complexity)
    mod, desc = apply_injector(code, injectors)
    code_a, code_b = (code, mod) if random.random() < 0.5 else (mod, code)
    error_type = _derive_error_type(code_a, code_b)
    all_types = ["Substitution", "Transposition", "Omission", "Addition"]
    distractors = [t for t in all_types if t != error_type]
    random.shuffle(distractors)
    choices = [error_type] + distractors[:3]
    random.shuffle(choices)
    explanation = (f"The discrepancy is a {error_type.lower()}: {desc}. "
                   f"Compare the codes character by character to locate the exact position.")
    question = f"{stem}\n\nCode A: {code_a}\nCode B: {code_b}"
    return build_q(qid, difficulty, question, choices, error_type, explanation,
                   ["error-type", "alphanumeric-code", error_type.lower()])

# ── Type 5: Count-identical ───────────────────────────────────────────────

COUNT_STEMS = [
    "How many of the following pairs of codes are EXACTLY identical?",
    "Count the pairs below where both codes match perfectly.",
    "How many of these code pairs have NO discrepancy?",
    "Among the following pairs, how many are exactly the same?",
    "How many pairs below are character-for-character identical?",
]

def make_count_identical_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(COUNT_STEMS)
    n_identical = random.randint(1, 4)
    pairs = []
    for _ in range(n_identical):
        c = random_code(code_complexity)
        pairs.append((c, c))
    for _ in range(5 - n_identical):
        c = random_code(code_complexity)
        mod, _ = apply_injector(c, injectors)
        pairs.append((c, mod))
    random.shuffle(pairs)
    lines = "\n".join(f"{i+1}. {a}    {b}" for i, (a, b) in enumerate(pairs))
    question = f"{stem}\n\n{lines}"
    answer = str(n_identical)
    wrong = [c for c in ["0","1","2","3","4","5"] if c != answer]
    random.shuffle(wrong)
    choices = sorted([answer] + wrong[:3], key=int)
    explanation = (f"Exactly {n_identical} pair(s) are identical. "
                   f"Compare each pair character by character, segment by segment.")
    return build_q(qid, difficulty, question, choices, answer,
                   explanation, ["count-identical", "alphanumeric-code"])

# ── Type 6: Spot-the-error (NEW) ──────────────────────────────────────────
# Given one base code repeated 4 times, one copy has an error. Find it.

SPOT_STEMS = [
    "Three of the following codes are identical. Which one is DIFFERENT?",
    "One of the codes below has been incorrectly transcribed. Which one?",
    "Which of the following codes does NOT match the others?",
    "A filing clerk copied a code four times. One copy contains an error. Which is it?",
    "Identify the code below that differs from the other three.",
]

def make_spot_the_error_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(SPOT_STEMS)
    base = random_code(code_complexity)
    mod, desc = apply_injector(base, injectors)
    # place the error at a random position among 4 choices
    error_pos = random.randint(0, 3)
    labels = ["A", "B", "C", "D"]
    codes = [base if i != error_pos else mod for i in range(4)]
    choices = [f"{labels[i]}. {codes[i]}" for i in range(4)]
    answer = choices[error_pos]
    explanation = (f"Choice {labels[error_pos]} ({mod}) differs from the others ({base}): {desc}. "
                   f"The remaining three choices are all identical to the original code.")
    return build_q(qid, difficulty, stem, choices, answer,
                   explanation, ["spot-the-error", "alphanumeric-code"])

# ── Type 7: Position ──────────────────────────────────────────────────────

POSITION_STEMS = [
    "At which character position does the FIRST difference occur between the following codes?",
    "Counting from left to right, at which position do these two codes first differ?",
    "At what position (left to right) is the first discrepancy between Code A and Code B?",
    "Which character position contains the first error when comparing these two codes?",
]

def make_position_question(qid, difficulty, code_complexity, injectors):
    stem = random.choice(POSITION_STEMS)
    code = random_code(code_complexity)
    mod, desc = apply_injector(code, [inject_substitution, inject_transposition])
    diff_pos = next((i+1 for i, (a, b) in enumerate(zip(code, mod)) if a != b), len(code))
    question = f"{stem}\n\nCode A: {code}\nCode B: {mod}"
    answer = str(diff_pos)
    # build 4 distinct numeric choices that include the correct answer
    max_pos = max(len(code), len(mod))
    candidates = set()
    for delta in [-3, -2, -1, 1, 2, 3, 4, 5]:
        p = diff_pos + delta
        if 1 <= p <= max_pos and p != diff_pos:
            candidates.add(str(p))
    wrong = list(candidates)
    random.shuffle(wrong)
    choices = sorted([answer] + wrong[:3], key=int)
    # if we still don't have 4, pad with sequential positions
    pos = 1
    while len(choices) < 4:
        s = str(pos)
        if s not in choices:
            choices.append(s)
        pos += 1
    choices = sorted(choices[:4], key=int)
    explanation = (f"The first difference is at character position {diff_pos}. "
                   f"Code A has '{code[diff_pos-1]}' while Code B has '{mod[diff_pos-1]}' at that position.")
    return build_q(qid, difficulty, question, choices, answer,
                   explanation, ["position-of-difference", "alphanumeric-code"])

# ── Type 8: Mixed record ──────────────────────────────────────────────────

MIXED_RECORD_STEMS = [
    "Are the following employee records EXACTLY identical?",
    "Do these two personnel records match in every detail?",
    "Compare the two records below. Are they exactly the same?",
    "A payroll clerk copied this record. Does the copy match the original?",
]

def make_mixed_record_question(qid, difficulty, injectors):
    surnames   = ["SANTOS","REYES","CRUZ","GARCIA","MENDOZA",
                  "BAUTISTA","VILLANUEVA","HERNANDEZ","GONZALES","AQUINO"]
    first_names = ["JUAN","MARIA","PEDRO","ELENA","JOSE",
                   "ANNA","ROBERTO","GRACE","ANTONIO","SOFIA"]
    initials   = ["A.","B.","C.","D.","E.","F.","G.","H.","J.","L."]
    sg_levels  = [f"SG-{n}-{s}" for n in range(10, 25) for s in range(1, 9)]
    stem = random.choice(MIXED_RECORD_STEMS)
    sn, fn, mi = random.choice(surnames), random.choice(first_names), random.choice(initials)
    emp_code = make_csc_code()
    sg = random.choice(sg_levels)
    record_a = f"{sn}, {fn} {mi}    {emp_code}    {sg}"
    if random.random() < 0.6:
        mod_code, desc = apply_injector(emp_code, injectors)
        record_b = f"{sn}, {fn} {mi}    {mod_code}    {sg}"
        answer = "No, they are NOT identical"
        explanation = f"The records differ in the employee code: {desc}. Compare each component separately."
    else:
        record_b = record_a
        answer = "Yes, they are identical"
        explanation = "Both records are exactly identical — name, employee code, and salary grade all match."
    question = f"{stem}\n\nRecord A: {record_a}\nRecord B: {record_b}"
    choices = ["Yes, they are identical", "No, they are NOT identical",
               "They differ only in the name portion", "They differ only in the salary grade"]
    return build_q(qid, difficulty, question, choices, answer,
                   explanation, ["mixed-record", "alphanumeric-code"])

# ---------------------------------------------------------------------------
# Main generation — balanced distribution
# ---------------------------------------------------------------------------
#
# Target per difficulty (200 each):
#   simple-pair      Easy:30  Med:30  Hard:30  → 90
#   find-identical   Easy:40  Med:35  Hard:30  → 105
#   find-different   Easy:30  Med:35  Hard:30  → 95
#   error-type       Easy:30  Med:30  Hard:30  → 90
#   count-identical  Easy:20  Med:25  Hard:25  → 70
#   spot-the-error   Easy:20  Med:25  Hard:25  → 70
#   mixed-record     Easy:10  Med:15  Hard:20  → 45
#   position         Easy:20  Med:5   Hard:10  → 35
#   TOTAL            Easy:200 Med:200 Hard:200 → 600

PLAN = {
    "Easy": [
        (30,  "simple_pair"),
        (40,  "find_identical"),
        (30,  "find_different"),
        (30,  "error_type"),
        (20,  "count_identical"),
        (20,  "spot_the_error"),
        (10,  "mixed_record"),
        (20,  "position"),
    ],
    "Medium": [
        (30,  "simple_pair"),
        (35,  "find_identical"),
        (35,  "find_different"),
        (30,  "error_type"),
        (25,  "count_identical"),
        (25,  "spot_the_error"),
        (15,  "mixed_record"),
        (5,   "position"),
    ],
    "Hard": [
        (30,  "simple_pair"),
        (30,  "find_identical"),
        (30,  "find_different"),
        (30,  "error_type"),
        (25,  "count_identical"),
        (25,  "spot_the_error"),
        (20,  "mixed_record"),
        (10,  "position"),
    ],
}

COMPLEXITY = {"Easy": "simple", "Medium": "medium", "Hard": "complex"}
INJECTORS  = {"Easy": EASY_INJECTORS, "Medium": MEDIUM_INJECTORS, "Hard": HARD_INJECTORS}

def generate_bank():
    questions = []
    qid = 1
    for diff in ["Easy", "Medium", "Hard"]:
        cx = COMPLEXITY[diff]
        inj = INJECTORS[diff]
        for count, qtype in PLAN[diff]:
            for _ in range(count):
                if qtype == "simple_pair":
                    q = make_simple_pair_question(qid, diff, cx, inj)
                elif qtype == "find_identical":
                    q = make_find_identical_question(qid, diff, cx, inj)
                elif qtype == "find_different":
                    q = make_find_different_question(qid, diff, cx, inj)
                elif qtype == "error_type":
                    q = make_error_type_question(qid, diff, cx, inj)
                elif qtype == "count_identical":
                    q = make_count_identical_question(qid, diff, cx, inj)
                elif qtype == "spot_the_error":
                    q = make_spot_the_error_question(qid, diff, cx, inj)
                elif qtype == "mixed_record":
                    q = make_mixed_record_question(qid, diff, inj)
                elif qtype == "position":
                    q = make_position_question(qid, diff, cx, inj)
                questions.append(q)
                qid += 1
    return questions


if __name__ == "__main__":
    bank = generate_bank()
    assert len(bank) == 600, f"Expected 600, got {len(bank)}"
    for diff, expected in [("Easy", 200), ("Medium", 200), ("Hard", 200)]:
        actual = sum(1 for q in bank if q["difficulty"] == diff)
        assert actual == expected, f"{diff}: {actual}"
    for i, q in enumerate(bank):
        assert q["id"] == i + 1
        assert q["answer"] in q["choices"], f"Q{q['id']}: answer not in choices"

    out = Path(__file__).parent.parent / (
        "data/seed/questions/clerical-ability/"
        "name-and-number-comparison/alphanumeric-comparison/questions.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)

    from collections import Counter
    types = Counter(q["tags"][0] for q in bank)
    print(f"Generated {len(bank)} questions → {out}")
    print("\nType distribution:")
    for t, n in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t:<22} {n:>4}  ({n/6:.1f}%)")
