"""
Generate 600-question bank for Indexing Basics.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).

Topics covered:
- Key unit identification (surname first)
- Filing unit separation and counting
- Titles and suffixes handling
- Punctuation rules (hyphens, apostrophes, periods)
- Prefix handling (De, Dela, De Los, etc.)
- Nothing before something (initials vs full names)
- Cross-reference identification
- Indexing order vs filing order
- Mixed indexing scenarios
"""
import json
import random
import os
from itertools import permutations

random.seed(42)

# ============================================================
# DATA POOLS
# ============================================================

GIVEN_NAMES_MALE = [
    "Jose", "Juan", "Pedro", "Roberto", "Carlos", "Antonio", "Fernando",
    "Ricardo", "Eduardo", "Miguel", "Rafael", "Andres", "Manuel", "Luis",
    "Ramon", "Ernesto", "Alfredo", "Arturo", "Sergio", "Enrique",
    "Francisco", "Alejandro", "Rodrigo", "Bernardo", "Gregorio",
    "Leonardo", "Marcelo", "Nestor", "Oscar", "Pablo", "Renato",
    "Salvador", "Teodoro", "Vicente", "Wilfredo"
]

GIVEN_NAMES_FEMALE = [
    "Maria", "Ana", "Elena", "Rosa", "Carmen", "Teresa", "Gloria",
    "Patricia", "Lourdes", "Corazon", "Imelda", "Josefina", "Luisa",
    "Cristina", "Dolores", "Esperanza", "Felicidad", "Gracia",
    "Isabel", "Juliana", "Leonora", "Milagros", "Natividad", "Olivia",
    "Pilar", "Remedios", "Soledad", "Victoria", "Yolanda", "Zenaida",
    "Angelica", "Beatriz", "Catalina", "Diana", "Estrella"
]

GIVEN_NAMES = GIVEN_NAMES_MALE + GIVEN_NAMES_FEMALE

SURNAMES = [
    "Abad", "Abella", "Acosta", "Aguilar", "Aguirre", "Alba",
    "Alcantara", "Almonte", "Alvarez", "Aquino", "Aragon", "Araneta",
    "Bautista", "Bernardo", "Bondoc", "Buenaventura", "Cabrera",
    "Camacho", "Campos", "Carlos", "Castillo", "Castro", "Concepcion",
    "Cordero", "Cruz", "Custodio", "David", "Diaz", "Dizon", "Domingo",
    "Enriquez", "Escueta", "Espino", "Estrada", "Evangelista",
    "Fernandez", "Flores", "Francisco", "Gabriel", "Galang", "Garcia",
    "Gomez", "Gonzales", "Guerrero", "Gutierrez", "Hernandez",
    "Hidalgo", "Ignacio", "Ilagan", "Javier", "Jimenez", "Lacson",
    "Lara", "Laurel", "Lazaro", "Leon", "Lim", "Lopez", "Luna",
    "Macapagal", "Macaraeg", "Magbanua", "Magsaysay", "Manalang",
]

SURNAMES_2 = [
    "Manalo", "Mangubat", "Marquez", "Martinez", "Medina", "Mendoza",
    "Mercado", "Miranda", "Montano", "Morales", "Navarro", "Nicolas",
    "Ocampo", "Olivares", "Ong", "Ortega", "Padilla", "Palma",
    "Pangilinan", "Pascual", "Perez", "Pineda", "Ramos", "Reyes",
    "Rivera", "Rodriguez", "Romero", "Rosales", "Roxas", "Salazar",
    "Salvador", "Sanchez", "Santiago", "Santos", "Soriano", "Tan",
    "Tolentino", "Torres", "Trinidad", "Valdez", "Valencia", "Vargas",
    "Velasco", "Villanueva", "Yap", "Zamora", "Zulueta"
]

SURNAMES = SURNAMES + SURNAMES_2

# Prefixed surnames (prefix + base)
PREFIXED_SURNAMES = [
    ("De", "Leon"), ("De", "Guzman"), ("De", "Castro"), ("De", "Jesus"),
    ("De", "Vera"), ("De", "Asis"), ("De", "Ocampo"), ("De", "Mesa"),
    ("Dela", "Cruz"), ("Dela", "Rosa"), ("Dela", "Torre"), ("Dela", "Paz"),
    ("Dela", "Fuente"), ("Dela", "Vega"), ("De La", "Cruz"),
    ("De La", "Rosa"), ("De La", "Torre"), ("De Los", "Santos"),
    ("De Los", "Reyes"), ("De Los", "Angeles"), ("Del", "Rosario"),
    ("Del", "Mundo"), ("Del", "Pilar"), ("San", "Juan"),
    ("San", "Jose"), ("San", "Miguel"), ("San", "Pedro"),
    ("Santa", "Maria"), ("Santa", "Ana"), ("Santa", "Cruz"),
]

# Hyphenated surname pairs
HYPHENATED_PAIRS = [
    ("Reyes", "Santos"), ("Cruz", "Garcia"), ("Santos", "Reyes"),
    ("Aquino", "Cojuangco"), ("Marcos", "Araneta"), ("Sotto", "Padilla"),
    ("Gonzales", "Rivera"), ("Lopez", "Martinez"), ("Fernandez", "Torres"),
    ("Mendoza", "Castillo"), ("Garcia", "Luna"), ("Bautista", "Enriquez"),
    ("Morales", "Diaz"), ("Romero", "Valdez"), ("Salazar", "Navarro"),
    ("Pangilinan", "Reyes"), ("Villanueva", "Cruz"), ("Padilla", "Santos"),
    ("Ramos", "Aquino"), ("Estrada", "Macapagal"),
]

# Apostrophe names
APOSTROPHE_NAMES = [
    "O'Brien", "O'Malley", "O'Connor", "O'Sullivan", "O'Reilly",
    "D'Angelo", "D'Cruz", "D'Souza", "D'Costa", "D'Silva",
]

TITLES = [
    ("Dr.", "Dr."), ("Atty.", "Atty."), ("Engr.", "Engr."),
    ("Arch.", "Arch."), ("Hon.", "Hon."), ("Gen.", "Gen."),
    ("Col.", "Col."), ("Maj.", "Maj."), ("Capt.", "Capt."),
    ("Rev.", "Rev."), ("Fr.", "Fr."), ("Sr.", "Sr. (Sister)"),
    ("Sen.", "Sen."), ("Rep.", "Rep."), ("Gov.", "Gov."),
    ("Dir.", "Dir."), ("Sec.", "Sec."), ("Usec.", "Usec."),
]

SUFFIXES = ["Jr.", "Sr.", "III", "IV", "II"]

PROFESSIONAL_DESIGNATIONS = ["CPA", "RN", "LPT", "MD", "Ph.D.", "Ed.D.", "MBA"]

MIDDLE_INITIALS = list("ABCDEFGHIJKLMNOPRSTUVWY")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_random_surname():
    return random.choice(SURNAMES)


def get_random_given(gender=None):
    if gender == "M":
        return random.choice(GIVEN_NAMES_MALE)
    elif gender == "F":
        return random.choice(GIVEN_NAMES_FEMALE)
    return random.choice(GIVEN_NAMES)


def get_random_initial():
    return random.choice(MIDDLE_INITIALS) + "."


def get_prefixed_surname():
    prefix, base = random.choice(PREFIXED_SURNAMES)
    return prefix, base


def get_hyphenated_surname():
    return random.choice(HYPHENATED_PAIRS)


def close_up_prefix(prefix, base):
    """Close up prefix with base: 'De La' + 'Cruz' -> 'DeLaCruz'"""
    return prefix.replace(" ", "") + base


def close_up_hyphen(part1, part2):
    """Close up hyphenated name: 'Reyes' + 'Santos' -> 'ReyesSantos'"""
    return part1 + part2


def close_up_apostrophe(name):
    """Remove apostrophe: O'Brien -> OBrien"""
    return name.replace("'", "")


def make_simple_name():
    """Generate: Given Surname"""
    return get_random_given(), get_random_surname()


def make_name_with_middle_initial():
    """Generate: Given M. Surname"""
    return get_random_given(), get_random_initial(), get_random_surname()


def make_name_with_middle_name():
    """Generate: Given Middle Surname"""
    given = get_random_given()
    middle = get_random_surname()  # Filipino middle = mother's maiden surname
    surname = get_random_surname()
    while middle == surname:
        surname = get_random_surname()
    return given, middle, surname


def index_simple_name(given, surname):
    """Index: Surname, Given"""
    return {"key_unit": surname, "unit2": given, "units": [surname, given]}


def index_name_with_initial(given, initial, surname):
    """Index: Surname, Given, Initial"""
    init_clean = initial.replace(".", "")
    return {"key_unit": surname, "unit2": given, "unit3": init_clean,
            "units": [surname, given, init_clean]}


def index_name_with_middle(given, middle, surname):
    """Index: Surname, Given, Middle"""
    return {"key_unit": surname, "unit2": given, "unit3": middle,
            "units": [surname, given, middle]}


def index_prefixed_name(given, prefix, base):
    """Index: PrefixBase (closed up), Given"""
    key = close_up_prefix(prefix, base)
    return {"key_unit": key, "unit2": given, "units": [key, given]}


def index_hyphenated_name(given, part1, part2):
    """Index: Part1Part2 (closed up), Given"""
    key = close_up_hyphen(part1, part2)
    return {"key_unit": key, "unit2": given, "units": [key, given]}


def index_apostrophe_name(given, apo_surname):
    """Index: surname without apostrophe, Given"""
    key = close_up_apostrophe(apo_surname)
    return {"key_unit": key, "unit2": given, "units": [key, given]}


def format_indexed(units, suffix=None, title=None):
    """Format indexed name as string: KeyUnit, Unit2, Unit3 (Suffix) (Title)"""
    result = ", ".join(units)
    if suffix:
        result += f" ({suffix})"
    if title:
        result += f" ({title})"
    return result


def filing_sort_key(units):
    """Sort key for indexed names (list of units)."""
    return [u.lower() for u in units]


# ============================================================
# QUESTION GENERATORS
# ============================================================

def generate_easy_questions():
    """Generate 200 Easy questions (IDs 1-200)."""
    questions = []
    used = set()
    qid = 1

    # --- Type A: Identify the key unit (50 questions) ---
    while len(questions) < 50:
        given = get_random_given()
        surname = get_random_surname()
        name_str = f"{given} {surname}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        choices = [surname, given, f"{given} {surname}", f"{surname} {given}"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Easy",
            "question": f'What is the key unit when indexing the name "{name_str}"?',
            "choices": choices,
            "answer": surname,
            "explanation": f"The key unit for personal names is always the surname. '{surname}' is the surname, so it is the key unit.",
            "tags": ["key-unit", "surname-first"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type B: Identify key unit with title (40 questions) ---
    while len(questions) < 90:
        title, _ = random.choice(TITLES)
        given = get_random_given()
        surname = get_random_surname()
        name_str = f"{title} {given} {surname}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        choices = [surname, given, title.replace(".", ""), f"{title} {given}"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Easy",
            "question": f'What is the key unit when indexing the name "{name_str}"?',
            "choices": choices,
            "answer": surname,
            "explanation": f"Titles like '{title}' are not filing units — they are placed at the end. The key unit is the surname '{surname}'.",
            "tags": ["key-unit", "title-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type C: Count filing units - simple names (35 questions) ---
    while len(questions) < 125:
        variant = random.choice(["two", "three_init", "three_mid"])
        if variant == "two":
            given = get_random_given()
            surname = get_random_surname()
            name_str = f"{given} {surname}"
            correct = "2"
            explanation = f"'{name_str}' has 2 filing units: {surname} (key unit) and {given} (unit 2)."
        elif variant == "three_init":
            given = get_random_given()
            init = get_random_initial()
            surname = get_random_surname()
            name_str = f"{given} {init} {surname}"
            correct = "3"
            explanation = f"'{name_str}' has 3 filing units: {surname} (key unit), {given} (unit 2), and {init.replace('.', '')} (unit 3)."
        else:
            given = get_random_given()
            middle = get_random_surname()
            surname = get_random_surname()
            while middle == surname:
                surname = get_random_surname()
            name_str = f"{given} {middle} {surname}"
            correct = "3"
            explanation = f"'{name_str}' has 3 filing units: {surname} (key unit), {given} (unit 2), and {middle} (unit 3)."

        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        choices = ["2", "3", "4", "1"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Easy",
            "question": f'How many filing units does the name "{name_str}" have?',
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["unit-count"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type D: Correct indexed form - simple (40 questions) ---
    while len(questions) < 165:
        given = get_random_given()
        surname = get_random_surname()
        name_str = f"{given} {surname}"
        if ("indexed_" + name_str.lower()) in used:
            continue
        used.add("indexed_" + name_str.lower())

        correct = f"{surname}, {given}"
        wrong1 = f"{given}, {surname}"
        wrong2 = f"{given} {surname}"
        wrong3 = f"{surname} {given}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Easy",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Personal names are indexed surname first: '{surname}, {given}'.",
            "tags": ["indexed-form", "surname-first"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type E: Where does title go? (35 questions) ---
    while len(questions) < 200:
        title, _ = random.choice(TITLES)
        given = get_random_given()
        surname = get_random_surname()
        name_str = f"{title} {given} {surname}"
        if ("title_" + name_str.lower()) in used:
            continue
        used.add("title_" + name_str.lower())

        correct = f"{surname}, {given} ({title})"
        wrong1 = f"{title} {surname}, {given}"
        wrong2 = f"{surname}, {title} {given}"
        wrong3 = f"({title}) {surname}, {given}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Easy",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Titles are placed at the end in parentheses. Correct form: {surname}, {given} ({title}).",
            "tags": ["indexed-form", "title-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


def generate_medium_questions():
    """Generate 200 Medium questions (IDs 201-400)."""
    questions = []
    used = set()
    qid = 201

    # --- Type A: Prefix handling - key unit identification (35 questions) ---
    while len(questions) < 35:
        prefix, base = get_prefixed_surname()
        given = get_random_given()
        name_str = f"{given} {prefix} {base}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        closed = close_up_prefix(prefix, base)
        choices = [closed, base, prefix, given]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'What is the key unit when indexing "{name_str}"?',
            "choices": choices,
            "answer": closed,
            "explanation": f"Prefixes are closed up with the surname. '{prefix} {base}' becomes '{closed}' as one key unit.",
            "tags": ["key-unit", "prefix-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type B: Hyphenated surname - indexed form (30 questions) ---
    while len(questions) < 65:
        part1, part2 = get_hyphenated_surname()
        given = get_random_given()
        name_str = f"{given} {part1}-{part2}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        closed = close_up_hyphen(part1, part2)
        correct = f"{closed}, {given}"
        wrong1 = f"{part1}, {given}, {part2}"
        wrong2 = f"{part1}-{part2}, {given}"
        wrong3 = f"{part2}, {given}, {part1}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Hyphens are removed and parts closed up. '{part1}-{part2}' becomes '{closed}' as one key unit. Indexed: {closed}, {given}.",
            "tags": ["indexed-form", "hyphen-rule"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type C: Apostrophe names - indexed form (20 questions) ---
    while len(questions) < 85:
        apo_name = random.choice(APOSTROPHE_NAMES)
        given = get_random_given()
        name_str = f"{given} {apo_name}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        closed = close_up_apostrophe(apo_name)
        correct = f"{closed}, {given}"
        wrong1 = f"{apo_name}, {given}"
        wrong2 = f"{given}, {closed}"
        wrong3 = f"{given}, {apo_name}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Apostrophes are removed and letters closed up. '{apo_name}' becomes '{closed}'. Indexed: {closed}, {given}.",
            "tags": ["indexed-form", "apostrophe-rule"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type D: Suffix handling - indexed form (30 questions) ---
    while len(questions) < 115:
        given = get_random_given()
        surname = get_random_surname()
        suffix = random.choice(SUFFIXES)
        name_str = f"{given} {surname} {suffix}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        correct = f"{surname}, {given} ({suffix})"
        wrong1 = f"{surname}, {given}, {suffix}"
        wrong2 = f"{surname} {suffix}, {given}"
        wrong3 = f"{given}, {surname} ({suffix})"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Suffixes are placed at the end in parentheses after all name units. Correct: {surname}, {given} ({suffix}).",
            "tags": ["indexed-form", "suffix-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type E: Nothing before something - which files first (30 questions) ---
    while len(questions) < 145:
        surname = get_random_surname()
        given = get_random_given()
        initial = given[0] + "."
        # Ensure initial letter matches given name first letter
        name_full = f"{given} {surname}"
        name_init = f"{initial} {surname}"
        key = f"nbs_{surname}_{given}".lower()
        if key in used:
            continue
        used.add(key)

        correct = f"{initial} {surname}"
        question_text = f'Which name files FIRST: "{name_init}" or "{name_full}"?'

        choices = [
            f"{initial} {surname}",
            f"{given} {surname}",
            "They file in the same position",
            "Cannot be determined"
        ]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": question_text,
            "choices": choices,
            "answer": correct,
            "explanation": f"'Nothing before something' rule: the initial '{initial.replace('.', '')}' (one letter) files before the full name '{given}'. So '{name_init}' files first.",
            "tags": ["nothing-before-something", "filing-order"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type F: Unit counting with titles/suffixes (25 questions) ---
    while len(questions) < 170:
        title, _ = random.choice(TITLES)
        given = get_random_given()
        init = get_random_initial()
        surname = get_random_surname()
        suffix = random.choice(SUFFIXES)

        variant = random.choice(["title_only", "suffix_only", "both"])
        if variant == "title_only":
            name_str = f"{title} {given} {init} {surname}"
            correct = "3"
            explanation = f"Filing units: {surname} (1), {given} (2), {init.replace('.', '')} (3). The title '{title}' is NOT a filing unit."
        elif variant == "suffix_only":
            name_str = f"{given} {init} {surname} {suffix}"
            correct = "3"
            explanation = f"Filing units: {surname} (1), {given} (2), {init.replace('.', '')} (3). The suffix '{suffix}' is NOT a filing unit for comparison."
        else:
            name_str = f"{title} {given} {init} {surname} {suffix}"
            correct = "3"
            explanation = f"Filing units: {surname} (1), {given} (2), {init.replace('.', '')} (3). Neither '{title}' nor '{suffix}' count as filing units."

        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        choices = ["2", "3", "4", "5"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'How many filing units does "{name_str}" have for comparison purposes?',
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["unit-count", "title-handling", "suffix-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type G: Cross-reference needed? (30 questions) ---
    while len(questions) < 200:
        scenario = random.choice(["hyphenated", "name_change", "nickname", "simple"])

        if scenario == "hyphenated":
            part1, part2 = get_hyphenated_surname()
            given = get_random_given()
            name_str = f"{given} {part1}-{part2}"
            correct = "Yes"
            explanation = f"Hyphenated surnames need a cross-reference. File under '{part1}{part2}' with cross-reference under '{part2}'."
            key = f"xref_hyp_{name_str}".lower()
        elif scenario == "name_change":
            given = get_random_given()
            old_surname = get_random_surname()
            new_surname = get_random_surname()
            while old_surname == new_surname:
                new_surname = get_random_surname()
            name_str = f"{given} {new_surname} (formerly {given} {old_surname})"
            correct = "Yes"
            explanation = f"Name changes require a cross-reference. File under '{new_surname}' with cross-reference under '{old_surname}'."
            key = f"xref_nc_{name_str}".lower()
        elif scenario == "nickname":
            given = get_random_given()
            nickname = random.choice(["Bong", "Jun", "Boy", "Bing", "Nene", "Totoy", "Baby", "Dong", "Inday", "Nena"])
            surname = get_random_surname()
            name_str = f'{given} "{nickname}" {surname}'
            correct = "Yes"
            explanation = f"Nicknames require a cross-reference. File under '{surname}, {given}' with cross-reference under '{surname}, {nickname}'."
            key = f"xref_nick_{name_str}".lower()
        else:
            given = get_random_given()
            surname = get_random_surname()
            name_str = f"{given} {surname}"
            correct = "No"
            explanation = f"Simple names with no alternative forms do not need a cross-reference."
            key = f"xref_simple_{name_str}".lower()

        if key in used:
            continue
        used.add(key)

        choices = ["Yes", "No", "Only if requested", "Depends on the filing system"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Medium",
            "question": f'Does the name "{name_str}" require a cross-reference?',
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["cross-reference"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions[:200]


def generate_hard_questions():
    """Generate 200 Hard questions (IDs 401-600)."""
    questions = []
    used = set()
    qid = 401

    # --- Type A: Complex indexed form (title + prefix + suffix) (35 questions) ---
    while len(questions) < 35:
        title, _ = random.choice(TITLES)
        given = get_random_given()
        init = get_random_initial()
        prefix, base = get_prefixed_surname()
        suffix = random.choice(SUFFIXES)

        name_str = f"{title} {given} {init} {prefix} {base} {suffix}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        closed = close_up_prefix(prefix, base)
        correct = f"{closed}, {given}, {init.replace('.', '')} ({suffix}) ({title})"
        wrong1 = f"{base}, {given}, {init.replace('.', '')} ({title}) ({suffix})"
        wrong2 = f"{prefix} {base}, {given}, {init.replace('.', '')} ({suffix})"
        wrong3 = f"{closed}, {title} {given}, {init.replace('.', '')} {suffix}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Prefix closed up: '{closed}'. Title '{title}' and suffix '{suffix}' go at end in parentheses. Units: {closed}, {given}, {init.replace('.', '')}.",
            "tags": ["indexed-form", "prefix-handling", "title-handling", "suffix-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type B: Complex indexed form (title + hyphenated) (30 questions) ---
    while len(questions) < 65:
        title, _ = random.choice(TITLES)
        given = get_random_given()
        init = get_random_initial()
        part1, part2 = get_hyphenated_surname()

        name_str = f"{title} {given} {init} {part1}-{part2}"
        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        closed = close_up_hyphen(part1, part2)
        correct = f"{closed}, {given}, {init.replace('.', '')} ({title})"
        wrong1 = f"{part1}, {given}, {init.replace('.', '')}, {part2} ({title})"
        wrong2 = f"{part1}-{part2}, {given}, {init.replace('.', '')} ({title})"
        wrong3 = f"{closed}, {title} {given}, {init.replace('.', '')}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f'What is the correct indexed form of "{name_str}"?',
            "choices": choices,
            "answer": correct,
            "explanation": f"Hyphen removed, closed up: '{closed}'. Title '{title}' goes at end. Units: {closed}, {given}, {init.replace('.', '')}.",
            "tags": ["indexed-form", "hyphen-rule", "title-handling"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type C: Filing order - 4 names with same surname (35 questions) ---
    while len(questions) < 100:
        surname = get_random_surname()
        # Create 4 variants
        given1 = get_random_given()
        given2 = get_random_given()
        while given2 == given1:
            given2 = get_random_given()
        init1 = given1[0] + "."

        names = [
            (f"{init1} {surname}", [surname, given1[0]]),
            (f"{given1} {surname}", [surname, given1]),
            (f"{given1} A. {surname}", [surname, given1, "A"]),
            (f"{given2} {surname}", [surname, given2]),
        ]

        key = f"order_{surname}_{given1}_{given2}".lower()
        if key in used:
            continue
        used.add(key)

        # Sort by filing units
        sorted_names = sorted(names, key=lambda x: [u.lower() for u in x[1]])
        correct_order = [n[0] for n in sorted_names]

        # Pick a random question type
        q_type = random.choice(["first", "last", "order"])

        if q_type == "first":
            display_names = [n[0] for n in names]
            random.shuffle(display_names)
            answer = correct_order[0]
            choices = display_names[:4]
            if answer not in choices:
                choices[0] = answer
            random.shuffle(choices)
            question_text = f'Which of the following names files FIRST?'
            explanation = f"After indexing, compare unit by unit. '{answer}' files first by the nothing-before-something rule or alphabetical comparison."
            tags = ["filing-order", "nothing-before-something"]
        elif q_type == "last":
            display_names = [n[0] for n in names]
            random.shuffle(display_names)
            answer = correct_order[-1]
            choices = display_names[:4]
            if answer not in choices:
                choices[-1] = answer
            random.shuffle(choices)
            question_text = f'Which of the following names files LAST?'
            explanation = f"After indexing, compare unit by unit. '{answer}' files last alphabetically."
            tags = ["filing-order"]
        else:
            answer = ", ".join(correct_order)
            # Generate wrong orders
            wrong_orders = []
            for p in permutations(correct_order):
                if list(p) != correct_order:
                    wrong_orders.append(", ".join(p))
            if len(wrong_orders) < 3:
                continue
            wrong_sample = random.sample(wrong_orders, 3)
            choices = [answer] + wrong_sample
            random.shuffle(choices)
            question_text = f'Arrange in correct filing order: {", ".join([n[0] for n in names])}.'
            explanation = f"Index each name (surname first), then compare unit by unit. Correct order: {answer}."
            tags = ["filing-order", "sequencing"]

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": question_text,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": tags,
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type D: Unit counting - complex names (25 questions) ---
    while len(questions) < 125:
        variant = random.choice(["prefix_title_suffix", "hyphen_title", "ma_teresa"])

        if variant == "prefix_title_suffix":
            title, _ = random.choice(TITLES)
            given = get_random_given()
            init = get_random_initial()
            prefix, base = get_prefixed_surname()
            suffix = random.choice(SUFFIXES)
            name_str = f"{title} {given} {init} {prefix} {base} {suffix}"
            correct = "3"
            closed = close_up_prefix(prefix, base)
            explanation = f"Filing units: {closed} (1), {given} (2), {init.replace('.', '')} (3). Title '{title}' and suffix '{suffix}' are NOT filing units."
        elif variant == "hyphen_title":
            title, _ = random.choice(TITLES)
            given = get_random_given()
            middle = get_random_surname()
            part1, part2 = get_hyphenated_surname()
            name_str = f"{title} {given} {middle} {part1}-{part2}"
            correct = "3"
            closed = close_up_hyphen(part1, part2)
            explanation = f"Filing units: {closed} (1), {given} (2), {middle} (3). Title '{title}' is NOT a filing unit. Hyphenated surname is ONE unit."
        else:
            # Ma. Teresa pattern
            title, _ = random.choice(TITLES)
            surname = get_random_surname()
            init = get_random_initial()
            name_str = f"{title} Ma. Teresa {init} {surname}"
            correct = "4"
            explanation = f"Filing units: {surname} (1), Ma (2), Teresa (3), {init.replace('.', '')} (4). 'Ma.' and 'Teresa' are separate units. Title is NOT a filing unit."

        if name_str.lower() in used:
            continue
        used.add(name_str.lower())

        choices = ["2", "3", "4", "5"]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f'How many filing units does "{name_str}" have for comparison purposes?',
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": ["unit-count", "complex-name"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type E: Which rule applies? (25 questions) ---
    while len(questions) < 150:
        rule_type = random.choice([
            "prefix", "hyphen", "apostrophe", "title", "suffix", "initial"
        ])

        if rule_type == "prefix":
            prefix, base = get_prefixed_surname()
            given = get_random_given()
            element = f'"{prefix} {base}" in "{given} {prefix} {base}"'
            correct = "Close up the prefix with the surname into one unit"
            wrong1 = "Treat the prefix as a separate filing unit"
            wrong2 = "Ignore the prefix entirely"
            wrong3 = "File under the base surname only"
            explanation = f"Prefixes like '{prefix}' are closed up with the surname: '{close_up_prefix(prefix, base)}' becomes one key unit."
            tags_q = ["rule-identification", "prefix-handling"]
        elif rule_type == "hyphen":
            part1, part2 = get_hyphenated_surname()
            given = get_random_given()
            element = f'the hyphen in "{given} {part1}-{part2}"'
            correct = "Remove the hyphen and close up into one unit"
            wrong1 = "Treat each part as a separate filing unit"
            wrong2 = "File under the first part only"
            wrong3 = "Keep the hyphen and file as written"
            explanation = f"Hyphens are removed and parts closed up: '{part1}-{part2}' becomes '{part1}{part2}' as one unit."
            tags_q = ["rule-identification", "hyphen-rule"]
        elif rule_type == "apostrophe":
            apo = random.choice(APOSTROPHE_NAMES)
            given = get_random_given()
            element = f'the apostrophe in "{given} {apo}"'
            correct = "Remove the apostrophe and close up the letters"
            wrong1 = "Treat the parts before and after as separate units"
            wrong2 = "Keep the apostrophe and file as written"
            wrong3 = "Ignore the letter before the apostrophe"
            explanation = f"Apostrophes are disregarded. '{apo}' becomes '{close_up_apostrophe(apo)}' as one unit."
            tags_q = ["rule-identification", "apostrophe-rule"]
        elif rule_type == "title":
            title, _ = random.choice(TITLES)
            given = get_random_given()
            surname = get_random_surname()
            element = f'"{title}" in "{title} {given} {surname}"'
            correct = "Place it at the end in parentheses — it is not a filing unit"
            wrong1 = "Use it as the key unit"
            wrong2 = "Treat it as the second filing unit"
            wrong3 = "Ignore it completely — do not record it"
            explanation = f"Titles are not filing units. '{title}' is placed at the end in parentheses for identification only."
            tags_q = ["rule-identification", "title-handling"]
        elif rule_type == "suffix":
            suffix = random.choice(SUFFIXES)
            given = get_random_given()
            surname = get_random_surname()
            element = f'"{suffix}" in "{given} {surname} {suffix}"'
            correct = "Place it at the end in parentheses as a distinguishing element"
            wrong1 = "Treat it as the last filing unit"
            wrong2 = "Place it before the given name"
            wrong3 = "Attach it to the surname as one unit"
            explanation = f"Suffixes like '{suffix}' are not filing units. They are placed at the end in parentheses and used only to distinguish identical names."
            tags_q = ["rule-identification", "suffix-handling"]
        else:  # initial
            given = get_random_given()
            surname = get_random_surname()
            init = given[0] + "."
            element = f'"{init}" compared to "{given}" when both share surname "{surname}"'
            correct = "The initial files before the full name (nothing before something)"
            wrong1 = "The full name files first because it has more information"
            wrong2 = "They file in the same position"
            wrong3 = "Compare the second letter of the full name to determine order"
            explanation = f"'Nothing before something' rule: a single initial '{init.replace('.', '')}' files before the full name '{given}' starting with the same letter."
            tags_q = ["rule-identification", "nothing-before-something"]

        key = f"rule_{element}".lower()
        if key in used:
            continue
        used.add(key)

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f"What indexing rule applies to {element}?",
            "choices": choices,
            "answer": correct,
            "explanation": explanation,
            "tags": tags_q,
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type F: Filing order with mixed name types (30 questions) ---
    while len(questions) < 180:
        # Generate 4 names with different characteristics
        surname = get_random_surname()
        given1 = get_random_given()
        given2 = get_random_given()
        while given2 == given1:
            given2 = get_random_given()
        given3 = get_random_given()
        while given3 in (given1, given2):
            given3 = get_random_given()

        title, _ = random.choice(TITLES)
        suffix = random.choice(SUFFIXES)
        init1 = given1[0] + "."

        # 4 names sharing a surname but with different features
        names_data = [
            (f"{title} {given1} {surname}", [surname, given1]),
            (f"{given1} {surname} {suffix}", [surname, given1]),
            (f"{init1} {surname}", [surname, given1[0]]),
            (f"{given2} {surname}", [surname, given2]),
        ]

        key = f"mixed_order_{surname}_{given1}_{given2}".lower()
        if key in used:
            continue
        used.add(key)

        # Sort by filing units
        sorted_data = sorted(names_data, key=lambda x: [u.lower() for u in x[1]])
        correct_first = sorted_data[0][0]

        display = [n[0] for n in names_data]
        random.shuffle(display)

        choices = display[:4]
        if correct_first not in choices:
            choices[0] = correct_first
            random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f"After proper indexing, which of the following names files FIRST?",
            "choices": choices,
            "answer": correct_first,
            "explanation": f"Index all names (surname first, titles/suffixes at end). Compare filing units only. '{correct_first}' files first based on unit-by-unit comparison.",
            "tags": ["filing-order", "mixed-rules"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type G: Error identification (20 questions) ---
    error_scenarios = [
        {
            "name": "Dr. Maria Santos",
            "wrong_indexing": "Dr., Maria, Santos",
            "error": "Using the title 'Dr.' as a filing unit",
            "correct": "Santos, Maria (Dr.)",
            "explanation": "Titles are never filing units. The correct indexing is: Santos, Maria (Dr.)."
        },
        {
            "name": "Jose Dela Cruz",
            "wrong_indexing": "Dela, Jose, Cruz",
            "error": "Separating the prefix 'Dela' from the surname",
            "correct": "DelaCruz, Jose",
            "explanation": "Prefixes are closed up with the surname. 'Dela Cruz' becomes 'DelaCruz' as one key unit."
        },
        {
            "name": "Anna Reyes-Santos",
            "wrong_indexing": "Reyes, Anna, Santos",
            "error": "Splitting the hyphenated surname into separate units",
            "correct": "ReyesSantos, Anna",
            "explanation": "Hyphenated surnames are one unit. Remove the hyphen and close up: 'ReyesSantos'."
        },
        {
            "name": "Roberto Garcia Jr.",
            "wrong_indexing": "Garcia, Roberto, Jr.",
            "error": "Treating 'Jr.' as a filing unit instead of a distinguishing element",
            "correct": "Garcia, Roberto (Jr.)",
            "explanation": "Suffixes are not filing units. 'Jr.' goes in parentheses at the end as a distinguishing element."
        },
        {
            "name": "Patrick O'Brien",
            "wrong_indexing": "O, Patrick, Brien",
            "error": "Splitting at the apostrophe into separate units",
            "correct": "OBrien, Patrick",
            "explanation": "Apostrophes are removed and letters closed up. 'O'Brien' becomes 'OBrien' as one unit."
        },
        {
            "name": "Hon. Juan De Los Santos",
            "wrong_indexing": "Hon., Juan, De, Los, Santos",
            "error": "Using the title as a unit and separating the prefix",
            "correct": "DeLosSantos, Juan (Hon.)",
            "explanation": "Title goes at end. Prefix 'De Los' is closed up with 'Santos': DeLosSantos, Juan (Hon.)."
        },
        {
            "name": "Elena Santos Cruz",
            "wrong_indexing": "Santos, Elena, Cruz",
            "error": "Using the middle name as the key unit instead of the surname",
            "correct": "Cruz, Elena, Santos",
            "explanation": "In Filipino names, the last name is the surname (key unit). 'Cruz' is the surname, 'Santos' is the middle name."
        },
        {
            "name": "Atty. Ma. Lourdes Reyes",
            "wrong_indexing": "Atty., Ma. Lourdes, Reyes",
            "error": "Treating 'Atty.' as a filing unit and 'Ma. Lourdes' as one unit",
            "correct": "Reyes, Ma, Lourdes (Atty.)",
            "explanation": "Title goes at end. 'Ma.' and 'Lourdes' are separate units. Correct: Reyes, Ma, Lourdes (Atty.)."
        },
        {
            "name": "Gen. Fernando De La Cruz III",
            "wrong_indexing": "De La Cruz, Fernando, III, Gen.",
            "error": "Not closing up the prefix and treating suffix/title incorrectly",
            "correct": "DeLaCruz, Fernando (III) (Gen.)",
            "explanation": "Prefix closed up: DeLaCruz. Suffix and title in parentheses at end. Filing units: DeLaCruz, Fernando."
        },
        {
            "name": "J. P. Santos",
            "wrong_indexing": "Santos, JP",
            "error": "Combining initials into one unit instead of keeping them separate",
            "correct": "Santos, J, P",
            "explanation": "Each initial is a separate filing unit. 'J' is unit 2, 'P' is unit 3."
        },
        {
            "name": "Fr. Pedro B. Santos Sr.",
            "wrong_indexing": "Fr., Santos, Pedro, B, Sr.",
            "error": "Using the title 'Fr.' as the key unit",
            "correct": "Santos, Pedro, B (Sr.) (Fr.)",
            "explanation": "Title and suffix go at end. Key unit is surname. Correct: Santos, Pedro, B (Sr.) (Fr.)."
        },
        {
            "name": "Maria Clara De Guzman",
            "wrong_indexing": "Guzman, Maria, Clara, De",
            "error": "Separating 'De' from 'Guzman' and placing it as a separate unit",
            "correct": "DeGuzman, Maria, Clara",
            "explanation": "Prefix 'De' is closed up with 'Guzman': DeGuzman is one key unit."
        },
        {
            "name": "Col. Roberto Cruz-Aquino Jr.",
            "wrong_indexing": "Cruz, Roberto, Aquino, Jr., Col.",
            "error": "Splitting the hyphenated surname and misplacing suffix/title",
            "correct": "CruzAquino, Roberto (Jr.) (Col.)",
            "explanation": "Hyphen removed, closed up: CruzAquino. Suffix and title in parentheses at end."
        },
        {
            "name": "Ana Marie B. Villanueva",
            "wrong_indexing": "Villanueva, Ana Marie, B",
            "error": "Treating 'Ana Marie' as one unit instead of two separate units",
            "correct": "Villanueva, Ana, Marie, B",
            "explanation": "Each word is a separate filing unit. 'Ana' is unit 2, 'Marie' is unit 3, 'B' is unit 4."
        },
        {
            "name": "Dra. Corazon S. Aquino-Cojuangco",
            "wrong_indexing": "Aquino, Corazon, S, Cojuangco, Dra.",
            "error": "Splitting the hyphenated surname into separate units",
            "correct": "AquinoCojuangco, Corazon, S (Dra.)",
            "explanation": "Hyphen removed: AquinoCojuangco is one key unit. Title at end."
        },
        {
            "name": "Rev. Msgr. Jose A. Santos",
            "wrong_indexing": "Rev., Msgr., Santos, Jose, A",
            "error": "Treating multiple titles as filing units",
            "correct": "Santos, Jose, A (Rev. Msgr.)",
            "explanation": "All titles go at end together. Filing units are: Santos, Jose, A."
        },
        {
            "name": "Elena R. De Los Reyes",
            "wrong_indexing": "De, Elena, R, Los, Reyes",
            "error": "Breaking up 'De Los Reyes' into separate units",
            "correct": "DeLosReyes, Elena, R",
            "explanation": "Prefix 'De Los' is closed up with 'Reyes': DeLosReyes is one key unit."
        },
        {
            "name": "Jose Santos",
            "wrong_indexing": "Jose, Santos",
            "error": "Using the given name as the key unit instead of the surname",
            "correct": "Santos, Jose",
            "explanation": "Personal names are always indexed surname first. 'Santos' is the key unit."
        },
        {
            "name": "Ma. Teresa L. Santos",
            "wrong_indexing": "Santos, Ma. Teresa, L",
            "error": "Treating 'Ma. Teresa' as one unit",
            "correct": "Santos, Ma, Teresa, L",
            "explanation": "'Ma.' and 'Teresa' are separate filing units. Each word/abbreviation is one unit."
        },
        {
            "name": "Vice Gov. Elena Sotto-Padilla",
            "wrong_indexing": "Vice, Gov., Elena, Sotto, Padilla",
            "error": "Splitting the title and hyphenated surname into separate units",
            "correct": "SottoPadilla, Elena (Vice Gov.)",
            "explanation": "Title 'Vice Gov.' goes at end. Hyphenated surname closed up: SottoPadilla."
        },
    ]

    random.shuffle(error_scenarios)
    for scenario in error_scenarios[:20]:
        key = f"error_{scenario['name']}".lower()
        if key in used:
            continue
        used.add(key)

        choices = [
            scenario["error"],
            "The indexing is correct — no error",
            f"The name should be filed under '{scenario['name'].split()[0]}'",
            "The units are in the wrong alphabetical order"
        ]
        random.shuffle(choices)

        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization",
            "subtopic": "Indexing Basics",
            "difficulty": "Hard",
            "question": f'A clerk indexed "{scenario["name"]}" as: {scenario["wrong_indexing"]}. What is the error?',
            "choices": choices,
            "answer": scenario["error"],
            "explanation": scenario["explanation"],
            "tags": ["error-identification"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # --- Type H: Filing order with different surnames + complex rules (remaining) ---
    while len(questions) < 200:
        # Pick 4 names with different surnames, some with prefixes/hyphens
        name_type = random.choice(["prefix_mix", "hyphen_mix", "suffix_compare"])

        if name_type == "prefix_mix":
            prefix, base = get_prefixed_surname()
            closed_prefix = close_up_prefix(prefix, base)
            surname2 = get_random_surname()
            surname3 = get_random_surname()
            while surname2 == surname3 or surname2 == base or surname3 == base:
                surname2 = get_random_surname()
                surname3 = get_random_surname()

            given1 = get_random_given()
            given2 = get_random_given()
            given3 = get_random_given()

            names = [
                (f"{given1} {prefix} {base}", closed_prefix),
                (f"{given2} {surname2}", surname2),
                (f"{given3} {surname3}", surname3),
            ]

            key = f"pfx_mix_{closed_prefix}_{surname2}_{surname3}".lower()
            if key in used:
                continue
            used.add(key)

            sorted_names = sorted(names, key=lambda x: x[1].lower())
            correct_first = sorted_names[0][0]

            display = [n[0] for n in names]
            # Add a 4th distractor
            extra_surname = get_random_surname()
            while extra_surname in (base, surname2, surname3):
                extra_surname = get_random_surname()
            extra_given = get_random_given()
            display.append(f"{extra_given} {extra_surname}")

            all_with_keys = [(d, closed_prefix if prefix in d and base in d else
                             extra_surname if extra_surname in d else
                             surname2 if surname2 in d else surname3)
                            for d in display]
            # Re-sort properly
            name_key_pairs = []
            for d in display:
                if f"{prefix} {base}" in d:
                    name_key_pairs.append((d, closed_prefix))
                elif surname2 in d:
                    name_key_pairs.append((d, surname2))
                elif surname3 in d:
                    name_key_pairs.append((d, surname3))
                else:
                    name_key_pairs.append((d, extra_surname))

            sorted_all = sorted(name_key_pairs, key=lambda x: x[1].lower())
            correct_first = sorted_all[0][0]

            choices = display[:4]
            if correct_first not in choices:
                choices[0] = correct_first
            random.shuffle(choices)

            questions.append({
                "id": qid,
                "subtest": "Clerical Ability",
                "module": "Indexing and Record Organization",
                "subtopic": "Indexing Basics",
                "difficulty": "Hard",
                "question": "After proper indexing, which of the following names files FIRST?",
                "choices": choices,
                "answer": correct_first,
                "explanation": f"Index each name (prefix closed up, surname first). Compare key units alphabetically. '{correct_first}' has the key unit that comes first.",
                "tags": ["filing-order", "prefix-handling", "mixed-rules"],
                "category": ["Sub-Professional"],
                "language": "English"
            })
            qid += 1

        elif name_type == "hyphen_mix":
            part1, part2 = get_hyphenated_surname()
            closed_hyp = close_up_hyphen(part1, part2)
            surname2 = get_random_surname()
            surname3 = get_random_surname()
            while surname2 == surname3 or surname2 == part1 or surname3 == part1:
                surname2 = get_random_surname()
                surname3 = get_random_surname()

            given1 = get_random_given()
            given2 = get_random_given()
            given3 = get_random_given()

            names = [
                (f"{given1} {part1}-{part2}", closed_hyp),
                (f"{given2} {surname2}", surname2),
                (f"{given3} {surname3}", surname3),
                (f"{given1} {part1}", part1),  # Just the first part as surname
            ]

            key = f"hyp_mix_{closed_hyp}_{surname2}_{surname3}".lower()
            if key in used:
                continue
            used.add(key)

            sorted_names = sorted(names, key=lambda x: x[1].lower())
            correct_first = sorted_names[0][0]

            choices = [n[0] for n in names]
            random.shuffle(choices)

            questions.append({
                "id": qid,
                "subtest": "Clerical Ability",
                "module": "Indexing and Record Organization",
                "subtopic": "Indexing Basics",
                "difficulty": "Hard",
                "question": "After proper indexing, which of the following names files FIRST?",
                "choices": choices,
                "answer": correct_first,
                "explanation": f"Index each name (hyphen removed and closed up for compound surnames). Compare key units. '{correct_first}' files first.",
                "tags": ["filing-order", "hyphen-rule", "mixed-rules"],
                "category": ["Sub-Professional"],
                "language": "English"
            })
            qid += 1

        else:  # suffix_compare
            surname = get_random_surname()
            given = get_random_given()

            names = [
                (f"{given} {surname}", f"{surname}, {given}"),
                (f"{given} {surname} Jr.", f"{surname}, {given} (Jr.)"),
                (f"{given} {surname} Sr.", f"{surname}, {given} (Sr.)"),
                (f"{given} {surname} III", f"{surname}, {given} (III)"),
            ]

            key = f"suf_cmp_{surname}_{given}".lower()
            if key in used:
                continue
            used.add(key)

            # Filing order: plain name first, then Jr., then Sr., then III
            # Actually: plain (no suffix) < II < III < IV < Jr. < Sr.
            # Standard: Jr. before Sr. (J before S), numerals in order
            # Plain name (no suffix) files before any with suffix
            correct_order = [
                f"{given} {surname}",
                f"{given} {surname} III",
                f"{given} {surname} Jr.",
                f"{given} {surname} Sr.",
            ]

            answer = correct_order[0]  # Plain name files first
            choices = [n[0] for n in names]
            random.shuffle(choices)

            questions.append({
                "id": qid,
                "subtest": "Clerical Ability",
                "module": "Indexing and Record Organization",
                "subtopic": "Indexing Basics",
                "difficulty": "Hard",
                "question": f"After indexing, which files FIRST among these names that share the same surname and given name?",
                "choices": choices,
                "answer": answer,
                "explanation": f"When all filing units are identical, the name with no suffix files first. '{answer}' has no distinguishing suffix.",
                "tags": ["filing-order", "suffix-handling"],
                "category": ["Sub-Professional"],
                "language": "English"
            })
            qid += 1

    return questions[:200]


# ============================================================
# MAIN
# ============================================================

def main():
    easy = generate_easy_questions()
    medium = generate_medium_questions()
    hard = generate_hard_questions()

    all_questions = easy + medium + hard

    # Reassign IDs sequentially
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    # Validate
    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"
    for i, q in enumerate(all_questions):
        assert q["id"] == i + 1, f"ID mismatch at index {i}"
        assert q["answer"] in q["choices"], f"Answer not in choices for ID {q['id']}: {q['answer']}"
        if i < 200:
            assert q["difficulty"] == "Easy", f"ID {q['id']} should be Easy"
        elif i < 400:
            assert q["difficulty"] == "Medium", f"ID {q['id']} should be Medium"
        else:
            assert q["difficulty"] == "Hard", f"ID {q['id']} should be Hard"

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "indexing-and-record-organization", "indexing-basics"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_questions)} questions")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
