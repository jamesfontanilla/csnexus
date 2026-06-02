"""
Generate 600 speed and accuracy drill questions for the CSE clerical ability reviewer.
Distribution: 200 Easy, 200 Medium, 200 Hard (IDs 1-200, 201-400, 401-600).

Easy: Single-field comparisons (names only, numbers only, codes only) — fast items.
Medium: Two-field records (name + ID, name + code) — moderate complexity.
Hard: Three/four-field records with mixed data types — full complexity at speed.

All questions are timed-drill style: compare source vs. transcribed, determine if identical.
"""
import json
import random
import string

random.seed(99)

# ---------------------------------------------------------------------------
# Data pools
# ---------------------------------------------------------------------------
SURNAMES = [
    "SANTOS", "REYES", "CRUZ", "GARCIA", "MENDOZA", "TORRES", "FLORES",
    "BAUTISTA", "VILLANUEVA", "HERNANDEZ", "GONZALES", "RODRIGUEZ",
    "AQUINO", "TOLENTINO", "PANGILINAN", "MANALO", "GUERRERO", "ESPINOSA",
    "FERNANDEZ", "MARTINEZ", "CONSTANTINO", "DIMACULANGAN", "EVANGELISTA",
    "BUENAVENTURA", "ENRIQUEZ", "DELA CRUZ", "DELOS REYES", "DEL ROSARIO",
    "SAN JUAN", "DELA ROSA", "MAGBANUA", "RAMOS", "NAVARRO", "SORIANO",
    "CASTILLO", "MORALES", "SANTIAGO", "AGUILAR", "DIAZ", "LOZANO",
    "PASCUAL", "SALAZAR", "MIRANDA", "VELASCO", "OCAMPO", "PEREZ",
    "DOMINGUEZ", "CABRERA", "FUENTES", "MEDINA",
]

FIRST_NAMES = [
    "JUAN PEDRO", "MARIA TERESA", "JOSE ANTONIO", "ANNA MARIE", "ROBERTO",
    "ELENA", "CARLOS", "SOFIA", "RAFAEL", "GRACE ANNE", "MICHAEL ANGELO",
    "PATRICIA", "ALEJANDRO", "VICTORIA", "CHRISTOPHER", "LOURDES",
    "BENIGNO", "CORAZON", "FERDINAND", "IMELDA", "RODRIGO", "SARA",
    "MARK", "ALAN PETER", "LEILA", "PANFILO", "MIRIAM", "ANTONIO",
    "FRANCISCO", "ROSARIO", "GABRIEL", "ANGELICA", "RAMON", "CECILIA",
]

MIDDLES = ["R.", "C.", "A.", "M.", "P.", "S.", "V.", "T.", "B.", "J.", "L.", "N."]

AGENCIES = ["CSC", "COA", "DILG", "DBM", "DOH", "DOLE", "DPWH", "BIR",
            "NBI", "PNP", "DSWD", "DENR", "DOJ", "DOT", "TESDA", "CHED"]

REGIONS = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
           "R10", "R11", "R12", "R13", "NCR", "CAR", "BARMM"]

BUDGET_PREFIXES = ["PS", "MOOE", "CO", "OR", "DV", "PR"]
BUDGET_CODES = ["101", "102", "201", "202", "205", "301", "302"]

YEARS = ["2022", "2023", "2024", "2025"]
MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
DAYS = ["01", "05", "10", "15", "20", "25", "28", "30"]

SG_GRADES = [str(i) for i in range(1, 34)]
SG_STEPS = [str(i) for i in range(1, 9)]

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def rand_seq_padded(n, digits=5):
    return str(n).zfill(digits)


def rand_amount():
    pesos = random.randint(5000, 999999)
    centavos = random.randint(0, 99)
    return f"\u20b1{pesos:,}.{centavos:02d}"


def rand_name():
    s = random.choice(SURNAMES)
    f = random.choice(FIRST_NAMES)
    m = random.choice(MIDDLES)
    return f"{s}, {f} {m}"


def rand_surname_only():
    return random.choice(SURNAMES)


def rand_full_name_no_mi():
    s = random.choice(SURNAMES)
    f = random.choice(FIRST_NAMES)
    return f"{s}, {f}"


def rand_emp_id():
    yr = random.choice(YEARS)
    seq = rand_seq_padded(random.randint(1, 99999), 5)
    return f"EMP-{yr}-{seq}"


def rand_doc_code():
    ag = random.choice(AGENCIES)
    rg = random.choice(REGIONS)
    seq = rand_seq_padded(random.randint(1, 999), 3)
    return f"{ag}-{rg}-{seq}"


def rand_full_code():
    pfx = random.choice(BUDGET_PREFIXES)
    bc = random.choice(BUDGET_CODES)
    yr = random.choice(YEARS)
    mo = random.choice(MONTHS)
    seq = rand_seq_padded(random.randint(1, 9999), 4)
    return f"{pfx}-{bc}-{yr}-{mo}-{seq}"


def rand_sg():
    g = random.choice(SG_GRADES)
    s = random.choice(SG_STEPS)
    return f"SG-{g}-{s}"


def rand_date():
    mo = random.choice(MONTHS)
    dy = random.choice(DAYS)
    yr = random.choice(YEARS)
    return f"{mo}/{dy}/{yr}"


def rand_sss():
    a = str(random.randint(10, 99))
    b = str(random.randint(1000000, 9999999))
    c = str(random.randint(0, 9))
    return f"{a}-{b}-{c}"


def rand_phone():
    prefix = "09"
    digits = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return prefix + digits


def rand_number_seq(length=None):
    if length is None:
        length = random.randint(6, 12)
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


# ---------------------------------------------------------------------------
# Error injection
# ---------------------------------------------------------------------------

def inject_substitution(s):
    chars = list(s)
    candidates = [i for i, c in enumerate(chars) if c.isalnum()]
    if not candidates:
        return s, None
    pos = random.choice(candidates)
    c = chars[pos]
    if c.isdigit():
        replacement = str((int(c) + random.randint(1, 8)) % 10)
    else:
        pool = [ch for ch in "ABCDEFGHJKLMNPQRSTUVWXYZ" if ch != c]
        replacement = random.choice(pool)
    chars[pos] = replacement
    result = "".join(chars)
    if result == s:
        return s, None
    return result, "substitution"


def inject_transposition(s):
    chars = list(s)
    candidates = [
        i for i in range(len(chars) - 1)
        if chars[i].isalnum() and chars[i+1].isalnum() and chars[i] != chars[i+1]
    ]
    if not candidates:
        return s, None
    pos = random.choice(candidates)
    chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
    result = "".join(chars)
    if result == s:
        return s, None
    return result, "transposition"


def inject_omission(s):
    chars = list(s)
    candidates = [i for i, c in enumerate(chars) if c.isalnum()]
    if not candidates:
        return s, None
    pos = random.choice(candidates)
    chars.pop(pos)
    result = "".join(chars)
    if result == s:
        return s, None
    return result, "omission"


def inject_addition(s):
    chars = list(s)
    candidates = [i for i, c in enumerate(chars) if c.isalnum()]
    if not candidates:
        return s, None
    pos = random.choice(candidates)
    c = chars[pos]
    if c.isdigit():
        extra = str(random.randint(0, 9))
    else:
        extra = random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ")
    chars.insert(pos, extra)
    result = "".join(chars)
    if result == s:
        return s, None
    return result, "addition"


_INJECTORS = {
    "substitution": inject_substitution,
    "transposition": inject_transposition,
    "omission": inject_omission,
    "addition": inject_addition,
}
_FALLBACK_ORDER = ["substitution", "transposition", "omission", "addition"]

# Cycling error type selector for even distribution
_error_type_cycle = ["substitution", "transposition", "omission", "addition"] * 200
_error_type_idx = 0


def next_error_type():
    """Return error types in a round-robin cycle for even distribution."""
    global _error_type_idx
    t = _error_type_cycle[_error_type_idx % len(_error_type_cycle)]
    _error_type_idx += 1
    return t


def apply_error(field_value, requested_type):
    result, actual = _INJECTORS[requested_type](field_value)
    if actual is not None:
        return result, actual
    for t in _FALLBACK_ORDER:
        if t == requested_type:
            continue
        result, actual = _INJECTORS[t](field_value)
        if actual is not None:
            return result, actual
    raise ValueError(f"Could not inject any error into: {field_value!r}")

# ---------------------------------------------------------------------------
# Question stems (varied to prevent duplicates)
# ---------------------------------------------------------------------------

_SPEED_DRILL_STEMS = [
    "Speed drill: Compare the following. Are they EXACTLY identical?",
    "Timed comparison: Do these two entries match character for character?",
    "Quick check: Is the transcribed version identical to the source?",
    "Rapid verification: Are both versions exactly the same?",
    "Speed test: Does the transcribed entry match the source perfectly?",
    "Accuracy check: Compare source and transcribed. Any difference?",
    "Drill item: Are these two records character-for-character identical?",
    "Timed drill: Is there any discrepancy between source and transcribed?",
    "Quick compare: Do both versions match in every character?",
    "Speed check: Is the transcription error-free?",
]

_FIND_IDENTICAL_STEMS = [
    "Speed drill: Which pair below is EXACTLY identical? (Set {n})",
    "Timed comparison: Which of the following pairs matches perfectly? (Set {n})",
    "Quick check: Select the pair with NO discrepancy. (Set {n})",
    "Rapid drill: Which pair has zero errors? (Set {n})",
    "Accuracy test: Identify the identical pair. (Set {n})",
]

_IDENTIFY_TYPE_STEMS = [
    "Speed drill: The transcribed version has ONE error. What type?",
    "Timed check: Classify the error in the transcribed version.",
    "Quick identification: What kind of error was made?",
    "Rapid drill: Name the error type in the transcription.",
]

_COUNT_ERRORS_STEMS = [
    "Speed drill: How many errors does the transcribed record contain?",
    "Timed check: Count the discrepancies between source and transcribed.",
    "Rapid verification: How many fields contain an error?",
    "Accuracy drill: How many transcription errors are present?",
]

# ---------------------------------------------------------------------------
# EASY question builders (IDs 1-200): Single-field comparisons
# ---------------------------------------------------------------------------

def build_easy_name_identical(qid):
    name = rand_name()
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {name}\nTranscribed: {name}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both versions match exactly in every character, space, and punctuation mark.",
        "tags": ["identical", "single-field", "name", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_name_error(qid):
    name = rand_name()
    req = next_error_type()
    bad_name, etype = apply_error(name, req)
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {name}\nTranscribed: {bad_name}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Not identical — contains an error",
        "explanation": f"The transcribed version contains a {etype} error: '{name}' was transcribed as '{bad_name}'.",
        "tags": ["different", "single-field", "name", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_number_identical(qid):
    num = rand_number_seq()
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {num}\nTranscribed: {num}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both number sequences are exactly the same digit for digit.",
        "tags": ["identical", "single-field", "number", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_number_error(qid):
    num = rand_number_seq()
    req = random.choice(["substitution", "transposition"])
    bad_num, etype = apply_error(num, req)
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {num}\nTranscribed: {bad_num}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Not identical — contains an error",
        "explanation": f"The transcribed version contains a {etype} error: '{num}' was transcribed as '{bad_num}'.",
        "tags": ["different", "single-field", "number", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_code_identical(qid):
    code = rand_doc_code()
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {code}\nTranscribed: {code}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both codes match exactly in every character and separator.",
        "tags": ["identical", "single-field", "code", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_code_error(qid):
    code = rand_doc_code()
    req = next_error_type()
    bad_code, etype = apply_error(code, req)
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {code}\nTranscribed: {bad_code}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Not identical — contains an error",
        "explanation": f"The transcribed version contains a {etype} error: '{code}' was transcribed as '{bad_code}'.",
        "tags": ["different", "single-field", "code", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_emp_id_identical(qid):
    emp = rand_emp_id()
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {emp}\nTranscribed: {emp}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both employee IDs match exactly.",
        "tags": ["identical", "single-field", "employee-id", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_emp_id_error(qid):
    emp = rand_emp_id()
    req = next_error_type()
    bad_emp, etype = apply_error(emp, req)
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {emp}\nTranscribed: {bad_emp}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — contains an error"
        ],
        "answer": "Not identical — contains an error",
        "explanation": f"The transcribed version contains a {etype} error: '{emp}' was transcribed as '{bad_emp}'.",
        "tags": ["different", "single-field", "employee-id", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_find_identical(qid):
    """Four pairs, one identical, three with errors."""
    correct = rand_name()
    options = [(correct, correct, True)]
    for _ in range(3):
        n = rand_name()
        req = next_error_type()
        bad, _ = apply_error(n, req)
        options.append((n, bad, False))
    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    choices = [
        f"{labels[i]}. Source: {opt[0]}  /  Transcribed: {opt[1]}"
        for i, opt in enumerate(options)
    ]
    answer_idx = next(i for i, opt in enumerate(options) if opt[2])
    answer = choices[answer_idx]
    stem = random.choice(_FIND_IDENTICAL_STEMS).format(n=qid)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Easy",
        "question": stem,
        "choices": choices,
        "answer": answer,
        "explanation": f"Option {labels[answer_idx]} is the only pair where both versions match exactly.",
        "tags": ["find-identical", "single-field", "name", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# MEDIUM question builders (IDs 201-400): Two-field records
# ---------------------------------------------------------------------------

def build_medium_two_field_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    source = f"{name}    {emp}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {source}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both fields match exactly — name and employee ID are identical in both records.",
        "tags": ["identical", "two-field", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_name_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    req = next_error_type()
    bad_name, etype = apply_error(name, req)
    source = f"{name}    {emp}"
    transcribed = f"{bad_name}    {emp}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Not identical — error in the name field",
        "explanation": f"The name field contains a {etype} error: '{name}' was transcribed as '{bad_name}'.",
        "tags": ["different", "two-field", "name-field", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_id_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    req = next_error_type()
    bad_emp, etype = apply_error(emp, req)
    source = f"{name}    {emp}"
    transcribed = f"{name}    {bad_emp}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Not identical — error in the ID/code field",
        "explanation": f"The ID field contains a {etype} error: '{emp}' was transcribed as '{bad_emp}'.",
        "tags": ["different", "two-field", "id-field", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_code_record_identical(qid):
    name = rand_name()
    code = rand_doc_code()
    source = f"{name}    {code}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {source}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Identical — no differences",
        "explanation": "Both fields match exactly — name and document code are identical.",
        "tags": ["identical", "two-field", "document-code", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_code_error(qid):
    name = rand_name()
    code = rand_doc_code()
    req = next_error_type()
    bad_code, etype = apply_error(code, req)
    source = f"{name}    {code}"
    transcribed = f"{name}    {bad_code}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Not identical — error in the ID/code field",
        "explanation": f"The document code contains a {etype} error: '{code}' was transcribed as '{bad_code}'.",
        "tags": ["different", "two-field", "document-code", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_both_errors(qid):
    name = rand_name()
    emp = rand_emp_id()
    req1 = next_error_type()
    req2 = next_error_type()
    bad_name, etype1 = apply_error(name, req1)
    bad_emp, etype2 = apply_error(emp, req2)
    source = f"{name}    {emp}"
    transcribed = f"{bad_name}    {bad_emp}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Identical — no differences",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — errors in both fields"
        ],
        "answer": "Not identical — errors in both fields",
        "explanation": f"Both fields contain errors. Name: {etype1} ('{name}' → '{bad_name}'). ID: {etype2} ('{emp}' → '{bad_emp}').",
        "tags": ["different", "two-field", "both-fields", "speed-drill", etype1, etype2],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_identify_type(qid):
    name = rand_name()
    emp = rand_emp_id()
    field_choice = random.choice(["name", "id"])
    req = next_error_type()
    if field_choice == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}"
        transcribed = f"{bad}    {emp}"
        orig = name
    else:
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}"
        transcribed = f"{name}    {bad}"
        orig = emp

    choices = [
        "Substitution — one character replaced by another",
        "Transposition — two adjacent characters swapped",
        "Omission — one character is missing",
        "Addition — one extra character inserted",
    ]
    answer_map = {
        "substitution": choices[0],
        "transposition": choices[1],
        "omission": choices[2],
        "addition": choices[3],
    }
    stem = random.choice(_IDENTIFY_TYPE_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": q,
        "choices": choices,
        "answer": answer_map[etype],
        "explanation": f"The error is a {etype}: '{orig}' was transcribed as '{bad}'.",
        "tags": ["error-type", "two-field", "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_find_identical(qid):
    correct_name = rand_name()
    correct_emp = rand_emp_id()
    correct_src = f"{correct_name}    {correct_emp}"
    options = [(correct_src, correct_src, True)]
    for _ in range(3):
        n = rand_name()
        e = rand_emp_id()
        src = f"{n}    {e}"
        field = random.choice(["name", "id"])
        req = next_error_type()
        if field == "name":
            bad, _ = apply_error(n, req)
            trn = f"{bad}    {e}"
        else:
            bad, _ = apply_error(e, req)
            trn = f"{n}    {bad}"
        options.append((src, trn, False))
    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    choices = [
        f"{labels[i]}. Source: {opt[0]}  /  Transcribed: {opt[1]}"
        for i, opt in enumerate(options)
    ]
    answer_idx = next(i for i, opt in enumerate(options) if opt[2])
    answer = choices[answer_idx]
    stem = random.choice(_FIND_IDENTICAL_STEMS).format(n=qid)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Medium",
        "question": stem,
        "choices": choices,
        "answer": answer,
        "explanation": f"Option {labels[answer_idx]} is the only pair where both fields match exactly.",
        "tags": ["find-identical", "two-field", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# HARD question builders (IDs 401-600): Three/four-field records
# ---------------------------------------------------------------------------

def build_hard_three_field_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    source = f"{name}    {emp}    {sg}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {source}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": q,
        "choices": [
            "Identical — no differences in any field",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — error in the salary grade/date field"
        ],
        "answer": "Identical — no differences in any field",
        "explanation": "All three fields match exactly between source and transcribed records.",
        "tags": ["identical", "three-field", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_three_field_error(qid, target_field):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    req = next_error_type()

    if target_field == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{bad}    {emp}    {sg}"
        answer = "Not identical — error in the name field"
        expl = f"The name field contains a {etype} error: '{name}' → '{bad}'."
    elif target_field == "id":
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {bad}    {sg}"
        answer = "Not identical — error in the ID/code field"
        expl = f"The ID field contains a {etype} error: '{emp}' → '{bad}'."
    else:
        bad, etype = apply_error(sg, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {emp}    {bad}"
        answer = "Not identical — error in the salary grade/date field"
        expl = f"The salary grade contains a {etype} error: '{sg}' → '{bad}'."

    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": q,
        "choices": [
            "Identical — no differences in any field",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — error in the salary grade/date field"
        ],
        "answer": answer,
        "explanation": expl,
        "tags": ["different", "three-field", target_field, "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_four_field_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    source = f"{name}    {emp}    {sg}    {date}"
    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {source}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": q,
        "choices": [
            "Identical — no differences in any field",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — error in the salary grade or date field"
        ],
        "answer": "Identical — no differences in any field",
        "explanation": "All four fields match exactly between source and transcribed records.",
        "tags": ["identical", "four-field", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_four_field_error(qid, target_field):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    req = next_error_type()

    if target_field == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{bad}    {emp}    {sg}    {date}"
        answer = "Not identical — error in the name field"
        expl = f"The name field contains a {etype} error: '{name}' → '{bad}'."
    elif target_field == "id":
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {bad}    {sg}    {date}"
        answer = "Not identical — error in the ID/code field"
        expl = f"The ID field contains a {etype} error: '{emp}' → '{bad}'."
    elif target_field == "sg":
        bad, etype = apply_error(sg, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {emp}    {bad}    {date}"
        answer = "Not identical — error in the salary grade or date field"
        expl = f"The salary grade contains a {etype} error: '{sg}' → '{bad}'."
    else:  # date
        bad, etype = apply_error(date, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {emp}    {sg}    {bad}"
        answer = "Not identical — error in the salary grade or date field"
        expl = f"The date field contains a {etype} error: '{date}' → '{bad}'."

    stem = random.choice(_SPEED_DRILL_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": q,
        "choices": [
            "Identical — no differences in any field",
            "Not identical — error in the name field",
            "Not identical — error in the ID/code field",
            "Not identical — error in the salary grade or date field"
        ],
        "answer": answer,
        "explanation": expl,
        "tags": ["different", "four-field", target_field, "speed-drill", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_count_errors(qid):
    """Three-field record with 0, 1, or 2 errors — examinee counts them."""
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    error_count = random.choice([0, 1, 1, 2])  # weighted toward 1

    bad_name, bad_emp, bad_sg = name, emp, sg
    errors_made = []

    if error_count >= 1:
        field = random.choice(["name", "id", "sg"])
        req = next_error_type()
        if field == "name":
            bad_name, etype = apply_error(name, req)
            errors_made.append(f"name ({etype})")
        elif field == "id":
            bad_emp, etype = apply_error(emp, req)
            errors_made.append(f"ID ({etype})")
        else:
            bad_sg, etype = apply_error(sg, req)
            errors_made.append(f"salary grade ({etype})")

    if error_count >= 2:
        remaining = [f for f in ["name", "id", "sg"]
                     if f not in [e.split(" ")[0] for e in errors_made]]
        if remaining:
            field = random.choice(remaining)
            req = next_error_type()
            if field == "name":
                bad_name, etype = apply_error(name, req)
                errors_made.append(f"name ({etype})")
            elif field == "id":
                bad_emp, etype = apply_error(emp, req)
                errors_made.append(f"ID ({etype})")
            else:
                bad_sg, etype = apply_error(sg, req)
                errors_made.append(f"salary grade ({etype})")

    source = f"{name}    {emp}    {sg}"
    transcribed = f"{bad_name}    {bad_emp}    {bad_sg}"

    # Re-derive actual error count by comparing fields directly (handles edge cases)
    import re
    src_fields = re.split(r'\s{4,}', source)
    trn_fields = re.split(r'\s{4,}', transcribed)
    actual_count = sum(1 for s, t in zip(src_fields, trn_fields) if s != t)
    # Update errors_made to match actual count
    errors_made = errors_made[:actual_count]

    stem = random.choice(_COUNT_ERRORS_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"

    choices = ["0 errors", "1 error", "2 errors", "3 errors"]
    answer = choices[actual_count]

    if actual_count == 0:
        expl = "The records are identical — no errors in any field."
    else:
        expl = f"There {'is' if actual_count == 1 else 'are'} {actual_count} error(s): {', '.join(errors_made)}."

    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": q,
        "choices": choices,
        "answer": answer,
        "explanation": expl,
        "tags": ["count-errors", "three-field", "speed-drill", f"{actual_count}-errors"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_find_identical(qid):
    """Four-field record: find the identical pair among four options."""
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    correct_src = f"{name}    {emp}    {sg}    {date}"

    options = [(correct_src, correct_src, True)]
    for _ in range(3):
        n = rand_name()
        e = rand_emp_id()
        s = rand_sg()
        d = rand_date()
        src = f"{n}    {e}    {s}    {d}"
        field = random.choice(["name", "id", "sg", "date"])
        req = next_error_type()
        if field == "name":
            bad, _ = apply_error(n, req)
            trn = f"{bad}    {e}    {s}    {d}"
        elif field == "id":
            bad, _ = apply_error(e, req)
            trn = f"{n}    {bad}    {s}    {d}"
        elif field == "sg":
            bad, _ = apply_error(s, req)
            trn = f"{n}    {e}    {bad}    {d}"
        else:
            bad, _ = apply_error(d, req)
            trn = f"{n}    {e}    {s}    {bad}"
        options.append((src, trn, False))

    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    choices = [
        f"{labels[i]}. Source: {opt[0]}  /  Transcribed: {opt[1]}"
        for i, opt in enumerate(options)
    ]
    answer_idx = next(i for i, opt in enumerate(options) if opt[2])
    answer = choices[answer_idx]
    stem = random.choice(_FIND_IDENTICAL_STEMS).format(n=qid)
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Speed and Accuracy Drills",
        "difficulty": "Hard",
        "question": stem,
        "choices": choices,
        "answer": answer,
        "explanation": f"Option {labels[answer_idx]} is the only pair where all fields match exactly.",
        "tags": ["find-identical", "four-field", "speed-drill"],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def generate_easy(start_id=1, count=200):
    """Generate 200 easy questions: single-field comparisons.
    
    Rebalanced for diversity:
    - ~40% identical, ~45% different, ~15% find-identical (format variety)
    - Data types: names 30%, numbers 25%, codes 25%, emp IDs 20%
    """
    questions = []
    builders = [
        # Identical: 80 total (40%) — spread across data types
        (build_easy_name_identical, 22),
        (build_easy_number_identical, 22),
        (build_easy_code_identical, 18),
        (build_easy_emp_id_identical, 18),
        # Different: 90 total (45%) — spread across data types
        (build_easy_name_error, 24),
        (build_easy_number_error, 24),
        (build_easy_code_error, 22),
        (build_easy_emp_id_error, 20),
        # Find-identical: 30 total (15%) — format variety
        (build_easy_find_identical, 30),
    ]
    pool = []
    for builder, n in builders:
        pool.extend([builder] * n)
    random.shuffle(pool)

    for i, builder in enumerate(pool[:count]):
        qid = start_id + i
        questions.append(builder(qid))
    return questions


def generate_medium(start_id=201, count=200):
    """Generate 200 medium questions: two-field records.
    
    Rebalanced for diversity:
    - ~35% identical, ~35% single-field error, ~10% both-field errors
    - ~10% error-type identification, ~10% find-identical
    """
    questions = []
    builders = [
        # Identical: 70 total (35%)
        (build_medium_two_field_identical, 40),
        (build_medium_code_record_identical, 30),
        # Single-field errors: 70 total (35%)
        (build_medium_name_error, 25),
        (build_medium_id_error, 25),
        (build_medium_code_error, 20),
        # Both-field errors: 20 total (10%)
        (build_medium_both_errors, 20),
        # Error-type identification: 20 total (10%) — format variety
        (build_medium_identify_type, 20),
        # Find-identical: 20 total (10%) — format variety
        (build_medium_find_identical, 20),
    ]
    pool = []
    for builder, n in builders:
        pool.extend([builder] * n)
    random.shuffle(pool)

    for i, builder in enumerate(pool[:count]):
        qid = start_id + i
        questions.append(builder(qid))
    return questions


def generate_hard(start_id=401, count=200):
    """Generate 200 hard questions: three/four-field records.
    
    Rebalanced for diversity:
    - ~25% identical, ~40% single-field error, ~20% count-errors, ~15% find-identical
    - Errors spread evenly across all field positions
    """
    questions = []

    def _three_identical(qid):
        return build_hard_three_field_identical(qid)

    def _three_name(qid):
        return build_hard_three_field_error(qid, "name")

    def _three_id(qid):
        return build_hard_three_field_error(qid, "id")

    def _three_sg(qid):
        return build_hard_three_field_error(qid, "sg")

    def _four_identical(qid):
        return build_hard_four_field_identical(qid)

    def _four_name(qid):
        return build_hard_four_field_error(qid, "name")

    def _four_id(qid):
        return build_hard_four_field_error(qid, "id")

    def _four_sg(qid):
        return build_hard_four_field_error(qid, "sg")

    def _four_date(qid):
        return build_hard_four_field_error(qid, "date")

    def _count(qid):
        return build_hard_count_errors(qid)

    def _find(qid):
        return build_hard_find_identical(qid)

    pool = (
        # Identical: 50 total (25%)
        [_three_identical] * 25
        + [_four_identical] * 25
        # Single-field errors: 80 total (40%) — evenly across positions
        + [_three_name] * 12
        + [_three_id] * 12
        + [_three_sg] * 12
        + [_four_name] * 11
        + [_four_id] * 11
        + [_four_sg] * 11
        + [_four_date] * 11
        # Count-errors: 40 total (20%) — format variety
        + [_count] * 40
        # Find-identical: 30 total (15%) — format variety
        + [_find] * 30
    )
    random.shuffle(pool)

    for i, builder_fn in enumerate(pool[:count]):
        qid = start_id + i
        questions.append(builder_fn(qid))
    return questions


def main():
    easy = generate_easy(1, 200)
    medium = generate_medium(201, 200)
    hard = generate_hard(401, 200)

    all_questions = easy + medium + hard
    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"

    output_path = (
        "data/seed/questions/clerical-ability/"
        "name-and-number-comparison/speed-and-accuracy-drills/questions.json"
    )
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_questions)} questions → {output_path}")
    print(f"  Easy:   {len(easy)} (IDs 1-200)")
    print(f"  Medium: {len(medium)} (IDs 201-400)")
    print(f"  Hard:   {len(hard)} (IDs 401-600)")


if __name__ == "__main__":
    main()
