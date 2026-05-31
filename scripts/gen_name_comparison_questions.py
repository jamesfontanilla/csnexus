"""
Generate 600 name comparison questions for the CSE reviewer.
200 Easy, 200 Medium, 200 Hard.

Question types:
- Are these names identical? (Yes/No with identification)
- Which pair is identical?
- Which pair is NOT identical?
- How many pairs are identical/not identical?
- What type of error exists?
"""

import json
import random
import os

random.seed(42)

# Track used combinations to avoid duplicates
_used_question_keys = set()

# --- Name Data ---

SURNAMES = [
    "SANTOS", "REYES", "CRUZ", "BAUTISTA", "GARCIA", "MENDOZA", "TORRES",
    "VILLANUEVA", "GONZALES", "HERNANDEZ", "RODRIGUEZ", "AQUINO", "RAMOS",
    "TOLENTINO", "PANGILINAN", "ENRIQUEZ", "MANALO", "GUERRERO", "CASTILLO",
    "FERNANDEZ", "MARTINEZ", "SANTIAGO", "ALVAREZ", "MORALES", "JIMENEZ",
    "NAVARRO", "DOMINGUEZ", "AGUILAR", "PASCUAL", "SORIANO", "MERCADO",
    "SALVADOR", "ESPINOSA", "DELGADO", "ROSARIO", "FRANCISCO", "LORENZO",
    "MARQUEZ", "PEREZ", "RAMIREZ", "VELASCO", "CABRERA", "MIRANDA",
    "SALAZAR", "OCAMPO", "MAGBANUA", "DIMACULANGAN", "EVANGELISTA",
    "CONSTANTINO", "BUENAVENTURA", "VILLACORTA", "MAGSAYSAY", "LAUREL",
    "MACAPAGAL", "OSMENA", "QUEZON", "ROXAS", "QUIRINO", "GARCIA",
    "DIOKNO", "TANADA", "SUMULONG", "RECTO", "ARANETA", "ZOBEL",
    "AYALA", "COJUANGCO", "ONGPIN", "YUCHENGCO", "GOKONGWEI",
    "CONCEPCION", "ABOITIZ", "ALCANTARA", "FLOIRENDO", "UYANGUREN",
    "VILLAMOR", "PALMA", "MABINI", "BONIFACIO", "JACINTO", "SILANG",
    "DAGOHOY", "TUPAS", "LEGASPI", "URDANETA", "SALCEDO", "LACSON",
    "ESCUDERO", "BINAY", "ESTRADA", "ARROYO", "DUTERTE", "MARCOS"
]

FIRST_NAMES = [
    "JUAN", "MARIA", "JOSE", "ANNA", "PEDRO", "ELENA", "CARLOS", "TERESA",
    "ROBERTO", "PATRICIA", "ANTONIO", "LOURDES", "FRANCISCO", "SOFIA",
    "MICHAEL", "GRACE", "RICARDO", "CHRISTINE", "ALEJANDRO", "ISABELLE",
    "FERNANDO", "ANGELICA", "EDUARDO", "ROSARIO", "BENJAMIN", "CARMELA",
    "GABRIEL", "DIANA", "RAFAEL", "VICTORIA", "DANIEL", "KATHERINE",
    "CHRISTOPHER", "STEPHANIE", "NATHANIEL", "MICHELLE", "DOMINIC", "ANDREA",
    "MARCO", "BIANCA", "LORENZO", "CAMILLE", "VINCENT", "JASMINE",
    "ANGELO", "NICOLE", "JEROME", "CLARISSA", "ALDRIN", "PRINCESS",
    "MARK", "JOANNE", "PAUL", "CATHERINE", "JAMES", "ELIZABETH",
    "JOHN", "MARGARET", "WILLIAM", "THERESA", "ROBERT", "VIRGINIA",
    "DAVID", "JOSEPHINE", "RICHARD", "ROSEMARIE", "THOMAS", "ANNABELLE"
]

MIDDLE_NAMES = [
    "REYES", "SANTOS", "CRUZ", "GARCIA", "BAUTISTA", "MENDOZA", "TORRES",
    "VILLANUEVA", "GONZALES", "HERNANDEZ", "AQUINO", "RAMOS", "CASTILLO",
    "FERNANDEZ", "MARTINEZ", "MORALES", "NAVARRO", "AGUILAR", "PASCUAL",
    "SORIANO", "MERCADO", "SALVADOR", "DELGADO", "ROSARIO", "LORENZO"
]

PARTICLES = ["DELA", "DE LA", "DELOS", "DE LOS", "DEL", "SAN", "SANTA", "STO."]

SUFFIXES = ["JR.", "SR.", "II", "III", "IV"]

# --- Error Generation Functions ---

def substitute_char(name: str) -> str:
    """Replace one character with a similar-looking or nearby character."""
    substitutions = {
        'S': 'Z', 'Z': 'S', 'I': 'E', 'E': 'I', 'A': 'O', 'O': 'A',
        'N': 'M', 'M': 'N', 'B': 'D', 'D': 'B', 'C': 'K', 'K': 'C',
        'L': 'I', 'T': 'F', 'F': 'T', 'P': 'B', 'G': 'C', 'V': 'W',
        'W': 'V', 'U': 'O', 'R': 'P'
    }
    # Find valid positions (letters only, not spaces/punctuation)
    positions = [i for i, c in enumerate(name) if c.isalpha()]
    if not positions:
        return name
    pos = random.choice(positions)
    char = name[pos]
    replacement = substitutions.get(char, 'X')
    return name[:pos] + replacement + name[pos+1:]


def transpose_chars(name: str) -> str:
    """Swap two adjacent alphabetic characters."""
    positions = [i for i in range(len(name)-1)
                 if name[i].isalpha() and name[i+1].isalpha() and name[i] != name[i+1]]
    if not positions:
        return substitute_char(name)
    pos = random.choice(positions)
    return name[:pos] + name[pos+1] + name[pos] + name[pos+2:]


def omit_char(name: str) -> str:
    """Remove one character (preferring double letters)."""
    # Prefer removing from double letters
    for i in range(len(name)-1):
        if name[i] == name[i+1] and name[i].isalpha():
            return name[:i] + name[i+1:]
    # Otherwise remove a random letter
    positions = [i for i, c in enumerate(name) if c.isalpha()]
    if not positions:
        return name
    pos = random.choice(positions[1:-1]) if len(positions) > 2 else positions[0]
    return name[:pos] + name[pos+1:]


def add_char(name: str) -> str:
    """Insert a duplicate of an adjacent character (creating a double)."""
    positions = [i for i, c in enumerate(name) if c.isalpha()]
    if not positions:
        return name
    pos = random.choice(positions)
    return name[:pos] + name[pos] + name[pos:]


def change_spacing(name: str) -> str:
    """Change spacing in particle names."""
    replacements = [
        ("DELA ", "DE LA "), ("DE LA ", "DELA "),
        ("DELOS ", "DE LOS "), ("DE LOS ", "DELOS "),
        ("SAN ", "SA N"), ("DEL ", "DE L"),
    ]
    for old, new in replacements:
        if old in name:
            return name.replace(old, new, 1)
    # If no particle, add/remove a space somewhere
    if "  " in name:
        return name.replace("  ", " ", 1)
    positions = [i for i, c in enumerate(name) if c == ' ']
    if positions:
        pos = random.choice(positions)
        return name[:pos] + name[pos+1:]  # remove space
    return name


def change_punctuation(name: str) -> str:
    """Add or remove punctuation."""
    if "." in name:
        # Remove a period
        pos = name.index(".")
        return name[:pos] + name[pos+1:]
    if "," in name:
        # Remove comma
        pos = name.index(",")
        return name[:pos] + name[pos+1:]
    # Add a period after a 2-3 letter segment
    parts = name.split()
    for i, part in enumerate(parts):
        if 2 <= len(part) <= 3 and part.isalpha():
            parts[i] = part + "."
            return " ".join(parts)
    return substitute_char(name)

def rn_m_swap(name: str) -> str:
    """Swap 'RN' with 'M' or vice versa (visual confusion)."""
    if "RN" in name:
        return name.replace("RN", "M", 1)
    if "M" in name and name.index("M") > 0:
        pos = name.index("M")
        return name[:pos] + "RN" + name[pos+1:]
    return substitute_char(name)


# --- Name Generation ---

def generate_simple_name() -> str:
    """Generate a simple surname only, avoiding recent repeats."""
    return random.choice(SURNAMES)


def generate_unique_simple_name(used: set) -> str:
    """Generate a surname not already in the used set."""
    available = [s for s in SURNAMES if s not in used]
    if not available:
        # If all used, just pick random
        return random.choice(SURNAMES)
    name = random.choice(available)
    used.add(name)
    return name


def generate_full_name(include_particle=False, include_suffix=False) -> str:
    """Generate a full name: SURNAME, FIRSTNAME MIDDLENAME"""
    surname = random.choice(SURNAMES)
    if include_particle:
        particle = random.choice(PARTICLES)
        surname = f"{particle} {surname}"
    first = random.choice(FIRST_NAMES)
    middle = random.choice(MIDDLE_NAMES)
    # Avoid same surname and middle name
    while middle == surname or middle == surname.split()[-1]:
        middle = random.choice(MIDDLE_NAMES)

    name = f"{surname}, {first} {middle}"
    if include_suffix:
        name += f" {random.choice(SUFFIXES)}"
    return name


def generate_abbreviated_name() -> str:
    """Generate name with MA. or STA. abbreviation."""
    surname = random.choice(SURNAMES)
    abbrev = random.choice(["MA.", "STA.", "STO."])
    second = random.choice(["TERESA", "LOURDES", "CLARA", "ROSA", "ELENA", "LUCIA"])
    middle = random.choice(MIDDLE_NAMES)
    return f"{surname}, {abbrev} {second} {middle}"


# --- Question Generation ---

def make_error(name: str, error_type: str) -> str:
    """Apply a specific error type to a name."""
    if error_type == "substitution":
        return substitute_char(name)
    elif error_type == "transposition":
        return transpose_chars(name)
    elif error_type == "omission":
        return omit_char(name)
    elif error_type == "addition":
        return add_char(name)
    elif error_type == "spacing":
        return change_spacing(name)
    elif error_type == "punctuation":
        return change_punctuation(name)
    elif error_type == "rn_m":
        return rn_m_swap(name)
    else:
        return substitute_char(name)


def get_error_explanation(name_a: str, name_b: str, error_type: str) -> str:
    """Generate explanation for the error."""
    explanations = {
        "substitution": f"'{name_a}' and '{name_b}' differ by one character substitution.",
        "transposition": f"'{name_a}' and '{name_b}' have two adjacent characters swapped.",
        "omission": f"'{name_b}' is missing a character that appears in '{name_a}'.",
        "addition": f"'{name_b}' has an extra character not present in '{name_a}'.",
        "spacing": f"'{name_a}' and '{name_b}' differ in spacing.",
        "punctuation": f"'{name_a}' and '{name_b}' differ in punctuation.",
        "rn_m": f"'{name_a}' and '{name_b}' differ — 'rn' vs 'm' visual confusion.",
    }
    return explanations.get(error_type, f"The names differ: '{name_a}' vs '{name_b}'.")

# --- Easy Questions (IDs 1-200) ---
# Simple surname-only or short name comparisons
# Single obvious difference or identical pairs
# Question types: "Are these identical?" with Yes/No choices

def generate_easy_questions() -> list:
    questions = []
    qid = 1
    used_names_identical = set()
    used_names_different = set()

    # Type 1: Are these names identical? (Yes/No) - 100 questions
    # 50 identical pairs, 50 with one obvious difference
    for i in range(50):
        name = generate_unique_simple_name(used_names_identical)
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Easy",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {name}",
            "choices": ["Yes, they are identical", "No, they differ by one letter",
                       "No, they differ by spacing", "No, they differ by punctuation"],
            "answer": "Yes, they are identical",
            "explanation": f"Both names are exactly '{name}' — all characters match.",
            "tags": ["identical-pair", "surname-only"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    easy_errors = ["substitution", "transposition", "omission", "addition"]
    for i in range(50):
        name = generate_unique_simple_name(used_names_different)
        error_type = random.choice(easy_errors)
        modified = make_error(name, error_type)
        # Ensure they're actually different
        attempts = 0
        while modified == name and attempts < 10:
            modified = make_error(name, error_type)
            attempts += 1
        if modified == name:
            modified = substitute_char(name)

        error_labels = {
            "substitution": "No, they differ by one letter",
            "transposition": "No, they differ by one letter",
            "omission": "No, they differ by one letter",
            "addition": "No, they differ by one letter",
        }
        correct_answer = error_labels.get(error_type, "No, they differ by one letter")

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Easy",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {modified}",
            "choices": ["Yes, they are identical", "No, they differ by one letter",
                       "No, they differ by spacing", "No, they differ by punctuation"],
            "answer": correct_answer,
            "explanation": get_error_explanation(name, modified, error_type),
            "tags": [f"{error_type}-error", "surname-only"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 2: Which pair is identical? (4 pairs, one is identical) - 50 questions
    for i in range(50):
        # Generate 4 names, make 3 have errors, 1 stays identical
        identical_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            name = generate_simple_name()
            if j == identical_pos:
                pairs.append((name, name))
            else:
                error_type = random.choice(easy_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))

        labels = ["A", "B", "C", "D"]
        choices_text = []
        for idx, (a, b) in enumerate(pairs):
            choices_text.append(f"{a} / {b}")

        pair_display = "; ".join([f"{labels[i]}. {a} vs. {b}" for i, (a, b) in enumerate(pairs)])
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Easy",
            "question": f"Which of the following pairs contains names that are IDENTICAL?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only '{pairs[identical_pos][0]}' / '{pairs[identical_pos][1]}' are identical. The other pairs each contain a character difference.",
            "tags": ["which-identical", "surname-only"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 3: Which pair is NOT identical? (4 pairs, 3 identical, 1 different) - 50 questions
    for i in range(50):
        different_pos = random.randint(0, 3)
        pairs = []
        error_type = random.choice(easy_errors)
        for j in range(4):
            name = generate_simple_name()
            if j == different_pos:
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))
            else:
                pairs.append((name, name))

        choices_text = []
        for idx, (a, b) in enumerate(pairs):
            choices_text.append(f"{a} / {b}")

        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[i]}. {a} vs. {b}" for i, (a, b) in enumerate(pairs)])
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Easy",
            "question": f"Which of the following pairs contains names that are NOT identical?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[different_pos],
            "explanation": f"'{pairs[different_pos][0]}' and '{pairs[different_pos][1]}' differ ({error_type} error). All other pairs are identical.",
            "tags": ["which-not-identical", "surname-only"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Fill remaining to reach 200
    while len(questions) < 200:
        name = generate_simple_name()
        error_type = random.choice(easy_errors)
        modified = make_error(name, error_type)
        if modified == name:
            modified = substitute_char(name)

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Easy",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {modified}",
            "choices": ["Yes, they are identical", "No, they differ by one letter",
                       "No, they differ by spacing", "No, they differ by punctuation"],
            "answer": "No, they differ by one letter",
            "explanation": get_error_explanation(name, modified, error_type),
            "tags": [f"{error_type}-error", "surname-only"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    return questions[:200]

# --- Medium Questions (IDs 201-400) ---
# Full names (surname, first, middle)
# May include particles or abbreviations
# Differences can be in any component

def generate_medium_questions() -> list:
    questions = []
    qid = 201

    medium_errors = ["substitution", "transposition", "omission", "addition", "spacing", "punctuation"]

    # Type 1: Are these full names identical? - 60 questions (30 identical, 30 different)
    for i in range(30):
        include_particle = random.random() < 0.3
        include_suffix = random.random() < 0.2
        name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {name}",
            "choices": ["Yes, they are identical",
                       "No, they differ in the surname",
                       "No, they differ in the first name",
                       "No, they differ in the middle name"],
            "answer": "Yes, they are identical",
            "explanation": f"Both names are exactly '{name}' — all characters, spaces, and punctuation match.",
            "tags": ["identical-pair", "full-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    for i in range(30):
        include_particle = random.random() < 0.4
        include_suffix = random.random() < 0.2
        name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)
        error_type = random.choice(medium_errors)

        # Apply error to a specific part
        parts = name.split(", ", 1)
        surname = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        target_part = random.choice(["surname", "rest"])
        if target_part == "surname":
            modified_surname = make_error(surname, error_type)
            if modified_surname == surname:
                modified_surname = substitute_char(surname)
            if modified_surname != surname:
                modified = f"{modified_surname}, {rest}"
            else:
                # Fallback to rest
                target_part = "rest"
                modified_rest = make_error(rest, error_type)
                if modified_rest == rest:
                    modified_rest = substitute_char(rest)
                modified = f"{surname}, {modified_rest}"
        else:
            modified_rest = make_error(rest, error_type)
            if modified_rest == rest:
                modified_rest = substitute_char(rest)
            if modified_rest != rest:
                modified = f"{surname}, {modified_rest}"
            else:
                # Fallback to surname
                target_part = "surname"
                modified_surname = make_error(surname, error_type)
                if modified_surname == surname:
                    modified_surname = substitute_char(surname)
                modified = f"{modified_surname}, {rest}"

        if modified == name:
            modified = substitute_char(name)

        # Determine correct answer by checking what actually differs
        parts_mod = modified.split(", ", 1)
        sur_mod = parts_mod[0]
        rest_mod = parts_mod[1] if len(parts_mod) > 1 else ""

        if sur_mod != surname:
            correct_answer = "No, they differ in the surname"
        elif rest_mod != rest:
            correct_answer = "No, they differ in the first name"
        else:
            correct_answer = "No, they differ in the surname"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {modified}",
            "choices": ["Yes, they are identical",
                       "No, they differ in the surname",
                       "No, they differ in the first name",
                       "No, they differ in the middle name"],
            "answer": correct_answer,
            "explanation": get_error_explanation(name, modified, error_type),
            "tags": [f"{error_type}-error", "full-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 2: Which pair is identical? (full names) - 50 questions
    for i in range(50):
        identical_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            include_particle = random.random() < 0.3
            name = generate_full_name(include_particle=include_particle)
            if j == identical_pos:
                pairs.append((name, name))
            else:
                error_type = random.choice(medium_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))

        choices_text = [f"{a} / {b}" for a, b in pairs]

        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[i]}. {a} vs. {b}" for i, (a, b) in enumerate(pairs)])
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"Which of the following pairs contains IDENTICAL names?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only the pair '{pairs[identical_pos][0]}' is repeated identically. The other pairs each contain a discrepancy.",
            "tags": ["which-identical", "full-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 3: What type of error? - 30 questions
    error_type_choices = ["Substitution", "Transposition", "Omission", "Addition"]
    for i in range(30):
        name = generate_simple_name()
        error_idx = random.randint(0, 3)
        error_types_map = ["substitution", "transposition", "omission", "addition"]
        error_type = error_types_map[error_idx]
        modified = make_error(name, error_type)
        attempts = 0
        while modified == name and attempts < 10:
            modified = make_error(name, error_type)
            attempts += 1
        if modified == name:
            modified = substitute_char(name)
            error_idx = 0

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"What type of error exists between these names?\n\nName A: {name}\nName B: {modified}",
            "choices": error_type_choices,
            "answer": error_type_choices[error_idx],
            "explanation": f"'{name}' vs '{modified}' — {error_type_choices[error_idx].lower()} error: {get_error_explanation(name, modified, error_type)}",
            "tags": ["error-type-identification", error_type],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 4: Which pair is NOT identical? (full names) - 30 questions
    for i in range(30):
        different_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            include_particle = random.random() < 0.3
            name = generate_full_name(include_particle=include_particle)
            if j == different_pos:
                error_type = random.choice(medium_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))
            else:
                pairs.append((name, name))

        choices_text = [f"{a} / {b}" for a, b in pairs]

        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[i]}. {a} vs. {b}" for i, (a, b) in enumerate(pairs)])
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"Which of the following pairs contains names that are NOT identical?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[different_pos],
            "explanation": f"'{pairs[different_pos][0]}' and '{pairs[different_pos][1]}' differ. All other pairs are identical.",
            "tags": ["which-not-identical", "full-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Fill remaining to reach 200
    while len(questions) < 200:
        include_particle = random.random() < 0.4
        include_suffix = random.random() < 0.3
        name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)
        error_type = random.choice(medium_errors)

        # Decide where to apply the error and track it
        parts = name.split(", ", 1)
        surname = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        # Randomly choose target, but verify the error actually lands there
        target_part = random.choice(["surname", "rest"])
        if target_part == "surname":
            modified_surname = make_error(surname, error_type)
            if modified_surname == surname:
                modified_surname = substitute_char(surname)
            if modified_surname == surname:
                # Can't modify surname, try rest
                target_part = "rest"
                modified_rest = make_error(rest, error_type)
                if modified_rest == rest:
                    modified_rest = substitute_char(rest)
                modified = f"{surname}, {modified_rest}"
            else:
                modified = f"{modified_surname}, {rest}"
        else:
            modified_rest = make_error(rest, error_type)
            if modified_rest == rest:
                modified_rest = substitute_char(rest)
            if modified_rest == rest:
                # Can't modify rest, try surname
                target_part = "surname"
                modified_surname = make_error(surname, error_type)
                if modified_surname == surname:
                    modified_surname = substitute_char(surname)
                modified = f"{modified_surname}, {rest}"
            else:
                modified = f"{surname}, {modified_rest}"

        if modified == name:
            modified = substitute_char(name)
            # Determine where the change actually is
            parts_m = modified.split(", ", 1)
            if parts_m[0] != surname:
                target_part = "surname"
            else:
                target_part = "rest"

        # Verify the answer matches reality
        parts_mod = modified.split(", ", 1)
        sur_mod = parts_mod[0]
        rest_mod = parts_mod[1] if len(parts_mod) > 1 else ""

        if sur_mod != surname:
            correct_answer = "No, they differ in the surname"
        elif rest_mod != rest:
            correct_answer = "No, they differ in the first/middle name"
        else:
            # Shouldn't happen, but fallback
            correct_answer = "No, they differ in the surname"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Medium",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {modified}",
            "choices": ["Yes, they are identical",
                       "No, they differ in the surname",
                       "No, they differ in the first/middle name",
                       "No, they differ in punctuation or spacing"],
            "answer": correct_answer,
            "explanation": get_error_explanation(name, modified, error_type),
            "tags": [f"{error_type}-error", "full-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    return questions[:200]

# --- Hard Questions (IDs 401-600) ---
# Full names with particles, suffixes, abbreviations
# Multiple subtle differences, rn/m swaps, very similar names
# "How many pairs are identical?" counting questions

def generate_hard_questions() -> list:
    questions = []
    qid = 401

    hard_errors = ["substitution", "transposition", "omission", "addition",
                   "spacing", "punctuation", "rn_m"]

    # Type 1: Complex full names with subtle errors - 50 questions
    for i in range(50):
        include_particle = random.random() < 0.5
        include_suffix = random.random() < 0.4
        if random.random() < 0.3:
            name = generate_abbreviated_name()
        else:
            name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)

        error_type = random.choice(hard_errors)
        modified = make_error(name, error_type)
        attempts = 0
        while modified == name and attempts < 10:
            error_type = random.choice(hard_errors)
            modified = make_error(name, error_type)
            attempts += 1
        if modified == name:
            modified = substitute_char(name)

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Hard",
            "question": f"Are the following names identical?\n\nName A: {name}\nName B: {modified}",
            "choices": ["Yes, they are identical",
                       "No, there is a substitution error",
                       "No, there is a transposition error",
                       "No, there is an omission or addition error"],
            "answer": "No, there is a substitution error" if error_type in ["substitution", "rn_m"]
                      else "No, there is a transposition error" if error_type == "transposition"
                      else "No, there is an omission or addition error",
            "explanation": get_error_explanation(name, modified, error_type),
            "tags": [f"{error_type}-error", "complex-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 2: How many pairs are identical? (5 pairs shown) - 40 questions
    for i in range(40):
        num_identical = random.randint(1, 4)
        identical_positions = random.sample(range(5), num_identical)
        pairs = []
        for j in range(5):
            include_particle = random.random() < 0.4
            name = generate_full_name(include_particle=include_particle)
            if j in identical_positions:
                pairs.append((name, name))
            else:
                error_type = random.choice(hard_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))

        pair_lines = "\n".join([f"{idx+1}. {a}  |  {b}" for idx, (a, b) in enumerate(pairs)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Hard",
            "question": f"How many of the following pairs contain IDENTICAL names?\n\n{pair_lines}",
            "choices": ["1", "2", "3", "4"],
            "answer": str(num_identical),
            "explanation": f"{num_identical} pair(s) are identical (pairs at positions {[p+1 for p in identical_positions]}). The others contain character discrepancies.",
            "tags": ["counting-identical", "complex-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 3: How many pairs are NOT identical? (5 pairs) - 40 questions
    for i in range(40):
        num_different = random.randint(1, 4)
        different_positions = random.sample(range(5), num_different)
        pairs = []
        for j in range(5):
            include_particle = random.random() < 0.4
            include_suffix = random.random() < 0.3
            name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)
            if j in different_positions:
                error_type = random.choice(hard_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))
            else:
                pairs.append((name, name))

        pair_lines = "\n".join([f"{idx+1}. {a}  |  {b}" for idx, (a, b) in enumerate(pairs)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Hard",
            "question": f"How many of the following pairs contain names that are NOT identical?\n\n{pair_lines}",
            "choices": ["1", "2", "3", "4"],
            "answer": str(num_different),
            "explanation": f"{num_different} pair(s) are not identical (pairs at positions {[p+1 for p in different_positions]}). The others are exact matches.",
            "tags": ["counting-not-identical", "complex-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 4: Which pair is identical? (very similar complex names) - 40 questions
    for i in range(40):
        identical_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            include_particle = random.random() < 0.5
            include_suffix = random.random() < 0.3
            if random.random() < 0.3:
                name = generate_abbreviated_name()
            else:
                name = generate_full_name(include_particle=include_particle, include_suffix=include_suffix)
            if j == identical_pos:
                pairs.append((name, name))
            else:
                error_type = random.choice(hard_errors)
                modified = make_error(name, error_type)
                attempts = 0
                while modified == name and attempts < 10:
                    modified = make_error(name, error_type)
                    attempts += 1
                if modified == name:
                    modified = substitute_char(name)
                pairs.append((name, modified))

        choices_text = [f"{a} / {b}" for a, b in pairs]

        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[i]}. {a} vs. {b}" for i, (a, b) in enumerate(pairs)])
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Hard",
            "question": f"Which of the following pairs contains names that are EXACTLY identical?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only '{pairs[identical_pos][0]}' is repeated exactly. The other pairs contain subtle differences (substitution, transposition, spacing, or punctuation errors).",
            "tags": ["which-identical", "complex-name", "subtle-difference"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 5: Identify ALL errors in a pair - 30 questions
    for i in range(30):
        include_particle = random.random() < 0.5
        name = generate_full_name(include_particle=include_particle, include_suffix=True)
        error_type = random.choice(hard_errors)
        modified = make_error(name, error_type)
        attempts = 0
        while modified == name and attempts < 10:
            error_type = random.choice(hard_errors)
            modified = make_error(name, error_type)
            attempts += 1
        if modified == name:
            modified = substitute_char(name)
            error_type = "substitution"

        error_desc = {
            "substitution": "One letter is replaced by a different letter",
            "transposition": "Two adjacent letters are swapped",
            "omission": "One letter is missing",
            "addition": "One extra letter is inserted",
            "spacing": "The spacing between words differs",
            "punctuation": "A punctuation mark is added or removed",
            "rn_m": "The letters 'rn' are replaced by 'm' or vice versa",
        }

        # Create plausible wrong answers
        all_descs = list(error_desc.values())
        correct_desc = error_desc[error_type]
        wrong_descs = [d for d in all_descs if d != correct_desc]
        random.shuffle(wrong_descs)
        choices = [correct_desc] + wrong_descs[:3]
        random.shuffle(choices)

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Name Comparison",
            "difficulty": "Hard",
            "question": f"What is the difference between these names?\n\nName A: {name}\nName B: {modified}",
            "choices": choices,
            "answer": correct_desc,
            "explanation": f"Comparing '{name}' with '{modified}': {correct_desc.lower()}.",
            "tags": ["error-identification", "complex-name", error_type],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    return questions[:200]

# --- Main ---

def main():
    easy = generate_easy_questions()
    medium = generate_medium_questions()
    hard = generate_hard_questions()

    # Renumber sequentially
    all_questions = []
    for idx, q in enumerate(easy + medium + hard, start=1):
        q["id"] = idx
        all_questions.append(q)

    # Verify counts
    easy_count = sum(1 for q in all_questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in all_questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in all_questions if q["difficulty"] == "Hard")
    print(f"Generated: {easy_count} Easy, {medium_count} Medium, {hard_count} Hard = {len(all_questions)} total")

    # Validate answers are in choices
    errors = 0
    for q in all_questions:
        if q["answer"] not in q["choices"]:
            print(f"ERROR: Question {q['id']} answer '{q['answer']}' not in choices")
            errors += 1

    if errors:
        print(f"\n{errors} validation errors found!")
    else:
        print("All answers validated successfully.")

    # Write output
    output_dir = os.path.join("data", "seed", "questions", "clerical-ability",
                              "name-and-number-comparison", "name-comparison")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
