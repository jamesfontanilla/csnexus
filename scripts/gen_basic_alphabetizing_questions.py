"""
Generate 600-question bank for Basic Alphabetizing.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).
"""
import json
import random
import os

random.seed(42)

# Word pools organized by first letter for controlled generation
FILIPINO_SURNAMES = [
    "Abad", "Abella", "Abueva", "Acosta", "Aguilar", "Aguirre", "Alba",
    "Alcantara", "Almonte", "Alvarez", "Andrada", "Angeles", "Aquino",
    "Aragon", "Araneta", "Arroyo", "Baguio", "Balmaceda", "Bautista",
    "Bernardo", "Bondoc", "Buenaventura", "Cabrera", "Camacho", "Campos",
    "Carlos", "Carmen", "Castillo", "Castro", "Concepcion", "Cordero",
    "Cruz", "Custodio", "David", "Dela Cruz", "Dela Rosa", "Diaz",
    "Dimaculangan", "Dizon", "Domingo", "Enriquez", "Escueta", "Espino",
    "Estrada", "Evangelista", "Fernandez", "Flores", "Francisco",
    "Gabriel", "Galang", "Garcia", "Gomez", "Gonzales", "Gonzalez",
    "Guerrero", "Gutierrez", "Hernandez", "Hidalgo", "Ignacio",
    "Ilagan", "Javier", "Jimenez", "Jose", "Juan", "Lacson", "Lara",
    "Laurel", "Lazaro", "Leon", "Lim", "Lopez", "Luna", "Macapagal",
    "Macaraeg", "Magbanua", "Magsaysay", "Manalang", "Manalo",
    "Mangubat", "Manila", "Marquez", "Martinez", "Medina", "Mendoza",
    "Mercado", "Miranda", "Montano", "Morales", "Navarro", "Nicolas",
    "Ocampo", "Olivares", "Ong", "Ortega", "Padilla", "Palma",
    "Pangilinan", "Pascual", "Perez", "Pineda", "Quiambao", "Quinto",
    "Ramos", "Reyes", "Rivera", "Rodriguez", "Romero", "Rosales",
    "Roxas", "Salazar", "Salvador", "Sanchez", "Santiago", "Santillan",
    "Santos", "Soriano", "Tan", "Tolentino", "Torres", "Trinidad",
    "Valdez", "Valencia", "Vargas", "Velasco", "Villanueva", "Yap",
    "Zamora", "Zulueta"
]

OFFICE_WORDS = [
    "Accounting", "Administration", "Agenda", "Agreement", "Allocation",
    "Amendment", "Announcement", "Application", "Appointment", "Approval",
    "Archive", "Assessment", "Assignment", "Attendance", "Audit",
    "Authorization", "Badge", "Balance", "Billing", "Bond", "Budget",
    "Bulletin", "Bureau", "Business", "Calendar", "Cashier", "Catalog",
    "Certificate", "Circular", "Claim", "Clearance", "Clerk", "Client",
    "Code", "Collection", "Commission", "Committee", "Communication",
    "Compensation", "Compliance", "Conference", "Contract", "Control",
    "Correspondence", "Credential", "Data", "Database", "Deadline",
    "Delivery", "Department", "Deposit", "Designation", "Directive",
    "Disbursement", "Discipline", "Dispatch", "Division", "Document",
    "Eligibility", "Employee", "Endorsement", "Enrollment", "Equipment",
    "Evaluation", "Examination", "Expenditure", "Facility", "File",
    "Filing", "Finance", "Folder", "Form", "Grievance", "Handbook",
    "Hiring", "Identification", "Incentive", "Increment", "Index",
    "Inspection", "Insurance", "Inventory", "Invoice", "Issuance",
    "Journal", "Justification", "Ledger", "Leave", "Letter", "License",
    "Liquidation", "Logbook", "Maintenance", "Mandate", "Manual",
    "Memorandum", "Minutes", "Monitoring", "Notice", "Obligation",
    "Office", "Operation", "Order", "Ordinance", "Organization",
    "Overtime", "Payroll", "Penalty", "Pension", "Performance",
    "Permit", "Personnel", "Petition", "Placement", "Planning",
    "Policy", "Position", "Posting", "Procurement", "Promotion",
    "Property", "Proposal", "Protocol", "Provision", "Qualification",
    "Quarterly", "Questionnaire", "Quota", "Ranking", "Reclassification",
    "Record", "Recruitment", "Reference", "Register", "Regulation",
    "Reimbursement", "Remittance", "Renewal", "Report", "Requisition",
    "Resolution", "Retirement", "Revenue", "Review", "Roster", "Salary",
    "Sanction", "Schedule", "Screening", "Section", "Security",
    "Selection", "Seminar", "Service", "Specification", "Statement",
    "Stipend", "Submission", "Summary", "Supervision", "Supply",
    "Suspension", "Tally", "Tenure", "Terminal", "Training", "Transfer",
    "Transaction", "Travel", "Treasury", "Turnover", "Vacancy",
    "Validation", "Verification", "Voucher", "Waiver", "Warrant",
    "Worksheet", "Yearbook", "Zoning"
]

# Groups of words sharing first letter (for second-letter and multi-letter comparisons)
SAME_FIRST_LETTER_GROUPS = {
    "A": ["Abad", "Abella", "Acosta", "Administration", "Agenda", "Agreement",
          "Allocation", "Amendment", "Application", "Appointment", "Approval",
          "Archive", "Assessment", "Assignment", "Attendance", "Audit",
          "Authorization", "Aquino", "Aragon", "Araneta", "Alvarez"],
    "B": ["Badge", "Balance", "Balmaceda", "Bautista", "Billing", "Bond",
          "Budget", "Bulletin", "Bureau", "Business", "Bondoc", "Bernardo",
          "Buenaventura", "Baguio"],
    "C": ["Cabrera", "Calendar", "Camacho", "Campos", "Carlos", "Carmen",
          "Cashier", "Castillo", "Castro", "Certificate", "Circular", "Claim",
          "Clearance", "Clerk", "Client", "Code", "Collection", "Commission",
          "Committee", "Communication", "Compensation", "Compliance",
          "Concepcion", "Conference", "Contract", "Control", "Cordero",
          "Correspondence", "Credential", "Cruz", "Custodio"],
    "D": ["Data", "Database", "Deadline", "Dela Cruz", "Dela Rosa", "Delivery",
          "Department", "Deposit", "Designation", "Diaz", "Dimaculangan",
          "Directive", "Disbursement", "Discipline", "Dispatch", "Division",
          "Dizon", "Document", "Domingo"],
    "E": ["Eligibility", "Employee", "Endorsement", "Enrollment", "Enriquez",
          "Equipment", "Escueta", "Espino", "Estrada", "Evaluation",
          "Evangelista", "Examination", "Expenditure"],
    "F": ["Facility", "Fernandez", "File", "Filing", "Finance", "Flores",
          "Folder", "Form", "Francisco"],
    "G": ["Gabriel", "Galang", "Garcia", "Gomez", "Gonzales", "Gonzalez",
          "Grievance", "Guerrero", "Gutierrez"],
    "M": ["Macapagal", "Macaraeg", "Magbanua", "Magsaysay", "Maintenance",
          "Manalang", "Manalo", "Mandate", "Mangubat", "Manila", "Manual",
          "Marquez", "Martinez", "Medina", "Memorandum", "Mendoza", "Mercado",
          "Minutes", "Miranda", "Monitoring", "Montano", "Morales"],
    "P": ["Padilla", "Palma", "Pangilinan", "Pascual", "Payroll", "Penalty",
          "Pension", "Perez", "Performance", "Permit", "Personnel", "Petition",
          "Pineda", "Placement", "Planning", "Policy", "Position", "Posting",
          "Procurement", "Promotion", "Property", "Proposal", "Protocol",
          "Provision"],
    "R": ["Ramos", "Ranking", "Reclassification", "Record", "Recruitment",
          "Reference", "Register", "Regulation", "Reimbursement", "Remittance",
          "Renewal", "Report", "Requisition", "Resolution", "Retirement",
          "Revenue", "Review", "Reyes", "Rivera", "Rodriguez", "Romero",
          "Rosales", "Roster", "Roxas"],
    "S": ["Salazar", "Salvador", "Sanchez", "Sanction", "Santiago", "Santillan",
          "Santos", "Schedule", "Screening", "Section", "Security", "Selection",
          "Seminar", "Service", "Soriano", "Specification", "Statement",
          "Stipend", "Submission", "Summary", "Supervision", "Supply",
          "Suspension"],
    "T": ["Tally", "Tan", "Tenure", "Terminal", "Tolentino", "Torres",
          "Training", "Transaction", "Transfer", "Travel", "Treasury",
          "Trinidad", "Turnover"],
    "V": ["Vacancy", "Valdez", "Valencia", "Validation", "Vargas", "Velasco",
          "Verification", "Villanueva", "Voucher"],
}

# Shorter-word pairs for the shorter-word rule
# ONLY true prefix pairs where longer.lower().startswith(shorter.lower()) is True
SHORTER_WORD_PAIRS = [
    ("Data", "Database"), ("Clear", "Clearance"),
    ("Plan", "Planning"), ("Pay", "Payroll"), ("Form", "Format"),
    ("Record", "Recording"), ("Report", "Reporting"), ("Train", "Training"),
    ("Transfer", "Transferee"), ("Budget", "Budgeting"), ("Audit", "Auditing"),
    ("Post", "Posting"), ("Screen", "Screening"), ("Monitor", "Monitoring"),
    ("Control", "Controller"), ("Process", "Processing"),
    ("Manage", "Manager"), ("Manage", "Management"), ("Over", "Overtime"),
    ("Account", "Accounting"), ("Employ", "Employer"), ("Employ", "Employment"),
    ("Assign", "Assigning"), ("Assess", "Assessing"), ("Attend", "Attending"),
    ("Contract", "Contractor"), ("Direct", "Directive"), ("Direct", "Directory"),
    ("Dispatch", "Dispatcher"), ("Document", "Documentary"),
    ("Endorse", "Endorsement"), ("Enroll", "Enrollment"), ("Equip", "Equipment"),
    ("Grievance", "Grievances"), ("Hand", "Handbook"),
    ("Inspect", "Inspector"), ("Invoice", "Invoices"),
    ("Journal", "Journals"), ("Ledger", "Ledgers"),
    ("Log", "Logbook"), ("Mail", "Mailing"), ("Memo", "Memorandum"),
    ("Order", "Ordering"), ("Organ", "Organization"), ("Pay", "Payment"),
    ("Permit", "Permits"), ("Person", "Personnel"), ("Position", "Positions"),
    ("Rank", "Ranking"), ("Refer", "Reference"),
    ("Roster", "Rosters"), ("Schedule", "Schedules"),
    ("Section", "Sections"), ("Stipend", "Stipends"),
    ("Tally", "Tallying"), ("Tenure", "Tenured"), ("Turn", "Turnover"),
    ("Vouch", "Voucher"), ("Warrant", "Warrants"), ("Work", "Worksheet"),
    ("Board", "Boardroom"), ("Book", "Bookkeeper"), ("Brief", "Briefing"),
    ("Cash", "Cashier"), ("Chair", "Chairman"), ("Correspond", "Correspondence"),
    ("Counsel", "Counselor"), ("Counter", "Countersign"),
]


def alphabetical_sort_key(word: str) -> str:
    """Generate sort key: case-insensitive, character by character."""
    return word.lower()


# Validate SHORTER_WORD_PAIRS at import time
for short, long_ in SHORTER_WORD_PAIRS:
    assert long_.lower().startswith(short.lower()), \
        f"Invalid pair: '{long_}' does not start with '{short}'"
    assert len(short) < len(long_), \
        f"Invalid pair: '{short}' is not shorter than '{long_}'"


def sorted_alphabetically(words: list[str]) -> list[str]:
    """Sort words in alphabetical order (case-insensitive)."""
    return sorted(words, key=alphabetical_sort_key)


def get_first(words: list[str]) -> str:
    """Return the word that comes first alphabetically."""
    return sorted_alphabetically(words)[0]


def get_last(words: list[str]) -> str:
    """Return the word that comes last alphabetically."""
    return sorted_alphabetically(words)[-1]


def explain_first(words: list[str]) -> str:
    """Generate explanation for 'which comes first' questions."""
    ordered = sorted_alphabetically(words)
    first = ordered[0]
    # Determine comparison level
    first_letters = [w[0].lower() for w in words]
    if len(set(first_letters)) == len(first_letters):
        return (f"Compare first letters: {', '.join(w[0].upper() for w in words)}. "
                f"{first[0].upper()} comes earliest in the alphabet, so {first} is filed first.")
    else:
        # Find where difference occurs
        return _explain_comparison(ordered, "first")


def explain_last(words: list[str]) -> str:
    """Generate explanation for 'which comes last' questions."""
    ordered = sorted_alphabetically(words)
    last = ordered[-1]
    first_letters = [w[0].lower() for w in words]
    if len(set(first_letters)) == len(first_letters):
        return (f"Compare first letters: {', '.join(w[0].upper() for w in words)}. "
                f"{last[0].upper()} comes latest in the alphabet, so {last} is filed last.")
    else:
        return _explain_comparison(ordered, "last")


def _explain_comparison(ordered: list[str], position: str) -> str:
    """Generate detailed comparison explanation."""
    target = ordered[0] if position == "first" else ordered[-1]
    # Find first differing position among all words
    min_len = min(len(w) for w in ordered)
    diff_pos = 0
    for i in range(min_len):
        letters_at_pos = set(w[i].lower() for w in ordered)
        if len(letters_at_pos) > 1:
            diff_pos = i
            break
    else:
        # Difference is in length (shorter word rule)
        return (f"All compared letters are identical. The shorter word '{target}' "
                f"is filed {'first' if position == 'first' else 'last'} "
                f"by the shorter-word rule.")

    pos_name = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth"}
    pos_label = pos_name.get(diff_pos, f"position {diff_pos + 1}")

    if position == "first":
        return (f"Compare {pos_label} letters where they differ: "
                f"{', '.join(w[diff_pos].lower() for w in ordered)}. "
                f"'{target[diff_pos].lower()}' comes earliest, so {target} is filed first.")
    else:
        return (f"Compare {pos_label} letters where they differ: "
                f"{', '.join(w[diff_pos].lower() for w in ordered)}. "
                f"'{target[diff_pos].lower()}' comes latest, so {target} is filed last.")


def explain_order(words: list[str]) -> str:
    """Generate explanation for 'correct order' questions."""
    ordered = sorted_alphabetically(words)
    return (f"Comparing letter by letter: the correct alphabetical order is "
            f"{', '.join(ordered)}.")


def explain_position(target: str, words: list[str]) -> str:
    """Generate explanation for 'which position' questions."""
    ordered = sorted_alphabetically(words)
    pos = ordered.index(target) + 1
    ordinals = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
    return (f"In alphabetical order: {', '.join(ordered)}. "
            f"{target} is in the {ordinals[pos]} position.")


def determine_tags(words: list[str]) -> list[str]:
    """Determine appropriate tags based on the comparison type."""
    tags = []
    first_letters = [w[0].lower() for w in words]

    if len(set(first_letters)) == len(first_letters):
        tags.append("first-letter")
    else:
        # Check if second letter differs
        same_first = [w for w in words if w[0].lower() == words[0][0].lower()]
        if len(same_first) >= 2:
            second_letters = [w[1].lower() for w in same_first if len(w) > 1]
            if len(set(second_letters)) == len(second_letters):
                tags.append("second-letter")
            else:
                tags.append("multi-letter")

    # Check for shorter-word rule (one word is a strict prefix of another)
    for i, w1 in enumerate(words):
        for w2 in words[i+1:]:
            if len(w1) == len(w2):
                continue
            shorter = min(w1, w2, key=len)
            longer = max(w1, w2, key=len)
            if longer.lower().startswith(shorter.lower()):
                tags.append("shorter-word-rule")
                break
        if "shorter-word-rule" in tags:
            break

    if not tags:
        tags.append("letter-comparison")

    return tags


def pick_distinct_first_letter_words(n: int, pool: list[str]) -> list[str] | None:
    """Pick n words with distinct first letters from pool."""
    by_letter = {}
    for w in pool:
        fl = w[0].lower()
        if fl not in by_letter:
            by_letter[fl] = []
        by_letter[fl].append(w)
    if len(by_letter) < n:
        return None
    letters = random.sample(list(by_letter.keys()), n)
    return [random.choice(by_letter[l]) for l in letters]


def pick_same_first_letter_words(n: int, letter: str = None) -> list[str] | None:
    """Pick n words sharing the same first letter."""
    if letter is None:
        available = [k for k, v in SAME_FIRST_LETTER_GROUPS.items() if len(v) >= n]
        if not available:
            return None
        letter = random.choice(available)
    group = SAME_FIRST_LETTER_GROUPS.get(letter, [])
    if len(group) < n:
        return None
    return random.sample(group, n)


def pick_shorter_word_set() -> list[str]:
    """Pick a shorter-word pair plus 1-2 distractors."""
    pair = random.choice(SHORTER_WORD_PAIRS)
    short, long_ = pair
    # Add a distractor with different first letter
    all_words = OFFICE_WORDS + FILIPINO_SURNAMES
    distractors = [w for w in all_words
                   if w[0].lower() != short[0].lower() and w != short and w != long_]
    extra = random.sample(distractors, 2)
    return [short, long_] + extra


def generate_easy_questions() -> list[dict]:
    """Generate 200 Easy questions (IDs 1-200)."""
    questions = []
    used_sets = set()
    qid = 1
    all_pool = OFFICE_WORDS + FILIPINO_SURNAMES

    # Type 1: Which comes FIRST? (first-letter comparison, 3 choices) — 60 questions
    attempts = 0
    while len(questions) < 60 and attempts < 5000:
        attempts += 1
        words = pick_distinct_first_letter_words(3, all_pool)
        if words is None:
            continue
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Easy",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": ["first-letter"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 2: Which comes LAST? (first-letter comparison, 3 choices) — 50 questions
    attempts = 0
    while len(questions) < 110 and attempts < 5000:
        attempts += 1
        words = pick_distinct_first_letter_words(3, all_pool)
        if words is None:
            continue
        key = ("last",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_last(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Easy",
            "question": "Which of the following should be filed LAST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_last(words),
            "tags": ["first-letter"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 3: Correct order (first-letter, 3 items) — 50 questions
    attempts = 0
    while len(questions) < 160 and attempts < 5000:
        attempts += 1
        words = pick_distinct_first_letter_words(3, all_pool)
        if words is None:
            continue
        key = ("order",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        correct_order = sorted_alphabetically(words)
        # Generate distractors (wrong orderings)
        all_perms = []
        from itertools import permutations
        for p in permutations(words):
            seq = list(p)
            if seq != correct_order:
                all_perms.append(seq)
        if len(all_perms) < 3:
            continue
        wrong = random.sample(all_perms, 3)
        choices = [", ".join(correct_order)] + [", ".join(w) for w in wrong]
        random.shuffle(choices)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Easy",
            "question": f"Arrange the following in correct alphabetical order: {', '.join(words)}. Which sequence is correct?",
            "choices": choices,
            "answer": ", ".join(correct_order),
            "explanation": explain_order(words),
            "tags": ["first-letter", "sequencing"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 4: Second-letter comparison, which comes FIRST (3 choices) — 40 questions
    attempts = 0
    while len(questions) < 200 and attempts < 5000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        words = pick_same_first_letter_words(3, letter)
        if words is None:
            continue
        # Ensure second letters are all different for Easy
        second_letters = [w[1].lower() if len(w) > 1 else "" for w in words]
        if len(set(second_letters)) != len(second_letters):
            continue
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Easy",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": ["second-letter"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions


def generate_medium_questions() -> list[dict]:
    """Generate 200 Medium questions (IDs 201-400)."""
    questions = []
    used_sets = set()
    qid = 201
    all_pool = OFFICE_WORDS + FILIPINO_SURNAMES

    # Type 1: Which comes FIRST? (same first letter, 4 choices) — 50 questions
    attempts = 0
    while len(questions) < 50 and attempts < 5000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        words = pick_same_first_letter_words(4, letter)
        if words is None:
            continue
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Medium",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": determine_tags(words),
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: Which comes LAST? (same first letter, 4 choices) — 40 questions
    attempts = 0
    while len(questions) < 90 and attempts < 5000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        words = pick_same_first_letter_words(4, letter)
        if words is None:
            continue
        key = ("last",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_last(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Medium",
            "question": "Which of the following should be filed LAST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_last(words),
            "tags": determine_tags(words),
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 3: Correct order (same first letter, 3-4 items) — 40 questions
    attempts = 0
    while len(questions) < 130 and attempts < 5000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        n = random.choice([3, 4])
        words = pick_same_first_letter_words(n, letter)
        if words is None:
            continue
        key = ("order",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        correct_order = sorted_alphabetically(words)
        from itertools import permutations
        all_perms = []
        for p in permutations(words):
            seq = list(p)
            if seq != correct_order:
                all_perms.append(seq)
        if len(all_perms) < 3:
            continue
        wrong = random.sample(all_perms, 3)
        choices = [", ".join(correct_order)] + [", ".join(w) for w in wrong]
        random.shuffle(choices)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Medium",
            "question": f"Arrange the following in correct alphabetical order: {', '.join(words)}. Which sequence is correct?",
            "choices": choices,
            "answer": ", ".join(correct_order),
            "explanation": explain_order(words),
            "tags": determine_tags(words) + ["sequencing"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 4: Which position? (4 items, same first letter) — 35 questions
    attempts = 0
    while len(questions) < 165 and attempts < 5000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        words = pick_same_first_letter_words(4, letter)
        if words is None:
            continue
        key = ("pos",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        ordered = sorted_alphabetically(words)
        target = random.choice(words)
        pos = ordered.index(target) + 1
        ordinals = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
        random.shuffle(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Medium",
            "question": f"In what position would \"{target}\" be filed among the following: {', '.join(words)}?",
            "choices": ["1st", "2nd", "3rd", "4th"],
            "answer": ordinals[pos],
            "explanation": explain_position(target, words),
            "tags": determine_tags(words) + ["position"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 5: Shorter-word rule questions — 35 questions
    attempts = 0
    while len(questions) < 200 and attempts < 5000:
        attempts += 1
        pair = random.choice(SHORTER_WORD_PAIRS)
        short, long_ = pair
        # Pick 2 more words with different first letters
        distractors = [w for w in all_pool
                       if w[0].lower() != short[0].lower()
                       and w != short and w != long_]
        if len(distractors) < 2:
            continue
        extras = random.sample(distractors, 2)
        words = [short, long_] + extras
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Medium",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": ["shorter-word-rule"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions


def generate_hard_questions() -> list[dict]:
    """Generate 200 Hard questions (IDs 401-600)."""
    questions = []
    used_sets = set()
    qid = 401
    all_pool = OFFICE_WORDS + FILIPINO_SURNAMES

    # Type 1: Which comes FIRST? (4-5 items, same first letter, multi-letter) — 45 questions
    attempts = 0
    while len(questions) < 45 and attempts < 8000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        group = SAME_FIRST_LETTER_GROUPS[letter]
        if len(group) < 5:
            continue
        n = random.choice([4, 5])
        words = random.sample(group, min(n, len(group)))
        if len(words) < n:
            continue
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Hard",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": determine_tags(words),
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 2: Which comes LAST? (4-5 items, multi-letter) — 40 questions
    attempts = 0
    while len(questions) < 85 and attempts < 8000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        group = SAME_FIRST_LETTER_GROUPS[letter]
        if len(group) < 5:
            continue
        n = random.choice([4, 5])
        words = random.sample(group, min(n, len(group)))
        if len(words) < n:
            continue
        key = ("last",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_last(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Hard",
            "question": "Which of the following should be filed LAST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_last(words),
            "tags": determine_tags(words),
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 3: Correct order (4-5 items, same first letter) — 40 questions
    attempts = 0
    while len(questions) < 125 and attempts < 8000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        group = SAME_FIRST_LETTER_GROUPS[letter]
        n = random.choice([4, 5])
        if len(group) < n:
            continue
        words = random.sample(group, n)
        key = ("order",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        correct_order = sorted_alphabetically(words)
        from itertools import permutations
        # For 5 items, generate wrong orderings by swapping
        if n <= 4:
            all_perms = []
            for p in permutations(words):
                seq = list(p)
                if seq != correct_order:
                    all_perms.append(seq)
            if len(all_perms) < 3:
                continue
            wrong = random.sample(all_perms, 3)
        else:
            # For 5 items, create plausible wrong orderings by swapping adjacent
            wrong = []
            for _ in range(20):
                w = correct_order.copy()
                i = random.randint(0, len(w) - 2)
                w[i], w[i+1] = w[i+1], w[i]
                if w != correct_order and w not in wrong:
                    wrong.append(w)
            if len(wrong) < 3:
                continue
            wrong = wrong[:3]
        choices = [", ".join(correct_order)] + [", ".join(w) for w in wrong]
        random.shuffle(choices)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Hard",
            "question": f"Arrange the following in correct alphabetical order: {', '.join(words)}. Which sequence is correct?",
            "choices": choices,
            "answer": ", ".join(correct_order),
            "explanation": explain_order(words),
            "tags": determine_tags(words) + ["sequencing"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1


    # Type 4: Shorter-word rule with similar words (tricky) — 35 questions
    attempts = 0
    while len(questions) < 160 and attempts < 8000:
        attempts += 1
        pair = random.choice(SHORTER_WORD_PAIRS)
        short, long_ = pair
        # Add words with same first letter to make it harder
        same_letter_pool = [w for w in all_pool
                            if w[0].lower() == short[0].lower()
                            and w.lower() != short.lower()
                            and w.lower() != long_.lower()]
        if len(same_letter_pool) < 2:
            continue
        extras = random.sample(same_letter_pool, 2)
        words = [short, long_] + extras
        key = tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        random.shuffle(words)
        answer = get_first(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Hard",
            "question": "Which of the following should be filed FIRST?",
            "choices": words,
            "answer": answer,
            "explanation": explain_first(words),
            "tags": ["shorter-word-rule", "multi-letter"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    # Type 5: Position questions with 4-5 similar items — 40 questions
    attempts = 0
    while len(questions) < 200 and attempts < 8000:
        attempts += 1
        letter = random.choice(list(SAME_FIRST_LETTER_GROUPS.keys()))
        group = SAME_FIRST_LETTER_GROUPS[letter]
        if len(group) < 4:
            continue
        words = random.sample(group, 4)
        key = ("pos",) + tuple(sorted(w.lower() for w in words))
        if key in used_sets:
            continue
        used_sets.add(key)
        ordered = sorted_alphabetically(words)
        # Pick a non-obvious position (2nd or 3rd)
        target_idx = random.choice([1, 2])
        target = ordered[target_idx]
        pos = target_idx + 1
        ordinals = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
        random.shuffle(words)
        questions.append({
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Alphabetical Filing",
            "subtopic": "Basic Alphabetizing",
            "difficulty": "Hard",
            "question": f"In what position would \"{target}\" be filed among the following: {', '.join(words)}?",
            "choices": ["1st", "2nd", "3rd", "4th"],
            "answer": ordinals[pos],
            "explanation": explain_position(target, words),
            "tags": determine_tags(words) + ["position"],
            "category": ["Sub-Professional"],
            "language": "English"
        })
        qid += 1

    return questions


def validate_questions(questions: list[dict]) -> bool:
    """Validate all questions have correct answers."""
    errors = []
    for q in questions:
        if q["answer"] not in q["choices"]:
            errors.append(f"ID {q['id']}: answer '{q['answer']}' not in choices")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return False
    return True


def main():
    print("Generating Easy questions (1-200)...")
    easy = generate_easy_questions()
    print(f"  Generated {len(easy)} Easy questions")

    print("Generating Medium questions (201-400)...")
    medium = generate_medium_questions()
    print(f"  Generated {len(medium)} Medium questions")

    print("Generating Hard questions (401-600)...")
    hard = generate_hard_questions()
    print(f"  Generated {len(hard)} Hard questions")

    all_questions = easy + medium + hard

    # Re-number sequentially
    for i, q in enumerate(all_questions, 1):
        q["id"] = i

    print(f"\nTotal questions: {len(all_questions)}")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")

    # Validate
    if not validate_questions(all_questions):
        print("\nVALIDATION FAILED — fix errors above")
        return

    print("\nValidation passed — all answers match choices")

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "alphabetical-filing", "basic-alphabetizing"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to: {output_path}")


if __name__ == "__main__":
    main()
