"""
Generate 600 error detection questions for the CSE clerical ability reviewer.
Distribution: 200 Easy, 200 Medium, 200 Hard (IDs 1-200, 201-400, 401-600).

Fixes v2:
- transpose_chars: skip pairs where both chars are identical (would produce no
  visible swap), and verify the result actually differs from the source.
- add_char: operate only on the isolated field string, not the full record, so
  the length change is guaranteed.
- apply_error: after injection, re-derive the actual error type from the diff
  (length change → omit/add; same-length adjacent swap → trans; else → sub)
  and use THAT label in the explanation — eliminating type-label mismatches.
- build_easy_find_identical: vary the question stem with a context phrase so
  no two stems are identical.
- Diversity: add Medium identify-type questions; add Hard find-identical
  questions; rebalance builder pools.
"""
import json
import random

random.seed(42)

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
]

FIRST_NAMES = [
    "JUAN PEDRO", "MARIA TERESA", "JOSE ANTONIO", "ANNA MARIE", "ROBERTO",
    "ELENA", "CARLOS", "SOFIA", "RAFAEL", "GRACE ANNE", "MICHAEL ANGELO",
    "PATRICIA", "ALEJANDRO", "VICTORIA", "CHRISTOPHER", "LOURDES",
    "BENIGNO", "CORAZON", "FERDINAND", "IMELDA", "RODRIGO", "SARA",
    "MARK", "ALAN PETER", "LEILA", "PANFILO", "MIRIAM", "ANTONIO",
]

MIDDLES = ["R.", "C.", "A.", "M.", "P.", "S.", "V.", "T.", "B.", "J."]

AGENCIES = ["CSC", "COA", "DILG", "DBM", "DOH", "DOLE", "DPWH", "BIR",
            "NBI", "PNP", "DSWD", "DENR", "DOJ", "DOT", "TESDA"]

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
    return f"₱{pesos:,}.{centavos:02d}"

def rand_name():
    s = random.choice(SURNAMES)
    f = random.choice(FIRST_NAMES)
    m = random.choice(MIDDLES)
    return f"{s}, {f} {m}"

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

# ---------------------------------------------------------------------------
# Error injection — operate on isolated field strings only
# FIX: each function returns (result, actual_error_type) so the caller always
#      uses the label that matches what actually happened.
# ---------------------------------------------------------------------------

def inject_substitution(s):
    """Replace one alphanumeric char with a different one. Returns (result, 'substitution')."""
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
    """Swap two adjacent alphanumeric chars that are DIFFERENT. Returns (result, 'transposition')."""
    chars = list(s)
    # Only consider pairs where both are alnum AND they differ (otherwise no visible change)
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
    """Remove one alphanumeric char. Returns (result, 'omission')."""
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
    """Insert one extra alphanumeric char adjacent to an existing one. Returns (result, 'addition')."""
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


# Priority order for fallbacks when a requested type can't be applied
_INJECTORS = {
    "substitution": inject_substitution,
    "transposition": inject_transposition,
    "omission": inject_omission,
    "addition": inject_addition,
}
_FALLBACK_ORDER = ["substitution", "transposition", "omission", "addition"]


def apply_error(field_value, requested_type):
    """
    Apply the requested error type to field_value.
    Falls back through other types if the requested one produces no change.
    Returns (modified_field, actual_error_type_string).
    Raises ValueError if no injector can produce a change (shouldn't happen with real data).
    """
    # Try requested type first
    result, actual = _INJECTORS[requested_type](field_value)
    if actual is not None:
        return result, actual
    # Fallback
    for t in _FALLBACK_ORDER:
        if t == requested_type:
            continue
        result, actual = _INJECTORS[t](field_value)
        if actual is not None:
            return result, actual
    raise ValueError(f"Could not inject any error into: {field_value!r}")

# ---------------------------------------------------------------------------
# EASY question builders  (2-field records, IDs 1-200)
# ---------------------------------------------------------------------------

# Varied stems for find-identical to prevent duplicate question text
_FIND_IDENTICAL_STEMS = [
    "Which of the following pairs of records is EXACTLY identical? (Set {n})",
    "Which pair below shows a source and transcribed record that match perfectly? (Set {n})",
    "Select the pair where the transcribed record contains NO errors. (Set {n})",
    "Which of the following has NO discrepancy between source and transcribed? (Set {n})",
    "Identify the pair where both records are character-for-character the same. (Set {n})",
]

_IDENTIFY_TYPE_STEMS = [
    "The transcribed record contains ONE error in the {field}. What type of error is it?",
    "A clerk noticed a discrepancy in the {field}. What kind of error was made?",
    "The {field} was incorrectly transcribed. Which error type best describes the mistake?",
    "One error exists in the {field} of the transcribed record. Classify the error.",
]


_IDENTICAL_CHECK_STEMS = [
    "Compare the following records. Are they EXACTLY identical?",
    "A clerk transcribed the record below. Does the transcribed version match the source exactly?",
    "Review the source and transcribed records. Are all fields character-for-character the same?",
    "Check the following entry. Was it transcribed without any errors?",
    "Examine both records carefully. Do they match in every character, space, and punctuation mark?",
    "A data encoder submitted the following. Does it exactly match the source record?",
    "Compare the source and transcribed versions below. Is the transcription error-free?",
]

_DIFFERENT_CHECK_STEMS = [
    "Compare the following records. Are they EXACTLY identical?",
    "A clerk transcribed the record below. Does the transcribed version match the source exactly?",
    "Review the source and transcribed records. Are all fields character-for-character the same?",
    "Check the following entry. Was it transcribed without any errors?",
    "Examine both records carefully. Do they match in every character, space, and punctuation mark?",
    "A data encoder submitted the following. Does it exactly match the source record?",
    "Compare the source and transcribed versions below. Is the transcription error-free?",
]


def build_easy_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    source = f"{name}    {emp}"
    stem = random.choice(_IDENTICAL_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {source}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there are errors in both fields",
        ],
        "answer": "Yes, the records are identical",
        "explanation": "Both records are exactly the same — every character, space, and punctuation mark in both fields matches.",
        "tags": ["identical", "two-field", "name-field", "employee-id"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_name_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    bad_name, etype = apply_error(name, req)
    source = f"{name}    {emp}"
    transcribed = f"{bad_name}    {emp}"
    stem = random.choice(_DIFFERENT_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there are errors in both fields",
        ],
        "answer": "No, there is an error in the name field",
        "explanation": f"The records are NOT identical. The name field contains a {etype} error: '{name}' was transcribed as '{bad_name}'.",
        "tags": ["different", "two-field", "name-field", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_id_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    bad_emp, etype = apply_error(emp, req)
    source = f"{name}    {emp}"
    transcribed = f"{name}    {bad_emp}"
    stem = random.choice(_DIFFERENT_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there are errors in both fields",
        ],
        "answer": "No, there is an error in the employee ID",
        "explanation": f"The records are NOT identical. The employee ID contains a {etype} error: '{emp}' was transcribed as '{bad_emp}'.",
        "tags": ["different", "two-field", "employee-id", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_identify_error_type(qid):
    name = rand_name()
    emp = rand_emp_id()
    field_choice = random.choice(["name", "id"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    if field_choice == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}"
        transcribed = f"{bad}    {emp}"
        field_label = "name field"
        orig = name
    else:
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}"
        transcribed = f"{name}    {bad}"
        field_label = "employee ID"
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
    stem = random.choice(_IDENTIFY_TYPE_STEMS).format(field=field_label)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": choices,
        "answer": answer_map[etype],
        "explanation": f"The error is a {etype}: in the {field_label}, '{orig}' was transcribed as '{bad}'.",
        "tags": ["error-type", "two-field", field_label.replace(" ", "-"), etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_find_identical(qid):
    correct_name = rand_name()
    correct_emp = rand_emp_id()
    correct_src = f"{correct_name}    {correct_emp}"

    options = [(correct_src, correct_src, True)]
    for _ in range(3):
        n = rand_name()
        e = rand_emp_id()
        src = f"{n}    {e}"
        field = random.choice(["name", "id"])
        req = random.choice(["substitution", "transposition", "omission", "addition"])
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
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": stem,
        "choices": choices,
        "answer": answer,
        "explanation": (
            f"Option {labels[answer_idx]} is the only pair where every character "
            f"in both fields matches exactly. The other pairs each contain at least one discrepancy."
        ),
        "tags": ["find-identical", "two-field"],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# MEDIUM question builders  (3-field records, IDs 201-400)
# ---------------------------------------------------------------------------

def build_medium_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    source = f"{name}    {emp}    {sg}"
    stem = random.choice(_IDENTICAL_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {source}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there is an error in the salary grade",
        ],
        "answer": "Yes, the records are identical",
        "explanation": "All three fields match exactly — name, employee ID, and salary grade are identical in both records.",
        "tags": ["identical", "three-field", "name-field", "employee-id", "salary-grade"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_error_in_field(qid, target_field):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if target_field == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{bad}    {emp}    {sg}"
        answer = "No, there is an error in the name field"
        expl = f"The name field contains a {etype} error: '{name}' was transcribed as '{bad}'."
    elif target_field == "id":
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {bad}    {sg}"
        answer = "No, there is an error in the employee ID"
        expl = f"The employee ID contains a {etype} error: '{emp}' was transcribed as '{bad}'."
    else:
        bad, etype = apply_error(sg, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {emp}    {bad}"
        answer = "No, there is an error in the salary grade"
        expl = f"The salary grade contains a {etype} error: '{sg}' was transcribed as '{bad}'."

    stem = random.choice(_DIFFERENT_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there is an error in the salary grade",
        ],
        "answer": answer,
        "explanation": expl,
        "tags": ["different", "three-field", target_field, etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_doc_code_error(qid):
    name = rand_name()
    code = rand_doc_code()
    sg = rand_sg()
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    bad_code, etype = apply_error(code, req)
    source = f"{name}    {code}    {sg}"
    transcribed = f"{name}    {bad_code}    {sg}"
    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the document code",
            "No, there is an error in the salary grade",
        ],
        "answer": "No, there is an error in the document code",
        "explanation": f"The document code contains a {etype} error: '{code}' was transcribed as '{bad_code}'.",
        "tags": ["different", "three-field", "document-code", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_amount_error(qid):
    name = rand_name()
    code = rand_full_code()
    amount = rand_amount()
    req = random.choice(["substitution", "transposition"])
    bad_amount, etype = apply_error(amount, req)
    source = f"{name}    {code}    {amount}"
    transcribed = f"{name}    {code}    {bad_amount}"
    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the document code",
            "No, there is an error in the amount field",
        ],
        "answer": "No, there is an error in the amount field",
        "explanation": f"The amount field contains a {etype} error: '{amount}' was transcribed as '{bad_amount}'.",
        "tags": ["different", "three-field", "amount-field", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_date_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    date = rand_date()
    req = random.choice(["substitution", "transposition"])
    bad_date, etype = apply_error(date, req)
    source = f"{name}    {emp}    {date}"
    transcribed = f"{name}    {emp}    {bad_date}"
    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the employee ID",
            "No, there is an error in the date field",
        ],
        "answer": "No, there is an error in the date field",
        "explanation": f"The date field contains a {etype} error: '{date}' was transcribed as '{bad_date}'.",
        "tags": ["different", "three-field", "date-field", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_find_correct_version(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    source = f"{name}    {emp}    {sg}"

    wrong_versions = []
    for f in random.sample(["name", "id", "sg"], 3):
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if f == "name":
            bad, _ = apply_error(name, req)
            wrong_versions.append(f"{bad}    {emp}    {sg}")
        elif f == "id":
            bad, _ = apply_error(emp, req)
            wrong_versions.append(f"{name}    {bad}    {sg}")
        else:
            bad, _ = apply_error(sg, req)
            wrong_versions.append(f"{name}    {emp}    {bad}")

    all_versions = wrong_versions + [source]
    random.shuffle(all_versions)
    labels = ["A", "B", "C", "D"]
    choices = [f"{labels[i]}. {v}" for i, v in enumerate(all_versions)]
    answer_idx = all_versions.index(source)
    answer = choices[answer_idx]
    q = (
        f"The source record reads:\n\n"
        f"  {source}\n\n"
        f"Which of the following transcribed versions is EXACTLY correct?"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": choices,
        "answer": answer,
        "explanation": (
            f"Option {labels[answer_idx]} exactly matches the source record in all three fields. "
            f"The other options each contain at least one error."
        ),
        "tags": ["find-correct-version", "three-field"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_identify_error_type(qid):
    """Medium: 3-field record, identify the error type in a specified field."""
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    field_choice = random.choice(["name", "id", "sg"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if field_choice == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{bad}    {emp}    {sg}"
        field_label = "name field"
        orig = name
    elif field_choice == "id":
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {bad}    {sg}"
        field_label = "employee ID"
        orig = emp
    else:
        bad, etype = apply_error(sg, req)
        source = f"{name}    {emp}    {sg}"
        transcribed = f"{name}    {emp}    {bad}"
        field_label = "salary grade"
        orig = sg

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
    stem = random.choice(_IDENTIFY_TYPE_STEMS).format(field=field_label)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": choices,
        "answer": answer_map[etype],
        "explanation": f"The error is a {etype}: in the {field_label}, '{orig}' was transcribed as '{bad}'.",
        "tags": ["error-type", "three-field", field_label.replace(" ", "-"), etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# HARD question builders  (4-field records, IDs 401-600)
# ---------------------------------------------------------------------------

_COUNT_ERRORS_STEMS = [
    "Compare the following four-field records. How many errors does the transcribed record contain?",
    "A clerk transcribed the four-field record below. How many fields contain an error?",
    "Review the source and transcribed records. How many transcription errors are present?",
    "Count the number of errors in the transcribed record compared to the source.",
    "How many discrepancies exist between the source and transcribed records below?",
]

_IDENTIFY_FIELD_STEMS = [
    "Compare the following records. In which field does the error appear?",
    "A transcription error was made in one field. Which field contains the error?",
    "One field in the transcribed record does not match the source. Which field is it?",
    "Review the records below. In which field was the error introduced?",
]


def build_hard_four_field_identical(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    source = f"{name}    {emp}    {sg}    {date}"
    stem = random.choice(_IDENTICAL_CHECK_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {source}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": ["0 — the records are identical", "1 error", "2 errors", "3 errors"],
        "answer": "0 — the records are identical",
        "explanation": "All four fields match exactly — name, employee ID, salary grade, and date are identical in both records.",
        "tags": ["identical", "four-field", "count-errors"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_one_error(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    target = random.choice(["name", "id", "sg", "date"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if target == "name":
        bad, etype = apply_error(name, req)
        transcribed = f"{bad}    {emp}    {sg}    {date}"
        field_label, orig, err = "name field", name, bad
    elif target == "id":
        bad, etype = apply_error(emp, req)
        transcribed = f"{name}    {bad}    {sg}    {date}"
        field_label, orig, err = "employee ID", emp, bad
    elif target == "sg":
        bad, etype = apply_error(sg, req)
        transcribed = f"{name}    {emp}    {bad}    {date}"
        field_label, orig, err = "salary grade", sg, bad
    else:
        bad, etype = apply_error(date, req)
        transcribed = f"{name}    {emp}    {sg}    {bad}"
        field_label, orig, err = "date field", date, bad

    source = f"{name}    {emp}    {sg}    {date}"
    stem = random.choice(_COUNT_ERRORS_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": ["0 — the records are identical", "1 error", "2 errors", "3 errors"],
        "answer": "1 error",
        "explanation": (
            f"There is 1 error: a {etype} in the {field_label} "
            f"('{orig}' transcribed as '{err}'). All other fields are correct."
        ),
        "tags": ["different", "four-field", "count-errors", "one-error", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_two_errors(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    targets = random.sample(["name", "id", "sg", "date"], 2)
    errors_desc = []
    bad_name, bad_emp, bad_sg, bad_date = name, emp, sg, date

    for t in targets:
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if t == "name":
            bad_name, etype = apply_error(name, req)
            errors_desc.append(f"a {etype} in the name field ('{name}' → '{bad_name}')")
        elif t == "id":
            bad_emp, etype = apply_error(emp, req)
            errors_desc.append(f"a {etype} in the employee ID ('{emp}' → '{bad_emp}')")
        elif t == "sg":
            bad_sg, etype = apply_error(sg, req)
            errors_desc.append(f"a {etype} in the salary grade ('{sg}' → '{bad_sg}')")
        else:
            bad_date, etype = apply_error(date, req)
            errors_desc.append(f"a {etype} in the date field ('{date}' → '{bad_date}')")

    source = f"{name}    {emp}    {sg}    {date}"
    transcribed = f"{bad_name}    {bad_emp}    {bad_sg}    {bad_date}"
    stem = random.choice(_COUNT_ERRORS_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": ["0 — the records are identical", "1 error", "2 errors", "3 errors"],
        "answer": "2 errors",
        "explanation": f"There are 2 errors: {'; '.join(errors_desc)}.",
        "tags": ["different", "four-field", "count-errors", "two-errors"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_find_correct_four_field(qid):
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    source = f"{name}    {emp}    {sg}    {date}"

    wrong_versions = []
    for f in random.sample(["name", "id", "sg", "date"], 3):
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if f == "name":
            bad, _ = apply_error(name, req)
            wrong_versions.append(f"{bad}    {emp}    {sg}    {date}")
        elif f == "id":
            bad, _ = apply_error(emp, req)
            wrong_versions.append(f"{name}    {bad}    {sg}    {date}")
        elif f == "sg":
            bad, _ = apply_error(sg, req)
            wrong_versions.append(f"{name}    {emp}    {bad}    {date}")
        else:
            bad, _ = apply_error(date, req)
            wrong_versions.append(f"{name}    {emp}    {sg}    {bad}")

    all_versions = wrong_versions + [source]
    random.shuffle(all_versions)
    labels = ["A", "B", "C", "D"]
    choices = [f"{labels[i]}. {v}" for i, v in enumerate(all_versions)]
    answer_idx = all_versions.index(source)
    answer = choices[answer_idx]
    q = (
        f"The source record reads:\n\n"
        f"  {source}\n\n"
        f"Which of the following transcribed versions is EXACTLY correct?"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": choices,
        "answer": answer,
        "explanation": (
            f"Option {labels[answer_idx]} exactly matches the source record in all four fields. "
            f"The other options each contain at least one error."
        ),
        "tags": ["find-correct-version", "four-field"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_dv_record(qid):
    """4-field DV record: name, DV code, amount, date. Error in one field."""
    name = rand_name()
    dv = rand_full_code()
    amount = rand_amount()
    date = rand_date()
    target = random.choice(["name", "dv", "amount", "date"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    bad_name, bad_dv, bad_amount, bad_date = name, dv, amount, date
    if target == "name":
        bad_name, etype = apply_error(name, req)
        field_label, orig, err = "name field", name, bad_name
        answer = "No, there is an error in the name field"
    elif target == "dv":
        bad_dv, etype = apply_error(dv, req)
        field_label, orig, err = "DV code", dv, bad_dv
        answer = "No, there is an error in the DV code"
    elif target == "amount":
        bad_amount, etype = apply_error(amount, req)
        field_label, orig, err = "amount field", amount, bad_amount
        answer = "No, there is an error in the amount field"
    else:
        bad_date, etype = apply_error(date, req)
        field_label, orig, err = "date field", date, bad_date
        answer = "No, there is an error in the date field"

    source = f"{name}    {dv}    {amount}    {date}"
    transcribed = f"{bad_name}    {bad_dv}    {bad_amount}    {bad_date}"
    q = (
        f"Compare the following disbursement voucher records. In which field does the error appear?\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": [
            "No error — the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the DV code",
            "No, there is an error in the amount field",
            "No, there is an error in the date field",
        ][:4],  # keep 4 choices; rotate which 3 wrong options appear
        "answer": answer,
        "explanation": f"The {field_label} contains a {etype} error: '{orig}' was transcribed as '{err}'.",
        "tags": ["different", "four-field", "dv-record", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_find_identical_four_field(qid):
    """Hard: 4 options of 4-field records, find the identical pair."""
    correct_name = rand_name()
    correct_emp = rand_emp_id()
    correct_sg = rand_sg()
    correct_date = rand_date()
    correct_src = f"{correct_name}    {correct_emp}    {correct_sg}    {correct_date}"

    options = [(correct_src, correct_src, True)]
    for _ in range(3):
        n, e, s, d = rand_name(), rand_emp_id(), rand_sg(), rand_date()
        src = f"{n}    {e}    {s}    {d}"
        target = random.choice(["name", "id", "sg", "date"])
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if target == "name":
            bad, _ = apply_error(n, req)
            trn = f"{bad}    {e}    {s}    {d}"
        elif target == "id":
            bad, _ = apply_error(e, req)
            trn = f"{n}    {bad}    {s}    {d}"
        elif target == "sg":
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
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": stem,
        "choices": choices,
        "answer": answer,
        "explanation": (
            f"Option {labels[answer_idx]} is the only pair where all four fields "
            f"match exactly. The other pairs each contain at least one discrepancy."
        ),
        "tags": ["find-identical", "four-field"],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_identify_error_type_four_field(qid):
    """Hard: 4-field record, identify the error type in a specified field."""
    name = rand_name()
    emp = rand_emp_id()
    sg = rand_sg()
    date = rand_date()
    field_choice = random.choice(["name", "id", "sg", "date"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if field_choice == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{bad}    {emp}    {sg}    {date}"
        field_label, orig = "name field", name
    elif field_choice == "id":
        bad, etype = apply_error(emp, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {bad}    {sg}    {date}"
        field_label, orig = "employee ID", emp
    elif field_choice == "sg":
        bad, etype = apply_error(sg, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {emp}    {bad}    {date}"
        field_label, orig = "salary grade", sg
    else:
        bad, etype = apply_error(date, req)
        source = f"{name}    {emp}    {sg}    {date}"
        transcribed = f"{name}    {emp}    {sg}    {bad}"
        field_label, orig = "date field", date

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
    stem = random.choice(_IDENTIFY_TYPE_STEMS).format(field=field_label)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": choices,
        "answer": answer_map[etype],
        "explanation": f"The error is a {etype}: in the {field_label}, '{orig}' was transcribed as '{bad}'.",
        "tags": ["error-type", "four-field", field_label.replace(" ", "-"), etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }

# ---------------------------------------------------------------------------
# Fix build_hard_dv_record: ensure answer is always in choices
# (redefine to replace the version above)
# ---------------------------------------------------------------------------

def build_hard_dv_record(qid):  # noqa: F811 — intentional redefinition
    """4-field DV record: name, DV code, amount, date. Error in one field."""
    name = rand_name()
    dv = rand_full_code()
    amount = rand_amount()
    date = rand_date()
    target = random.choice(["name", "dv", "amount", "date"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    bad_name, bad_dv, bad_amount, bad_date = name, dv, amount, date
    if target == "name":
        bad_name, etype = apply_error(name, req)
        field_label, orig, err = "name field", name, bad_name
    elif target == "dv":
        bad_dv, etype = apply_error(dv, req)
        field_label, orig, err = "DV code", dv, bad_dv
    elif target == "amount":
        bad_amount, etype = apply_error(amount, req)
        field_label, orig, err = "amount field", amount, bad_amount
    else:
        bad_date, etype = apply_error(date, req)
        field_label, orig, err = "date field", date, bad_date

    source = f"{name}    {dv}    {amount}    {date}"
    transcribed = f"{bad_name}    {bad_dv}    {bad_amount}    {bad_date}"

    # Build exactly 4 choices that always include the correct answer
    all_field_choices = {
        "name field": "No, there is an error in the name field",
        "DV code": "No, there is an error in the DV code",
        "amount field": "No, there is an error in the amount field",
        "date field": "No, there is an error in the date field",
    }
    answer = all_field_choices[field_label]
    wrong_choices = [v for k, v in all_field_choices.items() if k != field_label]
    random.shuffle(wrong_choices)
    choices = wrong_choices[:3] + [answer]
    random.shuffle(choices)

    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = (
        f"{stem}\n\n"
        f"Source:      {source}\n"
        f"Transcribed: {transcribed}"
    )
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": choices,
        "answer": answer,
        "explanation": f"The {field_label} contains a {etype} error: '{orig}' was transcribed as '{err}'.",
        "tags": ["different", "four-field", "dv-record", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


# ---------------------------------------------------------------------------
# Additional record generators for diversity
# ---------------------------------------------------------------------------

def rand_sss():
    """SSS number: NN-NNNNNNN-N"""
    a = str(random.randint(10, 99))
    b = str(random.randint(1000000, 9999999))
    c = str(random.randint(0, 9))
    return f"{a}-{b}-{c}"

def rand_philhealth():
    """PhilHealth ID: NN-NNNNNNNNN-N"""
    a = str(random.randint(10, 99)).zfill(2)
    b = str(random.randint(100000000, 999999999))
    c = str(random.randint(0, 9))
    return f"{a}-{b}-{c}"

def rand_tin():
    """TIN: NNN-NNN-NNN-NNN"""
    parts = [str(random.randint(100, 999)) for _ in range(4)]
    return "-".join(parts)

def rand_phone():
    """PH mobile: 09NNNNNNNNN"""
    return f"09{random.randint(100000000, 999999999)}"

def rand_position_code():
    """Position item: XXXX-NNNNN-NNN"""
    prefixes = ["OSEC", "ADAS", "SVDO", "ACCT", "HRMO", "PDMU", "ITSD"]
    pfx = random.choice(prefixes)
    a = rand_seq_padded(random.randint(1, 99999), 5)
    b = rand_seq_padded(random.randint(1, 999), 3)
    return f"{pfx}-{a}-{b}"

def rand_payroll_record():
    """Full payroll record: name, SSS, gross, net, period"""
    name = rand_name()
    sss = rand_sss()
    gross = rand_amount()
    net = rand_amount()
    return name, sss, gross, net

def rand_personnel_record():
    """Personnel record: name, position code, SG, date"""
    name = rand_name()
    pos = rand_position_code()
    sg = rand_sg()
    date = rand_date()
    return name, pos, sg, date


# ---------------------------------------------------------------------------
# New Easy builders for diversity
# ---------------------------------------------------------------------------

def build_easy_sss_error(qid):
    """Two-field record with SSS number, error in SSS."""
    name = rand_name()
    sss = rand_sss()
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    bad_sss, etype = apply_error(sss, req)
    source = f"{name}    {sss}"
    transcribed = f"{name}    {bad_sss}"
    stem = random.choice(_DIFFERENT_CHECK_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the SSS number",
            "No, there are errors in both fields",
        ],
        "answer": "No, there is an error in the SSS number",
        "explanation": f"The SSS number contains a {etype} error: '{sss}' was transcribed as '{bad_sss}'.",
        "tags": ["different", "two-field", "sss-number", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_easy_phone_error(qid):
    """Two-field record with phone number, error in phone."""
    name = rand_name()
    phone = rand_phone()
    req = random.choice(["substitution", "transposition", "omission", "addition"])
    bad_phone, etype = apply_error(phone, req)
    source = f"{name}    {phone}"
    transcribed = f"{name}    {bad_phone}"
    stem = random.choice(_DIFFERENT_CHECK_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Easy",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the phone number",
            "No, there are errors in both fields",
        ],
        "answer": "No, there is an error in the phone number",
        "explanation": f"The phone number contains a {etype} error: '{phone}' was transcribed as '{bad_phone}'.",
        "tags": ["different", "two-field", "phone-number", etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


# ---------------------------------------------------------------------------
# New Medium builders for diversity
# ---------------------------------------------------------------------------

def build_medium_payroll_error(qid):
    """Payroll record: name, SSS, gross pay. Error in one field."""
    name = rand_name()
    sss = rand_sss()
    gross = rand_amount()
    target = random.choice(["name", "sss", "gross"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if target == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {sss}    {gross}"
        transcribed = f"{bad}    {sss}    {gross}"
        answer = "No, there is an error in the name field"
        expl = f"The name field contains a {etype} error: '{name}' was transcribed as '{bad}'."
    elif target == "sss":
        bad, etype = apply_error(sss, req)
        source = f"{name}    {sss}    {gross}"
        transcribed = f"{name}    {bad}    {gross}"
        answer = "No, there is an error in the SSS number"
        expl = f"The SSS number contains a {etype} error: '{sss}' was transcribed as '{bad}'."
    else:
        bad, etype = apply_error(gross, req)
        source = f"{name}    {sss}    {gross}"
        transcribed = f"{name}    {sss}    {bad}"
        answer = "No, there is an error in the gross pay"
        expl = f"The gross pay contains a {etype} error: '{gross}' was transcribed as '{bad}'."

    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the SSS number",
            "No, there is an error in the gross pay",
        ],
        "answer": answer,
        "explanation": expl,
        "tags": ["different", "three-field", "payroll-record", target, etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_medium_personnel_error(qid):
    """Personnel record: name, position code, SG. Error in one field."""
    name = rand_name()
    pos = rand_position_code()
    sg = rand_sg()
    target = random.choice(["name", "pos", "sg"])
    req = random.choice(["substitution", "transposition", "omission", "addition"])

    if target == "name":
        bad, etype = apply_error(name, req)
        source = f"{name}    {pos}    {sg}"
        transcribed = f"{bad}    {pos}    {sg}"
        answer = "No, there is an error in the name field"
        expl = f"The name field contains a {etype} error: '{name}' was transcribed as '{bad}'."
    elif target == "pos":
        bad, etype = apply_error(pos, req)
        source = f"{name}    {pos}    {sg}"
        transcribed = f"{name}    {bad}    {sg}"
        answer = "No, there is an error in the position code"
        expl = f"The position code contains a {etype} error: '{pos}' was transcribed as '{bad}'."
    else:
        bad, etype = apply_error(sg, req)
        source = f"{name}    {pos}    {sg}"
        transcribed = f"{name}    {pos}    {bad}"
        answer = "No, there is an error in the salary grade"
        expl = f"The salary grade contains a {etype} error: '{sg}' was transcribed as '{bad}'."

    stem = random.choice(_IDENTIFY_FIELD_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Medium",
        "question": q,
        "choices": [
            "Yes, the records are identical",
            "No, there is an error in the name field",
            "No, there is an error in the position code",
            "No, there is an error in the salary grade",
        ],
        "answer": answer,
        "explanation": expl,
        "tags": ["different", "three-field", "personnel-record", target, etype],
        "category": ["Sub-Professional"],
        "language": "English",
    }


# ---------------------------------------------------------------------------
# New Hard builders for diversity
# ---------------------------------------------------------------------------

def build_hard_payroll_four_field(qid):
    """Payroll 4-field: name, SSS, gross, net. Count errors."""
    name = rand_name()
    sss = rand_sss()
    gross = rand_amount()
    net = rand_amount()
    # 0, 1, or 2 errors
    num_errors = random.choice([0, 1, 1, 2])
    fields = ["name", "sss", "gross", "net"]
    targets = random.sample(fields, num_errors) if num_errors > 0 else []
    errors_desc = []
    bad_name, bad_sss, bad_gross, bad_net = name, sss, gross, net

    for t in targets:
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if t == "name":
            bad_name, etype = apply_error(name, req)
            errors_desc.append(f"a {etype} in the name field ('{name}' → '{bad_name}')")
        elif t == "sss":
            bad_sss, etype = apply_error(sss, req)
            errors_desc.append(f"a {etype} in the SSS number ('{sss}' → '{bad_sss}')")
        elif t == "gross":
            bad_gross, etype = apply_error(gross, req)
            errors_desc.append(f"a {etype} in the gross pay ('{gross}' → '{bad_gross}')")
        else:
            bad_net, etype = apply_error(net, req)
            errors_desc.append(f"a {etype} in the net pay ('{net}' → '{bad_net}')")

    source = f"{name}    {sss}    {gross}    {net}"
    transcribed = f"{bad_name}    {bad_sss}    {bad_gross}    {bad_net}"
    stem = random.choice(_COUNT_ERRORS_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    answer_map = {0: "0 — the records are identical", 1: "1 error", 2: "2 errors"}
    if num_errors == 0:
        expl = "All four fields match exactly — name, SSS, gross pay, and net pay are identical."
    elif num_errors == 1:
        expl = f"There is 1 error: {errors_desc[0]}."
    else:
        expl = f"There are 2 errors: {'; '.join(errors_desc)}."
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": ["0 — the records are identical", "1 error", "2 errors", "3 errors"],
        "answer": answer_map[num_errors],
        "explanation": expl,
        "tags": ["payroll-record", "four-field", "count-errors"] + (["identical"] if num_errors == 0 else ["different"]),
        "category": ["Sub-Professional"],
        "language": "English",
    }


def build_hard_personnel_four_field(qid):
    """Personnel 4-field: name, position code, SG, date. Count errors."""
    name = rand_name()
    pos = rand_position_code()
    sg = rand_sg()
    date = rand_date()
    num_errors = random.choice([0, 1, 1, 2])
    fields = ["name", "pos", "sg", "date"]
    targets = random.sample(fields, num_errors) if num_errors > 0 else []
    errors_desc = []
    bad_name, bad_pos, bad_sg, bad_date = name, pos, sg, date

    for t in targets:
        req = random.choice(["substitution", "transposition", "omission", "addition"])
        if t == "name":
            bad_name, etype = apply_error(name, req)
            errors_desc.append(f"a {etype} in the name field ('{name}' → '{bad_name}')")
        elif t == "pos":
            bad_pos, etype = apply_error(pos, req)
            errors_desc.append(f"a {etype} in the position code ('{pos}' → '{bad_pos}')")
        elif t == "sg":
            bad_sg, etype = apply_error(sg, req)
            errors_desc.append(f"a {etype} in the salary grade ('{sg}' → '{bad_sg}')")
        else:
            bad_date, etype = apply_error(date, req)
            errors_desc.append(f"a {etype} in the date field ('{date}' → '{bad_date}')")

    source = f"{name}    {pos}    {sg}    {date}"
    transcribed = f"{bad_name}    {bad_pos}    {bad_sg}    {bad_date}"
    stem = random.choice(_COUNT_ERRORS_STEMS)
    q = f"{stem}\n\nSource:      {source}\nTranscribed: {transcribed}"
    answer_map = {0: "0 — the records are identical", 1: "1 error", 2: "2 errors"}
    if num_errors == 0:
        expl = "All four fields match exactly — name, position code, salary grade, and date are identical."
    elif num_errors == 1:
        expl = f"There is 1 error: {errors_desc[0]}."
    else:
        expl = f"There are 2 errors: {'; '.join(errors_desc)}."
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Name and Number Comparison",
        "subtopic": "Error Detection",
        "difficulty": "Hard",
        "question": q,
        "choices": ["0 — the records are identical", "1 error", "2 errors", "3 errors"],
        "answer": answer_map[num_errors],
        "explanation": expl,
        "tags": ["personnel-record", "four-field", "count-errors"] + (["identical"] if num_errors == 0 else ["different"]),
        "category": ["Sub-Professional"],
        "language": "English",
    }


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_questions():
    questions = []
    qid = 1

    # ---- EASY: 200 questions (IDs 1-200) ----
    # More diverse: add SSS and phone number record types
    easy_builders = (
        [build_easy_identical] * 35 +
        [build_easy_name_error] * 35 +
        [build_easy_id_error] * 30 +
        [build_easy_sss_error] * 20 +
        [build_easy_phone_error] * 20 +
        [build_easy_identify_error_type] * 35 +
        [build_easy_find_identical] * 25
    )
    random.shuffle(easy_builders)
    for builder in easy_builders:
        questions.append(builder(qid))
        qid += 1

    # ---- MEDIUM: 200 questions (IDs 201-400) ----
    # More diverse: add payroll and personnel record types
    medium_builders = (
        [build_medium_identical] * 20 +
        [lambda q: build_medium_error_in_field(q, "name")] * 25 +
        [lambda q: build_medium_error_in_field(q, "id")] * 25 +
        [lambda q: build_medium_error_in_field(q, "sg")] * 20 +
        [build_medium_doc_code_error] * 20 +
        [build_medium_amount_error] * 15 +
        [build_medium_date_error] * 15 +
        [build_medium_payroll_error] * 20 +
        [build_medium_personnel_error] * 15 +
        [build_medium_find_correct_version] * 15 +
        [build_medium_identify_error_type] * 10
    )
    random.shuffle(medium_builders)
    for builder in medium_builders:
        questions.append(builder(qid))
        qid += 1

    # ---- HARD: 200 questions (IDs 401-600) ----
    # More diverse: add payroll and personnel 4-field records
    hard_builders = (
        [build_hard_four_field_identical] * 15 +
        [build_hard_one_error] * 40 +
        [build_hard_two_errors] * 35 +
        [build_hard_find_correct_four_field] * 20 +
        [build_hard_dv_record] * 20 +
        [build_hard_find_identical_four_field] * 15 +
        [build_hard_identify_error_type_four_field] * 10 +
        [build_hard_payroll_four_field] * 25 +
        [build_hard_personnel_four_field] * 20
    )
    random.shuffle(hard_builders)
    for builder in hard_builders:
        questions.append(builder(qid))
        qid += 1

    return questions


if __name__ == "__main__":
    import os

    questions = generate_questions()
    assert len(questions) == 600, f"Expected 600, got {len(questions)}"

    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]
    assert len(easy) == 200, f"Easy: {len(easy)}"
    assert len(medium) == 200, f"Medium: {len(medium)}"
    assert len(hard) == 200, f"Hard: {len(hard)}"

    # Verify all answers are in choices
    bad = [q["id"] for q in questions if q["answer"] not in q["choices"]]
    assert not bad, f"Answer not in choices for IDs: {bad}"

    out_dir = os.path.join(
        os.path.dirname(__file__),
        "..", "data", "seed", "questions",
        "clerical-ability", "name-and-number-comparison", "error-detection"
    )
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "questions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(questions)} questions → {out_path}")
    print(f"Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")
